# Mo52ExecScorecardPinsHistory — the nine SCORECARD round-section tally pins, re-executed at their own round commits

Seat: `Mo52ExecScorecardPinsHistory` (executor, leaf). Round 52, wave `w1`. Lane `mori-shokunin`.
Read at lane HEAD `075436b1346ca659afb8be7a46f0e67e4170aa83`; SCORECARD bytes and every tool taken at the data commit
`8524904adb25e44f24d9f25aac7eae909625c18c` unless a row names another revision.
Scratch: `/fast/scratch/hyaku/mori-r52/Mo52ExecScorecardPinsHistory/` (`a39` = `git archive` of round 39, `clone` =
`git clone --shared` of the lane, `tmp/` = `TMPDIR`); removed at end. `scripts/hyaku/disk-guard.sh status` rc 0 before
the runs (`/fast/scratch/hyaku` 24 % used, 614.5 G free). No tool installed or upgraded; no pacman transaction.
Scope: history check only. This is own-work evidence for the L1, not a change to any counter, predicate or kill rule.

## 1. Enumeration (frozen instrument, not a re-typed regex)

`LPIN` and `living_pins()` were imported from the frozen `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-52/count-c1.py`
(read-only, `importlib`) and applied to `git show 8524904:SCORECARD.md` (2734 lines). Result: **exactly 9 matches**, all
inside `## Round N` sections, none in `## Axes` or outside a round section:

| # | SCORECARD line | round | pinned span (LPIN `group(0)`) | landed rev of that round |
|---|---|---|---|---|
| 1 | 2209 | 39 | `` `--selftest` → `CONFORM_SELFTEST pass=9 fail=0` `` | `bb1f2457bb8d3e8d5dfe98488b91e8c02e378ca3` |
| 2 | 2210 | 39 | `` `python3 tools/mori-sources-appendonly.py --selftest` → `pass=12 fail=0` `` | `bb1f2457` |
| 3 | 2238 | 40 | `` `--selftest` → `CONFORM_SELFTEST pass=11 fail=0` `` | `62a207f7521fa2e2fcd2e8b0260f047ccfce8862` (T1 `265a955cc67b…`) |
| 4 | 2239 | 40 | `` `python3 tools/mori-sources-appendonly.py --selftest` → `pass=15 fail=0` `` | `62a207f7` (T1 `265a955c`) |
| 5 | 2300 | 41 | `` `python3 tools/mori-sources-appendonly.py --selftest` → `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0` `` | `9de7323de482699743619cfa2ee444e7418421e3` |
| 6 | 2593 | 47 | `` `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=34 fail=0` `` | `e5dbac05459887d9597ea5d1da0d8e3d024e0d17` (cell: `af2250d8`) |
| 7 | 2620 | 48 | `` `python3 .ufo/waves/round-48/count-c1.py --selftest` → `C1_SELFTEST pass=34 fail=0` `` | `b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86` (cell: `e4dfff32`) |
| 8 | 2621 | 48 | `` `python3 tools/mori-unlanded-check.py --selftest` → `UNLANDED_SELFTEST pass=13 fail=0` `` | `b3e3453d` (cell: `e4dfff32`) |
| 9 | 2651 | 49 | `` `python3 .ufo/waves/round-49/count-c1.py --selftest` → `C1_SELFTEST pass=44 fail=0` `` | `2023465f8b961eed8d5baa46cafde3259f36873f` |

Landing revisions are each round's `round-NN verifier spot-check (integrator, hyaku)` commit, i.e. the tip the next
round names as its entering tip (round 40 closed REJECTED at `62a207f7`; round 47's cell measured `af2250d8` before the
round landed at `e5dbac05`; round 48's cells measured `e4dfff32` before the round landed at `b3e3453d`).

Runs were made at the round's **landed** revision, and additionally at the revision the cell itself names where that
differs. `git archive` was used for plain-byte runs (extracted tree 255 M in `a39`); `git clone --shared` was
used for the tools that call git (clone `git rev-parse --show-toplevel` printed the clone dir; `--is-shallow-repository`
`false`; `.git` 1.9 M). Every run had `cwd` inside the clone or archive and `TMPDIR` set to this seat's scratch.

## 2. Pinned vs observed

| # | exact command (cwd = archive/clone at the stated rev) | rc | observed | verdict |
|---|---|---|---|---|
| 1 | `python3 .ufo/waves/round-39/conform.py --selftest` @ `bb1f2457` | **2** | `conformance setup error: expected str, bytes or os.PathLike object, not NoneType` (no tally) | pinned text not runnable (F1) |
| 1b | `python3 conf39.py bb1f2457bb8d3e8d5dfe98488b91e8c02e378ca3 --selftest --repo <clone> --counter <clone>/.ufo/waves/round-39/count-c7.py --contract <clone>/.ufo/waves/round-39/contract.md` (copy with one line changed, §5) | 0 | `CONFORM_SELFTEST pass=9 fail=0` | **agrees** |
| 1c | same with rev `f920eaf7` (the revision the receipt names) | 0 | `CONFORM_SELFTEST pass=9 fail=0` | **agrees** |
| 2 | `python3 tools/mori-sources-appendonly.py --selftest` @ `bb1f2457` (archive `a39` and clone) | 0 / 0 | `MORI_SOURCES_APPENDONLY_SELFTEST pass=12 fail=0` | **agrees** (pinned text omits the name prefix; tally matches) |
| 3 | `python3 .ufo/waves/round-40/conform.py --selftest` @ `62a207f7` and @ `265a955c` | **2** / **2** | same setup error | pinned text not runnable (F1) |
| 3b | `python3 conf40.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --selftest --repo <clone> --counter <clone>/.ufo/waves/round-40/count-c8.py --contract <clone>/.ufo/waves/round-39/contract.md` | 0 | `CONFORM_SELFTEST pass=11 fail=0` | **agrees** |
| 3c | same with rev `62a207f7521fa2e2fcd2e8b0260f047ccfce8862` (landed) | 0 | `CONFORM_SELFTEST pass=11 fail=0` | **agrees** |
| 4 | `python3 tools/mori-sources-appendonly.py --selftest` @ `265a955c` and @ `62a207f7` | 0 / 0 | `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` (both) | **agrees** |
| 5 | `python3 tools/mori-sources-appendonly.py --selftest` @ `9de7323d` | 0 | `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0` | **agrees** (name and tally exact) |
| 6 | `python3 tools/mori-pin-check.py --selftest` @ `af2250d8` and @ `e5dbac05` | 0 / 0 | `PIN_CHECK_SELFTEST pass=34 fail=0` (both) | **agrees** |
| 7 | `python3 .ufo/waves/round-48/count-c1.py --selftest` @ `e4dfff32` and @ `b3e3453d` | 0 / 0 | `C1_SELFTEST pass=34 fail=0` (both) | **agrees** |
| 8 | `python3 tools/mori-unlanded-check.py --selftest` @ `e4dfff32` and @ `b3e3453d` | 0 / 0 | `UNLANDED_SELFTEST pass=13 fail=0` (both) | **agrees** |
| 9 | `python3 .ufo/waves/round-49/count-c1.py --selftest` @ `2023465f` and @ `24ebc799` | 0 / 0 | `C1_SELFTEST pass=44 fail=0` (both) | **agrees** |

Seven of nine pins reproduce byte-exact (tally and name) at their round's landed revision; the two remaining pins
reproduce their tally once the revision positional that the cell elides is supplied.

### Cause of the rc 2 on pins 1 and 3

`conform.py`'s argument parser takes the revision as an optional positional (`parser.add_argument("rev", nargs="?",
default=None)`), and `--selftest` hands it straight through: `selftest(os.path.abspath(args.repo), args.rev, …)` →
`evaluate(repo, rev, …)` → `run([sys.executable, first, rev, "--repo", repo, "--tool", HANG_FIXTURE, …])` (round-39
`conform.py:369`, round-40 `conform.py:573`). With `rev=None` the subprocess argument list holds `None`, which raises
`TypeError: expected str, bytes or os.PathLike object, not NoneType`; the module-level `except Exception` prints it as
`conformance setup error:` and exits 2. The revision is therefore mandatory even for `--selftest`, and the two cells'
backticked text (a bare `--selftest`) is not the command that produced the tally.

Receipts, for the record: round 39's `.ufo/waves/round-39/evidence/c8-after-selftest.txt` opens `command: r39 conform
--selftest at f920eaf7` — a description, no literal argv, and the revision appears only in prose; round 40's
`.ufo/waves/round-40/evidence/c10-after-selftest.txt` opens `command: python3 .ufo/waves/round-40/conform.py
265a955cc67be4eae97d2dc5a9338a25f31eb29b --selftest` with `EXIT=0` — a literal command that does carry the revision.
So round 40's receipt is complete while its SCORECARD cell is truncated; round 39 has both forms incomplete. This
predates the round-51 rule that every receipt records its literal command line.

## 3. Same pins at today's tip (dated-record boundary)

At `8524904` (the round-52 data commit), in the same clone, cwd = clone root:

| command | rc | observed today | pinned in |
|---|---|---|---|
| `python3 tools/mori-sources-appendonly.py --selftest` | 0 | `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0` | rounds 41 (still equal) |
| `python3 tools/mori-pin-check.py --selftest` | 0 | `PIN_CHECK_SELFTEST pass=125 fail=0` | round 47 pin says 34 |
| `python3 tools/mori-unlanded-check.py --selftest` | 0 | `UNLANDED_SELFTEST pass=17 fail=0` | round 48 pin says 13 |
| `python3 .ufo/waves/round-48/count-c1.py --selftest` | 0 | `C1_SELFTEST pass=34 fail=0` | round 48 (still equal) |
| `python3 .ufo/waves/round-49/count-c1.py --selftest` | 0 | `C1_SELFTEST pass=44 fail=0` | round 49 (still equal) |

Two of the five surfaces moved after their round (pin-check 34 → 125, unlanded-check 13 → 17). This does not
falsify a round-section pin — those are dated records of what was measured then — but it is the concrete reason the
K4 carve-out matters: a reader who runs the SCORECARD line today sees a different tally and the line carries no
"as of round 47" marker of its own (the marker is the enclosing `## Round 47` heading).

One related byte observation: `.ufo/waves/round-40/conform.py` was edited in place after round 40 — blob
`71fa5977…` at `265a955c`/`62a207f7`, blob `63cff4a6…` at `8524904`; the only commits touching that path are
`265a955c` (round-40 instruments) and `87e0c374` ("round-51: … conform.py path fix"). The pin's tally still
reproduces at the round-40 bytes, which is what the cell claims. Whether a later round may edit an earlier round's
instrument is the round-52 in-lane-writer inventory question (routed item 8), not mine; recorded here only because it
means a "run the pin now" reading of that line exercises different bytes.

## 4. Completeness of the enumeration

`LPIN` matched nothing in SCORECARD outside a `## Round N` section at R, and matched nothing with the `(n/m)` form —
all nine are `→ tally` pins. The two bare-`--selftest` spans are the only spans whose command is unbound:
`count-c1.py:228 bound_path()` requires exactly `python3 <repo-relative>.py --selftest` (len(argv)==3, argv[0]
`python3`, argv[2] `--selftest`), so if SCORECARD round sections were ever added to the `LIVING` set these two would
score `unbound_or_not_regular`, not a tally mismatch.

## 5. Lane safety (frozen instruments that hardcode the lane)

`round-39/conform.py` and `round-40/conform.py` hardcode `LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"`, and
their selftest does `os.makedirs(SCRATCH_ROOT)` + `mkdtemp(dir=SCRATCH_ROOT)` with `SCRATCH_ROOT` under that lane.
To avoid creating anything in the lane I ran a copy in scratch with exactly one line changed (quoted in full):

```
-SCRATCH_ROOT = os.path.join(LANE, ".ufo", "waves", "round-39", "scratch")
+SCRATCH_ROOT = "/fast/scratch/hyaku/mori-r52/Mo52ExecScorecardPinsHistory/tmp/conform-scratch"
```

and likewise `round-40/scratch` → `…/tmp/conform40-scratch`; all reads were redirected with
`--repo/--counter/--contract` at the clone. `HANG_FIXTURE` stays an absolute lane *read*
(`.ufo/waves/round-39/fixtures/hang-after-flush.py`); its blob is identical at `f920eaf7`, `bb1f2457`, `265a955c` and
`8524904` (`3a7c96db0356d9568fcc8d326b502b13b73cbe70`; working-tree sha256 `647410536bcc6b9e…` in both the lane and the
clone), so the read is byte-faithful and read-only. No other instrument hardcoded the lane: at the revisions used,
`tools/mori-sources-appendonly.py`, `tools/mori-pin-check.py`, `tools/mori-unlanded-check.py` and both
`.ufo/waves/round-4{8,9}/count-c1.py` resolve paths from their own location or the cwd (round-49's `LANE` is
`dirname(dirname(dirname(HERE)))`).

Post-run checks: `find /home/vgpnk/Projects/shokunin/mori-shokunin -newermt '-40 minutes' -type f -not -path '*/.git/*'`
→ empty; `git -C … status --porcelain` still 29 entries, the only round scratch entry being the pre-existing
`?? .ufo/waves/round-39/scratch/` (mtime `2026-10-26T21:20`, before this seat ran; the bare `--selftest` runs abort
before `makedirs`). No git/jj mutation was issued in the lane or the fleet root; the clone is scratch.
`/home/vgpnk/Projects/shokuknow` was not touched.

## 6. What this does not establish

A tally proves the instrument prints that arm count from the bytes at that revision; it says nothing about whether
the arms discriminate, and none of the seven selftest runs above was mutation-tested here. The two unbound pins are dated
records, so K4's exclusion of round sections is unaffected: at the data commit the K4 scope ("QUALITY.md + README.md
living pins") is unchanged and no claim in this report asks for it to change. A counter weakness found here is a
named limit for round 53, not a fix for round 52.

## Findings

- **F1 (MED)** — `SCORECARD.md:2209` and `SCORECARD.md:2238` pin a bare `` `--selftest` `` as the command behind
  `CONFORM_SELFTEST pass=9 fail=0` and `pass=11 fail=0`. Neither span is a command (`count-c1.py:228 bound_path()`
  returns `None` for it), and the tool each cell names (`.ufo/waves/round-39/conform.py:519,528`; round-40 the same)
  exits **2** with `conformance setup error: expected str, bytes or os.PathLike object, not NoneType` when given only
  `--selftest`, because the revision positional defaults to `None` and reaches `run([... first, rev ...])`
  (round-39 `conform.py:369`, round-40 `conform.py:573`). Both tallies are honest: they reproduce exactly with the
  revision supplied (`pass=9` at `f920eaf7` and `bb1f2457`; `pass=11` at `265a955c` and `62a207f7`). The defect is
  record form — a reader copying the backticked text gets no tally — and it is mirrored in
  `.ufo/waves/round-39/evidence/c8-after-selftest.txt`, whose `command:` line omits the required revision.
- **F2 (LOW)** — the seven other pins (`SCORECARD.md:2210`, `2239`, `2300`, `2593`, `2620`, `2621`, `2651`) reproduce
  byte-exact at their round's landed revision, and the three whose cell names an earlier measurement revision
  (`af2250d8` r47, `e4dfff32` r48 ×2) also reproduce there: no drift between "measured" and "landed" for these cells.
  Nothing to correct; recorded as the positive half of the check.
- **F3 (LOW)** — `SCORECARD.md:2593` (`PIN_CHECK_SELFTEST pass=34`) and `SCORECARD.md:2621`
  (`UNLANDED_SELFTEST pass=13`) no longer reproduce at today's tip: `pass=125` and `pass=17` at `8524904`. Consistent
  with these being dated records, but the pinned line itself carries no as-of marker beyond its `## Round` heading, so
  a reader who runs it as a current claim reads a contradiction. Suggest (round 53, not this claim) the round-section
  pin form name its revision, e.g. `at <rev>`.
- **F4 (LOW)** — `.ufo/waves/round-40/conform.py` was edited after round 40 (`71fa5977…` → `63cff4a6…` in
  `87e0c374`, "round-51: … conform.py path fix"). The round-40 pin remains true against the round-40 bytes, but any
  later re-run of the path exercises different bytes; this is an instance of the round-52 in-lane-writer inventory
  theme (contract §5 item 8) and is routed, not fixed here.
- **F5 (INFO)** — enumeration is complete and machine-derived: the frozen `LPIN` finds exactly nine matches in
  `git show 8524904:SCORECARD.md`, all inside `## Round 39/40/41/47/48/49` sections, none in `## Axes` and none in the
  `(n/m)` form; no SCORECARD tally pin sits outside a round section, so the K4 carve-out covers every one of them at
  the data commit.

Report: `.ufo/waves/round-52/w1/Mo52ExecScorecardPinsHistory.md`
