# ReopenS133 — wave-2 re-open of SOURCES row S133 at tip 5f00fd04

- Seat: MoriR27.ReopenS133 (leaf; no subagents, no background jobs).
- Date: 2026-10-22. Tip: 5f00fd045c137b7e3835506d69946cfd9d010eb5 (master). Entering tip fc09f96c.
- Lane access: read-only git (show, grep, log, ls-tree) and one clone into scratch for a validator run.
- Scratch: /fast/scratch/hyaku/mori-r27/ReopenS133/ (fetched bytes, tip copies, outputs).

## 0. Verdict in brief

- Row S133 (corpus/SOURCES.md:139): both URLs return HTTP 200, both sha256 values match the row, and the tag is systemd 262. Anchors hold except one summary (A3) that is wider than the bytes. Two facts the teaching uses are in the bytes but not anchored (A6, A7). One teaches clause is not in the bytes (T5).
- S133 is a same-URL supersession of S124. The protocol and the validator allow that form. S124 stays `mined`, keeps a teaching the lane itself calls wrong, and has no marker (M2).
- The 14 lane lines that cite S133 (`git grep -n S133 5f00fd04`): 1 is the row; 3 hold (round-27.md:76, :99; userspace-oom-killers-r26.md:288-290); 2 are partly wrong (round-27.md:39, :108, both on QUALITY 81); 1 holds in substance but the entry's citation map is incomplete (userspace-oom-killers-r26.md:291); 7 are stale proposal ids in ReviewR7Knowledge.md.
- Adjacent finding that the S133 Gate relies on: QUALITY 81 is red at the landed tip (`changed=5`, exit 1). The lesson does not report that value, and its pointer "their disposition is recorded below" points to nothing (H1).

## 1. Fetch, hashes, tag

| Item | Result | Compared with | Verdict |
|---|---|---|---|
| man/systemd.resource-control.xml at v262 | HTTP 200; 110,159 bytes; sha256 d57641df40e45811403de91e55059b6a8f7506c6812a85cbe9c6ba22900587d8 | SOURCES:139 anchor records the same hash | holds |
| man/systemd-oomd.service.xml at v262 | HTTP 200; 8,348 bytes; sha256 4b29be2e41ef309beb9f9a9fcc9a84f18cd7f9f3540f094b0b5717891ef8651d | SOURCES:139 anchor records the same hash | holds |
| meson.version at v262 (tag identity) | reads `262`; sha256 1b8bdfb87f3d60549cc3e640a0cb99ea4001da5b24efd7b240b5f7cf170e14cc | not recorded in the row | "systemd 262 only" holds |

- The Gate entry (round-27.md:76) records no hash, so the row's anchor cell is the only hash record. Both match.
- My first fetch batch failed for a local reason: the scratch directory did not exist yet. The second attempt returned HTTP 200 for both files.
- Tools: curl, sha256sum (already present). No installs or upgrades.

## 2. Anchors (grep -n on the downloaded bytes)

| ID | Anchor as written | Bytes | Verdict |
|---|---|---|---|
| A1 | resource-control `:1545-1548` (auto: not actively used for monitoring; an ancestor set to kill can still make the unit a kill candidate) | :1545-1546 "When set to <option>auto</option>, <command>systemd-oomd</command> will not actively use this" / "cgroup's data for monitoring and detection. However, if an ancestor cgroup has one of these"; :1547-1548 "properties set to <option>kill</option>, a unit with <option>auto</option> can still be a candidate" / "for <command>systemd-oomd</command> to terminate." | holds |
| A2 | oomd `:44` (units set to kill are monitored) | :43-44 "Cgroups of units with ManagedOOMSwap= or" / "ManagedOOMMemoryPressure= set to kill will be monitored." | holds; cite :43-44 (L4) |
| A3 | oomd `:48-52` ("only descendant leaf cgroups, or cgroups with memory.oom.group=1, are candidates") | :48 "only descendant cgroups are eligible candidates for killing"; :50-51 "Also only leaf cgroups and cgroups with memory.oom.group set to 1 are eligible candidates" | locator holds; summary WRONG: it lets a non-descendant cgroup with oom.group=1 qualify (M4) |
| A4 | both sha256 values | §1 | holds |
| A5 | HTTP 200 on 2026-10-22 | §1 | holds |
| A6 | (not anchored) default `auto` | resource-control `:1527-1529` "Specifies how systemd-oomd.service will act on this unit's cgroups. Defaults to auto." | bytes support the teaching; the row cites no line (M5) |
| A7 | (not anchored) what kill means | resource-control `:1531-1535` "When set to kill, the unit becomes a candidate for monitoring by systemd-oomd" and "send SIGKILL to all of the processes under it"; oomd `:43-47` covers part | bytes support the scope; the row cites neither (L5) |
| A8 | (not anchored) "systemd 262" | meson.version = 262 | holds (L8) |

- The two ManagedOOM properties share one varlistentry (resource-control `:1522-1552`), so the auto paragraph at `:1545-1548` governs both. The row's "ManagedOOMSwap= / ManagedOOMMemoryPressure= auto" holds.
- Quote check: the lesson's `:1545-1546` quote matches the bytes only after the DocBook tags are removed (L3). Byte check: `grep -c` for the curly apostrophe returns 0, so the bytes use a straight apostrophe, as the quote does.

## 3. Teaches cell, clause by clause

Text (SOURCES:139, after "supersedes S124 —"): "On systemd 262 systemd-oomd monitors only cgroups of units set to kill; a unit left at the default auto is never monitored itself and becomes a kill candidate only under a kill ancestor, so an inactive or unconfigured oomd is unavailable evidence, not a quiet killer."

| Clause | Bytes | Verdict |
|---|---|---|
| T1 "monitors only cgroups of units set to kill" | oomd `:43-45`: kill-set cgroups "will be monitored"; systemd-oomd "polls PSI statistics for the system and those cgroups" | holds; "only" is [INFERENCE] (L1). The clause omits system-wide PSI polling (`:45`), which is not a cgroup, so no conflict. |
| T2 "a unit left at the default auto" | resource-control `:1529` "Defaults to auto" | holds (unanchored, M5) |
| T3 "is never monitored itself" | `:1545-1546` "will not actively use this cgroup's data for monitoring and detection" | holds; "never" is stronger than the bytes (L2) |
| T4 "becomes a kill candidate only under a kill ancestor" | `:1546-1548` (an ancestor set to kill makes an auto unit a candidate); oomd `:47-48` (candidates are descendants of the monitored cgroup) | holds by reading; "only" is inference from `:47-48` (L1) |
| T5 "so an inactive or unconfigured oomd is unavailable evidence, not a quiet killer" | Neither man page mentions an inactive or unconfigured oomd, evidence, or journal evidence. Check: `grep -n -i -E 'inactive|unconfigured|evidence|never|quiet|journal'` on both files returns no oomd or ManagedOOM sentence. This is mori's evidence policy stated as a systemd teaching. Its logic is also unclear: an inactive oomd runs nothing and cannot kill, so its silence would be informative, not "unavailable". | unsupported (M3) |

Scope cell (SOURCES:139):
- "what ManagedOOMSwap=/ManagedOOMMemoryPressure= auto and kill mean": holds (`:1523-1548`; oomd `:43-52`).
- "which cgroups systemd-oomd monitors": holds at oomd `:43-45`. Not wider than the bytes if read as the list at `:43-45`.
- "systemd 262 only": holds (§1).
- "not this host's unit values (tsukuroi-owned)": a boundary; holds. Shipped-unit check: units/user@.service.in at v262 (1,315 bytes) has no ManagedOOM line. Two other paths I tried (units/user-.slice.in, units/-.slice.in) returned 404. The row claims no shipped defaults.

## 4. Is S133 a duplicate of an older row's file?

- Literally yes. S133 cites the same two URLs as S124 (SOURCES:130). Its scope cell is byte-identical to S124's (checked with awk on field 5 of both rows).
- S124 cell history (diff of each commit's S124 cells): first published at 327fbcc (row md5 prefix ec4cec6f0cb7, 1,152 bytes). Round-26 commit 16935e2 (md5 prefix e6b22dc7eee7, 1,358 bytes) changed cells 5-7 (scope, anchor, teaches) and nothing else. Restored at 79ecf58; the tip equals 327fbcc. This matches round-27.md:97-98.
- Protocol: CORPUS Rule 2 (the kimi-shokunin protocol file, read-only, lines 116-118 as cited in ReviewS124Supersede.md:9-10) allows in-place change only to status, recheck and used-by. A correction is a new row whose teaches opens `supersedes S0NN —`. S133 uses that form.
- Validator: fleet-root `scripts/sources-census.sh` (read-only). I ran a copy against a scratch clone of the tip with `--root` and `--file`. `validate` exits 0 with `ok` and six W04 warnings, none on S124 or S133. E04 is not raised for S133 because its teaches contains "supersedes S124" (script `:648`). S124 is earlier in file order and is not flagged; the waiver is order-dependent (L7). `census` reports 141 rows: mined 99, queued 25, rejected 17.
- Precedent: same-URL supersessions already exist in the lane, with the old row left unmarked each time: S074 supersedes S071 (SOURCES:77, :80), S075 supersedes S070 (:76, :81), S076 supersedes S067 (:73, :82), and S073 narrows S069 (:75, :79). S087 and S088 supersede S083 and S084 but cite different files (:89-90, :93-94).
- Verdict: a protocol-compliant same-URL supersession. It follows established practice here. The residual risk is M2.
- S124's first-published teaching reads as "monitored" when an ancestor is kill. The bytes (`:1545-1548`) say an auto unit is never used for monitoring, even under a kill ancestor; it can only become a candidate. So S124 is wrong on exactly the point S133 corrects. The lane knows this (ReviewS124Supersede.md:168).

## 5. Citing statements (all 14 lines of `git grep -n S133 5f00fd04`)

| # | Location | Statement (short) | Verdict | Basis |
|---|---|---|---|---|
| 1 | corpus/SOURCES.md:139 | the row | see §2–§4; findings M1–M5, L1–L5 | |
| 2 | round-27.md:39 | "S124 restored to its first-published cells and corrected by new row S133 (`supersedes S124 —`); QUALITY 81 with the committed check" | partly wrong | Restoration holds (§4). The check exists. QUALITY.md:373-377 requires `changed=0`, exit 0; the landed tip prints `changed=5`, exit 1 (§6; H1). "Shown able to fail" holds: ef9dbee1 and fc09f96c print changed=6, exit 1 with S124 among them; bad_rev exits 2 (reproduced). |
| 3 | round-27.md:76 (Gate) | `:1545-1546` quote; "admit, A, mined — supersedes S124 —" | holds (wording) | The quote matches `:1545-1546` once DocBook tags are removed. Say "markup removed" (L3). The Gate records no hash, so there is nothing to compare. |
| 4 | round-27.md:99 | "The corrected teaching moved to S133. Status stays mined (the census accepts only queued, mined, rejected)" | holds | §4; validator `:4`, `:658-659`. The validator sits at the fleet root, not in the lane. |
| 5 | round-27.md:108 | "r26 D3 … fixed: S124 restored, S133 `supersedes S124 —`; M2 and QUALITY 81" | partly wrong | As line 2: QUALITY 81 is not met at tip (H1). |
| 6 | corpus/knowledge/userspace-oom-killers-r26.md:288-290 | "S124: its teaches, scope and anchor cells were restored to their first-published text (327fbcc); the corrected teaching … now lives in row S133, which opens `supersedes S124 —`" | holds | §4 verified. The quoted clause is faithful with the elision of "is never monitored itself and" (T3, T4). |
| 7 | userspace-oom-killers-r26.md:291 | "This entry's oomd statements rest on S133 as well as S124." | holds in substance; citation map incomplete (M1) | F8 (`:143-157`) states the auto default, the not-monitored point and the candidate-under-kill point; each matches `:1529` and `:1545-1548`. But the entry's `source:` line (`:1`) cites S124 and not S133 (count 0), and F8 names no row. |
| 8 | .ufo/waves/round-27/w1/ReviewR7Knowledge.md:25 | "the four oh-my-pi commits must renumber; next free id is **S133**" | stale id (L6) | True when written. S133 is now the systemd row (SOURCES:139). The four commits landed as S138–S141 (SOURCES:144–147). |
| 9 | ReviewR7Knowledge.md:55 | "NEW (holds; ids are proposals, next free S133)" | stale id (L6) | As line 8. |
| 10 | ReviewR7Knowledge.md:63 | "…moved 15 to 100 on 2026-02-26 (S133)" | stale id (L6) | The commit row is S138 (SOURCES:144). The content holds. |
| 11 | ReviewR7Knowledge.md:74 | "the entry's source: front-matter line adds S133–S136" | stale; implemented under other ids (L6) | harness-job-capacity-r25.md line 1 cites S138, S139, S140, S141 (`grep -o`). |
| 12 | ReviewR7Knowledge.md:75 | "the recheck: line's … gains S133–S136 once numbered" | stale; implemented (L6) | The entry's recheck line reads "…S138–S141". |
| 13 | ReviewR7Knowledge.md:151 | "## 4. Registry rows … next free S133" | stale id (L6) | As line 8. |
| 14 | ReviewR7Knowledge.md:157 | "| S133 | oh-my-pi commit 944d7f8d…" (proposal row) | stale id (L6) | The landed row is S138 (SOURCES:144). The proposal ids S133–S136 also collided with the landed S134–S136 (SOURCES:140–142). The report has no renumber note (`grep -n renumber` finds only :25). |

Counts: holds 3 (lines 3, 4, 6); partly wrong 2 (lines 2, 5); holds in substance with an incomplete citation map 1 (line 7); stale ids 7 (lines 8–14); the row itself 1 (line 1).

## 6. Adjacent finding that the S133 Gate relies on: QUALITY 81 at the tip

Command: `python3 -I -B check-row-identity.py <rev>` (the committed script, run from a scratch copy; reads the lane through read-only git).

- 5f00fd04: `changed S090 cells=anchor,teaches`, `changed S093 cells=anchor`, `changed S096 cells=teaches`, `changed S097 cells=anchor,teaches`, `changed S101 cells=teaches`, `rows=141 changed=5`, exit 1.
- fc09f96c and ef9dbee1: the same five plus `changed S124 cells=scope,anchor,teaches`, `rows=126 changed=6`, exit 1.
- bad_rev: `bad_rev`, exit 2.
- QUALITY.md:373-377: "Check: … must print `changed=0`, exit 0."
- S124 is no longer among the changed rows at the tip, so the S124 restoration itself holds.
- round-27.md:41-42 says the five rows "are routed to wave 2 … their disposition is recorded below". `grep -n` for S090 and S101 in the lesson finds only :35-36 and :41. No disposition is recorded.

## 7. Findings, by severity

### HIGH

**H1. QUALITY 81 is unmet at the landed tip, and the lesson does not say so.** Evidence: §6. The lesson's M2 block (round-27.md:33-42) reports only the earlier values (changed=6) and cites "QUALITY 81 with the committed check" as the fix. Correction: in round-27.md:35-42 state "at 5f00fd04 the check prints changed=5, exit 1 (S090, S093, S096, S097, S101); QUALITY 81 is open until it exits 0". Either record the real disposition for each of the five rows or remove "recorded below". Do not describe QUALITY 81 as a closed fix until the check exits 0.

### MEDIUM

**M1. The entry's citation map omits S133.** Evidence: userspace-oom-killers-r26.md:1 lists S114–S126 and S137; the string S133 appears only at :290–291. SOURCES:139 lists this entry as used-by. Correction: add S133 to the `source:` line at :1. The wave-1 seat recommended this citation flip (ReviewS124Supersede.md:153-156); it was not applied.

**M2. S124 keeps a wrong teaching with no marker.** Evidence: SOURCES:130 says an auto unit "is not monitored by systemd-oomd unless an ancestor is kill", which reads as monitored under a kill ancestor. The bytes (`:1545-1548`) say otherwise. The lane's own wave-1 report agrees that the restored text is wrong (ReviewS124Supersede.md:168). Within the protocol, status cannot be `superseded` (validator E07) and only status, recheck and used-by may change in place. The same pattern leaves S067, S069, S070 and S071 unmarked (§4). Correction: none is possible in S124 without breaking Rule 2. The mitigation is M1, so that the entry's source line points readers to S133. Residual risk: a reader who opens S124 first gets the wrong monitoring statement. Severity medium; high impact if read alone.

**M3. The last teaches clause is not in the bytes.** Evidence: T5 (§3). Correction: delete "so an inactive or unconfigured oomd is unavailable evidence, not a quiet killer." from SOURCES:139. If mori needs that policy, state it in the entry, labelled [INFERENCE], with its reasoning.

**M4. The `:48-52` summary is wider than the bytes.** Evidence: A3. Correction for SOURCES:139: replace "(only descendant leaf cgroups, or cgroups with `memory.oom.group=1`, are candidates)" with "(only descendant cgroups are eligible candidates; of those, only leaf cgroups and cgroups with `memory.oom.group=1`)".

**M5. The default `auto` that the teaching uses is not anchored.** Evidence: A6 (resource-control `:1527-1529`). Correction for SOURCES:139: add "systemd.resource-control.xml:1527-1529 (default `auto`)" to the anchor cell.

### LOW

- **L1.** "only" appears in T1 and T4 but not in the bytes. Mark it [INFERENCE], or cite oomd `:47-48` for T4.
- **L2.** "never monitored itself" (T3). Use the bytes' wording: "will not actively use this cgroup's data for monitoring and detection".
- **L3.** The Gate quote at round-27.md:76 drops `<option>` and `<command>` tags. Say "markup removed".
- **L4.** A2 cites `:44`; the sentence starts at `:43`. Cite `:43-44`.
- **L5.** resource-control `:1531-1535` (the kill meaning) is not anchored; oomd `:43-47` covers part of it. Add the range if the scope's kill claim should rest on the resource-control page.
- **L6.** ReviewR7Knowledge.md:25, :55, :63, :74, :75, :151, :157 use S133–S136 for proposals that landed as S138–S141. Add a dated note that the ids were renumbered at landing.
- **L7.** (Validator, informational, not an S133 defect.) The E04 waiver matches "supersedes S###" anywhere in a teaches cell (script `:648`), and the check is order-dependent: if S133 came before S124, S124 would be flagged.
- **L8.** (Informational.) "systemd 262" has no anchor on meson.version; the tag in the URL carries it.

## 8. Residual risk and verification gaps

- Other lane statements that teach S133's content without citing S133 were not enumerated, apart from entry F8, which was checked. SKILL.md and README rows that mention oomd were not read.
- Shipped unit files: only units/user@.service.in was checked. The row claims no shipped defaults, so this is informational.
- ReviewS124Supersede.md "Draft (b)" cells were not compared with the 16935e2 to tip diff. The S124 cell diff was done directly (cells 5–7 changed at 16935e2).
- The validator ran from a scratch copy against a scratch clone of the tip, not in the fleet root or the lane.
- The identity check ran only at the revisions listed in §6.
- Upstream bytes are tag-pinned; the hashes matched on 2026-10-22.

## 9. Tooling and privacy

- Installs or upgrades: none. Tools used, all already present: curl, sha256sum, md5sum, git (read-only in the lane; one clone into scratch for the validator run), python3 (committed check run from a scratch copy), bash, awk, grep, sed. No pacman transaction.
- Writes: this report and /fast/scratch/hyaku/mori-r27/ReopenS133/ only. No git write ran in the lane.
- Privacy: no uid, pid, session identifier, process command line, journal text or settings value appears here. The entry's F8 host observations are not repeated.
