# RevScorecardClaims — round-38 SCORECARD claim rows re-derived at f725f3076972e6e70595b5ac8279be524a111ff8

Verdict: **FAIL** — claim 3's after cell carries a literal the counting command does not
print, claim 2's committed supporting receipt contradicts the cell it evidences, and five
cited evidence paths do not resolve as blobs at the scored tip (untracked worktree files).

All commands below were run this session from `/home/vgpnk/Projects/shokunin/mori-shokunin`.
"Tip" = `f725f3076972e6e70595b5ac8279be524a111ff8` (also `git rev-parse HEAD`). The lane
working tree is dirty (SCORECARD.md and two evidence receipts modified; seven evidence
files untracked); the rows under review are the **committed** cells at the tip — the
worktree already carries a mid-flight correction naming this seat, reviewed separately below.

## Claim → declared vs observed

| # | cell element | declared (committed SCORECARD.md:2153-2155) | observed (fresh run) | verdict |
|---|---|---|---|---|
| 1 before | fabricated binding `C2=met` (r37 counter) | `C2=met` | `python3 .ufo/waves/round-37/count-c2.py 4255cb2d… --repo .ufo/waves/round-38/scratch/RevScorecardClaims/fabricated-binding` → `C2=met`, EXIT=0 (sandbox built by `fixtures/make-witness-sandbox.py f725f30…` under my scratch) | PASS |
| 1 before | fabricated binding `C4=unmet` | `C4=unmet` | `count-c4.py 4255cb2d… --repo <sandbox>` → `C4=unmet`, EXIT=1 (`capability FAIL missing=['evidence/no-such-receipt.txt']`, `live_rows FAIL`) | PASS |
| 1 before | do-nothing arm at `e37dcc6` | `C4=unmet` | `count-c4.py e37dcc6` → `C4=unmet` EXIT=1 (`anchors FAIL anchors=0`, `capability FAIL missing=['evidence/drift-live-r37.txt']`) | PASS |
| 1 after | real binding `C4=met`, exit 0 | `C4=met`, exit 0 | `count-c4.py f725f30…` → `C4=met` EXIT=0, all 4 checks PASS, 3 negatives rejected | PASS |
| 2 before | `CONFORM=unmet`, 6/6 FAIL on r37 counters | `CONFORM=unmet` (6/6 FAIL) | `conform.py e37dcc6 --counter round-37/count-c1.py --counter round-37/count-c2.py` → `CONFORM=unmet` EXIT=1, six checks FAIL | PASS |
| 2 after | `CONFORM=met` (6/6) + `CONFORM_SELFTEST pass=6 fail=0` | `CONFORM=met` | `conform.py f725f30… --counter count-c1.py --counter count-c4.py` → `CONFORM=met` EXIT=0, six PASS; `--selftest` → `CONFORM_SELFTEST pass=6 fail=0` EXIT=0 | PASS (cell); but committed receipt contradicts — finding F2 |
| 3 before | gate prints no timing field (0 occurrences) | 0 occurrences | `git show e37dcc6:tools/mori-sources-appendonly.py` run at `e37dcc6 --round-base f10a320d` → no `supersede_timing` line; `grep -c 'stale_supersede\|superseded_as_of'` on those bytes = 0; `evidence/gate-before.txt` contains none | PASS |
| 3 after | `superseded_as_of=[S069,S182,S193] stale_supersede=[]` at the tip | the literal above | `tools/mori-sources-appendonly.py f725f30… --round-base f10a320d` prints `supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] stale_supersede=[]` | **FAIL — F1** |
| 3 after | `stale_supersede=[S069]` at `e37dcc6` | `stale_supersede=[S069]` | same command at `e37dcc6` → `supersede_timing superseded_as_of=[S041,…,S193 minus S069] stale_supersede=[S069]` | PASS |

## Findings

**F1 (HIGH) — claim-3 after cell literal does not match the gate's real `supersede_timing`
line.** `SCORECARD.md:2155` (blob `28778c5` at tip) declares
`supersede_timing superseded_as_of=[S069,S182,S193] stale_supersede=[]`. The counting
command at the tip prints `superseded_as_of=` with **all 18** superseded ids
`[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193]`
— every superseded id whose latest superseding row's landing commit postdates its last
immutable-cell edit (`tools/mori-sources-appendonly.py:282-289`, P-C6). The cell's 3-id list
matches the *`round_changed`/`superseded`-this-round* shape (`round_changed=[S182,S193]`,
S069 changed-but-not-round-changed), i.e., the wrong field was transcribed. The
untracked-but-present `evidence/gate-after.txt:22` records the same 18-id line, so the cell
misquotes its own receipt. `stale_supersede=[]` and the `e37dcc6` discriminator
(`stale_supersede=[S069]`) are both correct — the semantic claim (postdating superseder
discharges; predating does not) survives; the literal fails acceptance.

**F2 (MEDIUM) — committed `evidence/c5-after.txt` at the tip contradicts claim 2's
after cell.** `git show f725f30:.ufo/waves/round-38/evidence/c5-after.txt` records a run
against `daa1d4d` showing `check bounded_reads FAIL (count-c4.py … cap=False)` and
`CONFORM=unmet EXIT=1`. The cell declares `CONFORM=met` at the tip — true when re-run
(the tip's `f725f30` commit added the `MAX_BLOB_BYTES` cap to count-c4.py; my fresh run
prints `bounded_reads PASS` for both counters, `CONFORM=met` EXIT=0) — but the receipt
committed as the claim's evidence shows the *pre-fix* run. The corrected receipt exists only
as an uncommitted worktree modification. At the scored tip, the claim's evidence cell points
at bytes that print `CONFORM=unmet`.

**F3 (MEDIUM) — five cited evidence paths do not resolve at the tip.** `git cat-file -e
f725f30:<path>` fails for: `evidence/v3-token-control.txt`, `evidence/c4-witness.txt`
(claim-1 evidence cell); `evidence/c5-after-selftest.txt` (claim-2 evidence cell **and**
capability row round-38 C2, where it is written wave-relative — `evidence/c5-after-selftest.txt`
is not a repo-relative path under either reading, unlike its sibling
`.ufo/waves/round-38/evidence/c5-after.txt`); `evidence/gate-after.txt` (claim-3 evidence
cell **and** capability row round-38 C3); `evidence/gate-selftest-after.txt`;
`evidence/gate-after-e37dcc6.txt` (contract evidence list). All exist only as untracked
worktree files (wave-1's receipts, never committed). Claims 1 and 3 therefore have *no
committed* after-receipt for the witness-sandbox arm and for the `supersede_timing` line;
claim 2 has no committed receipt at all that prints `CONFORM=met` (see F2). The claims'
values are correct when re-run — the receipts cited at the scored tip are absent.

**F4 (LOW) — contract text vs gate selftest count.** Contract §C3 says "--selftest gains
two cases". The gate went 8 → 9 cases (`gate-selftest-before.txt` pass=8, my run of the tip
tool: `pass=9 fail=0`): one new case `supersede before edit` (`tools/mori-sources-appendonly.py:441`);
the `supersede after edit` expectation was folded into the pre-existing `superseding row`
case's expected dict (`:437`, now asserting `superseded_as_of: ["S001"]`). Semantics fine;
the "two cases" phrasing is off.

**F5 (LOW) — declaration cites the superseded pin file.** SCORECARD.md:2147 says "pins in
`evidence/freeze-r38.txt`". At the tip, `count-c1.py`/`count-c4.py` blobs hash to
`9ebf10a1…`/`3340d594…` = the **v2** pins (`evidence/freeze-r38-v2.txt`), not the v1 file's
`4e59eeff…`/`5d416a1c…`. Contract.md and conform.py match both files. Harmless given
v2's header explains the versioning, but the declaration's pointer is stale.

## Capability rows — path resolution at the tip (repo-relative)

| row | cited path | resolves at `f725f30`? |
|---|---|---|
| round-38 C1 | `.ufo/waves/round-38/count-c4.py` | yes |
| round-38 C1 | `.ufo/waves/round-38/evidence/c4-after.txt` | yes (committed rev names `daa1d4d`, see F2's sibling issue — value `C4=met` still matches) |
| round-38 C1 | `.ufo/waves/round-38/fixtures/` | yes |
| round-38 C2 | `.ufo/waves/round-38/conform.py` | yes |
| round-38 C2 | `.ufo/waves/round-38/evidence/c5-after.txt` | yes (content contradicts cell — F2) |
| round-38 C2 | `evidence/c5-after-selftest.txt` | **no** — absent at tip and malformed under repo-relative reading (F3) |
| round-38 C3 | `tools/mori-sources-appendonly.py` | yes |
| round-38 C3 | `.ufo/waves/round-38/evidence/gate-after.txt` | **no** — untracked at tip (F3) |

`count-c4.py`'s own `capability` check only parses the round-37 `source-drift re-fetch
probe` row (resolved paths `tools/mori-source-drift.py`,
`.ufo/waves/round-37/evidence/{c2-after-v3,drift-live-r37}.txt` — all resolve at the tip);
the round-38 rows are unmechanized text, checked above by hand.

## Axes cells — wrong-move check

Committed axes table (SCORECARD.md:8-15 at tip): scores unchanged from round 37
(coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6). Round 38
claims moves on calibration/operability/depth only — consistent with "score held"
convention; freshness cell carries the corrected text verbatim ("round-37 C2 is
re-attributed to operability … round 38 claims no freshness move"), matching the
superseded-text note at :2169-2177. No axis cell claims a move the receipts contradict.
PASS.

## Notes / residual risk

- `conform.py`'s `tip=` field in `head_pin` prints the **live** lane tip at run time:
  the committed `c5-before.txt` receipt shows `tip=1f1e9968…` while my re-run prints
  `tip=f725f30…`. Receipts are not byte-reproducible across time by design (P-C5 wants
  the measured head); disclosed, not a defect.
- `conform.py`'s `bounded_reads`/`scratch` audit reads the `--counter` files from the
  worktree, not `<rev>` blobs — correct for this round (worktree == tip for all three
  instruments), but a caller passing `<rev>` ≠ worktree HEAD audits the wrong bytes.
  Not exercised by the frozen contract; flagged for the next counter version.
- The claim-3 counting command exits 1 at the tip (`appendonly_violations=18` — the
  historical in-place edits); the cell makes no exit-code claim for claim 3.
- Worktree already contains the same-round correction for F1 (SCORECARD.md
  worktree diff: cell rewritten to the 18-id literal + appended correction note naming
  `w2/RevScorecardClaims` and quoting the superseded text). My FAIL stands against the
  **committed tip**; the uncommitted remediation is consistent with this report.
- `conform.py` selftest cost ~42 s; all runs above completed inside normal timeouts.

## Checks run (all this session)

`count-c4.py` at `f725f30` (C4=met), at `e37dcc6` (C4=unmet), at witness-sandbox `4255cb2d`
(C4=unmet); `round-37/count-c2.py` on the sandbox (C2=met); `conform.py` at `f725f30`
(CONFORM=met) and `--selftest` (pass=6); `conform.py` at `e37dcc6` vs r37 counters
(CONFORM=unmet, 6 FAIL); `mori-sources-appendonly.py` at `f725f30` and `e37dcc6` (18-id
line / `stale_supersede=[S069]`), tip `--selftest` (pass=9), `e37dcc6` tool bytes at
`e37dcc6` (no timing line, 0 timing refs in source); `git cat-file -e` over every cited
evidence/capability path; sha256 of committed counters vs both freeze-pin files.

Tooling: none installed (pacman paused; nothing needed beyond git/python3).
Report: .ufo/waves/round-38/w2/RevScorecardClaims.md
