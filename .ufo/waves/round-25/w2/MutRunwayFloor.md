# W2 — MutRunwayFloor: mutation attack on the C2 effective formula

Seat: `MoriR25.MutRunwayFloor` (mutation tester, wave 2, leaf).
Target: `tools/mori-job-runway.py` (claim C2) — the **effective formula** only, i.e. the
`max(1, min(clamp, base))` term and the choice of `base` inside `_effective`
(`tools/mori-job-runway.py:436-455`).
Lane tip under test: `07a31ae8e22514bbc603afa13f2de7c8b2424cca`.
Private copy: `/fast/scratch/hyaku/mori-r25/w2-MutRunwayFloor` (`git clone --no-hardlinks` of the
lane; the tool bytes there are byte-identical to the lane's). The lane checkout was never modified
except for this report file.

## Verdict

**C2's declared after-value: HELD.** All three named mutants of the effective formula are **killed**
by the declared detector `--selftest` (frozen 21). The landed formula is faithful to the shipped
harness: `max(1, min(clamp, base))` reproduces upstream exactly — the clamp number is read from the
binary's bytes and the floor of 1 comes from the manager, not from a guess.

**The supplementary 18: WEAKENED as a formula detector (coverage finding, not a defect).** Three of
the six formula mutants (drop-floor, use-configured, hardcode-100) print `PASS 18/18` — that file
has **almost no power over the numeric branch**: 16 of its 18 cases are abstentions (`effective:
null`), and the two numeric ones (R03, R17) use `maxJobs: 50` under a clamp of 100, a point where
the clamp term and the floor are both invisible.

**One formula mutant survives both declared detectors (coverage finding, not a defect).** Moving the
floor inside the clamp (`min(max(1, base), clamp)`) still prints `PASS 21/21` and `PASS 18/18`. No
shipped case pins the floor when the *clamp itself* is below 1. The mutant is wrong (upstream floors
at 1), but the region is unreachable on omp 18.12.6, whose clamp is 100.

Nothing here is a defect in the landed tool, and nothing in the landed code should change. The
findings are about what the fixtures pin.

## Detectors (bounded, run on pristine, mutated and restored bytes)

* **D-A (declared after-value):** `python3 -I -B tools/mori-job-runway.py --selftest` must print
  exactly `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21` and exit 0; `python3 -I -B tools/mori-job-runway.py
  --selftest --cases tools/fixtures/mori-job-runway/supplementary-cases.json` must print exactly
  `MORI_JOB_RUNWAY_SELFTEST: PASS 18/18` and exit 0.
* **D-C (private probe, mine):** `--selftest --cases probe-cases.json` — two probe cases (P01, P02)
  that cover the two regions neither shipped corpus pins. Used only to name the killing input of a
  survivor; not a claim about the lane's after-value.
* A mutant is **killed** when the detector fails (non-zero exit and/or a `CASE ` failure line); it
  **survived** when the detector still prints the expected `PASS` string and exits 0.

Baseline (pristine bytes, sha256 of `tools/mori-job-runway.py` =
`5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411`, identical in lane and copy):

```
frozen        : MORI_JOB_RUNWAY_SELFTEST: PASS 21/21   exit 0
supplementary : MORI_JOB_RUNWAY_SELFTEST: PASS 18/18   exit 0
private probe : MORI_JOB_RUNWAY_SELFTEST: PASS 2/2     exit 0
```

## The formula under attack

`tools/mori-job-runway.py:436-455` (`_effective`), verbatim from the pristine bytes:

```python
    if clamp_state_name != "found" or clamp_value is None:
        return None
    if configured_state_name == "set":
        base = configured_value
    elif configured_state_name == "absent" and default_state_name == "found":
        base = default_value
    else:
        return None
    if base is None:
        return None
    return max(1, min(clamp_value, base))
```

## Mutants and results

Each mutant was applied alone to the private copy, both declared detectors were run, then the
pristine bytes were restored and re-hashed (restoration column: all `true`, hashes below).

| # | Mutant (one behaviour-bearing point) | Frozen 21 | Supplementary 18 | Private probe | Verdict | Failing case id |
|---|---|---|---|---|---|---|
| M1 | **drop `max(1, ..)`**: `return min(clamp_value, base)` | `FAIL 20/21` rc 2 | `PASS 18/18` rc 0 | `FAIL 1/2` rc 2 | **killed** (frozen + probe) | J12 (frozen), P01 (probe) |
| M2 | **use configured instead of min**: `return max(1, configured_value if configured_state_name == "set" else min(clamp_value, base))` | `FAIL 16/21` rc 2 | `PASS 18/18` rc 0 | `FAIL 1/2` rc 2 | **killed** (frozen + probe) | J01, J11, J15, J17, J21 (frozen), P01 (probe) |
| M3a | **use default when configured is set (strict)**: `base = default_value` unconditionally | `FAIL 17/21` rc 2 | `FAIL 16/18` rc 2 | `FAIL 1/2` rc 2 | **killed** (frozen + supplementary + probe) | J02, J12, J18, J21 (frozen), R03, R17 (supp.), P02 (probe) |
| M3b | **use default when configured is set (lenient)**: `base = default_value if default_state_name == "found" else configured_value` | `FAIL 18/21` rc 2 | `FAIL 16/18` rc 2 | `FAIL 1/2` rc 2 | **killed** (frozen + supplementary + probe) | J02, J12, J18 (frozen), R03, R17 (supp.), P02 (probe) |
| M4 | **floor moved inside the clamp**: `return min(max(1, base), clamp_value)` | `PASS 21/21` rc 0 | `PASS 18/18` rc 0 | `FAIL 1/2` rc 2 | **survived both declared detectors** | none (P01 kills it) |
| M5 | **clamp additionally capped at 100**: `return max(1, min(clamp_value, base, 100))` | `FAIL 20/21` rc 2 | `PASS 18/18` rc 0 | `FAIL 1/2` rc 2 | **killed** (frozen + probe) | J18 (frozen), P02 (probe) |

M1–M3 are the three points the assignment named. M3 was probed in two readings of "use default when
configured is set" (strict = the default always wins; lenient = the default wins whenever it is
found). M4 and M5 are two further plausible defects of the same formula, added so that the
survivor question has an answer.

### Actual outputs (verbatim)

```
=== M1-drop-floor ===
frozen rc=2 MORI_JOB_RUNWAY_SELFTEST: FAIL 20/21
  FROZEN-CASE J12: verdict: expected 'RUNWAY_CLAMPED', got 'RUNWAY_AS_CONFIGURED'; exit: expected 1, got 0; effective: expected 1, got 0
supp   rc=0 MORI_JOB_RUNWAY_SELFTEST: PASS 18/18

=== M2-use-configured ===
frozen rc=2 MORI_JOB_RUNWAY_SELFTEST: FAIL 16/21
  FROZEN-CASE J01: verdict: expected 'RUNWAY_CLAMPED', got 'RUNWAY_AS_CONFIGURED'; exit: expected 1, got 0; effective: expected 100, got 200
  FROZEN-CASE J11: verdict: expected 'RUNWAY_CLAMPED', got 'RUNWAY_AS_CONFIGURED'; exit: expected 1, got 0; effective: expected 100, got 200
  FROZEN-CASE J15: verdict: expected 'RUNWAY_CLAMPED', got 'RUNWAY_AS_CONFIGURED'; exit: expected 1, got 0; effective: expected 100, got 200
  FROZEN-CASE J17: verdict: expected 'RUNWAY_CLAMPED', got 'RUNWAY_AS_CONFIGURED'; exit: expected 1, got 0; effective: expected 100, got 200
  FROZEN-CASE J21: verdict: expected 'RUNWAY_CLAMPED', got 'RUNWAY_AS_CONFIGURED'; exit: expected 1, got 0; effective: expected 100, got 200
supp   rc=0 MORI_JOB_RUNWAY_SELFTEST: PASS 18/18

=== M3a-default-when-set-strict ===
frozen rc=2 MORI_JOB_RUNWAY_SELFTEST: FAIL 17/21
  FROZEN-CASE J02: verdict: expected 'RUNWAY_AS_CONFIGURED', got 'RUNWAY_CLAMPED'; exit: expected 0, got 1; effective: expected 50, got 100
  FROZEN-CASE J12: effective: expected 1, got 100
  FROZEN-CASE J18: verdict: expected 'RUNWAY_AS_CONFIGURED', got 'RUNWAY_CLAMPED'; exit: expected 0, got 1; effective: expected 250, got 100
  FROZEN-CASE J21: verdict: expected 'RUNWAY_CLAMPED', got 'RUNWAY_UNKNOWN'; exit: expected 1, got 2; effective: expected 100, got None
supp   rc=2 MORI_JOB_RUNWAY_SELFTEST: FAIL 16/18
  SUPP-CASE R03: verdict: expected 'RUNWAY_AS_CONFIGURED', got 'RUNWAY_CLAMPED'; exit: expected 0, got 1; effective: expected 50, got 100
  SUPP-CASE R17: verdict: expected 'RUNWAY_AS_CONFIGURED', got 'RUNWAY_CLAMPED'; exit: expected 0, got 1; effective: expected 50, got 100

=== M3b-default-when-set-lenient ===
frozen rc=2 MORI_JOB_RUNWAY_SELFTEST: FAIL 18/21
  FROZEN-CASE J02: verdict: expected 'RUNWAY_AS_CONFIGURED', got 'RUNWAY_CLAMPED'; exit: expected 0, got 1; effective: expected 50, got 100
  FROZEN-CASE J12: effective: expected 1, got 100
  FROZEN-CASE J18: verdict: expected 'RUNWAY_AS_CONFIGURED', got 'RUNWAY_CLAMPED'; exit: expected 0, got 1; effective: expected 250, got 100
supp   rc=2 MORI_JOB_RUNWAY_SELFTEST: FAIL 16/18
  SUPP-CASE R03: ... effective: expected 50, got 100
  SUPP-CASE R17: ... effective: expected 50, got 100

=== M4-floor-after-min ===
frozen rc=0 MORI_JOB_RUNWAY_SELFTEST: PASS 21/21
supp   rc=0 MORI_JOB_RUNWAY_SELFTEST: PASS 18/18

=== M5-hardcode-100 ===
frozen rc=2 MORI_JOB_RUNWAY_SELFTEST: FAIL 20/21
  FROZEN-CASE J18: verdict: expected 'RUNWAY_AS_CONFIGURED', got 'RUNWAY_CLAMPED'; exit: expected 0, got 1; effective: expected 250, got 100
supp   rc=0 MORI_JOB_RUNWAY_SELFTEST: PASS 18/18
```

Probe run (`--selftest --cases probe-cases.json`; pristine passes 2/2):

```
PRISTINE probe: rc=0 MORI_JOB_RUNWAY_SELFTEST: PASS 2/2
M1-drop-floor                  probe: KILLED   rc=2 MORI_JOB_RUNWAY_SELFTEST: FAIL 1/2
     CASE P01: effective: expected 1, got 0
M2-use-configured              probe: KILLED   rc=2 MORI_JOB_RUNWAY_SELFTEST: FAIL 1/2
     CASE P01: verdict: expected 'RUNWAY_CLAMPED', got 'RUNWAY_AS_CONFIGURED'; exit: expected 1, got 0; effective: expected 1, got 5
M3a-default-when-set-strict    probe: KILLED   rc=2 MORI_JOB_RUNWAY_SELFTEST: FAIL 1/2
     CASE P02: verdict: expected 'RUNWAY_AS_CONFIGURED', got 'RUNWAY_CLAMPED'; exit: expected 0, got 1; effective: expected 250, got 100
M3b-default-when-set-lenient   probe: KILLED   rc=2 MORI_JOB_RUNWAY_SELFTEST: FAIL 1/2
     CASE P02: verdict: expected 'RUNWAY_AS_CONFIGURED', got 'RUNWAY_CLAMPED'; exit: expected 0, got 1; effective: expected 250, got 100
M4-floor-after-min             probe: KILLED   rc=2 MORI_JOB_RUNWAY_SELFTEST: FAIL 1/2
     CASE P01: effective: expected 1, got 0
M5-hardcode-100                probe: KILLED   rc=2 MORI_JOB_RUNWAY_SELFTEST: FAIL 1/2
     CASE P02: verdict: expected 'RUNWAY_AS_CONFIGURED', got 'RUNWAY_CLAMPED'; exit: expected 0, got 1; effective: expected 250, got 100
PRISTINE re-check: rc=0 MORI_JOB_RUNWAY_SELFTEST: PASS 2/2 ; tool sha256 5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411
```

## Ground truth the formula is measured against (re-opened this round, read-only)

* **Installed binary** `/home/vgpnk/.local/bin/omp`, 256,702,432 bytes, sha256
  `85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4`: exactly **one** clamp site,
  at byte 164406766 — `maxRunningJobs: () => Math.min(100, XPe.get(R))` — and exactly one setting
  definition, at byte 155231590 — `id: "async.maxJobs", … default: 100`. The binary was read as
  bytes; `omp` was never executed.
* **Upstream oh-my-pi 18.12.6** (commit `45c35e40c46166dc726ccc52f5d27f40f2449f99`), re-fetched
  this round as raw files in the private copy:
  * `packages/coding-agent/src/sdk.ts:2284` — `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings))`
    (sha256 `c0228addd4cfe93cfd370c7248e9db29743f0fa802aea0e1d1adf4994dbe6957`).
  * `packages/coding-agent/src/async/job-manager.ts:331-334` — `get #maxRunningJobs()` returns
    `Math.max(1, Math.floor(value ?? DEFAULT_MAX_RUNNING_JOBS))` (sha256
    `0f37afaaa822ef1de845b8eb21473a70210176ff61e2dcff5925f85ec0e544e7`).
  * `packages/coding-agent/src/config/registry.ts:639-646` — a configured value wins; the schema
    `default` is used **only** when the raw value is `undefined` (the setting is not configured) or
    invalid. `accepts()` for a `number` setting is `typeof value === "number" && Number.isFinite(value)`
    (`registry.ts:613-614`), so `0` is a *valid* configured value.
  Composed, the shipped effective cap is `max(1, floor(min(clamp, base)))` with `base` = the
  configured value, else the schema default. The tool's `max(1, min(clamp, base))` is the same
  function on the values it can represent: the config grammar only accepts integers
  (`INTEGER_RE = ^[+-]?[0-9]+$`, `tools/mori-job-runway.py:122`), so upstream's `Math.floor` is a
  no-op on them.
* **This host** (`~/.omp/agent/config.yml`, read 2026-10-22): a column-0 `async:` block with
  `maxJobs: 200`. Live run of the pristine tool in the private copy:
  `configured {set 200}`, `clamp {found 100, sites 1}`, `setting_default {found 100, sites 1}`,
  `effective 100`, `verdict RUNWAY_CLAMPED`, exit 1.

## Survivors: the killing input, and whether omp's real behaviour makes it matter

### M4 — floor moved inside the clamp (`min(max(1, base), clamp)`) — survived **both** declared detectors

* **Killing input:** `probe-cases.json` **P01** — a binary whose clamp site is
  `maxRunningJobs: () => Math.min(0, XPe.get(R))` with the config `async:\n  maxJobs: 5\n`.
  Pristine: `effective = max(1, min(0, 5)) = 1` → `RUNWAY_CLAMPED`, exit 1. M4: `min(max(1, 5), 0) = 0`
  → `FAIL 1/2, CASE P01: effective: expected 1, got 0`. (P01 is my private probe; it is not in the
  lane and I did not add it there — the lane is read-only for this seat.)
* **Does omp's real behaviour make it matter? Only for a build whose clamp is below 1.** Upstream's
  manager floors at 1 (`Math.max(1, Math.floor(value ?? 15))`), so a hypothetical binary clamping at
  0 would still run 1 job and the tool's `effective` must be 1; M4 would report 0, and a report of 0
  would read as "no runway at all". On omp 18.12.6 the clamp is 100, so the region is unreachable:
  the tool and the mutant agree on every input this binary can produce. Severity: **low** (coverage
  gap; no live consequence today).

### M1 — `max(1, ..)` dropped — survived the **supplementary** detector

* **Killing input:** the shipped **J12** — config `async:\n  maxJobs: 0\n` under a clamp of 100.
  Pristine: `effective = max(1, min(100, 0)) = 1` → `RUNWAY_CLAMPED`, exit 1. M1: `min(100, 0) = 0`
  → `FAIL 20/21, CASE J12: … effective: expected 1, got 0`. P01 kills it too.
* **Does omp's real behaviour make it matter? Yes.** `0` is a valid configured value upstream
  (`registry.ts:613-614` accepts any finite number; `registry.ts:642` returns it as-is), so the
  session's real cap is `Math.min(100, 0) = 0` → `Math.max(1, Math.floor(0)) = 1`. The floor is a
  real property of the harness, not an invention of the tool, and a tool that reported 0 would be
  reporting a cap that never exists. Severity: **medium** (a `maxJobs: 0` config is unusual but
  legal, and the number is the machine-readable half of the claim).

### M2 — configured value used instead of the clamp — survived the **supplementary** detector

* **Killing input:** the shipped **J01** — config `async:\n  maxJobs: 200\n` under a clamp of 100.
  Pristine: `effective = 100` → `RUNWAY_CLAMPED`, exit 1. M2: `200` → `FAIL 16/21, CASE J01: …
  effective: expected 100, got 200` (also J11, J15, J17, J21). P01 kills it too.
* **Does omp's real behaviour make it matter? Yes — this is the most consequential mutant of the
  six.** On this host the config says `maxJobs: 200` and the binary clamps at 100
  (`sdk.ts:2284`); the live tool reports `effective 100`, `RUNWAY_CLAMPED`, exit 1. M2 would report
  `effective 200`, `RUNWAY_AS_CONFIGURED`, exit 0 — i.e. it would tell the operator that the file's
  200 is in force and hide the very clamp the claim exists to document, and the number in a real
  refusal (`Background job limit reached (100)`) would contradict the tool's own output. Severity:
  **high** for the claim's substance; the frozen corpus catches it, so nothing needs to change in
  the tool.

### M5 — clamp additionally capped at 100 — survived the **supplementary** detector

* **Killing input:** the shipped **J18** — a binary whose clamp site is
  `maxRunningJobs: () => Math.min(300, XPe.get(R))` with the config `async:\n  maxJobs: 250\n`.
  Pristine: `effective = 250` → `RUNWAY_AS_CONFIGURED`, exit 0. M5: `100` → `FAIL 20/21, CASE J18: …
  effective: expected 250, got 100`. P02 kills it too.
* **Does omp's real behaviour make it matter? Not today, but it will.** The clamp number is a
  property of the binary under test, and the contract's rule 2 says it is read from the bytes; on
  18.12.6 the clamp *is* 100, so hardcoding 100 is accidentally right. A future release with a
  different clamp would be mis-reported by M5 and correctly reported by the tool. Severity: **low**
  today, **medium** for the claim's freshness ("a different build may clamp elsewhere").

### M3a / M3b — default used when the setting is configured — killed by both corpora

Both readings are killed by the frozen 21 **and** by the supplementary 18 (R03, R17), so they are not
survivors. Recorded for completeness because they are the strongest evidence that the corpora pin
the *base* choice and not only the arithmetic: with `maxJobs: 50` configured, upstream uses the
configured 50 (`registry.ts:642` — the default is the fallback for an unset setting), so the real cap
is 50; M3a/M3b would report 100. Note the one case that separates the two readings is **J21**
(ambiguous default + configured value): it kills the strict reading (which nulls the result) and
lets the lenient reading pass. Nothing in the corpora says *why* — the difference is only visible
through the mutant.

## Coverage findings (fixtures, not the tool)

1. **The supplementary 18 have almost no power over the effective formula.** M1, M2 and M5 all print
   `PASS 18/18`. 16 of the 18 cases are abstentions (`effective: null`), and the two numeric ones
   (R03, R17) sit at `maxJobs: 50` under a clamp of 100 — a point where the clamp term and the
   floor cannot show. The supplementary file's declared subject (YAML forms the line grammar cannot
   read) is not the formula's; it is a *co-evolved* corpus, not a second witness for the formula.
   Severity: **low** for the claim (the frozen 21 carries the load), **medium** for anyone who
   treats a green supplementary run as evidence about the numbers.
2. **Nothing pins the floor when the clamp itself is below 1** — M4 survives both corpora. The
   frozen 21 pins the floor only against `base` (J12, `maxJobs: 0` under a clamp of 100).
   Severity: **low** (unreachable on 18.12.6).
3. **The clamp term is pinned only by the frozen 21** (J01/J11/J15/J17/J21 for M2, J18 for M5).
   Any future corpus that replaces the frozen file must keep a case where `configured > clamp` and
   a case where `clamp > 100`, or the formula regresses unnoticed.

## Smallest fixes (fixtures only; not applied — the lane is read-only for this seat)

Nothing in `tools/mori-job-runway.py` needs to change. Two case additions would close the two gaps
above; each is one case in the existing schema, and neither changes the frozen blob (which the
contract pins at `48df844a`):

* **P01** (kills M4): binary with `Math.min(0, XPe.get(R))`, config `async:\n  maxJobs: 5\n`,
  `expect {verdict: RUNWAY_CLAMPED, exit: 1, effective: 1}`.
* **P02** (kills M5): binary with `Math.min(300, XPe.get(R))`, config `async:\n  maxJobs: 250\n`,
  `expect {verdict: RUNWAY_AS_CONFIGURED, exit: 0, effective: 250}` — note that a case with a clamp
  above 100 also has to keep the *setting default* at 100 so that it tests the clamp and not the
  default.

If the lane prefers not to grow the frozen corpus, the same two cases can be added as a third
cases file loaded with `--cases` (the amendment-A2 mechanism already in use), which keeps the
declared after-value `PASS 21/21` untouched.

## Restoration evidence

* Pristine tool bytes: `5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411`
  (identical in the lane and in the private copy before, during and after the session).
* Per-mutant hashes (pristine → mutated → restored), from `mutation-results.json` in the private
  copy:

| mutant | pristine | mutated | restored |
|---|---|---|---|
| M1-drop-floor | `5d90d7d43df0` | `814427298ae1` | `5d90d7d43df0` |
| M2-use-configured | `5d90d7d43df0` | `94243991931f` | `5d90d7d43df0` |
| M3a-default-when-set-strict | `5d90d7d43df0` | `46b935186a52` | `5d90d7d43df0` |
| M3b-default-when-set-lenient | `5d90d7d43df0` | `6f91701804b2` | `5d90d7d43df0` |
| M4-floor-after-min | `5d90d7d43df0` | `758614c023ef` | `5d90d7d43df0` |
| M5-hardcode-100 | `5d90d7d43df0` | `693bd2865072` | `5d90d7d43df0` |

* Final check after the last mutant and the probe matrix: the tool file in the private copy hashes
  `5d90d7d43df0…` and `python3 -I -B tools/mori-job-runway.py --selftest` prints
  `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21`.
* Lane untouched: the lane's `tools/mori-job-runway.py` still hashes `5d90d7d43df0…`; the only file
  this seat wrote in the lane is this report. `git status --porcelain` in the lane shows no
  modification under `tools/`.
* No `jj` command was run anywhere; no git write (`add`/`commit`/`checkout`/`stash`/`reset`/`push`)
  was run in the lane or in the fleet root; `omp` was never executed — the tool only read the
  binary's bytes.
* Tooling: **no package was installed or upgraded** for this seat. The mutation harness is plain
  Python 3 standard library (`python3 -I -B`, version 3.14.8): `mutate_runway.py`, `probe_matrix.py`,
  `probe-cases.json`, `mutation-results.json`, `mutation-log.txt`, `probe-log.txt`, plus the
  re-fetched upstream files under `upstream/`. The private copy lives at
  `/fast/scratch/hyaku/mori-r25/w2-MutRunwayFloor` and can be removed with
  `rm -rf /fast/scratch/hyaku/mori-r25/w2-MutRunwayFloor`.

## Summary table

| Mutant | Frozen 21 (declared) | Supplementary 18 | Private probe | Verdict | Failing case id |
|---|---|---|---|---|---|
| M1 drop `max(1, ..)` | killed (`FAIL 20/21`) | survived (`PASS 18/18`) | killed | **killed** | J12 (frozen), P01 |
| M2 use configured instead of min | killed (`FAIL 16/21`) | survived (`PASS 18/18`) | killed | **killed** | J01, J11, J15, J17, J21 (frozen), P01 |
| M3a use default when configured is set (strict) | killed (`FAIL 17/21`) | killed (`FAIL 16/18`) | killed | **killed** | J02, J12, J18, J21 / R03, R17 / P02 |
| M3b use default when configured is set (lenient) | killed (`FAIL 18/21`) | killed (`FAIL 16/18`) | killed | **killed** | J02, J12, J18 / R03, R17 / P02 |
| M4 floor inside the clamp | survived (`PASS 21/21`) | survived (`PASS 18/18`) | killed | **survivor of both declared detectors** | none (P01 kills it) |
| M5 clamp additionally capped at 100 | killed (`FAIL 20/21`) | survived (`PASS 18/18`) | killed | **killed** | J18 (frozen), P02 |
