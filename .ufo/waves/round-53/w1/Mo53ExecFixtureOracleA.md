# Mo53ExecFixtureOracleA — independent fixture oracle for C2

Seat: `Mo53ExecFixtureOracleA` (wave `w1`, round 53, lane `mori-shokunin`).
Scope: C2 only — the 16 frozen fixtures of `.ufo/waves/round-53/count-c2.py` against the
read-only tool `tools/mori-commit-runway.py`, recomputed independently from the kernel
sources. Detection and report only; no data file, counter, predicate or tool was changed.

Date: 2026-10-26. Scratch: `/fast/scratch/hyaku/mori-r53/Mo53ExecFixtureOracleA/` (removed at the end).

---

## 1. What this seat did, and how it stayed independent

The seat spec required: import **only** `mk` and `frozen_fixtures` from the frozen counter;
do **not** read or call `ref`; compute every expected value myself from
`corpus/evidence/sources-r53/mm_init.c.v7.2`, `corpus/evidence/sources-r52/util.c.v7.2`
and the tool's own docstring; then run the tool on each fixture and compare.

**Import discipline.** My oracle (`oracle.py`, seat scratch) loads the counter with
`importlib.util.spec_from_file_location("c2frozen", COUNTER)` and binds only
`mk = c2.mk` and `frozen_fixtures = c2.frozen_fixtures`. `ref` and `ref_for` were never
called. The module-level `assert "ref" not in globals()` in the oracle is a standing
check of that discipline. The counter's `main()` was never invoked by my oracle (the
module was imported under the name `c2frozen`, not `__main__`, so the `sys.exit(main(...))`
guard did not fire).

**Kernel ground truth used** (read-only, absolute paths):

- `corpus/evidence/sources-r52/util.c.v7.2:906-916` — `vm_commit_limit()`:
  `allowed = sysctl_overcommit_kbytes >> (PAGE_SHIFT - 10)` when kbytes is nonzero,
  else `((totalram_pages() - hugetlb_total_pages()) * sysctl_overcommit_ratio / 100)`,
  then `allowed += total_swap_pages` (pages throughout).
- `corpus/evidence/sources-r52/util.c.v7.2:961-996` — `__vm_enough_memory()`:
  mode 1 (`OVERCOMMIT_ALWAYS`) returns 0 (test always passes); mode 0 (`OVERCOMMIT_GUESS`)
  refuses only when `pages > totalram_pages() + total_swap_pages`;
  mode 2 (`OVERCOMMIT_NEVER`) computes `allowed = vm_commit_limit()`, subtracts
  `sysctl_admin_reserve_kbytes >> (PAGE_SHIFT - 10)` and
  `min_t(long, mm->total_vm / 32, sysctl_user_reserve_kbytes >> (PAGE_SHIFT - 10))`,
  and the test passes while `percpu_counter_read_positive(&vm_committed_as) < allowed`.
- `corpus/evidence/sources-r53/mm_init.c.v7.2:191-210` — `mm_compute_batch()`:
  `batch = max_t(s32, nr*2, 32)`, `memsized_batch = min_t(u64, ram_pages/nr/256, INT_MAX)`
  for `OVERCOMMIT_NEVER` (else `/4`), `vm_committed_as_batch = max_t(s32, memsized_batch, batch)`,
  with `nr = num_present_cpus()` and `ram_pages = totalram_pages()`.

Kernel sources re-opened from cgit (`git.kernel.org`, `?h=v7.2`) for the pages the lane
does not pin, into seat scratch only: `mm/hugetlb.c` (for `hugetlb_total_pages()`,
`hugetlb_report_meminfo()`), `fs/proc/meminfo.c` (`CommitLimit`/`Committed_AS`/`MemTotal`
lines), `mm/swapfile.c` (`si_swapinfo`), `include/linux/mm.h` (`totalram_pages()`),
`mm/page_alloc.c`. All were fetched with `curl` into the seat scratch; none was written
into the lane.

---

## 2. Result: 16/16 frozen fixtures agree with my independent arithmetic

For each of the 16 frozen fixtures I computed, from the kernel rules above, the expected
`verdict`, exit code, `batch_pages`, `band_kb`, `usable_kb`, `reserve_kb`,
`single_request_cap_kb`, `limit_recomputed_kb` and `limit_consistent`; I then wrote the
fixture files into scratch exactly as the counter's `write_fixture` does
(`<name>/meminfo`, `<name>/vm/<key>`, `<name>/present`), ran the real tool on them, and
compared all 15 counter fields plus the exit code and the field *types*.

```
$ cd /fast/scratch/hyaku/mori-r53/Mo53ExecFixtureOracleA && TMPDIR=$PWD/tmp python3 oracle.py
...
fixtures=16 mismatches=0
```

**Zero disagreements.** Each fixture's arithmetic (my own, printed by the oracle):

| fixture | mode | limit recomputed (= printed) | batch | band_kb | reserve_kb | usable_kb | cap_kb | verdict / exit |
|---|---|---|---|---|---|---|---|---|
| host-mode0-over | 0 | 47583772 = 47583772 | – | – | – | – | 63444672 | COMMIT_HEURISTIC / 0 |
| mode1-over | 1 | 15860896 = 15860896 | – | – | – | – | – | COMMIT_UNLIMITED / 0 |
| mode2-ok | 2 | 47583772 = 47583772 | 968 | 123904 | 139264 | 27444508 | – | COMMIT_OK / 0 |
| mode2-low-negative | 2 | 15860896 = 15860896 | 968 | 123904 | 139264 | −1278368 | – | COMMIT_LOW / 1 |
| mode2-band-edge-low | 2 | 4194304 = 4194304 | 256 | 32768 | 139264 | 32768 | – | COMMIT_LOW / 1 |
| mode2-band-edge-ok | 2 | 4194304 = 4194304 | 256 | 32768 | 139264 | 32772 | – | COMMIT_OK / 0 |
| mode2-kbytes | 2 | 5242880 = 5242880 | 968 | 123904 | 139264 | 4103616 | – | COMMIT_OK / 0 |
| mode2-hugetlb | 2 | 10066328 = 10066328 | 2048 | 65536 | 139264 | 6927064 | – | COMMIT_OK / 0 |
| mode2-one-cpu | 2 | 1048576 = 1048576 | 2048 | 8192 | 139264 | 309312 | – | COMMIT_OK / 0 |
| mode2-sparse-cpus | 2 | 33554432 = 33554432 | 10922 | 262128 | 139264 | 32415168 | – | COMMIT_OK / 0 |
| mode2-page64 | 2 | 33554432 = 33554432 | 128 | 524288 | 139264 | 32415168 | – | COMMIT_OK / 0 |
| mode0-limit-mismatch | 0 | 47583772 ≠ 123456 | – | – | – | – | 63444672 | COMMIT_HEURISTIC / 0 |
| unknown-mode3 | – | – | – | – | – | – | – | COMMIT_UNKNOWN / 2 |
| unknown-missing-commitlimit | – | – | – | – | – | – | – | COMMIT_UNKNOWN / 2 |
| unknown-vm-missing | – | – | – | – | – | – | – | COMMIT_UNKNOWN / 2 |
| unknown-bad-present | – | – | – | – | – | – | – | COMMIT_UNKNOWN / 2 |

Worked example, `mode2-band-edge-low` (the one fixture whose verdict hinges on the `<=`
boundary): `MemTotal 8388608 kB`, page 4 kB → `ram_pages 2097152`; ratio 50 →
`allowed = 2097152*50//100 = 1048576` pages, + swap 0 → `1048576*4 = 4194304 kB`
(printed `CommitLimit` is also 4194304 → `limit_consistent` true). Batch from
`mm_compute_batch`: `nr = 32` (present `0-31`), `ram_pages = 2097152` →
`memsized_batch = min(2097152//32//256, INT_MAX) = min(256, INT_MAX) = 256`;
`batch = max(256, max(2*32, 32)) = 256`; `band_kb = 256*32*4 = 32768`.
`reserve_kb = 8192 + 131072 = 139264`; `headroom_kb = 4194304 − 4022272 = 172032`;
`usable_kb = 172032 − 139264 = 32768`; `32768 <= 32768` → **COMMIT_LOW**, exit 1.
The sibling `mode2-band-edge-ok` (committed 4022268) gives `usable_kb = 32772 > 32768` →
**COMMIT_OK**, exit 0. The tool produced exactly these values.

---

## 3. Additional independent checks (beyond the 16)

### 3.1 The tool's own committed fixture file `tools/fixtures/mori-commit-runway/cases.json`

The counter never checks `cases.json`; it only runs the tool's `--selftest`, which tests
the tool against `cases.json` — a file written by the tool's author, so the selftest is
self-consistent rather than independent. I recomputed **all 23** committed expectations
with my oracle, from the case's own `meminfo`/`vm`/`present`/`page_kb` inputs only.

```
$ cd /fast/scratch/hyaku/mori-r53/Mo53ExecFixtureOracleA && TMPDIR=$PWD/tmp python3 cases_check.py
cases=23 disagreements=0
```

All 23 agree with my kernel-derived reading — including `unknown-cpulist-reversed`
(`present = "5-1"`), where my first oracle pass disagreed with the tool. **My oracle was
wrong there and the tool was right**: `parse_cpulist` rejects a reversed range
(`tools/mori-commit-runway.py:118-120`), which the kernel's `num_present_cpus()` can never
produce, so `COMMIT_UNKNOWN`/exit 2 is correct. I fixed my oracle to reject reversed
ranges and re-ran everything (16/16 and 23/23 still clean). This is reported as a
self-correction, not a tool defect.

### 3.2 Live host

Run against this host's real `/proc/meminfo`, `/proc/sys/vm/*` and
`/sys/devices/system/cpu/present` (mode 0, 32 CPUs, `MemTotal 31721796 kB`,
`SwapTotal 31722876 kB`, `CommitLimit 47583772 kB`, `Hugetlb 0`): my oracle and the tool
agree on every field. A second reading (with the meminfo pinned to one snapshot so that
`Committed_AS` cannot drift between the two reads) gives **no disagreements**; the
un-pinned run differed only in `committed_as_kb`/`headroom_kb`, i.e. ordinary kernel
movement between reads, not a rule difference. The tool's live exit code is 0
(`COMMIT_HEURISTIC`).

### 3.3 The counter itself, read-only, in scratch

```
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-53/count-c2.py \
    2a4213bf8da72f7cd78189baa5bb9be825dca1df --scratch /fast/scratch/hyaku/mori-r53/Mo53ExecFixtureOracleA/c2scratch
C2=met tool=present selftest=pass n=23 fixtures=80 agree=80 disagree=0 registry=ok live=ok rev=2a4213bf8da72f7cd78189baa5bb9be825dca1df
```
(exit 0). This reproduces the L1's `c2-at-data.txt` reading independently.

### 3.4 Frozen bytes verified

`sha256sum` of the files I relied on, checked against
`.ufo/waves/round-53/evidence/freeze-sha256.txt`:

```
5684b69f7ae9030b33195490f10c650c3c123909f0d61e182b6c1cadfbb168c5  .ufo/waves/round-53/count-c2.py   (matches freeze manifest)
ed691b24afbc0dc45090e149d115d707af0c5f7369a10b7722d491075f26a754  corpus/evidence/sources-r53/mm_init.c.v7.2   (matches freeze manifest)
80cb169650bf02578439703bc006173aab7b759ff9cf57337611b27164676156  tools/mori-commit-runway.py
cea8045192babe3017a2682c17a1647e73c597eaf0330a27643858577cc43b63  tools/fixtures/mori-commit-runway/cases.json
```
The working-tree bytes of the two frozen files equal the freeze manifest, so I measured
the bytes the contract froze.

---

## 4. Mutation probe: what the fixture arms cannot see

The contract already names the shared-author limit ("REF and the tool share one author").
I quantified it. I mutated the tool (scratch copies only; the lane's tool was never
modified) and checked whether the fixture arms catch the mutant **against my oracle**
(never against `ref`).

Ten mutants were caught by the 16 frozen fixtures; two of my first-pass mutants were
my own errors (a "mode-blind" mutant whose LOW branch sat inside the mode-2 `else:` and
could never fire in modes 0/1 — corrected in round 2).

| mutant (wrong reading) | caught by the 16 frozen fixtures? | caught by the 23 `cases.json`? |
|---|---|---|
| band without the ×cpus multiplier | yes (8) | – |
| reserve = admin only | yes (9) | – |
| reserve = 0 | yes (9) | – |
| `usable <= band` → `usable < band` | yes (1: band-edge-low) | – |
| mode 0/1 verdicts swapped | yes | yes |
| hugetlb not subtracted from the limit | yes (1: hugetlb) | – |
| kbytes path without the page division | yes (1: kbytes) | – |
| swap pages added twice | yes (4) | – |
| `limit_consistent` always true | yes (1: limit-mismatch) | – |
| band without the ×cpus multiplier / mode-blind LOW | yes / yes | yes / yes |
| **batch floor `max(nr*2, 32)` → `2*cpus`** | **NO — survives all 16** | **NO — survives all 23** |
| **mode-0 cap subtracting hugetlb** | **NO — survives all 16** | **NO — survives all 23** |
| **batch `min_t(..., INT_MAX)` clamp removed** | **NO — survives all 16** | **NO — survives all 23** |

Three wrong readings are invisible to **both** fixture arms:

1. **`batch = max(min(ram//cpus//256, INT_MAX), 2*cpus)`** (the `max(nr*2, 32)` floor
   dropped). `mm_compute_batch` uses `max_t(s32, nr*2, 32)`; with fewer than 16 CPUs the
   32 dominates. I wrote one extra fixture that exposes it: `MemTotal 16384 kB`,
   `present 0` (1 CPU) → `ram//cpus//256 = 16 < 32`, so the correct batch is 32 and the
   mutant's is 16. The unmodified tool agrees with my oracle there (`batch = 32`), so the
   **tool is right** and the frozen fixture set simply never reaches the region.
2. **mode-0 `single_request_cap_kb` subtracting hugetlb.** The kernel's `OVERCOMMIT_GUESS`
   test is `pages > totalram_pages() + total_swap_pages()` — `totalram_pages()`, with **no**
   hugetlb subtraction (only `vm_commit_limit()` subtracts `hugetlb_total_pages()`).
   The tool uses `(ram_pages + swap_pages)`, i.e. the kernel's rule: **the tool is right**.
   A mode-0 fixture with hugetlb > 0 exposes the difference; the frozen set has none.
3. **`min_t(u64, ram_pages/nr/256, INT_MAX)` clamp removed.** The kernel clamps to
   `INT_MAX`; the tool clamps to `INT_MAX` too: **the tool is right**. Reaching the
   difference needs ~8 TiB of RAM per CPU, so it is not practically testable.

Conclusion: in all three cases the **tool matches the kernel and my oracle**; the gap is
in the *fixture evidence*, not in the tool. No frozen fixture, and no case in the tool's
own `cases.json`, exercises `mm_compute_batch`'s 32-page floor or a mode-0 reading with
hugetlb. This is a named limit for the report and a routed item for round 54 — **not** a
change to any frozen counter, predicate or control.

The counter's own fixture arm (16 frozen + 64 seeded) is stronger than either of these:
the seeded set draws `mem` down to 2^18 kB and `ncpu` up to 256, so it does reach the
small-RAM region. I did not re-score the seeded set against my oracle (it is the L1's
arm and the counter is frozen); I note only that the *frozen* subset of the arm has the
three gaps above.

---

## 5. A rounding difference worth recording (not a disagreement)

The kernel's reserves are page-granular: `sysctl_admin_reserve_kbytes >> (PAGE_SHIFT - 10)`
and `sysctl_user_reserve_kbytes >> (PAGE_SHIFT - 10)` (`util.c.v7.2:983,991`), i.e. the
kB values are converted to pages by a shift, which truncates. The tool adds the raw kB
values (`tools/mori-commit-runway.py:185`). With the fixture values (`admin 8192`,
`user 131072`, page 4 kB) both are exact multiples of the page size, so the two agree.
With a non-page-aligned reserve they differ by one page: I built
`admin_reserve_kbytes = 8193` (page 4 kB) and got

```
tool    reserve_kb = 139265  usable_kb = 32767   (COMMIT_LOW)
kernel  admin_reserve pages = 8193 >> 2 = 2048 -> 8192 kB;  user 32768 pages -> 131072 kB
kernel  usable (page-granular) = 172032 - 139264 = 32768 kB
difference = 1 kB
```

So the tool's `usable_kb` is conservative by up to one page per reserve. It is a
defensible reading of "the room a large non-root allocation has" (the docstring says the
reserve is the worst case, `min(total_vm/32, reserve)`), and the contract's own frozen
rule states `usable_kb = CommitLimit − Committed_AS − admin_reserve_kbytes −
user_reserve_kbytes` in kB — so the tool implements the frozen rule as written. Recorded
as LOW.

---

## 6. Scope discipline and environment

- **Writes:** only this report file
  (`.ufo/waves/round-53/w1/Mo53ExecFixtureOracleA.md`) and my own seat scratch
  `/fast/scratch/hyaku/mori-r53/Mo53ExecFixtureOracleA/`. The lane's tool, fixtures,
  `SKILL.md`, `corpus/`, `tools/`, `considerthese/` and every file under
  `.ufo/waves/round-53/` were **not** modified — verified: `git status --porcelain` in
  `mori-shokunin` shows only the pre-existing untracked wave directories
  (`.ufo/waves/round-53/w1/`, `w1.ready*`, `evidence/selftests/`), no modified tracked
  file, and `find` over the lane shows no file I created there.
- **No git mutation:** no `add`/`commit`/`stash`/`checkout`/`reset`/`pull`/`push` in
  `mori-shokunin` or the fleet root; only read-only `git status`, `git show`,
  `git archive` (via the counter) and `git rev-parse`. No `jj` command. No clone was
  needed: the counter's `--scratch` mode archives the revision into my scratch.
- **No host mutation:** only reads of `/proc/meminfo`, `/proc/sys/vm/*`,
  `/sys/devices/system/cpu/present`, `/proc/swaps`. No sysctl written, no OOM triggered,
  no allocation above fixture size, no cgroup/swap/watermark change, no `journalctl`
  vacuum/rotate, no kernel-log grep for kill records (lane rule QUALITY 15).
- **Disk:** `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` before
  the runs → rc 0, `/fast/scratch` 613 G free (24 % used). The heaviest single step was
  the 80-fixture counter run in scratch (6 s). Peak seat scratch use 3.3 MB.
- **Tooling:** no tool was installed or upgraded — the task needed only the stdlib
  (`python3`, `json`, `importlib`, `subprocess`) and `curl` for the cgit fetches. No
  `pacman` transaction was run (pacman is paused host-wide by the 2026-10-20 ruling);
  no `uv`/`npx`/`cargo` install was needed.
- **Credentials:** no credential, session or private URL appears in this report; no
  machine id is printed.
- **Scratch removal:** the seat scratch was removed at the end of the seat (see the
  closing note below).

---

## Findings

| # | severity | finding | file / line |
|---|---|---|---|
| 1 | **NONE** | The 16 frozen fixtures and the tool agree with my independent kernel-derived reading on every field, type and exit code (16/16, 0 disagreements). C2's fixture data is arithmetically correct. | `tools/mori-commit-runway.py`; `.ufo/waves/round-53/count-c2.py:178-199` |
| 2 | **NONE** | The tool's own committed `cases.json` (23 cases) also agrees with my independent reading on all 23 — including the `unknown-cpulist-reversed` case, where the tool is right and my first oracle pass was wrong (self-correction, tool unchanged). | `tools/fixtures/mori-commit-runway/cases.json`; `tools/mori-commit-runway.py:118-120` |
| 3 | **LOW** | The frozen fixture arm cannot see three wrong readings, and two of them survive the tool's own `cases.json` too: (a) `mm_compute_batch`'s `max(nr*2, 32)` floor (needs a fixture with <16 CPUs and tiny RAM); (b) a mode-0 cap that wrongly subtracts hugetlb (needs a mode-0 fixture with hugetlb > 0); (c) the `min_t(..., INT_MAX)` clamp (needs ~8 TiB/CPU, not practically testable). In all three the **tool is correct**; this is a gap in the fixture evidence, not in the tool. Route to round 54: one extra frozen fixture for (a) and one for (b). | `.ufo/waves/round-53/count-c2.py:178-199` (frozen fixture builder); `tools/fixtures/mori-commit-runway/cases.json` |
| 4 | **LOW** | The tool's `reserve_kb` adds the raw kB reserve values, while the kernel shifts them to pages (`>> (PAGE_SHIFT - 10)`), truncating. The tool's `usable_kb` is therefore conservative by up to one page per reserve (measured: 1 kB with `admin_reserve_kbytes=8193`, page 4 kB). The tool implements the contract's frozen kB rule as written, so this is a precision limit of the frozen rule, not a tool defect. | `tools/mori-commit-runway.py:185-186`; `corpus/evidence/sources-r52/util.c.v7.2:983,991` |
| 5 | **LOW** | `mm_compute_batch` uses `totalram_pages()` (no hugetlb subtraction) for the batch, while `vm_commit_limit()` subtracts `hugetlb_total_pages()`. The tool keeps these two distinct (batch from `ram_pages`, limit from `ram_pages − huge_pages`), which matches the kernel; but the distinction is exercised by only one frozen fixture (`mode2-hugetlb`). Worth a named limit: a future edit that unifies the two readings would be caught by that single fixture only. | `tools/mori-commit-runway.py:154-160,182`; `corpus/evidence/sources-r53/mm_init.c.v7.2:196,205`; `corpus/evidence/sources-r52/util.c.v7.2:911-912` |
| 6 | **LOW** | `limit_recomputed_kb` is derived from `/proc/meminfo`'s `MemTotal`/`Hugetlb`/`SwapTotal`, while the kernel's `vm_commit_limit()` uses `totalram_pages()`, `hugetlb_total_pages()` and `total_swap_pages()`. On this host the reconstruction is exact (`47583772 kB` recomputed = `47583772 kB` printed) and `totalram_pages()` is the memblock-derived page count that `/proc/meminfo`'s `MemTotal` mirrors, so the reading is sound; but the equality is a host-specific observation, not a proof for every host (e.g. a kernel built with `CONFIG_HUGETLB` reporting a `Hugetlb` line the tool's optional-field handling defaults to 0). | `tools/mori-commit-runway.py:154-166`; `corpus/evidence/sources-r52/util.c.v7.2:906-916`; `corpus/evidence/sources-r53/mm_init.c.v7.2:196` |
| 7 | **INFO** | The counter's own reading reproduces independently: `C2=met tool=present selftest=pass n=23 fixtures=80 agree=80 disagree=0 registry=ok live=ok`, exit 0, at `2a4213bf8da72f7cd78189baa5bb9be825dca1df`. The 80-fixture arm is stronger than the 16 frozen fixtures alone (finding 3) because its seeded half reaches small RAM / many CPUs. | `.ufo/waves/round-53/count-c2.py` |
| 8 | **INFO** | Scope discipline held: no lane file, tool, fixture, `SKILL.md` or `corpus/` byte was modified; the only lane write is this report; all scratch was under the seat directory and removed afterwards. No git/jj mutation, no host mutation, no tooling installed, no pacman transaction. | this file; `/fast/scratch/hyaku/mori-r53/Mo53ExecFixtureOracleA/` |

**Unverified / not checked by this seat:** the seeded half of the counter's fixture arm
against my oracle (it is the L1's arm; the counter is frozen and I did not re-score it);
the C2 registry row's exact wording against the frozen predicate (I only checked that the
counter reports `registry=ok`); and the `--selftest` matcher-rejection strength beyond
the tool's own `23/23` claim.

**No defect was found in the tool, the fixtures, or the counter's data.** The three
gaps in finding 3 are gaps in the *evidence*, all of them leaving the tool correct; per
the round-53 rules the frozen counters, predicates, controls and kill rules were not
proposed for change, and the fixture-evidence gaps are routed to round 54 instead.
