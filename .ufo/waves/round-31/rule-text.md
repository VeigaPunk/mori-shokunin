# Round-31 C2 rule text — the files-opened rule `tools/mori-blind-check.sh` implements (copied from `contract.md`)

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

