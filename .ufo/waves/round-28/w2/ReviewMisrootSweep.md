# ReviewMisrootSweep — round 28 wave 2

**Verdict: holds** — the seven lane-root files at `f2de0ee` are byte-equal to upstream, absent from the
fleet root, and `misroot-hash-check.sh 27 f2de0ee` exits 0; one lesson-M2 wording nit (an unrecorded tool
run stated as executed) and two information notes below.

Seat: `MoriR28.ReviewMisrootSweep` (read-only attacker; wrote only this report + scratch under
`/fast/scratch/hyaku/mori-r28-w2/ReviewMisrootSweep/`). Attack rev `f2de0eedcd60d2e354da75265ea6122bc3896073`.
Tools installed/upgraded: none (curl, sha256sum, git already present). `~/.omp/agent/RULES.md` not re-read
here; no pacman/jj/git-write command was run.

## 1. Byte equality: lane files at `f2de0ee` vs upstream (my own curl, 2026-10-22T18:54Z)

All seven `git show f2de0ee:<path>` hashes equal my fetched upstream bytes:

| lane path | committed sha256 | upstream URL (HTTP 200) | match |
|---|---|---|---|
| `base.c` | `cef1a2cf…0084915c6` | raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c | equal |
| `oom_kill.c` | `452f1348…a401f756b4e` | raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c | equal |
| `MANPAGE.md` | `cc48b02e…0dfeda` | raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/MANPAGE.md | equal |
| `main.c` | `08656b0b…f9d0e4` | raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c | equal |
| `meminfo.c` | `526e512c…0edfeb` | raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/meminfo.c | equal |
| `sd-main.c` | `5ecdca43…3aae3` | raw.githubusercontent.com/systemd/systemd/v262/src/core/main.c | equal |
| `user@.service.in` | `72c2f40d…20504c` | raw.githubusercontent.com/systemd/systemd/v262/units/user@.service.in | equal |

`oom_kill.c` first fetch returned HTTP 429 (rate limit, 18:54:22Z); a retry 22 s later returned 200 with the
matching hash — same transient wave-1 `MisrootProvenance.md:43-44` observed. URLs from
`w1/MisrootProvenance.md:31-37`.

## 2. Fleet-root absence (now)

`test -e`/`test -L` on `/home/vgpnk/Projects/shokunin/{base.c,oom_kill.c,MANPAGE.md,main.c,meminfo.c,
sd-main.c,user@.service.in}`: all `absent`. `git -C fleet status --porcelain -z --untracked-files=all`
shows 6 untracked entries; depth-1 names are `AGENTS.md`, `live_s228.html`, `nama.html`, `tf_bavelas.html` —
none of the seven.

## 3. `misroot-hash-check.sh 27 f2de0ee`

Ran read-only (git status + sha256sum + `git grep` on the committed rev): printed `misroot_hits=0`, exit 0.
Mechanism verified against committed data: for each 16-hex prefix, `git grep -l -F <h> f2de0ee --
.ufo/waves/round-27/` resolves to ≥1 committed round-27 **w1** report (e.g. `cef1a2cf3f34f683` →
`w1/CriticInheritProbe.md`, `w1/SrcProcBaseOomScore.md`; `5ecdca43a8e0ed08` → `w1/HostUnitOomAdjust.md`,
`w1/CriticInheritProbe.md`), so the lesson's "each sha256 prefix is cited by a mori round-27 w1 report"
holds for all seven. Script logic re-read: only `?? ` porcelain entries that are regular non-symlink files;
`REV` resolved via `git rev-parse --verify` (exit 2 on bad rev); counts via `misroot_hits=` line.

## 4. Lesson M2 wording vs evidence (corpus/lessons/round-28.md "M2" bullet)

- "written at the fleet root during round 27 (mtime 14:08:55-03:00)": corroborated by
  `.ufo/waves/round-27/w2/ScoutMisroot.md:32` ("appeared together at 14:08:55 −03:00") and
  `w1/MisrootProvenance.md:26`.
- "each sha256 prefix is cited by a mori round-27 w1 report": verified (§3).
- "no other lane claims them … tsukuroi RevSeatScope.md:13 disowns them": verified;
  `tsukuroi-shokunin/.ufo/waves/round-27/w2a2/RevSeatScope.md:13` lists all seven as untracked fleet-root
  paths and records a tsukuroi-name grep returning nothing — observed and disowned, not claimed.
- "printed misroot_hits=7, exit 1 before … misroot_hits=0, exit 0 after": `evidence/misroot-before.txt`
  (run 18:01:15Z at rev `6ebd518f`) lists exactly the 7 `misroot` lines with cited-by reports, then
  `misroot_hits=7`/`exit=1`; `evidence/misroot-after.txt` (18:01:48Z) prints `misroot_hits=0`/`exit=0`.
- "copied byte-exact to the lane root (cmp ok) and the fleet copies deleted at 18:01Z, landed in
  `763d3469`": commit `763d34696a527f26efbceafd64b8a8138fbd344b` (2026-10-22 15:06:33 −03:00 = 18:06:33Z,
  after the deletion window) adds all 7 root files + the check script + both evidence files, is an ancestor
  of `f2de0ee`, and `git diff 763d3469 f2de0ee -- <the seven>` is empty. Byte-exactness is transitively
  anchored: committed sha256 = upstream sha256 = fleet-copy sha256 recorded in `MisrootProvenance.md:31-37`
  and `misroot-before.txt`.

## Findings

- **F1 (low, evidence/wording)** — M2 states "`tools/mori-misroot-sweep.py --lane mori --round 27` read
  `MORI_MISROOT_CLEAN` on them", past tense, but no run of that tool is recorded under
  `.ufo/waves/round-27/` or `.ufo/waves/round-28/` at `f2de0ee` (`git grep 'mori-misroot-sweep|MISROOT_CLEAN'
  <rev>` → only `misroot-hash-check.sh:2,5`, which describes the mechanism). The actual round-27 record,
  `w2/ScoutMisroot.md:13-14,33`, is a manual `git status` + content `grep` that returned 0 matches per file.
  The underlying claim is still supported — the tool's own docstring (`tools/mori-misroot-sweep.py`
  argparse epilog/doc: candidate only when a file "names a lane and a round"; `FINDING_CLEAN` at :57) plus
  ScoutMisroot's 0-match greps — so this is an unrecorded-or-paraphrased execution, not a wrong conclusion.
- **F2 (info)** — `meminfo.c` is byte-identical at earlyoom v1.8.2 and v1.9.0, and `user@.service.in` at
  systemd v261 and v262 (`MisrootProvenance.md:35,37,160-161`). Equality to upstream holds; the pinned tag
  rests on the r27 rows (S116/S130), not the bytes.
- **F3 (info, design scope)** — the check inspects untracked non-symlink regular files only; a misroot
  that became tracked/staged or matched fleet `.gitignore` would evade it. Stated limitation, matches its
  header; the seven were untracked, so irrelevant to this incident.

## Residual risk / verification gaps

- "cmp ok" and "deleted at 18:01Z" rest on `misroot-{before,after}.txt` and seat reports; the fleet copies
  are unrecoverable now — hash-chain evidence only.
- Four other depth-1 untracked files at the fleet root today (`AGENTS.md`, `live_s228.html`, `nama.html`,
  `tf_bavelas.html`) have zero round-27 hash citations (the check's own `misroot_hits=0`); provenance is
  outside this assignment's scope.
- I did not rerun `tools/mori-misroot-sweep.py` (it finds nothing to flag on an absent fileset); its CLI
  accepts `--lane`/`--round` as the lesson writes (`add_argument` block).
