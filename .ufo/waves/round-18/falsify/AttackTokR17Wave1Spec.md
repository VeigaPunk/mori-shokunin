# Round-17 wave-1 JSON redaction attack

## Findings

### High — private routing and per-seat retry detail remains in both artifacts

The lines `.ufo/waves/round-17/wave1-spec.json:70` (SHA-256 `43707315f5d440715186f48dc89cf44e161196ab26ec6d8d50d6b173ed42b083`) and `.ufo/waves/round-17/wave1-dispatch.json:522` (SHA-256 `2859c9a9de8747eee8fec409f8c33514cf4144c90f7489b23d10b9b6dba30313`) are unchanged from `d005cdd` to `e2bfbd6`. Each retains one R7 config-surface reference and one R8 field-name hit, plus two configuration-derived routing selectors and one seat-specific retry/failure detail with numeric context. The R8 field name and config surface, taken alone, could be name-only references; the selector values and retry detail make these lines more than names-only. The frozen C1 adjudication rule permits surface-only instructions without private contents, and the out-of-metric privacy definition separately includes operator routing values and session-record/retry values (`frozen/c1-policy.json:27,29`; `out-of-metric-triage.md:10-13,25-26`). The name-only rationale therefore does not justify retaining these lines as a whole. Redact/minimize those values before treating the sweep as clean. The line classifier found no literal fallback-table assignment on either line; the finding is the retained selectors and retry/failure context, not a claim that a full table is present.

### No finding — changed token redactions

Read-only diffs of the assigned files (`git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff d005cdd e2bfbd6 -- <path>`) each exited 0 and contained five changed prompt/task strings. The base lines had five R2 session-store-path hits per file and three R1 session-identity hits per file; all R1/R2 hits are absent from the corresponding tip lines. No R3/R4/R5/R6 or email marker was detected on the changed lines or their immediate tip neighbors. The retained retry field mention on the edited prompt line is a name/instruction, not an embedded per-seat value.

| File | Line | Base hit class(es) | Tip line SHA-256 |
|---|---:|---|---|
| `.ufo/waves/round-17/wave1-spec.json` | 45 | R2 | `a296d71c27f8713c7f407647a993fb1a16fee68fd789d457f55410a446ba8357` |
| same | 50 | R1, R2 | `b44b7ce0e17fea01fb0287a307ba7bbc505c2f8ee2a905a32707c42ccf655c7e` |
| same | 55 | R1, R2 | `495608b3be6ee6bc7a9d773d48b1653fce855ee294bb388d9f8253a41d4ae133` |
| same | 150 | R2 | `b2bbd129fcba83e5970c0055adc2beaf5cd4009f2436e1fff717f53e310eae93` |
| same | 255 | R1, R2 | `8fd9126010d312e1c8fcc78af490312dd6121f61447ccfa472449e0ea7cdcad6` |
| `.ufo/waves/round-17/wave1-dispatch.json` | 497 | R2 | `99da0de5061b15f9655376f4576703114d2ff8f1953f05bb7f43b5bc5bdcbc20` |
| same | 502 | R1, R2 | `bf15e437b1abdd7d0c8bafeda547d337891585279167da23613d5cf151ef59d2` |
| same | 507 | R1, R2 | `38e0050ca916d7875aa49ddaea3394e35ddafd6a0ea7525b7c5aa17e5459caa8` |
| same | 602 | R2 | `5c8f613d10bd9d793426aeefd83ab029469b1e1625b8bba51fbefaef0f57da5f` |
| same | 707 | R1, R2 | `e7ae36fdf81de859e10cbeac2e8a924d9828a207e6ca6e2753dc71cb2bec3cd3` |

The JSON object/array shape and item/task counts remain unchanged (70 each); each file has five changed prompt/task leaves. After masking the removed tokens and their withheld markers, the redacted strings preserve the original wording, except for a punctuation-only difference in two mirrored prompt/task strings. No material technical-meaning break was found.

## Name-only adjudication

The unchanged R9 hits at `.ufo/waves/round-17/wave1-spec.json:155` (SHA-256 `2eb76b4a2158d326196d7727d36cbe8c3b58ee98e8e4a58b54996fb1431fa73d`) and `.ufo/waves/round-17/wave1-dispatch.json:607` (SHA-256 `b1b281ae8031fcdc0d5d5e3cedb2655dda37c328f3ef6c98c3a13fbd7d482943`) are field/record-type names only: no value assignment or session-record value was found. I agree with retaining such names narrowly where the frozen adjudication rule applies; that does not extend to the private values on lines 70/522.

## Verification and gaps

- Both assigned `git diff` commands: exit 0. Read-only `git show` of both revisions succeeded; parsed base and tip JSON for both files.
- JSON validity at `e2bfbd6`: `git ... show ... | python3 -m json.tool | wc -l` with `set -o pipefail` returned exit 0 for each file (358 formatted lines for the spec, 813 for the dispatch).
- LSP availability check (`read xd://lsp`) returned “No such tool” for this runtime; no LSP status/references/definition/diagnostics could be run. No grep fallback was used.
- Residual scope limitation: this was a targeted class/value review, not a general entity-recognition proof; unpatterned personal-identity material is not established absent. No tool was installed or updated.