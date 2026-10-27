# Mo56ExecBinderSelftest — round 56 w1, seat report

Seat scope (as assigned): falsify the C2 vote-binding claim by (a) running
`tools/mori-vote-bind.py --selftest` three times from the freeze-tip archive
`8be2717b0809281d07dffe83dad424a4859e0747`, and (b) running `extract` over one
synthetic plain-text output and one JSON-wrapped output written in scratch, and
pasting the VOTE lines.

Lane: mori-shokunin. Read-only seat: detection and report only. No tool was
installed or upgraded (no pacman, no uv, no downloads) — nothing in this
assignment needed a tool the host did not already have (`python3` only), so the
operator tooling directive of 2026-10-19 produced no install record.

Scratch (all under `/fast/scratch/hyaku/mori-r56/Mo56ExecBinderSelftest/`,
removed at the end of this seat):
`tree/` (archive extract of the freeze tip), `fixtures/` (the two synthetic
outputs), `probe/` (falsification probes), `ind/` (committed round-55 bytes
materialized read-only via `git show`), `tmp/` (TMPDIR).

Base of every command below: `/fast/scratch/hyaku/mori-r56/Mo56ExecBinderSelftest/tree`
(the extracted archive), unless the command says otherwise. The archive was
produced read-only with
`git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive 8be2717b… | tar -x -C <scratch>`.
No clone, no mirror, no fixture repo, no git mutation of any kind.

---

## 1. Assigned check A — `--selftest` three times

```
$ for i in 1 2 3; do out=$(python3 tools/mori-vote-bind.py --selftest 2>&1); ec=$?; echo "=== RUN $i === exit=$ec"; echo "$out"; done
=== RUN 1 === exit=0
VOTE_BIND_SELFTEST pass=16 fail=0
=== RUN 2 === exit=0
VOTE_BIND_SELFTEST pass=16 fail=0
=== RUN 3 === exit=0
VOTE_BIND_SELFTEST pass=16 fail=0
```

All three runs printed `VOTE_BIND_SELFTEST pass=16 fail=0` and exited 0. The
literal string asserted by the frozen counter (`EXPECT_SELFTEST` at
`.ufo/waves/round-56/count-c2.py:43`) is matched exactly.

Corroborating determinism check (the selftest and the tally both iterate sets,
so hash-order sensitivity was a plausible falsification target):

```
$ for seed in 0 1 42 12345 999983; do PYTHONHASHSEED=$seed python3 tools/mori-vote-bind.py --selftest; done
VOTE_BIND_SELFTEST pass=16 fail=0      (seed 0)
VOTE_BIND_SELFTEST pass=16 fail=0      (seed 1)
VOTE_BIND_SELFTEST pass=16 fail=0      (seed 42)
VOTE_BIND_SELFTEST pass=16 fail=0      (seed 12345)
VOTE_BIND_SELFTEST pass=16 fail=0      (seed 999983)
```

Identical under five hash seeds. The 16 case names actually registered (read
out of the module, not inferred from the printed count) are: `t_plain_binds`,
`t_json_array_binds`, `t_json_nested_binds`, `t_json_string_doc_binds`,
`t_fenced_text_ignored`, `t_fenced_scalar_ignored`,
`t_json_prose_substring_rejected`, `t_junk_rejected`,
`t_hash_len_drift_rejected`, `t_last_wins_text`, `t_last_wins_json`,
`t_dissent_detected`, `t_entailed_verb_parsed`,
`t_malformed_json_falls_back_to_text`, `t_tally_mini`,
`t_roster_and_name_filter` — 16, matching `pass=16`. The `@case` decorator
count in the file is also 16.

**A: CONFIRMED.** The selftest is deterministic, exits 0, and prints the frozen
expected string.

## 2. Assigned check B — `extract` over one plain-text and one JSON-wrapped output

Both synthetic outputs were written by this seat into
`/fast/scratch/hyaku/mori-r56/Mo56ExecBinderSelftest/fixtures/`.

### 2a. Plain-text output — `fixtures/plain-seat-output.md`

Contents (deliberately mixed): a prose sentence containing a vote token, two
agreeing/disagreeing plain vote lines, an `ENTAIL` line, an `ENTAIL` line with a
rest, a repeat of an earlier hash with a different word (last-write-wins), a
fenced block containing a vote line (must be ignored), a 13-hex-digit hash
(length drift, must be rejected), and a 12-hex-plus-suffix hash (must be
rejected).

```
$ python3 tools/mori-vote-bind.py extract /fast/scratch/hyaku/mori-r56/Mo56ExecBinderSelftest/fixtures/plain-seat-output.md
VOTE ENTAIL 909839af93ac overclaim text 
VOTE RECHECK 0124918d278a stale text 
VOTE RECHECK 7b2d297eec60 entailed text extra reason text
VOTE RECHECK a6e5226259c9 stale text 
exit=0
```

### 2b. JSON-wrapped output — `fixtures/json-seat-output.json`

Contents: a `findings` string containing a vote token in prose, a `vote_lines`
array with two votes, a nested `nested.deep[0].c` vote, a fenced scalar, a
`trailing` scalar repeating an earlier hash with a different word, and a
13-hex-digit note.

```
$ python3 tools/mori-vote-bind.py extract /fast/scratch/hyaku/mori-r56/Mo56ExecBinderSelftest/fixtures/json-seat-output.json
VOTE ENTAIL 7b2d297eec60 entailed json — unit
VOTE RECHECK 0124918d278a stale json 
VOTE RECHECK a6e5226259c9 stale json 
exit=0
```

**B: CONFIRMED.** Both shapes bind. The channel tag differs as designed
(`text` vs `json`), the prose substring did not bind, the fenced scalar did not
bind, the 13-hex drift did not bind, and last-write-wins is visible in both
channels (`a6e5226259c9` resolved to `stale`, the later word, in both).

---

## 3. Independent re-derivation of the frozen C2 numbers

Not asked for, but the C2 claim is only falsifiable against its own numbers, so
the frozen receipts were re-derived from the committed bytes rather than trusted.

Tool pin (the counter's `PIN` at `count-c2.py:46`):

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 8be2717b:tools/mori-vote-bind.py | sha256sum
8be1acdbb36cd68deba005e21a4a8679534ab5a5099a787aa9335d288dfa6bca  -
$ grep -n '^PIN' .ufo/waves/round-56/count-c2.py
46:PIN = "8be1acdbb36cd68deba005e21a4a8679534ab5a5099a787aa9335d288dfa6bca"
```

Same digest at `c419fe6d`, `6ced9da9`, `3f494b49`, `8be2717b` and in the working
tree — the pin is stable across every commit that touches the tool.

The frozen tally, re-derived by hand over the committed round-55 ledger and
results (not by running the counter):

```
$ python3 tools/mori-vote-bind.py tally --ledger ind/ledger.md --results ind/results.json --verb RECHECK --voter Mo55Rc01 … --voter Mo55Rc16
TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15
exit=0
```

Byte-identical to the frozen receipt `.ufo/waves/round-56/evidence/tally-r55.txt`.

The do-nothing control (every voter output replaced with junk prose):

```
$ python3 tools/mori-vote-bind.py tally --ledger ind/ledger.md --results ind/junk.json --verb RECHECK --voter Mo55Rc01 … --voter Mo55Rc16
TALLY rows=78 agree=0 double=0 single=0 zero=78 dissent=0 voters=16 bound_voters=0
exit=0
```

`zero=78` as the contract requires. The junk control is a genuine discriminator:
the ledger still yields 78 rows, so `zero=78` is caused by the absence of votes,
not by an empty ledger.

The contrast arm (frozen round-55 C1 counter over the same committed bytes):

```
$ python3 .ufo/waves/round-55/count-c1.py 8be2717b0809281d07dffe83dad424a4859e0747
C1=unmet scope=78 rows=78 matched=78 status_ok=78 line_ok=78 source_rows=ok pins=ok provenance=ok same=69 moved=7 changed=2 broken=0 holds=78 stale=0 voted=0 dissent=0 rev=8be2717b… failed=votes
exit=1
```

`voted=0` on the same bytes on which the new binder reports `agree=78` — the
contrast is real, not an artifact of which revision was checked.

The frozen counter itself, run read-only against the lane repo at both the
receipt-stamped revision and the freeze tip:

```
$ python3 .ufo/waves/round-56/count-c2.py 3f494b49cde612d929e82887a48e1660c022c359
C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=3f494b49…   exit=0
$ python3 .ufo/waves/round-56/count-c2.py 8be2717b0809281d07dffe83dad424a4859e0747
C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=8be2717b…   exit=0
```

`count-c2.py --selftest` → `C2_COUNTER_SELFTEST pass=1 fail=0` exit 0;
`count-c1.py --selftest` → `C1_COUNTER_SELFTEST pass=1 fail=0` exit 0.

**C2 as frozen is not falsified.** Every number in the contract reproduces from
the committed bytes.

---

## 4. Falsification probes — where the binder is weaker than its own docstring

The C2 counters, predicates, controls and kill rules are frozen and are **not**
proposed for change here. These are named limits with routed items for round 57.

### 4.1 MED — `extract` on a results file sees nothing, while `tally` over the same file binds 15 voters

The tool's own docstring names the binding unit as "the orchestrator-captured
final output (the `output` field of a seat's result record in a wave's
*-results.json)". The `tally` subcommand honours that: `read_results`
(`tools/mori-vote-bind.py:119-133`) pulls `r["output"]` out of each record and
`final_votes` is then applied to that string alone. The `extract` subcommand
(`tools/mori-vote-bind.py:423-435`) instead reads the whole file and hands the
whole file to `final_votes`, so the per-record `output` values are never
re-parsed.

Against the real committed round-55 results file:

```
$ python3 tools/mori-vote-bind.py extract ind/results.json | wc -l
0
$ python3 tools/mori-vote-bind.py extract --verb ENTAIL ind/results.json | wc -l
0
$ python3 tools/mori-vote-bind.py tally --ledger ind/ledger.md --results ind/results.json --verb RECHECK --voter Mo55Rc01 … --voter Mo55Rc16
TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15
```

Mechanism, confirmed by walking the document by hand: the results file is a JSON
document whose `results[i].output` values are JSON *strings* containing escaped
newlines. `_walk_strings` on the whole file sees 194 scalars, **none** of which
starts with a vote verb, because the vote text sits inside a larger JSON string
and the JSON channel only binds a scalar whose *stripped content* matches the
grammar anchored at the start. Re-parsing one `output` value in isolation does
expose the votes:

```
$ python3 tools/mori-vote-bind.py extract ind/output-00.json
VOTE RECHECK 1c11a3f36bf3 holds json 
VOTE RECHECK 441f0b4099e5 holds json 
… (10 VOTE lines)
exit=0
```

This is a real footgun for a future operator who wants to audit votes with
`extract` on the natural input file: they get exit 0 and zero VOTE lines and may
wrongly conclude the binder is broken or that the wave carried no votes. It did
not affect the frozen C2 numbers, because the counter uses `tally`, not
`extract`. Named limit; routed to round 57 (an `extract --results` mode, or a
docstring note that `extract` takes one seat output, not a results file).

### 4.2 MED — a JSON-wrapped output whose vote sits inside a multi-line field is silently dropped, while the identical plain-text output binds

The JSON channel binds a scalar only if the scalar's *stripped content* starts
with the verb. A seat that returns `{"report": "## Findings\n\nRECHECK <hash> holds\n…"}`
therefore binds nothing, while the same text unwrapped binds:

```
$ python3 tools/mori-vote-bind.py tally --ledger probe/n1-ledger.md --results probe/n1.json --verb RECHECK
TALLY rows=1 agree=0 double=0 single=0 zero=1 dissent=0 voters=1 bound_voters=0    # JSON-wrapped, vote inside a report field
$ python3 tools/mori-vote-bind.py tally --ledger probe/n1-ledger.md --results probe/n2.json --verb RECHECK
TALLY rows=1 agree=1 double=0 single=1 zero=0 dissent=0 voters=1 bound_voters=1    # same content as plain text
$ python3 tools/mori-vote-bind.py tally --ledger probe/n1-ledger.md --results probe/n3.json --verb RECHECK
TALLY rows=1 agree=1 double=0 single=1 zero=0 dissent=0 voters=1 bound_voters=1    # JSON with a dedicated vote_lines array
```

The third case is why the frozen round-55 tally is unaffected: the fifteen
reporting voters all emitted a dedicated `vote_lines` / `final_vote_lines` /
`votes` array of single-line scalars, which is the shape the JSON channel
handles. Measured over the real round-55 bytes: 63 of 64 captured outputs are
JSON documents, all bound votes live in dedicated vote-list keys
(`vote_lines` 64, `votes` 172, `final_vote_lines` 122, `final_votes` 10,
`voteLines` 8, `finalVoteLines` 23, `entail_votes` 23), and there are **zero**
multi-line scalars whose vote line is not at the scalar's start, and **zero**
vote-shaped lines that fail to bind. The frozen number is sound; the shape
dependency is the named limit. A future seat that puts its vote in a prose field
of a JSON document would be counted as a zero row — the exact class of failure
round 55 was raised to fix, in a narrower form. Routed to round 57.

### 4.3 MED — `tally --min N` is inert; the threshold is hardcoded

The CLI accepts `--min` (`tools/mori-vote-bind.py:414`) and passes it through as
`min_votes` (`tools/mori-vote-bind.py:438`), but `min_votes` is only echoed into
the returned dict (`tools/mori-vote-bind.py:202`); the row classification is
hardcoded at `len(words) == 1` / `else` (`tools/mori-vote-bind.py:184-192`).

```
$ python3 tools/mori-vote-bind.py tally --ledger ind/ledger.md --results ind/results.json --verb RECHECK --min 1
TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=64 bound_voters=15
$ python3 tools/mori-vote-bind.py tally --ledger ind/ledger.md --results ind/results.json --verb RECHECK --min 99
TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=64 bound_voters=15
identical=YES
```

(The `voters=64` here is the roster default `sorted(outputs)` — all 64 seats in
the results file — because no `--voter` was passed; the frozen counter passes
all 16 explicitly, which is why it prints `voters=16`.)

An operator cannot use `--min` to require 3 or more voters per row. The contract
notes the dispatch-coverage validator (≥2 voters per scoped row) "stays planned"
— this is the concrete reason it could not be enabled. Routed to round 57.

### 4.4 LOW — `--disposition-cols N` is documented in the tool's usage but not implemented

```
$ python3 tools/mori-vote-bind.py tally --ledger ind/ledger.md --results ind/results.json --verb RECHECK --disposition-cols 7
usage: mori-vote-bind.py [-h] [--selftest] {extract,tally} …
mori-vote-bind.py: error: unrecognized arguments: --disposition-cols 7
exit=2
```

The docstring usage block at `tools/mori-vote-bind.py:45` advertises
`[--disposition-cols N]`, but no such argparse option exists
(`tools/mori-vote-bind.py:413-415` defines only `--ledger`, `--results`,
`--verb`, `--voter`, `--min`). Exit 2 with an argparse error. A docstring that
advertises a flag the parser rejects. Routed to round 57 (fix the docstring or
add the flag).

### 4.5 LOW — a ledger row can be counted "double" with unanimous disagreement, and `dissent` only counts disagreement among bound voters

`dissent` is raised when the bound voters for a row carry more than one distinct
word (`tools/mori-vote-bind.py:188-189`). It does **not** compare the voters'
words against the ledger's disposition cell. So two voters who both say `stale`
on a row whose disposition is `holds` produce `double=1, agree=0, dissent=0`:

```
$ … --results probe/s1.json   # both voters say "stale", ledger wants "holds"
TALLY rows=1 agree=0 double=1 single=0 zero=0 dissent=0 voters=2 bound_voters=2
$ … --results probe/s2.json   # one says "holds", one says "stale"
TALLY rows=1 agree=0 double=1 single=0 zero=0 dissent=1 voters=2 bound_voters=2
```

For the frozen round-55 tally this is moot — every bound word is `holds`, so
`agree=78` already implies agreement with the ledger, and `dissent=0` is
truthful in that case. But the `dissent` counter as specified cannot distinguish
"voters agree with each other and with the ledger" from "voters agree with each
other and are all wrong". Routed to round 57.

### 4.6 LOW — text channel: a stray fence marker in prose suppresses every later vote

Fence state toggles on any line whose lstrip starts with ``` or ~~~
(`tools/mori-vote-bind.py:65`, `96-100`), with no check that the line is a fence
*delimiter* rather than prose containing one. A report that mentions a code fence
in passing, or contains an unbalanced fence, silently loses all subsequent votes:

```
$ python3 tools/mori-vote-bind.py extract probe/r1_unpaired_fence.txt   # "intro", "```", then two vote lines
exit=0        # no VOTE lines
$ python3 tools/mori-vote-bind.py extract probe/r2_stray_fence.txt       # "intro", "see ``` snippet", then one vote line
VOTE RECHECK a6e5226259c9 holds text 
exit=0
```

An unbalanced fence is not detectable from one side, so this is inherent to the
design rather than a bug; the risk is a seat that pastes a fenced snippet into
its output mid-report. The JSON channel is unaffected (a fenced scalar is
rejected outright, which the selftest `t_fenced_scalar_ignored` covers). Noted
as a limit, not proposed for change.

### 4.7 LOW — trailing punctuation on the disposition word suppresses the vote

The disposition word is `[A-Za-z][A-Za-z0-9_-]*` with no trailing-punctuation
tolerance (`tools/mori-vote-bind.py:64`), and the rest must be whitespace-
separated. A vote line ending in a period or comma does not bind:

Measured, one vote token per case (the verb is spelled out here so no line in
this report begins with a vote verb): the token `RECHECK a6e5226259c9 holds.`
(period-terminated) produced **no** VOTE line; the token
`RECHECK a6e5226259c9 holds,` (comma-terminated) produced **no** VOTE line; the
token `RECHECK a6e5226259c9 holds (row 12)` produced
`VOTE RECHECK a6e5226259c9 holds text (row 12)`.

Also `RECHECK a6e5226259c9` with no word at all does not bind (correct), and a
13-hex hash does not bind (correct, `t_hash_len_drift_rejected` covers it).
Period-terminated votes are plausible in prose-shaped seat output. Noted as a
limit.

### 4.8 Checks that found nothing

- **No vote loss on the real round-55 bytes.** Every 12-hex vote token appearing
  in any captured output binds; no output had a vote-shaped token that failed to
  bind, and none was dropped by the JSON channel.
- **No hash-prefix collisions** in the committed ledger: 78 rows, 78 distinct
  12-hex prefixes, so `read_ledger`'s hash-keyed dict cannot silently collapse
  two rows.
- **`Mo55Rc14` is the only roster voter with no bound vote** (15 bound of 16),
  and all 10 `single` rows are attributable to `Mo55Rc13` alone. This matches the
  round-55 loss the tool docstring itself describes ("the round-55 lost seat
  Mo55Rc14 carried no votes in either surface, which the tally reports as
  single-vote rows, never as zeros"). The `single=10` figure is a real
  distribution fact, not a binding defect.
- **Literal `\n` inside a text line is expanded to a newline** before line
  splitting (`tools/mori-vote-bind.py:94`), which is what lets a truncated JSON
  document fall back to the text channel. It does not manufacture a vote: a
  quoted peer payload containing an escaped newline before a vote token still
  yields no VOTE line, because the payload's leading prose keeps the line from
  starting with the verb.
- **TMPDIR hygiene holds.** With `TMPDIR` redirected to the seat scratch, the
  counter's scratch directory lands under that TMPDIR (`mori-r56-c2-*`), and
  `/tmp/mori-vote-bind-*` count is 0 — the vote-bind selftest creates its own
  `mori-vote-bind-*` fixture directories under TMPDIR and removes them itself
  (confirmed: after a selftest run with `TMPDIR` set, that TMPDIR is empty).
  No `/tmp` residue from either tool.
- **No credential material, machine id, session material or private URL** appears
  in this report.

---

## Findings

| # | Sev | Finding | File / line |
|---|-----|---------|-------------|
| 1 | MED | `extract` on a wave results file returns exit 0 with zero VOTE lines, because it walks the file document and never re-parses each record's `output` string; `tally` over the identical file binds 15 voters and reports `agree=78`. The two subcommands disagree about the same bytes, and the natural audit command is the silent one. Named limit; does not affect the frozen C2 numbers (the counter uses `tally`). | `tools/mori-vote-bind.py:423-435` (vs `119-133`) |
| 2 | MED | A JSON-wrapped seat output whose vote line sits inside a multi-line field binds nothing (`zero=1, bound_voters=0`), while the identical content as plain text binds (`agree=1`). The frozen round-55 tally is unaffected because all 63 JSON outputs put votes in dedicated single-line vote-list arrays, but the shape dependency is the round-55 failure class in a narrower form. Named limit. | `tools/mori-vote-bind.py:80-104` (JSON channel, `_walk_strings`) |
| 3 | MED | `tally --min N` is inert: the flag is parsed and forwarded as `min_votes` but the row classification is hardcoded at `len(words)==1` / else, so `--min 1` and `--min 99` produce byte-identical output. This is the concrete blocker on the planned ≥2-voters-per-row dispatch-coverage validator. | `tools/mori-vote-bind.py:161`, `184-192`, `202`, `414`, `438` |
| 4 | LOW | The docstring usage advertises `[--disposition-cols N]` but argparse defines no such option; passing it exits 2 with "unrecognized arguments". Docstring/parser drift. | `tools/mori-vote-bind.py:45` vs `413-415` |
| 5 | LOW | `dissent` counts only disagreement *among bound voters*, not disagreement with the ledger disposition: two voters both saying `stale` on a `holds` row yields `double=1 agree=0 dissent=0`. A unanimous-but-wrong row is indistinguishable from a unanimous-and-right row in the `dissent` field. | `tools/mori-vote-bind.py:188-189` |
| 6 | LOW | Text channel: any line whose lstrip begins with ``` or ~~~ toggles fence state, so an unbalanced or prose-embedded fence suppresses every subsequent vote line (exit 0, no VOTE lines). Inherent to line-wise fence tracking; JSON channel unaffected. | `tools/mori-vote-bind.py:65`, `96-100` |
| 7 | LOW | The disposition word carries no trailing-punctuation tolerance: `RECHECK <hash> holds.` and `…, holds,` do not bind, while `…, holds (row 12)` does. | `tools/mori-vote-bind.py:64` |
| 8 | LOW (informational) | `extract` prints no per-file attribution when given multiple files; VOTE lines from different files are interleaved with no separator, so a multi-file invocation cannot be attributed after the fact. | `tools/mori-vote-bind.py:424-435` |

**No HIGH finding.** The assigned checks (A: selftest ×3; B: extract over plain
and JSON outputs) both passed, and every frozen C2 number — the tool pin, the
16/0 selftest, `TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0
voters=16 bound_voters=15`, the `zero=78` junk control, and the frozen round-55
`voted=0` contrast — was independently re-derived from the committed bytes and
reproduced exactly. The counter reports `C2=met` at both `3f494b49` and
`8be2717b`. Nothing found here falsifies the frozen C2 claim; findings 1-3 are
named limits with routed items for round 57, and the counters, predicates,
controls and kill rules are not proposed for change.

Cleanup: the seat scratch tree
`/fast/scratch/hyaku/mori-r56/Mo56ExecBinderSelftest/` was removed after the
evidence above was captured into this report. No fleet-repo, sibling-lane, or
`jj`/git state was mutated by this seat.
