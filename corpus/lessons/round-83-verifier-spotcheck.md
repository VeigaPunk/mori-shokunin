author: hyaku closure (non-author integrator, @m_zfl)
round: mori 83 (lane round 83, attempt 1) — non-author closure verification
report: `.ufo/reports/round-83/mori.md` (fleet repo, `32da2b2b`)
lane repo: `mori-shokunin` @ `8819c94c62f5d99ad9592ed965d37db4eab62d02` (branch `master`, pushed)
entering: `68185d6e719054c55b107280085b05609e96165b`
dispatch digest (copied from `.ufo/watchdog.log`, mutable):
`2026-11-04T05:12:33-03:00 launch mori round=83 pgid=2932901 driver=hyaku-inline attempt=1`
`2026-11-04T06:12:11-03:00 complete mori round=83; hyaku-inline attempt=1`

This reviewer authored no part of the round. Claims were re-derived with plain measurements over
committed bytes and compared with the reported values; where a claim rests on a lane-owned counter
or selftest, its **committed evidence** was verified and the instrument was not executed
(PROTOCOL §Gate standard, Closure consequence). No lane-authored file (report, SCORECARD, LOG,
lessons, SKILL, PROVINCE) was edited and no `[x]` was written into `SHONEN.md`.

## Conformance (step 1)

| Check | Result | Evidence |
|---|---|---|
| Report committed in the fleet repo by the lane identity | pass | `git log --format='%an %ae %H' -- .ufo/reports/round-83/mori.md` → `mori-shokunin mori@shokunin.local 32da2b2b…`; sole commit on the path |
| Report lands after the lane's work | pass | report committer `2026-11-04T06:11:18-03:00`; lane tip `8819c94c` committer `06:10:51-03:00` (author `06:08:39`) |
| `SHONEN` heading, one line per box | pass | report `## SHONEN` with four `[~]` lines, each with a pointer; lane `SHONEN.md` carries the four canonical boxes |
| Every cited lane commit exists and is an ancestor of the branch | pass | 11 hashes tested (`68185d6e 9075c729 d2987c67 466d28bc c4845c83 9cf7fda9 405dc48c 582604bf 8819c94c f02ad83b 075574c8`), `git merge-base --is-ancestor <h> master` → all `ANCESTOR-OK` |
| No uncommitted round work; pushed | pass | `jj-lane.sh state` → `ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` empty; `ls-remote origin refs/heads/master` = `8819c94c…` |
| Prompt committed and carries the template contract | pass | `.ufo/prompts/mori-round-83.md` at `63ef8961` (lane identity); head 140/140 lines byte-identical to rendered `templates/round-prompt.md`, tail 564/564 byte-identical to rendered `scripts/hyaku/lane-addendum.md`; all five round-level items (i–v), all five child-lane items, and addendum §6 present |
| Real report, not a marker | pass | work performed, evidence pointers, landed changes each tied to a `LOG.md` entry (`LOG.md` Round 83), resolvable commit citations → status `ok` |

Status-neutral defects named in the notes: (a) the addendum's base route map (prompt line 144)
was superseded by its own line 149, which matched the live host table at dispatch; the operator
rebalance landed 23 minutes after dispatch, so this is not the prompt's defect; (b) the addendum
carries two round-size bands (8–16 operative via its supersede clause, plus older 32–128 text);
(c) `templates/round-prompt.md` contains no literal write-scope child item — that item reaches
the lane only through the addendum, so the protocol/template claim that the template embeds all
five child-lane items is not literally borne out (operator-side); (d) addendum §6 cites
`ufo-wave-policy.json` as the "band 8–16" source, but that file carries no band field (the band is
operator convention).

## Per-claim re-check

### C1 — operability (score 7) — verdict **improved**

| Measurement (mine) | Command | Observed |
|---|---|---|
| Mutant population | `awk '/^\| file \| label \| old/,/^$/' .ufo/waves/round-83/contract.md \| grep -c '^\| \.'` | `23` (c1 7 / c2 9 / c3 7), matching the counter's `MUTANTS` table (23 entries) |
| Kill accounting | three receipt runs in `.ufo/waves/round-83/evidence/after-r83.txt` | 69 `MUTANT` lines = 3 × 23; per run `killed rc=1` ×22, `equivalent rc=0` ×1 (`duplicates_accepted`), `survived` ×0; summaries at `c4845c83`, `9cf7fda9`, `405dc48c` all `C1=met mutants=23 killed=22 equivalent=1 survivors=0 total=23 pristine=green detector=green`, rc 0 |
| Anchor integrity | 23 `old` strings `str.count` over `git show 8819c94c:<path>` (reviewer seat, re-measured) | 23/23 exactly once, including the two escaped/multi-line rows (`derive_key_eol_only`, `defeated_accepted`) |
| A1 coupling | `git show 8819c94c:.ufo/waves/round-82/count-c2.py \| grep -c 'residual += duplicates'` | `1`; the same file's `met` requires `residual == 0`; `count-c1.py`'s `EQUIVALENT` map exempts the mutant only while `base.count(coupling) == 1` and records `coupling-absent` (unmet) otherwise |
| Do-nothing controls | `.ufo/waves/round-83/evidence/controls-r83.txt` | `C1=unmet harness=absent` at `68185d6e`; pre-amendment `killed=3 survivors=20` **retained**; A1 re-take `killed=3 equivalent=1 survivors=19` at `9075c729` |
| Graded bytes at the tip | `git diff --stat 405dc48c 8819c94c -- <six counters> <classification> <tool> SCORECARD.md` | empty — the after receipt's revision and the tip are byte-identical on every graded path |

Evidence-verified (not executed): the kill verdicts above are the committed receipt; the r83
`count-c1.py --selftest` tally `pass=6 fail=0` is in `w1/Mo83R01C1.md:41`, and the graded r82
`count-c1.py` tally `pass=10 fail=0` in `w1/Mo83E01C1C1.md:82,128`; `count-c1.py` is unchanged
from `c4845c83` to the tip. All frozen anchors occur once in the tip bytes.

### C2 — calibration (score 5, tied lowest) — verdict **improved**

| Measurement (mine) | Command | Observed |
|---|---|---|
| Exactly-one header lines | `grep -c '^# Snapshot:'`, `'^# Snapshot-sha256:'`, `'^# As-of:'` on `corpus/evidence/drift-classification-r82.txt` | `1`, `1`, `1`; `grep -n '^# Snapshot'` shows only lines 6–7, no duplicate |
| Snapshot hash | `sha256sum .ufo/waves/round-82/evidence/drift-r82-live.txt` | `6091bc46cba5ef6e73f882f035f234d0ece023e6e12d98ca92368e2039bf9a5d` — equals the stated line |
| As-of | line 8 vs the snapshot's first `# run-start:` (line 1) | `2026-11-04T07:45:13Z` = `2026-11-04T07:45:13.552564+00:00` truncated to UTC whole seconds |
| Population | last `MORI_DRIFT:` list (snapshot line 10) vs `^DRIFT_CLASS ` lines | 64 tokens, 64 unique; 64 class rows, 64 unique tokens; 0 missing, 0 extra, 0 malformed, 0 duplicate; histogram `added-since-r10=45`, `value-changed=19` |
| Class agreement (sample, re-derived by the C2/C3 seat from the baseline bytes) | all 64 tokens recomputed from baseline `0993b23505de…` against the frozen derivation table | disagreements = 0; split 45/19 matches the report |
| SCORECARD binding | `SCORECARD.md:60` (Retired `drift-pin-r10`), `SCORECARD.md:13` (freshness cell) | row names baseline, classification path **and** snapshot path; cell carries `r10 pin retired` and the classification path; red literal `round-10 drift pin still red` = 0 |
| Live re-derivation | receipts in `after-r83.txt`; code read (not run) | `live_tokens=63 live_agree=63` at `c4845c83`, `live_tokens=64 live_agree=64` at `9cf7fda9` and `405dc48c`; `live_read()` requires exit 1 + non-empty token list (`live_ok = live_rc == 1 and bool(live_tokens)`); the receipt's note discloses the movement and the snapshot binding |

Evidence-verified: the three `C2=met …` lines are committed receipts; the header parser requires
exactly one of each provenance line and the frozen path (code at `count-c2.py:46-49,99-101,208-210`),
with `duplicate_header_*` / `foreign_snapshot_path_unmet` fixtures in the final bytes.

### C3 — depth (score 5, tied lowest) — verdict **improved**

| Measurement (mine) | Command | Observed |
|---|---|---|
| Markers and anchored check | `git show 8819c94c:tools/mori-record-sweep.py` | `ANCHORED_OCCURRENCE` at `:120`, `REVISION_MISMATCH` at `:194`; `contains_anchored()` requires `row_contains in line and contains_value(line, key, value)` on one line |
| Tool selftest tally | `.ufo/waves/round-83/evidence/battery-r83-final.txt:399-400` | `RECORD_SWEEP_SELFTEST pass=40 fail=0`; dispatch receipt 36 → 40 (+4 anchored arms) |
| Arm count in committed bytes | 36 literal `check(...)` sites + the 4-arm loop | 40 runtime arms = `ARMS_FLOOR` 40 |
| Fixtures | `count-c3.py:114-135`, `:245` | `elsewhere`: value only on a Note row while the anchored row says 18 → expects rc 1, `revisions>=1`, `REVISION_MISMATCH … rev-bytes`; `conformant`: value on the anchored row → rc 0, `revisions=0` |
| r82 fixtures updated | r82 tool blob defaults | `9075c729` blobs `pointers=240`/`pointers=237` → tip `| tool pointers=240 |` / `| tool pointers=237 |` |
| Real run | `after-r83.txt` at all three revisions | `C3=met arm=anchored defeated=2 fixtures=2/2 bindings=3 revisions=0 arms=40`, rc 0 |
| Bindings | `.ufo/waves/round-82/record-pins.json`; anchors in tip `SCORECARD.md` | exactly 3 revision bindings; `row_tally=19` ×1, `survivors=0` ×5, `wrong=0 fixtures=7` ×1; each value present at its named revision (`075574c8` ×1/×1, `482dc48d` ×1) |

Evidence-verified: the `elsewhere` r82-green run (r82 tool `revisions=0`, rc 0; anchored tool
`REVISION_MISMATCH`; scratch transcript in `w1/Mo83R02C23.md` §C3.4). The C3 counter's own tally
`C3_COUNTER_SELFTEST pass=9 fail=0` is receipted in `evidence/c3-selftest-r83.txt` and its bytes
are unchanged after `466d28bc`.

### Axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| operability (7) | improved | C1 verified: 22 killed + 1 adjudicated equivalent, 0 survivors, controls reproduce; 6 new r82-c1 arms (4 → 10) |
| calibration (5) | improved | C2 verified: snapshot binding, 64/64 class agreement, live reading reported as an observation |
| depth (5) | improved | C3 verified: anchored occurrence with the defeated `elsewhere` fixture and the real bindings green |
| coverage (6) | unchanged | no score move; the new ground is absorbed as an entry, not a surface |
| freshness (5) | unchanged | snapshot binding strengthens the retired-pin replacement; no new drift surface |
| adjacency (6) | unchanged | connector scan (a) overlap-declared, (b) distinct, (c) contested at the boundary; no sibling or fleet file written |

No axis is harmed: `git diff 68185d6e 8819c94c -- SCORECARD.md` is +94/−1 (the `## Retired` row
gains the snapshot path, plus appended round-83 sections); scores are unchanged; the battery reads
`BATTERY pass=57 setup=4 fail=0` at both dispatch and final bytes; the changed-path list is
confined to the lane repo's wave dir, counters, corpus, tool and SCORECARD (`PROVINCE.md` untouched).

## Discernment spot-check (LEARNING.md)

| Item | Decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|
| S598 — PIT "What is mutation testing?" (tier A, docs, ADMIT) | admit | pinned copy `corpus/evidence/sources-r83/pitest-home.html` | **agree** | sha256 `b0c7e0505c51c95b596060ef27babbce08e72d5aaf4557eb002c2637d2bf10cc`, 12023 bytes / 284 lines match the row; the located quote sits at raw line 114, exactly 14 words ("The quality of your tests can be gauged from the percentage of mutations killed."); the corrected "51 words" block is reproducible (lines 106-114 = 51 alphanumeric tokens; 108-113 = 31) |
| PIT "Mutation operators" (REJECT, no row) | reject | live `https://pitest.org/quickstart/mutators/` | **agree on the decision; disagree on one incidental count** | re-fetched bytes are identical to the recorded `a31331daf89f246f…` (67033 bytes); `grep -ci` for `killed`/`lived`/`adequacy`/`gauged` = 0/0/0/0, so the page does not state the adequacy gauge; but the page carries 29 mutator table entries and 29 `h2` mutator headings, not the recorded "38 operator headings" — the rejection stands on the sweep, the count is imprecise (routed) |
| S595 — arXiv:2102.11378v2 (not re-admitted) | no row change | `corpus/SOURCES.md:376` | **agree** | S595's scope is the abstract's own test-adequacy definition; S598 supplies the killed-percentage gauge sentence that scope does not claim |
| Newly written SOURCES row S598 | row is a claim | `corpus/SOURCES.md:379` + pinned page | **agree** | row written only after opening the pinned copy; `anchor` names line 114 and the 106-114 block; the quote is ≤25 words (14) with its location; search-log row at `SOURCES.md:457` records identified 2 / screened 2 / included 1 / excluded 1 |
| Sources census | gate | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` | **agree** | rc 0, `mori ok`, 371 rows, 0 malformed, 35 tolerated W04 duplicate-URL warnings (same class as entering); rows 370 → 371 by `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` (before/after) |

## Trend verdicts (with evidence)

- **expansion: improved** — one new admitted `corpus/knowledge/` entry on ground the coverage map
  did not hold as a distinct line (`counter-mutation-adequacy-r83.md`, K1–K4), `source: S598`
  opened, pinned and quoted this round; coverage-map row added in `corpus/README.md`; registry
  370 → 371; census rc 0.
- **quality: improved** — the three r82 counters gained working arms measured from committed bytes
  (c1 4 → 10, c2 9 → 16, c3 8 → 16 executed; 17 labels incl. the tool-absent branch), the record
  sweep 36 → 40 arms with the anchored occurrence rule, and the classification gained an immutable
  snapshot binding; the standing battery is unchanged at `BATTERY pass=57 setup=4 fail=0`.
  Counterweight routed: the final selftest tallies for r83 `count-c2` (12) and r82 `count-c3` (16)
  are statically present but have no committed run at the final bytes (D83-1).
- **discernment: improved** — the non-author spot-check agrees with the sampled admit and reject
  decisions; the round discloses six dead seats and the L1 stand-in work rather than presenting it
  as seat output; two independent reviewers, the arm map and the connector falsified the claims
  before data (R02 closed two C2 header bypasses pre-data; Sc02 and A1 converged on the equivalent
  mutant; R01 found zero fake kills and re-proved both controls). Named weakness: the reject note's
  operator-heading count is imprecise (D83-3), and the D82-2 receipt-gap class recurs for the two
  final tallies (D83-1).

## Routed defects the lane must fix next round

1. **D83-1 (status-neutral, evidence gap; the D82-2 class recurring).** The report claims the final
   selftest tallies `count-c2.py --selftest 12/12` (SHONEN box 3, SCORECARD capability row) and
   "Both counters now read `pass=16 fail=0`" for the r82 `count-c2.py`/`count-c3.py`; and the
   quality trend cites `c3 8 → 16`. The committed receipts do not print those tallies at the final
   bytes: `evidence/c3-selftest-r83.txt` pins HEAD `466d28bc` and prints r82 c3 `pass=8` and r83 c3
   `pass=9`; `w1/Mo83E04Snap.md:52` and `w1/Mo83R02C23.md:114` print r83 `count-c2` `pass=10`
   (pre-repair). Both r83 `count-c1.py` (+36/−4) and `count-c2.py` (+26/−1) changed after
   `466d28bc`; the r82 `count-c3.py` gained arms after its receipted 8. Static counts at the tip are
   6 / 12 / 9 / 16, so the claims are derivable but not receipted. Fix: commit the run tallies for
   the final bytes beside the after receipt (the D82-2 fix direction), and state the arm delta
   exactly.
2. **D83-2 (status-neutral, numeric precision).** The report says "7 arms for count-c3"; the
   committed delta is 8 executed cases (9 added labels including the tool-absent
   `main_path_arms_skipped` branch), taking the executed tally 8 → 16. Correct in a later record
   entry; do not rewrite the filed report.
3. **D83-3 (status-neutral, reject-note precision).** `corpus/lessons/round-83.md` `## Gate` says
   the PIT mutators page "catalogues 38 operator headings"; the re-fetched bytes (sha
   `a31331daf89f…`, 67033 bytes) carry 29 mutator table entries / 29 `h2` mutator headings. The
   rejection decision and its sweep (`0` hits for killed/lived/adequacy/gauged) reproduce exactly;
   correct the count in a later lesson entry.

## Operator notes (non-lane)

- The four `SHONEN.md` boxes look checkable by a non-author from committed bytes (SKILL registry
  row 17, the logged end-to-end round work, the runnable keepers, and the diff-scoped no-bleed
  check); this reviewer writes no `[x]` and promotion stays operator-owned.
- No tool was installed or upgraded; no pacman transaction, no sibling or fleet write, and no
  lane, OS or orchestration state was changed. The dispatch digests above are copied into this
  file because `.ufo/watchdog.log` is mutable.
