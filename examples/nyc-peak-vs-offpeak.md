# Worked example — NYC peak vs off-peak (same 4-night trip)

**Locality:** New York City (Bronx / Kings / New York / Queens / Richmond), dest_id 266. M&IE $92 year-round. Lodging is seasonal.

GSA FY2026 lodging:

| Season | Lodging / night |
| --- | --- |
| Oct 1 – Dec 31 | $342 |
| Jan 1 – Feb 28 | $179 |
| Mar 1 – Jun 30 | $281 |
| Jul 1 – Aug 31 | $237 |
| Sep 1 – Sep 30 | $342 |

M&IE $92 first/last = $69.00.

## Peak (Sep 14–18, 2026) — 4 nights, 5 calendar days, 1 person

```bash
python3 desk/quote.py --dest "New York City" --start 2026-09-14 --end 2026-09-18
```

| | Amount |
| --- | --- |
| Lodging 4 × $342 | $1,368.00 |
| M&IE 3 × $92 + 2 × $69 | $414.00 |
| **Trip cap** | **$1,782.00** |

## Off-peak (Jan 12–16, 2026)

```bash
python3 desk/quote.py --dest "New York City" --start 2026-01-12 --end 2026-01-16
```

| | Amount |
| --- | --- |
| Lodging 4 × $179 | $716.00 |
| M&IE same | $414.00 |
| **Trip cap** | **$1,130.00** |

**Delta: $652.** Pricing a January trip at the September cap (or the reverse) is how bids lose or get protested. Use the month that matches travel dates.

With 80 POV miles in January (GSA auto $0.725 through 2026-06-30):

```bash
python3 desk/quote.py --dest "New York City" --start 2026-01-12 --end 2026-01-16 --miles 80
```

Adds $58.00 → **$1,188.00**.
