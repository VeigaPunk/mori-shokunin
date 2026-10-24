# Round-17 build privacy reading sweep

## Scope and method

Read the round-18 contract, `frozen/c1-policy.json`, `frozen/c1-population.json`, and all 11 requested round-17 build reports at frozen revision `d005cdde0e009dea6c0cc29b37163de536528658`. Each report was read fully; SHA-256 of the worktree file was compared with `git show d005cdde0e009dea6c0cc29b37163de536528658:<path> | sha256sum` (rc 0 for each). All match that revision except `PacmanActorTrace.md`: its d005 blob is SHA-256 `109e92f4d846c80d08a7ccb18c51dd42d1c0aabb9e921709515421c5f79097ef` (157 lines); the worktree currently has a distinct 90-line replacement (SHA-256 `b30443665d48a32bb49dfa501eef8ec594a3ab03b299bf9e84d0904b6512d1bf`). Findings and line numbers below refer to the committed d005 blob, as requested. No files other than this report were written; no VCS mutation, installs, URLs, or live host/session queries were made.

The tables do not quote target text. A cited line count is the number of affected source lines, not the number of private values. SHA-256 is for the complete committed report blob. `C1 missed` means the finding is outside R1–R9; a listed R-class is an overlap already enumerated by the frozen population.

## Findings beyond C1 classes

| Report (SHA-256) | Path:line(s); count | Kind | Minimal redaction |
|---|---:|---|---|
| `OmpRetryDocs.md` (`d4e72fa321596cbf1a1acfb1823e3427350e51839718984e76a08c5c2c307f30`) | `:240`; 1 | Concrete-looking session-filename/seat example with a partial identity; C1 missed the abbreviated form. | Replace the example with `<timestamp>_<session-id>.jsonl`; remove the concrete seat example. |
| same | `:252`; 1 | Session-store root path/pattern, not a concrete child path; R2 does not match the root-only form. | Use `<session-store-root>` or omit the path. |
| `OverlapJjSiblings.md` (`1288f404ba4293d0e2f1a8d48b415998c31ee0d3fe279a2392bba7f0c5875e82`) | `:12`; 1 | Cross-report git identity probe output: personal identity/email and exact revision values. C1 missed. | Remove identity/email and exact revisions; retain only the abstract author/committer divergence. |
| same | `:15`; 1 | Cross-report repository-ref/state probe output. C1 missed; private-repository sensitivity is [INFERENCE]. | Replace the observed ref/state tuple with the generic resolver edge case. |
| `OverlapTsukuroi.md` (`83bf9fad237998eebe92f17cacdff031e5f29b701334e7b08ebee2026bc39322`) | `:25-39`; 15 | Detailed host package-transaction commands, times, paths, and results. These are operator-specific host activity; classification as private host history is [INFERENCE]. | Retain only a bounded event summary and handoff; remove argv, per-package rows, exact times and local paths. |
| same | `:85-94, :98-102`; 15 | Paraphrased outputs/capture results from other seats, including detailed boot, package, memory, and census state. C1 missed. | Keep source references and ownership boundary only; remove the copied state/results and exact event details. |
| same | `:95-97`; 3 | Cross-session privileged attribution and operator personal-document/session-intent facts. Line `:96` also has frozen class R4. | Remove actor identity, personal-document location and intent details; retain only that attribution belongs to the authorized owner. |
| same | `:106-124`; 19 | Cross-report pause ruling, actor/host-state and service/journal findings. C1 missed. | Replace copied findings with the non-sensitive policy boundary and a source citation. |
| same | `:128-149`; 22 | Proposed note repeats capture-derived host/service and kill-class details from other reports. C1 missed. | Reduce to the dated ownership/handoff conclusion; omit event values, output identifiers and derived class details. |
| `PacmanActorTrace.md` (committed d005 blob `109e92f4d846c80d08a7ccb18c51dd42d1c0aabb9e921709515421c5f79097ef`) | `:7-8, :12-17`; 8 | Session-time correlation, transaction actor attribution, user/uid and privileged invocation facts. | Remove session correlation and personal/actor fields; report only a non-attributed event if needed. |
| same | `:21, :23-27`; 6 | Host log metadata and detailed package-command/output records, including an operator-home path. | Replace with a minimal event statement; remove command arguments, path, timestamps and transaction identifiers. |
| same | `:31-34`; 4 | Concrete session-store path, timestamped session identity and transcript metadata. R1/R2 overlap. | Remove the entire identity/path block; do not substitute another identifier. |
| same | `:36-50`; 15 | Numbered tool-output artifact metadata, excerpts/paraphrases of process stdout, invocation correlation, neighboring calls and counts. R3 overlaps at some lines. | Remove artifact identity, output content, timestamps and correlation evidence; keep only an abstract conclusion. |
| same | `:52-57`; 6 | Operator personal-document location/content summary and planned-vs-executed command details. R4 overlaps. | Remove the document reference and intent/command comparison; retain only a non-attributed transaction summary. |
| same | `:59-61`; 3 | Cross-seat report claims and timing used to infer who acted. | Remove the seat/report attribution evidence; retain uncertainty without the source-seat trail. |
| same | `:65-78`; 14 | Additional session-store identity/inventory, numbered log references, log-body summaries and cross-project session-store facts. R1/R2/R3 overlap at some lines. | Remove store roots, child identities, numbered artifacts and content summaries. |
| same | `:82-105`; 24 | Package-cache owner/timestamps, session-store search results, shell-history and login facts, privileged logging/accounting state, and other agent-store inventory. R5/R6 overlap at some lines. | Remove the filesystem/history/privileged-configuration results and all store inventory; keep only the conclusion needed for the report. |
| same | `:109-119`; 11 | Inferences associating an exact session/seat, personal account, interactive shell, and privilege escalation with transactions. | Remove the session/seat/person and privilege-path inferences; state actor as unknown unless independently authorized. |
| same | `:123-129`; 7 | Residual actor/session identity and transcript-mining details. | Keep only the generic evidence limitation; omit artifact and transcript identity discussion. |
| same | `:135-155`; 21 | Command/result table reproducing session-store searches, shell-history, login, and privileged-configuration results. R3/R5/R6 overlap at some lines. | Remove the private command/result rows; summarize only the safe verification boundary. |
| `PacmanTxnToday.md` (`26cd1ee28aa5124e68f2ac9baee0b38681cc0bdf3fa7885571499b51a88ab37c`) | `:12-24, :30-49, :51-67, :71-88, :90-113`; 91 | Detailed operator host transaction history, full command/package rows, exact event times and internal pause/dispatch timeline. C1 missed. | Replace with counts or a short authorized handoff; remove transaction-level argv, package/version rows and exact internal timeline. |
| same | `:117-125`; 9 | Another seat's journal-derived actor/account and working-directory attribution plus related safety-gate evidence. Line `:119` also has frozen class R4. | Remove account and working-directory details and copied journal attribution; leave actor unknown or cite the authorized handoff without its values. |
| same | `:128-132`; 5 | Specific scratch/cache path and post-event log-state details. C1 missed. | Remove local path and exact observation-time details; retain only the policy-relevant conclusion. |
| `ProvinceFrontier.md` (`b3e55b617fa87565a322503290bbc55fc3b26a7bd209175d6970ce162815f434`) | `:28-31`; 4 | Host package/version and boot-time measurements. C1 missed. | Keep a dated, high-level version-change statement only; omit exact versions, times and counters. |
| same | `:38-44`; 7 | Exact hashes and outputs from prior capability/live-window receipts and version records. C1 missed. | Cite the receipt paths and bounded disposition only; remove raw output values, digests and timestamps. |
| same | `:190-214`; 25 | Reproduction of gate and live journal receipt results, counts, identifiers and limits from another wave's evidence. C1 missed. | Replace the copied receipt payload with a path citation and one-line scope statement. |
| same | `:219-249`; 31 | Quoted prior host-version note plus detailed package-upgrade/boot/version measurements and resulting inference. C1 missed. | Remove the quoted prior note and exact host measurements; retain only the dated correction and its source path. |
| same | `:252-264`; 13 | Repeated historical/current host-version and live-capture facts in a proposed note. C1 missed. | Remove the copied version/capture values; point to the authoritative record without transcribing it. |
| same | `:268-278`; 11 | Recap of host measurements and inference about process/version state. C1 missed. | Keep the uncertainty statement; remove the underlying exact measurements and repeated evidence values. |
| `ProvinceNotesDraft.md` (`1cae4366b881c4616a8c516963f4bfd7fe0902327b3ed9ff4d8084cfdae59477`) | `:19-29`; 11 | Command/read outputs, search-result counts, package-database and file-metadata facts. C1 missed. | Replace the raw result inventory with a minimal source citation and relevant conclusion. |
| same | `:42-50`; 9 | Copied prior gate and live journal result values, counts and execution status. C1 missed. | Cite the receipt only; remove copied result payloads and counters. |
| same | `:61-78`; 18 | Host-version, package-log/database and capture-derived measurements, including exact timestamps and inference. C1 missed. | Use dated source references without copying measurements or output values. |
| same | `:101-111`; 11 | Detailed host package/boot transaction and operator safety/pause context. C1 missed. | Replace with a high-level, non-attributed handoff; remove package/version/time detail and operator-action speculation. |
| `QualityCriteriaDraft.md` (`f943c8c71d7279447c4aa610de3cc4316f374449f624239391cc064d0a0f1866`) | `:27-34`; 8 | Internal wave receipt digests/times and dispatch-attempt result fields. C1 missed. | Preserve the acceptance rule, but remove concrete receipt identifiers, times and attempt values. |
| same | `:41`; 1 | Other-seat live-probe outputs and a background-job identifier. C1 missed. | Describe the disclosure gap abstractly; omit command results and job identity. |
| same | `:62-64`; 3 | Cross-report VCS probe output and exact revisions. C1 missed. | Keep the generic branch-divergence lesson; remove sandbox revision values. |
| same | `:73`; 1 | A concrete provider-error/session-message example, i.e. a non-allowlisted session-record value. C1 missed. | Replace the error text/code example with a generic placeholder or point to the contract without reproducing the record value. |
| `R16LessonM7.md` (`bd91c7c8b4da50223f7e01c43a6e4ccf0e88347e482f9b931c54063957fb7854`) | `:22, :24-32`; 10 | Other-seat lesson/tool activity, temporary output names and background-job identity. C1 missed. | Replace the copied row with a short evidence-pointer correction; omit temporary paths and job identity. |
| same | `:36-49`; 14 | Other-seat live journal output and derived cursor/boot, byte-count, access and host-version facts. C1 missed. | Keep only the fact that the cited block contains live probes; remove output fields, values, counts and identity/group facts. |
| same | `:60`; 1 | Proposed append reproduces the same journal outputs, temporary paths, background-job and host identity details. C1 missed. | Replace with the short line-pointer correction at `:63-65`, after removing its copied values. |
| same | `:63-65, :69-79`; 14 | Repeated job/probe timing and journal-command/output metadata. C1 missed. | Keep only a high-level completeness note; remove probe/result particulars and identity-linked metadata. |

## Frozen C1 population cross-check

At d005, the population file records these hits within the requested set (no matched text reproduced):

- `OmpRetryDocs.md`: 3 hit records — `:34 R2`, `:42 R9`, `:55 R9`.
- `OverlapTsukuroi.md`: 1 — `:96 R4`.
- `PacmanActorTrace.md`: 18 hit records across 17 unique lines — `R1 :32,:34,:66`; `R2 :31,:66`; `R3 :36,:45,:47,:48,:90,:144,:145`; `R4 :53`; `R5 :95,:146,:147`; `R6 :103,:152`.
- `PacmanTxnToday.md`: 1 — `:119 R4`.
- The other seven requested reports have no R1–R9 population hits. The reading-sweep findings above are independent of that count.

## Repeated facts among requested reports

- **From `PacmanActorTrace.md`:** transaction/actor material recurs in `OverlapTsukuroi.md:25-39,95-97`, `PacmanTxnToday.md:15-16,39,48,117-121`, and `ProvinceNotesDraft.md:101-111`. These repetitions include content that should be minimized along with the source; the cited ranges above identify it without restating it.
- **From `OmpRetryConfig.md`:** `OmpRetryDocs.md:81-87,94-107,148-156,259-271` repeats retry-default/fallback/error-class analysis. This is an overlap in subject matter; no concrete operator routing/candidate value from the source was observed in those target lines. `QualityCriteriaDraft.md:73` repeats the concrete session-error example, which should be removed as noted above.
- **From `SessionExitCorrelation.md`:** `OmpRetryDocs.md:40-42,195-235,281-287`, `OverlapKumitate.md:11,25-28`, and `QualityCriteriaDraft.md:70-77` repeat generic session-exit/recovery or terminal-count/resumability conclusions. No empirical cross-tab counts or actual disposal-field values from `SessionExitCorrelation.md` were found repeated in the requested reports.

## Clean files

- `OverlapAuditLanes.md` (`ec7269e51800f0ea69830bdfdc398acdd09dcb7f23db759af6c75671b8c67481`): no private-context retention found beyond public contract/tool descriptions.
- `OverlapKumitate.md` (`0255eb6bc65c4cc8d2ee26756fc46a6b3b3355c79e74d5458107ac866a050819`): only generic routing ownership/architecture discussion; no concrete operator route/provider/model values or session/tool outputs identified.

## Commands and installs

- SHA comparison command form: `sha256sum <worktree-file>` and `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show d005cdde0e009dea6c0cc29b37163de536528658:<lane-relative-path> | sha256sum`; rc 0 for each requested report. For committed `PacmanActorTrace.md`, `git show ... | nl -ba` returned rc 0 for line mapping.
- Installs or updates: none.
