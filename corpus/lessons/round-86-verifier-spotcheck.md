author: hyaku closure (non-author integrator, @m_zfl)
round: 86 · lane: mori · date: 2026-11-04 · attempt 1
entering revision: `fec2b328a4c83e0c61bc09d70e254ca47d547d34` · measured after: `6e77fe0e6bd4e71156276fe46880c758df0fc000`
report: `.ufo/reports/round-86/mori.md` (fleet repo, mori-shokunin identity, `d281d53` filed and `9836323` in-place correction; both on `origin/master`)

This is the non-author closure review: I did not author this round and changed nothing in it
except this file. The lane's three gates were **not executed** (PROTOCOL §Gate standard, Closure
consequence); their committed evidence was verified, and each claim's numbers were re-derived over
committed bytes with plain `git`/`grep`/`awk`/`python` reads. `jj-lane.sh state` (read-only) reported
`branch=master local=6e77fe0e remote=6e77fe0e ahead=0 behind=0 ... tracked=0 untracked=0` and
`git status --porcelain` was empty before this file.

## Step-1 conformance

| check | result |
|---|---|
| report committed in the fleet repo by the lane identity | **pass** — `git log --format='%an %H' -- .ufo/reports/round-86/mori.md` → `mori-shokunin <mori@shokunin.local> 9836323...` and `d281d53...` |
| report pushed | **pass** — `git merge-base --is-ancestor 9836323... refs/remotes/origin/master` holds |
| `SHONEN` heading, one line per box | **pass** — heading present; four `[~]` lines, one per box of `SHONEN.md`; no `[x]` mark (the only `[x]` string is the sentence saying none was written) |
| every cited lane commit exists and is an ancestor of the branch | **pass** — 12/12 hashes (`fec2b328`, `5e80229a`, `98d15d8f`, `c2bfded0`, `87644619`, `50d80df0`, `b0aa564c`, `8b4b4ad7`, `095bd1f6`, `6e77fe0e`, `4eab48c0`, `57104423`) pass `git merge-base --is-ancestor <hash> refs/heads/master` |
| lane repo clean and pushed | **pass** — `jj-lane.sh state` shows `ahead=0 behind=0`; `git status --porcelain` empty |
| prompt carries the template contract | **pass** — `.ufo/prompts/mori-round-86.md` is `templates/round-prompt.md` rendered (`mori`, `86`, fleet root, axes, lane repo path) plus the hyaku §6 addendum; the only text difference in §1–5 is the rendered `<mori-repo>` → `mori-shokunin` |
| marker vs report | **report** — names real committed work, a `LOG.md` entry and resolvable hashes |

Conformance defects (status-neutral, none bars admission):

1. **Unbacked tally.** Work performed says "Each mutated copy's own selftest reads `pass=25 fail=1`
   rc 1 (`evidence/after-r86.txt`)". That file carries only `MUTANT count-c3.py <label> killed
   rc=1`; the only r86 occurrences of `pass=25` are the assertion itself (`SCORECARD.md:4411`) and
   the report text — no receipt records it. The tally is derivable (26 arms − 1) but is not the
   cited output. The claim's actual evidence — six `MUTANT` lines, `killed=6 survivors=0` — is
   present.
2. **Missing battery.** `Mo86E04Controls` died before writing `evidence/battery-r86.txt`, so the two
   graded subjects' selftest tallies cited in the report (`C3_COUNTER_SELFTEST pass=26 fail=0`,
   `C2_COUNTER_SELFTEST pass=21 fail=0`) are documented claims (`SCORECARD.md:4427`,
   `SKILL.md:1372`) without a committed stdout receipt. They are implied by each gate's own target
   (C1 requires a green 26-arm pristine; C2's stub guard requires the 21-arm green), and the
   subject bytes are identical at `50d80df0` and `6e77fe0e` (`count-c2.py` sha256 `28071997…` at
   both), so the numbers hold; the receipt is what is missing.
3. **Diff sweep overstatement.** "Every other path in `git diff --numstat fec2b328 6e77fe0e` is
   additions only" is false: `SCORECARD.md` is `51 11` (the replaced `## Planned (round 86)` block).
   The four named deletion-bearing files are right (6/110/1/2) and no path was deleted
   (`git diff --diff-filter=D --name-only …` empty).
4. **Stale SCORECARD revision pointer.** The round-86 SCORECARD header/table say the after cells
   were measured at `50d80df0` with `evidence/after-r86.txt` as receipt; the committed receipt now
   names `b0aa564c` (re-measured after the C3 counter fix). `git diff 8b4b4ad7 6e77fe0e --
   .ufo/waves/round-86/evidence/after-r86.txt` shows `rev: 50d80df0 → b0aa564c` and C3 digest
   `6b7fc2dd… → e5f72141…`, so the unversioned pointer resolves to different bytes than the
   revision it cites. The report itself discloses the re-measurement.
5. **Contract prose vs its own control.** P-C1's entering control says "none of the six anchors
   exist" at `fec2b328`. Measured there: `all(rc == 1 for rc in rcs)` ×1, `if word == "agreed":`
   ×1, `and subject_tokens == len(own_tokens)` ×1, and the other two ×0 — consistent with the
   measured `mutants=4 survivors=4`, not with "none". The report states the right thing ("two
   anchors absent, the other four survivors"); the frozen contract sentence is the defect.
6. **Seat list double-count.** "Dead seats (8)" includes `Mo86M01Mut`; "Landed seats (4)" then lists
   five names, including `Mo86M01Mut` again. The consistent account is 4 landed (`S01`, `S02`,
   `Sc01`, `K01`) and 8 dead (`E01`–`E04`, `R01`, `R02`, `C01`, `M01`), which `w1-results.json`
   (`seats: 12`) supports.
7. **Unreceipted sweep sentence.** The quality trend says "the record and claim sweeps are green at
   the measured revision (`revisions=0`, `mismatches=0`)". Those tokens are the r85 receipts
   (`record-sweep-r85.txt`, `claim-sweep-r85.txt`, both `# rev: 25a74d4c…`); no r86 receipt re-runs
   them, and the r86 C2 run grades them as `legacy` headers only.
8. **Gate has no reject row.** `corpus/lessons/round-86.md` `## Gate` records one candidate (S602,
   ADMIT) and no rejected candidate with a reason, although the round's screen excluded six
   candidates; the reasons live only in `w1/Mo86S02Sources.md` §3. The registry also gained no
   rejected row this round. LEARNING requires every rejection logged with its reason.
9. **Same-round report rewrite.** The report was filed at `d281d53` and its landed-changes table
   rewritten in place at `9836323` rather than as an appended erratum naming the superseded text.
   History preserves both, and the correction names what it fixes in its subject, but the filed
   bytes were replaced.

## Claim re-checks (commands and observed output)

### C1 — operability: six surviving r85-C3-counter mutants get the failing arm each

- Before, at `fec2b328` (committed control, `.ufo/waves/round-86/evidence/controls-r86.txt`):
  `C1=unmet mutants=4 killed=0 survivors=4 total=4 arms=20 subject=arms` rc 1; the label-only stub
  reads `C1=unmet … survivors=6 arms=26 detector=green` (labels and tally alone are refused).
- Arm count, static: `git show fec2b328:.ufo/waves/round-85/count-c3.py | grep -c 'cases.append('`
  → **20**; at `6e77fe0e` → **26**.
- Anchors at `6e77fe0e`, each `grep -cF` → **1**: `return (rc == 0 and fields.get("verdict") ==
  "met"`, `all(rc == 1 for rc in rcs)`, `all(tokens == first for tokens in token_lines[1:])`,
  `if word == "agreed":`, `and subject_tokens == len(own_tokens)` (the C3-01/C3-02 rows share one
  anchor string, so five distinct strings cover six mutants). At `fec2b328`: 0, 1, 0, 1, 1.
- After, committed receipt `evidence/after-r86.txt` at `6e77fe0e`: six `MUTANT count-c3.py …
  killed rc=1` lines and `C1=met mutants=6 killed=6 survivors=0 total=6 arms=26 rev=b0aa564ca0de`,
  `rc=0`; its three `# counter-sha256:` lines equal `sha256` of the three counter files at
  `b0aa564c` (`1912e87d…`, `94a645b5…`, `e5f72141…`) — recomputed by me.
- The subject diff `fec2b328..6e77fe0e` is exactly the contract's three helpers plus six arm cases;
  the live conjuncts are the same expressions moved behind `subject_ok`/`met_verdict`/`stability`.

Verified: **evidence-verified, not executed** (gate not run). **Verdict: improved.**

### C2 — calibration: a `required` receipt's body is bound to its command

- Before, at `fec2b328` (committed control): `C2=unmet subject=stub
  missing=replay_match,replay_stale_mismatch,replay_none_requires_reason` rc 1.
- Population/grammar, measured by me at `6e77fe0e`: five receipts exist; each has `# cmd:`, one
  40-hex `# rev:`, a `# limits:` containing "limit" with ≥3 words; exactly two carry
  `# replay: required`; every body after the single `# ---` carries its summary token.
- Bindings: 7 `# counter-sha256:` lines total (3+1+1+1+1); each 64-hex digest equals
  `sha256(git show <receipt-rev>:<path>)` — **7/7 verify, 0 bad** (script printed
  `total bindings 7 bad []`).
- Arms: `grep -c 'cases.append('` on `.ufo/waves/round-85/count-c2.py` → **18** at `fec2b328`,
  **21** at `6e77fe0e`; the three new labels are present (`:400`, `:405`, `:409`).
- Replay evidence: `after-c1-r86.txt` and `replay-defeat-r86.txt` each read `REPLAY <name> rc=0
  exported=1`; the first grades `met`, the second `failed problems=replay-mismatch`. The two bodies
  are both 356 bytes and differ at one byte only — `killed=6` vs `killed=7` (`diff` at index 309) —
  while the defeat body's own six `MUTANT … killed` lines sum to six, so a header-only gate would
  accept an internally impossible body and the replay rule rejects it. Correct control.
- After line in the same receipt: `C2=met receipts=5 bindings=7 bound=7 revs=5 limits=5 cmd=5
  summary=5 replay=2 matched=4 defeated=1 legacy=3 unexpected=0 rev=b0aa564ca0de`.

Verified: **evidence-verified, not executed**. **Verdict: improved.**

### C3 — depth (capability acquisition): value-channel reconciliation of the classification

- Before: the counter file is absent at `fec2b328` (`git cat-file -e` rc 128, recorded in the
  control). Disclosed: applied retroactively it already reads met — the row claims a capability,
  not a subject-state move.
- Re-derived by me over committed bytes at `6e77fe0e` with a standalone implementation of the frozen
  name rule (`corpus/evidence/baseline-r10-20261015T2231Z.json` names vs
  `corpus/evidence/drift-classification-r82.txt`): **64** `DRIFT_CLASS` rows, **0** derivation
  mismatches, **19** `value-changed`, **14** bare-key `value-changed`. These are exactly
  `tokens=64 derived=64 name_agree=64 value_rows=14`.
- Contradictions: the baseline records `subject_commits=yes` and `window=launch..NOW`, the census
  prints the same literals (`tools/mori-census.sh:2473`, `GL_EXTRA='subject_commits=yes
  window=launch..NOW'`), and the classification labels both rows `value-changed`; the counter names
  them rather than relabelling the frozen file. The receipt prints `VALUE -subject_commits equal`,
  `VALUE -window equal` and `C3=met observations=2 aa=stable tokens=64 derived=64 name_agree=64
  value_rows=14 contradicting=2 rev=b0aa564ca0de`, `rc=0`.
- The capability rows entered the SCORECARD capabilities table in the same round, and the
  counter's `TARGET` is now compared (`count-c3.py:350`), discharging the mutation probe's finding 3.

Verified: **evidence-verified, not executed**; the two live-stability legs (`observations=2
aa=stable`) rest on the committed receipt, since the census is a live observation. **Verdict:
improved.**

## Per-axis verdicts

| axis | verdict | reason |
|---|---|---|
| operability | **improved** | 20 → 26 arms, six named mutants killed at the frozen revision, the label-only stub still refused |
| calibration | **improved** | five receipts, 7/7 bindings verified, the one-byte stale body rejected by the replay rule that the r85 predicate lacked |
| depth | **improved** | the 64-row classification is re-derived with a value channel (14 rows), two contradictions named, capability row entered |
| coverage | unchanged | no new surface claimed; the round is instrument work on existing surfaces |
| freshness | unchanged | no pin re-verified or retired this round; the r10 baseline stays in use |
| adjacency | unchanged | the connector scan found no lane replaying a receipt and absorbed nothing; PROVINCE unchanged in scope |

No axis is harmed: the `SCORECARD.md` diff adds the round section, three capability rows and the
planned-87 block, and removes only the superseded planned-86 block; no score decreases, no existing
capability row is removed, no criterion is deleted.

## Discernment spot-check

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S602 — in-toto Specification v1.0.0, `https://raw.githubusercontent.com/in-toto/docs/v1.0/in-toto-spec.md` | **ADMIT** (tier A, `spec`, `mined`) | live fetch 2026-11-04 + committed pin `evidence/sources-r86/in-toto-spec-v1.0.md` | **agree** | re-fetch is byte-identical to the pin (`cmp` clean): sha256 `17d3326e4cf58234619dbfe821cdc5187e55e2c89f7b63f03699c46588322097`, 87108 bytes, 2217 lines; the 9-word quote "Byproducts are not verified by in-toto’s default verification routine." sits at raw lines 1063–1064 and occurs exactly once in the joined text. It grounds the entry's recorded-vs-verified split, and the entry's `source:`/`verified-at:`/`recheck:` trio and coverage-map row exist |
| (no reject in the round's Gate) S601 — arXiv:2404.09241, "An Empirical Evaluation of Manually Created Equivalent Mutants" | **REJECTED** (registry row at `corpus/SOURCES.md:383`, r85) | committed copy `corpus/evidence/sources-r85/arXiv-2404.09241-abs.html` | **agree** | the copy matches its row (`4bcb20b2…`, 40386 bytes, 596 lines); abstract line 121 defines "mutants that differ only in syntax but not semantics" and says they "hamper this process", but contains no gate-tally bias or adjudication procedure, exactly the recorded rejection; the flip condition (a revision stating the cost-and-bias half for a tally/procedure, freshly pinned and quoted) is testable |

Gate completeness: the round's own `## Gate` carries **no rejected candidate row**, so the reject
half of this spot-check could only be exercised against the registry's nearest rejected row. The
six excluded candidates carry reasons only in `w1/Mo86S02Sources.md` §3; the seven-candidate screen
(7 identified, 5 fetched/opened, 1 included, 6 excluded, two of them already-held S600/S601)
reconciles arithmetically, but not in the Gate block LEARNING specifies.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → `mori ok
/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`, rc **0**, **35** `W04` duplicate-URL
warnings, zero `E` codes — matching the report.

## Trend verdicts

- **expansion: improved.** One admitted knowledge entry on ground the coverage map did not hold
  (`corpus/knowledge/execution-evidence-r86.md`, coverage-map row `corpus/README.md:907`), its
  `source:` citing S602; registry **374 → 375** by
  `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` at `5e80229a`
  (374) and `6e77fe0e` (375); append-only (`git diff --numstat fec2b328 6e77fe0e -- corpus/SOURCES.md`
  → `3 0`); census rc 0.
- **quality: improved.** All three frozen targets are met in the digest-bound after receipt at
  `b0aa564c`, the two graded subjects moved 20→26 and 18→21 arms, and QUALITY 177–180 add the
  round's rules with able-to-fail controls (`evidence/c3-value-controls.txt`). Named gaps: the r86
  battery is missing and the sweep sentence is inherited r85 evidence (defects 2 and 7 above) —
  record gaps, not a falsified entry.
- **discernment: improved.** The value channel names two of the classification's own
  `value-changed` labels as contradicting its values instead of relabelling the frozen file; the
  r85 `predicate-underreach` class is mined into QUALITY 178 with a rebuilt one-byte-stale fixture;
  the S602 admit agrees with the outside re-open. Routed defect: the Gate records no reject row.

## Routed defects (fix in round 87)

1. C1 evidence sentence: cite the receipt's `MUTANT … killed rc=1` output, or commit the mutated
   tallies; do not cite `pass=25 fail=1` to `after-r86.txt`.
2. Commit `battery-r86.txt` (or a receipt for the two subjects' `pass=26`/`pass=21` selftest
   tallies) so the report's sentences resolve.
3. Correct the SCORECARD round-86 measurement pointer: the receipt it cites is re-measured at
   `b0aa564c`, not `50d80df0` (append a correction naming the superseded cell).
4. Record the six exclusions as Gate reject rows (or a Gate paragraph with reason and flip each),
   and add the rejected-row entries the registry contract expects.
5. Fix the report's sweep sentence (SCORECARD has 11 deletions) and the seat lists (M01 is dead,
   not landed; "4" must name four).
6. Add the contract erratum: at `fec2b328` two anchors are absent, four mutants apply — not "none of
   the six anchors exist".
7. If the "record and claim sweeps green at the measured revision" sentence is kept, ship an r86
   receipt that re-runs both sweeps at the named revision.
8. Report corrections after filing: append an erratum naming the superseded text instead of
   rewriting filed table cells.
