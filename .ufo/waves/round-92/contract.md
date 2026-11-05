# mori round 92 — frozen contract (attempt 1)

Lane: mori. Round: 92. L1: MoriR92 (planner and integration owner; no seat writes the lane tree).
Entering revision: `f63d1ab030d4179576e494342f48ef8718e497a5` (lane `master`, clean, remote-equal;
`jj-lane.sh state` ahead=0 behind=0 tracked=0 untracked=0). Written and committed before any
wave output exists; the counters `count-c1.py`, `count-c2.py` and the do-nothing control receipt
`evidence/controls-r92.txt` are committed in the same commit as this file.

## Axes and scores (SCORECARD.md `## Axes`)

coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6. Retired:
drift-pin-r10. The lowest non-retired scores are depth, freshness and calibration (5, tied).

## Claims (two; each on a distinct tied-lowest axis; causally separable)

Round-91 planned re-declarations (C1 gate-clause arming with P1/P2 populations; C2 dated
value-channel snapshot) are NOT re-declared this round. Reason, recorded before data: the
Mo91R01Atk attack found the round-91 family labels do not match any label the subject emits, and
the Mo91R01Atk/Mo91R02Atk rewrites require a counter-synthesized guard (QUALITY 191, a carried
operability item) that cannot land in one round honestly. They stay carried as Planned (round
92) items with their attack records; no verdict on them is claimed here.

### C1 — depth: every `corpus/knowledge/` entry carries the provenance trio

Subject: the 98 files `corpus/knowledge/*.md` at the entering revision.
Counter: `python3 -I .ufo/waves/round-92/count-c1.py <rev> --repo <clone>`.
Predicate (this sentence is the counter's condition and the receipt label): at revision R the
command prints `C1=met knowledge=<n> missing=0 floor=98 rev=<12>` and exits 0, where each knowledge
file has a line beginning `source:`, `verified-at:` and `recheck:` (each key at least once) within
its first 12 lines, and `n >= 98`.
Entering control (committed): `C1=unmet knowledge=98 missing=19 floor=98 rev=f63d1ab030d4`, exit 1.
The 19 files: `evidence/c1-missing-entering.txt` (one `MISSING <path> keys=…` line each).
Kill rule: met iff `missing == 0` and `knowledge >= 98`; any absent key in any file is a miss.
Landing constraint: the landing adds or edits only the provenance lines of the 19 listed files;
no body text, no claim, no admitted conclusion is changed. Each added line must be true at its
commit: `verified-at` names the admission commit of the file (`git log --diff-filter=A`), and
`recheck` names the command or citation the file's own body already gives, or
`manual — <path:line>` when the body gives none. Presence is what the counter measures; truth of
each trio line is spot-checked by the non-author closure (discernment), not by this counter.
Known limit (named, not waived): the counter checks presence, not provenance quality.

### C2 — freshness: the registry digest gate reports zero unresolved mismatches

Subject: the landed digest tool `tools/mori-source-digest.py` (round 91) and the two corrections of
record in `corpus/lessons/round-91.md` (C-1: S615; C-2: S235).
Counter: `python3 -I .ufo/waves/round-92/count-c2.py <rev> --repo <clone>` (black-box over the
tool extracted from R, full tree, `git archive`; no judgement of digests by the counter itself).
Predicate (this sentence is the counter's condition and the receipt label): at revision R the
command prints `C2=met mismatch=0 superseded=2 superseded_ids=S235,S615 prefix_only=31 unpinned=1
negatives=2 selftest=pass rev=<12>` and exits 0, where the tool run as the round-91 receipt ran it
(`python3 -I tools/mori-source-digest.py corpus/SOURCES.md .ufo/waves/round-90/w1/Mo90S01Sources/sources`)
exits 0 with a summary `DIGEST_CHECK ... mismatch=0 superseded=2 ... prefix_only=31 unpinned=1`;
the per-row lines `DIGEST S235 superseded-by S620` and `DIGEST S615 superseded-by S619` are the
only superseded rows; negative fixture A (S619's recorded digest with one hex character flipped)
makes the tool exit 1 and print `DIGEST S615 mismatch`; negative fixture B (S620 row deleted)
makes it exit 1 and print `DIGEST S235 mismatch`; and the tool's `--selftest` exits 0 with
`DIGEST_SELFTEST pass=<n> fail=0`, n >= 8.
Entering control (committed): `C2=unmet mismatch=2 superseded=None superseded_ids=- prefix_only=31
unpinned=1 negatives=0 selftest=absent`, exit 1. The entering tool run reproduces the round-91
receipt exactly: `DIGEST_CHECK rows=121 ok=87 mismatch=2 prefix_only=31 unpinned=1`.
Kill rule: met iff every clause above holds; any clause failing is `checks_failed=`; a change to
`prefix_only` or `unpinned` is a no-harm regression and keeps the claim unmet.
Supersession rule (CORPUS.md rule 2): the corrections are NEW rows S619 (`supersedes S615 —`) and
S620 (`supersedes S235 —`). No existing row's digest is edited. A successor counts only if the tool
classifies the successor itself `ok` against its named pinned copy. Status, recheck and used-by of
old rows stay unchanged.
Landing constraint: the tool gains a `--selftest` mode and supersession logic; its existing
classification of `mismatch`, `prefix-only` and `unpinned` rows is unchanged for every row other
than S615 and S235.

## Frontier step (protocol §2b, round 92)

- Census before: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` →
  exit 0, `391` rows (wave `census-before.txt`, recorded at round start in the report).
- Mined mistake: round-91 `recorded-digest-unverified` (`corpus/lessons/round-91.md`
  `## Mistakes`, captured-by `none`). Fix: C2's black-box gate run with its own selftest; shown
  able to fail by negative fixtures A and B (both must exit 1 before the claim counts) and by the
  mutation-tester's mutants of the supersession logic (wave item `Mo92M01Mut`).
- Sourced claim: C2 rests on `S619` and `S620`, rows written this round after re-hashing each
  pinned copy at R and locating a ≤25-word quote from it (wave item `Mo92Sc01Src`).
  The scout also opens one new spec-tier source for the digest semantics (candidate `S621`).

## Ordering (binding)

1. This contract, `count-c1.py`, `count-c2.py`, `evidence/controls-r92.txt` committed through
   `jj-lane.sh` before the wave is dispatched.
2. Wave `w1` builds only in scratch clones, writes only patches, row drafts and reports under
   `.ufo/waves/round-92/w1/` (absolute paths under the lane). No seat commits.
3. The L1 applies the patches to the lane tree, lands via `jj-lane.sh`, then records the
   after-receipts `evidence/after-r92.txt` at the landing revision.
4. Any change to a frozen predicate, population, kill rule, floor or landing constraint after step
   1 voids the claim; nothing is rewritten. A do-nothing control that meets a target voids the
   target (none did).

## Out of scope (declared before data)

No change to the fleet root, sibling lanes, MANIFEST.json, `.ufo/state/`, the watchdog log, host
configuration, routing, pacman, or domain trees; no pushes outside the mori lane remote and the
fleet repo. `scripts/sources-census.sh` is not modified (it does not read digests; wiring the
digest gate into it is deferred and recorded as a decision: reader gate only). No re-scoring of
existing knowledge bodies; no change to prefix-only rows (append-only rule).

## Carried, not claimed (named)

Operability: nonce guard for the round-90 gate (QUALITY 191). Depth: supersession record for the
round-87 arm pins (`w1/candidates/pins.txt`, round 91). Calibration: the round-91 gate-clause
families (`c2-replay-compare-off`, `c2-supersede`, `c2-absent`, `c2-defeated-accounting`) remain
unarmed; the family-to-label map must be frozen from the subject's real labels before any
re-declaration. The 31 prefix-only rows and the 1 unpinned row (S125) stay as reported debt.
