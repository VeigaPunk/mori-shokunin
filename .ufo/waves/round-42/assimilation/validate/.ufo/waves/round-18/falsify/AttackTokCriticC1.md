# AttackTokCriticC1 — wave 2 falsification

## Verdict

No actionable defect found in this diff's single changed line.

## Review findings

- **Private-token removal — pass.** The read-only diff changes only ` .ufo/waves/round-17/build/CriticC1.md:50`. At the base, the frozen population records that line as both C1 class R1 (session identity) and R2 (session-store path), with the same `line_sha256` (`589f9d598e2700b141a9375ed176f53996440e5a593affad219f8d039c451914`). The replacement removes the concrete identity/path; an exact R1–R9 scan at `e2bfbd6` returned no matching lines in this file. The base scan returned only line 50.
- **Same/neighboring-line values — pass.** `CriticC1.md:47-51` contains field/key names and scope metadata: a file-count aggregate, a file-type pattern, and the symlink-handling statement. It does not leave a session-record value, routing value, per-seat retry value, or another private token beside the redaction. `retryRecovery` is described by key shape only. This is consistent with the explicit distinction between private values and field names/aggregates in `out-of-metric-triage.md:10-16,26`.
- **Name-only allowlisting — supported for this context.** The adjacent field/key and surface names disclose no values. The frozen policy permits allowlisting a surface named without its contents and field/key names (`frozen/c1-policy.json:27`); the triage decision separately accepts field/record-type names and filename census aggregates (`out-of-metric-triage.md:26`). This is not a basis to allowlist copied values.
- **Technical meaning — pass.** The text still conveys the scope's count/type and symlink treatment. The concrete source path is intentionally unavailable, but the redaction does not alter those stated scope facts. This is Markdown, not JSON; `python3 -m json.tool` was not applicable.

## Residual risk and verification gaps

The conclusion is limited to the changed line, its immediate context, and the frozen token classes. The policy itself warns that those classes are a recall floor, not a privacy proof (`frozen/c1-policy.json:29`); this review does not establish absence of arbitrary unclassified private context elsewhere. No JSON validity check was run because the reviewed file is `.md`.

## Read-only evidence and commands

- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff d005cdd e2bfbd6 -- .ufo/waves/round-17/build/CriticC1.md` — exit 0; one changed line, line 50.
- Frozen-population lookup at `frozen/c1-population.json` for this path — observed R1 and R2 hits at line 50 with the line hash stated above.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -nE '[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{3}Z_[0-9a-f]{8}-|\.omp/agent/sessions/|[0-9]{2,}\.(bash|bash-original|wait|read|eval|task)\.log|(/home/[^/[:space:]]+|~)/Documents/|\.bash_history|sudoers|config\.yml:[0-9]|\.omp/agent/config\.yml|\b(fallbackChains|agentModelOverrides|enabledModels|modelRoles)\b|data\.(reason|kind)|retryRecovery\.note|\bmodel_change\b' d005cdd -- .ufo/waves/round-17/build/CriticC1.md` — exit 0; only the line-50 R1/R2 match.
- The same frozen-class scan at `e2bfbd6` — exit 1 (no matches).
