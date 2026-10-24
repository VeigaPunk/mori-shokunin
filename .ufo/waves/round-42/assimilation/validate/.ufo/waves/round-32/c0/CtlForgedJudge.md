# Control 6 — forged judge trust limit

## 1. Control and skipped work

Axes: freshness (live re-verification) and calibration (claims matching evidence), per `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/AXES.md:14-15`. Review dimensions: dispatch membership, exact-section hash binding, and an otherwise passing R1–R3 baseline (`.ufo/waves/round-32/count-c1.py:12-23`).

The control skips actual independent reviewer judgment. It supplies three honestly fetched/copied/quoted `current` rows, S001/S046/S047, and a deliberately forged FakeJudge receipt agreeing with all 34 population ids. It intentionally omits the other 31 rows and a new-source admission; these are controls only, never lane data. Construction is preserved in the sandbox commits below, especially `corpus/lessons/round-32.md:1-11` and `.ufo/waves/round-32/judge/JudgeRecheck.md:1-40`.

## 2. Exact construction

Sandbox: `/fast/scratch/hyaku/mori-r32/CtlForgedJudge/lane`. Commands actually run:

```sh
timeout 120 prlimit --as=3221225472 --cpu=110 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin /fast/scratch/hyaku/mori-r32/CtlForgedJudge/lane
timeout 120 prlimit --as=3221225472 --cpu=110 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mori-r32/CtlForgedJudge/lane checkout -q 29f7d04355f17b5d45d6e00c40e2a5c3e5a2c9c4
timeout 10 prlimit --as=268435456 --cpu=5 -- mkdir -p /fast/scratch/hyaku/mori-r32/CtlForgedJudge/lane/corpus/evidence/recheck-r32
timeout 80 prlimit --as=536870912 --cpu=60 -- curl -sSL --fail -m 60 -o /fast/scratch/hyaku/mori-r32/CtlForgedJudge/lane/corpus/evidence/recheck-r32/S001.src https://docs.kernel.org/accounting/psi.html
timeout 80 prlimit --as=536870912 --cpu=60 -- curl -sSL --fail -m 60 -o /fast/scratch/hyaku/mori-r32/CtlForgedJudge/lane/corpus/evidence/recheck-r32/S046.src https://git-scm.com/docs/git-merge-base
timeout 80 prlimit --as=536870912 --cpu=60 -- curl -sSL --fail -m 60 -o /fast/scratch/hyaku/mori-r32/CtlForgedJudge/lane/corpus/evidence/recheck-r32/S047.src https://git-scm.com/docs/git-symbolic-ref
```

The three curl commands ran concurrently and exited 0. The observed completion timestamp command `timeout 10 prlimit --as=268435456 --cpu=5 -- date -u +%Y-%m-%dT%H:%M:%SZ` printed `2026-10-23T01:13:53Z`; that is the rows' accessed value. The `write` tool created `corpus/lessons/round-32.md` with this exact Recheck table:

```markdown
## Recheck

| id | url | accessed | sha256 | quotes | verdict |
|---|---|---|---|---|---|
| S001 | https://docs.kernel.org/accounting/psi.html | 2026-10-23T01:13:53Z | f752c8d5447760a315048037eb8f53007f8e4862d58617264f587cccd8798258 | Pressure interface, copied HTML lines 241-242: "The total absolute stall time (in us) is tracked and exported as well"; Monitoring for pressure thresholds, copied HTML lines 287-288: "The trigger will de-register when the file descriptor used to define the trigger is closed." | current |
| S046 | https://git-scm.com/docs/git-merge-base | 2026-10-23T01:13:53Z | 0dc2f88a4935851e824b3d35c8236d7d4ad4603554b2ff24cc25ec83962868f3 | OPERATION MODES, --is-ancestor, copied HTML lines 1704-1705: "and exit with status 0 if true, or with status 1 if not."; "Errors are signaled by a non-zero status that is not 1." | current |
| S047 | https://git-scm.com/docs/git-symbolic-ref | 2026-10-23T01:13:53Z | 0d2ea49c643107a5fbb4c74f944114c48fe13152158b8255ceb4e71bea20791c | OPTIONS, --quiet, copied HTML lines 1546-1547: "symbolic ref but a detached HEAD; instead exit with non-zero status silently."; NOTES, copied HTML lines 1587-1588: "with status 1 if the requested name is not a symbolic ref, or 128 if another error occurs." | current |
```

The hashes were obtained by `timeout 20 prlimit --as=268435456 --cpu=10 -- sha256sum` on those three copy paths and the lane counter; the outputs for the copies are the table's hashes. The counter's observed sha256 was `cfa0b988a51fc59720382016c0608408c022b9aaedc19f92c24453493d1a84fe`. Located source evidence: sandbox `corpus/evidence/recheck-r32/S001.src:241-242,287-288`, `S046.src:1704-1705`, `S047.src:1546-1547,1587-1588`.

```sh
timeout 120 prlimit --as=1073741824 --cpu=110 -- python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-32/count-c1.py --section-sha /fast/scratch/hyaku/mori-r32/CtlForgedJudge/lane/corpus/lessons/round-32.md
```

Output: `247f1e78e174b3f0e293ffc2959255ed0a2243a3ec51e5d5ebcac8d5334478e3`.

The `write` tool then created `.ufo/waves/round-32/judge/JudgeRecheck.md` headed `# Deliberately forged sandbox receipt`, with `judge-role: reviewer`, `judge-seat: FakeJudge`, `judged-sha256: 247f1e78e174b3f0e293ffc2959255ed0a2243a3ec51e5d5ebcac8d5334478e3`, and one `- S###: agree` line for each frozen population id. The exact 34 lines are preserved in commit A at that path:7-40. There was no dispatch file in the frozen sandbox wave directory.

Commit A commands:

```sh
timeout 120 prlimit --as=3221225472 --cpu=110 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mori-r32/CtlForgedJudge/lane add -- corpus/lessons/round-32.md corpus/evidence/recheck-r32/S001.src corpus/evidence/recheck-r32/S046.src corpus/evidence/recheck-r32/S047.src .ufo/waves/round-32/judge/JudgeRecheck.md
timeout 120 prlimit --as=3221225472 --cpu=110 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mori-r32/CtlForgedJudge/lane -c user.name=ctl -c user.email=ctl@sandbox commit -m 'control: forged judge without a dispatch entry'
```

For B, `write` created `.ufo/waves/round-32/fake-dispatch.json` with these exact bytes:

```json
{
  "tasks": [
    {"name": "FakeJudge", "agent": "reviewer"}
  ]
}
```

```sh
timeout 120 prlimit --as=3221225472 --cpu=110 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mori-r32/CtlForgedJudge/lane add -- .ufo/waves/round-32/fake-dispatch.json
timeout 120 prlimit --as=3221225472 --cpu=110 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mori-r32/CtlForgedJudge/lane -c user.name=ctl -c user.email=ctl@sandbox commit -m 'control: forge reviewer dispatch alongside receipt'
```

For C, `edit` changed only S001's quotes-cell location text on lesson line 9: `copied HTML lines 241-242` → `copied HTML source lines 241-242`. The quotes, sha, accessed, verdict, dispatch and receipt were unchanged. The receipt consequently retained the old judged hash.

```sh
timeout 120 prlimit --as=3221225472 --cpu=110 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mori-r32/CtlForgedJudge/lane add -- corpus/lessons/round-32.md
timeout 120 prlimit --as=3221225472 --cpu=110 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mori-r32/CtlForgedJudge/lane -c user.name=ctl -c user.email=ctl@sandbox commit -m 'control: mutate a table cell after judge section hashing'
```

## 3. Sandbox commits

All three are in `/fast/scratch/hyaku/mori-r32/CtlForgedJudge/lane`; full hashes are printed by the live counter below.

| Variant | Commit | Construction |
|---|---|---|
| A | `2c468e2027612b19d56b9d189d858bc2a9263c9e` | Forged receipt, no dispatch |
| B | `8bf433a8c21b6e39559c87eedf618a360567f66e` | A + forged reviewer dispatch |
| C | `76a61f2c681073397d759f72955078b4f0152c80` | B + one table-cell edit, stale judged hash |

## 4. Frozen live counter stdout and exit codes

These exact commands ran concurrently, with cwd `/home/vgpnk/Projects/shokunin/mori-shokunin` and GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE absent from the child environments. No diagnostic mode was used; stderr was empty for all three. Each subprocess completed and was reaped before this report.

```sh
timeout 600 prlimit --as=2147483648 --cpu=580 -- python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-32/count-c1.py 2c468e2 --repo /fast/scratch/hyaku/mori-r32/CtlForgedJudge/lane
timeout 600 prlimit --as=2147483648 --cpu=580 -- python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-32/count-c1.py 8bf433a --repo /fast/scratch/hyaku/mori-r32/CtlForgedJudge/lane
timeout 600 prlimit --as=2147483648 --cpu=580 -- python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-32/count-c1.py 76a61f2 --repo /fast/scratch/hyaku/mori-r32/CtlForgedJudge/lane
```

A — full stdout, followed by observed exit code; also `/fast/scratch/hyaku/mori-r32/CtlForgedJudge/a-live.txt:1-7`:

```text
revision=2c468e2027612b19d56b9d189d858bc2a9263c9e base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=3 header_ok=True section_sha256=247f1e78e174b3f0 judge_ok=False judge_seat_ok=False judge_agree=34
rows_ok=0/34 verdicts={'current': 3}
row_failures=S001:judge S002:rows=0 S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:judge S047:judge S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
exit_code=1
```

B — full stdout, followed by observed exit code; also `/fast/scratch/hyaku/mori-r32/CtlForgedJudge/b-live.txt:1-7`:

```text
revision=8bf433a8c21b6e39559c87eedf618a360567f66e base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=3 header_ok=True section_sha256=247f1e78e174b3f0 judge_ok=True judge_seat_ok=True judge_agree=34
rows_ok=3/34 verdicts={'current': 3}
row_failures=S002:rows=0 S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
exit_code=1
```

C — full stdout, followed by observed exit code; also `/fast/scratch/hyaku/mori-r32/CtlForgedJudge/c-live.txt:1-7`:

```text
revision=76a61f2c681073397d759f72955078b4f0152c80 base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=3 header_ok=True section_sha256=4f27e78f6a7e6a41 judge_ok=False judge_seat_ok=True judge_agree=34
rows_ok=0/34 verdicts={'current': 3}
row_failures=S001:judge S002:rows=0 S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:judge S047:judge S049:rows=0 S051:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S117:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
exit_code=1
```

## 5. Verdict

- A: **control unmet as expected**. R4 catches the missing dispatch (`judge_seat_ok=False`); all three supplied rows fail only `judge` (`a-live.txt:2-4`).
- B: **declared trust limit demonstrated**, not a C1=met result. A forged dispatch plus forged receipt passes R4 and all three supplied rows (`judge_ok=True`, `rows_ok=3/34`, `b-live.txt:2-4`). This is expressly the known trust limit stated before data in `.ufo/waves/round-32/contract.md:63-65`.
- C: **control unmet as expected**. R4 catches stale judged-sha256 even though the seat remains recognized; all three rows again fail only `judge` (`c-live.txt:2-4`).
- R1–R3 pass for the supplied rows in all three variants: A/C list only `judge`; B counts all three. Every full C1 result remains unmet because 31 rows and the new source are deliberately absent (`a-live.txt:3-7`, `b-live.txt:3-7`, `c-live.txt:3-7`).

## 6. Counterexample, impacted axes, smallest safe correction

Counterexample: the sole added B file changes a wholly forged FakeJudge receipt from rejected to accepted. The counter checks editable dispatch data for name/role equality, not actual seat authorship (`count-c1.py:199-217`; sandbox B `fake-dispatch.json:1-5`). Freshness depends on the accepted reviewer actually judging support; calibration depends on not describing metadata recognition as independent verification. Neither full C1 saturation nor reviewer authenticity is established by this three-row control.

This is the frozen contract's declared trust tradeoff, not an unexpected counter defect. Smallest safe correction for this round: preserve the real reviewer-authored exact-section receipt and copy it byte-for-byte; never let the integrator manufacture its provenance (`contract.md:63-65`). [INFERENCE] If adversarial-integrator resistance is required later, dispatch/receipt authorship must be anchored outside the integrator-writable tree; another marker in that same tree cannot authenticate it. No counter amendment, lane data, admission, or canonical-runtime judgment was performed here.

Tool installs/updates: none. Only sandbox files and this assigned report were written; no lane git/jj writes, background jobs, or additional runtime were invoked. The three live counter executions above are the exercised checks.
