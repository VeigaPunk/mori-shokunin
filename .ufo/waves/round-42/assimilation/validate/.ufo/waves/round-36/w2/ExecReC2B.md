# ExecReC2B — C2 determinism across fixed seeds (mori round 36, wave 2)

Seat: `MoriR36.ExecReC2B-9` (executor, leaf; no subagent dispatch).
Item attacked: **C2 (measured, operability)** — whether the frozen counter
`.ufo/waves/round-36/count-c2.py` returns a **seed-dependent verdict** at the
landed tip, and whether the real-arm lists (`ids` / `deleted` / `superseded` /
`round_changed`) are stable across seeds while the blind-arm sandbox histories
genuinely differ (drawn at run time).

Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin` (read-only for this seat).
Landed data tip under test: `bf0df77fee4b6ef54a90aea09335c7617f125151`.
Counter frozen at: `evidence/freeze-v2.txt` → `count-c2.py`
sha256 `c7edaacfff029c2055bee6ddda42ff6f5c040dad7fbac81e9d169602edcbac34`.

**VERDICT: PASS** — no seed-dependent verdict found. 488 scored runs across 476
distinct seeds all scored `C2=met` (exit 0) with a **single** distinct real-arm
list line. The one robustness defect found is a **scratch-directory collision
hazard** (§5): it produces `exit 2` (could-not-evaluate, no verdict) and never a
wrong `C2=met`/`C2=unmet`. That is a liveness/ergonomics defect in the counter's
scratch naming, not a soundness defect in the C2 verdict, and it does not touch
the frozen predicate, the counter bytes, or the landed receipt.

---

## 0. Counter identity and predicate binding (checked before any run)

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && sha256sum .ufo/waves/round-36/count-c2.py
c7edaacfff029c2055bee6ddda42ff6f5c040dad7fbac81e9d169602edcbac34  .ufo/waves/round-36/count-c2.py

$ grep count-c2 .ufo/waves/round-36/evidence/freeze-v2.txt
c7edaacfff029c2055bee6ddda42ff6f5c040dad7fbac81e9d169602edcbac34  count-c2.py
```

The counter's bytes match the v2 freeze pin **exactly**, so every receipt below
is a receipt of this claim.

The counter prints `PREDICATE` verbatim. That printed sentence is byte-identical
to `contract.md` and stable across **all three** byte-versions of the contract
that exist in this repo (freeze commit `c1a026cb`, landed tip `bf0df77`, and the
current working tree) — the round's later contract edits changed the C1 table
row and the C1 exploratory declaration, and did **not** touch P-C2:

```
freeze-commit c1a026cb   contract_sha256=dbd3f6d793239a2f  P-C2_sha=81c3080a9f174f77  identical_to_first=True
landed tip bf0df77       contract_sha256=065a17b523b29840  P-C2_sha=81c3080a9f174f77  identical_to_first=True
working tree             contract_sha256=e0426b8ce1ceddc4  P-C2_sha=81c3080a9f174f77  identical_to_first=True
counter PREDICATE sha256: 81c3080a9f174f77
```

`count-c1.py` is likewise unmodified (`86dd3b7ab2d2563b…` == its v2 pin), and its
printed P-C1 sentence is likewise byte-identical to the contract across the
landed tip and the working tree (`0f2c3a28e9f514a1`, len 386).

---

## 1. The two required runs, pasted in full

### Run A — `--seed 42`

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && python3 .ufo/waves/round-36/count-c2.py bf0df77fee4b6ef54a90aea09335c7617f125151 --seed 42
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /tmp/mori-c2-q51aoc6f/mori-sources-appendonly.py
blind arm: 24/24 sandbox histories matched the hidden truth (1.7s; coverage: deletions=23 changed-back=16 superseded=10)
real arm: pass (0.3s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
C2=met
seed=42
EXIT=0
```

### Run B — `--seed 7`

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && python3 .ufo/waves/round-36/count-c2.py bf0df77fee4b6ef54a90aea09335c7617f125151 --seed 7
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /tmp/mori-c2-4hvrxez8/mori-sources-appendonly.py
blind arm: 24/24 sandbox histories matched the hidden truth (1.7s; coverage: deletions=22 changed-back=17 superseded=9)
real arm: pass (0.3s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
C2=met
seed=7
EXIT=0
```

**Both score `C2=met` (exit 0).** The four real-arm lists are byte-identical
across the two seeds. The blind-arm **coverage counters differ**
(`deletions=23 changed-back=16 superseded=10` vs `deletions=22 changed-back=17
superseded=9`), which is the first direct evidence that the seed actually
changes the drawn histories.

---

## 2. Real-arm lists identical across seeds — 488 runs, 476 distinct seeds

Every scored run in this seat's campaign was captured to
`/fast/scratch/hyaku/mori-r36/ExecReC2B/`. Tally over **all** non-concurrent
runs (`seed*.txt sweep_*.txt big_*.txt wide/*.txt final/*.txt rep42_*.txt
replay42_*.txt load/*.txt load40/*.txt`):

```
=== total full counter runs (non-concurrent) ===
488
=== distinct seeds across ALL full runs ===
476
=== all verdicts (non-concurrent) ===
    488 C2=met
=== distinct real-arm tool lines ===
1
```

The single distinct real-arm line, over all 488 runs:

```
appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
```

Seeds exercised include the two required (`42`, `7`), the landed receipt's seed
(`15440749816798970567`), the round's declared seed, edge values, and wide
bands:

```
$ for s in 1 2 3 13 99 12345 999999999 15440749816798970567; do ... done
$ for s in 5 11 17 23 31 101 777 2026 314159 271828 1000003 424242; do ... done
$ for s in $(seq 100 135); do ... done      # 36 seeds
$ for s in $(seq 1000 1119); do ... done    # 120 seeds
$ for s in $(seq 2000 2199); do ... done    # 200 seeds
$ for s in $(seq 5000 5059); do ... done    # 60 seeds, 16-way parallel
$ for s in $(seq 6000 6039); do ... done    # 40 seeds, 40-way parallel
```

Edge seeds:

```
--- seed 0 ---                  --- seed -1 ---                --- seed 9223372036854775807 ---
C2=met   seed=0   rc=0          C2=met   seed=-1   rc=0       C2=met   seed=9223372036854775807   rc=0
```

Every one of these runs also printed `real arm: pass`, `blind arm: 24/24 sandbox
histories matched the hidden truth`, and `tool exit=1`.

### The landed receipt replays exactly

Replaying the receipt's own seed reproduces the landed receipt byte-for-byte
apart from wall-clock timings and the temp tool path:

```
$ diff <(grep -vE '^tool: /tmp' seed_15440749816798970567.txt | sed -E 's/\([0-9.]+s\)//') \
       <(grep -vE '^tool: /tmp' .ufo/waves/round-36/evidence/c2-after.txt | sed -E 's/\([0-9.]+s\)//')
2c2
< blind arm: 24/24 sandbox histories matched the hidden truth (3.1s; coverage: deletions=22 changed-back=17 superseded=10)
---
> blind arm: 24/24 sandbox histories matched the hidden truth (1.6s; coverage: deletions=22 changed-back=17 superseded=10)
```

Only the elapsed-seconds field differs; the coverage counters, the real-arm
`tool`/`oracle` lines, `C2=met` and the seed all match. The landed receipt is
reproducible.

### Same seed → same blind arm (replay determinism)

Eight identical `--seed 42` runs produce one identical output modulo timing:

```
$ for i in $(seq 1 8); do python3 .ufo/waves/round-36/count-c2.py bf0df77... --seed 42 > rep42_$i.txt; done
=== distinct outputs across 8 identical seed-42 runs (tool path stripped) ===
blind arm: 24/24 ... (coverage: deletions=23 changed-back=16 superseded=10)   [x5, differing only in the seconds field]
C2=met
  oracle: appendonly_violations=18 ids=[S041,...] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool:   appendonly_violations=18 ids=[S041,...] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
seed=42
```

A direct diff of two seed-42 runs differs on exactly one line — the ephemeral
temp tool path:

```
$ diff replay42_1.txt replay42_2.txt
2c2
< tool: /tmp/mori-c2-y1k9bpm3/mori-sources-appendonly.py
---
> tool: /tmp/mori-c2-avvg6on4/mori-sources-appendonly.py
```

---

## 3. Blind-arm sandbox histories genuinely differ across seeds

The requirement is that the histories *differ*, not merely that a coverage
counter differs. I replayed the frozen counter's own `build_sandbox` (read-only
import of the frozen module; the lane file was never modified) for seeds 42 and
7 and fingerprinted each of the 24 sandbox repos by its git history, its
`corpus/SOURCES.md` path log, its HEAD tree content, and the counter's hidden
truth:

```
$ python3 sandbox_fingerprint.py 42 7
seed=42
  repo00 commits=7 log=16f78b7956b0e936 pathlog=16f78b7956b0e936 head=d6aab79bb4e61d8d bytes=1694 ids=[S017,S053] del=[S141] sup=[S017,S053] rc=[S017,S141]
  repo01 commits=7 log=285478281010a292 pathlog=285478281010a292 head=40d42586c183da8c bytes=2332 ids=[S068,S153] del=[S275] sup=[S153] rc=[S068,S153,S275]
  ... (24 rows)
seed=7
  repo00 commits=5 log=0dfeaedd16f51455 pathlog=0dfeaedd16f51455 head=9b3c6ba6e0bb9994 bytes=2140 ids=[S299] del=[S025] sup=[S299] rc=[S025,S299]
  repo01 commits=7 log=ccbd4893f2002e62 pathlog=ccbd4893f2002e62 head=d972b95187b4a119 bytes=1504 ids=[] del=[S007,S087,S112] sup=[] rc=[S159]
  ... (24 rows)
COMPARE seed42 vs seed7: identical_git_history=0/24 identical_HEAD_tree=0/24 identical_truth=0/24
```

**0 of 24** sandbox repos share a git history, a HEAD tree, or a hidden truth
between seed 42 and seed 7. The blind arm is not replaying a cached fixture; the
histories are redrawn per seed.

### Same seed → identical histories (control for the above)

```
$ python3 sandbox_fingerprint.py 42 42
COMPARE seed42 vs seed42: identical_git_history=24/24 identical_HEAD_tree=24/24 identical_truth=24/24
```

Content is reproducible for a fixed seed (the git *object ids* differ between
runs only because sandbox commits carry wall-clock author timestamps; the
`head`/`pathlog` content hashes and the hidden truth are stable).

---

## 4. Deep blind-arm sweep — 8 640 sandbox histories, 0 mismatches

Because the blind arm is the only place the seed enters the scoring, I swept it
directly with the frozen counter's own comparison logic
(`build_sandbox` / `run_tool` / `parse_summary` / `same_lists`), in parallel:

```
$ python3 blind_sweep.py 0 120 6
seeds swept: 120 (range 0..119)
sandbox histories evaluated: 2880
history mismatches: 0
seeds with any mismatch: 0
min coverage: delete=17 (seed 36, gate >=12)  changed_back=12 (seed 97, gate >=12)  supersede=6 (gate >=1)
seeds tripping the frozen coverage minimum (would be exit 2, NO VERDICT): 0 []

$ python3 blind_sweep.py 120 360 6
seeds swept: 240 (range 120..359)
sandbox histories evaluated: 5760
history mismatches: 0
seeds with any mismatch: 0
min coverage: delete=18 (seed 165, gate >=12)  changed_back=12 (seed 192, gate >=12)  supersede=6 (gate >=1)
seeds tripping the frozen coverage minimum (would be exit 2, NO VERDICT): 0 []
```

**8 640 sandbox histories across 360 seeds, zero list mismatches, zero exit
codes.** The tool's output matches the counter's hidden truth on every drawn
history.

### Coverage-gate sweep — 700 seeds, no seed can starve the blind arm

The counter aborts with `exit 2` ("blind coverage below the frozen minimum") if
`delete < 12 or changed_back < 12 or supersede < 1`. A seed that starved the
coverage would produce **no verdict at all**, which would itself be a
seed-dependent outcome. Swept over 700 seeds:

```
$ python3 coverage_sweep.py 0 250
seeds tested: 250 (range 0..249)
min coverage delete=17 (gate >=12) changed_back=12 (gate >=12) supersede=6 (gate >=1)
seeds that would trip the frozen coverage minimum (exit 2, NO VERDICT): 0

$ python3 coverage_sweep.py 250 700
seeds tested: 450 (range 250..699)
min coverage delete=15 (gate >=12) changed_back=12 (gate >=12) supersede=6 (gate >=1)
seeds that would trip the frozen coverage minimum (exit 2, NO VERDICT): 0
```

`changed_back` bottoms out at **exactly 12**, the gate value, so I probed its
structure to confirm it can never fall below:

```
$ python3 changed_back_probe.py 0 120
seeds tested: 120
min changed_back coverage over all seeds: 12 (seed 97); gate requires >= 12
odd-index (forced changed-back) sandboxes with EMPTY changed_back: 0
even-index sandboxes that contributed changed_back (extra margin): 437
seeds sitting exactly at the floor of 12: 2 [97, 115]
```

`build_sandbox` forces `want_changed_back = (index % 2 == 1)` — exactly 12 of
the 24 sandboxes are *designed* to carry a changed-back id
(`count-c2.py:385`), and every one of those 12 always did (0 empty odd-index
sandboxes over 120 seeds). The floor of 12 is therefore **structural**, not a
lucky draw: `coverage["changed_back"] >= 12` holds by construction, and the
even-index sandboxes add margin on top. The gate cannot be starved by any seed.

---

## 5. Defect found (robustness, not verdict soundness): scratch-directory collision

**The counter's scratch directory name is a pure function of the seed**, so two
counter processes running the *same* seed concurrently target the *same*
directory and destroy each other's sandboxes:

`count-c2.py:689` — `scratch = os.path.join(SCRATCH_ROOT, "c2-%08x" % rng.randrange(1 << 32))`,
where `rng = random.Random(seed)` (`count-c2.py:658`).

```
$ python3 -c "import random; print('seed 42 -> c2-%08x' % random.Random(42).randrange(1<<32))"
seed 42 -> c2-a3b1799d
```

Four concurrent `--seed 42` runs:

```
$ for i in 1 2 3 4; do (python3 .ufo/waves/round-36/count-c2.py bf0df77... --seed 42 > conc/c_$i.txt 2>&1; echo "exit=$?" >> conc/c_$i.txt) & done; wait
c_1.txt  exit=2 c_2.txt  exit=2 c_3.txt  exit=2 c_4.txt  exit=2
```

with the stderr showing the collision:

```
counter setup error: [Errno 17] File exists: '/fast/scratch/hyaku/mori-r36/c2-a3b1799d/repo00/corpus'
counter setup error: git config user.email counter@example.invalid failed in /fast/scratch/hyaku/mori-r36/c2-a3b1799d/repo00: fatal: cannot change to '/fast/scratch/hyaku/mori-r36/c2-a3b1799d/repo00': No such file or directory
```

Over 18 concurrent same-seed runs the outcome distribution was:

```
=== exit code distribution over 18 concurrent same-seed runs ===
      5 exit=0
     13 exit=2
=== verdict lines present ===
      5 C2=met
=== runs with C2=unmet (false negative)? ===
0
```

**This never produces a wrong verdict.** Every failure is `exit 2`
("could-not-evaluate, no verdict", `count-c2.py:730-733`) — the counter's
documented no-verdict code. **Zero** runs emitted `C2=unmet` (a false negative)
and **zero** emitted `C2=met` with a partial blind arm (a false positive). The
five surviving runs each reported `blind_passed=24`.

The same hazard exists for *different* seeds, because only 32 bits of the
scratch path come from the seed. I searched for and confirmed a colliding pair
— seeds `30642` and `35807` both map to `c2-25da5cc0`:

```
$ python3 -c "import random; [print('seed',s,'-> c2-%08x' % random.Random(s).randrange(1<<32)) for s in (30642,35807)]"
seed 30642 -> c2-25da5cc0
seed 35807 -> c2-25da5cc0
```

Running them concurrently again yields no verdict from either, never a wrong one:

```
--- x_30642.txt ---  counter setup error: git commit -q -m c2 failed ... exit=2   (C2-lines: 0)
--- x_35807.txt ---  counter setup error: [Errno 17] File exists: ... exit=2      (C2-lines: 0)
```

For *scored* runs (no `--seed`, seed drawn from `os.urandom`) the birthday
collision probability over N concurrent runs is small but nonzero, because the
path carries only 32 bits:

```
N= 10 concurrent scored runs -> P(scratch path collision) ~= 1.048e-08
N= 30 concurrent scored runs -> P(scratch path collision) ~= 1.013e-07
N= 60 concurrent scored runs -> P(scratch path collision) ~= 4.121e-07
N=100 concurrent scored runs -> P(scratch path collision) ~= 1.153e-06
N=200 concurrent scored runs -> P(scratch path collision) ~= 4.633e-06
empirical collisions over 200000 random seeds: 5
```

**Assessment.** This is a *liveness/ergonomics* defect in the counter's scratch
naming (the path should be unique per process, e.g. include the PID or the full
64-bit seed). It is **not** a soundness defect: the failure mode is `exit 2`
with no verdict, which is the contract's honest no-verdict code, and the counter
never emits a wrong verdict. It also does not touch the frozen predicate, the
counter bytes, or the landed receipt — the landed receipt was produced by a
sequential run. **It does not change the C2 verdict and is not counted against
the claim.** It is reported because wave-2 seats run this counter concurrently
(e.g. `ExecReC1A`, mutation-tester seats using `--tool` controls), and a seat
that re-runs a *fixed* seed concurrently with another seat on the same seed will
see `exit 2` and could mistake it for a claim failure.

Mitigation available to the parent without touching the frozen counter: give
each concurrent seat its own scratch root. `count-c1.py` already honours an
environment override for exactly this purpose — `SCRATCH = os.environ.get("MORI_R36_SCRATCH", "/fast/scratch/hyaku/mori-r36")`
(`count-c1.py:60`) — but `count-c2.py` hardcodes `SCRATCH_ROOT =
"/fast/scratch/hyaku/mori-r36"` (`count-c2.py:42`) and has **no** such override.
I did not change the counter (frozen, sha-pinned) and did not remediate.

---

## 6. Structural checks: why the real arm *cannot* be seed-dependent

Static analysis of the frozen counter, by function body:

```
$ python3 - <<'EOF'
for fn in ("def real_arm(", "def oracle(", "def parse_summary(", "def same_lists("):
    ... rng/seed/random/time tokens: NONE
EOF
def real_arm           rng/seed/random/time tokens: NONE
def oracle             rng/seed/random/time tokens: NONE
def parse_summary      rng/seed/random/time tokens: NONE
def same_lists         rng/seed/random/time tokens: NONE
```

Every `rng` reference in the counter is confined to sandbox construction
(`make_row`, `Sandbox`, `build_sandbox`) plus the scratch-name draw at
`count-c2.py:689` and the `random.Random(seed)` at `:658`. The real arm and the
oracle contain **no** rng, seed, clock or randomness reference at all, so the
real-arm lists are structurally seed-independent — confirmed empirically by the
single distinct real-arm line over 488 runs.

The landed tool itself has no clock or randomness dependency:

```
$ grep -nE '^import |^from ' tool-landed.py
47:import argparse   48:import os   49:import re   50:import shutil
51:import subprocess   52:import sys   53:import tempfile
```

and its output is byte-stable across repeats:

```
$ for i in 1 2 3; do python3 tool-landed.py 6bd57097 --repo <lane> --round-base f10a320d | md5sum; done
7cabbf3ee586144c7c4785c0ff83b58d  -
7cabbf3ee586144c7c4785c0ff83b58d  -
7cabbf3ee586144c7c4785c0ff83b58d  -
```

The real arm is also **immune to the lane's dirty working tree**, because it
reads pinned revisions only. The lane tree is currently dirty (other wave-2
seats are mid-edit), yet the real-arm result is identical to a clean clone
checked out at the same revision:

```
=== tool against the CLONE (clean tree at 6bd57097) ===
appendonly_violations=18 ids=[S041,...] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
=== tool against the LANE (dirty tree, same revs) ===
appendonly_violations=18 ids=[S041,...] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
```

---

## 7. Adjacent observation (not my lane, no action taken): C1 is currently `unmet` from worktree drift

Not part of the C2 item, but recorded because it will look like a defect to
anyone re-running the counters now. `count-c1.py`'s real arm requires the
lane's **working-tree** `corpus/` to equal the revision under test
(`count-c1.py:583-587` — `git diff --quiet <rev> -- corpus` plus an untracked-file
check; failure prints `real=unmet worktree_corpus_differs_from_rev`). The live
lane's working tree does not match either `bf0df77` or the then-current `HEAD`,
**because concurrent wave-2 seats are editing `corpus/` right now**:

```
$ git status --porcelain corpus/
 M corpus/SOURCES.md
 M corpus/lessons/round-36.md

$ git diff --quiet 6827d6e -- corpus ; echo "rc=$?"
rc=1   # working tree corpus/ differs from the rev under test
```

So a run against the live lane reports `C1=unmet`, identically for every seed —
not a seed effect and not a claim defect; it is the frozen counter correctly
refusing to score a claim whose input surface is mid-edit. Against a **clean
clone checked out at the revision under test**, C1 is `met` and seed-stable:

```
$ python3 .ufo/waves/round-36/count-c1.py bf0df77... --repo <clean clone> --seed 42
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
real_rows=220 oracle_fetched=58 oracle_fresh=49 oracle_drifted=9 oracle_excluded=0 tool_exit=1 tool_rows=220 mismatches=0
C1=met
seed=42

# same clone, seeds 7 and the receipt seed 15440749816798970567:
blind_rows=40 ... mismatches=0 / real_rows=220 oracle_fetched=58 oracle_fresh=49 oracle_drifted=9 oracle_excluded=0 ... mismatches=0 / C1=met
```

C1 is byte-evidence only and admits **no** freshness verdict (contract.md
declares it exploratory; `SKILL.md:859` reads `drifted` as "the copy is not
reproducible from today's body, **never** as a changed source"). I found no
artifact that infers freshness admission from `C1=met`.

---

## 7b. Lane advanced mid-seat — C2 verdict holds at the new HEAD too

While this seat was running, the lane advanced past the data tip:

```
$ git log --oneline -1
6827d6e round-36: close-out — critic corrections (contract history, novelty bound, disposition wording), post-land check records
$ git merge-base --is-ancestor bf0df77... HEAD && echo "bf0df77 IS an ancestor of HEAD"
bf0df77 IS an ancestor of HEAD
```

The counter bytes are **unchanged** by that advance (re-checked after it):

```
$ sha256sum .ufo/waves/round-36/count-c1.py .ufo/waves/round-36/count-c2.py
86dd3b7ab2d2563bbc811e83717b35dfea3d69717dab4d41d454f8b87c8764c0  .ufo/waves/round-36/count-c1.py
c7edaacfff029c2055bee6ddda42ff6f5c040dad7fbac81e9d169602edcbac34  .ufo/waves/round-36/count-c2.py
```

Re-running C2 at the new HEAD reproduces the same verdict and the same
seed-stable behaviour:

```
$ python3 .ufo/waves/round-36/count-c2.py 6827d6e --seed 42
blind arm: 24/24 sandbox histories matched the hidden truth (3.8s; coverage: deletions=23 changed-back=16 superseded=10)
real arm: pass (0.4s)
C2=met
seed=42

$ python3 .ufo/waves/round-36/count-c2.py 6827d6e --seed 7
blind arm: 24/24 sandbox histories matched the hidden truth (2.5s; coverage: deletions=22 changed-back=17 superseded=9)
real arm: pass (0.4s)
C2=met
seed=7
```

So the C2 verdict is stable across **both** revisions and both seeds; the
counter's real arm is pinned to the frozen window (`6bd57097` / `f10a320d`) and
is therefore unaffected by later lane commits.

---

## 8. Routed round-35 repairs re-verified (arithmetic, read-only)

The task lists "SOURCES supersede rows S205–S220 (18 in-place-edited ids
discharged)". At the landed tip, all 18 real-arm ids do carry a superseder:

```
S041->S206  S044->S207  S051->S208  S062->S209  S064->S210  S069->S073
S179->S211  S180->S212  S181->S213  S182->S201  S183->S214  S184->S215
S185->S216  S186->S217  S188->S218  S189->S219  S190->S220  S193->S202
count of the 18 with a superseder at tip: 18
```

S205–S220 are absent at `6bd57097` and present at `bf0df77` (16 rows landed),
and they supply 15 of the 18 superseders; the remaining three (S069, S182,
S193) are superseded by the pre-existing rows S073, S201, S202. The round
append-only gate at the tip is clean:

```
$ python3 tools/mori-sources-appendonly.py bf0df77... --round-base 6bd57097
appendonly_violations=18 ids=[S041,...] deleted=[] superseded=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] round_changed=[]
EXIT=0
```

`round_changed=[]` and exit 0, matching the round's stated gate result. Note
the gate's `superseded` list at the tip (all 18) differs from the counter's
real-arm `superseded` list (`[S069,S182,S193]`) because the counter's real arm
is deliberately pinned to the *older* window (rev `6bd57097`, base `f10a320d`)
per the frozen P-C2 sentence, while the gate above runs at the tip. Both are
correct for their own windows; the difference is the S205–S220 landing, which
happened after the counter's pinned window.

---

## 9. Scope, method and hygiene

- **Files written by this seat: exactly one** — this report at
  `.ufo/waves/round-36/w2/ExecReC2B.md`.
- The lane repo was treated as **read-only**. No `git add/commit/push/fetch/reset`,
  no mutating `jj` command, no lane file was edited. The counter was never
  modified: its sha256 still equals the v2 freeze pin (checked in §0 and again
  after all runs).
- All scratch code and outputs live under
  `/fast/scratch/hyaku/mori-r36/ExecReC2B/` (scratch scripts
  `sandbox_fingerprint.py`, `coverage_sweep.py`, `changed_back_probe.py`,
  `blind_sweep.py`; captured run outputs). `count-c2.py` was *imported*
  read-only by those scripts (`importlib.util.spec_from_file_location`), which
  is what wrote a `__pycache__` entry into the lane; I removed exactly my own
  artifact (`.ufo/waves/round-36/__pycache__/count-c2.cpython-314.pyc`) and left
  the pre-existing `count-c1.cpython-314.pyc` (not mine) alone at that moment.
  That whole `__pycache__` directory was subsequently removed by another party
  during this seat's run (verified gone at the end), so no `__pycache__` residue
  from this seat remains in the lane. The lane index remains clean:
  `git diff --cached --name-only | wc -l` → `0`.
- No remediation, no kills, no config edits, no host-state changes. Detection and
  report only (mori province).
- No tooling was installed or upgraded for this item; the host's `git 2.56.0`
  and `python3 3.14.8` were sufficient. No pacman transaction was run.
- Untracked scratch clone of the lane used for the clean-tree comparison:
  `/fast/scratch/hyaku/mori-r36/ExecReC2B/clone` (read-only use of the lane as a
  git source; no write to the lane).

## 10. Summary table

| check | result | evidence |
|---|---|---|
| `--seed 42` verdict | `C2=met`, exit 0 | §1 Run A |
| `--seed 7` verdict | `C2=met`, exit 0 | §1 Run B |
| real-arm lists identical across seeds | yes — 1 distinct line over 488 runs / 476 seeds | §2 |
| real-arm lists match the landed receipt | yes (modulo elapsed-seconds) | §2 |
| same seed → same output | yes (diff = temp tool path only) | §2 |
| blind histories differ across seeds | yes — 0/24 identical history, HEAD tree, or truth | §3 |
| same seed → same blind histories | yes — 24/24 identical content and truth | §3 |
| blind-arm mismatches over 360 seeds | 0 of 8 640 histories | §4 |
| coverage gate starvable by a seed | no — 700 seeds, 0 trips; floor is structural | §4 |
| seed-dependent verdict found | **none** | §1, §2, §4 |
| defect found | scratch-path collision → `exit 2` (no verdict), never a wrong verdict | §5 |
| C1 freshness admission inferred anywhere | no | §7 |
| verdict stable after the lane advanced to `6827d6e` | yes — `C2=met` at seeds 42 and 7 on the new HEAD | §7b |

**VERDICT: PASS** — no seed-dependent verdict. The C2 verdict is stable at
`C2=met` across 476 distinct seeds; the real-arm lists are byte-identical
everywhere; the blind arm genuinely redraws its 24 sandbox histories per seed
and the tool matched the hidden truth on all 8 640 histories tested. The one
defect found (seed-derived scratch path ⇒ `exit 2` under concurrent same-seed
runs) is a robustness issue in the counter's scratch naming that can only
suppress a verdict, never falsify one, and does not bear on the C2 claim.
