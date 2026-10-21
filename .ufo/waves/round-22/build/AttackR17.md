# AttackR17 — "malformed JSON returns2" (R17) attack review

Seat: MoriR22.AttackR17 (reviewer, read-only). Scope: R17 in
`.ufo/waves/round-22/contract.md`. Reviewed: contract, `tools/mori-retention-gate.py`
(existing gate, receipt producer semantics), `.ufo/waves/round-22/frozen/fixture-builder.py`,
`.ufo/waves/round-22/oracle-reconcile.py`, `.ufo/waves/round-22/frozen/requirements.json`,
`build/ReceiptBinding.md`. Static review only; no tests, builds, or gate runs executed.
SUT `tools/mori-retention-reconcile.py` is absent at HEAD (also noted in ReceiptBinding.md:20),
so the measured baseline remains `capability_absent` per `frozen/requirements.json` (`before_kind`).

## Axes (godspeed)

1. Layer coverage — which JSON layers the frozen malformed arm actually exercises.
2. Exit-code discrimination — setup(2) vs mismatch(1) vs interpreter crash(also 1).
3. Sanitization — "sanitized error code only, never arbitrary bytes or exception text".
4. Strictness/edge inputs — Python `json.loads` permissiveness vs RFC-strict JSON.
5. Oracle fixture gaps — what a superficial SUT passes without satisfying the contract.

## What the frozen R17 arm actually is (verified)

`frozen/fixture-builder.py:93`: `if variant=='malformed': (root/RECEIPT).write_bytes(b'{bad')`
— the committed receipt **blob itself** is unparseable. `oracle-reconcile.py:54` then
`record('R17','malformed',2,'RETENTION_RECONCILIATION_SETUP')`, and `record()` (lines 40-46)
additionally requires stdout to parse as a JSON dict and `cp.stderr==''`.

So R17 as committed tests exactly one layer: outer receipt-wrapper unparseable.
`measured_revision` is unobtainable from `b'{bad'`, so every downstream check is vacuous;
any SUT that wraps one `json.loads(receipt_blob)` in try/except and returns 2 on failure
passes R17 while leaving the contract's real malformed-input surface untested.

## Concrete counterexample fixtures (primary + secondary)

### C1 (primary — the layer the frozen arm never touches): malformed `stdout` inside a valid wrapper

Construct as a new variant `'malformed-stdout'` beside line 93 of fixture-builder.py:
build the `'valid'` fixture unchanged, then before writing the receipt do
`wrapper['stdout'] = json.dumps(result)[:-20]` (truncated mid-token), leaving
`measured_revision`/`argv`/`exit_code`/`stderr` fully valid and correctly typed.

- Receipt blob: parses cleanly; `measured_revision` is a valid ancestor; policy/allowlist
  byte-equality holds. Every setup gate passes. Only the embedded payload is unparseable.
- Expected: exit **2**, stdout is one JSON object with
  `finding_id == "RETENTION_RECONCILIATION_SETUP"`, `stderr == ""`.
- Expected counters: **none emitted**. The run is unevaluable, so the setup emission MUST NOT
  carry `raw_total`/`scanner_total`/`receipt_match`/`privacy_clearance` success fields or
  fabricated zero counts. Emitting `raw_total: 0` on a receipt it could not read would be a
  counter lie equivalent to R10. Digest fields for actually-loaded inputs MAY appear.
- Kills SUT classes: (a) uncaught `json.JSONDecodeError` on `wrapper['stdout']` → interpreter
  exit **1** colliding with MISMATCH; (b) parse failure folded into "empty population" →
  recomputation disagrees → exit **1** MISMATCH, which wrongly asserts a *valid receipt
  disagreed* — the exit-1 definition in contract line 15 requires a valid, evaluable receipt;
  (c) `str(exc)` or the raw stdout fragment echoed into `error` → sanitization violation.

### C2: parseable `stdout`, wrong JSON type

`wrapper['stdout'] = 'null'`, `'[]'`, `'123'`, `'""'`, and `''` (empty). All five parse or
miss cleanly; none is a hit-bearing retention object. Expected exit **2** under
"required field/type/schema inconsistencies must fail closed". A SUT that parses, then does
`payload.get('hits', [])` (AttributeError → crash path) or treats non-dict as zero hits
(→ MISMATCH exit 1) is exposed. Missing `stdout` key entirely is the same arm.

### C3: deep-nesting receipt blob — exception-class coverage

Receipt blob `b'[' * 3000`: `json.loads` raises `RecursionError`, a `RuntimeError` —
**not** a `ValueError` and not `json.JSONDecodeError`. The gate's own pattern
(`read_json`, gate line 53: `except (OSError, UnicodeError, json.JSONDecodeError)`)
would not catch it; only the gate's outer `except Exception` (line 754) saves it.
A SUT copying only the narrow except clause exits **1** with a traceback on stderr
(double violation: wrong code, unsanitized bytes). Expected exit **2**.

### C4: equal-byte malformed policy (R15/R16 intersection — coverage gap, no seat owns it)

Variant `'malformed-policy'`: set `files[POLICY] = b'{bad'` at **both** commits so the
input-rev vs measured-rev byte-equality check (R15) is *satisfied*, and update the receipt's
inner `policy_sha256` accordingly. The SUT cannot skip parsing policy bytes just because
they are equal — `validate_policy` must still run and must fail closed. Expected exit **2**.
A SUT that skips the parse on equality, or crashes on `json.loads(policy_bytes)`, is exposed.
Same arm for `--allowlist` (R16). The committed fixture family has no equal-byte-malformed
input arm at all — equality is only ever tested with valid JSON (R15/R16 append `\n`).

### C5: non-strict JSON literal in payload

`result['metric'] = float('nan')` before `json.dumps` → `stdout` contains literal `NaN`.
Python `json.loads` accepts `NaN`/`Infinity` (non-RFC); a SUT using `json.loads` parses it,
then `nan != recomputed` → exit **1** MISMATCH. If "malformed JSON" is meant RFC-strict,
expected is exit **2** (parse via `parse_constant` raising, or `math.isfinite` validation).
Flag as ambiguity (below) — but the current text rewards either reading being pinned.

### C6: empty and non-UTF-8 receipt blobs

Receipt blob `b''` and `b'\xff\xfe{bad'` (invalid UTF-8 → `UnicodeDecodeError`, caught by the
gate's `UnicodeError` clause but a distinct path from `JSONDecodeError`). Expected exit **2**.

### C7: encoding-detection divergence

`json.loads(bytes)` auto-detects UTF-8/16/32 BOMs; `json.loads(raw.decode('utf-8'))` (the
gate's own pattern) does not. A UTF-16-BOM receipt parses under the first and fails under the
second. Same for `"\ud800"` lone-surrogate escapes (accepted by `loads`, crashes later
`.encode()`). If the SUT parses where the producer-class would not, "malformed" is
implementation-defined. Expected: reject non-UTF-8 receipt/policy/allowlist bytes → **2**.

## Semantic ambiguities in R17 (to pin before integration)

1. **Layer scope.** "malformed JSON" binds the receipt blob in the fixture, but contract
   line 15 lists "malformed/unreadable input" as an exit-2 class and the receipt's *payload*
   is the object under reconciliation. Malformed `stdout`, malformed policy blob, and
   malformed allowlist blob all fit "malformed input" and none is a "disagreement". Pin:
   R17 covers every JSON input at every layer — receipt wrapper, embedded stdout payload,
   policy, allowlist — each → exit 2.
2. **Strictness.** Python `json.loads` accepts `NaN`/`Infinity`, UTF-16 BOM on bytes input,
   lone surrogates, and duplicate keys (last wins). Whether these are "malformed" is
   unspecified. Recommend: decode UTF-8 strictly first (gate parity), reject non-finite
   numbers and duplicate keys in required fields, or explicitly record the permissive
   reading. Both arms are one-line fixture mutations; leaving it unpinned lets a
   NaN-accepting SUT turn a malformed receipt into a fabricated exit-1 mismatch.
3. **Boundary vs R05–R10.** A receipt that cannot be evaluated is not "a valid receipt
   [that] disagrees" — exit 1 is reserved for evaluated disagreement. Any parse/typing
   failure anywhere upstream of comparison must be 2, never 1. This is the single most
   important pinning because Python's uncaught-exception exit code is **also 1**.
4. **Sanitization granularity.** "sanitized error code only" — the `error` field must be a
   fixed enum token, not `str(exc)` ("Expecting value: line 1 column 1"), not a byte echo of
   the input. On a real receipt the input can contain retained matched text (R23 only runs
   the 'valid' variant, so nothing else guards the failure path).
5. **Missing vs malformed.** Missing `stdout`/`measured_revision` keys, wrong-typed keys
   (string `exit_code`), and unparseable documents are all exit 2 — the shared code hides a
   distinction the `error` enum should still make (e.g., `receipt_unparseable` vs
   `receipt_schema`), but only the exit/finding contract is frozen; error-token naming is
   the SUT's.

## Superficial-pass risks (ranked)

- **P1 — outer-only guard.** `try: receipt = json.loads(blob) except: return 2` passes R17
  while malformed stdout crashes with exit 1 (interpreter default), which is both the wrong
  code and a channel collision with MISMATCH. The frozen arm cannot detect this.
- **P2 — exception-text echo.** Oracle asserts only `finding_id` + `stderr==''`; it does not
  check that `error` (or any field) avoids input bytes/exception text. A SUT emitting
  `{"finding_id":"RETENTION_RECONCILIATION_SETUP","error":"{bad"}` passes R17 while violating
  contract line 15 — and the identical code path on a real receipt leaks matched text.
- **P3 — blob-vs-worktree invisibility.** For the malformed arm, the committed blob and the
  worktree file are byte-identical (`{bad` is committed at line 98), so R17 cannot
  distinguish a SUT that reads the receipt from the worktree. That violation is carried by
  R24/digest arms, not R17 — worth noting so no one cites R17 as blob-read evidence.
- **P4 — blanket-2 SUT.** A SUT returning 2/SETUP on every input passes R17 trivially; the
  falsification is collective (R01/R02 force the success path), so R17 alone proves nothing
  about discrimination. Noted for completeness; no extra arm needed.
- **P5 — equality-shortcut.** With no equal-byte-malformed arm, a SUT that treats
  "policy bytes equal across revisions" as proof of evaluability never parses policy and can
  pass R15/R16 while failing open on C4-class input.

## Exact actionable criterion for R17 (proposed replacement text)

> **R17:** For every JSON input layer — the receipt blob, the receipt's `stdout` payload,
  the policy blob, and the allowlist blob — any failure to produce a JSON value of the
  required schema type (unparseable bytes, non-UTF-8, empty, wrong top-level type, missing
  required key, non-finite literal, recursion/depth failure) yields exit **2** with
  `finding_id == "RETENTION_RECONCILIATION_SETUP"`, `stderr == ""`, and an `error` field that
  is a fixed enum token containing no bytes copied from the input and no exception text.
  No evaluation counters, hit lists, or clearance fields are emitted on this path.
  Specifically, a byte-identical-but-malformed policy or allowlist at both revisions must
  still fail closed (equality is not evaluability).

Minimum additive fixture arms to enforce it: `malformed-stdout` (C1), `stdout-nonobject`
(C2), `deep-nest` (C3), `malformed-policy`/`malformed-allowlist` equal-byte (C4). C5–C7 are
ambiguity-pinning arms pending the strictness ruling. All are ≤5-line deltas to
`frozen/fixture-builder.py` using existing `make()`/`encoded()` machinery.

## Oracle hardening (one line, zero new arms)

In `oracle-reconcile.py:record()`, extend the `ok` predicate for the setup family to assert
`v['error']` is absent or matches `[a-z0-9_]+` and shares no ≥3-byte substring with the
fixture's malformed payload — this closes P2 without new variants.

## Verification performed

Static reads only: contract (all lines, incl. truncated 11/13/19), gate `read_json`/`main`
error paths and `scan`/`_scan_result` semantics, fixture-builder variant table, oracle
`record`/`invoke` mechanics, ReceiptBinding wrapper-shape facts. No tools run, no installs
performed (none needed; pacman paused host-wide per bounds). Nothing claimed executed.
