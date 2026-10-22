defect found — all 13 `shape` descriptions match their pinned fixture inputs, but several source citations are incomplete or decorative.

## Findings by severity

### Moderate — rows 1–3 omit the source for comparing the two monotonic timestamps

The three shapes are accurate: c02 has its action one microsecond before the active-enter value (`cases.json:49-53`); c03 has it at that value (`:75-79`); c04 has its version line before and action after (`:102-106`). But S157 only covers when systemd assigns active-enter/active-exit timestamps, and its registry scope explicitly excludes the meaning of `ActiveEnterTimestampMonotonic` and the journal entry stamp ( `corpus/SOURCES.md:163`; excerpt `corpus/evidence/sources-r30/S157.txt:17-20`). S119 supports the startup version line in row 3 (`corpus/SOURCES.md:125`; upstream `main.c:161`). S160 supports current-boot and unit filtering, not the before/at comparison (`corpus/SOURCES.md:166`; excerpt `corpus/evidence/sources-r30/S160.txt:12-16,41-45`). The direct source for comparability—both values are same-boot `CLOCK_MONOTONIC` microseconds—is S122 (`corpus/SOURCES.md:128`), but rows 1–3 omit it. Thus their cited sources are partial for the distinguishing boundary claim; S160 in row 1 is context only.

### Moderate — row 5 cites S157 where S122 is needed for the zero property

The shape is accurate: the case has `ActiveState=inactive`, a zero active-enter property and only a version record (`cases-a2.json:583-603`). S156 supports how the property is printed as a bare decimal (`corpus/SOURCES.md:162`; excerpt `corpus/evidence/sources-r30/S156.txt:10-15,59-61`). S157 supports transition-time assignment, but its registry entry expressly says it does **not** support the meaning of the property ( `corpus/SOURCES.md:163`). S122 is the cited source that says the property is zero when no transition was recorded (`corpus/SOURCES.md:128`; the quoted source text is recorded at `corpus/lessons/round-30.md:119`), yet row 5 omits it. S157 is therefore only partial here; row 4 correctly cites S122 for the same zero-stamp premise (`earlyoom-invocation-scope-r30.md:98-99`).

### Low — row 11's S160 is context-only for the removed-unit case

The shape matches: the fixture is `LoadState=not-found`, has two version records and action records in both segments (`cases-a2.json:1085-1109`). S160 documents `journalctl`'s current-boot and unit filters (`corpus/SOURCES.md:166`; excerpt `corpus/evidence/sources-r30/S160.txt:12-16,41-45`); it does not establish the absent-state mapping, version-line invocation boundaries, or send classification. As the sole citation on the row (`earlyoom-invocation-scope-r30.md:105`), it is decorative for the row's distinctive claim.

### Moderate — row 13's sources do not cover its malformed JSON stamp

The shape matches: the fixture has a send record with a nonnumeric `__MONOTONIC_TIMESTAMP` (`cases-a2.json:1165-1179`). S154 covers the internal monotonic stamp and decimal export format, but its registry scope explicitly excludes JSON rendering (`corpus/SOURCES.md:160`; excerpt `corpus/lessons/round-29.md:57`). S160 covers journal filtering, not JSON field representation or malformed-record handling (`corpus/SOURCES.md:166`). Neither cited source supports the row's malformed JSON input or the reader's uncounted behavior; the latter is A2-10 in the rule text (`.ufo/waves/round-30/rule-text.md:95-98,114`). S154 is at most background for what a normal stamp is, and S160 is decorative for this row (`earlyoom-invocation-scope-r30.md:107`).

## Row-by-row audit

All rows below refer to the measured-tip decision table at `corpus/knowledge/earlyoom-invocation-scope-r30.md:95-107`. “Accurate” means the shape matches the named case's actual `inputs`, not merely its `expect`.

| Row / case | Shape | Each cited source against the row |
|---|---|---|
| 1 `c03-scope-boundary-exactly-at` | Accurate: matching active-enter and journal stamps (`cases.json:75-79`). | S157 supports the active-enter assignment; S160 only current-boot/unit filtering, not the exact boundary. S122 is missing for timestamp comparability. |
| 2 `c02-scope-boundary-one-microsecond-before` | Accurate: action timestamp is one unit before the active-enter value (`cases.json:49-53`). | S157 supports the stamp assignment, but not the property/journal-stamp comparison; S122 is missing. |
| 3 `c04-incomplete-scope-with-action` | Accurate: version record precedes the stamp and the action follows it (`cases.json:102-106`). | S119 supports the startup version record; S157 supports active-enter assignment. Neither substitutes for S122's cross-stamp semantics. |
| 4 `a2-05-monotonic-zero-active-quiet` | Accurate: active, zero stamp, no action record (threshold announcements are present) (`cases-a2.json:517-533`). | S156 supports bare-decimal display; S122 supports the unset-zero meaning. Both fit. |
| 5 `a2-05-monotonic-zero-inactive-quiet` | Accurate: inactive, zero stamp, version record only (`cases-a2.json:583-603`). | S156 supports rendering; S157 does not support the property's zero meaning. S122 is missing; see finding above. |
| 6 `a2-06-active-earlier-invocation-sends-quiet` | Accurate: two earlier action records precede the current version record; the current segment has no action (`cases-a2.json:610-646`). | S119 supports the startup marker and S159 supports restart possibility. These support the split, though neither establishes the timestamp comparison. |
| 7 `a2-06-inactive-earlier-invocation-sends-acted` | Accurate: inactive unit, three sends before the later version record (`cases-a2.json:677-710`). | S157 supports retaining the active-enter stamp across stop; S159 supports restart possibility. Neither directly supports version-line segmentation; S119 is omitted. |
| 8 `a2-06-active-earlier-and-current-send-acted` | Accurate: one send precedes the current version record and another follows it (`cases-a2.json:728-765`). | S159 supports restart possibility only; it does not define the version-line boundary. S119 is omitted, so the citation is partial. |
| 9 `a2-07-earlier-real-then-current-dryrun` | Accurate: earlier real action records precede a current dry-run startup/send (`cases-a2.json:795-827`). | S159 supports restarts and S155 supports the dry-run guard (`corpus/SOURCES.md:165,161`; excerpt `corpus/lessons/round-29.md:62`). Neither establishes the version-line split; S119 is omitted. |
| 10 `a2-07-three-invocations-dryrun-in-the-middle` | Accurate: three version records, with dry-run enabled in the middle and sends in the first and last segments (`cases-a2.json:906-966`). | S159 supports restarts and S155 the dry-run behavior; neither establishes the segment marker. S119 is omitted. |
| 11 `a2-09-removed-unit-two-invocations-mixed-sends` | Accurate: not-found load state, two version records and sends across both (`cases-a2.json:1085-1109`). | S160 supports only journal query filters; it does not support the removed-unit or invocation claims. Decorative for this row. |
| 12 `a2-01-suppressed-in-scope-active-quiet` | Accurate: suppression record follows the active-enter/version record in scope (`cases-a2.json:7-20`). | S158 directly supports the journald suppression notice text/origin (`corpus/SOURCES.md:164`; excerpt `corpus/evidence/sources-r30/S158.txt:7-11`), not the timestamp-in-scope relation. |
| 13 `a2-10-malformed-action-line-uncounted` | Accurate: the action record's monotonic field is nonnumeric (`cases-a2.json:1165-1179`). | S154 is only normal internal/export stamp context and expressly excludes JSON; S160 is only filtering. Neither supports malformed JSON/reader behavior. |

## Residual risk

No `shape` mismatch found. This review did not re-evaluate the tool's verdict/field semantics; it checked only each shape against the fixture `inputs` and the listed sources against their registered scope and excerpts.

## Verification gaps

No counter, build, or tests were run; this was a static source/fixture review. The assigned measured revision was `ad0f04745ced2194e58c22a0d6b38131bee3e230`; the checkout HEAD was `713be294669272b8b29e9a8cd60c5313704a2ee1`, and the working-tree entry blob differed, so row and fixture claims above were anchored to the requested committed bytes via read-only `git show`. No code callers or definitions were in scope for LSP navigation.