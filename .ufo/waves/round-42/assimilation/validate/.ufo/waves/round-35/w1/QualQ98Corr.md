measured 2026-10-23T08:51:52Z

# QUALITY 98 correction — routed defect 5

## Behavior
Reviewed QUALITY 98, the round-34 control table and receipt, and the round-34 spot-check's C2 Against findings. Drafted an append-only paragraph correcting D1, D2 and D4; the required target remains `corpus/QUALITY.md` (QUALITY.md:715-731; round-34-verifier-spotcheck.md:96-107, 209-213).

## Findings
VERDICT: D1 agree — QUALITY 98 names “a rule changed” after data as a shape (corpus/QUALITY.md:717-718), but the round-34 table has no row for that shape; its after-judgment inapplicability is only for rows deleted after judgment (round-34/contract.md:67-81; round-34-verifier-spotcheck.md:103).

VERDICT: D2 agree — the server-echo row is marked “unmet (guard)” (round-34/contract.md:77-78), and C-echo-v1's P-C1 receipt shows the guard trip and `C1=unmet` (round-34/evidence/c1-controls.txt:26-28). QUALITY 98 permits a guard-tripped generic absence to discharge only skip-work and content-free, not server echo (corpus/QUALITY.md:718-720; round-34-verifier-spotcheck.md:100-102).

VERDICT: D4 agree — the contract says three of the 16 negative controls met P-C1 (round-34/contract.md:142-143), but four negative-control runs have `C1=met` under P-C1: C-echo-v2-base64 (round-34/evidence/c1-controls.txt:29-31), C-echo-v3-umount (:32-34), C-emptylive (:38-40), and C-zero-singleread (:41-43). Other negative-control receipts show unmet (round-34/evidence/c1-controls.txt:2-28, 35-37, 44-49). These are four runs across three shape groupings; the contract groups C-echo v2/v3 together (round-34/contract.md:115-121, 145-146).

## Draft

```text
DRAFT QUALITY 98-correction
98 correction (round 35). Append-only correction: D1 — 98 includes “a rule changed” after data among the required shapes (corpus/QUALITY.md:717-718), but the round-34 control table has no row for that shape; its inapplicability entry covers only rows deleted after judgment (round-34/contract.md:67-81). D2 — the C-echo server-echo row is marked “unmet (guard)” (round-34/contract.md:77-78), and C-echo-v1's receipt records the guard trip with P-C1 `C1=unmet` (round-34/evidence/c1-controls.txt:26-28). Since 98 says a guard-tripped generic absence discharges only skip-work and content-free (corpus/QUALITY.md:718-720), that result does not show the server-echo shape was discharged. D4 — the contract's statement that three of the 16 negative controls met P-C1 is an undercount of runs (round-34/contract.md:142-143): four negative-control runs met P-C1, namely C-echo-v2-base64 (round-34/evidence/c1-controls.txt:29-31), C-echo-v3-umount (:32-34), C-emptylive (:38-40), and C-zero-singleread (:41-43); the other negative-control receipt rows are unmet (round-34/evidence/c1-controls.txt:2-28, 35-37, 44-49). These four runs belong to three shape groupings because the contract groups C-echo v2/v3 together (round-34/contract.md:115-121, 145-146).
```

## Gates and touched surfaces
- Source reads only; no counter, build, test, lint, or other project gate was run. Timestamp command: `timeout 5 date -u +%FT%TZ` → `2026-10-23T08:51:52Z`.
- Written surface: `.ufo/waves/round-35/w1/QualQ98Corr.md` (this report). No product/source document, contract, receipt, or judge was edited.
- No tools were installed. No git/jj writes, commit, push, publish, deploy, or subagent dispatch occurred.

## Out of scope and limits
No lane change was made to `corpus/QUALITY.md`; the correction above is a draft for the integration owner. Findings are based on the cited text and receipt; no counter was rerun.

## Artifact path
`.ufo/waves/round-35/w1/QualQ98Corr.md`
