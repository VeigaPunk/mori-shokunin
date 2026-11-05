# Mo99ExecReplay — round 99 attempt 1, wave w1 — executor replay of frozen measurements

Seat: Mo99ExecReplay (executor, replay). Lane repo: /home/vgpnk/Projects/shokunin/mori-shokunin.
Revisions: entering 73308ff6e5c933f53498e9501ef95917b0ef7171; freeze 462cef1cc637de4c6e993aefd00ed9df32895984; landing 5013f0be8ac9e7fce3c08b680e43cf9cbd49620d (lane HEAD).
Scratch: /fast/scratch/hyaku/mori-r99/Mo99ExecReplay (removed at end). Tools installed: none. Nothing in the lane or fleet was mutated; read-only git only.
Seeds chosen for replay: 1, 42, 2026 (plus one run without `--seed`; the counter then printed seeds 24547793127459 on entering and 125824862970594 on landing).

## 1. C1 counter (count-c1.py) — replayed

Archive → `$S/landing` (5013f0be) and `$S` (73308ff6, entering); freeze archived to `$S/freeze`.

Entering (73308ff6):
```
seed=1    : C1=unmet cases_ok=24/60 seed=1 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=unmet checks_failed=battery,sourced  RC=1
seed=42   : C1=unmet cases_ok=24/60 seed=42 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=unmet checks_failed=battery,sourced  RC=1
seed=2026 : C1=unmet cases_ok=24/60 seed=2026 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=unmet checks_failed=battery,sourced  RC=1
no seed   : C1=unmet cases_ok=24/60 seed=24547793127459 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=unmet checks_failed=battery,sourced  RC=1
```
Landing (5013f0be):
```
seed=1    : C1=met cases_ok=60/60 seed=1 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-  RC=0
seed=42   : C1=met cases_ok=60/60 seed=42 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-  RC=0
seed=2026 : C1=met cases_ok=60/60 seed=2026 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-  RC=0
no seed   : C1=met cases_ok=60/60 seed=125824862970594 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) incident=ok registry=met sourced=met(S633,S634,S635,S636) checks_failed=-  RC=0
```
Matches the frozen receipts `evidence/before-c1.txt` (`C1=unmet cases_ok=24/60 ... checks_failed=battery,sourced`, exit 1) and `evidence/landing-c1.txt` (`C1=met cases_ok=60/60 ... checks_failed=-`, exit 0). Battery failures on entering are in the W4–W8, R1–R4 and S1–S3 families (per-case `FAIL` lines, identical set across seeds).

## 2. C2 counter (count-c2.py) — replayed

```
entering 73308ff6: axis coverage/operability/depth/freshness/calibration pointer=missing, adjacency pointer=ok
                   C2=unmet mismatches=5 cells_unchanged=yes gate=rc1 mismatched_axes=coverage,operability,depth,freshness,calibration rev=73308ff6e5c9  RC=1
freeze 462cef1c:   same five missing pointers
                   C2=unmet mismatches=5 cells_unchanged=yes gate=rc1 mismatched_axes=coverage,operability,depth,freshness,calibration rev=462cef1cc637  RC=1
landing 5013f0be:  axis coverage/operability/depth/freshness/calibration/adjacency all pointer=ok
                   C2=met mismatches=0 cells_unchanged=yes gate=ok mismatched_axes=- rev=5013f0be8ac9  RC=0
```
Matches `evidence/before-c2.txt` and `evidence/landing-c2.txt`. Note: the counter's `pointer=ok` checks only that each pointer is present and located; I did not re-audit the cell text beyond what the counter does.

## 3. Controls runner — re-run on entering

`controls-r99.py --lane /home/vgpnk/Projects/shokunin/mori-shokunin --entering 73308ff6e5c933f53498e9501ef95917b0ef7171 --scratch $S/ctl` → exit 0, final line `CONTROLS_DONE unexpected=0`.
- First line (sha256 prefixes) identical to the frozen receipt: `count-c1.py=0d8ad8b759b3580e`, `count-c2.py=b9b58acae05f0d88`, `candidate/tools/mori-userns-runway.py=4ef3108f171dc5fa`, `candidate/apply-c2.py=beadfec7740590fd`, `controls-r99.py=79b56857654836d0`, `SKILL.md=3d05509abfb0015a`, `corpus/SOURCES.md=a426416125ed7284`, `corpus/knowledge/sudo-log-grammar-r99.md=d826d3dd7d18bf75`.
- Verdict column: all 19 control rows `AS_EXPECTED` (K0–K11, P1, K0c–K4c, P1c), same as the frozen receipt (19 rows AS_EXPECTED, 0 UNEXPECTED).
- Non-verdict detail differs only in host-dependent live `used_lb` (6/7/8/9 across runs); verdicts unaffected.

## 4. Instrument identity

- `git diff 462cef1cc637de4c6e993aefd00ed9df32895984 5013f0be8ac9e7fce3c08b680e43cf9cbd49620d -- .ufo/waves/round-99/` → 0 bytes. Freeze bytes = landing bytes for all wave files.
- `sha256(landing tools/mori-userns-runway.py)` = `4ef3108f171dc5fa0b42c8dc1cf4f374cb223ab0bb9411c1e992e255e46abc0b`; `sha256(freeze candidate/tools/mori-userns-runway.py)` = the same. Equal.
- Landing hashes of pinned files: SKILL.md `3d05509a…`, corpus/SOURCES.md `a4264161…`, corpus/knowledge/sudo-log-grammar-r99.md `d826d3dd…`, incident capture `7ec650c9d41085938793451b4404e66fdb4f2c6e960600f3b57bfbfcf2d6090d` (equals freeze and the pin in count-c1.py).

## 5. r98 counter on landing — which case changed and why

Entering (73308ff6): `C1=met cases_ok=15/15 ... checks_failed=-` (RC 0).
Landing (5013f0be): `C1=unmet cases_ok=13/15 ... checks_failed=case_J1-incident,case_J2-forms` (RC 1). Runway cases F1–F9 all still pass.

**Case J1-incident (disclosed).** The r98 capture lacks the `(command continued)` line: `grep -c 'command continued'` = 0 on `round-98/evidence/journal-incident-r98.txt`, = 1 on the r99 capture (line 320). Entry 107 of the r98 capture (`sudo[1749648]… COMMAND=/usr/bin/sh -c 'cat > … <<\'EOF\'#012CAP=…`) opens a quote that is never closed in the capture. Landing on that line alone: `SYSCTL_WRITES n=0 keys=0 userns_zero=0` + `SYSCTL_WRITES_SETUP unparsed=1`, rc 2. Entering on the same line: rc 0, silent. Whole r98 capture on landing:
```
SYSCTL_WRITE ts=2026-11-05T05:42:18-03:00 pid=2548588 key=user.max_user_namespaces value=122865 via=sysctl
SYSCTL_WRITES n=6 keys=1 userns_zero=2
SYSCTL_WRITES_SETUP unparsed=1      (rc 2)
```
Writes are the same six as entering (`n=6 keys=1 userns_zero=2`); the change is exit 2 on the truncated entry. Matches the claim's disclosure.

**Case J2-forms (NOT disclosed).** The r98 counter's J2 fixture contains, as its last line, `2026-11-05T10:00:07-03:00 h systemd[1]: Started sudo[108] COMMAND=/usr/bin/sysctl -w x.y=1`. Per-line landing check: that line alone → `SYSCTL_WRITES_SETUP unparsed=1`, rc 2. Full J2 on landing:
```
SYSCTL_WRITES n=4 keys=4 userns_zero=0
SYSCTL_WRITES_SETUP unparsed=1      (rc 2)
```
Entering: same four writes, `SYSCTL_WRITES n=4 keys=4 userns_zero=0`, rc 1, and the systemd line is ignored. The landing tool's docstring (line 32) states it only considers lines carrying `sudo[` and ` COMMAND=`; this line carries both, so the fail-closed rule fires on a systemd message that is not a sudo log entry. The four real writes are unchanged. The claim's "Disclosed behaviour change" names only J1 and says "the frozen r98 counter's J1 case no longer holds"; it does not name J2.

## 6. Other observations (not remediated)

- Lane working tree is dirty and not clean at landing: `git -C mori-shokunin diff HEAD --stat` → `corpus/QUALITY.md | 18 ++++++++++++++++++` (uncommitted criteria 210 and 211 for round 99). Not in commit 5013f0be; not part of the frozen instrument set. Reported for the L1 to decide. No edit made.
- `count-c1.py` at landing: the frozen predicate (a)–(f) holds on all four seeds (see §1).

## Verdicts

VERDICT C1 needs-amend: frozen P1 holds on replay (landing `C1=met cases_ok=60/60` on seeds 1, 42, 2026 and unseeded; entering `C1=unmet cases_ok=24/60`), but the disclosed behaviour change omits the r98 J2 case, which also flips rc 1→2 because the tool fail-closes on a systemd line carrying `sudo[` and ` COMMAND=`.

VERDICT C2 holds: replayed `C2=unmet mismatches=5 ... gate=rc1` at entering and freeze; `C2=met mismatches=0 cells_unchanged=yes gate=ok mismatched_axes=-` at landing; controls K4c (score edit) fails as expected.

## Unrun checks

- No build, lint or test suite was run (none assigned to this seat).
- The `--selftest` of the tool was not run separately; the counter invokes it on each replay and reports `selftest=ok`.
- I did not re-run the full r98 counter with any seed (it has no seed parameter).
