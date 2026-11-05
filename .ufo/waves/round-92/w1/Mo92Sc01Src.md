# Mo92Sc01Src — round 92 w1 scout: source-open gate facts for S619, S620, and candidate S621

Scope: open the sources behind the two successor rows and one candidate spec row; locate the
gate facts (contract §Frontier step; fleet `CORPUS.md` rule 1). No lane-tree write by this seat;
the L1 integrates. Entering revision `f63d1ab030d4179576e494342f48ef8718e497a5`. All values below
were measured by this seat in its scratch clone; every command and its exit code is given.

Scratch clone: `git clone --shared -q <lane> <scratch>/repo` then
`git -C <scratch>/repo checkout -q --detach f63d1ab0…`; `git -C <scratch>/repo rev-parse --show-toplevel`
printed `<scratch>/repo` (exit 0) and `rev-parse HEAD` printed `f63d1ab0…` (exit 0).

---

## 1. Pinned copy `python-ast-3.15.2.html` (behind S619 / successor of S615)

Path at the entering revision: `.ufo/waves/round-90/w1/Mo90S01Sources/sources/python-ast-3.15.2.html`

| measure | command | value | exit |
|---|---|---|---|
| sha256 | `git -C <lane> show f63d1ab0…:<path> \| sha256sum` | `7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b0f83b9a8a42f5` | 0 |
| bytes | `git -C <lane> show f63d1ab0…:<path> \| wc -c` | `362493` | 0 |
| byte-identical to the file in the scratch tree | `sha256sum <scratch>/work/python-ast-3.15.2.html` | same digest, 362493 B | 0 |

**Equals the digest the successor row S619 records** (`7891c588…a8a42f5`) and the digest the brief
pins. The digest S615 records in `corpus/SOURCES.md`
(`7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b8f1a60ad1a6f0`) is **not** it: the two agree
for 51 characters and then differ (first differing index 51), so the recorded value is a corrupted
tail, not a prefix. The entering tool therefore classifies S615 `mismatch` (equal length ⇒ the
`prefix-only` branch cannot apply).

### The located quote

Quote required by the brief: *“Recursively yield all descendant nodes in the tree starting at node”*.

- **Occurrences: 1.** **Word count: 11** (≤ 25 ✓).
- **Line number in the tag-stripped text: 1907** — under the round-90 method
  (remove `<script>`/`<style>`, tags → space, HTML-unescape, **drop blank lines**, collapse runs of
  whitespace per line). This reproduces the line number S615 already records (1907-1908), so the
  method is the same one round 90 used.
- Method dependence (worth recording, because the anchor in a registry row is only meaningful
  together with its method): keeping blank lines puts the same quote at **line 2835**; a raw
  tag-strip without dropping blanks and without `<script>` removal puts it at 2854. The value 1907
  is reproducible only with blank lines dropped. A row that cites “tag-stripped lines 1907-1908”
  is therefore a claim about a specific extraction, and the successor row should carry the same
  method wording or a digest-pinned line reference.
- The full sentence, which is what S615 quotes, is
  *“Recursively yield all descendant nodes in the tree starting at node (including node itself), in
  no specified order.”* — **18 words**, **1 occurrence**, spanning lines **1907-1908** (same method).

### Second fact S619/S615 name — a discrepancy the L1 should know

The second anchor fact, `ast.get_source_segment`, is recorded in S615 and repeated in S619 as
*“If some location information (lineno, end_lineno, col_offset, or end_col_offset) is missing,
return None.”* — 13 words. **Measured occurrence count of that string in the tag-stripped text: 0**
(the rendered page puts spaces inside the parentheses and before the commas:
`If some location information ( lineno , end_lineno , col_offset , or end_col_offset ) is missing,
return None .` — a whitespace-collapsed search still does not match the recorded punctuation).
The **sentence is present** at lines 1881-1882 of the same extraction (the second half at 1882), so
the *fact* is grounded; the *recorded string* is a punctuation-normalized paraphrase, not a
byte-verbatim quote. Recommendation to the L1: let S619 quote only the `ast.walk` sentence (11 or 18
words, verbatim, 1 occurrence) and let the `get_source_segment` half carry a re-quoted, punctuation-
exact string, or the recheck will fail on a string that was never in the page.

---

## 2. Pinned copy `S235.pdf` (behind S620 / successor of S235)

Path at the entering revision: `corpus/evidence/sources-r42/S235.pdf`

| measure | command | value | exit |
|---|---|---|---|
| sha256 | `git -C <lane> show f63d1ab0…:<path> \| sha256sum` | `9855a4986a312dfc946b1b97b6010a8e4f1e65a4a30dca99359e6df057ad8020` | 0 |
| bytes | `git -C <lane> show f63d1ab0…:<path> \| wc -c` | `6482693` | 0 |
| copy in scratch tree | `sha256sum <scratch>/work/S235.pdf` | same digest | 0 |

Equals the digest S620 records and the digest the brief pins. The digest S235 records
(`…a30cda99359e6df057ad8020`) differs from the measured one **only by a transposition of two
adjacent characters at indices 43-44** (`a30cda99` vs `a30dca99`); both strings are 64 hex chars, so
the tool reports `mismatch`, not `prefix-only`.

### Text extraction

```
pdftotext -layout S235.pdf S235-layout.txt      # exit 0   (stderr: repeated "Syntax Warning: Invalid Font Weight")
pdftotext S235.pdf S235-plain.txt               # exit 0
pdfinfo S235.pdf                                # exit 0   → Pages: 45, file size 6482693 bytes, PDF 1.6
```

Both extractions succeed (the warnings are font-weight warnings, not failures).

### The located quote (row anchor = the 「约束限制」 iSulad bullet)

> 由于 cgroup oom 会同时触发容器 cgroup 路径删除，若 iSulad 对 oom 事件处理发生在 cgroup 路径删除之后，iSulad 则无法成功捕捉容器 oom 事件，可能导致 ContainerStatus 中 reason 字段设置不正确。

- **Occurrences: 1.** `grep -c "无法成功捕捉容器" S235-layout.txt` → **1** (exit 0);
  `grep -c "无法成功捕捉容器" S235-plain.txt` → **1** (exit 0).
  The count 1 that S235's own anchor records (“pdftotext 无法成功捕捉容器 count 1”) reproduces exactly.
- **Line number: 1054** in the `-layout` text (the bullet starts at 1053, wraps onto 1054);
  **line 1144** in the plain text. The sentence spans two layout lines, so a row anchor should say
  “lines 1053-1054 (layout)”.
- **Word count.** The quote is Chinese with embedded Latin tokens; two counts are defensible:
  **19 whitespace-delimited tokens** and **133 characters** — both ≤ 25 under the token reading.
  Because the corpus rule is a word limit and the corpus already carries CJK rows, the L1 should
  fix one reading in the row text (token count 19) so the recheck is reproducible.
- **Page location.** The bullet is on **PDF page 27** of 45; the printed footer of that page reads
  `openEuler 24.03 LTS 技术白皮书 25`. So the anchor “p.27” in S235 matches the **PDF page index**,
  not the printed page number (25). The 「约束限制」 heading appears 4 times in the document
  (PDF pages 27, 29, 38, 39); only the one on PDF page 27 is the iSulad one — the anchor must say
  “PDF page 27, printed page 25, 「约束限制」 section, iSulad bullet 2”, otherwise the recheck can
  land on the wrong 约束限制 block. The S235 anchor as it stands (“p.27「约束限制」項 iSulad 小節”) is
  under-specified in exactly this way; the successor row S620 should carry the disambiguating form.

---

## 3. Candidate spec row S621 — NIST FIPS 180-4 (opened)

- `read` tool on `https://csrc.nist.gov/pubs/fips/180-4/upd1/final` → **available** (HTTP 200;
  title “FIPS 180-4, Secure Hash Standard (SHS)”; Date Published: August 2015; Supersedes:
  FIPS 180-4 (03/06/2012); Planning Note 03/07/2023: NIST has decided to revise FIPS 180-4;
  Publication DOI https://doi.org/10.6028/NIST.FIPS.180-4; Download URL
  `https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf`; Document History “08/04/15: FIPS
  180-4 (Final)”).
- The **landing page carries no output-length statement**: `grep -c -i "256" fips180-4-page.html`
  → **0** (exit 0); the page HTML is 40642 bytes, sha256
  `c241807d9513fc64732937b35c65819fcccde30aa67ab88b5b9e94466e49ba47` (HTTP 200). So the quote had to
  be taken from the standard PDF that the landing page points to.
- `curl -sSL -o NIST.FIPS.180-4.pdf https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf`
  → HTTP 200, **833315 bytes**, sha256
  `0455b406d89648d20cbde375561e19c245b9815e894164c2670772e3d54deb82` (exit 0).
- `pdftotext -layout NIST.FIPS.180-4.pdf fips-layout.txt` → exit 0 (36 pages).

**Located quote (10 words, 1 occurrence):**

> The final result of SHA-256 is a 256-bit message digest.

- Occurrences: `grep -c "The final result of SHA-256 is a 256-bit" fips-layout.txt` → **1** (exit 0);
  the sentence sits at text line **1016** and on **PDF page 26 of 36**, printed page **21**.
- Location in the standard: **§6.2 “SHA-256”** (the section that fixes the algorithm), plus the
  corroborating table in §1/§3 (“Message Digest Size … SHA-256 … 256”, table at text lines 251-259).
- Access date **2026-11-05**; document revision/publication: **FIPS 180-4 Update 1, published
  2015-08-04** (with NIST's 2023-03-07 planning note to revise it — that is the recheck trigger).

### Draft row S621

| field | value |
|---|---|
| id | `S621` |
| source | NIST FIPS 180-4, Secure Hash Standard (SHS) — https://csrc.nist.gov/pubs/fips/180-4/upd1/final (document PDF https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf) |
| kind | spec |
| tier | A |
| scope | the sha256 digest definition and its fixed output length, so a digest check knows how many hex characters a full sha256 must have |
| anchor | section 6.2 SHA-256, FIPS 180-4 Update 1 published 2015-08-04, printed page 21 of 36 (PDF page 26); quote located 2026-11-05 at pdftotext line 1016, grep -c -F = 1: “The final result of SHA-256 is a 256-bit message digest.”; document sha256 0455b406d89648d20cbde375561e19c245b9815e894164c2670772e3d54deb82, 833315 bytes |
| teaches | a full sha256 is a fixed-width 256-bit value, so a recorded digest that is not 64 hex characters is already a defect before any byte comparison runs |
| status | mined |
| used-by | corpus/lessons/round-92.md |
| flip | if a corpus/knowledge entry that cites this row is not landed, the row must be flipped to rejected with the reason that no admitted entry grounds it, the same treatment the lane gave S618 |

**Calibration note on `status: mined` (L1 decision, disclosed).** No `corpus/knowledge/*.md` entry
is planned to cite S621 in round 92; the citing artifact is the round-92 lesson, exactly as for the
two successor rows S619 and S620, whose `used-by` is `corpus/lessons/round-92.md` with status
`mined`. This row is therefore drafted `mined` on that precedent, not on a knowledge-entry citation;
the `flip` field above states the fallback if the L1 applies the stricter reading.

### Operability finding the L1 must apply before appending S621 (measured)

The digest gate resolves a row's recorded digest against a copy path named in the row. Measured on
the scratch clone with the two successor rows appended (S619 + S620 verbatim from the brief):

```
python3 -I tools/mori-source-digest.py corpus/SOURCES-sim.md .ufo/waves/round-90/w1/Mo90S01Sources/sources
# exit 1 (expected: supersession logic not landed yet)
DIGEST S619 ok      recorded=7891c588…a8a42f5 actual=7891c588…a8a42f5
DIGEST S620 ok      recorded=9855a498…57ad8020 actual=9855a498…57ad8020
DIGEST S235 mismatch recorded=9855a498…a30cda99359e6df057ad8020 actual=9855a498…a30dca99359e6df057ad8020
DIGEST S615 mismatch recorded=7891c588…94b8f1a60ad1a6f0 actual=7891c588…94b0f83b9a8a42f5
DIGEST_CHECK rows=123 ok=89 mismatch=2 prefix_only=31 unpinned=1
```

Three measurements the L1 can rely on:

1. **Both successor rows classify `ok` against the copies they name.** The contract's supersession
   rule (“a successor counts only if the tool classifies the successor itself `ok`”) is satisfied by
   the rows as drafted, provided the L1 appends them **with the digest and copy path in the row** —
   my simulation used a scratch `corpus/SOURCES-sim.md` placed **inside `corpus/`** so the tool's
   `repo_root` derivation works. Putting the modified registry anywhere else makes the tool resolve
   no copies at all and report `unpinned=120` (measured, exit 1) — a silent trap for the tool patch.
2. **Appending S621 changes the C2 no-harm counters if its copy is not in the tree.** With a row
   naming a pinned copy path that does not exist (`corpus/evidence/sources-r92/S621.pdf`),
   the gate reports `DIGEST S621 unpinned` and `DIGEST_CHECK … unpinned=2` (measured, exit 1) —
   C2's frozen `unpinned=1` would break. With the PDF committed to
   `corpus/evidence/sources-r92/S621.pdf` in the same landing, the gate reports `DIGEST S621 ok` and
   `DIGEST_CHECK rows=124 ok=90 mismatch=2 prefix_only=31 unpinned=1` (measured, exit 1) — no-harm
   preserved. Third option: a row with a digest but no copy path and no “pinned copy” wording is
   skipped entirely by the tool (`rows=123`, `unpinned=1`, measured, exit 1) — safe but the digest
   is then never checked. **Recommendation: commit the FIPS PDF into the lane tree as the pinned
   copy and name that path in the row.**
3. `prefix_only=31` is untouched by all of the above.

### Dead ends / negative results (recorded so nobody repeats them)

- The S615/S235 `mismatch` verdicts are **not** caused by the pinned copies having drifted: both
  re-hashed to the digests the brief pins. The defect is in the recorded strings (S615: tail
  replaced from index 51; S235: two characters transposed at 43-44).
- The `ast.get_source_segment` quote as recorded in S615/S619 is **not byte-verbatim** in the page
  (0 occurrences); no whitespace normalization reproduces it because the page renders spaces before
  commas and inside parentheses.
- The NIST **landing page** contains no sha256 output-length sentence (`grep -c -i 256` = 0); the
  quote exists only in the standard PDF the page links to. Opening only the landing page would have
  produced a rejected row.
- `pdftotext` on `S235.pdf` succeeds; the “Invalid Font Weight” lines are warnings on stderr with
  exit 0, not extraction failures.

---

## 4. Gate blocks (fleet `CORPUS.md` rule 1 form)

**S619**

- URL: https://docs.python.org/3/library/ast.html
- Access date: 2026-11-05
- Pinned copy: `.ufo/waves/round-90/w1/Mo90S01Sources/sources/python-ast-3.15.2.html`,
  sha256 `7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b0f83b9a8a42f5`, 362493 bytes
- Located quote: “Recursively yield all descendant nodes in the tree starting at node” — **11 words**,
  **1 occurrence**, tag-stripped (blank lines dropped) **line 1907**; the full sentence with
  “(including node itself), in no specified order.” is **18 words**, 1 occurrence, lines 1907-1908

**S620**

- URL: https://www.openeuler.org/whitepaper/openEuler%2024.03%20LTS%20%E6%8A%80%E6%9C%AF%E7%99%BD%E7%9A%AE%E4%B9%A6.pdf
- Access date: 2026-11-05
- Pinned copy: `corpus/evidence/sources-r42/S235.pdf`,
  sha256 `9855a4986a312dfc946b1b97b6010a8e4f1e65a4a30dca99359e6df057ad8020`, 6482693 bytes
- Located quote: “由于 cgroup oom 会同时触发容器 cgroup 路径删除，若 iSulad 对 oom 事件处理发生在 cgroup 路径删除之后，iSulad 则无法成功捕捉容器 oom 事件，可能导致 ContainerStatus 中 reason 字段设置不正确。” — **19 whitespace tokens**
  (133 chars), **1 occurrence** (`grep -c` = 1, layout and plain), **PDF page 27 / printed page 25**,
  「约束限制」 section, iSulad bullet 2, layout lines **1053-1054** (plain text line 1144)

## 5. Handoff / not done

- No lane-tree write by this seat; **no patch files produced** (the S619/S620 append belongs to
  scribe `Mo92S01Successors`; this report supplies the gate facts and the S621 draft only).
- Tools used: `git`, `python3` (3.14.8), `pdftotext`/`pdfinfo` (poppler 26.10.0), `curl`, `grep`,
  `sha256sum`. **Nothing installed or upgraded** by this seat.
- Scratch `/fast/scratch/hyaku/mori-r92/Mo92Sc01Src` removed before yield.
