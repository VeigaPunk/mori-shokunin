# Mo53RevC2Tool — review of `tools/mori-commit-runway.py` (C2) at 2a4213bf

Seat: attack/review of the C2 tool against its docstring, the frozen interface in
`.ufo/waves/round-53/contract.md` `## C2`, and the kernel. Leaf seat; no subagents; no fleet/lane writes.

Bytes reviewed: `git show 2a4213bf8da72f7cd78189baa5bb9be825dca1df:tools/mori-commit-runway.py` (316 lines),
byte-identical to the worktree when the review began (`git diff --stat 2a4213bf -- tools/mori-commit-runway.py`
empty, rc 0). **Every line number below is that blob's.** The worktree changed under me mid-review; see
"Status of the uncommitted worktree" at the end — I did not score those bytes.

Kernel bytes used (all read from the lane's committed copies unless noted):
`corpus/evidence/sources-r52/util.c.v7.2` (904–916 `vm_commit_limit`, 937–941 `vm_memory_committed`, 959–1003
`__vm_enough_memory`, 853–861 the `overcommit_memory` sysctl entry), `corpus/evidence/sources-r53/mm_init.c.v7.2:191-210`
(`mm_compute_batch`), `percpu_counter.c.v7.2:93-137`, `percpu_counter.h.v7.2:118-126`, `mman.h.v7.2:65-83`
(`vm_acct_memory` → `vm_committed_as_batch`), `meminfo.c.v7.3:28-31,60,89,125-126` (`show_val_kb` =
`num << (PAGE_SHIFT-10)`).

Scratch: `/fast/scratch/hyaku/mori-r53/Mo53RevC2Tool/` with `TMPDIR` set there; removed at the end. No installs
(no pacman, no uv/npx). Nothing written to the lane; the hand fixtures, the fuzz harness and the tool copies live
only in scratch.

---

## Verified consistent (no finding)

1. **Limit recompute, lines 156–161 vs `util.c.v7.2:904-916`.** The kernel's `sysctl_overcommit_kbytes >>
   (PAGE_SHIFT - 10)` is a division by `PAGE_SIZE/1024`, i.e. by `page_kb` for every power-of-two page size the
   CLI accepts, so `// page_kb` (158) is the same integer for 4, 16, 64 and 1024 kB pages; the hugetlb
   subtraction is inside the ratio branch and before the `* ratio / 100` (160), swap is added after both
   branches (161), kbytes takes precedence over the ratio (157), exactly as the kernel orders it.
   * `python3 -I -B … --meminfo /proc/meminfo …` → `"commit_limit_kb": 47583772, "limit_recomputed_kb":
     47583772, "limit_consistent": true, "verdict": "COMMIT_HEURISTIC"`, rc 0.
   * Hand case A (page 4, MemTotal 16777216, Hugetlb 4194304, ratio 80, 8 CPUs): `(4194304-1048576)*80//100 =
     2516582` pages → `limit 10066328`; observed `limit_recomputed_kb 10066328`, `batch_pages 2048`,
     `band_kb 65536`, `usable_kb 6927064`, `COMMIT_OK`, rc 0 — matches my hand arithmetic.
   * Hand case D (kbytes 4194304, swap 1048576): observed `limit_recomputed_kb 5242880` with
     `findings:[{"id":"limit_mismatch","printed_kb":5235712,"recomputed_kb":5242880}]`, rc 0 — my *printed*
     value was arithmetically wrong and the tool flagged it, which is the finding working as documented.
2. **Mode branches, 173–196 vs `util.c.v7.2:959-1003`.** Mode 1 → `return 0` (173–175). Mode 0 → only a request
   above `totalram_pages() + total_swap_pages` is refused; the cap at 178 uses ram+swap pages and does **not**
   subtract hugetlb, as the kernel does not (hand case E: `single_request_cap_kb 16777216 = 4194304*4`, rc 0).
   Mode 2 → `usable_kb = headroom - (admin + user reserve)` (185–186) compared with `<=` (187) against
   `batch*cpus*page`; `over_limit_not_enforced` only in modes 0/1 (195), matching the docstring's split.
3. **Band, 182–184 vs `mm_init.c.v7.2:191-210`.** The expression is the kernel's, including the `INT_MAX` cap
   and the `max(2*nr, 32)` floor, and `ram_pages` is `totalram_pages()` (`MemTotal // page_kb`, exact because
   `show_val_kb` prints `totalram_pages << (PAGE_SHIFT-10)`), not totalram−hugetlb — which is what
   `mm_compute_batch` uses. The premise "each local delta below one batch" holds: `vm_acct_memory` passes
   `vm_committed_as_batch` (`mman.h.v7.2:76-79`) and `percpu_counter_add_batch` folds as soon as
   `abs(count) >= batch` (`percpu_counter.c.v7.2:100,127`), so the lag per CPU is `< batch` pages and
   `batch × cpus × page` is a strict upper bound. `percpu_counter_read_positive` returns `fbc->count` only
   (`percpu_counter.h.v7.2:118-126`) while the printed `Committed_AS` is `percpu_counter_sum_positive`
   (`util.c.v7.2:937-941`): the tool subtracts the *larger* (exact) figure, the conservative direction.
   Hand checks: 64-CPU floor case `batch 128, band 32768`; one CPU `batch 2048, band 8192`; sparse `0,2-5,8`
   → 6 CPUs, `batch 10922, band 262128`; band edge committed 4022272 → `usable_kb 32768 == band_kb` → LOW rc 1,
   committed 4022268 → `32772 > 32768` → OK rc 0 (the shipped cases `mode2-band-edge-equal-is-low` /
   `-one-page-above` agree with my arithmetic).
4. **Exit map, line 74** = the contract's (`OK`/`HEURISTIC`/`UNLIMITED` 0, `LOW` 1, `UNKNOWN` 2); the `unknown()`
   path (136–141) sets all 13 reading fields, `findings` and `notes`, matching the docstring.
5. **Parsing, 91–133.** Duplicates of a wanted key → `InputError` (102), missing required keys → `InputError`
   (108), `Hugetlb` optional defaulting to 0 (111 — correct also when `CONFIG_HUGETLB_PAGE` is off, where
   `hugetlb_report_meminfo` prints nothing and `hugetlb_total_pages()` is 0); non-`<digits> kB` values rejected
   (104); non-wanted keys and their duplicates ignored (99); each vm file must be a non-negative integer (130–133).
6. **`--selftest`, 246–278.** `tempfile.mkdtemp` honours `TMPDIR`; `finally: shutil.rmtree` runs on every path
   (256–267) — after the run `ls -A $TMPDIR` was empty; the PASS line is the last stdout line, so `count-c2.py`'s
   `SELFTEST_RE.match(lines[-1])` (line 333 of the counter) finds it.
   `python3 -I -B tools/mori-commit-runway.py --selftest` → `MATCHER: rejected 23/23 corrupted expectations` /
   `MORI_COMMIT_RUNWAY_SELFTEST: PASS 23/23`, rc 0.
7. **Counter at the measured commit:**
   `python3 .ufo/waves/round-53/count-c2.py 2a4213bf8da72f7cd78189baa5bb9be825dca1df --scratch …` →
   `C2=met tool=present selftest=pass n=23 fixtures=80 agree=80 disagree=0 registry=ok live=ok rev=2a4213bf…`,
   rc 0; scratch empty afterwards, lane clean apart from the uncommitted tool change noted below.
8. **Differential fuzz, tool vs the frozen REF:** 400 random inputs (unit variants, duplicate/missing keys,
   overlapping/reversed/garbage CPU lists, page sizes 1–64, ratios 0–199, kbytes, hugetlb, modes 0/1/2/3/7),
   all 15 fields and the exit code compared → **0 divergences**. So the tool is the counter's reading outside the
   fixture sample as well; the remaining risk is a *shared* kernel misreading, which is what the kernel checks
   above address.

---

## Findings in detail (F1–F10)

### F1 — MED — a >4300-digit number aborts with a traceback, exit 1 (the `COMMIT_LOW` code), no JSON
Lines **107** (`vals[key] = int(kb.group(1))`), **122** (`a, b = int(lo), int(hi) …`), **133** (`return int(t)`);
the handler at **149** catches only `InputError`, so Python 3.11+'s int-string limit escapes `evaluate`.
```
$ python3 -I -B tools/mori-commit-runway.py --meminfo <5000-digit MemTotal> --vm-dir … --page-kb 4
  File ".../mori-commit-runway.py", line 107, in parse_meminfo
    vals[key] = int(kb.group(1))
ValueError: Exceeds the limit (4300 digits) for integer string conversion: value has 5000 digits
rc=1
```
Same for a 5000-digit CPU list (line 122) and a 5000-digit `overcommit_ratio` (line 133), rc 1 in both. This
contradicts the docstring (41–42: "Anything required missing, unreadable or malformed … `COMMIT_UNKNOWN`, exit 2")
and the frozen verdict map: exit 1 is the `COMMIT_LOW` code, so a consumer that gates on the exit code alone
(SKILL.md: "1 → failed (`COMMIT_LOW`)") reads a corrupt input as "inside the band", on stderr only and with no
JSON object. `count-c2.py` never generates a 4300-digit value, so the counter cannot see this.
Reproduce: write any one of those files with `"9"*5000`.

### F2 — LOW — the usage-error object is not the frozen field set
Lines **283–285**. Every other `COMMIT_UNKNOWN` path goes through `unknown()` (136–141) and emits
`mode … limit_consistent` as null plus `findings`; the argparse path prints a look-alike with three keys only:
```
$ python3 -I -B tools/mori-commit-runway.py --bogus
{"schema": "mori-commit-runway-v1", "verdict": "COMMIT_UNKNOWN", "notes": ["usage: unrecognized arguments: --bogus"]}
rc=2
```
A reader of the contract's field list (`verdict mode enforced commit_limit_kb … limit_consistent`) gets a
`KeyError` on `out["mode"]` instead of `null`; only `.get()` consumers survive. Exit code 2 and the `usage:` note
are correct. Not exercised by the counter.

### F3 — LOW — `--selftest` passes with zero cases
Lines **246–277**: `rejected != len(cases)` is `0 != 0`, so the matcher arm passes and `PASS %d/%d` prints n/n.
```
$ printf '{"cases": []}' > /fast/scratch/.../empty.json
$ python3 -I -B tools/mori-commit-runway.py --selftest --cases …/empty.json
MATCHER: rejected 0/0 corrupted expectations
MORI_COMMIT_RUNWAY_SELFTEST: PASS 0/0
rc=0
```
The docstring says "exit 0 only when all pass"; with no cases nothing is checked, and `--cases` is a documented
flag (SKILL.md registry row), so an operator can get a green selftest from an empty or accidentally emptied file.
The claim is not at risk — `count-c2.py` requires `n >= MIN_SELFTEST = 12`.

### F4 — LOW — the matcher arm mutates only `verdict`, so "rejected 23/23" does not bound the other 13 fields
Lines **239–243** (`_corrupt` flips `expect["verdict"]` only), compared at **231**. Because the corrupted verdict
always differs from the tool's actual verdict, `rejected == len(cases)` is implied by the cases passing: the arm
cannot detect a `_mismatches` regression that stops comparing `commit_limit_kb`, `usable_kb`, `band_kb`,
`batch_pages`, `cpus_present` … or `expect_findings`. Demonstrated on a scratch copy whose `_mismatches` compares
only `verdict`:
```
MATCHER: rejected 23/23 corrupted expectations
MORI_COMMIT_RUNWAY_SELFTEST: PASS 23/23
rc=0
```
The shipped `_mismatches` does compare all of them (a copy with one wrong `headroom_kb` fails:
`FAIL host-mode0-over-limit: headroom_kb -12585684 != 123`), so the current expectations are bound — but the SKILL
row quotes `MATCHER: rejected 23/23` as if it were evidence for that, and it is not.

### F5 — LOW — the FAIL summary counts *passing* cases
Line **275**: `total - len([f for f in failed if ":" in f])`. With the corruption made a no-op the tool prints
```
MATCHER: rejected 0/23 corrupted expectations
FAIL matcher accepted a corrupted expectation
MORI_COMMIT_RUNWAY_SELFTEST: FAIL 23/23
rc=1
```
i.e. "FAIL 23/23" while a failure is printed and rc is 1 — the line an operator reads says everything passed. The
`":" in f` label test is also not robust (case ids are used as path components at line 209; an id containing `:`
would be miscounted). A single wrong case reports correctly (`FAIL 22/23`).

### F6 — LOW — `--page-kb` has no plausibility bound beyond "power of two"
Lines **307–308**. `--page-kb 4611686018427387904` (2^62) is accepted and produces a nonsense reading on the F
fixture rather than `COMMIT_UNKNOWN`:
```
"band_kb": 590295810358705651712, "limit_recomputed_kb": 0, "limit_consistent": false,
"findings": [limit_mismatch, inside_band], "verdict": "COMMIT_LOW"  rc=1
```
A page size larger than `MemTotal` cannot exist; the only guard is `limit_mismatch`, which does fire (here
`recomputed_kb 0` vs `printed_kb 1048576`). The same guard is what catches the common unit slip `--page-kb 4096`
(bytes passed for KiB), which is accepted by the committed blob:
```
$ git show 2a4213bf:tools/mori-commit-runway.py > scratch/committed-tool.py
$ python3 -I -B scratch/committed-tool.py --page-kb 4096
"limit_recomputed_kb": 47579136, "commit_limit_kb": 47583772,
"findings": [{"id": "limit_mismatch", "printed_kb": 47583772, "recomputed_kb": 47579136}],
"single_request_cap_kb": 63438848, "verdict": "COMMIT_HEURISTIC"   rc=0
```
(the true cap at `--page-kb 4` is 63444672, so the slip costs 5.8 MB and no verdict change in mode 0; in mode 2 it
would shift `batch_pages` and `band_kb` too). Since `--page-kb` is a documented input, a bound (e.g.
`page_kb <= 1024` or `MemTotal`) would keep a typo from producing a confident verdict.

### F7 — LOW — overlapping CPU ranges are summed, not merged
Lines **115–125**. Present `0-3,2-5` → `cpus_present 8` where `num_present_cpus()` would be 6, which changes the
batch and the band (on the F fixture: `batch 256, band 8192` vs 6 CPUs → `batch 341, band 8184 kB`). The real
`/sys/devices/system/cpu/present` is a disjoint ascending mask, and the frozen REF has the same reading, so
`count-c2.py` cannot see it — a documented parser limit, not a reachable host error.

### F8 — LOW (routed, contract-frozen) — all five `/proc/sys/vm` files are required before the mode is known
Line **147** builds the dict over `VM_FILES`; the mode is only examined at **151**. On a host without
`user_reserve_kbytes`/`admin_reserve_kbytes` (kernel < 3.3) or `overcommit_kbytes` (< 2.6.30) the tool returns
`COMMIT_UNKNOWN` exit 2 even in mode 0/1, where only `overcommit_memory` decides the verdict. The contract froze
the five-file interface and REF matches, so this is a round-54 item, not a fix this round.

### F9 — LOW (provenance) — the Hugetlb unit bridge has no committed source copy
Lines **156** and **160** convert meminfo's `Hugetlb` (kB) to base pages. That step is only correct because
`hugetlb_report_meminfo` prints `total / SZ_1K` with `total = huge_page_size(h) * h->nr_huge_pages`, i.e.
`base_pages * page_kb`, while `hugetlb_total_pages()` returns `nr_huge_pages * pages_per_huge_page(h)` — both in
base pages. `mm/hugetlb.c` is **not** among the round-53 rows or committed copies (`sources-r53/` holds
mm_init.c, percpu_counter.c/.h; S499 holds util.c), so a recheck cannot re-derive the tool's Hugetlb handling
from pinned bytes. I fetched it to confirm (see verification gaps), so the reading is right; the gap is that the
lane cannot re-derive it.

### F10 — LOW — docstring arithmetic differs from the code (doc-only)
Docstring lines **23–25** say `(MemTotal - Hugetlb) / page * overcommit_ratio / 100`; code **160** computes
`(MemTotal//page - Hugetlb//page) * ratio // 100`. The two agree whenever both values are page-aligned (always,
since meminfo prints them shifted by `PAGE_SHIFT-10`), and the code is the form the kernel uses, so this is a
wording fix, not a behaviour change.

---

## Status of the uncommitted worktree (not the measured bytes)

At 2026-10-27T02:14:40Z `git status --porcelain` reports ` M tools/mori-commit-runway.py` against 2a4213bf
(`+136/−23`, sha256 `82924be72e7784dd76d16a53deebfbbc96aed5e2936b162912b5e20f10506506`), citing round-53 findings
`Mo53SentC2ReadOnly` and `Mo53SentC2Hostile`. Observed there, not scored here:
`NUM = [0-9]{1,20}`, a regular-file/1 MiB reader, disjoint ascending CPU lists, `MAX_PAGE_KB = 1024`, a
non-empty-cases check and five hostile-input checks. Probes against that version:
`--selftest --cases <empty>` → `FAIL cannot load cases (cases is not a non-empty list)`, rc 1 (closes F3);
`--page-kb 2^62` → usage `COMMIT_UNKNOWN`, rc 2 (closes F6); the 5000-digit input no longer reaches `int()`
(closes F1). Still open there: the usage JSON at 389–391 (F2), `_corrupt` at 303–306 (F4), and the FAIL numerator
at 380 (`checks - len([f for f in failed if not f.startswith("matcher")])`, same "counts passes" shape → F5).
I did not evaluate that file further; the measured claim is 2a4213bf.

---

## Residual risk

* REF and tool share one author. The 400-case fuzz proves they agree, not that both match the kernel; the
  independent kernel-side checks (limit, modes, band, units) all passed, so the residual shared-misreading space
  is (a) the band being an upper bound computed from today's `totalram`/present CPUs (hotplug and a balloon that
  changes RAM without a MEM_ONLINE recompute widen it), (b) the reserve being the non-root worst case
  (`!cap_sys_admin` at `util.c.v7.2:982`, `min(total_vm/32, reserve)` per process at `:989-991`), (c) meminfo
  truncation — none, every `show_val_kb` shift is exact.
* Sampling race: meminfo is read (146) before the five sysctls (147), so a concurrent sysctl write can produce a
  spurious `limit_mismatch`. The tool's wording ("the reading of the inputs is off") is honest about that.
* The live leg is mode 0 on this host (Linux 7.2.11-arch1-1); one point-in-time read gave `commit_limit_kb
  47583772`, `committed_as_kb 41163136`, `headroom_kb 6420636`, `limit_consistent true`, `COMMIT_HEURISTIC`,
  rc 0 (Committed_AS moved to 35941120/35957640 on later reads, so the headroom figure is not stable).
  `COMMIT_LOW` is exercised only on fixtures; no mode-2 host was available to me.
* The entry's host sentence ("Committed_AS exceeds it — `over_limit_not_enforced`, exit 0") did not reproduce at
  2026-10-27T02:0xZ (`findings: []`). It is date-dated and the counter's live leg compares stable fields only, so
  no claim impact — but a reader taking it as current would be wrong.

## Verification gaps

* **UNVERIFIED:** any real mode-2 host and any 64 kB-page host; the band's hotplug behaviour.
* **Not independently recomputed:** all 23 `cases.json` expectations. Three were hand-checked against the kernel
  formulas (`host-mode0-over-limit`, both band-edge cases) and five wider hand cases (A/B/D/E/F) cover the same
  arithmetic; the file's own `note` says the rest are REF-derived. Full independent fixture recomputation is the
  independent-recomputation seat's ground.
* **Source fetched outside the lane:** `https://git.kernel.org/.../plain/mm/hugetlb.c?h=v7.2` (210457 bytes) into
  scratch, read only at 4517–4545 (`hugetlb_report_meminfo`) and 4586–4594 (`hugetlb_total_pages`) for F9; scratch
  removed afterwards, so F9's confirmation is this report's text, not a lane path.
* Timing: the tool's `--selftest` wall time is under a second; nothing heavy was run, `disk-guard.sh status` was
  checked first (exit 0).

---

## Findings

| id | severity | file:line | finding |
|---|---|---|---|
| F1 | MED | `tools/mori-commit-runway.py:107,122,133` (handler 149) | a >4300-digit number raises `ValueError` out of `evaluate`: traceback, no JSON, exit 1 — the frozen `COMMIT_LOW` code — instead of `COMMIT_UNKNOWN` exit 2 |
| F2 | LOW | `tools/mori-commit-runway.py:283-285` | the usage-error object carries only `schema`/`verdict`/`notes`; the 13 reading fields and `findings` that every other `COMMIT_UNKNOWN` path emits are absent |
| F3 | LOW | `tools/mori-commit-runway.py:246-277` (esp. 269, 277) | `--selftest --cases <empty>` prints `MATCHER: rejected 0/0` and `PASS 0/0`, rc 0: zero cases pass vacuously |
| F4 | LOW | `tools/mori-commit-runway.py:239-243` (compared at 231) | the corruption arm mutates only `expect["verdict"]`, so `MATCHER: rejected n/n` cannot detect a matcher regression on the other 13 fields or `expect_findings` |
| F5 | LOW | `tools/mori-commit-runway.py:275` | the FAIL summary numerator counts passing cases: a matcher-only failure prints `FAIL 23/23`; the `":" in f` label test is fragile |
| F6 | LOW | `tools/mori-commit-runway.py:307-308` | `--page-kb` accepts any power of two (2^62 observed) with no plausibility bound; the verdict becomes nonsense and only `limit_mismatch` hints at it |
| F7 | LOW | `tools/mori-commit-runway.py:115-125` | overlapping CPU ranges are summed: `0-3,2-5` → 8 CPUs vs the kernel's 6, shifting batch and band |
| F8 | LOW | `tools/mori-commit-runway.py:147,151` | all five vm files are required before the mode is examined; a host missing a reserve file reads `COMMIT_UNKNOWN` in modes 0/1 (contract-frozen → round 54) |
| F9 | LOW | `tools/mori-commit-runway.py:156,160` | the meminfo `Hugetlb` (kB) → `hugetlb_total_pages()` bridge has no committed source copy (`mm/hugetlb.c`), so a recheck cannot re-derive it |
| F10 | LOW | `tools/mori-commit-runway.py:23-25` vs `:160` | the docstring's `(MemTotal - Hugetlb) / page * ratio / 100` and the code's subtract-in-pages differ as written (identical as computed) |

No HIGH finding: at 2a4213bf the tool implements the frozen C2 interface on well-formed inputs; `count-c2.py`
reads `C2=met … agree=80 disagree=0 registry=ok live=ok` there, and a 400-input differential fuzz finds no
divergence from the counter's reference reading.
