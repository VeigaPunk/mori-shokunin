# Mo50bExecReexecR49 — round 49's frozen counters and tool selftests, executed

Seat: `Mo50bExecReexecR49` (executor, leaf). Assignment: `considerthese/2026-10-26.md` suggestion 3 —
"re-execute what closures only evidence-verified" — against round 49
(`corpus/lessons/round-49-verifier-spotcheck.md`, `LOG.md` Round 49, `.ufo/waves/round-49/`).

**Result: 14 of 14 committed round-49 receipts reproduce byte for byte, with matching exit codes, from a
`git clone --shared` of the lane checked out at the round-49 tip `43d84666`. Two of the receipts
(`selftest-c1.txt`, `selftest-c2.txt`) and both tool selftests (`PIN_CHECK_SELFTEST pass=114 fail=0`,
`UNLANDED_SELFTEST pass=17 fail=0`) also reproduce; the tool tallies close the round-49 closure's routed
defect 2 (D-d: "the tool selftest tally has no committed output file") with actual output bytes. One pin
inside the C1 predicate is *not* hermetic: it reads the host lane by absolute path (§4). Nothing DIVERGE;
nothing CANNOT-RUN.**

## 0. Setup, provenance, hygiene

| item | observation |
|---|---|
| disk guard | `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → `use% 24  free 612.1G` for `/fast/scratch/hyaku`, rc 0 |
| scratch | `/fast/scratch/hyaku/mori-r50/Mo50bExecReexecR49/` (`mkdir -p`); `TMPDIR=$S/tmp` exported in every shell; `-B` on every python run; removed at the end (§9) |
| clone (one, `--shared`) | `git clone --shared -q /home/vgpnk/Projects/shokunin/mori-shokunin $S/lane` → 0.58 s, 330 MB on disk |
| working tree | `git -C $S/lane checkout -q 43d84666` → `43d846669efe5a2fcc2325006f165af4e7e7fda4` |
| revisions resolved in the clone | `b3e3453d` `0df17b7b` `64c2d5fc` `24ebc799` `43d84666` all resolve; `4387cf94` and `e4dfff32` resolve too (§6) |
| freeze integrity | `sha256sum -c --quiet .ufo/waves/round-49/evidence/freeze-sha256.txt` → no output, rc 0 (31/31 lines OK) |
| frozen bytes used | `count-c1.py` `3c262a15ae28adff…`, `count-c2.py` `be39475d997f5cf4…`, `tools/mori-pin-check.py` `697ab2cc6ca6702a…`, `tools/mori-unlanded-check.py` `612d50c1590d5a30…`; `git diff --stat 0df17b7b 43d84666 -- count-c1.py count-c2.py controls contract.md` → empty |
| tool bytes at measured rev | `git show 64c2d5fc:tools/mori-pin-check.py \| sha256sum` = `697ab2cc…` = `sha256sum tools/mori-pin-check.py` at `43d84666` (the closure's claim re-measured) |
| interpreter / git | Python 3.14.8, git 2.56.0 |
| tools installed | none. No pacman transaction was attempted (host-wide pause respected); nothing was missing for this seat |
| host writes by this seat | none persisted: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --porcelain` → 0 paths of mine (the 11 listed paths are round-50's in-flight work). See §4 for one transient host scratch dir created and removed by a pinned command |

**Command reconstruction.** No round-49 receipt file carries its own command line; each holds only
`variant …`/verdict lines plus `exit=N`. The commands below are reconstructed from (a) contract §P-C1/P-C2,
(b) each counter's `Usage:` block, (c) the `rev=` field inside each receipt, (d) the contract's
"Scored with `count-c1.py` at the entering tip `b3e3453d` (jobs 4)". The counter's own defaults supply the
predicate's flags (`MIN_TALLY=26`, `BASELINE=2d85e33d14198d388fd3cda9cc15ec07e57e7a53`,
`TOOL_TIMEOUT=900`), so no extra flags were passed.

## 1. Re-execution table (the receipt the L1 can commit)

All runs: `cwd=$S/lane`, `TMPDIR=$S/tmp`, `python3 -B`, a `timeout 900` wrapper on every run, `--scratch`
under `$S` (never the repo). Paths below are relative to the clone root.

| # | command | rev | printed final line | rc | committed receipt | verdict |
|---|---|---|---|---|---|---|
| 1 | `.ufo/waves/round-49/count-c1.py --tool tools/mori-pin-check.py --rev 64c2d5fc… --repo $S/lane --scratch $S/c1-tip --jobs 4` | `64c2d5fc` | `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26 rev=64c2d5fcd95a11f195de0387fa791cab7a54ecb1` | 0 | `after-c1-at-tip.txt` (`exit=0`) | **AGREE** (28/28 lines identical) |
| 2 | `… count-c1.py --tool .ufo/waves/round-49/controls/tool-v3-entering.py --rev b3e3453d… --scratch $S/c1-tool-v3-entering --jobs 4` | `b3e3453d` | `C1=unmet junk_met=9 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86` | 1 | `control-c1-tool-v3-entering.txt` (`exit=1`) | **AGREE** (28/28) |
| 3 | `… --tool …/controls/stub-always-met.py …` | `b3e3453d` | `C1=unmet junk_met=18 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d…` | 1 | `control-c1-stub-always-met.txt` (`exit=1`) | **AGREE** (28/28) |
| 4 | `… --tool …/controls/stub-always-unmet.py …` | `b3e3453d` | `C1=unmet junk_met=0 honest_unmet=8 real=unmet errors=0 variants=26 rev=b3e3453d…` | 1 | `control-c1-stub-always-unmet.txt` (`exit=1`) | **AGREE** (28/28) |
| 5 | `… --tool …/controls/stub-filename-sniffer.py …` | `b3e3453d` | `C1=unmet junk_met=18 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d…` | 1 | `control-c1-stub-filename-sniffer.txt` (`exit=1`) | **AGREE** (28/28) |
| 6 | `… --tool …/controls/tool-r48-surface-fixes.py …` | `b3e3453d` | `C1=unmet junk_met=1 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d…` | 1 | `control-c1-tool-r48-surface-fixes.txt` (`exit=1`) | **AGREE** (28/28) |
| 7 | `… --tool …/controls/tool-r48-r11-only.py …` | `b3e3453d` | `C1=unmet junk_met=7 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d…` | 1 | `control-c1-tool-r48-r11-only.txt` (`exit=1`) | **AGREE** (28/28) |
| 8 | `… --tool …/controls/tool-r48-merged-witness.py …` | `b3e3453d` | `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d…` | 0 | `control-c1-tool-r48-merged-witness.txt` (`exit=0`) | **AGREE** (28/28) |
| 9 | `.ufo/waves/round-48/count-c1.py --tool .ufo/waves/round-49/controls/stub-filename-sniffer.py --rev b3e3453d… --scratch $S/c1-sniffer-r48 --jobs 4` | `b3e3453d` | `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=b3e3453d…` | 0 | `control-c1-sniffer-under-r48-counter.txt` (`exit=0`) | **AGREE** (14/14) |
| 10 | `.ufo/waves/round-49/count-c1.py --selftest` | clone `master`=`b3e3453d` | `C1_SELFTEST pass=44 fail=0` | 0 | `selftest-c1.txt` | **AGREE** (45/45, byte-identical) |
| 11 | `.ufo/waves/round-49/count-c2.py --selftest` | — | `C2_SELFTEST pass=26 fail=0` | 0 | `selftest-c2.txt` | **AGREE** (27/27, byte-identical) |
| 12 | `.ufo/waves/round-49/count-c2.py 24ebc799… --repo $S/lane` | `24ebc799` | `C2=met claims=21 located=21 quote_missing=0 bad_rows=0 sources=4 source_rows=ok pins=ok provenance=ok rev=24ebc7991e9081348d1aa4f558f994b1f4feccab` | 0 | `after-c2-at-24ebc799.txt` (`exit=0`) | **AGREE** |
| 13 | `.ufo/waves/round-49/count-c2.py 64c2d5fc… --repo $S/lane` | `64c2d5fc` | `C2=met claims=21 located=21 quote_missing=0 bad_rows=0 sources=4 source_rows=ok pins=ok provenance=ok rev=64c2d5fcd95a11f195de0387fa791cab7a54ecb1` | 0 | `after-c2-at-tip.txt` (`exit=0`) | **AGREE** |
| 14 | `.ufo/waves/round-49/count-c2.py b3e3453d… --repo $S/lane` | `b3e3453d` | `C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=bad provenance=bad rev=b3e3453d… failed=entry_absent,pins` | 1 | `control-c2-donothing.txt` (`exit=1`) | **AGREE** |

Supporting runs (not committed receipts of round 49, run for context):

| # | command | printed final line | rc |
|---|---|---|---|
| 15 | `python3 -B tools/mori-pin-check.py --rev 43d84666 --repo $S/lane` (no `--min-tally-pins`/`--baseline-rev`, unlike the predicate's inner runs: `min_tally_pins=1 … baseline=no`) | `PIN_CHECK=met tally_pins=33 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=43d846669efe5a2fcc2325006f165af4e7e7fda4 baseline=no` | 0 |
| 16 | `python3 -B tools/mori-pin-check.py --selftest` | `PIN_CHECK_SELFTEST pass=114 fail=0` (114 PASS, 0 FAIL) | 0 |
| 17 | `python3 -B tools/mori-unlanded-check.py --selftest` | `UNLANDED_SELFTEST pass=17 fail=0` (17 PASS, 0 FAIL) | 0 |
| 18 | `python3 -B .ufo/waves/round-40/conform.py 43d84666 --selftest` (the command registry line 911 pins) | `CONFORM_SELFTEST pass=11 fail=0` | 0 |
| 19 | `python3 -B .ufo/waves/round-49/flagged-fixed/count-flagged.py --repo $S/lane` | `flagged=45 fixed=18 unfixed=9` / `na=18` | 0 |
| 20 | `… count-flagged.py --repo $S/lane --landing 4387cf94…` (control: freeze as landing) | `flagged=45 fixed=0 unfixed=27` / `na=18` | 0 |

Run 15's own pin lines corroborate rows 10, 11 and 18 from the tool's side:
`pin line=911 … prefix=CONFORM_SELFTEST state=match pinned='pass=11 fail=0' observed='pass=11 fail=0' rc=0 cmd='python3 .ufo/waves/round-40/conform.py 43d84666… --selftest'`,
`pin line=938 … prefix=PIN_CHECK_SELFTEST state=match pinned='pass=114 fail=0' observed='pass=114 fail=0'`,
`pin line=973 … prefix=UNLANDED_SELFTEST state=match pinned='pass=17 fail=0' observed='pass=17 fail=0'`;
`grep -o 'kind=[a-z_]*'` → 33 `kind=tally` + 8 `kind=digest` + 2 `kind=lines`, and
`grep -o 'state=[a-z]*'` → 43 × `state=match`, 0 of anything else.

## 2. Hash equality at freeze level

My output, re-shaped as the receipt (`output` + `exit=N`), hashed against the committed receipt:

| committed receipt | sha256 of my re-shaped output | freeze pin (`evidence/freeze-sha256.txt`) | equality |
|---|---|---|---|
| `after-c1-at-tip.txt` | `ff199f676cb5581a…` | (not pinned) | **HASH-EQ** |
| `control-c1-tool-v3-entering.txt` | `5a608ea1fd06b373…` | `5a608ea1fd06b373…` | **HASH-EQ** |
| `control-c1-stub-always-met.txt` | `673966107b7ca1f0…` | `673966107b7ca1f0…` | **HASH-EQ** |
| `control-c1-stub-always-unmet.txt` | `b910925282d45327…` | `b910925282d45327…` | **HASH-EQ** |
| `control-c1-stub-filename-sniffer.txt` | `673966107b7ca1f0…` | `673966107b7ca1f0…` | **HASH-EQ** |
| `control-c1-tool-r48-surface-fixes.txt` | `b5c3186a3a3aac8c…` | `b5c3186a3a3aac8c…` | **HASH-EQ** |
| `control-c1-tool-r48-r11-only.txt` | `135ddc1a5302e329…` | `135ddc1a5302e329…` | **HASH-EQ** |
| `control-c1-tool-r48-merged-witness.txt` | `2568221d44006dcf…` | `2568221d44006dcf…` | **HASH-EQ** |
| `control-c1-sniffer-under-r48-counter.txt` | `03f6063ec00825d4…` | `03f6063ec00825d4…` | **HASH-EQ** |
| `selftest-c1.txt` | `8bbb1dd3e5b42a77…` | `8bbb1dd3e5b42a77…` | **HASH-EQ** |
| `selftest-c2.txt` | `9d260eac79c3bedd…` | `9d260eac79c3bedd…` | **HASH-EQ** |
| `after-c2-at-24ebc799.txt` | `11ba5671afcb427b…` | (not pinned) | **HASH-EQ** |
| `after-c2-at-tip.txt` | `5692b524dd331660…` | (not pinned) | **HASH-EQ** |
| `control-c2-donothing.txt` | `68b974e3269a414f…` | `68b974e3269a414f…` | **HASH-EQ** |

Four committed receipts (`after-c1-at-tip`, `after-c2-at-24ebc799`, `after-c2-at-tip`, plus
`control-c1-*` pairs already pinned) are not themselves in the freeze manifest except as noted; the three
unpinned ones are the *after* files scored at the landing revs, so their pins would have to move with the
landing — that is the expected asymmetry, not a gap.

## 3. Tools round 49 registered — selftests now executed (closes closure D-d)

Closure D-d: "`PIN_CHECK_SELFTEST pass=114 fail=0` and the unlanded check's 17/17 appear only as prose …
The tally is therefore unverified by me." Both are now executed at the scored rev.

- `python3 -B tools/mori-pin-check.py --selftest` — 6.2 s wall, rc 0, `PIN_CHECK_SELFTEST pass=114 fail=0`,
  114 `PASS` lines, 0 `FAIL`; output sha256 `11ee6e5e7d9e1b646cb5c3738e3250514ffc23f58e096f0b97f2202efdad2a38`
  (115 lines). Full output: Appendix A.
- `python3 -B tools/mori-unlanded-check.py --selftest` — 0.2 s wall, rc 0,
  `UNLANDED_SELFTEST pass=17 fail=0`, 17 `PASS`, 0 `FAIL`; output sha256
  `22604de3387ebb25eb92e151c41a44a2b2ab9ab77289fa4d1f71e5c61445fe1b` (18 lines). Full output: Appendix B.

The L1 can commit both blocks verbatim as `.ufo/waves/round-50/evidence/selftest-pin-check.txt` and
`…-unlanded.txt`; the hashes above are the check.

Round 49 also landed a capability with no selftest, `flagged-fixed/count-flagged.py` (its docstring states
the verdict rule instead; `grep -c selftest` → 0). Its documented numbers reproduce (row 19–20): the round-48
landing count `flagged=45 fixed=18 unfixed=9` + `na=18`, and the freeze-as-landing control
`fixed=0 unfixed=27` + `na=18` — matching `corpus/lessons/round-49.md:159` and `SCORECARD.md:2642`
word for word.

## 4. Measured non-hermeticity: one pin reads the host by absolute path

The `counter conformance v3 (r40)` row (`SKILL.md:911`) pins
`CONFORM_SELFTEST pass=11 fail=0` from `.ufo/waves/round-40/conform.py`, which hardcodes
`LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"` and derives `SCRATCH_ROOT`, `DEFAULT_COUNTERS`,
`DEFAULT_CONTRACT`, `FIXTURE_REL`, `HANG_FIXTURE` from it (`conform.py:69-77`). So the pin's `AGREE` in row 1
is partly host-derived. Measured, from the clone, under
`strace -f -e trace=openat -o $S/strace-conform2.log python3 -B .ufo/waves/round-40/conform.py 43d84666 --selftest`:

```
CONFORM_SELFTEST pass=11 fail=0        (rc 0, 2m30s)

distinct host paths opened (rename only, counts):
  45  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/scratch/<scratch>/
  33  /home/vgpnk/Projects/shokunin/mori-shokunin/.git/HEAD
  22  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-39/fixtures/hang-after-flush.py
  11  …/round-40/scratch/<scratch>/counter-<mutation>.py   (one line per arm class)
   1  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/count-c8.py
   1  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-39/contract.md
```

Effect on the verdict: none for this round, because the pinned rev was passed explicitly (`43d84666`) and
the host holds those same bytes (the freeze check in §0 passed against the clone, and the clone is a
`--shared` clone of the same object store). Effect on the *instrument*: this pin cannot be re-executed
off-host at all (the r49 daily note already saw it exit 2 with
`conformance setup error: No such file … /round-40/count-c8.py`), and on-host it silently re-measures the
host tree even when the caller is a clone. QUALITY 127's scope (13 files) is unchanged by this seat.

Side effect to disclose: that command creates and removes
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/scratch/mori-conform-selftest-<rand>/` on
the host. I checked before and after: `ls -d .ufo/waves/round-40/scratch/*` → 3 entries
(`mutconform-arms2`, `selftest-v3-draft.txt`, `selftest-v3-draft2.txt`) both times, i.e. no residue survived;
none of the three is mine. Note also that the closure's D-e figure ("seven `round-40/scratch/mori-conform-selftest-*`
dirs") no longer matches disk — no such directory exists now.

Related, observed while probing: `python3 .ufo/waves/round-40/conform.py --selftest` **without** a rev exits
2 with `conformance setup error: expected str, bytes or os.PathLike object, not NoneType` — a raw `TypeError`
reported as a setup error rather than a usage error (`conform.py:791-799`). Pre-existing r40 code, outside
round 49's claim; noted, not fixed.

## 5. `count-c1.py --selftest` is not self-contained: it reads the repo's mutable `master`

The receipt row 10 reproduced only after I moved the *clone's* `master` ref to `b3e3453d` (the rev its own
detail line prints). Measured both ways:

| clone `master` | result | difference |
|---|---|---|
| `b3e3453d` | `C1_SELFTEST pass=44 fail=0`, byte-identical to `selftest-c1.txt` | — |
| `4548a34d` (current lane tip) | `C1_SELFTEST pass=44 fail=0` | one line: `PASS filename_sniffer_not_met  … rev=4548a34d…` instead of `rev=b3e3453d…` |

The selftest takes its input text from `git -C LANE rev-parse master` (`count-c1.py:339-341`), not from a
pinned rev, so a committed `--selftest` receipt is reproducible only in a tree whose `master` is at the
freeze-era rev. The tally itself was master-insensitive between these two revs; whether an arm's anchor can
disappear at a later `master` is untested here (not claimed).

## 6. What this re-execution does not prove

- **Location, not entailment.** C2's 21/21 located quotes are substring matches in the committed copies (the
  counter's own named limit). I did not re-fetch the three freedesktop pages; the r49 closure did that.
- **Variant classes are round-47/48 classes.** `junk_met=0` covers J1-J8, N1-N10 only; the contract's K2-K8
  residual classes stay open, unchanged.
- **One pin is host-derived** (§4), so `real=met` in row 1 is not a clone-isolated measurement.
- **Only the frozen instruments were run.** I did not re-run any wave-1 seat's own probe, and I did not run
  the round-49 counters at the current lane tip (round-50 data has landed since; that would score a different rev).
- **`variants=26` against 27 `variant` lines** reproduces exactly (closure D-f). The reason is in the code:
  `verdict()` prints `len(results) - 1` and `results` carries 27 entries (12 r48 + 11 new + 2 fixture + `real`
  + `real-opaque`). So the receipt's arithmetic is internally consistent and the gap is documentation only.
- **Two committed controls share one receipt hash** (`control-c1-stub-always-met.txt` and
  `control-c1-stub-filename-sniffer.txt`, both `673966107b…`, both `junk_met=18`); the sniffer's distinct
  behaviour rests on `control-c1-sniffer-under-r48-counter.txt`, which does differ. No claim is harmed.

## 7. Cost of the re-execution (for the next round's budget)

| run | wall |
|---|---|
| one `count-c1.py` predicate/partial-tool run (26 tool invocations, `--jobs 4`, loaded host) | 9m31s – 10m08s |
| stub controls (3) | < 5 s total (the stub returns instantly) |
| `round-48/count-c1.py` sniffer receipt | < 5 s |
| `count-c1.py --selftest` / `count-c2.py --selftest` | 0.19 s / 0.10 s |
| `mori-pin-check.py --selftest` / `--rev` (33 pins) | 6.2 s / 1m41s |
| `mori-unlanded-check.py --selftest` | 0.20 s |
| pinned `conform.py … --selftest` | 2m30s (dominates every C1 run) |
| whole seat (9 C1 runs + 3 C2 + 4 selftests + 2 flagged) | ~55 min of compute |

## 8. Report-shape notes for the L1

- There is no `after-c1-at-64c2d5fc.txt`; the closure's "at tip" receipt is named `after-c1-at-tip.txt` and
  its `rev=` is `64c2d5fc`, not `43d84666`. Byte identity of the tool at both revs is what licenses the name
  (§0), and my run reproduced it with `--rev 64c2d5fc` and the tool bytes of `43d84666`.
- Round-49 receipts carry no command line; a committed re-execution receipt should carry one (this table does).

## 9. Cleanup

`rm -rf -- /fast/scratch/hyaku/mori-r50/Mo50bExecReexecR49` after the report was written; verified absent
(`test -e` → false). Nothing was written to the lane, the fleet repo, `shokuknow`, `/tmp`, or any sibling
lane; the host working tree shows only other seats' round-50 paths.

## Appendix A — `tools/mori-pin-check.py --selftest`, verbatim

`cd $S/lane && TMPDIR=$S/tmp python3 -B tools/mori-pin-check.py --selftest` (at `43d84666`), rc 0,
115 lines, sha256 `11ee6e5e7d9e1b646cb5c3738e3250514ffc23f58e096f0b97f2202efdad2a38`:

```
PASS honest  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS stale_tally  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS stale_in_cell_true_elsewhere  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=1 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS pin_moved_out_of_cell  PIN_CHECK=unmet tally_pins=0 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=1 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS digest_ok  PIN_CHECK=met tally_pins=1 digest_pins=1 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS digest_stale  PIN_CHECK=unmet tally_pins=1 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS malformed_row  PIN_CHECK=unmet tally_pins=0 digest_pins=0 mismatches=0 unparsed=1 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=0 rev=deadbeef baseline=no
PASS no_command  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=1 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS digitless_pin  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=1 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS timeout  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS bare_flag_rev_entry  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS escaped_pipe_cell  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS below_floor  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=2 rev=deadbeef baseline=no
PASS mutant_pin_bound_to_mutant  PIN_CHECK=met tally_pins=2 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=2 rev=deadbeef baseline=no
PASS mutant_pin_wrong  PIN_CHECK=unmet tally_pins=2 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=2 rev=deadbeef baseline=no
PASS tmpdir_inside_measured_tree  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS token_boundary_truncated_pin  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS baseline_row_deleted  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=1 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=yes
PASS baseline_all_present  PIN_CHECK=met tally_pins=2 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=yes
PASS v2_inline_code_rejected  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=1 no_command=1 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS v2_scratch_path_rejected  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=1 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS v2_weakened_pin_exact  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS v2_rebound_to_other_tool  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=1 duplicate=0 hidden=0 misattributed=1 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=yes
PASS v2_entry_rebound  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=1 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=yes
PASS x1_baseline_binding_disappears  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=1 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=yes
PASS x1_baseline_binding_inline_code  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=1 no_command=1 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=yes
PASS k5_namespace_new_instrument_rejected  PIN_CHECK=unmet tally_pins=3 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=1 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=3 rev=deadbeef baseline=yes
PASS k5_namespace_family_join_admitted  PIN_CHECK=met tally_pins=3 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=3 rev=deadbeef baseline=yes
PASS v2_hidden_row_and_duplicate  PIN_CHECK=unmet tally_pins=2 digest_pins=0 mismatches=0 unparsed=1 no_command=0 dropped=0 rebound=0 duplicate=1 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=yes
PASS v2_duplicate_name  PIN_CHECK=unmet tally_pins=2 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=1 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS v2_digest_path_traversal  PIN_CHECK=unmet tally_pins=1 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS v2_stale_echo_line_ignored  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS v2_disagreeing_tally_lines  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS v2_fenced_example_not_counted  PIN_CHECK=unmet tally_pins=0 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=1 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS v2_entry_column_from_header  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r1_header_selftest_spelling  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r1_header_self_test_spelling  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r2_hidden_row_outside_table  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=1 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r2_hidden_fenced  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=1 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r2_hidden_selftest_arg  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=1 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r3_fullwidth_prefix  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=1 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r3_lowercase_prefix  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=1 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r3_mixedcase_prefix  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=1 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r4_rebound_new_row_same_prefix  PIN_CHECK=unmet tally_pins=2 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=1 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=yes
PASS r5_line_count_match  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r5_line_count_mismatch  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r5_line_count_no_path  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=1 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r5_line_count_overpin_mismatch  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r6_trunc_digest_match  PIN_CHECK=met tally_pins=1 digest_pins=1 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r6_trunc_digest_mismatch  PIN_CHECK=unmet tally_pins=1 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r7_token_not_at_span_start  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=1 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r7_symlink_digest_not_inside  PIN_CHECK=unmet tally_pins=1 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r7_argv_shape_rejected  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=1 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r7_argv_dotdot_rejected  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=1 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r7_argv_trailing_args_rejected  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=1 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r7_escaped_double_backslash_pipe  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r10_digest_decoy_file_in_other_cell  PIN_CHECK=unmet tally_pins=1 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r10_trunc_digest_decoy_file_in_other_cell  PIN_CHECK=unmet tally_pins=1 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r10_digest_binds_to_nearest_preceding_path  PIN_CHECK=met tally_pins=1 digest_pins=1 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r10_digest_binds_to_nearest_preceding_path_not_following  PIN_CHECK=unmet tally_pins=1 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r9a_tally_in_pinned_values_cell  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=1 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r9b_continuation_line_tally  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=1 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r9c_tally_outside_backticks  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=1 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r11_misattributed_instrument  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=1 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r11_mutant_other_basename_rejected  PIN_CHECK=unmet tally_pins=2 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=1 env_unexpanded=0 min_tally_pins=2 rev=deadbeef baseline=no
PASS r11_second_entry_path_not_claimed  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=1 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r11_entry_cell_without_instrument  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=1 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r11_mutant_right_basename_wrong_directory  PIN_CHECK=unmet tally_pins=2 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=1 env_unexpanded=0 min_tally_pins=2 rev=deadbeef baseline=no
PASS r12_line_count_pin_deleted  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=1 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=yes
PASS r12_trunc_digest_pin_deleted  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=1 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=yes
PASS r12_trunc_digest_repaired_to_full  PIN_CHECK=met tally_pins=1 digest_pins=1 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=yes
PASS r14_line_count_decoy_path  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS k2_env_prefix_as_written  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS k2_env_applied_honest_pin  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS k2_env_pwd_expanded  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS k2_env_unexpanded  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=1 min_tally_pins=1 rev=deadbeef baseline=no
PASS k2_entry_cell_env  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS k8_pass_form_rc0  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS k8_failure_count_exception  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS f1_blankline_continuation_tally  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=1 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS f1_honest_prose_after_blank  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS f1_adjacency_is_nearest_nonblank  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS f2_laundered_header_row_measured  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS f2_laundered_header_zwsp_token  PIN_CHECK=unmet tally_pins=0 digest_pins=0 mismatches=0 unparsed=1 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS f2_laundered_header_honest_row  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS f2_zwsp_in_header_cell  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS f3_tab_indented_fenced_row  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=1 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS f3_four_space_row  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=1 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS f3_indented_examples_without_token  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS f4_html_row_with_pin  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=1 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS f4_html_without_pin  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS f5_conflicting_exit_contracts  PIN_CHECK=unmet tally_pins=2 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=1 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=2 rev=deadbeef baseline=no
PASS f5_agreeing_exit_contracts  PIN_CHECK=met tally_pins=2 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=2 rev=deadbeef baseline=no
PASS f5_unstated_contract_skipped  PIN_CHECK=met tally_pins=2 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=2 rev=deadbeef baseline=no
PASS f5_nbsp_verdict_map_header_still_read  PIN_CHECK=unmet tally_pins=2 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=1 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=2 rev=deadbeef baseline=no
PASS r11_same_instrument_green  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r1_header_case_insensitive  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r2_hidden_selftest_arg_no_token  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=1 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r3_nonascii_decorative_span  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=1 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r9a_tally_in_pinned_cell_pass_only  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=1 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r9b_continuation_line_selftest_flag  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=1 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r9c_tally_PASS_form_outside_backticks  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=1 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r7_argv_tools_scratch_rejected  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=1 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r7_symlink_digest_precedes_path_containment  PIN_CHECK=unmet tally_pins=1 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r7_symlink_digest_prefix_sibling  PIN_CHECK=unmet tally_pins=1 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r5_line_count_overpin_mismatch  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r10_digest_following_path_not_bound  PIN_CHECK=unmet tally_pins=1 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS nonzero_rc_with_fail0  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS k8_pass_form_rc1  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r13_self_row_deleted  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=1 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r13_self_row_pinned  PIN_CHECK=met tally_pins=2 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r13_self_instrument_absent_no_obligation  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS cli_met_rc0  rc=0
PASS cli_bad_rev_rc2  rc=2
PIN_CHECK_SELFTEST pass=114 fail=0
```

## Appendix B — `tools/mori-unlanded-check.py --selftest`, verbatim

`cd $S/lane && TMPDIR=$S/tmp python3 -B tools/mori-unlanded-check.py --selftest` (at `43d84666`), rc 0,
18 lines, sha256 `22604de3387ebb25eb92e151c41a44a2b2ab9ab77289fa4d1f71e5c61445fe1b`:

```
PASS clean_tree_exit0  rc=0 UNLANDED=clean round=8
PASS untracked_late_result_exit1_names_it  rc=1 ['UNLANDED=dirty round=8 paths=1', 'unlanded ?? .ufo/waves/round-8/w2/Late.md']
PASS modified_tracked_report_exit1  rc=1 ['UNLANDED=dirty round=8 paths=1', 'unlanded .M .ufo/waves/round-8/w1/A.md']
PASS outside_scope_and_scratch_not_listed  rc=0 ['UNLANDED=clean round=8']
PASS other_round_not_listed  rc=0 ['UNLANDED=clean round=8']
PASS other_round_listed_for_that_round  rc=1
PASS lessons_and_space_in_path_listed  rc=1 ['UNLANDED=dirty round=8 paths=2', 'unlanded ?? corpus/lessons/round-8.md', 'unlanded ?? tools/new tool.py']
PASS staged_but_uncommitted_listed  rc=1
PASS rename_source_not_listed  rc=0 ['UNLANDED=clean round=8']
PASS in_scope_rename_lists_destination_only  rc=1 ['UNLANDED=dirty round=8 paths=1', 'unlanded R. corpus/moved.md']
PASS list_cap_50_of_60  rc=1 lines=51 last=unlanded ?? .ufo/waves/round-8/w2/F49.md
PASS modified_status_rendered_with_dot  rc=1 ['UNLANDED=dirty round=8 paths=1', 'unlanded .M corpus/lessons/round-8.md']
PASS subdirectory_is_setup_error  --repo is not a repository top level (git top level is /fast/scratch/hyaku/mori-
PASS missing_directory_is_setup_error  setup
PASS cli_dirty_rc1  rc=1
PASS cli_setup_rc2  rc=2
PASS cli_usage_rc2  rc=2
UNLANDED_SELFTEST pass=17 fail=0
```

## Findings

Positive results (no defect; stated with their evidence above): all 14 committed round-49 receipts reproduce
byte for byte with matching exit codes (§1, §2), and both round-49 tool selftests now have executed output
(§3, Appendices A/B), which closes closure routed defect 2. The findings below are defects, limits and risks.

| # | severity | finding | file / line |
|---|---|---|---|
| 1 | MED | The C1 predicate's `real` reading is not hermetic: the pinned `counter conformance v3 (r40)` row executes `conform.py`, which reads the **host** lane by absolute path. Measured under strace: 33 host `.git/HEAD` opens, host `round-40/count-c8.py`, host `round-39/contract.md`, host `round-39/fixtures/hang-after-flush.py`, all work done in host `round-40/scratch/`. Verdict unaffected here (explicit `--rev`, identical bytes) but the re-execution is not clone-isolated for that pin, and the same shape is what made the pin fail off-host. | `.ufo/waves/round-40/conform.py:69-77`; pinned at `SKILL.md:911` |
| 2 | MED | `count-c1.py --selftest` reads the repo's mutable `master` ref instead of a pinned revision, so its committed receipt is reproducible only when `master` sits at the freeze-era rev. Measured: identical tally at `4548a34d`, but one output line differs (`rev=`). A committed `--selftest` receipt therefore does not pin what it measured. | `.ufo/waves/round-49/count-c1.py:339-341` (`git -C LANE rev-parse master`) |
| 3 | LOW | Running the pinned conform command mutates the host tree transiently: it creates and removes `.ufo/waves/round-40/scratch/mori-conform-selftest-*/` on the host even when invoked from a clone. No residue survived (`ls -d` → same 3 entries before and after), but a clone-side re-execution is not side-effect free on the host. | `.ufo/waves/round-40/conform.py:70` (`SCRATCH_ROOT`) |
| 4 | LOW | `conform.py --selftest` without a rev exits 2 with a raw `TypeError` text (`expected str, bytes or os.PathLike object, not NoneType`) instead of a usage error, because `args.rev` (default `None`) reaches `selftest()`. Pre-existing r40 code, outside round 49's claim. | `.ufo/waves/round-40/conform.py:782-784`, `:791-799` |
| 5 | LOW | Round-49 receipts store no command line, so every re-execution needs the contract plus the `rev=` field to reconstruct the invocation. The `rev` in `after-c1-at-tip.txt` is `64c2d5fc` although the file is named "at tip". | `.ufo/waves/round-49/evidence/after-c1-at-tip.txt`, `contract.md:141-161` |
| 6 | LOW | The 27-`variant`-line vs `variants=26` gap (closure D-f) is explained by `verdict()` printing `len(results) - 1` over 27 entries; the arithmetic is consistent and reproduces, so only documentation is missing. | `.ufo/waves/round-49/count-c1.py:305-309` |
| 7 | LOW | `control-c1-stub-always-met.txt` and `control-c1-stub-filename-sniffer.txt` are byte-identical (same sha256, same `junk_met=18`), so the sniffer pair's able-to-fail weight rests entirely on `control-c1-sniffer-under-r48-counter.txt`. | `.ufo/waves/round-49/evidence/control-c1-stub-*.txt` |
| 8 | LOW | The r49 closure's D-e figure ("seven `round-40/scratch/mori-conform-selftest-*` dirs") no longer matches disk: no such directory exists; `round-40/scratch/` holds 3 unrelated entries. Whatever removed them, the routed defect's record is now stale. | `corpus/lessons/round-49-verifier-spotcheck.md` §1 (D-e) |
