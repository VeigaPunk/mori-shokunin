# C1 population adjudication — SentinelTranscripts

## Scope and result

The frozen population is pinned to measured revision `d005cdde0e009dea6c0cc29b37163de536528658`; per task, the hit windows and whole-file sweep were inspected at `29b0dc7`. The two population `line_sha256` values match hashes of the corresponding line bytes at `29b0dc7` with the terminal newline omitted. The frozen population contains two rows for this path, both class R9. Both are **redact** under `c1-policy.json`: this authored review is not lane tool code, a contract, a synthetic fixture, or a non-author file; neither observation qualifies for allow-a/b/c. Preserve neither occurrence-bearing content in the replacement.

## Evidence and method

- `jq '.hits[] | select(.path==".ufo/waves/round-17/build/SentinelTranscripts.md")' /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-18/frozen/c1-population.json` — exit 0; returned two rows.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 29b0dc7:.ufo/waves/round-17/build/SentinelTranscripts.md | sed -n '36,42p'` — exit 0; inspected the line-39 hit with three lines of context on either side.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 29b0dc7:.ufo/waves/round-17/build/SentinelTranscripts.md | sed -n '170,176p'` — exit 0; inspected the line-173 hit with three lines of context on either side.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 29b0dc7:.ufo/waves/round-17/build/SentinelTranscripts.md | nl -ba` — exit 0; reviewed the complete 218-line file for private context outside the regex metric.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 29b0dc7:.ufo/waves/round-17/build/SentinelTranscripts.md | sed -n '39p' | tr -d '\n' | sha256sum` and the corresponding `173p` command — exit 0; each digest matched its frozen population hash.
- No tools installed or updated.

## Redaction guidance

- **Line 39, R9, SHA-256 `661371a61bc744c5a35bb2ba8ccb5e50dfe587dac579679ae4942a1a0dfb93f8`: redact.** The observation includes session-derived record-type labels and their frequencies, rather than a permitted instruction or schema fixture. Replace it with a neutral redaction record retaining `decision=redact`, `count=1`, `class=R9`, and the original line SHA-256. Remove the session-derived labels and per-label counts.
- **Line 173, R9, SHA-256 `85df3409e543ee22d8feacff16a0c0d45d17d07375e34dd43bb486f7beb73ba3`: redact.** The finding lists session-record field names and asserts their presence on live terminal records; it is not an allowed tool/contract/fixture field-name location. Replace it with a neutral redaction record retaining `decision=redact`, `count=1`, `class=R9`, and the original line SHA-256. Remove the field-name list and the assertion connecting those fields to live records.

## Other private context missed by the frozen regex classes

These are qualitative reading-sweep observations, outside the frozen C1 metric; they do not add population rows. References identify only the lane path and line numbers, without copying the private material.

- `.ufo/waves/round-17/build/SentinelTranscripts.md:5,19` — a home-scoped live session-store root location and observed filesystem permission facts. R2 does not match the root-only path form used there.
- `.ufo/waves/round-17/build/SentinelTranscripts.md:31-32,196-201` — an identity for a timestamped, lane-resident transcript copy, plus a disclosure that a previous search surfaced content-bearing lines. The timestamp format is outside R1; the copy is outside R2's session-store path form. No actual transcript prose or record values are quoted in this report.
- `.ufo/waves/round-17/build/SentinelTranscripts.md:20-24,37-46` — aggregate live-corpus inventory and tail/record-shape measurements (file counts, sizes, type frequencies, parse and line-length facts). These are session-derived operational statistics, not raw excerpts.
- `.ufo/waves/round-17/build/SentinelTranscripts.md:47-51,54-66` — a live-record field inventory and aggregate terminal-field census. In particular, the error-message section contains literal value fragments copied from terminal records with frequencies; R9 does not cover those values. The strings are intentionally not reproduced here.
- `.ufo/waves/round-17/build/SentinelTranscripts.md:67-77,142-150` — retry-metadata shapes and counts, provider/model distribution facts, and session-tree stem/collision statistics derived from the live corpus. No provider or model names are present.

The full file contains no actual personal-document, operator-config, shell-history, or routing-table values. It contains no extended transcript prose; the terminal-value table includes field-value categories and literal error-message fragments copied from live records. Those strings are intentionally omitted here. A generic threat-model example is not treated as an observed private fact.

## Population rows

```json
[
  {
    "path": ".ufo/waves/round-17/build/SentinelTranscripts.md",
    "line": 39,
    "class": "R9",
    "line_sha256": "661371a61bc744c5a35bb2ba8ccb5e50dfe587dac579679ae4942a1a0dfb93f8",
    "decision": "redact",
    "reason": "Authored report observation containing session-derived labels and counts; not an allowed surface statement, tool/contract/fixture field name, or non-author file."
  },
  {
    "path": ".ufo/waves/round-17/build/SentinelTranscripts.md",
    "line": 173,
    "class": "R9",
    "line_sha256": "85df3409e543ee22d8feacff16a0c0d45d17d07375e34dd43bb486f7beb73ba3",
    "decision": "redact",
    "reason": "Authored report observation names live-record fields and asserts their presence; it is not an allowed tool/contract/fixture location or non-author file."
  }
]
```
