# Mo53ExecC2Replay — round 53, wave w1, C2 replay seat (independent run + tool attack)

Lane `mori-shokunin`, fleet root `/home/vgpnk/Projects/shokunin`. Host MACHINE_ID (value withheld per lane
rule). Python 3.14.8, curl 8.23.0, git from the distribution; no tool was installed or upgraded (nothing was
needed, and all pacman transactions remain paused host-wide per the orchestrator ruling). Scratch
`/fast/scratch/hyaku/mori-r53/Mo53ExecC2Replay` (338 MB at peak), `TMPDIR` set to its `tmp/`, removed at the end
(§8). `/fast` had 608 GB free before and 605 GB after; disk-guard ran clean.

Claim under test: C2 (coverage) — `tools/mori-commit-runway.py` as a read-only commit-ledger runway read, by
overcommit mode, at data commit `2a4213bf8da72f7cd78189baa5bb9be825dca1df` (entering tip
`20edafa59b38dac1ca358893f0259b1f436372d3`, freeze `f4da3fd400fa88a6db8ea544a4f7045c15d2410e`). Frozen bytes were
read from the lane and from a `git archive` of `2a4213b` in my scratch; the lane repo, its index and jj state
were never mutated (`git status --porcelain` before and after shows only untracked dispatcher paths and this
wave's `w1/` directory).

## 1. The four assigned runs, replayed

All commands run with `cwd=/fast/scratch/hyaku/mori-r53/Mo53ExecC2Replay` and
`TMPDIR=/fast/scratch/hyaku/mori-r53/Mo53ExecC2Replay/tmp`.

### 1.1 Counter at the data commit

```
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-53/count-c2.py \
      2a4213bf8da72f7cd78189baa5bb9be825dca1df --scratch …/Mo53ExecC2Replay/c2
C2=met tool=present selftest=pass n=23 fixtures=80 agree=80 disagree=0 registry=ok live=ok rev=2a4213bf8da72f7cd78189baa5bb9be825dca1df
exit=0        (wall 4.3 s)
```

Byte-for-byte the receipt line in `.ufo/waves/round-53/evidence/c2-at-data.txt` (that file additionally carries
the literal `$ python3 …` command line, which my run reproduced with a different `--scratch`). A second run of the
same command returned the identical line and `exit=0` — the fixture set is deterministic in the revision
(seed `sha256(full commit id)`, recomputed below).

### 1.2 Counter selftest

```
$ TMPDIR=…/Mo53ExecC2Replay/tmp python3 …/round-53/count-c2.py --selftest
ok   ref_host_limit
ok   ref_mode2_ok
ok   ref_mode2_low
…                                   (30 checks in the receipt's order, one per line; truncated here for length)
ok   harness_live_witness
C2_SELFTEST pass=30 fail=0
exit=0        (wall 21.3 s)
```

The 30 check names and their order are `ref_host_limit, ref_mode2_ok, ref_mode2_low, ref_small_batch,
ref_batch_floor, ref_kbytes, ref_hugetlb, ref_present_parse, ref_mode1, ref_unknown_mode3, ref_unknown_drop,
ref_unknown_dup, ref_unknown_garble, ref_unknown_vmdrop, ref_limit_mismatch, frozen_count, seeded_reproducible,
seeded_varies, fixture_verdict_mix, harness_witness_met, harness_absent_unmet, harness_registry_unmet,
harness_mutant_mode_blind_unmet, harness_mutant_no_band_unmet, harness_mutant_no_hugetlb_unmet,
harness_mutant_string_numbers_unmet, harness_selftest_floor_unmet, harness_selftest_partial_unmet,
harness_memoriser_unmet, harness_live_witness` — identical to `evidence/selftest-c2.txt`, same tail, same exit.
TMPDIR residue after the run: none under `…/tmp`, none under `/tmp`.

### 1.3 Tool selftest from a `git archive` of the data commit

```
$ git -C …/mori-shokunin archive 2a4213bf8da72f7cd78189baa5bb9be825dca1df | tar -x -C …/Mo53ExecC2Replay/arch
$ cd …/Mo53ExecC2Replay/arch && python3 -I -B tools/mori-commit-runway.py --selftest
MATCHER: rejected 23/23 corrupted expectations
MORI_COMMIT_RUNWAY_SELFTEST: PASS 23/23
exit=0
```

`ls -l` on the archived pair: `tools/mori-commit-runway.py` `-rwxr-xr-x` 14785 B,
`tools/fixtures/mori-commit-runway/cases.json` `-rw-r--r--` 24910 B. The archive's 212 `*.pyc` files equal the
212 `__pycache__` entries in `git ls-tree -r 2a4213b` — all round-20 falsify material committed in the lane, none
created by my runs (`-B`).

### 1.4 Fixture dump, first and last three lines

```
$ python3 …/round-53/count-c2.py --fixtures 2a4213bf8da72f7cd78189baa5bb9be825dca1df      exit=0, 80 lines
host-mode0-over        exit=0 {"band_kb": null, "batch_pages": null, "commit_limit_kb": 47583772, "committed_as_kb": 60169456, "cpus_present": 32, "enforced": false, "headroom_kb": -12585684, "limit_consistent": true, "limit_recomputed_kb": 47583772, "mode": 0, "reserve_kb": null, "schema": "mori-commit-runway-v1", "single_request_cap_kb": 63444672, "usable_kb": null, "verdict": "COMMIT_HEURISTIC"}
mode1-over             exit=0 {… "commit_limit_kb": 15860896, "committed_as_kb": 90000000, … "verdict": "COMMIT_UNLIMITED"}
mode2-ok               exit=0 {… "band_kb": 123904, "batch_pages": 968, "commit_limit_kb": 47583772, "committed_as_kb": 20000000, … "usable_kb": 27444508, "verdict": "COMMIT_OK"}
seeded-61              exit=1 {"band_kb": 8388608, "batch_pages": 512, "commit_limit_kb": 57587648, "committed_as_kb": 65453331, "cpus_present": 256, … "usable_kb": -8004947, "verdict": "COMMIT_LOW"}
seeded-62              exit=1 {"band_kb": 89280, "batch_pages": 465, "commit_limit_kb": 11448092, "committed_as_kb": 15292645, "cpus_present": 48, … "usable_kb": -4069434, "verdict": "COMMIT_LOW"}
seeded-63              exit=0 {"band_kb": 637568, "batch_pages": 19924, "commit_limit_kb": 102237128, "committed_as_kb": 101260748, "cpus_present": 8, … "usable_kb": 637580, "verdict": "COMMIT_OK"}
```

Exit distribution over the 80 fixtures: `exit=0` 51, `exit=1` 16, `exit=2` 13 — every verdict class present.

### 1.5 Do-nothing control, replayed

```
$ python3 …/round-53/count-c2.py 20edafa59b38dac1ca358893f0259b1f436372d3 --scratch …/Mo53ExecC2Replay/c2ctl
C2=unmet tool=absent selftest=error n=0 fixtures=80 agree=0 disagree=0 registry=bad live=error failed=registry,tool_absent rev=20edafa59b38dac1ca358893f0259b1f436372d3
exit=1
```

Same line and exit as `evidence/control-c2-do-nothing.txt` (that receipt ran against a throwaway clone with
`--repo`; I ran against the lane repo at the same revision, which is the reading the receipt records).

### 1.6 Extra: the reading also holds at the lane tip

```
$ python3 …/round-53/count-c2.py 95cf78ee --scratch …/Mo53ExecC2Replay/c2head
C2=met tool=present selftest=pass n=23 fixtures=80 agree=80 disagree=0 registry=ok live=ok rev=95cf78eef71979f9b740ef6bc3c5299b6beff86e
exit=0
```

The w1-spec commit above the data commit changes neither the tool, the fixtures nor the registry row.

### 1.7 Fail-closed surfaces (tool and counter)

| probe | output | exit |
|---|---|---|
| `mori-commit-runway.py --selftest --cases` with a case whose expectation I falsified | `MATCHER: rejected 1/1 corrupted expectations` / `FAIL x: exit 2 != 0; verdict 'COMMIT_UNKNOWN' != 'COMMIT_LOW'` / `MORI_COMMIT_RUNWAY_SELFTEST: FAIL 0/1` | 1 |
| `mori-commit-runway.py --nope` | one JSON object, `verdict COMMIT_UNKNOWN`, `notes ["usage: unrecognized arguments: --nope"]` | 2 |
| `mori-commit-runway.py --page-kb 3` and `--page-kb 0` | one JSON object, all reading fields null, `notes ["--page-kb must be a power of two (got N)"]` | 2 |
| `count-c2.py deadbeef` | `C2_SETUP unresolvable revision deadbeef` | 2 |
| `count-c2.py` at the entering tip | §1.5 | 1 |

The tool writes nothing in its working directory (run in an empty dir with a marker file: 0 files newer than the
marker afterwards) and its selftest cleans its `mkdtemp` (0 residues under `$TMPDIR` and `/tmp`).

## 2. Independent recomputation of the reading, from the kernel copies

The trigger for this section is the counter's own named limit: *"REF and the tool may share the author's
misreading of the kernel."* I wrote a second reading (`indep.py`, my own parser and arithmetic) directly from
`corpus/evidence/sources-r53/` — `mm/util.c.v7.3` (`vm_commit_limit`, `__vm_enough_memory`,
`vm_memory_committed`), `mm/mm_init.c.v7.2` (`mm_compute_batch`), `lib/percpu_counter.c.v7.2`
(`percpu_counter_add_batch`), `include/linux/percpu_counter.h.v7.2` (`percpu_counter_read_positive`) — and used
the counter module **only** to obtain the fixture inputs (disclosed: the 16 frozen and 64 seeded fixture
definitions are shared input, not my output).

```
INDEP fixtures=80 vs_ref_disagree=0 vs_tool_disagree=0
CASES n=23 disagree=0
```

- All 80 fixtures: my reading, REF and the shipped tool agree on all 14 checked reading fields and the exit code.
- All 23 cases in the tool's own `cases.json`: agreed with my reading (with the duplicate-key rule the tool uses;
  the one apparent difference was my first script's last-wins duplicate handling, not the tool — see probe
  p01/p16 below).
- Live host: mode 0, 32 present CPUs, `MemTotal 31721796 kB`, `SwapTotal 31722876 kB`, `CommitLimit 47583772 kB`,
  `Hugetlb 0 kB`, `admin_reserve 8192`, `user_reserve 131072`, page 4 kB, `overcommit_ratio 50`,
  `overcommit_kbytes 0`. My reading: `limit_recomputed_kb 47583772`, `limit_consistent true`,
  `single_request_cap_kb 63444672`, `COMMIT_HEURISTIC`, exit 0; the tool on its defaults prints the same on all
  stable fields (`Committed_AS`/`headroom_kb` differ only because the counter moves between the two reads — the
  counter's live leg deliberately compares stable fields only). This also confirms the host paragraph of
  `commit-runway-read-r53.md` ("the recomputed limit equals the printed 47583772 kB").

Hand arithmetic, band edge (frozen fixture `mode2-band-edge-low`, the sharpest case): MemTotal 8388608 kB, page 4
→ 2097152 pages; 32 CPUs → `batch = max(min(2097152/32/256 = 256, INT_MAX), max(64,32)) = 256`;
`band = 256 × 32 × 4 = 32768 kB`; `limit = (2097152 × 50 / 100) × 4 = 4194304 kB`; `reserve = 139264`;
committed 4022272 → `usable = 172032 − 139264 = 32768 ≤ 32768` → `COMMIT_LOW`, exit 1 (dump: exit=1).
`mode2-band-edge-ok` with committed 4022268 → usable 32772 > band → `COMMIT_OK`, exit 0 (dump: exit=0).

### 2.1 Edge inputs outside the fixture set (REF vs tool, side by side)

22 hand-built inputs, each materialised as `meminfo`/`vm/`/`present` files and run through both the counter's REF
and the tool binary; every one agrees on all fields and the exit code:

```
p01-dup-committed_as       ref=2 tool=2 UNKNOWN  AGREE      p12-mode2-space            ref=0 tool=0 OK        AGREE
p02-dup-memfree            ref=0 tool=0 OK       AGREE      p13-no-user-reserve        ref=2 tool=2 UNKNOWN   AGREE
p03/p04 spacing variants   ref=0/2 tool=0/2     AGREE      p14-negative-headroom-m2   ref=1 tool=1 LOW       AGREE
p05-hugetlb-eq-mem         ref=1 tool=1 LOW     AGREE      p15-trailing-space-value   ref=0 tool=0 OK        AGREE
p06-ratio100               ref=0 tool=0 OK      AGREE      p16-garbled-committed_as   ref=2 tool=2 UNKNOWN   AGREE
p07-kbytes-wins            ref=0 tool=0 OK      AGREE      p17-lowercase-key          ref=2 tool=2 UNKNOWN   AGREE
p08-sparse-6cpu            ref=0 tool=0 OK      AGREE      p18-zero-memtotal          ref=1 tool=1 LOW       AGREE
p09-committed-zero         ref=0 tool=0 OK      AGREE      p19-kbytes-below-page      ref=0 tool=0 OK        AGREE
p10-page64-kbytes          ref=0 tool=0 OK      AGREE      p20-no-hugepagesize-line   ref=0 tool=0 OK        AGREE
p11-crlf                   ref=0 tool=0 OK      AGREE      p21-present-zero-range     ref=0 tool=0 OK        AGREE
                                                           p22-ratio-zero             ref=0 tool=0 OK        AGREE
```

That closes the two input classes this revision's fixture set does not exercise (§4.3): a duplicated required
`meminfo` key and a value missing its unit are both rejected identically by REF and the tool.

## 3. Kernel sources re-opened independently (currency at v7.3)

Fetched from cgit (`https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/<path>?h=<tag>`,
the channel the contract names because raw.githubusercontent.com answered HTTP 429) into my scratch:

| file | fetch | sha256 | versus the lane's pinned copy |
|---|---|---|---|
| `mm/mm_init.c?h=v7.3` | 76467 B | `678410005f881a64ae94d180c82174dc4474679b056ace69b6bc3d23978f976c` | no v7.3 copy in the lane to compare with |
| `lib/percpu_counter.c?h=v7.3` | 10932 B | `2c26e67751f939dfb21ff6221884280ae84a2a94a54de4468fb9dc8746130d6d` | identical to `sources-r53/percpu_counter.c.v7.2` (same sha256) |
| `include/linux/percpu_counter.h?h=v7.3` | 6977 B | `4a107bc381b3b5425b8ff441f7487d97ba6883dc6f5b426c4bd361ad7cbef896` | identical to `sources-r53/percpu_counter.h.v7.2` (same sha256) |
| `mm/util.c?h=v7.2` | 43965 B | `4dfcce2b8fa8f18c350565950a10248b3590e3d3c0c9335fef6d47daa7a9e1f2` | identical to `sources-r53/util.c.v7.3` (same sha256); `diff -u` empty |

`mm_compute_batch` at v7.3, lines 195–213, is the same body as v7.2 lines 191–209:
`memsized_batch = min_t(u64, ram_pages/nr/256, INT_MAX)` under `OVERCOMMIT_NEVER`, `ram_pages/nr/4` otherwise,
`vm_committed_as_batch = max_t(s32, memsized_batch, max_t(s32, nr*2, 32))`, `nr = num_present_cpus()`. So the
tool's reading (batch, band, reserve subtraction, `vm_commit_limit`) is unchanged at v7.3, and its v7.2 pinning is
not a staleness defect. Direction of the band, verified from the sources rather than assumed: `__vm_enough_memory`
compares `percpu_counter_read_positive(&vm_committed_as) < allowed` (util.c:994), and that read returns only
`fbc->count` (percpu_counter.h:118–126 v7.2) while `percpu_counter_add_batch` folds a CPU's delta only when
`abs(count + amount) >= batch` (percpu_counter.c:100) — so each CPU's unfolded delta is below one batch, the
printed `Committed_AS` (`vm_memory_committed` → `percpu_counter_sum_positive`, util.c:937–940) is the exact sum,
and `batch × present CPUs × page` is an upper bound on the undercount. Present CPUs ≥ online CPUs, so the bound is
conservative.

## 4. Weaknesses found in the frozen counter (named limits, not fixes — round 54 routing)

The counters, predicates, controls and kill rules are frozen this round; nothing below was used to propose a
change to them, and none of it prevents `C2=met` at `2a4213b`.

4.1 **Registry arm is a loose scan.** `count-c2.py` `evaluate_tree` accepts *any* SKILL.md line that starts with
`|` (after optional spaces) and contains both `tools/mori-commit-runway.py` and `--selftest` — anywhere in the
file, not in the `### Round53 registry additions` table and with no column or kind check. The row at `SKILL.md:1208`
satisfies it legitimately, but a prose row such as `SKILL.md:1182` (the decision-table header that also names the
tool) would satisfy a laxer variant, and the arm cannot tell a registry row from a documentation row.

4.2 **Selftest arm trusts the tool's own case count.** The counter requires `n ≥ 12` and `n == n` from the tool's
own last line; the shipped file has 23 cases. Replacing `tools/fixtures/mori-commit-runway/cases.json` with 12
trivial cases still passes the selftest arm. The 80-fixture arm is the real separator (the contract's junk tools
print a fake `PASS 12/12` and are caught there), so the residual risk is small, but the selftest arm is a
self-declaration.

4.3 **This revision's fixture set exercises no duplicate-key and no garbled-unit input.** For seed
`sha256("2a4213bf8da72f7cd78189baa5bb9be825dca1df") = bd8349d56c3147bc86b2db4be6c8d0f387da0acddd298f7c00e55b73d39dfea4`
the 64 seeded fixtures produced 4 `drop` cases and 5 `vm_drop` cases and 0 `dup`, 0 `garble`, 0 malformed-cpu-list
cases (the generator's `bad < 0.07` / `< 0.09` / `< 0.13` branches did not fire). Verdict mix: seeded 15 OK / 14
LOW / 13 HEURISTIC / 13 UNLIMITED / 9 UNKNOWN; frozen 7 OK / 2 LOW / 2 HEURISTIC / 1 UNLIMITED / 4 UNKNOWN. The
frozen 16 do cover `drop`, `vm_drop` and a malformed cpu list, so the gap is narrow — I closed it for this
revision with probes p01/p16 (§2.1), where REF and the tool agree.

4.4 **`usable_kb` mixes an exact printed value with an approximate decision.** The tool subtracts the *exact*
`Committed_AS` from the limit and compares the result with the band; the kernel's decision uses the
*approximate* read. The inequality direction is right (my §3 derivation), and the entry states it, but the
quantity named `usable_kb` is not the kernel's `allowed − read` and can be up to one band away from it. It reads
as a limit, and the entry's `recheck` prose does not restate it.

## 5. Entry and SKILL text against the bytes

- `SKILL.md:1208` (round-53 registry row) names the tool, its four flags, `--selftest [--cases FILE]`, the default
  paths, the exit map (`0` clean / `1` `COMMIT_LOW` / `2` `COMMIT_UNKNOWN` plus usage), and the selftest's exact
  two printed lines (`PASS 23/23`, `MATCHER: rejected 23/23 corrupted expectations`) — all four verified by §1.3
  and §1.7.
- `SKILL.md:1182–1189` (decision table header and its six rows) matches observed behaviour for `COMMIT_HEURISTIC` (host, mode 0),
  `COMMIT_LOW`/`COMMIT_OK` (fixtures), `COMMIT_UNKNOWN` (probes) and the `limit_mismatch` finding
  (`mode0-limit-mismatch` fixture).
- `corpus/knowledge/commit-runway-read-r53.md` `## Reading rules` matches the tool's arithmetic field for field;
  `usable_kb = CommitLimit − Committed_AS − admin_reserve_kbytes − user_reserve_kbytes`, `LOW` at `≤ band_kb`,
  `band_kb = batch × present CPUs × page size`.
- The entry's `## Boundaries` asserts the v7.3 comparison — see finding 1.

### 5.1 In-flight state of the claim surface (not mine — measured, not touched)

While this seat ran, the lane's **working tree** diverged from the committed bytes. `git log -1` stayed at
`95cf78ee` (the w1-spec commit) throughout, and `git status --porcelain` at 23:2x showed
`M SKILL.md`, `M corpus/knowledge/commit-runway-read-r53.md`, `M tools/mori-commit-runway.py` (142 insertions,
27 deletions versus `95cf78ee`; minutes earlier `tools/fixtures/mori-commit-runway/cases.json` was also modified,
then became clean again with the committed 23-case content). None of the four paths appears in
`.ufo/waves/round-53/evidence/freeze-sha256.txt`, so no frozen byte was edited; I wrote none of these bytes and
left them exactly as found.

The changes are a hostile-input hardening of the tool (regular-file/size/ASCII checks in `_read`, 1–20 ASCII
digits, ascending-and-disjoint CPU lists, `MAX_CPUS`, `MAX_PAGE_KB = 1024`), attributed in its own docstring to
wave findings `Mo53SentC2ReadOnly` and `Mo53SentC2Hostile`, plus an entry paragraph recording that `Committed_AS`
moved between reads and a SKILL registry edit. Working-tree `tools/mori-commit-runway.py` sha256
`82924be72e7784dd76d16a53deebfbbc96aed5e2936b162912b5e20f10506506` (mode 100755).

My C2 measurements are unaffected: `count-c2.py` reads revisions through `git archive`/`git show`, never the
working tree, so §1 scored the committed bytes at `2a4213b` and `95cf78ee`. What *is* observable is a divergence
between the hardening and the frozen REF — see finding 6 — and an inconsistency inside the working tree itself —
finding 7. I did not run the in-flight tool's `--selftest` or score it against the 80 fixtures: that is an
editing wave in flight, and this seat skips it.

## 6. What I did not verify

- No mutation testing of the tool by me: the counter's mutants (`mode_blind`, `no_band`, `no_hugetlb`,
  `string_numbers`, the memoriser) were exercised only through the counter's own selftest (§1.2); I did not
  rebuild them independently. Other seats hold the mutation lane.
- I did not independently re-derive the 64 seeded fixture *inputs* — they are the counter's generator output; my
  independence is on the reading (§2), which is where a shared misreading would show.
- `limit_consistent` on a host with a non-zero huge-page pool: no such host here (`Hugetlb 0 kB`), so the
  `Hugetlb` interpretation is confirmed only by the ratio fixtures (`mode2-hugetlb`, `mode2-hugetlb-ratio80`) and
  by proc.rst's sample (`Hugetlb: 0 kB` next to `Hugepagesize`, `corpus/evidence/sources-r53/proc.rst.v7.3:1115–1117`),
  not by a live non-zero pool.
- I did not run `count-c1.py` (another seat's claim) and did not touch the twelve voter reports.
- I did not score the uncommitted working-tree tool against the frozen 80 fixtures, and did not run its
  `--selftest`; only two single-input probes of it appear in finding 6.

## 7. Machine-readable replay summary

```
counter@2a4213b   C2=met tool=present selftest=pass n=23 fixtures=80 agree=80 disagree=0 registry=ok live=ok rev=2a4213bf8da72f7cd78189baa5bb9be825dca1df   exit=0
counter@95cf78ee  C2=met … same numbers … rev=95cf78eef71979f9b740ef6bc3c5299b6beff86e                                      exit=0
control@20edafa5  C2=unmet tool=absent selftest=error n=0 fixtures=80 agree=0 disagree=0 registry=bad live=error failed=registry,tool_absent   exit=1
selftest          C2_SELFTEST pass=30 fail=0                                                                               exit=0
tool selftest     MORI_COMMIT_RUNWAY_SELFTEST: PASS 23/23 (MATCHER: rejected 23/23)                                        exit=0
indep             80/80 fixtures, 23/23 tool cases, 22/22 edge probes agree with my kernel-derived reading
```

## 8. Scratch hygiene

Everything lived under `/fast/scratch/hyaku/mori-r53/Mo53ExecC2Replay/` (`arch/` the archive tree, `c2*` the
counter scratch, `fx/`, `probe/`, `probe2/`, `ro/`, `tmp/`, the fetched v7.3/v7.2 kernel files, `indep.py`,
`probe.py`, `probe2.py`, `cases_check*.py`). It was removed after this report was written; verified
`ls -d /fast/scratch/hyaku/mori-r53/Mo53ExecC2Replay` → nothing, `/fast` back to 607 GB free. `TMPDIR` was the
scratch `tmp/` for every run; `/tmp` residue check returned 0 for `mori-commit-runway-*`/`c2-*` created by me (the
two `/tmp/c2-<sha>.txt` files present at 17:44 predate this seat's first command by five hours and are not mine).
No file was created inside the lane by any tool I ran, nothing was written to `~/.local/bin` or any PATH
directory, no pacman or install command ran, and no host setting was touched.

Final `git status --porcelain` in the lane (read-only):

```
 M SKILL.md
 M corpus/knowledge/commit-runway-read-r53.md
 M tools/mori-commit-runway.py
?? .ufo/waves/round-53/evidence/selftests/
?? .ufo/waves/round-53/w1.ready
?? .ufo/waves/round-53/w1.ready.dispatched
?? .ufo/waves/round-53/w1/
```

The three modified files are the in-flight edits of §5.1 (not mine); the untracked paths are the dispatcher's and
this wave's, `?? .ufo/waves/round-53/w1/` containing this report.

One further untracked path appeared at the lane root while I was writing this report — `r53-data.tar`, 51200 B,
mtime 2026-10-26 23:19:41 -03, sha256 prefix `e8f6f1c5865446514936883d…`, five members. It is not mine (my archive
was `git archive … | tar -x` inside my scratch), and a stray tarball at the lane root is exactly the class of
artifact the scratch rule exists to prevent; reported as finding 8.

## Findings

1. **LOW — unsourced v7.3 comparison in the C2 entry.**
   `corpus/knowledge/commit-runway-read-r53.md`, `## Boundaries`, first bullet: "the batch rule is unchanged at
   v7.3 (`mm_compute_batch` in the v7.3 copy differs only by its line number)". The lane holds only
   `corpus/evidence/sources-r53/mm_init.c.v7.2` (`evidence/freeze-sha256.txt:23`) and S511 pins v7.2; no v7.3 copy
   of `mm_init.c` exists in `corpus/evidence/sources-r53/` and no SOURCES row names one, so the sentence reports a
   comparison whose bytes the lane cannot show. It is true — my own cgit v7.3 fetch
   (`sha256 678410005f881a64ae94d180c82174dc4474679b056ace69b6bc3d23978f976c`) has lines 195–213 identical to
   v7.2 lines 191–209 — and `limit_consistent` would not catch a drift there. Suggested data correction for the
   L1: cite the fetched v7.3 bytes as a row, or say the rule is unchanged by the v7.3 fetch of 2026-10-26 and pin
   it.
2. **LOW — registry arm accepts any table row.**
   `.ufo/waves/round-53/count-c2.py` `evaluate_tree` (the `for line in (skill_text or "").split("\n")` loop):
   `line.lstrip().startswith("|") and TOOL in line and "--selftest" in line`. A documentation row (`SKILL.md:1182`)
   or a row outside `### Round53 registry additions` satisfies it; no kind, owner or column check. Frozen this
   round; route to round 54.
3. **LOW — selftest arm accepts a self-declared count.**
   `.ufo/waves/round-53/count-c2.py` `evaluate_tree` (`MIN_SELFTEST = 12`, `SELFTEST_RE` last-line check): the 23
   shipped cases could be reduced to 12 trivial ones under `tools/fixtures/mori-commit-runway/cases.json` with the
   selftest arm still green; only the 80-fixture arm separates the contract's junk tools.
4. **LOW — this revision's frozen+seeded arm does not exercise duplicate-key or garbled-unit inputs.**
   For seed `bd8349d5…` the 64 seeded fixtures contain 0 `dup`, 0 `garble`, 0 malformed-cpu-list cases
   (`count-c2.py` `seeded_fixtures`, the `bad < 0.07` / `< 0.09` / `< 0.13` branches); agreement on those classes
   therefore rests on one-author selftests. I closed it for this revision with direct REF-vs-tool probes
   (`p01-dup-committed_as`, `p16-garbled-committed_as`, both AGREE), so no live defect — but the arm's coverage is
   seed-dependent and should be pinned by a junk-tool case in round 54.
5. **LOW — `usable_kb` is not the kernel's decision margin.**
   `tools/mori-commit-runway.py` `evaluate` (mode 2 branch) and `count-c2.py` `ref`: `usable_kb` subtracts the
   exact printed `Committed_AS`, while `__vm_enough_memory` compares the approximate global read; the value can
   differ from the kernel's margin by up to one `band_kb`, in the conservative direction the entry describes. The
   name invites reading it as the margin; the entry's `recheck` line does not restate the caveat.
6. **MED — the in-flight hardening narrows the tool's acceptance surface below the frozen REF, measured on two
   inputs.** Working-tree `tools/mori-commit-runway.py` (sha256 `82924be7…`, not mine, §5.1) against the frozen
   REF of `.ufo/waves/round-53/count-c2.py` on identical fixture files:
   `present = 0-5,2-7` (overlapping ranges — the kernel never prints this, but `count-c2.py` `parse_present`
   accepts it and counts 12 CPUs) → tool `exit 2`, `COMMIT_UNKNOWN`,
   `notes ['cpu present list not ascending and disjoint at 2-7']`; REF `exit 0`, `COMMIT_OK`, `cpus_present 12`,
   `band_kb 32736`, `usable_kb 3055040`. And `--page-kb 2048` (a power of two, accepted by REF's
   `page_kb & (page_kb-1)` guard) → tool `exit 2`, `COMMIT_UNKNOWN`,
   `notes ['--page-kb must be a power of two in 1..1024 (got 2048)']`; REF `exit 0`, `COMMIT_OK`, `cpus_present 8`,
   `band_kb 524288`. The same class covers non-ASCII digits and >20-digit numbers (`MAX_READ_BYTES`, `NUM`), which
   the frozen REF's `re.fullmatch(r"\d+")` accepts. This cannot make C2 unmet under the frozen generator (it emits
   only `page_kb` 4/16/64, ASCII digits and ascending lists), but the tool must never be narrower than the reading
   it is scored against: either the hardening stays outside every input the frozen `seeded_fixtures`/`mk` can
   produce, or the divergence is stated as a known REF/tool mismatch. Route to round 54 with the counters.
7. **MED — the working tree advertises a selftest count its own fixture file does not contain.**
   Working-tree `SKILL.md:1208` says `` `--selftest` → `MORI_COMMIT_RUNWAY_SELFTEST: PASS 31/31` `` and the
   working-tree entry says "the reading below as 26 frozen cases and 5 hostile-input checks", while
   `tools/fixtures/mori-commit-runway/cases.json` holds **23** cases in both the committed and the working tree
   (`len(cases) == 23`, sha256 `cea80451…`). Committing the three modified files without the fixture growth would
   land a registry row whose pinned value does not come from the landed bytes — the round-52 closure D2 class
   ("numbers from the at-data receipt while citing the landed one"). It does not fail the frozen counter (which
   only needs `n ≥ 12` and `n == n`), so it is a reviewer trap, not a claim blocker.
8. **LOW — an untracked tarball at the lane root.** `/home/vgpnk/Projects/shokunin/mori-shokunin/r53-data.tar`
   (51200 B, mtime 2026-10-26 23:19:41 -03, sha256 prefix `e8f6f1c5865446514936883d…`, five members) appeared
   during the wave; not mine, not in `freeze-sha256.txt`, and not a path any seat's report trailer names. A wave
   artifact left in the lane root will be picked up by whatever the next `git add -A`-style integration does; the
   L1 should decide whether to remove it before the integration commit. Matches the scratch rule under
   "every clone, work tree, fixture and temp file lives under `/fast/scratch/hyaku/mori-r53/<seat>/`".
