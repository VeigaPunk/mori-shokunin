# w1 / RevC2Arms — drift selftest + both mutations, by hand

Scope: re-run `tools/mori-source-drift.py --selftest` unmutated, then kill each named fetch
policy in a scratch copy and confirm the selftest fails with exit 1. Lane repo untouched
(runs were read-only; mutants are copies under `/fast/scratch/hyaku/mori-r37/RevC2Arms/`).
No tools installed; nothing to record under the tooling directive.

## Command 1 — unmutated (lane tip e57c58b, read-only run)

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin && python3 tools/mori-source-drift.py --selftest; echo EXIT=$?
```

Observed:

```
selftest exit_code            PASS
selftest row_states           PASS
selftest summary              PASS
selftest huge_cap             PASS
selftest redirect_private_refused PASS
selftest missing_sources_exit2 PASS
MORI_SOURCE_DRIFT_SELFTEST: PASS (6 cases)
EXIT=0
```

Holds: PASS on all 6 cases, exit 0.

## Command 2 — mutant A, 4 MiB read cap removed

Copy `mori-source-drift.py` → `mutant-a-memsize.py`; single-line diff vs lane file:
`FETCH_MAX_BYTES = 4 * 1024 * 1024` → `FETCH_MAX_BYTES = 1 << 40` (line 54). Verified by
`diff` that this is the only changed line.

```
python3 /fast/scratch/hyaku/mori-r37/RevC2Arms/mutant-a-memsize.py --selftest; echo EXIT_A=$?
```

Observed:

```
selftest exit_code            PASS
selftest row_states           FAIL (got=[..., ('S109', 'excerpt'), ...] want=[..., ('S109', 'unavailable'), ...])
selftest summary              FAIL (summary=('10', '2', '2', '1', '3', '2'))
selftest huge_cap             FAIL (over_cap=body at_cap=body len=4194304)
selftest redirect_private_refused PASS
selftest missing_sources_exit2 PASS
MORI_SOURCE_DRIFT_SELFTEST: FAIL (3/6)
EXIT_A=1
```

Named arm `huge_cap` FAILs, exit 1. The other named arm `redirect_private_refused` stays PASS.

## Command 3 — mutant B, post-redirect public-destination check removed

Copy `mori-source-drift.py` → `mutant-b-redirect.py`; single-line diff vs lane file:
`if not _public_redirect_target(final):` → `if False:` (line 158). Verified by `diff` that
this is the only changed line.

```
python3 /fast/scratch/hyaku/mori-r37/RevC2Arms/mutant-b-redirect.py --selftest; echo EXIT_B=$?
```

Observed:

```
selftest exit_code            PASS
selftest row_states           FAIL (got=[..., ('S110', 'fresh'), ...] want=[..., ('S110', 'unavailable'), ...])
selftest summary              FAIL (summary=('10', '3', '1', '1', '3', '2'))
selftest huge_cap             PASS
selftest redirect_private_refused FAIL (redirect_to_loopback=body)
selftest missing_sources_exit2 PASS
MORI_SOURCE_DRIFT_SELFTEST: FAIL (3/6)
EXIT_B=1
```

Named arm `redirect_private_refused` FAILs, exit 1. The other named arm `huge_cap` stays PASS.

## Analysis

- Discrimination holds: mutant A kills `huge_cap` and leaves `redirect_private_refused`
  green; mutant B is the mirror image. Each policy (4 MiB bounded read; post-redirect
  public-destination check) is killed by its own mutation and only by it — P-C2's
  "each of those arms fails in a copy with its policy removed" (contract.md:60-62) is
  satisfied by direct observation.
- The literal phrase "FAIL exactly its own named arm" is not a singleton kill: each mutant
  fails 3 of 6 cases. Both collateral failures are corpus bindings of the same removed
  policy, not independent breakage: S109 is the over-cap-body row (`unavailable` expected)
  dying with mutant A, S110 is the 302→loopback row (`unavailable` expected) dying with
  mutant B — exactly the "the corpus binds them" half of claim C2 (contract.md:55-56).
  `summary` fails downstream of the same row misclassifications (mutant A counts S109 as
  excerpt: ('10','2','2','1','3','2'); mutant B counts S110 as fresh: ('10','3','1','1','3','2')).
  The committed counter's own kill checks (evidence/c2-after.txt: `cap_kill PASS
  huge_cap=FAIL`, `redirect_kill PASS redirect_private_refused=FAIL`) gate the same
  named-arm property, so this behavior is in-contract.
- Scratch copies diff clean against the lane tool except the one intended line each, so the
  kills are attributable to the mutations alone.

## Residual risk / verification gaps

- Only the two policies named in P-C2 were mutation-tested; other selftest arms
  (`exit_code`, `missing_sources_exit2`) have no dedicated kill in this check (out of my
  slice; the counter does not require them).
- `huge_cap` probes the boundary directly: `/huge` serves 4 MiB + 64 bytes (must grade
  `unavailable`) and `/big` serves exactly 4 MiB (must grade `body`, len 4194304), with the
  frozen cap repeated as a literal in the selftest (scratch line 402: "a mutated cap must
  not resize this fixture"). Mutant A's observed `over_cap=body at_cap=body len=4194304`
  shows the cap+1 detection is exercised, not extrapolated. S109's on-disk fixture copy
  (`b"x" * 100`, scratch line 339) is only the local file; the over-cap body is the remote
  `/huge` route.

VERDICT: PASS
