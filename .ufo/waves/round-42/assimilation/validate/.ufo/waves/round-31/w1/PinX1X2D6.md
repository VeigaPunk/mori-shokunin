# MoriR31.PinX1X2D6 — routed D6: freeze the round-30 X1/X2 dry-run verdict flips

Seat: MoriR31.PinX1X2D6 (executor, leaf). Item attacked: routed defect D6.
Input: the round-30 critic report
`.ufo/waves/round-30/w2/CriticHarmAxes.md` (axis 2: "Counterexample (unpinned
shapes)" and "Reachability" bullets).

Sandbox: `/fast/scratch/hyaku/mori-r31/PinX1X2D6/`. Tool copies under `/tmp`
extracted with read-only `git show` from the lane repo (no repo writes, no
fixture edits). Tools installed or updated: none (system `python3` and
read-only git only). Lane writes: this report only, plus the scratch case file
below.

## Deliverable

New case file, not a fixture edit:
`/fast/scratch/hyaku/mori-r31/PinX1X2D6/cases-r31-dryrun-flips.json`
(sha256 `b0446f522cefea52b47a519a2073bb727a1bba79c4e7824474027c6ef13a3d09`).

- Schema: copied from `tools/fixtures/mori-oom-killers/cases-a2.json` (top-level
  `schema` `frozen_with` `note` `cases`; per-case `id` `rule` `why` `inputs`
  `expect`; `expect.verdict`/`expect.exit`/`expect.fields` dotted paths only).
  Two cases, each additionally carrying a per-case `note` as assigned. The
  selftest reader compares only verdict, exit and the dotted paths present in
  `expect.fields` (`tools/mori-oom-killers.py@a12c68ae:739-766`).
- Both cases are the `a2-06-inactive-earlier-invocation-sends-acted` template
  (inactive unit, retained `ActiveEnterTimestampMonotonic=1000`; template at
  `tools/fixtures/mori-oom-killers/cases-a2.json:676-728`), with the round-30
  X1 and X2 inputs substituted:
  - `r31-x1-stopped-dryrun-escalation-acted`: version line, `dryrun mode
    enabled`, one SIGTERM send, one `escalating to SIGKILL after 10s` — all
    after the stamp.
  - `r31-x2-stopped-prestamp-dryrun-send-acted`: version and `dryrun mode
    enabled` before the stamp, one SIGTERM send after it.
- Each `note` names the round-30 CriticHarmAxes axis-2 finding (base
  `58b61681` KILLERS_QUIET -> tip KILLER_ACTED) and states the shape is not
  producible by stock earlyoom 1.9.0, with the report's reasons:
  - X1: in dry-run mode `kill_wait` returns at `kill.c:271-273` before the
    escalation message at `kill.c:318`, so no dry-run invocation emits both
    `dryrun mode enabled` and `escalating to SIGKILL after`.
  - X2: `earlyoom.service.in` sets no `Type=`, so [INFERENCE] the unit is
    `Type=simple` and each invocation's active-enter stamp precedes its first
    log line; a stopped unit's last invocation therefore always opens with a
    post-stamp version line, and the pinned pre-stamp-dryrun/post-stamp-send
    shape cannot arise from a real 1.9.0 boot. Completed with the post-stamp
    version line, the shape reads KILLER_ACTED at both revisions, so the flip
    is unreachable.

## Runs (both verbatim, exit codes recorded)

Tool copies: `git -C <lane> show a12c68ae:tools/mori-oom-killers.py >
/tmp/mori-oom-killers-tip.py`; `git -C <lane> show 58b61681:tools/mori-oom-killers.py
>/tmp/mori-oom-killers-base.py`. Both blobs exist at those revisions
(`git cat-file -e` passed); revisions resolve to
`58b61681a0e3f3b821a17d38a4e713ccd9921615` and
`a12c68ae81257fb6f918bb165bcb39c73f82d212`. sha256 of the copies:
tip `9c88ef272dbe3e07eb87e40f10faaedb82584df0d9f21e78e3d8764400da0fe1`,
base `41464957540fbe3f0855d0a23df4437d0c850a256a4d15f9e76f0b4057e749d7`.

Tip (round-31 entering tip `a12c68ae`):

```
$ timeout 120 python3 -I -B /tmp/mori-oom-killers-tip.py --selftest --cases /fast/scratch/hyaku/mori-r31/PinX1X2D6/cases-r31-dryrun-flips.json
MORI_OOM_KILLERS_SELFTEST: PASS 2/2
TIP_EXIT=0
```

Result: PASS 2/2, exit code 0.

Base (`58b61681`):

```
$ timeout 120 python3 -I -B /tmp/mori-oom-killers-base.py --selftest --cases /fast/scratch/hyaku/mori-r31/PinX1X2D6/cases-r31-dryrun-flips.json
MORI_OOM_KILLERS_SELFTEST: FAIL 0/2
FAIL r31-x1-stopped-dryrun-escalation-acted: verdict: got 'KILLERS_QUIET' expected 'KILLER_ACTED'
FAIL r31-x1-stopped-dryrun-escalation-acted: exit: got 0 expected 1
FAIL r31-x1-stopped-dryrun-escalation-acted: earlyoom.dryrun_send_lines: got null expected 1
FAIL r31-x2-stopped-prestamp-dryrun-send-acted: verdict: got 'KILLERS_QUIET' expected 'KILLER_ACTED'
FAIL r31-x2-stopped-prestamp-dryrun-send-acted: exit: got 0 expected 1
FAIL r31-x2-stopped-prestamp-dryrun-send-acted: earlyoom.dryrun_send_lines: got null expected 0
BASE_EXIT=1
```

Result: FAIL 0/2, exit code 1; both cases read KILLERS_QUIET at base and
KILLER_ACTED at tip — exactly the round-30 X1/X2 flip, now frozen.

## Mechanism (why the flip exists)

- At base `58b61681`, scoping happens only for active units
  (`tools/mori-oom-killers.py@58b61681:278-315`), so every line of a stopped
  unit goes to the earlier-line path; a dry-run segment there drops sends and
  escalations (`:333-352`), and the non-active `acted` branch uses only
  `earlier_send_lines` (`:465-469`). X1/X2 read QUIET.
- At tip `a12c68ae`, a retained nonzero stamp on a non-active unit still scopes
  post-stamp lines to the last invocation (`tools/mori-oom-killers.py@a12c68ae:304-321`);
  in that scoped path escalations count outside the per-segment dry-run split
  (`:409-410`), and a send after the stamp counts because the pre-stamp
  dry-run segment is lost (`:389-426`, `:471-483`). X1 reads ACTED via the
  escalation, X2 via the post-stamp send.

## Files changed

1. `/fast/scratch/hyaku/mori-r31/PinX1X2D6/cases-r31-dryrun-flips.json` (new).
2. `.ufo/waves/round-31/w1/PinX1X2D6.md` (this report, new).

No existing fixture, tool, lane or fleet file was edited; no git/jj writes
ran.

## Risks / blockers

- None. The two cases pass at the entering tip and fail at base with the
  predicted verdict flip; the run evidence above is complete.
- One labeled inference: the `Type=simple` reachability argument for X2 is
  copied from the round-30 report and is marked [INFERENCE] in the case note;
  the reachability claim itself is the round-30 finding being frozen, not new
  analysis.
