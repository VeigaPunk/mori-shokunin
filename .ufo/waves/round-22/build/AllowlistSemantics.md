# AllowlistSemantics — round 22 scout report (seat MoriR22.AllowlistSemantics)

Scope: `corpus/evidence/retention-allowlist.json` plus its sole consumer `tools/mori-retention-gate.py` (read-only, targeted sections). Metadata only; no matched line text read into or emitted from this report. No tests/builds/gates run. No tool installs.

## Axes
1. Schema shape and validation strictness.
2. Uniqueness dimensions (row key vs hit identity).
3. Line-number omission → repeated-line fan-out.
4. Precedence/partition interactions (forbidden, stale, non-author).
5. Provenance/stability of the blob.

## Observed facts

### Blob identity
- Git blob `f8be55b1204bbb0b54b5f089407a4a10c8145b15`, identical at HEAD `306e06ecd02e…` and entering revision `77a5bbe8a0b4…`; worktree clean for this path; file SHA-256 `f46c78ec…0c63b`.
- Single commit in history: `3127c3a0aec4` "round-18: C1 retention allowlist (86 name-only rows, L1 rulings)"; it is an ancestor of HEAD.

### Schema
- Top-level keys: `schema` = `mori-retention-allowlist-v1`, `note`, `rows`.
- 86 rows; every row has exactly `path, class, line_sha256, reason, rule`, all JSON strings. All 86 digests match `^[0-9a-f]{64}$`.
- `rule`: 79 × `a`, 7 × `b` (`c` permitted by gate, unused). `reason`: exactly 2 distinct strings (79 rule-a, 7 rule-b).
- Class histogram: R2 2, R4 8, R5 12, R6 33, R7 10, R8 7, R9 14.

### Gate consumption (`tools/mori-retention-gate.py`)
- `scan()` L317–320: if top-level is a dict, takes `.get("rows")`; a bare list is also accepted. **`schema` and `note` are never checked**; a wrapper with a wrong/absent schema string still loads. A dict without `rows` → `None` → `invalid_allowlist_shape` (exit 2).
- `_validate_allowlist` L135–158: exact field-set equality per row; `path` non-empty str (no safety/normalization check); `class` must be a policy class id; digest regex; `reason` non-blank; `rule ∈ {a,b,c}`; **duplicate key `(path, class, line_sha256)` rejected** (`duplicate_allowlist_row`). `reason`/`rule` are not part of the key.
- Hit identity (`HIT_FIELDS` L31, `_hit_tuple` L106): `(path, line, class, line_sha256)`. Allowlist key (L235–266): `(path, class, line_sha256)` — **no line**.
- Digest = SHA-256 of the line after `decode("utf-8", errors="replace")` and `split("\n")` (L92–101); CR is retained, empty lines hashed, NUL blobs skipped.

### Uniqueness measurements (run by this seat, counts only)
- Duplicate `(path, class, line_sha256)`: 0 (consistent with gate rejection).
- Distinct `(path, line_sha256)`: 56; distinct `line_sha256`: 56; digests shared across >1 path: 0; distinct paths: 29.
- Multi-class lines: 6 `(path, digest)` pairs carry 2 class rows, 8 carry 4 class rows (6·2 + 8·4 + 42·1 = 86). This is the intended per-class row model (gate selftest M5: one line matching two classes counts once per class).
- Per-row line multiplicity in its own path blob, gate decode/split/hash rules, at both HEAD and `77a5bbe8`: **every one of the 86 digests occurs exactly once** (histogram `{1: 86}`); 0 rows reference absent paths; 0 NUL-skipped paths. Policy-class regexes were **not** run, so this does not prove each row is a live (non-stale) hit, only that its line exists once.
- `.ufo/waves/round-18/frozen/c1-policy.json` (the path the gate selftest loads as policy, L470) carries 4 rows (R2, R5, R6, R8), each digest occurring once.

## Implications

### Line-number omission / repeated lines (latent, not currently exercised)
- Because the key drops `line`, one row allowlists **every** hit in that path with the same class and identical line text. `allowed_keys` is a set and `allowed_hits` (L261) counts hits, so `len(allowlisted_hits) ≥ matched rows`; a reconciler must not equate allowlisted-hit count with row count.
- Consequences: (a) a later commit adding another identical copy of an allowlisted line in the same file is silently allowlisted (new hit, metric unchanged); (b) line moves/insertions elsewhere do not stale the row (stability by design); (c) removing one of several copies is invisible to stale detection (stale only when all copies vanish).
- Gate selftest comment at L564–565 ("an allowlist row binds one hit … never every hit in the same path") is accurate only for *distinct* text; no selftest arm covers two identical lines in one path. [INFERENCE] An independent reconciler that keyed allowlist matching by `(path, line, class, digest)` would diverge from the gate exactly on repeated lines; R04/R11/R12 fixtures SHOULD include a repeated-identical-line arm to pin gate-compatible fan-out (or flag it as a separate finding) rather than leave it implicit.
- Current data: fan-out = 0 at HEAD and entering revision, so present partitions are not inflated by it; the risk applies to the receipt's `measured_revision` only if that revision's blobs differ (r21 measured revision not inspected by this seat).

### Partition interactions
- Forbidden precedence (L241): a row whose path is in `must_redact_paths` is reported `allowlist_forbidden` and **never** added to `allowed_keys`, so its hits stay unallowlisted; `finding_id` precedence forbidden > findings > stale > clean (L280–287), exit 1 on forbidden. Note says must-redact paths carry no rows (policy not checked by this seat).
- Non-author exclusion is applied independently of the allowlist (L262–266): a hit can be both non-author and allowlisted, so `allowlisted_hits` and `non_author` partitions can overlap; they are not disjoint subtractions of `hits`.
- Stale rows (L251–258) carry `line: None` — row-level, not hit-level; they only warn (exit 0).
- Allowlist path is not normalized; a row like `./x` or with a replacement char simply never matches (stale), not rejected. Hit paths are decoded with `errors="replace"`, so non-UTF-8 tracked paths could collide on the decoded string. [INFERENCE] low relevance for current 29 ASCII-like paths.

### Policy-excluded denominator
- [INFERENCE] If the r21 receipt's `--policy` was `.ufo/waves/round-18/frozen/c1-policy.json`, the 4 allowlist rows there are the allowlisted subset of that file's hits; the contract's "5 policy source hits" would then imply ≥1 unallowlisted or multi-class hit there. Not verified: the r21 receipt, its policy argv, and class regexes were not opened/run by this seat.
- Row counts per path are not hit counts; scanner/policy-excluded denominators must be computed from hit identities, never `rows`.

### Other
- `line_sha256` is an unsalted SHA-256 of a whole line: it identifies, it does not conceal; short/predictable lines are confirmable by guessing. It is not secrecy or authentication evidence.
- `rule` b rows' reason cites disagreement recorded in `out-of-metric-triage.md`; that file was not opened (not needed for schema semantics).

## Confidence
- Schema, counts, gate keying/precedence, blob identity: high (direct reads + measured counts).
- Fan-out = 0 now: high for digest presence at HEAD/77a5bbe8; liveness per class unmeasured.
- r21 policy-path linkage: unresolved.

## Remaining unknowns
- r21 receipt `measured_revision` and whether the allowlist/policy bytes there equal the entering revision's (R15/R16 territory).
- Which policy path r21 used; per-class liveness (stale count) of the 86 rows at r21 measured revision.
- Whether L1 wants repeated-line fan-out mirrored (gate-compatible) or surfaced as a distinct finding in the reconciler.

## Commands run
- `jq` field/type/uniqueness counts on the allowlist; `git -C <lane> rev-parse/log/status/hash-object/merge-base` (read-only); one `python3` stdin script using `git cat-file blob` to count per-row digest multiplicity at HEAD and `77a5bbe8` (output: counts only). No installs.
