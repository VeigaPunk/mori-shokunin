# mori round 48 — frozen contract (L1 MoriR48, attempt 1)

Entering lane tip: `e5dbac05459887d9597ea5d1da0d8e3d024e0d17` (round 47; non-author closure
`corpus/lessons/round-47-verifier-spotcheck.md`). This file, both counters, the committed
source copies and the controls under `controls/` and `evidence/` are committed in one freeze
commit before any wave seat runs. A predicate, counter, floor or kill rule changed after any
seat has scored is not the claim's rule.

Active scores entering (SCORECARD.md Axes table): coverage 6, operability 7, depth 5,
freshness 5, calibration 5, adjacency 6. Lowest non-retired axes: depth, freshness, calibration
(tied at 5). Both claims work a lowest axis; no stagnation waiver is used.

Frozen instrument bytes (sha256) are printed in `evidence/freeze-sha256.txt` at the freeze commit.
If the working-tree bytes ever differ, the claim is measured with `git show <freeze>:<path>`.

## C1 — calibration: the pin reconciler cannot be turned green by the junk the round-47 closure found

Surface: `tools/mori-pin-check.py` (the lane's instrument that re-measures its own SKILL.md
self-assessment). Routed by round 47: `w2/CritV2Junk.md` FG1-FG5 and O1, `w2/ConnNextRound.md`
D2 (line-count pins) and D3 (truncated digests), the contract's named limits, and
`corpus/lessons/round-47-verifier-spotcheck.md` §5 item 3. Mined proposal: none from
`considerthese/` for this claim.

**P-C1.** At revision R, `python3 .ufo/waves/round-48/count-c1.py --tool <tools/mori-pin-check.py
at R> --rev R` prints `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12`
and exits 0: the tool bytes under test score `PIN_CHECK=unmet` (exit 1) on each of the eight
frozen junk edits J1-J8 of R's SKILL.md, and `PIN_CHECK=met` (exit 0) on each of the four frozen
honest edits H1-H4 and on R's unedited SKILL.md, every run with `--min-tally-pins 26
--baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53` (the round-47 baseline, so the round-47
gate rows carry no baseline obligation and hiding them is not a `dropped` finding). A tool crash, setup exit or
timeout is `errors`, never `unmet`.

The variants are edit functions inside `count-c1.py` (listed in its docstring), so they stay valid
when R's registry rows move; an anchor absent at R is exit 2.

- Before (entering tool, `controls/tool-v2-entering.py`, sha256 `9832e38c…` = `tools/mori-pin-check.py`
  at `e5dbac05`): the receipt `evidence/control-c1-tool-v2-entering.txt`.
- Target after: `C1=met` at the landed tip, same command, with the tool at R.
- Controls (each scored with the frozen counter before data; each must stay unmet):
  do-nothing = the entering tool (green on the junk); `controls/stub-always-met.py` (green on all
  junk); `controls/stub-always-unmet.py` (red on the honest edits and the real registry).
- Kill rule: if the landed tip prints `C1=unmet`, C1 is not verified; no re-scoring under a changed
  counter. The counter's own selftest pin (`C1_SELFTEST pass=34 fail=0`) and the freeze sha256 are
  receipts, not part of the predicate.
- Named limits: the variants are eight junk classes found by round-47 seats, not the class of all
  junk; wave 2 attacks with fresh classes and reports survivors as limits rather than re-scoring.
  A tool can pass by being narrower than the junk (rejecting every row with a pipe, say) so the
  honest edits H1-H4 and the real registry are part of the predicate. The counter does not run the
  tool's own `--selftest`.

## C2 — depth: filesystem-quota observability (FR2), field by field, each claim a located quote

Surface: `corpus/knowledge/` FR2 (quota/EDQUOT observability). Assimilation theme from
`/home/vgpnk/Projects/shokuknow/merge/mori/` — staged entry
`knowledge/corpus/knowledge/quota-observability-r38.md` (sources staged as S477-S482, which collide
with lane S477/S478 and are renumbered by document). The lane holds kernel quota flags (S078,
S084, S088, S089) and no user-space reporting or error surface
(`grep -cE 'xfs_quota|quotactl|EDQUOT|repquota' corpus/SOURCES.md` at `e5dbac05`: run in the
receipt `evidence/sweep-quota-rows.txt`). The RHEL 9 Japanese PDF named by the staged entry returns HTTP 403 to a
plain and a browser user-agent fetch on 2026-10-25 and is not part of this claim; the Solaris
`errno=49` document stays rejected.

**P-C2.** At revision R, `corpus/knowledge/quota-observability-r48.md` opens with `source:` lines,
`verified-at:` and `recheck:`, and carries a table whose header cells are `claim`, `source`,
`quote` with at least 8 rows; each row's source cell is one S-id naming a `corpus/SOURCES.md`
row at R that is `mined`, opened 2026-10-25, names its URL among the four frozen URLs in
`count-c2.py`, and lists the entry in `used-by`; each row's quote cell is one backticked span of
6 to 25 words, unique in the table, that occurs (tags stripped, entities decoded, whitespace
collapsed) in the committed copy of that row's URL under `corpus/evidence/sources-r48/`, and the
table draws on at least 3 distinct sources; every committed copy matches its frozen sha256.

Counting command: `python3 .ufo/waves/round-48/count-c2.py R` → `C2=met|unmet …`.

- Before (entering `e5dbac05`): `C2=unmet … failed=entry_absent,…` (`evidence/control-c2-donothing.txt`).
- Target after: `C2=met claims=N located=N quote_missing=0 bad_rows=0 sources=S source_rows=ok pins=ok
  provenance=ok` with N ≥ 8 and S ≥ 3 at the landed tip.
- Controls: do-nothing (entering revision); the counter's selftest arms carry the entry-level
  controls with their reason isolated — staged entry byte-exact (no claims table), altered quote,
  quote from the wrong copy, short and long quotes, duplicate quote, unmined row, row opened on
  another day, missing `used-by`, copy digest mismatch (`C2_SELFTEST`, 22 arms at freeze).
- Kill rule: `C2=unmet` at the landed tip → C2 not verified.
- Named limits: the counter checks that each quote occurs in its committed copy and that rows and
  provenance line up. It does not check that the claim cell follows from the quote, that the page is
  unchanged today (the copies are dated), or the entry's prose. Wave 2 attacks those with reviewers
  and records the result as a limit.

## Separability

C1 touches only `tools/mori-pin-check.py`, its SKILL.md registry rows and `count-c1.py`'s measured
variants; C2 touches only the FR2 entry, its SOURCES rows and `corpus/evidence/sources-r48/`.
Either counter can be run with the other claim's changes reverted.

## Frontier step, assimilation, mistake (not claims)

- Census: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` at round start
  (`evidence/census-start.txt`, exit 0, 20 lines of output with 19 W04 warnings plus one `ok`) and round end.
- Assimilation: theme FR2 (quota). Admit/reject per entry in the lesson `## Gate`. The three
  quarantine-slice rows (S244, S262, S268) get a hand-check verdict each.
- considerthese: `considerthese/2026-10-25.md` suggestion 2 (host-path portability count) lands as a
  lesson and QUALITY criterion with the counting command.
- Mistake: round-47 routed defect 1 (late seat results never committed, a `landing` class) with a fix
  that is shown able to fail.
- Round-47 routes carried: successor `count-c2` shape (used-by arm, 0-3-space rows, one path per cell)
  is realised in this round's `count-c2.py`; v2 selftest arms for symlink containment, argv
  sub-checks and case-insensitive unparsed ride C1's tool work.

## Round shape

Two v1 waves (policy `scripts/hyaku/ufo-wave-policy.json`, band 32-64): w1 build + first falsifiers,
w2 falsify after landing. Total within 64-100.
