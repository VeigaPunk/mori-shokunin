# Mo59Scribe49 — round-59 SCORECARD section skeleton (draft only)

Seat: `Mo59Scribe49` (scribe, leaf). Assignment: draft the SCORECARD round-59 section
skeleton — claim-table rows for C1/C2, the frozen counting commands, and receipt names —
read-only, no repo edits, return the draft in this report file only.

Nothing in `corpus/`, `SCORECARD.md`, `LOG.md`, `MANIFEST.json` or lane VCS was written.
All paths below are absolute-from-lane-root
(`/home/vgpnk/Projects/shokunin/mori-shokunin/…`) unless stated.

Disk guard before work: `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`
→ `/fast/scratch/hyaku 27% 592.6G free`, `/tmp 5%`, `/var/tmp 36%`. Green.

## 1. Inputs read

| Input | Revision / path | Observation |
|---|---|---|
| Frozen contract | `.ufo/waves/round-59/contract.md`, sha256 `427fca0b…107e` | C1/C2 claims, targets, kill rules, controls, round shape |
| Frozen C1 counter | `.ufo/waves/round-59/count-c1.py`, sha256 `2be6fda8…9dfd` | 277 lines; constants at 34–46, `measure()` 91, `selftest()` 214, output line 262 |
| Frozen C2 counter | `.ufo/waves/round-59/count-c2.py`, sha256 `2df3ae84…77be` | 464 lines; constants 45–53, `ARTIFACTS` 55–68, `eval_entry()` 100, `measure()` 193, `selftest()` 365, output line 452 |
| Entering revision | `2b9f03975bfb6e508f35074ac8181ec8bf54e805` | round-58 verifier spot-check commit |
| Amended freeze | `60b3a76ad0524c8978cc51922940be1c8c388915` | freeze `ccfd554e` + pre-data counter/tool amendment |
| Dispatch | `8ff344ff18924c1ea63d46c3b3969f9fea05bc51` = lane HEAD | validated w1 dispatch payload (64 seats, v2) |
| MANIFEST binding | fleet `2807c6ab8a9b04dcf256682bcd722c695fdd6e14:MANIFEST.json` | `rounds[]` length 864; `rounds[832]` = round 56 closure, `capabilities_added[0]` starts `dual-shape seat-output vote binding`, `[1]` starts `strict per-event driver-liveness probe` — both equal the counter's `BOUND` prefixes (count-c1.py:39-44) |
| Active register | `SCORECARD.md:1951` `## Capabilities` (self-declares "current capabilities register"); rows `SCORECARD.md:1989-1990` | keys `rounds[832].capabilities_added[0]` / `[1]`, matching `REQUIRE` (count-c1.py:38); the superseded stub header sits at `SCORECARD.md:596` |
| Wave state | `.ufo/waves/round-59/w1/` | only `swarm-registry.json` (8055 B); **no `w1-results.json` yet — wave unsettled at scribe time** |

Frozen bytes verified unchanged at HEAD: counter shas above equal their `git show
60b3a76a:` shas; `tools/mori-register-check.py` = `38b733d896f880f5b7ecb464848b80798810ab052fcf0a8afb320918151472b8`
(= C1 `PIN`, count-c1.py:46); `tools/mori-settlement-scan.py` =
`4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9` (= C2 `PIN`, count-c2.py:53).

## 2. Independent re-run of the frozen instruments

Scratch: `/fast/scratch/hyaku/mori-r59/Mo59Scribe49` (`TMPDIR` set there, `--scratch` passed
explicitly). Receipt copy (inline, small):

```
# Mo59Scribe49 independent re-run, 2026-10-28T05:55:03Z
## selftest C1
C1_SELFTEST pass=6 fail=0
rc=0
## selftest C2
C2_SELFTEST pass=9 fail=0
rc=0
## C1 at amended freeze 60b3a76a
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=60b3a76ad0524c8978cc51922940be1c8c388915
rc=0
## C2 at amended freeze 60b3a76a
C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=bad rows=bad pins=bad tree=bad claims=0 files=0 rev=60b3a76ad0524c8978cc51922940be1c8c388915 failed=copy_absent:corpus/evidence/sources-r59/w1-results-r54.json,copy_absent:corpus/evidence/sources-r59/w1-results-r55.json,copy_absent:corpus/evidence/sources-r59/w1-results-r56.json,copy_absent:corpus/evidence/sources-r59/w1-results-r57.json,copy_absent:corpus/evidence/sources-r59/w1-results-r58.json,copy_absent:corpus/evidence/sources-r59/w1-settlement-r58.json,entry_absent,tree
rc=1
## C1 do-nothing at entering 2b9f0397
C1=unmet selftest=bad fixtures=bad real=bad pointers=bad rev=2b9f03975bfb6e508f35074ac8181ec8bf54e805 failed=tool_absent,selftest,fixtures_absent,real,pointers
rc=1
## C2 do-nothing at entering 2b9f0397
C2=unmet selftest=bad scan=bad drift=bad trees=bad entry=bad rows=bad pins=bad tree=bad claims=0 files=0 rev=2b9f03975bfb6e508f35074ac8181ec8bf54e805 failed=copy_absent:corpus/evidence/sources-r59/w1-results-r54.json,copy_absent:corpus/evidence/sources-r59/w1-results-r55.json,copy_absent:corpus/evidence/sources-r59/w1-results-r56.json,copy_absent:corpus/evidence/sources-r59/w1-results-r57.json,copy_absent:corpus/evidence/sources-r59/w1-results-r58.json,copy_absent:corpus/evidence/sources-r59/w1-settlement-r58.json,drift,entry_absent,scan,selftest,tool_absent,tree,trees,trees_absent
rc=1
```

All five lines reproduce the committed receipts byte-for-byte:
`evidence/c1-at-freeze.txt`, `evidence/c2-at-freeze.txt`, `evidence/control-c1-do-nothing.txt`,
`evidence/control-c2-do-nothing.txt`, `evidence/selftests.txt` — independently re-derived, no
divergence. (C2 freeze receipt matches even though C2's data has not landed: `entry=bad
rows=bad pins=bad tree=bad claims=0 files=0`.)

Presence checks (`git cat-file -e`, read-only):

| Path | at `2b9f0397` | at `60b3a76a` |
|---|---|---|
| `tools/mori-register-check.py` | ABSENT | PRESENT |
| `tools/mori-settlement-scan.py` | ABSENT | PRESENT |
| `corpus/knowledge/wave-settlement-artifacts-r59.md` | ABSENT | ABSENT (data not landed) |
| `.ufo/waves/round-59/count-c1.py` | ABSENT | PRESENT |
| `.ufo/waves/round-59/count-c2.py` | ABSENT | PRESENT |
| `.ufo/waves/round-59/fixtures-c1/` dirs | 0 | 13 |
| `.ufo/waves/round-59/trees-c2/` dirs | 0 | 12 |
| `corpus/evidence/sources-r59/` files | 0 | 0 |

Frozen fixture/tree reject prefixes actually committed (for the claim-row wording):
C1 `f01-stub-only binding`, `f02-two-declared binding`, `f03-dup-key keys`, `f04-missing-key keys`,
`f05-pointer-missing pointers`, `f06-pointer-absolute pointers`, `f07-pointer-relative-parent pointers`,
`f08-manifest-name-altered manifest:name`, `f09-manifest-substring-only manifest:name`,
`f10-manifest-foreign-lane manifest:lane`, `f11-manifest-wrong-index manifest`,
`f12-lane-round-mismatch manifest:lane_round`, `f13-empty-pointer pointers`.
C2 `t01-no-frontmatter frontmatter`, `t02-dup-k distinct`, `t03-quote-wrong-line span`,
`t04-stale-pin pin`, `t05-few-claims claims_min`, `t06-outside-file files`, `t07-no-row rows:missing`,
`t08-extra-cell-row rows:bad_row`, `t09-usedby-other rows:usedby`, `t10-queued-status rows:status`,
`t11-quote-short span`, `t12-malformed-claim grammar`.

Other reads: `corpus/SOURCES.md` rows 325 at entering **and** at HEAD (max id `S552`, unreconciled);
`evidence/census-start.txt` = 25 `W04` lines + `mori ok …/corpus/SOURCES.md`, no row-count line;
`corpus/lessons/round-58-verifier-spotcheck.md:82-89` = the five routed items.

## 3. Draft — SCORECARD round-59 section skeleton

Paste-ready; `<…>` / `TBD` are placeholders to be filled only from the wave's own receipts.
Style matches rounds 56–58 (`SCORECARD.md:2867-2937`).

````markdown
## Round 59 — active-register binding checker (C1, calibration) and wave-settlement artifact depth entry (C2, depth)

Entering `2b9f03975bfb6e508f35074ac8181ec8bf54e805`; initial freeze `ccfd554e`; amended freeze
`60b3a76ad0524c8978cc51922940be1c8c388915` (counter scratch/ptrs/PIN/name-boundary amendment,
pre-data); validated dispatch wave `w1`, 64 seats, policy v2. C1's data landed with the amended
freeze (tool, 13 fixtures, counter); C2's data (`<entry>`, 6 copies, S-rows) is measured at the
data revision `<DATA_REV>`. Scores entering/after: coverage 6, operability 7, depth 5, freshness
5, calibration 5, adjacency 6. Lowest-scoring tie: depth/freshness/calibration at 5; C1 targets
calibration, C2 targets depth. No scalar score delta claimed; no capability added.

| Claim | Axis | Counting command | Before | After / verdict |
|---|---|---|---|---|
| C1: `tools/mori-register-check.py` at frozen sha256 `38b733d8…472b8` is the ACTIVE capabilities-register checker — unique register identity (`SCORECARD.md:1951`, rows `1989-1990`, not the `— none yet —` stub at `:596`), exact key/name binding for `rounds[832].capabilities_added[0..1]`, every backticked evidence pointer resolvable at R, MANIFEST binding at revision-pinned fleet `2807c6ab…`, and 13/13 committed hostile fixtures rejected with their frozen expect prefix | calibration 5 | `python3 .ufo/waves/round-59/count-c1.py R --scratch DIR` | `C1=unmet selftest=bad fixtures=bad real=bad pointers=bad rev=2b9f03975bfb6e508f35074ac8181ec8bf54e805 failed=tool_absent,selftest,fixtures_absent,real,pointers`, rc 1 — `evidence/control-c1-do-nothing.txt` | `C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=60b3a76ad0524c8978cc51922940be1c8c388915`, rc 0 — `evidence/c1-at-freeze.txt`; re-verified at `<DATA_REV>`, rc 0 — `evidence/c1-at-data.txt` (TBD) |
| C2: `tools/mori-settlement-scan.py` at frozen sha256 `4c04bf21…5ac9a9` scans the five committed r54–r58 wave-results files `SETTLEMENT_SCAN_OK` with `members==seats` per file and fails the r53 file (schema drift, reported); `corpus/knowledge/wave-settlement-artifacts-r59.md` carries `N≥10` byte-exact pin-bound claims over `F≥3` of the six copies in `corpus/evidence/sources-r59/` (each copy byte-equal to its `.ufo` artifact at R), every cited S### row `status=mined` with `used-by` exactly the entry, and 12/12 hostile trees rejected with their frozen expect prefix | depth 5 | `python3 .ufo/waves/round-59/count-c2.py R --scratch DIR` | `C2=unmet selftest=bad scan=bad drift=bad trees=bad entry=bad rows=bad pins=bad tree=bad claims=0 files=0 rev=2b9f03975bfb6e508f35074ac8181ec8bf54e805 failed=copy_absent:…(6 copies)…,drift,entry_absent,scan,selftest,tool_absent,tree,trees,trees_absent`, rc 1 — `evidence/control-c2-do-nothing.txt`; at the amended freeze the same run yields `C2=unmet … entry=bad rows=bad pins=bad tree=bad claims=0 files=0`, rc 1 — `evidence/c2-at-freeze.txt` | **TBD** at `<DATA_REV>`; frozen target `C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=<N≥10> files=<F≥3> rev=<DATA_REV>`, rc 0 — `evidence/c2-at-data.txt` |

Counter selftests (explicit `--scratch`/`TMPDIR`): `C1_SELFTEST pass=6 fail=0`,
`C2_SELFTEST pass=9 fail=0`; the two tool selftests they gate: `REGCHECK_SELFTEST pass=12 fail=0`,
`SETSCAN_SELFTEST pass=10 fail=0` — `evidence/selftests.txt` (re-run byte-identical by
`Mo59Scribe49`). Frozen target tokens were diffed against the emitters: `count-c1.py:262`
and `count-c2.py:452` emit exactly the contract's token set in the contract's order.

Wave: one v2 `w1`, 64 seats (reviewer 20, critic 10, mutation-tester 8, executor 8, scribe 4,
scout 4, connector 2, sentinel 2, revenger 4, simplifier 2); attack share
reviewer+critic+mutation-tester+sentinel = 40/64 = 62.5%; L1 holds the planner seat (connector
items carry the bounded planning/sibling-overlap walks); no `agent://all`. <SETTLEMENT_TBD:
settled count, results-JSON shape, report-file scan, missing/partial reports>.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` start rc 0,
25 `W04` duplicates + `mori ok` — `evidence/census-start.txt`; `corpus/SOURCES.md` 325 rows at
entering and at `<DATA_REV>` = `<END_COUNT>`; end receipt `evidence/census-end.txt` (TBD).

Routed round-58 defects (contract §Routed defects,
`corpus/lessons/round-58-verifier-spotcheck.md:82-89`):

| # | Routed defect | Round-59 disposition |
|---|---|---|
| 1 | SHONEN assessment bound to `kotodama-shokunin/SHONEN.md` | `<TBD: re-filed against mori-shokunin/SHONEN.md, four [~] boxes>` |
| 2 | duplicate source row S552 (repeats S478) | `<TBD: appended reconciliation + ## Mistakes row + QUALITY criterion>` |
| 3 | C1 target/predicate identity | frozen C1 emits every required token; 13 fixtures bind `keys`/`pointers`/`manifest*`/`binding` — `evidence/c1-at-freeze.txt` |
| 4 | C2 control (c) predicates + explicit scratch CLI | frontmatter/no-frontmatter, duplicate K, designated quote spans, exact `used-by`, 11-cell row, `--scratch` on both counters — 12 trees + selftest |

Limits: `<TBD from W1 — at minimum: C1's fixture arm is a reject-only battery authored beside the
tool; C2's §2b "rows opened this round" and "one row per cited artifact copy" have no counting arm
(see §4 F3), and its row binding reads frontmatter `source:` lines only (F4)>`.

Axis observations: `<TBD>` — no scalar change is claimed for calibration (5) or depth (5) until the
C2 data arm and the W1 findings are in; no-harm is a separate seat's verdict.

Assimilation none (`assimilation/` holds only `quarantine-slice/`); quarantine slice re-derived at
round time with hand-checked verdicts in the lesson; considerthese: at most one still-unimplemented
proposal from `considerthese/2026-10-26.md`.

Planned (round 60): `<TBD>`.
````

### Receipt map for the rows above

Existing and committed at `8ff344ff`:

| Receipt | Covers |
|---|---|
| `.ufo/waves/round-59/evidence/control-c1-do-nothing.txt` | C1 Before (entering `2b9f0397`) |
| `.ufo/waves/round-59/evidence/control-c2-do-nothing.txt` | C2 Before (entering `2b9f0397`) |
| `.ufo/waves/round-59/evidence/c1-at-freeze.txt` | C1 After at amended freeze `60b3a76a` |
| `.ufo/waves/round-59/evidence/c2-at-freeze.txt` | C2 at amended freeze (data absent → unmet; a limit, not the claim result) |
| `.ufo/waves/round-59/evidence/selftests.txt` | both counter + both tool selftests |
| `.ufo/waves/round-59/evidence/census-start.txt` | round-start census |

Proposed names for receipts the frozen claims still need (none exists yet):

| Receipt | Covers |
|---|---|
| `.ufo/waves/round-59/evidence/c2-at-data.txt` | C2 After at `<DATA_REV>` — the claim row's `After` cell |
| `.ufo/waves/round-59/evidence/c1-at-data.txt` | C1 re-verified at `<DATA_REV>` (freeze receipt alone is not a landed-tip measurement) |
| `.ufo/waves/round-59/evidence/c2-at-landed.txt`, `c1-at-landed.txt` | optional re-verify at the wave's landed tip (round-56 practice) |
| `.ufo/waves/round-59/evidence/census-end.txt` | round-end census (`exit 0` required by the contract) |
| `.ufo/waves/round-59/evidence/w1-settlement.json` | settlement integration (round-58 precedent) |
| `.ufo/waves/round-59/w1-results.json` | the 64-seat wave result set (named by C2's `REAL_SCAN` for round 59 itself only in round 60) |

## 4. Findings (data for the canonical judge; no remediation performed)

F1 — **Target-token identity holds.** `count-c1.py:262-268` emits
`C1=<met|unmet> selftest=… fixtures=… real=… pointers=… rev=R` and appends
`failed=<comma list>` only when unmet; `count-c2.py:452-458` emits
`C2=… selftest=… scan=… drift=… trees=… entry=… rows=… pins=… tree=… claims=N files=F rev=R`.
Both equal the contract's frozen target strings token-for-token and in order (verified by running
them, §2). This closes the round-58 routed defect 3 as far as the target string is concerned.

F2 — **`selftest=` in the C1 output line is the *tool's* selftest, not the counter's.** The output
token is set from the tool arm (`count-c1.py:114-126`, `EXPECT_SELFTEST` at `:37` =
`REGCHECK_SELFTEST pass=12 fail=0`); the CLI `--selftest` prints the counter's own
`C1_SELFTEST pass=6 fail=0` (6 `chk` calls, `:214-247`). Both were observed and both match the
contract's two separate sentences. No conflict — but `selftest=ok` in the claim-cell must not be
read as the counter self-pass. Same shape in C2 (`:50` `SETSCAN_SELFTEST pass=10 fail=0` vs
`:365-…` `C2_SELFTEST pass=9 fail=0`).

F3 — **C2 §2b has no counting arm.** Contract C2, "Sourced-claim rule (§2b)": *"the entry cites
only S### rows opened this round (one per cited artifact copy; a ≥1 admit / ≥1 reject Gate pair
lands in the round-59 lesson)"*. `eval_entry()` (`count-c2.py:100-190`) only checks that each SID
appearing in the entry's first ten lines is a row with 11 cells, `cells[7] == "mined"` and
`cells[10] == ENTRY`. It never reads the row's opening round, never counts rows per cited copy,
and never looks at the Gate pair. The frozen predicate P-C2 (`count-c2.py:13-33`) omits the same
clause. Consequence as data: `met` is reachable with rows that predate round 59.

F4 — **C2 binds only frontmatter SIDs.** `head = lines[:10]` (`:112`), `sids` is built from `head`
only (`:161-162`), while the contract says "the registry rows **those claims** cite". Body-level
`source:` lines and per-claim citations are neither required nor bound.

F5 — **C2 drift arm asserts exit-status only.** `# drift arm` (`:251-264`) sets `drift_ok` from
`p.returncode != 0`; it does not inspect the FAIL verdict or the `report_file` extra-key reason the
contract names as the drift being reported.

F6 — **C1 fixture arm dead code.** `got = {…}` (`count-c1.py:155-158`) is computed and never used;
the arm's verdict comes from `matched`/`verdict_unmet` (`:159-164`). No effect on any token.

F7 — **C1 emptiness is enforced.** `all_exist = bool(ptrs)` (`:186`) makes an empty pointer list
`pointers=bad`, so the "empty pointer cell" class (f13) plus a fully empty pointer set both fail.

F8 — **Data not yet landed.** At `8ff344ff` the C2 entry, the six `corpus/evidence/sources-r59/`
copies and the round-59 S-rows do not exist (`git cat-file -e` ABSENT; 0 files under
`corpus/evidence/sources-r59/`); `corpus/SOURCES.md` is 325 rows at both entering and HEAD, max id
`S552`. Therefore the C2 `After` cell cannot be filled from the current tree and the skeleton
leaves it `<TBD>`; do not let a freeze-revision receipt (`c2-at-freeze.txt`, all data arms bad) be
pasted into that cell as a result.

F9 — **Wave unsettled.** `.ufo/waves/round-59/w1/` contains only `swarm-registry.json`; no
`w1-results.json`, no seat reports. The wave/attack-share numbers in the skeleton come from
`.ufo/waves/round-59/build-w1-spec.py:16-21` (role counts summing to 64) and the seat's own
assignment (40/64 attack), not from a settled result set.

F10 — **Census start has no row-count line.** `evidence/census-start.txt` is 25 `W04` lines plus
`mori ok <SOURCES path>`; the `Planned`-style "N → N rows" wording used in earlier rounds has no
source in this receipt. Row counts for the after cell must be measured separately (done here:
325 at entering and 325 at HEAD, read-only).

## 5. Scope statement

- Read-only throughout: `git show` / `cat-file` / `ls-tree`, `grep`, `sed -n`, frozen counters run
  with `--scratch` inside `/fast/scratch/hyaku/mori-r59/Mo59Scribe49`. No `git add/commit`,
  no `jj`, no worktree, no fixture repo created, no `pacman`, no tool installs (nothing installed
  or updated), no fleet/sibling writes, no `agent://all` broadcast.
- Only file written: this report. Scratch dir was removed after copying the receipt into §2.
- Not done (out of seat scope): filling the `<TBD>` cells, scoring, judging frozen bytes, editing
  `SCORECARD.md`/`LOG.md`/`corpus/`, or reproducing W1's adversarial constructions.
