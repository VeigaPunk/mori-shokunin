author: hyaku closure (non-author integrator, @m_zfl)
round: mori 85 (lane round 85, attempt 1) — non-author closure verification
report: `.ufo/reports/round-85/mori.md` (fleet repo, `d8927d9f` + `49693fa7`)
lane repo: `mori-shokunin` @ `66772cae74b4509ec2b38db6fd8b562438f379e6` (branch `master`, pushed)
entering: `2cc4b1ae35a83e4fd3fc48bae842bdf38df2e80e`
dispatch digest (copied from `.ufo/watchdog.log`, mutable):
`2026-11-04T07:48:48-03:00 launch mori round=85 pgid=2001209 driver=hyaku-inline attempt=1`
`2026-11-04T08:56:07-03:00 complete mori round=85; hyaku-inline attempt=1`

This reviewer authored no part of the round. Claims were re-derived with plain measurements over
committed bytes (grep, wc, git, sha256) and compared with the reported values; where a claim rests
on a lane-owned counter or selftest, its **committed evidence** was verified and the instrument was
not executed (PROTOCOL §Gate standard, Closure consequence). No lane-authored file (report,
SCORECARD, LOG, lessons, SKILL, PROVINCE) was edited and no `[x]` was written into `SHONEN.md`.

## Conformance (step 1)

| Check | Result | Evidence |
|---|---|---|
| Report committed in the fleet repo by the lane identity | pass | `git log --format='%an %ae %H' -- .ufo/reports/round-85/mori.md` → `mori-shokunin mori@shokunin.local d8927d9f…` (08:48:32 -0300) and `49693fa7…` (08:55:35 -0300) |
| Report lands after the lane's work | pass | lane tip `66772cae` committer 08:55:04 -0300; report commit 08:55:35 -0300 (31 s later) |
| `SHONEN` heading, one line per box | pass | report `## SHONEN` (1 occurrence), four `[~]` bullet lines (199-211), each with a resolvable pointer; `SHONEN.md` unchanged by the round (no `[x]`) |
| Every cited lane commit exists and is an ancestor of the branch | pass | 26 distinct hex tokens in the report tested; every commit hash resolves and `git merge-base --is-ancestor <h> master` holds (`2cc4b1ae ab260865 79bb4ed8 4ffd5a2d 89f82eac 91f657f6 25a74d4c 42865833 0649e5ca 3dc05084 d78dd652 66772cae 729b794a`). Non-commits: `7fd5e043` = sha256 prefix of `make-receipts.sh` (measured `7fd5e04346…`), `a558c89f` = sha256 prefix of the S600 pin (measured `a558c89f5f…`); `786aab60 409de5e8 f2efbfcb` are this round's scratch fixture commits, disclosed as non-resolving with committed rebuild recipes (`evidence/c3-controls.txt`) |
| No uncommitted round work; pushed | pass | `jj-lane.sh state` → `branch=master local=66772cae74b4… remote=66772cae74b4… ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` empty; `ls-remote origin refs/heads/master` = `66772cae74b4509ec2b38db6fd8b562438f379e6` |
| Prompt committed and carries the contract | pass with a defect | `.ufo/prompts/mori-round-85.md` (704 lines) at `f9a8a8d2`, committed by the **lane identity** `mori-shokunin <mori@shokunin.local>` at 07:47:45 (launch 07:48:48) — the integrator owns this path; recurrence of D84-1. `diff` of the prompt's §1–§5 against `templates/round-prompt.md` shows only placeholder substitution; the five child-lane items are present (report path §4 line 99; commit-then-push line 131; `SHONEN` heading §4 line 118; hash-citation rule §4 line 107 + addendum §4 line 513/517; write scope addendum §3 line 443); §2b frontier step, §3 L2 floor and §6/§7 hyaku addendum present |
| Real report, not a marker | pass | work performed with evidence pointers, landed changes tied to `LOG.md` Round 85, resolvable commit citations → status `ok` |
| Wave shape | pass | `w1-dispatch.json` `counts={spawn:12,resume:0,total:12}` under band 8–16; registry roles 4 executor / 2 scribe / 1 scout / 2 reviewer / 1 critic / 1 mutation-tester / 1 connector, attack 4/12 = 33.3 %; `w1-results.json` 12 entries, `Mo85R02C2` empty (dead seat, disclosed), 11 seat reports on disk |
| Fleet repo cleanliness | pass | `git -C /home/vgpnk/Projects/shokunin status --porcelain` shows no file written by this round: `.scratch/*` and `.ufo/l0-questions.md` are run state / another lane's (mado r78) append; untracked `after` (mtime 2026-11-03, a SCORECARD scratch excerpt) and `.ufo/reports/round-80/mado.md` predate or belong to other lanes |

Status-neutral defects are named in **Routed defects**.

## Per-claim re-check

### C1 — operability (score 7) — verdict **improved**

Target: `C1=met mutants=2 killed=2 survivors=0 total=2 arms=17 r84=met`.

Re-measured over committed bytes (no lane counter executed):
- `git show 2cc4b1ae:.ufo/waves/round-84/count-c1.py | grep -c 'cases.append('` → **15**.
- `git show 66772cae:.ufo/waves/round-84/count-c1.py | grep -c 'cases.append('` → **17**.
- `git diff 2cc4b1ae 66772cae -- .ufo/waves/round-84/count-c1.py` → `29 insertions(+), 0 deletions`;
  every added hunk sits inside `selfcheck()`; `grade()`/`green()`/`killed()` untouched; the two new
  labels `killed_mutant_with_coupling_not_equivalent` and `duplicate_coupling_not_equivalent` occur
  exactly once each at the tip (`grep -n`, lines 285 and 299 of the tip blob).

Evidence-verified (committed runs, not re-executed):
- `.ufo/waves/round-85/evidence/after-r85.txt` (committed `42865833`): `MUTANT count-c1.py
  X1_killed_rescued_as_equivalent killed rc=1`, `X2… killed rc=1`, then `C1=met mutants=2 killed=2
  survivors=0 total=2 arms=17 r84=met rev=25a74d4c34e8`, rc 0.
- `.ufo/waves/round-85/evidence/tip-r85.txt` (committed `66772cae`): same tail
  `rev=d78dd6522889`, rc 0.
- Kill-rule behaviour: `w1/Mo85E01C1Arms.md:55/58/62` — pristine `pass=17 fail=0` rc 0; X1 and X2
  mutated copies `pass=16 fail=1` rc 1 with the FAIL line naming the arm.
- The r84 counter's own frozen 4-mutant line at the graded bytes:
  `w1/Mo85E01C1Arms.md:74` → `C1=met mutants=4 killed=2 equivalent=2 survivors=0 total=4
  pristine=green detector=green` rc 0 (also the source of the after line's `r84=met` token).

### C2 — calibration (score 5, tied lowest) — verdict **improved**

Target: `C2=met receipts=3 bindings=5 bound=5 revs=3 limits=3 cmd=3 summary=3 mismatch=0`.

Re-measured (my own hashes over the committed blobs at the receipts' own `# rev: 25a74d4c…`):
- `.ufo/waves/round-85/count-c1.py` → `da5fb27b9cd9b9cfbbefc58fb2465fb162f796cd280f82d0aeee0e8deca485fe` — MATCH
- `.ufo/waves/round-85/count-c2.py` → `497738932080b8044142e5f49a8a4f3151ab16b876d77d25a8e0771785f8b918` — MATCH
- `.ufo/waves/round-85/count-c3.py` → `43ad71d8104df29f1be8e3e0cef20d485e35a5f3f70d4994d70adc67b88a2724` — MATCH
- `tools/mori-record-sweep.py` → `b8683be24e28ce4e79730b46615174d888af4c22ac7ee4fe16b97048516e8efa` — MATCH
- `tools/mori-claim-sweep.py` → `4ac6b52615a427d1f7d8993ab636a5830bcde744c4a51f22d9157833d940ba1d` — MATCH

Grammar re-measured: each receipt carries exactly one `# cmd:`, one `# rev:` (40-hex), one
`# limits:` (contains the word `limit`, ≥3 words) and exactly one `# ---`; bindings 3+1+1 = **5**;
the frozen summary tokens (`C1=met`, `RECORD_SWEEP`, `CLAIM_SWEEP`) appear after the separator;
`25a74d4c` is an ancestor of the tip. The three counters' bytes at `25a74d4c` and at the tip are
identical (`sha256` prefixes equal), so the after reading binds the graded bytes.

Evidence-verified:
- `.ufo/waves/round-85/evidence/tip-r85.txt` → `C2=met receipts=3 bindings=5 bound=5 revs=3
  limits=3 cmd=3 summary=3 mismatch=0 detector=green rev=d78dd6522889`, rc 0. The three receipt
  files are byte-identical from `42865833` to the tip (`git diff --stat` empty), so this run grades
  the committed receipt set.
- Defeats: flipped digest → `C2=unmet … bound=4 mismatch=1` rc 1; headerless receipt →
  `C2=unmet … mismatch=7` rc 1 (`evidence/controls-r85-defeated.txt`).

### C3 — depth (score 5, tied lowest; **capability acquisition**) — verdict **improved**

Target: `C3=met observed=3 aa=stable own_tokens=64 subject_tokens=64 unmatched=0 unnamed=0`.

Re-measured:
- `git cat-file -e 2cc4b1ae:.ufo/waves/round-85/count-c3.py` → `fatal: … exists on disk, but not in
  '2cc4b1ae'`, rc **128** — the counter, i.e. the claimed capability, is absent before the round.
- Counter at the tip carries `20` `cases.append(` selftest arms; committed precondition
  `C3_COUNTER_SELFTEST pass=20 fail=0` (`evidence/c3-controls.txt:49`,
  `w1/Mo85E03C3Fixture.md:41`).
- Corroboration for `own_tokens=64`: `corpus/evidence/drift-classification-r82.txt` line 4
  `# Token count: 64` against the same census subject.

Evidence-verified:
- `after-r85.txt`: `C3=met observed=3 aa=stable own_tokens=64 subject_tokens=64 subject_deltas=0
  unmatched=0 unnamed=0 detector=green rev=25a74d4c34e8`, rc 0; `tip-r85.txt`: same at
  `rev=d78dd6522889`, rc 0.
- Load-bearing controls (`evidence/c3-controls.txt`): census-stub fixture →
  `C3=unmet observed=3 aa=unstable own_tokens=0 rcs=1,1,1` rc 1; stale-subject fixture
  (single-difference) → `subject_tokens=63`, everything else passing, rc 1; pristine anchor → met.
- Capability rows entered in `SCORECARD.md` (`### Capabilities (round 85)`, three rows) and the
  `PROVINCE.md` Round-85 note in the same round.

## No-harm check (owned axes)

- `git diff --numstat 2cc4b1ae 66772cae` for lane files: `LOG.md 69/0`, `PROVINCE.md 25/0`,
  `SCORECARD.md 54/0`, `SKILL.md 1/0`, `corpus/QUALITY.md 102/0`, `corpus/README.md 6/0`,
  `corpus/SOURCES.md 3/0`, `corpus/lessons/round-85.md 161/0`,
  `corpus/knowledge/receipt-provenance-r85.md 88/0` — **no deletions anywhere**.
- SCORECARD axis cells unchanged (operability 7, calibration 5, depth 5, coverage 6, freshness 5,
  adjacency 6); the round states "no score moves"; no axis retired.
- `SOURCES.md` 372 → 374 rows by `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`,
  append-only (no `status`/`recheck`/`used-by` cell of an existing row moved).
- Standing battery unchanged: `BATTERY pass=57 setup=4 fail=0`, `BATTERY 57/61`
  (`evidence/battery-r85.txt`, header carries `rev=4ffd5a2d … date=…`).
- Sweeps green at the measured bytes: `RECORD_SWEEP … revisions=0` rc 0;
  `CLAIM_SWEEP … pointers=274` rc 0.

## Discernment spot-check (LEARNING.md — non-author)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S600 — Reproducible Builds, "Definitions", `https://reproducible-builds.org/docs/definition/` | **ADMIT** (tier A, `docs`, `mined`) | live URL at closure: HTTP 200, no redirect, 37681 bytes, 3662 lines, sha256 `a558c89f5f27dffa69fd1dc49904179b60233bcfdfc64807abfe1acf37518ebb`; committed pin `corpus/evidence/sources-r85/rb-definition-1.html:175-177` | **agree** | The ≤25-word quote is verbatim: "given the same source code, build environment and build instructions, any party can recreate bit-by-bit identical copies of all specified artifacts" — 21 words at raw lines 175-177; it grounds the receipt property (K1/K2) and tier A is apt for the primary definition page; the live bytes equal the three committed pins byte-for-byte at closure, so the open-and-pin rule holds |
| S601 — "An Empirical Evaluation of Manually Created Equivalent Mutants", `arXiv:2404.09241` | **REJECT** (row kept `rejected`; D84-3 row) | live URL at closure: HTTP 200, 40386 bytes, 596 lines, sha256 `4bcb20b23ad5046657a65a29595517da973128a289ff75ba13ad8926c5511a80`; committed pin `corpus/evidence/sources-r85/arXiv-2404.09241-abs.html:121` | **agree** | The ≤25-word quote is verbatim: "mutants that differ only in syntax but not semantics, hamper this process" — 12 words in the abstract body; the paper studies humans creating equivalent mutants in a gamified setting and reports a cost, not an adjudication procedure, a kill tally or a gate rule; the row keeps it with its reason and a stated flip condition, which is what `status: rejected` is for; live bytes match the pin |

Both decisions were re-derived from the source, not from the round's prose. The lesson Gate records
URL, access date (2026-11-04) and a located quote for both new rows, as contract v1 rule 1 requires.
Census re-run at closure: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
mori` → `mori ok /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`, rc **0**, 35
tolerated `W04` duplicate-URL warnings, zero `E` codes — matches the report's before and after
readings.

## Trend verdicts (non-author)

- **expansion: improved** — one admitted knowledge entry on ground the coverage map did not hold
  (`corpus/knowledge/receipt-provenance-r85.md`, receipt provenance), its `source:` citing S600 — a
  `mined` row opened, pinned three times byte-identically and quoted this round; registry 372 → 374
  (one admit, one reject), census rc 0, append-only. Evidence above.
- **quality: improved** — the weaker criterion 172 is superseded by QUALITY 173 (stale tally and
  moved pointer, measured `pass=11` vs `pass=15` and the relocation at `:296-300` → `selfcheck()`
  at `:174`), and QUALITY 176 re-pins the moved tally at the landing round (17 arms); three
  counters carry 18/18/20 detector arms and behavioural kill sets measured from committed bytes;
  the standing battery is unchanged and the sweeps are green. No admitted entry was found false or
  left stale.
- **discernment: improved** — the round mines its own `number-drift` + `reference-drift` mistake
  into the lesson and a superseding QUALITY row; this outside spot-check agrees with **both** gate
  decisions (admit S600, reject S601) and both quotes re-opened verbatim; four attack seats
  (two reviewers, critic, mutation-tester) report verdicts and the mutation probe names the surviving
  unarmed clauses for round 86.

## Routed defects the lane must fix next round

1. **`LOG.md:5310` carries a literal placeholder.** The Round-85 wave paragraph ends "Dead seats /
   stand-ins: `<fill>`." — an unfilled template slot in an append-only log. The facts are in the
   report's *Round shape and hygiene*; `LOG.md` is append-only, so append a correction entry naming
   the superseded text (never rewrite line 5310).
2. **Contradictory entering-control receipt.** `.ufo/waves/round-85/evidence/controls-r85-entering.txt`
   (added at `25a74d4c`, referenced by nothing) prints `rc=0` for the C1-unmet and C2-unmet outputs
   whose identical stdout `evidence/controls-r85.txt` records with `rc=1`. One of the two is wrong
   as evidence; delete the superseded file or replace it with a corrected receipt and name the
   supersession in the round record.
3. **Contract has no `A4` block.** The C3 entering-control correction landed at `91f657f6` and is
   cited as "A4" by the report, SCORECARD, knowledge entry and README row, but
   `grep -n A4 .ufo/waves/round-85/contract.md` at the tip returns nothing and §Amendments jumps
   A3 → A5. Add the A4 block (or an A5 errata sentence naming the missing anchor) so the
   freeze-then-amend trail is self-contained.
4. **Report overstates amendment disclosure.** The report says the "five amendments, each disclosed
   in the contract and the round lesson"; `grep -n 'A1\|A2\|A3\|A4\|A5\|amendment'
   corpus/lessons/round-85.md` finds no amendment disclosure, and A4 is absent from the contract.
   Append an erratum naming the sentence (reports are filed records).
5. **Prompt attribution (D84-1 recurrence).** `.ufo/prompts/mori-round-85.md` was committed by
   `mori-shokunin <mori@shokunin.local>` (`f9a8a8d2`); committing generated prompts is
   integrator-owned (PROTOCOL §Invariants). Recorded, never re-attributed; history is not rewritten.

Observations, not defects: `w1/Mo85R02C2` is a dead seat (empty output) disclosed in the report and
its attack is covered by three other seats; `Mo85E01C1Arms`' stand-in and duplicate-arm collision
are disclosed with the restore and independent re-verification; ignored `__pycache__` bytecode
remains under `.ufo/waves/round-85/` on disk but is untracked and absent from the pushed tree; the
three scratch fixture commit ids are non-resolving by design and carry committed rebuild recipes.

**SHONEN note for the operator:** the four boxes look checkable by a named non-author on the
evidence cited (SKILL.md:1371 + QUALITY 173-176 + knowledge entry; LOG Round 85; the three
selftest commands; the PROVINCE note and the connector's sibling scan). Promotion remains
operator-owned; this reviewer wrote no `[x]`.
