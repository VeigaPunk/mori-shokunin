# Mo56ScoutR55Shapes — round-55 voter output shapes vs the dual-shape binder

Seat assignment: classify the captured `output` of every seat in
`.ufo/waves/round-55/w1-results.json` into shapes (JSON object with vote_lines /
JSON string doc / plain text with unfenced lines / fenced / mixed / empty); for
each of the 16 Mo55Rc seats name the binding channel of
`tools/mori-vote-bind.py` and the bound vote count; answer "binds neither
channel?" and "binds but should not?". Wave carries no vote items; nothing in
this report is a vote line.

Tooling: no installs or upgrades were needed (python3 stdlib only; no pacman,
no network).

## Method

- Imported the frozen binder `tools/mori-vote-bind.py` by path and ran its real
  `final_votes()` against each of the 64 captured outputs, then cross-checked
  with the CLI `tally` subcommand over the committed round-55 ledger
  `corpus/knowledge/kernel-v7.3-recheck-r55.md` and the committed
  `.ufo/waves/round-55/w1-results.json` bytes.
- Shape classification: `json.loads()` on the captured output decides the JSON
  channel vs the text channel exactly as the tool does; within text, fence
  state per line (`FENCE_RE`) decides fenced vs unfenced.
- Scratch: `/fast/scratch/hyaku/mori-r56/Mo56ScoutR55Shapes/` (removed after
  the report was written). `TMPDIR` pointed there for the selftest.

## Tool identity and liveness checks (frozen claims C2)

```
$ sha256sum tools/mori-vote-bind.py
8be1acdbb36cd68deba005e21a4a8679534ab5a5099a787aa9335d288dfa6bca
$ python3 tools/mori-vote-bind.py --selftest
VOTE_BIND_SELFTEST pass=16 fail=0        exit=0
$ python3 tools/mori-vote-bind.py tally --ledger corpus/knowledge/kernel-v7.3-recheck-r55.md \
    --results .ufo/waves/round-55/w1-results.json --verb RECHECK \
    --voter Mo55Rc01 --voter Mo55Rc02 ... --voter Mo55Rc16
TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15   exit=0
```

The sha256 equals the PIN recorded in `.ufo/waves/round-56/count-c2.py`; the
CLI tally over the 16 Mo55Rc voters reproduces byte-for-byte the frozen line in
`.ufo/waves/round-56/evidence/tally-r55.txt`. Over the full 64-seat roster the
same call gives `voters=64 bound_voters=15` — the 48 non-Rc seats bind nothing.

## Shape classification — the 16 Mo55Rc seats

All 16 outputs are non-empty. 15 parse as JSON objects (JSON channel); 1 is
plain text (text channel). No JSON string doc, no fenced-only, no mixed, no
empty shape appears among the 16.

| seat | shape | vote-list key | channel | bound votes |
|------|-------|---------------|---------|-------------|
| Mo55Rc01 | JSON object w/ vote_lines | `vote_lines` | json | 10 |
| Mo55Rc02 | JSON object w/ vote_lines | `votes` | json | 10 |
| Mo55Rc03 | JSON object w/ vote_lines | `votes` | json | 10 |
| Mo55Rc04 | JSON object w/ vote_lines | `votes` | json | 10 |
| Mo55Rc05 | JSON object w/ vote_lines | `votes` | json | 10 |
| Mo55Rc06 | JSON object w/ vote_lines | `final_vote_lines` | json | 10 |
| Mo55Rc07 | JSON object w/ vote_lines | `votes` | json | 10 |
| Mo55Rc08 | JSON object w/ vote_lines | `final_votes` | json | 10 |
| Mo55Rc09 | JSON object w/ vote_lines | `votes` | json | 10 |
| Mo55Rc10 | JSON object w/ vote_lines | `final_vote_lines` | json | 10 |
| Mo55Rc11 | JSON object w/ vote_lines | `votes` | json | 10 |
| Mo55Rc12 | JSON object w/ vote_lines | `votes` | json | 10 |
| Mo55Rc13 | JSON object w/ vote_lines | `final_vote_lines` | json | 10 |
| Mo55Rc14 | plain text, unfenced lines, none vote-grammar | — | text | 0 |
| Mo55Rc15 | JSON object w/ vote_lines | `vote_lines` | json | 8 |
| Mo55Rc16 | JSON object w/ vote_lines | `voteLines` | json | 8 |

Bound-vote total: 13×10 + 2×8 + 0 = 146, which equals the tally's vote mass
(68 double rows × 2 + 10 single rows × 1 = 146); every bound word is `holds`,
zero dissent. The 15 JSON seats bind through the document-order string-scalar
walk — the key name is irrelevant to the binder, which is why all five distinct
key spellings bind identically.

## Channel answers

- Text-channel fallback live check: simulating a pure text-channel read (the
  round-55 C1 counter's behavior) on the 15 JSON seats yields 0 anchored
  unfenced vote lines per seat — every vote line sits inside a quoted JSON
  scalar. This is exactly the frozen contrast in
  `.ufo/waves/round-56/evidence/c2-old-counter-voted0.txt` (`voted=0` at the
  entering tip 5b295eee on the same bytes).
- Shape binding NEITHER channel: none as a shape class. The empty-output shape
  would (channel `none`, no votes) but no Mo55Rc seat emitted empty output.
  The only zero-binding seat is Mo55Rc14: its truncated plain-text fragment
  selects the text channel and carries no vote-grammar line, so 0 votes bind.
  Per the tool docstring this is intended — the tally reports its rows as
  single-vote rows (10 of the 78), never zeros.
- Shape binding but should not: none observed. Five seats (Mo55Rc02, Mo55Rc08,
  Mo55Rc13, Mo55Rc15, Mo55Rc16) carry exactly one bare prose mention of the
  word RECHECK each (11 vs 10, or 9 vs 8, literal occurrences vs hash-bearing
  occurrences); the anchored grammar plus the overclaim guard reject all five.
  Bound counts equal each seat's declared assigned-row count (10 or 8), and the
  48 non-voter seats contribute zero bound votes over the full roster.

## Findings

- MED — `tools/mori-vote-bind.py` text-channel binding path (plain-text
  unfenced vote lines) has no live exerciser among round-55's 16 voters: all 15
  binding seats used the JSON channel, and the one text-channel seat (Mo55Rc14)
  bound zero. Its coverage rests on the frozen selftest cases
  (`t_plain_binds`, `t_malformed_json_falls_back_to_text`). Routed item for
  round 57: exercise the text channel against live wave bytes.
- LOW — Mo55Rc14's captured output is a mid-work plain-text fragment (no
  report, no vote surface); the binder's honest single-vote reporting depends
  on seats like this being visibly vote-less in both channels. Concern:
  `.ufo/waves/round-55/w1-results.json` result record Mo55Rc14 (truncated
  fragment, no vote lines).
- LOW — The overclaim guard is load-bearing on live data: 5 of 16 voter outputs
  embed a bare prose RECHECK token that a substring binder would have
  miscounted. Concern: `tools/mori-vote-bind.py` `VOTE_RE` anchoring.
- INFO — No HIGH findings; both C2 surface claims (dual-shape binding, re-bound
  round-55 tally) verified against the committed bytes with the pinned tool.

Report: .ufo/waves/round-56/w1/Mo56ScoutR55Shapes.md
