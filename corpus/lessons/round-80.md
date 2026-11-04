# Round 80 — mori (L1 MoriR80): three claims — calibration sweep, mutation-counter arms, instrument coverage

author: mori L1 (MoriR80); wave-w1 lesson draft by Mo80S03Lesson
round: 80
date: 2026-11-04
entering: `d58889220d3c6a18d461f2d31b5ab162ffef1e4e`

Axes: C1 calibration, C2 operability, C3 coverage. The frozen authority is
`.ufo/waves/round-80/contract.md`; this lesson does not change its predicates.
The round rules out do-nothing as sufficient: the entering controls in
`.ufo/waves/round-80/evidence/controls-r80.txt` show the sweep tool absent
(`git cat-file -e` rc 128), C1 unmet rc 1, two surviving C2 mutants rc 1,
and C3 naming only 14 of 55 instruments, missing 41, extra 0, rc 1.
These are inherited control receipts, not checks rerun by this lesson seat.
They establish absent after-states, not a landed result.

The contract's introductory C3 claim says “15 of 55”; its frozen P-C3 and
controls say “named=14 present=55 missing=41 extra=0”. Likewise C2's headline
says “from 3 of 6”, while P-C2 and controls measure survivors=2 killed=4.
Those conflicting statements are retained here verbatim in substance; the
frozen measured predicates govern, not the introductory shorthand.

LANDING PENDING — filled by the L1: landed revision, exact frozen-counter
commands/output/exit codes for C1/C2/C3, and receipt paths. No claim is marked
met by this draft, and no axis score changes.

## Gate

### S595 — mutation analysis, abstract only

- URL: https://arxiv.org/abs/2102.11378v2 — “Practical Mutation Testing at Scale”.
- Access date: 2026-11-04.
- Located quote, pinned HTML line 121 (22 words): “Mutation analysis assesses a test suite&#39;s adequacy by measuring its ability to detect small artificial faults, systematically seeded into the tested program.”
- Pin: `corpus/evidence/sources-r80/arXiv-2102.11378v2-abs.html`.
- sha256: **PIN PENDING — filled by the L1**. The source seat's report
  `.ufo/waves/round-80/w1/Mo80Sc02Source.md` was not yet present when this scaffold
  was drafted; no digest is invented here.
- Pre-fetch duplicate sweep: source seat Mo80Sc02Source reports that searches of
  `corpus/SOURCES.md` for the exact URL, `2102.11378`, and case-insensitive
  `mutation test` each returned rc 1, no matches. The wider `mutation` search
  hit S350 (host mutation) and S563 (label-mutation arm), neither this source;
  the last row was S594. **DUPLICATE RECEIPT PENDING — filled by the L1**:
  bind those reported commands/results to the source report's durable receipt.
  These are source-seat observations, not a sweep performed by this lesson seat.
- Verdict: **admitted, scope narrowed** to the abstract's definition of mutation
  analysis, grounding C2's test-suite-adequacy criterion. This is the bounded
  Gate disposition, not proof of a landed source row or a passing C2 counter.
  No equivalent-mutant theory, Python implementation guarantee, production
  reliability, or inference that an unmutated green selftest is adequate is admitted.
  Intended entry: `corpus/knowledge/mutation-adequacy-r80.md`.

## Mistakes

### D79-1 — a corrected fact left standing in a sibling carrier

- **Class:** correction-sweep / spot-check disagreement, not a newly invented
  mistake. SKILL's registry said 19 selftest arms while SCORECARD's capability
  row still said 18 after the tool grew an arm.
- **Evidence pointer:** `corpus/lessons/round-79-verifier-spotcheck.md:98`
  identifies the stale `SCORECARD.md:4016` row and its stale `18/18` evidence-cell
  wording; `SKILL.md:1365` records `CONTROL_RECEIPT_SELFTEST pass=19 fail=0`.
  The r80 entering control receipt retains the disagreement and its command.
- **Captured-by:** the r79 non-author spot-check's routed D79-1; the round's C1
  sweep turns that correction-sweep class into a repeatable gate.
- **Fix:** land `tools/mori-claim-sweep.py`, its frozen pins and gate registry
  row 14; correct the control-receipt capability row and evidence-cell tally
  with a named correction. The sweep checks graded pointers, pinned live
  selftest tallies and stale literals rather than trusting one corrected file.
  Fix status is LANDING PENDING, not asserted complete by this lesson draft.

Shown able to fail, inherited entering bytes (not a new execution by this seat):

```text
$ grep -c 'selftest 18 in-memory cases' SCORECARD.md
1
rc=0
$ python3 -I .ufo/waves/round-80/count-c1.py d5888922
C1=unmet tool=absent sweep=- mismatches=- row_tally=- live_tally=- rev=d58889220d3c
rc=1
```

The same frozen counter is the red-to-green command:
`python3 -I .ufo/waves/round-80/count-c1.py <revision>` (from the lane root).
It is red at entering as pasted above; only the L1's landed-revision run can
establish green. GREEN RECEIPT PENDING — filled by the L1: exact revision,
output, rc and receipt. Required green includes a present tool, zero sweep
mismatches, and capability/live tallies both 19; a proposed output is not evidence.
The sweep's own invocation is `python3 -I tools/mori-claim-sweep.py --root
<export-of-revision> --pins .ufo/waves/round-80/claim-pins.json`, as frozen in P-C1.

Only this one mistake is mined: no second round-local mistake is invented to
inflate the lesson count.

## Census

Executed by Mo80S03Lesson over the live lane registry during wave w1, before
any S595 row was observed in that registry (not an export of a landed revision):

```text
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
mori\tW04\tS035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in across scopes
[additional W04 duplicate-URL warnings; full output retained in .ufo/waves/round-80/w1/Mo80S03Lesson.md]
mori\tok\t/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
exit=0
$ grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
367
exit=0
```

The displayed census excerpt spells tab separators as `\t`; it is not a
byte-exact full transcript. Census rc 0 does not mean no warnings.
Before row count: 367. AFTER CENSUS PENDING — filled by the L1: after-value,
landed tree/revision, census command/output/rc and final receipt path. The
expected new S595 row is not counted as landed merely because it is planned.

## Refusals

- `merge/mori/` assimilation remains closed behind the r61 L0: 94/136 staged
  ids collide; adopting package rows without document-keyed reconciliation
  would convert collisions into false coverage. No package adoption is claimed.
- The boot-scoped events window remains behind mori | round-65; any
  SOURCES-wide word-count/label sweep remains behind mori | round-73.
  This round routes around those L0s; this lesson does not claim a new
  operator ruling or broaden a vendor-scoped drift grammar (QUALITY 159).
- Do not touch `tools/mori-control-receipt.py`'s selftest: it is now a registered,
  tally-pinned instrument. The r79 D79-5 asks for permission-denial and full
  `--dir` cases **when the selftest is next touched**, not as an unconditional
  r80 change. Correct the stale carrier and add the separate sweep instead.
  The receipt guard proves textual command/count co-presence, not command
  relevance or semantic correctness (r79 D79-4; QUALITY 164).
- No axis score changes: no closure states a new number. C1 calibration,
  C2 operability and C3 coverage are capability/predicate claims, not permission
  to raise scalar scores. Detection/report only; no remediation, OS/unit-state
  change, credential handling or orchestration takeover.
