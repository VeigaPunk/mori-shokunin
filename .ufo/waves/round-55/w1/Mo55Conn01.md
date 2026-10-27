# Mo55Conn01 — C2 sibling-overlap scan

## Evidence
- Frozen contract `mori-shokunin/.ufo/waves/round-55/contract.md:29-41` defines C2 as depth coverage of block/inode runway, XFS, btrfs reserve/sysfs, tmpfs limits, and ENOSPC/EDQUOT boundary; it explicitly calls C2 separable from C1.
- `mori-shokunin/corpus/knowledge/disk-runway-enospc-r55.md:7-46` is the specific 23-claim C2 knowledge entry. Its boundary at lines 46, 54 excludes diagnosing quota failures and distinguishes EDQUOT; the host snapshot is separately labeled point-in-time at lines 48-58.
- Adjacent corpus search found chousa round-52 through round-57 and kaidoku rounds 36-42 / kake rounds 58-60 repeat a distinct fleet-operational incident: large temporary clone/work trees under `/tmp` exhaust the temporary filesystem and cascade seat failures. For example, `chousa-shokunin/.ufo/prompts/chousa-round-55.md:606-632` describes stale multi-GB `/tmp` trees and operational disk guard controls. This is not a duplicate of C2's filesystem accounting claims: it concerns orchestration scratch lifecycle and capacity guardrails, not kernel statfs semantics, XFS/btrfs/tmpfs behavior, or per-filesystem availability diagnosis.
- `disk-runway-enospc-r55.md:50` explicitly identifies `/tmp` as XFS and reports ample snapshot runway; C2's captured host state is observation, not reproduction (lines 54-58).
- Read-only disk guard status: `/tmp` 125.1G free (3% used), `/var/tmp` 589.9G free, `/fast/scratch/hyaku` 594.6G free. No ENOSPC condition observed.

## Ownership collision
No direct sibling ownership collision found for C2's technical claim ground in the inspected adjacent corpora. The same broad ENOSPC vocabulary appears in fleet operational lessons, but their ownership is the dispatcher/disk-guard scratch-lifecycle failure domain. Treating those repeated incidents as competing C2 claims would conflate runtime substrate (filesystem behavior) with orchestration contract (where temporary work is placed and reclaimed). Explicit contradiction: C2's scope says detection/reporting only and prohibits writes or ENOSPC reproduction; the fleet lessons discuss operational mitigation (guard/sweep/purge). They can coexist only as separate domains, not as a combined recommendation to modify the host from this C2 entry.

## One bounded proposal
Keep C2 ownership scoped to source-backed filesystem runway interpretation; avoid absorbing repeated fleet scratch-cleanup policy. Add no change to frozen C2 claims or predicates. If the round needs a cross-lane synthesis, link the fleet disk-guard policy only as an external operational dependency, without duplicating its instructions in the C2 knowledge entry. This preserves depth while avoiding adjacency/ownership duplication and does not harm freshness, coverage, or calibration.

## Risks and verification
Risk: the search was limited to accessible local corpus/search results and does not establish absence of every possible neighboring entry. The adjacent evidence also contains repeated excerpts of the same policy, not independent implementations. No production files changed. Verification performed: reviewed frozen contract and C2 entry; searched local corpus for ENOSPC/runway overlap; checked disk-guard status. No tests/builds applicable.

## Findings
- INFO — Similar ENOSPC topic exists in fleet operational lessons, but ownership is scratch lifecycle/dispatcher behavior, not C2 filesystem semantics. Evidence: `chousa-shokunin/.ufo/prompts/chousa-round-55.md:606-632`.
- INFO — C2's explicit non-reproduction/detection boundary avoids conflict with operational mitigation material. Evidence: `mori-shokunin/corpus/knowledge/disk-runway-enospc-r55.md:46,54-58`.
