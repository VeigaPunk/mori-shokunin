# Vary-selected representations: grounding the ua-serving class (round 79)

A changed body at one URL is not, by itself, evidence that the source's content changed. RFC 9111 §4.1 makes request-header matching part of cache selection when a stored response names those fields in Vary. This grounds the distinction the lane already makes empirically for S591/S592/S593: compare the same served variant before interpreting byte drift. The RFC supplies the cache-selection mechanism, not proof of why those particular vendor responses differed.

source: S594 — https://www.rfc-editor.org/rfc/rfc9111.txt, RFC 9111 §4.1; pin `corpus/evidence/sources-r79/rfc9111.txt`, sha256 `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e` (84477 bytes, 1956 lines).
verified-at: 2026-11-04 — independently opened the RFC text; `sha256sum` and `cmp` bound that fetch byte-for-byte to the pin (rc 0). Pinned-copy grep located all four spans below at their named lines; `wc -w` measured their counts.
recheck: 365d

Provenance (each quote is a contiguous verbatim span on ONE line of the RFC pin, not a joined sentence; each is below 25 words):

| Anchor in rfc9111.txt | Verbatim quote | wc -w |
|---|---|---|
| :529 | response and that stored response contains a Vary header field | 10 |
| :532 | fields nominated by that Vary field value match those fields in the | 12 |
| :559 | If multiple stored responses match, the cache will need to choose one | 12 |
| :576 | If no stored response matches, the cache cannot satisfy the presented | 11 |

The operative sentence spans :528–534: absent revalidation, a cache MUST NOT reuse the stored response unless the request fields nominated by its Vary value match the original request's fields. The short spans above locate that sentence and the subsequent selection branches without pretending a wrapped fragment is a complete sentence.

## K1 — The response names the selecting request fields

Vary is carried by the stored response; its value nominates the request-header fields whose matching matters for reuse. RFC 9111 §4.1 (:528–534) therefore distinguishes stored responses for the same target by more than URL alone. Matching permits the normalization listed at :536–550; an absent field only matches another absence (:552–554), and a Vary member of `*` never matches (:556–557). Where several stored responses match, the cache chooses among them (:559–565); where none matches, it cannot satisfy the request from those stored responses (:576–579). This is a conditional cache rule, not a claim that every origin varies on User-Agent.

## K2 — A User-Agent byte difference need not be content drift

If a response nominates User-Agent in Vary, changing that request field can select a different representation. A byte difference between two User-Agent fetches of the same URL is therefore compatible with legitimate representation selection; it does not establish content drift by itself. Applying this mechanism to the lane's observed UA-associated differences is an interpretation, not evidence that the vendor emitted that header.

The empirical ground remains the round-78 receipts, not an experiment repeated here: `.ufo/waves/round-78/evidence/pin-family-r78.txt` records S591/S592 as `ua-serving` and S593 initially `unavailable`; its disclosed cause chain identifies URL parsing, not a serving-policy diagnosis. After the encoded-URL accommodation, `.ufo/waves/round-78/evidence/pin-family-r78-final.txt` records S591/S592/S593 `ua-serving`, `ua-serving=3 content-drift=0 unavailable=0`, exit 0, with window `2026-11-02T18:40:57Z..2026-11-02T18:40:58Z`. Those are historical observations, not today's fetch window or a timing series.

## K3 — Adjudicate before assigning a class

A first-fetch byte mismatch still requires the standing drift adjudication, including the pinning-UA comparison and the vendor-scoped grammars of QUALITY 159. Neither the URL alone nor a change of client identity decides the class. A same-variant difference may still need `time-churn`, `asset-churn`, `content-drift`, or another established disposition; an unavailable response remains unavailable. Existing adjudication and semantic review stay in force. The vendor's bot-management intent, policy, implementation and correctness are not the lane's to infer from two bodies or from this RFC.

## K4 — Compare variant to variant, or pin per client

Read a byte comparison against the variant captured by its pin: compare variant to variant, or keep separate pins per client when the serving variants cannot be compared as one. An adjudicated variant mismatch is `ua-serving`, never `content-drift` merely because the cross-variant bytes differ. This reader rule does not automatically label every cross-UA mismatch `ua-serving`; K3's standard adjudication remains the prerequisite. It adds no third churn grammar and never normalizes away unclassified bytes.

## Limits

RFC 9111 §4.1 governs cache reuse and matching, not a vendor's origin-side negotiation or bot-management algorithm. It does not specifically name User-Agent in this section and does not prove that S591/S592/S593 emitted `Vary: User-Agent`, traversed a cache, complied with the RFC, or held identical underlying content. No response-header capture or new vendor fetch was performed for this entry. A cache-selection mechanism supports the distinction; it cannot certify the cause of a historical byte delta. The historical receipts preserve their own fetch moments, and establish no rotation TTL, persistence interval or vendor-wide guarantee (QUALITY 161).

## Boundaries

Detection and report only. This entry changes no instrument, registry row, immutable pin, churn grammar, threshold, OS state or vendor policy. It gives no remediation, cache-configuration or bot-evasion instruction. It deepens the source-drift interpretation already taught by `corpus/knowledge/source-drift-hardening-r37.md` (byte non-reproducibility is not automatically a changed taught claim) and QUALITY 159; it neither enlarges the census surface roster nor closes an instrument-change authorization boundary. S594's registry row, source pin and README index are integrated separately; their presence and the committed C3 predicate are not established by this prose alone.
