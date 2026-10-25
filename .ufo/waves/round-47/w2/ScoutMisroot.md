# ScoutMisroot — mori round 47, wave w2 (falsify the landed round)

Seat: ScoutMisroot (leaf; no subagents dispatched). Date: 2026-10-25.
Scope: misroot sweep of the fleet root — read-only `git status --porcelain` plus
`tools/mori-misroot-sweep.py --lane mori --round 47`. **Nothing was deleted, moved, or edited**;
the only files written are this report and the seat's own scratch dir
`/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-ScoutMisroot/`.
Tooling: no install/update performed (operator directive RULES.md read first; none needed).

## 1. Commands run (verbatim) and outputs

### 1.1 `git -C /home/vgpnk/Projects/shokunin status --porcelain` (read-only)

rc=0. Full porcelain (`--untracked-files=all`), final snapshot at
`/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-ScoutMisroot/status-final.txt`:

```
 M .ufo/state/chousa.report-baseline
 M .ufo/state/kaidoku.report-baseline
 M .ufo/state/kama.report-baseline
 M .ufo/state/kasegi.report-baseline
 M .ufo/state/kengaku.report-baseline
 M .ufo/state/mado.report-baseline
 M .ufo/state/mori.report-baseline
 M .ufo/state/souji.report-baseline
 M .ufo/state/tabi.report-baseline
 M .ufo/state/tameshi.report-baseline
 M .ufo/state/tsukuroi.report-baseline
 M .ufo/watchdog.log
?? .ufo/waves/round-30/wave1/ScribeLesson.md
```

Counts: **12 modified tracked paths, 1 untracked path.** All 12 modified paths are fleet
infrastructure (11 `.ufo/state/*.report-baseline` round-counter files + `.ufo/watchdog.log`);
none is a lane report. `jj --repository . status` (read-only) agrees: same 12 modified + `?
.ufo/waves/round-30/`.

### 1.2 Misroot sweep tool

```
TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-ScoutMisroot \
  python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-misroot-sweep.py \
    --fleet-root /home/vgpnk/Projects/shokunin --lane mori --round 47
```

rc=0, one JSON line (saved to `.scratch/r47w2-ScoutMisroot/misroot-sweep.txt`):

```json
{"candidate_count": 0, "candidates": [], "detection_only": true,
 "finding": "MORI_MISROOT_CLEAN",
 "fleet_root": "/home/vgpnk/Projects/shokunin",
 "git_command": ["git","--no-optional-locks","-c","core.fsmonitor=false","-C",
   "/home/vgpnk/Projects/shokunin","status","--porcelain=v1","-z","--untracked-files=all"],
 "lane": "mori", "legacy_pathspec": null, "moves_or_deletes": false,
 "repo_root": "/home/vgpnk/Projects/shokunin", "round": 47,
 "scan": {"bytes_read": 1521, "non_regular_skipped": 0, "read_cap": 65536,
   "regular_files": 1, "truncated_files": 0, "unreadable": 0, "untracked_entries": 1},
 "schema": "mori-misroot-sweep-v1"}
```

Tool self-test (same TMPDIR): `python3 tools/mori-misroot-sweep.py --selftest` →
`{"arms":12,"finding":"MORI_MISROOT_SELFTEST_OK","fixture_sha256":"15f9f82d…","planted_found_with_legacy_pathspec":false,"planted_found_without_pathspec":true,"sandbox_unchanged":true,…}`, rc=0.

**The sweep's own scan surface agrees exactly with §1.1**: 1 untracked entry, 1 regular file,
1521 bytes read, none truncated/unreadable/skipped. Independent agreement.

### 1.3 Content scan of the untracked file against all 79 r47 seat names

Seat names harvested from `w1-spec.json` + `w2-spec.json` (`"name": "…"`), 79 distinct.
For `.ufo/waves/round-30/wave1/ScribeLesson.md`:

- `grep -oiE 'round[-_ ]?47|r47|mori'` → **rc=1, no matches** (the only `47` in the file is
  `rows 47` on line 4, a kasegi registry count, not a round token).
- Substring test of all 79 seat names → **`[]`, zero hits.**
- SHA-256 `687c0b93bdca7ba54fa4b818f9f70f2f2824ed6c5d5113685d32fb7fb24e0dcf`, 1521 bytes.

Modified tracked files were scanned the same way: 12 paths, **0** hits for
`mori.*round[-_ ]?47|round[-_ ]?47.*mori|r47w2` and 0 hits for any r47 seat name.

## 2. Verdict on the assigned question

**Holds.** *No untracked fleet-root file names mori round 47 or any r47 seat name.* The single
untracked fleet-root file is a **kasegi round-30** artifact, not a mori r47 artifact, and the
misroot sweep's `MORI_MISROOT_CLEAN` verdict for (mori, 47) is correct.

### 2.1 The one untracked fleet-root file — attributed to a sibling lane, NOT mori r47

`/home/vgpnk/Projects/shokunin/.ufo/waves/round-30/wave1/ScribeLesson.md` (untracked; not in
fleet `git ls-files`; birth 2026-10-25 15:58:07).

Evidence it is kasegi's round-30 `ScribeLesson` seat report, misrooted to the fleet root:

1. **Path shape**: `.ufo/waves/round-30/wave1/ScribeLesson.md` is exactly the kasegi spec trailer
   (kasegi `wave1-spec.json`, item `ScribeLesson`): *"Report (the lesson itself): .ufo/waves/
   round-30/wave1/ScribeLesson.md plus the lesson at corpus/lessons/round-30.md."* The path is
   lane-relative; the file landed at the fleet root instead of inside `kasegi-shokunin/`.
2. **The lane copy is absent**: `kasegi-shokunin/.ufo/waves/round-30/wave1/ScribeLesson.md` does
   **not** exist (`ls` → No such file). The lane has `ScribeLessonGate.md` (a different seat).
   So the file was not copied — it was written to the wrong root.
3. **Content fingerprint matches kasegi's lesson, not mori's**: the stray's distinct claims —
   `B2`, `stem mismatch`, `F14`, `rows 47`, `harness 17/17`, `M30`, `recheck-audit.py`,
   `proposals-ledger` — all appear in `kasegi-shokunin/corpus/lessons/round-30.md`
   (`grep -c`: B2→6, stem mismatch→1, harness 17/17→1, recheck-audit.py→3, M30→7), and in
   `mori-shokunin/corpus/lessons/round-30.md` the same probes give **0** for B2, F14, rows 47 and
   harness 17/17.
4. **Timeline**: kasegi's r30 wave-1 seat reports run 15:49→15:58; the stray's birth is
   15:58:07; kasegi's `corpus/lessons/round-30.md` mtime is 16:00:41; the fleet watchdog records
   `complete kasegi round=30` at 16:03:22. The stray sits inside kasegi's r30 wave-1 window.
5. **The lane's own corpus file was written correctly** (`kasegi-shokunin/corpus/lessons/
   round-30.md` exists) — only the *seat report* was misrooted, the classic one-sided misroot.

**This is a genuine misroot of a sibling lane (kasegi round 30), not of mori round 47.**
Per lane bounds it is reported, not touched; the kasegi L1 owns it. I did not delete or move it.

### 2.2 Why the sweep tool cannot see it (tool-coverage limit, not a tool bug)

The tool's predicate is **AND** over (lane token, round token) — `tools/mori-misroot-sweep.py`
lines 224-225 build `lane_rx`/`round_rx`, and a file is a candidate only if *both* hit (line
~311: `if not (lane_hit and round_hit): continue`). The stray's content names `round 30` /
`Round 30` / `corpus/lessons/round-30.md` but **never names its own lane** (`grep -ci kasegi` →
0). So:

- `--lane mori --round 47` → CLEAN (correct: it is not mori r47).
- `--lane kasegi --round 30` → **CLEAN** (rc=0, candidate_count=0) — the real owner cannot be
  detected by its own lane/round pair.
- `--lane round --round 30` → `MORI_MISROOT_CANDIDATE`, candidate_count=1,
  path `.ufo/waves/round-30/wave1/ScribeLesson.md`, `matched_in: ["content","path"]`.

Reproducer (read-only, lane tool, scratch TMPDIR):

```
python3 tools/mori-misroot-sweep.py --fleet-root /home/vgpnk/Projects/shokunin --lane round --round 30
→ MORI_MISROOT_CANDIDATE 1 ['.ufo/waves/round-30/wave1/ScribeLesson.md'] ['content', 'path']
```

**Verdict on the tool: it holds for the assigned question** (mori r47 clean is a true negative
here) **and its blind spot is now measured**: a lane's own misroot is invisible to that lane's
lane/round sweep when the seat report omits the lane id. The round-28 complement
`.ufo/waves/round-28/misroot-hash-check.sh` closes exactly this class by content hash, and I ran
it for this round:

```
bash .ufo/waves/round-28/misroot-hash-check.sh 47  → misroot_hits=0   (rc=0)
bash .ufo/waves/round-28/misroot-hash-check.sh 30  → misroot_hits=0   (rc=0)
```

`misroot_hits=0` for round 30 is expected and *not* a refutation: the script only greps the
**mori** lane's `.ufo/waves/round-N/` reports for the untracked file's sha256, and no mori r30
report cites the kasegi file's hash (`687c0b93…`). The hash complement is lane-scoped by
construction, so it is blind to a sibling lane's misroot exactly as the name-based sweep is.

## 3. Two fleet-root strays that `git status` cannot show (tool-coverage limit #2)

`git status` does not report **empty directories**, and the sweep tool only reads paths that
`git status` reports. Two empty directories therefore escape both instruments:

1. `/home/vgpnk/Projects/shokunin/ok/` — empty dir, birth **2026-10-25 16:43:05.478289356**.
   `git status --porcelain --untracked-files=all | grep -c '^\?\? ok'` → **0** (invisible);
   `git check-ignore -v ok` → no rule (not ignored, merely invisible because it is empty).
2. `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47-ScribeQuality/2echo/` — empty dir,
   birth **2026-10-25 16:43:05.478289356** — *the identical nanosecond as (1)*.

Both are empty and were created by one `mkdir`-style call at the same instant; the sibling name
`2echo` is a shell-redirect typo shape (`… >ok 2echo` / a stray `2>&1` fragment) rather than a
path any lane intended. The identical birth timestamps tie (1) to the same moment as mori r47
w1's `ScribeQuality` seat scratch dir — **[INFERENCE]** this is a mori r47 w1 seat running a
command with a relative path from the fleet-root cwd. Attribution to the exact seat command is
**UNVERIFIED**: I could not find the offending command in any w1/w2 report
(`grep -rniE 'mkdir.*ok|2echo'` over `.ufo/waves/round-47/` → no hits), and no report mentions
creating a fleet-root path. Reported as observed; nothing was removed.

I confirmed the invisibility mechanism with a controlled fixture (own scratch, read-only w.r.t.
the fleet):

```
D=<scratch>/fixture2; git init; commit base; mkdir -p "$D/emptydir"
git -C "$D" status --porcelain | grep -c emptydir   → 0
```

Empty dirs are not listed by `git status` at all, so no status-driven sweep can see them.

**Practical consequence for this round**: the instrument's `MORI_MISROOT_CLEAN` covers *untracked
regular files only*. It cannot certify the absence of an empty stray directory at the fleet
root, and it cannot certify the absence of a misroot whose report omits the lane id. Both
limits are now measured, not assumed.

## 4. w1 → w2 delta (the fleet-root surface changed between the waves)

The w1 seat `ExecMisrootBaseline` (`.ufo/waves/round-47/w1/ExecMisrootBaseline.md`, mtime
16:42:48) recorded **11 modified + 2 untracked**, the second untracked being
`corpus/knowledge/journalctl-v262-field-filter-r36.md` at the fleet root. At w2 time:

- The fleet root has **no `corpus/` directory at all** (`ls -d corpus` → No such file or directory;
  `git status … | grep -c corpus` → 0).
- That file now lives in the tsukuroi lane at
  `tsukuroi-shokunin/.ufo/waves/round-37/misroot/corpus/knowledge/journalctl-v262-field-filter-r36.md`
  (birth 16:56:10, mtime 16:08:07 — i.e. copied in with original bytes preserved, after the w1
  snapshot at 16:42:48).

**[INFERENCE]** tsukuroi round 37's L1/misroot sweep relocated its own fleet-root misroot into
its lane between the two waves. I did not find a tsukuroi report recording the move
(`grep -rn -i misroot` over `tsukuroi-shokunin/.ufo/waves/round-37/w1/` → no move record), so the
*action* is unrecorded; the *state change* is observed. Either way it is a sibling lane's
business, not mori's, and mori r47 wrote nothing at the fleet root.

Modified count rose 11 → 12 purely because `chousa.report-baseline` advanced 48→49 (chousa r49
launched 16:50:02 per the fleet watchdog).

## 5. Checks that the mori r47 wave wrote nothing at the fleet root

- **Seat-report placement**: every w1/w2 seat report name harvested from `w1-spec.json` /
  `w2-spec.json` was searched for in the lane repo; **0 misplaced**. All 31 w2 reports are under
  `mori-shokunin/.ufo/waves/round-47/w2/`, all 41 w1 reports under `…/w1/`.
- **No mori r47 file at the fleet root**: the fleet-level grep for `mori`+`round 47` / `r47w2`
  over every untracked and modified fleet path returned **0** hits.
- **Only one tracked fleet file names mori round 47 at all**: `.ufo/prompts/mori-round-47.md`
  (tracked, `git ls-files` confirms) — the fleet's own dispatch prompt, correct by construction.
  It is not a seat report and does not name any r47 seat name.
- **Sibling lanes are clean of mori r47 artifacts**: for each of the 22 `*-shokunin/` siblings,
  `grep -rlE 'mori-pin-check|count-c2\.py|CritC1Predicate|ScribeCatalogue|ExecC1Controls|MutC2Fields|SourcesSection'`
  → no hits in any lane. Sibling lanes also contain no `round-47`/`r47w2` content.
- **Lane-level hash complement**: `.ufo/waves/round-28/misroot-hash-check.sh 47` → `misroot_hits=0`.

## 6. Limits / UNVERIFIED

- **UNVERIFIED** — the exact command/author that created the empty fleet-root dir `ok/` and its
  sibling `2echo/` (identical birth nanosecond, no report or spec mentions either path). The
  [INFERENCE] that it is a mori r47 w1 seat running from the fleet-root cwd rests only on the
  timestamp coincidence with `mori-shokunin/.scratch/r47-ScribeQuality/`.
- **UNVERIFIED** — whether tsukuroi r37 moved its misroot deliberately (no report records it);
  the before/after state is observed.
- **Not checked** — content of any file beyond its first 65536 bytes (the sweep's own `read_cap`,
  and the documented limit of the instrument). Every file named in this report is far smaller.
- **Not checked** — files inside git-ignored fleet paths (`*-shokunin/` lane dirs are ignored by
  the fleet repo, as are `.ufo/waves/*/*-scratch/`); the fleet-root status surface cannot see
  them by construction. A targeted grep over the ignored scratch trees for
  `r47w2|mori.*round[-_ ]?47` returned no hits.
- The `.ufo/waves/round-30/` fleet-root directory is itself untracked as a whole; only its single
  file `wave1/ScribeLesson.md` is a regular file, and it is the one file the sweep inspected.

## 7. Bottom line

| Question | Verdict | Basis |
|---|---|---|
| Any untracked fleet-root file naming mori round 47 / r47 seat names? | **No — none** | 1 untracked file; 0 hits for `mori`/`r47`/`round-47`; 0 hits for all 79 r47 seat names |
| Sweep verdict for (mori, 47) | **`MORI_MISROOT_CLEAN` — correct** | tool scan surface == `git status` surface (1 entry / 1 file / 1521 B) |
| Did mori r47 write anything at the fleet root? | **No** | 0 misplaced seat reports; 0 mori-r47 hits across all fleet untracked+modified paths |
| Is there a real misroot at the fleet root? | **Yes — but it is kasegi r30's `ScribeLesson.md`**, not mori r47 | lane copy absent; content matches kasegi's r30 lesson (B2/F14/rows 47/harness 17/17) not mori's; birth inside kasegi's r30 w1 window. Reported, left untouched (not mori's to move) |
| Can the instrument catch a lane's own misroot? | **Not always** | AND-predicate needs lane+round; the stray names no lane ⇒ `--lane kasegi --round 30` = CLEAN. Measured; reproducer in §2.2 |
| Can the instrument see empty strays? | **No** | `git status` omits empty dirs (fixture-verified) ⇒ fleet-root `ok/` invisible to both `git status` and the sweep |
