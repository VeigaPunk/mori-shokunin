# SrcRfc8785 — RFC 8785 (JCS) screen for the C3 payload identity

Seat: MoriR18Recovery.SrcRfc8785 (scribe, leaf). Access date: 2026-10-21. No VCS commands, no downloads, no file writes outside this report. Interpreter used for stdin-only checks: system `python3` 3.14.8 (no install performed; no tool installed or updated this round).

Question (C3): is the frozen payload identity `json.dumps({"context":…,"tasks":…}, ensure_ascii=False, sort_keys=True, separators=(',', ':'))`, UTF-8 encoded (`frozen/c3-ledger-format.json`, `payload_identity`), a canonical form, and what are its limits versus JCS for property sorting and number/string serialization?

## 1. Sources opened

| Item | Value |
|---|---|
| Primary URL | https://www.rfc-editor.org/rfc/rfc8785 (opened 2026-10-21, reader Markdown rendering; section numbers cited, rendering not line-pinned) |
| Document | RFC 8785, "JSON Canonicalization Scheme (JCS)", June 2020, Category Informational, Independent Submission, ISSN 2070-1721, 20 pages; authors A. Rundgren, B. Jordan, S. Erdtman |
| Errata | https://www.rfc-editor.org/errata/rfc8785 (opened 2026-10-21 via errata search records). One record: Section 5 (-0), reported 2024-05-02 by P. Patel-Schneider, Verified 2024-05-15 |
| Alternative screened | https://docs.python.org/3/library/json.html (opened 2026-10-21; page is the 3.15 docs, local interpreter is 3.14.8) — see section 4 |

## 2. Located quotes (each ≤25 words)

- Q1, §3.2.3 Sorting of Object Properties: "The sorting is based on pure value comparisons, where code units are treated as unsigned integers, independent of locale settings." (20 words)
- Q2, §3.2.1 Whitespace: "Whitespace between JSON tokens MUST NOT be emitted." (8 words)
- Q3, §3.2.2.3 Serialization of Numbers: "Such data MUST be serialized according to Section 7.1.12.1 of [ECMA-262], including the "Note 2" enhancement." (16 words)
- Q4, §3.2.2.3 (Note): "occurrences of NaN or Infinity MUST cause a compliant JCS implementation to terminate with an appropriate error." (17 words)
- Q5, §3.1 Creation of Input Data: "JSON objects MUST NOT exhibit duplicate property names." (8 words)
- Q6, errata record (Section 5, -0): "a JSON parser following this specification SHOULD generate an error condition" (14 words; errata text, not RFC body)

## 3. Checks run (stdin-only, read-only; no files)

Command (C-A, sort + string test on the RFC §3.2.3 test keys; emoji written as `\U0001F600`, a single code point):
```
python3 -c '…sorted(d.items())… vs sorted(d.items(), key=lambda kv: kv[0].encode("utf-16-be"))…'
```
Observed (exit 0):
- Python `sorted` order: Carriage Return, One, Control, Latin Small Letter O…, Euro Sign, **Hebrew Letter Dalet With Dagesh, Emoji: Grinning Face**
- UTF-16 code-unit order: Carriage Return, One, Control, Latin Small Letter O…, Euro Sign, **Emoji: Grinning Face, Hebrew Letter Dalet With Dagesh**
- RFC §3.2.3 expected order: the UTF-16 list above (Emoji before Hebrew). Python's identity sort disagrees with the RFC expected order.

Note: a first attempt wrote the emoji as `"\ud83d\ude00"` inside a Python literal, which is two lone surrogates, not U+1F600. That run failed at UTF-8 encode and was discarded; the result above uses the correct code point.

Command (C-B, number/string/whitespace/duplicate/surrogate probes), exit 0 except the intentional encode failure:
- `json.dumps(1e30)`→`1e+30`; `4.5`→`4.5`; `0.002`→`0.002`; `1e-27`→`1e-27`; `333333333.33333329`→`333333333.3333333` (the five values in the RFC §3.2.3 example output all match).
- `json.dumps(1e-5)`→`1e-05`; `json.dumps(1e16)`→`1e+16`; `json.dumps(1.0)`→`1.0`; `json.dumps(-0.0)`→`-0.0`.
- `json.dumps(float('nan'))`→`NaN`; `float('inf')`→`Infinity` (default `allow_nan=True`).
- `json.dumps(2**64+1)`→`18446744073709551617` (exact int, no double rounding).
- `json.loads('{"a":1,"a":2}')`→`{'a': 2}` (duplicate name silently collapsed).
- `json.dumps("\x00\x08\x09\x0a\x0c\x0d\x1f", ensure_ascii=False)`→`"\u0000\b\t\n\f\r\u001f"`.
- `json.dumps("\ud800", ensure_ascii=False).encode('utf-8')` raises `UnicodeEncodeError` (lone surrogate).

ECMAScript comparison values (`1e-5`→`0.00001`, `1e16`→`10000000000000000`, `1.0`→`1`) are [INFERENCE] from the ECMA-262 §7.1.12.1 rules as recalled; ECMA-262 was not opened this round.

## 4. Verdict on the C3 question

The frozen identity is a deterministic canonical form for its own domain (CPython `json.dumps` on dicts/lists/str/bool/null/plain ints). It is **not** JCS-equivalent in general. Matches and divergences:

Matches JCS:
- Whitespace (§3.2.1): `separators=(',', ':')` emits none.
- Literals and array order (§3.2.2.1, §3.2.3): null/true/false; arrays not reordered; nested dicts sorted recursively.
- Control-character escapes (§3.2.2.2): observed short forms `\b \t \n \f \r` and lowercase `\u00XX` for the tested set.
- Lone surrogate: UTF-8 encode fails (observed), which is consistent with the §3.2.2.2 MUST-terminate rule, but only because the frozen call uses strict encoding; this is incidental, not a designed check.
- Output bytes: UTF-8 (§3.2.4).

Divergences (limits):
1. **Key sort (§3.2.3, Q1). Divergence, observed.** `sort_keys` orders `str` by code point; JCS orders by UTF-16 code units. The two differ only when two keys in one object first differ at a position where one has a supplementary-plane character (U+10000+, surrogate pair in UTF-16) and the other has a BMP character in U+E000–U+FFFF. Reproduced on the RFC test data (C-A).
2. **Number serialization (§3.2.2.3, Q3). Divergence.** Python float repr is not ECMAScript Number::toString. Observed `1.0`→`1.0` (JCS `1`), `-0.0`→`-0.0` (JCS `0`; erratum record on -0 as well), `1e-5`→`1e-05` and `1e16`→`1e+16` (ECMAScript gives plain decimal [INFERENCE]). The RFC's own five example values agree.
3. **NaN / Infinity (§3.2.2.3, Q4). Divergence.** Frozen call does not pass `allow_nan=False`; output `NaN`/`Infinity`, which JCS requires to be an error. Docs for `allow_nan` state the default is `True` (see §5).
4. **Duplicate names (§3.1, Q5). Divergence in input handling.** `json.loads` silently keeps the last duplicate. The identity hashes the parsed in-memory object, not the committed bytes, so a dispatch file with duplicate names, reordered keys, or different whitespace hashes identically to its parsed value. This matches the ledger's own `known_limit` ("payload equals what the ledger hashed"), but it means the ledger binds parsed values, not file bytes.
5. **Big integers (§3.1, I-JSON double requirement). Outside the JCS input domain.** Python keeps `2**64+1` exact; the frozen code neither rejects nor rounds it.
6. **Interoperability.** The identity is CPython-specific. A JCS implementation (e.g. a JavaScript canonicalizer) would not reproduce the same bytes for inputs in items 1–3. Calling it "canonical" is accurate only as "canonical within this tool and domain".

Domain where the frozen form and JCS agree: objects whose keys have no item-1 collision; strings, booleans, null, arrays and objects; numbers that are integers or decimals whose ECMAScript and Python forms coincide (no `-0`, no integral floats written as `x.0`, no exponents outside the plain range); no NaN/Infinity; no duplicate names. [INFERENCE] dispatch payloads (task text, context strings) are probably inside this domain; not measured here. Suggested C3 check for the executor/L1 (not run): count non-string scalars, non-BMP keys and duplicate names in each committed `wave*-dispatch.json`.

Recommendation to L1 (advice only): either rename the identity to a Python-specific name with the domain stated, or make it JCS-equal by (a) sorting by UTF-16 code units, (b) ECMAScript number formatting, (c) rejecting NaN/Infinity/-0 and duplicate names. Choice is L1's.

## 5. Alternative source screened: Python json module documentation

https://docs.python.org/3/library/json.html (opened 2026-10-21; 3.15 docs). Located text: `ensure_ascii` — "all characters will be outputted as-is, except for the characters that must be escaped" (14 words); `allow_nan` — "If True (the default), their JavaScript equivalents (NaN, Infinity, -Infinity) are used." (13 words); `sort_keys` — "If True, dictionaries will be outputted sorted by key." (9 words).

Decision: **REJECTED** for the canonical-form question. Reason: it documents the Python call contract (parameters and defaults), which the frozen code uses, but it specifies no collation order and no number format, so it cannot establish or refute JCS equivalence (items 1–2). Its parameter text is adequate to ground the `allow_nan` default (item 3). Flip condition: admit as a narrow tool-behaviour row (scope: CPython `json.dumps` parameter defaults) if L1 wants a citation for the frozen call's parameters.

## 6. Registry rows (draft; NOT applied to SOURCES.md; L1 integrates)

Column order: id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by

```
| S0xx | RFC 8785 JSON Canonicalization Scheme (JCS) — https://www.rfc-editor.org/rfc/rfc8785 | spec | A | JCS canonical JSON serialization for hashing: whitespace, string escapes, ECMAScript number serialization, UTF-16 property-name sort and UTF-8 output; normative for JCS conformance, Informational independent submission (June 2020) | §3.1 I-JSON input constraints; §3.2.1 Whitespace; §3.2.2.2 Serialization of Strings; §3.2.2.3 Serialization of Numbers and NaN/Infinity note; §3.2.3 Sorting of Object Properties and test data; §3.2.4 UTF-8 Generation; errata record for Section 5 (-0, verified 2024-05-15); rendering not line-pinned; opened 2026-10-21 | A canonical form for hashing needs UTF-16 code-unit key order, ECMAScript number text, no whitespace, error on NaN/Infinity, no duplicate names; -0 is a parser SHOULD-error per the verified errata; a Python json.dumps identity matches JCS only inside a restricted domain. | queued | 2026-10-21 | 365d | — |
| S0xx | Python json module documentation — https://docs.python.org/3/library/json.html | docs | C | CPython json.dumps parameter contract only (sort_keys, separators, ensure_ascii, allow_nan defaults) | ensure_ascii and allow_nan parameter entries in Basic Usage; 3.15 docs page opened 2026-10-21 | REJECTED: documents the frozen call's parameters but specifies no key collation and no number format, so it cannot test JCS equivalence; flip: admit as a narrow tool-behaviour row (tier A, call-contract scope) if L1 needs a citation for the frozen parameters. | rejected | 2026-10-21 | 180d | — |
```

Tier note: the RFC is tier A for the scheme definition (its BCP 14 keywords apply to conforming implementations); "Informational" status does not lower the authority of its definition for JCS conformance, but the row's scope limits claims to the JCS serialization rules. The rejected Python row is tier C because this question asks for a conformance source, and it is not one.

## 7. Recheck commands

- RFC text (recheck when the row's 365d window lapses or the errata record changes): `curl -s https://www.rfc-editor.org/rfc/rfc8785.txt | grep -n "pure value comparisons"` — NOT run in this round (listed for the L1 recheck).
- Sort divergence (run this round, exit 0): `python3 -c 'import json;d={"\U0001F600":1,"\ufb33":2};print(json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(",",":")))'` → `{"דּ":2,"😀":1}` (Hebrew first; RFC/UTF-16 order would put the emoji first).
- Number divergence (run this round): `python3 -c 'import json;print([json.dumps(x) for x in (1.0,-0.0,1e-5,1e16)])'` → `['1.0', '-0.0', '1e-05', '1e+16']`.

## 8. Out of scope / not done

No edit to `corpus/SOURCES.md`, no edit to the frozen inputs, no lane git command. No samples from the round-17 dispatch files were opened or measured (privacy and scope). No tool was installed or updated.

## 9. Findings for L1 (short)

- C3 identity: canonical within CPython `json.dumps` for the restricted domain in section 4; not JCS-equal in general (key collation, number text, NaN/Infinity, -0, duplicate names).
- Source: RFC 8785 admitted as tier A (row drafted); Python json docs rejected for this question (row drafted).
- Recheck command for C3 domain coverage is listed in section 4 but was not executed (requires reading committed dispatch files, outside this item).
