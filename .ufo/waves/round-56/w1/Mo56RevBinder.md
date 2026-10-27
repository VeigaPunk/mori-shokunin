# Mo56RevBinder — code review of tools/mori-vote-bind.py (round 56 w1)

Scope: review `tools/mori-vote-bind.py` at the frozen sha256
`8be1acdbb36cd68deba005e21a4a8679534ab5a5099a787aa9335d288dfa6bca` (working
tree, HEAD acc62f54) on the assigned axes: VOTE_RE anchoring, channel
selection edges, same-channel last-wins, single-vote agree counting, and the
`read_ledger` disposition cell for ENTAIL-shaped tables. Method: import the
module in a scratch harness plus CLI runs; every number below is executed
output, not reading.

Scratch: `/fast/scratch/hyaku/mori-r56/Mo56RevBinder/` (probes
`probe_extract.py`, `probe_tally.py`; removed after this report was written).
Tools installed/updated: none. `sha256sum tools/mori-vote-bind.py` at HEAD
equals the frozen PIN; `--selftest` prints `VOTE_BIND_SELFTEST pass=16
fail=0`, exit 0.

## Assigned axes, resolved

### Channel selection edge (JSON `null` / number / bool)

Executed matrix via `final_votes`:

| output | channel | votes |
|---|---|---|
| `null` | text | 0 |
| `null\nRECHECK a6e5226259c9 holds` | text | 1 |
| `42` | json | 0 |
| `42\nRECHECK a6e5226259c9 holds` | text | 1 |
| `true` | json | 0 |
| `{"a": 1}\nRECHECK a6e5226259c9 holds` | text | 1 |

`json.loads` accepts non-string scalars (`42`, `true`, `NaN`), so a bare
scalar document takes the json channel with a zero-scalar walk and reports
`channel=json` — cosmetic only, zero votes either way. `json.loads("null")`
returns `None`, indistinguishable from parse failure, so `null` falls into
the text channel where a literal `null` line cannot match VOTE_RE — also
harmless. Any trailing text after a JSON value makes `json.loads` fail, so
`{"a": 1}` followed by an unfenced vote line binds via the text channel
(the text path scans raw lines, never de-quoted JSON). No cross-channel
double counting. Correct behavior; the `ch=json` label on a bare scalar is
a cosmetic wrinkle at most.

### Last-wins across the SAME channel only — proof

`extract_votes` is single-path per call: if `json.loads(output)` returns
non-None it runs the scalar walk and `return`s (tool line 95); the text
loop below it is unreachable on that call. One output therefore produces
votes from exactly one channel, so a text vote and a JSON vote can never
co-exist in one seat's final `fv` map — "last-wins across the same channel
only" is not a restriction but the only reachable state. Cross-channel
conflict for one hash is additionally impossible across the tally because
`final_votes` is applied per voter output, and a hash's row aggregates
`v["word"]` per voter, not per channel. Verified: `{"a": 1}` + unfenced
trailing vote binds via text (the doc is not JSON-parseable as a whole);
`{"a": 1}` + fenced trailing vote binds nothing.

### VOTE_RE anchoring (word charset, rest capture, tabs, trailing space)

Executed: tabs between fields bind (`RECHECK\t<h>\tholds` → word `holds`);
tabs inside rest are captured; trailing spaces strip cleanly. The
fail-closed edges: a disposition glued to punctuation
(`RECHECK <h> holds.`, `RECHECK <h> (holds)`) binds nothing — silently
dropped, not mis-bound; a word starting with a digit or `-` binds nothing;
uppercase or 11/13-hex hashes bind nothing. Two-space gap before rest
leaves one leading space inside `rest` (`rest=' two-spaces'`, cosmetic).
The one real shape gap is multi-line scalars — see Findings.

### Single-vote agree counting — intended, verified

`tally`: `len(words)==1` → `single += 1` and `agree += 1` iff the lone word
equals the ledger disposition. Executed: one voter, want `holds`, votes
`holds` → `{agree: 1, single: 1}`. This is the contract's "surfaces
single-voted rows honestly instead of zeroing the arm" (contract.md
carried item; entry §"Measured on the round-55 bytes"). `agree` is "every
voter on the row agreed with the ledger, and at least one voted" — not a
quorum — and the TALLY line exposes `single`/`zero`/`dissent` so the
consumer can subtract. Correct as designed.

### read_ledger cell index for ENTAIL tables — dead code

`read_ledger` only assigns `word` under `if verb == "RECHECK"` (line 152);
the ENTAIL branch is absent while the docstring claims "ENTAIL tables
share the same trailing shape here". Executed on a constructed ENTAIL
table with `entailed` in cell 6 and an `ENTAIL <h> entailed` voter:
`tally(verb="ENTAIL")` → `rows=0` (dict empty before counting). An
`ENTAIL ... --verb ENTAIL` tally silently reports an empty ledger. See
Findings.

The frozen r55 ledger `corpus/knowledge/kernel-v7.3-recheck-r55.md` has
7 columns with disposition at index 6 (`| hash | entry | pointer | v7.3
source | v7.3 lines | status | disposition |`), so cell 6 is right for
*that* table; the index is positional, not named — a table with an extra
column before disposition reads the wrong cell (exhibited below).

## Findings

- **MED — multi-line vote scalar silently loses or voids votes**
  (`tools/mori-vote-bind.py:64,91`). VOTE_RE is `^...$`-anchored with
  `.` not matching `\n`: in the JSON channel a *single scalar* holding
  multiple vote lines binds only the first line when the scalar has
  exactly two lines — the second line is swallowed into `rest` —
  and binds zero votes when the scalar has three or more lines.
  Executed:
  `{"v": "RECHECK a6e5226259c9 holds\nRECHECK 0124918d278a stale"}` →
  `votes=1, rest='RECHECK 0124918d278a stale'` (second vote swallowed);
  `{"v": "RECHECK a6e5226259c9 holds\nmid\nRECHECK 0124918d278a stale"}`
  → `votes=0`. A seat that packs its vote block into one JSON string
  field (natural shape: `"notes": "RECHECK a.. holds\nRECHECK b..
  stale"`) loses votes with no signal. Named limit + routed item for
  round 57: split each scalar on `\n` before matching, or document the
  one-vote-per-scalar rule in the entry's Limits section.

- **MED — `tally --verb ENTAIL` silently reports an empty ledger**
  (`tools/mori-vote-bind.py:152`). `read_ledger` assigns a disposition
  only for `verb == "RECHECK"`; the documented "ENTAIL tables share the
  same trailing shape" branch does not exist. Exhibiting input:
  1-row ENTAIL ledger (disposition `entailed` in cell 6) + one
  `ENTAIL <h> entailed` voter → `rows=0 agree=0 double=0 single=0
  zero=0 dissent=0 bound_voters=1`. The verb is accepted by VOTE_RE,
  the extract subcommand and `--verb`, so a caller gets `TALLY rows=0`
  with exit 0 — a silent wrong answer on a documented path. Routed
  item: implement the ENTAIL cell rule or reject `--verb ENTAIL` at
  setup with exit 2. Does not affect C2's frozen RECHECK arm.

- **LOW — `--min` / `min_votes` is dead metadata** (`tools/mori-vote-bind.py:161,202,418`).
  `min_votes` is echoed in the result dict (`'min': 5` observed) but
  never gates `agree`/`single`: `min_votes=2` and `min_votes=5` on a
  1-voter-1-row tally both print `agree=1 single=1`. A reader of
  `--min N` would expect it to withhold `agree` below quorum; either
  apply it or drop the flag. Cosmetic for C2 (counter greps the line,
  which is correct), but the printed `min` field invites a wrong
  reading.

- **LOW — `read_ledger` positional cell + duplicate-hash collapse**
  (`tools/mori-vote-bind.py:146-155`). (a) disposition is `cells[6]`
  unconditionally: an 8-column ledger (`... | status | confidence |
  disposition |`) yields `want='high'` → unanimous `holds` voters tally
  `agree=0` with no signal (exhibited). The `--disposition-cols N` flag
  in the usage docstring (line 45) is not implemented in the arg parser
  — running it exits 2 (argparse error). (b) duplicate backticked-hash
  rows collapse last-wins into `disp`, and `rows=` counts unique
  hashes, not table rows (exhibited: `holds` then `stale` on one hash →
  `rows=1`, counted against `stale`). (c) a hash cell without backticks
  is skipped by the row regex → `rows=0` (exhibited). All fail-closed;
  routed item: parse the header row to locate the disposition column by
  name.

- **LOW — text-channel `\n`-unescape and fence toggling side effects**
  (`tools/mori-vote-bind.py:97-99`). `output.replace("\\n", "\n")`
  unescapes literal backslash-n before line scanning: `intro\nRECHECK
  <h> holds` (as raw bytes) binds — intended resilience — but also
  splits a literal `\n` inside `rest` (`see a\nb` → `rest='see a'`,
  vote still binds; cosmetic) and an escaped `~~~`/``` marker toggles
  fence state, so `x\n```\nRECHECK <h> holds` binds nothing (exhibited:
  `votes=0`). Separately, a plain line starting with `~~~` — valid
  Markdown thematic break — opens a never-closed fence and swallows all
  later votes in a text output (exhibited: `votes=0`; blank-line
  separators are safe). Both are fail-closed; routed item: require the
  fence marker to *end* the line (`^\s*(```|~~~)\s*$`) or name the
  constraint.

- **LOW — dict keys and `json` label cosmetics**
  (`tools/mori-vote-bind.py:74-76,89`). `_walk_strings` visits dict
  values, not keys: `{"RECHECK <h> holds": true}` → `votes=0`
  (exhibited). And a bare JSON scalar doc (`42`, `true`) reports
  `channel=json` though no string scalars exist — label only, no votes
  lost. Named-limit material, not a defect.

Residual risk: the binder's contract-critical arms (frozen-grammar
binding on the r55 bytes, selftest 16/0, pin match at HEAD) all check
out under direct execution; findings above are edge-shape losses that
fail closed (votes dropped, never fabricated) except the ENTAIL tally
which is a silent no-op on a documented path. Verification gaps: I did
not exercise the `extract` CLI on binary/non-UTF8 output bytes beyond
the surrogateescape read path, and did not diff the tool against the
round-55 substring counter it replaces beyond the frozen receipts.
