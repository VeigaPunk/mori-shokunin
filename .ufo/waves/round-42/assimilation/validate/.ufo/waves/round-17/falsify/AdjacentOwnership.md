# AdjacentOwnership — C3 candidate vs souji cleanup

Date: 2026-10-20. Seat: `MoriR17.AdjacentOwnership-4`. Advisory only; L1 remains planner and sole integrator. No admission judgment.

## Axes

- **C3 calibration (improved, documentation only):** a `candidate_misroot` is a review lead. It is not a souji removal order, and it is not evidence the file is stale.
- **C1 coverage (held):** terminal-at-scan stays observation. Provider/model labels and `dead_*` classes do not become kumitate route or fallback inputs.
- **C2 operability (held):** branch/author findings stay diagnostic. No bookmark, author, or publication repair.
- **Tsukuroi / kagi (held):** package-log rows stay detection. Credential material stays unread and unreported.

## Local evidence

1. C3 emits `class: candidate_misroot` with path, size, and `matched_in` only. The payload sets `detection_only: true` and `moves_or_deletes: false` (`tools/mori-misroot-sweep.py:307-334`). Help says a candidate is a review lead, not ownership proof, and the tool never moves, deletes, edits, or commits (`tools/mori-misroot-sweep.py:789-798`).
2. The province closure notes hand package transactions to tsukuroi and terminal status away from kumitate (`PROVINCE.md:103-120`). The souji row only says souji “acts on artifacts” (`PROVINCE.md:69`). C3 has no matching handoff sentence. `corpus/README.md:357` says ownership is reviewed before moving anything, but that sentence is not in the province table.
3. Souji refuses live lane work products, including current-round drafts and uncommitted reports (`../souji-shokunin/PROVINCE.md:42`). Its adjacency line is complementary observation versus artifact action, not a license to delete on mori’s finding (`../souji-shokunin/PROVINCE.md:45-46`). Souji’s own 2026-10-20 log left a prescribed misroot sweep’s other-round paths untouched (`../souji-shokunin/LOG.md:795-802`).
4. C1 knowledge already refuses routing: error-string tokens are not kumitate dispatch or fallback decisions (`corpus/knowledge/seat-terminal-status-r17.md:50-51`). The classifier reads `errorMessage` only to derive retry and error-code scalars (`tools/mori-seat-terminal.py:217-243`). The seat record omits that text (`tools/mori-seat-terminal.py:369-384`). Non-message types, including `credential_pin`, are skipped (`contract.md:45-46`). The selftest forbids echoing `errorMessage`, `credential_pin`, content, and usage (`tools/mori-seat-terminal.py:511-518`).
5. C2 knowledge already refuses repair: a mismatch does not authorize bookmark repair, rebase, force-push, author-field changes, routing, or worker replacement (`corpus/knowledge/jj-branch-anchor-r17.md:50-55`).
6. The tsukuroi package handoff is already present and is not widened here (`PROVINCE.md:111-117`; `corpus/lessons/round-17.md:88-96`).

**Contradiction:** README and the tool say “review before moving.” The province souji row can be read as “souji acts on whatever mori lists.” Those are not the same owner. A current-round uncommitted report can be a true misroot candidate and still be outside souji’s allowed removals.

## Proposed move

Append one sentence to the round-17 province closure, beside the existing tsukuroi handoff. Do not edit the tool, souji, or kumitate.

> **Adjacent souji handoff, detection only:** `tools/mori-misroot-sweep.py` emits `candidate_misroot` as a review lead (`detection_only`, `moves_or_deletes: false`). A candidate is not a removal, quarantine, or commit order, and not proof the file is stale or unowned. Souji may act only under its own receipt rules; it refuses live current-round drafts and uncommitted reports (`../souji-shokunin/PROVINCE.md:42`). Mori never moves or deletes the file. Credential-shaped bytes, if seen while classifying, are not reported; hygiene evidence stays with kagi.

## Risks

- **Runtime:** exit 1 means at least one candidate, not permission to clean. Wiring that status into souji would delete or quarantine a live report the province forbids. [INFERENCE] A path-only match can name a file whose body is unrelated.
- **Contract:** git-ignored files stay invisible (`tools/mori-misroot-sweep.py:793-794`). A clean sweep is not an empty fleet root. Ignored credential files are not a kagi scan.
- **Substrate:** kumitate still owns resume, reroute, and dispatch. Tsukuroi still owns package and boot diagnosis. This sentence does not move either.
- **Verification:** C3’s existing sandbox witness checks detection, not the absence of a cleanup caller. After the sentence lands, confirm the province names `candidate_misroot` as a review lead and names souji’s live-report refusal. Do not treat that sentence as a new tool test.

## Verification performed

Static reads only: province closure, C1/C2 knowledge notes, C3 tool payload and help, souji province and log, contract field rule, README index line. No shell, no selftest, no live transcript, no journal, no VCS mutation. No tool installed or updated.
