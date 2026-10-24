# ExeParity — round 40 wave 1

## Result

At revision `bb1f2457`, the round-39 counter and round-40 counter produced byte-identical receipts for both seeds (`cmp_exit=0` for each pair).

Counter SHA-256:

- Round-39 `.ufo/waves/round-39/count-c7.py`: `b92c65f224a6268a901aa6bc5ad66b499048eaca82b493356eb8e1f324ef0520`
- Round-40 `.ufo/waves/round-40/count-c8.py`: `4e4d50eb1e96d947f0e9d2ab25a13b2b8c33963f216f3be43060a3348702f6da`

The extracted round-39 byte copy, `.ufo/waves/round-40/fixtures/extracted/count-c7-r39.py`, also hashed to `b92c65f224a6268a901aa6bc5ad66b499048eaca82b493356eb8e1f324ef0520`.

## Commands and outputs

Seed `20261024` command:

```sh
set -o pipefail; python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-39/count-c7.py bb1f2457 --seed 20261024 | tee /dev/stderr | cmp - <(python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/count-c8.py bb1f2457 --seed 20261024); result=$?; printf 'cmp_exit=%s\n' "$result"; exit "$result"
```

Output (the c7 receipt printed by `tee`; c8 receipt compared byte-for-byte):

```text
P-C7: at revision R, the committed drift-corpus binding passes five content checks that the round-38 checks could not discriminate — every `anchor:` line in the knowledge entry is a string of eight or more characters that occurs byte-exactly in tools/mori-source-drift.py at R at a position that is not inside a comment; every path the SCORECARD capability row cites resolves at R to a committed file, not a directory; the live receipt names one drifted row per drifted row its summary counts and every named id has a committed source copy at R; and the probe's selftest named-row arm `row_states` is killed by its own mutation, detected as a structural per-row state difference between the honest and mutated runs whose expected post-mutation state is drawn at run time — and the same counter rejects four fabricated witnesses (an entry carrying tokens with no resolvable anchor, a capability row citing a nonexistent path, a live receipt with only the summary sentence, a self-consistent clone whose anchors are parked inside comments) while the real bytes pass.
negative witness-token-entry        rejected
negative witness-dangling-row       rejected
negative witness-summary-only-live  rejected
negative witness-comment-anchors    rejected
check anchors_v2       PASS (anchors=3 short=[] not_in_code=[] unique=True)
check capability_v2    PASS (paths=['tools/mori-source-drift.py', '.ufo/waves/round-37/evidence/c2-after-v3.txt', '.ufo/waves/round-37/evidence/drift-live-r37.txt'] not_file=[])
check live_rows_v2     PASS (named=10 summary_drifted=10 unknown=[] unique=True no_copy=[])
check named_row_drift  PASS (exit=0 row_states=('PASS', ''))
check drift_kill_v2    PASS (drawn=fresh exit=1 row_states=('FAIL', "got=[('S101', 'fresh'), ('S102', 'excerpt'), ('S103', 'fresh'), ('S104', 'unavailable'), ('S105', 'unavailable'), ('S106', 'no-copy'), ('S107', 'no-copy'), ('S108', 'fresh'), ('S109', 'unavailable'), ('S110', 'unavailable')] want=[('S101', 'fresh'), ('S102', 'excerpt'), ('S103', 'drifted'), ('S104', 'unavailable'), ('S105', 'unavailable'), ('S106', 'no-copy'), ('S107', 'no-copy'), ('S108', 'fresh'), ('S109', 'unavailable'), ('S110', 'unavailable')]") want_drifted=['S103'] flips_ok=True)
C7=met
cmp_exit=0
```

Seed `20261025` command:

```sh
set -o pipefail; python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-39/count-c7.py bb1f2457 --seed 20261025 | tee /dev/stderr | cmp - <(python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/count-c8.py bb1f2457 --seed 20261025); result=$?; printf 'cmp_exit=%s\n' "$result"; exit "$result"
```

Output (the c7 receipt printed by `tee`; c8 receipt compared byte-for-byte):

```text
P-C7: at revision R, the committed drift-corpus binding passes five content checks that the round-38 checks could not discriminate — every `anchor:` line in the knowledge entry is a string of eight or more characters that occurs byte-exactly in tools/mori-source-drift.py at R at a position that is not inside a comment; every path the SCORECARD capability row cites resolves at R to a committed file, not a directory; the live receipt names one drifted row per drifted row its summary counts and every named id has a committed source copy at R; and the probe's selftest named-row arm `row_states` is killed by its own mutation, detected as a structural per-row state difference between the honest and mutated runs whose expected post-mutation state is drawn at run time — and the same counter rejects four fabricated witnesses (an entry carrying tokens with no resolvable anchor, a capability row citing a nonexistent path, a live receipt with only the summary sentence, a self-consistent clone whose anchors are parked inside comments) while the real bytes pass.
negative witness-token-entry        rejected
negative witness-dangling-row       rejected
negative witness-summary-only-live  rejected
negative witness-comment-anchors    rejected
check anchors_v2       PASS (anchors=3 short=[] not_in_code=[] unique=True)
check capability_v2    PASS (paths=['tools/mori-source-drift.py', '.ufo/waves/round-37/evidence/c2-after-v3.txt', '.ufo/waves/round-37/evidence/drift-live-r37.txt'] not_file=[])
check live_rows_v2     PASS (named=10 summary_drifted=10 unknown=[] unique=True no_copy=[])
check named_row_drift  PASS (exit=0 row_states=('PASS', ''))
check drift_kill_v2    PASS (drawn=no-copy exit=1 row_states=('FAIL', "got=[('S101', 'fresh'), ('S102', 'excerpt'), ('S103', 'no-copy'), ('S104', 'unavailable'), ('S105', 'unavailable'), ('S106', 'no-copy'), ('S107', 'no-copy'), ('S108', 'fresh'), ('S109', 'unavailable'), ('S110', 'unavailable')] want=[('S101', 'fresh'), ('S102', 'excerpt'), ('S103', 'drifted'), ('S104', 'unavailable'), ('S105', 'unavailable'), ('S106', 'no-copy'), ('S107', 'no-copy'), ('S108', 'fresh'), ('S109', 'unavailable'), ('S110', 'unavailable')]") want_drifted=['S103'] flips_ok=True)
C7=met
cmp_exit=0
```

Hash commands and outputs:

```sh
sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-39/count-c7.py
b92c65f224a6268a901aa6bc5ad66b499048eaca82b493356eb8e1f324ef0520  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-39/count-c7.py

sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/count-c8.py
4e4d50eb1e96d947f0e9d2ab25a13b2b8c33963f216f3be43060a3348702f6da  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/count-c8.py
```

## Corrected invocation note

I first tried the relocated extracted c7 copy for both seeds. Its relative fixture lookup points at a nonexistent nested `fixtures/` path, so those attempts are not parity evidence; I then ran the actual round-39 counter path above (whose SHA-256 matches the extracted byte copy).

Attempted commands (first seed 20261024, then 20261025):

```sh
set -o pipefail; python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/fixtures/extracted/count-c7-r39.py bb1f2457 --seed 20261024 | tee /dev/stderr | cmp - <(python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/count-c8.py bb1f2457 --seed 20261024); result=$?; printf 'cmp_exit=%s\n' "$result"; exit "$result"
set -o pipefail; python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/fixtures/extracted/count-c7-r39.py bb1f2457 --seed 20261025 | tee /dev/stderr | cmp - <(python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/count-c8.py bb1f2457 --seed 20261025); result=$?; printf 'cmp_exit=%s\n' "$result"; exit "$result"
```

For each command, c7 printed the P-C7 predicate paragraph shown above, followed by:

```text
counter setup error: [Errno 2] No such file or directory: '/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/fixtures/extracted/fixtures/witness-token-entry.md'
cmp: EOF on - after byte 1069
cmp_exit=1
```
