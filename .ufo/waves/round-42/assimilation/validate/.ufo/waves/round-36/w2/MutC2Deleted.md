# MutC2Deleted — C2 deleted-row arm removal (mutation probe)

measured 2026-10-23T19:14Z (host tz -03:00) by seat `mori-r36-w2-MutC2Deleted-28`
Target: `tools/mori-sources-appendonly.py` (C2 gate) at data tip `bf0df77fee4b6ef54a90aea09335c7617f125151`
Detector: frozen `.ufo/waves/round-36/count-c2.py`, `--seed 11`
Item attacks: **C2's deleted-row arm** — the claim that the gate reports ids held by an ancestry commit and absent
at `<rev>` (`deleted=[...]`, `deleted <id>` lines), and the frozen counter's sensitivity to that arm being removed
(control shape J5, "no deleted arm", contract.md table row `rule-level skips`).

## Frozen inputs measured before any mutation

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ sha256sum .ufo/waves/round-36/count-c2.py .ufo/waves/round-36/contract.md tools/mori-sources-appendonly.py
c7edaacfff029c2055bee6ddda42ff6f5c040dad7fbac81e9d169602edcbac34  .ufo/waves/round-36/count-c2.py
f88cf4d254c5582588be122251902d2429f2d69ec1950220ce78e62dc1bbeea1  .ufo/waves/round-36/contract.md
915527a7d2f553740ed3ab0166669031f19ce2de6b2fec8501208f97244cfc89  tools/mori-sources-appendonly.py
```
counter sha `c7edaac…` matches `evidence/freeze-v2.txt:3`. The tool bytes at the tip equal the working-tree bytes:
```
$ git show bf0df77f:tools/mori-sources-appendonly.py | sha256sum
915527a7d2f553740ed3ab0166669031f19ce2de6b2fec8501208f97244cfc89  -
```
`contract.md` at HEAD is **not** the freeze-v2 pin (`dbd3f6d7…`); the pin matches the C0 commit, and the file was
amended after the freeze (declaration `5842dc0`, integration `9ca8f2e`, close-out `6827d6e`):
```
$ git show c1a026c:.ufo/waves/round-36/contract.md | sha256sum
dbd3f6d793239a2f729f89778847eb47b901167fa7a98f57269621f4273c4127  -
$ git show c1a026c:.ufo/waves/round-36/count-c2.py | sha256sum
c7edaacfff029c2055bee6ddda42ff6f5c040dad7fbac81e9d169602edcbac34  -
```
My detector is the counter, whose bytes match the freeze pin; the amended prose does not change P-C2, and the
amendments are the ones the contract records itself. Not scored as a defect for this probe (freeze integrity is a
sibling item); recorded because the hash was measured and differs.

## Mutation

Copied the tip bytes to `/fast/scratch/hyaku/mori-r36/MutC2Deleted/pristine.py`, then one line in the copy:

```
$ git diff --no-index --unified=2 pristine.py mutant.py
--- 1/pristine.py
+++ 2/mutant.py
@@ -240,5 +240,5 @@ def analyze(repo, rev, path, round_base=None):
                  if cid not in first
                  or imm_key(cells, imm_idx) != imm_key(first[cid], imm_idx))
-    deleted = sorted(set(first) - set(tip))
+    deleted = []          # mutation: deleted-row arm removed
     sup_map = superseders(tip_rows, colmap)
     superseded = sorted(cid for cid in ids if cid in sup_map)
```
`tools/mori-sources-appendonly.py:242` → the deleted list is never populated, so neither the `deleted <id>` lines
(`:280`) nor the summary `deleted=[...]` can ever name a deleted id; `violations` (`len(ids)+len(deleted)`) stops
counting deletions. Deletion events still reach `round_changed` through `deleted_at` (`:220`, `:235`, `:255`), so this
probe is **strictly weaker** than the J5 control (which also stripped deletion events from `round_changed`).

```
$ sha256sum pristine.py mutant.py
915527a7d2f553740ed3ab0166669031f19ce2de6b2fec8501208f97244cfc89  pristine.py
e71495b832f9a294334ec681807302138dcaf90a9add6250e1b0cb1276e4569f  mutant.py
```

## Detector runs — pristine, mutant, restored (same seed, same 24 histories)

Command shape (frozen counter, `--tool` copies; the wrapper is explained under *Harness note* below):

```
unshare -rm sh -c 'mount -t tmpfs tmpfs /fast/scratch/hyaku/mori-r36; cd /home/vgpnk/Projects/shokunin/mori-shokunin
  TMPDIR=/tmp/mutc2 python3 .ufo/waves/round-36/count-c2.py bf0df77fee4b6ef54a90aea09335c7617f125151 --tool <T> --seed 11'
```
Log: `/fast/scratch/hyaku/mori-r36/MutC2Deleted/all-runs.txt` (copied from `/tmp/mutc2/all-runs.txt`).

### Stage 1 — pristine (`--tool pristine.py`, sha `915527a7…`), exit code 0

```
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /tmp/mutc2/pristine.py
blind arm: 24/24 sandbox histories matched the hidden truth (1.8s; coverage: deletions=24 changed-back=16 superseded=12)
real arm: pass (0.3s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
C2=met
seed=11
COUNTER_EXIT=0
```
Baseline passes — a mutant failure below is a kill, not a baseline failure.

### Stage 2 — mutant (`--tool mutant.py`, sha `e71495b8…`), exit code 1

```
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /tmp/mutc2/mutant.py
blind arm: 0/24 sandbox histories matched the hidden truth (1.6s; coverage: deletions=24 changed-back=16 superseded=12)
  repo00 FAIL: lists differ
      want: appendonly_violations=3 ids=[S096,S143] deleted=[S203] superseded=[S096,S143] round_changed=[S016,S143,S203]
      got:  appendonly_violations=2 ids=[S096,S143] deleted=[] superseded=[S096,S143] round_changed=[S016,S143,S203]
  repo01 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S079] superseded=[] round_changed=[]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  repo02 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S044] superseded=[] round_changed=[]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  repo03 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S017] superseded=[] round_changed=[S017,S162]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[S017,S162]
  repo04 FAIL: lists differ
      want: appendonly_violations=3 ids=[S275] deleted=[S140,S194] superseded=[S275] round_changed=[S194]
      got:  appendonly_violations=1 ids=[S275] deleted=[] superseded=[S275] round_changed=[S194]
  repo05 FAIL: lists differ
      want: appendonly_violations=5 ids=[S021,S085,S200] deleted=[S237,S240] superseded=[S021] round_changed=[S085,S200,S240]
      got:  appendonly_violations=3 ids=[S021,S085,S200] deleted=[] superseded=[S021] round_changed=[S085,S200,S240]
  repo06 FAIL: lists differ
      want: appendonly_violations=2 ids=[] deleted=[S270,S272] superseded=[] round_changed=[S245,S270,S272]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[S245,S270,S272]
  repo07 FAIL: lists differ
      want: appendonly_violations=2 ids=[] deleted=[S021,S218] superseded=[] round_changed=[S218]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[S218]
  repo08 FAIL: lists differ
      want: appendonly_violations=4 ids=[S163] deleted=[S128,S143,S217] superseded=[S163] round_changed=[S128,S217]
      got:  appendonly_violations=1 ids=[S163] deleted=[] superseded=[S163] round_changed=[S128,S217]
  repo09 FAIL: lists differ
      want: appendonly_violations=2 ids=[S282] deleted=[S009] superseded=[S282] round_changed=[S009,S031,S282]
      got:  appendonly_violations=1 ids=[S282] deleted=[] superseded=[S282] round_changed=[S009,S031,S282]
  repo10 FAIL: lists differ
      want: appendonly_violations=2 ids=[] deleted=[S228,S244] superseded=[] round_changed=[S057,S244]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[S057,S244]
  repo11 FAIL: lists differ
      want: appendonly_violations=4 ids=[S137] deleted=[S102,S148,S172] superseded=[] round_changed=[S102,S137,S148,S172,S257]
      got:  appendonly_violations=1 ids=[S137] deleted=[] superseded=[] round_changed=[S102,S137,S148,S172,S257]
  repo12 FAIL: lists differ
      want: appendonly_violations=3 ids=[S193] deleted=[S054,S203] superseded=[S193] round_changed=[S054]
      got:  appendonly_violations=1 ids=[S193] deleted=[] superseded=[S193] round_changed=[S054]
  repo13 FAIL: lists differ
      want: appendonly_violations=3 ids=[S045] deleted=[S257,S271] superseded=[S045] round_changed=[]
      got:  appendonly_violations=1 ids=[S045] deleted=[] superseded=[S045] round_changed=[]
  repo14 FAIL: lists differ
      want: appendonly_violations=6 ids=[S082,S234] deleted=[S122,S218,S262,S270] superseded=[S082] round_changed=[S234,S262]
      got:  appendonly_violations=2 ids=[S082,S234] deleted=[] superseded=[S082] round_changed=[S234,S262]
  repo15 FAIL: lists differ
      want: appendonly_violations=2 ids=[S105] deleted=[S196] superseded=[] round_changed=[S011,S196]
      got:  appendonly_violations=1 ids=[S105] deleted=[] superseded=[] round_changed=[S011,S196]
  repo16 FAIL: lists differ
      want: appendonly_violations=2 ids=[S278] deleted=[S142] superseded=[S278] round_changed=[S142]
      got:  appendonly_violations=1 ids=[S278] deleted=[] superseded=[S278] round_changed=[S142]
  repo17 FAIL: lists differ
      want: appendonly_violations=2 ids=[S073] deleted=[S242] superseded=[S073] round_changed=[S073,S150,S242]
      got:  appendonly_violations=1 ids=[S073] deleted=[] superseded=[S073] round_changed=[S073,S150,S242]
  repo18 FAIL: lists differ
      want: appendonly_violations=2 ids=[S136] deleted=[S005] superseded=[] round_changed=[S005,S136,S158]
      got:  appendonly_violations=1 ids=[S136] deleted=[] superseded=[] round_changed=[S005,S136,S158]
  repo19 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S134] superseded=[] round_changed=[S134,S169]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[S134,S169]
  repo20 FAIL: lists differ
      want: appendonly_violations=4 ids=[S106] deleted=[S184,S212,S233] superseded=[S106] round_changed=[S184]
      got:  appendonly_violations=1 ids=[S106] deleted=[] superseded=[S106] round_changed=[S184]
  repo21 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S239] superseded=[] round_changed=[S181]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[S181]
  repo22 FAIL: lists differ
      want: appendonly_violations=2 ids=[S012] deleted=[S043] superseded=[S012] round_changed=[]
      got:  appendonly_violations=1 ids=[S012] deleted=[] superseded=[S012] round_changed=[]
  repo23 FAIL: lists differ
      want: appendonly_violations=2 ids=[] deleted=[S024,S181] superseded=[] round_changed=[S024,S134]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[S024,S134]
real arm: pass (0.3s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
C2=unmet
seed=11
COUNTER_EXIT=1
```
Every one of the 24 histories carries a deletion (`deletions=24`), and every failure is the missing `deleted` list;
`round_changed` matched truth in **all** 24 (e.g. repo03: want `round_changed=[S017,S162]`, got the same) — the kill
rests on the deleted list alone, not on the weakened round-changed arm.

### Stage 3 — restored (mutant file rewritten with the pristine bytes, sha `915527a7…`), exit code 0

```
tool: /tmp/mutc2/mutant.py      (# sha256 915527a7d2f553740ed3ab0166669031f19ce2de6b2fec8501208f97244cfc89)
blind arm: 24/24 sandbox histories matched the hidden truth (2.1s; coverage: deletions=24 changed-back=16 superseded=12)
real arm: pass (0.7s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
C2=met
seed=11
COUNTER_EXIT=0
```
The three stages drew the identical 24 histories (same seed, same coverage line) and differ only in the tool bytes.

## Mutation verdict: killed

| stage | tool sha256 | blind | real | C2 | exit |
|---|---|---|---|---|---|
| pristine | `915527a7…` | 24/24 | pass | met | 0 |
| mutant | `e71495b8…` | **0/24** | pass | **unmet** | **1** |
| restored | `915527a7…` | 24/24 | pass | met | 0 |

## Selftest of the mutant

The tool's `--selftest` has a hand-written deletion fixture (`tools/mori-sources-appendonly.py:372`,
`("deleted row", [two_rows, one_row], 1, {... "deleted": ["S002"] ...})`), so it is expected to catch this mutation —
this is therefore **not** the "selftest passes while the counter fails" case.

```
$ cd /tmp/mutc2 && TMPDIR=/tmp/mutc2 python3 pristine.py --selftest
MORI_SOURCES_APPENDONLY_SELFTEST pass=8 fail=0          # exit 0
$ TMPDIR=/tmp/mutc2 python3 mutant2.py --selftest        # sha 915527a7… mutated to e71495b8…
FAIL deleted row: deleted: want ['S002'] got []
MORI_SOURCES_APPENDONLY_SELFTEST pass=7 fail=1           # exit 1
```
Receipts: `/fast/scratch/hyaku/mori-r36/MutC2Deleted/selftest-pristine.txt`, `selftest-mutant2.txt`,
`/fast/scratch/hyaku/mori-r36/MutC2Deleted/mutant-e71495b8.py` (the exact mutant; selftest exit 1).
Note: my first selftest invocation was mislabelled — it ran a copy the restore step had already overwritten with
pristine bytes and printed `pass=8`; the valid mutant selftest above was re-run from a freshly re-mutated copy with
sha `e71495b8…`, the same bytes the counter killed. The invalid run is not cited as a receipt.

## Restoration evidence

```
$ cp /tmp/mutc2/pristine.py /fast/scratch/hyaku/mori-r36/MutC2Deleted/mutant.py
$ sha256sum /fast/scratch/hyaku/mori-r36/MutC2Deleted/pristine.py /fast/scratch/hyaku/mori-r36/MutC2Deleted/mutant.py /tmp/mutc2/mutant.py /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-sources-appendonly.py
915527a7d2f553740ed3ab0166669031f19ce2de6b2fec8501208f97244cfc89  /fast/scratch/hyaku/mori-r36/MutC2Deleted/pristine.py
915527a7d2f553740ed3ab0166669031f19ce2de6b2fec8501208f97244cfc89  /fast/scratch/hyaku/mori-r36/MutC2Deleted/mutant.py
915527a7d2f553740ed3ab0166669031f19ce2de6b2fec8501208f97244cfc89  /tmp/mutc2/mutant.py
915527a7d2f553740ed3ab0166669031f19ce2de6b2fec8501208f97244cfc89  /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-sources-appendonly.py
$ git diff --no-index --stat /fast/scratch/hyaku/mori-r36/MutC2Deleted/{pristine,mutant}.py ; echo diff_exit=$?
diff_exit=0
```
No lane file was written, staged or mutated; the lane tool's sha is unchanged from the pre-probe value.

## Findings and observations (detection only, no remediation)

1. **Kill is real and narrow.** The frozen counter rejects the deleted-arm removal 0/24 while the same histories pass
   the pristine and restored bytes. This is direct evidence for the C2 deleted arm being load-bearing and detected
   (`count-c2.py:498-516`, `same_lists` `:517-522`, `blind_arm` `:590-621`; truth from the op log, `truth_from_states`, independent of the tool).
2. **The real arm cannot see this defect.** The lane history has `deleted=[]` at `6bd57097` (all three stages print
   it), so the mutant's real arm passes. The blind arm's forced deletions are the *only* witness for the deleted arm —
   consistent with w1/CritAxisFit.md's note that the deletion arm is non-vacuous only because of the sandbox histories.
   A future predicate whose blind histories stop forcing deletions would silently lose this coverage; the guard is
   `count-c2.py:703` (`coverage["delete"] < 12` → setup error, exit 2), which fired nothing here
   (deletions=24 ≥ 12).
3. **Unprobed coverage limit, adjacent to this arm.** The counter reads only the summary line
   (`parse_summary`, `count-c2.py:498-516`) and compares only that (`same_lists`, `:517-522`; call sites `:602-618`,
   `real_arm` `:624-641`). The contract's C2 output spec also requires a per-id `deleted <id>` line
   (`contract.md`, "C2 tool interface"; tool `:280`). A program printing a correct summary but omitting the `deleted
   <id>` lines would pass `count-c2.py`; only the tool's own selftest checks those lines. I did not run that mutant
   (one assigned probe); recorded as a coverage limit of the frozen counter, not a defect of the claim's numbers.
4. **Harness note — seed-derived scratch collides across concurrent seats.** `count-c2.py:689` builds the sandbox
   root as `SCRATCH_ROOT/c2-<first 32 bits of rng(seed)>`, so two concurrent runs with `--seed 11` share
   `/fast/scratch/hyaku/mori-r36/c2-7734d7c1`. Observed first-hand when I ran pristine and mutant in parallel:
   ```
   counter setup error: git config user.name mori counter failed in /fast/scratch/hyaku/mori-r36/c2-7734d7c1/repo00: fatal: not in a git directory
   counter setup error: [Errno 17] File exists: '/fast/scratch/hyaku/mori-r36/c2-7734d7c1/repo00/corpus'
   ```
   both exit 2 — i.e. a collision yields "could not evaluate", never a verdict, so it cannot counterfeit a pass or a
   kill. My three scored stages were run one at a time inside `unshare -rm` with a private tmpfs mounted at
   `SCRATCH_ROOT`; counter bytes and tool bytes were unchanged (verified above), only the shared scratch root was
   isolated. Seats replaying seed 11 concurrently should expect exit 2, not an unmet score.
5. Tooling: no install or upgrade was performed for this probe.

VERDICT: PASS — the frozen counter `count-c2.py` (sha `c7edaac…`) kills the deleted-row-arm removal
(`tools/mori-sources-appendonly.py:242` in the copy, sha `e71495b8…`): blind 0/24, `C2=unmet`, exit 1; pristine and
restored bytes (`915527a7…`) score `C2=met`, exit 0; no defect found in the C2 deleted arm or its detector.
