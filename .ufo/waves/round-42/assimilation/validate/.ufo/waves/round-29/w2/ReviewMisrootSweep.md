# ReviewMisrootSweep — fleet-root delta after wave 1 and CaseA207c sweep check

Seat: MoriR29.ReviewMisrootSweep (leaf, read-only). Sweep window 2026-10-22T20:31Z–20:38Z.
Lane `mori-shokunin` HEAD `8809a3fe1eaa87a0afa177a15263d174378e7462`; fleet HEAD `63729047644f839fe4c8cc97abd0d8bf741a5787`
(both via `git rev-parse`; matches the wave pins).
No tools installed (all pacman transactions paused host-wide; nothing was needed). No writes outside this file and
`/fast/scratch/hyaku/mori-r29/w2/MoriR29.ReviewMisrootSweep/sweep.txt`.

## 1. Verdict

- **Three untracked paths at the fleet root postdate the wave-1 baseline**; two are file-backed at the end of the
  sweep and one was transient:
  1. `.ufo/waves/round-33/w2/ScoutPinsFlagAccuracy.md` — **not mori**: a concurrent round-33 seat's report (§4).
  2. `mori-shokuhin/.ufo/waves/round-29/w2/Judge06.md` — **yes, a mori round-29 wave-2 seat wrote it** (§3). It sits
     under a misspelled lane directory (`mori-shokuhin`, missing the `n` in `shokunin`) created at **20:34:28Z**, i.e.
     during this sweep; it is a superseded draft of the correctly placed `mori-shokunin/.ufo/waves/round-29/w2/Judge06.md`
     written 13 s later. **This is a live misroot and needs L1 cleanup** (I am read-only; I did not touch it).
  3. `tools/fixtures/mori-oom-killers/cases-a2-r29-renamed.json` — **mori round-29 naming**, seen in `status` at
     **20:38:32Z** and already gone at 20:38:55Z (23 s later). Its bytes were gone before I could hash or read them
     (§3b); it left behind an empty `tools/fixtures/mori-oom-killers/` directory skeleton at the fleet root.
  The fleet root is therefore **not** clean of mori round-29 writes; seats are actively writing with the fleet cwd.
- The five baseline untracked paths are **bit-identical** to the baseline hashes; no baseline path was rewritten.
- **CaseA207c sweep confirmed**: `.ufo/waves/round-29/w1/CaseA207c.md` hashes to exactly
  `0fe85d0b2ce857cd954c6831ec907043590651ec47794760512f87f88a505a0a`, is the committed 14 015-byte blob, and
  `/home/vgpnk/Projects/shokunin/.ufo/waves/round-29/` **does not exist**; no copy exists anywhere else in the fleet
  tree either (§5).

## 2. Fleet-root untracked set (`git -C /home/vgpnk/Projects/shokunin --no-optional-locks status --porcelain -uall`)

| # | path | vs baseline | bytes | sha256[:16] | mtime (local -0300 → UTC) |
|---|---|---|---|---|---|
| 1 | `AGENTS.md` | unchanged | 5921 | `382f28ab4e2846a9` | 18:12:23Z |
| 2 | `live_s228.html` | unchanged | 5196 | `918d496cf0c3e6af` | 15:45:20Z |
| 3 | `nama.html` | unchanged | 68855 | `bee96464d0fe77f7` | 17:24:25Z |
| 4 | `tf_bavelas.html` | unchanged | 5583 | `9f07c0d0e4afa6ea` | 15:45:19Z |
| 5 | `scripts/hyaku/__pycache__/wave-live.cpython-314.pyc` | unchanged | 10708 | `a0b914e3bb3a8679` | 17:06:56Z |
| 6 | `.ufo/waves/round-33/w2/ScoutPinsFlagAccuracy.md` | **NEW** | 8705 | `753e5a794644d89c` | 17:18:18 -0300 = 20:18:18Z |
| 7 | `mori-shokuhin/.ufo/waves/round-29/w2/Judge06.md` | **NEW** | 2998 | `16432f46b4d9f4ef` | 17:34:28 -0300 = 20:34:28Z |
| 8 | `tools/fixtures/mori-oom-killers/cases-a2-r29-renamed.json` | **NEW, transient** | unknown | not captured | seen 20:38:32Z, gone 20:38:55Z |

Full 64-hex digests for rows 1–7 are in the scratch `sweep.txt`. Rows 1–5 match `w1/ScoutMisrootBaseline.md:12-18`
byte for byte. Row 6 was present at my first status run (≈20:31Z); row 7 appeared at 20:34:28Z, was captured in the
20:35:18Z evidence file and re-confirmed at 20:37:27Z; row 8 appeared and vanished between 20:38:32Z and 20:38:55Z
(§3b). So a single early `status` would have missed rows 7 and 8 — timing matters here, and a clean early read does not
prove a clean wave.

Everything else in the porcelain output is the churn the baseline already recorded, not new untracked content: 11
` M .ufo/state/*.report-baseline` (incl. `mori.report-baseline`), ` M .ufo/watchdog.log` (live fleet watchdog), and the
same five intent-to-add entries (` A .ufo/state/{kotoba,kotodama,revenger}.report-baseline`,
` A scripts/hyaku/__pycache__/append-closure.cpython-314.pyc`, ` A write` — `w1/ScoutMisrootBaseline.md` §2). None of
rows 6–8 was ever staged; the intent-to-add set is unchanged.

## 3. Row 7 — `mori-shokuhin/…/Judge06.md` is a mori round-29 wave-2 write (misrooted)

Observed:

- Directory chain `mori-shokuhin/.ufo/waves/round-29/w2/` is six empty-looking levels plus the one file; **every**
  directory in it carries mtime `2026-10-22 17:34:28 -0300` = 20:34:28Z, and `find mori-shokuhin -type f` returns only
  `Judge06.md`. The directory name is a typo of the lane (`mori-shokuhin`, no `n`); the file is not gitignored
  (`git check-ignore -v` exits 1).
- Content, `mori-shokuhin/.ufo/waves/round-29/w2/Judge06.md:1` — `# Judge06 — frozen case judgment`; `:3` — case
  ``r29-a2-10-zero-unbounded-mixed-sigterm`` (`tools/fixtures/mori-oom-killers/cases-a2-r29.json`), with BASE/FIX
  inputs named under `/fast/scratch/hyaku/mori-r29/L1/judge/`. I confirmed those three inputs exist:
  `ls /fast/scratch/hyaku/mori-r29/L1/judge/ | grep r29-a2-10-zero-unbounded-mixed-sigterm` returns `.base.json`,
  `.fix.json`, `.inputs.json`.
- Same document as the lane's wave-2 judge report: `mori-shokunin/.ufo/waves/round-29/w2/Judge06.md` is 3011 B,
  sha256 `c82d138ceb9dabaeebebaa9012c72c320999e7c252f32d26011e81ab9b6d9efb`, mtime 20:34:41Z. `cmp` says the two differ
  at char 1250, line 14; the whole `diff -u` is **one reworded cell** on the `earlyoom.actions.sigkill` row ("a
  nonnumeric-timestamp record is “left uncounted” and positive evidence elsewhere stands" → "a record without a numeric
  timestamp is “left uncounted” and positive evidence elsewhere still stands"). Everything else is identical.
- Reading: the stray is the **13-seconds-earlier draft** of the file that then landed at the correct lane path. A mori
  round-29 wave-2 judge seat ran with the fleet cwd and a misspelled destination, then rewrote to the lane path.
  [INFERENCE: author is the wave-2 judge seat responsible for `Judge06.md`; the file declares no seat id. Certainty of
  "mori round-29 artifact": high — the case id `r29-a2-10-…`, the L1 judge scratch paths, the `Judge06.md` name and the
  lane twin all agree.]
- Consequence: this is stale draft content under a path that is not part of the lane. It should be removed by the L1
  (or the seat's owner); anyone globbing `mori-shokuhin` or `*/Judge*.md` could otherwise read the superseded wording.

## 3b. Row 8 — `tools/fixtures/mori-oom-killers/cases-a2-r29-renamed.json` (transient, content not captured)

- `git status -uall` at **20:38:32Z** listed `?? tools/fixtures/mori-oom-killers/cases-a2-r29-renamed.json`.
- At **20:38:55Z** the same command no longer lists it; `stat` and `sha256sum` on the path both return
  `No such file or directory`. I have **no bytes, size or hash** for it — it disappeared within 23 s.
- What remains is evidence of the path, not the content: `find tools -maxdepth 4` now shows the empty skeleton
  `tools/fixtures/mori-oom-killers/` (dirs mtime 17:38 local = 20:38Z), and the fleet repo has **zero** tracked paths
  under `tools/` (`git ls-files tools | wc -l` → 0), so the skeleton is invisible to a file-only status.
- Reading: the name is mori round-29's own fixture namespace (`mori-oom-killers`, `cases-a2-r29`) with a `-renamed`
  suffix, and the lane fixture directory contains `cases-a2-r29.json` (54620 B, mtime 17:28 local) but **no**
  `-renamed` variant (`ls` → no such file). [INFERENCE: a wave-2 seat produced a renamed-ids variant of the frozen case
  file with the fleet cwd and then deleted or moved it; a mutation-test shape. Certainty of "mori round-29 origin":
  medium-high — the path names the tool and case set, but I could not read the bytes.]
- Consequence: because the file is gone, this is a **process** finding, not lingering content — but the empty
  `tools/fixtures/mori-oom-killers/` skeleton at the fleet root is new (mtime 20:38Z) and is itself fleet-root dirt that
  `git status` cannot show.

## 4. Row 6 — the round-33 path is not a mori artifact

- `.ufo/waves/round-33/w2/ScoutPinsFlagAccuracy.md:1` — `# ScoutPinsFlagAccuracy — is the freshness-pins.json flag
  accurate? (round 33, wave 2)`; `:3` — `Seat: KakeR33.ScoutPinsFlagAccuracy. Lane rev 0a0acfb1…`.
- Marker counts (`grep -ci`): `mori` = 0, `round 29`/`round-29` = 0, `earlyoom` = 0, `oom-killer` = 0, `kake` = 6,
  `ds4cc` = 14; subject matter is `corpus/knowledge/freshness-pins.json` and `SKILL.md:946` (`:15`, `:52`).
- It cites its own scratch `/fast/scratch/hyaku/kake-r33/w2/ScoutPinsFlagAccuracy/…` (`:4-6`) and ends on a finished
  bullet under `## 6. Unverified / remaining unknowns` (`:121`–`:128`), so it is not a half-written spill.
- `KakeR33` is a live peer of this run. [INFERENCE: that seat wrote it to the fleet-level `.ufo/waves/round-33/` tree,
  which the fleet already uses for round dirs.] Either way it is **not** a mori round-29 write and must not be counted
  as one. There is no `Report:` trailer in it (`grep -n '^Report:'` → nothing).

## 5. CaseA207c sweep verification (L1's claim, checked independently)

1. **Hash**: `sha256sum mori-shokunin/.ufo/waves/round-29/w1/CaseA207c.md` →
   `0fe85d0b2ce857cd954c6831ec907043590651ec47794760512f87f88a505a0a`, exact full 64-hex match.
2. **Identity**: first line `# CaseA207c — A2-07 blind cases`, with `"id": "r29-a2-07-dryrun-then-real-missing-enter"`
   in the JSON body — the digest belongs to the intended case file, not a namesake.
3. **Committed and undrifted**: `git ls-files -s` → `100644 66cc803a11efee7403f28acdf4bbc9e9ec485c3c 0 …`;
   `git cat-file -s` on that blob → `14015` = worktree size; `git diff --quiet HEAD -- <path>` exits 0. Landed in
   `e1c6bbe`.
4. **Absent at the fleet wave root**: `ls -d /home/vgpnk/Projects/shokunin/.ufo/waves/round-29` → `No such file or
   directory`; `git ls-files '*CaseA207c*'` at fleet → empty; `git ls-tree -r --name-only HEAD | grep -c
   'ufo/waves/round-29'` → `0`.
5. **No copy anywhere else**: two `find /home/vgpnk/Projects/shokunin -name 'CaseA207c*'` runs (whole tree excluding
   the lane `w1/` dir, 143.6 s, no output; and a depth-limited run, no output) return **only** the lane path. Sibling
   lanes' round-29 dirs (`kaidoku-shokunin`, `kengaku-shokunin`, `kake-shokunin`, `tsukuroi-shokunin`) contain no
   `CaseA207*`. Hardlink count is 1.
6. Distinct-path caution: the fleet root does have `.ufo/reports/round-29/` (fleet *report* dir, not the wave dir) with
   `kake.md`, `kengaku.md`, `kotodama.md`; `grep -rl A207c` there returns nothing.

Conclusion: the L1's CaseA207c sweep is **verified** — the file exists once, at the lane path, with the stated digest.

## 6. Empty directory skeletons at the fleet root (invisible to a path diff)

Pre-existing, from earlier rounds: `mori-shokukin/` (mtime 2026-10-21 09:53 local) and `tameshi-shokukin/`
(2026-10-21 02:50 local) — `find … -type f` returns 0 files for both, so `git status -uall` shows nothing, which is why
the wave-1 baseline did not list them. Their shape (`mori-shokukin/.ufo/waves/round-21/build`,
`tameshi-shokukin/tameshi-shokunin/.ufo/waves/round-19/w1`) shows this misspelled-lane misroot class recurs.

New this sweep: `tools/fixtures/mori-oom-killers/` (mtime 20:38Z) is the skeleton left by row 8; zero files, zero
tracked fleet paths under `tools/`. Both classes of skeleton are invisible to a file-only sweep, exactly like the
round-27-era baselines that used `git status` alone.

## 7. Method, discipline, disclosures

- Commands: `git status --porcelain -uall`, `git ls-files`, `git ls-tree`, `git ls-files -s`, `git diff --quiet`,
  `git cat-file -s`, `git rev-parse`, `git check-ignore`, `find`, `ls`, `stat`, `sha256sum`, `cmp`, `diff`, `grep`,
  `sed`. Every git call used `--no-optional-locks` with `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset, run directly
  against the lane and fleet repos — **read-only, no writes**; no sandbox clone needed and no jj command run.
- Timing disclosure: my first status (≈20:31Z) showed rows 1–6 only. Row 7 was created at 20:34:28Z, captured in the
  20:35:18Z evidence file and re-confirmed at 20:37:27Z. Row 8 was seen at 20:38:32Z and absent at 20:38:55Z; its bytes
  are lost to me. Any earlier "fleet root clean" reading of my run is superseded by §3 and §3b.
- Baseline comparison used `w1/ScoutMisrootBaseline.md` §1 table and its §6 constants.
- Privacy: no OMP setting, session id/path, uid, pid, unit name, journal message or `/etc/default` value appears here.
- The oom-killers tool was never opened or run (nor live, inputs, selftest or cases mode).
- Raw capture: `/fast/scratch/hyaku/mori-r29/w2/MoriR29.ReviewMisrootSweep/sweep.txt` (39 lines, 20:35:18Z).

## 8. Remaining unknowns

- Which exact seat id wrote row 7: the file carries no seat line; [INFERENCE] it is the wave-2 seat owning `Judge06.md`.
  Whether the L1 already noticed the draft is unknown to me.
- Row 8's bytes, size and hash: the file was gone 23 s after I first saw it, so its content is unrecoverable from my
  seat. Only the path name and the leftover skeletons attest to it.
- Whether the round-33 path is that flame's intended fleet-level location: round-33 L1's call, outside my seat.
- Baseline-era unknowns (author of fleet-root `AGENTS.md`; the `FixR1Runway.md` removal) are unchanged, not re-opened.

## 9. Hand-off for the L1 (read-only seat, no cleanup performed)

1. `rm` the stray draft `mori-shokuhin/.ufo/waves/round-29/w2/Judge06.md` and the `mori-shokuhin/` skeleton — it is
   stale content under a typo'd lane path. Empty dirs are invisible to git, but the file is real content and would enter
   any `git add -A` at the fleet root.
2. Re-run the after-wave `status --porcelain -uall` at freeze, not only once now: row 7 appeared 2.5 min after my first
   read and row 8 existed for under half a minute. A single pass cannot prove absence.
3. Treat the three empty skeletons (`mori-shokukin/`, `tameshi-shokukin/`, `tools/fixtures/mori-oom-killers/`) as
   known fleet-root dirt; they hold no bytes and no tracked paths.
