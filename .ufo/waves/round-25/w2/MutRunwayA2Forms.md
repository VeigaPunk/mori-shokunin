# MutRunwayA2Forms — mutation attack on the A2 abstentions of `tools/mori-job-runway.py` (claim C2)

Seat: `MoriR25.MutRunwayA2Forms` (wave 2, mutation tester). Target claim: **C2 (coverage)** —
`tools/mori-job-runway.py` and its declared after-value `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21`
over the frozen 21 cases, plus the co-evolved `tools/fixtures/mori-job-runway/supplementary-cases.json`
(18 cases, R01–R18) that amendment A2 made the home of the A2 abstentions.

Scope of this seat: one mutant per A2 abstention, applied one at a time, each run against the same
two bounded detectors, each restored to exact bytes afterwards. Rule-1 block scoping and the
verdict/exit ordering are other seats' scope (`MutRunwayYamlScope`, `MutRunwayVerdictOrder`).

## Verdict

**The A2 abstentions are pinned — with one caveat that is about the counted after-value, not about
the tool.**

- **Eight of ten mutants are killed**, each by exactly the case that names its form: R01 (quoted
  `async` key), R02 (`async :`), R10 (tab indent), R12 (document marker), R08 (`#` without space),
  R05+R13 (`<<:` merge key), R04 (quoted `maxJobs` child), R06+R14 (`? ` complex key). No mutant
  survived that changed behaviour.
- **Two mutants survive: M6 (block-scalar clause) and M10 (quote-opening clause). Both are
  equivalent mutants — no input can kill them.** The two clauses are dead code: every value the
  block-scalar clause rejects is rejected a line later by the integer check, and every
  quote-leading value is rejected by the integer check too. Removing them changes the tool's
  answer on **zero** inputs (differential over 201 candidate values: 0 differences). The tool's
  behaviour is correct; the clauses are redundant, and cases R15/R16 pass for a reason other than
  the one they name.
- **The counted after-value detects none of the ten.** For every mutant the frozen 21 still print
  `PASS 21/21`, exit 0. Detection rests entirely on the supplementary file, which amendment A2
  explicitly excludes from the after-value ("not counted toward the after-value"). A regression
  that deletes every A2 abstention would still satisfy C2's declared after-value.
  Severity: **medium as a calibration finding, low in operational effect** (the tool is right; the
  gate that is supposed to witness it is blind).
- **The tool never produces a number omp would not use.** For the forms where the tool abstains,
  Bun's YAML parser (the one the omp binary embeds) either refuses the file or yields a non-number,
  with two exceptions — the quoted `async` key (R01) and `async :` (R02) — where omp reads a clean
  `50` and the tool abstains anyway. Those two abstentions are **over-conservative, not wrong**:
  they lose ground, never invent it.
- Severity of the whole set: **no defect in the shipped tool** (the eight killed mutants were
  killed, and the two survivors change nothing). Two **low** findings are about dead code and case
  attribution, one **medium** finding is about the counted gate's blindness, one **info** finding
  is a missing committed evidence file.

## What I did

Private copy only: `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin
/fast/scratch/hyaku/mori-r25/w2-MutRunwayA2Forms` (clone HEAD `07a31ae`; the lane's own git HEAD
is `e5e1b7b` — the tool bytes are identical in both, sha256 `5d90d7d4…c3411`). The lane checkout
was **not** modified; the only file written in the lane is this report. No `jj`/`git` mutation was
run in the lane or at the fleet root. `omp` was never executed: its bytes were read only
(`grep -a` over `~/.local/bin/omp`, 256,702,432 bytes), and `~/.omp/agent/config.yml` was read
read-only.

Environment: Python 3.14.8, `python3 -I -B` throughout, Bun 1.4.3 (already installed; used as the
YAML-semantics oracle because the omp binary is Bun-compiled: `grep -a -o -c` over the binary
gives `YAML.parse` 3, `Bun.YAML` 2, `async.maxJobs` 2, `maxRunningJobs` 3). **No tool was
installed or upgraded** — nothing was needed.

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
`cases.json` `7098b008…55fb4`, `supplementary-cases.json` `8d09756d…9ffd6`); the lane was never
touched. The frozen file's git blob is still the pinned `48df844a22d74a57204f55a62e54760c7038c60f`
at `7634be75` and at the tip; the tool blob at the tip is `239dd8ebe630400a2739151260e482ad83dea459`.

### Detectors

| id | command | expected on pristine |
|---|---|---|
| D-frozen | `python3 -I -B tools/mori-job-runway.py --selftest` | `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21`, exit 0 |
| D-supp | `python3 -I -B tools/mori-job-runway.py --selftest --cases tools/fixtures/mori-job-runway/supplementary-cases.json` | `MORI_JOB_RUNWAY_SELFTEST: PASS 18/18`, exit 0 |

One mutant at a time: the pristine bytes were copied aside, the mutant was applied to the copy,
both detectors ran, then the file was restored from the copy and re-hashed. No two mutants were
ever live together. A mutant was counted as *killed* only when a detector that was green on
pristine turned red on the mutant.

## Mutants and results

All sites are in `tools/mori-job-runway.py`, function `_parse_config` (rule 1 + A2).

| id | A2 clause removed | site (pristine) | D-frozen (21) | D-supp (18) | verdict | failing case |
|---|---|---|---|---|---|---|
| **M1** | quoted top-level `async` key (`"async":`) | `tools/mori-job-runway.py:295-297` (`if not header.startswith(ASYNC_PREFIX): return "malformed", None` → accept a `"async":` header) | **survived** `PASS 21/21` | **KILLED** `FAIL 17/18`, exit 2 | killed | **R01** |
| **M2** | space before the colon (`async :`) | same guard, a second mutant that accepts only the spaced spelling | **survived** `PASS 21/21` | **KILLED** `FAIL 17/18`, exit 2 | killed | **R02** |
| **M3** | tab in the indentation of an async-block line | `tools/mori-job-runway.py:317-319` (`if "\t" in _leading_whitespace(line):` removed) | **survived** `PASS 21/21` | **KILLED** `FAIL 17/18`, exit 2 | killed | **R10** |
| **M4** | `---` / `...` document marker anywhere | `tools/mori-job-runway.py:265-267` (`if DOC_MARKER_RE.match(stripped):` removed) | **survived** `PASS 21/21` | **KILLED** `FAIL 17/18`, exit 2 | killed | **R12** |
| **M5** | `#` not preceded by whitespace | `tools/mori-job-runway.py:353-356` (the `raw[index - 1] not in " \t"` guard removed) | **survived** `PASS 21/21` | **KILLED** `FAIL 17/18`, exit 2 | killed | **R08** |
| **M6** | a `maxJobs` value opening a block scalar | `tools/mori-job-runway.py:361` (`or BLOCK_SCALAR_RE.match(value)` removed) | **survived** `PASS 21/21` | **survived** `PASS 18/18` | **survivor (equivalent)** | – |
| **M7** | `<<:` merge key | `tools/mori-job-runway.py:271-273` (`if MERGE_KEY_RE.match(stripped):` removed) | **survived** `PASS 21/21` | **KILLED** `FAIL 16/18`, exit 2 | killed | **R05, R13** |
| **M8** | quoted direct child key (`"maxJobs":`) | `tools/mori-job-runway.py:341-344` (`if key == "maxJobs": return "malformed", None` removed) | **survived** `PASS 21/21` | **KILLED** `FAIL 17/18`, exit 2 | killed | **R04** |
| **M9** | *(extra, beyond the assigned list)* `? ` complex key | `tools/mori-job-runway.py:268-270` (`if COMPLEX_KEY_RE.match(stripped):` removed) | **survived** `PASS 21/21` | **KILLED** `FAIL 16/18`, exit 2 | killed | **R06, R14** |
| **M10** | *(extra)* a `maxJobs` value opening a quote | `tools/mori-job-runway.py:361` (`value[:1] in ('"', "'")` removed) | **survived** `PASS 21/21` | **survived** `PASS 18/18` | **survivor (equivalent)** | – |

Failing-case detail (verbatim from the mutated runs, `CASE <id>: <mismatches>`):

```
M1  R01: verdict: expected 'RUNWAY_UNKNOWN', got 'RUNWAY_AS_CONFIGURED'; exit: expected 2, got 0; configured.state: expected 'malformed', got 'set'; configured.value: expected None, got 50; effective: expected None, got 50
M2  R02: verdict: expected 'RUNWAY_UNKNOWN', got 'RUNWAY_AS_CONFIGURED'; exit: expected 2, got 0; configured.state: expected 'malformed', got 'set'; configured.value: expected None, got 50; effective: expected None, got 50
M3  R10: verdict: expected 'RUNWAY_UNKNOWN', got 'RUNWAY_AS_CONFIGURED'; exit: expected 2, got 0; configured.state: expected 'malformed', got 'set'; configured.value: expected None, got 50; effective: expected None, got 50
M4  R12: verdict: expected 'RUNWAY_UNKNOWN', got 'RUNWAY_AS_CONFIGURED'; exit: expected 2, got 0; configured.state: expected 'malformed', got 'set'; configured.value: expected None, got 50; effective: expected None, got 50
M5  R08: verdict: expected 'RUNWAY_UNKNOWN', got 'RUNWAY_AS_CONFIGURED'; exit: expected 2, got 0; configured.state: expected 'malformed', got 'set'; configured.value: expected None, got 50; effective: expected None, got 50
M7  R05: verdict: expected 'RUNWAY_UNKNOWN', got 'RUNWAY_DEFAULT'; exit: expected 2, got 0; configured.state: expected 'malformed', got 'absent'; effective: expected None, got 100
    R13: verdict: expected 'RUNWAY_UNKNOWN', got 'RUNWAY_AS_CONFIGURED'; exit: expected 2, got 0; configured.state: expected 'malformed', got 'set'; configured.value: expected None, got 50; effective: expected None, got 50
M8  R04: verdict: expected 'RUNWAY_UNKNOWN', got 'RUNWAY_DEFAULT'; exit: expected 2, got 0; configured.state: expected 'malformed', got 'absent'; effective: expected None, got 100
M9  R06: verdict: expected 'RUNWAY_UNKNOWN', got 'RUNWAY_DEFAULT'; exit: expected 2, got 0; configured.state: expected 'malformed', got 'absent'; effective: expected None, got 100
    R14: verdict: expected 'RUNWAY_UNKNOWN', got 'RUNWAY_DEFAULT'; exit: expected 2, got 0; configured.state: expected 'malformed', got 'absent'; effective: expected None, got 100
```

### Before/after hashes (restoration evidence)

Pristine sha256 of `tools/mori-job-runway.py`: `5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411`.

| id | mutant sha256 (first 12) | restored sha256 (first 12) | restored == pristine |
|---|---|---|---|
| M1 | `4816174a6b58` | `5d90d7d43df0` | yes |
| M2 | `7153296a4d6e` | `5d90d7d43df0` | yes |
| M3 | `0036f0d21ffa` | `5d90d7d43df0` | yes |
| M4 | `96c94344999f` | `5d90d7d43df0` | yes |
| M5 | `58f1fbf325d8` | `5d90d7d43df0` | yes |
| M6 | `f157bda33f11` | `5d90d7d43df0` | yes |
| M7 | `6f4fb638142b` | `5d90d7d43df0` | yes |
| M8 | `5a4f93d7b21a` | `5d90d7d43df0` | yes |
| M9 | `9c03cdc5df3d` | `5d90d7d43df0` | yes |
| M10 | (recorded in the log below) | `5d90d7d43df0` | yes |

Final state after the whole run: `sha256sum tools/mori-job-runway.py` → `5d90d7d43df0…c3411`,
`diff` against the lane working copy → identical, and both detectors green again
(`PASS 21/21`, `PASS 18/18`). The clone's only untracked leftovers are my own log files
(`.mutant-log.json`, `.pristine-tool.py`).

## The two survivors, in detail

### M6 — block scalar clause; M10 — quote-opening clause

**Which input would kill them: none.** Both clauses are unreachable in effect, because the value
check two lines later already rejects everything they reject:

```
BLOCK_SCALAR_RE = ^[|>][+-]?\d*\s*(#.*)?$      INTEGER_RE = ^[+-]?[0-9]+$
```

`BLOCK_SCALAR_RE` requires a first character of `|` or `>`; `INTEGER_RE` requires a first
character in `[+-0-9]`. The two sets are disjoint, and a quote-leading value (`"50"`, `'50'`) can
never match `INTEGER_RE` either. Measured directly
(`/fast/scratch/hyaku/mori-r25/equivalence_check.py`, 201 candidate values built from
`| > - + 2 0 " ' # space x 1 tab` plus hand-picked values):

```
values tried: 201
M6 (block-scalar clause removed) differences: 0 []
M10 (quote clause removed) differences: 0 []
intersection BLOCK_SCALAR_RE and INTEGER_RE: []
quote-leading values accepted by INTEGER_RE: []
```

**Does omp's real behaviour make it matter: no.** Bun 1.4.3 reads the R16 shape
`maxJobs: |\n    50` as the **string** `"50\n"` and the R15 shape `maxJobs: "50"` as the string
`"50"`. Neither is the number the setting wants, so omp does not use it (it falls back to the
`async.maxJobs` default of 100), and the tool's `malformed` → `RUNWAY_UNKNOWN` → exit 2 is the
safe direction. Deleting the dead clauses changes nothing omp can observe.

**What this does mean.** Cases R15 and R16 are *named* after these clauses but are actually
carried by the integer check, so their `what` text overstates what they pin. Severity: **low**
(dead code and case attribution, no behavioural defect). Smallest fix, in order of preference:
1. delete the two clauses (behaviour identical — verified above) and amend the R15/R16 `what`
   text to say the value is not a decimal integer; or
2. keep them and reword R15/R16 to say the abstention is carried by the integer check.

## Does it matter in the real harness? (omp behaviour per mutant)

Ground truth from Bun 1.4.3 on the same config texts
(`/fast/scratch/hyaku/mori-r25/bun_yaml_probe.ts`):

| form | Bun / omp reads | pristine tool | mutant's answer | is the mutant's answer a false number? |
|---|---|---|---|---|
| R01 `"async":` | `async.maxJobs = 50` (number) | malformed / UNKNOWN | 50 | **no** — it matches omp; the clause is stricter than omp |
| R02 `async :` | `async.maxJobs = 50` (number) | malformed / UNKNOWN | 50 | **no** — same |
| R10 tab indent | **parse error** ("Tab characters cannot be used as indentation") → omp falls back to the default | malformed / UNKNOWN | 50 | **yes** — omp uses 100, the mutant claims 50 |
| R08 `50#x` | the **string** `"50#x"` → not a number → omp uses the default | malformed / UNKNOWN | 50 | **yes** |
| R05 in-block `<<: *d` | `async.maxJobs = 50` (merge resolved) | malformed / UNKNOWN | 100 (absent → default) | **yes** |
| R13 top-level `<<: *defaults` | **parse error** ("Unresolved alias") → omp uses the default | malformed / UNKNOWN | 50 | **yes** |
| R04 `"maxJobs": 50` | `async.maxJobs = 50` | malformed / UNKNOWN | 100 (absent → default) | **yes** |
| R06 `? maxJobs` / `: 50` | `async.maxJobs = 50` | malformed / UNKNOWN | 100 (absent → default) | **yes** |
| R14 `? async` / `: 50` | `async = 50` (no `maxJobs`) → omp uses the default | malformed / UNKNOWN | 100 | no (coincides) |
| R12 `...` end marker | `async.maxJobs = 50` | malformed / UNKNOWN | 50 | **no** — matches omp |
| R16 block scalar | the **string** `"50\n"` | malformed / UNKNOWN | unchanged (equivalent mutant) | n/a |
| R15 quoted value | the **string** `"50"` | malformed / UNKNOWN | unchanged (equivalent mutant) | n/a |

So the tool never turns an unreadable form into a number omp does not use: for every form where
omp would use a different number, the pristine tool abstains. That is the contract's own
requirement ("`RUNWAY_UNKNOWN` is never a false number") and it holds under every mutant.

The live host is unaffected by any of this: `~/.omp/agent/config.yml` reads
`async:` / `  maxJobs: 200` (lines 244–245, no tab, no quote, no marker), and the read-only live
run in the clone gives `configured {state: set, value: 200}`, `clamp {found, 100, sites: 1}`,
`effective 100`, `RUNWAY_CLAMPED`, exit 1 — identical with and without every A2 clause.

## Findings

**F1 — medium (calibration / coverage): the counted after-value detects none of the ten mutants.**
The declared after-value is `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21` over the frozen file. With
each of the ten A2 mutants live, the frozen 21 still printed `PASS 21/21`, exit 0, for all ten.
Every kill came from the supplementary file, which amendment A2 states is "not counted toward the
after-value". Concretely: deleting every A2 abstention from the tool would leave C2's declared
after-value fully satisfied. The tool is right, but the gate that is supposed to witness the A2
behaviour does not.
*Smallest fix:* land the A2 run as committed evidence beside the claim — e.g. a second file
`.ufo/waves/round-25/evidence/runway-selftest-a2.txt` with header lines `revision:`, `command:
python3 -I -B tools/mori-job-runway.py --selftest --cases tools/fixtures/mori-job-runway/supplementary-cases.json`,
`exit: 0`, then the stdout `MORI_JOB_RUNWAY_SELFTEST: PASS 18/18` — and cite it from the
knowledge entry `corpus/knowledge/harness-job-capacity-r25.md` and the SCORECARD round-25 row.
The frozen file must not be touched (blob pinned at `48df844a` by the contract).

**F2 — low (dead code): the block-scalar and quote clauses are unreachable in effect.** Proven
above: 0 behavioural differences over 201 values, disjoint regex sets. R15/R16 pass via
`INTEGER_RE`. No behavioural defect; the fix is a two-clause deletion plus a wording fix on the
two cases, or nothing at all.

**F3 — low (case attribution): the document-marker clause is pinned only by the harmless shape.**
M4 is killed by R12 (`...` end marker), where the mutant's answer (50) is exactly what omp reads —
a contract kill, not a harm-detection kill. The *harmful* shape of the same clause is not pinned:
`async:\n  maxJobs: 50\n---\nother: 1\n` makes Bun return two documents (so omp reads no
`async.maxJobs` and uses the default 100), while the M4 mutant reports `set 50`. Measured with
the tool's own parser (`/fast/scratch/hyaku/mori-r25/shapes_probe.py`):

```
shape                        | pristine _parse_config | M4 _parse_config | bun async.maxJobs | bun error
S1_second_document_marker    | malformed/None         | set/50            | null              | -
S2_end_marker                | malformed/None         | set/50            | 50                | -
S3_leading_marker            | malformed/None         | set/50            | 50                | -
```

R09's `---` shape does not isolate the clause either: it also has two `async` blocks, so the
duplicate-`async` rule (rule 1, not A2) fires first and the case passes for the wrong reason.
*Smallest fix:* add one supplementary case with config
`"async:\n  maxJobs: 50\n---\nother: 1\n"` expecting `verdict RUNWAY_UNKNOWN`, `exit 2`,
`configured {malformed, null}` — that pins the document-marker clause on its own. The frozen
file stays as it is.

**F4 — info (missing committed evidence, flagged for the integration owner):** amendment A1 asks
for a committed evidence file `runway-selftest.txt` under `.ufo/waves/round-25/evidence/` for the
C2 after-value. At the lane tip that file does not exist:
`git ls-tree HEAD .ufo/waves/round-25/evidence/` lists only `pressure-selftest.txt`,
`routed-r24-after-a5.txt`, `routed-r24-after.txt`, `routed-r24-before-a5.txt`,
`routed-r24-before.txt`, `wave1-bind.json`, `wave2-bind.json`. The C2 after-value therefore has
no committed witness at all. This is outside my seat's scope (I did not write to the lane except
this report) — it is reported, not fixed.

**F5 — info (over-conservatism, no action needed):** R01 and R02 are forms omp reads cleanly
(`async.maxJobs = 50`), yet the tool abstains. That is stricter than omp, which loses ground but
never invents it; the contract's A2 requires the abstention, so I propose no change.

## Reproduction

Scratch (private, disposable):
`/fast/scratch/hyaku/mori-r25/w2-MutRunwayA2Forms` (the clone), plus the drivers
`/fast/scratch/hyaku/mori-r25/mut_a2forms.py` (the ten mutants, the two detectors, the restore
and hash log), `/fast/scratch/hyaku/mori-r25/equivalence_check.py` (M6/M10 differential) and
`/fast/scratch/hyaku/mori-r25/shapes_probe.py` (document-marker shapes, pristine vs M4 vs Bun).
The clone is left in place for the reader to inspect; nothing in the lane, in a sibling lane or in
the fleet repo was modified by this seat.
