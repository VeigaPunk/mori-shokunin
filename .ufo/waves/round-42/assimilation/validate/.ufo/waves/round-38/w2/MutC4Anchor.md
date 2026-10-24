# MutC4Anchor — one-byte anchor mutation against C4 `check anchors`

**Seat:** MoriR38.MutC4Anchor (wave 2, falsify)
**Claim under attack:** C1/C4 — every `anchor:` line of the round-38 knowledge entry must occur
byte-exactly in `tools/mori-source-drift.py` at the measured revision
(`.ufo/waves/round-38/count-c4.py:137-143`, `:169-172`, `MIN_ANCHORS = 3` at `:49`).
**Verdict: KILLED** — the mutant flips `check anchors` to FAIL, `C4=unmet`, exit 1, while
the pristine and restored bytes print `C4=met`, exit 0, and no other check moves.

## Mutant

A fresh sandbox clone of the lane was made in my scratch and detached at the scored tip:

```
git clone /home/vgpnk/Projects/shokunin/mori-shokunin .ufo/waves/round-38/scratch/MutC4Anchor/sandbox
git -C sandbox checkout --detach f725f3076972e6e70595b5ac8279be524a111ff8
HEAD=f725f3076972e6e70595b5ac8279be524a111ff8   STATUS=[]
```

One byte inside one `anchor:` string of `corpus/knowledge/source-drift-content-anchor-r38.md`
(line 27), colon → semicolon:

```diff
@@ -24,7 +24,7 @@
    anchor: FETCH_MAX_BYTES = 4 * 1024 * 1024
-   anchor: if not _public_redirect_target(final):
+   anchor: if not _public_redirect_target(final);
    anchor: return "drifted"
```

Byte-level confirmation (`cmp -l` over the two committed blobs) — **exactly one differing byte**,
0-based offset 1619 / 1-based 1620, octal 072 (`:`) → 073 (`;`):

```
===NUMSTAT===
1	1	corpus/knowledge/source-drift-content-anchor-r38.md
===BYTE-CMP(all differing bytes)===
1620  72  73
```

The real tool carries the pristine string at `tools/mori-source-drift.py:158`, so the mutated
anchor cannot resolve. Committed only in the sandbox (parent = scored tip, one file, 1 insertion /
1 deletion):

```
MUTANT_COMMIT=6a997d1ece5203495ca3d1eecd269a09a14a7b6a
PARENT=f725f3076972e6e70595b5ac8279be524a111ff8
MUTANT_BLOB_SHA=67eccee3f872dcd2c8e052f366d422295898a8b1   (pristine blob 06e7ea0…)
MUTANT_SHA256=aa18031891c88d5355a74f3aec24159d4f19af62b602d453130db639af79392c
```

## Detector runs (bounded, same command each leg)

Counter reads committed objects at the rev it is given (`git -C repo show <rev>:<path>`,
`.ufo/waves/round-38/count-c4.py:124`), so the mutant is measured at the commit that carries it;
the pristine byte-identical base is measured at `f725f30`.

1. **Baseline — pristine bytes at `f725f30`, same sandbox** (`scratch/…/baseline-mine.txt`):

   ```
   check anchors          PASS (anchors=3 missing=[])
   C4=met        exit 0
   ```

2. **Mutant — commit `6a997d1` in the sandbox** (`scratch/…/mutant-mine.txt`):

   ```
   check anchors          FAIL (anchors=3 missing=['if not _public_redirect_target(final);'])
   check capability       PASS (paths=['tools/mori-source-drift.py', '.ufo/waves/round-37/evidence/c2-after-v3.txt', '.ufo/waves/round-37/evidence/drift-live-r37.txt'] missing=[])
   check live_rows        PASS (named=10 summary_drifted=10 unknown=[])
   check named_row_drift  PASS (exit=0 row_states=('PASS', ''))
   check drift_kill       PASS (exit=1 row_states=('FAIL', "…('S103', 'excerpt')…"))
   C4=unmet      exit 1
   ```

   All three fabricated witnesses are still `rejected`; only the anchors line flips, so the
   kill is attributable to the one-byte entry mutation and nothing else.

3. **Restored — pristine bytes at `f725f30` after reset** (`scratch/…/restored-mine.txt`):

   ```
   check anchors          PASS (anchors=3 missing=[])
   C4=met        exit 0
   ```

Instrument control, run as worded in the ticket against the same mutant sandbox **while its HEAD
was the mutant commit**, `count-c4.py f725f30 --repo <sandbox>` (`scratch/…/mutant-rev-literal.txt`):
`check anchors PASS`, `C4=met`, exit 0. This is not a survivor — `f725f30` names the pristine tree
and the counter deliberately reads committed bytes at the rev (`count-c4.py:124`), so a mutation
committed on top is outside that rev's bytes. The discriminating measurement is the descendant
commit `6a997d1` shown in leg 2. Wave-1 sibling scratch `scratch/MutC4Anchor/` (a stale clone whose
mutant sat on `daa1d4d`, i.e. *before* the scored tip) was not reused; every line above was
re-derived in the fresh clone.

## Restoration evidence

```
git reset --hard f725f3076972e6e70595b5ac8279be524a111ff8
RESTORED_HEAD=f725f3076972e6e70595b5ac8279be524a111ff8
RESTORED_BLOB=06e7ea067f53e56a4a26358838add7e5c9e897f2
RESTORED_SHA256=0fd361d4d0c0d1b70f07b03661b22fb9af0c2b3c3a0fc24f2700f68506736005
RESTORED_STATUS=[]
```

`0fd361d4…` equals the pristine content hash recorded before the mutation and equals the lane's
working-tree file hash. Restore re-run of the detector on restored bytes is leg 3 above.

## Lane untouched

```
LANE_STATUS=[]
LANE_SHA256=0fd361d4d0c0d1b70f07b03661b22fb9af0c2b3c3a0fc24f2700f68506736005
LANE_TIP(blob)=06e7ea067f53e56a4a26358838add7e5c9e897f2
```

`git -C <lane> status --porcelain -- corpus/knowledge/source-drift-content-anchor-r38.md` is empty
before and after the probe; the lane's file matches `f725f30`'s blob. The only lane-relative file
written by this seat is this report; all scratch lives under
`.ufo/waves/round-38/scratch/MutC4Anchor/`. No installs or upgrades were made (tooling directive
not exercised).

## Coverage note

Anchor discrimination is substring-based (`:171`). This probe shows a single-byte divergence in a
git-tracked entry is detected at pair-granularity through the committed-bytes path. It says nothing
about an anchor that is *satisfied by an unrelated occurrence* in the tool, and nothing about
mutations applied only to a working tree while the counter is asked for the pristine rev — see the
literal-rev control above, which is a property of rev-addressed measurement, not a counter defect.
