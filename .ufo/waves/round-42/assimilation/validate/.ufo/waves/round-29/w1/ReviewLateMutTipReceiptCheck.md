# ReviewLateMutTipReceiptCheck — re-verification of round-28 w2 `MutTipReceiptCheck.md`

Seat: `MoriR29.ReviewLateMutTipReceiptCheck` (leaf reviewer; no subagents, no background jobs).
Item: re-verify every finding of the inherited untracked file
`.ufo/waves/round-28/w2/MutTipReceiptCheck.md` against the committed lane at
`7118f320a5ef18d20c1e361eff77db0e1a97b2d6`, in a sandbox clone; decide impact on round 28's
admitted C1/C2 verdict and QUALITY 83/84; privacy-audit; recommend commit or dispose.
The oom-killers tool was never opened, run or quoted. Round-26/27/28 w1/w2 report dirs were
not opened beyond the one named file.

## Method and drift check

- Sandbox: `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin`
  into `/fast/scratch/hyaku/mori-r29/MoriR29.ReviewLateMutTipReceiptCheck/lane/` (lane untouched;
  only read-only git was run in the lane).
- The wave-2 seat's scratch harness was still on disk; I copied `run.py`,
  `fixtures/build.py` and the detector wrapper into my scratch, patched only the scratch-path
  constants, rebuilt all 32 fixtures fresh in my clone (temp index + `commit-tree`; fresh
  fixture hashes), and re-ran every mutant plus the restore check.
- Detector bytes: wrapper and committed blob are byte-identical (`diff` clean), sha256
  `172f140751de38b753cd6d5eca37fe215855dc8828933e890b4879f4cc3a492c` at both `f2de0ee` and
  `7118f320`; the script blob is `184904d3c25dd5dad99ab6773a84a98cebad47d0` at both revs
  (`git rev-parse <rev>:…`), and no commit in `f2de0ee..7118f320` touches it
  (`git log --oneline <range> -- .ufo/waves/round-28/check-tip-receipts.sh` is empty).
  So no finding can be "closed by a later commit" as code; statuses below are
  reproduced-open or superseded-situation.
- Tooling directive: no tool installed or upgraded (bash, git, python3 sufficed).

## Re-run results — all 32 fixture verdicts match the report row for row

Re-run command: `python3 run.py` in the sandbox (sets `GIT_DIR`/`GIT_WORK_TREE` to the sandbox
clone, `GIT_INDEX_FILE` to a temp path; detector wrapper invoked per fixture `<T> 28`).
Observed partition: baseline `s00_met` exit 0 (met); 14 fail-open survivors (m01b, m01d, m02c,
m02d, m02e, m03b, m03c, m05, m07, m08, m10, m12, m14, m15); 16 killed (m01a, m01c, m01e, m02a,
m02b, m03a, m03d, m03e, m04a, m04b, m04c, m06, m09, m11, m13, m16); m03f exit 0 (correct
accept). Restore `s00_met` after all mutants: exit 0, `tip_receipts=met`.
Compact observed verdicts (fixture=exit:verdict):

```
s00_met=0:met m01a=1:killed m01b=0:survived m01c=1:killed m01d=0:survived m01e=1:killed
m02a=1:killed m02b=1:killed m02c=0:survived m02d=0:survived m02e=0:survived
m03a=1:killed m03b=0:survived m03c=0:survived m03d=1:killed m03e=1:killed m03f=0:met
m04a=1:killed m04b=1:killed m04c=1:killed m05=0:survived m06=1:killed m07=0:survived
m08=0:survived m09=1:killed m10=0:survived m11=1:killed m12=0:survived m13=1:killed
m14=0:survived m15=0:survived m16=1:killed  restore(s00_met)=0:met
```

Example observed output (m01b, survivor): `counter=count-c1.sh
receipt=.ufo/waves/round-28/evidence/r28-tip-c1.txt measured=965193ff… cited_lane=yes
cited_fleet=na | … | tip_receipts=met`, exit 0.

## Findings (the report's 8 fail-open paths) — each re-verified

All detector line citations are `.ufo/waves/round-28/check-tip-receipts.sh` at `7118f320`.

- **F1 wrong parent accepted when P appears anywhere in the body** (report items 1; m01b, m12).
  Mechanism confirmed at `:63` and `:84` (`case "$body" in *"$P"*` — whole-body substring, not
  the `revision:` line). Re-run: both exit 0, `tip_receipts=met`. **Status: reproduced open.**
- **F2 no `revision:` field required** (item 2; m01d). No line of `:60-65` mentions a revision
  field; P inside the `command:` line satisfies `:63`. Re-run: exit 0, met. **Reproduced open.**
- **F3 exit value never checked** (item 3; m02c). `:64` is `grep -qE '^exit: *[0-9]+'` —
  value-blind. Re-run: receipt with `exit: 1` accepted, met. **Reproduced open.** Live
  instance: the real committed receipt `.ufo/waves/round-28/evidence/tip-retention.txt` at
  `1fc6bb0e` records `exit: 1` and the real check still prints met (see S2). The header comment
  only demands "an `exit:` line", so this is a spec-level gap (gate certifies that a receipt
  exists, not that the run passed), not an implementation bug.
- **F4 "at least one stdout line" not enforced; headers count toward the 3-line floor**
  (item 4; m02d, m02e). `:65` counts non-empty body lines (`grep -cE '.' >= 3`). Re-run: both
  exit 0, met. **Reproduced open.**
- **F5 citation is a bare basename substring over concatenated report text** (item 5; m03b,
  m03c, m08, m14). `:70` and `:91` (`case "$lane_text" in *"$base"*`). Re-run: longer-name
  citation, negative sentence ("No receipt named …") and suffix name all accepted, met.
  **Reproduced open.**
- **F6 only the first body-passing receipt per counter is citation-checked; collation decides**
  (item 6; m10 survived vs m11 killed). `:66` (`hit=$f; break`) over `ls-tree|sort` order
  (`:45`). Re-run: m10 exit 0 met, m11 exit 1 killed — exactly the reported pair.
  **Reproduced open.**
- **F7 a counter is satisfied by any receipt whose body names it** (item 7; m05 shared receipt,
  m07 c1 receipt mentioning `count-c2.sh`). `:62`. Re-run: both exit 0, met — one shared
  receipt counted for both counters; a note-mention served as the c2 receipt.
  **Reproduced open.**
- **F8 counter set is grepped from the contract at `$R`, so a tip batch can edit the contract
  to drop a counter** (item 8; m15 survived; m16 killed because retention is matched by the
  literal `mori-retention-gate.py` at `:82`, not the contract grep at `:43`). Re-run: m15 exit
  0 met, m16 exit 1 killed. **Reproduced open.**

Killed directions: all 16 killed fixtures reproduced exit 1, including `exit=0` style (m02b),
indented `exit:` (m09), absent receipt / receipt outside `evidence/` (m04a/b/c, m06), short or
foreign revision with P absent (m01a/c/e), uncited selected receipt (m03a/d/e), retention
missing exit line (m13), contract dropping the retention clause (m16). The note "exit=0 is
house style in 7 of the 10 pre-existing round-28 evidence files" verified: at `f2de0ee`,
`git grep -l '^exit='` = 7 files, `'^exit:'` = 3 of 10.

Minor discrepancy (cosmetic): the fixture manifest labels m03f `expect=unmet`, while the
report's table (row 17) and observed behavior say met (correct accept — the lesson is a default
report path at `:39`). The report's classification is right; the manifest label is stale.
No other mismatch between the report's 32 rows and observation.

## Situational claims — re-verified at the entering tip

- **S1 "structurally yes" on a met fixture** — reproduced (s00 baseline and restore, exit 0).
- **S2 "on the real lane now (f2de0ee): no — every receipt MISSING, measured d21b8bd3"** —
  reproduced exactly at `f2de0ee`: observed `counter=count-c1.sh receipt=MISSING
  measured=d21b8bd38b1bf72ec903a19ed543c615564e8278` (×2 more), `tip_receipts=unmet`, exit 1.
  **Status: superseded by a later commit.** The round-28 last batch `1fc6bb0e` (first parent of
  the entering tip `7118f320`; its own parent `5ef4e8db`) added exactly three receipt files —
  `git diff --stat 5ef4e8db 1fc6bb0e`: "3 files changed, 50 insertions", all under
  `.ufo/waves/round-28/evidence/` — and the detector now passes there: observed
  `counter=count-c1.sh receipt=…tip-count-c1.txt measured=5ef4e8db… cited_lane=yes`,
  same for c2 and retention, `tip_receipts=met`, exit 0.
- **S3 caveats**: (a) `exit: 0` colon style — confirmed (m02b killed; real c1/c2 receipts use
  `exit: 0`). (b) full 40-hex parent in `revision:` — confirmed in the real receipts
  (`revision: 5ef4e8db…` = `1fc6bb0e^1`), though the detector does not enforce it (F2).
  (c) fleet-report mode blocked on a missing `.ufo/reports/round-28/mori.md` — **closed**: the
  file exists at the pinned fleet rev `63729047644f839fe4c8cc97abd0d8bf741a5787` (also current
  fleet HEAD) and cites all three receipt basenames (`grep -c` = 3 matching lines). Clean-env
  fleet-mode run `check-tip-receipts.sh 1fc6bb0e 28 --report-repo /home/vgpnk/Projects/shokunin
  --report-rev 63729047…`: observed `… cited_lane=yes cited_fleet=yes` ×3,
  `tip_receipts=met`, exit 0. (Disclosure: my first fleet-mode attempt exported `GIT_DIR` to
  the sandbox and was invalid — the detector's fleet `git -C` read the sandbox odb,
  `cited_fleet=no`; redone with `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE`.)

## Impact on round 28's admitted verdicts and QUALITY 83/84

- **C1/C2: no change.** All reproduced findings live in `check-tip-receipts.sh`, a receipt
  hygiene gate, not in `count-c1.sh`/`count-c2.sh`. The committed tip receipts carry full
  counter stdout — `tip-count-c1.txt`: `C1=met` / `exit: 0`; `tip-count-c2.txt`: `C2=met` /
  `a2_selftest=PASS 30/30` / `frozen32_selftest=PASS 32/32` / `exit: 0` — measured at
  `5ef4e8db`, and the fleet MANIFEST at the pinned rev records mori round 28 `admitted: true`
  with `trends.quality: "improved"` and a verification note that C1 and C2 were re-measured
  with receipts evidence-verified (paraphrased; no session fields copied).
- **QUALITY 83/84: no flip.** The detector header self-describes as the "Round 28, QUALITY 84
  check" (its own comment, line 1-2); round 27's counterpart was labeled "QUALITY 81"
  (`.ufo/waves/round-28/contract.md:18`). I found no committed numeric 83/84 in the files I may
  read (SCORECARD Axes table `SCORECARD.md:8-15` holds per-axis scores 5-7; SHONEN.md and
  MANIFEST trends carry no number) [INFERENCE: the numeric ledger sits in wave/closure
  bookkeeping outside my read bounds]. On the substance: at the report's timestamp the gate was
  unmet at `f2de0ee`; at the admitted round-28 tip chain it is now met — lane mode at
  `1fc6bb0e` and fleet mode at the pinned rev both exit 0. The 14 fail-open directions are
  hardening debt, not live flips: no real batch exploited them. Flag for the L1: the one live
  consequence is F3 — `tip-retention.txt` records `exit: 1`, so the gate's retention leg
  certifies existence of a scan receipt, not a passing scan; whether round 28's admission
  relied on retention passing is outside this item and unjudged here.
- **Latent risk named**: with F5+F6+F7 combined, a tip batch could satisfy the gate with one
  self-authored receipt per counter whose "stdout" is invented, cited by a substring —
  worth a round-29+ hardening item (require `revision:` line equal to P, exit value 0 for
  counter receipts, full-path citation, one receipt per counter, contract-read at a pinned
  parent rev).

## Privacy audit of `MutTipReceiptCheck.md`

Grepped the file for `uid=`, `pid`, `pgid`, `user-<digits>.slice`, `user@<digits>.service`,
`.service`, `session`, `journal`, `--prefer/--avoid/--ignore`, `/etc/default`, OMP settings or
session-store keys: zero hits (grep exit 1). Contents are hashes, fixture names, script
behavior, scratch paths and invented fixture command lines. No host command lines, no
user-session identifiers, no settings values. **Safe to commit.**

## Recommendation

**Commit as evidence** (alongside this re-verification, which supersedes its two situational
sections). Reasons: (1) round-29 contract "Routed hygiene" item 1 prescribes exactly
commit-as-evidence-or-dispose for late round-28 outputs, and this file is genuine, fully
reproducible detector analysis — every one of its 32 fixture verdicts, both real-lane
observations and the house-style note reproduced; (2) its 8 fail-open findings are the best
available hardening backlog for `check-tip-receipts.sh`; (3) privacy-clean. Condition: a future
reader must not run the detector at the round-28 tip expecting failure — since `1fc6bb0e` the
gate passes (lane and fleet modes); the file's "cannot pass" statements were true only at
`f2de0ee` and say so.

## Residual risk and verification gaps

- Fixtures were rebuilt fresh (new commit hashes by design); equivalence to the original run is
  behavioral (all 32 verdicts + notes match), not byte-level.
- I did not test any fixed/alternate detector — the item was verification, not repair.
- The meaning of `exit: 1` in `tip-retention.txt` (retention gate state at `5ef4e8db`) was not
  investigated — outside this item; flagged above.
- The numeric QUALITY 83/84 ledger was not located within my read bounds (see INFERENCE above).
- LOG.md and the round-28 lesson were touched only by `grep -c` for citation counts, never read,
  per the wave's blindness bounds.
