# SupersedeS093 — S093 changed in place: cell diff, bytes verdict, paste lines, census

seat: MoriR27.SupersedeS093 (leaf; no subagents; no background jobs)
lane: /home/vgpnk/Projects/shokunin/mori-shokunin
named tip: 5f00fd045c137b7e3835506d69946cfd9d010eb5 (examined)
lane master now: 47f6543a (HEAD). Commits after the tip: 0becc42, b97b2e3, b89ac34, 47f6543. The tip is an ancestor (`git merge-base --is-ancestor`, rc=0). The S093 row is identical at tip and master (python cell compare: True).
scratch: /fast/scratch/hyaku/mori-r27/SupersedeS093/ (no lane writes; one clone under scratch; commits only in that clone)

## 0. Summary

- One cell changed in place: the S093 anchor. The row was first published at df4db54 (`git show df4db54:corpus/SOURCES.md`, line 99). The first first-parent commit whose tree carries `| S093 |` is df4db54 (`grep -c`: 1). The in-place change is 7c77fba (2026-10-22 06:11:03 -0300, "round-24: wave-2 source corrections (S093 anchor, S096 teaches, S097 cells)"). Comparing 7c77fba's parent with 7c77fba, the S093 row differs only in the anchor.
- The bytes support `730-731` for the help-text file list. The old `730-733` is too wide under its own label: lines 732-733 are the next sentence and name no file. Severity: low for the span (over-broad, not false). Medium for the protocol breach: CORPUS.md Rules 2 allows in-place change only to status, recheck and used-by.
- Restored line: the df4db54 row verbatim (section 3). New row: S143, not S142. S142 is taken on master by b89ac34 (`oh-my-pi task/executor.ts`).
- Census (step 4), on the scratch copy with the two lines applied: `validate --root <scratch> mori` exits 0. Control copy (the same new row without `supersedes S093 — `): exit 1, E04 on S143.
- Row-identity check (QUALITY 81) in a scratch clone with the two lines committed: S093 is no longer listed. Four other rows (S090, S096, S097, S101) stay listed; they are outside this item.

## 1. Cell-level old (first-published) and new (tip)

Split on ` | ` after stripping the outer pipes; 11 cells per row. The only differing cell is column 6 (anchor). Compared: df4db54 vs tip 5f00fd04, df4db54 vs master 47f6543a, and 7c77fba's parent vs 7c77fba. Each gives `['anchor']`.

- old, df4db54 line 99, anchor: `CONFIG_PSI:723-741 (help-text file list:730-733, cgroup2 text:735-737); CONFIG_PSI_DEFAULT_DISABLED:743-760 (psi=1 text:748-750); CONFIG_IRQ_TIME_ACCOUNTING:615-624; tag v7.2; sha256 a43f09d89309a6bd`
- new, tip 5f00fd04 line 99 and master line 99, anchor: identical except `help-text file list:730-731`.
- Unchanged cells (identical at df4db54, tip and master): id `S093`; source `Linux PSI and IRQ time accounting Kconfig at v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/init/Kconfig`; kind `code`; tier `A`; scope (the CONFIG_PSI, CONFIG_PSI_DEFAULT_DISABLED and CONFIG_IRQ_TIME_ACCOUNTING build options ... v7.2 only); teaches; status `mined`; opened `2026-10-22`; recheck `on-release`; used-by `corpus/knowledge/system-pressure-r24.md, corpus/lessons/round-24.md`.
- The same commit family also changed S096 and S097 (the 7c77fba subject names them). Those are outside this item.

## 2. Source re-opened today

- URL: https://raw.githubusercontent.com/torvalds/linux/v7.2/init/Kconfig
- Access: 2026-10-22T17:10:28Z. `curl -sS -L`, HTTP 200, 74156 bytes, final URL unchanged, 2321 lines.
- sha256: a43f09d89309a6bd7036c96e0836c30c021f2d56b042be288a15533dd9e944bd. The row's pin `a43f09d89309a6bd` is its prefix. That supports, but does not prove, identity with the first-published bytes [INFERENCE].
- `grep -n` pins on the downloaded file (`kconfig-v7.2.txt` under scratch):
  - 615 `config IRQ_TIME_ACCOUNTING`; 616 `bool "Fine granularity task level IRQ time accounting"`; 619 `Select this option to enable fine granularity task irq time`; 624 `If in doubt, say N here.`
  - 723 `config PSI`; 730 `If you say Y here, the kernel will create /proc/pressure/ with the`; 731 `pressure statistics files cpu, memory, and io. These will indicate`; 732 `the share of walltime in which some or all tasks in the system are`; 733 `delayed due to contention of the respective resource.`; 735 `In kernels with cgroup support, cgroups (cgroup2 only) will`; 736 `have cpu.pressure, memory.pressure, and io.pressure files,`; 739 `For more details see Documentation/accounting/psi.rst.`; 741 `Say N if unsure.`
  - 743 `config PSI_DEFAULT_DISABLED`; 748 `If set, pressure stall information tracking will be disabled`; 749 `per default but can be enabled through passing psi=1 on the`; 750 `kernel commandline during boot.`; 759 `used for, say Y.`; 760 blank; 761 `Say N if unsure.`; 763 `endmenu`
- Located quote, file list, lines 730-731 (19 words): "If you say Y here, the kernel will create /proc/pressure/ with the pressure statistics files cpu, memory, and io."
- Located quote, the old span's extra lines, 732-733 (22 words): "the share of walltime in which some or all tasks in the system are delayed due to contention of the respective resource."

Which text the bytes support: `730-731`. The file list (`/proc/pressure/` at 730, `cpu, memory, and io` at 731) occupies exactly those two lines. Lines 732-733 describe the walltime share and name no file. The first-published `730-733` is therefore too wide under the label "help-text file list". The tip's `730-731` is the supported text. The round-24 lesson already logs this correction (`corpus/lessons/round-24.md:48-49`), and the round-24 wave-2 seat suggested it (`.ufo/waves/round-24/w2/ReopenS092S093.md:97-100`).

### Claim-by-claim verdicts (every S093 claim, against the bytes in section 2)

| # | statement (cell) | bytes | verdict | severity |
|---|---|---|---|---|
| 1 | anchor `help-text file list:730-733` (df4db54) | list is 730-731; 732-733 name no file | wrong span: correction `730-731` | low |
| 2 | anchor `help-text file list:730-731` (tip, master) | lines 730-731 | holds | - |
| 3 | anchor `CONFIG_PSI:723-741` | 723 config; 741 `Say N if unsure.` | holds | - |
| 4 | anchor `cgroup2 text:735-737` | 735-736 name cgroup2 files; 737 holds the aggregation sentence | holds | - |
| 5 | anchor `CONFIG_PSI_DEFAULT_DISABLED:743-760` | block is 743-761; substantive help ends at 759; 761 `Say N if unsure.` is outside the range | holds for substance; optional widen to `743-761` | low |
| 6 | anchor `psi=1 text:748-750` | 748-750 | holds | - |
| 7 | anchor `CONFIG_IRQ_TIME_ACCOUNTING:615-624` | 615-624 block; 624 `If in doubt, say N here.` | holds | - |
| 8 | anchor `sha256 a43f09d89309a6bd` | digest a43f09d8...944bd | holds as a prefix | - |
| 9 | teaches: help text names only cpu, memory, io under /proc/pressure/ plus the cgroup2 per-cgroup files | 730-731; 736 names `cpu.pressure`, `memory.pressure`, `io.pressure` | holds. Wording: the help text also cites `psi.rst` (739), a doc path, so `only` means only pressure files | low (wording) |
| 10 | teaches: PSI_DEFAULT_DISABLED leaves tracking disabled unless psi=1 is passed on the kernel commandline | 748-750 | holds | - |
| 11 | teaches: IRQ_TIME_ACCOUNTING is a separate fine-granularity task irq time option | 616, 619 | holds | - |
| 12 | scope: "the psi=1 opt-in that overrides CONFIG_PSI_DEFAULT_DISABLED" | help text says tracking "can be enabled through passing psi=1" (749-750); `overrides` is the row's own word | holds in substance [INFERENCE on the wording] | low (wording) |
| 13 | source: tag v7.2 | not re-verified here; the ReopenS127 seat checks the v7.2 tag | gap | - |

## 3. Ready-to-paste lines

Restored first-published row (= df4db54 line 99 verbatim; its status, recheck and used-by equal the tip values, so nothing else changes). Replace master line 99:

```
| S093 | Linux PSI and IRQ time accounting Kconfig at v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/init/Kconfig | code | A | the CONFIG_PSI, CONFIG_PSI_DEFAULT_DISABLED and CONFIG_IRQ_TIME_ACCOUNTING build options and their help text: the /proc/pressure/ files the CONFIG_PSI help text names, and the psi=1 opt-in that overrides CONFIG_PSI_DEFAULT_DISABLED; v7.2 only | CONFIG_PSI:723-741 (help-text file list:730-733, cgroup2 text:735-737); CONFIG_PSI_DEFAULT_DISABLED:743-760 (psi=1 text:748-750); CONFIG_IRQ_TIME_ACCOUNTING:615-624; tag v7.2; sha256 a43f09d89309a6bd | The CONFIG_PSI help text names only the pressure statistics files cpu, memory, and io under /proc/pressure/ plus the cgroup2 per-cgroup files; CONFIG_PSI_DEFAULT_DISABLED leaves tracking disabled unless psi=1 is passed on the kernel commandline; CONFIG_IRQ_TIME_ACCOUNTING is a separate fine-granularity task irq time option. | mined | 2026-10-22 | on-release | corpus/knowledge/system-pressure-r24.md, corpus/lessons/round-24.md |
```

New row S143 (the next free id at master 47f6543a: the highest Registry id is S142). Its teaches opens `supersedes S093 — `. Its anchor carries the corrected 730-731. Status `mined`; opened `2026-10-22`; recheck is the original `on-release`; used-by names the three corpus files that cite the corrected fact. Insert after master line 148 (S142):

```
| S143 | Linux PSI and IRQ time accounting Kconfig at v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/init/Kconfig | code | A | the CONFIG_PSI, CONFIG_PSI_DEFAULT_DISABLED and CONFIG_IRQ_TIME_ACCOUNTING build options and their help text: the /proc/pressure/ files the CONFIG_PSI help text names, and the psi=1 opt-in that overrides CONFIG_PSI_DEFAULT_DISABLED; v7.2 only | CONFIG_PSI:723-741 (help-text file list:730-731, cgroup2 text:735-737); CONFIG_PSI_DEFAULT_DISABLED:743-760 (psi=1 text:748-750); CONFIG_IRQ_TIME_ACCOUNTING:615-624; tag v7.2; sha256 a43f09d89309a6bd | supersedes S093 — anchor only: the help-text file list is lines 730-731; lines 732-733 are the next sentence (the walltime share) and name no file. The CONFIG_PSI help text names only the pressure statistics files cpu, memory, and io under /proc/pressure/ plus the cgroup2 per-cgroup files; CONFIG_PSI_DEFAULT_DISABLED leaves tracking disabled unless psi=1 is passed on the kernel commandline; CONFIG_IRQ_TIME_ACCOUNTING is a separate fine-granularity task irq time option. | mined | 2026-10-22 | on-release | corpus/knowledge/system-pressure-r24.md, corpus/lessons/round-24.md, corpus/lessons/round-24-verifier-spotcheck.md |
```

used-by justification: `corpus/knowledge/system-pressure-r24.md:70` cites `init/Kconfig:730-731`. `corpus/lessons/round-24.md:28` quotes 730-731 in the Gate row, and `:48-49` logs the correction. `corpus/lessons/round-24-verifier-spotcheck.md:121` says "The row's corrected anchor `730-731` is right". `corpus/lessons/round-27.md:36` names S093 only as a changed row, not the fact, so it is not listed.

Gate line:

Gate: https://raw.githubusercontent.com/torvalds/linux/v7.2/init/Kconfig · accessed 2026-10-22T17:10:28Z · sha256 a43f09d89309a6bd7036c96e0836c30c021f2d56b042be288a15533dd9e944bd · located Kconfig:730-731, 19 words: "If you say Y here, the kernel will create /proc/pressure/ with the pressure statistics files cpu, memory, and io."

## 4. Census validate (step 4)

How the script finds the lane: `--root DIR` sets the root (the default is the script's parent directory, the fleet root). `build_roster` reads `$ROOT/shokunin.conf` textually, with `sed` over `lane|repo|desc` rows. The conf row is line 63: `mori|mori-shokunin|...`, so lane `mori` maps to `$ROOT/mori-shokunin/corpus/SOURCES.md`, and used-by paths resolve under `$ROOT/mori-shokunin/`. The argument `mori` is matched against that roster. The validator was never pointed at the real fleet root.

Scratch copies (committed bytes: `git archive` of master 47f6543a, plus a copy of `shokunin.conf`):
- `head-base`: master unchanged.
- `head-applied`: S093 restored and S143 inserted after line 148 (the two lines in section 3).
- `head-control`: as `head-applied`, but S143 teaches without `supersedes S093 — `.
- `census-base` / `census-applied`: the same test on the older tip 5f00fd04, where the new row was S142 (free there). Exit 0 on both.

Results:

- `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /fast/scratch/hyaku/mori-r27/SupersedeS093/head-applied mori` → **exit 0**. Output: six pre-existing W04 warnings (S035, S037, S073, S074, S075, S076; warnings do not change the exit) and `mori ok <scratch path>`.
- Same command on `head-base` → exit 0.
- Same command on `head-control` → exit 1: `mori E04 S143 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/init/Kconfig within scope ...`. The `supersedes S[0-9]{3}` exemption (`sources-census.sh:646-649`) is what keeps the applied copy clean.
- `census --root .../head-applied mori` → `mori rows 143`.

## 5. Row-identity check (QUALITY 81)

The lane's check file (sha256 5f05d4fe...) equals the master blob, and `git log -- .ufo/waves/round-27/check-row-identity.py` shows b89ac34 as its latest commit. That is the hardened version, which prints `removed` and `bad` fields. The tip's version (sha256 21dfa3d7...) does not print them. My first run was at the tip and used the older version. The working-tree file changed before my clone run, so the clone run used the hardened version.

- Master 47f6543a (hardened check): `changed S090 cells=anchor,teaches`, `changed S093 cells=anchor`, `changed S096 cells=teaches`, `changed S097 cells=anchor,teaches`, `changed S101 cells=teaches`; `rows=142 changed=5 removed=0 bad=0`; exit 1.
- Scratch clone of master with the two lines committed (hardened check): `changed S090`, `changed S096`, `changed S097`, `changed S101`; `rows=143 changed=4 removed=0 bad=0`; exit 1. S093 is no longer listed; the four rows left are outside this item.
- Tip 5f00fd04 (older version, run from the lane): `changed S090 (anchor,teaches)`, `changed S093 (anchor)`, `changed S096 (teaches)`, `changed S097 (anchor,teaches)`, `changed S101 (teaches)`; `rows=141 changed=5`; exit 1.

## 6. Lane movement and the S142 collision

- After the named tip, the lane landed 0becc42, b97b2e3, b89ac34 and 47f6543. `git log -S '| S142 | oh-my-pi task/executor.ts' master` shows b89ac34 introduced that row, and master line 148 holds it. S142 is therefore taken and the new row is S143.
- If another row lands before integration, take the next free id and re-run `validate` and the row-identity check.

## 7. For the integration owner (MoriR27 decides; this seat made no lane edits)

1. Replace master line 99 with the restored S093 line (section 3). Insert the S143 line after S142 (master line 148).
2. Log the change in the round-27 lesson's "Row changes logged" section, in the same form as S124: "S093 anchor restored to first-published text; corrected by S143 (`supersedes S093 —`)".
3. Optional, not needed for correctness: `system-pressure-r24.md:70` and `round-24.md:28` cite S093 for 730-731. That span lies inside S093's restored 730-733, so they stay true. They could cite S143 for the exact pointer.
4. Optional, low: widen the PSI_DEFAULT_DISABLED span in S093 and S143 to `743-761` (`Say N if unsure.` at 761).
5. After landing, `python3 -I -B .ufo/waves/round-27/check-row-identity.py <rev>` would show `changed=4` (S090, S096, S097, S101) if nothing else changes, and `validate` should exit 0.

## 8. Gaps

- Tag v7.2 not re-verified here (row 13).
- `validate` was run only on scratch copies, as instructed. The real fleet root was not validated.
- The sha256 prefix match supports the same bytes as first publication. I did not prove the full digest matched at first publication [INFERENCE].
- Not checked here: S090, S096, S097, S101 (routed elsewhere).

## 9. Tooling and privacy

- No installs or updates. Versions observed: bash 5.3.20, GNU Awk 5.4.1, Python 3.14.8, sha256sum (`--version` prints 0.8.0), curl 8.23.0, git 2.56.0, GNU tar 1.35. The operator's agent rules file was read; its tooling directive is the only content.
- Only read-only git was used in the lane (`show`, `log`, `cat-file`, `rev-parse`, `merge-base`, `archive`), plus `clone` from the lane into scratch. Commits exist only in the scratch clone.
- Only commit ids, row cells, line numbers and counts appear in this report. No user, process or login identifiers, and no settings values.
