# ScoutMisrootSweep — fleet-root misroot sweep for round 25 (wave 2, falsify)

**Verdict: HELD** for the sweep's own hypothesis — **no new untracked fleet-root path names
mori, round 25, or a MoriR25 seat.** The only untracked path at the fleet root carries zero such
markers. Three adjacent findings are real and belong to other lanes (two of them live misroots or
losses of another lane's artifact); none is a mori round-25 artifact.

Seat: MoriR25.ScoutMisrootSweep (leaf, read-only). Nothing was moved, deleted, created, or
written at the fleet root; the only file written is this report. No tool was installed.

## 0. Snapshots

| Snapshot | UTC | HEAD | porcelain lines | SHA-256 of porcelain bytes |
|---|---|---|---|---|
| baseline S3 (wave 1) | 2026-10-22T10:01:22Z | `31ba19e` | 18 | `732dd5878f5c…f731d7` |
| S4 (this seat) | 2026-10-22T11:40:33Z | `5d2774f` | 20 | `a257196be34e…85697b9` |
| S5 (this seat) | 2026-10-22T11:41:40Z | `5d2774f` | 20 | same `a257196b…` (S4→S5 delta empty) |

Commands: `git -C /home/vgpnk/Projects/shokunin status --porcelain`, then `wc -l` and `sha256sum`
on the captured bytes; `git rev-parse HEAD`.

## 1. Porcelain delta against the wave-1 baseline

Only three deltas exist at S5. `comm` over the two sorted line sets leaves 17 common lines.

| Δ | Line | What it is |
|---|---|---|
| added | ` M .ufo/l0-questions.md` | fleet-owned L0 queue, one appended line (see F4) |
| added | ` M .ufo/state/mado.report-baseline` | 68 B, `23 e3b0c442…` (sha256 of the empty string); no markers |
| removed | `?? .ufo/waves/round-51/` | **deleted from disk** since baseline (F2) |
| added (after 11:38:25Z) | `?? .ufo/waves/round-49/` | **new untracked dir** (F1) |

The first status of this seat, taken before 11:37:50Z, had **zero `??` lines** — so
`.ufo/waves/round-49/` is the only untracked path that has appeared at the fleet root in the
wave-2 window.

## 2. The asked question, answered literally

`git ls-files --others --exclude-standard` = **1** path (`.ufo/waves/round-49/falsify/RowGameDev2d.md`).
`grep -laiE 'mori|round[- ]25|MoriR25'` over that set returns **nothing**. So the requested list —
*every new untracked fleet-root path whose content names mori, round 25 or a MoriR25 seat* — is
**empty**.

The one untracked file, for the record (it is not a mori artifact):

| Path | Size | mtime (local) | mori | MoriR25 | `round 25` | `round-25` | `R25` |
|---|---|---|---|---|---|---|---|
| `.ufo/waves/round-49/falsify/RowGameDev2d.md` | 13,630 B | 2026-10-22 08:38:25 -0300 | 0 | 0 | 0 | 0 | 0 |

Header line 1: `# Falsify: C1 census row \`game-dev-2d\` (seat RowGameDev2d)`; judged at
`kotoba master c48793db…` against sibling pin `7753d49b…`. It is KotobaR49's seat output.

## 3. New fleet-root content that *does* name mori / round 25 (all tracked, all clean)

These are not misroots; they are the fleet owner's own records, and they are the reason a bare
`grep -l round-25` at the fleet root cannot be read as "mori wrote here".

| Path | Line | Marker counts | Reading |
|---|---|---|---|
| `.ufo/l0-questions.md` | 102 | mori 3, `round-25` 4 | **Uncommitted** added line: `mori \| round-25 \| Evidence for the hyaku capacity question above ("why the process enforces 100")…`. The capacity finding (`max(1, floor(min(100, async.maxJobs)))`, omp 18.12.6, binary byte 164406766) landing as an L0 question. mtime 11:36:27Z. |
| `.ufo/waves/hyaku/PHASE3.md` | 258, 293 | mori 37, **MoriR25 2**, `round-25` 4, `R25` 16 | Driver log: `Dispatch mori r25 attempt 1 (B4…); base 28b79d3d; L1 MoriR25`, and the 10:24Z sourcing-rule steer to all seven L1s. Also freeze/hard-stop lines `11:42:02 freeze mori r25`, `13:02:02 hard stop mori r25` (lines 324, 334) and the late-freeze note at line 349. |
| `MANIFEST.json` | 12916 | mori 163, `round-25` 13 | Rounds ledger; cites `mori-shokunin/corpus/lessons/round-24-verifier-spotcheck.md@28b79d3d1b76824f0c825aabe6cb6c5dc49961bf` — the same base commit C1 pins. |
| `.ufo/watchdog.log` | 552 (only `round-25` hit) | mori 30, `round-25` 1 | The single `round-25` hit is *chousa's* round 25 at 2026-10-21T02:47:21-03:00, pre-baseline. All 30 `mori` hits are lane-state/retry lines. |
| `.ufo/reports/round-49/kotoba.md` | 48, 100 | mori 4 | `mori` only as a lane name inside a `PROVINCE.md` census regex and a seat-id list. |

## 4. Findings

### F1 — Misroot: a kotoba r49 seat report landed in the fleet root (severity: medium, not our lane)

`.ufo/waves/round-49/falsify/RowGameDev2d.md` (13,630 B, written 11:38:25Z) is the **only** copy of
that seat's report:

* `kotoba-shokunin/.ufo/waves/round-49/falsify/` holds 19 `Row*.md` files (`RowAudio`,
  `RowChousa`, `RowGameDev3d`, `RowKagi`, `RowKaidoku`, `RowKake`, `RowKama`, `RowKasegi`,
  `RowKengaku`, `RowKotodama`, `RowKumitate`, `RowLore`, `RowMado`, `RowMori`, `RowRevenger`,
  `RowSouji`, `RowTabi`, `RowTameshi`, `RowTsukuroi`) but **no `RowGameDev2d.md`**.
* `git log --all -- .ufo/waves/round-49/falsify` is empty — the fleet-root copy has never been in
  any commit, while commit `ecb3a52` ("round-49: kotoba report addendum (late falsify seats)")
  already reports its verdict in prose (`RowGameDev2d` HOLDS-BOUNDED). The bytes backing that
  sentence exist only at the untracked path.
* This is exactly the misroot failure mode the baseline §8.3 asks the end sweep to catch — a
  `write` whose path lost its lane prefix. It is kotoba's, not mori's.

Smallest fix (owner action, not mine): kotoba's L1 copies the file to
`kotoba-shokunin/.ufo/waves/round-49/falsify/RowGameDev2d.md` and removes `.ufo/waves/round-49/`
from the fleet root. I did not move or delete it.

### F2 — Loss: the baseline's only untracked artifact is gone (severity: medium, not our lane)

`.ufo/waves/round-51/falsify/ReopenS113.md` (26,024 B at baseline, KotodamaR51a3's seat report) is
**absent from disk** at 11:40Z, absent from `HEAD`, and `git log --all -- .ufo/waves/round-51` is
empty — it never entered history. Something `rm`'d an untracked another-lane report between
10:01:22Z and 11:37:50Z. Not caused by this seat (read-only commands only). Cleanup of another
lane's untracked output is not in anyone's bounds as written, so this is an unowned deletion.

Smallest fix: kotodama's L1 confirms whether the report's content survives elsewhere (its lane or
a transcript); if not, it is unrecoverable and should be recorded as lost rather than assumed
cleaned.

### F3 — Name collision: fleet-root `round-25` is kama's, not mori's (severity: low, structural)

At the fleet root, "round 25" resolves to kama:

* `.ufo/reports/round-25/kama.md` — **new since baseline**: the directory had 6 tracked files at
  10:01Z (chousa, kagi, kake, kengaku, kotodama, tameshi) and has 7 now; `kama.md` was added by
  `f1a75c9 round-25: kama report` at 10:19Z. Content: `mori` 0, `MoriR25` 0, `round-25` 7,
  `round 25` 3 (line 1 `# kama — round 25 report (attempt 2)`).
* `.ufo/prompts/closure/kama-round-25.md` — tracked, `mori` 0, `round-25` 7.
* `.ufo/waves/round-25/` — empty (below).

Mori's round 25 lives **only** in `mori-shokunin/.ufo/waves/round-25/`. Any pass that greps the
fleet root for `round-25` and assumes it found this lane's contract or report is wrong. Smallest
fix: none in files — the round-25 contract and report paths are already lane-qualified; treat any
fleet-root `round-25` hit as kama's unless the path contains `mori-shokunin/`.

### F4 — Uncommitted fleet-owner L0 line naming mori round 25 (severity: low, fleet owner's)

`.ufo/l0-questions.md:102` (added 11:36:27Z, still ` M` at 11:41:40Z) is the mori round-25 capacity
L0 question. It is fleet-owned state and looks like the hyaku driver recording this lane's L0 —
correct behaviour, but it is **uncommitted**, so a leg that ends without a fleet commit loses it.
Smallest fix: hyaku commits the L0 queue with its next ledger commit; no action from this lane.

### F5 — Fleet-root `.ufo/waves/round-25/` still empty; its mtime moved in wave 2 (severity: low)

`find .ufo/waves/round-25 -type f | wc -l` = **0**; the tree is the directory plus an empty
`build/` (mtime 2026-10-21 04:32:22 -0300). The parent directory's mtime is **2026-10-22
07:55:34 -0300 (10:55:34Z)** versus 09:46Z at baseline, so a child entry was created and removed
there during the wave-2 window. No residue, no record of what it was, and it never appeared in
`git status` (an empty dir is invisible, and any file lived less than one snapshot apart).
Same-shaped new empty dirs exist for other lanes and look like driver round-dir creation:
`.ufo/reports/round-52` (10:32:12Z, 0 files) and `.ufo/waves/round-29` (11:30:22Z, 0 files).
Read: driver housekeeping, not a MoriR25 seat misroot.

### F6 — Pre-existing misroot classes unchanged (severity: low, informational)

All three baseline misroots are untouched at S5, same sizes and mtimes as baseline §3/§4:

* `write` — staged `A`, 25 B, content `agent://U100N079H334f935b` (no trailing newline); `mori` 0.
* `bash: ` — top-level dir whose name ends in a space, one file
  `…/souji-shokunin/tests/tools/souji-verify.sh: No such file or directory`; `find 'bash: ' -type f`
  = 1; ignored via the `*-shokunin/` component.
* `scripts/hyaku/__pycache__/append-closure.cpython-314.pyc` — staged `A`, committed-byproduct class.

No new file of the literal-`write` shape exists: `ls -b` at the fleet root lists exactly one
extension-less regular file, the same `write`.

## 5. Checks run, and what they cover

1. `git status --porcelain` ×2 (S4, S5), SHA-256 anchored; `comm` against the S3 line set.
2. `git ls-files --others --exclude-standard` (1 path) and `--others` (320 paths, 21 lane repos +
   `bash: ` + `.tower` 139 + `.jj` 120 + `.ufo` 36 + `.ruff_cache` 3). Baseline was 321; the one
   missing entry is F2's deleted report, so no new ignored path appeared.
3. `grep -laiE 'mori|round[- ]25|MoriR25'` over the untracked set (empty result) and a per-token
   count matrix over every fleet-root file with mtime > 10:01:22Z.
4. New-file enumeration with pruning:
   `find . \( -path ./.git -o -path ./.jj -o -name '*-shokunin' -o -name '*-shokukin' -o -path ./.ruff_cache -o -path ./.tower \) -prune -o -type f -newermt '2026-10-22T10:01:22Z' -print`
   → 18 files, all accounted for in §3/§4 above.
5. Empty-dir sweep at depth ≤ 3 and `find .ufo/waves/round-25` recursively (§4 F5).
6. `git log --all -- <path>` for both fleet-root wave-2 candidates and `git log --diff-filter=A
   31ba19ee..HEAD` to enumerate every path added by the fleet in the window (10 paths, all
   `.ufo/prompts/` or `.ufo/reports/` files for kake r29, kotoba r49, kama r25, kotodama r51/r52,
   mado r23, kake r29).
7. `grep -ac 'MoriR25'` on `.ufo/watchdog.log` = 0 and `git log -S'MoriR25' 31ba19ee..HEAD` = one
   commit, `521106f`, whose only added file is `.ufo/waves/hyaku/PHASE3.md` (fleet log).

## 6. Gaps

* Fixed-byte markers only: synonyms ("round twenty-five", `MORI-r25`) would not match.
* `.tower/` (139 paths) and `.jj/` internals were not content-read; lane repo contents were not
  swept (they appear as single ignored directory entries). Re-checked with a correct baseline
  epoch (1792663282): the only ignored path newer than baseline is the directory
  `kotoba-shokunin/` (mtime 11:14:17Z) — no new ignored file appeared.
* S4/S5 are instant-bound and the fleet root is live (HEAD moved `31ba19e` → `460caec` →
  `5d2774f` during this seat's run; the `??` set changed once). Use S5's hash `a257196b…` as the
  anchor for any later comparison, and re-run the §5.4 `find` rather than trusting this list.
