# ScribeKnowledgeMinimization — round 18 scoped findings

Seat: MoriR18Recovery.ScribeKnowledgeMinimization (leaf; no dispatch). Base read: `d005cdde0e009dea6c0cc29b37163de536528658`. Scope: draft `corpus/knowledge/evidence-minimization-r18.md` (not written to the lane; full draft in section 3).

## 1. Ground read

- Contract: `.ufo/waves/round-18/contract.md` (C1 retention gate; repair item 1 routes `corpus/lessons/round-17-verifier-spotcheck.md:390-397`).
- Policy: `.ufo/waves/round-18/frozen/c1-policy.json` (policy_sha256 `db06e9810bbfd243fb0a753a46960573df39083ea90174ce463cf2a0ab523128`, matches the field in `c1-population.json`). Classes R1–R9; adjudication rules (a) instruction/boundary statement naming a surface without contents, (b) field or key name inside lane tool code, a contract or a synthetic fixture, (c) non-author file recorded as retained-by-non-author. Every other hit is redacted.
- Frozen population: `.ufo/waves/round-18/frozen/c1-population.json` (file sha256 `392c5ab49df3b019bab57ead013a4066cbdb9ad4e06bc7abb2f0166a97e251a2`), summary: hits 119, non_author 3, must_redact 40, files 28, metric_before 116.
- Gate: `tools/mori-retention-gate.py` does **not** exist yet at the lane tip (glob of `tools/mori-retention-gate*` returned nothing). Every gate reference below is to the contract interface, not to observed behaviour. [INFERENCE] until the executor's selftest and scan run.
- Source placeholders: S0xx entries for OWASP Logging Cheat Sheet ("Data to exclude"), NIST SP 800-122 (minimization), OpenTelemetry ("Handling sensitive data"). This seat did **not** open them; their wording is not relied on. Mapping of each source to a rule below is [INFERENCE] until the source-opening seats commit receipts. The existing registry `corpus/SOURCES.md` already uses numeric IDs (48 rows beginning `| S0` at d005cdd); the placeholders must be replaced by the registrar's numbers.

### Population by class at base d005cdd (counts only, computed by `grep -o` on the frozen population file)

| Class | Name | Hits |
|---|---|---|
| R1 | session_identity | 22 |
| R2 | session_store_path | 30 |
| R3 | tool_output_artifact | 9 |
| R4 | private_document | 3 |
| R5 | shell_history | 4 |
| R6 | privileged_config | 6 |
| R7 | operator_config_ref | 13 |
| R8 | routing_table_key | 11 |
| R9 | session_record_value | 21 |
| total | | 119 |

The three `must_redact_paths` files hold 40 of the 119 hits (18 + 17 + 5). The non-author lesson file holds 3 (not counted in the metric). The class tally sums to 119, matching `summary.hits`.

## 2. Findings (gate-side, for L1 to decide; none were fixed by this seat)

1. **Frozen policy self-hits at the measured round-18 commit.** `c1-policy.json` itself contains class-matching text on four lines (counted with `grep -cE` against the frozen regex text: R2 1, R5 1, R6 1, R8 1). These lines are class definitions, not private values, so rule (b) is the only candidate adjudication, and the policy file is not in `non_author_paths_glob`. These paths postdate the base, so the d005cdd population does not contain them; they affect only the "after: 0" target. Any gate source that embeds the same regex text will self-hit the same way [INFERENCE]; expect allowlist rows keyed by `line_sha256` for `tools/mori-retention-gate.py` and its fixtures.
2. **Public-source quotes have no adjudication rule.** Rules (a)–(c) do not cover a quote from an external document. A quoted public line that contains a class token would be "redacted" under the frozen rule. Replacement: quote only token-free phrases, or paraphrase with the source ID. Policy change would require L1 approval; not proposed here.
3. **Committed line digests of short lines.** The frozen population file commits 119 `line_sha256` values, 40 of them for lines in the three routed files. A SHA-256 of a short or predictable line can be confirmed by guessing [INFERENCE: not measured]. L1 should decide whether digests of routed-file lines are acceptable provenance or should be replaced by counts plus file-level digests.
4. **Regex-only recall.** The policy's own known limit stands: classes are a recall floor. Private context without these tokens is found only by a reading sweep, which this seat did not run.

## 3. Draft entry — `corpus/knowledge/evidence-minimization-r18.md` (not written)

```
source: S0xx (OWASP Logging Cheat Sheet, "Data to exclude") — placeholder pending registrar ID; S0xx (NIST SP 800-122, minimization of personally identifiable information) — placeholder; S0xx (OpenTelemetry, "Handling sensitive data") — placeholder; lane policy .ufo/waves/round-18/frozen/c1-policy.json, sha256 db06e9810bbfd243fb0a753a46960573df39083ea90174ce463cf2a0ab523128.
verified-at: 2026-10-21 — policy and frozen population read at base d005cdd (counts only); gate not yet built; the three source pages were not opened by this entry's author; claims about their wording are pending their source-opening receipts.
recheck: TMPDIR=<fresh-empty-dir> python3 tools/mori-retention-gate.py --selftest ; python3 tools/mori-retention-gate.py scan --repo . --rev d005cdde0e009dea6c0cc29b37163de536528658 --policy .ufo/waves/round-18/frozen/c1-policy.json --expect-population .ufo/waves/round-18/frozen/c1-population.json
```

# Evidence minimization for committed observability — round 18

## Ground and decision rule

A committed item must support a stated claim. Mori commits the claim's support — a count, a class identity, a digest, a lane-relative path, a public-source quote or a synthetic fixture — and never the observed text it was derived from. Everything else is minimized. The gate is a recall floor over the frozen classes R1–R9, not a privacy proof; reading sweeps find what the classes miss and are recorded separately.

## Decision table A — may commit

| Evidence class | Committed form | Gate that checks it |
|---|---|---|
| Counts (per class, per file, totals) with revision and denominator | integers, one line per class | `scan` summary reproduces the frozen population |
| Class identifiers and names (R1–R9) | id plus name | scan emits class only, never matched text |
| SHA-256 of a whole file, policy or ledger | hex digest | digest recorded; digest of a single short line is not a substitute for its content (see caveat) |
| Lane-relative paths of tracked files | path beginning at the lane root | R2 and R4 must not match |
| Public-source quotes | short phrase, source ID, URL and pinned revision | quote must match no class; otherwise paraphrase |
| Synthetic fixtures | generated under `$TMPDIR` by `--selftest`; committed fixtures use tokens no class matches | rule (b) for field or key names in tool code and contracts only |

Caveat: a digest of a short or predictable line can be confirmed by guessing; prefer counts and file-level digests for any line derived from private material.

## Decision table B — must minimize

| Evidence class | Replacement form | Never committed | Gate |
|---|---|---|---|
| Other-session output (numbered tool-output artifact) | count, class id, line digest | artifact name, line text | R3 |
| Session identity (dated session directory or transcript name) | "one session observed" with an ordinal | directory or transcript name, any hash of it | R1 |
| Session-store path below the store root | "session store path withheld" | the path | R2 |
| Operator personal documents | "operator document withheld" | the path | R4 |
| Shell history | "not read" statement | path or content | R5 |
| Privileged host configuration | "not read" statement | name or content | R6 |
| Operator configuration reference (file or line) | "operator configuration present; values withheld" | file reference, line number | R7 |
| Routing table keys with values | "routing configuration present; keys and values withheld" | key names, values | R8 |
| Session-record value outside the allowlist | count of records with a field outside the allowlist | field value; field name in prose | R9 |

Field and key names are allowed only inside lane tool code, a contract or a synthetic fixture (rule b). In prose they are minimized.

## Adjudication

A population hit may be allowlisted only under rules (a), (b) or (c) of the frozen policy. A hit in a `must_redact_paths` file cannot be allowlisted (`allowlist_forbidden`). A stale allowlist row is a warning. Public-source quotes are not covered by any rule; quote token-free text only.

## Limits

- The gate is regex-based; private context without the tokens is outside the metric.
- Policy-file and gate-source self-hits require explicit rule (b) rows; they are not exempt by location.
- Source wording for the three external sources is pending their receipts.
```

## 4. Commands run (all read-only; no tool installed or updated)

- `git -C` reads were not needed; all lane access was `read`, `glob`, `grep`, and `bash` counts on committed frozen files.
- `grep -o '"class": "R[0-9]"' ... | sort | uniq -c` — exit 0; class counts above.
- `grep -o '"path": "..."' ... | sort | uniq -c` — exit 0; path counts used only for the routed-file totals (not reproduced).
- `grep -c` with class regex text against `c1-policy.json`, `contract.md`, `c1-population-cmd.py` — exit 0 for lines with counts, exit 1 where the count is zero (expected); counts in section 2 item 1.
- `sha256sum` of `c1-policy.json` and `c1-population.json` — exit 0.
- `ls` of `round-18/build/` — exit 0; files present there belong to other seats and were not read or modified.

Not run: no selftest (gate absent), no journal query, no transcript or session-store access, no `~/.omp` reads, no pacman transactions, no writes outside this report.

## 5. Tooling

No tools installed or upgraded by this seat. Channel check: none needed; the scope is read-only.

## 6. Out of scope / handed off

- Writing `corpus/knowledge/evidence-minimization-r18.md` (not requested; draft only).
- Replacing the S0xx placeholders with registrar IDs and verifying source wording (source-opening seats).
- Decision on findings 1–3 (L1).
- Exposure assessment of already-pushed history (operator/kagi-owned, per contract).
