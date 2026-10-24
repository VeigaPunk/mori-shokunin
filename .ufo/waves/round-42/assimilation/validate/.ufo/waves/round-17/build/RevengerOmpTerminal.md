# OMP terminal-status semantics — source review

## Axes

1. **Implementation evidence:** whether the installed OMP source is locally available and exposes these fields.
2. **C1 contract fit:** what the round-17 tool is actually specified to classify and emit.
3. **Lifecycle certainty:** whether `stopReason="error"`, `retryRecovery`, and custom `session_exit` prove a seat is permanently dead.

## Verdict

I could not establish OMP's source-level semantics for these fields. `command -v omp` resolved to `/home/vgpnk/.local/bin/omp`; `omp --version` printed `omp/18.12.3`. The resolved executable is an ELF 64-bit x86-64 file, 256,628,704 bytes, with `.bun_builtins` and `.bun` sections (`file`, `stat`, and `readelf -S --wide`). This is a compiled executable, not an on-disk source file. `pacman -Qo /home/vgpnk/.local/bin/omp` reported that no package owns it (exit 1). The project-root listing I inspected did not surface a dedicated `omp` checkout. These observations do not prove that no source exists elsewhere or that the executable contains no bundled code; I found no textual OMP implementation source from which to quote code lines.

The `xd://lsp` request returned “No such tool” and the mounted-tool inventory did not expose an LSP device. No LSP definitions/references are therefore available. I did not read any OMP transcript records or inspect their contents.

## Reconstructed contract available here (lane contract, not OMP implementation evidence)

- The proposed C1 parser considers only JSON records with `type == "message"` and a dictionary-valued `message`; it skips every other record type, explicitly including `custom`. Its terminal record is the last such message in the bounded tail (`.ufo/waves/round-17/contract.md:37-39`). Thus the contract does not inspect or give special meaning to a custom record named `session_exit`.
- For the terminal assistant message, `stopReason == "error"` is classed as `dead_rate_limit` when the stated status/text markers match, otherwise as `dead_quota` when its markers match, otherwise as `dead_error_other`; rate-limit matching precedes quota matching (`.ufo/waves/round-17/contract.md:42-51`). This is the C1 classification rule, not a quoted OMP source rule.
- C1's `retry_exhausted` output is derived from `errorMessage` beginning with `Retry budget exhausted`; it extracts the retry count from `after N retries` and the digits from `(type=NNNN)`. Its specified output contains no `retryRecovery` field (`.ufo/waves/round-17/contract.md:52-56`).
- The contract explicitly limits terminal status to the *last observed* state, not proof that a session will never resume (`.ufo/waves/round-17/contract.md:65-67`).
- The binding transcript restriction permits only selected record fields and the `retryRecovery` key shape, while forbidding content, usage, and other fields (`.ufo/waves/round-17/wave1-context.txt:9`). No transcript observations were needed or made for this source review.

## OMP field meanings and divergence

- `message.stopReason == "error"`: **[INFERENCE]** the name and C1 branch indicate an assistant message ended on an error path. I found no installed source evidence that this value alone means the whole OMP seat/session is permanently terminated. The C1 contract's last-observed-state warning is consistent with not treating it as permanent-death proof, but that warning is a lane contract, not OMP behavior evidence.
- `message.retryRecovery`: **[INFERENCE]** no semantic expansion is justified from the key name alone. The source review did not establish its type, values, whether it records an attempted retry versus recovered result, or whether it is authoritative for final status. C1 currently does not consume or emit it; whether that omits meaningful recovery state is unverified.
- Custom `session_exit`: **[INFERENCE]** no source evidence establishes whether this is a definitive termination event, a notification, or another lifecycle marker. C1 skips custom records, so it would classify from the preceding/final message regardless of this event; whether that is correct relative to OMP's lifecycle semantics is unverified.

The actionable divergence is therefore an evidence gap, not a proven C1 defect: C1 is specified to ignore both `retryRecovery` and custom records, but the installed OMP semantics needed to validate those omissions were unavailable. No inference above should be treated as source-confirmed.

## Investigation commands and outcomes

- `command -v omp; command -v omp >/dev/null && omp --version 2>&1 | head -c 400` — resolved `/home/vgpnk/.local/bin/omp`; printed `omp/18.12.3`. The tool output did not expose a per-command exit status.
- `readlink -f /home/vgpnk/.local/bin/omp; file /home/vgpnk/.local/bin/omp; stat -c '%F %s bytes %A %n' /home/vgpnk/.local/bin/omp` — resolved path, ELF metadata, and size above; per-command exit statuses were not surfaced.
- `readelf -p .comment /home/vgpnk/.local/bin/omp` and `readelf -S --wide /home/vgpnk/.local/bin/omp` — returned compiler-comment and section information, including `.bun_builtins` and `.bun`; per-command exit statuses were not surfaced.
- `pacman -Qo /home/vgpnk/.local/bin/omp` — exit 1, “error: No package owns …”.
- `go version -m /home/vgpnk/.local/bin/omp` — exit 127, `go` was not installed; this did not yield source metadata.
- `llvm-dwarfdump --verify /home/vgpnk/.local/bin/omp` — reported “No errors”; the tool output did not surface an exit code. The attempted `llvm-dwarfdump --debug-info --max-depth=0 ...` source-path query exited 1 because this installed tool does not support `--max-depth`; its help output did not expose source lines.
- Text searches for the three tokens against the ELF returned no matches. Because the target is a binary, I do not treat those results as evidence that the embedded executable lacks the tokens or implementation.

No tools were installed or updated. No URLs were accessed.
