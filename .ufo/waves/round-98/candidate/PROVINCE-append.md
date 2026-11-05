

## Round-98 appended scope notes (2026-11-05)

- Core (resource runway, new surface): user namespace runway — the `user.max_user_namespaces` limit against the user namespaces visible on readable process links, and kernel-tunable writes logged by sudo in the journal — read by `tools/mori-userns-runway.py` (detection and report only). Motivating incident: the 2026-11-05 host incident (seats set the limit to 0; every bwrap sandbox failed with ENOSPC). Knowledge: `corpus/knowledge/userns-runway-r98.md`.
- Boundary: mori reads the limit and the write events; it never writes a sysctl, creates or destroys a namespace, or restores a value. Restoring host configuration is the operator's; repairing OS state is tsukuroi's.
