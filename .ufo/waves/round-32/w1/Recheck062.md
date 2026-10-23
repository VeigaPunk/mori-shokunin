# Recheck S062 — RFC 8785 (JCS), round 32 C1

Seat: MoriR32A2.Recheck062. Verdict: **current**.

## 1. Fetch record

- population url: `https://www.rfc-editor.org/rfc/rfc8785`
- redirect: `HTTP/2 301` → `location: https://www.rfc-editor.org/info/rfc8785/` → `HTTP/2 200`,
  `content-type: text/html;charset=utf-8` (command: `curl -sSIL -m 60 https://www.rfc-editor.org/rfc/rfc8785`).
  The info page embeds the complete RFC 8785 text, so the row is still supported at the population url;
  the url cell stays the population url.
- fetch command: `curl -sSL --fail -m 60 https://www.rfc-editor.org/rfc/rfc8785 -o /fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck062/S062.src`,
  exit 0 on first try.
- accessed: `2026-10-23T01:31:23Z` (`date -u +%FT%TZ` at the fetch)
- bytes: **476660**; `sha256 = 4dd9f775b3e6b5977df3e43c56c4e7530be988f9bf8fc0d5b5be202aafae76c9`
- scratch copy: `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck062/S062.src`
  (planner to commit as `corpus/evidence/recheck-r32/S062.src`)
- normalised text: `S062.norm.txt`, 35761 bytes, produced by
  `python3 .ufo/waves/round-32/seat-check.py text S062.src` (offsets below are into that file).

## 2. Ready-to-paste row

```
| S062 | https://www.rfc-editor.org/rfc/rfc8785 | 2026-10-23T01:31:23Z | 4dd9f775b3e6b5977df3e43c56c4e7530be988f9bf8fc0d5b5be202aafae76c9 | "Property name strings to be sorted are formatted as arrays of UTF-16"; "Whitespace between JSON tokens MUST NOT be emitted."; "occurrences of NaN or Infinity MUST cause a compliant JCS implementation to terminate with an appropriate error" | current |
```

## 3. Quotes → teaches-cell facts

Teaches cell: "A canonical form for hashing needs UTF-16 code-unit key order, ECMAScript number text, no
whitespace, error on NaN/Infinity, no duplicate names; -0 is a parser SHOULD-error per the verified errata;
a Python json.dumps identity matches JCS only inside a restricted domain."

- Q1 `Property name strings to be sorted are formatted as arrays of UTF-16` (12 words, norm offset 12182,
  §3.2.3; the page continues `[ UNICODE ] code units`, so the quote stops on the whole token `UTF-16`).
  Bears on **UTF-16 code-unit key order**; the following sentence in the copy adds "The sorting is based on
  pure value comparisons, where code units are treated as unsigned integers". Supports `current`.
- Q2 `Whitespace between JSON tokens MUST NOT be emitted.` (8 words, offset 7433, §3.2.1).
  Bears on **no whitespace** verbatim, negation preserved. Supports `current`.
- Q3 `occurrences of NaN or Infinity MUST cause a compliant JCS implementation to terminate with an
  appropriate error` (17 words, offset 10902, §3.2.2.3 note). Bears on **error on NaN/Infinity** verbatim.
  Supports `current`.

Other teaches clauses checked against the same copy (not quoted, to stay within 3 quotes):

- no duplicate names, §3.1, offset 6167: `JSON objects MUST NOT exhibit duplicate property names.`
- ECMAScript number text, §3.2.2.3, offset 10104: `Such data MUST be serialized according to Section 7.1.12.1 of [ ECMA-262 ] , including the "Note 2" enhancement.`
- string escapes, §3.2.2.2 (offset ~10000): invalid/lone-surrogate data `MUST cause a compliant JCS implementation to terminate with an appropriate error`.
- UTF-8 output, §3.2.4, offset 14691: `the result of the preceding step MUST be encoded in UTF-8.`
- `-0` errata: fetched live `https://errata.rfc-editor.org/eid7920/` (`Status: Verified`, `Type: Technical`,
  `Date Verified: 2024-05-15`, `Section 5 says: <end of section>` / `It should say: Since -0 is a valid JSON
  Number but is serialized as 0, a JSON parser following this specification SHOULD generate an error
  condition ... when it encounters -0`). The errata search page
  (`https://errata.rfc-editor.org/search/?rfc_number=8785&presentation=records`) shows `Verified (2)`, and the
  RFC info page carries `Errata 2`. Matches the teaches clause exactly, so it is still verified, not drifted.
- second errata eid6292 is Editorial and Verified (`Section 3.2.2.2 says: see Section 24.3.2.2 of
  [ECMA-262]` / `It should say: ... 24.5.2.2`); it changes a pointer, not the teaches content.
- metadata unchanged: page shows `Informational`, "This is a contribution to the RFC Series, independently of
  any other RFC stream.", `Copyright (c) 2020`; no `Obsolet`/`Updates` markers anywhere in the copy (0 hits),
  so RFC 8785 is not superseded.
- "Python json.dumps identity only in a restricted domain" is grounded in the same §3.2.2.3/Appendix B
  number rules; the copy's Appendix B note bounds true integers to `-9007199254740991` to `9007199254740991`,
  which is what restricts the identity.

## 4. seat-check output

```
$ timeout 300 python3 .ufo/waves/round-32/seat-check.py row S062 S062.src '"Property name strings to be sorted are formatted as arrays of UTF-16"; "Whitespace between JSON tokens MUST NOT be emitted."; "occurrences of NaN or Infinity MUST cause a compliant JCS implementation to terminate with an appropriate error"'
sha256=4dd9f775b3e6b5977df3e43c56c4e7530be988f9bf8fc0d5b5be202aafae76c9
quotes=3 words=[12, 8, 17] in_copy=[True, True, True]
shared_tokens=['error', 'infinity', 'json', 'name', 'property', 'strings', 'whitespace'] topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
```

## 5. Drift details

None. Verdict `current`, so no `Round32` correction is due for `corpus/knowledge/dispatch-ledger-r18.md`.
The only observable change is presentation: the plain `/rfc/rfc8785` path now 301s to the `/info/rfc8785/`
HTML page, which still contains the whole RFC body (and the `Errata 2` link); the population row already says
"rendering not line-pinned", and every teaches clause is present verbatim in the live bytes, so this is not a
teaches-level change.

## 6. Bounds / hygiene

- Wrote only this report and files under `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck062/`; no git/jj
  writes, no lane mutations.
- Every command ran under `timeout`; no background jobs, no subagents, no processes left running.
- Tool installs: none (curl, python3, sha256sum already present).
