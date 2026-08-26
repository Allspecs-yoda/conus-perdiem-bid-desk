# Worked example — lodging tax is not in the GSA cap

GSA FAQ Q11 and FTR 301-11.27: CONUS lodging taxes are reimbursable as a **miscellaneous** expense, limited to tax on reimbursable lodging. Bidding the cap alone understates travel ODC.

## Austin, TX · 9–12 Mar 2026 · 1 person

GSA ceiling (no tax): lodging 3 × $187 + M&IE $280 = **$841.00**.

Cited tax stack (Texas Comptroller 6% + City of Austin 11% = 17%):

```bash
python3 desk/quote.py --dest Austin --state TX --start 2026-03-09 --end 2026-03-12 --tax
```

Lodging tax bench = 17% × $561 = **$95.37**. Bid line = **$936.37**.

If the on-site includes a hosted lunch every day (`--meals lunch`), M&IE drops $22/day → GSA cap **$753.00**, tax still **$95.37**, bid line **$848.37**.

## NYC flats only (understates)

NYC.gov documents $2.00/room/day occupancy fee (rent ≥ $40) + NYS $1.50 unit fee. The occupancy **percent** and NY/NYC sales tax are **not** printed on that page, so this pack does **not** invent them.

```bash
python3 desk/quote.py --dest "New York City" --start 2026-09-14 --end 2026-09-18 --tax
```

Adds $3.50 × 4 nights = **$14.00** only. Do not treat $1,796 as the full NYC tax-inclusive bid.

## DC 14.95% (OCFO rate list)

```bash
python3 desk/quote.py --dest "District of Columbia" --start 2026-03-03 --end 2026-03-05 --people 2 --tax
```

GSA cap $1,564.00 + 14.95% × $1,104 lodging = $165.05 → **$1,729.05**. Federal travelers may be exempt — confirm before bidding tax as zero.

## Batch five worksheet trips

```bash
python3 desk/quote.py --batch data/trip_worksheet.csv --tax
```

Expected:

| trip | dest | gsa_cap | tax_bench | bid_line |
| --- | --- | ---: | ---: | ---: |
| T-001 | Austin | $841.00 | $95.37 | $936.37 |
| T-002 | NYC peak | $1,782.00 | $14.00 | $1,796.00 |
| T-003 | NYC off-peak + 80 mi | $1,188.00 | $14.00 | $1,202.00 |
| T-004 | DC × 2 | $1,564.00 | $165.05 | $1,729.05 |
| T-005 | Standard CONUS | $655.00 | $0.00 | $655.00 |
