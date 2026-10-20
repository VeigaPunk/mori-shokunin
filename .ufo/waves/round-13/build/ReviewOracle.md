# Round 13 — ReviewOracle (MoriR13.ReviewOracle)

Scope: baseline oracle `tools/mori-silence-cases.sh` (frozen copy
`.ufo/waves/round-13/frozen/mori-silence-cases.sh`, sha256 `448f7723…`, 1090 lines),
its final-verdict consumers, and the regex / cardinality / rc failure conditions.
SUT (census) implementation was not checked; census contract text is cited only from
its usage header (`tools/mori-census.sh:352-354`).

Method and limits:
- Read-only inspection: full baseline read, `grep` over consumers, `diff -u` of
  frozen vs live, `sha256sum`. No oracle, census, selftest, or wrapper was executed.
  Every "would pass/fail" below is a code-reading prediction [INFERENCE], not an observation.
- The live `tools/mori-silence-cases.sh` was edited by OracleFix while I read it. Observed
  live sha256 at last read: `fa60f12e…` (1170 lines); it moved several times during review
  (`b6a39d91…` → `a8824408…` → `fa60f12e…`). Live anchors below are from the last grep
  and must be re-anchored when OracleFix settles. Baseline anchors are frozen-file lines.
- Tools installed/updated: none. No credential material, journal MESSAGE, process env, or
  secret path was read.

## 1. Final-verdict consumers of the oracle

| # | Consumer | What it reads | Breaks if |
|---|---|---|---|
| C1 | `SKILL.md:68` gate row; `SKILL.md:94-114` contract text | rc 0 clean / 1 failed / 2 could-not-evaluate; `MORI_SILENCE_CASES: matched=N total=M`; 28 cases; bare `PASS <id>` for check-style cases | rc 1 can mean crash; tally denominator silently shrinks; check-style PASS format changes |
| C2 | `.ufo/waves/round-13/frozen/inputs.json:5` | pinned sha `448f7723…` | oracle sha changes without a recorded re-pin (QUALITY criterion 10/13) |
| C3 | `corpus/knowledge/audit-r11.md:157` (F02), `:197` (D02), `:376-407` (Appendix C) | D02 acceptance: "BANANA/roll-rc/tally-corruption mutants must fail without weakening lane-state cases" | any mutant that keeps `exit 0` with a non-28 tally |
| C4 | Round-13 RegressionHarness and spec (`spec.json` item OracleFix/RegressionHarness) | honest 28/28; BANANA, duplicate, CLEAN rc1, DRIFT rc0, missing each must fail the oracle | any adversarial wrapper reaching `matched=28 total=28` or exit 0 |
| C5 | `SCORECARD.md:605`, `LOG.md`, `corpus/evidence/*` receipts, `corpus/README.md:55-58`, `corpus/evidence/README.md:166` | cited `matched=28 total=28` at a pinned sha; receipts "reproduce only at the pinned sha" | any byte change invalidates receipts until a recorded re-pin |
| C6 | `corpus/QUALITY.md` criteria 6, 7, 8, 10, 13, 19, 21 | rc-gating, no live producer pipe in match tests, enumerated channels, pre-registered gradient | the oracle's own claims go unverified by its own gates |

No consumer reads per-case lines or the `failed:` stderr line programmatically; all consumers
read the tally line and/or the exit code.

## 2. Failure conditions (baseline anchors = frozen file)

Severity: H = oracle can go green on a wrong/absent verdict; M = wrong grade under a
specific input class; L = hygiene / latent.

### H1 — No expected-case-count assertion (tally corruption)
- `TOTAL_N` is incremented only by `assert_case` (frozen `:561`) and `count_check` (`:621`).
  The denominator is "however many ran", not `${#CASE_IDS[@]}` = 28.
- Final `printf 'MORI_SILENCE_CASES: matched=%d total=%d'` (`:1083`) and `[ PASS_N -eq TOTAL_N ] && exit 0` (`:1088`) have no reference to the registry size.
- Predicted [INFERENCE]: deleting one `CASE_IDS` entry (`:1016-1045`), or inserting `return 0` before `assert_case` in one `case_*` function, or duplicating an id, yields `matched=27 total=27` (or `matched=N total=N`) and exit 0.
- Unregistered `case_*` functions are never executed and never counted.
- D02 (`audit-r11.md:197`) explicitly names "tally-corruption" mutants as in scope for this round.
- Proposed check: assert `TOTAL_N == ${#CASE_IDS[@]}` and that each id recorded exactly one grade (per-id done flag); otherwise exit 1 with the mismatch named. Mutants: (a) drop one registry id, (b) early `return 0` in one case, (c) duplicate id, (d) registry id with no function → each must exit non-zero and must not print `total=27`-style green.

### H2 — Crash exits collide with the verdict exit code
- `set -euo pipefail` (`:141`) with no ERR trap. Any unguarded failure mid-run aborts before the tally line with the failing command's rc, usually 1.
- Concrete paths: registry id without a function → rc 127 (`:1074-1075`); `before=$(fx_fingerprint)` at `:945` where `fx_fingerprint` (`:626-629`) is a pipefail pipeline with `find … -exec sha256sum` → any unreadable path in `CASE_DIR` → rc 1, no tally; `jl_*`/`printf` write failures → rc 1.
- Exit 1 is documented as "failed" (`SKILL.md:68`, `:96-97`); exit 2 is the documented "could-not-evaluate / setup" code. A crash therefore reads as a real failure without a tally, and the documented 2 is never used for mid-run crashes.
- Proposed check: ERR trap (or explicit guards) that prints `mori-silence-cases: internal error at line N` and exits 2 with no tally; mutants: unreadable file under `CASE_DIR` during readonly-no-mutation; unregistered id; a case calling a failing command → each must exit 2, never 1, and never 0.

### H3 — Aggregate state defaults to `not-open` (vacuous pass channel)
- `aggregate_state_from_out` (`:506-520`): only `silent`, `progressing`, `progressing_weak`, `skipped` are parsed; anything else, including a `SURFACE silence:` line with all four zero and `young=`/`not_open=` values, falls through to `printf not-open` (`:519`).
- Three cases want `not-open` with finding 0 and rc 0: `completed-not-open` (`:655`), `nolane-launch-not-open` (`:694`), `committed-report-closes` (`:859`). A census with no lane rows whose aggregate line carries only zero counters (or none recognized) grades `not-open` and passes all three when verdict/rc/nonce are consistent.
- `young=` is never parsed, so the aggregate path can never grade `young` (`:664`, `:673`, `:682`) correctly; a truthful census without lane rows fails those cases for the wrong reason.
- Proposed check: parse every counter explicitly; require exactly one non-zero state counter (or an explicit `not_open=1`); empty or zero-state line → FAIL, never `not-open`. Mutant: a census that prints verdict/rc/nonce and `SURFACE silence: ok (silent=0 progressing=0 progressing_weak=0 skipped=0)` with no lane rows must fail `completed-not-open`.

### H4 — Lane-row and aggregate cardinality not checked
- `lane_state_from_out` (`:497-504`) takes the first `SURFACE lane.<l>:` row (`grep -m1`); a second row with a different state is never seen.
- `aggregate_state_from_out` (`:506-520`) resolves contradictions by precedence (silent > progressing > weak > skipped) — `silent=1 progressing=1` grades `silent`.
- Proposed check: exactly one lane row for the fixture lane (count == 1) and exactly one `SURFACE silence:` line; contradictory counters → FAIL.

### M1 — Nonce token matched as an unanchored substring
- `nonce_present` (`:533`): `*"$NONCE_TOKEN"*`. The token `nonce-<N>` matches inside any longer token (`nonce-1744128` ⊂ `nonce-17441281…`) and inside an output carrying a stale longer token.
- With a pinned small nonce (`MORI_RUN_NONCE=1`, documented as operator reproducibility `:177`) the token `nonce-1` matches any `nonce-1…` replay.
- Proposed check: boundary match, e.g. `grep -Eq "(^|[^0-9])nonce-${RUN_NONCE}([^0-9]|$)"` over a here-string. Mutant: pin `MORI_RUN_NONCE=1`, replay output carrying `nonce-17…` → must FAIL.

### M2 — `finding_present` unanchored and count-collapsed
- `:522-526`: `grep -c '^FINDING LANE_SILENT'` matches `FINDING LANE_SILENTX`; `n -gt 0` collapses duplicate findings into one boolean.
- Proposed check: `^FINDING LANE_SILENT( |$)`; duplicate LANE_SILENT → FAIL (count must be exactly 0 or 1 as the case wants).

### M3 — Verdict grammar is count-blind (residual of the F02 fix)
- The in-flight `verdict_grade` (live `:580+`) checks cardinality, vocabulary, the full line grammar, and word↔rc. It does not check the counts: `DRIFT (findings=0 drift=0 unavailable=0 surfaces=7)` with rc 1 passes, and `CLEAN (findings=5 drift=5 …)` with rc 0 passes.
- The admitted contract text (`tools/mori-census.sh:352-354`) states the grammar and the exit mapping only; it does not state a count↔word rule. [INFERENCE] a `drift=0 ⇔ CLEAN` rule is probable but not documented, so do not enforce it until the contract owner states it. Record as a named residual.

### M4 — Verdict and rc order vs header claim (wording only)
- The in-flight header (live `:41-55`) says rc > 1 is "rejected before the roll is read". In `assert_case` the `vcheck` (`verdict_grade`) runs before the `CASE_RC -gt 1` gate (live `:636` vs the gate after). Behavior is correct (the setup message wins), but the header is inaccurate. Fix the comment or move the computation below the gate.

### L1 — Pipelines feeding match tests (QUALITY criterion 7 spirit)
- `lane_state_from_out` (`:498-504`), `aggregate_state_from_out` (`:506-508`), `assert_case` verdict capture (`:570`), `shape_observe` (`:981`) all use `printf | grep -m1` inside `$(… || true)`. The captured value is correct (grep emits its match before exiting) and the SIGPIPE rc is masked by `|| true`. This is latent: a future edit removing `|| true` yields rc 141 misread as "no match".
- The new `verdict_grade` uses here-strings — the compliant form. Convert the remaining sites to here-strings for consistency.

### L2 — Unquoted want expansion
- `want_match` (`:541-547`): `for w in ${2//|/ }` is unquoted, so want tokens undergo pathname expansion. All current wants are glob-free; latent only.

### L3 — Re-exec guard with a stale marker
- `:207-221`: `MORI_CASES_SCRUBBED=1` preset without fd 3 → `read <&3` fails → `die` exit 2 with "pinned-entropy channel read failed". Loud, but the diagnostic misleads an operator who only exported the marker. Low.

## 3. In-flight F02 fix (OracleFix edits, observed live, sha `fa60f12e…`)

Covered (code-reading [INFERENCE] unless noted):
- Lane cases: `assert_case` grades `vcheck` for every case; any non-`ok` verdict is FAIL, and the crash path now reports `verdict missing` (live `:636` onward).
- `readonly-no-mutation` (live `:1016`) and `case_shape_invariance` (live `:1067`, `:1072`) both call `verdict_grade` per side, so the guards no longer rely on prefix presence. `shape_has_verdict` was removed.
- `verdict_grade` (live `:580+`): `grep -c '^MORI_CENSUS:'` exact count (missing/duplicate), anchored `VERDICT_RE` with the documented field order, word↔rc mapping `CLEAN:0|DRIFT:1`, here-string capture (no SIGPIPE).

Not covered by the in-flight fix:
- H1 (tally cardinality), H2 (crash exit collision), H3 (aggregate vacuity), H4 (lane/aggregate cardinality), M1 (nonce boundary), M2 (LANE_SILENT anchor), M3 (count consistency residual).
- Pre-register: this fix removes only the verdict-word blind spot; the wrappers below must now fail, but the lane-state vacuity and tally corruption channels remain open.

## 4. Pre-registered expected gradient (QUALITY criterion 13) — predictions, not observations

Honest run (no wrapper): `matched=28 total=28`, exit 0, stderr empty, 28 `PASS` lines (2 bare, 26 with `nonce=1`).

Adversarial census wrappers (all rewrite only the verdict or rc; nonce and lane rows preserved). Predicted `matched=0 total=28`, exit 1 for each:
- Appendix C (`CLEAN|DRIFT` → `BANANA`, rc kept) → `malformed`.
- Duplicate roll (second `MORI_CENSUS:` line appended) → `duplicate (2 lines)`.
- Missing roll (`MORI_CENSUS:` line removed) → `missing`.
- CLEAN with rc 1 (DRIFT → CLEAN, `exit "$rc"`) → `inconsistent (word=CLEAN rc=1)`.
- DRIFT with rc 0 (CLEAN → DRIFT, `exit 0`) → `inconsistent (word=DRIFT rc=0)`.
- Crash rc 2 with a valid roll → `census setup rc=2` in every case; oracle exit 1 (not 2) because these are case failures.

Expected residual: a wrapper that keeps a grammar-valid roll and changes only the count values (`findings=999`) still scores 28/28 (M3).

Tally-corruption mutants (H1), not yet covered by any in-flight change: a dropped or duplicated registry id or a `return 0` before `assert_case` predicted to exit 0 under the frozen and in-flight code. The required result is non-zero exit with the mismatch named.

## 5. Recommended checks for the integrated run (L1, after all seats land; not run by this seat)

1. Honest run: `bash tools/mori-silence-cases.sh` → `matched=28 total=28`, exit 0.
2. Appendix C wrapper plus the five adversarial wrappers in §4 → each `matched=0 total=28`, exit 1, none `exit 0`.
3. Tally mutants (H1 a–d) and crash mutants (H2) → non-zero, never exit 0 and never exit 1 for H2 setup/crash (expect 2).
4. Nonce boundary mutant (M1) and LANE_SILENT anchor mutant (M2).
5. Aggregate vacuity mutant (H3) must fail `completed-not-open`.
6. Re-pin: record the new oracle sha as a recorded act with its reason (QUALITY criteria 10/13), update `frozen/inputs.json` and the SKILL.md/evidence references (C1, C2, C5).

## 6. Residual risk and verification gaps

- Nothing executed; all predictions above are code-reading [INFERENCE] until L1 runs the checks in §5.
- Live file moved during review; findings anchored to the frozen baseline. Re-anchor after OracleFix finalises.
- H1 and H3 are the strongest remaining channels: each lets an oracle that does not grade the intended cases report green, and neither is addressed by the in-flight F02 fix.
- M3 depends on a contract statement that does not currently exist in the census usage text.
