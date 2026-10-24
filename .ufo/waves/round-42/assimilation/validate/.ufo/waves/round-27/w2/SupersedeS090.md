# Round 27, wave 2: SupersedeS090 (seat MoriR27.SupersedeS090)

Routed by the row-identity check (QUALITY 81, `.ufo/waves/round-27/check-row-identity.py`): row S090 in `corpus/SOURCES.md` changed in place after its first publication at df4db54. Read-only seat. The only lane write is this file. Scratch: `/fast/scratch/hyaku/mori-r27/SupersedeS090/`.

Commits: first published `df4db54` ("round-24: sources S090-S097 ..."); in-place change `a730ecf` ("round-24: wave-1 seat reports, S090 wording correction, contract amendment A5"); tip `5f00fd045c137b7e3835506d69946cfd9d010eb5`. The S090 row at `a730ecf` equals the tip in every cell. All analysis used committed bytes (`git archive` of the tip), not the working tree.

**Bottom line.** Against psi.rst, both changed cells are closer to the tip wording. The tip teaches still holds two clauses the bytes do not support: "so a zero full value carries no information" (an inference), and the window clause read as v7.2 behaviour (the document states it; the kernel does not enforce the 500 ms floor). The new row S142 carries the corrected teaches and attributes the window statement to the document.

## 1. Cell-level old and new

Cells that differ: `anchor` and `teaches`. Cells equal at df4db54 and tip: id, source, kind, tier, scope, status, opened, recheck, used-by.

Word-level changes (difflib over the two cells, no other word differs):
- anchor: `undefined and zeroed` becomes `undefined, reported as zero`
- teaches: `each file is exactly two lines,` becomes `each named file (cpu, memory, io) shows a some line and a full line,`

Full anchor cells (both continue with the same pins, ending `pressure interface heading:34-35; ... cgroup2 file set:181-185; tag v7.2; sha256 11c6b7129103b454`):

```
df4db54: system CPU full undefined and zeroed since 5.13:57-58
tip:     system CPU full undefined, reported as zero since 5.13:57-58
```

Full teaches, df4db54 (the tip text is this text with the first change above):

```
The document names only cpu, memory and io as the /proc/pressure/ files; each file is exactly two lines, some for time in which at least some tasks are stalled and full for time in which all non-idle tasks are stalled; avg10/60/300 are percentages over 10/60/300-second windows and total is absolute stall time in microseconds; system-level CPU full is undefined and exported as zero since 5.13, so a zero full value carries no information; trigger windows are accepted from 500ms to 10s, so the minimum monitoring update interval is 50ms and the maximum 1s.
```

## 2. Source re-opened today

- URL: https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst (HTTP 200, 6792 bytes, 188 lines).
- Accessed: 2026-10-22T17:10:26Z (`curl -sS -L`, ordinary GET).
- sha256: `11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692`. The row digest `11c6b7129103b454` matches.
- Line pins (`grep -n` on the fetched bytes, `psi-v7.2.rst` in scratch):
  - 34-35 heading. 37-38: "Pressure information for each resource is exported through the" / "respective file in /proc/pressure/ -- cpu, memory, and io."
  - 40-43 format block; 42-43 are the `some` and `full` lines.
  - 45-46 `some` meaning; 48-49 `full` meaning.
  - 57-58: "CPU full is undefined at the system level, but has been reported" / "since 5.13, so it is set to zero for backward compatibility."
  - 60-63 ratios in percent and total in microseconds.
  - 81-88 trigger format and examples; 102-103 window bounds; 118-119 trigger lifetime; 181-185 cgroup2 file set.
  - The word `irq` never occurs in the file. The words `exactly` and `two lines` never occur.

Clause by clause, tip teaches (df4db54 differs only where noted):

1. "names only cpu, memory and io as the /proc/pressure/ files": holds (37-38; no other resource is named).
2. "each named file (cpu, memory, io) shows a some line and a full line": holds (37-38 with the format block 40-43). The df4db54 wording "each file is exactly two lines" is loose: "exactly" is not in the document, and the format block shows two lines (42-43). Low.
3. The `some` and `full` meanings (45-49): hold.
4. avg10/60/300 as percentages over 10/60/300-second windows, and total in microseconds (60-63): hold.
5. "system-level CPU full is undefined and exported as zero since 5.13" (57-58): holds in substance. The document says CPU full "has been reported since 5.13, so it is set to zero". The df4db54 anchor "undefined and zeroed since 5.13" dates the zeroing, which the document does not do. Low (wording). The tip wording "reported as zero since 5.13" follows the document.
6. "so a zero full value carries no information": not in the document. It is an inference from "undefined" (57). [INFERENCE] Low. S142 drops it.
7. "trigger windows are accepted from 500ms to 10s, so the minimum monitoring update interval is 50ms and the maximum 1s": true as the document's statement (102-103: "The kernel accepts window sizes ranging from 500ms to 10s, therefore min monitoring update interval is 50ms and max is 1s."). Wrong as v7.2 kernel behaviour. The kernel source at tag v7.2 (`kernel/sched/psi.c`, fetched 2026-10-22T17:14:35Z, 48859 bytes, sha256 `452318beaca3e6d19ab81a16528ae6b1695828a9ed080e329d07dedd9a3312c5`, the S091 digest) defines `WINDOW_MAX_US 10000000` (psi.c:167) and rejects only `window_us == 0 || window_us > WINDOW_MAX_US` (psi.c:1372). Unprivileged writers need a multiple of 2 s (psi.c:1379). `WINDOW_MIN_US` does not exist in the file. The knowledge entry already records the difference (`corpus/knowledge/system-pressure-r24.md:22-24`, K6). Severity high as written: the row scope names "window bounds", and a reader could take the 500 ms floor as enforced. S142 attributes the statement to the document.

Which text the bytes support:
- anchor: the tip wording (psi.rst:57-58).
- teaches: the tip's first clause is supported and the df4db54 "exactly two lines" is not. Neither text is fully supported, because clauses 6 and 7 remain. The text in S142 is the one the bytes support.

## 3. Ready-to-paste lines

(a) Restored first-published row. Byte-identical to the df4db54 S090 line (`cmp` in scratch). Status, recheck and used-by are unchanged from df4db54.

```text
| S090 | Linux PSI accounting documentation v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst | docs | A | the v7.2 system PSI interface only: the /proc/pressure/ file set the document names, the some/full line grammar, the unit and window semantics of avg10/avg60/avg300 and total, the system-level CPU full rule, and the trigger format and window bounds; v7.2 only | pressure interface heading:34-35; documented file set:37-38; line format:40-43; some meaning:45-46; full meaning:48-55; system CPU full undefined and zeroed since 5.13:57-58; avg windows and total unit:60-65; trigger format and examples:81-88; trigger window bounds:102-110; trigger lifetime:118-119; cgroup2 file set:181-185; tag v7.2; sha256 11c6b7129103b454 | The document names only cpu, memory and io as the /proc/pressure/ files; each file is exactly two lines, some for time in which at least some tasks are stalled and full for time in which all non-idle tasks are stalled; avg10/60/300 are percentages over 10/60/300-second windows and total is absolute stall time in microseconds; system-level CPU full is undefined and exported as zero since 5.13, so a zero full value carries no information; trigger windows are accepted from 500ms to 10s, so the minimum monitoring update interval is 50ms and the maximum 1s. | mined | 2026-10-22 | on-release | corpus/knowledge/system-pressure-r24.md, corpus/lessons/round-24.md |
```

(b) New row S142. Teaches opens `supersedes S090 — `. Scope is identical to S090, so the duplicate-URL rule (E04) is the one in play, and the `supersedes S090 —` prefix satisfies it (section 4). Status mined, opened 2026-10-22, recheck as the original (on-release). Used-by names the two files that cite the corrected psi.rst facts.

```text
| S142 | Linux PSI accounting documentation v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst | docs | A | the v7.2 system PSI interface only: the /proc/pressure/ file set the document names, the some/full line grammar, the unit and window semantics of avg10/avg60/avg300 and total, the system-level CPU full rule, and the trigger format and window bounds; v7.2 only | pressure interface heading:34-35; documented file set:37-38; line format:40-43; some meaning:45-46; full meaning:48-55; system CPU full undefined, reported as zero since 5.13:57-58; avg windows and total unit:60-65; trigger format and examples:81-88; trigger window bounds:102-110; trigger lifetime:118-119; cgroup2 file set:181-185; tag v7.2; sha256 11c6b7129103b454 | supersedes S090 — The document names only cpu, memory and io as the /proc/pressure/ files; each named file (cpu, memory, io) shows a some line and a full line, some for time in which at least some tasks are stalled and full for time in which all non-idle tasks are stalled; avg10/60/300 are percentages over 10/60/300-second windows and total is absolute stall time in microseconds; system-level CPU full is undefined and reported as zero since 5.13 for backward compatibility; the document states that the kernel accepts window sizes from 500ms to 10s, so the minimum monitoring update interval is 50ms and the maximum 1s. | mined | 2026-10-22 | on-release | corpus/knowledge/system-pressure-r24.md, corpus/lessons/round-24.md |
```

Paste position: replace line 96 (the S090 row) with (a). Insert (b) after line 147 (the S141 row, inside the Registry table, before the blank line and `## Paths`). Nothing else changes.

Gate (S142): URL https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst; accessed 2026-10-22T17:10:26Z; sha256 11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692. Located quotes: psi.rst:57-58 "CPU full is undefined at the system level, but has been reported since 5.13, so it is set to zero for backward compatibility." (23 words). psi.rst:102-103 "The kernel accepts window sizes ranging from 500ms to 10s, therefore min monitoring update interval is 50ms and max is 1s." (21 words).

Used-by evidence: `corpus/knowledge/system-pressure-r24.md` cites psi.rst for F1-F3 (lines 63-87), K6 (22-24) and its pointer line (61). `corpus/lessons/round-24.md` cites S090 at line 25 (quoting 57-58) and logs the anchor and teaches change at lines 50-54. Precedent: S133's used-by names its citing knowledge entry.

## 4. Census validate on a scratch copy

How the script finds the lane:
- The default root is the parent of the script's directory (`scripts/sources-census.sh:88`). `--root DIR` overrides it (`:74`).
- `build_roster` reads `$ROOT/shokunin.conf` (`:452-455`), takes the repo column of each LANES row (`:470`), and reads `$ROOT/<repo>/corpus/SOURCES.md` (`:467`). The conf row for this lane is line 63: `mori|mori-shokunin|...`, so `mori` resolves to `$ROOT/mori-shokunin`. Any other `*-shokunin` directory is added as an "unlisted" lane (`:472-485`).
- With `--root <scratch>`, the lane is the scratch copy. The output prints that path.

Scratch build: `root-tip/` holds the fleet `shokunin.conf` (copied) and `git archive 5f00fd0` extracted as `mori-shokunin/`. `root-applied/` is a copy of root-tip with the two lines applied through the edit tool. Checks: the S090 line is byte-identical to df4db54 (`cmp`); the S142 line is identical to the generated line (`cmp`); `diff` against the tip shows exactly two hunks (line 96 replaced, one row added after line 147); 142 rows; one S090; one S142.

Commands and results:
- `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /fast/scratch/hyaku/mori-r27/SupersedeS090/root-applied mori` gives **exit 0**. Output: W04 lines for S035, S037, S073, S074, S075, S076 (same as baseline), then `mori ok`.
- Baseline: the same command on `root-tip` gives exit 0 with the same output. The tip's in-place S090 change therefore validates clean; the census does not check row identity.
- Negative control on `root-neg` (root-applied plus a row S999 with S090's URL and scope and no supersedes prefix): `mori E04 S999 duplicate url ... within scope ...`, **exit 1**. So the exit 0 on root-applied comes from the E04 exemption, which S142 meets with `supersedes S090 —`.

Row-identity check, read-only run on the committed tip: `changed=5` for S090 (anchor, teaches), S093 (anchor), S096 (teaches), S097 (anchor, teaches) and S101 (teaches); `removed=0 bad=0`; exit 1. After the paste S090 should leave the list. [INFERENCE] The check's LANE path is fixed to the live lane, so it was not run on a candidate commit. Expected count after the paste: changed=4.

## 5. Findings

- HIGH. S090 teaches, window clause (tip and df4db54). The document's statement is recorded as v7.2 kernel behaviour, and psi.c v7.2 does not enforce the 500 ms floor (psi.c:167, 1372; no `WINDOW_MIN_US`). Correction: S142 attributes the statement to psi.rst:102-103. The knowledge entry (K6, lines 22-24) already says so.
- LOW. S090 anchor (df4db54) "undefined and zeroed since 5.13" dates the zeroing. The document dates the reporting (57-58). Tip wording is supported.
- LOW. S090 teaches (df4db54) "each file is exactly two lines": "exactly" is not in the document, and the format block shows two lines (42-43). Tip wording is supported.
- LOW. S090 teaches (both texts) "so a zero full value carries no information": [INFERENCE] from "undefined" (57). The document does not say it. S142 omits it.
- PROCESS. The in-place change at `a730ecf` was logged (`corpus/lessons/round-24.md:50-54`), but CORPUS.md Rule 2 requires a new row for a correction. S142 is that row. The restored line reverts the in-place edit, and the round-27 lesson's M2 entry should record both.

## 6. Notes for the integrator (not done here)

- Paste (a) at line 96 and (b) after line 147. Record the revert and S142 in the round-27 lesson's M2 disposition.
- Optional: the knowledge entry's source line (line 1) and pointer (line 61), and the round-24 lesson's Gate row, still name S090 for the psi.rst facts. Add S142 there if the used-by claim should read literally. The census does not require it.
- SKILL.md cites S090 facts at line 619 and in the round-24 table rows at 625-633. SKILL.md is not a used-by path under CORPUS.md, which defines used-by as knowledge entries or lessons.
- The lane working tree was dirty during this run: uncommitted changes to SKILL.md and `corpus/knowledge/oom-victim-selection-r27.md`, and untracked `.scratch/` and `.ufo/waves/round-27/w2/`. This seat read committed bytes only.
- The row-identity script changed in the working tree during this run. The first read printed `rows` and `changed` only. The run used for the count printed `removed` and `bad` too. The committed-tip count is 5 either way.

## 7. Tools and bounds

- Tools used: curl (ordinary HTTPS GET), sha256sum, git (read-only: show, log, archive, cat-file; one `git status --porcelain` in the lane without GIT_OPTIONAL_LOCKS=0, which may refresh `.git/index` stat data but changes no content), tar, cp, cmp, gawk 5.4.1 (`/usr/bin/gawk`, present; used by the census), python3 (`-I -B`, the row-identity check).
- Installed or updated: nothing. No pacman, uv, npm or cargo operation ran.
- One wide bash grep over the lane (including `.ufo`) ran past 60 s and moved to a background job (bg_11028). It completed. Its output was discarded and it wrote nothing.
- No subagents. No background job left running. No git write. No lane write except this file.
