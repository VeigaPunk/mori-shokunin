# mori round 30 — wave 1 — DraftSkillRows (SKILL.md `Round30` rows + routed R7 second half)

Seat `MoriR30.DraftSkillRows` (leaf: no subagents, no background jobs). Lane
`/home/vgpnk/Projects/shokunin/mori-shokunin`, read at `git rev-parse HEAD` =
`e936482a6070db40049bff46f7da4754b15d41af`, re-checked at `b039dd4ffa3057ce4a0df7ad6505048d04bc68d3` (writer and
wave-1 reports committed; `SKILL.md` still 742 lines and `git status --porcelain -- SKILL.md` clean, entry and
`count-c1.sh` still absent). Contract read first: `.ufo/waves/round-30/contract.md` (C1
condition 5 at `:42`). Deliverable: four ready-to-paste `SKILL.md` rows tagged `Round30` that cite the C1 entry,
their exact insertion lines, and the qualified replacement for routed R7's second half (`SKILL.md:661`).

## 1. State read (commands and their output)

- `git diff --stat 58b61681..HEAD` lists only round-30 wave files plus `LOG.md` and `SCORECARD.md`; `SKILL.md` is
  unchanged since the entering tip, so the line numbers below hold at both revisions.
- `wc -l SKILL.md` → `742`; the last byte is `\n` with no trailing blank line (`tail -c 120 SKILL.md | od -c` ends
  `|  \n`), so an appended section starts at line 743.
- The only table carrying `Round2x` tags is Round27's: header `SKILL.md:725` is
  `| Situation | What to conclude | What not to conclude | Grounding |`, separator `:726`, data rows `:727-734`.
- `grep -n 'Round2' SKILL.md` returns section headers `Round21`–`Round27` only: **no `Round29`-tagged row
  exists** (round 28's whole `SKILL.md` change is 2 insertions/2 deletions, `1c4c186`). The assignment's premise
  "tables that hold `Round27`/`Round29`-tagged rows" holds only for Round27, so the drafted table copies Round27's
  four-column shape.
- The C1 entry `corpus/knowledge/earlyoom-invocation-scope-r30.md` does not exist at HEAD (`ls corpus/knowledge | grep r30` empty), and
  `.ufo/waves/round-30/count-c1.sh` does not exist at HEAD (`ls .ufo/waves/round-30/` → contract.md, evidence,
  rule-text.md, w1, wave1-dispatch.json, wave1-run.err, wave1-run.json, wave1-spec.json). Condition 5 is therefore
  drafted against `contract.md:42` by inspection; **I ran no counter**.

## 2. Drafted `Round30` rows — ready to paste

Insertion: append after current line 742. The fenced block occupies new lines 743-755; the header is line 744 and
the four rows land at **752, 753, 754, 755** (row 1 = unbounded scope, row 2 = disputed shape + A2a, row 3 =
earlier-invocation sends by unit state, row 4 = per-invocation dry-run). The file ends at `742` with `\n`, so the
leading blank line in the block is the separator.

```markdown

## Round30 — earlyoom invocation scope (earlyoom-invocation-scope-r30.md)

Grounding for every row: `corpus/knowledge/earlyoom-invocation-scope-r30.md` (its decision table over frozen cases;
sources S156 and later). Every row is tagged `Round30`. Detection and report only: no row advises changing an
earlyoom option, a unit or `/etc/default/earlyoom`.

| Situation | What to conclude | What not to conclude | Grounding |
|---|---|---|---|
| earlyoom is `active` and `ActiveEnterTimestampMonotonic` is missing or `0` | the invocation is unbounded: `earlyoom.scope_complete=false`; every placeable boot line stays a candidate and the current invocation is taken from the last version line, so a send before that line is an earlier-invocation send; with no positive evidence the verdict is `KILLERS_UNKNOWN` (exit 2), and a send inside the last-version tail is still `KILLER_ACTED` (exit 1) | that an unbounded scope is an empty one (nothing happened); that the whole boot is attributed to the running instance; that `KILLERS_UNKNOWN` here is a read failure | (Round30) `corpus/knowledge/earlyoom-invocation-scope-r30.md` (unbounded-scope row); rule A2-05 (`.ufo/waves/round-27/contract.md:53`); `tools/mori-oom-killers.py:278-302`, `:424` |
| earlyoom is `active`, `ActiveEnterTimestampMonotonic` is missing or `0`, a real send line appears in the boot, then a plain restart (a later version line) — the disputed shape round 29 moved from `KILLER_ACTED` to `KILLERS_UNKNOWN` | `KILLERS_UNKNOWN` (exit 2): the send falls before the last version line and is counted only in `earlyoom.earlier_invocation_send_lines`, `earlyoom.actions.sigterm` stays 0 and `scope_complete` is false. This is the A2a limit: for an `active` unit an earlier-invocation send is reported but is not a verdict input, so the reader abstains — it neither claims the send acted now nor calls the unit quiet | that the restart erased the earlier send; that the earlier send proves the current invocation acted; that this `KILLERS_UNKNOWN` is a tool or read failure; that the same shape reads `KILLERS_QUIET` | (Round30) `corpus/knowledge/earlyoom-invocation-scope-r30.md` (disputed-shape row; A2a limit); rules A2-05, A2-06, A2-07 (`.ufo/waves/round-27/contract.md:53-55`); A2a (`.ufo/waves/round-26/contract.md:171-172`, `:178-179`); `tools/mori-oom-killers.py:293-302`, `:465-469`, `:487-489` |
| a send or escalation line of this boot sits outside the current invocation (before `ActiveEnterTimestampMonotonic`, or before the last version line under an unbounded scope) | it counts in `earlyoom.earlier_invocation_send_lines`; for an earlyoom that is not `active` a non-zero count is positive evidence → `KILLER_ACTED` (exit 1) with `earlyoom.actions=null`, so a stop or restart is not quiet; for an `active` unit it is reported and is not itself a verdict input | that a restarted or stopped earlyoom never killed anything; that `scope_complete=true` means the whole boot was checked; that earlier sends belong to the current invocation's `earlyoom.actions` | (Round30) `corpus/knowledge/earlyoom-invocation-scope-r30.md` (earlier-invocation row); rule A2-06 (`.ufo/waves/round-27/contract.md:54`); `.ufo/waves/round-26/contract.md:175-179`; `tools/mori-oom-killers.py:317-352`, `:465-469` |
| the journal holds `dryrun mode enabled` and send lines, or one invocation ran dry-run and another did not | dry-run is per invocation: the scan splits at each version line, so send lines inside a segment that logged `dryrun mode enabled` go to `earlyoom.dryrun_send_lines` while `actions.sigterm` and `.sigkill` stay 0 and are never positive evidence; a real send in another invocation still counts (`KILLER_ACTED`), and a dry-run invocation with no other evidence reads `KILLERS_QUIET` | that a `sending SIG… to process` line inside a dry-run invocation sent a signal (earlyoom prints the same line and signals nothing); that the current invocation's dry-run flag applies to an earlier invocation or the reverse; that `KILLERS_QUIET` on a dry-run invocation means no send lines were logged (they are in `dryrun_send_lines`) | (Round30) `corpus/knowledge/earlyoom-invocation-scope-r30.md` (per-invocation dry-run row); rules A2-04 and A2-07 (`.ufo/waves/round-27/contract.md:52,55`); `tools/mori-oom-killers.py:333-381`, `:417-419` |
```

Notes for the C1 author (not part of the paste):
- Each row contains the literal `Round30` and the full path `corpus/knowledge/earlyoom-invocation-scope-r30.md`, satisfying
  `contract.md:42` under either reading (full path or bare filename). The tag sits in the Grounding cell, so a
  counter should match anywhere in the row, not in a fixed column.
- The entry is absent, so rows name its decision rows by shape ("unbounded-scope row", "disputed-shape row",
  "earlier-invocation row", "per-invocation dry-run row") and ground on rules A2-04…A2-07 plus current tool lines.
  Once the entry lands, replacing those shape names with its actual row names or case ids is a safe improvement;
  condition 5 does not require it.
- No row advises changing an earlyoom option, a unit or `/etc/default/earlyoom`.

## 3. Routed R7, second half — `SKILL.md:661` unqualified citation

Defect as charged (`.ufo/waves/round-29-verifier-spotcheck.md:166`): `SKILL.md:661` cites `contract.md:83-84`
without a directory. Evidence read this wave:

- `sed -n '661p' SKILL.md | wc -c` → `1134` bytes including the newline; `sed -n '661p' SKILL.md | grep -o
  'contract\.md:83-84'` → one hit. Line 661 is the cap row `| mori must state the cap | ...`; it is **not** the
  "mori never acts on this text" paragraph (that paragraph starts at `:663`), so an edit at 661 must land on the
  cap row; `sed -n '661p'` and `awk 'NR==661'` agree with the round-29 record.
- Ten files match `.ufo/waves/round-2*/contract.md` (`ls .ufo/waves/round-2*/contract.md | wc -l` → `10`), so a
  bare `contract.md:83-84` is ambiguous from the lane root.
- The cited claim is at `SKILL.md:661`: the tool "reports the **cap**, never a running-job count, and the live count
  is not readable from outside the session". `.ufo/waves/round-25/contract.md:83-85` carries it: `:83` "**Scope
  bounds:** the tool reads one config file, not project-level or environment overrides; it reports", `:84` "the
  per-session cap the binary computes, not how many jobs run now. The live running-job count is not", `:85`
  "readable from outside the session and stays frontier." The cited `:83-84` stops mid-sentence.
- Round-29 record: `.ufo/waves/round-29/w1/ScoutShonen.md:87-90` ("resolves only from the section context to
  `.ufo/waves/round-25/contract.md:83-85` (checked: scope bounds and the unreadable live count — the claim is
  accurate)") and `:162` (`contract.md:83-84` → `.ufo/waves/round-25/contract.md:83-85`).

Replacement is line 661, in place, one token changed (1143 chars after the change; `grep -c
'contract\.md:83-84'` → `0`). Ready to paste:

```
| mori must state the cap | `python3 -I -B tools/mori-job-runway.py` → one JSON object (`schema: mori-job-runway-v1`) with `configured {state,value}`, `clamp {state,value,sites}`, `setting_default {state,value,sites}`, `effective`, and `verdict` ∈ `RUNWAY_CLAMPED` (exit 1) / `RUNWAY_AS_CONFIGURED` (exit 0) / `RUNWAY_DEFAULT` (exit 0) / `RUNWAY_UNKNOWN` (exit 2) | that the session was at capacity — the tool reports the **cap**, never a running-job count, and the live count is not readable from outside the session (`.ufo/waves/round-25/contract.md:83-85`); that an absent or unreadable clamp means "no clamp" (it is `RUNWAY_UNKNOWN`); that the file sets no `maxJobs` — `RUNWAY_DEFAULT` also reads a root flow mapping, a JSON file or a flow-mapped `maxJobs` child as absent, so the effective 100 is the schema default rather than a value read from the file (`corpus/knowledge/harness-job-capacity-r25.md` decision row `RUNWAY_DEFAULT`); that the file's `async.maxJobs` is the value the session resolved — the runtime settings stack has project and overlay layers the tool does not read (`corpus/knowledge/harness-job-capacity-r25.md` F13) |
```

R7's first half (PROVINCE stale in five places, listed at `ScoutShonen.md:110-124`) is outside this seat's scope
and is not reported here.

## 4. Evidence for the row wording (invented inputs, reader only)

Five invented inputs (no lane fixture, no host value, no unit name) were written under
`/fast/scratch/hyaku/mori-r30/DraftSkillRows/` and run one at a time as
`python3 -I -B tools/mori-oom-killers.py --inputs <name>.json`; observed output:

| invented input | verdict | exit | fields observed |
|---|---|---|---|
| `disputed.json` (active, start stamp absent, real send, then version line) | `KILLERS_UNKNOWN` | 2 | `scope_complete=false`, `actions.sigterm=0`, `earlier_invocation_send_lines=1` |
| `unbounded_current_send.json` (active, start stamp absent, send after the last version line) | `KILLER_ACTED` | 1 | `scope_complete=false`, `actions.sigterm=1`, `earlier_invocation_send_lines=0` |
| `earlier_dryrun.json` (earlier invocation dry-run; current invocation real send) | `KILLER_ACTED` | 1 | `actions.sigterm=1`, `dryrun=false`, `dryrun_send_lines=0`, `earlier_invocation_send_lines=0` |
| `current_dryrun.json` (current invocation dry-run with one send line) | `KILLERS_QUIET` | 0 | `dryrun=true`, `dryrun_send_lines=1`, `actions.sigterm=0`, `scope_complete=true` |
| `inactive_earlier_send.json` (unit inactive, one send this boot) | `KILLER_ACTED` | 1 | `actions=null`, `earlier_invocation_send_lines=1`, `scope_complete=false` |

These runs exercise the pure reader only. They are evidence for how the rows phrase the rules; they are **not** a
C1 or C2 verification and no case file was touched.

## 5. Bounds, privacy, and known limits

- Wrote only this report and files under `/fast/scratch/hyaku/mori-r30/DraftSkillRows/`; no lane edit, no commit,
  no git/jj write, no unit started/stopped/signalled, no omp invocation.
- Read-only git only (`rev-parse`, `diff`, `show`, `log`). No writer seat was messaged; no tool source line and no
  raw tool output was copied anywhere — citations here are path:line and verdict strings already in the contract.
- Invented values only; no uid, pid, user unit name, `/etc/default/earlyoom` value, journal `MESSAGE`, session id
  or settings value is recorded.
- No tools installed or updated this seat.
- Limits: the entry and `count-c1.sh` are absent, so condition 5 is checked by inspection against `contract.md:42`,
  not by a run; the "S156 and later" wording in the drafted grounding line presupposes the C1 source rows land as
  the contract declares — if fewer than three S156+ rows land, that phrase, not the rows' tag or path, is what
  needs correcting.
- Unrun checks are not passes: `count-c1.sh`, `check-blind-wave.sh`, `count-c2.sh` and both selftests were not run
  by this seat.

## 6. Files

- Report: `.ufo/waves/round-30/w1/DraftSkillRows.md` (this file).
- Scratch: `/fast/scratch/hyaku/mori-r30/DraftSkillRows/` — `block.md` (paste block), `line661.txt` (line 661 as
  read), `line661.qualified.txt` (replacement), `disputed.json`, `unbounded_current_send.json`,
  `earlier_dryrun.json`, `current_dryrun.json`, `inactive_earlier_send.json`.
