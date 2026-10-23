# Routed D2 — A1 loosening

## Ready-to-paste `## Mistakes` row

```markdown
- **M1 — A1 silently weakened C1's frozen case-uniqueness predicate (class: undisclosed-contract-relaxation).** Evidence: the frozen contract requires each row's case id to exist in exactly one eligible fixture file (`a66751b1:.ufo/waves/round-30/contract.md:32-36`; the original contract is identified at `round-30-verifier-spotcheck.md:38-39`). Amendment A1's preamble says "nothing is narrowed" (`05db57ed:.ufo/waves/round-30/contract.md:124`), but its added 3a text permits a case id in more than one eligible file when copies' `inputs` and `expect` are identical (`05db57ed:.ufo/waves/round-30/contract.md:136-137`). This relaxes the exactly-one predicate. Captured-by: QUALITY 25 says narrowing must be an explicit correction, not a silent edit (`corpus/QUALITY.md:50`). It did not catch this at amendment time: the round-30 spotcheck records both the relaxation and the absence of a `## Mistakes` row (`round-30-verifier-spotcheck.md:34-37,179-181`). [INFERENCE] The criterion was not operationalized as an amendment-versus-frozen-predicate check; A1's broad preamble was not tested against its condition-level change. Fix: before accepting an amendment, compare every amended condition against the frozen predicate, list each removed or loosened obligation, and fail if an undisclosed relaxation remains. Show that the check can fail by applying it to A1 and requiring a red result that names condition 3a's `exactly one` → `more than one when identical` change despite the preamble; retain that failing receipt (and an unchanged-predicate control). A3 (`55f9a694`) is no precedent: its contract labels it AFTER the L1 ran the A2 gate and describes a gate-allowlist counter change after data (`.ufo/waves/round-30/contract.md:207-218`); the spotcheck explicitly says not to use A3 as precedent (`round-30-verifier-spotcheck.md:180-181`).
```

## Behavior and finding

- The frozen C1 condition at `a66751b1` says each case id occurs in exactly one eligible fixture file; A1 adds an identical-copy exception at `05db57ed` while its preamble claims nothing was narrowed (`a66751b1:.ufo/waves/round-30/contract.md:32-36`; `05db57ed:.ufo/waves/round-30/contract.md:124,136-137`).
- QUALITY 25 is the relevant capture rule (`corpus/QUALITY.md:50`). The outside spotcheck explicitly identifies D2 and says no lesson `## Mistakes` row captured it (`round-30-verifier-spotcheck.md:179-181`).
- A3 is explicitly an after-data gate change, not a precedent for A1 (`55f9a694:.ufo/waves/round-30/contract.md:207-218`; `round-30-verifier-spotcheck.md:180-181`).
- [INFERENCE] The miss was failure to operationalize QUALITY 25 as a condition-by-condition amendment review: the cited records show the policy, the contrary A1 preamble and addition, and the later spotcheck finding, but no intervening diff-check receipt.

## Gates and limits

- No test, build, linter, or proposed amendment-diff check was run. The check and its red A1 demonstration above are recommendations, not executed evidence.
- No tools were installed or updated. No source, gate, lesson, or harness file was modified by this seat. `corpus/lessons/round-31.md` was not present when read; this seat is authorized to write only this report, so the row is a draft for integration.
- Every shell command below was wrapped in `timeout -s KILL 120s` and set `ulimit -v 1048576`; all returned finite output synchronously. No background process was started.

## Evidence commands and outcomes

1. `timeout -s KILL 120s bash -c 'ulimit -v 1048576; git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 05db57ed -- .ufo/waves/round-30/contract.md'` — returned commit `05db57ed08e53512c749c97cbc4e0360fb5ad3c5` and the A1 addition; its preamble says nothing is narrowed, and clause 3a permits identical duplicates.
2. `timeout -s KILL 120s bash -c 'ulimit -v 1048576; git -C /home/vgpnk/Projects/shokunin/mori-shokunin show a66751b1:.ufo/waves/round-30/contract.md'` — returned the frozen contract; its condition 3 is the exactly-one rule, confirmed at line 32 by the locator command below.
3. `timeout -s KILL 120s bash -c 'ulimit -v 1048576; git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -n -E "exactly one|Every row.s case id" a66751b1 -- .ufo/waves/round-30/contract.md'` — returned frozen line 32 with "exists in exactly one".
4. `timeout -s KILL 120s bash -c 'ulimit -v 1048576; git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -n -E "nothing is narrowed|case id may occur" 05db57ed -- .ufo/waves/round-30/contract.md'` — returned A1 lines 124 and 136.
5. `timeout -s KILL 120s bash -c 'ulimit -v 1048576; git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -n -E "identical|Every row.s case id exists in exactly one" 05db57ed -- .ufo/waves/round-30/contract.md'` — returned frozen line 32 and A1 line 137.
6. `timeout -s KILL 120s bash -c 'ulimit -v 1048576; git -C /home/vgpnk/Projects/shokunin/mori-shokunin show --format=fuller --stat 55f9a694 && git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 55f9a694 -- .ufo/waves/round-30/contract.md'` — returned the A3 commit metadata and diff; its message calls it an after-data gate change, and the contract says AFTER the gate run and that the allowlist change followed data.

Read-only document evidence: `corpus/lessons/round-30-verifier-spotcheck.md:32-40,179-181` records A1's relaxation, unchanged preamble, and D2; `corpus/QUALITY.md:50` gives criterion 25. The round-30 lesson's existing M1 style was read at `corpus/lessons/round-30.md:24-42`. The attempted read of `corpus/lessons/round-31.md:1-80` returned “not found.”

## Surfaces and artifact

- Written: `.ufo/waves/round-31/w1/MineA1Loosening.md` (this report only).
- Read-only evidence surfaces: `corpus/lessons/round-30-verifier-spotcheck.md`, `corpus/QUALITY.md`, round-30 contract blobs at `a66751b1`, `05db57ed`, and `55f9a694`, and `corpus/lessons/round-30.md` for row style.
- Out of scope and untouched: product code, judge, lesson file, commits, pushes, publication, deployment, runtime, and harness configuration.
