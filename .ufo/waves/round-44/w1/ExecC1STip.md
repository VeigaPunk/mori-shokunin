# ExecC1STip — round-43 routed defect 5: C1S receipt measured at the round-44 tip

Seat: `L1Mori44-4.ExecC1STip` (leaf executor, wave 1). Read-only run at the round-44
tip; nothing edited except this report. No tool installed or upgraded.

- Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin`
- Measured revision (lane branch `master`, `HEAD`): `7cb59c6891d4f5d0266fe062565f094da835dc84`
- Round-43 receipt under review: `.ufo/waves/round-43/evidence/c1s-after.txt`
  (measured at `dde525ea4a7fca365e8ff2f3c486bccf28b94e52`)
- Defect text being closed (`corpus/lessons/round-43-verifier-spotcheck.md:217-219`):
  "C1S's receipt is measured at `dde525ea`, while the report's verdict says 'at
  the landed tip'; the tip equivalence rests on the documented identical counter
  sha256. A tip-run receipt would close the gap."

## 1. The run

Executed with cwd = the lane repo (read-only; the counter only writes to `/tmp`
sandboxes it creates itself):

```
python3 .ufo/waves/round-43/count-c1s.py $(git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse master)
```

Full output (14 `check` lines, then the verdict line; shell exit status 0):

```
check self_at_rev            PASS (match)
check frozen_sha             PASS (105ce075f331)
check frozen_sig             PASS (run params argv, timeout)
check v5_present             PASS (.ufo/waves/round-42/conform.py)
check sandbox_clone          PASS
check noharm_cwd             PASS (rc=0 MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0)
check v5_selftest_17         PASS (pass=17 fail=0 rc=0)
check mutant_present_walrus-branch PASS (.ufo/waves/round-42/fixtures/mutants/conform-mut-walrus-branch.py)
check mutant_kill_walrus-branch PASS (pass=16 fail=1 fails=['timeout_scope_walrus_positive'])
check mutant_present_tuple-extract PASS (.ufo/waves/round-42/fixtures/mutants/conform-mut-tuple-extract.py)
check mutant_kill_tuple-extract PASS (pass=16 fail=1 fails=['timeout_scope_tupleunpack_positive'])
check mutant_present_sort-deletion PASS (.ufo/waves/round-42/fixtures/mutants/conform-mut-sort-deletion.py)
check mutant_kill_sort-deletion PASS (pass=16 fail=1 fails=['timeout_scope_source_order'])
check frozen_still_crashes   PASS (rc=1 crash=True C1_line=False)
C1S=met
```

Wall time `11m17.357s` (`real`; `user 6m46.600s`, `sys 3m14.911s`) under a
loaded host, exit `0`. The 14 `check` lines are the same set, in the same order,
as the `dde525ea` receipt (`.ufo/waves/round-43/evidence/c1s-after.txt` also
carries 14 `check` lines) — the round-43 report's "15 checks" is the count slip
already routed as defect 3, and this tip run reproduces 14.

### Answers to the three questions

1. **Does it print `C1S=met exit 0`?** Yes. Last line `C1S=met`, process exit
   status `0`, all 14 checks PASS. Nothing prints `unmet` or `FAIL`.

2. **Does its `self_at_rev` check still PASS at the new tip?** Yes —
   `check self_at_rev            PASS (match)`. The check compares the running
   file's bytes with `<rev>:.ufo/waves/round-43/count-c1s.py`. Both revs carry the
   same blob, and it equals the worktree bytes:

   ```
   dde525ea count-c1s blob aa23fd090f5a4a8bef42e36d6e676ec314c62bd3 sha256 93482248b46def2a2cec7238732af1551ef315517e76833c3843875313b65dc5
   master   count-c1s blob aa23fd090f5a4a8bef42e36d6e676ec314c62bd3 sha256 93482248b46def2a2cec7238732af1551ef315517e76833c3843875313b65dc5
   worktree sha256 93482248b46def2a2cec7238732af1551ef315517e76833c3843875313b65dc5
   ```

   So the counter scored at the tip is the same instrument, byte for byte, as the
   one the round-43 receipt scored.

3. **Does anything in the round-43/44 tree make the frozen r42 counter behave
   differently?** No. The frozen counter
   `.ufo/waves/round-42/count-c1.py` is the same blob at both revs
   (`a23160f13f76…`, sha256 `105ce075f33120837ba5a49a1ad4f23a3dd7dc17fea506ab917140bc7f2053f6`),
   and every path it reads is byte-identical at `dde525ea` and `master`
   (blob-object comparison, `git rev-parse <rev>:<path>`):

   ```
   SAME a23160f13f76  .ufo/waves/round-42/count-c1.py
   SAME 8add90f0c0a3  .ufo/waves/round-42/conform.py
   SAME 3b67d958c338  .ufo/waves/round-41/conform.py
   SAME 17e32ad214f0  .ufo/waves/round-41/fixtures/c1/count-c8.py
   SAME 16ac973ce919  .ufo/waves/round-39/contract.md
   SAME 1ffbd001d691  .ufo/waves/round-42/evidence/freeze-r42.txt
   SAME 887fd85d96fd  tools/mori-sources-appendonly.py
   SAME ede8a79247be  .ufo/waves/round-41/fixtures/c1/survivor-walrus-none.py
   SAME 2d60565e6716  .ufo/waves/round-41/fixtures/c1/survivor-tupleunpack-none.py
   SAME 954a4610c4de  .ufo/waves/round-41/fixtures/c1/survivor-deadloop-rebind.py
   SAME 3d8964002ae0  .ufo/waves/round-42/fixtures/mutants/conform-mut-walrus-branch.py
   SAME d8340249b826  .ufo/waves/round-42/fixtures/mutants/conform-mut-tuple-extract.py
   SAME eaa86468f03c  .ufo/waves/round-42/fixtures/mutants/conform-mut-sort-deletion.py
   ```

   All 19 paths named in `.ufo/waves/round-42/evidence/freeze-r42.txt` also
   compare SAME across the two revs (checked the same way, one line per pin).
   The round-43/44 additions are additive and unread by the frozen counter:
   `git diff --stat dde525ea..master` = `110 files +16130 -0`, and the only
   non-additive edits are `LOG.md`, `SCORECARD.md`, `SKILL.md` (+4 round-44 gate
   rows), `corpus/QUALITY.md`, `corpus/lessons/round-43.md` — none of which the
   frozen counter opens. The tip run's own arm confirms the unchanged behaviour:
   `check frozen_still_crashes   PASS (rc=1 crash=True C1_line=False)` at
   `7cb59c68`, i.e. the frozen counter still exits non-zero with
   `TypeError: run() got unexpected keyword argument 'cwd'` and prints no `C1=`
   line, exactly as the `dde525ea` receipt recorded. The `cwd` keyword is bound
   at the call site, so the crash is independent of tree content beyond the
   pinned inputs above.

   Scope note: the measurement is at commit `7cb59c68`, not at the dirty
   worktree. At run time the worktree carried sibling seats' in-flight edits
   (`M LOG.md SCORECARD.md corpus/QUALITY.md corpus/README.md corpus/SOURCES.md
   corpus/lessons/round-43.md`, `?? corpus/knowledge/pid-probe-conclusion-r44.md`,
   `?? .ufo/waves/round-44/w1-spec.json`, `?? .ufo/waves/round-44/w1/`). The
   counter reads committed bytes (`git show <rev>:<path>` and a `--shared`
   clone checked out at `<rev>`), and no frozen instrument appears in that
   dirty list.

## 2. Committable receipt — `.ufo/waves/round-44/evidence/c1s-tip-run.txt`

Integration owner: commit the block below verbatim as
`.ufo/waves/round-44/evidence/c1s-tip-run.txt`. Nothing in the round-43 counter
or its evidence was touched.

```
# C1S at the round-44 tip — closes round-43 routed defect 5
# rev: 7cb59c6891d4f5d0266fe062565f094da835dc84 (lane branch master, HEAD)
# command: python3 .ufo/waves/round-43/count-c1s.py $(git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse master)
# cwd: /home/vgpnk/Projects/shokunin/mori-shokunin
# when: 2026-10-25T05:20:19-03:00 (run completed; wall time 11m17.357s)
# counter sha256: 93482248b46def2a2cec7238732af1551ef315517e76833c3843875313b65dc5
# frozen r42 counter sha256: 105ce075f33120837ba5a49a1ad4f23a3dd7dc17fea506ab917140bc7f2053f6
# exit: 0
check self_at_rev            PASS (match)
check frozen_sha             PASS (105ce075f331)
check frozen_sig             PASS (run params argv, timeout)
check v5_present             PASS (.ufo/waves/round-42/conform.py)
check sandbox_clone          PASS
check noharm_cwd             PASS (rc=0 MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0)
check v5_selftest_17         PASS (pass=17 fail=0 rc=0)
check mutant_present_walrus-branch PASS (.ufo/waves/round-42/fixtures/mutants/conform-mut-walrus-branch.py)
check mutant_kill_walrus-branch PASS (pass=16 fail=1 fails=['timeout_scope_walrus_positive'])
check mutant_present_tuple-extract PASS (.ufo/waves/round-42/fixtures/mutants/conform-mut-tuple-extract.py)
check mutant_kill_tuple-extract PASS (pass=16 fail=1 fails=['timeout_scope_tupleunpack_positive'])
check mutant_present_sort-deletion PASS (.ufo/waves/round-42/fixtures/mutants/conform-mut-sort-deletion.py)
check mutant_kill_sort-deletion PASS (pass=16 fail=1 fails=['timeout_scope_source_order'])
check frozen_still_crashes   PASS (rc=1 crash=True C1_line=False)
C1S=met
```

Shell timing lines from the same run, for completeness (stderr, not counter
output): `real 11m17.357s`, `user 6m46.600s`, `sys 3m14.911s`.

## 3. What this does and does not establish

- Establishes: `C1S=met` exit 0 is reproducible at the landed round-44 tip
  `7cb59c68` with the same counter bytes that produced the `dde525ea` receipt;
  `self_at_rev` matches at the tip; the frozen r42 counter's behaviour is
  unchanged because all of its inputs are unchanged.
- Does not establish: tamper-evidence. The round-43 mutant battery
  (`evidence/c1s-mutants.txt`) already recorded four SURVIVED classes against
  this counter; a tip run inherits that limitation unchanged, since the counter
  bytes are identical.

## 4. Files changed / installs

- Written: this report only
  (`.ufo/waves/round-44/w1/ExecC1STip.md`). No evidence file, no instrument, no
  counter, no round-43 artifact edited; no git write command run.
- Tools installed or upgraded: none.
- Scratch: the counter's own `/tmp/mori-r43-c1s-*` sandboxes (outside the repo).

## 5. Risks / blockers

- None blocking. Residual, unchanged from round 43: the successor counter is not
  tamper-evident (routed to round 44 as a check-name/count guard, i.e. the C2
  gate work); the "15 checks" figure in the round-43 report is 14 and stays a
  routed count slip (defect 3) — this receipt deliberately states 14.
- The receipt is text for an integration owner to commit; it is not committed by
  this seat (lane bounds: no `git add`/`commit`).
