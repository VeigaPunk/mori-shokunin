# S041 scope review

## Axes
- Source fidelity: distinguish the RFC's text from conclusions drawn for Mori.
- Lane-boundary clarity: explicitly label application as lane doctrine.
- Minimality: preserve every existing cell word except the needed declaration.

## Finding
The routed, unadjudicated S041 concern is real: the teaches cell's second assertion is not stated by RFC 6585 and is not labeled as lane doctrine. The scope cell is a direct description of the page. Proposed repair: insert `lane rule: ` before the existing second clause; change no other wording.

## Cell audit
The frozen base row (`git show 7d382043:corpus/SOURCES.md`, row 47) and current `corpus/SOURCES.md:47` have identical S041 scope and teaches cells.

Scope cell: `HTTP 429 Too Many Requests status meaning`

- No lane inference/application found. The committed copy labels section 4 `429 Too Many Requests` (`corpus/evidence/recheck-r32/S041.src:243`); its next lines define the status (`:245-246`).

Teaches cell: `HTTP 429 denotes too many requests in a time window; it does not identify a vendor business error or establish permanent seat death.`

1. `HTTP 429 denotes too many requests in a time window` — sourced. The committed copy states, “The 429 status code indicates that the user has sent too many requests in a given amount of time” (`corpus/evidence/recheck-r32/S041.src:245-246`). This supports the row's first clause.
2. `it does not identify a vendor business error` — lane inference, not stated by the cited page. The recheck row's quote that the specification does not define how the origin server identifies users or counts requests (`corpus/lessons/round-32.md:31`) does not state a vendor business-error rule.
3. `or establish permanent seat death` — lane application, not stated by the page. RFC 6585 §4 discusses HTTP status semantics, not Mori seats or their permanence (`corpus/evidence/recheck-r32/S041.src:243-250`).

The two unsupported assertions form the teaches cell's second clause. Make that whole clause explicit lane doctrine rather than attributing it to the RFC.

## Old and proposed cells

Old scope:
```text
HTTP 429 Too Many Requests status meaning
```

Proposed scope (unchanged):
```text
HTTP 429 Too Many Requests status meaning
```

Old teaches:
```text
HTTP 429 denotes too many requests in a time window; it does not identify a vendor business error or establish permanent seat death.
```

Proposed teaches:
```text
HTTP 429 denotes too many requests in a time window; lane rule: it does not identify a vendor business error or establish permanent seat death.
```

Old → new diff:
```diff
 HTTP 429 denotes too many requests in a time window;
-it does not identify a vendor business error or establish permanent seat death.
+lane rule: it does not identify a vendor business error or establish permanent seat death.
```

## Basis and limits
- Recheck evidence lists three RFC quotes for S041: the 429 meaning, the unspecified origin-server user identification/request count, and optional Retry-After (`corpus/lessons/round-32.md:31`). Only the first directly supports a current cell assertion.
- The closure note records CriticScopingRows' S041 finding as unadjudicated and recommends declaring lane application or sourcing it (`corpus/lessons/round-32-verifier-spotcheck.md:100-104,190-192`). The comparison rows make that distinction explicit: S073 says the containment rule is Mori's own tool rule, S074 says the observe-only boundary is the lane's own, and S076 labels the census interpretation as the lane's own application (`corpus/SOURCES.md:79-82`).
- Read-only provenance command: `timeout 120 git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 7d382043:corpus/SOURCES.md`. Its output contains the S041 row at line 47; that row matches current `corpus/SOURCES.md:47`.
- Touched surface: this report only. No source registry, lesson, evidence copy, or knowledge entry was changed. No counter, build, test, lint, or formatter was run; no external URL was fetched. This is a scoped draft finding, not an adjudication or a claim that the proposed cell has been committed.
- Tool installs/updates: none.
