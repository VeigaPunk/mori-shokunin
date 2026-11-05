# Mo99CritC2 — C2 falsification attempt (mori r99, wave w1)

Seat: critic, lane mori. Scope: attack claim C2 only; detection/report, no remediation. Instruments used are the
frozen bytes: `count-c2.py` sha256 `b9b58acae05f0d889705572f46540a67c321b445f1814538c7796e8a0703f911` = controls
receipt prefix `b9b58acae05f0d88` (`evidence/controls-r99.txt` line 1); the registered gate's sha in the fixture
matched `GATE_SHA 662fafde7ba446e1…` exactly. All runs read-only git; no lane/fleet mutation; no sysctls; no sudo;
scratch removed at end.

## (a) Do-nothing control — predicate NOT do-nothing-meetable

Re-scored entering myself with the frozen counter:
```
$ python3 .ufo/waves/round-99/count-c2.py 73308ff6e5c933f53498e9501ef95917b0ef7171
axis coverage expect=round_98 pointer=missing
axis operability expect=round_97 pointer=missing
axis depth expect=round_86 pointer=missing
axis freshness expect=round_97 pointer=missing
axis calibration expect=round_98 pointer=missing
axis adjacency expect=round_19 pointer=ok
C2=unmet mismatches=5 cells_unchanged=yes gate=rc1 mismatched_axes=coverage,operability,depth,freshness,calibration rev=73308ff6e5c9
exit=1
```
Five pointer mismatches AND the registered gate prints rc1 at entering (`gate=rc1`) — a do-nothing fails twice.
This is the exact defect class that killed r95 C2 (QUALITY 208, do-nothing reached the predicate); r99 C2 does not
repeat it. Attack (a) fails to falsify.

## (b) Pointer-token position — counter-level weakness confirmed; landing unaffected

Counter code scans the whole Evidence cell (`re.findall(re.escape(path)+r":(\d+)", ev)` over the full cell) and
switches to `ok` if ANY hit's line names axis+verdict, so (i) the token may sit anywhere in the cell and (ii) a
stale superseded sibling pointer is tolerated. Forge C (below) demonstrates both: `C2=met` with the round-98 token
buried mid-sentence after `round-80-verifier-spotcheck.md:3, since superseded`. The frozen predicate says the cell
"carries a located pointer"; the counter implements "contains one anywhere" — a letter-vs-implementation
divergence of the counter, real against future forgeries.

Given the landed text it is not exploitable: `git diff 73308ff6..5013f0be -- SCORECARD.md` shows each of the five
rewritten Evidence cells LEADS with the located pointer as its first clause, and I verified the cited lines carry
genuine axis-verdict rows (harm-check tables: round-98 file contains `| coverage | improved | C1 above |` and
`| calibration | improved | C2 above |` at :89/:90; round-97 `| operability | improved | C1 above |` /
`| freshness | improved | C2 above |` at :78/:79; round-86 the `| depth | **improved** | …` row at :145). Attack
(b) finds a counter weakness, not a landing defect.

## (c) MANIFEST pin at 4ad377ea — point-in-time by convention, not a defect

Expectations re-derived independently from the pinned fleet blob match the claim exactly:
coverage (98, rounds[1389]), operability (97, rounds[1384]), depth (86, rounds[1205]), freshness (97, rounds[1384]),
calibration (98, rounds[1389]), adjacency (19, rounds[398]) — all `improved`. When the r99 closure itself lands in
the fleet MANIFEST and grades axes, `expectations()` advances and round-98/97 pointers become stale — but the
frozen counter hard-pins `FLEET_PIN=4ad377ea…`, so it keeps measuring freeze-time state forever. Re-pointing each
round is the lane's standing convention (r50 and r79 corrections exist precisely because "latest admitted" moves
every admitted round), and the landed cells carry their own provenance (`(round 98, MANIFEST rounds[1389])`).
Staleness after landing is expected re-work, not a claim defect.

## (d) Calibration move or bookkeeping — calibration, by the lane's own doctrine and precedent

Pro (calibration): AXES.md:15 defines the calibration signal as "SHONEN.md/SCORECARD entries match observed repo
state"; the contract's §9 form is "a calibration claim counts mismatches between self-assessment and record" — the
predicate is literally a mismatch count (5 → 0, receipted both ways). The r98 D3 finding was five cells asserting
a false "latest admitted closure" against the record; fixing them reconciles self-assessment with record. The r79
correction paragraph (SCORECARD.md:31-43) names its own limit — "this predicate grades the `Last change` clause
only, not the `Evidence` cell" — and r99 C2 closes exactly that named limit, with a strictly stronger instrument
(located, content-validated pointers). r50 and r79, the two same-class corrections recorded in SCORECARD.md
(:21-29, :31-43), were both graded calibration while leaving every score unchanged — precedent says score movement
is not what makes it calibration.
Con (bookkeeping): no score moved, no new instrument, prose re-pointing; r95's C2 shows the thin-claim trap. But
here the do-nothing fails twice (5 pointers + gate rc1), the pointers are content-validated (Forges A/B), and the
gate must independently print `C1=met`. The bookkeeping reading fails on the doctrine's own signal sentence, the
§9 form, and precedent. Resolved: calibration.

## (e) Forged SCORECARDs — fixture runs

Fixture per the rules: `git init` in scratch, toplevel asserted, `git -C <lane> archive 5013f0be | tar -x`,
committed (`base cfa4c61d69ab`), read-only alternates to the lane object store so the counter's hardcoded
`ENTERING 73308ff6:SCORECARD.md` resolves. Harness validated: unmodified base scores `C2=met mismatches=0
cells_unchanged=yes gate=ok` — identical to landing. Gate bytes sha256 = `GATE_SHA` prefix `662fafde7ba446e1`.

| Forge | Mutation | Result |
|---|---|---|
| A (should fail) | coverage lead `:89`→`:1` (valid file, wrong line) | `coverage pointer=bad-line … C2=unmet mismatches=1 cells_unchanged=yes gate=ok … exit=1` (bc6e6da05c23) |
| B (should fail) | coverage lead pointed at superseded `round-47…md:68` | `coverage pointer=missing … C2=unmet mismatches=1 … exit=1` (907fb09932cc) — r98-D3 class stays closed |
| C (predicted pass) | token buried mid-sentence + stale `round-80…md:3, since superseded` sibling | `all pointer=ok … C2=met mismatches=0 cells_unchanged=yes gate=ok … exit=0` (2c26d029de4c) — **passes: the (b) weakness, demonstrated** |
| D (predicted pass, was wrong) | Last-change head `round 98`→`round 7` | `mismatches=0 cells_unchanged=no gate=rc1 … C2=unmet … exit=1` (5643e44df125) |

Forge D is a positive surprise recorded honestly: I predicted the counter's `round \d+` clause regex would accept a
fabricated head; it does not — `last_ok` requires the intact entering cell as verbatim suffix (`cells_unchanged=no`)
and the registered gate independently rejects the fabricated head (`gate=rc1`). The counter is stronger than the
contract sentence "one prepended `round N (verdict, score held); ` clause" reads alone.

## Residual (new; report-only, no patch — instruments frozen)

The counter validates the cited line against the landing revision's OWN copy of the spot-check file; unlike the
gate (`GATE_SHA`), the cited `corpus/lessons/round-N-verifier-spotcheck.md` blobs are not pinned. A landing that
edited `round-98-verifier-spotcheck.md:89` to say "coverage improved" would pass `count-c2`. Mitigated today by
protocol (spot-check files are verifier-written, the landing diff is reviewed, and C2's causal separation scopes C2
to SCORECARD cells only — the landing's SCORECARD delta is exactly 5 insertions/5 deletions, numstat verified).
Smallest safe correction for a future freeze: pin the cited lesson blobs like `GATE_SHA`, anchor the pointer to the
cell's leading clause, and reject stale same-family pointers (Forge C class). Not applied here.

## Verdict

VERDICT C2 holds: do-nothing fails (5 pointer mismatches + gate rc1, reproduced); landing `C2=met mismatches=0
cells_unchanged=yes gate=ok` reproduced at the frozen counter bytes; three of four forgeries that should fail fail
(wrong line, superseded pointer, fabricated Last-change head) and the one counter leniency (token position, Forge C)
is not exploited by the landed text, whose five cells lead with genuine located pointers; the MANIFEST pin is
point-in-time convention; the move is calibration by AXES.md:15, §9's mismatch-counting form, and r50/r79 precedent.

Unrun: C1 attacks (other seats' scope); no forge with a doctored spot-check file was executed (residual argued
analytically above); no audit of `count-c2.py` beyond the code paths the attacks exercised.
