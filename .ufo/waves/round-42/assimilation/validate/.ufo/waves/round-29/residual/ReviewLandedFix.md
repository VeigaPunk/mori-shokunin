# Residual review — landed tool change (cdfcf66d vs 7118f320) against A2-05/06/07/10

Seat: MoriR29.ReviewLandedFix (wave 2, residual). 2026-10-22. Recommendations only; a verdict I
emit is not a ruling. No LSP device exists in this seat's toolset (not in the harness inventory),
so caller/definition checks were done by direct source read and by executing the pure reader at
both revisions; no semantic server cross-check is behind any claim below.

## Setup and provenance

- Sandbox clone at cdfcf66d9da2e5598aa844195f85fd74d6379968 under
  `/fast/scratch/hyaku/mori-r29/residual/ReviewLandedFix/clone` (git read-only, env-unset);
  `git show 7118f320:tools/mori-oom-killers.py` extracted the base tool.
- `fix-landed.diff` matches the committed change: re-deriving base→landed differs from the
  evidence file only in diff headers (the `diff --git` line and hunk-header function suffixes);
  all content hunks are identical.
- No tools installed (tooling directive: nothing needed; python3 already present). No pacman
  transaction run. No live mode; only `--inputs`, `--selftest`.

## Selftest markers at the landed tip (all four frozen files)

| File | Result | Exit |
|---|---|---|
| cases.json | `MORI_OOM_KILLERS_SELFTEST: PASS 32/32` | 0 |
| cases-supplementary.json | `PASS 32/32` | 0 |
| cases-a2.json | `PASS 30/30` | 0 |
| cases-a2-r29.json | `FAIL 21/24` | 1 |

Residual failures (all `rule: A2-10`, all author CaseA210c): `r29-a2-10-inactive-lone-missing-stamp`,
`r29-a2-10-failed-stamped-positive`, `r29-a2-10-not-found-earlier-stamped-positive`. All three pass
their verdict/exit pins; only field expectations fail. Official counter at the landed tip
(`bash .ufo/waves/round-29/count-c2.sh cdfcf66d…`, run in the sandbox clone): case blobs match the
freeze, `provenance=24/24 unselected=0`, `shape_a207=3/2`, `shape_a210=6/2`,
`a2_r29_selftest=FAIL(exit=1)`, **`C2=unmet`, exit 1**; it also prints `blind_violations=20`
(see Residual risk).

## F1 (high — C2-blocking): the 3 residual case expectations contradict the rule text, not the tool

Evidence, case bodies in `tools/fixtures/mori-oom-killers/cases-a2-r29.json` (frozen d6d5cb0a):

1. `…inactive-lone-missing-stamp` and `…not-found-earlier-stamped-positive` expect
   `earlyoom.dryrun_send_lines: 0` and `earlyoom.process_group_lines: 0` for an inactive/absent
   unit. Round-26 contract.md:102-104: an inactive or absent killer reports `actions: null`
   "(unavailable), **never zero counts**". The tool reports null for both counters when actions is
   null (`tools/mori-oom-killers.py:456-458`). A tool change to satisfy 0 would violate the text;
   these are `case error`, not `tool error`.
2. `…failed-stamped-positive` expects `earlier_invocation_send_lines: 0` with `actions: null`,
   `state: unavailable`, and still `KILLER_ACTED`. With actions null there is no in-scope carrier
   (round-26 contract.md:97-99 keys positive evidence to in-scope send lines or oomd notices), so
   ACTED can only come through the A2-06 earlier bucket — which the case pins to 0. A failed unit
   has no current invocation (A2-02 maps failed to unavailable), so the stamped send at
   ≥ ActiveEnterTimestampMonotonic is an earlier-invocation line; the tool's `earlier=1`
   (all timestamped boot lines land in `earlier` for non-active states) is the coherent reading and
   the only carrier the contract defines. Self-contradictory case → `case error`.
3. The `earlyoom.version: "1.9.0"` / `grammar: "verified-1.9.0"` pins on all three non-active cases
   have no rule-text basis either way (round-26 contract.md:82-95 list the fields but never say a
   non-active unit reports a version; frozen c06/c07 do not pin the key). The tool nulls
   version/grammar for every non-active state (`tools/mori-oom-killers.py:433-440`). At best
   `unclear text`.

Per the round-29 protocol (`.ufo/waves/round-29/contract.md:74-79`): on `tool error` the L1 may
change the tool, never the case file; `case error` or `unclear text` on any case "is a C2 miss,
reported as one". The case file is frozen and cannot be fixed; the tool cannot satisfy items 1–2
without breaking round-26:102-104 and A2-06. So round-29 C2 is heading to a miss on these three
cases regardless of judging, and the correct disposition is to report it as such, not to change the
tool. Constraint "may not turn any KILLER_ACTED of either older file into another verdict" holds:
both older files fully pass.

## F2 (medium — answers the assigned question, no defect): the unbounded split is what A2-05/A2-06/A2-07 decide

The landed change makes an unbounded (AETM missing or 0, `tools/mori-oom-killers.py:280`) active
scope start at the last version line (`:297-302`); demoted lines fall into `earlier`
(`:326-333`). Invented input `inv1-flip-active.json` (active, AETM=0, journal = [version, real
SIGTERM, version]) shows the flip concretely:

- base 7118f320: `exit=1 KILLER_ACTED, sigterm=1, earlier=0`
- landed cdfcf66d: `exit=2 KILLERS_UNKNOWN, sigterm=0, earlier=1, scope_complete=false`

Judgment against the text: the journal holds two invocations (a version line is the first line of
an invocation, round-26 contract.md:83); the real send belongs to the invocation before the last
version line, i.e. outside the current invocation. A2-07 grounds the split at version lines; A2-06
sends such lines to `earlier_invocation_send_lines` and says that for an active unit they are
"reported without a verdict change"; A2-05 keeps `scope_complete` false (`:424`, `scope_known`
never set in the unbounded branch), and verdict rule 2 (round-26 contract.md:99-102, implemented at
`tools/mori-oom-killers.py:488`) then yields KILLERS_UNKNOWN. Three guards make this safe:

- An active unit can never read QUIET here: active + incomplete scope forces UNKNOWN. The flip is
  ACTED→UNKNOWN, never ACTED→QUIET.
- Non-active units are untouched: `scoped` is empty for them (only the active branch scopes,
  `:266`), every timestamped line stays in `earlier`, and a non-zero earlier count is positive
  evidence for them (`:465-469`). No input turns real evidence into QUIET for a stopped or removed
  killer (A2-06, A2-09). Verified: inv3 (inactive, stamped-send variant) and the frozen not-found
  cases still ACTED.
- The demotion never removes a current-invocation send under chronologically ordered input (the
  contract's live collection is `journalctl -o json`, round-26 contract.md:87-88): sends at or
  after the last version line stay in `scoped`. Error directions are evidence-preserving
  (over-inclusion), never evidence-dropping.

So: yes, real evidence moves from `actions.sigterm` to `earlier_invocation_send_lines` and the
verdict can drop from ACTED to UNKNOWN for an active unit — and that is the outcome A2-05/A2-06
jointly decide, with the evidence still reported in the output field (`:513`).

## F3 (low, residual): the split point is a positional heuristic

`last_version` is the last version-line array index among stamped records (`:297-301`), not a
timestamp comparison. Two caveats, both outside the live input shape or evidence-preserving: an
out-of-order journal array (not producible by the contract's live collection) could demote a
current-invocation send; a stamp-less version line is invisible to the split, so its invocation's
stamped tail can be over-included into the current scope. Neither can drop a send from all buckets.

## F4 (low, disclosure): non-send lines before the last version line are counted nowhere

In an unbounded scope, `kill failed:` / `low memory!` / `killing whole process group` /
Suppressed lines before the last version line are in no bucket (the earlier handler counts only
send/escalation lines). These are report-only counts, not verdict inputs (`acted` at `:465-469`
carries sigterm/sigkill/escalations/oomd only), and the bounded scope has the same convention for
pre-AETM lines. No rule pins them for the unbounded shape; noting as a silent-shrink disclosure.

## F5 (info): invented-input differential, base vs landed (all run via `--inputs`)

| Input (shape) | base 7118f320 | landed cdfcf66d | Text says |
|---|---|---|---|
| inv1 active, AETM=0, send before last version | ACTED/1, sigterm 1 | UNKNOWN/2, earlier 1 | landed (F2) |
| inv2 active, AETM=0, dryrun seg then real seg | UNKNOWN/2, dryrun_lines 2 | ACTED/1, sigterm 1 | landed — base violated A2-07 (one dryrun invocation zeroed a later real send) |
| inv3 inactive, lone stamp-less send | ACTED/1, earlier 1 | QUIET/0, earlier 0 | landed — A2-10 leaves the record uncounted |
| inv4 active, AETM=0, stamp-less SIGKILL + stamped SIGTERM | ACTED/1, sigkill 1, sigterm 1 | ACTED/1, sigkill 0, sigterm 1, scope incomplete | landed — stamp-less record uncounted, evidence elsewhere stands |
| inv5 not-found, real send then dryrun in one segment | QUIET/0 | QUIET/0 (unchanged) | whole-segment dryrun granularity matches A6's per-invocation reading; not a landed regression |
| inv6 active, AETM=0, real seg then dryrun seg | UNKNOWN/2, dryrun_lines 2 | UNKNOWN/2, dryrun_lines 1, earlier 1 | landed reports the real send as earlier instead of silently zeroing it |

Inputs are invented (process names fictional-*, invented pids, no host values); files under
`/fast/scratch/hyaku/mori-r29/residual/ReviewLandedFix/inv*.json`.

## Residual risk and verification gaps

- `blind_violations=20` printed by the counter at the landed tip (and the pre-freeze receipt
  `.ufo/waves/round-29/evidence/blind-check-prefreeze.txt` records 20): R3
  (`.ufo/waves/round-29/contract.md:166-167`) binds the freeze-commit run and makes a non-zero
  count a C2 miss. Outside my assigned rules; flagged for the judge/L1, not adjudicated here.
- My F1 classifications are recommendations for the non-author judge seat, not rulings; the
  protocol requires that seat to read only rule text, case, and tool output.
- No LSP server check (device unavailable in this seat's toolset); no live-mode run (forbidden by
  bounds); the live-mode readability probe is out of scope per round-27 contract.md:60.
- inv5's whole-segment dryrun granularity means a send printed before a dryrun marker in the same
  invocation is reclassified as dry-run; both revisions behave identically and the A6 text
  ("when the invocation logged dryrun mode enabled") supports it, but a stricter position-reading
  would differ. Not exercised by any frozen case.
