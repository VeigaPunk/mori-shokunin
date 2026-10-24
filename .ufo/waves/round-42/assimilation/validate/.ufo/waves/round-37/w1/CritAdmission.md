# CritAdmission — SCORECARD preservation and causal separability

Attacks: a hidden score rewrite, replacement of existing register rows, or an apparent two-claim advance that requires both round-37 artifact sets together. This is the assigned admission-bar review, not a canonical closure judgment.

Axes: coverage **6**, operability **7**, depth **5**, freshness **5**, calibration **5**, adjacency **6**. No score change or scoped axis harm found. C1 targets calibration; C2 targets freshness.

## SCORECARD diff

Command (exit 0):

```sh
git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff 842a320..e57c58b5 -- SCORECARD.md
```

Observed complete diff: one append-only hunk, 26 additions, zero deletions. The existing six-axis table and every pre-existing row are preserved.

```diff
diff --git a/SCORECARD.md b/SCORECARD.md
index 43448e9..e70ef72 100644
--- a/SCORECARD.md
+++ b/SCORECARD.md
@@ -2031,3 +2031,29 @@ counter that fails content-free controls.
 Held: coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6. No axis score moves this
 round; C2 moves the operability surface (new registered gate + capability), C1 moves coverage/technique ground
 (README Round-36 rows). No retirement.
+
+## Round 37 declaration (attempt 1, L1 MoriR37) — measurement discrimination (calibration) and the drift probe's hardening (freshness)
+
+Entering tip `842a32074b5c7972e9728f3f629d83eb92f127c2` (round 36 admitted; MANIFEST closure `rounds[54x]`,
+`corpus/lessons/round-36-verifier-spotcheck.md`). Contract and both counters are frozen before any data:
+`.ufo/waves/round-37/contract.md` (P-C1, P-C2, kill rules) with `count-c1.py` and `count-c2.py` pinned by git
+blob hash in `evidence/freeze-r37.txt`. The declared cells below copy the frozen contract; targets, not results.
+
+| Claim | Axis / score | Before (one command over committed bytes) | Declared after-value (one command over committed bytes) |
+|---|---|---|---|
+| C1 the C2 measurement discriminates a real-arm memoizer and enforces the per-id grammar: an extended counter with a run-time-drawn challenge arm in real-arm clothing and `deleted <id>` line parsing (r36 w2/RevNgC2 N1 class; w2/MutC2Deleted limit 3) | calibration 5 (tied lowest with depth and freshness) | `python3 .ufo/waves/round-36/count-c2.py bf0df77 --tool .ufo/waves/round-37/fixtures/memo-n1.py --seed 11` → `C2=met`, exit 0 (a tool that never computes the real-arm answer passes; `evidence/c1-before-memo.txt`); same counter with `fixtures/summary-only.py` → `C2=met`, exit 0 (`evidence/c1-before-summary.txt`) | `python3 .ufo/waves/round-37/count-c1.py <landed tip>` → blind 24/24, real pass, challenge pass, `negative memo-n1.py rejected`, `negative const.py rejected`, `negative summary-only.py rejected`, `C1=met`, exit 0 (`evidence/c1-after.txt`) |
+| C2 the drift probe's two fetch policies are named, mutation-killable and corpus-bound (r36 w2/SentCensus hardening at `8ff9bba`) | freshness 5 (tied lowest) | `python3 .ufo/waves/round-37/count-c2.py 842a320` → `selftest FAIL` (4 unnamed arms), `knowledge FAIL`, `capability FAIL`, `readme FAIL`, `live FAIL`, `C2=unmet`, exit 1 (`evidence/c2-before.txt`) | the same command at the landed tip → all checks PASS, `C2=met`, exit 0 (`evidence/c2-after.txt`) |
+
+Held and observed: coverage 6, operability 7, depth 5, calibration 5, freshness 5, adjacency 6. No retirement,
+waiver, exploratory claim or promotion. Controls: the before receipts are the r36 counter's own pass on the two
+negative fixtures (a do-nothing control cannot produce `C1=met`); the after counter must both accept the honest
+tool and reject all three fixtures, so a counter that only documents cannot meet it. Anti-loop: rounds 35
+(register binding) and 36 (C2 gate acquisition, drift technique) are not repeated; C1 is the measurement
+discrimination the r36 closure routed, C2 the hardening verification it left open.
+
+Capabilities register — rows demonstrated running this round (closure admits them; evidence is the receipts):
+
+| key | name | what it can now do | evidence | first working |
+|---|---|---|---|---|
+| round-37 C1 | real-arm challenge counter | Extends the C2 gate measurement with a run-time-drawn challenge history in real-arm clothing and per-id `deleted` line parsing, so a real-arm memoizer and a summary-only printer are both rejected while the honest gate passes | `.ufo/waves/round-37/count-c1.py`; `evidence/c1-after.txt`; fixtures under `.ufo/waves/round-37/fixtures/` | 37 |
+| round-37 C2 | source-drift re-fetch probe | Re-fetches every registry row with a committed copy and classifies the copy against today's body under a 4 MiB bounded read and a post-redirect public-destination policy; `--selftest` 6 cases with two named, mutation-killable arms | `tools/mori-source-drift.py`; `.ufo/waves/round-37/evidence/c2-after.txt`; `evidence/drift-live-r37.txt` | 37 |
```

Scored path evidence: `SCORECARD.md:10-15` retains the axes; `:2044-2045` adds the two declared claims; `:2047` repeats held scores; `:2058-2059` adds two distinct capability keys. No old row is removed, rewritten, or renamed. The review uses the scored commit, not later working-tree edits.

## Counterexample experiment: remove the other claim

Reproducer retained solely in this seat's permitted scratch:
`/fast/scratch/hyaku/mori-r37/CritAdmission/admission-separate.py`.

It creates two synthetic commits parented directly on entering tip `842a32074b5c7972e9728f3f629d83eb92f127c2`, taking selected blobs from scored tip `e57c58b57c025364e79d130fbdf764d2674d83d6`. No lane Git metadata or source was modified. Both counters are byte-identical to the frozen scored versions.

- **C1 only:** entering tree plus `count-c1.py` and its three fixtures. The drift tool, README, SOURCES and SCORECARD remain entering bytes; the C2 counter, new knowledge, new source copies and live receipt are absent.
- **C2 only:** entering tree plus `count-c2.py`, the drift-tool change, its corpus changes/source copies/live receipt, and only the C2 capability row appended to the entering SCORECARD. The C1 counter, all three fixtures and C1 register row are absent.
- Both trees omit the joint round-37 contract/freeze files and unrelated round-17 debt fix. The original baseline Git history remains available read-only for C1's specified real arm.

Commands run in Bubblewrap: host root read-only, the scratch repository mounted at the lane's exact pathname, separate scratch-backed `/tmp` and counter scratch root, and original Git objects read-only. Thus the pinned C1 counter keeps its original absolute-path challenge and fixture behavior without writing the actual lane. No counter/fixture source or predicate was patched.

Preparation command (exit 0):

```sh
python3 -B /fast/scratch/hyaku/mori-r37/CritAdmission/admission-separate.py prepare
```

Observed output:

```text
axis_tables_identical=True
scorecard_prefix_preserved=True
scorecard_added_lines=26
axis coverage=6
axis operability=7
axis depth=5
axis freshness=5
axis calibration=5
axis adjacency=6
gate_blob_base=dfb5040b159f7a0b4afedc90a633d997352908f0
gate_blob_tip=dfb5040b159f7a0b4afedc90a633d997352908f0
c1_revision=e5fcbeed91c23bc90c269c98af1cff4d8ad0cab5
c1_tree_changes=['.ufo/waves/round-37/count-c1.py', '.ufo/waves/round-37/fixtures/const.py', '.ufo/waves/round-37/fixtures/memo-n1.py', '.ufo/waves/round-37/fixtures/summary-only.py']
c1 C2-path .ufo/waves/round-37/count-c2.py absent=True
c1 C2-path .ufo/waves/round-37/evidence/drift-live-r37.txt absent=True
c1 C2-path tools/mori-source-drift.py baseline_bytes=True
c1 C2-path corpus/README.md baseline_bytes=True
c1 C2-path corpus/SOURCES.md baseline_bytes=True
c1 C2-path corpus/knowledge/source-drift-hardening-r37.md absent=True
c1 C2-path corpus/evidence/sources-r37/S221.src absent=True
c1 C2-path corpus/evidence/sources-r37/S222.src absent=True
c1 C2-path corpus/evidence/sources-r37/S223.src absent=True
c1 C2-path corpus/evidence/sources-r37/S224.src absent=True
c1_shared_contract_and_freeze_absent=True
c1_counter_blob=7518fef8f54afff69ee38a99f2acbf518006f5ad pinned_equal=True
c2_revision=1a386e4537c75899b19b3ee45cd3da2ee3b83940
c2_tree_changes=['.ufo/waves/round-37/count-c2.py', '.ufo/waves/round-37/evidence/drift-live-r37.txt', 'SCORECARD.md', 'corpus/README.md', 'corpus/SOURCES.md', 'corpus/evidence/sources-r37/S221.src', 'corpus/evidence/sources-r37/S222.src', 'corpus/evidence/sources-r37/S223.src', 'corpus/evidence/sources-r37/S224.src', 'corpus/knowledge/source-drift-hardening-r37.md', 'tools/mori-source-drift.py']
c2 C1-path .ufo/waves/round-37/count-c1.py absent=True
c2 C1-path .ufo/waves/round-37/fixtures/memo-n1.py absent=True
c2 C1-path .ufo/waves/round-37/fixtures/const.py absent=True
c2 C1-path .ufo/waves/round-37/fixtures/summary-only.py absent=True
c2 scorecard_C1_row_absent=True
c2_shared_contract_and_freeze_absent=True
c2_counter_blob=6213cf9a5ada709da8cd867581782737b2f06c71 pinned_equal=True
```

### C1 without C2 changes

Command (exit 0):

```sh
python3 -B /fast/scratch/hyaku/mori-r37/CritAdmission/admission-separate.py c1
```

The command runs this exact pinned counter invocation inside the namespace:

```sh
python3 -B .ufo/waves/round-37/count-c1.py e5fcbeed91c23bc90c269c98af1cff4d8ad0cab5 --repo /home/vgpnk/Projects/shokunin/mori-shokunin --seed 41
```

Observed output excerpts:

```text
blind arm: 24/24 sandbox histories matched the hidden truth (2.1s; coverage: deletions=21 changed-back=14 superseded=12)
real arm: pass (0.3s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
challenge arm (real-arm clothing): pass (0.1s)
  truth:  appendonly_violations=4 ids=[S054,S116,S236] deleted=[S081] superseded=[S054] round_changed=[S081,S116,S236]
  tool:   appendonly_violations=4 ids=[S054,S116,S236] deleted=[S081] superseded=[S054] round_changed=[S081,S116,S236]
negative memo-n1.py     rejected (challenge: lists differ: want appendonly_violations=3 ids=[S179] deleted=[S066,S116] superseded=[S179] round_changed=[S066,S116] got appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193])
negative const.py       rejected (blind 4/4 (repo200: lists differ))
negative summary-only.py rejected (blind 4/4 (repo200: per-id lines differ (malformed=0)))
C1=met
seed=41
counter_exit=0
```

### C2 without C1 changes

Command (exit 0), launched concurrently with the C1 command:

```sh
python3 -B /fast/scratch/hyaku/mori-r37/CritAdmission/admission-separate.py c2
```

Exact pinned counter invocation inside its separate namespace:

```sh
python3 -B .ufo/waves/round-37/count-c2.py 1a386e4537c75899b19b3ee45cd3da2ee3b83940 --repo /home/vgpnk/Projects/shokunin/mori-shokunin
```

Observed output excerpts:

```text
check tool_present   PASS (path=tools/mori-source-drift.py)
check selftest       PASS (exit=0 arms=[('exit_code', 'PASS'), ('huge_cap', 'PASS'), ('missing_sources_exit2', 'PASS'), ('redirect_private_refused', 'PASS'), ('row_states', 'PASS'), ('summary', 'PASS')])
check cap_kill       PASS (exit=1 huge_cap=FAIL)
check redirect_kill  PASS (exit=1 redirect_private_refused=FAIL)
check knowledge      PASS (present=True rows=['S205', 'S221', 'S222', 'S223', 'S224', 'S225'] cited_commit=True)
check capability     PASS (rows=1 names_tool=True)
check readme         PASS (r36_row=True r37_row=True)
check live           PASS (present=True sentence=True)
C2=met
counter_exit=0
```

Initial asynchronous launch requests for these same two commands were refused with `Background job limit reached (100)`; the observed executions above used concurrent synchronous calls. No results were inferred from the refused requests.

## Separability argument and disposition

The strongest scoped counterexample did not materialize: **both pinned counters meet their predicates on entering-tip-based trees lacking the other claim's round-37 changes.**

C1 depends on the unchanged append-only gate, its own fixtures, generated histories and historical SOURCES walk (`count-c1.py:855-888,895-949`). It never needs C2's drift-tool additions, corpus binding or receipt. Its original absolute fixture dependency resolves to the baseline gate in the isolated lane, not the live working tree.

C2 reads only its drift probe, knowledge entry, capability row, README coverage rows and live receipt from its target revision (`count-c2.py:151-211`). Its C2 capability row suffices without C1's row; no C1 counter or fixture is required. The common entering history is a shared prerequisite, not a new cross-claim dependency.

Impacted axes: calibration and freshness are independently measurable here; coverage, operability, depth and adjacency retain their prior score/evidence table unchanged. This review finds no defect in the requested preservation/separability bar and does not substitute for other seats' semantic or axis-fit reviews.

Smallest safe correction: none required for this scoped bar. Tools installed or updated: none.

Report: .ufo/waves/round-37/w1/CritAdmission.md
VERDICT: PASS
