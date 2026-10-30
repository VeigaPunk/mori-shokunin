# Mo61ScribeReg5455 — SKILL.md gate-registry rows for the round-54 and round-55 gates

Seat: scribe (leaf; no subagent dispatch). Lane: mori-shokunin.
Date: 2026-10-30. Round-61 freeze `7370a731abcafc4c803111de7c22cd6264d63be1`; entering `325f7e639916fcbc77fa2ec7475951a1b86bb1cb`.
Scope: the 4 manifest paths of rounds 54–55 in `.ufo/waves/round-61/gate-manifest.json`:

| path | round | landing commit |
|---|---|---|
| `.ufo/waves/round-54/count-c1.py` | 54 | `6830f3af992d906bfa1e17e3743e631ab834f67c` |
| `.ufo/waves/round-54/count-c2.py` | 54 | `6830f3af992d906bfa1e17e3743e631ab834f67c` |
| `.ufo/waves/round-55/count-c1.py` | 55 | `c9b908f0bb89974f30b927776ce2450ae4198b10` |
| `.ufo/waves/round-55/count-c2.py` | 55 | `c9b908f0bb89974f30b927776ce2450ae4198b10` |

Read-only. No production file, registry, VCS state, or fleet/sibling file was touched. Scratch
(`$HYAKU_SCRATCH/mori-r61/Mo61ScribeReg5455`, i.e. `/fast/scratch/hyaku/mori-r61/Mo61ScribeReg5455`)
held one `git clone --shared` of the lane and the freeze extracts; it was removed after the receipts
below were copied in.

## Tooling

No tool was installed or updated for this seat (plain `python3`, `git`, `sha256sum`, `grep` only). Per
`/home/vgpnk/.omp/agent/RULES.md`, pacman transactions are paused host-wide; none was attempted.

Disk guard before the work: `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → `rc=0`,
`/tmp 24% free 97.5G`, `/var/tmp 41% free 533.9G`, `/fast/scratch/hyaku 49% free 416.7G` (green, no ENOSPC).

## Draft registry rows (for L1 integration into SKILL.md)

One row per line, eight cells each, inside one fenced block. The entry cell names the artifact path
verbatim; the self-test cell names the runnable `--selftest` command and the measured output line; the
owner cell names the landing round's L1.

```markdown
| r54 v7.3 recheck-ledger counter (C1) | gate (freshness claim-table verdict; not a census or fleet-admission gate) | `python3 .ufo/waves/round-54/count-c1.py <rev> [--repo DIR]`; also `--scope` (prints the frozen 31-row scope; exit 2 when empty) and `--selftest` | 0 → `C1=met scope=N rows=N matched=N status_ok=N line_ok=N quote_ok=N source_rows=ok/bad pins=ok/bad provenance=ok/bad held=N absent=N holds=N changed=N voted=N dissent=N rev=R` · 1 → `C1=unmet … failed=<arms>` (ledger_absent, pins, status, line, quote, source_rows, provenance, votes) · 2 → `C1_SETUP` (usage, unresolvable revision, empty scope at entering tip `39dcf4d7e410d362781a47e8365ca23b5c807598`) | `python3 .ufo/waves/round-54/count-c1.py --selftest` → `C1_SELFTEST pass=57 fail=0` (57 cases, exit 0; measured at landing commit `6830f3af992d906bfa1e17e3743e631ab834f67c`; must be run from a lane checkout — the selftest reads the working-tree copies under `corpus/evidence/sources-r54/`, so a lone materialized file raises FileNotFoundError) | counter sha256 `e97a11986694b60f3a5d9d50b151553072f08a8a8d46cbea8f4b63a90dff433c` (identical at landing, round-61 freeze and tip); ledger `corpus/knowledge/kernel-v7.3-recheck-r54.md`; the eight in-script `V73` copy pins (memcontrol.c, oom_kill.c, percpu_counter.c, percpu_counter.h, errno.h, util.c, mm_init.c, cgroup-v2.7.3.html); voters `Mo54Rc01`–`Mo54Rc12`; `MIN_VOTES=2` | none (read-only: `git show` / `git ls-tree` / `git rev-parse`; TMPDIR is honoured, no `--scratch` flag) | MoriR54 |
| r54 memory-failure-kills counter (C2) | gate (depth claim-quote verdict; not a census or fleet-admission gate) | `python3 .ufo/waves/round-54/count-c2.py <rev> [--repo DIR] [--entry PATH]`; also `--hashes <rev>` (prints each row's 12-hex claim handle) and `--selftest` | 0 → `C2=met claims=N located=N quote_missing=N bad_rows=N sources=N source_rows=ok/bad pins=ok/bad provenance=ok/bad entailed=N dissent=N rev=R` · 1 → `C2=unmet … failed=<arms>` (entry_absent, table, claims floor, bad_rows, quote_missing, sources_floor, pins, provenance, entailment) · 2 → `C2_SETUP` (usage, unresolvable revision) | `python3 .ufo/waves/round-54/count-c2.py --selftest` → `C2_SELFTEST pass=54 fail=0` (54 cases, exit 0; measured at landing commit `6830f3af992d906bfa1e17e3743e631ab834f67c`; must be run from a lane checkout — the selftest reads the working-tree copies under `corpus/evidence/sources-r54/`) | counter sha256 `d6b42f893b304ca355c03a4e43ad431b268b39ecfe8163c6871bbc0d6550785e` (identical at landing, round-61 freeze and tip); entry `corpus/knowledge/memory-failure-kills-r54.md`; the six in-script `COPIES` pins (memory-failure.c, hwpoison.rst, sysfs-devices-node, memory-failure-trace.h, vm.rst, proc.rst); voters `Mo54En01`–`Mo54En12`; `MIN_CLAIMS=14`, `MIN_SOURCES=4` | none (read-only: `git show` / `git ls-tree` / `git rev-parse`; TMPDIR is honoured, no `--scratch` flag) | MoriR54 |
| r55 v7.2-pointer recheck-ledger counter (C1) | gate (freshness line-pointer verdict; not a census or fleet-admission gate) | `python3 .ufo/waves/round-55/count-c1.py <rev> [--repo DIR]`; also `--scope` (prints the frozen 78-pointer scope) and `--selftest` | 0 → `C1=met scope=N rows=N matched=N status_ok=N line_ok=N source_rows=ok/bad pins=ok/bad provenance=ok/bad same=N moved=N changed=N broken=N holds=N stale=N voted=N dissent=N rev=R` · 1 → `C1=unmet … failed=<arms>` (ledger_absent, pins, status, line, source_rows, provenance, votes) · 2 → `C1_SETUP` (usage, unresolvable revision, entering tip unreadable at `ca52426ea496bc6592e3e867cc9d28843e45f196`) · defect as frozen: this counter's vote arm binds stripped-line equality against the orchestrator-captured output, so round 55's structured-JSON voter yields did not count — the row registers the artifact as it stands, `failed=votes` at every revision measured | `python3 .ufo/waves/round-55/count-c1.py --selftest` → `C1_SELFTEST pass=44 fail=0` (44 cases, exit 0; measured at landing commit `c9b908f0bb89974f30b927776ce2450ae4198b10`; must be run from a lane checkout — the selftest loads the sibling `checks/selftest-c1.py` and `controls/c1data.py` and reads the working-tree copies under `corpus/evidence/sources-r55/`) | counter sha256 `e30658be34bfbf866860b20c9bde4117d467e351bb79e523131424cd5061e20b` (identical at landing, round-61 freeze and tip); ledger `corpus/knowledge/kernel-v7.3-recheck-r55.md`; the ten in-script `COPIES` v7.2/v7.3 sha256 pairs; voters `Mo55Rc01`–`Mo55Rc16`; `MIN_VOTES=2` | none (read-only: `git show` / `git ls-tree` / `git rev-parse`; TMPDIR is honoured, no `--scratch` flag) | MoriR55 |
| r55 disk-runway-ENOSPC counter (C2) | gate (depth claim-quote verdict; not a census or fleet-admission gate) | `python3 .ufo/waves/round-55/count-c2.py <rev> [--repo DIR] [--entry PATH]`; also `--hashes <rev>` (prints each row's 12-hex claim handle) and `--selftest` | 0 → `C2=met claims=N located=N quote_missing=N bad_rows=N sources=N source_rows=ok/bad pins=ok/bad provenance=ok/bad entailed=N dissent=N rev=R` · 1 → `C2=unmet … failed=<arms>` (entry_absent, table, claims floor, bad_rows, quote_missing, sources_floor, pins, provenance, entailment) · 2 → `C2_SETUP` (usage, unresolvable revision) · defect as frozen: round 55 closed this gate unmet on the vote arm (`entailed=15 dissent=8 failed=entailment`) because eight rows drew reviewer dissent that the frozen arm cannot settle — the row registers the artifact as it stands | `python3 .ufo/waves/round-55/count-c2.py --selftest` → `C2_SELFTEST pass=10 fail=0` (10 cases, exit 0; measured at landing commit `c9b908f0bb89974f30b927776ce2450ae4198b10`; must be run from a lane checkout — the selftest loads the sibling `checks/selftest-c2.py` and `controls/c2data.py` and reads the working-tree copies under `corpus/evidence/sources-r55/`) | counter sha256 `ccb2333a7e3d6744f00041b5bb95a95cb5191b6b5d5a8a963949db4891e12754` (identical at landing, round-61 freeze and tip); entry `corpus/knowledge/disk-runway-enospc-r55.md`; the nine in-script `COPIES` pins (errno-base.h, statfs.c, xfs_super.c, btrfs_super.c, btrfs_sysfs.c, tmpfs.rst, statfs.2.man-pages-6.19, statvfs.3.man-pages-6.19, coreutils.texi.v9.12); voters `Mo55En01`–`Mo55En12`; `MIN_CLAIMS=16`, `MIN_SOURCES=6` | none (read-only: `git show` / `git ls-tree` / `git rev-parse`; TMPDIR is honoured, no `--scratch` flag) | MoriR55 |
```

Notes on the drafts:

- **No literal or escaped `|` inside any cell.** The frozen C1 counter splits a registry row with a plain
  `str.split("|")` (`count-c1.py:63` — `lines[i].strip().strip("|").split("|")`), with no escape handling:
  an escaped `\|` inside a cell adds a field, the row then has ≠ 8 cells and is dropped silently.
  Measured (`pipe_test.py` against the frozen parser): a row with no pipe → `rows_parsed=1`; the same row
  with `\|` in the verdict cell → `rows_parsed=0`. Every verdict-map cell therefore spells `ok/bad` where the
  counter prints `ok|bad`, and the row cells use `·` as the separator.
- **Owner cells** name the landing round's L1: `MoriR54` (LOG.md:2890 `## Round 54 (L1 MoriR54, attempt 1; …)`)
  and `MoriR55` (LOG.md:2938 `## Round 55 (L1 MoriR55 attempt 1 died pre-WAVE-DONE; attempt 2 MoriR55a2 closed it; …)`).
  L1 decision needed: round 55 was closed by `MoriR55a2`; I wrote the round L1 (`MoriR55`) because the seat
  spec asks for the landing round's L1, and the artifacts were frozen under attempt 1 (`c9b908f0`). If the L1
  prefers the closing L1, the two r55 owner cells become `MoriR55a2` — a one-word change, no other cell moves.
- **The r55 rows name their frozen defects in the verdict-map cell** (the artifact is registered as it is).
  Round 55 closed both r55 claims **unmet**; see findings 3 and 4.

## Evidence

### 1. Bytes: landing == round-61 freeze == tip (no drift)

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ git show <rev>:<path> | sha256sum
.ufo/waves/round-54/count-c1.py  landing=e97a11986694b60f freeze=e97a11986694b60f tip=e97a11986694b60f
.ufo/waves/round-54/count-c2.py  landing=d6b42f893b304ca3 freeze=d6b42f893b304ca3 tip=d6b42f893b304ca3
.ufo/waves/round-55/count-c1.py  landing=e30658be34bfbf86 freeze=e30658be34bfbf86 tip=e30658be34bfbf86
.ufo/waves/round-55/count-c2.py  landing=ccb2333a7e3d6744 freeze=ccb2333a7e3d6744 tip=ccb2333a7e3d6744
```

Full digests: `e97a11986694b60f3a5d9d50b151553072f08a8a8d46cbea8f4b63a90dff433c` (r54 c1),
`d6b42f893b304ca355c03a4e43ad431b268b39ecfe8163c6871bbc0d6550785e` (r54 c2),
`e30658be34bfbf866860b20c9bde4117d467e351bb79e523131424cd5061e20b` (r55 c1),
`ccb2333a7e3d6744f00041b5bb95a95cb5191b6b5d5a8a963949db4891e12754` (r55 c2).

Each equals the wave's own frozen receipt: `.ufo/waves/round-54/evidence/freeze-sha256.txt` (lines for
`count-c1.py` / `count-c2.py`) and `.ufo/waves/round-55/evidence/freeze-sha256.txt` (same), both read at the
landing commits. The r55 counters' sibling selftest modules are pinned there too:
`checks/selftest-c1.py` `48c4c38c24dbc9c726fe5bb08645f3443293a7a461cef4e587fcbd1167a029fa`,
`checks/selftest-c2.py` `2ab590d2ea1ac4dd2a364644e1108de3a6a13923e1f11fa86aaae015f44499ff`.

### 2. Selftests, run once each at the landing commit (measured)

Method: `git clone --shared` of the lane into scratch, `git checkout <landing>`, `TMPDIR` inside scratch,
one `--selftest` per artifact.

```
$ python3 .ufo/waves/round-54/count-c1.py --selftest   # at 6830f3af
C1_SELFTEST pass=57 fail=0                              rc=0
$ python3 .ufo/waves/round-54/count-c2.py --selftest   # at 6830f3af
C2_SELFTEST pass=54 fail=0                              rc=0
$ python3 .ufo/waves/round-55/count-c1.py --selftest   # at c9b908f0
C1_SELFTEST pass=44 fail=0                              rc=0
$ python3 .ufo/waves/round-55/count-c2.py --selftest   # at c9b908f0
C2_SELFTEST pass=10 fail=0                              rc=0
```

The same four lines reproduce at the round-61 freeze `7370a731` (4 runs, all rc=0). The counts agree with
the committed receipts `.ufo/waves/round-54/evidence/selftest-c1.txt` (`C1_SELFTEST pass=57 fail=0`, `exit=0`),
`…/round-54/evidence/selftest-c2.txt` (`C2_SELFTEST pass=54 fail=0`, `exit=0`),
`…/round-55/evidence/selftest-c1.txt` (`C1_SELFTEST pass=44 fail=0`, `exit=0`),
`…/round-55/evidence/selftest-c2.txt` (`C2_SELFTEST pass=10 fail=0`, `exit=0`).

Case names for r54 c1 (tail): `ok scope_path_without_copy_unmet`, `ok scope_reader`.
For r54 c2 (tail): `PASS voters_frozen`, `PASS words_beyond_counts`, `PASS text_copy_keeps_angle_brackets`.

### 3. What the gates read when measured (the rows' verdict maps)

r54 at its integration commit `f111d4b0` — both **met** (matches LOG.md:2897-2904):

```
$ python3 .ufo/waves/round-54/count-c1.py f111d4b0 --repo <clone>
C1=met scope=31 rows=31 matched=31 status_ok=31 line_ok=31 quote_ok=31 source_rows=ok pins=ok provenance=ok held=31 absent=0 holds=31 changed=0 voted=31 dissent=0 rev=f111d4b0120a04ed1a0a2270a72ec0a343d20e29   rc=0
$ python3 .ufo/waves/round-54/count-c2.py f111d4b0 --repo <clone>
C2=met claims=21 located=21 quote_missing=0 bad_rows=0 sources=6 source_rows=ok pins=ok provenance=ok entailed=21 dissent=0 rev=f111d4b0120a04ed1a0a2270a72ec0a343d20e29   rc=0
```

r55 at its integration commit `a27ec482` — both **unmet** on the vote arm (LOG.md:2942-2944), and the same
two lines reproduce at the round-61 freeze `7370a731`:

```
$ python3 .ufo/waves/round-55/count-c1.py a27ec482 --repo <clone>
C1=unmet scope=78 rows=78 matched=78 status_ok=78 line_ok=78 source_rows=ok pins=ok provenance=ok same=69 moved=7 changed=2 broken=0 holds=78 stale=0 voted=0 dissent=0 rev=a27ec48210b136d9f2fd1b71c5e64f65f5a30e22 failed=votes   rc=1
$ python3 .ufo/waves/round-55/count-c2.py a27ec482 --repo <clone>
C2=unmet claims=23 located=23 quote_missing=0 bad_rows=0 sources=9 source_rows=ok pins=ok provenance=ok entailed=15 dissent=8 rev=a27ec48210b136d9f2fd1b71c5e64f65f5a30e22 failed=entailment   rc=1
```

(At the freeze the same two lines read `rev=7370a731abcafc4c803111de7c22cd6264d63be1`, rc=1 in both cases.)

### 4. The rows parse and register under the frozen C1 counter

The frozen parser was exercised directly (`count-c1.py:63-70` `parse_tables`, `:72-81` `row_hits`) on the
draft block: `parsed rows: 4`, each row 8 cells, no empty cell, `--selftest` present in every self-test
cell, and exactly one live row per path:

```
path=.ufo/waves/round-54/count-c1.py hits=1 live=1 empty=[] selftest_flag=True
path=.ufo/waves/round-54/count-c2.py hits=1 live=1 empty=[] selftest_flag=True
path=.ufo/waves/round-55/count-c1.py hits=1 live=1 empty=[] selftest_flag=True
path=.ufo/waves/round-55/count-c2.py hits=1 live=1 empty=[] selftest_flag=True
```

No cross-matching: no draft row names another manifest path.

End-to-end dry run in the scratch clone (SKILL.md + the four rows appended **in the clone only**, throwaway
identity `t <t@t>`, commit `084b8b7aa8f6e2148355b303b9a9586820f04cad`):

```
$ python3 .ufo/waves/round-61/count-c1.py 084b8b7a --repo <clone> --scratch <scratch>
C1=unmet gates=25 registered=4 missing=21 thin=0 dup=0 unres=0 noselftest=0 noowner=0 failed=missing:.ufo/waves/round-52/count-c1.py,…
```

`registered=4` — exactly my four paths register; `missing=21` are the paths owned by the other four scribe
seats (round-52/53, 56/57, 58/59, 60). The before-state at the freeze, unchanged by this seat:
`C1=unmet gates=25 registered=0 missing=25 …` (rc=1), matching the contract's control.

The clone and every scratch artifact were deleted after the receipts above were copied in.

### 5. Docstring / argparse surface read (path:line pointers)

| artifact | pointers |
|---|---|
| `.ufo/waves/round-54/count-c1.py` | docstring 3-33 (predicate P-C1, `Usage: count-c1.py <rev> [--repo DIR] \| --selftest \| --scope`, output line 32-33); `LEDGER` 53; `SRC_DIR` 56; `VOTERS` 60; `main` 401; `selftest` 435; tally print 724; `lane_root` 397 |
| `.ufo/waves/round-54/count-c2.py` | docstring 3-36 (P-C2, `Usage: count-c2.py <rev> [--repo DIR] [--entry PATH] \| --selftest \| --hashes <rev>`, output line 26-27); `ENTRY` 45; `VOTERS` 50; `MIN_CLAIMS` 53; `MIN_SOURCES` 54; `main` 305; `selftest` 339; tally print 565 |
| `.ufo/waves/round-55/count-c1.py` | docstring 3-36 (P-C1, `Usage: count-c1.py <rev> [--repo DIR] \| --selftest \| --scope`, output line 32-34); `ENTER` 49; `ENTRIES` 50-51; `LEDGER` 52; `SRC` 53; `VOTERS` 56; `main` 444; `--selftest` delegates to `checks/selftest-c1.py` (444-450); output assembly 414-418 |
| `.ufo/waves/round-55/count-c2.py` | docstring 3-38 (P-C2, `Usage: count-c2.py <rev> [--repo DIR] [--entry PATH] \| --selftest \| --hashes <rev>`, output line 26-27); `ENTRY` 46; `VOTERS` 50; `MIN_CLAIMS` 53; `MIN_SOURCES` 54; `main` 313; `selftest` 347 (delegates to `checks/selftest-c2.py`); output assembly 288-291 |

(LOG.md: the round-54 counters are named at LOG.md:2890-2905; the round-55 counters at LOG.md:2938-2944.)

## Findings

1. **The frozen C1 parser drops any registry row containing a pipe inside a cell.** `count-c1.py:63` splits a
   row with `str.split("|")` and takes no escape into account; the row then has ≠ 8 fields and is skipped
   without a counter. Measured: the identical row parses as 1 row without a pipe and as 0 rows with `\|` in the
   verdict-map cell. Any row the L1 appends (mine or another seat's) must avoid `|` in every cell. This is a
   counter defect, not a fix to apply here — reported, not repaired (round-61 amendments are barred).
2. **The r54 counters are green; the r55 counters are red on their vote arm and stay red.**
   r54 c1/c2 read `met` at `f111d4b0` and at the round-61 freeze (rc=0). r55 c1/c2 read `unmet`
   (`failed=votes`, `failed=entailment`; `voted=0`, `entailed=15 dissent=8`) at `a27ec482` and at the freeze
   (rc=1). Round 55's own LOG explains the causes (LOG.md:2946): the frozen r55 C1 vote arm binds
   stripped-line equality against the orchestrator-captured output, so the seats' structured-JSON yields did
   not count (`voted=0`), and eight C2 rows carry reviewer dissent the frozen arm cannot settle. Round 56's
   `tools/mori-vote-bind.py` was built for exactly this shape (LOG.md:2952). The r55 rows therefore register
   the artifact **as it is**, with the defect named in the verdict-map cell — a registry row must not claim a
   gate green that the frozen counter does not print.
3. **Both r55 counters' selftests need committed siblings, and all four selftests need a lane checkout.**
   A lone materialized file fails: r55 c1 → `FileNotFoundError: …/checks/selftest-c1.py`; r54 c1 →
   `FileNotFoundError: /…/corpus/evidence/sources-r54/memcontrol.c.v7.3` (the selftest reads the working-tree
   copies under `lane_root()`, not the git object store). The self-test cells say so, so the L1's dry run does
   not misread a path-dependent failure as a red selftest.
4. **The r55 counters' vote-arm defect is not a data defect.** Both r55 gates show every data arm green
   (`rows=78 matched=78 status_ok=78 line_ok=78 source_rows=ok pins=ok provenance=ok`;
   `claims=23 located=23 quote_missing=0 bad_rows=0 sources=9 source_rows=ok pins=ok provenance=ok`) and fail
   only on the vote arms. Their selftests pass 44/44 and 10/10 — the vote-binding shape is covered by the
   round-56 tool, not by these frozen counters.
5. **Owner-cell wording is the one open decision** (see Notes): `MoriR55` vs `MoriR55a2` for the two r55 rows.

## Out of scope

No edits to `SKILL.md`, `corpus/`, `LOG.md`, `SCORECARD.md`, `tools/`, the registry, or the round-61 counters;
no commit, push, tag, or any other VCS mutation in the lane or the fleet; nothing written to a sibling repo;
no service, config, or host-state change; no provider-death inference; no tool install. The scratch clone and
all scratch files were removed after the receipts above were copied in (scratch root
`/fast/scratch/hyaku/mori-r61/Mo61ScribeReg5455` no longer exists).
