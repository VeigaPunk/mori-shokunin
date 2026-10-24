# Recheck051 — S051 (C1, round 32 attempt 2)

Seat: `MoriR32A2.Recheck051`. Scope: one population id, S051. Verdict: **current**.
No tools installed or updated this seat (nothing needed; `curl`, `python3`, `pdftotext` already present).

## 1. Fetch

| field | value |
|---|---|
| id | S051 |
| population url | `https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-122.pdf` |
| accessed (UTC, at fetch) | `2026-10-23T01:31:26Z` |
| HTTP | `200`, `final=https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-122.pdf` (no redirect, no bot challenge) |
| tries | 1 of 3 (curl exit=0) |
| byte size | 818516 |
| sha256 | `555b9df82af12de4ca887efc21c0a9e159a14485d5d570f44b32ef15c6c62470` |
| scratch copy (bytes unchanged) | `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck051/S051.src` |
| normalised text (`seat-check.py text`) | `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck051/S051.txt` (174006 bytes, 1 logical line) |

Command used:
`curl -sSL --fail -m 60 https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-122.pdf -o S051.src -w 'HTTP=%{http_code} REDIRECTS=%{num_redirects} URL_EFF=%{url_effective}\n'`
→ `HTTP=200 REDIRECTS=0 URL_EFF=https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-122.pdf`, `EXIT=0`;
`sha256sum S051.src` → the digest above. The body is a `%PDF` stream (818516 bytes), so the counter/seat-check normalise it with `pdftotext -layout` (`count-c1.py:90-96`) — the quotes below were copied from that output, not from a browser view.

Independent check of the population **anchor** claims, from the fetched bytes and the anchor's own landing page (opened live this seat, `https://csrc.nist.gov/pubs/sp/800/122/final`, HTTP 200, no redirect, sha256 `10f4cadb560c559c7481d161e90c7173bee168adf58f143b0fdbfe04ffb40a1f`, scratch `S051.landing.src`): title/date `Special Publication 800-122 … April 2010` (§1.1 front matter); §4.2.1 heading `Minimizing the Use, Collection, and Retention of PII` at normalised offsets 77467 (body) and its TOC entry `4.2.1 … 4-3`; §4.2.2 at 80328; landing page `Document History: 04/06/10: SP 800-122 (Final)`. No newer edition or supersession notice appears on the landing page.

## 2. Ready-to-paste row

```markdown
| S051 | https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-122.pdf | 2026-10-23T01:31:26Z | 555b9df82af12de4ca887efc21c0a9e159a14485d5d570f44b32ef15c6c62470 | "If the PII serves no current business purpose, then the PII should no longer be used or collected."; "Develop a schedule for periodic review of PII holdings"; "Disposal of PII should be conducted in accordance with the retention schedules approved by the National Archives and Records Administration" | current |
```

## 3. Quote → teaches-cell mapping

Teaches cell: *"Retention needs a current-business-purpose test per item: PII with no current purpose 'should no longer be used or collected'; holdings need periodic review and disposal under schedules. A class-hit gate does not by itself establish necessity."*

1. `If the PII serves no current business purpose, then the PII should no longer be used or collected.` (18 words, §4.2.1 body at offset 78203, i.e. between the §4.2.1 heading at 77467 and §4.2.2 at 80328)
   Bears on clause 1: the test is **per holding, keyed to a *current* business purpose** — PII that fails it "should no longer be used or collected". This is the exact wording the teaches cell quotes. Verdict current follows: this sentence is present verbatim in the live PDF.
2. `Develop a schedule for periodic review of PII holdings` (9 words, offset 14833, same bulleted recommendation list that begins `Reduce PII holdings to the minimum necessary for proper performance of agency functions`)
   Bears on clause 2 ("holdings need periodic review"): review of holdings is scheduled, not one-off. Present verbatim.
3. `Disposal of PII should be conducted in accordance with the retention schedules approved by the National Archives and Records Administration` (20 words, offset 16594, footnote-7 sentence)
   Bears on clause 2 ("disposal under schedules"): disposal is bound to **NARA-approved retention schedules**. Present verbatim.

Row-level content words shared with teaches/anchor/scope (seat-check, §4 below): `business, collected, current, disposal, holdings, longer, periodic, purpose, retention, review, schedules, should` — 12 ≥ 2, topic_ok=true.

Clause 3 of the teaches cell ("A class-hit gate does not by itself establish necessity") is the knowledge entry's own inference from clause 1, not a sentence of SP 800-122; nothing in the live PDF contradicts it, and the teaches cell here is supported by the purpose test it cites. No drift.

## 4. seat-check output

```
$ python3 .ufo/waves/round-32/seat-check.py row S051 S051.src '<quotes cell>'
EXIT 0
sha256=555b9df82af12de4ca887efc21c0a9e159a14485d5d570f44b32ef15c6c62470
quotes=3 words=[18, 9, 20] in_copy=[True, True, True]
shared_tokens=['business', 'collected', 'current', 'disposal', 'holdings', 'longer', 'periodic', 'purpose', 'retention', 'review', 'schedules', 'should'] topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
```

(`live_quotes_ok=True` is the helper's own live re-fetch of the population url — the quotes are also in today's remote bytes, not only in my saved copy. Verbatim transcript saved at `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck051/S051.row.out`.)

## 5. Drift

**None.** The live document is still the April 2010 final (`April 2010` in the front matter, `04/06/10: SP 800-122 (Final)` in the landing page history), the §4.2.1 text still carries the current-purpose/minimisation/periodic-review/disposal guidance, and the population url resolves directly with no redirect. No `Round32` correction is needed in `corpus/knowledge/evidence-minimization-r18.md` (its S051 citation at line 1 reads `NIST SP 800-122 §4.2.1`, which the fetched bytes still carry).

Process note: every command was wrapped in `timeout`; no subagents, no background jobs, no git/jj writes, no pacman; only files under `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck051/` and this report were written.
