# GateAllow — retention-gate allowlist / non-author / precedence audit (round-22, C1)

Seat: MoriR22.GateAllow (read-only scout). Scope: `tools/mori-retention-gate.py` plus its one directly
referenced public input `.ufo/waves/round-18/frozen/c1-policy.json` (structure and prose fields only;
regex bodies not printed). No tests, builds, selftests, or scans executed. No tools installed. No matched
text below.

## Provenance (observed)

- Gate file sha256 `cf0896a2ea36f169c9e900c58eefe7e2a900a4c9d67f849f753f4631d8ab829e`; `git diff 77a5bbe8 -- tools/mori-retention-gate.py` empty, worktree clean for that path; last touching commits `9db5168`, `b8f5c6c` (round-18).
- Policy sha256 `db06e9810bbfd243fb0a753a46960573df39083ea90174ce463cf2a0ab523128`; classes R1..R9; `must_redact_paths` = 3 round-17 build reports; `non_author_paths_glob` = `corpus/lessons/round-*-verifier-spotcheck.md`, `corpus/lessons/operator-*.md`. Literal must_redact ∩ non-author glob overlap: none (checked with `fnmatch.fnmatch`).
- LSP: no `lsp` device reachable from this seat; all symbol tracing is single-file text reading of the named file (self-contained, no imports of lane code). Treat as source reading, not semantic proof.

## 1. Allowlist classification (`_scan_result`, lines 226-307)

Per allowlist row, in allowlist order, a strict if/elif/else (lines 239-258):

1. `row.path in must_paths` → **forbidden** (`allowlist_forbidden`, `line: null`). Checked **before** any hit match: a forbidden row is forbidden whether or not it matches a hit, and is **never** stale and **never** added to `allowed_keys`.
2. else key `(path, class, line_sha256)` ∈ set of keys of **all** hits (non-author included) → allowed.
3. else → **stale** (`allowlist_stale`, emitted under `warnings`, `line: null`).

Consequences the reconciler MUST reproduce exactly:

- **Forbidden never allows.** A must_redact hit stays in `unallowlisted_hits`, counts in `metric` and `routed`. A forbidden row cannot make R11 clean: exit is 1 even when `metric == 0` (line 288).
- **Key is line-free.** Allowance binds `(path, class, line_sha256)`, not the line number: one row allows **every** occurrence of byte-identical lines of that class in that path (multiplicity > 1). Selftest arm M4 (lines 564-583) only covers a *different* line in the same path, not duplicate identical lines.
- **Stale is computed against the full hit set, including non-author hits.** A row that matches only a non-author hit is "used" (not stale), although it removes nothing from `metric`.
- **Setup validation precedes classification.** `_validate_allowlist` (lines 135-158) raises exit 2 for unknown class, bad digest, bad `rule` ∉ {a,b,c}, blank reason, extra/missing fields, or duplicate key, **before** forbidden/stale. An invalid forbidden row is SETUP, not `allowlist_forbidden`.
- **Wrapper acceptance:** allowlist JSON may be a bare list or a dict whose `rows` is the list (lines 317-319); other dict keys (including any schema) are ignored; dict without `rows` → `invalid_allowlist_shape`. `--allowlist ""` (falsy) silently means "no allowlist" (line 316). The receipt's argv must be checked for that.
- `forbidden_allowlist` / `warnings` entries carry `{finding_id, path, line:null, class, line_sha256}`, no reason/rule, in allowlist order.

## 2. Non-author overlap semantics

- `non_author_hits` = hits whose path `fnmatch.fnmatch`es any glob (line 260). `metric` set = hits that are **not** non-author **and** whose key is not allowed (lines 262-266).
- `allowlisted_hits` (line 261) is computed over **all** hits, so it **overlaps** `non_author` when a non-author hit is also allowlisted (policy adjudication rule (c) explicitly allows non-author rows). Therefore `len(hits) != non_author + len(allowlisted_hits) + metric` in general; the gate output has **no disjoint partition**. Recommended reconciler partition (disjoint, sums to `raw_total`): `non_author` (all), `allowlisted_author = allowed ∖ non_author`, `unallowlisted = metric set`, plus an explicit `non_author_allowlisted_overlap` count. Validate the receipt's `non_author`, `allowlisted_hits`, `unallowlisted_hits`, `metric` against **the gate's overlapping definitions**, not against a subtraction.
- **Non-author beats must_redact.** Non-author exclusion is applied before routing: `routed` (line 268) = unallowlisted ∩ must_paths, so a must_redact path matching a non-author glob would drop out of `metric` and `routed` silently, while a forbidden row on it would still force exit 1. `validate_policy` (lines 58-86) does not reject such overlap. Currently unreachable (no overlap in the frozen policy), but the policy prose `metric` field defines routed as "hits inside must_redact_paths" with no non-author carve-out. [INFERENCE] Reconciler should report `must_redact ∩ non_author` count explicitly (expected 0) instead of assuming it.
- Two population-summary definitions differ: `_population_summary.must_redact` (line 130) counts all must_paths hits incl. non-author; `routed` excludes non-author and allowlisted. They are equal only under zero overlap.
- **Glob semantics:** `fnmatch.fnmatch` uses `os.path.normcase` (case-insensitive on Windows, identity on Linux) and `*` crosses `/`. Observed: `corpus/lessons/round-3/deep/x-verifier-spotcheck.md` matches the first glob; `corpus/lessons/sub/operator-x.md` does not match the second. `[`…`]` is a character class. Reconciler must use the same function (or `fnmatchcase`, which is identical on this Linux host only) — "reproduce existing semantics" means not substituting `PurePath.match`/`glob` segment semantics.

## 3. Finding precedence (observed, lines 280-288)

Gate `finding_id` (one value) and exit code are computed separately:

| order | condition | finding_id | exit |
|---|---|---|---|
| 0 | any `EvaluationError` (policy/allowlist/population/git/revision) | `RETENTION_SETUP` + `error` only | 2 |
| 1 | `forbidden_rows` non-empty | `allowlist_forbidden` | 1 |
| 2 | `metric > 0` or `population_match is False` | `RETENTION_FINDINGS` | 1 |
| 3 | `stale_rows` non-empty | `allowlist_stale` | 0 |
| 4 | otherwise | `RETENTION_CLEAN` | 0 |

Masking the reconciler must account for (detail stays in other fields, not in `finding_id`):

- `allowlist_forbidden` masks `metric > 0` **and** population mismatch; `metric`, `routed`, `population_match` remain in the body.
- `RETENTION_FINDINGS` is ambiguous: `metric > 0` vs `metric == 0 ∧ population_match false`; disambiguate via `population_match`/`new_hits`/`missing_population_hits` (present only when `--expect-population` was supplied).
- `RETENTION_FINDINGS` masks stale rows; they remain in `warnings`.
- Stale alone is exit 0 (warning, not a failure).

**Determination (correct precedence for C1 reconciliation):** the existing order is internally consistent with the policy adjudication rule ("a must_redact_paths file may carry no allowlist entry and must scan to zero hits"): an allowlist integrity violation (forbidden) is a configuration breach and outranks counted findings; counted findings outrank advisory staleness. The contract requires reproduce-not-fix, so the reconciler MUST recompute `finding_id` with exactly orders 1-4 above and compare to the receipt's; it MUST NOT re-rank. Reconciler's own outcome precedence: SETUP (2: malformed/unsafe input, revision/ancestry, policy/allowlist byte drift) is decided before any comparison; then any disagreement in lists/counts/`finding_id`/exit → MISMATCH (1); else RECONCILED (0), including when the recomputed gate state is red. `retention_state` should carry the recomputed gate `finding_id` + exit verbatim (never a "clean" alias), and `privacy_clearance` stays false regardless of order 4.

## 4. Binding gaps relevant to R15/R16/R24 (observed)

- The gate reads policy and allowlist from **filesystem paths**, not Git blobs (lines 311, 317). `policy_sha256` binds raw policy bytes; the receipt's value must be compared to sha256 of the policy blob at both input and measured revisions (mismatch → SETUP, not silent current policy).
- **The allowlist bytes are not bound anywhere in gate output** (no digest field). Allowlist identity at r21 is verifiable only indirectly through `allowlisted_hits` / `forbidden_allowlist` / `warnings`. R16 must therefore rely on blob equality input-vs-measured revision; no receipt-side digest exists to cross-check.
- Tree scan includes symlink blobs (mode 120000 is `blob`; only `kind != blob` / `160000` skipped, line 199). The contract's symlink rejection applies to the **inputs** (receipt/policy/allowlist), not to scanned tree entries; rejecting tree symlinks would diverge from the gate.
- Paths decode with `utf-8, errors=replace` (line 202): two distinct non-UTF-8 tracked paths can collide, so the gate itself could emit duplicate `(path,line,class,line_sha256)` identities. The contract's "reject duplicate receipt hits" would then turn a faithful receipt into SETUP. [INFERENCE] Fail closed with a dedicated sanitized code (e.g. path-decode collision) rather than treating it as receipt tampering.
- `line_sha256` hashes the **re-encoded** decoded line (replacement chars, `\r` retained), not raw bytes; hits order = `ls-tree` order, then line, then policy class order. Comparing as a multiset is safe; list-order equality also holds for faithful receipts.

## 5. Selftest coverage gaps (for MutantPlan; not executed)

Uncovered combinations: forbidden + stale; stale + metric > 0; population-mismatch with metric 0; forbidden row matching no hit; non-author hit also allowlisted (overlap); one row allowing two identical lines; must_redact path also non-author. Mutating the if/elif order at 280-286, or moving the forbidden check after the hit-key check at 241/249, would survive the 21 arms for at least the forbidden+stale and no-hit forbidden cases. [INFERENCE from reading the arms at 598-645]

## Remaining unknowns

- r21 receipt argv (whether `--allowlist`/`--expect-population` were used, absolute vs relative paths) — not read (outside the named file).
- What the reconciler should do with a receipt whose `exit_code == 2` while recomputation succeeds (MISMATCH vs SETUP) — contract silent; L1 decision.
- Whether the round-18 frozen snapshot (`retention.json`, which embeds the policy) contributes hits that stay in `scanner_total` — [INFERENCE] yes under "remove the one policy file only"; not measured.
