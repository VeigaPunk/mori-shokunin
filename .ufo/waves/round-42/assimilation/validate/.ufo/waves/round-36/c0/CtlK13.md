measured 2026-10-23T11:51:57Z
control K13 shape rule-level skip (oldest copy)
control_sha256 6ed1fa01223f07ed3a980c8dce291d8a38ec1e367b2a1853116ae14730cbeeb7
counter_sha256 ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145

## Mutation and expected detector

Axes: single-defect fidelity, detector discrimination, exact-byte restoration.
The control implements the C1 CLI and classification rules from `.ufo/waves/round-36/contract.md:35-47`, except its selection comparison is `<` rather than `>`: it selects the lowest integer sources-r<N> containing the row's copy (`.ufo/waves/round-36/c0/controls/K13.py:28-48`, specifically line 46). No state labels or fetch rules were changed.
[INFERENCE] A discriminating fixture with different old and new copy classifications should reject this control. The frozen contract explicitly calls for older decoys (`.ufo/waves/round-36/contract.md:49-52`).

## Frozen bytes

Before scoring and again afterward, command `timeout 120 sha256sum <control> <count-c1.py> <count-c2.py> <scratch subject.py>` produced these final hashes; both counter hashes matched the supplied freeze and `.ufo/waves/round-36/evidence/freeze.txt:3-4`:

```text
6ed1fa01223f07ed3a980c8dce291d8a38ec1e367b2a1853116ae14730cbeeb7  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K13.py
ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py
302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
aba0269af0365e1b3d0436e14debcea41c1523f1de660ec2cc04bdbe972723cd  /fast/scratch/hyaku/mori-r36/CtlK13/subject.py
```

## Scored run — full counter output

Command (no --seed):

```text
timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py 6bd57097 --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/K13.py
```

Environment: `MORI_R36_SCRATCH=/fast/scratch/hyaku/mori-r36/CtlK13`; `PYTHONDONTWRITEBYTECODE=1`. The subprocess returned exit 0. Complete stdout follows; stderr was empty. Raw receipts: `/fast/scratch/hyaku/mori-r36/CtlK13/counter.stdout.txt`, `counter.stderr.txt`, `counter.exit.txt`.

```text
P-C1: at revision R, tools/mori-source-drift.py classifies every row of a 40-row blind fixture drawn at run time exactly as the counter's hidden truth, and on the lane's own corpus/SOURCES.md at R it agrees with the counter's independent live oracle on every row the oracle classified, with at least 10 oracle-fetched rows including at least one oracle-fresh and one oracle-drifted row.
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
real_rows=204 oracle_fetched=42 oracle_fresh=35 oracle_drifted=7 oracle_excluded=0 tool_exit=1 tool_rows=204 mismatches=0
C1=met
seed=5651777992482807522
```

VERDICT: K13 met exit 0

## Pristine / mutated / restored probe

The same bounded command was run on all three subject byte states:
`timeout 120 python3 /fast/scratch/hyaku/mori-r36/CtlK13/detect.py <phase>`.
The detector invokes the frozen counter's `blind_arm` with replay seed 6213, not the real arm; these supplemental runs are not scored receipts. Detector source: `/fast/scratch/hyaku/mori-r36/CtlK13/detect.py:1-35`.

Pristine actual output (`/fast/scratch/hyaku/mori-r36/CtlK13/pristine.txt`):

```text
detector=frozen_count_c1_blind seed=6213
subject_sha256=aba0269af0365e1b3d0436e14debcea41c1523f1de660ec2cc04bdbe972723cd
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
detector=pass
exit=0
```

Mutated actual output (`/fast/scratch/hyaku/mori-r36/CtlK13/mutated.txt`), after changing only the selection operator at subject.py:46:

```text
detector=frozen_count_c1_blind seed=6213
subject_sha256=6ed1fa01223f07ed3a980c8dce291d8a38ec1e367b2a1853116ae14730cbeeb7
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
detector=pass
exit=0
```

Restored actual output (`/fast/scratch/hyaku/mori-r36/CtlK13/restored.txt`), after changing that operator back:

```text
detector=frozen_count_c1_blind seed=6213
subject_sha256=aba0269af0365e1b3d0436e14debcea41c1523f1de660ec2cc04bdbe972723cd
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
detector=pass
exit=0
```

The mutation survived both the supplemental blind detector and the scored frozen counter. Pristine and restored subject hashes are identical; the mutant hash equals the retained control hash. The scratch subject is restored exactly; the requested defective control remains intentionally.

## Coverage finding and containment

The frozen counter builds `with_copy` from integer row positions and stores a subset in `decoy_rows` (`.ufo/waves/round-36/count-c1.py:395-397`), but the decoy writer tests string source ids for membership (`count-c1.py:511-512`; string ids originate at `count-c1.py:388`). [INFERENCE] This type mismatch skips every intended older decoy, leaving the blind arm unable to distinguish oldest-copy selection. No counter or contract was amended. The owner decision rule for a met control is recorded at `.ufo/waves/round-36/contract.md:85-88`.

The scoring wrapper's process-session cleanup reported `remaining_started_processes_cleaned=0` after the counter exited: no running descendants remained. Lane writes were limited to this report and the named K13 control; all probe files and counter fixtures were under the seat's scratch root. No git writes or tool installs/updates were performed. Existing runtime: command `timeout 120 python3 --version` returned `Python 3.14.8`. Timestamp command `timeout 120 date -u +%FT%TZ` returned the first line's measurement time.
