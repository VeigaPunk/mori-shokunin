# Fabricated-binding control

## Axes
- R37 token-control acceptance: **C2=met** (required).
- R38 content-binding rejection: **C4=unmet** (required).

## Commands and retained evidence

Sandbox build:
```text
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-38/fixtures/make-witness-sandbox.py f725f3076972e6e70595b5ac8279be524a111ff8 --out /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-38/scratch/ExecWitnessSandbox/fabricated-binding
```
Output: sandbox commit `d2ee0532b716b963623fb421aaa571c54c754aad`; sandbox path `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-38/scratch/ExecWitnessSandbox/fabricated-binding`.

R37 counter:
```text
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-37/count-c2.py d2ee0532b716b963623fb421aaa571c54c754aad --repo /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-38/scratch/ExecWitnessSandbox/fabricated-binding
```
Retained output: all eight checks passed (`tool_present`, `selftest`, `cap_kill`, `redirect_kill`, `knowledge`, `capability`, `readme`, `live`); terminal verdict `C2=met`.

R38 counter:
```text
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-38/count-c4.py d2ee0532b716b963623fb421aaa571c54c754aad --repo /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-38/scratch/ExecWitnessSandbox/fabricated-binding
```
Retained output: all three fabricated witnesses rejected; `anchors` PASS (`anchors=3 missing=[]`); `capability` FAIL because `evidence/no-such-receipt.txt` is missing; `live_rows` FAIL (`named=0 summary_drifted=10`); `named_row_drift` PASS (`row_states=PASS`); `drift_kill` PASS (mutated `row_states=FAIL`, including S103). Terminal verdict: `C4=unmet`.

## Files, behavior, risks, blockers
- File written: `.ufo/waves/round-38/w1/ExecWitnessSandbox.md` only. No lane implementation files changed.
- The fabricated token witnesses satisfy the R37 counter but fail R38's content-binding requirements, as expected by the requested control.
- No blocker. No tool installs or other checks were performed.
