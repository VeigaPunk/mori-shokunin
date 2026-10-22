# ScoutMisroot — round-27 wave-2 fleet-root misroot sweep

Seat: MoriR27.ScoutMisroot (leaf). Task: list every untracked or modified path at the fleet root
`/home/vgpnk/Projects/shokunin` whose content names mori round 27 or a MoriR27 seat, and compare with
`/fast/scratch/hyaku/mori-r27/fleet-status-before-w1.txt`. Detection only; nothing was moved, edited or deleted.
No tool was installed (none needed).

## Method

- Snapshot: `git -C /home/vgpnk/Projects/shokunin status --porcelain` (read-only; no index writes).
- Baseline: `wc -l /fast/scratch/hyaku/mori-r27/fleet-status-before-w1.txt` → 20; baseline file mtime 12:45.
- First full snapshot 28 lines; a re-snapshot minutes later 29 lines (one other-lane report appeared, §5).
- Content test per status path: `grep -a -I -c -E 'MoriR27|mori|round[ _=-]?27' <path>`, plus a stricter
  same-line test `mori[^|]{0,40}round[- =]?27|round[- =]?27[^|]{0,40}mori`.
- Empty directories were checked by name (git cannot report them).

## 1. Paths whose content names mori round 27 or a MoriR27 seat — exact list: one path

| Path | State | Naming evidence | Verdict |
|---|---|---|---|
| `.ufo/watchdog.log` | modified vs HEAD (+112/−1) | `:712` `launch mori round=27` … `driver=hyaku-inline attempt=1` (pgid omitted here by the privacy bound) | expected orchestrator log, not seat debris |

- No status path contains the literal `MoriR27`: the strict seat-id loop over every status path printed no hit.
- The same-line test printed exactly one line, `.ufo/watchdog.log:712`; the working-tree line is a `+` addition
  relative to HEAD. This file is fleet-level and logs every lane (`:714` names another lane's round 31); it is
  modified as designed by the orchestrator, not a round-27 seat writing outside its area.
- Because the baseline file records paths, not content, I cannot prove whether `:712` already existed at 12:45
  (it is stamped 12:35:27, before the baseline snapshot). It is in the working tree either way.

## 2. New since baseline, no round-27 naming in text, but round-27 source bytes at the fleet root

Seven untracked files appeared together at 14:08:55 −03:00, after the 12:45 baseline. `grep`
for `MoriR27|mori|round[ _=-]?27` returned 0 for each. Their linkage to round 27 is byte identity, not text:

| Path (fleet root) | sha256 (short) | Round-27 SOURCES row | Byte-identical scratch copy |
|---|---|---|---|
| `base.c` | `cef1a2cf…` | S127 `fs/proc/base.c` v7.2 | `/fast/scratch/hyaku/mori-r27/SrcProcBaseOomScore/base.c` |
| `oom_kill.c` | `452f1348…` | S003 `mm/oom_kill.c` | `…/SrcProcBaseOomScore/oom_kill.c` |
| `MANPAGE.md` | `cc48b02e…` | S115 earlyoom MANPAGE | `…/SrcEarlyoomManpageOptions/MANPAGE.md` |
| `main.c` | `08656b0b…` | S119 earlyoom `main.c` | `…/SrcEarlyoomManpageOptions/main.c` |
| `meminfo.c` | `526e512c…` | S116 earlyoom `meminfo.c` | `…/SrcKillCSelection/meminfo.c` (also 4 other wave-1 scratch dirs) |
| `sd-main.c` | `5ecdca43…` | S130 systemd `src/core/main.c` | `/fast/scratch/hyaku/mori-r27/sd-main.c` |
| `user@.service.in` | `72c2f40d…` | S130 per-user service unit | `…/SrcSystemdUserService/user@.service.in` |

- `cmp -s` confirmed identity for all seven (`IDENTICAL` for each pair).
- The hash of `user@.service.in` also matches `…/w1/SrcSystemdUserService.md:129`; `base.c`, `oom_kill.c`,
  `meminfo.c` hashes match `…/w1/SrcProcBaseOomScore.md:135` and `…/w1/CriticC1Novelty.md:152`.
- Round-27 source provenance, confidence: high (seven independent sha256 equalities to wave-1 captures).
- Which seat left them: **unresolved**. Bounds forbid reporting pids and command lines; no process held these
  files open at scan time (`lsof …` printed no rows), and 25 processes had a cwd equal to the fleet root
  (count only; no ids read out). [INFERENCE] a wave-2 seat copied the wave-1 captures with its cwd at the fleet
  root instead of using its scratch directory; the one-shot 14:08:55 mtimes fit a copy loop, not edits.
- Severity: medium. The bytes are public upstream sources and carry no private data, so no privacy harm; but the
  lane bound says scratch goes under `/fast/scratch/hyaku/mori-r27/<seat>/`, and these seven files are round-27
  debris in a repository that must stay clean at the fleet root.

## 3. New since baseline, unrelated to round 27

| Path | State | Evidence | Verdict |
|---|---|---|---|
| `scripts/hyaku/__pycache__/wave-live.cpython-314.pyc` | untracked | binary interpreter cache; 0 naming hits | incidental cache from running the fleet `wave-live` script; not round-27 content |

The companion `scripts/hyaku/__pycache__/append-closure.cpython-314.pyc` was already staged at baseline.

## 4. Baseline-present paths checked, no round-27 naming

| Path | Baseline state | Content check |
|---|---|---|
| `write` | ` A` (staged) | one internal agent URI token; not reproduced here (privacy); no round-27 text |
| `live_s228.html` | `??` | bot-challenge page; 0 naming hits |
| `tf_bavelas.html` | `??` | bot-challenge page; 0 naming hits |
| `.scratch/goal-20261022-hyaku-12h.md` | ` A` | names mori only as `mori r24` at `:86,:102`; no round 27 |
| 15 × `.ufo/state/*.report-baseline` | modified | one-line pointer `NN <sha256>`; no `mori`/`round 27` text. `mori` pointer changed `22`→`27` with the unchanged hash of empty input (`git diff` hunk at `:1`) |

## 5. Baseline comparison

- Baseline 20 lines; current 28 lines at the first full snapshot: **8 added, 0 removed, 0 state changes**.
  The 8 additions are the seven source files in §2 and the `.pyc` in §3.
- During the scan a 29th line appeared: `?? .ufo/reports/round-31/kake.md`. Content check 0 naming hits for
  `mori|MoriR27|round.?27`; `:1` reads `# kake round 31 report …`. Another lane's artifact, not round 27.
- Empty directory not visible to git: `.ufo/waves/round-27/residual/` at the fleet root, created
  10:48:19–10:48:53 −03:00 (pre-baseline), contains nothing. Naming is round-27 but the directory is empty and
  inert; low severity.
- Ignored entries were not expanded (sibling lane checkouts and old wave scratch dirs, e.g. `chousa-shokunin/`,
  `audio-shokunin/`); no visible ignored root name names mori round 27. Strictly out of the requested
  `status --porcelain` set.

## 6. Unresolved

- Seat attribution for §2 (no pid/command-line evidence may be read out under the bounds; no writer held the
  files open).
- Whether the seven files are still needed by a running wave-2 seat; deleting or moving them is left to the
  integration owner, as instructed.
- Baseline carries paths only, so content-level drift in baseline-present files (e.g. watchdog line 712) cannot
  be dated from it.

## 7. Action suggested to the integration owner (not taken by this seat)

Remove or relocate the seven §2 files after confirming no seat needs them, and drop the stray `.pyc`; the empty
`.ufo/waves/round-27/residual/` can be ignored. No lane file was touched by this seat.
