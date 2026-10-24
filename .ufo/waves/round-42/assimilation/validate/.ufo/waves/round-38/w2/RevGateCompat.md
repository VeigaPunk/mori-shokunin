# RevGateCompat — round 38 wave 2 (falsify): gate field-compat review

Seat: MoriR38.RevGateCompat (reviewer, leaf). Target: `tools/mori-sources-appendonly.py` output
compatibility across `e33bb561712b32f46861362a3fa43762fa70ae4f` (entering tip), `e37dcc6dffde8e74d5f0b89b002586390c65e6fa`
(before), and `f725f3076972e6e70595b5ac8279be524a111ff8` (scored tip), on all fields other than
`supersede_timing`. Every number below was re-derived by running the command; nothing is taken
from the receipts.

## Method

- `git show <rev>:tools/mori-sources-appendonly.py` for all three revs into
  `.ufo/waves/round-38/scratch/RevGateCompat/gate_{e33,e37,f72}.py`. Blob ids:
  e33 = e37 = `dfb5040b159f7a0b4afedc90a633d997352908f0` (sha256 `915527a7…`); f72 =
  `c2c86f4d3ca1c6f9b6d46462fb6481dab543b967` (sha256 `9a6164e3…`, matches the working-tree file;
  HEAD = f725f307).
- Commit order confirmed: `e37dcc6` is an ancestor of `e33bb56` is an ancestor of `f725f307`
  (`merge-base --is-ancestor`); the gate changed once, in `daa1d4d`.
- Ran each gate blob on each target: `python3 gate_<V>.py <target> --repo <lane> --round-base f10a320d`
  (raw outputs in `scratch/RevGateCompat/out_<V>_on_<T>.txt`), plus `--selftest` for each blob
  (`selftest_{e37,f72}.txt`).
- Claim command run verbatim on the working tree: `python3 tools/mori-sources-appendonly.py
  f725f307… --round-base f10a320d` → prints the P-C6 line, 18 `changed` lines, the summary,
  `supersede_timing superseded_as_of=[18 ids] stale_supersede=[]`, `EXIT=1` — byte-identical in
  content to `evidence/gate-after.txt`.

## Field-by-field diff table (old gate vs new gate, same target)

`ids`, `deleted`, `superseded`, `round_changed` are summary-line lists; `changed`/`deleted` rows
are the per-id lines. "same" = byte-identical sets and order.

| target | exit | per-id `changed` lines (18) | per-id `deleted` | `ids` | `deleted` | `superseded` | `round_changed` | added lines |
|---|---|---|---|---|---|---|---|---|
| e37dcc6 | 1 → 1 | identical | identical (none) | same (18) | same `[]` | same (18) | same `[S182,S193]` | `+P-C6` line, `+supersede_timing … stale_supersede=[S069]` |
| e33bb56 | 1 → 1 | identical | identical (none) | same (18) | same `[]` | same (18) | same `[S182,S193]` | same additions; output byte-identical to e37dcc6 (verified `diff`) |
| f725f307 | 1 → 1 | `S069: superseded_by S073 → S226`; other 17 identical | identical | same (18) | same `[]` | same (18) | same `[S182,S193]` | `+P-C6` line, `+supersede_timing … stale_supersede=[]` |

Changed pre-existing verdict at the compared revisions: exactly one — `changed S069
superseded_by=S073` → `superseded_by=S226` at f72. This is the contract's disclosed change
(`contract.md` P-C6: "the per-id `superseded_by=` names the latest superseder"). `S226`'s
`teaches` opens `supersedes S069` (verified: pair `(S069,S226)` present at tip).
No undisclosed verdict change at e37dcc6, e33bb56, or f725f307. `appendonly_violations=18`,
`ids`, `deleted`, `superseded`, `round_changed`, and the exit code are unchanged on all three.

## Selftest before/after

| gate | cases | result | delta |
|---|---|---|---|
| e37 blob (`--selftest`) | 8 | `MORI_SOURCES_APPENDONLY_SELFTEST pass=8 fail=0`, exit 0 | — |
| f72 blob (`--selftest`) | 9 | `pass=9 fail=0`, exit 0 | **+1** |

Case-level diff (`_selftest_cases`, e37.py:348-382 → f72.py:400-434): one new tuple
`("supersede before edit", [with_old_superseder, old_superseder_then_edit], 1, {…
stale_supersede: [S001]})` at f72.py:427-430; all 8 pre-existing cases kept, expectations only
*extended* with `superseded_as_of`/`stale_supersede` keys — no key weakened or removed, no
expected exit changed. The runner (f72.py:481-482, 506-517, 527-533) additionally asserts
exactly one `TIMING_RE` line, filters the new P-C6 line, and grammar-checks every remaining
line — both new arms are enforced, not cosmetic. The "supersede after edit" arm required by the
contract is the extended `superseding row` case (f72.py:423-426: expects
`superseded_as_of=[S001]`), which now exercises both arms.
Selftest receipts reproduced: `gate-selftest-before.txt` pass=8, `gate-selftest-after.txt` pass=9.

## Findings

**LOW-1 — contract says "`--selftest` gains two cases"; the code gains one case tuple (+1, 8→9).**
`contract.md` C3 text lists `supersede after edit` and `supersede before edit` as gained cases,
but only `supersede before edit` is a new tuple; `supersede after edit` semantics are folded
into the pre-existing `superseding row` case. Both required arms are covered and enforced
(`superseded_as_of=[S001]` and `stale_supersede=[S001]` both asserted and passing), so this is a
wording inaccuracy, not missing coverage. An acceptance test keyed on case *count* = 10 would
fail; the actual count is 9.

**LOW-2 — `superseded`/`superseded_by` semantics broadened beyond the disclosed "latest
superseder" naming.** Old: `superseders(tip_rows, colmap)`, first-declaring row wins
(e37.py:175-185, 243). New: scans *every* history state, pair with the max first-appearance
index wins (f72.py:242-253, 272-276). Side effects not covered by the contract wording:
- A superseder row deleted before tip still counts: demonstrated on a scratch sandbox
  (c0: S001 + S002`supersedes S001`; c1: S001 edited, S002 deleted) — old gate printed
  `superseded=[]`, `superseded_by=-`; new gate prints `superseded=[S001]`,
  `superseded_by=S002`, `stale_supersede=[S001]`. Field changed on that input class; exit code
  unchanged (`violations` counts ids+deleted only, f72.py:308).
- Two rows declaring the same target: old names the first in tip order; new names the latest
  landing — the disclosed lane effect (`S069: S073→S226`), but the class is broader than the
  naming disclosure implies.
On lane history this is provably unreachable today: all 33 `supersedes` declarations ever made
survive to the f72 tip (checked all 52 commits touching `corpus/SOURCES.md`; zero vanished
pairs), so tip-scan ≡ history-scan at every ancestor → `count-c1.py`'s tip-scan oracle
(count-c1.py:198-206, 249-250, 668-669) cannot diverge on `superseded` in its drawn-ancestor
arm, and `superseded_by` naming is grammar-checked only (`same_id_lines`, count-c1.py:561-593).
No C1 flake; latent if the registry ever retracts a declaration.

**INFO-1 — undocumented unconditional predicate line.** The new gate prints the full P-C6
predicate before the report on every verdict run (f72.py:580); the gate's own `Output` docstring
lists only `changed`/`deleted`/summary/`supersede_timing` lines. The new selftest filters it
(f72.py:481-482) and `count-c1` parses by anchored regexes, so no consumer on record breaks;
downstream line-positional consumers would.

## Residual risk / verification gaps

- `superseded_as_of` landing index is a pair's *first* appearance (`setdefault`, f72.py:252);
  a retracted-then-restored declaration would under-report the landing commit and could
  misclassify `stale`. Unreachable on the lane today (no vanished pairs); unverified elsewhere.
- `teaches_idx` uses the walk's single resolved `colmap` (f72.py:236, 244); a mid-history header
  reorder would mis-scan old states. Lane header is canonical at all 52 commits (verified), and
  the header-variant sandbox (teaches at index 7, consistent across history) produced identical
  old/new verdicts — so this matches pre-existing single-colmap behavior for `imm_idx`.
- Verified targets are the three named revisions + two synthetic sandboxes; "no changed verdict"
  is proven on that set, not on arbitrary histories (see LOW-2).
- `round_base` invariance: all runs used the claim's `f10a320d`; no other base was exercised.

## Verdict

**PASS.** Every changed pre-existing verdict at the compared revisions is disclosed (S069
`superseded_by` S073→S226, per contract P-C6); all other fields — `ids`, `deleted`, `superseded`,
`round_changed`, per-id lines, exit code — are identical across e37dcc6, e33bb56, f725f307.
The selftest is strictly additive: 8 → 9 cases, zero removed or weakened. Contract case-count
wording is off by one (LOW-1); the `superseded`/`superseded_by` semantics broadened on
non-lane-shaped histories (LOW-2).

## Tooling

No installs. Used: system `git`, `python3`, `diff` — lane read-only throughout; all scratch under
`.ufo/waves/round-38/scratch/RevGateCompat/` (gate blob copies `gate_{e33,e37,f72}.py`, outputs
`out_*`, `selftest_*`, sandboxes `rgc-sandbox-*`, `rgc-hdr-*`).
