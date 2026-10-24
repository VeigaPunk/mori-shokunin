# AttackR19 — frozen R19 "duplicate hit reject2"

Seat: MoriR22.AttackR19 (reviewer, static review only). No tests, selftests, builds or tool runs; nothing installed. Sources read: `contract.md`, `tools/mori-retention-gate.py` (762 lines, hit emission and normalization), the landed candidate `tools/mori-retention-reconcile.py` (274 lines, full read), `build/ReceiptBinding.md` (receipt shape), `build/AttackR06.md`, `build/AttackR18.md`, `build/GateRaw.md`, `build/RequirementTrace.md` (K6, ordering constraint). No separate fixture-builder or oracle artifact was readable under `build/` at review time; I did not wait for one.

## Axes

- A1 detection: a repeated receipt hit identity must be caught before any multiset comparison.
- A2 classification: the failure must be exit 2 / RETENTION_RECONCILIATION_SETUP, never 0 or 1.
- A3 key correctness: the duplicate key is the 4-tuple `(path, line, class, line_sha256)` — not the allowlist 3-key `(path, class, line_sha256)` and not `(path, line)`.
- A4 coverage: the check must apply to every receipt hit list (`hits`, `unallowlisted_hits`, `allowlisted_hits`), not only `hits`.
- A5 non-forgery and no-leak: a tampered receipt must never reconcile to 0, and the exit-2 payload stays sanitized (error token only, no hit data).

## The core trap (why R19 exists)

Contract line 13: "preserve duplicates as multiset but reject duplicate receipt hits." The asymmetric semantics is deliberate:

- **Recomputed side**: multiset (`Counter`) semantics, duplicates preserved.
- **Receipt side**: the existing gate can never emit two identical 4-tuples (`_blob_hits` gives unique `(path,line)` per file and appends once per matching class, `tools/mori-retention-gate.py:89-103`), so a repeated receipt identity is **unproducible** — tampering, i.e. a malformed input: exit 2, not a "valid receipt that disagrees" (exit 1) and never reconciled (exit 0).

The superficial-pass failure modes, in order of severity:

1. **Set-collapse → exit 0 (forgery reconciled).** An implementation that deduplicates receipt hits into a `set` before comparing accepts `hits = [H1, H1, H2, H3]` when recomputation is `{H1, H2, H3}` — the duplicate adds no new identity — and returns `RETENTION_RECONCILED` if the counters were left unchanged. This is the worst outcome: a tampered receipt validates clean. **This is exactly what R19a below must kill.**
2. **Multiset-only → exit 1 (misclassification).** A `Counter`-vs-`Counter` implementation without a prior duplicate check returns 1 on the same input. Wrong taxonomy: exit 1 certifies "well-formed receipt, disagreeing content", which a duplicate receipt is not. RequirementTrace:113 already pins the ordering constraint (R18/R19/R20/R21 rejection runs before multiset comparison); an oracle asserting only "nonzero" cannot tell 1 from 2.
3. **Crash-masked 2.** The candidate's `main` (`tools/mori-retention-reconcile.py:269-271`) maps any `OSError/ValueError/TypeError/KeyError/RecursionError` to `error: 'input_unavailable'` with exit 2. An oracle asserting only `exit == 2` passes an implementation that *crashes* in duplicate handling without ever reaching dedup logic. The oracle must assert the error token.
4. **Wrong dedup key → valid receipts rejected.** Deduping on the allowlist 3-key `(path, class, line_sha256)` (the gate's allowlist semantics, gate:235-266) falsely rejects a valid receipt containing the same line content at two line numbers of one path. Deduping on `(path, line, line_sha256)` falsely rejects the gate's own multi-class emission — a single line matching two classes yields two hits identical in everything but `class` (proven legal by the gate's own selftest, "multi-class-line" arm at `tools/mori-retention-gate.py:588-596`). Both are false-positive axes; the fixture below carries both inside the valid control.
5. **`hits`-only dedup.** If only the top-level `hits` list is normalized, a duplicate inside `unallowlisted_hits` or `allowlisted_hits` passes through to partition comparison — reaching 1 instead of 2, or 0 if counters were forged coherently.

## Landed candidate: observed R19 behavior

`tools/mori-retention-reconcile.py` exists (274 lines). What it does for R19, verified by reading, not running:

- `normalize_hits` (lines 119-126) validates each of `hits`, `unallowlisted_hits`, `allowlisted_hits` separately: exact 4-field dict, `path` non-empty str, `line` int-excluding-bool ≥ 1, `class` non-empty str, `line_sha256` 64-hex; then `require(key not in seen,'duplicate_receipt_hit')` on the 4-tuple. Correct key, correct coverage, correct exit path (`Invalid` → `main` → exit 2, `finding_id: RETENTION_RECONCILIATION_SETUP`, `error: 'duplicate_receipt_hit'`).
- `auxiliary` (lines 128-136) dedupes `forbidden_allowlist`/`warnings` rows on the 3-key — correct, since those rows carry `line: null` and are fully determined by `(path, class, line_sha256)` — with `error: 'duplicate_auxiliary'`.
- `parse` (lines 43-47) installs `object_pairs_hook=no_duplicates`, so `{"hits": […], "hits": […]}` at any level → `'duplicate_json_key'` → exit 2, at both wrapper and inner-`stdout` parse levels.
- Type check precedes the key check per row, so a second "copy" with `line: true` fails as `receipt_hit_type`, not a missed dup.
- The multiset comparison `claimed[field] != Counter(...)` runs only after all three lists normalize — setup precedence over mismatch, as recommended in AttackR06 §5.

### Gaps/ambiguities in the landed candidate (severity order)

1. **[HIGH — verification, not code] `--selftest` has zero R19 arms.** Lines 250-256 run exactly three subprocess arms: valid→0, unsafe path→2, unknown flag→2. No duplicate arm exists anywhere; if the frozen oracle reuses the tool's selftest as evidence, R19 is entirely unexercised. The contract requires "fixture generator and expected values committed before implementation integration" — R19 coverage must come from the committed oracle, and the arms below are what it needs.
2. **[MED — ambiguity, pin required] Same `(path, line, class)`, different `line_sha256`.** E.g. `(src/b.py, 2, R6, shaA)` and `(src/b.py, 2, R6, shaB)`. These are *distinct* 4-tuples: the candidate passes dedup, the multiset then differs → **exit 1**. Alternative reading: two rows for one line/class position is itself a duplicate (the gate emits exactly one sha per line) → exit 2. The contract's identity definition supports the candidate's 1; "reject duplicate" supports 2. **Must be pinned before expected values freeze; the candidate currently answers 1.** Arm R19e exposes whichever choice is made.
3. **[MED — ambiguity, pin required] Duplicates in `forbidden_allowlist`/`warnings`.** The candidate exits 2 (`duplicate_auxiliary`). Contract R19 says "hit" — auxiliary rows are allowlist-findings, not hits. The candidate's fail-closed answer is defensible; pin it or record the deviation. Arm R19g.
4. **[LOW] `scan` reuses `normalize_hits` on the *recomputed* list** (line 151). If recomputation ever produced a duplicate 4-tuple, it would exit 2 with the misleading token `duplicate_receipt_hit`, and the contract's "preserve duplicates as multiset" clause implies compare-not-reject. Under the candidate's strict UTF-8 path decoding (`tree`, line 76, `errors='strict'` → `invalid_tree_path`), the only known source of recomputed duplicates — two raw paths decoding to the same string under `errors='replace'` (gate line 202; GateRaw F1) — is unreachable: such trees fail earlier. A malformed tree object with a literally duplicated path entry would still hit it. Cosmetic token misattribution plus the already-flagged gate-vs-impl decode divergence; record, do not expand.
5. **[LOW] The `error` token does not identify which list carried the duplicate.** `duplicate_receipt_hit` is emitted for `hits`, `unallowlisted_hits`, and `allowlisted_hits` alike (dict-comprehension order: `hits` first). Keep every oracle mutant single-list so the token stays attributable.
6. **[LOW] Duplicate-JSON-key is a different code path and token** (`duplicate_json_key`). An oracle asserting `error == 'duplicate_receipt_hit'` on a `{"hits":…,"hits":…}` mutant fails a correct implementation. Treat it as a separate arm with its own token, or accept a `duplicate_*` token family.
7. **[boundary, not a defect] Cross-list repetition is required behavior.** Every `unallowlisted_hits`/`allowlisted_hits` entry also appears in `hits`; that is partitioning, not duplication. A "global dedup across all lists" fix would reject every valid red receipt — the valid control catches it.

## Concrete counterexample fixture F19 and arms

One-commit synthetic repo, committed expected values. Two policy classes so the multi-class false-dup control lives inside the valid receipt itself.

Files (UTF-8, LF):

- `policy.json`: `{"schema":"mori-retention-policy-v1","classes":[{"id":"R6","regex":"DUPEDGE_[0-9]+"},{"id":"R7","regex":"DUPEDGE_[0-9]+_X"}],"must_redact_paths":[],"non_author_paths_glob":["vendor/*"],"example":"DUPEDGE_9"}` — serialized `json.dumps(indent=2)` so the example sits on its own line → exactly 1 hit on the policy path (R6 only; `DUPEDGE_9` has no `_X` suffix).
- `allow.json`: one row `{path:"docs/a.md",class:"R6",line_sha256:sha256(b"DUPEDGE_1"),reason:"synthetic",rule:"a"}`.
- `docs/a.md`: `x` / `DUPEDGE_1` / `DUPEDGE_4_X` / `DUPEDGE_1` → hits: line2 R6 (allowlisted), line3 **R6+R7** (both classes match; unallowlisted), line4 R6 (allowlisted — same 3-key as line2).
- `src/b.py`: `a = 1` / `DUPEDGE_2` / `b = 2` → 1 unallowlisted R6 hit.
- `vendor/c.txt`: `DUPEDGE_3` / `z` → 1 non-author R6 hit.

Recomputed literals at commit C (contract denominator semantics): `raw_total=7`, `policy_excluded=1` (exact policy-path hits only), `scanner_total=6`, `non_author=1`, `forbidden_allowlist=0`, `raw_unallowlisted=4` (policy + line3 R6 + line3 R7 + src), `scanner_unallowlisted=3`, `allowlisted=2`. Receipt `metric=4`, `finding_id=RETENTION_FINDINGS`, wrapper `exit_code=1`, `retention_state=red`, `privacy_clearance=false`. (Note: the candidate currently emits `exclusion_basis:'non_author_paths_glob'` and reports `policy_excluded = non_author` — the flagged denominator divergence ReceiptBinding §8 and AttackR06's out-of-scope flag; R19 expected values must be pinned to contract semantics regardless.)

Control G = the well-formed `mori-r21-command-receipt-v1` wrapper for C: `hits` = the 7 identities above, `unallowlisted_hits` = the 4, `allowlisted_hits` = the 2, `forbidden_allowlist=[]`, `warnings=[]`, `stderr=""`, `argv` bound as the candidate requires (`--rev` == `measured_revision`, `--policy`/`--allowlist` repo-relative). **Required: exit 0, RETENTION_RECONCILED.** G itself exercises both false-dup controls: same `(path,class,sha)` on lines 2 and 4, and same `(path,line,sha)` with different classes on line 3. If either rejects, the dedup key is wrong.

### R19 arms (each = G + one mutation; single-list only)

| Arm | Mutation | Wrong-but-plausible result | Required |
|---|---|---|---|
| R19a | `hits` += second copy of the src/b.py identity, counters/lists untouched | set-collapse → **0 RECONCILED**; multiset → 1; crash-mask → 2/`input_unavailable` | 2, SETUP, `error=='duplicate_receipt_hit'` |
| R19b | same duplicate but at a non-adjacent `hits` index | adjacent-pair dedup misses → 0 | 2, same token |
| R19c | `hits` clean; `unallowlisted_hits` = each entry doubled | hits-only dedup → 1 or 0 | 2, same token |
| R19d | `hits` clean; `allowlisted_hits` doubled | hits-only dedup → 1 or 0 | 2, same token |
| R19e | `hits` += `(src/b.py,2,R6,sha_other)` — same position, different valid-hex digest | **AMBIGUITY — pin before freeze**: candidate exits 1 (multiset injection); position-duplicate reading exits 2 | pinned value; never 0 |
| R19f | duplicate in `hits` **and** `unallowlisted_hits` **and** `metric` 4→5 (coherent forgery) | dedupe-then-compare → 1 (counter lie) | 2, same token — dedup must precede all comparison |
| R19g | duplicate row inside `warnings` | "not a hit" reading → 1 | candidate → 2, `duplicate_auxiliary`; pin |
| R19h | `"hits"` key appears twice in the inner JSON | `json.loads` last-wins → 0 or 1 | 2, `duplicate_json_key` (distinct token — separate arm) |
| R19i | duplicate **plus** a dropped hit | ordering dispute → 1 | 2 — setup rejection precedes multiset comparison (RequirementTrace:113) |

Oracle assertions per exit-2 arm: stdout is exactly one JSON object; `finding_id == 'RETENTION_RECONCILIATION_SETUP'`; `error` equals the arm's exact token (not `input_unavailable`, not `invalid_json`); `receipt_match is False`; `privacy_clearance is False` (JSON bool); no `hits`/`raw_hits`/`raw_total`/hit-bearing field present; `stderr == ''`. Control G must return 0 in the same run, proving each 2 came from the mutation rather than fixture breakage.

## Exact actionable criterion

R19 passes iff, in the committed oracle (actual isolated CLI subprocess arms, not in-process calls):

1. G returns 0 with `RETENTION_RECONCILED` and the committed literal counters (`raw_total=7, policy_excluded=1, scanner_total=6, non_author=1, raw_unallowlisted=4, scanner_unallowlisted=3, forbidden_allowlist=0, receipt_match=true, privacy_clearance=false`).
2. Each of R19a-d, f, i returns exit 2 with `finding_id=='RETENTION_RECONCILIATION_SETUP'` and `error=='duplicate_receipt_hit'` — the token is required so a crash-masked `input_unavailable` or a JSON-layer `duplicate_json_key`/`invalid_json` cannot launder the arm.
3. R19g returns exit 2 with `error=='duplicate_auxiliary'` (candidate-consistent pin); R19h returns exit 2 with `error=='duplicate_json_key'`.
4. R19e's expected value is written explicitly after L1 pins the same-position/different-digest case (candidate's current answer: 1 MISMATCH). Whatever is pinned, 0 is forbidden.
5. No arm's stdout contains fixture line content or receipt hit records; every exit-2 stdout is the sanitized result object only.

## Superficial-pass risks (checklist for the Oracle)

- Asserting `exit == 2` without the error token → crash-masking passes.
- Asserting `!= 0` → exit-1 multiset misclassification passes.
- Asserting `finding_id` only → the same SETUP finding covers R17/R18/R20/R21; a mutant broken elsewhere (e.g. malformed JSON) satisfies it vacuously.
- Exercising duplicates only in `hits` → `hits`-only dedup passes.
- Missing the valid control → a too-broad dedup key (3-key or `(path,line,sha)`) is invisible.
- Counting the candidate's own `--selftest` as R19 evidence → it has no duplicate arm at all.
- Re-serializing mutants non-canonically → a 2 caused by JSON formatting rather than the duplicate; keep mutants differing from G in exactly the named arrays/values.

## Residual risk and verification gaps

- R19e and R19g expected values are unpinned in the contract; the candidate answers 1 and 2 respectively. If the frozen oracle pins differently, the candidate fails or the pin is silent — decide before expected values are committed.
- The candidate's strict UTF-8 path decode makes the contract's "preserve duplicates as multiset" clause unreachable-but-also-untestable on the recompute side (GateRaw F1 territory); a deliberately malformed tree remains the only trigger and yields a mislabeled `duplicate_receipt_hit`.
- The error token conflates the three hit lists; any future multi-list mutant loses attribution (avoided by single-list arms).
- Not verified (out of scope, static review): whether `git()` plumbing inside `check` can raise an uncaught `subprocess`/`Invalid` path that would mask dedup ordering; the except tuple in `main` covers the common cases but `subprocess.CalledProcessError`-style leaks were not exercised.
- No measurement was run: every "candidate exits X" claim above is derived by reading the code path (`Invalid` → `main` handler → `code=2`, `finding_id=SETUP`), not by execution.

Installs: none.
