# MutRunwayYamlScope — mutation attack on `tools/mori-job-runway.py` rule 1 (YAML block scoping)

Seat: `MoriR25.MutRunwayYamlScope` (wave 2, mutation tester). Target claim: **C2 (coverage)** —
the new read-only harness-runway tool `tools/mori-job-runway.py` and its declared after-value
`MORI_JOB_RUNWAY_SELFTEST: PASS 21/21` over the frozen 21 cases, plus the co-evolved
`tools/fixtures/mori-job-runway/supplementary-cases.json` (18 cases).

## Verdict

**The landed code held; the declared after-value is weakened as a detector.**

- **No defect found in the tool.** On all seven YAML shapes I probed, the shipped rule 1 agrees
  with the YAML the omp harness actually reads (Bun's YAML parser). The tool never produced a
  number where omp would not, and never refused to read a shape omp reads cleanly.
- **Two of five block-scoping mutants survive both case files.** The frozen 21 and the
  supplementary 18 do not discriminate *"the `async` block ends at the next column-0 key"* and
  *"a comment line does not set the child indentation"*. The declared after-value
  (`PASS 21/21`, exit 0) is therefore **not evidence** that rule 1's block scoping is correct:
  a rule-1 regression that reports a false number or a false abstention still prints
  `PASS 21/21`.
- Severity: **medium as a calibration/coverage finding** (the declared gate does not pin a
  contract rule), **low in operational effect** (the two survivors need a config shape that the
  shipped omp settings schema does not produce, or an unusual hand-written comment).
- The two survivors are **fixture gaps, not code bugs**. The smallest fix is two co-evolved
  cases (verified below); the frozen file must not be touched (it is pinned by contract).

## What I did

Private clone only: `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin
/fast/scratch/hyaku/mori-r25/w2-MutRunwayYamlScope` (HEAD `e5e1b7b`). The lane checkout was
**not** modified — the only file written in the lane is this report. No `jj`/`git` mutation was
run in the lane or the fleet root; `omp` was never executed (its bytes were read only, and
the operator's OMP settings file was read read-only).

Environment: Python 3.14.8, `python3 -I -B` throughout. **No tool was installed** (nothing to
install: `python3` 3.14.8 and `bun` 1.4.3 were already present); `bun` was used read-only as the
YAML-semantics oracle because the installed `omp` is a Bun-compiled binary.

### Baseline (pristine clone)

```
$ sha256sum tools/mori-job-runway.py
5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411  tools/mori-job-runway.py
$ python3 -I -B tools/mori-job-runway.py --selftest
MORI_JOB_RUNWAY_SELFTEST: PASS 21/21            exit 0
$ python3 -I -B tools/mori-job-runway.py --selftest --cases tools/fixtures/mori-job-runway/supplementary-cases.json
MORI_JOB_RUNWAY_SELFTEST: PASS 18/18            exit 0
```

The same three sha256 values hold in the lane (`tools/mori-job-runway.py` `5d90d7d4…c3411`,
`cases.json` `7098b008…55fb4`, `supplementary-cases.json` `8d09756d…9ffd6`) — the lane was
never touched.

### Detectors

| id | command | expected on pristine |
|---|---|---|
| D-frozen | `python3 -I -B tools/mori-job-runway.py --selftest` | `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21`, exit 0 |
| D-supp | `python3 -I -B tools/mori-job-runway.py --selftest --cases tools/fixtures/mori-job-runway/supplementary-cases.json` | `MORI_JOB_RUNWAY_SELFTEST: PASS 18/18`, exit 0 |

Each mutant was applied to the pristine bytes, both detectors were run, then the file was
restored from a byte copy and re-hashed. One mutant at a time; no two mutants were ever live
together.

## Mutants and results

All four mutation sites are in `tools/mori-job-runway.py`, function `_parse_config` (rule 1).

| id | mutation | site | D-frozen (21) | D-supp (18) | verdict |
|---|---|---|---|---|---|
| **Y1** | deeper children count as direct children (indent filter dropped) | `tools/mori-job-runway.py:334` (`if _indent_of(line) != child_indent:` → `if False:`) | **KILLED** — `FAIL 20/21`, `CASE J19` | survived — `PASS 18/18` | killed |
| **Y2a** | the `async` block does not end at the next column-0 key | `tools/mori-job-runway.py:310` (`if line[:1] not in ("", " ", "\t") and not _is_blank_or_comment(line): break` → `if False:`) | **SURVIVED** — `PASS 21/21` | **SURVIVED** — `PASS 18/18` | **survivor** |
| **Y2b** | the scan covers the whole file, so a `maxJobs` under another top-level block counts | `tools/mori-job-runway.py:305` (`for index in range(async_lines[0] + 1, len(lines)):` → `range(0, len(lines))`) | **KILLED** — `FAIL 8/21`, failing ids `J01 J02 J03 J07 J08 J09 J10 J11 J12 J15 J17 J18 J21` | **KILLED** — `FAIL 11/18`, failing ids `R03 R04 R08 R10 R15 R16 R17` | killed |
| **Y3** | an indented comment ends the `async` block | `tools/mori-job-runway.py:310` (extra `break` when the line is an indented `#` comment) | **KILLED** — `FAIL 20/21`, `CASE J01` | survived — `PASS 18/18` | killed |
| **Y4** | a comment line also sets the child indentation | `tools/mori-job-runway.py:323` (`if index in continuation or _is_blank_or_comment(line): continue` → blank-only skip) | **SURVIVED** — `PASS 21/21` | **SURVIVED** — `PASS 18/18` | **survivor** |

Mutated-file sha256 (the "before/after" of each probe):

| mutant | sha256 of `tools/mori-job-runway.py` while mutated |
|---|---|
| pristine | `5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411` |
| Y1 | `3eeb116765c8871c…` |
| Y2a | `5d3dd7d772748e2f…` |
| Y2b | `0403caaec5ba0a61…` |
| Y3 | `dec90ec2b733c523…` |
| Y4 | `acbbe3f291df5b69…` |

### Exact detector output for the killed mutants

Y1 (D-frozen, exit 2):

```
MORI_JOB_RUNWAY_SELFTEST: FAIL 20/21
CASE J19: verdict: expected 'RUNWAY_DEFAULT', got 'RUNWAY_AS_CONFIGURED'; configured.state: expected 'absent', got 'set'; configured.value: expected None, got 5; effective: expected 100, got 5
```

Y3 (D-frozen, exit 2):

```
MORI_JOB_RUNWAY_SELFTEST: FAIL 20/21
CASE J01: verdict: expected 'RUNWAY_CLAMPED', got 'RUNWAY_DEFAULT'; exit: expected 1, got 0; configured.state: expected 'set', got 'absent'; configured.value: expected 200, got None
```

Y2b (D-frozen, exit 2, 13 failures) and (D-supp, exit 2, 7 failures) — first lines:

```
MORI_JOB_RUNWAY_SELFTEST: FAIL 8/21
CASE J01: verdict: expected 'RUNWAY_CLAMPED', got 'RUNWAY_DEFAULT'; exit: expected 1, got 0; configured.state: expected 'set', got 'absent'; configured.value: expected 200, got None
...
MORI_JOB_RUNWAY_SELFTEST: FAIL 11/18
CASE R03: verdict: expected 'RUNWAY_AS_CONFIGURED', got 'RUNWAY_DEFAULT'; configured.state: expected 'set', got 'absent'; configured.value: expected 50, got None; effective: expected 50, got 100
```

### Behavioural divergence on seven probe configs (with the pristine tool as reference)

Each probe was run with a synthetic binary carrying the clamp (`Math.min(100, …)`) and the
setting default (`default: 100`). "Truth" is `Bun.YAML.parse` — the YAML parser of the shipped
Bun-compiled `omp` (`~/.local/bin/omp` carries Bun's `YAML Parse error: Unable to parse YAML
string` and omp's own `Config overlay must be a YAML mapping`).

| probe (config text) | truth (`Bun.YAML.parse`) | pristine tool | Y1 | Y2a | Y2b | Y3 | Y4 |
|---|---|---|---|---|---|---|---|
| P1 `async:\n  # background jobs\n  enabled: true\n  maxJobs: 200` | `{"async":{"enabled":true,"maxJobs":200}}` | set 200 ✓ | set 200 | set 200 | **absent** | **absent** | set 200 |
| P2 `async:\n  widgets:\n    maxJobs: 5\n  enabled: true` | `{"async":{"widgets":{"maxJobs":5},"enabled":true}}` | absent ✓ | **set 5** | absent | absent | absent | absent |
| P3 `async:\n  enabled: true\ntask:\n  maxJobs: 300` | `{"async":{"enabled":true},"task":{"maxJobs":300}}` | absent ✓ | absent | **set 300** | absent | absent | absent |
| P4 `async:\n  maxJobs: 50\ntask:\n  maxJobs: 300` | `{"async":{"maxJobs":50},"task":{"maxJobs":300}}` | set 50 ✓ | set 50 | **malformed** | absent | set 50 | set 50 |
| P5 `async:\n# note\n  maxJobs: 40` | `{"async":{"maxJobs":40}}` | set 40 ✓ | set 40 | set 40 | absent | set 40 | **absent** |
| P6 `async:\n    # note\n  maxJobs: 50` | `{"async":{"maxJobs":50}}` | set 50 ✓ | set 50 | set 50 | absent | **absent** | **absent** |
| P7 = P3 (alias) | `{"async":{"enabled":true},"task":{"maxJobs":300}}` | absent ✓ | absent | **set 300** | absent | absent | absent |

Live host check (real the operator's OMP settings file + real `~/.local/bin/omp`, read-only):

```
pristine : configured {set 200}  effective 100  RUNWAY_CLAMPED  exit 1
Y1       : configured {set 200}  effective 100  RUNWAY_CLAMPED  exit 1
Y2a      : configured {set 200}  effective 100  RUNWAY_CLAMPED  exit 1
Y2b      : configured {absent}   effective 100  RUNWAY_DEFAULT  exit 0
Y3       : configured {set 200}  effective 100  RUNWAY_CLAMPED  exit 1
Y4       : configured {set 200}  effective 100  RUNWAY_CLAMPED  exit 1
```

(The host config is `async:\n  maxJobs: 200` followed by `tier:` — one child, no comments, no
foreign `maxJobs` — so only Y2b changes the live reading, and Y2b is killed by the suites.)

## Survivors: killing input, and whether omp's real behaviour makes it matter

### S1 — Y2a (block does not end at the next column-0 key) — survives both files

**Killing input (verified):** config

```
async:
  enabled: true
task:
  maxJobs: 300
```

expected `configured {state: absent, value: null}`, `verdict RUNWAY_DEFAULT`, `exit 0`
(pristine tool gives exactly this); Y2a gives `configured {set, 300}`, `RUNWAY_CLAMPED`, exit 1.

A second discriminating input: `async:\n  maxJobs: 50\ntask:\n  maxJobs: 300` — pristine gives
`set 50` / `RUNWAY_AS_CONFIGURED` / exit 0; Y2a gives `malformed` → `RUNWAY_UNKNOWN`, exit 2.

**Does omp's real behaviour make it matter?** omp reads the first as
`{"async":{"enabled":true},"task":{"maxJobs":300}}` — `async.maxJobs` is **undefined**, so the
pristine tool's "absent" is right and Y2a's "300" is a false number; the second as
`{"async":{"maxJobs":50},"task":{"maxJobs":300}}` — pristine's "set 50" is right and Y2a's
"malformed" is a false abstention. So the mutant is wrong against omp in both directions.

**But it is hard to reach in practice.** The defect needs a `maxJobs` key under a top-level
block *other than* `async`. A byte scan of the shipped binary shows the only `maxJobs` strings in
`~/.local/bin/omp` are the setting id (byte 96085914), its definition `id: "async.maxJobs" …`
(byte 155231601) and the clamp site — the `async.` settings are `async.enabled`, `async.maxJobs`,
`async.widgets`. No other omp setting is named `maxJobs`, so a foreign `maxJobs` is not an omp
setting and omp would never read it as `async.maxJobs`. **Operational severity: low.**
**Coverage severity: medium** — the declared after-value does not pin contract rule 1's
"the block runs to the next non-blank, non-comment line at column 0"
(`tools/mori-job-runway.py:20`, `tools/mori-job-runway.py:303`).

### S2 — Y4 (a comment line sets the child indentation) — survives both files

**Killing input (verified):** config

```
async:
# note
  maxJobs: 40
```

expected `configured {state: set, value: 40}`, `RUNWAY_AS_CONFIGURED`, exit 0 (pristine gives
exactly this); Y4 gives `absent` → `RUNWAY_DEFAULT`, exit 0. The variant
`async:\n    # note\n  maxJobs: 50` kills Y4 the same way (pristine `set 50`, Y4 `absent`).

**Does omp's real behaviour make it matter?** omp (Bun's YAML) reads both as
`{"async":{"maxJobs":40}}` / `{"async":{"maxJobs":50}}` — a comment is not content and its
indentation is irrelevant, so the pristine tool is right and Y4 is a false negative.

**Operational severity: low-to-medium.** The shape needs a comment inside the `async` block
whose indentation differs from the keys (a column-0 comment inside an indented block, or a
deeper-indented one). Both are hand-writable but unusual; on this host's shape the consequence
would be that the tool reports "absent / RUNWAY_DEFAULT" instead of "configured 200 vs clamp
100 → RUNWAY_CLAMPED" — i.e. the tool loses the finding it exists to make, in the safe
direction (never a false number). **Coverage severity: medium** — the same declared-after-value
gap, on a different clause of rule 1 ("Direct children sit at the indentation of the block's
first non-blank, non-comment line", `tools/mori-job-runway.py:20`).

### What the survivors are not

Neither survivor is a defect in the shipped rule 1. The landed parser matches omp's YAML on all
seven probes. What is missing is **fixture coverage of two scoping clauses**, so the after-value
`PASS 21/21` cannot be read as "rule 1's block scoping is correct". The frozen case file
contains a block-scope case (J19: `async:\n  widgets:\n    maxJobs: 5`) and a comment-in-block
case (J01: an indented comment before the children) — those two kill Y1 and Y3 — but nothing
pins *where the block ends* and nothing pins *that a comment does not set the child
indentation*.

## Smallest fix (verified)

Two co-evolved cases in `tools/fixtures/mori-job-runway/supplementary-cases.json` (the frozen
`cases.json` must not change: blob `48df844a` at `7634be75` is pinned by
`.ufo/waves/round-25/contract.md:129-130`):

```json
{
  "id": "R19",
  "what": "the async block ends at the next top-level key: a maxJobs under another block is not async.maxJobs",
  "config": "async:\n  enabled: true\ntask:\n  maxJobs: 300\n",
  "binary": "<the same clamp+default string the other R cases carry>",
  "expect": {
    "verdict": "RUNWAY_DEFAULT", "exit": 0,
    "configured": {"state": "absent", "value": null},
    "clamp": {"state": "found", "value": 100, "sites": 1},
    "setting_default": {"state": "found", "value": 100},
    "effective": 100
  }
},
{
  "id": "R20",
  "what": "a comment line inside the async block neither ends the block nor sets the child indentation",
  "config": "async:\n# note\n  maxJobs: 40\n",
  "binary": "<the same clamp+default string the other R cases carry>",
  "expect": {
    "verdict": "RUNWAY_AS_CONFIGURED", "exit": 0,
    "configured": {"state": "set", "value": 40},
    "clamp": {"state": "found", "value": 100, "sites": 1},
    "setting_default": {"state": "found", "value": 100},
    "effective": 40
  }
}
```

Measured with the two cases appended to the supplementary file in the scratch clone:

```
pristine : MORI_JOB_RUNWAY_SELFTEST: PASS 20/20
Y1       : PASS 20/20
Y2a      : FAIL 19/20   failing ids: ['R19']
Y2b      : FAIL 12/20   failing ids: ['R03','R04','R08','R10','R15','R16','R17','R20']
Y3       : PASS 20/20
Y4       : FAIL 19/20   failing ids: ['R20']
```

So R19 kills the Y2a survivor and R20 kills the Y4 survivor, and no other mutant regresses.
Note for the integrator: contract amendment A2 states the supplementary file "is not counted
toward the after-value" (`contract.md:152-154`), so the *declared* after-value stays
`PASS 21/21`; the discriminating gate has to be named explicitly (run the supplementary selftest
too), or a new frozen generation has to be cut. I am not changing the contract's wording.

## Restoration evidence

- After every mutant the tool file was restored from a byte copy and re-hashed: sha256
  `5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411` in every case, identical to
  the pristine value and to the lane's file.
- Final state of the scratch clone: `git status --short` empty; `sha256sum
  tools/mori-job-runway.py` = `5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411`;
  the temporary `proposed-cases.json` and the backup copies were deleted.
- The lane checkout was never written to except for this report file
  (`.ufo/waves/round-25/w2/MutRunwayYamlScope.md`); the lane's
  `tools/mori-job-runway.py` still hashes to `5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411`.

## Bounds and honest limits

- Read-only on the lane except this report; all mutation happened in
  `/fast/scratch/hyaku/mori-r25/w2-MutRunwayYamlScope` (a `git clone --no-hardlinks` of the
  lane) and was removed afterwards.
- No `jj` command was run at the fleet root or in the lane; no `git add/commit/stash/checkout/
  switch/reset/pull/push` in the lane or the fleet repo; the lane Git index was not touched.
- `omp` was never executed. The installed binary was read as bytes only; the harness's YAML
  semantics were taken from `Bun.YAML.parse` (bun 1.4.3), the same parser family the
  Bun-compiled binary embeds — this is a *parity* argument, not a session observation: I did not
  start a harness session and did not observe which YAML library a live session uses for
  `config.yml`.
- The Y2a/Y4 severities are judged against the *shipped* settings schema (one `maxJobs`
  setting). A deployment with a project-layer or hand-written config that carries a foreign
  `maxJobs` key, or a config whose `async` block carries an oddly indented comment, would hit
  the mutants' wrong answers.
- No claim is made about `async.maxJobs` under other config layers (project layer, `--config`
  overlay, runtime override); that is the knowledge note's U4, unchanged by this probe.
- Tooling: no package was installed or upgraded (nothing was missing); `python3` 3.14.8 and
  `bun` 1.4.3 were already on the host.

## Files

- This report: `.ufo/waves/round-25/w2/MutRunwayYamlScope.md`.
- Scratch: the clone `/fast/scratch/hyaku/mori-r25/w2-MutRunwayYamlScope` (357 MB) was removed
  after the run. The small evidence set was kept out of the shared scratch root, under
  `/fast/scratch/hyaku/mori-r25/w2-MutRunwayYamlScope-evidence/`:
  `harness.py` (the mutation harness: patches, detectors, probe table),
  `mutation-results.json` (raw detector output, mutated-file hashes, probe table),
  `pass2.json` (live-host readings per mutant), `yaml-truth.json` (Bun.YAML ground truth),
  `probes.tsv` (probe config texts). No other seat's scratch was touched.
