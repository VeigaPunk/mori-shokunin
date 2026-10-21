# Round-17 build-report privacy sweep — outside the frozen C1 metric

## Scope and method

Read the round-18 contract and its frozen C1 policy, then read all 11 requested round-17 build reports in full using line-ranged reads. The C1 policy explicitly describes its regular expressions as a recall floor and requires this separate reading sweep (policy `:27-29`). Findings below are location-only: no private excerpt, value, credential, transcript text, or raw tool output is reproduced.

Scoped searches were limited to the 11 requested reports. Search results showed no R4–R8 tokens; the scoped credential-indicator search found only explicitly synthetic fixture sentinels and a report of a credential-bearing record's presence, not a credential value. The specialized grep device did not expose numeric exit codes. `wc -l` and `sha256sum` over the 11 target reports and the three comparison reports completed with exit code 0. No external URL was accessed by this sweep; no tool was installed or updated.

## Frozen-class coverage in the 11 target reports

Counts are literal matching line occurrences against `frozen/c1-policy.json`, not the full C1 population metric. One line may match more than one class.

| Frozen class | Matching lines | Count |
|---|---|---:|
| R1 | `SeatNaming.md:15` | 1 |
| R2 | `ReviewSchemaDrift.md:9`; `ReviewSeatBreachDetect.md:29`; `SeatNaming.md:15` | 3 |
| R3 | `SeatNaming.md:33` | 1 |
| R4 | none | 0 |
| R5 | none | 0 |
| R6 | none | 0 |
| R7 | none | 0 |
| R8 | none | 0 |
| R9 | `ReviewSeatBreachDetect.md:68,94` | 2 |

Total: 7 class occurrences across 6 unique lines. The partial timestamped session identity in `ReviewSeatBreachDetect.md:29` is abbreviated, so it does not satisfy R1's complete pattern; the same line does match R2. The manually discovered private material below is not represented by these literal counts.

## Manual findings and minimum redaction

Manual line counts include lines already caught by a frozen class. Each recommendation is a minimal removal or generalization, not a proposed report rewrite.

- `.ufo/waves/round-17/build/ReviewSchemaDrift.md:9,13,22` — **M-SESSION-HEADER, 3 lines; R2 hits `:9`.** Retains an observed session-header value, repeats it in the recommendation, and records the query that emitted it. The concrete value is outside the frozen session-record patterns. **Redact:** remove the observed value and session-store locator; state only that header validation needs synthetic supported/unsupported-version fixtures.

- `.ufo/waves/round-17/build/ReviewSeatBreachDetect.md:24-25,46-57,59-61,141-152,195-205` — **M-TOOL-TRACE, 40 lines.** These contain specific prior-seat command/path fragments, temporary-path and process identifiers, host-read examples, tool-call/message locators, and paraphrases of other sessions' tool activity. They are not numbered tool-log names covered by R3. `:52,147` contain only generic package-query/transaction classification, not the PacmanActorTrace event finding. **Redact:** replace the concrete examples, identifiers and command-shaped fragments with abstract breach categories; retain only the rule and its limits.

- `.ufo/waves/round-17/build/ReviewSeatBreachDetect.md:29-33` — **M-SESSION-ID, 5 lines; R2 hit `:29`, R1 miss at the abbreviated identity.** Retains a partial session-directory identity, byte count and commands used to inspect a session transcript. **Redact:** remove the locator, size and query details; retain only a non-attributable method summary.

- `.ufo/waves/round-17/build/ReviewSeatBreachDetect.md:67-80,93-95` — **M-SESSION-RECORD, 17 lines; R9 hits `:68,94`.** Retains an observed session-record/type inventory, tool-name/schema observations, and the presence of a credential-bearing record. No credential value is present. **Redact:** remove the observed inventory and record-presence assertion; keep only abstract parser allowlist requirements.

- `.ufo/waves/round-17/build/ReviewSpotcheckRouting.md:25,36` — **M-DISPATCH-HISTORY, 2 lines.** Retains exact pre-dispatch receipt/attempt chronology and a statement that an unscoped search surfaced excluded session-record excerpts. These are private operational/session-history facts outside the frozen patterns; the excerpts themselves are not repeated. **Redact:** generalize the timing to ordering only and remove the search-exposure detail.

- `.ufo/waves/round-17/build/SeatFixtures.md:66-70,72,183-186,188-189,516-517` — **M-RETRY-MODEL, 14 lines.** Synthetic fixture labels and expected behavior repeat the distinctive provider-specific retry scenario summarized in OmpRetryConfig; direct copying is not proven, but the overlap is observable. **Redact:** replace provider/model and retry-message identifiers with neutral synthetic labels while keeping the class assertion.

- `.ufo/waves/round-17/build/SeatTool.md:98` — **M-RETRY-MODEL, 1 line.** The selftest description repeats the provider/model-specific retry scenario and its diagnostic details summarized in OmpRetryConfig. **Redact:** use a neutral provider/model placeholder and a generic retry fixture description.

- `.ufo/waves/round-17/build/SeatNaming.md:7-11,15,17-18,20-33,37-50,52-57,59-71,73-111,113-228,232-245,249-261,265-277` — **M-SESSION-CORPUS, 250 lines; R1/R2 hits `:15`, R3 hit `:33`.** Retains a live session-store census: session identities and paths, corpus and subdirectory counts, timing/drift, tool-log naming, peer/roster joins, per-prefix and per-seat inventories, and terminal/incomplete-state observations. `:17` also records reading a field outside this wave's transcript-field allowlist. **Redact:** remove the live census, identities, per-seat/prefix tables, timestamps, log names and observed status correlations; preserve only a synthetic filename grammar and abstract prefix caveat.

- `.ufo/waves/round-17/build/SentinelJjSandbox.md:25-33,52-57,59-62,75-82,92-95,193,200-204` — **M-OPERATOR-CONFIG, 37 lines.** Retains local jj/git configuration identifiers and values, account/author identity facts, remote-origin settings, global configuration/helper-key facts, session environment values, sandbox-to-lane reachability, a prior configuration-store count, and command/probe timing. The helper configuration key is disclosed, but no credential/helper secret is present. **Redact:** remove actual config IDs/paths, identities, remote details, ambient environment and host counts/times; retain generic isolation requirements only.

## Repeated-fact cross-checks

Comparison sources were read only as needed to classify overlap; hashes are supplied for provenance without repeating their content.

- `PacmanActorTrace.md:11-39` (SHA-256 `b30443665d48a32bb49dfa501eef8ec594a3ab03b299bf9e84d0904b6512d1bf`): **no repeated transaction/actor/tool-output finding** in the 11 targets. The generic allowed package-query examples in `ReviewSeatBreachDetect.md:52,147` are not the same fact.
- `OmpRetryConfig.md:11-28,34-41` (SHA-256 `6428d1154253d54788bb5dccaec71efb0f80c610f92c6db52e99a4a81b3cf7f4`): **overlap in two target files** — `SeatFixtures.md` at the lines listed above and `SeatTool.md:98`. They repeat the distinctive provider-specific retry case and related model/retry details. The fixtures are described as synthetic; the overlap is observed, while direct derivation from that report is **[INFERENCE]**.
- `SessionExitCorrelation.md:11-18,40-56` (SHA-256 `fcacbcc60ad8b4c8c30c074b1005d6993d653a9c9d8d0ca941028fc69daf6765`): **dataset-level overlap in `SeatNaming.md`** at the lines listed above: both report the same live session corpus/structure and terminal-state domain. `SeatNaming.md` does not repeat the disposal-marker cross-tabulation itself. Direct borrowing is **[INFERENCE]**.

## Clean reports and synthetic-token determination

Clean of private-context retention for this sweep:

- `.ufo/waves/round-17/build/ReviewScorecardRubric.md`
- `.ufo/waves/round-17/build/ReviewSkillRows.md`
- `.ufo/waves/round-17/build/ScorecardAxisCheck.md`
- `.ufo/waves/round-17/build/SeatGate.md`

Their references to contract fields, tool schemas, scorecard/project history or synthetic test behavior do not expose private session values, operator config values, personal-document/history locations or credentials. `SeatFixtures.md:212,233` and `SeatTool.md:108,337` describe explicitly fake fixture sentinels only; no actual credential or token value was observed there. `ReviewSeatBreachDetect.md:69` discloses a credential-bearing record's presence, as noted above, but not its value.

## Evidence inventory

The following SHA-256 values bind the reviewed report snapshots. “Flagged lines” are the manual line occurrences listed above; clean files have zero.

| Report | Lines read | Flagged lines | Manual class | SHA-256 |
|---|---:|---:|---|---|
| `.ufo/waves/round-17/build/ReviewSchemaDrift.md` | 22 | 3 | M-SESSION-HEADER | `5f3e244089520e0325d5580208bc6df83c2dd70b9c6f089bc0d6f285c458cdba` |
| `.ufo/waves/round-17/build/ReviewScorecardRubric.md` | 33 | 0 | clean | `d1b38b728e5bf4a4deedcc9e5bbb1587eca9f8a80a513e5906ee9afd27073233` |
| `.ufo/waves/round-17/build/ReviewSeatBreachDetect.md` | 219 | 62 | M-TOOL-TRACE; M-SESSION-ID; M-SESSION-RECORD | `125f0f34bdee3811de23af6590d35c0040c8878d2a534a61d54cadf0af8cab7f` |
| `.ufo/waves/round-17/build/ReviewSkillRows.md` | 44 | 0 | clean | `d51b61103e1363c2910257601940b8cd85df32b7cfdc487057ab8dd4188277ad` |
| `.ufo/waves/round-17/build/ReviewSpotcheckRouting.md` | 37 | 2 | M-DISPATCH-HISTORY | `2c763700161ef509611ee7a2adc8e1a8a08331a0b57f9ee30690f791ee5cc357` |
| `.ufo/waves/round-17/build/ScorecardAxisCheck.md` | 359 | 0 | clean | `3f9e651bbee47e59179cfe83fbb50810903e51d9a895b68629aa81f766882b8a` |
| `.ufo/waves/round-17/build/SeatFixtures.md` | 799 | 14 | M-RETRY-MODEL | `6c9f6525751a996d7a22bd45318ca6e294e4aadf077d87628d3769832f5b8002` |
| `.ufo/waves/round-17/build/SeatGate.md` | 528 | 0 | clean | `5091df008f35f54fb37c5e8236b79794f2136acae24c820559f8ecc6263c096a` |
| `.ufo/waves/round-17/build/SeatNaming.md` | 281 | 250 | M-SESSION-CORPUS | `b3b8a95b8e75fc38c7a47c919c2152a8b376e4fc2ead67ccbaced3967c6ebae9` |
| `.ufo/waves/round-17/build/SeatTool.md` | 449 | 1 | M-RETRY-MODEL | `0945e1e10f4b52aa2993002f97fd24a11ddbc944c03171d14d0b2cecfb679430` |
| `.ufo/waves/round-17/build/SentinelJjSandbox.md` | 208 | 37 | M-OPERATOR-CONFIG | `9c5bc34ab0747a9dc8f4b5b9f501899e7c210ec2307ee8301a8e39789249ba42` |
