# RevMisroot — fleet-root mori-seat misroot audit (wave 2, re-derived)

Verdict: **PASS.** Exactly one mori-seat misroot existed at the fleet root
(`.ufo/waves/round-38/scratch/RevC4Anchors/mori-source-drift-f725f30.py`). It was
relocated into the lane by a concurrent actor while this seat ran; this seat
verified the relocation byte-exact against the canonical tip tool and verified the
current fleet root is clean with the lane's own detection-only sweep. No file is
proposed for deletion; the one unrelated-lane file that names mori/round-38 (hyaku's
driver card) stays.

No tools installed or upgraded (none needed; operator directive 2026-10-19: nothing
recorded).

## 1. Candidate, named

`git -C /home/vgpnk/Projects/shokunin status --porcelain` (run ~20:05:1x -03) showed,
expanded with `-uall`:

```
?? .ufo/waves/round-38/
# -uall: ?? .ufo/waves/round-38/scratch/RevC4Anchors/mori-source-drift-f725f30.py
```

The fleet-root `.ufo/waves/round-38/` tree contained exactly one file. It is a mori
round-38 wave-1 seat artifact (`RevC4Anchors` = wave-1 C4 anchors seat) rooted at the
fleet instead of
`mori-shokunin/.ufo/waves/round-38/scratch/RevC4Anchors/` → **seat misroot, must
live in the lane**. Content identifies the tool: line 2
`mori-source-drift.py — re-fetch each corpus/SOURCES.md row …`, line 55
`UA = "mori-source-drift/1.0"`; the path names both the lane (`mori`) and the round
(`round-38`).

## 2. sha256 + byte-exact cmp plan

Plan (as it applies to the misroot pair):

```
cmp /home/vgpnk/Projects/shokunin/.ufo/waves/round-38/scratch/RevC4Anchors/mori-source-drift-f725f30.py \
    /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-38/scratch/RevC4Anchors/mori-source-drift-f725f30.py
sha256sum <both>   # expected identical; canonical: 453c5d8e260301df7a99daf62b4c16ea08e4a0b4f9e4f53821cdbce447011552
```

The fleet side was removed by a concurrent actor before my `sha256sum` call
(batch-1 ~20:05:1x listed it, batch-2 ~20:05:5x got ENOENT). Executed equivalent
against the surviving lane copy:

- `git -C mori-shokunin show f725f3076972e6e70595b5ac8279be524a111ff8:tools/mori-source-drift.py`
  → sha256 `453c5d8e…1552`, 19676 bytes; identical at entering tip `e33bb561…` and at
  the worktree (tool unchanged across both tips).
- `cmp mori-shokunin/.ufo/waves/round-38/scratch/RevC4Anchors/mori-source-drift-f725f30.py /tmp/msd-f725f30.py`
  → **IDENTICAL**. Same for `tool_f725.py` (second lane copy) → **IDENTICAL**.
- Both lane copies: sha256 `453c5d8e260301df7a99daf62b4c16ea08e4a0b4f9e4f53821cdbce447011552`,
  19676 bytes; `RevC4Kill/original.py` (wave-1 receipt) is the same bytes.
- Chain of custody for the moved file: fleet listing at ~20:05:1x showed name +
  19.2 KB created 9 min prior; lane copy has mtime `2026-10-23 19:53:52` (a `mv`
  preserves mtime) and byte-size 19676 — consistent with a byte-preserving move.
  [INFERENCE] The move preserved bytes; see residual R1.

## 3. Concurrent remediation observed (not performed by this seat)

- 19:53:52 — fleet-root file created (mtime; creation predates wave-1 ScoutMisroot's
  snapshot, which is why w1/ScoutMisroot.md never saw it).
- ≤20:04:04 — lane `scratch/RevC4Anchors/tool_f725.py` written (mtime).
- ~20:05:1x→20:05:5x — fleet-root `.ufo/waves/round-38/` tree disappeared between my
  two `git status` snapshots; lane `scratch/RevC4Anchors/mori-source-drift-f725f30.py`
  appeared (mtime 19:53:52 preserved). `stat /home/vgpnk/Projects/shokunin/.ufo/waves/round-38`
  at 20:09:31 → `No such file or directory`; pathspec status empty.
- Timing anomaly, recorded honestly: my lane scratch listing at ≈20:05:1x did not yet
  show `RevC4Anchors/` although `tool_f725.py`'s mtime reads 20:04:04 — likely a stale
  directory listing; all hashes above were taken at 20:08:07. Attribution of the move
  is not established (mtimes carry no seat id; not investigated further — detection
  and report only).

## 4. Current fleet root: clean (canonical detector)

```
python3 mori-shokunin/tools/mori-misroot-sweep.py --fleet-root /home/vgpnk/Projects/shokunin --lane Mori --round 38
→ {"candidate_count": 0, "finding": "MORI_MISROOT_CLEAN", … "regular_files": 20, "unreadable": 0}
rc=0
```

Calibration of that negative: `--selftest` → `MORI_MISROOT_SELFTEST_OK` (rc=0):
the 847-byte path-only fixture is found without pathspec and missed by the legacy
pathspec, sandbox unchanged — so a mori+round-38-naming fleet-root file WOULD be
flagged. Independent binary-safe scan of all 20 untracked files (every byte, incl.
the two `.pyc`s) at 20:08:07: only hits are `.ufo/waves/hyaku/inline-run-20261023.md`
(`mori`) and `nama.html` (`mori` inside "Memories").

## 5. Non-candidates (NOT proposed for deletion)

- `.ufo/waves/hyaku/inline-run-20261023.md` — hyaku driver card; names mori only as a
  lane row (`| mori | 38 | 1 | 19:34 |`). Another lane's file: **keep** (concrete evidence: lanes 3–6, 43, 66 of wave-1's independent read; confirmed by my scan).
- `nama.html` — namuseum.gr 404 page; substring "Memories", not the token `mori`. Keep.
- `0`, `write`, `AGENTS.md`, `bm.json`, `live*.html`, `s395.txt`, `tf_bavelas.html`,
  `wb2.html`, `xc.xml`, `scripts/hyaku/*`, `.omp/mcp.json`, `.ufo/state/*` — no
  mori/round-38 content (bytes inspected); fleet junk / other lanes / infra. Out of scope.
- `.ufo/watchdog.log` — tracked-dirty, lane telemetry (`launch mori round=38 …`),
  never-touch path; read-only scan only.

## 6. Disposition

Fleet root requires **no further action**: the single misroot is already relocated
byte-exact into the lane's `scratch/RevC4Anchors/` (the canonical place — 34 files
under lane `.ufo/waves/round-38/` are tracked, `scratch/` is the seats' untracked
area, matching 36 sibling seat dirs), the tip-frozen tool bytes are intact, and the
canonical sweep reports `MORI_MISROOT_CLEAN`. Nothing deleted, nothing moved, no lane
file edited by this seat; this report is the only file written.

## Residual risk / verification gaps

- R1: The fleet-root bytes were never hashed (removed during a ~2-min observation
  window). Byte-exactness rests on name + 19.2 KB size + mtime preservation + the
  lane copy equaling the canonical tip tool. An in-place mutation between 19:53:52
  and the move is not falsifiable post hoc; impact bounded because the surviving lane
  copy is the pristine `tools/mori-source-drift.py`@f725f30 bytes.
- R2: Mover unattributed (see §3 anomaly). No ledger entry for file moves exists in
  scope.
- R3: The sweep's 64 KiB read cap truncated `nama.html` (68855 B); its only `mori`
  substrings sit below the cap and wave-1 full-scanned it — no gap in practice.
- R4 (observation, out of scope): lane has an untracked root-level `.scratch/`
  (lane-side convention question, not a fleet-root misroot).
