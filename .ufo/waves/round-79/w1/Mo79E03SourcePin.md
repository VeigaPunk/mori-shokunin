# Mo79E03SourcePin — round 79 w1 C3

Axes: operability, calibration, freshness. This seat supplies source-opening evidence for freshness, not a closure verdict.

## 1. Work and files
1. Swept the existing registry: 366 source rows; exact URL absent. Initial sweep preceded fetch but was not persisted first; corrective sweep was persisted before corrective fetch.
2. Fetched the exact RFC Editor URL using curl into `corpus/evidence/sources-r79/rfc9111.txt` (verbatim). HTTP/2 200; media type text/plain;charset=utf-8; 84477 bytes; sha256 `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`.
3. Located title `HTTP Caching` at line 14 and body §4.1 heading at line 526 (TOC heading at 82). First body line is BOM-only, not the title; bytes unchanged.
4. Ran requested anchor checks: six PASS, wrong-line FAIL rc 1. Actual tool grammar from --help is `LABEL|LINE|WORDS|TEXT`, not `line:quote`.
5. Removed own scratch; `test ! -e /fast/scratch/hyaku/mori-r79/Mo79E03SourcePin` rc 0.

Changed files only:
- `corpus/evidence/sources-r79/rfc9111.txt`
- `.ufo/waves/round-79/evidence/source-rfc9111-r79.txt`
- `.ufo/waves/round-79/w1/Mo79E03SourcePin.md`

## 2. Sweep evidence
```text
$ grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
366
rc=0

$ grep -nFi rfc9111 /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
rc=1

$ grep -nFi 9111 /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
129:| S123 | systemd v262 journal JSON field encoder and printable-UTF-8 rule — https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/logs-show.c ; https://raw.githubusercontent.com/systemd/systemd/v262/src/basic/utf8.c ; https://raw.githubusercontent.com/systemd/systemd/v262/src/basic/utf8.h | code | A | the encoder that produces `journalctl -o json` field values at the v262 release tag: the 4096-byte null threshold, the printable check that decides string versus byte array, and the definition of "printable"; the file that builds the JSON object only, not the journal's own storage or matching code | src/shared/logs-show.c:43 (`JSON_THRESHOLD 4096U`), :1124-1131 (null / string / `sd_json_variant_new_array_bytes` decision); src/basic/utf8.h:23-24 (`utf8_is_printable` macro); src/basic/utf8.c:30-40 (`unichar_is_control`), :105-127 (`utf8_is_printable_newline`); tag v262 = commit 8cc40e0c5e9234bf45084751ac53b1fbfe70b492; sha256 logs-show.c abc2fc1f3d6f10d0f01b4d1ff18689eb5561a98fd71fde911117ce16c50ed72f, utf8.c 7cbebe621330509d7ed4928ea0e8374cf7155e954fee2745ebf08b90cd030d27, utf8.h 2adc446e1e5d13f497b59f6e2fe1c02752b022cc7eaec35393f87689c6ea297a; HTTP 200 on 2026-10-22 | A field is a JSON string only when it is valid UTF-8 and carries no control character other than tab or newline; other C0 controls, DEL, the C1 range and invalid UTF-8 yield a byte array, and a field whose name plus value reaches 4096 bytes yields null instead. | mined | 2026-10-22 | on-release | corpus/knowledge/userspace-oom-killers-r26.md |
rc=0

$ grep -nFi 'HTTP Caching' /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
rc=1

$ grep -nFi Vary /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
360:| S579 | Token use in AWS WAF intelligent threat mitigation — https://docs.aws.amazon.com/waf/latest/developerguide/waf-tokens.html | docs | A | bot-management session-token semantics (the AWS WAF class): a mitigation token is a per-client-session artifact the mitigation creates, updates and encrypts for clients that answer its challenges, and the client carries it on every request | "token, sometimes called a fingerprint, is a collection of information about a single client" (`S579.html:49`, 14 words; sentence opens with "A" at the end of `:48`) + continuation `:50` ("session that the client stores and provides with every web request that it sends", 14 words); section heading `:48`; "AWS WAF creates, updates, and encrypts tokens for clients that successfully respond to silent challenges" `:56`; copy `corpus/evidence/sources-r68/S579.html` sha256 `41b601f1da6ad11b5cfb167c5e64c780c15b83b7609caac4e9d8fefeafda7a9e` (14127 bytes, opened 2026-11-01) | a mitigation token is serving machinery bound to the request/response exchange, not page identity — token-bearing served bytes are expected to vary per response, which is what the instrument-UA A/A separation receipts (the r68 ua-variance probe; QUALITY 159's vendor scoping untouched: no grammar taught, no row re-classed) | mined | 2026-11-01 | 180d | corpus/lessons/round-68.md |
rc=0

$ grep -nFi https://www.rfc-editor.org/rfc/rfc9111.txt /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
rc=1

$ grep -nE '^\| S(042|591|592|593) ' /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
48:| S042 | RFC 9110 HTTP Semantics — https://www.rfc-editor.org/rfc/rfc9110#section-10.2.3 | spec | A | Retry-After response-header semantics | §10.2.3 Retry-After; Standards Track, June 2022; opened 2026-10-20 | Retry-After indicates how long a user agent ought to wait before a follow-up request; this section is not proof of a client retry implementation. | queued | 2026-10-20 | 365d | — |
372:| S591 | Acquiring high-resolution time stamps — https://learn.microsoft.com/en-us/windows/win32/sysinfo/acquiring-high-resolution-time-stamps | docs | A | the Windows-platform ground of the schedule clock realization, continuing S589: the vendor QPC guidance for reading THIS host rotation receipts — QPC is monotonic and completely independent of the system time and UTC, so the receipt window_s/wall_s differences ride a clock that neither goes backwards nor moves with system-time or timezone changes | "Yes. QPC does not go backward." (`S591.html:918`, 6 words) + "is completely independent of the system time and UTC." (`:863`, 9 words — the sentence subject QPC sits inside a strong tag on the same line, so the located contiguous span starts at "is"); page `<title>` "Acquiring high-resolution time stamps - Win32 apps" in the pinned head (the pinned head also carries the site-suffix naming Microsoft Learn; its separator character is deliberately not spelled in this row so no field split can occur); copy `corpus/evidence/sources-r76/S591.html` sha256 `233893693810754dbd4122a9a43320596a381e179a38ade6636e294d2dbffc1c` (106427 bytes, opened 2026-11-02; duplicate sweep INSIDE `.ufo/waves/round-76/evidence/source-s591-r76.txt` BEFORE the fetch — no registry row is this page, S589's row mentions the QPC note only inside the Python time page at its `:529` located-unopened; the resolved title checked before the pin per the r75 lesson rule; anchors machine-verified by the r72 anchor-checker: PASS items=2 rc 0, able-to-fail mislocation arm FAIL rc 1, `.ufo/waves/round-76/evidence/s591-anchor-check-r76.txt`) | grounds WHAT the Windows-host monotonic clock is under the Python docs naming (S589 `:529` names the calls); it decides no TTL value and pins no per-machine accuracy number (QPC frequency is runtime-queried); the lane still prints differences only, never an absolute stamp | mined | 2026-11-02 | 180d | corpus/knowledge/rotation-receipt-grammar-r76.md, corpus/lessons/round-76.md |
373:| S592 | typeperf (Windows Commands reference) — https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/typeperf | docs | A | the read command the counter probe executes: the command writes performance data to the command window or to a log file, the -sc sample bound, and the -q installed-counter enumeration — the documented read grammar of the PDH counter surface | "command writes performance data to the command window or to a log file." (`S592.html:749`, 13 words — the sentence subject sits inside a strong tag on the same line, so the located contiguous span starts at "command"); "Specifies the number of samples to collect." (`:806`, 7 words); "Display a list of installed counters (no instances). To list counters for one object, include the object name." (`:798`, 18 words) | grounds `tools/mori-counter-win.py` (round 77): the commit gauge pair (Memory Committed Bytes, Memory Commit Limit), the in-use share and the paging-activity rate read ONCE through the documented command — the Windows-host continuation of the r53 Linux commit-runway read; the counter paths are NOT doc-located — they are live-enumerated on THIS host by the documented -q listing (enumeration receipt, round 77) and pinned in the instrument; a gauge or rate sample is volatile, one-shot, and never a cause | mined | 2026-11-02 | 180d | corpus/knowledge/counter-win-r77.md, corpus/lessons/round-77.md, corpus/knowledge/counter-semantics-r78.md |
374:| S593 | Memory Performance Information (Windows desktop legacy) — https://learn.microsoft.com/en-us/previous-versions/windows/desktop/legacy/aa965225%28v%3Dvs.85%29 | docs | A | the vendor's own association of the memory-object performance-counter names with the memory-manager structures: Committed Bytes to PERFORMANCE_INFORMATION.CommitTotal; Commit Limit to MEMORYSTATUSEX.ullTotalPageFile and PERFORMANCE_INFORMATION.CommitLimit | "This topic associates performance counters with the data returned by memory performance functions and the Windows Task Manager" (`S593.html:713`, 18 words); "The following table associates memory object performance counters with the data returned by the memory performance functions in the" (`:720`, 19 words — the sentence continues through three linked structure names on the same line, so the located contiguous span ends at "the", recorded as such); "Memory object counter (unless otherwise noted)" (`:730`, 6 words); "Committed Bytes" (`:750`, 2 words); "Commit Limit" (`:756`, 2 words) | grounds `corpus/knowledge/counter-semantics-r78.md` (round 78): the counter NAMES the r77 probe reads are the vendor's memory-object counter names (the K4 object ground no longer only inferred from S572's exhaustion-event semantics), and the vendor table itself links the counter surface to S574's struct (the r64 API approximation reads the same quantity family — vendor-stated, not lane-inferred); Pages/sec is NOT on this page (named absent — the rate semantics stay as landed in counter-win-r77 K5, live-verified); the resolved page title carries "Memory Performance Information (Windows)" with the Microsoft Learn site suffix in the pinned head (its separator character deliberately not spelled in the row so no pipe can split the row — the r76 title-pipe mistake's standing fix); a previous-versions archive page — the recheck cell governs its drift watch | mined | 2026-11-02 | 180d | corpus/knowledge/counter-semantics-r78.md, corpus/lessons/round-78.md |
rc=0

Interpretation: exact RFC9111 URL, rfc9111 and HTTP Caching have no matches. The 9111 hit is S123 digest text, not HTTP caching. Case-insensitive Vary also matches S579 (substring); that held AWS token row is mechanism context, not normative cache selection. S042 is queued HTTP Semantics (Retry-After); mined S591/S592/S593 are empirical ua-serving neighbours.

```
All hits are retained untruncated in the receipt. S123's 9111 substring is inside a digest, not an RFC reference. Case-insensitive Vary additionally hits S579, an AWS token-context row; the initial case-sensitive Vary sweep had no hits. Nearest held empirical rows are mined S591/S592/S593; S042 is queued HTTP Semantics/Retry-After, not normative Vary selection. No exact URL duplicate was found at sweep time.

## 3. Quotes (single-line contiguous spans)
| Pin line | wc -w | Verbatim text |
|---|---|---|
| 529 | 10 | `response and that stored response contains a Vary header field` |
| 530 | 11 | `(Section 12.5.5 of [HTTP]), the cache MUST NOT use that stored` |
| 531 | 9 | `response without revalidation unless all the presented request header` |
| 532 | 12 | `fields nominated by that Vary field value match those fields in the` |
| 536 | 13 | `The header fields from two requests are defined to match if and only` |
| 557 | 5 | `"*" always fails to match.` |

## 4. Anchor-check transcript
```text
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-anchor-check.py --help
usage: mori-anchor-check [-h] [--pin PIN] [--check CHECK] [--selftest]

Verify recorded quote anchors (line + word count) against a pinned copy.

options:
  -h, --help     show this help message and exit
  --pin PIN      path to the pinned copy (required unless --selftest)
  --check CHECK  LABEL|LINE|WORDS|TEXT (WORDS '-' skips the count arm;
                 repeatable)
  --selftest     run the offline selftest and exit
rc=0

$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-anchor-check.py --pin /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r79/rfc9111.txt --check 'Q1|529|10|response and that stored response contains a Vary header field' --check 'Q2|530|11|(Section 12.5.5 of [HTTP]), the cache MUST NOT use that stored' --check 'Q3|531|9|response without revalidation unless all the presented request header' --check 'Q4|532|12|fields nominated by that Vary field value match those fields in the' --check 'Q5|536|13|The header fields from two requests are defined to match if and only' --check 'Q6|557|5|"*" always fails to match.'
anchor item=Q1 span=529 verdict=ok located_on=529 occurrences=1 words_counted=10 words_recorded=10
anchor item=Q2 span=530 verdict=ok located_on=530 occurrences=1 words_counted=11 words_recorded=11
anchor item=Q3 span=531 verdict=ok located_on=531 occurrences=1 words_counted=9 words_recorded=9
anchor item=Q4 span=532 verdict=ok located_on=532 occurrences=1 words_counted=12 words_recorded=12
anchor item=Q5 span=536 verdict=ok located_on=536 occurrences=1 words_counted=13 words_recorded=13
anchor item=Q6 span=557 verdict=ok located_on=557 occurrences=1 words_counted=5 words_recorded=5
ANCHOR_CHECK: PASS items=6 ok=6 pin_sha256=aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e pin_bytes=84477
rc=0

$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-anchor-check.py --pin /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r79/rfc9111.txt --check 'wrong-line|530|10|response and that stored response contains a Vary header field'
anchor item=wrong-line span=530 verdict=mislocated located_on=- occurrences=0 words_counted=- words_recorded=10
ANCHOR_CHECK: FAIL items=1 ok=0 mislocated=1 wordcount_mismatch=0 pin_sha256=aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e pin_bytes=84477
rc=1

```
Complete command/output evidence, including fetch facts, grep line locations, individual wc -w commands and cleanup:
`.ufo/waves/round-79/evidence/source-rfc9111-r79.txt`.

## 5. Limits, own defects, handoff
- Source scope is conditional cache reuse under Vary. No observed vendor Vary: User-Agent header, compliance verdict, or empirical serving-cause proof follows from this source alone.
- Own ordering defect: first sweep was not written into receipt before first fetch; corrective sweep/fetch sequence is prospectively receipted. No claim that this erases the initial defect.
- Own redaction defect: full response-header capture briefly included unneeded session-header material in the receipt. Removed that entire retained block immediately, replaced with status/content-type allowlist, deleted scratch headers; no values reproduced here. Sentinel notified.
- Tool-output defect: named process read returned sibling scratch output for the fetch service; reported to tool QA and did not use it as fetch evidence. Corrective finite subprocess run retained actual command/output pairs.
- No LSP symbol work applies: this assignment adds source/evidence text, not a symbol refactor.
- No installs, builds, linters, formatters, selftests, census or closure counters run. Parent owns integration gates. SOURCES.md, knowledge entry and index are sibling/L1 scope, intentionally unedited.
- Pin identity sent to S594-row and entry authors. No unresolved source-opening blocker; parent should run integrated receipt guard/C3/census and review the disclosed process defects.

## 6. Self-evaluation
Accuracy 4 (exact pin/hash and six anchors; conditional scope explicit). Completeness 3 (initial receipt-order defect remains historical). Clarity 4 (full commands in one evidence receipt; summary here). Actionability 4 (pin identity and precise anchors supplied; integration belongs to parent). Conciseness 3 (sweep/anchor excerpts duplicate retained evidence). Overall 3.6/5. Highest-impact improvements: persist sweep before any first fetch, allowlist headers before capture, avoid named bash services for finite commands. User agreement is not assumed.
