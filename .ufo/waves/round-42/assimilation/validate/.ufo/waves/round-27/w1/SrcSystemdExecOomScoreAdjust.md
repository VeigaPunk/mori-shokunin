# SrcSystemdExecOomScoreAdjust — round 27, wave 1, claim C1 (depth, FR10 "fleet attribution of a victim")

Seat: `MoriR27.SrcSystemdExecOomScoreAdjust` (scout, leaf). Lane repo:
`/home/vgpnk/Projects/shokunin/mori-shokunin`. Contract:
`.ufo/waves/round-27/contract.md` (C1, "how earlyoom 1.9.0 and the Linux 7.2 kernel choose an OOM victim").
Assigned question: the systemd 262 man-page contract for the OOM score adjustment — range, manager
defaults, user-unit inheritance, and which process receives the setting — as ground for
`corpus/knowledge/oom-victim-selection-r27.md`. Scratch: `/fast/scratch/hyaku/mori-r27/SrcSystemdExecOomScoreAdjust/`.
No lane file touched except this report.

## 1. Sources opened (both new; no existing row covers either file)

| File | URL | HTTP | Bytes | Lines | sha256 of fetched bytes |
|---|---|---|---|---|---|
| `man/systemd.exec.xml` | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml | 200 | 343,315 | 5,308 | `44b89bffce737aff803966c207329e9fe2d28ad07709a4bb8e0edf6a4ec0d844` |
| `man/systemd-system.conf.xml` | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-system.conf.xml | 200 | 49,977 | 919 | `161359987affadc8e4a533bc9117bbbd98053cb807808b623eb24794b49b0c58` |

Access: 2026-10-22T15:46:34Z, `curl -sS` only (no browser, no challenge bypass). Tag resolution by
ordinary API read: `v262` is an annotated tag object `1f7dffaf714cc4488159c498b7a17cf34c5a96d5`
(tagger 2026-09-22T13:12:43Z) pointing at commit `8cc40e0c5e9234bf45084751ac53b1fbfe70b492`; this
matches the v262 pin already recorded in `corpus/SOURCES.md:127` (S121). Byte identity between the tag
URL and the commit-pinned URL was checked for both files (same sha256), so the quotes below hold at the
tag and at the commit.

## 2. Gate block

| Field | Value |
|---|---|
| URL (1) | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml |
| URL (2) | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-system.conf.xml |
| Access date | 2026-10-22 (2026-10-22T15:46:34Z) |
| sha256 (1) | `44b89bffce737aff803966c207329e9fe2d28ad07709a4bb8e0edf6a4ec0d844` |
| sha256 (2) | `161359987affadc8e4a533bc9117bbbd98053cb807808b623eb24794b49b0c58` |
| Tag under test | v262 = commit `8cc40e0c5e9234bf45084751ac53b1fbfe70b492` |

Verbatim quotes (XML tags and line wrapping are not part of the quote; each quoted string was checked
as an exact substring of the fetched bytes after stripping tags and normalizing line-wrap whitespace,
and each is <= 25 words). The Gate set is quotes 1-6 (2-5 requested; 1-3 ground the per-unit setting,
4-6 the manager-wide default); quote 7 is carried because it answers "which process receives the
setting" from the other side and would otherwise make the set seven items.

1. `man/systemd.exec.xml:1295-1296` — "Sets the adjustment value for the Linux kernel's Out-Of-Memory (OOM) killer score for executed processes." (15 words)
2. `man/systemd.exec.xml:1296-1297` — "Takes an integer between -1000 (to disable OOM killing of processes of this unit) and 1000" (16 words)
3. `man/systemd.exec.xml:1299-1300` — "If not specified, defaults to the OOM score adjustment level of the service manager itself, which is normally at 0." (20 words)
4. `man/systemd-system.conf.xml:303-304` — "Configures the default OOM score adjustments of processes run by the service manager." (13 words)
5. `man/systemd-system.conf.xml:304-305` — "This defaults to unset (meaning the forked off processes inherit the service manager's OOM score adjustment value)" (17 words)
6. `man/systemd-system.conf.xml:305-306` — "if the service manager is run for an unprivileged user, in which case this defaults to the service manager's OOM adjustment value plus 100" (24 words)
7. `man/systemd-system.conf.xml:310-311` — "Note that this setting has no effect on the OOM score adjustment value of the service manager process itself" (19 words)

## 3. Extracted facts

| # | Fact | Anchor |
|---|---|---|
| F1 | `OOMScoreAdjust=` is a per-unit (`systemd.exec(5)`) setting that adjusts the kernel OOM killer score of the unit's **executed processes**. | `systemd.exec.xml:1293` (term), `:1295-1296` |
| F2 | Range is an integer **-1000 .. 1000**: -1000 "to disable OOM killing of processes of this unit", 1000 "to make killing of processes of this unit under memory pressure very likely". The page names no other accepted value. | `systemd.exec.xml:1296-1297` |
| F3 | Per-unit default when unset: the score of **the service manager itself**, "normally at 0". So for the system manager a unit with no `OOMScoreAdjust=` is at the manager's level, read as 0 unless the manager itself was started with a different value. | `systemd.exec.xml:1299-1300` |
| F4 | `DefaultOOMScoreAdjust=` (`system.conf(5)` / `user.conf(5)`) is the manager-wide default for the per-unit setting, and it governs "processes run by the service manager". | `systemd-system.conf.xml:301`, `:303-304`, `:307-308` |
| F5 | Its default is **unset**, which means forked processes **inherit the service manager's OOM score adjustment value**. | `systemd-system.conf.xml:304-305` |
| F6 | Exception branch: "if the service manager is run for an unprivileged user", the default becomes **the manager's OOM adjustment value plus 100**, which "makes service processes slightly more likely to be killed under memory pressure than the manager itself" (17 words). This is the user-manager inheritance rule: a user unit with no explicit `OOMScoreAdjust=` lands at (user manager's own `oom_score_adj` + 100). | `systemd-system.conf.xml:305-307` |
| F7 | The setting never rewrites the manager: it "has no effect on the OOM score adjustment value of the service manager process itself, it retains the original value set during its invocation". | `systemd-system.conf.xml:310-311` |
| F8 | `systemd-system.conf(5)` is one page for both managers: the system instance reads `system.conf` (+`system.conf.d`), the user instance reads `user.conf` (+`user.conf.d`) from the user's home and `/etc`, `/run`, `/usr/lib`. So F4-F7 apply to the user manager's units through `user.conf`. | `systemd-system.conf.xml:49-55`; `:21-27` (refnames include `systemd-user.conf`, `user.conf.d`); `:37-43` (user.conf search paths) |
| F9 | The page pins `DefaultOOMScoreAdjust=` to systemd **v250**; the v262 `OOMScoreAdjust=` entry carries no `xi:include` version marker. | `systemd-system.conf.xml:313`; `systemd.exec.xml:1293-1306` (no include in the varlistentry) |
| F10 | A failed adjustment aborts the invocation with the systemd-specific exit code **206** (`EXIT_OOM_ADJUST`, "Failed to adjust the OOM setting. See `OOMScoreAdjust=` above."); the page frames these codes as "problems during process invocation", so the value is applied during invocation, not once per unit at load. | `systemd.exec.xml:4890-4891`, `:4934-4938` |
| F11 | For an *active* memory-pressure decision the page only cross-references `OOMPolicy=` for the manager's reaction to a kill by the kernel OOM killer or systemd-oomd; it says nothing about victim selection. | `systemd.exec.xml:1302-1305` |

Consequence for the C1 entry: the manager that forks a process is the one whose `DefaultOOMScoreAdjust=`
applies, so a fleet process forked by the system manager defaults to that manager's level (normally 0) and
one forked by an unprivileged user manager defaults to that manager's own level + 100, unless the unit,
the service, or a container path sets `OOMScoreAdjust=`. Which branch the host's fleet runtimes actually
take is a host measurement owned by other seats (`MoriR27.HostUnitOomAdjust`,
`MoriR27.SrcOmpBunOomAdj`); this report claims no host value. [INFERENCE] on the fleet consequence;
F1-F11 are page text.

## 4. Row-coverage check (why this is a new row, not an anchor)

| Probe | Result |
|---|---|
| `grep -c -F 'systemd.exec' corpus/SOURCES.md` | 0 |
| `grep -c -F 'systemd-system.conf' corpus/SOURCES.md` | 0 |
| `grep -c -F 'DefaultOOMScoreAdjust' corpus/SOURCES.md` | 0 |
| `grep -n -F 'OOMScoreAdjust' corpus/SOURCES.md` | 1 hit: `corpus/SOURCES.md:126` (S120) |

S120 is the earlyoom unit template `earlyoom.service.in` at v1.9.0 and its anchor `:14 (OOMScoreAdjust=-100)`.
That row's scope is "the upstream unit template only"; it does not document the systemd setting, so it is
not the row to extend. S124 covers `systemd.resource-control.xml` and `systemd-oomd.service.xml` only,
so it is not it either. Table ends at `corpus/SOURCES.md:132` (S126); no S127+ row exists yet.

## 5. Ready-to-paste SOURCES row

Id `S127` is the first free id at read time (`corpus/SOURCES.md:132` is S126). If a sibling seat lands a
row first, renumber this row and its `used-by` target consistently.

```
| S127 | systemd v262 `OOMScoreAdjust=` and `DefaultOOMScoreAdjust=` manual pages — https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml ; https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-system.conf.xml | docs | A | systemd 262 release documentation of the OOM score adjustment only: the per-unit range and its stated effects, the per-unit default of the managing manager's own level, the manager-wide default and its unset/inherit reading, the unprivileged-user-manager default of manager value plus 100, and the statement that the manager's own value is never rewritten; not this host's unit values, user-manager state or fleet process scores, not the kernel's `oom_score` computation or `proc(5)` wording, not earlyoom's or systemd-oomd's victim choice, not the privilege rule on lowering the value (kernel doc, separate row) | man/systemd.exec.xml:1293 (term), :1295-1296 (executed processes), :1296-1297 (range -1000..1000), :1299-1300 (unset => manager's level, normally 0), :1302-1305 (OOMPolicy cross-ref), :4934-4938 (EXIT_OOM_ADJUST = 206, "problems during process invocation" at :4890-4891); man/systemd-system.conf.xml:301 (term), :303-304 (processes run by the manager), :304-305 (unset => fork inherits manager value), :305-307 (unprivileged user manager => manager value plus 100), :307-308 (global default for the per-unit setting), :310-311 (manager process keeps its own value), :313 (v250), :49-55 (system.conf vs user.conf read by the two managers); tag v262 = commit 8cc40e0c5e9234bf45084751ac53b1fbfe70b492 (annotated tag 1f7dffaf714cc4488159c498b7a17cf34c5a96d5, tagger 2026-09-22T13:12:43Z); systemd.exec.xml 343,315 B sha256 44b89bffce737aff803966c207329e9fe2d28ad07709a4bb8e0edf6a4ec0d844; systemd-system.conf.xml 49,977 B sha256 161359987affadc8e4a533bc9117bbbd98053cb807808b623eb24794b49b0c58; HTTP 200 both, 2026-10-22T15:46:34Z | The per-unit score is an integer in -1000..1000 applied to a unit's executed processes; unset means the managing manager's own level (normally 0 for the system manager), and for an unprivileged user manager the manager-wide default is that manager's value plus 100, so user units inherit manager+100 unless they set the value; the setting never changes the manager's own score. | mined | 2026-10-22 | on-release | corpus/knowledge/oom-victim-selection-r27.md |
```

Column count check against the header at `corpus/SOURCES.md:5`
(`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`):
11 cells, same as S114-S126. `status` = `mined`, `opened` = `2026-10-22`, `recheck` = `on-release`,
`used-by` = the C1 entry path.

## 6. Adjacent evidence found while tracing, NOT in the row above

These are code, not the two assigned man pages. Recorded so the entry does not over-claim from the page;
each would need its own row (or an anchor on a file-scoped row) before it is cited in the entry.

| Item | Anchor | Note |
|---|---|---|
| systemd writes the value into `/proc/self/oom_score_adj` in the forked child, after validating it against `OOM_SCORE_ADJ_MIN..MAX` | https://raw.githubusercontent.com/systemd/systemd/v262/src/basic/process-util.c (sha256 `239148a8e9d447de6ffaf5f747d072b179ccb688aeb0fe81d71c1f13db8c627d`), `:1927-1929` (`oom_score_adjust_is_valid`), `:1931-1941` (`set_oom_score_adjust` writes `/proc/self/oom_score_adj`) | the page's "executed processes" is implemented as a pre-exec write on the child |
| the write site is inside `exec_invoke()` and **silently skips an EPERM**: "When we can't make this change due to EPERM, then let's silently skip over it." (15 words); the debug string is "Failed to adjust OOM setting, assuming containerized execution, ignoring" | https://raw.githubusercontent.com/systemd/systemd/v262/src/core/exec-invoke.c (sha256 `3be6c5a98ff29d3c7e929759f0d6c2f2ff8cc66bb146fdf836fbd2fe8fbebfed`), `:5172` (`exec_invoke`), `:5594-5599` | a configured value can be *rejected* without failing the unit, while the page's exit code 206 (`EXIT_OOM_ADJUST`, F10) covers every non-privilege failure; so the configured value is not proof of the effective value — this is the falsifier the entry needs before it reports a fleet score |
| kernel rule on lowering: "The value of /proc/&lt;pid&gt;/oom_score_adj may be reduced no lower than the last value set by a CAP_SYS_RESOURCE process." (18 words), and "To reduce the value any lower requires CAP_SYS_RESOURCE." | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst (sha256 `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126`), `:1799-1801` | this is why the user-manager default goes *up* by 100 and why a user unit cannot lower its score |
| unit-file grammar is a plain integer, no symbolic values (`parse_oom_score_adjust` = `safe_atoi` then the -1000..1000 check) | https://raw.githubusercontent.com/systemd/systemd/v262/src/basic/parse-util.c (sha256 `5281ab7a3b760ac79a33342b22aa0a584e481cde2fa44a953678e6b500d44f81`), `:762-777` | it confirms the page's F2 range for the unit-file path as well; no `auto`/`infinity` spelling exists to look for on this host's unit files |
| an out-of-range or unparsable unit-file value is **logged as a warning and ignored**, leaving the inherited default in place ("OOM score adjust value out of range, ignoring") | https://raw.githubusercontent.com/systemd/systemd/v262/src/core/load-fragment.c (sha256 `a510b28617813a915779183a06ad5b567827e5522137c854b0034a3f772a44f5`), `:763-800` (`config_parse_exec_oom_score_adjust`), `:789-793` | a unit that *tries* to set a score can end up at the default; a configured-looking unit file is not evidence of the effective score |
| existing row conflict | `corpus/SOURCES.md:88` (S082) is the same kernel file and its anchor already carries the same bytes (`sha256 e760f716…`), but its scope reads "textual mountinfo field layout only" | do not bolt the oom_score_adj passage onto S082; either the L1 accepts a scope correction on S082, or the passage gets its own scoped row |

## 7. Hygiene

- Privacy: this report contains upstream page text, URLs, hashes, file sizes, line numbers and system
  paths only. No journal `MESSAGE`, no uid, no pid list, no `/etc/default/earlyoom` or `--prefer`/
  `--avoid`/`--ignore` value, no settings-file path or key name, no session id.
- Detection and report only: nothing was started, stopped, enabled, restarted or signalled; no
  `oom_score_adj` of any process was written; no omp invocation.
- Tooling: no install or upgrade. Host `curl 8.23.0` and `python3 3.14.8` were sufficient; no pacman
  transaction was attempted.
- Lane writes: this report only. No `jj` or mutating `git` command was run.
- Unrun checks: none claimed. Line counts and sha256 were recomputed from the fetched bytes
  (`wc -l`, `sha256sum`); every quote was substring-checked against the tag-stripped bytes.

## 8. Remaining unknowns (outside this seat's ticket)

1. The page states the unprivileged-user branch (+100) but gives no value for a user manager run by a
   privileged user; how the host's user manager was started, and its own `oom_score_adj`, is the
   `MoriR27.HostUnitOomAdjust` / `MoriR27.SrcOmpBunOomAdj` seats' measurement, not derivable here.
2. Whether any fleet unit sets `OOMScoreAdjust=` explicitly (a host unit census), and whether containers
   (`systemd-nspawn`/`podman`) re-map the value, is not in either page.
3. The kernel's own `oom_score` weighting (`oom_score_adj` is one input to `oom_badness`) is not in these
   pages at all; it belongs to `MoriR27.SrcKernelOomBadness`.
4. Exact `OOM_SCORE_ADJ_MIN/MAX` constants: not quoted here (their definition file was not opened); the
   man page range -1000..1000 stands on F2 alone.
