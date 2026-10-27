# Mo56ExecBinderTally — round 56 w1 (C2 binder/tally falsification seat)

Seat: `Mo56ExecBinderTally` (leaf, executor). Lane: mori-shokunin.
Scope: reproduce the frozen round-56 C2 tally line, then build an INDEPENDENT
counter (no import of `tools/mori-vote-bind.py`) and attack both the number and
the semantics behind it. Detection and report only — no lane, fleet or jj state
mutated; scratch removed on exit.

Freeze tip (entered): `8be2717b0809281d07dffe83dad424a4859e0747`.
Entering tip: `5b295eeebd87ebd610d8d39bfe2035742f740cfa`.
Tool sha256 at 8be2717b and in the worktree: `8be1acdbb36cd68deba005e21a4a8679534ab5a5099a787aa9335d288dfa6bca`
(== `PIN` in `.ufo/waves/round-56/count-c2.py:46`).

## Verdict

- The frozen line **reproduces exactly** from the committed bytes:
  `TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15`, exit 0.
- Three independent counters (my own JSON-aware one, a line-wise variant, and a
  raw-bytes/no-JSON-parse variant) all produce the **same four totals**:
  **double=68, single=10, zero=0, dissent=0** (and agree=78).
- A raw-bytes scan (no parser, no grammar, every `RECHECK <hash> <word>`
  occurrence anywhere in all 64 captured outputs) finds **zero** votes the
  binder misses and **zero** extra binds: the grammar loses nothing on this
  dataset.
- The 10 single-voted rows are **not** a binder defect: they are exactly the
  10 rows of `Mo55Rc13`, whose paired seat `Mo55Rc14` was lost (no report file,
  captured output carries no vote token). The tally surfaces this honestly.
- C2 as frozen is **not falsified**. But two **metric semantics** differ from
  the round-55 counter the C2 claim contrasts itself against, and one of them
  can report `dissent=0` while every voter is wrong. Those are named limits +
  routed items for round 57 (the C2 counter, predicates and controls are
  frozen; I propose no change to them here).

## 1. Reproduction of the frozen line

Command (exactly as specified in the seat brief):

```
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-vote-bind.py tally \
  --ledger /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/knowledge/kernel-v7.3-recheck-r55.md \
  --results /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-55/w1-results.json \
  --verb RECHECK --voter Mo55Rc01 .. --voter Mo55Rc16
```

Observed output:

```
TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15
exit=0
```

Byte-identical to the frozen receipt
`.ufo/waves/round-56/evidence/tally-r55.txt` (`TALLY rows=78 agree=78 double=68
single=10 zero=0 dissent=0 voters=16 bound_voters=15` / `exit=0`).

Inputs are the committed bytes, verified identical at every relevant revision
(`git show <rev>:<path> | sha256sum`):

| artifact | 3f494b49 | 8be2717b | HEAD | worktree |
|---|---|---|---|---|
| `.ufo/waves/round-55/w1-results.json` | `2e5b0a0f…d9763b` | same | same | same |
| `corpus/knowledge/kernel-v7.3-recheck-r55.md` | `462e67c1…5e8e` | same | same | same |
| `tools/mori-vote-bind.py` | — | `8be1acdb…a6bca` | — | `8be1acdb…a6bca` |

(`git status --porcelain` on the two artifacts: empty — no worktree drift.)

Tool selftest, run from the worktree copy:

```
VOTE_BIND_SELFTEST pass=16 fail=0
exit=0
```

Frozen C2 counter re-run at the freeze tip (read-only):

```
python3 .ufo/waves/round-56/count-c2.py 8be2717b0809281d07dffe83dad424a4859e0747
C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=8be2717b0809281d07dffe83dad424a4859e0747
exit=0
```

## 2. My independent counter (no tool import)

Built at `/fast/scratch/hyaku/mori-r56/Mo56ExecBinderTally/indep_tally.py`
(scratch, now removed). It does **not** import `tools/mori-vote-bind.py`; it
re-derives the ledger from the header (disposition column located **by header
name**, not by hardcoded index) and re-implements vote extraction itself.

Three extraction modes were run over the same bytes:

- `toolish` — JSON channel walks string scalars, whole-scalar anchored match;
  text channel scans unfenced lines; last write wins per (verb, hash).
- `linewise` — every string scalar is split into lines and each line matched
  on its own (deliberately looser: a vote anywhere on its own line counts).
- raw bytes — a third script with **no JSON parsing at all**: for each voter,
  the last occurrence in byte order of a vote token decides that voter's word.

All three agree, and the `toolish` table is **byte-identical** to the `linewise`
table (`diff` of the two per-hash tables: no differences).

Header derivation (independent): `ledger_header=['hash','entry','pointer','v7.3
source','v7.3 lines','status','disposition']`,
`disposition_col_index=6`; `ledger_rows=78`; `results_records=64`;
`voters_requested=16 present=16 missing=[]`;
`bound_voters=15 unbound=['Mo55Rc14']`.

### Per-hash table head (independent counter, mode `toolish`)

```
hash        bucket  n  agree distinct        want   entry
0124918d278a single   1     1 holds            holds   corpus/knowledge/system-pressure-r24.md
02b8d2d11094 double   2     2 holds            holds   corpus/knowledge/system-pressure-r24.md
037f662ce719 double   2     2 holds            holds   corpus/knowledge/system-pressure-r24.md
0527161c4edd single   1     1 holds            holds   corpus/knowledge/oom-victim-selection-r27.md
079fc0192229 double   2     2 holds            holds   corpus/knowledge/system-pressure-r24.md
07a985363937 double   2     2 holds            holds   corpus/knowledge/oom-victim-selection-r27.md
0d7523eee480 double   2     2 holds            holds   corpus/knowledge/system-pressure-r24.md
0e16bb6f5925 double   2     2 holds            holds   corpus/knowledge/system-pressure-r24.md
0ee301f4c8ae double   2     2 holds            holds   corpus/knowledge/system-pressure-r24.md
14238678b995 double   2     2 holds            holds   corpus/knowledge/system-pressure-r24.md
1490a683aca7 double   2     2 holds            holds   corpus/knowledge/system-pressure-r24.md
1c11a3f36bf3 double   2     2 holds            holds   corpus/knowledge/oom-tracepoints-r47.md
1c3dad2ad6e2 double   2     2 holds            holds   corpus/knowledge/system-pressure-r24.md
2547b0838a9b double   2     2 holds            holds   corpus/knowledge/system-pressure-r24.md
2b9148b31cd6 double   2     2 holds            holds   corpus/knowledge/system-pressure-r24.md
2ba00a976118 single   1     1 holds            holds   corpus/knowledge/oom-victim-selection-r27.md
301bfba80d7d double   2     2 holds            holds   corpus/knowledge/oom-tracepoints-r47.md
3b2c0c15134d double   2     2 holds            holds   corpus/knowledge/system-pressure-r24.md
... (78 rows total; table head above, tail below)
ee326a28c54f double   2     2 holds            holds   corpus/knowledge/oom-tracepoints-r47.md
ee7308fa713e double   2     2 holds            holds   corpus/knowledge/system-pressure-r24.md
eee4454705c0 double   2     2 holds            holds   corpus/knowledge/system-pressure-r24.md
f701e7773747 double   2     2 holds            holds   corpus/knowledge/system-pressure-r24.md
```

### The four totals (independent counters)

| counter | rows | agree | double | single | zero | dissent | voters | bound_voters |
|---|---|---|---|---|---|---|---|---|
| frozen tool (specified invocation) | 78 | 78 | **68** | **10** | **0** | **0** | 16 | 15 |
| independent `toolish` | 78 | 78 | 68 | 10 | 0 | 0 | 16 | 15 |
| independent `linewise` | 78 | 78 | 68 | 10 | 0 | 0 | 16 | 15 |
| independent raw-bytes (no JSON parse) | 78 | 78 | 68 | 10 | 0 | 0 | 16 | 15 |

Bucket arithmetic checks out: sum of per-row vote counts = 146 =
68×2 + 10×1; per-voter distinct-hash counts sum to the same 146
(13 voters × 10 + 2 voters × 8 + 1 voter × 0).

## 3. Falsification passes

### 3a. Does the grammar drop or invent votes? (raw scan)

A parser-free scan of all 64 captured outputs for every occurrence of the
`RECHECK <hash12> <word>` token shape, compared per hash against the bound
set:

```
ledger_hashes=78 unique=78
DIVERGENT_HASHES=0
RAW hashes outside the ledger: 0
votes cast by NON-recheck seats (any seat other than Mo55Rc01..16): (none)
occurrence multiplicity (same voter, same hash, >1 occurrence): count=0
words used by any raw vote (whole wave): ['holds']
```

So: no vote is lost to the fence/anchor/grammar rules, no prose mention is
mistaken for a vote, no off-ledger hash is voted on, and no non-voter seat
emits a vote token. The 26 outputs that contain the literal string "RECHECK"
include 11 non-voters whose only mentions are prose (e.g. a `role` field saying
"critic non-voter (no ENTAIL/RECHECK/REPLACE/QUOTE lines emitted)") — the
binder correctly ignores all of them.

Vote-bearing JSON scalars in the real captures: **151 single-line, 0
multi-line**, and 0 vote lines sit inside a multi-line scalar that the
whole-scalar anchor would miss. That is why `linewise` and `toolish` agree
here.

### 3b. Why the round-55 counter reads `voted=0` — and is "shape the whole difference" true?

Root cause reproduced mechanically. The round-55 counter
(`.ufo/waves/round-55/count-c1.py:295-303`) takes the vote from the voter's
**report file** and then requires the **captured output** to contain the same
line, compared as an exact stripped line:

```
stripped captured line = '"RECHECK 7b2d297eec60 holds",'
== "RECHECK 7b2d297eec60 holds"                 -> False
startswith "RECHECK 7b2d297eec60 holds "         -> False
```

The JSON quoting plus the trailing comma defeats both the `==` and the
`startswith` test, so **every** seat's vote is unbound → `voted=0`. The
counter's own code comment says this and the round-55 lesson records it.

I ran the round-55 binding logic (unchanged, reimplemented from its source)
against two shapes of the same vote content:

```
r55 logic on JSON-shaped captures    r55-predicate voted=0  dissent=0
r55 logic on PLAIN-TEXT captures     r55-predicate voted=68 dissent=0
```

**The shape is the whole difference between `voted=0` and `voted=68`, but it is
NOT the whole difference between `voted=0` and `voted=78`.** The round-55
predicate additionally requires **≥2 agreeing bound voters per row**
(`count-c1.py:402`, `len(agree) >= MIN_VOTES`), and 10 rows have exactly one
voter. Under the round-55 metric the same committed bytes would score
`voted=68` even with the shape fixed. `count-c2.py:16` asserts "the binding
shape is the whole difference"; that is true of the 0-vs-68 gap but overstates
the 0-vs-78 gap. The residual 68-vs-78 gap is the dispatch-coverage gap the
contract already lists as still-planned ("the dispatch-coverage validator (≥2
voters per scoped row) stays planned").

Contrast arm re-verified at the freeze tip:

```
python3 .ufo/waves/round-55/count-c1.py 8be2717b0809281d07dffe83dad424a4859e0747
C1=unmet scope=78 rows=78 matched=78 status_ok=78 line_ok=78 source_rows=ok pins=ok
provenance=ok same=69 moved=7 changed=2 broken=0 holds=78 stale=0 voted=0 dissent=0
rev=8be2717b0809281d07dffe83dad424a4859e0747 failed=votes
exit=1
```

### 3c. Where the 10 single-voted rows come from

The round-55 dispatch assigned every row to a **pair** of seats with identical
row lists. Recovered from `.ufo/waves/round-55/w1-plan.json` (per-seat 12-hex
row lists) and confirmed against the bound votes:

| pair | rows | bound votes per row |
|---|---|---|
| Rc01+Rc02, Rc03+Rc04, Rc05+Rc06, Rc07+Rc08, Rc09+Rc10, Rc11+Rc12 | 10 each = 60 | 2 (double) |
| Rc15+Rc16 | 8 | 2 (double) |
| **Rc13 (+Rc14 lost)** | 10 | **1 (single)** |

`Mo55Rc14` has no report file at `.ufo/waves/round-55/w1/` (all other 15 Rc
reports exist), its captured output contains no "RECHECK" token and no 12-hex
token at all (it is a prose fragment, 1055 bytes), and the tool's docstring
names it as the lost seat. So `single=10` is an honest surfacing of a lost
seat, not a binding failure — exactly what the contract says the binder was
built to do ("surfaces single-voted rows honestly instead of zeroing the arm").

### 3d. Metric semantics: `agree` vs round-55 `voted`, and `dissent`

**`agree` is not the same metric as round-55 `voted`.** The tool counts a row as
agreeing when *all* of its votes agree with the ledger disposition and there is
**≥1** vote; the round-55 counter requires **≥2** agreeing bound votes. So the
frozen `agree=78` includes the 10 single-voted rows. Recomputed under round-55
semantics over the *same* votes the binder finds: `voted=68`, `dissent=0`.

Consequence: `agree=78` must not be read as "78 rows were quorum-verified".
68 rows were; 10 rows rest on one voter.

**`dissent` is not the same metric as round-55 `dissent`, and this one can
hide a unanimous wrong wave.** The tool's dissent counts rows where the voters
disagree **among themselves** (more than one distinct word). The round-55
counter's dissent counts rows where any voter's word **differs from the
ledger disposition**. Probes:

```
one voter, voting AGAINST the disposition:
  TALLY rows=78 agree=0 double=0 single=1 zero=77 dissent=0 voters=1 bound_voters=1
  (round-55 semantics on the same bytes: dissent=1)

16 voters unanimously voting "stale" against a "holds" disposition:
  TALLY rows=78 agree=0 double=1 single=0 zero=77 dissent=0 voters=16 bound_voters=16
  (round-55 semantics on the same bytes: dissent=1)
```

So a wave in which every voter is wrong on a row can still print `dissent=0`.
On the frozen round-55 bytes this is inert — all 78 dispositions are `holds`
and every raw vote word in the wave is `holds`, so there is nothing to
disagree about — but `dissent=0` is a weaker statement than it looks, and the
C2 predicate reads it as part of the target line.

### 3e. Robustness / shape-invariance probes (limits, not falsifications)

1. **JSON channel is stricter than the text channel.** The JSON channel anchors
   the vote at the *start* of a scalar; the text channel scans line by line.
   Same bytes, two shapes:
   ```
   "note:\nRECHECK a6e5226259c9 holds"      as TEXT  -> bound
                                               as JSON  -> NOT bound
   ```
   Also a JSON scalar whose vote is followed by ≥2 further lines fails to bind
   (the anchored pattern cannot span the newlines), while the same content as
   text binds. Impact on this dataset: **zero** (all 151 vote-bearing scalars
   are single-line; `linewise` and `toolish` tables are identical).
2. **Shape-invariance of the whole pipeline.** Re-emitting the same vote
   content in four different envelopes gives the same tally for three of them:
   ```
   plain-text          TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15
   json-array          TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15
   json-nested         TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15
   json-string-scalar  TALLY rows=78 agree=0  double=0  single=0  zero=78 dissent=0 voters=16 bound_voters=0
   ```
   The JSON **string-scalar** document shape (one scalar holding all vote
   lines) binds nothing — a direct consequence of probe 1. The seat brief's
   "plain-text and JSON string-scalar shapes" therefore holds for
   *per-vote* string scalars inside a JSON document (the real round-55 shape:
   a `vote_lines` array), but a document that is a single JSON string
   containing many vote lines binds zero. Not triggered here.
3. **`ENTAIL` cannot be tallied at all.** `read_ledger` only assigns a
   disposition word when `verb == "RECHECK"` (`mori-vote-bind.py:152`), so an
   ENTAIL ledger reads empty:
   ```
   read_ledger(ENTAIL) -> {}
   read_ledger(RECHECK) -> {'aaaa…': 'entailed', …}
   ENTAIL tally on an ENTAIL-shaped ledger -> TALLY rows=0 agree=0 … bound_voters=5
   ```
   The tool's own docstring claims "ENTAIL tables share the same trailing
   shape here"; the code does not implement it. The round-55 ENTAIL arm
   (12 seats, `Mo55En01..12`) therefore cannot be re-bound by this tool.
   C2's predicate is RECHECK-only, so the frozen claim is unaffected.
4. **Ledger column position is hardcoded.** `read_ledger` reads the
   disposition from cell index 6. A ledger with the disposition moved reads the
   wrong cell (`agree=0` where `agree=1` is correct). The frozen ledger has
   `disposition` at index 6, and my counter derived the same index from the
   header, so no impact here.
5. **Ledger row edge cases.** An empty disposition cell drops the row entirely
   (`rows=2` for a 3-row ledger); a duplicated hash collapses to one row
   (`rows=1` for 2 rows). The round-55 counter flags both (`dup`/`extra`); this
   tool does not.
6. **`--min N` is accepted but inert.** `min_votes` is stored in the returned
   dict and never used to select rows (`--min 3` and `--min 5` produce the same
   line as `--min 2`).
7. **`--disposition-cols N` is documented in the usage docstring but is not an
   argparse option** → argparse error, exit 2.
8. **Roster widening is silent.** Omitting `--voter` makes the roster all 64
   outputs (`voters=64 bound_voters=15`, same four totals); adding a
   non-voter makes `voters=17`. The four totals are roster-insensitive here
   because no non-Rc seat casts a vote.
9. **Counter matching is substring, not exact-line.** `count-c2.py:96` uses
   `EXPECT_TALLY not in p.stdout`, so trailing text after the target line would
   still pass; the control arm at `:108` checks `zero=78` / `double=0` as
   substrings too. The tool itself prints exactly one line, so no impact.
10. **Do-nothing control reproduced.** A junk-output results file (17 junk
    outputs, no vote surface) tallies `rows=78 agree=0 double=0 single=0
    zero=78 dissent=0 voters=16 bound_voters=0`, matching the C2 control arm.

## 4. What I did not verify

- UNVERIFIED: whether the 78 ledger dispositions are themselves correct against
  v7.3 sources — that is the C1 recheck arm, not this seat's scope. I verified
  only that the binder's *agreement* with the ledger is what it claims.
- UNVERIFIED: whether any non-Rc seat in round 55 cast a vote in a surface
  other than its captured output (e.g. only in its report file). The binder's
  binding unit is the captured output by design; I checked the report files
  for the 15 present Rc reports and each carries the same 10/8 vote lines the
  binder found (146 report votes, 146 bound votes — same set).
- UNVERIFIED: the round-55 ENTAIL arm's numbers (this tool cannot read an
  ENTAIL ledger; see 3e.3).

## 5. Host / tooling notes

- No installs were needed or performed. Tooling used: system `python3` and
  `git` only, both pre-existing; no pacman, no uv, no new binaries, no writes
  to `~/.local/bin` or any PATH directory.
- Read-only on the lane repo: `git log/show/diff/rev-parse/ls-files/status`
  only. No `add`/`commit`/`stash`/`checkout`/`reset`/`pull`/`push`, no mutating
  `jj`, no writes to any tracked lane file.
- Scratch: `/fast/scratch/hyaku/mori-r56/Mo56ExecBinderTally/` with
  `TMPDIR=/fast/scratch/hyaku/mori-r56/Mo56ExecBinderTally/tmp`; removed on
  exit. No fixture git repo was created (no commit of any kind was needed).
- `disk-guard.sh status` was consulted before the runs; `/fast` had 587 G free.
- Host reads only; no process, service, cgroup or sysctl was touched.
- No credential, session or private-URL material appears in this report.

## Findings

| # | severity | finding | file / line |
|---|---|---|---|
| 1 | MED | `dissent` counts only *inter-voter* disagreement, so a wave where every voter is wrong prints `dissent=0`. Probe: 16 unanimous `stale` votes against a `holds` disposition → `dissent=0`; round-55 semantics on the same bytes → `dissent=1`. Inert on the frozen bytes (all 78 dispositions and all raw vote words are `holds`), but the frozen target line reads `dissent=0` as if it were a stronger guarantee. Named limit + routed item for round 57 (counter frozen; no change proposed here). | `tools/mori-vote-bind.py:186-196` (tally dissent branch) vs `.ufo/waves/round-55/count-c1.py:388-390` |
| 2 | MED | `agree` ≠ round-55 `voted`: the tool counts a row as agreeing with ≥1 agreeing vote, the round-55 counter required ≥2 agreeing bound votes. Same bytes → tool `agree=78`, round-55 metric `voted=68`. The 10 extra rows rest on a single voter (`Mo55Rc13`, paired seat `Mo55Rc14` lost). `agree=78` must not be read as "78 rows quorum-verified". | `tools/mori-vote-bind.py:186-196` vs `.ufo/waves/round-55/count-c1.py:388-392` |
| 3 | MED | The C2 counter's contrast rationale "the binding shape is the whole difference" overstates: with the shape fixed the round-55 metric scores `voted=68`, not 78, because its ≥2-voter rule still fails on the 10 single-voted rows. The residual 68-vs-78 gap is the dispatch-coverage gap the contract lists as still-planned. | `.ufo/waves/round-56/count-c2.py:15-16`; contract.md "Carried planned item" |
| 4 | MED | The `ENTAIL` arm of the binder cannot read an ENTAIL ledger: `read_ledger` only fills the disposition cell when `verb == "RECHECK"`, so any ENTAIL ledger tallies `rows=0`. The docstring claims ENTAIL tables share the same shape. The round-55 ENTAIL arm (12 seats) is therefore not re-bindable by this tool. | `tools/mori-vote-bind.py:144-158` (read_ledger), docstring line ~40 |
| 5 | LOW | JSON channel is stricter than text channel: a vote must start a scalar, and a scalar with the vote followed by ≥2 further lines does not bind at all. A document that is one JSON string holding many vote lines binds **zero** votes (`zero=78`). Not triggered on this dataset (151/151 vote-bearing scalars are single-line). | `tools/mori-vote-bind.py:78-104` (extract_votes) |
| 6 | LOW | Ledger parsing is positional and lossy: disposition read from hardcoded cell index 6 (a reordered ledger reads the wrong cell); an empty disposition cell drops the row (`rows` shrinks); a duplicated hash collapses to one row. The round-55 counter flags dup/extra; this tool does not. | `tools/mori-vote-bind.py:144-158` |
| 7 | LOW | `--min N` is accepted but never used to select rows; `--disposition-cols N` is documented in the usage docstring but is not an argparse option (exit 2 on use). | `tools/mori-vote-bind.py:161,202,418,438`; docstring line ~45 |
| 8 | LOW | Counter arm matching is substring-based, so a tool that printed the target line plus trailing content would still satisfy the predicate; the do-nothing control is likewise substring-matched. | `.ufo/waves/round-56/count-c2.py:96,108` |
| 9 | LOW | Tool-internal vs ledger-relative `dissent` divergence is invisible to the `agree` counter: with a lone dissenting voter the row reads `single=1 dissent=0 agree=0` — correct on `agree`, blind on `dissent` (same root as #1). | `tools/mori-vote-bind.py:186-196` |
| 10 | INFO | The 10 single-voted rows are fully explained and are NOT a binder defect: they are `Mo55Rc13`'s 10 assigned rows whose paired seat `Mo55Rc14` was lost (no report file; captured output carries no vote token and no 12-hex token). The tally surfaces this honestly, as the contract intended. | `.ufo/waves/round-55/w1-results.json` (Mo55Rc14 record); `.ufo/waves/round-55/w1-plan.json` (per-seat row lists) |
| 11 | INFO | No falsification of the frozen C2 line: three independent counters (JSON-aware, line-wise, raw-bytes) reproduce `rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15` exactly; the raw scan finds 0 dropped and 0 spurious binds; inputs are byte-identical at 3f494b49 / 8be2717b / HEAD / worktree; `count-c2.py 8be2717b` → `C2=met`. | `.ufo/waves/round-56/evidence/tally-r55.txt`; `tools/mori-vote-bind.py:161-202` |

C2 is **not falsified** by this seat. The falsifiable part of the claim
reproduces from the committed bytes under three independent readings; the
remaining objections are metric-semantics limits (findings 1-4), routed to
round 57, with no proposal to change the frozen C2 counter, predicates or
controls.

Report: .ufo/waves/round-56/w1/Mo56ExecBinderTally.md
