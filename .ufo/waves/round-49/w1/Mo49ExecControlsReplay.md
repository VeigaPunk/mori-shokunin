# Mo49ExecControlsReplay — independent replay of the round-49 frozen controls

Seat: wave 1 executor (controls replay). Lane: `mori-shokunin`. Date: 2026-10-25.
Read first: `.ufo/waves/round-49/contract.md` (committed at freeze `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115`).
Lane HEAD during this seat: `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115`; `git status --porcelain | grep -v '^??'`
printed nothing (`rc=1`) and `git diff HEAD --stat` was empty, so the worktree tracked bytes equal the freeze commit.
Host at start: `nproc` = 32, `/proc/loadavg` = `50.18 28.29 28.41`. No tool was installed or upgraded (nothing was
needed; `/usr/bin/time` is absent on this host, so the shell builtin `time` was used for the one timed run).
All lane-tool runs used `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecControlsReplay`;
scratch residue is confined to that directory (30M). Nothing outside my report and that scratch directory was written.

Every command below is reproduced with its observed output and exit code. Where my capture wrapper differs from the
committed receipt by a trailing `exit=N` line, that is called out explicitly — the committed receipts were produced by
a wrapper that appended `exit=$?`; my runs appended the same number only to the shell's exit status, not to the file.

## 1. Counter selftests

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ TMPDIR=…/r49-Mo49ExecControlsReplay/s python3 .ufo/waves/round-49/count-c1.py --selftest
…
PASS filename_sniffer_not_met  C1=unmet junk_met=17 honest_unmet=0 real=met errors=0 variants=24 rev=0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115
PASS order_covers_every_variant  27
PASS fixture_False_* / fixture_True_*  (8 arms)
PASS lane_head_unchanged
C1_SELFTEST pass=44 fail=0
exit=0
```

```
$ TMPDIR=…/r49-Mo49ExecControlsReplay/s python3 .ufo/waves/round-49/count-c2.py --selftest
PASS honest_met … PASS normalise_keeps_visible_text
C2_SELFTEST pass=26 fail=0
exit=0
```

Tallies match the contract's recorded `C1_SELFTEST pass=44 fail=0` / `C2_SELFTEST pass=26 fail=0`.

`count-c2.py --selftest` output is **byte-identical** to `evidence/selftest-c2.txt` (`diff -u` → no output;
`sha256` of my capture `9d260eac79c3bedddf01d4d1df47da4d2269ca558be8abf7fc8d2d473e9a8c59` equals the freeze entry for
`selftest-c2.txt`).

`count-c1.py --selftest` differs from `evidence/selftest-c1.txt` in exactly one line (plus the committed receipt's
two-trailing-space padding, which is cosmetic):

```
-PASS filename_sniffer_not_met  … variants=24 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86
+PASS filename_sniffer_not_met  … variants=24 rev=0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115
```

That arm prints the lane `master` commit it read (`head = git -C LANE rev-parse master`), so the receipt was recorded
at the entering tip before the freeze commit moved `master`; the arm still passes. Not a predicate change.

## 2. Freeze integrity and control-tool hashes

```
$ sha256sum -c .ufo/waves/round-49/evidence/freeze-sha256.txt
… (all verified) …
$ … | grep -c ': OK$'
31
$ … | grep -v ': OK$'      # nothing
```

31/31 frozen paths verify against `evidence/freeze-sha256.txt`, including the four `corpus/evidence/sources-r49/`
copies, the four `assimilation/` files and all receipts.

The contract's entering-tool prefix is confirmed three ways:

```
$ git show b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86:tools/mori-pin-check.py | sha256sum
85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1  -
$ sha256sum tools/mori-pin-check.py
85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1  tools/mori-pin-check.py
$ sha256sum .ufo/waves/round-49/controls/tool-v3-entering.py
85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1  .ufo/waves/round-49/controls/tool-v3-entering.py
```

So `controls/tool-v3-entering.py` is byte-identical to `tools/mori-pin-check.py` at `b3e3453d` **and** to the current
worktree file — it is a genuine do-nothing control (the worktree tool has not been touched yet this round).

All control hashes equal their `freeze-sha256.txt` rows:

| control | sha256 |
|---|---|
| `stub-always-met.py` | `c6f12be844264304fd2007b1f30c4b9a15d4a5414c918588d800021221987b2d` |
| `stub-always-unmet.py` | `c963e47c5392584d8b658099330178655d9021d99de1ccf403f9411cdb44ec9d` |
| `stub-filename-sniffer.py` | `e31aa8361ec743ed1a5fecd72e9379392521c83dc6a5fb1507467fd9285abb9b` |
| `tool-r48-surface-fixes.py` | `dcecbe2c9636cffd449722164ac7c8100ec14a42ce562d59fd4ca958bdec598b` |
| `tool-r48-r11-only.py` | `8321a3104f3fc8187bcf2350bdfca26562a417ba42bfb90308563a04924cdcf6` |
| `tool-r48-merged-witness.py` | `c30ab6232893d984d1440784b6ce962d7c987c6d5538db0ead2f458a8ea1c9f0` |
| `tool-v3-entering.py` | `85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1` |

Structural spot-check of the three derived controls against the entering tool (`diff -u`, 917-line base):

* `tool-r48-surface-fixes.py` (949 lines, 42 changed content lines) adds the five surface rules (row-shape/HTML-row
  recognition, NFKC + zero-width normalisation, indented-row handling, `prev_raw` carry) and no instrument-attribution
  rule except a comment at the N5 site labelled "R11".
* `tool-r48-r11-only.py` (988 lines, 84 changed lines) adds only the R11 paragraph and `instrument_of()` (misattributed
  instrument is fatal).
* `tool-r48-merged-witness.py` (1020 lines, 126 changed lines) contains both blocks.

That matches the contract's description of each control (surface rules only / R11 only / mechanical merge). The one
naming wrinkle is that the surface-fixes comment at the duplicate-command rule calls itself "R11
(round-48 w2 CritV3Junk1)" while round 48's R11 is the D7 misattribution rule — cosmetic, in a control file, no
effect on scoring (see Findings L4).

## 3. Cheap controls replayed under the round-49 counter

Command shape (one scratch dir per control, all `--rev b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 --jobs 4`):

```
$ python3 .ufo/waves/round-49/count-c1.py --tool .ufo/waves/round-49/controls/<control>.py \
      --rev b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 --jobs 4 \
      --scratch …/r49-Mo49ExecControlsReplay/s-<control>
```

| control | replayed result line | rc | wall | committed receipt |
|---|---|---|---|---|
| `stub-always-met.py` | `C1=unmet junk_met=18 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d…` | 1 | 0.2s | `control-c1-stub-always-met.txt` |
| `stub-always-unmet.py` | `C1=unmet junk_met=0 honest_unmet=8 real=unmet errors=0 variants=26 rev=b3e3453d…` | 1 | 0.3s | `control-c1-stub-always-unmet.txt` |
| `stub-filename-sniffer.py` | `C1=unmet junk_met=18 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d…` | 1 | 0.3s | `control-c1-stub-filename-sniffer.txt` |

Per-variant comparison against the committed receipts (`difflib.unified_diff` over all 27
`variant name=… expect=… got=… rc=…` lines and the verdict line): **byte-identical for all three**, the only diff
being the committed files' trailing `exit=1` line, which my wrapper wrote to the shell rather than the file:

```
@@ -26,4 +26,3 @@
 variant name=real-opaque expect=met got=met rc=0
 C1=unmet junk_met=18 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86
-exit=1
```

None of the three reaches `met`, as the contract requires. `stub-always-unmet` is red on exactly H1-H4, H6, H7, H5 and
`real-opaque` (the opaque copy of the real registry) and on `real`, i.e. it rejects everything — the control is shown
able to fail on the honest side.

Note on evidence value: my replay of `stub-filename-sniffer` produced a file byte-identical to my
`stub-always-met` replay (`sha256 7bb5d0dfca2ff34a3f2e77820fbe84722c1bf0d43584f75d4ac4537b1b114812` for both), exactly as
the two committed receipts are byte-identical (`673966107b7ca1f0e415699e2bdf9f3836299fdcdea86c769b929b0c250331e3`
for both). Under opaque handles *every* variant scores `met`, so the two controls are indistinguishable from their
round-49 output alone; only the round-48 pair separates them (see §4). See Findings L3.

Scratch handle names actually handed to the tools contain no variant string:

```
$ ls …/s-v3 | grep -Ei 'J[0-9]|N[0-9]{1,2}|H[0-9]|variant|junk|honest'   → none
$ ls …/s-v3 | head -4
s-04ec89496f1e.md  s-37fdad947d20.md  s-3cce1d334281.md  s-3f9babd911bb.md
```

## 4. The sniffer pair (round 48 vs round 49)

```
$ python3 .ufo/waves/round-48/count-c1.py --tool .ufo/waves/round-49/controls/stub-filename-sniffer.py \
      --rev b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 --jobs 4 --scratch …/s-r48
variant name=J1 … got=unmet rc=1  …  variant name=H4 … got=met rc=0
variant name=real expect=met got=met rc=0
C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86
exit=0
```

Paired with §3's round-49 run (`C1=unmet junk_met=18 … variants=26`, exit 1), the pair **reproduces**: the same tool
bytes score `met` under the round-48 counter and `unmet` under the round-49 counter. Diff against
`evidence/control-c1-sniffer-under-r48-counter.txt`: identical apart from the trailing `exit=0` line. This is the
receipt that carries the round-48 leak closure; the round-48 counter's 12 variants and `variants=12` line match.

## 5. Timed do-nothing run (`tool-v3-entering.py`, jobs 3)

```
$ time env TMPDIR=…/s python3 .ufo/waves/round-49/count-c1.py \
      --tool .ufo/waves/round-49/controls/tool-v3-entering.py \
      --rev b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 --jobs 3 --scratch …/s-v3
C1=unmet junk_met=9 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86
exit=1
real 15m49.584s   user 151m5.386s   sys 89m40.215s      (wall 949.59s)
```

Compared with `evidence/control-c1-tool-v3-entering.txt`: **byte-identical for all 27 variant lines and the verdict
line**; only the trailing `exit=1` differs. The nine green junk variants are exactly N1-N9 (J1-J8, N10 unmet), as the
contract's freeze table states. So `junk_met=9` reproduces exactly.

Timing note: 949.6s wall at `--jobs 3` on a host carrying load 50.18 on 32 cores. The contract's "~10 minutes with
`--jobs 4`" is a load-dependent figure and was not contradicted by anything I measured (I did not run jobs 4 on this
tool). Recorded as observation only.

## 6. Extra replays (beyond the assigned steps)

Replayed the remaining C1 controls at `--jobs 3`, three concurrently (wall ≈ 2122-2127s each, host under heavy fleet
load, so wall time is not comparable):

| control | replayed result line | rc | committed receipt |
|---|---|---|---|
| `tool-r48-merged-witness.py` | `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d…` | **0** | `control-c1-tool-r48-merged-witness.txt` |
| `tool-r48-surface-fixes.py` | `C1=unmet junk_met=1 …` | 1 | `control-c1-tool-r48-surface-fixes.txt` |
| `tool-r48-r11-only.py` | `C1=unmet junk_met=7 …` | 1 | `control-c1-tool-r48-r11-only.txt` |

All three are byte-identical to their committed receipts apart from the trailing `exit=` line. The residue sets are
exactly as the contract claims: surface-fixes leaves **N9** green only; r11-only leaves **N1-N7** green only; the
merged witness reaches the target `met` line with exit 0. So the predicate is reachable with the recorded bytes, and
each half is separately required.

C2 do-nothing control:

```
$ python3 .ufo/waves/round-49/count-c2.py b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86
C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=bad provenance=bad \
rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 failed=entry_absent,pins
exit=1
```

Identical to `evidence/control-c2-donothing.txt` apart from the trailing `exit=1` line.

## 7. Falsifier probe on the opacity claim

The counter names each staged SKILL.md copy and scratch directory by `sha256(rev, body)[:12]`
(`count-c1.py` `opaque()` / `plan()`), submits runs sorted by that name and prints results in fixed `ORDER`. I tested
whether the *name→variant* map is recoverable by a tool that can read the lane: it is.

```
$ python3 (importlib load of .ufo/waves/round-49/count-c1.py; recompute opaque(rev, fn(text)) for every variant)
staged skill files in my own scratch: 24
map recovered for 24/24 staged names
sample: [('s-04ec89496f1e.md', ('J6','unmet')), ('s-37fdad947d20.md', ('N5','unmet')),
         ('s-3cce1d334281.md', ('H1','met')), ('s-3f9babd911bb.md', ('J2','unmet'))]
```

24/24 staged handles map to a variant name
*and* its expected verdict from the counter source alone; the fixture handles `w-…` and the `real` handle
`t-<opaque(rev,"real")>` are likewise derivable. The tool is handed `--repo <lane>` (and the rev), and the counter
lives at a fixed readable path inside that repo, so a determined tool can reconstruct the map at run time and answer
from it. This does not weaken any replay above — every control I replayed is a real tool/stub, not a map-reader —
but the contract's reading "the round-48 leak is closed" holds against *filename sniffing* only; a source-reading
sniffer is not in the predicate or in the named limits. See Findings M1.

## 8. Retained evidence

All artifacts under `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecControlsReplay/`:

| file | sha256 |
|---|---|
| `c1-selftest.txt` | `20a907b0c0b9cc58fc4ce30ed3b66f6d52f70dff0cc222e28a7dd40acd552adc` |
| `c2-selftest.txt` | `9d260eac79c3bedddf01d4d1df47da4d2269ca558be8abf7fc8d2d473e9a8c59` (== freeze entry) |
| `replay-stub-always-met.txt` | `7bb5d0dfca2ff34a3f2e77820fbe84722c1bf0d43584f75d4ac4537b1b114812` |
| `replay-stub-always-unmet.txt` | `929d89f60447f3bd76b3bfc3453c8c068450dc9e2c06d51f15b656d5a24431fa` |
| `replay-stub-filename-sniffer.txt` | `7bb5d0dfca2ff34a3f2e77820fbe84722c1bf0d43584f75d4ac4537b1b114812` |
| `replay-sniffer-under-r48-counter.txt` | `9283121cc2164f1e4a985332f843a8819ddd5c9ac174edf4e85d59e05b529729` |
| `replay-tool-v3-entering.txt` | `513c917d2df068420ed99926e9b0d724c4af3a89faf719396b0eb00ab5c938f8` |
| `replay-tool-r48-merged-witness.txt` | `b299ce1b0550697e0ddcc951acbe3bc62ea95669d95de8e47d528034c26238f1` |
| `replay-tool-r48-surface-fixes.txt` | `c16b3c2e6780b1411cf780164237921f6d316158b5153edbe111a3c187e49160` |
| `replay-tool-r48-r11-only.txt` | `ec379a456335d3daf2dffdb19018863256f57c018b8c0e28666cc42da1e2ad01` |
| `replay-c2-donothing.txt` | `724aae9069a3ff8ca2fe2b70b88d0975e05078e48e70008e69e5e31c83e5cbd8` |
| `time-v3.out` | `774d7d3dc6d5998e689adf9c7a70d58e4757369efb3cbe067eb04eb0a1048668` |
| `time-stub-always-unmet.txt`, `time-stub-filename-sniffer.txt`, `time-stub-always-met.txt` | wall/rc lines |

## 9. UNVERIFIED / blockers

* `UNVERIFIED`: whether the `__pycache__/*.pyc` in `.ufo/waves/round-49/` were written by my runs or by earlier
  seats — my script invocations do not write bytecode for `__main__`, my one `importlib` load matched an existing
  current `.pyc` (`count-c1.cpython-314.pyc` mtime 21:24, before my 21:40 selftest), and both are gitignored
  (`.gitignore:3 __pycache__/`); tracked state is unchanged.
* `UNVERIFIED`: the landed-tip `C1=met` (that is the L1's integration run, not this seat's; the witness reaching
  `met` shows it is reachable, not that the landed tool does it).
* No tooling was installed or upgraded, so there is nothing to record under the operator's tooling directive.

## Findings

Severity is about the frozen instrument and its receipts, not about the lane's implementation.

* **M1 — MED — `.ufo/waves/round-49/count-c1.py` (`opaque()`, `plan()`; contract §C1 "handles", §C1 "Named limits").**
  The opaque handles are content-hash names, and the counter's variant functions are readable at a fixed path inside
  the `--repo` the tool is handed. Recomputed from the counter source alone, 24/24 staged handles in my run mapped to
  `(variant, expected verdict)`; the fixture and `real` handles are derivable too. The round-48 filename-sniffer leak
  is closed, but a source-reading sniffer is neither in the predicate nor in the named limits. Suggested disposition
  (wave 2, as a limit rather than a re-score): add the class to the contract's named limits or add a control that
  reads `count-c1.py` and scores it, and/or stage variants from a directory outside `--repo`.
* **L1 — LOW — `count-c1.py` `verdict()`.** `junk_met` counts any non-`unmet` junk outcome, so a crashing/timing-out
  tool increments both `junk_met` and `errors` (e.g. `C1=unmet junk_met=1 … errors=1`). The verdict is still
  correctly `unmet` and the contract's "a crash is `errors`, never `unmet`" reads consistently, but the `junk_met`
  label means "junk not scored unmet", not "junk accepted". Receipt readers should not cite `junk_met=0` as evidence
  of no crashes; `errors=0` is that evidence.
* **L2 — LOW — `count-c1.py` `verdict()`.** `honest_unmet` sums `expect=="met"` rows excluding only `real`, so it
  includes the `real-opaque` read: the `stub-always-unmet` receipt's `honest_unmet=8` is 7 honest edits + 1 opaque
  copy, not 8 honest edits, and a tool red only on the opaque copy shows `honest_unmet=1`. Semantics are right
  (`met` requires 0), the label is what invites misreading.
* **L3 — LOW — `evidence/control-c1-stub-filename-sniffer.txt` vs `evidence/control-c1-stub-always-met.txt`.**
  The two receipts are byte-identical (both `673966107b7ca1f0e415699e2bdf9f3836299fdcdea86c769b929b0c250331e3` in
  `freeze-sha256.txt`), which my replay reproduced (both `7bb5d0df…`). Under opaque handles every variant scores
  `met`, so the sniffer's round-49 receipt carries no information by itself; the sniffer's evidence is the round-48
  pairing (`control-c1-sniffer-under-r48-counter.txt`, reproduced in §4). Any future receipt table should cite the
  pair, not the round-49 line alone.
* **L4 — LOW — `.ufo/waves/round-49/controls/tool-r48-surface-fixes.py`, comment at the duplicate-command rule.**
  The comment reads `# R11 (round-48 w2 CritV3Junk1): two rows binding one (prefix, argv) …` while round 48's R11 is
  the D7 instrument-misattribution rule (implemented only in `tool-r48-r11-only.py` / the witness). Control-only, no
  scoring effect; it makes the two half-controls harder to read.
* **L5 — LOW — `count-c1.py` `main()` (`tool = os.path.abspath(opts["--tool"])`).** The counter reads whatever file
  path it is given and never binds the tool bytes to `--rev`; the predicate's "the tool bytes at R" is an operator
  convention. In this replay that was true (`v3-entering` == `git show b3e3453d:tools/mori-pin-check.py`), and the
  L1's landed run should state the same one-line check (`sha256(git show R:tools/mori-pin-check.py)` ==
  `sha256(<tool>)`) in its receipt.
* **L6 — LOW — `evidence/selftest-c1.txt` (`filename_sniffer_not_met` arm).** The arm prints the lane `master`
  commit, so the frozen receipt carries `rev=b3e3453d…` while any run at or after the freeze commit prints
  `rev=0df17b7b…`. Both pass; the difference is the freeze commit itself, not a predicate change, but a future
  reader should not treat the rev string as a reproduction mismatch.
* **No HIGH finding.** Every assigned control replay (§3, §5) and the extra witness/partial replays (§6) reproduce
  their committed receipts byte for byte apart from my wrapper's missing `exit=` trailer; the freeze hashes verify
  31/31; both selftests tally exactly as frozen; the sniffer pair (round 48 `met` / round 49 `unmet`) reproduces.
