# RevGateS226 — S226 SOURCES.md verification (wave 2)

Verdict: **PASS**. Row well-formed, `teaches` opens `supersedes S069`, landing commit `daa1d4d` postdates `62db24c` on `corpus/SOURCES.md` history and is an ancestor of the scored tip.

## Commands run (all in /home/vgpnk/Projects/shokunin/mori-shokunin, read-only)

- `git log --format='%h %ad %s' -S 'S226' -- corpus/SOURCES.md` → exactly one hit:
  `daa1d4d Fri Oct 23 17:55:19 2026 -0300 round-38 data: S226 + content-anchor/containment entries, timed supersede in the append-only gate, C1-C3 declaration and capability rows, README/QUALITY/SKILL, lesson, recipe fix`
- `git log -1 --format='%H %h %ad %s' 62db24c` → `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8 62db24c Thu Oct 22 23:55:24 2026 -0300 round-33: C1 FR6 entry, sources S180-S190, round-32 repair, QUALITY 97, wave-1 reports`
- `git merge-base --is-ancestor 62db24c daa1d4d` → exit 0 (62db24c precedes landing)
- `git merge-base --is-ancestor daa1d4d f725f3076972e6e70595b5ac8279be524a111ff8` → exit 0 (landing on scored-tip history); same for HEAD
- `git show f725f307…:corpus/SOURCES.md | grep -c 'S226'` → 2 (row at blob line 232 + round-38 bounded-search note); row present at scored tip
- Cell-count check via python3 on working-tree `corpus/SOURCES.md` (header line 5)

## 1. Row text (`corpus/SOURCES.md:232`, present in scored-tip blob)

> | S226 | Python `os.path.realpath` documentation — https://docs.python.org/3/library/os.path.html#os.path.realpath | docs | A | the canonical-path resolution realpath applies (symlinks eliminated) and its relation to lexical containment | `os.path.realpath` paragraph "Return the canonical path of the specified filename, eliminating any symbolic links encountered in the path (if they are supported by the operating system)":657-658; page fetched 2026-10-23 | supersedes S069 — containment is decided on the resolved canonical path, because realpath eliminates symlinks; the lexical rejection of absolute and \`..\` segments is a pre-filter, not the containment decision. | mined | 2026-10-23 | on-release | corpus/knowledge/containment-timed-supersede-r38.md |

Well-formedness: 11 cells, matching the 11-cell header/separator at lines 5–6 (`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`); no stray pipes in cells. `status=mined`, `opened=2026-10-23`, `recheck=on-release`, `used-by=corpus/knowledge/containment-timed-supersede-r38.md` (file exists). Supersede target S069 exists (`corpus/SOURCES.md:75`, Python pathlib docs, lexical-containment rule), so the supersession is a real row-to-row reference and semantically coherent (canonical-path rule supersedes lexical rule).

`teaches` opens exactly `supersedes S069` — programmatic `startswith('supersedes S069')` → True.

## 2. Landing commit and order vs `62db24c`

- Landing commit: `daa1d4d` (2026-10-23 17:55:19 -0300), the unique `-S 'S226'` touch of `corpus/SOURCES.md`.
- `62db24c` (2026-10-22 23:55:24 -0300) is an ancestor of `daa1d4d` (merge-base exit 0), so the row lands ~18h after the round-33 commit, on the file's history.
- `daa1d4d` is an ancestor of the scored tip `f725f3076` and of HEAD; the tip blob contains the S226 row at line 232.

## 3. Source-copy quote (`corpus/evidence/sources-r38/S226.src`)

The copy is the saved Python 3.15.1 `os.path` HTML page (`<title>os.path — Common pathname manipulations`, canonical URL matches the row's source). Lines 657–658:

- 657: `<dd><p>Return the canonical path of the specified filename, eliminating any symbolic`
- 658: `links encountered in the path (if they are supported by the operating`

Quoted sentence is verbatim present; the paragraph opens exactly at line 657 as anchored. The round-38 bounded-search note (`corpus/SOURCES.md:287`) independently cites `S226.src:657-658`.

## Findings by severity

- **PASS (verdict)** — all three acceptance criteria hold (well-formed row, teaches opens `supersedes S069`, landing postdates `62db24c`).
- **MINOR (precision note, not a FAIL)** — anchor cites `:657-658`, but the quoted sentence's final word `system).` completes on line 659 of `S226.src`; the cited range covers the paragraph start and all but the last word of the quote. Consistent with the file's coarse line-range anchor convention; no action taken (detection-only seat).

## Residual risk / verification gaps

- Anchor is against a local HTML copy; I did not refetch the live page to confirm the copy still matches upstream (out of scope for this seat; `page fetched 2026-10-23` is recorded in the row).
- No tools were installed or upgraded for this seat (built-in git/python3 sufficed); tooling directive: nothing to record.
