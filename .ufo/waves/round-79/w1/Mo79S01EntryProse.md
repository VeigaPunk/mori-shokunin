# Mo79S01EntryProse — round 79 w1 C3 prose

## 1. Behavior and touched surfaces

Axes named by the frozen assignment: operability (C1), calibration (C2), freshness (C3). This seat supplies C3 prose only, not an axis verdict or an admission decision.

Wrote `corpus/knowledge/ua-serving-normative-r79.md`: title and teaching paragraph; separate S594 source / verified-at / recheck lines (2026-11-04, 365d); K1–K4 headings; Limits and Boundaries. Four single-line RFC spans carry pin-relative line numbers and measured word counts. The entry distinguishes RFC-defined conditional cache selection from unproven explanations of vendor behavior. It reads the historical round-78 receipts as historical evidence, without rerunning them.

Only authored surfaces: that knowledge entry and this report. Tool write results: entry initially 6208 bytes, then a provenance-only edit; this report written separately. No SOURCES/README/SCORECARD/receipt/instrument/fleet edits by this seat; no git mutation, fixture, installed tool, OS change or other runtime invocation.

## 2. What I read

Read `skill://godspeed`, the frozen round-79 contract, SCORECARD's axes table and end-of-file round-78 section, QUALITY 159/161/162/163, SKILL's registry at :1280–1330, `corpus/knowledge/counter-semantics-r78.md`, `corpus/knowledge/source-drift-hardening-r37.md`, and both `pin-family-r78.txt` and `pin-family-r78-final.txt`. Read operations are tool observations, not gate executions.

Historical final receipt bytes name S591/S592/S593 `ua-serving`, summary `rows=7 adjudicated=7 fresh=2 excerpt=0 time-churn=1 asset-churn=1 receipt-open=0 receipt-stale=0 ua-serving=3 content-drift=0 gate=0 unavailable=0 window=2026-11-02T18:40:57Z..2026-11-02T18:40:58Z`, `exit=0`. The initial receipt instead names S593 unavailable and discloses the URL-parser cause chain. These outputs belong to their original runs, not this seat.

## 3. Independent source opening: exact commands and output

Executed from `/home/vgpnk/Projects/shokunin`:

```sh
S=/fast/scratch/hyaku/mori-r79/Mo79S01EntryProse; mkdir -p "$S" && curl -sS https://www.rfc-editor.org/rfc/rfc9111.txt -o "$S/rfc9111.txt" && wc -lc "$S/rfc9111.txt" && grep -n "^4\.1\.\|^4\.1 " "$S/rfc9111.txt" | head -5
```

Output (rc 0):

```text
 1956 84477 /fast/scratch/hyaku/mori-r79/Mo79S01EntryProse/rfc9111.txt
526:4.1.  Calculating Cache Keys with the Vary Header Field
```

Read source lines :500–620 and exact :526–580 with the read tool. The source's normative sentence is wrapped across :528–534; entry quotes are contiguous single-line spans, never joined paraphrases.

Specialized grep over the scratch source used pattern `^4\.1\.|fields nominated|If multiple stored responses match|If no stored response matches`. Matching output used:

```text
477:   *  request header fields nominated by the stored response (if any)
526:4.1.  Calculating Cache Keys with the Vary Header Field
532:   fields nominated by that Vary field value match those fields in the
559:   If multiple stored responses match, the cache will need to choose one
576:   If no stored response matches, the cache cannot satisfy the presented
```

Then specialized grep over both scratch and the landed pin, :529–576, used this exact pattern:

```text
response and that stored response contains a Vary header field|fields nominated by that Vary field value match those fields in the|If multiple stored responses match, the cache will need to choose one|If no stored response matches, the cache cannot satisfy the presented
```

Both copies returned these same line-located matches:

```text
529:   response and that stored response contains a Vary header field
532:   fields nominated by that Vary field value match those fields in the
559:   If multiple stored responses match, the cache will need to choose one
576:   If no stored response matches, the cache cannot satisfy the presented
```

Executed exact word-count commands from this seat's scratch directory:

```sh
printf '%s\n' 'response and that stored response contains a Vary header field' | wc -w && printf '%s\n' 'fields nominated by that Vary field value match those fields in the' | wc -w && printf '%s\n' 'If multiple stored responses match, the cache will need to choose one' | wc -w && printf '%s\n' 'If no stored response matches, the cache cannot satisfy the presented' | wc -w
```

Output (rc 0):

```text
10
12
12
11
```

Executed independent-fetch/pin binding:

```sh
sha256sum /fast/scratch/hyaku/mori-r79/Mo79S01EntryProse/rfc9111.txt /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r79/rfc9111.txt && cmp /fast/scratch/hyaku/mori-r79/Mo79S01EntryProse/rfc9111.txt /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r79/rfc9111.txt
```

Output (rc 0, cmp silent):

```text
aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e  /fast/scratch/hyaku/mori-r79/Mo79S01EntryProse/rfc9111.txt
aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e  /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r79/rfc9111.txt
```

This verifies the quotes against the pinned bytes as required by QUALITY 162. It is not an execution of the anchor-checker tool or a committed-revision counter.

## 4. Findings and negative results

The normative text is narrower than an unconditional claim about the vendor: §4.1 addresses caches, stored responses containing Vary, matching request fields and revalidation. It does not explicitly mention User-Agent in that section, certify vendor response headers, prove the requests traversed a cache, or explain bot-management intent. Accordingly the entry's K2 uses conditional language, K3 retains standard adjudication, and Limits denies any new vendor/header/compliance/TTL proof. An adjudicated variant mismatch remains `ua-serving`; arbitrary cross-UA differences are not auto-classified.

Specialized grep for `S594|rfc9111|RFC 9111` in SOURCES returned `No matches found` at the time it ran; that was an observation of then-current working-tree bytes, not the entering-revision C3 control or a final census. An earlier pin lookup failed because the sibling had not written it yet; the later pin-specific grep/hash/cmp above resolved that prerequisite. No canonical claim counter, census, selftest, live drift probe, git revision check, final source-row/index check, or report gate was run by this seat. Main retains those gates; no pass is claimed.

## 5. Own defects and corrections

1. Initial commentary exposed verbose planning despite the requested direct-action posture. Subsequent work used direct tool calls; this does not change the evidence.
2. Initial shell discovery used `ls`, shell `grep` and `head` instead of the prescribed specialized filesystem/search tools. A basic-regex `grep -c '^\|\s*S59[0-9]\s*|'` printed `448`; that pattern did not measure registry rows and the number is INVALID, unused in the entry or any judgment. The same discovery command ended rc 1 on a missing pin. Specialized glob/grep replaced discovery, and the actual pinned-byte checks above provide the source evidence.
3. The cleanup trap was not attached to the original fetch shell. Before yielding I explicitly executed cleanup with an EXIT trap (below), so no scratch payload is intentionally retained.
4. My first provenance patch addressed line 8 rather than the intended line 6, briefly duplicating `verified-at:`. The edit response exposed both copies at :6/:8; the next surgical edit replaced :6 with the validated provenance and restored :8 to a blank. Final edit response shows exactly the separate source/verified-at/recheck trio at :5/:6/:7. No downstream check was run over the transient duplicate.

## 6. Cleanup and boundaries

Executed from the lane directory:

```sh
S=/fast/scratch/hyaku/mori-r79/Mo79S01EntryProse; trap 'rm -rf -- "$S"' EXIT; printf 'scratch-cleanup=%s\n' "$S"
```

Output (rc 0): `scratch-cleanup=/fast/scratch/hyaku/mori-r79/Mo79S01EntryProse`. EXIT executes the removal; no separate post-cleanup scan was run. No fixture repo was created. No tool install/update occurred.

Out of scope: C1 receipt guard, C2 axes cells, source-row/index/pin ownership, committed-revision admission and canonical Rust judgment. This prose neither closes the existing L0 boundaries nor remediates any host or vendor state.

## 7. Self-evaluation (not a gate)

Accuracy 4/5: pin hash/cmp and exact-line grep support all four quotes; vendor causation is explicitly unproven. Completeness 4/5: specified entry sections are authored; committed C3 integration belongs to Main. Clarity 4/5: mechanism, empirical history and inference limits are separated; conditional cache wording is necessarily narrower than the shorthand claim. Actionability 4/5: entry is at its integration target with pin-bound provenance; no canonical gate run is asserted. Conciseness 4/5: entry is one small text artifact, though repeated inference boundaries add length. Overall 4.0/5. Improvements: retain conditional wording in any integration summary; use only specialized discovery tools and observed line anchors in future edits. A reader requiring canonical admission should agree these are candidate prose/source checks, not admission evidence.

Artifacts: `corpus/knowledge/ua-serving-normative-r79.md`; `.ufo/waves/round-79/w1/Mo79S01EntryProse.md`. Sibling-owned pin consumed read-only: `corpus/evidence/sources-r79/rfc9111.txt`.
