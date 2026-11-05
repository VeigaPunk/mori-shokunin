# Mo98ExecReplay — counter replay + controls re-run (mori r98 w1)

Seat: executor, replay only. Scratch: /fast/scratch/hyaku/mori-r98/Mo98ExecReplay (removed at finish). No lane file outside this report touched; no mutating git/jj command run; no sudo, no sysctl change. Master tip at replay time: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse master` → `379a2f616c146f29341987e73b2828a0ce728ce2` (note: master tip has advanced past landing `600deb7ed2695f54b289cf5b6c3931e0fa9c8bb3`; both are C1/C2 met, see §2/§3).

## 1. Instrument hash verification

`sha256sum .ufo/waves/round-98/count-c1.py .ufo/waves/round-98/count-c2.py`:
```
a9f140bdd53ae0a17da3bd4549d6db6cb2db68298cd97cc73f51db0e8a152e44  .ufo/waves/round-98/count-c1.py
d6fe755fff2e2805c6550ff9bfe0b53c369d5dd8c9799fe4e02bd1e5e73c01fd  .ufo/waves/round-98/count-c2.py
```
CONTROLS_HEADER (committed, evidence/controls-r98.txt line 1):
```
CONTROLS_HEADER entering=b2a67ce562bbf2f0cc73f47d8e79f792badf5e63 count-c1.py=a9f140bdd53ae0a17da3bd4549d6db6cb2db68298cd97cc73f51db0e8a152e44 count-c2.py=d6fe755fff2e2805c6550ff9bfe0b53c369d5dd8c9799fe4e02bd1e5e73c01fd candidate-tool=5ab134ee036f83851eb98a9027db699a5800130c5c13598cb37aeb2abe452db2 date=2026-11-05T21:30:07Z
```
VERDICT-HASH: both counters match the frozen header exactly. (Incidental: the live controls run reprinted the same header with the same `candidate-tool=5ab134ee…` hash; only the timestamp moved to 21:36:26Z.)

## 2. Counter replay — 4 revisions × 2 counters (exact output lines, exit codes in `rc_*`)

Command shape per rev: `git -C <lane> archive <rev> | tar -x -C $S/<rev>` then `count-c1.py --root $S/<rev> --work $S`, `count-c2.py <rev> --work $S`.

**entering b2a67ce562bbf2f0cc73f47d8e79f792badf5e63**
```
C1=unmet cases_ok=0/15 selftest=absent live=absent registry=met sourced=unmet province=unmet checks_failed=selftest,live,sourced,province root=/fast/scratch/hyaku/mori-r98/Mo98ExecReplay/b2a67ce562bbf2f0cc73f47d8e79f792badf5e63
rc_c1=1
C2=unmet mismatches=2 columns_unchanged=yes tool=ok tool_rc=1 mismatched_axes=operability,freshness rev=b2a67ce562bb
rc_c2=1
```
Matches committed before-c1.txt line `C1=unmet cases_ok=0/15 selftest=absent live=absent registry=met sourced=unmet province=unmet checks_failed=selftest,live,sourced,province root=/fast/scratch/hyaku/mori-r98/before/t exit=1` (only the scratch `root=` path differs) and before-c2.txt exactly (`exit=1`).

**freeze b75e26ccd771b872099ef7233a61e3e91d9f6f7a**
```
C1=unmet cases_ok=0/15 selftest=absent live=absent registry=met sourced=unmet province=unmet checks_failed=selftest,live,sourced,province root=/fast/scratch/hyaku/mori-r98/Mo98ExecReplay/b75e26ccd771b872099ef7233a61e3e91d9f6f7a
rc_c1=1
C2=unmet mismatches=2 columns_unchanged=yes tool=ok tool_rc=1 mismatched_axes=operability,freshness rev=b75e26ccd771
rc_c2=1
```
Consistent: the freeze adds contract/counters/controls/candidate only; the landing work tree (tools/, corpus/, SCORECARD cells) is absent there, so the do-nothing result carries through. No committed receipt exists for this rev; this is a replay observation, not a comparison.

**landing 600deb7ed2695f54b289cf5b6c3931e0fa9c8bb3**
```
C1=met cases_ok=15/15 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) registry=met sourced=met(S629,S630,S631,S632) province=met checks_failed=- root=/fast/scratch/hyaku/mori-r98/Mo98ExecReplay/600deb7ed2695f54b289cf5b6c3931e0fa9c8bb3
rc_c1=0
C2=met mismatches=0 columns_unchanged=yes tool=ok tool_rc=0 mismatched_axes=- rev=600deb7ed269
rc_c2=0
```
Matches committed landing-c1.txt `C1=met cases_ok=15/15 selftest=ok live=ok(limit=122865,used_lb=8,state=ok) registry=met sourced=met(S629,S630,S631,S632) province=met checks_failed=- root=/fast/scratch/hyaku/mori-r98/landing/t exit=0` — every field identical except live-leg `used_lb` (8 → 6), an expected live lower bound (contract "Not claimed" says used_lb is a lower bound; namespace count varies run to run). Matches landing-c2.txt exactly (`exit=0`).

**master tip 379a2f616c146f29341987e73b2828a0ce728ce2**
```
C1=met cases_ok=15/15 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) registry=met sourced=met(S629,S630,S631,S632) province=met checks_failed=- root=/fast/scratch/hyaku/mori-r98/Mo98ExecReplay/379a2f616c146f29341987e73b2828a0ce728ce2
rc_c1=0
C2=met mismatches=0 columns_unchanged=yes tool=ok tool_rc=0 mismatched_axes=- rev=379a2f616c14
rc_c2=0
```
The claimed work is present and passes on the current master tip; no committed receipt exists for this rev (observation only).

## 3. Controls live re-run vs committed receipt

`HYAKU_SCRATCH=$S bash .ufo/waves/round-98/controls-r98.sh b2a67ce562bbf2f0cc73f47d8e79f792badf5e63` → full output (23 CONTROL lines + header + done, `rc_controls=0`, `CONTROLS_DONE unexpected=0`). Field-by-field comparison against the committed evidence/controls-r98.txt:

- All 23 lines match on every verdict-bearing field: expect/rc/AS_EXPECTED, `C1=`/`C2=` verdict, `cases_ok=n/15`, `selftest=`, `registry=`, `sourced=`, `province=`, full `checks_failed=` lists, `mismatches=`, `columns_unchanged=`, `tool=`, `tool_rc=`, `mismatched_axes=`.
- `CONTROLS_DONE unexpected=0` reproduced; exit code 0.
- Divergences observed, all inherent to live/fixture legs, none verdict-bearing:
  1. Live-leg `used_lb` values (c1 rows): P1 9→6, K2 57→48, K3 9→6, K4 9→6, K5 9→6, K7 9→6, K8 9→6, K9 9→6, K10 9→6, K11 9→6; K1 3→3 and K6 7→7 unchanged. Lower-bound drift on the real /proc, explicitly allowed by the task line.
  2. c2 fixture commit ids differ per run (fresh scratch-clone fixture repos are committed anew each run, so their SHAs cannot be stable): P1c `81a755d4a49a`→`d601f3b3eafd`, K1c `2b8d81109deb`→`f03aaf1c0956`, K2c `21093ab6d116`→`e8e1bca93ebc`, K3c `320fa5a4d005`→`fe03b0b51f7a`, K4c `21f337ab76be`→`8d11ac108bfd`. All calibration verdict fields on those rows match exactly.
  3. CONTROLS_HEADER `date=` 21:30:07Z→21:36:26Z (same four pinned hashes).
- Committed receipt reproduced verbatim for citation:
```
CONTROLS_HEADER entering=b2a67ce562bbf2f0cc73f47d8e79f792badf5e63 count-c1.py=a9f140bdd53ae0a17da3bd4549d6db6cb2db68298cd97cc73f51db0e8a152e44 count-c2.py=d6fe755fff2e2805c6550ff9bfe0b53c369d5dd8c9799fe4e02bd1e5e73c01fd candidate-tool=5ab134ee036f83851eb98a9027db699a5800130c5c13598cb37aeb2abe452db2 date=2026-11-05T21:30:07Z
CONTROL c1 K0-do-nothing-entering expect=unmet rc=1 AS_EXPECTED :: C1=unmet cases_ok=0/15 selftest=absent live=absent registry=met sourced=unmet province=unmet checks_failed=selftest,live,sourced,province
CONTROL c1 P1-positive-candidate expect=met rc=0 AS_EXPECTED :: C1=met cases_ok=15/15 selftest=ok live=ok(limit=122865,used_lb=9,state=ok) registry=met sourced=met(S999) province=met checks_failed=-
CONTROL c1 K1-constant-printer expect=unmet rc=1 AS_EXPECTED :: C1=unmet cases_ok=1/15 selftest=ok live=ok(limit=122865,used_lb=3,state=ok) registry=met sourced=met(S999) province=met checks_failed=case_F2-limit-zero,case_F3-full,case_F4-low,case_F5-boundary,case_F6-missing-limit,case_F7-bad-limit,case_F8-low-flag,case_F9-nonpid,case_J1-incident,case_J2-forms,case_J3-two-keys,case_J4-empty,case_J5-unreadable,case_J6-redaction
CONTROL c1 K2-counts-pids-not-namespaces expect=unmet rc=1 AS_EXPECTED :: C1=unmet cases_ok=14/15 selftest=fail live=ok(limit=122865,used_lb=57,state=ok) registry=met sourced=met(S999) province=met checks_failed=selftest,case_F1-mixed
CONTROL c1 K3-fail-open-missing-limit expect=unmet rc=1 AS_EXPECTED :: C1=unmet cases_ok=14/15 selftest=fail live=ok(limit=122865,used_lb=9,state=ok) registry=met sourced=met(S999) province=met checks_failed=selftest,case_F6-missing-limit
CONTROL c1 K4-reads-as-writes expect=unmet rc=1 AS_EXPECTED :: C1=unmet cases_ok=13/15 selftest=fail live=ok(limit=122865,used_lb=9,state=ok) registry=met sourced=met(S999) province=met checks_failed=selftest,case_J1-incident,case_J2-forms
CONTROL c1 K5-accepts-decoy-lines expect=unmet rc=1 AS_EXPECTED :: C1=unmet cases_ok=14/15 selftest=ok live=ok(limit=122865,used_lb=9,state=ok) registry=met sourced=met(S999) province=met checks_failed=case_J2-forms
CONTROL c1 K6-no-registry-row expect=unmet rc=1 AS_EXPECTED :: C1=unmet cases_ok=15/15 selftest=ok live=ok(limit=122865,used_lb=7,state=ok) registry=unmet sourced=met(S999) province=met checks_failed=registry
CONTROL c1 K7-no-knowledge-entry expect=unmet rc=1 AS_EXPECTED :: C1=unmet cases_ok=15/15 selftest=ok live=ok(limit=122865,used_lb=9,state=ok) registry=met sourced=unmet province=met checks_failed=sourced
CONTROL c1 K8-row-not-mined expect=unmet rc=1 AS_EXPECTED :: C1=unmet cases_ok=15/15 selftest=ok live=ok(limit=122865,used_lb=9,state=ok) registry=met sourced=unmet province=met checks_failed=sourced
CONTROL c1 K9-no-province-line expect=unmet rc=1 AS_EXPECTED :: C1=unmet cases_ok=15/15 selftest=ok live=ok(limit=122865,used_lb=9,state=ok) registry=met sourced=met(S999) province=unmet checks_failed=province
CONTROL c1 K10-limit-zero-reads-ok expect=unmet rc=1 AS_EXPECTED :: C1=unmet cases_ok=14/15 selftest=fail live=ok(limit=122865,used_lb=9,state=ok) registry=met sourced=met(S999) province=met checks_failed=selftest,case_F2-limit-zero
CONTROL c1 K11-echoes-raw-journal-line expect=unmet rc=1 AS_EXPECTED :: C1=unmet cases_ok=13/15 selftest=ok live=ok(limit=122865,used_lb=9,state=ok) registry=met sourced=met(S999) province=met checks_failed=case_J1-incident,case_J6-redaction
CONTROL c2 K0c-do-nothing-entering expect=unmet rc=1 AS_EXPECTED :: C2=unmet mismatches=2 columns_unchanged=yes tool=ok tool_rc=1 mismatched_axes=operability,freshness rev=b2a67ce562bb
CONTROL c2 P1c-positive-both-cells expect=met rc=0 AS_EXPECTED :: C2=met mismatches=0 columns_unchanged=yes tool=ok tool_rc=0 mismatched_axes=- rev=81a755d4a49a
CONTROL c2 K1c-one-cell-only expect=unmet rc=1 AS_EXPECTED :: C2=unmet mismatches=1 columns_unchanged=yes tool=ok tool_rc=1 mismatched_axes=freshness rev=2b8d81109deb
CONTROL c2 K2c-wrong-verdict-word expect=unmet rc=1 AS_EXPECTED :: C2=unmet mismatches=1 columns_unchanged=yes tool=ok tool_rc=1 mismatched_axes=operability rev=21093ab6d116
CONTROL c2 K3c-score-cell-edited expect=unmet rc=1 AS_EXPECTED :: C2=unmet mismatches=0 columns_unchanged=no tool=ok tool_rc=1 mismatched_axes=- rev=320fa5a4d005
CONTROL c2 K4c-tool-bytes-changed expect=unmet rc=1 AS_EXPECTED :: C2=unmet mismatches=0 columns_unchanged=yes tool=changed tool_rc=0 mismatched_axes=- rev=21f337ab76be
CONTROLS_DONE unexpected=0
```

## 4. Verdict

- C1: before-receipt reproduced at entering (unmet 0/15, rc 1); landing-receipt reproduced at landing (met 15/15, rc 0); also met at freeze-absence boundary (unmet, as expected) and at current master tip (met). HOLDS.
- C2: before-receipt reproduced at entering (unmet mismatches=2, rc 1); landing-receipt reproduced at landing (met mismatches=0 columns_unchanged=yes, rc 0); also met at current master tip. HOLDS.
- Controls: live re-run reproduces all 23 committed CONTROL verdicts with `unexpected=0`; only allowed live-leg `used_lb`, per-run fixture commit ids, and the header timestamp differ.
- No divergence to report. Unrun checks: none — every check named in the seat task was executed. No tool was installed or upgraded (none needed).
