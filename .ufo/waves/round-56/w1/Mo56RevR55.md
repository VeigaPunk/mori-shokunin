# Mo56RevR55 — round-55 vote-binding failure: reconstruction with hashes

Seat: Mo56RevR55 (reviewer, leaf). Lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Entering tip `5b295eeebd87ebd610d8d39bfe2035742f740cfa`; round-56 freeze `8be2717b0809281d07dffe83dad424a4859e0747`.
Scratch `/fast/scratch/hyaku/mori-r56/Mo56RevR55/` (removed at end). No tool installed (no pacman, no uv, no binary
added) — no tool/version record owed. Read-only throughout: `git show/log/cat-file/ls-tree` only; nothing in the lane
worked tree, the index or jj was touched.

Revisions this reconstruction stands on:

| role | hash | timestamp |
|---|---|---|
| r53 freeze | `f4da3fd4` | 2026-10-26 22:08:38 -0300 |
| r53 results record (salvage) | `0df80303` | 2026-10-26 23:28:22 -0300 |
| r54 freeze | `6830f3af` | 2026-10-27 01:10:36 -0300 |
| r54 integration (results + verdict) | `f111d4b0120a04ed1a0a2270a72ec0a343d20e29` | 2026-10-27 02:15:42 -0300 |
| r55 freeze (counters, contract) | `c9b908f0bb89974f30b927776ce2450ae4198b10` | 2026-10-27 03:04:36 -0300 |
| r55 dispatch input (seat prompts) | `96d888f5` | 2026-10-27 03:39:57 -0300 |
| r55 `w1.ready` published | `b8a70adf` | 2026-10-27 03:40:30 -0300 |
| r55 settlement integrated | `a27ec48210b136d9f2fd1b71c5e64f65f5a30e22` | 2026-10-27 03:41:17 -0300 |
| r55 verdict receipts | `d27d943a` | 2026-10-27 04:11:58 -0300 |

## 1. Timeline (diff of the vote arm, r53 → r54 → r55)

Command (exit 0):

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --format='%H %ad %s' --date=iso \
    -- .ufo/waves/round-55/count-c1.py .ufo/waves/round-54/count-c1.py
c9b908f0bb89974f30b927776ce2450ae4198b10 2026-10-27 03:04:36 -0300 round-55: freeze claims, counters, sources and controls
6830f3af992d906bfa1e17e3743e631ab834f67c 2026-10-27 01:10:36 -0300 round-54: freeze — contract, counters C1 (v7.3 recheck of the 31 remaining v7.2-pinned rows, line arm, results-bound voters) and C2 (memory-failure kills at v7.3), controls, receipts, census-start, sweeps, ten v7.3 copies
```

Round-53 counter first added at `f4da3fd4` (2026-10-26 22:08:38), round-54 at `6830f3af`, round-55 at `c9b908f0`
(`git log --diff-filter=A ... -- .ufo/waves/round-53/count-c1.py .ufo/waves/round-54/count-c1.py
.ufo/waves/round-55/count-c1.py .ufo/waves/round-5[0-9]/count-c2.py`, exit 0).

**r53 arm (report-only).** `count-c1.py:final_votes(read, ls)` reads `VOTE_DIR + voter + ".md"` only; it never opens
`w1-results.json`. A vote is the voter's last unfenced line in its own report. Landed met:
`C1=met ... voted=46 dissent=0` (`exit=0`, `.ufo/waves/round-53/evidence/c1-at-landed.txt`).

**r54 arm (settlement-name filter, no output content).** `count-c1.py:238-267` adds `settled.add(r["name"])`
(line 247) from `w1-results.json`; a voter counts only when present in the results file's `name` fields. The `output`
string is never read — the selftest fixture is the literal placeholder `"output": "x"` (line 481). Landed met:
`C1=met ... voted=31 dissent=0 ... exit=0` (`.ufo/waves/round-54/evidence/c1-at-landed.txt`).

**r55 arm (stripped-line binding).** New `def votes(read, ls)` at `.ufo/waves/round-55/count-c1.py:284-303`:

```
284 def votes(read, ls):
...
291                 outputs[r["name"]] = r.get("output") if isinstance(r.get("output"), str) else ""
...
299         out_lines = set(l.strip() for l in outputs.get(voter, "").replace("\\n", "\n").split("\n"))
301             bound = voter in outputs and any(l == "RECHECK %s %s" % (h, w) or l.startswith("RECHECK %s %s ")
302                                               for l in out_lines)
```

An agreeing vote counts only when a *stripped line* of the captured `output` equals, or starts with, `RECHECK <h> <w> `.
Landed: `C1=unmet scope=78 rows=78 matched=78 status_ok=78 line_ok=78 source_rows=ok pins=ok provenance=ok
same=69 moved=7 changed=2 broken=0 holds=78 stale=0 voted=0 dissent=0 rev=a27ec482... failed=votes`, `exit=1`
(`.ufo/waves/round-55/evidence/c1-at-landed.txt`, committed `d27d943a`).

## 2. When the stripped-line binding was introduced, and where

**Introduced at the round-55 freeze, commit `c9b908f0bb89974f30b927776ce2450ae4198b10` (2026-10-27 03:04:36 -0300),
file `.ufo/waves/round-55/count-c1.py`, lines 299-302 — first and only introduction in lane history.**

Command (exit 0):

```
$ git -C ... log -S'out_lines' --format='%h %ad %s' --date=iso -- '.ufo/waves/*/count-c1.py' '.ufo/waves/*/count-c2.py'
c9b908f0 2026-10-27 03:04:36 -0300 round-55: freeze claims, counters, sources and controls
```

`git log -L 295,305:.ufo/waves/round-55/count-c1.py` (exit 0) shows the file born at `c9b908f0` with that block already
present — no earlier revision of any round's C1/C2 counter contains `out_lines` or names a results-`output` token in a
vote arm. A per-round token census over `.ufo/waves/round-4[7-9]`/`round-5[0-3]` `count-c1.py`/`count-c2.py` returns
zero `output` occurrences; round-54 contains exactly one (the selftest placeholder `"output": "x"`).

The frozen pin of the file is `e30658be34bfbf866860b20c9bde4117d467e351bb79e523131424cd5061e20b`
(`.ufo/waves/round-55/evidence/freeze-sha256.txt` line 6), and `sha256sum .ufo/waves/round-55/count-c1.py` reproduces it
(exit 0), so the code I diffed is the code that scored.

## 3. Where the seat-output format rule was written before the wave dispatched

The only pre-dispatch written statement is in the per-seat dispatch prompts — `.ufo/waves/round-55/w1-input.json`
(and the identical `.ufo/waves/round-55/w1-plan.json`), committed `96d888f5` at 03:39:57, i.e. **57 s before the
`w1.ready` marker (`b8a70adf`, 03:40:30)**:

- RECHECK seats (Mo55Rc01…Mo55Rc16), verbatim: “Write one unfenced line `RECHECK <hash> holds|stale` for every
  assigned hash; include exactly those final lines in final output. No other hashes.”
- ENTAILMENT seats (Mo55En01…Mo55En12), verbatim: “Exactly one unfenced ENTAIL line per hash; repeat all exact final
  lines in final response.”

Nothing else carried the rule before dispatch:

- `.ufo/waves/round-55/contract.md` (frozen `c9b908f0`) says only “2+ settled, output-bound RECHECK voters per row” —
  it states that an output binding exists, never what shape the output must have.
- `SKILL.md` has no seat-output rule (grep for `output`/`final line` returns tool-inventory rows only).
- The round-54 dispatch record (`.ufo/waves/round-54/w1-spec.json`) contains no such instruction at all — grep for
  `final output|include exactly|in your final` returns no hit, and `.ufo/waves/round-54/w1-dispatch.json` reports
  `has final output: False`. So the instruction was *new* at r55.
- The “run-10 binding note” cited by the round-56 contract exists in committed text only as a round-56 artefact
  (`corpus/knowledge/vote-binding-r56.md:19`, `tools/mori-vote-bind.py:11`, `.ufo/waves/round-56/contract.md:40`).
  A scan of the lane tree and fleet `.ufo` for `run-10` / `binding note` found no pre-r55 copy. Whether the L1 held
  that note in session before 03:39:57 is **UNVERIFIED**.

Critically, the rule as written was *satisfied* by the seats: it asks for the lines to be included, and every one was
included — inside a structured yield. It never says “plain text, not inside a JSON object/array”, and the strictness
lived only in code (see §6).

## 4. Was the JSON-wrap shape foreseeable from r54's seats? Yes — universally, and it had never once been otherwise

The harness makes the wrap structural. `scripts/hyaku/inline-dispatcher.py:279-296` captures each seat as
`str(h.output())[:20000]` and writes it to `<wave>-results.json` as the `output` field:

```
279 def seat_output(name, w=None):
...
284         return str(h.output())[:20000]
...
294         res.append({'name': n, 'agent': w['agents'][n], 'output': o,
```

A seat that yields structured data therefore stores a structured (JSON-shaped) string; a bare line-start text line is
possible only when the seat's entire final yield is plain text.

Captured-bytes census over every committed results record (script: parse `output`, split on real newlines, test
`^(RECHECK|ENTAIL) <12 hex> <word>` at line start vs. quoted-line form; exit 0):

| round | results | JSON-wrapped output | line-start vote lines | quoted vote lines |
|---|---|---|---|---|
| 53 (`0df80303`) | 67 | 67 | **0** | 23 |
| 54 (`f111d4b0`) | 74 | 73 | **0** | 7 |
| 55 (`a27ec482`) | 64 | 63 | **0** | 422 |

So in the two waves committed before the r55 freeze — r54 at 02:15:42, 49 minutes before `c9b908f0`; r53 at
2026-10-26 23:28:22, about 5 h 36 min before it — **zero of 141 captured seat outputs carried a line-start vote line**.
Round-54's RECHECK voters in particular emitted `{"seat": ..., "votes": {"<hash>": "holds", ...}}` (hash→word maps:
e.g. `Mo54Rc02`), i.e. the votes were present but never as text lines at all. The new binding demanded a shape no seat
in lane history had produced.

Direct reproduction with the frozen counter (copied to scratch, sha256 verified `e30658be…`, imported, `votes()`
called on synthetic `read`/`ls`; two hashes, plain reports identical in every case; exit 0):

```
A selftest-shape plain output: votes=4 bound=4
C captured r55 output (16 voters): votes=32 bound=0
E r55 output with literal backslash-n: votes=32 bound=0
```

Shape of the captured r55 side (every vote line present, every one quoted):

```
Mo55Rc01 output fragment:  "vote_lines": [\n    "RECHECK 7b2d297eec60 holds",\n ...
Mo55Rc02 output fragment:  "votes": [\n    "RECHECK 7b2d297eec60 holds",\n ...
```

Verbatim check (exit 0): of the 146 vote lines that appear in the 15 delivered RECHECK reports at `a27ec482`, **146 occur
verbatim as substrings in the matching captured outputs and 0 are absent**. A substring test binds 146/146; the frozen
stripped-line test binds 0/146.

## 5. The check that would have caught it (captured-by)

**A freeze-time control that feeds the binding a captured `output` instead of a synthetic one.** The r55 selftest builds
its results fixture by hand — `.ufo/waves/round-55/checks/selftest-c1.py:59`:

```
res = {"results": [{"name": n, "output": "\n".join("RECHECK %s %s" % (h, out_word or word) for h in hashes)
```

i.e. the fixture output is a plain multi-line string, which is the one shape that never occurs in a real wave. Of the 44
selftest cases (`C1_SELFTEST pass=44 fail=0`, `.ufo/waves/round-55/evidence/selftest-c1.txt`), the only two touching the
output field are “voter whose output lacks the line does not count” and “voters absent from results do not count”, both
also built from synthetic plain strings. Had either fixture used a byte-copied `output` from the previous round's
committed results file (`f111d4b0:.ufo/waves/round-54/w1-results.json`, available 49 min before the freeze), the case
would have printed bound=0 for every voter and the arm would have failed at freeze, before dispatch — exactly what my
scratch reproduction above shows (A 4/4 vs C 0/32).

Two weaker variants of the same check, both also satisfied by committed bytes:

1. **Satisfiability control:** “for at least one captured voter output in the preceding wave's results record, the
   binding binds” (census above: 0/74 at r54).
2. **Sibling-diff control:** the round's other counter implemented the same clause differently
   (`.ufo/waves/round-55/count-c2.py:160-170` uses substring containment, `("ENTAIL %s %s" % (...)) in out`) and bound
   the identical JSON-wrapped shape (`entailed=15`). Diffing the two arms' “contains” would have exposed the mismatch
   at freeze.

The retrospective form of this check exists only at round 56: `tools/mori-vote-bind.py` re-binds the round-55 tally over
committed bytes (`TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15`) and its
selftest case `t_json_array_binds` exercises exactly the `vote_lines` array shape.

## 6. Divergence between the frozen predicate text and the frozen code

- Frozen predicate (`count-c1.py:26-27`, and the identical sentence in `contract.md`): an agreeing vote counts only
  when “that result's output contains that same final `RECHECK <h> <word>` line”.
- Frozen code (`count-c1.py:299-302`): a *stripped line* must equal, or begin with, `RECHECK <h> <word> `.

Under the sentence's plain reading (“contains … line”) the r55 bytes satisfy the predicate 146/146 (§4); under the code
they satisfy it 0/146. The two r55 counters also resolved the same clause oppositely (line equality in C1, substring in
C2), and C2's reading is the one that bound. The strict reading is a defensible overclaim guard (a scalar that merely
mentions a vote sentence is prose), but it was not what the frozen text said, and it was frozen without a
captured-shape fixture.

## 7. Second, independent cause: the shape fix alone would not have met C1

Coverage computed from the delivered reports at `a27ec482` (script: parse assignment sets from `w1-input.json` items and
final vote lines from each report; exit 0):

```
assigned per voter: Rc01–Rc13 = 10 each, Rc14 = 10, Rc15 = 8, Rc16 = 8
votelines per voter: Rc01–Rc13 = 10 each, Rc14 = 0 (no report), Rc15 = 8, Rc16 = 8
rows covered: 78   single-voted: 10
single rows == Rc14's assigned set: True (overlap 10/10)
assigned-but-unvoted hashes: 0
```

`Mo55Rc14` has no report at any revision (`git log --all -- .ufo/waves/round-55/w1/Mo55Rc14.md` → empty; `git cat-file
-e a27ec482:.ufo/waves/round-55/w1/Mo55Rc14.md` → “does not exist”, exit 128), and its settlement record is a
non-answer prose blob (`"agent": "critic"`, no vote lines). Its ten rows are covered only by `Mo55Rc13`, which received
the identical assignment. With `MIN_VOTES = 2`, even a fully working binding yields `voted=68`, still `failed=votes` —
consistent with the round-56 re-bound tally's `double=68 single=10`.

## 8. Limits of this reconstruction

- I did not run the frozen r55 counter at `a27ec482` (would need its committed copies + SOURCES read path; the verdict
  receipts already record `voted=0`, and the L1's scoring is not mine to re-derive). My binding figures come from
  importing the frozen `votes()` on the frozen sha256 and from the committed `output`/report bytes.
- The `output` field is truncated at 20000 chars by the dispatcher (`inline-dispatcher.py:284`). No r55 voter output
  approaches it (largest Rc output 2717 chars in r54, ≈1.5 KB in r55), so truncation is not a cause here; it is a named
  limit for any future tally over long seats.
- Whether the orchestrator/L1 could have issued a run-10 binding note before dispatch, and whether an uncommitted
  captured-output probe was ever attempted, is **UNVERIFIED** (no committed record).
- Intent attribution (why the strict form was chosen) is inference; only the texts and bytes are observed.
- Confidence: **HIGH** for every hash, line number, count and reproduction above (each from a command whose output is
  quoted); **MEDIUM** only for the run-10 provenance gap, which is stated as unverified.

## Findings

1. **HIGH — the r55 C1 vote arm was unsatisfiable as frozen.** `.ufo/waves/round-55/count-c1.py:299-302` was introduced
   at freeze `c9b908f0` (2026-10-27 03:04:36) and requires a line-start `RECHECK <h> <w>` line in the captured
   `output`; the harness stores `str(h.output())[:20000]` (`scripts/hyaku/inline-dispatcher.py:284`), and 0 of 141
   captured outputs in r53+r54 carried such a line. Result `voted=0` on 146/146 votes that were present. This is
   history, not a proposal to change the frozen r56 predicate — the counter-side lesson is “no output binding without a
   captured-shape fixture”.
2. **HIGH — no captured-output fixture anywhere in the freeze.** `.ufo/waves/round-55/checks/selftest-c1.py:59` builds a
   plain-text `output`; the round-54 precedent was the placeholder `"output": "x"`
   (`.ufo/waves/round-54/count-c1.py:481`). A one-case control fed the previous round's committed `output` bytes
   (`f111d4b0:.../round-54/w1-results.json`) would have printed bound=0 at freeze (reproduced: A 4/4 vs C 0/32).
3. **MED — frozen predicate text and frozen code disagreed on “contains”.** `count-c1.py:26-27` (“output contains that
   same final … line”) vs `count-c1.py:299-302` (stripped-line equality), and vs the same round's
   `count-c2.py:160-170` (substring). Same bytes, three readings, two verdicts in one round.
4. **MED — the pre-dispatch rule named no shape.** The only written rule before dispatch was the seat-prompt sentence
   in `.ufo/waves/round-55/w1-input.json` (commit `96d888f5`, 03:39:57, 57 s before `b8a70adf`): “include exactly those
   final lines in final output”. It did not say “plain text, unfenced, not inside a JSON object/array”, and the frozen
   contract (`c9b908f0`) named only “output-bound … voters”. Every seat complied with the sentence as written.
5. **MED — coverage gap independent of the binding (latent).** `Mo55Rc14` delivered no report at any revision and its
   settlement carried no vote lines, leaving exactly its ten assigned rows single-voted by `Mo55Rc13`
   (`a6e5226259c9 0124918d278a 6f9f1d32ac46 68afd0d6fa2f 0527161c4edd 82952b5a6ec2 2ba00a976118 d0338d4263b9
   bfb67ed4f174 53875978a00b`). A correct binding still reads `voted=68/78`. Already routed in the r55 lesson; restated
   because any “shape fix” alone would not have met C1.
6. **LOW — cite drift in the round-56 knowledge note.** `corpus/knowledge/vote-binding-r56.md:12-13` cites
   `.ufo/waves/round-55/count-c1.py:286-301` for the binding; the block is `def votes` at 284 through `return per` at
   303, with the binding itself at 299-302.
7. **LOW — output truncation is an unstated bound in every output-binding design.** `inline-dispatcher.py:284`
   truncates at 20000 chars; a long seat's later vote lines could be cut silently (no r55 case is near the bound).
   Named limit for round 57, not a defect of the frozen r56 counters.
