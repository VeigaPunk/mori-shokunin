# ResidC5Drain — round 38 residual falsification of conform.py `bounded_reads`

## Scope and axes

Attacked the committed bytes of `.ufo/waves/round-38/conform.py` at landed tip
`b6993744171a05efc627b5e0664489c31aa5214e`, specifically the `bounded_reads` check that
lesson M13 hardened ("drains now carry `communicate(timeout=TOOL_GRACE_S)` in both
counters and `static_checks` parses every `communicate` call requiring `timeout=`").

Axes: (1) does the M13 hardening actually reject a counter whose drain has no timeout?
(2) is the rule's *scope* (which calls it inspects, and what it inspects of them)
equal to the contract it claims to enforce? Detection and report only; no remediation,
no change to the landed bytes, no commit to the lane.

The required `git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse mori` exited
128 (`fatal: ambiguous argument 'mori': unknown revision or path not in the working
tree.`); `jj log -r mori` likewise reports `Revision 'mori' doesn't exist`. The moving
`mori` name therefore could not be verified in this checkout; the assigned commit was
used and checked out detached in an isolated `/tmp` clone. This limits branch-name
provenance, not the committed-byte checks below.

## Method

Scratch clone: `git clone --no-local /home/vgpnk/Projects/shokunin/mori-shokunin /tmp/r38-c5drain`,
checked out detached at `b6993744`. All mutants were committed *in the clone only*;
the lane Git index and jj state were never touched.

Each mutant is a one-hunk mutation of the committed `count-c1.py` at the **third-level
drain** (`count-c1.py:130`), the `communicate` reached only after the SIGTERM drain has
already timed out and SIGKILL has been issued to the process group:

```python
            try:
                out, err = proc.communicate(timeout=TOOL_GRACE_S)
            except subprocess.TimeoutExpired:
                # bounded: a setsid descendant can hold the pipe open (r38 RevC5Bounds)
                out, err = "", ""
```

| Mutant | Mutation | Shape |
|---|---|---|
| M1 | `proc.communicate(timeout=TOOL_GRACE_S)` → `proc.communicate()` | drain with **no** timeout |
| M2 | `proc.communicate(timeout=TOOL_GRACE_S)` → `proc.communicate(timeout=UNBOUNDED_DRAIN_S)`, with `UNBOUNDED_DRAIN_S = None` added at `:81` | drain with a timeout that is **a variable that is actually unbounded** |
| M3 | `proc.communicate(timeout=TOOL_GRACE_S)` → `proc.wait(timeout=TOOL_GRACE_S)` + `out, err = proc.stdout.read(), proc.stderr.read()` | **timeout on the wrong call**; the drain is an unbounded `read()` |

Full diffs are the three hunks above; each mutant's working-tree file was verified
byte-identical to its own committed blob (`git show <rev>:<path> | sha256sum` equals
`sha256sum <path>`) for every run.

### Detector

`conform.py`'s own six checks, run twice per mutant:

* **Form A — literal required invocation** (no `--repo`; `conform.py`'s default `--repo`
  is the read-only lane):
  `python3 .ufo/waves/round-38/conform.py <mutant-rev> --counter .ufo/waves/round-38/count-c1-m<N>.py --counter .ufo/waves/round-38/count-c4.py`
* **Form B — same command with `--repo .`** (the clone), so that `<mutant-rev>` and the
  mutant file actually exist for the checker's behavioural arms.

### Independent behavioural probe (the discriminating evidence)

`conform.py`'s own `timeout_state` arm uses `fixtures/hang-after-flush.py`, which is a
plain `time.sleep(120)` child. When the counter SIGTERMs/SIGKILLs its process group the
child dies, the pipe closes, and the **third-level drain is never reached** — so no
mutation of that line can be observed by the shipped fixture.

To reach it I wrote `/tmp/r38-probe/hold-pipe.py`: it prints a summary line, flushes,
then spawns a **setsid descendant** that holds the pipe's write end open (exactly the
hazard the landed comment names: *"a setsid descendant can hold the pipe open"*), and
sleeps. Probe invocation, mirroring the checker's own `timeout_state` arm
(`--tool-timeout 3 --arms real --seed 5`) with a 45 s outer `timeout`:

```sh
timeout 45 python3 <counter> b6993744 --repo /tmp/r38-c5drain \
  --tool /tmp/r38-probe/hold-pipe.py --tool-timeout 3 --arms real --seed 5
```

## Results

### Baseline (pristine committed bytes)

`conform.py b6993744 --selftest --counter count-c1.py` → **`CONFORM_SELFTEST pass=6 fail=0`**,
exit 0 (run twice: once from the lane, once from the clone).

`conform.py b6993744 --repo /tmp/r38-c5drain --counter count-c1.py --counter count-c4.py`
→ all six checks PASS, **`CONFORM=met`**, exit 0.

### Form A — literal required invocation (default `--repo` = read-only lane)

| Mutant | rev | bounded_reads | timeout_state | CONFORM | exit |
|---|---|---|---|---|---|
| M1 | `5b16a9c6766443837afc7dea5eeeccc184cb269d` | **FAIL** (`popen=False`) | FAIL (exit=2) | `unmet` | **1** |
| M2 | `37f3f96535017e8f646d4d98d9f5528344bd0ce0` | PASS | FAIL (exit=2) | `unmet` | 1 |
| M3 | `f5a8e391db7a2c0584b43a8a65590b6acdf1a9cc` | PASS | FAIL (exit=2) | `unmet` | 1 |

M1 detail line:

```text
check bounded_reads    FAIL (count-c1-m1.py: run=True popen=False cap=True mkdtemp=True scratch=True; count-c4.py: run=True popen=True cap=True mkdtemp=True scratch=True)
```

**The assignment's required outcome holds for M1: `bounded_reads` FAILS and `CONFORM=unmet`
with exit 1**, in the literal required command form.

The `timeout_state` exit=2 in this form is an artifact, not evidence about the mutants:
the counter resolves `<mutant-rev>` inside `--repo`, and the lane does not contain the
mutant commit, so the counter exits 2 (setup error) and the arm cannot discriminate.
Form B below removes that artifact.

### Form B — same command with `--repo .` (the clone)

| Mutant | rev | bounded_reads | timeout_state | CONFORM | exit | verdict |
|---|---|---|---|---|---|---|
| M1 | `7d869875cdf0b7e23f4c5f5ebb6a8b31c26d6763` | **FAIL** (`popen=False`) | PASS | `unmet` | **1** | **killed** |
| M2 | `1e84f5248f745da284447670451937da20412636` | **PASS** | PASS | `met` | **0** | **SURVIVED** |
| M3 | `76e44b02f68be74dffcc3640e1f5e9947d8e520b` | **PASS** | PASS | `met` | **0** | **SURVIVED** |

M1 in Form B:

```text
check bounded_reads    FAIL (count-c1-m1.py: run=True popen=False cap=True mkdtemp=True scratch=True; count-c4.py: run=True popen=True cap=True mkdtemp=True scratch=True)
CONFORM=unmet
EXIT=1
```

M2 in Form B (the surviving bypass):

```text
check bounded_reads    PASS (count-c1-m2.py: run=True popen=True cap=True mkdtemp=True scratch=True; count-c4.py: run=True popen=True cap=True mkdtemp=True scratch=True)
CONFORM=met
EXIT=0
```

### Independent behavioural probe — the survivors are genuinely defective, not cosmetic

| Counter | probe exit | elapsed | observed |
|---|---|---|---|
| pristine `count-c1.py` | 1 | 13 s | `tool_timeout: tool exceeded 3s (SIGTERM, then SIGKILL after 5s)`; `C1=unmet` — **bounded** |
| M1 | **124** (killed by outer timeout) | 45 s | **HANG** — no `tool_timeout`, no `C1=` line, no output past `tool:` |
| M2 | **124** | 45 s | **HANG** |
| M3 | **124** | 45 s | **HANG** |

Pristine output (bounded): `real arm: FAIL (13.1s)` … `diff: tool_timeout: tool exceeded 3s
(SIGTERM, then SIGKILL after 5s)` … `C1=unmet`. All three mutants produced no `C1=` line
at all within 45 s: with a setsid descendant holding the pipe, the mutated third-level
drain never returns.

So M2 and M3 are **real hangs** — the same unbounded-drain hazard M13 was written to
eliminate — yet `conform.py` reports `CONFORM=met` (exit 0) on their bytes. M1 is the
only one the checker rejects.

## Finding: `bounded_reads` is a syntactic keyword-presence test, not a bound

`conform.py:117-124` implements the rule as:

```python
        if name == "communicate":
            # every drain must carry its own timeout (r38 RevC5Bounds: a setsid
            # descendant can hold the pipe open past the kill)
            saw_communicate = True
            popen_ok = popen_ok and "timeout" in kw
...
    popen_ok = popen_ok and saw_communicate
```

`kw` is `{k.arg for k in node.keywords}` — the set of **keyword names**, not their
values. Two gaps follow, and each is demonstrated above by a mutant that hangs for 45 s
yet passes the check:

1. **A timeout whose value is unbounded satisfies the rule (M2).** `timeout=UNBOUNDED_DRAIN_S`
   where `UNBOUNDED_DRAIN_S = None` has the keyword `timeout` in `kw`, so the check
   passes; at runtime `communicate(timeout=None)` blocks indefinitely. The rule never
   inspects that the timeout is a finite, non-`None` number.
2. **A drain that is not a `communicate()` call is outside the rule entirely (M3).**
   The check only fires on calls named `communicate`. Moving the drain to
   `proc.stdout.read()` (with the timeout parked on `proc.wait(...)`) leaves the
   remaining two `communicate` calls — which do carry `timeout=` — to satisfy the rule,
   while the actual drain is an unbounded `read()`. The `saw_communicate` conjunct
   (`:124`) only requires that *some* `communicate` call exists; it does not require
   that the drain be one.

Secondary observation on the same rule: the shipped `--selftest` never exercises the
`communicate`-timeout conjunct. Its `bounded_reads` mutation (`:246-248`) removes
`timeout=timeout` from the **`run(`** helper call, which flips `run_ok` (`:113`), not
`popen_ok`. So the rule that M13 hardened — "every `communicate` call requires
`timeout=`" — has no selftest coverage, and the two gaps above are invisible to the
declared `pass=6 fail=0` evidence. (M1 confirms the conjunct does fire when the keyword
is genuinely absent, so this is a coverage gap in the selftest, not a dead rule.)

## Impacted axes and smallest safe correction

The landed counter is **not** defective: the committed `count-c1.py` drains with
`communicate(timeout=TOOL_GRACE_S)` and returns `tool_timeout` in 13 s under the probe.
The finding is that the *checker* would not catch a regression of this kind, and that
the six-check `CONFORM=met` verdict is therefore weaker than the contract text implies
("bounds every child and git read by a timeout"). The `bounded_reads` arm should be
read as "every `communicate()` call carries a `timeout=` keyword", not "every drain is
bounded".

Smallest safe correction, in the checker's own idiom (not applied — this seat is
detection and report only):

* Evaluate the `timeout=` **value** rather than the keyword name: require a numeric
  literal or a name that resolves to a positive finite number, and treat `None` as a
  failure. This closes M2.
* Require that the drain *is* a `communicate()` call — e.g. reject a `stdout.read()` /
  `stderr.read()` drain, or require the `communicate` call to be the one that reads the
  child's output. This closes M3.
* Optionally extend the `--selftest` with a seventh mutation that drops the `timeout=`
  from the third-level `communicate` specifically, so the `communicate`-timeout conjunct
  is covered rather than only the `run(` conjunct.

The `count-c4.py` counter carries the same three-level drain shape
(`count-c4.py:86/93/100`, with `SELFTEST_GRACE_S`), so the same two gaps apply to it;
that mutant was not run in this seat.

## Restoration and provenance

Clone restored to `b6993744` with `git reset --hard b6993744`; the three pristine
instruments are byte-identical to their committed state and to the round-38 freeze
manifest (`evidence/freeze-r38-v3.txt` lines 17-19, as recorded by ResidFreezePins):

| File | SHA-256 after restore | Matches freeze manifest |
|---|---|---|
| `.ufo/waves/round-38/count-c1.py` | `5aa51556946a3e5293ba069a12b9e816694ea406bd11f5cb22da5e5ba7c22ea3` | yes (line 17) |
| `.ufo/waves/round-38/count-c4.py` | `8332341c3901ef09e76bbd7f31e8c8e68b4e4ecc5d3002f2d20201c9e7093ba1` | yes (line 18) |
| `.ufo/waves/round-38/conform.py` | `580a0bf15a815b5a26aed908f67a3d74f29d714b19175cee6057fb694aaeb01e` | yes (line 19) |

The lane worktree was not modified by this seat: the three instrument hashes read from
`/home/vgpnk/Projects/shokunin/mori-shokunin` are unchanged, no lane commit was made,
and the only lane write is this report. Scratch artifacts live in `/tmp/r38-c5drain`
(clone), `/tmp/r38-probe` (mutant sources, probe fixture, driver scripts).

No tools were installed or upgraded for this seat.

## Commands run (all in the /tmp clone; lane read-only)

```sh
# baseline
git clone --no-local /home/vgpnk/Projects/shokunin/mori-shokunin /tmp/r38-c5drain
git -C /tmp/r38-c5drain checkout --detach b6993744171a05efc627b5e0664489c31aa5214e
python3 .ufo/waves/round-38/conform.py b6993744 --selftest --counter count-c1.py
python3 .ufo/waves/round-38/conform.py b6993744 --repo /tmp/r38-c5drain \
  --counter .ufo/waves/round-38/count-c1.py --counter .ufo/waves/round-38/count-c4.py

# per mutant: commit the mutation, then Form A and Form B
python3 .ufo/waves/round-38/conform.py <mutant-rev> \
  --counter .ufo/waves/round-38/count-c1-m<N>.py --counter .ufo/waves/round-38/count-c4.py
python3 .ufo/waves/round-38/conform.py <mutant-rev> --repo . \
  --counter .ufo/waves/round-38/count-c1-m<N>.py --counter .ufo/waves/round-38/count-c4.py

# independent behavioural probe (per counter)
timeout 45 python3 <counter> b6993744 --repo /tmp/r38-c5drain \
  --tool /tmp/r38-probe/hold-pipe.py --tool-timeout 3 --arms real --seed 5

# restore
git -C /tmp/r38-c5drain reset --hard b6993744
sha256sum .ufo/waves/round-38/count-c1.py .ufo/waves/round-38/count-c4.py \
          .ufo/waves/round-38/conform.py
```

## Verdicts at a glance

| Mutant | Mutation | Detector verdict | Behavioural probe | Reportable status |
|---|---|---|---|---|
| M1 | `communicate()` — no timeout | **killed** (`bounded_reads` FAIL, `CONFORM=unmet`, exit 1) | HANG (45 s) | M13 hardening confirmed for this shape |
| M2 | `communicate(timeout=UNBOUNDED_DRAIN_S)`, variable = `None` | **survived** (`CONFORM=met`, exit 0) | HANG (45 s) | **coverage gap** |
| M3 | timeout on `proc.wait`, drain = `stdout.read()` | **survived** (`CONFORM=met`, exit 0) | HANG (45 s) | **coverage gap** |
