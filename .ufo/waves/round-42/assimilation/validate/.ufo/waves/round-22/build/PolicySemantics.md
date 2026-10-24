# PolicySemantics — frozen C1 policy: non-author / must-redact semantics

Seat: MoriR22.PolicySemantics (read-only scout). No tests, builds, scans, regex executions, installs or
measurements were run. Every count below is either read directly from source text or marked
`[INFERENCE]` (derived by hand). No regex string or matched text from the policy is reproduced here.

Sources read (worktree copies, read-only):
- `.ufo/waves/round-18/frozen/c1-policy.json` (whole file, 30 lines).
- `.ufo/waves/round-22/contract.md` (whole file).
- `corpus/lessons/round-17-verifier-spotcheck.md:335-400` (the policy's `must_redact_source` citation).
- `tools/mori-retention-gate.py` (whole file). It is the existing retention gate whose semantics the
  contract requires the reconciler to reproduce independently.

LSP note: no `lsp` device was used, so the symbol references below come from reading the file
directly. They are single-file definitions, not cross-file semantic proof.

## 1. Policy fields (observed)

| Field | Value shape | Observed semantics source |
|---|---|---|
| `schema` | `mori-retention-policy-v1` | gate `validate_policy` requires an exact string match (`:61`) |
| `classes` | 9 rows, ids R1–R9, each `{id, name, regex, why}` | gate compiles `regex` with Python `re`, no flags; rejects duplicate ids and invalid regex (`:70-81`) |
| `must_redact_paths` | 3 exact repo-relative paths under `.ufo/waves/round-17/build/` | gate turns them into a `set[str]` and matches by exact string equality (`:86`, `:130`, `:241`, `:268`) |
| `must_redact_source` | prose citation of the round-17 lesson, lines 339-346 and 390-397 | not read by the gate; provenance only |
| `non_author_paths_glob` | 2 patterns under `corpus/lessons/` | gate `_is_non_author` uses `fnmatch.fnmatch` (`:121-122`) |
| `adjudication_rule` | prose: allowlist rules (a), (b), (c); must-redact files get no allowlist and must scan to zero | the gate enforces only the rule letter and the must-redact prohibition (see section 4) |
| `metric` | prose: C1 = unallowlisted hits excluding non-author; routed = hits inside must-redact | gate `_scan_result` (`:260-268`) |
| `known_limit` | regex classes are a recall floor, not a privacy proof | not enforced; it is a claim boundary |

The R1–R9 class purposes, paraphrased from the `why` fields: session identity, session-store path,
numbered tool-output artifact, private document path, shell history, privileged config, operator config
reference, routing-table key names, and session-record field values outside the round-17 allowlist.

## 2. Non-author semantics (exact)

- Matching is `fnmatch.fnmatch(path, pattern)` against the hit's path. That path is the Git tree path
  decoded as UTF-8 with `errors="replace"` (`:202`). The gate passes `--full-tree` with `-z`, so paths are
  repo-root-relative and unquoted (`:189`).
- On POSIX, `fnmatch.fnmatch` applies `os.path.normcase`, which does nothing there, so matching is
  **case-sensitive**. `*` matches **any** characters, **including `/`**: the glob for round verifier
  spot-checks also matches deeper paths whose final component ends in the spot-check suffix
  (`[INFERENCE]` from the stdlib `fnmatch.translate` contract; no fixture exercises it). `?` and `[...]`
  are also special characters.
- Non-author hits are **kept** in `hits` and counted in `non_author`. They are excluded only from
  `unallowlisted_hits`, and therefore from `metric` and `routed` (`:260-268`).
- An allowlist row can still match a non-author hit, so `allowlisted_hits` is **not disjoint** from the
  non-author partition (`:261` computes allowlisted hits without the non-author filter). The exact
  identities are therefore `unallowlisted = raw − non_author − allowed`, with
  `non_author ∩ allowed` possibly non-empty. A reconciler that adds up partition counts will be wrong
  whenever that intersection exists.
- The population summary defines `metric_before = hits − non_author`, with no allowlist applied (`:125-133`).
- The `must_redact_source` lesson (`corpus/lessons/round-17-verifier-spotcheck.md`) itself matches the
  non-author glob, so its hits are retained-by-non-author and excluded from the metric. This is policy
  rule (c) in effect, not an allowlist row.

## 3. Must-redact semantics (exact)

- Membership is exact string equality on the decoded path, with no normalization, glob or prefix
  matching (`:241`, `:268`).
- **Allowlist prohibition:** any allowlist row whose `path` is a must-redact path becomes a
  `forbidden_allowlist` record (`line: null`). It is **not** added to the allowed keys, even if its
  `(path, class, line_sha256)` equals a real hit. That hit stays unallowlisted, so it counts toward
  `metric` and `routed` (`:239-249`). The gate selftest arm "allowlist-forbidden" asserts exit 1,
  `finding_id=allowlist_forbidden`, metric 1 and routed 1 (`:609-623`). That is a selftest assertion,
  not a result observed in this wave.
- A forbidden row forces exit 1 and `finding_id=allowlist_forbidden` **even when it matches no hit and
  the metric is 0** (`:280-288`). A forbidden allowlist can never produce a clean result (requirement R11).
- `routed` counts unallowlisted hits in must-redact paths (`:268`). This matches the policy's prose
  "hits inside must_redact_paths" only because the must-redact paths (under `.ufo/`) and the non-author
  globs (under `corpus/lessons/`) are disjoint in this frozen policy, and because must-redact hits cannot
  be allowlisted. If a future policy made those sets overlap, overlapping hits would silently leave both
  `metric` and `routed`, and the gate does not check for this.
- "Must scan to zero hits" has no dedicated finding id. It is enforced only indirectly: any must-redact
  hit raises `metric`, giving `RETENTION_FINDINGS` and exit 1.
- The population summary's `must_redact` field counts **all** raw hits in must-redact paths, including
  any non-author ones (`:130`). It is a different quantity from `routed`.

## 4. Allowlist semantics the reconciler must reproduce

- Accepted file shape: either a JSON list, or an object whose `rows` key holds the list. Any other
  object (for example one without `rows`) becomes `invalid_allowlist_shape` (`:316-320`, `:136-138`).
- Each row must have exactly the keys `{path, class, line_sha256, reason, rule}`. `class` must be a known
  policy id, `line_sha256` must be lowercase 64-hex, `reason` must be non-blank, and `rule` must be one of
  `a`, `b`, `c`. Duplicate `(path, class, line_sha256)` rows are a setup error (`:142-157`). The row's
  `path` gets no safety check beyond being a non-empty string.
- The allowlist match key is `(path, class, line_sha256)`, with **no line number** (`:235`, `:240`,
  `:261`). One row therefore allowlists **every** hit with the same digest in that file. Identical lines
  repeated in one file are all allowlisted together. The selftest comment says a row "binds one hit"
  (`:564-565`), which holds only for distinct line content.
- A row matching no hit (and not must-redact) becomes a `warnings` stale record. It yields
  `finding_id=allowlist_stale` only when the metric is 0 and no row is forbidden. The exit code stays 0.
- The gate checks the rule letter, not its meaning. Nothing ties rule (c) to non-author paths or rule
  (b) to tool, contract or fixture files. The adjudication judgment (whether a line carries no value
  copied from a private source) is human-only and not machine-checkable from the receipt.
- `finding_id` priority: `allowlist_forbidden`, then `RETENTION_FINDINGS` (metric > 0 or population
  mismatch), then `allowlist_stale`, then `RETENTION_CLEAN`. Exit 1 if metric > 0, any forbidden row, or
  a population mismatch; otherwise 0. Setup errors exit 2 (`:280-288`, `:750-756`).

## 5. Population and hit identity semantics (for independent recomputation)

- Tree walk: `ls-tree -r -z --full-tree <commit>`. The walk skips entries that are not blobs and skips
  mode `160000` (submodules). **Symlink entries (mode `120000`) are blobs and are scanned**, using the
  link-target text (`:199-203`). The contract's symlink rejection applies to the receipt, policy and
  allowlist *inputs*, not to population blobs.
- A blob containing any NUL byte yields no hits (`:90-91`).
- Lines come from `decode("utf-8", errors="replace").split("\n")`, numbered from 1. A trailing newline
  produces a final empty segment. A `\r` stays in the line and in the digest (`:92-94`).
- `line_sha256` hashes the **decoded and re-encoded** line, so invalid input bytes are hashed as
  U+FFFD (`EF BF BD`), not as the original bytes (`:101`).
- Each class is tested with `search` once per line, so a line gives at most one hit per class. A line
  matching k classes gives k hits that share one `(line, line_sha256)` pair (selftest "multi-class-line",
  `:585-596`). Hits are ordered by tree path, then line, then policy class order.
- The patterns are `str` patterns, so the word-boundary and whitespace classes use Unicode semantics.
- Duplicate-identity risk `[INFERENCE]`: two distinct non-UTF-8 tree paths can decode to the same
  replaced string and produce identical `(path, line, class, line_sha256)` tuples in one honest scan.
  The contract says to preserve duplicates as a multiset but reject duplicate receipt hits (R19). On such
  a tree those two rules conflict. Failing closed (exit 2 on non-UTF-8 tree paths) is the consistent
  choice. L1 should decide; this seat recorded it only.
- Receipt binding: the gate's `policy_sha256` hashes the policy bytes read from a filesystem path,
  usually a worktree file (`:311-313`), and the gate also reads the allowlist from the filesystem
  (`:317`). The contract requires the reconciler to read both from Git blobs and to demand byte equality
  between the input and measured revisions. If a receipt's `policy_sha256` differs from the blob at the
  measured revision, the gate ran against an uncommitted policy. Per the contract, that is unevaluable
  (exit 2), not a mismatch.

## 6. Policy-source self-hits (relevant to raw versus scanner denominators)

- The contract defines "policy-excluded" as hits whose path is exactly the supplied `--policy` path.
  The frozen policy path sits under `.ufo/waves/round-18/frozen/`. That is neither non-author nor
  must-redact, so any self-hits count toward `metric` unless allowlisted.
- `[INFERENCE]` A hand trace of each class pattern against each JSON-escaped line of
  `c1-policy.json` finds **4** self-matching lines, one hit each: line 8 (R2 row, class R2), line 11
  (R5 row, class R5), line 12 (R6 row, class R6) and line 14 (R8 row, class R8). The JSON doubling of
  backslashes stops the R1, R3, R4, R7 and R9 rows from matching their own patterns. None of the `why`,
  `scope`, `metric` or other prose lines match any class.
- **Open discrepancy:** the round-22 contract and the open debt state that the retained r21 raw count
  of 95 includes **5** policy-source hits (95 raw against 90 scanner). By my hand trace, this policy file
  contributes 4 at line-class granularity. Three explanations are possible: (a) my hand trace is wrong,
  (b) the r21 "policy source" covered more than this one path, or (c) the r21 measured tree held
  different policy bytes. Any of these blocks a count-only reconciliation. L1 should measure the
  policy-path hit identities at the r21 measured revision before freezing R03/R04-style expectations
  for the real receipt. Whether the r21 allowlist covers these self-hits was not inspected; the
  allowlist is outside this seat's bounds.

## 7. Must-redact source citation check (observed, worktree only)

- `round-17-verifier-spotcheck.md:339-346` (worktree) lists the three must-redact report paths with
  category-only descriptions of what each retains: other-session tool-output excerpts, a session
  identity, planned command text from a private document, history facts, privileged config, private
  model routing configuration, and non-allowlisted transcript and custom-record field values. Each
  category maps to one or more of R1–R9. The lesson deliberately cites locations without values.
- `:390-397` is routed defect 1: narrow or redact the retained Markdown and add a minimization lesson.
  Exposure assessment for pushed history belongs to the operator or kagi. Rotation, deleting another
  owner's copy, and history rewriting are not authorized.
- These line numbers were checked in the worktree file, not in the blob at the policy's `base` commit.
  Byte identity at `base` was not checked.

## 8. Confidence and remaining unknowns

- High confidence (direct source reading): sections 2–5, the gate behaviour, and the field shapes.
- Medium confidence: the `fnmatch` slash-crossing claim. It is standard-library behaviour, but no
  fixture in the repo exercises it.
- Unverified `[INFERENCE]`: the 4-hit self-match count and the non-UTF-8 duplicate-path collision.
- Unknown: the source of the fifth policy-source hit; whether the r21 allowlist rows cover any
  policy-file self-hits; and the citation's byte identity at `base`.
- Not a privacy clearance: these semantics define the frozen regex recall floor only. As the policy's
  `known_limit` states, private context without these tokens is out of scope for this metric.

Installs or updates: none.
