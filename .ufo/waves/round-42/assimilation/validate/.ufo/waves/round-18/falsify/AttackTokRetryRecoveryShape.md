# Round-18 falsification: RetryRecoveryShape redactions

## Findings (severity order)

### High — session artifact identities remain outside the redacted source line

The requested diff has one replacement at `build/RetryRecoveryShape.md:12` (`git diff d005cdd e2bfbd6 -- .ufo/waves/round-17/build/RetryRecoveryShape.md`, exit 0). The entering line matched C1 `R1` once (session identity) and `R2` once (session-store path); the replacement matches none of `R1`–`R9`. No `R3`–`R9` token was present on that changed line. The intended path/provenance is withheld without breaking the surrounding Markdown statement.

That edit is incomplete as a privacy repair of this report. A read-only scan of the full attacked-tip blob found 14 distinct session `.jsonl` basenames, 20 mentions over 13 lines: `build/RetryRecoveryShape.md:41-44,83-84,120-122,171-177`. They are session artifact identities (some paired with record line locations), not merely field names or surface labels. The round-18 minimization rule permits only a count/class for other-session artifacts and says to withhold artifact identity; it also prohibits session-store file names (`corpus/knowledge/evidence-minimization-r18.md:26-27`). These references are not caught by the frozen C1 regexes, so a zero C1 class count does not clear them. The names are intentionally not reproduced here.

### Medium — name-only allowlist rationale is too broad without provenance

Name-only schema and record-class mentions are not automatically equivalent to private values, and can be retained when they are publicly documented or expressly covered by a contract. However, the L1 triage's broad name/aggregate disposition (`.ufo/waves/round-18/out-of-metric-triage.md:26`) cites the round-17 closure's finding about the separate `seat-live-final.json` status-metadata projection (`corpus/lessons/round-17-verifier-spotcheck.md:333-336`); that finding does not establish a blanket allowlist for other reports or for session artifact identities. The current minimization rule permits session-record field names from public documentation and aggregate counts, while forbidding field values (`corpus/knowledge/evidence-minimization-r18.md:24,29`). `build/RetryRecoveryShape.md:51-78` presents its schema as observed from the session corpus; the report gives no public-document provenance for those field names. [INFERENCE] The names may be public elsewhere, but that is not established by the cited closure or this report. Treat field names as allowlistable only with that public/contract provenance; record-type/class labels and surface names may remain only when they disclose no artifact identity or value.

## No defect found in the changed line or value redaction

- In the immediate hunk neighborhood (`:9-16`), the only C1-token hit was the old line 12; adjacent content is unchanged and has no session-record or routing-value assignment.
- The whole-file C1 `R1`–`R9` scan at `e2bfbd6` found zero matches. No routing-table keys/values were found (`R8` zero). The report states that text values for the observed session fields were not read, and the retry histogram and epoch range are withheld (`:63,75-78,213-215`). Remaining numerical material is aggregate corpus/cardinality/classification data, not individual per-seat retry values; aggregates are permitted when accompanied by their denominator (`corpus/knowledge/evidence-minimization-r18.md:24,29`).
- The value-histogram and epoch-range withholding markers at `:63` and `:78` are unchanged between `d005cdd` and `e2bfbd6`; the diff does not substantiate that those particular values were newly redacted this round. Their values were already absent at the entering tip.
- The sole changed file is Markdown; no JSON changed, so `python3 -m json.tool` was not applicable. No code/callsite review, LSP request, tests, or external URLs were involved.

## Verification and provenance

Read-only commands, all exit 0:

- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff d005cdd e2bfbd6 -- .ufo/waves/round-17/build/RetryRecoveryShape.md` — one removed and one added line, hunk at line 12.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show d005cdd:.ufo/waves/round-17/build/RetryRecoveryShape.md`
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show e2bfbd6:.ufo/waves/round-17/build/RetryRecoveryShape.md`

Whole-file SHA-256 provenance: entering blob `66001c196e9e808f1b344e73195a6298619972c75d3fc31e88aa7adebe8cfc22`; attacked blob `ecd6dc7718cc33d16fc3a263cffb7801deb6215bde26dabaf6bf60d3de8735b9`. The private identifiers themselves are not copied into this report.