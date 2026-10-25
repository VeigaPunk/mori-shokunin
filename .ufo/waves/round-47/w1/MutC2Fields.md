# MutC2Fields — round 47 w1

## Baseline

Command (with `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47-MutC2Fields`):
`python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47-MutC2Fields/count-c2.py --selftest`

Output: `C2_SELFTEST pass=13 fail=0`; exit 0. All 13 named checks printed PASS (honest, missing event, invented event, missing field, wrong callsite, pin tamper, no source row, no provenance, no table, duplicate row, entry absent, queued source row, CLI non-repo rc2).

Pristine production and scratch-copy SHA-256 both equal the contract's frozen hash `fc77b93338b3f49b9038eaac3832537b1be2e0ff9dff2476fef750153978901e`.

## Mutation probes

UNVERIFIED / not executed: (a) field-set equality → subset; (b) skip `__string` fields; (c) remove duplicate-row rejection; (d) remove missing-event comparison.

The repository counter file is protected from edits by the assignment. I attempted the required scratch edit using the hash-anchored editor after reading the target lines, but the editor returned `File not found: .scratch/r47-MutC2Fields/count-c2.py. Use the write tool to create new files.` The scratch copy was created and baseline-run successfully, but I could not safely perform the mutations with the available surgical-edit path. No mutant verdicts or missing-arm conclusions are claimed.

Restoration evidence: scratch copy remained pristine; its SHA-256 was the frozen hash before and after the failed edit attempt. Production file was not modified. Since no mutant was successfully applied, mutant-specific detector outputs are unavailable.
