

## Round98 gate registry row (user-namespace runway and sysctl-write scan)

The round-98 capability `tools/mori-userns-runway.py` (C1, `.ufo/waves/round-98/contract.md`) enters this
registry home in the same landing, so the lane auditor (`python3 tools/mori-gate-registry.py --rev <rev>
--audit-all`) stays `REGISTRY=met`. Knowledge: `corpus/knowledge/userns-runway-r98.md`. Appended at the
file's end; no earlier byte edited.

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| user-namespace runway and sysctl-write scan (r98 tool) | probe | `python3 tools/mori-userns-runway.py [--proc DIR] [--low N] [--init-ino INO]`; `python3 tools/mori-userns-runway.py --journal FILE` or `--journal -` or `--journal-live --since TS --until TS` (`--selftest`) | runway: `USERNS_RUNWAY limit=L used_lb=U pids=P unreadable=X runway=R low=T state=ok/low/exhausted` · 0 -> ok · 1 -> low or exhausted (a limit of 0 is exhausted) · 2 -> `USERNS_RUNWAY_SETUP` (limit missing/unparsable, no process entries); scan: one `SYSCTL_WRITE ts=T pid=N key=K value=V via=sysctl/sysctl-load/sh-echo/tee` per write, then `SYSCTL_WRITES n=N keys=K userns_zero=Z` · 0 -> no write · 1 -> at least one write · 2 -> `SYSCTL_WRITES_SETUP` | `python3 tools/mori-userns-runway.py --selftest` -> `MORI_USERNS_RUNWAY_SELFTEST: PASS (11 cases)` exit 0 | initial user namespace inode 4026531837 (PROC_USER_INIT_INO); low threshold 32; used_lb is a lower bound (fd/bind-mount-held and unreadable-link namespaces invisible); incident capture `.ufo/waves/round-98/evidence/journal-incident-r98.txt` scores `SYSCTL_WRITES n=6 keys=1 userns_zero=2` | stdout only; selftest fixtures in a tempfile dir under TMPDIR, deleted on exit; never writes a sysctl or creates a namespace | mori |
