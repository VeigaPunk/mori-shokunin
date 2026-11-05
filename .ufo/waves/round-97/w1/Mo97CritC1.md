# Mo97CritC1 — critic: falsification attempt on C1 (operability)

Seat Mo97CritC1, mori round 97 w1. Measured revs: entering `973b2af11f41bd362163d7e29ac08286832f546b`, freeze `dd1ae1150f53df54e7530311b2323368e3c0e5e9`, landing `e85ed91249953094b067554bfa79fcdc65791f8e`. Scratch: `/fast/scratch/hyaku/mori-r97/Mo97CritC1` (archives via `git archive | tar -x`, `TMPDIR=$S`). Read-only git only.

## Provenance

- Frozen counter bytes intact: `sha256sum .ufo/waves/round-97/count-c{1,2}.py` → `78a09016fa8151b72049400600b6b154437c919df6fccb55b8bfa6253b4d2a95`, `957a7be605ba920734a218388b7ebb50f4f829979931c6e4193caee2149a1e91` — equal to line 1 of `evidence/controls-r97.txt`.
- `git rev-parse e85ed91^` → `dd1ae1150f53df54e7530311b2323368e3c0e5e9` (landing sits directly on the freeze).
- `git diff --stat 973b2af1 e85ed912` → SKILL.md +17 (registry section appended at EOF, no earlier byte edited), corpus/SOURCES.md +1 (S628), candidate/evidence/wave files; **no `tools/` entry** — the four tools (r62/r66/r91/r96) are byte-identical at entering and landing, so no tool-side selftest edit backs the claim.

## (a) Do-nothing and cheaper controls, run in my scratch

Baselines (reproduced first-hand, matching receipts):

```
$ count-c1.py --root $S/entering        # entering do-nothing
C1=unmet unregistered=4 registry=unmet targets_ok=0/4 checks_failed=registry,target_... root=.../entering   rc=1
$ count-c1.py --root $S/landing         # landing as-is
C1=met unregistered=0 registry=met targets_ok=4/4 checks_failed=-   rc=0   (all four stated_in_cell=yes token_in_verdict_map=yes)
```

Mutation battery (SKILL.md edits only, in scratch copies of the landing tree):

| # | Construction (attack) | Counter verdict |
|---|---|---|
| M3 | 4 truthful rows moved out of SKILL.md into side file `notes.md` | `C1=unmet unregistered=4 registry=unmet targets_ok=0/4` rc=1 — defended; rows must be in SKILL.md |
| M3b | same rows under a junk heading `# scratch notes (not the registry)` at the TOP of SKILL.md | `C1=met ... targets_ok=4/4` rc=0 — **residual R1** |
| M4 | duplicate registry name appended to the same table (junk cells) | `C1=unmet unregistered=0 registry=unmet targets_ok=3/4 checks_failed=registry,target_mori-source-digest.py` rc=1; counter prints `rows_found=2` — defended at both layers |
| M5 | junk-metadata rows: kind=`junk`, pinned values=`none`, write scope=`everything`, owner=`nobody`, verdict map=`<token> (unverified)` — but entry + verbatim true self-test line kept | `C1=met ... targets_ok=4/4` rc=0 — **residual R2** |
| M7 | true self-test line kept, false claim appended in the same cell ("this line also prints when the tool aborts") | `C1=met ... targets_ok=4/4` rc=0 — **residual R3** |

Pre-freeze controls (frozen receipt, all `AS_EXPECTED`, `CONTROLS_DONE unexpected=0`): junk rows *without* the true selftest line → `targets_ok=0/4`; rows stating a wrong outcome → `0/4`; verdict map missing the token → `3/4`; candidate rows → `met`.

Classification of the residuals: every **counted** conjunct of P1 stays truth-checked — the counter executes each tool's `--selftest` from the archive (exit 0 required), demands the verbatim final stdout line inside the self-test cell, the frozen verdict token in the verdict-map cell, exactly one attributed row with exactly 8 cells, and the pre-existing auditor's `REGISTRY=met` (which itself enforces shape, resolvable entry path, real `--selftest` argv branch, no duplicates). R1 is by-design of the *pre-existing* surface: the r44/r45 auditor treats every standard-header table in SKILL.md as registry, and the claim's stated surface is "SKILL.md (registry home)". R2/R3 falsity sits in cells/text predicate P1 never counts; the rows still state the true selftest outcome, so the operability essence ("runs and produces the stated outcome") is intact. These are counter-strength defects a future amendment could fix (pin kind/owner cells; exact-match the cell) — for the canonical judge, not grounds to reject the frozen claim. A tool-side selftest edit would defeat the counter, but is outside the claimed surface (SKILL.md rows) and provably absent from the landing diff.

## (b) Operability move, not bookkeeping

AXES.md:13 — operability: "A checklist item can be run and produces the stated outcome". The moved surface is the existing gate registry in SKILL.md audited by the existing auditor `tools/mori-gate-registry.py` (r44/r45): before, `--audit-all` fails (`unregistered=4`) — the checklist item cannot produce its stated outcome; after, it runs green with each gate's self-test outcome stated. No new artifact was created (contrast r94's sustained objection: "three new files passing their own checks is not that move" — an existing surface IS moved here). The r95 objection (predicate does not discriminate: do-nothing already met) is inapplicable — the do-nothing at entering fails. Not calibration: the deliverable is runnable gates with stated outcomes, not records about them; r96 routed defect 1 (four gates ran with no row) is repaired in place.

## (c) Host-state dependence of counted conjuncts

Conjunct (b) runs four selftests from DIR: `mori-cgroup-pressure` = fixture battery over `tools/fixtures/mori-cgroup-pressure/cases.json` (verified: `_selftest` reads only the fixture tree; `/sys/fs/cgroup` is the probe's CLI default at `mori-cgroup-pressure.py:42,238`, never opened by the selftest); `mori-source-digest` = TMPDIR fixtures; `mori-scorecard-calibration` = TMPDIR fixtures + `git` binary (fixture `git init`/commit); `mori-drift-recheck` = fixtures served on `127.0.0.1` ephemeral port (loopback only, no external network). Counter/auditor: python3 stdlib; auditor runs at `--rev WORK` and reads the archive directly. A hermetic closure needs python3 + git + loopback + writable TMPDIR; no sysctls, kernel settings, services or user limits. Empirical cross-check: my scratch runs (plain host, TMPDIR under /fast) reproduce the frozen receipt outputs byte-for-byte on the verdict lines. No counted conjunct depends on host state a closure could not reproduce.

## Checks not run

- C2 falsification (assigned to another seat); live fetch legs of C2; `--audit-all` on revs other than WORK/entering/landing; jj commands; any mutation editing `tools/` (forbidden surface, only analyzed).

VERDICT C1 holds: do-nothing fails at entering and all attempted falsities in counted conjuncts are rejected; residuals R1–R3 (placement freedom inside SKILL.md, unpoliced non-counted cells/text) are counter-strength defects outside frozen P1, reported for the canonical judge.
