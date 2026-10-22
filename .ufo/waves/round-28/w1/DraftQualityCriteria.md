# DraftQualityCriteria — QUALITY 83 and 84 (mori round 28, wave 1)

Seat: MoriR28.DraftQualityCriteria (scribe, leaf). Date: 2026-10-22.
Lane: /home/vgpnk/Projects/shokunin/mori-shokunin. Read-only lane use; no lane writes beyond this report.
Draft target: append to `corpus/QUALITY.md` after criterion 82 (file ends at line 383 at `079a47c`).

## Deliverable — ready to paste into `corpus/QUALITY.md`

```markdown
## Criteria added round 28 — round-27 routed defects 1 and 2

83. A dated amendment or heading states a time read from the clock or from git, never a time typed from memory, and
    that time is never later than the commit that ships the line. The check reads the contract and every commit time
    from git objects at `<rev>`. The bound is the commit's committer time: in this jj-colocated lane the author time
    is when the empty change was opened, not when its content was written, so an author-time bound false-fires on
    honest text — the round-17 A1 heading states `2026-10-20 ~16:10` and ships in `273aa74` (author
    15:26:13-03:00, committer 16:31:56-03:00). A heading that states only a date is compared by calendar day; a
    zone-less local time by that minute in the commit's own offset; a full instant by the second. Check:
    `python3 -I -B .ufo/waves/round-28/check-heading-time.py <rev> <file> [--heading <substring>]
    [--bound cI|aI]` prints one line per dated heading with `verdict=ok|FUTURE-DATED` and exits 1 when any heading is
    future-dated, 0 when none is, 2 on a bad revision, a missing file or a usage error. It FAILS on round-27 W1 at
    `df886be1` (`stated=2026-10-22T15:55Z`, `added_by=dd4dbb20`, `cI=2026-10-22T12:50:10-03:00`,
    `verdict=FUTURE-DATED`, exit 1) and passes on the appended correction heading at `079a47c` (day granularity,
    exit 0). ← lessons/round-27-verifier-spotcheck.md:144-145; lessons/round-28.md (M1).

84. A round's last lane batch carries tip receipts of every counter and of the retention scan, measured at the first
    parent of that batch — a commit cannot hold a receipt of its own hash — and the round's report cites every receipt.
    A receipt must live under `.ufo/waves/round-<N>/evidence/` in the tree at the batch, name the counter it ran (or
    `mori-retention-gate.py` for the scan), name the measured revision as the full 40-hex first parent, carry an
    `exit:` line and at least one line of stdout, and be cited by name in a report. Check:
    `bash .ufo/waves/round-28/check-tip-receipts.sh <rev> <round> [--report-repo <dir> --report-rev <rev>]` reads
    every input from committed bytes at named revisions (default reports: the lane's `LOG.md` and the round lesson;
    with `--report-repo/--report-rev`, the fleet `.ufo/reports/round-<N>/mori.md` is also required to cite them).
    Exit 0 when every counter and the retention scan have a cited receipt, 1 otherwise, 2 on a bad revision or usage
    error. It FAILS on round-27 at `df886be1` (no receipt naming parent `9c2c7de9…`, exit 1); a synthetic round-28
    tip batch measured at its parent passes (exit 0). ← lessons/round-27-verifier-spotcheck.md:146-147;
    lessons/round-28.md (M2).
```

## Check scripts

Full, tested source is staged in my scratch dir for the L1 to commit at the lane paths named above:

- `.ufo/waves/round-28/check-heading-time.py` → `/fast/scratch/hyaku/mori-r28/DraftQualityCriteria/check-heading-time.py`
- `.ufo/waves/round-28/check-tip-receipts.sh` → `/fast/scratch/hyaku/mori-r28/DraftQualityCriteria/check-tip-receipts.sh`

Both read committed bytes only (`git show <rev>:<path>`, `git log`), return 0/1/2 per the criteria text, and were
exercised end-to-end below.

## Runs (committed bytes)

### 83 — required FAIL (r27 W1 at df886be1) and PASS (corrected line at 079a47c)

```
$ python3 -I -B .ufo/waves/round-28/check-heading-time.py df886be1 \
    .ufo/waves/round-27/contract.md --heading 'Amendment W1'
heading .ufo/waves/round-27/contract.md:91 stated=2026-10-22T15:55Z granularity=instant \
  added_by=dd4dbb20a601 aI=2026-10-22T12:45:38-03:00 cI=2026-10-22T12:50:10-03:00 \
  bound=2026-10-22T12:50:10-03:00 delta_s=-290 verdict=FUTURE-DATED
headings=1 future_dated=1
exit=1
$ python3 -I -B .ufo/waves/round-28/check-heading-time.py 079a47c \
    .ufo/waves/round-27/contract.md --heading 'Correction to amendment W1'
heading .ufo/waves/round-27/contract.md:101 stated=2026-10-22 granularity=day \
  added_by=079a47c61691 aI=2026-10-22T14:50:48-03:00 cI=2026-10-22T14:56:06-03:00 \
  bound=2026-10-22T14:56:06-03:00 delta_s=0 verdict=ok
headings=1 future_dated=0
exit=0
```

### 83 — the `%aI`-vs-`%cI` conflict (finding F1)

Dispatch asked for an `%aI` comparison. In this jj-colocated lane `%aI` is when the empty change was opened, not when
its content was written (verified: child author time equals parent committer time in 15 of the mori-authored commits
measured, e.g. `126e192d` author 12:50:10-03:00 equals `dd4dbb20` committer 12:50:10-03:00; the round-27 contract's
second correction at `763d346` says the same). Keying the bound to `%aI` false-fires on honest text:

```
$ python3 -I -B .ufo/waves/round-28/check-heading-time.py 763d346 \
    .ufo/waves/round-17/contract.md --heading 'Amendment A1' --bound aI
heading ...:109 stated=2026-10-20 ~16:10 granularity=local-minute added_by=273aa74ab737 \
  aI=2026-10-20T15:26:13-03:00 cI=2026-10-20T16:31:56-03:00 \
  bound=2026-10-20T15:26:13-03:00 delta_s=-2627 verdict=FUTURE-DATED
exit=1      # FALSE POSITIVE on the honest r17 A1 heading
```

The check defaults to the committer bound and exposes `--bound aI` for the literal `%aI` comparison (the W1
failure and the corrected-line pass hold under both bounds). Criterion 83 as drafted names the committer bound for
this reason.

### 84 — required failing run on round 27 (real lane)

```
$ bash .ufo/waves/round-28/check-tip-receipts.sh df886be1 27 \
    --report-repo /home/vgpnk/Projects/shokunin --report-rev ee9adb2
counter=count-c1.sh receipt=MISSING measured=9c2c7de9bc946d5152f69545e9babf6b06f131a1
counter=count-c2.sh receipt=MISSING measured=9c2c7de9bc946d5152f69545e9babf6b06f131a1
retention receipt=MISSING measured=9c2c7de9bc946d5152f69545e9babf6b06f131a1
tip_receipts=unmet
exit=1
```

Passing and negative runs (sandbox clones `git clone --no-hardlinks`): a synthetic round-28 tip batch (parent
`763d3469…`) with the three receipts and lane LOG.md citations exits 0; the same receipts without the report
citation exit 1. Transcripts are in the scratch dir (`sandbox/`, `sandbox3/`, `f49587d` tip batch).

## Findings

- F1 (design, medium): in this jj-colocated lane `%aI` is the change-open time; keying criterion 83 to `%aI`
  false-fires on honest text (r17 A1 heading, measured). The check default is the committer-time bound; `--bound aI`
  reproduces the dispatch's literal `%aI` comparison. Reading: "the time of the commit that ships it".
- F2 (contract wording): `.ufo/waves/round-28/contract.md:69-70` says receipts are "committed for `df886be1` and,
  as the last lane batch, for the round-28 tip"; a batch cannot hold a receipt of its own hash, so criterion 84
  defines the measured revision as the batch's first parent (consistent with `w1/CriticRoutingCoverage.md` RD2/E3).
- F3 (open dependency): `corpus/lessons/round-28.md` does not exist yet; M1 is already attributed to routed defect 1
  by the committed W1 correction at `079a47c`, M2 is assigned to routed defect 2 by convention — the L1 should
  confirm M2 when writing the lesson.

## Behavior, gates, touched surfaces

- Behavior: delivered the two criteria, the two check scripts (scratch, for the L1 to commit), and the
  failing/passing runs; no lane edits beyond this report.
- Gates: exit 0/1/2 semantics per the criteria text; both checks read committed bytes from git objects only.
- Touched surfaces: `corpus/QUALITY.md` (draft only); `.ufo/waves/round-28/w1/DraftQualityCriteria.md` (this
  report); scratch dir `/fast/scratch/hyaku/mori-r28/DraftQualityCriteria/`. No tool installed/upgraded; no
  processes started; no writes outside the scratch dir and this report.
- Out of scope: C1/C2 claim counters, round-28 lesson content, fleet report content.

Report: .ufo/waves/round-28/w1/DraftQualityCriteria.md
