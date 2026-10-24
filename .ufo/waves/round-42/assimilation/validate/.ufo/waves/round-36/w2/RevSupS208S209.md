# RevSupS208S209 — re-opening S208 (NIST SP 800-122) and S209 (RFC 8785)

Seat: `mori-r36-w2-RevSupS208S209-23` (wave 2, attempt 2, L1 MoriR36). Lane:
`/home/vgpnk/Projects/shokunin/mori-shokunin`, tip `bf0df77fee4b6ef54a90aea09335c7617f125151`,
round base `6bd57097`. Attacked item: SOURCES rows S208 and S209 (rows + committed copies +
located quotes + tier justification).

## Method

1. Read the frozen contract (`.ufo/waves/round-36/contract.md`) and the row cells in
   `corpus/SOURCES.md` (raw lines 214, 215).
2. Hashed working-tree copies, their blobs at the tip, and fresh live fetches of both row URLs
   (scoped under `/fast/scratch/hyaku/mori-r36/mori-r36-w2-RevSupS208S209-23/`).
3. Located the quotes in the fetched documents: NIST ES-2 minimization sentence (pdftotext
   -layout extraction of the PDF) and RFC 8785 §1 hashable-output sentence (plain-text lines
   93–102, plus contiguity check in the HTML rendering that is the committed copy).
4. Checked row identity (working tree vs tip blob) and tier rule source
   (`corpus/evidence/sources-r36/S205.src`, contract v1 rules).

No tool installs performed this seat (used preinstalled `curl`, `pdftotext`, `python3`
stdlib). No lane files modified; lane read-only respected.

## Measurements (command → observed output)

### S208 — NIST SP 800-122

- Row (raw line 214): `| S208 | NIST SP 800-122, Guide to Protecting the Confidentiality of
  Personally Identifiable Information (PII) — https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-122.pdf | docs | A | PII minimum-necessary collection, use and retention; federal-agency guidance with voluntary non-federal use (§1.1) | ES-2 text: Organizations should minimize the use, collection, and retention of PII; §4.2.1 printed pp. 4-3 to 4-4; April 2010 final, document history 04/06/10; ... | supersedes S051 — ... | mined | 2026-10-23 | 365d | corpus/knowledge/evidence-minimization-r18.md |`
- Copy sha256 (working tree, tip blob, live fetch all equal):

  `$ sha256sum corpus/evidence/sources-r36/S208.src`
  → `555b9df82af12de4ca887efc21c0a9e159a14485d5d570f44b32ef15c6c62470  corpus/evidence/sources-r36/S208.src`
  (818,516 bytes, `%PDF-1.6`)

  `$ git show bf0df77fee4b6ef54a90aea09335c7617f125151:corpus/evidence/sources-r36/S208.src | sha256sum`
  → `555b9df82af12de4ca887efc21c0a9e159a14485d5d570f44b32ef15c6c62470  -`

  `$ curl -sSL --max-time 90 -o nist-sp800-122.pdf https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-122.pdf && sha256sum nist-sp800-122.pdf`
  → `555b9df82af12de4ca887efc21c0a9e159a14485d5d570f44b32ef15c6c62470  nist-sp800-122.pdf` (818,516 bytes)

- Quote contiguity at anchor (pdftotext -layout; 60 pages):

  `$ python3` regex `Organizations should minimize the use, collection, and retention of PII`
  → found on exactly one page (page index 7), contiguous run, context:
  `... financial information). Organizations should minimize the use, collection, and retention of PII to what is strictly necessary to accomplish their business purpose and mission.`
  Folio check: `ES-2` is the page label of page index 7 (`ES-1` on idx 4/6, `ES-2` on idx 7,
  `ES-3` idx 8, `ES-4` idx 9). Array → ES-2.
- Quote word count: 10 ≤ 25.

### S209 — RFC 8785

- Row (raw line 215): `| S209 | RFC 8785 JSON Canonicalization Scheme (JCS) — https://www.rfc-editor.org/rfc/rfc8785 | spec | A | JCS canonical JSON serialization for hashing: ... | §1 hashable output:93-102; ... | supersedes S062 — JCS yields a hashable JSON representation ... | mined | 2026-10-23 | 365d | corpus/knowledge/dispatch-ledger-r18.md |`
- Copy sha256 (working tree, tip blob, live fetch all equal):

  `$ sha256sum corpus/evidence/sources-r36/S209.src`
  → `a0f3ccdf5e85ec2de043923f53e7aa96cf99e3587264bf941c9af506f075b434  corpus/evidence/sources-r36/S209.src`
  (476,658 bytes, HTML rendering)

  `$ git show bf0df77fee4b6ef54a90aea09335c7617f125151:corpus/evidence/sources-r36/S209.src | sha256sum`
  → `a0f3ccdf5e85ec2de043923f53e7aa96cf99e3587264bf941c9af506f075b434  -`

  `$ curl -sSL --max-time 90 -o rfc8785.html https://www.rfc-editor.org/rfc/rfc8785 && sha256sum rfc8785.html`
  → `a0f3ccdf5e85ec2de043923f53e7aa96cf99e3587264bf941c9af506f075b434  rfc8785.html` (476,658 bytes);
  `rfc8785.txt` (41,879 bytes) fetched for anchor-line verification.

- Quote contiguity at anchor (plain-text lines 93–102 = §1 Introduction):

  line 93: `1.  Introduction`
  lines 100–102: `The output from JCS is a "hashable" representation of JSON data that can be used by cryptographic methods.`
  → sentence occurs contiguously inside the named range; the paragraph is the §1 hashable-
  output language. In the HTML copy the same sentence is contiguous with entity escaping
  (`The output from JCS is a &quot;hashable&quot; representation of JSON data that can be used by cryptographic methods`, regex-matched within §1).
- Quote word count: 18 ≤ 25.

### Row identity and append-only interplay

- `$ git show bf0df77...:corpus/SOURCES.md | grep -E '^\| S2(08|09) '` == working-tree rows
  (`diff` empty); `git diff --quiet bf0df77... -- corpus/SOURCES.md corpus/evidence/sources-r36/S208.src corpus/evidence/sources-r36/S209.src` → exit 0.
- `$ git show 6bd57097...:corpus/SOURCES.md | grep -E '^\| S2(05|...|20) '` → no output:
  S205–S220 did not exist at the round base; S208/S209 are appends this round, so no C2
  immutable-change/deletion violation from these rows. Supersedes chains open with
  `supersedes S051 —` / `supersedes S062 —` (rule 2 format).
- C1 live receipt (`evidence/drift-live-r36.txt`) lists `S208 fresh`, `S209 fresh`,
  consistent with this seat's independent live-fetch equality.

### Tier A justification

- Contract v1 tier rule (S205.src, lines 93–97): A = "primary or authoritative for that scope
  (spec, official docs, source code, original paper, maintainer statement, the lane's own
  re-runnable gate output)". `community` is never A.
- S208 `docs`/A: NIST SP 800-122 is an official NIST Special Publication served from the
  agency's publication server (nvlpubs.nist.gov); primary standards-body document for the
  stated scope (PII minimum-necessary collection, use and retention guidance). Justified.
- S209 `spec`/A: RFC 8785 is the canonical RFC-series document for JCS, served by the RFC
  Editor (rfc-editor.org). The row explicitly discloses `Informational independent submission`
  (June 2020) — honest about the submission stream; the document remains the primary
  authoritative spec for the "normative for JCS conformance" scope. Consistent with sibling
  RFC rows at tier A (S041, S042, S206). Justified.

## Findings

No defects found in scope. Severity-ordered:

- (none) S208 quote: contiguous at ES-2, 10 words, copy sha256-equal to live fetch and tip blob.
- (none) S209 quote: contiguous in §1 lines 100–102, 18 words, copy sha256-equal to live
  fetch and tip blob.
- (none) Tier A justified for both rows under contract v1 rule.
- (none) Rows single-occurrence at tip, working tree == tip, appended this round (no C2 violation).

Minor observations (not defects):

1. S209's anchor `:93-102` refers to plain-text line numbers (as S041 explicitly qualifies
   with "plain-text lines"); the committed copy is the HTML rendering. The quoted sentence is
   verbatim present in both forms, and §1 is unambiguous, so the locator is honest.
2. S208's quote continues in-source "...to what is strictly necessary to accomplish their
   business purpose and mission."; the row quotes the first clause, which is contiguous and
   within the 25-word bound.

## Residual risk / verification gaps

- Live fetches are point-in-time (2026-10-23); equality with the committed copies matches the
  `evidence/c1-after.txt` receipt (`oracle_fetched=58 oracle_fresh=49`, S208/S209 fresh).
- `S209`'s erratum 7920 statement (anchor cell) and `S208`'s §4.2.1 page citations were not
  re-verified here (outside the scoped quote set).
- Counter re-scoring and other rows' discharge status are covered by sibling seats.

## VERDICT: PASS

(no defect found in the attacked S208/S209 rows, copies, located quotes, or tier justification).
