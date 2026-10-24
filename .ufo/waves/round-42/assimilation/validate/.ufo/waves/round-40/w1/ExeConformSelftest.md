# ExeConformSelftest

## Result
Re-derived `evidence/c10-after-selftest.txt` at the requested scored revision `265a955cc67be4eae97d2dc5a9338a25f31eb29b`. The run printed all 11 expected per-mutation PASS lines and `CONFORM_SELFTEST pass=11 fail=0`; exit status was 0. Measured wall time: **57.371 seconds** (`real 0m57.371s`). The complete output is retained in the evidence receipt.

## Exact commands and outputs

1. `git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD`

   Output: `ede486b7a09afbacfb380d5871c46a8051a6dc2e`.

2. `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 265a955cc67be4eae97d2dc5a9338a25f31eb29b:.ufo/waves/round-40/conform.py | sha256sum && sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/conform.py`

   Output: `5025b9664632d01063c11b4f5dadd4f9a063db66d73315d7ed25db8d90b83aaf  -` and the same digest for the working-tree checker.

3. `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 265a955cc67be4eae97d2dc5a9338a25f31eb29b:.ufo/waves/round-40/count-c8.py | sha256sum && sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/count-c8.py && git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 265a955cc67be4eae97d2dc5a9338a25f31eb29b:.ufo/waves/round-39/contract.md | sha256sum && sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-39/contract.md`

   Output: scorer/worktree counter digests both `4e4d50eb1e96d947f0e9d2ab25a13b2b8c33963f216f3be43060a3348702f6da`; scorer/worktree contract digests both `fc36841bff00e46bf3d2ba662c9e4e13e36577da1d1f2fec41d0bea91f8ebcd3`.

4. Initial timing attempt: `/usr/bin/time -f 'WALL_SECONDS=%e' python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --selftest`

   Output: `error: command not found: /usr/bin/time`; exit 127. Retimed successfully using the shell `time` keyword; no tool was installed.

5. `TIMEFORMAT='WALL_SECONDS=%3R'; time python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --selftest`

   Output:
   ```text
   PASS predicate          predicate token changed -> only predicate failed
   PASS head_pin           pin label renamed -> only head_pin failed
   PASS tool_resolve       relative resolution removed -> only tool_resolve failed
   PASS bounded_reads      git helper run timeout removed -> only bounded_reads failed
   PASS timeout_scope      timeout value replaced with None -> only timeout_scope failed
   PASS timeout_scope_shadow function-local None shadow inserted -> only timeout_scope failed
   PASS drain_bind         communicate drains replaced by wait+read -> only drain_bind failed
   PASS drain_bind_decoy   decoy used communicate beside a wait+read drain -> only drain_bind failed
   PASS timeout_state      budget flag ignored -> only timeout_state failed
   PASS scratch            scratch parent moved off-lane -> only scratch failed
   PASS selftest_conjunct  communicate timeout keyword stripped -> only selftest_conjunct failed
   CONFORM_SELFTEST pass=11 fail=0

   real 0m57.371s
   user 1m55.238s
   sys 0m57.023s
   ```

## Files and boundaries
- Replaced only `.ufo/waves/round-40/evidence/c10-after-selftest.txt` and wrote this exclusive report.
- The working-tree checker and counter hashes match their blobs at the scored revision; the checker uses that revision argument. Current repository HEAD reported above is later than the scored revision.
- No blocker. No tool installation, production-file edit, build, lint, or test beyond the assigned self-test.