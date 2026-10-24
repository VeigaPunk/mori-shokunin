# Round 18 shared-context falsification: V12 and routed defect 3

## Scope and method

Compared this wave's shared context with the two open gaps in `.ufo/waves/round-18/build/SentinelContextAudit.md:30,39-41`, checking the underlying round-17 findings at `corpus/lessons/round-17-verifier-spotcheck.md:316,403-407` and the round-18 contract/frozen inputs. This is a context-text audit only; it does not establish runtime compliance or re-audit the other V-items. No shell commands, selftests, installs, or updates were run.

## Findings

### V12 — closed in the shared context

- **Severity:** No remaining context gap in the reported V12 scope; residual procedural risk remains because instructions do not enforce themselves.
- **Exploit path considered:** The prior gap allowed a `jj` config-path/query operation outside the lane Git-read allowlist, or a direct read of repository/user jj configuration. Both are now explicitly prohibited.
- **Evidence:** The shared context states: “never run `jj config` (path discovery included) and never read repository or user jj configuration.” It separately keeps lane reads to the named Git allowlist and prohibits running `jj` against the lane. This directly addresses the unguarded config-path and user-config accesses classified in the cited V12 source finding.
- **Impact:** The previous ambiguity is removed at the pre-action instruction layer. A violation remains possible, but cannot be treated as authorized by the context.
- **Smallest remediation:** None; retain the existing prohibition. No further text change is indicated for the reported V12 gap.

### Routed defect 3 — closed in the shared context

- **Severity:** No remaining context gap for the routed caveat; residual risk is the inherent lack of runtime enforcement.
- **Exploit path considered:** A reader could otherwise infer from a clean later worktree/status or missing artifact that a prohibited action never occurred.
- **Evidence:** The shared context states: “These instructions are not runtime guards, and a clean later worktree, status or absence of artifacts cannot establish that a prohibited action did not occur: report what you actually ran.” This covers both cautions recorded at `corpus/lessons/round-17-verifier-spotcheck.md:405-407` and the missing-context finding at `.ufo/waves/round-18/build/SentinelContextAudit.md:41`.
- **Impact:** Later-state observations are explicitly disallowed as proof of historical compliance; reporting is directed toward actual actions.
- **Smallest remediation:** None; the needed caveat is present.

## New gap

None observed within the requested V12 and routed-defect-3 scope. This conclusion is limited to these two context gaps; it is not a claim that all instructions are runtime guards or that other shared-context requirements were independently revalidated.
