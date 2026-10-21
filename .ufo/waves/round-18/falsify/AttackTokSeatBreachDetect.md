# Round-18 token-redaction attack: ReviewSeatBreachDetect

## Axes

1. Completeness of the changed-line redaction.
2. Residual value-bearing material and allowlist eligibility.
3. Preservation of technical meaning and format.

## Findings

### Medium — R9 record-type hits are not safe to blanket-allowlist

At attacked tip `e2bfbd6`, `.ufo/waves/round-17/build/ReviewSeatBreachDetect.md:68` and `:94` remain unchanged and match frozen C1 class R9. The frozen baseline population records exactly two R9 hits there; their line SHA-256 values are respectively `55572f88ea43cfbd6c87d8f28d0f9e568a2f7f3a01b59e1ae892d025d035e8eb` and `da045ab3748666daebeae8425562784a45ef7d5739c5170ea593720061a58e00`. These are record-type tokens described as observed in the transcript, not field/key names. C1 policy `frozen/c1-policy.json:15,27` defines R9 as a session-record-value class and permits allowlisting only when a hit carries no private-source value under the listed cases. Accordingly, “name-only” is not sufficient grounds to allowlist these two occurrences. The broad draft characterization at `draft-verdicts.md:8` needs this exception narrowed or the occurrences minimized. The out-of-metric triage already carries this report's session-record material as pending debt at `out-of-metric-triage.md:25`; that admission is consistent with the observed residue, but does not make the R9 hits eligible for an allowlist.

### Medium — value-bearing session metadata remains in the report

The changed path line is followed by a precise transcript-size value at `ReviewSeatBreachDetect.md:30` (post-image line SHA-256 `cae4dd3e1dd716ec28005276119886eb3604c210c470673a04998e561cae050a`). Elsewhere, `:69` asserts the presence of a sensitive record type, `:75` gives sample counts, and `:105` includes an opaque call identifier. These are values or session-specific assertions, not merely schema/surface names; their post-image line SHA-256 values are `d8c828b38bbc493d13c37489f98f258a9ee9b9e20d6dceb74672c887a8770143`, `4eaa8948f59b21f02d54fc9bcc2fa6d0efb20412c5857828da008fd5b3545c79`, and `490173be17cc9bb31f93baf6d0687cf392bf8d96717ae2ea0287a8d2312fe859`. The pending-minimization disposition at `out-of-metric-triage.md:25` accurately records this as unresolved; these lines must not be reclassified as allowlistable names or described as fully minimized. I found no routing values or per-seat retry values in this file; the retry-related mention at `:27` is a key-shape reference only.

## No finding: changed-line removal and technical meaning

The requested diff (`git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff d005cdd e2bfbd6 -- .ufo/waves/round-17/build/ReviewSeatBreachDetect.md`) exited 0 and contains one changed line, at `:29`. The original session-store path and numbered transcript basename are fully replaced; the frozen population has one R2 hit at `:29` (line SHA-256 `b7aab3a4656e93648ea475f1739bf3a9d21d5965ebc5949aad84cba9c2c6b76a`). The post-image keeps the redaction marker within the existing parenthetical, which closes on `:30`; the surrounding explanation remains understandable. The lane seat label at `:3` is not the transcript path and is within the triage's explicit lane-seat-name carveout (`out-of-metric-triage.md:14-16`). Field/key and surface names may be allowlisted only when they truly contain no copied value and satisfy the frozen policy's conditions; the record-type cases above do not.

The target is Markdown, and the diff changes no JSON file. A search for fenced JSON blocks returned none (exit 1, no matches), so `python3 -m json.tool` was not applicable.

## Residual risk and verification gaps

- C1's committed population is the frozen **before** inventory. At `e2bfbd6`, the tracked round-18 evidence inventory contains that baseline but no post-redaction C1 measurement. Thus `draft-verdicts.md:8`'s final target-zero statement cannot be independently verified from the attacked tip's committed evidence.
- Target-file SHA-256: before `d005cdd` `125f0f34bdee3811de23af6590d35c0040c8878d2a534a61d54cadf0af8cab7f`; after `e2bfbd6` `61eddeddc146fe75769c55abc19b540099030d3fa3d04a60a42b8b8503330d13`.
- No tooling was installed or updated.