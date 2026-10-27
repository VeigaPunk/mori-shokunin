# Mo56CritC1Claim — falsification review of the C1 driver-liveness claim

seat: Mo56CritC1Claim (leaf critic, mori round 56 w1) · lane mori-shokunin · 2026-10-27
scope: attack the C1 claim only — (a) novelty of the FR5 ground, (b) do-nothing
control vs `count-c1.py`, (c) axis label coverage vs operability, (d) overlap
with `inline.sh:193`. No vote items in this wave; no counter/proposal edits.

Verdict: **claim stands**, with two named limits (novelty attribution narrowed;
axis attribution not counter-verifiable). Neither limit kills C1 under its
frozen predicate; both are routed items for round 57.

## (a) Is the FR5 launch/complete ground genuinely new?

Commands and evidence:

```
grep -n "FR5" corpus/README.md        # row at :345
sed -n '1978,2140p' tools/mori-census.sh   # r2 silence surface grammar
head -30 corpus/knowledge/silence-grading-r2.md
grep -n "watchdog" tools/mori-census.sh    # WATCHDOG_STALE arm, lines 725-737
```

What I found:

1. `corpus/README.md:345` (FR5) says reading the driver's `launch`/`complete`
   lines in `.ufo/watchdog.log` as a second liveness source "is open coverage
   ground", citing `lessons/round-33.md` Round-32 repair §6. That §6 retired
   the pid-based `WATCHDOG_ABSENT` probe and named the log reading as coverage
   ground "now named in FR5's boundary".
2. **But the census already reads the same lines, second-party, since round 2.**
   `tools/mori-census.sh` `probe_silence`/`grade_lane` (header comment
   "surface: lane silence ... Authority: PROTOCOL.md:153-168", contract
   `corpus/knowledge/silence-grading-r2.md`, written 2026-10-15) parses
   `launch <lane> round=N <tail>` (pid=/runId=/mission=/absent), legacy `steer`,
   and `complete|wrap` closes from the same `.ufo/watchdog.log`, grades each
   lane silent/progressing/young/not-open/unavailable, and emits per-lane
   `SURFACE lane.<lane>:` lines plus `LANE_SILENT` findings. That is a per-lane
   liveness reading over the same log, predating the FR5 boundary naming.
3. The census watchdog surface also already treats the log as a driver-liveness
   signal: `WATCHDOG_STALE` fires on log mtime age (lines 725-737), and the
   round-33 §6 retirement note records `WATCHDOG_ABSENT` firing every round
   under the inline driver.
4. What the probe adds over the census grammar (`mori-census.sh:1994-1998`):
   `lane-dead-no-report` / `launch-fail` / `wrap` as counted first-class events
   (the census only excludes launch-fail as an anchor), malformed-line
   accounting with capped examples, `other_lines` classification for ts-first
   driver prose, `unclosed`/`in_flight` pairing facts with **no git
   correlation**, `*.round` state-entry *shape* census, and a standalone
   fleet-wide JSON report that runs when git is unavailable (the census grades
   `unavailable` on git rc!=0). The census ignores tails, takes LAST-line-wins,
   and never reports log-shape counts.

Assessment: the strict surface named in the contract — "reported as per-lane
log-shape facts only" — is genuinely new. The FR5 parenthetical ("FR5's
round-33 named open ground") overstates: the broad reading it cites (launch/
complete lines as a second liveness source) was partially worked by the r2
census silence surface and the log-freshness arm. The claim's own boundary
sentence is the defensible novelty; the map citation inflates it. Claim
stands on the narrowed surface; novelty attribution should be narrowed at
closure.

## (b) Could a do-nothing control meet `count-c1.py`?

Read of the counter (`.ufo/waves/round-56/count-c1.py`): hard gate on
`git_show(rev, "tools/mori-driver-liveness.py")` then frozen
`PIN = 6b3dba74...`; selftest arm materializes the tool and requires
`DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0` and rc 0; fixture arm
materializes the 9 frozen fixtures and re-runs the tool per fixture requiring
JSON `verdict == DRIVER_LIVENESS_OK` and the frozen malformed count; entry,
S544 row and a health-word scan (tool text before `# selftest`) complete it.

Experiments (scratch repo under /fast/scratch, removed after; TMPDIR set):

```
# 1. real entering tip (tool absent)
python3 .ufo/waves/round-56/count-c1.py 5b295eeebd87ebd610d8d39bfe2035742f740cfa
C1=unmet selftest=bad fixtures=bad entry=bad row=bad norem=bad failed=tool_absent rev=5b295eee...
rc=1

# 2. scratch repo: entry + S544 row + vacuous tool (prints selftest line only)
python3 .ufo/waves/round-56/count-c1.py <scratch-rev> --repo <scratch>
C1=unmet selftest=ok fixtures=bad entry=ok row=ok norem=ok failed=pins,fixtures
rc=1
```

An entry-only control fails at `tool_absent` (also the committed control
receipt `evidence/controls.txt` line 1, `do-nothing-c1 PASS ... failed=tool_absent`).
A vacuous tool passes only the selftest/entry/row/norem arms: the frozen sha
pin blocks substitution (`pins`) and the counter's own re-runs over the frozen
fixtures reject non-JSON output (`fixtures`). The pin is the load-bearing
control; layered with the fixture re-runs, a do-nothing control cannot meet
the counter.

Residual (named limit, not a kill): the fixture arm checks only `verdict` and
`log.malformed` — not the other reported counts — and the selftest arm trusts
the tool's own printed line. Both are closed in practice by the pin plus the
pinned, human-visible 13-case selftest text, but the counter would not catch a
pinned tool whose selftest cases were vacuous. Claim's control story stands.

## (c) Is "coverage" the right axis label?

The predicate is operability-shaped: tool present at a pinned sha, selftest
line, fixtures parse with frozen counts, entry names S544 + tool, registry row
mined with used-by, no health-verdict string. That is the same predicate
*shape* as C2's capability counter (pin/selftest/behaviour/entry/row). Nothing
in `count-c1.py` verifies coverage-specific content — that the surface names
map open ground, or that the ground was unworked. The "coverage" attribution
rests entirely on the contract's FR5 citation, which (a) shows is partially
overstated. The contract also records "coverage is the lowest owned axis",
so the label carries scoring weight the counter cannot itself support.
Named limit: an axis-attribution check (surface names map rows whose novelty
is counter- or closure-verified) or an explicit operability/coverage split
belongs in round 57 routing; per the freeze rules I do not propose changing
this round's counter.

## (d) Does the probe duplicate `inline.sh:193`?

```
sed -n '185,200p' scripts/hyaku/inline.sh
193:  DISPATCH_LINES=$(grep -E "^[^ ]+ (launch|complete|lane-dead-no-report) $lane round=$n( |;|$)" "$UFO/watchdog.log" | tail -10)
```

Line 193 is inside the `closure)` arm: it greps three of the five verbs for
**one lane and one round**, keeps the last 10 lines, and substitutes the
result into the closure prompt template (`{{DISPATCH_LINES}}`, used at
`inline.sh:100`). It is a first-party render helper: no counts, no malformed
accounting, no unclosed detection, no other lanes, no launch-fail/wrap verbs,
no state shapes, no report. The probe reads the same log fleet-wide, parses
all five verbs plus malformed/other-line accounting, and emits per-lane
log-shape JSON. Shared grammar ancestry (both derive from the writers at
`inline.sh:149,176,182` and `shokunin-watchdog.sh:241-249,266,398,405,448`,
extracted in S544) is not duplication of function. No regression: the probe
subsumes the grep's grammar; the closure render does not depend on the probe.

## Verification of the landed claim (independent re-run)

```
sha256sum tools/mori-driver-liveness.py
6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997   # == PIN

python3 .ufo/waves/round-56/count-c1.py 8be2717b0809281d07dffe83dad424a4859e0747
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=8be2717b...
rc=0

python3 tools/mori-driver-liveness.py --fixture .ufo/waves/round-56/fixtures/driver/malformed
verdict DRIVER_LIVENESS_OK, log.malformed=5 (matches frozen expectation)

python3 tools/mori-driver-liveness.py        # live fleet log, read-only
verdict=DRIVER_LIVENESS_OK lines=1730 malformed=0 other_lines=121 lanes=23
totals: launches=843 completes=571 deads=166 launch_fails=7 wraps=22 unclosed=124
```

The live counts grow over the committed receipt (`driver-liveness-live.txt`,
1728 lines) by exactly the two lines the driver appended since — consistent
with the entry's "reproduces it modulo ages". Commit order confirmed:
`5b295eee` (entering) → `c419fe6d` (data) → `6ced9da9` (norem docstring
correction) → `3f494b49` (freeze) → `8be2717b` (controls+receipts); the
counter's norem arm demonstrably bites, having caught the tool's own docstring
before freeze (commit 6ced9da9). 13 selftest cases and 9 frozen fixtures
confirmed by inspection (`grep -c "def t_"` → 13; `ls fixtures/driver` → 9).

## Findings

- **MED — novelty attribution overstated** (corpus/README.md:345 FR5 cell;
  .ufo/waves/round-56/contract.md C1 surface sentence). The r2 census silence
  surface (mori-census.sh probe_silence/grade_lane, silence-grading-r2.md) and
  the watchdog log-freshness arm already read launch/complete lines from the
  same log as liveness input. The probe's strict surface (per-lane log-shape
  facts: malformed accounting, dead/fail/wrap counts, unclosed/in_flight
  without git, state shapes) is new; the FR5 "open ground" citation is not.
  Route to round 57: narrow the FR5 boundary cell or add a closure-verified
  novelty check. Claim stands.
- **MED — axis label not counter-verifiable** (.ufo/waves/round-56/count-c1.py
  predicate shape). The predicate is operability-shaped; "coverage" rests on
  the FR5 citation alone and carries scoring weight ("coverage is the lowest
  owned axis"). Route to round 57 as an axis-attribution item; do not change
  the frozen counter this round.
- **LOW — frozen counter stricter than its own predicate sentence**
  (count-c1.py HEALTHT_WORDS tuple vs docstring). The docstring names three
  health words; the tuple carries five ("is stuck", "wedged" added). Stricter
  is safe; the mismatch is cosmetic in the frozen text.
- **LOW — norem scan scope** (count-c1.py `tool_src.split("# selftest", 1)[0]`
  vs tools/mori-driver-liveness.py:248). Only the tool text before the
  `# selftest` marker is scanned for health words; the selftest section is
  exempt. The frozen tool's selftest section carries none, so no live exposure.
- **LOW — fixture-arm under-check** (count-c1.py fixture loop). Only `verdict`
  and `log.malformed` are re-verified per fixture; the other reported counts
  are not. Closed in practice by the frozen pin plus the pinned 13-case
  selftest text; recorded as discrimination context for the closure.
- **INFO — do-nothing controls empirically blocked** (evidence/controls.txt:1
  and scratch re-runs above). Entry-only fails `tool_absent`; entry+vacuous
  tool fails `pins,fixtures`. C1's before/after contrast is real.
