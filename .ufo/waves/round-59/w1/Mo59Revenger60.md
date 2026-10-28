# Mo59Revenger60 — results.json writer contract and the settlement semantics actually observable

Round 59, wave w1, seat Mo59Revenger60 (revenger). Read-only reconstruction: no production
file, corpus row, SCORECARD, LOG, lane VCS or fleet/sibling repo was written; all mutants live
under `/fast/scratch/hyaku/mori-r59/Mo59Revenger60/mut/` (removed after this report was written).

Lane HEAD when measured: `8ff344ff18924c1ea63d46c3b3969f9fea05bc51`; freeze
`60b3a76ad0524c8978cc51922940be1c8c388915`; entering `2b9f03975bfb6e508f35074ac8181ec8bf54e805`
(all three `git rev-parse` verified present; the freeze commit is an ancestor of HEAD, and no
tracked file was modified — `git status --porcelain` lists only untracked paths, all of them
round-59 wave/artifact paths written by other seats, none by this one).

Frozen inputs read first: `.ufo/waves/round-59/contract.md`,
`.ufo/waves/round-59/count-c1.py`, `.ufo/waves/round-59/count-c2.py` (P-C2, ARTIFACTS,
REAL_SCAN/DRIFT_SCAN, scan/drift arms).

## 1. The writer contract, derived from the writer

The only producer of `*-results.json` is the fleet in-session driver
`/home/vgpnk/Projects/shokunin/scripts/hyaku/inline-dispatcher.py` (fleet, read-only here).
Its stated contract (`inline-dispatcher.py:53-55`) is: spawn every `taskCall.tasks[]` seat
inline, mark `<ready>.dispatched`, "and when no seat is live write
`<dispatch-dir>/<wave>-results.json`".

Derived shape, line by line:

| Property | Evidence |
|---|---|
| registration captures `names = [t['name'] for t in tasks]` in **dispatch order** and `agents = {t['name']: t['agent']}` | `inline-dispatcher.py:268-269` (same at `:226-227` on the adopt path) |
| `output = str(handle.output())[:20000]`; `None` only when the handle is missing or is a `_Spawned` id from the `.dispatched` file; an `output()` exception becomes the literal string `<output unavailable: …>` | `:279-286` |
| member record is exactly `{name, agent, output, note}`; `note` is non-null **iff** `output is None` | `:290-295` |
| `seats = len(res)` where `res` was built by iterating `w['names']` | `:292-296` |
| top level is exactly `{lane, round, wave, seats, results}`, `indent=1` | `:296-297` |
| settlement trigger is `nlive = sum(seat_live(...))`; `if nlive == 0: finalize(...)` | `:327-328` |
| write is once per wave (`w['done'] = True`, and `tick()` skips `w['done']`) | `:299`, `:325-326` |

Consequences, stated as contract clauses:

1. **Name and role identity are constructor-enforced, not validated**: `name` and `agent` are
   copied verbatim from the dispatch task object, so `results[].name`/`agent` equal
   `taskCall.tasks[].name`/`agent` element-wise **in dispatch order**.
2. **`seats` is tautological**: it is `len(results)` by construction, so the relation
   `seats == len(results)` carries no information about how many seats were dispatched.
3. **"Settled" means `nlive == 0` at a tick**, not "every seat produced a deliverable". A seat
   that died, or whose final assistant text was mid-flight narration, still gets one member
   record with that narration as `output` (non-`None`) and `note: null`.
4. `output` is capped at 20 000 characters with no truncation marker.
5. `wave` in results is the ready-file wave (`"w1"`), not the dispatch `wave` field
   (`"mori-r58-w1"`); the two artifacts do not share a wave namespace.

## 2. Dispatch `taskCall.tasks[]` vs `results[]`, five (plus one) rounds

Command (lane root): a Python comparison of `w1-dispatch.json` vs `w1-results.json` for
r53–r58, comparing ordered name lists, per-name `agent`, `counts.total`, registry member count
and `seats`. Receipt: `$HYAKU_SCRATCH/mori-r59/Mo59Revenger60/receipt-identity.txt`.

```
r53 tasks=67 seats=67 members=67 counts.total=67 registry=67 names_equal_ordered=True agents_equal=True sha16=0d644e0fb9c50101
r54 tasks=74 seats=74 members=74 counts.total=74 registry=74 names_equal_ordered=True agents_equal=True sha16=ea48a0cc07fa948c
r55 tasks=64 seats=64 members=64 counts.total=64 registry=64 names_equal_ordered=True agents_equal=True sha16=2e5b0a0f94d1fa5b
r56 tasks=64 seats=64 members=64 counts.total=64 registry=64 names_equal_ordered=True agents_equal=True sha16=19536201a689c954
r57 tasks=64 seats=64 members=64 counts.total=64 registry=64 names_equal_ordered=True agents_equal=True sha16=29e7a35df544315d
r58 tasks=64 seats=64 members=64 counts.total=64 registry=64 names_equal_ordered=True agents_equal=True sha16=a57b660d9f41c55d
```

Across the five rounds the assignment names as primary (r54–r58) **and** r53: no name was
dropped, added, renamed, re-roled or reordered, and `results.seats` equals both the dispatch
`counts.total` and the registry member count. All seven dispatch files (r53–r59) have
`counts.resume == 0`, `resumeSends == []` and every registry member `kind == "spawn"`, so the
untested branch of the writer (a resumed seat that is *not* a `taskCall.tasks[]` entry and
therefore would never appear in `results[]`) has not been exercised in any round.

## 3. Settlement semantics that are actually observable

Measured over the same five committed files (scanner `SETTLEMENT_SCAN_OK`, rc 0, no failures —
`python3 tools/mori-settlement-scan.py` over r54…r58):

| round | seats | non-JSON `output` | `note` non-null | member report files present |
|---|---|---|---|---|
| r54 | 74 | 1 | 0 | 73/74 |
| r55 | 64 | 1 | 0 | 63/64 |
| r56 | 64 | 0 | 0 | 64/64 |
| r57 | 64 | 2 (both begin `<think>`) | 0 | 62/64 |
| r58 | 64 | 8 | 0 | **58/64** |

S1. **Settled ≠ delivered.** 10 of 330 members (3.0%; r58 alone 6/64 = 9.4%) have no report
file in `w1/` although their dispatch task carries an explicit `Report:` trailer. Exact r58
case: `Mo58Executor41` (executor, task 1216 bytes, trailer
`.ufo/waves/round-58/w1/Mo58Executor41.md`) has `output` (len 89):

```
"I'll start by reading the frozen contract and counter files, and checking the disk guard."
```

and `note: null`; file `Mo58Executor41.md` does not exist. Its sibling set in the same state:
`Mo58Reviewer10`, `Mo58Reviewer15`, `Mo58Reviewer19`, `Mo58Critic31`, `Mo58Executor47`
(r57: `Mo57Reviewer15`, `Mo57MutationTester37`; r54: `Mo54RevC1Counter`; r55: `Mo55Rc14`).

S2. **`note` cannot flag a dead seat.** `note` is written only when `output is None`
(`inline-dispatcher.py:295`); a seat killed mid-flight yields its last narration, so
`notes_nonnull == 0` in all five rounds while ten seats delivered nothing. The only committed
file with notes is r53 (67 non-null notes, plus `spawned=67`, `outputs_recovered=66`,
`settled_by="orchestrator session exit (no seat live)"`) — i.e. the file where the driver was
*not* the writer.

S3. **Rejected reasoning traces count as settlement.** r57 has two `<think>`-prefixed outputs
(`Mo57Reviewer15`, `Mo57MutationTester37`); both have no report file and are accepted by the
scanner as valid non-empty `output`.

S4. **Nothing cross-checks the artifact against its dispatch.** Grep of the lane
(`grep -rn "taskCall" --include=*.py tools/`) finds `taskCall` in
`tools/mori-wave-settlement.py` (per-seat *report* scan, does not read results files) and
`tools/mori-dispatch-ledger.py` (its `row_results` is a local list, not results.json). The only
lane consumer of results `output` is `tools/mori-vote-bind.py:119-132` (`read_results`), which
keys votes by `name` and therefore *assumes* the dispatch↔results name identity; it also drops
members whose `output` is not a `str` (`:129`), so a null-output seat is absent from every
`tally` (`:161-180`). `tools/mori-census.sh:858-861`
treats a wave as settled on file **existence** alone ("Settled if results.json OR closeout.json … exists").

S5. **No truncation is observable in the committed set.** Max output length per round
(r53…r58): 11812 / 7331 / 11252 / 14254 / 7746 / 13622 — all below the 20 000 cap, so no
committed output was cut. [INFERENCE] A future truncated output would be an unparsable
JSON/markdown tail and would silently drop trailing vote lines consumed by
`mori-vote-bind.py:80-117` (vote extraction) and `:161-180` (tally); unexercised.

S6. **One write per wave.** `finalize()` sets `w['done']`; `tick()` skips done waves, so a late
arriving seat output can never be added later. [INFERENCE] the consequence (a straggler is
permanently absent from `results`) is not directly observable; the code path is
`inline-dispatcher.py:288-300, 325-331`.

## 4. Adversarial result: the scanner's verdict is independent of settlement

Mutants are derived from the parsed `.ufo/waves/round-58/w1-results.json` (and r53 for T9b),
re-serialized under scratch so that only the named field differs, each run through the pinned
tool `tools/mori-settlement-scan.py` (`sha256sum` = `4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9`,
byte-equal to the C2 counter's `PIN`). Receipt:
`$HYAKU_SCRATCH/mori-r59/Mo59Revenger60/receipt-mutants.txt`.

```
T1_drop_1_seat_seats_fixed         rc=0 verdict=SETTLEMENT_SCAN_OK   seats=63 members=63 dispatch_missing=1
T1b_drop_1_seat_seats_kept_64      rc=1 verdict=SETTLEMENT_SCAN_FAIL seats=64 members=63 dispatch_missing=1 reasons=[['seats_mismatch']]
T2_swap_role_reviewer_critic       rc=0 verdict=SETTLEMENT_SCAN_OK   seats=64 members=64 role_mismatch_vs_dispatch=2
T3_null_one_output                 rc=0 verdict=SETTLEMENT_SCAN_OK   seats=64 members=64
T8_null_plus_notes_everywhere      rc=0 verdict=SETTLEMENT_SCAN_OK   seats=64 members=64
T4_rename_all_64_seats             rc=0 verdict=SETTLEMENT_SCAN_OK   seats=64 members=64 dispatch_missing=64 dispatch_extra=64
T5_wrong_wave_and_round            rc=0 verdict=SETTLEMENT_SCAN_OK   seats=64 members=64 (wave="r99-not-this-wave", round=1)
T7_r53style_header_keys            rc=0 verdict=SETTLEMENT_SCAN_OK   seats=64 members=64
T9b_r53_minus_report_file          rc=0 verdict=SETTLEMENT_SCAN_OK   seats=67 members=67 names_equal_r53dispatch=True
                                   null_outputs=1 nonnull_notes=67 extra_header=['note','outputs_recovered','settled_by','spawned']
T6_same_file_passed_five_times     rc=0 verdict=SETTLEMENT_SCAN_OK   files=5
```

Findings:

**A1 — `SETTLEMENT_SCAN_OK` does not imply the wave settled.** A 63-seat truncation of r58 with
`seats` adjusted (T1) and a 64-seat file with every name rewritten to `Mo58GhostNN` (T4) both
score OK. The scanner's docstring (`tools/mori-settlement-scan.py:4-7`) calls the file "the
inline spawn handoff's settlement artifact … when every seat of the wave settles"; nothing in
the tool reads a dispatch, so that sentence is a claim about the writer, not a measured
predicate.

**A2 — the only seat-count check is a tautology.** T1 vs T1b: `seats` corrected to 63 passes;
`seats` left at 64 fails. Because `finalize()` writes `seats=len(res)`
(`inline-dispatcher.py:296`), an under-populated wave that re-derives its own `seats` is
indistinguishable from a full one. This is exactly the failure r58 shows in real data (58/64
delivered, `members==seats==64`, verdict OK).

**A3 — role binding is enum-only.** Swapping `reviewer`↔`critic` between two named seats (T2)
yields OK with two per-name role divergences from the dispatch. The scanner checks membership
in a frozen 10-role tuple (`:39-40, :89-92`), not the seat's assigned role.

**A4 — round/wave headers are unbound.** T5 changes `wave` to an unrelated string and `round`
to 1; still OK (`:64-68` only require non-empty str / int ≥ 1). A recycled r58 artifact placed
at round-59's path would pass the scanner *and* the census existence test.

**A5 — the C2 "drift" arm's detection power is one member key.** r53 fails only on
`member[i]:extra_keys=report_file` (67/67 members). Stripping that one key (T9b) makes the
crash-recovered r53 artifact — one null output, 67 non-null notes, four extra header keys —
scan OK. Re-adding those same header keys, and null-output+notes, to a schema-clean r58 (T7)
also scans OK, i.e. r53's *semantic* anomalies are invisible to the tool; only its key spelling
is visible. `count-c2.py:260` accepts any nonzero exit (`drift_ok = p.returncode != 0`) without
a reason check, so the drift arm is reason-blind as well.

**A6 — the five-file arm cannot detect repetition.** The same file passed five times (T6)
returns OK with five entries. `count-c2.py:242-243` checks only
`verdict == SETTLEMENT_SCAN_OK` and `members == seats` per file; `empty_output`,
`notes_nonnull` and `role_counts` are emitted but unread. (The frozen counter's *tree* arm does
compare copy bytes to the `.ufo` artifacts, so duplicate real artifacts are not currently in
play; the point is the scan arm has no distinctness or delivery signal of its own.)

## 5. Explicit no-counterexample result on the committed data

**No counterexample exists in the committed set for the identity property itself.** Across
r53–r58, the ordered `results[].name` list equals the ordered `taskCall.tasks[]` name list
element-for-element, and `results[].agent` equals the dispatch role for every member; all six
files have `seats == len(results) == counts.total == len(registry.members)`; the five r54–r58
files carry exactly the driver's five top-level keys and `indent=1` layout, while r53 carries
four extra header keys and a per-member `report_file` (the hand-recovered crash artifact). What
*would* have falsified it: any extra/missing
name, any role divergence, any `seats` differing from the dispatch total, or a member count
≠ dispatch count. None occurred.

The counterexample that does exist is to the *semantics*, not the identity: the committed
r54–r58 files record 10 seats with `Report:` trailers and no report file, 12 non-JSON
narration/`<think>` outputs, and 0 notes, and all five return `SETTLEMENT_SCAN_OK`. So the
observable settlement semantics are: **one non-empty `handle.output()` snapshot per dispatched
seat at the first tick where no seat is live**; delivery, verdict, and even JSON-ness are not
part of them.

## 6. What the frozen C2 predicate therefore proves

`count-c2.py`'s scan arm (`:222-250`: five REAL files from R, verdict OK, `members == seats`)
and drift arm (`:252-261`: r53 nonzero exit) prove that five committed files match the
scanner's internal schema and that r53 carries one extra member key. They do **not** prove that
the five waves settled, that their seats delivered, or that the files correspond to their
dispatches — there is no dispatch input anywhere in the predicate. That is consistent with the
contract's own wording ("the five r54–r58 wave-results files MUST scan OK"), but the contract
also describes them as "REAL wave-results files" and the tool docstring as settlement artifacts;
the stronger reading is not supported by data or code.

Corroboration that this gap is already visible in the lane, but was not routed: `SCORECARD.md:2932`
records for round 58 "Results JSON has 64 nonempty outputs and no status/error fields;
report-file scan: 58 present, 6 missing, partial (missing reports are not labeled dead)".
The round-59 contract's routed defects (1-4, §"Round-58 verifier spot-check") do not include
this item, and the frozen scanner has no predicate for it.

## 7. Confidence and limits

- High confidence: writer clauses and identity results (direct code read + six committed
  artifacts, mechanically compared); scanner verdicts on all mutants (rc and JSON captured).
- High confidence: the 58/64 and 10/330 delivery tallies (filesystem listing of `w1/` against
  member names, independently matching SCORECARD:2932 for r58).
- [INFERENCE]: no-rewrite ("one write per wave"), truncation-vote-loss chain, and the resumed-seat
  branch — each backed by code, none exercised by data.
- Not investigated (out of scope): whether the L1 compensated for the 10 undelivered seats out
  of band; the other lane tools' semantics; any round-59 seat's work.

Hygiene: scratch `/fast/scratch/hyaku/mori-r59/Mo59Revenger60/` (mutants + two receipts) was
created with `mkdir -p`, used as `TMPDIR`, and removed before yield; no lane or fleet tracked
file was created or modified.
