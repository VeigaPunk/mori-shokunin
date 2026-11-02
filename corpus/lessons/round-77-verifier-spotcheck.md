# Round 77 verifier spot-check — mori (non-author closure)

author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))
round: 77
date: 2026-11-02
lane head closed: `6a230c4ba1234cb4dc4f282eb697548f1c3ff1ad` (refs/heads/master == origin/master, ahead 0)
entering: `608815aa6b82ca591a69cb43b768e33564a68f03`
report commit: fleet `4e9ee125d746ba94740e52cb129257917bde8dca` (mori-shokunin <mori@shokunin.local>, 2026-11-02T08:33:55-08:00)
dispatch digest (watchdog, matches the closure contract): `2026-11-02T07:02:27-08:00 launch mori round=77 base=608815aa6b82 (zcode run14)` / `2026-11-02T08:33:54-08:00 complete mori round=77 head=6a230c4ba123 pushed=True`

## Verdict summary

**rejected-honest-stop, admitted=false.** C1 (depth) and C3 (freshness) verify in full
(re-measured by this closure). C2 (operability, capability acquisition) does NOT verify as
LANDED work: `tools/mori-counter-win.py` is disk-only — absent from the landing commit, from
`refs/heads/master`, and from every ref (`git log --all -- tools/mori-counter-win.py` is
empty). Landed means committed; a working-tree-only change does not count for the round.
No axis harmed. The lane-round itself is a real report, not a marker: substantial committed
C1/C3 work plus honest receipts.

## Step-1 conformance

| Check | Result |
|---|---|
| Report committed in fleet repo by lane identity | PASS — `git log --format='%an %ae %H' -1 -- .ufo/reports/round-77/mori.md` → `mori-shokunin mori@shokunin.local 4e9ee125d746ba94740e52cb129257917bde8dca` |
| SHONEN heading in committed report bytes | PASS — `git show 4e9ee125:.ufo/reports/round-77/mori.md | grep -n '## SHONEN'` → line 55; 4 boxes, all `[~]`, zero `[x]` |
| Report is real, not a marker | PASS — names committed work with checkable hashes (landing `6a230c4b`, entering `608815aa`) and evidence pointers; landing diff re-derived 21 paths, +2414/−7 |
| Cited lane commits exist and are ancestors | PASS — `git merge-base --is-ancestor` for `608815aa…` (YES), `6a230c4b…` == tip; receipt-cited `986d4b46…` (r61 data tip) YES |
| Lane tip pushed | PASS — `ls-remote origin refs/heads/master` = `6a230c4ba1234cb4dc4f282eb697548f1c3ff1ad` = local `refs/heads/master` |
| Round's cited lane work reachable from 608815aa..6a230c4b | PASS — the landing commit is the sole commit in the range (authored by mori-shokunin), pushed at 08:33:54−08:00, report committed 08:33:55−08:00 (commit-before-report ordering holds) |
| Commit-before-report ordering | PASS — see above |
| No `[x]` written into SHONEN.md | PASS — SHONEN.md diff is 4 box-line rewrites, all `[~]` with evidence pointers, canonical 4-box structure preserved |
| PROVINCE/AGENTS/QUALITY and registered instruments absent from round diff | PASS — name-status list contains none of them |

Conformance defects: none. Claim-verification defects are routed below (they are
status-neutral for step 1; they decide the verdict, not conformance).

## Per-claim re-check

### C1 (depth, sourced — S592): VERIFIED MET (re-measured)

- Before/after: `git cat-file -e 608815aa:corpus/knowledge/counter-win-r77.md` → rc 128
  (absent at entering); present at `6a230c4b`; `grep -c '^- \*\*K'` → 7 (K1–K7).
- SOURCES rows 364 → 365: `git show <rev>:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → 364 entering / 365 landing. badNF=0 shape.
- S592 pin: `git show 6a230c4b:corpus/evidence/sources-r77/S592.html | sha256sum` →
  `5f2e58ad44160bc35bb52be688812047f09bd5bab81c2959f32682c586ee2bfe`, 50980 bytes — matches
  the row, the knowledge-entry provenance trio, and the receipt.
- LIVE RE-OPEN (this closure, 2026-11-02T17:1xZ): `curl -sS -m 60 -L` of
  https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/typeperf
  → `<title>typeperf | Microsoft Learn</title>`, **50980 bytes, sha256 identical to the
  pin** — the pin is live-true today; all three anchor quotes present on the live page.
- Anchors re-run by this closure over the committed pin bytes:
  `python -I tools/mori-anchor-check.py --pin corpus/evidence/sources-r77/S592.html --check …`
  ×3 → `ANCHOR_CHECK: PASS items=3 ok=3` rc 0 (13/7/18 words each, located_on 749/806/798);
  able-to-fail mislocation arm (wrong line 806 + mutated count 14) → `ANCHOR_CHECK: FAIL
  items=1 ok=0 mislocated=1` **rc 1**. The checker discriminates — reproduced exactly.
- Used-by appends: SOURCES diff is exactly 3 modified rows (S572/S573/S574) + 1 new row
  (S592); status/opened/recheck cells byte-identical entering→landing (only used-by gained
  `, corpus/knowledge/counter-win-r77.md`); old→new logged in LOG.md Round 77 (S572
  `host-events-win-r63.md → …, counter-win-r77.md`; S574 `runway-win-r64.md → …,
  counter-win-r77.md`; S573 same form) — matches the observed diff.
- Census: `sources-census.sh validate --root <fleet root> mori` → rc 0 this closure; output
  = the tolerated 35-row W04 duplicate-URL class + 1 ok row (matches both committed census
  receipts' stated class).

### C2 (operability, capability acquisition — `tools/mori-counter-win.py`): NOT VERIFIED AS LANDED (re-measured)

The capability itself is REAL on this host — this closure ran it from the disk bytes:

- Disk sha256 of `tools/mori-counter-win.py` = `e6c527dbef07dbede0b963db1d68cbbbccdf0d148d0e9409b9a4514789ff7a1f`
  — exactly the sha the committed selftest receipt records as "the landing bytes". The
  receipts honestly describe the bytes they ran.
- `python -I tools/mori-counter-win.py --selftest` → `COUNTER_WIN_SELFTEST: PASS (12 cases)` rc 0 (12 PASS lines, re-derived).
- One live receipt re-run → `COUNTER_WIN: AVAILABLE surfaces=4 ok=4 unavailable=0 samples=2` rc 0 (4 counters read, redaction holds — no machine-name prefix, no timestamps in the counter lines).
- Read-only audit of the tool: the only child is `typeperf <4 counter paths> -sc 2` (no `-o`, no `-f`); the only writes are the selftest's temp fixture tree (removed on exit) — the declared write scope holds.
- Enumeration receipt matches: `typeperf -q Memory` fixed-string matches matched=4 rc 0.

But the INSTRUMENT DID NOT LAND:

- `git ls-tree -r 6a230c4b | grep counter-win` → only the two evidence receipts; NO
  `tools/mori-counter-win.py`.
- `git ls-tree refs/heads/master tools/` → no `mori-counter-win.py`; `git log --all --
  tools/mori-counter-win.py` → EMPTY (no commit on any local ref ever touched the path);
  `git rev-list --all --objects -- tools/mori-counter-win.py` → EMPTY. Remote `ls-remote`
  shows only `master` (this tip), an old ancestor branch (`devin/wiki-link`, 2026-10-17, 0
  counter-win paths), and an unfetched pull ref — the tool is committed NOWHERE.
- The report, LOG.md, SCORECARD and SHONEN all state the tool landed in the landing commit
  ("the landing commit 6a230c4b (21 paths, +2414/−7 … tools/mori-counter-win.py — NEW";
  "registered AT LANDING as registry row 12"; "selftest 12/12 ×3 at the landing bytes"). The
  actual landing commit carries 21 paths and the tool is NOT one of them — the report's path
  list totals 22 items. The lane's own foreign-sweep receipt had already listed
  `tools/mori-counter-win.py` as disk-only at 16:00:57Z and again inside
  "this_rounds_artifacts=14 (committed this round)" at 16:09:42Z; the landing commit was
  created at 16:26:12Z without the file. One `git cat-file -e 6a230c4b:tools/mori-counter-win.py`
  would have caught it.
- Per the protocol's landed-means-committed rule, the claimed after-state of C2 does not
  exist in committed bytes: a fresh clone cannot run the registered row-12 command.
- Second, independent defect in the same claim: **no canonical SCORECARD capabilities-table
  row.** Canonical capability-table headings (`grep -c 'Capability | What it can now do'`)
  are 26 → 26 entering→landing, and no counter-win row exists in any capabilities table
  (the only `^\| counter` row is the r61 `count-c3.py` boundary). The round prompt requires
  "its row enters the SCORECARD capabilities table in the same round"; the lane's own r75
  round backfilled the r74 capability row precisely because "the register the closures grade
  against did not match the demonstrated state" — the same class recurs here.
- What DID land for C2: the SKILL.md registry row 12 (family table 11 → 12 re-derived,
  tolerant form; SKILL 1351 → 1352 append-only with the entering 1327-line prefix sha
  `8e287544…` byte-identical; SKILL:905 `PASS (6 cases)` tally pin grep 1 at both revs),
  the three receipts, and the LOG/SCORECARD narrative. Registration is metadata; the
  instrument it registers is not in the tree.

### C3 (freshness — the standing pin-family arm extended to rows=5): VERIFIED MET (re-derived)

- This closure re-ran `python -I tools/mori-drift-recheck.py --root . --only S241,S581,S589,S590,S591`
  → `MORI_DRIFT_RECHECK rows=5 adjudicated=5 fresh=2 excerpt=0 time-churn=1 asset-churn=1
  receipt-open=0 receipt-stale=0 ua-serving=1 content-drift=0 gate=0 unavailable=0` rc 0 —
  every classification identical to the committed receipt (`pin-family-r77.txt`, window
  15:52:24Z..15:52:25Z; this re-run window 17:16:37Z..17:16:38Z).
- S591's first `ua-serving` classification: grounded in QUALITY criterion 159 ("per-response
  bot-manager chrome is serving variance, not content, and not a third grammar"); the r76
  anchor receipt (`s591-anchor-check-r76.txt`, PASS items=2 + able-to-fail FAIL rc 1) holds
  the pin's anchors; no supersedes row owed and none manufactured (SOURCES diff touches
  S591 not at all). Agree with the classification.
- Do-nothing control holds: the receipt is absent at entering (rc 128, controls receipt).

### Craft findings — VERIFIED

- Own misroot `output.csv`: absent from disk (`ls` → no such file), absent from the landing
  tree (`git ls-tree -r 6a230c4b | grep -c output.csv` → 0), provenance-proven in
  `foreign-sweep-r77.txt` (144 bytes, sha `beaab2ca…`, PDH-CSV header, one commit-gauge
  sample — the exploratory `-f csv`-without-`-o` argv writing to typeperf's default log
  file), disclosed and mined as lesson Mistake 1 (class: landing / unverified-cause
  attribution), and the docstring/K7/registry-row wording corrected BEFORE landing (the
  honest-unavailable arm retained). The correction-before-landing is real: the SKILL row's
  2-state text now attributes the empty-stdout shape to the misdirect, not a clock transient.
- The three r76 foreign receipt files (`source-s591-sweep-r76.txt`, `s591-source-r76.txt`,
  `win-family-live-r76.txt`): disk=YES, committed=NO (`git cat-file -e` rc ≠ 0 at
  `6a230c4b`), and every committed mention is disclosure/ruling-class (the r77 foreign-sweep
  receipt, LOG.md, the r76 closure's spotcheck, the r76/r77 lessons) — none rests a claim on
  their content. The leave-for-operator ruling stands, unchanged, as reported.
- The round's own sweep did flag the tool as disk-only (first sweep list, line
  `disk-only tools/mori-counter-win.py`) but then classified it under
  "this_rounds_artifacts=14 (committed this round)" — the one orphan its sweep caught and
  then mis-filed. Routed as D77-3.

### No axis harmed

- `git diff-tree -r -p 608815aa 6a230c4b -- SCORECARD.md` → pure append (+70/−0); the axes
  table rows byte-identical (no scalar moved; coverage 6, operability 7, depth 5, freshness
  5, calibration 5, adjacency 6).
- Append-only prefix proofs re-derived: LOG entering 4562 lines sha `e5f15163…` =
  landing first-4562 (now 4695); README 852 → 858 with entering sha `c84c0c92…` byte-identical;
  SCORECARD entering 3867 lines sha `27e57d41…` = landing first-3867 (now 3937); SKILL
  entering 1327 lines sha `8e287544…` byte-identical (1351 → 1352).
- PROVINCE.md, AGENTS.md, corpus/QUALITY.md and every previously registered instrument byte
  are absent from the round diff (name-status verified).

## Per-axis verdicts

| Axis | Verdict | Reason |
|---|---|---|
| depth | improved | C1 verified: new sourced ground (K1–K7) landed, S592 live-true byte-identical, anchors machine-verified with a discriminating able-to-fail arm, used-by appends contract-clean |
| coverage | unchanged | no claim targeted it; axes table byte-identical |
| operability | unprovable | C2's capability demonstrably runs from the disk bytes (selftest 12/12 rc 0, live rc 0 re-run by this closure) but the instrument is committed nowhere — the round's claimed after-state does not exist in committed bytes; per the closure contract a claim that cannot be re-opened in committed bytes grades `unprovable`, never `harmed` |
| freshness | improved | C3 re-derived exactly (rows=5, classifications identical, rc 0); S591 ua-serving per the standing QUALITY 159 grammar; the standing fetch rule honored (every live URL read from the registry row) |
| calibration | unchanged | no claim targeted it; the round's do-nothing controls and fresh-start re-derivations check out but move no scalar |
| adjacency | unchanged | detection-and-report boundary held (read-only probes verified by audit); foreign evidence disclosed, not absorbed |

## Spot-check table (discernment, checked from outside)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S592 typeperf reference — ADMIT (tier A, docs) | admit | live URL re-fetched this closure: byte-identical to the pin (sha `5f2e58ad…`, 50980 bytes), `<title>typeperf | Microsoft Learn</title>`, all 3 located quotes present | agree | official vendor documentation; tier A for the documented-command scope is right; the ≤25-word quotes (13/7/18 words) verify at their recorded lines; the duplicate-sweep interpretation is correct (S573 wevtutil / S572 exhaustion-troubleshooter are sibling pages, not this one) |
| Event-ID-41 kernel-power source row — REFUSED (ruled out, fresh-start item 3; the round's reject-shaped decision — the lesson's Gate records no rejects this round) | reject | grounds re-opened: S588 row present in SOURCES; `corpus/knowledge/boot-anchor-win-r73.md` carries K1–K4; the r76 closure notes rule the parallel unauthored Event-ID-41 plan leave-for-operator/reject-implicit | agree | a new row there would either restate already-held ground (S588 + r73 K1–K4) or rest the round on a foreign actor's plan — both bars the lane names are real |
| S591 classification `ua-serving` (first time) — adjudicated by the standing instrument, no manual registry edit | classify (not a reject) | re-derived live via `mori-drift-recheck --only …S591` → `ua-serving` reproduced; QUALITY 159 text re-read | agree | the classification follows the standing grammar; the pin is immutable and its r76 anchors hold; manufacturing a supersedes row would have been wrong and none was made |
| S592 row quote check (new SOURCES row re-opened per contract) | admit | live page: "command writes performance data to the command window or to a log file." / "Specifies the number of samples to collect." / "Display a list of installed counters (no instances). To list counters for one object, include the object name." each found exactly once; word counts 13/7/18 machine-verified by the anchor checker | agree | quotes are located, ≤25 words, and truthful to the live source |

## Trend verdicts

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | improved | one new admitted knowledge ground the lane did not hold (the Windows performance-counter surface), `source:` citing S592 opened and mined this round; SOURCES 364 → 365 re-counted; census rc 0. The repertoire-growth clause of the round's expansion narrative (registry row 12) landed as metadata only — the instrument and canonical capabilities row did not land (D77-1/D77-2); the trend's primary observable (admitted entry on uncovered ground citing a mined row) stands |
| quality | improved | corpus-side quality work landed and verifies: sourced entry with machine-verified anchors and an able-to-fail arm, census rc 0 both ends, append-only sha proofs on four carriers, five mistakes mined with class/evidence/captured-by/fix, a misattribution corrected before landing; no admitted entry failed its re-check. The capability clause of the round's quality narrative ("the capability runs and verifies … at the landing bytes") fails with C2 and is routed — it does not flip the corpus trend |
| discernment | improved | the round caught its own instrument-design misattribution in-round (the output.csv header) and corrected three carriers before landing; disclosed a first-run battery FAIL beside three PASS re-runs instead of overwriting it; refused a foreign-plan-shaped source row; left S591 to the standing grammar; routed around three open L0 lines (re-verified unanswered this closure — the L0 file ends at the round-73 line, no answers after it). This closure's spot-checks agree with all sampled decisions. The sweep's mis-filing of the unlanded tool as "committed" is a booking failure, named under D77-3, not a taste failure |

## Routed defects the lane must fix next round

- **D77-1 (decides the verdict; blocking for admission):** land `tools/mori-counter-win.py`
  at the receipted sha `e6c527dbef07dbede0b963db1d68cbbbccdf0d148d0e9409b9a4514789ff7a1f`
  as a NEW commit (corrections land as new commits, never an amend of `6a230c4b`); re-run
  the selftest + one live receipt AT THE LANDED BYTES and receipt them; a closure-correction
  may then re-grade C2. Until then the SKILL registry row 12 cites a command that does not
  resolve from committed bytes.
- **D77-2 (status-neutral, owed per the lane's own r75 precedent):** append the canonical
  4-column SCORECARD capabilities-table row for the counter-win probe (first-working round
  77) append-only at end-of-file; canonical capability-table headings are 26 → 26 across the
  round — the register the closures grade against does not match the demonstrated state, the
  exact class the r75 round discharged as its C1 claim.
- **D77-3 (status-neutral, report/log precision):** the report's landed-changes list and the
  LOG/SCORECARD/SHONEN r77 clauses state the tool landed in the 21-path landing commit; the
  commit's 21 paths exclude it (the list totals 22). The phrase "at the landing bytes" (selftest
  ×3) names bytes that never landed. A correction of record in the next round's own report/LOG
  entry (append-only, no r77 artifact edited) naming the true decomposition.
- Operator note (same as r76): all four SHONEN boxes are fully checkable by a non-author from
  committed bytes + receipts (this closure re-derived every box's substance); the boxes stay
  `[~]` under the protocol until the operator runs the `[x]` promotion review — the r76/r77
  spotcheck files are the non-author evidence pointers.

## Re-derivation inventory (commands this closure ran)

Conformance: `git log -1 -- .ufo/reports/round-77/mori.md` (identity); `git show
4e9ee125:.ufo/reports/round-77/mori.md | grep -n '## SHONEN'`; `merge-base --is-ancestor`
(608815aa, 6a230c4b, 986d4b46); `ls-remote origin refs/heads/master`; `git log
608815aa..6a230c4b` (1 commit); `diff-tree -r --name-status/--stat` (21 paths, +2414/−7);
`diff-tree -r -p -- SCORECARD.md` (pure append) and `-- SHONEN.md` (4 box rewrites, all
`[~]`). C1: `cat-file -e` before; K count 7; SOURCES 364/365; S592 pin sha256+bytes; live
curl re-open (byte-identical); `mori-anchor-check.py` 3-anchor PASS rc 0 + mislocation arm
FAIL rc 1; SOURCES column-level old/new comparison (status/opened/recheck untouched);
LOG old→new read. C2: `ls-tree -r` at 6a230c4b and master; `log --all` and `rev-list --all
--objects` for the tool path (empty); `ls-remote` (3 refs, none carries it); disk sha256 =
`e6c527db…`; selftest re-run 12/12 rc 0; live re-run rc 0 AVAILABLE surfaces=4; argv +
write-scope audit; family rows 11 → 12; SKILL 1351 → 1352 + prefix sha + SKILL:905 pin;
canonical capability headings 26 → 26. C3: `mori-drift-recheck.py --only
S241,S581,S589,S590,S591` re-run — identical classifications, rc 0; QUALITY 159 re-read.
Craft: `ls output.csv` (absent); `ls-tree | grep output.csv` (0); foreign files
disk/committed/citation-class check. Census: `sources-census.sh validate … mori` rc 0.
