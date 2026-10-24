# ExecGateRegistry — round-37 capabilities vs the lane gate registry (SKILL.md)

**What this attacks:** the completeness and field conformance of mori's registry home — `SKILL.md`, which
PROTOCOL.md:398-402 makes the only place a child lane registers a gate/probe, and PROTOCOL.md:418-421 the
condition on which closure grades one conformant. Scope: read-only inspection of the lane at
`e57c58b57c025364e79d130fbdf764d2674d83d6` (scored tip; `SKILL.md` byte-identical at current HEAD
`1ae1d6d`, measured below) plus one read-only selftest run. `SKILL.md` was **not edited**; this is a report.

Axes named (godspeed): (1) *registry completeness* — does every capability the round declares have a row at
the registry home? (2) *field conformance* — eight PROTOCOL columns, with the kind vocabulary `gate|probe`
and the self-test spelling recorded; (3) *evidence binding* — does each cell name a path/command that exists
in the tree the row would land in?

## 1. The registry home today

The Round-36 table is `SKILL.md:872-876`: header `| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |`
(8 columns, 9 pipe-delimited fields — measured) and three rows: `source drift (r36)` (:874),
`SOURCES append-only (r36)` (:875), `index clean (r36)` (:876). It is the last table in the file (`SKILL.md`
is 876 lines; the `index clean` row is the final line).

```
$ grep -n "round-37\|Round37\|R37\|r37" SKILL.md
NONE                     # shell fallback echo: zero matches
$ git show e57c58b57c025364e79d130fbdf764d2674d83d6:SKILL.md | grep -n "count-c1\|round-37" | cut -c1-90
802:S175–S177). Tool for the counted check: `python3 .ufo/waves/round-32/count-c1.py <rev>
                         # the only `count-c1` hit is the round-32 counter, in prose; zero round-37 text
$ git diff --stat e57c58b57c025364e79d130fbdf764d2674d83d6 HEAD -- SKILL.md
         # empty: SKILL.md is unchanged from the scored tip to HEAD 1ae1d6d
```

Round 37 added `SKILL.md` to no commit: the round's diff (`git diff --stat 842a320..e57c58b`) touches 25
paths and `SKILL.md` is not one of them. Both round-37 capabilities therefore have **no** registry row.

## 2. Missing row A — the hardened source-drift probe (C2 capability)

SCORECARD.md:2059 registers `round-37 C2 | source-drift re-fetch probe | … first working 37`; the round
changed `tools/mori-source-drift.py` (diff `842a320..e57c58b`) by adding the two named selftest arms
`huge_cap` and `redirect_private_refused`. No row at `SKILL.md:872-876` or anywhere else in the file names
those arms, the cap constant, the redirect policy, or the mutation that must kill each.

| field (PROTOCOL.md:401-402) | required cell — grounded value |
|---|---|
| name | `source drift (r37)` — must differ from the r36 name at `SKILL.md:874`; same tool, hardened self-test |
| kind | `probe` (byte-behaviour probe; sample, not a subject verdict — same class as the r36 row) |
| entry | `python3 tools/mori-source-drift.py --root <repo>` (usage line: `tools/mori-source-drift.py:460-462`; `--root`/`--selftest` dispatch `:453`. All measured §7) |
| verdict map | 0 `drifted=0` (rows may be `unavailable` or `no-copy`) · 1 `drifted>0` · 2 could-not-evaluate (`MORI_SOURCE_DRIFT_SETUP`, SOURCES.md missing/unreadable `:217-221`, non-directory root `:455-458`, usage `:460-462`) · **new in r37:** over-cap body and post-redirect non-public destination grade `unavailable`, never `drifted` |
| self-test | `python3 tools/mori-source-drift.py --selftest` (spelling `--selftest`), exit 0, `MORI_SOURCE_DRIFT_SELFTEST: PASS (6 cases)`; arms `exit_code, row_states, summary, huge_cap, redirect_private_refused, missing_sources_exit2` (measured, §6) |
| pinned values | `FETCH_MAX_BYTES = 4 * 1024 * 1024` (`tools/mori-source-drift.py:54`; read as `+1` at `:163-166`); `if not _public_redirect_target(final):` (`:158`, policy `:113-136`); mutants that must kill their own arm: `FETCH_MAX_BYTES = 1 << 40` → `huge_cap FAIL`, `if False:  # round-37 mutation: policy removed` → `redirect_private_refused FAIL` (`.ufo/waves/round-37/count-c2.py` constants); corpus binding `corpus/knowledge/source-drift-hardening-r37.md` (S221–S225, commit `8ff9bba`); receipts `.ufo/waves/round-37/evidence/c2-after.txt` (`C2=met`) and `drift-live-r37.txt`; freeze pin `.ufo/waves/round-37/evidence/freeze-r37.txt` (tool sha256 `453c5d8e260301df7a99daf62b4c16ea08e4a0b4f9e4f53821cdbce447011552`, measured equal to current bytes) |
| write scope | none — read-only over `corpus/SOURCES.md` and the copies, off-tree network reads, selftest temp dir removed |
| owner | mori |

## 3. Missing row B — the C1 counter's challenge arm (C1 capability)

SCORECARD.md:2058 registers `round-37 C1 | real-arm challenge counter | … first working 37` and points at
`.ufo/waves/round-37/count-c1.py`. No `SKILL.md` row names it; `count-c1` appears in `SKILL.md` only at
`:802` as the *round-32* counter (prose, not a row).

| field (PROTOCOL.md:401-402) | required cell — grounded value |
|---|---|
| name | `append-only measurement discrimination (r37, C1 counter)` — or `real-arm challenge counter (r37)` to match SCORECARD:2058 |
| kind | **`probe`** is the only honest value today. PROTOCOL.md:377-379 defines a *gate* as comparing against expected values **persisted in its own repo**, and PROTOCOL.md:385-389 requires a self-invocation mode over isolated fixtures with a stable expected finding-id. `count-c1.py` has neither: its hidden truth is computed at run time from its own op log (`REAL_REV`/`REAL_BASE` are the only persisted expectations, `:59-60`), and `grep -n "selftest\|self-test" .ufo/waves/round-37/count-c1.py` returns nothing. Declaring `gate` now would pin a clause the bytes do not meet |
| entry | `python3 .ufo/waves/round-37/count-c1.py <rev> [--repo DIR] [--tool FILE] [--negatives DIR] [--seed N]` (argparse `:843-847`); default tool path is `tools/mori-sources-appendonly.py` at `<rev>` (`TOOL_REL` `:54`) |
| verdict map | 0 `C1=met` · 1 `C1=unmet` (includes `tool_timeout`, scored unmet-by-timeout, never a list mismatch `:694,737,776`) · 2 counter setup error (`:960`) |
| self-test | **`none`** — no `--selftest`/`--self-test` mode exists (grep above). The able-to-fail evidence is the three negatives that must each be rejected: `.ufo/waves/round-37/fixtures/memo-n1.py`, `const.py`, `summary-only.py` (`NEGATIVES_DIR` `:57`, `NEG_BLIND = 4` `:62`). Recording `none` is required; nothing may be invented |
| pinned values | PREDICATE text `:42-52`; `REAL_REV = "6bd57097"`, `REAL_BASE = "f10a320d"` (`:59-60`); challenge clothing `LANE_TITLE` (`:288`); fixture blob pins in `evidence/freeze-r37.txt` (`memo-n1` `19324701…`, `const` `2f3993a0…`, `summary-only` `2d62f742…`); counter freeze pin sha256 `86699627c7627cc3eea3ba9ea952079d081db390f9ba2be1e1d4d685dd98cdae` (measured equal to current bytes); frozen run `.ufo/waves/round-37/evidence/c1-after.txt` (`blind 24/24`, `real arm: pass`, `challenge arm … pass`, three negatives rejected, `C1=met`, seed `13985344346805549517`, `EXIT=0`) and controls `c1-before-memo.txt`, `c1-before-summary.txt` |
| write scope | scratch only, and it must say so because it writes **inside the lane tree**: `tempfile.mkdtemp` children under `<lane>/.ufo/waves/round-37/scratch/` (challenge arm, `:762-763`), under `/fast/scratch/hyaku/mori-r37/` (`SCRATCH_ROOT` `:55`, fallback `:818-828`), and a tool extract under `TMPDIR` (`:872`); never a tracked lane file |
| owner | mori |

## 4. Field-level gaps in the existing r36 row (`SKILL.md:874`)

The `source drift (r36)` row exists and stays true, but two of its cells now under-describe the same tool's
bytes. If the lane appends a Round-37 row (§2) these are merely stale; if it instead amends the r36 row, these
are the exact cells to correct (no prior round has edited a registry row in place — rounds 24, 26, 32 add
rows or append corrections):

- column 5 (self-test), current text `(offline 127.0.0.1 fixture)` — names no case count and neither
  `huge_cap` nor `redirect_private_refused`; the tool now prints `PASS (6 cases)` (§6).
- column 6 (pinned values), current text `newest copy … per row; live URL bodies` — omits
  `FETCH_MAX_BYTES` (`:54`), the `_public_redirect_target` anchor (`:158`), the two mutants, the knowledge
  entry, and both receipts; PROTOCOL.md:390-397 asks a gate's pinned values to be the persisted expectations.
- column 4 (verdict map) is conformant; only the r37 "over-cap / refused redirect → `unavailable`" clause is
  missing, and that is behaviour the r37 arms newly exercise.

## 5. Explicitly not missing (checked, so the set above is closed)

- `r17 jj regressions` (`SKILL.md:175`): round 37 changed the *assertion* inside
  `tools/mori-round17-jj-regressions.py` (`jj_config_redirected` now tests the redirect property, plus the
  jj-workspace file evidence when a workspace exists; diff `842a320..e57c58b`, receipt
  `.ufo/waves/round-37/evidence/r17-jj-selftest-r37.txt`, `EXIT=0`). The row's eight cells stay true: same
  entry, same 0/1/2 map, same `--selftest --scratch DIR` spelling, same pinned "in-script fixed
  case/assertion universe", same write scope. No row missing.
- `.ufo/waves/round-37/count-c2.py`: a committed verdict script (0/1/2) with no self-test mode, and it holds
  no row — but it is not one of the two named capabilities (SCORECARD:2059 names the *probe*, not the
  counter), and no wave counter has ever held a `SKILL.md` row (round-32 `count-c1.py` is prose at
  `SKILL.md:802` only). Recording it as a third row is the lane's call; if taken, it needs the same honest
  `kind`/self-test treatment as §3.
- `blind-writer gate (r31)` (`SKILL.md:794`) already carries a frozen arm under `.ufo/waves/round-32/frozen/`;
  precedent exists for a row whose evidence lives in a wave directory, so §2/§3 rows do not need copies of
  the counters under `tools/`.

## 6. Measurement that both round-37 gates cannot see this gap

Neither counter reads `SKILL.md`, so `C1=met` and `C2=met` are both true with zero registry rows:

```
$ grep -n "SKILL" .ufo/waves/round-37/count-c1.py .ufo/waves/round-37/count-c2.py
NO SKILL.md REFERENCE IN EITHER COUNTER      # shell fallback echo: zero matches in both files
$ grep -n '^    check("' .ufo/waves/round-37/count-c2.py
152:    check("tool_present", …)
189:    check("knowledge", knowledge is not None
198:    check("capability", bool(cap_rows) and TOOL_REL in cap_rows[-1],
203:    check("readme", "knowledge/source-drift-r36.md" in readme
209:    check("live", live is not None and LIVE_SENTENCE in live,
```

`count-c2.py` binds knowledge entry, SCORECARD capability row, README coverage-map rows and the live receipt
(plus `selftest` `:161`, `cap_kill` `:170`, `redirect_kill` `:177`) — the lane registry home is not among its
surfaces. This is the structural half of the finding:
the round's own measurement cannot detect a missing registry row, so the row is only landed if a human seat
writes it.

## 7. Exact measurements (command → observed output)

```
$ sed -n '872,876p' SKILL.md | cut -c1-120
| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| source drift (r36) | probe | `python3 tools/mori-source-drift.py --root <repo>` | 0 `drifted=0` (rows may be `unavaila
| SOURCES append-only (r36) | gate | `python3 tools/mori-sources-appendonly.py <rev> [--repo DIR] [--round-base REV] [--
| index clean (r36) | gate | `bash tools/mori-index-clean.sh <repo>` | 0 `staged=0 intent_to_add=0` · 1 staged or inten
                       # ^ `cut -c1-120`: every row is one long pipe line; nothing else is elided
$ awk 'NR>=872 && NR<=876' SKILL.md | awk -F'|' '{print NR": fields="NF-1}'
1: fields=9 … 5: fields=9          # 8 columns, 9 delimited fields, header included
$ grep -n "round-37\|Round37\|R37\|r37" SKILL.md
NONE
$ python3 -I -B tools/mori-source-drift.py --selftest ; echo rc=$?
selftest exit_code            PASS
selftest row_states           PASS
selftest summary              PASS
selftest huge_cap             PASS
selftest redirect_private_refused PASS
selftest missing_sources_exit2 PASS
MORI_SOURCE_DRIFT_SELFTEST: PASS (6 cases)
rc=0
$ grep -n "selftest\|self-test" .ufo/waves/round-37/count-c1.py
NO SELFTEST MODE                  # shell fallback echo: zero matches
$ sha256sum .ufo/waves/round-37/count-c1.py .ufo/waves/round-37/count-c2.py tools/mori-source-drift.py
86699627…98cdae  .ufo/waves/round-37/count-c1.py        # = freeze-r37.txt
71c72929…a7c1    .ufo/waves/round-37/count-c2.py        # = freeze-r37.txt
453c5d8e…11552   tools/mori-source-drift.py             # = freeze-r37.txt
$ git log --oneline -1 -- .ufo/waves/round-37/evidence/c1-after.txt
5631efa round-37: wave-1 corrections — …        # same commit carries c2-after.txt
```

The C1/C2 receipts (`evidence/c1-after.txt`, `c2-after.txt`) are **not** in `e57c58b` — they landed at
`5631efa`. A row written now may cite them; a row written against the scored tip could not have.

## 8. Risks, blockers, installs

- Risk: landing the r36-row amendment instead of a new r37 row would leave no row whose self-test cell names
  the mutation-killed arms, which is precisely what the C2 capability claims.
- Risk: writing `kind=gate` for `count-c1.py` would assert a self-test clause the bytes do not meet
  (PROTOCOL.md:385-389); `kind=probe` with `self-test: none` is the conformant record.
- Blocker: none. Every field value above is read from committed bytes at the scored tip or from a read-only
  run; nothing was edited, no lane file was touched, no counter invoked.
- Installs/upgrades: none.

Artifact: `.ufo/waves/round-37/w1/ExecGateRegistry.md` (only file written).

VERDICT: PASS — every missing registry row is named precisely: **A** `source drift (r37)` (hardened probe:
`huge_cap` + `redirect_private_refused`, cap and redirect-policy pins) and **B** the C1 counter's challenge
arm `.ufo/waves/round-37/count-c1.py` (`kind=probe`, `self-test: none`), with the two stale cells at
`SKILL.md:874` col 5/col 6 recorded. The absence of those rows is the lane's registry-conformance defect
(PROTOCOL.md:398-402, :418-421) for L1 to land; it is not a defect in this measurement.
