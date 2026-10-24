# RevC4WitnessControl — wave-2 re-derivation of the C4 discrimination control

**Verdict: PASS.** The fabricated-witness control discriminates exactly as claimed: the
round-37 token counter accepts the witness sandbox (`C2=met`, exit 0), the round-38
content counter rejects it (`C4=unmet`, exit 1), and the sandbox cannot be mistaken for
the lane on path, author, or title. **The wave-1 Medium `--out` escape finding persists**
at the scored tip and was re-demonstrated, not re-read.

## Pin verification

- `git rev-parse HEAD` → `f725f3076972e6e70595b5ac8279be524a111ff8` (working tree at the scored tip).
- `git status --porcelain` and `git diff f725f30` over `count-c4.py`, `count-c2.py`, and
  `fixtures/` → clean; the executed counters and fixture are the pinned bytes.

## Commands run (all this session, lane cwd)

1. Sandbox build:
   `python3 .ufo/waves/round-38/fixtures/make-witness-sandbox.py f725f3076972e6e70595b5ac8279be524a111ff8 --out .ufo/waves/round-38/scratch/RevC4WitnessControl/witness-sandbox`
   → sandbox commit `ec37920c88a2912c260e19f0468f3799415703d1`.

2. R37 counter:
   `python3 .ufo/waves/round-37/count-c2.py ec37920c88a2912c260e19f0468f3799415703d1 --repo <sandbox>`
   → all eight checks PASS (`tool_present`, `selftest`, `cap_kill`, `redirect_kill`,
   `knowledge` rows=['S221'], `capability`, `readme`, `live`); **`C2=met`, exit 0**.

3. R38 counter:
   `python3 .ufo/waves/round-38/count-c4.py ec37920c88a2912c260e19f0468f3799415703d1 --repo <sandbox>`
   → the three fabricated witnesses each printed `rejected`; `anchors` PASS (3/3),
   `capability` FAIL (`missing=['evidence/no-such-receipt.txt']`), `live_rows` FAIL
   (`named=0 summary_drifted=10`), `named_row_drift` PASS, `drift_kill` PASS
   (mutated `row_states=FAIL` flipping S103 excerpt→drifted); **`C4=unmet`, exit 1**.

The r38 counter fails the sandbox on the two checks that require content the tokens
cannot supply (resolvable capability path, per-row live receipt) while passing the checks
that bind real structure — the control isolates each witness as designed.

## Sandbox identity evidence (cannot be mistaken for the lane)

| signal | sandbox | lane | distinct? |
|---|---|---|---|
| path | `.ufo/waves/round-38/scratch/RevC4WitnessControl/witness-sandbox` (inside the contract-designated scratch area, not lane root) | `/home/vgpnk/Projects/shokunin/mori-shokunin` | yes |
| author/committer | `mori witness <witness@shokunin.invalid>` (fixture lines 52-53; observed `git log -1`) | `mori-shokunin <mori@shokunin.local>` | yes |
| title | `fabricated token-satisfying binding (control)` | `round-38: C1 counter v4.1 + freeze v2 pins, C4 byte-capped reads, wave-1 spec/dispatch, attempt-2 evidence` | yes |
| lineage | `HEAD` parent exactly `f725f30`, detached HEAD, changed paths exactly the three substitution targets | — | control shape correct |

Caveat (carried from wave-1, re-observed): `origin` is the lane path and
`.git/objects/info/alternates` → the lane's object store; a consumer identifying a repo
solely by `origin` URL could confuse source with identity. This is a shared-clone
property, not impersonation of the lane's own identity signals.

Determinism note: the escape-demonstration build (below) produced the same commit
`ec37920c88a2912c260e19f0468f3799415703d1` — the witness commit is fully deterministic
(fixed parent, tree, author, message; same-second timestamp), so two sandboxes built the
same second collide on sha. Harmless here; worth one line for provenance hygiene.

## Medium finding: `--out` escape — PERSISTS at f725f30

Wave-1 `SentWitnessSandbox.md` found: `--out` is used verbatim
(`make-witness-sandbox.py:47-48`: `out = args.out or tempfile.mkdtemp(...)`), with no
canonicalisation or containment check against the lane scratch root, and `FIXTURES`
stays bound to `DEFAULT_LANE` (line 22-23) even when `--lane` is overridden.

Re-demonstrated this session:
`python3 make-witness-sandbox.py f725f30 --out /tmp/tmp.c8UlpZoReg-RevC4WitnessControl-escape`
→ the builder cloned and committed a complete sandbox **outside** the lane scratch tree
(`test -d $ESCAPE_OUT/.git` confirmed). The code path is unchanged at the scored tip;
the finding stands verbatim. Smallest fix remains: canonicalize `out` and reject unless
beneath canonical lane scratch; derive `FIXTURES` from the selected `--lane`.

## Bounds, installs, blockers

- Files written: this report plus scratch sandboxes under
  `.ufo/waves/round-38/scratch/RevC4WitnessControl/` and `$TMPDIR` (sanctioned areas).
  No lane files edited; no git mutations in the lane repo.
- No tool installs or updates performed; system `git`/`python3` sufficed.
- No blockers.
