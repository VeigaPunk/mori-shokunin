# Mo51CritEntailArm — attack on the design of P-C2's entailment arm

Seat: Mo51CritEntailArm (mori round 51, wave w1; critic item — attacks the **design** of the
entailment arm, not the counter's code). No ENTAIL lines are written here (not an ENTAILMENT item).
Scratch: `/fast/scratch/hyaku/mori-r51/Mo51CritEntailArm/` (created, used, removed before finish).
No tools were installed or updated.

## What I read / ran (all read-only)

- `…/round-51/contract.md` (P-C2 at lines 74–100; round shape at 129–133; controls at 90–97).
- `/home/vgpnk/Projects/shokunin/LEARNING.md` (discernment gate: "A subagent the lane dispatched is
  still the lane", line 45; outside non-author spot-check, lines 42–48).
- `…/round-51/count-c2.py` (docstring 2–27; `entail_votes` 120–130; `evaluate` 140–248; readers
  251–264; selftest 301–471).
- `…/round-51/evidence/c2-at-data.txt`, `c2-hashes-at-data.txt`; `…/w1/*.md` (current seats);
  `…/w1/swarm-registry.json`; `…/w1-dispatch.json` (68 seats; agent labels = roles; 11 seats carry
  the word ENTAILMENT in their prompt).
- Lane git state at HEAD `b504cb17`: `.ufo/waves/round-51/w1/` is **untracked** (`??`);
  `git ls-files` shows zero tracked files there; no `w1-results.json` exists yet (mid-wave).
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/inline-dispatcher.py` (`finalize` 286–295; `register`
  229–275; `seat_output` 277–284).
- `python3 …/count-c2.py --selftest` → `C2_SELFTEST pass=34 fail=0`, exit=0 (frozen counter behaves
  as documented).

## Findings

### F1 — HIGH — A vote is a bare token; the counter verifies format, not judgment, reason, or entitlement
`entail_votes` (`count-c2.py:117-130`) accepts any line matching `^\s*ENTAIL [0-9a-f]{12}
(entailed|overclaim)\b` in any `.md` file under `w1/` whose name does not start with `MoriR51`; the
report body (locators, reasoning) is ignored. `evaluate` (`:218-226`) needs only one such line per row
hash, and the selftest (34 cases) never requires a vote to carry reasoning or a locator.
Counterexample: a report whose entire body is a single `ENTAIL <h> entailed` line passes the arm for
that row — indistinguishable from a genuine review. Entitlement is never consulted: the 11
ENTAILMENT-item seats are machine-derivable from `w1-dispatch.json`, but any non-L1 `.md` file in
`w1/` (e.g. a helper `README.md`, or a non-entailment executor's report) would count as a voter.

### F2 — HIGH — Nothing binds the scored bytes to what seats wrote; the L1 can edit reports invisibly
The counter reads the **committed tree at R** (`git show R:<path>`, `:251-264`). Reports are written
to the untracked working tree and the L1 integrates and commits them. There is today **no
pre-integration byte snapshot**: the harness's `finalize()` (`inline-dispatcher.py:286-295`) records
only each seat's terminal output (`str(h.output())[:20000]`), not the report file bytes. So an L1
edit before landing is undetectable: appending `ENTAIL <h> entailed` lines to any eligible seat file,
or deleting an `overclaim` line, sails through the counter. Concrete exploit against the current
draft: deleting `ENTAIL 5d06a2ae70cf overclaim` (`w1/Mo51CritEntail01.md:52`) clears row 6 without
replacing the claim text, and C2 would pass as-is. "Votes are never deleted" (contract.md:97) is
instruction-level, not machine-checked.

### F3 — HIGH — "Two seats of different roles" is prose, not P-C2; one voter can clear every row
P-C2 requires only `>= 1` `ENTAIL <h> entailed` line per row (contract.md:79-82; `evaluate`
`:221-226`); the two-seat/different-role requirement appears only in the round shape
(contract.md:131-132) and is unscored. `entail_votes` records `(verdict, filename)` but `evaluate`
never counts distinct voters, filenames, or roles; roles exist only as dispatch `agent` labels.
Current draft state already illustrates it: rows 1–18 each carry exactly one vote today (file scan of
`w1/`), which would satisfy the counter. A single seat could vote all 21 rows entailed and C2 would
read `entailed=21 dissent=0`.

### F4 — MED — Two agreeing votes are correlated samples: one model, same sources, same lane
All seats run under the same omp session on the same model (workstation: `inception/mercury-3`); the
dispatch `agent` labels select no distinct model, and all seats read the same committed copies. A
second agreeing vote therefore buys: (a) rejection of single-seat stochastic/careless errors, (b) a
dissent channel (one `overclaim` blocks the row — visible conflict), (c) quorum against a lone rubber
stamp — but not independence, and not outside verification: LEARNING.md is explicit that a dispatched
subagent is still the lane, so this arm is self-attestation (the contract's own named limit already
says "committed reviewer step, not outside verification"). The limit should name the correlation.

### F5 — LOW — Votes on hashes absent from the table pass silently
`w1/Mo51CritEntail01.md:53` carries `ENTAIL 0a908e8eb4f3 entailed` — the hash of a **proposed
replacement claim**, not of any row cell. The counter ignores it (only table-row hashes are looked
up), so no harm here; but it shows the channel is opaque: a typo'd hash silently fails its row, and
a stray vote line is never cross-checked against the table.

### F6 — LOW — w1-results.json as it exists will not anchor file bytes
`w1-results.json` is written by `finalize()` at WAVE-DONE, before L1 integration, and will hold
`{name, agent, output}` where output is the terminal message (≤ 20 kB), not the report file. So a
naïve "compare committed reports to w1-results.json" cannot detect edits today; but it is the right
place to hold per-report digests (below). [Content of the not-yet-written file is inferred from the
generator code — `inline-dispatcher.py:286-295`.]

## Answers to the posed questions

1. **Is a wave-seat vote a meaningful entailment check?** Only as *process* evidence: it proves some
   non-L1 seat recorded a judgment for that exact text (and that no seat recorded dissent), so it
   catches unreviewed rows, wording drift and contested claims. It is not *truth* evidence: seats are
   the lane (LEARNING.md:45), so it is a committed inner-review step, not the outside spot-check
   LEARNING.md requires for discernment.
2. **What stops the L1 from editing a seat's report?** Today, nothing mechanical. The counter scores
   the L1's integration commit; there is no baseline digest; "votes are never deleted" is an
   instruction. (F2.)
3. **Could closure compare against `w1-results.json`?** Only if that file is extended to carry the
   report bytes' digests captured at settle time by the harness; as generated today it carries the
   terminal output message, not the file. (F6.)
4. **Two votes vs one; shared model?** Two votes buy dissent detection, noise reduction and quorum,
   not independence: both voters share a model family, the same sources and the same lane, so
   systematic misreading passes both. The two-vote rule is also unenforced by P-C2 (F3).

## Proposed named-limit wording (add to C2 limits)

> An entailment vote is a recorded judgment line, not proof: all voters are lane-dispatched subagents
> (LEARNING.md) on a shared model, and P-C2 counts any non-L1 wave-report line, so the arm certifies
> that some wave report contains the verdict line for that exact hash — not that the reasoning is
> sound, that the voter was entitled to vote, or that reports survived integration unedited. P-C2
> requires only one such line per row and does not distinguish voters by role or entitlement.

## Proposed closure check (makes the arm auditable; lives outside the frozen counter)

1. **Snapshot at settle (harness)**: `finalize()` additionally computes `sha256` of each seat's
   report file in `w1/`, stores it as `report_sha256` per seat in `w1-results.json`, and retains a
   copy of that manifest **outside the lane repo** (orchestrator-side), so the integrator cannot
   rewrite it.
2. **Verify at landing**: a closure verifier (script, run by the operator/harness after the L1
   lands at R) asserts, for every seat:
   - **byte-equality**: `sha256(git show R:<report-path>)` == manifest digest (committed verbatim);
   - **entitlement**: filenames contributing votes ⊆ the 11 ENTAILMENT-item seats (derived from
     `w1-dispatch.json`);
   - **quorum + roles**: every row hash has ≥ 2 contributors with distinct role labels (from the
     dispatch roster) — turning the prose guarantee into a checked invariant;
   - **no-deletion**: the vote-line set at settle is a subset of the vote lines at R (mechanizes
     "votes are never deleted");
   - **locators (optional strengthening)**: each ENTAIL line must be accompanied, in its report, by
     a quote locator (source file + line range), so a spot-checker can re-derive entailed judgments
     from the committed copies; bare lines are rejected.

## Findings

- HIGH — `count-c2.py:117-130,218-226`: votes are format-only tokens; judgment, reasoning and
  entitlement are unverified; any non-L1 `.md` in `w1/` counts as a voter.
- HIGH — `count-c2.py:251-264` + workflow: scored bytes are the L1's integration commit; no
  pre-integration snapshot exists, so L1 edits (append `entailed`, delete `overclaim`) are
  undetectable; concrete: deleting `w1/Mo51CritEntail01.md:52` clears row 6 without claim
  replacement.
- HIGH — contract.md:79-82 vs 131-132: P-C2 enforces ≥ 1 vote per row with no distinct-voter or role
  check; one seat can clear all rows; today rows 1–18 each have exactly one vote.
- MED — workstation model `inception/mercury-3` + LEARNING.md:45: two votes are correlated samples
  (shared model, shared sources, same lane); they buy dissent detection/noise reduction/quorum, not
  independence or outside verification.
- LOW — `w1/Mo51CritEntail01.md:53`: vote line for a non-table hash (replacement claim) passes
  silently; no cross-check that votes refer to live rows.
- LOW — `inline-dispatcher.py:286-295`: `w1-results.json` records terminal output, not file bytes;
  it cannot anchor report immutability until it carries settle-time report digests.
