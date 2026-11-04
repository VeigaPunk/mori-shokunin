# Mo80R02Probe — paired-tree falsifier

Axes: calibration, operability, coverage. Detection/report only; no lane implementation edited.

## Findings (severity order)

**High: H is not supported at the measured sweep bytes.** Changing only the requested SCORECARD number removes the stale mismatch but does not produce a clean sweep: three pre-existing wildcard-shaped evidence tokens remain unresolved. This falsifies the bounded deliverable-shape hypothesis, not necessarily the tool's literal frozen pointer rule. No admission or final-round verdict is asserted.

**Positive adversarial result:** replacing a real capability evidence pointer with `corpus/lessons/does-not-exist.md` adds exactly one unresolved mismatch. The unresolved arm distinguishes that defect even with the tally corrected.

## What I did and evidence

1. Read the frozen contract, controls, SCORECARD axes/capabilities/r79 row, SKILL registry, QUALITY 90/154/159/161–164, and PROVINCE. Read `skill://godspeed` and self-evaluation guidance. `read xd://lsp` returned `No such tool: xd://lsp`; semantic definition/reference/diagnostics services were unavailable. Literal searches are not semantic proof.

2. Pinned the actual entering revision:

```text
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse d5888922
d58889220d3c6a18d461f2d31b5ab162ffef1e4f
```

The frozen contract spells the full SHA ending `e4e`; the resolvable named revision ends `e4f`. I used the assignment's actual `d5888922` object, without changing the contract.

For each DIR below, ran the archive pipeline (both completed without diagnostics):

```sh
mkdir -p DIR && git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive d5888922 | tar -x -C DIR
```

DIR values:
- `/fast/scratch/hyaku/mori-r80/Mo80L01Probe/Mo80R02Probe-entering`
- `/fast/scratch/hyaku/mori-r80/Mo80L01Probe/Mo80R02Probe`

The second export's SCORECARD line 4016 was changed only from `selftest 18 in-memory cases` to `selftest 19 in-memory cases` using the edit device. An in-memory byte comparison printed:

```text
original_literal_count= 1
delta_changed_bytes= 1 same_length= True
single_edit_exact= True
```

The specialized literal grep found the original at line 4016 and returned `No matches found` after correction. Those device results expose no shell exit status. A supplementary isolated Python literal matcher (`python3 -I -c`, input = the captured corresponding SCORECARD bytes; `sys.exit(0 if matching_lines else 1)`) measured:

```text
entering literal_match_rc= 0 output= 4016:selftest 18 in-memory cases
corrected literal_match_rc= 1 output= (none)
```

These are Python matcher exit statuses, not fabricated grep statuses. The sweep/pins were initially absent and appeared during the probe, so the final verdict uses the real sweep, not the degraded matcher.

3. Ran the entering export's instrument independently:

```text
$ TMPDIR=<entering-DIR> python3 -I <entering-DIR>/tools/mori-control-receipt.py --selftest
CONTROL_RECEIPT_SELFTEST pass=19 fail=0
rc=0; stderr=''
```

The output also named and passed cases 01–19; summary excerpt above.

4. Ran the two real sweeps concurrently, with each export as process cwd and TMPDIR. Exact command template:

```sh
python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-claim-sweep.py --root DIR --pins /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80/claim-pins.json
```

Measured sweep SHA256: `a481cd28371273d899cbbbe52322c1a1f545cfdead8a6a600abfa884222abe99`.
Measured pins SHA256: `3835315cedf32ab032db817a2c4ffc10ccbabac713b548d6df0d2ded4e81f25a`.
Before/after byte comparisons confirmed both files stayed identical across all three sweep runs. Pins specify control-receipt tally 19 and stale literal `selftest 18 in-memory cases`.

Entering DIR output (complete):

```text
CLAIM_SWEEP_MISMATCH unresolved SCORECARD.md:1558 .ufo/waves/round-24/w2/Mut*.md
CLAIM_SWEEP_MISMATCH unresolved SCORECARD.md:1559 .ufo/waves/round-24/evidence/c1-*.json
CLAIM_SWEEP_MISMATCH unresolved SCORECARD.md:1593 .ufo/waves/round-25/evidence/routed-r24-*-a5.txt
CLAIM_SWEEP_MISMATCH stale SCORECARD.md:4016 'selftest 18 in-memory cases'
CLAIM_SWEEP mismatches=4 unresolved=3 tallies=0 stale=1 carriers=4 pointers=228
rc=1; stderr=''
```

One-number-corrected DIR output (complete):

```text
CLAIM_SWEEP_MISMATCH unresolved SCORECARD.md:1558 .ufo/waves/round-24/w2/Mut*.md
CLAIM_SWEEP_MISMATCH unresolved SCORECARD.md:1559 .ufo/waves/round-24/evidence/c1-*.json
CLAIM_SWEEP_MISMATCH unresolved SCORECARD.md:1593 .ufo/waves/round-25/evidence/routed-r24-*-a5.txt
CLAIM_SWEEP mismatches=3 unresolved=3 tallies=0 stale=0 carriers=4 pointers=228
rc=1; stderr=''
```

The canonical implementation at these bytes explains the result: `tools/mori-claim-sweep.py:87–95` extracts pointer tokens without glob expansion; `:157–165` records missing paths and stale literals independently; `:185–188` aggregates every class and returns nonzero for any mismatch. Thus removing the stale literal cannot erase these three independent unresolved entries.

`sha256sum SCORECARD.md` on the two states:

```text
entering:  93611d782f6b258a6738430db4983e364c13e324c8be020b8c6ac30d2a17dfca
corrected: 82d05025f8accd93151dce9e8194a602a9247f9a7fc85832550a1311286d49fd
```

5. Adversarial variant: retained corrected tally; changed only line 655's source-registry evidence pointer `corpus/SOURCES.md` to `corpus/lessons/does-not-exist.md`. `Path.exists()` printed `False` for the planted target. Re-ran the same corrected-DIR command:

```text
CLAIM_SWEEP_MISMATCH unresolved SCORECARD.md:655 corpus/lessons/does-not-exist.md
CLAIM_SWEEP_MISMATCH unresolved SCORECARD.md:1558 .ufo/waves/round-24/w2/Mut*.md
CLAIM_SWEEP_MISMATCH unresolved SCORECARD.md:1559 .ufo/waves/round-24/evidence/c1-*.json
CLAIM_SWEEP_MISMATCH unresolved SCORECARD.md:1593 .ufo/waves/round-25/evidence/routed-r24-*-a5.txt
CLAIM_SWEEP mismatches=4 unresolved=4 tallies=0 stale=0 carriers=4 pointers=228
rc=1; stderr=''
```

Adversarial SCORECARD SHA256: `2e30a0d0315808112b950a24090aad4e7af09fbf6ef1430bd3cdd35ab4ca898a`.

6. Removed both owned exports using `shutil.rmtree`; post-removal `exists()` printed `False` for each. Removed their now-empty explicitly assigned parent `Mo80L01Probe` using `rmdir`. No scratch tree remains. No tools installed or updated.

## Residual risk and verification gaps

- Verdict: **not supported** at the pinned sweep/pins bytes: stale detection works; correction alone is not clean; adversarial unresolved detection works.
- This probes entering-tree exports with the new sweep and absolute current-wave pins. It does not grade a final committed revision, C2, C3, or later sweep revisions.
- No canonical-runtime rerouting, saturation, or resume-continuity behavior is changed or claimed by this bounded filesystem sweep experiment.
- No implementation remediation performed; the sweep owner received the three concrete unresolved paths.

## Own defects and self-assessment

- Initial discovery used shell directory listings instead of the required file-discovery device; subsequent discovery used glob/grep/read. This did not alter files.
- I initially checked tool absence before it landed; caught its appearance on a later prerequisite check and upgraded to the real paired sweep rather than returning a degraded claim.
- The literal matcher used Python to expose actual return codes because the mandated grep device does not expose them; its statuses are labeled honestly above.
- Accuracy 4/5 (runtime result pinned, final integration not observed); completeness 4/5 (full real hypothesis and adversary, no shell-grep statuses); clarity 4/5 (long evidence blocks retained for audit); actionability 4/5 (three independent blockers named, remediation intentionally out of scope); conciseness 4/5 (command template avoids repeated absolute paths). Overall 4.0/5. Highest-value next integration check: re-run this same bounded pair if sweep semantics change; this report makes no claim about those later bytes.

Post-measurement notice: the sweep owner subsequently reported implementing wildcard expansion and two added selftest cases. That peer statement is not exercised verification here; all three results above remain pinned to the earlier SHA. Scratch had already been deleted, and no later-byte outcome is asserted.
