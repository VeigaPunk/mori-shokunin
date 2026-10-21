# Round-18 privacy re-sweep — e2bfbd6

## Axes and scope

- **Privacy retention:** other-session/session-derived output, operator/runtime configuration, personal/account identifiers, and private-document paths.
- **Classification:** distinguish actual private values from class tokens used as instructions, contracts, or field names.
- **Provenance:** pin all observations to the committed tree at `e2bfbd6f8dccc51fc06455efc41f720301112dd4`; the lane HEAD observed during this review had advanced to `95c6158`. The sweep covered 77 tracked files under `.ufo/waves/round-18/` at the pinned revision, not the later working tree.

## Verdict

**Yes.** Wave-1 reports and L1-authored round-18 records retain private context outside the frozen C1 regex classes. Most consequential are session-derived corpus data and operator/host configuration details in three `build/Redact*` reports. This is a qualitative reading-sweep result; it does not change the frozen C1 count. Values are not reproduced here.

Qualitative classes below are local to this report and outside C1: **P1** session/other-seat-derived output or metadata; **P2** operator/runtime or privileged configuration values; **P3** host account identifier. Counts are affected lines (a line may be in more than one class), not counts of underlying source records. SHA-256 values identify the complete round-18 file blob at the pinned revision.

## Findings

| Lane-relative path:line | Class; count | Finding kind (no values quoted) | File SHA-256 |
|---|---:|---|---|
| `.ufo/waves/round-18/build/RedactOmpRetryConfig.md:55,142-154,169` | P1; 15 lines | Session-derived retry outcome, corpus/record aggregates, and per-session behavior remain in the round-18 report. | `c72fafd0ba865f597b171e283219de5a438679ff2a98fd457f9327972bdef029` |
| `.ufo/waves/round-18/build/RedactOmpRetryConfig.md:65-82,158-165` | P2; 26 lines | The report discloses operator-owned runtime configuration state and routing/candidate topology, alongside effective retry/default behavior. These are configuration values or derived configuration facts, notwithstanding the report's minimization claim at line 59. | `c72fafd0ba865f597b171e283219de5a438679ff2a98fd457f9327972bdef029` |
| `.ufo/waves/round-18/build/RedactSessionExitCorrelation.md:69-71,81-108,112-114,118-120,126` | P1; 38 lines | Session-corpus scope, snapshot timing, field/status cross-tabs, per-file counts, drift and tail-window results are retained. This is session-derived metadata even though message prose and the source path are withheld. | `fe50242f441ede59a536a7fdfc260a4f64db57d8e99378e905c8f031694d536b` |
| `.ufo/waves/round-18/build/RedactPacmanActorTrace.md:76-78,83,85,109-110` | P1; 7 lines | Session-store search results, shell-history inventory/status, and session-linked activity attribution remain. | `06fd86df883a90600bcb3d6a26961da110e924be72d16730a5dde996bc27ffc7` |
| `.ufo/waves/round-18/build/RedactPacmanActorTrace.md:79` | P2; 1 line | A value/state from privileged host configuration is retained. | `06fd86df883a90600bcb3d6a26961da110e924be72d16730a5dde996bc27ffc7` |
| `.ufo/waves/round-18/build/RedactPacmanActorTrace.md:84,86` | P3; 2 lines | A numeric host login/account identifier and linked privilege attribution are retained. **[INFERENCE]** The report does not establish the human identity behind that identifier. | `06fd86df883a90600bcb3d6a26961da110e924be72d16730a5dde996bc27ffc7` |
| `.ufo/waves/round-18/contract.md:5-6` | P1; 2 lines | Launch/dead timestamps tied to the prior failed lane attempt are retained. | `6986c9338b4c38f8b66831526d4427c04c589226adc43e0240ff34ce08fcf11b` |
| `.ufo/waves/round-18/draft-verdicts.md:23` | P1; 1 line | The L1 summary retains a same-wave seat-failure reason and retry/resume metadata. | `c83dc17160b108cec68526dcf817ff78ffabf8859c3f39b6ab11936101c22ff6` |
| `.ufo/waves/round-18/evidence/wave1-dead-seats.json:2-4` | P1; 3 lines | Other-seat failure/resume output and a session-tied timestamp are retained. | `0c7c2da40bfd69ff30a028b842d4683f313d3f0038e6aa29a615e64a8dc88f5f` |
| `.ufo/waves/round-18/evidence/wave1-dead-seats.json:2` | P2; 1 occurrence | A runtime model-assignment value is embedded in the failure record. **[INFERENCE]** The record alone does not prove that the assignment was copied from the operator's OMP configuration rather than supplied as runtime metadata. | `0c7c2da40bfd69ff30a028b842d4683f313d3f0038e6aa29a615e64a8dc88f5f` |

The contract and draft-summary findings are session-associated timestamps/outcome metadata, not concrete R1 identities. The dead-seat evidence is a same-wave receipt, but it still contains other-seat output and the global privacy rule treats retained retry/exit/timestamp values as sensitive. No actual personal name or email was found; the account identifier above is the only personal/account-identity candidate. No concrete private-document path was found.

## Frozen C1 token allowlist candidates (rules a/b)

The C1 scan found **43** token matches across the files below. All are surface-only instruction/contract/class-analysis text (rule **a**) or field/key names in the frozen policy (rule **b**); none of these matches is itself a copied private value. They are **allowlist candidates**, not allowlist rows already admitted. R1, R3 and R9 had no matches. In particular, the payloads' session-store glob is not an R2 hit because the class excludes a wildcard immediately after the prefix.

| Path:line | C1 token matches; rule | SHA-256 |
|---|---|---|
| `.ufo/waves/round-18/frozen/c1-policy.json:8,11-12,14` | R2, R5, R6 (rule a); four R8 field/key names (rule b); 7 matches | `db06e9810bbfd243fb0a753a46960573df39083ea90174ce463cf2a0ab523128` |
| `.ufo/waves/round-18/build/AdjDocumentRefs.md:33` | R6; rule a; 1 match | `60fdfb0778f475de275a52a7fd21be830332144f5ee71bb3651f6f12f968f5af` |
| `.ufo/waves/round-18/build/SentinelContextAudit.md:29` | R6; rule a; 1 match | `0b5717eeb2dc516bfb8fbc2146737c929eeee015dbdb6ba59bd0fd01b6e53c0c` |
| `.ufo/waves/round-18/build/SweepR15Md2.md:53` | R6; rule a; 1 match | `bb95ec6f24b34aa925b9805af758bf43d9e74c35618ab585d26e69e96fe78bfa` |
| `.ufo/waves/round-18/build/SweepR17Falsify4.md:15` | R6; rule a; 1 match | `47d52312ab8433948c91bd0e46cad7070b844bd22e7fe896a26e942759e83216` |
| `.ufo/waves/round-18/residual-drafting-taskcall.json:5` | R4, R5, R7 and R6 ×2; rule a; 5 matches | `9fbd918af8b7ac1f9d7bff1f070c38e83726797bb2540dd7906b5216402fc68e` |
| `.ufo/waves/round-18/wave1-dispatch.json:445,550,555,560` | R4, R5, R7 and R6 ×6; rule a; 9 matches | `84bfb3dd29a23ec5c8715478d316ab89df6aba4e96fb6f81b7ad81ba51ac0d7e` |
| `.ufo/waves/round-18/wave1-plan.json:4,555,560,565` | R4, R5, R7 and R6 ×6; rule a; 9 matches | `a6c0240d740b32cb7ca1f4bd99169074a377105693a2b4e77c5fcbb7a7a093e9` |
| `.ufo/waves/round-18/wave1-spec.json:5,110,115,120` | R4, R5, R7 and R6 ×6; rule a; 9 matches | `1e9772c4842f54e0ee050b3fa9a62c442437f4b0fa3e83d8ba291bfe8a21541e` |

## Negative findings and limits

- No full R1 session identity, R3 numbered tool-output artifact, or R9 session-record-value match was found at the pinned revision; the supplementary UUID/session-ID, email, and concrete private-document-path searches were also empty.
- R4/R5/R6/R7 occurrences in the task payloads are instructions naming prohibited surfaces; the four R6 report mentions are class/boundary statements. R8 occurrences are field/key names in the policy. The synthetic retention snapshot had no raw R4 match.
- References to the Kagi lane and same-wave seat labels were treated as lane/seat names, not personal identities. No independent human name or email was observed.
- The frozen policy states its regexes are a recall floor. The targeted qualitative reading found the P1–P3 data above; this report is not a proof that all unrecognized private context is absent from every blob.

## Method and execution record

- Read `contract.md`, the frozen C1 policy/population metadata, frozen C2/C3 inputs, `draft-verdicts.md`, and `out-of-metric-triage.md` first; then inspected the risk-bearing round-18 files and token-hit lines. Target artifact content came from the pinned revision; the required Godspeed skill was read separately, and only the current report-directory listing came from the later checkout.
- Read-only `git log` and `git ls-tree` at the lane returned success (exit 0); the target tree contained 77 tracked files. `git show <rev>:<path>` and `git show <rev>:<path> | sha256sum` returned success (exit 0) for the cited blobs.
- `git grep` searches were scoped to the pinned revision and round-18 tree: a matching search returns 0; a no-match search returns 1. Pattern/count pipelines did not retain matched private text in this report. One malformed R2 regex attempt and one mistyped-root read/hash attempt were discarded; their exit codes were not captured, and neither supplied a finding.
- No URLs were opened, no tools installed or updated, no tests/selftests run, and no VCS mutation, scratch write, or write outside this report was performed.
