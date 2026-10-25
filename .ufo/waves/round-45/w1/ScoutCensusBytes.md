# ScoutCensusBytes — level-naming facts pinned from `tools/mori-census.sh`

Scope: one unknown — which cgroup **level** each counter/claim in the census comes from,
and whether the printed level names can be false. Read-only. No lane file was edited;
two mutant scripts were written **only** under my TMPDIR and run there.

## Instrument pin

| fact | value |
|---|---|
| path | `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-census.sh` |
| sha256 | `87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28` |
| lines | 4744 |
| HEAD | `3ad8faaa` (round-45 freeze) on entering tip `554ff416` |
| blob at entering tip | `git show 554ff416:tools/mori-census.sh \| sha256sum` → **same** `87b8d680…` |
| working tree | `git status --porcelain tools/mori-census.sh` → empty |

```
$ sha256sum tools/mori-census.sh
87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28  tools/mori-census.sh
$ git -C . rev-parse HEAD
3ad8faaa637ae466c61f9427fea1c208bf49ea82
$ git status --porcelain tools/mori-census.sh
(no output)
```

Note, outside my item: the contract names the digest manifest `evidence/freeze-r45.txt`;
it did **not** exist at my read time (`find . -maxdepth 3 -name 'freeze-r45*'` → no output),
so my pin above is by direct computation, and it equals the entering-tip blob.

Scratch: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/tmp/ScoutCensusBytes`.
No tool was installed or upgraded this seat.

---

## 1. The `cgroup` surface row (line 1862): counter → level

```bash
$ awk 'NR==1862' tools/mori-census.sh
  emit_surface cgroup "$st" "cmd=$cmd; oom_kill=$oom_kill oom=${oom:-?} high=${high:-?} max=${max:-?} current=${cur:-?}; local_oom_kill=${service_oom_kill:-unavailable} psi_some_avg10=${psi_some:-unavailable} psi_full_avg10=${psi_full:-unavailable} psi_source=$psi_state psi_warn_avg10=$MEM_PSI_WARN_AVG10 $fill_field mem_peak=${peak:-unavailable} mem_peak_source=$peak_src mem_peak_anchor=${peak_anchor:-unavailable}; ts=$TS_UTC"
```

Source resolution (defaults block, lines 304–311):

```
304: CGROUP_EVENTS=${MORI_CGROUP_EVENTS:-/sys/fs/cgroup/user.slice/user-$(id -u).slice/memory.events}
305: CGROUP_CURRENT=${MORI_CGROUP_CURRENT:-/sys/fs/cgroup/user.slice/user-$(id -u).slice/memory.current}
   (CGROUP_PRESSURE = ${CGROUP_EVENTS%.events}.pressure, CGROUP_MAX = ….max, CGROUP_PEAK = ….peak)
```

Reads (numbered):

```
1709:     service_oom_kill=$(cgroup_field "$LOCAL_EVENTS" oom_kill)      # level A: THIS cgroup
1711:     service_oom_kill=$(cgroup_field "$SERVICE_EVENTS" oom_kill)    # level B: user@1000.service
1713:   oom=$(cgroup_field "$CGROUP_EVENTS" oom)
1714:   high=$(cgroup_field "$CGROUP_EVENTS" high)
1715:   max=$(cgroup_field "$CGROUP_EVENTS" max)
1722-1725: current ← read_file(CGROUP_CURRENT) only if realpath is under /sys/fs/cgroup, else `refused:outside-sysfs-cgroup`
1687:   oom_kill=$(cgroup_field "$CGROUP_EVENTS" oom_kill)
1741-1746: psi_some/psi_full ← psi_avg10(CGROUP_PRESSURE)
1789-1792: mem_fill host-ram branch ← meminfo_field MemTotal/MemAvailable  (level: host RAM)
1805-1807: mem_fill cgroup branch ← cur_num(CGROUP_CURRENT) / mem_limit(CGROUP_MAX)
1827-1832: mem_peak ← num_of(CGROUP_PEAK)
```

| row token | level it actually comes from | level named in the row |
|---|---|---|
| `oom_kill=` | parent `user-1000.slice` `memory.events`, cumulative since boot | **none** (bare name; only the prose at 1691–1704 and the sibling finding id `CGROUP_OOM_KILL_CUMULATIVE` say "cumulative/parent") |
| `oom=` `high=` `max=` | same parent `memory.events` | none |
| `current=` | parent `memory.current`, only if under `/sys/fs/cgroup` | none; refusal token `refused:outside-sysfs-cgroup` |
| `local_oom_kill=` | **`LOCAL_EVENTS` OR `SERVICE_EVENTS`** — whichever was readable (1708–1712) | claims "local"; **false when the fallback fired** |
| `psi_some/full_avg10`, `psi_warn_avg10` | parent `memory.pressure` | none (`psi_source=` is the *state* ok/unreadable/absent, not the level) |
| `mem_fill_pct`, `mem_fill_scope` | cgroup: parent `current/max`; host-ram: `/proc/meminfo` | **`mem_fill_scope=host-ram\|cgroup\|unavailable`** — the only field in the row that names a level |
| `mem_peak`, `mem_peak_source`, `mem_peak_anchor` | parent `memory.peak`; anchor = parent directory mtime | none |

Three measured consequences:

1. **No `path=` token in the row.** `grep -c 'path='` over the cgroup surface line → `0`.
2. **`cmd=` names only four files and omits both events levels:**
   ```
   1681:   local cmd="cat $CGROUP_EVENTS; cat $CGROUP_CURRENT; cat $CGROUP_PRESSURE; cat $CGROUP_MAX"
   ```
   Neither `LOCAL_EVENTS` nor `SERVICE_EVENTS` appears in `cmd=`, so even the command text does
   not disclose which file produced `local_oom_kill`.
3. **In fixture mode `current=` is structurally refused.** Every one of my fixture runs printed
   `current=refused:outside-sysfs-cgroup`, because `realpath` of the fixture path is not under
   `/sys/fs/cgroup` — so the `cur=$(read_file …)` arm at 1723 is never exercised by `--selftest`
   either (the selftest pins `MORI_CGROUP_CURRENT="$FX/cgroup/memory.current"`, line 3255).

`local_oom_kill` is additionally a drift key (line 2747, `DRIFT_COUNTER_KEYS`), whose digits
`drift_normalize` masks to `<V>` (`s/\b(${cre})=[0-9]+/\1=<V>/g`), so `--drift` compares neither
the value nor the level of this counter.

---

## 2. `LOCAL_EVENTS` / `SERVICE_EVENTS` (lines 1705–1712)

```
1705:   LOCAL_EVENTS=${MORI_CGROUP_LOCAL_EVENTS:-${CGROUP_EVENTS%.events}.events.local}
1706:   SERVICE_EVENTS=${MORI_CGROUP_SERVICE_EVENTS:-/sys/fs/cgroup/user.slice/user-$(id -u).slice/user@$(id -u).service/memory.events}
1707:   service_oom_kill=''
1708:   if [ -r "$LOCAL_EVENTS" ]; then
1709:     service_oom_kill=$(cgroup_field "$LOCAL_EVENTS" oom_kill)
1710:   elif [ -r "$SERVICE_EVENTS" ]; then
1711:     service_oom_kill=$(cgroup_field "$SERVICE_EVENTS" oom_kill)
1712:   fi
```

- **File for `local_oom_kill`:** `LOCAL_EVENTS` = `<sibling of CGROUP_EVENTS>.events.local`, i.e. by
  default `/sys/fs/cgroup/user.slice/user-1000.slice/memory.events.local` — the parent slice's own
  *local* counter (kills in that cgroup only, excluding descendants).
- **Preference order:** `LOCAL_EVENTS` → `SERVICE_EVENTS` → nothing. Strictly `if/elif`: when the
  local file is readable the service file is never opened.
- **When `LOCAL_EVENTS` is unreadable:** silent fallback to `SERVICE_EVENTS` (1710–1711). Nothing is
  emitted and no field records that the local read failed or that the service file was used.
  - Both unreadable → `service_oom_kill=''` → the row prints `local_oom_kill=unavailable` and no
    OOM finding fires (measured, case D below).
  - `-r` cannot tell *absent* from *present-but-mode-000*. This contradicts the census's own stated
    rule two functions later:
    ```
    1747:    # Present but not readable is a DIFFERENT fact from absent, and the state
    1748:    # field must not claim the file does not exist (measured: a mode-000
    1749:    # MORI_CGROUP_PRESSURE was reported `absent` before this branch existed).
    ```
    The pressure branch (1745–1753) and the peak branch (`-r`/`-e`, 1827–1834) both respect that
    rule; the events branch does not.
- **Name inversion inside the code:** the variable that receives a *local* read is called
  `service_oom_kill` (1709), and that same variable is printed as `local_oom_kill=` (1844, 1862). The
  internal name and the printed name denote different levels; the printed one can be false.

Measured (all `EXIT=1`, DRIFT from other surfaces; only cgroup tokens shown):

| case | LOCAL_EVENTS | SERVICE_EVENTS | row token |
|---|---|---|---|
| B | readable, `oom_kill=0` | readable, `oom_kill=3` | `local_oom_kill=0` (no finding) |
| C | readable, `oom_kill=7` | readable, `oom_kill=3` | `local_oom_kill=7` |
| D | absent | absent | `local_oom_kill=unavailable` |
| E | present, mode 000, `oom_kill=7` | readable, `oom_kill=3` | `local_oom_kill=3` |

Case E is the discriminating one: the local file holds `7`, is unreadable, and the row reports the
service file's `3` under the name `local_oom_kill`.

---

## 3. `emit_finding CGROUP_OOM_KILL` (line 1844): value vs path

```
1842:   # presence flag semantics (tsukuroi note): oom_kill is a flag/counter, not a meter to clear
1843:   if [ -n "$service_oom_kill" ] && [ "$service_oom_kill" -gt 0 ] 2>/dev/null; then
1844:     emit_finding CGROUP_OOM_KILL crit "local_oom_kill=$service_oom_kill path=${LOCAL_EVENTS} (local counter: kills in this cgroup only)"
1845:     st=drift
1846:   elif [ "$oom_kill" -gt 0 ] 2>/dev/null; then
1847:     emit_finding CGROUP_OOM_KILL_CUMULATIVE info "parent_slice_oom_kill=$oom_kill service_scope_oom_kill=${service_oom_kill:-unavailable} note=cumulative boot counter; attribute the event before treating it as fleet evidence"
1848:   fi
```

- **Value:** `$service_oom_kill` — the if/elif result from 1708–1712, i.e. *either* level.
- **Path:** `path=${LOCAL_EVENTS}`, **hard-wired** to the local path regardless of which file was
  read. The parenthetical then asserts the level: `(local counter: kills in this cgroup only)`.
- Therefore the printed path **can name a file the value was not read from.** Two shapes, both
  constructed and executed against a fixture tree under my TMPDIR (census run directly with
  `MORI_CGROUP_*` overrides; `MORI_CGROUP_EVENTS` = parent `memory.events` with `oom_kill=0` so the
  cumulative branch stays quiet):

**(A) local file absent, service file readable.** The printed path does not exist at all.

```
$ printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 3\noom_group_kill 0\n' > $FX/cgroup/service-scope-memory.events
$ test -e $FX/cgroup/memory.events.local; echo $?      # 1 → absent
$ env MORI_CGROUP_EVENTS=…/memory.events \
      MORI_CGROUP_LOCAL_EVENTS=…/memory.events.local \
      MORI_CGROUP_SERVICE_EVENTS=…/service-scope-memory.events … ./tools/mori-census.sh
EXIT=1
FINDING CGROUP_OOM_KILL severity=crit obs=local_oom_kill=3 path=…/ScoutCensusBytes/fx-misattrib/cgroup/memory.events.local (local counter: kills in this cgroup only) ts=2026-10-25T10:41:38Z script_sha256=87b8d680…
SURFACE cgroup: drift (cmd=…; oom_kill=0 oom=0 high=0 max=0 current=refused:outside-sysfs-cgroup; local_oom_kill=3 …)
```

**(E) local file present but unreadable, with a *different* value.** Here the printed path's own
bytes contradict the printed value: the path contains `oom_kill 7`, the finding says `3`.

```
$ cp local7.events unreadable7.events; chmod 000 unreadable7.events
$ test -r unreadable7.events; echo $?   # 1 (UNREADABLE);  test -e … → 0 (exists)
$ … MORI_CGROUP_LOCAL_EVENTS=…/unreadable7.events MORI_CGROUP_SERVICE_EVENTS=…/svc3.events …
EXIT=1
FINDING CGROUP_OOM_KILL severity=crit obs=local_oom_kill=3 path=…/ScoutCensusBytes/unreadable7.events (local counter: kills in this cgroup only) …
```

Control (C) proves the defect is specifically the fallback: with the local file readable and
`oom_kill=7` while the service file holds `3`, the same line prints the correctly attributed
`local_oom_kill=7 path=…/local7.events`.

**(F) The output cannot distinguish the levels at all.** Two runs whose `local_oom_kill` came from
different files are byte-identical after `ts=` normalization:

```
F1: LOCAL readable (oom_kill=3), SERVICE oom_kill=9  → local_oom_kill=3   (3 ⇒ LOCAL was read)
F2: same LOCAL path chmod 000 (contents 3), SERVICE oom_kill=3 → local_oom_kill=3  (⇒ SERVICE was read)
$ for f in F1 F2; do sed -E 's/ts=[^ ;)]*/ts=<V>/g' $f.out > $f.norm; done
$ diff -u F1.norm F2.norm && echo IDENTICAL
IDENTICAL: the two runs are byte-equal after ts normalization
```

Both print `path=…/level-A.events`; in F2 that file was never opened. So the
`path=`+parenthetical pair is not evidence of provenance.

The same ambiguity is carried by the informational sibling at 1847
(`service_scope_oom_kill=${service_oom_kill:-unavailable}`), which labels the *local* read as
service scope when the local file is readable — the inversion of `local_oom_kill=` at 1844.

---

## 4. Selftest cgroup level pins (lines 3252–3254)

```
3252:       MORI_CGROUP_EVENTS="$FX/cgroup/memory.events"
3253:       MORI_CGROUP_SERVICE_EVENTS="$FX/cgroup/memory.events"
3254:       MORI_CGROUP_LOCAL_EVENTS="$FX/cgroup/memory.events"
```

All three level pins point at the **same file**. Set once in `sut_env`, never overridden per case
(`grep -n "MORI_CGROUP_LOCAL_EVENTS\|MORI_CGROUP_SERVICE_EVENTS"` returns only 3253/3254 plus the
definitions at 1705/1706). The fixture only ever creates that one events file:

```
3190:     printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\noom_group_kill 0\n' > "$d/cgroup/memory.events"
3906:   printf 'low 0\nhigh 0\nmax 0\noom 1\noom_kill 1\noom_group_kill 0\n' > "$FX/cgroup/memory.events"
4371:   rm -f "$FX/cgroup/memory.events"
```

`memory.events.local` is never created, and 4371 deletes the shared events file — which makes
`probe_cgroup` return at 1683–1687 *before* reaching 1705, so the `elif` at 1710 is unreachable in
every selftest case.

**No case can distinguish the levels.** The only cgroup OOM check asserts a bare finding id:

```
3906:   printf 'low 0\nhigh 0\nmax 0\noom 1\noom_kill 1\noom_group_kill 0\n' > "$FX/cgroup/memory.events"
3907:   check 'drift: CGROUP_OOM_KILL' 1 DRIFT \
3908:     'FINDING CGROUP_OOM_KILL'
```

Proved by mutation on copies in my TMPDIR (lane file untouched, digest above unchanged):

```
control  (unmutated copy)                       → EXIT=0  MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)
M1  delete lines 1710–1711 (service fallback)   → EXIT=0  MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)
M2  1844: path=${LOCAL_EVENTS} → ${SERVICE_EVENTS} → EXIT=0  MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)
M3  1844: local_oom_kill=$service_oom_kill → 0  → EXIT=0  MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)
```

M1 removes an entire level of the acquisition; M2 and M3 rewrite the two tokens of the finding that
claim a level and a value; all three leave 134/134 PASS. So `--selftest` pins *that a
`CGROUP_OOM_KILL` line appears*, never *which file it came from* or *what number it carries*.

---

## Verdict — measured vs inferred

**Measured** (byte quotes or executed with exit codes above): the row emits no `path=` and no token
naming the level of `oom_kill`; the only level-naming field is `mem_fill_scope`; `local_oom_kill`
is filled from `LOCAL_EVENTS` if readable else `SERVICE_EVENTS`, with no disclosure of the fallback
and no absent/unreadable distinction; `emit_finding CGROUP_OOM_KILL` hard-wires
`path=${LOCAL_EVENTS}` while printing a value that may come from `SERVICE_EVENTS`, and I produced two
concrete runs where that pair is false — one naming a nonexistent file, one naming a mode-000 file
whose own `oom_kill` is `7` while the finding printed `3` — plus a pair of runs that are byte-identical
although the value came from different files; and the selftest pins all three cgroup levels to one
file, so deleting the service fallback, or rewriting the finding's path and value tokens, still
yields `PASS (134 cases, 134 passed, 0 failed)`. **Inferred** (code reading only, not run): that the
default `memory.events.local` of the parent slice is in practice unreadable on a live host (it is a
readable file normally, so the fallback is usually silent and harmless — the false `path=` only bites
on the fallback path, or on a mode-000/overridden local file); and that `--drift` cannot surface a
level change, which follows from `DRIFT_COUNTER_KEYS` containing `local_oom_kill` and
`drift_normalize` masking its digits, not from a drift run I executed. **Unresolved for C3:** whether
an entry asserting "the census names its cgroup level" is admissible — on this evidence the row names
one level (`mem_fill_scope`) truthfully and one level (`local_oom_kill`) untruthfully under fallback,
so an entry must assert the *fallback* fact, not a general "level is named" fact, or it is
refuted by case E above.
