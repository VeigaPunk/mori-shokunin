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

Landed revision `8108dfcc00d8b680cd4fb03cd9a6cc6dd5a74a77` (branch `master`). The
three frozen counters, run by the L1 from the lane root with
`HYAKU_SCRATCH=/fast/scratch/hyaku/mori-r80`, at that revision:

```text
$ python3 -I .ufo/waves/round-80/count-c1.py 8108dfcc00d8b680cd4fb03cd9a6cc6dd5a74a77
C1=met tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19 rev=8108dfcc00d8
rc=0
$ python3 -I .ufo/waves/round-80/mutate-c2.py --rev 8108dfcc00d8b680cd4fb03cd9a6cc6dd5a74a77
unmutated survived rc=0 C2_COUNTER_SELFTEST pass=7 fail=0
mutant drop_admitted killed rc=1 C2_COUNTER_SELFTEST pass=6 fail=1
mutant raise_ceiling killed rc=1 C2_COUNTER_SELFTEST pass=5 fail=2
mutant count_other_verdicts killed rc=1 C2_COUNTER_SELFTEST pass=5 fail=2
mutant cut_clause_boundary killed rc=1 C2_COUNTER_SELFTEST pass=6 fail=1
mutant any_round_in_cell killed rc=1 C2_COUNTER_SELFTEST pass=4 fail=3
mutant met_ignores_mismatch killed rc=1 C2_COUNTER_SELFTEST pass=2 fail=5
MUTATION_C2 survivors=0 killed=6 total=6 unmutated=green rev=8108dfcc00d8
rc=0
$ python3 -I .ufo/waves/round-80/count-c3.py 8108dfcc00d8b680cd4fb03cd9a6cc6dd5a74a77
C3=met named=56 present=56 missing=0 extra=0 rev=8108dfcc00d8
rc=0
```

Do-nothing controls stay valid: at `d5888922` C1 reads `tool=absent` rc 1, the harness reads
`survivors=2` and C3 reads `named=14 present=55 missing=41` rc 1
(`.ufo/waves/round-80/evidence/controls-r80.txt`). No axis score changes; the verdicts are the
round report's.

## Gate

### S595 — mutation analysis, abstract only

- URL: https://arxiv.org/abs/2102.11378v2 — “Practical Mutation Testing at Scale”.
- Access date: 2026-11-04.
- Located quote, pinned HTML line 121 (22 words): “Mutation analysis assesses a test suite&#39;s adequacy by measuring its ability to detect small artificial faults, systematically seeded into the tested program.”
- Pin: `corpus/evidence/sources-r80/arXiv-2102.11378v2-abs.html`.
- sha256: `28ea1f163860348979a3aa9e9ef8e00fc8eb3ecec2762782d639783003f1b884`,
  43884 bytes / 613 lines, measured by the L1 with `sha256sum` and `wc -lc` on the
  committed pin at `8108dfcc`; the source seat's own two fetches were byte-identical.
  The same sentence also appears in the page's meta description tags at `:28` and
  `:32`, so an anchor checker demanding one occurrence refuses this page — the anchor
  is the abstract block at `:121`.
- Pre-fetch duplicate sweep: source seat Mo80Sc02Source reports that searches of
  `corpus/SOURCES.md` for the exact URL, `2102.11378`, and case-insensitive
  `mutation test` each returned rc 1, no matches. The wider `mutation` search
  hit S350 (host mutation) and S563 (label-mutation arm), neither this source;
  the last row was S594. Re-run by the L1 against the ENTERING registry
  (`git show d5888922:corpus/SOURCES.md` -> scratch copy, 367 rows):
  `grep -c -F 'arxiv.org/abs/2102.11378'` -> 0; `grep -c -F '2102.11378'` -> 0;
  `grep -ci 'mutation test'` -> 0. No duplicate; S595 is the next unused id.
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
  Fix status: landed at `8108dfcc` and measured by the C1 counter (see the landing block).

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
It is green at the landed revision, the same command and the same counter:

```text
$ python3 -I .ufo/waves/round-80/count-c1.py 8108dfcc00d8b680cd4fb03cd9a6cc6dd5a74a77
C1=met tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19 rev=8108dfcc00d8
rc=0
```

plus the guard's own run over the round's receipts:
`python3 -I tools/mori-control-receipt.py --dir .ufo/waves/round-80/evidence` ->
`CONTROL_RECEIPT_SUMMARY files=1 sections=5 claims=9 unbound=0` rc 0 (before the after-run
receipt was added). The fix's second carrier correction (the row's Evidence cell `18/18`
-> the landed `19/19` with a named supersession) is part of the same landed bytes.
The sweep's own invocation is `python3 -I tools/mori-claim-sweep.py --root
<export-of-revision> --pins .ufo/waves/round-80/claim-pins.json`, as frozen in P-C1.

### The sweep's first arm was over-broad on wildcard citations (this round)

- **Class:** `vacuous` (an arm that fires on a legitimate form), found by the L1's first
  after-run, not by a seat.
- **Evidence pointer:** the run that found it printed
  `CLAIM_SWEEP_MISMATCH unresolved SCORECARD.md:1558 .ufo/waves/round-24/w2/Mut*.md`,
  `:1559 .../c1-*.json` and `:1593 .../routed-r24-*-a5.txt`, all of them evidence-set
  citation patterns, and would have forced either a history rewrite in the r24/r25 sections
  or a false red forever.
- **Captured-by:** the frozen predicate's own after-run at the first landed tool bytes; the
  contract's arm definition said "does not exist under --root", which a pattern token does
  only under a literal reading.
- **Fix:** the tool resolves a token carrying `*`/`?` by globbing at least one existing path
  under `--root` (literal existence is kept for wildcard-free tokens), with two selftest arms
  (match -> clean, no match -> unresolved) and a docstring limit: a match proves the pattern
  is not dead, not that the matched files are the intended ones. Fixed and re-measured at
  `8108dfcc` (`mismatches=0`, `pointers=233`). Two further arms were added the same way after
  the mutation seat killed nothing on the total-summary shape (`mismatches` counting only
  `unresolved` had survived).

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
Before row count: 367. After, run by the L1 at the landed tree (`8108dfcc`, same
command): rc **0**, `mori ok /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`,
no `E` findings, 35 tolerated `W04` duplicate-URL warnings;
`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` -> **368**
(367 -> 368, the one addition being S595). Malformed rows
(`awk -F'|' ... NF!=13`) -> 0.

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
