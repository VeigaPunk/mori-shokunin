# Scout — census and misroot sweep (round 33, wave 2)

Seat: MoriR33.ScoutCensusMisroot. Read-only; no lane edits. All commands run from
`/home/vgpnk/Projects/shokunin` (fleet root) unless a `-C` is shown. Tools installed: none
(no pacman, no uv, no binary drop) — nothing to record. Verdict is not a judge verdict.

Lane premise checked: `git -C mori-shokunin rev-parse HEAD` = `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8`
(clean for `corpus/SOURCES.md`, see F4). Census script identity:
`sha256sum scripts/sources-census.sh` → `3fb7261569f46423dd80ecc2…`.

## 1. Census validate — output and baseline comparison

Command (the frozen command from `.ufo/prompts/mori-round-33.md:65`):

```
cd /home/vgpnk/Projects/shokunin && timeout 120 ./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori; echo EXIT=$?
```

Output, verbatim (exit 0):

```
mori	W04	S035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in across scopes
mori	W04	S037 duplicate url www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html across scopes
mori	W04	S073 duplicate url docs.python.org/3/library/pathlib.html across scopes
mori	W04	S074 duplicate url kubernetes.io/docs/concepts/architecture/controller across scopes
mori	W04	S075 duplicate url ftp.gnu.org/gnu/bash/bash-5.3.tar.gz across scopes
mori	W04	S076 duplicate url michaelfeathers.silvrback.com/characterization-testing across scopes
mori	W04	S147 duplicate url raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/docs/settings.md across scopes
mori	W04	S148 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes
mori	W04	S149 duplicate url man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html across scopes
mori	W04	S150 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml across scopes
mori	W04	S166 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes
mori	W04	S168 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst across scopes
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
EXIT=0
```

Comparison with `mori-shokunin/.ufo/waves/round-33/evidence/census-start.txt`:

```
timeout 60 diff <now> census-start.txt
0a1
> 2026-10-23T02:27:00Z
13a15
> EXIT=0
DIFF_EXIT=1
```

**New W04 lines: none.** The only differences are the harness-captured timestamp header and the
trailing `EXIT=0` (census-start.txt is 15 lines, raw output 13). The 12 W04 rows are byte-identical.

**The comparison is not vacuous** (F1, severity none — supports C1's census claim):
`git -C mori-shokunin show <rev>:corpus/SOURCES.md | grep -c '^| S18[0-9] '` gives `0` at
`2796913` and `fdf4371`, `10` at `62db24c`; row count 179 → 190. census-start.txt was created in
`2796913` (round-33 freeze, file mtime 23:27, before the 23:55 data commit), so it predates
S180–S190 and the current run postdates them: **the 11 rows added this round introduced no W04.**

Mechanism (why that is airtight): `scripts/sources-census.sh:645` flags only the *later* row —
`if (u!="" && (u in url_seen) && !(scope_key in url_scopes))`. S180–S190 are appended last, so any
new duplicate URL would be flagged on the new row; none is. No `E0x` codes at all → no
duplicate-URL-within-scope rows (E04) and exit 0.

Duplicate-pair structure (evidence for the main agent, from `grep -F <url> corpus/SOURCES.md` +
scope extraction): each flagged row duplicates an older row under a different `scope` cell —
S035↔S013, S037↔S015, S073↔S069, S074↔S071, S075↔S070, S076↔S067, S147↔S101, S148↔S127,
S149↔S128, S150↔S129, S166↔S127/S148, S168↔S082. S166 and S168 are self-declared
"rejected candidate: same URL and bytes as …" rows, so these warnings are by design (W04, like the
other W-codes, does not fail validation — `scripts/sources-census.sh:33`).

Detector liveness (F2, severity none): `TMPDIR=<scratch> timeout 120 ./scripts/sources-census.sh
selftest` → `selftest ok`, exit 0, with `killed W04-scope-sensitive-mutant`,
`killed W04-does-not-fail-validation`, `killed E04-rejected-pair-exemption-mutant` among the killed
mutants — the W04 path is exercised, not dead.

Rooting (F3, severity none — **no misroot**): the id-based run and the explicit-dir run
(`validate --root /home/vgpnk/Projects/shokunin mori-shokunin`) differ only in the lane label
column (`mori` vs `mori-shokunin`); both print the same 12 rows and the same resolved path
`…/mori-shokunin/corpus/SOURCES.md`, exit 0. `shokunin.conf:63` maps `mori` → `mori-shokunin`
(one entry only). The census reads one file per lane, so its "scope" is the `scope` *column*, not a
filesystem scope — no cross-lane or fleet-root scan is involved.

F4 (severity none): `sha256sum mori-shokunin/corpus/SOURCES.md` =
`c2ef765e527cce02a44f8709fd7b5440…` = `git -C mori-shokunin show 62db24c:corpus/SOURCES.md |
sha256sum`; `git -C mori-shokunin diff --stat corpus/SOURCES.md` empty. The registry bytes the
census judged are exactly revision `62db24c` — unaffected by the in-flight edits in F8.

## 2. Fleet-root misroot sweep (`git -C /home/vgpnk/Projects/shokunin status --porcelain`)

Untracked files (all of them), with mtime and a `grep -il -e mori -e round.33 -e round33 -e r33`
verdict:

| path | mtime | size | mori / round-33 mention |
|---|---|---|---|
| `.omp/mcp.json` | 2026-10-22 21:45 | 285 | none |
| `AGENTS.md` | 2026-10-22 15:12 | 5921 | none |
| `bm.json` | 2026-10-22 18:28 | 5563 | none |
| `live_s228.html` | 2026-10-22 12:45 | 5196 | none |
| `nama.html` | 2026-10-22 14:24 | 68855 | grep hit only on `…Memories 1940-1944…` (false positive, F5) |
| `s395.txt` | 2026-10-22 19:12 | 0 | none (empty file) |
| `scripts/hyaku/__pycache__/wave-live.cpython-314.pyc` | 2026-10-22 14:06 | 10708 | none (build artifact) |
| `tf_bavelas.html` | 2026-10-22 12:45 | 5583 | none |
| `wb2.html` | 2026-10-22 20:37 | 620 | none |

Tracked-but-modified at the fleet root: 14 `.ufo/state/*.report-baseline` files and
`.ufo/watchdog.log` (+198 lines). Only one touches this round:
`.ufo/state/mori.report-baseline` `22 e3b0…` → `33 e3b0…` (HEAD value confirmed via
`git show HEAD:.ufo/state/mori.report-baseline`), consistent with the lane being in round 33;
`.ufo/watchdog.log` gained `2026-10-22T23:22:21-03:00 launch mori round=33 pgid=207913
driver=hyaku-inline attempt=1`. Both are the tracker's own home, not lane output — **not a misroot.**

Index entries present as intent-to-add (`git diff --cached` empty, `git diff --name-status` shows
`A`, blob `e69de29…`): `write` (25 bytes, content `agent://U100N079H334f935b`, mtime 2026-10-21
19:52), `scripts/hyaku/__pycache__/append-closure.cpython-314.pyc` (mtime 2026-10-22 05:01),
`.ufo/state/{kotoba,kotodama,revenger}.report-baseline`. F6, severity minor: a stray 25-byte
`write` file and a `__pycache__` artifact are registered in the fleet index — both predate the
round-33 window (23:22+), so not caused by this round. Not moved or deleted.

**No round-33 artifact exists at the fleet root:** `ls -d .ufo/waves/round-33` →
`No such file or directory`; `git grep -l -e round-33 -e disk-write-rate-r33 HEAD` returns only
fleet-owned files (`.ufo/prompts/mori-round-33.md`, other lanes' prompts/reports,
`.ufo/reports/round-33/{kake,kotodama}.md`) — no mori round-33 payload, and no `mori.md` under
`.ufo/reports/round-33/` yet (round still open). No `corpus/` or `SOURCES.md` copy for mori outside
`mori-shokunin/`.

F5 (severity minor, **not mori's**): the stray fetch artifacts belong to the **kotodama** lane —
`kotodama-shokunin/corpus/SOURCES.md` owns `S228` (Gullberg 2009), `S395` (Met Museum *Power Figure*)
and the only `Bavelas` row, matching `live_s228.html`, `s395.txt`, `tf_bavelas.html`, `nama.html`.
`wb2.html` is a Wayback "suspected abusive bot traffic" block page and `bm.json` is a Cloudflare
"Just a moment…" interstitial — saved blocked responses, not fetched content. All mtimes are
before mori's round-33 launch (23:22), so nothing here is this lane's. Reported for the fleet
record; I did not touch them.

F7 (severity none): the wave-2 dispatch is rooted in the lane, not the fleet root —
`.ufo/waves/round-33/wave2-spec.json` contains lane-relative `.ufo/waves/round-33/…` report paths
(`w1/*`, `w2`, `judge/JudgeC1Rows.md`, `evidence/census-start.txt`) and its only absolute
fleet-root string is the prompt reference `.ufo/prompts/mori-round-33.md:343-365`. No
`cwd`/`workdir` key is present in the spec. The fleet root has no `w2/` output directory, so no
wave-2 seat has written outside the lane.

## 3. Lane status (`git -C mori-shokunin status --porcelain`, no pathspec)

Untracked: `.scratch/`, `.ufo/waves/round-33/__pycache__/` (contains
`count-c1.cpython-314.pyc`, 27621 B, mtime 23:28), `.ufo/waves/round-33/w2/` (contains only
`swarm-registry.json`), `.ufo/waves/round-33/wave2-dispatch.json` (77787 B, 23:56:47),
`wave2-run.json` (85040 B, 23:56:46), `wave2-spec.json` (72077 B, 23:56:41), `wave2-run.err`
(0 B, 23:56:46). All are wave-2 harness/seat scratch; nothing tracked was modified at my first
snapshot (23:56).

F8 (severity none, live sibling work — flag for the integration owner): between my two snapshots
the lane gained two modified tracked files, `SCORECARD.md` (mtime 23:59:27, +17 lines: a
"## Round 33 declaration" section) and `SKILL.md` (mtime 23:59:45, +11/−5: five "Round33 rule"
bullets reworded). `git diff --stat` = 23 insertions, 5 deletions. Not a defect; noted because my
census snapshot predates them and because they are uncommitted at `62db24c`. Neither file affects
the census (which reads `corpus/SOURCES.md` only, F4).

## Severities

- F1 no new W04 / non-vacuous baseline — none (supports the round-33 census claim).
- F2 W04 detector selftest liveness — none.
- F3 census lane resolution identical by id and by explicit dir — none (no misroot).
- F4 census judged the exact bytes of `62db24c:corpus/SOURCES.md` — none.
- F5 fleet-root fetch artifacts all belong to kotodama, all pre-round-33 — minor, not mori's.
- F6 fleet index holds intent-to-add `write` + `__pycache__` artifact — minor, pre-round-33.
- F7 wave-2 dispatch rooted in the lane; no fleet-root round-33 output — none.
- F8 lane `SCORECARD.md`/`SKILL.md` modified uncommitted at 23:59 — none (live wave-2 work).

## Residual unknowns

- Who wrote `write`, the two `__pycache__` blobs and `bm.json`/`wb2.html` is not recorded anywhere I
  read; I attributed them only by mtime and by the kotodama source rows they match ([INFERENCE] on
  authorship, observed on content and mtime).
- `census-start.txt` is the round-start snapshot only; the prompt (`.ufo/prompts/mori-round-33.md:54-60`)
  also requires an *end-of-round* census with exit 0. My run is a mid-round "after", not that
  artifact — the end-of-round capture is still owed by the integration owner.
- I did not re-run the C1 judge (`count-c1-a1.py`); row-level support is outside this seat.
