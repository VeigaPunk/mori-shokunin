# Mo50bSimpCounters — dead weight in the frozen round-50 counters and controls

Seat: simplifier (leaf). Lane: mori-shokunin. Wave: round-50 / a2w1.
Scope measured: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-50/`
`count-c1.py`, `count-c2.py`, `controls/c1-controls.py`, `controls/c2-controls.py`.
Report path (relative to the lane root): `.ufo/waves/round-50/a2w1/Mo50bSimpCounters.md`.

I changed nothing in the lane, the fleet repo, the wave directory, `SKILL.md`, `SHONEN.md`,
`SCORECARD.md`, `LOG.md`, `corpus/`, `tools/` or `considerthese/`. The four files I measured are
byte-identical to the data revision and to the working tree (sha256 below, both measured). Every
mutation was made on a private copy under `/fast/scratch/hyaku/mori-r50/Mo50bSimpCounters/`, which was
removed at the end; the commands and outputs needed to re-derive each result are quoted here.

The counters and predicates are frozen. Everything below is a **proposal for the successor round**;
none of it changes the round-50 claim, and no counter weakness is presented as a fix for round 50.

## 1. Frozen bytes measured

```
$ sha256sum .ufo/waves/round-50/count-c1.py .ufo/waves/round-50/count-c2.py \
            .ufo/waves/round-50/controls/c1-controls.py .ufo/waves/round-50/controls/c2-controls.py
2d5c3ee53198124ef001908cc5abba5c71a6fb63773c31ece211b7c6cdae4456  count-c1.py
533c8403b90e650c786381bbf1394cf327b331936a4111b9faba4abd068ee55d  count-c2.py
c7b49dae9043ceda327e45ddaa5ce2c2ca09158e381162b76f393a50b7ee8a04  controls/c1-controls.py
641eecc5055955046a5039c765e34793ca693f3c1772397f11b2e593a99b1bd4  controls/c2-controls.py
```

```
$ for f in .ufo/waves/round-50/{count-c1.py,count-c2.py,controls/c1-controls.py,controls/c2-controls.py}; do
    a=$(git cat-file -p 487941b9:$f | sha256sum); b=$(sha256sum "$f"); ...; done
count-c1.py committed=2d5c3ee5… worktree=2d5c3ee5… same=yes
count-c2.py committed=533c8403… worktree=533c8403… same=yes
controls/c1-controls.py committed=c7b49dae… worktree=c7b49dae… same=yes
controls/c2-controls.py committed=641eecc5… worktree=641eecc5… same=yes
$ git status --porcelain -- .ufo/waves/round-50/count-c1.py .ufo/waves/round-50/count-c2.py \
      .ufo/waves/round-50/controls .ufo/waves/round-50/contract.md
(no output)
```

Sizes: `count-c1.py` 481 lines, `count-c2.py` 391, `controls/c1-controls.py` 153,
`controls/c2-controls.py` 60.

## 2. Method and tooling

1. Copy each file to scratch, mirror it at the same depth under
   `<scratch>/lane/.ufo/waves/round-50/` (so `count-c2.py`'s lane-root derivation and its
   `corpus/evidence/sources-r50/` reads still resolve; `corpus` is a symlink to the read-only lane
   copy), and record the baseline.
2. Baseline, both counters, at the data revision (read-only `--repo` on the lane):
   ```
   $ python3 count-c1.py 487941b9395e89678af0053cc443cdb49cdee6e3 --repo <lane> --fleet-repo <fleet>
   item axis coverage expect=round_47_improved got=ok state=ok
   … (8 item lines) …
   C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=487941b9395e89678af0053cc443cdb49cdee6e3
   $ echo $?
   0
   $ python3 count-c2.py 487941b9395e89678af0053cc443cdb49cdee6e3 --repo <lane>
   C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=487941b9395e89678af0053cc443cdb49cdee6e3
   $ echo $?
   0
   ```
   The item and `C1=`/`C2=` lines are identical to `evidence/a2-c1-at-data.txt` and
   `evidence/a2-c2-at-data.txt` (the evidence files additionally carry the shell's `exit=0` line).
   Selftests: `C1_SELFTEST pass=34 fail=0`, `C2_SELFTEST pass=31 fail=0`
   (matches `evidence/selftest-c1.txt`, `evidence/selftest-c2.txt`).
3. Apply one deletion per scratch copy (`M1`…`M8`), then:
   `python3 -m py_compile`, `--selftest` (tally and full stdout must equal baseline), and the real run
   at `487941b9` (full stdout must equal baseline). For the two control-suite mutants the "real run"
   is the suite itself: `controls/c1-controls.py <entering> --scratch <dir>` executed through a wrapper
   that only rebinds its module globals `LANE`/`FLEET`/`EVID` (the file is not edited; the fixture clone
   and the receipts land in scratch). Baseline suite and both mutants were run at entering
   `950e99be6757a52b00e9eb70ae1a1a7bbe2ea379`.
4. Static census: `pyflakes 4.0.3` and `ruff 0.17.2` (F841, F811, F401, F821, F822, F823, B018,
   PLW0127, PLW0602, PLR0206, RUF100, ARG001, ARG002) on all four files: `All checks passed!`, no
   unused imports, no undefined names. A sequential store/load scan over the AST produced the
   dead-store candidate list, and a call-site census across `round-48`…`round-50` produced the
   default-only-parameter list.
5. Branch census: `coverage run --branch` over the real run plus `--selftest` for each counter
   (`coverage 7.17.0`), to separate "unreachable" from "reachable but unexercised".

Tooling record: `ruff 0.17.2` installed/upgraded with `uv tool install --force ruff` (uv 0.13.0;
channel: `uv tool`, target `~/.local/bin/ruff`) because F841/F811/F401 give an auditable static census.
`pyflakes 4.0.3`, `coverage 7.17.0`, `python3 3.14.8`, `git 2.56.0` were already present. No `pacman`
transaction was run.

## 3. What was deleted, and the proof

All eight proposals are independent, add no new file or helper, and keep each instrument a single
self-contained file. Net line change for all eight: **−3**.

### P1 — `count-c1.py:154` dead store in `parse_shonen`

`rest = line` is overwritten at `:157` before any read; the only reader is `:158`.

```diff
@@ -151,7 +151,6 @@
     for line in text.split("\n"):
         if BOX.match(line):
             boxes += 1
-        rest = line
         for m in PIN.finditer(line):
             pins.append(m.groups())
         rest = PIN.sub(" ", line)
```

Proof (`M1`): `py_compile` ok; `C1_SELFTEST pass=34 fail=0`; real run output identical to baseline
(`diff` empty). Net −1 line.

### P2 — `count-c1.py:146`/`:211` the second return of `check_axes` has no reader

`check_axes` returns `(items, len(rows))`; the only caller binds the second element to `_` and never
reads it. The `rows is not None` guard inside the removed expression is already handled by the loop.

```diff
@@ -143,7 +143,7 @@
         items.append(("axis", ax, "round %d %s" % (n, verdict),
                       ",".join(problems) if problems else "ok", "mismatch" if problems else "ok"))
-    return items, (len(rows) if rows is not None else 0)
+    return items
@@ -208,7 +208,7 @@
     failed = []
     targets = manifest_targets(manifest_text)
-    axis_items, _ = check_axes(read("SCORECARD.md"), targets, exists)
+    axis_items = check_axes(read("SCORECARD.md"), targets, exists)
```

Proof (`M2`): selftest 34/0, real run identical, `py_compile` ok. Net 0 lines; removes a value no
caller consumes.

### P3 — `count-c1.py:229-230` unreachable failure marker `failed.append("axes")`

`check_axes` appends exactly one item per `AXES` element on every branch (`:114-145`: append+continue
for `want is None`, `rows is None`, `rows != 1`, `cells != 4`, and a final append), so
`len(axis_items) == len(AXES)` always, and the marker can never be appended.

```diff
@@ -226,8 +226,6 @@
         failed.append("pins_floor")
     if boxes < MIN_BOXES:
         failed.append("boxes_floor")
-    if sum(1 for i in axis_items) != len(AXES):
-        failed.append("axes")
     met = not failed
```

Proof, three ways:
```
# (a) invariant probe: 7 adversarial scorecards, every one yields items=6 and no "axes" in failed
none         items=6 rows=0   axes=6 failed has axes: False
empty        items=6 rows=0   axes=6 failed has axes: False
garbage      items=6 rows=0   axes=6 failed has axes: False
fenced       items=6 rows=0   axes=6 failed has axes: False
header_only  items=6 rows=0   axes=6 failed has axes: False
dup_rows     items=6 rows=2   axes=6 failed has axes: False
three_cells  items=6 rows=1   axes=6 failed has axes: False
# (b) coverage over real run + selftest: line 230 never executes
lane/.ufo/waves/round-50/count-c1.py  375  23  122  16  92%  93->108, 95, 102->104, 117-118, 129-130,
        165-166, 214, 230, 258-259, 263-265, 273, 277, 279-281, 303, 309-310, 313, 321, 322->324, 480->exit
# (c) mutation M3: selftest 34/0, real run identical, py_compile ok
```
Net −2 lines. This is the one deletion whose absence is proven by an invariant, not just by data.

### P4 — `count-c2.py:110`/`:112` the `copies` parameter is a seam with no caller (`:117`, `:171` read it)

`evaluate(..., copies=None)` is called at `:239` (`main`), at `:300` (selftest `run`) and from
`controls/c2-controls.py:50`; none passes `copies`. Census across rounds:

```
grep -c 'copies=' round-48/count-c2.py   -> 1   (the definition only)
grep -c 'copies=' round-49/count-c2.py   -> 1   (the definition only)
grep -c 'copies=' round-50/count-c2.py   -> 1   (the definition only)
grep -c 'copies=' round-50/controls/c2-controls.py -> 0
```
The parameter has had zero callers since round 48; the overlay reader the controls need is built by
`c2-controls.py` itself, not through this argument. After the first draft of the patch (parameter and
alias removed, body still reading `copies`) the selftest failed with
`NameError: name 'copies' is not defined`, which is why the patch also replaces the two body reads:

```diff
-def evaluate(read, rev, entry_path=None, copies=None):
+def evaluate(read, rev, entry_path=None):
     entry_path = entry_path or ENTRY
-    copies = copies or COPIES
     failed = []
@@
-    for url, (path, digest, kind) in copies.items():
+    for url, (path, digest, kind) in COPIES.items():
@@
-                for u in copies:
+                for u in COPIES:
```

Proof (`M4`, final form): `C2_SELFTEST pass=31 fail=0` and the real run line identical to baseline.
Net −1 line.

### P5 — `count-c2.py:281`/`:293` the `drop` parameter and its ternary are dead

`build(claim_rows=None, drop=None, claims=None, **kw)` — no call site passes `drop` (`grep -c 'drop='`
= 1 in round-48, round-49, round-50 `count-c2.py`: the definition only). With `drop is None` the
condition `drop != sids[u]` is always true, so the `else {"status": "queued"}` arm is unreachable.
This seam is also carried from round 48 unchanged.

```diff
-    def build(claim_rows=None, drop=None, claims=None, **kw):
+    def build(claim_rows=None, claims=None, **kw):
@@
-            srow(u, sids[u], **({k: v for k, v in kw.items() if k in ("status", "opened", "used", "indent")}
-                                if drop != sids[u] else {"status": "queued"})) for u in urls])
+            srow(u, sids[u], **{k: v for k, v in kw.items() if k in ("status", "opened", "used", "indent")})
+            for u in urls])
```

Proof (`M5`): selftest 31/0, real run identical, `py_compile` ok. Net 0 lines.

### P6 — `controls/c1-controls.py:38` the `check` parameter of `g()` is never varied

All eleven call sites (`:79, 82, 83, 84, 85, 87, 88, 128, 134, 135, 136`) omit it; the default is the only
value ever used and `subprocess.run` already takes the knob.

```diff
-def g(repo, *args, check=True):
-    return subprocess.run(["git", "-C", repo] + list(args), check=check, stdout=subprocess.PIPE,
+def g(repo, *args):
+    return subprocess.run(["git", "-C", repo] + list(args), check=True, stdout=subprocess.PIPE,
```

Proof (`M6`, full control suite, 8 controls, baseline vs mutant; `rev=` fields normalised because the
fixture commit hash depends on wall-clock time):

```
$ diff ctl/norm-base.txt ctl/norm-M6.txt ; echo rc=$?
rc=0
$ diff <(cd evidence-base && cat *) <(cd evidence-M6 && cat *)   # receipts, rev= normalised
(no output)
```
Both suites exit 0 with `witness` met and the other seven unmet; receipts identical. Net 0 lines.

### P7 — `controls/c1-controls.py:50-53` the `spot` string is computed and then discarded for `adjacency`

`spot` is formatted for every axis, then `if ax == "adjacency": ev = cells[2]` throws it away. The
adjacency row is always present in the target map (MANIFEST target `(19, "improved")`), so this is the
normal path, not an edge case.

```diff
             n, v = targets[ax]
-            spot = "corpus/lessons/round-%d-verifier-spotcheck.md" % n
-            ev = cells[2] + "; latest admitted closure grading %s %s: `%s`" % (ax, v, spot)
             if ax == "adjacency":
                 ev = cells[2]
+            else:
+                spot = "corpus/lessons/round-%d-verifier-spotcheck.md" % n
+                ev = cells[2] + "; latest admitted closure grading %s %s: `%s`" % (ax, v, spot)
```

Proof (`M7`): the same suite comparison as P6 (`diff ctl/norm-base.txt ctl/norm-M7.txt` rc=0; receipts
identical). Net **+1 line** — the win is that a reader no longer sees a spotcheck path being built for
a row that must not cite one; a denser inline conditional would be net −2 but harder to read, so I did
not propose it. This is the one proposal whose line count goes the wrong way; drop it if the successor
prefers pure line count.

### P8 — `count-c2.py:248`/`:252` unused tuple bindings in `selftest`

`for url, (path, digest, kind) in COPIES.items()` reads only `path`; `for u, (p, d, k) in
COPIES.items()` reads only `p` and `k`. The AST load census shows `digest`, `kind` and `d` are never
loaded. (`ruff`/`pyflakes` do not report tuple-unpack targets, so this needed the AST pass.)

```diff
-    for url, (path, digest, kind) in COPIES.items():
+    for url, (path, _digest, _kind) in COPIES.items():
@@
-             for u, (p, d, k) in COPIES.items()}
+             for u, (p, _d, k) in COPIES.items()}
```

Proof (`M8`): selftest 31/0, real run identical. Net 0 lines.

### Proof summary

| mutant | file | py_compile | selftest | real run (487941b9) | net lines |
|---|---|---|---|---|---|
| M1 | count-c1.py:154 | ok | `pass=34 fail=0` | `diff` empty | −1 |
| M2 | count-c1.py:146,211 | ok | `pass=34 fail=0` | `diff` empty | 0 |
| M3 | count-c1.py:229-230 | ok | `pass=34 fail=0` | `diff` empty | −2 |
| M4 | count-c2.py:110,112,117,171 | ok | `pass=31 fail=0` | `diff` empty | −1 |
| M5 | count-c2.py:281,293 | ok | `pass=31 fail=0` | `diff` empty | 0 |
| M6 | controls/c1-controls.py:38 | — | — | suite output + receipts identical | 0 |
| M7 | controls/c1-controls.py:50-53 | — | — | suite output + receipts identical | +1 |
| M8 | count-c2.py:248,252 | ok | `pass=31 fail=0` | `diff` empty | 0 |

Harness fidelity: the baseline control suite I ran (entering `950e99be`) reproduces the landed
receipts' verdict lines at entering `7197160b` on all eight controls. Comparing my suite's line for
each control against `evidence/control-c1-<name>.txt` with only `rev=` stripped:

```
do-nothing SAME | all-latest SAME | pins-deleted SAME | pins-updated-no-receipt SAME
axes-only SAME | shonen-only SAME | box-dropped SAME | witness SAME
```
(`do-nothing … items=8 axes=6 pins=2 boxes=4 mismatches=6 errors=0 hidden=0 failed=mismatch`;
`pins-deleted … items=6 pins=0 … failed=mismatch,pins_floor`; `box-dropped … boxes=3 …
failed=boxes_floor,mismatch,pins_floor`; `witness … C1=met … mismatches=0`, exit 0.)

## 4. Candidates examined and deliberately **not** proposed

1. **`split_cells` is duplicated between the two counters** (`count-c1.py:56-61`, `count-c2.py:48-59`;
   identical semantics, different style — conditional expression vs if/else). Measured on 3,087 inputs
   (the ten table-edge probes plus every line of `SCORECARD.md`, `SHONEN.md`, `corpus/SOURCES.md` and
   the entry): **0 differences**. Not proposed: merging it would have to live in a third file (or make
   one counter import the other), and each counter is audited as one self-contained frozen artefact;
   that buys ~6 lines at the cost of a shared authority between two independently frozen predicates
   and a new failure mode (the C1 counter would depend on the C2 file's bytes). The successor should
   keep the copy.
2. **Carry-over from round 49's counter.** `count-c2.py` shares 11 byte-identical function bodies with
   `round-49/count-c2.py` (`split_cells` 8 lines, `normalise` 6, `parse_claims` 23, `sources_row` 5,
   `git_reader` 6, `main` 23, and the nested `read`/`quote_from`/`srow`/`run`/`check`, 15) — 86 lines;
   `round-48`→`round-49` shared 175 lines including `evaluate`. `count-c1.py` shares nothing with
   round-49's C1 (the predicate was rewritten). The carried code is live, not dead; the same
   self-contained-artefact argument as (1) applies. Nothing proposed.
3. **Default-only parameters that are predicate documentation, not dead seams.**
   `manifest_targets(manifest_text, through=THROUGH, lane=LANE)` (`count-c1.py:63`; five selftest calls
   and `:210` pass one argument only), `git(repo, *args, timeout=120)` (`:243`, never overridden),
   `quote_from(url, needle, n=8)` (`count-c2.py:254`; all 15 call sites pass `n`). These name a cutoff,
   a subprocess budget and a quote length in one place; deleting them saves two default expressions and
   loses the only named seam. Note for the successor: `LANE` (`:42`) is read *only* by the
   `manifest_targets` default, so the two stand or fall together.
4. **MANIFEST shape fallbacks** (`count-c1.py:64-77`: `data["rounds"] if isinstance(data, dict) else
   data`, `r.get("lane_round", r.get("round"))`, `not isinstance(n, int)`, `not isinstance(v, dict)`).
   Checked against the pinned manifest: 750 rounds, 38 `lane`, 24 admitted mori rounds, **all** admitted
   rows carry `lane_round` as an int and a dict `verdicts`; the manifest also holds 160 entries with
   non-dict `verdicts` and rows keyed `round`/`type` without `lane`, so the guards are live filters for
   the file's real shape diversity, and the `round` alias is a schema tolerance rather than a dead arm.
   Not proposed — deleting them would turn a shape change into a traceback.
5. **`source_rows` in the C2 output line** (`count-c2.py:196-201`) is nearly implied by `bad_rows`:
   `srows_ok = "ok" if (ids_in_table and not bad) else "bad"` and the `failed` list then carries both
   `bad_rows` and `source_rows` with the same cause. It is part of the frozen output format and adds a
   second failure name, not a second fact. Named limit only; no change proposed for round 50, and the
   successor should keep the field if it keeps the format.
6. **`controls/c1-controls.py:92-101`, the `obs-tree` directory guard sits inside the two-iteration
   loop.** It is idempotent and correct (the second pass skips the rebuild), so it is not dead; moving
   it out would be churn.

## 5. Coverage census (not all gaps are dead code)

```
count-c1.py  375 stmts  92%  missing: 93->108, 95, 102->104, 117-118, 129-130, 165-166, 214, 230,
                             258-259, 263-265, 273, 277, 279-281, 303, 309-310, 313, 321, 322->324
count-c2.py  294 stmts  97%  missing: 57, 171->175, 228, 230-231, 236-238
```

Classified only where the evidence supports it:

- **Unreachable by invariant:** `count-c1.py:230` (P3). One line.
- **Reachable, never exercised by the 34-arm selftest or the honest run** — these are selftest gaps, not
  dead code, and I do not propose deleting them: `count-c1.py:117-118` (`manifest_has_no_target`),
  `:129-130` (`cells != 4`), `:214` (`shonen_absent` — the selftest never drops `SHONEN.md`),
  `:165-166` (`bound_path` on a backticked command with unbalanced quoting), `:258-259/:263-265`
  (usage errors), `:273/:277/:279-281` (setup errors), `:303/:309-310/:313` (archive/missing-tally/
  timeout arms), `:321/:322->324` (cleanup branches); `count-c2.py:57` (a table row without a trailing
  pipe), `:171->175` (a row whose S-id matches none of the three frozen URLs, so the match loop never
  exits without a hit), `:228` (`--entry`), `:230-231`,
  `:236-238`.
- **Exercised:** everything else, including both counters' honest paths and the four `check_axes`
  early-exit append arms that P3's invariant depends on.

## 6. One control-suite defect found while proving P6/P7 (not dead code)

`controls/c1-controls.py:110-112` builds its two edited-SHONEN controls by substituting the literal
strings `"(60/60)"` and `"(13/13)"`:

```
sh_upd   = sh0.replace("(60/60)", "(%s/%d)" % (pa, int(pa) + int(pf))).replace("(13/13)", …)
sh_nopin = sh0.replace(" (60/60)", "").replace(" (13/13)", "")
```

At the entering revision those literals are present
(`git show 950e99be:SHONEN.md:7` → ``…--selftest` (60/60); …--selftest` (13/13)``), so the controls are
live today. If a round enters with any other pin values, both `replace` calls become no-ops, the
`pins-updated-no-receipt` and `pins-deleted` controls silently collapse into (near-)copies of
`do-nothing`, and the suite still exits 0 because its only assertion is
`(name == "witness") != (r.returncode == 0)` at `:141`: an unchanged SHONEN is still `unmet`, so the
control passes **vacuously**. The suite never asserts that `sh_upd != sh0`. This vacuity is deduced
from the code (the edited text would equal `sh0`, and `do-nothing` is unmet at both entering revisions
observed this round), **not run**: I did not have an entering revision with different pin literals to
demonstrate it end to end, so the end-to-end demonstration is UNVERIFIED. Proposed for the successor
(no round-50 change): derive the two literals from `sh0` (e.g. take the two pin spans with the same
`c1.PIN` regex the counter uses) or assert `sh_upd != sh0 and sh_nopin != sh0` before the run.

`controls/c2-controls.py:17` hardcodes `STAGED = "/home/vgpnk/Projects/shokuknow/merge/mori"`; the
control raises `FileNotFoundError` rather than reporting a setup error if that read-only share moves.
LOW, named only.

## 7. Named limits of this proof

- Every "identical output" claim is against the **round-50** bytes at `487941b9` (counters) and
  entering `950e99be` (control suite). The successor's bytes will differ; the patches are minimal and
  self-contained, but they must be re-proved on the successor's base.
- The control-suite mutants (M6, M7) were run through a wrapper that rebinds the module globals
  `LANE`/`FLEET`/`EVID` so that no receipt is written into the lane and no commit is made in it; the
  controlled file itself is byte-identical apart from the quoted diff. The baseline suite under that
  wrapper reproduces the landed verdicts, which is the fidelity check for the harness.
- Coverage was measured over exactly two executions per counter (real run, selftest). A line absent from
  both is "unexercised", not automatically "dead"; only P3 is argued from an invariant.
- I did not audit the data (entry wording, SOURCES rows, SCORECARD/SHONEN cells) — that is other seats'
  scope, and this seat found no data error in what it had to read.
- Frozen counters were not edited, so no round-50 claim is re-scored and no kill rule is touched.

## Findings

1. **MED — `count-c2.py:110,112,117,171`: `evaluate(..., copies=None)` is a stale seam.** Zero callers
   pass it in rounds 48, 49 and 50 (definition-only occurrences) and in `controls/c2-controls.py`;
   the overlay reader the controls need is built outside `evaluate`. Removing it (P4, M4) leaves
   selftest 31/0 and the data-revision output identical.
2. **MED — `count-c2.py:281,293`: `build(..., drop=None)` and its `else {"status": "queued"}` arm are
   unreachable.** No caller passes `drop` in rounds 48–50, so `drop != sids[u]` is always true.
   Removing it (P5, M5) leaves selftest 31/0 and the data-revision output identical.
3. **MED — `count-c1.py:229-230`: `failed.append("axes")` is unreachable by invariant.**
   `check_axes` emits exactly one item per axis on every branch; seven adversarial scorecards and the
   branch coverage (line 230 never executed across the real run plus the 34-arm selftest) both agree.
   Removing it (P3, M3) leaves both outputs identical.
4. **MED — `controls/c1-controls.py:110-112,141`: two controls can pass vacuously.** The `(60/60)` /
   `(13/13)` substitutions are hardcoded, the suite never asserts the edited SHONEN differs from the
   entering one, and its only assertion still accepts `unmet`; a round with different pin values turns
   `pins-updated-no-receipt` and `pins-deleted` into near-copies of `do-nothing` while the suite stays
   green. Deduced from the code, not demonstrated end to end (UNVERIFIED — no entering revision with
   different pin literals was available; see §6).
5. **LOW — `count-c1.py:154`: dead store `rest = line`.** Overwritten at `:157` before any read;
   deleting it (P1, M1) leaves both outputs identical.
6. **LOW — `count-c1.py:146` + caller `:211`: the row count returned by `check_axes` has no reader.**
   Simplifying the return (P2, M2) leaves both outputs identical.
7. **LOW — `controls/c1-controls.py:38`: `g(..., check=True)` is default-only.** All eleven call sites omit
   it; removing the parameter (P6, M6) leaves the whole 8-control suite and its receipts identical.
8. **LOW — `controls/c1-controls.py:50-53`: `spot` is formatted and then discarded for `adjacency`.**
   The adjacency row is the normal path; (P7, M7) gives identical suite output at +1 line.
9. **LOW — `count-c2.py:248,252`: unused tuple bindings `digest`, `kind`, `d` in `selftest`.**
   Renaming them (P8, M8) leaves both outputs identical; `ruff`/`pyflakes` cannot see tuple-unpack
   targets, so this needed the AST census.
10. **LOW — `count-c1.py:117-118,129-130,165-166,214` and `count-c2.py:57,171->175,228`: predicate arms
    that neither counter's selftest nor the honest run exercises.** Not dead code; a gap in what the
    frozen selftests prove (notably `shonen_absent` and the two `check_axes` early exits).
11. **LOW — duplication kept on purpose:** `split_cells` identical in both counters (0 differences over
    3,087 inputs) and 86 lines carried verbatim from `round-49/count-c2.py`. Merging would create a
    shared authority between two independently frozen predicates; recommended unchanged.
