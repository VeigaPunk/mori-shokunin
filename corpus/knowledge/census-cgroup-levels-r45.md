# The cgroup row's OOM provenance is silent: a preferred fallback, a hard-wired `path=`, and a selftest that cannot see the switch

source: S473 — https://cdn.jsdelivr.net/gh/torvalds/linux@v7.2/Documentation/admin-guide/cgroup-v2.rst — `memory.events` (hierarchical) and `memory.events.local` (local); opened copy `cgroup-v2.rst.src`, sha256 a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad, fetched 2026-10-25
verified-at: 2026-10-25
recheck: 90d — `curl -fsSL --max-time 40 https://cdn.jsdelivr.net/gh/torvalds/linux@v7.2/Documentation/admin-guide/cgroup-v2.rst | sha256sum` -> a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad; `sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-census.sh` -> 87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28 (both ran 2026-10-25)
coverage-map: FR1, FR12 — FR1 kernel OOM event-time attribution (a count whose source file is misnamed cannot be attributed to a scope); FR12 pressure provenance in the same row
ground: frontier item **FR12** — boundary (`PROVINCE.md:55`): "a PSI trigger watcher is resident, not a one-shot census probe; system CPU `full=0` is not evidence of no stall"

## Claim

`local_oom_kill` is filled by a silent preference order — the slice's `.events.local`, else the session service's hierarchical `memory.events`, else empty (`tools/mori-census.sh:1707-1712`) — and when both files are missing the row still reads `ok` with `local_oom_kill=unavailable`, while neither the state nor any path cell records which file was missing, though the census states absent ≠ unreadable for `CGROUP_PRESSURE` (`:1747-1749`). The `CGROUP_OOM_KILL` finding prints `path=${LOCAL_EVENTS}` as a constant while the value may have come from `SERVICE_EVENTS`: measured this run, a mode-000 local file holding `oom_kill 7` beside a service holding `3` yields `local_oom_kill=3` with a `path=` naming the file whose own bytes say 7 (exit 1). The selftest cannot see the level — one fixture file for all three paths, `.events.local` never created, a bare finding-id assertion — and three mutants (drop the fallback, re-point `path=`, force the value to 0) each still print `PASS (134 cases…)`, while `--drift` masks the field so a level switch cannot surface in a drift verdict.

## What is measured here

Measured at tip `3ad8faaa637ae466c61f9427fea1c208bf49ea82`, census sha256 `87b8d680…b977ab28`; the census was not touched this round and every cited line is the entering tip's. Inference is marked `[INFERENCE]`.

**The silent order** (`tools/mori-census.sh:1707-1712`, 20 words):

```sh
  service_oom_kill=''
  if [ -r "$LOCAL_EVENTS" ]; then
    service_oom_kill=$(cgroup_field "$LOCAL_EVENTS" oom_kill)
  elif [ -r "$SERVICE_EVENTS" ]; then
    service_oom_kill=$(cgroup_field "$SERVICE_EVENTS" oom_kill)
  fi
```

`LOCAL_EVENTS` defaults to `<CGROUP_EVENTS%.events>.events.local` (`:1705`) and `SERVICE_EVENTS` to the absolute `/sys/fs/cgroup/user.slice/user-<uid>.slice/user@<uid>.service/memory.events` (`:1706`). Received (fixture overrides, live mode, which writes nothing; all rc 1; each line ≤13 words):

```
A  local absent, service oom_kill=3   → obs=local_oom_kill=3 path=…/absent-memory.events.local
B  local mode-000 oom_kill=7, service 3 → obs=local_oom_kill=3 path=…/local-memory.events.local
C  local and service absent           → SURFACE cgroup: ok … local_oom_kill=unavailable; CGROUP_OOM_KILL findings=0
```

B is the provenance defect: the emitted `path=` names a file whose bytes read `oom_kill 7`, and the value is the other file's. C is the silence: absent files leave the surface `ok`, while the census states the opposite rule for a sibling path: `field must not claim the file does not exist` (`:1748`, 9 words, in the comment block `:1747-1749`). That rule is written for `CGROUP_PRESSURE` and not applied to either events file.

**The hard-wired cell** (`:1844`, 9 words): `local_oom_kill=$service_oom_kill path=${LOCAL_EVENTS} (local counter: kills in this cgroup only)`. The value comes from either branch; the path does not.

**The level-blind selftest.** `MORI_CGROUP_SERVICE_EVENTS="$FX/cgroup/memory.events"` (`:3253`, 1 word) and the local pin at `:3254` name that same file, which the fixture creates as `memory.events` only — `memory.events.local` is never created (`grep -c 'events\.local'` over the census: 3 — the comments at `:1698` and `:1701` and the default at `:1705`; no fixture line). The only `CGROUP_OOM_KILL` assertion is `check 'drift: CGROUP_OOM_KILL' 1 DRIFT` (`:3907`, 5 words) against `'FINDING CGROUP_OOM_KILL'` (`:3908`, 2 words). Measured: baseline `PASS (134 cases, 134 passed, 0 failed)` (7 words) rc 0; then, on private copies, `elif` deleted → PASS 134/134 (live: `local_oom_kill=unavailable`); `path=` re-pointed to `SERVICE_EVENTS` → PASS 134/134 (live: `path=…/service-memory.events`); value forced to `0` → PASS 134/134 (live: `local_oom_kill=0`).

**The drift mask.** `local_oom_kill` is on the declared volatile list (`DRIFT_COUNTER_KEYS`, `:2747`, 6 words: `ledger_round local_oom_kill max mem_fill_pct mem_peak not_open`), and `drift_normalize` rewrites it (`:2791`, 2 words: `-e "s/\\b(${cre})=[0-9]+/\\1=<V>/g"`). Measured twice: two rows differing only in `local_oom_kill=1` vs `=2` normalize to identical text; and a pin/drift pair over one fixture directory whose only change was that counter printed `MORI_DRIFT: +FINDING:DISK_LOW -FINDING:DISK_CRITICAL` (3 words) — no cgroup field and no cgroup line named, rc 1 from unrelated live disk churn.

## What the source grounds

Only the generic distinction. `memory.events` (`cgroup-v2.rst.src:1468`) is the hierarchical file: "all fields in this file are hierarchical and the file modified event can be generated due to an event down the hierarchy" (`:1474-1476`, 22 words), pointing at "For the local events at the cgroup level see memory.events.local." (`:1476-1477`, 10 words); `memory.events.local` (`:1517`) is "Similar to memory.events but the fields in the file are local to the cgroup i.e. not hierarchical." (`:1518-1519`, 17 words). The docs define two counting scopes; they say nothing about which file a census row must name, so every claim above about the row is measured from the census, not derived from S473.

Line numbers belong to the opened copy. `oom-kill-counter-kernel-only-r12.md:12` cites the local-vs-hierarchical distinction from `docs.kernel.org` at `memory.events.local:1505–1509`; that render does not carry the "all fields in this file are hierarchical" sentence this entry quotes (the equivalent text sits at `memory.events:1448–1458,1491–1494` there), and the renders differ, so a line number travels with its copy and digest.

## What is already held

- `observability-census-r1.md:135` holds the measured propagation — "the parent slice's `1` is a propagated count, and `memory.events.local` reads `0`" (12 words) — and `:136` holds that the probe prefers the local file.
- `oom-kill-counter-kernel-only-r12.md:12` holds the local-vs-hierarchical distinction from S002; that the two files differ is not new here.
- `surfaces-r7.md:88-90` holds that the row carries both counters — "the bare `oom_kill=` is still the parent cumulative counter, and the session-service reading is printed next to it as `local_oom_kill=`" (20 words).
- `pid-probe-conclusion-r44.md:53` is the round-44 precedent in form — one reading, several worlds, "the read alone separates none of these" (7 words) — landed without a census change (`:79`).

**New here:** the *silent* order (no absent/unreadable state for either events file), the constant `path=` cell proven by two executions, the level-blind selftest with three surviving mutants, and the drift mask. The held entries name the counters and the preference; none reports that the preference is unobservable when it fires.

## What this does not license

- No census change. Nothing is patched, reworded or recommended for adoption this round; the bytes above are the entering tip's.
- No cgroup v1: the source is `cgroup-v2.rst`, and v1's control files are outside this entry.
- No remediation and no defect-to-patch instruction: it records what the bytes do, not what the lane should do next.
- No live-host claim: A/B/C are fixture overrides; nothing here shows a real host whose two counters differ.
- No general weakness claim about the selftest: only that no case separates the three paths and these three mutants survive.
- No FR1 closure and no FR12 advance. FR12's boundary stands — this is a one-shot row's provenance, not a resident watcher — and FR1's event-time attribution is untouched.
