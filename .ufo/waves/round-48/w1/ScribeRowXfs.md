# ScribeRowXfs — draft SOURCES row S479 (xfs_quota.8)

Seat: ScribeRowXfs (leaf; no subagents). Claim: C2 (depth) — filesystem-quota
observability entry. Scope: draft the lane SOURCES.md row for
https://man7.org/linux/man-pages/man8/xfs_quota.8.html as id S479, 11-column schema
of CORPUS.md §SOURCES.md. No production file was edited; the candidate row is a draft
below. Scratch only under `.scratch/r48-ScribeRowXfs/`. No tools installed (used
existing `curl` and `python3`; no pacman; host reads read-only).

## Evidence log (command + output + exit)

1. Committed copy hash — `sha256sum corpus/evidence/sources-r48/xfs_quota.8.html`
   ```
   6375e40e9c0e950d78b38edbe9b7e7fdf5868d55be07040d4a029c552c437d5f  corpus/evidence/sources-r48/xfs_quota.8.html
   ```
   exit 0. Matches the frozen `COPIES` entry in `.ufo/waves/round-48/count-c2.py`
   (lines 37-39: `6375e40e9c0e950d78b38edbe9b7e7fdf5868d55be07040d4a029c552c437d5f`).

2. Live fetch (browser User-Agent), access date 2026-10-25 —
   ```
   $ TMPDIR=<scratch> curl -s -A 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36' \
       -o .scratch/r48-ScribeRowXfs/xfs_quota-live.html \
       -w 'http=%{http_code} size=%{size_download} url=%{url_effective}\n' \
       'https://man7.org/linux/man-pages/man8/xfs_quota.8.html'
   http=200 size=33702 url=https://man7.org/linux/man-pages/man8/xfs_quota.8.html
   ```
   exit 0. `sha256sum` of the live fetch = `6375e40e…` — byte-identical to the
   committed copy (page unchanged today).

3. Quote check in the committed copy (Python; mimic `count-c2.py` `normalise`:
   strip tags, `html.unescape`, collapse whitespace):
   - quote `If a user's usage reaches the hard limit, further requests for space
     (or attempts to create a file) fail with the "Quota exceeded" (EDQUOT)
     error.` → occurs exactly once in the normalised text, 25 words (≤25). Raw
     file line 165, QUOTA OVERVIEW section.
   - supporting tool-identity lines also occur: `xfs_quota - manage use of quota
     on XFS filesystems` (NAME, 9 words); `xfs_quota is a utility for reporting
     and editing various aspects of filesystem quota.` (DESCRIPTION, 13 words).

4. Man-page footer / revision text (command copy, COLOPHON + footer):
   - `This page was obtained from the project's upstream Git repository … on
     2026-08-04. (At that time, the date of the most recent commit that was found
     in the repository was 2026-07-17.)` (COLOPHON; raw lines 527-529).
   - `HTML rendering created 2026-09-09 by Michael Kerrisk` (footer; raw line 558).
   - headline: `xfs_quota(8)  System Manager's Manual  xfs_quota(8)` (raw line 144).
   The page is an xfsprogs project page; its revision text is the COLOPHON above
   (no "Linux man-pages 6.x" line on this page).

5. Registry facts: highest existing id is S478 (`grep -n '^| S' corpus/SOURCES.md`
   tail; `awk` id list ends S471…S478) → S479 is the next unused id. New rows
   open 2026-10-25 (C2 `OPENED` constant, count-c2.py line 31). Lane S477/S478
   are taken; staged assimilation ids S477-S482 collide and are renumbered by the
   document — not by this row.

## Draft row (one line; never written to corpus/SOURCES.md by this seat)

```markdown
| S479 | xfs_quota(8) — https://man7.org/linux/man-pages/man8/xfs_quota.8.html | docs | A | user-space XFS quota reporting and the EDQUOT error surface on hard-limit exhaustion; not kernel quota-flag emission (S078, S084, S088, S089) and not any measurement on this host | QUOTA OVERVIEW paragraph at raw line 165: "If a user's usage reaches the hard limit, further requests for space (or attempts to create a file) fail with the "Quota exceeded" (EDQUOT) error."; NAME and DESCRIPTION paragraphs (raw lines 147, 154); page obtained from upstream xfsprogs Git 2026-08-04 (latest commit then 2026-07-17), HTML rendering created 2026-09-09 | Hard-limit exhaustion fails further space or file-creation requests with EDQUOT to the calling process — the user-space-visible error surface the lane's kernel-flag rows do not cover. | mined | 2026-10-25 | 180d | corpus/knowledge/quota-observability-r48.md |
```

## Gate

- URL: https://man7.org/linux/man-pages/man8/xfs_quota.8.html
- accessed: 2026-10-25 (live fetch, browser User-Agent, HTTP 200; byte-identical to the
  committed copy, sha256 6375e40e9c0e950d78b38edbe9b7e7fdf5868d55be07040d4a029c552c437d5f)
- quote (25 words): `If a user's usage reaches the hard limit, further requests for space (or attempts to create a file) fail with the "Quota exceeded" (EDQUOT) error.`
- location: `corpus/evidence/sources-r48/xfs_quota.8.html:165` (QUOTA OVERVIEW section)

## Limits / unverified

- I did not run `count-c2.py` (entry authoring is a sibling seat; the counter is the
  L1's acceptance run). The quote was verified against the committed copy with the
  counter's own `normalise` semantics.
- The live page could change after 2026-10-25; the copy is dated by its freeze sha256.
- This seat drafted only the SOURCES row; the entry table's quote set (unique, 6-25
  words, ≥8 rows, ≥3 sources) is out of this seat's scope.
