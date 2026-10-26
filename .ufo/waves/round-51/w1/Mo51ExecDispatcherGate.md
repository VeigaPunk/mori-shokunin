# Mo51ExecDispatcherGate — adjacency: how the fleet gates on MemAvailable, versus the entry's Reading rules

Seat: `Mo51ExecDispatcherGate` (executor, dispatched — not an independent judge).
Item: adjacency check, read-only. Find where the fleet orchestration reads `MemAvailable`, quote the parse, the
units and the threshold, quote what happens on a parse failure, and compare with
`corpus/knowledge/memavailable-estimate-r51.md` §Reading rules (`:44-55`). Report only; the dispatcher is
orchestrator-owned and mori never edits it.
Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin`. Fleet root: `/home/vgpnk/Projects/shokunin`.
Scratch: `/fast/scratch/hyaku/mori-r51/Mo51ExecDispatcherGate/` (created with `mkdir -p`, `TMPDIR` set to its
`tmp/`, largest artefact 40 K, removed at the end; nothing under `/tmp` is cited). Disk guard before the work:
`bash scripts/hyaku/disk-guard.sh status` → rc 0, `/fast` 603 G free (25 % used) — no ENOSPC.

Subject bytes (working tree clean against HEAD, so the quotes below are the committed state):

```
$ git -C /home/vgpnk/Projects/shokunin rev-parse HEAD
34a47b1ad6bd55d135b80f9c55ae55aae76fa4c0
$ git -C /home/vgpnk/Projects/shokunin log -1 --format='%H %ad %s' --date=short -- scripts/hyaku/inline-dispatcher.py scripts/hyaku/wave-slot.sh
717d28da0e6f953b59eba70c73614d9b4f44728e 2026-10-26 hyaku dispatcher: append host guard to every seat prompt (…)
$ git -C /home/vgpnk/Projects/shokunin status --porcelain -- scripts/hyaku/inline-dispatcher.py scripts/hyaku/wave-slot.sh
(no output)
$ sha256sum scripts/hyaku/inline-dispatcher.py scripts/hyaku/wave-slot.sh
e6b689bd04e3c9fb033ceb818aace3e2f83155a46609956cffebeeffd076d041  scripts/hyaku/inline-dispatcher.py
41b487ef51012c099ab704e8c226f3bb701e11c120f7c6973ab73cb1f3737a81  scripts/hyaku/wave-slot.sh
```

The whole-gate mechanism landed in one commit, `216cfd36` (2026-10-26 12:30:54 -0300,
`git log -S'MemAvailable' -- scripts/hyaku/inline-dispatcher.py`), i.e. the same day as the entry's sources.

## 1. Where the fleet reads MemAvailable — exactly two readers

`grep -rn MemAvailable --include=*.py --include=*.sh --include=*.json --include=*.md scripts/` matches only:

| reader | line | role |
|---|---|---|
| `scripts/hyaku/inline-dispatcher.py` | `:129-140` (`host_ok`), called at `:243` | in-session dispatcher: gates seat spawns of a wave (`register()`), sampled once per tick before a tranche |
| `scripts/hyaku/wave-slot.sh` | `:68` (`mem_avail_mb`), used at `:80`, `:87`, `:101` | L1-side global seat grant: `acquire` waits while the floor is unmet |

`scripts/hyaku/wave-slot-selftest.sh:177` sets `HYAKU_WAVE_MIN_AVAIL_MB="0"` but asserts nothing about the number.
No other fleet script (`ready-watch.sh`, `disk-guard.sh`, `wave-live.py`, `shokunin-watchdog.sh`) reads memory.
The L1 spawn (`spawn_l1`, `:201-206`) and closure spawn (`spawn_closure`, `:208-215`) call no host gate at all —
only the wave-seat path at `:243` does (see F6).

## 2. How each reader parses the line

### inline-dispatcher.py (`:132-138`, verbatim)

```python
def host_ok():
    """True while the host can take more seats (1-min load and MemAvailable within bounds)."""
    try:
        load1 = float(open('/proc/loadavg').read().split()[0])
        mem_gb = next(int(l.split()[1]) for l in open('/proc/meminfo') if l.startswith('MemAvailable:')) / 1048576
    except (OSError, ValueError, StopIteration):
        return True
    if load1 > LOAD_MAX or mem_gb < MEM_MIN_GB:
        dlog('host-pressure', f'load1={load1}', f'mem_avail_gb={mem_gb:.1f}')
        return False
    return True
```

- Input unit: kB — field 2 of the `MemAvailable:` line is parsed with `int(...)` and the `kB` suffix in field 3 is
  not read or checked.
- Divisor `1048576` = 1024 × 1024 = kB per **GiB**. So `mem_gb` is GiB: this is a *correct* kB→GiB conversion, and
  no 1000-vs-1024 scaling error exists in the arithmetic.
- Threshold: `MEM_MIN_GB = float(os.environ.get('HYAKU_MEM_MIN_GB', '4'))` (`:112`); the comparison is
  `mem_gb < MEM_MIN_GB`, so exactly 4.000 GiB passes and 4 GiB − 1 kB is blocked.
- Naming: the variable is called `_GB`, the log field `mem_avail_gb`, and the env var `HYAKU_MEM_MIN_GB`, but the
  number held is GiB (F1).

### wave-slot.sh (`:68`, verbatim)

```bash
mem_avail_mb() { awk '/^MemAvailable:/ {print int($2 / 1024)}' /proc/meminfo; }
```

- Input unit: kB — `$2` of the `MemAvailable:` line; suffix unchecked.
- Divisor `1024` = kB per **MiB**, and `int()` truncates downward. So `m` is MiB, named `MB` (F1).
- Threshold `MIN_AVAIL_MB=${HYAKU_WAVE_MIN_AVAIL_MB:-6144}` (`:21`); the arm is
  `if fits_cap "$used" "$CAP" && [ "$m" -ge "$MIN_AVAIL_MB" ]` (`:80`) — integer, inclusive.

### Threshold table (arithmetic reproduced from both source expressions, `python3`, scratch)

| MemAvailable | dispatcher `mem_gb` | vs floor 4 GiB | wave-slot `m` (MiB) | vs floor 6144 |
|---|---|---|---|---|
| 4194304 kB (4 GiB exactly) | 4.000000 | allow | 4096 | hold |
| 4194303 kB (4 GiB − 1 kB) | 3.999999 | **block** | 4095 | hold |
| 4000000 kB (**4.000 GB** decimal) | 3.814697 | **block** | 3906 | hold |
| 4718592 kB (4.5 GiB) | 4.500000 | allow | 4608 | hold |
| 6291455 kB (6 GiB − 1 kB) | 5.999999 | allow | 6143 | **hold** |
| 6291456 kB (6 GiB exactly) | 6.000000 | allow | 6144 | grant |
| 18303504 kB (this host now) | 17.455627 | allow | 17874 | grant |

Read: 4 GiB = 4194304 kB vs 4 GB = 4000000 kB → a floor written “4 GB” is 1.0737× **stricter** than decimal 4 GB
(194304 kB of headroom dropped). 6144 “MB” = 6144 MiB = 6.000 GiB = 6.442 GB, i.e. the `/ MB` label understates the
floor in decimal terms by 4.6 % and the dispatcher's floor by 2 GiB (F3).

## 3. What each reader does on a parse failure

Probes below run the *source expressions* (not the live files' readers) against synthetic meminfo bodies, in
`/fast/scratch/hyaku/mori-r51/Mo51ExecDispatcherGate/`, bash 5.3.20(1)-release. The dispatcher expression was
extracted by reading file line 133 and evaluated with `open` replaced by an in-memory body; the awk expression is
`wave-slot.sh:68` with the path argument replaced.

```
dispatcher file line 133 verbatim: mem_gb = next(int(l.split()[1]) for l in open('/proc/meminfo') if l.startswith('MemAvailable:')) / 1048576
normal 16 GiB          -> (16.0, 'allowed')
exactly 4 GiB          -> (4.0, 'allowed')
just under 4 GiB       -> (3.9999990463256836, 'blocked')
4.0 GB decimal         -> (3.725290298461914, 'blocked')
missing line           -> ('fail-open->True', 'StopIteration')
empty value            -> ('fail-open->True', 'ValueError')
```

- Dispatcher, line missing (`StopIteration`), empty/garbage value (`ValueError`), or `/proc/meminfo` unreadable
  (`OSError`): `host_ok()` returns **True** — the memory arm (and the load arm, read in the same `try`) is silently
  disabled, and nothing is logged on that path. Fail-open, silent (F2).
- wave-slot, line missing: `awk` prints nothing, so `m=""`; `[ "$m" -ge "$MIN_AVAIL_MB" ]` errors and is false:

```
$ bash probe.sh            # exact shape of wave-slot.sh:68 + :80
file=full.meminfo m=[6144] verdict=grant
file=noline.meminfo m=[] probe.sh: line 9: [: : integer expected
verdict=hold test_rc=2
file=boundary.meminfo m=[6143] verdict=hold test_rc=1
script_rc=0
```

  Acquire therefore neither grants nor dies: it re-tests every 20 s until the deadline and then prints
  `timeout … mem_avail_mb= min=6144` and exits 3 (`:87`). Fail-closed.
- wave-slot, `/proc/meminfo` unreadable: `awk` exits 2, the assignment `m=$(mem_avail_mb)` fails and `set -euo
  pipefail` (`:17`) aborts the script with rc 2 — the same code `die()` uses, with no `wave-slot:` message
  (`awk: fatal: cannot open file … for reading` on stderr, observed rc 2).
- Dispatcher, bad *configuration*: `float()` at `:112` runs at `%load` time, so `HYAKU_MEM_MIN_GB=4gib` raises
  `ValueError: could not convert string to float: '4gib'` while the module is being loaded — the gate has no
  fallback (F4).

## 4. Against the entry's Reading rules (`corpus/knowledge/memavailable-estimate-r51.md:44-55`)

| entry rule | line | dispatcher | wave-slot | verdict |
|---|---|---|---|---|
| read `MemAvailable` itself; never rebuild it as `MemFree + Cached` | `:46-47` | reads `MemAvailable` only | reads `MemAvailable` only | **agree** — `grep -rn "MemFree\|Cached:" scripts/` → no match |
| the figure excludes swap; 0 is a clamp, not an exact zero | `:48-49` | `mem_gb < 4` → a clamped 0 blocks; swap never read | `0 -ge 6144` false → holds; swap never read | **agree** in behaviour, but see F5 (swap headroom ignored, unlabelled) |
| units are kB on every line; a ratio is unit-free | `:50` | parses kB, divides by 1048576 → GiB | parses kB, divides by 1024 → MiB | **units right, labels wrong** (F1): neither reader checks the `kB` field, both label the result with decimal `GB`/`MB` |
| compare `Shmem` when `Cached` is large but `MemAvailable` small | `:51-52` | not read | not read | not applicable to a gate (no diagnostic path needs it) — informational |
| a runway threshold is a threshold on a model; report it as local | `:53-55` | `MEM_MIN_GB` default 4 | `MIN_AVAIL_MB` default 6144 | **agree in the goal file, not in the identifiers** — `.scratch/goal-20261026-hyaku-run9.md:60` says “MemAvailable < 4 GiB (`MEM_MIN_GB`)”, so the run-9 record names GiB while the env var says GB; `.ufo/waves/hyaku/PHASE2.md:503` gives `6144` with no unit at all |

Answer to the item's question “is there a GiB/GB conversion error?”: **no scaling error** — 1048576 kB/GiB and
1024 kB/MiB are the correct binary factors for a kB input, and both readers honour the entry's kB rule. The mismatch
is one of *labels and idioms*: a `_GB`-named knob whose value is compared in GiB, and a `_MB`-named knob whose value
is in MiB, so an operator who tunes in the units the names advertise moves the effective floor by 7.4 %/4.6 % — or,
if they use the sibling gate's idiom (a four-digit MB value), disables spawning permanently (F1, F4).

## 5. Reproduce

```bash
# quotes and call sites
grep -n "MemAvailable" /home/vgpnk/Projects/shokunin/scripts/hyaku/inline-dispatcher.py /home/vgpnk/Projects/shokunin/scripts/hyaku/wave-slot.sh
sed -n '108,140p' /home/vgpnk/Projects/shokunin/scripts/hyaku/inline-dispatcher.py
sed -n '66,68p;78,88p' /home/vgpnk/Projects/shokunin/scripts/hyaku/wave-slot.sh
# unit arithmetic (read-only)
python3 -c 'R=1048576; print(4*1024**2, 4*10**6, (4*1024**2)/(4*10**6), 4*1024**3/4e9, 6144*1024**2/1024**3, 6144*1024**2/1e9)'
# wave-slot gate shape on a synthetic meminfo (no host file touched)
S=/fast/scratch/.../Mo51ExecDispatcherGate; printf 'MemTotal: 1 kB\n' > $S/noline.meminfo
m=$(awk '/^MemAvailable:/ {print int($2 / 1024)}' $S/noline.meminfo); [ "$m" -ge 6144 ]; echo rc=$?   # rc=2, "integer expected"
# the dispatcher expression with the file replaced by a synthetic body: see §3 (missing line -> StopIteration -> True)
```

## 6. Limits and unverified

- I did **not** execute `inline-dispatcher.py` (it is a `%load` session file: no `__main__`, needs `agent()`/session
  globals) nor `wave-slot.sh` (`acquire`/`status` write `~/.local/state/shokunin-hyaku`: ledger, lock, `mkdir -p`).
  Both were read and their expressions were replayed on synthetic input. UNVERIFIED: the live gate's behaviour
  inside the orchestrator session.
- UNVERIFIED whether `HYAKU_MEM_MIN_GB` / `HYAKU_WAVE_MIN_AVAIL_MB` are set in the running orchestrator session
  (reading a session's environment would touch session material; not done). The defaults 4 and 6144 are what the
  code says.
- Both readers were checked on the present kernel only (`/proc/meminfo` here has the line). The missing-line path is
  exercised only against a synthetic file; no kernel/host was observed without `MemAvailable`.
- The `/ MB` and `/ GB` labels are a naming observation about the fleet, not a claim about this host's values.

## Findings

1. **MED — `scripts/hyaku/inline-dispatcher.py:133` fails open and silently.** `except (OSError, ValueError,
   StopIteration): return True` disables the memory *and* load arms with no `dlog` when `/proc/meminfo` lacks the
   line, has an unparseable value, or is unreadable (observed: `StopIteration`, `ValueError` → True). The documented
   run-9 host gate then does not exist, and no log line says so. The sibling gate `wave-slot.sh:80` fails closed on
   the same input, so the two gates disagree on the failure direction.

2. **MED — `scripts/hyaku/inline-dispatcher.py:112,133,136,137` name GiB as GB, and any float is accepted as GiB.**
   `mem_gb` = kB / 1048576 is GiB; the knob is `HYAKU_MEM_MIN_GB` and the log field `mem_avail_gb`. With the live
   reading 17.46 GiB: `HYAKU_MEM_MIN_GB=4096` (the sibling gate's MB idiom) or `6144` blocks every wave forever
   (rate-limited only by tick cadence), and `0` disables the memory arm with no warning. `4` (decimal-GB reading)
   is really 4 GiB, 7.37 % stricter than intended. `.scratch/goal-20261026-hyaku-run9.md:60` says “4 GiB
   (`MEM_MIN_GB`)”, so the run record and the identifier disagree.

3. **MED — the two gates hold different floors on the same quantity:** dispatcher 4 GiB (`inline-dispatcher.py:112`)
   vs wave-slot 6144 MiB = 6 GiB (`wave-slot.sh:21`). In the 4–6 GiB band the dispatcher spawns a wave's seats while
   an L1 calling `acquire` for the same wave is held, so “the gate” is not one number (observed band 4194304–6291455 kB).

4. **LOW — `scripts/hyaku/wave-slot.sh:68,21` label MiB as MB** (`int($2 / 1024)` → MiB; env
   `HYAKU_WAVE_MIN_AVAIL_MB`, status field `mem_avail_mb=`). 6144 is 6 GiB = 6.442 GB; `.ufo/waves/hyaku/PHASE2.md:503`
   repeats `6144` with no unit. `int()` also truncates, so 6291455 kB (6 GiB − 1 kB) reports 6143 MiB and holds.

5. **LOW — neither gate sizes its floor to the wave it admits.** `inline-dispatcher.py:243` samples `host_ok()` once
   per tick per wave and then spawns up to `SEAT_CEILING − occupied` seats (`:250-260`) with no re-check;
   `wave-slot.sh:80` compares `mem_avail_mb` to a constant that is independent of `seats` (only `fits_cap` sees the
   seat count). A 128-seat wave and a 2-seat wave clear the same 4/6 GiB floor, and a spike inside the tranche is
   invisible to the gate.

6. **LOW — the floor is not applied to the L1/closure spawn path.** `host_ok()` has one call site (`:243` in
   `register()`); `spawn_l1` (`:201-206`) and `spawn_closure` (`:208-215`) spawn regardless of `MemAvailable` and of
   `LOAD_MAX`. The comment at `:110` says 4 slots are reserved below `HOST_JOB_CAP`, not that these spawns skip the
   memory floor.

7. **LOW — swap headroom is ignored and not shown.** Both gates read `MemAvailable` alone; the entry (`:48-49`) says
   a host with free swap keeps running past 0, so the gates are conservative — but the only diagnostic
   (`host-pressure` at `:137`) prints `load1` and `mem_avail_gb` only, and the `timeout` line at `wave-slot.sh:87`
   prints `mem_avail_mb= min=` only, so an operator cannot tell a real exhaustion from a hold on a clamped or
   swap-backed host. Matches the entry's `:53-55` rule that the threshold is local; the logs do not carry that
   qualification.

8. **LOW — the memory arm has no test.** `wave-slot-selftest.sh:177` forces `HYAKU_WAVE_MIN_AVAIL_MB="0"`, so no
   assertion exercises the kB→MiB divisor, the inclusive boundary, or the missing-line path; the dispatcher has no
   harness at all (`host_ok` appears only in `scripts/hyaku/inline-dispatcher.py` and two narrative reports). The
   `MB`/`GB` label defect (F1/F4) is therefore free to persist.

No counter, predicate, floor or kill rule is proposed for change here; the dispatcher and `wave-slot.sh` are
orchestrator-owned and this report only names what an operator should know.
