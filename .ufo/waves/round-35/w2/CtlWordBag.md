measured 2026-10-23T09:14:12Z
# CtlWordBag: post-data shuffled-word control

Axes: exact-byte provenance, semantic destruction, detector discrimination, isolation.

## Target, mutation and expected detector

Attacks only: P-C1 alone discriminates this shape. No round-admission judgment.
Base: `cedb0ec4f3a4f672804deac388b7191258f01fcd`. Clone: `/fast/scratch/hyaku/mori-r35/CtlWordBag/clone`.
Mutant commit: `7a2f22ae9f5b990ab23e653e189786b1640d7657`. Restoration commit: `bb3243669fa2e03a50e3577a046672dee824a7a0`.

Mutation: only the capability and what-it-can-now-do cells in the final table were replaced; 18 rows, 36 prose cells. Keys, rounds, evidence, header and all other bytes stay unchanged (`SCORECARD.md:1959-1978` at the mutant commit; construction results below).
Vocabulary comes from admitted mori `capabilities_added` strings returned by `timeout 25s prlimit --as=536870912 --cpu=20 -- git -C /home/vgpnk/Projects/shokunin show 37b51a243302e8009c7067431e8a47f9a722fd14:MANIFEST.json`; selected output: `admitted_capabilities=18`.
Recipe: sorted unique lowercased alphabetic words of length at least four; `random.Random(3502)`; sample 8 words for each capability cell and 10 for each what cell, then shuffle each sample, in table order.
Construction output: `changed_rows=18 changed_prose_cells=36 protected_cells_equal=true outside_table_equal=true all_bag_tokens_in_manifest_vocabulary=true vocabulary_size=214` (`/fast/scratch/hyaku/mori-r35/CtlWordBag/receipts.json`, construction).

Expected discrimination of this negative control: `C1=unmet`, exit 1. The frozen predicate is not amended. The earlier closure requires word-bag controls for calibration (`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-32-verifier-spotcheck.md:74-76,116`).

## Exact control register (38 lines)

Complete final section, `SCORECARD.md:1941-1978` at `7a2f22ae9f5b990ab23e653e189786b1640d7657`; also `/fast/scratch/hyaku/mori-r35/CtlWordBag/control-register.md`:

```markdown
## Capabilities

Round 35 (claim C1, calibration). This is the lane's current capabilities register, the `capabilities` field of the
AXES.md SCORECARD contract (S199). It holds one row per capability that a non-author closure admitted, as fleet
`MANIFEST.json` at fleet commit `37b51a24` records it (S200). The key is that closure's `rounds[i].capabilities_added[j]`;
the first-working round is the closure's round; the evidence is the artifact that round landed and the closure names.
Rows enter only through a round that demonstrates the capability running (S199), so the three capabilities of round 17,
a rejected round, are not rows. As the current self-assessment this register supersedes the `— none yet —` table in the
first `## Capabilities` section (left as filed at `d677cf3`) and the per-round capability tables, none of which listed
the admitted set. Check: `python3 .ufo/waves/round-35/count-c1.py <rev>` (predicate P-C1,
`.ufo/waves/round-35/contract.md`).

Rows that predate MANIFEST are not register rows: live census and census self-test (round 1), silence oracle (round 2)
and drift pin (round 10), in `## Capabilities (round 12 demonstrations)` above. They were admitted before MANIFEST
carried any mori `capabilities_added` key (its first keyed mori entry is `rounds[313]`, round 12): round 1 by the fleet
closure `rounds[140]`, rounds 2 and 10 by goal-wave verdicts with no named non-author verifier (this file's Round 2
and Round 10 verdicts). Their evidence pointers resolve at `dd76eb79`.

| key | capability | what it can now do | evidence | first-working round |
|---|---|---|---|---|
| `rounds[313].capabilities_added[0]` | killed flagged freeze head survivors kill pressure attempt | reads zero clamp writer cursor call aggregate default escalation probe | `corpus/SOURCES.md` | 12 |
| `rounds[339].capabilities_added[0]` | totals version without reconciliation captures published read record | while knowledge advancing after evidence failed repointed supersedes tool pinned | `tools/mori-round14-regressions.py` | 14 |
| `rounds[345].capabilities_added[0]` | style memory alarm kill eight journal unsafe written | reconcile user dispatch async without knowledge objects amendment proc plain | `tools/mori-round15-regressions.py` | 15 |
| `rounds[353].capabilities_added[0]` | recount attempt this order configs remain agreement escalation | held call scope exit item always objects receipt dispositions rows | `tools/mori-journal-window.py` | 16 |
| `rounds[386].capabilities_added[0]` | reconciliation always full effective json explicit runway configured | accounting nearest null dispatch remain journal window measured timing round | `tools/mori-retention-gate.py` | 18 |
| `rounds[386].capabilities_added[1]` | held coverage alarm over restored aggregate eight disclosed | positive subject invalid clamp repointed live remains captures setting overclaims | `tools/mori-freeze-order.py` | 18 |
| `rounds[386].capabilities_added[2]` | journal free review some regression fixtures boot verify | retention corpus bounded requirements clearance freeze tool round oomd exact | `tools/mori-dispatch-ledger.py` | 18 |
| `rounds[398].capabilities_added[0]` | attempt harness axes json corpus detector dispatch head | configs case background invalid ledger default head this coverage observations | `tools/mori-content-review.py` | 19 |
| `rounds[427].capabilities_added[0]` | harness counts published written content this oomd privacy | version metric seek defect plus foreign gate cases without defects | `tools/mori-retention-reconcile.py` | 22 |
| `rounds[443].capabilities_added[0]` | cases equal after axes shot bound captures frozen | order never probe thresholds content lane agreement oomd actual blob | `tools/mori-pressure.py` | 24 |
| `rounds[443].capabilities_added[1]` | aggregate published timing system frozen wave block lane | while cells totals writer advancing clamp current shot retained order | `tools/mori-routed-check.py` | 24 |
| `rounds[455].capabilities_added[0]` | style configs amendment bounded unit background watchdog state | seek repointed fixtures resource journal killers zero superseded configs system | `tools/mori-job-runway.py` | 25 |
| `rounds[455].capabilities_added[1]` | overclaims blob unavailable send state version typed evidence | scope killers start undefined disclosed repointed watchdog clamp mismatches advancing | `tools/mori-routed-r24.py` | 25 |
| `rounds[462].capabilities_added[0]` | sources verify harness exact file states positive runway | mori free default async four exit head foreign recount binary | `tools/mori-oom-killers.py` | 26 |
| `rounds[476].capabilities_added[0]` | invalid processes earlyoom pinned alarm carried amendment retain | processes alarms disclosed setting invalid corpus memory objects zero path | `corpus/SOURCES.md`, `corpus/knowledge/oom-victim-selection-r27.md` | 28 |
| `rounds[476].capabilities_added[1]` | table systemd cursor configured user refusing residual subject | residual wave cases unit routed recount content repointed check probe | `tools/fixtures/mori-oom-killers/cases-a2.json` | 28 |
| `rounds[495].capabilities_added[0]` | shot order signal check window retention alarm inputs | refusing cursor case from blob full qualified verified byte before | `tools/mori-blind-check.sh` | 31 |
| `rounds[495].capabilities_added[1]` | retained rows reconcile fixtures objects verdict plus survivors | this held only readers foreign observations blind cells path byte | `corpus/knowledge/watchdog-identity-r31.md` | 31 |
```

## Frozen detector and actual outputs

Command for each row below (only REV changes):
```text
timeout 300s prlimit --as=1073741824 --cpu=290 -- python3 -B /fast/scratch/hyaku/mori-r35/CtlWordBag/clone/.ufo/waves/round-35/count-c1.py REV --repo /fast/scratch/hyaku/mori-r35/CtlWordBag/clone
```
`sha256sum` output before the probe for both the scratch counter and the lane counter: `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167`. The exact same hash was recorded for all three runs and after restoration (`/fast/scratch/hyaku/mori-r35/CtlWordBag/receipts.json`, detector_sha256 and each run's counter_sha256).

Pristine full summary:
```text
label=P-C1 rev=cedb0ec4f3a4f672804deac388b7191258f01fcd manifest_rev=37b51a243302 register='## Capabilities' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met
```
Exit 0; verdict met; stderr empty. All 18 row lines said matched.

Mutant full summary:
```text
label=P-C1 rev=7a2f22ae9f5b990ab23e653e189786b1640d7657 manifest_rev=37b51a243302 register='## Capabilities' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met
```
Exit 0; verdict met; stderr empty. All 18 row lines said matched.

Restored full summary:
```text
label=P-C1 rev=bb3243669fa2e03a50e3577a046672dee824a7a0 manifest_rev=37b51a243302 register='## Capabilities' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met
```
Exit 0; verdict met; stderr empty. All 18 row lines said matched.
Full stdout, stderr, argv and exit codes for all runs: `/fast/scratch/hyaku/mori-r35/CtlWordBag/receipts.json`, baseline/mutant/restored.

VERDICT: survived — shuffled-word mutant, C1=met, exit 0.
VERDICT: fails — P-C1 alone discriminates this shape.

The frozen counter checks the key, five-cell shape, round and evidence, not either prose cell (`.ufo/waves/round-35/count-c1.py:141-186` at `cedb0ec4f3a4f672804deac388b7191258f01fcd`). The contract explicitly reserves prose review to non-authors (`.ufo/waves/round-35/contract.md:95-99` at that revision). This is a coverage finding about P-C1 alone, not permission to revise the frozen contract or a claim that the landed prose is false.

## Hashes and restoration evidence

SHA-256 measured from the scratch SCORECARD bytes before mutation, after mutation and after exact restoration:
```text
pristine  2bc9b9c42e8a8bc98f4b6747d4010be92a786894f9bd819ca8bbe0d862a3f27d
mutant    bea8c3b1eb6d79ada20cadbdbe163ab2d495982fd06fe0f0d6c98a4e2a93a0ba
restored  2bc9b9c42e8a8bc98f4b6747d4010be92a786894f9bd819ca8bbe0d862a3f27d
```
Restoration used the original 18 row bytes and committed them in the clone. `git -C /fast/scratch/hyaku/mori-r35/CtlWordBag/clone rev-parse REV^{tree}` returned `9666fedea72e1e308db07513287783711ee61e24` for both the pristine and restored commits. The restored counter run above therefore scored the original complete tracked tree, not just a passing substitute.

Only this report was written in the lane. All mutation/commit operations were confined to `/fast/scratch/hyaku/mori-r35/CtlWordBag`; no lane or fleet git writes, runtime invocation, installs, background jobs or services. All bounded child commands returned. No lane restoration was needed. Tools installed/updated: none.
