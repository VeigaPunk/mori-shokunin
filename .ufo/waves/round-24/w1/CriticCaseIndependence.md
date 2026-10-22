# MoriR24.CriticCaseIndependence — C2 case independence versus freeze order

Seat: critic, read-only, leaf. Written 2026-10-22T08:19Z. Lane tip when read: `f7eb430`
(contract amendment A1), after `4059ffb` and `06d4f4d`. Installs: none (git 2.56.0 and
Python 3.14.8 were already present). Every git write ran only in my own sandbox,
`/fast/scratch/hyaku/mori-r24-a2/critic-case-independence/` (fixture script `run.sh`,
fixture repos `fx/`, patched copy `fo-patched.py`; a temporary lane clone used for the
selftest was deleted).

## Verdict in one paragraph

Committed bytes can show one thing: within the lane's history, the commit that adds
`tools/fixtures/mori-pressure/cases.json` is a strict ancestor of every commit that touches
`tools/mori-pressure.py`, and the cases bytes never change after that. They cannot show what
any author read or when. `tools/mori-freeze-order.py` checks only the first half of that
statement, and only if the L1 picks a sound register and lands the work as a straight line.
I found two ways it grades `pre-build` (exit 0) when the cases were not landed before the
tool, plus one false source claim about how it handles merges. The contract sentence "written
by a seat that does not see the implementation" (`contract.md:81`) claims something
universal about reading, and no byte check can prove it. Below I give a register and an
invocation, with preflight checks, that close the fixable holes. The remaining holes are
listed as things the evidence cannot show.

## Counterexamples (all exercised; reproduce with `bash run.sh` in my sandbox)

The `run.sh` fixtures follow the round-24 shape: the base holds only the contract, the
register is a `mori-freeze-register-v1` row with `declared: pre-build`, and the lane
script is used unmodified (`sha256 ec1be305d9fbf81d…`).

| Scenario | freeze-order result | Correct? |
|---|---|---|
| S1 straight line: cases + register commit, then tool commit | exit 0, `pre-build` | yes |
| S2 cases and tool in one commit | exit 1, `co-evolved`, `co_committed` true | yes (positive control) |
| S3 cases edited after the tool commit | exit 1, `co-evolved` | yes (positive control) |
| **S4b** base set to the commit that added both files, register committed alone, then a tool fix | **exit 0, `pre-build`**, `co_committed` false | **no**: cases and tool were co-committed |
| **S5a** tool seat's report (carrying tool code) committed together with the cases; `impl` lists only the tool | **exit 0, `pre-build`** | **no**: tool-derived bytes landed with the cases |
| S5b same history, `impl` also lists `.ufo/waves/round-24/w1/BuildPressureTool.md` | exit 1, `co-evolved`, `co_committed` true | yes |
| **S6** tool first committed as `tools/pressure_draft.py`, cases next, then renamed to `tools/mori-pressure.py` | **exit 0, `pre-build`** | **no**: implementation preceded cases under another path |
| S7 tool on a side branch from base (the sandbox shape: `r24-wt-pressure` on `29c1bf45`), cases on main, `merge --no-ff` | exit 1, `co-evolved`, `co_committed` true, for both early and late tool dates | right answer, wrong reason (see the next section) |

**S4b, base vacuity.** freeze-order never checks that the implementation paths are absent at
`base` (`tools/mori-freeze-order.py:296-306`: it checks only that the frozen paths are present
at the tip). Round 23 already set this requirement: "strict ancestor, production
absent/unchanged at seal" (`corpus/lessons/round-23.md:25`). The tool does not enforce it.

**S5a and S6, path-list blindness.** The verdict sees only the paths named in the register
(`tools/mori-freeze-order.py:280-294`). Implementation bytes under any other path never
count: a seat report that quotes the code or pastes live tool output, a draft filename, or a
rename. The knowledge entry says renames are seen as a delete plus an add
(`corpus/knowledge/freeze-order-r18.md:37`). That makes the draft path invisible unless it
is listed in `impl`.

## Freeze-order defect found along the way (calibration; route, do not fix in C2)

`tools/mori-freeze-order.py:95-99` says "-m plus --first-parent makes a merge's change set its
first-parent diff". On git 2.56.0 that is false. For the S7 merge commit:

```
diff-tree -m                         -> tools/mori-pressure.py, …/c2-freeze-register.json, tools/fixtures/mori-pressure/cases.json
diff-tree -m --first-parent          -> same three paths (diff against both parents)
diff-tree --diff-merges=first-parent -> tools/mori-pressure.py only
```

`man git-diff-tree` documents `-m` as "shows differences to that commit from all of its
parents" and does not document `--first-parent` at all. In `git-rev-list` that option is a
walk option ("When finding commits to include…"). The same false statement appears in
`corpus/knowledge/freeze-order-r18.md:36-38` ("merges are judged against their first
parent") and in the scope of SOURCES row S058.

The impact is currently conservative. The diff against all parents only adds hits, so every
`--no-ff` merge grades `co-evolved`. But it hides a second gap. With a patched copy that uses
`--diff-merges=first-parent`, S7 grades **exit 0 `pre-build`** (both dates), even though
`git merge-base --is-ancestor <cases> <tool>` fails: the tool commit does not descend from
the cases commit. The rev-list `--topo-order` index (`tools/mori-freeze-order.py:105-110`)
is a position in a list, not ancestry. Both the original and the patched copy pass
`SELFTEST freeze-order PASS 12/12` in a lane clone, so selftest arm 10
(`tools/mori-freeze-order.py:640-655`) does not discriminate. Smallest correction for a
later calibration round: use `--diff-merges=first-parent`, require the last frozen commit to
be an ancestor of the first implementation commit, require the implementation paths to be
absent at base, and add selftest arms for S4b and S7. For round 24, avoid the whole question
by landing a straight line.

## What committed bytes can show (if the L1 follows the recommendation)

1. Neither path exists at the base `29c1bf45dde6af48fc9a07aef447bd7d7f822cc5` (checked:
   `cat-file -e` fails for both at `29c1bf45` and at `06d4f4d`).
2. Exactly one commit A between base and tip touches `cases.json`. A is a strict ancestor of
   the first commit F that touches `tools/mori-pressure.py`, and the range contains no merges.
3. The register itself, committed in A and listed as frozen, is never edited after F. That
   catches a later narrowing of the `impl` list.
4. The lane's `cases.json` blob equals the cases seat's committed blob in
   `/fast/scratch/hyaku/mori-r24-a2/wt-cases`, and the SHA-256 written in
   `FreezePressureCases.md`. That shows the L1 did not change the cases between the seat and
   the lane.
5. The cases seat's commit tree lacks `tools/mori-pressure.py`, and the tool seat's commit
   tree lacks `cases.json`. That shows only what was in each seat's own tree.

## What committed bytes cannot show (state these as limits, never as passed)

- **What the cases seat read.** Its guard covers file names only: "do not open any file named
  mori-pressure.py anywhere" (wave1-spec item FreezePressureCases). It does not forbid any of
  these: `git -C …/wt-pressure show <rev>:tools/mori-pressure.py` (no file of that name is
  opened); the tool seat's report `.ufo/waves/round-24/w1/BuildPressureTool.md`, which the
  tool seat is told to fill with pasted live and interval outputs, that is, the real output
  shape; the tool seat's private cases under `…/build-pressure-private/`; peer messages; and
  `history://` transcripts. [INFERENCE: transcript access as described in the session's
  coordination notes; I did not read any transcript.]
- **A private dry run before landing.** If the L1 or the cases seat ran a sandbox build
  against the cases and then changed them, the landed order is still `pre-build`. Point 4
  above covers changes the L1 makes after the seat commits, not changes the seat makes before
  it commits. Round 23 recorded this limit: "timestamps alone do not prove private
  chronology" (`corpus/lessons/round-23.md:25`).
- **Independence of the specification.** Both seats derive from the same contract and the
  same shared-interface text. A shared misreading of the interface passes jointly. Examples:
  how `some: null` is represented for irq, `stall_ratio` rounding, the shape of a findings
  object. Separate authorship is not independent evidence of correctness (that belongs to
  CriticC2Semantics).
- **Matcher strictness.** The selftest's matcher (exact `exit`/`verdict`, subset matching of
  `some`/`full`, `findings_include` membership) lives inside the implementation file. Freezing
  the cases does not freeze how they are judged. A lax matcher produces `PASS 12/12`. C2 has
  no "Able to fail" clause, while C1 has one (`contract.md:46`; the C2 section,
  `contract.md:51-103`, has none).
- **Wall-clock order.** Committer and author dates are set by whoever writes the commit.
  freeze-order uses topology only, which is correct, so dates add nothing. After a
  cherry-pick, an author date earlier than the cases commit is expected and proves nothing
  either way.
- **That the 12 cases match the frozen topics P01–P12.** freeze-order is not a content check.

## Recommendation to the L1

**Landing shape (fixable now).** Straight line, no merge commits, no fetch-and-merge of
`r24-wt-pressure`. Copy the bytes or cherry-pick onto the cases commit.

- Commit A contains only the cases-seat outputs: `tools/fixtures/mori-pressure/cases.json`,
  the register below, and optionally `FreezePressureCases.md`.
- Commit F (a descendant of A) and later commits contain `tools/mori-pressure.py`,
  `BuildPressureTool.md` and every other report that quotes tool code or output.

**Register** at `.ufo/waves/round-24/frozen/c2-freeze-register.json`, committed in A:

```json
{"schema":"mori-freeze-register-v1",
 "frozen_by":"MoriR24 (L1) in the cases commit, before any tools/mori-pressure.py commit",
 "claims":[{"id":"r24-C2",
  "base":"29c1bf45dde6af48fc9a07aef447bd7d7f822cc5",
  "tip":"<landed round-24 tip>",
  "frozen":["tools/fixtures/mori-pressure/cases.json",".ufo/waves/round-24/frozen/c2-freeze-register.json"],
  "impl":["tools/mori-pressure.py",".ufo/waves/round-24/w1/BuildPressureTool.md"],
  "declared":"pre-build","outside_ruling":null,"ruling_at":null}]}
```

Listing the register itself as frozen was exercised in S1 (still `pre-build`). Do **not**
pass `--corrections corpus/evidence/freeze-register.json`: its only row has id `r17-C3`,
which is not in this register, so `_load_corrections` raises `invalid-corrections` and the
run exits 2 (`tools/mori-freeze-order.py:225-233`).

**Exact invocation** (the receipt is bound; `<LANDED_TIP>` is the full 40-hex commit, the
same value in both places, and the working-tree register must equal its blob at that commit):

```
python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-freeze-order.py check \
  --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
  --rev <LANDED_TIP> \
  --register /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-24/frozen/c2-freeze-register.json \
  --tip-for r24-C2=<LANDED_TIP>
```

Expected: exit 0, `claims[0].verdict` `pre-build`, `co_committed` false, `overclaim` false,
`provenance.status` `bound`, `totals.overclaims` 0.

**Required preflight** (read-only git; this covers S4b, S6 and S7, which freeze-order does
not check). Set `L=/home/vgpnk/Projects/shokunin/mori-shokunin`,
`B=29c1bf45dde6af48fc9a07aef447bd7d7f822cc5`, `T=<LANDED_TIP>`,
`C=tools/fixtures/mori-pressure/cases.json`, `P=tools/mori-pressure.py`:

```
git -C $L cat-file -e $B:$C            # must exit 128
git -C $L cat-file -e $B:$P            # must exit 128
git -C $L rev-list --merges $B..$T     # must print nothing
git -C $L rev-list $B..$T -- $C        # exactly one commit: A
git -C $L rev-list --reverse $B..$T -- $P   # first line: F
git -C $L merge-base --is-ancestor A F # exit 0, with A != F
git -C $L log --format=%H --name-status $B..$T | rg -n 'pressure'   # no earlier draft or rename path
git -C $L rev-parse $T:$C              # equals the seat's blob:
git -C /fast/scratch/hyaku/mori-r24-a2/wt-cases rev-parse <cases-seat commit>:$C
git -C $L show $T:$C | sha256sum       # equals the SHA-256 in FreezePressureCases.md
git -C /fast/scratch/hyaku/mori-r24-a2/wt-cases cat-file -e <cases-seat commit>:$P   # 128
git -C /fast/scratch/hyaku/mori-r24-a2/wt-pressure cat-file -e <tool-seat commit>:$C # 128
```

**Wording correction (fixable, false provenance).** Replace "written by a seat that does not
see the implementation" (`contract.md:81`), in any receipt or SCORECARD text, with what is
shown: "landed in a commit that is a strict ancestor of every tool commit, byte-equal to the
cases seat's committed blob; the cases seat was instructed not to open the tool file; reads
through reports, transcripts, git objects and private cases were not prevented or observed."
This is not a narrowing of the C2 target. The `PASS 12/12` after-value stands as declared.

**Able to fail (smallest addition, sandbox only).** Add one cases mutant (flip P06's
expected exit from 1 to 0; the selftest must print `FAIL 11/12`) and one matcher mutant (drop
the `findings_include` check; P06 or P07 must still fail once the expected findings are
wrong). This shows the matcher can reject.

## Impacted axes

- **Coverage (C2):** what `PASS 12/12` means depends on matcher strictness and on the
  disclosed limits on what the seats read. It is not affected by the ordering verdict alone.
- **Calibration:** freeze-order's `pre-build` can be produced vacuously (S4b, S5a, S6). The
  merge comment, `freeze-order-r18.md:36-38` and the S058 scope claim first-parent merge
  diffs that git 2.56.0 does not perform, and selftest arm 10 cannot tell the difference.

## Tradeoffs the judge must reject if they are claimed

Any assertion that the seat "did not see" the implementation, or that the commit order shows
when the cases were written, is a claim about reads and wall-clock time. Committed bytes
cannot support it. The fixable parts are the register, the straight-line landing, the
preflight, the blob binding, the wording, and the mutants.

## Not run

I did not run freeze-order on the lane at a round-24 tip, because no cases, tool or register
are committed yet (`cat-file -e` fails for both paths at `06d4f4d`; `wt-cases` had no
`tools/fixtures` at 05:17 local time). I did not read either seat's report or transcript,
and did not open any `mori-pressure.py`. I did not message any peer.
