# Scout — per-surface recon for QUALITY 79 (round 28, wave 1)

Seat: MoriR28.ScoutSurfaceRecon. Lane tip read-only at 2026-10-22T18:01:40Z: `git rev-parse --short HEAD` → `079a47c`; `git status --porcelain corpus/SOURCES.md` → ` M corpus/SOURCES.md` (working copy, so all row reads below are of the working copy at that instant).

Question: for rows S096, S097, S101, S127, S128, S129, S131, S140 — what is the row's pinned ref, what is installed on the host, and does a host-scoped statement on the row hold?

## 1. Installed versions (read-only)

| Surface | Command | Output |
|---|---|---|
| kernel | `uname -r` | `7.2.11-arch1-1` |
| kernel package | `pacman -Q linux` | `linux 7.2.11.arch1-1` |
| systemd | `systemctl --version \| head -1` | `systemd 262 (262-1-arch)` |
| systemd package | `pacman -Q systemd` | `systemd 262-1` |
| earlyoom | `pacman -Q earlyoom` | `earlyoom 1.9.0-1` |
| man-pages | `pacman -Q man-pages` | `man-pages 6.19-1` |
| bun | `bun --version` | `1.4.3` (installed binary `/home/vgpnk/.local/bin/bun`; not a pacman package — `pacman -Q bun` → exit 1, `error: package 'bun' was not found`) |
| omp | embedded package manifest in `/home/vgpnk/.local/bin/omp` | `18.12.6` (see §3) |

No tool was installed, upgraded or downgraded by this seat; no pacman transaction was run (only `-Q` queries).

## 2. Comparison table

Row ids per `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md` (line numbers are that file's): S096 :102, S097 :103, S101 :107, S127 :133, S128 :134, S129 :135, S131 :137, S140 :146.

| row | pinned ref (row) | installed | host-scoped statement holds? |
|---|---|---|---|
| S096 | upstream commit 52b1364, merged v6.1-rc1, "first release Linux 6.1" (:102) | kernel 7.2.11 | **Holds.** `/proc/pressure/irq` exists (`ls -l /proc/pressure/`) and reports a single `full` line only; no `some` line. `/proc/pressure/cpu` and `/proc/pressure/irq` are mode 666. The current cgroup contains `irq.pressure` (exactly 1 match in its file list). |
| S097 | man-pages **6.20** (2026-10-21) (:103) | man-pages **6.19** | **Does not hold as a host statement.** The pin is one release newer than installed. Host still confirms the substantive absence: `man -w proc_pressure` → `No manual entry for proc_pressure`; `ls /usr/share/man/man5/ \| grep -c proc_pressure` → `0`. So the row's "no such page" is true of 6.19 too, but its present-tense "current release 6.20" is false of the host → needs an upstream-only scope, per criterion 79 (`corpus/QUALITY.md:361-364`). |
| S101 | omp tag **v18.12.6** = commit 45c35e40 (:107) | omp 18.12.6 | **Holds.** Embedded manifest `@oh-my-pi/pi-coding-agent` version `18.12.6` (byte 151991040) and changelog `## [18.12.6] - 2026-10-21` (byte 252999416). Embedded settings spec for `async.maxJobs` is `type: "number", default: 100` with no `max`/`min` field (byte 155231595). |
| S127 | kernel **v7.2 tag** of fs/proc/base.c, oom.h, fork.c (:133) | kernel 7.2.11 | **Holds exactly for every quoted anchor** — see §4. Runtime modes agree: `/proc/self/oom_score` `-r--r--r--` (0444), `/proc/self/oom_score_adj` `-rw-r--r--` (0644, owner-writable). |
| S128 | man-pages **6.19** (:134) | man-pages 6.19-1 | **Holds.** Both pages installed: `/usr/share/man/man5/proc_pid_oom_score_adj.5.gz`, `/usr/share/man/man5/proc_pid_oom_score.5.gz` (`man -w` resolves both). Range text present: `Acceptable values range from -1000` (:46) `(OOM_SCORE_ADJ_MIN) to +1000 (OOM_SCORE_ADJ_MAX).` (:47). |
| S129 | systemd **v262** (:135) | systemd 262-1 | **Holds.** Installed docs carry the documented symbols: `OOMScoreAdjust=` at `systemd.exec.5.gz:1636` with `Takes an integer between -1000 (to disable OOM killing of processes of this unit) and` (:1638); `DefaultOOMScoreAdjust=` at `systemd-system.conf.5.gz:318`. |
| S131 | earlyoom **v1.9.0** tag (:137) | earlyoom 1.9.0-1 | **Holds as an upstream pin; no host statement to check** — the row explicitly excludes "this host's /etc/default/earlyoom file or its values". Installed package ships that path as a conffile (`pacman -Ql earlyoom` → `/etc/default/earlyoom`); its values were not read or copied. |
| S140 | omp commit **6962d5cd** (authored 2026-09-24) (:146) | omp 18.12.6 (2026-10-21) | **Structure holds, verbatim quote does not.** Binary contains `maxRunningJobs: () => Math.min(100, XPe.get(R))` at byte 164406766 — per-check function with the 100 ceiling, but the minified getter `XPe.get(R)` replaces `cfgAsyncMaxJobs.get(settings)` and there is **no** `?? 100` fallback. A host reading must not claim the row's quoted text appears verbatim in the shipped build. |

## 3. omp identity evidence (`/home/vgpnk/.local/bin/omp`, sha256 `85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4`, 256,702,432 bytes, mtime 2026-10-21 20:37)

Offsets from `grep -abo`, which reports byte offsets for a binary (no line numbers exist):

- bytes 151990820-151991140: `// packages/coding-agent/package.json` → `name: "@oh-my-pi/pi-coding-agent", version: "18.12.6"` (version string at 151991040; the same version appears for `@oh-my-pi/pi-natives` at 147615522).
- byte 252999416: changelog fragment `## [18.12.6] - 2026-10-21` preceded by `## [Unreleased]` → 18.12.6 is the top shipped release.
- byte 256648606: literal `omp/18.12.6` (user-agent string).
- byte 155231595: `id: "async.maxJobs", protocolDefault: ["rpc"], type: "number", default: 100`.
- byte 164406766: the clamp, quoted above. The other five `Math.min(100` hits were each dumped and are unrelated: a JSON-depth cap (95906716), a reserve percentage (150439459, 150607636), a daemon log-line cap `Math.max(1, Math.min(1000, …))` (152600751), and percent formatting (155406775).
- `grep -abo '6962d5c'` → no match: the pinned S140 commit hash is not embedded, so commit identity is not provable from the binary. [INFERENCE] 2026-09-24 (S140 author date) precedes the 18.12.6 build date 2026-10-21, so the rewrite is very likely inside the installed build; the structural match above is the direct evidence.

## 4. v7.2 → v7.2.11 source check for S127

Fetched with `curl` from git.kernel.org stable, `?h=v7.2.11`:

| file | fetched (UTC) | HTTP | bytes | sha256 | vs S127's pinned v7.2 hash |
|---|---|---|---|---|---|
| fs/proc/base.c | 2026-10-22T18:00:30Z | 200 | 98,196 | `cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6` | identical |
| include/uapi/linux/oom.h | 2026-10-22T18:00:36Z | 200 | 526 | `6b00b4d0648bcdc9d6be7ea8a33b8e6b842c063e7b2b71bdabd757de773896ae` | identical |
| kernel/fork.c | 2026-10-22T18:00:36Z | 200 | 85,868 | `4548f28fd8ee2b7f3a974260b871f3d49159a4e8b9d121be19f26e7671b65200` | **differs** (pin: 85,725 B, `359882ea981b58f5289293e5644f7c0085a8350e4f1937f39dcb94ae1cd0dd1d`) |

Even though fork.c changed, every anchor S127 cites is still at the stated line in v7.2.11:

- fork.c:1728 `sig = kmem_cache_zalloc(signal_cachep, GFP_KERNEL);`.
- fork.c:1768-1769 `sig->oom_score_adj = current->signal->oom_score_adj;` / `sig->oom_score_adj_min = current->signal->oom_score_adj_min;`.
- fork.c:1949 `static void copy_oom_score_adj(u64 clone_flags, struct task_struct *tsk)`; :1961 `mm_flags_set(MMF_MULTIPROCESS, tsk->mm);`; function ends at :1966.
- base.c:583-599 `proc_oom_score`; :586 `unsigned long totalpages = totalram_pages() + total_swap_pages;`; :590 `badness = oom_badness(task, totalpages);`; :596-597 `if (badness != LONG_MIN)` / `points = (1000 + badness * 1000 / (long)totalpages) * 2 / 3;`.
- base.c:1131-1133 `if ((short)oom_adj < task->signal->oom_score_adj_min &&` / `!capable(CAP_SYS_RESOURCE)) {` / `err = -EACCES;`.
- base.c:1275-1279 `if (oom_score_adj < OOM_SCORE_ADJ_MIN ||` … `err = -EINVAL;`.
- base.c:3351-3353 and :3706-3708 `ONE("oom_score", S_IRUGO, …)` and `REG("oom_score_adj", S_IRUGO|S_IWUSR, …)`.
- oom.h:9-10 `#define OOM_SCORE_ADJ_MIN (-1000)` / `#define OOM_SCORE_ADJ_MAX 1000`.

So S127's pin (tag v7.2) transfers to the host's 7.2.11 without any line shift, and the only file-level drift is fork.c outside the quoted regions [INFERENCE: "outside" is supported by all anchors matching, not by a full diff].

Note: `/proc/self/oom_score_adj_min` does not exist (`ls` → `No such file or directory`). That is not a contradiction of S127 — S127 cites `oom_score_adj_min` as the in-kernel per-task floor at base.c:1131-1133, not as a proc file. No proc page in man-pages 6.19 documents such a file either (`grep -n oom_score_adj_min` on the gz page → no match).

## 5. Findings that affect the rows (for the planner)

1. **S097 / QUALITY 79 (real):** the row's "current release 6.20, 2026-10-21" is a present-tense upstream statement while the host holds man-pages 6.19-1. Either scope it "man-pages 6.20 upstream" explicitly (the rest of the row already is upstream-scoped) or add the 6.19 host fact. The 404 finding itself is unchanged.
2. **S140 verbatim drift (real):** the shipped 18.12.6 build carries the function-shaped clamp but minified, without `?? 100`. Any host reading that quotes the row's source line as if it were the binary's text is false of the build. The behaviour (ceiling 100, default 100 from the spec) is unchanged.
3. **S096, S101, S127, S128, S129, S131:** pins equal or predate the installed release, and the host-scoped claims were reproduced above; no scoping defect found.
4. **C1 observation (not my row set):** `corpus/SOURCES.md` at the tip had 199 lines, 144 `S` rows, max id `S144`; `grep 'S145\|…\|S152'` → no match at 2026-10-22T18:01:40Z, so the eight superseding rows were not yet in the working copy when sampled. Stated as an observation only — scribe/lane work is in flight.

## 6. Remaining unknowns

- omp commit identity for the installed build: no embedded short or full hash; only version 18.12.6 and build date 2026-10-21 are observable. [INFERENCE] S140's commit is contained, per dates and the structural match.
- Whether the staff/`linux` package's `/usr/src/linux` tree (a build-dir symlink to `/lib/modules/7.2.11-arch1-1/build`, no `fs/proc/base.c`) was patched relative to upstream 7.2.11: not checked. Arch's `fs/proc/base.c` is not among its patches as far as observable here, but this was not verified.
- S131's "shipped default args" text was not re-read from upstream this pass (no fetch of the v1.9.0 tree); only the version identity (1.9.0-1 = v1.9.0) was checked.
- The exact enforcement of the docs' "floor of 1" for `async.maxJobs` on 18.12.6: the embedded spec shows no `min`, and no runtime clamp below 1 was located; not proven either way.

## 7. Compliance

- Writes: only this report. No lane commit, no git/jj mutating command, no unit/process action, no omp invocation, no settings or MCP file touched.
- Privacy: no unit names, uids, pids, session ids or paths, no earlyoom config values, no `/proc` per-process values printed beyond the file modes and the mere existence of files.
- Sources were opened with `curl` only; URL, access time, byte size and sha256 are recorded in §4. Bytes are cached at `/tmp/base-7.2.11.c`, `/tmp/oom.h-7.2.11`, `/tmp/fork.c-7.2.11`.
