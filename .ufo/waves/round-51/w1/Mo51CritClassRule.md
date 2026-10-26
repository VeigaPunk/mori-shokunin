# Mo51CritClassRule — attack on v5 env/stale classification

Seat: Mo51CritClassRule (critic, leaf). Item: attack the env/stale rule of pin-check v5
("no tally line for the prefix => env; any tally that differs, or an exit code contradicting it => stale").
Frozen counters are untouched; this report names misclassification cases and the right class for each.

Tool measured: `tools/mori-pin-check.py` v5 at data commit `87e0c374` (verified byte-identical at
working-tree HEAD `b504cb17`: `git diff 87e0c374 HEAD -- tools/mori-pin-check.py` is empty).
Every run below is `python3 …/tools/mori-pin-check.py --root <fixture> --repo <scratch> [--timeout N]`
in scratch `/fast/scratch/hyaku/mori-r51/Mo51CritClassRule/` with a one-row fixture SKILL.md, per the seat spec.

## Mechanism under attack (v5, tool lines)

- `run_cmd` (lines 539-559): timeout → `(None, "timeout")`; exec OSError → `(None, "oserror: …")`.

  subprocess.run raises `TimeoutExpired` before any stdout is read, so ALL output of a timed-out
  instrument is discarded.
- Tally extraction (lines 805-807):

  `tails = {l.strip()[len(prefix):].strip() for l in text_out.splitlines() if re.match(prefix…)…}`
  `observed = tails.pop() if len(tails) == 1 else None`

  `observed` is `None` in TWO different situations: zero prefix lines, **and** ≥ 2 distinct
  prefix lines (disagreeing tallies).
- Class decision (lines 818-826): `kind = "env" if observed is None else "stale"`. The decision
  keys on output shape, never on why the run failed. Suggestion 1's discriminator was the failure
  cause; see §Compare.
- The tool's own selftest bakes these in (lines 1433-1457): `v5_class_env_setup_error`,
  `v5_class_env_timeout`, `v5_class_stale_tally`, `v5_class_stale_digest`. So the behavior below
  is intended; my findings are about what it misreports.

## Compare: considerthese/2026-10-26.md suggestion 1 (lines 47-50)

> "Split pin-check mismatches into 'can't run here' and 'stale'. In my daily run, tag a mismatch as
> environmental when the pinned command exits with a setup error or a missing absolute path, and as stale
> when it runs and prints a different tally."

The suggestion's discriminator is **where the command failed**. v5 implements it as **whether a tally
line appeared**. Those agree in the two suggestion shapes (setup error, no tally → env; prints different
tally → stale) but diverge for every case below: a crash-after-printing is "missing absolute path" per
the suggestion yet v5 says stale; a wrong-tally-then-timeout is "runs and prints a different tally" yet
v5 says env.

## Evidence (all runs, verbatim)

Control — matching pin (rc 0):

```
pin line=3 kind=tally prefix=HONEST_SELFTEST state=match pinned='pass=1 fail=0' observed='pass=1 fail=0' rc=0 cmd='python3 tools/honest.py --selftest'
PIN_CHECK=met … env=0 stale=0
rc=0
```

### Case A1 — prints a partial tally, then crashes on a missing host path  → v5: **stale**, right: env

Fixture `partcrash` prints `PARTO_SELFTEST pass=1` (no `fail=0`), flushes, then opens
`/nonexistent/mori-host-path-guard` → rc 1.

```
pin line=3 kind=tally prefix=PARTO_SELFTEST state=mismatch pinned='pass=1 fail=0' observed='pass=1' rc=1 cmd='python3 tools/partcrash.py --selftest' class=stale
PIN_CHECK=unmet … env=0 stale=1
rc=1
```

The crash cause is a missing absolute host path — the suggestion's own "environmental" case — but the
partial tally line makes v5 emit `stale` (and `stale=1`). The pin text is not shown to be outdated;
the instrument never finished.

### Case A2 — prints the complete correct tally, then crashes on a missing host path → v5: **stale**, right: env

Fixture `partcrash_full` prints `PARTF_SELFTEST pass=1 fail=0` (exactly the pinned text), flushes, then
crashes on `/nonexistent/mori-host-path-guard` → rc 1.

```
pin line=3 kind=tally prefix=PARTF_SELFTEST state=mismatch pinned='pass=1 fail=0' observed='pass=1 fail=0' rc=1 cmd='python3 tools/partcrash_full.py --selftest' class=stale
PIN_CHECK=unmet … env=0 stale=1
rc=1
```

Here the tally matched; the rc-contradiction arm (line 816) demotes it to `stale`. The pin text is
current — the failure is the missing host path. Same root cause as case A1 and as the round-50
conform.py setup error (which prints no tally and so is correctly `env`); opposite classes purely
because of whether one tally line appeared before the crash.

### Case B — timeout after printing a wrong tally → v5: **env**, right: stale

Fixture `sloowrong` prints `SLWR_SELFTEST pass=9 fail=0` (a different tally), flushes, then sleeps 60 s.
Run with `--timeout 2`.

```
pin line=3 kind=tally prefix=SLWR_SELFTEST state=mismatch pinned='pass=1 fail=0' observed=None rc=None cmd='python3 tools/sloowrong.py --selftest' class=env
PIN_CHECK=unmet … env=1 stale=0
rc=1
```

The instrument ran here and printed a different tally — the suggestion's stale case verbatim. `run_cmd`
discards the captured output on timeout (line 554-555), so the direct evidence of drift is lost and the
record says env. (Also note the tool's `v5_class_env_timeout` selftest arm only ever tested a timeout
with no tally; it never tested timeout-with-a-tally.)

### Case C — two tally lines that disagree → v5: **env**, right: stale

Fixture `two` prints `TWO_SELFTEST pass=1 fail=0` then `TWO_SELFTEST pass=2 fail=0`, rc 0.

```
pin line=3 kind=tally prefix=TWO_SELFTEST state=mismatch pinned='pass=1 fail=0' observed=None rc=0 cmd='python3 tools/two.py --selftest' class=env
PIN_CHECK=unmet … env=1 stale=0
rc=1
```

`len(tails) == 2` → `observed=None` → env, even though the instrument plainly ran on this host (rc 0)
and even when one of the two lines equals the pinned text. Disagreeing tallies are drift evidence —
the pin cannot be trusted, the environment is fine. A partitioned/flaky instrument that prints one
line per shard or phase under the same prefix flips daily into `env`. Note the asymmetry: two lines
that agree on a wrong value → `stale` (observed = wrong tail); two lines that disagree → `env`.

### Case D — instrument file deleted in a later revision → v5: **env**, right: no_command/stale

Fixture `gone` pins `python3 tools/gone.py --selftest`; `tools/gone.py` does not exist in the measured
tree (as if removed by a later revision). rc 2, python's "can't open file" on merged stderr.

```
pin line=3 kind=tally prefix=GONE_SELFTEST state=mismatch pinned='pass=1 fail=0' observed=None rc=2 cmd='python3 tools/gone.py --selftest' class=env
PIN_CHECK=unmet … env=1 stale=0
rc=1
```

This is a content regression: every host fails identically, so it is not environmental. The tool's own
X1 rule (lines 749-752, 777-780) already reserves `no_command` for a binding that fails to resolve —
but X1 only fires at bind time (argv_ok/`norm is None`), and a well-formed argv naming a deleted file
sails past it into `run_cmd`, where the ENOENT becomes `env`. Deleted instrument, `env`; deleted
instrument, `no_command` — the same fact, two classes, depending only on the argv shape.

### Case E1 — import error from a missing (host) Python module → v5: **env**, right: env

Fixture `impsy` does `import zzz_no_such_module_9182` → ModuleNotFoundError, rc 1, no tally.

```
pin line=3 kind=tally prefix=IMPSY_SELFTEST state=mismatch pinned='pass=1 fail=0' observed=None rc=1 cmd='python3 tools/impsy.py --selftest' class=env
PIN_CHECK=unmet … env=1 stale=0
rc=1
```

Correct: a host-side dependency absence means the instrument could not run here.

### Case E2 — import error from a missing repo-local module → v5: **env**, right: stale/no_command

Fixture `imprepo` does `import lanewide_helper` where `tools/lanewide_helper.py` is absent from the
measured tree (deleted in a later revision). rc 1, no tally. Output is byte-identical in shape to E1:

```
pin line=3 kind=tally prefix=IMPREPO_SELFTEST state=mismatch pinned='pass=1 fail=0' observed=None rc=1 cmd='python3 tools/imprepo.py --selftest' class=env
PIN_CHECK=unmet … env=1 stale=0
rc=1
```

An ImportError text cannot tell host-level (site-packages) from repo-level (sibling module) origin.
v5 does not resolve the missing name against the measured tree, so a repo regression is reported as an
environment problem. Right class: stale/no_command (content regression).

## Summary table

| # | scenario | v5 prints | v5 class | right class |
|---|---|---|---|---|
| control | exact tally, rc 0 | match, met | — | — |
| A1 | partial tally → crash on missing host path | `observed='pass=1' rc=1` | stale | env |
| A2 | complete correct tally → crash on missing host path | `observed='pass=1 fail=0' rc=1` | stale | env |
| B | timeout after wrong tally | `observed=None rc=None` | env | stale |
| C | two disagreeing tallies, rc 0 | `observed=None rc=0` | env | stale |
| D | instrument deleted in later revision | `observed=None rc=2` | env | no_command/stale |
| E1 | ImportError, host module | `observed=None rc=1` | env | env |
| E2 | ImportError, repo module | `observed=None rc=1` | env | stale/no_command |

Root cause of all five misclasses: the class decision (lines 818-826) sees only the boolean
"did exactly one tally line appear"; the failure cause, the exit code (except as a pass/fail
demoter), and whether the missing object resolves inside the measured tree are never consulted.
`observed=None` conflates: no output, timeout (output discarded), tally disagreement, run-C error,
and import failure. And any run that died after printing a tally is always stale, even when the
death was the missing host path.

## Named limit for the round report (no counter change proposed — counters are frozen)

P-C1 arm C's five-row fixture covers only: no-tally pins → env, different-tally → stale,
rc-contradicting → stale, matching → no class. The frozen rule as written cannot express:
ran-here-but-discordant (C), ran-here-printed-different-then-timed-out (B), content-regression
(D, E2), and post-tally environmental death (A1/A2). If the L1 later revises v5 (outside this
round), the smallest safe correction is to separate `observed=None` into (a) rc 0 + no tally,
(b) ≥2 distinct tails, (c) timeout, (d) exec/resolution failure, and to resolve ENOENT/ImportError
names against the measured tree before calling the failure environmental.

## Findings

- **HIGH** — `tools/mori-pin-check.py` lines 818-826: a deleted instrument file (fixture `gone`)
  is classed `env`; X1's own `no_command` (lines 749-752) covers only bind-time failure. Content
  regressions are reported as host problems and hidden from drift reporting.
- **HIGH** — lines 818-826: a mismatch whose tally line exists is always `stale`, even when the run
  died on a missing host path (fixtures `partcrash`, `partcrash_full`). The round-50 conform.py
  setup-error shape (no tally) is `env`; the same failure preceded by one tally line is `stale` —
  the env/stale split does not track the cause the suggestion named.
- **MED** — lines 805-807 + 818-826: two disagreeing tally lines collapse to `observed=None` →
  `env` (fixture `two`), discarding direct drift evidence; a partitioned instrument printing one
  tally per shard is permanently env.
- **MED** — lines 554-555: timeout discards all printed output, so a wrong-tally-then-timeout is
  classed `env` (fixture `sloowrong`) although the instrument ran and printed a different tally.
  The `v5_class_env_timeout` selftest arm (line 1445-1447) never exercises timeout-with-a-tally.
- **MED** — lines 818-826: ImportError of a repo-local module (fixture `imprepo`) is classed `env`
  identically to a host module absence (fixture `impsy`); the origin is not resolved against the
  measured tree.
- **LOW** — suggestion-1 wording vs implementation: the suggestion discriminates on failure cause
  ("setup error or missing absolute path" vs "runs and prints a different tally"); v5 discriminates
  on output shape. Cases A, B, C, D, E2 are where the two disagree.
