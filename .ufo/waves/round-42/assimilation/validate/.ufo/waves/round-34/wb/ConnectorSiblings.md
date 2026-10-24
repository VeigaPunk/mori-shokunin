measured 2026-10-23T07:53:32Z

# Sibling-overlap scan — mori round 34 (wave B)

Scope: read-only over /home/vgpnk/Projects/shokunin/*-shokunin. Judged object: tools/mori-disk-rate.py (ba525e1a..fd252135), contract C1 P-C1-A1. Draft reference: /fast/scratch/hyaku/mori-r34/a3-L1/drafts/corpus_QUALITY.md criterion 99.

## (a) /proc/diskstats, /sys/class/block, rates, device classes

No sibling's newest round covers this surface directly. Code-level scan found no "diskstats" or "class/block" in sibling lane code (excluding .ufo). Closest historical mentions:

- tsukuroi-shokunin/.ufo/waves/round-26/w1/ConnSiblingOverlap.md:22,88 — device-name instability (nvme0n1p1 vs nvme1n1p1) for mori's census write average; enumeration fact only.
- tsukuroi-shokunin/.ufo/waves/round-26/w2/RevProvinceReadme.md:52 — mori would now find nvme1n1p1 in /proc/diskstats.
- kama-shokunin/.ufo/waves/round-16/falsify/advice/ConnectMoriFootprint.md:53 — mori census only /proc reads are diskstats, uptime, meminfo, boot_id.

Verdict: mori should cite tsukuroi r26 as context (device-name drift) but differ: mori-disk-rate.py classifies from <sysfs>/class/block (R3-R4), not df/kernel names; importing the tsukuroi conclusion would overstate. Affected axes: C1 (no-harm to device set) only. VERDICT: no recent sibling overlap for (a).

## (b) Pre-data shortcut / label-keyed / harness-keyed controls

Strong overlap in control discipline, not in domain:

- chousa-shokunin/.ufo/waves/round-29/controls/CtlLabelKeyed/report.md — label-keyed shortcut reaches 82/82 (v1) and 130/130 (v2 warmed) without reopening sources; receipt-before-data discipline.
- chousa-shokunin/.ufo/waves/round-29/controls/CtlIdKeyed/ — id-keyed variant (sibling control).
- chousa-shokunin/.ufo/waves/round-31/controls/CtlShortcutC1.md — ten shortcut rules scored on fresh seeds; endpoint-exact reaches 120/120; v2 re-score closes it to 112/120.
- kake-shokunin/.ufo/waves/round-39/a3-controls/dead-w1/CtlLabelIds.py — label-keyed control for a sitemap validator counter.

Mori should cite chousa r29/r31 and kake r39 for the control-table method and receipt-before-data. Mori should differ/extend: QUALITY 99 requires a harness-keyed arm (detects the counter's own harness: FIFO, namespace, tmpfs, fixed interval/seed) with two-direction bounds on the real input; neither chousa nor kake has a harness-keyed arm, and their label-keyed arms key on fixture labels rather than device names/seed-shaped values. Affected axes: C1 calibration (no-harm), C2 (unprovable-but-better, named non-author review). VERDICT: overlaps found for (b) in chousa and kake.

## (c) Attempt-death recovery of uncommitted round work

Multiple siblings document the same quarantine pattern mori round 34 already follows:

- chousa-shokunin/corpus/lessons/round-32.md:4-6 — attempt 1 died with orchestrator; uncommitted wave files deleted unread-as-evidence.
- kaidoku-shokunin/corpus/lessons/round-31-verifier-spotcheck.md:5 — earlier closure session died; partial work not used.
- kama-shokunin/.ufo/waves/round-27/residual/advice/ReviewLogSecondCorrection.md:40 — 37-seat control wave died; no receipts landed.
- kotoba-shokunin/LOG.md:2498 — attempts 1/2 died; attempt-2 uncommitted edits saved then reset, scratch moved to /fast/scratch.
- kotodama-shokunin/corpus/lessons/round-60.md:3 — attempts 1/2 died; attempt-2 uncommitted build treated as untrusted scratch, captures re-fetched byte-identical.
- kumitate-shokunin/.ufo/waves/round-45/plan.md:206-210 — attempt 2 died after landing; uncommitted entries quarantined.
- mado-shokunin/.ufo/waves/round-25/registration.md:129-130,171 — attempt 1/2 died; untracked scratch deleted/untrusted.
- tameshi-shokunin/corpus/lessons/round-30.md:4-5 — three attempts, two died with orchestrator.
- tsukuroi-shokunin/SCORECARD.md:1365,1380 — attempts 1/2 died; 170/247 uncommitted entries moved to /fast/scratch tarballs, none cited.

Mori should cite these as precedent and adopt the same quarantine (already: attempt-2 snapshot under /fast/scratch/hyaku/mori-r34/a3-L1/drafts is untrusted; re-derive). Affected axes: provenance/reproducibility (C2). VERDICT: overlaps found for (c) in 9 siblings.

## Proposed move (one bounded)

Cite chousa r29/r31 and kake r39 control precedents plus the (c) quarantine precedents in mori's SOURCES/QUALITY evidence; add the missing harness-keyed control (counter-harness detection on real input with two-direction bounds) to the round-34 pre-data control table before any data commit; keep attempt-2 scratch quarantined and re-derived. This improves C1 calibration (closes the QUALITY 99 gap) and C2 provenance without harming C1 coverage, because the new control is an additional negative arm, not a change to mori-disk-rate.py or P-C1-A1.

## Risks

- Harness detection may overfit to one counter harness shape (FIFO/tmpfs/fixed interval); a real tool that incidentally matches could be rejected. Mitigate with two-direction bounds and multiple harness shapes.
- Quarantine citations must not be treated as evidence; only committed re-derived artifacts count.

## Verification

- Frozen counter (count-c1-a1.py) scores both new controls unmet before first data commit; receipt committed as ancestor of first data commit.
- grep confirms no sibling code-level diskstats overlap; report paths above resolve.

VERDICT: overlaps found 10.