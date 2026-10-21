# AttackTokConformanceAudit — L1 redaction review

Scope: read-only comparison of `.ufo/waves/round-17/falsify/ConformanceAudit.md` from `d005cdd` to `e2bfbd6`, with review of the changed rows and adjacent rows. Tip blob SHA-256: `34f7a9dbb0eeed78505dd674fb0c6720286ce473f06780f1c6ec62a99cc07cc9`. The counts below classify the reviewed tip blob; no private text is reproduced.

## Findings (severity order)

### High — Name-only mentions are not a blanket C1 allowlist category

`.ufo/waves/round-17/falsify/ConformanceAudit.md:43-44` retains four C1 R9 name-token matches: two on each row. These are field/record-type names, not field values. The redaction did remove the concrete examples and config-location details from the changed rows, and no routing/model strings or per-seat retry values remain in these rows or the adjacent V13 row (`:48`). However, the frozen rule at `.ufo/waves/round-18/frozen/c1-policy.json:27` permits names only in the listed contexts (instruction/boundary/contract surface names; field/key names in lane code, a contract, or a synthetic fixture; or qualifying non-author files the lane may not edit). This historical findings table is not a code, contract, or synthetic fixture, and it is outside the declared non-author glob (`c1-policy.json:23-25`). The out-of-metric triage's broader name-only rationale (`out-of-metric-triage.md:25-28`) therefore cannot by itself authorize those R9 hits. Treating such rows as allowlisted would make the frozen C1 result inconsistent with its own admission rule; the draft's name-only rationale at `draft-verdicts.md:8` is not sufficient evidence for a clean metric.

### Medium — A neighboring session identity remains

The unchanged adjacent V3 row at `.ufo/waves/round-17/falsify/ConformanceAudit.md:38` still carries one session-identity token and a session-specific path. This is a human-review session-identity finding (R1 family; the token shape is not a match for the frozen R1 regex), so the frozen metric does not catch it. It is directly adjacent to the changed V4 row and falls under the triage's broader session-identity scope (`out-of-metric-triage.md:10-13`). The changed V4 row (`:39`) itself does remove its session-name fragment and account identity; no identity value remains there.

### Medium — V11 redacts the artifact number but leaves sensitive surface tokens

At `.ufo/waves/round-17/falsify/ConformanceAudit.md:46`, the concrete tool-log number is replaced by a generic filename pattern, and the technical finding remains understandable. The same changed row still contains one R5 shell-history token and one R6 privileged-configuration token, plus a generic store-root location (no session-child path; therefore not a frozen R2 regex hit). These are surface names without contents, but the frozen policy does not make every prose mention allowlistable: this row is a findings-table statement, not one of the instruction/contract/code/fixture contexts in `c1-policy.json:27`. The generic filename pattern itself exposes no concrete artifact number.

## Changed-line and meaning check

- V4 (`:39`): the session and account identities were generalized; no actual invocation UUID or identity value is present. Remaining host-event facts do not disclose those identity tokens.
- V8 (`:43`): example values are withheld; the row still explains which fields were improperly read, so the technical claim remains intact. Only the R9 name tokens noted above remain.
- V9 (`:44`): config location/line details and concrete values are withheld; the technical claim remains intact. Only R9 name tokens remain; no route/model value or retry value is present.
- V11 (`:46`): the numbered artifact is generalized without changing the finding's meaning; residual R5/R6 surface tokens are listed above.
- The diff changes Markdown only; the table rows remain structurally readable. No JSON file was changed, so `python3 -m json.tool` was not applicable.

## Residual risk and verification gaps

This review covered the changed rows and their nearby rows, not a complete privacy sweep of all 145 lines. In particular, the residual identity in V3 is outside the diff hunk's edits and is not represented by the frozen R1 regex. The name-only decision requires the frozen context test, not blanket acceptance by token type.

No `lsp` device/route was exposed in this session, so LSP status, references, definition, and diagnostics could not be run. No grep was used as semantic proof. No build, tests, JSON validation, or other runtime verification was run; no tools were installed or updated.

## Read-only command evidence

- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff d005cdd e2bfbd6 -- .ufo/waves/round-17/falsify/ConformanceAudit.md` — exit 0; one Markdown file, four changed rows.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show e2bfbd6:.ufo/waves/round-17/falsify/ConformanceAudit.md | sha256sum` — pipeline exit 0; digest recorded above.
