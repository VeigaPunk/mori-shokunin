source: S056 (Nosek et al. 2018, "The preregistration revolution"), S058 (git-rev-list(1), git-diff-tree(1)); lane register `.ufo/waves/round-18/frozen/c2-register.json`
verified-at: 2026-10-21, sources opened by `.ufo/waves/round-18/build/Src{NosekPrereg,GitRevList}.md`; r17 verdicts independently re-derived by `build/RevFreezeR17C{1,2,3}.md`
recheck: `python3 tools/mori-freeze-order.py check --repo . --register .ufo/waves/round-18/frozen/c2-register.json --corrections corpus/evidence/freeze-register.json --tip-for r18-C1=<tip> --tip-for r18-C2=<tip> --tip-for r18-C3=<tip>`; `mkdir -p .scratch && TMPDIR=$PWD/.scratch python3 tools/mori-freeze-order.py --selftest` (TMPDIR must not be under /tmp; remove `.scratch` afterwards)

# Freeze-order: a "pre-build" label is a commit-order verdict

Preregistration separates prediction from postdiction only when the plan is fixed before
outcomes are seen (S056). In a lane repository the observable equivalent is commit order:
a claim's requirement inputs (expected tables, oracles, populations) must be committed in a
commit that strictly precedes the first commit touching its implementation, and must not
change afterwards.

## Verdict rule (frozen in `c2-register.json`)

| Observation over `git rev-list --reverse --topo-order base..tip` (S058) | Verdict |
|---|---|
| any frozen path missing at tip | `absent` |
| no commit touches an implementation path | `no-implementation` |
| last frozen-touching commit strictly precedes the first impl-touching commit, or frozen inputs predate base | `pre-build` |
| frozen inputs co-committed with, or edited after, the first impl commit | `co-evolved` |

A `pre-build` label with any other verdict is an **overclaim**, including
`no-implementation` (nothing has yet been ordered against it). Corrections are appended
rows (`corpus/evidence/freeze-register.json`), never rewrites of the filed label.

## What round 18 measured

- r17-C1, r17-C2, r17-C3 all grade `co-evolved` with `co_committed` true, matching the
  non-author closure 3/3. Only r17-C3 had been labelled "precommitted"; that one overclaim
  is corrected by an appended row. The closure's ruling on C3 is partial (witness and
  miss/hit oracle precede the final tool change), so the correction keeps the calibration
  repair and withdraws only the pre-build label.
- Agreement with an oracle the register author had already read is not independent
  evidence of discernment (round-18 CriticC2Calibration); the failure-capable evidence is
  the selftest's co-commit arm and the r18 self-application at the measured tip.
- The selftest (12 arms) does not yet distinguish `--topo-order` from `--date-order` on a dated divergent DAG (round-18 MutFreezeOrder M04 survived); history with merges is judged by first-parent diffs only.
- Path renames are seen as delete + add (`diff-tree` without `-M`), and merges are judged
  against their first parent; both are declared limits, not proofs of freeze.

## Round19 operational correction — intrinsic input binding

The original `recheck:` command above is a historical unbound invocation.
For committed-input evidence now add `--rev <INPUT_REV>` explicitly. The
register and supplied corrections must reside beneath `--repo` and their
loaded bytes must exactly match blobs at that revision; dirty, missing,
uncommitted or external input is could-not-evaluate. Claim tip overrides
still name the chronology endpoints and may differ from INPUT_REV. The
executing-script SHA is a separate identity, not a claim that this newer
checker exists at the historical input revision.

This operational correction is sourced to S064 (`git-rev-parse(1)`,
`--verify`/commit peeling), `corpus/lessons/round-19.md` and its independent
frozen assertions. It is not a new covered-ground knowledge entry or a
retroactive claim that the old C2 JSON already carried these fields.
The r18 before count remains one historical overclaim plus three
prospective labels; their input-revision replays are recorded in round19
evidence without changing the six original verdicts.
