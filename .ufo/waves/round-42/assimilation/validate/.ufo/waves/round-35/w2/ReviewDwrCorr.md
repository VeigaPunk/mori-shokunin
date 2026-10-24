measured 2026-10-23T09:15:12Z

# ReviewDwrCorr — attack on `## Round-35 correction`, `corpus/knowledge/disk-write-rate-r33.md`

Tip under review: `cedb0ec4f3a4f672804deac388b7191258f01fcd`. The correction occupies
`corpus/knowledge/disk-write-rate-r33.md:100-108` at that revision (`git show` diff vs `5c3e2dd` confirms
append-only: only lines 100-108 added). Every claim below was checked with read-only git at the pinned revision.

## Per-statement verdicts

VERDICT: supported — "routed by `corpus/lessons/round-34-verifier-spotcheck.md` §6 item 3". §6 is "Routed defects"
and item 3 (`round-34-verifier-spotcheck.md:205-206`) reads: "**Dangling pointer.**
`corpus/knowledge/disk-write-rate-r33.md:71` cites the uncommitted `.ufo/waves/round-34/w1/`. Land an append-only
correction that names the committed audit seats instead." The correction is exactly that. `:71` at tip still holds
the `w1/` citation (`disk-write-rate-r33.md:71`).

VERDICT: supported — "The Round-34 revision header above says rows 3r, 6r, 7r and 13r were drafted by attempt-1
seats in `.ufo/waves/round-34/w1/`." Header at `disk-write-rate-r33.md:70-71`: "Drafted by round-34 attempt-1 seats
RepairRow03, RepairRow06, RepairRow07 and RepairRow13 (`.ufo/waves/round-34/w1/`), integrated by the L1 (attempt 2)
and judged by a non-author seat in round 34 wave A". Quoted correctly.

VERDICT: supported — "That directory was never committed, so the pointer does not resolve." `git ls-tree
cedb0ec:.ufo/waves/round-34/` lists only `c0`, `evidence`, `wa`, `wb` (plus files); no `w1` entry. `git log --all
--oneline -- .ufo/waves/round-34/w1/` returns 0 commits — no commit on any ref ever touched the path. The pointer
cannot resolve in any committed tree.

VERDICT: supported — "The committed judgments of those rows are the attempt-2 wave-A judges `wa/JudgeRow3r.md`,
`JudgeRow6r.md`, `JudgeRow7r.md`, `JudgeRow13r.md`, and the attempt-3 wave-B re-judges `wb/ReJudgeRow3r.md`,
`ReJudgeRow6r.md`, `ReJudgeRow7r.md`, `ReJudgeRow13r.md`." All eight files exist as committed blobs
(`git ls-tree cedb0ec .ufo/waves/round-34/wa/ wb/`). A recursive ls-tree of `.ufo/waves/round-34/` shows no other
judge/rejudge receipt for these rows outside `wa/` and `wb/` (c0, evidence contain none). Attempt numbering holds:
`wa-spec.json` context reads "mori round 34 (attempt 2) — wave A", `wb-spec.json` reads "(attempt 3) — wave B";
`corpus/lessons/round-34.md:1-4` records attempt 1 dying 05:25:25Z and attempt 2 dying 06:19:06Z, and the wa
receipts are measured 05:38-05:39Z (inside attempt 2) while the wb receipts are 07:40-07:56Z (attempt 3).
`wa-spec.json` seats JudgeRow{3r,6r,7r,13r} carry `role: reviewer`, distinct from the named attempt-1 drafting
seats, consistent with the header's "non-author seat".

VERDICT: supported — "Wave A judged row 3r supported (`wa/JudgeRow3r.md:33`)". Line 33 is exactly
"VERDICT: row 3r: supported".

VERDICT: supported — "wave B judged it unsupported (`wb/ReJudgeRow3r.md:36`)". Line 36 is exactly
"VERDICT: row 3r: unsupported".

VERDICT: supported — "row 3r2 supersedes it (`wb/residual/MoriR34A3.JudgeRow3r2.md:95`, supported)". The
supersession itself is in-file (`disk-write-rate-r33.md:97`: "row 3r2 supersedes it"), the receipt
`wb/residual/MoriR34A3.JudgeRow3r2.md` is committed, and its line 95 is "VERDICT: row 3r2: supported". The residual
dispatch (`wb-residual-dispatch.json`) shows a dedicated `JudgeRow3r2` seat (agent `reviewer`) under attempt-3
context judging snapshotted bytes.

VERDICT: supported — "Rows 6r, 7r and 13r were judged supported by both waves." `wa/JudgeRow6r.md:68`,
`wa/JudgeRow7r.md:43`, `wa/JudgeRow13r.md:61`; `wb/ReJudgeRow6r.md:117`, `wb/ReJudgeRow7r.md:66`,
`wb/ReJudgeRow13r.md:82` — each reads "VERDICT: row <N>: supported".

VERDICT: supported — "Drafting seats' own outputs are not evidence." Consistent with the lane's stated rule:
`corpus/lessons/round-34.md:3-4` — "Every attempt-1/2 file that was not committed is untrusted". Normative
statement, not a resolvable pointer.

## Residual risk / verification gaps

- `wb/residual/MoriR34A3.JudgeRow3r2.md` is a `MoriR34A3.*` sub-seat — a reviewer seat delegated inside the
  attempt-3 L1 scope (`MoriR34A3` is the L1 and only integration owner per `wb-spec.json`), judging L1-made
  revisions. The residual call did dispatch it as a separate `reviewer` seat judging snapshotted bytes, so the
  "supported" verdict is real, but it is not as arm's-length as the wave-A/B judges the correction foregrounds. The
  correction does not claim otherwise.
- The spotcheck also flagged a second dead `w1/` pointer (`wb/GateS195.md:26`, noted at
  `round-34-verifier-spotcheck.md:135`). Item 3 routed only the knowledge-file pointer; the correction correctly
  repairs the routed one. `wb/GateS195.md:26` remains a dead evidence pointer inside a committed receipt —
  observation only, outside this correction's text.
- `wa/JudgeRow3r.md` (supported) was overturned by `wb/ReJudgeRow3r.md` (unsupported) on an unstated-premise
  argument (`wb/ReJudgeRow3r.md:24,67`); the correction reports both verdicts without endorsing either, and the
  superseding 3r2 row resolves the defect. Accurate.
- No tools installed or updated this run (all reads via read-only `git show`/`ls-tree`/`log`/`diff`).
