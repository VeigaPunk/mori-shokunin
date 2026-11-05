# Mo100MutC1 — mutation probe of the landed C1 auth logic (mori r100, wave w1, attempt 1)

Seat: mutation-tester. Target: `tools/mori-seat-terminal.py` as landed at `5e2bcf2c487e377b51287c587144bdde5b233f8f`,
restricted to the round-100 change surface (AUTH_STATUSES, AUTH_TOKENS/AUTH_TOKEN_BYTES, auth_token window matching,
_auth_evidence, its two call sites and their order, the zai branch, the CLASSES entry). Detector: the frozen counter
`python3 .ufo/waves/round-100/count-c1.py --root MUTANT_TREE --work $S --seed 5` and `--seed 6`, on a
`git archive`-extracted copy of the landing with exactly one single-point edit applied to the tool. No lane file was
modified; all mutants lived in scratch trees under `/fast/scratch/hyaku/mori-r100/Mo100MutC1` (removed after this probe).

## Calibration (pristine, before any mutation)

- landing seed 5, rc=0: `C1=met cases_ok=50/50 families_failed=- selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=- seed=5 tool_rc=1`
- landing seed 6, rc=0: `C1=met cases_ok=50/50 families_failed=- selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=- seed=6 tool_rc=1`
- entering d1bd1b33 seed 5, rc=1: `C1=unmet cases_ok=23/50 families_failed=A1-auth-status,A2-auth-spelling,A3-auth-escaped,A4-auth-status-composed,A5-auth-spelling-composed,Z1-zai-unmapped-auth selftest=ok r17gate=ok registry=unmet sourced=unmet checks_failed=battery,registry,sourced seed=5 tool_rc=1`

All three reproduce the frozen receipts exactly, so a mutant verdict below is attributable to the edit, not detector drift.

## Mutant battery (32 single-point mutants; kill = counter unmet on ≥1 seed, per contract kill rule)

| ID | Single-point mutation (tool sha256 prefix) | Seed 5 counter line (exact) | Seed 6 counter line (exact) | Verdict |
|---|---|---|---|---|
| M01 | AUTH_STATUSES drops 403 (5cb3aa077f67d787) | `C1=unmet cases_ok=44/50 families_failed=A1-auth-status,A4-auth-status-composed selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery seed=5 tool_rc=1` | `C1=unmet cases_ok=43/50 families_failed=A1-auth-status,A4-auth-status-composed selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery seed=6 tool_rc=1` | killed |
| M02 | AUTH_STATUSES drops 401 (72bf07e2df9ae061) | `C1=unmet cases_ok=43/50 families_failed=A1-auth-status,A4-auth-status-composed,Z1-zai-unmapped-auth selftest=rc1 r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery,selftest seed=5 tool_rc=1` | `C1=unmet cases_ok=44/50 families_failed=A1-auth-status,A4-auth-status-composed,Z1-zai-unmapped-auth selftest=rc1 r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery,selftest seed=6 tool_rc=1` | killed |
| M03 | AUTH_STATUSES adds 407 (1131d791972113f1) | `C1=met cases_ok=50/50 families_failed=- selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=- seed=5 tool_rc=1` | `C1=met cases_ok=50/50 families_failed=- selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=- seed=6 tool_rc=1` | survived → G1 |
| M04 | AUTH_STATUSES widened 400/401/403/404/429 (be0ab58af90dc7cc) | `C1=unmet cases_ok=48/50 families_failed=N3-other-stays,N5-other-composed selftest=rc1 r17gate=rc1 registry=met sourced=met(S637,S638) checks_failed=battery,selftest,r17gate seed=5 tool_rc=1` | `C1=unmet cases_ok=48/50 families_failed=N5-other-composed selftest=rc1 r17gate=rc1 registry=met sourced=met(S637,S638) checks_failed=battery,selftest,r17gate seed=6 tool_rc=1` | killed |
| M05 | AUTH_STATUSES emptied (e0662d851fcda8f6) | `C1=unmet cases_ok=37/50 families_failed=A1-auth-status,A4-auth-status-composed,Z1-zai-unmapped-auth selftest=rc1 r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery,selftest seed=5 tool_rc=1` | `C1=unmet cases_ok=37/50 families_failed=A1-auth-status,A4-auth-status-composed,Z1-zai-unmapped-auth selftest=rc1 r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery,selftest seed=6 tool_rc=1` | killed |
| M06 | AUTH_TOKENS drops permission_denied (67f179c5c5f5612c) | `C1=unmet cases_ok=48/50 families_failed=A2-auth-spelling selftest=rc1 r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery,selftest seed=5 tool_rc=1` | `C1=unmet cases_ok=49/50 families_failed=A2-auth-spelling selftest=rc1 r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery,selftest seed=6 tool_rc=1` | killed |
| M07 | AUTH_TOKENS drops unauthenticated (0b97002e5be94a81) | `C1=unmet cases_ok=44/50 families_failed=A2-auth-spelling,A3-auth-escaped,A5-auth-spelling-composed selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery seed=5 tool_rc=1` | `C1=unmet cases_ok=48/50 families_failed=A2-auth-spelling,A3-auth-escaped selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery seed=6 tool_rc=1` | killed |
| M08 | AUTH_TOKENS drops PERMISSION_DENIED (02c4bab52108f9bd) | `C1=unmet cases_ok=49/50 families_failed=A2-auth-spelling selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery seed=5 tool_rc=1` | `C1=unmet cases_ok=47/50 families_failed=A2-auth-spelling,A5-auth-spelling-composed selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery seed=6 tool_rc=1` | killed |
| M09 | AUTH_TOKENS drops authentication_error (f463fe9d38d9c34a) | `C1=met cases_ok=50/50 families_failed=- selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=- seed=5 tool_rc=1` | `C1=unmet cases_ok=47/50 families_failed=A2-auth-spelling selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery seed=6 tool_rc=1` | killed (seed 6; survives seed 5 — seed-sensitive family draw) |
| M10 | AUTH_TOKENS drops permission_error (0497b3f4ebb9b20b) | `C1=unmet cases_ok=46/50 families_failed=A2-auth-spelling,A3-auth-escaped selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery seed=5 tool_rc=1` | `C1=unmet cases_ok=47/50 families_failed=A2-auth-spelling,A3-auth-escaped,A5-auth-spelling-composed selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery seed=6 tool_rc=1` | killed |
| M11 | AUTH_TOKENS adds plain word `denied` (0da25e47d8d15ebb) | `C1=unmet cases_ok=49/50 families_failed=N3-other-stays selftest=rc1 r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery,selftest seed=5 tool_rc=1` | `C1=unmet cases_ok=48/50 families_failed=N3-other-stays,N5-other-composed selftest=rc1 r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery,selftest seed=6 tool_rc=1` | killed |
| M12 | AUTH_TOKENS adds `not_authorized` (85d31820d8512aad) | `C1=met cases_ok=50/50 families_failed=- … checks_failed=- seed=5 tool_rc=1` | `C1=met cases_ok=50/50 families_failed=- … checks_failed=- seed=6 tool_rc=1` | survived → G2 |
| M13 | AUTH_TOKENS adds `unauthorized` (91df2c5933e96f41) | `C1=met cases_ok=50/50 families_failed=- … checks_failed=- seed=5 tool_rc=1` | `C1=met cases_ok=50/50 families_failed=- … checks_failed=- seed=6 tool_rc=1` | survived → G3 |
| M14 | auth window match `window.lower().endswith(token)` (33f904bb53e84a04) | `C1=met cases_ok=50/50 families_failed=- … checks_failed=- seed=5 tool_rc=1` | `C1=met cases_ok=50/50 families_failed=- … checks_failed=- seed=6 tool_rc=1` | survived → G4 |
| M15 | AUTH_TOKEN_BYTES emptied (263e779e5ddc50b2) | `C1=unmet cases_ok=36/50 families_failed=A2-auth-spelling,A3-auth-escaped,A5-auth-spelling-composed selftest=rc1 r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery,selftest seed=5 tool_rc=1` | `C1=unmet cases_ok=36/50 families_failed=A2-auth-spelling,A3-auth-escaped,A5-auth-spelling-composed selftest=rc1 r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery,selftest seed=6 tool_rc=1` | killed |
| M16 | scanner init `auth_token = True` (78092e967b9c1ee2) | `C1=unmet cases_ok=39/50 families_failed=N3-other-stays,N5-other-composed selftest=rc1 r17gate=rc1 registry=met sourced=met(S637,S638) checks_failed=battery,selftest,r17gate seed=5 tool_rc=1` | `C1=unmet cases_ok=39/50 families_failed=N3-other-stays,N5-other-composed selftest=rc1 r17gate=rc1 registry=met sourced=met(S637,S638) checks_failed=battery,selftest,r17gate seed=6 tool_rc=1` | killed |
| M17 | guard `if not auth_token` → `if auth_token` (e86c22fb586c735a) | `C1=unmet cases_ok=36/50 families_failed=A2-auth-spelling,A3-auth-escaped,A5-auth-spelling-composed selftest=rc1 r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery,selftest seed=5 tool_rc=1` | `C1=unmet cases_ok=36/50 families_failed=A2-auth-spelling,A3-auth-escaped,A5-auth-spelling-composed selftest=rc1 r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery,selftest seed=6 tool_rc=1` | killed |
| M18 | drop `break` after `auth_token = True` (0bdc25e3707057d3) | `C1=met cases_ok=50/50 families_failed=- … checks_failed=- seed=5 tool_rc=1` | `C1=met cases_ok=50/50 families_failed=- … checks_failed=- seed=6 tool_rc=1` | survived — equivalent mutant (proof below) |
| M19 | auth match endswith → startswith (4d801a2d44f1771b) | `C1=unmet cases_ok=39/50 families_failed=A2-auth-spelling,A3-auth-escaped,A5-auth-spelling-composed selftest=rc1 r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery,selftest seed=5 tool_rc=1` | `C1=unmet cases_ok=40/50 families_failed=A2-auth-spelling,A3-auth-escaped,A5-auth-spelling-composed selftest=rc1 r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery,selftest seed=6 tool_rc=1` | killed |
| M20 | metadata return `"auth_token": False` (df5bb4ac5e87b58c) | `C1=unmet cases_ok=36/50 families_failed=A2-auth-spelling,A3-auth-escaped,A5-auth-spelling-composed selftest=rc1 r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery,selftest seed=5 tool_rc=1` | `C1=unmet cases_ok=36/50 … checks_failed=battery,selftest seed=6 tool_rc=1` | killed |
| M21 | view init `"auth_token": True` (d7a3e250444f9831) | `C1=met cases_ok=50/50 families_failed=- … checks_failed=- seed=5 tool_rc=1` | `C1=met cases_ok=50/50 families_failed=- … checks_failed=- seed=6 tool_rc=1` | survived → G5 |
| M22 | projector drops `view["auth_token"]` copy (18ec524f2ef3943e) | `C1=unmet cases_ok=36/50 … selftest=rc1 … checks_failed=battery,selftest seed=5 tool_rc=1` | `C1=unmet cases_ok=36/50 … selftest=rc1 … checks_failed=battery,selftest seed=6 tool_rc=1` | killed |
| M23 | `_auth_evidence` or → and (affb7825e9290ad3) | `C1=unmet cases_ok=23/50 families_failed=A1-auth-status,A2-auth-spelling,A3-auth-escaped,A4-auth-status-composed,A5-auth-spelling-composed,Z1-zai-unmapped-auth selftest=rc1 … checks_failed=battery,selftest seed=5 tool_rc=1` | same shape, `seed=6` | killed |
| M24 | `_auth_evidence` in → not in (7d9434727f951ab9) | `C1=unmet cases_ok=26/50 families_failed=A1-auth-status,A4-auth-status-composed,N3-other-stays,N5-other-composed,Z1-zai-unmapped-auth selftest=rc1 r17gate=rc1 … checks_failed=battery,selftest,r17gate seed=5 tool_rc=1` | same shape, `seed=6` | killed |
| M25 | `_auth_evidence` drops token clause (6cda4e4fe2cc3a8d) | `C1=unmet cases_ok=36/50 … selftest=rc1 … checks_failed=battery,selftest seed=5 tool_rc=1` | `C1=unmet cases_ok=36/50 … selftest=rc1 … checks_failed=battery,selftest seed=6 tool_rc=1` | killed |
| M26 | zai-branch call site deleted (4c0704b3244ebe1b) | `C1=unmet cases_ok=49/50 families_failed=Z1-zai-unmapped-auth selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery seed=5 tool_rc=1` | same shape, `seed=6` | killed (deterministic, 1 case) |
| M27 | non-zai call site deleted (ed5efabb3288e24c) | `C1=unmet cases_ok=24/50 families_failed=A1-auth-status,A2-auth-spelling,A3-auth-escaped,A4-auth-status-composed,A5-auth-spelling-composed selftest=rc1 … checks_failed=battery,selftest seed=5 tool_rc=1` | same shape, `seed=6` | killed |
| M28 | zai call site moved above Z.AI code checks (0711b03da1e93923) | `C1=unmet cases_ok=48/50 families_failed=Z1-zai-quota-code,Z1-zai-rate-code selftest=ok … checks_failed=battery seed=5 tool_rc=1` | same shape, `seed=6` | killed |
| M29 | non-zai call site moved above quota check (97f1ef68c466f9ee) | `C1=unmet cases_ok=43/50 families_failed=N1-quota-wins,N2-rate-wins selftest=rc1 … checks_failed=battery,selftest seed=5 tool_rc=1` | same shape, `seed=6` | killed |
| M30 | non-zai call site moved between quota and rate (644e82ceaa810a04) | `C1=unmet cases_ok=47/50 families_failed=N2-rate-wins selftest=ok … checks_failed=battery seed=5 tool_rc=1` | same shape, `seed=6` | killed |
| M31 | CLASSES entry `dead_auth` deleted (7ad1b58e13c04697) | `C1=unmet cases_ok=0/50 families_failed=<all 15> selftest=rc1 r17gate=rc1 … checks_failed=battery,selftest,r17gate seed=5 tool_rc=2` | same shape, `seed=6` | killed (tool crashes: emitted class outside CLASSES) |
| M32 | zai return label `dead_auth`→`dead_authz` (59bb756b795edff7) | `C1=unmet cases_ok=0/50 families_failed=<all 15> selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=battery seed=5 tool_rc=2` | same shape, `seed=6` | killed (same crash path, battery-only) |

Tally: 25 killed on both seeds; M09 killed on seed 6 only (still killed under the contract kill rule "any family failing
on any seed"); 6 survivors: M03, M12, M13, M14, M21 (battery gaps, below) and M18 (equivalent).

## Survivors — distinguishing records (single-seat probes, pristine vs mutant tool, `--now-ms 1793000000000`)

Each record is an aged (3600 s) assistant `error` seat; classes read from the tool's JSON output.

- **G1 (M03, status over-match)** — `errorStatus=407`, `errorMessage="407 Proxy Authentication Required"`:
  pristine `dead_error_other` → mutant `dead_auth`. Battery gap: no case pins a non-401/403 auth-flavored 4xx status.
- **G2 (M12, token over-match)** — `errorMessage="not_authorized: subscription does not include this model"`, no status:
  pristine `dead_error_other` → mutant `dead_auth`. Gap: no negative-control spelling outside the six frozen tokens.
- **G3 (M13, token over-match)** — `errorMessage="unauthorized client rejected by provider policy"`, no status:
  pristine `dead_error_other` → mutant `dead_auth`. Gap: same family as G2.
- **G4 (M14, case-insensitive over-match)** — `errorMessage="Permission_Denied: seat lacks model access"`, no status:
  pristine `dead_error_other` → mutant `dead_auth`. Gap: no mixed-case spelling negative control.
- **G5 (M21, view-default leak)** — `errorStatus=500`, **no errorMessage** member at all:
  pristine `dead_error_other` → mutant `dead_auth`. Gap: no battery case reaches the dead path without `errorMessage`,
  so the view-default value of `auth_token` is unobserved.
- **M18 (drop break) — proof of equivalence, not a gap.** `auth_token` is monotone: once True, the `if not auth_token`
  guard stops all further matching, and the loop body has no other side effect, so scanning remaining tokens after a
  match cannot change any observable value. Empirical: battery met on both seeds; probes EQ1
  (`"stream error unauthenticated: PERMISSION_DENIED repeated thrice"`), EQ2 (`"PERMISSION_DENIED: caller lacks access to model"`),
  EQ3 (`"please retry permission_denied or unauthenticated later"`) all classify identically in pristine and mutant
  (`dead_auth`); G1–G5 all identical (`dead_error_other`).

Per-seat rules: these are coverage findings on the battery generator, not contract amendments — the frozen predicate P1
is met by the landing and none of the survivors makes it lie about what it checks. M09's one-seed survival shows the
A2/A5 template draws are seed-sensitive for rare tokens (`authentication_error` appears in 1 of 7 A2 templates and 1 of 6
A5 spellings); the two-seed measurement required by the contract is what catches it.

## Integrity / restoration evidence

- Pristine landing tool sha256 before probe: `a7ff6fb67a4c2378171c676adc2dd948baa7074421a56a6ba2282dbe402169e7`;
  after probe (scratch copy and lane file): identical.
- Lane repo after probe: `git rev-parse HEAD` = `5e2bcf2c487e377b51287c587144bdde5b233f8f`;
  `git status --porcelain -- tools/` = empty. All 32 mutant tool sha256s listed in the table differ from pristine;
  mutant trees existed only in scratch and were deleted after measurement.
- Scratch dir `/fast/scratch/hyaku/mori-r100/Mo100MutC1` removed at seat completion.

## Unrun checks

- `count-c2.py` (C2 axis): not run — outside this seat's mutation target.
- Mutants outside the named round-100 surface (scanner internals shared with quota/rate, r17 gate internals): not generated.
- Surviving-mutant probes beyond the 8 records above: not run.

VERDICT C1 holds: landing meets the frozen P1 on seeds 5 and 6 and entering fails it; the 32-mutant probe finds 26 killed
(incl. one seed-sensitive) and 5 battery gaps (G1–G5) plus one equivalent mutant — coverage observations for the next
battery, not falsifications of the claim.
