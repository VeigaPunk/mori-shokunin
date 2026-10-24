# Round-32 wave 1 — routed defect 6: blind-check edge fixtures (seat `ExecEdgeFixtures`)

Scope: one minimal fixture brief per named edge case of `tools/mori-blind-check.sh` (routed defect 6,
`corpus/lessons/round-31-verifier-spotcheck.md:224-227`), each with the rule-text clause that governs it, the report
that clause requires, and the tool's actual stdout/exit. **No tool change**: the fixtures pin current behaviour as
evidence. Nothing was written in the lane except this report; all fixtures, the runner and the generator live under
`/fast/scratch/hyaku/mori-r32/ExecEdgeFixtures/`.

## Axes

1. Coverage of the 9 named edge shapes (setext, indented `#`, CRLF, tab after `-`, `../` through an allow glob,
   fenced `# files opened`, words between `files`/`opened`, lead-in prose, sub-heading in block), plus 3 controls that
   isolate *why* a shape behaves as it does.
2. Fidelity: expected column derived from the quoted rule text *before* the tool ran; actual recorded verbatim.
3. Reproducibility: one runner that rebuilds the sandbox, reruns the lane tool and re-checks every stored actual.

## Artifacts

| path | what | sha256 (bytes) |
|---|---|---|
| `…/ExecEdgeFixtures/fixtures/edge-r32.json` | 12 cases: brief bytes (base64+text), rule-text reading, expected, alt reading, actual, agree | `79b530f6…2539` (33 604) |
| `…/ExecEdgeFixtures/run-edge-r32.py` | runner; reproduces the `actual` column, `--update` rewrites it | `569bdfbb…370b` (4 854) |
| `…/ExecEdgeFixtures/make-edge-r32.py` | generator of the JSON (briefs + expected, no tool run) | `74a13753…de91` (21 252) |
| `…/ExecEdgeFixtures/sandbox/repo` | sandbox git repo, rev `70c1699d4a19f59bc37242176c8aef14950893a3` | — |

Inputs (read-only): tool `tools/mori-blind-check.sh` sha256 `79b774f7…beb8` at lane HEAD `8ab61aff` (blob unchanged
since `458ff1c3`); rule text `.ufo/waves/round-31/rule-text.md` sha256 `79ea24c8…698b`.

## Method (exactly as the usage says)

`run-edge-r32.py` writes each brief's bytes and one allow file into a fresh sandbox repo, commits, then for each case
runs, with cwd = the sandbox repo:

`timeout 120 bash /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-blind-check.sh <sandbox-rev> .ufo/waves/round-32/fx/<id> '^CaseE[0-9]+[a-z]?\.md$' <sandbox>/allow/<id>.txt`

Per-case wave dir → `scanned=1`. Blob fidelity was checked: `git show <rev>:<path>` sha256 equals each
`brief_sha256`, including the CRLF case (`b'\r\n'` present, 0d0a in the bytes).

## Case table

`L<n>` = hit line; expected is the primary rule-text reading (`rule_text_reading.basis`); alt = the competing reading.

| id | shape | expected (primary) | actual | agree | alt (reading → expected / agree_alt) |
|---|---|---|---|---|---|
| E01 | setext heading | none / exit 0 | L1 writer-missing-files-opened-list / exit 1 | **no** | atx-only → L1 missing / yes |
| E02 | `#` heading indented 2 | none / exit 0 | L1 missing / exit 1 | **no** | atx-col-0 → L1 missing / yes |
| E02b | control: `#` indented 4 (code block) | L1 missing / exit 1 | L1 missing / exit 1 | yes | — |
| E03 | CRLF endings | none / exit 0 | L2 forbidden-opened-path / exit 1 | **no** | byte-literal → L2 forbidden / yes |
| E04 | tab straight after `-` | L1 missing / exit 1 | L1 missing / exit 1 | yes | CommonMark list item → L2 forbidden / no |
| E05 | `../` through allow glob | none / exit 0 | none / exit 0 | yes | path normalisation → L2 forbidden / no |
| E06 | fenced `# files opened` | none / exit 0 | L5 forbidden-opened-path / exit 1 | **no** | fence-blind → L5 forbidden / yes |
| E06b | control: ` ```json ` fence | L5 forbidden / exit 1 | L5 forbidden / exit 1 | yes | — |
| E07 | words between `files`/`opened` | L1 missing / exit 1 | L1 missing / exit 1 | yes | loose-mention → none / no |
| E08 | lead-in prose before entry | L1 missing / exit 1 | L1 missing / exit 1 | yes | loose-lead-in → none / no |
| E09 | sub-heading inside block | none / exit 0 | none / exit 0 | yes | markdown-section → L4 forbidden / no |
| E09b | control: entries only after sub-heading | L1 missing / exit 1 | L1 missing / exit 1 | yes | — |

Tally: 4 divergences from the primary reading (E01, E02, E03, E06), 5 literal-reading agreements (E04, E05, E07, E08,
E09), 3 controls agreeing. Every divergence is one of the limits SKILL.md already names at `SKILL.md:778-781`.

## Per-case detail (brief bytes · clause · expected · actual)

Rule-text clauses (verbatim, `rule-text.md`): C1 = "A block opens at a Markdown heading (any level) whose text
contains `files opened` or `opened files` (case-insensitive), or at a line whose trimmed text starts with `Files
opened:` or `Opened files:` (case-insensitive)." C2 = "Entries are the following lines that start (after optional
indentation) with `- `, `* `, `+ `, `N. ` or `N) `, or with `|` (a table row)…" C3 = "The block closes at the first
heading or at the first other non-blank line." C4 = "…An entry with no candidate, or with a candidate no allow line
matches, is one `writer-forbidden-opened-path` hit at its own line." C5 = "A brief with no entry in any block is one
`writer-missing-files-opened-list` hit at line 1."

**E01 setext** — `Files opened\n------------\n- .ufo/waves/round-31/rule-text.md\n` (61 B, `ea1a59e4…`).
C1+C2+C4: a setext heading is a Markdown heading, its text is `Files opened`, so the block opens, the `- ` line is an
entry and its candidate matches the allow line → no hit, exit 0. Actual: `scanned=1` / `blind_violations=1` /
`.ufo/waves/round-32/fx/e01/CaseE01.md:1:writer-missing-files-opened-list`, exit 1 → **agree=no**; the ATX-only
reading predicts exactly this (agree_alt=yes). The tool never opens a block: `heading_re='^#{1,6}[[:space:]]'`
(`tools/mori-blind-check.sh:100`, tested on the raw line at `:132-136`).

**E02 indented `#`** — `  ## Files opened\n  - .ufo/waves/round-31/rule-text.md\n` (55 B, `5be64a4e…`). C1 says "a
Markdown heading (any level)" with no column-0 qualifier; CommonMark allows 1–3 spaces of heading indent. Expected:
block opens, entry allowed → no hit, exit 0. Actual: `scanned=1` / `blind_violations=1` /
`…/e02/CaseE02.md:1:writer-missing-files-opened-list`, exit 1 → **agree=no** (alt atx-col-0 → yes).

**E02b control, `#` indented 4** — `    ## Files opened\n    - …\n` (59 B, `b681bf92…`). Four spaces is an indented
code block in CommonMark, not a heading under any reading; C5 then gives the missing-list hit at line 1. Actual:
`scanned=1` / `blind_violations=1` / `…/e02b/CaseE02b.md:1:writer-missing-files-opened-list`, exit 1 → agree=yes.
Pinned consequence: the tool's reaction to indentation is depth-sensitive, so E02 isolates heading indentation and
not indentation in general.

**E03 CRLF** — `## Files opened\r\n- .ufo/waves/round-31/rule-text.md\r\n` (53 B, `c0e7c01d…`; bytes contain 0d0a). No
clause mentions line terminators, so CRLF reads as a terminator: heading contains `files opened` (C1), entry (C2),
candidate matches the allow line (C4) → no hit, exit 0. Actual: `scanned=1` / `blind_violations=1` /
`…/e03/CaseE03.md:2:writer-forbidden-opened-path`, exit 1 → **agree=no**. The `\r` stays in the path token, so an
exact allow line stops matching. Probe (see below): with a trailing-`*` allow line the same brief passes, so the
failure is allow-line-shape dependent.

**E04 tab after `-`** — `## Files opened\n-\t/etc/passwd\n` (30 B, `91e47cf7…`). C2 lists the marker as `- ` (dash
space); `-\t` is not that marker, so the line is not an entry, C3 closes the block there and C5 gives one hit at line
1. Actual: `scanned=1` / `blind_violations=1` / `…/e04/CaseE04.md:1:writer-missing-files-opened-list`, exit 1 →
agree=yes. Under the CommonMark reading it would instead be a list item → `…:2:writer-forbidden-opened-path`
(agree_alt=no). Both readings exit 1; only the rule differs, so this shape needs rule-aware comparison.

**E05 `../` through an allow glob** — `## Files opened\n- /fast/scratch/hyaku/mori-r32/ExecEdgeFixtures/allowed/../../secret.txt\n`
(89 B, `1ba28ba8…`), allow line `/fast/scratch/hyaku/mori-r32/ExecEdgeFixtures/allowed/*`. C4 forbids a candidate
only when "no allow line matches"; the literal token matches the glob (bash `*` spans `/`) and no clause normalises
`..` → no hit, exit 0. Actual: `scanned=1` / `blind_violations=0`, exit 0 → agree=yes. Normalising first would resolve
to `…/ExecEdgeFixtures/secret.txt`, outside `allowed/` → L2 forbidden (agree_alt=no).

**E06 fenced `# files opened`** — `## Cases\n\n```text\n# files opened\n- /etc/passwd\n```\n\n## Files opened\n- .ufo/…rule-text.md\n`
(103 B, `014196c3…`). C1 opens blocks at "a Markdown heading"; a fenced line is code, not a heading, and its `- `
line is not an entry; the real `## Files opened` block's entry is allowed → no hit, exit 0. Actual: `scanned=1` /
`blind_violations=1` / `…/e06/CaseE06.md:5:writer-forbidden-opened-path`, exit 1 → **agree=no** (fence-blind → yes).
This is residual ReviewC2Tool F1 named at `SKILL.md:781`.

**E06b control, ` ```json ` fence** — same brief with `json` on the fence line (103 B, `8c8630f2…`). The tool's
`in_case_json` protection is scoped to the two round-30 detectors, not to the files-opened parser, so the fenced
heading still opens a block and the fenced path is still a forbidden entry. Expected (tool-faithful): L5 forbidden,
exit 1. Actual: `scanned=1` / `blind_violations=1` / `…/e06b/CaseE06b.md:5:writer-forbidden-opened-path`, exit 1 →
agree=yes. Pinned consequence: E06 measures fence-blindness, not a missing json exemption.

**E07 heading with words between `files` and `opened`** — `## Files I opened\n- .ufo/…rule-text.md\n` (53 B,
`208e9633…`). C1 requires the heading text to contain `files opened` or `opened files`; `Files I opened` contains
neither → no block → the `- ` line is not an entry → C5 gives one hit at line 1. Actual: `scanned=1` /
`blind_violations=1` / `…/e07/CaseE07.md:1:writer-missing-files-opened-list`, exit 1 → agree=yes; a loose
"mentions files and opened" reading would report nothing (agree_alt=no). This is the round-29 shape recorded at
`corpus/lessons/round-31.md:105-107`.

**E08 lead-in prose before the first entry** — `## Files opened\nI read the rule text before listing the entries.\n- .ufo/…rule-text.md\n`
(100 B, `6de804ef…`). C3 closes the block "at the first other non-blank line", so the prose closes it and the list
below is not an entry → C5 one hit at line 1. Actual: `scanned=1` / `blind_violations=1` /
`…/e08/CaseE08.md:1:writer-missing-files-opened-list`, exit 1 → agree=yes (loose lead-in reading → no hit,
agree_alt=no).

**E09 sub-heading inside the block** — `## Files opened\n- .ufo/…rule-text.md\n### Notes\n- /etc/passwd\n` (75 B,
`b487719a…`). C3 closes the block "at the first heading" with no depth rule, so `### Notes` closes it and the
`/etc/passwd` line below is not an entry; the one entry is allowed → no hit, exit 0. Actual: `scanned=1` /
`blind_violations=0`, exit 0 → agree=yes. A Markdown-section reading (deeper heading keeps the section open) would
flag L4 (agree_alt=no).

**E09b control, entries only after the sub-heading** — `## Files opened\n### Notes\n- .ufo/…rule-text.md\n` (61 B,
`d504e570…`). The sub-heading closes the block before any entry, so C5 applies: one missing-list hit at line 1.
Actual: `scanned=1` / `blind_violations=1` / `…/e09b/CaseE09b.md:1:writer-missing-files-opened-list`, exit 1 →
agree=yes. This is the round-29 consequence the lesson describes ("the literal reading yields missing-list hits a
looser reading would not", `corpus/lessons/round-31.md:105-107`).

## CRLF allow-shape probe (extra evidence, same sandbox pattern)

Same CRLF brief, path `/fast/scratch/hyaku/mori-r32/ExecEdgeFixtures/out/e03.txt`, two allow files:

- allow `/fast/scratch/hyaku/mori-r32/ExecEdgeFixtures/out/*` → `scanned=1` / `blind_violations=0`, exit 0.
- allow `/fast/scratch/hyaku/mori-r32/ExecEdgeFixtures/out/e03.txt` (exact) → `scanned=1` / `blind_violations=1` /
  `.ufo/waves/round-32/fx/p/CaseP.md:2:writer-forbidden-opened-path`, exit 1.

So the CRLF defect is not "CRLF always fails": a trailing `*` starves the match of the `\r`, an exact allow line does
not. Any future fix has to treat the token, not the allow file, as the place to strip the terminator.

## Divergence / ambiguity classification

- **Tool diverges from the rule text** (primary reading): E01, E02, E03, E06 — in each the tool emits one
  `writer-forbidden-opened-path` or `writer-missing-files-opened-list` hit where the clause requires none. All four
  are the limits already named at `SKILL.md:778-781`.
- **Tool follows the clause literally; a competing reading differs**: E04, E05, E07, E08, E09. For E04 and E05 the
  clause text does not support the stricter reading (it says `- `, and it states no normalisation), yet
  `SKILL.md:779-780` lists both as known limits — so the *intent* reading is the alt column and the written rule is
  the gap. For E07, E08, E09 the lane's own lesson takes the literal reading as correct
  (`corpus/lessons/round-31.md:105-107`), and the fixtures confirm the tool implements it.
- **Controls**: E02b (indent depth), E06b (json-fence scope), E09b (sub-heading → missing-list consequence) all agree
  with their stated expectations, which is what makes the neighbouring divergences attributable to the intended
  property rather than to a stray hit.

## Reproducibility

```
cd /fast/scratch/hyaku/mori-r32/ExecEdgeFixtures
python3 make-edge-r32.py      # rewrites fixtures/edge-r32.json (briefs + expected, no tool run)
python3 run-edge-r32.py       # rebuilds sandbox, reruns the lane tool, compares the actual column
python3 run-edge-r32.py --update   # rewrites actual + agree/agree_alt + actual_run receipt
```

Observed on rerun: `stored actual column reproduced for every case` (exit 0). Blob check: all 12
`git show <rev>:<path>` sha256s equal their `brief_sha256` (`all_blobs_match= True`). Stored receipt in the JSON:
`sandbox_rev=70c1699d…`, `tool_sha256=79b774f7…beb8`.

## Risks and limits

- The runner and fixtures are scratch-only; the JSON is evidence, not a gate input. Nothing in the lane changed:
  `tools/mori-blind-check.sh` sha256 is still `79b774f7…` and `git status --porcelain` in the lane shows no tracked
  modification from this seat (only other seats' untracked dirs and this report).
- `expected` is the rule-text reading I state with the clause; where the clause is ambiguous the alt reading is
  recorded with its own expected. A judge reviewing a case should read the `basis` field before treating `agree=no`
  as a defect.
- The `\r`-in-token mechanism for E03 was verified indirectly (exact vs glob allow line probe above); no patched
  tool was built, per "no tool change".
- Not exercised: headings inside list items/blockquotes, setext underlines of `===`, `~~~` fences, `|`-table entries,
  and nested allow-glob `**`; none is named by defect 6.

## Tooling

No tool installed or updated; no pacman transaction run (host-wide pause respected). `git`, `python3` 3.14.8 and
`bash` 5.3.20 were already present. No background jobs started; every process finished inside its `timeout`.
