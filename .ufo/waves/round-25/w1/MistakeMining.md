# MistakeMining — one mined mistake for round-25.md `## Mistakes`

Seat: `MoriR25.MistakeMining` (scout, leaf; no subagents dispatched). Read-only on the lane except this
file. Measured at lane tip `7bb0fe61766fa011db03c529c693469c7a5a3e2b` (the tip moved during this seat:
`042d75b` contract amendment A3 → `ec840f9` supplementary S08–S16 + D3 correction + QUALITY 76–77 →
`7bb0fe6` the D1 evidence file). All git use was object reads (`cat-file`, `show`, `rev-parse`, `ls-tree`,
`log`, `diff --stat`); no jj, no lane git write, no `omp` run, no settings touched, no tool installed.
Toolchain as found: Python 3.14.8, git 2.56.0. Scratch (throwaway, outside the lane, outside the fleet
root): `/fast/scratch/hyaku/mori-r25-mistake/` — probe scripts `d1probe.py`, `d1probe_a1.py`,
`d1probe_a3.py` (sha256 `2d4cf84e0ff364f1253b03a859d1e0b323817b517c5b0dea0f3fedb8fc60f45a`,
`8da25f156df9782fefa81b7ff30e7493ebef9444b3f0ada2afa1c528e61004f8`) and temporary `git show` extracts of
`tools/mori-pressure.py` at `6ee6248`, `89849a7`, `6a344d2`, `c484f6d`, `4f05dd5`.

## The mined mistake (paste-ready for `corpus/lessons/round-25.md` `## Mistakes`)

Table form, matching the round-24 column set (`corpus/lessons/round-24.md:56-68`):

| ID | Class | Evidence pointer | Captured-by | Fix / able to fail |
|---|---|---|---|---|
| M1 | gate evidence written before the final tool: a committed selftest-output file that names no revision and is the stdout of an **earlier** tool revision, shipped in the same commit that changed the tool | `.ufo/waves/round-24/evidence/c2-selftest-after.txt` — blob `4618daf95d9a612f8f18a04e29520cb599e92862`, 35 bytes, one line `MORI_PRESSURE_SELFTEST: PASS 12/12`; landed at `89849a7` (empty-message twin `d637dbd`, identical tree `a408b474`). sha256 of the file = `31c510bf3a5e28d8a415666d9d646b3dc35bf8855110b5a5d0ab60d8b0925541` = sha256 of `python3 -I -B tools/mori-pressure.py --selftest` stdout at `6ee6248` (tool blob `4e08739a…`), while the tree's own tool at that same commit is blob `6927dc19…`, whose stdout is 82 bytes, sha256 `d767d1b6fd53e45caae8ca430f54f91badc08f89676a4d606bd1e2ac0be16f`, two lines (`MORI_PRESSURE_SELFTEST: PASS 12/12` + `MATCHER: rejected 48/48 corrupted expectations`). The file's blob is byte-identical at `89849a7`, `4f05dd5`, `28b79d3d` and `7bb0fe6` — it was never repaired in round 24. The lane's own self-assessment contradicts it: `SCORECARD.md:1514` states the two-line stdout | PROTOCOL §Gate standard "Two evidences", `PROTOCOL.md:390-393` ("A verdict names the revision it was measured against"), and lane QUALITY criterion 31, `corpus/QUALITY.md:73` ("any self-test tally names the revision and is measured on the bytes of the actually delivered gate; an earlier revision's tally … is not a self-test of the delivered gate" ← `corpus/lessons/round-14.md:17` M4 — the same class, already captured in round 14). Round 24's own lesson cites QUALITY 19 and 70 only (`corpus/lessons/round-24.md:60,64`), so the criterion was in the corpus and never invoked; no lane tool reads the evidence file (`grep -rn "c2-selftest-after" tools/` → no hit), so nothing in the lane's gate set could turn red on it | Fix landed in round 25 at `7bb0fe6`: `.ufo/waves/round-25/evidence/pressure-selftest.txt` — five header lines `revision: ec840f9df9999bb6f5796c07128db0fec26e7c7e` (a commit that is an ancestor of the tip, `git merge-base --is-ancestor ec840f9d 7bb0fe6` → exit 0), `command: python3 -I -B tools/mori-pressure.py --selftest`, `tool_blob: 5785c5b23233a5ed1d2116ab610f9aa0cf3b12ec` (equal at `ec840f9d` and at `7bb0fe6`), `fixtures_tree: c28ccfdf6233ecc04c5b7f827cc3c66c3d8da9c8` (equal at both), `exit: 0`, then the exact two-line stdout. Able to fail: `python3 -I -B tools/mori-routed-r24.py --repo <lane> --rev <landed tip>`, D1 row (`contract.md:19`, restated `contract.md:107`, body tightened to byte-equality by `contract.md:165-167`) — red on the old bytes, green on the fixed bytes; see "Red/green" below for what was actually observed vs. what is pending the tool's landing |

Prose form, in the requested shape:

- **class** — gate evidence written before the final tool (a committed selftest-output file that names no
  revision and carries an earlier tool revision's stdout);
- **evidence pointer** — `.ufo/waves/round-24/evidence/c2-selftest-after.txt`, blob `4618daf9…`, 35 bytes,
  landed at `89849a7`; file sha256 `31c510bf…` = stdout of `tools/mori-pressure.py --selftest` at
  `6ee6248`, while the tree at that same commit already ships tool blob `6927dc19…` whose stdout is
  `d767d1b6…` (two lines). Routed as D1 at `corpus/lessons/round-24-verifier-spotcheck.md:137` and first
  noticed there at `:80`; the lane's own `SCORECARD.md:1514` states the two-line stdout the file lacks;
- **captured-by** — PROTOCOL §Gate standard "Two evidences" (`PROTOCOL.md:390-393`) **and** lane QUALITY
  criterion 31 (`corpus/QUALITY.md:73`, from `corpus/lessons/round-14.md:17` M4). Both pre-date round 24.
  Round 24 cited QUALITY 19 and 70 only, so neither fired; and no lane tool reads that file, so the class
  was not reachable by any check;
- **fix** — round-25 evidence carries the revision, the tool blob, the fixtures tree, the exit code and the
  full stdout (`7bb0fe6`), and the new C1 gate's D1 row makes that shape a red condition for every future
  round; the red/green command is `python3 -I -B tools/mori-routed-r24.py --repo <lane> --rev <landed tip>`.

## Why round 24's own process let it through

Four measured facts, each with the command that shows it.

1. **The inconsistency was created and committed in one commit, so no diff exposed it.** The commit that
   added the MATCHER line to the tool is the commit that added the evidence file:
   `git log -S 'MATCHER: rejected' -- tools/mori-pressure.py` → `89849a7`;
   `git log --diff-filter=A -- .ufo/waves/round-24/evidence/c2-selftest-after.txt` → `89849a7`.
   In that tree the file (35 bytes, one line) and the tool (blob `6927dc19…`, two lines of stdout) already
   disagree; the file is byte-identical to the **pre-change** tool's stdout at `6ee6248`
   (`31c510bf…` on both sides). A reviewer reading the diff sees a *new* evidence file, not a *stale* one:
   the comparison that matters is against the new tool's stdout, and nothing in the lane asked for that
   comparison. The class is therefore "written before the final tool", not merely "not updated later" —
   the co-commit hid it from the diff that created it.

2. **The lane's own instruments could not see it.** No lane tool reads the evidence file:
   `grep -rn "c2-selftest-after" tools/` → no hit (and none reads `.ufo/waves/round-25/evidence/pressure-selftest.txt`
   either, at `7bb0fe6`). The lane's gate set at that tip was the freeze-order gate
   (`SKILL.md:179`, cases-before-tool ordering) and the routed-check gate (`SKILL.md:642`, round-23
   items) plus the census (`SKILL.md:164`) — none of them reads a selftest-output artifact or compares it
   with the tool revision at the same commit. The pressure gate's own registry row (`SKILL.md:641`) names
   the command but binds no revision.

3. **The round's own wave-2 seats measured it and it was carried as prose, not as a fix.** Two seats
   flagged it inside round 24: `LiveBracketCheck.md:327-333` (F1, Medium — "The one-line file … predates
   both later blobs … So the file is not the output of HEAD", with the action "name the blob the C2
   after-value is measured on, re-run `--selftest` on it, and retain the output with the commit hash") and
   `RerunC2Count.md:198-202` (Low-1 — the file "postdates the measurement tip it supports"). Both were
   addressed to "the integration owner". The L1's tip commit `4f05dd5` landed the measured outcome, the
   capability rows, the QUALITY 72–75 wording, the lesson corrections and the knowledge corrections, and
   left blob `4618daf9…` in place: `git rev-parse 4f05dd5:.ufo/waves/round-24/evidence/c2-selftest-after.txt`
   = `4618daf9…` = the value at `89849a7`. Consequently round 24's own Mistakes table
   (`corpus/lessons/round-24.md:56-68`, rows M1–M9) has **no row of this class**, even though two seats
   had measured it: the wave-2 finding never became a lesson row, and a lesson row is what would have
   carried the class into the next round.

4. **The rule that would have caught it already existed and was not cited.** QUALITY criterion 31
   (`corpus/QUALITY.md:73`) states exactly this bar, and cites `corpus/lessons/round-14.md:17` M4 — where
   the *same* class was already mined ("Verdict-producing r13 checker omitted its protocol registry row and
   final delivered selftest evidence … Historical 24 checks at `80bd58a` remain historical"). Round 24's
   lesson cites QUALITY 19 (`round-24.md:60`) and QUALITY 70 (`round-24.md:64`) and nothing else
   (`grep -no "QUALITY [0-9]\+" corpus/lessons/round-24.md` → `60:QUALITY 19`, `64:QUALITY 70`), and the
   round-24 spot-check note cites only QUALITY 72–75
   (`corpus/lessons/round-24-verifier-spotcheck.md:133`). The criterion was available, uncited, and
   unexercised: a defect class that has been mined once is not automatically captured the second time.

Addendum: the class is not a one-off. The sibling seat `PatternStaleEvidence`
(`.ufo/waves/round-25/w1/PatternStaleEvidence.md`, their measurement, not mine) counted 16
selftest-output files that bind to no revision and no tool hash, and 3 of 15 re-run ones are stale — every
stale one landed in a commit that also edited the named tool. That is the same co-commit mechanism as
point 1. I did not re-derive their counts.

## Red/green: what was observed, and what is still pending

The D1 fix bytes are landed; the gate that grades them is not. Both halves are stated separately.

**Observed (my own probe of the contract's D1 predicate, verbatim from `contract.md:107` + the A3
body rule at `contract.md:165-167`; git object reads only; script
`/fast/scratch/hyaku/mori-r25-mistake/d1probe_a3.py`):**

| Evidence bytes under test | Result |
|---|---|
| old round-24 capture (`4618daf9…`) at rev `7bb0fe6` | **RED** — `header line 1 must start 'revision:'` (and headers 2–5 likewise) |
| landed round-25 file `.ufo/waves/round-25/evidence/pressure-selftest.txt` at rev `7bb0fe6` | **GREEN** — `R=ec840f9d…`, `tool_blob=5785c5b2…`, `fixtures_tree=c28ccfdf…` |
| mutant: landed file with the `MATCHER: rejected 48/48 …` line removed | **RED** — `body not byte-equal to the two-line stdout (got 35 bytes, want 82)` |
| mutant: landed file with `revision:` moved to `4f05dd5a…` (fixtures tree differs there) | **RED** — `fixtures_tree header != tree of tools/fixtures/mori-pressure at R and at REV` |
| mutant: landed file with `revision:` moved to `6ee6248…` (tool blob differs there) | **RED** — `tool_blob header != blob of tools/mori-pressure.py at R and at REV` |

The predicate's inputs are the committed objects: `git rev-parse ec840f9d:tools/mori-pressure.py` and
`7bb0fe6:tools/mori-pressure.py` are both `5785c5b23233a5ed1d2116ab610f9aa0cf3b12ec`;
`ec840f9d:tools/fixtures/mori-pressure` and `7bb0fe6:tools/fixtures/mori-pressure` are both
`c28ccfdf6233ecc04c5b7f827cc3c66c3d8da9c8`; the tool's stdout at that tool blob is the two lines
`sha256 d767d1b6fd53e45c…` (82 bytes), reproduced from a `git show` extract under `python3 -I -B`.

**Pending (not observed by me):** the lane's own command
`python3 -I -B tools/mori-routed-r24.py --repo <lane> --rev <landed tip>` with its D1 row.
`git cat-file -e HEAD:tools/mori-routed-r24.py` → `fatal: path 'tools/mori-routed-r24.py' does not exist
in 'HEAD'` at `7bb0fe6`, and the file is absent from the working tree too. So the gate's own
red-on-old / green-on-new run is **[INFERENCE] until the tool lands**: my probe implements the contract
predicate, not the shipped tool, and the two may differ (the A1 row permits an optional `--rerun` whose
result is "reported, never needed for `held`"; `contract.md:107`). Two other contract-level facts that
bear on the same item and are already committed bytes: the D1 body must be byte-equal to the two lines
(`contract.md:165-167`), and the counted set is three items with D4 reported as an uncounted hygiene row
(`contract.md:121-124`).

## Scope and out-of-scope

- This seat changed no C1 target, no contract, no lesson, no criterion, no tool. It wrote this file only.
- It did not judge whether the round-25 D1 fix is *the* right fix, only that the fix's bytes satisfy the
  contract's D1 predicate as written and that the old bytes do not.
- It did not re-derive the sibling `PatternStaleEvidence` recurrence counts; it did verify that seat's
  central mechanism claim for the D1 instance itself (the co-commit: the file and the tool change landed
  together at `89849a7`).
- It did not check D2, D3 or D4 beyond confirming the round-25 D3 correction exists
  (`corpus/lessons/round-24.md:98-100`, at `7bb0fe6`) and that QUALITY 76–77 landed
  (`corpus/QUALITY.md:338-340`).
- Nothing here is an admission or a closure judgement; the non-author integrator owns that.

Report: `.ufo/waves/round-25/w1/MistakeMining.md`
