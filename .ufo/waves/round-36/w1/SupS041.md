measured 2026-10-23T12:05:41Z

# SupS041 — S041 append-only supersede

## Behavior
- Detection/reporting only. No product behavior or lane registry was changed; the replacement row and Gate entry below are drafts for L1.

## Gates and findings
- At lane tip `6bd57097`, `timeout 120 git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 6bd57097:corpus/SOURCES.md | grep '^| S041 '` returned S041 with source RFC 6585, kind `spec`, tier `A`, scope `HTTP 429 Too Many Requests status meaning`, anchor `§4, plain-text lines 132–135`, teaches `HTTP 429 denotes too many requests in a time window; lane rule: it does not identify a vendor business error or establish permanent seat death.`, status `mined`, opened `2026-10-20`, recheck `365d`, and used-by `corpus/knowledge/seat-terminal-status-r17.md`.
- First-published row: `timeout 120 git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 273aa74a:corpus/SOURCES.md | grep '^| S041 '` returned the same cells except the teaches cell did not contain `lane rule:`. `ScoutAppendDebt.md:21` records the in-place addition at `62db24c0`; `ScoutAppendDebt.md:59` classifies S041 as a defect. Thus the routed append-only defect is confirmed.
- `timeout 120 git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree -r --name-only 6bd57097 -- corpus/knowledge/seat-terminal-status-r17.md` returned `corpus/knowledge/seat-terminal-status-r17.md`; the draft retains this single existing used-by path.
- Reopened the exact tip URL with `curl --location --silent --show-error --output /fast/scratch/hyaku/mori-r36/SupS041/S041.src --write-out "HTTP_STATUS=%{http_code}\n" https://www.rfc-editor.org/rfc/rfc6585`: HTTP 200. `sha256sum /fast/scratch/hyaku/mori-r36/SupS041/S041.src` returned `cc0123160b49d4abce57f51a1d56c02745afc61d29dd20c0e51fc42bb5f5d968`.
- The fetched original URL is HTML; matching section text is at `S041.src:245–246`. For the cited plain-text locator, fetched `https://www.rfc-editor.org/rfc/rfc6585.txt` with curl: HTTP 200; `/fast/scratch/hyaku/mori-r36/SupS041/S041.txt:134–135` reads `The 429 status code indicates that the user has sent too many requests in a given amount of time (rate limiting).` The source’s corresponding HTML section reads the same text with HTML-escaped quotation marks.
- The §4 quote supports the status meaning and the anchor. The RFC does not classify vendor business errors or seat permanence; the tip explicitly marks that caveat as a lane rule. Search `vendor|business|seat|permanent` in the fetched plaintext returned no matches. [INFERENCE] I treat that caveat as local policy, not RFC teaching; the replacement wording makes that attribution explicit.

VERDICT: supported

## DRAFT SOURCES row
```text
| S2NN | RFC 6585 Additional HTTP Status Codes — https://www.rfc-editor.org/rfc/rfc6585 | spec | A | HTTP 429 Too Many Requests status meaning | §4, plain-text lines 132–135; Standards Track, April 2012; opened 2026-10-23 | supersedes S041 — RFC 6585 defines 429 as too many requests in a given amount of time (rate limiting); mori lane rule: do not infer vendor business error or permanent seat death from status 429 alone. | mined | 2026-10-23 | 365d | corpus/knowledge/seat-terminal-status-r17.md |
```

## DRAFT round-36 lesson Gate row
```text
| S2NN | https://www.rfc-editor.org/rfc/rfc6585 (accessed 2026-10-23) | cc0123160b49d4abce57f51a1d56c02745afc61d29dd20c0e51fc42bb5f5d968 | (19 words) The 429 status code indicates that the user has sent too many requests in a given amount of time — RFC 6585 §4, plain-text lines 134–135; matching HTML body at S041.src:245–246 | admit, A; the cited meaning is supported and the remaining caveat is local lane policy |
```

## Touched surfaces and artifact paths
- Report written only at `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/w1/SupS041.md`.
- Reopened source bytes: `/fast/scratch/hyaku/mori-r36/SupS041/S041.src` — HTTP 200, SHA-256 `cc0123160b49d4abce57f51a1d56c02745afc61d29dd20c0e51fc42bb5f5d968`.
- Plain-text locator copy: `/fast/scratch/hyaku/mori-r36/SupS041/S041.txt` — HTTP 200, SHA-256 `f6d55d1b491cd515c35827cf9181753b23b2a68c4df14e56d83dc445b3876e58`.

## Out of scope and limits
- No edits to `corpus/SOURCES.md` or other product files; no git/index writes, tests, build, or tool installation.
- The source Gate judgment is for the RFC’s 429 meaning. The lane-policy caveat remains mori policy, not a claim established by RFC 6585.
