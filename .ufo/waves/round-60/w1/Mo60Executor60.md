# Mo60Executor60 — misroot probe: fleet root untracked set (round 60, w1)

Role: executor, leaf. Work mode: read-only. No commits, no VCS mutation, no production edits,
no fleet/sibling writes. Nothing was moved, deleted or renamed (the probe reports only).

Host guard: `scripts/hyaku/disk-guard.sh status` read before work — `/tmp` use 14% (111.2G free),
`/var/tmp` 38% (557.1G), `/fast/scratch/hyaku` 26% (600.0G). Green; no ENOSPC.

## Pins (every number below is re-derivable)

| Item | Value |
|---|---|
| Fleet root (probed) | `/home/vgpnk/Projects/shokunin` |
| Fleet-root toplevel | `/home/vgpnk/Projects/shokunin` (`rev-parse --show-toplevel`) |
| Fleet-root HEAD, snapshot 1 (13:09 -03) | `4fecd4db378fd66d422ab3a5076a3e753c5ec8d3` |
| Fleet-root HEAD, snapshot 2 (13:16:16 -03) | `fbe9c1f5ef63bc59a831e6f6e7fe33b84c093157` |
| Mori lane HEAD (observed, not used for scoring) | `b3c256138f00c704d5aa56eb0332d74506502ef2` |
| Entry revision named by the contract | `ddfb12fb0838b4307c445194a844f0c4b1950195` (not read this seat) |
| Scratch | `$HYAKU_SCRATCH/mori-r60/Mo60Executor60` (created, `TMPDIR` set, cleaned before yield) |

"Untracked" below means git's non-ignored untracked set (`git ls-files --others
--exclude-standard`); ignored paths are bounded separately in Command 5. Content predicate:
case-insensitive `mori` OR `round[-_ ]?60|r60`.

## Command 1 — the probe, no pathspec

```
git -C /home/vgpnk/Projects/shokunin status --porcelain
```

Snapshot 2, verbatim (9 lines; exit 0):

```text
 M .scratch/goal-20261028-hyaku-run11.md
 M .ufo/l0-questions.md
?? .scratch/closure-mado-r50.json
?? .scratch/closure-r54/
?? .scratch/source-routing-queue.md
?? .ufo/reports/round-45/kaidoku.md
?? o.bin
?? oldrep1.out
?? oldrep2.out
```

Snapshot 1 (13:09) was the same minus ` M .scratch/goal-20261028-hyaku-run11.md` — 8 lines.
The extra line is a mid-probe change, not a probe artefact (Command 6).

## Command 2 — expand the collapsed directory entries

```
git -C /home/vgpnk/Projects/shokunin ls-files --others --exclude-standard
```

**39 entries = 36 real files + 3 collapsed nested git repositories** (`.scratch/closure-r54/lane/`,
`.scratch/closure-r54/work-c2/clone/`, `.scratch/closure-r54/work-c2-base/clone/`). The 36 files are
the 3 root droppings (`o.bin`, `oldrep1.out`, `oldrep2.out`), `.scratch/closure-mado-r50.json`,
`.scratch/closure-r54/manifest-entry.json`, 24 files under `.scratch/closure-r54/work-c{0,1,1-base,c2,c2-base}/`
(scripts, `mirror/` copies of round-18/21 `measure.py`, and 14 `strace-*.log`), `.scratch/source-routing-queue.md`
and `.ufo/reports/round-45/kaidoku.md`.

## Command 3 — content test over all 36 untracked files

```
git -C /home/vgpnk/Projects/shokunin ls-files --others --exclude-standard \
 | while IFS= read -r f; do [ -f "$f" ] || continue
     m=$(rg -c -i 'mori' "$f"); r=$(rg -c -i 'round[-_ ]?60|r60' "$f")
     printf '%s mori_lines=%s r60_lines=%s\n' "$f" "${m:-0}" "${r:-0}"; done
```

Result: **0 of 36 files match.** Every row is `mori_lines=0 r60_lines=0`; the filtered tail is
empty (`NO_MATCHING_FILES`).

Matcher control (guards against a silently dead pipeline): `rg -c -i 'mori'` on a file known to
carry lane names returns non-zero, e.g. `.scratch/closure-r54/lane/corpus/lessons/round-45.md`;
`rg -c` on `.scratch/closure-r54/lane/PROVINCE.md` (no `mori` token) returns exit 1 / empty, which
is the same shape the 36 rows show.

## Command 4 — the 3 collapsed nested repos (what porcelain cannot see)

`git status --porcelain` prints each nested repo as one `??` line, so the untracked footprint is
under-reported by ~54,110 files / 832 MB:

| Nested repo | `remote.origin.url` | HEAD | files | size | porcelain lines |
|---|---|---|---|---|---|
| `.scratch/closure-r54/lane` | `/home/vgpnk/Projects/shokunin/tameshi-shokunin` | `0263c71ed6ec930603f5e37578ef46e498c96111` (`tameshi-shokunin`, 2026-10-28T12:25:51, branch `master`) | 23,983 | 362M | 1 |
| `.scratch/closure-r54/work-c2/clone` | `/home/vgpnk/Projects/shokunin/.scratch/closure-r54/lane` | `c21081008adbb6b6fe4e58a0aeec4831b30e318c` | 15,750 | 249M | 1 |
| `.scratch/closure-r54/work-c2-base/clone` | `/home/vgpnk/Projects/shokunin/.scratch/closure-r54/lane` | `d33053f7552db4bd290c99a36979760f544c41ad` | 14,377 | 220M | 1 |

All three working trees are clean (`status --porcelain | wc -l` → `0`). The `lane/` clone is a
**tameshi** round-54 closure clone, not a mori clone: `.scratch/closure-r54/manifest-entry.json`
reads `"lane": "tameshi"`, `"lane_round": 54`, `"commit": "tameshi-shokunin@0263c71e…"`.

Content scan inside each tree (`rg -l -i -g '!.git/**'`, identical result in all three):

- `mori` → **7 files**, all tameshi-side text that *names* mori as a peer lane:
  `considerthese/2026-10-23.md`, `corpus/knowledge/guard-kill-closure.md`,
  `corpus/knowledge/runner-tally-audit.md`, `corpus/knowledge/runner-tally-audit-v2.md`,
  `corpus/lessons/round-32.md`, `corpus/lessons/round-35.md`, `corpus/lessons/round-45.md`.
- `round[-_ ]?60|r60` → **1 file**, `corpus/knowledge/verification-patterns-fleet.md`, at
  `:169`, `:191`, `:259`, describing the fleet `reports/` form switch (`flat rN-*` through r59 →
  `round-NN/` from round-60). Not a mori artefact.
- `find … -type d -name 'round-60*'` → **0**.

Representative `mori` hit inside the closure tree (cross-lane manifest row, tameshi evidence):

```text
.scratch/closure-r54/lane/.ufo/evidence/round-18/final/measure-final.json:234
  "/home/vgpnk/Projects/shokunin/mori-shokunin/.gitignore": "b0cb500a…91dfa",
```

## Command 5 — ignored-space bound (closes the "untracked but gitignored" loophole)

```
git -C /home/vgpnk/Projects/shokunin status --porcelain --ignored=matching   # 131 lines
```

Ignored entries are the designed driver runtime (`.ufo/state/*`, `.tower/`, `.jj/`) plus the lane
directories (`/home/vgpnk/Projects/shokunin/.gitignore:1:*-shokunin/`). The only mori-named ignored
paths are `.ufo/state/mori.{mission,out,report-baseline,round}` and `mori-shokunin/`; no file in
that set carries the literal token `mori` or `round-60` in content (`rg -c` → 0 for all four
state files). Worth recording for the L1:

```text
.ufo/state/mori.report-baseline  (68 B, mtime 2026-10-28 11:57 -03)
60 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

i.e. round 60 registered against the **empty-blob** sha256 — the mori r60 report did not exist at
11:57. That state file is correctly placed (fleet driver state, gitignored by design), so it is not
a misroot; it is cited only because it *numerically* names round 60.

## Per-file ownership guess (report only)

| Path | Status | Content names mori / round-60 | Ownership guess |
|---|---|---|---|
| `.scratch/goal-20261028-hyaku-run11.md` | ` M` (tracked, index `H`) | yes — `:40` `\| 9 \| mori \| 60 \| 69 \|`, `:59`, `:69` | Operator / L0 run-11 goal doc. Tracked fleet-level orchestration file; **not untracked**, so out of the literal probe. Correct root. |
| `.ufo/l0-questions.md` | ` M` (tracked) | no (the 3 added lines are `kaidoku \| round-45`, not mori/r60) | L0 question ledger; tracked, correct root. |
| `.scratch/closure-mado-r50.json` | `??` | no | hyaku-closure, mado r50 (`"lane": "mado"`, `verdict: rejected-honest-stop`). Non-mori. |
| `.scratch/closure-r54/` (832M, 3 nested repos) | `??` | no (mori only as peer-lane rows inside tameshi evidence) | hyaku-closure on **tameshi** r54 (`manifest-entry.json`: `lane=tameshi`, `round=54`, `admitted=true`). Non-mori. Misplaced by hygiene (fleet-root `.scratch/`, should be under `$HYAKU_SCRATCH`), not by lane. |
| `.scratch/source-routing-queue.md` | `??` | no | hyaku orchestrator (L0) operator-directive routing queue, "run 10", mtime 2026-10-27 22:05. Non-lane. |
| `.ufo/reports/round-45/kaidoku.md` | `??` | no | **kaidoku** lane r45 report. The fleet dir is the canonical per-lane report location — 9 tracked siblings incl. `.ufo/reports/round-45/mori.md`; `kaidoku.md` is the only untracked one (mtime 13:14 today). Owner: kaidoku author + hyaku commit path. |
| `o.bin` | `??` | no | Unattributable from content: Cloudflare interstitial `<title>Just a moment...</title>` (5,867 B, no trailing newline, mtime 2026-10-27 16:58). Looks like `curl -o o.bin` output from a shortener/URL resolution (queue file routes `t.co` resolutions to revenger r72, so revenger/kagi are the plausible fetchers). Misrooted bare file at fleet root. |
| `oldrep1.out`, `oldrep2.out` | `??` | no | **tsukuroi** — byte-identical (`sha256 f8c8acfba89b45f4a5c015d1da0f0d33b610f620b0734026bd56dae6a12eb51c`, `cmp` equal) stdout of `tsukuroi-shokunin/tools/tsukuroi-census.sh` (`sha256 375aa737…2426`, 216,047 B), whose labels (`healthy: rc=1 backup-only sample is not a defect`, `degraded: foreign packages`, …) it reproduces verbatim; mt 09:10/09:11 today. Misrooted bare files at fleet root. |

## Findings

1. **No untracked file at the fleet root names mori or round-60.** 36/36 untracked files tested, 0
   hits, against the pinned fleet-root HEAD `fbe9c1f5` (and the same 36 files at `4fecd4db`).
2. **Misrooted material does exist at the fleet root, and none of it belongs to mori**: a 832 MB
   tameshi closure scratch tree, two identical tsukuroi census outputs, one Cloudflare fetch
   artefact, a mado closure entry, the L0 routing queue, and one kaidoku round report. Ownership
   per file in the table above. None was touched.
3. **Porcelain under-reports the root by ~54,110 files / 832 MB** because three nested git repos
   collapse to single `??` lines. A misroot gate that reads `status --porcelain` alone cannot see
   inside them; the `closure-r54/work-c2*/clone` remotes also point *at another scratch dir*
   (`…/closure-r54/lane`), i.e. clone-of-a-clone chains living inside a repo worktree.
4. **The fleet root is live, not quiescent.** Two commits landed during this probe —
   `7c63d1d9 2026-10-28T13:12:35 round-37: souji report erratum 9` and
   `fbe9c1f5 2026-10-28T13:14:44 round-37: hyaku closure dispatch for souji` — moving HEAD
   `4fecd4db → fbe9c1f5` and flipping `.scratch/goal-20261028-hyaku-run11.md` to ` M` between
   snapshots. Every number in this report is pinned to a named snapshot/revision for that reason.
   (Both commits touched `.ufo/prompts/closure/souji-round-37.md` and
   `.ufo/reports/round-37/souji.md` only — 2 files, 106 insertions / 8 deletions — so the misroot
   set was unchanged by them.)
5. **Nested-tree content that names mori is peer-lane prose, not misrooted mori product**: 7
   tameshi text files naming mori, 1 file naming round-60, 0 `round-60*` directories, and the
   `mori`-bearing hits are cross-lane manifest/ledger rows (example pointer above).

## Scope / non-actions

Read-only throughout. `git` was used only in read form (`status`, `ls-files`, `rev-parse`,
`log`, `diff`, `show`-free) on the fleet root and on the three nested repos; no `git -C` target was
mutated, nothing was committed, checked out, added, cleaned or gc'd. No file was created, moved or
deleted at the fleet root, in any lane, or in a sibling repo — the only writes were this report and
`$HYAKU_SCRATCH/mori-r60/Mo60Executor60` (removed before yield; its 3-line receipt is inlined
above). No pacman, no installs, no subagent dispatch, no `agent://all`.

## Blockers / risks

None blocking. Residual risks for the L1:

- The probe result is revision-bound: at `fbe9c1f5` (13:16) the answer is "no mori/round-60
  untracked file". Any later root write can change it; re-derive with Command 1 + Command 3 at a
  named HEAD rather than trusting a working-tree read.
- The literal predicate reads *content*. A mori r60 seat that writes into the fleet root under a
  gitignored path (`.ufo/state/*`, `.tower/`) would be invisible to `--exclude-standard`; the
  ignored-space bound in Command 5 currently shows only driver state, but that arm was measured
  once, not continuously.
- `o.bin` and `oldrep{1,2}.out` are unattributed-by-design droppings at the root; ownership above
  is inferred from emitted labels and fetch fingerprint, marked as inference, not proof.
