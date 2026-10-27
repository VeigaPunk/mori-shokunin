# Seat Mo52RevQualityRows — review of the appended QUALITY 141–142 and README `## Round-52 corrections`

Scope: the appended `corpus/QUALITY.md` criteria 141–142 and the `corpus/README.md` `## Round-52 corrections` block at the data commit `8524904adb25e44f24d9f25aac7eae909625c18c` (diff vs entering tip `4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d`). Review asked: (a) factual statements true, (b) house style (cite lesson, Check, Shown able to fail, Not covered), (c) no duplication of criteria 123–140. All reads and runs were read-only against the fleet; every tool run happened in my scratch (`/fast/scratch/hyaku/mori-r52/Mo52RevQualityRows/`), TMPDIR set there, disk-guard OK (608.8G free). No tools installed.

## 1. Factual checks — evidence

### 1.1 "The committed tool has printed 22 since the round-41 freeze `d72ac167`" (QUALITY 141 rationale; README bullet 1)

Ran the frozen gate's selftest at three revisions in `git archive` trees (archives under my scratch):

- archive of `8524904adb25e44f24d9f25aac7eae909625c18c` (data commit):
  `$ python3 tools/mori-sources-appendonly.py --selftest` → `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0`, rc=0
- archive of `d72ac167` (round-41 freeze):
  `$ python3 tools/mori-sources-appendonly.py --selftest` → `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0`, rc=0
- archive of `62a207f7` (parent of `d72ac167`, round-40 verifier spot-check):
  `$ python3 tools/mori-sources-appendonly.py --selftest` → `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0`, rc=0

So the boundary is exactly the round-41 freeze: the parent prints 15, the freeze and the data commit print 22. The statement holds at both endpoints (and corroborates QUALITY 123: `SKILL.md:912` pinned `pass=15` from round 40 to round 47 while the committed tool printed `pass=22` from the round-41 freeze `d72ac167` on). The round-39 row's `pass=12` is likewise an earlier value (before the round-40 bump to 15). The quoted output format `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0` is exactly what the tool prints.

### 1.2 README bullet 2 — conform.py runnable form

Cloned the lane into scratch (single clone) and ran the literal command from the bullet:

```
$ python3 .ufo/waves/round-39/conform.py 4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d --selftest
PASS predicate          predicate token changed -> only predicate failed
PASS head_pin           pin label renamed -> only head_pin failed
PASS tool_resolve       relative resolution removed -> only tool_resolve failed
PASS bounded_reads      git helper run timeout removed -> only bounded_reads failed
PASS timeout_value      timeout value replaced with None -> only timeout_value failed
PASS drain_shape        communicate drains replaced by wait+read -> only drain_shape failed
PASS timeout_state      budget flag ignored -> only timeout_state failed
PASS scratch            scratch parent moved off-lane -> only scratch failed
PASS selftest_conjunct  communicate timeout keyword stripped -> only selftest_conjunct failed
CONFORM_SELFTEST pass=9 fail=0
$ echo rc=$?
rc=0
```

`CONFORM_SELFTEST pass=9 fail=0`, rc=0 — exactly the bullet's claim. The old pin `--selftest` → `pass=9 fail=0` indeed "names no command"; the corrected form is real and runnable.

### 1.3 The superseded rows and stale pins exist verbatim

At the data commit (line numbers in those files):

- `corpus/README.md:607` row `Counter conformance v2 (operability)` (the "Counter conformance v2" row of the round-39 coverage table) pins `--selftest` → `pass=9 fail=0`, each mutation flipping exactly its own check.
- `corpus/README.md:608` row `Ancestry-based timed supersede (depth/gate)` (the "Ancestry-based timed supersede" row) pins `python3 tools/mori-sources-appendonly.py --selftest` → `pass=12 fail=0`.
- `corpus/QUALITY.md:909` (criterion 112's check cell) pins `python3 tools/mori-sources-appendonly.py --selftest` → `pass=12 fail=0`.

None of these lines changed between the entering tip and the data commit (append-only holds; the diff adds only the trailing blocks), so the bullets' line references and quotes are accurate.

### 1.4 Criterion 142's rationale and shown-able-to-fail

At the data commit, `SCORECARD.md:1771` = "Round-28 amendment A1 (before any data; `.ufo/waves/round-28/contract.md` "Amendment A1"): …" (holds the amendment A1 paragraph), and `SCORECARD.md:1781` = the round-28 measured-outcome C1 row containing "… freshness 5 → 6 proposed" (holds the pair `5 → 6`). The Axes freshness cell pointed at `SCORECARD.md:1771` at the entering tip and points at `SCORECARD.md:1781` at the data commit — exactly as the rationale narrates. The shown-able-to-fail line `item locator SCORECARD.md:1771 expect=pair:5_→_6 got=absent state=mismatch` appears verbatim in `.ufo/waves/round-52/evidence/control-c1-do-nothing.txt` (line 27). Criterion 141's shown-able-to-fail (three living-pin mismatches at the entering tip) also matches the receipt: `corpus/QUALITY.md:909`, `corpus/README.md:607`, `corpus/README.md:608` are exactly the three `item living` lines in `state=mismatch` (receipt lines 12–14). The receipt path cited (`.ufo/waves/round-52/evidence/control-c1-do-nothing.txt`) exists.

## 2. House style

Every criterion 123–140 carries a `Lesson:` citation (even when it says "no round-51 M row covers this rule" — 139) followed by Rationale/Check/Shown able to fail/Not covered. Criteria 141 and 142 have no `Lesson:` line at all; they open with the bold statement and go straight to "This row supersedes … / Rationale:". That is a deviation from the established template (the round-52 instruction lists "cite lesson, Check, Shown able to fail, Not covered"). Both contain Check, Shown able to fail and Not covered, so only the lesson citation is missing. 141 also adds a separate `Counter:` clause inside its Check cell — no other criterion uses a `Counter:` field; the counter reference is normally folded into the Check. (Cosmetic.) The "supersedes 112's check cell only" phrasing matches the existing precedent (111 supersedes 109's check cell).

## 3. Duplication vs criteria 123–140

Grepped criteria 123–140 (and the older pointer/tally criteria 9, 20, 31, 46, 96, 110–115) for `locator|pointer|path:N|lands on|living|supersed|tally`. No existing criterion covers "a command-tally pin in a living document prints its tally today or is superseded" or "a self-assessment pointer lands on the words it reports". Nearest neighbours are all distinct: 9 (general pointer resolution at the carrying commit), 96 (reproducible receipt command/output), 110/111/112 (registry gate ancestry and conformance — 141 explicitly supersedes only 112's check cell), 125/130/131 (hidden pins a checker can see; row-as-rendered; pin bound to its own cells), 134 (round reconciles self-assessment; SHONEN pins carry receipts), 136 (closure counters re-executed). No duplication found.

## 4. One mis-citation (finding)

QUALITY 141's rationale ends "(QUALITY 128)". The parenthesised fact — "the committed tool has printed 22 since the round-41 freeze `d72ac167`" — is stated in QUALITY 123 (`:1033-1034`), not in 128 (which is the depth located-quote criterion and does not mention the gate or the freeze). Grep over QUALITY at the data commit finds `d72ac167`/`pass=22` only at `:1033-1034` (123) and `:1359` (141 itself). The citation should be QUALITY 123.

## 5. Side effect to report (frozen-instrument rule)

`conform.py` hardcodes `LANE` and `SCRATCH_ROOT` to the lane; its `--selftest` creates `tempfile.mkdtemp(prefix="mori-conform-selftest-", dir=SCRATCH_ROOT)` inside the lane's `.ufo/waves/round-39/scratch/`. Before my run that directory was empty; after the run, four `mori-conform-selftest-*` dirs remain there (each holding mutated `counter-*.py` copies; the enclosing `finally: shutil.rmtree(work)` removes only the top-level work dir, not the nested evaluation dirs). These are untracked files inside the lane; I did not delete or edit them. No tracked lane file changed (verified read-only `git status --short` shows only pre-existing untracked wave artifacts plus these dirs).

## 6. UNVERIFIED

- I did not re-run `count-c1.py`/`count-c2.py` (counter execution is the executors' part); statements about what the counter reads are cross-checked against the control receipt only.
- Whether the four conform scratch dirs were created solely by my run (a peer running the same frozen instrument in the same window could also create them) — I can only state they were absent before my run and present after.

## Findings

- MED — `corpus/QUALITY.md:1359` (criterion 141): parenthetical citation "(QUALITY 128)" is wrong; the cited fact lives in QUALITY 123 (`:1033-1034`). Suggest citing 123.
- MED — `corpus/QUALITY.md:1356,1366` (criteria 141, 142): missing `Lesson:` citation, present in every criterion 123–140 and part of the house template. Suggest adding lesson pointers (round-51 closure §5 item 4 / round-50 verifier-spotcheck §5 item 3 for 141; round-51 closure D-c / round-50 lesson locator drift for 142).
- LOW — `corpus/QUALITY.md:1361`: a separate `Counter:` clause inside the Check cell is not used by other criteria (counter refs are folded into Check); cosmetic.
- LOW — lane side effect: running `conform.py --selftest` left four untracked `mori-conform-selftest-*` dirs under `.ufo/waves/round-39/scratch/` (frozen instrument behavior; reported, not touched).
- INFO — all quoted facts verified true: gate prints 22 at `d72ac167` and at the data commit (15 at the parent, 12 at round 39); `CONFORM_SELFTEST pass=9 fail=0` reproduces exactly; the superseded row names/pins are quoted verbatim at README 607/608 and QUALITY 909; SCORECARD 1771/1781 contents and the entering-tip locator/living-pin mismatches match the control receipt. No duplication with criteria 123–140.
