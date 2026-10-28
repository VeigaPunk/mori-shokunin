# Mo59Reviewer10 — C2 scan-arm attack: `results.json` hostile fixtures

Seat role: reviewer (attack). Target: `tools/mori-settlement-scan.py` at frozen
sha256 `4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9`
(verified byte-exact: `git show HEAD:tools/mori-settlement-scan.py | sha256sum`).
Method: read tool source (204 lines) + `count-c2.py`, build 45 hostile
`results.json` fixtures under scratch, run pinned tool on each; read-only on
lane. Fixture battery covered every class named by the seat spec plus adjacent
escapes found in source review.

## Verdicts (tool rc / verdict / failure reasons)

| Fixture (attack class) | rc | verdict | reasons |
|---|---|---|---|
| ok (baseline, 2 members) | 0 | OK | — |
| **seats: true, 1 member** | 0 | **OK** | — bool escapes `isinstance(int)` |
| **seats: false, results: []** | 0 | **OK** | — `False == 0` |
| **seats: true, 2 members** | 1 | FAIL | seats_mismatch (`True==1≠2`) |
| seats: 1.0 (float) | 1 | FAIL | seats_mismatch |
| seats: "1" / null / missing | 1 | FAIL | seats_mismatch |
| seats: 2, 2 members | 0 | OK | — |
| **round: true** | 0 | **OK** | — bool escapes `isinstance(int)` |
| round: null / 0 / 59.0 | 1 | FAIL | round_bad |
| results: object / null / missing | 1 | FAIL | results_not_list |
| member is `["A","reviewer","x",null]` (tuple-in-list) | 1 | FAIL | member[0]:not_object |
| member null / "A" (non-object) | 1 | FAIL | member[0]:not_object |
| name: 42 / null / true / ["A"] / {} / "" | 1 | FAIL | member[0]:name_bad |
| name key missing | 1 | FAIL | member[0]:missing_keys=name |
| output: "" | 0 | OK | counted as `empty_output` |
| output: null | 0 | OK | counted as `empty_output` |
| output: false / 0 / ["x"] | 1 | FAIL | member[0]:output_bad |
| note: "crashed" / {"rc":1} / false | 0 | OK | counted `notes_nonnull` only |
| note key missing | 1 | FAIL | member[0]:missing_keys=note |
| duplicate name within file (A,A) | 1 | FAIL | duplicate_names=A |
| **duplicate name across 2 files, one invocation** | 0 | **OK** | — per-file check only |
| near-dup "A" vs "A " / "a" | 0 | OK | distinct (byte-exact, correct) |
| member extra `report_file` (r53-style drift) | 1 | FAIL | member[0]:extra_keys=report_file |
| **top-level extra keys (report_file, bogus)** | 0 | **OK** | — top-level keys unchecked |
| lane: "" | 1 | FAIL | lane_bad |
| wave: 1 | 1 | FAIL | wave_bad |

Tool selftest: `SETSCAN_SELFTEST pass=10 fail=0` rc=0. C2 counter selftest:
`C2_SELFTEST pass=9 fail=0` rc=0.

Lane-side checks: r53 file fails on member-level `report_file` extra keys
(seats=members=67, member keys include `report_file`) — matches contract drift
arm. r54–r58 files: seats==members (74/64/64/64/64), zero duplicate names,
zero non-null notes, zero empty outputs — the real scan arm is clean.

## Findings (by severity)

### F1 — bool-for-int escapes `seats` and `round` type gates (LOW)
`isinstance(True, int) is True` and `True == 1`, `False == 0`
(`scan_file`, tool lines ~61-63, ~68-69). A file with `"seats": true` +
exactly 1 member, or `"seats": false` + `"results": []`, scans
`SETTLEMENT_SCAN_OK` rc=0; `"round": true` likewise. Every JSON schema treats
boolean as non-integer — the docstring promises "`seats` int == len(results)",
"`round` int >= 1". The equal-count guard (`True==1` needs exactly one member)
narrows exploitability to degenerate 1-member and empty waves, but it is a
real type-safety hole. Fix would be `type(seats) is int` or `not
isinstance(seats, bool)`; frozen bytes cannot change this round, so this lands
as a capability-gap note, not a verdict flip.

### F2 — empty wave accepted (LOW)
`results: []` with `seats: 0` (or `false`) produces a valid file summary
(`members: 0`). A settled wave with zero seats is grammatically allowed by
this grammar; only the zero-*file* invocation is refused (exit 1). Per-file
non-emptiness is unchecked.

### F3 — duplicate names undetectable across files (LOW, docstring-scoped)
`dups` is computed per file (tool lines ~96-98). Two files in one invocation
sharing member name "A" both pass. The contract claim is "name-unique" and the
tool docstring narrows it to "unique inside the file", so this matches stated
semantics — but a wave-level settlement spanning multiple results files would
not catch a seat name duplicated across files.

### F4 — `output:""` ≡ `output:null`; `note` any-type (INFO, docstring-consistent)
`""` and `null` both increment `empty_output`; a settlement cannot distinguish
"seat returned empty" from "seat settled without output". `note` accepts any
JSON value (object, false) and only increments `notes_nonnull` — never fails.
Both match the docstring ("output str or null", "note free"); flagged only
because the spec's "empty string vs null" / "note non-null" classes were named
as attack surfaces and the tool intentionally does not reject either.

### F5 — top-level extra keys unchecked (LOW, asymmetry)
Member keys are exactly `{name,agent,output,note}` (extra → FAIL, the r53
drift basis), but top-level keys beyond `lane/round/wave/seats/results` are
ignored — `"report_file": "x"` at file level scans OK. Schema strictness is
member-level only. Consistent with the frozen r53 arm (which relies on
member-level detection), so no drift-arm impact.

## Verdict impact on C2

**No counterexample to the C2 verdict.** `count-c2.py:measure` derives
`scan_ok`/`drift_ok` exclusively from the six committed r53–r58 files via
`git show` at rev R (counter lines ~205-247); hostile fixtures cannot enter
that arm. The counter's own `members==seats` gate reads ints emitted by the
tool, so F1's bool escape cannot reach it. All findings are capability/
robustness gaps in the pinned tool relative to a strict reading of its own
grammar — the C2 claim ("a capability that validates …") is stated loosely
enough that none falsifies it. F1 is the most defensible defect; recommend a
`rows`/lesson note for a future bool-guard, not a round-59 invalidation.

## Method bounds

- 45 fixtures × 1 tool run each + 1 two-file invocation; all verdicts observed,
  none inferred. Fixture JSON written via `json.dumps` (real JSON types, not
  hand-rolled text).
- Scope: scan arm only. Grammar/entry/rows/pins/trees arms untouched (other
  seats own them).
- Tool pinned bytes confirmed at lane HEAD `8ff344ff`; tool selftest and
  counter selftest receipts above. Scratch
  `/fast/scratch/hyaku/mori-r59/Mo59Reviewer10/` (TMPDIR set) cleaned before
  yield; the fixture table above is the only retained artifact.
