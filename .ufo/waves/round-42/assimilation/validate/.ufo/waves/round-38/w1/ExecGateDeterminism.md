# ExecGateDeterminism

## Runs and retained output

Captured combined stdout/stderr and exit status for each invocation under `.ufo/waves/round-38/scratch/ExecGateDeterminism/`:

- `python3 tools/mori-sources-appendonly.py --selftest` ran three times. Each exited `0` (`selftest-1.status:1`, `selftest-2.status:1`, `selftest-3.status:1`) and printed exactly:
  `MORI_SOURCES_APPENDONLY_SELFTEST pass=9 fail=0`
  (retained in `selftest-1.txt:1`, `selftest-2.txt:1`, `selftest-3.txt:1`).
- `python3 tools/mori-sources-appendonly.py daa1d4d2501e1671e7b7ff1fd60a069564f178b0` ran twice. Both exited `1` (`gate-1.status:1`, `gate-2.status:1`). The captured outputs are `gate-1.txt` and `gate-2.txt`; each reports `appendonly_violations=18` and ends with `supersede_timing ... stale_supersede=[]` (`gate-1.txt:20-21`, `gate-2.txt:20-21`).

## Byte comparisons

Used `cmp -s` on the captured outputs:

- Selftest 1 vs 2: byte-identical; `cmp` exit `0`.
- Selftest 1 vs 3: byte-identical; `cmp` exit `0`.
- Selftest 2 vs 3: byte-identical; `cmp` exit `0`.
- Gate 1 vs 2: byte-identical; `cmp` exit `0`.

No output differences were observed; the nondeterminism failure criterion was not triggered.

## Risks and blockers

The two gate commands returned status `1` even though their captured output matched byte-for-byte. Their output reports 18 append-only violations for the pinned revision; this is recorded as gate behavior, not treated as a determinism failure. No blocker to this comparison task.
