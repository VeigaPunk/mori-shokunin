# Round 26 wave 2 — CriticA2Amendment (critic, leaf)

Target: amendment A2 and its addenda (`.ufo/waves/round-26/contract.md:152-179` at `16935e24`) and the four
post-freeze tool commits `278f02e`, `825f988`, `93aa1b9`, `738eec1` (from
`git log --format='%h %ci %s' c2fdd929..16935e24 -- tools/mori-oom-killers.py`). Everything was read from
committed bytes (`git show`, `git archive` into `/fast/scratch/hyaku/mori-r26/CriticA2Amendment/`).
Tooling: nothing was installed or upgraded. The tools used were `git`, `jq`, `python3`, `gh` (read-only API) and
`jj op log --ignore-working-copy` (read-only).

## Verdict

**The counted value holds. A2 is legitimate as a change to the tool's rules only. Three of its adopted rules have
defects.** No frozen case was changed, shaped or contradicted. N and the counter did not move, and the blind build
already gave the same `PASS 32/32`. None of the case seat's later commits reached the counted file. Changing the
tool after the freeze fits the round-25 closure, which itself asked for abstain fixes after its own freeze.
However, A2 repeats two things that closure routed: rules with no committed fixtures (round-25 R1) and a
capability row wider than its evidence (round-25 R2). It also adds one new regression that throws away positive
evidence.

## Q1 — Was any frozen case's expectation shaped or contradicted? **Holds.**

| Check | Command / evidence | Observed |
|---|---|---|
| frozen file unchanged | `git rev-parse <r>:tools/fixtures/mori-oom-killers/cases.json` for 5b10649, c2fdd929, 278f02e, 825f988, 93aa1b9, 738eec1, 21386b9, 16935e24 | all `5b4dcee7b682…` |
| selftest at every tool revision | `python3 -I -B rev-<r>/tools/mori-oom-killers.py --selftest` on archives of the six revisions | `PASS 32/32`, exit 0 at every one |
| per-case output, blind build compared with the tip | scratch `percase.py`: `read_inputs` on each frozen case, every output leaf diffed between c2fdd929 and 16935e24 | 32 of 32 `same-core`: every field the blind build printed is byte-equal at the tip. The only differences are three added keys (`dryrun_send_lines`, `process_group_lines`, `earlier_invocation_send_lines`). No case takes the new SetupError path. |
| non-adoption claims (contract.md:170-172) | frozen pins (`jq` on the frozen file) | Real. A1a conflicts with c04, which pins `scope_complete:false` with `actions.sigterm:1`. A2a conflicts with c02, which pins QUIET with a send line 1 µs before the invocation start. A3 conflicts with c19, which pins QUIET for a version line alone. |

The selftest instrument changed once. Since 278f02e, a SetupError result is scored against the case's
expectations; before, it was an automatic FAIL (tool.diff hunk `@@ -597,8 +671,9 @@`). This loosens the scoring
of error cases. It changed nothing on the frozen file, because no frozen case raises. It also matches contract
rule 4 (contract.md:104-105). Severity: none for the counted value; noted as a disclosed change to the instrument.

## Q2 — Did the L1 change the counted value or N? **Holds.**

- `count-c2.sh` was added only in `99338de` (A1) and is not touched by any A2 commit: `git log -- .ufo/waves/round-26/count-c2.sh`
  lists 99338de only, and the A2 commits change only `contract.md` and the tool (`git show --stat`).
- `bash <(git show 16935e24:.ufo/waves/round-26/count-c2.sh) 16935e24` prints `freeze_order=ok`,
  `cases_changed_since_freeze=0`, `N=32`, `PASS 32/32`, `exit=0`. The same script with `c2fdd929` (the blind build)
  prints the same five lines. A2 therefore did not decide the outcome. This is the test round 25 applied
  (`round-25-verifier-spotcheck.md:52-53`).
- The receipt `evidence/c2-selftest.txt` at 16935e24 names `tool_blob 44dac3fd…`. That equals
  `git rev-parse 16935e24:tools/mori-oom-killers.py` and the same at 4dba9cc7.

## Q3 — Did the case seat's later commits leak into the counted file? **Holds: no leak, and the exclusion was required.**

| Case-seat commit (sandbox `/fast/scratch/hyaku/mori-r26/wt-cases`) | Date | cases.json blob | Where it went |
|---|---|---|---|
| `eaa13ef9` initial | 10:18:00 | `5b4dcee7` | counted file (`5b10649`) |
| `4447597f` amendment 1 (withdraw c19, c24, c28; add c33, c34, c35) | 10:20:31 | `6b6fa4ed` | `cases-supplementary.json` at 278f02e (blob `6b6fa4ed`) |
| `da9af118` amendment 2 (c21 journal grows) | 10:38:21 | `d7c9040b` | supplementary at 21386b9 (blob `d7c9040b`) |

- The case seat's handoff asks for its **tip** `da9af118` to be landed as the frozen file
  (`w1/WriteOomKillersCases.md:247-249`). It also says "No tool existed when either amendment was made" (`:21-22`).
  That is false for the lane: the tool's lane commit `c2fdd929` is dated 10:20:00, before amendment 1 (10:20:31)
  and amendment 2 (10:38:21; later even than `738eec1`). Landing the tip would have broken freeze-before-tool. The
  L1 counted `eaa13ef9` and kept the amendments uncounted. That is the correct choice.
- Supplementary compared with frozen: 29 shared ids have the same inputs and expectations, except c21, whose inputs
  differ. c19, c24 and c28 are absent; c33–c35 are new (scratch comparison).
- The blind build fails the supplementary file 31/32 (`c35`: got `KILLER_ACTED` exit 1, expected
  `KILLERS_UNKNOWN` exit 2). The tip passes it 32/32. So the case seat's later commit did shape the tool
  (278f02e), but only in the uncounted file. Counting `da9af118` would have given the blind build 31/32.
- External timing, partly not run: GitHub push events show `5e5e86f1..5b10649d` at 13:19:02Z and
  `c2fdd929..99338de7` at 13:21:10Z (`gh api repos/VeigaPunk/mori-shokunin/events`). So the freeze was really
  pushed before amendment 1. No push event exists for `c2fdd929` itself. Its 10:20:00 date (an exact minute, as
  are the jj op entries at 10:19:00 and 10:20:00) cannot be checked independently against 10:20:31.
  [INFERENCE] The DAG order (freeze → tool → A1) is what the counter checks, and it holds.

## Q4 — Is a post-freeze tool change consistent with the round-25 closure? **Holds in principle, with two repeated defects.**

- Round 25 ruled that the counted value is "a tally over the 21 frozen cases". It routed the tool's false numbers
  as **R1**: "Make rule 1 abstain … and commit the probe corpus as fixtures so the count can be re-derived"
  (`round-25-verifier-spotcheck.md:73-74,173-176`). Round 25 itself expected the tool to change after its freeze.
  A2's direction (more abstention, frozen file untouched) matches that.
- The round-25 order rule was broken again: round 25 flagged A4 landing 15 s after its code (`:54-56`). Here the
  malformed-timestamp rule's code landed in `278f02e` at 10:22:41, but its A2 record landed in `825f988` at
  10:26:11. The A2 header says "after the tool landed" (contract.md:152), which is true, but it does not say that
  this rule's code came first. **Defect (low, provenance).**
- Round-25 R1 says to commit the fixtures so the count can be re-derived. Not done (see D3).

## Counterexamples and defects

**D1 — the malformed-timestamp rule discards positive evidence (defect, moderate; attacks contract.md:168-169, tool `16935e24:tools/mori-oom-killers.py:291-296`).**
Contract rule 1 says positive evidence stands even when the scope is incomplete (contract.md:97-98). Frozen c30
applies that principle to a null journal with oomd notices (KILLER_ACTED). Scratch `ce.py` on the c01 inputs gave:
- CE1, an in-scope `sending SIGKILL to process` line plus one in-scope record with no `__MONOTONIC_TIMESTAMP`:
  blind `KILLER_ACTED` exit 1; tip `KILLERS_UNKNOWN` exit 2 (SetupError).
- CE2, `oomd_notices=2` plus one earlyoom record with no timestamp: blind `KILLER_ACTED` exit 1; tip
  `KILLERS_UNKNOWN` exit 2. A malformed earlyoom record now hides systemd-oomd's kill notices.

Smallest safe correction: do not raise. Leave the unplaceable record uncounted, set `scope_complete` false, and
let rule 1 apply. [INFERENCE, not run] c35 still passes: it pins only `KILLERS_UNKNOWN`/2, and its only send line
is the unplaceable one, so the verdict stays UNKNOWN through the incomplete scope.

**D2 — a dry-run invocation anywhere in the boot hides a later real kill (defect, low to moderate, false quiet; attacks contract.md:175-178, tool tip lines around `if any(t.startswith(PREFIX_DRYRUN) for t in earlier_texts)`).**
- CE3: earlyoom is inactive. The journal has invocation 1 (`earlyoom 1.9.0`, `dryrun mode enabled`), then
  invocation 2 (`earlyoom 1.9.0`, `sending SIGKILL to process …`). Tip result: `KILLERS_QUIET` exit 0,
  `earlier_invocation_send_lines=0`.
- CE4, the control (invocation 2 alone): `KILLER_ACTED` exit 1.

This contradicts A2's own sentence that "a stop without restart no longer reads quiet". Smallest correction: split
the earlier lines into invocations at each version line and apply the dry-run flag per invocation.

**D3 — the adopted A2 rules have no committed case; the capability row cites evidence that does not exercise them (defect, moderate, width; attacks `SCORECARD.md:1620`).**
Scan of both fixture files (scratch). No case in either file contains a `Suppressed … earlyoom.service` line, a
non-steady `ActiveState`, a dry-run invocation with send lines, an active unit with
`ActiveEnterTimestampMonotonic=0`, or an earlier-invocation send line. Only supplementary c21 contains a
`killing whole process group` line, and it does not pin `process_group_lines`. No case in either file pins any of
the three new fields. Only the malformed-timestamp rule is tested (supplementary c35).

The row nevertheless claims "process-group and dry-run send log lines … send lines of earlier invocations this
boot". Its evidence column cites "PASS 32/32 on `cases-supplementary.json`". This repeats round-25 R1 (probe
corpus not committed; CriticC2Width's X1–X9 inputs are "in scratch", `w1/CriticC2Width.md:40`) and R2 (row wider
than its evidence). Smallest correction: commit X1–X9 and CE1–CE4 as uncounted supplementary cases that pin the
new fields, or narrow the row to what the cases exercise.

**D4 — A2 rejects A3 on the strength of c19, which its author had already withdrawn (defect, low, disclosure; attacks contract.md:170-172).**
The case seat withdrew c19 in `4447597f` at 10:20:31 (`w1/WriteOomKillersCases.md:18-19,155,225-229`). The L1 had
that withdrawal at 10:22:41, when it landed the supplementary file without c19. A2 was written at 10:26:11. c19 is
still in the counted file, so adopting A3 would really drop the count to 31/32. A2 should say that the pinning case
was withdrawn by its author to stay within the 24–32 band, not for being wrong.

**D5 — the lesson's tally does not match A2 (defect, low, calibration; attacks `corpus/lessons/round-26.md:26-30`).**
The lesson says there were nine shapes, of which five were fixed and three stay as disclosed limits (eight in
total). A2 lists eight adopted items and four non-adopted ones (contract.md:157-179).

## Not run

- Whether systemd 262 journald emits `Suppressed N messages from earlyoom.service` with exactly that text, and
  whether `journalctl -u earlyoom.service` returns it. A1b depends on both.
- An independent timestamp for `c2fdd929`'s push (see Q3).
- Applying the D1 and D2 corrections and re-running the 32 frozen and 32 supplementary cases.

## Impacted axes

- coverage (C2): the counted value holds; the capability row is wider than its evidence (D3); two rule regressions
  (D1, D2).
- calibration: low-severity disclosure and tally drift (D4, D5, and the order note under Q4).
- Not affected: freshness (C1), adjacency, depth, operability.

Checks for the owner: `bash count-c2.sh 16935e24` and `bash count-c2.sh c2fdd929` (both should print PASS 32/32);
scratch `ce.py` (CE1–CE4); the supplementary selftest at the tip and at c2fdd929 (32/32 and 31/32).
