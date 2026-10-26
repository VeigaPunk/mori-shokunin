# mori round 50 — frozen contract (L1 MoriR50, attempt 1)

Entering lane tip: `7197160b927f04db294c9553fb48fadcc7a3f4e3` (round 49 closure,
`corpus/lessons/round-49-verifier-spotcheck.md`). This file, both counters, the controls under `controls/`,
their receipts under `evidence/`, the assimilation scratch under `assimilation/` and the three source copies
under `corpus/evidence/sources-r50/` are committed in one freeze commit before any wave seat runs. A
predicate, counter, floor or kill rule changed after any seat has scored is not the claim's rule. Frozen
bytes are listed with sha256 in `evidence/freeze-sha256.txt`; if working-tree bytes ever differ, the claim
is measured with `git show <freeze>:<path>`.

Scores entering (SCORECARD.md Axes table): coverage 6, operability 7, depth 5, freshness 5, calibration 5,
adjacency 6. Lowest non-retired axes: depth, freshness, calibration (tied at 5). Both claims work a lowest
axis; no stagnation waiver; no exploratory claim. Two claims (the prompt prefers two).

## C1 — calibration: the self-assessment agrees with the fleet record and with the instruments

Surface: the lane's self-assessment files — `SCORECARD.md` `## Axes` table (the Last change and Evidence
pointer cells) and `SHONEN.md` (its tally pins). AXES.md defines calibration as "SHONEN.md/SCORECARD entries
match observed repo state"; the round prompt (§9) requires a calibration claim to count mismatches between
that self-assessment and observed state. Observed state here is (a) the fleet `MANIFEST.json` closure
entries (verdict and per-axis grades of every admitted mori round), read at the pinned fleet revision
`e014499613f63f8a467821219b0296121119ca53` (the commit that carries the round-49 closure), and (b) the
tallies the pinned instruments print at R. Routed by: `corpus/lessons/round-49-verifier-spotcheck.md` §5
item 2 (commit a selftest output for the tools; the 114/114 and 17/17 tallies were prose only) and the lane's own K4
class (pins outside the registry's self-test cell, open since round 48). The Last-change convention is the
one the table already uses ("round 26 (improved, score held)"): the latest admitted round whose closure
graded the axis improved or harmed.

**P-C1.** At revision R, `python3 .ufo/waves/round-50/count-c1.py R` prints
`C1=met items=N axes=6 pins=P boxes=B mismatches=0 errors=0 hidden=0 …` and exits 0, where: (a)
SCORECARD.md's `## Axes` table has exactly one row for each of the six axes, and for each axis the Last
change cell's first `round N` equals N*, the highest mori lane round <= 49 that the fleet MANIFEST.json (at
the pinned fleet revision) records with verdict `admitted` and that axis graded `improved` or `harmed`; the
text from that `round N` to the next `;` names N*'s verdict word; and the Evidence cell names
`corpus/lessons/round-N*-verifier-spotcheck.md` when that file exists at R, else `MANIFEST.json`. (b)
SHONEN.md keeps at least 4 checklist boxes and at least 2 tally pins; every tally pin is a backticked
`python3 <repo-relative path> --selftest` span directly followed by `(N/M)` or by
`-> `PREFIX pass=N fail=K``; run at R (git archive of R, TMPDIR in the scratch dir) the command's last
`PREFIX pass=P fail=F` line gives N=P and M=P+F (or the same prefix, pass and fail for the token form); no
other tally token stands anywhere else in SHONEN.md; and `.ufo/waves/round-50/evidence/selftests/<stem>.txt`
at R holds the observed `PREFIX pass=P fail=F` line.

Counting command: `python3 .ufo/waves/round-50/count-c1.py R` (optional `--scratch DIR`; the fleet repo is
the lane's parent directory, `--fleet-repo` overrides it).

- Before (entering `7197160b`, `evidence/control-c1-do-nothing.txt`): `C1=unmet items=8 axes=6 pins=2
  boxes=4 mismatches=6 errors=0 hidden=0 manifest=a94551c5bc8d` — coverage (cell round 26, MANIFEST 47),
  operability (31 vs 47), depth (31 vs 49), calibration (25 vs 49), and SHONEN's `(60/60)` and `(13/13)`
  against `PIN_CHECK_SELFTEST pass=114 fail=0` and `UNLANDED_SELFTEST pass=17 fail=0`; freshness (28) and
  adjacency (19) already agree.
- Target after: `C1=met items=8 axes=6 pins>=2 boxes>=4 mismatches=0 errors=0 hidden=0` at the landed tip.
- Controls (built as commits in a throwaway shared clone by `controls/c1-controls.py`, scored by this counter
  before data; receipts `evidence/control-c1-<name>.txt`):

  | control | result | reading |
  |---|---|---|
  | do-nothing | `mismatches=6` unmet | the target is not reachable without work |
  | all-latest (every Last change cell `round 49 (improved, …)`, evidence cites round 49) | `mismatches=6` unmet | a blanket "latest round" edit fails four axes |
  | pins-deleted (tallies removed) | `pins=0 … failed=mismatch,pins_floor` | deleting the self-assessment is not calibrating it |
  | pins-updated-no-receipt | `mismatches=6` unmet | a corrected number without a committed receipt fails |
  | axes-only | `mismatches=2` unmet | the SHONEN half is separately required |
  | shonen-only | `mismatches=4` unmet | the Axes half is separately required |
  | box-dropped | `boxes=3 … boxes_floor` unmet | deleting a box fails |
  | witness (both halves, receipts) | `C1=met … mismatches=0` exit 0 | feasibility only; built by the L1's script, not the claim's landing |

- Kill rule: `C1=unmet` at the landed tip → C1 not verified; no re-scoring under a changed counter.
- Named limits (before data): the Score column is not checked (MANIFEST holds verdicts, not scores); the
  counter reads the Last-change convention, not whether a different convention would be better; a pin split
  across lines or outside backticks in another file is not enumerated (the hidden scan covers SHONEN.md only);
  a matching tally proves the instrument prints it at R, not that its arms are good; the MANIFEST is
  fleet-written and the counter trusts it (it does not re-judge the closures).

## C2 — depth: the memcg OOM report block and what memory.stat says about a killed cgroup's charge (FR1)

Surface: `corpus/knowledge/` — event-time attribution of a memcg OOM kill (frontier FR1, "Kernel OOM
event-time attribution and fleet correlation"): what the kernel prints for a memcg OOM (the usage/limit/
failcnt line, the `Memory cgroup stats for <path>:` block produced by the same formatter as the
`memory.stat` file, the per-victim `Killed process` fields), what each memory.stat key means (anon, file
including tmpfs and shared memory, shmem, kernel), which units each line uses, and how a global OOM differs
(`__show_mem` instead of the memcg block). Sweep before data (`evidence/sweep-memcg-stat.txt`, at `7197160b`
over `corpus/SOURCES.md corpus/knowledge SKILL.md`): `memory.stat`, `Memory cgroup stats`, `failcnt`,
`print_oom_meminfo`, `memory_stat_format` and the v7.2 cgroup-v2 / memcontrol.c URLs occur 0 times;
`anon-rss`/`shmem-rss` occur once (`oom-tracepoints-r47.md`, the tracepoint schema, not the report block).
Assimilation theme from `/home/vgpnk/Projects/shokuknow/merge/mori/`: staged entries
`scope-charge-fields-r46.md` (row S533, the v7.2 cgroup-v2 page; own-work S534) and
`scope-composition-in-the-block-r47.md` (own-work S539) — rewritten as one entry
`corpus/knowledge/oom-memcg-stat-r50.md`. The staged own-work rows cite notes outside this lane and are
not adopted; the staged r46 tmpfs hypothesis is the r47 entry's own refutation and is not adopted as a
claim. New rows: S489 (the v7.2 cgroup-v2 page; staged S533 renumbered by document), S490 (memcontrol.c at
tag v7.2), S491 (oom_kill.c at tag v7.2; same URL as S003 and S476, different scope — a W04 warning, not an
error).

**P-C2.** At revision R, corpus/knowledge/oom-memcg-stat-r50.md opens with source: lines, verified-at: and
recheck:, and carries a table whose header cells are claim, source, quote with at least 10 rows; each row's
claim cell has at least 6 words, is unique in the table (case and whitespace folded) and carries at least 3
words of 3+ letters that are absent from its quote; each row's source cell is one S-id naming a
corpus/SOURCES.md row at R that is mined, opened 2026-10-26, names its URL among the three frozen sources
and lists the entry in used-by; each row's quote cell is one backticked span of 6 to 25 words (an escaped
`\|` reads as `|`), unique in the table, that occurs (HTML copy: script, style and comment blocks dropped,
tags stripped, entities decoded; every copy: whitespace collapsed) in the committed copy of that row's URL
under corpus/evidence/sources-r50/; the table draws on all 3 sources; every committed copy matches its
frozen sha256.

Counting command: `python3 .ufo/waves/round-50/count-c2.py R` → `C2=met|unmet …`.

- Before (entering `7197160b`): `C2=unmet … pins=bad … failed=entry_absent,pins`
  (`evidence/control-c2-donothing-git.txt`; pins read bad because the copies are not at the entering tip).
- Target after: `C2=met claims=N located=N quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok
  provenance=ok` with N >= 10 at the landed tip.
- Controls (`controls/c2-controls.py`, entering bytes plus the frozen copies, receipts
  `evidence/control-c2-*.txt`): do-nothing `failed=entry_absent`; staged r46 entry byte-exact, staged r47
  entry byte-exact, staged r46 entry plus staged row S533 byte-exact — each unmet (`table`,
  `claims_floor`, `source_rows`). Selftest arms (`C2_SELFTEST pass=31 fail=0`, `evidence/selftest-c2.txt`)
  carry the entry-level controls with their reason isolated, including the two round-49 critic classes:
  breadcrumb rows with one repeated claim (`bad_rows=9`) and claims that only echo their quote.
- Kill rule: `C2=unmet` at the landed tip → C2 not verified.
- Named limits: a located quote proves the quoted words occur in the committed copy, not that the claim cell
  follows from them; the three-new-words floor is a floor, not entailment; v7.2 code says nothing about other
  kernels or cgroup v1; no host OOM block is read (no MESSAGE grep — lane rule S351/QUALITY 15), so the entry
  states what the kernel prints, not what a past kill on this host printed. Wave 2 reviewers re-open every
  row against the text around its quote and report the result as a limit.

## Separability

C1 touches only `SCORECARD.md`'s Axes table rows, `SHONEN.md` and `.ufo/waves/round-50/evidence/selftests/`;
C2 touches only the entry, its SOURCES rows and `corpus/evidence/sources-r50/`. Either counter can be run with
the other claim's changes reverted (C1 reads no corpus entry; C2 reads neither SCORECARD.md nor SHONEN.md).

## Frontier step, assimilation, mistake, considerthese (not claims)

- Census at round start: `evidence/census-start.txt` (rc 0; 21 W04 warnings + `ok`). Round end: same command.
- Sourced claim: C2 rests on S489–S491, opened 2026-10-26.
- Assimilation (one theme, one entry): collision check `assimilation/{reg-ids,staged-ids,collisions}` — 261
  registry ids, 136 staged, 18 collisions S471–S488 (S485–S488 are the lane's round-49 rows for other
  documents); the adopted staged row S533 collides with none (`grep -cx S533 reg-ids` → 0). Guard proof
  `assimilation/guard-proof/` (indented `  | S533 |` and `   | S534 |` rows are caught; a column-0-only
  pattern catches neither). Quarantine slice `assimilation/quarantine-slice`: S244, S262, S268 (round-48
  verdicts stand; none cited by the admitted entry). Renumber by document: staged S533 → S489; S534/S539 not
  adopted.
- considerthese: `considerthese/2026-10-25.md` suggestion 2 (host-path portability count) — a measurement
  and a QUALITY criterion this round; suggestions 1 and 3 were mined by rounds 47 and 49.
- Mistake mined: the self-assessment drift C1 measures (SHONEN pinned 60/60 and 13/13 since round 48 while
  the tools grew to 114 and 17; the Axes table's Last change cells lagged four admitted closures).

## Round-49 closure routed defects (§5 of the spot-check) — carriers

1 author date → the report is filed in two fleet commits so the last one's author date (= the first one's
commit time) is after the lane tip; 2 selftest output files → C1's receipts; 3 the 48-vs-47 erratum → lesson
and LOG.md correction entry; 4 `.scratch/` and `round-40/scratch/mori-conform-selftest-*` → deleted at round
end with a before/after count; 5 round shape → two waves summing to >= 64 seats; the two round-49 seats with no
report are accounted (one late report is on disk and is committed as inherited); 6 the `variants=26` vs 27
lines count → documented in the lesson; 7 K4, R11 carve-out, randomised handle → C1 closes K4 for SHONEN.md
only; the rest stays routed; 8 D-g wording → lesson note.

## Round shape

Two v1 waves (policy `scripts/hyaku/ufo-wave-policy.json`, band 32–64): w1 build + first falsifiers, w2
falsify after integration. Total 64–100. The L1 holds the planner seat.
