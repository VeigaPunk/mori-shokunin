# CritAxisHarm — no-axis-harm audit of the round-45 planned edits

Seat: critic (leaf). Scope: read the round's planned changes and decide, per item, whether an
edit **removes or lowers an axis score's evidence**, breaks a consumer, changes production output,
or contradicts an admitted entry. Nothing in the lane was edited by this seat except this report.

## Snapshot (the tree is moving; every measurement below names its revision or digest)

| object | measured state |
|---|---|
| tip at first read | `3ad8faaa637ae466c61f9427fea1c208bf49ea82` (`round-45: frozen contract, wave-1 spec and dispatch, opened sources`) |
| **tip at last read (landed)** | `18fd68b052a7f06b033421434e59a56e3dd98732` (`round-45: SKILL.md registry refresh, corpus entry + row + README map, QUALITY 120-122, lesson, selftest branches`) |
| contract at last read | `contract.md` **modified** (+28 lines: "Correction 1 — appended before any after-measurement") |
| entering tip | `554ff416459c92f0dea9762f834a556df2990187` |
| `tools/mori-gate-registry.py` at `7cb59c68`, `554ff416`, `b1d7269f`, `3ad8faaa` | `743996b1…a1f` (v1, 308 lines — the r44 frozen bytes) |
| `tools/mori-gate-registry.py` worktree (v2) — window 1 / window 2 | `2b971ec3…da03eda` / `8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832` |
| files modified (uncommitted), window 1 (07:48) | `mori-gate-registry.py`, `mori-round19-regressions.py`, `mori-routed-check.py`, `mori-silence-cases.sh` |
| files modified (uncommitted), window 2 (07:57) | the four above **plus** `mori-disk-rate.py`, `mori-round41-calibration.py`, `mori-routed-r24.py` |
| new (untracked) round-45 instruments | `.ufo/waves/round-45/count-c{1,2,3}.py`, `figures.tsv.draft`, `fixtures/write-scope.json`, `write-scope-run.py`, `corpus/knowledge/census-cgroup-levels-r45.md` |

The worktree was being written throughout the audit (mtimes 07:46–07:57). Every result below names
the snapshot it belongs to; where the two windows disagree the later one is marked **window 2**.
The three files that appeared in window 2 matter: they are exactly the three this audit first named
as the `no_selftest` gap (H1).

## Verdict table

| # | question | verdict |
|---|---|---|
| 1 | does any edit invalidate a pointer SCORECARD.md already cites (r18/r19 gate rows, SKILL.md `--selftest` tallies)? | **not harmed in SCORECARD**; **harmed in SKILL.md** — four registry cells are false against the instruments (`:184`, `:190`, `:191` auditor pin, `:194`), and the landed commit `18fd68b0` measures `REGISTRY=unmet` because three committed rows name three uncommitted counters (`wrong_row=3`) |
| 2 | does the hardened ledger grammar invalidate the round-44 ledger or an earlier committed one SCORECARD cites? | **harmed** for `.ufo/waves/round-44/figures.tsv` as an *admissible* ledger (measured); **not harmed** for SCORECARD's r44 C1 pointer (the r44 counter is frozen) |
| 3 | does auditor v2 break a consumer? does the v1 CLI survive? | **not broken** for the one real consumer (measured against v2 window 2); v1 argv/verdicts survive; **one attribution value changes** and two authority rules now disagree |
| 4 | does adding `--selftest` change a production tool's production output? | **not changed** for all six edited tools (measured, byte-identical production runs); the planned byte-identity *evidence method* is invalid for `mori-round19-regressions.py` and must pin seed+nonce for `mori-silence-cases.sh` |
| 5 | does the new entry contradict an admitted one? | **no contradiction** with `observability-census-r1.md` or `pid-probe-conclusion-r44.md`; **a disclosed narrowing** of `surfaces-r7.md:88-90` |

---

## Item 1 — does an edit remove/lower an axis's evidence?

### 1a. SCORECARD's own pointers: not harmed

The axes table (`SCORECARD.md:8-18`) and the round tables cite:

- **operability 7** — `census --selftest PASS (134 cases)` (`SCORECARD.md:10`); round 13/14/28/31 closures.
  `tools/mori-census.sh` is **unmodified** in both windows (`git status --porcelain tools/` lists the
  seven files named in the snapshot, never `mori-census.sh`), so the 134-case receipt and the census's
  own numbers stand.
- **depth 5** — "source-linked knowledge entries with `source:`/`verified-at:`/`recheck:` lines"
  (`SCORECARD.md:12`). The new entry carries all four lines plus `coverage-map:`/`ground:`; depth's
  evidence is *extended*, not invalidated.
- **freshness 5**, **coverage 6**, **adjacency 6**, **calibration 5** — their pointers name round
  closures, `corpus/README.md`, `PROVINCE.md`, `MANIFEST.json@63729047`; no file they name is edited
  this round.
- **r18 gate rows** — `SCORECARD.md:1143-1145` cite `tools/mori-retention-gate.py`,
  `tools/mori-freeze-order.py`, `tools/mori-dispatch-ledger.py`. All three are **unmodified**. Also
  v2 still audits them clean (measured, below: `PASS row='r18 retention (C1)'`, `PASS row='r18
  freeze-order (C2)'`, `PASS row='r18 dispatch ledger (C3)'`).
- **r19 content review** — `tools/mori-content-review.py`, unmodified.
- **round-23 routed-item check** (calibration evidence, `SCORECARD.md:1505,1517,1535,1971`) — the tool
  *is* edited, but its production projection is byte-identical (item 4).
- **wave settlement** — `SCORECARD.md:1269` cites `tools/mori-wave-settlement.py --selftest 22/22`; the
  tool is unmodified and the scribe's row is additive.
- The `--selftest` tallies (`C1_SELFTEST pass=6`, `GATE_REGISTRY_SELFTEST pass=6`, `C2_SELFTEST pass=5`,
  `C3_SELFTEST pass=6`) are quoted **only in `SKILL.md:183-186`**, nowhere in SCORECARD (`grep -n
  'GATE_REGISTRY_SELFTEST' SCORECARD.md` → no hit).

### 1b. SKILL.md's registry cells: harmed — four cells, including two the round itself just wrote

`SKILL.md` is **committed** at `18fd68b0` (no longer a draft) and carries seven new rows (187, 190-196).
Measured against the worktree instruments after that commit:

```
$ python3 tools/mori-gate-registry.py --selftest        → GATE_REGISTRY_SELFTEST pass=15 fail=0  (15 arms)
$ sha256sum tools/mori-gate-registry.py                 → 8b82ac999091ebe6…   743 lines
$ python3 .ufo/waves/round-45/count-c1.py --selftest    → C1_SELFTEST pass=16 fail=0
$ sha256sum .ufo/waves/round-45/count-c1.py             → 5f2deea0b35c5e13…
$ python3 .ufo/waves/round-45/fixtures/mutants/count-c1.py --selftest
                                                        → C1_SELFTEST pass=15 fail=1   rc=1
$ grep -n MUTANT .ufo/waves/round-45/fixtures/mutants/count-c1.py
                                                        → 478: if False:  # MUTANT: duplicate-id check disabled
```

| cell | says | measured | verdict |
|---|---|---|---|
| `:184` `r44 gate registry (C2)` | v2 `GATE_REGISTRY_SELFTEST pass=6 fail=0`, six named arms; entry cell without `--audit-all`; verdict map without `duplicate`/`wrong_row` | `pass=15`, fifteen arms | **false, untouched by the round** |
| `:190` `r45 ledger counter (C1)` | `C1_SELFTEST pass=10 fail=0` "at sha256 `f80e75ac7421…`"; mutant "disables the duplicate-command check (`if key in cmds:` to `if False:`)" and reads `pass=8 fail=2` rc 1 | `pass=16`; `5f2deea0b35c…`; line 478 disables **duplicate-id** (`if key in cmds:` at 483 is intact); mutant reads `pass=15 fail=1` rc 1 | **false on four counts — the round's own new row** |
| `:191` `r45 gate conformance (C2)` | auditor v2 "sha256 `64db765e60e3…`, 622 lines"; counter `pass=10` at `e8ee29eb8852…` | auditor `8b82ac999091ebe6…`, **743 lines**; counter digest and `pass=10` both correct | **auditor pin false; rest true** |
| `:192` `r45 corpus coverage (C3)` | `pass=19` at `37fd7c24ff52…`; mutant `69bf9b6eb29b…` | both match | **true** |
| `:194` `r44 gate registry (C2) — write scope superseded` | v2 `GATE_REGISTRY_SELFTEST pass=10 fail=0` | `pass=15` | **false** |
| `:187` disk write rate · `:195` · `:196` | `MORI_DISK_RATE_SELFTEST pass=14`; r44 `C2_SELFTEST pass=5`, `C3_SELFTEST pass=6` | match | **true** |
| `:165/:166` silence oracle · `:182` r19 · `:646/:665` routed-check · `:721` routed-r24 | 24 / 26 / 20 / 26 | match (paragraph at `SKILL.md:199-204` records the in-place update) | **true — my window-1 finding on `:646` ("none built in") is fixed** |

So the two cells I first named are not the whole set: `:646` is fixed, `:184` remains, and the round's
own new rows `:190`, `:191` (auditor pin) and `:194` quote an instrument state that no longer exists.
Every one of these passes the auditor (it reads the *tool*, never the cell's tally/digest), so
`REGISTRY=met` coexists with four false cells. The cheapest fix is a re-pin at the landing commit:
`:190` tally+digest+mutant description, `:191` auditor digest+line count, `:194` v2 tally, `:184` tally
and arm list.

### 1b-bis. The landed commit: the registry now points at three uncommitted instruments

`18fd68b0` committed the SKILL.md rows but **not** the three round-45 counters (they are still
`?? .ufo/waves/round-45/count-c{1,2,3}.py`), and v2's global `wrong_row` arm reads every row's entry path
at the revision:

```
$ python3 tools/mori-gate-registry.py --rev 18fd68b0 --repo $PWD --audit-all
wrong_row line=190 row='r45 ledger counter (C1)' entry=.ufo/waves/round-45/count-c1.py absent at 18fd68b052a7
wrong_row line=191 row='r45 gate conformance (C2)' entry=.ufo/waves/round-45/count-c2.py absent at 18fd68b052a7
wrong_row line=192 row='r45 corpus coverage (C3)' entry=.ufo/waves/round-45/count-c3.py absent at 18fd68b052a7
registered=36 unregistered=0 no_selftest=0 duplicate=0 wrong_row=3 tables=7
REGISTRY=unmet            (auditor rc 1)
```
At `--rev WORK` the same command reads `registered=39 … wrong_row=0 … REGISTRY=met`. So the round's own
landing commit is the one state where C2 is **unmet**, and the cause is commit ordering, not a predicate:
the rows and their instruments must land in the same commit (or the counters must be committed first).
This also means any after-measurement run at `18fd68b0` sees `C2=unmet`, and `count-c2.py`'s
`wrong_row == 0` check (`:548`/`:569` neighbourhood) fails on it. Fix before the after-measurement, not
after: a later commit that only adds the counters changes the measured revision and voids the receipt.

### 1c. Scope note found while checking durability (pre-existing, not caused by this round)

`SCORECARD.md:2413` cites the r44 C2 after-value **without** `--mutants-dir`:

```
$ python3 .ufo/waves/round-44/count-c2.py 3ad8faaa --repo $PWD \
    --counter .ufo/waves/round-44/count-c1.py --counter .ufo/waves/round-44/count-c2.py \
    --counter .ufo/waves/round-44/count-c3.py
check mutant_kill       FAIL (count-c1.py mutant absent; count-c2.py mutant absent; count-c3.py mutant absent)
C2=unmet            rc=1

$ … same + --mutants-dir .ufo/waves/round-44/fixtures/mutants
check mutant_kill       PASS (count-c1.py killed (fail=1); count-c2.py killed (fail=1); count-c3.py killed (fail=1))
C2=met              rc=0
```
`count-c2.py` defaults `--mutants-dir` to `fixtures/mutants` (repo-root-relative), while
`SKILL.md:185` documents "`fixtures/mutants/<basename>` **beside each counter**". The cited command
therefore does not reproduce the declared value at any tip. This is round 44's citation, not v2's
doing; the round-45 count-c2 spec already fixes its own default (".ufo/waves/round-45/fixtures/mutants
(an existing path)"). Report it so the round does not inherit the broken citation as a baseline.

---

## Item 2 — does the hardened ledger grammar invalidate a committed ledger?

**Harmed: `.ufo/waves/round-44/figures.tsv` (the only scored figure ledger in the lane).**

Revision sensitivity of all 16 rows, measured with the ledger's own commands:

| revision pair | rows that move |
|---|---|
| `554ff416` → `3ad8faaa` | **only F15** (73 → 74) |
| `554ff416` → `b1d7269f` | **only F15** |

No row carries `CONST=`. The round-45 counter on that ledger:

```
$ python3 .ufo/waves/round-45/count-c1.py 554ff416 --repo $PWD \
    --ledger .ufo/waves/round-44/figures.tsv --other-rev 18fd68b0 \
    --witness-dir .ufo/waves/round-44/fixtures
check revision_sensitivity   FAIL (F02 value=2 at both revisions; F03 value=3 at both revisions; …)
check revision_moves         PASS (moved=5 floor=1)
check const_cap              PASS (const=0 cap=14 rows=16 …)
witness figures-r43.tsv      NOT-PROVING (rows=12 classes=5 fails=rows_parse,revision_sensitivity,revision_moves)
C1=unmet mismatches=0 rows=16 … witnesses=1/1 witnesses_vacuous=0/1
    failed=revision_sensitivity,witnesses_vacuous     rc=1
```

So under P-C1 (including the appended Correction 1, whose `moved>=1` and CONST-cap arms the counter now
implements and which *pass* here) the r44 ledger is **inadmissible**: `moved=5` clears the floor, `const=0`
clears the cap, and eleven rows are still revision-constant with no `CONST=`, so `revision_sensitivity`
fails. Under the frozen r44 counter the same bytes still score `C1=met`. Affected artifacts, named:

- `.ufo/waves/round-44/figures.tsv` — inadmissible under the new grammar; its values still reconcile at
  `554ff416` (`mismatches=0`).
- `.ufo/waves/round-44/count-c1.py` — **frozen, unedited** (`git status` clean; sha in
  `.ufo/waves/round-44/evidence/freeze-r44.txt`); it still scores the ledger, which is why
  `SCORECARD.md:2410`'s pointer (`count-c1.py <landed tip>` → `C1=met`) is **not** invalidated.
- `.ufo/waves/round-44/fixtures/figures-r43.tsv` — a *witness* expected to fail; unaffected
  (`witnesses=1/1` rejected).
- `.ufo/waves/round-45/figures.tsv.draft` — **already compliant**: 15 rows, 5 classes, 10 rows carry
  `CONST=<reason>`, 5 are MOVE. Its MOVE rows were spot-checked: F05 `43` at both tips, F08 `28` at both
  tips (so both genuinely need the landed tip to move, and the +7 rows / +3 branches the plan expects
  are the only motion).
- The other 33 committed `*.tsv` files (`git ls-files '*.tsv'`) are round-20 build artefacts, not
  P-C1 ledgers; none is scored but by the r45 counter and none is cited by SCORECARD.

No earlier figure ledger exists (`ls .ufo/waves/*/figures.tsv*` → round 44 only), so "an earlier
committed ledger SCORECARD cites" has no referent.

**Instrument status, two snapshots.** The substantive verdict is stable (`failed=revision_sensitivity`
on both). The counter's *own* `--selftest` was red at 08:01 and green at 08:0x, and both states matter
because `SKILL.md:190` still pins the earlier one:

```
08:01 bytes
selftest FAIL short_sha_tip_rejected: TypeError: not enough arguments for format string
selftest FAIL absent_path_zero_rejected: 'git ls-tree -r --name-only @REV@ corpus | wc -l'
    rejected: ['row 1: asserted 0 from a listing verb (ls-tree/ls-files): an absent path is
    indistinguishable from a zero count; take a zero from show, cat-file -e or rev-list --count']
C1_SELFTEST pass=14 fail=2          rc=1

08:0x bytes (sha256 5f2deea0b35c5e13…)
C1_SELFTEST pass=16 fail=0          rc=0
```
- At 08:01 `short_sha_tip_rejected` (`count-c1.py:1022`) set
  `rows[11] = "F12\t12\tchecks\tgit log --format=%s @REV@ | wc -l"` — a bare `%s` where the arm three
  lines above correctly writes `%%s` for the same shape; the literal was later `%`-interpolated, hence
  the `TypeError`. Fixed by 08:0x.
- At 08:01 `absent_path_zero_rejected` was rejected by the *listing-verb* rule before the arm's intended
  "absent path" rule fired, so the arm did not test what its name claims. Fixed by 08:0x.
- The ledger run now also prints `witnesses_vacuous=0/1` alongside `witnesses=1/1`
  (`.ufo/waves/round-44/fixtures/figures-r43.tsv`): the witness is rejected, and the second counter says
  it is not counted as a *vacuity* witness. Keep both numbers; either alone is readable as the other.

Neither 08:01 defect is an axis harm by itself (the C1 verdict did not change), but the sequence is
why `SKILL.md:190` is false: the row was written against `pass=10`/`f80e75ac…` and the instrument moved
twice more before landing.

Minor doc/code precision note (non-blocking): the counter's docstring lists `(`, `)` and `$` as
unconditional "shell metacharacter" rejections, but `split_stages` accepts them inside single quotes
(`count-c1.py:161-186`: `elif ch in ";$`<>&()\n\r"` outside quotes; the `'` branch appends literally).
That is what lets r44's `grep -cE '^ {0,3}\|…'` and the draft's `'\.md$'` rows pass. A reader
auditing admissibility from the docstring would over-reject.

---

## Item 3 — does auditor v2 break a consumer?

`grep -rn "mori-gate-registry"` over the lane (excluding `.git/` and `__pycache__`) gives exactly one
*executing* consumer:

- `.ufo/waves/round-44/count-c2.py` — materialises the auditor **at a revision**
  (`materialize(repo, rev, "tools/mori-gate-registry.py", tmp)`, line 132) and runs
  `--rev <rev> --repo <repo> --audit A --audit B …`, expecting rc 0 + `REGISTRY=met`, then
  `--selftest` with `pass>=4 fail=0` (lines 137-139).
  **Measured against v2, the exact consumer argv still passes:**
  ```
  $ python3 tools/mori-gate-registry.py --rev 3ad8faaa --repo $PWD \
      --audit .ufo/waves/round-44/count-c1.py --audit .ufo/waves/round-44/count-c2.py \
      --audit .ufo/waves/round-44/count-c3.py
  audit …count-c1.py      PASS row='r44 figure ledger (C1)' (8 cells, entry resolves, --selftest argv branch)
  …
  registered=3 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0 tables=7
  REGISTRY=met        rc=0
  ```
  and `GATE_REGISTRY_SELFTEST pass=15 fail=0` (window 2) satisfies `pass>=4 fail=0`.
- The remaining hits are fixture path lists (`.ufo/waves/round-44/count-c1.py:44`, `count-c3.py:44`, the
  mutant copies) and prose (`corpus/QUALITY.md:964`, `SKILL.md:184`). No `tools/mori-*.py` invokes it.

**v1 CLI survives**: `--rev`, `--repo`, `--registry`, repeatable `--audit`, `--selftest`, the
`REGISTRY=met|unmet|REGISTRY_SETUP` tokens and 0/1/2 exits are all still present (the `main()` at
`tools/mori-gate-registry.py:673` in the last-read 743-line v2), and `--rev WORK` is still accepted. Tightenings that are intended, not breaks: absolute or
`..` audit paths are now rejected (`safe_relpath`), and the substring fallback is gone (P-C2 item 2).
No current population member depended on the fallback — measured at `3ad8faaa`, `unregistered=3` and
each of the three really has no row.

**But two attribution authorities now disagree, and one cited receipt changes value.**

1. Auditor v2 attributes a path to `matches[0]` — the **first** row in document order (`row = matches[0]`).
   The round's own write-scope fixture states the opposite rule: "a row attributes a path only through
   its entry cell naming that exact repo-relative path; **the last such row in document order
   supersedes earlier ones**" (`.ufo/waves/round-45/fixtures/write-scope.json`, `source.attribution`).
   The append-only superseding row ScribeRegistryRows is told to write *names the same path* as
   `r44 figure ledger (C1)`, so the two instruments will attribute the same path to different rows
   (auditor → the old row; arm → the superseding row).
2. Measured attribution change for an existing PASS:
   ```
   v1: audit tools/mori-census.sh  PASS (row 'drift pin': 8 cells, entry resolves, --selftest present)
   v2: audit tools/mori-census.sh  PASS row='census'   (8 cells, entry resolves, --selftest argv branch)
   ```
   `tools/mori-census.sh` is named by two rows under v2's first-command rule (`census`, `drift pin`);
   three other tools are named twice (`mori-evidence-loss.py` ×2, `mori-source-drift.py` ×2,
   `mori-sources-appendonly.py` ×2). v1's shortest-entry sort picked `drift pin`; v2's first-match
   picks `census`. Deterministic, but it invalidates receipts that
   quote the old label: `.ufo/waves/round-45/w1/PlanDataWalk.md:542` and
   `.ufo/waves/round-44/w1/ExecGateInventory.md:163` both quote `row 'drift pin'`.
3. Diagnostics gap — **present in window 1, closed in window 2 (measured).** Window 1 kept a seventh
   status `bad_row` (missing cell / 7-cell row / unresolvable entry) that set `ok=False` without
   appearing in the printed counter line, so a run could print `REGISTRY=unmet` with every printed
   counter at 0 (`count-c2.py` closed the vacuity with `record("auditor_rc"`, so it was diagnostics
   only). Window 2 folds those row-level failures into the printed `wrong_row` and adds
   `mode=`/`population_digest=` lines:
   ```
   $ (throwaway repo, one seven-cell row)
   audit tools/t.sh   FAIL row='short row' (row has 7 cells, expected 8)
   mode=population
   population_digest=006e88f8b9b3f6b6a3b49c24f5ff1a9b180e0ea91610638241d39b970790b571
   registered=0 unregistered=0 no_selftest=0 duplicate=0 wrong_row=1 tables=1     REGISTRY=unmet  rc=1
   ```
   No defect remains here; record it as closed so no one re-opens it as a live gap.

---

## Item 4 — does adding `--selftest` change production output?

### `tools/mori-round19-regressions.py` — not changed by construction; byte-identity unprovable

`main()` intercepts raw argv and only diverts when the literal token appears:
```
raw = list(sys.argv[1:] if argv is None else argv)
if "--selftest" in raw:
    if raw != ["--selftest"]: … return 2
    return run_selftest()
args = parse_args(raw)          # unchanged production path
```
Measured (before = `git show 3ad8faaa:…`, after = worktree copy, both run from identically named
files so `argv[0]` matches):
```
mori-round19-regressions.py:  --help BYTE-IDENTICAL;  no-args BYTE-IDENTICAL (rc 2 both)
mori-routed-check.py:         --help BYTE-IDENTICAL;  no-args BYTE-IDENTICAL (rc 2 both)
mori-silence-cases.sh <bad-census-path>: BYTE-IDENTICAL (rc 2 both)
```
A full production run of `--mode after` (content tool + freeze tool + frozen expected, output into my
scratch) differs between before and after in **34 leaf keys, all digests** (`inputs_sha256.*`,
`process.stdout_sha256`); every status, case id, exit code and issue list is equal.

**The finding is the evidence method, not the code.** The *unmodified* harness is not byte-stable
across two runs of the same bytes: two `before` runs differ in 4 leaves
(`c2/fixture_inputs_sha256/register`, three `c2/processes/*/stdout_sha256`) because
`mori-round19-regressions.py:980` creates its sandbox with
`tempfile.mkdtemp(prefix="mori-r19-regressions-", dir=tmpdir)` and hashes content that carries that
path. No `TMPDIR` pin removes the randomness. So "production invocations must produce byte-identical
output to before on one representative call each" **cannot be satisfied for this tool**; a single
before/after diff will always differ. The honest evidence is the behavioural projection (statuses,
case ids, exits, issues) plus a before-vs-before control showing the digest leaves already fluctuate.

### `tools/mori-routed-check.py` — not changed, measured

Full production run, byte-identical:
```
$ python3 ./mori-routed-check.py --repo <lane> --rev 554ff416 --round 24
before rc=0  after rc=0   cmp → identical   11484 bytes  "held":4,"items":4
```

### The three window-2 edits (`mori-disk-rate.py`, `mori-round41-calibration.py`, `mori-routed-r24.py`) — not changed, measured

Committed `3ad8faaa` bytes vs worktree, run from identically named copies:
```
--help                       BYTE-IDENTICAL (all three)
mori-disk-rate.py  --a S1 --b S2 --interval-ms 1000        rc 0 both, PRODUCTION BYTE-IDENTICAL
mori-round41-calibration.py --repo <lane> --reference-rev 554ff416 3ad8faaa   rc 1 both, BYTE-IDENTICAL
mori-routed-r24.py --repo <lane> --rev 554ff416            rc 0 both, PRODUCTION BYTE-IDENTICAL
```
(The round41 run exits 1 on the same finding in both versions; the comparison is of bytes and rc.)

### `tools/mori-silence-cases.sh` — not changed by construction

The branch is inserted before the positional parse (`case "${1:-}" in --selftest) SELFTEST=1; shift
;; esac` at `:189`), the re-exec after the entropy scrub carries the flag (`exec bash "$SELF"
--selftest`, `:258`), and the new fixtures use `$TMPDIR` only (`:301-308`) while production keeps
`WORK=$(mktemp -d /tmp/mori-silence-cases.XXXXXX)`. Before/after on the argv-validation path is
byte-identical (above). Caveat for the executor's evidence: a bare production run is *per-run random*
unless both pins are set — `MORI_SHUFFLE_SEED` (case order, `:82`) and `MORI_RUN_NONCE` (fixture
nonce, `:205`), and the script's own header says "pinned stdout stays byte-identical because no case's
grade depends on the salt" (`:174`). A bare before/after diff proves nothing; the receipt must name
both pins.

---

## Item 5 — does the new entry contradict an admitted one?

Entry: `corpus/knowledge/census-cgroup-levels-r45.md`, 47 lines (limit 90). Its grounding checks out
byte-for-byte:

```
$ sha256sum .ufo/waves/round-45/assimilation/opened/cgroup-v2.rst.src
a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad   (matches the entry's source line)
$ grep -c 'MORI_CGROUP_LOCAL_EVENTS="$FX/cgroup/memory.events"' tools/mori-census.sh   → 1
opened copy, cited lines: 1468 memory.events · 1474-1476 hierarchical · 1476-1477 "local counterpart"
· 1506-1508 oom_kill definition · 1517 memory.events.local · 1518-1519 "local … not hierarchical"
census: 1705-1706 LOCAL_EVENTS/SERVICE_EVENTS defaults · 1708-1711 the if/elif · 1844 the crit
finding's unconditional `path=${LOCAL_EVENTS}` · 1862 `local_oom_kill=${service_oom_kill:-unavailable}`
```
All present as quoted.

- **`observability-census-r1.md` — no contradiction.** `:135` says "The probe now **prefers**
  `memory.events.local`, which is immune to both traps the ancestor/service reads hit: propagation …
  and restart". A *preference* plus a fallback is compatible; the immunity is scoped to the local
  file. The new entry narrows the implication (the reported field can still be the service-hierarchical
  read), it does not deny the sentence.
- **`pid-probe-conclusion-r44.md` — no contradiction.** The entry cites it only as precedent in form
  and quotes "the read alone separates none of these" (7 words), which exists at `:53`.
- **`oom-kill-counter-kernel-only-r12.md:12` — no contradiction, and it is disclosed.** r12 puts
  `memory.events.local` at `1505–1509`; the opened copy has it at `1517-1519`, and the entry says so:
  "the two renders differ, so a line number travels with its copy and digest, not alone."
- **`surfaces-r7.md:88-90` — a real tension, disclosed, not silent.** r7: "the bare `oom_kill=` is
  still the parent cumulative counter, and **the session-service reading is printed next to it as
  `local_oom_kill=`** (`:754`)". The code's first branch reads the *slice's* `.events.local`, so r7's
  characterization is true only on the fallback path. The new entry states this openly: "Its phrase
  'session-service reading' is looser than the code: the first branch reads the *slice's*
  `.events.local`." Two admitted entries will therefore describe one field differently. The smallest
  safe correction is the one already present (the new entry names r7 and the branch); do **not** edit
  r7 — a one-line pointer from a later round-45 correction section is the append-only way.

---

## Cross-cutting hazards the plan does not name (both bear on an axis move)

### H1 — the frozen wave spec names three files; the worktree now edits six (window 2 closes the gap, outside the spec)

`ExecSelftestModes` freezes the premise "the three lane tools that have none" and names
`mori-silence-cases.sh`, `mori-round19-regressions.py`, `mori-routed-check.py`. Measured, that premise
was false at the entering tip: **six** population files lacked a real branch.

- Four *registered* tools, measured at `3ad8faaa` with v2:
  ```
  … FAIL row='r19 finite regressions' … no real --selftest argv branch
  … FAIL row='routed round-23 items (r24, C1)' … no real --selftest argv branch
  … FAIL row='routed round-24 items (r25, C1)' … no real --selftest argv branch
  … FAIL row='silence oracle' … no real --selftest argv branch
  registered=29 unregistered=3 no_selftest=4 duplicate=0 wrong_row=0 tables=7   REGISTRY=unmet rc=1
  ```
  `mori-routed-r24.py`'s only `--selftest` strings are its *subprocess target*
  (`:96 EVIDENCE_COMMAND = "python3 -I -B tools/mori-pressure.py --selftest"`, `:422`), never its own
  argv; no w1 item names the file (`grep -n 'routed-r24'` over `.ufo/waves/round-45/w1-spec.json` →
no hit; a mid-wave message would not appear there).
- Two *orphan* tools had no `--selftest` and no alternate flag (`--help`; `grep -c -- --selftest` → 0),
  and ScribeRegistryRows told the scribe to **admit** that ("If a tool has no `--selftest` mode, say so
  in the self-test cell … and name it as a round-46 finding"). Giving those two honest 8-cell rows
  produces `no_selftest`, not `registered` (throwaway repo under TMPDIR, window 1):
  ```
  audit tools/mori-disk-rate.py            FAIL row='disk write rate (r34)' (… no real --selftest argv branch)
  audit tools/mori-round41-calibration.py  FAIL row='r41 calibration' (… no real --selftest argv branch)
  registered=0 unregistered=0 no_selftest=2 duplicate=0 wrong_row=0 tables=1   REGISTRY=unmet  rc=1
  ```
  So from the frozen item alone the projected landed state was `no_selftest=3` and `C2=met` was
  unreachable (`count-c2.py` fails on `record("no_selftest"` (`:563` in the 07:57 snapshot), on
  `record("population_members"` (`:548`) and on `record("auditor_rc"` (`:569`)).

**Window 2 changes the answer.** All six files are now edited and every branch is real, with a computed
tally (not a constant — e.g. `R19_SELFTEST pass=26 fail=0` is emitted from `tally.check(...)` results):
```
tools/mori-disk-rate.py             MORI_DISK_RATE_SELFTEST pass=14 fail=0      rc=0
tools/mori-round41-calibration.py   MORI_R41_CALIBRATION_SELFTEST pass=10 fail=0 rc=0
tools/mori-routed-r24.py            ROUTED_R24_SELFTEST pass=26 fail=0           rc=0
tools/mori-routed-check.py          ROUTED_CHECK_SELFTEST pass=20 fail=0         rc=0
tools/mori-round19-regressions.py   R19_SELFTEST pass=26 fail=0                  rc=0
tools/mori-silence-cases.sh         MORI_SILENCE_CASES_SELFTEST pass=24 fail=0   rc=0
round-45 counters                   C2 pass=10 · C3 pass=19, fail=0; C1 pass=14 fail=2 at 08:01 (item 2)
$ python3 tools/mori-gate-registry.py --rev WORK --repo $PWD --audit-all
# before the rows landed (07:57): registered=33 unregistered=6 no_selftest=0 → unmet (rows absent)
# after they landed     (08:0x): registered=39 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0 tables=7 → met
```
The population is **39** targets (33 `tools/` files + 3 round-44 counters + 3 round-45 counters), so
`population_members` requires `registered == 39`, not 36. The six unregistered at 07:57 were the three
orphan tools plus the three round-45 counters; the landed rows close all six, and the three branches
that appeared later close `no_selftest`. C2 is reachable on the landed *worktree*; at the landed *commit* it is not, because the counters are
uncommitted (item 1b-bis). The intermediate state is
independently measured in `.ufo/waves/round-45/w1/ScribeRegistryRows.md:23-27`
("my rows + the three ExecSelftestModes branches … `no_selftest=3`, `unmet`"), which agrees with the
H1 projection this audit made before the branches landed. **The hazard is provenance, not arithmetic:** three of the six edited files
(`mori-disk-rate.py`, `mori-round41-calibration.py`, `mori-routed-r24.py`) are named by no frozen w1
item, while the seat contract says a seat writes "ONLY … the exact files your item names". If the L1
extended the wave mid-run (a message, not the frozen spec), that extension must be recorded in the wave
report — otherwise three lane files were edited outside the declared write scope, and P-C2's
`no_selftest=0` now rests on work no item authorises. Also note `population_members` requires
`registered == members` = 39, so every row must be *attributed*, not merely present.

### H2 — duplicate authority for the same four write-scope cells

- `.ufo/waves/round-44/w1/SentTools.md:37,433` (F8) calls the four r44 write-scope cells "false as
  written", on the *trust-boundary* argument (the C1 gate executes arbitrary ledger pipelines; the C3
  gate executes an arbitrary program; all four selftests follow `GIT_DIR`).
- `.ufo/waves/round-45/evidence/write-scope.txt:350-362,166-170` measures all four **TRUE**
  (`FALSE: -`, `writescope_mismatch=0`) by running each `--selftest` in a sandbox; the same file
  honestly records that the *positive* clauses are "not observed" and TRUE "rests on the negative
  half".
- ScribeRegistryRows item 3 tells the scribe to write a superseding row for "the two round-44
  write-scope cells the sentinel measured false".

Neither measurement is wrong; they answer different questions (capability vs observed writes) — but
the round would land a second cell about the same path with no arbiter, and the write-scope fixture
quotes only the **original** cell (`entries[0].declared`), so the arm will keep saying TRUE about a
row the superseding row corrects, and will never test the new cell. Combined with the item-3
attribution disagreement (last-wins in the fixture vs first-wins in the auditor), the same append-only
row is "the" row for one instrument and not the other.

---

## Smallest safe corrections, in order

0. **Commit the three round-45 counters (with their mutants, witnesses and ledger) in the same landing
   commit as the rows that name them** — otherwise `--rev <landed>` measures `wrong_row=3` and
   `REGISTRY=unmet` (item 1b-bis). This is the one correction that changes a measured verdict today.
1. **Record the six-file scope delta** (H1): the frozen item names three tools, the worktree edits
   six; without that record, `no_selftest=0` — and therefore `C2=met` — rests on unassigned edits.
   The six rows have since landed; `registered=members=39` holds at `--rev WORK` and fails at the
   landed commit only for the reason in correction 0.
2. Re-pin the four false cells at the landing commit: `SKILL.md:184` (tally + arm list + `--audit-all` +
   the new failure causes), `:190` (tally, counter digest, and the mutant description — it names the
   *duplicate-command* check, line 478 disables *duplicate-id*), `:191` (auditor digest `64db765e…`/622
   lines → `8b82ac99…`/743), `:194` (v2 tally 10 → 15). No mechanical check reads a cell's tally or
   digest, so `REGISTRY=met` coexists with all four being false.
3. Pick **one** attribution rule for a path named by several rows and use it in both instruments; the
   append-only supersede design implies last-wins, so either change the auditor's `matches[0]` or state
   first-wins in `write-scope.json` and accept that the superseding row is never attributed.
   While the rule is undecided, do not quote `row 'drift pin'` as reproducible
   (`PlanDataWalk.md:542`).
4. Have the superseding write-scope row quote F8's *capability* sentence and the arm's *observation*
   sentence, and extend `fixtures/write-scope.json` with an entry for the superseding row — otherwise
   the correction is unmeasured.
5. For `mori-round19-regressions.py`, replace "byte-identical production output" with the behavioural
   projection plus a before-vs-before control; for `mori-silence-cases.sh`, require
   `MORI_SHUFFLE_SEED` + `MORI_RUN_NONCE` in the evidence command.
6. Cite the r44 C2 receipt with its `--mutants-dir` (item 1c) or footnote it as under-specified; the
   r45 counter's default already exists.

## What this audit did not do

- Did not edit, format or re-run any instrument's *remedy*; no lane file was modified.
- Did not judge the claims' predicates (CritContract, CritC2Target hold those), the counters'
  single-check granularity (MutCounters), or the entry's quotes line-by-line (RevEntryQuotes).
- Did not measure the in-flight files' final bytes: `tools/mori-gate-registry.py`,
  `mori-round19-regressions.py`, `mori-routed-check.py`, `mori-silence-cases.sh`,
  `mori-disk-rate.py`, `mori-round41-calibration.py`, `mori-routed-r24.py` were still being written
  during the audit; a landing commit (`18fd68b0`) and a contract correction section appeared while I
  worked, and the counters changed again after it. The digests above name the snapshot each result
  belongs to. Anyone writing the verdict line must re-measure `--rev <landed> --audit-all` first —
  today that reads `wrong_row=3`, not `met`.
- No tools were installed or upgraded; no network fetch was made; no pacman transaction was run.

Scratch (`TMPDIR=.ufo/waves/round-45/tmp/CritAxisHarm`, plus the throwaway repos under it) was created
by this seat and is removed at the end of the run.
