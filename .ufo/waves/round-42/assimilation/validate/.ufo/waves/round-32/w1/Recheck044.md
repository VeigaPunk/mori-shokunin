# Recheck044 — S044

Seat: MoriR32A2.Recheck044. Scope: C1 freshness recheck of S044 only.

## 1. Fetch record

| field | value |
|---|---|
| id | S044 |
| url (population, unchanged) | https://docs.jj-vcs.dev/latest/git-compatibility/ |
| accessed | 2026-10-23T01:31:27Z |
| byte size | 61334 |
| sha256 | db9c9a760810386858e6b1bad4a7a334c56bd48c77692dbc1c343657ae0ca254 |
| scratch copy | /fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck044/S044.src |
| normalised text | /fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck044/S044.txt (13920 bytes, via `seat-check.py text`) |
| fetch log | /fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck044/S044.fetch.txt (empty; first try succeeded) |

Command: `curl -sSL --fail -m 60 https://docs.jj-vcs.dev/latest/git-compatibility/ -o S044.src` → HTTP 200, curl exit 0 on try 1.
Redirect: none. `curl -sSIL` shows only `HTTP/2 200` with no `Location` header; the `latest` alias resolved in place, so the url cell stays the population url.

Fetched copy differs from the counter's own live fetch? No: `live_quotes_ok=True` in the seat-check output below means the counter's fresh fetch contains all three quotes verbatim.

## 2. Ready-to-paste row

```markdown
| S044 | https://docs.jj-vcs.dev/latest/git-compatibility/ | 2026-10-23T01:31:27Z | db9c9a760810386858e6b1bad4a7a334c56bd48c77692dbc1c343657ae0ca254 | "jj commands will usually put the Git repo in a \"detached HEAD\" state"; "since in jj there is not concept of a \"currently tracked branch\""; "either have no branches at all (not even a main branch) or will have branches that are out of date with jj's bookmarks" | current |
```

Verdict: **current**.

## 3. Quote → teaches-cell support

Teaches cell: "jj commands usually put Git in detached HEAD state; a commit-id read is not a branch-identity proof."

1. `jj commands will usually put the Git repo in a "detached HEAD" state` (13 words) — normalised page, Colocated Jujutsu/Git workspaces section: "One reason for this (see below for more) is that jj commands will usually put the Git repo in a "detached HEAD" state, since in jj there is not concept of a "currently tracked branch"." Directly states teaches clause 1 (jj → Git detached HEAD). Shared tokens: commands, detached, head, state, usually.
2. `since in jj there is not concept of a "currently tracked branch"` (12 words) — same sentence, carries the reason: no jj-side current branch exists, so the Git HEAD is not a branch binding. Supports both clause 1 and clause 2. Shared token: branch. The odd "there is not concept" wording is verbatim from the page (not my truncation).
3. `either have no branches at all (not even a main branch) or will have branches that are out of date with jj's bookmarks` (23 words) — Colocated section, on a Git repo hidden under `.jj` when colocation is off: "unless you explicitly use the jj git import and jj git export commands, that Git repository will either have no branches at all (not even a main branch) or will have branches that are out of date with jj's bookmarks." Supports teaches clause 2: what a Git-side read of a commit id shows (an unattached or stale branch) is not evidence of branch identity; jj's bookmarks are the authority. Shared token: branch.

Corroborating (not quoted, to stay at 3): the "Supported features" list still carries "Detached HEAD: Yes. Jujutsu supports anonymous branches, so this is a natural state." (anchor's feature row, still present), and "Branches ¶ TODO: Describe how branches are mapped" still shows jj does not define a per-commit Git branch mapping.

## 4. Seat-check output

Command (quotes cell passed as argv, read from `quotes.txt` to avoid shell escaping):

```
sha256=db9c9a760810386858e6b1bad4a7a334c56bd48c77692dbc1c343657ae0ca254
quotes=3 words=[13, 12, 23] in_copy=[True, True, True]
shared_tokens=['branch', 'commands', 'detached', 'head', 'state', 'usually'] topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
```

Saved at /fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck044/row-check.txt.

## 5. Drift details

None. No `Round32` correction is required: both clauses of the teaches cell are still stated by the live page, the anchor's "Detached HEAD" feature row and "Colocated Jujutsu/Git workspaces" section are both still present at the same URL, and no sentence that mattered was reworded. The used-by file `corpus/knowledge/jj-branch-anchor-r17.md` (lines 9, 19, 44) still matches the page's claim that a detached HEAD names a commit that need not be on the bookmark and that commit-id reads are not branch-identity proofs.

## 6. Environment / tooling

No tools installed or updated (no pacman/uv/cargo/npx transactions). Only curl, python3 (stdlib), sha256sum, date were used. No git or jj commands were needed. No subagents, no background jobs.
