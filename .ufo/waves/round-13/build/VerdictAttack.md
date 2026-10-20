# VerdictAttack — round 13 critic, F02 verdict-integrity repair

Seat: `MoriR13.VerdictAttack` (critic, leaf). Target: OracleFix's uncommitted edit to
`tools/mori-silence-cases.sh` (working tree, read 2026-10-20; HEAD `6531ac6`, oracle blob
`0698810` → working tree). Nothing was run: no oracle, no census, no wrapper. Every
"predicted" tally below is `[INFERENCE]` from the source and is unmeasured until L1 runs it.
No tools installed or updated.

Axes: **operability** (the oracle's green certifies the verdict contract it claims) and
**coverage** (the mutant classes the claim names are the ones actually exercised). The
24 lane-state wants must not move.

## What the repair closes (source-confirmed, unmeasured)

| Class | Mechanism after repair | Anchor |
|---|---|---|
| BANANA word (audit-r11 Appendix C) | full-line `VERDICT_RE` rejects the word | `:579`, `:589-591` |
| Missing roll | `n=0` → `missing` | `:582-585` |
| Duplicate roll (also identical duplicates, and a second roll written to stderr, because of `2>&1` at `:492`) | prefix count `^MORI_CENSUS:` ≠ 1 → `duplicate`. The count uses the loose prefix and the grammar uses the strict regex, so a valid line plus a BANANA line still fails | `:582-586` |
| CLEAN rc 1 / DRIFT rc 0 | `word:rc` must equal `CLEAN:0` or `DRIFT:1` | `:593-597` |
| Mangled tail, CR suffix, double space, `MORI_CENSUS:CLEAN` | anchored `^…$` regex | `:579` |
| readonly-no-mutation ignored the verdict | it previously checked only the fingerprint and the nonce (old `:945-954`), so a census that printed only the nonce token passed. It now needs `verdict_grade == ok` | `:1015-1023` |
| shape-invariance passing with equal bad grades | per-side `va`/`vb` are checked before the A/B comparison | `:1067`, `:1077-1078` |
| **Old shape crash guard was substring-forgeable** (counterexample against HEAD): `shape_has_verdict` searched the composed grade string for `MORI_CENSUS:` (old `:985`). A census that printed `SURFACE lane.kagi: MORI_CENSUS:x (…)` and no roll got `obs=MORI_CENSUS:x` from `lane_state_from_out` (`${rest%% *}`, old `:502-503`). The guard was satisfied and shape has no state want, so the case passed with no verdict at all | removed; replaced by `verdict_grade` over `CASE_OUT` | diff hunk `@@ -982` |
| Aggregate API path | `verdict_grade` does not depend on `api=lane` or `api=aggregate`, so the roll check holds on both paths | `:636`, `:648` |
| Historical r1 gradient (QUALITY 13) | the grammar and rc mapping are byte-identical at the first census commit `7ca17b1` (`:499-506`: same `printf`, `CLEAN) exit 0 ; DRIFT) exit 1`), so a frozen-r1 run does not gain new verdict failures | `git show 7ca17b1:tools/mori-census.sh` |
| `MORI_CENSUS_SELFTEST:` collision | `^MORI_CENSUS:` needs a colon right after `CENSUS`, so the selftest summary line is never counted | `7ca17b1:786` |

## Counterexamples against the repair

### V1 — HIGH (coverage/claim): tally corruption survives, so D02 is only partly closed
`audit-r11.md:197` sets D02's acceptance as "BANANA/**roll-rc/tally-corruption** mutants must fail".
The repair checks that the tallies are `[0-9]+`, but not what they mean.

Wrapper (proxy; the real rc and rows are kept):
```bash
out=$(bash …/tools/mori-census.sh "$@" 2>&1); rc=$?
out=$(sed -E '/^MORI_CENSUS: CLEAN /s/ drift=[0-9]+ / drift=9 /; /^MORI_CENSUS: DRIFT /s/ drift=[0-9]+ / drift=0 /' <<<"$out")
printf '%s\n' "$out"; exit "$rc"
```
This yields `CLEAN (… drift=9 …)` rc 0 and `DRIFT (… drift=0 …)` rc 1. Both match `VERDICT_RE` and
both are word/rc-consistent. **Predicted 28/28 under the current repair.**

The census can never produce these lines. `ROLL` is set only at `mori-census.sh:333` (`CLEAN`) and
`:370` (`DRIFT`), inside the same `warn|crit` arm that increments `N_DRIFT` (`:367-371`). So
CLEAN ⇔ drift=0 and DRIFT ⇔ drift≥1 is an increment-site invariant (QUALITY 14).
`FINDING_LINES` is appended only at `:366`, so `findings` = count of `^FINDING ` lines and
`drift` = count of `^FINDING [^ ]+ severity=(warn|crit) ` lines. Both are checkable from the
captured output alone, with no source inspection.

**Smallest safe correction:** in `verdict_grade`, after the word/rc check, reject
`CLEAN` with `drift≠0` and `DRIFT` with `drift=0`. A stronger optional check: reject when `drift > findings`.
If the counts are cross-checked against lines, cross-check **only `findings` and `drift`**; see V2.
If this is not taken, the F02 claim must say "tally semantics not validated; D02 tally class open".

### V2 — HIGH if someone "strengthens" V1 naively: `surfaces=`/`unavailable=` must NOT be cross-counted against lines
Lane rows bypass `emit_surface`. `mori-census.sh:1564` appends `SURFACE lane.$lane: …` directly to
`SURFACE_LINES`, so they are counted in neither `N_SURFACES` (`:377`) nor `N_UNAVAIL` (`:380`).
Appendix B's observed honest output shows `surfaces=7`: the 7 `emit_surface` calls in `run_census`
(`:1721-1727`) plus one uncounted lane row. A check of "surfaces = count of `^SURFACE ` lines"
would false-FAIL every honest case. **Predicted 0/28 on the honest census.** This is a crash-masking
inverse: a gate that is red for the wrong reason.

### V3 — MEDIUM (claim bound): "final roll" position is not enforced
The header (`:21-22`, `:41-42`) and the comments say *final* roll, but `verdict_grade` accepts the
single valid line anywhere. Wrapper: `printf '%s\n%s\n' "$last" "$body"` puts the verdict first and
the rows after it. **Predicted 28/28.** The honest census prints the roll as its last line and exits
immediately (`mori-census.sh:1729-1740`; live mode installs no EXIT trap, since the only trap is the
selftest one at `:2019`). So "roll is the last line of `CASE_OUT`" is safe for the honest census
`[INFERENCE]`. Note that `$(…)` strips trailing newlines at `:462`.

**Smallest correction:** either add `[ "${out##*$'\n'}" = "$line" ]`, or drop "final" from the
claim and say "exactly one, any position".

### V4 — LOW (hygiene, documented invariant): the new FAIL texts print census bytes without redaction
`verdict_grade` prints `malformed (line=%s)` with the raw line (`:590`). That text reaches stdout
unredacted in three places:
- `assert_case` `"$vcheck"` (`:649-650`), although `$verdict` beside it *is* redacted;
- readonly (`:1023`);
- shape (`:1078`), whose `shape_grade_a/b` also embeds the raw `v` (`:1055-1056`).

The header promises that "failure texts redact the nonce token" (`:30-31`, r6 R1).
Counterexample: append ` nonce-$MORI_RUN_NONCE` to the roll line, and the token reaches the
per-case stdout mid-run. Caveat `[INFERENCE]`: the census already receives the token
(`MORI_RUN_NONCE`, `:484`), so this is convention drift, not a new secret leak. The pre-existing
shape `:1081` message has the same exposure.

**Smallest correction:** wrap each print site with `redact`, or make `verdict_grade` return the
reason without the line. `assert_case` already prints the redacted `got=[…]`.

### V5 — MEDIUM, pre-existing, outside F02 (residual, not a blocker): aggregate fallback is a second, stale authority
`aggregate_state_from_out` (`:540-554`) returns `not-open` for **any** `SURFACE silence:` row whose
counters do not parse. It reads unavailability from `skipped=`, but the current census hard-codes
`skipped=0` and reports `unavailable=`/`young=` separately (`mori-census.sh:1571`).

Wrapper that deletes `^SURFACE lane\.` lines and keeps everything else, including a valid roll:
**predicted 23/28**. The 5 failures would be the 3 young cases (→ `not-open`) and
`repo-missing-unavailable`/`unreadable-git-unavailable` (→ `not-open`). `ledger-missing-not-silent`
passes on `not-open`; readonly and shape pass. The F02 repair is not weakened by this: the roll
check holds on both APIs. But a correct verdict does not make a row-stripping proxy wrong-free.

Record this as a named residual. Future smallest fixes: make the fallback reject unparseable
counters (empty `obs` → FAIL), or a clean cutover that removes it, since every honest r12 case
grades `via lane` (`corpus/evidence/roster-r12-20261019T220912Z-oracle.log:2-29`). Under V1's
stronger option, `findings`/`drift` cross-counts do **not** catch this wrapper, because lane rows
are not FINDINGs.

### V6 — LOW: readonly and shape still have no state/rc want
A census that is consistent but wrong (`DRIFT` rc 1 with a `LANE_SILENT`-free progressing tree)
passes both guards. This is bounded rather than open: both are open-old pid launches with a
post-launch subject commit (readonly `:1006-1013`, `shape_build :1037-1048`), which is the same
grading class as `subject-postlaunch-progressing` (`:815`, a runId launch, so not byte-identical).
Anti-sniff plus per-run
salt means a census cannot treat them differently from the graded `assert_case` fixtures without
identifying the case. Name it in the claim and do not fix it this round. Pinning `CLEAN`/rc 0 there
would add wants to two guards whose ids and wants the assignment says to preserve.

### Not defects (attacked, held)
- **Leftover live pipes** at `:542`, `:635`, `:1055` (and `lane_state_from_out`). All are
  `printf | grep -m1 … || true`. Under `pipefail`, SIGPIPE changes only the rc; `grep -m1` has
  already written the matched line, so the captured value is intact. These are display or state
  reads, not a match-test rc, so QUALITY 7 is not violated. The new code uses here-strings
  (`:582`, `:588`).
- **rc > 1.** `assert_case` rejects it before the roll is read (`:638`). readonly and shape reject
  it through `word:rc` (`CLEAN:2` → inconsistent). A crash before the roll gives `missing`.
- **Binary or invalid-UTF-8 output.** A grep "binary file matches" would empty `line` and give a
  `malformed` FAIL (fail-closed). The same exposure already existed for the other `grep` reads, so
  this is not a regression.
- **Registry.** 28 ids unchanged, shuffle/nonce untouched, no source greps added.

## Bounded claim L1 may make after measurement
"Oracle cases (all 28, including readonly-no-mutation and shape-invariance) require exactly one
`^MORI_CENSUS:` line matching the full CLEAN|DRIFT grammar, with CLEAN⇔rc 0 and DRIFT⇔rc 1.
Tested mutant classes: BANANA, missing, duplicate, word-flip, rc-flip, malformed tail[, drift-tally
— only if V1 lands]. Not covered: roll position (V3 unless fixed), surfaces/unavailable tally
meaning (V2), row-stripping via aggregate fallback (V5), consistent-but-wrong rolls in the two
guards (V6), and any newline injected into census rows from fleet inputs (census-side, live only)."

## Proposed L1 checks
Run once, after integration. Wrappers proxy the real census like Appendix C. Per QUALITY 23, commit
the wrapper generator and its digest, not a `/tmp` path.

| # | Wrapper edit of `out`/`rc` | Predicted (repair as read) | Predicted with V1 + V3 |
|---|---|---|---|
| 0 | honest census, no wrapper | 28/28, exit 0 | 28/28 |
| 1 | Appendix C BANANA bytes (`audit-r11.md:381-391`) | 0/28, exit 1 | 0/28 |
| 2 | remove the `^MORI_CENSUS:` line, keep rc | 0/28 | 0/28 |
| 3 | duplicate the last line | 0/28 | 0/28 |
| 4 | swap CLEAN↔DRIFT, keep rc | 0/28 | 0/28 |
| 5 | keep word, `exit $((1-rc))` for rc∈{0,1} | 0/28 | 0/28 |
| 6 | V1 drift-tally sed | **28/28 (survives)** | 0/28 |
| 7 | V3 roll moved to first line | **28/28 (survives)** | 0/28 |
| 8 | append `$'\r'` to the roll | 0/28 | 0/28 |
| 9 | delete `^SURFACE lane\.` lines (V5 residual) | 23/28 | 23/28 |

Also run the census `--selftest`, because CensusFix's edits share the run. Re-derive
oracle/census SHA-256 at the carrying commit. Row 9 is a residual probe and needs no fix this round.

## Re-review after OracleFix applied V1/V3/V4 (appended 2026-10-20)

I re-read `verdict_grade` in the working tree (`tools/mori-silence-cases.sh:578-633`).

- **V1, closed with one hole (see V7):** CLEAN requires `drift=0` and DRIFT requires `drift≥1`
  (`:620-632`). Per V2, `surfaces=`/`unavailable=` are not cross-counted (`:622-625`).
- **V3, closed:** the roll must be the last non-empty line, via `awk 'NF{last=$0}…'`
  (`:608-615`); otherwise the reason is `not-final`.
- **V4, closed in `verdict_grade`:** the malformed line is printed through `redact` (`:603`).
  The other reasons carry no census bytes. Nit: the comment at `:586` says the line is "never
  echoed here", which contradicts `:603`.
- **Anchor correction:** my V2 anchor `mori-census.sh:1564` was right for the bytes I read, but
  CensusFix has since shifted them. The lane-row append is now `:1687` and the ROLL/N_DRIFT flip is
  `:374-375`. OracleFix's comments cite `:1684` and `:366-371`, which are already stale. L1 must
  re-resolve every census pointer in the oracle comments and in this report at the carrying commit
  (QUALITY 9).

### V7 — MEDIUM: arithmetic overflow reopens CLEAN tally forgery
`:607` computes `drift=$((10#${BASH_REMATCH[2]}))`, and bash integers wrap without any error.
**Measured** (direct shell probe, not an oracle run) on GNU bash 5.3.15: `$((10#18446744073709551616))`
→ `0`, `$((10#18446744073709551617))` → `1`.

Counterexample: the roll `MORI_CENSUS: CLEAN (findings=0 drift=18446744073709551616 unavailable=0 surfaces=7)`
with rc 0 matches `VERDICT_RE`, wraps to `drift=0`, and grades `ok`. Applied as the CLEAN arm of
a tally wrapper, this is predicted to pass every rc-0 case (`[INFERENCE]`). The DRIFT arm fails
closed, because wrapped values are ≤0 or are positive garbage that a forger cannot choose freely
as 0.

**Smallest correction:** compare the captured digits as a string, never as a number. CLEAN requires
`BASH_REMATCH[2] == 0`; DRIFT requires `^[1-9][0-9]*$`. The census prints `%d`, so it never emits
leading zeros (`mori-census.sh` verdict `printf`). I sent this to OracleFix.

Add to L1's table: **row 10**, the CLEAN roll's drift rewritten to `18446744073709551616` (rc kept).
Predicted under the current tree: every case whose honest roll is CLEAN passes (the rc-0 wants).
Predicted after the string compare: 0 of those.

### V7 re-review (appended 2026-10-20): closed
`tools/mori-silence-cases.sh:611`, `:635-643`: `drift` is kept as the captured digit string. CLEAN
requires the literal `0`, so `00` and `2^64` fail closed. DRIFT requires `[1-9]*`; the regex at
`:594` has already restricted the field to digits, so this means "first digit nonzero". Census
pointers in the oracle comments are now symbolic (`:585`, `:624-634`), which leaves the numeric
anchors in this report as the only ones L1 must re-resolve.

Residual nit, LOW, needs no fix: `inconsistent (… drift=%s)` (`:637`, `:641`) prints SUT-chosen
digits without `redact`. `redact` masks only `nonce-<N>`, so a SUT could put the bare `<N>` digits
there. The SUT already receives `MORI_RUN_NONCE`, and the oracle prints `RUN_NONCE=` after the
loop, so this is the same no-new-secret class as V4. Claim bound unchanged, except that V1/V3/V4/V7
are now in the tested set once L1 runs rows 6, 7 and 10.
