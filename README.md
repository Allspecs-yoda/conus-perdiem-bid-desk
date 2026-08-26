# CONUS Per Diem Bid Desk

Offline FY2026 GSA CONUS per diem desk: 297 localities, 650 season rows, M&IE splits, POV mileage, and a no-network trip quote so you can price travel into a bid today.

## Who it's for

GovCon estimators, traveling consultants, and finance ops who need a GSA ceiling on a trip without an API key.

## What's included

- `data/localities.csv` — 297 destinations (296 NSAs + Standard CONUS $110+$68)
- `data/seasons.csv` — 650 lodging seasons (peak/off-peak)
- `data/monthly.csv` — lodging + daily cap by FY month (Oct–Sep)
- `data/mie_breakdown.csv` — $68/$74/$80/$86/$92 meal splits + 75% first/last
- `data/mileage.csv` — GSA POV + IRS business cents, Jan–Jun and Jul–Dec 2026
- `data/highest_caps.csv` — 40 highest peak daily caps (Park City $575 …)
- `data/trip_worksheet.csv` — five sample trips to quote
- `desk/quote.py` — offline calculator
- `examples/` — Austin, NYC peak vs off-peak, DC two-traveler
- `sources/FY2026_PerDiemMasterRatesFile.xlsx` — official GSA workbook copy
- `data/SOURCES.md` — citations

## Quick start

```bash
python3 desk/quote.py --dest Austin --state TX --start 2026-03-09 --end 2026-03-12
python3 desk/quote.py --dest "New York City" --start 2026-09-14 --end 2026-09-18
python3 desk/quote.py --list CA
```

First and last calendar days use 75% M&IE. Lodging nights = calendar days − 1. Lodging tax is **not** in the cap.

No API keys. Files work after Gamut credits are gone.

## Price

$49 USD. Unlimited non-exclusive buyers; copies may be resold. Pay https://buy.stripe.com/6oU8wQ05i9357FE27HcIE03 then open a GitHub issue titled `CLAIM: CONUS Per Diem Bid Desk` with the receipt last-4. If checkout is down, star + watch and open the same CLAIM issue.

## License

MIT for the desk code, CSVs, and docs. The GSA workbook and rate figures are U.S. government works. See LICENSE.

## Foundry

Shipped by Night Shift Foundry for Dakota (@Allspecs-yoda).
SKU: NSF-20260826-PERDIEM-BID | Decision: list | Cycle: 2026-08-26
