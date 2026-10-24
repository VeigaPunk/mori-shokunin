# The verdict machine, round 4 — matcher, anti-sniff, `:227`, per-round close tracking

seat: **verdict-note-writer** (round-4 flash wave) · lane mori-shokunin · written
2026-10-15T17:47Z · detection and report only; nothing here remediates a fleet
process. This seat writes **this file only** (SCORECARD.md / LOG.md are
parent-owned; `corpus/evidence/` belongs to the receipts-writer).

describes the two tools at the round-4 working-tree bytes:

| tool | sha256 | revision |
|---|---|---|
| `tools/mori-silence-cases.sh` | `be0e28b8bf3cc34e2a35e6cea7c05bffff376111b42d985b6bec7f0e21f59456` | r4 oracle, 745 lines |
| `tools/mori-census.sh` | `af2d4e79e69b70bb0b5aecd6acc9608fc7c16b0716766d4a60310e0689d350d7` | `VERSION=census-r3` (`:61`), 1438 lines |

lane HEAD `bbcc1adcefd95f212dcab5dc8b2c39e41b111e63`; both tools were still
uncommitted at this seat's clock, so every figure is pinned to the hashes above
and re-checked before and after each run. Baselines for the "before" column: the
frozen r3 oracle `505a7504…` (git HEAD bytes) and the r2 census `fe22a14f…`
(`VERSION=census-r2`). `VERSION=census-r3` names the *probe revision*, not the
round number — the r2 census was `VERSION=census-r2` (`corpus/knowledge/silence-cutover-r3.md:8`).

Every measurement below was taken by this seat in `/tmp/mori-vnw-r4/` (scratch,
never in the lane tree) and cross-checked against the receipts-writer's
independent runs under `corpus/evidence/verdict-r4-20261015T173551Z-*.log`; where
the two disagree the difference is stated.

## 1. The matcher defect: an expanded `|` is a literal, so two cases were unwinnable

**Mechanism.** The frozen oracle compared the observed state with the wanted state
through a `case` pattern built by parameter expansion:

```
tools/mori-silence-cases.sh (frozen 505a7504…:361-365)
  case "$obs" in
    $want) : ;;
    *) ok=0; why="state want [$want] got [$obs] via $api";;
  esac
```

In bash, a `|` that arrives *through expansion* is an ordinary character in the
pattern, not the alternation operator — alternation is syntactic only. Measured on
this host, GNU bash 5.3.15:

```
$ bash -c 'a="x|y"; for v in x y "x|y"; do case "$v" in $a) echo "$v: MATCH";; *) echo "$v: no-match";; esac; done'
x: no-match
y: no-match
x|y: MATCH
$ bash -c 'a="x|y"; for v in x y "x|y" z; do if [[ "$v" =~ ^($a)$ ]]; then echo "$v: MATCH"; else echo "$v: no-match"; fi; done'
x: MATCH
y: MATCH
x|y: no-match
z: no-match
```

Two of the twenty-seven frozen cases pass a want-*set*:
`ledger-missing-not-silent` `'not-open|unavailable'` (frozen `:455`) and
`report-future-no-close` `'progressing-weak|silent'` (frozen `:613`). Under the
frozen matcher those can only be satisfied by the literal strings
`not-open|unavailable` and `progressing-weak|silent` — which are **not states in
the vocabulary** (`silent | progressing | progressing-weak | young | not-open |
unavailable`, `tools/mori-silence-cases.sh:67-68`). So:

- an honest implementation that emits a single state can reach at most
  `matched=25 total=27`; the registered end-goal `N = M` was arithmetically
  unattainable, which is what round 3 diagnosed
  (`corpus/knowledge/silence-cutover-r3.md:182-217`);
- and the *only* way to pass those two cases was to print a string no grader
  should accept — the defect was also the accomplice of the forgery in §2.

**Witness (re-measured, independently).** A scratch copy of the frozen oracle with
only the matcher block replaced by `[[ "$obs" =~ ^($want)$ ]]` scores
`matched=27 total=27`, exit **0**, at the identical r2 census bytes
(`fe22a14f…`, sha re-checked mid-run). My copy hashes to
`ae95b601b8c49cfeff275d223e37e68cf0a3602280bad70efeb9911fc07182fe` — **byte-identical
to the round-3 witness** recorded in
`corpus/evidence/cutover-r3-20261015T165712Z-oracle-counterfactual.log`. The frozen
file itself was never edited (`FROZEN_ORACLE_SHA256_BEFORE == AFTER` in that receipt).

**The fix.** `want_match()` (`tools/mori-silence-cases.sh:342-348`, call site
`:389`) splits the want on `|` and compares **exact strings**, never patterns:

```
want_match() {
  local obs=$1 w
  for w in ${2//|/ }; do
    if [ "$obs" = "$w" ]; then return 0; fi
  done
  return 1
}
```

Exact equality was chosen over the regex witness deliberately: an exact compare
cannot let a state name act as a glob (`*`, `?`, `[...]`) or as a regex
metacharacter, and it keeps the matcher free of the `[`-quoting hazard that made
the original `case` construct look correct.

**Measured effect.** `bash tools/mori-silence-cases.sh` at the r4 bytes →
`MORI_SILENCE_CASES: matched=28 total=28`, exit **0**. The two round-3 FAILs now
pass with the observed states they always had:
`ledger-missing-not-silent (state=unavailable via lane finding=0 rc=0)` and
`report-future-no-close (state=silent via lane finding=1 rc=1)`.

**This is not a loosened expectation.** `diff` of the `assert_case` want-strings
between the frozen revision and the r4 revision is **empty**; the `new_case` ids
and the 27 case ids are also unchanged (`diff` empty for both). The only change to
what each case demands is the matching mechanism, so the 25 previously passing
probes could not have been affected by the fix.

## 2. The sniffer channels: which existed, what closed them, and what is left

### 2.1 Channels that existed (frozen `505a7504…`)

The oracle built each fixture under a directory named after the case and handed
that directory to the system under test:

| channel | frozen line | what the SUT could read |
|---|---|---|
| case id inside the fixture path | `:149` `CASE_DIR=$WORK/c/$CASE_ID` | `MORI_SHOKUNIN_ROOT=<work>/c/<case-id>/root` → the case identity |
| fixture marker | `:269` `MORI_FIXTURE=1` | "I am being graded", no logic needed to branch on |
| the path conduit | `:270` `MORI_SHOKUNIN_ROOT="$CASE_ROOT"` | and with it `MORI_UFO_DIR`, `MORI_STATE_DIR`, `MORI_WAVES_DIR`, `MORI_TIMELINE_FILE`, `MORI_CGROUP_*`, `MORI_DISK_TARGETS` — all sharing the same `$CASE_DIR` prefix |

The expectation table *is* the case-id list, so the leak handed the SUT the answer
key. Measured: a census with **no grading logic at all** that parses the case id
out of `MORI_SHOKUNIN_ROOT` and prints the canned row scores
`matched=27 total=27`, exit **0** against the frozen oracle. I reproduced this
independently (`sniffer-v1`, sha `5ead56f2…`, `matched=27 total=27` exit 0); it is
also the round-3 falsifier mutant m4b, re-measured by the lessons seat
(`corpus/lessons/2026-10-15-forgeable-oracle-visible-fixtures.md`) and by the
receipts-writer (`…-sniffer-v2.log`). My run's own output shows the impossible
states passing:

```
PASS ledger-missing-not-silent (state=not-open|unavailable via lane finding=0 rc=0)
PASS report-future-no-close (state=progressing-weak|silent via lane finding=0 rc=0)
```

— a case satisfied by a string that is not a member of the state vocabulary.

### 2.2 What closed them (r4 `be0e28b8…`)

1. **Opaque per-case trees.** `CASE_DIR=$(mktemp -d "$WORK/case.XXXXXXXX")`
   (`:187`); the shape case uses `shape.XXXXXXXX` (`:720-721`). No path handed to
   the census encodes which case is running. The fixture body was factored into
   `case_skeleton()` (`:151`) so the same bytes can be built twice under two names.
2. **No fixture marker.** `MORI_FIXTURE` is gone from the census export list
   (`:279-283`); `grep -n MORI_FIXTURE tools/mori-silence-cases.sh` → no hits. (The
   census still *uses* `MORI_FIXTURE` for its **own** selftest fixtures at `:377`,
   `:952-953`, `:1055`; that is the census's internal harness, not a signal the
   oracle exports.)
3. **Shape invariance as a case.** Case 28 (`:690-742`) builds identical fixture
   bytes under two random directory names and requires identical grade *and*
   identical stdout after each tree name is normalized to `<case-tree>`.

A channel probe (`/tmp/mori-vnw-r4/probe-channels.sh`, run as the census under the
r4 oracle) dumped every environment value and path token for all **29** census
invocations (27 cases + the two shape runs): `MORI_FIXTURE=<unset>` in every run,
and every case path token random (`case.XXXXXXXX` / `shape.XXXXXXXX`). No
case-identifying token survives.

### 2.3 Measured after-state of the attacks

| attacker | vs frozen oracle | vs r4 oracle | evidence |
|---|---|---|---|
| case-id sniffer (round-3 m4b, verbatim) | `matched=27 total=27` exit 0 | `matched=1 total=28` exit 1 | `…-sniffer-v2.log`; my `sniffer-v1` gives `7/28` exit 1 (it keeps a default branch the verbatim mutant lacks) |
| m4c (same attack, single states) | 27/27 exit 0 | `matched=1 total=28` exit 1 | `…-sniffer-v2.log` |
| order-replay counter v2b (deliberately answers `silent` at position 29) | n/a (post-fix attack) | `matched=27 total=28` exit 1; the **single** FAIL is `shape-invariance` | `…-sniffer-v2.log`; reproduced by me verbatim → `matched=27 total=28`, FAIL `shape-invariance` |

The receipt's scope line reads "the strongest no-logic adaptation (order replay) is
caught by shape-invariance alone". **That holds only for the variant tested.** See
the residual below.

### 2.4 Residual named by this seat: order replay that agrees with itself passes

The oracle runs the cases in a fixed source order, and a census can count its own
invocations in state outside the fingerprinted fixture tree (`readonly-no-mutation`
hashes `CASE_DIR` only, oracle `:419-422`). An attacker that answers from a positional
table — and, unlike v2b, gives the **same** answer to both shape runs — is not
caught:

```
/tmp/mori-vnw-r4/sniffer-v2-runorder.sh   sha256 29cb09ce5a63d38f6fc7bc5653b05f69cb1e294108a866d633f93611355e4e67
  counter at $WORK/.c ; positions 1..27 = the r3 want table ; default `progressing` for 28 and 29
$ bash oracle-r4.sh sniffer-v2-runorder.sh
PASS readonly-no-mutation
PASS shape-invariance
MORI_SILENCE_CASES: matched=28 total=28
EXIT 0        (reproduced twice; identical tally both runs)
```

So the honest statement of the anti-sniff result is:

- **claimed and verified** — the *case-id* channel is closed (27/27 → 1/28 for the
  verbatim round-3 mutant), `MORI_FIXTURE` is no longer exported, and no path
  handed to the census names the case;
- **not claimed** — that no sniffer can fake a pass. An invocation-order replay
  still reaches `28/28` exit 0. Shape-invariance catches it only if the attacker's
  positional table happens to disagree between positions 28 and 29, which is a
  one-line difference in the attacker's table.

Named unblock (not applied here): randomize the case order per invocation, and/or
interleave decoy fixture runs so that run position does not map to case identity.
The lessons note reaches the same conclusion from the other side — a forger keyed
on fixture *content* still passes shape invariance, so only randomized fixture
parameters make memorization cost approach real logic
(`corpus/lessons/2026-10-15-forgeable-oracle-visible-fixtures.md`, Limits).

## 3. The `:227` fix: an unreadable `.ufo/state` no longer kills the census

**Before** (r2 census `fe22a14f…`): `state_n=$(find "$STATE_DIR" -maxdepth 1 -type f
-name '*.round' 2>/dev/null | wc -l | tr -d ' ')`. Under `set -euo pipefail`
(`tools/mori-census.sh:54`) an unreadable `.ufo/state` makes the producer fail,
`pipefail` propagates it, and the assignment aborts the whole gate **before any
verdict line** — the crash signature documented in
`corpus/lessons/2026-10-15-errexit-pipefail-silent-crash.md` (canary B). The rc is
`1`, which is also this gate's DRIFT code, so a rc-only consumer reads a false
DRIFT and a verdict-line consumer reads nothing.

**After** (r4 `af2d4e79…`, `:233-241`, `:256-260`): the walk is `cap find` with an
rc branch, exactly the pattern the wave-age read already used (`:315-321`). A
failed walk sets `state_read=unreadable`, renders `state_rounds=unavailable
state_unreadable=1` in the surface detail, and the run continues to a full verdict.
A missing or empty directory cannot fail the walk, so it keeps the provable
`state_rounds=<n>` — the readable row bytes are unchanged from r2.

Differential canary, one fixture tree, `.ufo/state` `chmod 000`, identical env
(`/tmp/mori-vnw-r4/canary227.sh`, sha `983796a9…`):

```
census fe22a14f…  MODE=state000  RC=1  stdout_lines=1  verdicts=0  stderr_bytes=0
                  LAST_STDOUT_LINE: mori-census census-r2 — ts=2023-11-14T22:13:20Z — mode=live — read-only
census af2d4e79…  MODE=state000  RC=0  stdout_lines=10 verdicts=1  stderr_bytes=0
                  SURFACE watchdog: ok (… state_rounds=unavailable state_unreadable=1; ts=…)
                  LAST_STDOUT_LINE: MORI_CENSUS: CLEAN (findings=0 drift=0 unavailable=1 surfaces=7)
census af2d4e79…  MODE=control   RC=0  stdout_lines=10 verdicts=1
                  SURFACE watchdog: ok (… state_rounds=1; ts=…)
```

The receipts-writer measured the same shape independently
(`corpus/evidence/verdict-r4-20261015T173551Z-canary227.log`: BEFORE rc 1 / 0
verdicts / 1 line; AFTER rc 0 / 1 verdict / 10 lines, same disclosure field,
`CANARY_OUTPUT_SHA256 3f5868fa…`). The `unavailable=1` in both after-rows is the
fixture's own shape (no lane repo under the canary root), not a crash artifact —
the control row carries it too.

## 4. Per-round close tracking: a later close for another round no longer erases the anchor's close

**Before** (`fe22a14f…:611-616`, `:624`): the ledger pass kept only the **last**
close line anywhere — `close_ln=$n; close_round=$round` — and closed the anchor
only if `close_round = LA_ROUND`. Any later close for a *different* round
overwrote `close_round`, so the anchor's own close was forgotten and the mission
was graded as still open.

**After** (`af2d4e79…:601`, `:640`, `:653-661`): closes are accumulated as
`"<line> <round>"` pairs (`close_pairs`), and the anchor is closed iff **some**
close line has `cl > LA_LINE` and `cr = LA_ROUND`. Closes for other rounds are
irrelevant whether they sit before or after the anchor. (For a given round the
last such close is also the latest, so "any" and "the last one" agree.)

Differential canary (`/tmp/mori-vnw-r4/canary-close.sh`, sha `ee225519…`), ledger
`launch kagi round=7` (old) then `complete kagi round=7`, with an optional later
`complete kagi round=5`:

```
census fe22a14f…  MODE=clean      RC=0  SURFACE lane.kagi: not-open (… basis=row-4 reason=ledger-close round=7)
census fe22a14f…  MODE=lastother  RC=1  SURFACE lane.kagi: silent (… basis=row-D …)
                                        FINDING LANE_SILENT … DRIFT (findings=1 drift=1 …)   <- misgrade
census af2d4e79…  MODE=clean      RC=0  SURFACE lane.kagi: not-open (… basis=row-4 reason=ledger-close round=7)
census af2d4e79…  MODE=lastother  RC=0  SURFACE lane.kagi: not-open (… basis=row-4 reason=ledger-close round=7)
```

The `lastother` row is the critic defect 1 shape: a closed r7 anchor graded
`silent` with a false `LANE_SILENT` finding and a DRIFT exit. Both r4 rows are now
byte-identical, and `clean` is unchanged from r2 — the fix adds no new closure.

## 5. New selftest inventory

`bash tools/mori-census.sh --selftest` at `af2d4e79…`:
`MORI_CENSUS_SELFTEST: PASS (30 cases, 30 passed, 0 failed)`, exit **0**
(round 3: 25 cases; receipt `…-selftest.log`, `f890989c…`). Five new cases:

| line | case |
|---|---|
| `:1163` | `watchdog: unreadable state dir -> unavailable-disclosed, no crash` — asserts `^SURFACE watchdog: ok`, `state_rounds=unavailable`, `state_unreadable=1`, `^MORI_CENSUS: CLEAN ` |
| `:1171` | `watchdog: missing state dir -> provable 0, no crash` — asserts `state_rounds=0` |
| `:1177` | `watchdog: empty state dir -> provable 0, no crash` — asserts `state_rounds=0` |
| `:1350` | `silence: close r7 then close r5 -> r7 anchor stays closed` — asserts `^SURFACE lane\.kagi: not-open `, `basis=row-4`, `reason=ledger-close round=7` |
| `:1361` | `silence: close for another round does not close the anchor` — the complementary guard: `silent` + `FINDING LANE_SILENT` + DRIFT |

The three watchdog cases pin the `:227` contract at both ends (unreadable →
disclosed, missing/empty → provable zero). The two silence cases pin close
tracking in both directions (the anchor round's close survives a later other-round
close; another round's close never closes the anchor).

Oracle side: one new case, `shape-invariance` (`tools/mori-silence-cases.sh:690-742`,
`:728-735` for its four failure branches). It fails the run if either side crashed
mid-run, if the two grades differ, or if the two stdouts differ after normalizing
the tree name — i.e. it catches both a grade that depends on the directory name and
output that leaks it.

## 6. Final pinned tally and receipts

| probe | before | after | receipt / measurement |
|---|---|---|---|
| `bash tools/mori-silence-cases.sh` | `matched=25 total=27` exit 1 (frozen `505a7504…` / census `fe22a14f…`) | **`matched=28 total=28` exit 0** | `…-oracle.log` (`67a91103…`); this seat's independent run, case-line identical |
| counterfactual matcher witness | `matched=27 total=27` exit 0 | n/a (defect fixed) | `…-oracle-counterfactual.log`; witness sha `ae95b601…` re-derived byte-identical |
| `bash tools/mori-census.sh --selftest` | `PASS (25 cases, 25 passed, 0 failed)` exit 0 | **`PASS (30 cases, 30 passed, 0 failed)` exit 0** | `…-selftest.log` (`f890989c…`) |
| case-id sniffer (m4b verbatim) | `matched=27 total=27` exit 0 (this seat's `sniffer-v1` `5ead56f2…` vs the frozen oracle) | `matched=1 total=28` exit 1 | `…-sniffer-v2.log` (`ab7b41ae…`) |
| `:227` canary, `.ufo/state` `chmod 000` | rc 1, 0 verdicts, header only | rc 0, 1 verdict, disclosure row | `…-canary227.log` (`3377c224…`); this seat's canary agrees |
| close canary `complete r7; complete r5` | `silent` + `LANE_SILENT` DRIFT rc 1 | `not-open (basis=row-4)` rc 0 | this seat's `canary-close.sh`; pinned selftest case `:1350` |
| live census | r3: `DRIFT (findings=14 …)` (`corpus/evidence/cutover-r3-20261015T165712Z-live.log`) | **`MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)` exit 1** | `corpus/evidence/verdict-r4-20261015T173551Z-live.log` (`92808191…`); this seat's two spots at 17:38:49Z / 17:39:18Z agree |

Live detail (mutable spot, not a baseline): all 9 roster lanes `progressing`
(8 × `basis=row-A`; aggregator `row-B rowb_files=2 attribution=inference`),
`SURFACE silence: ok (… silent=0 progressing=9 progressing_weak=0 young=0 not_open=0
unavailable=0 skipped=0 window_s=7200 …)`, **zero** `LANE_SILENT` findings, the one
`unavailable` surface being tmux (`tmux ls` rc 1). Two spots 29 s apart produced
identical finding-id sets. The census file sha was verified unchanged before and
after every run.

## 7. Regression, limits, carried

- **Regression: none measured.** All 25 probes that passed at the frozen oracle pass
  at the r4 oracle, and the two flipped cases are the intended ones. Because the
  `assert_case` want-strings and the case ids are byte-identical between the two
  revisions (§1), the flip is attributable to the matcher alone.
- **Residual, this seat:** the order-replay sniffer in §2.4 reaches `28/28` exit 0.
  The registered claim ("a sniffer-v2 attempt cannot fake a pass") is true for the
  case-id attack class and false in general.
- **Carried, unchanged:** the frozen-behavioral drift pin is still absent; row 6
  (committed report) still checks presence + commit window only, so a fresh
  contentless committed marker closes a mission; the row-6 presence-only residual
  and the receipt-binding / role-routing debts from the blocked round-2 attempt are
  untouched by this move.
- **Not claimed:** any admission or axis verdict (parent), any scalar score, any
  remediation. Live figures are a pinned clock, not a baseline. If either tool
  changes from the hashes at the top of this note, re-measure everything here.
- **Scratch (re-run material, `/tmp` only):** `oracle-baseline.sh` `505a7504…`,
  `census-baseline.sh` `fe22a14f…`, `oracle-r4.sh` `be0e28b8…`, `census-r4.sh`
  `af2d4e79…`, `oracle-cf.sh` `ae95b601…`, `sniffer-v1.sh` `5ead56f2…`,
  `sniffer-v2-runorder.sh` `29cb09ce…`, `sniffer-v2b-receipt.sh` `122045ff…`,
  `canary227.sh` `983796a9…`, `canary-close.sh` `ee225519…`, all under
  `/tmp/mori-vnw-r4/`.
