# Mo100ExecReplay — full measurement replay, mori round-100 w1 (2026-11-05)

Seat: executor, replay of every frozen measurement + controls re-run + freeze integrity.
Revisions: entering `d1bd1b339b894de0249b0f60702dff9962da88d9`, landing `5e2bcf2c487e377b51287c587144bdde5b233f8f`,
freeze `9579cff6cfab2f06b1918e54aec4a5553b705a9c`. `git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse master`
→ `5e2bcf2c487e377b51287c587144bdde5b233f8f` (TIP == landing; tip runs are a second measurement of the landing tree).
Method: `git archive <rev> | tar -x` into `$S/{entering,landing,tip}`; counters run exactly per contract
(`count-c1.py --root DIR --work $S [--seed N]`, `count-c2.py --root DIR --repo LANE`). Read-only git only; no
mutations anywhere; no tools installed (none needed). Scratch `$S=/fast/scratch/hyaku/mori-r100/Mo100ExecReplay`,
removed at end.

## 0. Frozen receipts (copied from evidence/, read-only)

`evidence/before-c1.txt` (entering, seed 100):
```
# 2026-11-05T23:10:13Z entering d1bd1b33 archive -> python3 count-c1.py --root DIR --seed 100
C1=unmet cases_ok=23/50 families_failed=A1-auth-status,A2-auth-spelling,A3-auth-escaped,A4-auth-status-composed,A5-auth-spelling-composed,Z1-zai-unmapped-auth selftest=ok r17gate=ok registry=unmet sourced=unmet checks_failed=battery,registry,sourced seed=100 tool_rc=1
exit=1
```
`evidence/landing-c1.txt` (landing, seed 100 / unseeded):
```
# 2026-11-05T23:10:53Z landing 5e2bcf2c archive -> python3 count-c1.py --root DIR --seed 100 / unseeded
C1=met cases_ok=50/50 families_failed=- selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=- seed=100 tool_rc=1
exit=0
C1=met cases_ok=50/50 families_failed=- selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=- seed=2103123362 tool_rc=1
exit=0
```
`evidence/before-c2.txt`:
```
# 2026-11-05T23:10:21Z entering d1bd1b33 archive -> python3 count-c2.py --root DIR --list
C2=unmet stated=58 mismatches=7 uncorrected=7 spurious=0 altered=0 census=ok checks_failed=mismatch base=d1bd1b33
  uncorrected S581 10->9,15->14
  uncorrected S582 14->13
  uncorrected S583 14->13
  uncorrected S584 17->15,22->26
  uncorrected S634 17->18
exit=1
```
`evidence/landing-c2.txt`:
```
# 2026-11-05T23:11:14Z landing 5e2bcf2c archive -> python3 count-c2.py --root DIR --list
C2=met stated=60 mismatches=7 uncorrected=0 spurious=0 altered=0 census=ok checks_failed=- base=d1bd1b33
exit=0
```
`evidence/controls-r100.txt` ends (seed 100): `CONTROLS_DONE unexpected=0 rev=d1bd1b339b894de0249b0f60702dff9962da88d9 seed=100`
(P1 expect=met got=met, P2 expect=met got=met; all K-lines AS_EXPECTED).
`evidence/live-errors-prefreeze.txt` (cited by the claim): `r99_dead_error_other 190 of_which_auth_evidence 187`.

## 1. C1 replay — entering d1bd1b33 (all four runs reproduce the frozen receipt exactly)

```
== C1 entering seed=1 ==
C1=unmet cases_ok=23/50 families_failed=A1-auth-status,A2-auth-spelling,A3-auth-escaped,A4-auth-status-composed,A5-auth-spelling-composed,Z1-zai-unmapped-auth selftest=ok r17gate=ok registry=unmet sourced=unmet checks_failed=battery,registry,sourced seed=1 tool_rc=1
  miss C012:A2-auth-spelling:want=dead_auth:got=dead_error_other
  miss C038:A5-auth-spelling-composed:want=dead_auth:got=dead_error_other
  miss C034:A4-auth-status-composed:want=dead_auth:got=dead_error_other
  miss C001:A1-auth-status:want=dead_auth:got=dead_error_other
  miss C010:A2-auth-spelling:want=dead_auth:got=dead_error_other
  miss C015:A2-auth-spelling:want=dead_auth:got=dead_error_other
  miss C006:A1-auth-status:want=dead_auth:got=dead_error_other
  miss C040:A5-auth-spelling-composed:want=dead_auth:got=dead_error_other
  miss C037:A5-auth-spelling-composed:want=dead_auth:got=dead_error_other
  miss C036:A4-auth-status-composed:want=dead_auth:got=dead_error_other
  miss C004:A1-auth-status:want=dead_auth:got=dead_error_other
  miss C005:A1-auth-status:want=dead_auth:got=dead_error_other
exit=1
== C1 entering seed=7 ==
C1=unmet cases_ok=23/50 families_failed=A1-auth-status,A2-auth-spelling,A3-auth-escaped,A4-auth-status-composed,A5-auth-spelling-composed,Z1-zai-unmapped-auth selftest=ok r17gate=ok registry=unmet sourced=unmet checks_failed=battery,registry,sourced seed=7 tool_rc=1
  miss C010:A2-auth-spelling:want=dead_auth:got=dead_error_other
  miss C004:A1-auth-status:want=dead_auth:got=dead_error_other
  miss C017:A3-auth-escaped:want=dead_auth:got=dead_error_other
  miss C050:Z1-zai-unmapped-auth:want=dead_auth:got=dead_error_other
  miss C036:A4-auth-status-composed:want=dead_auth:got=dead_error_other
  miss C014:A2-auth-spelling:want=dead_auth:got=dead_error_other
  miss C007:A1-auth-status:want=dead_auth:got=dead_error_other
  miss C003:A1-auth-status:want=dead_auth:got=dead_error_other
  miss C033:A4-auth-status-composed:want=dead_auth:got=dead_error_other
  miss C034:A4-auth-status-composed:want=dead_auth:got=dead_error_other
  miss C001:A1-auth-status:want=dead_auth:got=dead_error_other
  miss C038:A5-auth-spelling-composed:want=dead_auth:got=dead_error_other
exit=1
== C1 entering seed=2026 ==
C1=unmet cases_ok=23/50 families_failed=A1-auth-status,A2-auth-spelling,A3-auth-escaped,A4-auth-status-composed,A5-auth-spelling-composed,Z1-zai-unmapped-auth selftest=ok r17gate=ok registry=unmet sourced=unmet checks_failed=battery,registry,sourced seed=2026 tool_rc=1
  miss C016:A2-auth-spelling:want=dead_auth:got=dead_error_other
  miss C013:A2-auth-spelling:want=dead_auth:got=dead_error_other
  miss C008:A1-auth-status:want=dead_auth:got=dead_error_other
  miss C033:A4-auth-status-composed:want=dead_auth:got=dead_error_other
  miss C001:A1-auth-status:want=dead_auth:got=dead_error_other
  miss C002:A1-auth-status:want=dead_auth:got=dead_error_other
  miss C015:A2-auth-spelling:want=dead_auth:got=dead_error_other
  miss C005:A1-auth-status:want=dead_auth:got=dead_error_other
  miss C010:A2-auth-spelling:want=dead_auth:got=dead_error_other
  miss C003:A1-auth-status:want=dead_auth:got=dead_error_other
  miss C039:A5-auth-spelling-composed:want=dead_auth:got=dead_error_other
  miss C034:A4-auth-status-composed:want=dead_auth:got=dead_error_other
exit=1
== C1 entering unseeded ==
C1=unmet cases_ok=23/50 families_failed=A1-auth-status,A2-auth-spelling,A3-auth-escaped,A4-auth-status-composed,A5-auth-spelling-composed,Z1-zai-unmapped-auth selftest=ok r17gate=ok registry=unmet sourced=unmet checks_failed=battery,registry,sourced seed=608439923 tool_rc=1
  miss C017:A3-auth-escaped:want=dead_auth:got=dead_error_other
  miss C035:A4-auth-status-composed:want=dead_auth:got=dead_error_other
  miss C040:A5-auth-spelling-composed:want=dead_auth:got=dead_error_other
  miss C016:A2-auth-spelling:want=dead_auth:got=dead_error_other
  miss C038:A5-auth-spelling-composed:want=dead_auth:got=dead_error_other
  miss C013:A2-auth-spelling:want=dead_auth:got=dead_error_other
  miss C008:A1-auth-status:want=dead_auth:got=dead_error_other
  miss C050:Z1-zai-unmapped-auth:want=dead_auth:got=dead_error_other
  miss C004:A1-auth-status:want=dead_auth:got=dead_error_other
  miss C011:A2-auth-spelling:want=dead_auth:got=dead_error_other
  miss C039:A5-auth-spelling-composed:want=dead_auth:got=dead_error_other
  miss C006:A1-auth-status:want=dead_auth:got=dead_error_other
exit=1
```

## 2. C1 replay — landing 5e2bcf2 (mandated seeds) and tip

```
== C1 landing seed=1 ==  C1=met cases_ok=50/50 families_failed=- selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=- seed=1 tool_rc=1  (exit=0)
== C1 landing seed=7 ==  C1=met cases_ok=50/50 families_failed=- selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=- seed=7 tool_rc=1  (exit=0)
== C1 landing seed=2026 == C1=met cases_ok=50/50 families_failed=- selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=- seed=2026 tool_rc=1 (exit=0)
== C1 landing unseeded == C1=met cases_ok=50/50 families_failed=- selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=- seed=557468927 tool_rc=1 (exit=0)
== C1 tip seed=1 ==      C1=met cases_ok=50/50 families_failed=- selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=- seed=1 tool_rc=1  (exit=0)
== C1 tip seed=7 ==      C1=met cases_ok=50/50 families_failed=- selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=- seed=7 tool_rc=1  (exit=0)
== C1 tip seed=2026 ==   C1=met cases_ok=50/50 families_failed=- selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=- seed=2026 tool_rc=1 (exit=0)
== C1 tip unseeded ==    C1=met cases_ok=50/50 families_failed=- selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=- seed=100257949 tool_rc=1 (exit=0)
== C1 landing seed=100 (direct re-run of the receipt seed) == C1=met cases_ok=50/50 families_failed=- selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=- seed=100 tool_rc=1 (exit=0)
```

## 3. FINDING — landing C1 fails on other seeds (contract kill rule: "any family failing on any seed at landing = C1 unmet")

Direct re-runs of `count-c1.py` on the landing tree (identical 49/50 line reproduced twice for seed 11: once by the
controls runner, once directly — counter is seed-deterministic):

```
seed=10 FAIL C1=unmet cases_ok=49/50 families_failed=A1-auth-status selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery seed=10 tool_rc=1
     miss C006:A1-auth-status:want=dead_auth:got=dead_rate_limit
seed=11 FAIL C1=unmet cases_ok=49/50 families_failed=A2-auth-spelling selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery seed=11 tool_rc=1
     miss C010:A2-auth-spelling:want=dead_auth:got=dead_rate_limit
seed=17 FAIL C1=unmet cases_ok=49/50 families_failed=N3-other-stays selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery seed=17 tool_rc=1
     miss C032:N3-other-stays:want=dead_error_other:got=dead_quota
seed=42 FAIL C1=unmet cases_ok=49/50 families_failed=A2-auth-spelling selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery seed=42 tool_rc=1
     miss C013:A2-auth-spelling:want=dead_auth:got=dead_rate_limit
seed=51 FAIL C1=unmet cases_ok=49/50 families_failed=N3-other-stays selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery seed=51 tool_rc=1
     miss C029:N3-other-stays:want=dead_error_other:got=dead_rate_limit
seed=52 FAIL C1=unmet cases_ok=49/50 families_failed=N3-other-stays selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery seed=52 tool_rc=1
     miss C032:N3-other-stays:want=dead_error_other:got=dead_quota
SWEEP seeds 1..60: failures = 10, 11, 17, 42, 51, 52 → 6/60 (10%); seeds 1..9,12..16,18..41,43..50,53..60 all 50/50.
```
All six failures are 49/50 single-case; families A1-auth-status (1), A2-auth-spelling (2), N3-other-stays (3) —
fixed-template families, not the disclosed composed A4/A5/N5 — with `got=dead_rate_limit` or `got=dead_quota`,
i.e. records where the battery plants an auth/other death but the landed tool sees quota/rate evidence it lets win
(or fires spuriously). Frozen receipt covered only seed 100.

## 4. Controls re-run (mandated: `--rev d1bd1b33… --work $S/ctl --seed 11`)

```
K0 expect=unmet got=unmet AS_EXPECTED | C1=unmet cases_ok=23/50 families_failed=A1-auth-status,A2-auth-spelling,A3-auth-escaped,A4-auth-status-composed,A5-auth-spelling-composed,Z1-zai-unmapped-auth selftest=ok r17gate=ok registry=unmet sourced=unmet checks_failed=battery,registry,sourced seed=11 tool_rc=1
K1 expect=unmet got=unmet AS_EXPECTED | C1=unmet cases_ok=38/50 families_failed=A2-auth-spelling,N3-other-stays,N5-other-composed selftest=rc1 r17gate=rc1 registry=met sourced=met(S637,S638) checks_failed=battery,selftest,r17gate seed=11 tool_rc=1
K2 expect=unmet got=unmet AS_EXPECTED | C1=unmet cases_ok=36/50 families_failed=A2-auth-spelling,A3-auth-escaped,A5-auth-spelling-composed selftest=rc1 r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery,selftest seed=11 tool_rc=1
K3 expect=unmet got=unmet AS_EXPECTED | C1=unmet cases_ok=36/50 families_failed=A1-auth-status,A2-auth-spelling,A4-auth-status-composed,Z1-zai-unmapped-auth selftest=rc1 r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery,selftest seed=11 tool_rc=1
K4 expect=unmet got=unmet AS_EXPECTED | C1=unmet cases_ok=43/50 families_failed=N1-quota-wins,N2-rate-wins selftest=rc1 r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery,selftest seed=11 tool_rc=1
K5 expect=unmet got=unmet AS_EXPECTED | C1=unmet cases_ok=40/50 families_failed=A2-auth-spelling,A3-auth-escaped,A4-auth-status-composed,A5-auth-spelling-composed,Z1-zai-unmapped-auth selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery seed=11 tool_rc=1
K6 expect=unmet got=unmet AS_EXPECTED | C1=unmet cases_ok=49/50 families_failed=A2-auth-spelling selftest=ok r17gate=ok registry=met sourced=unmet checks_failed=battery,sourced seed=11 tool_rc=1
K7 expect=unmet got=unmet AS_EXPECTED | C1=unmet cases_ok=49/50 families_failed=A2-auth-spelling selftest=ok r17gate=rc1 registry=met sourced=met(S637,S638) checks_failed=battery,r17gate seed=11 tool_rc=1
K8 expect=unmet got=unmet AS_EXPECTED | C1=unmet cases_ok=49/50 families_failed=A2-auth-spelling selftest=ok r17gate=ok registry=unmet sourced=met(S637,S638) checks_failed=battery,registry seed=11 tool_rc=1
P1 expect=met got=unmet UNEXPECTED | C1=unmet cases_ok=49/50 families_failed=A2-auth-spelling selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery seed=11 tool_rc=1
K0c expect=unmet got=unmet AS_EXPECTED | C2=unmet stated=58 mismatches=7 uncorrected=7 spurious=0 altered=0 census=ok checks_failed=mismatch base=d1bd1b33
K1c expect=unmet got=unmet AS_EXPECTED | C2=unmet stated=45 mismatches=0 uncorrected=0 spurious=0 altered=5 census=ok checks_failed=altered base=d1bd1b33
K2c expect=unmet got=unmet AS_EXPECTED | C2=unmet stated=58 mismatches=7 uncorrected=7 spurious=0 altered=0 census=ok checks_failed=mismatch base=d1bd1b33
K3c expect=unmet got=unmet AS_EXPECTED | C2=unmet stated=58 mismatches=7 uncorrected=0 spurious=27 altered=0 census=ok checks_failed=spurious base=d1bd1b33
K4c expect=unmet got=unmet AS_EXPECTED | C2=unmet stated=58 mismatches=0 uncorrected=0 spurious=0 altered=5 census=ok checks_failed=altered base=d1bd1b33
K5c expect=unmet got=unmet AS_EXPECTED | C2=unmet stated=58 mismatches=7 uncorrected=6 spurious=2 altered=0 census=ok checks_failed=mismatch,spurious base=d1bd1b33
P2 expect=met got=met AS_EXPECTED | C2=met stated=58 mismatches=7 uncorrected=0 spurious=0 altered=0 census=ok checks_failed=- base=d1bd1b33
CONTROLS_DONE unexpected=1 rev=d1bd1b339b894de0249b0f60702dff9962da88d9 seed=11
exit=1
```
Does NOT end `CONTROLS_DONE unexpected=0`: P1 is UNEXPECTED (candidate battery 49/50 at seed 11 — same failure as
the direct landing seed-11 run above). All C2 controls (K0c–K5c, P2) behave as in the frozen receipt.

## 5. C2 replay (exact match to frozen receipts on all three trees)

```
== C2 entering == C2=unmet stated=58 mismatches=7 uncorrected=7 spurious=0 altered=0 census=ok checks_failed=mismatch base=d1bd1b33 (exit=1)
  uncorrected S581 10->9,15->14
  uncorrected S582 14->13
  uncorrected S583 14->13
  uncorrected S584 17->15,22->26
  uncorrected S634 17->18
== C2 landing == C2=met stated=60 mismatches=7 uncorrected=0 spurious=0 altered=0 census=ok checks_failed=- base=d1bd1b33 (exit=0)
== C2 tip ==     C2=met stated=60 mismatches=7 uncorrected=0 spurious=0 altered=0 census=ok checks_failed=- base=d1bd1b33 (exit=0)
```

## 6. Freeze integrity

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --stat 9579cff6 5e2bcf2 -- .ufo/waves/round-100/count-c1.py .ufo/waves/round-100/count-c2.py .ufo/waves/round-100/contract.md .ufo/waves/round-100/candidate
(empty output, rc=0)  → frozen files untouched between freeze and landing: PASS
tools/mori-seat-terminal.py        candidate↔landing↔tip BYTE_IDENTICAL, sha1 0ca820f7f2fd9501e0df367f775c6d22cb53c550
tools/mori-round17-seat-regressions.py candidate↔landing↔tip BYTE_IDENTICAL, sha1 55d7fcf72df0991d45e221aab30583d2a4f025f2
(candidate blobs read from 9579cff6:.ufo/waves/round-100/candidate/tools/*; landed from 5e2bcf2:tools/*; cmp + sha1sum)
```

## 7. Verdicts

- VERDICT C1 needs-amend: entering and landing reproduce exactly on the mandated seeds (23/50 unmet; 50/50 met incl.
  seed 100), but the landing battery fails 49/50 on seeds 10, 11, 17, 42, 51, 52 (A1-auth-status/A2-auth-spelling/
  N3-other-stays → got=dead_rate_limit|dead_quota), violating the frozen kill rule "any family failing on any seed at
  landing = C1 unmet"; controls at seed 11 end `CONTROLS_DONE unexpected=1` (P1 UNEXPECTED), vs `unexpected=0` in the
  frozen seed-100 receipt.
- VERDICT C2 holds: entering `unmet stated=58 mismatches=7 uncorrected=7`; landing and tip `met stated=60
  uncorrected=0 spurious=0 altered=0 census=ok`; byte-for-byte equal to the frozen receipts.
- Freeze integrity holds: diff --stat empty; both landed tools byte-identical to the freeze candidate.

## 8. Unrun checks

- Controls runner at seed 100 this session: unrun (frozen receipt `evidence/controls-r100.txt` covers seed 100; my
  re-run used the mandated seed 11).
- C1 seeds beyond 1..60 and 100/2026/unseeded draws: unrun.
- Root cause of the six seed failures inside the battery generator vs the tool's quota/rate precedence: not diagnosed
  (detection seat; counter and tool are frozen — never edit).

Scratch `/fast/scratch/hyaku/mori-r100/Mo100ExecReplay` removed. No git/jj mutations, no host changes, no pacman, no
sessions content read (only counts via the frozen counter), no files written outside this report and scratch.
