# mori round 31 — claim contract (attempt 1, L1 MoriR31)

Entering tip `a12c68ae81257fb6f918bb165bcb39c73f82d212` (round 30 closed `rejected-honest-stop`,
`corpus/lessons/round-30-verifier-spotcheck.md`). Written before any round-31 entry, source row, tool code or seat
output. Targets, not results. A declared claim is never withdrawn, narrowed, re-scaled or amended after data; a miss is
reported as a miss. Each predicate below is the same sentence here, in its counter's docstring and code, and in the
receipt label (`C1=met` / `C2=met`).

## Why these two claims

- Lowest-scoring active axes: depth, freshness, calibration (5 each, `SCORECARD.md:12-14`). C1 works depth.
- C1 surface: `SKILL.md` and `corpus/knowledge/` gain a sourced decision table on FR5 ground (watchdog daemon identity
  and degraded-pgrep visibility, `PROVINCE.md:48`, `corpus/README.md:338`), where no knowledge entry and no SOURCES row
  on pgrep matching, `/proc/<pid>/comm` truncation or `/proc/<pid>/stat` start time exists at the entering tip
  (`corpus/knowledge/audit-r11.md:201` names the open false-positive class only). The command that shows it unmoved:
  `count-c1.py a12c68ae` → `entry=absent`, `C1=unmet`.
- C2 surface: a new runnable lane gate `tools/mori-blind-check.sh`, the round-30 blindness gate with routed D1 fixed
  (`corpus/lessons/round-30-verifier-spotcheck.md:176-178`): it parsed prose after the files-opened list as an entry
  (`CaseR30a.md:105`), reported one forbidden hit per file, and missed label-form lists (`CaseA210c`). It works
  operability (7). The round-30 gate bytes stay as round-30 evidence; nothing in `.ufo/waves/round-30/` changes.
  The command that shows it unmoved: `count-c2.py a12c68ae` → `tool=absent`, `C2=unmet`.
- Causally separable: C1 touches only the entry, `SKILL.md` lines tagged `Round31`, `corpus/SOURCES.md` rows S161+,
  their Gate rows in `corpus/lessons/round-31.md` and copies under `corpus/evidence/sources-r31/`. C2 touches only
  `tools/mori-blind-check.sh`. Neither counter reads the other claim's files.
- Not re-claimed: the round-29/30 disputed-shape blind-case freeze. C2 is the gate a later freeze would depend on.
- Sourced claim: C1.

## C1 — depth (5): how a pid probe can and cannot establish that the fleet watchdog is alive

Predicate P-C1: C1=met iff at <lane-rev> the entry corpus/knowledge/watchdog-identity-r31.md carries source:,
verified-at: and recheck: lines and exactly one table whose header holds the cells observation, reading, verdict and
sources, with at least 8 data rows, every row naming at least one S### that is a corpus/SOURCES.md row; at least 6 rows
cite an id S161 or higher and at least 4 such ids are cited; every such id has exactly one SOURCES.md row, exactly one
admit Gate row in corpus/lessons/round-31.md with an https URL, a 64-hex sha256 and at least one quote of at most 25
words, and a committed copy corpus/evidence/sources-r31/S###.src whose sha256 equals the Gate sha256 and which contains
every quote; the URL fetched at measurement time hashes to the same sha256; and SKILL.md has at least 4 lines naming
both Round31 and the entry path.

Counting command (exit 0 met, 1 unmet, 2 bad revision):

```sh
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-31/count-c1.py <lane-rev>
```

Gate quote syntax the counter reads: `` `file:L-M` (N words): "quote" `` inside the Gate row, where `\"`, `\|` and
`\\` stand for `"`, `|` and `\`; the quote is matched with whitespace runs collapsed. One URL per new id.

Controls, scored under the frozen counter and committed before any seat runs (`evidence/c1-controls.txt`):
do-nothing (the entering tip) and two shortcuts in a sandbox clone — (a) a sourceless table citing only pre-existing
ids; (b) a table citing four fabricated new rows whose Gate lines, SOURCES rows and copies are mutually consistent but
whose copies are not the upstream bytes. Each must print `C1=unmet`; if one meets, the counter is wrong and is fixed
before data.

Uncounted residual for wave-2/residual non-authors: whether each row's reading follows from its cited quote.
Score policy: depth stays 5 unless an admitted closure states the move.

## C2 — operability (7): the blindness gate parses the files-opened list and reports every forbidden entry

Predicate P-C2: C2=met iff tools/mori-blind-check.sh exists at <lane-rev>, and run on the 16 frozen fixtures of
.ufo/waves/round-31/c2-fixtures.json (committed under random brief names in a /tmp sandbox repo) it prints scanned=16,
blind_violations equal to its hit-line count, exit 1, no hit line outside the 16 briefs, and for every fixture exactly
the expected set of (line, rule) hits (exact=16/16).

Counting command (exit 0 met, 1 unmet, 2 bad revision or fixtures not the frozen sha256
`1442c14e963bf77df34774015dff7ee73a9738d49b3911d26b4e3b96f48e0b31`):

```sh
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-31/count-c2.py <lane-rev>
```

Tool interface the fixtures assume: `tools/mori-blind-check.sh <lane-rev> <wave-report-dir> <writer-name-regex>
<allow-file>`, run inside the repo; output `scanned=N`, `blind_violations=M`, then one `path:line:rule` line per hit;
exit 0 no hit, 1 hits, 2 usage or input error. The allow file holds one bash glob per line; `{report}` in a line stands
for the brief's basename without `.md`; `file://` is stripped from a candidate before matching.

Files-opened rule (the rule the fixtures encode; `rule-text.md` in this directory carries it for seats):

1. A block opens at a Markdown heading (any level) whose text contains `files opened` or `opened files`
   (case-insensitive), or at a line whose trimmed text starts with `Files opened:` or `Opened files:`
   (case-insensitive).
2. Entries are the following lines that start (after optional indentation) with `- `, `* `, `+ `, `N. ` or `N) `, or
   with `|` (a table row); a table's separator row (only `|`, `-`, `:` and spaces) and the row directly above it are
   not entries. Blank lines inside the block are skipped.
3. The block closes at the first heading or at the first other non-blank line.
4. An entry's candidates are its tokens, stripped of wrapping backticks, quotes and brackets, trailing `,;.` and a
   `:L` / `:L-M` suffix, that contain `://`, `/` or `.` or equal `LOG.md`, `SCORECARD.md`, `SKILL.md` or
   `PROVINCE.md`. An entry with no candidate, or with a candidate no allow line matches, is one
   `writer-forbidden-opened-path` hit at its own line.
5. A brief with no entry in any block is one `writer-missing-files-opened-list` hit at line 1.
6. The `writer-tool-source-citation` and `writer-tool-run-output` detectors are the round-30 gate's, unchanged.

Controls, scored under the frozen counter with `--tool-file` and committed before any seat runs
(`evidence/c2-controls.txt`): do-nothing — the round-30 gate with only its round-30 allowlist function replaced by
the allow-file reader (no parser change); shortcut 1 — a script that greps list-marker lines anywhere and flags any
path not matching the allow file; shortcut 2 — a script that prints canned hits keyed on fixture brief names
(`CaseF01.md`…). Each must print `C2=unmet`.

Score policy: operability stays 7 unless an admitted closure states the move.

## Repairs routed by the round-30 closure (not claims; each lands with a LOG entry)

D1 is C2's substance (the round-30 gate stays as evidence; the lane tool supersedes it, its self-test drops the locked-in
`CaseA210c|writer-missing-files-opened-list` false positive). D2 mistake row citing QUALITY 25 (A1's silent loosening;
A3 is no precedent). D3 a new QUALITY row superseding 93 by name, and QUALITY 92's unmet state recorded. D4 the entry
`earlyoom-invocation-scope-r30.md` "reports its version" corrected by appended text at every mention, and the S159/S120
`Restart=always` overlap handled. D5 the coverage-map row for that entry in `corpus/README.md`. D6 the X1/X2 dry-run
verdict flips pinned as cases in a new fixture file (no existing fixture file changes). D7 a LOG entry for `713be294`.
D8 a SCORECARD correction for the round-30 C1 counts and the stale C2 condition-4 parenthetical. D9 noted.
