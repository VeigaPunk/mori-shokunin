measured 2026-10-23T12:09:03Z

# Round 36 source-corpus finding

## Provenance and behavior
- Re-opened the pinned public source from the requested URL with:
  `timeout 120s sh -c 'mkdir -p /fast/scratch/hyaku/mori-r36/SrcCorpus && curl --fail --location --silent --show-error --max-time 90 https://raw.githubusercontent.com/VeigaPunk/shokunin/6a1dd8ce1a3165a25f9f2b774b21449e0d125c94/CORPUS.md --output /fast/scratch/hyaku/mori-r36/SrcCorpus/S205.src && sha256sum /fast/scratch/hyaku/mori-r36/SrcCorpus/S205.src'`
  Result: `88556402940e7a0f1dbbed3abef9e00c87a90db6f80eaed03269e371f50050b8  /fast/scratch/hyaku/mori-r36/SrcCorpus/S205.src`.
- Append-only rule 2 is at `CORPUS.md:116-118`; the `recheck` definition is at `CORPUS.md:105-106`. The correction clause says corrections are new rows whose teaches opens with the supersedes marker (`CORPUS.md:117-118`).
- Quotes, each under 25 words:
  1. “Only `status`, `recheck` and `used-by` change in place, and each change is logged old→new in the round lesson.” (`CORPUS.md:116`)
  2. “`recheck` — ISO date or cadence (`90d`, `180d`, `on-release`).” (`CORPUS.md:105-106`)
- A targeted scan of the saved source for changed-source/recheck instructions returned `No matches found`; this contract defines the column value but does not specify an action when the source changes.
- `VERDICT: admit — pinned official fleet protocol text, tier A for the SOURCES append-only and recheck-column claims.`

## Drafts for L1

```DRAFT corpus/SOURCES.md
| S205 | Shokunin Corpus Contract, SOURCES.md rules — https://raw.githubusercontent.com/VeigaPunk/shokunin/6a1dd8ce1a3165a25f9f2b774b21449e0d125c94/CORPUS.md | docs | A | SOURCES.md append-only rule and recheck column contract | CORPUS.md:105-106,116-118; fleet commit 6a1dd8ce1a3165a25f9f2b774b21449e0d125c94 | Rule 2 limits in-place changes to status, recheck and used-by; corrections are new rows whose teaches opens supersedes S0NN —. Recheck is an ISO date or cadence; no action on source changes is specified. | mined | 2026-10-23 | on-release | tools/mori-source-drift.py |
```

```DRAFT corpus/lessons/round-36.md § Gate
- S205 — https://raw.githubusercontent.com/VeigaPunk/shokunin/6a1dd8ce1a3165a25f9f2b774b21449e0d125c94/CORPUS.md; accessed 2026-10-23; sha256 88556402940e7a0f1dbbed3abef9e00c87a90db6f80eaed03269e371f50050b8. Quote: “Only `status`, `recheck` and `used-by` change in place, and each change is logged old→new in the round lesson.” (CORPUS.md:116). Quote: “`recheck` — ISO date or cadence (`90d`, `180d`, `on-release`).” (CORPUS.md:105-106). The correction clause is at CORPUS.md:117-118; no changed-source action is specified. Decision: admit, tier A.
```

## Gates and touched surfaces
- Scratch source copy: `/fast/scratch/hyaku/mori-r36/SrcCorpus/S205.src` (sha256 above). Draft registry copy: `/fast/scratch/hyaku/mori-r36/SrcCorpus/validate-root/mori-shokunin/corpus/SOURCES.md`; draft row is line 211 there. The lane registry itself was not edited; S199 is the model row at `corpus/SOURCES.md:205` and the header is at line 5.
- Manual row count: `timeout 120s gawk -F'|' '$0 ~ /S205/ { print "NF=" NF " cells=" NF-2; n++ } END { if (n != 1) exit 1 }' /fast/scratch/hyaku/mori-r36/SrcCorpus/validate-root/mori-shokunin/corpus/SOURCES.md` → `NF=13 cells=11`.
- Ran `timeout 120s /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /fast/scratch/hyaku/mori-r36/SrcCorpus/validate-root --today 2026-10-23 /fast/scratch/hyaku/mori-r36/SrcCorpus/validate-root/mori-shokunin`. It emitted existing W04 duplicate-URL warnings and `mori-shokunin E11 S205 missing used-by tools/mori-source-drift.py`, then exited 1. E11 is the validator's missing-used-by-path finding (`scripts/sources-census.sh:24-30`). Search of the lane `tools` directory for `mori-source-drift.py` returned no matches at inspection time; the draft's required used-by path is not yet present in this checkout.
- Only this report was written in the lane. Scratch files are confined to `/fast/scratch/hyaku/mori-r36/SrcCorpus/`. No tool installs/updates, counter runs, builds, tests, or product-code edits were made.

## Findings and limits
- The requested row and lesson Gate wording are drafts only; the census reports the absent tool path, so the `mined` row is not yet cleanly valid against this checkout.
- This is protocol-source evidence only. No verdict is offered on C1/C2 behavior, the drift-tool implementation, or the append-only gate implementation.
