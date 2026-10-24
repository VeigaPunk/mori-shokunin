# Round-18 token-redaction attack: DeadSeatCrossCheck

Target: `.ufo/waves/round-17/build/DeadSeatCrossCheck.md`, tree diff `d005cdd..e2bfbd6`.

## Findings

### High — private session context remains beyond the three path substitutions

- `DeadSeatCrossCheck.md:7` still identifies the referenced session through a time fragment beside the seat-prefix list. The full store path was removed at `:11`, `:82`, and `:209`, but this partial session identity remains. It is not a name-only surface mention; the frozen C1 token regex is a recall floor (`.ufo/waves/round-18/frozen/c1-policy.json:29`).
- `DeadSeatCrossCheck.md:5-17,85-91` still contains per-seat retry values and a retained scan-output excerpt, including a session-tied scan timestamp. The round-18 minimization rule allows aggregate counts/class tallies, but explicitly excludes per-seat retry values and limits other-session output to count/class rather than excerpts (`corpus/knowledge/evidence-minimization-r18.md:24-30`). Thus the blanket rejection in `out-of-metric-triage.md:26` is too broad for this report: these lines are not name-only mentions. No private values are reproduced here.

### Medium — redaction breaks the shell example

- `DeadSeatCrossCheck.md:82` removes the store path but leaves an unquoted angle-bracket placeholder in the shell code block and drops the separator before the trailing status command. The resulting line is not valid shell as written, so the example's technical meaning/executability is broken.

## Redaction and allowlist assessment

- `DeadSeatCrossCheck.md:11` and `:209` remove the concrete store-path values. The table row at `:209` remains intelligible as a description of the inspected surface.
- Name-only mentions of fields, keys, record types, or surfaces are allowlistable only when they carry no private-source value and occur in an allowed context (frozen C1 policy `:27`; evidence-minimization rule `:29`). That narrow decision is sound. It does not justify retaining the session identity fragment or per-seat/output values above.
- Only a Markdown file changed; JSON validity testing with `python3 -m json.tool` is not applicable. No JSON files were changed.

## Verification and gaps

- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff d005cdd e2bfbd6 -- .ufo/waves/round-17/build/DeadSeatCrossCheck.md` — exit 0; reviewed all three changed lines and surrounding passages.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --stat d005cdd e2bfbd6 -- .ufo/waves/round-17/build/DeadSeatCrossCheck.md` — exit 0.
- No source callers or definitions apply to this Markdown-only target; no JSON parser, build, or tests were run. No URLs accessed. No tools installed or updated.