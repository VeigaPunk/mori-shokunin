# Mo57Reviewer17 — mori round 57 w1: C2 source-grounding (one quote, independently located and tested)

Seat: Mo57Reviewer17 (leaf reviewer, lane mori-shokunin, wave w1). Date: 2026-10-27.
Scope per seat spec: read the frozen contract first; independently locate ONE exact
quote in the committed source report and test the knowledge claim it supports.
Findings only — no production edits, no commits, no predicate/counter/claim changes.
Fixtures lived only under `/fast/scratch/hyaku/mori-r57/Mo57Reviewer17/` (removed
after reporting; TMPDIR pointed there during runs). Disk guard checked before work
(27% used, no ENOSPC). No tool installs (none needed).

## Ground state (verified commands)

- Lane HEAD: `618562c72a03dc4d17386b715357f863fd327274` (freeze commit
  `round-57: freeze calibration and depth claims`); entering rev `53e2b476` is its
  parent. `git rev-parse HEAD`, `git log --oneline -3`.
- C2 artifacts are absent at tip, as the freeze ordering implies:
  `git show HEAD:corpus/knowledge/watchdog-unclosed-r57.md` → "path does not exist
  in 'HEAD'"; `git show HEAD:corpus/SOURCES.md | grep S548` → no match;
  `python3 .ufo/waves/round-57/count-c2.py HEAD` → `C2=unmet claims=0 source=bad`
  exit 1 — identical to the frozen entering state in controls.txt. This seat
  therefore grounds against the committed round-56 source report, the document the
  entry's newly opened S548 row will quote from.
- Tool identity: `sha256sum tools/mori-driver-liveness.py` →
  `6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997` — equals the
  frozen PIN recorded by round 56 (`count-c1.py:46`).
  `python3 tools/mori-driver-liveness.py --selftest` →
  `DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0`, exit 0.
- All cited sources are committed and byte-identical to HEAD:
  `git diff --quiet HEAD -- tools/mori-driver-liveness.py
  .ufo/waves/round-56/w1/Mo56CritDriverSemantics.md
  .ufo/waves/round-56/evidence/driver-liveness-live.txt` → clean; and
  `git ls-files --error-unmatch` lists all three.

## The quote (located)

Source report: `.ufo/waves/round-56/w1/Mo56CritDriverSemantics.md:168-170`
(committed; working tree == HEAD). Exact text:

> one number a consumer will read first (`unclosed`, "launches with no
> same-(lane,round,attempt) complete") is ~99% historical residue on the real
> log. The docstring (`:34-36`) and notes (`:239`) do disclaim it as a pairing
> count, so the frozen predicate is not violated

Byte-uniqueness: `grep -cF 'same-(lane,round,attempt) complete") is ~99%
historical residue on the real'` → 1 (one match in the file). Companion committed
quote, same semantics, from the round-56 live evidence report:
`.ufo/waves/round-56/evidence/driver-liveness-live.txt:290` —
`  "in_flight/unclosed are log-shape facts, not health verdicts",` (grep -cF → 1).

Knowledge claim the quote supports (contract C2 wording): **`unclosed` is a
pairing count rather than a present-running count.**

## Testing the claim

Code anchors, `tools/mori-driver-liveness.py` (frozen PIN above):

- `:133` every `launch` appends its key `(round, attempt|None)` to
  `row["open_launches"]` — unconditional, with multiplicity (plain list append).
- `:116-121` `close_round()` removes at most ONE matching open: the exact key, or
  the `(round, None)` fallback; called from `complete` (`:143`) and `wrap` (`:150`).
- `:157` `lane-dead-no-report` clears every open of that round;
  `:158-163` `launch-fail` closes nothing.
- `:172-173` `in_flight` and `unclosed` are computed from different facts:
  `"in_flight": row["last_event"] == "launch"` vs `"unclosed": len(row["open_launches"])`.

So `unclosed` = number of launch events left open under the probe's own
(lane, round, attempt-compatible) close grammar — a pairing count by construction,
and structurally independent of the present-running-ish flag `in_flight`.

Falsification attempts (scratch fixtures, run
`python3 tools/mori-driver-liveness.py --fixture <dir> --now 1793200000`, exit 0,
`malformed=0` each; full JSON inspected):

1. **fx1 — open pairing while "not running":** launch r1, launch r2, complete r1 →
   `mori: launches=2 completes=1 in_flight=false unclosed=1 rounds_seen=2`.
   Round 2's launch genuinely never closed (open work exists), yet `in_flight`
   says false (last event is a complete). `unclosed=1` tracks the unpaired
   launch, not any running state — and conversely `in_flight` misses it. The two
   fields are independent facts, as the claim requires.
2. **fx2 — multiplicity, not process count:** launch r1 attempt=1 twice
   (pgid 111 then 222), one complete attempt=1 →
   `mori: launches=2 completes=1 in_flight=false unclosed=1`. At most one of the
   two sequential pgids could ever be alive, and the honest running count is 0
   (last event: complete); `unclosed=1` counts the leftover open launch EVENT.
   A present-running reading is false here; the pairing reading (2 opened − 1
   closed = 1 open) is exact.
3. **fx3 — parked lane, permanent residue:** launch r1 attempt=1, then
   `wrap mori round=1 landed; NOT respawning (fleet-wrap)` →
   `mori: launches=1 wraps=1 in_flight=false unclosed=1`. The fleet explicitly
   stopped respawning — nothing can be running — yet `unclosed=1` persists
   forever: the wrap's `close_round` tries `(1,None)`/`(1,None)` against the
   attempt-keyed `(1,1)` open (`:116-121`, `:150`) and matches nothing. This is
   the sharpest counterexample to the present-running reading, and it also fixes
   the claim's precise limit: the "pairing" is relative to the probe's close
   grammar, which can strand semantically-closed launches as ghosts.

Committed real-log corroboration (round-56 evidence report, no live run needed):

- `.ufo/waves/round-56/evidence/driver-liveness-live.txt:271-286` — lane
  `tsukuroi`: `launches=47 deads=8 wraps=0 in_flight=false unclosed=5`: a lane
  whose last event is a dead carries five pairing ghosts while reporting
  not-in-flight. `:2-14` — lane `aggregator`: `launches=9 completes=7 wraps=2
  unclosed=2 in_flight=true`: nine closes against nine opens yet `unclosed=2`,
  i.e. close attempts that did not pair under the keying — again log-shape, not
  process state.
- The quoted source report's own census (≥123 of 124 fleet-wide opens historical)
  is consistent with these two committed lanes.

Directional check found while testing: `in_flight=true` ⇒ `unclosed ≥ 1` (a
launch is always appended before `last_event` is set, and nothing after it could
have closed it without changing `last_event`) — but `unclosed ≥ 1` ⇏
`in_flight=true` (fx1, fx2, fx3, tsukuroi). The one-directional implication is
exactly what distinguishes a pairing count from a running count; a present-running
field would saturate in both directions.

## Verdict

**Claim CONFIRMED with one precision limit.** The quote at
`Mo56CritDriverSemantics.md:168-170` accurately supports the contract's C2 core
statement: `unclosed` is a pairing count (open launch events under the probe's
(lane, round, attempt-compatible) grammar), not a present-running count — verified
against the frozen tool's code, three constructed counterexamples, and the
committed round-56 evidence. Limit to carry into the entry's wording: the pairing
is *grammar-relative* — `wrap`/`launch-fail` do not close attempt-keyed opens
(fx3), so `unclosed` legitimately retains ghosts the grammar itself created; an
entry that rounds this to "unmatched work" or "still running" would overstate.
The quote's second sentence already disclaims exactly this ("do disclaim it as a
pairing count"), so the quote is not misrepresented by the claim.

## Findings by severity

- **None (no defect in scope).** The tested claim holds; the quoted source is
  committed, byte-unique, and faithfully characterized.
- **INFO — counter does not machine-locate quotes.**
  `.ufo/waves/round-57/count-c2.py` `quote_ok` tests only that each `| K` claim
  line contains backticks; it never verifies a quoted string exists in the source
  copy. Located-ness rests on wave discipline (this seat's independent grounding
  is one instance of it). Not a predicate change — noted as residual risk only.
- **INFO — final entry untestable at tip.** The entry and S548 row do not exist
  at `618562c7` (freeze precedes wave data by design); when the entry lands, its
  S548 pointer should resolve to a copy of the round-56 source report cited above
  for my located quote to transfer directly.

## Residual risk / verification gaps

- I tested one quote/one claim as assigned, not all eight entry claims; sibling
  facets cover the rest.
- If the entry's S548 copy is cut from a different committed document than
  `Mo56CritDriverSemantics.md` (e.g. only the evidence JSON), my located quote
  still stands on its own file:lines, but the entry's located-quote lines would
  need their own verification against that copy.

No fleet/sibling/lane files were modified; nothing committed; scratch
`/fast/scratch/hyaku/mori-r57/Mo57Reviewer17/` removed before yielding.
