measured 2026-10-23T09:14:18Z
# CtlOffTopic — post-data what-cell derangement

Axes: semantic discrimination, reproducibility, lane isolation.

VERDICT: survived — the off-topic what-cell derangement received C1=met, exit 0.
VERDICT: fails — P-C1 alone discriminates this shape.

## Mutant and expected detector

Attack: keep the final register's keys, capability names, evidence and rounds unchanged, but replace each what-cell with the next row's original what-cell, wrapping row 18 to row 1. This is one cyclic derangement, not eighteen independently tuned probes. Source: `SCORECARD.md@cedb0ec4f3a4f672804deac388b7191258f01fcd:1959-1978` in the clone below.

A detector that discriminated this shape would accept pristine/restored registers and reject the reassociated register (C1=unmet, exit 1). Actual frozen P-C1 accepted all three; receipts below.

Clone: `/fast/scratch/hyaku/mori-r35/CtlOffTopic/clone`.
Base: `cedb0ec4f3a4f672804deac388b7191258f01fcd`.
Mutant clone commit: `c71c73112c51668972580c4e5031f956eeaf43d9`.
Restoration clone commit: `17d53eb8a044a993874a276b77c56dda8c62c85b`.
These revisions are scratch-clone commits, not lane commits.

Creation command (exit 0):
```text
timeout 120 prlimit --as=2147483648 --cpu=110 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -c core.hooksPath=/dev/null clone --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/mori-shokunin /fast/scratch/hyaku/mori-r35/CtlOffTopic/clone
```
Then a bounded clone checkout selected the base; output: `HEAD is now at cedb0ec` (exit 0).

The in-memory byte comparison constructed the expected file by replacing only the raw third cell of each of these 18 rows with its successor's cell. Comparison with the edited file succeeded; actual output:
```text
Mutation checks: rows=18 changed_what_cells=18 fixed_points=0; every other byte unchanged
mutant_scorecard_sha256: 0324cf99a9ac8650e534809be22b545bd052e1f2e8623f79b815380276781157
commit exit: 0
[detached HEAD c71c731] Control: cyclic derangement of final capability what cells
 1 file changed, 18 insertions(+), 18 deletions(-)
mutant_commit: c71c73112c51668972580c4e5031f956eeaf43d9
```

## Control register bytes inline (20 lines)

`git -C /fast/scratch/hyaku/mori-r35/CtlOffTopic/clone show c71c73112c51668972580c4e5031f956eeaf43d9:SCORECARD.md` retains this table at lines 1959–1978:
```text
| key | capability | what it can now do | evidence | first-working round |
|---|---|---|---|---|
| `rounds[313].capabilities_added[0]` | source registry | Classifies structured failed-unit subjects as fleet, tsukuroi-routed or unresolved and raises one critical OOM journal alarm; the six named fixture failures went 6 to 0; no live-positive or exhaustive coverage proof. | `corpus/SOURCES.md` | 12 |
| `rounds[339].capabilities_added[0]` | typed journal alarm and subject triage | On finite committed fixtures, keeps individually qualified current-boot OOM and user-signal alarms beside invalid aggregate records, whose raw totals stay unavailable; no live positive load is claimed. | `tools/mori-round14-regressions.py` | 14 |
| `rounds[345].capabilities_added[0]` | partial positive journal alarms | Reads one user or system journal scope after a byte-equal retained anchor cursor on the anchor's boot, MESSAGE-free, refusing unsafe captures as unavailable without advancing cursor state; 64/64 fixtures; live runs were anchor-only. | `tools/mori-round15-regressions.py` | 15 |
| `rounds[353].capabilities_added[0]` | exact-start journal record window | Scans lane revisions under the retention policy and reports metric and routed counts; selftest 21/21; after-metric 0 and routed 0 at 3127c3a. | `tools/mori-journal-window.py` | 16 |
| `rounds[386].capabilities_added[0]` | retention gate | Checks frozen claim inputs against implementation history and counts overclaims; selftest 12/12; overclaims 4 to 0 at 3127c3a. | `tools/mori-retention-gate.py` | 18 |
| `rounds[386].capabilities_added[1]` | freeze-order check | Verifies that dispatch attempts bind their payloads: round-18 wave 1 1/1 and wave 2 2/2 bound clean, residual 7/7 bound with STARTED_MISSING; selftest 14/14. | `tools/mori-freeze-order.py` | 18 |
| `rounds[386].capabilities_added[2]` | dispatch-attempt ledger verify | Passes 10/10 frozen finite requirements; on the actual 194-path population it exits 1 with 155 unresolved dispositions, so it is not privacy clearance. | `tools/mori-dispatch-ledger.py` | 18 |
| `rounds[398].capabilities_added[0]` | blob-bound content-review coverage gate | Independently recounts the measured tree of a committed retention receipt and reports identity agreement and policy exclusions; accounting agreement only, privacy clearance always false. | `tools/mori-content-review.py` | 19 |
| `rounds[427].capabilities_added[0]` | retention receipt reconciliation | Reads /proc/pressure cpu, memory, io and irq once per resource; unavailable is never zero, system cpu full is flagged undefined and irq some is null; frozen selftest PASS 12/12, six wave-2 survivors disclosed. | `tools/mori-retention-reconcile.py` | 22 |
| `rounds[443].capabilities_added[0]` | one-shot system pressure read | Checks the R1-R3 regression pins and R4 dispatch-before-call ordering over lane-written times; held 3 to 4; round-23 wave-1 timing mismatches 8, round-24 0 of 2. | `tools/mori-pressure.py` | 24 |
| `rounds[443].capabilities_added[1]` | round-23 routed-item check | Reads the configured async.maxJobs from one settings file plus the binary clamp and default, and reports the effective cap and a verdict (not a live job count); frozen selftest PASS 21/21; bounded to block-style configs. | `tools/mori-routed-check.py` | 24 |
| `rounds[455].capabilities_added[0]` | harness background-job runway read | Checks round-24 defects D1-D3 and D5 from git objects plus D4 hygiene; 4 to 0, re-measured by the closure with plain git reads; no registry row or selftest. | `tools/mori-job-runway.py` | 25 |
| `rounds[455].capabilities_added[1]` | round-24 routed-defect and Axes-table check | Reads earlyoom and systemd-oomd unit state, earlyoom startup thresholds, counts of earlyoom send, escalation, failed-kill and low-memory lines this invocation and oomd kill notices this boot; KILLER_ACTED, KILLERS_UNKNOWN or KILLERS_QUIET; counts are log lines, not processes. | `tools/mori-routed-r24.py` | 25 |
| `rounds[462].capabilities_added[0]` | userspace OOM killer one-shot read | Superseded eight carried SOURCES row defects with re-opened rows S145-S152, restored S096, S097 and S101 to their first-published cells, and repointed the live readers. | `tools/mori-oom-killers.py` | 26 |
| `rounds[476].capabilities_added[0]` | SOURCES freshness repair | Pins ten round-26 amendment-A2 rules of the OOM killer read with 30 frozen cases (freeze d21b8bd3), PASS 30/30; fixture-only, not a live-host result. | `corpus/SOURCES.md`, `corpus/knowledge/oom-victim-selection-r27.md` | 28 |
| `rounds[476].capabilities_added[1]` | amendment-A2 frozen cases | Blind-writer gate with a passing --selftest; on the round-30 inputs it reports three missing-list hits and no longer flags CaseR30a.md:105; supersedes the round-30 wave gate (routed D1). | `tools/fixtures/mori-oom-killers/cases-a2.json` | 28 |
| `rounds[495].capabilities_added[0]` | blind-writer gate | A sourced FR5 table (S161-S174) on what pid probes can and cannot establish about watchdog liveness; measurements used throwaway processes and did not change the census probe. | `tools/mori-blind-check.sh` | 31 |
| `rounds[495].capabilities_added[1]` | watchdog identity decision table | Curates where mori learns: opened, tiered, anchored source rows with a search log; 34 rows with a clean contract-v1 census at the round-12 closure (the registry has grown since). | `corpus/knowledge/watchdog-identity-r31.md` | 31 |
```

## Same bounded frozen detector, three states

Counter actually run: `/fast/scratch/hyaku/mori-r35/CtlOffTopic/clone/.ufo/waves/round-35/count-c1.py`.
SHA-256 checked before the baseline and after both subsequent runs: `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167`.
Each invocation used the same argv below, substituting only REV. Git environment overrides were removed; bytecode writes were disabled. Each returned with empty stderr.
```text
timeout 300 prlimit --as=1073741824 --cpu=240 -- python3 -B /fast/scratch/hyaku/mori-r35/CtlOffTopic/clone/.ufo/waves/round-35/count-c1.py REV --repo /fast/scratch/hyaku/mori-r35/CtlOffTopic/clone
```
Pristine REV=`cedb0ec4f3a4f672804deac388b7191258f01fcd`; actual full summary; exit 0, verdict met:
```text
label=P-C1 rev=cedb0ec4f3a4f672804deac388b7191258f01fcd manifest_rev=37b51a243302 register='## Capabilities' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met
```
Mutated REV=`c71c73112c51668972580c4e5031f956eeaf43d9`; actual stdout; exit 0, verdict met:
```text
row rounds[313].capabilities_added[0] matched 
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=c71c73112c51668972580c4e5031f956eeaf43d9 manifest_rev=37b51a243302 register='## Capabilities' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met
```
Restored REV=`17d53eb8a044a993874a276b77c56dda8c62c85b`; actual full summary; exit 0, verdict met:
```text
label=P-C1 rev=17d53eb8a044a993874a276b77c56dda8c62c85b manifest_rev=37b51a243302 register='## Capabilities' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met
```

## Explanation and scope

At the pinned clone revision, `.ufo/waves/round-35/count-c1.py:141-191` checks keys, shape, rounds and evidence; it never inspects the what-cell. Acceptance at lines 192–207 consequently remains unchanged. For example, the mutant source-registry row describes journal alarms while retaining the registry key and `corpus/SOURCES.md` evidence (mutant `SCORECARD.md:1961`).

This finding does not amend the contract or decide integration/admission: `.ufo/waves/round-35/contract.md:95-99` explicitly leaves what-cell prose to non-author reviewers. The pre-data receipt already records an empty-cells survivor and separates prose judgments from P-C1 (`.ufo/waves/round-35/evidence/c1-controls.txt:36-44`). The assigned post-data probe demonstrates that fully populated, correct sentences reassigned to the wrong capabilities also survive.

Calibration motivation: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-32-verifier-spotcheck.md:76,116` rejects counters that credit denial/word bags and requires off-topic controls before subsequent calibration data. This report supplies only the assigned post-data control, not an overall calibration verdict.

## Restoration and containment evidence

SHA-256 of complete SCORECARD bytes, measured with `sha256sum` before mutation and `hashlib.sha256` after mutation/restoration:
```text
pristine  2bc9b9c42e8a8bc98f4b6747d4010be92a786894f9bd819ca8bbe0d862a3f27d
mutated   0324cf99a9ac8650e534809be22b545bd052e1f2e8623f79b815380276781157
restored  2bc9b9c42e8a8bc98f4b6747d4010be92a786894f9bd819ca8bbe0d862a3f27d
bytes_equal_pristine: True
restore commit exit: 0
restored_commit: 17d53eb8a044a993874a276b77c56dda8c62c85b
```
The exact-byte comparison occurred before the restoration commit; the restored detector read that committed revision. The mutant remains reachable as its parent. Only this report was written in the lane; all source edits and Git writes were confined to the named scratch clone. No lane restoration was needed. All subprocess calls returned; no background jobs or services were started.

Before cloning, `timeout 10 prlimit --as=1073741824 --cpu=5 -- df -h /fast` reported `/dev/nvme1n1p2 804G 634G 170G 79% /fast`.
Tool installations/updates: none. No further checks were run or claimed.
