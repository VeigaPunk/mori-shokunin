# Mo58MutationTester39 — mutation probe on the considerthese-2026-10-26 s1 split; s2 selection

Seat: Mo58MutationTester39 (mutation-tester, leaf — no subagents). Date: 2026-10-27.
Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin`. Freeze revision: `fe8801120a67c1a6b8899d7d0423839caa09e7d0`.
Lane HEAD at seat start: `4272736cfc5147586e1543413772f80daf44b04b`. Freeze-blob == working tree for every
byte this seat cites (`git cat-file blob fe8801…:tools/mori-pin-check.py` sha256 == `sha256sum tools/mori-pin-check.py`
== `32685b9306db061d2c2df21e976823d84a4017cc3524194f4ed76327443081f0`).
Disk guard before heavy work: green (`/fast/scratch/hyaku` 32% used, 552.2G free).
Scratch (created explicitly, cleaned before yield): `/fast/scratch/hyaku/mori-r58/Mo58MutationTester39` with `TMPDIR` set there.
Read first, per dispatch: `.ufo/waves/round-58/contract.md`, `.ufo/waves/round-58/count-c1.py`, `.ufo/waves/round-58/count-c2.py`.
No tool installed or updated (nothing to record); no pacman; no remote scripts; no fleet/sibling writes; no VCS mutation.

## Part A — suggestion 1 status against `tools/mori-pin-check.py`

**Status: CONFIRMED IMPLEMENTED (no counterexample found).** The contract's "ALREADY implemented at
`tools/mori-pin-check.py:140-150`" is true of the freeze bytes, and the implementation is behavior-bearing (Part B).

- `:139-144` (v5, round 51): "every mismatch line carries `class=env` or `class=stale` … `env` = the pinned command
  printed no tally line for its prefix (setup error, missing path, timeout, OS error …); `stale` = it ran and printed a
  different tally, or a tally whose exit code contradicts it, or a digest/line-count pin differs. The summary line ends
  `env=N stale=N`, and env + stale = mismatches." The v5 block names its motivation:
  `considerthese/2026-10-26.md` suggestion 1.
- `:145-150` (v5.1): absent instrument file → `stale`; ≥2 disagreeing tallies → `stale`; different tally printed before
  a timeout → `stale`; pinned tally then timeout → `env`.
- Behavior-bearing classifier: `:835-856` (`absent or ntails > 1` → stale; `observed is None` → env;
  `observed.strip() != want` → stale; else `env` iff `rc is None`).
- Detector arms: `:1481-1497` (`v5_class_env_setup_error`, `v5_class_env_timeout`, `v5_class_stale_tally`,
  `v5_class_stale_digest`) and `:1509-1527` (`v51_class_absent_instrument_stale`, `v51_class_two_tallies_stale`,
  `v51_class_wrong_then_timeout_stale`, `v51_class_right_then_timeout_env`).
- Registry record: `corpus/QUALITY.md` criteria 137/138 under "Criteria added round 51" (freeze-rev lines 1254, 1285:
  "the class rule itself is `considerthese/2026-10-26.md` suggestion 1").

**Adversarial finding (prose-vs-bytes divergence, LOW):** two committed lessons still describe s1 as not done:
`corpus/lessons/round-55.md:106` (freeze rev) — "its outstanding pin-environment split and carry-over-flag ledger are not
part of the frozen claims" — and `corpus/lessons/round-57.md` (Assimilation) — "`considerthese/2026-10-26.md` was
checked: no proposal implemented". The freeze bytes and QUALITY 137/138 show the s1 split landed in round 51; both
phrasings overstate per-round scope and read as "s1 still outstanding". Decided by bytes; not edited (report-only).

## Part B — mutation probe (required return)

Invariant challenged (from the contract's considerthese clause): *the s1 env/stale split is implemented and
behavior-bearing — an instrument that cannot run here (`env`) is never reported as drift (`stale`)*.

- **Mutant M1** (smallest behavior-bearing point; one line in an isolated scratch copy
  `/fast/scratch/hyaku/mori-r58/Mo58MutationTester39/probe.py`, byte-identical to the freeze blob before mutation):
  classifier line 844, `elif observed is None:` branch, `kind = "env"` → `kind = "stale"`. This reintroduces exactly
  the defect suggestion 1 was written against: a can't-run-here pin reported as stale/drift.
- **Expected detector** (registered before the run): the tool's own frozen selftest as the bounded behavioral detector,
  same command all three legs — `python3 -B <copy> --selftest`, `TMPDIR=<scratch>/runs/<leg>-tmp`, cwd scratch.
  Pristine: `PIN_CHECK_SELFTEST pass=N fail=0`, rc 0. Mutant: rc 1 with `FAIL v5_class_env_setup_error` and
  `FAIL v5_class_env_timeout` (both `env=0 stale=1`; the stale-class and v5.1 arms must keep passing). Restored:
  byte-identical to pristine, detector output identical to pristine.
- **Output (actual):**
  - Pristine: rc 0, 14.2 s, `PIN_CHECK_SELFTEST pass=125 fail=0`, 0 FAIL lines.
  - Mutant: rc 1, 14.2 s, `PIN_CHECK_SELFTEST pass=123 fail=2` — exactly the two predicted arms:
    `FAIL v5_class_env_setup_error … env=0 stale=1`, `FAIL v5_class_env_timeout … env=0 stale=1`
    (all 123 other arms, including every stale-class and v5.1 arm, still passed).
  - Restored: rc 0, 14.1 s, `PIN_CHECK_SELFTEST pass=125 fail=0` — summary line identical to pristine.
- **Verdict: KILLED.** The s1 classification is load-bearing, and the detector distinguishes the can't-run-here case
  from drift at exactly the point the suggestion targets.
- **Hashes:** pristine = restored = `32685b9306db061d2c2df21e976823d84a4017cc3524194f4ed76327443081f0`
  (== freeze blob == working tree); mutant = `79ce083a1222cb53fb82bea5669862994a8ea4f5b789f30dd6736524b6400827`.
- **Restoration evidence:** after the mutant leg, `probe.py` was overwritten from the pristine scratch copy; sha256
  equals the freeze blob and the working-tree tool; the restored detector leg reproduces the pristine summary exactly.
  The lane working tree was never touched by the probe (`git status --porcelain tools/mori-pin-check.py` empty at seat
  start; no write to any production path at any point).

## Part C — the one still-unimplemented suggestion suitable for this round

**Selection: suggestion 2 — the flagged-versus-fixed carry-over ledger (id-keyed, round-qualified).**

Why the others are not selectable:
- s1 (env/stale split): implemented (Parts A–B); contract says land its status as a lesson/criterion note, not a claim.
- s3 (re-execute what closures only evidence-verified): acted in round 50 (three counter re-executions,
  `corpus/lessons/round-50.md` "considerthese" bullet; QUALITY 136); no new lane artifact is mine to draft here.
- s4 (per-day suggestion-adoption status line): lives in the operator's daily reflections — operator input, which this
  seat must not edit.

Evidence that s2 is still unimplemented:
- `considerthese/2026-10-26.md` suggestion 2 (operator input, read-only): r48 left 9 UNFIXED flags; make the
  flagged-versus-fixed count a carry-over ledger, not a one-round snapshot.
- `corpus/QUALITY.md` criterion 153 (freeze-rev line 1524 cites the suggestion): "An unfixed critic flag is carried by
  round-qualified id into the next round's ledger, and its disposition is decided against that round's landing."
- `.ufo/waves/round-49/flagged-fixed/count-flagged.py` `:45-46` hardcodes `FREEZE = 4387cf94…` /
  `LANDING = e4dfff32…` and reads one `defects.jsonl` — it decides one round against one diff.
- Reproduced live by this seat (scratch copy of `count-flagged.py` + `defects.jsonl`, `--repo` = lane, documented
  read-only "No writes, no network"): `flagged=45 fixed=18 unfixed=9` / `na=18`, matching `corpus/lessons/round-49.md:159`.
  The nine UNFIXED ids: `C1-F1, C1-F6, C1-F8, C2-F1, JC-D7, V3-J10, V3-J11, RA-F2, RH-F2`.
- `corpus/lessons/round-57.md` (Assimilation): "suggestion 2's carry-over ledger remains planned."
- Independent corroboration in this wave: `.ufo/waves/round-58/w1/Mo58Scribe53.md` ("unimplemented as an artifact;
  a criterion only").

Adversarial check of the criterion's rationale ("the nine UNFIXED rows are named nowhere in rounds 49-56"):
**no counterexample found** within the bounded method — a lane-wide search for the eight distinct id strings hits only
the round-49 ledger/receipt, QUALITY 153's own text and worked example, the round-56 criterion-drafting report's copy
of the example string (`.ufo/waves/round-56/w1/Mo56ScribeConsiderthese.md:112` — the known false-fix shape, not a
disposition line), and round-58 wave reports. No `corpus/lessons/round-<NN>.md` with `NN > 48` names any of the nine.
Bounded to `corpus/lessons` + `.ufo/waves` (the criterion's own scope; a LOG/SCORECARD disposition would be invisible
to it, per its "Not covered").

Suitability: s2 matches the contract's "at most one still-unimplemented proposal" clause, needs no operator-input edit,
and lands as an artifact/criterion note (successor-clause dispositions for `C1-F1`/`RH-F2`, round-directory-qualified
ids) — decision left to the L1; this seat claims nothing and edits nothing.

## Bounds and cleanup

Wrote exactly one lane file: this report. Scratch `/fast/scratch/hyaku/mori-r58/Mo58MutationTester39` (probe copies,
run receipts, s2 counter copies) removed after the receipts above were quoted into this report. Did not run the frozen
round-58 counters (other seats own them); did not judge, integrate, or modify any sibling's source; no installs.
