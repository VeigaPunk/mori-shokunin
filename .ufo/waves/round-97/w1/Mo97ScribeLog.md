# Mo97ScribeLog — scribe: LOG.md and SCORECARD.md draft blocks for round 97 (L1 to integrate)

Seat `Mo97ScribeLog` (scribe), mori round 97 attempt 1, wave `w1`. Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`.
**Nothing was written to `LOG.md` or `SCORECARD.md`** — this file holds the two draft blocks only. No git/jj mutation
was run (read-only `rev-parse`/`log`/`show`/`diff`/`ls-tree`/`archive` only, always `git -C <absolute lane path>`).
No host sysctl, kernel setting, service or user limit was touched. No tool was installed or upgraded (none needed;
`pacman` was not invoked).

Revisions used: entering `973b2af11f41bd362163d7e29ac08286832f546b`; freeze
`dd1ae1150f53df54e7530311b2323368e3c0e5e9` (contract + counters + pre-freeze controls); landing
`e85ed91249953094b067554bfa79fcdc65791f8e` (the claimed work).

## 1. What this seat did

1. Re-read the frozen contract, both frozen counters (docstrings = the predicates), the four receipts
   (`before-c1.txt`, `before-c2.txt`, `landing-c1.txt`, `landing-c2.txt`), the controls receipt, the lesson
   (`corpus/lessons/round-97.md`), the tail of `LOG.md` (round 88→96 entries) and the round-96 SCORECARD section.
2. Re-ran **both frozen counters myself** at both revisions from scratch archives (independent of the receipts),
   plus the registry auditor, the digest gate, the census, and the pinned-byte hashes (§4).
3. Drafted the two integration blocks (§6 = LOG.md entry, §7 = SCORECARD.md section), quoting only bytes that exist
   on disk. **No score move is claimed.**

## 2. Files read (all read-only)

`.ufo/waves/round-97/contract.md`, `count-c1.py`, `count-c2.py`, `evidence/{controls-r97,before-c1,before-c2,landing-c1,landing-c2}.txt`,
`corpus/lessons/round-97.md`, `corpus/lessons/round-96.md`, `corpus/lessons/round-95.md`, `LOG.md` (tail), `SCORECARD.md`
(round-96 section), `SKILL.md` (r97 registry section), `corpus/SOURCES.md` (S615/S616/S619/S623/S628 rows),
`corpus/evidence/sources-r97/*`, `tools/mori-gate-registry.py`, `tools/mori-source-digest.py`,
`.ufo/waves/round-97/w1/*.md` (peer seat reports), `.ufo/waves/round-97/w1-dispatch.json`, `.ufo/waves/round-97/w1-validator.out`.

## 3. Receipts copied (verbatim, as cited)

`evidence/before-c1.txt`:

```
$ (entering) count-c1.py --root DIR  rev=973b2af11f41bd362163d7e29ac08286832f546b date=2026-11-05T20:50:06Z
TARGET tools/mori-cgroup-pressure.py unattributed
TARGET tools/mori-drift-recheck.py unattributed
TARGET tools/mori-scorecard-calibration.py unattributed
TARGET tools/mori-source-digest.py unattributed
C1=unmet unregistered=4 registry=unmet targets_ok=0/4 checks_failed=registry,target_mori-cgroup-pressure.py,target_mori-drift-recheck.py,target_mori-scorecard-calibration.py,target_mori-source-digest.py root=/fast/scratch/hyaku/mori-r97/l1/enter
exit=1
```

`evidence/landing-c1.txt`:

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive e85ed91249953094b067554bfa79fcdc65791f8e | tar -x -C DIR && python3 .ufo/waves/round-97/count-c1.py --root DIR   # rev=e85ed91249953094b067554bfa79fcdc65791f8e count-c1.sha256=78a09016fa8151b72049400600b6b154437c919df6fccb55b8bfa6253b4d2a95 date=2026-11-05T20:50:04Z
TARGET tools/mori-cgroup-pressure.py row='cgroup PSI survey (r62 tool, registry r97)' selftest_rc=0 selftest_line='MORI_CGROUP_PRESSURE_SELFTEST: pass=12 fail=0' stated_in_cell=yes token_in_verdict_map=yes
TARGET tools/mori-drift-recheck.py row='drift re-check (r66 tool, registry r97)' selftest_rc=0 selftest_line='MORI_DRIFT_RECHECK_SELFTEST: PASS (10 cases)' stated_in_cell=yes token_in_verdict_map=yes
TARGET tools/mori-scorecard-calibration.py row='SCORECARD Last-change calibration counter (r96 tool, registry r97)' selftest_rc=0 selftest_line='CALIB_SELFTEST pass=11 fail=0' stated_in_cell=yes token_in_verdict_map=yes
TARGET tools/mori-source-digest.py row='SOURCES digest check (r91 tool, registry r97)' selftest_rc=0 selftest_line='DIGEST_SELFTEST pass=11 fail=0' stated_in_cell=yes token_in_verdict_map=yes
C1=met unregistered=0 registry=met targets_ok=4/4 checks_failed=- root=/fast/scratch/hyaku/mori-r97/l1/land
exit=0
```

`evidence/before-c2.txt`:

```
$ (entering) count-c2.py --root DIR  rev=973b2af11f41bd362163d7e29ac08286832f546b date=2026-11-05T20:50:06Z
TARGET S615 unpinned copy=- copy_sha=-
TARGET S616 unpinned copy=- copy_sha=-
TARGET S623 unpinned copy=- copy_sha=-
LIVE S615 no-copy
LIVE S616 no-copy
LIVE S623 no-copy
C2=unmet mismatch=0 unpinned=3 targets_ok=0/3 hole_guard=n/a live=S615:no-copy,S616:no-copy,S623:no-copy checks_failed=unpinned,target_S615,target_S616,target_S623,live root=/fast/scratch/hyaku/mori-r97/l1/enter
exit=1
```

`evidence/landing-c2.txt`:

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive e85ed91249953094b067554bfa79fcdc65791f8e | tar -x -C DIR && python3 .ufo/waves/round-97/count-c2.py --root DIR   # rev=e85ed91249953094b067554bfa79fcdc65791f8e count-c2.sha256=957a7be605ba920734a218388b7ebb50f4f829979931c6e4193caee2149a1e91 date=2026-11-05T20:50:05Z
TARGET S615 superseded-by S619 successor_ok=yes copy_equals_successor=yes copy=corpus/evidence/sources-r97/S615.html copy_sha=7891c58897fe9f78
TARGET S616 ok copy_matches_tool=yes copy=corpus/evidence/sources-r97/S616.html copy_sha=6842ed0f53882c5a
TARGET S623 ok copy_matches_tool=yes copy=corpus/evidence/sources-r97/S623.html copy_sha=90ac3b25cb2dd281
LIVE S615 time-churn as-of=2026-11-05T20:50:05Z
LIVE S616 time-churn as-of=2026-11-05T20:50:05Z
LIVE S623 time-churn as-of=2026-11-05T20:50:05Z
C2=met mismatch=0 unpinned=0 targets_ok=3/3 hole_guard=pass live=S615:time-churn,S616:time-churn,S623:time-churn checks_failed=- root=/fast/scratch/hyaku/mori-r97/l1/land
exit=0
```

`evidence/controls-r97.txt` (headline only): `CONTROLS rev=973b2af11f41bd362163d7e29ac08286832f546b
count-c1.sha256=78a09016fa8151b72049400600b6b154437c919df6fccb55b8bfa6253b4d2a95
count-c2.sha256=957a7be605ba920734a218388b7ebb50f4f829979931c6e4193caee2149a1e91 date=2026-11-05T20:47:49Z` … final line
`CONTROLS_DONE unexpected=0` (do-nothing C1 `rc=1` / `C1=unmet unregistered=4`; do-nothing C2 `rc=1` / `unpinned=3`;
three C1 forgery controls `rc=1`; three C2 forgery controls `rc=1`; two positive controls `rc=0`; every block ends
`OBSERVED rc=… -> AS_EXPECTED`).

## 4. My own verification (this seat's commands, exact outputs)

Scratch: `S=$HYAKU_SCRATCH/mori-r97/Mo97ScribeLog` (`/fast/scratch/hyaku/mori-r97/Mo97ScribeLog`), `TMPDIR="$S"`,
archives materialised with `git -C <lane> archive <rev> | tar -x -C DIR`; the scratch tree was removed on exit.

```
$ sha256sum .ufo/waves/round-97/count-c1.py .ufo/waves/round-97/count-c2.py
78a09016fa8151b72049400600b6b154437c919df6fccb55b8bfa6253b4d2a95  count-c1.py
957a7be605ba920734a218388b7ebb50f4f829979931c6e4193caee2149a1e91  count-c2.py
$ git cat-file blob e85ed912:.ufo/waves/round-97/count-c1.py | sha256sum   # same two hashes at the landing rev
$ git rev-parse --verify 973b2af1^{commit}  dd1ae115^{commit}  e85ed912^{commit}   # all three resolve
```

Counter replay (mine, both revisions, both claims) — **reproduces the receipts line for line, including exit codes**:

```
$ (entering) count-c1.py --root $S/enter
C1=unmet unregistered=4 registry=unmet targets_ok=0/4 checks_failed=registry,target_mori-cgroup-pressure.py,target_mori-drift-recheck.py,target_mori-scorecard-calibration.py,target_mori-source-digest.py root=…/enter
exit=1
$ (entering) count-c2.py --root $S/enter
C2=unmet mismatch=0 unpinned=3 targets_ok=0/3 hole_guard=n/a live=S615:no-copy,S616:no-copy,S623:no-copy checks_failed=unpinned,target_S615,target_S616,target_S623,live root=…/enter
exit=1
$ (landing) count-c1.py --root $S/land
C1=met unregistered=0 registry=met targets_ok=4/4 checks_failed=- root=…/land
exit=0
$ (landing) count-c2.py --root $S/land
C2=met mismatch=0 unpinned=0 targets_ok=3/3 hole_guard=pass live=S615:time-churn,S616:time-churn,S623:time-churn checks_failed=- root=…/land
exit=0
```

Registry auditor (the C1 leg (a) surface), at both revisions:

```
$ (entering) python3 tools/mori-gate-registry.py --rev WORK --repo $S/enter --audit-all
audit tools/mori-cgroup-pressure.py            FAIL (no row names tools/mori-cgroup-pressure.py)
audit tools/mori-drift-recheck.py              FAIL (no row names tools/mori-drift-recheck.py)
audit tools/mori-scorecard-calibration.py      FAIL (no row names tools/mori-scorecard-calibration.py)
audit tools/mori-source-digest.py              FAIL (no row names tools/mori-source-digest.py)
tables=16
registered=61 unregistered=4 no_selftest=0 duplicate=0 wrong_row=0 tables=16
REGISTRY=unmet
exit=1
$ (landing) python3 tools/mori-gate-registry.py --rev WORK --repo $S/land --audit-all
audit tools/mori-cgroup-pressure.py            PASS row='cgroup PSI survey (r62 tool, registry r97)' (8 cells, entry resolves, --selftest argv branch)
audit tools/mori-drift-recheck.py              PASS row='drift re-check (r66 tool, registry r97)' (8 cells, entry resolves, --selftest argv branch)
audit tools/mori-scorecard-calibration.py      PASS row='SCORECARD Last-change calibration counter (r96 tool, registry r97)' (8 cells, entry resolves, --selftest argv branch)
audit tools/mori-source-digest.py              PASS row='SOURCES digest check (r91 tool, registry r97)' (8 cells, entry resolves, --selftest argv branch)
tables=17
registered=65 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0 tables=17
REGISTRY=met
exit=0
```

Digest gate (C2 leg (a) surface) and the pinned bytes:

```
$ (landing) python3 tools/mori-source-digest.py corpus/SOURCES.md corpus/evidence
DIGEST S615 superseded-by S619
DIGEST S616 ok recorded=6842ed0f53882c5a4d7a852ff969842f62aba92f918e2192db0df6ed23c3cb72 actual=6842ed0f53882c5a4d7a852ff969842f62aba92f918e2192db0df6ed23c3cb72
DIGEST S619 ok recorded=7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b0f83b9a8a42f5 actual=7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b0f83b9a8a42f5
DIGEST S623 ok recorded=90ac3b25cb2dd28192a5d1c7d45da5ef966d32666d0c583a13eb2ec6f4831ad0 actual=90ac3b25cb2dd28192a5d1c7d45da5ef966d32666d0c583a13eb2ec6f4831ad0
DIGEST S628 ok recorded=0ae6b8806cbb28edd4f8b1ae98ac5045ced71234ba8c81dfa3bf7312eccac618 actual=0ae6b8806cbb28edd4f8b1ae98ac5045ced71234ba8c81dfa3bf7312eccac618
DIGEST_CHECK rows=125 ok=92 mismatch=0 superseded=2 prefix_only=31 unpinned=0
exit=1            # exit 1 is the 31 standing prefix_only rows, out of scope by the contract
$ sha256sum corpus/evidence/sources-r97/{S615.html,S616.html,S623.html,S628.md}
7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b0f83b9a8a42f5  S615.html   (362493 B)
6842ed0f53882c5a4d7a852ff969842f62aba92f918e2192db0df6ed23c3cb72  S616.html    (53982 B)
90ac3b25cb2dd28192a5d1c7d45da5ef966d32666d0c583a13eb2ec6f4831ad0  S623.html   (171073 B)
0ae6b8806cbb28edd4f8b1ae98ac5045ced71234ba8c81dfa3bf7312eccac618  S628.md       (6835 B)
```

Census (the lesson's frontier-step command, run on the working tree == landing bytes for `corpus/SOURCES.md`):

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
mori	W04	S622 duplicate url git-scm.com/docs/git-log across scopes
… (43 W04 rows in total) …
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
exit=0
```

Registry sizes (census `rows` metric): entering `399` → landing `400` (S628 added; tier.B 19 → 20).

S623 pin provenance, checked by this seat independently of the peer reports (one live fetch, read-only):

```
$ curl -sS --max-time 60 -A "curl/8.21.0" -o live-cmdline.html https://docs.python.org/3/using/cmdline.html
171073 bytes, sha256 57b7f76ba01d888cecf61e184cc2dfddd148b31716284e71f44a92df6d0e6811
stamp lines: [b'      Last updated on Nov 05, 2026 (12:47 UTC).']
replace that one line with "Last updated on Nov 05, 2026 (08:02 UTC)."
reconstructed sha256: 90ac3b25cb2dd28192a5d1c7d45da5ef966d32666d0c583a13eb2ec6f4831ad0
recorded digest    : 90ac3b25cb2dd28192a5d1c7d45da5ef966d32666d0c583a13eb2ec6f4831ad0
MATCH: True
```

So the S623 pin is today's live body with one stamp line restored — bit-for-bit the recorded fetch, not a stand-in.

## 5. Findings for the L1 (not repairs — nothing here was changed)

**F1 — lesson census count is off by one (a count stated without the row it counts; the lesson text is landed at
`e85ed912` and this seat did not edit it).** `corpus/lessons/round-97.md` §Frontier step says the census-before run
gave "`mori ok`, **42 W04**". The same command on the same lane prints **43** W04 rows, and it printed 43 at the
entering revision too, so the delta is not this round's row:

**Confirmed by the lane's own committed receipts (added after this seat's first pass; the L1's commits
`5497e6f7` and `b6d03408` landed after my seat finished).** `.ufo/waves/round-97/evidence/census-before.txt` and
`census-after.txt`, both committed in `b6d03408`, each contain **43** `W04` rows and end `mori ok` / `exit=0`:

```
$ git show b6d03408:.ufo/waves/round-97/evidence/census-before.txt | grep -cP '\tW04\t'   -> 43
$ git show b6d03408:.ufo/waves/round-97/evidence/census-after.txt  | grep -cP '\tW04\t'   -> 43
$ git show b6d03408:.ufo/waves/round-97/evidence/census-after.txt | tail -2
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
exit=0
$ git show b6d03408:.ufo/waves/round-97/evidence/census-after.txt | grep -P '\tW04\t' | tail -1
mori	W04	S622 duplicate url git-scm.com/docs/git-log across scopes
```

So the committed receipts and the committed lesson **disagree with each other**: the receipts say 43, the lesson's
prose says 42. The receipt is the command's own output; the prose is the count. The committed
`## Planned (round 98)` list in `SCORECARD.md` has four items and does not mention this. Correction-of-record
candidate for the closure; no claim impact (neither C1 nor C2 reads the census count).

My own measurement, taken before those receipts existed:

```
$ scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori | awk -F'\t' '$2=="W04"{n++} END{print n}'
43
$ for rev in 66c5518e 973b2af1 e85ed912; do … --file <that rev's SOURCES.md> … ; done
66c5518e W04=43
973b2af1 W04=43
e85ed912 W04=43
```

The 43rd row is **S622** (`git-scm.com/docs/git-log`, present since the round-93 landing `aade1775`; the diff of the
W04 sets between `9dce2ca6` (42) and `aade1775` (43) is exactly that one row). The new row **S628 produces no W04
row** (its URL is unique; `grep -c 'S628'` on the census output = 0). Two consequences: (a) the lesson's `42 W04`
is wrong against its own command — the count is 43 before and after; (b) `w1/Mo97RevC2.md` §5, which explains the
43rd row as "the 42 before the round + the new S628 row", mis-attributes it to S628 — the before-count was already
43. The lesson's census **exit 0** claim stands (measured: exit 0, `mori ok`). This is a counting-attribution defect
of the same family as the r96 lesson's `unpinned=3` slip (r96 Mistake 2), and it is a **correction-of-record**
candidate for the L1, not a claim impact: neither C1 nor C2 reads the census count.
**Status: still open, and now visible inside the lane's own committed bytes.** At the final revision
`b6d03408` the lesson still reads "`mori ok`, 42 W04" (`corpus/lessons/round-97.md`, §Frontier step) while the
census receipts committed in the same commit (`evidence/census-before.txt`, `evidence/census-after.txt`) each hold
43 W04 rows. The concurrent edit that fixed F2 left this count untouched, and the committed
`## Planned (round 98)` list in `SCORECARD.md` does not mention it.

**F2 — the S628 quote word count was 12, not 14 (CORRECTED and now committed).** At the landing commit
`e85ed912`, `corpus/lessons/round-97.md` §Gate said the located quote is "14 words"; the pinned copy's raw lines 6-7
are 12 whitespace-separated tokens
(`This repository contains scripts for automatically building the Python documentation on [docs.python.org](https://docs.python.org).`).
The ≤25-word rule was still met; only the stated count was wrong. Independently reported by `w1/Mo97RevC2.md` §4
nit 1 and `w1/Mo97ScoutLive.md`. **Status: fixed.** The committed lesson at `b6d03408` now reads "12 words by `wc -w`
— the first draft of this cell said 14, corrected after seat Mo97ScoutLive §3b", and the lesson carries a
`quote-length label not counted` mistake row naming the 14-vs-12 slip with the QUALITY 90 ground. Closed; no claim
impact.

**F3 — the L1's own `SCORECARD.md`/`SKILL.md`/lesson edits are now committed (not mine).** At the time of this
seat's first pass `git status --porcelain` showed ` M SCORECARD.md`, ` M SKILL.md` and
` M corpus/lessons/round-97.md` at HEAD `e85ed912` — the L1's draft integration, plus the registry-cell corrections
(the cgroup row's `--group` note and the drift row's `unresolved` class). **I checked that the `SKILL.md` edit does
not break C1**: with the worktree `SKILL.md` substituted into the landing tree, the frozen counter still read
`C1=met unregistered=0 registry=met targets_ok=4/4` (exit 0). Those edits are committed in `5497e6f7`; the working
tree is now clean at `b6d03408`. I did not make or attribute any of them.

**F4 — wave state (final).** Dispatch `w1-dispatch.json`: 14 seats (2 scout, 2 executor, 2 reviewer,
2 critic, 3 mutation-tester, 1 connector, 1 revenger, 1 scribe; attack seats 7 of 14 by the lane's convention —
reviewer + critic + mutation-tester, as in r93 6/12 and r94 6/12; the revenger seat is not counted). Validator rc 0
(`w1-validator.out`: `validator rc=0 (stderr empty); dispatch=w1-dispatch.json tasks=14`). At 18:07 local, 13 report
files were on disk in `.ufo/waves/round-97/w1/` (12 peers plus this one); `Mo97ScoutConsider` had not yet written its
report file. **All 14 report files are now present** and are committed in `5497e6f7`; the working tree is clean at
`b6d03408`. `w1-results.json` is not in the wave directory — that is the orchestrator-owned file (r96 routed defect
3, not lane-editable), so no seat-level settlement is mine to read.

**F5 — the L1's integration was already in the worktree while this seat drafted; it is now committed.** At
18:07–18:09 local, `git status` showed ` M LOG.md`, ` M SCORECARD.md`, ` M SKILL.md` and
` M corpus/lessons/round-97.md` (all uncommitted, at HEAD `e85ed912`), i.e. the L1 had already written its own
`## Round 97 — 2026-11-05 …` LOG entry and `## Round 97 verdict …` SCORECARD section before this seat's drafts
existed. **The L1 reconciled rather than double-appended**: the committed `SCORECARD.md` carries one
`## Round 97 verdict` section and one four-item `## Planned (round 98)` list (`5497e6f7`), and the committed
`LOG.md` carries one round-97 entry. The two texts agree on every measured value (C1 `unmet unregistered=4 …` →
`met unregistered=0 … targets_ok=4/4`; C2 `unmet … unpinned=3` → `met … targets_ok=3/3 hole_guard=pass`; no score
move; both verdicts left to the closure). The committed list differs from my draft §7 in that it does not carry the
census-count correction (F1). My draft blocks in §6 and §7 stand as the alternative formulation the L1 may draw on;
nothing in them contradicts the committed text.

**F6 — the final committed revision re-measures both claims as met (confirmation, not a new claim).** The L1's
`b6d03408` adds `evidence/final-c1.txt` and `evidence/final-c2.txt`, measured at the post-correction revision
`5497e6f7` (the landing plus the registry cell corrections):

```
$ git show b6d03408:.ufo/waves/round-97/evidence/final-c1.txt | grep -E '^C1='
C1=met unregistered=0 registry=met targets_ok=4/4 checks_failed=- root=/fast/scratch/hyaku/mori-r97/l1/final
exit=0
$ git show b6d03408:.ufo/waves/round-97/evidence/final-c2.txt | grep -E '^C2='
C2=met mismatch=0 unpinned=0 targets_ok=3/3 hole_guard=pass live=S615:time-churn,S616:time-churn,S623:time-churn checks_failed=- root=/fast/scratch/hyaku/mori-r97/l1/final
exit=0
```

Both final receipts carry the same counter sha256 pins as the freeze (`78a09016…d2a95`, `957a7be6…9a1e91`), so the
post-landing registry-cell corrections did not move either verdict. The four receipts I quoted in §3
(`before-c1.txt`, `before-c2.txt`, `landing-c1.txt`, `landing-c2.txt`) are byte-identical to the versions committed
in `5497e6f7` — I re-checked their `C1=`/`C2=` lines against the committed blobs at `b6d03408`.

## 6. Draft block 1 — LOG.md entry (append at end of `LOG.md`; L1 to integrate)

```markdown
## Round 97 — 2026-11-05 (L1 MoriR97, attempt 1)

Two claims, frozen at `dd1ae115` before any wave output (`.ufo/waves/round-97/contract.md`; counters `count-c1.py`
sha256 `78a09016…d2a95`, `count-c2.py` sha256 `957a7be6…9a1e91`; pre-freeze controls `evidence/controls-r97.txt`,
`CONTROLS_DONE unexpected=0`). Entering `973b2af1`; landing `e85ed912`.

- **C1 operability (score 7) — the gate registry states the outcome of four unregistered gates.** The r96 closure's
  routed defect 1 (`corpus/lessons/round-96-verifier-spotcheck.md:141-144`) and the lane's own auditor named four
  tools that ran as gates with no row at the registry home `SKILL.md`. The landing appends four rows to `SKILL.md`
  (`cgroup PSI survey (r62 tool, registry r97)`, `drift re-check (r66 tool, registry r97)`, `SCORECARD Last-change
  calibration counter (r96 tool, registry r97)`, `SOURCES digest check (r91 tool, registry r97)`); no earlier byte of
  `SKILL.md` is edited and no `tools/` byte changes. Command: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin
  archive <rev> | tar -x -C DIR && python3 .ufo/waves/round-97/count-c1.py --root DIR`. Before (entering `973b2af1`,
  `evidence/before-c1.txt`): `C1=unmet unregistered=4 registry=unmet targets_ok=0/4`, exit 1. After (landing
  `e85ed912`, `evidence/landing-c1.txt`): `C1=met unregistered=0 registry=met targets_ok=4/4`, exit 0 — the auditor
  alone moves `registered=61 unregistered=4 … REGISTRY=unmet` (exit 1) to `registered=65 unregistered=0 …
  REGISTRY=met` (exit 0), and each row's self-test cell carries verbatim the final line its tool prints now
  (`MORI_CGROUP_PRESSURE_SELFTEST: pass=12 fail=0`, `MORI_DRIFT_RECHECK_SELFTEST: PASS (10 cases)`,
  `CALIB_SELFTEST pass=11 fail=0`, `DIGEST_SELFTEST pass=11 fail=0`), each selftest exit 0, each verdict-map cell
  carrying its frozen token.
- **C2 freshness (score 5) — three stale-flagged rows pinned with their recorded bytes and re-verified live.**
  S615, S616 and S623 (flagged stale at r96) are pinned under `corpus/evidence/sources-r97/` with the exact bytes
  their recorded digests name (S616 the r90 copy; S623 today's live body with the `Last updated on` stamp line
  restored to the recorded time — substituting that one line back into today's bytes reproduces the recorded
  sha256 bit for bit, so the pin is the recorded fetch and not a stand-in, per `w1/Mo97RevC2.md` §3 and
  `w1/Mo97RevStamp.md` §5; S615 the r90 ast copy that S619 already records as the correction of S615's
  mis-recorded digest, which is not edited); the new row S628 (docsbuild-scripts README) grounds the build-churn
  reading of the stamp delta. Command: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive <rev>
  | tar -x -C DIR && python3 .ufo/waves/round-97/count-c2.py --root DIR`. Before (entering `973b2af1`,
  `evidence/before-c2.txt`): `C2=unmet mismatch=0 unpinned=3 targets_ok=0/3 hole_guard=n/a
  live=S615:no-copy,S616:no-copy,S623:no-copy`, exit 1. After (landing `e85ed912`, `evidence/landing-c2.txt`):
  `C2=met mismatch=0 unpinned=0 targets_ok=3/3 hole_guard=pass live=S615:time-churn,S616:time-churn,S623:time-churn`,
  exit 0 — S615 `superseded-by S619` with `copy_equals_successor=yes` (the r96 supersession-hole guard), S616 and
  S623 `ok` with `copy_matches_tool=yes`, and every live class `time-churn` (the docs.python.org `Last updated on`
  stamp only).
- **Evidence motivating the round:** r96 routed defect 1 (four gates unregistered at the registry home) and r96
  routed defect 5 (the digest gate's supersession hole, now guarded in the frozen counter); the r96 lesson's
  `unpinned=3` rows S615/S616/S623 and the operator L0 line `mori | round-96`
  (`.ufo/l0-questions.md:355`) on stale digests.
- **Landed:** four `SKILL.md` registry rows; `corpus/evidence/sources-r97/{S615.html,S616.html,S623.html,S628.md}`;
  the S628 row in `corpus/SOURCES.md` (append-only: one row added, no existing byte changed); the frozen contract,
  counters and control battery; `corpus/lessons/round-97.md` (four mistakes mined); this entry and the SCORECARD
  round-97 section.
- **Not landed:** no score move on either axis. The 31 standing `prefix_only` digest rows are untouched (the digest
  gate still exits 1 on them); no recorded digest was edited and no supersession row was appended for S616/S623
  (CORPUS rule 2 mechanism reached only through the pre-existing S619 correction row); the operator L0 on stale
  digests is not treated as answered.
- **Wave:** `w1`, 14 seats (`.ufo/waves/round-97/w1-dispatch.json`, validator rc 0): 2 scout, 2 executor,
  2 reviewer, 2 critic, 3 mutation-tester, 1 connector, 1 revenger, 1 scribe; attack seats 7 of 14
  (reviewer + critic + mutation-tester, the lane's counting convention: r93 6/12, r94 6/12; the revenger seat is
  not counted as an attack seat).
- **Trend verdicts and axis verdicts are in `corpus/lessons/round-97.md` and the round report.**
```

## 7. Draft block 2 — SCORECARD.md section (append at end of `SCORECARD.md`; L1 to integrate)

```markdown
## Round 97 verdict — 2026-11-05 (L1 MoriR97, attempt 1)

Frozen contract `.ufo/waves/round-97/contract.md` at freeze `dd1ae1150f53df54e7530311b2323368e3c0e5e9` (contract,
counters `count-c1.py` / `count-c2.py`, and the pre-freeze control battery `evidence/controls-r97.txt`,
`CONTROLS_DONE unexpected=0`); entering `973b2af11f41bd362163d7e29ac08286832f546b`; landing
`e85ed91249953094b067554bfa79fcdc65791f8e`. Wave `w1`, 14 seats. Lesson `corpus/lessons/round-97.md`.

| claim | axis (score) | predicate | before (`973b2af1`) | after (landing `e85ed912`) | command | verdict |
|---|---|---|---|---|---|---|
| C1 | operability (7) | P1: the registry at `SKILL.md` runs and states the outcome of the four gates the auditor reported unregistered — auditor `REGISTRY=met`; each of the four rows' self-test cell holds, verbatim, the final line the tool's own `--selftest` prints now (exit 0); each verdict-map cell holds the tool's frozen verdict token | `C1=unmet unregistered=4 registry=unmet targets_ok=0/4` (exit 1; auditor `registered=61 unregistered=4 … REGISTRY=unmet`) | `C1=met unregistered=0 registry=met targets_ok=4/4` (exit 0; auditor `registered=65 unregistered=0 … REGISTRY=met`) | `git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive <rev> \| tar -x -C DIR && python3 .ufo/waves/round-97/count-c1.py --root DIR` | pending closure |
| C2 | freshness (5) | P2: S615/S616/S623 pinned with the exact bytes their recorded digests name and re-verified live — digest gate `mismatch=0 unpinned=0`; each target `ok` or hole-guarded `superseded-by S<n>` whose newest copy hashes to the successor's `ok` digest; each `ok` copy hashes to the tool's `actual=`; a live drift re-check exits 0 with every class in {fresh, time-churn} | `C2=unmet mismatch=0 unpinned=3 targets_ok=0/3 hole_guard=n/a live=S615:no-copy,S616:no-copy,S623:no-copy` (exit 1) | `C2=met mismatch=0 unpinned=0 targets_ok=3/3 hole_guard=pass live=S615:time-churn,S616:time-churn,S623:time-churn` (exit 0) | `git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive <rev> \| tar -x -C DIR && python3 .ufo/waves/round-97/count-c2.py --root DIR` | pending closure |

Receipts: `.ufo/waves/round-97/evidence/before-c1.txt`, `before-c2.txt`, `landing-c1.txt`, `landing-c2.txt`,
`controls-r97.txt`. No score move is claimed on either axis; both claims are left to the closure's ruling.

### Planned (round 98)

1. **calibration / quality** — the mutation sweep of `tools/mori-scorecard-calibration.py` and of the frozen r79
   counter's survivors M2, M5, M6, with a successor selftest arm for each survivor (a new revision, never an edit
   of the frozen counter): carried from `corpus/lessons/round-97.md` §r96 closure routed defects (item 7). The
   round-97 wave adds the calibration counter's own survivor M10 (verdict vocabulary widened in
   `cell_round_verdict`; `w1/Mo97MutCalib.md`).
2. **operability** — the gate-registry auditor's own junk-row false green (the auditor accepts any eight-cell row
   whose entry names the tool; the frozen C1 counter is what checks the stated selftest outcome and the verdict
   token): the auditor itself is not amended this round, so the fix is carried
   (`corpus/lessons/round-97.md` §Mistakes 4). The round-97 wave adds the counter-strength residuals R1–R3
   (rows under a non-registry heading still count; junk metadata cells beside a true entry/selftest/token; a true
   selftest line followed by a false clause) — outside frozen P1, carried (`w1/Mo97CritC1.md`).
3. **freshness** — the digest gate's own supersession hole (a predecessor whose copy merely mismatches is superseded
   by any verifying successor); it is documented in the tool's new registry row and guarded in the frozen C2 counter,
   but the tool is unchanged: carried (`corpus/lessons/round-97.md` §Mistakes 3).
4. **freshness** — the 31 standing `prefix_only` digest rows and the operator L0 on stale digests
   (`.ufo/l0-questions.md:355`, `mori | round-96`) stay open and unclaimed; this round reached CORPUS rule 2's
   mechanism only through the pre-existing S619 correction row and edited no recorded digest.
5. **conformance** — `corpus/lessons/round-95.md` heading `## Frontier step` against the `## Gate` convention (r95
   routed defect 2) and the dormant `census_path` literal arm (r95 E02) are still open (verified: the r95 lesson
   still opens `## Frontier step (corpus/SOURCES.md, contract v1)`, and the round-93 counter still carries
   `CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"`).
6. **carried** — the frozen-battery survivors m8, m10, m11 (r95 routed defect 1); D1 planner binding (operator).
7. **correction of record** — the round-97 lesson's census count (`corpus/lessons/round-97.md`: "`mori ok`, 42
   W04") does not match its own command: the census prints 43 W04 rows, before and after the round, the 43rd being
   S622 (since the round-93 landing), not the new S628 row; see the round-97 report's F1.
```

## 8. Unrun checks (named, not run)

- The round-97 control battery was **read** (`evidence/controls-r97.txt`), not re-executed: the control fixtures live
  under another seat's scratch root, and re-running them would consume live fetch rounds. Their recorded outputs are
  quoted in §3 as read bytes, not as evidence this seat produced.
- The live network fetch behind C2 leg (d) was not re-run by this seat as a *separate* drift-recheck invocation;
  the `time-churn` classes come from re-running the frozen counter (which performs its own fresh fetch) at the
  landing revision. One separate live fetch was made by this seat for the S623 pin-provenance check in §4 (one
  `curl` of `docs.python.org/3/using/cmdline.html`); no other network call was made.
- No mutation testing of any frozen counter by this seat (other wave seats own it).
- No `git`/`jj` mutation of any kind: no `add`, `commit`, `stash`, `checkout`, `switch`, `reset`, `pull`, `push`,
  `fetch`, `rebase`; `jj-lane.sh` and `fleet-commit.sh` were not run.
- The L0 questions file was read at the fleet root only; no question was filed, answered or amended by this seat.
- The round-97 lesson's `## Mistakes` table, the `QUALITY.md` criteria and `corpus/README.md` were read for context
  only; none was edited (no QUALITY entry was added this round).
- The peer seat reports in `.ufo/waves/round-97/w1/` were read for cross-checking; no peer file was edited.

## 9. Scope note

Detection and report only. This seat edited no product code, no tool, no corpus file, no ledger, no contract, no
counter, no receipt, no `MANIFEST.json`, nothing outside its own report file, and no sibling lane. The two blocks
above are drafts for the L1 to integrate; the L1 owns the final text, the wave settlement, the dead-seat accounting
and any correction of record for findings F1 and F2.

**Post-draft state (added when the L1's commits landed after this seat finished).** The lane has since been
integrated by the L1: `5497e6f7` (wave-1 evidence — all 14 seat reports, the four receipts, the registry cell
corrections, the lesson, LOG and SCORECARD) and `b6d03408` (final-revision receipts and census before/after). HEAD
is `b6d03408`, the working tree is clean, and this seat's report file is committed with the wave evidence. The
L1's committed `## Round 97 verdict` SCORECARD section and round-97 LOG entry agree with the draft blocks in §6 and
§7 on every measured value. **F1 (the lesson's "42 W04" against the census's own committed 43-row receipts) is
still open in the committed bytes and is not in the committed `## Planned (round 98)` list** — it is the one item of
my §7 list the L1's text does not carry, and it is the only thing this seat asks to be carried forward. F2 is
fixed in the committed lesson. F6 records that the final committed revision re-measures both claims as met.

**Cross-lane incident note.** At ~18:14Z a sibling lane's seat (`ConnectorScope-23`, kake r97) deleted the round
parent scratch directory `/fast/scratch/hyaku/kake-r97`, removing sibling seats' scratch trees under it. That path
is the kake lane's; the mori lane's scratch is `/fast/scratch/hyaku/mori-r97`, which was untouched — verified after
the report: this lane's frozen counter bytes, receipts, lesson, MANIFEST and the committed digests are all intact,
and this seat's own scratch was already removed on exit. Nothing this seat produced depended on kake scratch. The
incident is the reporting seat's to route; this seat records only that it did not affect mori.

Report: .ufo/waves/round-97/w1/Mo97ScribeLog.md
