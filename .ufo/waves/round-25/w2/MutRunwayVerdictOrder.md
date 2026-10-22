# MutRunwayVerdictOrder — round 25, wave 2 (falsify)

Seat: `MoriR25.MutRunwayVerdictOrder` (mutation tester). Target: claim **C2** (coverage) —
`tools/mori-job-runway.py`, the verdict and exit mapping (contract `.ufo/waves/round-25/contract.md`
C2 rules 5 and 7, lines 68–89). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.

## Verdict

**The three named mutants are all KILLED. The verdict/exit mapping itself holds; the hole is one
layer out — the exit code the CLI actually returns to a shell is untested.**

| Mutant | Change | frozen 21 | supplementary 18 | Verdict |
|---|---|---|---|---|
| **M1** | `RUNWAY_DEFAULT` decided before the null check on `effective` | FAIL 20/21 — **J14** | PASS 18/18 | **KILLED** (frozen 21) |
| **M2** | swap exit 0/1 on the `CLAMPED` / `AS_CONFIGURED` branches | FAIL 12/21 — **J01, J02, J03, J11, J12, J15, J17, J18, J21** | FAIL 16/18 — **R03, R17** | **KILLED** (both) |
| **M3** | `CLAMPED` when `effective == configured` | FAIL 12/21 — **J01, J02, J03, J11, J12, J15, J17, J18, J21** | FAIL 16/18 — **R03, R17** | **KILLED** (both) |

Three further mutants in the same region (not named in the task) were run to look for survivors:

| Mutant | Change | frozen 21 | supplementary 18 | Verdict |
|---|---|---|---|---|
| **M4** | swap the `RC_OK` / `RC_CLAMPED` constants (`:101-102`) | FAIL 7/21 — **J01, J02, J03, J04, J05, J06, J11, J12, J13, J15, J17, J18, J19, J21** | FAIL 16/18 — **R03, R17** | **KILLED** (both) |
| **M5** | `main()` returns `RC_OK` (`:684-686`): the CLI exit code never reflects the verdict | PASS 21/21 | PASS 18/18 | **SURVIVED** |
| **M6** | `main()` swallows the selftest's return code (`:673-674`): `--selftest` always exits 0 | PASS 21/21 | PASS 18/18 | **SURVIVED** |
| **M7** | the trailing `return VERDICT_UNKNOWN, RC_UNKNOWN` (`:471`) → `VERDICT_DEFAULT, RC_OK` | PASS 21/21 | PASS 18/18 | **SURVIVED — equivalent mutant** (dead code, see below) |
| **M8** | `UNKNOWN` keeps its verdict but exits 0 instead of 2 (`:463-464`) | FAIL 14/21 — **J07, J08, J09, J10, J14, J16, J20** | FAIL 2/18 — **R01, R02, R04–R16, R18** | **KILLED** (both) |
| **M9** | `RUNWAY_DEFAULT` exits 1 instead of 0 (`:469-470`) | FAIL 16/21 — **J04, J05, J06, J13, J19** | PASS 18/18 | **KILLED** (frozen 21) |
| **M10** | `CLAMPED` exits 2 instead of 1 (`:466-467`) | FAIL 15/21 — **J01, J11, J12, J15, J17, J21** | PASS 18/18 | **KILLED** (frozen 21) |
| **M11** | `evaluate()` forces `rc = RC_OK` (`:480`): the exit code is lost before the caller sees it | FAIL 8/21 — **J01, J07, J08, J09, J10, J11, J12, J14, J15, J16, J17, J20, J21** | FAIL 2/18 — **R01, R02, R04–R16, R18** | **KILLED** (both) |

So: **11 mutants, 8 killed, 2 survivors (M5, M6) and 1 equivalent (M7).** The rule-5 mapping
inside `_verdict` (`:458-471`) is fully pinned by the frozen cases; the *plumbing* that carries the
exit code out of the process is not.

**Severity of the survivors: medium (latent, not a live defect).** The landed code is correct; what
is missing is a detector. Nothing in the repo is wrong today.

## Method

* Private clone, never the lane checkout:
  `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin /fast/scratch/hyaku/mori-r25/w2-MutRunwayVerdictOrder`
  (clone HEAD `07a31ae`, tree byte-identical to the lane working copy — verified below).
* Pristine bytes kept at `/fast/scratch/hyaku/mori-r25/mut/pristine.py`,
  sha256 `5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411` (the lane's
  `tools/mori-job-runway.py` hash; the clone and the lane agree).
* One mutant at a time; each mutant is a single exact-string replacement in `_verdict` / `main` /
  the exit constants, applied to the private copy only.
* Bounded behavioural detector (the two the task names), run on pristine, mutated and restored bytes:
  * `python3 -I -B tools/mori-job-runway.py --selftest` → the frozen 21 (`J01`–`J21`)
  * `python3 -I -B tools/mori-job-runway.py --selftest --cases tools/fixtures/mori-job-runway/supplementary-cases.json` → the 18 (`R01`–`R18`)
  * Kill criterion: the detector prints `MORI_JOB_RUNWAY_SELFTEST: FAIL` (and names the failing case id) — i.e. the mutant changed the tool's verdict/exit behaviour on a case the contract froze.
* The tool was never run against a mutated lane copy; the lane `jj` working copy is unchanged
  (`jj --ignore-working-copy status` → "The working copy has no changes.").

### Baseline (pristine bytes, before any mutant)

```
$ cd /fast/scratch/hyaku/mori-r25/w2-MutRunwayVerdictOrder
$ python3 -I -B tools/mori-job-runway.py --selftest
MORI_JOB_RUNWAY_SELFTEST: PASS 21/21          rc=0
$ python3 -I -B tools/mori-job-runway.py --selftest --cases tools/fixtures/mori-job-runway/supplementary-cases.json
MORI_JOB_RUNWAY_SELFTEST: PASS 18/18          rc=0
```

Baseline is green on both detectors, so every kill below is attributable to the mutation, not to a
pre-existing failure.

### Live host run (pristine, read-only) — the behaviour the survivors would distort

```
$ python3 -I -B tools/mori-job-runway.py
{ "schema": "mori-job-runway-v1",
  "config_path": "/home/vgpnk/.omp/agent/config.yml",
  "binary_path": "/home/vgpnk/.local/bin/omp",
  "binary_sha256": "85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4",
  "configured": {"state": "set", "value": 200},
  "clamp": {"state": "found", "value": 100, "sites": 1},
  "setting_default": {"state": "found", "value": 100, "sites": 1},
  "effective": 100,
  "verdict": "RUNWAY_CLAMPED" }
rc=1
```

This host is **clamped** (configured 200, compiled-in clamp 100 → effective 100), so the live
`RUNWAY_CLAMPED` / exit 1 path is the one that matters today.

## The three named mutants, in detail

### M1 — `RUNWAY_DEFAULT` before the null check  →  KILLED (J14)

Mutation in `_verdict` (`:458-471`): the `configured_state_name == "absent"` branch is moved **above**
`if effective is None`. Mutant file sha256 `2a3bc6a147776d1318b6d69f773d9637bf93c5f4738bbf3ad714ddda14f6603a`.

```
frozen21  rc=2   MORI_JOB_RUNWAY_SELFTEST: FAIL 20/21
  CASE J14: verdict: expected 'RUNWAY_UNKNOWN', got 'RUNWAY_DEFAULT'; exit: expected 2, got 0
supp18    rc=0   MORI_JOB_RUNWAY_SELFTEST: PASS 18/18
```

J14 is the case where `async:` is absent *and* the clamp site is absent, so `effective` is null:
the mutant turns a safe abstention (`RUNWAY_UNKNOWN`, exit 2) into a false "the harness default
applies" (`RUNWAY_DEFAULT`, exit 0). The supplementary file has **no** such case (every `R*` case
either carries a clamp or is abstained on for other reasons), so the frozen 21 are what kill this
mutant — worth noting that the supplementary file alone would have let it through.

### M2 — swap exit 0/1  →  KILLED (J01, J02, J03, J11, J12, J15, J17, J18, J21; R03, R17)

Mutation: `return VERDICT_CLAMPED, RC_OK` and `return VERDICT_AS_CONFIGURED, RC_CLAMPED` — the
verdict strings stay correct, the two exit codes are exchanged. Mutant file sha256
`63386b6d99a773decd6b838ee05f0b08ae135c6a75e8199cbe2fc79a4aafa20e`.

```
frozen21  rc=2   MORI_JOB_RUNWAY_SELFTEST: FAIL 12/21
  CASE J01: exit: expected 1, got 0      CASE J11: exit: expected 1, got 0
  CASE J02: exit: expected 0, got 1      CASE J12: exit: expected 1, got 0
  CASE J03: exit: expected 0, got 1      CASE J15: exit: expected 1, got 0
  CASE J17: exit: expected 1, got 0      CASE J21: exit: expected 1, got 0
  CASE J18: exit: expected 0, got 1
supp18    rc=2   MORI_JOB_RUNWAY_SELFTEST: FAIL 16/18
  CASE R03: exit: expected 0, got 1      CASE R17: exit: expected 0, got 1
```

Only the `exit` field differs — the verdicts still read correctly, which is exactly the failure
mode a verdict-only reader would miss. Both detectors kill it; the supplementary file contributes
R03 and R17 (a BOM-prefixed config that is read normally).

### M3 — `CLAMPED` when equal  →  KILLED (J01, J02, J03, J11, J12, J15, J17, J18, J21; R03, R17)

Mutation: `if effective != configured_value:` → `if effective == configured_value:` in
`_verdict` (`:466`), i.e. the clamp verdict is raised exactly when the configured value is
*honoured*. Mutant file sha256 `5f924d04f71d775144c7d8d69c9f1c25c884dd6b7d8a468fa961140eba1adaa3`.

```
frozen21  rc=2   MORI_JOB_RUNWAY_SELFTEST: FAIL 12/21
  CASE J01: verdict: expected 'RUNWAY_CLAMPED', got 'RUNWAY_AS_CONFIGURED'; exit: expected 1, got 0
  CASE J02: verdict: expected 'RUNWAY_AS_CONFIGURED', got 'RUNWAY_CLAMPED'; exit: expected 0, got 1
  ... (J03, J11, J12, J15, J17, J18, J21)
supp18    rc=2   MORI_JOB_RUNWAY_SELFTEST: FAIL 16/18
  CASE R03: verdict: expected 'RUNWAY_AS_CONFIGURED', got 'RUNWAY_CLAMPED'; exit: expected 0, got 1
  CASE R17: verdict: expected 'RUNWAY_AS_CONFIGURED', got 'RUNWAY_CLAMPED'; exit: expected 0, got 1
```

Both verdict **and** exit are inverted for every `configured = set` case, so the frozen 21 kill it
twice over.

## The survivors

### M5 — `main()` returns `RC_OK`: the CLI exit code never reflects the verdict  →  SURVIVED

Mutation at `tools/mori-job-runway.py:684-686`:

```python
    payload, rc = evaluate(config_path, binary_path)
    _emit(payload)
    return RC_OK          # mutant: was `return rc`
```

Mutant file sha256 `3d519986584ce01f65f93643096f48d7aa4fc1cbc9afd9c8d3e9f996f8bd8702`.

Both detectors stay green (`PASS 21/21`, `PASS 18/18`) because the frozen cases call
`evaluate()` in-process and read the `rc` that `evaluate()` returns (`:583-585`), never the code
path that carries the exit code out of the process.

**Which input kills it** — the end-to-end CLI exit code, i.e. a run *without* `--selftest`:

```
$ python3 -I -B tools/mori-job-runway.py --config <clamped.yml> --binary ~/.local/bin/omp
  pristine : rc=1  verdict=RUNWAY_CLAMPED effective=100
  M5 mutant: rc=0  verdict=RUNWAY_CLAMPED effective=100     <-- killed here
$ python3 -I -B tools/mori-job-runway.py --config <clamped.yml> --binary /tmp/not-a-binary
  pristine : rc=2  (RUNWAY_UNKNOWN)
  M5 mutant: rc=0                                     <-- killed here too
```

(`clamped.yml` = `async:` / `  maxJobs: 200`, the same shape as frozen case J01.)

**Does omp's real behaviour make it matter? Yes, mildly.** On this host the live run is
`RUNWAY_CLAMPED` (configured 200 → effective 100), i.e. the live answer is exit 1. The round-25
skill text and the knowledge entry both advertise the exit code as the machine-readable half of
rule 5 (`RUNWAY_CLAMPED` exit 1 / `RUNWAY_AS_CONFIGURED` exit 0 / `RUNWAY_DEFAULT` exit 0 /
`RUNWAY_UNKNOWN` exit 2 — see `.ufo/waves/round-25/w1/SkillErrorPattern.md:114` and
`contract.md:68-73`). Under M5 the JSON still says `RUNWAY_CLAMPED`, so an agent that parses the
JSON is unaffected, but a shell gate that tests `$?` (`if ! python3 -I -B tools/mori-job-runway.py;
then …`) would read a clamped harness as a clean run. Note this is a **coverage** finding about the
detector, not a defect in the landed tool: the landed `main()` returns `rc` and the live run really
does exit 1.

### M6 — `main()` swallows the selftest's return code: `--selftest` always exits 0  →  SURVIVED

Mutation at `tools/mori-job-runway.py:673-674`:

```python
    if ns.selftest:
        _selftest(ns.cases)      # mutant: was `return _selftest(ns.cases)`
        return RC_OK
```

Mutant file sha256 `ea9952689537720dbbcc4f9f87a8539ea7a7dbb457f11d6a45e9b1e9747ff420`.

Both detectors stay green because the frozen 21 and the supplementary 18 all *pass* on the mutated
tool; the mutation only shows up when a case actually fails, and then only in the exit code (the
`FAIL` text is still printed).

**Which input kills it** — a cases file with one deliberately wrong expectation:

```
$ python3 -I -B tools/mori-job-runway.py --selftest --cases <broken-cases.json>
  pristine : rc=2   MORI_JOB_RUNWAY_SELFTEST: FAIL 0/1
                       CASE X01: exit: expected 7, got 0
  M6 mutant: rc=0   MORI_JOB_RUNWAY_SELFTEST: FAIL 0/1     <-- killed here (exit code only)
                       CASE X01: exit: expected 7, got 0
```

**Does omp's real behaviour make it matter? Weakly.** The declared after-value is stated as a
*printed* string (`MORI_JOB_RUNWAY_SELFTEST: PASS 21/21`, `contract.md:87-89`), and a text-reading
gate still sees `FAIL`. A gate that checks only `$?` of `--selftest` would accept a failing
selftest. The landed code is correct (`return _selftest(ns.cases)`), and the failing-selftest path
is exercised today only by hand.

### M7 — the trailing `return VERDICT_UNKNOWN, RC_UNKNOWN` (`:471`) →  **equivalent mutant**, not a coverage gap

This mutant survived because the branch it changes is **unreachable**, so the survivor says nothing
about detector strength:

* `_effective` (`:436-455`) returns a number only when `configured.state` is `"set"` or `"absent"`
  (`:447-452`); for `malformed` / `unreadable` it returns `None`.
* `_verdict` returns at `:463-464` whenever `effective is None`, so a `malformed` / `unreadable`
  configuration never reaches `:471`.
* Brute force over all 4 × 4 × 4 triples of (`configured.state` × `clamp.state` ×
  `setting_default.state`): **zero** combinations reach the trailing return.
  `_verdict(("malformed", None), None)` → `('RUNWAY_UNKNOWN', 2)`.

The trailing `return VERDICT_UNKNOWN, RC_UNKNOWN` is therefore redundant defensive code, not a
missing case. (Contrast M8, which changes the *live* `effective is None` branch at `:463-464` and
is killed by 14 of the 21 frozen cases.)

## Smallest fixes

1. **Cover the exit code that leaves the process (kills M5).** In `_selftest`
   (`tools/mori-job-runway.py:566-608`), after the per-case comparison, assert the *process* exit
   code rather than only the in-process `rc`: e.g. one extra case that runs the tool as a
   subprocess (`sys.executable`, `-I`, `-B`, the script path) with a clamped config and checks
   `returncode == 1`, one with an unreadable binary checking `returncode == 2`, and one
   `as-configured` checking `0`. Smallest form: one subprocess case per exit value (3 cases) in
   the supplementary file (which is *not* counted toward the frozen 21) plus one line asserting
   the mapping. This is a test-only change; the tool's behaviour is already right.
2. **Make the selftest's own exit code honest (kills M6).** Same place: one selftest case whose
   `expect` is deliberately wrong cannot be done inside the tool (it must fail to fail), so the
   smallest fix is a *harness* line: the gate that claims `PASS 21/21, exit 0` should assert
   `$? == 0` **and** the printed `PASS` string together. If the tool itself must carry it, the
   smallest tool change is to keep `return _selftest(ns.cases)` (already correct) and add an
   explicit `assert rc == 0` style guard so the mapping is stated once.
3. **Optional, cheap:** delete the dead trailing `return VERDICT_UNKNOWN, RC_UNKNOWN` at `:471`
   (M7's equivalent region), or keep it as an explicit `raise AssertionError` so the invariant
   "effective is not None ⇒ configured is set or absent" is machine-checked rather than implied.
   Nothing behavioural; low priority.

None of these is a change to the contract or to the tool's semantics: **the landed C2 tool
behaves correctly on every input I probed**, and the rule-5 mapping is pinned by the frozen cases.

## Restoration evidence

Every mutant was reverted immediately after its probe, and the pristine bytes were re-verified by
hash after each run. The tool file in the private clone and in the lane are byte-identical to the
pre-run state.

```
pristine (before all mutants)  5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411  tools/mori-job-runway.py
restored after M1              5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411  (match=True)
restored after M2              5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411  (match=True)
restored after M3              5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411  (match=True)
restored after M4..M11         5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411  (match=True)
restored after the kill demos  5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411  (match=True)
```

(the driver's own `assert sha256(TOOL) == PRISTINE_SHA` after every mutant passed; the final
check, after the last restore, is reproduced verbatim below.)

Final state, re-measured:

```
$ sha256sum /fast/scratch/hyaku/mori-r25/w2-MutRunwayVerdictOrder/tools/mori-job-runway.py
5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && sha256sum tools/mori-job-runway.py tools/fixtures/mori-job-runway/*.json
5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411  tools/mori-job-runway.py
7098b008d614e84c4328af96d15badef700ea84b75a43ba4a375264a01755fb4  tools/fixtures/mori-job-runway/cases.json
8d09756d10a9f501b0fa69599e096ce6ef5f3cd9debda89b5de2bc094679ffd6  tools/fixtures/mori-job-runway/supplementary-cases.json
$ jj --ignore-working-copy status        # lane repo, read-only
The working copy has no changes.
```

The frozen fixture is untouched: `cases.json` sha256 `7098b008d614e84c4328af96d15badef700ea84b75a43ba4a375264a01755fb4`
(git blob `48df844a`, committed at `7634be75` before the tool landed). The supplementary file
sha256 `8d09756d10a9f501b0fa69599e096ce6ef5f3cd9debda89b5de2bc094679ffd6` is unchanged.

**Lane bounds respected:** all code was mutated and executed only in
`/fast/scratch/hyaku/mori-r25/w2-MutRunwayVerdictOrder` (a `git clone --no-hardlinks` of the lane).
No `jj` command was run at the fleet root; no `git add/commit/stash/checkout/switch/reset/pull/push`
was run in the lane; no settings file, `~/.omp` file, fleet script or lane index was touched; `omp`
was never executed (its bytes were read by the tool only, exactly as the tool is designed to do);
no sibling lane was touched. The only file written in the lane is this report.

## Tooling

* `python3` 3.14.8 (system), `git` (system), `jj` (read-only, `--ignore-working-copy`) — all already
  present. **No package was installed or upgraded in this seat** (no pacman / uv / npm / cargo
  transaction was run), so there is nothing to record as a tool change.
* Scratch used: `/fast/scratch/hyaku/mori-r25/w2-MutRunwayVerdictOrder` (private clone, 358 MiB) and
  `/fast/scratch/hyaku/mori-r25/mut/` (driver scripts, pristine copy, per-mutant logs, the two
  killing-input fixtures). **The 358 MiB clone was removed after the run**, as the lane bounds ask;
  the 76 KiB of driver scripts, pristine copy and raw per-mutant logs
  (`results.txt`, `results2.txt`, `kill-demo.txt`) are kept there for re-reading.
