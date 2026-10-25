# ScribeQuality — mori round 47, wave w1 (build + first falsifiers)

Seat: ScribeQuality (leaf; no subagents dispatched). Date: 2026-10-25.
Assignment: draft one new `corpus/QUALITY.md` criterion (registry-pin calibration) citing
`corpus/lessons/round-47.md` M1/M2 and `considerthese/2026-10-25.md` suggestion 1 (opened
2026-10-25), plus a second criterion if justified (stated counts of kernel objects), with exact
proposed text; report to `.ufo/waves/round-47/w1/ScribeQuality.md`.

## Observed evidence (commands, outputs, exit codes)

1. **Contract read** — `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-47/contract.md`
   (HEAD = freeze `63eecf27`, entering `2d85e33`). P-C1 names `SKILL.md:912` pin
   `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` vs committed tool printing `pass=22`;
   P-C2 names the staged "exactly three" claim vs eight `TRACE_EVENT`s in the committed v7.2
   `oom.h` copy.

2. **C1 do-nothing control** (`.ufo/waves/round-47/evidence/control-c1-donothing.txt`):
   `python3 tools/mori-pin-check.py --rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53`
   → `pin line=912 kind=tally prefix=MORI_SOURCES_APPENDONLY_SELFTEST state=mismatch pinned='pass=15 fail=0' observed='pass=22 fail=0' rc=0 cmd='python3 tools/mori-sources-appendonly.py 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --selftest'`,
   then `PIN_CHECK=unmet tally_pins=26 digest_pins=5 mismatches=1 unparsed=0 no_command=0 dropped=0 min_tally_pins=26 rev=2d85e33d14198d388fd3cda9cc15ec07e57e7a53 baseline=yes`, `rc=1`.

3. **Pin-check self-test** (`.ufo/waves/round-47/evidence/selftest-pin-check.txt`):
   `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=22 fail=0`, `rc=0`,
   including arms `stale_tally`, `stale_in_cell_true_elsewhere`, `pin_moved_out_of_cell`,
   `token_boundary_truncated_pin`, `mutant_pin_wrong`, `baseline_row_deleted` — the instrument
   reads pins from the row's own `self-test` cell and fails when the same string sits in another
   cell or anywhere in the row.

4. **C2 three-tracepoints control** (`.ufo/waves/round-47/evidence/control-c2-three-at-freeze.txt`):
   `python3 .ufo/waves/round-47/count-c2.py 63eecf2738db96f46b0bd02b1b2dfd66787493d0 --entry .ufo/waves/round-47/controls/control-c2-three.md`
   → `C2=unmet events=8 rows=3 name_mismatch=5 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=bad provenance=ok rev=63eecf2738db96f46b0bd02b1b2dfd66787493d0 failed=name_mismatch,source_row` ( `rc=1` — the "exactly three" claim as a table mismatches on 5 of 8 events.

5. **considerthese/2026-10-25.md suggestion 1** (verbatim): "Add a registry pin check to my daily
   review. For each `SKILL.md` gate row from the window, compare the pinned sha256 and selftest
   tally against `git show HEAD:<path> | sha256sum` and a real `--selftest` run. Then list any
   mismatch by line number. Today this would have caught `:190` on its own, without relying on the
   closure." File exists at lane root; reflection window ends at HEAD `9834fed4`; dated 2026-10-25.
   Note: the assignment spelled the directory "consideredthemes/"; the repo path is
   `considerthese/2026-10-25.md` (spelling used in drafts below).

6. **Lesson file status**: `corpus/lessons/` (working tree) contains up to `round-46-verifier-spotcheck.md`;
   `corpus/lessons/round-47.md` does **not** exist at report time. M1/M2/M3 citations below are
   therefore prospective — the lesson seat's file must land for the citations to resolve. No
   `round-47.md` exists anywhere under the fleet root (glob found none).

7. **Freeze vs working-tree state** (read-only `git`): HEAD `63eecf27` (freeze) does **not**
   contain the "Criteria added round 47" section. The working tree `corpus/QUALITY.md` *already*
   contains section "Criteria added round 47 — the round-46 routed counter defect, a stale pin, and
   a count the source refutes" with criteria 123 and 124 (see below). Working tree also differs from
   freeze in `SKILL.md` (+15/−1; line 912 now pins `pass=22 fail=0` with a Round47 registry-pin
   reconciler section), `corpus/README.md` (+13), `corpus/SOURCES.md` (+5/−1). These edits predate
   this seat's report (this seat wrote only this report; no production file touched). The L1 should
   reconcile this pre-existing working-tree state with wave outputs.

## Draft 1 — registry-pin calibration criterion (exact proposed text)

```markdown
123. **A registry pin is calibrated only when an instrument re-runs it from committed bytes and reads
    it from its own semantic cell; row-wide substring checks do not qualify.** Lesson:
    `corpus/lessons/round-47.md` M1, M2; `considerthese/2026-10-25.md` suggestion 1 (operator-authored
    reflection, opened 2026-10-25). Rationale: round 46's counter matched needles anywhere in the row
    and turned green with the stale receipt still in the self-test cell
    (`corpus/lessons/round-46-verifier-spotcheck.md` routed defect 1); and `SKILL.md:912` pinned
    `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` while the committed tool printed `pass=22`.
    Check: `python3 tools/mori-pin-check.py --rev <rev> --baseline-rev <entering>` exits 0 before a
    round that edits a registry row or a registered tool lands. Shown able to fail: at the round-47
    entering tip `2d85e33` it prints `PIN_CHECK=unmet … mismatches=1` (line 912), and the committed
    controls for a deleted row, a moved-cell receipt and a truncated pin each stay unmet
    (`.ufo/waves/round-47/evidence/control-c1-*.txt`). Not covered: line-count pins and truncated
    digests.
```

## Draft 2 — stated kernel-object count criterion (exact proposed text; justified)

Justification: the P-C2 surface is a knowledge entry state a count ("exactly three" tracepoints)
refuted by the pinned source (eight `TRACE_EVENT`s). A count claim is only falsifiable when the
enumerating command and source are pinned, so the criterion is warranted and mirrors M3.

```markdown
124. **A stated count of kernel objects carries the enumerating command over a pinned source.**
    Lesson: `corpus/lessons/round-47.md` M3. Rationale: the staged assimilation entry
    `oom-tracing-tracepoints-r42.md` headlined "exactly three named tracepoints" from a paper whose
    own sentence says "such as"; the v7.2 header defines eight (`grep -c '^TRACE_EVENT('` → 8).
    Check: "exactly N", "the N …" or "only" about kernel events, fields, files or knobs is admitted
    only with the command that enumerates them in the cited revision's bytes. Shown able to fail:
    `.ufo/waves/round-47/controls/control-c2-three.md` scores `name_mismatch=5` under `count-c2.py`
    at the freeze commit (`evidence/control-c2-three-at-freeze.txt`).
```

## Findings for the L1

- Both drafts' text matches the equivalent section already present in the working-tree
  `corpus/QUALITY.md` (lines after 1022, criteria 123–124). This seat did not author those working-tree
  lines; L1 should decide whether they came from an earlier attempt or an in-flight integration and
  treat them as reconciled with these drafts.
- `corpus/lessons/round-47.md` (M1/M2/M3) did not exist at report time; the drafts cite it as the
  round's lesson deliverable.
- Directory spelling: `considerthese/` (repo) vs "consideredthemes/" (assignment); suggestion 1 and
  the "opened 2026-10-25" tag confirmed.

## Out of scope

- No production files edited by this seat (read-only git; no installs; no lane tools run; no host
  state touched; no subagents).
- `SKILL.md`, `SOURCES.md`, `README.md`, `corpus/` changes observed in the working tree are L1
  territory; not reviewed here.

## Artifacts

- This report: `.ufo/waves/round-47/w1/ScribeQuality.md`
- Evidence read: `.ufo/waves/round-47/evidence/control-c1-donothing.txt`, `selftest-pin-check.txt`,
  `control-c2-three-at-freeze.txt`
- Sources read: `considerthese/2026-10-25.md`, `.ufo/waves/round-47/contract.md`,
  `corpus/QUALITY.md` (freeze via `git show HEAD:` and working tree)
