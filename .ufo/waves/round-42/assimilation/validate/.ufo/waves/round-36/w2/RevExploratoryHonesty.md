# w2 RevExploratoryHonesty — exploratory-claim honesty sweep (C1 freshness overreach)

Seat: `mori-r36-w2-RevExploratoryHonesty-23` (reviewer, leaf; no subagent dispatch).
Item attacked: any sentence in the round's artifacts that presents C1's byte result as a freshness admission,
a verified-stale-facts claim, or an axis score move. Rule under test: with no named non-author reviewer, the
only admissible C1 outcome is `unprovable`; artifacts must state that rule or name the missing reviewer condition.

Canonical runtime: Python 3.14.8, git backend, lane HEAD = `bf0df77fee4b6ef54a90aea09335c7617f125151`
(landed/pushed data tip). Read-only commands only; no lane file edited by this seat. LSP unavailable
(`read xd://lsp` → no such tool). Scratch: none needed (no code written).

## Method

1. Read the four artifact groups in full or by targeted ranges: `SKILL.md`, `corpus/QUALITY.md`,
   `corpus/knowledge/source-drift-r36.md`, `.ufo/waves/round-36/` (contract.md, evidence/, c0/,
   w1/ reports, w2/ reports, dispatch-log.txt, w1/w2 spec/dispatch JSON).
2. Pattern greps over those roots: `fresh|stale|admis|verdict|unprovable|reviewer|proven|verified`,
   plus lane-wide admission phrasings (`proven fresh|verified fresh|established freshness|admitted fresh|
   freshness (is|was) (proven|established|admitted|verified)|proves freshness|verifies freshness|
   stale (facts|source|skills)|admit.{0,30}fresh|fresh.{0,30}admit`).
3. Verified the **landed bytes** (`git show bf0df77:<path>`), because the worktree carries uncommitted
   edits (measured below) — a live-file read alone would miss the pushed artifact's wording.

## Findings by severity

### F1 — MEDIUM: the landed contract's C1 claim row is a freshness overreach (contract.md:13 at bf0df77)

The pushed tip's claim table still describes C1 as flagging stale rows, with an unqualified `C1=met` after-state:

Command: `git show bf0df77:.ufo/waves/round-36/contract.md | sed -n '13p'`
Observed:
```
| C1 | freshness (lowest-scoring non-retired axis, tied at 5 with depth and calibration) — surface: a new lane tool `tools/mori-source-drift.py`, a new operation (re-fetch each SOURCES row that has a committed copy and classify it against that copy) | flags stale source rows: `fresh`, `excerpt`, `drifted`, `unavailable`, `no-copy` per row | `count-c1.py 6bd57097` → `C1=unmet` (tool absent) | `count-c1.py <landed tip>` → `C1=met` |
```

- The capability cell asserts the probe **flags stale source rows** — a semantic freshness/staleness claim the
  byte classifier cannot carry (w1/CritAxisFit.md; contract.md:117-120 itself says the classifier "certifies
  representation differences, not stale skill claims").
- The after cell is a plain `C1=met` with no "byte-behavior evidence only / unprovable" qualifier; the qualifier
  lives only in the appended declaration section (contract.md:114-125), not in the claim row. The frozen claim
  table and the declaration are internally contradictory at the tip.
- This is exactly the sentence class this sweep targets. It is the *landed* artifact: `git diff 5842dc0
  bf0df77 -- .ufo/waves/round-36/contract.md` is empty, so bf0df77 carries the pre-declaration row unchanged
  (the declaration commit 5842dc0 appended lines 114-125 without amending row 13).
- Sibling seat RevContractSizing (w2) independently flagged this same row; its quote matches the tip blob.

**Worktree note (measured):** the live worktree already carries an **uncommitted** edit that rewrites row 13 to
"no freshness verdict is admitted from it … `drifted` is a representation mismatch, not a stale-source verdict
… else lands `unprovable`":
`git status --porcelain` → ` M .ufo/waves/round-36/contract.md`; `git diff HEAD -- …contract.md` shows exactly
that one-line replacement. So a reader of the live file no longer sees the overreach, but the **pushed tip still
contains it** (HEAD is still bf0df77). The index-clean gate (staged=0 intent_to_add=0) holds because the edit is
unstaged; it would break the C1 real-arm `corpus/`-clean check only if it were under `corpus/` (it is not).

### F2 — LOW (adjacent, not a freshness admission): stale "seven drifted rows" enumeration at the tip

The tip knowledge note, QUALITY 105 and SKILL.md describe the drifted set as seven rows (S156–S160, S176, S177)
while the same tip's receipt and the live probe measure nine (adds S210, S211):
- `corpus/knowledge/source-drift-r36.md:16-19` (tip blob = worktree): "the seven `drifted` rows were …".
- `corpus/QUALITY.md:840-842`: "all seven real drifted rows were representation differences …".
- `SKILL.md:860`: names only "annotated excerpts (round 30, S156–S160) and rebuilt doc pages (S176, S177)".
Contradicted by `evidence/c1-after.txt:3` (`oracle_drifted=9`) and by the live probe (`drifted=9`, ids S210/S211).
This is a stale-documentation defect (already reported by ExecDriftLive / ExecReC1A / RevC1Interface), not an
overreach: these sentences *deny* staleness rather than admitting freshness. Recorded for completeness only.

### F3 — INFO: worktree `corpus/README.md:565` (uncommitted, concurrent seat) over-characterizes nine rows

The uncommitted "Round-36 coverage additions" table claims "on 2026-10-23 all 9 oracle-drifted rows were
representation differences (annotated excerpts S156–S160, docs.python.org build footers S176/S177), not changed
sources" — it says 9 but enumerates only 7 ids, and for S211 (per-request `ncbi_phid`/`csrfmiddlewaretoken`
nonce, byte-unstable across three fetches) the "representation difference, not changed source" characterization is
unproven (ExecReC1A §4). It does explicitly add "no freshness verdict is claimed from it", so it is not a
freshness admission; it overstates the blanket "representation difference" claim on the other side. Uncommitted;
the pushed tip's README does not contain it.

## Verified clean (the sweep's main territory)

No other sentence in the four artifact groups presents C1's byte result as freshness/verified-stale/axis-score.
The standing texts actively disclaim:

- `SKILL.md:859-861`: "Read `drifted` as 'the copy is not reproducible from today's body', never as a changed
  source …". `SKILL.md:872` verdict map: "0 `drifted=0` (rows may be `unavailable` or `no-copy`; not proof
  every URL was reachable)".
- `corpus/QUALITY.md:104-105`: "A green fixture or sibling gate never establishes drift freshness"; "A green C1
  fixture gate does not establish freshness." `QUALITY.md:837-843` (105) requires the what-changed check before a
  drift witness is used as a target.
- `corpus/knowledge/source-drift-r36.md:5` titles the note "(round 36, C1 — exploratory)"; `:11-13` "a probe,
  not a gate"; `:15` "`fresh` proves only byte identity with the committed copy, never that the row's `teaches`
  is right"; `:16` "That is not the same as a changed source".
- `evidence/c1-after.txt` is pure frozen-counter output (P-C1 line + blind/real counts + `C1=met` as the
  predicate's verdict token + seed); no prose. `dispatch-log.txt:19,28-31` labels the landing "C1 byte-evidence
  met".
- `contract.md:114-125` (declaration) is the operative rule: "It verifies only as `unprovable-but-better` with a
  named non-author reviewer; otherwise it lands `unprovable`. P-C1 is still run and reported as evidence of the
  probe's byte behaviour, not as C1's verdict."
- w1: `CritAxisFit.md` ("do not infer freshness admission solely from C1=met"; "describing these results as
  verified stale facts would also overstate calibration"), `DraftSkillRows.md` ("even an all-unavailable run can
  exit 0 and cannot establish freshness").
- w2 reports: `RevC1Receipt.md` §7 ("no wording … asserts a freshness/axis verdict"), `RevC1Interface.md`
  ("no freshness-admission claim was found in these surfaces"), `ExecDriftLive.md` §8 (dedicated admission scan),
  `RevDebtR35.md`, `RevPredIdentity.md`, `RevQuality105.md` ("No inference of freshness admission from C1 is made
  anywhere in this item").

**Named non-author reviewer:** none. All `reviewer` occurrences are wave-internal seat roles; no artifact names a
non-author party satisfying the contract's condition, and none claims `unprovable-but-better` as achieved. The
artifacts state the conditional rule (contract.md:13-after/124-125; w2-spec/taskcall/dispatch context: "C1 admits
NO freshness verdict; it verifies only as unprovable-but-better with a named non-author reviewer, else lands
unprovable"; ScribeLesson spec: "verdict unprovable pending named non-author reviewer"). The admissible status at
the tip is therefore `unprovable`, and nothing claims more — except the row-13 wording of F1.

## Residual risk and verification gaps

- The after-receipts (`evidence/c1-after.txt`, `c2-after.txt`) are untracked at the tip; their bytes are pinned
  only by local hash (peers' findings). This does not affect the text sweep.
- Worktree vs tip divergence (contract.md, knowledge note, corpus/README.md, dispatch-log.txt modified
  uncommitted): reviewers reading live files see corrected text; the pushed tip is the artifact under judgment.
- The lane-wide admission-pattern grep is pattern-limited; the semantic read covered SKILL.md Round36, QUALITY
  103-105 + 105, the knowledge note, contract.md, and all w1/w2 report files.

## VERDICT: FAIL

Defect path:line evidence:
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/contract.md:13` at landed tip
  `bf0df77` (git blob): capability cell "**flags stale source rows**: `fresh`, `excerpt`, `drifted`,
  `unavailable`, `no-copy` per row"; after cell "`count-c1.py <landed tip>` → `C1=met`" with no
  byte-evidence-only/unprovable qualifier. Conflicts with the same file's declaration at `:117-125`.
  (The worktree already carries an uncommitted repair of this row; the pushed tip does not.)

Item attacked: exploratory-claim honesty — the landed C1 claim row is a freshness overreach; all other scanned
surfaces hold the `unprovable` line.
