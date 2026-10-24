# OracleFix — round 13 (F02 verdict integrity + structured journal stubs)

Owner: MoriR13.OracleFix (leaf executor). Assigned file: `tools/mori-silence-cases.sh`.
No other files touched; no commits; no checks run (L1 owns the integrated gate).

## Axes

- operability: the oracle can no longer be green while the final roll is not a
  verdict. All 28 case ids grade the complete `MORI_CENSUS` contract — word,
  admitted grammar, terminal position, rc and drift counter — instead of a
  prefix match.
- coverage: the contract is asserted in all 28 ids (26 through `assert_case`,
  2 through their own guards) and the quiet structured journal channel is
  confirmed against the census-side resolution chain.

## Defect repaired (audit-r11 F02 / Appendix C)

Anchor: `corpus/knowledge/audit-r11.md:156` (F02), `:376-407` (Appendix C
wrapper). Before this change the oracle read

    verdict=$(printf '%s\n' "$CASE_OUT" | grep -m1 '^MORI_CENSUS:' || true)

and only tested non-emptiness; `shape-invariance` tested the substring
`*"MORI_CENSUS:"*` anywhere in its grade line, and `readonly-no-mutation` did
not look at the roll at all. A proxy that rewrote `CLEAN`/`DRIFT` to `BANANA`
and preserved rc scored `matched=28 total=28`, exit 0.

## Changes (file: tools/mori-silence-cases.sh)

1. `verdict_grade <output> <rc>` (:594-647) — single admission gate. A roll is
   `ok` only when ALL hold; every other outcome is a reason that carries no raw
   target bytes except through `redact()`:
   - exactly one line begins `MORI_CENSUS:` (missing / duplicate rejected;
     numeric counts only in the reason);
   - the line matches the whole documented grammar (`VERDICT_RE`, :594):
     `^MORI_CENSUS: (CLEAN|DRIFT) \(findings=[0-9]+ drift=([0-9]+) unavailable=[0-9]+ surfaces=[0-9]+\)$`
     — census `usage()` "Verdict:" contract and `run_census`'s final printf.
     A malformed roll is echoed only through `redact()` (:607): it can carry the
     run nonce, and the r6 rule keeps run secrets off per-case stdout;
   - the roll is the LAST non-empty line (`awk 'NF{last=$0} END{print last}'`
     over the capture) — "final" means final; a moved/replayed roll fails
     `not-final`;
   - word/rc contract: `CLEAN=>0`, `DRIFT=>1`; `CLEAN` rc1 and `DRIFT` rc0 are
     `inconsistent`;
   - word/drift contract: `CLEAN` requires the captured digit string to be
     exactly `0`; `DRIFT` requires `[1-9][0-9]*`. `ROLL` flips to `DRIFT`
     exactly in `emit_finding`'s warn|crit branch together with `N_DRIFT`, so
     the word and the counter cannot disagree. The digits are compared as
     STRINGS, never through arithmetic: `$((10#…))` silently wraps (measured
     bash 5.3.15: `10#18446744073709551616` => `0`), so a forged
     `CLEAN drift=<2^64>` would pass a numeric `==0` test. `surfaces=`/
     `unavailable=` are NOT cross-counted: lane rows append to `SURFACE_LINES`
     directly (`SURFACE_LINES+=("SURFACE lane.` in `probe_silence`) and never
     increment `N_SURFACES`, so an honest run's `surfaces=` is smaller than its
     row count.
   The match runs over here-strings, so no live producer pipe exists for a
   consumer's early exit to SIGPIPE (`corpus/QUALITY.md` criterion 7). rc > 1 is
   rejected by the caller as a crash before this gate, never read as DRIFT.
2. `assert_case` (:669-700) — computes `vcheck=$(verdict_grade "$CASE_OUT"
   "$CASE_RC")` (:682); any non-`ok` value is an immediate FAIL before state,
   finding and rc wants (:691-700). The failure text prints `$vcheck` (already
   redacted) and the raw first roll line through `redact()`; the rc-want reason
   also redacts the roll (`:713`), so no branch can echo it raw.
3. `case_readonly_no_mutation` (:1049-1075) — validates the roll (:1062) after
   the mutation check and before the nonce; the guard is no longer exempt.
4. `case_shape_invariance` (:1096-1137) — each side is graded (`va`/`vb`)
   before equality, so equal-but-bad grades (same BANANA, same duplicate, same
   mismatch on both sides) cannot satisfy invariance; the old
   `shape_has_verdict` substring helper is deleted. `shape_observe` redacts the
   embedded roll at construction (:1101-1105) and the contract-broken print
   redacts both grades again (:1127), closing the r6 leak OracleFixtureDesign
   measured: a malformed roll can carry the run nonce and shape FAIL lines are
   written while later census invocations can still read stdout.
5. Header (:41-67) — documents the full admitted contract, the drift invariant,
   the terminal-position rule, the no-cross-count rule and the redaction rule;
   the "grades behavior only" bullet (:20-24) now says the roll is graded
   against its admitted grammar.
6. Structured journal stubs (:296-308 dispatcher, :375-382 skeleton) — see
   coordination below.

## Rejection matrix now enforced (all 28 ids, both guards)

| forged/absent roll | grade |
|---|---|
| `MORI_CENSUS: BANANA (…)`, rc preserved (Appendix C wrapper) | FAIL — `malformed` |
| no `MORI_CENSUS:` line | FAIL — `missing` |
| two or more `MORI_CENSUS:` lines | FAIL — `duplicate (N lines)` |
| valid roll followed by any other non-empty line | FAIL — `not-final` |
| `CLEAN (…)` with rc 1 | FAIL — `inconsistent (word=CLEAN rc=1)` |
| `DRIFT (…)` with rc 0 | FAIL — `inconsistent (word=DRIFT rc=0)` |
| `CLEAN (… drift=9 …)` rc 0 | FAIL — `inconsistent (CLEAN drift=9)` |
| `CLEAN (… drift=18446744073709551616 …)` rc 0 (wraps to 0 numerically) | FAIL — `inconsistent (CLEAN drift=18446744073709551616)` |
| `DRIFT (… drift=0 …)` rc 1 | FAIL — `inconsistent (DRIFT drift=0)` |
| valid `CLEAN (… drift=0 …)` rc 0 / `DRIFT (… drift>=1 …)` rc 1 as last line | admitted (state/finding/rc wants still apply) |

## What is preserved

- `CASE_IDS` still holds the same 28 ids in the same source order (counted:
  28); every `assert_case` want triple is byte-identical to before.
- Seeded Fisher-Yates shuffle, per-run nonce/salt, pin re-exec scrub, nonce
  assertion in every case, no census-source inspection — untouched.
- Aggregate/lane API expectations, nonce scope and want grammar unchanged.

## Structured journal stub coordination (C1 hand-off surface)

Confirmed against `MoriR13.CensusFix`'s exact schema (5 argv forms per scope,
`--user` and `--system`, `-o json --output-fields=_BOOT_ID,MESSAGE_ID` with the
three MESSAGE_ID filters plus `COREDUMP_SIGNAL=11`) and against
`MoriR13.JournalFixtureDesign`'s resolution chain (per-(scope,class) file >
per-scope file > legacy `journal`): the fixture answers every invocation with
0 bytes and rc 0 — a valid zero-record journal. Empty-query rc 0 was measured
on systemd 261.2 for both scopes; denial is rc1 plus an explicit permissions
message, so rc0/empty is the quiet arm. No synthetic `MESSAGE_ID`/`_BOOT_ID`
record is emitted, so the probe's `MESSAGE_ID`-equality/record-invalid path
cannot be triggered by the fixture.

In this file:

- `$CASE_STUB/journal` empty (text form / `--no-pager`);
- `$CASE_STUB/journal.json` empty (structured `-o json` / `--output=json` /
  `--output json`), routed by any journalctl argument containing `json`
  (:296-308);
- `$CASE_STUB/journal.rc` = 0 shared by both — the query ran; zero records.
- `MORI_BOOT_ID` is not set by the oracle: the census default
  (`/proc/sys/kernel/random/boot_id`) needs no fixture change.
- No case seeds journal content; keep both files empty (no text seeding).

## Risks / blockers

- The grammar, invariants and terminal-position rule are deliberately strict.
  If the r13 census changes the `MORI_CENSUS` tail, moves the roll, or emits
  anything after it, every case goes red by design — that is the contract check
  working, but it is a joint edit: `VERDICT_RE`/`verdict_grade` (:591-644) must
  move with the census emitter. [INFERENCE] CensusFix's MESSAGE_ID rewrite
  touches `probe_journal`, not the emitter/`run_census` order.
- Anchor policy (QUALITY 9): census line numbers shifted during CensusFix's
  rewrite (contract `:360`, warn|crit branch `:376-378`, lane row `:1729`,
  emitter `:1898` at this reading; earlier readings saw `:352-354`,
  `:366-371`, `:1684`, `:1733`). Code comments now cite census symbols
  (`emit_finding` warn|crit branch, `SURFACE_LINES+=("SURFACE lane.`,
  `usage()` "Verdict:" contract, `run_census`'s final printf) so they survive
  the rewrite; L1 must re-sweep the report's numeric pointers at the carrying
  commit.
- `not-final` assumes stderr is captured into the same stream (`run_census` uses
  `2>&1`). The census emits nothing after the roll; any future trailing
  diagnostic is a real contract change and should be raised with L1.
- Accepted residual (VerdictAttack V4/V7 nit): `inconsistent (… drift=%s)`
  prints the census-chosen digit string. The bare digits are not the
  `nonce-<N>` token that `redact()` masks, the census already receives
  `MORI_RUN_NONCE`, and the run header prints `RUN_NONCE=` only after all cases
  by design (r5/R1) — so this exposes no new channel. Kept for diagnosability.
- Accepted D02 tally residual (OracleFixtureDesign): `findings=`,
  `unavailable=` and `surfaces=` are grammar-checked only, so a wrapper that
  rewrites `findings=99` still passes. A safe partial closure exists —
  `findings=` must equal `count(^FINDING )` because every finding goes through
  `emit_finding` — but it is outside the instructed V1-V4 scope and was not
  applied. Row-counting `surfaces=`/`unavailable=` would false-red: lane rows
  append to `SURFACE_LINES` directly (`SURFACE_LINES+=("SURFACE lane.`) and
  never increment `N_SURFACES`; the oracle must not assume rows == surfaces.
- Claim limit: V1/V3/V4/V7 are source-level until L1 runs the negative rows
  (drift-tally wrapper, verdict-first/not-final wrapper, CLEAN 2^64). Only the
  L1 run promotes them to measured.
- Empty `journal.json` is a zero-record stream, not `[]`/`{}`; confirmed valid
  zero by both CensusFix and JournalFixtureDesign (only nonzero rc or non-JSON
  bytes make classes unavailable).

## Negative families handed to MoriR13.RegressionHarness

Tally shape (not blanket): BANANA, missing, duplicate and not-final fail all
28 (`matched=0 total=28`, exit 1); CLEAN rc1 / CLEAN drift>0 (incl. 2^64) fail
only CLEAN-emitting fixtures; DRIFT rc0 / DRIFT drift=0 fail only DRIFT-emitting
(id list in the message; `report-future-no-close` is `auto` and must be pinned
from a same-seed baseline). Shape fails on contract per side, not invariance.

## Proposed checks for L1 (not run here)

1. `bash -n tools/mori-silence-cases.sh`.
2. Pinned reproducibility, twice, expect byte-identical stdout and
   `matched=28 total=28`:
   `MORI_SHUFFLE_SEED=7 MORI_RUN_NONCE=11 bash tools/mori-silence-cases.sh`
3. Appendix C BANANA wrapper verbatim under `/tmp` (byte source:
   `corpus/knowledge/audit-r11.md:376-407`): expect `matched=0 total=28`,
   exit 1, every reason `malformed`.
4. Negative wrappers: delete roll (missing), append second roll (duplicate),
   append trailer after roll (not-final), CLEAN rc1, DRIFT rc0, CLEAN drift=9,
   CLEAN drift=18446744073709551616, DRIFT drift=0 — expected pass sets per the
   section above.
5. Confirm `CASE_IDS` count 28 and both guards present in `CASE_ORDER`.

## Retained evidence

- `corpus/knowledge/audit-r11.md:156` — F02 statement; `:376-407` — exact
  BANANA proxy and its pre-fix `matched=28 total=28`, exit 0, stderr 0.
- Census symbols (line numbers at this reading): `usage()` "Verdict:"
  contract `:360`; `emit_finding` warn|crit branch `N_DRIFT`/`ROLL` `:376-378`;
  `probe_silence` lane row append `:1729`; `run_census` emitter `:1898`.
- `corpus/QUALITY.md` criteria 6, 7, 9 — rc-gating, no live producer pipe in a
  match test, pointers resolve at the carrying commit.
- Peer review applied: MoriR13.Safety (raw-line redaction, drift invariant),
  MoriR13.VerdictAttack (tally corruption, terminal position, redaction, and
  the `10#` wrap hole at `drift=`), MoriR13.OracleFixtureDesign (r6 leak in
  shape grade diagnostics, D02 tally residual), parent MoriR13 (apply V1-V4,
  no aggregate/want/nonce broadening), MoriR13.JournalFixtureDesign (stub
  chain confirmation).

## Tool installs

None.
