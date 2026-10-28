# Mo60MutationTester34 — C3 gate mutants (execute-ignoring-pin / no containment / accept any expect.txt)

Seat: mutation tester, round 60 w1. Lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin`
(read-only; no commits, no VCS mutation, no fleet/sibling writes).
Frozen contract: `.ufo/waves/round-60/contract.md`, freeze revision
`ac496c7cde8cad965079858accae3bedfe4a73f2`; entering revision
`ddfb12fb0838b4307c445194a844f0c4b1950195`. Lane tip during the run:
`b3c256138f00c704d5aa56eb0332d74506502ef2` (moved by C1 data landing, as the
dispatch warned); every re-derivation below is pinned to `ac496c7c…`.
Disk guard `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`:
green (26% used, 600 G free on `/fast`). No tools installed.

## 1. Setup and baseline

Counters at the freeze revision are byte-identical to the working tree:

```
count-c1.py 795c1f3193a76406a40561ac60fedb3eee75fc38df2b2efb3fc5295d617ddbae
count-c2.py 8c4814f54c564a7f00beec5249de092a2d3b2c4043e07be773d80e8e3ccdf976
count-c3.py fabde06c9d0a94a8487e5de45be3e413f6084816fb0507a71fd335bad5153514
```

Sandbox: `git clone --shared --no-checkout <lane> $SCRATCH/clone` then
`git -C clone checkout ac496c7c…`; `git -C clone rev-parse --show-toplevel`
printed the clone path before every mutation commit. All mutants are commits
*inside that throwaway clone*; the lane never saw a write (see §6).

Selftest (freeze bytes):
`C3_SELFTEST pass=3 fail=0`, exit 0 — matches the contract.

Baseline at the freeze revision (`--scratch` under my scratch root) reproduces
`evidence/c3-at-freeze.txt` byte-for-byte:

```
$ python3 .ufo/waves/round-60/count-c3.py ac496c7c… --scratch $D/out/base
C3=met toolgate=ok containment=ok expectgate=ok cases=6 rev=ac496c7cde8cad965079858accae3bedfe4a73f2
exit=0
# only marker anywhere: BASE/g1-old/st2/EXEC-MARKER  (the G1 old-counter control, by design)
```

## 2. Probe design (two probes per mutant)

* **Probe A — shipped instrument.** Pristine `count-c3.py` (freeze bytes),
  rev R = the mutant commit, pin intact. This is what the claim actually runs.
* **Probe B — behavioural coverage.** The same `count-c3.py` with exactly one
  line changed, `c2_ok = c2_b is not None` (was
  `c2_b is not None and sha256(c2_b) == PIN_C2`, line 140-141 of the freeze
  bytes), so the G1/G2/G3 arms execute instead of being skipped by the hash
  gate. Probe B answers *which clause kills the mutant*, independent of the
  pin. It is not a claim about shipped bytes; it is the mutant-coverage
  question.
* Detector = the counter's printed `C3=` line + exit code plus an independent
  filesystem scan of the scratch for `EXEC-MARKER` / escape artifacts.

Mutant revs/shas in the clone (single file touched each time,
`.ufo/waves/round-60/count-c2.py`):

| id | defect | rev | c2 sha256 |
|---|---|---|---|
| M1 | entry-claims tool written+executed regardless of pin (`run_pinned` guard, the `ec_ok` execution gate, and the materialize guard removed; `tool_sha` reason still emitted) | `296a8917bc74b451e527fa604412dcd50ed41799` | `97e87cca4122baa28cc881bde99f65837a91c91923a504f4d8738adbc98315ac` |
| M2 | containment assert dropped from `materialize()` (no refuse path) | `324a34a0f19b0f53e391b77b1e4a0293fb9d75db` | `af57a93785d0c2fc9f0af2ff4c8764360f01f2cba8d3bfc5f5ac9cca18838699` |
| M2b | M2 + write errors swallowed (a robust sloppy writer) | `34d8912c13efb1bcaedd202da57e5889ef71024e` | `58f3abb7f48078162350aec33d14f0989e5f9db6c68e81ea6bd3dd03ba6ea380` |
| M3 | committed `expect.txt` accepted without comparison to the frozen table | `8cd61d1e3f99d5d55f60b32969c8ee5a2816a1e6` | `4fef51ce51032e67f2a4016a4513c9a2c0ff91ba74a51fce88d2b610611a39ee` |
| M4 | battery variant: G1-new arm wired to the r59 (unpinned) counter, i.e. execute the blob regardless of pin at the *battery* level (`count-c3.py` line 167) | freeze rev (script copy, no commit) | n/a |

## 3. Results

### M1 — execute the blob regardless of pin

Probe A (shipped bytes, pin intact) — **killed by the c2 hash pin, zero
execution**:

```
C3=unmet toolgate=bad containment=bad expectgate=bad cases=1 rev=296a8917… failed=count_c2_sha,g1_new_skipped,g2_skipped,g3_skipped
exit=1
# markers in pa-m1: only pa-m1/g1-old/st2/EXEC-MARKER ; pa-m1/g1-new is empty
```

Probe B (pin relaxed; behavioural arms only) — **killed by the marker scan**:

```
C3=unmet toolgate=ok containment=ok expectgate=ok cases=6 rev=296a8917… failed=g1_new_executed:$D/out/pb-m1/g1-new/st/EXEC-MARKER
exit=1
# markers: OUT/pb-m1/g1-new/st/EXEC-MARKER ; OUT/pb-m1/g1-old/st2/EXEC-MARKER
# marker bytes: executed --selftest --scratch $D/out/pb-m1/g1-new/st
```

Note: `gated` was **true** (the mutant still prints `tool_sha`), so the
string check at `count-c3.py:174` passed and only `no_exec`
(`count-c3.py:173,175`) produced the kill. The `g1_new_no_tool_sha` token did
not fire.

Detector-removal control (`toolgate = gated`, marker clause deleted, pin
relaxed) at the M1 rev — **survives, i.e. the marker clause is necessary**:

```
C3=met toolgate=ok containment=ok expectgate=ok cases=6 rev=296a8917…
exit=0
# markers: OUT/dr-m1/g1-new/st/EXEC-MARKER present  -> green verdict with the hole reproduced
```

### M2 / M2b — containment assert dropped

Probe A (pin intact) — **killed by the pin, no escape attempted**:
`C3=unmet … failed=count_c2_sha,g1_new_skipped,g2_skipped,g3_skipped`, exit 1;
no `escape.txt` anywhere under `pa-m2`.

Probe B at M2 (assert dropped, no error handling) — **killed by the counter
aborting; escape write already on disk, no `C3=` line at all**:

```
Traceback (most recent call last):
  File "$D/out/c3-relaxed.py", line 216, in measure
    r3 = mod.materialize(g2, "ln/f.txt", b"x")
  File "$D/out/pb-m2/c2-mod.py", line 138, in materialize
    t.parent.mkdir(parents=True, exist_ok=True)
FileExistsError: [Errno 17] File exists: '$D/out/pb-m2/g2/ln'
# exit 1
# escape artifact: OUT/pb-m2/escape.txt  (1 byte, 0x78 = "x") written outside the sanctioned g2 root
```

Probe B at M2b (assert dropped, errors swallowed) — **killed by the three G2
tokens**:

```
C3=unmet toolgate=ok containment=ok expectgate=ok cases=6 rev=34d8912c… failed=g2_escape_written,g2_parent_escape,g2_symlink_escape
exit=1
# escape artifacts: OUT/pb-m2b/escape.txt (1 byte); OUT/pb-m2b/g2/inside/f.txt; g2/ln -> nowhere
```

### M3 — accept any expect.txt

Probe A (pin intact) — **killed by the pin**:
`C3=unmet … failed=count_c2_sha,g1_new_skipped,g2_skipped,g3_skipped`, exit 1.

Probe B (pin relaxed) — **killed by the expectgate arm**:

```
C3=unmet toolgate=ok containment=ok expectgate=ok cases=6 rev=8cd61d1e… failed=g3_no_tamper_flag
exit=1
```

Direct A/B on one tampered PoC tree (fixture repo created with `mktemp -d -p
$SCRATCH/tmp`, `git -C "$F" init -q`, toplevel asserted;
`.ufo/waves/round-60/trees-c2h/h02-malformed-claim/expect.txt` =
`grammar\nTAMPERED-EXTRA\n`, rev `392b186b…`), pristine c2 vs M3 c2:

```
pristine c2: expect_tamper:h02-malformed-claim count = 1
M3 c2:       expect_tamper:h02-malformed-claim count = 0   (tamper unflagged; its only tree token is tree:h02-malformed-claim:tool)
```

### M4 — battery-level “execute the blob regardless of pin”

`count-c3.py` copy with the G1-new arm invoking `run_counter(r59c2_b, …)`
instead of the pinned `c2_b`, run at the freeze rev — **killed by the marker
scan**:

```
C3=unmet toolgate=ok containment=ok expectgate=ok cases=6 rev=ac496c7c… failed=g1_new_executed:$D/out/m4/g1-new/st2/EXEC-MARKER
exit=1
# marker bytes: executed --selftest --scratch $D/out/m4/g1-new/st2
```

## 4. Verdicts

| mutant | expected detector | actual | verdict |
|---|---|---|---|
| M1 (execute regardless of pin) | marker appears → `g1_new_executed` | Probe A: `count_c2_sha`, no execution, no marker. Probe B: marker at `g1-new/st/EXEC-MARKER`, `failed=g1_new_executed:…`, exit 1 | **killed** (pin; behaviourally by the marker scan — the `tool_sha` string alone did not catch it) |
| M2 (containment assert dropped) | escape writes → containment bad | Probe A: pin kill, no escape. Probe B: `escape.txt` written at scratch root, counter aborts with `FileExistsError` (no `C3=` line), exit 1 | **killed** (pin; behaviourally by non-verdict + escape artifact) |
| M2b (same, errors swallowed) | escape writes → `g2_*` tokens | Probe A: pin kill. Probe B: `failed=g2_escape_written,g2_parent_escape,g2_symlink_escape`, exit 1 | **killed** |
| M3 (accept any expect.txt) | tamper unflagged → `g3_no_tamper_flag` | Probe A: pin kill. Probe B: `failed=g3_no_tamper_flag`; A/B shows pristine c2 prints `expect_tamper:…`, M3 c2 does not | **killed** |
| M4 (battery wires old counter) | marker appears → `g1_new_executed` | marker present, `failed=g1_new_executed:…` at the freeze rev | **killed** |
| detector-removal (marker clause deleted) | should kill M1 | `C3=met`, exit 0, marker present | **survives — by construction; records that `g1_new_executed` is the only guard for marker execution** |

No baseline failure: the pristine pre-mutation and post-restoration runs both
printed the frozen `C3=met … cases=6` line with exit 0 (§6).

## 5. Findings (report only, no remediation)

**F1 — per-gate ok/bad labels are not causally derived (`count-c3.py:298-305`).**
The three labels test for the literals `"toolgate"`, `"containment"`,
`"expectgate"` in `failed`, but no `failed.append` site ever emits those
literals (`count-c3.py:143-253` appends `count_c2_sha`, `g1_new_no_tool_sha`,
`g1_new_executed:…`, `g2_parent_escape`, `g2_escape_written`,
`g2_symlink_escape`, `g3_no_tamper_flag`, …). Only the corresponding
`*_skipped` token flips a label to `bad`, so the labels really mean “the arm
ran”, not “the gate held”. Reproduced four times in this seat:

```
C3=unmet toolgate=ok containment=ok expectgate=ok … failed=g1_new_executed:…      (pb-m1)
C3=unmet toolgate=ok containment=ok expectgate=ok … failed=g2_escape_written,…     (pb-m2b)
C3=unmet toolgate=ok containment=ok expectgate=ok … failed=g3_no_tamper_flag       (pb-m3)
C3=unmet toolgate=ok containment=ok expectgate=ok … failed=g1_new_executed:…      (m4)
```

`met` and the exit code use the booleans and stayed correct in every run, so
the frozen claim's truth value is not affected; the printed predicate token
is. The §9 do-nothing control cannot expose this (its arms are skipped, which
is the one path that yields `bad`). Severity: reporting defect, latent until
a non-met verdict occurs.

**F2 — the G2 arm cannot produce a verdict for a fully uncontained writer.**
With the assert dropped (M2) the `..` escape is already written
(`pb-m2/escape.txt`) before `materialize("ln/f.txt")` raises
`FileExistsError` inside the imported subject; the counter dies with a
traceback and emits no `C3=` line. A dropped-assert subject is still caught
(no verdict, exit 1, escape artifact), and the `g2_*` tokens are reachable
with an error-swallowing writer (M2b), but the counter has no exception
boundary around the imported subject's `materialize`.

**F3 — G1 is genuinely two-detector.** The mutant that keeps printing
`tool_sha` while executing (M1) passes `gated` and is caught only by
`no_exec` / `markers_under` (`count-c3.py:173-175`); deleting that clause
yields `C3=met` with the marker on disk. G1's pin plus marker scan are
independently necessary.

**F4 — the c2 hash pin is the first-line kill for all three gate mutants.**
Probe A on M1/M2/M2b/M3 always returned
`failed=count_c2_sha,g1_new_skipped,g2_skipped,g3_skipped` with no marker and
no escape write, i.e. the behavioural arms are unreachable for a non-pinned
counter — correct defence, and it means each behavioural clause is only ever
exercised against pinned bytes.

## 6. Restoration and containment evidence

```
m1  c2 97e87cca4122baa28cc881bde99f65837a91c91923a504f4d8738adbc98315ac
m2  c2 af57a93785d0c2fc9f0af2ff4c8764360f01f2cba8d3bfc5f5ac9cca18838699
m2b c2 58f3abb7f48078162350aec33d14f0989e5f9db6c68e81ea6bd3dd03ba6ea380
m3  c2 4fef51ce51032e67f2a4016a4513c9a2c0ff91ba74a51fce88d2b610611a39ee
restored (git -C clone checkout ac496c7c…):
    c2 8c4814f54c564a7f00beec5249de092a2d3b2c4043e07be773d80e8e3ccdf976
    c3 fabde06c9d0a94a8487e5de45be3e413f6084816fb0507a71fd335bad5153514
    clone git status --porcelain: 0 lines
post-restoration baseline:
    C3=met toolgate=ok containment=ok expectgate=ok cases=6 rev=ac496c7cde8cad965079858accae3bedfe4a73f2   (exit 0)
    markers: only g1-old/st2/EXEC-MARKER
lane untouched (frozen-bytes hash + status, after all runs):
    count-c1.py 795c1f31…5d617ddbae / count-c2.py 8c4814f5…ccdf976 / count-c3.py fabde06c…5153514
    git status --porcelain on the three counters: no lines; lane head b3c25613… (unchanged by me)
```

All writes stayed under `/fast/scratch/hyaku/mori-r60/Mo60MutationTester34/`
(clone, `$TMPDIR`, run scratches, detector copies); the scratch root was
removed after the report was written from these receipts. No lane, corpus,
SCORECARD, LOG, fleet or sibling write; no commits outside the throwaway
clone; no subagents; no tool installs.
