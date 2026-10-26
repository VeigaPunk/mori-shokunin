# Mo50bRevC1Counter — line-by-line review of `.ufo/waves/round-50/count-c1.py` (wave a2w1)

Seat: Mo50bRevC1Counter (reviewer, leaf — no subagents). MACHINE_ID: 432d02b544a5459ebbff9c42ec68334d
Date: 2026-10-26. Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin`. Fleet root: `/home/vgpnk/Projects/shokunin`.

Scope: the frozen C1 counter `count-c1.py` (481 lines) — `manifest_targets()`, `axes_table()`,
`check_axes()`, `parse_shonen()`/PIN/HIDDEN, `bound_path()`, `run()` archive extraction, exit codes,
and the 34 selftest arms tested by mutation. Read-only everywhere; scratch
`/fast/scratch/hyaku/mori-r50/Mo50bRevC1Counter/` (removed before this report was written; all cited
output is reproduced inline). No pacman use; no tool installs (none needed). No kernel log read; no
config change; no OOM triggered.

## 0. Bytes verified frozen; real runs reproduced

```
$ sha256sum .ufo/waves/round-50/count-c1.py
2d5c3ee53198124ef001908cc5abba5c71a6fb63773c31ece211b7c6cdae4456  .ufo/waves/round-50/count-c1.py
$ grep count-c1 .ufo/waves/round-50/evidence/freeze-sha256.txt
2d5c3ee53198124ef001908cc5abba5c71a6fb63773c31ece211b7c6cdae4456  .ufo/waves/round-50/count-c1.py
```
Working tree == frozen bytes (HEAD is 4548a34d, later than the landed data rev; the reviewed bytes are
the frozen ones either way).

```
$ python3 .ufo/waves/round-50/count-c1.py --selftest          → C1_SELFTEST pass=34 fail=0, rc=0
$ python3 .ufo/waves/round-50/count-c1.py 487941b9395e89678af0053cc443cdb49cdee6e3 --scratch <scratch>
C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=487941b… rc=0
$ python3 .ufo/waves/round-50/count-c1.py 7197160b927f04db294c9553fb48fadcc7a3f4e3 --scratch <scratch>
C1=unmet items=8 axes=6 pins=2 boxes=4 mismatches=6 errors=0 hidden=0 manifest=a94551c5bc8d rev=7197160b… failed=mismatch rc=1
```
The entering run reproduces the frozen control receipt (`evidence/control-c1-do-nothing.txt`,
`manifest=a94551c5bc8d`, mismatches=6) item for item: coverage round=26 vs 47, operability round=31
vs 47, depth round=31 vs 49, calibration round=25 vs 49 (each also `evidence_missing` for the round-47/49
spot files), freshness and adjacency ok, pins `(60/60)` vs `PIN_CHECK_SELFTEST pass=114 fail=0` and
`(13/13)` vs `UNLANDED_SELFTEST pass=17 fail=0`.

Real-data cross-checks at the landed rev (all consistent with the counter's `ok` verdicts):

- Fleet `MANIFEST.json` at `e0144996…`: 38 mori entries; **zero duplicate `lane_round`s**; every
  `lane_round` an int; verdict values only `admitted` / `rejected-harmed` / `rejected-honest-stop`.
  Resolved targets: coverage 47, operability 47, depth 49, freshness 28, calibration 49, adjacency 19 —
  exactly the counter's `expect=` lines. Round 36's extra key `freshness-technique` is correctly ignored
  (not in AXES).
- `SHONEN.md` at R: 4 boxes `- [~]`, two fraction pins `(114/114)` and `(17/17)`, receipt paths named;
  `hidden=0` is right — the only tally-adjacent text outside the pins is lowercase `selftests/…` in
  receipt paths, and HIDDEN's `SELFTEST` alternative is case-sensitive.
- Receipts at R: `…/selftests/mori-pin-check.txt` line 116 `PIN_CHECK_SELFTEST pass=114 fail=0`;
  `…/selftests/mori-unlanded-check.txt` line 19 `UNLANDED_SELFTEST pass=17 fail=0` — the exact stripped
  lines `has_receipt` requires.
- Spot files at R: round-19 ABSENT (so adjacency correctly requires `MANIFEST.json`, and its Evidence
  cell contains `MANIFEST.json@63729047`), rounds 25/26/28/31/47/49 exist.
- All six real Last-change cells lead with the space form `round N` equal to the target; every
  `round-37`/`round-38`/`round-50` reference sits **after the first `;`** (freshness segment 2,
  operability segment 3, calibration segment 3) and is correctly ignored by the first-token rule.

So the counter's verdict on the real data is sound. Everything below is edge-case behaviour and
selftest coverage; none of it flips the current C1 verdict.

## 1. Function-by-function review

### manifest_targets() — lines 63–77

- Line 68 filters `lane == "mori"` and `verdict == "admitted"`; line 72 cuts `n > 49` and requires
  `verdicts` to be a dict; line 75 takes `improved`/`harmed` grades. All per contract P-C1(a).
- Line 70 `n = r.get("lane_round", r.get("round"))`: the fallback fires only when the KEY IS ABSENT.
  An entry with `"lane_round": null` and a valid `"round"` is silently dropped (`.get` returns None,
  line 72 skips it) — fail-safe direction (a missing target → `manifest_has_no_target` error → unmet),
  but the fallback is narrower than "lane_round vs round fallback" reads. Real MANIFEST has no nulls.
- Line 75 tie-break `n >= best…`: for two qualifying entries with the SAME `lane_round`, the last one
  in the JSON array wins — order-dependent (demo D8 below). No arm covers duplicates.
- Line 64 `json.loads` is uncaught here; called from `evaluate()` (line 210) inside the `try` at line
  317 that has only a `finally` — a malformed MANIFEST crashes with exit 1, not the documented setup
  exit 2 (Finding 2, demo D7).
- Mutation teeth: through cut mt3 → 12 arms fail; lane filter mt4 → 11; harmed grade mt5 → 8;
  `lane_round` preference mt7 → arm crash (KeyError); **admitted filter mt1 → NO arm fails** (Finding 1);
  tie-break mt6 → NO arm fails; type guards mt8/mt9 → NO arm fails.

### axes_table() — lines 80–107

- Heading: line 87 `^## Axes\s*$` exact, only when not in a fence (lines 84–86 toggle on any
  ```/~~~ line). `## Axes (old)` → no table → all six axes `no_axes_table` mismatch (arm
  `heading_renamed_unmet` has teeth, at1; fence arm `table_in_fence_unseen`, at2/at8). Only the FIRST
  non-fenced `## Axes` is used; a later duplicate table is ignored (per contract "the `## Axes` table").
- Header: line 102 requires exactly `["axis","score","evidence pointer","last change"]` lowercased —
  column order or wording changes → no table (at3 → 12 arms fail). Strict, per contract.
- Rows: line 96 accepts 0–3 leading spaces before `|`; line 105 skips separator rows only when EVERY
  cell is `:?-{3,}:?` (a 1-dash separator would be appended as a data row — harmless: its first cell
  can never equal an axis name, and the row count is discarded at line 211). `split_cells` (56–60)
  keeps escaped `\|` inside cells.
- **Fence state is not tracked while scanning rows** — only while finding the heading. `|`-looking
  lines inside a fence between the header and the first row would be parsed as rows. Real data
  unaffected (the table is followed by prose, which breaks the scan). LOW (Finding 8).
- Termination: line 94 (`#` stop) is shadowed by lines 96–98 (first non-`|` line after the first row
  breaks) whenever a row exists — the `#` stop only matters for a `#` line between header and first
  row. Both breaks are unguarded by any arm (at4, at5 → NO arm fails). LOW (Finding 8).

### check_axes() — lines 111–146

- Line 123 matches the axis name with `.strip("* ").lower()` (bold tolerance); line 124 requires
  exactly one row; line 128 exactly 4 cells. Teeth: ca10 (cells≠4) → 10 arms; ca12 (row-count check
  dropped) → arm crash IndexError at line 127; ca9 (bold strip dropped) → NO arm fails.
- Line 132 round regex `\bround[ -]?(\d+)\b` (re.I): matches `round 47`, `Round 47`, `round-47`, and
  `round-47` **inside a path** (`round-47-verifier-spotcheck.md` → 47); matches inside `pre-round 5`;
  does NOT match `rounds 47` or `round 47th` (strict). The hyphen branch is untested by the selftest
  (ca1 → NO arm fails; ca2 hyphen-only → 7 arms fail, so the space form is guarded). The
  `round-37 C2` hazard: a cell LEADING with `round-37 C2 …` is measured as round 37 (demo D10). The
  real cells keep such references after the first `;`. LOW (Finding 7).
- Line 134 `seg = last[m.start():].split(";")[0]` — the verdict-word segment is the text from the
  first `round` token to the next `;`, per contract. ca3 (last segment instead) → 6 arms fail.
- Line 140 verdict check `verdict not in seg.lower()` is a SUBSTRING test: `unimproved` contains
  `improved`, `not improved` contains `improved` — both pass (demo D9). ca4 (check dropped) →
  `verdict_word_wrong_unmet` fails, so the check's presence is guarded; its substring weakness is not.
  MED (Finding 4).
- Lines 135–136 + 142: the required evidence is `corpus/lessons/round-<n>-verifier-spotcheck.md` when
  it exists at R, else `MANIFEST.json` — keyed to the MANIFEST target `n` (correct per contract).
  Mutating it to the cell's round `got_n` leaves the suite green (ca7b → NO arm fails). MED (Finding 5).
  The evidence check itself is a substring test over the Evidence cell (line 142) — `MANIFEST.json@…`
  satisfies `MANIFEST.json`; ca5 (checked against the Last-change cell instead) → 6 arms fail.
- Line 138 round equality guarded (ca8 → 2 arms fail). A missing SCORECARD → `no_axes_table` mismatch
  ×6 (unmet, not error) — correct direction.

### parse_shonen() and the regexes — lines 43–53, 149–159

- BOX (line 53) `^\s*[-*] \[[ ~xX]\]`: counts `[ ]`, `[~]`, `[x]`, `[X]` (done boxes count —
  consistent with "keeps at least 4 checklist boxes"); `[*]` not counted. Dropping `~` → honest_met
  fails (ps1); dropping `x`/`X` → NO arm fails (ps2, all fixture boxes are `[~]`).
- PIN (lines 49–51): backticked span containing `--selftest`, directly followed on the SAME line by
  `(N/M)` or `→`/`->` + backticked `PREFIX pass=N fail=K`. Per-line processing (line 151) means a
  fraction on the next line is NOT a pin (the docstring's "split across lines" limit holds). A
  whitespace-variant fraction `( 114/114 )` is NOT a pin but IS hidden (HIDDEN allows inner spaces,
  PIN does not) — conservative direction. Both alternatives guarded (ps3b/ps4b → honest_met +
  stale_*_pin_unmet fail; the naive group-dropping variants crash the harness unpack at line 178 —
  detection via crash).
- HIDDEN (line 52): after `PIN.sub` (line 157) removes well-formed pins, any remaining `(N/M)`,
  `pass=\d+`, or `SELFTEST` (case-sensitive, also inside `X_SELFTEST`) counts. Teeth: fraction ps6,
  SELFTEST ps5b, PIN.sub removal ps8 — all detected. The `\bpass=\d+` alternative is untested
  (ps7b → NO arm fails). A bare `114/114` without parens or a bare `fail=0` is not a hidden token —
  matches the contract's two token forms (named limit, already in the docstring).

### bound_path() — lines 162–172

- Line 167: exactly 3 argv, `python3`, `--selftest` (extra args/other interpreter/quoted variants →
  unbound). shlex dequotes, so `` `python3 "tools/a.py" --selftest` `` binds to `tools/a.py` — the
  bound path equals the quoted path's target; benign.
- Line 170: rejects absolute paths, any `..` component, non-`.py`. Teeth: dotdot bp2 (sole arm
  `bound_path_dotdot`), argc bp3, interpreter bp4, happy path bp6 (11 arms). **The absolute-path check
  is NOT isolated**: deleting `p.startswith("/")` leaves 34/34 (bp1) because the harness `exists()`
  misses `/abs/tools/a.py` anyway — `absolute_path_unbound` (line 449) passes for the wrong reason.
  In the real counter the removal is doubly masked: git rejects `rev:/path` outright
  (`git cat-file -e <rev>:/SCORECARD.md` → rc 128, demo D11), so `exists()` would be False regardless.
  Defense-in-depth whose absence no arm would notice. LOW (Finding 9). The `.py` check is also
  untested (bp5 → NO arm fails).

### check_pins() — lines 175–200

- Line 186: run failure/timeout/no-tally → `error` (guarded, cp5). Line 191 fraction form `M = P+F`
  (guarded, cp3); line 193 token form requires prefix+pass+fail equality (guarded, cp4 —
  `prefix_mismatch_unmet` fails when the prefix check is dropped). Line 194 stem = basename minus
  `.py` (guarded, cp6). Line 196: the receipt must contain the observed `PREFIX pass=P fail=F` as an
  exact stripped LINE; dropping the content check → `receipt_other_tally_unmet` fails (cp1); dropping
  the None check → arm crash (cp8); relaxing exact-line to substring → NO arm fails (cp2). LOW
  (Finding 11).
- Two tools sharing a basename in different directories would share one receipt file — no arm, exotic.

### evaluate() — lines 208–241

- Floors and failure reasons all guarded: mismatch ev1 (21 arms), errors ev2, hidden ev3, pins floor
  ev4/ev6, boxes floor ev5/ev7, `met` flag ev8 (26 arms).
- Line 229 `if sum(1 for i in axis_items) != len(AXES)` is DEAD: `check_axes` appends exactly one item
  per axis on every path (lines 114–145), so the `axes` failed-reason is unreachable (ev9: removing the
  line leaves 34/34). LOW (Finding 16).
- `hidden` fails the claim (line 223) — consistent with the printed `hidden=0` target.

### run() — lines 294–315 (selftest-blind: the selftest's runner is a mock, line 388)

Verified behaviourally on fixture repos (D1–D6):

- Archive extraction (299–303): `git archive rev | tar -x -C tree`; failure of either → `None` →
  `no_tally_or_timeout` error. A failed extraction leaves a PARTIAL tree that is not removed in
  `--scratch` mode (the finally removes only `state["tree"]`, lines 320–323, which stays None on
  failure) and a retry re-extracts over the stale dir without clearing it; a PID-reused base
  (line 291) after a kill -9 could mix two revs' trees. Exotic (rev fixed per invocation). LOW
  (Finding 13).
- TMPDIR (line 305): the pinned tool's temp writes land in `<scratch>/tmp` (demo D1 marker file);
  deleting the override lets them fall through to the inherited TMPDIR (D4). No arm covers either.
- Timeout (line 308): `--timeout 2` against a 31 s tool → error item at 2.1 s, rc=1, and NO orphan
  child (subprocess.run kills on TimeoutExpired — verified). Deleting the timeout arg → the counter
  waits for the full 31 s (killed by an outer guard in the demo). No arm covers this.
- Last-tally rule (line 314 `found[-1]`): a tool printing `L_SELFTEST pass=113 fail=1` then
  `L_SELFTEST pass=114 fail=0` is measured as 114/0 (D1, met); mutating to `found[0]` measures 113/1 →
  mismatch (D3). Load-bearing, zero arm coverage.
- Interpreter: line 307 runs `sys.executable`, not the literal `python3` from PATH — fidelity gap vs
  the pin text. LOW (Finding 14).

### main() and exit codes — lines 248–327

Verified: rc 0 met (landed rev), rc 1 unmet (entering tip), rc 2 setup for a bad rev
(`C1_SETUP cannot resolve rev`), rc 2 for a missing option value (`C1_SETUP missing value for
--repo`), rc 2 when the default fleet dir (the lane's parent) is not a git repo
(`C1_SETUP cannot resolve manifest`). `--selftest` alone → selftest; `--selftest x` → usage rc 2.

- **Malformed MANIFEST.json → traceback, rc 1** (JSONDecodeError from line 64), not the documented
  setup exit 2 — the fetch is guarded (lines 267–273) but the parse is not. MED (Finding 2, demo D7).
- The cleanup `finally` (319–323) runs on the crash path too: after the malformed-MANIFEST crash, no
  `count-c1-r50-*` dir remained in TMPDIR (verified). In `--scratch` mode only `tree` is removed and
  `tmp` is left for the caller — per the scratch contract.
- Mutating line 327 to `return 0` makes the counter print `C1=unmet …` and exit 0 on the real entering
  tip (demo D7) — the exit-code line is load-bearing for the kill rule and has zero arm coverage.

## 2. The 34 selftest arms under mutation

Method: one mutation per run on a scratch COPY of the frozen counter (`--selftest` is pure
in-memory; the frozen file was never modified). 66 mutations applied (4 more first skipped on ambiguous
old-strings, all 4 re-run with fixed old-strings). Baseline 34/34. Result: **39 detected by clean arm failures, 6 detected
only by an arm crashing (rc≠0, no tally line), 21 detected by NO arm** (suite stays green, pass=34).

Detected cleanly (mutation → failing arms, abridged): through-cut mt3 → 12 arms; lane filter mt4 → 11;
harmed grade mt5 → 8; heading at1 → heading_renamed_unmet; heading fence at2/at8 →
table_in_fence_unseen; header cells at3 → 12; round-regex space form ca2 → 7; seg-last ca3 → 6;
verdict-check drop ca4 → verdict_word_wrong_unmet; evidence-vs-last ca5 → 6; need-always-spot ca6 → 5;
round-equality drop ca8 → 2; cells≠4 ca10 → 10; cell swap ca11 → 7; box-tilde ps1 → honest_met;
HIDDEN fraction ps6 / SELFTEST ps5b / PIN.sub ps8; PIN fraction alt ps4b → 12; PIN token alt ps3b → 4;
dotdot bp2 → bound_path_dotdot; argc bp3 → extra_args_unbound; interpreter bp4 →
other_interpreter_unbound; happy path bp6 → 11; receipt content cp1 → 2; fraction-sum cp3 →
honest_failing_pin_needs_receipt; token prefix cp4 → prefix_mismatch_unmet; error-vs-mismatch cp5 →
runner_error_counts; stem cp6 → 6; exists check cp7 → missing_tool_unbound; ev1–ev8 as above.

Detected only via arm crash: mt2 (admitted filter inverted → KeyError 'freshness' at line 401),
mt7 (lane_round preference dropped → KeyError 'calibration' at line 399), ca12 (row-count check
dropped → IndexError at line 127), cp8 (receipt None-check dropped → AttributeError at line 196),
ps3/ps4 (naive group-dropping variants → ValueError unpack at line 178 — driver artifact, superseded
by the arity-preserving ps3b/ps4b which detect cleanly).

**The 21 mutations NO arm detects** (each leaves `C1_SELFTEST pass=34 fail=0`):

| # | mutation (guard deleted/changed) | line | why the suite stays green |
|---|---|---|---|
| 1 | `verdict != "admitted"` → accept ALL verdicts | 68 | fixture round 45's grades (calibration harmed, depth improved) are superseded by admitted round 49 either way; `rejected_round_ignored` (399) asserts only the final value |
| 2 | duplicate tie-break `>=` → `>` | 75 | the fixture manifest has no duplicate `lane_round` |
| 3 | `isinstance(v, dict)` guard dropped | 72 | all fixture verdicts are dicts |
| 4 | `isinstance(n, int)` guard dropped | 72 | all fixture rounds are ints |
| 5 | `#` stop removed | 94 | shadowed by the non-\| break (96–98) once a row exists |
| 6 | non-\| break removed | 97 | the `#` stop still ends the scan at `## Move log` in the fixture |
| 7 | separator `-{3,}` → `-{1,}` | 105 | fixture separator is `---`; a bogus separator row can never match an axis name and the row count is discarded (211) |
| 8 | row indent `^ {0,3}\|` → `^\|` | 96 | fixture rows sit at column 0 |
| 9 | round regex `[ -]?` → space-only | 132 | every fixture cell uses the space form |
| 10 | spot file keyed to the CELL's round (`got_n`) instead of the MANIFEST target (`n`) | 135 | no arm has a cell whose round differs from the target AND cites the wrong round's spot |
| 11 | bold-marker strip dropped | 123 | no fixture axis name is bold |
| 12 | `[x]`/`[X]` dropped from BOX | 53 | all fixture boxes are `[~]` |
| 13 | HIDDEN `\bpass=\d+` alternative dropped | 52 | no arm's stray token is a bare `pass=` |
| 14 | absolute-path guard dropped | 170 | `absolute_path_unbound` (449) passes because the harness `exists()` misses the path anyway |
| 15 | `.py` extension check dropped | 170 | no fixture pin names a non-.py file |
| 16 | receipt exact-line match → substring | 196 | fixture receipts contain the exact line, so both pass |
| 17 | dead `axes` failed-reason line removed | 229 | the line is unreachable (check_axes always emits 6 items) |
| 18 | `found[-1]` → `found[0]` (first tally wins) | 314 | the selftest runner is a mock (388); run() is never exercised |
| 19 | TMPDIR override dropped | 305 | same |
| 20 | exit cleanup removed | 321 | same |
| 21 | `return 0 if met else 1` → `return 0` | 327 | main() is never exercised |

Items 1, 10, 14, 16, 18, 21 guard predicate semantics or the kill rule's exit code; the rest are
robustness/parse-tolerance lines whose fixture data never varies. All are named limits for this round
(the bytes are frozen and sha256-pinned); none is proposed as a fix.

## 3. Behavioural demos (fixture repos under scratch; `git -C $D` throughout, toplevel verified)

```
D1  frozen counter, fixture with a two-tally tool + a TMPDIR-marker tool, --scratch S:
    C1=met … rc=0; marker in S/tmp (TMPDIR override works); tree removed after run; tmp kept (caller's)
D2  same, no --scratch: base $TMPDIR/count-c1-r50-<pid> removed on exit (no leftovers); the marker
    went with it (it lived under base/tmp)
D3  mutated found[0]: pin expects L_SELFTEST pass=114 fail=0, tool's FIRST tally is 113/1 →
    got=L_SELFTEST_pass=113_fail=1 state=mismatch rc=1  (last-tally rule is load-bearing)
D4  mutated TMPDIR drop: marker NOT in S/fixC/tmp, IS in the inherited TMPDIR
D5  frozen counter, 31 s tool, --timeout 2 → got=no_tally_or_timeout state=error rc=1 in 2.1 s;
    pgrep finds no surviving tool process
D6  mutated timeout=None: ignored --timeout 2, killed only by an outer 6 s guard
D7  bad rev → rc=2 "C1_SETUP cannot resolve rev"; trailing --repo → rc=2 "missing value for --repo";
    MANIFEST.json="{not json" → Traceback, json.decoder.JSONDecodeError, rc=1 (not 2);
    no scratch leftovers after the crash (finally ran)
D7b mutated exit-always-0 on the REAL entering tip: prints "C1=unmet … failed=mismatch" and exits 0
D8  duplicate entries for lane_round 47: [improved, harmed] → expect=round_47_harmed (last wins);
    [harmed, improved] → expect=round_47_improved; mutated `>` → first wins either way
D9  frozen counter, module import, target (47, improved): cells "round 47 (unimproved)" and
    "round 47 (not improved)" → state=ok; "round 47 (improved, score held)" → ok
D10 cell "round-37 C2 re-attributed here (score held, 7); round 47 (improved)" →
    got=round=37,verdict_word_missing state=mismatch (hyphenated first token is read as the round)
D11 git cat-file -e <rev>:/SCORECARD.md → rc=128 (git rejects leading-slash paths; exists() would
    reject absolute paths even without bound_path's guard)
```

## Findings

All findings concern `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-50/count-c1.py`
(frozen bytes, sha256 2d5c3ee5…). No finding changes the counter's verdict on the real data at
487941b9 (C1=met) or at the entering tip 7197160b (C1=unmet, mismatches=6) — both reproduce the frozen
receipts exactly. Per the round rules these are named limits, not proposed changes.

1. **MED — Selftest cannot detect a broken `admitted` filter** (line 68; arm `rejected_round_ignored`
   line 399). Deleting the guard leaves `C1_SELFTEST pass=34 fail=0` (mutation mt1): the fixture's
   rejected round 45 grades calibration harmed and depth improved, both superseded by admitted round
   49, so no target changes. The arm only reacts to the INVERTED filter — and then by crashing
   (KeyError 'freshness', line 401), not by failing cleanly. A future edit accepting rejected rounds
   would move N* to a rejected round with the suite green. Contained this round by the freeze sha.

2. **MED — Exit-code contract violated on the malformed-MANIFEST path** (line 64 via line 210; the
   `try` at 317 has only a `finally`). `json.loads` failure → traceback, exit 1 — the docstring's
   "1 unmet" class — instead of the documented setup exit 2 (demo D7). The kill rule reads exit 1 as
   unmet. Fetch failures ARE exit 2 (lines 267–273); the parse is not. Not live this round (the fleet
   rev is pinned), but the 0/1/2 contract does not hold on the crash path.

3. **MED — run()/main() have zero selftest coverage** (runner mocked at line 388). The last-tally rule
   (`found[-1]`, 314), the TMPDIR override (305), the archive extraction (299–303), the cleanup
   (320–323) and the exit-code line (327) all pass 34/34 under deletion mutations (items 18–21), and
   the demos show each is load-bearing (D3, D4, D6, D7b, D2). The real runs exercised this path once
   each; there is no arm that would catch a regression.

4. **MED — Verdict-word check is a substring test** (line 140). "round 47 (unimproved)" and
   "round 47 (not improved)" pass for target `improved` (D9); the contract says the segment "names
   N*'s verdict word". The check's PRESENCE is guarded (ca4) but its substring weakness is not.
   Frozen → named limit.

5. **MED — Spot-file requirement keyed to the cell's round under mutation** (line 135). The frozen
   code correctly keys the required evidence file to the MANIFEST target `n`; mutating it to the
   cell's claimed round `got_n` leaves the suite green (ca7b) — no arm distinguishes "evidence names
   N*'s spot" from "evidence names the cell's round's spot".

6. **LOW — Duplicate qualifying entries are order-dependent** (line 75 `>=`; last qualifying wins).
   Demo D8: entries [improved, harmed] → target (47, harmed); reversed → (47, improved); mutation mt6
   (`>`) → first wins. No arm has duplicates. Real MANIFEST at e0144996: 38 mori entries, zero
   duplicate `lane_round`s (verified) — no live impact.

7. **LOW — Hyphenated `round-N` accepted as the round token** (line 132 `[ -]?`). A Last-change cell
   leading with "round-37 C2 …" is measured as round 37 (D10). Real cells keep every such reference
   after the first `;` (verified for all six). Also matches inside `pre-round 5`; does not match
   `rounds 47` or `round 47th`.

8. **LOW — Table-scan termination unguarded and partially shadowed** (lines 94, 96–98, 105; mutations
   at4/at5/at6/at7 all undetected). The `#` stop is shadowed by the non-`|` break once a row exists;
   fence state is not tracked while scanning rows (only while finding the heading), so `|`-looking
   lines inside a fence between header and first row would be parsed as rows. Real data unaffected.

9. **LOW — bound_path's absolute-path and `.py` guards untested** (line 170; bp1/bp5 undetected).
   `absolute_path_unbound` (449) passes via the harness `exists()` miss, not via the guard. In the
   real counter the removal is masked by git's rejection of `rev:/path` (D11, rc 128) —
   defense-in-depth whose absence no arm would notice.

10. **LOW — HIDDEN's `\bpass=\d+` alternative untested** (line 52; ps7b undetected). A bare `fail=0`
    or unparenthesised `114/114` in SHONEN prose is not a hidden token — matches the contract's two
    token forms; named limit (docstring already scopes the hidden scan to SHONEN.md).

11. **LOW — Receipt matching is exact-line and the distinction is untested** (line 196; cp2
    undetected). A receipt carrying the tally with extra text on the same line fails (strict
    direction); relaxing to substring leaves the suite green.

12. **LOW — `--timeout 0` means instant timeout; negative crashes** (lines 253, 307–308). `--timeout 0`
    → every pin `no_tally_or_timeout` error; a negative value → uncaught ValueError from subprocess,
    exit 1. No arm covers either.

13. **LOW — Failed extraction leaves a partial tree; retries and PID reuse can mix trees**
    (lines 291, 296–304, 320–323). In `--scratch` mode the partial tree is not removed on failure
    (`state["tree"]` stays None); a retry re-extracts over the stale dir without clearing; a recycled
    PID's base (no-scratch mode) could mix two revs' trees after a kill -9. Exotic; rev fixed per
    invocation.

14. **LOW — run() uses `sys.executable`, not the pin's literal `python3`** (line 307). Interpreter
    fidelity gap vs the pin text (a venv interpreter could differ from the pinned system python3).

15. **LOW — `exists()` accepts any git object at the path** (lines 288–289): a directory named like
    the spot file would satisfy `exists` (`git cat-file -e` succeeds on trees). Exotic.

16. **LOW — Dead line** (229): `if sum(1 for i in axis_items) != len(AXES)` never fires —
    `check_axes` appends exactly one item per axis on every path (114–145); the `axes` failed-reason
    is unreachable (ev9 undetected, confirming).

17. **INFO — Four mutations detected only by an arm crashing** (mt2/mt7 KeyError, ca12 IndexError at
    127, cp8 AttributeError at 196): detection holds (rc≠0, no tally line) but no clean FAIL line is
    printed.

18. **INFO — Untested tolerances, all consistent with the contract**: BOX counts done boxes
    (`[x]`/`[X]`, line 53; ps2); bold axis names (line 123; ca9); the isinstance type guards
    (line 72; mt8/mt9) — the real MANIFEST is well-formed on all three.

## Residual risk and verification gaps

- I did not audit `count-c2.py` (out of my seat's scope; Mo50bRevC2Counter and Mo50bCritC2Counter hold it).
- The mutation study exercises the selftest harness only; run()/main() behaviour was verified by the
  D1–D11 fixture demos, each run once — not exhaustively (e.g., no demo of a corrupted tar stream, and
  the partial-tree retry-mixing scenario of Finding 13 is code-reading only).
- The verdict-word substring hole (Finding 4) and the duplicate tie-break (Finding 6) are demonstrated
  on synthetic cells/manifests; the real SCORECARD cells and MANIFEST were verified clean against both.
- Scratch `/fast/scratch/hyaku/mori-r50/Mo50bRevC1Counter/` removed (verified). Nothing outside my
  report and scratch was written; no mutating git/jj command anywhere; fixture commits only under
  throwaway identities inside scratch fixtures.
