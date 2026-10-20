# FleetRootUntracked — fleet-root untracked census baseline (mori round 17, wave 1)

Scope: one read-only census of `/home/vgpnk/Projects/shokunin` (fleet root) for the end-of-round
misroot sweep. No file was moved, deleted, or opened beyond its first 4096 bytes. No VCS mutation
was performed by this seat; the only write is this report, inside the lane checkout
(`mori-shokunin/.ufo/waves/round-17/build/`). Nothing was written under the fleet root.

## Probe

```
$ cd /home/vgpnk/Projects/shokunin
$ GIT_OPTIONAL_LOCKS=0 git status --porcelain        # exit 0
 M .ufo/watchdog.log
?? .ufo/reports/round-19/mado.md
?? .ufo/state/kaidoku.report-baseline
?? .ufo/state/kake.report-baseline
?? .ufo/state/kama.report-baseline
?? .ufo/state/mado.report-baseline
?? .ufo/state/mori.report-baseline
?? .ufo/state/souji.report-baseline
?? .ufo/state/tabi.report-baseline
?? .ufo/state/tameshi.report-baseline
?? .ufo/state/tsukuroi.report-baseline
```

Snapshot: **2026-10-20T18:57:06Z** (15:57:06 -03); re-run at 18:57:42Z gave the identical set.
Repo identity, same window: `git rev-parse --git-dir` → `.git` (no `.jj` at the fleet root),
branch `master`, `HEAD=206442a3bfa84bc23ac3c9f0f110ce13a2a88462` ("ops(hyaku): simplifier →
m_flash, distiller → m_haiku, planner stays m_opus", committer date 2026-10-20 15:56:33 -03).
The working tree is **live**: HEAD and two tracked files changed inside the census window
(see "Transients" below), so this set is a timestamped baseline, not a frozen state.

`git status --porcelain` default (`-unormal`) collapses wholly untracked directories; `-uall`
was used only to expand them. `git check-ignore -v` returned **rc=1** for both
`.ufo/reports/round-19/mado.md` and `.ufo/state/mori.report-baseline`, i.e. the entries are
untracked, **not** gitignored. Gitignored paths are outside this probe and were not enumerated.

## Untracked inventory (10 regular files, no symlinks, no untracked file-dirs)

| # | Path | Bytes | mtime -03 | SHA-256 (full) | Lane token | Round token | Token evidence in first 4 KiB |
|---|------|------:|-----------|----------------|-----------|-------------|-------------------------------|
| 1 | `.ufo/reports/round-19/mado.md` | 12652 | 15:34:57.035 | `ba01d2824b4222235d203164113509c7a2f18b8407e01869f2d951065c10f8fd` | `mado` / `mado-shokunin` | `round 19` (hyaku phase 2, attempt 1) | L1 `# mado — round 19 (hyaku phase 2, attempt 1)`; L3 "Lane `mado-shokunin`, branch `master`"; baseline `9c54c56…`; S084/S094/S096–S098; R18-V1..V4; criteria 24/26/27/28. No `mori`/round-17 token in the first 4 KiB. |
| 2 | `.ufo/state/kaidoku.report-baseline` | 68 | 15:28:56.860 | `e020abed1bff727275d7e3ed1f38254dad348b48ad06b3d35ed8716c275dee5d` | `kaidoku` | `19` | Content exactly `19 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 3 | `.ufo/state/kake.report-baseline` | 68 | 05:51:50.286 | `c20bb00a372c10e6504210f41ebea0bae14c5d281926a2439a99f71d37cdd48e` | `kake` | `21` | Content exactly `21 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 4 | `.ufo/state/kama.report-baseline` | 68 | 11:52:24.446 | `6f71be54bb490ab1899d969745fa567ee568e9b67956648e7c8d9bc752fc009b` | `kama` | `17` | Content exactly `17 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 5 | `.ufo/state/mado.report-baseline` | 68 | 13:54:20.747 | `e020abed1bff727275d7e3ed1f38254dad348b48ad06b3d35ed8716c275dee5d` | `mado` | `19` | Content exactly `19 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 6 | `.ufo/state/mori.report-baseline` | 68 | 15:26:13.456 | `6f71be54bb490ab1899d969745fa567ee568e9b67956648e7c8d9bc752fc009b` | `mori` | `17` | Content exactly `17 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 7 | `.ufo/state/souji.report-baseline` | 68 | 12:43:23.318 | `6f71be54bb490ab1899d969745fa567ee568e9b67956648e7c8d9bc752fc009b` | `souji` | `17` | Content exactly `17 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 8 | `.ufo/state/tabi.report-baseline` | 68 | 15:36:23.338 | `12c1c7c85c4040186cfb84c1f5da7d76f3dc03101d0caf72924870300a6a338c` | `tabi` | `18` | Content exactly `18 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 9 | `.ufo/state/tameshi.report-baseline` | 68 | 12:07:32.084 | `6f71be54bb490ab1899d969745fa567ee568e9b67956648e7c8d9bc752fc009b` | `tameshi` | `17` | Content exactly `17 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 10 | `.ufo/state/tsukuroi.report-baseline` | 68 | 15:38:14.789 | `12c1c7c85c4040186cfb84c1f5da7d76f3dc03101d0caf72924870300a6a338c` | `tsukuroi` | `18` | Content exactly `18 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

All ten are `regular file`. Content groups: rows 4/6/7/9 are byte-identical (round 17), rows 8/10
(round 18), rows 2/5 (round 19); row 3 alone (round 21).

## What the `.report-baseline` entries are (observed in code, not process-attributed)

`scripts/shokunin-watchdog.sh` is the producer of the format:

- header doc, lines 30-32: "`.ufo/state/<lane>.report-baseline` holds `round SHA256` for the
  report bytes captured immediately before launch or after a blocked source-gate check".
- `record_report_baseline()` at lines 121-137 writes `printf '%s %s\n' "$n" "$digest"` through a
  `.tmp.$$` + `mv -fT` atomic replace to `.ufo/state/<lane>.report-baseline`.
- `report_digest()` at lines 109-118: "a missing report is the empty byte stream"
  (`printf '' | sha256sum`).

Therefore the digest `e3b0c442…b855` — the SHA-256 of the **empty byte stream** — in all nine
files means that when each baseline was captured, the driver saw no
`.ufo/reports/round-<n>/<lane>.md` for that lane/round (absent, treated as empty, not an error
path). These are driver state files written at the fleet root by design; they are not seat files.

Cross-check against report presence at 18:57:28Z (`[ -f ]`):

| Lane | Baseline round | `.ufo/reports/round-<n>/<lane>.md` now | Note |
|------|---------------:|----------------------------------------|------|
| kama | 17 | ABSENT | consistent with empty digest |
| mori | 17 | ABSENT | consistent |
| souji | 17 | ABSENT | consistent |
| tameshi | 17 | ABSENT | consistent |
| tabi | 18 | ABSENT | consistent |
| tsukuroi | 18 | ABSENT | consistent |
| kaidoku | 19 | ABSENT | consistent |
| mado | 19 | PRESENT 12652 B (mtime 15:34:57) | report appeared **after** the 13:54:20 baseline capture |
| kake | 21 | PRESENT 11101 B, tracked | report appeared **after** the 05:51:50 baseline capture |

The driver's own `.round` counters do not equal the baseline rounds: `kaidoku=1, kake=16, kama=1,
mado=1, mori=2, tabi=1, tameshi=1, tsukuroi=1` (`.ufo/state/<lane>.round`), and `souji.round` does
not exist although `souji.report-baseline` does; souji also has no tracked `.mission`/`.out`/
`.round`. [INFERENCE] `.round`/`.report-baseline` are distinct driver counters (launch counter vs
report-round scope, cf. the round-scoping tests recorded at
`.ufo/waves/hyaku/kaika-w3/driver-retry-after.txt:25`), so a baseline round greater than the
`.round` value is not by itself a defect.

For the misroot question, the determined fact is: **none of the nine baselines nor the mado
report was written by this seat**, and all ten sit at paths the driver and the established lane
report convention expect at the fleet root. No mori-round-17 seat artifact is present at the
fleet root at snapshot time.

## Transients during the census window (not in the final set)

The tree changed while it was being censused; these are recorded so the end-of-round sweep can
distinguish "never existed" from "appeared and was withdrawn". None was touched by this seat.

1. `.ufo/waves/round-17/falsify/advice/ServedIdsMirror.md` — **appeared then removed**.
   - First probe (before 18:55:25Z): the fleet-root `.ufo/waves/round-17/` path did not appear in
     porcelain at all (the pre-existing `w1/` dir is empty, and git does not report empty dirs).
   - 18:55:59Z: `git status --porcelain -uall` showed it; point-in-time `stat` = regular file,
     **9639 B**, mtime **2026-10-20 15:55:25.949895279 -03**, sha256
     `afeb6d61064c6b04b8b0eea4dfd93cd318026d893497a7e49d535f9895cb7edd`. Default porcelain
     collapsed the whole tree to `?? .ufo/waves/round-17/`.
   - First 4 KiB: `VERDICT: partial — …`; a falsifier of kama C1's `served_model` invariant,
     comparing `tests/probe-verdicts/check.py` `served_ids_of()`/`expected_served_model()` with
     `tools/kama-probe.sh`; cites `kama-probe.sh:526-529`, D1–D5, rows exercising them. Tokens
     named: **kama**, C1, "falsify/advice", round-17 (by path). No `mori` token.
   - By 18:57:06Z the file and its `falsify/advice/` parents were gone (fleet-root
     `.ufo/waves/round-17/` mtime 15:56:19 -03); only the empty dir
     `.ufo/waves/round-17/w1/` remains (mtime 12:27:49 -03). Exact deletion instant not observed.
     The writer process was not observable from this seat: the content is kama-lane, while seat
     `KamaR17.ServedIdsMirror` was live in the roster naming this very advice dir; attribution is
     [INFERENCE].
2. HEAD moved inside the window: commit `206442a3` at 15:56:33 -03 touches exactly
   `.ufo/waves/hyaku/PHASE2.md` and `scripts/hyaku/lane-addendum.md` (`git show --name-status`).
   Both showed ` M` at 18:55:59Z and neither does at 18:57:06Z. Observed content churn on
   `scripts/hyaku/lane-addendum.md`: working sha256 `8c8438e9…` (content equal to the then-index
   blob) at 18:55:59Z → `9de6df75…` by 18:57:28Z, at which point the index blob held the same
   `9de6df75…`. `.ufo/waves/hyaku/PHASE2.md` working bytes equaled its index blob in both probes
   (stat-dirty only). This is another writer's VCS activity at the fleet root, not this seat's.
3. The only tracked modification in the final snapshot is `.ufo/watchdog.log`: 36089 B, mtime
   15:38:16 -03, sha256 `a26ca323312bf95b9b9bb582c43ebc752355f439f01b79d835f8a0c8bcf7f333`,
   `git diff --stat` = `+28` insertions. It is the driver log the watchdog appends; it is not a
   seat artifact and was left untouched.

## Commands run (all read-only; all exit 0 unless noted)

- `GIT_OPTIONAL_LOCKS=0 git status --porcelain` (no pathspec) — the commanded probe; snapshots at
  ~18:52Z (pre-transient), 18:55:59Z (transient visible only under `-uall`), 18:57:06Z,
  18:57:08Z, 18:57:42Z (stable 10-entry set).
- `GIT_OPTIONAL_LOCKS=0 git status --porcelain -uall` — expansion only.
- `GIT_OPTIONAL_LOCKS=0 git ls-files --others --exclude-standard`, `git ls-files`, `git ls-files -s`,
  `git rev-parse --show-toplevel|--git-dir|--abbrev-ref HEAD`, `git log -1`, `git show --name-status HEAD`,
  `git show :<path>`, `git diff --stat|--name-only`, `git check-ignore -v` (**rc=1**, not ignored).
- `stat -c '%F|%s|%y|%n'`, `sha256sum`, `dd if=<path> bs=4096 count=1` (byte cap enforced on every
  content read; one `dd` failed rc=1 when the transient had already been removed), `find
  .ufo/waves/round-17 -mindepth 1 -printf …` (names/sizes only), `ls`.

No file was moved, deleted, or modified. No background jobs, no services, no `/tmp` writes, no
journal queries, no pacman/uv/npm activity. **Tool installs: none.**

## How to use this as a sweep baseline

At end of round, re-run the exact probe at the same root and diff the untracked path set against
the ten rows above. A new untracked path is a misroot candidate if its first 4 KiB names a lane
other than the seat that wrote it, or if it lands under a fleet-root `round-*/`/`falsify/` tree
that is not wave-protocol content (cf. fleet-root `.ufo/waves/round-16/`, tracked protocol content
from commit `7c5b34f`; fleet-root `.ufo/waves/round-17/` currently holds no file, only an empty
`w1/` dir). Because the reported set moved twice in two minutes (advice file withdrawn, HEAD
advanced), any end-of-round comparison must record its own timestamp and `HEAD` and must re-run
`-uall` when the default output shows a collapsed `?? <dir>/`.

## Confidence and remaining unknowns

- Observed (certain): the ten-path set, sizes, mtimes, SHA-256, file types, ignore status, HEAD,
  the transient's bytes/hash, the driver code lines quoted, report-presence cross-check.
- [INFERENCE]: process-level attribution of each baseline (code-read producer, not an observed
  write); attribution of the transient advice file to `KamaR17.ServedIdsMirror`; that `.round`
  counters and baseline rounds are intentionally different counters.
- Unresolved: whether `.ufo/reports/round-19/mado.md` is the final round-19 mado report or an
  in-flight draft — its first 4 KiB carry the placeholder `⟨TIP⟩` and "attempt 1", and its
  baseline is a same-round empty digest, so the driver would see changed bytes; deciding
  completion is outside this item. Exact deletion instant and deleting process of the transient
  advice file were not observed.
