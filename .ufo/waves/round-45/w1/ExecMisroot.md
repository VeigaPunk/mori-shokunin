# ExecMisroot — misroot and hygiene sweep, mori round 45 wave 1

Seat `L1Mori45.ExecMisroot`, leaf executor. Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`;
fleet root `/home/vgpnk/Projects/shokunin` (read-only for me). Contract read first
(`.ufo/waves/round-45/contract.md`, P-C1/P-C2/P-C3, kill rules, floors). All commands below were
read-only git/grep/find plus one scoped `rm` of my own scratch; nothing in the fleet repo was
mutated.

## Verdict

**Zero seat misroots.** No untracked file at the fleet root, and no changed file in any sibling
lane, names both mori and round 45. Consequently: **copies made = 0, `cmp` runs = 0,
fleet-root deletions = 0.** The only deletion executed was my own scratch directory (and one file
my own mistyped redirect created inside the lane); both are listed in §3. Sibling lanes contain
45 mori-naming dirty files, every one pre-existing lane-local work (mtimes 2026-10-15 … 2026-10-25
06:45, i.e. before this wave's 07:39 start), none a mori round-45 artifact.

## 1. Fleet-root untracked inventory

`git -C /home/vgpnk/Projects/shokunin status --porcelain` → 24 entries, exit 0: **17 `M`** (14
`.ufo/state/*.report-baseline`, `.ufo/watchdog.log`, `scripts/hyaku/hyaku.env`,
`scripts/hyaku/lane-addendum.md`) and **7 `??`**. `-uall` expands the seven `??` entries to
exactly seven files (no collapsed directories):

```
?? .omp/mcp.json
?? .scratch/goal-20261025-hyaku-12h.md
?? .ufo/state/kotoba.report-baseline
?? .ufo/state/kotodama.report-baseline
?? .ufo/state/revenger.report-baseline
?? .ufo/waves/round-24/w2/RevUnlandedResolution.md
?? .ufo/waves/round-69/w1/ScoutAmp.md
```

Each was opened (first 20 lines, per the item) and grepped in full for `mori` and for
`round[ -]45|r45`:

| path | first-20-lines content | mori | round45 | disposition |
|---|---|---|---|---|
| `.omp/mcp.json` | MCP config, one disabled `rea` server, no seat/lane text | 0 | 0 | other lane/config — untouched |
| `.scratch/goal-20261025-hyaku-12h.md` | self-declared `ORCHESTRATOR-OWNED run state (hyaku run 6)`; line 2 says "Not a misroot: lanes and seats never move, copy-then-delete, or edit this file" | 2 | 0 | `.scratch/`, orchestrator state — untouched |
| `.ufo/state/kotoba.report-baseline` | `69 e3b0c442…` | 0 | 0 | `.ufo/state/` — untouched |
| `.ufo/state/kotodama.report-baseline` | `70 e3b0c442…` | 0 | 0 | `.ufo/state/` — untouched |
| `.ufo/state/revenger.report-baseline` | `69 e3b0c442…` | 0 | 0 | `.ufo/state/` — untouched |
| `.ufo/waves/round-24/w2/RevUnlandedResolution.md` | tabi seat r24 ("Lane root `/home/vgpnk/Projects/shokunin/tabi-shokunin`") | 0 | 0 | another lane, another round — untouched |
| `.ufo/waves/round-69/w1/ScoutAmp.md` | round-69 seat (no mori lane named) | 0 | 0 | another lane, another round — untouched |

Because the mori×round-45 conjunct is empty, the copy→`cmp`→delete branch never triggered:
**no file qualified, so no byte-exact copy and no `cmp` exists to report.** That absence is the
measured result, not an unrun check.

Two corroborating facts: the fleet root has **no** `.ufo/waves/round-45/` directory at all
(`test -e .ufo/waves/round-45` → NO), while `.ufo/reports/round-45/{chousa,kake,kumitate}.md` and
`.ufo/prompts/mori-round-45.md` are tracked orchestrator files (they appear in neither the `M`
nor the `??` set), so they are not seat droppings. `.ufo/waves/round-24/` and `round-69/` are the
only untracked fleet wave dirs, and each holds one file from a different lane.

## 2. Sibling-lane sweep

Method: for every `*/` in the fleet root that has `.git` (21 lanes; mori excluded as the lane under
test), materialise `git status --porcelain` paths, expand untracked directories with `find -type f`
(1216 files total), then `grep -lIE` for `mori-shokunin|\bmori\b|/mori/` (strict; the loose
case-insensitive form false-positives on "memorise"/"re-memorize" in kumitate `corpus/QUALITY.md`
and `SOURCES.md`) and for `round[ -]45|\br45\b`.

Dirty counts: `chousa 16, kake 1, kama 102, kotoba 2, kumitate 27, mado 1, mori 8 (the lane under
test, excluded), revenger 1, souji 1`; the other 12 lanes are clean. Lanes/dirs with no git repo at
all (`research/`, `scripts/`, `templates/`) are not lanes.

**Intersection mori ∧ round-45 = 0 files.** Not one changed sibling file names mori and round 45.

**mori-naming files = 45**, all lane-local and all predating this wave:

- `kama-shokunin` — 34 files, all under untracked `.ufo/waves/round-35|36|37/` debris plus two
  tracked-dirty corpus files (`LOG.md:1925` "S179 (mori r36 source-drift …)", `corpus/SOURCES.md`).
  The 34 include `round-37/w1/out/ExecMisroot.md` (kama's own sweep; its only mori line is
  `M .ufo/state/mori.report-baseline`, an observation of the fleet root, not a write) and
  `round-37/w1/out/L1Kama37.*/…`
- `souji-shokunin` — 8 files in untracked `census/operator-sweep-20261019/` (the 2026-10-19
  operator census; mori appears only as scanned `/tmp/mori-r12-base.…` / `jj-probe-mori-pin.txt`
  entries).
- `kumitate-shokunin` — 2 files: `.ufo/waves/round-61/w1/ConnectorSiblings.md:108-113` and its
  `build/ConnectorSiblings/scan.md`, quoting mori r44 M6 as prior art.
- `chousa-shokunin` — 1 file: `.ufo/waves/round-41/w1/swarm-registry.json` ("mori pin/drift
  lineage").

Newest mtime among the 45: `kumitate …/ConnectorSiblings/scan.md` at 2026-10-25T06:45:37. Files
written after 07:00 today in any sibling (8 total: revenger r69 replay, kumitate r60/r61 items,
kake r52 ladder, kotoba r69 receipts, chousa r46 RevRerunC1) were each re-grepped individually:
`mori=0 r45=0` for all 8. So no wave-1 seat wrote into a sibling repo.

## 3. Deletions and scratch

- Removed at end: `.ufo/waves/round-45/tmp/ExecMisroot/` (my scratch; held 7 grep/list artifacts).
  `rm -rf` exit 0. Nothing of mine remains under `tmp/`.
- Self-inflicted, removed: `mori-shokunin/.ufo/never`, an empty file my own mistyped redirect
  created at 07:41 and deleted in the next command. It existed only inside the lane and for
  seconds; it never existed in the fleet repo.
- No fleet-root deletion was performed (nothing qualified under §1).
- Scratch home for scans was `TMPDIR=.ufo/waves/round-45/tmp/ExecMisroot`; `/tmp` was not used.

**26 peer scratch dirs remain** under `.ufo/waves/round-45/tmp/` and are left untouched (not mine):
`CritAxisHarm, CritC2Target, CritContract, ExecCollisionGuard, ExecControlReceipts,
ExecSelftestModes, ExecWitnesses, MutAuditor, MutCounters, PlanDataWalk, RevAudit, RevBeforeAfter,
RevC1Grammar, RevCensusAppend, RevEntryQuotes, RevengerAuditorHistory, ScoutCensusBytes,
ScoutConsider, ScoutKernelDoc, ScoutS472, ScribeLesson, ScribeQuarantine, ScribeRegistryRows,
ScribeRows, SentInstruments, SimpInstruments`. The count grew from 8 to 26 during the sweep as
peers started — consistent with a live wave, not with leakage.

Lane worktree at sweep end (`git -C mori-shokunin status --porcelain`): 8 untracked round-45 paths
(`assimilation/{collisions,quarantine-slice,reg-ids,renumber-map.tsv,staged-ids}`, `evidence/`,
`tmp/`, `w1/`) — all expected round-45 work in the lane, none a fleet-root artifact.

## 4. Tooling

No installs or upgrades. `pacman` untouched (host-wide pause), no `uv`/`npx`/binary fetch needed;
read-only git, `find`, `grep`, `stat`, `rm` only.

## 5. Risks / notes for the L1

1. `kama-shokunin` carries 102 dirty paths and `kumitate-shokunin` 27 — pre-existing backlog, not
   this round's, but any future mid-flight `git status` audit over the fleet will keep seeing false
   mori hits there. A lane-local cleanup round (not a mori r45 seat) is the right owner.
2. The loose `grep -i mori` form is unsafe for this sweep: "memorise"/"re-memorize" produced 4 of
   the 63 raw hits. Any future ExecMisroot receipt should pin the strict
   `mori-shokunin|\bmori\b` pattern and record it, otherwise reviewers will re-litigate noise.
3. Fleet-root state baselines are modified for 14 lanes (`M .ufo/state/*.report-baseline`), which
   is orchestrator-owned live state; a seat that "cleans" them would corrupt report drift
   accounting. Out of scope here, flagged only.
