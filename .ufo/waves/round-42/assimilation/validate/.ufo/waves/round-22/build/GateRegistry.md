# GateRegistry — round22 scout report (MoriR22.GateRegistry)

Scope: registry conventions in `SKILL.md` and the exact row for the new
agreement gate `tools/mori-retention-reconcile.py`. Read-only; no tool, test,
selftest or gate was run. Lane HEAD observed `306e06ecd02e0ea8e544fbd30d1ff7e7359c581e`
(entering branch per contract `77a5bbe8…`); `tools/mori-retention-reconcile.py`
is absent at HEAD (expected before integration). No installs.

## Observed conventions (facts)

- Schema owner is fleet `PROTOCOL.md` §Gate standard (lines 375-423): row fields
  are name, `gate|probe`, entry command, verdict map (code → `clean|failed|could-not-evaluate`),
  self-test command and spelling, pinned-value path, write scope, owner. Registry
  home for a child lane is its own `SKILL.md` (`PROTOCOL.md:398-406`). Closure
  grades no gate conformant until its row exists there (`PROTOCOL.md:418-421`).
- `SKILL.md` renders those as an 8-column table:
  `| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |`
  (`SKILL.md:162-163`, repeated at `SKILL.md:518-519`).
- Two placement idioms exist: the main `## Gates` table (r10–r19 rows,
  `SKILL.md:164-182`) and per-round sections with their own header copy
  (`## Round21 retained-loss observation and policy-test registry`,
  `SKILL.md:516-532`). Newest convention is the per-round section.
- Name idiom: `rNN <noun> (Cn)` for claim-bound gates, e.g. `r18 retention (C1)`
  (`SKILL.md:177`), `r19 content review (C1)` (`SKILL.md:181`).
- Self-test spelling for Git-creating lane tools: `TMPDIR=$PWD/.scratch python3 tools/<tool>.py --selftest`
  (r18 retention, r19 content review, r21 evidence-loss); tally is "measured at L1
  integration, not predicted" (r15/r16/r17 wording).
- Write-scope idiom for Git-reading gates: "read-only over the measured repo
  (git ls-tree/cat-file/rev-list/diff-tree); selftest creates and commits only to
  throwaway git sandboxes under the caller's `$TMPDIR` (GIT_CONFIG_GLOBAL=/dev/null);
  JSON stdout, never matched text" (`SKILL.md:177-180`).
- Supersession precedent: r19's freeze-receipt paragraph explicitly *supersedes*
  the r18 C2 invocation (`SKILL.md:184-194`). The new row must say the opposite
  about r18 C1: it supersedes nothing.
- PROTOCOL "Two evidences" (`PROTOCOL.md:390-397`): selftest green is capability
  only; a verdict names its measured revision; a frozen baseline `expected.json`
  must pin every snapshot input digest, else `snapshot_tampered` / `unpinned (legacy)`.

## Existing retention row — must stay active

`r18 retention (C1)` at `SKILL.md:177` stays byte-unchanged: same entry
(`tools/mori-retention-gate.py scan … --policy .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json`),
0/1/2 map, frozen-run snapshot `.ufo/waves/round-18/gate-snapshots/retention/`
(file `retention.json` present), pins under `.ufo/waves/round-18/frozen/`. The
contract forbids changing the existing retention implementation/allowlist/policy/history.
`git ls-tree` shows that the policy blob `8bf285bd…` and the allowlist blob `f8be55b1…` are the same at
`9fb1f911`, `77a5bbe8` and HEAD. The new gate is additive and secondary: it checks a
receipt, it is not a retention verdict.

## Proposed row (draft for L1; placement: new section after `SKILL.md:532`)

Heading: `## Round22 retention reconciliation registry` with the 8-column header copy.

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| r22 retention reconciliation (C1) | gate (receipt-accounting agreement, not privacy clearance) | `python3 tools/mori-retention-reconcile.py check --repo <repo> --rev <INPUT_REV> --receipt .ufo/waves/round-21/evidence/final/retention-floor.json --policy .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json` (paths repo-relative, read as Git blobs at the once-resolved `<INPUT_REV>`; receipt `mori-r21-command-receipt-v1` `measured_revision` must be a full commit and an ancestor of `<INPUT_REV>`; policy/allowlist bytes at both revisions must be equal) | 0 clean = `RETENTION_RECONCILED`: exact hit-multiset and partition agreement only. Exit 0 can coexist with `retention_state=red`, and `privacy_clearance=false` is always printed · 1 failed = `RETENTION_RECONCILIATION_MISMATCH`: a valid receipt disagrees with the independent recomputation (dropped/injected hit, altered digest/line/class, metric lie) · 2 could-not-evaluate = `RETENTION_RECONCILIATION_SETUP`: malformed/unreadable input, bad type/schema/path/revision, non-ancestor target, policy/allowlist byte mismatch, duplicate receipt hit, symlink input, unsupported policy. Only a sanitized error code is printed | `TMPDIR=$PWD/.scratch python3 tools/mori-retention-reconcile.py --selftest`: actual isolated CLI subprocess arms over synthetic Git fixtures, asserting the exit code and `finding_id`. L1 measures the tally at integration; it is not predicted here | `.ufo/waves/round-22/frozen/requirements.json` (R01–R24, `contract_sha256` `1658c390…`); committed expected values and fixture generator (path assigned by L1, must be committed before implementation integration, with digests for every input); retained real input `.ufo/waves/round-21/evidence/final/retention-floor.json` (sha256 `4001e2d9…`) | read-only over the measured repo through `git -C` plumbing only, and no code is executed from blobs; JSON stdout only, never matched text; the selftest commits only to throwaway Git sandboxes under `$TMPDIR` (= `<repo>/.scratch`, GIT_CONFIG_GLOBAL=/dev/null) | mori |

Companion prose (one paragraph, required by the precedents): the `r18 retention (C1)`
row remains the active retention gate and is not superseded. Exit 0 here is
accounting agreement, never clean retention or privacy clearance. Raw denominator
is authoritative; the scanner-compatible denominator removes only hits whose path
equals the supplied `--policy` path. It does not authorize a pin, actuation or
lifecycle step, and it does not change r21 RED11/12 or the blocked baseline acceptance.

Frozen-run expectation (Two evidences) for the retained receipt. These values come from the
receipt's own JSON, filtered with `jq`; none of them was independently recomputed:
`raw_total=95`, allowlisted 86, `raw_unallowlisted=4`, `non_author=5`,
`forbidden_allowlist=0`, receipt `exit_code=1`, `finding_id=RETENTION_FINDINGS`, `metric=4`,
`policy_sha256=db06e981…`. That digest matches `sha256sum` of the committed policy, and the allowlist sha256 is `f46c78ec…`.
Expected reconciliation: exit 0, `retention_state=red`, `privacy_clearance=false`.
The 95 hit identities `(path,line,class,line_sha256)` are all distinct, so R19 does not trigger on the retained receipt.

## Load-bearing discrepancies (route to L1)

1. **Policy-excluded count is 4, not 5.** In the retained receipt, exactly 4 hits have
   path `.ufo/waves/round-18/frozen/c1-policy.json`, and all 4 are allowlisted. Under the
   contract's exact-path rule that gives `policy_excluded=4` and `scanner_total=91`, not the
   debt's "raw95 incl 5 policy / scanner90". A further 4 hits sit at
   `.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json`.
   That is a copy, not the supplied path, so they must stay counted.
   `95 − 90 = 5` equals `non_author=5`: the paths match `non_author_paths_glob`, with
   3 hits in `corpus/lessons/round-17-verifier-spotcheck.md` and 2 in
   `round-18-verifier-spotcheck.md`. [INFERENCE] The "5 policy" debt figure may be
   conflating the non-author partition with the policy source. Do not pin 5/90 in expected
   values until the reconciler's recomputation has actually measured them.
2. **The entering receipt is internally inconsistent.** In
   `.ufo/waves/round-21/evidence/final/retention-floor-entering.json` (sha256 `87899139…`),
   the wrapper `measured_revision` is `9fb1f911…`, but argv `--rev` and stdout `commit`
   are both `e9f340ce…`, a different commit with a different tree (ancestor of `77a5bbe8`).
   Counts are the same as the final receipt (95/86/4/5/0). The row and the expected values should
   name the final receipt as the input. The reconciler should fail closed with exit 2 when
   `measured_revision`, argv `--rev` and stdout `commit` disagree. This is a required-field
   consistency check, and it is not among the named requirements R01–R24.
3. **Receipt argv uses absolute lane paths** for `--repo`, `--policy` and `--allowlist`, while the new
   CLI takes repo-relative inputs. The R20 unsafe-path rule must apply to the reconciler's own
   arguments, not to the bound argv contents. Whether argv is compared after normalizing
   `<repo>/<REPO_REL>` or only carried as provenance (R24) is an implementation decision that L1 should fix.

## Unresolved

- Pinned expected-values and fixture-generator path: not yet committed (only
  `round-22/frozen/requirements.json` at `df880b4`).
- Whether L1 prefers the main `## Gates` table or the per-round section. Both are
  schema-conformant; the per-round section follows the newest (r21) idiom.
- The source of the r21 "scanner90" figure was not located inside the bounded reads.

Measured nothing beyond the read-only `git rev-parse`/`ls-tree`/`merge-base`/`log`,
`sha256sum` and `jq` metadata projections listed above (no matched text read or emitted).
