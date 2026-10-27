# mori round 55 — frozen contract (L1 MoriR55, attempt 1)

Entering lane tip: `ca52426ea496bc6592e3e867cc9d28843e45f196` (round-54 admitted closure; spot-check `corpus/lessons/round-54-verifier-spotcheck.md`).
Freeze includes this contract, both counters, their control/selftest code, the source copies and their pins, scope listing,
control readings, selftest receipts, census-start and misroot precheck. The contract and counters are immutable after any
seat scores; source evidence is pinned in `evidence/freeze-sha256.txt`.

Scores entering: coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6. Lowest non-retired axes
are depth, freshness and calibration (tied at 5). Two non-exploratory claims, each on a distinct lowest axis, no score
number change claimed; closure sets axis verdicts. The planner seat is held by the L1 (the validator does not permit a
planner role).

## C1 — freshness: release recheck of out-of-ledger v7.2 Linux pointers

Predicate P-C1 is the exact counter docstring in `count-c1.py`. It counts the explicit extraction of Linux-v7.2 line
pointers in the four previously out-of-scope entries, at entering revision `ca52426ea496bc6592e3e867cc9d28843e45f196`. Frozen scope: 78 unique
(entry, path, lines) pointers (including comma-line groups and same-line continuation tokens), of which 69 derive
`same`, 7 `moved`, 2 `changed`; `watchdog-identity-r31.md` has cited v7.2 kernel S-ids but no matching line pointers and
therefore contributes no pointer. The line/status arm is mechanical; reviewers judge claim meaning and hold/stale.

Target at landed revision: all 78 scoped hashes in `kernel-v7.3-recheck-r55.md`, all source pins correct, v7.3 pointers
within bounds and statuses independently derived by the frozen counter, with 2+ settled, output-bound RECHECK voters
per row and no dissent. Command: `python3 .ufo/waves/round-55/count-c1.py R`. Before: ledger absent at entering tip,
`scope=78 rows=0`, exit 1. Controls in `controls/` and selftest receipt: do-nothing, copies-only, all-same label, v7.2
line relabel, mislocated line, missing/extra/duplicate rows, wrong source URL/open date/status/provenance, missing or
unbound voters, dissent, fenced votes, bad pins and synthetic feasibility witness. Kill: any missing row, line/status
mismatch, bad pin/provenance, or uncovered/dissenting vote => unmet. C1 is separable from C2.

## C2 — depth: ENOSPC runway is not just the filesystem's block column

Predicate P-C2 is the exact counter docstring in `count-c2.py`. Surface: knowledge and source-grounded interpretation of
free blocks available to unprivileged writers, independent inode runway, XFS statfs behavior, btrfs metadata/global
reserve availability and sysfs observations, tmpfs's independent size/inode limits, and ENOSPC versus EDQUOT boundary.
The source table has 23 unique claims, 9 sources, at least 16 claims/6 sources required. The live host snapshot is a
read-only observation, not an ENOSPC reproduction or a counted subclaim.

Target: 23 claims with 6–25-word located quotes and source rows, every source hash pinned, at least two settled,
output-bound ENTAIL voters per final claim text and no overclaims. Command: `python3 .ufo/waves/round-55/count-c2.py R`.
Before: entry absent at entering tip, exit 1. Controls/selftest include do-nothing, no table, quote mutation, queued source,
no votes/unbound votes/overclaim and feasibility witness. Kill: missing/invalid source, non-located quote, fewer than 16
rows or 6 sources, no votes, dissent or bad pin => unmet. C2 is separable from C1.

## Frontier and routed defects

Round-54 routed corrections D1–D6 are appended (never rewrite prior lesson/report): capture census output mechanically;
correct the four S515/S520/S522/S525 Gate locators; narrow panic switch wording; correct SCORECARD Ten→12/14;
commit r54 dispatch marker; correct seat-report count and M-label pointers. C2 reuses round-54's planned disk-runway topic only
if shown not already held; it is novel to the covered corpus. Assimilation is none unless package material is located and
opened this round; quarantine slice is re-derived. considerthese proposals checked.

Start census receipt: `evidence/census-start.txt`. End census must exit 0. Mistake mined: `corpus/lessons/round-54-verifier-spotcheck.md` D1–D6. One v2 wave `w1` (64 seats) carries build and falsification; attack seats at least 16 (25%). Residual work only if it is fewer than 32 concrete attack items, with explicit residual call.
