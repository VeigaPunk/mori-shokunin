# Round 79 — mori verifier spotcheck (non-author closure review)

author: hyaku closure (non-author integrator, @m_zfl)
round: 79
date: 2026-11-04
entering: `84c6cbc3b47c536a504aaee329c77897d389935e` (lane HEAD before the round)
lane head after: `d577b3d3921a1a5f9d05202ae100c272635823b3` (branch `master`, pushed; `ls-remote` prints it)
method: index-free read-only git (`rev-parse`, `cat-file`, `show`, `diff`, `merge-base --is-ancestor`, `ls-remote`), the three frozen counters re-run from committed bytes, and the landed tool re-run from the committed blob extracted to scratch. Two fresh non-author reviewer seats (C1 tool attack, C3 source re-open) ran read-only, no `model` parameter, no repo writes. No lane file was edited except this one; no mutating jj command was run except the lane helper's own commit for this file.

## Verdict summary

**status ok, admitted.** All three claims verify on independent re-derivation; no owned axis is harmed (the six axis scores are byte-unchanged: 6/7/5/5/5/6). The round discharges the r78 routed D78-1 mechanically and discloses two self-inflicted defects it caught before the report. One status-neutral correction-sweep defect is routed (the SCORECARD capabilities row still states the seat's 18-arm freeze while the landed blob carries 19), plus the lane's own C2-selftest route is confirmed.

## Step-1 conformance

| Check | Result | Evidence |
|---|---|---|
| Report committed by lane identity | PASS | `git log --format='%an %ae %H' -1 -- .ufo/reports/round-79/mori.md` → `mori-shokunin mori@shokunin.local 13bb44965355…`, 2026-11-04 |
| Report lands last | PASS | report committer date 02:48:06 -0300 > lane tip `d577b3d3` 02:46:55 -0300 > `324c182b` 02:45:54; the report's cited hash exists and the report names the final receipt. (Its *author* date 02:46:04 is the jj working-copy change's creation time, not the commit time; the commit is after the lane work.) |
| `SHONEN` heading | PASS | `grep -c '^## SHONEN'` = 1; four `[~]` lines, one per box, each with a resolvable pointer — correct author-asserted form while SHONEN.md is held |
| Cited lane commits exist + ancestor | PASS | 8/8: `merge-base --is-ancestor` rc 0 for `aa53b485`, `e6f3fd09`, `4629dce4`, `f5460942`, `8f4f7f12`, `e3e2e272`, `324c182b`, `d577b3d3` against `refs/heads/master` |
| Lane repo pushed, no uncommitted round work | PASS | `jj-lane.sh state` → `ahead=0 behind=0 tracked=0 untracked=0`; `git status --porcelain` empty; `ls-remote origin refs/heads/master` = `d577b3d3921a…` |
| Write scope held | PASS | entering→final `diff --name-status` = 46 paths, all lane-owned carriers (wave evidence, LOG, SCORECARD, SKILL, corpus, the new `tools/mori-control-receipt.py`); no existing instrument byte changed; no sibling, MANIFEST, fleet-root or `.ufo/state/` path |
| Prompt carries the template contract | PASS | `.ufo/prompts/mori-round-79.md` carries §1–§5 of `templates/round-prompt.md` (claims, frontier step, L2 floor, report contract incl. the `SHONEN` heading, commit/push scope) plus the hyaku addendum; §3 rests on one batched call with ≥8 seats matching `MISSION.md` §L2 concurrency (≥8, one call) |
| Not a marker report | PASS | real work, three frozen counters, checkable hashes, receipts; minimum content complete |
| Contract frozen before data | PASS | `aa53b485` (02:32:35) precedes the wave (`w1.ready` 02:34:49); `contract.md` and the three counters are byte-identical at `aa53b485` and `d577b3d3` (blob hashes equal) |

## Claim re-checks

Re-measured by this reviewer (commands run, not receipts read): C1 before/after presence, blob sha, selftest, witness and after runs; C2 independent MANIFEST derivation plus the counter; C3 pin hash/size, quote lines, census, row count. Evidence-verified (committed receipts read and cross-checked, gate not executed): the standing 13-receipt battery, the wave attack seats' tallies.

### C1 — operability (capability acquisition, D78-1 discharge): VERIFIED

- Before: `git cat-file -e 84c6cbc3:tools/mori-control-receipt.py` → rc 128; the path is in no ref.
- After: `git show d577b3d3:tools/mori-control-receipt.py | sha256sum` → `531d6b524635…` (367 lines).
- Selftest re-run from the committed blob with `python3 -I`: 19 arms executed, `CONTROL_RECEIPT_SELFTEST pass=19 fail=0`, rc 0. Arms assert exact finding strings (`unbound <path>#<section> claims=N keys=…`, summary totals) and rc per case — no vacuous arm.
- Witness re-run: over `.ufo/waves/round-78/evidence` → rc **1**, `CONTROL_RECEIPT_SUMMARY files=15 sections=37 claims=40 unbound=11`, and the named line `unbound …/controls-r78.txt#4. the D78-1 correction absent at entering claims=1 keys=correction_marker_in_LOG_at_entering` — the report's C1 claim word for word.
- After run: over `.ufo/waves/round-79/evidence` → rc **0**, `files=6 sections=27 claims=89 unbound=0`.
- Independent seat (`CloseMoriR79.C1ToolAudit`) reproduced all three, plus blob `4ae72950659b…` (git object) and the same sha256. Its adversarial additions define the limit, not a claim failure: a `$ this-is-not-a-counting-command` line binds a section (the frozen predicate is textual co-presence, declared before data), and decimal/exponent-only values are outside the declared `key=<integer>` grammar so they are not claims. Registry row 13 carries all eight fields (name, kind, entry, verdict map, self-test, pinned values, write scope, owner) with the landed 19/0 tally; SKILL.md:1363-1365.

Grade: **operability improved.**

### C2 — calibration (the five stale `Last change` cells): VERIFIED

- Independent derivation (this reviewer, not the lane's counter):

  `jq -r '[.rounds[] | select(.lane=="mori" and .admitted==true and .round<=78) | select((.verdicts//{})[$ax]=="improved" or (.verdicts//{})[$ax]=="harmed") | .round] | max' MANIFEST.json`
  → coverage **56**, operability **78**, depth **76**, freshness **78**, calibration **78**, adjacency **19**; 46 admitted mori rows ≤78; 0 admitted rows with `harmed`. r77 (`admitted:false`, depth `improved`) correctly excluded.
- Entering cells at `84c6cbc3` read 47/51/51/28/50/19 → 5 mismatches. `count-c2.py 84c6cbc3` reproduces `C2=unmet axes=6 mismatches=5 errors=0 rows=46 through=78` rc 1.
- Final cells at `d577b3d3` lead 56/78/76/78/78/19, each verdict word inside the first clause; `count-c2.py d577b3d3` reproduces `C2=met … mismatches=0` rc 0.
- The frozen contract's descriptive before-state (47/47/49/28/50/19) mis-states two cells; the graded predicate compares against MANIFEST and is unaffected. The lane discloses this as `## Mistakes` 3 — the report itself states the correct 47/51/51/28/50.
- Named limit (declared before data, holds): the predicate grades the `Last change` clause only, not the `Evidence` cell; the adjacency cell's cited `corpus/lessons/round-19-verifier-spotcheck.md` does not exist (the cell discloses this). Routed below.

Grade: **calibration improved.**

### C3 — freshness (sourced, S594): VERIFIED

- Rows, my own count: `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` 366 → **367**; malformed rows (NF≠13) **0**; tier histogram A=328 B=19 C=20 (the one addition is tier A).
- Row `S594` at `SOURCES.md:375`: 11 cells, unique id, `spec`/A/`mined`, opened 2026-11-04, recheck `365d`, anchor = §4.1 lines :528-534/:552-554/:556-557/:559/:576 + pin sha + copy path + size, `used-by` names the entry, which exists.
- Pin: `sha256sum` = `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`, `wc -lc` = 1956 lines / 84477 bytes — matches row, entry and report. Independent seat's live fetch of `https://www.rfc-editor.org/rfc/rfc9111.txt` returned HTTP 200 with byte-identical content and the same sha.
- Re-opened source: line 526 is `4.1.  Calculating Cache Keys with the Vary Header Field`; `:529`/`:532`/`:559`/`:576` carry the four quoted spans verbatim, on one line each, 10/12/12/11 words (all ≤25). The operative sentence at :528-534 is the MUST-NOT-reuse-unless-fields-match rule the entry cites; :552-554 absent-field and :556-557 `*` never match are as stated.
- Entry `corpus/knowledge/ua-serving-normative-r79.md` opens with the provenance trio (source S594 + pin sha, verified-at, recheck 365d) and its Limits section explicitly disclaims evidence of vendor `Vary: User-Agent`, cache traversal, RFC compliance, and the cause of any historical byte delta — no overreach found.
- `sources-census.sh validate --root … mori` → rc **0** (35 tolerated W04 duplicate-URL warnings, `mori ok`), matching both round receipts.
- README gained one index row naming the entry (`corpus/README.md:865`).

Grade: **freshness improved.**

## Discernment spot-check (checked from outside)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S594 (RFC 9111 §4.1) admit, tier A, scope "what selects among stored representations" | admit | Pinned copy at the committed sha, plus a fresh live fetch by the independent seat (HTTP 200, byte-identical); heading :526; quotes :529/:532/:559/:576 re-located and word-counted | **agree** | Quotes are contiguous, located and ≤25 words; §4.1 really governs Vary-based selection and reuse; tier A is right for a spec; the entry states what the section does not prove |
| The scribe's S594 row draft superseded by the L1 row (30-word quote vs the lane's ≤25-word rule, QUALITY 90) | reject (row draft) | `.ufo/waves/round-79/w1/Mo79S02SourcesRow-append.md` anchor cell; counted the quoted span | **agree** | The draft's quote is 30 words against the lane's own limit; the landed row carries line refs and the pin sha instead, which is stronger provenance for a spec row |
| Gate declares "Rejected: none" for sources | observation | `SOURCES.md` at entering (366 rows) + the pre-fetch duplicate sweep (exact URL 0, `rfc9111` 0, "HTTP Caching" 0; nearest held rows named) | **agree, with a named weakness** | One candidate was screened and none competed; the admit is sound, but an admit-only source gate shows less discrimination than a round with a real reject. The round's other refusals (merge package, tally-pinned instruments, axis re-scoring) carry the taste evidence |
| New SOURCES row quote check (contract rule 1) | admit | Same pinned bytes; the row's anchor cell re-read cell by cell | **agree** | The row itself carries line anchors plus the sha; the ≤25-word located quotes live in the lesson's Gate and all four verify |

## Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| operability | improved | C1 verified: a new registered gate runs from committed bytes (selftest 19/0, witness rc 1 on the D78-1 class, after rc 0/unbound=0), registered at the lane's registry home with all eight fields |
| calibration | improved | C2 verified: five `Last change` cells reconciled to the independently derived fleet record (5 → 0 mismatches); no score moved; one unswept count routed |
| freshness | improved | C3 verified: S594 opened, pinned, quoted and cited; the pin reproduces live; census rc 0; the entry names its limits |
| coverage | unchanged | No new surface claimed; `PROVINCE.md` byte-identical entering→final (diff 0 bytes); the new entry is knowledge ground, cited under the freshness claim |
| depth | unchanged | No depth-axis claim; the entry's K1–K4 detail is cited but the lane claims no depth move and no depth metric moved |
| adjacency | unchanged | No sibling surface touched; the `merge/mori/` package stays closed with reasons; the control-receipt tool reads receipts only (sentinel-audited: no write, subprocess, socket or `/tmp`) |

No axis is harmed. Lowest-non-retired-axis rule satisfied: depth/freshness/calibration are tied at the floor (5); C2 (calibration) and C3 (freshness) both work it, and C1 is an admitted capability acquisition.

## Trend verdicts

- **expansion: improved** — one new admitted entry on ground the coverage map did not hold (the normative Vary-selection mechanism behind the empirical `ua-serving` class), citing `mined` S594; rows 366 → 367 with malformed 0 and census rc 0; README index row landed the same round. Agrees with the report.
- **quality: improved** — a new 19-arm gate whose mutation seat reports 7/7 mutants killed (evidence-verified from `w1/Mo79M01Mutant.md`, not re-run), the r78 routed D78-1 discharged mechanically, and the round's own receipts conform to the rule it lands (`unbound=0`). Counterweights, both routed: the SCORECARD capabilities row still says 18 arms (D79-1), and the C2 counter's selftest lacks three arms (D79-2, lane-routed before the report). No admitted corpus entry failed a re-check.
- **discernment: improved** — four mistakes mined with class/evidence/captured-by/fix and eight process refusals recorded with their flips; this spot-check agrees with the sampled admit and with the round's reject-class decision (the superseded 30-word row). Named weakness: the source gate was admit-only this round.

## Routed defects the lane must fix next round

1. **D79-1 (status-neutral, correction-sweep class).** `SCORECARD.md:4016` (capabilities row) states "selftest 18 in-memory cases" and its evidence cell says "`after-r79.txt` (selftest 18/18, both live dirs)", while the landed blob runs 19 arms and `after-r79.txt` records `selftest=19/0`. `e3e2e272` corrected the SKILL row only; the Evidence-standard sweep ("a corrected fact left standing in a sibling file is still a defect") was not run over SCORECARD. Fix: correct the capabilities row (and any other 18-arm mention) with a named correction, and re-grep the round's carriers for the superseded tally.
2. **D79-2 (status-neutral, selftest coverage; lane-routed before the report).** `count-c2.py`'s selftest does not kill three mutants the mutation seat survived: dropping the `admitted` filter, searching past the first `;`, and accepting a matching round anywhere in the cell. Fix: one arm per surviving mutant before the counter is used for a new claim.
3. **D79-3 (status-neutral, dead pointer in a claim-bearing row).** The adjacency `Evidence` cell cites `corpus/lessons/round-19-verifier-spotcheck.md`, which is not in the repo (the cell itself discloses this). Fix: point at the committed MANIFEST row pointer the cell already names (`rounds[398]` at the recorded fleet revision) or a committed spot-check file; a pointer must resolve at closure.
4. **D79-4 (named limit, record it).** The control-receipt guard enforces section-level textual co-presence, not command relevance: a `$ <any text>` line binds a section, and decimal/exponent-only values are outside the declared integer grammar and are not claims. This is the frozen predicate, not a defect; record the limit beside QUALITY 164 so a reader does not read the gate as command-semantic proof.
5. **D79-5 (low, selftest precision).** Arm 17 ("unreadable file") exercises `FileNotFoundError`, overlapping arm 9 rather than permission denial, and arm 16 tests the filename-sort helper rather than full `--dir` integration. Add a permission-denied arm and one end-to-end `--dir` case when the selftest is next touched.

Carried, not new: the three open mori L0 lines (round-62 wave-surface waiver, round-65 instrument-change ruling, round-73 label-sweep instrument) remain present and unanswered and were routed around correctly; the three r76 foreign receipt files remain disk-only under the standing leave-for-operator ruling.

## Notes for the operator

- `SHONEN.md` is still 4/4 `[~]` (author-asserted). Reading the committed evidence, all four boxes look checkable by a non-author: SKILL contains real decision tables/error patterns/cited sources; the round's claims are logged end-to-end in LOG with measured commits; the frozen contract + three selftesting counters + receipts make the round re-derivable without oral context; and `PROVINCE.md` is byte-unchanged with the tool's read-only behaviour sentinel-audited. Promotion remains operator-owned; nothing here writes `[x]`.
- The round's own defects were caught and mined before the report (the C2 applier's newline damage at `e6f3fd09`, repaired at `4629dce4`; the pipeline-read rc in the first controls receipt, regenerated). The `e6f3fd09` defect is preserved in history, not rewritten — correct append-only behaviour.
