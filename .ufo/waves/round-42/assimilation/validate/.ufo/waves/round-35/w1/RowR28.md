measured 2026-10-23T08:52:03Z
# Mori round 28 capabilities-register draft

## Rows

ROW: | rounds[476].capabilities_added[0] | SOURCES freshness repair | Supersedes eight listed defects with reopened S145–S152 rows, restores S096/S097/S101 to first-published cells, and repoints live readers; scope is freshness repair, no FR row advanced (MANIFEST.json:14312,14319; .ufo/reports/round-28/mori.md:20-23,68-75) | `corpus/SOURCES.md`, `corpus/knowledge/oom-victim-selection-r27.md` | 28 |
Why these paths: `corpus/SOURCES.md` contains the replacement rows, while the changed knowledge reader replaces old S127/S131 references with S148/S151; the spot-check identifies its remaining S127 mention as tsukuroi's row (corpus/SOURCES.md:151-158; corpus/knowledge/oom-victim-selection-r27.md:1,36-38,48-55,62-75; corpus/lessons/round-28-verifier-spotcheck.md:49-59).
VERDICT: supported

ROW: | rounds[476].capabilities_added[1] | A2 frozen-case regression | Fixture-only: pins ten round-26 A2 rules with 30 frozen cases; closure records a post-freeze PASS 30/30, not a live-host result [INFERENCE] (MANIFEST.json:14313,14319; .ufo/reports/round-28/mori.md:24-27,60; corpus/lessons/round-28-verifier-spotcheck.md:66-76) | `tools/fixtures/mori-oom-killers/cases-a2.json` | 28 |
Why this path: `tools/fixtures/mori-oom-killers/cases-a2.json` is the frozen case set itself; the closure names it and verifies 30 cases, three per A2-01–A2-10 rule (MANIFEST.json:14313,14319; corpus/lessons/round-28-verifier-spotcheck.md:66-75; tools/fixtures/mori-oom-killers/cases-a2.json:2-5).
VERDICT: supported

## Behavior, gates, and provenance

- The frozen manifest records both capabilities and identifies the non-author spot-check at `mori-shokunin/corpus/lessons/round-28-verifier-spotcheck.md@7118f320a5ef18d20c1e361eff77db0e1a97b2d6` (MANIFEST.json:14311-14321).
- `timeout 120 date -u +%FT%TZ` returned `2026-10-23T08:52:03Z`.
- `timeout 120 git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --name-status df886be1cc75f1052002698bdb4a3d18a2eaf6c6 1fc6bb0eaab40d9ea4fe996b64d140282b76337d -- corpus/SOURCES.md corpus/knowledge/oom-victim-selection-r27.md tools/fixtures/mori-oom-killers/cases-a2.json; timeout 120 git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD` returned `M corpus/SOURCES.md`, `M corpus/knowledge/oom-victim-selection-r27.md`, `A tools/fixtures/mori-oom-killers/cases-a2.json`, then lane tip `913df22e29f131ef9cb5de9dcb7e3e272256c5f0`. These are the selected changed surfaces between closures.
- `for p in corpus/SOURCES.md corpus/knowledge/oom-victim-selection-r27.md tools/fixtures/mori-oom-killers/cases-a2.json; do printf '%s ' "$p"; timeout 120 git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse 1fc6bb0eaab40d9ea4fe996b64d140282b76337d:"$p"; timeout 120 git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD:"$p"; done` resolved all three candidates. At closure and lane tip, the source registry blobs are `bae2e85249981dc81d441b3fa1b652da8f6d6435` and `ca2551e75f4e794b02fba4749d97ebf7fd246a61`; the knowledge-entry blob is `ffc91cd2af24318782a569c83b862cdbda0e8128` at both; the fixture blob is `7ba553d45e3b00d507e57132cc3c28fb140f83fd` at both. The later registry change does not erase its closure-time rows (SOURCES.md:151-158).
- `timeout 120 git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 1fc6bb0eaab40d9ea4fe996b64d140282b76337d:tools/fixtures/mori-oom-killers/cases-a2.json | jq -r '"count="+(.cases|length|tostring), (.cases[] | [.id,.rule,.expect.verdict] | @tsv)'` returned `count=30` and three cases each for A2-01 through A2-10. This inspected fixture data; it did not run the tool.
- The closure report states C1 `C1=met`, exit 0, with 8/8 superseding rows and zero live readers left; the closure spot-check calls the counter receipt evidence-verified, not executed by its reviewer (.ufo/reports/round-28/mori.md:59,62-64; corpus/lessons/round-28-verifier-spotcheck.md:49-60).
- The closure report records the first tool run after the C2 freeze as `PASS 30/30`, exit 0; the spot-check describes this self-test as evidence-verified, not executed by its reviewer (.ufo/reports/round-28/mori.md:24-27; corpus/lessons/round-28-verifier-spotcheck.md:71-76).

## Touched surfaces, limits, and out of scope

- Only this report is written: `.ufo/waves/round-35/w1/RowR28.md`. Candidate artifacts, manifest, and closure report were read-only.
- No counters, self-tests, or other checks were rerun by this seat. The two verdicts are supported by the closure record and spot-check, not independent execution here.
- C2 limits: one writer read 45 lines of the critic design before drafting, and the reported A2-07/A2-10 breach shapes have no frozen case; the closure discloses both limits (corpus/lessons/round-28-verifier-spotcheck.md:75-76,126-127).
- The fixture result does not establish live-host clearance [INFERENCE]. No tool install was needed.
- Artifact path: `.ufo/waves/round-35/w1/RowR28.md`.
