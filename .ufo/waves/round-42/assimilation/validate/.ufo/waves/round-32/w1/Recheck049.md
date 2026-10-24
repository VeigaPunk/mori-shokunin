# Recheck S049 — OWASP Logging Cheat Sheet (C1 freshness, wave 1)

Seat: MoriR32A2.Recheck049. Population row S049 from `.ufo/waves/round-32/c1-population.json`
(teaches: map each log data class to one treatment; hash session identifiers when correlation is
needed; replace the malformed field rather than drop the whole event; paths and internal names get
documented handling, not blanket exclusion).

## 1. Fetch

- url: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- command: `curl -sSL --fail -m 60 <url> -o /fast/scratch/hyaku/mori-r32/Recheck049/S049.src`
- HTTP 200, **no redirect** (`url_effective` printed back equals the population url), 2026-10-23T01:31:23Z
- accessed: `2026-10-23T01:31:23Z` (>= contract minimum 2026-10-23T01:00:00Z)
- bytes: 108735
- sha256: `604378c015d263638d7fd3c066762e7da7ed104be7fa974223f085b5bf330bb9`
- scratch copy: `/fast/scratch/hyaku/mori-r32/Recheck049/S049.src` (bytes unchanged; lane copy to be
  committed by the integrator as `corpus/evidence/recheck-r32/S049.src`)
- normalised text used for quoting: `python3 .ufo/waves/round-32/seat-check.py text S049.src`
  (32992 bytes, written to `/fast/scratch/hyaku/mori-r32/Recheck049/S049.text`)
- build metadata unchanged from the anchor: `<meta name="generator" content="mkdocs-1.6.1,
  mkdocs-material-9.7.7">`; grep for `20[0-9]{2}-[0-9]{2}-[0-9]{2}` over the raw page returns nothing,
  and grep for `revision|last updated|changelog` returns nothing — still no revision date, as the
  anchor says.

## 2. Ready-to-paste row

```markdown
| S049 | https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html | 2026-10-23T01:31:23Z | 604378c015d263638d7fd3c066762e7da7ed104be7fa974223f085b5bf330bb9 | "should usually not be recorded directly in the logs, but instead should be removed, masked, sanitized, hashed, or encrypted"; "Session identification values (consider replacing with a hashed value if needed to track session specific events)"; "If a field is malformed, omit or safely replace that field and record the validation failure with bounded, safe context" | current |
```

## 3. Quote → teaches-cell fact (verdict: current)

- Q1 `should usually not be recorded directly in the logs, but instead should be removed, masked,
  sanitized, hashed, or encrypted` (19 words). Bears on teaches clause 1, "map each log data class to
  one treatment", and on the scope cell's list `exclude, remove, mask, sanitize, hash, encrypt`; it is
  also the exact sentence the knowledge entry relies on (`corpus/knowledge/evidence-minimization-r18.md:15-16`).
  Live page still carries the menu verbatim at the head of the "Data to exclude" section ⇒ current.
- Q2 `Session identification values (consider replacing with a hashed value if needed to track session
  specific events)` (16 words). Bears on teaches clause 2, "hash session identifiers when correlation is
  needed" — the bullet says replace with a hashed value *when needed to track session specific events*,
  i.e. for correlation ⇒ current.
- Q3 `If a field is malformed, omit or safely replace that field and record the validation failure with
  bounded, safe context` (20 words). Bears on teaches clause 3, "replace the malformed field rather than
  drop the whole event"; the live bullet continues `; do not discard the entire security event` (not
  included, quote stops at 20 words on a clause boundary) ⇒ current.

Section integrity check (raw HTML, `python3` slice from `id="data-to-exclude"` to
`<h3 id="customizable-logging">`, 2348 bytes): the 12 exclusion bullets are all present
(application source code, session identification values, access tokens, PII, passwords, DB connection
strings, encryption keys, bank/card data, higher-classification data, commercially-sensitive info,
illegally collected info, opted-out/expired-consent info), followed by the 4-bullet "sometimes" list
(file paths, DB connection strings, internal network names and addresses, non-sensitive personal data).
Nothing in the section has been softened or reversed.

Teaches clause 4 ("paths and internal names get documented handling, not blanket exclusion") is still
supported live but is **not carried by a quote** (3-quote cap; Q1–Q3 cover clauses 1–3). The supporting
live text is `Sometimes the following data can also exist, and while useful for subsequent investigation,
it may also need to be treated in some special manner before the event is recorded:` followed by
`File paths` / `Internal network names and addresses` (normalised offset ~20371). "Documented" is supported
adjacent to it by Note B (`consistent, and documented, approach to classification of events`). If the
judge wants clause 4 evidenced in the table, the cheapest swap is Q2 → `and while useful for subsequent
investigation, it may also need to be treated in some special manner before the event is recorded: File
paths` (24 words, verified present and passing the in-copy test); Q1 must stay because the knowledge entry
quotes it verbatim.

## 4. seat-check output

Command:
`timeout 300 python3 .ufo/waves/round-32/seat-check.py row S049 S049.src '<quotes cell from §2>'`

```
sha256=604378c015d263638d7fd3c066762e7da7ed104be7fa974223f085b5bf330bb9
quotes=3 words=[19, 16, 20] in_copy=[True, True, True]
shared_tokens=['directly', 'encrypted', 'field', 'hashed', 'instead', 'logs', 'malformed', 'masked', 'needed', 'recorded', 'removed', 'replace', 'sanitized', 'session', 'should', 'usually']
topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
```

(exit 0; `live_quotes_ok=True` means the three quotes are also in a fresh live fetch, which is counter R3.)

## 5. Drift

None. Verdict `current`; no `Round32` correction is drafted and
`corpus/knowledge/evidence-minimization-r18.md` needs no change (R5 not applicable).

## Notes

- Tools installed/updated: none (curl, python3, sha256sum already present). No pacman run (host
  transactions paused); no subagents, no background jobs; no git/jj writes.
- Scratch dir `/fast/scratch/hyaku/mori-r32/Recheck049/` holds `S049.src`, `S049.text`, this draft only.
- Only lane file written by this seat: `.ufo/waves/round-32/w1/Recheck049.md`.
