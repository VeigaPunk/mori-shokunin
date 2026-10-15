# mori-shokunin — corpus

## Coverage map

| Note | Holds | Sources |
|---|---|---|
| `knowledge/observability-census-r1.md` | the six census surfaces, the live receipt, and the finding-id compare contract | `tools/mori-census.sh`, live run 2026-10-15 |

## Known gaps

- One note per surface family is still owed (watchdog, waves, kill events, cgroup,
  disk, silence); round 1 landed a single consolidated receipt instead.
- `progressing-weak` (sibling-authored activity) is deferred: the probe cannot yet
  prove authorship, so it grades in-window activity as `progressing`.
