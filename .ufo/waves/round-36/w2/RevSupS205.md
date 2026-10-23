# RevSupS205 — S205 re-open (round 36, wave 2)

Item attacked: `corpus/SOURCES.md` row S205 (Shokunin Corpus Contract, SOURCES.md rules). Both round-36 claims (C1/C2) rest on this row.

## 1. Copy integrity: `corpus/evidence/sources-r36/S205.src` vs fetched pinned body

Command (fetch):
```
curl -fsSL https://raw.githubusercontent.com/VeigaPunk/shokunin/6a1dd8ce1a3165a25f9f2b774b21449e0d125c94/CORPUS.md \
  -o /fast/scratch/hyaku/mori-r36/RevSupS205-23/CORPUS.md
```

Observed:
```
sha256sum /fast/scratch/hyaku/mori-r36/RevSupS205-23/CORPUS.md
88556402940e7a0f1dbbed3abef9e00c87a90db6f80eaed03269e371f50050b8

sha256sum mori-shokunin/corpus/evidence/sources-r36/S205.src
88556402940e7a0f1dbbed3abef9e00c87a90db6f80eaed03269e371f50050b8

cmp mori-shokunin/corpus/evidence/sources-r36/S205.src \
    /fast/scratch/hyaku/mori-r36/RevSupS205-23/CORPUS.md && echo BYTES_IDENTICAL
BYTES_IDENTICAL
```

Result: **match** (sha256 equal, bytes identical).

## 2. Anchor lines 105-106, 116-118 carry the append-only rule and recheck contract the teaches cell asserts

Fetched body (`CORPUS.md`, fleet commit `6a1dd8ce1a3165a25f9f2b774b21449e0d125c94`), lines as read:

```
105: - `opened` — ISO date the row's author opened the source. `recheck` — ISO date or cadence
106:   (`90d`, `180d`, `on-release`).
116: 2. **Append-only.** Only `status`, `recheck` and `used-by` change in place, and each change
117:    is logged old→new in the round lesson. A correction is a new row whose `teaches` opens
118:    `supersedes S0NN —`.
```

Teaches cell (row at `bf0df77`, line 211):
> Rule 2 limits in-place changes to status, recheck and used-by; corrections are new rows whose teaches opens supersedes S0NN —. Recheck is an ISO date or cadence; no action on source changes is specified.

Mapping:
- "Rule 2 limits in-place changes to status, recheck and used-by" → line 116 ("Only `status`, `recheck` and `used-by` change in place") ✓
- "corrections are new rows whose teaches opens supersedes S0NN" → lines 117–118 ("A correction is a new row whose `teaches` opens `supersedes S0NN —`") ✓
- "Recheck is an ISO date or cadence" → lines 105–106 ("`recheck` — ISO date or cadence (`90d`, `180d`, `on-release`)") ✓
- "no action on source changes is specified" → verified by targeted scan of the whole fetched body for changed-source/action instructions (`grep -niE "source change|changed source|source changed|action (on|when)|when a source|if the source|update.*source|re-fetch|refetch"`): the only `recheck` occurrences are column definition/usage sites (lines 18, 86, 105, 116, 164, 169–170); none specifies an action on source changes ✓

## 3. Located quote ≤25 words, contiguous

Quote 1 (recorded w1/SrcCorpus.md, `CORPUS.md:116`):
> "Only `status`, `recheck` and `used-by` change in place, and each change is logged old→new in the round lesson."

Word count: **18** ≤ 25. Contiguity: present verbatim in fetched body (normalized across the 116→117 wrap), confirmed by `grep -o -F` on `tr '\n' ' '`-normalized body.

Quote 2 (recorded w1/SrcCorpus.md, `CORPUS.md:105-106`):
> "`recheck` — ISO date or cadence (`90d`, `180d`, `on-release`)."

Word count: **9** ≤ 25. Contiguity: present verbatim in fetched body (spans 105–106), confirmed the same way.

Minor location note (non-defect): quote 1's sentence physically spans lines 116–117 in the fetched body; the recorded location label says `:116` only. Content, contiguity and word count all hold; this is a citation-location precision nit, not a mismatch.

## 4. Tier A

Tier A definition (same fetched contract, `CORPUS.md:93-96`): "primary or authoritative for that scope (spec, official docs, source code, original paper, maintainer statement, the lane's own re-runnable gate output)". S205's source is the fleet's own pinned protocol contract (`Shokunin Corpus Contract`), i.e., authoritative for the SOURCES.md append-only/recheck-column rules. Tier A **holds**.

## Verification gaps / limits
- Fetched once over the network at verification time; sha256 is self-consistent with the pinned commit's body and the committed copy. No second host/ETag independent check was made.
- Quote word counts counted from the recorded quote strings, not from a re-loop of the w1 report's draft (draft text identical in `SrcCorpus.md`).

## VERDICT: PASS
No defect found in S205's anchored claims or in the copy identity. Both the append-only rule and the recheck contract asserted by the teaches cell are carried by the anchor lines 105-106 and 116-118 of the fetched pinned body; both located quotes are ≤25 words and contiguous; `corpus/evidence/sources-r36/S205.src` is byte-identical to the fetched body (sha256 `88556402940e7a0f1dbbed3abef9e00c87a90db6f80eaed03269e371f50050b8`). Row S205's tier A holds.
