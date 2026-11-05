# mori round 97 — frozen claim contract (L1 MoriR97, attempt 1)

Entering revision: `973b2af11f41bd362163d7e29ac08286832f546b` (master = origin/master, clean).
Fresh start (amendment 35, `blocked/.mori.fresh-20261105`): the last three closures r94, r95, r96 were
rejected-honest-stop. Read before declaring: `corpus/lessons/round-94-verifier-spotcheck.md`,
`round-95-verifier-spotcheck.md`, `round-96-verifier-spotcheck.md`. Root causes carried into this contract:
r94 C2 and r95 C2 — successor artifacts / predicates a do-nothing control already met (the entering state
passed); r96 C2 — a freshness predicate (`live == recorded`) the vendor's per-build page stamp can never
meet, frozen while the lane already held the stamp grammar (`tools/mori-drift-recheck.py`, r66).
This contract therefore binds (1) do-nothing controls that FAIL at entering, (2) forgery controls that
make each instrument's own green insufficient, (3) positive controls so blanket refusal is not a gain —
all executed and committed before this freeze: `evidence/controls-r97.txt` (`CONTROLS_DONE unexpected=0`).

Measurement method (both claims): materialize the measured revision `R` with
`git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive R | tar -x -C DIR` (DIR under
`$HYAKU_SCRATCH/mori-r97/`), then run the frozen counter with `--root DIR`. Frozen instrument bytes:
`count-c1.py` sha256 `78a09016fa8151b72049400600b6b154437c919df6fccb55b8bfa6253b4d2a95`,
`count-c2.py` sha256 `957a7be605ba920734a218388b7ebb50f4f829979931c6e4193caee2149a1e91`
(recorded on the first line of `evidence/controls-r97.txt`). Never edited after this freeze; a defect
found later is reported, not patched into the claim.

## C1 — operability (score 7): the lane's gate registry runs and states the outcome for four unregistered gates

Surface moved: the existing gate registry at `SKILL.md` (registry home), audited by the existing
auditor `tools/mori-gate-registry.py` (r44/r45). Entering state: `unregistered=4`
(`tools/mori-cgroup-pressure.py`, `tools/mori-drift-recheck.py`, `tools/mori-scorecard-calibration.py`,
`tools/mori-source-digest.py`) — r96 routed defect 1. AXES.md operability: "A checklist item can be run
and produces the stated outcome".

Predicate P1 (same sentence as `count-c1.py` docstring): on the tree of R, (a) the auditor `--rev WORK
--audit-all` prints `REGISTRY=met`; (b) for each of the four tools the row the auditor attributes to it
has a `self-test` cell containing, verbatim, the final line the tool's own `--selftest` prints when run
now, and that selftest exits 0; (c) that row's `verdict map` cell contains the tool's frozen verdict token
(`MORI_CGROUP_PRESSURE`, `MORI_DRIFT_RECHECK`, `C1=met`, `DIGEST_CHECK`).

Counter: `python3 .ufo/waves/round-97/count-c1.py --root DIR`. Label: `C1=met` / `C1=unmet`.
Before (do-nothing, entering): `C1=unmet unregistered=4 registry=unmet targets_ok=0/4`.
Target (after, landing): `C1=met unregistered=0 registry=met targets_ok=4/4`.
Kill rule: any other output at the landing revision is unmet; no re-declaration.
Controls (committed, pre-freeze): junk eight-cell rows make the auditor alone go green but score
`targets_ok=0/4`; rows stating a wrong selftest outcome score `0/4`; a verdict map without the token
scores `3/4`; candidate rows score `met`.

## C2 — freshness (score 5, lowest non-retired tier): three stale-flagged registry rows re-verified against the live surface

Surface moved: `corpus/SOURCES.md` rows S615, S616, S623 (flagged stale by r96, `unpinned` in the
existing digest gate `tools/mori-source-digest.py`, no copy for the existing live re-check
`tools/mori-drift-recheck.py`). Work: pin, under `corpus/evidence/sources-r97/<id>.html`, the exact bytes
each row's recorded digest names (S616: the r90 copy; S623: today's live page with the build stamp line
restored, sha256 equal to the recorded digest; S615: the r90 ast copy that S619 already records as the
correction of S615's mis-recorded digest), then re-verify each against a fresh live fetch with the r66
stamp grammar (grounded by S577 and the new row opened this round on the docs.python.org build).
AXES.md freshness: "skill claims re-verified against live surfaces; stale items flagged or fixed".

Predicate P2 (same sentence as `count-c2.py` docstring): on the tree of R, (a) the digest tool prints
`DIGEST_CHECK` with `mismatch=0` and `unpinned=0`; (b) each of S615, S616, S623 prints `ok`, or
`superseded-by S<n>` where the newest `sources-r<N>/<id>.*` copy hashes exactly to the successor's own
`ok` digest (the r96 supersession-hole guard); (c) each `ok` target's newest copy hashes to the tool's
`actual=`; (d) a live `tools/mori-drift-recheck.py --only S615,S616,S623` run exits 0 and classifies each
row `fresh` or `time-churn`.

Counter: `python3 .ufo/waves/round-97/count-c2.py --root DIR`. Label: `C2=met` / `C2=unmet`.
Before (do-nothing, entering): `C2=unmet mismatch=0 unpinned=3 targets_ok=0/3 hole_guard=n/a
live=S615:no-copy,S616:no-copy,S623:no-copy`.
Target (after, landing): `C2=met mismatch=0 unpinned=0 targets_ok=3/3 hole_guard=pass` with every live
class in {fresh, time-churn}.
Kill rule: any other output at the landing revision is unmet (including a live `content-drift` or
`unavailable` at measurement time); no re-declaration.
Controls (committed, pre-freeze): a random 362,493-byte S615 copy is superseded by the digest tool (the
r96 hole) but scores `hole_guard=fail`; today's live S616 bytes pinned score `mismatch=1`; correct pins
with S623 pointed at another live page fail on the live leg alone (`content-drift`); candidate pins score
`met`.

Sourced: C2 rests on a SOURCES row opened this round (the docsbuild-scripts README, S628) — the lesson
`## Gate` carries URL, access date and the located quote.

## Not claimed (honest scope)

- No score move is claimed on either axis; scores stay until a closure states one.
- The 31 `prefix_only` rows of the digest gate are not touched (gate exit stays 1).
- The operator L0 on stale digests (`.ufo/l0-questions.md`, mori | round-96) is not treated as answered:
  this round uses option (a)'s mechanism already in CORPUS rule 2 only through the pre-existing S619
  correction row, appends no supersession row for S616/S623, and edits no recorded digest.
