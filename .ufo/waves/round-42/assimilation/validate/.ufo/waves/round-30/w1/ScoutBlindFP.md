# ScoutBlindFP — class spec for the 20 round-29 blindness-gate hits

Seat: MoriR30.ScoutBlindFP (leaf). Evidence read at lane rev
`221cbd8faa88e07ad20445d5a87bbc1a3039d73e` (read-only `git show`), the rev the gate ran
(`.ufo/waves/round-29/evidence/blind-check-prefreeze.txt:1`). Hit set:
`.ufo/waves/round-29/evidence/blind-check-prefreeze.txt:4-23`. Adjudication read:
`.ufo/waves/round-29/w2/AdjudicateBlindHits.md`. Gate source read:
`.ufo/waves/round-29/check-blind-wave.sh:59-64` (patterns), `:74-156` (loop).

Matched text is not quoted anywhere below; hits are named by file and line only. Every
predicate claim was re-executed per hit line (scratch probe), and the whole corrected rule
set was measured against all 35 wave-1 reports at that rev: **counted violations 0,
specimens 1**. No tool was installed or updated.

## Class table (20 hits)

| id | predicate that fired | hits | file:line (all at rev 221cbd8f) |
|---|---|---|---|
| P1 | generic round-id ∧ result conjunction | 9 | AxisOperability.md:19; BuildTipReceipts.md:5,135,136,137,140; ReviewLateMutCountC1Amended.md:78; ReviewLateMutHeadingCheck.md:37,39 |
| P2 | case-insensitive substring of the tool-header phrase | 1 | DraftQualityCriteria.md:75 |
| P3 | selftest-marker substring, no allowed tally after it | 1 | DraftQualityCriteria.md:76 |
| P4 | `--inputs` flag coinciding with a result token | 1 | DraftQualityCriteria.md:77 |
| P5 | tool-file citation regex | 1 | DraftQualityCriteria.md:86 |
| P6 | exact files-opened heading grammar | 7 | CaseA207a.md:1; CaseA207b.md:1; CaseA207c.md:1; CaseA207d.md:1; CaseA210a.md:1; CaseA210b.md:1; CaseA210d.md:1 |

9+1+1+1+1+7 = 20. Correction to the adjudication summary
(`.ufo/waves/round-29/w2/AdjudicateBlindHits.md:70-80`): it counts 10 P1 + 3 P2-P4 + 1 P5
= 14 non-writer, but there are 13 non-writer hits; the per-line table in that file is
correct and only its summary arithmetic is off by one. Independently reproduced split:
9 / 1 / 1 / 1 / 1 / 7.

## Text kinds per class (no quoted text)

- P1-k1 `AxisOperability.md:19`: a shell command echo with a redirect and a trailing
  status comment. The round token is a substring of a `/tmp` file name.
- P1-k2 `BuildTipReceipts.md:5`: prose describing a generator's exit-code behaviour.
- P1-k3 `BuildTipReceipts.md:135-137,140`: demo receipt write lines (scratch path plus a
  parenthesized status).
- P1-k4 `ReviewLateMutCountC1Amended.md:78`: prose summary of a *different* checker's
  metric set and exit status.
- P1-k5 `ReviewLateMutHeadingCheck.md:37,39`: markdown table rows naming an unrelated
  Python checker and that checker's exit status.
- P2-P5 (all four): the criteria document's ready-to-paste QUALITY block
  (`DraftQualityCriteria.md:69-116`, a `markdown` fence). The sensitive shape appears in
  inline code spans as a *definition*: a grammar metavariable (`:75`), a category name
  (`:76`), a flag name (`:77`), and the criterion's own red-input example (`:86`). The
  tempting blanket fix -- ignore every fenced block -- would blind the gate to pasted
  output: the P1 receipt lines sit in a `text` fence (`BuildTipReceipts.md:134-138`).
- P6: the writer files' own files-opened headings (five distinct phrasings), each followed
  by a genuine list. `CaseA210c.md:194` happens to match the strict grammar and was not
  flagged, which proves the strict branch works; the fix is broadening, not replacement.

## P1 — round-id ∧ exit-status conjunction

Observed (reproduced per line): every P1 line pairs an `rN` token with an `exit 0|1|2`.
All nine statuses belong to non-tool commands (a `git show`, a receipt generator, a
retention scan, a heading checker, a supersed check). None carries a tool verdict. The `rN` alternative caught zero
real leaks in this wave.

Rule change (replace, do not extend):

1. Delete the `rN` alternative of the round-id predicate. Round names, file names that embed a round
   number, and table cells naming a round are ordinary citation, and `exit N` is ordinary
   prose; their coincidence is not evidence of a tool run.
2. Keep only a *same-run repro claim*: an `observed:` token (case-insensitive) or
   `run e<N>`, followed by a tool verdict or exit status within 60 characters and within
   the same inline-code-span-delimited run, with no table-cell separator between:

   `((?i:observed:)|run[[:space:]]+[eE][0-9]+)[^`|]{0,60}(KILLER_ACTED|KILLERS_QUIET|KILLERS_UNKNOWN|exit[[:space:]]+[012])`

   The vocabulary tokens stay uppercase and case-sensitive.

Must-catch synthetic leak:

```text
observed: after the send -> exit 0, no process killed
```

Measured: fires `repro` (both `observed:` and `Observed:` forms); the nine P1 lines do not.

## P2 — tool-header phrase

The predicate is a case-insensitive substring over the whole line. In `:75` the phrase is
one alternative inside a definition sentence in a markdown fenced block. A real citation
header is a table header or a labelled column, not prose.

Rule change: require cell position.

`^[[:space:]]*\|?[[:space:]]*tool[[:space:]]+lines[[:space:]]*(\||:[[:space:]]*[0-9])`

applied per run, case-insensitively. A hit inside a `markdown` fence is reported as a
specimen, not counted (same treatment as P5).

Must-catch synthetic leak:

```text
| Tool lines | 305-330 |
```

## P3 — selftest marker

The predicate flags a marker substring anywhere without an allowed tally immediately after
it. In `:76` the marker is a quoted category name inside an inline span, followed by the
word "line".

Rule change: the marker counts only with a status token in the same run, allowing for one
closing backtick:

`MORI_OOM_KILLERS_SELFTEST:[[:space:]]*`?[[:space:]]*(PASS[[:space:]]+(30/30|32/32)|FAIL|ERROR|[0-9]+/[0-9]+)`

A violation is (a) a captured status other than `PASS 30/30` or `PASS 32/32`, or (b) a
marker at the start of a run that is *not* inside backticks and has no status (a pasted
marker line). A marker alone inside backticks is a quoted specimen and is not counted.

Must-catch synthetic leak:

```text
MORI_OOM_KILLERS_SELFTEST: FAIL cases-a2.json:07
```

plus the bare marker line `MORI_OOM_KILLERS_SELFTEST:` at line start (fires `baremark`).
Allowed controls verified: `PASS 32/32` and `PASS 30/30`, plain and backticked, stay clean.

## P4 — inputs flag ∧ result

The predicate fires on any line containing the flag and any result token. In `:77` both
tokens are separate inline spans naming the category.

Rule change: the flag needs a concrete JSON argument and a result in the same run:

`--inputs[[:space:]]+\S+\.json[^`|]{0,60}(KILLER_ACTED|KILLERS_QUIET|KILLERS_UNKNOWN|exit[[:space:]]+[012])`

Must-catch synthetic leak:

```text
run under --inputs cases-a2.json: KILLERS_QUIET exit 0.
```

## P5 — tool-file citation

The citation regex is correct; the false positive is contextual. `:86` is the criterion's
own red-input example (an invented file with a concrete line number), placed inside a fenced block tagged
`markdown` whose whole content is the text to append to `corpus/QUALITY.md`. The identical
line in an ordinary report is a real leak, so no text-local distinction exists.

Rule change: scope by the enclosing fence's info string.

- Track fence state; a fence whose info string is `markdown` is a quoted-document region.
- A citation found in such a region is accumulated as `specimen_citations=<n>` per file and
  printed, but does not increment violations.
- A citation anywhere else (prose, plain fences, table rows, `text`/`bash` fences) is a
  violation exactly as today. No file-name allowlist and no role header: a path whitelist
  would exempt the whole file, which is weaker than scoping to the fenced region.

Must-catch synthetic leak (ordinary report, no fence):

```text
| branch | mori-oom-killers.py:512 | send path |
```

Verified: the same line inside a `markdown` fence yields exactly one specimen and zero
counted violations.

## P6 — files-opened heading

Two defects, one visible and one hidden.

Visible: the header test anchors to end-of-line, so any qualifying words after the
files/opened pair break it. All seven headers are ordinary English headings with extra
words; each section has a real list.

Hidden (the leak this false positive hides): when a heading is not recognised, the
forbidden-path scan never runs. Today a writer can use a non-matching heading and list the
tool, another report, or `corpus/lessons/` with no violation. Also, the list scan ends at
*any* heading, so even a matching header is truncated by a sub-heading:
`CaseA207d.md:194` has its entries under `### Lane files` at `:196` and `### Upstream
sources` at `:206`, so scanning stops after two blank lines.

Rule change:

1. Accept a header when either (a) the strict whole-line form still matches, or (b) the
   line is an ATX heading whose text, lowercased, contains a noun from
   `files?|sources?|urls?|evidence|inputs` and a verb from
   `opened|read|accessed|consulted|examined`, in either order, and contains no negation
   word (`not|never|no|none`). This covers all five observed phrasings and rejects
   `## Files not opened`.
2. Section extent: from the header to the next heading of equal or shallower level; deeper
   sub-headings stay inside the section. A prose-form label (`Files opened:`) has level 0
   and closes at the next heading of any level.
3. Require at least one path-like token in the section (`/`, `.md`, `.json`, `://`), not
   merely a non-blank line; today a one-word placeholder entry would satisfy the rule.
4. Forbidden-path test, in-section items and table rows only: for each occurrence of the
   tool file name or `corpus/lessons/`, exempt only when a negator
   (`not|never|no|without|none`) precedes it in the same clause (boundaries `;`, `. `,
   ` but `, ` however `). This separates a disclosure bullet (`CaseA210a.md:212`,
   `CaseA210d.md:191`; `CaseA207d.md:220` is outside the section) from an entry. Keep the
   report-reference test and the three own-path exemptions (`w1/<own>.md`,
   `round-29/w1/<own>.md`, `.ufo/waves/round-29/w1/<own>.md`, plus any suffix ending in
   the last form).
5. Keep `writer-missing-files-opened-list` when no header is found at all.

Must-catch synthetic leak (a writer entry under a heading the old gate cannot see):

```text
## Opened files and URLs

- tools/mori-oom-killers.py — whole file
```

Measured on the real round-29 gate in a sandbox git repo: this file produces only one
fact, `writer-missing-files-opened-list` at `:1`; the entry at `:3` is not reported. With
the strict heading `## Files opened` the same entry is reported as
`writer-forbidden-opened-path` at `:3`, which proves the scan works once the heading is
recognised. Additional must-catch lines: `- corpus/lessons/round-29.md` and
`- .ufo/waves/round-29/w2/CriticC2Design.md — read` as in-section entries; and
`## Files not opened` must *not* satisfy the requirement, so a file whose only heading is
that one still fires `writer-missing-files-opened-list` (verified).

## Implementation constraint discovered by the prototype

Do **not** implement "same run" by deleting inline code spans and matching the remainder.
Deletion concatenates text that backticks separate: `ReviewLateMutCountC1Amended.md:78`
then puts an `observed:` token and a later exit status into one apparent run and becomes a
false positive again. Split each line into *ordered runs* (outside text, span content,
outside text, ...) and apply every predicate run by run. Also test "first run" by index,
not by string identity.

## Residual risks (state them; do not hide them)

- The `markdown`-fence specimen rule lets a non-writer hide a citation in such a fence; it
  is counted and printed, not silently dropped, but it is not a failure.
- The negation-scope exemption can be abused by a denial that also cites inside the same
  clause.
- Writer prose outside a files-opened section is still unscanned (as today); the spec does
  not widen scanning there because the disclosures themselves are prose.
- A marker alone inside backticks is allowed; it carries no value beyond the public name.

## Acceptance the wave-2 attack should apply to the fixed gate

1. On `.ufo/waves/round-29/w1` at `221cbd8f` with writer regex `^CaseA2(07|10)[a-d]\.md$`:
   `blind_violations=0`, `specimen_citations=1`, exit 0. (Measured 0/1 with this spec's
   rules; today the rev yields 20.)
2. Exit 1 with a named file and line for each synthetic line above, one per class
   (P1-P6), and for the bare-marker and negated-heading variants.
3. Still exit 1 on the strict-heading variant that lists the tool at `:3`, i.e. the fix
   must not trade detection for silence.
4. `--selftest` must include the FP corpus (these seven real headings and the criteria
   document's fenced block) and the leak corpus, or it is untested on the exact shapes
   that failed.
