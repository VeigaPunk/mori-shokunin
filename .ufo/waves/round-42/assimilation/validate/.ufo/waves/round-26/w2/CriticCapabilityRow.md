# Round 26 wave 2 — CriticCapabilityRow (critic, leaf)

Seat `MoriR26.CriticCapabilityRow`, 2026-10-22. Target: the round-26 capability row, `SCORECARD.md:1620` at
`16935e24c93fa7e7567413d7ec091339a5df1474`, and the C2 width behind it. All lane bytes were read with
`git show` / `git archive 16935e24` into `/fast/scratch/hyaku/mori-r26/CriticCapabilityRow/tree/`, never from the
working tree. Tools installed or upgraded: none (python3, jq, git, journalctl, systemctl and sudo were already present).
`skill://godspeed` did not resolve on this host. A file search found only `~/.omp/agent/hooks/pre/godspeed-always-on.js`,
which loads the skill and does not contain it. Lane writes: this file only.

## Verdict

**Defect (medium): the row is wider than the counted 32/32 and wider than its listed limits.**
- The row's "What it can now do" bundles behaviour from after the freeze (amendment A2) with the counted behaviour.
  It then cites `PASS 32/32` as the evidence for all of it.
- No committed case pins any field that A2 added, and no committed case exercises any rule that A2 adopted (F1).
- Three input shapes reproduce on the tip tool that the row does not disclose:
  - Y1: a stopped earlyoom that sent a real signal this boot reads `KILLERS_QUIET`, exit 0.
  - Y2: a running earlyoom reports earlier-invocation sends as 0 when it actually has some.
  - Y3: a stopped earlyoom whose journal read failed reads `KILLERS_QUIET`, exit 0.
  (F2, F3.)
- Four limits are missing even though wave 1 named them: S3, S4 and S5 from ReviewScopeClock, and the end-of-journal
  rate-limit residual from CriticC2Width (F5).
- The four limits the row does list are accurate (F4).

## What holds (checked)

- **H1 — counted value.** `evidence/c2-selftest.txt` records revision `4dba9cc7`, `tool_blob: 44dac3fd…`,
  `cases_blob: 5b4dcee7…`, `PASS 32/32`.
  - `git rev-parse` gives the same tool blob at `327fbcca`, `4dba9cc7` and `16935e24` (`44dac3fd6cb1…`).
  - It gives the same cases blob at `5b10649d` and `16935e24` (`5b4dcee7b682…`).
  - `git log` on the tool and fixtures shows that the last tool change, `738eec1`, comes before `327fbcc`.
  - Result: the row's `PASS 32/32 (frozen at 5b10649d)` matches the tip bytes. **Holds.**
- **H2 — live receipt.** `evidence/c2-live-run.txt:1-5` records revision `4dba9cc7`, the same tool blob, exit 0.
  - Its output (`:6-36`): `KILLERS_QUIET`, earlyoom `active`, `verified-1.9.0`, thresholds 10/10/5/5, all counts 0,
    `earlier_invocation_send_lines: 0`, oomd `inactive` with 0 notices.
  - The row's unit-state, version and threshold reading is shown live. **Holds**, but only for the quiet path on one
    host; see the wording correction.
- **H3 — wave-1 X shapes fixed by A2.** These now behave as the row says, by the tool code at the tip and A2
  (`contract.md:156-169`):
  - X1 dry-run sends: `tools/mori-oom-killers.py:370-374`.
  - X2 process-group lines: `:362-363`.
  - X3 suppression: `:364-365`, `:378`.
  - X5 and X6 non-steady states: `:209-212`.
  - My Y5 (dry-run plus `-g` in the current invocation) printed `KILLERS_QUIET` with `dryrun_send_lines=1` and
    `process_group_lines=1`.
- **H4 — X9 in live mode.** `sudo -n -u nobody python3 -I -B <tip tool copy>` printed `KILLERS_UNKNOWN`,
  `actions: null`, `notices_this_boot: null`, exit 2. The A1c probe (`:545-549`) holds for a user that cannot read
  the system journal. **Holds.** This run is not committed.
- **H5 — S1 (a restart in the same boot).** My Y9 (active, one real send in an earlier invocation) printed
  `KILLERS_QUIET` with `earlier_invocation_send_lines=1`. The row's first limit is accurate. Frozen `c02` pins this
  verdict (`cases.json` c02 `expect`), so it is a **tradeoff the judge must weigh**, not a fixable defect.
- **H6 — S2 (a stop without a restart).** Fixed for the plain shape: `:422` makes a non-zero
  `earlier_invocation_send_lines` positive evidence for an earlyoom that is not active. Y7 (stopped, unverified
  version, one send) printed `KILLER_ACTED`, exit 1. See F2 and F3 for the shapes where it still fails.

## Findings

**F1 — the row's evidence does not cover its A2 clauses. Defect (medium; calibration, coverage).**
- Attacks: `SCORECARD.md:1620`, the clauses "process-group and dry-run send log lines" and "send lines of earlier
  invocations this boot", and the evidence column.
- Evidence: `jq -r '[.cases[].expect.fields|keys[]]|group_by(.)…'` over both case files lists 18 pinned keys in
  `cases.json` and 17 in `cases-supplementary.json`.
  - Neither file contains `earlyoom.dryrun_send_lines`, `earlyoom.process_group_lines` or
    `earlyoom.earlier_invocation_send_lines`.
  - A grep of both files finds no `Suppressed N messages`, no `ActiveState=` other than `active` or `inactive`, and no
    dry-run invocation that has a send line.
  - The only two `killing whole process group` lines are in supplementary `c21`, which pins no process-group field.
- Supplementary history: the file was added at `278f02e` and last changed at `21386b9`, which comes after the last
  tool change `738eec1`. That change was "c21 near misses" against the contract grammar (`git show 21386b9`).
- Consequence:
  - The frozen 32/32 cannot test A2: those cases were frozen before it.
  - The supplementary 32/32 does not test it either.
  - The A2 rules were shown only on wave-1 and wave-2 seats' invented inputs, which are not committed.
  - The lesson says the same (`corpus/lessons/round-26.md:26-30`, "Five were fixed in the tool after the freeze").
    The row does not.

**F2 — one dry-run invocation zeroes every earlier invocation's sends. Defect (medium; operability, calibration).**
- Attacks: the row clause "send lines of earlier invocations this boot", and the A2 claim at `contract.md:177-178`
  ("a stop without restart no longer reads quiet").
- Code: `tools/mori-oom-killers.py:312-313` sets `earlier_send_lines = 0` if *any* line outside the current scope is
  `dryrun mode enabled`. It treats all earlier invocations as a single dry-run invocation. Upstream sets the dry-run
  flag once per invocation (`main.c:294-296`; CriticC2Width `w1/CriticC2Width.md:151`).
- Reproduced with `python3 -I -B cx.py` in scratch (invented process names):
  - **Y1**: stopped earlyoom. Invocation A sent a real SIGTERM, then invocation B ran in dry-run.
    Output: `exit=0 KILLERS_QUIET … earlier_invocation_send_lines=0`. This is a false quiet with exit 0.
  - **Y2**: running earlyoom. Earlier invocation A was real with one send, earlier invocation B was dry-run.
    Output: `KILLERS_QUIET … earlier_invocation_send_lines=0`. The count is false: the true value is 1.
- Fixable inside the freeze. A scan of both case files found no case whose earlyoom is not active and that has a
  dry-run or a send line. The non-active cases are `c06`, `c07`, `c25`, `c27` and `c29`, each with 0 or 1 journal
  lines and no send line.
- Smallest correction: split the out-of-scope lines into invocations at each `earlyoom <version>` line, and drop only
  the sends of dry-run invocations. Otherwise, disclose the shape in the row (wording below).

**F3 — a stopped earlyoom with an unread journal reads quiet. Defect (low to medium; operability).**
- Attacks: the same A2 clause, and contract rule 2 ("a needed read is null", `contract.md:99`).
- Code: `:432` treats a null journal as unknown only when earlyoom is `active`. Since A2 (`:422`), the journal of a
  stopped earlyoom is evidence, so for that unit the journal is now a needed read.
- **Y3**: stopped earlyoom, `ActiveEnterTimestampMonotonic` > 0, `earlyoom_journal: null`.
  Output: `exit=0 KILLERS_QUIET`.
- Live reach [INFERENCE]: if the earlyoom journalctl call fails or hits the 30 s timeout (`:476-489`) while the oomd
  call succeeds, the output is a quiet exit 0 for a killer whose evidence went unread.
- Fixable inside the freeze. No case has an earlyoom that is not active with a `null` journal; `c06` and `c07` use
  `[]`, not null.

**F4 — the listed limits are correct but not complete. Holds as far as they go.**
- Wave-1 items the row covers, with their status at the tip:

| Wave-1 item | At the tip | In the row |
|---|---|---|
| X4 / S1, earlier invocation while running | reported, verdict unchanged (Y9) | yes, limit 1 |
| X8 / A1a, head-truncated count | count printed as exact | yes, "lower bounds" |
| X7 / A3, logger-heartbeat | not checked | yes |
| boot −1 history (ReviewScopeClock §13: 39 action lines) | not read | yes, "previous boots are not read" |
| S2, stopped unit | fixed for the plain shape; fails for Y1 and Y3 | not stated |

**F5 — wave-1 residuals missing from the row. Defect (low; calibration).**
- S5 (`w1/ReviewScopeClock.md:112`): an inactive or never-started earlyoom reads `KILLERS_QUIET`, exit 0.
  - Reproduced as **Y6** (inactive, bound 0, journal `[]`): `exit=0 KILLERS_QUIET`.
  - The entry discloses that quiet is not "zero kills" (`userspace-oom-killers-r26.md:242-243`). The row does not.
- S3 (`w1/ReviewScopeClock.md:110`): the two live reads are not atomic, so a restart between them mixes invocations.
  No false quiet has been traced. Not disclosed.
- S4 and CriticC2Width "other holes" (`w1/CriticC2Width.md:158-161`): the `-u` read keeps PID 1 records and lines
  from earlyoom's child processes (`-N`, `-P`, the dbus helper). `_collect_journal` (`:493-505`) has no `_COMM`
  filter. Not disclosed.
- End-of-journal rate-limit loss (`w1/CriticC2Width.md:162-163`): journald writes the suppression notice only with
  the unit's next accepted line, so loss after earlyoom's last line is invisible. A1b cannot close this. Not
  disclosed.
- **Y4** (stopped earlyoom with a suppression notice) printed `KILLERS_QUIET`: suppression is checked only inside the
  current scope (`:364-365`). **Y8** (`LoadState=not-found` with sends in the journal) printed `KILLERS_QUIET`, because
  `:308` skips an absent unit. Both are low severity. A brief disclosure is enough; a fix is optional and fits the
  freeze by the same scan as F2.

**F6 — next to this row, routed to CriticEntryOverclaim. Not judged here.**
- `userspace-oom-killers-r26.md:237-239` says the tool "implements exactly" the note's "eight-line grammar".
- The tip tool also classifies `killing whole process group` and `Suppressed … messages from earlyoom.service`
  (`:118-121`, `:362-365`).

## Smallest safe correction: exact row wording

Use this text if the L1 does not change the tool. It keeps every number the counter and the receipt show, and moves
the A2 behaviour out of what the count backs:

```markdown
| userspace OOM killer read (earlyoom 1.9.0, systemd-oomd), bounded | from `systemctl show` and this boot's journal, report each killer's unit state, the earlyoom version string and its four startup thresholds, counts of earlyoom send, escalation, failed-kill and low-memory log lines for the current invocation, and the number of systemd-oomd kill notices this boot, with a `KILLER_ACTED` / `KILLERS_UNKNOWN` / `KILLERS_QUIET` verdict as in contract C2; the 32 frozen cases test this part. Added after the freeze (amendment A2) and pinned by no committed case: journald-suppression and non-steady-state abstains, process-group and dry-run send line counts, and send lines of earlier invocations this boot. Counts are log lines, not processes killed. `KILLERS_QUIET` means no send line or notice in what the tool could read, not zero kills; an inactive or never-started earlyoom reads quiet with `actions: null`. Known limits: for a running earlyoom, sends of an earlier invocation in the same boot are reported but do not change the verdict; if any earlier invocation this boot ran in dry-run mode, earlier sends are reported as 0 and a stopped earlyoom reads quiet; a stopped earlyoom whose journal read failed reads quiet; counts with an incomplete scope are lower bounds; no logger-heartbeat check; journald rate-limit loss after earlyoom's last line is not seen; PID 1 and earlyoom child-process lines are not filtered; the unit and journal reads are not atomic; previous boots are not read | `tools/mori-oom-killers.py --selftest` PASS 32/32 over cases frozen at `5b10649d` (blob `5b4dcee7`) before the tool (`evidence/c2-selftest.txt`, `evidence/c2-count.txt`); PASS 32/32 on `cases-supplementary.json` (not counted; pins no A2 field); `.ufo/waves/round-26/evidence/c2-live-run.txt` (one run on this host, quiet path only); `corpus/knowledge/userspace-oom-killers-r26.md` | 26 |
```

If the L1 fixes F2 and F3 in the tool instead (both fit inside the freeze, per the scans above):
- Drop the two clauses "if any earlier invocation … reads quiet" and "a stopped earlyoom whose journal read failed
  reads quiet".
- The tool blob then changes, so `evidence/c2-selftest.txt`, `evidence/c2-count.txt` and `evidence/c2-live-run.txt`
  must be regenerated at the new tip. Otherwise the row cites receipts for a different blob.
- The A2 clause stays "pinned by no committed case" unless a case seat other than the tool seat adds supplementary
  cases for Y1 to Y4. Those cases would stay uncounted.

Words to keep out of the row, as before: "never", "no OOM kill", "kills N processes", "complete".

## Impacted axes

- coverage: the C2 capability statement is wider than its counter (F1).
- calibration: the row overclaims, which is the round-25 R2 pattern (F1, F5).
- operability: exit 0 on a false quiet (F2, F3), and that exit code is what callers branch on.

Fixable defects: F1 and F5 (wording); F2, F3, Y4 and Y8 (tool, inside the freeze).
Tradeoff for the judge: S1 under frozen `c02` (H5).

## Reproduction

Scratch: `/fast/scratch/hyaku/mori-r26/CriticCapabilityRow/`.
- Run `cx.py` against `tree/tools/mori-oom-killers.py`, the `git archive 16935e24` copy (sha256 `1a71b2df…`).
- It writes `in-Y*.json` and prints one line per shape.
- Inputs use only the process name `invented-proc` and upstream v1.9.0 message prefixes. No host journal text was
  copied.
- The live runs (H4, and one as my own user printing `KILLERS_QUIET`, all counts 0, `earlier_invocation_send_lines`
  0) were read-only and are not committed.
