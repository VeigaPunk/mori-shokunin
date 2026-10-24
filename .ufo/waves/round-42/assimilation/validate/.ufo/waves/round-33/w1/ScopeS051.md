# S051 scope finding — round 32 defect 3

## Finding

The S051 row at base commit `7d382043` is an unadjudicated `CriticScopingRows` finding, not an accepted verdict: the verifier spotcheck calls it “critic finding, not adopted” and says it was routed, not graded (`corpus/lessons/round-32-verifier-spotcheck.md:100-104,190-192`). The base row is `corpus/SOURCES.md:57`; its round-32 recheck is `corpus/lessons/round-32.md:38`.

I found one lane-application clause not stated by NIST: **“A class-hit gate does not by itself establish necessity.”** The page says nothing about a class-hit gate. It should be explicitly labelled as lane doctrine. The remaining teaches clauses and both scope clauses are stated or directly supported by the page:

- **“Retention needs a current-business-purpose test per item”** is a synthesis of the page’s explicit rule for PII with no current business purpose and its regular review instruction; see quoted text below (printed page 4-3). The page’s “If the PII serves no current business purpose” criterion applies to the PII itself.
- **“PII with no current purpose ‘should no longer be used or collected’”** is stated in §4.2.1, page 4-3.
- **“holdings need periodic review and disposal under schedules”** is stated in §4.2.1, page 4-3, and the Executive Summary, page ES-2. Note the source also specifies litigation holds; the round-32 recheck note separately flags that its S051 Q3 quote omits that clause (`corpus/lessons/round-32.md:106`).
- Scope **“PII minimum-necessary collection, use and retention”** is stated in the Executive Summary, page ES-2, and §4.2.1, page 4-3.
- Scope **“federal-agency guidance with voluntary non-federal use (§1.1)”** is stated in §1.1, page 1-1.

The committed source copy is `corpus/evidence/recheck-r32/S051.src` (NIST SP 800-122 PDF). Page references below are the PDF’s printed page labels. Quotes were extracted from that copy; they are not a fresh URL fetch.

## Old and proposed cells

**Scope — old**

```text
PII minimum-necessary collection, use and retention; federal-agency guidance with voluntary non-federal use (§1.1)
```

**Scope — proposed** (unchanged; all clauses are supported)

```text
PII minimum-necessary collection, use and retention; federal-agency guidance with voluntary non-federal use (§1.1)
```

**Teaches — old**

```text
Retention needs a current-business-purpose test per item: PII with no current purpose "should no longer be used or collected"; holdings need periodic review and disposal under schedules. A class-hit gate does not by itself establish necessity.
```

**Teaches — proposed**

```text
Retention needs a current-business-purpose test per item: PII with no current purpose "should no longer be used or collected"; holdings need periodic review and disposal under schedules. lane rule: A class-hit gate does not by itself establish necessity.
```

**Old → new diff**

```diff
-Retention needs a current-business-purpose test per item: PII with no current purpose "should no longer be used or collected"; holdings need periodic review and disposal under schedules. A class-hit gate does not by itself establish necessity.
+Retention needs a current-business-purpose test per item: PII with no current purpose "should no longer be used or collected"; holdings need periodic review and disposal under schedules. lane rule: A class-hit gate does not by itself establish necessity.
```

Equivalently, the only textual change is insertion of `lane rule: ` immediately before `A class-hit gate`; every other cell word remains unchanged. This follows the lane-application disclaimers in S073, S074 and S076 (`corpus/SOURCES.md:79-80,82`), e.g. S073 says that its trailer-path rule is “mori's own tool rule, not taught by this page.”

## Located page text

All quotations are from `corpus/evidence/recheck-r32/S051.src`:

- ES-2: “Organizations should minimize the use, collection, and retention of PII to what is strictly necessary to accomplish their business purpose and mission.” Supports the minimum-necessary scope and retention-purpose clause.
- §4.2.1, 4-3: “If the PII serves no current business purpose, then the PII should no longer be used or collected.” Supports the current-purpose criterion and the quoted no-purpose clause.
- §4.2.1, 4-3: “Also, an organization should regularly review its holdings of previously collected PII to determine whether the PII is still relevant and necessary” and “The destruction or disposal of PII must be conducted in accordance with any litigation holds and the Federal Records Act and records control schedules approved by the National Archives and Records Administration (NARA).” Supports periodic review and disposal under schedules; the quoted sentence also identifies the litigation-hold qualification.
- §1.1, 1-1: “This guideline has been prepared for use by Federal agencies” and “It may be used by nongovernmental organizations on a voluntary basis.” Supports the federal/voluntary scope clause.
- There is no text in these cited passages about a “class-hit gate”; the necessity disclaimer is therefore lane doctrine, not NIST teaching.

## Evidence and limits

- Read the base row with `timeout 120 git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -n '^| S051 ' 7d382043 -- corpus/SOURCES.md`; output located the row at `corpus/SOURCES.md:57`.
- Read the recheck table and source rows at `corpus/lessons/round-32.md:38` and `corpus/SOURCES.md:79-82`; read the closure note at `corpus/lessons/round-32-verifier-spotcheck.md:100-104,190-192`.
- PDF command record (the source was the committed copy `corpus/evidence/recheck-r32/S051.src`):
  - `timeout 120 pdfinfo /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/recheck-r32/S051.src` — reported 59 pages, unencrypted.
  - `timeout 120 pdftotext -layout /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/recheck-r32/S051.src -` — extracted full document text.
  - `timeout 120 pdftotext -f 6 -l 7 -layout /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/recheck-r32/S051.src -` — output included the end of contents and printed page ES-1.
  - `timeout 120 pdftotext -f 10 -l 11 -layout /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/recheck-r32/S051.src -` — output included §1.1 on printed page 1-1.
  - `timeout 120 pdftotext -f 27 -l 29 -layout /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/recheck-r32/S051.src -` — output included printed page 4-4 and following section text.
  - `timeout 120 pdftotext -f 8 -l 8 -layout /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/recheck-r32/S051.src -` — output printed ES-2.
  - `timeout 120 pdftotext -f 11 -l 11 -layout /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/recheck-r32/S051.src -` — output printed 1-1.
  - `timeout 120 pdftotext -f 26 -l 27 -layout /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/recheck-r32/S051.src -` — output printed 4-3 and 4-4, including §4.2.1 quotations above.
- No product source or judge was changed. No counter, tests, or adjudication were run; no source URL was fetched; no tool was installed. The single requested artifact is `.ufo/waves/round-33/w1/ScopeS051.md`.
- Out of scope: deciding the critic’s overall disposition, modifying `corpus/SOURCES.md`, and repairing the separate litigation-hold quote-boundary finding.
