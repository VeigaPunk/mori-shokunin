# containment on the resolved path, and a supersede that postdates the edit

source: S226 — Python `os.path.realpath` documentation (canonical-path resolution, symlinks
eliminated); S069 — Python `pathlib` documentation (lexical versus resolved containment, superseded
by S226); S073 — the round-20 row that narrowed S069 without a postdating commit.
verified-at: 2026-10-23 — S226 opened this round (`corpus/evidence/sources-r38/S226.src:657-658`);
the edit and supersede commits re-derived with `git log -- reversals` over `corpus/SOURCES.md`.
recheck: on the next change to a containment rule in this lane's tools, and when the S226 page's
canonical-path paragraph moves.

## What happened

S069's row was edited in place at `62db24c` (2026-10-22 23:55, round 33): the `teaches` cell gained
the words "lane rule:" before "reject absolute and .. lexically before any filesystem call, and test
symlinks separately". Its only supersede row at the time, S073, had landed at `71abd41`
(2026-10-21 08:18, round 20) — **before** the edit. The append-only gate was presence-based: it
reported `superseded_by=S073` and could not express that the disposition predates the change
(r37 ExecGateRound D3; QUALITY 102's "later row" clause says *later*).

## The rule, restated with its source

Containment is decided on the **resolved canonical path**: `os.path.realpath` eliminates the
symlinks a lexical check cannot see, so a prefix test on `realpath(p)` is the containment test, and
rejecting absolute or `..` segments before any filesystem call is a cheap pre-filter, not the
decision (S226). `realpath` does not require the path to exist, so a nonexistent path is a decision
about a would-be location, not a permission to touch it.

S226's row therefore opens `supersedes S069` and lands **after** `62db24c`; under the timed reading
S069 is `superseded_as_of`, not merely `superseded`.

## The timed disposition (gate P-C6)

`tools/mori-sources-appendonly.py` now reports, after its summary line:

```
supersede_timing superseded_as_of=[...] stale_supersede=[...]
```

An id is superseded-as-of only when the **latest** superseding row's landing commit is a
descendant of the id's last immutable-cell edit commit. The landing commit of a superseder is the
first commit in the path's history where its `teaches` cell opens `supersedes <id>`; the edit
commit is the last commit in that history where the id's immutable cells changed. On the lane
history the field separates the two cases that presence cannot:

| revision | `stale_supersede` | why |
|---|---|---|
| `e37dcc6` (round-37 tip) | `[S069]` | the only superseder, S073 (`71abd41`), predates the edit (`62db24c`) |
| round-38 tip | `[]` | S226 lands after `62db24c`, so the latest superseder postdates the edit |

## Limits (disclosed)

- Commit order in the **path's** history, not global ancestry: a supersede row that landed in a
  commit which did not touch `corpus/SOURCES.md` cannot be seen. Every row landing touches the
  path, so this is a limit of the implementation, not of the rule.
- A later supersede row disposes the *content* of the edit, not its history: the in-place change
  stays listed in `changed <id>` and in `ids=[...]` (QUALITY 102's listing rule).
- A substring anchor (the `anchor:` line convention) proves presence in the bytes, not that the
  code does what the entry says; the counter's mutation arm is the separate statement.
