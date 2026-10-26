# Mo49MutC2Counter — mutation test of the frozen C2 counter (`count-c2.py`)

Seat: w1 mutation-tester · 2026-10-25 · lane `mori-shokunin` · leaf seat, no subagents used.
Target under test: `.ufo/waves/round-49/count-c2.py` (frozen). Kill rule: a mutant is
**killed iff `--selftest` exits non-zero**. All work in
`.scratch/r49-Mo49MutC2Counter/` (`pristine/` + `m01`–`m10/` + `probe_survivors.py`); the
frozen counter was never modified. No tools installed (operator authorization read, none
needed); every run used `TMPDIR=…/.scratch/r49-Mo49MutC2Counter/tmp`; no pacman, no
mutating git/jj, no host config reads. No credential or session material and no host
machine id appears in any output; nothing to redact.

## Baseline (pristine detector)

```
$ cp .ufo/waves/round-49/count-c2.py .scratch/r49-Mo49MutC2Counter/pristine/count-c2.py
$ sha256sum <frozen> <scratch pristine copy>
be39475d997f5cf4e67c7d69f66f176b1632985451ed0a6b8a5a4c2a495dd837  .ufo/waves/round-49/count-c2.py
be39475d997f5cf4e67c7d69f66f176b1632985451ed0a6b8a5a4c2a495dd837  .scratch/r49-Mo49MutC2Counter/pristine/count-c2.py
$ grep count-c2 .ufo/waves/round-49/evidence/freeze-sha256.txt
3:be39475d997f5cf4e67c7d69f66f176b1632985451ed0a6b8a5a4c2a495dd837  .ufo/waves/round-49/count-c2.py
$ TMPDIR=$S/tmp python3 $S/pristine/count-c2.py --selftest
C2_SELFTEST pass=26 fail=0        # exit=0
```

Working-tree counter bytes equal the freeze receipt, so the baseline is conclusive.

## Battery: 10 single-point mutants, detector = `--selftest`

Mutant scripts live at `.scratch/r49-Mo49MutC2Counter/m01..m10/count-c2.py`; the layout
(`<lane>/.scratch/<seat>/mNN/count-c2.py`) keeps the selftest's 3×-dirname lane
resolution pointing at the real lane, so each run reads the real committed source copies.

| mutant | single point (frozen-file line) | expected detector | observed | verdict |
|---|---|---|---|---|
| m01 | drop opened-date check (L161) | `row_opened_other_day_unmet` FAILs | exit=1, that check FAIL, pass=25 fail=1 | **killed** |
| m02 | drop used-by check (L162) | `used_by_missing_unmet` FAILs | exit=1, that check FAIL, pass=25 fail=1 | **killed** |
| m03 | drop unique-quote check (L146) | `duplicate_quote_unmet` FAILs | exit=1, that check FAIL, pass=25 fail=1 | **killed** |
| m04 | drop sources floor (L175) | `sources_floor_unmet` FAILs | exit=0, pass=26 fail=0 | **survived** |
| m05 | `MIN_WORDS` 6→1 (L34) | `short_quote_unmet` FAILs | exit=0, pass=26 fail=0 | **survived** |
| m06 | `MAX_WORDS` 25→99 (L34) | `long_quote_unmet` FAILs | exit=0, pass=26 fail=0 | **survived** |
| m07 | drop pin check (L108) | `pin_mismatch_unmet` FAILs | exit=1, that check FAIL, pass=25 fail=1 | **killed** |
| m08 | accept other-copy locations (L166) | `quote_from_wrong_copy_unmet` FAILs | exit=0, pass=26 fail=0 | **survived** |
| m09 | accept status `queued` (L160) | `row_not_mined_unmet` FAILs | exit=1, that check FAIL, pass=25 fail=1 | **killed** |
| m10 | stop dropping `<script>` text in `normalise` (L60) | `normalise_drops_script_text` FAILs | exit=1, that check FAIL, pass=25 fail=1 | **killed** |

Raw runs (`exit=` is the selftest exit code; PASS lines omitted):

```
=== m01 exit=1   FAIL row_opened_other_day_unmet   C2_SELFTEST pass=25 fail=1
=== m02 exit=1   FAIL used_by_missing_unmet        C2_SELFTEST pass=25 fail=1
=== m03 exit=1   FAIL duplicate_quote_unmet        C2_SELFTEST pass=25 fail=1
=== m04 exit=0   C2_SELFTEST pass=26 fail=0
=== m05 exit=0   C2_SELFTEST pass=26 fail=0
=== m06 exit=0   C2_SELFTEST pass=26 fail=0
=== m07 exit=1   FAIL pin_mismatch_unmet           C2_SELFTEST pass=25 fail=1
=== m08 exit=0   C2_SELFTEST pass=26 fail=0
=== m09 exit=1   FAIL row_not_mined_unmet          C2_SELFTEST pass=25 fail=1
=== m10 exit=1   FAIL normalise_drops_script_text  C2_SELFTEST pass=25 fail=1
```

Each kill is exactly the expected single check flipping to FAIL; no collateral flips.

## Mutant diffs (unified, one hunk each)

```diff
--- m01 (L161)
-                          and srow[8] == OPENED
+                          and True
--- m02 (L162)
-                          and entry_path in [u.strip() for u in re.split(r"[,;]", srow[10])])
+                          and True)
--- m03 (L146)
-            if not (MIN_WORDS <= len(words) <= MAX_WORDS) or q in seen_quotes:
+            if not (MIN_WORDS <= len(words) <= MAX_WORDS):
--- m04 (L175)
-        if len(used_sources) < MIN_SOURCES:
+        if False:
--- m05 (L34)
-MIN_WORDS, MAX_WORDS = 6, 25
+MIN_WORDS, MAX_WORDS = 1, 25
--- m06 (L34)
-MIN_WORDS, MAX_WORDS = 6, 25
+MIN_WORDS, MAX_WORDS = 6, 99
--- m07 (L108)
-        if b is None or hashlib.sha256(b.encode("utf-8", "surrogateescape")).hexdigest() != digest:
+        if False:
--- m08 (L166)
-            if q in norm[url]:
+            if q in " ".join(norm.values()):
--- m09 (L160)
-… and srow[7] == "mined"
+… and srow[7] in ("mined", "queued")
--- m10 (L60)
-    t = re.sub(r"<(script|style)\b.*?</\1\s*>", " ", text, flags=re.S | re.I)
+    t = re.sub(r"<(style)\b.*?</\1\s*>", " ", text, flags=re.S | re.I)
```

## Why the four survivors pass (probe evidence)

`.scratch/r49-Mo49MutC2Counter/probe_survivors.py` replays the selftest scenarios under
pristine and each survivor and prints the real `evaluate()` line (read-only; reads lane
copies, writes nothing). All probes are unmet under pristine except the `clean_*` cases,
which pristine rejects — the probe discriminates, the battery does not.

**m04 — sources floor.** The battery's only floor control (`only2`, L309-312) is a
5-row table containing a duplicate quote, and its check asserts only `not met`:

```
pristine clean_two_sources8  met=False … claims=8 located=8 … sources=2 … failed=sources_floor
m04      clean_two_sources8  met=True  … claims=8 located=8 … sources=2 …          (exit 0)
```

An 8-row table over 2 distinct sources (all quotes unique and located, provenance ok)
scores `C2=met` under m04. The control can never see the floor because it fails earlier
via `claims_floor` (5 < 8) and `bad_rows`/`source_rows` (the planted duplicate).

**m05 / m06 — quote word bounds.** `short_quote_unmet` (L300) and `long_quote_unmet`
(L303) assert `"bad_rows" in line`, but the summary line always carries the literal
field name `bad_rows=N`, so the substring matches even when `bad_rows=0`:

```
vacuity demo: substring 'bad_rows' in an unmet line with bad_rows=0 -> True
m05 selftest_short  met=False … quote_missing=1 bad_rows=0 … failed=quote_missing   (check PASSES on this)
m06 selftest_long   met=False … quote_missing=1 bad_rows=0 … failed=quote_missing   (check PASSES on this)
```

Under m05 the 2-word control quote is accepted by the length gate and rejected only by
location (`quote_missing`), which the check cannot tell from a length rejection. On
clean inputs the mutants really open the bounds:

```
pristine clean_short_located (3-word quote)  met=False … bad_rows=1 … failed=bad_rows,source_rows
m05      clean_short_located (3-word quote)  met=True  … claims=8 located=8 bad_rows=0
pristine clean_long_located  (30-word quote) met=False … bad_rows=1 … failed=bad_rows,source_rows
m06      clean_long_located  (30-word quote) met=True  … claims=8 located=8 bad_rows=0
```

**m08 — location bound to the row's own copy.** The wrong-copy control (L293-297)
appends `" x"` to the cross-copy quote, so the exact string occurs in *no* copy and the
mutant still rejects it as `quote_missing`; the check passes. Without the poison the
mutant locates across copies:

```
pristine clean_cross_copy  met=False … quote_missing=1 … failed=quote_missing   (S902 row, quote from journald.conf copy)
m08      clean_cross_copy  met=True  … claims=8 located=8 bad_rows=0 …           (same table accepted)
```

So "each quote occurs in the committed copy of that row's own source" is unguarded by
the battery: any future weakening of L166 to any-copy (or a substring/prefix match)
would leave `C2_SELFTEST pass=26 fail=0`.

## Restoration evidence

The lane file was never edited; mutants are separate scratch copies.

```
after battery: sha256sum .ufo/waves/round-49/count-c2.py $S/pristine/count-c2.py
be39475d997f5cf4e67c7d69f66f176b1632985451ed0a6b8a5a4c2a495dd837  (both — identical to freeze receipt and to pre-battery hash)
$ TMPDIR=$S/tmp python3 $S/pristine/count-c2.py --selftest   # restored bytes, same detector
pristine-rerun-exit=0, 26 PASS lines, C2_SELFTEST pass=26 fail=0
```

## Limits

- This tested only the counter's own `--selftest` battery as kill oracle, per the
  tasking; the full predicate run (`count-c2.py R`) and the C1 counter were not scored.
- Survivors are coverage findings about the frozen counter; per the contract the
  counter is the claim's rule and is not changed by this seat. Wave 2 reviewers should
  treat the four arms above (`sources=…` floor, 6-25 word bounds, own-copy location) as
  battery-unguarded and re-check them by hand against landed data.
- The m08 probe's clean cross-copy table is synthetic (selftest fixtures), not lane
  data; it demonstrates the mutant's behavior, not a defect in any landed entry.

## Findings

- **HIGH** — `.ufo/waves/round-49/count-c2.py:166` + selftest `:293-297`: the
  `quote_from_wrong_copy_unmet` control poisons its cross-copy quote with a trailing
  `" x"`, so the `quote_from_wrong_copy` arm cannot kill a mutant that accepts
  other-copy locations (m08 survived; a clean cross-copy quote scores `C2=met
  located=8` under the mutant). Quote-to-own-source binding is unguarded by the
  battery.
- **MED** — `.ufo/waves/round-49/count-c2.py:300,303`: `short_quote_unmet` and
  `long_quote_unmet` assert `"bad_rows" in line`, which matches the always-present
  summary field `bad_rows=0`, so any unmet outcome satisfies them; m05 (`MIN_WORDS`
  6→1) and m06 (`MAX_WORDS` 25→99) both survived with `pass=26 fail=0`.
- **MED** — `.ufo/waves/round-49/count-c2.py:309-312`: the sources-floor control is a
  5-row table with a planted duplicate, so it fails via `claims_floor`/`bad_rows`
  regardless of the floor check, and the check asserts only `not met`; m04 (floor
  dropped) survived, and an 8-row/2-source table scores `C2=met … sources=2` under it.
- **LOW** — `.ufo/waves/round-49/count-c2.py:34,175`: the same floor/bounds constants
  are also reachable via `MIN_SOURCES`, which no battery arm pins directly (adjacent to
  the m04 finding; not separately mutated).
