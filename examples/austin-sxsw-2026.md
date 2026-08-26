# Worked example — Austin, TX · 3 nights · 1 person

**Scenario:** A contractor flies to Austin for a client on-site. Travel Mon 2026-03-09, return Thu 2026-03-12. No POV miles billed.

**Locality:** Austin, Travis County, TX (dest_id 343). FY2026 GSA: lodging $187 in Jan–Mar, M&IE $80.

## Day math

| Date | Kind | Lodging | M&IE | Day |
| --- | --- | --- | --- | --- |
| 2026-03-09 | first travel day | $187 | $60.00 (75%) | $247.00 |
| 2026-03-10 | full | $187 | $80.00 | $267.00 |
| 2026-03-11 | full | $187 | $80.00 | $267.00 |
| 2026-03-12 | last travel day | $0 (no night) | $60.00 (75%) | $60.00 |
| **Trip cap** | 3 nights + 4 M&IE days | **$561** | **$280.00** | **$841.00** |

M&IE $80 split (GSA): breakfast $20, lunch $22, dinner $33, incidental $5. First/last = $60.00.

## Command

```bash
python3 desk/quote.py --dest Austin --state TX --start 2026-03-09 --end 2026-03-12
```

Expected last line: `TRIP CAP (GSA ceiling, excl. lodging tax): $841.00`

## Bid line you can paste

> Travel ODC, Austin TX, 9–12 Mar 2026, 1 traveler: lodging 3 × $187 + M&IE (2 × $80 + 2 × $60) = **$841** GSA FY2026 ceiling, lodging tax extra, no POV.

If the same trip were in October (lodging $173): cap drops to $799.00. Seasonal miss is the usual bid leak.
