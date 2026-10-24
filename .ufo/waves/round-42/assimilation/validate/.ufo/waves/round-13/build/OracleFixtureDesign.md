# OracleFixtureDesign — round 13 (F02 verdict fixtures and residual verdict-parsing bypasses)

Seat: `MoriR13.OracleFixtureDesign` (leaf, read-only design seat).
Owned output: this file only. **No source edits. No oracle/census run, no build, no
test, no lint, no formatter executed.** The only commands run were read-only
inspection (`read`, `grep`, `git show`, `sha256sum`, `nl`) and two synthetic
shell-semantics probes of the verdict helper on literal strings (not the repo's
SUT). Every runtime prediction below is marked `[INFERENCE]` unless it is an
audit measurement carried from `corpus/knowledge/audit-r11.md`.

## Axes

- **coverage** — the oracle must reject a forged/absent/duplicated final roll in
  all 28 cases, including the two guards that never used `assert_case`
  (`readonly-no-mutation`, `shape-invariance`).
- **operability** — the rejection must be reproducible from exact wrapper bytes,
  with a pre-registered before/after gradient and no run secret printed on
  per-case lines.

## Bytes examined (revisions matter; the live files moved during this review)

| Artifact | sha256 | Notes |
|---|---|---|
| frozen oracle `.ufo/waves/round-13/frozen/mori-silence-cases.sh` | `448f7723…eeb5` | 1090 lines; equals `git show HEAD:tools/mori-silence-cases.sh`; the audited F02 bytes |
| frozen census `.ufo/waves/round-13/frozen/mori-census.sh` | `3da5b098…3164` | matches `.ufo/waves/round-13/frozen/inputs.json` |
| live oracle `tools/mori-silence-cases.sh` | `34cd5770…1abfa` at 2026-10-20 01:19:34 -0300 | 1219 lines; OracleFix edited it while this seat read it (`448f7723` → `a8824408` → `fa60f12e` → `7f489544` → `c4f8e63c` → `34cd5770`). The helper semantics below were probed at `c4f8e63c` and are unchanged at `34cd5770`; the redaction fixes and their anchors are from `34cd5770` |
| live census `tools/mori-census.sh` | `479abc7a…d611` at 01:12:07 | CensusFix still editing; not the oracle's contract source |

Live line anchors below are quoted **by symbol and by the line numbers observed at
`34cd5770`**; they will shift if OracleFix edits again. Frozen anchors are stable.

## 1. Contract under test

- Census usage text: `frozen/mori-census.sh:352-354` —
  `Verdict: MORI_CENSUS: CLEAN|DRIFT (findings=N drift=M unavailable=U surfaces=S)`;
  `Exit: 0 CLEAN | 1 DRIFT | 2 setup/usage`.
- Census emitter: `frozen/mori-census.sh:1733-1739` prints exactly one such line
  after every `SURFACE`/`FINDING` line, then `case "$ROLL"` maps word→rc.
- `ROLL=DRIFT` is set in exactly one place, `emit_finding`'s warn|crit branch
  (`frozen/mori-census.sh:361-371`). Therefore, for honest output,
  `DRIFT ⇔ drift>0` and `CLEAN ⇒ drift=0`; `findings` may be >0 on CLEAN when an
  `info` finding was emitted.
- Audit: F02 at `corpus/knowledge/audit-r11.md:156-157`, D02 at `:197`
  (“BANANA/roll-rc/tally-corruption mutants must fail without weakening lane-state
  cases”), reproduce wrapper at `:376-407`.
- Oracle's own admitted contract after the fix: live header `:41-64` and
  `verdict_grade` comment `:579-593` (at `34cd5770`).

## 2. Bypass inventory at the frozen baseline (`448f7723`)

| id | anchor (frozen) | bypass | required failing class |
|---|---|---|---|
| B1 | `assert_case` `:570`, `:578-585` | `verdict=$(… \| grep -m1 '^MORI_CENSUS:' \|\| true)` and only `-z "$verdict"` is tested: a prefix-present line of any content admits the case | invalid roll word (`BANANA`), malformed tail |
| B2 | `:570`, `:604-609` | the roll word is never compared with `CASE_RC`; `wrr` comes from the observed state only | `CLEAN`+rc1, `DRIFT`+rc0 |
| B3 | `:570` `grep -m1` | only the first roll line is seen; a second well-formed roll is invisible | duplicate roll |
| B4 | `shape_has_verdict` `:985` | `case "$1" in *"MORI_CENSUS:"*)` — unanchored substring anywhere in the constructed grade string | missing roll hidden by a mention; BANANA |
| B5 | `case_shape_invariance` `:987-1006` | compares `A == B` only; two identically bad rolls pass; no expected state/rc | BANANA, duplicate, rc mismatch (both sides equal) |
| B6 | `case_readonly_no_mutation` `:939-955` | grades fingerprint + nonce only; never reads rc/roll/state | all of the above |

### Residual channels at the baseline (not repaired by F02 alone)

- **R1 tallies** — `findings=`, `unavailable=`, `surfaces=` are grammar-only;
  the old oracle and the current fix do not cross-count them. `findings=99` on a
  CLEAN `drift=0` line still passes (see §5).
- **R2 duplicate state rows** — `lane_state_from_out` (`:500-504`) and
  `aggregate_state_from_out` (`:506-520`) take the first matching row; a second,
  contradictory `SURFACE lane.<l>:` row is invisible.
- **R3 semantic anchor in the guards** — `readonly` and `shape` have no expected
  state/rc of their own; a consistently wrong but well-formed roll (e.g. always
  `DRIFT` rc1) passes those two guards.
- **R4 repairing proxy** — a proxy that drops the SUT roll and recomputes it from
  rc is indistinguishable from a correct SUT; Appendix C's own boundary note
  (`audit-r11.md:396-400`) applies.

### Pre-registered pre-fix gradient (frozen oracle + frozen census)

`BANANA` is measured by the audit; the rest are code-reading predictions
`[INFERENCE]` at the frozen pair (honest control is 28/28 there). The split is
7 silent-expectation cases (6 explicit `assert_case ... silent 1 1` plus
`report-future-no-close`, whose auto want resolves to silent under row-D: the
root-lane log pathspec excludes `.ufo`, the `>launch && <=NOW` awk window drops
the future commit, row B sees no dirty file) and 21 non-silent cases
(19 `assert_case` + `readonly-no-mutation` + `shape-invariance`).

| Mutant | frozen-oracle result | Why it survives the old oracle |
|---|---|---|
| BANANA word, rc preserved | **28/28, exit 0** (audit-measured) | prefix present; word never read |
| roll line deleted | **1/28** | 26 `assert_case` + shape fail; `readonly` passes (no roll check) |
| duplicate roll (same or opposite word) | **28/28** | `grep -m1` sees only the real first line |
| `CLEAN` + rc1 | **9/28** | 7 silent-want cases already want rc1; `readonly`/`shape` never compare rc to a want |
| `DRIFT` + rc0 | **21/28** | 19 clean-want cases + `readonly` + `shape` accept rc0 |
| valid word, tail `(…)` stripped | **28/28** | non-empty prefix is the whole test |

## 3. Current fix audit (`34cd5770`, live)

`verdict_grade <output> <rc>` (live `:595-644`) now requires, in order:

1. `grep -c '^MORI_CENSUS:'` **exactly 1** — `missing` / `duplicate (N lines)`
   otherwise (`:597-602`).
2. The single line matches the anchored full grammar
   `VERDICT_RE='^MORI_CENSUS: (CLEAN|DRIFT) \(findings=[0-9]+ drift=([0-9]+)
   unavailable=[0-9]+ surfaces=[0-9]+\)$'` (live `:594`) — `malformed` otherwise.
   The malformed line is emitted only through `redact()` (`:603-609`).
3. The roll is the **last non-empty line** — `awk 'NF { last=$0 } END {print last}'`
   (`:615-619`) — `not-final` otherwise. Honest census prints it last.
4. Word↔rc: `CLEAN:0|DRIFT:1` (`:620-623`).
5. Word↔drift as **strings**: `CLEAN` requires the captured `drift` text exactly
   `0`; `DRIFT` requires `[1-9]*` (`:624-643`). The comment records the measured
   bash wrap `10#18446744073709551616 => 0`, which a numeric test would have
   admitted; the string form closes it. `%d` printing means honest output has no
   leading zeros.

Consumers: `assert_case` computes `vcheck` (`:682`) and fails before state/finding/rc
wants on any non-`ok` (`:694`); `readonly-no-mutation` adds the same gate
(`:1062`, function at `:1052`); `shape-invariance` grades both sides (`va` `:1116`,
`vb` `:1121`) before its equality comparisons (`:1126-1136`).

### Measured helper semantics (synthetic literal strings, not the SUT)

Extracted `verdict_grade` logic at `c4f8e63c` (semantics unchanged at `34cd5770`), run over literal captures:

| capture (last line) | rc | grade |
|---|---|---|
| `CLEAN (findings=0 drift=0 unavailable=1 surfaces=7)` | 0 | `ok` |
| `DRIFT (findings=1 drift=1 unavailable=0 surfaces=7)` | 1 | `ok` |
| `BANANA (…)` | any | `malformed` |
| `CLEAN (findings=0 drift=00 …)` | 0 | `inconsistent (CLEAN drift=00)` |
| `CLEAN (findings=0 drift=18446744073709551616 …)` | 0 | `inconsistent (CLEAN drift=…)` |
| `DRIFT (findings=1 drift=01 …)` | 1 | `inconsistent (DRIFT drift=01)` |
| `BANANA nonce-<current>` | 0 | `malformed (line=…nonce-<redacted>)` |
| valid roll followed by another non-empty line | 0 | `not-final (…)` |

Honest-safety: the `drift` rule is derived from the single `ROLL=DRIFT` increment
site (frozen census `:361-371`); an `info` finding leaves `drift=0`/CLEAN intact, so
`findings>0, drift=0, CLEAN` remains admitted. The `not-final` rule matches the
emitter, which prints the roll and immediately exits.

## 4. Exact cases required (the deliverable)

### Invocation invariants

- The oracle invokes the SUT as `bash "$CENSUS"` with **no arguments** (`run_census`,
  live `:506-541`; frozen `:460-496`). A wrapper must hardcode the census path;
  `"$@"` is empty.
- The oracle runs the SUT under `env -i` with `PATH="$BIN:/usr/bin:/bin"`. Use
  absolute `/usr/bin/sed`, `/usr/bin/grep`, `/usr/bin/awk`; the wrapper itself is
  started by `bash`, so no shebang execution is involved.
- The SUT receives `MORI_RUN_NONCE` and the nonce-bearing disk target. Every
  wrapper below must preserve every non-roll byte (lane rows, FINDING lines,
  nonce echoes) and must not write under the case tree (`readonly-no-mutation`
  fingerprints it).
- Wrappers live outside the lane (runtime temp dir under the harness `--output`
  tree). A raw `${TMPDIR}` path is not evidence (QUALITY criterion 23): commit
  the generator and the wrapper digests, not the wrapper path.
- Substitute `@CENSUS@` with the shell-quoted census path (Python: `shlex.quote`).
  Use the **frozen** census for the pre-fix gradient and the **integrated** census
  for the final run.
- Pin `MORI_SHUFFLE_SEED` and `MORI_RUN_NONCE` for reproducible evidence; the
  oracle re-execs once to scrub the pins from its environment, so the SUT cannot
  read them, and pinned stdout is byte-identical across runs.

### Required mutants (each must fail the fixed oracle in all 28 cases)

Every template starts with:

```bash
#!/usr/bin/env bash
set +e
out=$(bash @CENSUS@ 2>&1)
rc=$?
```

**M1 — invalid roll word (Appendix C verbatim semantics).**

```bash
out=${out//MORI_CENSUS: CLEAN/MORI_CENSUS: BANANA}
out=${out//MORI_CENSUS: DRIFT/MORI_CENSUS: BANANA}
printf '%s\n' "$out"
exit "$rc"
```

**M2 — missing roll.**

```bash
out=$(/usr/bin/sed '/^MORI_CENSUS:/d' <<<"$out")
printf '%s\n' "$out"
exit "$rc"
```

**M3 — duplicate roll, same word.** Append a copy of the first roll line:

```bash
line=$(/usr/bin/grep -m1 '^MORI_CENSUS:' <<<"$out")
printf '%s\n' "$out"
[ -n "$line" ] && printf '%s\n' "$line"
exit "$rc"
```

**M4 — duplicate roll, conflicting word.** Append the opposite well-formed roll:

```bash
line=$(/usr/bin/grep -m1 '^MORI_CENSUS:' <<<"$out") || line=''
case "$line" in
  *CLEAN*) second='MORI_CENSUS: DRIFT (findings=1 drift=1 unavailable=0 surfaces=7)' ;;
  *)       second='MORI_CENSUS: CLEAN (findings=0 drift=0 unavailable=0 surfaces=7)' ;;
esac
printf '%s\n' "$out"
[ -n "$line" ] && printf '%s\n' "$second"
exit "$rc"
```

**M5 — CLEAN with rc1.** Rewrite every word to CLEAN and force rc1:

```bash
out=$(/usr/bin/sed -E 's/^MORI_CENSUS: (CLEAN|DRIFT) /MORI_CENSUS: CLEAN /' <<<"$out")
printf '%s\n' "$out"
exit 1
```

**M6 — DRIFT with rc0.** Rewrite every word to DRIFT and force rc0:

```bash
out=$(/usr/bin/sed -E 's/^MORI_CENSUS: (CLEAN|DRIFT) /MORI_CENSUS: DRIFT /' <<<"$out")
printf '%s\n' "$out"
exit 0
```

**M7 — malformed tail (contract-implied by “well-formed”; not separately named in
the executor prompt).** Keep the word, drop the parenthesised counters:

```bash
out=$(/usr/bin/sed -E 's/^(MORI_CENSUS: (CLEAN|DRIFT)) \(.*\)$/\1/' <<<"$out")
printf '%s\n' "$out"
exit "$rc"
```

**Honest control (N0).** No wrapper: `bash tools/mori-silence-cases.sh`.

### Expected gradient at the fixed oracle

Precondition: the honest control at the **same census bytes** is `matched=28
total=28`, exit 0, stderr 0 B, 28 `PASS` lines. If honest is not 28/28, stop: that
is integration, not F02.

| Case | frozen oracle `448f7723` | fixed oracle `34cd5770` | fixed reason class |
|---|---|---|---|
| N0 honest | 28/28 exit 0 | 28/28 exit 0 | — |
| M1 BANANA | 28/28 (measured) | **0/28 exit 1** | `malformed` |
| M2 missing | 1/28 `[INFERENCE]` | **0/28 exit 1** | `missing` |
| M3 duplicate same | 28/28 `[INFERENCE]` | **0/28 exit 1** | `duplicate (2 lines)` |
| M4 duplicate conflict | 28/28 `[INFERENCE]` | **0/28 exit 1** | `duplicate (2 lines)` |
| M5 CLEAN rc1 | 9/28 `[INFERENCE]` | **0/28 exit 1** | `inconsistent (word=CLEAN rc=1)` |
| M6 DRIFT rc0 | 21/28 `[INFERENCE]` | **0/28 exit 1** | `inconsistent (word=DRIFT rc=0)` |
| M7 malformed tail | 28/28 `[INFERENCE]` | **0/28 exit 1** | `malformed` |

Expected mutant stdout: 28 `FAIL` lines (none `PASS`), then `SHUFFLE_SEED=…`,
`RUN_NONCE=…`, `CASE_ORDER=…`, then `MORI_SILENCE_CASES: matched=0 total=28`.
Expected stderr: `mori-silence-cases: failed: <28 ids in shuffled execution order>`.
Assert tally/exit/reason class, not exact whitespace of the per-case text.

Per-consumer failure shapes at `34cd5770` (assert these substrings, not line
numbers):

- `assert_case`: `FAIL <id>: MORI_CENSUS verdict <reason> (rc=N) — one well-formed
  CLEAN|DRIFT line matching its rc is required; got=[…] tail=…`
- `readonly-no-mutation`: `FAIL readonly-no-mutation: MORI_CENSUS verdict <reason>
  (rc=N) — one well-formed CLEAN|DRIFT line matching its rc is required`
- `shape-invariance`: `FAIL shape-invariance: MORI_CENSUS verdict contract broken:
  A=[…] verdict=<reason> B=[…] verdict=<reason>`

Both guards must fail under every mutant — that is the coverage claim M2 previously
escaped through (only `readonly` passed) and M5/M6 escaped through (both guards
passed).

### Residual/attack fixtures (not part of the five-class acceptance; L1 decision)

**TALLY-1 — non-drift counters are not reconciled (D02 residual).**

```bash
out=$(/usr/bin/sed -E 's/(findings=)[0-9]+/\199/; s/(unavailable=)[0-9]+/\199/; s/(surfaces=)[0-9]+/\199/' <<<"$out")
printf '%s\n' "$out"
exit "$rc"
```

`drift` is left intact, so the word↔drift rule still holds. Predicted at
`34cd5770`: **28/28, exit 0** `[INFERENCE]` — the tally-corruption class named by
D02 remains open for `findings`/`unavailable`/`surfaces`. OracleFix records this as
a named D02 residual, not an applied change (its scope is the five F02 classes).
Safe partial closure: count `^FINDING ` lines and require it to equal `findings=`
(every `emit_finding` appends exactly one line and increments the counter; info
findings make `findings>0, drift=0, CLEAN` legal). Do **not** cross-count
`surfaces=`/`unavailable=` against `^SURFACE` rows: `probe_silence` appends lane rows
directly (`frozen/mori-census.sh:1564`) without incrementing `N_SURFACES`/
`N_UNAVAIL`, so such a count would be false-red on honest output.

**STATE-DUP-1 — duplicate lane row (state parsing, not verdict parsing).**

```bash
row=$(/usr/bin/grep -m1 '^SURFACE lane\.' <<<"$out") || row=''
flip=${row/: progressing /: unavailable }
printf '%s\n' "$out"
[ -n "$row" ] && printf '%s\n' "$flip"
exit "$rc"
```

Predicted at `34cd5770`: **28/28, exit 0** `[INFERENCE]`; the first-match reader wins.
Out of F02; name it as a residual unless L1 widens scope.

**LEAK-1 — per-run nonce in a malformed roll (regression found at `c4f8e63c`,
fixed at `34cd5770`).**

```bash
out=$(/usr/bin/sed -E "s/^MORI_CENSUS: .*/MORI_CENSUS: BANANA ${MORI_RUN_NONCE:-nonce-absent}/" <<<"$out")
printf '%s\n' "$out"
exit "$rc"
```

`MORI_RUN_NONCE` is exported to the SUT by `run_census`, so the wrapper can embed
the current run's token in a malformed roll. At `c4f8e63c`, `verdict_grade`
correctly redacted its own reason and `assert_case`/`readonly` printed only redacted
text — but `shape_observe` embedded the raw first roll line as `verdict=[…]` and the
verdict-contract-broken branch interpolated `shape_grade_a`/`shape_grade_b`
unredacted, so the `shape-invariance` FAIL line carried the literal nonce while
later census invocations could still read the oracle's stdout (r6 violation). At
`34cd5770` both points are redacted: `shape_observe` builds
`verdict=[$(redact "$v")]` (`:1105`) and the contract-broken branch redacts both
grades (`:1127`); `assert_case`'s rc-want reason also redacts `$verdict` (`:713`).
Retain the wrapper as a regression check: at `34cd5770` all 28 cases must fail
(tally 0/28, exit 1), and no `PASS`/`FAIL` line may contain the literal
`nonce-<N>` — only `nonce-<redacted>`. The only literal nonce on stdout is the
final `RUN_NONCE=` header line, printed after every case by design.

## 5. Acceptance conditions for OracleFix (preserve these)

1. Exactly one column-0 `MORI_CENSUS:` line; missing and duplicate are distinct
   reasons, never a first-match pass.
2. Full anchored grammar with the documented field order and integer tails.
3. `CLEAN ⇒ rc0`, `DRIFT ⇒ rc1`; rc>1 remains a setup/crash failure before grading.
4. `CLEAN ⇒ drift` text is exactly `0`; `DRIFT ⇒ drift` text starts `[1-9]`.
5. The roll is the last non-empty line.
6. All three consumers — 26 `assert_case` ids + `readonly-no-mutation` +
   `shape-invariance` (both sides) — apply the same gate.
7. Failure text is redacted — malformed line, shape grade and rc-want roll (verified
   by reading at `34cd5770`; LEAK-1 was open at `c4f8e63c`).
8. Registry still 28 ids, all want triples byte-identical; shuffle/nonce/re-exec
   untouched; no census-source inspection; here-strings only (QUALITY criteria 6-7).

## 6. Proposed checks for L1 (not run by this seat)

1. Honest control, pinned, twice, against the integrated census:
   `MORI_SHUFFLE_SEED=7 MORI_RUN_NONCE=11 bash tools/mori-silence-cases.sh`
   → exit 0, 28 `PASS`, `matched=28 total=28`, stderr 0 B, and the two runs’
   stdout byte-identical.
2. Repeat the honest control against the frozen census (`--census
   .ufo/waves/round-13/frozen/mori-census.sh`) before any mutant run; the frozen
   pair must reproduce the old 28/28 so the mutant gradient isolates the oracle.
3. M1-M6 (and M7) each: `bash tools/mori-silence-cases.sh <wrapper>` → exit 1,
   exactly 28 `FAIL`, `matched=0 total=28`, stderr lists 28 ids.
4. Pre-fix control: run the **frozen oracle** with M1-M6 against the frozen census
   and record the predicted gradient from §4 (28, 1, 28, 28, 9, 21 of 28). A
   different baseline is a finding, not a nuisance: it means the census state
   grading or the fixture split moved.
5. LEAK-1 regression check: run the fixed oracle with the nonce-carrying malformed
   wrapper; assert every per-case `PASS`/`FAIL` line contains no literal
   `nonce-<N>` (only `nonce-<redacted>`), and the shape failure says
   `nonce-<redacted>`. This channel was open at `c4f8e63c` and is closed at
   `34cd5770`.
6. TALLY-1: record as the named D02 residual (expected green until/unless L1
   widens the contract to counter reconciliation).
7. Evidence: capture argv, both artifact hashes, stdin-free environment pins,
   stdout/stderr, exit, and wall time; store under the harness `--output` path.
   Re-pin the oracle hash as a recorded act (QUALITY 10/13) because the F02 bytes
   change.

## 7. Risks and blockers

- **Concurrent bytes.** The live oracle and census both moved during this review.
  All fixed-oracle anchors are tied to `34cd5770`; re-anchor after the edit settles
  and before quoting line numbers in the report/LOG.
- **Joint grammar edit.** `VERDICT_RE` and the census emitter/usage must move
  together; a census tail change reds all 28 cases by design.
- **Honest control first.** The new `not-final` and word↔drift checks are
  honest-safe against the frozen census by source inspection, but the integrated
  census is still being edited; a late diagnostic after the roll or a new warn
  finding in a quiet fixture would be an integration defect, not an oracle defect.
- **D02 is only partly closed.** `findings`/`unavailable`/`surfaces` remain
  grammar-only (TALLY-1); duplicate state rows remain first-match (STATE-DUP-1).
  Both are named residuals, not claims of this fix.
- **LEAK-1 was a real regression in the new path** (open at `c4f8e63c`, closed at
  `34cd5770` by redacting the shape grade at construction and at the print site);
  keep its wrapper as a regression check and do not reintroduce a raw grade print.
- **Proxy boundary.** A proxy that recomputes the roll from rc is indistinguishable
  from a correct SUT; the oracle can only grade what the SUT emits (Appendix C’s
  own boundary). Do not claim “cannot forge”, only the tested classes.
- **No /tmp path is evidence.** The harness must commit the wrapper generator and
  expected digests (QUALITY 23).

## 8. Tool installs

None. No credential material, raw journal MESSAGE, process environment, or secret
path was read. The only non-public value observed was a synthetic `nonce-4242`
literal invented for the helper probe.
