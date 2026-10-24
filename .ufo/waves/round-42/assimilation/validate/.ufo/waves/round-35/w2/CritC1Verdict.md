measured 2026-10-23T09:12:44Z

# CritC1Verdict — structural meet is not C1 verification

Advisory falsification review only; no canonical judgment or admission. All lane citations below refer to `cedb0ec4f3a4f672804deac388b7191258f01fcd`, except the explicitly cited baseline `dd76eb79` and freeze `f2d28711`. Sources were read with bounded, read-only `git show`; no working-tree version substitutes for the assigned revision.

VERDICT: fails — C1 verifies. The strongest existing counterexample is pre-data control 10c: the declared register without either human-readable capability field still receives matched=18, mismatches=0, C1=met, exit 0. Under pre-existing QUALITY 98, treating that defective deliverable as a positive control does not discharge the content-free shape. The frozen kill rule therefore calls for an honest stop, even if the landed register itself meets P-C1. Evidence: `.ufo/waves/round-35/c0/CtlSkipDesign-register.md:3-22`; `.ufo/waves/round-35/c0/CtlSkipDesign.md:210-231`; `corpus/QUALITY.md@dd76eb79:715-725`; `.ufo/waves/round-35/contract.md:103-104`.

## Axes

VERDICT: holds — calibration is the right axis. The surface is the lane's current SCORECARD self-assessment against historical admitted closures, not a new observability operation. Structural missing/bad/extra binding counts are relevant to calibration, but are not sufficient evidence of semantic calibration. Coverage, depth and operability acquisitions cannot be inferred from restoring eighteen historical rows. Evidence: `.ufo/waves/round-35/contract.md:14-31`; `.ufo/waves/round-35/count-c1.py:103-133,192-198`; `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/AXES.md:11-16,57-64`; `../.ufo/prompts/mori-round-35.md:348-349,361-365`.

The impacted dimensions are calibration and its discernment signal; preservation of capability identity, first-working rounds and operational scope are the no-harm constraints. Filling the pinned register is not saturation of calibration: the SCORECARD retains calibration 5 and the contract claims this finite register only. Evidence: `SCORECARD.md:14,1941-1978`; `.ufo/waves/round-35/contract.md:35-47`.

## Strongest argument for verification

1. The frozen claim deliberately measures a historical provenance join. Its positive-control clause already allows oracle-derived rows and reserves prose and pointer choice for separate human review. This limitation exists at freeze `f2d28711`, not merely in a post-data explanation. Evidence: `.ufo/waves/round-35/contract.md@f2d28711:28-47,95-99`.
2. Control 10c is not do-nothing or an ID-only guess: it actually derives each correct key, closure round and strong artifact, including named-path restrictions. Control 9d retains a strong backticked artifact in each row. Their shared pre-data ruling classifies that binding as the claimed work. Evidence: `.ufo/waves/round-35/c0/CtlSkipDesign.md:184-207`; `.ufo/waves/round-35/c0/CtlDangling.md:79-80,195-219`; `.ufo/waves/round-35/evidence/c1-controls.txt:36-44`.
3. Do-nothing, missing-register, label-only and round-wide-reuse controls do fail. A met genuine positive control is necessary to show reachability, not automatically a falsification. Evidence: `.ufo/waves/round-35/evidence/c1-controls.txt:11-30,33-35`; `.ufo/waves/round-35/contract.md:95-99`.

This is a strong defense of literal P-C1 and of retaining useful maintenance. It is not a defense of bypassing the lane's pre-existing admission bar. The question is not whether correct key/artifact binding takes work, but whether a deliverable missing the self-assessment content can certify the declared calibration repair. Evidence: `corpus/QUALITY.md@dd76eb79:715-725`; `.ufo/waves/round-35/contract.md:16-19,46-47`.

## Strongest argument against verification

### Counterexample 10c is already measured, not hypothetical

The declared five fields are key, capability, what it can now do, evidence and first-working round. In the retained 10c register, key/evidence/round are populated, while both capability and what fields are empty in every data row. The generator deliberately emits those empty fields, and the retained full output reports oracle=18, rows=18, matched=18, missing=bad=extra=0, C1=met, exit 0. Evidence: `.ufo/waves/round-35/contract.md:46-47`; `.ufo/waves/round-35/c0/CtlSkipDesign-register.md:3-22`; `.ufo/waves/round-35/c0/CtlSkipDesign.md:203-231`.

The mechanism is visible without rerunning it: the row checker validates cell count, key, round and backticked evidence, but never validates the capability or what fields. Thus 10c does substantive provenance binding while omitting the very human-readable self-assessment the repertoire table promises. Evidence: `.ufo/waves/round-35/count-c1.py:141-191`; `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/AXES.md:59-64`.

### Why this does not depend on retroactive QUALITY 101

QUALITY 98 already existed at entering tip `dd76eb79`. It requires each rejection shape to have a named injected-defect control or reasoned inapplicability; a guard/absent-deliverable failure is not a substitute for testing other shapes. It explicitly requires redesign or exploratory declaration when a defective control meets the counter. Evidence: `corpus/QUALITY.md@dd76eb79:715-725`.

10c preserves the table and its valid bindings while removing the capability-description content; it is the stronger injected content-free case, not merely an absent-register guard failure. The pre-data ruling cannot make those empty fields a faithful self-assessment by calling them residuals. This is the substantive classification defect, not an allegation that the counter violated its narrower implementation. Evidence: `.ufo/waves/round-35/c0/CtlSkipDesign-register.md:3-22`; `.ufo/waves/round-35/evidence/c1-controls.txt:36-44`; `.ufo/waves/round-35/contract.md:16-19,46-47,103-104`.

Independently, the original contract's controls do not map server echo, observed-column copying, no-decision content or post-data rule change to named controls or reasoned inapplicability. That fails pre-existing 98(a), even for a reader who accepts 10c as a positive structural join. This missing mapping is not a claim that an unrun control passed. Evidence: `.ufo/waves/round-35/contract.md:77-99`; `corpus/QUALITY.md@dd76eb79:715-725`.

The landed lesson itself identifies the 10c residual ruling as M1 and says QUALITY 98 should have caught it. New QUALITY 101 makes the field-level prevention explicit and cites that same receipt. Those are supporting admissions and future prevention, not a replacement frozen predicate or a necessary retroactive premise of this finding. Evidence: `corpus/lessons/round-35.md:64`; `corpus/QUALITY.md:788-798`.

### 9d is corroborating, not the decisive falsifier

9d appends a nonexistent plaintext path beside each valid backticked path and receives C1=met. The strongest defense is real: the frozen row grammar says evidence paths are backticked, so the parser treats that plaintext as outside its citation set. Do not misreport 9d as having no valid evidence or no binding work. It shows a reader-facing evidence-cell limit, but 10c and the missing QUALITY-98 shape mapping suffice without resolving 9d's classification. Evidence: `.ufo/waves/round-35/c0/CtlDangling.md:195-233`; `.ufo/waves/round-35/contract.md:46-47`; `.ufo/waves/round-35/count-c1.py:161-185`.

### Precedent and freeze constraint

The kaidoku round-32 reviewer separated a truthful capabilities repair from a counter that also credited denial and word bags: maintenance remained accurate, calibration was unprovable, and a later exploratory relabel was not available. Its routed defect demanded pre-data denial/word-bag/off-topic controls. This is corroborating precedent, not proof that those mori controls were run, and not a new authority overriding mori's frozen rule. Evidence: `../kaidoku-shokunin/corpus/lessons/round-32-verifier-spotcheck.md:69-76,116`.

The round prompt independently prohibits narrowing after landing and changing the scored rule after seats have scored. Later supported-row reviews can establish that the actual table is useful; they cannot erase an earlier met defective control or become a newly counted semantic arm of P-C1. Evidence: `../.ufo/prompts/mori-round-35.md:351-360`; `.ufo/waves/round-35/evidence/c1-controls.txt:40-44`; `.ufo/waves/round-35/contract.md:103-104`.

## Is anything harmed?

No separate C1 artifact regression is established by this review. The new register explicitly supersedes the old current-table appearances, retains legacy capabilities in a separate disclosure, and keeps historical keys and first-working rounds; the standing scores are not increased. This avoids duplicate current authorities and new-round acquisition credit. Evidence: `SCORECARD.md:10-15,1943-1978`; inspected command `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff dd76eb79 cedb0ec4f3a4f672804deac388b7191258f01fcd -- SCORECARD.md` shows two historical last-change corrections plus the appended register, with no score change.

Unprovable is not automatically harmed. The calibration failure is the proposed verification inference, not proof that every repaired row is false. An honest-stop disclosure preserves that distinction; calling the measured claim verified despite 10c would repeat the self-assessment overreach. Evidence: `corpus/lessons/round-35.md:64`; `.ufo/waves/round-35/contract.md:103-104`; analogous distinction at `../kaidoku-shokunin/corpus/lessons/round-32-verifier-spotcheck.md:76`.

This is not a fleet-wide or six-axis no-harm certification, and does not replace the individual row reviews. No tool behavior, source-admission decision or regression suite was exercised here. The prompt bars universal no-harm claims without an enumerating measure. Evidence: `../.ufo/prompts/mori-round-35.md:346-347`; the contract reserves semantic review separately at `.ufo/waves/round-35/contract.md:95-99`.

## Smallest safe correction / what L1 must report

- Preserve the frozen counter, contract, predicate and raw receipts. Report the exact landed-revision numeric P-C1 result separately, when actually measured; do not change a recorded met into an unmet to match the claim verdict. Evidence: `.ufo/waves/round-35/contract.md:5-7,51-55,103-104`; `../.ufo/prompts/mori-round-35.md:357-360`.
- Report C1 not verified, calibration unprovable, honest stop: 10c met before data despite the omitted capability/what fields; the non-skip ruling conflicts with pre-existing QUALITY 98; the required shape map is also incomplete. Keep QUALITY 101/M1 as learned prevention, not a cure for this round's frozen measure. Evidence: `corpus/QUALITY.md@dd76eb79:715-725`; `.ufo/waves/round-35/evidence/c1-controls.txt:36-44`; `corpus/lessons/round-35.md:64`.
- Retain the useful register and report supported/unsupported row evidence beside P-C1. Do not retroactively declare this measured claim exploratory, award new round-35 capabilities, raise calibration, retire it as saturated, or use outside prose review to waive the kill rule. Evidence: `.ufo/waves/round-35/contract.md:14-20,95-104`; `../.ufo/prompts/mori-round-35.md:351-360`; `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/AXES.md:43-55,59-64`.

The defect is fixable for a future frozen instrument and in present reporting. It is not a permissible trade of semantic self-assessment for a clean structural tally in this frozen claim. The canonical judge remains the only admission authority.

## Inspection and containment

- Read the assigned contract at both freeze and attacked tip, pre-data receipt, actual 10c bytes/generator/output, 9d generator/output, counter, baseline and landed QUALITY, M1, scorecard diff, named precedent/prompt sections, and wave-1 critiques. Existing control failures/successes were not rerun.
- Executed digest command: `timeout 90 prlimit --as=1073741824 --cpu=80 -- git -C /home/vgpnk/Projects/shokunin/mori-shokunin show cedb0ec4f3a4f672804deac388b7191258f01fcd:.ufo/waves/round-35/count-c1.py` piped to equally bounded `sha256sum`; output `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167  -`, matching the assigned freeze digest and `evidence/c1-controls.txt:2`.
- No counter, gate, test, canonical judge, other runtime, live host probe, subagent or background job was started. No exact landed-tip counter pass is claimed by this seat. All started foreground commands completed.
- Only this assigned report was written. No scratch files, clones, git/jj writes or tool installs/updates. Timestamp command `timeout 10 prlimit --as=268435456 --cpu=5 -- date -u +%FT%TZ` returned `2026-10-23T09:12:44Z`.
