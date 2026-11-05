author: hyaku closure (non-author integrator, @m_zfl)

# Round 96 — non-author verifier spot-check (hyaku closure, mori)

Verifier: hyaku closure judge, fresh non-author session, 2026-11-05. Report `.ufo/reports/round-96/mori.md`
(fleet commit `17fd4049`, author `mori-shokunin <mori@shokunin.local>`). Lane entering `66c5518e`, freeze
`b88c8ae8`, landing `9bde9322`, HEAD/pushed tip `167325885f0ca840f408b1a8bc15f981e170ea3e`. No lane-authored
file was edited by this check.

## 1. Conformance (PROTOCOL step 1)

- Report commit: `git log --format='%an %H' -- .ufo/reports/round-96/mori.md` (fleet repo) →
  `mori-shokunin <mori@shokunin.local> 17fd404951e230d3cb4ead77c3dc0788454dd4da` (2026-11-05 10:09:33 -0300,
  before the driver complete line 10:09:58). Lane identity ✓.
- `SHONEN` heading with one line per box: `## SHONEN` once (report line 75), four `[~]` lines; lane
  `SHONEN.md` has exactly 4 boxes; no `[x]` anywhere. ✓
- Cited hashes exist and are ancestors of the branch ref (`git merge-base --is-ancestor <h> master`, exit 0):
  `66c5518e`, `b88c8ae8`, `9bde9322`, `16732588`. Fleet L0 commit `0ddb53f7` exists, authored by the lane
  identity, +3 lines (the mori question now at `.ufo/l0-questions.md:355`). ✓
- Pushed, no leftovers: `scripts/hyaku/jj-lane.sh state mori-shokunin` → `branch=master local=16732588
  remote=16732588 ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` empty. ✓
- Driver digest (`.ufo/watchdog.log:2831,2846`) matches the dispatch record: launch
  `2026-11-05T09:11:40-03:00 attempt=1`, complete `2026-11-05T10:09:58-03:00 attempt=1`. ✓
- Prompt fidelity (read-only seat re-check): `templates/round-prompt.md` renders into
  `.ufo/prompts/mori-round-96.md` byte-identically except the schematic `<mori-repo>` → `mori-shokunin` fill;
  all operative items present — mission/axes binding; 1–3 falsifiable claims on distinct axes; lowest
  non-retired axis rule; L2 ≥8 in one batched call; commit-then-push; push scope; L0 side channel; report
  path+filename; report-lands-last; SHONEN heading; commit-hash citation; lane write scope — plus hyaku
  addendum §6. ✓
- Landed diff `66c5518e..16732588`: wave dir, `LOG.md` (+10 appended entry), `SCORECARD.md` (five
  Last-change cell rewrites + appended round-96 section only), `corpus/evidence/` pinned copies,
  `corpus/lessons/round-96.md`, `tools/mori-scorecard-calibration.py`. `SKILL.md`, `PROVINCE.md`,
  `corpus/QUALITY.md`, `corpus/README.md`, `corpus/knowledge/`, `corpus/SOURCES.md` untouched
  (`git diff --stat` empty). ✓
- Status: `ok` — real report, real committed work, no marker. Defects below are status-neutral.

## 2. Per-claim re-checks

Method: plain measurements over committed bytes run by this verifier; lane-owned gates NOT executed
(PROTOCOL §Gate standard, Closure consequence) — their committed receipts are the check.

### C1 (calibration) — re-measured by this verifier; predicate verified

Independent re-derivation, no lane tool executed: from fleet `MANIFEST.json` (1347 rounds entries; mori
`admitted=true` closures enumerated) the expected `Last change` lead per axis (the latest admitted mori
closure grading that axis improved/harmed): coverage **80** (r80), operability **93** (r93), depth **86**
(r86), freshness **82** (r82), calibration **93** (r93), adjacency **19** (r19). r94/r95 are rejected and do
not count; the single `closure-correction` row (r91) is admitted false.

Cells read from committed bytes (`git show <rev>:SCORECARD.md`, `## Axes` table):

| axis | expected | cell @66c5518e (before) | cell @16732588 (after) |
|---|---|---|---|
| coverage | round 80 improved | round 56 — mismatch | round 80 — ok |
| operability | round 93 | round 78 — mismatch | round 93 — ok |
| depth | round 86 | round 76 — mismatch | round 86 — ok |
| freshness | round 82 | round 78 — mismatch | round 82 — ok |
| calibration | round 93 | round 78 — mismatch | round 93 — ok |
| adjacency | round 19 | round 19 — ok | round 19 — ok |

Before = 5 mismatches, after = 0; the Score/Evidence columns are byte-identical at both revisions
(6/7/5/5/5/6). This matches the report and the committed receipts: `w1/calib/base-run.txt`
(`C1=unmet … mismatches=5 … rev=66c5518e239e`) and `evidence/landing-c1-new-counter.txt`
(`C1=met axes=6 mismatches=0 columns_unchanged=yes rows=6 rev=9bde9322d78a`). The frozen r79 counter
cross-check receipt (`evidence/landing-c1-frozen-r79-through95.txt`) reads `C2=met … mismatches=0 …
through=95` at the landing rev against `unmet mismatches=5` at entering with `--through 95` — the fix is
visible through the unamended instrument too. Gate evidence per §Gate standard: selftest receipt
`w1/calib/selftest.txt` (11 arms pass, `CALIB_SELFTEST pass=11 fail=0`, exit=0) and the verdict names its
revision. **Predicate verified.**

### C2 (freshness) — receipts verified + live re-open; predicate unmet (honest stop)

Committed receipts: `evidence/before-c2-digest.txt` = `DIGEST_CHECK rows=124 ok=86 mismatch=0 superseded=1
prefix_only=31 unpinned=6` (S125, S612, S615, S616, S622, S623 unpinned); `evidence/landing-c2-digest.txt` =
`… ok=89 … unpinned=3` (S615, S616, S623). Frozen P2 (`.ufo/waves/round-96/contract.md`): `unpinned=0
mismatch=0 ok=92 prefix_only=31` — **unmet**; the lane recorded the honest stop and did not rescope after
data.

This verifier's read-only seat re-opened all six rows live (2026-11-05 ~13:15–13:20 UTC): S125, S612, S622
live bytes hash exactly to the recorded digests, and the landed copies (`corpus/evidence/git-log-docs.html`,
`corpus/evidence/posix-shell-v3-chap02.html`, `corpus/evidence/.ufo/waves/round-25/capture/*`) are
byte-identical to the executor's staged `w1/digest/pinned/` set (`cmp`) and, for S125, to the sibling lane
originals (`cmp`, read-only). S615, S616, S623 live bytes differ from the recorded digests (docs.python.org
rebuild footer churn; S616 and S623 reproduce their recorded digests exactly under a footer-minute
substitution; S615's recorded digest matches no build and no file in the repo — the corruption round-91's
lesson C-1 already declared). `corpus/SOURCES.md` bytes unchanged across the round (diff empty) — no
in-place digest edit. Census re-run by this verifier: `scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin mori` → exit 0, final line `mori ok` (42 pre-existing W04 duplicate-URL
warnings). **Predicate unmet as frozen — honest stop agreed; no falsification.**

### No axis harmed

`git diff 66c5518e 16732588 -- SCORECARD.md` touches only the five `Last change` cells (the round's declared
correction) and appends the round-96 section; scores 6/7/5/5/5/6 unchanged; no SKILL/PROVINCE/knowledge/
QUALITY/SOURCES byte moved; `LOG.md` appended only. Owned pair coverage+operability unharmed. ✓

## 3. Per-axis verdicts (closure judge)

| Axis | Verdict | Reason |
|---|---|---|
| calibration | improved | C1 verified by independent re-derivation (§2); five cells now match the admitted MANIFEST record; score held 5, correctly not moved pending closure. |
| freshness | unchanged | Declared move P2 unmet (unpinned=3 ≠ 0, ok=89 ≠ 92). The partial progress is real and recorded (6→3, three byte-identical pins, three stale rows named with causes), but the frozen axis-move did not verify, so no admitted freshness move. Score held 5. Not harmed. |
| depth | unchanged | No depth work claimed; score unchanged. |
| coverage | unchanged | No coverage work claimed; score unchanged. |
| operability | unchanged | The new counter is a working instrument (selftest receipt green, 11/11) but no operability axis-move was claimed; score unchanged. |
| adjacency | unchanged | Sibling tsukuroi receipts pinned as evidence only; PROVINCE adjacency respected (report and lesson Gate). No absorption; not harmed. |

## 4. Discernment spot-check (LEARNING.md, from outside)

No new `corpus/SOURCES.md` row was written this round (diff empty), so the "re-open a newly written row"
duty is vacuous; the sample below re-opens this round's six `## Gate` decisions (3 admits, 3 rejects)
instead. Live re-open by this verifier's read-only seat, 2026-11-05.

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S622 git-log(1) | admit as pinned copy | `https://git-scm.com/docs/git-log` live: sha256 `f206647f…2f69b` = recorded; landed copy byte-identical | agree | Gate quote "Select only files that are Added ( A ), Copied ( C ), Deleted ( D ), Modified ( M ), Renamed ( R )" located in the pinned bytes (raw line 6732); ≤25 words; grounds `teaches` (`--diff-filter`, `%h`). |
| S612 POSIX 2.9.3 | admit as pinned copy | live: `0889867a…c1acd` = recorded; landed copy byte-identical (357,953 B) | agree | Gate quote "AND-OR list (see 2.9.3.1 Asynchronous AND-OR Lists ) executed from the current shell execution environment" located (tag-stripped 1385-1386, raw 2103). |
| S125 tsukuroi r25 receipts | admit as pinned copy | live: entry bytes `ecafdcdd…cd25`; receipt digests `e60f1bbc…` and `7adbe069…` both reproduce live; copies byte-identical to sibling originals (`cmp`, read-only) | agree | Evidence-only pin of sibling-owned bytes, not absorbed knowledge; PROVINCE adjacency respected. Nit: the Gate's "receipt head" quote is a whitespace-normalised join of `capture.txt` lines 2–4, not a literal single line. |
| S615 python ast | reject for pin (stale) | live 362,493 B, sha256 `d5d9d590…e65e8f` ≠ recorded `7891c588…`; no pinned copy | agree | The recorded digest matches no build and no file in the repo (round-91 lesson C-1 declared the corruption); pinning would require editing the recorded digest in place (CORPUS rule 2 forbids). Flip condition stated (supersession row or live-hash match). |
| S616 python tokenize | reject for pin (stale) | live 53,982 B, sha256 `bce32489…3da0e` ≠ recorded `6842ed0f…` | agree | Stale only by the docs.python.org rebuild footer minute (footer substitution reproduces the recorded digest exactly; the r90 copy is byte-true) — but under the frozen rule live ≠ recorded ⇒ cannot pin without an in-place edit. Reject correct; supersession/recheck ruling owed to the operator (L0 filed). |
| S623 python cmdline | reject for pin (stale) | live 171,073 B, sha256 `57b7f76b…` ≠ recorded `90ac3b25…` | agree | Same footer-minute story (recorded digest reproduces under a footer `08:02` substitution); no copy of that build exists anywhere in the repo. Reject correct under the frozen rule. |

Result: **agree 6/6** (three admits, three rejects). The lane's DigestRev subagent agreement is
lane-internal and does not count as the outside check; this table is it.

## 5. Trend verdicts (closure judge; evidence above)

- **expansion: unchanged** — no admitted `knowledge/` entry, no new registry row, no capability row
  (`git diff 66c5518e 16732588 -- corpus/knowledge/ corpus/SOURCES.md` empty; SCORECARD capabilities table
  untouched). Lane verdict agreed.
- **quality: improved (narrow)** — three registry rows re-verified against live bytes with byte-identical
  pins (S125, S612, S622); three stale rows named with footer-level causes and routed to an operator ruling,
  not silently left; no admitted entry failed a re-check. Lane verdict agreed.
- **discernment: improved** (lane self-graded unchanged pending this closure; closure grades improved) —
  this outside spot-check agrees with the gate on all six decisions (admits and rejects), and the round's
  disagreements (critic needs-amend on both predicates; the uncommanded r95 digest count) became lesson
  Mistakes 2/4/5 with evidence. LEARNING.md improved condition met.

## 6. Routed defects for round 97 (status-neutral)

1. **Unregistered gates.** `tools/mori-scorecard-calibration.py` (new this round) and
   `tools/mori-source-digest.py` have no registry row at the lane's registry home (`SKILL.md`: entry
   command, verdict map, selftest spelling, pinned-value path, write scope, owner). r95's routed item 1
   (the r95 battery gates) is still open too. §Gate standard Registry.
2. **Evidence-loss: `w2-validator.err` deleted before commit.** The w2 refusal (`too_few_lanes`, floor 8)
   survives only as prose in the report and lesson (both disclose "file since removed");
   `git log --all --diff-filter=A` finds no committed copy. Corroborated by
   `scripts/hyaku/ufo-wave-policy.json` (`minLanes: 8`) — but a primary artifact must be committed, not
   quoted.
3. **`w1-results.json` schema gap.** The file carries `name/agent/output/note` only — no `id`/`status`;
   settled state is inferable only from a non-empty `output`.
4. **Lab bookkeeping contradiction.** `w1/lab/Lab-digest-stability.md` labels S125 `falsified-no-match` by
   comparing the entry markdown (`ecafdcdd…`) against the receipt digest (`e60f1bbc…`), contradicting its
   own fetch table and the landing receipt (`S125 ok`). The stability demonstration itself (two fetches
   60 s apart, byte-stable per URL) is sound; the row label is not.
5. **Digest-tool supersession hole (self-disclosed).** `DigestExec.md` "Note for L1": a stale S615 copy
   would classify `superseded-by S619` and escape `mismatch=`. Fix or document before the next digest
   claim relies on `mismatch=`.
6. **Framing correction.** Registry rows = 399; "124 rows" is the digest tool's evaluated-row count, not
   the registry size (report prose and receipts use 124 consistently as the tool count; do not read it as
   the registry size).
7. **Carried debts.** Mutation sweep of the new counter (never run post-build; r97 planned) and the frozen
   r79 selftest survivors M2/M5/M6 (`w1/mut/MutCalib.md`); the frozen r79 counter's default bound still
   reads `met` (THROUGH=78) — retire it or pin `--through` in its registry row; stale digests
   S615/S616/S623 await the operator ruling (`.ufo/l0-questions.md:355`); D1 planner binding; r95 carried
   items m8/m10/m11 survivors and the dormant `census_path` arm. (r95's routed item 2, the literal
   `## Gate` heading, is discharged — this round's lesson carries `## Gate`.)

Operator note: all four SHONEN boxes carry `[~]` with resolvable pointers and no `[x]`; the boxes look
fully checkable by a non-author verifier (promotion review remains operator-owned).
