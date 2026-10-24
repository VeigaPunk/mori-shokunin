measured 2026-10-23T08:51:54Z
# S200 frontier source: fleet MANIFEST.json

## Findings
- Read the frozen snapshot with `ulimit -v 1048576; timeout 120 git -C /home/vgpnk/Projects/shokunin show 37b51a243302e8009c7067431e8a47f9a722fd14:MANIFEST.json`. The raw display was elided by the reader; filtered queries below returned the counts and selected fields.
- Counter behavior (`mori-shokunin/.ufo/waves/round-35/count-c1.py:103-131`): select `rounds` entries with `lane == "mori"`; only `admitted is True` entries with non-empty `capabilities_added` add oracle rows. Each capability is keyed by `rounds[i].capabilities_added[j]`; `round`, `commit`, `verification`, and `report` populate/ground that record. The counter serializes `verification`, resolves its spot-check paths and the fleet `report` (`:114-125`), and checks the evidence paths (`:128-131`, `:153-185`).
- Command outcome: `admitted_mori_entries=13 capabilities=18`. Per-round capability counts: r12=1, r14=1, r15=1, r16=1, r18=3, r19=1, r21=0, r22=1, r24=2, r25=2, r26=1, r28=2, r31=2. The printed summary also returned each admitted record's `report`, `commit`, and `verification` keys; all 13 records had those fields. This count was from a jq query over the pinned manifest, not a run of the C1 counter.
- Exact quote from `MANIFEST.json@37b51a243302e8009c7067431e8a47f9a722fd14`, JSON path `rounds[313].capabilities_added[0]` (round 12): “sources-registry (34 rows; census clean)” (5 words). The focused `git show … | jq -r '.rounds[313] | {round,lane,admitted,capabilities_added,report,commit,verification}'` output returned that value and the listed fields.
- Source-path rules: `CORPUS.md:129` bars credential material, session or private URLs, and `op://`; it does not bar repository paths. The source-cell rule explicitly allows a repo path or command for own-work (`CORPUS.md:90`). This is a pinned fleet-repository path, not a URL, and is allowed on that reading. [INFERENCE] The contract does not explicitly state whether the own-work path exception requires `kind=own-work`; this draft uses the requested `kind=dataset` for the first-party ledger.
- ID sequencing caveat: `CORPUS.md:89` requires the next unused ID. The observed `corpus/SOURCES.md:204-206` ends at S198 before `## Paths`; S199 was not present in the read snapshot. S200 is retained below as assigned, but should not land before S199 is accounted for.

VERDICT: admit — the pinned fleet ledger is primary evidence for the requested scope, and its admitted mori entries contain 18 capability strings.

## DRAFT SOURCES S200
```DRAFT SOURCES S200
| S200 | fleet MANIFEST.json rounds ledger — /home/vgpnk/Projects/shokunin/MANIFEST.json@37b51a24 | dataset | A | which mori rounds a non-author closure admitted and which capabilities it recorded | `MANIFEST.json@37b51a243302e8009c7067431e8a47f9a722fd14`; `rounds[*].lane`, `.round`, `.admitted`, `.capabilities_added`, `.commit`, `.verification`, `.report` | The fleet ledger records which mori rounds were admitted and which capabilities each admitted closure recorded. | mined | 2026-10-23 | per-closure | SCORECARD.md |
```

## DRAFT Gate S200
```DRAFT Gate S200
| S200 | `git -C /home/vgpnk/Projects/shokunin show 37b51a243302e8009c7067431e8a47f9a722fd14:MANIFEST.json` | 2026-10-23 | — | `rounds[313].capabilities_added[0]` (5 words): “sources-registry (34 rows; census clean)” | admit, pinned first-party closure ledger grounds the requested scope |
```

## Gates, surfaces, and limits
- Gate: source opened read-only at the pinned fleet commit; quote and location above. No C1 counter, test, build, or other gate was run; no install/update occurred.
- Read-only inputs: fleet `MANIFEST.json@37b51a24`; fleet `/home/vgpnk/Projects/shokunin/CORPUS.md:86-129`; lane `.ufo/waves/round-35/count-c1.py:1-23,103-185`; lane `corpus/SOURCES.md:5-6,204-206`; lane `corpus/lessons/round-34.md:9-27` (Gate format). The lane root listing showed `SCORECARD.md` present.
- Only written surface: this report, `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/w1/SrcManifest.md`. No product files, registry, SCORECARD, manifest, Git/JJ state, or other repo paths were written.
- Out of scope: landing S200, resolving the S199 sequence, executing the frozen counter, and judging the full C1 register.
