# RevC5Pin — `head_pin` verification (round 38, wave 2)

Seat: `MoriR38.RevC5Pin` (reviewer, leaf). Scope: `conform.py`'s `head_pin` check and the
counter's `--pin-only` probe. Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin` (read-only;
no mutations performed — counter invocations write only under its own scratch).
Date run: 2026-10-23.

## Verdict

**PASS** — no FAIL criterion triggered.

- Printed pin is the lane tip and is 40 lowercase hex.
- The checker performs a real comparison: `head_pin` PASS requires the parsed pin to equal a
  freshly resolved `git rev-parse HEAD` (conform.py:151–153); there is no path to PASS without
  comparing.

## Printed pin

```
$ python3 .ufo/waves/round-38/count-c1.py --pin-only --repo /home/vgpnk/Projects/shokunin/mori-shokunin
head_at_measurement=f725f3076972e6e70595b5ac8279be524a111ff8
EXIT=0
```

`f725f3076972e6e70595b5ac8279be524a111ff8` — 40 chars, all lowercase hex. Format enforced both
by git's output and by the checker's regex `^head_at_measurement=([0-9a-f]{40})$`
(conform.py:149), anchored and lowercase-only.

## rev-parse values (all run 2026-10-23)

| command | output |
|---|---|
| `git -C <lane> rev-parse f725f3076972e6e70595b5ac8279be524a111ff8` | `f725f3076972e6e70595b5ac8279be524a111ff8` |
| `git -C <lane> rev-parse HEAD` | `f725f3076972e6e70595b5ac8279be524a111ff8` |
| `git -C <lane> rev-parse master` | `f725f3076972e6e70595b5ac8279be524a111ff8` |
| `git -C /home/vgpnk/Projects/shokunin rev-parse master` (fleet repo) | `2d723a1ccf92680308824ef1f9635ebdac5a6d9d` |

Lane HEAD is **detached** at the scored tip (`symbolic-ref HEAD` → `HEAD`; `.git/HEAD` contains
the raw sha). `master` in the lane also points at the scored tip, so pin == HEAD == master ==
scored tip. (The fleet repo's `master` is a different commit in a different repository; the
check compares against the lane's HEAD via `--repo`, which defaults to the lane —
conform.py:37, 151.)

## Non-tip behaviour — `--pin-only` ignores the positional rev

`count-c1.py:950-952`:

```python
if args.pin_only:
    print("head_at_measurement=%s" % git_out(repo_abs, "rev-parse", "HEAD").strip())
    return 0
```

The pin is a **live `rev-parse HEAD` read of `--repo`**, evaluated at call time; `args.rev` is
never consulted. Measured:

| invocation | output | exit |
|---|---|---|
| `count-c1.py e37dcc6 --pin-only` | `head_at_measurement=f725f30…1ff8` | 0 |
| `count-c1.py --pin-only e37dcc6` (rev after flag) | `head_at_measurement=f725f30…1ff8` | 0 |
| `count-c1.py daa1d4d --pin-only` | `head_at_measurement=f725f30…1ff8` | 0 |
| `count-c1.py bogusrev --pin-only` | `head_at_measurement=f725f30…1ff8` | 0 |
| `count-c1.py --pin-only --repo /tmp/nonexistent-repo-xyz` | setup error to stderr | 2 |

So yes: given a non-tip revision (or a garbage one), it still prints the lane tip — the
revision is entirely ignored by the probe. That is the declared semantics ("the lane tip it
measured", P-C5; "the lane tip the drawn arm drew from, R2", count-c1.py:15), and the checker's
`head_pin` check itself never passes a rev to the probe (conform.py:146).

The same live-HEAD read backs all six `head_at_measurement` print sites in the counter
(count-c1.py:951, 997, 1008, 1035–1036, 1125) — no divergent print site.

## Full checker run

```
$ python3 .ufo/waves/round-38/conform.py f725f3076972e6e70595b5ac8279be524a111ff8 \
    --counter .ufo/waves/round-38/count-c1.py --counter .ufo/waves/round-38/count-c4.py
check predicate        PASS (exit=0 equal=True)
check head_pin         PASS (pin=f725f3076972e6e70595b5ac8279be524a111ff8 tip=f725f3076972e6e70595b5ac8279be524a111ff8)
check tool_resolve     PASS (…)
check bounded_reads    PASS (…)
check timeout_state    PASS (…)
check scratch          PASS (…)
CONFORM=met
EXIT=0
```

`head_pin` detail line shows `pin=` and `tip=` both `f725f30…1ff8` — the comparison populated
both sides; nothing blank or skipped.

## Honest-comparison analysis (conform.py:146–154)

```python
proc = run([sys.executable, first, "--pin-only", "--repo", repo], timeout=30)
pin = <regex match on proc.stdout or None>
tip_proc = run(["git", "-C", repo, "rev-parse", "HEAD"], timeout=30)
tip = tip_proc.stdout.strip() if tip_proc is not None else ""
results["head_pin"] = (proc is not None and proc.returncode == 0 and pin == tip, …)
```

- PASS requires: probe ran (not None), exit 0, regex matched a 40-hex pin, **and**
  `pin == tip` where `tip` is an independent `git rev-parse HEAD` issued by the checker itself
  — not the pin re-echoed. If git fails or repo is bad, `tip` is `""`/missing and a 40-hex pin
  cannot equal it → FAIL. If the probe times out (`run` → None) → FAIL.
- Selftest covers this check: the `head_pin` mutation renames the label to `head=%s`
  (conform.py:218–219) so the regex misses and only `head_pin` flips to FAIL.
- `rev-parse HEAD` output is always a 40-char lowercase hex (or fails); no case/truncation
  ambiguity is possible on the comparison path.

## Residual risk (informational, not a FAIL)

- **Tip-drift window.** Both sides of the comparison are live `rev-parse HEAD` reads. If the
  lane tip advanced after the scored run but before the check, the pin and tip would advance
  together and the check still passes — `head_pin` verifies that the pin mechanism reports the
  *current* lane tip, not that the pinned value equals the evaluated `rev`. In the current
  state HEAD == master == scored tip, so the printed pin coincides with the scored tip;
  `conform.py` is always invoked with the scored tip as `rev` per the contract, and a lane that
  moved its tip mid-round would self-consistently pin the new tip. This is inherent to
  "pin the tip" semantics and matches the frozen P-C5 wording; flagged only as the boundary of
  what the check proves.
- **Dirty working tree** (observed: `git status` shows modified evidence/spec files) does not
  affect `rev-parse HEAD`; pin is commit identity only.

## Tooling

No installs or upgrades performed. Existing `python3` and `git` sufficed.

Report: .ufo/waves/round-38/w2/RevC5Pin.md
