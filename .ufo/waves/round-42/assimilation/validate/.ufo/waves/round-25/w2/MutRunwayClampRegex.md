# Mutation probe — C2 clamp regex in `tools/mori-job-runway.py`

Seat: `MoriR25.MutRunwayClampRegex` (wave 2, mutation tester). Target: claim C2
(`tools/mori-job-runway.py`, rule 2 `CLAMP_RE`). Probe: the clamp regex only — accept any
`Math.*` method, drop the `.get(` binding, accept a non-digit as the clamp number.

## Verdict

**WEAKENED — the claim's after-value holds, but the two case files do not pin three of the
clamp regex's discriminating properties; four of six mutants survive both detectors.**

- The tool's code is not falsified. On pristine bytes both detectors pass
  (`PASS 21/21` exit 0; `PASS 18/18` exit 0), and on this host the live run is
  `configured set 200 / clamp found 100 sites 1 / effective 100 / RUNWAY_CLAMPED`, exit 1 —
  **identical under every mutant I applied**, because the installed binary carries the clamp in
  exactly the canonical shape the regex expects.
- What is missing is fixture coverage, not correctness:
  - **KILLED** — removing the `.get(...)` binding outright (`M2b`) and capturing only the first
    digit (`M3c`).
  - **SURVIVED** — accepting any `Math` method (`M1`), making the `.get(...)` binding optional
    (`M2a`), accepting a word as the number (`M3a`), accepting any token as the number (`M3b`).
- Severity of the survivors: **medium** for `M1` and `M2a` (both can make the tool state a
  **false clamp number**, the one direction the contract forbids: "RUNWAY_UNKNOWN is never a false
  number"), **low-medium** for `M3a`/`M3b` (they mislabel the clamp state as `unreadable` and lose
  true answers; `M3b` can also report a negative clamp). **No effect on today's number**: the
  installed omp 18.12.6 spells the clamp `Math.min(100, XPe.get(R))`, so all four survivors read
  it identically.
- The after-value is therefore not falsified; the *detector* is thin. The smallest fix is four
  cases in the co-evolved `supplementary-cases.json` (not the frozen 21) — verified below: pristine
  `PASS 22/22`, each survivor killed by its own case.

## Where and how (private clone, never the lane)

- Private clone: `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin
  /fast/scratch/hyaku/mori-r25/w2-MutRunwayClampRegex` (clone HEAD
  `e5e1b7bc1c8dd3dc838585f5ebacfd1bc39e1098`). The lane checkout was never written to; the only
  lane file written is this report.
- The clone's tool bytes are identical to the lane's:
  `sha256(tools/mori-job-runway.py) = 5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411`
  in both. Fixtures: `cases.json` blob `48df844a22d74a57204f55a62e54760c7038c60f` (the contract's
  pin `48df844a` at `7634be75` — confirmed with `git rev-parse
  7634be75:tools/fixtures/mori-job-runway/cases.json`), file sha256
  `7098b008d614e84c4328af96d15badef700ea84b75a43ba4a375264a01755fb4`;
  `supplementary-cases.json` sha256
  `8d09756d10a9f501b0fa69599e096ce6ef5f3cd9debda89b5de2bc094679ffd6`.
- Detector 1 (the claim's after-value): `python3 -I -B tools/mori-job-runway.py --selftest`.
- Detector 2 (the co-evolved file): `python3 -I -B tools/mori-job-runway.py --selftest --cases
  tools/fixtures/mori-job-runway/supplementary-cases.json`.
- Baseline on pristine bytes: `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21` (exit 0) and
  `MORI_JOB_RUNWAY_SELFTEST: PASS 18/18` (exit 0). A baseline failure would have made every
  result below inconclusive; there is none.
- One mutant at a time; the clone's tool file was restored from a pristine copy after every
  mutant and the restoration was checked by sha256 and by `git status --porcelain` on the tracked
  file (empty).

## Mutants, detectors, verdicts

The mutated point is always the one literal at `tools/mori-job-runway.py:112-115`:

```python
# Rule 2: the compiled clamp site.
CLAMP_RE = re.compile(
    rb"maxRunningJobs:\s*\(\)\s*=>\s*Math\.min\(\s*(\d+)\s*,\s*[\w$]+\.get\([\w$]+\)\s*\)"
)
```

| id | mutation | detector 1 (frozen 21) | detector 2 (supplementary 18) | verdict |
|---|---|---|---|---|
| M1 | `Math\.min\(` → `Math\.[A-Za-z]+\(` — **accept any Math method** | `PASS 21/21`, exit 0 | `PASS 18/18`, exit 0 | **SURVIVED** |
| M2a | `[\w$]+\.get\([\w$]+\)` → `[\w$]+(?:\.get\([\w$]+\))?` — **drop the `.get(` binding** (made optional) | `PASS 21/21`, exit 0 | `PASS 18/18`, exit 0 | **SURVIVED** |
| M2b | `[\w$]+\.get\([\w$]+\)` → `[\w$]+` — the `.get(` binding removed outright | `FAIL 1/21`, exit 2 — first failing case **J01**: `verdict: expected 'RUNWAY_CLAMPED', got 'RUNWAY_UNKNOWN'; exit: expected 1, got 2; clamp.state: expected 'found', got 'absent'; clamp.value: expected 100, got None; clamp.sites: expected 1, got 0; effective: expected 100, got None` (every frozen case except J09 — the one whose binary has no clamp at all — fails the same way) | `FAIL 0/18`, exit 2 — first failing case **R01**: `clamp.state: expected 'found', got 'absent'; clamp.value: expected 100, got None; clamp.sites: expected 1, got 0` | **KILLED** (by J01 / R01) |
| M3a | `(\d+)` → `(\w+)` — **accept a non-digit** (a word) | `PASS 21/21`, exit 0 | `PASS 18/18`, exit 0 | **SURVIVED** |
| M3b | `(\d+)` → `([^\s,)]+)` — accept any token as the number | `PASS 21/21`, exit 0 | `PASS 18/18`, exit 0 | **SURVIVED** |
| M3c | `(\d+)` → `(\d)` — control: capture only the first digit | `FAIL 1/21`, exit 2 — first failing case **J01** (same row as M2b's) | `FAIL 0/18`, exit 2 — first failing case **R01** | **KILLED** (by J01 / R01) |

Mutated-file hashes (tool bytes only; the frozen 21 and supplementary 18 were never edited):

| id | pristine sha256 | mutated sha256 |
|---|---|---|
| M1 | `5d90d7d4…12c3411` | `5f4d2f7d8f0951234835447d7b3a974a11708b934224bb4fb3722e3f456e69da` |
| M2a | `5d90d7d4…12c3411` | `e281b5290a8b5550d0c08add5bc803094e9b089dc02b6977fb6dc10337ad4c86` |
| M2b | `5d90d7d4…12c3411` | `40c223e0b82ad69294f36b2224b920bbd59c666f2094f5306fc68a60dbcc806b` |
| M3a | `5d90d7d4…12c3411` | `5456a510b38372f785a72bfd829f0e890d72f40d18a6b3e38efa0af3dee160fc` |
| M3b | `5d90d7d4…12c3411` | `c89317ce339b9522fc03fcdca22bafa0fd64ad463970a898bbdee12dc35a734b` |
| M3c | `5d90d7d4…12c3411` | `b11a4abcb05edf46c6d741028604c8d1980558f985953d03e5e1cdd39b4ce92d` |

Restoration evidence: after the last mutant the clone's `tools/mori-job-runway.py` hashed
`5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411` (identical to pristine) and
`git status --porcelain tools/mori-job-runway.py tools/fixtures/mori-job-runway/` in the clone was
empty. The lane's tool file hashes the same `5d90d7d4…12c3411` after the probe — unchanged.

*Disclosure:* the first `M3c` run was piped through `head`, which closed the pipe early (SIGPIPE)
and killed the restore step of my runner, leaving the clone's tool file mutated (`b11a4abc…`).
The hash check caught it; the file was restored to `5d90d7d4…12c3411`, the mutant was re-applied
and both detectors were re-run to completion (frozen `FAIL 1/21`, first failing case J01;
supplementary `FAIL 0/18`, first failing case R01) and the file restored again. The lane was never
touched.

## Why the four survivors survive: what the two files actually exercise

Both case files feed the **same canonical binary shape** and never vary the three properties the
mutants attack:

- `supplementary-cases.json`: 18 cases, **1 distinct binary** — the canonical
  `maxRunningJobs: () => Math.min(100, XPe.get(R))`. All 18 vary the *config* side only (the A2
  YAML abstentions). It carries no signal at all for rule 2.
- `cases.json`: 21 cases, 8 distinct binaries — canonical (×14: J01–J08, J12, J13, J15, J16, J19,
  J20), no clamp at all (J09), two sites with different numbers (J10), two sites with the same
  number (J11), no setting default (J14), identifier/spacing variant `()=>Math.min( 100 , a$.get(b) )`
  (J17), number 300 instead of 100 (J18), two setting defaults (J21).

Every one of those eight shapes keeps `Math.min`, a literal decimal first argument and an
`X.get(Y)` second argument. So the frozen 21 pin the **captured number** (`M3c` dies) and the
**presence of the `.get(...)` call in its strict form** (`M2b` dies), but they pin neither the
**method name** (`M1` lives), nor the **presence** of the `.get(...)` binding (`M2a` lives), nor the
**digit-only class** of the captured number (`M3a`, `M3b` live).

## The survivors, one at a time

All probe runs below use the same `--config` (`async:\n  maxJobs: 200\n`) and differ only in the
binary. Pristine output is the reference.

### M1 — accept any `Math` method (severity: medium)

**What it does when it survives.** Probe P1, binary
`maxRunningJobs: () => Math.max(100, XPe.get(R))` (a `Math.max` site — the number is a *floor*,
not a cap):

```
pristine   verdict=RUNWAY_UNKNOWN exit=2 clamp=absent/None   sites=0 effective=None
M1         verdict=RUNWAY_CLAMPED exit=1 clamp=found/100     sites=1 effective=100
```

`M1` states "your configured 200 is clamped to 100" for a site whose 100 is a lower bound: the
true effective cap is `max(100, 200) = 200`. The pristine tool abstains, which is the contract's
required direction ("An absent clamp is never read as 'no clamp'", "RUNWAY_UNKNOWN is never a
false number"). `M1` breaks exactly that rule.

**Which input would kill it.** One case whose binary carries a `Math.max` clamp site, expecting
`clamp.state: "absent"`, `RUNWAY_UNKNOWN`, exit 2 (case `S19` below).

**Does omp's real behaviour make it matter?** Not on this host: the installed binary carries the
clamp exactly once, at byte offset 164406766, in the canonical form
`maxRunningJobs: () => Math.min(100, XPe.get(R))` (binary sha256
`85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4`, 256,702,432 bytes; upstream
source at v18.12.6 `sdk.ts:2282-2286`: `maxRunningJobs: () => Math.min(100,
cfgAsyncMaxJobs.get(settings))`). The live run under pristine **and** under `M1` is identical:
`configured set 200 / clamp found 100 sites 1 / effective 100 / RUNWAY_CLAMPED`, exit 1. It matters
for the next omp release: the tool exists to describe a *different* build, and the knowledge entry
already says a build that "spells the same logic differently reads as absent — a failed lookup,
not an absent clamp". Under `M1` that release would produce a false number instead of an
abstention.

### M2a — the `.get(` binding made optional (severity: medium)

**What it does when it survives.** Probe P2, binary `maxRunningJobs: () => Math.min(100, XPe)`
(the second argument is the settings *store*, not a setting read):

```
pristine   verdict=RUNWAY_UNKNOWN exit=2 clamp=absent/None   sites=0 effective=None
M2a        verdict=RUNWAY_CLAMPED exit=1 clamp=found/100     sites=1 effective=100
```

Probe P3, binary with one real site (`Math.min(100, XPe.get(R))`) **plus** one decoy site
(`Math.min(64, LIMIT)`):

```
pristine   verdict=RUNWAY_CLAMPED exit=1 clamp=found/100 sites=1 effective=100
M2a        verdict=RUNWAY_UNKNOWN  exit=2 clamp=ambiguous/None sites=2 effective=None
```

So `M2a` can (i) invent a clamp of 100 where the second argument is not a setting read, and
(ii) destroy a true answer by counting a decoy site and declaring the clamp `ambiguous`. (For
comparison, `M2b` — the killed variant — reports the *decoy's* number on probe P3:
`clamp=found/64 sites=1 effective=64`, a plain wrong number.)

**Which input would kill it.** One case whose binary's clamp site has a second argument that is
not `X.get(Y)`, expecting `clamp.state: "absent"`, `RUNWAY_UNKNOWN`, exit 2 (case `S20` below).

**Does omp's real behaviour make it matter?** Same answer as `M1`: no effect today (the real site
is `XPe.get(R)`), but the current pattern is the *only* thing standing between a future build and
a false number. Note the risk is narrow in the good direction too: if a future build hoisted the
setting into a variable (`Math.min(100, v)`), `M2a` would read 100 — which happens to be right —
while the pristine tool would abstain. `M2a`'s false-number path needs a *non-setting* identifier
in that slot, which is what P2 is.

### M3a / M3b — accept a non-digit as the number (severity: low-medium)

**What they do when they survive.** Probes P4 (`Math.min(MAX_JOBS, XPe.get(R))`) and P5
(`Math.min(0x64, XPe.get(R))`):

```
pristine   verdict=RUNWAY_UNKNOWN exit=2 clamp=absent/None     sites=0 effective=None
M3a        verdict=RUNWAY_UNKNOWN exit=2 clamp=unreadable/None sites=0 effective=None
M3b        verdict=RUNWAY_UNKNOWN exit=2 clamp=unreadable/None sites=0 effective=None
```

The verdict and the number are safe, but the **state label lies**: `clamp.state: "unreadable"`
asserts that the *binary cannot be read*, while the tool read it fine and printed its sha256 —
rule 2's `unreadable` means "the binary cannot be read". The cause is in `_binary_sites`
(`tools/mori-job-runway.py:388-397`): `int(m.group(1))` on a non-numeric group raises
`ValueError`, which the `except (ValueError, OSError)` arm converts into `"unreadable"`.

Two further effects, both measured:

- A binary that carries a literal site **and** a named-constant site
  (`Math.min(100, XPe.get(R))` plus `Math.min(MAX, Y.get(S))`) makes `M3a`/`M3b` **lose a true
  answer**, because the whole list comprehension dies on the first non-numeric group:
  ```
  pristine   verdict=RUNWAY_CLAMPED exit=1 clamp=found/100 sites=1 effective=100
  M3a        verdict=RUNWAY_UNKNOWN  exit=2 clamp=unreadable/None sites=0 effective=None
  M3b        verdict=RUNWAY_UNKNOWN  exit=2 clamp=unreadable/None sites=0 effective=None
  ```
- `M3b` (any token) accepts a signed literal: on `Math.min(-1, XPe.get(R))` it reports
  `clamp=found/-1`, `effective=1`, `RUNWAY_CLAMPED`, exit 1 — a *false number* (and a nonsensical
  one, a negative cap), where pristine reads `absent` / `RUNWAY_UNKNOWN` / exit 2:
  ```
  pristine   verdict=RUNWAY_UNKNOWN  exit=2 clamp=absent/None    sites=0 effective=None
  M3b        verdict=RUNWAY_CLAMPED exit=1 clamp=found/-1       sites=1 effective=1
  ```
  (`M3a` does not match here: `\w` does not cover the sign.)

**Which input would kill them.** `S21` below (a non-literal first argument, expecting
`clamp.state: "absent"`) kills `M3a` and `M3b`; `S22` (a negative literal) kills `M3b` outright.

**Does omp's real behaviour make it matter?** Today, no: the real clamp literal is `100`, and
every live run under `M3a`/`M3b` is identical to pristine (`clamp found 100 sites 1`,
`effective 100`, `RUNWAY_CLAMPED`, exit 1). It matters for a build that names the ceiling
(`Math.min(MAX_JOBS, …)`) — the pristine tool abstains, the mutant claims the binary is
unreadable.

### An honest note in the other direction (not a mutant finding)

The pristine pattern is tuned to the *current* shape only. The historical upstream form from the
feature commit (`476b858`, quoted in the round-25 knowledge entry U1) is
`Math.min(100, Math.max(1, settings.get("async.maxJobs") ?? 15))`. I ran that shape as a binary:
pristine **and** all four survivors report `clamp.state: "absent"`, `RUNWAY_UNKNOWN`, exit 2. The
pristine behaviour is the documented safe direction (a failed lookup, never "no clamp"), but it is
a coverage gap in the tool's upstream grounding, and no case in either file covers it.

## Live run on this host (all survivors agree with pristine)

```
$ python3 -I -B tools/mori-job-runway.py --binary ~/.local/bin/omp     # config defaults to the operator's OMP settings file
verdict RUNWAY_CLAMPED clamp {'state': 'found', 'value': 100, 'sites': 1}
                  configured {'state': 'set', 'value': 200} effective 100   exit=1
```

Byte-for-byte the same output for pristine, `M1`, `M2a`, `M3a` and `M3b`. The lane's own
knowledge entry F12 records this same live measurement.

## Smallest fix (fixtures only, no tool change)

The tool needs **no code change**: on every input above it answers correctly. The missing thing is
coverage of the clamp *shape*. Add four cases to the co-evolved
`tools/fixtures/mori-job-runway/supplementary-cases.json` (which is *not* counted toward the
after-value, so the frozen 21 and the declared after-value stay untouched):

| id | binary (the clamp site) | expect |
|---|---|---|
| `S19` | `maxRunningJobs: () => Math.max(100, XPe.get(R))` | `clamp {state: absent, value: null}`, `effective null`, `RUNWAY_UNKNOWN`, exit 2 |
| `S20` | `maxRunningJobs: () => Math.min(100, XPe)` | same as S19 |
| `S21` | `maxRunningJobs: () => Math.min(MAX_JOBS, XPe.get(R))` | same as S19 |
| `S22` | `maxRunningJobs: () => Math.min(-1, XPe.get(R))` | same as S19 |

(all with the canonical `id: "async.maxJobs" … default: 100` setting block and
`config: "async:\n  maxJobs: 200\n"`)

I wrote exactly these four cases into a candidate file outside the lane and ran both the pristine
tool and every mutant copy against it:

```
pristine                   exit=0 | MORI_JOB_RUNWAY_SELFTEST: PASS 22/22
M1-any-Math-method         exit=2 | FAIL 21/22  CASE S19: verdict: expected 'RUNWAY_UNKNOWN', got 'RUNWAY_CLAMPED'; exit: expected 2, got 1; clamp.state: expected 'absent', got 'found' …
M2a-get-binding-optional   exit=2 | FAIL 21/22  CASE S20: verdict: expected 'RUNWAY_UNKNOWN', got 'RUNWAY_CLAMPED'; exit: expected 2, got 1; clamp.state: expected 'absent', got 'found' …
M3a-accept-non-digit-word  exit=2 | FAIL 21/22  CASE S21: clamp.state: expected 'absent', got 'unreadable'
M3b-accept-any-token       exit=2 | FAIL 20/22  CASE S21: clamp.state: expected 'absent', got 'unreadable';  CASE S22: verdict: expected 'RUNWAY_UNKNOWN', got 'RUNWAY_CLAMPED'; exit: expected 2, got 1; clamp.state: expected 'absent', got 'found' …
M2b-get-binding-removed    exit=2 | FAIL 3/22   (already killed by the existing R cases)
M3c-single-digit           exit=2 | FAIL 4/22   (already killed by the existing R cases)
```

So the pristine tool agrees with the four new cases (`PASS 22/22`) and each survivor is killed by
its own case. If the lane prefers a code-side hardening instead of fixtures, the equivalent is to
keep rule 2's `unreadable` meaning "the binary cannot be read" (e.g. by catching the `int()`
conversion failure separately and reporting `absent`), but the fixtures alone close the gap, and
they close it without touching the frozen 21.

## What I did not do

- No change to the lane's tool, fixtures, contract, knowledge entry or scorecard; the only lane
  file written is this report.
- No `jj` command at the fleet root; no git write of any kind in the lane; no subagents dispatched
  (leaf seat).
- omp was never executed. The installed binary was read as bytes only (grep for `maxRunningJobs`,
  `Math.min`, the clamp regex); upstream facts are quoted from the lane's own round-25 knowledge
  entry, not re-fetched.
- The supplementary detector passed on every survivor (18/18) — it carries no rule-2 signal at
  all, because all 18 of its cases use one and the same canonical binary. Its value is entirely in
  the YAML-form abstentions (A2).
- No tool was installed or upgraded for this probe; the stock `python3` 3.14.8 and `git` on this
  host were sufficient.

## Cleanup

The 357 MB clone was removed after the run; the small probe artifacts (mutant copies, probe
binaries, the candidate cases file and the run logs) are kept outside the lane in
`/fast/scratch/hyaku/mori-r25/work/`.
