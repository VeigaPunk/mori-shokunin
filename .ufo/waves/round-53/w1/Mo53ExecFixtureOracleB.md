# Mo53ExecFixtureOracleB — independent oracle for C2's seeded fixtures (round 53, wave w1)

Seat: independent recomputation of the C2 tool's readings on the 64 seed-generated fixtures at the data
commit `2a4213bf8da72f7cd78189baa5bb9be825dca1df`.

**Result: 64 fixtures, exit code and all 15 compared fields agree on 64, disagree on 0.** No defect found in
`tools/mori-commit-runway.py`; three boundary/coverage limits are named under Findings.

Scope note: the seat asks for the 64 seeded fixtures. The 16 frozen fixtures (`frozen_fixtures()`) were not
recomputed by me — the counter's receipt `evidence/c2-at-data.txt` (`agree=80`) covers them, and the frozen
set is not my assignment. Nothing here re-runs `count-c2.py` scoring; the L1's receipt stands as given.

## Method and independence

- Imported **only** `seeded_fixtures` and `write_fixture` from
  `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-53/count-c2.py` (verified: `grep -n 'c2\.ref\|ref_for\|frozen_fixtures' oracle.py` → no match, rc 1). The expected exit and the 15 expected fields
  were computed by my own implementation from the kernel source lines, never from the counter's `ref`:
  - `vm_commit_limit()`: `corpus/evidence/sources-r52/util.c.v7.2:904-916` — `allowed = kbytes >> (PAGE_SHIFT-10)`
    when `sysctl_overcommit_kbytes`, else `(totalram_pages() - hugetlb_total_pages()) * overcommit_ratio / 100`;
    then `allowed += total_swap_pages`. `PAGE_SHIFT-10 == log2(page_kb)`, so `>> (PAGE_SHIFT-10)` is
    `// page_kb`; `show_val_kb` (`corpus/evidence/sources-r53/meminfo.c.v7.3:125`) prints pages as
    `pages * page_kb` kB.
  - `__vm_enough_memory()`: `util.c.v7.2:972-995` — mode 0 refuses only `pages > totalram_pages() + total_swap_pages`
    (so `single_request_cap_kb = (ram_pages + swap_pages) * page_kb`); mode 2 subtracts the admin reserve
    (`982`) and per-process user reserve `min(mm->total_vm/32, user_reserve)` (`990-992`) and compares
    `percpu_counter_read_positive() < allowed` (`994`), i.e. the global part only.
  - `mm_compute_batch()`: `corpus/evidence/sources-r53/mm_init.c.v7.2:191-210` —
    `memsized_batch = min_t(u64, ram_pages/nr/256, INT_MAX)` for `OVERCOMMIT_NEVER`, `batch = max_t(s32, nr*2, 32)`,
    `vm_committed_as_batch = max(memsized_batch, batch)`.
  - counter lag: `percpu_counter.c.v7.2:100`/`:127` fold into `fbc->count` only when the per-CPU delta reaches
    the batch, and `percpu_counter.h.v7.2:118-127` (`percpu_counter_read_positive`) returns `fbc->count` alone;
    each CPU's residue is below one batch, so one batch per present CPU bounds the lag → `band_kb =
    batch * cpus * page_kb`.
  - `hugetlb_total_pages()` is not in the lane corpus; I fetched upstream master
    `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/hugetlb.c?h=master`
    (216702 bytes) and read `mm/hugetlb.c:4662-4670`: `nr_total_pages += h->nr_huge_pages * pages_per_huge_page(h)`
    — **base pages**, so the tool's `Hugetlb_kB // page_kb` (`tools/mori-commit-runway.py:156`) is the right
    conversion of the meminfo `Hugetlb` line. The exact v7.2 bytes of `mm/hugetlb.c` are not held by the lane
    (UNVERIFIED for the tag; the unit agrees with the v7.2 call site).
- Seed: `hashlib.sha256('2a4213bf8da72f7cd78189baa5bb9be825dca1df')` =
  `bd8349d56c3147bc86b2db4be6c8d0f387da0acddd298f7c00e55b73d39dfea4`; `git rev-parse <id>^{commit}` on the lane
  returns that same full id.
- Tool under test: extracted from the data commit, not the working tree —
  `git show 2a4213bf…:tools/mori-commit-runway.py` → 316 lines, sha256
  `80cb169650bf02578439703bc006173aab7b759ff9cf57337611b27164676156`, identical to
  `tools/mori-commit-runway.py` in the lane working tree (same sha256). Run as `python3 -I -B <tool> --meminfo …
  --vm-dir … --cpu-present … --page-kb N` with cwd = the tree root, i.e. the counter's own argv and isolation.
- Every fixture was materialised with `write_fixture` under my scratch and **read back from disk with my own
  parsers** (meminfo `<digits> kB` with duplicate/missing detection, CPU-list count, unsigned integer vm files),
  so the fixture dicts are not trusted as inputs.

## Evidence (commands and outputs, run from /fast/scratch/hyaku/mori-r53/Mo53ExecFixtureOracleB)

Disk guard before the run: `scripts/hyaku/disk-guard.sh status` → rc 0, `/fast` 613 G free.

1. Independent oracle over the 64 seeded fixtures (`python3 oracle.py tree/tools/mori-commit-runway.py result.json`, rc 0):

```
fixtures=64 agree=64 disagree=0
verdict mix: {"COMMIT_HEURISTIC": 13, "COMMIT_LOW": 14, "COMMIT_OK": 15, "COMMIT_UNKNOWN": 9, "COMMIT_UNLIMITED": 13}
```

   Re-run byte-identical (`sha256sum` of `result.json` twice → `de1dfa1233bb214bdbe4025160057ee50d71b739cee33b88cc9b4180b399fefb`),
   so the fixture set and the comparison are deterministic for this seed.

2. Third opinion — my oracle vs the counter's own printed REF (`count-c2.py --fixtures 2a4213bf…`, read-only,
   rc 0, 80 lines; seeded rows compared): `REF-vs-oracle: fixtures=64 mismatches=0`. Three arithmetics
   (my kernel-grounded oracle, the counter's REF, the landed tool) coincide on exit and all 15 fields for every
   seeded fixture. That is the strongest statement this arm can make about the shared-author limit named in the
   contract: a tool that had memorised REF would still have had to match an implementation written here from the
   kernel lines without reading REF's numbers.

3. Hand-arithmetic spot check on the exact band edge (the strongest fixture in the set, `usable_kb == band_kb`):

```
SPOT seeded-53 (page_kb=64)
  meminfo: CommitLimit=62356096 Committed_AS=61406976 Hugetlb=82627328 MemTotal=207339584 SwapTotal=0
  vm: admin_reserve_kbytes=8192 overcommit_kbytes=0 overcommit_memory=2 overcommit_ratio=50 user_reserve_kbytes=131072
  present='0-1' -> nr=2
  ram_pages=207339584//64=3239681; nrn256=6327; floor=32; batch=6327; band=6327*2*64=809856
  headroom=62356096-61406976=949120; reserve=8192+131072=139264; usable=809856; band=809856; LOW iff usable<=band -> COMMIT_LOW
```

   (limit check: `(3239681-1291052)*50//100 = 974314` pages × 64 = 62356096 = the printed CommitLimit.)

4. What the 64 fixtures exercise (so the agreement count can be read for coverage):

| dimension | coverage in the 64 |
|---|---|
| mode | 2 → 29, 0 → 13, 1 → 13, invalid (mode 3 or absent vm) → 9 |
| verdict | COMMIT_OK 15, COMMIT_LOW 14, COMMIT_HEURISTIC 13, COMMIT_UNLIMITED 13, COMMIT_UNKNOWN 9 |
| page size | 4 kB → 45, 16 kB → 8, 64 kB → 11 |
| present CPUs | 1, 2, 4, 8, 12, 16, 32, 48, 64, 96, 128, 256 |
| `overcommit_kbytes` path | 14 (includes floor truncation not page-aligned: seeded-61 `57587678 // 64 = 899807` pages → 57587648 printed) |
| `Hugetlb > 0` (the subtraction) | 16 (`seeded-53` alone carries 82627328 kB) |
| printed limit ≠ recomputed | 6 (all exactly `+page_kb`: 4 kB in seeded-01/41/42/43/45, 16 kB in seeded-55) |
| band path | `memsized` binds in 26 of 29 mode-2 fixtures, the `2*nr` floor in 3 (seeded-17 nr=256, seeded-39 nr=96, seeded-61 nr=256); the 32-page floor and the INT_MAX cap bind in **none** |
| boundary distance (mode 2) | 8 fixtures have `abs(usable_kb - band_kb) <= 4*page_kb`: seeded-11 +4, seeded-19 +8, seeded-28 −12, seeded-44 −4, seeded-48 −8, seeded-50 −48, seeded-53 0 (LOW at equality), seeded-63 +12 |
| inputs not page-aligned | 0 (`MemTotal`, `SwapTotal`, `CommitLimit` are always multiples of `page_kb`) |
| `overcommit_ratio = 0` with `kbytes = 0` (`util.c.v7.2:911-912` swap-only limit) | 0 |

5. The 9 UNKNOWN fixtures and the malformed input behind each (all four classes the generator can emit):

```
seeded-03   vm/overcommit_memory=3
seeded-05   vm/overcommit_memory absent
seeded-10   vm/overcommit_ratio absent
seeded-15   meminfo: missing CommitLimit
seeded-18   meminfo: missing SwapTotal
seeded-23   present='0-1,a' malformed
seeded-25   vm/overcommit_memory=3
seeded-34   vm/overcommit_memory=3
seeded-37   meminfo: missing MemTotal
```

   On these the tool returns `COMMIT_UNKNOWN`/exit 2 with all 13 reading fields null, matching my expectation
   field by field (they are the arm that catches a tool that silently defaults a missing input to a pass).

6. Seven hand-computed boundary probes outside the seeded set (`python3 probe.py <tool>`, rc 0) — each expected
   value written as a literal from the kernel lines, not by my oracle:

```
A-intmax-cap   batch pin at INT_MAX                                              OK
B-floor-32     the 32-page floor with nr=16                                      OK
C-floor-2nr    the 2*nr floor with nr=256                                        OK
D-odd-limit    printed limit not page-aligned                                    OK
E-kbytes-page  kbytes below one page                                             OK
F-huge-gt-ram  unsigned wrap in C, negative in Python (unreachable input)        OK
G-ratio-zero   ratio 0 and kbytes 0 (swap-only limit)                            OK
probes=7 diff=0
```

   These close the coverage gaps the seeded set leaves (the zero rows of item 4's table): INT_MAX batch cap,
   32-page floor, non-page-aligned printed limit, `kbytes < page`, `ratio = 0` with `kbytes = 0`.

7. Adjacent check, not part of the fixture arm: the tool's own `--selftest` at the data commit (with
   `tools/fixtures/mori-commit-runway/cases.json` extracted from that commit) → `MATCHER: rejected 23/23
   corrupted expectations`, `MORI_COMMIT_RUNWAY_SELFTEST: PASS 23/23`, rc 0. Same author as the cases, so this
   is confirmation of internal consistency only.

## Sensitivity measurements (named limits, not defects)

- **Reserve granularity.** The tool subtracts `admin_reserve_kbytes + user_reserve_kbytes` in kB
  (`tools/mori-commit-runway.py:185`), while `util.c.v7.2:982,990-992` applies both reserves in **pages**
  (`>> (PAGE_SHIFT-10)`) and caps the user part at `min(mm->total_vm/32, reserve)`. Recomputed with the
  page-granularity reserves over the 64 fixtures: **0 verdict flips** (`reserve_rounding_flip: 0`). The kB form
  can move the LOW edge by less than `2*page_kb` on a host whose reserve knobs are not page multiples.
- **Band convention at the edge.** The frozen rule uses `batch * CPUs`; the kernel's actual per-CPU residue is
  below one batch, i.e. `(batch-1) * CPUs`. With the tighter bound, **3 of the 29 mode-2 fixtures flip
  COMMIT_LOW → COMMIT_OK**: seeded-44 (`usable-band = -4`), seeded-48 (`-8`), seeded-53 (`0`). The frozen band is
  documented as an upper bound (contract C2), and the tool matches it; the boundary verdict is therefore a
  convention, not a measured refusal point.
- **`Hugetlb > MemTotal`.** Unreachable on a host (hugetlb is carved out of RAM), but the tool computes
  `(ram_pages - huge_pages)` in Python and can emit a negative `limit_recomputed_kb`, where the C is `unsigned
  long` and wraps (probe F, both sides "OK" against my hand literal: `-524288`). Not a live defect.

## Files changed, scratch, tooling

- Wrote only this report: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-53/w1/Mo53ExecFixtureOracleB.md`.
  No other lane path was created or modified: `git ls-files --others --exclude-standard` lists exactly one path
  bearing this seat's name — this report — and the other untracked entries present are pre-existing L1 evidence
  under `.ufo/waves/round-53/evidence/` plus `w1.ready`/`w1.ready.dispatched`.
- Scratch `/fast/scratch/hyaku/mori-r53/Mo53ExecFixtureOracleB/` held the extracted tool, the fixture trees and
  the four scripts; `TMPDIR` was pointed inside it and the directory was removed at the end (`rm -rf`), so no
  `/tmp` path is cited as evidence and the tool's own selftest temp dirs lived there too.
- No pacman call, no tool install or upgrade, no writes to any PATH directory. One network fetch:
  `git.kernel.org` cgit `mm/hugetlb.c?h=master` (216702 bytes) for the `hugetlb_total_pages()` unit; it is not
  cited as a v7.2 source, only as evidence that the function counts base pages.
- Host reads were `/proc`-free for this seat (fixtures only); the lane and fleet repos were read with
  `git show`/`git grep`/`git ls-files` only — no git or jj mutation anywhere.

## Findings

1. **LOW — the fixture arm is blind to `findings` and `notes`.** `compare()` checks only the 15 `FIELDS` plus the
   exit code (`count-c2.py:47`, `:272-283`), so a tool that emitted a wrong `inside_band` / `limit_mismatch` /
   `over_limit_not_enforced` id, or a wrong note, passes all 80 fixtures. The reading fields are what the claim
   fixes, so this is a scope limit of the counter, not a tool defect; the tool's own selftest does check
   `expect_findings` (`tools/mori-commit-runway.py:233-235`), but that file is the same author's.
   Concerned lines: `.ufo/waves/round-53/count-c2.py:47,272-283`; `tools/mori-commit-runway.py:168-196`.
2. **LOW — the seeded generator never reaches the INT_MAX batch cap, the 32-page batch floor, a non-page-aligned
   `CommitLimit`, `overcommit_kbytes < page_kb`, or `overcommit_ratio = 0` with `kbytes = 0`.**
   Measured: 0 of 64 for each (`batch_intmax: 0`, `batch_floor_32: 0`, `limit_nonmultiple: 0`,
   `ratio0_nokbytes: 0`). I probed all five by hand against the tool (7/7 OK), so the tool is fine on them, but
   the arm the counter actually scores cannot see a regression there. Concerned lines:
   `.ufo/waves/round-53/count-c2.py:202-247` (`seeded_fixtures`), `:178-201` (`frozen_fixtures`).
3. **LOW — `COMMIT_LOW` at the boundary is a convention, and 3 of the 29 mode-2 fixtures sit inside the
   convention's own slack.** Using the kernel's per-CPU residue bound `(batch-1)*CPUs` instead of `batch*CPUs`,
   seeded-44 (`usable-band = -4`), seeded-48 (`-8`) and seeded-53 (`0`) read `COMMIT_OK`; the frozen rule calls
   them LOW. This is the documented "upper bound, not a measured deviation" limit of the claim; it matters if a
   later round treats `COMMIT_LOW` as an alarm. Concerned lines: `count-c2.py:141` and
   `tools/mori-commit-runway.py:184-187`; fixtures seeded-44, seeded-48, seeded-53.
4. **LOW — reserve subtraction is done in kB where the kernel applies it in pages** and caps the user reserve at
   `min(mm->total_vm/32, reserve)`. Measured 0 verdict flips across the 64 fixtures, but the reading is a
   worst-case convention, so the LOW edge can differ by up to `2*page_kb` from a specific process's outcome.
   Concerned lines: `tools/mori-commit-runway.py:185-186` vs `corpus/evidence/sources-r52/util.c.v7.2:982-992`.
5. **LOW — `Hugetlb > MemTotal` would print a negative `limit_recomputed_kb` where the kernel's unsigned
   arithmetic wraps.** Unreachable on a real host, and probe F matches the documented arithmetic, so this is an
   input-domain note for round 54, not a live defect. Concerned lines:
   `tools/mori-commit-runway.py:156-161` vs `util.c.v7.2:911-912`.

No HIGH or MED finding: on the seeded arm the tool reproduces an independent kernel-derived reading exactly
(64/64 exit + 15 fields), its `--selftest` passes 23/23, and the seven hand probes hold at the boundaries the
fixtures miss.
