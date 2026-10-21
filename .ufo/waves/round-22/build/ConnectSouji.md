# ConnectSouji — round22 connector: reconciliation boundary vs souji cleanup authority and evidence preservation

Seat: `MoriR22.ConnectSouji` (connector, leaf, detection/report only).
Scope: does the proposed `tools/mori-retention-reconcile.py check` boundary
(`.ufo/waves/round-22/contract.md:7-15`) stay outside souji's cleanup authority, and does it
preserve evidence? Axes touched: calibration (C1, the declared claim axis) and adjacency.
Coverage, operability, depth and freshness are not touched by the move below.

## Verdict

The boundary does not overlap souji's authority. The reconciler is read-only and blob-based,
and has no actuation (`contract.md:15`). Souji's "receipt" is a removal-safety verdict, while
mori's `mori-r21-command-receipt-v1` is a command-output wrapper; they share only the word.

There is one load-bearing contradiction, and it sits on the evidence-preservation seam. Under
the contract's own exact-policy-path rule (`contract.md:13`), the retained r21 receipt
reconciles to `policy_excluded=4` and `scanner_total=91`. It does not reconcile to the
"policy-excluded5 / scanner90" declared at `LOG.md:1447` (and in the open-debt line of the
assignment). The 90 is `hits − non_author` (95 − 5), the existing gate's `metric_before`
(`tools/mori-retention-gate.py:132`). That is exactly the count-subtraction coincidence the
round's root lesson forbids (`contract.md:23`). The four hits missing from the "policy"
exclusion live in a byte-identical preserved evidence mirror, and the tempting way to make
the numbers agree is to remove that mirror, which mori has no authority to do. Messages sent
to `MoriR22` (L1) and `MoriR22.OracleReconcile` (expected-value owner) only; no other writes.

## Evidence (read-only `git -C <abs>` plumbing and in-memory JSON counts; no matched text printed)

| Fact | Command / source | Result |
|---|---|---|
| Mori is jj-colocated | `test -d .jj`; `for-each-ref` grouped | colocated; 193 `refs/jj/keep/*`, 11 `refs/remotes/origin/*` |
| Retained receipt shape | `.ufo/waves/round-21/evidence/final/retention-floor.json` keys | `argv,cwd,elapsed_seconds,exit_code,measured_revision,schema,started_utc,stderr,stdout`; `measured_revision=9fb1f911…`, `exit_code=1`, stdout `finding_id=RETENTION_FINDINGS` |
| Receipt counts | stdout JSON lengths | hits 95, allowlisted 86, unallowlisted 4, non_author 5, forbidden 0, warnings 0, metric 4 |
| Hits at supplied policy path `.ufo/waves/round-18/frozen/c1-policy.json` | partition of receipt hits by exact path | **4** (lines 8,11,12,14; classes R2,R5,R6,R8), all allowlisted |
| Independent recount | re-applied the policy's R1–R9 regexes to blob `9fb1f911:<policy>` in memory (gate not imported) | **4** |
| Byte-identical mirror | `rev-parse 9fb1f911:.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json` | blob `8bf285bd…` = policy blob; mode 100644; added `71abd41` (mori-shokunin, 2026-10-21); holds 4 more hits |
| Non-author partition | fnmatch of the policy's `non_author_paths_glob` | 5 hits in `corpus/lessons/round-1{7,8}-verifier-spotcheck.md` |
| Candidate denominators | arithmetic over the identity sets above | exact path: 95−4=**91**; non-author: 95−5=90; any `*/c1-policy.json` basename: 95−8=87 |
| Scanner unallowlisted | unallowlisted hits not at policy path | 4 (all under `.ufo/waves/`), so "four unallowlisted" survives |
| Input-tree equality | `rev-parse <rev>:<path>` at e9f340ce, 9fb1f911, 77a5bbe8 | policy `8bf285bd`, allowlist `f8be55b1`: identical at all three; receipt exists at 77a5bbe8 only (`5c81c3f9`) |
| Ancestry / durability | `merge-base --is-ancestor`; `for-each-ref --contains` over heads/tags/remotes | e9f340ce ⊂ 9fb1f911 ⊂ 77a5bbe8 ⊂ HEAD 306e06ec; each reachable from 3 durable refs |
| Souji pattern overlap | `git grep -F` of R-class tokens over souji `tools/souji-proc-census.sh`, `tools/souji-census.sh` at HEAD | 0 files for all 8 tokens; 0 souji census files name `mori-shokunin/.ufo/waves/round-2*` |

[UNKNOWN] The operator's r21 independent closure census (cited as motivation at `LOG.md:1451`)
was not read, so its exclusion rule is not known. If it excluded something other than the
exact policy path, its 90 does not describe this contract's `scanner_total`.

## Overlap / non-overlap

**Shared method, separate authority (convergent; do not import souji code):**
- Reading committed blobs instead of the worktree. Souji's `souji-rev-pin` binds "owned regular file/directory byte set matches committed raw blobs" (`souji-shokunin/SKILL.md:207`), and its evidence cache says "Preserve the original declared revision: no fallback to a file-level revision or current HEAD" (`SKILL.md:276-277`). These match the contract's "Read receipt/policy/allowlist via Git blobs" and its rule that a policy or allowlist byte mismatch is unevaluable (`contract.md:10`).
- Symlink refusal: souji's `symlink-present` (`SKILL.md:30-31,36`) and rev-pin's symlink refusal match R21.
- Durable revision: souji requires reachability from `refs/heads|tags|remotes`, never `refs/jj` (`SKILL.md:126-132`; `PROVINCE.md:116-124`). The contract requires only a full commit that is an ancestor (`contract.md:10`). All of today's inputs are durable (table above), so nothing is harmed now. This is a residual, not a new requirement (see Risks).

**Non-overlap (boundary holds):**
- Removal, quarantine and receipts belong to souji, under operator approval (`souji-shokunin/PROVINCE.md:7-18`; `SKILL.md:33-40,55-61`). The reconciler forbids actuation, clearance, history rewrite, lifecycle authorization and pinning (`contract.md:15`). Mori's tip redaction covers its own lane-authored copies only (`mori-shokunin/PROVINCE.md:125-131`), which the round leaves unchanged (`contract.md:13`, "Existing retention implementation/allowlist/policy/history unchanged").
- A receipt in each lane means something different. A souji `pushed` receipt means removal-safety and recoverability (`SKILL.md:35,49`; mori `PROVINCE.md:183-190`). `RETENTION_RECONCILED` means accounting agreement and is neither privacy clearance nor removal eligibility for any hit-bearing file.
- Pattern classes do not overlap. Mori's R1–R9 private-context classes do not appear in souji's census or process-census tools (0/8). Souji's r21 redaction patterns are credential-shaped and its output-privacy guarantee is unproved (`souji-shokunin/PROVINCE.md:160-172`). Exposure stays with Kagi and the operator in both lanes.
- Live round outputs: souji refuses current-round drafts and uncommitted reports (`PROVINCE.md:42`), so round-22 build artifacts are fenced from cleanup without any mori action.

**Seam (where cleanup could silently move the denominator):**
- The NoHarmRun mirror is a byte-identical duplicate. A duplicate receipt class would be a taxonomy change and is an operator decision (`souji-shokunin/PROVINCE.md:69-70`). At most the mirror could get a `pushed` receipt for recoverable removal. Removing it would change the raw population (95→91) and destroy round-20 falsification evidence, repeating the aggregator-r10 evidence-loss pattern (`mori-shokunin/PROVINCE.md:162-172`).
- Blob-based reading protects a fixed `--rev` from later removals at the tip. If souji ever removes the r21 receipt at the tip, `check --rev <new tip>` must exit 2 with a setup error. That exit 2 is not evidence that the receipt was never written (FR3, `PROVINCE.md:44`).

## Proposed move (one, bounded; for L1 to judge)

Bind the real-receipt expectations to identities, not to the declared 5/90. In the committed
oracle for R02/R24 (the real retained receipt), freeze `raw_total=95`, `policy_excluded=4`,
`scanner_total=91`, `non_author=5`, `raw_unallowlisted=4`, `scanner_unallowlisted=4`,
`privacy_clearance=false`. Freeze the four excluded identities as digest-only (path, line,
class, line_sha256). Then append one erratum to `LOG.md`; do not edit the r22 declaration in
place. The erratum should say that "policy-excluded5 / scanner90" was `non_author`
subtraction, and that the four mirror hits remain in the scanner population and are never
closed by removal. R03's synthetic 5/1/4 fixture is unaffected.

Affected axes:
- **Calibration improves.** The capability's first real output would otherwise either "mismatch" the declared denominator or be bent to fit it. With identity-bound expectations it demonstrates the root lesson instead of violating it.
- **Adjacency improves.** It names the duplicate-mirror seam, so the denominator gap cannot be resolved by a cleanup that neither lane is authorized to run.
- **No harm.** Coverage, operability, depth and freshness are unchanged. No evidence bytes, retention gate, policy, allowlist or history change. The four unallowlisted hits stay red. No clearance, pin or disposition is created.

## Falsifiable no-axis-harm check (L1 runs after integration; not run here)

At integrated commit `I`, in a lane-local clone:

```sh
python3 tools/mori-retention-reconcile.py check --repo <clone> --rev 77a5bbe8a0b41dfbfd2546d024d36e294b814bd0 \
  --receipt .ufo/waves/round-21/evidence/final/retention-floor.json \
  --policy .ufo/waves/round-18/frozen/c1-policy.json \
  --allowlist corpus/evidence/retention-allowlist.json
git -C <lane> diff --name-status --diff-filter=DRM 77a5bbe8a0b41dfbfd2546d024d36e294b814bd0 <I> -- \
  .ufo/waves/round-18 .ufo/waves/round-20 .ufo/waves/round-21 corpus/evidence/retention-allowlist.json tools/mori-retention-gate.py
```

The check passes only if all of the following hold:
- The first command exits 0 with `RETENTION_RECONCILED`.
- It reports `raw_total=95`, `policy_excluded=4`, `scanner_total=91`, `raw_unallowlisted=4`, `scanner_unallowlisted=4` and `privacy_clearance=false`.
- Its excluded identities are exactly the four at the supplied policy path.
- The diff prints nothing.

It is falsified by any of these:
- `policy_excluded=5` or `scanner_total=90`, which means non-author conflation.
- `8` or `87`, which means a broad basename or regex exclusion.
- Any nonzero exit.
- Any `privacy_clearance` other than `false`.
- Any deleted, renamed or modified retained input, the NoHarmRun mirror included.

An optional extra arm: delete the worktree copies of the three inputs in the clone and rerun.
Byte-identical stdout proves the read-set is blobs only.

## Risks

- **Contradiction with the declaration.** `LOG.md:1447` and the assignment's open-debt line state 5/90. If L1 keeps 5/90, the tool must either violate `contract.md:13` (exact path only) or report a mismatch on the real receipt. That decision is L1's; I have not resolved it.
- **Entering-receipt binding ambiguity.** In `retention-floor-entering.json` the wrapper's `measured_revision` is `9fb1f911`, but its argv `--rev` and stdout `commit` are `e9f340ce`. e9f340ce is an ancestor of 9fb1f911, 8 commits apart. "Receipt target measured_revision" (`contract.md:10`) could mean either the wrapper field or the scanned commit. A reconciler should require wrapper `measured_revision` = argv `--rev` (resolved) = stdout `commit`, or state which one is the target. Otherwise this receipt is recomputed at the wrong tree, or accepted with an unbound commit.
- **Keep-only revisions.** With 193 keep refs, a `--rev` or `measured_revision` held only by `refs/jj/keep/*` would pass "full commit + ancestor" and could later be garbage-collected, turning a reproducible result into exit 2. Souji's durable-root rule is the precedent. Adopting it is a contract change for L1 or the operator, not something this seat adds.
- Citing souji's methods must not be restated as mori policy, and nothing here is permission to run a souji tool on mori evidence.

## Tooling / bounds

- No installs or updates. `skill://godspeed` did not resolve (`glob **/godspeed/SKILL.md` under `/home/vgpnk/.omp` → 0), so I followed the inline godspeed steps from the assignment.
- No tests, builds, gates, census or live probes. No sibling, production or VCS writes. Only this file was written.
- Two peer messages, to exact ids only: `agent://MoriR22` and `agent://MoriR22.OracleReconcile`.
