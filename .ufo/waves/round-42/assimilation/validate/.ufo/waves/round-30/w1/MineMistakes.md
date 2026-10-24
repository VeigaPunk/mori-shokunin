# MineMistakes — round-30 `## Mistakes` draft (mori, L1 MoriR30)

Seat: `MoriR30.MineMistakes` (scribe, leaf). Read at lane `e936482` (round-30 declaration; contract landed
`a66751b1`, entering tip `58b61681`). Nothing written outside this file: no lesson, QUALITY, SOURCES, tool,
counter or gate edit; no git/jj write; no subagent, no background job.

Sources read: `.ufo/waves/round-30/contract.md`; `corpus/lessons/round-29-verifier-spotcheck.md:152-166` (R1-R7);
`corpus/lessons/round-29.md` (`## Mistakes` :26-47, wave-2 corrections :92-121, `## Gate` :57,62,65);
`/home/vgpnk/Projects/shokunin/CORPUS.md:171-179` (class list); `corpus/QUALITY.md:404-412` (84), `:441-444` (86);
`.ufo/waves/round-28/check-tip-receipts.sh`.

Class vocabulary reused from `CORPUS.md:174-176` (`mistakes.md` §5: `reference-drift`, `number-drift`, `scope`,
`landing`, …). Every entry carries class · evidence pointer · captured-by · fix · how the fix is shown able to fail.

## Ready-to-paste Markdown for `corpus/lessons/round-30.md`

````markdown
## Mistakes

- **M1 — a Gate reject reason states a grep result its own pointer contradicts (class: reference-drift).**
  Evidence: `corpus/lessons/round-29.md:65` (S155 reject row) ends "a case-insensitive grep for `dryrun` and
  `version` returned no line in either file", while the same row's source cell names `kill.h`. That file carries
  `:36` `/* Flag --dryrun was passed */` and `:37` `bool dryrun;` — HTTP 200, 1 440 B, fetched
  2026-10-22T21:13:41Z, sha256 `abf8577b434096e1eb980bacc24508e8421af9edbefb0d78cf5b8b5f28160bfb`;
  `grep -in -e dryrun -e version` prints exactly those two lines. The reject decision holds (a flag declaration is
  not the send-site behaviour), so the defect is the reason, not the row:
  `round-29-verifier-spotcheck.md:126` and `:157-158`.
  Captured-by: none. QUALITY 86's awk (`corpus/QUALITY.md:441-444`) reads a reject row's id, source cell and
  `reject, <reason>` shape, never whether the reason is true; the outside spot-check's manual re-open found it.
  Fix: append a correction in this lesson (`round-29.md:65` is not edited): the grep does return `kill.h:36-37`,
  and S155 is rejected because the match is a field declaration, not the behaviour the row needed.
  Shown able to fail: the correction ships with a check that re-runs `grep -icE 'dryrun|version'` on the fetched
  bytes and requires the correction to name `kill.h:36-37`. Red-before is the round-29 row itself (the file
  matches: 2 lines, 2026-10-22T21:13:41Z; the row says "no line"); a correction that repeats "no line" fails the
  line-number assertion; at `e936482` `corpus/lessons/round-30.md` is absent (21:17:19Z), so any check that reads
  this lesson has no subject until the lesson lands.

- **M2 — two quote word-count labels are one high (class: number-drift).**
  Evidence: `corpus/lessons/round-29.md:57` labels the `journal-upload-journal.c:100-101` quote "(11 words)";
  the committed text counts **10** by `wc -w`. `:62` labels the `ca2251fc` patch guard "(17 words)"; the committed
  text counts **16**. Recomputed from the lesson bytes in this session (clock read 2026-10-22T21:13:41Z in the
  same batch); the same two are recorded at `round-29-verifier-spotcheck.md:130`.
  Captured-by: none. No QUALITY criterion counts the words of a quoted excerpt (QUALITY 86's awk,
  `corpus/QUALITY.md:441-444`, reads id/source/decision cells only); the spot-check's §4 `wc -w` re-measure found
  it.
  Fix: append a correction in this lesson giving 10 and 16 with the recompute command; `round-29.md:57` and `:62`
  are not edited. The correction belongs in the lesson only — `awk 'NR==160||NR==161' corpus/SOURCES.md |
  grep -ci word` prints 1 and that match is "wording", so rows S154/S155 carry no count label to correct.
  Shown able to fail: a counter extracts each labelled quote from the row, runs `wc -w` and compares it with the
  label. Red-before at the entering tip: `label=11 words=10`, `label=17 words=16`, exit 1; a corrected label that
  still misses by one keeps failing; the pass state is `words=10`/`words=16`, exit 0.

- **M3 — tip receipts cited only where the receipts check does not read (class: landing; round-29 R1, the
  round-28 M5 shape).**
  Evidence: `round-29-verifier-spotcheck.md:154-156`. At `b581173a` the three receipts exist under
  `.ufo/waves/round-29/evidence/`, but the citations live only at `SCORECARD.md:1796-1797` (`tip-c1.txt`,
  `tip-c2.txt`); `git show b581173a:LOG.md | grep -c 'tip-c1.txt'` prints `0` and the round-29 lesson likewise
  prints `0`. Reproduced 2026-10-22T21:17:19Z: `bash .ufo/waves/round-28/check-tip-receipts.sh b581173a 29` →
  `cited_lane=no` for `count-c1.sh` and `count-c2.sh`, `tip_receipts=unmet`, exit 1.
  Captured-by: QUALITY 84 (`corpus/QUALITY.md:404-412`) and its check, whose default report set is `LOG.md` and
  `corpus/lessons/round-<N>.md` (`check-tip-receipts.sh:37`); the author cited a third file that the default read
  set excludes and ran no check on the tip batch.
  Fix: the round-30 `LOG.md` names the three receipts before the receipts-only batch (`LOG.md:1965-1966`, landed
  `e936482`), and this lesson names the same three basenames. The check concatenates its report set, so the LOG
  citation alone turns `cited_lane=yes`; the round's routing binds both files, so both are written.
  Shown able to fail: the same command at `b581173a 29` prints `tip_receipts=unmet`, exit 1, for exactly the named
  reason (`cited_lane=no`); at the round-30 tip it must print `tip_receipts=met`, exit 0. The lesson half is
  unobserved here: `corpus/lessons/round-30.md` does not exist at `e936482` (21:17:19Z).

- **M4 — the blindness gate is bound into a counted condition before the fixed instrument exists (class: scope;
  round-29 M2 recurs).**
  Evidence: `contract.md:75-79` makes `.ufo/waves/round-30/check-blind-wave.sh` a C2 condition (selftest `PASS`;
  0 on the round-29 writer wave at `d6d5cb0a`; a violation for each planted leak class; `blind_violations=0` at
  the freeze commit), but the file does not exist at the declaration commit: `git ls-tree -r --name-only
  e936482 -- .ufo/waves/round-30` lists no `.sh` (0 matches) and the working tree has none. The round-29
  instrument's first run on its own writer wave printed `blind_violations=20`, exit 1
  (`.ufo/waves/round-29/evidence/blind-check-prefreeze.txt:3,24` at `d6d5cb0a`).
  Captured-by: round-29 M2's rule (`round-29.md:32-37`, `:96-99`: a gate enters a counted condition only after a
  receipt of it on the round's own inputs), still not a QUALITY row. This round's contract is the first
  enforcement: an unscreened gate can now only fail C2, not silently pass it.
  Fix: land the gate with `--selftest` over the four named leak classes and the round-29 wave control, and commit
  the selftest receipt under `.ufo/waves/round-30/evidence/` before the freeze commit.
  Shown able to fail: the round-29 gate is the red control on that same input (`blind_violations=20`, exit 1 at
  `d6d5cb0a`); the fixed gate must print 0 there and ≥1 per planted leak class. Both green values are unobserved
  at `e936482` (no round-30 gate exists). Residual ordering defect, narrowed not removed: condition 4's last
  clause runs the gate at the freeze commit, after the writers' reports are fixed, so a matcher blind spot
  surfaces only once the data is frozen.
````

## Reproduction ledger (observed this session)

| # | Command (cwd = lane) | Output | Time |
|---|---|---|---|
| 1 | `bash .ufo/waves/round-28/check-tip-receipts.sh b581173a 29` | `counter=count-c1.sh … cited_lane=no`; `counter=count-c2.sh … cited_lane=no`; `retention … cited_lane=yes`; `tip_receipts=unmet`; exit 1 | 2026-10-22T21:17:19Z |
| 2 | `git show b581173a:LOG.md \| grep -c 'tip-c1.txt'` (same for `corpus/lessons/round-29.md`) | `0` both times, grep exit 1 — no citation in either report | 2026-10-22T21:19:54Z |
| 3 | `git show b581173a:SCORECARD.md \| grep -n tip-c1.txt` | `1796` (`tip-c1.txt`) and `1797` (`tip-c2.txt`) | 21:13-21:17Z |
| 4 | `curl -sS https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.h` then `grep -in -e dryrun -e version` | HTTP 200, 1 440 B, sha256 `abf8577b…28160bfb`; `36:    /* Flag --dryrun was passed */`, `37:    bool dryrun;` | 21:13:41Z |
| 5 | `wc -w` on the two quotes extracted from `round-29.md:57,62` (committed bytes) | `10` and `16` (labels say 11 and 17) | 21:13-21:17Z |
| 6 | `awk 'NR==160\|\|NR==161' corpus/SOURCES.md \| grep -ci word` | `1`, the match being "wording" — no count label in S154/S155 | 21:13-21:17Z |
| 7 | `git ls-tree -r --name-only e936482 -- .ufo/waves/round-30 \| grep -c '\.sh$'` | `0` (contract, rule-text, evidence/census-start.txt, three wave1 JSON/err files only) | 21:17:19Z |
| 8 | `ls corpus/lessons/round-30.md` | `No such file or directory` | 21:17:19Z |
| 9 | `git show d6d5cb0a:.ufo/waves/round-29/evidence/blind-check-prefreeze.txt \| grep -n blind_violations` | `3:blind_violations=20`; `exit: 1` at line 24 | 21:13-21:17Z |

Read-only only: lane `git` limited to `show`, `ls-tree`, `log`, `cat-file`; no revision, index or ref touched.

## Findings for the L1

1. **Both R2 and R3 corrections target the lesson, not `corpus/SOURCES.md`.** The false reject sentence is
   `round-29.md:65`; the two labels are `round-29.md:57,62`; SOURCES rows `:160-161` carry no count label
   (ledger #6). The contract's routed R2/R3 phrase "in the round-30 lesson and `corpus/SOURCES.md`" therefore has
   no SOURCES-side target for either defect. A correction added to SOURCES would either restate a count that is
   not there or edit an older row, which R2/R3 forbid.
2. **`check-tip-receipts.sh` passes on one citing report, not the union the lesson promises.** The script
   concatenates its report set into `lane_text` and matches the receipt basename anywhere in it
   (`check-tip-receipts.sh:49,70`); QUALITY 84's prose says "cited by name in a report". So M3's lesson half is a
   routing duty, not a check requirement — the check would print `met` on the LOG citation alone.
3. **Entry M4 is a narrowed repeat, not a fresh bind.** The round-29 failure was an unscreened gate passing a
   counted condition (20 false positives, `round-29-verifier-spotcheck.md:162-163`). Round 30 cannot repeat that form: the screening
   is written inside C2 condition 4. What remains is that the gate's first run on round-30 reports happens at the
   freeze commit, so a matcher defect discovered there is a C2 miss with the data already frozen — the same
   "discover after the freeze" cost, one layer later.
4. **No fifth entry is warranted from the four candidates.** R4/R6/R7 are open work items, not mistakes with a
   red-before state; R5 is the same defect as M4.
5. **Numbering.** Round 30 has no `## Mistakes` yet; these are M1-M4 for this lesson. If another seat drafts
   `## Mistakes` text before integration, the L1 must renumber — I found no such seat: the working-tree `w1/` holds
   only the untracked `swarm-registry.json` (18:10 local), and `w1/` is absent from the tree at `e936482`.

## Limits

- M1's and M2's fixes are drafts: no correction, check or QUALITY row exists yet, so their green states are
  unobserved. Red-before states are observed (ledger #4, #5) except that no round-30 correction exists to fail
  (ledger #8).
- M3's round-30 green state depends on receipts that do not exist at `e936482` (`tip-c1.txt`, `tip-c2.txt`,
  `tip-retention.txt` are round-29 files); only the citation half is observable now.
- M4's green side needs the gate, absent at `e936482` (ledger #7). I did not write, run or simulate it, and did
  not adjudicate the round-29 gate's 20 hits myself; that count is taken from the committed receipt (ledger #9).
- No tool installed or updated (nothing needed); no pacman transaction. No host unit, PID, uid, journal message,
  `/etc/default/earlyoom` value or session field is copied here.
