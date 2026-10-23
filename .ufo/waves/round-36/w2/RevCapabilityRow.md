# RevCapabilityRow — SCORECARD capability-row consistency (pre-landing)

Item attacked: the pending C2 capability row for the SOURCES append-only gate
(`tools/mori-sources-appendonly.py`), which the integration commit will add to
the SCORECARD capabilities register, keyed to round 36. Scope: receipts exist,
evidence pointer resolves at the tip, no pre-claim of unrun capabilities; the
existing 18 register rows' pointers still resolve at
bf0df77fee4b6ef54a90aea09335c7617f125151.

All commands ran from the lane repo
`/home/vgpnk/Projects/shokunin/mori-shokunin` (read-only). No lane file was
edited by this seat; the only file written is this report. No tools installed.

## 1. Existing register rows and pointer resolution at tip bf0df77

Register table (tip SCORECARD.md): intro `SCORECARD.md:1941-1957`
(row-entry rule: only rounds that demonstrate the capability running, keyed to
fleet MANIFEST `capabilities_added` records), table `SCORECARD.md:1959-1978`.

```
$ git show bf0df77:SCORECARD.md | grep -cE '^\| `rounds\['
18
```

Exactly 18 rows (`rounds[313]`, `[339]`, `[345]`, `[353]`, `[386]`x3,
`[398]`, `[427]`, `[443]`x2, `[455]`x2, `[462]`, `[476]`x2, `[495]`x2),
matching the round-35 C1 count `matched=18`.

Each evidence cell resolved at bf0df77:

```
$ for p in 'corpus/SOURCES.md' 'tools/mori-round14-regressions.py' \
  'tools/mori-round15-regressions.py' 'tools/mori-journal-window.py' \
  'tools/mori-retention-gate.py' 'tools/mori-freeze-order.py' \
  'tools/mori-dispatch-ledger.py' 'tools/mori-content-review.py' \
  'tools/mori-retention-reconcile.py' 'tools/mori-pressure.py' \
  'tools/mori-routed-check.py' 'tools/mori-job-runway.py' \
  'tools/mori-routed-r24.py' 'tools/mori-oom-killers.py' \
  'corpus/SOURCES.md' 'corpus/knowledge/oom-victim-selection-r27.md' \
  'tools/fixtures/mori-oom-killers/cases-a2.json' \
  'tools/mori-blind-check.sh' 'corpus/knowledge/watchdog-identity-r31.md'; do
    git cat-file -e "bf0df77:$p" && echo "OK  $p" || echo "MISS $p"; done
OK  corpus/SOURCES.md
OK  tools/mori-round14-regressions.py
OK  tools/mori-round15-regressions.py
OK  tools/mori-journal-window.py
OK  tools/mori-retention-gate.py
OK  tools/mori-freeze-order.py
OK  tools/mori-dispatch-ledger.py
OK  tools/mori-content-review.py
OK  tools/mori-retention-reconcile.py
OK  tools/mori-pressure.py
OK  tools/mori-routed-check.py
OK  tools/mori-job-runway.py
OK  tools/mori-routed-r24.py
OK  tools/mori-oom-killers.py
OK  corpus/SOURCES.md
OK  corpus/knowledge/oom-victim-selection-r27.md
OK  tools/fixtures/mori-oom-killers/cases-a2.json
OK  tools/mori-blind-check.sh
OK  corpus/knowledge/watchdog-identity-r31.md
```

No dangling pointer among the existing 18 rows. SCORECARD.md has no
uncommitted edits (`git diff bf0df77 -- SCORECARD.md` = 0 lines).

## 2. C2 demonstrated running in this round

- Tool exists at tip:
  `git cat-file -e bf0df77:tools/mori-sources-appendonly.py` -> OK.
- Before receipt COMMITTED at tip (`evidence/c2-before.txt`, present in
  `git ls-tree bf0df77:.ufo/waves/round-36/evidence/`): P-C2 sentence,
  `tool_absent`, `C2=unmet`, seed 3261301256787951392, `EXIT=1` — acquisition
  vs entering tip 6bd57097.
- After receipt (`evidence/c2-after.txt`): first line byte-identical to the
  frozen P-C2 sentence (contract.md:23 at tip):
  `cmp <(awk '/^P-C2:/{print;exit}' <(git show bf0df77:.ufo/waves/round-36/contract.md)) <(head -1 .ufo/waves/round-36/evidence/c2-after.txt)` -> `PC2_BYTE_IDENTICAL`.
- Counter sha256 at tip = freeze pin:
  `git show bf0df77:.ufo/waves/round-36/count-c2.py | sha256sum` ->
  `c7edaacfff029c2055bee6ddda42ff6f5c040dad7fbac81e9d169602edcbac34` =
  `evidence/freeze-v2.txt` line for count-c2.py.
- Receipt scores: blind 24/24 (deletions=22 changed-back=17 superseded=10),
  real arm pass, tool==oracle (`ids=[S041,...]` 18 ids, superseded 3,
  round_changed 2, exit=1), `C2=met`, seed 15440749816798970567. The tool
  path in the receipt (`/tmp/mori-c2-pdznuaps/mori-sources-appendonly.py`) is
  the counter's temp extraction of `git show <rev>:tools/<tool>` — the
  committed tool bytes were run.

## 3. Pending row evidence pointer resolution at the tip — DEFECT

The planned row's evidence pointer will be the receipt path under
`.ufo/waves/round-36/evidence/`. At the landed data tip bf0df77 that file is
absent:

```
$ git cat-file -e bf0df77:.ufo/waves/round-36/evidence/c2-after.txt
fatal: path '.ufo/waves/round-36/evidence/c2-after.txt' exists on disk, but not in 'bf0df77'
exit=128
```

```
$ git ls-tree --name-only bf0df77:.ufo/waves/round-36/evidence/
c0-rescore-v2.txt
c1-before.txt
c2-before.txt
census-start.txt
freeze-v2.txt
freeze.txt
refs
```

No `c2-after.txt`, `c1-after.txt`, or `drift-live-r36.txt` in the committed
tree. Working-tree state:

```
$ git status --porcelain
?? .ufo/waves/round-36/evidence/c1-after.txt
?? .ufo/waves/round-36/evidence/c2-after.txt
?? .ufo/waves/round-36/evidence/drift-live-r36.txt
... (plus ?? .scratch/, __pycache__/, w2-* spec files, w2/)
```

The jj view confirms: the after-receipts live in the uncommitted working copy
(draft cd79cd52, parent = bf0df77 master), not in any commit:

```
$ jj status
Working copy (@): xozttkkx cd79cd52 (no description set)
Parent commit (@-): plkxpspm bf0df77f master | round-36: C1/C2 data ...
Untracked paths: ... evidence/c1-after.txt, evidence/c2-after.txt, evidence/drift-live-r36.txt
```

Consequence: a capability row added against bf0df77 that references
`.ufo/waves/round-36/evidence/c2-after.txt` is a **dangling pointer at every
committed revision** until the integration commit also commits the receipt.
Nothing in the committed bytes binds the receipt to the tip. This is exactly
the failure mode this seat is asked to catch.

## 4. No pre-claim of unrun capabilities

```
$ git show bf0df77:SCORECARD.md | grep -nE 'appendonly|append-only|round-36|r36'
1845:- **C1 tip-receipt correction (append-only; the historical row above is retained):** ...
```

The only `append-only` mention in SCORECARD.md at tip is round-30 prose
(unchanged historical record). There is no round-36 capability row anywhere:
the register ends at `rounds[495]` (round 31). No drafted row text exists in
the wave-2 spec or any committed file. Nothing currently over-claims the
append-only gate.

## Findings

- **F1 (HIGH, FAIL — pending-row pointer dangles at tip).** The C2
  after-receipt `evidence/c2-after.txt` is not committed; bf0df77's tree does
  not contain it (nor c1-after.txt, drift-live-r36.txt). The integration
  commit must include these untracked receipts alongside the capability row,
  or the row's evidence pointer will not resolve at the tip.
- **F2 (LOW, same class).** Identical uncommitted state for
  `evidence/c1-after.txt` and `evidence/drift-live-r36.txt`; any artifact
  pointing at them also dangles until committed.
- Note (out of seat scope, for RevFreezeIntegrity): contract.md at tip hashes
  to `065a17b5...`, not the freeze-v2.txt pin `dbd3f6d7...` (the declaration
  commit 5842dc0 amended the contract after the v2 freeze; P-C1/P-C2
  sentences at tip are unchanged). Does not affect receipt validity: the C2
  receipt sentence is byte-identical to the frozen P-C2.

## Residual risk / verification gaps

- The final row text is not drafted in any committed file; I verified the
  current bytes only, as instructed.
- Fleet MANIFEST.json intentionally not read (hard bound); alignment of the
  future row key with the closure's `capabilities_added` record is not
  independently checkable here.

## VERDICT: FAIL

Defect found: the pending C2 capability row's evidence pointer is dangling at
the landed data tip bf0df77 because `evidence/c2-after.txt` (and
`evidence/c1-after.txt`, `evidence/drift-live-r36.txt`) are uncommitted
working-tree files, absent from `bf0df77`'s tree. The existing 18 register
rows' pointers all resolve at bf0df77 (verified individually, `git cat-file
-e`, no dangling among them); the receipt content, predicate byte-identity,
frozen counter hash, and acquisition (before: `C2=unmet`, tool_absent) are
all valid. Fix direction: the integration commit must commit
`.ufo/waves/round-36/evidence/c2-after.txt` (and the related untracked
receipts if referenced) together with the row.
