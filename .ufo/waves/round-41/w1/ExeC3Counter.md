# ExeC3Counter — calibration counter at the r40 anchor and the r41 revisions

Executor seat, read-only w.r.t. production files. All runs used a disposable clone
(`git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin /tmp/r41-exe-c3/sandbox`,
detached HEAD set to the measured revision per run) plus one read-only literal
invocation from the lane root. No production file, lane Git index, jj state or
`.ufo/state` was written; no tool was installed or updated.

Instrument under test: `tools/mori-round41-calibration.py`
blob `951e302d28c90141cdfe6037a587cac67b825c8a`,
sha256 `ddeaf5abe6fc7067737163a46e9538d67afac886e205956115a891cde504407a`
(identical at `aa161e99`, `c5326c61`, `7450722e`; absent from every r40 revision, so the
HEAD tool was run against older measured revisions).
Frozen gate reference for every measurement below: `--reference-rev 62a207f7521fa2e2fcd2e8b0260f047ccfce8862`.

## Exact runs, mismatch totals, exit codes

| Label | Measured revision | Live HEAD of checkout | `mismatches` | Exit |
|---|---|---|---|---|
| entering-r40 tip (r40 declaration's own anchor) | `bb1f2457bb8d3e8d5dfe98488b91e8c02e378ca3` | same | — (`MORI_R41_CALIBRATION_SETUP: cannot locate legacy r40 self-assessment in SCORECARD.md`) | **2** |
| r40 record commit (34/16 self-assessment) | `8d3badd0647c5dbfaf5f5a1443c5d4d5109a8d21` | same | **6** | **1** |
| r40 closure / entering-r41 tip = frozen reference | `62a207f7521fa2e2fcd2e8b0260f047ccfce8862` | same | **6** | **1** |
| r41 correction records (wrapped form) | `aa161e998eb22282e3d96ed2710bb0b39e5163de` | same | **6** | **1** |
| r41 single-line correction | `c5326c61bd60244cc29d84169fd1dc585fca8cd7` | same | **0** | **0** |
| r41 live HEAD (attempt-1 measured tip) | `7450722e5f3b4fc6df3d719386ed643af59630e3` | same | **0** | **0** |
| repeat of the live HEAD run | `7450722e…` | same | **0** | **0** |
| negative-control mutant (sandbox only) | `b664f299dc7a5476abba068dae7c0b9715a612d0` | same | **1** | **1** |
| alternate reference (r41 gate bytes, no frozen pin) | `7450722e…`, `--reference-rev 7450722e…` | same | **6** | **1** |

Command form for every row (paths elided only where identical):

```
/usr/bin/python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-round41-calibration.py <measured-rev> \
  --repo /tmp/r41-exe-c3/sandbox --reference-rev 62a207f7521fa2e2fcd2e8b0260f047ccfce8862
```

Literal contract-form invocation, run from the lane root against the lane repo (read-only):

```
python3 tools/mori-round41-calibration.py 7450722e5f3b4fc6df3d719386ed643af59630e3 \
  --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
  --reference-rev 62a207f7521fa2e2fcd2e8b0260f047ccfce8862
EXIT=0
SCORECARD.md recorded_as_of=35 observed_as_of=35 recorded_extension=17 observed_extension=17
LOG.md recorded_as_of=35 observed_as_of=35 recorded_extension=17 observed_extension=17
corpus/lessons/round-40.md recorded_as_of=35 observed_as_of=35 recorded_extension=17 observed_extension=17
MORI_R41_CALIBRATION mismatches=0 observed_as_of=35 extension_rows=17
```

The lane working tree was byte-unchanged by these runs (`git status --porcelain` before and
after shows only the pre-existing untracked `evidence/wave-run.json`,
`evidence/wave-run.stderr`, `w1/`).

## Frozen target

`mismatches=0` at `7450722e` and at `c5326c61`, exit 0, three records each reading 35/35/17.
The committed receipt `.ufo/waves/round-41/evidence/calibration-after.txt` is **byte-identical**
to my reproduced stdout (four lines, compared programmatically: `IDENTICAL`).

## Before-side decomposition (why exactly 6)

`observed_as_of=35`, `extension_rows=17` at the frozen reference (`35 as-of ids` minus the
`18` ids on the gate's `appendonly_violations` line). Per-record mismatch counts at
`62a207f` (identical at `8d3badd0`):

| Record | recorded | parser path | mismatches |
|---|---|---|---|
| `SCORECARD.md` | as_of 34, extension **MISSING** | `old_record` finds `measured value is **34 as-of ids**`; the extension phrase is line-wrapped (`16 never-edited\nsuperseded rows`), so `(\d+) never-edited superseded rows` cannot match | 2 |
| `LOG.md` | as_of 34, extension **MISSING** | `old_record` finds `lane line at T1 lists 34 as-of ids`; the r40 LOG entry carries no extension figure at all | 2 |
| `corpus/lessons/round-40.md` | as_of 34, extension 16 | M24 table row `(16 rows: S226 plus 15 earlier)` matches | 2 |
| total | | | **6**, exit 1 |

This reproduces `.ufo/waves/round-41/evidence/control-before.txt` `## C3 before calibration`
line-for-line (same three record lines, `mismatches=6`, `EXIT=1`).

## Negative controls (anti-vacuity)

1. **Drift detection.** Sandbox-only commit `b664f299` rewrote one SCORECARD correction to
   `observed_as_of=36; extension_rows=17.` → `SCORECARD.md recorded_as_of=36 … mismatches=1`,
   exit 1, other two records untouched. The counter is not a constant-zero printer.
2. **Reference sensitivity.** With `--reference-rev` pinned at the r41 tip (`7450722e`, gate
   blob `887fd85d96fd97f99f1845090cda64cf5e084fa8`) the same measured tip derives
   `observed_as_of=36 extension_rows=18` → `mismatches=6`, exit 1. The frozen `62a207f`
   reference is load-bearing; the 35/17 target exists only against the r40 gate bytes.
3. **Committed-bytes only.** With `SCORECARD.md` modified but uncommitted in the measured
   working tree (`observed_as_of=99` on disk), the counter still reports 35/35/17, exit 0:
   it reads `git show <rev>:<path>` and cannot be satisfied or broken by working-tree drift.
4. **Fail-closed boundaries.** Missing `--reference-rev` → argparse usage error, exit 2.
   Unresolvable revision (`deadbeef`) → `MORI_R41_CALIBRATION_SETUP: git show deadbeef:SCORECARD.md:
   fatal: invalid object name`, exit 2. Gate exit outside `{0,1}` → setup error path (exit 2),
   so a crashed reference gate can never masquerade as `mismatches=0`.
5. **Determinism.** Two consecutive runs at `7450722e` produce identical bytes.

## Findings for the parent / CritC3Reference

1. **"Entering r40" has two referents and only one is measurable.** The r40 SCORECARD
   declaration names the entering tip `bb1f2457`; at that revision the counter exits 2 because
   no `## Round 40 declaration` exists yet — correct fail-closed behavior, but not a numeric
   datum. The revision the round-41 fixture runner calls "the entering r40 commit"
   (`fixtures/run-r41-controls.py` line 5, `BASE = 62a207f…`) is in fact the r40 *closure*,
   and it is the revision whose before-side is 6 mismatches / exit 1. Both runs are recorded
   above so the L1 can cite either without ambiguity; the docstring wording is imprecise.
2. **The contract's parenthetical understates the before-side composition.** Contract C3 says
   "six mismatches (the LOG extension value is missing)". Measured: **SCORECARD's** extension
   is also unreadable (line-wrapped `16 never-edited\nsuperseded rows`), so `SCORECARD.md` and
   `LOG.md` both report `recorded_extension=MISSING`; only the lesson yields 16. The total 6
   and exit 1 are right; the attribution is not. Any future before-side re-measurement must
   expect `MISSING` twice, not once.
3. **The single-line record form is a hard requirement of the frozen regex.** At `aa161e99`
   the three correction paragraphs wrap `extension_rows=17.` onto the next line, so
   `CORRECTION_RE` matches nothing and the counter falls back to the legacy 34/16 read:
   6 mismatches, exit 1. `c5326c61` ("single-line calibration correction records (frozen
   counter regex)") is therefore the earliest revision that can reach the frozen target —
   the after-side is not attributable to the record content alone, but to content *and*
   single-line form.
4. **The after-side C3 receipt is a bare four-line stdout block.** The contract routes C3
   through `run-r41-controls.py after … --output evidence/control-after.txt`, but that runner's
   after mode deliberately skips `c3_section` ("C1/C2 after captured; C3 uses the separate
   calibration counter") and `control-after.txt` contains no C3 section; the C3 evidence is
   `evidence/calibration-after.txt`, which records neither the exact command line nor the exit
   code (the before side does, via `control-before.txt`'s `## C3 before calibration` command +
   `EXIT=1`). The numbers reproduce exactly, so this is a receipt-shape asymmetry, not a
   measurement gap.
5. **Unchanged limits of the instrument.** `extension_rows` is arithmetic
   (`len(as_of) − len(ids)` from the gate's `appendonly_violations` line), so it inherits any
   gate misclassification; and corrections are read by "last match wins", so a later wrapped
   or stale correction paragraph would silently re-route the record to the legacy regex.
   Neither is exercised by the frozen target.

## Files changed

- `.ufo/waves/round-41/w1/ExeC3Counter.md` (this report) — only file written.
- Scratch (disposable, outside the lane): `/tmp/r41-exe-c3/measure.sh`,
  `/tmp/r41-exe-c3/transcript.txt`, `/tmp/r41-exe-c3/sandbox/` (clone incl. the
  negative-control commit `b664f299`, never pushed anywhere).
- No production file edited, no tool installed, no pacman transaction.
