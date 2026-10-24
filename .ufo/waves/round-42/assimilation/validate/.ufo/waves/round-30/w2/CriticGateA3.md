# CriticGateA3 — attack on amendment A3 (gate allowlist admits two host instruction files)

**Verdict: agree.** Admitting exactly the two paths opens no route by which a writer could have seen tool source,
tool output or expected values. Neither file carries rule text, expected values or tool content. A3 corrects an
instrument defect; it does not narrow the claim. It is still an after-data loosening of A2's literal "anything else is
a violation", and the closure must rule on that tradeoff. The ruling cannot change the round outcome: C2.4 misses
under both gate versions (A2: 4 violations, A3: 1). Two minor instrument defects found outside the admitted paths are
listed under Defects.

Attacked item: `git diff 32e287ff 55f9a694 -- .ufo/waves/round-30/check-blind-wave.sh`, which adds the case arm at
`check-blind-wave.sh:18-20` (blob `dbcbe50e`, identical at `55f9a694`, `db1ec469` and `ad0f0474`: `git rev-parse <rev>:<path>`).

## 1. What the two files contain (read in full)

- `/home/vgpnk/.agents/skills/godspeed/SKILL.md` (869 bytes, sha256 `1d616723…f83a`): YAML front matter (name, description,
  triggers) and a four-line posture list ("Name the axes", "Iterate cheap, in parallel", "Keep moves that improve any axis
  and harm none", "Don't aim"). It ends with a line telling the agent to stop asking clarifying questions and to batch tool
  calls. Its only sibling, `directive.md` (429 bytes), holds the same body with no front matter.
- `/home/vgpnk/.omp/agent/RULES.md` (995 bytes, sha256 `beb647d0…99ed`): the operator tooling directive of 2026-10-19
  (install channel order; a pacman `-Syu` safety note about mkinitcpio and boot hooks; record every install).
- Neither file mentions earlyoom, systemd, `mori-oom-killers`, any verdict token (`KILLER_ACTED`/`KILLERS_QUIET`/
  `KILLERS_UNKNOWN`), any case field, any fixture, or any lane path. Neither carries rule text, expected values, tool
  source or tool output. Evidence: the read tool on both paths.

## 2. Could a writer have seen different bytes at those paths? No.

- Both are regular files, not symlinks. `readlink -f` returns the path itself. `namei -l` shows real directories along
  the whole path, so no link reaches into the lane or the fleet. `ls -la /home/vgpnk/.agents/skills` shows that some
  sibling skills (shokunin, ufo, tower, swarm) are symlinks into `/home/vgpnk/Projects/ompskills`, but `godspeed` is a
  real directory.
- `stat`: SKILL.md mtime 2026-10-06 15:44 -0300, ctime 2026-10-19 10:17 -0300. RULES.md mtime and ctime 2026-10-19
  18:31 -0300. Both predate the round-30 contract commit `a66751b` (2026-10-22 18:00:36 -0300, `git log`) and the
  writers' recorded access times (21:12Z = 18:12 -0300, `git show db1ec469:.ufo/waves/round-30/w1/CaseR30a.md` :99 and
  `CaseR30c.md` :80). So the writers read the bytes I read, and no writer wrote to these files during the wave. [INFERENCE: ctime
  cannot be set backwards without root or a clock change; nothing indicates either.]

## 3. Is the admission exact? Mutation probes on the A3 blob

Setup: a sandbox clone at `/fast/scratch/hyaku/mori-r30-w2/CriticGateA3/clone`, checked out at `db1ec469`, gate taken
from `git show 55f9a694:…` (`git hash-object` = `dbcbe50e`). The writers' lane-absolute `rule-text.md` entries were
remapped to the clone root (see D2). With only that remap, the probe reproduces the lane result exactly
(`blind_violations=1`, `CaseR30a.md:105`). The A2 blob on the same commit reproduces the A2 receipt (4 hits at a:96,
b:116, c:79, d:110). Removing only the `json.load` token from a:105 gives the probe base: A3 gate
`scanned=4 blind_violations=0`. Each probe below replaces CaseR30a line 97 on that base:

| probe entry | A3 result |
|---|---|
| `/home/vgpnk/.omp/agent/RULES.md` | 0 (admitted) |
| `- /home/vgpnk/.omp/agent/RULES.md:1-14` | 0 (`:L-M` stripped at `:45`, same file) |
| `…/RULES.md;` and `…/RULES.md (read; tooling directive)` | 0 (punctuation trimmed at `:34-37`; plain words are not candidates) |
| `/home/vgpnk/.agents/skills/godspeed/directive.md` | 1 |
| `/home/vgpnk/.omp/agent/RULES.md.bak` | 1 |
| `/home/vgpnk/.omp/agent/../../Projects/shokunin/mori-shokunin/tools/mori-oom-killers.py` | 1 |
| `/home/vgpnk/.agents/skills/godspeed/SKILL.md/../../../../Projects/…/fixtures/mori-oom-killers/cases.json` | 1 |
| `/home/vgpnk/.omp/agent/RULES.md tools/mori-oom-killers.py` | 1 (each token is checked) |
| `/home/vgpnk/.omp/agent/RULES.md — then mori-oom-killers.py` | 1 |
| RULES.md joined by a comma to another file in the same OMP agent directory | 1 |
| another file in the same OMP agent directory | 1 |
| `file:///home/vgpnk/.omp/agent/RULES.md` | 1 (the `file://` arm matches first, so the A3 arm is never reached) |
| `~/.omp/agent/RULES.md` | 1 |
| `skill://godspeed` | 1 |

The case patterns hold no `*` or `?`, `set -f` is on (`:3`), and `.` is literal in a case glob. The arm therefore
matches only the two whole tokens. No traversal, prefix, suffix, sibling or joined form gets through. The last three
rows are false positives, but they fail in the safe direction: they can only add violations. Commands: the probe loop
in the clone, with output as listed. One harness slip (probe M1 left nothing to commit, so its reset discarded the base
commit) was caught. The table comes from the corrected rerun, which resets to the base before each probe.

## 4. Other routes a writer could use to reach tool content through A3: none found

- The task hook injects the godspeed skill into each prompt. The admitted file and its sibling carry only posture text
  (§1), so the injection adds no content beyond what the gate admits.
- RULES.md authorizes tool installs, but it names no lane path. Opening any lane path is still caught by the unchanged
  allowlist (`:22-23`).
- A3 leaves the leak classes untouched: tool line citation (`:121-123`), tool output markers (`:135-151`) and the
  missing files-opened list (`:156-158`). Tokens from the two files are not checked by those rules, so admitting the
  files does not hide them.
- Residual, unchanged by A3: the gate trusts each writer's self-reported files-opened list. That limitation predates A3
  and is no reason to reject it.

## 5. Ruling: correction of an instrument defect, not a narrowing of the claim

What favors correction:
- The C2.4 claim and its condition are unchanged: the same writers, cases and leak classes, `blind_violations=0` at
  the freeze, and k equal to the number of authors (`contract.md:75-79`, `:162-165`). A3 only reclassifies two tokens
  that are false positives with respect to the property the gate measures, which is whether writers saw tool source,
  output or expected values (§1).
- The original writer bound forbids "other lane file[s]" (`contract.md:81-84`). A2's allowlist was introduced against
  tool copies outside the lane (`contract.md:166-172`, G3/G4), and these files are not such copies.
- The change was not fitted to pass. The gate records only the first forbidden line per file (`:129-131`), so the A2
  receipt could not reveal the a:105 hit, and the A3 gate still fails (`blind_violations=1`, rerun above). The author
  reports C2 as a miss (`evidence/c2-after.txt` :21-23, rerun independently here) and keeps the A4 matcher run labelled
  "UNCOUNTED, after-data diagnostic" (`evidence/gate-a4-diagnostic.txt` :1).
- It is disclosed as after-data, the A2 receipt stays committed (`evidence/gate-a2-prefreeze.txt`), and the lesson
  records the cause (`corpus/lessons/round-30.md:94-99`, M5).

The tradeoff the closure must rule on (not a fixable defect):
- Under the letter of A2 ("anything else is a violation", `contract.md:166-170`) and the brief's "read only
  `rule-text.md` and public upstream … sources" (`contract.md:81-83`), the 4 A2 hits were real rule violations. A3
  rewrites the written rule after the L1 saw gate output (`contract.md:207`). A2's own preamble allows only changes that
  make C2 harder or "fix a counter defect" (`contract.md:159`). A3 fits the second category in substance, but it makes
  the gate easier to pass.
- Outcome sensitivity is nil: C2.4 = miss under A2 (4) and under A3 (1). So the closure loses nothing by ruling A3 a
  correction while still recording C2 as missed.

## Defects (none opens a leak path)

- **D1, untested branch.** No committed instrument exercises the A3 arm. The self-test fixtures (`:192-198`) plant
  neither path and no near-miss. `git show ad0f0474:.ufo/waves/round-30/count-c2.sh | grep -c -E 'godspeed|RULES'` → 0,
  so the counter's planted mutants do not touch it either. The probes in §3 are the only test of the arm. Smallest
  correction, for the next gate version since the freeze blob is fixed: one planted writer that lists both exact paths
  and must pass, and one that lists `directive.md` plus a `..` traversal and must fail.
- **D2, gate result depends on the checkout path, outside A3.** `rule_abs="$repo_root/$rule_rel"` (`:86-87`) comes from
  the checkout running the gate, while the writers recorded lane-absolute paths. Run from a clone, the A3 gate flags
  every writer's `rule-text.md` entry (`blind_violations=4` at a:98, b:117, c:78, d:111 in my unmapped clone run). The
  counter works around this by running with `cwd=LANE` (`count-c2.sh:192-198`). Independent re-runs from sandbox clones,
  which the wave bounds require, therefore give false failures unless the paths are remapped. Smallest correction: also
  accept the fixed lane-absolute path as a constant.
- **D3, masking.** Reporting only the first forbidden line per file (`:129-131`) hid the a:105 hit behind the godspeed
  hit at A2 time, so A3 was written without seeing every defect. Smallest correction: report every forbidden line.
  The remaining a:105 hit is the prose token `json.load` in "The scratch JSON passed python3 json.load; …" (`git show
  db1ec469:…/CaseR30a.md`, line 105), not an opened file.

Impacted axes: operability (C2.4 instrument fidelity). No leak path, so the C2 cases and their blindness are not
affected. A3 itself has no impact on depth (C1).

## Bounds and tooling

Read-only git in the lane. Writes only in this report and `/fast/scratch/hyaku/mori-r30-w2/CriticGateA3/` (sandbox
clone, gate copies, probe commits). No tools installed or updated. RULES.md was read first, as directed. No units,
processes, settings or other repos were touched.
