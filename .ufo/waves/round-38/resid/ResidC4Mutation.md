# ResidC4Mutation — residual falsification of `count-c4.py` at the round-38 tip

Seat: `mori-r38.ResidC4Mutation` (residual falsification, 8-seat call).
Object: `.ufo/waves/round-38/count-c4.py` committed at the scored tip, plus the artifacts it measures
(`corpus/knowledge/source-drift-content-anchor-r38.md`, `SCORECARD.md`, `.ufo/waves/round-37/evidence/drift-live-r37.txt`,
`tools/mori-source-drift.py`). Claim under attack: lesson M14's four discriminators.

## 0. Tip, method, tooling

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse mori
fatal: ambiguous argument 'mori': unknown revision or path not in the working tree.   # no `mori` ref in this lane
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse master
b6993744171a05efc627b5e0664489c31aa5214e
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse --verify b6993744171a05efc627b5e0664489c31aa5214e
b6993744171a05efc627b5e0664489c31aa5214e
$ git -C /tmp/c4attack rev-parse HEAD
b6993744171a05efc627b5e0664489c31aa5214e
```

The assignment's `mori` ref does not exist; `master` and the full 40-hex both resolve to the same
commit, and the clone was detached at the 40-hex. `git show b6993744:.ufo/waves/round-38/count-c4.py
| sha256sum` → `8332341c3901ef09e76bbd7f31e8c8e68b4e4ecc5d3002f2d20201c9e7093ba1`, equal to the freeze
v3 pin (`evidence/freeze-r38-v3.txt:18`). Counter bytes were read from `git show`, never the working tree.

Method: one scratch clone, `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin
/tmp/c4attack`, `git checkout b6993744`, `git status --porcelain` empty. Every mutant is a commit in
that clone on its own branch; the lane repo's tracked bytes were never edited and no lane commit was
made. The counter is invoked exactly as committed, from its committed path in the clone, with
`--repo /tmp/c4attack`; no fixture or counter byte was patched for the four assigned mutants.

Runtimes: Python 3.14.8 (`sys.executable` is the only interpreter the counter uses for the probe
selftest), git 2.56.0. One canonical runtime, no rerouting path exists in this scope. Tools installed:
none. `lsp` device: not exposed to this seat (tool inventory is read/bash/edit/eval/glob/grep/task/
wait/web_search/write), so caller/definition evidence is execution + committed-byte reads; called out
where it matters.

Side effect inside my write scope: `count-c4.py:39,45` hardcodes
`DEFAULT_REPO = "/home/vgpnk/Projects/shokunin/mori-shokunin"` and
`SCRATCH_ROOT = <DEFAULT_REPO>/.ufo/waves/round-38/scratch`; `main` uses it at `:279-280` regardless of
`--repo` (`:233`). Each run therefore created and removed one `scratch/mori-c4-*` dir under the lane.
`find .ufo/waves/round-38/scratch -maxdepth 1 -name 'mori-c4-*' | wc -l` → `0` after the last run.
That the scratch root ignores `--repo` is finding L-3 below.

## 1. Baseline at the landed tip

```
$ cd /tmp/c4attack && python3 .ufo/waves/round-38/count-c4.py b6993744171a05efc627b5e0664489c31aa5214e --repo /tmp/c4attack
negative witness-token-entry        rejected
negative witness-dangling-row       rejected
negative witness-summary-only-live  rejected
check anchors          PASS (anchors=3 missing=[] empty=0 unique=True)
check capability       PASS (paths=['tools/mori-source-drift.py', '.ufo/waves/round-37/evidence/c2-after-v3.txt', '.ufo/waves/round-37/evidence/drift-live-r37.txt'] missing=[])
check live_rows        PASS (named=10 summary_drifted=10 unknown=[] unique=True)
check named_row_drift  PASS (exit=0 row_states=('PASS', ''))
check drift_kill       PASS (exit=1 row_states=('FAIL', "... got [('S103', 'excerpt')] ... want [('S103', 'drifted')] ..."))
C4=met
EXIT=0
```

The tip is honestly `met` on its own bytes. The tool's literal is in the live path:
`tools/mori-source-drift.py:202 def classify`, `:208 return "drifted"`, reached from
`:242 state = classify(body, copy)` in `run()`.

## 2. The four assigned mutants (tip counter)

Each mutant is one commit off `b6993744` in `/tmp/c4attack`; command for every row:
`python3 .ufo/waves/round-38/count-c4.py <branch> --repo /tmp/c4attack`.

### (a) three blank `anchor:` lines — `mu-a` = `a615c479bc4f06b7973f65238cb15e6605df5f1c`

Entry `:26-28` replaced by three lines `   anchor:`.

```
check anchors          FAIL (anchors=3 missing=[] empty=3 unique=False)
check capability       PASS (paths=['tools/mori-source-drift.py', '.ufo/waves/round-37/evidence/c2-after-v3.txt', '.ufo/waves/round-37/evidence/drift-live-r37.txt'] missing=[])
check live_rows        PASS (named=10 summary_drifted=10 unknown=[] unique=True)
check named_row_drift  PASS (exit=0 row_states=('PASS', ''))
check drift_kill       PASS (exit=1 row_states=('FAIL', ... ('S103', 'excerpt') ... ('S103', 'drifted') ...))
C4=unmet
EXIT=1
```

Verdict: **killed at `anchors`**, `empty=3`, exactly as M14 claims. Note `missing=[]` — see L-2.

### (b) duplicate anchor line — `mu-b` = `0f636ef365f60242a5e92452768b29b67c96b142`

Entry gained a second `   anchor: FETCH_MAX_BYTES = 4 * 1024 * 1024` (four anchor lines, one repeated).

```
check anchors          FAIL (anchors=4 missing=[] empty=0 unique=False)
C4=unmet
EXIT=1
```

Other checks `PASS` (same values as (a)). Verdict: **killed at `anchors`**, `unique=False`.

### (c) appended decoy capability row — `mu-c` = `c08f0d89906bc3ed836b7a2d3c32b0c113649eee`

`SCORECARD.md` gained one appended line containing the key and a *resolving* path (so the decoy would
satisfy the pre-fix "last row wins" check):

```
| round-38 decoy | source-drift re-fetch probe | a second row naming the same capability, citing `tools/mori-source-drift.py` | 0 |
```

```
check anchors          PASS (anchors=3 missing=[] empty=0 unique=True)
check capability       FAIL (row absent missing=[])
check live_rows        PASS (named=10 summary_drifted=10 unknown=[] unique=True)
check named_row_drift  PASS (exit=0 row_states=('PASS', ''))
check drift_kill       PASS (exit=1 row_states=('FAIL', ...))
C4=unmet
EXIT=1
```

Verdict: **killed at `capability`**. `capability_row` (`:160-162`) returns `None` whenever the match
count is not exactly 1, so the decoy cannot shadow the audited row.

### (d) duplicate named drifted id — `mu-d` = `56aa0d15bba53513e1dba825933fd7a700aef6ba`

Live receipt `:157-158` `S156 drifted / S157 drifted` → `S156 drifted / S156 drifted` (count and
summary unchanged at `drifted=10`).

```
check anchors          PASS (anchors=3 missing=[] empty=0 unique=True)
check capability       PASS (paths=[...] missing=[])
check live_rows        FAIL (named=10 summary_drifted=10 unknown=[] unique=False)
check named_row_drift  PASS (exit=0 row_states=('PASS', ''))
check drift_kill       PASS (exit=1 row_states=('FAIL', ...))
C4=unmet
EXIT=1
```

Verdict: **killed at `live_rows`**, `unique=False`; all four M14 claims hold on the tip.

## 3. The fixes are load-bearing (pre-fix counter, same four revs)

Counter bytes at `daa1d4d` (`git show daa1d4d:.ufo/waves/round-38/count-c4.py`, materialised as
`.ufo/waves/round-38/count-c4-daa.py` in the /tmp clone only) on the identical revs:

```
===== OLD COUNTER (daa1d4d bytes) on mu-a =====   check anchors PASS (anchors=3 missing=[])   ... C4=met
===== OLD COUNTER (daa1d4d bytes) on mu-b =====   check anchors PASS (anchors=4 missing=[])   ... C4=met
===== OLD COUNTER (daa1d4d bytes) on mu-c =====   check capability PASS (paths=['tools/mori-source-drift.py']) ... C4=met
===== OLD COUNTER (daa1d4d bytes) on mu-d =====   check live_rows PASS (named=10 summary_drifted=10 unknown=[]) ... C4=met
```

All four exit 0. The `mu-c` line is the shadowing proof: the audited row's three paths are replaced by
the decoy's single path. The tip's four fixes strictly dominate the pre-fix counter on these bytes.

## 4. Bypass A (my design, `check_anchors`) — degenerate anchors score `met`

`bp-a` = `73acb3236f9e28ad738c19b768ee986bcef7559e`: the three anchors become three one-character
tokens that occur in any Python file.

```
   anchor: #
   anchor: :
   anchor: ==
```

```
$ python3 .ufo/waves/round-38/count-c4.py bp-a --repo /tmp/c4attack
negative witness-token-entry        rejected
negative witness-dangling-row       rejected
negative witness-summary-only-live  rejected
check anchors          PASS (anchors=3 missing=[] empty=0 unique=True)
check capability       PASS (paths=['tools/mori-source-drift.py', '.ufo/waves/round-37/evidence/c2-after-v3.txt', '.ufo/waves/round-37/evidence/drift-live-r37.txt'] missing=[])
check live_rows        PASS (named=10 summary_drifted=10 unknown=[] unique=True)
check named_row_drift  PASS (exit=0 row_states=('PASS', ''))
check drift_kill       PASS (exit=1 row_states=('FAIL', ...))
C4=met
EXIT=0
```

**BYPASS.** `check_anchors` (`:180-187`) is `len>=MIN_ANCHORS` + substring containment + non-empty +
distinct. There is no minimum anchor length, no requirement that an anchor contain an identifier or
operator, and no pinned expected-anchor set, so three arbitrary tokens satisfy the check while the
entry locates no policy at all. This re-opens the r37 M9 hole *for check 1*: `anchor: #` is exactly the
"token, not content" shape M9 was filed against. The entry concedes substring-level semantics
(`:55-57`, "An anchor is a substring, not a semantics proof"), but P-C4's predicate sells the check as
"resolves byte-exactly", and a hollow entry is indistinguishable from the real one.
Recommendation (not applied): pin the three expected anchor strings, or require each anchor to be
>= N chars and to contain an identifier token from the tool.

## 5. Bypass B (my design, `drift_kill`) — the counter accepts the inverse flip

`bp-b` = `e9b90efd09fb1d902e8a6800b8e85a99691db1b8`: the live classifier returns a dict constant, and
the only `return "drifted"` in the file is moved into an arm-expectation mirror that the selftest uses
to compute `want` (`tools/mori-source-drift.py` at that rev):

```
202  _ARM_EXPECT = {"fresh": "fresh", "excerpt": "excerpt", "drift": "drifted"}
205  def _arm_expected(kind):
209      return "drifted"
212  def classify(body, copy):
214          return _ARM_EXPECT["fresh"]
217          return _ARM_EXPECT["excerpt"]
218      return _ARM_EXPECT["drift"]
379  ("S101", "fresh"), ("S102", "excerpt"), ("S103", _arm_expected("drift")),
```

Two selftest legs (the counter's exact mutation, `return "drifted"` → `return "excerpt"`, applies only
to line 209):

```
$ python3 /tmp/bpb-real.py --selftest        -> PASS (6 cases)                 REAL_RC=0
$ python3 /tmp/bpb-mutant.py --selftest      -> row_states FAIL (got[('S103','drifted')] want[('S103','excerpt')])   MUT_RC=1
```

```
$ python3 .ufo/waves/round-38/count-c4.py bp-b --repo /tmp/c4attack
negative witness-token-entry        rejected
negative witness-dangling-row       rejected
negative witness-summary-only-live  rejected
check anchors          PASS (anchors=3 missing=[] empty=0 unique=True)
check capability       PASS (paths=[...] missing=[])
check live_rows        PASS (named=10 summary_drifted=10 unknown=[] unique=True)
check named_row_drift  PASS (exit=0 row_states=('PASS', ''))
check drift_kill       PASS (exit=1 row_states=('FAIL', "got=[... ('S103', 'drifted') ...] want=[... ('S103', 'excerpt') ...]"))
C4=met
EXIT=0
```

**BYPASS.** `flipped` (`:298-300`) is a symmetric substring test over one formatted blob:
`('S103','drifted')` present **and** `('S103','excerpt')|('S103','fresh')` present. The `drifted` half
is normally supplied by `want=` (the expected list), so the check cannot tell
*classifier flipped* (`got` becomes `excerpt`, `want` stays `drifted`) from
*expectation flipped* (`got` stays `drifted`, `want` becomes `excerpt`). `drift_kill` therefore does not
establish what item 4 of the entry claims — "the arm is load-bearing, not decorative"
(`corpus/knowledge/source-drift-content-anchor-r38.md:40-43`): a tool whose arm asserts a mirror is
decorative and still prints `C4=met`. The same move also satisfies the `return "drifted"` anchor, since
that anchor now resolves in the mirror rather than the classifier, so bypass A and B compose.
Landed tip is not mis-scored (its literal is in `classify` at `tools/mori-source-drift.py:208`,
reached from `:242`); this is a counter-robustness defect, not a mis-scored green.
Recommendation (not applied): parse `got`/`want` and require `got[S103] != want[S103]`,
`want[S103] == 'drifted'`, `got[S103] in ('excerpt','fresh')`, and additionally require the pristine
run's `got` to be identical to the mutated run's `want` list.

## 6. Control (not a bypass): equivalent spelling fails closed

`bp-c` = `66f057825fdbddbdf7f9e139e548d8471aa82d42`: behavioural no-op refactor, `_DRIFT_STATE =
"drifted"` + `return _DRIFT_STATE` in `classify` (the literal disappears from the file).

```
check anchors          FAIL (anchors=3 missing=['return "drifted"'] empty=0 unique=True)
check capability       PASS (paths=[...] missing=[])
check live_rows        PASS (named=10 summary_drifted=10 unknown=[] unique=True)
check named_row_drift  PASS (exit=0 row_states=('PASS', ''))
check drift_kill       FAIL (mutation anchor absent)
C4=unmet
EXIT=1
```

Fails closed via `:304`, so it is a false-negative risk (a harmless const extraction scores `unmet`),
not a way to smuggle a decorative arm past the counter. Recorded as residual risk R-4, not a finding
against the tip.

## 7. Pin and evidence audit

All 13 freeze-v3 pins verified against the tip (`git show b6993744:<path> | sha256sum`):

```
PIN-OK   .ufo/waves/round-38/contract.md
PIN-OK   .ufo/waves/round-38/count-c1.py
PIN-OK   .ufo/waves/round-38/count-c4.py
PIN-OK   .ufo/waves/round-38/conform.py
PIN-OK   .ufo/waves/round-38/fixtures/make-witness-sandbox.py
PIN-OK   .ufo/waves/round-38/fixtures/memo-n1.py
PIN-OK   .ufo/waves/round-38/fixtures/const.py
PIN-OK   .ufo/waves/round-38/fixtures/summary-only.py
PIN-OK   .ufo/waves/round-38/fixtures/hang-after-flush.py
PIN-OK   .ufo/waves/round-38/fixtures/memo-sha.py
PIN-OK   .ufo/waves/round-38/fixtures/witness-token-entry.md
PIN-OK   .ufo/waves/round-38/fixtures/witness-dangling-row.md
PIN-OK   .ufo/waves/round-38/fixtures/witness-summary-only-live.txt
```

But `evidence/c4-after.txt` does not reproduce from the pinned counter. Its `command:` line names
`f725f30`, while its body carries the pre-hardening detail format:

```
check anchors          PASS (anchors=3 missing=[])            # no empty=/unique=
check live_rows        PASS (named=10 summary_drifted=10 unknown=[])   # no unique=
```

`git diff f725f30 b6993744 -- .ufo/waves/round-38/evidence/c4-after.txt` is 1 insertion / 1 deletion,
and the only changed line is the `command:` line (`daa1d4d…` → `f725f30…`). Running the pinned tip
counter on `f725f30` prints `empty=0 unique=True` / `unique=True`; running the `daa1d4d` counter on
`f725f30` (and on `daa1d4d`) reproduces the committed body exactly. The receipt's body was produced by
an older counter and re-labelled, not re-run. The LOG claim it evidences
(`LOG.md:2219`, `count-c4.py <tip>` → `C4=met` exit 0) is itself true — I reproduced it in §1 — but
the cited receipt is not derived from the instrument it is attributed to.
Mitigating: `c4-before.txt` carries the same old format and is explicitly labelled `e37dcc6`, and no
pin covers `c4-after.txt`, so nothing in the freeze is internally inconsistent.

Also: M14's "Shown able to fail" rests on the detail-line format change and on
`w2/MutC4Anchor.md`, `w2/MutC4Live.md`, `w2/MutC4CapPath.md`, `w2/MutC4KillAlt.md` — all four of which
attacked `f725f30` (`grep` of each report's tip line: `f725f3076972e6e70595b5ac8279be524a111ff8`), i.e.
the *pre-fix* counter for exactly the four checks that changed. No committed receipt at `b6993744`
exercised the four new discriminators before this seat; the runs in §2 now do.

## Findings by severity

- **MEDIUM-1 — `drift_kill` accepts the inverse flip (§5).** `count-c4.py:298-302` tests two substrings
  in one blob; `want=` supplies `('S103','drifted')`, so an expectation-side change passes identically
  to a classifier-side change. Effect: a tool whose `row_states` arm asserts a mirror prints
  `C4=met`, contradicting the entry's "the arm is load-bearing, not decorative" (`:40-43`). The landed
  tool is not mis-scored.
- **MEDIUM-2 — `check_anchors` admits degenerate anchors (§4).** `:180-187` + `MIN_ANCHORS = 3` (`:49`)
  accept `#`, `:`, `==`; three one-char tokens score `C4=met`. Effect: the content check for the
  knowledge entry can be satisfied by non-content, the exact M9 shape, for check 1.
- **MEDIUM-3 — `evidence/c4-after.txt` is not reproducible from the pinned counter (§7).** Only its
  `command:` line was relabelled at `b6993744`; the body is the `daa1d4d` counter's output, and the
  pinned tip counter prints two additional fields. The LOG's C1 evidence pointer therefore does not
  derive from the instrument it names. Claim itself verified independently.
- **LOW-1 — ambiguous capability row is reported as "row absent".** `capability_row` (`:160-162`)
  returns `None` for both zero and ≥2 matches, and `check_capability` (`:190-193`) prints
  `row absent` with `missing=[]`; `main` then computes `cap_missing` against `""`. A maintainer reading
  `check capability FAIL (row absent missing=[])` cannot tell deletion from ambiguity. Diagnostics only
  (the check correctly fails).
- **LOW-2 — `check_anchors` prints `missing=[]` for blank anchors.** `:182` tests `a not in tool_text`,
  and `"" in any string` is true, so blank anchors are never "missing"; `empty=3` carries the truth
  (§2a). Diagnostics only.
- **LOW-3 — the counter's scratch root is a hardcoded absolute path.** `DEFAULT_REPO`/`SCRATCH_ROOT`
  (`:39,:45`) are used at `:279-280` regardless of `--repo` (`:233`). With `--repo /tmp/c4attack` the
  run still created and removed a dir under the lane's `.ufo/waves/round-38/scratch`; observed
  `stat -c %y` of that dir advancing `23:34:45 → 23:36:31` across one run. Consequence: the
  docstring's "re-derived from the pushed tree alone" holds only where that host path exists and is
  writable, and a seat measuring a foreign repo writes into the lane.
- **INFO — M14's able-to-fail evidence predates the fix (§7).** Not a code defect; the four receipts in
  §2 close the gap.

## Residual risk and verification gaps

- **R-1 (unbounded, untested):** `drift_kill` and `named_row_drift` are text assertions on the probe's
  stdout. A tool that inspects its own source and prints both arms' expected strings would pass both.
  [INFERENCE] — not built; it is a self-attesting claim no stdout-reading counter can settle, and the
  §5 mirror is the realistic version of it.
- **R-2:** `named_row_drift` was not attacked separately (out of the two-bypass assignment). It has no
  independent evidence beyond "the selftest exits 0 and prints `row_states PASS`".
- **R-3:** `check_live_rows` (`:198-211`) proves the receipt is enumerable and registry-consistent, not
  that the rows were drifted in this round. The entry's Limits (`:52-54`) says so; M14 should not be
  read as a truth check on the sweep.
- **R-4:** the instrument binds literal spellings (`return "drifted"` as both anchor and mutation
  target), so a behaviour-preserving refactor scores `unmet` (§6). Fail-safe direction, but it makes
  `C4=met` refactor-fragile rather than semantics-stable.
- **R-5:** no `lsp` device in this seat; every semantic statement above is grounded in execution output
  or committed bytes quoted with a line number, not in grep-only inference (grep was used only to
  locate lines).
- **R-6:** `resume_continuity_v1` / resume-preflight checks: not applicable to this object. `count-c4.py`
  is a single-shot measurement with no resume path, no checkpoint, and no mutation of the measured rev.
- No tools installed or upgraded; nothing to record under the tooling directive.
