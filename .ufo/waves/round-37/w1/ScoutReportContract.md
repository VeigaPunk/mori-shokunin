# ScoutReportContract — round-37 report vs prompt §4

Axes: section presence (order), evidence-pointer resolution, marker-rule class.
Attacked item: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-37/mori.md` against `/home/vgpnk/Projects/shokunin/.ufo/prompts/mori-round-37.md` §4 (lines 99–129). Checklist source: `mori-shokunin/SHONEN.md:5-8`.
Tool installs: none.

## Section-present table

| # | Required section | Report | Present | Evidence pointers (resolved) |
|---|---|---|---|---|
| 1 | Work performed — claims (1–3) and axes first, then one bullet per item with a pointer | `mori.md:7-57` | yes | C1 calibration and C2 freshness named at `:11-18` before the bullets. Pointers resolve: `e57c58b5` (`git rev-parse` → `e57c58b57c025364e79d130fbdf764d2674d83d6`); `evidence/c1-after.txt` ends `C1=met` / `EXIT=0` / seed `13985344346805549517`; `c1-before-memo.txt` and `c1-before-summary.txt` end `C2=met` `EXIT=0`; `c2-after.txt` ends `C2=met` `EXIT=0`; `c2-before.txt` ends `C2=unmet` `EXIT=1`; `tools/mori-source-drift.py:398-415` is the `huge_cap` / `redirect_private_refused` arms; `corpus/knowledge/source-drift-r36.md:24-33` is the nine-row drifted prose; `SCORECARD.md:2035` Round 37 declaration; `corpus/README.md:45-46` and `:585` coverage rows; `corpus/QUALITY.md:853` and `:862` are criteria 106 and 107; `corpus/lessons/round-37.md:3` Gate |
| 2 | Landed changes — each change tied to a LOG.md entry and a commit | `mori.md:59-71` | yes | Six hashes all `git rev-parse` as commits: `e57c58b5`, `bcf65505` → `bcf65505cf016fa50cd19e52f6dc287a3ca206a5`, `5dff52a1` → `5dff52a1ba4e76b8a30f2557a09239b9568b5680`, `52d636d5` → `52d636d5015cd54f03ce680aa43d5ceb3f396710`, `4bec58eb` → `4bec58ebb873e1791dee1704822255275e98e77e`, `c31076ed` → `c31076ed85b3aadf2454637747343e0ab97eb58f` (`round-37: LOG lesson range M1-M5…`). Tie target `LOG.md:2139` exists |
| 3 | Before → after measurements — one per claim, counting command and measured commit | `mori.md:73-82` | yes | C1 and C2 rows name `count-c1.py` / `count-c2.py`, commits `e57c58b5` and re-score `bcf65505`. Receipt tails match the table: `c1-after-tip.txt` seed `5097152322487907681` `C1=met` `EXIT=0`; `c2-after-tip.txt` `C2=met` `EXIT=0` |
| 4 | Sources & frontier — before→after, counting command, rows by tier, old→new, frontier rows | `mori.md:84-100` | yes | Census command named; both receipts `EXIT=0` (`census-start.txt:17`, `census-end.txt:17`). Row command reproduced: `git show 842a320:corpus/SOURCES.md \| grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → `220`; same at `5dff52a1` → `225`. Tip rows S221–S225: tiers A, B, A, A, A (spec/docs/docs/docs/spec). old→new stated none; frontier advance stated none |
| 5 | Trend verdicts — expansion, quality, discernment; allowed words; evidence; no scalar | `mori.md:102-113` | yes | All three are `improved` (allowed). Evidence is the 220→225 row move, QUALITY 106/107, and lesson M1/M2. No numeric verdict |
| 6 | SHONEN — one line per `SHONEN.md` box | `mori.md:115-127` | yes | Four lines, same four boxes as `SHONEN.md:5-8`. No `[x]` (no named non-author verifier). Each `[~]` names a file that exists: knowledge entry + QUALITY 106/107; `evidence/c1-after*.txt` / `c2-after*.txt` and `LOG.md:2139`; `contract.md` + `count-c1.py` / `count-c2.py`; `PROVINCE.md` |

Order is the §4 order. Later headings (`mori.md:129` Round shape, `:151` Inherited state) are extra, not substitutes.

No placeholder hits (`TODO`, `PENDING`, `[PARENT`, `TBD`, `FIXME`) in the report.

## Marker rule

§4 (`mori-round-37.md:121-125`): a contentless report (placeholder, missing a required section other than Sources & frontier and Trend verdicts, or no evidence pointers) is a relaunch failure. Skipping only those two sections would be `ok` plus one conformance defect; neither is a marker predicate.

Observed: not placeholder; Work performed, Landed changes, Before → after measurements, and SHONEN are present and carry pointers; Sources & frontier and Trend verdicts are also present. Marker class: not a relaunch failure. No skip-defect.

## Notes that do not remove a section

- `census-start.txt` and `census-end.txt` are byte-identical (`cmp` exit 0). Both are the W04 list plus `EXIT=0`. They do not store `220` vs `225`; that pair is the separate `grep -cE` command, which matches.
- `LOG.md:2139-2167` names `e57c58b5` and `52d636d5` only. The other four landed hashes are tied in the report table to that same entry, not repeated inside the log body.
- SHONEN box 1 (`mori.md:117-119`) says the SKILL box was not touched and still uses `[~]` rather than `[ ]`. The `[~]` pointers resolve, but they point at the knowledge entry and QUALITY 106/107, not at a SKILL.md edit.
- SHONEN box 4 (`mori.md:126-127`) names `PROVINCE.md` (file exists) and says connector sibling scans are "not yet returned". `w1/` at check time has 13 seat files and no `Conn*` report, so that half of the `[~]` is still unresolved. The line is present; it is not `[x]`.

VERDICT: PASS
