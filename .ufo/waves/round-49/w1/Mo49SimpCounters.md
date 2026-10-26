# Mo49SimpCounters — dead weight in the two frozen counters and the r48 reconciler

Seat: Mo49SimpCounters (simplifier, leaf). Round 49, wave w1. Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Lane tip when measured: `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115` (freeze). The tip moved to
`24ebc7991e9081348d1aa4f558f994b1f4feccab` ("round-49: data C2 — journal-reach entry …") while my first
C1 pair was running; both C1 runs were re-pinned to the freeze sha before comparison (see §5).
Report author date: 2026-10-25 (at/after the tip it cites).

Scope: `count-c1.py`, `count-c2.py` (frozen — proposals only) and
`controls/tool-r48-merged-witness.py` (control; the same bytes are the landing target for
`tools/mori-pin-check.py`, which carries the same two unused parameters — see §9). Nothing in the lane was
edited: every change below lives in `.scratch/r49-Mo49SimpCounters/b/`, and every run reads only from the
lane.

## 1. Freeze identity and what I did not touch

```
$ sha256sum .ufo/waves/round-49/count-c1.py .ufo/waves/round-49/count-c2.py \
            .ufo/waves/round-49/controls/tool-r48-merged-witness.py
3c262a15ae28adffa63f6646d5ec15498d1a4c735dbc3c38f68af16afc616b6d  .ufo/waves/round-49/count-c1.py
be39475d997f5cf4e67c7d69f66f176b1632985451ed0a6b8a5a4c2a495dd837  .ufo/waves/round-49/count-c2.py
c30ab6232893d984d1440784b6ce962d7c987c6d5538db0ead2f458a8ea1c9f0  .ufo/waves/round-49/controls/tool-r48-merged-witness.py
```
All three equal the values in `evidence/freeze-sha256.txt`. Working tree after all work:
`git status --porcelain --untracked-files=no` → empty (no tracked file changed; no git/jj mutation was run;
fixture repos were created only under scratch with `-c user.name/user.email` and their
`rev-parse --show-toplevel` was checked equal to the scratch dir before the first commit).

## 2. Method, and the one tool that was unavailable

- **Semantic proof of "no caller"**: the `lsp` device is not mounted on this host —
  `read xd://lsp` → `No such tool: xd://lsp. Mounted devices: ast_edit, debug, mcp__tripo_*, mcp__unity_cli_status`.
  So callers were proven (a) inside each module by an AST pass (module-scope `Name` loads and
  assigned-but-never-read locals, run over the frozen bytes) and (b) across the lane by literal grep — the
  text fallback, recorded as such, not a semantic proof. Repo-wide, none of `FIX_HEADER`, `_cur_pin`,
  `measure_text_only` is referenced outside the defining file, and `plan_text_only` has **no committed
  caller** — it appears only in this round's seat prose and in one wave-1 scratch harness
  (`w1/Mo49ExecRegressionCorpus.md`, which calls `count-c1.plan_text_only()` on the frozen counter). That is
  why §7 records a return-arity caveat for that one function and none for the others.
- **Linter** (second opinion, ephemeral, nothing installed): `uvx ruff@0.14.0 check --select F,ARG --isolated`
  — `F` (pyflakes: unused imports/vars) **0 findings before and after** on all three files; `ARG` (unused
  arguments) 7 findings before, 4 after. The four survivors are the callback signature of `sniff_run`,
  required by the 7-argument call at `count-c1.py:457`. Tooling record: `uvx`
  channel (`~/.local/bin/uvx`, official PyPI via uv cache), reason: unused-argument second opinion; no
  pacman transaction (`/usr/bin/time` is absent on this host — my first timing attempt returned rc 127 and I
  re-ran with `date` arithmetic instead of installing anything).
- **A/B harness**: `$S=.scratch/r49-Mo49SimpCounters`; `$S/a/.ufo/waves/round-49/*` = byte-identical frozen
  copies; `$S/b/...` = the same files after the deletions; each of `$S/a`, `$S/b` is its own fixture git
  repo (`init -b master`, one commit containing `SKILL.md` and the four `corpus/evidence/sources-r49/`
  copies) so that the counters' `__file__`-relative `LANE` computation and `count-c2.py --selftest` file
  reads resolve inside scratch. `TMPDIR=$S` for every run.

## 3. Deletions proven on the scratch copy (no behaviour change)

Frozen line numbers are from the `a/` copies (= freeze bytes).

| # | file:frozen line | deletion | why it is dead | proof |
|---|---|---|---|---|
| 1 | `count-c1.py:73` | `_cur_pin(text, prefix, cmd_hint=None)` → `(text, prefix)` | `cmd_hint` never read; all 3 call sites pass 2 args (lines 102,136,141) | AST unused-param, ruff ARG001, grep of call sites |
| 2 | `count-c1.py:157-158`, use `:169` | delete `FIX_HEADER`; `_fixture_skill` uses `HEADER` (line 65) | byte-identical literal: `ast.literal_eval(HEADER) == ast.literal_eval(FIX_HEADER)` → `True`; `HEADER` is module scope; the only other reference was line 169 | literal comparison + grep (`FIX_HEADER` count 2: def + one use) |
| 3 | `count-c1.py:248` | `plan(repo, rev, scratch, baseline, min_tally)` (drop both defaults) | sole caller passes both (line 282); no other caller in the lane | grep `plan(` → 1 call |
| 4 | `count-c1.py:281,289` | drop `run=run_tool` seam; submit `run_tool` directly | the seam is never supplied (`measure` has 1 caller, `main:334`, 7 positional args) | grep `measure(` → 1 call |
| 5 | `count-c1.py:372-373` | `plan_ok` arm: `err is None` → exact job count | `plan_text_only` has no failure path, so the old arm could not fail (finding 1); new condition `len(pl) == len(r48.VARIANTS)+len(NEW_VARIANTS)+2` = 25, which holds | selftest A/B below; arm stays PASS |
| 6 | `count-c1.py:398-399` | drop `verdict(res, head) if res else (True, str(err))` fallback | `measure_text_only` always returns a non-empty list (`plan_text_only` always appends 25 jobs) | AST + reading; selftest output identical |
| 7 | `count-c1.py:449,459` | `return jobs, None` → `return jobs`; `return results, None` → `return results`; `(pl or [])` at `:374` → `pl` | second elements are literal `None` at both sites, and the only unpack sites test them for truth; `pl` can no longer be `None` | selftest identical |
| 8 | `count-c2.py:79` | `header = header if rows else None` → `header = None` | the branch is reached only when `header is None` (else `rows` truthy broke out at :76) or when `rows` is empty; the expression evaluates to `None` either way | truth-table by reading; selftest identical |
| 9 | `count-c2.py:99,101,106,156` | drop `copies=None` parameter; use module `COPIES` | no caller passes it (`main` calls `evaluate(read, rev, entry_path=…)`; selftest passes only `**kw` built from empty kwargs) | grep `copies=` → 1 hit (the parameter itself) |
| 10 | `count-c2.py:260,270-271` | drop `drop=None` from selftest `build()` and the untaken `else {"status": "queued"}` | no `build(...)` call passes `drop` (grep `drop=` → only the def) | grep; selftest 26/26 identical |
| 11 | `count-c2.py:311` | `only2[:8] if len(only2) >= 8 else only2` → `only2` | `qs` holds 2 quotes per URL for 4 URLs; `only2` is 4 + 1 = **5** items, so the condition is always false and the slice is unreachable | counted from the `qs` literal; selftest identical |
| 12 | witness `:346,577` | `trunc_digest_pins(st, raw, root)` → `(st, root)` | `raw` never read; one call site | ruff ARG001 + AST unused-param |
| 13 | witness `:433,637` | `run_cmd(words, root, scratch, timeout)` → `(words, root, timeout)` | `scratch` never read (the function makes its own tmp under `<root>/.scratch`); one call site | ruff ARG001 + AST |
| 14 | witness `:485,756,988-990,996-997` | drop `scratch` through `check()`; delete the two per-case `tempfile.mkdtemp(prefix="c-", …)` | after #13 the only consumer of `check`'s `scratch` was `run_cmd`; the selftest's per-case dir existed only to be passed in (41 dirs per selftest run) | selftest 65/65 identical; real run identical |

Net size: `count-c1.py` 463→459 lines (22808→22583 B), `count-c2.py` 355→354 (16227→16052 B),
witness 1020→1018 (55116→54925 B).

No `text = …` leftover was found: the AST scan for assigned-but-never-read locals on the frozen bytes
reports only tuple-unpack names (`verdict`'s `r`, `selftest`'s `expect`, `measure_text_only`'s `err` in the
frozen version, `count-c2.py`'s `digest`/`d` in loop unpacks) — the pattern the seat hypothesised does not
exist in these three files.

## 4. Selftest tallies — unchanged

```
$ TMPDIR=$S python3 $S/a/.../count-c1.py --selftest   → C1_SELFTEST pass=44 fail=0 (rc 0)
$ TMPDIR=$S python3 $S/b/.../count-c1.py --selftest   → C1_SELFTEST pass=44 fail=0 (rc 0)
$ TMPDIR=$S python3 $S/a/.../count-c2.py --selftest   → C2_SELFTEST pass=26 fail=0 (rc 0)
$ TMPDIR=$S python3 $S/b/.../count-c2.py --selftest   → C2_SELFTEST pass=26 fail=0 (rc 0)
$ TMPDIR=$S python3 $S/a/.../tool-r48-merged-witness.py --selftest → PIN_CHECK_SELFTEST pass=65 fail=0 (rc 0)
$ TMPDIR=$S python3 $S/b/.../tool-r48-merged-witness.py --selftest → PIN_CHECK_SELFTEST pass=65 fail=0 (rc 0)
```
Output comparison after normalising the scratch roots (`s|$S/a|ROOT|`, `s|$S/b|ROOT|`): `count-c2.py` and
the witness are **byte-identical** (27 and 66 lines). `count-c1.py` differs in exactly one line — the detail
column of the arm I re-specified:

```
< PASS plan_ok  None
> PASS plan_ok  25
```
i.e. the arm passes on both sides; only its evidence string changed (and the frozen string was the constant
`None`).

## 5. Real runs — identical output

**C1** (the predicate line; 26 variants, `--jobs 3`, ~14-32 min per run):

```
python3 $S/{a,b}/.ufo/waves/round-49/count-c1.py \
  --tool $LANE/.ufo/waves/round-49/controls/tool-r48-merged-witness.py \
  --rev 0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115 --repo $LANE --jobs 3
```
```
C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26 rev=0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115
```
Both files (28 lines = 27 variant rows — J1-J8, H1-H4, N1-N9, H6, H7, N10, H5, `real`, `real-opaque` — plus
the verdict line; `variants=26` is `len(results) - 1`, the `real` row not being counted as a variant) hash to
`9db78339850202956cedbdc4c5deea0d1bd03fe627944b4c4fd46017f09a0c57` — **byte-identical**.

Observed hazard worth recording: my first B run used `--rev HEAD` and the lane tip moved
(`0df17b7b` → `24ebc799`) between the two runs, so the pair printed different `rev=` values; the only guard
is the `rev=` field on the output line. I re-ran B against the pinned sha. Anyone comparing two counter runs
should pin the sha in the receipt (see F9).

**C2** (4 runs: A/B × two revisions):

```
$ python3 $S/a/.../count-c2.py HEAD     --repo $LANE  → C2=unmet … source_rows=bad pins=ok  provenance=bad rev=0df17b7b… failed=entry_absent          (rc 1)
$ python3 $S/b/.../count-c2.py HEAD     --repo $LANE  → (identical line, rc 1)
$ python3 $S/a/.../count-c2.py b3e3453d --repo $LANE  → C2=unmet … source_rows=bad pins=bad provenance=bad rev=b3e3453d… failed=entry_absent,pins     (rc 1)
$ python3 $S/b/.../count-c2.py b3e3453d --repo $LANE  → (identical line, rc 1)
```
The `b3e3453d` line reproduces the freeze receipt `evidence/control-c2-donothing.txt` exactly
(`failed=entry_absent,pins`), so the pins arm and the entry-absent arm are exercised on both sides.

**Witness tool** (real registry read through an exported tree, with the baseline pin check):

```
$ python3 $S/{a,b}/.../tool-r48-merged-witness.py --rev 0df17b7b… --repo $LANE --min-tally-pins 26 \
      --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53
PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 \
  duplicate=0 hidden=0 misattributed=0 min_tally_pins=26 rev=0df17b7b… baseline=yes   (rc 0)
```
42 output lines, identical byte-for-byte after path normalisation on both sides.

## 6. Diffs (elided; the authoritative patch is `diff -u a/ b/`, and the bytes persist)

`count-c1.py`:
```diff
-def _cur_pin(text, prefix, cmd_hint=None):
+def _cur_pin(text, prefix):
@@
-FIX_HEADER = ("| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |\n"
-              "|---|---|---|---|---|---|---|---|\n")
-
-
 def _probe_src(arms):
@@
-    return ("# fixture registry\n\n" + FIX_HEADER +
+    return ("# fixture registry\n\n" + HEADER +
@@
-def plan(repo, rev, scratch, baseline=BASELINE, min_tally=MIN_TALLY):
+def plan(repo, rev, scratch, baseline, min_tally):
@@
-def measure(tool, repo, rev, baseline, min_tally, scratch, jobs, run=run_tool):
+def measure(tool, repo, rev, baseline, min_tally, scratch, jobs):
@@
-            futs[ex.submit(run, tool, rrepo, rrev, skill, rbase, rmin, tmp)] = (name, expect)
+            futs[ex.submit(run_tool, tool, rrepo, rrev, skill, rbase, rmin, tmp)] = (name, expect)
@@
-        pl, err = plan_text_only(base, text, head)
-        arm("plan_ok", err is None, str(err))
-        names = [os.path.basename(j[2] or "") + "|" + os.path.basename(j[5]) for j in (pl or [])]
+        pl = plan_text_only(base, text, head)
+        arm("plan_ok", len(pl) == len(r48.VARIANTS) + len(NEW_VARIANTS) + 2, "%d" % len(pl))
+        names = [os.path.basename(j[2] or "") + "|" + os.path.basename(j[5]) for j in pl]
@@
-        res, err = measure_text_only(base2, text, head, sniff_run)
-        met, line = verdict(res, head) if res else (True, str(err))
+        res = measure_text_only(base2, text, head, sniff_run)
+        met, line = verdict(res, head)
@@
-    return jobs, None
+    return jobs
@@
-    jobs, err = plan_text_only(scratch, text, rev)
+    jobs = plan_text_only(scratch, text, rev)
@@
-    return results, None
+    return results
```

`count-c2.py`:
```diff
-                header = header if rows else None
+                header = None
@@
-def evaluate(read, rev, entry_path=None, copies=None):
+def evaluate(read, rev, entry_path=None):
     entry_path = entry_path or ENTRY
-    copies = copies or COPIES
     failed = []
@@
-    for url, (path, digest) in copies.items():
+    for url, (path, digest) in COPIES.items():
@@
-                for u in copies:
+                for u in COPIES:
@@
-    def build(claim_rows=None, drop=None, **kw):
+    def build(claim_rows=None, **kw):
@@
-            srow(u, sids[u], **({k: v for k, v in kw.items() if k in ("status", "opened", "used", "indent")}
-                                if drop != sids[u] else {"status": "queued"})) for u in urls])
+            srow(u, sids[u], **{k: v for k, v in kw.items() if k in ("status", "opened", "used", "indent")})
+            for u in urls])
@@
-    met, line = run(build(claim_rows=only2[:8] if len(only2) >= 8 else only2))
+    met, line = run(build(claim_rows=only2))
```

`tool-r48-merged-witness.py`:
```diff
-def trunc_digest_pins(st, raw, root):
+def trunc_digest_pins(st, root):
@@
-def run_cmd(words, root, scratch, timeout):
+def run_cmd(words, root, timeout):
@@
-def check(text, root, scratch, rev, timeout, min_tally, baseline_text=None):
+def check(text, root, rev, timeout, min_tally, baseline_text=None):
@@
-        for pfx, hit in trunc_digest_pins(st, row["raw"], root):
+        for pfx, hit in trunc_digest_pins(st, root):
@@
-                cache[key] = run_cmd(words, root, scratch, timeout)
+                cache[key] = run_cmd(words, root, timeout)
@@
-            met, out = check(text, root, scratch, rev, args.timeout, args.min_tally_pins, baseline_text)
+            met, out = check(text, root, rev, args.timeout, args.min_tally_pins, baseline_text)
@@
-            scratch = tempfile.mkdtemp(prefix="c-", dir=base)
             text, btext = text if isinstance(text, tuple) else (text, None)
-            met, out = check(text, root, scratch, "deadbeef", 5, floor, btext)
+            met, out = check(text, root, "deadbeef", 5, floor, btext)
@@
-        scratch = tempfile.mkdtemp(prefix="c-", dir=base)
-        met, out = check(HDR + row(good), root, scratch, "deadbeef", 5, 1)
+        met, out = check(HDR + row(good), root, "deadbeef", 5, 1)
```
The modified bytes also persist at `$S/b/.ufo/waves/round-49/` (`count-c1.py` sha256 `6dedc49c…`,
`count-c2.py` `01b3a42a…`, witness `103e71de…`) so an integrator can `cp` rather than re-play the patch.
`main`'s `scratch` in the witness is **kept** — after the deletions it is still used by
`export_rev(repo, args.rev, scratch)` and the `rmtree` in the `finally`.

## 7. Candidates found, deliberately not applied (unproven)

- **Duplicated staging convention (the one with teeth)** — `plan()` `stage()` (`count-c1.py:252-270`) and
  `plan_text_only()` (`:434-449`) repeat the same eight lines (opaque tag → write `s-<tag>.md` → job tuple),
  and `measure()` (`:281-295`) / `measure_text_only()` (`:452-459`) repeat the loop. The copy has already
  diverged: `plan_text_only` appends a `real-opaque` job at `:445-446` pointing at
  `s-<tag>.md` but never writes that file (the `with open(...)` at `:440-442` runs only inside the variant
  loop), and it hardcodes `LANE` as the repo (`:444,447`) so it cannot follow `--repo`. A shared
  `_stage(scratch, rev, name, expect, body)` would delete ~20 lines and one authority for the tuple shape.
  Not applied: it restructures the selftest path and needs its own real run. Corroboration, not my
  measurement: the round-49 mutation seat reports that a `plan()` stage-path defect survives the selftest
  44/44 (`w1/Mo49RevC1Counter.md:222` K04), which is exactly the blind spot this duplication creates.
  Successor-round candidate, HIGH value for the selftest's reach; the deletion itself is low-risk but
  unproven here.
- **`plan_text_only` return arity** — collapsing `return jobs, None` to `return jobs` (item 7) changes a
  function that one wave-1 scratch harness unpacks as a tuple. The frozen counter keeps the old shape, and
  a successor that lands item 7 should re-point or drop that harness rather than carry it.
- **Witness re-parses the registry** — `check()` calls `parse_registry(text)` three times (four with a
  baseline; `pin_keys`/`pin_bindings` each parse again). `parse_registry` is pure, so aggregating the loops
  over one list cannot change output. Not applied: no output change but no deletion either (it removes
  repeated work, not code), and it edits the hot function in a calibration round. LOW value.
- **`count-c1.py:377`** still reads `order = [j[0] for j in (pl or [])]` — the same unreachable-`None`
  fallback I collapsed at `:374`. Left as-is on purpose so the A/B run measures one frozen modification set;
  it is a one-token change in the successor.
- **`sniff_run`'s four unused parameters** (`count-c1.py:397`) are the callback contract of
  `measure_text_only`'s 7-argument call; renaming them `_tool`/`_rrev`/… is cosmetic, not weight.

## 8. Preserved contract

- Frozen bytes untouched and equal to `evidence/freeze-sha256.txt`; no tracked lane file modified
  (`git status --porcelain --untracked-files=no` empty); no git/jj mutation; `shokuknow` not opened.
- The C1 predicate line, the C2 predicate line, all three selftest tally lines and the witness's
  `PIN_CHECK=` line are unchanged by the deletions (tables in §4-§5).
- A successor counter keeps: opaque handles, the fixture-repository honest/junk pair, the `ORDER`/`vars`
  arithmetic, the `pins`/`provenance`/`source_rows` arms of C2, and the R9/R10/R11 rules of the tool.
- Edited scope: only `.scratch/r49-Mo49SimpCounters/` and this report.

## 9. Note for the landing target

`tools/mori-pin-check.py` (v3, sha256 `85a89a3b…`) carries the same two unused parameters as the witness —
`trunc_digest_pins(st, raw, root)` at `tools/mori-pin-check.py:313` and `run_cmd(words, root, scratch,
timeout)` at `:400` (ruff ARG001 on the landed tool: exactly these two). The `check()` scratch chain does
**not** exist in v3 (v3's `check` has no scratch parameter), so items 12-13 apply to the tool today and item
14 applies only once the witness's `check()` lands.

## Findings

1. **MED** — `.ufo/waves/round-49/count-c1.py:372-373`: the `plan_ok` selftest arm asserts `err is None`
   where `plan_text_only` has no failure path, so the arm cannot fail while counting toward
   `C1_SELFTEST pass=44`. An unfalsifiable arm in a calibration counter's own receipt (see also the
   hit at `count-c2.py` selftest `sources_floor_unmet`, which is a `not met` check and does fail).
2. **MED** — `.ufo/waves/round-49/count-c1.py` `--rev`: the counter resolves a moving ref once at start, so
   `--rev HEAD` in two receipts can compare different revisions with no other warning than the `rev=` field.
   Observed live: my first A/B pair printed `rev=0df17b7b…` and `rev=24ebc799…`. Receipts for the successor
   round should pin the sha.
3. **MED** — `.ufo/waves/round-49/count-c1.py:445-446`: `plan_text_only` appends a `real-opaque` job whose
   staged path `s-<opaque(rev, text)>.md` is never written (the write at `:440-442` runs only inside the
   variant loop), while `plan()` stages the same copy correctly (`:266`). Invisible today because the
   selftest injects a fake runner that never opens the path; a real runner on that job scores `error`,
   which the counter counts as `errors≠0` → a false `unmet`.
4. **MED** — `.ufo/waves/round-49/count-c1.py:252-261` vs `:434-449`: the staging logic exists twice, and the
   selftest only exercises the copy — so a defect in the production `plan()`/`stage()` path is invisible to
   `C1_SELFTEST pass=44` (independently measured by `w1/Mo49RevC1Counter.md:222` K04, which survives 44/44).
   This is the highest-value deletion in the file and the reason item 7's arity change should ride with it.
5. **LOW** — `.ufo/waves/round-49/count-c1.py:73`: `_cur_pin` carries an unused `cmd_hint` parameter (a
   half-finished API from an earlier shape).
6. **LOW** — `.ufo/waves/round-49/count-c1.py:157-158` vs `:65`: `FIX_HEADER` duplicates the `HEADER`
   literal byte-for-byte — two authorities for the gate-table header.
7. **LOW** — `.ufo/waves/round-49/count-c1.py:248,281,289,449,459`: dead defaults (`plan`), an unused
   injection seam (`run=run_tool`), and two always-`None` return elements.
8. **LOW** — `.ufo/waves/round-49/count-c2.py:79`: `header = header if rows else None` always yields
   `None`; the conditional suggests a state that cannot occur.
9. **LOW** — `.ufo/waves/round-49/count-c2.py:99,101,260,270-271,311`: unused `copies` seam, unused
   `drop` parameter with an untaken branch, and an unreachable `only2[:8]` ternary (`len(only2)` is 5).
10. **LOW** — `.ufo/waves/round-49/controls/tool-r48-merged-witness.py:253` vs `:264`: the docstring says
    hidden-row detection covers "up to three leading spaces, then `|`" while the code uses `^\s*\|` (any
    indent) and also counts `<td>/<tr>` rows, which the paragraph never mentions. The witness's widened rule
    is what makes N4/N7 unmet, so the *code* is the intent and the docstring is the stale half — a landing
    target would inherit the stale spec.
11. **LOW** — `.ufo/waves/round-49/controls/tool-r48-merged-witness.py:346,433,485` (and
   `tools/mori-pin-check.py:313,400`): unused `raw`/`scratch` parameters; in the witness the `scratch`
   parameter is threaded through `check()` into `run_cmd()` where it is ignored, and the selftest creates 41
   per-case temp dirs only to pass that argument.

Report: .ufo/waves/round-49/w1/Mo49SimpCounters.md
