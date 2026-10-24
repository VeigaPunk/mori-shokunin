# ExeSurvivorSweep

## Commands and result

Ran each command below independently. In all ten runs the checker printed `CONFORM=unmet`; the shell reported exit code 1. The long `P-C10:` banner was the same in every run. Every named check not listed as failing in the table passed.

```text
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --counter /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/fixtures/generated/survivor-underscore.py
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --counter /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/fixtures/generated/survivor-tuple.py
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --counter /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/fixtures/generated/survivor-shadow-none.py
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --counter /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/fixtures/generated/survivor-shadow-neg.py
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --counter /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/fixtures/generated/survivor-second-popen.py
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --counter /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/fixtures/generated/survivor-inf.py
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --counter /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/fixtures/generated/survivor-divzero.py
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --counter /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/fixtures/generated/survivor-decoy.py
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --counter /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/fixtures/generated/survivor-cond.py
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --counter /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/fixtures/generated/survivor-barecomm.py
```

| Fixture | Exact failed check output(s) | Final output / process exit |
|---|---|---|
| `survivor-underscore.py` | `drain_bind FAIL (survivor-underscore.py: violations=['Popen at line 143 not drained by a bound, consumed communicate in its function'])` | `CONFORM=unmet`; 1 |
| `survivor-tuple.py` | `drain_bind FAIL (survivor-tuple.py: violations=['Popen at line 143 not drained by a bound, consumed communicate in its function'])` | `CONFORM=unmet`; 1 |
| `survivor-shadow-none.py` | `timeout_scope FAIL (survivor-shadow-none.py: bounded=[] value=['line 115 (communicate): non-numeric constant'])` | `CONFORM=unmet`; 1 |
| `survivor-shadow-neg.py` | `timeout_scope FAIL (survivor-shadow-neg.py: bounded=[] value=['line 115 (communicate): timeout value -1 is not positive'])` | `CONFORM=unmet`; 1 |
| `survivor-second-popen.py` | `drain_bind FAIL (survivor-second-popen.py: violations=['Popen at line 143 not drained by a bound, consumed communicate in its function'])` | `CONFORM=unmet`; 1 |
| `survivor-inf.py` | `timeout_scope FAIL (survivor-inf.py: bounded=[] value=['line 114 (communicate): timeout value inf is not finite'])` | `CONFORM=unmet`; 1 |
| `survivor-divzero.py` | `predicate FAIL (exit=1 equal=False)`; `head_pin FAIL (pin=None tip=ede486b7a09afbacfb380d5871c46a8051a6dc2e)`; `tool_resolve FAIL (exit=1 resolved=)`; `timeout_scope FAIL (survivor-divzero.py: bounded=[] value=['line 114 (communicate): fold error: division by zero'])`; `timeout_state FAIL (exit=1 timeout_reason=False pass=False)` | `CONFORM=unmet`; 1 |
| `survivor-decoy.py` | `drain_bind FAIL (survivor-decoy.py: violations=['Popen at line 143 not drained by a bound, consumed communicate in its function'])` | `CONFORM=unmet`; 1 |
| `survivor-cond.py` | `timeout_scope FAIL (survivor-cond.py: bounded=[] value=['line 116 (communicate): non-numeric constant'])` | `CONFORM=unmet`; 1 |
| `survivor-barecomm.py` | `drain_bind FAIL (survivor-barecomm.py: violations=['Popen at line 143 not drained by a bound, consumed communicate in its function'])`; `timeout_state FAIL (exit=None timeout_reason=False pass=False)`; `selftest_conjunct FAIL (survivor-barecomm.py: honest_comm=['communicate without timeout at line 147'] strips=5 detected=5 anchor=True entry_live=True)` | `CONFORM=unmet`; 1 |

## P-C10 comparison and caveat

The nine survivors explicitly enumerated in contract.md §C1 map as predicted: `shadow-none`, `shadow-neg`, `cond`, `inf`, and `divzero` fail `timeout_scope`; `decoy`, `underscore`, `second-popen`, and `tuple` fail `drain_bind`. The divzero fixture additionally fails `predicate`, `head_pin`, `tool_resolve`, and `timeout_state`; the committed `evidence/c10-after-divzero.txt` records the same pattern (there, `tip=265a955cc67be4eae97d2dc5a9338a25f31eb29b`).

The tenth generated fixture, `survivor-barecomm.py`, also fails `drain_bind`; its missing communicate timeout is additionally caught by `selftest_conjunct`, as P-C10 specifies. It also fails `timeout_state`. Thus all ten are unmet/exit 1, including the contract's explicitly named nine and the extra generated survivor.

Caveat: each run's passing `head_pin` output (except divzero, whose import-time fold error prevents obtaining a pin) reported `pin=ede486b7a09afbacfb380d5871c46a8051a6dc2e tip=ede486b7a09afbacfb380d5871c46a8051a6dc2e`, while the command argument was the scored revision `265a955cc67be4eae97d2dc5a9338a25f31eb29b`. This records the lane checkout HEAD observed during this run, not a mismatch in the supplied revision argument. No production files were changed; this report is the sole artifact written.
