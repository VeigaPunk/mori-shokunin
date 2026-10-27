# Mo56ExecMisroot — round 56, wave w1 (misroot pre-sweep, read-only)

Seat scope: fleet-root misroot pre-sweep. Run
`git -C /home/vgpnk/Projects/shokunin status --porcelain` (no pathspec) and
list every untracked file at the fleet root or under
`/home/vgpnk/Projects/shokunin/.ufo` that could belong to mori round 56
(content names mori / round 56 / Mo56). Detection and report only — nothing
was mutated: no `git add/commit/stash/checkout/reset/pull/push` in the fleet
repo or the lane repo, no mutating `jj` command, no write to `.ufo/state/`,
`.ufo/watchdog.log`, `.scratch/` or another lane's files, no sysctl/cgroup/
systemctl/process-kill.

- Fleet root: `/home/vgpnk/Projects/shokunin`
- Lane repo (separate git repo): `/home/vgpnk/Projects/shokunin/mori-shokunin`
- Scratch used and removed: `/fast/scratch/hyaku/mori-r56/Mo56ExecMisroot/`
- Fleet HEAD at sweep time: `0ba76c42` ("rounds ledger: kake r63 closure
  (rejected-honest-stop) — hyaku, non-author")
- Lane freeze tip named by the L1: `8be2717b0809281d07dffe83dad424a4859e0747`
- Tool installs: none (no pacman, no uv/npx installs; read-only sweep needs none)

## 1. The requested command

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain
?? .scratch/closure-mado-r50.json
?? .ufo/reports/round-53/tameshi.md
?? .ufo/reports/round-56/mori.md
exit=0
```

Three untracked paths at the fleet root, two of them under `.ufo`.
Repeated twice during the sweep with the same output (stable).

## 2. Classification of each untracked path (mori round 56 or not)

| Path | mori r56? | Evidence |
|---|---|---|
| `/home/vgpnk/Projects/shokunin/.ufo/reports/round-56/mori.md` | **YES** | Content names the lane and the round: first line `# mori round 56`; line 3 `Lane: mori-shokunin (fleet & host observability, 森). Attempt 1, L1 MoriR56.`; body names the C1/C2 tools `tools/mori-driver-liveness.py` and `tools/mori-vote-bind.py`, the freeze commit `8be2717b`, the data commits `c419fe6d` / `6ced9da9`, the freeze commit `3f494b49`, and the wave `w1` with 64 seats. 6744 bytes, mtime 2026-10-27 11:02:49. |
| `/home/vgpnk/Projects/shokunin/.ufo/reports/round-53/tameshi.md` | no | Round 53, lane tameshi: first line `# Tameshi round 53 — cold-read floor repair (calibration) + tools scratch hygiene (operability)`; names lane base `6db1d220`, freeze `e62d9971`, `.ufo/evidence/round-53/freeze.json`. No mori/round-56 marker (grep for `mori|round-56|Mo56` returns nothing). |
| `/home/vgpnk/Projects/shokunin/.scratch/closure-mado-r50.json` | no | Round 50, lane mado: `{"round": 50, ... "lane": "mado", "lane_round": 50, ...}`. Outside `.ufo`, in the operator-reserved `.scratch/` tree (not touched, not written). |

So exactly **one** untracked file at the fleet root / under fleet `.ufo`
belongs to mori round 56: `.ufo/reports/round-56/mori.md`.

## 3. Context that changes the "expect none yet" expectation

The seat brief expected "none yet (the wave has not run)". That expectation
is stale at sweep time — the wave had already been dispatched and this seat
is itself part of it:

```
$ grep -n 'mori 56' /home/vgpnk/Projects/shokunin/.ufo/state/inline-dispatcher.log | tail -3
60503:2026-10-27T11:08:04 partial mori 56 w1 61 64
60504:2026-10-27T11:08:04 cap-defer .../mori-shokunin/.ufo/waves/round-56/w1.ready occupied 96
60507:2026-10-27T11:08:27 spawned mori 56 w1 64
```

(read-only read of the fleet log; no write.)

The untracked `.ufo/reports/round-56/mori.md` is therefore the L1's own
round-56 report, sitting at the fleet root before the L1's integration
commit. Every sibling lane's round-56 report is already tracked at the same
fleet-root location, so the convention is established and the file is
correctly placed:

```
$ git -C /home/vgpnk/Projects/shokunin ls-files .ufo/reports/round-56/
.ufo/reports/round-56/chousa.md
.ufo/reports/round-56/kake.md
.ufo/reports/round-56/kotoba.md
.ufo/reports/round-56/kotodama.md
.ufo/reports/round-56/kumitate.md
$ git -C /home/vgpnk/Projects/shokunin ls-files --error-unmatch .ufo/reports/round-56/mori.md
error: pathspec '.ufo/reports/round-56/mori.md' did not match any file(s) known to git
```

The lane's own working copy of the same report is
`/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/report-draft-r56.md`
(1327 bytes, mtime 11:00:06), which the L1 expanded into the fleet-root
file.

## 4. Method limitation the post-wave sweep must know (fleet-root porcelain cannot see mori r56)

The fleet root `.gitignore` ignores the whole lane-repo subtree
(`.gitignore:1  *-shokunin/`). Therefore **no mori round-56 wave artifact can
ever appear in fleet-root porcelain** — not the contract, counters, controls,
fixtures, evidence, source rows, or the 40 seat reports. The mori r56 corpus
lives in the lane repo, which is its own git repository
(`git -C …/mori-shokunin rev-parse --show-toplevel` → the lane dir;
`--git-dir` → `.git`).

Lane-repo porcelain, for the record (read-only `git status --porcelain`):

```
 M LOG.md
 M SCORECARD.md
 M SHONEN.md
?? .ufo/waves/round-56/w1/            (40 seat reports + swarm-registry.json)
?? .ufo/waves/round-56/w1.ready
?? .ufo/waves/round-56/w1.ready.dispatched
?? corpus/lessons/round-56.md
```

All of these are inside the lane repo (not the fleet root) and are the
expected in-wave shape: the L1's own integration edits plus the wave's
seat-report directory. A misroot sweep limited to the fleet root would
report "one mori r56 file" and miss the whole lane-side wave surface; the
post-wave sweep must run both.

## 5. Untracked-but-ignored fleet-root material (excluded by rule or by .gitignore)

`git status --porcelain --ignored=matching -uall -- .ufo` (fleet root) lists
122 ignored entries; the classes relevant to a misroot sweep:

- `.ufo/state/*` — fleet runtime state (`.gitignore: .ufo/state/*`). Includes
  `mori.mission`, `mori.out`, `mori.report-baseline`, `mori.round`
  (`mori.round` contains `2`). **Read-only, never touched** per the seat
  spec; the lane's own `mori.round` value is driver bookkeeping, not mori
  round-56 material.
- `.ufo/watchdog.log` — the fleet's live driver log (163775 bytes, mtime
  10:56). Contains exactly one mori round-56 driver line
  (`2026-10-27T10:08:36-03:00 launch mori round=56 pgid=620717
  driver=hyaku-inline attempt=1`). Read-only; never written.
- `.ufo/waves/shokunin-train-2026*/x{sconnector,entinel}-scratch/` — other
  waves' transient scratch, unrelated to round 56.
- `.tower/` (fleet root, ignored) contains
  `.tower/quarantine/fleet-root-strays-20261027T0600/mori-r55-closure-entry.json`
  — a **round-55** mori closure entry (2487 bytes, mtime 04:32), inside the
  quarantine slice the contract mentions ("quarantine slice re-derived"). Not
  round 56; recorded only so the post-wave sweep does not re-flag it.

## 6. Misrooted mori round-56 artifacts OUTSIDE the fleet root and outside the seat-scratch rule

The operator scratch directive (2026-10-25) requires every clone, work tree,
fixture and temp file to live under
`/fast/scratch/hyaku/mori-r56/<seat>/`, and states that a `/tmp` path is
never evidence. The sweep found mori r56 material that landed in `/tmp`.

### 6.1 A **mutant** of the frozen C1 tool left behind in `/tmp` (still present)

```
$ ls -la /tmp/mori-driver-liveness.py
-rwxr-xr-x 1 vgpnk vgpnk 18301 Oct 27 11:00 /tmp/mori-driver-liveness.py
$ sha256sum /tmp/mori-driver-liveness.py
93fe821b992a2da46c6c3a32d054097fd1e7861097bb3b23c3b98ebe6c2f55ea  /tmp/mori-driver-liveness.py
$ sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-driver-liveness.py
6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997  …/tools/mori-driver-liveness.py
```

Byte-diff against the committed tool — the event-keyword alternation is
narrowed to `launch` only (one line, the tool's `LINE_RE`):

```
55c55
<     r"^(\S+) (launch) ([A-Za-z0-9_-]+) round=(\d+)(.*)$")
---
>     r"^(\S+) (launch|complete|lane-dead-no-report|launch-fail|wrap) ([A-Za-z0-9_-]+) round=(\d+)(.*)$")
```

This is not the frozen tool and not a copy of it — it is a deliberately
weakened variant. It is materially wrong: on the frozen fixture
`fixtures/driver/two-lanes` the stray reports a lane as still in flight with
no completion, where the committed tool reports the completion:

```
$ python3 /tmp/mori-driver-liveness.py --fixture …/fixtures/driver/two-lanes
  "kake": { "completes": 0, "in_flight": true,  "unclosed": 1, … }
$ python3 …/mori-shokunin/tools/mori-driver-liveness.py --fixture …/fixtures/driver/two-lanes
  "kake": { "completes": 1, "in_flight": false, "unclosed": 0, … }
```

Attribution: the write is in a wave seat's own session log —
`cp ../mut3/tools/mori-driver-liveness.py /tmp/` in
`Mo56ExecDriverSelftest`'s session transcript, immediately after that seat
created the `mut3` mutant ("M1: break launch/complete event keyword set ->
only 'launch' recognized"). That seat's report states all fixtures "lived
under `/fast/scratch/hyaku/mori-r56/Mo56ExecDriverSelftest/` and were removed
on exit"; the `/tmp` copy was outside its scratch and was not removed
(still present at sweep end, 11:00 mtime). The seat's own report is
internally consistent about its *scratch* cleanup, so this is a leftover
outside the declared scratch, not a contradiction inside it.

### 6.2 Counter temp trees that landed in `/tmp` (transient, gone by sweep end)

At the first pass of the sweep, 13 trees `/tmp/mori-r56-c1-*` and 3 trees
`/tmp/mori-r56-c2-*` existed (creation times 11:00–11:07). Each contains a
materialized copy of a mori r56 tool plus the round-55 ledger/results
(`ledger.md`, `results.json`, `junk.json`, `r55-count-c1.py`) — i.e. exactly
what `count-c1.py` / `count-c2.py` create. By the end of the sweep
(≈11:11) they were gone; **attribution of the removal is UNVERIFIED**
(no `rm` of those paths appears in any session log I could grep, and
`systemd-tmpfiles-clean` has no matching journal entry).

Root cause visible in the frozen counters: both create their workspace with
`tempfile.mkdtemp(prefix="mori-r56-c1-", dir=os.environ.get("TMPDIR") or None)`
and **never remove it** — `grep -nE 'rmtree|cleanup|unlink|shutil'
.ufo/waves/round-56/count-c1.py` and `count-c2.py` return no matches (exit
1) in both files. With `TMPDIR` unset by a caller, the workspace therefore
lands in `/tmp`. This matches the independent observation recorded by a
sibling lane's seat: `tameshi-shokunin/.ufo/waves/round-53/w2/T53W2CritTools.md:78`
("/tmp before-vs-after diff during the same run: only mori-r56-c1-* entries,
which belong to sibling seat MoriR56") — corroboration that mori r56 counter
runs did reach `/tmp`. The frozen counter itself already carries this as a
named limit in `Mo56ExecDriverSelftest.md` (LOW-3, "the counter … does leave
its materialization tree behind").

### 6.3 Other mori-labelled `/tmp` leftovers from earlier rounds (not round 56)

- `/tmp/r55r56-notes.txt` — 3275 bytes, mtime 2026-10-27 05:45:50, sha256
  `def7ebdcececf017bdc395324fbbfaaa5b0e6503cce9e073048b7664ea187af4`.
  Content: round-55 and round-56 dispatch digests of the hyaku inline driver
  (`ROUND 55 len 1741`, `ROUND 56 len 1395`; the round-56 block is chousa
  round 56). Written by a round-57 wave seat
  (`R57W1ReviewReportShape` session log contains the redirect
  `> /tmp/r55r56-notes.txt`). Round 55/56 digests, but not mori round-56
  material.
- `/tmp/r55-hashes.txt` — 4187 bytes, mtime 04:08:31, sha256
  `2ef982ba1af86f29af8e35d99964d62aa4f237eca3203e0d3d71a5ad63aeb05b`;
  `row=N hash=… claim=…` lines of the round-55 registry. Written during
  `MoriR55a2` (round-55 attempt 2). Round 55, not 56.

## 7. Cross-lane check (no mori r56 spillover into other lanes)

For every sibling lane repo under the fleet root, a content scan for
`mori-driver-liveness|mori-vote-bind|mori-r56` returned exactly one hit:

```
tameshi-shokunin/.ufo/waves/round-53/w2/T53W2CritTools.md:78
  …only mori-r56-c1-* entries, which belong to sibling seat MoriR56…
```

That is a round-53 tameshi wave report (untracked in the tameshi lane,
`.ufo/waves/round-53/w2/T53W2CritTools.md`, 9081 bytes, mtime 11:07:36) that
merely *observes* mori r56's `/tmp` residue; it contains no mori r56 artifact
and is not a spillover of mori files into another lane. No mori r56 tool
copy, fixture, entry or evidence file exists in any sibling lane repo.

## 8. Lane-repo local residue (gitignored, inside the lane — informational)

The lane repo's own `.scratch/` (ignored via `.gitignore:5 .scratch/`, so
invisible to porcelain) holds 14 mori-r56-named entries left by the L1's own
pre-freeze runs (10:39–10:45), 1.2 MB total:

```
.scratch/mori-r56-c1-9tu1zbeg  .scratch/mori-r56-c1-jpt84j6e
.scratch/mori-r56-c1-kyk3l8k9  .scratch/mori-r56-c1-xv2gd8jk
.scratch/mori-r56-c2-2fxkb7mc  .scratch/mori-r56-c2-dq7gv23w
.scratch/mori-r56-c2-v3wpjmcq  .scratch/mori-r56-controls-6cjiugss
.scratch/mori-r56-controls-j32fkxhx  .scratch/mori-r56-controls-usopp7mr
.scratch/mori-vote-bind-ne847lty  .scratch/mori-vote-bind-uko56s45
.scratch/mori-vote-bind-v3wtu23q  .scratch/report-draft-r56.md
```

Same class as the `/tmp` residue: counter/control workspaces created under a
`TMPDIR` that pointed into the lane's ignored scratch rather than the
mandated `/fast/scratch/hyaku/mori-r56/<seat>/`. No action taken (read-only
seat; `.scratch/` is outside the paths this seat may write).

## 9. Housekeeping

- Scratch `/fast/scratch/hyaku/mori-r56/Mo56ExecMisroot/` (with `tmp/`
  inside) was created for the one fixture comparison in §6.1 and removed
  before finishing; nothing under it is cited as evidence — the two JSON
  outputs in §6.1 were regenerated in-place from the frozen fixture and the
  committed tool, both with `TMPDIR` pointed at that scratch.
- `scripts/hyaku/disk-guard.sh status` before the sweep: `/fast/scratch/hyaku`
  28 % used, 581.8 G free (`df -h /fast/scratch/hyaku` → 582 G avail). No
  ENOSPC; the sweep is light.
- No tool was installed, upgraded or removed; no pacman transaction.

## Findings

- **MED — a weakened copy of the frozen C1 tool sits outside every sanctioned
  scratch root, at a plausible tool path.** `/tmp/mori-driver-liveness.py`
  (18301 bytes, sha256 `93fe821b…`, mtime 11:00) is the `mut3` mutant with
  the event-keyword set narrowed to `launch` only, copied there by the
  `Mo56ExecDriverSelftest` wave seat (`cp ../mut3/tools/mori-driver-liveness.py /tmp/`).
  It is not the frozen tool (sha `6b3dba74…`) and it produces different
  liveness facts than the committed tool on the frozen `two-lanes` fixture
  (`completes=0, in_flight=true` vs `completes=1, in_flight=false`). Any
  later seat or the post-wave sweep that resolves the tool by name can pick
  it up. File: `/tmp/mori-driver-liveness.py` (line 55 of the copy). Owned by
  the L1's integration step: delete it (or have the owning seat clean up);
  no change to the frozen counter or tool is implied.
- **MED — the frozen counters leave their materialization tree behind, and
  with `TMPDIR` unset it lands in `/tmp`.** `.ufo/waves/round-56/count-c1.py:124`
  and `.ufo/waves/round-56/count-c2.py:77` create
  `tempfile.mkdtemp(prefix="mori-r56-c1-"|"mori-r56-c2-", dir=os.environ.get("TMPDIR") or None)`
  and never remove it (no `rmtree`/`shutil` in either file). 16 such trees
  existed under `/tmp` during the sweep (11:00–11:07) and were gone by ≈11:11
  with the remover UNVERIFIED. Corroborated independently by
  `tameshi-shokunin/.ufo/waves/round-53/w2/T53W2CritTools.md:78`. The
  counters are frozen for this round, so this is a named limit and a routed
  item for round 57 (counter-side temp cleanup or a forced `TMPDIR`), not a
  change proposed here.
- **MED — fleet-root porcelain structurally cannot see mori round 56.** The
  fleet `.gitignore:1` ignores `*-shokunin/`, so every mori r56 artifact
  (contract, counters, controls, fixtures, evidence, source rows, the 40 wave
  seat reports) is invisible to `git -C /home/vgpnk/Projects/shokunin status
  --porcelain`; the lane repo is a separate git repository. The post-wave
  misroot sweep must run `git status --porcelain` in the lane repo too, or
  it will report a clean fleet root while the whole mori r56 wave surface
  sits untracked in the lane. File: `/home/vgpnk/Projects/shokunin/.gitignore:1`.
- **LOW — mori round-56 material in `/tmp` from earlier rounds.**
  `/tmp/r55r56-notes.txt` (3275 bytes, 05:45:50, sha256 `def7ebdce…`) and
  `/tmp/r55-hashes.txt` (4187 bytes, 04:08:31, sha256 `2ef982ba…`) are
  round-55 / round-55-56 digests written by the `MoriR55a2` seat and by a
  round-57 wave seat respectively. Round-55 material, not r56; flagged only
  so the post-wave sweep classifies them once and does not re-report them as
  new. Files: `/tmp/r55r56-notes.txt`, `/tmp/r55-hashes.txt`.
- **LOW — mori r56 residue inside the lane's ignored scratch instead of the
  mandated seat scratch.** 14 entries (1.2 MB) under
  `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/`
  (`mori-r56-c1-*` ×4, `mori-r56-c2-*` ×3, `mori-r56-controls-*` ×3,
  `mori-vote-bind-*` ×3, `report-draft-r56.md`), created 10:39–10:45 by the
  L1's own pre-freeze counter/control runs. Invisible to porcelain
  (`.gitignore:5 .scratch/`). No action taken (read-only seat). Directory:
  `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/`.
- **LOW — mori round-56 report untracked at the fleet root, correctly
  placed.** `/home/vgpnk/Projects/shokunin/.ufo/reports/round-56/mori.md`
  (6744 bytes, 11:02:49) is the L1's own round-56 report; the five sibling
  lanes' round-56 reports are already tracked at the same path, so this is
  the expected pre-integration state, not a misroot. The L1 owns the
  integration commit. File: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-56/mori.md`.
- **LOW — one mori-labelled file in the fleet-root quarantine slice is
  round 55, not round 56.**
  `/home/vgpnk/Projects/shokunin/.tower/quarantine/fleet-root-strays-20261027T0600/mori-r55-closure-entry.json`
  (2487 bytes, 04:32; `"round": 55, "lane": "mori"`), inside the ignored
  `.tower/` tree the contract calls "quarantine slice re-derived". Recorded
  so the post-wave sweep classifies it once.
- **INFO — fleet-root untracked set is exactly three paths and only one is
  mori r56.** `git -C /home/vgpnk/Projects/shokunin status --porcelain`
  (no pathspec) → `.scratch/closure-mado-r50.json` (mado r50, not mori),
  `.ufo/reports/round-53/tameshi.md` (tameshi r53, not mori),
  `.ufo/reports/round-56/mori.md` (mori r56 — yes). Exit 0, stable across two
  passes. No other untracked file exists at the fleet root or under fleet
  `.ufo` outside `.ufo/state/` (operator-reserved, read-only) — 122 ignored
  entries, all runtime state, the watchdog log, other waves' transient
  scratch, or the quarantine slice.
- **INFO — no mori r56 spillover into sibling lanes.** A content scan of all
  20 sibling lane repos for `mori-driver-liveness|mori-vote-bind|mori-r56`
  yields one observation-only hit (a tameshi round-53 seat noting mori r56
  `/tmp` residue) and no copied mori artifact.
- **INFO — the wave had already been dispatched when this seat ran**, so the
  "the wave has not run yet" expectation in the seat brief was stale:
  `.ufo/state/inline-dispatcher.log:60507` records
  `2026-10-27T11:08:27 spawned mori 56 w1 64` (read-only).
