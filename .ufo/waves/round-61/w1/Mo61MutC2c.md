# Mo61MutC2c — C2 row-grammar mutation receipts

Axes: detector discrimination, grammar fidelity, byte restoration, containment.

## Verdict

**Three behavior-bearing mutants survive the usable committed witness set: ROUTED DEFECT / coverage finding, not permission to amend the frozen counter.** Default `--selftest` fails already on pristine, so that detector is inconclusive, not a kill. The explicit synthetic-fixture invocation `--selftest --floor 6` passes 10/10 on pristine, all mutants, and restored bytes. Both committed control states remain identically unmet. No integrated ledger or live after-state was certified.

## Method and command templates

Scratch: `/fast/scratch/hyaku/mori-r61/Mo61MutC2c`; TMPDIR set there; every CLI invocation has `--scratch <seat scratch>/runs/<variant>/<detector>`. Lane paths are absolute. Frozen counter: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/count-c2.py`.

```text
python3 <scratch counter> --selftest --scratch <scratch detector directory>
python3 <scratch counter> --selftest --floor 6 --scratch <scratch detector directory>
python3 <scratch counter> 325f7e639916fcbc77fa2ec7475951a1b86bb1cb --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch <scratch detector directory>
python3 <scratch counter> 7370a731abcafc4c803111de7c22cd6264d63be1 --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch <scratch detector directory>
```

These four identical detectors were run on pristine, each mutant, and each byte-restored scratch file. Required selftests internally create and commit their own scratch fixture repositories (counter lines 209–242); no separate fixture-builder Git mutations were executed. Committed lane controls are read through `git -C <absolute lane> show`. No lane/fleet VCS state was changed.

## Kill table

| Mutant | Default selftest | Synthetic floor-6 selftest | Enter / freeze controls | Committed-witness verdict |
|---|---|---|---|---|
| M1-quote-nobacktick | 9 pass / 1 fail, rc=1: baseline failure, inconclusive | 10/10, rc=0, identical | both rc=1, identical entry_absent | survived: ROUTED DEFECT |
| M2-extra-midcols | 9 pass / 1 fail, rc=1: baseline failure, inconclusive | 10/10, rc=0, identical | both rc=1, identical entry_absent | survived: ROUTED DEFECT |
| M3-anchor-casefold | 9 pass / 1 fail, rc=1: baseline failure, inconclusive | 10/10, rc=0, identical | both rc=1, identical entry_absent | survived: ROUTED DEFECT |

## Actual outputs

Default pristine selftest:
```text
case good: ok=False want=True FAIL failed=['pointer_floor:6<40']
case quote-missing: ok=False want=False pass failed=['quote_missing:a.rst:5-7', 'pointer_floor:6<40']
case row-missing: ok=False want=False pass failed=['rows_missing:a.rst:5-7', 'pointer_floor:6<40', 'rows_ne_pointers']
case orphan: ok=False want=False pass failed=['rows_orphan:b.c:25', 'quote_words:b.c:25', 'pointer_floor:6<40', 'rows_ne_pointers']
case small-span: ok=False want=False pass failed=['span_small:a.rst:5-7', 'pointer_floor:6<40']
case dup-quote: ok=False want=False pass failed=['quote_dup:a.rst:9', 'pointer_floor:6<40']
case not-mined: ok=False want=False pass failed=['rows_src:a.rst', 'rows_src:b.c', 'rows_src:c.txt', 'rows_src:d.h', 'pointer_floor:6<40']
case usedby-miss: ok=False want=False pass failed=['rows_src:a.rst', 'rows_src:b.c', 'rows_src:c.txt', 'rows_src:d.h', 'pointer_floor:6<40']
case tampered-copy: ok=False want=False pass failed=['copy_pin:a.rst', 'loc_bad:a.rst:5-7', 'loc_bad:a.rst:9', 'sources_floor', 'pointer_floor:6<40']
case no-prov: ok=False want=False pass failed=['provenance', 'pointer_floor:6<40']
C2_SELFTEST pass=9 fail=1
rc=1
```

Floor-6 pristine selftest (all mutants identical):
```text
case good: ok=True want=True pass failed=[]
case quote-missing: ok=False want=False pass failed=['quote_missing:a.rst:5-7']
case row-missing: ok=False want=False pass failed=['rows_missing:a.rst:5-7', 'rows_ne_pointers']
case orphan: ok=False want=False pass failed=['rows_orphan:b.c:25', 'quote_words:b.c:25', 'rows_ne_pointers']
case small-span: ok=False want=False pass failed=['span_small:a.rst:5-7']
case dup-quote: ok=False want=False pass failed=['quote_dup:a.rst:9']
case not-mined: ok=False want=False pass failed=['rows_src:a.rst', 'rows_src:b.c', 'rows_src:c.txt', 'rows_src:d.h']
case usedby-miss: ok=False want=False pass failed=['rows_src:a.rst', 'rows_src:b.c', 'rows_src:c.txt', 'rows_src:d.h']
case tampered-copy: ok=False want=False pass failed=['copy_pin:a.rst', 'loc_bad:a.rst:5-7', 'loc_bad:a.rst:9', 'sources_floor']
case no-prov: ok=False want=False pass failed=['provenance']
C2_SELFTEST pass=10 fail=0
rc=0
```

Floor-6 output matches committed selftest-c2.txt excluding rc line: True

Control outputs, identical across pristine, mutated and restored:
```text
C2=unmet pointers=47 rows=0 same=0 moved=0 changed=0 quotes_ok=0 spans_ok=0 sources=0 failed=entry_absent rev=325f7e639916fcbc77fa2ec7475951a1b86bb1cb
rc=1
C2=unmet pointers=47 rows=0 same=0 moved=0 changed=0 quotes_ok=0 spans_ok=0 sources=0 failed=entry_absent rev=7370a731abcafc4c803111de7c22cd6264d63be1
rc=1
```

## Exact mutations and behavior-bearing probes

The required selftest generated a committed positive fixture at `c44d966df7f2cbb125171be5b9ff03fb895bfd6f` in seat scratch. For supplementary probes, imported each scratch counter, set FILES/PINS/NAMES to that same four-file synthetic fixture as selftest does, and overlaid only cat(..., LEDGER) in memory; measure(..., floor=6) and fmt were unchanged. These hostile overlays are NOT committed hostile trees or CLI exit observations. No separate fixture Git mutation was run. All-good overlay meets for all variants.

### M1-quote-nobacktick
```diff
-    r"\s*([a-zA-Z0-9_.\-]+:\d+(?:-\d+)?|-)\s*\|\s*`([^`]*)`\s*\|")
+    r"\s*([a-zA-Z0-9_.\-]+:\d+(?:-\d+)?|-)\s*\|\s*`?([^`]*)`?\s*\|")
```
```text
pristine: C2=unmet pointers=6 rows=5 same=3 moved=1 changed=1 quotes_ok=5 spans_ok=5 sources=4 failed=rows_missing:a.rst:5-7;rows_ne_pointers rev=c44d966df7f2cbb125171be5b9ff03fb895bfd6f
mutant:   C2=met pointers=6 rows=6 same=4 moved=1 changed=1 quotes_ok=6 spans_ok=6 sources=4 failed=none rev=c44d966df7f2cbb125171be5b9ff03fb895bfd6f
```

### M2-extra-midcols
```diff
-    r"\s*([a-zA-Z0-9_.\-]+:\d+(?:-\d+)?|-)\s*\|\s*`([^`]*)`\s*\|")
+    r"\s*([a-zA-Z0-9_.\-]+:\d+(?:-\d+)?|-)\s*\|(?:[^|`]*\|)*?\s*`([^`]*)`\s*\|")
```
```text
pristine: C2=unmet pointers=6 rows=5 same=3 moved=1 changed=1 quotes_ok=5 spans_ok=5 sources=4 failed=rows_missing:a.rst:5-7;rows_ne_pointers rev=c44d966df7f2cbb125171be5b9ff03fb895bfd6f
mutant:   C2=met pointers=6 rows=6 same=4 moved=1 changed=1 quotes_ok=6 spans_ok=6 sources=4 failed=none rev=c44d966df7f2cbb125171be5b9ff03fb895bfd6f
```

### M3-anchor-casefold
```diff
-    pset = set(pointers)
+    pset = {p.lower() for p in pointers}
-        copies[f] = b.decode("utf-8", "replace")
+        copies[f.lower()] = b.decode("utf-8", "replace")
-            rows.append(m.groups())
+            rows.append(tuple([x.lower() for x in m.groups()[:3]] + [m.groups()[3]]))
```
```text
pristine: C2=unmet pointers=6 rows=6 same=3 moved=1 changed=1 quotes_ok=5 spans_ok=6 sources=4 failed=rows_missing:a.rst:5-7;rows_orphan:A.RST:5-7;loc_bad:A.RST:5-7 rev=c44d966df7f2cbb125171be5b9ff03fb895bfd6f
mutant:   C2=met pointers=6 rows=6 same=4 moved=1 changed=1 quotes_ok=6 spans_ok=6 sources=4 failed=none rev=c44d966df7f2cbb125171be5b9ff03fb895bfd6f
```

Hostile alterations affect only the first row: remove quote backticks; insert an `extra` cell between location and quote; or change `a.rst:5-7` to `A.RST:5-7`. The new overlays demonstrate behavior changes but do not retroactively constitute committed witnesses.

**Extra trailing columns are already accepted by pristine** (ROW is a prefix match), so M2 specifically admits extra middle cells. A trailing-column-only relaxation is not behavior-bearing here. No stricter column-count contract is inferred.
```text
C2=met pointers=6 rows=6 same=4 moved=1 changed=1 quotes_ok=6 spans_ok=6 sources=4 failed=none rev=c44d966df7f2cbb125171be5b9ff03fb895bfd6f
```

## Frozen evidence pointers

All paths below are relative to `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/`.
- `count-c2.py:41–43,119–122`: row grammar and prefix matching.
- `count-c2.py:100,117,124–133,145–149`: exact anchor set and copy-key lookup.
- `count-c2.py:261–273`: ten cases; none tests missing backticks, extra middle cells, or anchor-case differences.
- `count-c2.py:38,183–184,291,297`: default floor 40 reaches six-pointer selftest; default baseline fails. Floor 6 used only for the synthetic selftest, never controls.
- `count-c2.py:101–104`: missing ledger short-circuits grammar, explaining control nondiscrimination.
- `evidence/control-c2-do-nothing.txt:1–2`; `evidence/selftest-c2.txt:1–12`: committed receipts.

## Restoration evidence

| Mutant | Before and restored SHA-256 | Mutated SHA-256 |
|---|---|---|
| M1-quote-nobacktick | `82d0fee6124685f8a50f93550f3665703a33dce644948958db642a77d5aec2d8` | `5d57c4d82fe635a6054e47b79b837186a24167058efd9a0c227820edac3d25ac` |
| M2-extra-midcols | `82d0fee6124685f8a50f93550f3665703a33dce644948958db642a77d5aec2d8` | `a28beb0dfa639d63c26e51d08a3e72ce4657da54809bc895fc4129c73bdd12fd` |
| M3-anchor-casefold | `82d0fee6124685f8a50f93550f3665703a33dce644948958db642a77d5aec2d8` | `bc9275b88e0a5fe6b6ab549a60b79e3f5ab68fc368b6a8d57ddb34fc58c41a92` |

Each scratch mutant was restored byte-for-byte and the same four CLI detectors rerun: every restored `(rc, stdout, stderr)` equals pristine. Lane counter was never written; before/after SHA-256 remains `82d0fee6124685f8a50f93550f3665703a33dce644948958db642a77d5aec2d8`.

Disk guard green: scratch 370.6G free, /tmp 97.5G, /var/tmp 533.8G. No ENOSPC or tool installs. No production, registry, fleet, sibling or lane VCS-state writes. Required selftests internally initialize/commit their own scratch fixtures; no independent fixture-builder Git mutations ran. The unexecuted general fixture-builder draft was discarded. Receipts copied here before scratch removal. No amendment, remediation, integration or live-after certification proposed.

Self-evaluation: accuracy 4/5 (hostile probes explicitly overlays); completeness 4/5 (default selftest inconclusive, usable synthetic invocation separately identified); clarity 4/5 (survival distinguished from new differential probes); actionability 4/5 (exact diffs, hashes and pointers retained); conciseness 4/5 (full receipts lengthen report). Overall 4.0/5. User-alignment: detection/report only.
