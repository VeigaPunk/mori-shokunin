source: S064 https://git-scm.com/docs/git-rev-parse OPTIONS --verify; tools/mori-retention-reconcile.py; .ufo/waves/round-22/denominator-correction.md; .ufo/waves/round-21/evidence/final/retention-floor.json
verified-at: 2026-10-21; exercised results and measured tool revision are recorded in the round22 report and SCORECARD
recheck: TMPDIR=$PWD/.scratch python3 tools/mori-retention-reconcile.py --selftest; python3 tools/mori-retention-reconcile.py check --repo "$PWD" --rev INPUT_COMMIT --receipt .ufo/waves/round-21/evidence/final/retention-floor.json --policy .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json

# Retention receipt reconciliation — accounting, not clearance

A retention count has two distinct questions: which identities were observed, and which policy membership excludes them from a metric. A scalar difference cannot identify the excluded population. L1 initially made exactly this mistake: interpreting 'policy-excluded' as excluding the policy source file. The original contract is retained; the pre-implementation correction and v2 oracle define the effective behavior. This is calibration of existing own-evidence ground, not new frontier coverage.

## Decision table

| Condition | Reconciler outcome | Meaning |
|---|---|---|
| Valid committed receipt agrees with exact independent recount | exit0 RETENTION_RECONCILED | Accounting agreement only; retention may remain red |
| Well-typed claimed hit list, partition, finding or exit disagrees | exit1 RETENTION_RECONCILIATION_MISMATCH | Named field disagreement; counts are independently recomputed |
| Invalid schema/types/JSON, duplicate hit, unsafe/nonregular input, unresolved/divergent revision, changed policy/allowlist bytes | exit2 RETENTION_RECONCILIATION_SETUP | Could not evaluate; sanitized error, never fake zero |
| Wrapper revision differs from argv --rev or inner commit | exit2 | Equal counts cannot fix contradictory provenance |
| Four unallowlisted inherited hits remain | retention_state=red, privacy_clearance=false | Neither agreement nor zero new hits clears privacy debt |

## Exact populations

A raw hit identity is `(path, line, class, line_sha256)`. Compare exact multisets, independent of order; a duplicate claimed identity is a setup error. Line hashes cover decoded UTF-8 replacement text without the newline, matching the retained gate. Every tracked blob is scanned, including stored symlink target bytes; a NUL-containing blob is skipped. Input files themselves must be regular committed blobs. Non-UTF8 tree paths are explicitly unevaluable rather than allowed to collapse into duplicate replacement-decoded identities.

`policy_excluded` names the hits matching the frozen policy's `non_author_paths_glob`, not the policy JSON path. `scanner_hits` is the raw list minus those identities. The supplied policy source and any policy copies are scanned normally. Allowlist membership uses `(path,class,line_sha256)` without line number, so one row can allow multiple identical lines in the same file. Non-author and allowlisted membership may overlap: do not subtract their scalar totals as if they were a general disjoint partition. Forbidden rows on must-redact paths cannot allow any hit; stale rows retain the original warning/finding precedence.

The r21 receipt's observed metadata has95raw/5non-author/90scanner/4unallowlisted. Its source-policy file has4allowlisted hits, and a nested byte-identical policy copy contains the4unallowlisted hits. Neither source-file subtraction (giving91) nor digest/basename exclusion is the operator's scanner population. These values are historical receipt metadata; actual round22 recount receipts carry their own measured revisions.

The output's `raw_unallowlisted` and `scanner_unallowlisted` intentionally
name the same existing policy-filtered metric, not two independent counts.
Likewise `policy_excluded` equals `non_author` by definition. The full
identity lists, not these aliases, establish membership. The no-clearance
field is always false even when the frozen-regex retention state is clean.

## Provenance limits

The reconciler resolves the input commit once, reads receipt/policy/allowlist from Git, and recounts the full commit named consistently by wrapper/command/inner result. The measured commit must be an ancestor of or equal to the input commit. Policy and allowlist bytes must match across both commits. Output binds loaded input digests, executing tool digest, resolved revisions and argv. Git replace refs, inherited Git redirection/trace variables and lazy fetching are disabled for reads.

S064 documents resolving an existing commit; it does not authenticate an actor or a historical execution. The old receipt lacks an allowlist digest and read its inputs from the working tree, so a present recount establishes reproducible accounting under these committed bytes, not proof of which allowlist was actually loaded then. A forged self-consistent receipt may also agree. Hashes are provenance, not secrecy, and no output grants privacy clearance, baseline acceptance, lifecycle settlement, cleanup, reap or dispatch permission. Four retention hits, original permission11/12red and both unknown wave dispositions remain open.
