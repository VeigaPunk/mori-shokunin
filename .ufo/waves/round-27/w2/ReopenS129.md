# ReopenS129 — SOURCES row S129 re-open at tip 5f00fd04

Seat: MoriR27.ReopenS129 (leaf; no subagent, no background job). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Assigned tip: `5f00fd045c137b7e3835506d69946cfd9d010eb5`. Entering tip: `fc09f96c`.
Lane HEAD moved to `47f6543a` during this run (four commits after the tip). Every verdict below is at the assigned tip; §8 records drift.
Scratch copies (tip bytes, both fetched XML files, tag API record): `/fast/scratch/hyaku/mori-r27/MoriR27.ReopenS129/`.

## 1. Summary

- Row S129 (`corpus/SOURCES.md:135`): identity, both sha256 values, both sizes, HTTP status, tag, commit, and all 15 line anchors **hold**. Not a duplicate row. No number in the row is wrong. The `teaches` cell has one unflagged inference (M2) and two wording defects (L1, L2).
- Round-27 Gate row (`corpus/lessons/round-27.md:72`): URL, quote and decision **hold**. The Gate row records no sha256. The wave-1 report it names (`.ufo/waves/round-27/w1/SrcSystemdExecOomScoreAdjust.md:32-33`) records both hashes, and they match the fresh downloads.
- Citing statements: 12 literal `S129` lines in 5 files (13 statements, because line 85 carries two), plus 4 dependent statements with no `S129` token. Result: 7 hold, 1 unsupported (M1), 1 mixed (the row itself, §3–5), 2 hypothetical (G1, G5), 1 holds as membership with an incomplete list (L3), and the rest wording (L5). §7 gives each verdict.
- Severity: high: none. Medium: M1, M2, M3, M4. Low: L1–L6.

## 2. Findings by severity (old → new)

### Medium

**M1. Entry says the systemd.exec(5) default describes the system manager only.** Unsupported.
- Where: `corpus/knowledge/oom-victim-selection-r27.md:85-86` at tip (HEAD `:79-80`; HEAD `:201-203` repeats it, about a tsukuroi file this seat did not open).
- Bytes: `systemd.exec.xml:1299-1300`: "If not specified, defaults to the OOM score adjustment level of the service manager itself, which is normally at 0." No manager type is named. No line in the OOM passages of `systemd.exec.xml` (1293–1305, 4890–4891, 4934–4937) says "system manager" (`grep -n -i 'system manager'` on the file, filtered to OOM lines, returns nothing).
- Origin: `.ufo/waves/round-27/w1/SrcSystemdExecOomScoreAdjust.md:56` (F3): "So for the system manager a unit with no `OOMScoreAdjust=` is at the manager's level…". A wave-1 inference that the entry adopted as fact.
- Old: `describes the system manager, not a user manager.`
- New: `is generic: it names no manager type. The unprivileged-manager default is S129 systemd-system.conf.xml:305-307. [INFERENCE] For units under a user manager, the two sentences disagree unless the manager-wide default governs the per-unit default; the pages do not say which.`

**M2. The `teaches` clause "so user units inherit manager+100 unless they set the value" is a derivation, presented as a reading of the bytes, and it conflicts with the row's own anchor `:1299-1300` without saying so.** Unsupported as stated.
- Where: `corpus/SOURCES.md:135`, `teaches` cell.
- What the bytes give: `systemd-system.conf.xml:305-307` (unprivileged default is the manager's value plus 100, with the parenthetical "makes service processes slightly more likely to be killed"); `:49-55` (the user instance reads `user.conf`); `:307-308` ("This may be used to pick a global default for the per-unit `OOMScoreAdjust=` setting"). Chaining these gives manager plus 100 for user units. Read literally, `systemd.exec.xml:1299-1300` gives the service manager's own level for an unset per-unit value, which for a user manager is not plus 100.
- Origin: `.ufo/waves/round-27/w1/SrcSystemdExecOomScoreAdjust.md:59` (F6) and `:61` (F8), which state the same chain as settled.
- Old: `so user units inherit manager+100 unless they set the value`
- New: `[INFERENCE] A user unit that leaves OOMScoreAdjust= unset gets, by the chain systemd-system.conf.xml:49-55 and :305-308, the unprivileged default (manager plus 100). systemd.exec.xml:1299-1300 says an unset per-unit value is the service manager's own level; the two pages do not reconcile them.`

**M3. The entry's recheck line omits the two S129 pages.**
- Where: `corpus/knowledge/oom-victim-selection-r27.md:3` (tip and HEAD).
- Old: `on a systemd release re-open `units/user@.service.in` and `src/core/main.c` `determine_default_oom_score_adjust``
- New: the same text, then `; on a systemd release also re-open `man/systemd.exec.xml` (OOMScoreAdjust=, :1293-1305) and `man/systemd-system.conf.xml` (DefaultOOMScoreAdjust=, :301-313) at the new tag`.
- Why: S129 is the only source for the "normally at 0" sentence and the unprivileged plus-100 sentence. A systemd release that changes either would not trigger this recheck line.

**M4. S114's `used-by` names the entry, but the entry never cites S114.** Found while checking G5, not in the S129 row.
- Where: `corpus/SOURCES.md:120` (S114 `used-by`), at tip and HEAD.
- Evidence: the entry contains 0 tokens `S114` at tip and HEAD (`S115` 7 tokens and `S118` 10 tokens at tip; both are cited, so their `used-by` entries are accurate).
- Old: `used-by: corpus/knowledge/userspace-oom-killers-r26.md, corpus/knowledge/oom-victim-selection-r27.md`
- New: `used-by: corpus/knowledge/userspace-oom-killers-r26.md` (drop the entry path), or cite S114 in the entry if it is in fact used.

### Low

**L1. `teaches` narrows the source.** Old `(normally 0 for the system manager)` → New `(normally at 0 for the service manager, systemd.exec.xml:1300)`. The bytes say "normally at 0" of "the service manager itself" with no manager type.

**L2. `teaches` clause "the setting never changes the manager's own score" is ambiguous, and read as the per-unit setting it is not in the bytes.** `systemd-system.conf.xml:310-311` says it of `DefaultOOMScoreAdjust=`. `systemd.exec.xml:1295-1300` says nothing about the manager's own value. Old `the setting never changes the manager's own score.` → New `DefaultOOMScoreAdjust= never changes the manager's own score (systemd-system.conf.xml:310-311).`

**L3. SKILL.md:722 grounding list is a subset of the entry's sources.** "Grounding for every row: … (sources S003, S118, S127, S129, S130, S132)". S129 membership holds. The entry's own source line (`entry:1`) also cites S082, S092, S115, S119, S120, S128 and S131, and SKILL.md:732 grounds a row on the cgroup document that is S092. Old: the six-id list → New: the thirteen ids of `entry:1`, or "sources: see entry line 1".

**L4. CriticC1Counter G5 (`.ufo/waves/round-27/w1/CriticC1Counter.md:59`) describes a renumbering that the tip does not contain.** S114, S115 and S118 keep their IDs and URLs (`SOURCES.md:120,121,124`), and S127–S129 are absent at fc09f96c (`git grep -c '^| S12[7-9] |'` = 0). The `used-by` append did happen (M4). The round-26 entry claim "cites S114 to S126" holds: `corpus/knowledge/userspace-oom-killers-r26.md:1` names S114 through S126 one by one. Presented as a hypothetical shape; no S129 change needed.

**L5. CriticC1Counter `:125` landing-form example separates ids with commas; the tip uses semicolons (`entry:1`).** Substance holds: one `source:` line (`grep -c '^source:'` = 1), line 2 is `verified-at:` (no wrap), S127, S128 and S129 each written out, no range. Wording only.

**L6. CriticC1Counter G1 (`:55`) is a hypothetical gaming shape** ("the three rows have 4 cells"). The tip rows have 11 cells (S129 has 12 pipes). No correction needed.

## 3. Anchor verdicts (row S129, tip)

Method: `grep -n -F` on the downloaded bytes for quoted lines; the read tool's numbered windows on the same bytes for the rest. Both files fetched with `curl -sS -L` (HTTP 200, 2026-10-22T17:09:38Z).

| Row anchor | Row says | Bytes (line: text, quotes ≤25 words) | Verdict |
|---|---|---|---|
| exec:1293 | term | 1293 `<term><varname>OOMScoreAdjust=</varname></term>` | holds |
| exec:1295-1296 | applies to executed processes | 1295 "Sets the adjustment value for the Linux kernel's Out-Of-Memory (OOM) killer score for" / 1296 "executed processes." | holds |
| exec:1296-1297 | range -1000..1000 and stated effects | 1296 "Takes an integer between -1000 (to disable OOM killing of processes of this unit)" / 1297 "and 1000 (to make killing of processes of this unit under memory pressure very likely)." | holds |
| exec:1299-1300 | unset → manager's own level, normally 0 | 1299 "If not specified, defaults to the OOM score adjustment level of the service manager itself," / 1300 "which is normally at 0." | holds |
| exec:1302-1305 | OOMPolicy cross-reference | 1302 "Use the OOMPolicy= setting of service units to configure how the service" … 1305 "for details." | holds |
| exec:4890-4891 | "problems during process invocation" | 4891 "used by the service manager to indicate problems during process invocation:" | holds |
| exec:4934-4938 | EXIT_OOM_ADJUST = 206 | 4934 `<row>`; 4935 `<entry>206</entry>`; 4936 `EXIT_OOM_ADJUST`; 4937 "Failed to adjust the OOM setting. See OOMScoreAdjust= above."; 4938 `</row>` | holds |
| conf:49-55 | system instance reads system.conf, user instance reads user.conf | 49 "When run as a system instance, systemd interprets the configuration file"; 51 "run as a user instance, it interprets the configuration file user.conf"; 55 "controlling basic manager operations." | holds |
| conf:301 | term | 301 `<term><varname>DefaultOOMScoreAdjust=</varname></term>` | holds |
| conf:303-304 | processes run by the manager | 303 "Configures the default OOM score adjustments of processes run by the service" | holds |
| conf:304-305 | unset → forked processes inherit manager's value | 304 "This defaults to unset (meaning the forked off processes inherit the service manager's OOM" / 305 "score adjustment value), except if the service manager is run for an unprivileged user, in which case" | holds |
| conf:305-307 | unprivileged → manager value plus 100 | 305 (above); 306 "this defaults to the service manager's OOM adjustment value plus 100 (this makes service processes" / 307 "slightly more likely to be killed under memory pressure than the manager itself)." | holds |
| conf:307-308 | global default for the per-unit setting | 307 "This may be used to" / 308 "pick a global default for the per-unit OOMScoreAdjust= setting." | holds |
| conf:310-311 | manager's own value kept | 310 "Note that this setting has no effect on the OOM score adjustment value of the service" / 311 "manager process itself, it retains the original value set during its invocation." | holds (for DefaultOOMScoreAdjust=; see L2) |
| conf:313 | "(v250)" | 313 `<xi:include href="version-info.xml" xpointer="v250"/>` | holds |

Quote verdicts:
- Gate quote (`round-27.md:72`): "if the service manager is run for an unprivileged user, in which case this defaults to the service manager's OOM adjustment value plus 100" = conf:305-306 joined across the wrap, verbatim, ASCII apostrophe (`grep -c` for typographic apostrophes = 0), 24 words. **Holds.**
- Entry quote "normally at 0" (`entry:85-86`) = exec:1300, verbatim. **Holds.**

## 4. Row-level verdicts

| Row claim | Check | Verdict |
|---|---|---|
| tag v262 = commit 8cc40e0c5e9234bf45084751ac53b1fbfe70b492 | `git ls-remote https://github.com/systemd/systemd.git refs/tags/v262 'refs/tags/v262^{}'` → `refs/tags/v262^{}` = 8cc40e0c… | holds |
| annotated tag 1f7dffaf714cc4488159c498b7a17cf34c5a96d5 | same `ls-remote`: `refs/tags/v262` = 1f7dffaf…; API `git/refs/tags/v262` object type `tag` | holds |
| tagger 2026-09-22T13:12:43Z | API `git/tags/1f7dffaf…` (saved `api-tag-v262.json`): `tagger.date` = 2026-09-22T13:12:43Z; `verification.verified` = true | holds |
| systemd.exec.xml 343,315 B; sha256 44b89bffce737aff803966c207329e9fe2d28ad07709a4bb8e0edf6a4ec0d844 | curl `size_download` 343315; `sha256sum` matches | holds |
| systemd-system.conf.xml 49,977 B; sha256 161359987affadc8e4a533bc9117bbbd98053cb807808b623eb24794b49b0c58 | curl `size_download` 49977; `sha256sum` matches | holds |
| HTTP 200 both | curl `-w %{http_code}` = 200 both | holds |
| access 2026-10-22T15:46:34Z (row and Gate) | historical; cannot be re-observed. The fetch at 17:09:38Z gives files whose sha256 equals the row's recorded values, and v262 is a tag | unverifiable; not contradicted |
| Gate hashes | `round-27.md:72` records none; the w1 report records both at `:32-33`, matching | holds |
| row `used-by` = the entry | `entry:1` and `:79` cite S129 | holds |
| row `opened` 2026-10-22, status mined, kind docs, tier A | consistent with the Gate row | holds |

## 5. Teaches and scope, clause by clause

| Clause (teaches cell) | Bytes | Verdict |
|---|---|---|
| "integer in -1000..1000" | exec:1296-1297 | holds |
| "applied to a unit's executed processes" | exec:1295-1296 | holds |
| "unset means the managing manager's own level" | exec:1299-1300 | holds |
| "(normally 0 for the system manager)" | exec:1300 says "normally at 0" of "the service manager"; no "system manager" in the text | narrowed (L1) |
| "for an unprivileged user manager the manager-wide default is that manager's value plus 100" | conf:303, conf:305-306 | holds |
| "so user units inherit manager+100 unless they set the value" | derived from conf:49-55 and :305-308; conflicts with exec:1299-1300 read literally | unflagged inference (M2) |
| "the setting never changes the manager's own score" | conf:310-311 says it of DefaultOOMScoreAdjust= only | unsupported for the per-unit setting; holds for the manager-wide one (L2) |

Scope cell, item by item: "per-unit range and its stated effects" (exec:1296-1297) holds; "per-unit default of the managing manager's own level" (exec:1299-1300) holds; "manager-wide default and its unset/inherit reading" (conf:303-305) holds; "unprivileged-user-manager default of manager value plus 100" (conf:305-306) holds; "the manager's own value is never rewritten" (conf:310-311) holds for DefaultOOMScoreAdjust=. The exclusions are fine. The scope is not wider than the bytes; the one non-OOM anchor (conf:49-55) is used only to say which manager reads the file.

## 6. Duplicate check

- No other SOURCES row cites `systemd.exec.xml` or `systemd-system.conf.xml`: `git grep -n -e 'systemd\.exec\.xml' -e 'systemd-system\.conf\.xml' 5f00fd04 -- corpus/SOURCES.md` matches only `:135`.
- Neither sha256 prefix (`44b89bff…`, `16135998…`) appears in `corpus/SOURCES.md` except at `:135`.
- At the entering tip fc09f96c there is no S127–S129 row and no literal `S129` (`git grep -n S129 fc09f96c` returns nothing).
- The same bytes were opened earlier in round 26 without a registry row: `.ufo/waves/round-26/w1/SrcEarlyoomUnit.md:220-221` and `.ufo/waves/round-26/w1/SrcJournalJson.md:28` record the same sha256 and sizes. Those are wave reports, not SOURCES rows, so S129 is the first registry row for these bytes. **Not a duplicate row.**
- Neighbours cite other v262 files (S120–S124, S133). S124 and S133 share a URL set (`SOURCES.md:130`, `:139`); see §10.

## 7. Citing statements

Literal `git grep -n 'S129' 5f00fd04`: 12 lines in 5 files (`CriticC1Counter.md` ×5, `SOURCES.md` ×2, entry ×3, SKILL ×1, lesson ×1). Dependent statements with no `S129` token are listed after the table.

| # | Location (tip) | Statement (short) | Verdict |
|---|---|---|---|
| S1 | `SOURCES.md:135` | the S129 row | anchors hold (§3–4); teaches: M2, L1, L2 |
| S2 | `SOURCES.md:136` (S130 row) | "the manual sentence is row S129" | **holds**: the unprivileged plus-100 sentence is `systemd-system.conf.xml:305-306`. The main.c and user@.service half of that row is S130's and is not checked here |
| S3 | `entry:1` | "S129 (systemd v262 systemd.exec.xml and systemd-system.conf.xml — OOMScoreAdjust= and DefaultOOMScoreAdjust=)" | **holds**: matches the row's source cell |
| S4 | `entry:79` heading | "(S129, S130, S127)" | **holds**: S129 supports `:85`, S130 supports `:81-84`, S127 supports `:92` |
| S5 | `entry:85` | "the manual sentence is S129 `systemd-system.conf.xml:305-306`" | **holds** (quote verified, §3) |
| S6 | `entry:85-86` | `"normally at 0" (S129 systemd.exec.xml:1299-1300) describes the system manager, not a user manager.` | quote and anchor **hold**; the restriction is **unsupported** (M1) |
| S7 | `SKILL.md:722` | "Grounding for every row: … (sources S003, S118, S127, S129, S130, S132)" | S129 membership **holds**; list incomplete (L3) |
| S8 | `round-27.md:72` (Gate row) | URL, quote `:305-306`, accessed 15:46:34Z, "admit, A, mined" | **holds**, except the access time is unverifiable (§4) |
| S9 | `CriticC1Counter.md:55` (G1) | hypothetical gaming shape, "entry is the single line `source: S127 S128 S129`" | hypothetical; not a claim about the tip (L6) |
| S10 | `CriticC1Counter.md:59` (G5) | renumbering of S114/S115/S118 to S127–S129, entry appended to `used-by`, round-26 entry cites S114 to S126 | renumbering **absent** at tip; `used-by` append **present** (M4 for S114; S115 and S118 accurate); round-26 range **holds** (L4) |
| S11 | `CriticC1Counter.md:79` (U5) | "source: S127–S129" → `new_rows_cited=2` (endpoints only); `SKILL.md:646` quote | **holds**: `SKILL.md:646` contains "sources S098–S104, S112–S113" verbatim; `count-c1.sh:21` regex `\bS[0-9]{3}\b` picks S127 and S129 and skips S128, so the count is 2 |
| S12 | `CriticC1Counter.md:125` (landing form) | one physical line, each id written out, no wrap, no second `source:` line | **holds** in substance (one `source:` line, line 2 is `verified-at:`); separator wording (L5) |
| S13 | `CriticC1Counter.md:126` | "no ranges (S127–S129 counts 2)" | **holds** (same counter behaviour as S11) |

Dependent statements with no `S129` token, resting on the M2 chain:
- D1 `entry:3` recheck line: omits the S129 pages (M3). **Incomplete.**
- D2 `entry:94-95`: "Every process a user unit starts … inherits 200 unless something writes a new value." **Unsupported as a bytes claim.** The 200 is host-observed evidence from wave-1 HostUnitOomAdjust, not S129; the per-unit rule for user units is the M2 inference. Not re-observed here.
- D3 `entry:160`: "descends from a user unit of an unprivileged user manager (100 + 100)". Same dependency; the 100 is from S130 (user@.service.in:35) and the plus-100 from S129 conf:305-306.
- D4 `SKILL.md:729`: "(manager 100, children 100 more)". Same dependency.

## 8. HEAD drift (`47f6543a`, four commits after the tip: `0becc42`, `b97b2e3`, `b89ac34`, `47f6543`)

- The S129 row (`SOURCES.md:135`) is byte-identical at tip and HEAD (sha256 of the line `2c3141c9…`). S130 row, SKILL.md:722 and the CriticC1Counter report are identical.
- The Gate row moved from `round-27.md:72` to `:71`, same text.
- Entry: S129 mentions now at `:1`, `:73`, `:79`. The M1 sentence is at `:79-80` and repeated at `:201-203`. M3 (recheck `:3`) is unchanged. M4 is unchanged (S114 `used-by` still names the entry; `S114` tokens in the entry = 0).
- D1–D4 were not re-checked at HEAD.

## 9. Residual risk and verification gaps

1. The row's and Gate's access time (2026-10-22T15:46:34Z) cannot be re-observed. Content identity is established by sha256 against my 17:09:38Z fetch, and the source is a tag.
2. Not checked: the S130 half of `SOURCES.md:136` (user@.service.in, main.c, commit ce7de0ba) and the rest of the entry, which are other rows' scope.
3. Not re-observed: the host values the wave-1 reports cite (oom_score_adj 200, DefaultOOMScoreAdjust 200). This seat ran no host reads and no probes.
4. Not checked individually: wave-1 quotes of the same S129 bytes that carry no `S129` token (`ConnSiblingOverlap.md:83-85`, `CriticC1Novelty.md:163`, `SrcSystemdUserService.md:45,68-69`). They repeat the M1 and M2 readings.
5. Not opened: `kill-event-deep-r8.md:142` (a tsukuroi file quoted at HEAD `entry:202`).
6. Documentation only. Whether systemd at runtime gives user units manager plus 100 was not tested.

## 10. Out of scope, noticed

- `SOURCES.md:130` (S124) and `:139` (S133) name the same v262 resource-control and systemd-oomd pages. The S133 gate says it "supersedes S124", but both rows remain. Not checked further.

## 11. Access record and tools

- Fetched by curl (ordinary means, no browser, no challenge bypass): `https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml` (HTTP 200, 343,315 B, 5,308 lines, sha256 `44b89bffce737aff803966c207329e9fe2d28ad07709a4bb8e0edf6a4ec0d844`, 2026-10-22T17:09:38Z); `https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-system.conf.xml` (HTTP 200, 49,977 B, 919 lines, sha256 `161359987affadc8e4a533bc9117bbbd98053cb807808b623eb24794b49b0c58`, 2026-10-22T17:09:38Z).
- API: `https://api.github.com/repos/systemd/systemd/git/refs/tags/v262` (2026-10-22T17:11:00Z) and `…/git/tags/1f7dffaf714cc4488159c498b7a17cf34c5a96d5` (2026-10-22T17:17:48Z).
- Git (read-only only: `show`, `grep`, `ls-remote`, `merge-base`, `diff`); `python3` and `sha256sum` for checks.
- Tools installed or upgraded: none. Everything used was already present.
- Lane edits: none. The only file written is this report, plus scratch under `/fast/scratch/hyaku/mori-r27/MoriR27.ReopenS129/`.
