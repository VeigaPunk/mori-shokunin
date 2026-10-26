# Mo51RevSkillRow — SKILL.md / SHONEN.md edit review at 87e0c37 (round 51, w1)

Seat: Mo51RevSkillRow (leaf; no subagents). Scoped to the doc cells of the C1 data land:
`git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd 87e0c374537557754bf71dd68036ded3ddc6699c -- SKILL.md SHONEN.md` (rc 0) — exactly 2 files changed. All git reads are `git show`/`git grep` at the rev; nothing was mutated. Scratch: `/fast/scratch/hyaku/mori-r51/Mo51RevSkillRow/` (removed before finish); disk-guard OK (594.9G free on /fast). Host: MACHINE_ID.

## 1. What the data edit changed

- SKILL.md:938 (registry row "registry pin reconciler (r47, C1)"): entry cell adds `[--scratch DIR]` and the v5 note ("the `--rev` tree is a `git clone --shared` under `--scratch`/TMPDIR, never under the repo"); verdict-map cell adds the `class=env`/`class=stale` sentence and "the summary ends `env=N stale=N` (v5, round 51)"; self-test cell `PIN_CHECK_SELFTEST pass=114 fail=0` → `pass=119 fail=0`. The write-scope cell and the pinned-values cell are unchanged.
- SHONEN.md:6: tally pin `(114/114)` → `(119/119)`; receipt paths moved from `.ufo/waves/round-50/evidence/selftests/…` to `.ufo/waves/round-51/evidence/selftests/…`; appended "(round-51 C1: pin-check v5 adds five arms)".

## 2. Receipts exist, are tracked at R, and carry the lines

`git ls-tree -r 87e0c37 --name-only -- .ufo/waves/round-51/evidence/selftests/` lists both files; working-tree sha256 == blob sha256 at 87e0c37:

- `.ufo/waves/round-51/evidence/selftests/mori-pin-check.txt` — 98ef79d805a86c3b0d7c2fdde92ff71236143d7790f1404878f46db55c9155ee; final lines `PIN_CHECK_SELFTEST pass=119 fail=0` / `exit=0`.
- `.ufo/waves/round-51/evidence/selftests/mori-unlanded-check.txt` — 28df984fcda39244a1b199f56361e8992b8f80d1d3adf353836150c07a1c8bd4; final lines `UNLANDED_SELFTEST pass=17 fail=0` / `exit=0`.

The pin-check receipt carries exactly five new PASS arms versus the round-50 (v4) receipt's 114:
`v5_class_env_setup_error`, `v5_class_env_timeout`, `v5_class_stale_tally`, `v5_class_stale_digest`, `v5_rev_export_outside_repo` → 119 = 114 + 5, so SHONEN's "adds five arms" is exact.

## 3. Verdict-map wording versus observed v5 behavior

The row's verdict map claims: every mismatch line ends `class=env` (no tally line) or `class=stale` (different tally / contradicting exit code / digest or line-count pin), and the summary ends `env=N stale=N`. The frozen round-51 counter receipt `.ufo/waves/round-51/evidence/c1-at-data.txt` (read from the working tree; untracked at 87e0c37 — the L1's post-data receipt) shows exactly:

```
classified: pin line=3 kind=tally prefix=ENVA_SELFTEST state=mismatch pinned='pass=3 fail=0' observed=None rc=2 cmd='python3 tools/enva.py --selftest' class=env
classified: pin line=4 kind=tally prefix=ENVB_SELFTEST state=mismatch pinned='pass=4 fail=0' observed=None rc=1 cmd='python3 tools/envb.py --selftest' class=env
classified: pin line=5 kind=tally prefix=STLA_SELFTEST state=mismatch pinned='pass=4 fail=0' observed='pass=5 fail=0' rc=0 cmd='python3 tools/stla.py --selftest' class=stale
classified: pin line=6 kind=tally prefix=STLB_SELFTEST state=mismatch pinned='pass=2 fail=0' observed='pass=2 fail=0' rc=1 cmd='python3 tools/stlb.py --selftest' class=stale
classified: pin line=7 kind=tally prefix=OKAY_SELFTEST state=match pinned='pass=1 fail=0' observed='pass=1 fail=0' rc=0 cmd='python3 tools/okay.py --selftest'
classified: PIN_CHECK=unmet tally_pins=5 digest_pins=0 mismatches=4 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=- baseline=no env=2 stale=2
C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=119,fail=0 rev=87e0c374537557754bf71dd68036ded3ddc6699c failed=-
exit=0
```

This matches the wording case-for-case: env = setup error (rc 2) / no tally line (rc 1, observed=None); stale = different tally (STLA) / contradicting exit code with matching tally (STLB); the match line has no class; summary ends `env=2 stale=2`. The row's escaped-pipe state alternation parses (the v5 `--rev` arm B ran the real SKILL.md at R and came out `relocated=met reloc_mismatch=0`). UNVERIFIED: I did not independently re-run `count-c1.py` (designated attack seats re-run both counters); the `class=` line text above is cited from the frozen receipt plus the passing v5 selftest arms.

## 4. Round-50 calibration counter at 87e0c37 — does round 50's C1 stay met? NO.

Command (absolute): `TMPDIR=/fast/scratch/hyaku/mori-r51/Mo51RevSkillRow/tmp python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-50/count-c1.py 87e0c374537557754bf71dd68036ded3ddc6699c --scratch /fast/scratch/hyaku/mori-r51/Mo51RevSkillRow/r50run` → exit 1:

```
item axis coverage expect=round_47_improved got=ok state=ok
item axis operability expect=round_47_improved got=ok state=ok
item axis depth expect=round_49_improved got=ok state=ok
item axis freshness expect=round_28_improved got=ok state=ok
item axis calibration expect=round_49_improved got=ok state=ok
item axis adjacency expect=round_19_improved got=ok state=ok
item pin python3_tools/mori-pin-check.py_--selftest expect=(119/119) got=PIN_CHECK_SELFTEST_pass=119_fail=0_receipt_missing state=mismatch
item pin python3_tools/mori-unlanded-check.py_--selftest expect=(17/17) got=UNLANDED_SELFTEST_pass=17_fail=0 state=ok
C1=unmet items=8 axes=6 pins=2 boxes=4 mismatches=1 errors=0 hidden=0 manifest=a94551c5bc8d rev=87e0c374537557754bf71dd68036ded3ddc6699c failed=mismatch
EXIT=1
```

Mechanism: the frozen round-50 counter re-runs the pinned tool at R from `git archive 87e0c37` (observed `PIN_CHECK_SELFTEST pass=119 fail=0` — so the new `(119/119)` pin's numbers match the tool), then requires `.ufo/waves/round-50/evidence/selftests/mori-pin-check.txt` at R to contain the observed line. The round-50 receipt still holds `PIN_CHECK_SELFTEST pass=114 fail=0` — it is the historical freeze record of round-50's v4 tool — hence `receipt_missing` → mismatch. This is exactly the shape round-50's own control demonstrated (`evidence/control-c1-pins-updated-no-receipt.txt:8`: `expect=(114/114) got=PIN_CHECK_SELFTEST_pass=114_fail=0_receipt_missing state=mismatch`). This is not a defect of the round-51 edit: overwriting the round-50 receipt to hold 119 would falsify a historical record, and the round-50 counter is a calibration instrument scored at its own rev (the round-51 contract routes the successor calibration counter to round 52). Residual (named): any re-run of the round-50 counter at a rev ≥ 87e0c37 reads unmet on the receipt arm; the changed pin is what exposes it. The unlanded pin (17/17) stays met (receipt unchanged and matches).

## 5. Stale 114 sweep at 87e0c37

`git grep -nE '114/114|pass=114' 87e0c37` (whole tracked tree) plus `git grep -n 'PIN_CHECK_SELFTEST pass=' 87e0c37 -- SKILL.md SHONEN.md LOG.md PROVINCE.md corpus`. Every hit classified; all remaining 114 mentions are historical:

- round-50 wave reports, contract, controls, evidence (`.ufo/waves/round-50/`) — records of that round;
- the round-51 frozen contract's before-rows (`contract.md:45,139,140,141`), the control builder (`controls/c1-controls.py:32` `PIN_OLD`), and the control receipts (`evidence/control-c1-*.txt`) — the entering-state fixtures/readings;
- `LOG.md:2737,2744` and `SCORECARD.md:2674` — round-50 closure narrative;
- `SKILL.md:1020` — Round50 section narrative ("Round 49's spot-check routed defect 2 — the 114/114 and 17/17 tallies were prose only");
- `corpus/QUALITY.md:1181` — QUALITY 134's rationale quoting the round-50 before-state;
- `corpus/lessons/round-48.md/round-49.md/round-49-verifier-spotcheck.md/round-50.md/round-50-verifier-spotcheck.md` — lessons;
- `considerthese/2026-10-26.md:9` — the suggestion text as written at that time.

No current tally carrier says 114: SKILL.md:938 and SHONEN.md:6 both say 119, and SHONEN.md had no 114 token at R (the round-50 counter observed `hidden=0`).

## Findings

1. **MED — SKILL.md:938, write-scope cell is stale for v5.** The cell still reads: "its own export and TMPDIR under `<repo>/.scratch` (removed on exit); runs the registered selftests, which write only their own temp dirs". The same row's entry cell now says the `--rev` tree is "never under the repo", and the v5 tool's own docstring (`tools/mori-pin-check.py:127-134`) says: with `--rev` it writes only its measured tree (a `git clone --shared`) under `--scratch DIR` (default: the TMPDIR temp dir, never `<repo>`; removed on exit; a killed run leaves it in scratch, not the repo); with `--root` it writes temp dirs under `<root>/.scratch`; `--selftest` builds synthetic trees under TMPDIR. So the cell's "its own export … under `<repo>/.scratch`" is false for the row's primary `--rev` mode, and "TMPDIR under `<repo>/.scratch`" is true only in `--root` mode (where the measured tree is the given root). A reader of the write-scope cell would expect repo writes that v5 no longer performs (and might even "fix" the tool to restore them). The entry cell carries the correct v5 note, so the truth is adjacent — hence MED, not HIGH. Draft correction for the L1 (fenced below).

2. **LOW — round-50 `count-c1.py` at 87e0c37 reads `C1=unmet`** on the receipt arm (line pasted in §4); named residual, not a fix proposal (counters are frozen).

3. **LOW — receipt provenance labels.** Both round-51 receipts' first line says "working tree after the round-51 C1 data edit, run 2026-10-26" rather than naming the frozen rev (the round-50 receipts named `git archive of <rev>`; round-50's Mo50bCritNoHarm already flagged that label class). Mitigated: my archive re-run at 87e0c37 (via the round-50 counter) observed the identical final tally, and the tracked receipt blobs are byte-identical to the working tree.

Verification gaps: round-51 `count-c1.py` not re-run by this seat (frozen receipt cited); `c1-at-data.txt` is untracked at 87e0c37 (read from the working tree); the `class=` line text relies on that receipt plus the v5 selftest arms, not on an independent fixture run by this seat.

```markdown
Draft (for the L1 only): SKILL.md:938 write-scope cell →
"v5 (round 51): `--rev` writes only its clone under `--scratch`/TMPDIR
(removed on exit), never under the repo; `--root` writes temp dirs under
`<root>/.scratch`; `--selftest` builds synthetic trees under TMPDIR"
```
