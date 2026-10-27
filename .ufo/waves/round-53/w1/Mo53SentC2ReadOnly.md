# Mo53SentC2ReadOnly — safety review of `tools/mori-commit-runway.py`

Seat type: sentinel (detection and report only; no edits to lane files).
Surface: `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-commit-runway.py` at data commit
`2a4213bf8da72f7cd78189baa5bb9be825dca1df` (lane HEAD `95cf78eef71979f9b740ef6bc3c5299b6beff86e`).
Bytes reviewed: `sha256sum tools/mori-commit-runway.py` → `80cb169650bf02578439703bc006173aab7b759ff9cf57337611b27164676156`;
`git show 2a4213bf…:tools/mori-commit-runway.py | sha256sum` → the same hash, so the working-tree bytes are the
committed bytes (316 lines). Host at probe time: `MemTotal 31721796 kB`, `MemAvailable 16415684 kB`,
`CommitLimit 47583772 kB`, `Committed_AS 41708124 kB` (drifting under sibling load), `overcommit_memory = 0`.

Method: every probe ran `/usr/bin/python3 -I -B <tool>` from `/fast/scratch/hyaku/mori-r53/Mo53SentC2ReadOnly`
under `resource.setrlimit(RLIMIT_AS)` in the child (`preexec_fn`), killed by `timeout`/`killpg`, with peak RSS
read from `getrusage(RUSAGE_CHILDREN).ru_maxrss` (one child per harness process). GNU `/usr/bin/time` is absent
on this host and pacman is paused host-wide, so nothing was installed; `getrusage` gives the same VmHWM figure.
No sysctl, cgroup, swap or watermark was written; all fixtures live in the seat scratch and are removed at the
end of this report's run.

## 1. Read-only posture — PASS, with one precondition

`strace -f -e trace=openat,open,creat,mkdir,mkdirat,unlink,unlinkat,rename,renameat2,socket,connect,bind,execve`
over two runs (`--selftest` with the committed fixtures, and the default `/proc` read), `TMPDIR` in scratch:

- Write-intent opens outside `$TMPDIR/mori-commit-runway-*` (and `tempfile`'s own single probe file in
  `$TMPDIR`): **NONE**.
- `socket(` count **0**, `connect(` count **0**. `execve(` count **1** (the interpreter itself) → no subprocess.
  Static confirmation: the only imports are `argparse, json, os, re, shutil, sys, tempfile`; no `socket`,
  `subprocess`, `urllib`, `http`, `os.system`, `popen`, `execl` anywhere in the file.
- The default read opens exactly, all `O_RDONLY`: `/proc/meminfo`, `/proc/sys/vm/{overcommit_memory,
  overcommit_ratio,overcommit_kbytes,admin_reserve_kbytes,user_reserve_kbytes}`, `/sys/devices/system/cpu/present`,
  plus the script itself and the loader's locale/gconv/tzdata files.
- `unlinkat`/`AT_REMOVEDIR` lines are all inside the mkdtemp root (`present`, the five `vm/*`, `vm`,
  `<case>`), i.e. `shutil.rmtree(root)`.

`--selftest` under `python3 -I -B` with `TMPDIR` in scratch:

```
MATCHER: rejected 23/23 corrupted expectations
MORI_COMMIT_RUNWAY_SELFTEST: PASS 23/23
exit=0
```

(23 cases, not the "frozen 16" the control prose mentions; `cases` length printed as 23, ids contain no `/` and
none start with `.`.)

Isolation is genuine: with a `json.py` that raises `SystemExit("shadow json imported")` in the cwd, the tool run
from that cwd with `-I -B` still printed its reading (`{"band_kb": null, … "verdict": "COMMIT_HEURISTIC" …}`, rc 0)
— the shadow module is not imported, and the fixture path is resolved from `os.path.realpath(__file__)` (line 203)
rather than from `sys.path`, so nothing depends on the import path.
`-B` is honoured: no `tools/__pycache__` exists after all runs and the strace shows no `__pycache__` write.

Baseline cost: `exit 0`, wall `0.041 s`, peak RSS `16944 kB`, one JSON object, `verdict COMMIT_HEURISTIC`
(host mode 0).

**Precondition:** read-only holds for the two inputs the tool actually reads (`/proc`, `/sys`) and for the frozen
fixtures. It does **not** hold when the operator points `--meminfo`/`--vm-dir` at a non-regular file or `--cases`
at a hostile cases file (findings 1, 2, 4).

## 2. Hostile-input verdicts

| # | input (all under scratch) | verdict | exit | wall | peak RSS |
|---|---|---|---|---|---|
| 1 | defaults (`/proc`, `/sys`) | safe, correct JSON | 0 | 0.041 s | 16 944 kB |
| 2 | `--meminfo <directory>` | safe: `COMMIT_UNKNOWN`, note `unreadable (Is a directory)` | 2 | 0.037 s | 16 560 kB |
| 3 | `--meminfo <symlink loop>` (`loopa -> loopb -> loopa`) | safe: `COMMIT_UNKNOWN`, note `unreadable (Too many levels of symbolic links)` | 2 | 0.038 s | 17 096 kB |
| 4 | `--meminfo /dev/zero` (AS cap 512 MiB) | **UNBOUNDED**: dies with `MemoryError` in `_read`, no JSON | 1 | 0.135 s | **467 644 kB** growing ~3.4 GB/s |
| 5 | `--meminfo <FIFO, no writer>` | **HANGS** in `open()` until killed | killed at 10.012 s | — | 17 116 kB |
| 6 | `--meminfo <FIFO with writer, valid bytes>` | safe: correct JSON | 0 | 0.065 s | 16 880 kB |
| 7 | `--meminfo <FIFO, endless 262 MB stream>` (cap 1024 MiB) | **UNBOUNDED**: still growing at kill | killed at 6.02 s | — | 269 652 kB and rising |
| 8 | `--meminfo <2 GiB sparse file>` (AS cap 2048 MiB) | **cannot process**: needs ≥ file size in address space, `MemoryError` in `_read` | 1 | 0.049 s | 17 364 kB (VA refused) |
| 9 | `--meminfo <256 MiB sparse file>` | 2.1× input in RSS, then `COMMIT_UNKNOWN` | 2 | 0.713 s | 540 764 kB |
| 10 | `--meminfo <100 MiB single line>` | 2.2× input in RSS, exit 0 | 0 | 0.749 s | 221 036 kB |
| 11 | `--meminfo <MemTotal with 5000 digits>` | **contract breach**: `ValueError` escapes → traceback | 1 | 0.043 s | 17 424 kB |
| 12 | `--vm-dir <dir with FIFO overcommit_memory, no writer>` | **HANGS** like 5 | killed at 8.011 s | — | 16 816 kB |
| 13 | `--page-kb 4611686018427387904` | accepted; `limit_recomputed_kb 0`, `limit_mismatch`, exit 0 | 0 | 0.038 s | 17 112 kB |
| 14 | `--selftest --cases <hostile ids>` | writes outside the selftest temp dir (finding 4) | 1 | — | — |

Clean shell receipts for the three worst rows:

```
$ timeout 10 python3 -I -B tools/mori-commit-runway.py --meminfo <scratch>/fx/fifo-nw
rc=124
$ ( ulimit -v 524288; timeout 10 python3 -I -B tools/mori-commit-runway.py --meminfo /dev/zero 2>&1 | tail -4 )
  File ".../tools/mori-commit-runway.py", line 87, in _read
    return f.read()
           ~~~~~~^^
MemoryError
rc=1
$ ( ulimit -v 2097152; timeout 30 python3 -I -B tools/mori-commit-runway.py --meminfo <scratch>/fx/sparse-2g 2>&1 | tail -3 )
    return f.read()
           ~~~~~~^^
MemoryError
rc=1
```

The 2 GiB and 256 MiB rows were run under an explicit `RLIMIT_AS` so that the probe could not OOM the host (the
lane's "never trigger an OOM or a large allocation" rule); the ceiling is reported in the table. Row 8 shows the
tool never reads a 2 GiB input at all — it asks for the whole file in one allocation — and rows 7/9/10 show the
allocation is proportional to input size with a 2.1× factor (unbounded, no cap, no stream termination).

## 3. Draft: smallest bound (for the L1; not applied by this seat)

One helper, replacing lines 84-89, plus two `int()` guards and one case-id guard. This closes findings 1, 2, 3
and 4 without touching any counter, predicate, verdict or reading field.

```python
MAX_READ_BYTES = 64 * 1024   # /proc/meminfo is ~2 KiB; every real input of this tool is < 8 KiB


def _read(path: str) -> str:
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK | os.O_CLOEXEC)
    except FileNotFoundError:
        raise InputError("%s: absent" % path)
    except OSError as exc:
        raise InputError("%s: unreadable (%s)" % (path, exc.strerror or type(exc).__name__))
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise InputError("%s: not a regular file" % path)
        raw = b""
        while len(raw) <= MAX_READ_BYTES:
            chunk = os.read(fd, MAX_READ_BYTES + 1 - len(raw))
            if not chunk:
                break
            raw += chunk
    except OSError as exc:
        raise InputError("%s: unreadable (%s)" % (path, exc.strerror or type(exc).__name__))
    finally:
        os.close(fd)
    if len(raw) > MAX_READ_BYTES:
        raise InputError("%s: larger than %d bytes" % (path, MAX_READ_BYTES))
    try:
        return raw.decode("ascii")
    except UnicodeDecodeError:
        raise InputError("%s: not ascii" % path)
```

- `O_NONBLOCK` makes the FIFO probe return immediately instead of blocking in `open()`; the `S_ISREG` check then
  rejects `/dev/zero`, FIFOs, sockets and directories before a byte is read. `/proc` and `/sys` entries are
  regular files, so the real inputs keep working (`st_size` is not trusted — the loop reads to EOF).
- `int()` guards at line 107 (`parse_meminfo`) and line 133 (`parse_vm_value`): `try: … except ValueError: raise
  InputError("%s: value too long or not decimal" % key)` — this is what row 11 needs (CPython 3.11+ caps int
  parsing at 4300 digits).
- `_materialise` (line 207) needs `if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", case["id"]): raise
  InputError(...)` and `selftest` must turn that `InputError` into a `failed.append(...)` rather than a traceback.
- With those three changes no `MemoryError` path remains, so no `except MemoryError` is needed; the docstring's
  "nothing is written outside the selftest's temporary directory" then becomes true.

## 4. Notes for the C2 claim seats (not a counter change)

- The tool, its fixtures and the entry all behave as the contract interface says for the inputs they are
  designed for (rows 1, 2, 3, 6 of the table; selftest PASS 23/23 under `-I -B`).
- The `COMMIT_LOW`-is-not-an-alarm limit is visible in the source (`notes`, line 192) and unchanged here.
- Observations outside this seat's surface, recorded so they are not lost: `parse_cpulist` counts duplicate
  indices (`0,0` → 2 CPUs, line 115-127) and `--page-kb` accepts any power of two up to 2^62 (row 13), which
  yields a `limit_recomputed_kb` of 0 with exit 0. Neither is a read-only or memory-safety defect.

## Findings

**HIGH — unbounded read of the input file in `_read` (`tools/mori-commit-runway.py:87`, `return f.read()`).**
Evidence: `--meminfo /dev/zero` reached 467 644 kB RSS in 0.135 s under a 512 MiB `RLIMIT_AS` and then died with
an uncaught `MemoryError` (rc 1, no JSON); a 256 MiB file cost 540 764 kB RSS; a 100 MiB single line cost
221 036 kB; an endless FIFO stream reached 269 652 kB in 6 s and was still growing; a 2 GiB file is never read at
all (needs ≥ its size in address space, rc 1). Exploit path: any caller that passes an operator- or
config-supplied path — or a `/proc`/`/sys` path that is swapped for a device or a growing file — makes the
process allocate one buffer the size of the input; on this host (`MemAvailable 16.4 GB`, `Committed_AS 41.7 GB`
under sibling load) a 10 GiB input is an OOM, and the wave loses the tool's verdict entirely (no JSON, rc 1).
Impact: memory exhaustion of the host from a documented read-only tool, plus a false `exit 1` that collides with
`COMMIT_LOW`'s documented code. Remediation: the `MAX_READ_BYTES` helper in §3.

**MED — non-regular `--meminfo`/`--vm-dir` entries block forever in `open()` (`tools/mori-commit-runway.py:86`).**
Evidence: a FIFO with no writer hung the tool until `timeout 10` killed it (`rc=124`, wall 10.012 s, RSS 17 116 kB);
a `--vm-dir` whose `overcommit_memory` is a FIFO hung identically (killed at 8.011 s). Exploit path: a stale FIFO
at a configured path, or a mount that appears but never yields bytes, turns the tool into a hung wave seat with
no output and no exit — the failure mode the lane is supposed to detect, produced by its own instrument.
Remediation: `O_NONBLOCK` + `S_ISREG` gate from §3 (same edits).

**MED — malformed numeric input escapes the `InputError` contract and exits 1 (`tools/mori-commit-runway.py:107`,
`:133`, caught only at `:146`).**
Evidence: `MemTotal: <5000 digits> kB` raises `ValueError: Exceeds the limit (4300 digits) for integer string
conversion` through `parse_meminfo`; the traceback is printed, no JSON object is emitted, and the process exits 1
— the code the interface reserves for `COMMIT_LOW`. The same class covers the `MemoryError` rows above
(`:87`). Impact: a caller that keys on the exit status (the natural reading of `COMMIT_LOW` = 1, `COMMIT_UNKNOWN`
= 2) records a malformed input as "inside the error band", i.e. a fabricated low-runway reading. Remediation: the
two `ValueError → InputError` guards in §3; the exit-code table then stays truthful for every malformed input.

**MED — `--cases` case ids are joined unvalidated, so the selftest writes outside its temporary directory
(`tools/mori-commit-runway.py:207-221`, `_materialise`).**
Evidence: a cases file with `id` = an absolute path had `meminfo`, `present` and the five `vm/*` files created at
that absolute path; `id` = `../../fx/PWN-par` escaped the mkdtemp root the same way, and both trees survived
`shutil.rmtree(root)` (`find` listed `fx/PWN-abs/{meminfo,present,vm/*}`, `fx/PWN-par/{…}` after the run).
Content of every written file is attacker-controlled. The docstring's "nothing is written outside the selftest's
temporary directory" is therefore false for this input. Exploit path: requires the operator to pass a hostile
`--cases` file (the committed fixtures are clean — no id contains `/` and none starts with `.`), so this is not a
remote path; it is a write primitive reachable from any script that forwards a cases path. Remediation: the
single-component id check in §3, plus an `InputError` → `failed.append` in `selftest`.

**LOW — a nonsense `--page-kb` yields a reading with exit 0 (`tools/mori-commit-runway.py:307-308`).**
Evidence: `--page-kb 4611686018427387904` (2^62, a power of two, so it passes the guard) produced
`limit_recomputed_kb 0`, `single_request_cap_kb 0`, `limit_mismatch`, `verdict COMMIT_HEURISTIC`, rc 0. Impact: a
caller mistake is reported as a valid reading rather than `COMMIT_UNKNOWN`; no memory or write consequence.
Remediation (optional, minimal): also require `1 <= page_kb <= 65536`.

**LOW — duplicate CPU indices inflate `cpus_present` (`tools/mori-commit-runway.py:115-127`).** Observation only:
`parse_cpulist("0,0")` returns 2. Not exercised by any fixture and outside this seat's read-only surface; it
would shift `band_kb` and the batch divisor, which is a claim-side question for the C2 seats, not a safety one.

## Hygiene

- Scratch `/fast/scratch/hyaku/mori-r53/Mo53SentC2ReadOnly` (fixtures were 101 MiB on disk, 2.4 GiB apparent; the
  2 GiB and 256 MiB sparse files cost metadata only) removed after this report; `TMPDIR` was inside it for both
  selftest runs and `/tmp/mori-commit-runway-*` is empty. No clone and no git/jj mutation of any repo was made;
  the lane's `git status` is unchanged by this seat (`tools/` clean, no `__pycache__`). Disk guard reported
  `/fast/scratch/hyaku` at 25 % before the heavy rows.
- No tool was installed or upgraded (GNU time is absent; `getrusage` covered the measurement).
