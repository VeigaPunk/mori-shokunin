# Mo79S02SourcesRow — seat report (mori round 79, wave w1, C3 registry prose)

Date: 2026-11-04. Leaf scribe seat, godspeed framing. Lane bounds respected: no git
mutation, no edits outside my two wave-dir files + scratch, no subagent dispatch, no
installs (none needed), detection and report only.

## What I did

1. Read the frozen inputs: contract §C3 (`.ufo/waves/round-79/contract.md`), the
   SOURCES.md registry header + last rows (11-column shape `id | source | kind | tier |
   scope | anchor | teaches | status | opened | recheck | used-by`, verified on S574–S593),
   `corpus/README.md`'s coverage-map/knowledge-additions structure, QUALITY 159/161/162/163
   (`corpus/QUALITY.md:1644,1677,1704,1731`), and the SKILL.md gate-registry section
   (context only).
2. Checked preconditions at draft start: `.ufo/waves/round-79/evidence/source-rfc9111-r79.txt`
   — path not found; `corpus/evidence/sources-r79/rfc9111.txt` — path not found (read
   tool, both). Registry row census: `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'
   corpus/SOURCES.md` → `366`; S594 absent (`grep -nE '^\|\s*S594\s*\|'` → rc 1). 366+1 =
   367 = P-C3's landed count.
3. Fetched the canonical bytes myself into scratch:
   `curl -fsSL https://www.rfc-editor.org/rfc/rfc9111.txt` → 1956 lines,
   sha256 `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`.
4. Messaged Mo79E03SourcePin (pin bytes identity); their reply: pin written verbatim at
   `corpus/evidence/sources-r79/rfc9111.txt`, HTTP 200 text/plain, 84477 bytes, same
   sha256. Two independent fetches, one hash — the row's sha cell is the real pin sha,
   never invented. Acked.
5. Re-ran every located-line check against the PINNED copy (QUALITY 162) once it landed:
   heading `:526`; MUST NOT paragraph `:528-534` (clause `:530-533`); match definition
   `:536-538`; transforms `:540/:543/:546-550`; absent-field rule `:552-554`; `*` refusal
   `:556-557`. Full command battery and outputs embedded in the append doc.
6. Drafted the S594 row + the README r79 knowledge-addition section; delivered both with
   insertion points and self-checks in
   `.ufo/waves/round-79/w1/Mo79S02SourcesRow-append.md`. SOURCES.md and README.md were
   NOT edited (L1 appends).

## Commands and outputs (load-bearing)

- Pin identity (run twice, before and after drafting):
  `sha256sum corpus/evidence/sources-r79/rfc9111.txt` →
  `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`;
  `wc -c -l` → `1956 84477`.
- Located lines (grep -n over the pin): `526` heading; `536` match definition; `538`
  "second request by applying any"; `540`/`543`/`546` the three transforms; `550`
  "case-insensitive)"; `553`/`554` absent-field pair; `556`/`557` `*` refusal.
- 30-word span: trimmed join of :530-533 prints the exact clause and `wc -w` → `30`.
- 11-cell self-check over the delivered append-doc bytes:
  `awk -F'|' '/^\| S594 \|/ {…}'` → `pipes=12 cells=11`, all 11 cells listed in census
  order (`S594 / HTTP Caching (RFC 9111) §4.1 — https://… / spec / A / the Vary-selected…
  / §4.1 "Calculating Cache Keys… / A cache must not serve… / mined / 2026-11-04 / 365d /
  corpus/knowledge/ua-serving-normative-r79.md`), zero BADPAD lines.
- Escaped-pipe check: `printf '%s' "$ROW" | grep -oF '\' | wc -l` → `0`.
- README row: `awk -F'|' '/^\| The normative ground of the lane/ {print NF-2}'` → `3`
  (twice — the section-table copy and the row-alone copy are byte-identical by
  construction).

## What I found

- The pin and its receipt did not exist when this seat started; resolved by coordination
  (pin executor confirmed verbatim rfc-editor.org bytes) plus my own independent hash of
  the same URL — no waiting idle, no invented sha. The receipt
  `.ufo/waves/round-79/evidence/source-rfc9111-r79.txt` now exists (pin executor's); my
  checks read the pin bytes directly, so the receipt was not needed for the sha.
- Registry insertion point: `corpus/SOURCES.md:374` (the S593 row) is the registry's last
  row; blank 375, `## Paths` 376. The S594 row follows 374.
- README insertion point: the coverage-map table (lines 4–50) ends at r45; rounds 46–78
  index new growth in per-round `## Round-N knowledge addition` sections at the file end
  (Round-76 §:848-851, Round-77 §:854-857; file ends at :859 with the r78 row). My section
  therefore appends after :859 — a bare row inside the Round-77 table would misattribute
  the r79 entry to round 77.
- Cross-line quote convention: RFC 9111 wraps at ~72 chars, so the MUST NOT clause spans
  :530-533 with both boundaries mid-line. Recorded per the S592/S593 precedent ("the
  located contiguous span starts at … ends at …, recorded as such"), and the word count is
  mechanically verified at 30.
- C3 grounding lands in the teaches/scope cells: a UA-differentiated byte difference
  between two fetches of one URL is representation selection under the Vary cache-key rule
  (RFC 9111 §4.1 :530-533), not content drift by itself — exactly the contract's sentence,
  put in the registry's own idiom.

## What I could not verify (limits)

- Line numbers and sha are verified against the pin's bytes as they exist now. If anything
  rewrites `corpus/evidence/sources-r79/rfc9111.txt` before the L1 lands, the sha256 cell
  moves with it and the grep battery in the append doc must re-pass (byte-identity guard:
  re-run `sha256sum`; any drift = re-pin or re-derive).
- Mo79S01EntryProse's entry content is a sibling deliverable; my `used-by` names the path
  only and P-C3's entry clauses (source:/verified-at:/recheck:) are graded there, not here.

## My defects (what I got wrong and how I caught it)

1. Off-by-two located-line guesses: from the first (truncated, context-anchored) read I
   drafted absent-field `:551-552` and the `*` rule `:554-555`. `grep -n` against the pin
   bytes gave `:552-554` and `:556-557`. Caught before any candidate bytes left this seat;
   the append doc carries only the verified numbers.
2. Word-count tail: my first mechanical extraction of :530-533 counted 38 words because
   the `(i.e., …` continuation rode along. Fixed by recording the span's mid-line end
   boundary and re-verifying the trimmed span at exactly 30 words.
3. Assumed the sha could be read from the round-79 evidence receipt per the seat rule's
   first branch; the receipt did not exist. Correct behavior followed (hash the pin bytes
   myself after they landed; cross-check with a second independent fetch) rather than
   inventing or stalling.
4. Minor: my first verification bash was backgrounded by an incoming message interrupt;
   its scratch-copy results were superseded by the pin-file re-run (same sha, same lines)
   and are not cited anywhere.

## Bounds kept / provenance

- Wrote exactly two files: `Mo79S02SourcesRow-append.md` (deliverable) and this report.
- No edits to `corpus/SOURCES.md`, `corpus/README.md`, MANIFEST, `.ufo/state/`, contract,
  counters, or any sibling's files; read-only access otherwise.
- Scratch: `/fast/scratch/hyaku/mori-r79/Mo79S02SourcesRow/` (RFC fetch), removed before
  yield (verified below in the cleanup line of the transcript).
- No tool installs or upgrades (stock `curl`/`sha256sum`/`grep`/`awk`/`sed`/`wc` only);
  pacman untouched. Peer messages: Mo79E03SourcePin only (pin-identity question + ack).
