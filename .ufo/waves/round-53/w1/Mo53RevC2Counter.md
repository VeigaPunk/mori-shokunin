# Mo53RevC2Counter — `.ufo/waves/round-53/count-c2.py`, reviewed line by line

Seat: reviewer (leaf, no dispatch). Scope: the C2 counter only — REF against the kernel lines it cites, the
fixture generators (verdict and band-edge reach), `compare()` strictness, the selftest's hand arithmetic, the
harness, the live leg, and whether the docstring predicate is the condition the code implements. The tool was
read only to establish whether the instrument can see its errors; the tool's own defects belong to the tool seat.

Machine: MACHINE_ID (host MemTotal 31721796 kB, 32 present CPUs, page 4 kB, `vm.overcommit_memory=0`).
Scratch: `/fast/scratch/hyaku/mori-r53/Mo53RevC2Counter/` (`tmp/`, `c2/`, one-off python via heredoc); removed
at the end of the seat. No tool installed or upgraded. No file outside this report was written; lane reads were
`read`, `grep`, `git log/show/rev-parse/ls-tree/archive` only.

## Commands run (evidence)

```
$ python3 .ufo/waves/round-53/count-c2.py --selftest
… (30 check lines, all "ok  ")
C2_SELFTEST pass=30 fail=0
exit=0                                    # 19.2 s wall

$ python3 .ufo/waves/round-53/count-c2.py 2a4213bf8da72f7cd78189baa5bb9be825dca1df \
      --scratch /fast/scratch/hyaku/mori-r53/Mo53RevC2Counter/c2
C2=met tool=present selftest=pass n=23 fixtures=80 agree=80 disagree=0 registry=ok live=ok rev=2a4213bf8da72f7cd78189baa5bb9be825dca1df
exit=0                                    # 3.3–4.1 s wall; child peak RSS 655.2 MiB (resource.getrusage RUSAGE_CHILDREN)
                                          # after the run only the empty --scratch root remains (work dir removed)

$ git archive 2a4213bf | wc -c
334049280

$ git -C <lane> show 2a4213bf:tools/mori-commit-runway.py > committed-tool.py
$ git hash-object ./committed-tool.py      # and git rev-parse 2a4213bf:tools/mori-commit-runway.py
27e4d913ee3545e494d8f4d5e02cc19cc1798a78   # the bytes the counter scores; every tool check below used this blob
```

The at-data receipt (`evidence/c2-at-data.txt`) reproduces byte for byte, including `n=23`, `agree=80`,
`disagree=0`, `registry=ok`, `live=ok`, `rev=`. The counter is sound as an instrument at this tip.

## 1. REF against the kernel lines it cites

REF is `count-c2.py:104-159`. Every arithmetic term was traced to a committed copy (all quoted lines read from
`corpus/evidence/sources-r52/util.c.v7.2`, `corpus/evidence/sources-r53/mm_init.c.v7.2`,
`corpus/evidence/sources-r53/percpu_counter.c.v7.2`, `corpus/evidence/sources-r53/percpu_counter.h.v7.2`,
`corpus/evidence/sources-r53/mman.h.v7.3`, `corpus/evidence/sources-r53/meminfo.c.v7.3`).

| REF term (line) | kernel line | verdict |
|---|---|---|
| `ram_pages = MemTotal // page_kb` (`:124`) | `meminfo.c.v7.3:28-31` `show_val_kb` → `num << (PAGE_SHIFT-10)`; `:60` `MemTotal = i.totalram` | held: printed kB is pages × page_kb, so the division recovers `totalram_pages()` exactly for a power-of-two page. Confirmed live: printed CommitLimit 47583772 == REF's recomputation from the printed MemTotal/SwapTotal at ratio 50 |
| `allowed = kbytes // page_kb` else `(ram_pages - huge_pages) * ratio // 100`, then `+= swap_pages` (`:126-133`) | `sources-r52/util.c.v7.2:904-916` `vm_commit_limit` | held, including both precedence and the unconditional `allowed += total_swap_pages` and the precedence of `sysctl_overcommit_kbytes` over the ratio. `>> (PAGE_SHIFT-10)` equals `// page_kb` for power-of-two pages; the v7.2 and v7.3 copies of this function are byte-identical (`diff` empty) |
| `limit_recomputed_kb = allowed * page_kb`, `limit_consistent` (`:137-139`) | `meminfo.c.v7.3:125` `show_val_kb(… vm_commit_limit())` | held |
| `headroom_kb = CommitLimit − Committed_AS` (`:135`) | `meminfo.c.v7.3:126`; `util.c:936-939` `vm_memory_committed` = `percpu_counter_sum_positive` | held: Committed_AS is the exact sum |
| `batch = max(min(ram_pages // cpus // 256, INT_MAX), max(cpus*2, 32))` (`:136`) | `mm_init.c.v7.2:191-210` `mm_compute_batch` | held: `/256` is the `OVERCOMMIT_NEVER` branch (= policy 2), floor `max_t(s32, nr*2, 32)`, cap `INT_MAX`, `nr = num_present_cpus()`, `ram_pages = totalram_pages()` (not minus hugetlb — REF is right not to subtract it here, and right to subtract it in the limit term: the kernel does exactly this split) |
| `band_kb = batch * cpus * page`, `usable_kb = headroom − reserve`, LOW iff `usable ≤ band` (`:136-145`) | `percpu_counter.c.v7.2:93-113` (fold at `abs(count+amount) >= batch`), `percpu_counter.h.v7.2:118-126` (global only, negative→0), `mman.h.v7.3:76-84` (`vm_acct_memory` = `percpu_counter_add_batch(&vm_committed_as, pages, vm_committed_as_batch)`), `util.c.v7.2:960-1000` `__vm_enough_memory` | the *bound* is right (each per-CPU slot holds `< batch`, so `|global − sum| < band`); the *direction* stated for LOW is not — see finding MED-1 |
| `reserve_kb = admin + user` (`:141`) | `util.c.v7.2:977-992` (`allowed -= admin_reserve`; `allowed -= min(total_vm/32, user_reserve)`) | held as a worst-case bound (the kernel's per-process term is `min(total_vm/32, user_reserve)`); the entry discloses it, and the conservative direction is the same one as MED-1 |
| mode 1 → `COMMIT_UNLIMITED`, mode 0 → `COMMIT_HEURISTIC` + `(ram+swap)*page` (`:146-152`) | `util.c.v7.2:968-976` (`ALWAYS` returns 0 before any check; `GUESS` refuses only `pages > totalram + total_swap_pages`) | held |
| `unknown()` on any missing/malformed input, exit 2 (`:98-115`) | — | docstring-level rule, no kernel line needed |

No arithmetic defect found in REF. The frozen edge fixtures and the independent recomputation in §2 agree with it.

## 2. Fixture generators: does the set reach every verdict and the band edge?

At the landed seed `sha256(2a4213bf8da72f7cd78189baa5bb9be825dca1df)` = `bd8349d56c3147bc…`, 16 frozen + 64 seeded:

| half | COMMIT_HEURISTIC | COMMIT_UNLIMITED | COMMIT_OK | COMMIT_LOW | COMMIT_UNKNOWN |
|---|---|---|---|---|---|
| frozen (16) | 2 | 1 | 7 | 2 | 4 |
| seeded (64) | 13 | 13 | 15 | 14 | 9 |

All five verdicts are reached by each half; 38 of 80 fixtures are mode 2; exit codes 0/1/2 all occur
(`(mode,exit)` pairs: `(0,0):15`, `(1,0):14`, `(2,0):22`, `(2,1):16`, `(None,2):13`).

Band edge. The frozen pair pins it to one page: `mode2-band-edge-low` (usable 32768 == band, LOW) and
`mode2-band-edge-ok` (usable 32772, OK) differ by 4 kB. The seeded near-edge branch (`count-c2.py:222-224`)
reaches the edge exactly, verified by an independent recomputation that does not call `ref()`:

```
seeded-53  usable−band =    0  → LOW   (limit 62356096, cpus 2,  batch 6327,  band 809856, usable 809856)
seeded-11  usable−band =   +4  → OK    (limit 8916496,  cpus 8,  batch 29388, band 940416, usable 940420)
seeded-44  usable−band =   −4  → LOW   (limit 39965200, cpus 32, batch 2496,  band 319488, usable 319484)
```

Independent arithmetic matched REF on all three (printed CommitLimit == recomputed in each). 5 seeded fixtures
land within 3 pages of the edge on the LOW side and 3 on the OK side. The batch floor branch
(`max(cpus*2,32) > memsized`) is exercised by 4 of the 80; the `INT_MAX` clamp by none (unreachable below ~2 TB
per CPU). The generator's own degenerate case is handled: when `lim − admin − user − band < 0` the near-edge
fixture clamps `committed` to 0 and stops being near-edge (it stays a valid fixture, just not an edge one).

## 3. `compare()` strictness (`:272-290`)

- Missing key: `k not in got` → reported with `<missing>`; `non-dict` JSON rejected explicitly (`:280`).
- Types: `type(got[k]) is not type(want[k])` catches the traps that `!=` misses — `True == 1`, `32768.0 == 32768`,
  `0 == False`. Confirmed against the tool with `string_numbers` (a mutant in the selftest) and, in my fuzz,
  numbers are int-typed on both sides.
- Exit code compared separately, and a timeout (`rc=None`, `out=""`) degrades to a recorded disagreement
  (`no JSON (rc=None)`) rather than an exception (`run_tool` catches `SubprocessError`/`OSError`, `:263-271`).
- Extra keys are ignored, which is what the predicate says ("15 checked fields"); `notes`/`findings` are
  deliberately outside the contract. Stringly-comparison holes: none found. `want` always carries all 15 keys
  in both branches.
- Residual: `json.loads` accepts `NaN`/`Infinity`; any such value is a float where REF has an int, so it is
  caught by the type arm.

## 4. Selftest hand arithmetic (`:458-560`) — each check recomputed by hand

| check | my recomputation | result |
|---|---|---|
| `ref_host_limit` | 31721796//4 = 7930449; ×50//100 = 3965224; +31722876//4 = 7930719 → 11895943 pages ×4 = **47583772**; cap = 63444672; headroom −12585684 | correct (and 47583772 == the host's printed CommitLimit, read now) |
| `ref_mode2_ok` | 2097152 pages, 32 cpus → 2097152//32//256 = 256, floor 64 → batch 256, band 32768; headroom 194304 − 139264 = **55040** > 32768 → OK | correct |
| `ref_mode2_low` | committed 4030000 → headroom 164304 − 139264 = **25040** ≤ 32768 → LOW, exit 1 | correct |
| `ref_small_batch` | 262144//4//256 = 256; floor max(8,32) = 32 → batch 256, band **4096** | correct |
| `ref_batch_floor` | 262144//64//256 = 16 < max(128,32) = 128 → batch 128, band 32768 | correct |
| `ref_kbytes` | 4194304>>2 = 1048576 pages + 262144 swap = 1310720 ×4 = **5242880** | correct |
| `ref_hugetlb` | (4194304 − 1048576) × 80 // 100 = 2516582 pages ×4 = **10066328** | correct |
| `ref_present_parse` | `0,2-5,8` → 1+4+1 = 6; `0-31` → 32; `3-1` → None; `0-3,x` → None | correct |
| `ref_mode1` | limit 524288 vs committed 9999999 → headroom < 0, band/usable None, UNLIMITED | correct |
| five `ref_unknown_*` | mode 3; dropped Committed_AS; duplicated MemTotal; `CommitLimit` without ` kB`; dropped `overcommit_ratio` → each hits a distinct reject in `parse_meminfo`/`parse_int_file` | correct |
| `ref_limit_mismatch` | printed 123456 vs recomputed 47583772 → `limit_consistent` False | correct |
| `frozen_count` / `seeded_*` / `fixture_verdict_mix` | 16; identical bytes for one seed, different for another; all five verdicts | correct |

Precision nit: the `headroom_kb` assertion in `ref_host_limit` restates REF's own subtraction
(`== 47583772 - 60169456`) rather than pinning an independently derived number; the value is still pinned because
both operands are pinned elsewhere in the same check. `harness_live_witness` (`:553`) accepts `error` as a pass,
so the selftest cannot fail if the live path is broken.

## 5. Harness (`:369-421`)

- Archive: `git archive <rev>` → `tar -x` into a temp tree; `cwd` for every tool run is the archive root
  (`:263-271`, `dirname(dirname(tool))`), which matches the predicate's "run from a git archive of R". The repo
  has no `.gitattributes`, so no `export-ignore` can hide the tool or `cases.json`; `git archive … | tar -t`
  confirms `tools/fixtures/mori-commit-runway/cases.json` ships.
- `-I`: `sys.path[0]` is not the script directory under isolated mode, so a tool that imported a sibling module
  would fail. The shipped tool is stdlib-only and the witness compensates explicitly (`REF_TOOL` inserts
  `C2_COUNTER_DIR`). Not a defect today, but the predicate inherits the restriction.
- Memory: the whole archive is buffered (`:409` `stdout=PIPE`) and then handed to `tar` again (`:413`
  `input=arch.stdout`). 334 049 280 B at this rev; measured child peak RSS **655.2 MiB**. It grows with the
  repository every round.
- Timeouts: rev-parse 60 s, `git show` 60 s, archive 300 s, tar 300 s, tool `--selftest` 300 s, **each fixture
  30 s** (`:263`) × 80. There is no whole-run cap; a tool that sleeps 29 s per fixture costs ≈ 40 min, and the
  worst case of every step is ≈ 57 min.
- Cleanup: the work tree is removed in `finally` (`:417`); verified — after my run only the empty `--scratch`
  root remained. The `--scratch` root itself is created (`:406`) and not removed (harmless), and it is **not**
  required to be outside the lane, so a seat that passes a lane path makes the counter write there.
- Failure mode: `check=True` on `tar` (`:413`) and `tempfile.mkdtemp` (`:405`) raise outside any handler, so a
  setup failure exits **1 with a traceback**, not the documented 2 — indistinguishable by exit code from
  `C2=unmet`.
- Atoms of the scored run are read-only on the lane: `git archive` and `git show` only. (Bytecode: the lane's
  `.ufo/waves/round-53/__pycache__/count-c{1,2}.cpython-314.pyc` exist from 22:58, but a fresh-copy experiment
  shows the counter's own `--selftest` does **not** create them — `REF_TOOL` runs under `-B` — so they came from
  some other lane-local import, not from this counter. See LOW-14.)

## 6. The live leg (`:298-318`)

Fields checked: `mode`, `commit_limit_kb`, `limit_recomputed_kb`, `cpus_present`, `limit_consistent`, each
required to be equal in a pre-run and a post-run REF and equal to the tool's own output. That selection is the
right one: they are the only fields that cannot move between the two reads (`Committed_AS`, `headroom_kb`,
`usable_kb` do). `rc` is constrained only to `{0,1}` (`:313`); the REF exit codes `c1`/`c2` are computed on
`:307-308` and **never used**. On this mode-0 host, REF's live exit is 0, so a tool that printed `COMMIT_LOW`
with exit 1 and the same five stable fields would still be `live=ok`. The docstring and the contract both say
"exits 0 or 1", so the code matches the predicate — the gap is in the predicate's strength, not in the code.

## 7. Docstring predicate vs the code, clause by clause

| docstring clause (lines 8-20) | code | match |
|---|---|---|
| regular file | `isfile and not islink` (`:326`) | yes |
| from a git archive with `python3 -I -B` | `git archive` + `[sys.executable, "-I", "-B", tool]` | yes (interpreter is `sys.executable`, effectively `python3`) |
| `--selftest` exits 0, **last line** `PASS n/n`, n ≥ 12 | `rc == 0`, regex on the last **non-empty** line, `g1 == g2`, `n >= 12` (`:331-337`) | yes, one page more lenient (a trailing blank line is allowed) |
| 16 frozen + 64 seeded from `sha256(<full commit id of R>)` | `frozen_fixtures() + seeded_fixtures(seed)`, `seed = sha256(full)` (`:394`, `:326`) | yes |
| the four `--…` arguments point at the fixture | all four passed (`:274-277`) | yes |
| exits with the reference exit code | `if rc != code` | yes |
| one JSON object, 15 checked fields equal | `json.loads(whole stdout)`, `FIELDS` (15) | yes |
| SKILL.md at R has a table row naming the tool and `--selftest` | any line whose lstrip starts `\|` and contains both (`:351-353`) | yes (loose: any such row, including one about another tool that mentions this path) |
| live: exits 0 or 1 and reports **the mode, CommitLimit, the recomputed limit and the present-CPU count** | five fields — the four plus `limit_consistent` (`:315`) | **no**: the code adds a fifth requirement the sentence does not name |
| usage / output / exit codes / "writes only under --scratch" / "reads the lane with `git archive` / `git ls-tree` / `git show`" | implemented, except `git ls-tree` is never called (`:24` claim) | two small deltas (LOW-4, LOW-5) |

## Residual risk and verification gaps

- REF and the tool share one author, so agreement (`agree=80`) cannot detect a *shared* kernel misreading. I
  checked REF against the committed kernel copies function by function (§1) and found no arithmetic defect, but
  the checks are mine, not an independent implementation of the kernel.
- The band is an upper bound from the batch rule with present CPUs and today's `totalram`; it is not a measured
  deviation, and hotplug/balloon differences are outside it (entry Boundaries). Not ratable by this counter.
- The live leg is host-dependent and, per §6, weaker than `live=ok` suggests.
- I did not re-fetch v7.2/v7.3 bytes from cgit (another seat holds the refetch); I read the committed copies and
  their hashes are pinned in `evidence/freeze-sha256.txt`. Where a claim needs a copy that is not committed
  (v7.3 `mm_init.c`) I say so rather than asserting it.
- Out-of-generator inputs that the scored fixtures never produce were checked for REF/tool divergence against
  the committed blob (`27e4d913…`, extracted with `git show`, not the working tree): 56 hand-built cases (page
  0/1/2/3/8/16/32/64/100/4096/−4; present `0-0`, `0`, `1-0`, `0-1,0-1`, `0,0`, `0-3,2-5`, empty, trailing comma,
  `0-4294967295`; mode 3/−1; ratio 0/101/1000; kbytes 1 with ratio 50; admin 0/2^63; MemTotal 0 / below one page
  / not page-aligned; Hugetlb > MemTotal; every required key dropped; missing Hugetlb; value without ` kB`; CRLF;
  extra and non-colon lines; VM files with `+`, spaces, blank, `0x`, empty) → **0 divergences**, exit codes
  included. The tool and REF are equivalent on the classes the generator omits; the gaps below are instrument
  coverage, not live defects. (Against the *working tree* copy, see finding 18.)

## Findings

1. **MED** — the mode-2 band's *meaning* is stated in the opposite direction to the mechanism it cites, and the
   entry contradicts itself. `corpus/knowledge/commit-runway-read-r53.md:14-18` says the mode-2 test "reads only
   the global part of a per-CPU counter, which lags the sum", then concludes "there, a non-root allocation may
   already be refused although the printed numbers still show room". A lagging global count (`global = sum −
   Σper-CPU deltas`, each `|delta| < batch`) makes `__vm_enough_memory`'s test (`util.c.v7.2:995`,
   `percpu_counter_read_positive(...) < allowed`) *easier* to pass, so the dominant consequence is that the
   kernel can admit allocations while the exact committed sum is already at/over `allowed` — over-admission by up
   to one band (123 904 kB on this host), not early refusal. Early refusal needs Σdeltas negative by ~a band
   (possible only through `vm_unacct_memory`, `mman.h.v7.3:81-84`). The same wrong-direction sentence appears at
   `corpus/knowledge/commit-runway-read-r53.md:39` ("LOW when `usable_kb ≤ band_kb`" in the meaning column),
   `SKILL.md:1187`, and `tools/mori-commit-runway.py:36-37`. The verdict rule is unaffected; only the reading it
   licenses is. Data (entry/SKILL/tool docstring) — correctable by the L1 per the contract; not a counter change.
2. **MED** — the counter buffers the entire repository archive in memory. `count-c2.py:409` (`git archive` into
   `stdout=PIPE`) and `:413` (`input=arch.stdout` to `tar`): 334 049 280 B at the data rev, measured child peak
   RSS 655.2 MiB, with no size guard and growth every round. On a host that runs several counters inside one
   wave this is the largest single allocation any wave seat makes. Counter is frozen: named limit + routed item
   for round 54 (stream `git archive` straight into `tar`), not a re-score.
3. **LOW** — `live_check` computes REF's exit codes and discards them: `count-c2.py:307-308` (`c1`, `c2` unused)
   and `:313` (`rc not in (0,1)`), so `live=ok` does not mean the live verdict or exit code agree with REF.
   Predicate-compatible (docstring says "exits 0 or 1") but the receipt's `live=ok` should not be read as "the
   live reading is correct". Route to round 54 with finding 4.
4. **LOW** — docstring/code divergence in the live clause: `count-c2.py:17-19` names four fields, `:315` requires
   five (`limit_consistent` added). A conforming tool that reports the four but leaves `limit_consistent` null
   live would be `live=bad` although the written predicate does not require it. (Strict direction: the code is
   harder than the text.)
5. **LOW** — harness setup failures exit 1, not the documented 2 (`count-c2.py:23`). `tar … check=True` (`:413`),
   `tempfile.mkdtemp` (`:405`) and `os.makedirs` are unguarded, so an ENOSPC/oom/tar failure produces a
   traceback and exit 1 — the same code as `C2=unmet`, which the kill rule reads as "claim not verified".
6. **LOW** — no whole-run timeout. Per-fixture 30 s (`:263`) × 80 plus 300+300+60+60 s for archive/tar/selftest/
   rev-parse ≈ 57 min worst case; a single slow-but-correct tool on a loaded host is charged as `failed=fixtures`.
7. **LOW** — REF branches with no fixture: non-power-of-two `page_kb` (`:105`), `cpus < 1` (`:111`, unreachable
   through `parse_present`), a meminfo without `Hugetlb` (`:76`, the generator only ever drops
   `MEMINFO_KEYS` = the four required keys, `:227-232`), VM values with surrounding whitespace, and duplicate CPU
   ranges. Verified no REF/tool divergence on all of these (§Residual risk), so the gap is in what the instrument
   *proves*, not a live defect.
8. **LOW** — "frozen" names two disjoint fixture sets of different sizes: the counter's 16 (`contract.md` C2,
   `count-c2.py:178-200`) and the tool's 23 (`tools/fixtures/mori-commit-runway/cases.json`, called "23 frozen
   cases" at `corpus/knowledge/commit-runway-read-r53.md:9` and `SKILL.md:1208`). No oracle conflict — all 23
   cases.json expectations equal REF's (0/23 disagreements, 15 fields and exit code, all five verdicts present) —
   but the word and the number differ by document.
9. **LOW** — `count-c2.py:24` claims the lane is read with `git archive` / `git ls-tree` / `git show`; `git
   ls-tree` is never invoked anywhere in the file.
10. **LOW** — the C2 control counts are seed-dependent and none was measured at the landed rev. Each control is
    its own commit (`controls/controls.py:14` `E = 20edafa5`, `:86`, `:102`) and the counter seeds its 64 fixtures
    from `sha256(<that commit>)`, so the six C2 controls each scored a *different* 64-fixture set, and the
    contract's table elides exactly those revs. The readings are reproducible only through the receipts. Not a
    counter defect; a presentational one for the round-53 record.
11. **LOW** — `count-c2.py:405-407` creates `--scratch` and writes under it without checking that it is outside
    the lane, so the docstring's "writes only under --scratch" is true but the lane-protection depends on the
    caller. Nothing in the predicate forbids a lane path.
12. **LOW** — dead parameter: `meminfo_lines(..., extra=None)` (`:163`) is never passed by any of the 80 fixtures.
13. **LOW** — the only selftest check of the live path accepts `error` as a pass (`:553`), so the harness selftest
    cannot detect a broken live leg.
14. **LOW** — an absent tool still prints `fixtures=80` and `live=error` with neither counted
    (`:319` initialises `live_s="error"`; only `tool_absent`/`registry` land in `failed`), so the do-nothing line
    shows two alarming values that are not failures. Cosmetic; the receipt reads correctly.
15. **LOW** — `corpus/knowledge/commit-runway-read-r53.md:49-50` asserts the batch rule is unchanged at v7.3
    "(`mm_compute_batch` in the v7.3 copy differs only by its line number)", but no v7.3 `mm_init.c` copy is
    committed anywhere in the lane (`corpus/evidence/sources-r53/` holds `mm_init.c.v7.2` only; the nine v7.3
    copies are the C1 files). The recheck line does instruct re-fetching that path next tag, so it is
    forward-covered, but the sentence is unverifiable in-lane today. (The `mm/util.c` half of the same sentence is
    verifiable and holds: v7.2 and v7.3 `vm_commit_limit` are byte-identical.)
16. **LOW** — the entry's host reading is volatile but stated as a property: `commit-runway-read-r53.md:41-43`
    says Committed_AS exceeds the 47583772 kB limit; measured now, Committed_AS is 35351532 kB, so a reader
    re-running the tool today sees no `over_limit_not_enforced` finding (the verdict stays `COMMIT_HEURISTIC`,
    exit 0). Fix by dating the sentence as a snapshot or dropping the exceeds clause.
17. **LOW** — seeded-fixture reproducibility rests on CPython's `random.Random(int)` plus `choice`/`randrange`
    (`count-c2.py:203-256`); the stdlib guarantees reproducibility only for `random()` under a compatible seeder.
    Two seats on different Python versions could score different 64-fixture sets and both be "correct". Note it
    in the named limits rather than changing the counter.
18. **MED** — the lane's working-tree `tools/mori-commit-runway.py` was modified during this wave, after the data
    commit: `git status` reports ` M tools/mori-commit-runway.py`, worktree mtime 2026‑10‑26 23:13:27, committed
    blob `27e4d913…` vs worktree `91a9f40b…` (+41/−10: `MAX_READ_BYTES = 1<<20`, `MAX_CPUS = 1<<16`,
    `MAX_PAGE_KB = 1024`, a `[0-9]{1,20}` numeric regex, an `S_ISREG` check on `_read`). It changed again at
    23:14:17 (20481 B, blob `e5cc756f…`), so the file is being edited while the wave runs and the worktree is not
    a stable reading surface for this round. The C2 reading is
    unaffected — `count-c2.py` reads only committed bytes through `git archive`/`git show`, and my run at
    23:05 reproduced the at-data receipt from blob `27e4d913…` — but the working tree no longer matches
    `2a4213bf`, so the receipt cannot be reproduced from a checkout of the worktree, and any seat that opens the
    file directly now reads a different tool. Measured against REF, that worktree copy diverges on three classes
    the 80 scored fixtures never produce: `--page-kb 4096` and `--page-kb > 1024` (REF accepts, worktree →
    `COMMIT_UNKNOWN`/exit 2), `--cpu-present 0-65536` and wider (REF accepts, worktree rejects), and a meminfo
    value of 21+ digits (REF accepts, worktree rejects). If the edit is to land, it needs its own data commit and
    a re-run of the counter at the new tip; if it is a sibling seat's in-flight mutation it must be restored, per
    the seat rule against mutating the lane.
