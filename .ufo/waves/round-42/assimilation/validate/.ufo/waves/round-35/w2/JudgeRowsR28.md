measured 2026-10-23T09:14:52Z

# JudgeRowsR28 — register rows for mori round 28 (keys `rounds[476].capabilities_added[0..1]`)

Scope: the two rows at `SCORECARD.md:1975` and `SCORECARD.md:1976` (final `## Capabilities` section) of the landed tip
`cedb0ec4f3a4f672804deac388b7191258f01fcd` in this lane. Rule under test, quoted from
`.ufo/waves/round-35/evidence/c1-controls.txt:41-44`: "(a) non-empty, closure-faithful capability and what cells and
(b) evidence cells holding only backticked paths". Item (c) pointer-relevance is outside the rule, reported separately.

Closure record used: fleet `MANIFEST.json@37b51a24` `rounds[476]` (capabilities_added strings, `verification.rechecks`,
`report`, `commit` fields), fleet `.ufo/reports/round-28/mori.md@37b51a24`, lane
`corpus/lessons/round-28-verifier-spotcheck.md@7118f320a5ef`. Artifacts opened at closure commit
`1fc6bb0eaab40d9ea4fe996b64d140282b76337d` (exists in lane; `git cat-file -e` rc=0).

Corroboration (not part of the rule): `timeout 280 python3 .ufo/waves/round-35/count-c1.py cedb0ec4…` prints
`row rounds[476].capabilities_added[0] matched`, `row rounds[476].capabilities_added[1] matched`, summary
`matched=18 … C1=met` exit 0.

## Row `rounds[476].capabilities_added[0]` — `SCORECARD.md:1975`

Cells: capability `SOURCES freshness repair`; what cell: "Superseded eight carried SOURCES row defects with re-opened
rows S145-S152, restored S096, S097 and S101 to their first-published cells, and repointed the live readers.";
evidence `` `corpus/SOURCES.md` ``, `` `corpus/knowledge/oom-victim-selection-r27.md` ``; round cell `28`.

(a) Non-empty, closure-faithful. Every fact is stated by the record and bounded as it bounds it:
- "eight carried SOURCES row defects … superseded by re-opened rows S145-S152" — MANIFEST `capabilities_added[0]`
  verbatim semantics; spotcheck §2 C1 table `spotcheck-lane.md:49-52` re-measures `superseding=8/8`.
- "restored S096, S097 and S101 to their first-published cells" — MANIFEST `capabilities_added[0]` ("S096/S097/S101
  restored to first-published cells"); report `mori.md:20` ("S096, S097, S101 restored to first-published cells");
  spotcheck `spotcheck-lane.md:50` (in-place restore, no other row touched).
- "repointed the live readers" — MANIFEST `capabilities_added[0]` ("live readers repointed"); report `mori.md:20-21`
  names the readers; spotcheck `spotcheck-lane.md:51` re-measures old-id cites 35→1 (the 1 is tsukuroi's S127,
  `spotcheck-lane.md:54-56`), `readers_left=0`.
- The cell claims nothing more (no verdict inflation, no extra artifacts). Bounded as the record bounds it.
(b) Evidence cell holds only backticked paths: two paths, both in backticks. Pass.

VERDICT: rounds[476].capabilities_added[0] supported

(c) Pointer relevance at `1fc6bb0e`:
- `corpus/SOURCES.md` — the artifact the repair acts on. At that commit rows `S145–S152` exist (file lines 151–158),
  each carrying `supersedes S096`/`S097`/`S101`/`S127`/`S128`/`S129`/`S131`/`S140` respectively; the round diff
  `git diff 6ebd518f 1fc6bb0e -- corpus/SOURCES.md` is `11 insertions, 3 deletions`, the only removed/added row lines
  being the S096/S097/S101 restore pair and the eight added S145–S152 rows. Demonstrates THIS capability.
- `corpus/knowledge/oom-victim-selection-r27.md` — a repointed live reader, i.e. the third clause of the same
  capability. In the same diff it swaps `S127→S148`, `S128→S149`, `S129→S150` (five `-`/`+` id-bearing lines observed);
  its retained `S127` at line ~204 names tsukuroi's row per `spotcheck-lane.md:54-56`. It is not a
  capability_added[1] artifact. Demonstrates THIS capability, not another of round 28.

VERDICT: rounds[476].capabilities_added[0] pointer-relevance holds

## Row `rounds[476].capabilities_added[1]` — `SCORECARD.md:1976`

Cells: capability `amendment-A2 frozen cases`; what cell: "Pins ten round-26 amendment-A2 rules of the OOM killer read
with 30 frozen cases (freeze d21b8bd3), PASS 30/30; fixture-only, not a live-host result."; evidence
`` `tools/fixtures/mori-oom-killers/cases-a2.json` ``; round cell `28`.

(a) Non-empty, closure-faithful. Facts vs record:
- "ten round-26 amendment-A2 rules" — MANIFEST `capabilities_added[1]` ("ten round-26 amendment-A2 rules"); report
  `mori.md:9-10` (C2 pins the ten round-26 A2 rules, re-declared, r27 withdrew it).
- "of the OOM killer read" for `tools/mori-oom-killers.py` — mild paraphrase of the tool path the MANIFEST string
  names; no fact added. [INFERENCE: "read" = what the tool reads; fair shorthand, not a new claim.]
- "30 frozen cases (freeze d21b8bd3), PASS 30/30" — MANIFEST `capabilities_added[1]` verbatim; spotcheck
  `spotcheck-lane.md:66-74` re-measures 3 cases per rule A2-01..A2-10, freeze commit `d21b8bd` never edited after,
  counter `7b75f45` committed before it, tool diff empty, `PASS 30/30`.
- "fixture-only, not a live-host result" — bounds the claim inside what the record bounds: the record's PASS is the
  frozen-fixture self-test (`spotcheck-lane.md:71-74`, `evidence/c2-freeze-selftest.txt`), never a live-host run.
  This narrows, does not extend. Faithful.
(b) Evidence cell: one path, backticked. Pass.

VERDICT: rounds[476].capabilities_added[1] supported

(c) Pointer relevance at `1fc6bb0e`: `tools/fixtures/mori-oom-killers/cases-a2.json` is the artifact MANIFEST names in
the capability string itself. At that commit it parses as JSON with exactly 30 objects bearing a `rule` field,
3 each for `A2-01` … `A2-10` (counted); the round diff shows it is the single freeze-commit file for C2. It
implements/demonstrates THIS capability (the frozen cases), not the C1 repair of the same round.

VERDICT: rounds[476].capabilities_added[1] pointer-relevance holds

## Notes / residuals

- Round cell `28` equals the MANIFEST `round`/`lane_rounds.mori` (28) on both rows.
- Both evidence paths changed inside the round window `6ebd518f..1fc6bb0e` (`git diff --name-only`: all three cited
  paths present) and appear as whole paths in the closure record (`cases-a2.json` in `capabilities_added[1]` and
  `spotcheck-lane.md:66`; `corpus/SOURCES.md` at `spotcheck-lane.md:49-50`; `oom-victim-selection-r27.md` at
  `spotcheck-lane.md:54` and `mori.md:129`).
- Tooling directive: no installs or updates performed; none needed.
- Scratch: `/fast/scratch/hyaku/mori-r35/JudgeRowsR28/` (scorecard, MANIFEST, report, spotcheck, closure-commit file
  copies). No lane or fleet writes made; only read-only git (`show`, `diff`, `cat-file`, `log`).
