measured 2026-10-23T09:16:21Z

# JudgeRowsR16 — mori round 16 register row (key `rounds[353].capabilities_added[0]`)

Method: read-only `git show`/`git cat-file` byte reads only; nothing executed, nothing written to the lane
except this file. No `lsp` device answers these objects (markdown/JSON), so line citations are from
git-show byte reads, with `grep -n` used only to locate lines inside them. Scratch dir created and unused:
`/fast/scratch/hyaku/mori-r35/MoriR35.JudgeRowsR16/`. No tools installed or updated; no pacman transaction
(paused host-wide); no network access. Objects judged: `SCORECARD.md` at lane `cedb0ec4`, final
`## Capabilities` section (heading line 1941, row line 1964); `MANIFEST.json` at fleet `37b51a24` JSON path
`.rounds[353]`; fleet report `.ufo/reports/round-16/mori.md` at `37b51a24` (the MANIFEST element's
`report` field names exactly this path); verification object
`corpus/lessons/round-16-verifier-spotcheck.md` at closure commit `24526ea9617cd020fee16c28fe4d4a2789dc28cb`.

## Ground-truth record

- MANIFEST `.rounds[353]` (`git show 37b51a24:MANIFEST.json | jq '.rounds[353]'`): `round:16`,
  `lane:mori`, `lane_round:16`, `admitted:true`, `verdict:admitted`,
  `report:".ufo/reports/round-16/mori.md"`, `capabilities_added` length 1 (index `[0]` is the only
  capability of this closure, so this row is the whole landed set for round 16).
- `.rounds[353].capabilities_added[0]` verbatim: `exact-start journal record window: read one explicit
  user/system scope after a byte-equal retained anchor cursor on the anchor's boot, MESSAGE-free, refusing
  nearest-seek/foreign-boot/unsafe captures as unavailable without advancing cursor state (finite 64-case
  fixtures + anchor-only live user/system observations)`.
- Register contract the row answers: `SCORECARD.md@cedb0ec`:1944-1946 — one row per capability a
  non-author closure admitted as `MANIFEST.json@37b51a24` records it; key is the closure's
  `rounds[i].capabilities_added[j]`; first-working round is the closure's round; evidence is the artifact
  that round landed and the closure names.
- Closure decision: spotcheck:11 `status: ok · admitted: true · verdict: admitted`; spotcheck:6-7 records
  the reviewer executed no gate/selftest/probe/live query — static re-counts only.
- Claim and measured result: spotcheck:81-82 — before manifest 64 `capability_absent`, after manifest 64
  `match`/64 ok, `inputs_moved=False`, start hashes == end hashes; spotcheck:90 recounts unmet 64→0
  (capability acquisition, not 64 reproduced defects). Live receipts: spotcheck:115 — exit0 each,
  `records_after_anchor:0`, all four positive subsets 0; spotcheck:118 — anchor-only captures, not positive
  live load. Report:5 declares bounded, read-only, MESSAGE-free observation after an exact retained anchor
  for one explicit scope and the anchor's boot; report:7 lists the tool behaviours; report:11 states the
  live runs were anchor-only with 0 after-anchor records.

## Row under judgment (SCORECARD.md@cedb0ec:1964)

- key: `rounds[353].capabilities_added[0]`
- capability: `exact-start journal record window`
- what: `Reads one user or system journal scope after a byte-equal retained anchor cursor on the anchor's
  boot, MESSAGE-free, refusing unsafe captures as unavailable without advancing cursor state; 64/64
  fixtures; live runs were anchor-only.`
- evidence: `tools/mori-journal-window.py`
- first-working round: `16`

## (a) Closure faithfulness — sentence by sentence

Every cell fact is stated by the record and bounded as the record bounds it:

- `exact-start journal record window` — verbatim capability name, `.rounds[353].capabilities_added[0]`:
  `exact-start journal record window:`.
- `Reads one user or system journal scope` — record `one explicit user/system scope`; report:7 `fixed
  single-scope argv`. Same one-scope bound; no plural/complete-coverage claim.
- `after a byte-equal retained anchor cursor` — record `byte-equal retained anchor cursor` (verbatim);
  report:7 `exact first-record cursor/boot acceptance`; spotcheck:142 — outside-verifier admit that the
  first record is dropped only on exact cursor+boot equality.
- `on the anchor's boot` — record `on the anchor's boot` (verbatim); spotcheck:99 shows
  `anchor_record_foreign_boot` → `UNAVAILABLE anchor-boot-mismatch`.
- `MESSAGE-free` — record `MESSAGE-free` (verbatim); report:5; spotcheck:88 — 0 of 61 recorded argv files
  carry a `MESSAGE` output field.
- `refusing unsafe captures as unavailable` — record `refusing nearest-seek/foreign-boot/unsafe captures
  as unavailable`; spotcheck:99; tool@24526ea lines 447-483. The row names only the `unsafe` class of the
  three the record enumerates — a narrowing of the enumeration, not an added or widened fact; every
  refusal fact stated is stated by the record.
- `without advancing cursor state` — record `without advancing cursor state` (verbatim); report:7 `cursor
  state is never advanced`; spotcheck:82 `inputs_moved=False`, start hashes == end hashes.
- `64/64 fixtures` — record `(finite 64-case fixtures …)`; spotcheck:82 `64 cases all match, 64 ok`;
  spotcheck:90 unmet 64→0; report c1-count (report:39-42 region, after manifest all-match). Bounded
  exactly as the record bounds it: fixture count, not a live or exhaustive claim.
- `live runs were anchor-only` — record `anchor-only live user/system observations`; spotcheck:115
  `records_after_anchor:0`; spotcheck:118 anchor-only captures, no no-event or positive-load conclusion.
- `first-working round` cell `16` — record `round:16`, `lane_round:16`.

All five cells non-empty; key matches MANIFEST index `[0]` of the admitted closure element. No cell fact
is absent from the record; no bound is looser than the record's.

## (b) Evidence cell

`tools/mori-journal-window.py` is the cell's entire content: exactly one backticked path, no prose, no
non-path tokens. Clause (b) holds only-backticked-paths.

## (c) Pointer relevance at closure commit `24526ea9617cd020fee16c28fe4d4a2789dc28cb`

The cited artifact resolves and is this capability's implementation, not another round-16 artifact:

- `git show 24526ea…:tools/mori-journal-window.py | sha256sum` =
  `d61e0d220a1825d738e2b9526b2bdd92047e39a4543d0ca0a040795d84ba0aeb` — identical at `87a57c1` (measured
  inputs) and `9de05bd` (delivered HEAD), matching the SHA the closure recorded (spotcheck:86).
- Implements THIS capability: tool:2 docstring `bounded MESSAGE-free same-boot journal window probe`;
  tool:12 non-anchor first record is `anchor-not-first-record` and never deletion/vacuum proof;
  tool:47 `OUTPUT_FIELDS` excludes `MESSAGE`; tool:310/312 refusal reasons `anchor-not-first-record` and
  `anchor-boot-mismatch` (nearest-seek and foreign-boot refused as unavailable); tool:441 query uses
  `--cursor=`; tool:447-483 `overflow`/`stderr-nonempty`/`timeout`/`rc-nonzero` all return
  `MORI_JOURNAL_WINDOW_UNAVAILABLE`; tool:352 `records_after_anchor`; tool:40-41 UNAVAILABLE/SETUP
  findings. Spotcheck:101-102 independently confirms `--after-cursor` appears only in a forbidden list
  and `--cursor=` is the query construction.
- Not another capability of the round: the round-16 sibling artifacts are distinct paths
  (`tools/mori-round16-regressions.py` report:42, `tools/mori-round16-context-check.py` spotcheck:218);
  the pointer names the probe itself, which is what the record's `capabilities_added[0]` describes.

VERDICT: rounds[353].capabilities_added[0] supported
VERDICT: rounds[353].capabilities_added[0] pointer-relevance holds

## Residual risk and verification gaps

- The row's what-cell drops two detail qualifiers the record carries: it enumerates only `unsafe` of the
  `nearest-seek/foreign-boot/unsafe` refusal classes, and omits `explicit`/`bounded`/`read-only`
  (report:5). This contracts detail inside the row; it introduces no overclaim, so (a) still holds. Flag
  to MoriR35 for optional tightening, not as a defect.
- Judgments (a) and (b) are static byte reads only; I executed no probe, gate, selftest or live query
  (consistent with the closure's own static method, spotcheck:6-7). The closure's executed measurement is
  the spotcheck's static re-count (spotcheck:81-82, 90).
- The C1 counter `count-c1.py` was not run; this seat's scope is row judging, not the counter predicate.
- Identity check is by SHA-256 of the cited path at three revisions (output above); same-identity
  rerouting for this pointer holds for the bytes inspected.
