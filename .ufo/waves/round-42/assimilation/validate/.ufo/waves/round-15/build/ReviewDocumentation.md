# ReviewDocumentation — read-only audit of SKILL / corpus index wording vs records

Scope: `SKILL.md`, `corpus/README.md`, and the count/receipt claims they make about
`tools/*` and `.ufo/waves/round-14/evidence/*`. No gates, builds, or tests were run.
No installs, upgrades, or pacman operations were performed (none were needed).
Current file hashes were read, not re-run.

## Current pins (observed now)

| file | sha256 (observed) | matches pinned claim |
|---|---|---|
| `tools/mori-census.sh` | `0e41cb83fce2e8c5c711171e1cde2e6fa2809dcfce630eccabe52bcbe41516d9` | yes, `SKILL.md:71` |
| `tools/mori-silence-cases.sh` | `34cd5770889ec6e7521b477aa9976cece7a64e07b83774c12ce2aea73161abfa` | not pinned in SKILL; matches r14 receipt |
| `tools/mori-round14-regressions.py` | `c39e5a7352666d09dc662293e1ea7be47ee3523b53247a5a6ae02e7dda19288d` | yes, `SKILL.md:77` |
| `.ufo/waves/round-14/frozen/mori-census.sh` | `39abda0a67028575d888d9157b8548dec0b4944c3d8c165691e88ab657fc3985` | yes, `SKILL.md:98` (`39abda0a…`) |

## Count claims checked against records

| claim (anchor) | record | verdict |
|---|---|---|
| census selftest `104/104` at 8d22d18, `SKILL.md:71` | `round-14/evidence/census-selftest.json`: `MORI_CENSUS_SELFTEST: PASS (104 cases, 104 passed, 0 failed)`, exit 0, `measured_commit 8d22d18…`, census sha `0e41cb83…` | consistent |
| oracle "28 cases", `SKILL.md:73` and `corpus/README.md` oracle notes | `tools/mori-silence-cases.sh:1145` `CASE_IDS=(` has 28 entries, 28 unique | consistent |
| r14 gate "20 checks" at 5601d12, `SKILL.md:75`, `:107-108` | `round-14/evidence/r14-selftest-accepted.json`: `SELFTEST: pass checks=20`, `measured_commit 5601d12…` | consistent |
| r13 gate "33 checks, 2 isolated cases" at 8d22d18, `SKILL.md:107-108` | `round-14/evidence/r13-selftest.json`: `SELFTEST: pass checks=33 cases=2`, commit 8d22d18 | consistent |
| "43 cases plus one frozen-red control, 44 assertions passing", `SKILL.md:109-110`, `corpus/README.md:303-304`, `journal-alarm-routing-r14.md:366-367` | `c1-measurement.json` `red_summary.claims=43`, `green_summary.claims=44` with `frozen_control=pass` | consistent |
| "six named acceptance arms fail 6 → 0", `corpus/README.md:303`, `journal-alarm-routing-r14.md:367` | `c1-measurement.json` `named_acceptance_arms` lists exactly 6 ids; `counting_command` is the jq count over red-before and green-after evidence | structurally consistent; the 6→0 integer values were not re-counted here (red/green evidence.json not opened) |
| "56 → 66 cases" r10 drift pin, `SKILL.md:126` | `corpus/knowledge/drift-pin-r10.md` and `corpus/README.md` both state `PASS (66 cases …)` | consistent with historical notes |
| "live 12/12 cells all zero", `corpus/README.md:306`, `journal-alarm-routing-r14.md:375` | `live-measurement.json` `measured_commit 5601d12`, one boot (`430d3038…`) | consistent, but it is one boot's observation |
| "twelve in the r13 bytes" journal class queries, `SKILL.md:81` | frozen r13 census has 3 `journal_query "` call sites (`.ufo/waves/round-14/frozen/mori-census.sh`), the 12 expansion was not measured in this audit; current `tools/mori-census.sh` has 4 call sites | [INFERENCE] the "r13 bytes" qualifier is correct; no current-byte count is stated anywhere; do not cite the current count without measuring |

## Index completeness (corpus/README.md)

- `corpus/knowledge/`: 22 notes on disk, all 22 have a row in the Coverage map. Consistent.
- `corpus/lessons/` dated `2026-10-15-*`: all 10 indexed. Consistent.
- `corpus/lessons/` round files NOT indexed (no row in Coverage map):
  - `round-12-verifier-spotcheck.md`
  - `round-13.md`
  - `round-13-verifier-spotcheck.md`
  - `round-14.md`
  - `round-14-verifier-spotcheck.md`
  Only `lessons/round-12.md` (`corpus/README.md:36`) and a prose mention of `round-13-verifier-spotcheck.md` (`corpus/README.md:293`) appear.

## Findings and necessary fixes

1. **Missing index rows (coverage gap).** `corpus/README.md` Coverage map (near line 36-39) needs rows for the five unindexed `corpus/lessons/round-*` files listed above, or an explicit statement that verifier spot-checks are out of the index. Severity: medium (index completeness).

2. **Undisclosed red selftest receipt for r14.** `.ufo/waves/round-14/evidence/r14-selftest.json` records `measured_commit 8d22d18…`, `exit 1`, stdout `SELFTEST: fail real-gate-red-oom-id | real-gate-red-unit-id | real-gate-red-evidence`. `SKILL.md:75` and `:107-110` cite only the accepted 5601d12 run (`checks=20`). The corpus never says the 8d22d18 run failed. Fix: add one sentence to `SKILL.md` near line 75 (and `corpus/README.md` near line 303) naming the 8d22d18 red run and stating it is superseded by the 5601d12 accepted receipt. Severity: medium (records not reconciled with wording).

3. **Unmeasured "twelve" qualifier.** `SKILL.md:81` says "twelve in the r13 bytes". The wording is historically scoped, which is correct, but the frozen census has 3 `journal_query` call sites and the current census has 4. If the current census is cited elsewhere for a query count, a current-byte count must be measured first. Severity: low.

4. **Mixed receipt SHAs for the r14 harness.** `census-selftest.json` (8d22d18) records `tools/mori-round14-regressions.py` at `7af94b4c…`, while `r14-selftest-accepted.json` (5601d12) and `SKILL.md:77` use `c39e5a73…`. These are different measured commits, not a contradiction, but `SKILL.md:77` should say which commit its SHA belongs to. Severity: low.

5. **Single-boot live parity wording.** `corpus/README.md:306` ("live 12/12 cells were all zero") is one boot (`430d3038…`) at 5601d12. Suggest adding "(one boot, 2026-10-20)" to keep it from reading as a durable claim. Severity: low.

## Verified consistent (no fix)

- `SKILL.md:71` (104/104, census sha `0e41cb83…`) — receipt and current file agree.
- `SKILL.md:73` (oracle 28 cases) — `CASE_IDS` has 28 unique ids.
- `SKILL.md:75`, `:77` (r14 20 checks, harness `c39e5a73…`) — accepted receipt and current file agree.
- `SKILL.md:107-110` (r13 33 checks / 2 cases; r14 43 + control = 44) — receipts agree.
- `SKILL.md:98` frozen pin `39abda0a…` — file agrees.
- All 22 knowledge notes indexed; all 10 dated lessons indexed.

## Residual risk / verification gaps

- The 6→0 integer counts in `c1-measurement.json` were not re-derived from `red-before-accepted/evidence.json` and `green-after-accepted/evidence.json`; only the structure and the jq command were read.
- `SKILL.md:81` "twelve" was not re-derived for either frozen or current bytes.
- No gate was run, per assignment.

## Tool installs/updates

None performed.
