measured 2026-10-23T09:16:26Z

# CritNoHarm — whole-round no-harm audit

Scope: `dd76eb79` → `cedb0ec4f3a4f672804deac388b7191258f01fcd`, immutable Git objects, not the moving working tree. Advisory review only; no admission or canonical judgment.

Axes: coverage (preserved surfaces), operability (commands meet their contracts), depth (correct technical detail), freshness (staleness flagged), calibration (truthful self-assessment), adjacency (ownership boundaries). Definitions: `corpus/evidence/sources-r35/S199.src:11-16`.

All lane-relative citations below refer to the attacked tip unless another revision is named. Scratch evidence root: `/fast/scratch/hyaku/mori-r35/CritNoHarm/`.

## Per-axis verdicts: the claim is not harmed

VERDICT: holds — coverage not harmed. No existing surface, tool, province boundary or coverage-map entry was removed; the earlier repertoire is explicitly retained as historical evidence rather than silently erased. Evidence: `PROVINCE.md:6-18,42-57`; `SCORECARD.md:1953-1957`; scratch `static-diff-receipt.txt:2,7`.

VERDICT: fails — operability not harmed. The newly shipped append-only checker returns the violation exit code for an operational error, contradicting its own advertised interface. Finding N2; `.ufo/waves/round-35/check-sources-appendonly.py:8-12,25-32`; scratch `checker-error-counterexample.txt:1-3`.

VERDICT: fails — depth not harmed. The new SKILL correction attaches the partition condition to the parent, while the cited kernel checks the device itself. Finding N1; `SKILL.md:846-848`; `corpus/evidence/sources-r34/S193.src:2430-2433,3508-3510,3542-3543`.

VERDICT: holds — freshness not harmed. The inherited freshness score/evidence is retained; the stacked-device attribution is explicitly downgraded to a bounded host observation, and the broken drafting pointer is marked unusable with committed replacement judgments. This is not a claim of a new live-host verification. Evidence: `SCORECARD.md:13`; `SKILL.md:849-854`; `corpus/knowledge/disk-write-rate-r33.md:102-108`.

VERDICT: fails — calibration not harmed. New QUALITY 102 and its checker introduce a weaker, competing meaning of append-only conformance: a supersession marker suppresses a cell-preservation violation. Existing QUALITY 81 does not grant that waiver. Finding N3; `corpus/QUALITY.md:373-377,799-808`; `.ufo/waves/round-35/check-sources-appendonly.py:80-94`.

VERDICT: holds — adjacency not harmed within this diff. Detection/report-only boundaries remain; the new checks inspect mori's own record rather than taking ownership of dispatch, OS remediation or sibling registers. No sibling path is in the changed-path inventory. Evidence: `PROVINCE.md:12-18,132-138`; `.ufo/waves/round-35/contract.md:16-20,28-31`; scratch `static-diff-receipt.txt:2,7`; read-only command `timeout 120 prlimit --as=1073741824 --cpu=110 git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --name-status dd76eb79 cedb0ec4f3a4f672804deac388b7191258f01fcd` lists only lane-local paths.

## N1 — device-versus-parent predicate changed in new prose

Counterexample: a partition device with a whole-disk parent. The new wording makes the parent's non-partition status the condition. The actual helper checks `dev->type`, and add/delete call it with `dev`, not its parent. [INFERENCE] A reader following that wording can infer that this partition qualifies when the kernel excludes it.

Evidence:
- New sentence: `SKILL.md:846-848`.
- Predicate definition: `corpus/evidence/sources-r34/S193.src:2430-2433`.
- Add/delete guards: the same source at `3508-3510,3542-3543`.
- The newly added source row itself uses the correct subject: `corpus/SOURCES.md:208`.

Impacted axis: depth. No changed classifier implementation or observed runtime classification regression is alleged; `tools/` is untouched (scratch `static-diff-receipt.txt:7`).

Smallest safe correction: state separately that the device has a parent and that the device itself is not a partition. Preserve the separate reparent-path qualification. This is a fixable wording defect, not an unavoidable tradeoff.

## N2 — operational errors are reported with the violation exit code

Counterexample executed against the immutable scratch copy:

`timeout 30 prlimit --as=536870912 --cpu=25 python3 -I -B /fast/scratch/hyaku/mori-r35/CritNoHarm/tip/.ufo/waves/round-35/check-sources-appendonly.py refs/heads/CritNoHarm-nonexistent-fixture --repo /home/vgpnk/Projects/shokunin/mori-shokunin`

Output was an error from `git rev-parse`, ending in `fatal: Needed a single revision`; observed exit was **1**, not the documented error exit **2**. Full command/output: scratch `checker-error-counterexample.txt:1-3`.

The mechanism is not specific to that synthetic revision: the Git failure paths call `sys.exit` with a string, as do other explicit error paths. Evidence: `.ufo/waves/round-35/check-sources-appendonly.py:25-32,46-48,64-67`; its exit contract is at `8-12`.

Impacted axis: operability. [INFERENCE] An exit-code consumer cannot distinguish this unavailable/error state from a completed scan finding violations.

Smallest safe correction: consistently print the diagnostic and terminate with numeric exit 2 for operational errors; retain exit 1 for completed scans with violations. Do not special-case the synthetic revision. Fixable interface defect; no production tool was changed by this probe.

## N3 — new append-only rule relaxes the preserved-cell authority

Counterexample already available locally: the checker author's sandbox adds replacement rows whose source cell explicitly says no source was opened, then gets `appendonly_violations=0`, exit 0, for all 17 previously flagged IDs. I did not rerun that reported observation. Evidence: `.ufo/waves/round-35/w1/MineAppendOnly.md:157-160`.

This is not merely a fabricated-row example. Even a genuine superseding source does not make an old row's rewritten cells equal its first-published cells. Existing QUALITY 81 requires that preservation; new QUALITY 102 expressly exempts superseded IDs and describes S182/S193 as discharged. Evidence: `corpus/QUALITY.md:373-377,799-808`.

The implementation trusts the teaches prefix alone and diverts any changed, superseded ID away from violations. It does not test replacement content or ordering in that decision. Evidence: `.ufo/waves/round-35/check-sources-appendonly.py:80-94`. Its own report acknowledges blanket per-ID discharge, including subsequent edits: `.ufo/waves/round-35/w1/MineAppendOnly.md:190-194`.

Impacted axis: calibration; this creates duplicate conformance authorities, not an actual round-35 edit to an old SOURCES cell. The endpoint comparison preserved **198/198** old rows and added S199–S204 (scratch `static-diff-receipt.txt:3`). The new waiver is the regression.

Smallest safe correction: keep supersession as disposition metadata, not permission to suppress the preservation violation. Remove QUALITY 102's exemption and report changed immutable cells even when a later row supersedes them. Alternatively, a narrower triage check must not be labelled an append-only conformance check or replace QUALITY 81. Corrected current knowledge and historical preservation are separate properties; do not trade one for the other or rewrite history.

## Preservation and limits

- The whole diff has 73 changed paths: 68 additions, five modifications, no deletions. SKILL, QUALITY and the existing disk-rate knowledge entry preserve their entire baseline bytes as prefixes. Evidence: scratch `static-diff-receipt.txt:1-7`; `git diff --numstat dd76eb79 cedb0ec4f3a4f672804deac388b7191258f01fcd` reports only two removed lines, both in SCORECARD.
- Those two replacements update the current operability/depth cells, name their old values and retain the scores. The cited round-31 closure supports the new last-change references. Evidence: `SCORECARD.md:11-12`; `corpus/lessons/round-31-verifier-spotcheck.md:154-155`. I found no new in-place rewrite of filed history in this diff.
- Static checking of 59 newly added, backticked substantive pointers found no out-of-bounds range and only the expressly repudiated historical `round-34/w1/` directory absent. Abbreviated/unbackticked references were not included in that count. Evidence: scratch `static-diff-receipt.txt:8` and `substantive-pointer-scan.json`; the repudiation is `corpus/knowledge/disk-write-rate-r33.md:102-103`.
- The replacement row judgments preserve the disagreement, not false unanimous provenance: wave A supports 3r, wave B rejects 3r, and the residual supports the distinct 3r2. Evidence: `.ufo/waves/round-34/wa/JudgeRow3r.md:33`; `wb/ReJudgeRow3r.md:36`; `wb/residual/MoriR34A3.JudgeRow3r2.md:95`.
- The pre-data blank-cell meet is already acknowledged in the landed lesson and QUALITY 101. That remains a frozen claim-validity issue; it is not repaired by these local corrections or converted here into a canonical admission decision. Evidence: `.ufo/waves/round-35/evidence/c1-controls.txt:36-44`; `corpus/lessons/round-35.md:64`; `corpus/QUALITY.md:788-798`.

Execution limits: the only behavior probe I ran was N2; no C1 counter, census, selftest, build, canonical judge or agent runtime was invoked. No installs/updates, Git/jj writes, subagents or background jobs. Writes were limited to this report and this seat's scratch directory; all started commands completed.
