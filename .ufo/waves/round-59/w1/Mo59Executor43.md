# Mo59Executor43 — scan of every committed `.ufo/waves/*/w*-results.json` with the pinned tool

Seat: executor (read-only). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Scope item: scan every committed wave-settlement results artifact in the lane with the
pinned tool and classify pass/fail + failure classes.

- Freeze revision: `60b3a76ad0524c8978cc51922940be1c8c388915`
- Entering revision: `2b9f03975bfb6e508f35074ac8181ec8bf54e805`
- Revisions scanned (all give byte-identical results files — verified with `git rev-parse
  <rev>:<path>` per file, no DIFF lines): freeze `60b3a76`, entering `2b9f0397`,
  wave-tip `8ff344ff`, final lane HEAD `7b86704d7c0754a09958d131b64dbfa2a6d3eaed`.
- Pinned tool: `tools/mori-settlement-scan.py`, sha256
  `4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9` — **equals the frozen
  C2 PIN** (`count-c2.py:57`), and equals the working-tree copy at every revision checked.
  Frozen bytes intact: `git diff --stat -- tools/mori-settlement-scan.py
  .ufo/waves/round-59/count-c1.py .ufo/waves/round-59/count-c2.py
  .ufo/waves/round-59/contract.md` → empty.
- Tool selftest (pinned copy, `--scratch` under my scratch root):
  `SETSCAN_SELFTEST pass=10 fail=0`, exit 0.
- Scratch root: `/fast/scratch/hyaku/mori-r59/Mo59Executor43` (`mkdir -p`, `TMPDIR` set to
  it, `--scratch` passed to every counter/tool run). No lane writes; no VCS mutation in the
  lane; all fixture/sim clones were `git init`-ed under my scratch dir and asserted with
  `git rev-parse --show-toplevel` before any git command.
- Disk guard: `scripts/hyaku/disk-guard.sh status` → green before work
  (`/fast/scratch/hyaku` 592.6G free). No ENOSPC. No tool installed/updated by this seat.

## 1. Inventory of committed results artifacts

`git -C <lane> ls-tree -r <rev> --name-only` over `.ufo/waves/` yields exactly **14**
committed `*-results.json` files (12 strict + 2 adjacent) plus 2 round-23 falsify fixtures
that are not wave-settlement artifacts.

STRICT glob (`.ufo/waves/<round>/w*-results.json`), n=12:

| # | path | seats | members |
|---|------|-------|---------|
| 1 | `.ufo/waves/round-47/w1-results.json` | 42 | 42 |
| 2 | `.ufo/waves/round-47/w2-results.json` | 37 | 37 |
| 3 | `.ufo/waves/round-48/w1-results.json` | 49 | 49 |
| 4 | `.ufo/waves/round-48/w2-results.json` | 34 | 34 |
| 5 | `.ufo/waves/round-51/w1-results.json` | 68 | 68 |
| 6 | `.ufo/waves/round-52/w1-results.json` | 68 | 68 |
| 7 | `.ufo/waves/round-53/w1-results.json` | 67 | 67 |
| 8 | `.ufo/waves/round-54/w1-results.json` | 74 | 74 |
| 9 | `.ufo/waves/round-55/w1-results.json` | 64 | 64 |
| 10 | `.ufo/waves/round-56/w1-results.json` | 64 | 64 |
| 11 | `.ufo/waves/round-57/w1-results.json` | 64 | 64 |
| 12 | `.ufo/waves/round-58/w1-results.json` | 64 | 64 |

ADJACENT (committed, but not matching the strict `w*` glob), n=2:
`.ufo/waves/round-50/a2w1-results.json` (seats 64), `.ufo/waves/round-53/a2r1-results.json`
(seats 8). Both scanned anyway.

EXCLUDED (not orchestrator wave-settlement artifacts; not part of the strict or adjacent
set): `.ufo/waves/round-23/falsify/MutModeRead/bounded-results.json`,
`.ufo/waves/round-23/falsify/MutSetupPartial/bounded-results.json` — mutation-test fixtures
of a different shape. Scanned for completeness; both FAIL with
`results_not_list, seats_mismatch, lane_bad, wave_bad, round_bad` — i.e. they are not
`ufo-wave-results` objects at all, which is expected and is *not* a lane defect.

## 2. Per-file verdict with the pinned tool

Command (per file, pinned tool copy under scratch, `TMPDIR` = scratch root):

```
python3 /fast/scratch/hyaku/mori-r59/Mo59Executor43/tool/mori-settlement-scan.py <file>
```

**STRICT: pass = 11, fail = 1.**

| file | exit | verdict | classes |
|------|------|---------|---------|
| round-47/w1 | 0 | SETTLEMENT_SCAN_OK | – |
| round-47/w2 | 0 | SETTLEMENT_SCAN_OK | – |
| round-48/w1 | 0 | SETTLEMENT_SCAN_OK | – |
| round-48/w2 | 0 | SETTLEMENT_SCAN_OK | – |
| round-51/w1 | 0 | SETTLEMENT_SCAN_OK | – |
| round-52/w1 | 0 | SETTLEMENT_SCAN_OK | – |
| **round-53/w1** | **1** | **SETTLEMENT_SCAN_FAIL** | **`member[i]:extra_keys=report_file` × 67** |
| round-54/w1 | 0 | SETTLEMENT_SCAN_OK | – |
| round-55/w1 | 0 | SETTLEMENT_SCAN_OK | – |
| round-56/w1 | 0 | SETTLEMENT_SCAN_OK | – |
| round-57/w1 | 0 | SETTLEMENT_SCAN_OK | – |
| round-58/w1 | 0 | SETTLEMENT_SCAN_OK | – |

**ADJACENT: pass = 2, fail = 0** (round-50/a2w1, round-53/a2r1).

### Failure classes

Exactly **one** failure class occurs across the whole committed corpus:

- **`member[i]:extra_keys=report_file`** — 67 occurrences, all in
  `.ufo/waves/round-53/w1-results.json`, one per member (member[0] … member[66]).
  Root cause: every member object of the r53 artifact carries a fifth key `report_file`
  (e.g. `".ufo/waves/round-53/w1/Mo53Fr01.md"`) beyond the frozen member key set
  `{name, agent, output, note}` (`tools/mori-settlement-scan.py:41`, check at `:78-81`).
  This is a **writer-version difference, and it is the contract's designated drift file**:
  `contract.md` C2 "Scan arm" requires the r53 file to scan FAIL ("`report_file` extra
  keys — schema drift, reported not fixed"). The frozen counter encodes this as
  `DRIFT_SCAN = [".ufo/waves/round-53/w1-results.json"]` (`count-c2.py:76`) and requires
  a non-zero exit (`count-c2.py:253-259`). Verified: `drift=ok` in every counter run.

No other failure class appears: no `seats_mismatch`, no `duplicate_names`, no `agent_bad`,
no `missing_keys`, no `lane_bad`/`wave_bad`/`round_bad`, no `not_json`, no `top_not_object`
on any committed wave-settlement artifact. `members == seats` holds for all 14 files
(42/42, 37/37, 49/49, 34/34, 68/68, 68/68, 67/67, 74/74, 64/64 ×4, 64/64, 8/8).

### Informational (not failure classes)

`empty_output` / `notes_nonnull` are reported but are **not** failure conditions in the
pinned tool. Three committed artifacts have every member's `output` empty:

- `.ufo/waves/round-47/w1-results.json` — 42/42 empty, all 42 carry the note
  "orchestrator kernel restarted mid-wave; seat output was delivered to the orchestrator
  session but not retained — read the seat report file in the wave dir".
- `.ufo/waves/round-48/w2-results.json` — 34/34 empty, same note.
- `.ufo/waves/round-50/a2w1-results.json` — 64/64 empty, same note.

The tool's `output` check accepts `null` and `""` (`tools/mori-settlement-scan.py:87-92`),
so these scan OK. Reporting only — no remediation, no inference about why the kernel
restarted. `round-53/w1-results.json` has 1 empty member (`Mo53RevLedgerProse`, note
"spawned as job Mo53RevLedgerProse; still running at the session exit") plus the
`report_file` class above.

## 3. Cross-check against the frozen counters

Both counters were run at the freeze revision and at the final lane HEAD, with
`--scratch` pointed at my scratch root:

```
C1_SELFTEST pass=6 fail=0                       (exit 0)
C2_SELFTEST pass=10 fail=0 → SETSCAN_SELFTEST pass=10 fail=0  (exit 0)

C1@60b3a76 : C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=60b3a76…
C1@7b86704d: C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=7b86704d…

C2@60b3a76 : C2=unmet … failed=copy_absent:corpus/evidence/sources-r59/w1-results-r54.json,
             …-r55, …-r56, …-r57, …-r58, w1-settlement-r58, entry_absent, tree   (exit 1)
C2@7b86704d: C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok
             tree=ok claims=13 files=6 rev=7b86704d…                              (exit 0)
```

The C2 `@freeze` arm is the contract's do-nothing control for the *data* half: the tool,
the frozen counter and the 12 hostile trees are all present at `60b3a76`, but the entry
and the six artifact copies were not yet landed — so `entry/rows/pins/tree` are unmet while
`selftest/scan/drift/trees` are already ok. The tool itself is absent at the entering
revision (`git show 2b9f0397:tools/mori-settlement-scan.py` → no such object), which is
the contract's `failed=tool_absent` control.

Independently re-derived the counter's scan arm by feeding the five `REAL_SCAN` files
(`count-c2.py:69-75`) to the pinned tool in one invocation:
`verdict: SETTLEMENT_SCAN_OK failures: 0`, per-file seats==members (74, 64, 64, 64, 64).

## 4. One defect found and its minimal fix (falsified in a scratch clone)

**Defect.** In the working-tree landing of the C2 depth entry (commit `be737211`, before
the correction), the entry `corpus/knowledge/wave-settlement-artifacts-r59.md` carried a
claim `K11` citing `corpus/evidence/sources-r59/w1-results-r53.json`. The frozen
`ARTIFACTS` map (`count-c2.py:55-68`) contains exactly six entries — r54, r55, r56, r57,
r58 wave-results copies and the r58 settlement-summary copy — and **no r53 copy**. The
entry evaluator therefore emits `files:outside=<copy>` (`count-c2.py:137-138`), which
makes the whole entry arm unmet.

Reproduced exactly, without touching the lane, in a scratch clone
(`/fast/scratch/hyaku/mori-r59/Mo59Executor43/simrepo`, `git init`-ed there, toplevel
asserted) containing the landed working-tree files:

```
C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=bad rows=ok pins=ok tree=ok
    claims=14 files=6 failed=entry
```

**Minimal fix, falsified in four scratch variants:**

| variant | change | counter result |
|---------|--------|----------------|
| simrepo  | as-landed | `C2=unmet … failed=entry` |
| simrepo2 | drop r53 copy + K11 claim + `source: S559` line | `C2=met … claims=13 files=6` |
| simrepo3 | keep r53 copy on disk; drop K11 + `source: S559` | `C2=met … claims=13 files=6` |
| simrepo4 | **minimal**: drop only the K11 claim line | `C2=met … claims=13 files=6` |

So the minimal correction is to demote the K11 claim to prose (the r53 `report_file`
observation stays in the entry body as prose, not as a pin-bound claim over a copy that
the frozen ARTIFACTS map does not admit).

**Status: already fixed in the lane.** The lane advanced to
`7b86704d "round-59: data correction — K11 demoted to prose (r53 copy outside frozen
ARTIFACTS)"`. At that revision the counter reports
`C2=met … claims=13 files=6`, and the committed entry holds 13 pin-bound claims. The
committed `corpus/evidence/sources-r59/` directory holds 7 copies (the 6 in ARTIFACTS plus
the r53 copy, which is byte-identical to its artifact and harmless — the counter's tree
arm only checks the six ARTIFACTS pairs). No further action required; the defect is
closed and independently confirmed by both the counter and my sandbox falsification.

## 5. Other observations (detection only, no remediation)

1. **Registry row shape, S560.** The `S560` row appended in commit `be737211` contained a
   literal backslash-escaped pipe inside a cell (`grep -n '10.1109/TSC.2026.3698682\|1603404d' …`),
   which the census pipe-splitter counted as a field separator: the row split into 12
   cells instead of 11 and the census emitted `mori E01 S560 fields=12`. The cell was
   re-escaped in the working tree before my final census run; at the final census run
   `SOURCES.md` parses to 11 cells and the census is clean:
   `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → exit 0,
   no `E0x` codes, last line `mori ok …/corpus/SOURCES.md` (26 lines, all `W04` duplicate-URL
   warnings that pre-date this round).
2. **`used-by` path existence — resolved.** The census `E11` check
   (`scripts/sources-census.sh:560-568`) only fires for `mined` rows, so the `rejected`
   `S560` row never triggers it. When I first inspected the registry, `S560`'s `used-by`
   path `corpus/lessons/round-59.md` did not exist on disk (dangling path, no `E11` raised).
   The owning seat has since landed that lesson file in the working tree (5718 bytes,
   `?? corpus/lessons/round-59.md`), so the path now resolves. Noted for the record; I did
   not create it and did not infer intent.
3. **Source-drift noise.** `tools/mori-source-drift.py --root <lane>` reports the eight new
   rows `S553`–`S560` as `no-copy`. That is a naming-convention mismatch, not missing
   evidence: the tool looks for `corpus/evidence/sources-r<N>/<sid>.<ext>`
   (`tools/mori-source-drift.py:76`, `COPY_DIR_RE` at `:48`), whereas the landed copies are
   named after the artifact (`w1-results-r54.json`, …). The copies are present and
   byte-identical to their artifacts. The tool also exits 1 on the pristine `HEAD` clone
   (`rows=325 fresh=54 drifted=21 unavailable=1 no-copy=249`), so the exit code is a
   pre-existing condition, not a regression introduced this round — the working-tree run
   adds exactly the 8 `no-copy` lines and nothing else.
4. **`empty_output` is not a failure class.** The pinned tool treats an empty/`null`
   member `output` as valid. Three committed artifacts (r47/w1, r48/w2, r50/a2w1) are
   100% empty-output with a kernel-restart note, yet scan OK. If the round wants
   "settled with retained output" to be a distinct condition from "schema-valid", that
   would be a new tool capability, not a defect in the frozen one — reported, not built.

## 6. Constraints honoured

- No production file, registry, SCORECARD, LOG or lane VCS state was edited by this seat.
  `git status --porcelain` in the lane at the end shows only the peers' in-flight changes
  (` M LOG.md`, ` M SHONEN.md`, ` M corpus/QUALITY.md`, plus untracked
  `.ufo/waves/round-59/w1/`, `.ufo/waves/round-59/w1.ready.dispatched`) — none of which
  this seat produced; this seat wrote exactly one file, this report.
- Every git mutation was performed inside a scratch clone created with
  `git init -q` at an explicit path under `$HYAKU_SCRATCH/mori-r59/Mo59Executor43`, with
  `git rev-parse --show-toplevel` asserted to that path before the mutation.
- Lane reads used `git show <rev>:<path>` / `git ls-tree` only.
- No fleet-root or sibling-repo writes. No `agent://all` broadcast. No seat spawns.
- No remediation performed: the one defect found (K11 outside frozen ARTIFACTS) was
  reported with a falsified minimal fix and was independently corrected by the owning
  seat before final HEAD.

## 7. Reproduction commands

```bash
SC=/fast/scratch/hyaku/mori-r59/Mo59Executor43
REPO=/home/vgpnk/Projects/shokunin/mori-shokunin
mkdir -p "$SC"; export TMPDIR="$SC"
git -C "$REPO" show 60b3a76ad0524c8978cc51922940be1c8c388915:tools/mori-settlement-scan.py \
  > "$SC/tool/mori-settlement-scan.py"
sha256sum "$SC/tool/mori-settlement-scan.py"   # 4c04bf21…5ac9a9 == frozen PIN
python3 "$SC/tool/mori-settlement-scan.py" --selftest --scratch "$SC/st"   # pass=10 fail=0
python3 "$SC/scan_strict.py" 7b86704d7c0754a09958d131b64dbfa2a6d3eaed        # 11 pass / 1 fail
python3 "$REPO/.ufo/waves/round-59/count-c1.py" 7b86704d… --repo "$REPO" --scratch "$SC/c1"
python3 "$REPO/.ufo/waves/round-59/count-c2.py" 7b86704d… --repo "$REPO" --scratch "$SC/c2"
```
