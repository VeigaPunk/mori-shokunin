# Attack: round-18 token redactions in ReviewC1Contract.md and ReviewSchemaDrift.md

Seat: MoriR18Recovery.AttackTokReviewC1Schema-2 (wave 2, falsify). Scope: the two named
round-17 build files only, diffed entering tip d005cdd → attacked tip e2bfbd6; L1 decisions
attacked, not judged. Advice only; MoriR18Recovery is the sole integration owner.
No private text is quoted below; citations are path:line, class id, counts, and SHA-256 prefixes.

## Method (all read-only; exit 0 unless noted)

- `git diff-tree -p --no-color d005cdd e2bfbd6 -- <both paths>`: exactly two hunks, one
  single-line replacement per file; 22 → 22 lines each; blob 0df55cc→1d8cc52 and
  9fe5f14→df1d5dc. `git log --oneline d005cdd..e2bfbd6 -- <both paths>`: only b8f5c6c
  touched them (matches the triage register's token-redaction commit).
- Frozen cross-check: `.ufo/waves/round-18/frozen/c1-population.json` (119 hit rows at
  d005cdd) flags exactly these lines in my two files: ReviewC1Contract.md:13 R1+R2 (line
  sha256 275cba91ef8c…), ReviewSchemaDrift.md:9 R2 (13fd6b8fb4b3…).
- Residue scan: applied all nine frozen class regexes from `frozen/c1-policy.json` to every
  line of both files at d005cdd, b8f5c6c, daceeec, e2bfbd6, plus substring search for
  redacted-token fragments (uuid head, `…Z_` timestamp fragment, store-root segments).
- JSON validity: `python3 -m json.tool` N/A for .md bodies; the embedded JSON literal in
  ReviewSchemaDrift.md:9 is byte-identical across the diff and parses. Frozen inputs read
  and validated: c1-policy.json, c1-population.json, c2-register.json, c3-ledger-format.json
  (all json.tool clean). Files read via `git show <rev>:<path>` only; no `git status`,
  no index contact, no VCS mutation, nothing written outside this report.

## Per-line judgments

### .ufo/waves/round-17/build/ReviewC1Contract.md — line 13 (the only changed line)

1. Token removal: PASS. Both frozen classes on the line (R1 session identity, R2 store path)
   are gone at b8f5c6c and stay gone at e2bfbd6; uuid and timestamp fragments absent from
   the whole file; exactly one redaction placeholder remains. No other private token class
   (R3–R9) was present on the line.
2. Missed values on line/neighbours (12–16): none harmful. Retained items are metadata
   field names (allowlistable under policy rule b), aggregate class counts accepted by the
   r17 closure's projection, and generic status/error-class observations on line 15 (triage
   family classifies this category as an allowlisted contract projection). No session-record
   value, routing value, or per-seat retry value remains.
3. Technical meaning: preserved. The line differs from its d005cdd version only by the
   path→placeholder substitution; every count and clause is byte-identical.

### .ufo/waves/round-17/build/ReviewSchemaDrift.md — line 9 (the only changed line)

1. Token removal: PASS for the private token. The R2 store path is gone from b8f5c6c on;
   no store-root segment survives anywhere in the file.
2. Missed values on line/neighbours: two retained session-header values on the changed
   line — a line-ordinal value and a format-version value inside the quoted header projection
   (the record-type designation is a name, allowlistable). These are values, not names, so
   the L1's name-only adjudication clause does not cover them (F2 below). Identifiability
   is negligible (store-format version + line ordinal of the then-current transcript), and
   the sentence self-declares the projection as line/type/version only.
3. Technical meaning: BROKEN (F1 below). The substitution was narrower than the pre-existing
   placeholder: the d005cdd line's evidence location contained a store-root path followed
   by an already-redacted transcript identifier; the edit replaced only the leading portion
   and left the suffix. The resulting evidence-location span has a withheld-path placeholder
   followed by a dangling word and unmatched closing angle bracket before the line-reference
   suffix. The reference no longer attaches to a coherent location and the pointer no longer
   parses.

## Findings by severity

- **F1 (Low, defect) — ReviewSchemaDrift.md:9, redaction debris breaks the line.**
  Evidence: diff hunk above; raw blob comparison at b8f5c6c/e2bfbd6. The token edit consumed
  only part of a pre-existing placeholder and left `transcript>` adjacent to the redaction
  token, so the evidence-location span is garbled. No privacy harm (debris is non-private);
  the harm is documentability, and it evidences the process risk that the same narrow
  string-substitution across the 22-file token-redaction family (commit b8f5c6c) can leave
  similar debris or partial tokens elsewhere. Recommendation: a residual-artifact scan of
  every token-redacted file for unbalanced brackets/backticks adjacent to placeholder tokens
  (or an automated placeholder-integrity check), and a one-word cleanup of this line.
- **F2 (Info) — ReviewSchemaDrift.md:9 retains two session-record values not covered by the
  name-only rule.** The line ordinal and header `version` value survived the redaction; the
  triage register's token-redaction family (session ids, store paths, tool-log numbers,
  document paths, config line refs) never dispositioned header values. Harm negligible;
  flagging so the disposition is explicit rather than accidental, and because it shows the
  pass distinguished name vs value only via the frozen regex floor, not a value scan.
- **F3 (Info, no action) — ReviewC1Contract.md:15 class tokens and aggregates.** Consistent
  with the r17 closure's accepted projection and the triage decision rule; recorded to show
  the neighbour lines were checked, not skipped.

Positive verification: both population-flagged lines are fully redacted; zero frozen-class
hits remain in either file at daceeec and e2bfbd6; no redacted-token fragments survive;
line counts and all other lines are byte-preserved; only b8f5c6c touched the files; the
embedded JSON literal is intact; draft-verdict wording ("routed 0 … pending allowlist rows")
is honest about the after-state.

## Judgment: keeping name-only mentions allowlistable

Sound, with the guards already frozen. `frozen/c1-policy.json` `adjudication_rule`
allowlists a hit only when the line "carries no value copied from a private source", with
three named carve-outs ((a) surface-naming instruction/contract statements, (b) field/key
names in tool code, contracts, fixtures, (c) non-author routed files); allowlist rows bind
path+class+line sha256, `allowlist_forbidden` bars rows for must_redact_paths, and stale
rows surface as warnings. That structure matches the privacy rule's name/value split and the
policy's own `known_limit` admission that regex classes are a recall floor. Residual risk,
confirmed by F2: value-shaped tokens (version numbers, status codes, provider/model values)
are not names and are excluded by the clause's wording, but nothing in the pass scans for
them once the floor is quiet; the final allowlist pass should re-read each row's line against
the no-value clause rather than trusting the class regexes. Note also the after-count is not
yet clean: the draft verdicts' 55 name-only hits at daceeec remain unallowlisted findings
until rows land, so "target 0 at the final measured commit" is still open, as the draft says.

## Residual risk and verification gaps

- I verified only the frozen regex floor plus targeted fragment search on the two named
  files at four revisions; beyond-floor private context in them was dispositioned by the L1's
  reading sweep, which I did not re-execute (out of my item's read-only command set).
- The 22-file token-redaction family was not diffed here (out of scope); F1's process risk
  generalizes to it only as [INFERENCE].
- No tool installs or upgrades were needed or performed. No pacman transaction, no live
  journal query, no /tmp writes, no subagent dispatch (leaf member).
