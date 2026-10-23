measured 2026-10-23T12:03:48Z

# SupS051 — round 36, wave 1

## Behavior and provenance

- `.ufo/waves/round-35/w2/ScoutAppendDebt.md:25` identifies first publication `daceeec8`, the in-place edit at `62db24c0`, and the change: `lane rule:` was inserted before `A class-hit gate` in teaches.
- `timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 6bd57097:corpus/SOURCES.md | grep '^| S051 '` returned the tip row. `timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin show daceeec8:corpus/SOURCES.md | grep '^| S051 '` returned first-published cells. The tip appends `lane rule:`; source, kind, tier, scope, anchor, status, opened, recheck, and used-by otherwise match the first-published row.
- Model rows inspected with `git show 6bd57097:corpus/SOURCES.md | grep '^| S201 '` and `... | grep '^| S073 '`. `timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree --name-only 6bd57097 -- corpus/knowledge/evidence-minimization-r18.md` returned that used-by path.
- `timeout 120s date -u +%FT%TZ` → `2026-10-23T12:03:48Z`.

## Reopened evidence and findings

- `timeout 120s sh -c 'mkdir -p /fast/scratch/hyaku/mori-r36/SupS051 && curl --location --silent --show-error --output /fast/scratch/hyaku/mori-r36/SupS051/S051.src --write-out "HTTP_STATUS=%{http_code}\n" https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-122.pdf && sha256sum /fast/scratch/hyaku/mori-r36/SupS051/S051.src'` → HTTP 200; SHA-256 `555b9df82af12de4ca887efc21c0a9e159a14485d5d570f44b32ef15c6c62470`.
- `timeout 120s pdftotext -layout /fast/scratch/hyaku/mori-r36/SupS051/S051.src /fast/scratch/hyaku/mori-r36/SupS051/S051.txt` completed without output; line references below are to this extraction, not native PDF line numbers.
- The NIST landing page was re-opened with `read` and fetched by `curl` on 2026-10-23; the curl returned HTTP 200 and SHA-256 `31a68678ce17854710c068e222be47f18b2dca0aae020ead72dd46eb7bca1b5f` for `/fast/scratch/hyaku/mori-r36/SupS051/S051.landing.html`.
- ES-2 locator: `Organizations should minimize the use, collection, and retention of PII to what is strictly necessary to accomplish their business purpose and mission.` — PDF extraction lines 249–250. The text is on ES-2, but it is body text, not a heading; the actual `Executive Summary` heading is at line 182. The tip locator word `heading` fails.
- §4.2.1 locator: `If the PII serves no current business purpose, then the PII should no longer be used or collected.` — PDF extraction lines 1250–1251. Section title is at line 1242; printed page 4-3 appears at line 1277, its continuation is at lines 1282–1284, and printed page 4-4 at line 1339. The cited page span is supported.
- Date locator: landing HTML line 429 says `Date Published: April 2010`; line 514 says `04/06/10: SP 800-122 (Final)`. The tip's date/history is supported by the reopened landing page.
- Teaches: the no-current-purpose sentence is supported at PDF extraction lines 1250–1251; periodic review is supported by `Develop a schedule for periodic review of PII holdings` at line 260; disposal under schedules is supported by `The effective management and prompt disposal of PII, in accordance with NARA-approved disposition schedules, will minimize the risk of unauthorized disclosure.` at lines 1283–1284. `Lane rule:` explicitly attributes the class-hit clause to lane policy, not to NIST.

## Drafts for L1

DRAFT corpus/SOURCES.md
```text
| S2NN | NIST SP 800-122, Guide to Protecting the Confidentiality of Personally Identifiable Information (PII) — https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-122.pdf | docs | A | PII minimum-necessary collection, use and retention; federal-agency guidance with voluntary non-federal use (§1.1) | ES-2 text: Organizations should minimize the use, collection, and retention of PII; §4.2.1 printed pp. 4-3 to 4-4; April 2010 final, document history 04/06/10; landing page https://csrc.nist.gov/pubs/sp/800/122/final opened 2026-10-23 | supersedes S051 — Retention needs a current-business-purpose test per item: PII with no current purpose should no longer be used or collected; holdings need periodic review and disposal under schedules. Lane rule: A class-hit gate does not by itself establish necessity. | mined | 2026-10-23 | 365d | corpus/knowledge/evidence-minimization-r18.md |
```

DRAFT corpus/lessons/round-36.md
```text
| S2NN | https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-122.pdf (accessed 2026-10-23) | 555b9df82af12de4ca887efc21c0a9e159a14485d5d570f44b32ef15c6c62470 | (22 words) Organizations should minimize the use, collection, and retention of PII to what is strictly necessary to accomplish their business purpose and mission — ES-2, S051.txt:249-250; (17 words) If the PII serves no current business purpose, then the PII should no longer be used or collected — §4.2.1, S051.txt:1250-1251; (9 words) Develop a schedule for periodic review of PII holdings — S051.txt:260; (21 words) The effective management and prompt disposal of PII, in accordance with NARA-approved disposition schedules, will minimize the risk of unauthorized disclosure — §4.2.1, S051.txt:1283-1284; (4 words) Date Published: April 2010 — S051.landing.html:429; (5 words) 04/06/10: SP 800-122 (Final) — S051.landing.html:514 | admit, A (re-opened; ES-2 locator corrected) |
```

## Touched surfaces, gates, and limits

- Wrote only this report in the lane. Scratch artifacts: `/fast/scratch/hyaku/mori-r36/SupS051/S051.src` (SHA-256 above), `/fast/scratch/hyaku/mori-r36/SupS051/S051.txt` (layout extraction), and `/fast/scratch/hyaku/mori-r36/SupS051/S051.landing.html` (SHA-256 above).
- No product/source registry or lesson file edited; no lane Git/index writes, installs, tests, or builds. No other gate was run. The report's draft Gate row uses the reopened PDF bytes and quotes with extracted line locations; the landing-page history/date is separately cited.
- Verdict is about the requested tip anchor and teaches only. The only unsupported tip-anchor wording is `heading`; the corrected draft calls it ES-2 text. Scope and other row cells were carried forward, not independently re-audited.

VERDICT: unsupported
