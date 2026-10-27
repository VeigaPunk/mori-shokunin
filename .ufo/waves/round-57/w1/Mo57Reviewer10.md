# Mo57Reviewer10 — independent receipt-path/wording recheck

Verdict: **Routed defects 1–2 reproduce as citation/wording defects; the underlying receipts themselves are present and their values are not falsified.** No production edits or commits made.

## Findings

- **MED — Report/LOG receipt pointers are rooted incorrectly.** The round-56 closure independently identifies the report and LOG pointers as `evidence/driver-liveness-live.txt`, `evidence/tally-r55.txt`, `evidence/controls.txt`, and `evidence/c1-at-landed.txt`, while the committed wave receipts are under `.ufo/waves/round-56/evidence/…` (`corpus/lessons/round-56-verifier-spotcheck.md:81-84`). The analogous landed receipts present here are `.ufo/waves/round-56/evidence/c1-at-landed.txt:1-2` and `c2-at-landed.txt:1-2`; these contain met verdicts and stamp `097c342b…`, not the freeze revision. Thus the basename-only references do not resolve from the lane root, and a resolver must add the wave path. Pointer defect, not evidence-value failure.
- **LOW — “1728 lines” wording can be misread as receipt-file length.** The lesson explicitly records this ambiguity at `corpus/lessons/round-56-verifier-spotcheck.md:28,84`: 1728 is the recorded live log field (`log.lines`), whereas the receipt is 304 lines. In `LOG.md:2952`, “full live-log grammar coverage: 1728 lines” is more clearly log-oriented than the reported parenthetical, but should still be made explicit as `log.lines=1728` and linked to the field. The claim is about captured watchdog-log lines, not receipt length.

## Independent recheck plan

From `/home/vgpnk/Projects/shokunin/mori-shokunin`, check each cited pointer exactly as written (`test -e evidence/<name>`); then check the wave-rooted counterpart (`test -e .ufo/waves/round-56/evidence/<name>`). For each receipt, read the recorded command, output, exit status, and revision; compare the `rev=` stamp to the revision named by the claim rather than assuming freeze and landed are interchangeable. For the live receipt, find the `log.lines=1728` field and count physical receipt lines separately; report both quantities and confirm `log.malformed` and lane count from recorded fields. Do not use live log growth or re-run output to overwrite the captured receipt. The round-56 verifier lesson lines 28, 31-35, and 81-85 already provide independent corroboration for the path and wording distinctions.

## Verification scope / gaps

Read frozen contract first (`.ufo/waves/round-57/contract.md`); it concerns C1 capability-table and C2 knowledge-entry predicates, not changing these frozen predicates. Disk guard status was checked before work; ample scratch volume was reported. This scoped review read the round-56 verifier report and evidence, but the cited `.ufo/reports/round-56/mori.md` path was not present in the current tree, so the original report citation locations could not be re-opened directly. No LSP device/server was available in the tool inventory; findings concern static evidence artifacts, not semantic code references. No fixture, host-state, or production changes were made.
