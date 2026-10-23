# Round-31 w1 — real round-30 writer briefs: hand-derived expected hit set for `tools/mori-blind-check.sh`

Seat: MoriR31.RealBriefsR30. Question: with the allow list given below, what must a correct
`tools/mori-blind-check.sh` report on the four real round-30 writer briefs? Derived by hand from
`.ufo/waves/round-31/rule-text.md:10-22` only. The checker was not run and no parser simulation was written;
nothing was installed or updated.

## 0. Provenance and inputs

- Lane revision read: `5c99f2d4213b41966d670d10006a2ff5135273e4`; wave dir `.ufo/waves/round-30/w1`.
- Blobs (from `git rev-parse 5c99f2d4:.ufo/waves/round-30/w1/CaseR30<x>.md`):
  a `61db9a9b3d10a93b41c4db9a2a5438d4d07aa5d0`, b `4a0bb80d27e803e7ed7a311aba909e3da9a70371`,
  c `7a4d82c268a899e3cc1631beced02101d00f4043`, d `fb70eadfef703c82dd168f0d7e128ca66d5e576f`.
- Rule: `.ufo/waves/round-31/rule-text.md:3-6` (interface, `{report}`, `file://` strip) and `:10-22`
  (rules 1-6). Line numbers below are stable for that file.
- Allow list as numbered here (`{report}` = brief basename without `.md`):
  A1 `.ufo/waves/round-30/rule-text.md`
  A2 `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-30/rule-text.md`
  A3 `/fast/scratch/hyaku/mori-r30/{report}`
  A4 `/fast/scratch/hyaku/mori-r30/{report}/*`
  A5 `/fast/scratch/hyaku/mori-r30/MoriR30.{report}`
  A6 `/fast/scratch/hyaku/mori-r30/MoriR30.{report}/*`
  A7 `https://raw.githubusercontent.com/rfjakob/earlyoom/*`
  A8 `https://github.com/rfjakob/earlyoom/*`
  A9 `https://raw.githubusercontent.com/systemd/systemd/*`
  A10 `https://github.com/systemd/systemd/*`
  A11 `https://www.freedesktop.org/software/systemd/*`
  A12 `/home/vgpnk/.agents/skills/godspeed/SKILL.md`
  A13 `/home/vgpnk/.omp/agent/RULES.md`
- Invocation scanned: `tools/mori-blind-check.sh 5c99f2d4... .ufo/waves/round-30/w1 '^CaseR30[a-d]\.md$' <allow-file>`.
  The tree at that revision holds 36 files; exactly the four `CaseR30[a-d].md` match the regex, so `scanned=4`.

## 1. Headline result (what the tool must print)

Block structure drives everything: each brief has exactly one block opener, `## Files opened`
(`.ufo/waves/round-30/w1/CaseR30a.md:95`, `CaseR30b.md:115`, `CaseR30c.md:77`, `CaseR30d.md:109`; the label form
`Files opened:` never occurs, and no other heading or opener exists — `grep -inE 'files opened|opened files'` returns
only those four lines).

Rules 2 and 3 decide the rest: an entry must start with `- `/`* `/`+ `/`N. `/`N) ` or `|` (`rule-text.md:13-15`), and
the block closes at the first other non-blank line (`rule-text.md:16`). Briefs a, b and d list their files as **bare
path lines with no list marker** (a:96-103, b:116-121, d:110-116), so the block closes on the very next line and
contains **zero entries**. Rule 5 (`rule-text.md:21`) then emits one `writer-missing-files-opened-list` at line 1 for
each. Brief c uses `- ` entries (78-84), so it is parsed, and every candidate resolves to the allow list.

```text
scanned=4
blind_violations=3
CaseR30a.md:1:writer-missing-files-opened-list
CaseR30b.md:1:writer-missing-files-opened-list
CaseR30d.md:1:writer-missing-files-opened-list
# exit status 1
```

No `writer-forbidden-opened-path`, no `writer-tool-source-citation`, no `writer-tool-run-output` line on any of the
four. The printed order above is git tree order; the spec fixes the set, not the order, so a selftest should compare
records as a set and check `blind_violations` equals the record count (3).

## 2. Paste-ready table: per brief

| brief | opener | block range (closes at) | entry lines | candidates → verdict | files-opened (line, rule) | citation | run-output |
|---|---|---|---|---|---|---|---|
| CaseR30a.md | `## Files opened` :95 | 95 (closes :96) | none — :96 starts `/`, no marker | none reached: :96-103 are outside every block | (1, writer-missing-files-opened-list) | cannot fire | cannot fire |
| CaseR30b.md | `## Files opened` :115 | 115 (closes :116) | none — :116 starts `/`, no marker | none reached: :116-121 outside every block | (1, writer-missing-files-opened-list) | cannot fire | cannot fire |
| CaseR30c.md | `## Files opened` :77 | 77-85 (blank :85; closes :86) | 78, 79, 80, 81, 82, 83, 84 | all allowed (table §3) | none (empty set) | cannot fire | cannot fire |
| CaseR30d.md | `## Files opened` :109 | 109 (closes :110) | none — :110 starts `/`, no marker | none reached: :110-116 outside every block | (1, writer-missing-files-opened-list) | cannot fire | cannot fire |

Paste-ready expected-record table for the selftest data:

| file | line | rule |
|---|---|---|
| CaseR30a.md | 1 | writer-missing-files-opened-list |
| CaseR30b.md | 1 | writer-missing-files-opened-list |
| CaseR30d.md | 1 | writer-missing-files-opened-list |

Negative half of the same selftest (single-file runs, same allow file):

| invocation | expected stdout | exit |
|---|---|---|
| writer regex `^CaseR30c\.md$` | `scanned=1` / `blind_violations=0` / no record | 0 |
| writer regex `^CaseR30a\.md$` | `scanned=1` / `blind_violations=1` / `CaseR30a.md:1:writer-missing-files-opened-list` | 1 |

## 3. Case c, entry by entry (`rule-text.md:17-20`: strip, then test)

Candidate test after stripping wrapping backticks/quotes/brackets, trailing `,;.`, and a `:L`/`:L-M` suffix: token
contains `://`, `/` or `.`, or equals one of the four bare names. `{report}` = `CaseR30c` (A3-A6 unused).

| line | entry (abridged) | candidate(s) after strip | allow hit | verdict |
|---|---|---|---|---|
| 78 | `- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-30/rule-text.md:1-114` | same path, `:1-114` stripped | A2 exact | allowed |
| 79 | `- /home/vgpnk/.agents/skills/godspeed/SKILL.md` | same path | A12 exact | allowed |
| 80 | `- https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c` + access stamp, sha256, `:161`, 5-word excerpt | URL only | A7 prefix | allowed |
| 81 | `- https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c — … :627 …` | URL only | A7 prefix | allowed |
| 82 | `- https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h — … :17 …` | URL only | A7 prefix | allowed |
| 83 | `- https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/MANPAGE.md — … :41 …` | URL only | A7 prefix | allowed |
| 84 | `- https://www.freedesktop.org/software/systemd/man/262/org.freedesktop.systemd1.html — … :1297 …` | URL only | A11 prefix | allowed |

Tokens on those lines that are deliberately **not** candidates: the access-time stamps (`2026-10-22T21:12:39Z;` has
no `.` or `/`), the 64-hex sha256 digests (same), `:161`/`:627`/`:17`/`:1297` (become empty after the `:L` strip),
`(5`/`(17`/`(8`/`(10`, `words):`, the em dash, and the backticked C-format fragments (`fprintf(stderr,`, `"earlyoom`,
`VERSION`, `"\n");`, `%s`, `%d`, `\"%s\":`, `oom_score`, `%lld`, `MiB,`, `cmdline`, `__attribute__((format(printf,`,
`2)));`, `**both**`, `**and**`) — none contains `.`, `/` or `://`, and `...` (line 82, from `...)`) strips to empty
(see risk R2).

## 4. Tool detectors (rule 6: round-30 gate, unchanged)

Round-30 definitions copied from `.ufo/waves/round-30/check-blind-wave.sh:76-82`; citation detection is applied to
every line (`:121-123`), run-output only to unprotected lines (`:135-154`). Exact-ERE audit over all four briefs:

- `writer-tool-source-citation` — **zero matches**. `mori-oom-killers.py:<n>` never appears; `tool lines N` /
  `tool: N` never appear (`grep -nE` with both gate regexes returned nothing). So no hit on any line, protected or not.
- `writer-tool-run-output` — **cannot fire, though the arming line is present in every brief**. The gate's
  `tool_run_re` matches exactly once per file, always the last line: a:105, b:122, c:86, d:118 (`…lane tool output…` /
  `…lane-tool output…`). Each such line only sets `pending_tool=8`; no later line exists, none of the four lines
  itself carries `KILLERS_ACTED|KILLERS_QUIET|KILLERS_UNKNOWN` or an exit token (measured: 0 and 0), and the
  same-line rule needs verdict and exit together, so `output_marker` never becomes 1.
- Near-misses that also do not fire: `--inputs` never appears and `MORI_OOM_KILLERS_SELFTEST:` never appears
  (case-insensitive audit). The case JSON is unprotected for the detectors (the fence at line 1 opens while
  `in_case_section=0`), so `"verdict": "KILLERS_UNKNOWN"` (a:28,70; b:40,84; c:21,48; d:40,83) is visible, but
  `exit_re` does **not** match `"exit": 2,` (a quote sits between `exit` and `:`), and no pending flag is armed
  anywhere near them. Prose such as `KILLERS_UNKNOWN (exit 2)` (a:7, d:54) does satisfy both, but its line matches
  neither `tool_run_re` nor an armed window.

## 5. Risks and edge cases the selftest must pin

- **R1 (headline, not a bug).** a/b/d are expected to be `missing-files-opened-list`, not clean: their file lists are
  unmarked, so rule 2 (`rule-text.md:13-15`) admits no entry and rule 3 (`:16`) closes the block immediately. The
  frozen fixtures agree that unmarked lines are not entries: F05 is `## Files opened` + blank + prose and expects only
  `(1, missing)`, not a forbidden hit on the prose line (`.ufo/waves/round-31/c2-fixtures.json:80`); F01's trailing
  prose after a real list expects nothing (`c2-fixtures.json:16`). If the L1 expects a/b/d clean, either the tool or
  the rule text is wrong — the rule text is unambiguous, so encode the three missing hits. For completeness, if those
  bare lines were wrongly taken as entries, every candidate still matches the allow list: a:96-103 (A12, A13, A2,
  A7 x4, A9), b:116-121 (A12, A2, A7 x4), d:110-116 (A12, A2, A7 x4, A9), so no forbidden hit would arise there
  either; the only line that changes verdict between the two readings is a:105 (R3).
- **R2 (strip order).** Line 82 contains `...)` and `...`. Rule 4 strips trailing `,;.` *before* the candidate test, so
  these become empty and are not candidates. A tool that tests "contains `.`" first prints a false
  `CaseR30c.md:82:writer-forbidden-opened-path`; that must not appear.
- **R3 (closure depth).** a:105 contains the only path-like token in any trailing prose (`json.load`), the exact
  round-30 D1 false positive (`corpus/lessons/round-30-verifier-spotcheck.md:176`). Under rule 3 the block died at
  a:96, so 105 is never inspected. A lenient parser flags it; this line is the discriminating negative for rule 3.
  b:122, c:86 and d:118 contain no path-like token at all (`report.` strips to `report`), so they cannot fire even
  under a lenient parser.
- **R4 (untested by these four).** The table separator/top-row exclusion (`rule-text.md:14-15`) is never exercised:
  the tables at a:82-93, b:98-113, c:61-75, d:96-107 sit above the opener and outside every block. Coverage must come
  from fixtures F06/F10 (`c2-fixtures.json:95`, `:154`), not from the real briefs.
- **R5 (set, not order).** Hit order follows git tree order here (a, b, d); the C2 predicate requires the exact set,
  so compare sets and assert `blind_violations == len(records) == 3`.
- **R6 (`{report}`/A3-A6).** No candidate in these four briefs touches the scratch paths, so this run does not
  exercise the `{report}` substitution; F11/F12 cover it (`c2-fixtures.json:176`, `:191`).

## 6. Unresolved / not claimed

- I did not run `tools/mori-blind-check.sh` (not present yet at the entering tip) and did not execute any parser
  simulator; every verdict above is a hand application of `rule-text.md:10-22`, cross-checked only against the frozen
  fixture expectations where they disambiguate (F01/F05). If the landed tool disagrees, the disagreement is a finding
  for the C2 critic, not an adjustment to this table.
- No tools were installed or updated for this seat.
