# w2 seat report — ExecRetentionData (no-harm retention scan)

Scope: falsify "wave 1 harmed the retention axis" by re-running the frozen retention gate at the
round-33 data revision and diffing its full output against the round-33 base run.
Verdict: **no harm measured on the retention axis; no new unallowlisted hit, no new hit of any class,
no change to the gate, policy, or allowlist.** Severity of the result for the retention axis: **none**.

## 1. Command run (exactly as assigned)

Sandbox clone: `/fast/scratch/hyaku/mori-r33/ExecRetentionData/clone`
(`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin <dir>`; clone HEAD == `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8`).

```
cd /fast/scratch/hyaku/mori-r33/ExecRetentionData/clone
timeout 300 python3 -I -B tools/mori-retention-gate.py scan --repo . \
  --rev 62db24c01d5b7c2247f43852ea2b28d0ae5e40c8 \
  --policy .ufo/waves/round-18/frozen/c1-policy.json \
  --allowlist corpus/evidence/retention-allowlist.json
```
Output captured at `/fast/scratch/hyaku/mori-r33/ExecRetentionData/scan-62db24c.json`
(35016 bytes; stderr empty, 0 bytes). **Exit code: `1`** (wall time 39.1 s).

## 2. Summary fields

| field | base `7d382043` | new `62db24c` | delta |
|---|---|---|---|
| metric | 4 | **4** | 0 |
| hits | 113 | 113 | 0 (sets byte-identical) |
| unallowlisted_hits | 4 | 4 | 0 (sets byte-identical) |
| non_author | 5 | 5 | 0 |
| routed | 0 | 0 | 0 |
| warnings | `[]` | `[]` | none |
| finding_id | `RETENTION_FINDINGS` | `RETENTION_FINDINGS` | none |
| policy_sha256 | `db06e9810bbfd243fb0a753a46960573df39083ea90174ce463cf2a0ab523128` | same | none |
| forbidden_allowlist | `[]` | `[]` | none |
| exit code | 1 | 1 | 0 |

Base values read from `.ufo/waves/round-33/evidence/base-retention.txt` line 2 (the JSON record;
line 1 is the command, line 3 is `exit=1`). `metric` is `len(unallowlisted_hits)`
(`tools/mori-retention-gate.py:267`), so metric 4 == the 4 rows below.

The metric did **not** rise, so no new-hit listing is required. For the record, the 4 unallowlisted
hits are unchanged and pre-existing at the base revision (path, line, class, line digest; no matched
text printed):

- `.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json` line 8 class R2
  sha256 `8d92bfa3…f0f1fb`
- same path line 11 class R5 sha256 `7f23448e…23228bd`
- same path line 12 class R6 sha256 `0cdc8972…72473a2`
- same path line 14 class R8 sha256 `1d2b6e6e…b855839`

They are a copy of the frozen round-18 policy file inside a round-20 falsify fixture directory; they
exist at both revisions and are outside the round-33 write scope. **Exit 1 is inherited from them, not
caused by wave 1** — a wave-2/round-33 report must not read `exit=1` as a wave-1 regression signal.

## 3. Set-level comparison (base vs new), script `/fast/scratch/.../ExecRetentionData/scan-62db24c.json`

Command: `python3 -I -B -c` over both JSON records, comparing
`{(path,line,class)}` sets for `hits`, `allowlisted_hits`, `unallowlisted_hits`:

```
hits added: []                 hits removed: []
unallow added: []              unallow removed: []
allowlisted added: []          allowlisted removed: []
new hits with '33' in path: []
```

Interpretation: wave 1 added 83 tree entries (`git diff --name-status 7d382043 62db24c`, 83 lines —
the whole round-33 wave-1 set plus `SKILL.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`,
`corpus/lessons/round-32.md`) and changed **not one line** that the frozen policy classes match.
`SKILL.md:718` (class R7) and `corpus/lessons/round-17.md:241` (class R6) still hit with the *same*
`line_sha256` as at base, i.e. the modified blobs still contain those byte-identical lines.

## 4. Harness-integrity checks (so "metric unchanged" cannot be an artifact)

- **Gate binary unchanged.** `tools/mori-retention-gate.py` blob is `988c5484…` at *both*
  `7d382043` and `62db24c`; `sha256sum tools/mori-retention-gate.py` in the clone =
  `cf0896a2ea36f169c9e900c58eefe7e2a900a4c9d67f849f753f4631d8ab829e`, identical to
  `git show 62db24c:tools/mori-retention-gate.py | sha256sum`. The run above used that file.
- **Policy and allowlist unchanged.** `git diff --stat 7d382043 62db24c -- tools/mori-retention-gate.py
  corpus/evidence/retention-allowlist.json .ufo/waves/round-18/frozen/c1-policy.json` printed nothing;
  neither path appears in the 83-line name-status list. Blobs at `62db24c`:
  allowlist `3f6f1527…`, policy `8bf285bd…`. No allowlist entry was added or widened in this range,
  so no new leak can have been masked by an allowlist edit.
- **Scope of the scan.** The gate walks every blob of the revision tree
  (`ls-tree -r -z --full-tree`, `tools/mori-retention-gate.py:189`) and skips a blob only when it
  contains a NUL byte (`_blob_hits`, `tools/mori-retention-gate.py:88-90`). Tree at `62db24c`:
  9846 files. The 79 new wave-1 paths (11 `corpus/evidence/sources-r33/*.src`, 11
  `corpus/evidence/recheck-r33/*`, `corpus/knowledge/disk-write-rate-r33.md`, 56 under
  `.ufo/waves/round-33/`) were each read as blobs at `62db24c` and **none contains a NUL byte**, so all
  79 were really scanned; none yields any hit of any class.
- **Working tree == measured revision.** `git -C <lane> rev-parse HEAD` = `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8`;
  `git --no-optional-locks diff --name-only 62db24c -- corpus tools .ufo/waves/round-33` = 0 paths.
  Wave-1 work was committed, so the `--rev` scan does cover wave-1's output, not a stale tree.

## 5. Findings

- **F1 — retention axis: no defect found (severity: none).** Checks run: full gate re-run at
  `62db24c` (exit 1, metric 4, hits 113, unallowlisted 4, non_author 5, routed 0, warnings []);
  set-diff of `hits` / `allowlisted_hits` / `unallowlisted_hits` against the base record (all four
  diffs empty); gate/policy/allowlist blob identity across the range; NUL-skip coverage proof over the
  79 wave-1 paths; HEAD and worktree-vs-rev check.
- **F2 — inherited gate red (severity: minor, pre-existing, not wave-1).** The gate exits 1 at
  `62db24c` solely because of the 4 round-20 `NoHarmRun` copy hits that also make the base run exit 1.
  Anyone reading only "exit=1" would misattribute it. Not repaired here: out of this seat's scope.

## 6. Risks / caveats (stated, not resolved)

- The scan reads a **committed revision only**. Wave-2 in-flight edits — including this report and any
  other uncommitted w2 file — are outside the measurement; the parent must re-run the same command at
  the round-33 integration commit before treating the axis as clean.
- [INFERENCE] The gate is a line-regex classifier over the frozen policy classes; "metric unchanged"
  proves no *policy-class* retention leak was added, not that wave-1 files are leak-free under any
  other definition of secret.
- No blocker found. No lane file was edited by this seat other than this report; no git/jj write, no
  process left running.

## 7. Housekeeping

- Tools installed or updated: **none** (no pacman/uv/npm action taken).
- Scratch (outside the lane): `/fast/scratch/hyaku/mori-r33/ExecRetentionData/` — `clone/`,
  `scan-62db24c.json`, `scan-62db24c.err`. Nothing written elsewhere in the lane.
- Commands run are the ones quoted in §1 and §3–§4; every command was wrapped in `timeout`.
