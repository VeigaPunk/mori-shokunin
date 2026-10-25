# ResCritNoHarm — round 43 residual attack on C1S's no-harm arm

Attack target: the P-C1S clause requiring "a sandbox-clone invocation of
`tools/mori-sources-appendonly.py --selftest` records rc 0 and
`MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0`" (contract.md lines 25-26;
implemented by frozen-adjacent counter `.ufo/waves/round-43/count-c1s.py`
`noharm_cwd`, which runs `[python, <clone>/tools/mori-sources-appendonly.py,
--selftest]` with `cwd=clone` and demands rc 0 plus (22, 0)).

Axes attacked: correctness (does it pass at all), stability (repeat runs),
environment independence (hostile git env, foreign cwd), hygiene (no writes
outside /tmp, no lane mutation), non-vacuity (can the selftest fail),
provenance (clone bytes == lane bytes, clone at entering tip, counter's
`--shared` clone mode).

## Setup

- Clone: `git clone --no-hardlinks` of the lane into `/tmp/rescrit43/clone`;
  HEAD = `e3a2b58f72ba3bd52a90646f7285fb85f0ee5dd2` (the contract's entering tip).
- Byte fidelity: sha256 of `tools/mori-sources-appendonly.py` identical in
  clone and lane working tree: `75af8f6fc63dc736f07c02617bed4bf6c1ad7f880ffb49849b065b4d40d8f76b`.
- Toolchain: git 2.56.0, Python 3.14.8. No packages installed; no tool
  installation needed, so no channel/version entry beyond these.

## Primary run (counter-style: cwd=clone, absolute script path)

```
$ cd /tmp/rescrit43/clone && python3 /tmp/rescrit43/clone/tools/mori-sources-appendonly.py --selftest
---STDOUT---
MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0
---STDERR---
EXIT_CODE=0
```

stdout is exactly the one marker line; stderr empty; rc 0. The 22 = 9 linear
cases + 6 dag cases + 7 r41-dag cases in the tool's selftest (verified by
reading the tool bytes; mutants below name cases from all three groups).

## Stability and independence (all green)

- 3 repeat runs: rc 0 each; all four stdout files sha256-identical
  (`e8e5f44c552dbfb3b571c2ec5f464e9b868255deaf71e8431c2a3f93ebf91d43`) — no flake, no ordering nondeterminism.
- Hostile env (`GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` pointed at the lane
  and a nonexistent index): rc 0, `pass=22 fail=0`. The gate's env-stripping
  (`_clean_env`/`_selftest_env`) holds; a caller's git redirection cannot
  skew the no-harm verdict.
- Foreign cwd (`cd /`): rc 0, `pass=22 fail=0`. The selftest is cwd-independent
  (re-executes via `os.path.abspath(__file__)`, fixtures under `tempfile.mkdtemp`).
- `--shared` clone checked out detached at the entering tip (the counter's
  actual clone mode): rc 0, `pass=22 fail=0`, same tool sha. The selftest
  never touches the clone's own git objects, so shared alternates are harmless.

## Hygiene

- With `TMPDIR=/tmp/rescrit43/tmpout`: rc 0 and the directory is empty after
  the run — fixtures are created and removed inside TMPDIR only.
- `git status --porcelain` clean in the /tmp clone after all runs and empty
  for lane `tools/` — no lane mutation, nothing written outside /tmp.

## Non-vacuity: three scratch mutants, all killed (copies in /tmp only)

- M1 deletion blindness (`deleted = sorted(set(first) - set(tip))` → `deleted = []`):
  rc 1, `MORI_SOURCES_APPENDONLY_SELFTEST pass=19 fail=3`; fails exactly the
  three deleted-row arms ("deleted row", "discarded superseder is ineligible
  at R", "discarded edit and superseder do not decide timing").
- M2 timing flip (as-of condition `and False`): rc 1, `pass=13 fail=9`; all
  nine as-of arms fail, including dag-r re-add and r41-dag-x.
- M3 loosened expectation (case "immutable edit" expected exit 1 → 0): rc 1,
  `pass=21 fail=1`, "FAIL immutable edit: exit: want 0 got 1" — expectations
  are checked against real tool output, not derived from it.

A selftest that cannot fail would make the no-harm arm unfalsifiable; all
three mutants die, so `pass=22 fail=0` is a discriminating signal.

## Residuals (bounds, not defects)

- The no-harm arm proves the gate's fixtures pass on the entering tip's bytes;
  it does not prove the gate's verdict on the lane's real `corpus/SOURCES.md`
  history (that is the round_changed/violations run, outside this arm).
- The counter greps `MORI_SOURCES_APPENDONLY_SELFTEST pass=(\d+) fail=(\d+)`
  anywhere in stdout; a chatty future tool could emit decoy lines. Today the
  tool prints exactly one line, and M3 shows the count cannot drift silently.
- Host `bc` is absent, so one wall-clock helper failed; per-run wall time
  observed ~1.2-3.7s across runs, far under any 180s child timeout.

## Verdict

The no-harm arm survived every attack vector tried: it passes byte-faithfully
at the entering tip, is deterministic, env- and cwd-independent, writes only
under TMPDIR, and is non-vacuous (3/3 mutants killed).

CONFIRMED — python3 /tmp/rescrit43/clone/tools/mori-sources-appendonly.py --selftest → stdout: "MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0", stderr: empty, exit code: 0
