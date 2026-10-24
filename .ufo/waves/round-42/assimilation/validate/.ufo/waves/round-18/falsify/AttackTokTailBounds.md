# Round-18 falsification: TranscriptTailBounds token redactions

## Findings by severity

No actionable defect found in the two changed lines of `.ufo/waves/round-17/build/TranscriptTailBounds.md`.

## Changed-line review

| Line | Before / after classification | Evidence and technical effect |
|---|---|---|
| 8 | One pre-edit C1 R2 (`session_store_path`) hit; zero R1–R9 hits after the edit. | Old-line SHA-256: `77cac0d6bf17e2c329ba84c82f79d9625cdaa73df157a8ce17399301fe1ea2fe`; new-line SHA-256: `a258d62f00f9bdd282a5400341e73e2915eb4a6fa47a24ae808f9ce8a77ffb55`. The question still identifies the subject as JSONL files under a withheld session-store root; its exact search target is intentionally unreproducible. |
| 22 | One pre-edit C1 R2 (`session_store_path`) hit; zero R1–R9 hits after the edit. | Old-line SHA-256: `cf006717e795e4d63e46bc26ea60c8d7d4f99c11039f46d0162fc930e421d38f`; new-line SHA-256: `ea21b8f3cb434250504ba600ef49ae844a2b2a37e6ec97acf17e607de475793c`. The line still conveys the intended working-directory role; the exact directory is withheld. No command text was changed. |

For the neighboring ranges `:7-9` and `:21-23`, the only pre-edit frozen-class match was the R2 token on the edited line. No adjacent routing-value, session-record-value, or retry/attempt-value pattern matched; no such pattern remains after the edit. The edit did not alter JSON: the changed artifact is Markdown, so `python3 -m json.tool` was not applicable.

## Name-only allowlisting judgment

The narrow principle is acceptable, not a blanket exception. Frozen policy `frozen/c1-policy.json:27` requires that the line carry no value copied from a private source and limits eligible cases to the specified instruction/contract surface names, structural field/key names in lane code/contracts/synthetic fixtures, or routed non-author files. A bare field/record-type/surface name can therefore be allowlistable only when its line and context meet those conditions; a structural name must not excuse a private value elsewhere on the same line.

The L1 draft (`.ufo/waves/round-18/draft-verdicts.md:8`) describes 55 intermediate hits as name-only and says their allowlist rows were pending. The draft does not provide those per-row line hashes/context, and the attacked tip's tracked wave-18 path inventory has no dedicated allowlist artifact. I therefore accept the *conditional rule*, but cannot independently approve the 55-row classification or its eventual application from this scoped evidence. This is a verification gap, not a defect in the two token edits.

## Residual risk and verification gaps

- Exact target-directory reproducibility is intentionally lost at lines 8 and 22; semantic scope remains understandable.
- The per-row proof for the L1's claimed name-only allowlist candidates was not available in the inspected wave-18 artifacts.
- No `lsp` device route was exposed to this seat, so LSP status/references/definition/diagnostics were unavailable; no grep-based semantic claim is made.

## Evidence / commands

- Read-only `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff d005cdd e2bfbd6 -- .ufo/waves/round-17/build/TranscriptTailBounds.md`: exit 0; 2 additions and 2 deletions. Diff lines were classified in memory; raw changed text is not reproduced here.
- Read-only `git show d005cdd:<path>` and `git show e2bfbd6:<path>` for the target file: exit 0; used only to classify the changed and neighboring lines and compute the line hashes above.
- Read-only `git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree -r --name-only e2bfbd6 -- .ufo/waves/round-18`: exit 0; no dedicated allowlist artifact appears in that wave directory's tracked paths.
- `command -v lsp || true`: no executable path was returned (wrapper exit 0); the exposed tool inventory also supplied no `lsp` device.
- No tools were installed or updated. No JSON file was changed, so no JSON validation command was run.