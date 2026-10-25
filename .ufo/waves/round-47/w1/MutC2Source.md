# MutC2Source — C2 counter first falsifiers

Scope: scratch-only mutations of `.ufo/waves/round-47/count-c2.py`. The frozen contract was read first. No production files changed.

## Baseline and restored detector

Command for both: `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47-MutC2Source python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47-MutC2Source/count-c2.py --selftest`

Pristine SHA-256 `fc77b93338b3f49b9038eaac3832537b1be2e0ff9dff2476fef750153978901e`; exit 0; output ended `C2_SELFTEST pass=13 fail=0`. Restored SHA-256 identical; exit 0; output ended `C2_SELFTEST pass=13 fail=0`.

## Mutation results

Each mutation used the same `--selftest` command above. The indicated FAIL row is the detector's observed output; each mutated run exited 1.

| Mutant | Mutant SHA-256 | Observed failure/output | Verdict |
|---|---|---|---|
| (a) Accept `queued` source status | `debea8ab4a5112a108227d47ec20e46c5d661ecfb9c838c99ff580f438825843` | `FAIL source_row_queued  C2=met events=2 rows=2 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok rev=fixture`; `C2_SELFTEST pass=12 fail=1` | Killed |
| (b) Skip used-by check | `0844ebbd6c11881bc16ba8b2998d031e8290f140dcc6467b703e3f5eaa963e51` | `C2_SELFTEST pass=13 fail=0` (exit 0) | Survived; coverage finding |
| (c) Skip SHA-256 pin checks | `3a22bc34af8971e2fd568524dc80c4e8c9362e3f8437714dbf7aad56a08e561f` | `FAIL pin_tamper  C2=met events=2 rows=2 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok rev=fixture`; `C2_SELFTEST pass=12 fail=1` | Killed |
| (d) Skip provenance check | `e139085891e33877cd632771d2deca28fd534d31ea913073f9411144a6fc649e` | `FAIL no_provenance  C2=met events=2 rows=2 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok rev=fixture`; `C2_SELFTEST pass=12 fail=1` | Killed |
| (e) Make callsite check always pass | `e5cdfda7f840ea80f8859e5e55195b22c0802b4050c4164fa419170564fc04fa` | `FAIL wrong_callsite  C2=met events=2 rows=2 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok rev=fixture`; `C2_SELFTEST pass=12 fail=1` | Killed |

Restoration evidence: after every mutant, the scratch file was restored from its original bytes. Every restore SHA-256 equaled `fc77b93338b3f49b9038eaac3832537b1be2e0ff9dff2476fef750153978901e`; final scratch hash also equals that baseline. No tool was installed.
