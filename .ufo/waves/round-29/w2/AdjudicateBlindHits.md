# AdjudicateBlindHits — wave 2 report (MoriR29.AdjudicateBlindHits)

Adjudication of all 20 hits in `.ufo/waves/round-29/evidence/blind-check-prefreeze.txt`
(committed, `blind_violations=20`). Hit lines were read from the committed tree at the
exact lane rev the check ran, `221cbd8faa88e07ad20445d5a87bbc1a3039d73e`
(`git show 221cbd8f:<path>`, read-only; evidence header line 1 confirms that rev). Check
logic reproduced from the committed `check-blind-wave.sh` (patterns at lines 52-64, loop
lines 91-155); every pattern claim below was re-executed against the committed lines and
matched exactly the branch stated.

No tool was installed or updated (tooling directive: nothing needed).

## Classes

- (a) tool source or tool-line citation
- (b) output of a run of `tools/mori-oom-killers.py`
- (c) writer report lacking a files-opened list
- (d) false positive (pattern and reason)

## Table (20 hits)

| # | file:line (committed line quote) | class | fired pattern / why not (a)-(c) |
|---|---|---|---|
| 1 | AxisOperability.md:19 — `git -C /home/vgpnk/Projects/shokunin show 63729047:MANIFEST.json > /tmp/manifest-r29.json   # exit 0, 1110380 bytes` | (d) | `repro_id_re`∧`result_re`: `-r29` inside `manifest-r29.json` + `exit 0`. A `git show` command echoing a MANIFEST with an exit-status comment; no tool run. |
| 2 | BuildTipReceipts.md:5 — `Created `/fast/scratch/hyaku/mori-r29/BuildTipReceipts/make-tip-receipts.sh` (SHA-256 `4bf31a0f32ad04662c06ac3c3f5fce00ec930e46682c80c6da9721fb819dd6eb`). It resolves the requested commit to a full hash, checks out that parent in a no-hardlink sandbox clone, records each exact command and captured output, and writes the three named receipts. If either round-29 counter is absent from the parent tree, its receipt says `counter absent at <full hash>` and records exit 2. The generator exits 0 when it has written all three receipts; measured command statuses remain in the receipts.` | (d) | `repro_id_re`∧`result_re`: `r29` in `mori-r29` + `exit 2` (prose: "records exit 2"). Prose describing the receipt generator; exit codes are counter-status narration, not oom-killers output. |
| 3 | BuildTipReceipts.md:135 — `wrote /fast/scratch/hyaku/mori-r29/BuildTipReceipts/demo/tip-c1.txt (exit 2)` | (d) | `repro_id_re`∧`result_re`: `r29` in path + `exit 2`. Demo receipt write line for the C1 counter; not oom-killers output. |
| 4 | BuildTipReceipts.md:136 — `wrote /fast/scratch/hyaku/mori-r29/BuildTipReceipts/demo/tip-c2.txt (exit 2)` | (d) | Same: `r29` + `exit 2`. Demo receipt for C2 counter. |
| 5 | BuildTipReceipts.md:137 — `wrote /fast/scratch/hyaku/mori-r29/BuildTipReceipts/demo/tip-retention.txt (exit 1)` | (d) | Same: `r29` + `exit 1`. Demo receipt for retention counter. |
| 6 | BuildTipReceipts.md:140 — `Both absent-counter receipts resolve the parent to `7118f320a5ef18d20c1e361eff77db0e1a97b2d6`, retain the required command, say `counter absent at 7118f320a5ef18d20c1e361eff77db0e1a97b2d6`, and end with `exit: 2` (`/fast/scratch/hyaku/mori-r29/BuildTipReceipts/demo/tip-c1.txt:1-5`, `tip-c2.txt:1-5`). The retention receipt records the specified scan command and its captured output, ending with `exit: 1` (`/fast/scratch/hyaku/mori-r29/BuildTipReceipts/demo/tip-retention.txt:1-5`). Thus the counter-absence behavior is observed; the retention scan's exit 1 is a risk for the parent to assess, not a pass. No lane implementation files were changed and no tool was installed.` | (d) | `repro_id_re`∧`result_re`: `r29` in `mori-r29` + `exit 1` ("retention scan's exit 1"). Narrative summary of receipt-file contents. |
| 7 | DraftQualityCriteria.md:75 — `    `mori-oom-killers.py:<digits>`, `mori-oom-killers.py` followed by a line range, or a `Tool lines` table header;` | (d) | Tool-header check (`lower_line` contains `tool lines`). This is the quality-criteria document itself defining what counts as a forbidden citation; the literal string `Tool lines` is meta-description, not a citation in a report. |
| 8 | DraftQualityCriteria.md:76 — `    tool-run output is a `MORI_OOM_KILLERS_SELFTEST:` line other than a PASS tally of an older case file, a` | (d) | `selftest_marker` present with no `PASS 30/30`/`32/32` after it. The criteria doc is quoting the marker to define the run-output category; not real tool output. |
| 9 | DraftQualityCriteria.md:77 — `    `KILLERS_QUIET exit` line, or an `--inputs` repro result. A files-opened list is a `Files opened` line or heading` | (d) | `input_flag` (`--inputs`)∧`result_re` (`KILLERS_QUIET` literal). Criteria doc defining the run-output category; not tool output. |
| 10 | DraftQualityCriteria.md:86 — `    non-writer report containing `mori-oom-killers.py:305`; a `CaseA2r` report with no files-opened list; a writer` | (d) | `cite_file_re` (`mori-oom-killers.py:305`). The criteria doc's illustrative example of a banned citation, not a citation in a report. |
| 11 | ReviewLateMutCountC1Amended.md:78 — `` `corpus/knowledge/system-pressure-r24.md`). Observed: `superseding=8/8`, `readers_left=0`, `C1=met`, exit 0 —` | (d) | `repro_id_re`∧`result_re`: `r24` in `system-pressure-r24.md` + `exit 0`. Review summary of the C1 supersed check (a different checker), not oom-killers output. |
| 12 | ReviewLateMutHeadingCheck.md:37 — `| named-1 | r27 contract must fail @f2de0e | `check_heading_time_7118f320.py f2de0e .ufo/waves/round-27/contract.md` | `stated=2026-10-22T15:55Z … cI=2026-10-22T12:50:10-03:00 verdict=FUTURE-DATED`, second heading day/ok, `headings=2 future_dated=1`, exit 1 | reproduced open (checker correct here) |` | (d) | `repro_id_re`∧`result_re`: `r27` + `exit 1`. Table row about `check_heading_time_7118f320.py`, an unrelated checker. |
| 13 | ReviewLateMutHeadingCheck.md:39 — `| named-2 | r28 contract must pass @f2de0e | `… f2de0e .ufo/waves/round-28/contract.md` | `headings=1 future_dated=0`, exit 0 (heading :73 day granularity) | reproduced open |` | (d) | `repro_id_re`∧`result_re`: `r28` + `exit 0`. Same unrelated checker. |
| 14 | CaseA207a.md:1 — `# Round 29 A2-07 blind cases — CaseA207a` | (d) | `writer-missing-files-opened-list`: regex `files_header_re` (check-blind-wave.sh:59) requires the whole heading line to be exactly `Files [i] opened`/`Opened files` (± trailing punctuation). Actual heading at line 192 is `## Opened files and URLs` — extra words break the match. A files-opened list exists (see below). |
| 15 | CaseA207b.md:1 — `# CaseA207b — A2-07 blind cases` | (d) | Same pattern; actual heading at line 195 `## Files and URLs opened` (word order breaks the regex). List exists. |
| 16 | CaseA207c.md:1 — `# CaseA207c — A2-07 blind cases` | (d) | Same pattern; actual heading at line 192 `## Files and URLs opened`. List exists. |
| 17 | CaseA207d.md:1 — `# CaseA207d — A2-07 blind cases` | (d) | Same pattern; actual heading at line 194 `## Opened files and source evidence`. List exists. |
| 18 | CaseA210a.md:1 — `# CaseA210a — A2-10 blind cases` | (d) | Same pattern; actual heading at line 203 `## Opened files and scope`. List exists. |
| 19 | CaseA210b.md:1 — `# CaseA210b — A2-10 blind cases` | (d) | Same pattern; actual heading at line 195 `## Files and URLs opened`. List exists. |
| 20 | CaseA210d.md:1 — `# A2-10 blind cases — CaseA210d` | (d) | Same pattern; actual heading at line 182 `## Opened files, source URLs, and evidence`. List exists. |

## Writer hits — actual files-opened headings and lists

For each of the 7 writer-named files, the check's `writer-missing-files-opened-list`
violation is a false positive: every file has a files-opened section with a genuine list,
but the heading phrasing does not match the strict `files_header_re` grammar.

- CaseA207a.md:192 `## Opened files and URLs` → list: `skill://godspeed` (SKILL.md); round-27 contract.md 40-80; round-26 contract.md 1-190; `tools/fixtures/mori-oom-killers/cases.json` and `cases-a2.json`; scratch `/fast/scratch/hyaku/mori-r29/CaseA207a/cases.json`; curl downloads (earlyoom main.c/kill.c/msg.h/MANPAGE.md, systemd.journal-fields.html) with hashes. Declares "I opened no `tools/mori-oom-killers.py`, no output from it, and no other report."
- CaseA207b.md:195 `## Files and URLs opened` → list: `skill://godspeed`; `/home/vgpnk/.omp/agent/RULES.md:1-14`; round-26 contract.md; round-27 contract.md 40-80; `cases.json`; `cases-a2.json`; scratch `main.c`, `kill.c`, `msg.h`, `MANPAGE.md`, `systemd.journal-fields.xml`, `cases-r29-a2-07.json`; curl fetches with hashes. Declares: opened no tool source, no tool output, no other report; "No round-29 contract, lesson, scorecard, or other report was opened."
- CaseA207c.md:192 `## Files and URLs opened` → list: SKILL.md, RULES.md; round-27 contract.md 40-80; round-26 contract.md 78-190; `cases.json`, `cases-a2.json`; scratch `main.c`, `kill.c`, `msg.h`, `MANPAGE.md`, `systemd.journal-fields.html`, `cases-a2-07-r29.json`; curl fetches with hashes. Declares: "I did not open or run `tools/mori-oom-killers.py`, inspect any of its output, or open any other report."
- CaseA207d.md:194 `## Opened files and source evidence` → `### Lane files`: round-27 contract.md 40-80; round-26 contract.md whole; `cases.json`; `cases-a2.json`; scratch `cases.json`. `### Upstream sources fetched with curl`: earlyoom main.c/kill.c/msg.h/MANPAGE.md, journalctl.html, journalctl.xml, systemd.journal-fields.xml with hashes/quotes. Declares: "I did not open or run `tools/mori-oom-killers.py`, did not view any of its output or a self-test, and opened no other report."
- CaseA210a.md:203 `## Opened files and scope` → list: `skill://godspeed`; round-27 contract.md 40-80; round-26 contract.md whole; `cases.json`; `cases-a2.json`; scratch `earlyoom-main.c`, `earlyoom-kill.c`, `earlyoom-msg.h`, `earlyoom-MANPAGE.md`, `systemd-journal-fields.xml`, `cases-a2-10.json`; public URLs above. Declares: "I opened no other report, no lessons, no SCORECARD, no LOG, and no other file under `.ufo/waves/` beyond the two named contracts"; "I did not open or run `tools/mori-oom-killers.py`, any copy of it, or its self-test; no output from that tool was read or copied."
- CaseA210b.md:195 `## Files and URLs opened` → list: SKILL.md; RULES.md; round-27 contract.md 40-80; round-26 contract.md whole; `cases.json`; `cases-a2.json`; scratch `main.c`, `kill.c`, `msg.h`, `MANPAGE.md`, `systemd.journal-fields.html`, `cases-a2-10.json`; five URLs in upstream table. Declares: "No tool implementation was opened or run, and no output from that tool was viewed. No other report was opened."
- CaseA210d.md:182 `## Opened files, source URLs, and evidence` → list: round-27 contract.md 40-80; round-26 contract.md 1-190; `cases.json` 1-8/6-44; `cases-a2.json` 1-11; RULES.md 1-14; SKILL.md; curl fetches (main.c, kill.c, msg.h, MANPAGE.md, systemd.journal-fields.html); scratch `main.c`, `kill.c`, `msg.h`, `systemd.journal-fields.html`, `cases-a2-10.json`. Declares: "I did not open or run `tools/mori-oom-killers.py`, did not view any of its output or a self-test, and opened no other report."

## Forbidden-path question

Did any writer's files-opened list name a forbidden path (the tool, another w1/w2 report,
or `corpus/lessons/`)? **No — none of the 7 lists name `tools/mori-oom-killers.py`
(or any copy of the tool), no other `w1/`/`w2/` report, and no `corpus/lessons/` file.**
The only fixture paths named are the frozen input data files `tools/fixtures/mori-oom-killers/cases.json`
and `cases-a2.json` (allowed fixture reads, each disclosed with a blindness risk note), and
each writer's own scratch scratch files. Every file affirmatively discloses that the tool
source and its output were not opened/read. (`report_ref_re` also matches none of the listed
paths: contracts are under `round-26/`/`round-27/`, not `w1/`/`w2/`.)

## Summary counts

| class | count |
|---|---|
| (a) tool source / tool-line citation | 0 |
| (b) output of a mori-oom-killers.py run | 0 |
| (c) writer report lacking files-opened list | 0 |
| (d) false positive | 20 |

All 20 hits are false positives. 13 are nonwriter-report lines where `repro_id_re`∧`result_re`
(10), the citation-grammar checks (3: `tool lines`/`selftest_marker`/`--inputs`+result in
the DraftQualityCriteria doc), or `cite_file_re` (1) matched ordinary prose, command echoes,
or the criteria document's self-description. 7 are writer-named case files that do have
files-opened lists whose heading wording (`## Opened files and URLs`, `## Files and URLs opened`,
`## Opened files and source evidence`, `## Opened files and scope`, `## Opened files, source URLs,
and evidence`) falls outside the strict `files_header_re` grammar.

Residual risk / verification gap: I verified hit-line content and every fired pattern against
the committed tree at `221cbd8f` (the rev the check ran), not at the current tip; the wave-2
reports in this directory were not opened (not needed for this adjudication). No source of
`tools/mori-oom-killers.py` was opened, per the assignment.
