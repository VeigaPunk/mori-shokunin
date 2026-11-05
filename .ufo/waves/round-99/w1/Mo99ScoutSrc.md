# Mo99ScoutSrc — r99 w1 source re-verification (S633–S636, S014)

Seat: scout. Axes judged: operability, calibration. Date: 2026-11-05.
Method: live refetch of all five URLs with curl (UTC-stamped), sha256 + byte-diff against the pinned copies in
`corpus/evidence/sources-r99/`; quote location and word counts computed against the pinned bytes (HTML rows located
after tag stripping + entity unescape + whitespace normalization, exactly as the rows prescribe). No file in the
lane was edited; scratch removed after the run.

## A. Live re-fetch vs pinned copies (all 2026-11-05T22:17:44Z)

| id | URL | HTTP | bytes | sha256 (live) | live == pinned |
|---|---|---|---|---|---|
| S633 | https://man7.org/linux/man-pages/man8/sysctl.8.html | 200 | 14152 | `a63af3f671366489bb8f1ba2334507a52b83753671d693b689c3cabeaefb95f3` | YES (`diff -q` empty) |
| S634 | https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html | 200 | 357953 | `0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd` | YES |
| S635 | https://raw.githubusercontent.com/sudo-project/sudo/v1.9.17p2/lib/eventlog/eventlog.c | 200 | 42109 | `5bdea0aeaa95bae4b06feb887f25e344b5ef244fa40f5124c34ee51e545bc84b` | YES |
| S636 | https://raw.githubusercontent.com/sudo-project/sudo/v1.9.17p2/lib/util/lbuf.c | 200 | 12373 | `eda9e0a3d5085ff37f6738ef7a11ece8d96e432337294565ccb47412837f0212` | YES |
| S014 | https://www.freedesktop.org/software/systemd/man/latest/journalctl.html | 200 | 87375 | `75440570fb1f71859229ca88fed0a6764b2057c7dd90651701b3d022a5649722` | YES |

All four sha256 values recorded in SOURCES.md rows S633–S636 match my live digests exactly. The S014 row predates
the re-open and records no digest; the r99 pinned copy `S014-journalctl-r99.html` is byte-identical to today's live
page, so the re-open receipt is accurate.

Exact receipts (one call per source; `date` printed first, then curl status, `wc -c`, `sha256sum`, `diff -q`):

```
2026-11-05T22:17:44Z / HTTP 200 / 14152 / a63af3f6…95f3 / S633-LIVE-EQUALS-PINNED
2026-11-05T22:17:44Z / HTTP 200 / 357953 / 0889867a…1acd / S634-LIVE-EQUALS-PINNED
2026-11-05T22:17:44Z / HTTP 200 / 42109 / 5bdea0ae…84b / S635-LIVE-EQUALS-PINNED
2026-11-05T22:17:44Z / HTTP 200 / 12373 / eda9e0a3…f212 / S636-LIVE-EQUALS-PINNED
2026-11-05T22:17:44Z / HTTP 200 / 87375 / 75440570…9722 / S014-LIVE-EQUALS-PINNED
```

## B. SOURCES.md rows S633–S636 — quote located, word count, verdict

| row | quote (as recorded) | located in pinned copy | words | verdict |
|---|---|---|---|---|
| S633 | "Only apply settings that match pattern." | tag-stripped raw lines 132–136 (row claims 134–136; contained) | 6 | supported |
| S634 | "it and all subsequent characters up to, but excluding, the next <newline> shall be discarded as a comment." | tag-stripped raw lines 297–304, completes in 303–304 (row claims 303–304) | 18 whitespace-split — row says 17 (likely not counting the `<newline>` placeholder); both ≤ 25 | supported |
| S635 | "Wrap args containing spaces in single quotes." | eventlog.c line 202 | 7 | supported |
| S636 | "Any non-printable characters are escaped in octal as #0nn." | lbuf.c line 145 | 9 | supported |

Row-level claims say no more than their sources: S633's "-r/--pattern takes a regex that filters settings" is
backed by the very next sentence on the page, "The pattern uses extended regular expression syntax." (stripped
132–136); S634's "so it is not a write" is the row's application of 2.3 token recognition, which the same chapter
carries; S635/S636 verdict columns restate the code cited below. One annotation nit (S634 word count 17 vs 18) is
cosmetic and does not breach the ≤ 25 rule.

## C. Knowledge claims — `corpus/knowledge/sudo-log-grammar-r99.md` (10 rows)

| # | claim | quote located | words | verdict |
|---|---|---|---|---|
| 1 | path then args; space-args single-quoted | eventlog.c:202 `/* Wrap args containing spaces in single quotes. */` | 9 | supported |
| 2 | unquoted args escaped same way; `'`/`\` backslash-escaped in every argument | eventlog.c:208 + lbuf.c:163 | 8, 10 | supported |
| 3 | control chars incl. newline logged as `#0nn` | lbuf.c:145 | 9 | supported |
| 4 | long line split at a space; rest is a continuation | eventlog.c:1042 `fmt = _("%8s : (command continued) %s");` | 7 | supported |
| 5 | exit event appends ` ; EXIT=` / ` ; SIGNAL=`; not arguments | eventlog.c:223 (SIGNAL= at 217) | 5 | supported |
| 6 | single quotes literal | XCU 2.2.2, raw line 104 (verbatim) | 16 | supported |
| 7 | token-initial `#` starts a comment to newline | XCU 2.3 rule 9, raw 303–304 (verbatim) | 25 (exactly at limit) | supported |
| 8 | -p/--load loads from file or /etc/sysctl.conf | sysctl.8, stripped 112–116 | 13 | supported |
| 9 | -r/--pattern takes a regex filter, never a key=v write | sysctl.8, stripped 132–136 + "extended regular expression syntax" | 6 | supported |
| 10 | `-o short` default = classic syslog; short-iso = RFC 3339 | journalctl page, stripped 194–195; short-iso cell: "shows timestamps in the RFC 3339 profile of ISO 8601" | 18 | supported |

Overreach notes (each claim checked against what its source actually says):

- 2: both argv branches pass `LBUF_ESC_QUOTE` (eventlog.c 204, 210), and lbuf.c's `should_quote` (162–163)
  backslash-escapes `'` and `\` under that flag — so "escaped everywhere [in arguments]" holds. Nuance, not a
  defect: the `COMMAND=` path itself (line 196) uses only `CNTRL|BLANK`, so quote-escaping applies to *arguments*,
  exactly as the claim scopes it. The quoted branch omits `LBUF_ESC_BLANK`, immaterial for an argument that
  contains a space.
- 3: escape() (116–141) emits `#` + `0` + 1/2/3 octal digits (`#0n`, `#0nn`, `#0nnn`); newline (012) → `#012`,
  the `#0nn` shape. The knowledge "Limits" section already states the full `#0n/#0nn/#0nnn` forms.
- 4: split code (1016–1045) cuts with `memrchr(p, ' ', maxlen)` and hard-cuts at maxlen only when no space exists;
  the no-space edge is disclosed in the entry's Limits section, so the claim overreaches nothing undisclosed.
- 5: ` ; SIGNAL=` / ` ; EXIT=` are appended by sudo after the argv loop (215–226) — "not arguments" is the code's
  own structure.
- 10: the claim's "RFC 3339" matches the page word-for-word ("the RFC 3339 profile of ISO 8601"); "must accept
  both or fail closed" is the tool's stated rule, not attributed to the source.
- No claim row is overreaching; none was not-located.

## D. Host sudo version and upstream drift

- Host: `/usr/bin/sudo` is owned by package `sudo 1.9.17.p2-6` and the binary contains the literal version string
  `1.9.17p2`. That equals the pinned tag v1.9.17p2. `sudo --version` was **not run** — the seat rules forbid
  running sudo on this host (only Mo99ExecSudo may); the read-only equivalents above are the evidence.
- sudo `main` (fetched 2026-11-05, HTTP 200: eventlog.c 43770 bytes sha256 `b80c26ec1357be32d3c10a6584949bf156f11062427d98f082016cbcf8934774`;
  lbuf.c 12205 bytes sha256 `4e0f9d3da429cfe5e072f52a3295688819d8360b10e4b09cd5609514e3f812af`):
  - lbuf.c: the ONLY hunk removes the PVS-Studio comment block (pinned lines 19–23) and shifts includes; escape(),
    `should_escape`, `should_quote` and `sudo_lbuf_append_esc_v1` are byte-identical. No drift in should_quote/escape.
  - eventlog.c: the COMMAND= block is byte-identical (pinned 199–231 == main 216–248; `Wrap args` comment, both
    esc-flag sets, ` ; SIGNAL=`, ` ; EXIT=` all unchanged). The syslog split keeps `memrchr(p, ' ', maxlen)` and
    the `(command continued)` fmt verbatim; main's changes there are clerical/defensive (local `submituser`, an
    `overhead` variable, and `maxlen = syslog_maxlen > overhead ? syslog_maxlen - overhead : 1`). The grammar the
    round-99 tool inverts is unchanged on main.

## E. Verdicts

- S633: supported. S634: supported. S635: supported. S636: supported. S014: supported (re-open receipt accurate).
- Knowledge sudo-log-grammar-r99.md: all 10 claim rows supported; 0 overreach; 0 not-located.
- Host sudo == pinned tag v1.9.17p2; upstream `main` shows no drift in any grammar-bearing block.

Report: .ufo/waves/round-99/w1/Mo99ScoutSrc.md
