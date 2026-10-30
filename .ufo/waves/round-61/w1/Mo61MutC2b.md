# Mo61MutC2b — frozen C2 mutation probe

Freeze: `7370a731abcafc4c803111de7c22cd6264d63be1`.
Axes: behavioral discrimination, committed-witness coverage, exact restoration.
Detection/report only; no production, registry, contract, or lane VCS changes.

## Finding: ROUTED DEFECT — source-floor arm has no discriminating committed witness

Disabling only count-c2.py:166-167 leaves the committed synthetic battery green:
`C2_SELFTEST pass=10 fail=0`, rc=0 (using `--floor 0`). It also preserves the
committed entering-revision control (`failed=entry_absent`, rc=1).
The positive case cites four copies, but the negative tampered-copy case already
fails on copy_pin/loc_bad, so its additional sources_floor failure is redundant.
Thus the arm is reached, but removal is not detected. This is a coverage finding,
not evidence that the pristine live arm is absent, and not a proposed amendment.

A new scratch-only hostile fixture demonstrates the distinction: all 47 rows
are valid changed rows pointing into psi.c, hence only one copy is cited.
Pristine/restored reject it solely for sources_floor; the mutant accepts it.
The scratch directory name `three_src` is historical: actual measured sources=1,
not three. It is NOT an existing committed lane witness.

## Baseline and kill table

Counter path below is absolute:
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/count-c2.py`.
Line pointers refer to frozen bytes at that path.

| Mutant | Minimal mutation | Expected detector | Actual selftest, floor 0 | Committed-witness verdict |
|---|---|---|---|---|
| M1_nosha | :114 `if sha != PINS[f]` → `if False` | tampered-copy | rc=1, pass=9 fail=1; `case tampered-copy: ok=True want=False FAIL failed=[]` | KILLED |
| M2_movedanchor | :148 same-only → same-or-moved, checking anchor span | positive moved row | rc=1, pass=9 fail=1; `case good: ok=False want=True FAIL failed=['quote_missing:b.c:9']` | KILLED |
| M3_nosrcfloor | :166 `if len(cited) < 4` → `if False` | isolated fewer-than-four-copies case | rc=0, pass=10 fail=0 | SURVIVED → ROUTED DEFECT |
| M4_noprov | :106 provenance predicate → `if False` | no-prov | rc=1, pass=9 fail=1; `case no-prov: ok=True want=False FAIL failed=[]` | KILLED |

Every mutant and pristine/restored bytes returned the same committed control:
```
C2=unmet pointers=47 rows=0 same=0 moved=0 changed=0 quotes_ok=0 spans_ok=0 sources=0 failed=entry_absent rev=325f7e639916fcbc77fa2ec7475951a1b86bb1cb
rc=1
```
This matches the committed receipt at
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/evidence/control-c2-do-nothing.txt:1-2`.

## Default selftest baseline is inconclusive, not a mutant kill

Running the pristine counter with `--selftest --scratch <S>/tmp` and default
floor 40 yields rc=1:
```
case good: ok=False want=True FAIL failed=['pointer_floor:6<40']
C2_SELFTEST pass=9 fail=1
```
All mutated default-floor runs are also red; these are NOT counted as kills,
because pristine is red. With `--floor 0`, pristine is green (10/0), reproducing
the committed receipt. The receipt does not establish the exact original floor;
any floor <=6 would remove this pointer-floor failure. Relevant frozen code:
:38 (default 40), :183-184 (floor rejection), :208-209 (six unique synthetic
pointers repeated), :294 (selftest receives CLI floor). No change proposed.

## Commands and new hostile-fixture receipts

`S=/fast/scratch/hyaku/mori-r61/Mo61MutC2b`; `TMPDIR=$S/tmp`.
Each measured program was invoked as:
```
python3 <absolute-scratch-program.py> --selftest --floor 0 --scratch "$S/tmp/st-<program>-f0"
python3 <absolute-scratch-program.py> 325f7e639916fcbc77fa2ec7475951a1b86bb1cb --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch "$S/tmp"
python3 <absolute-scratch-program.py> <fixture-rev> --repo "$S/fix/<fixture>" --scratch "$S/tmp"
```
Selftest and explicit fixture repos were committed only inside this seat's scratch;
all git calls named `git -C <fixture>`. Fixture top-level assertion preceded add/commit.
The new fixtures use frozen pinned copy bytes and the real 47-pointer source entry;
ledger quotes are single-line byte substrings. A met baseline fixture measured:
`pointers=47 rows=47 same=33 moved=0 changed=14 quotes_ok=47 spans_ok=47 sources=5 failed=none`, rc=0.

| New hostile fixture | Pristine | Corresponding mutant | Restored |
|---|---|---|---|
| tamper: append marker to psi.rst | rc=1 copy_pin + loc_bad | M1 rc=0 met, sources=5 | rc=1 identical pristine |
| moved_bogus: psi.rst:60-65 marked moved with Kconfig:1 location | rc=1 quote_missing:psi.rst:60-65 | M2 rc=0 met, moved=1 | rc=1 identical pristine |
| three_src: 47 changed rows cite only psi.c | rc=1 sources_floor, sources=1 | M3 rc=0 met, sources=1 | rc=1 identical pristine |
| no_prov: provenance trio omitted | rc=1 provenance | M4 rc=0 met | rc=1 identical pristine |

These NEW witnesses discriminate the mutants but do not retroactively count as
committed freeze witnesses. Their full observed outputs follow.

### M1_nosha / tamper
```
pristine/restored: C2=unmet pointers=47 rows=47 same=24 moved=0 changed=14 quotes_ok=38 spans_ok=47 sources=4 failed=copy_pin:psi.rst;loc_bad:psi.rst:60-65;loc_bad:psi.rst:36-38;loc_bad:psi.rst:40-43;loc_bad:psi.rst:45-56;loc_bad:psi.rst:57-59;loc_bad:psi.rst:67-88;loc_bad:psi.rst:102-104;loc_bad:psi.rst:178-187;loc_bad:psi.rst:70-88 rev=ef68fd20e960531ee884fcac4082d8d85f38d22f
rc=1
mutant: C2=met pointers=47 rows=47 same=33 moved=0 changed=14 quotes_ok=47 spans_ok=47 sources=5 failed=none rev=ef68fd20e960531ee884fcac4082d8d85f38d22f
rc=0
```

### M2_movedanchor / moved_bogus
```
pristine/restored: C2=unmet pointers=47 rows=47 same=32 moved=0 changed=14 quotes_ok=46 spans_ok=47 sources=5 failed=quote_missing:psi.rst:60-65 rev=7168ab3f0ffb929de8e109ef80676d266e1f04cd
rc=1
mutant: C2=met pointers=47 rows=47 same=32 moved=1 changed=14 quotes_ok=47 spans_ok=47 sources=5 failed=none rev=7168ab3f0ffb929de8e109ef80676d266e1f04cd
rc=0
```

### M3_nosrcfloor / three_src
```
pristine/restored: C2=unmet pointers=47 rows=47 same=0 moved=0 changed=47 quotes_ok=47 spans_ok=47 sources=1 failed=sources_floor rev=fea8ac02876f0f687b91201184acc9f3a18c1402
rc=1
mutant: C2=met pointers=47 rows=47 same=0 moved=0 changed=47 quotes_ok=47 spans_ok=47 sources=1 failed=none rev=fea8ac02876f0f687b91201184acc9f3a18c1402
rc=0
```

### M4_noprov / no_prov
```
pristine/restored: C2=unmet pointers=47 rows=47 same=33 moved=0 changed=14 quotes_ok=47 spans_ok=47 sources=5 failed=provenance rev=d8e09126e396f3e46b9cda9a0650158501e5a533
rc=1
mutant: C2=met pointers=47 rows=47 same=33 moved=0 changed=14 quotes_ok=47 spans_ok=47 sources=5 failed=none rev=d8e09126e396f3e46b9cda9a0650158501e5a533
rc=0
```

## Restoration and exclusions

Pristine SHA256 before and lane SHA256 after:
`82d0fee6124685f8a50f93550f3665703a33dce644948958db642a77d5aec2d8`.
All four mutant scratch files were overwritten with exact pristine bytes. Each
restored hash equals that value, each restored floor-0 selftest is 10/0 rc=0,
and each restored control and corresponding hostile detector reproduces pristine.

| Scratch mutant | Mutated SHA256 |
|---|---|
| M1_nosha | `d2587d71c4b77f4df625525c0b08a598008752b1f074b90b5613f711b2a83442` |
| M2_movedanchor | `ea5f0a35af5fcb3b861c8101796b3b227050e2249b622dbd1c6278fa50479714` |
| M3_nosrcfloor | `3d2a741e087d5039fb30773c5085608c2c538566a5c8102eb9e5390cd20477d3` |
| M4_noprov | `a4df0eac35316ff61a13884d1d8d3dbcff4972f15e1bfb0f01263a9b0a5feede` |

An exploratory M2b disjunctive variant was also run. It survived the synthetic
battery but did NOT flip the cross-file moved_bogus fixture: its fallback used
the location file rather than the anchor file. It is excluded from the assigned
kill table and from findings; no unsupported moved-arm coverage claim is made.

Disk guard before work: scratch free 370.6G, /tmp free 97.5G; no ENOSPC.
No tools installed or upgraded. Scratch fixtures and scripts removed after copying
these receipts into this report. Production counter was never overwritten.

Self-evaluation: accuracy 4 (extra M2b excluded due to faulty fallback), completeness
4 (all four assigned mutations, control, selftest, hostile and restored runs recorded),
clarity 4 (distinguishes committed witnesses from new fixtures), actionability 4
(exact mutation sites and commands), conciseness 3 (full receipts retained for audit).
Overall 3.8/5; improvement applied: narrowed finding to the supported source-floor
coverage gap. User agreement expected on that bounded verdict.
