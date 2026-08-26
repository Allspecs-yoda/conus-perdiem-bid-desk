#!/usr/bin/env python3
"""CONUS Per Diem Bid Desk — offline trip quote.

No network. No API keys. Reads ../data/*.csv next to this file.

Usage:
  python3 desk/quote.py --dest "Austin" --state TX --start 2026-03-09 --end 2026-03-12
  python3 desk/quote.py --dest "New York City" --start 2026-09-14 --end 2026-09-18 --miles 40
  python3 desk/quote.py --list CA
  python3 desk/quote.py --dest "Standard CONUS" --start 2026-01-05 --end 2026-01-08 --people 2

First and last calendar days of the trip get 75% M&IE (GSA first/last-day rule).
Lodging nights = calendar days − 1. Mid-trip days get 100% M&IE + lodging.
"""
from __future__ import annotations

import argparse
import csv
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

MONTH_ABBR = {
    1: "jan", 2: "feb", 3: "mar", 4: "apr", 5: "may", 6: "jun",
    7: "jul", 8: "aug", 9: "sep", 10: "oct", 11: "nov", 12: "dec",
}


def load_csv(name: str) -> list[dict]:
    path = DATA / name
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def parse_date(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def daterange(start: date, end: date):
    d = start
    while d <= end:
        yield d
        d += timedelta(days=1)


def find_dest(localities: list[dict], needle: str, state: str | None) -> dict:
    n = needle.strip().lower()
    hits = []
    for row in localities:
        dest = row["destination"].lower()
        st = row["state"].upper()
        if state and st not in {state.upper(), "CONUS"}:
            continue
        if n == dest or n in dest or n == row["dest_id"]:
            hits.append(row)
    if not hits:
        # fuzzy token
        for row in localities:
            dest = row["destination"].lower()
            st = row["state"].upper()
            if state and st not in {state.upper(), "CONUS"}:
                continue
            if n in dest or n in row["county"].lower():
                hits.append(row)
    if not hits:
        raise SystemExit(
            f"No locality matched {needle!r}"
            + (f" in {state}" if state else "")
            + ". Try --list ST or --dest 'Standard CONUS'."
        )
    if len(hits) > 1 and not any(h["destination"].lower() == n for h in hits):
        names = ", ".join(f"{h['destination']} ({h['state']})" for h in hits[:12])
        raise SystemExit(f"Ambiguous. Matches: {names}. Pass --state or a tighter --dest.")
    exact = [h for h in hits if h["destination"].lower() == n]
    return exact[0] if exact else hits[0]


def monthly_for(dest_id: str, monthly: list[dict]) -> dict:
    for row in monthly:
        if row["dest_id"] == dest_id:
            return row
    raise SystemExit(f"monthly.csv missing dest_id={dest_id}")


def mie_row(total: int, mie_table: list[dict]) -> dict:
    for row in mie_table:
        if int(row["mie_total"]) == total:
            return row
    raise SystemExit(f"No M&IE breakdown for ${total}")


def pov_rate(trip_start: date, mileage: list[dict]) -> float:
    gsa = [
        r
        for r in mileage
        if r["authority"] == "GSA POV"
        and r["period_start"] <= trip_start.isoformat() <= r["period_end"]
    ]
    if not gsa:
        gsa = [r for r in mileage if r["authority"] == "GSA POV"]
        gsa.sort(key=lambda r: r["period_start"], reverse=True)
    return float(gsa[0]["auto_authorized"])


def quote(dest: dict, month_row: dict, start: date, end: date, people: int, miles: float, mie_table, mileage) -> dict:
    if end < start:
        raise SystemExit("--end must be on or after --start")
    days = list(daterange(start, end))
    n_days = len(days)
    n_nights = max(0, n_days - 1)
    mie = int(dest["mie"])
    split = mie_row(mie, mie_table)
    first_last = float(split["first_last"])
    lodging_by_day = []
    mie_by_day = []
    for i, d in enumerate(days):
        key = MONTH_ABBR[d.month]
        lodge = int(month_row[f"lodging_{key}"])
        is_travel_day = i == 0 or i == n_days - 1
        mie_amt = first_last if is_travel_day else float(mie)
        lodge_amt = 0 if i == n_days - 1 else lodge  # no lodging on last calendar day
        lodging_by_day.append((d, lodge_amt, "travel-day" if is_travel_day else "full"))
        mie_by_day.append((d, mie_amt, "75%" if is_travel_day else "100%"))
    lodging_sub = sum(x[1] for x in lodging_by_day) * people
    mie_sub = sum(x[1] for x in mie_by_day) * people
    rate = pov_rate(start, mileage)
    miles_sub = round(miles * rate, 2)
    total = lodging_sub + mie_sub + miles_sub
    return {
        "dest": dest,
        "start": start,
        "end": end,
        "people": people,
        "n_days": n_days,
        "n_nights": n_nights,
        "mie": mie,
        "lodging_sub": lodging_sub,
        "mie_sub": mie_sub,
        "miles": miles,
        "mile_rate": rate,
        "miles_sub": miles_sub,
        "total": total,
        "lodging_by_day": lodging_by_day,
        "mie_by_day": mie_by_day,
        "split": split,
    }


def money(n: float) -> str:
    return f"${n:,.2f}"


def print_quote(q: dict) -> None:
    d = q["dest"]
    print(f"CONUS Per Diem Bid Desk — trip quote")
    print(f"Locality: {d['destination']}, {d['state']}  (dest_id={d['dest_id']})")
    print(f"County:   {d['county']}")
    print(f"Window:   {q['start'].isoformat()} → {q['end'].isoformat()}  ({q['n_days']} calendar days, {q['n_nights']} lodging nights)")
    print(f"People:   {q['people']}")
    print(f"M&IE:     ${q['mie']}/full day; first/last ${q['split']['first_last']}")
    print()
    print("Day-by-day (per person):")
    print(f"{'date':<12} {'kind':<12} {'lodging':>10} {'M&IE':>10} {'day total':>12}")
    for (d1, lodge, kind), (_, mie_amt, mie_kind) in zip(q["lodging_by_day"], q["mie_by_day"]):
        print(f"{d1.isoformat():<12} {kind:<12} {money(lodge):>10} {money(mie_amt):>10} {money(lodge+mie_amt):>12}")
    print()
    print(f"Lodging × {q['people']}: {money(q['lodging_sub'])}")
    print(f"M&IE × {q['people']}:    {money(q['mie_sub'])}")
    if q["miles"]:
        print(f"POV miles {q['miles']:.1f} × {q['mile_rate']:.3f}: {money(q['miles_sub'])}")
    print(f"TRIP CAP (GSA ceiling, excl. lodging tax): {money(q['total'])}")
    print()
    print("Not a billing determination. Verify at gsa.gov before voucher. Lodging tax is extra.")


def main() -> None:
    p = argparse.ArgumentParser(description="Offline GSA FY2026 CONUS per diem trip quote")
    p.add_argument("--dest", help="Destination name or dest_id")
    p.add_argument("--state", help="Two-letter state (disambiguates)")
    p.add_argument("--start", help="YYYY-MM-DD first travel day")
    p.add_argument("--end", help="YYYY-MM-DD last travel day")
    p.add_argument("--people", type=int, default=1)
    p.add_argument("--miles", type=float, default=0.0, help="POV automobile miles (GSA authorized rate)")
    p.add_argument("--list", metavar="ST", help="List localities in a state (or ALL)")
    args = p.parse_args()

    localities = load_csv("localities.csv")
    monthly = load_csv("monthly.csv")
    mie_table = load_csv("mie_breakdown.csv")
    mileage = load_csv("mileage.csv")

    if args.list:
        st = args.list.upper()
        rows = localities if st == "ALL" else [r for r in localities if r["state"] == st]
        if not rows:
            raise SystemExit(f"No rows for {st}")
        print(f"{'id':>4} {'ST':<5} {'destination':<40} {'daily min-max':>16} seasonal")
        for r in rows:
            print(
                f"{r['dest_id']:>4} {r['state']:<5} {r['destination']:<40} "
                f"{r['daily_min']:>6}-{r['daily_max']:<6} {r['seasonal']}"
            )
        return

    if not (args.dest and args.start and args.end):
        p.print_help()
        sys.exit(2)

    dest = find_dest(localities, args.dest, args.state)
    month_row = monthly_for(dest["dest_id"], monthly)
    q = quote(dest, month_row, parse_date(args.start), parse_date(args.end), args.people, args.miles, mie_table, mileage)
    print_quote(q)


if __name__ == "__main__":
    main()
