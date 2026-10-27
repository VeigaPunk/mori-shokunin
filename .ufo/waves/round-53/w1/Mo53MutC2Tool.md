# Mo53MutC2Tool — mutation test of `tools/mori-commit-runway.py` (round-53 claim C2)

Seat: mutation-tester, wave w1, round 53. Lane: mori-shokunin. Target: `tools/mori-commit-runway.py`
at data rev `2a4213bf8da72f7cd78189baa5bb9be825dca1df`.

Scope: challenge the claim that the new C2 tool is verified by (a) its own `--selftest` and (b) the
frozen counter `count-c2.py`. Detection and report only. No lane file was modified (verification in
§Restoration). The counters, predicates, controls and kill rules were treated as frozen and are not
proposed for change; the counter weaknesses found below are named limits and routed items for round 54.

## Method

* Scratch: `/fast/scratch/hyaku/mori-r53/Mo53MutC2Tool/` (one `git clone --shared --no-local` of the lane
  at the data rev; `git rev-parse --show-toplevel` asserted to equal the clone dir before every commit;
  local `user.name`/`user.email` set on the clone only; `TMPDIR` exported to the seat scratch;
  `disk-guard.sh status` checked first — 610.6 G free on `/fast/scratch/hyaku`, no ENOSPC).
* Each mutation is a single-point text edit of the tool source, applied to the *pristine* data-rev bytes
  (`sha256 80cb169650bf02578439703bc006173aab7b759ff9cf57337611b27164676156`) and nothing else.
* Per mutant, two detector readings:
  1. **Tool selftest** — `python3 -I -B tools/mori-commit-runway.py --selftest` in the clone
     (the tool resolves `fixtures/mori-commit-runway/cases.json` from its own directory).
  2. **Counter** — the mutant was *committed* in the scratch clone and scored with
     `python3 -I -B .ufo/waves/round-53/count-c2.py <mutant-rev> --repo <clone> --scratch <seat scratch>`.
     Two commits per mutant were scored (the mutant commit and an empty follow-up commit), because the
     counter's 64 seeded fixtures are derived from `sha256(<full commit id of R>)` — a different commit id
     means a different fixture seed. A mutant that survives one seed may not survive the next, so both are
     reported.
* A third, seed-stable reading was computed directly against the counter's frozen REF and its frozen
  fixture generator at the **data rev's own seed** (`sha256("2a4213bf8da72f7cd78189baa5bb9be825dca1df")`),
  so the fixture arm is measured at a fixed fixture set and is comparable across mutants. This is the
  "REF-arm" column; it uses the counter's own `ref()` and `compare()` unchanged.
* Baseline (pristine tool, pristine clone): `C2=met tool=present selftest=pass n=23 fixtures=80
  agree=80 disagree=0 registry=ok live=ok` — the counter is not broken before mutation.

20 single-point mutations were run (the seat asked for ≥14); all 20 anchors were unique in the pristine
file (the first attempt at M02/M16 hit an ambiguous anchor `max(2 * cpus, 32))` which also occurs in the
docstring at line 34 — re-anchored to the full `batch = max(...)` line at 182 and re-run).

## Results table

`selftest` = the tool's own `--selftest` (exit code and last line). `counter r1/r2` = `count-c2.py`
verdict on the committed mutant at two different fixture seeds. `REF-arm` = fixtures disagreeing with the
frozen REF out of 80 at the data rev's seed.

| id | mutation (one point) | tool `--selftest` | counter r1 | counter r2 | REF-arm disagree/80 |
|----|----------------------|------------------|-----------|-----------|---------------------|
| M01 | `<=` → `<` at the band test | **KILL** (1/23 fail) | **KILL** disagree=1 | **KILL** disagree=4 | 2 |
| M02 | batch floor `32` → `16` | **SURVIVE** (PASS 23/23) | **SURVIVE** `C2=met` | **SURVIVE** `C2=met` | 0 |
| M03 | batch divisor `256` → `4` | **KILL** (11/23) | **KILL** disagree=37 | **KILL** disagree=39 | 38 |
| M04 | present-CPU count +1 | **KILL** (15/23) | **KILL** disagree=69 | **KILL** disagree=69 | 67 |
| M05 | ignore `Hugetlb` in the recomputed limit | **KILL** (1/23) | **KILL** disagree=6 | **KILL** disagree=12 | 12 |
| M06 | ignore `overcommit_kbytes` (ratio path always) | **KILL** (1/23) | **KILL** disagree=13 | **KILL** disagree=16 | 15 |
| M07 | subtract only the admin reserve | **KILL** (11/23) | **KILL** disagree=38 | **KILL** disagree=48 | 38 |
| M08 | mode 0 verdict `COMMIT_OK` | **KILL** (3/23) | **KILL** disagree=10 | **KILL** disagree=16 | 15 |
| M09 | mode 1 reports `COMMIT_LOW` when over the limit | **KILL** (1/23) | **KILL** disagree=4 | **KILL** disagree=7 | 3 |
| M10 | duplicate meminfo-line check removed | **KILL** (1/23) | **KILL** disagree=6 | **KILL** (selftest arm only) | 0 |
| M11 | `kB` unit check removed from the meminfo regex | **KILL** (1/23) | **KILL** (selftest arm only) | **KILL** (selftest arm only) | 0 |
| M12 | integer division → float in the ratio limit | **KILL** (14/23) | **KILL** disagree=51 | **KILL** disagree=51 | 52 |
| M13 | page size ignored for `ram_pages` (fixed 4 kB) | **KILL** (1/23) | **KILL** disagree=22 | **KILL** disagree=30 | 17 |
| M14 | reversed CPU range accepted | **KILL** (1/23) | **KILL** (selftest arm only) | **KILL** (selftest arm only) | 0 |
| M15 | band drops the per-CPU factor (`batch*page`) | **KILL** (10/23) | **KILL** disagree=35 | **KILL** disagree=42 | 33 |
| M16 | batch floor `32` → `64` | **SURVIVE** (PASS 23/23) | **SURVIVE** `C2=met` | **SURVIVE** `C2=met` | 0 |
| M17 | user reserve subtracted twice | **KILL** (11/23) | **KILL** disagree=39 | **KILL** disagree=45 | 38 |
| M18 | `enforced` true in mode 0 | **KILL** (3/23) | **KILL** disagree=13 | **KILL** disagree=11 | 15 |
| M19 | swap pages omitted from the recomputed limit | **KILL** (4/23) | **KILL** disagree=32 | **KILL** disagree=23 | 18 |
| M20 | mode 2 verdict ignores the band (always `COMMIT_OK`) | **KILL** (3/23) | **KILL** disagree=18 | **KILL** disagree=25 | 16 |

**Summary: 18 of 20 mutants killed by both detectors. 2 survivors (M02, M16) — killed by neither.**
M02 and M16 are *not* equivalent mutants: see §Survivors.

Kill-attribution detail (from the counter's own `failed=` field): most mutants trip both arms
(`failed=fixtures,selftest`). M04, M12, M19 additionally trip `live` (`failed=fixtures,live,selftest`) —
their JSON fields change on the real host too. **M11 and M14 are killed only by the selftest arm**
(`failed=selftest`, `disagree=0`): the counter's 80-fixture REF arm never exercises a missing `kB` unit or
a reversed CPU range, so for those two mutants the counter's *fixture* arm is blind and the tool's own
fixtures are the only detector. M10's fixture arm is seed-dependent (killed at seed r1, `disagree=0` at r2).

## Survivors (the finding)

### M02/M16: the batch floor literal `32` is invisible to every frozen fixture

Both survivors change the constant in

```
        batch = max(min(ram_pages // cpus // 256, INT_MAX), max(2 * cpus, 32))
```

`tools/mori-commit-runway.py:182`.

This constant is not the tool's invention. The kernel source pinned as S511
(`corpus/evidence/sources-r53/mm_init.c.v7.2:195`) reads

```c
	s32 nr = num_present_cpus();
	s32 batch = max_t(s32, nr*2, 32);
```

and S512 (`percpu_counter.c.v7.2:262`) reads `percpu_counter_batch = max(32, nr*2);`. The tool's
`max(2 * cpus, 32)` is a faithful transcription of `max_t(s32, nr*2, 32)`. Changing the literal to 16 or
64 makes the tool **wrong against the kernel** — and both detectors score it as correct.

Why the fixtures miss it: the literal `32` only decides the batch when `2*cpus <= 32` **and**
`ram_pages/cpus/256 < 32`. Measured over the counter's 80 fixtures at the data rev's seed:

* CPU-count distribution of the seeded fixtures: `1:5, 2:5, 4:5, 6:1, 8:6, 12:4, 16:7, 32:12, 48:6,
  64:6, 96:7, 128:6, 256:7` — 74 of 80 fixtures have `2*cpus > 32`, where the literal is irrelevant.
* For the remaining low-CPU fixtures, `ram_pages/cpus/256` never drops below 32: the smallest observed
  values per CPU count are `1:3330, 2:6327, 4:5895, 8:95, 12:5193, 16:492` — all far above the literal.
* **0 of 80** counter fixtures and **0 of 23** tool cases have the literal binding
  (`2*cpus <= 32 and mint < 32`). The tool's `mode2-batch-floor-64cpu` case is named for the floor but
  has `2*cpus = 128`, so it exercises `nr*2`, never the `32`.
* Over 300 independent fixture seeds, only **21** produce a fixture that would expose M02 and **79** one
  that would expose M16 — i.e. ~93 % / ~74 % of possible commits would score these mutants as correct.

The mutants are demonstrably wrong, not equivalent. Witness fixtures (MemTotal 128 MiB / 8 CPUs), built
from the counter's own `mk()` and `ref()`:

| fixture | pristine | M02 (floor 16) | M16 (floor 64) | REF |
|---|---|---|---|---|
| `wit-128m-8cpu` | batch=32 band=1024 | batch=**16** band=**512** | batch=**64** band=**2048** | batch=32 band=1024 |
| `wit-64m-4cpu` | batch=32 band=512 | batch=**16** band=**256** | batch=**64** band=**1024** | batch=32 band=512 |
| `wit-256m-12cpu` | batch=32 band=1536 | batch=**24** band=**1152** | batch=**64** band=**3072** | batch=32 band=1536 |

`count-c2.py`'s own `compare()` on the `wit-128m-8cpu` witness:
`mode2-batch-floor-32-binds: band_kb want=1024 got=512; batch_pages want=32 got=16` (M02) and
`… got=2048 … got=64` (M16). The pristine tool agrees with REF on every witness. The mutants change the
band — and therefore the `COMMIT_LOW` decision — on exactly the small-RAM / few-CPU hosts where the
literal is the binding term.

**Where the fix belongs.** The tool's code is correct; the *fixtures* are incomplete. `tools/fixtures/
mori-commit-runway/cases.json` is data (the L1 may correct it), whereas `count-c2.py` is frozen. I
verified the fix works, using a candidate tool fixture only (no counter change):

* candidate case `mode2-batch-floor-32-binds`: MemTotal 131072 kB (128 MiB), present `0-7`, page 4,
  mode 2 → `ram_pages/cpus/256 = 32768/8/256 = 16 < 32`, so the literal binds;
  expected `batch_pages=32`, `band_kb=1024`, `usable_kb=-74728`, verdict `COMMIT_LOW`, exit 1,
  findings `["inside_band"]`.
* tool `--selftest` with the added case: pristine **PASS 24/24**; M02 **FAIL 23/24**; M16 **FAIL 23/24**.
* `count-c2.py` on the committed mutant + added fixture:
  `C2=unmet tool=present selftest=fail n=0 fixtures=80 agree=80 disagree=0 registry=ok live=ok
  failed=selftest` (exit 1) for both M02 and M16.
* control — the added fixture alone with the pristine tool:
  `C2=met tool=present selftest=pass n=24 fixtures=80 agree=80 disagree=0 registry=ok live=ok` (exit 0).

The candidate fixture JSON is copied in §Evidence below. I make no change to any lane file.

### M11/M14: the counter's fixture arm is structurally blind to two input classes

Independently of M02/M16, the counter's 80-fixture REF arm never generates (measured over 300 seeds):

* a meminfo value without the `kB` unit — **0 of 300 seeds** produce one (the `garble` knob exists in
  `count-c2.py`'s `meminfo_lines` but the seeded generator never sets it);
* a reversed CPU range — **0 of 300 seeds** produce one (the seeded generator's malformed `present` is
  `"0-N,a"`, i.e. garbage, not reversed);
* a duplicated required meminfo key — **257 of 300 seeds** produce one, but **not** at the data rev's
  seed (0 of 80), which is why M10's fixture kill is seed-dependent.

The tool's own `cases.json` *does* cover all three (`unknown-swaptotal-no-unit`,
`unknown-cpulist-reversed`, `unknown-committed-twice`), which is why the tool's selftest kills M10/M11/M14
while the counter's fixture arm does not. So for those three mutants the counter's fixture arm contributes
nothing and the selftest arm is the whole detector. I confirmed the mutants are genuinely wrong: with a
witness fixture missing the ` kB` unit, M11 disagrees with REF
(`exit want=2 got=0; verdict want='COMMIT_UNKNOWN' got='COMMIT_OK'`); with a witness `present="7-0"`, M14
disagrees the same way; the pristine tool agrees with REF on both.

## Also worth recording

* The tool's formula matches the pinned kernel exactly: `mm_init.c.v7.2:195` `max_t(s32, nr*2, 32)` and
  `:205` `memsized_batch = min_t(u64, ram_pages/nr/256, INT_MAX)` under `OVERCOMMIT_NEVER`, else
  `ram_pages/nr/4` (`:207`) — the tool applies the `/256` form only under mode 2 and the `/4` form never
  (it only needs the mode-2 band), and `percpu_counter.c.v7.2:339` `unknown = batch * num_online_cpus()`
  is the per-CPU error the band approximates. No defect found in the transcription.
* The live leg is host-dependent and this host is in mode 0 (`/proc/sys/vm/overcommit_memory` = 0,
  present = online = possible = `0-31`, MemTotal = 31721796 kB). `C2=unmet` was never observed for a
  pristine build here, so the live leg is exercised but never the deciding arm in this host's mode.
* `count-c2.py`'s seed (`sha256(<full commit id of R>)`) makes the 64 seeded fixtures change with every
  commit. Any mutation-testing or future fixture change must be read at more than one seed, or a
  seed-dependent mutant can be reported as killed or as survived depending on the commit id. This is a
  named limit of the counter, not a proposed change.

## Restoration evidence

**My seat wrote exactly one lane file: this report.** Every mutation was applied to a scratch clone
(`/fast/scratch/hyaku/mori-r53/Mo53MutC2Tool/clone`); the lane's `tools/` and `corpus/` trees were never
targets of a write.

Lane state at the start of my seat (measured before any mutation), and again after the mutation runs:

```
$ sha256sum tools/mori-commit-runway.py tools/fixtures/mori-commit-runway/cases.json
80cb169650bf02578439703bc006173aab7b759ff9cf57337611b27164676156  tools/mori-commit-runway.py      <- = data rev blob
cea8045192babe3017a2682c17a1647e73c597eaf0330a27643858577cc43b63  tools/fixtures/.../cases.json     <- = data rev blob
$ git rev-parse HEAD
95cf78eef71979f9b740ef6bc3c5299b6beff86e
$ git status --porcelain
?? .ufo/waves/round-53/evidence/selftests/
?? .ufo/waves/round-53/w1.ready
?? .ufo/waves/round-53/w1.ready.dispatched
?? .ufo/waves/round-53/w1/
```

**Concurrent change by the L1, not by me.** After my mutation runs and my first integrity check, the lane
worktree copy of `tools/mori-commit-runway.py` changed underneath me (file mtime 2026-10-26 23:13:27,
`git status` → ` M tools/mori-commit-runway.py`; `jj status` shows the change in the working-copy commit
`e2668c07`, i.e. an uncommitted L1 edit — the data rev's blob is untouched:
`git cat-file -p 2a4213b…:tools/mori-commit-runway.py` still hashes to `80cb1696…`). The edit adds a
digit-bounded numeric regex, a bounded/never-blocking `_read`, an ascending-disjoint CPU-list check and a
CPU-count ceiling, and the L1 was still editing `tools/fixtures/mori-commit-runway/cases.json` (23 → 26
cases) at 23:14:25 while my seat was reading it. My seat made no write to either file: my mutations were
applied to `…/Mo53MutC2Tool/clone/tools/mori-commit-runway.py` inside the scratch clone, and the only lane
path my seat ever wrote is this report.

**The finding survives the L1's in-flight version.** I re-ran the two survivors against a consistent
snapshot of the L1's current worktree (tool sha `82924be7…`, cases.json sha `3a1aef20…`, 26 fixture cases
plus 5 built-in hostile checks = 31 selftest checks):

| variant | L1 worktree `--selftest` | REF-arm disagree/80 | witness `wit-128m-8cpu` batch / band |
|---|---|---|---|
| L1 snapshot, pristine | **PASS 31/31** | 0 | 32 / 1024 |
| L1 + M02 (floor 16) | **PASS 31/31** | 0 | **16 / 512** |
| L1 + M16 (floor 64) | **PASS 31/31** | 0 | **64 / 2048** |

M11 and M14 remain killed by the L1 version's own selftest (`FAIL 29/31` and `FAIL 30/31` respectively),
so finding 2's "the tool's fixtures are the only detector" still holds; M14 is now caught twice over
(the L1 added a second reversed-range guard), and the counter's fixture arm is still blind to it
(0 of 300 seeds produce a reversed range). No L1 fixture case binds the literal `32` either — 0 of 26.

The scratch clone's tool and fixture files were restored to the data rev's bytes and verified
(`git diff 2a4213b… -- tools/` empty; worktree sha `80cb1696…` = pristine). The scratch tree
(`/fast/scratch/hyaku/mori-r53/Mo53MutC2Tool/`) is removed on exit by the seat.

No tool was installed or upgraded for this seat (no pacman, no uv tool, no network fetch); everything ran
on the host's stock `python3`.

## Evidence (copies, all under the seat scratch, removed with it)

* `Mo53MutC2Tool-evidence.json` — the detection matrix of §Results table (per mutant: the tool's failing
  selftest case count, the REF-arm disagreement count, the mutant's sha256) plus the data rev, the fixture
  seed and the candidate floor fixture's full expectation block.
* `cases-with-floor.json` — the candidate tool fixture file (pristine 23 cases + `mode2-batch-floor-32-binds`),
  the exact bytes that kill M02/M16 and leave the pristine tool passing.

## Findings

1. **MED — `tools/mori-commit-runway.py:182`: the batch floor literal `32` is unverified by any frozen
   fixture.** Mutants changing `max(2 * cpus, 32)` to `16` (M02) or `64` (M16) pass the tool's `--selftest`
   (23/23) and score `C2=met` on `count-c2.py` at two fixture seeds, yet change `batch_pages` and `band_kb`
   against the kernel's `max_t(s32, nr*2, 32)` (`corpus/evidence/sources-r53/mm_init.c.v7.2:195`,
   `percpu_counter.c.v7.2:262`) on small-RAM / few-CPU hosts. 0 of 80 counter fixtures and 0 of 23 tool
   cases exercise the regime; only 21/300 and 79/300 possible fixture seeds would. The tool code is
   correct — the fixtures are incomplete. Fix route (data, verified): add a tool fixture with
   MemTotal 128 MiB / 8 present CPUs (`ram_pages/cpus/256 = 16 < 32`); that makes the tool's selftest
   report `FAIL 23/24` for both mutants and the counter report `C2=unmet failed=selftest`, while the
   pristine tool still passes 24/24 and the counter still reports `C2=met`. Candidate JSON in
   §Evidence. Routed to the L1 (fixtures are data); round-54 item: the counter's seeded generator should
   produce low-RAM / low-CPU fixtures so the floor is covered without relying on the tool's own file.
   **Re-verified against the L1's in-flight worktree version** (tool sha `82924be7…`, 26 fixture cases +
   5 hostile checks = 31): M02 and M16 still `PASS 31/31` and still disagree 0/80 with REF, while the
   witness fixture shows batch 16 / band 512 (M02) and 64 / 2048 (M16) against the pristine 32 / 1024;
   0 of the L1's 26 fixture cases bind the literal either. The gap is still open.
2. **MED — `.ufo/waves/round-53/count-c2.py` fixture arm (frozen): structurally blind to two input classes.**
   Across 300 seeds the counter's seeded fixtures never contain a meminfo value missing the `kB` unit and
   never a reversed CPU range; the data rev's seed also contains no duplicated required meminfo key.
   Consequently M11 (unit check removed) and M14 (reversed range accepted) are killed only by the selftest
   arm (`failed=selftest`, `disagree=0`), and M10's fixture kill is seed-dependent. The tool's own
   `cases.json` covers all three, so today the tool's fixtures are the only detector for these inputs.
   Named limit, not a proposed counter change: routed to round 54. Still true of the L1's in-flight
   version (M11 `FAIL 29/31`, M14 `FAIL 30/31`; the counter's fixture arm remains at 0 of 300 seeds).
3. **LOW — `.ufo/waves/round-53/count-c2.py` seed is commit-id-derived** (`sha256(<full commit id of R>)`),
   so the 64 seeded fixtures change with every commit. A mutation reading at one seed is not stable: M10
   was killed at one mutant commit and survived the fixture arm at the next. Any future fixture or tool
   change should be scored at more than one seed. Named limit.
4. **LOW — `tools/fixtures/mori-commit-runway/cases.json`: the case named `mode2-batch-floor-64cpu` does not
   test the floor.** It has 64 present CPUs, so `2*cpus = 128` always exceeds the literal `32`; the case
   exercises `nr*2`, never the `max_t(..., 32)` term. The name over-promises what the case covers. Still
   true of the L1's in-flight 26-case file.
5. **LOW — no defect found in the tool's transcription of the kernel.** `mm_init.c.v7.2:195-209` and
   `percpu_counter.c.v7.2:262,339` match the tool's `max(2*cpus, 32)`, `ram_pages/cpus/256`, and the
   per-CPU error band. 18 of 20 single-point mutations are killed by both detectors; the two survivors
   are a fixture-coverage gap, not a tool defect.
6. **LOW — lane worktree changed concurrently during this seat (L1, not this seat).** The L1's uncommitted
   edits landed while this seat was running, so the lane worktree no longer matches the data rev's blobs.
   The files observed modified in the worktree at the end of this seat are
   `tools/mori-commit-runway.py` (mtime 23:13:27), `tools/fixtures/mori-commit-runway/cases.json`
   (23 → 26 cases, 23:14:25), plus `SKILL.md` and `corpus/knowledge/commit-runway-read-r53.md` (modified
   after my last check, at the end of this seat). The data rev's blobs are untouched (`git cat-file` →
   `80cb1696…` for the tool) and `count-c2.py` is unchanged (sha `5684b69f…`). Every reading in this
   report that quotes the tool is quoted from the **data rev** bytes (sha `80cb1696…`); the
   L1-version re-check is reported separately in §Restoration evidence so the two are not conflated.
   Recorded for the L1: if the in-flight edits are landed, this seat's M02/M16 result still applies to
   them, and the candidate fixture in §Evidence is the one I verified against both versions.
