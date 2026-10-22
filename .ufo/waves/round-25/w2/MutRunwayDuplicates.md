# MutRunwayDuplicates — mutation attack on `tools/mori-job-runway.py` rule 1 (duplicate keys)

Seat: `MoriR25.MutRunwayDuplicates` (wave 2, mutation tester). Target claim: **C2 (coverage)** —
the new read-only harness-runway tool `tools/mori-job-runway.py` and its declared after-value
`MORI_JOB_RUNWAY_SELFTEST: PASS 21/21` over the frozen 21 cases, plus the co-evolved
`tools/fixtures/mori-job-runway/supplementary-cases.json` (18 cases).

Attack surface assigned: **duplicate handling** — a duplicate `maxJobs` as a direct child of the
`async` block, and a second top-level `async` key.

## Verdict

**The landed code held. The declared after-value is weakened as a detector.**

- **No false-number defect found in the shipped duplicate handling.** The tool abstains
  (`malformed` → `RUNWAY_UNKNOWN`, exit 2) on every duplicate shape I probed, and that
  abstention is the safe direction: omp's own YAML reader never errors on a duplicate key, it
  silently keeps the **last** one.
- **Two of the six mutants survive both case files**, and one of them (M6) is a real
  false-number defect against omp that **no committed case kills**.
- **The counted after-value (`PASS 21/21`) does not cover the "more than one `async` key"
  rule at all.** Mutants M3 (accept the second `async:` block) and M4 (read the last one) both
  print `PASS 21/21` and exit 0. The only thing that kills them is `R07` in the *supplementary*
  file, which contract amendment A2 explicitly excludes from the after-value
  (`contract.md:152-154`). So the declared gate cannot be read as "the duplicate-`async`
  abstention is correct".
- Severity: **medium as a coverage/calibration finding** (the counted after-value does not pin
  two of rule 1's duplicate clauses; one of them guards a false number), **low in operational
  effect on this host** (the live the operator's OMP settings file has exactly one `async:` key and one
  `maxJobs` child — verified read-only — so no duplicate shape is present here).
- The survivors are **fixture gaps, not code bugs**. The smallest fix is three co-evolved
  supplementary cases (verified below) plus a disclosure that the frozen 21 cannot certify the
  duplicate-`async` clause. The frozen file must not be touched (blob `48df844a` at `7634be75`
  is pinned by `contract.md:129-130`).

## What I did

Private clone only: `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin
/fast/scratch/hyaku/mori-r25/w2-MutRunwayDuplicates` (HEAD `07a31ae8`). The lane checkout was
**not** modified — the only file written in the lane is this report. No `jj`/`git` mutation was
run in the lane or the fleet root; `omp` was never executed (its bytes were read only by the
tool under test, and the operator's OMP settings file was read read-only).

Environment: Python 3.14.8, `python3 -I -B` throughout, `bun` 1.4.3 as the YAML-semantics
oracle. **No tool was installed or upgraded** — nothing was missing; `bun` 1.4.3 was already on
the host and is the revision the omp binary embeds (`Bun v1.4.3 (c6da4a4d3)`; the parser is
`var {JSONC: uwe, YAML: OE } = globalThis.Bun`, called as `OE.parse` — wave-1 seat
`.ufo/waves/round-25/w1/CriticC2Rules.md:48-49`).

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
never touched. The clone's `cases.json` hashes to the contract-pinned blob
`48df844a22d74a57204f55a62e54760c7038c60f` (`git hash-object`), so the frozen file I attacked
is the pinned one.

### Detectors

| id | command | expected on pristine |
|---|---|---|
| D-frozen | `python3 -I -B tools/mori-job-runway.py --selftest` | `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21`, exit 0 |
| D-supp | `python3 -I -B tools/mori-job-runway.py --selftest --cases tools/fixtures/mori-job-runway/supplementary-cases.json` | `MORI_JOB_RUNWAY_SELFTEST: PASS 18/18`, exit 0 |
| D-extra (probe only, not committed) | `python3 -I -B tools/mori-job-runway.py --selftest --cases /tmp/extra-dup-cases.json` | `MORI_JOB_RUNWAY_SELFTEST: PASS 4/4`, exit 0 |

Each mutant was applied to the pristine bytes, all three detectors were run, then the file was
restored (`git checkout -- tools/mori-job-runway.py` inside the scratch clone) and re-hashed.
One mutant at a time; no two mutants were ever live together.

## Mutants and results

All six mutation sites are in `tools/mori-job-runway.py`, function `_parse_config` (rule 1).

| id | mutation | site | D-frozen (21) | D-supp (18) | verdict |
|---|---|---|---|---|---|
| **M1** | duplicate `maxJobs`: keep the **first** | `tools/mori-job-runway.py:348-349` (`if len(values) > 1: return "malformed", None` → `values = values[:1]`) | **KILLED** — `FAIL 20/21`, `CASE J08` | survived — `PASS 18/18` | killed |
| **M2** | duplicate `maxJobs`: keep the **last** | `tools/mori-job-runway.py:348-349` (→ `values = values[-1:]`) | **KILLED** — `FAIL 20/21`, `CASE J08` | survived — `PASS 18/18` | killed |
| **M3** | a second `async:` block is **accepted** (first one read) | `tools/mori-job-runway.py:288-290` (`if len(async_lines) > 1: return "malformed", None` → `pass`) | **SURVIVED** — `PASS 21/21` | **KILLED** — `FAIL 17/18`, `CASE R07` | survivor of the counted gate |
| **M4** | a second `async:` block is accepted and the **last** one read | `tools/mori-job-runway.py:288-290` (→ `async_lines = async_lines[-1:]`) | **SURVIVED** — `PASS 21/21` | **KILLED** — `FAIL 17/18`, `CASE R07` | survivor of the counted gate |
| **M5** | duplicate `maxJobs` with the **same value** is not a duplicate | `tools/mori-job-runway.py:348-349` (→ `if len(values) > 1 and len(set(values)) != 1:`) | **SURVIVED** — `PASS 21/21` | **SURVIVED** — `PASS 18/18` | **survivor** |
| **M6** | a second `async` key is only counted as a duplicate when **both** headers are spelled `async:` (a `"async":` or `async :` second key slips through) | `tools/mori-job-runway.py:288-290` (→ count only `lines[i].startswith("async:")`) | **SURVIVED** — `PASS 21/21` | **SURVIVED** — `PASS 18/18` | **survivor** |

Mutated-file sha256 (the "before/after" of each probe):

| mutant | sha256 of `tools/mori-job-runway.py` while mutated |
|---|---|
| pristine | `5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411` |
| M1 | `e5711d18702b11b19be84513aacaa96cca7d3249ff9131211b9575c746117f4d` |
| M2 | `18dcd7e3811fa4993452f3fa0e29948782122b81376156225c146792a767d65e` |
| M3 | `46fc0b672b5177b00c833c3800f142130023740b6a60ec78c201a052f494ce22` |
| M4 | `e324917387e2b47b9d083832d460f1446243f141e89ed7f369fbbbf5dc20aff5` |
| M5 | `c9425c501edbc021afaf7d6d98ce713988e3048da2409c21f0db1d3bf567e295` |
| M6 | `d084c01c197245013ed7764b5ec4a56b7072ac7c005770957e4299ee8e004490` |

### Exact detector output for the killed mutants

M1 (D-frozen, exit 2):

```
MORI_JOB_RUNWAY_SELFTEST: FAIL 20/21
CASE J08: verdict: expected 'RUNWAY_UNKNOWN', got 'RUNWAY_AS_CONFIGURED'; exit: expected 2, got 0; configured.state: expected 'malformed', got 'set'; configured.value: expected None, got 50; effective: expected None, got 50
```

M2 (D-frozen, exit 2):

```
MORI_JOB_RUNWAY_SELFTEST: FAIL 20/21
CASE J08: verdict: expected 'RUNWAY_UNKNOWN', got 'RUNWAY_AS_CONFIGURED'; exit: expected 2, got 0; configured.state: expected 'malformed', got 'set'; configured.value: expected None, got 60; effective: expected None, got 60
```

M3 (D-supp, exit 2):

```
MORI_JOB_RUNWAY_SELFTEST: FAIL 17/18
CASE R07: verdict: expected 'RUNWAY_UNKNOWN', got 'RUNWAY_AS_CONFIGURED'; exit: expected 2, got 0; configured.state: expected 'malformed', got 'set'; configured.value: expected None, got 50; effective: expected None, got 50
```

M4 (D-supp, exit 2):

```
MORI_JOB_RUNWAY_SELFTEST: FAIL 17/18
CASE R07: verdict: expected 'RUNWAY_UNKNOWN', got 'RUNWAY_AS_CONFIGURED'; exit: expected 2, got 0; configured.state: expected 'malformed', got 'set'; configured.value: expected None, got 60; effective: expected None, got 60
```

For M3 and M4 the frozen detector printed `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21` and exited 0 —
i.e. the counted after-value was reproduced by a mutant that reports a number omp does not use.

### omp's real behaviour on the duplicate shapes (the oracle)

`bun` 1.4.3 (`Bun.YAML.parse`, the reader omp embeds), emulating omp's own read path — parse,
root must be a mapping, nested lookup `async.maxJobs`, a raw value is used only when it is a
finite number, otherwise the schema default 100 applies, then `cap = max(1, floor(min(100, base)))`:

| probe (config text) | omp base | omp cap | omp's parse result |
|---|---|---|---|
| P1 `async:\n  maxJobs: 50\n  maxJobs: 60\n` | 60 | 60 | last duplicate wins, no error |
| P2 `async:\n  maxJobs: 50\n  maxJobs: 50\n` | 50 | 50 | last duplicate wins, no error |
| P3 `async:\n  maxJobs: 50\nasync:\n  maxJobs: 60\n` | 60 | 60 | second block replaces the first |
| P4 `async:\n  maxJobs: 50\n"async":\n  maxJobs: 60\n` | 60 | 60 | same key, different spelling → last wins |
| P5 `async:\n  maxJobs: 50\nasync:\n  minJobs: 5\n` | 100 (default) | 100 | second block replaces the first → `maxJobs` gone |
| P6 `async:\n  maxJobs: 50\nasync :\n  maxJobs: 60\n` | 60 | 60 | same key, different spelling → last wins |

So omp **never errors** on a duplicate key; it keeps the last one, and a second `async` block
*replaces* the first mapping entirely (P5: `maxJobs` disappears → the default 100 applies).

### Behavioural divergence on the six probes (real `~/.local/bin/omp` as the binary)

`python3 -I -B tools/mori-job-runway.py --config <probe> --binary ~/.local/bin/omp`:

| probe | pristine (shipped) | M1 | M2 | M3 | M4 | M5 | M6 | omp's cap |
|---|---|---|---|---|---|---|---|---|
| P1 dup `maxJobs` 50/60 | `malformed` / UNKNOWN / 2 | **set 50 / exit 0** | set 60 / exit 0 | malformed | malformed | malformed | malformed | 60 |
| P2 dup `maxJobs` 50/50 | `malformed` / UNKNOWN / 2 | set 50 / exit 0 | set 50 / exit 0 | malformed | malformed | **set 50 / exit 0** | malformed | 50 |
| P3 second `async:` (plain) | `malformed` / UNKNOWN / 2 | malformed | malformed | **set 50 / exit 0** | set 60 / exit 0 | malformed | malformed | 60 |
| P4 second `"async":` | `malformed` / UNKNOWN / 2 | malformed | malformed | **set 50 / exit 0** | malformed | malformed | **set 50 / exit 0** | 60 |
| P5 second `async:` without `maxJobs` | `malformed` / UNKNOWN / 2 | malformed | malformed | **set 50 / exit 0** | absent / 100 / exit 0 | malformed | malformed | 100 |
| P6 second `async :` (spaced) | `malformed` / UNKNOWN / 2 | malformed | malformed | **set 50 / exit 0** | malformed | malformed | **set 50 / exit 0** | 60 |

Reading of that table:

- **Pristine never reports a number omp does not use.** On every duplicate shape it abstains.
- **M1, M3 and M6 are false numbers** (bold): each prints a concrete `configured`/`effective`
  with exit 0 where omp computes something else (M1: 50 vs 60; M3: 50 vs 60 and 50 vs 100 on
  P5; M6: 50 vs 60).
- **M2 and M4 agree with omp** on these shapes (last-wins): they break the *contract* (rule 1
  says a duplicate is `malformed`) but not omp's arithmetic. M4 on P5 even lands on omp's 100.
  A judge should not read M2/M4 as evidence that the shipped abstention is wrong — they are
  contract violations, not false numbers.
- The shipped abstention therefore loses information omp has (omp knows 60, the tool says
  UNKNOWN). That is the safe direction and contract A2 sanctions it explicitly
  (`contract.md:154-156`: "duplicates and flow mappings that Bun reads stay abstentions:
  `RUNWAY_UNKNOWN` is never a false number").

### Live host check (read-only)

the operator's OMP settings file contains exactly one top-level `async:` key and one `maxJobs` child
(`async:\n  maxJobs: 200`, lines 244-245; counted with a read-only scan: `async` keys 1,
`maxJobs` occurrences 1). No duplicate shape is present on this host, so **none of the six
mutants changes the live reading** — the tool reports `configured {set 200}`, clamp 100,
effective 100, `RUNWAY_CLAMPED`, exit 1 on this host under the pristine code and under every
mutant. Every finding below is therefore a **fixture/after-value** finding, not a live
misreading.

## Survivors: killing input, and whether omp's real behaviour makes it matter

### S1 — M3 / M4 (a second `async:` block is accepted) — survive the counted after-value

**Killing input (verified):** the config

```
async:
  maxJobs: 50
async:
  maxJobs: 60
```

expected `configured {state: malformed, value: null}`, `verdict RUNWAY_UNKNOWN`, `exit 2` (the
pristine tool gives exactly this; it is the shape of the committed case `R07`). M3 gives
`set 50` / `RUNWAY_AS_CONFIGURED` / exit 0; M4 gives `set 60` / `RUNWAY_AS_CONFIGURED` / exit 0.
Measured against the pristine tool with the extra probe file: M3 fails `X01, X02, X03`, M4
fails `X01`.

**Does omp's real behaviour make it matter?** Yes for M3: omp reads 60 (last wins) and the
mutant claims 50 — a false number with exit 0, i.e. a false runway claim, which is exactly the
class the wave-1 seat `CriticC2Rules.md:118` recorded for the pre-A2 tool ("two blocks; Bun
keeps the last | 60 | set 50 → `RUNWAY_AS_CONFIGURED`, exit 0 | wrong value"). Amendment A2 was
written to close that defect ("Treat a second `async:` header line as `malformed`",
`CriticC2Rules.md:124-126`), and the shipped code does close it — but **the counted after-value
cannot tell whether it is still closed**. On P5 (`async:\n  maxJobs: 50\nasync:\n  minJobs: 5`)
M3 claims 50 with exit 0 where omp computes 100 (the default), which is the most damaging shape
of the three: a tool that says "your runway is 50" on a session that runs 100.

For M4 the numbers match omp, so the operational effect is nil; it is a contract violation
(rule 1 demands `malformed` for a duplicate `maxJobs` and, by A2, for a second `async` key).

**Severity: medium (coverage/calibration).** The declared after-value `PASS 21/21` is
reproduced by a mutant that reports a false number with exit 0, so the after-value is not
evidence for the duplicate-`async` abstention. The supplementary file (R07) does kill it, but
A2 excludes that file from the after-value, so the *counted* gate is blind here.

### S2 — M6 (a second `async` key spelled differently is not a duplicate) — survives both files

**Killing input (verified):** the config

```
async:
  maxJobs: 50
"async":
  maxJobs: 60
```

expected `configured {state: malformed, value: null}`, `verdict RUNWAY_UNKNOWN`, `exit 2` (the
pristine tool gives exactly this). M6 gives `set 50` / `RUNWAY_AS_CONFIGURED` / exit 0. The
spaced spelling `async :` kills it the same way. Measured: M6 fails `X02, X03` against the
pristine tool with the extra probe file.

**Does omp's real behaviour make it matter?** Yes: omp reads 60 (the quoted key is the same key
— P4/P6 in the oracle table), so M6's 50 is a false number with exit 0. The pristine tool's
abstention is right; M6 is the wrong number.

**Severity: medium (coverage), low in operational effect.** The shape needs a config file that
carries the same key twice under two spellings — a hand-edited file, not something omp's
settings writer produces, and not present on this host. The coverage point stands: **no committed
case kills M6**, in either file, so a future regression that narrows the duplicate-`async` rule
to the exact spelling `async:` would ship silently, and it would ship a false number with
exit 0.

### S3 — M5 (duplicate `maxJobs` with the same value) — survives both files

**Killing input (verified):** the config

```
async:
  maxJobs: 50
  maxJobs: 50
```

expected `configured {state: malformed, value: null}`, `verdict RUNWAY_UNKNOWN`, `exit 2` (the
pristine tool gives exactly this). M5 gives `set 50` / `RUNWAY_AS_CONFIGURED` / exit 0. Measured:
M5 fails `X04`.

**Does omp's real behaviour make it matter?** Not for the number: omp reads 50 (last wins), so
M5's answer equals omp's. The shipped abstention is stricter than omp needs here; M5's defect is
that it contradicts rule 1 ("`malformed` … when `maxJobs` appears twice as a direct child",
`tools/mori-job-runway.py:24-25`), not that it reports a wrong cap.

**Severity: low (coverage).** The gap is that the committed fixtures pin duplicate `maxJobs`
only with *different* values (`J08`: 50 and 60). A developer who "helpfully" relaxes the check
to "duplicates that disagree" passes both suites, and the tool then claims a number for a file
the contract says it must not read. The direction is safe against omp (the number coincides),
but the rule is unpinned.

## Smallest fix (verified)

Three co-evolved cases in `tools/fixtures/mori-job-runway/supplementary-cases.json` (the frozen
`cases.json` must not change: blob `48df844a` at `7634be75` is pinned by
`.ufo/waves/round-25/contract.md:129-130`):

```json
{
  "id": "R19",
  "what": "a second async key written with a different spelling is still a second async key",
  "config": "async:\n  maxJobs: 50\n\"async\":\n  maxJobs: 60\n",
  "binary": "<the same clamp+default string the other R cases carry>",
  "expect": {
    "verdict": "RUNWAY_UNKNOWN", "exit": 2,
    "configured": {"state": "malformed", "value": null},
    "clamp": {"state": "found", "value": 100, "sites": 1},
    "setting_default": {"state": "found", "value": 100},
    "effective": null
  }
},
{
  "id": "R20",
  "what": "the same, with the spaced spelling `async :`",
  "config": "async:\n  maxJobs: 50\nasync :\n  maxJobs: 60\n",
  "binary": "<the same clamp+default string the other R cases carry>",
  "expect": {
    "verdict": "RUNWAY_UNKNOWN", "exit": 2,
    "configured": {"state": "malformed", "value": null},
    "clamp": {"state": "found", "value": 100, "sites": 1},
    "setting_default": {"state": "found", "value": 100},
    "effective": null
  }
},
{
  "id": "R21",
  "what": "two identical maxJobs children are still a duplicate",
  "config": "async:\n  maxJobs: 50\n  maxJobs: 50\n",
  "binary": "<the same clamp+default string the other R cases carry>",
  "expect": {
    "verdict": "RUNWAY_UNKNOWN", "exit": 2,
    "configured": {"state": "malformed", "value": null},
    "clamp": {"state": "found", "value": 100, "sites": 1},
    "setting_default": {"state": "found", "value": 100},
    "effective": null
  }
}
```

Measured with the equivalent cases (`X01`–`X04`, `/tmp/extra-dup-cases.json`) in the scratch
clone:

```
pristine : MORI_JOB_RUNWAY_SELFTEST: PASS 4/4
M1       : FAIL 3/4   failing ids: ['X04']
M2       : FAIL 3/4   failing ids: ['X04']
M3       : FAIL 1/4   failing ids: ['X01','X02','X03']
M4       : FAIL 3/4   failing ids: ['X01']
M5       : FAIL 3/4   failing ids: ['X04']
M6       : FAIL 2/4   failing ids: ['X02','X03']
```

So R19+R20 kill the M6 survivor, R21 kills the M5 survivor, and no other mutant regresses
(the pristine tool still passes 4/4). The M3/M4 survivors are already killed by the committed
`R07`; what is missing there is *counting*: A2 says the supplementary file "is not counted
toward the after-value" (`contract.md:152-154`), so the declared after-value stays
`PASS 21/21` and the discriminating gate has to be named explicitly (the supplementary
selftest must be run and quoted as part of the C2 evidence), or a new frozen generation has to
be cut. I am not changing the contract's wording and I did not touch the frozen file.

## Restoration evidence

- After every mutant the tool file was restored (`git checkout -- tools/mori-job-runway.py`
  inside the scratch clone) and re-hashed: sha256
  `5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411` every time — identical to
  the pristine value and to the lane's file.
- Final state of the scratch clone: `git status --porcelain` empty;
  `sha256sum tools/mori-job-runway.py` = `5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411`;
  `cases.json` = `7098b008…55fb4`, `supplementary-cases.json` = `8d09756d…9ffd6` (unchanged);
  both suites re-run on the restored bytes print `PASS 21/21` and `PASS 18/18`, exit 0.
- The scratch clone `/fast/scratch/hyaku/mori-r25/w2-MutRunwayDuplicates` (358 MB) was removed
  after the measurements.
- The lane checkout was never written to except for this report file
  (`.ufo/waves/round-25/w2/MutRunwayDuplicates.md`); the lane's `tools/mori-job-runway.py`
  still hashes to `5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411`.

## Bounds and honest limits

- Read-only on the lane except this report; all mutation happened in
  `/fast/scratch/hyaku/mori-r25/w2-MutRunwayDuplicates` (a `git clone --no-hardlinks` of the
  lane), now deleted.
- No `jj` command was run at the fleet root or in the lane; no `git add/commit/stash/checkout/
  switch/reset/pull/push` in the lane or the fleet repo; the lane Git index was not touched.
- `omp` was never executed. The installed binary was read as bytes only (the tool under test
  reads it with `--binary`); the harness's YAML semantics were taken from `Bun.YAML.parse`
  (bun 1.4.3), the parser the Bun-compiled binary embeds — a *parity* argument, not a session
  observation: I did not start a harness session.
- The `bun` oracle is bun 1.4.3 as installed on this host; the binary embeds Bun v1.4.3
  (c6da4a4d3). Same version, possibly a different build hash; the duplicate-key behaviour
  reported here is the same one wave-1 seat `CriticC2Rules.md:118` recorded with the embedded
  revision, so the two agree.
- All six mutants touch the duplicate clauses only. Other rule-1 surfaces (block scoping, comment
  handling, quoting, tabs) were probed by the sibling seat
  `.ufo/waves/round-25/w2/MutRunwayYamlScope.md`; I did not duplicate that work.
- Severity is judged against the shipped settings schema and this host's config. A deployment
  with a hand-edited the operator's OMP settings file carrying a duplicated key would hit M3/M6's
  wrong answers; nothing in the shipped tooling produces such a file.
- Tooling: no package was installed or upgraded (nothing was missing); `python3` 3.14.8 and
  `bun` 1.4.3 were already on the host. No pacman transaction was run (all pacman transactions
  are paused host-wide).
