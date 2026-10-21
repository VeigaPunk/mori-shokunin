# AttackR23 — static attack on frozen requirement R23 "no matched-text leakage"

Seat `MoriR22.AttackR23`. Static review only; no tests, builds, gates, or scanners run. No tools installed or updated (none needed — reads only). Sources read: `contract.md`, `frozen/fixture-builder-v2.py`, `frozen/requirements-v2.json`, `oracle-reconcile-v2.py` (the pinned oracle per `requirements-v2.json.oracle_sha256` / `measure-round22.py`), `refinement-reconcile.py`, `measure-round22.py`, `frozen/expected-real.json`, `denominator-correction.md`, `tools/mori-retention-gate.py`, `build/RawPartition.md`. The v1 oracle/builder are superseded; all oracle citations are to **v2**. No matched text from real data is reproduced; only synthetic builder tokens are named.

## 1. What R23 currently is — and why it is superficially passable

R23's *entire* enforcement is one line (`oracle-reconcile-v2.py:60`):

```python
record('R23',predicate=lambda v,f:'R22_SAMPLE' not in json.dumps(v) and 'retained-red' not in json.dumps(v) and v['privacy_clearance'] is False)
```

applied to **only the `valid` arm**, to **only `json.dumps(v)`** — i.e. the *re-serialization of the parsed stdout JSON object* — against **two** sentinel substrings. Every other recorded arm (`R05`–`R21`, the conjunctive `bool-metric` probe at line 56, and the `receipt_override` run at line 57) asserts `exit_code`, `finding_id`, `isinstance(v,dict)`, and `stderr==''` **with `predicate=None`** — stdout content is never substring-checked outside the valid arm. `refinement-reconcile.py` likewise records `stdout` but asserts only exit/finding/`error`/`privacy_clearance`/`receipt_match`/empty-stderr (`refinement-reconcile.py:61-64`). `measure-round22.py` `real-reconciliation` checks a key-value allowlist on the parsed object and ignores extra keys (line 81); `--selftest` is asserted exit-only (`sr==0`, line 111) — its text is never scanned.

So the frozen check is: *one channel (parsed stdout), one arm (valid), two substrings, post-re-serialization.* That is a subset of "no matched text emitted" in every dimension.

## 2. Concrete counterexample fixtures (each passes the whole pinned oracle while emitting matched text)

Fixture ground truth (v2 builder, all arms share): tracked blobs `policy.json`, `allowed.txt`, `unallowed.txt`, `non-author.txt`, `binary.bin` (NUL, skipped). Raw hits = 5: `policy.json:1` (the `"synthetic"` line's match), `allowed.txt:1-2`, `unallowed.txt:1`, `non-author.txt:1`. Matched-line payloads are the token `R22_SAMPLE` plus four payload words: `allowed` (×2), `retained-red`, `outside-author`. Expected `valid` arm: exit 0, `RETENTION_RECONCILED`, raw_total 5 / policy_excluded 1 / scanner_total 4 / raw_unallowlisted 1 / scanner_unallowlisted 1 / non_author 1 / forbidden_allowlist 0, `retention_state='red'`, `privacy_clearance=false`.

**CE-1 — leak inside an exit-2 payload (strongest, zero cost to implementer).** Variant `malformed` (R17): receipt bytes are `{bad`. SUT emits exit 2 with stdout `{"finding_id":"RETENTION_RECONCILIATION_SETUP","error":"invalid_json","detail":"<verbatim receipt bytes / any matched line>"}`. Expected: exit 2, `RETENTION_RECONCILIATION_SETUP`, stderr empty. Oracle: R17 **passes** (no predicate); R23 **passes** (checks the valid arm only). Refinement case `malformed-stdout` also passes — it asserts only `obj.get('error')=='invalid_json'`; a `detail` key is unconstrained. Contract exit-2 clause says "sanitized error code only, never arbitrary bytes" — the *vocabulary exists and is unenforced.*

**CE-2 — leak inside an exit-1 mismatch payload.** Variant `drop` (R05) or `inject` (R06): SUT emits exit 1 with `{"finding_id":"RETENTION_RECONCILIATION_MISMATCH","diff":"<receipt stdout fragment or scanned matched line>"}`. R05/R06 pass; R23 untouched. This is the *most likely* honest defect — diffing is the natural way to report a mismatch, and the tool holds every matched line in memory.

**CE-3 — leak on the valid arm that evades the two sentinels.** SUT emits a correct `RETENTION_RECONCILED` object plus `"context":{"source":"outside-author"}`. `outside-author` is real matched-line content (the `non-author.txt` payload) but is **not in the sentinel set** — R23 passes while emitting scanned line content. Same for `allowed` / `must-not-count`. The sentinel list covers 2 of ≥5 payload words.

**CE-4 — valid-arm leak invisible to `json.dumps(v)`.** (a) Duplicate JSON keys: stdout `{"note":"R22_SAMPLE …","note":"ok"}` — `json.loads` keeps the last value; the emitted bytes contained the token but `json.dumps(v)` does not. (b) Any non-JSON noise line printed before/after the JSON object is invisible to the check yet is emitted matched text. (c) A field split across values — `{"a":"R22_","b":"SAMPLE retained-red"}` — emits the full regex match in stdout while no parsed *value* contains the sentinel. (d) Non-ASCII payload: `json.dumps` defaults `ensure_ascii=True`, so a leaked `é…` line re-serializes as `\uXXXX` escapes, defeating literal substring checks — latent today (ASCII fixture), live the moment a fixture line goes non-ASCII.

**CE-5 — unchecked channels.** (a) `--selftest`: measured by `measure-round22.py` with `sr==0` only; a selftest that prints `arm valid: line "R22_SAMPLE retained-red"` passes `all_claim_checks_pass`. (b) Real-receipt run: extra keys ignored; the real allowlist carries free-text `reason`/`rule` row fields (synthetic rows already carry `reason='synthetic field name only'`) — a SUT that echoes row reasons verbatim emits input free text on every arm, unchecked everywhere. (c) `binary.bin` preview on R22's arm: R22's predicate inspects `v['raw_hits']` paths only; a `"skipped_blob_preview":"R22_SAMPLE\x00must-not-count"` field passes R22 *and* R23 (R23 is a different arm anyway — double-blind).

**Oracle fragility (secondary):** `subprocess.run(text=True)` — a SUT emitting non-UTF-8 bytes to stdout raises `UnicodeDecodeError` in the oracle itself, crashing the run before any result is recorded; an entire suite lost rather than one failed arm.

**Evidence double-leak:** `data['runs']` stores raw `cp.stdout`/`cp.stderr` verbatim into the observation JSON (`oracle-reconcile-v2.py:38`); refinement does the same (line 65); `measure-round22.py:34` writes every captured stdout into retained receipts. Any CE leak is **re-persisted into committed evidence** — the oracle becomes the leak channel. The leak check must run *before* evidence write, or evidence must be sanitized.

## 3. Semantic ambiguities requiring a pinned ruling

1. **"matched text" scope:** the regex match (`R22_SAMPLE`) vs. the entire matched line vs. any scanned blob bytes (incl. `must-not-count` in a NUL-skipped blob, and `unmatched` line content). Oracle checks the match + 1 of 4 line payloads — all three readings are currently under-enforced.
2. **"emitted" scope:** stdout JSON only? stderr on exit 1/2? `--selftest`? exception tracebacks? evidence files downstream? Contract bans arbitrary bytes on exit 2 but names no channel set.
3. **Identity vs. content:** hit tuples are `(path, line, class, line_sha256)` — digest-only is sanctioned. Is `path` leak-safe when the *filename itself* is sensitive? Contract R24 forces `argv` echo which contains absolute repo paths — a filename containing the token would trip the sentinel check as a false positive. Pin: R23 guards *line/blob content*; paths and digests are identity, not content. No fixture distinguishes this today.
4. **Transformed leaks:** base64/hex/sliced/reversed fragments, or substrings of the line — is `UjIyX1NBTVBMRQ==` a violation? Contract silent; substring checks can't see it. The only robust rule is output-schema whitelisting (§4.2).
5. **Receipt pass-through:** receipt `stderr`/free-text fields may contain arbitrary user bytes. Is echoing them "leakage"? If yes, receipts must be treated as untrusted content and never echoed verbatim — currently unenforced on every arm.
6. **R23 atomicity:** the predicate conjunct `v['privacy_clearance'] is False` duplicates R02/R11 semantics. It makes R23 non-atomic (a clearance defect reports as an R23 failure) while adding zero leak coverage.

## 4. Exact actionable criterion

**R23 passes iff all five hold; each is implementable in the existing oracle without new dependencies:**

1. **All-arms raw-channel check.** For *every* `runs` row (all variants incl. `bool-metric`, `receipt_override`) plus the `--selftest` invocation and the real-receipt run in `measure-round22.py`: `assert all(p not in cp.stdout and p not in cp.stderr for p in payloads)` where `payloads` = every scanned matched line's payload set exposed by the fixture builder (`f['payloads']` — add it: per-blob list of matched line strings). Check **raw `cp.stdout`/`cp.stderr` strings, not `json.dumps(v)`** — kills CE-1/CE-2/CE-4a/CE-4b and the non-ASCII escape (CE-4d) in one move.
2. **Output-schema whitelist on failure arms.** exit-1/exit-2 payloads may contain only: `finding_id`, `error` from the enum already frozen by `refinement-reconcile.py` (`receipt_revision_conflict`, `input_not_regular`, `policy_changed`, `allowlist_changed`, `receipt_exit_type`, `receipt_counter_type`, `receipt_path_binding`, `invalid_json`), and structured counter/identity keys. Any other string-valued field fails the arm. This is the *fail-closed* form of "sanitized error code only" and is the only defense that also covers CE-3, CE-5b, and transformed leaks.
3. **Payload-evasion fixture line.** One fixture matched line must contain a control char + a non-ASCII byte, so any reproduction of it in output is caught by rule 1 in raw bytes regardless of escaping.
4. **Negative-control mutants** added to `measure-round22.py` `mutations` (currently 3, none exercise R23): `leak-error-arm` (emit a matched line in a `detail` field on an exit-2 arm), `leak-split` (emit the payload split across two fields on the valid arm), `leak-selftest` (print the token in `--selftest`). Each must produce `rc==1, unmet>0` — without them a green R23 is unfalsified.
5. **De-conflate:** move `privacy_clearance is False` out of the R23 predicate (R02/R11 own it). Keep R23 purely about emitted content.

## 5. Residual risk after the fix

- Substring checks can never see transformed leaks; mitigation is rule 2 (schema whitelist) — accept that rule 1 alone is not proof.
- "Matched text" vs. path-as-identity stays a judgment call; recommend pinning "line/blob content only" explicitly in the contract text since R24 forces path/`argv` echo.
- `UnicodeDecodeError` oracle crash needs `text=False` + explicit decode to keep a hostile-stdout SUT as a failed arm rather than a lost run.
- Evidence retention currently copies raw subprocess stdout into committed observation files; even with checks added, sanitize or hash-gate `runs[].stdout` so a future undetected leak is not persisted.
