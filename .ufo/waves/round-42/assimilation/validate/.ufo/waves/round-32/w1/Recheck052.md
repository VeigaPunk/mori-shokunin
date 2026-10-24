# Recheck052 — S052 (C1 freshness, round 32 attempt 2)

Seat: MoriR32A2.Recheck052. Verdict: **current**.
Scratch: `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck052/`

## 1. Fetch

- id: S052
- url: https://opentelemetry.io/docs/security/handling-sensitive-data/
- command: `curl -sSL --fail -m 60 <url> -o /fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck052/S052.src`
  → `HTTP=200 URL_EFF=https://opentelemetry.io/docs/security/handling-sensitive-data/ SIZE=414607`, `EXIT=0`
- redirect: none — `%{url_effective}` equals the population url exactly; one fetch, first try, no retry needed
- accessed (recorded at fetch): `2026-10-23T01:31:25Z`
- byte size: 414607
- sha256: `6104b09c73e65514ed10d7eea302bcdaed88fa12982cd77e5b3049d0df949f80`
- copy (bytes unchanged): `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck052/S052.src`
  → **L1 must commit this file as `corpus/evidence/recheck-r32/S052.src`** (R2 compares its sha256 to the row)
- normalised text: `S052.txt` (15973 bytes, `seat-check.py text S052.src`, EXIT=0)
- page identity: `<title>Handling sensitive data | OpenTelemetry</title>`; metadata
  `article:modified_time" content="2026-01-14T14:37:39-05:00"` (`S052.src:1`) — identical to the population
  anchor's `2026-01-14T14:37:39-05:00`, so the page has not been edited since the row was opened 2026-10-21
- headings the anchor names are all still present in the live text: `Data minimization`,
  `Protecting sensitive data`, `Deleting and hashing user information`, `Replacing user.id with user.hash`,
  `Risk and limitations of hashing for anonymization`, `Truncating IP addresses`,
  `Delete attributes with redaction processor` (`S052.txt`)

## 2. Ready-to-paste row

```markdown
| S052 | https://opentelemetry.io/docs/security/handling-sensitive-data/ | 2026-10-23T01:31:25Z | 6104b09c73e65514ed10d7eea302bcdaed88fa12982cd77e5b3049d0df949f80 | "Only collect data that serves an observability purpose."; "Hashing the ID or name of a user may not provide the level of anonymization you need"; "hashes are reversible in practice if the input space is small and predictable" | current |
```

## 3. Quote → teaches-cell bearing

teaches: "Collect the attribute only when an observability purpose needs it; hashing a small or
predictable identifier is reversible in practice, so prefer drop or truncation and do not claim
anonymization."
scope: "telemetry data minimization, attribute deletion, hashing and truncation guidance for OTel
pipelines, scope limited to OTel-project recommendations rather than legal compliance".

1. `"Only collect data that serves an observability purpose."` — the *data minimization* predicate:
   collection is gated on an observability purpose. This is exactly the first clause of the teaches
   cell ("Collect the attribute only when an observability purpose needs it"). Verbatim, single
   occurrence at `S052.txt` offset 12760 (inside "Data minimization … This means: …"), 8 words,
   whole-word start ("Only") and end ("purpose."), no negation dropped.
2. `"Hashing the ID or name of a user may not provide the level of anonymization you need"` — the
   *Risk and limitations of hashing for anonymization* callout opening: hashing does **not** buy
   anonymization. This is the teaches clause "do not claim anonymization". Verbatim at offset 14519,
   17 words. It is a clause cut of one sentence; the next clause is quote 3, so the two together are
   contiguous text, not a splice.
3. `"hashes are reversible in practice if the input space is small and predictable"` — the reason the
   callout gives, and the exact mechanism the teaches cell states ("hashing a small or predictable
   identifier is reversible in practice"). Verbatim at offset 14611, 13 words, whole-word start/end;
   the page continues "(e.g. numeric user IDs)." which is deliberately left out and not needed.

Together these are the page's own minimization rule plus its complete hashing/anonymization warning,
so the verdict follows: the live page still supports the teaches cell → `current`.

Corroboration for the "prefer drop or truncation" half of the teaches cell (not quoted in the cell,
because the cell allows 1–3 quotes): the same page still says "As an alternative to hashing you can
truncate data, or group it by a common prefix or suffix." (`S052.txt` offset 14738), still shows
`action : delete` for `user.full_name` and `delete_key(attributes, "user.id")` in the two pipeline
examples (offset ~14400), and still states "the best way to prevent the collection of sensitive data
is not to collect data that might be sensitive." (offset 13094). Page furniture (nav sidebar, "Ask AI"
labels, "Feedback") was deliberately not quoted. None of the three quotes contains `&`, a pipe, a
zero-width character or PDF hyphenation; all were copied from `seat-check.py text` output, never from
the rendered page.

`used_by` check: `corpus/knowledge/evidence-minimization-r18.md:18` already quotes
`"hashes are reversible in practice if the input space is small and predictable"` verbatim and
attributes it to S052 (line 1 lists S052 as a source). That sentence is still on the live page, so the
knowledge entry needs no correction.

## 4. seat-check output

```
$ timeout 300 python3 .ufo/waves/round-32/seat-check.py row S052 S052.src '"Only collect data that serves an observability purpose."; "Hashing the ID or name of a user may not provide the level of anonymization you need"; "hashes are reversible in practice if the input space is small and predictable"'
sha256=6104b09c73e65514ed10d7eea302bcdaed88fa12982cd77e5b3049d0df949f80
quotes=3 words=[8, 17, 13] in_copy=[True, True, True]
shared_tokens=['anonymization', 'collect', 'data', 'hashing', 'observability', 'practice', 'predictable', 'purpose', 'reversible', 'small', 'user'] topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
EXIT=0
```

Saved at `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck052/seatcheck-s052-final.txt`.
`live_quotes_ok=True` means the helper's own fresh `curl` of the population url also contains all
three quotes, so R3 is satisfied independently of my copy.

## 5. Drift details

None. With a `current` verdict no `Round32` correction is drafted. The page's `article:modified_time`
is unchanged from the anchor (`2026-01-14T14:37:39-05:00`), and every heading the anchor cites is
still present, so there is no evidence of drift on this row.

## Tooling

No installs or updates were made for this seat.
