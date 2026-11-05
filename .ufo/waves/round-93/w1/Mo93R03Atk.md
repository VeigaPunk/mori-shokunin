# Mo93R03Atk — attack on the calibration claim C1 itself (round 93 w1)

Seat: Mo93R03Atk, reviewer. Lane never written except this Report; no git/jj mutation against
the lane. Scratch `/fast/scratch/hyaku/mori-r93/Mo93R03Atk` (clone at patch base `6d82b8d7…`,
branch `seat`; `git rev-parse --show-toplevel` printed the scratch path before fixture work).
Frozen reads at `6d82b8d7…` via `git show 6d82b8d7:<path>`. No tool installed or
upgraded. Checks run are listed at the end; one named check was not run and says so.
## 1. Canonical wording vs the round-92 admission-commit rule
Canonical `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/LEARNING.md:69`:
`corpus/knowledge/<slug>.md — opens with source:, verified-at: (commit or date) and recheck:`.
The word "admission" appears nowhere in the canonical protocol (`grep -rn "admission commit"
…/protocol/*.md` → 0 hits).
Lane criterion 194 at `6d82b8d7` = `corpus/QUALITY.md:2249`: "A knowledge entry opens, within
its first 12 lines, with `source:`, `verified-at:` and `recheck:` lines. The frozen counter
measures presence only … **the truth of each line is a non-author check**." The admission-commit
requirement is **not** in QUALITY 194; it enters as round 92's own frozen landing constraint
(`.ufo/waves/round-92/contract.md:36`, at `699f6276`): "…names the admission commit of
the file (`git log --diff-filter=A`)"), restated in the lesson sentence at
`corpus/lessons/round-92.md:51-52`; the round-92 spotcheck confirms the split
(`…verifier-spotcheck.md:46-48` — 7 of 19 admission-commit form, 12 date/round form; D1 at `:104`).
**Verdict (1): the round-92 rule is the lane's own stricter criterion, not a conflict with the
canonical wording** — LEARNING.md:69 allows "(commit or date)", so the twelve date-form lines
were canonically valid and only violate the lane's round-92 self-imposed tightening. QUALITY
194 deliberately defers the truth check to the non-author closure — this report.
**Coverage finding (new):** the lesson sentence says "each `verified-at`" with no scope limit.
Census at `6d82b8d7`: of the 98 entries under `corpus/knowledge/`, only **7** carry the
admission-commit form (exactly audit-r11, progressing-weak-r2, silence-grading-r2,
silence-cutover-r3, verdict-machine-r4/r5/r6); the other **91 stay date-form** after the
round-93 repair (touching only the 12 trio files). Per-file classification is committed at
`.ufo/waves/round-93/evidence/c1-derive-entering.txt` (98 rows: 91 `MISMATCH`, 7 `OK`). So
after the repair the sentence is true for the 19 trio files only — **7/98 of the corpus** —
and if the appended round-92 correction does not carry the 19-file scope explicitly, the
sentence remains false as written.
## 2. Data repair: calibration move or bookkeeping?
The frozen counter operationalizes one sentence (`count-c1.py:14-16` at `6d82b8d7`):
"`claim_r92_true=1` is the round-92 lesson's claim … it holds iff `adm_fail == 0`". Repair
shape (`contract.md:53-56`): `verified-at: <admission-short-hash> (<original value, unchanged>)`
in 12 files.
**Case for calibration.** AXES.md:15 (`/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/AXES.md:15`) defines calibration
as "self-assessment quality: gaps named honestly, confidence graded, overreach caught", signal
"SHONEN.md/SCORECARD entries match observed repo state". Lane precedent round 50: criterion 134 (`corpus/QUALITY.md:1178-1199`) — a
self-assessment "reconciled with the fleet record and with the instruments" where SCORECARD
`## Axes` cells named rounds 26/31/31/25 against fleet `MANIFEST.json` 47/47/49/49; the fix
edited the self-assessment to match the observed record and landed as calibration
(`SCORECARD.md:21-29`). Round-93 C1 is the same class of reconciliation, with data ordered to
match the asserted state. Under that reading the repair *is* a calibration move.
**Case for bookkeeping.** Round 50 moved the self-assessment to match the *instruments*;
round 93 moves the *data* to match one sentence of one lesson. Nothing outside that sentence
and the frozen counter reads these 12 values: no QUALITY criterion (194 checks presence only),
no registry row, no gate. The original values' truth-promise was never broken: the 12 lines
are round-written date forms that were only *moved* into the 12-line window by seat Mo92K02Trio
(`.ufo/waves/round-92/w1/Mo92K02Trio.md:8-19`, 4 files; the date-form values are carried
byte-identical in `.ufo/waves/round-92/w1/patches/Mo92K02Trio.patch:70-140`). The repair
changes **where** a historically-true value sits, not what it says. That is bookkeeping.
**Observable defect the repair introduces (the real risk).** After the repair, `verified-at:`
certifies the file's *admission* commit, not the commit where its *current content* was
settled. `git diff --quiet <admission> 7b3fe9d5 -- <file>` shows **all 12** blobs changed
between admission and the entering revision (e.g. workstate-win-r71's r72 append-only
correction at `d2f55d8c`; execution-binding-r89's r89 body delta of 132 lines at `ab48dbec`;
surfaces-r8's r9 disposition block at `cffb37ef`). The contract names this limit
(§C1 "Named limit") but does not quantify it: the round-93 `verified-at` gains a hash that
certifies a state 1–3 revisions older than the claims it anchors. Admission-commit-form is
*harder to misuse* (it identifies a revision) but *less true as an anchor* for these 12 bodies.
**Single verifier question that decides it:** *does the round-92 sentence state a norm for the
value-form of `verified-at` (type-level), or only that the 19 trio files' values contain their
admission hash (token-level)?* Type-level → genuine calibration step, but the correction must
carry the 19-file scope and the stale-anchor limit. Token-level → bookkeeping dressed as
calibration: the instrument set acquired no new truth-checking power, and the same frozen
presence-style logic decides.
**Recommendation (this seat, not a ruling):** treat as **bookkeeping with a calibration
side-effect**, admitted only if (a) the appended round-92 correction carries the 19-file
scope, (b) a dated erratum records that the admission hash is *not* the content-settling
commit for these 12 bodies, and (c) the round-93 lesson adds a QUALITY criterion defining
what a `verified-at:` value may contain going forward. Failing (a)–(c), C1 should report
`met as frozen; calibration not established`, matching the round-92 C1 precedent
(`SCORECARD.md:4715`).
## 3. Is the appended round-92 lesson correction a self-assessment mismatch?
AXES.md:15's calibration signal is *"SHONEN.md/SCORECARD entries match observed repo state"*.
The round-92 sentence is **lesson prose**, not a SHONEN.md box or SCORECARD `## Axes` entry;
the round-49/50/79 calibration closures (`SCORECARD.md:14`;
`corpus/lessons/round-49-verifier-spotcheck.md:40-55`; `…round-50…:66-89`) all graded
calibration against SHONEN/SCORECARD pins, never lesson prose. So the false sentence is a
self-assessment mismatch in spirit but not in the definition's letters. Its canonical home is
**discernment**: `LEARNING.md:35` — "the spot-check agrees with the gate on admits *and*
rejects, **or a disagreement becomes a lesson that adds a grounded QUALITY.md criterion**".
The round-92 spotcheck already registered the disagreement
(`…spotcheck.md:100`: the false sentence "routed as D1"). The appended correction plus a new
QUALITY criterion is exactly that closure.
**Verdict (3):** the correction is **not** a calibration-axis self-assessment mismatch under
AXES.md:15's letters; it is a discernment-axis event (spot-check disagreement → lesson →
criterion) that the round-92 spotcheck set up and round 93 is discharging. It becomes
calibration-relevant only if the wave also updates SHONEN.md or `SCORECARD.md ## Axes`; as
dispatched, no seat touches those files, so no calibration *cell* moves. Calibration credit
for C1 must be earned by a SCORECARD entry, not by the append.
## 4. Exact sentence and file:line the non-author closure should check
Primary sentence: **`corpus/lessons/round-92.md:51-52`** at `6d82b8d7` — "Each `verified-at`
names the admission commit of its file (`git log --diff-filter=A`)". After the round-93
landing the closure must:
1. Re-run `python3 -I .ufo/waves/round-93/count-c1.py <landing> --repo <lane-clone>` and
   independently re-derive the 19 admission hashes with `git log --diff-filter=A --format=%h
   7b3fe9d5… -- <file> | tail -1` (counter method at `count-c1.py:86-90`). The counter's check
   is substring-in-line, so a mutated hash is invisible to it — the re-derivation is the check.
2. Verify the round-92 correction **is an append, not an in-place edit**:
   `git diff <entering> <landing> -- corpus/lessons/round-92.md` shows appended lines only
   (lines 1–110 byte-unchanged). An in-place edit of lines 51-52 would violate
   `corpus/SOURCES.md:211` (S205, CORPUS rule 2: only `status`, `recheck`, `used-by` change in
   place) — the same rule contract premise P3 relies on (contract.md:23-29).
3. Verify the correction carries the 19-file scope (§1 coverage) and the stale-anchor erratum
   (§2 defect); without both, the sentence still reads falsely universal and the stale-revision
   risk is undisclosed.
4. Verify the sentence agrees word-for-word across its committed copies round-93 forward:
   `corpus/lessons/round-92.md:51-52`, the contract §C1 opener (contract.md:37) and
   `count-c1.py:14-16` — the contract commits to that equivalence (contract.md:39-41); a
   divergence is a settlement failure.
Secondary: `corpus/QUALITY.md:2249` (194's "truth of each line is a non-author check" is this
closure's own authority — cite it) and `SCORECARD.md:4711-4716` (round-92 record, "met as
frozen; presence"), which round-93 must not rewrite in place.
## Checks run
- `git show 6d82b8d7:corpus/QUALITY.md` sed-reads for criterion 194 (`:2249`) and round-50
  criterion 134 (`:1178-1199`); `git log --diff-filter=A` admissions of corpus/QUALITY.md
  (`ec0664e1`) and corpus/lessons/round-92.md (`9dce2ca6`).
- `python3 -I .ufo/waves/round-93/count-c1.py 7b3fe9d540c98b8b0390a0f9bbe78de4341092a5 --repo
  <scratch-clone> --report` → `C1_REPORT rev=7b3fe9d540c9 trio=98 claim_r92_true=0 files=19
  adm_ok=7 adm_fail=12 patched12=0/12 seven_same=7/7 census_rc=0` — reproduces the committed
  entering receipt `.ufo/waves/round-93/evidence/measure-c1-entering.txt`. Also run at
  `6d82b8d7…`: `C1=unmet trio=98 claim_r92_true=0 … adm_ok=7 adm_fail=12 … census=ok
  checks_failed=admission,patched12`.
- Admission-hash vs verified-at census over all 98 entries in the scratch clone at the
  entering tree → 7 `OK`, 91 date-form; matches `evidence/c1-derive-entering.txt` exactly.
- Blob-state per file (`git diff --quiet <admission> 7b3fe9d5 -- <file>`): all 12 differ from
  their admission-commit state; per-file responsible commits enumerated in §2.
- Sample re-derivations: `git show 2360cc3b:corpus/knowledge/counter-semantics-r78.md`,
  `git show 9dce2ca6 -- corpus/knowledge/drift-pin-r10.md` / `…workstate-win-r71.md` /
  `…counter-semantics-r78.md` — confirming (a) the date-form value predates the round-92
  landing and (b) the landing moved it into the 12-line window without changing its text.
- Frozen-constraint origin: `git show 699f6276 -- .ufo/waves/round-92/contract.md:36`; lesson
  sentence `corpus/lessons/round-92.md:51-52`; spotcheck `…round-92-verifier-spotcheck.md:
  46-48,100,104`; patches audit: `Mo92K01Trio.patch` 2 admission-commit + 8 date-form lines,
  `Mo92K02Trio.patch` 5 admission-commit + 8 date-form lines.
- `git log -S"admission commit"` pickaxe over lane history — the phrase originates with the
  round-92 frozen contract `699f6276` (earlier hits are round-3..5 drafts and unrelated
  collisions), confirming the rule is lane-minted, not canonical.
- Sensitivity fixture `gi43/` in scratch: 12 rewritten entries where each `verified-at:` line
  carries the correctly-derived admission hash but sits at line ~51 outside the 12-line window.
  Census of the mixed tree: `trio=86` (equal to the committed deletion-control delta); the
  frozen counter cannot be pointed at a working-tree fixture, so the compare is by the
  counter's own trio method — its line-12 window is load-bearing and this is recorded, not
  defeated.
- **Not run (named):** no post-landing execution — the landing revision does not exist yet, so
  §4 step 1 and the leaf-member bound (no subagent dispatched) close this seat.
