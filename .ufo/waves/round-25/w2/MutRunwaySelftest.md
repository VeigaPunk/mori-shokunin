# W2 — MutRunwaySelftest: mutation attack on the C2 selftest harness

Seat: `MoriR25.MutRunwaySelftest` (mutation tester, wave 2, leaf).
Target: `tools/mori-job-runway.py` (claim C2) — the `--selftest` harness only.
Lane tip under test: `07a31ae8e22514bbc603afa13f2de7c8b2424cca`.
Private copy: `/fast/scratch/hyaku/mori-r25/w2-MutRunwaySelftest` (`git clone --no-hardlinks` of the
lane). The lane checkout was never modified except for this report file.

## Verdict

**C2's declared after-value: HELD.** The tool at the landed tip really prints
`MORI_JOB_RUNWAY_SELFTEST: PASS 21/21` (exit 0) over the frozen 21 cases and `PASS 18/18` (exit 0)
over the supplementary 18, and every one of the 39 expected values matches the tool's observed
output. The corpus is also strong against tool-level defects: a tool mutant that halves `effective`
is killed by 13 frozen cases and 2 supplementary cases.

**The selftest harness itself: WEAKENED (coverage finding, not a defect in the tool).** Four of the
six harness mutants I planted **survived both corpora** — a harness that asserts one field instead of
five, a harness with no empty-expect guard, a harness with no zero-case guard, and a harness that no
longer requires the `exit` field in a case's expectation all still print `PASS 21/21`. Two further
mutants (skipping the null-config cases) survive any detector that only looks at the **exit code**.
The after-value string `PASS 21/21` therefore does **not** by itself show that the harness compares
what it claims to compare.

Nothing here breaks the tool's live behaviour, and nothing in the landed code is wrong. The finding
is that the claim's evidence is self-referential: the selftest is its own witness, and no frozen or
supplementary case can detect a weakened selftest.

## Detectors (bounded, run on pristine, mutated and restored bytes)

* **D-A (declared after-value):** `python3 -I -B tools/mori-job-runway.py --selftest` must print
  exactly `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21` and exit 0; `python3 -I -B tools/mori-job-runway.py
  --selftest --cases tools/fixtures/mori-job-runway/supplementary-cases.json` must print exactly
  `MORI_JOB_RUNWAY_SELFTEST: PASS 18/18` and exit 0.
* **D-B (exit-code only):** the weaker gate a shell chain (`&&`, `set -e`) or a CI step would apply —
  exit status 0 and no `CASE ` failure lines. Reported separately, because it is the gate a script
  author is most likely to write.
* A mutant is **killed** when D-A (or D-B) fails; **survived** when both pass.

Baseline (pristine bytes, sha256 of `tools/mori-job-runway.py` =
`5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411`):

```
frozen        : MORI_JOB_RUNWAY_SELFTEST: PASS 21/21   exit 0
supplementary : MORI_JOB_RUNWAY_SELFTEST: PASS 18/18   exit 0
```

## Mutants and results

Each mutant was applied alone, run against both corpora, then the pristine bytes were restored and
the hash re-checked (restoration column: all `true`).

| # | Mutant (one behaviour-bearing point in the harness) | Frozen result | Supplementary result | D-A | D-B | Failing case id |
|---|---|---|---|---|---|---|
| M1 | `_selftest` compares only the `verdict` field: `problems = _compare({"verdict": expect.get("verdict")}, observed, "")` | `PASS 21/21` rc 0 | `PASS 18/18` rc 0 | **survived** | **survived** | none |
| M2a | skip cases whose `config` is null (`if case.get("config") is None: continue`), total unchanged | `PASS 19/21` rc 0 | `PASS 18/18` rc 0 | **killed** (count) | **survived** | none (no `CASE ` line; exit still 0) |
| M2b | same skip, plus `total` recounted over the non-skipped cases | `PASS 19/19` rc 0 | `PASS 18/18` rc 0 | **killed** (count) | **survived** | none (exit still 0) |
| M3 | empty-expect guard removed: `if not expect.get("verdict") or "exit" not in expect:` → the compare runs unguarded | `PASS 21/21` rc 0 | `PASS 18/18` rc 0 | **survived** | **survived** | none |
| M4 | zero-case guard removed: `if total == 0: failures.append("?: no cases loaded")` deleted | `PASS 21/21` rc 0 | `PASS 18/18` rc 0 | **survived** | **survived** | none |
| M5 | expect-guard relaxed to `if not expect.get("verdict"):` (the `exit` requirement is dropped) | `PASS 21/21` rc 0 | `PASS 18/18` rc 0 | **survived** | **survived** | none |

M2a/M2b skip exactly **J05** ("config file missing") and **J14** ("config missing and no setting
default in the binary") — the two frozen cases that cover the `configured: absent` branch.

## Killing inputs for each survivor

Each probe is a cases file that the *pristine* harness fails (naming the case ids) and the *mutant*
passes. The probe files live in the private copy (`probe-m1-cases.json`, `probe-m3-cases.json`,
`probe-m4-cases.json`, `probe-m5-cases.json`).

### M1 (compare only verdict) — survives

Killing input: `probe-m1-cases.json` — the frozen 21 cases with three expectations made wrong while
the **verdict stays correct** (J01 `effective: 100→42`, J01 `clamp.sites: 1→2`, J01
`configured.value: 200→999`; J02 `exit: 0→1`; J05 `configured.value: null→7`).

```
pristine : MORI_JOB_RUNWAY_SELFTEST: FAIL 18/21  rc=2
            CASE J01: configured.value: expected 999, got 200; clamp.sites: expected 2, got 1; effective: expected 42, got 100
            CASE J02: exit: expected 1, got 0
            CASE J05: configured.value: expected 7, got None
mutant M1: MORI_JOB_RUNWAY_SELFTEST: PASS 21/21  rc=0
```

**Does omp's real behaviour make it matter? Yes.** On this host the tool reports
`configured 200`, `clamp 100`, `effective 100`, `RUNWAY_CLAMPED`, exit 1 (live run of the clone,
binary sha256 `85d9daf3…`): the number omp will actually honour is the *effective* one, and the exit
code is the contract's machine-readable part (rule 5). A comparator that only reads `verdict` cannot
see a wrong `effective` (e.g. `50` where omp allows `100` — same `RUNWAY_CLAMPED` verdict) nor a
wrong `exit` (e.g. `RUNWAY_CLAMPED` with exit 0). The corpus *does* kill such tool defects — a tool
mutant that halves `effective` fails 13 frozen cases (`CASE J01 … CASE J21`, `FAIL 8/21`) and 2
supplementary cases (`CASE R03`, `CASE R17`) — so the coverage exists at the case level and is thrown
away at the comparator level. Severity: **medium** (harness blind to the fields that carry the
numbers; the landed tool itself is correct).

### M3 (no empty-expect guard) — survives

Killing input: `probe-m3-cases.json` — J07's `expect` set to `{}`, J08's `expect` key removed.

```
pristine : MORI_JOB_RUNWAY_SELFTEST: FAIL 19/21  rc=2
            CASE J07: expect must name at least verdict and exit
            CASE J08: expect must name at least verdict and exit
mutant M3: MORI_JOB_RUNWAY_SELFTEST: PASS 21/21  rc=0
```

**Does omp's real behaviour make it matter? Weakly.** The guard protects the harness against a cases
file that asserts nothing; it does not touch the tool's live output. The mitigating fact is that the
frozen cases file is pinned (`48df844a` at `7634be75`, per contract A1), so a future edit that
empties an `expect` block changes the blob and is visible in review. Severity: **low-medium**
(self-validation gap in the harness, not in the tool).

### M4 (no zero-case guard) — survives

Killing input: `probe-m4-cases.json` — `{"schema": "mori-job-runway-cases-v1", "cases": []}`.

```
pristine : MORI_JOB_RUNWAY_SELFTEST: FAIL 0/0  rc=2
            CASE ?: no cases loaded
mutant M4: MORI_JOB_RUNWAY_SELFTEST: PASS 0/0  rc=0
```

**Does omp's real behaviour make it matter? Yes, for any consumer of `--cases`.** The contract's own
amendment A2 introduces a second cases file loaded with `--cases PATH`; a mistyped path, a truncated
file, or a JSON without a `cases` key then yields `PASS 0/0` with **exit 0** — a green selftest that
tested nothing, and a green exit code for a gate that checks status. This is the most plausible
accident of the four survivors. Severity: **medium** (no effect on the declared after-value, which
uses the default frozen path; real effect on any script that passes `--cases`).

### M5 (`exit` no longer required in an expectation) — survives

Killing input: `probe-m5-cases.json` — J09 and J10 keep every other expected field but drop `exit`.

```
pristine : MORI_JOB_RUNWAY_SELFTEST: FAIL 19/21  rc=2
            CASE J09: expect must name at least verdict and exit
            CASE J10: expect must name at least verdict and exit
mutant M5: MORI_JOB_RUNWAY_SELFTEST: PASS 21/21  rc=0
```

**Does omp's real behaviour make it matter? Weakly.** Rule 5 makes the exit code part of the tool's
contract (`0` as-configured/default, `1` clamped, `2` unknown/usage). With M5 a case may silently
stop asserting its exit code while every other field is still checked. Severity: **low-medium**.

### M2 (skip null-config cases) — killed by the count, survived by the exit code

M2a/M2b are the only mutants that change the printed count, so D-A kills them and D-B does not:
`PASS 19/21` (M2a) and `PASS 19/19` (M2b) both exit **0**, so a gate that only checks the exit
status stays green while **2 of the 21 frozen cases never ran**.

The dropped coverage is exactly J05/J14 (the `configured: absent` branch). Probe P5 shows it: with a
tool defect injected (a missing config file reported as `configured: set 7` instead of `absent`) —

```
pristine+defect : MORI_JOB_RUNWAY_SELFTEST: FAIL 19/21  rc=2
                  CASE J05: verdict: expected 'RUNWAY_DEFAULT', got 'RUNWAY_AS_CONFIGURED'; configured.state: expected 'absent', got 'set'; configured.value: expected None, got 7; effective: expected 100, got 7
                  CASE J14: verdict: expected 'RUNWAY_UNKNOWN', got 'RUNWAY_AS_CONFIGURED'; exit: expected 2, got 0; configured.state: expected 'absent', got 'set'; configured.value: expected None, got 7; effective: expected None, got 7
mutant M2a+defect: MORI_JOB_RUNWAY_SELFTEST: PASS 19/21  rc=0
```

— the mutated harness is **blind to a real defect** that the pristine harness names. **Does omp's
real behaviour make it matter? Yes**: the `async:` block missing (a host with no
`~/.omp/agent/config.yml`, or a renamed key) is exactly the situation in which the runway falls back
to the compiled default, and rule 1's `absent` state is what the tool reports as `RUNWAY_DEFAULT`.
Severity: **medium** (the count is load-bearing; the exit code is not).

## Extra probes (same family, beyond the four assigned points)

| Probe | Change | Frozen | Supplementary | Verdict |
|---|---|---|---|---|
| T1 | tool: `effective` halved (`max(1, min(clamp, base) // 2)`) | `FAIL 8/21` rc 2 — `CASE J01 … J21` | `FAIL 16/18` rc 2 — `CASE R03`, `CASE R17` | killed (corpus covers the tool) |
| T2 | tool: payload drops the `schema` field | `PASS 21/21` rc 0 | `PASS 18/18` rc 0 | **survived** |
| T3 | tool: `binary_sha256` always `null` | `PASS 21/21` rc 0 | `PASS 18/18` rc 0 | **survived** |
| T4 | tool: `clamp.sites` forced to 1 | `FAIL 20/21` rc 2 — `CASE J11` | `PASS 18/18` rc 0 | killed by frozen only |

T2/T3: rule 6 of the contract requires the JSON object to carry `schema`, `config_path`,
`binary_path` and `binary_sha256`, but **no case in either corpus asserts any of them** — the
expectation blocks only ever carry `verdict`, `exit`, `configured`, `clamp`, `setting_default`,
`effective`. A tool that dropped the schema string or the binary digest would still print
`PASS 21/21`. Severity: **medium** (the schema string is what a consumer greps for; the digest is
what ties a report to a binary). T4: the supplementary 18 add no `clamp.sites` coverage of their
own (only the frozen J11 has two sites) — informational, not a defect.

## Smallest fixes (harness only; not applied — the lane is read-only for this seat)

One compact change in `_selftest` kills all six harness mutants at once:

```python
    # after the loop
    if executed != len(cases):                       # kills M2a, M2b (skipped cases)
        failures.append("?: %d of %d cases were not executed" % (executed, len(cases)))
    if total == 0:                                   # kills M4 (already present, keep it)
        failures.append("?: no cases loaded")
    # per case, before comparing
    required = {"verdict", "exit", "configured", "clamp", "setting_default", "effective"}
    if not required <= set(expect):                  # kills M3, M5
        problems = ["expect must name %s" % ", ".join(sorted(required))]
    # one self-check of the comparator itself
    if not _compare({"verdict": observed["verdict"], "effective": -1}, observed, ""):
        problems.append("comparator did not reject a wrong field")   # kills M1
```

`executed` is a counter incremented for every case that is actually run. The comparator self-check
is the piece that makes the harness witness itself: it fails if `_compare` ever stops comparing the
numeric fields. Optional extra: assert `schema == "mori-job-runway-v1"` and that `binary_sha256` is
a 64-hex string whenever the binary was readable — that kills T2/T3.

## Observations outside the assigned target (not counted, for the owning seats)

* The lane tip has **no** `.ufo/waves/round-25/evidence/runway-selftest.txt`, which amendment A1
  makes the committed evidence for the C2 after-value:
  `git ls-files .ufo/waves/round-25/evidence/` lists `pressure-selftest.txt`, `routed-r24-*.txt`,
  `wave1-bind.json`, `wave2-bind.json` only. The after-value string itself is reproducible (baseline
  above), so this is a missing-commit observation, owned by the evidence/claim-admission seats.
* The supplementary corpus (18 cases) is co-evolved and not counted toward the after-value, per A2.
  It is being co-evolved **concurrently**: at the time of this session the file in the lane was
  sha256 `8d09756d10a9f501b0fa69599e096ce6ef5f3cd9debda89b5de2bc094679ffd6` (18 cases, the bytes
  measured here) and it later became `6c5d5251946bc3335ff5a49312cb5062633bb7eeaa8e54255cd656e4459014a6`
  (+140 uncommitted lines, another seat's work — not mine, left untouched). A re-run of the
  supplementary detector may therefore report a different count; the frozen 21-case corpus
  (`7098b008d614e84c4328af96d15badef700ea84b75a43ba4a375264a01755fb4`) is unchanged.

## Restoration evidence

* Pristine tool bytes: `5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411`
  (identical in the lane and in the private copy before and after the whole session).
* After every mutant, the tool file was restored from the backup and re-hashed: `restored_exactly:
  true` for all six mutants (`mutants.json` in the private copy), and the final check after the
  probes printed `final restored sha 5d90d7d4… matches pristine: True`.
* Lane untouched: `git status --porcelain` in
  `/home/vgpnk/Projects/shokunin/mori-shokunin` shows no modification to `tools/` or
  `tools/fixtures/`; the only file this seat wrote in the lane is this report.
* No `jj` command was run anywhere; no git write was run in the lane; `omp` was never executed (the
  tool only reads the binary's bytes).
* Tooling: no package was installed or upgraded for this seat (the mutation harness is plain
  Python 3 standard library: `python3 -I -B`). The private copy lives at
  `/fast/scratch/hyaku/mori-r25/w2-MutRunwaySelftest` and can be deleted with
  `rm -rf /fast/scratch/hyaku/mori-r25/w2-MutRunwaySelftest`.

## Summary table

| Mutant | D-A (declared after-value) | D-B (exit code only) | Verdict | Failing case id |
|---|---|---|---|---|
| M1 compare only verdict | survived | survived | **survivor** — killing input `probe-m1-cases.json` (J01, J02, J05) | none |
| M2a skip null-config cases | killed (`PASS 19/21`) | survived | **weakened** — killed by the count only | none |
| M2b skip null-config + recount | killed (`PASS 19/19`) | survived | **weakened** — killed by the count only | none |
| M3 no empty-expect guard | survived | survived | **survivor** — killing input `probe-m3-cases.json` (J07, J08) | none |
| M4 no zero-case guard | survived | survived | **survivor** — killing input `probe-m4-cases.json` (`?: no cases loaded`) | none |
| M5 `exit` not required in expect | survived | survived | **survivor** — killing input `probe-m5-cases.json` (J09, J10) | none |
