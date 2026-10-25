# MutV2Rebound — w2 mutation probe of `tools/mori-pin-check.py` v2 (round 47)

Seat: MutV2Rebound (leaf, no subagents dispatched). Date: 2026-10-25.
Subject: the v2 bytes at T = `68d66ca53d89be5c34a62f46af7c37449d9f9b63`, extracted with
`git show 68d66ca…:tools/mori-pin-check.py` into
`.scratch/r47w2-MutV2Rebound/v2-pristine.py` — sha256 `9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6`, 32259 bytes.
No tracked lane path was ever passed to an edit tool; every mutation is a scratch copy
(`mut-a.py`, `mut-b.py`, `mut-b2.py`, `mut-c.py`, `mut-c2.py`). Lane HEAD before and after
all probes: `68d66ca…` (T); `git status --porcelain -- tools/mori-pin-check.py SKILL.md` → empty.
Environment: host python3 (3.14), cwd = `/home/vgpnk/Projects/shokunin/mori-shokunin`,
`TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-MutV2Rebound` on every tool run.
No tool installs or updates were performed (operator rule: nothing to record).

## Baseline (pristine legs)

- `TMPDIR=$S python3 $S/v2-pristine.py --selftest` → rc=0, `PIN_CHECK_SELFTEST pass=34 fail=0` (`selftest-v2-pristine.log`).
- Claim-shaped detector (canonical shape, explicit `--repo`):
  `TMPDIR=$S python3 $S/v2-pristine.py --repo /home/vgpnk/Projects/shokunin/mori-shokunin --rev 68d66ca… --baseline-rev 2d85e33d… --min-tally-pins 26`
  → rc=0, `PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 min_tally_pins=26 rev=68d66ca… baseline=yes` (`claim-v2-pristine.log`).
  The C1 calibration claim is thereby reproduced independently on the v2 bytes: met, 28 tally pins ≥ 26 floor, dropped=0, rebound=0.

## Mutant (a) — remove `counts["rebound"] == 0` from `met`

- Mutation (mut-a.py, sha256 `e4db688d946ba94f9fb74e00625c76091dbbfa9bbd76736fcf7208d78df1d7a7`):
  line 386 `and counts["rebound"] == 0 and counts["duplicate"] == 0` → `and counts["duplicate"] == 0`.
- Expected detector: the two `--selftest` rebound arms must fail (rebound still counted, no longer gating).
- Output: `--selftest` → rc=1, `PIN_CHECK_SELFTEST pass=32 fail=2`; the two FAIL lines:
  - `FAIL v2_rebound_to_other_tool  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=1 duplicate=0 min_tally_pins=1 rev=deadbeef baseline=yes`
  - `FAIL v2_entry_rebound  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=1 duplicate=0 min_tally_pins=1 rev=deadbeef baseline=yes`
- Ticket-specified control run (mut-a on the c1-junk control). Note: the tool has no positional
  path argument (argparse rejects a bare path), so the control is passed via `--skill`:
  `TMPDIR=$S python3 $S/mut-a.py --skill .ufo/waves/round-47/controls/c1-junk/skill-v7-entrycopy.md --rev 63eecf2738db96f46b0bd02b1b2dfd66787493d0 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --min-tally-pins 26`
  → rc=1, `PIN_CHECK=unmet tally_pins=26 digest_pins=5 mismatches=30 unparsed=0 no_command=1 dropped=0 rebound=0 duplicate=0 min_tally_pins=26 rev=63eecf27… baseline=yes` (`control-mut-a.log`).
  Pristine leg on the same control: byte-identical log (`diff` empty, `control-pristine.log`).
  The control does NOT discriminate mutant (a): it fails on `mismatches=30` (most pins rc=2 in the F
  export) with `rebound=0` under both bytes. The kill comes from `--selftest`, not the control.
- Verdict: **KILLED** (by `--selftest`). The `rebound == 0` conjunct is load-bearing in `met`; the
  claimed invariant holds against this defect.

## Mutant (b) — compute bindings without normalising the revision to `<REV>` (literal, `pin_bindings` line 287)

- Mutation (mut-b.py, sha256 `69397926ac0dd8eaea4db75ce173023e0870132d03925187f3548d09b11df4b0`):
  line 287 `norm = None if words is None else tuple("<REV>" if w == rev else w for w in words)` → `norm = None if words is None else tuple(words)`.
- Static analysis: `pin_bindings` has exactly one call site — `base_bind = pin_bindings(baseline_text, "<REV>")`
  (line 305). With `rev == "<REV>"` the substitution is the identity map, so the literal mutant is
  behaviorally equivalent by construction.
- Output: `--selftest` rc=0 with log byte-identical to pristine; fixture leg with a non-None
  baseline bind (fix-b2, below) rc=0, also identical to pristine.
- Verdict: **EQUIVALENT NO-OP**. The normalization inside `pin_bindings` is redundant; the
  behavior-bearing twin is the current-side normalization at line 330 inside `check()` — probed
  separately as (b2) so the probe lands on a behavior-bearing point.

## Mutant (b2) — supplementary: remove the current-side normalization (`check()` line 330)

- Mutation (mut-b2.py, sha256 `2fc43445b4a33144a0894c900850013aab865db825c29479d280372aa4dbb95b`):
  line 330 `norm = … tuple("<REV>" if w == rev else w for w in words)` → `norm = … tuple(words)`.
- `--selftest`: rc=0, log byte-identical to pristine → **coverage gap**: no selftest case binds a
  rev-worded current command against a baseline.
- Fixture fix-b2 (git repo inside the scratch dir; baseline commit's registry row carries the span
  `python3 tools/rev.py <REV> --selftest` → `FOO_SELFTEST pass=3 fail=0`; the current measurement
  reads a scratch skill file whose span bakes the resolved sha `fa048827…` in — the shape of the
  real registry's `conform.py 63eecf27… --selftest` row):
  - pristine → rc=0 `PIN_CHECK=met` (normalization maps the baked sha to `<REV>`, matches baseline bind);
  - mut-b2 → rc=1 `PIN_CHECK=unmet … rebound=1` with
    `pin line=3 kind=tally prefix=FOO_SELFTEST state=rebound baseline_cmd='python3 tools/rev.py <REV> --selftest' cmd='python3 tools/rev.py fa0488271015e9e72b2fdf37012cd9f444d1409a --selftest'` (`fixb2-mut-b2.log`).
- Real claim leg (`--rev T --baseline-rev E --min-tally-pins 26`): rc=0, log byte-identical to
  pristine → on the actual E→T delta the normalization is unexercised. Static bind-probe
  (`bind-probe.py`, using the tool's own parse functions on `git show` texts): 26 shared keys,
  0 dropped, and for every shared key `b2_rebound=False` — the two rows that bake a hash into the
  command span at T (('SOURCES append-only timing (r38)', `MORI_SOURCES_APPENDONLY_SELFTEST`) and
  ('counter conformance v3 (r40)', `CONFORM_SELFTEST`)) have **None baseline binds**, so the
  comparison is skipped entirely.
- Verdict: **SURVIVES `--selftest` and the real claim detector; killed only by a constructed
  fixture.** Coverage finding — line 330's normalization is behavior-bearing for the baked-hash
  shape but covered by neither the selftest nor the landed claim measurement. Not a contract change.

## Mutant (c) — skip rebound when baseline argv is None (literal)

- The specified skip **already exists** in pristine v2: line 331
  `if bkey in base_bind and base_bind[bkey] is not None and norm != base_bind[bkey]:` — when the
  baseline bind is None, rebound is not counted. No textual mutation is possible; `mut-c.py` is
  byte-identical to pristine (sha256 `9832e38c…` == pristine).
- Output: `--selftest` rc=0 (identical log); fixture leg rc=0, identical to pristine.
- Verdict: **EQUIVALENT NO-OP — the invariant is already implemented.** The behavior-bearing
  mutation is the guard's *removal*, probed as (c2) below.

## Mutant (c2) — supplementary: remove the None-guard (count rebound when baseline argv is None)

- Mutation (mut-c2.py, sha256 `8d4b00fbd969f69b2159d75f9479073806e8b3a9e5d209ecf3362ea6b7ed5060`):
  line 331 → `if bkey in base_bind and norm != base_bind[bkey]:`.
- `--selftest`: rc=0, log byte-identical to pristine → **coverage gap**: no selftest case has a
  None baseline bind.
- Fixture fix-c2 (baseline commit: pin with no derivable command → baseline bind None; current
  commit: same row name/prefix with a bound, matching command): pristine → rc=0 `PIN_CHECK=met`
  (rebound skipped on None baseline); mut-c2 → **crash**:
  `TypeError: can only join an iterable` at line 334 (`" ".join(base_bind[bkey])` with `None`), rc=1 (`fixc2-mut-c2.log`).
- Real claim leg: **rc=1, same TypeError crash** (`claim-mut-c2.log`) — the real E→T delta has
  exactly the 2 shared keys named above with None baseline binds and non-None current binds, so
  the unguarded rebound path fires and the output line joins None.
- Verdict: **KILLED by both the fixture and the real claim detector.** The None-guard is
  load-bearing for crash-freedom on the actual registry, and `--selftest` does not cover the path.

## Structural observation (emerged from the probes; detection only, not judged, not fixed)

For rows whose self-test cell is the bare `--selftest` flag with a `<rev>` placeholder in the
entry cell, the BASELINE parse always binds None: `derive_command` substitutes `<rev>` → `<REV>`
and its own post-check `any(w.startswith("<") for w in ewords)` then rejects the substituted
placeholder. So in pristine v2 as landed, the rebound comparison is structurally skipped for such
rows. Real impact today: 2 of the 26 shared E→T keys (r38 SOURCES append-only timing, r40 counter
conformance v3) are in this class — a tool-path swap in those entries between E and T would not be
flagged `rebound` by v2. (At E those rows bound no command; at T they bind
`… 68d66ca… --selftest`.) Observed evidence only.

## Restoration evidence

- `v2-pristine.py` sha256 before == after == `9832e38c…` (never edited; every run read it read-only).
- `mut-c.py` == pristine bytes (literal (c) is impossible — predicate already present).
- Lane HEAD before == after == T; `git status --porcelain -- tools/mori-pin-check.py SKILL.md` → empty.
- All writes confined to `.scratch/r47w2-MutV2Rebound/` (mutants, logs, probes, fixture repos
  fix-c2/fix-b2 — git repos initialized inside the scratch dir, stricter than the mktemp recipe)
  plus this report file. No lane git state touched (no add/commit/stash/checkout/reset/pull/push/restore
  outside fixture repos).
- Transient tool exports under `lane/.scratch/pin-check-*` are created and removed by the tool
  itself (`finally: shutil.rmtree`). Residue observed and deliberately NOT touched:
  1. `lane/.scratch/.scratch/` — empty parent dir left by my first claim attempt, where the
     scratch copy's DEFAULT `--repo` (two dirnames up from the copy) resolved to `lane/.scratch`;
     that attempt failed rc=2 `PIN_CHECK_SETUP unreadable …/.scratch/.scratch/pin-check-ufpnfgy_/tree/SKILL.md`
     (observed output; on-disk log later overwritten by the successful rerun — precise mechanism
     UNVERIFIED, not reproduced). Rerun with explicit `--repo <lane root>` succeeded (met, rc=0).
  2. `lane/.scratch/pin-check-sazzzdjn/` — an export of T (`tree/SKILL.md` sha256 `2c9772fe…` ==
     `skill-T.md`; no `tree.tar` → past the extract stage; dir created 17:23:07, still present
     17:24:10). Attribution UNVERIFIED: possibly my mut-c2 leg with a silently failed cleanup
     (`ignore_errors=True`), possibly a sibling's in-flight claim run. Left in place — deleting
     risks a sibling's live fixture (cf. the F35MutReceipt /tmp incident reported on IRC this wave;
     I confirmed non-involvement: no /tmp usage, no rm run by this seat).

## Verdict summary

| probe | mutation | `--selftest` | fixture | real claim (T vs E) | verdict |
|---|---|---|---|---|---|
| a | drop `rebound == 0` from `met` | rc=1, 2 FAIL arms (rebound arms flip to met) | — | — | **KILLED** (selftest) |
| b | literal: no normalization in `pin_bindings` | rc=0, log identical | rc=0, identical | — | **EQUIVALENT NO-OP** (identity at only call site) |
| b2 | no normalization at `check()` line 330 | rc=0, log identical (gap) | rc=1 rebound | rc=0, log identical | **SURVIVES selftest + claim; killed by fixture** → coverage finding |
| c | literal: skip rebound when baseline argv None | rc=0, log identical | rc=0, identical | — | **EQUIVALENT NO-OP** (guard already present) |
| c2 | remove the None-guard | rc=0, log identical (gap) | rc=1 TypeError crash | rc=1 TypeError crash | **KILLED** (fixture + real claim) |

Claim-facing bottom line: the landed v2's rebound machinery holds — the verdict-gating clause (a)
and the None-guard removal (c2) both die on real detectors. Two `--selftest` coverage gaps found
(no None-baseline-bind case; no rev-worded-current-command-vs-baseline case); the literal (b)/(c)
probes are no-ops as specified. C1 calibration reproduced independently: pristine
`--rev T --baseline-rev E --min-tally-pins 26` → `PIN_CHECK=met`, rc=0 (tally_pins=28 ≥ 26,
dropped=0, rebound=0).
