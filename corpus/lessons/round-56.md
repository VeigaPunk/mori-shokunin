# Round 56 lesson (L1 MoriR56)

Entering tip `5b295eeebd87ebd610d8d39bfe2035742f740cfa`; round-55 closure
rejected-honest-stop (both claims unmet on recorded causes). Freeze tip
`3f494b49cde612d929e82887a48e1660c022c359`; data commits `c419fe6d`, `6ced9da9`;
receipts `8be2717b`; dispatch spec `7eab9188`, validated dispatch `acc62f54`.
Claims: C1 coverage (FR5 driver-liveness probe), C2 operability (dual-shape
vote binder). One v2 wave `w1` (64 seats). Receipts and seat outcomes under
`.ufo/waves/round-56/`.

## Gate

### New source rows (S544, S545)

Both rows were opened 2026-10-27 from their pinned locations; the quotes are
located in the committed copies and the registry anchor cells carry the
sha256 pins.

| id | URL | accessed | ≤25-word located quote | decision |
|---|---|---|---|---|
| S544 | shokunin driver launch-log grammar — fleet repo scripts/hyaku/inline.sh + scripts/shokunin-watchdog.sh — extract `corpus/evidence/sources-r56/watchdog-log-grammar.txt` | 2026-10-27 | `log "launch $lane round=$n pgid=$$ driver=hyaku-inline attempt=$a"` (inline.sh:149, in the extract) | admit, tier A (own-work: the grammar authority for the log the probe reads) |
| S545 | https://www.rfc-editor.org/rfc/rfc8259.txt — copy `corpus/evidence/sources-r56/rfc8259.txt` | 2026-10-27 | `A JSON text is a serialized value.` (line 251) | admit, tier A |
| S545 | https://www.rfc-editor.org/rfc/rfc8259.txt — copy `corpus/evidence/sources-r56/rfc8259.txt` | 2026-10-27 | `string = quotation-mark *char quotation-mark` (line 461) | admit, tier A |

Rejected rows this round: none (two sources, both admitted). The 404-class
btrfs ABI path rejected in round 55 stays rejected; no new reject candidate
was opened.

### Reused source rows and row changes

No old row changed. S544/S545 are new; used-by names
`corpus/knowledge/driver-liveness-r56.md` (S544),
`corpus/knowledge/vote-binding-r56.md` + both tools (S545).

## Mistakes

| class | evidence pointer | captured-by | fix / shown able to fail |
|---|---|---|---|
| number-drift (retyped summary) | `corpus/lessons/round-55-verifier-spotcheck.md` routed defect 1 — report said "Registry 298→298 rows" while committed bytes went 298→316 | QUALITY 152 (census receipts are captured bytes) — the counting command was not pasted | this round's Sources & frontier section pastes the counting command and its output for the before→after row count; the round-start capture is `evidence/census-start.txt` (exit 0) and row counts come from `grep -cE '^\\|[[:space:]]*S[0-9]{3,}'` / the census validator, not retyping. Shown able to fail: the r55 spot-check diffed the saved bytes and found the drift. |
| attribution (receipt revision) | routed defect 2 — the r55 report's before→after said "After at d27d943a" while the receipt was stamped a27ec482 | receipt-stage check (QUALITY 148 family) | this round's After cells cite the receipt's own stamped `rev=` field; the counters stamp the measured full revision in their verdict line. Shown able to fail: `evidence/c1-at-freeze.txt`/`c2-at-freeze.txt` carry `rev=3f494b49…` and the controls' do-nothing lines carry the entering tip. |

## Census

Start command `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate
--root /home/vgpnk/Projects/shokunin mori` captured to
`.ufo/waves/round-56/evidence/census-start.txt` (`exit=0`, 316 rows, 23 W04).
End receipt is captured mechanically after the last registry edit.

## Assimilation and quarantine

Assimilation: none (no `merge/mori/` package entry adopted this round; the
claims rest on S544/S545 opened this round). considerthese proposals checked.
Quarantine slice re-derived and adjudicated by wave seats; verdicts land in
the wave evidence and the report.

## Wave w1 findings and resolutions (settled 2026-10-27, 64/64 seats, no dead seats)

Adjudication seats and their dispositions: the wave verified both counters
(met at the freeze tip, do-nothing unmet at the entering tip), reproduced the
tally and the `voted=0` contrast independently, confirmed no regression of
the drift pin / census / silence oracle (byte-identical verdicts at both
tips), and confirmed the wave shape. Findings landed as fixes this round:

- Entry corrections (data-side): the "all fifteen … `vote_lines` arrays"
  overstatement fixed (the JSON keys vary: `vote_lines` 2/15, `votes` 9,
  `final_vote_lines` 3, `final_votes`/`voteLines` 1 each — the binder walks
  every string scalar, which is why the key does not matter); the S545
  section labels corrected via new row S546 (§2/§3/§7; lines and quotes were
  always true substrings); the S544 anchor completed via new row S547
  (launch-fail :241-249 and wrap :398 lines plus the fleet revision);
  the contrast-rationale overstatement fixed (0→68 quorum rows via the
  dual-shape reading under the r55 ≥2 rule; the 10 single-voted rows are the
  dispatch-coverage gap, and `dissent=0` is inter-voter only); the FR5
  novelty claim softened (the census silence surface read launch epochs
  since round 2; the probe's new surface is the strict per-event pairing).
- QUALITY 153 landed from the considerthese seat (carry-over-flag ledger,
  `considerthese/2026-10-26.md` suggestion 2, grounded in
  `.ufo/waves/round-49/flagged-fixed/count-flagged.py`'s one-round limitation).

Named limits routed to round 57 (no counter or tool change this round — both
frozen): counter arms are byte-pin + self-report (the pin is the sole
load-bearing fence: CritC1CounterFences constructions 1–3 all killed by
`failed=pins`; RevC1Counter/RevC2Counter sitecheck/PATH injection classes);
`count-c2.py` arms cannot behaviorally distinguish a loose substring binder
from the anchored one on committed bytes (behavioral fixture needed); probe
selftest survivors (dead-rest grammar rejection, malformed-examples
emptiable, `log.lines` unasserted — MutDriver1 8 killed/3 survived; binder
dissent-metric survivor — MutBinder); SecTools F-1..F-11 hardening (int()
digit-limit crash on huge tokens, RecursionError on deep JSON, no max-bytes,
O(n²) open_launches, O_NOFOLLOW, unconfined paths, silent ledger drops,
dead `--min`, /tmp tempfile fallback, NaN tokens); `unclosed` ghost backlog
and `in_flight` naming (124 opens fleet-wide, ~123 ghosts; mori 9/10);
`lane-round-failed` (35 lines) unattributed — historical driver outside the
repo grammar; receipt craft (freeze-sha256 `@rev` suffix breaks `sha256sum
-c`, absolute paths hash the worktree, header commit naming, controls
verdict truncation); kasegi citation-survival records `.ufo/watchdog.log`
GONE under a case-spelled path (sibling instrument note); quarantine register
data-quality (a `fetch-failed` row hides an `exact` match — reported, not
absorbed; mori runs no campaign tools).

Self-caught mistake (this round, found by ExecCensus/ExecRowsCensus/
CritFrontier): `evidence/census-start.txt` was captured without the
row-counting command, and the round's contract/lesson/LOG retyped "316 rows"
— the exact QUALITY-152 class the round mined as the r55 fix, recurring in
the round that claimed the fix. The frozen contract keeps the parenthetical;
the correction is: the counting command `grep -cE '^\|[[:space:]]*S[0-9]{3,}'`
and both counts (316 at entering `5b295eee`, 320 at landing) are captured
bytes in `evidence/census-end.txt`; round-57 start receipts must carry the
counting command from the start.
