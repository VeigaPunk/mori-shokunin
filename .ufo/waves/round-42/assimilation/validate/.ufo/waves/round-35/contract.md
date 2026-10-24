# mori round 35 — frozen claim contract (L1 MoriR35, attempt 1)

Base (entering tip): `dd76eb79ef4f6d39c9c26647a56d3fb607308f8f` (round 34 closed `rejected-honest-stop`, MANIFEST
`rounds[524]`). Written and committed with `count-c1.py`, the before receipt and the census start before any seat of
this round exists. Nothing in this file, the counter or the predicate is amended after a data seat starts; a miss is
reported as an honest stop, never re-scaled. A pre-data amendment (only if the pre-freeze control wave finds a
skip-the-work control that meets P-C1) is a new file `contract-a1.md` and a new counter file; this file stays.

Anti-loop: rounds 32–34 failed on counters whose arms had one-sided bounds that skip programs met. C1 is not a re-claim
of round 34's tool. Its counter compares the lane's self-assessment against records the lane did not write (the fleet
MANIFEST closure entries, their spot-check files and the lane's own git history), and every arm has a lower and an
upper bound (below).

## C1 — calibration (5, tied lowest with depth and freshness): the SCORECARD capabilities register agrees with the closure record

**Surface changed:** `SCORECARD.md`'s capabilities register — the `capabilities` field of the AXES.md SCORECARD
contract ("name → what it can now do → evidence pointer → first-working round"; rows "enter only through a round that
demonstrates the capability running"). This is the lane's self-assessment of what it can do. Axis named by that
surface: calibration ("SHONEN.md/SCORECARD entries match observed repo state", AXES.md). The claim does not move
coverage, depth or operability: no tool, knowledge entry or gate is added.

**Observed state at base (the mismatch the claim removes).** The fleet `MANIFEST.json` at fleet commit
`37b51a243302e8009c7067431e8a47f9a722fd14` records 18 capabilities in `capabilities_added` of admitted mori closures
(rounds 12, 14, 15, 16, 18 ×3, 19, 22, 24 ×2, 25 ×2, 26, 28 ×2, 31 ×2). The lane's last `## Capabilities` section is
`## Capabilities (round 12 demonstrations)`, with five rows that bind to no closure, and the contract-field table at
`SCORECARD.md:586-592` still reads `— none yet —`. No current register names the 18.

**Claimed work.** Append one register section to `SCORECARD.md` whose rows bind each admitted capability to its closure
(MANIFEST key and round) and cite an artifact that the round landed and the closure record names. Rows from rejected
rounds and rows the closure record does not support do not enter. The register cites the AXES.md source row opened
this round (frontier step 4).

### Predicate P-C1 (frozen; the same sentence is the docstring of `count-c1.py` and the label `P-C1` it prints)

At the measured lane revision, the last level-2 section of SCORECARD.md whose heading begins "## Capabilities" holds
exactly one table row per capability that the fleet MANIFEST.json at fleet revision MANIFEST_REV records in
`capabilities_added` of an admitted mori closure, keyed `rounds[i].capabilities_added[j]`, naming that closure's round,
and citing one or two evidence paths, each of which exists at the measured revision (any cited line range inside the
file), exists at that closure's commit, changed between the previous mori closure commit and that closure's commit,
lies under tools/, corpus/knowledge/ or corpus/evidence/ or is corpus/SOURCES.md, equals a tools/ or corpus/knowledge/
path the capability string names (when it names one), and appears as a whole path in that closure's record text (its
MANIFEST verification object, its capabilities_added strings, the lane spot-check files that object names, and the
fleet report its `report` field names, all at MANIFEST_REV); and it holds no other row. C1=met iff matched == oracle
and missing == bad == extra == 0.

Row shape: `| rounds[i].capabilities_added[j] | capability | what it can now do | evidence | first-working round |`
(5 cells; the key may be in backticks; evidence paths in backticks, optional `:N` or `:N-M`).

### Counter

`python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py <lane-rev>` (read-only:
`git show`, `git diff --name-only`, `git ls-tree`; optional `--repo PATH` for a sandbox clone, `--fleet PATH`).
Prints one `row … matched|bad|extra|missing` line per row and a summary
`label=P-C1 … oracle=18 rows=R matched=M missing=X bad=Y extra=Z mismatches=N C1=met|unmet`; exit 0 met, 1 unmet,
2 error. sha256 at freeze: recorded in `evidence/c1-freeze.txt`.

Bounds, per arm:

| arm | lower bound (catches skip / do-nothing) | upper bound (catches all-rows / junk / shotgun) |
|---|---|---|
| register rows | every oracle key matched (`missing == 0`) | no row whose key is absent from the oracle, duplicated, or from a rejected round (`extra == 0`); rows == 18 |
| round cell | — (cell must equal the closure round) | a wrong round is `bad` |
| evidence cell | at least one path | at most two paths; every cited path must be strong (`weak-path`), resolve at the tip (`absent-at-rev`) and keep any line range inside the file |
| named-path capabilities | the cited path equals the tool/knowledge path the capability string names | a different path is `weak-path` |
| closure binding | the path must have changed in that closure's round and appear in that closure's record | a path the round did not land, or the closure never names, is `weak-path` |

### Before (measured, `evidence/c1-before.txt`)

`count-c1.py dd76eb79` → `register='## Capabilities (round 12 demonstrations)' oracle=18 rows=5 matched=0 missing=18
bad=0 extra=5 mismatches=23 C1=unmet`, exit 1.

### Target (declared after-value; one command over committed bytes)

`python3 .ufo/waves/round-35/count-c1.py <landed tip>` → `matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met`,
exit 0.

### Controls (pre-freeze control wave, scored under this counter before any data seat)

Skip-the-work controls — each must print `C1=unmet`; any that prints `C1=met` forces amendment A1 before data or
declares C1 exploratory:

1. do-nothing: the base revision itself (already measured: mismatches 23).
2. no-reader / delete: the `## Capabilities` sections removed, or an empty `## Capabilities` heading appended.
3. junk: 18 rows with random keys, rounds and paths.
4. label-keyed: 18 rows keyed by the correct MANIFEST keys and rounds, evidence `SCORECARD.md` / `LOG.md` /
   the closure's spot-check lesson (rows that key on labels and skip the evidence lookup).
5. all-false / wrong-round: correct keys and correct evidence, every round cell off by one.
6. shotgun: correct keys and rounds, evidence = every artifact the round changed.
7. rejected-round inclusion: the 18 correct rows plus rows for capabilities of rejected rounds (13, 17, 20, 23, 27, …).
8. stale pointers: correct keys and rounds, evidence = a tool path that exists at the tip but was not changed in that
   round (e.g. `tools/mori-census.sh` for round 19).
9. dangling: correct keys and rounds, evidence paths that do not exist at the tip (round-34 `w1/` style).
10. any further skip program a control seat designs against this counter's code.

Positive control (shows the target is reachable; not a skip): a register built from the oracle that cites, per row,
one strong artifact. It does the claimed work — binding every admitted capability to its closure and to an artifact
the closure names — so its `C1=met` is expected and is not a counter defect. The counter does not judge which of
several strong artifacts is the best pointer, nor the prose of the "what it can now do" cell; the non-author reviewers
read those (residual, stated here before data).

### Kill rule

C1 verifies only if the counter, byte-identical to the frozen file, prints `C1=met` exit 0 at the landed tip and no
skip-the-work control printed `C1=met` under the counter that judges the claim. Otherwise C1 is an honest stop.

## Not claims (repairs routed by `corpus/lessons/round-34-verifier-spotcheck.md` §6)

1. Counter discrimination: round-33 §8 item 1 clause 2 (verdict cells naming a reader action, checked by something
   other than the header label) → a lesson-backed QUALITY criterion; P-C1-A1's open live-arm lower bound is recorded,
   not re-claimed.
2. SOURCES append-only form: supersede rows for S182 and S193 (`supersedes S182 —`, `supersedes S193 —`), sources
   re-opened this round; correction of `round-34.md:46`.
3. Dangling pointer `corpus/knowledge/disk-write-rate-r33.md:71`: append-only correction naming committed audits.
4. `SKILL.md:834`: re-cite the stacked-device sentence to a source that states it, or mark it observed.
5. QUALITY 98 worked example (D1, D2, D4): append a correction; 98 is not rewritten.
6. Axes table: `Last change` for depth and operability names round 28 / round 12 while the latest admitted closure
   grading each improved is round 31 (`MANIFEST rounds[495]`). Repaired as a correction, not counted by P-C1.

Operator items left alone: `LOG.md:1801`; `refs/jj/keep/…` `3b19cac`; SHONEN promotion.
