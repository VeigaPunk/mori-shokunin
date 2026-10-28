# Mo59Reviewer19 — no-harm review (contract, counters, tools, fixtures)

Verdict: **no counterexample to no-harm on the destructive axes** (gate-weakening,
evidence deletion, sibling-scope absorption, freeze drift). One structural
defect found *inside the frozen counter* — a reason-classification hole that
makes the real-entry arm strictly weaker than the hostile-tree arm for the
`grammar` defect class — plus one bounded unverified-artifact gap. Neither
affects this wave's verdict (demonstrated below), but both are recorded as
residual risk for the integrator.

Method (read-only): freeze-fidelity sha256 triple-check; post-freeze diff audit;
static read of contract + both counters + both tools + all 25 expect files;
functional counter runs at HEAD and entering rev against my scratch dir only;
manual scans of the six real artifacts; adversarial `eval_entry` injection.

## Axes checked and held

1. **Freeze fidelity** — contract/count-c1/count-c2 worktree sha256 ==
   `git show 60b3a76:` blobs: `427fca0b…`, `2be6fda8…`, `2df3ae84…` (triple match).
   Tool PINs at HEAD == frozen pins (`38b733d8…472b8`, `4c04bf21…5ac9a9`).
   Post-freeze commits touch zero frozen bytes: `git diff --stat 60b3a76..HEAD`
   = spec/dispatch/evidence additions (8ff344ff), C2 corpus data (be737211),
   entry correction (7b86704d) — all claim-scoped.

2. **Gate strength** — functional runs (`--scratch /fast/scratch/hyaku/mori-r59/Mo59Reviewer19/*`):
   - `C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=HEAD` rc 0
   - `C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 rev=HEAD` rc 0
   - Do-nothing at entering: `C1=unmet … failed=tool_absent,selftest,fixtures_absent,real,pointers` rc 1 — control holds, `failed=tool_absent` present.
   - All 13 fixtures-c1 + 12 trees-c2 expect prefixes cover the emitted reason
     namespaces; `verdict_unmet`/`want_ok` criteria strict (tree arm uses raw
     `ok`, i.e. *every* reason kills — strict superset of real arm, see F1).
   - Real scan arm verified independently: r54–r58 → `SETTLEMENT_SCAN_OK`,
     members==seats (74/64/64/64/64); r53 → `SETTLEMENT_SCAN_FAIL`,
     `member[i]:extra_keys=report_file` — contract's drift arm holds.
   - MANIFEST pin real: `2807c6ab:MANIFEST.json` rounds[832] = lane mori,
     lane_round 56, `capabilities_added` strings start with both BOUND names.
     SCORECARD rows 1989–1990 bind key/name/pointers/56; pointers resolve.

3. **Evidence preservation** — `git log --diff-filter=D 2b9f039..HEAD` empty
   (zero deletions). At-freeze receipts consistent with history: C2 receipt's
   `copy_absent`/`entry_absent` at 60b3a76 verified — `ls-tree` shows those
   paths absent at both freeze commits; they landed later in be737211.
   Committed corpus state matches counter pins (S553–S559 mined, used-by ==
   entry, 11-cell rows; S560 reconciliation row for routed defect 2).

4. **Scope isolation** — w1-spec: 64 items, roles = reviewer 20 / critic 10 /
   mutation-tester 8 / executor 8 / revenger 4 / scout 4 / scribe 4 /
   connector 2 / sentinel 2 / simplifier 2; attack share 40/64 = 62.5% ≥ 25%;
   planner seats 0 (L1-held per contract); no prompt names a production file as
   Report target; all reports confined to `.ufo/waves/round-59/w1/`.

## Findings

### F1 (low–medium, frozen-counter design defect): `grammar:` reasons invisible to the real-entry arm

`count-c2.py` `eval_entry` emits `grammar:<line>` for any malformed claim line
(lines 121–122). The **hostile-tree arm** (line 346) uses `eval_entry`'s `ok`
directly — every reason, including `grammar`, forces UNMET (t12 relies on this).
The **real-entry arm** (lines 303–313) instead classifies reasons by prefix:
`entry_ok` covers only `frontmatter|distinct|claims_min|files|span|entry_absent`,
`rows_ok` covers `rows`, `pins_ok` covers `pin`. `grammar` is in none of them.

Demonstrated (materialized byte-exact HEAD tree under scratch, appended
`- **K99** — bogus Quote: no-pin-span-missing` to the entry copy):

    real entry ok= True  reasons= []
    defective ok= False  reasons= ['grammar:- **K99** — bogus Quote: no-pin-span-mis']
    real-arm flags after defect: entry_ok=True rows_ok=True pins_ok=True
    => grammar-only defect invisible to met

So a malformed claim line that is fatal in tree t12 would be silently ignored
on the real entry — the counter's own predicate is asymmetric between its two
arms for exactly this defect class. The counter is frozen; nothing to
remediate. The landed entry at 7b86704d produces zero `grammar:` reasons, so
the current verdict is unaffected; integrator should note the gap if the entry
is edited post-landing, and future counters should consume the full reasons
list rather than a prefix subset.

### F2 (informational): seventh artifact copy outside the frozen `ARTIFACTS` map

`corpus/evidence/sources-r59/w1-results-r53.json` (S559) is committed and cited
by the entry's source lines but is not in `count-c2.py ARTIFACTS` — the `tree`
arm never checks its byte-equality, and no K claim may quote it (the
`files:outside` reason would kill any such claim; the K11 prose demotion in
7b86704d is the correct response). Manually closed this instance: copy sha256
`0d644e0f…4260` == `git show HEAD:.ufo/waves/round-53/w1-results.json`.
Residual: the copy can drift unnoticed by the counter; bounded by S559's
recorded sha and `used-by` binding.

### Latent (not triggered): empty `expect.txt` flips a hostile tree into a positive control

`trees-c2` arm: `expect = [e for e in expect.split(",") if e]`;
`want_ok = not expect`. A blank expect file makes `want_ok=True`, so a
defective tree that *should* judge UNMET would instead be demanded to pass —
inverting the fixture's purpose. All 12 committed expects are non-empty;
flagged as a design trap for future counter authors (the C1 fixture arm's
`matched = all(...)` over an empty list has the same True-vacuous shape, though
`verdict_unmet` still must hold there, softening it).

## Residual risk / verification gaps

- Grammar hole (F1) means `C2=met` does not assert *no malformed claim lines* —
  only the counted classes. Verified the landed entry is clean today
  (`eval_entry` → `ok=True, reasons=[]`).
- `drift_ok` is `p.returncode != 0` — any nonzero exit counts as drift success;
  a hypothetical crash exit (e.g. argparse 2) would satisfy it. Unreachable in
  practice for `main()` on an existing file; noted for completeness.
- Census `exit 0 at round end` is outside this seat's window; schema spot-check
  of new rows S553–S560 passed (11 cells each).
- Lane HEAD moved during review (8ff344ff → 7b86704d); both counter runs and
  the corpus reads were against the later HEAD — all consistent.

Receipts: counter outputs and scan verdicts inline above; scratch
`/fast/scratch/hyaku/mori-r59/Mo59Reviewer19/` cleaned before yield.
No production edits, no VCS mutation, no fleet/sibling writes.
