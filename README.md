# CONUS Per Diem Bid Desk

Offline FY2026 GSA CONUS per diem desk: 297 localities, 650 season rows, M&IE splits, POV mileage, cited lodging-tax benches, provided-meal deductions, and a no-network trip quote so you can price travel into a bid today.

## Who it's for

GovCon estimators, traveling consultants, and finance ops who need a GSA ceiling **plus the lodging tax GSA left out of the cap**.

## What's included

- `data/localities.csv` — 297 destinations (296 NSAs + Standard CONUS $110+$68)
- `data/seasons.csv` — 650 lodging seasons (peak/off-peak)
- `data/monthly.csv` — lodging + daily cap by FY month (Oct–Sep)
- `data/mie_breakdown.csv` — $68/$74/$80/$86/$92 meal splits + 75% first/last
- `data/mileage.csv` — GSA POV + IRS business cents, Jan–Jun and Jul–Dec 2026
- `data/lodging_tax.csv` — cited CONUS lodging-tax benches (Austin 17%, SF 14%+TID, DC 14.95%, MA floor 8.45%, NYC **flat fees only**)
- `data/highest_caps.csv` — 40 highest peak daily caps (Park City $575 …)
- `data/trip_worksheet.csv` — five sample trips to quote
- `desk/quote.py` — offline calculator (`--tax`, `--meals`, `--batch`, `--json`)
- `examples/` — Austin, NYC peak vs off-peak, DC two-traveler, lodging-tax leak
- `sources/FY2026_PerDiemMasterRatesFile.xlsx` — official GSA workbook copy
- `data/SOURCES.md` — citations

## Quick start

```bash
python3 desk/quote.py --dest Austin --state TX --start 2026-03-09 --end 2026-03-12
python3 desk/quote.py --dest Austin --state TX --start 2026-03-09 --end 2026-03-12 --tax
python3 desk/quote.py --dest Austin --state TX --start 2026-03-09 --end 2026-03-12 --tax --meals lunch
python3 desk/quote.py --batch data/trip_worksheet.csv --tax
python3 desk/quote.py --list CA
```

First and last calendar days use 75% M&IE. Lodging nights = calendar days − 1. Lodging tax is **not** in the GSA cap (FTR 301-11.27); `--tax` adds a cited local bench.

No API keys. Files work after Gamut credits are gone.

## Price

$49 USD. Unlimited non-exclusive buyers; copies may be resold. Pay https://buy.stripe.com/6oU8wQ05i9357FE27HcIE03 then open a GitHub issue titled `CLAIM: CONUS Per Diem Bid Desk` with the receipt last-4. If checkout is down, star + watch and open the same CLAIM issue.

## License

MIT for the desk code, CSVs, and docs. The GSA workbook and rate figures are U.S. government works. See LICENSE.

## Foundry

Shipped by Night Shift Foundry for Dakota (@Allspecs-yoda).
SKU: NSF-20260826-PERDIEM-BID | Decision: list | Cycle: 2026-08-26 (hunt polish)
