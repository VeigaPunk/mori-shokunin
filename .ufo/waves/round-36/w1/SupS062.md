measured 2026-10-23T12:03:54Z

# S062 source re-open

## Behavior and provenance

- At lane tip `6bd57097`, `S062` is the RFC 8785 spec row, status `mined`, opened `2026-10-21`, recheck `365d`, used by `corpus/knowledge/dispatch-ledger-r18.md`; the row was read from `timeout 120 git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 6bd57097:corpus/SOURCES.md` (successful output, S062 row). The same row is at `corpus/SOURCES.md:68`.
- `ScoutAppendDebt.md:27` names first publication `daceeec8`. `timeout 120 git -C /home/vgpnk/Projects/shokunin/mori-shokunin show daceeec8:corpus/SOURCES.md` returned the first-published S062 row; it had `no whitespace`, `-0 is a parser SHOULD-error per the verified errata`, and the Python `json.dumps` restricted-domain clause. The tip row changes the whitespace phrase to `no whitespace between JSON tokens` and labels both the `-0` and Python clauses `lane rule:`.
- `timeout 120 git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree -r --name-only 6bd57097 -- corpus/knowledge/dispatch-ledger-r18.md` returned `corpus/knowledge/dispatch-ledger-r18.md`; proposed used-by path exists at tip.
- Opened the exact tip URL `https://www.rfc-editor.org/rfc/rfc8785` with ordinary curl; HTTP 200, no challenge. Also fetched its official text rendition and the RFC Editor errata record for line-numbered review. No tools were installed or updated.

## Evidence and gates

The numbered locations below are lines of the saved official RFC text rendition. Each quotation is contiguous in the source text and at most 25 words.

- §1 hashable output, RFC 8785 text lines 100–101: “representation of JSON data that can be used by cryptographic methods.”
- §3.1 I-JSON input constraints, line 185: “JSON objects MUST NOT exhibit duplicate property names.”
- §3.2.1 whitespace, line 217: “Whitespace between JSON tokens MUST NOT be emitted.”
- §3.2.2.2 string escaping, lines 262–264: “If the Unicode value falls within the traditional ASCII control character range (U+0000 through U+001F), it MUST be serialized using lowercase hexadecimal Unicode notation”
- §3.2.2.3 number serialization, lines 285–286: “Such data MUST be serialized according to Section 7.1.12.1 of [ECMA-262]”
- §3.2.2.3 NaN/Infinity note, lines 297–299: “occurrences of NaN or Infinity MUST cause a compliant JCS implementation to terminate with an appropriate error.”
- §3.2.3 sorting, lines 332–334: “Property name strings to be sorted are formatted as arrays of UTF-16 [UNICODE] code units.”
- §3.2.3 test data, lines 365–366: “The following JSON test data can be used for verifying the correctness of the sorting scheme in a JCS implementation:”
- §3.2.4 UTF-8 output, lines 399–400: “the result of the preceding step MUST be encoded in UTF-8.”
- RFC Editor erratum 7920 for Section 5, verified 2024-05-15; saved response lines 178–199. Lines 195–196 say: “Since -0 is a valid JSON Number but is serialized as 0, a JSON parser following this specification SHOULD generate an error condition”. The record is marked Verified at `S062.errata.src:125-180`.

HTTP and byte evidence:

- `timeout 120 curl -sS -L -o /fast/scratch/hyaku/mori-r36/SupS062/S062.src -w 'HTTP %{http_code}\n' https://www.rfc-editor.org/rfc/rfc8785` → `HTTP 200`; `timeout 120 sha256sum /fast/scratch/hyaku/mori-r36/SupS062/S062.src` → `a0f3ccdf5e85ec2de043923f53e7aa96cf99e3587264bf941c9af506f075b434`.
- `timeout 120 curl -sS -L -o /fast/scratch/hyaku/mori-r36/SupS062/S062.txt.src -w 'HTTP %{http_code}\n' https://www.rfc-editor.org/rfc/rfc8785.txt` → `HTTP 200`; hash → `63d52294eb0e3f0014174288186d388b4ddbf2c67d1ce8af1d9726eb0c3ab240`.
- `timeout 120 curl -sS -L -o /fast/scratch/hyaku/mori-r36/SupS062/S062.errata.src -w 'HTTP %{http_code}\n' 'https://errata.rfc-editor.org/search/?rfc_number=8785&presentation=records'` → `HTTP 200`; `timeout 120 sha256sum /fast/scratch/hyaku/mori-r36/SupS062/S062.errata.src` → `a6b93b847a0c74ffb89760521d574150e6ec65cfa5fcd3c1551cccc91e4acbfa`.

## Finding

The RFC and verified erratum support the JCS claims about hashable output, I-JSON input, token whitespace, string escapes, ECMAScript number serialization, UTF-16 code-unit sorting, UTF-8 output, NaN/Infinity errors, and the Section 5 `-0` parser recommendation. The tip teaches clause `a Python json.dumps identity matches JCS only inside a restricted domain` is not stated by the RFC or erratum; it is unsupported by these opened source bytes. This does not establish that the Python claim is false. The corrected draft omits it. S062 therefore does not hold as written, while the narrowed source is suitable for admission.

VERDICT: unsupported

## Drafts for L1

DRAFT corpus/SOURCES.md
```
| S2NN | RFC 8785 JSON Canonicalization Scheme (JCS) — https://www.rfc-editor.org/rfc/rfc8785 | spec | A | JCS canonical JSON serialization for hashing: whitespace, string escapes, ECMAScript number serialization, UTF-16 property-name sort and UTF-8 output; normative for JCS conformance, Informational independent submission (June 2020) | §1 hashable output:93-102; §3.1 I-JSON input constraints:174-204; §3.2.1 Whitespace:215-217; §3.2.2.2 Serialization of Strings:256-280; §3.2.2.3 Serialization of Numbers and NaN/Infinity note:282-299; §3.2.3 Sorting of Object Properties and test data:301-376; §3.2.4 UTF-8 Generation:397-400; erratum 7920 Section 5 (-0), verified 2024-05-15, response lines 135-199 | supersedes S062 — JCS yields a hashable JSON representation using UTF-16 code-unit property sorting and ECMAScript number serialization, no whitespace between JSON tokens, specified string escapes, UTF-8 output, and duplicate-name-free I-JSON input; NaN and Infinity cause errors. Verified erratum 7920 says a parser SHOULD generate an error condition on -0. | mined | 2026-10-23 | 365d | corpus/knowledge/dispatch-ledger-r18.md |
```

DRAFT corpus/lessons/round-36.md §Gate
```
| S2NN | https://www.rfc-editor.org/rfc/rfc8785; text rendition https://www.rfc-editor.org/rfc/rfc8785.txt; erratum https://errata.rfc-editor.org/search/?rfc_number=8785&presentation=records | 2026-10-23 | RFC page SHA-256 a0f3ccdf5e85ec2de043923f53e7aa96cf99e3587264bf941c9af506f075b434; text SHA-256 63d52294eb0e3f0014174288186d388b4ddbf2c67d1ce8af1d9726eb0c3ab240; errata SHA-256 a6b93b847a0c74ffb89760521d574150e6ec65cfa5fcd3c1551cccc91e4acbfa | representation of JSON data that can be used by cryptographic methods — RFC text 100-101; JSON objects MUST NOT exhibit duplicate property names — RFC text 185; Whitespace between JSON tokens MUST NOT be emitted — RFC text 217; If the Unicode value falls within the traditional ASCII control character range (U+0000 through U+001F), it MUST be serialized using lowercase hexadecimal Unicode notation — RFC text 262-264; Such data MUST be serialized according to Section 7.1.12.1 of [ECMA-262] — RFC text 285-286; occurrences of NaN or Infinity MUST cause a compliant JCS implementation to terminate with an appropriate error — RFC text 297-299; Property name strings to be sorted are formatted as arrays of UTF-16 [UNICODE] code units — RFC text 332-334; The following JSON test data can be used for verifying the correctness of the sorting scheme in a JCS implementation — RFC text 365-366; the result of the preceding step MUST be encoded in UTF-8 — RFC text 399-400; Since -0 is a valid JSON Number but is serialized as 0, a JSON parser following this specification SHOULD generate an error condition — verified erratum 7920 response 195-196 | admit A, mined as S2NN; omit the unsupported Python json.dumps clause from S062 |
```

## Touched surfaces and limits

- Lane write: this scoped report only, `.ufo/waves/round-36/w1/SupS062.md`. No edits to `corpus/SOURCES.md`, lessons, judge, or Git index; both drafts are report text for L1.
- Scratch artifacts: `/fast/scratch/hyaku/mori-r36/SupS062/S062.src`, `/fast/scratch/hyaku/mori-r36/SupS062/S062.txt.src`, and `/fast/scratch/hyaku/mori-r36/SupS062/S062.errata.src`; hashes and HTTP statuses are above. All were well under the 10 MB write limit.
- No Python `json.dumps` behavior test, code change, build, or test was run. The Python clause remains an out-of-scope source claim, not a falsified behavior claim.
