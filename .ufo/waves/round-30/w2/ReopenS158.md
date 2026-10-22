# ReopenS158 — contract A1 residual (F3), S158 only

**Verdict: agree.** The S158 admit row survives a fresh fetch: sha256 is stable across the excerpt header,
the lesson Gate admit line and the SOURCES anchor; all six excerpt lines are byte-identical to the fetched
file at the same numbers; the Gate quote is verbatim (whitespace-normalized) and its `(16 words)` label is
exact. Two bookkeeping/coverage notes below, neither a C1 defect under F3.

Lane tip read: `ad0f04745ced2194e58c22a0d6b38131bee3e230`. Only the report file and
`/fast/scratch/hyaku/mori-r30-w2/ReopenS158/` were written.

## 1. Fresh fetch (observed)

Access time recorded with `date -u` immediately before the request: **2026-10-22T22:02:38Z**.

```
curl -sS -o fetched.c -w 'HTTP=%{http_code} SIZE=%{size_download} URL=%{url_effective}\n' \
  https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-manager.c
HTTP=200 SIZE=101383 URL=https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-manager.c
sha256(fetched.c) = 428dc8308d5caf70faee074e87888264c3708aa8e24c6069854790b952a7ffa2
wc -l fetched.c    = 2633
```

## 2. sha256 comparison, three places

| where | recorded value | vs fetched |
|---|---|---|
| `corpus/evidence/sources-r30/S158.txt:3` (excerpt header) | `428dc830…a7ffa2` | identical |
| `corpus/lessons/round-30.md:126` (Gate admit line) | `428dc830…a7ffa2` | identical |
| `corpus/SOURCES.md:164` (anchor field) | `428dc830…a7ffa2`, `101383 B` | identical, byte size too |

The excerpt header (`S158.txt:4`) and the Gate line (`round-30.md:126`) both record access time
`2026-10-22T21:13:19Z`, i.e. an earlier fetch. Re-fetching at `22:02:38Z` returned the same full-byte hash,
so the committed hash is not stale and the URL still serves the same content at tag `v262`.

## 3. Every excerpt line vs the fetched line of the same number

Method (scratch script): split the excerpt body on `<n>\t`, compare the text bytes to fetched line `n`
with no normalization (tabs/indent preserved).

| excerpt line | fetched line | bytes of text | result |
|---|---|---|---|
| 1291 | 1291 | 27 | identical |
| 1292 | 1292 | 57 | identical |
| 1293 | 1293 | 93 | identical |
| 1294 | 1294 | 109 | identical |
| 1295 | 1295 | 80 | identical |
| 1296 | 1296 | 9 | identical |

**6/6 identical, 0 mismatches.** (Excerpt body is `corpus/evidence/sources-r30/S158.txt:7-12`; header is
`:1-5`.)

## 4. The Gate admit quote (`corpus/lessons/round-30.md:126`)

Located quote as written: `` `journald-manager.c:1291-1294` (16 words) `` followed by

```
if (rl > 1) manager_driver_message(m, c->pid, LOG_MESSAGE_ID(SD_MESSAGE_JOURNAL_DROPPED_STR), LOG_MESSAGE(\"Suppressed %i messages from %s\", rl - 1, c->unit),
```

- **Location:** lines 1291 (`if (rl > 1)`), 1292 (`manager_driver_message(m, c->pid,`), 1293
  (`LOG_MESSAGE_ID(SD_MESSAGE_JOURNAL_DROPPED_STR),`), 1294 (the `LOG_MESSAGE("Suppressed …)` line). The
  range is accurate and does not overrun into 1295.
- **Verbatimness:** whitespace-collapsed and with the two `\"` unescaped, the quote is **exactly** the join
  of fetched lines 1291-1294 (`exact match unescaped==joined: True`).
- **Word label:** `wc -w` on the quote = **16** (raw, with backslashes) and **16** (unescaped). The `(16
  words)` label is exact.
- **Byte-literal caveat:** raw bytes differ from the source only at the two embedded quotes, which the lesson
  escapes as `\"`. The same escaping style appears in the S156 row (`round-30.md:112`), so it is a house
  convention, not an S158 error. If the L1 wants byte-literal quotes in Gate lines, this row (and the S156
  row) would need the escapes removed; F3 does not require that, since F3 compares excerpt lines to fetched
  bytes.

## 5. Does the SOURCES `teaches` sentence hold? (`corpus/SOURCES.md:164`)

Element-by-element against the fetched bytes:

| teaches clause | fetched evidence | supported |
|---|---|---|
| "per-unit rate limit" | `:1280-1286` `rl = journal_ratelimit_test(&m->ratelimit_groups_by_id, c->unit, c->log_ratelimit_interval, c->log_ratelimit_burst, LOG_PRI(priority), available);` — keyed on `c->unit` | yes |
| "`rl > 1` guard" | `:1291` `if (rl > 1)` | yes |
| "the emitter call" | `:1292` `manager_driver_message(m, c->pid,` | yes |
| "`Suppressed %i messages from %s` wording with the count `rl - 1` and the unit name" | `:1294` `LOG_MESSAGE("Suppressed %i messages from %s", rl - 1, c->unit),` | yes |
| "SD_MESSAGE_JOURNAL_DROPPED_STR" | `:1293` | yes |
| "N_DROPPED tags" | `:1295` `LOG_ITEM("N_DROPPED=%i", rl - 1));` — in the excerpt, **not** in the 4-line Gate quote | yes (via excerpt line 1295) |
| "at the v262 release tag only" | URL is tag `v262`; GitHub API: `refs/tags/v262` = annotated tag `1f7dffaf714cc4488159c498b7a17cf34c5a96d5`, target type `commit`, target `8cc40e0c5e9234bf45084751ac53b1fbfe70b492` — exactly the anchor string at `SOURCES.md:164` | yes |
| "notice inside `manager_dispatch_message`" | `:1252` `void manager_dispatch_message(`; the notice block `:1290-1295` sits inside it | yes |
| exclusions: "not the rate-limit algorithm or its pools", "not the pre-split `src/journal/journald-server.c` copy", "not host configuration", "not the reader's own detection" | consistent with the reject rows re-verified in §6; `rl == 0` returns at `:1287-1288`, so only a nonzero result reaches the notice | yes |

Conclusion: **the `teaches` sentence is supported** by the quoted lines plus the excerpt. The N_DROPPED
clause is the only part that needs line 1295 (see note N2).

## 6. Supplementary — the S158 reject rows re-fetched (`round-30.md:127-134`)

These are the same S158 block; all reproduce exactly.

| lesson line | URL (tag) | claimed sha256 | fetched sha256 | quota |
|---|---|---|---|---|
| :127 | v262 `journald-server.c` | `d5558cd4…3512ed` | `d5558cd4…3512ed`, HTTP 404, body `404: Not Found` (14 B) | matches |
| :128 | v262 `journald-rate-limit.c` | `dfe42099…b5d6780a` | identical; `grep -c Suppressed` = 0 | matches |
| :129 | v262 `journald-native.c` | `226a4c01…d9bd3521` | identical; `grep -c Suppressed` = 0 | matches |
| :130 | v262 `man/journald.conf.xml` | `ed71e38d…908f87f2` | identical; `grep -ci suppress` = 0 | matches |
| :131 | v257 `journald-server.c` | `0c1bb73b…6aca21cd3` | identical; `:1304` = `LOG_MESSAGE("Suppressed %i messages from %s", rl - 1, c->unit),` | matches |
| :132 | v252 / v249 `journald-server.c` | `d9519978…57388aad` (101129 B) / `3478a46c…46ec8466ac` (95661 B) | both identical incl. sizes; `:1143` / `:1107` match the quoted `%i` line | matches |
| :133 | v233 `journald-server.c` | `1434afcf…54a066bde` | identical; `:1181` = `LOG_MESSAGE("Suppressed %u messages from %s", rl - 1, path),` — `%u` and `path` as the row says | matches |
| :134 | v262 `journald-socket.c` | none claimed (grep only) | — ; the URL does occur on `SOURCES.md:160` (3 occurrences on that line), so "duplicate URL already carried by S154" holds | matches |

One observation on :128: the row names the exact-case grep `grep -c Suppressed` = 0, which holds; a
case-insensitive `grep -ci suppress` on that file prints 6. The row is not wrong, but a reader must use the
case-sensitive pattern it names.

## 7. Notes / remaining unknowns

- **N1 (bookkeeping, not fact):** the SOURCES anchor says `src/journal/journald-manager.c:1290-1296`
  (`SOURCES.md:164`) while the excerpt header says `lines: 1291-1296` (`S158.txt:5`). Line 1290 is the
  comment `/* Write a suppression message if we suppressed something */`; the anchor is a superset and not
  false, but the committed excerpt does not attest 1290. Optional fix: align anchor or header.
- **N2 (coverage):** the Gate admit quote covers 1291-1294, so it alone does not evidence the teaches'
  N_DROPPED clause; excerpt line 1295 does. Not a defect under F3 (all excerpt lines match the fetched
  bytes), but if the Gate line is meant to be the row's single located quote it under-covers one clause.
- **Scope:** only the S158 URLs were re-fetched (this ticket). The S156/S157/S159/S160 URLs belong to
  sibling seats. No URL needed a bot challenge; every request returned a body.
- **Tooling:** nothing installed or updated; no pacman transaction run. `curl`, `sha256sum`, `python3`, `sed`
  were already present.
- **Privacy/retention:** this report and the scratch dir contain only public URLs, sha256 sums, upstream
  systemd source lines and line numbers — no host configuration values, unit names, session identifiers or
  host journal MESSAGE text. The lane retention scan should not rise.
- **Confidence:** high on every observed item above; no item is inference-only. The only judgment calls are
  the two notes, which are explicitly flagged.

Report: .ufo/waves/round-30/w2/ReopenS158.md
