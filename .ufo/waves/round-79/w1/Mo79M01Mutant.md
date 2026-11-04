# Mo79M01Mutant — C1 mutation probe

Axes: operability (detector sensitivity), calibration (honest verdicts), freshness (named candidate bytes). Detection only; no source remediation, integration, commits, host state changes, or installations.

## 1. Method and scope

Read the frozen contract, SCORECARD axes and r78 closure, QUALITY 159/161/162/163, and SKILL registry. Copied the executor-notified frozen candidate to an isolated scratch file. Each mutant is one source-line substitution, applied alone with the edit tool; the other command-recognition arms remain intact. M7 forces the normal receipt-check result to 0, not the selftest runner itself. Expected detector: the unchanged `--selftest` must become red (rc 1 and fail>0); pristine and exact-restored candidate must remain green. All seven were KILLED. SURVIVED list: none; no missing arm demonstrated by these probes. Worst class (green selftest plus changed live verdict): none observed.

Candidate (before, baseline, and every exact restoration): `b3b2f9e24d7aff284b1d50deef87a6862253ad20634d644d62c3d73245cdeb0a`.

Initial copy command:
```sh
cp /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py
sha256sum /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py
```
Output: `b3b2f9e24d7aff284b1d50deef87a6862253ad20634d644d62c3d73245cdeb0a  /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py`.

## 2. Mutation table

| mutant | hunk (original line; before → after) | selftest | verdict | live-dir effect (mutant vs restored) |
|---|---|---|---|---|
| M1 | L64: `return False` → `return True` | rc=1; `CONTROL_RECEIPT_SELFTEST pass=16 fail=2` | KILLED | r78 unbound 11→10 (selftests-battery); rc unchanged 1/0. |
| M2 | L68: `if stripped.startswith("$ "):` → `if False:` | rc=1; `CONTROL_RECEIPT_SELFTEST pass=15 fail=3` | KILLED | r78 unbound 11→19; r79 rc 0→1, unbound 0→16. |
| M3 | L70: `if stripped.split(None, 1)[0] in VERBS:` → `if False:` | rc=1; `CONTROL_RECEIPT_SELFTEST pass=17 fail=1` | KILLED | No stdout or rc change in either live dir. |
| M4 | L72: `if " cmd=" in line:` → `if False:` | rc=1; `CONTROL_RECEIPT_SELFTEST pass=17 fail=1` | KILLED | No stdout or rc change in either live dir. |
| M5 | L89: `if line.startswith("## "):` → `if False:` | rc=1; `CONTROL_RECEIPT_SELFTEST pass=15 fail=3` | KILLED | r78 sections 37→15, unbound 11→4; r79 sections 20→4; rc unchanged 1/0. |
| M6 | L52: `CLAIM_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]*=-?[0-9]+$")` → `CLAIM_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]*=.+$")` | rc=1; `CONTROL_RECEIPT_SELFTEST pass=15 fail=3` | KILLED | r78 claims 40→64, unbound 11→18; r79 rc 0→1, claims 49→56, unbound 0→2. |
| M7 | L149: `return 1 if any_unbound else 0` → `return 0` | rc=1; `CONTROL_RECEIPT_SELFTEST pass=9 fail=9` | KILLED | r78 rc 1→0 with unbound=11 unchanged; r79 unchanged. |

### Mutant SHA-256 (after mutation)

- M1: `cb994ba97c6a34a11d860eef29e5549e9356068a4e6253bbfbfa204f9f0c5b6d`
- M2: `fa18bce4f8a507d9c4dbe65f75f5968782a3e4de6129bab094ef937988f95ce9`
- M3: `692676ce5a25d1afa5ff9c34a9c9dd0c685860b0d1e57303dc757cff1cef2382`
- M4: `5613d5c01a04cc99b9e57c82b4df0bab593a79b28ed89e5e3c1705dd0166d389`
- M5: `cf88bd1d54e34589a4fa62ca6ced4a0455e23c6665c9535d88f0b99d1fd5e59a`
- M6: `da2a79ad21310621423307d1f3bc09f3fc5ae1235a90dee1bf45dc92e920d608`
- M7: `87979a90b4b8b925e31997f02641af056490539cdfc727ee9a92d2ba3f8560cd`

## 3. Executed commands and captured output excerpts

All commands below were run by `subprocess.run(..., capture_output=True, text=True, timeout=30, cwd="/fast/scratch/hyaku/mori-r79/Mo79M01Mutant")`. Each block records its own UTC start. Output excerpts retain the detector summary and every failed selftest case; omitted stdout consists of passing selftest cases or per-file receipt detail. All stderr was empty.

### pristine
Tool SHA-256: `b3b2f9e24d7aff284b1d50deef87a6862253ad20634d644d62c3d73245cdeb0a`.

```text
run-start=2026-11-04T05:40:02.497040+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --selftest
CONTROL_RECEIPT_SELFTEST pass=18 fail=0
rc=0
```
```text
run-start=2026-11-04T05:40:02.508621+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence
CONTROL_RECEIPT_SUMMARY files=15 sections=37 claims=40 unbound=11
rc=1
```
```text
run-start=2026-11-04T05:40:02.519479+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-79/evidence
CONTROL_RECEIPT_SUMMARY files=3 sections=15 claims=41 unbound=0
rc=0
```
### M1
Tool SHA-256: `cb994ba97c6a34a11d860eef29e5549e9356068a4e6253bbfbfa204f9f0c5b6d`.

```text
run-start=2026-11-04T05:40:13.851220+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --selftest
case 03 comment line neither command nor claim FAIL
case 12 indented comment/claim handled         FAIL
CONTROL_RECEIPT_SELFTEST pass=16 fail=2
rc=1
```
```text
run-start=2026-11-04T05:40:13.863030+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence
CONTROL_RECEIPT_SUMMARY files=15 sections=37 claims=40 unbound=10
rc=1
```
```text
run-start=2026-11-04T05:40:13.874825+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-79/evidence
CONTROL_RECEIPT_SUMMARY files=3 sections=15 claims=41 unbound=0
rc=0
```
### restored-M1
Tool SHA-256: `b3b2f9e24d7aff284b1d50deef87a6862253ad20634d644d62c3d73245cdeb0a`.

```text
run-start=2026-11-04T05:40:13.891018+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --selftest
CONTROL_RECEIPT_SELFTEST pass=18 fail=0
rc=0
```
```text
run-start=2026-11-04T05:40:13.901992+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence
CONTROL_RECEIPT_SUMMARY files=15 sections=37 claims=40 unbound=11
rc=1
```
```text
run-start=2026-11-04T05:40:13.914358+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-79/evidence
CONTROL_RECEIPT_SUMMARY files=3 sections=15 claims=41 unbound=0
rc=0
```
### M2
Tool SHA-256: `fa18bce4f8a507d9c4dbe65f75f5968782a3e4de6129bab094ef937988f95ce9`.

```text
run-start=2026-11-04T05:40:23.833165+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --selftest
case 01 bound section ($ cmd above count)      FAIL
case 05 split across two ## headings           FAIL
case 15 summary aggregates across files        FAIL
CONTROL_RECEIPT_SELFTEST pass=15 fail=3
rc=1
```
```text
run-start=2026-11-04T05:40:23.844702+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence
CONTROL_RECEIPT_SUMMARY files=15 sections=37 claims=40 unbound=19
rc=1
```
```text
run-start=2026-11-04T05:40:23.856101+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-79/evidence
CONTROL_RECEIPT_SUMMARY files=4 sections=20 claims=49 unbound=16
rc=1
```
### restored-M2
Tool SHA-256: `b3b2f9e24d7aff284b1d50deef87a6862253ad20634d644d62c3d73245cdeb0a`.

```text
run-start=2026-11-04T05:40:23.869273+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --selftest
CONTROL_RECEIPT_SELFTEST pass=18 fail=0
rc=0
```
```text
run-start=2026-11-04T05:40:23.880952+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence
CONTROL_RECEIPT_SUMMARY files=15 sections=37 claims=40 unbound=11
rc=1
```
```text
run-start=2026-11-04T05:40:23.892318+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-79/evidence
CONTROL_RECEIPT_SUMMARY files=4 sections=20 claims=49 unbound=0
rc=0
```
### M3
Tool SHA-256: `692676ce5a25d1afa5ff9c34a9c9dd0c685860b0d1e57303dc757cff1cef2382`.

```text
run-start=2026-11-04T05:40:39.927363+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --selftest
case 11 verb-led first token binds             FAIL
CONTROL_RECEIPT_SELFTEST pass=17 fail=1
rc=1
```
```text
run-start=2026-11-04T05:40:39.938626+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence
CONTROL_RECEIPT_SUMMARY files=15 sections=37 claims=40 unbound=11
rc=1
```
```text
run-start=2026-11-04T05:40:39.950139+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-79/evidence
CONTROL_RECEIPT_SUMMARY files=4 sections=20 claims=49 unbound=0
rc=0
```
### restored-M3
Tool SHA-256: `b3b2f9e24d7aff284b1d50deef87a6862253ad20634d644d62c3d73245cdeb0a`.

```text
run-start=2026-11-04T05:40:39.962488+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --selftest
CONTROL_RECEIPT_SELFTEST pass=18 fail=0
rc=0
```
```text
run-start=2026-11-04T05:40:39.973609+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence
CONTROL_RECEIPT_SUMMARY files=15 sections=37 claims=40 unbound=11
rc=1
```
```text
run-start=2026-11-04T05:40:39.984820+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-79/evidence
CONTROL_RECEIPT_SUMMARY files=4 sections=20 claims=49 unbound=0
rc=0
```
### M4
Tool SHA-256: `5613d5c01a04cc99b9e57c82b4df0bab593a79b28ed89e5e3c1705dd0166d389`.

```text
run-start=2026-11-04T05:40:48.967761+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --selftest
case 04 inline cmd= line binds the section     FAIL
CONTROL_RECEIPT_SELFTEST pass=17 fail=1
rc=1
```
```text
run-start=2026-11-04T05:40:48.979176+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence
CONTROL_RECEIPT_SUMMARY files=15 sections=37 claims=40 unbound=11
rc=1
```
```text
run-start=2026-11-04T05:40:48.990566+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-79/evidence
CONTROL_RECEIPT_SUMMARY files=4 sections=20 claims=49 unbound=0
rc=0
```
### restored-M4
Tool SHA-256: `b3b2f9e24d7aff284b1d50deef87a6862253ad20634d644d62c3d73245cdeb0a`.

```text
run-start=2026-11-04T05:40:49.004106+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --selftest
CONTROL_RECEIPT_SELFTEST pass=18 fail=0
rc=0
```
```text
run-start=2026-11-04T05:40:49.016063+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence
CONTROL_RECEIPT_SUMMARY files=15 sections=37 claims=40 unbound=11
rc=1
```
```text
run-start=2026-11-04T05:40:49.027289+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-79/evidence
CONTROL_RECEIPT_SUMMARY files=4 sections=20 claims=49 unbound=0
rc=0
```
### M5
Tool SHA-256: `cf88bd1d54e34589a4fa62ca6ced4a0455e23c6665c9535d88f0b99d1fd5e59a`.

```text
run-start=2026-11-04T05:40:56.852268+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --selftest
case 05 split across two ## headings           FAIL
case 10 receipt with no claims rc 0            FAIL
case 18 unbound line carries heading text      FAIL
CONTROL_RECEIPT_SELFTEST pass=15 fail=3
rc=1
```
```text
run-start=2026-11-04T05:40:56.863862+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence
CONTROL_RECEIPT_SUMMARY files=15 sections=15 claims=40 unbound=4
rc=1
```
```text
run-start=2026-11-04T05:40:56.874867+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-79/evidence
CONTROL_RECEIPT_SUMMARY files=4 sections=4 claims=49 unbound=0
rc=0
```
### restored-M5
Tool SHA-256: `b3b2f9e24d7aff284b1d50deef87a6862253ad20634d644d62c3d73245cdeb0a`.

```text
run-start=2026-11-04T05:40:56.888078+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --selftest
CONTROL_RECEIPT_SELFTEST pass=18 fail=0
rc=0
```
```text
run-start=2026-11-04T05:40:56.899228+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence
CONTROL_RECEIPT_SUMMARY files=15 sections=37 claims=40 unbound=11
rc=1
```
```text
run-start=2026-11-04T05:40:56.911255+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-79/evidence
CONTROL_RECEIPT_SUMMARY files=4 sections=20 claims=49 unbound=0
rc=0
```
### M6
Tool SHA-256: `da2a79ad21310621423307d1f3bc09f3fc5ae1235a90dee1bf45dc92e920d608`.

```text
run-start=2026-11-04T05:41:06.745390+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --selftest
case 06 non-integer key=value not a claim      FAIL
case 13 claim key character class              FAIL
case 14 bare cmd= without space does not bind  FAIL
CONTROL_RECEIPT_SELFTEST pass=15 fail=3
rc=1
```
```text
run-start=2026-11-04T05:41:06.757053+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence
CONTROL_RECEIPT_SUMMARY files=15 sections=37 claims=64 unbound=18
rc=1
```
```text
run-start=2026-11-04T05:41:06.768490+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-79/evidence
CONTROL_RECEIPT_SUMMARY files=4 sections=20 claims=56 unbound=2
rc=1
```
### restored-M6
Tool SHA-256: `b3b2f9e24d7aff284b1d50deef87a6862253ad20634d644d62c3d73245cdeb0a`.

```text
run-start=2026-11-04T05:41:06.781453+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --selftest
CONTROL_RECEIPT_SELFTEST pass=18 fail=0
rc=0
```
```text
run-start=2026-11-04T05:41:06.792961+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence
CONTROL_RECEIPT_SUMMARY files=15 sections=37 claims=40 unbound=11
rc=1
```
```text
run-start=2026-11-04T05:41:06.804165+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-79/evidence
CONTROL_RECEIPT_SUMMARY files=4 sections=20 claims=49 unbound=0
rc=0
```
### M7
Tool SHA-256: `87979a90b4b8b925e31997f02641af056490539cdfc727ee9a92d2ba3f8560cd`.

```text
run-start=2026-11-04T05:41:17.004664+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --selftest
case 02 unbound section (count, no command)    FAIL
case 03 comment line neither command nor claim FAIL
case 05 split across two ## headings           FAIL
case 07 negative integer claim                 FAIL
case 12 indented comment/claim handled         FAIL
case 13 claim key character class              FAIL
case 14 bare cmd= without space does not bind  FAIL
case 15 summary aggregates across files        FAIL
case 18 unbound line carries heading text      FAIL
CONTROL_RECEIPT_SELFTEST pass=9 fail=9
rc=1
```
```text
run-start=2026-11-04T05:41:17.016219+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence
CONTROL_RECEIPT_SUMMARY files=15 sections=37 claims=40 unbound=11
rc=0
```
```text
run-start=2026-11-04T05:41:17.027720+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-79/evidence
CONTROL_RECEIPT_SUMMARY files=4 sections=20 claims=49 unbound=0
rc=0
```
### restored-M7
Tool SHA-256: `b3b2f9e24d7aff284b1d50deef87a6862253ad20634d644d62c3d73245cdeb0a`.

```text
run-start=2026-11-04T05:41:22.794322+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --selftest
CONTROL_RECEIPT_SELFTEST pass=18 fail=0
rc=0
```
```text
run-start=2026-11-04T05:41:22.805658+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence
CONTROL_RECEIPT_SUMMARY files=15 sections=37 claims=40 unbound=11
rc=1
```
```text
run-start=2026-11-04T05:41:22.816370+00:00
$ python3 -I /fast/scratch/hyaku/mori-r79/Mo79M01Mutant/guard.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-79/evidence
CONTROL_RECEIPT_SUMMARY files=4 sections=20 claims=49 unbound=0
rc=0
```

### D78-1 witness (pristine output excerpt)
```text
unbound /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/controls-r78.txt#4. the D77-3 correction absent at entering claims=1 keys=correction_marker_in_LOG_at_entering
```

## 4. Restoration, limitations, and own defects

1. Restored after each mutant, checked byte equality against the initially captured candidate, and reran the same three commands. Each restored hash is the candidate hash above and each selftest is pass=18 fail=0; restored r78 rc=1 and r79 rc=0. The six initial restorations used the copy command above and exact-byte assertions passed.
2. The lane file changed concurrently before the M7 restoration. Copying it back produced an `AssertionError` against captured pristine bytes; lane SHA-256 then was `38648b602f9a09ea0471ab630b7cb4c693725918325fd3f83790de85a4691316`. Corrected only the scratch file through the write tool using the original captured byte string, then byte-equality assertion passed and restored-M7 ran green. No lane file was edited. Findings apply to the named candidate hash, not later executor bytes.
3. Live r79 evidence changed from 3 files / 15 sections / 41 claims during pristine and M1 to 4 files / 20 sections / 49 claims by M2. This is observed input churn, not a mutant effect. Live effects in the table compare each mutant with its immediate restored run; no live input hashes were captured before the early runs, so identity of every live input byte across paired runs cannot be independently established. Tool-byte identities are captured. Selftest kill verdicts do not depend on live dirs.
4. Own process defects: first shell discovery used ls/head instead of specialized read/glob; no mutation occurred from it. More importantly, restoring from the live source was unsafe under concurrent edits; the equality assertion caught this at M7 and captured original bytes repaired scratch restoration. Future probes should restore from captured bytes from the start.
5. No claim about untested mutations or full contract conformance. No surviving mutants to request new selftest arms for. M3/M4 show live receipts alone do not exercise deletion of verb-list/inline-cmd arms, but their selftest cases kill these mutants.

Self-evaluation: accuracy 4 (live inputs were not snapshotted); completeness 5 (seven probes, three detectors each plus restoration); clarity 4 (summary excerpts rather than full repetitive stdout); actionability 5 (exact hunks and hashes); conciseness 4 (per-run provenance repeats commands). Overall 4.4/5. Improvement: freeze receipt input bytes for byte-identical live comparisons.

## 5. Cleanup evidence

Executed `rm -rf -- /fast/scratch/hyaku/mori-r79/Mo79M01Mutant && test ! -e /fast/scratch/hyaku/mori-r79/Mo79M01Mutant && printf 'scratch_absent=1\n'`; output `scratch_absent=1`, rc 0. No scratch tree remains.
