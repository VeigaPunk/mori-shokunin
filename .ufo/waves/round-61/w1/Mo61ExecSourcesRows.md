# Mo61ExecSourcesRows — SOURCES draft census

Validated the six drafted S565–S570 rows in a scratch mirror made from the lane corpus plus a placeholder `corpus/knowledge/psi-v73-recheck-r61.md` to satisfy the new rows' used-by target. The mirror and scratch were removed after recording results. No production files or VCS state were changed.

## Exact results

Mirror `/fast/scratch/hyaku/mori-r61/Mo61ExecSourcesRows/corpus/SOURCES.md` proposed rows: S565–S570 at lines 346–351 (the six rows supplied in `w1/Mo61ScribePsiProv.md:52-57`).

- `sources-census.sh validate --file <mirror>/corpus/SOURCES.md`: exit 1. Output consisted of 26 existing W04 duplicate-URL warnings (S035, S037, S073–S076, S147–S150, S166, S168, S201, S218, S220, S228, S349, S351, S470, S476, S486, S491, S492, S546, S552) and 29 existing E11 missing-used-by errors (S076, S134–S136, S145–S146, S148–S151, S153–S155, S191–S196, S199–S202, S544–S545, S547). No validation diagnostics named S565–S570. The minimal corpus-only mirror lacks pre-existing referenced files, explaining its E11 diagnostics; the new ledger target was present as an empty placeholder.
- Manual census output:

```text
rows=343
malformed=0
enum violations:
duplicate IDs:
literal_or_escaped_pipe_in_new_rows:
new_row_count=6
```

The pipe scan checked each new row's split-column count and escaped pipe marker; each row has 11 cells / NF=13 and no literal or escaped pipe inside cells. No duplicate ids or enum violations were printed.

Manual census commands followed `/home/vgpnk/Projects/shokunin/CORPUS.md:131-145`; validator invocation was `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /fast/scratch/hyaku/mori-r61/Mo61ExecSourcesRows/corpus/SOURCES.md`.

## Baseline reference

Before inserting the draft, the lane registry had 337 rows, malformed=0, no enum violations, and no duplicate ids. The six rows yield 343 total. Contract discrepancy: contract.md:138 states “rows S565–S070”; the seat's draft and assignment specify S565–S570. This report validates only S565–S570; it does not resolve that frozen-contract discrepancy.

## Limits

The validator's exit 1 reflects unrelated baseline E11 errors due to the corpus-only mirror, not a clean whole-lane validation. A full lane-root mirror would be needed to suppress these pre-existing missing-path reports. No scratch files remain. No tools installed.