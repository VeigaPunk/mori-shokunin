# RevFindingsCoverage — r40 w1: 13 r39 findings + 6 closure defects vs the contract's Routed inputs

Seat: `RevFindingsCoverage` (reviewer, read-only). Round 40 wave 1, L1 mori-r40 attempt 1.
Delivered prompt carried no `Report:` trailer line; path used is the wave's
`reportDir` + seat name (`.ufo/waves/round-40/w1/RevFindingsCoverage.md`).
Tool installs: none. Repo mutations: none (read-only git/python3/grep).
The three modified receipts and untracked scratch dirs in the worktree are peers'
writes, recorded under Residual risk, not mine.

## Scope and ground truth

- 13 findings: `corpus/lessons/round-39.md:32-116`; counted with
  `grep -cE '^[0-9]+\. \(w1/' corpus/lessons/round-39.md` → **13**.
- 6 closure defects: `corpus/lessons/round-39-verifier-spotcheck.md:60-65`;
  the section's numbered list counts **6**.
- Contract `Routed inputs`: `.ufo/waves/round-40/contract.md:15-46` — 8 bullets
  (B1 line 17, B2 24, B3 29, B4 32, B5 36, B6 40, B7 42, B8 45).
- Claims C1 (conformance v3, P-C10) and C2 (gate v3, P-C11):
  `contract.md:52-147`.
- Receipts: `.ufo/waves/round-40/evidence/`; frozen bytes verified against
  `git show bb1f2457:<path>` (hashes below).
- Corroborating peer reports under `.ufo/waves/round-40/w1/` are cited where used;
  they are not my findings.

## Verdict summary

- The contract's list names **9 of 13** findings by number (1, 2, 4, 5, 7, 8,
  10, 11, 12 — with 2/5, 4/8/12, 7/10 combined) and echoes finding 9's
  receipt-discipline half at `contract.md:163`; it does not name findings 3, 6,
  or 13, nor finding 9's docstring defect.
- **8 of 13 are discharged by the list as claimed**: 2, 4, 5, 7, 8, 10, 11, 12
  (with finding 5(a)'s cited receipt weak and finding 7 split — see F4/F6).
- **5 of 13 are not discharged as claimed**:
  - finding 1: the bullet exists, but its cited record (the r39 erratum) does not
    contain the narrowed reading — **false coverage claim** (HIGH);
  - findings 3, 6, 13: no bullet, no seat, no disposition (3 and 13 still have the
    described defect in the landed bytes; 6 was already fixed in r39 but the r40
    list does not say so);
  - finding 9: only its receipt-discipline half is adopted; the docstring-anchor
    defect is untouched.
- **4 of 6 closure defects** are in the list (1-4). Defects 5 (wave 2) and 6
  (W04 census debt) are dispositioned **only outside** the list: 5 by the
  single-wave round-shape paragraph / wave plan, 6 by the r40 lesson Gate and the
  `ConnW04Routing` seat. The list heading itself says "defects 1–4", so this is a
  scope mismatch with the assignment, not necessarily a lane error.
- **Double coverage**: finding 7 is split across B3 (`18 ids`) and B5 (`pass=11`)
  with no cross-reference; the dag-r fixture is double-used for findings 2 and
  5(a) but demonstrates only finding 2's eligible-set aspect.
- **C2's declared count is false** in three artefacts: contract says 19 ids, the
  lesson/wave spec say 34, the receipt prints **35** (independent re-run at both
  the scored tip and HEAD). Semantic predicate is correct; the counted
  annotations are claim-sizing drift.

## Mapping matrix (13 findings)

| # | r39 w1 finding (lesson line) | Contract disposition | Claim | Verdict |
|---|---|---|---|---|
| 1 | P-C7 prose exceeds code (32) | B4 says narrowed reading is in the r39 erratum | non-claim | **UNCOVERED**: erratum has no such paragraph (`grep` exit 1) |
| 2 | gate eligible set edit-bounded; S226; 18-ids prose (38) | B3 | C2 | mapped; semantic fix verified; counted annotation still wrong (19/34 vs 35) |
| 3 | `timeout_value` message says "non-numeric constant" (45) | none | — | **UNCOVERED**: message unchanged (`conform.py:164,197`) |
| 4 | name-not-value survivors: shadow, conditional, `1e400`, fold exits 2 (47) | B2 | C1 | mapped; receipts verified (before met/exit 2, after unmet on `timeout_scope`) |
| 5 | (a) linear re-add; (b) first-parent-lacks-path fall-through (54) | B3 | C2 | mapped; (b) verified via timing flip; (a) receipt does not demonstrate the claimed changed-event divergence |
| 6 | `c9-after-lane.txt` counts name no rev (60) | none | — | **UNCOVERED in r40**; already amended in r39 (`c9-after-lane.txt:7-8`) |
| 7 | `pass=11` stale prose; 18-ids overclaim (63) | B5 + B3 (via "see finding 2") | erratum + C2 | split across two bullets; both components have an owner, no cross-reference |
| 8 | `drain_shape` per-function, decoy/underscore/tuple/second-Popen (66) | B2 | C1 | mapped; nine after receipts verified |
| 9 | `anchors_v2` treats docstring positions as code; rev discipline (72) | none for the defect; `contract.md:163` adopts the rev-discipline takeaway | — | **HALF-MAPPED**: docstring defect untouched (witnesses byte-identical to r39; occurrence rule excludes only `#` comments) |
| 10 | before-cell cites `fixtures/make-ancestry-dags.py`, a path in no commit (77) | B5 (erratum) | non-claim | mapped; verified (path in no commit; erratum:24-28) |
| 11 | drain-shape before-control not reproducible + wording + process notes (84) | B1 | C1 + erratum | main half mapped and verified (decoy fixture); `head_pin` and evidence-path-list notes partial |
| 12 | conjunct kill rule not read from checker table; multi-counter first-only (96) | B2 | C1 | mapped; receipts verified (gutted 0/10 vs 8/8; per-counter comm_violations) |
| 13 | `--arms selftest` spacing bug + `ROWSTATES_RE` cleanup; scorecard corroboration (104) | none | — | **UNCOVERED**: `ROWSTATES_RE` removed incidentally, spacing bug persists and reproduces |

PASS notes inside findings 10/12/13 (RevFreeze PASS, RevC7Live PASS, RevC7Negatives
PASS) are not defects and need no disposition; only the defect components are
mapped above.

## Mapping matrix (6 closure routed defects)

| # | Closure defect (spotcheck line) | Contract disposition | Status |
|---|---|---|---|
| 1 | drain-shape re-claim + "bypass-wait" wording (60) | B1 | ✓ verified: `c10-red-decoy.txt` r39 `CONFORM=met`; `c10-after-decoy.txt` v3 `CONFORM=unmet` with `drain_bind FAIL`; erratum:3-16 names and supersedes the sentence |
| 2 | name-not-value survivors + decoy (61) | B2 | ✓ verified by the nine survivor receipts + multicounter + gutted-conjunct receipts |
| 3 | first-parent prose vs fall-through; unreachable 18-ids prose, one source of truth (62) | B3 | ~ partial: first-parent semantics now match code; but the frozen predicate carries a **new** miscount (19) contradicted by its receipt (35), and the lesson's correction says 34 — one source of truth is not achieved |
| 4 | S227 quote label 18 vs 17 (63) | B6 | ✓ verified: erratum:18-22; quote word count = 17 |
| 5 | wave 2 (falsify) undispatched (64) | not in the list | ~ only implicit: `contract.md:171-174` one v2 wave with ≥25% attack roles; `wave-plan.json` 66 spawn / 0 resume. Never stated as the discharge |
| 6 | standing W04 census debt (65) | not in the list | ~ disposition outside the list: r40 lesson Gate (`corpus/lessons/round-40.md:8-10`) and the `ConnW04Routing` seat |

## Detailed findings

### F1 (HIGH) — B4's erratum record does not exist; finding 1 is uncovered

`contract.md:32-35` says the P-C7 narrowed reading is "recorded in the r39
erratum". It is not.

```
$ grep -n 'P-C7\|drift_kill\|narrowed\|honest and mutated' corpus/lessons/round-39-erratum.md
(no output; exit 1)
$ wc -l corpus/lessons/round-39-erratum.md
28 corpus/lessons/round-39-erratum.md
```

The 28-line erratum contains exactly three corrections: the bypass-wait sentence
(:3-16), the S227 18→17 label (:18-22), and the r39 `pass=11` / make-ancestry
citations (:24-28). The scored-tip blob is identical to the worktree file:

```
$ git show 265a955cc:corpus/lessons/round-39-erratum.md | sha256sum
5cfea3774885697ecb4201de839c36dec7eb97292231199aefc17557709747f6  -
$ sha256sum corpus/lessons/round-39-erratum.md
5cfea3774885697ecb4201de839c36dec7eb97292231199aefc17557709747f6  corpus/lessons/round-39-erratum.md
```

The r40 lesson repeats the false claim (`corpus/lessons/round-40.md:42-43`,
"narrowed reading recorded in the same erratum"). The narrowed reading in the
contract itself is accurate (drift_kill_v2 compares the mutant run's got table to
the arm's want table; `c10-parity`/`count-c8` still print P-C7). Fix is one
append-only erratum paragraph; no predicate change and no re-freeze needed.
As written, the round claims to discharge finding 1 but the r39 record remains
uncorrected.

### F2 (HIGH completeness; low/medium per item) — findings 3, 6, 13 have no disposition; 9 is half-mapped

- **Finding 3** (message names no symbol). `grep -n 'non-numeric constant'
  .ufo/waves/round-40/conform.py` → `164` and `197`. The after receipt still
  prints the generic text, e.g. `c10-after-shadow-none.txt:7`:
  `check timeout_scope FAIL (... 'line 115 (communicate): non-numeric constant')`.
  No contract bullet, no seat mentions it. Cosmetic, but uncovered.
- **Finding 6** (walk counts name no rev). No contract reference. The finding is
  already discharged in r39: `.ufo/waves/round-39/evidence/c9-after-lane.txt:7-8`
  names the entering tip `13f3db7e`, the landed tip `13bfba23`, and the 54/53
  counts. So no r40 work is owed; the r40 list simply does not record the no-op.
- **Finding 9** (docstring-parked anchors). The only contract reference is
  `:163` — "Receipts name the measured revision (r39 lesson finding 9
  discipline)" — which adopts the finding's *second* half. The defect half is
  untouched: the four r40 witness files are byte-identical to r39's
  (`cmp -s .ufo/waves/round-39/fixtures/$f .ufo/waves/round-40/fixtures/$f` →
  `identical` for `witness-comment-anchors.md`, `witness-dangling-row.md`,
  `witness-summary-only-live.txt`, `witness-token-entry.md`; no docstring
  witness), and the occurrence rule still excludes only `#` comment lines
  (`count-c8.py:244-264`: a line whose stripped form starts with `#` never
  counts; any other occurrence counts). A docstring occurrence would still pass.
  No seat mentions docstrings.
- **Finding 13** (`--arms selftest` spacing; `ROWSTATES_RE` cleanup).
  `ROWSTATES_RE` was removed from the r40 counter —
  `grep -c 'ROWSTATES_RE' .ufo/waves/round-40/count-c8.py` → 0, while the
  extracted r39 counter has it at `count-c7-r39.py:98` — so the dead-code cleanup
  landed incidentally (probably with SimpCounters D1–D4). The spacing bug
  persists and reproduces against the real probe format:

  ```
  $ python3  # import count-c8, format exactly as tools/mori-source-drift.py:441
  probe_format_repr: 'selftest row_states           PASS'
  parse_rowstates(PASS): None
  probe_format_repr_fail: "selftest row_states           FAIL (got=[('S1','fresh')] want=[('S1','drifted')])"
  parse_rowstates(FAIL): None
  ```

  `count-c8.py:335` requires exactly one space after `row_states`;
  `tools/mori-source-drift.py:441` prints `"selftest %-20s %s%s"`, i.e. the name
  padded to 20 columns. `--arms selftest` (`count-c8.py:439`) therefore returns
  `None` and reports failure even on a passing tool. The r39 finding called this
  latent/unreachable from the scored path, and that remains true, but the routed
  cleanup item is not discharged and the contract says nothing about it.
  Finding 13's corroboration items F2–F6/F8 (r39 scorecard before-side) also have
  no disposition; F1 is covered by B1 and F5's `pass=11` half by B5, but the
  A/C-swap half of F5 has no erratum paragraph (the erratum contains no A/C text).

### F3 (MEDIUM) — closure defects 5 and 6 are outside the Routed inputs list

The list heading is explicit: "r39 closure routed defects 1–4 + lesson findings"
(`contract.md:15`). Defect 5 (`spotcheck:64`, wave 2 undispatched) and defect 6
(`spotcheck:65`, W04 debt) are not bullets.

- Defect 5's only disposition is implicit: `contract.md:171-174` specifies ONE v2
  wave of 64 seats with ≥25% attack roles, and `wave-plan.json` counts
  `"spawn": 66, "resume": 0`. If folding falsification into the single wave is
  the intended discharge, one sentence in the Routed inputs should say so.
- Defect 6's disposition exists outside the list: `corpus/lessons/round-40.md:8-10`
  says the 16 W04 duplicate-URL rows are pre-existing fleet debt routed by the
  r39 closure, and the `ConnW04Routing` seat re-checks it. The substance is
  covered; the list is incomplete relative to the six defects in the assignment.

### F4 (MEDIUM) — finding 5(a) is double-covered by the dag-r receipt and not demonstrated

B3 routes findings 2/5 to C2 and cites the three DAG receipts. dag-r is the only
fixture for both the eligible-set omission (finding 2) and the re-add corner
(finding 5a). The receipts show:

```
c11-red-readd.txt:5     appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[S008]
c11-red-readd.txt:6     supersede_timing superseded_as_of=[] stale_supersede=[]
c11-after-fixture-r.txt:5 appendonly_violations=0 ids=[] deleted=[] superseded=[S008] round_changed=[S008]
c11-after-fixture-r.txt:6 supersede_timing superseded_as_of=[S008] stale_supersede=[]
```

Both gates print `round_changed=[S008]` and neither prints a `changed S008` line.
The only printed divergence is the timing line — i.e. the finding-2 eligible-set
class. `contract.md:132-133` nevertheless says v2 "prints a `changed` event for
the linear delete-then-re-add"; the cited receipt does not show that. The r40
lesson's honest-stop paragraph (`round-40.md:26-33`) admits the v2 red for the
re-add changed event is invisible at the frozen bytes; the gate selftest's
hand-written expectation (`tools/mori-sources-appendonly.py:615-618`) is the only
able-to-fail. Until `MutGateReadd` commits its mutation receipt, C2's kill rule
"a gate keeping the re-add changed event fails fixture R" (`contract.md:145-147`)
has no red receipt behind it.

The neighbouring dag-p wording has the same shape: `contract.md:130-132` says v2
"fabricates a `changed` line", but both `c11-red-firstparent.txt` and
`c11-after-fixture-p.txt` print the same `changed S001 superseded_by=S002` line
(the legitimate side-branch edit); only the timing verdict flips
(`as_of=[] → [S001]`). `ExeDagP.md` states it directly: "The changed-event and
violation lines are unchanged between red and after receipts." Finding 5(b)
itself is demonstrated; the contract's wording overstates the observable.

### F5 (MEDIUM, corroborates CritPredParenthetical/ExeGateLane) — C2's declared count is false

- `contract.md:137` (after-cell): `superseded_as_of=[19 ids incl. S226]`.
- `contract.md:119` (P-C11 verbatim) and `tools/mori-sources-appendonly.py:87`
  (PREDICATE): "(19 ids)".
- `c11-after-lane.txt:22` (the receipt cited at `contract.md:137`): **35** ids.
- `corpus/lessons/round-40.md:24` (M24): **34**; the wave spec and LOG likewise
  say 34 (and the `ExeGateLane` task text told that seat to verify 34).

My independent re-run:

```
$ python3 tools/mori-sources-appendonly.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --repo . | tail -1
supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S067,S069,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193,S226] stale_supersede=[]
```

Same line at `HEAD` (`ede486b7`). Python parse of the receipts: before 18,
after 35, at `e37dcc6` 33 as-of + `[S069]` stale (34 superseded). The 17
newcomers are `S067,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,
S128,S129,S131,S140,S226` — i.e. S226 plus 16 earlier, not "S226 plus 15".
`CritPredParenthetical.md` (35; the propagated 34 matches the `e37dcc6`
superseded union) and `ExeGateLane.md` (35) independently confirm.

Consequence for this seat's question: the mapping "findings 2/5 → C2" is present,
but the claim's declared after-state is not its measured output, and routed
defect 3's "one source of truth" is not achieved (contract 19, lesson/spec 34,
receipt 35). The gate code implements the predicate's semantic sentence
correctly; this is claim-sizing drift, not a broken predicate. The contract's own
kill rule cannot discriminate either: both the mutant (18) and the correct gate
(35) "mismatch the declared 19 ids"; the actual discriminator is S226 presence.

### F6 (LOW) — finding 7 is split across two bullets without a cross-reference

Finding 7 (`round-39.md:63-65`) has two components. Its `pass=11` component is
owned by B5 and verified (`erratum:24-28`; the r39 gate receipt prints 12). Its
"18 ids + S226" component is owned by B3 via finding 2 (the lesson itself says
"see finding 2 above"). Each component has exactly one owner, but B3 and B5 do
not mention each other, so a strict "exactly one bullet per finding" reading
fails. Bookkeeping fix: B5 should say "Finding 10 + finding 7's pass=11
component; the 18-ids component is under Findings 2/5".

### F7 (LOW) — finding 11's auxiliary process notes are only partially dispositioned

B1 discharges the drain-shape before-control and the wording, both verified (see
the closure-defect 1 row). The finding also recorded two process notes that B1
does not mention:

- `head_pin` still compares the counter's `head_at_measurement` to live
  `git rev-parse HEAD` (`conform.py:519-524`) — the r38-carried tautology.
  At the scored tip the receipt shows `pin=265a955cc tip=265a955cc`; running
  against a later HEAD makes the check fail, so it is not vacuous in that
  direction, but it does not pin the contract's declared revision independently.
- The contract's evidence-path list still does not match disk:
  `contract.md:151` writes `census-end.txt` without the `evidence/` prefix, and
  the list omits `evidence/c10-parity.txt`, which `contract.md:72` cites as the
  parity proof. This is the same class as finding 11's "contract's evidence-path
  list does not match the disk set".
- The c7-after rev-naming part is addressed generically by
  `contract.md:163` ("Receipts name the measured revision"), and the r40 receipts
  do name `265a955cc...`. Partial credit.

## Double-coverage summary

1. **Finding 7**: B3 + B5 split (see F6).
2. **dag-r fixture**: findings 2 and 5(a) share one before/after pair; only
   finding 2's eligible-set aspect is observable in it (see F4).
3. **Decoy fixture**: findings 8 and 11 share the one `survivor-decoy.py`
   red/after pair. This is legitimate — finding 8 names the decoy bypass and
   finding 11 names the missing before-control for the same shape — but it is one
   control for two findings, so a failure of that fixture would hit both.
4. **Finding 11 + closure defect 1**: the same item paired in B1; correct, not
   double coverage.

## Commands run (exact; cwd `/home/vgpnk/Projects/shokunin/mori-shokunin` unless noted)

1. `grep -cE '^[0-9]+\. \(w1/' corpus/lessons/round-39.md` → `13`.
   Closure list count from the `## Routed defects` section → `6`.
2. `grep -n 'Finding' .ufo/waves/round-40/contract.md` → lines
   `17,24,29,32,36` (findings 1, 2/5, 4/8/12, 7/10, 11).
   `grep -in 'finding [0-9]' .ufo/waves/round-40/contract.md` adds `:62`
   (finding 11 in the claim prose) and `:163` (finding 9 discipline).
3. `grep -n 'P-C7\|drift_kill\|narrowed\|honest and mutated' corpus/lessons/round-39-erratum.md`
   → no output, exit `1`; `wc -l` → `28`.
4. `git show 265a955cc:corpus/lessons/round-39-erratum.md | sha256sum` →
   `5cfea3774885697ecb4201de839c36dec7eb97292231199aefc17557709747f6`;
   worktree file identical.
5. `python3 tools/mori-sources-appendonly.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --repo . | tail -1`
   → the 35-id line quoted in F5. Same command with `HEAD` (ede486b7) → same line.
6. Python parse of the three `c11-*-lane`/`e37dcc6` receipts:
   as-of `18 / 35 / 33`, stale `0 / 0 / 1`, superseded `18 / 35 / 34`.
7. `python3` importing `.ufo/waves/round-40/count-c8.py` and calling
   `parse_rowstates('selftest row_states           PASS')` → `None`;
   the same on the FAIL-with-detail string → `None`.
8. `grep -c 'ROWSTATES_RE' .ufo/waves/round-40/count-c8.py` → `0`;
   `grep -n 'ROWSTATES_RE' .ufo/waves/round-40/fixtures/extracted/count-c7-r39.py`
   → `98`.
9. `grep -n 'non-numeric constant' .ufo/waves/round-40/conform.py` → `164`, `197`.
10. `git rev-list --all --objects | grep -c 'make-ancestry-dags.py'` → `0`;
    `git log --all --oneline -- '**/make-ancestry-dags.py'` → no commits.
11. `git diff --stat -- .ufo/waves/round-40/evidence/` →
    `3 files changed, 8 insertions(+), 3 deletions(-)`
    (`c10-after-conjunct.txt`, `c10-after-selftest.txt`, `c10-red-conjunct.txt`);
    `git status --porcelain` also lists untracked scratch dirs.
12. `git show bb1f2457:<path> | sha256sum` vs the extracted files:
    conform v2 `fe0be179...`, count c7 `b92c65f2...`, gate v2 `62cd4132...` —
    all identical to `fixtures/extracted/`.
13. AST extraction: `conform.PREDICATE` equals the contract P-C10 blockquote
    (1564 normalised chars) and `gate.PREDICATE` equals P-C11 (1036) — both
    `True`.
14. `sha256sum` of the six pinned paths vs `evidence/freeze-r40.txt` → all nine
    recorded hashes (six pins + three extracted) match.
15. `cmp -s` of the four r39 vs r40 witness files → identical each.

## Residual risk and verification gaps

- **Finding 5(a)'s able-to-fail**: the missing receipt is `MutGateReadd`'s
  mutation run. If that seat does not show the dag-r arm failing when the v2
  re-add branch is restored, C2's re-add kill rule is unsupported. This is the
  one open item from my mapping that a sibling can still close.
- **Worktree receipt mutation**: `ExeConjunctAfter.md` self-reports updating
  `evidence/c10-after-conjunct.txt` and `c10-red-conjunct.txt`;
  `ExeConformSelftest.md` self-reports replacing `c10-after-selftest.txt`.
  `ExeDagP.md` wrote its receipt directly to `evidence/` as well (content
  currently matches the committed blob; `ExeDagN`/`ExeDagR` correctly used
  `.scratch`). The wave bounds say executors write only the single named artifact
  under `.ufo/waves/round-40/w1/` or `.scratch/`. The committed blobs at
  `265a955cc` are still the scored ground truth; but any seat reading the
  worktree "already landed" receipts sees modified bytes (verdict bodies are
  unchanged; command lines/timing added). Integration should decide restore vs
  commit. I did not mutate.
- **Not re-run by me**: the 57-second conform `--selftest`. I verified
  `c10-after-selftest.txt` (11 arms, `pass=11 fail=0`) and
  `ExeConformSelftest.md`'s independent 57.371 s run; I re-ran the gate at both
  revs. The nine survivor after-receipts were read, not re-executed.
- **Low doc defect**: `conform.py:12` says the `predicate` check compares "the
  contract's P-C10 sentence" to the counter's first line, but the code extracts
  the P-C7 blockquote from the round-39 contract (`conform.py:72-74,142-150`) and
  the counter prints P-C7. The two PREDICATE strings are verbatim-correct; only
  the checker's self-description is stale.
- **Count 19/34/35** is also under attack by `CritPredParenthetical` and
  `ExeGateLane`; I confirm 35 independently and note that 34 equals the
  `e37dcc6` superseded union, which is the plausible source of the propagated
  number.
