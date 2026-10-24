# TabiTxtReports: C2 `missing` vs same-stem `.txt` in tabi round-12/w1 and round-13/w1

**PARTIAL.** Three parts, judged separately:

- **63-pair claim: HOLDS.** 63 of the 64 missing `.md` trailer paths in tabi `round-12/w1` and `round-13/w1` have a non-empty same-stem `.txt` in the same directory (31 + 32). AriaEntry has no file at either path.
- **Status computation: HOLDS** under the frozen C2 trailer rule (`contract.md:74-77`). The tool does exactly what the contract says.
- **Operator reading of `missing` and `unsettled`: BROKEN for those two waves.** The output reports 64 seats `missing` and both waves `unsettled` with 0 present. Nothing in it says the reports exist under the Acceptance path. The label is also broader than its docs (it covers symlinks, directories and unreadable paths), and the per-wave array named `missing` lists every non-present member. The fix is wording only (§5).

## Scope and bounds

- Read-only on tabi (named directories and files only) and on mori. The tool was run read-only against tabi with `--out` in scratch.
- Writes: this report; `.ufo/waves/round-20/falsify/TabiTxtReports/` (scan outputs); `/tmp/r20-txt-fixture-v3/` and the superseded `/tmp/r20-txt-fixture/` (fixtures).
- No lane or fleet file edited. No git or jj. No installs or updates. No subagents. No transcripts and no `.ufo/interactive-sessions`, `.ufo/worktrees` or `.jj` read.
- The settlement tool and `corpus/knowledge/wave-settlement-r20.md` were both edited by other actors during this run (§7). I did not touch either.
- Times are local (-03:00).

## 1. The 63 pairs (verified)

Method: for each member, the trailer is the last matching line after rstrip (the tool's rule). I then `lstat` the trailer path and `<stem>.txt` in the same directory.

| wave (canonical) | members | trailer `.md`, final line | `.md` present | non-empty same-stem `.txt` | Acceptance names `<Name>.txt` |
|---|---|---|---|---|---|
| `round-12/w1` | 32 | 32/32 | 0 | 31 (5,302 to 16,917 B) | 31/32 |
| `round-13/w1` | 32 | 32/32 | 0 | 32 (3,093 to 24,884 B) | 32/32 |

- AriaEntry (round-12) has no file at either path. Its Acceptance points to a corpus note, and the note holds its entry: `corpus/knowledge/playwright-accessible-locators-and-snapshots.md:4` ("lane AriaEntry (claim C2: one docs-held entry admitted, entry count 0→1"). Its registry record is `TabiR12.AriaEntry`.
- Directory listings. `round-12/w1` has 37 entries: 33 `.txt` (31 member reports, plus `assignments-result.txt` and `census-before.txt`), 3 `.json`, and `mistake/` (a checker and fixtures). `round-13/w1` has 37: 32 `.txt` and 5 `.json`. No top-level `.md` in either directory.
- Timing. Every member `.txt` is newer than its dispatch. Round-12 dispatch 01:02:58, `.txt` 01:05:07 to 02:09:33. Round-13 dispatch 02:07:13, `.txt` 02:09:24 to 02:50:28. `FreshRetry.txt` (round-12) was appended in round 13 by `ReceiptCorrection` (round-13 `dispatch.json:259`), so its mtime is a later edit. No `.txt` is a start stub, and no two share a hash. Headers are seat reports, e.g. `FreshProfile.txt`: "# FreshProfile — round-12 freshness review receipt".
- The dispatch contradicts itself. Round-12 `dispatch.json:239` (FreshProfile) says "Write concise evidence-backed findings to …/round-12/w1/FreshProfile.txt", and its trailer says `Report: write your scoped findings to .ufo/waves/round-12/w1/FreshProfile.md`. Round-13 `dispatch.json:234` (RoundGate) has the same pattern.
- Round 14 is clean. Its `dispatch.json` and `spec.json` contain no `.txt` (grep, no matches), and its 32 reports are `.md`. `AGENTS.md` has no report-format rule (grep for `.txt`, `Report:` and report format/extension: no matches). Neither side is documented as canonical.
- Registry. `swarm-registry.json` in round-12, round-13 and round-14 each has 32 of 32 members with `kind: spawn` and a non-null `agentId`. The embedded `registry.members` inside the dispatch files has null agentIds. Wave-1 F6 is true only for that embedded registry.

## 2. What the operator sees now

Command: `python3 tools/mori-wave-settlement.py scan --lane-root …/tabi-shokunin --fleet-root …/shokunin --out …/scan-tabi-lane.json`. Exit 1.

- `round-12/w1`: `unsettled`, present 0, missing 32. `round-13/w1`: `unsettled`, present 0, missing 32.
- Lane totals: 16 waves, 1,007 members, 891 present, 116 missing. States: 8 settled, 6 partial, 2 unsettled.
- 63 of the 116 `missing` rows (54%) have a same-stem non-empty `.txt` beside them. 64 of 116 (55%) sit in these two waves.
- The one other same-stem case is r19/w2 `SentinelInvoke` (two rows, dispatch and validation copies). Beside its `.md` path sits `SentinelInvoke.evidence.tar.gz`, an evidence archive (top-level `.ufo/` and `scripts/`), not a report. A stem match is not report evidence by itself.
- No other canonical wave has a same-stem file for any missing member. Examples: r15/w1 15 missing and 0 siblings; r17/w2 26 and 0; r20/w1 1 and 0. Round-20/w2 is now 64/64 settled (wave-1 F8 recorded 49/64 at its T2).
- The tool never reads `.txt`. `grep -c -i txt tools/mori-wave-settlement.py` returns 0 on sha256 `203c716e…` (mtime 08:11:12).
- Stability. The tool file changed twice during this run: 08:04:26 (sha256 `e5c06dad…`) and 08:11:12 (`203c716e…`). The tabi scan is byte-identical across both (`cmp` exit 0; first scan, re-run, and final scan all match). The §3 fixture gives the same results on both.

## 3. Controlled checks on `missing` (scratch fixture, current tool, sha256 `203c716e…`)

Fixture `/tmp/r20-txt-fixture-v3/`, seven members:

| member | report path shape | status |
|---|---|---|
| Sib | `Sib.md` absent; `Sib.txt` (3,000 B) beside it | `missing` |
| Link | symlink to a 3,000 B regular file | `missing` (frozen case `symlink-report` requires this: `frozen/c2-expected.json:16`, checked at tool line 583) |
| Dir | a directory at the path | `missing` |
| Locked | parent directory mode 000, outside `.ufo/waves` | `missing` |
| Empty | 0 B | `empty` |
| Stub | `STATUS: started` | `stub` |
| Ok | 3,000 B regular | `present` |

- Status mapping. `_member_status` (tool lines 225-238) returns `missing` for every outcome that is not regular, non-empty, non-stub or misrooted. `_inspect_report_path` (line 177 on) returns `other` for directories and symlinks, and `unavailable` on OSError. Both collapse to `missing`.
- The per-wave array. Tool line 291 is `missing = [… if member["status"] != "present"]`. Fixture result: `counts.missing: 4`, but the array is `["Dir","Empty","Link","Locked","Sib","Stub"]`. It includes the `empty` and `stub` members. One record gives two answers.
- Unreadable directory under `.ufo/waves/` (fixture B, removed): exit 2 with `mori-wave-settlement: lane root is unreadable` (tool line 674). `_dispatch_files` (lines 96-104) aborts the whole scan on any unreadable subdirectory. The lane root itself is readable, so the message is wrong.

## 4. Judgement: does `missing` mislead an operator?

**Yes, for these two waves; moderate severity.** The computation is not the problem. The words are.

Why the computation is right. The frozen contract defines member status by the `Report:` trailer (`contract.md:74-77`). The trailer path is absent, so `missing` is correct. The trailer is the machine contract, and the dispatch contradicts itself. "Trailer unmet" is a true statement.

Why an operator is still misled:

1. **Scope overclaim.** The decision table says "no file anywhere checked" (`knowledge doc:33`). The tool checks one path plus an optional fleet path. It never looks beside the path.
2. **`unsettled` reads as lost output.** The doc's own kama example says an `unsettled` wave was "exactly like a dispatched wave whose reports were lost" (`knowledge doc:64`). The tabi waves are the inverse: 63 reports exist. The contract's problem statement (`contract.md:51-54`) is the round-19 failure in which 48 reports were found by hand. As worded, this output presents 63 existing reports as lost.
3. **One label, four conditions.** `missing` covers absent, symlink, directory and unreadable. The decision table names only "no file".
4. **Contradictory fields.** The array named `missing` disagrees with `counts.missing` (§3).
5. **Thin disclosure.** The only disclosure is one sentence in the knowledge doc (`knowledge doc:68`). The lesson `corpus/lessons/round-20.md` does not mention r12 or r13. The frozen cases and the oracle have no sibling case (none of the 14 frozen cases has a same-stem file), so "14/14 matched" cannot detect this.

What an operator could do wrongly if they trusted the output (not observed): re-dispatch 64 seats, which wastes work and risks overwriting the `.txt` outputs; mark two waves failed; or record "lost reports" in a closure.

Where the tool is right: `missing` at the trailer path is a true signal that the trailer contract was not met, and an operator should fix the trailer/Acceptance contradiction. The change needed is wording that says so, not a change of status.

## 5. Proposed minimal wording (no code changes)

Essential for the tabi case:

**(a)** Decision-table row, `corpus/knowledge/wave-settlement-r20.md:33`. Replace with:

> `| no regular non-empty file at the \`Report:\` path (absent, symlink, directory or unreadable); files beside that path are not inspected | \`missing\` | **dead, failed or killed**; **that no output exists** (a same-stem file may hold it: §4) |`

**(b)** Row at `:38`. Replace the last cell with:

> `| none present, ≥1 member | \`unsettled\` | that the wave was dispatched (see §4); that its outputs are absent (zero trailer paths present is not zero outputs) |`

**(c)** New line after the decision table (§2):

> `In the per-wave output, \`missing\` lists every member whose status is not \`present\`, including \`empty\` and \`stub\`; \`counts.missing\` is the status count.`

**(d)** Replace the sentence at `:68` ("tabi r12/r13 wrote 63 same-stem `.txt` files beside missing `.md` paths.") with:

> `tabi \`round-12/w1\` and \`round-13/w1\`: every \`Report:\` trailer names \`.md\`; each member's \`# Acceptance\` names \`.txt\` (AriaEntry: a corpus note). 63 members wrote a non-empty same-stem \`.txt\`; AriaEntry wrote none. The tool reads all 64 as \`missing\` and both waves as \`unsettled\`. This is a trailer/Acceptance contradiction, not absent output.`

Optional:

- **(e)** New §4 bullet: "Same-stem files are not report evidence by themselves: r19/w2 `SentinelInvoke` has `SentinelInvoke.evidence.tar.gz` beside its `.md` path, an evidence archive."
- **(f)** `:88`: `wave1-dead-seats.json` contradicts `:33`. Rename it to a `missing` name. This is a file operation and was not done here.
- **(g)** Tool docstring line 17 (code comment; proposal only): "`missing`: no regular non-empty file at the Report: path (absent, symlink, directory or unreadable). Files beside that path are not read."
- **(h)** Tool line 674 (code string; proposal only): "mori-wave-settlement: cannot read a directory under .ufo/waves; scan aborted". Exit 2 unchanged.
- **(i)** Closure line for L1 (not tool output): "tabi r12/w1: 0/32 at `.md` trailer paths; 31 same-stem `.txt` reports present (5.3 to 16.9 KB); AriaEntry: no file, corpus-note entry admitted. tabi r13/w1: 0/32 at `.md`; 32 same-stem `.txt` (3.1 to 24.9 KB). Cause: dispatch Acceptance says `.txt`, trailer says `.md`. Round 14 uses `.md` throughout."

Not proposed now (code and frozen-case changes): renaming the array key, adding a `shadowed_by` annotation, or adding a frozen-style case "trailer absent + same-stem non-empty `.txt` → missing" to pin the intent.

## 6. Corrections to the wave-1 ground truth (`.ufo/waves/round-20/build/GtLaneTabi.md`)

- **F2 (line 129)**: "round-12/w1 (31 of 32 missing)" should read 32 of 32 missing, 31 with a same-stem `.txt`. The 63 total is right, and table row 36 is right.
- **F6 (line 137)**: true only for the embedded registry. The sibling `swarm-registry.json` in round-12, 13 and 14 has 32/32 `spawn` records with agentIds.
- **Clone trees.** `final-clones/` is absent at `tabi-shokunin/final-clones`, `tabi-shokunin/.ufo/waves/final-clones`, `tabi-shokunin/.ufo/final-clones` and `/home/vgpnk/Projects/shokunin/final-clones` (checked 08:0x to 08:12). The fleet record (`evidence/c2-live-fleet.json`, scan started 10:46:50Z, written 10:46:53Z per `knowledge doc:96`) shows tabi at 67 waves and 3,932 members, matching wave-1's T2 totals for those two fields. Its 561 missing differs from wave-1's 575. The current lane-root scan gives 16 waves, 1,007 members, 116 missing and 221 ignored JSON (wave-1's walk: 5,093). [INFERENCE] the clone trees existed around 10:34 to 10:46Z and were gone by about 11:03Z. Not verified.
- **F8 (line 141)**: live drift. Round-20/w2 is 64/64 settled now.

## 7. Unobserved or inferred

- Who wrote the `.txt` files, and why the Acceptance says `.txt`: [INFERENCE] a template mismatch in the dispatch. Transcripts were not read, per bounds.
- Whether the clone trees will return: not observed.
- `.txt` content quality beyond headers, sizes and timing: not reviewed.
- Other actors edited the tool twice and the knowledge doc during this run. My line numbers are the 08:12 values. The replacement sentences in §5 matched the current text of those lines at that time.
- The first scan's version (before or after the 08:04:26 edit) is not recorded. Its bytes match the final version's.

## 8. Artifacts and installs

- `.ufo/waves/round-20/falsify/TabiTxtReports/scan-tabi-lane.json` (71,163 B, exit 1) and `scan-tabi-lane-rerun.json` and `scan-tabi-lane-final.json` (byte-identical, exit 1).
- `/tmp/r20-txt-fixture-v3/` (fixture, `out.json`). `/tmp/r20-txt-fixture/` is the superseded v2 fixture.
- No lane or fleet file written. No git or jj. No installs or updates. Tools used: python3 3.14.8, `/usr/bin/jq` 1.8.2, coreutils.
