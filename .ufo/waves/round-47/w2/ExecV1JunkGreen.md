# ExecV1JunkGreen — frozen-v1 junk-variant scores

## Target and verdict

Target: the five requested C1 junk variants `skill-v2-oldcopy.md`, `skill-v3-fakeecho.md`, `skill-v4-weakened.md`, `skill-v7-entrycopy.md`, and `skill-v8-hide+dup.md`, scored with the frozen v1 pin checker using revision `63eecf2738db96f46b0bd02b1b2dfd66787493d0`, floor 26, and baseline `2d85e33d14198d388fd3cda9cc15ec07e57e7a53`.

**Verdict: breaks.** All five variants returned `PIN_CHECK=met` and exit 0 under frozen v1; they preserve the false-green behavior on the assigned corpus. This records the red-before/green-after contrast for the M2 fix: the same variants are unmet under v2 receipts (see table).

## Exact evidence

Frozen tool extracted from freeze commit to `.scratch/r47w2-ExecV1JunkGreen/v1.py`; observed SHA-256 `e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1`, matching the contract's frozen bytes.

Command run for each of the five variants (with `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-ExecV1JunkGreen`):

```text
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-ExecV1JunkGreen/v1.py --repo /home/vgpnk/Projects/shokunin/mori-shokunin --rev 63eecf2738db96f46b0bd02b1b2dfd66787493d0 --min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --skill /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-47/controls/c1-junk/<variant>.md
```

Observed v1 output (all had `EXIT=0`):

| Variant | Relevant v1 finding | Final v1 output |
|---|---|---|
| `skill-v2-oldcopy.md` | line 912: `state=match pinned='pass=15 fail=0' observed='pass=15 fail=0' rc=0 cmd='python3 .scratch/MutGateFirstParent/gate-v3-pristine.py --selftest'` | `PIN_CHECK=met tally_pins=26 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 min_tally_pins=26 rev=63eecf2738db96f46b0bd02b1b2dfd66787493d0 baseline=yes`; `EXIT=0` |
| `skill-v3-fakeecho.md` | line 912: `state=match pinned='pass=15 fail=0' observed='pass=15 fail=0' rc=0 cmd="python3 -c import sys; print('MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0'); sys.exit(0) --selftest"` | `PIN_CHECK=met tally_pins=26 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 min_tally_pins=26 rev=63eecf2738db96f46b0bd02b1b2dfd66787493d0 baseline=yes`; `EXIT=0` |
| `skill-v4-weakened.md` | line 912: `state=match pinned='pass=22' observed='pass=22 fail=0' rc=0 cmd='python3 tools/mori-sources-appendonly.py 63eecf2738db96f46b0bd02b1b2dfd66787493d0 --selftest'` | `PIN_CHECK=met tally_pins=26 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 min_tally_pins=26 rev=63eecf2738db96f46b0bd02b1b2dfd66787493d0 baseline=yes`; `EXIT=0` |
| `skill-v7-entrycopy.md` | line 912: `state=match pinned='pass=15 fail=0' observed='pass=15 fail=0' rc=0 cmd='python3 .scratch/MutGateFirstParent/gate-v3-pristine.py 63eecf2738db96f46b0bd02b1b2dfd66787493d0 --selftest'` | `PIN_CHECK=met tally_pins=26 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 min_tally_pins=26 rev=63eecf2738db96f46b0bd02b1b2dfd66787493d0 baseline=yes`; `EXIT=0` |
| `skill-v8-hide+dup.md` | inserted duplicate at line 913: `state=match pinned='pass=15 fail=0' observed='pass=15 fail=0' rc=0 cmd="python3 -c import sys; print('MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0'); sys.exit(0) --selftest"` | `PIN_CHECK=met tally_pins=26 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 min_tally_pins=26 rev=63eecf2738db96f46b0bd02b1b2dfd66787493d0 baseline=yes`; `EXIT=0` |

V2 comparison: existing receipts `.ufo/waves/round-47/evidence/v2/skill-v2-oldcopy.txt`, `skill-v3-fakeecho.txt`, `skill-v4-weakened.txt`, `skill-v7-entrycopy.txt`, `skill-v8-hide+dup.txt` each end `PIN_CHECK=unmet` (respectively with `no_command=1`, `no_command=1`, `mismatches=1`, `no_command=1`, `unparsed=1`); each has `dropped=0`. These receipts establish the intended contrasting red results for the identical variant files and frozen revision parameters.

Frozen-v1 run output was captured in scratch log `.scratch/r47w2-ExecV1JunkGreen/v1-scores.log`.

## Risks and blockers

The v1 control matrix is intentionally adversarial, not evidence that ordinary registry rows fail. The five v2 comparison outcomes are read from the committed evidence receipts rather than independently rerun in this seat; **UNVERIFIED** here: their live recomputation. No tools installed or updated. No build, lint, test, formatter, or smoke check run.
