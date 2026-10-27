# Mo56ScribeBinderEntry — `corpus/knowledge/vote-binding-r56.md` against the frozen binder

Seat: read the round-56 vote-binding knowledge entry and `tools/mori-vote-bind.py`
side by side at the freeze tip `8be2717b0809281d07dffe83dad424a4859e0747`, verify every
sentence against the code and the receipts (`evidence/tally-r55.txt`,
`evidence/c2-old-counter-voted0.txt`), check the three S545 citations as
true substrings of `corpus/evidence/sources-r56/rfc8259.txt` at lines 251/308/461
and ≤25 words, and propose corrections as fenced text.

Wave carries no vote items; no line here is a vote line.

Scratch: `/fast/scratch/hyaku/mori-r56/Mo56ScribeBinderEntry/` (`TMPDIR` pointed
inside it), removed at the end of the run. Tooling: nothing installed or
upgraded (python3 stdlib + curl only; no pacman).

## Commands and outcomes (all exit codes observed)

Worked from the lane root; every write went to this report or the scratch dir.

```
$ git show 8be2717b:tools/mori-vote-bind.py > $S/tool.py ; sha256sum $S/tool.py tools/mori-vote-bind.py
8be1acdbb36cd68deba005e21a4a8679534ab5a5099a787aa9335d288dfa6bca  tool.py
8be1acdbb36cd68deba005e21a4a8679534ab5a5099a787aa9335d288dfa6bca  tools/mori-vote-bind.py
$ grep -n "^PIN" .ufo/waves/round-56/count-c2.py
PIN = "8be1acdbb36cd68deba005e21a4a8679534ab5a5099a787aa9335d288dfa6bca"  # frozen at data commit c419fe6d
$ git rev-parse HEAD ; git rev-list --count 8be2717b..HEAD
acc62f54fb0f53b47b428594dc27365150cbd76b
3
```
The tool bytes at the freeze tip are byte-identical to the working tree and to
the C2 pin; HEAD has moved 3 commits past the freeze with the tool untouched.

```
$ python3 tools/mori-vote-bind.py --selftest
VOTE_BIND_SELFTEST pass=16 fail=0                                     exit=0
$ python3 tools/mori-vote-bind.py tally --ledger corpus/knowledge/kernel-v7.3-recheck-r55.md \
    --results .ufo/waves/round-55/w1-results.json --verb RECHECK \
    --voter Mo55Rc01 --voter Mo55Rc02 ... --voter Mo55Rc16
TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15   exit=0
$ python3 tools/mori-vote-bind.py tally --ledger ... --results ... --verb RECHECK   # no --voter
TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=64 bound_voters=15   exit=0
```
The first tally line equals `evidence/tally-r55.txt` byte for byte (that receipt
carries the same line plus `exit=0`).

```
$ python3 .ufo/waves/round-55/count-c1.py 5b295eeebd87ebd610d8d39bfe2035742f740cfa
C1=unmet scope=78 rows=78 matched=78 status_ok=78 line_ok=78 source_rows=ok pins=ok provenance=ok
same=69 moved=7 changed=2 broken=0 holds=78 stale=0 voted=0 dissent=0
rev=5b295eeebd87ebd610d8d39bfe2035742f740cfa failed=votes                                        exit=1
```
That reproduces `evidence/c2-old-counter-voted0.txt` field for field, so the
"identical bytes" contrast holds on a live read (the counter is read-only:
`git show`/`ls-tree`/`rev-parse` only; `PYTHONDONTWRITEBYTECODE=1` set, no
`__pycache__` written).

```
$ curl -sS --max-time 60 https://www.rfc-editor.org/rfc/rfc8259.txt | sha256sum
61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7   (28,360 bytes)
$ sha256sum corpus/evidence/sources-r56/rfc8259.txt
61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7
```
The entry's `sha256 61a5378f…` pin matches both the committed copy and today's
live fetch.

## Sentence-by-sentence verdicts

V = verified against code or receipt; F = falsified; L = true in substance but
imprecise (finding filed).

| entry line(s) | sentence (abridged) | verdict |
|---|---|---|
| 3-6 | header `source:`/`verified-at:`/`recheck:`/`coverage-map:` | V (sha and live fetch reproduced; only this entry matches "vote-binding" under `corpus/knowledge/`) |
| 10-11 | round-55 C1 78-row freshness ledger, unmet on the vote arm, data arms green | V (receipt; `rows=78`, `status_ok=78`, `failed=votes`) |
| 12-13 | cause (1): agreeing vote bound only on an exact stripped text line | L (also binds a prefix-with-rest form; cite range one line short) |
| 14-16 | all fifteen reporting voters are JSON yields "whose `vote_lines` arrays quote the lines" | **F** (2 of 15 use `vote_lines`) |
| 14-16 | stripped-line equality failed for every one and the counter read `voted=0` | V (0 text lines; live run) |
| 16-18 | the same round's C2 counter binds by substring and accepted the shape | V (`count-c2.py:169`, `("ENTAIL %s %s" % …) in out`) |
| 17 | parenthetical `entailed=15` | L (same receipt also records `dissent=8`) |
| 18-19 | the two counters disagreed because "contains" was implemented differently | V (code diff) |
| 19-20 | operator run-10 binding note said: dual-shape parser or bind on files | UNVERIFIED wording (no copy in repo; contract line 40 only names the note) |
| 24 | one parser, two channels, never mixed | V (`extract_votes` returns on the first branch) |
| 26-37 | JSON channel rule, anchored grammar, verb/hash/word alphabets | V (`VOTE_RE`, `_walk_strings`), except the two S545 citations, below |
| 34-37 | prose substrings do not bind | V (`t_json_prose_substring_rejected`) |
| 38-39 | text channel: lines, fences skipped, anchored stripped line | L (omits the literal `\n` un-escaping) |
| 40-41 | last write wins per (verb, hash); channel recorded | V |
| 43-45 | binding unit is the captured `output` field; a report file is not required | V (`read_results` never opens a report) |
| 49-52 | command line + `TALLY …` line | **command F** (argv exit 2); TALLY line V (reproduced) |
| 54-55 | frozen round-55 counter prints `voted=0` on the identical bytes | V (live run) |
| 55-56 | both readings are receipts | V |
| 56-60 | 10 single-vote rows = the dispatch-coverage hole; assigned to Rc13+Rc14; zero dissent | V (single set = the 10 hashes both plan tasks name; `dissent=0`) |
| 64-65 | carried-over limit: binds that output carried a vote, not who authored it | V (round-55 counter docstring states the same limit) |
| 66-68 | exact-scalar binding rejects mid-sentence votes; run-10 alternative remains | V for the rejection; run-10 wording UNVERIFIED |
| 69-71 | fenced-marker scalar does not bind; never observed | V (test; scan found none in round-55) |
| 72-73 | the tally re-binds history, does not re-run voters | V |

## S545 quotation gate (exact substrings, ≤25 words)

Section boundaries in the committed copy: §1 at line 147, §2 (JSON Grammar) at
246, §3 (Values) at 296, §4 at 316, §7 (Strings) at 424.

| cited | entry wording | line content | substring? | ≤25 words | section |
|---|---|---|---|---|---|
| 251 | "a JSON text is one serialized value" | `A JSON text is a serialized value.` | **no** ("one" vs "a", lower-case "a") | yes, 7 | entry says §1; line 251 is **§2** |
| 308 | "its value may be an object, array or string" | `value = false / null / true / object / array / number / string` | **no** | yes, 9 | entry says §2; line 308 is **§3** |
| 461 | `quotation-mark *char quotation-mark` | `    string = quotation-mark *char quotation-mark` | yes | yes, 3 | entry says §2; line 461 is **§7** |

The correct 251 quote already exists in this round's own lesson
(`corpus/lessons/round-56.md`, S545 admission row: `A JSON text is a serialized
value.` (line 251)), so the entry misquotes a sentence its own gate row got
right.

## Evidence for the falsified shape claim

Per-seat vote-carrying key in the committed `.ufo/waves/round-55/w1-results.json`
(a seat can carry two):

```
Mo55Rc01 vote_lines       Mo55Rc02 votes           Mo55Rc03 votes
Mo55Rc04 votes            Mo55Rc05 votes           Mo55Rc06 final_vote_lines
Mo55Rc07 votes            Mo55Rc08 final_votes     Mo55Rc09 votes
Mo55Rc10 votes,final_vote_lines                     Mo55Rc11 votes
Mo55Rc12 votes            Mo55Rc13 final_vote_lines Mo55Rc14 <malformed JSON>
Mo55Rc15 vote_lines       Mo55Rc16 voteLines
key census: vote_lines 2, votes 9, final_vote_lines 3, final_votes 1, voteLines 1
```
Every one of the 15 seats binds 10 votes (Rc15/Rc16: 8) through the
document-order scalar walk, so the shape conclusion stands and only the key name
is wrong — in the entry, in the tool docstring (`tools/mori-vote-bind.py:6`), and
in `corpus/lessons/round-55.md:95` (the likely origin).

Single-row check (independent of the binder's loop): the 10 hashes Rc13's and
Rc14's plan task texts name are identical sets (`comm -12` → 10), and that set
equals the 10 single-voted rows (`a6e5226259c9`, `0124918d278a`, `6f9f1d32ac46`,
`68afd0d6fa2f`, `0527161c4edd`, `82952b5a6ec2`, `2ba00a976118`, `d0338d4263b9`,
`bfb67ed4f174`, `53875978a00b`); every bound word on them is `holds`, dissent 0.
Rc14's captured output does not parse as JSON and carries no vote-grammar line
(0 bound votes).

## Proposed corrections

Entry, "The failure class", lines 14-16:

```text
-All fifteen reporting RECHECK voters emitted structured JSON yields whose
-`vote_lines` arrays quote the lines, so stripped-line equality failed for every
-one of them and the counter read `voted=0`.
+All fifteen reporting voters emitted structured JSON yields whose vote lines sit
+in quoted string scalars; the array key is not uniform (`vote_lines` 2, `votes`
+9, `final_vote_lines` 3, `final_votes` 1, `voteLines` 1), which is why only the
+document-order scalar walk binds all fifteen. Stripped-line equality failed for
+every one of them and the counter read `voted=0`.
```

Entry, "The frozen rule", lines 31-33 (two quote wordings and three section
labels):

```text
-  grammar reading: a JSON text is one serialized value (S545 §1, line 251)
-  whose value may be an object, array or string (S545 §2 grammar, line 308),
-  and a string is `quotation-mark *char quotation-mark` (S545 §2, line 461) —
+  grammar reading: "A JSON text is a serialized value." (S545 §2, line 251)
+  whose production is `value = false / null / true / object / array / number /
+  string` (S545 §3, line 308), and a string is
+  `quotation-mark *char quotation-mark` (S545 §7, line 461) —
```

Entry, "Measured", line 49 — `--voter` is argparse `action="append"`, so the
flag repeats and a space-separated list exits 2:

```text
-`python3 tools/mori-vote-bind.py tally --ledger corpus/knowledge/kernel-v7.3-recheck-r55.md --results .ufo/waves/round-55/w1-results.json --verb RECHECK --voter Mo55Rc01 … Mo55Rc16`
+`python3 tools/mori-vote-bind.py tally --ledger corpus/knowledge/kernel-v7.3-recheck-r55.md --results .ufo/waves/round-55/w1-results.json --verb RECHECK --voter Mo55Rc01 --voter Mo55Rc02 --voter Mo55Rc03 --voter Mo55Rc04 --voter Mo55Rc05 --voter Mo55Rc06 --voter Mo55Rc07 --voter Mo55Rc08 --voter Mo55Rc09 --voter Mo55Rc10 --voter Mo55Rc11 --voter Mo55Rc12 --voter Mo55Rc13 --voter Mo55Rc14 --voter Mo55Rc15 --voter Mo55Rc16`
```

(Omitting `--voter` also works: the roster defaults to every seat in the results
file, giving `voters=64 bound_voters=15`.)

Entry, lines 12-13 (mechanism is slightly wider than "exact line"; cite the
second predicate line):

```text
-agreeing vote only when the voter's captured output contained the exact
-`RECHECK <h> <w>` line as a stripped *text* line (`.ufo/waves/round-55/count-c1.py:286-301`).
+agreeing vote only when the voter's captured output carried, as a stripped
+*text* line, that verb line and word — equality, or the same line followed by a
+space and rest (`.ufo/waves/round-55/count-c1.py:286-302`, predicate at 301-302).
```

Entry, lines 38-39 (text channel pre-processing):

```text
-* **text channel** — otherwise the output is read as lines; fenced blocks are
-  skipped; an unfenced stripped line binds by the same anchored grammar.
+* **text channel** — otherwise the output is read as lines, after the literal
+  two-character sequence backslash-n is turned into a newline first; fenced
+  blocks are skipped; an unfenced stripped line binds by the same anchored
+  grammar.
```

Entry, line 17 (report both fields of the same receipt):

```text
-by substring and accepted the identical shape (`entailed=15`) — the two
+by substring and accepted the identical shape (`entailed=15 dissent=8` in
+`evidence/c2-at-landed.txt`) — the two
```

Entry, lines 56-58 (pairing is in the plan, not the lesson):

```text
-single-vote rows are the dispatch-coverage hole the round-55 lesson records
-(rows assigned to Mo55Rc13+Mo55Rc14, the latter settling with no votes); under
+single-vote rows are the dispatch-coverage hole the round-55 lesson records
+(`.ufo/waves/round-55/w1-plan.json` assigns the same 10 rows to Mo55Rc13 and
+Mo55Rc14; the latter settled with no votes); under
```

Tool docstring, line 45 (flag does not exist; `tally --help` lists only
`--ledger --results --verb --voter --min`):

```text
-      [--voter NAME ...] [--min N] [--disposition-cols N]
+      [--voter NAME ...] [--min N]
```

Tool docstring, lines 5-7 (same shape claim as the entry; the following line
must change with it or the prose breaks):

```text
-  output carried the exact `RECHECK <h> <w>` line as a stripped *text* line; all
-fifteen reporting voters emitted structured JSON yields whose `vote_lines`
-arrays quote the lines, so the frozen counter read `voted=0` on bytes that
+  output carried that verb line as a stripped *text* line; all fifteen reporting
+voters emitted structured JSON yields whose vote lines sit in quoted string
+scalars under five different array-key spellings, so the frozen counter read
+`voted=0` on bytes that
```

## Limits / not checked

- The `verified-at: 2026-10-27 (live fetch …)` provenance itself is unobservable;
  what is observable is that the pinned copy equals today's rfc-editor bytes and
  the recorded sha256 prefix.
- The run-10 note's wording is not in the repo; only the contract's reference
  (`.ufo/waves/round-56/contract.md:40`) corroborates that it exists.
- I did not audit `count-c2.py`'s predicate or the C1 driver-liveness surface
  (other seats own those); I read `count-c2.py` only for the pin.
- Nothing here re-runs voters, rewrites the ledger, or touches counters; the
  re-pin cost of any wording change is the L1's call.
- The lane tree was already dirty before this seat (`LOG.md`, `SCORECARD.md`,
  `SHONEN.md` modified; `w1.ready` untracked); I wrote only this report and my
  scratch, and removed the scratch.

## Findings

- **HIGH** — `corpus/knowledge/vote-binding-r56.md:14-16` states all fifteen
  reporting voters' votes sit in "`vote_lines` arrays". Committed bytes show
  literal `vote_lines` on 2 of 15 seats (Mo55Rc01, Mo55Rc15); the rest use
  `votes` (9), `final_vote_lines` (3), `final_votes` (1), `voteLines` (1). Same
  false wording at `tools/mori-vote-bind.py:6` and `corpus/lessons/round-55.md:95`;
  correction fenced above. Not a counter defect — the tally and the `voted=0`
  contrast both reproduce exactly.
- **MED** — `corpus/knowledge/vote-binding-r56.md:31-33`: two of the three S545
  citations fail the true-substring test — "a JSON text is one serialized value"
  (RFC: `A JSON text is a serialized value.`) and "its value may be an object,
  array or string" (line 308 is the full `value = false / null / true / object /
  array / number / string` production) — and all three section labels are wrong
  (§2/§3/§7 cited as §1/§2/§2). The line numbers 251/308/461 are correct.
- **MED** — `corpus/knowledge/vote-binding-r56.md:49`: the displayed tally
  command is not executable (`--voter` is `action="append"`; the space-separated
  list exits 2 with `unrecognized arguments: Mo55Rc02 …`). The receipt value
  itself is reproduced with repeated flags.
- **LOW** — `corpus/knowledge/vote-binding-r56.md:32`: the quoted `value`
  production omits `false/null/true/number`, and the code deviates exactly there
  for `null` (`final_votes("null")` → channel `text`, not `json`, because the
  guard is `doc is not None`); "if the whole output parses as a JSON value" is
  therefore not the implemented test.
- **LOW** — `corpus/knowledge/vote-binding-r56.md:38-39`: the text channel
  un-escapes the literal two-character `\n` before splitting lines
  (`extract_votes`, `output.replace("\\n", "\n")`); one captured "line" can
  therefore become several. Not documented.
- **LOW** — `corpus/knowledge/vote-binding-r56.md:12-13`: "exact … line" is
  narrower than the code, which also binds a stripped line that starts with the
  verb, hash and word followed by a space; and the cited range 286-301 stops one
  line before the `startswith` alternative at 302.
- **LOW** — `corpus/knowledge/vote-binding-r56.md:17`: citing only `entailed=15`
  from `evidence/c2-at-landed.txt` (which also records `dissent=8`) makes the
  substring binder read as fully green on that arm.
- **LOW** — `corpus/knowledge/vote-binding-r56.md:56-58`: the "rows assigned to
  Mo55Rc13+Mo55Rc14" detail is not in the lesson it is attributed to
  (`corpus/lessons/round-55-verifier-spotcheck.md:27` records only "10 rows
  single-voted via dead `Mo55Rc14`"); the pairing is in
  `.ufo/waves/round-55/w1-plan.json`. It is true — 10 identical hashes per task.
- **LOW** — `tools/mori-vote-bind.py:45`: docstring advertises
  `[--disposition-cols N]`, which argparse does not define (`tally --help`
  lists five options).

Report: .ufo/waves/round-56/w1/Mo56ScribeBinderEntry.md
