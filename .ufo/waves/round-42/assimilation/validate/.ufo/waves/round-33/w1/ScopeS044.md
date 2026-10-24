# S044 scope review

## Axes
- Source support: distinguish page statements from lane application.
- Auditability: tie each finding to the frozen row, recheck, and committed copy.
- Containment: write this report only; make no lane/product edits.

## Findings
The frozen S044 row is the same in base commit `7d382043` and the current registry: scope `colocated jj/Git HEAD state`; teaches `jj commands usually put Git in detached HEAD state; a commit-id read is not a branch-identity proof.` The base-row command and output are recorded below; the current row is `corpus/SOURCES.md:50`.

1. **Scope clause — sourced, not a lane inference.** The entire scope cell, `colocated jj/Git HEAD state`, is supported by the committed page copy: it calls the section “Colocated Jujutsu/Git workspaces” and says a colocated Jujutsu workspace is a hybrid Jujutsu/Git workspace whose Git repo and workspace share a working copy (`corpus/evidence/recheck-r32/S044.src:2223-2227`). The HEAD-state scope is also on that page: “jj commands will usually put the Git repo in a \"detached HEAD\" state” (`S044.src:2234-2235`). No scope-cell edit is proposed.

2. **Teaches clause — sourced.** `jj commands usually put Git in detached HEAD state` is stated by the page: “jj commands will usually put the Git repo in a \"detached HEAD\" state” (`S044.src:2234-2235`). The round-32 recheck records that quote (`corpus/lessons/round-32.md:33`).

3. **Teaches clause — lane application, not stated by the page.** `a commit-id read is not a branch-identity proof` has no located quote in the committed copy that states it. The closest passage says Jujutsu has no concept of a “currently tracked branch” (`S044.src:2235-2236`); another says a Git repo in the non-colocated case may have no branches or branches out of date with bookmarks (`S044.src:2246-2247`). Neither states what a commit-id read proves about branch identity. Declare this clause as lane doctrine, following the S073, S074, and S076 pattern (`corpus/SOURCES.md:79-82`).

### Old and proposed cells

Scope — old:
```text
colocated jj/Git HEAD state
```

Scope — proposed (unchanged):
```text
colocated jj/Git HEAD state
```

Teaches — old:
```text
jj commands usually put Git in detached HEAD state; a commit-id read is not a branch-identity proof.
```

Teaches — proposed:
```text
jj commands usually put Git in detached HEAD state; lane rule: a commit-id read is not a branch-identity proof.
```

Old → new diff:
```diff
-jj commands usually put Git in detached HEAD state; a commit-id read is not a branch-identity proof.
+jj commands usually put Git in detached HEAD state; lane rule: a commit-id read is not a branch-identity proof.
```

## Provenance and gates
- Base row command: `timeout 10s git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 7d382043:corpus/SOURCES.md | grep -n '^| S044 '`.
- Outcome: one match, line 50: `| S044 | jj Git compatibility — https://docs.jj-vcs.dev/latest/git-compatibility/ | docs | A | colocated jj/Git HEAD state | Detached HEAD feature row and Colocated Jujutsu/Git workspaces; opened 2026-10-20 | jj commands usually put Git in detached HEAD state; a commit-id read is not a branch-identity proof. | mined | 2026-10-20 | on-release | corpus/knowledge/jj-branch-anchor-r17.md |`.
- Round-32 recheck row `corpus/lessons/round-32.md:33` lists the S044 URL, accessed time, SHA-256 receipt, three quotes, and `current`; the committed copy inspected is `corpus/evidence/recheck-r32/S044.src`. The receipt digest was not independently recomputed.
- Closure note identifies S044 as a critic finding, not adopted or needed for its verdict, and describes the issue as an undeclared inference/lane application (`corpus/lessons/round-32-verifier-spotcheck.md:100-104,190-192`). S073/S074/S076 explicitly mark their own rules or applications as not taught by their pages (`corpus/SOURCES.md:79-82`).
- No tests, build, counter, or fresh URL fetch was run. No tool was installed. This was a read-only review followed by writing this report.

## Touched surfaces and limits
- Written: `.ufo/waves/round-33/w1/ScopeS044.md` only.
- No product code, registry, lesson, source copy, contract, judge, or Git state was changed. No lane commit or publication was made.
- This report proposes the cell text for the integration owner; it does not alter or adjudicate the frozen row.
