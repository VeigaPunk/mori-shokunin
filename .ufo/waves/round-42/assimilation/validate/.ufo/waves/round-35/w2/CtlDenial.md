measured 2026-10-23T09:14:40Z

# CtlDenial — post-data explicit-denial control

Axes: semantic discrimination; byte fidelity; containment; bounded reproducibility.

VERDICT: survived — the explicit-denial mutant receives C1=met, exit 0.
VERDICT: fails — P-C1 alone discriminates this shape.

## Mutant and expected detector

Clone: `/fast/scratch/hyaku/mori-r35/CtlDenial/clone`.
Pristine revision: `cedb0ec4f3a4f672804deac388b7191258f01fcd`.
Control commit: `527bcb89f7f1603a20ea142fc02ee1d93a976d24`.
Restoration commit: `1c0919747667f7e97caa7041db6c1d7fbbb89c6d`.
These revisions and committed-byte hashes are recorded in `/fast/scratch/hyaku/mori-r35/CtlDenial/pristine.json:4-6`, `/fast/scratch/hyaku/mori-r35/CtlDenial/mutated.json:4-6`, and `/fast/scratch/hyaku/mori-r35/CtlDenial/restored.json:4-6`.

Only the 18 what-cells in the last Capabilities table changed, at SCORECARD.md:1961-1978; each became an explicit denial. Keys, capability labels, evidence, rounds, and every other byte remained identical. Evidence: `/fast/scratch/hyaku/mori-r35/CtlDenial/shape.json:10-32`; generator assertions: `/fast/scratch/hyaku/mori-r35/CtlDenial/check-shape.py:1`.

Expected outcome for the discrimination claim under test: denial must receive C1=unmet, exit 1, while pristine and restored registers receive C1=met, exit 0. This is the denial-calibration challenge described in `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-32-verifier-spotcheck.md:71-76,116`; it does not amend frozen P-C1.

## Exact control register bytes (38 lines)

The following is the complete final section from the control commit, SCORECARD.md:1941-1978, retained at `/fast/scratch/hyaku/mori-r35/CtlDenial/denial-register.md:1-38`. SHA256: `64843a286e4e9f764515eaeb6d452df41af0ce7d9fff741cda0fab9429e0fd34` (`/fast/scratch/hyaku/mori-r35/CtlDenial/shape.json:4-9`). The file ends with a newline.

````markdown
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
| `rounds[313].capabilities_added[0]` | source registry | This capability was never demonstrated and does not work. | `corpus/SOURCES.md` | 12 |
| `rounds[339].capabilities_added[0]` | typed journal alarm and subject triage | This capability was never demonstrated and does not work. | `tools/mori-round14-regressions.py` | 14 |
| `rounds[345].capabilities_added[0]` | partial positive journal alarms | This capability was never demonstrated and does not work. | `tools/mori-round15-regressions.py` | 15 |
| `rounds[353].capabilities_added[0]` | exact-start journal record window | This capability was never demonstrated and does not work. | `tools/mori-journal-window.py` | 16 |
| `rounds[386].capabilities_added[0]` | retention gate | This capability was never demonstrated and does not work. | `tools/mori-retention-gate.py` | 18 |
| `rounds[386].capabilities_added[1]` | freeze-order check | This capability was never demonstrated and does not work. | `tools/mori-freeze-order.py` | 18 |
| `rounds[386].capabilities_added[2]` | dispatch-attempt ledger verify | This capability was never demonstrated and does not work. | `tools/mori-dispatch-ledger.py` | 18 |
| `rounds[398].capabilities_added[0]` | blob-bound content-review coverage gate | This capability was never demonstrated and does not work. | `tools/mori-content-review.py` | 19 |
| `rounds[427].capabilities_added[0]` | retention receipt reconciliation | This capability was never demonstrated and does not work. | `tools/mori-retention-reconcile.py` | 22 |
| `rounds[443].capabilities_added[0]` | one-shot system pressure read | This capability was never demonstrated and does not work. | `tools/mori-pressure.py` | 24 |
| `rounds[443].capabilities_added[1]` | round-23 routed-item check | This capability was never demonstrated and does not work. | `tools/mori-routed-check.py` | 24 |
| `rounds[455].capabilities_added[0]` | harness background-job runway read | This capability was never demonstrated and does not work. | `tools/mori-job-runway.py` | 25 |
| `rounds[455].capabilities_added[1]` | round-24 routed-defect and Axes-table check | This capability was never demonstrated and does not work. | `tools/mori-routed-r24.py` | 25 |
| `rounds[462].capabilities_added[0]` | userspace OOM killer one-shot read | This capability was never demonstrated and does not work. | `tools/mori-oom-killers.py` | 26 |
| `rounds[476].capabilities_added[0]` | SOURCES freshness repair | This capability was never demonstrated and does not work. | `corpus/SOURCES.md`, `corpus/knowledge/oom-victim-selection-r27.md` | 28 |
| `rounds[476].capabilities_added[1]` | amendment-A2 frozen cases | This capability was never demonstrated and does not work. | `tools/fixtures/mori-oom-killers/cases-a2.json` | 28 |
| `rounds[495].capabilities_added[0]` | blind-writer gate | This capability was never demonstrated and does not work. | `tools/mori-blind-check.sh` | 31 |
| `rounds[495].capabilities_added[1]` | watchdog identity decision table | This capability was never demonstrated and does not work. | `corpus/knowledge/watchdog-identity-r31.md` | 31 |
````

## Identical detector, actual outputs

Counter executed: `/fast/scratch/hyaku/mori-r35/CtlDenial/count-c1.py`.
SHA256 executed in every phase: `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167` (each phase receipt:5).
The same runner invoked the following command with only REV changing; address-space limit was 1610612736 bytes. Actual argv and limit: each receipt:7-17.

```text
timeout --kill-after=2 55 python3 /fast/scratch/hyaku/mori-r35/CtlDenial/count-c1.py REV --repo /fast/scratch/hyaku/mori-r35/CtlDenial/clone
```

Pristine — `/fast/scratch/hyaku/mori-r35/CtlDenial/pristine.json:18-21`:
```text
label=P-C1 rev=cedb0ec4f3a4f672804deac388b7191258f01fcd manifest_rev=37b51a243302 register='## Capabilities' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met
exit=0; verdict=met; stderr empty
```

Denial mutant — `/fast/scratch/hyaku/mori-r35/CtlDenial/mutated.json:18-21`:
```text
label=P-C1 rev=527bcb89f7f1603a20ea142fc02ee1d93a976d24 manifest_rev=37b51a243302 register='## Capabilities' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met
exit=0; verdict=met; stderr empty
```

Restored — `/fast/scratch/hyaku/mori-r35/CtlDenial/restored.json:18-21`:
```text
label=P-C1 rev=1c0919747667f7e97caa7041db6c1d7fbbb89c6d manifest_rev=37b51a243302 register='## Capabilities' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met
exit=0; verdict=met; stderr empty
```

Each receipt:20 retains lossless complete stdout, including all 18 individual matched-row lines. The successful pristine baseline makes this a surviving mutant, not an inconclusive baseline failure.

## Interpretation and restoration

The decision point validates five-cell shape, round and evidence, but never reads the what-cell (`/fast/scratch/hyaku/mori-r35/CtlDenial/count-c1.py:153-194`). Consequently the denial shape is not discriminated. This is a semantic-coverage finding, not permission to alter the frozen predicate or a judgment of the landed rows. The pinned contract already excludes prose judgment (`/fast/scratch/hyaku/mori-r35/CtlDenial/clone/.ufo/waves/round-35/contract.md:95-99`), and the prior receipt delegates faithful what-cells to separate reviewers (`/fast/scratch/hyaku/mori-r35/CtlDenial/clone/.ufo/waves/round-35/evidence/c1-controls.txt:36-44`). Combined row review was not tested here.

SCORECARD SHA256 before: `2bc9b9c42e8a8bc98f4b6747d4010be92a786894f9bd819ca8bbe0d862a3f27d`.
SCORECARD SHA256 mutated: `c2241ac90469f5339f1535175abd8e316318a19a0f27072e466d73ad31d8042f`.
SCORECARD SHA256 restored: `2bc9b9c42e8a8bc98f4b6747d4010be92a786894f9bd819ca8bbe0d862a3f27d`.
Evidence: `/fast/scratch/hyaku/mori-r35/CtlDenial/pristine.json:6`, `/fast/scratch/hyaku/mori-r35/CtlDenial/mutated.json:6`, `/fast/scratch/hyaku/mori-r35/CtlDenial/restored.json:6`.

Restoration command `cmp /fast/scratch/hyaku/mori-r35/CtlDenial/SCORECARD.pristine.md /fast/scratch/hyaku/mori-r35/CtlDenial/clone/SCORECARD.md && printf 'restored_bytes=identical\n'` printed `restored_bytes=identical`, exit 0, before the restoration commit and restored detector run. The mutant remains reachable at its separate commit.

Containment: my only lane write is this report. All source mutations, Git writes and retained probe files are under `/fast/scratch/hyaku/mori-r35/CtlDenial/`; no lane restoration was needed. No subagents, background jobs, external runtime, tool installs or updates were launched. All started bounded commands returned; detector children were awaited. No broader test suite was run.
