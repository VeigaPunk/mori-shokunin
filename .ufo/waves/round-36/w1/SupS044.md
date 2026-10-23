measured 2026-10-23T12:05:03Z

# SupS044 — Round-35 routed defect 2

## Finding

VERDICT: unsupported

At tip `6bd57097`, S044's source, kind, tier, scope, anchor, teaches, status, opened date, recheck, and used-by cells were: `jj Git compatibility — https://docs.jj-vcs.dev/latest/git-compatibility/`; `docs`; `A`; `colocated jj/Git HEAD state`; `Detached HEAD feature row and Colocated Jujutsu/Git workspaces; opened 2026-10-20`; `jj commands usually put Git in detached HEAD state; a commit-id read is not a branch-identity proof.`; `mined`; `2026-10-20`; `on-release`; `corpus/knowledge/jj-branch-anchor-r17.md`. Command output: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 6bd57097:corpus/SOURCES.md | grep '^| S044 '` returned that row.

First-published cells at `273aa74a` show the same row text in the corresponding command output. `ScoutAppendDebt.md:23` reports the intermediate immutable-teaches edit at `62db24c0`: insertion of `lane rule` before the clause about a commit-id read, logged at `corpus/lessons/round-33.md:83`.

The official source reopened at HTTP 200 supports the detached-HEAD tendency, but not the words `a commit-id read is not a branch-identity proof`. The reopened source says Jujutsu supports detached HEAD (`S044.src:2154`), names the colocated workspace (`:2223`), and states that jj commands usually put the Git repo in a detached HEAD state (`:2234-2235`). It does not make the commit-id/branch-identity claim. Scope and both anchor locators are supported. The unsupported part is omitted from the proposed teaches; the row is marked mined because that is S044's status at tip.

## Source and commands

- `timeout 120 git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 6bd57097:corpus/SOURCES.md | timeout 120 grep '^| S044 '` → tip row above.
- `timeout 120 git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 273aa74a:corpus/SOURCES.md | timeout 120 grep '^| S044 '` → first-published row; same text as tip output.
- `timeout 120 git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree -r --name-only 6bd57097 -- corpus/knowledge/jj-branch-anchor-r17.md` → `corpus/knowledge/jj-branch-anchor-r17.md` exists at tip.
- `timeout 120 mkdir -p /fast/scratch/hyaku/mori-r36/SupS044 && timeout 120 curl --max-time 110 -L -sS -o /fast/scratch/hyaku/mori-r36/SupS044/S044.src -w 'HTTP_STATUS=%{http_code}\n' https://docs.jj-vcs.dev/latest/git-compatibility/ && timeout 120 sha256sum /fast/scratch/hyaku/mori-r36/SupS044/S044.src` → `HTTP_STATUS=200`; sha256 `db9c9a760810386858e6b1bad4a7a334c56bd48c77692dbc1c343657ae0ca254`.
- `timeout 120 date -u +%FT%TZ` → `2026-10-23T12:05:03Z`.

## Drafts

DRAFT `corpus/SOURCES.md` — superseding row placeholder S2NN, 11 columns:
```text
| S2NN | jj Git compatibility — https://docs.jj-vcs.dev/latest/git-compatibility/ | docs | A | colocated jj/Git HEAD state | Detached HEAD feature row and Colocated Jujutsu/Git workspaces; re-opened 2026-10-23 | supersedes S044 — jj commands will usually put the Git repo in a detached HEAD state. | mined | 2026-10-23 | on-release | corpus/knowledge/jj-branch-anchor-r17.md |
```
The correction removes the commit-id/branch-identity sentence because the reopened source does not support it. The row carries the tip's source, kind, tier, scope, anchor locators, status, recheck, and used-by; its anchor records this round's reopen date.

DRAFT `corpus/lessons/round-36.md` §Gate line:
```text
| S2NN | https://docs.jj-vcs.dev/latest/git-compatibility/ | 2026-10-23 | `db9c9a760810386858e6b1bad4a7a334c56bd48c77692dbc1c343657ae0ca254` | (13 words) Detached HEAD: Yes. Jujutsu supports anonymous branches, so this is a natural state. — `S044.src:2154`; (3 words) Colocated Jujutsu/Git workspaces — `S044.src:2223`; (13 words) jj commands will usually put the Git repo in a detached HEAD state — `S044.src:2234-2235` | unsupported: detached-HEAD claim holds; commit-id/branch-identity claim is not supported |
```

## Gates, touched surfaces, limits

- Evidence gate: source reopened by ordinary `curl`; HTTP 200, saved bytes hashed, and each anchor locator has a located quote of at most 25 words. No test, build, lint, or lane gate was run.
- Read-only lane surfaces: `.ufo/waves/round-35/w2/ScoutAppendDebt.md:23`, `corpus/SOURCES.md` via the two `git show` commands, and the tip tree via `git ls-tree`.
- Wrote only this report and the fetched source artifact. No product file, lesson, registry, index, or git history was changed. No tool was installed. This report drafts the requested changes but does not append them.
- Limits: current URL content is the live `latest` page, not a version-pinned snapshot; the recorded digest binds only the bytes fetched in this run. No claim is made about other revisions of the page.

## Artifacts

- Report: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/w1/SupS044.md`
- Reopened source bytes: `/fast/scratch/hyaku/mori-r36/SupS044/S044.src` — SHA-256 `db9c9a760810386858e6b1bad4a7a334c56bd48c77692dbc1c343657ae0ca254`.
