# Recheck043 — C1 freshness recheck of S043

Seat `MoriR32A2.Recheck043`. Round 32, wave 1. Population row S043 only.
Population row read from `.ufo/waves/round-32/c1-population.json` (id S043); base row
`corpus/SOURCES.md:49`. Nothing in the lane was written except this report; copy and receipts live under
`/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck043/`.

## 1. Fetch

- url (population, unchanged): `https://docs.z.ai/api-reference/api-code`
- redirect: none. `curl -w url_effective` returned the same URL
  (`url_effective=https://docs.z.ai/api-reference/api-code`), so the population url cell stays as written.
- accessed: `2026-10-23T01:31:27Z` (`date -u` run in the same command, first and only try)
- fetch: `curl -sSL --fail -m 60` → `http_code=200 size=153701`, exit 0, try 1/3
- bytes saved unchanged: `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck043/S043.src` (153701 bytes)
- sha256: `4a6ac09770cabd93d0e16a65bfc23669e85b019c23e28ddb74ea33e88d82feb4`
- normalised text used for quoting: `S043.norm.txt` from
  `python3 .ufo/waves/round-32/seat-check.py text S043.src` (44833 bytes / 1746 words)
- fetch receipts: `S043.try1.err` (empty)

## 2. Ready-to-paste row

```
| S043 | https://docs.z.ai/api-reference/api-code | 2026-10-23T01:31:27Z | 4a6ac09770cabd93d0e16a65bfc23669e85b019c23e28ddb74ea33e88d82feb4 | "1302 429 Rate limit reached for requests"; "1113 429 Insufficient balance or no resource package. Please recharge."; "1308 429 Usage limit reached" | current |
```

## 3. Quotes vs the teaches cell

Teaches cell (population): "Code 1302 means request rate limit; 1113 and 1308 usage/balance causes also use
HTTP 429, so status alone cannot distinguish rate limit from quota."

Rendered error table in the live copy (offsets into `S043.norm.txt`):

- ~1100–4300 holds the table `Error Codes`, headed "HTTP Status Code Error messege", introduced by
  "the outer layer is the HTTP status code, and the inner layer is the business error code defined by Z.AI in
  the response body" (~offset 800–1050).

| # | quote | teaches fact it bears on | why it holds |
|---|---|---|---|
| 1 | `1302 429 Rate limit reached for requests` | "Code 1302 means request rate limit" | The row states code 1302, status 429, message "Rate limit reached for requests" — the exact mapping the cell asserts. |
| 2 | `1113 429 Insufficient balance or no resource package. Please recharge.` | "1113 … usage/balance causes also use HTTP 429" | Row 1113 is bound to 429 with a balance/resource-package message, i.e. a quota-class cause under the same status as the rate-limit row. |
| 3 | `1308 429 Usage limit reached` | "1308 usage/balance causes also use HTTP 429" | Row 1308 is bound to 429; the live full text continues "for {number} {unit} . Your limit will reset at {next_flush_time}", a usage-limit cause. Quote stops at "reached" (whole word) rather than cutting mid-placeholder. |

Contrast that carries the "status alone cannot distinguish" half: the rendered table binds **16 distinct business
codes to HTTP 429** in the same segment — `1113, 1302, 1305, 1308, 1309, 1310, 1311, 1313, 1314, 1315, 1316, 1317,
1318, 1319, 1320, 1321` (`re.findall(r'(\d{4}) 429 ', seg)` over offsets 1100–4300 → `len=16`). Two of those
(1305 "service may be temporarily overloaded", 1311 "subscription plan does not yet include access") are neither
rate limit nor quota, which strengthens rather than contradicts the cell.

Verdict `current`: all three asserted code→status→cause mappings are present verbatim in the live page, so
`corpus/knowledge/seat-terminal-status-r17.md` needs no `Round32` correction.

## 4. Self-check output

Command:

```
timeout 300 python3 .ufo/waves/round-32/seat-check.py row S043 \
  /fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck043/S043.src \
  '"1302 429 Rate limit reached for requests"; "1113 429 Insufficient balance or no resource package. Please recharge."; "1308 429 Usage limit reached"'
```

Output:

```
sha256=4a6ac09770cabd93d0e16a65bfc23669e85b019c23e28ddb74ea33e88d82feb4
quotes=3 words=[7, 10, 5] in_copy=[True, True, True]
shared_tokens=['balance', 'limit', 'rate', 'usage'] topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
exit=0
```

`live_quotes_ok=True` means the counter's own fresh `curl` of the population url still contained all three quotes
after normalisation — i.e. the copy and the live page agree this round.

## 5. Drift

None. Verdict `current`, so no `Round32` correction paragraph is drafted and no `corpus/knowledge/` file is touched.

Observations that are not drift (recorded for the integrator, not claim-relevant):

- The page is a Mintlify docs page: the rendered table appears once in the HTML body and a second time inside the
  serialised JSX payload (`_jsxs(_components.tr … children:` at ~offset 17300+). All quotes were taken from the
  rendered occurrence, never the payload.
- Table header misspelling "Error messege" is present in the live page — cosmetic, predates the row.
- The anchor's "api-code.md lines 16/31/33" refers to a markdown snapshot of this page, not to the live HTML; only
  the code/status/cause content was checked live, and it matches.

## Tooling

No installs, no updates, no package transactions. Tooling used as shipped: `curl`, `python3`, `sha256sum`,
`date`. Lane git untouched (read-only `grep`/`read` of `corpus/SOURCES.md` and
`corpus/knowledge/seat-terminal-status-r17.md`). No subagents, no background jobs left running.
