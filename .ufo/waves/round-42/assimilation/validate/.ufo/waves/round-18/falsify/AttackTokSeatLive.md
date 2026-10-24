# AttackTokSeatLive — round-18 wave-2 falsification

**Scope:** read-only diff of `.ufo/waves/round-17/evidence/seat-live.json` from `d005cdd` to `e2bfbd6`; no repository mutation. **Axes:** private-token completeness, value minimization, JSON/technical fidelity.

## Findings

### High — the stdout redaction makes the evidence JSON invalid

`seat-live.json:23` replaces the session-store value inside the JSON-encoded `stdout`, but the byte replacement also removed the backslash escaping the inner closing quote. The replacement leaves that quote bare; the outer `stdout` string ends early and parsing fails at the following escaped property. The old file parsed successfully; the new file does not. The byte comparison found 113 removed characters (the 112-character path plus one escape backslash) replaced by the 29-character placeholder.

- `python3 -m json.tool`: `d005cdd` exit **0**; `e2bfbd6` exit **1**, `Expecting property name enclosed in double quotes` at line 23, column 166833.
- New line 23 SHA-256 (UTF-8 line bytes, LF excluded): `7ee29c9398cd1ca0c1d93f1c649b81cad070b7b23c4bdddada8bd356a6fa4919`.
- The replacement in `seat-live.json:9` is a valid JSON string and fully withholds its path; new line SHA-256: `fe2611236379ef68e82bc05e3dfb5e509b5b2901632e66337f22cc6b308749f7`.

**Recommendation:** retain the redaction while preserving JSON string escaping (or parse and re-serialize the outer JSON). Do not treat the current `e2bfbd6` evidence file as consumable JSON.

### High — line 23 retains value-bearing session records; this is not a name-only projection

The frozen population lists R1 and R2 hits at `seat-live.json:9` and `:23` (four hit rows total; `.ufo/waves/round-18/frozen/c1-population.json:487-509`). Both occurrences are removed at `e2bfbd6`; a whole-file check for the frozen R1-R9 patterns, loose UUIDs, and email-shaped values found no remaining matches. Thus the targeted identity/path redactions are complete for those checked patterns. The residual values are a separate issue: all other stdout bytes remain on line 23.

In the baseline stdout structure, the line contains 469 seat records. The retained fields include 468 string-valued per-record `model` fields (7 distinct strings), 90 integer-valued `retries` fields (379 null), 469 boolean `retry_exhausted` fields, and 469 integer `terminal_ms` fields. Provider/model values are present per record, not only as aggregate labels. The exact values were not reproduced. Whether those observed per-record model strings equal configured routing assignments is **[INFERENCE]**; the existence of per-record model strings and retry/time values is directly observed.

This cannot be justified as name-only retention: the R18 minimization table permits field names and aggregate counts, but lists model strings and per-seat retry values in the never-commit column (`corpus/knowledge/evidence-minimization-r18.md:26,29`). The policy's allowlist rule only permits a hit where the line carries no copied private value (`.ufo/waves/round-18/frozen/c1-policy.json:27`); its recall-floor warning also makes zero regex hits insufficient as a privacy conclusion (`:29`). The R9 regex is narrower than these flat serialized fields (`frozen/c1-policy.json:15`), so the absence of an R9 match does not settle them.

The L1 triage rejects this family as covered by record names, key names, provider/model and class tokens (`.ufo/waves/round-18/out-of-metric-triage.md:26`). That rationale is over-broad for `seat-live.json:23`: the line contains values attached to the names. The triage's same-round lane-work exception (`out-of-metric-triage.md:14-15`; `evidence-minimization-r18.md:38-40`) does not by itself convert these value-bearing fields into name-only data.

**Name-only ruling:** retaining actual field names, the single record-type token, and lane surface/prefix names is reasonable when they occur without copied private values and satisfy the frozen allowlist rule. In this data line, 466 of 469 `key` values are prefix/seat name pairs and are name-like; the grouped `by_prefix`/`by_provider_model` counts are aggregates. Those facts do not authorize the separate per-seat model, retry, and timing values. The cited prior closure says the final artifact is a safe status projection (`corpus/lessons/round-17-verifier-spotcheck.md:333-336`), but the referenced `.ufo/waves/round-17/evidence/final/seat-live-final.json:22` itself has 469 seat rows, including 468 model strings, 90 integer retry values, and 469 terminal-time fields (line SHA-256 `21d0fc01db69ae34e2fe2fe0f810b22409a2c3f48dfeffc0d4888e9d5ed94cf8`). The prior description therefore does not establish that this retained projection is name-only under the R18 rule.

## Residual risk and verification gaps

- No R1-R9, UUID-shaped, or email-shaped match remained in the new target during the in-memory read-only scan. An arbitrary personal-name match was not independently established; no identity source was consulted.
- No source caller or definition changed in this data-only diff; no LSP caller/definition/diagnostics query was applicable. No build, test, or lint command was run.
- The C1 token scan does not validate that the per-seat stdout values are minimized; the R18 reading-sweep rule remains necessary.

## Commands and observed results

- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff d005cdd e2bfbd6 -- .ufo/waves/round-17/evidence/seat-live.json` — completed, exit **0**; one file, two changed lines (two insertions/two deletions).
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show d005cdd:.ufo/waves/round-17/evidence/seat-live.json | python3 -m json.tool > /dev/null` — exit **0**.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show e2bfbd6:.ufo/waves/round-17/evidence/seat-live.json | python3 -m json.tool > /dev/null` — exit **1**, parse failure as above.
- Read-only `git show`/in-memory structural comparison of target, frozen population and cited final projection — successful; no probe files or scratch outputs written.
