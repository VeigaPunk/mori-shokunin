# Mo53ExecToolPortability — portability of `tools/mori-commit-runway.py` and its fixtures (C2)

Seat: leaf executor, round 53 wave w1. Scope: the tool and fixture file at lane commit
`2a4213bf8da72f7cd78189baa5bb9be825dca1df` (`git log -1 --format='%H %ad' 2a4213bf8... -- tools/mori-commit-runway.py`
→ `2a4213bf… Mon Oct 26 22:31:29 2026 -0300`). All runs from a `git archive` extraction under
`/fast/scratch/hyaku/mori-r53/Mo53ExecToolPortability/` (removed after the runs; every number below was copied into
this file first). No file was created inside the lane except this report; `git ls-files --others --exclude-standard --
tools .ufo/waves/round-53` lists only sibling seat reports and `w1.ready*`, none of mine.

Verdict in one line: the tool is portable on every axis I could exercise — five interpreters, archive/symlink/
read-only/spaced/non-ASCII paths, cwd-independent fixture resolution, `TMPDIR` honoured and cleaned on pass, FAIL and
uncaught-exception paths, no environment dependency (`HOME` unset, `env -i`, `LC_ALL=C`), and `--page-kb 16`/`64` on the
live host exit 0 without crashing. One real defect (MED) and four LOW observations are below; none of them changes what
the C2 counter reads from the committed fixtures.

## 0. Artifact identity (archive == commit bytes)

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive 2a4213bf… tools/mori-commit-runway.py \
      tools/fixtures/mori-commit-runway | tar -x -C .
$ find tools -type f -printf '%m %s %p\n' | sort
644 24910 tools/fixtures/mori-commit-runway/cases.json
755 14785 tools/mori-commit-runway.py
$ git show 2a4213bf…:tools/mori-commit-runway.py | sha256sum
80cb169650bf02578439703bc006173aab7b759ff9cf57337611b27164676156  -
$ sha256sum tools/mori-commit-runway.py
80cb169650bf02578439703bc006173aab7b759ff9cf57337611b27164676156  tools/mori-commit-runway.py
$ git show 2a4213bf…:tools/fixtures/mori-commit-runway/cases.json | sha256sum
cea8045192babe3017a2682c17a1647e73c597eaf0330a27643858577cc43b63  -
$ sha256sum tools/fixtures/mori-commit-runway/cases.json
cea8045192babe3017a2682c17a1647e73c597eaf0330a27643858577cc43b63  tools/fixtures/mori-commit-runway/cases.json
```

`git ls-tree -r 2a4213bf… tools/ | grep mori-commit-runway` → `100644 … cases.json`, `100755 … mori-commit-runway.py`
(executable bit survives `git archive`; direct `./tools/mori-commit-runway.py --selftest` works, rc 0).

Fixture count: `n=23`, ids `host-mode0-over-limit, mode0-under-limit, mode1-over-limit, mode2-ok,
mode2-low-inside-band, mode2-band-edge-equal-is-low, mode2-band-edge-one-page-above, mode2-negative-headroom,
mode2-overcommit-kbytes, mode2-hugetlb-ratio80, mode2-batch-floor-64cpu, mode2-one-cpu, mode2-sparse-cpulist,
mode2-page64, mode0-limit-mismatch, unknown-mode3, unknown-commitlimit-missing, unknown-committed-twice,
unknown-swaptotal-no-unit, unknown-user-reserve-missing, unknown-cpulist-garbage, unknown-cpulist-reversed,
unknown-meminfo-absent`. `cases.json` is ASCII-only, no BOM, no CRLF; source has no CRLF and its non-ASCII bytes are
only in the docstring prose (Python 3 source default UTF-8).

## 1. Interpreters — every `python3.x` present

```
$ ls -l /usr/bin/python3 ; /usr/bin/python3 -V ; /usr/bin/python3.14 -V
lrwxrwxrwx 1 root root 10 Oct  2 07:23 /usr/bin/python3 -> python3.14
Python 3.14.8
Python 3.14.8
$ compgen -c | grep -E '^python3(\.[0-9]+)?$' | sort -u
python3
python3.11
python3.12
python3.13
python3.14
$ command -v python3.11 python3.12 python3.13 ; readlink -f …
/home/vgpnk/.local/bin/python3.11 → …/uv/python/cpython-3.11.17-linux-x86_64-gnu/bin/python3.11   (Python 3.11.17)
/home/vgpnk/.local/bin/python3.12 → …/uv/python/cpython-3.12.15-linux-x86_64-gnu/bin/python3.12   (Python 3.12.15)
/home/vgpnk/.local/bin/python3.13 → …/uv/python/cpython-3.13.16-linux-x86_64-gnu/bin/python3.13   (Python 3.13.16)
```

`/usr/bin` itself carries only the 3.14 interpreter and the `python3` symlink; 3.11–3.13 are uv-managed CPython builds
already on `PATH`. I ran the selftest under all five command names (each `cd /` so the cwd is outside the extraction,
`TMPDIR` = scratch):

```
/usr/bin/python3     --selftest                 MATCHER: rejected 23/23 … SELFTEST: PASS 23/23  rc=0
/usr/bin/python3     -I -B --selftest           MATCHER: rejected 23/23 … SELFTEST: PASS 23/23  rc=0
/usr/bin/python3.14  --selftest                 … PASS 23/23  rc=0
/usr/bin/python3.14  -I -B --selftest           … PASS 23/23  rc=0
python3.11           -I -B --selftest           … PASS 23/23  rc=0
python3.12           -I -B --selftest           … PASS 23/23  rc=0
python3.13           -I -B --selftest           … PASS 23/23  rc=0
```

Syntax floor probe (`ast.parse(src, feature_version=v)`): parses at `(3,7)`, `(3,8)`, `(3,9)`, `(3,10)`, `(3,11)`,
`(3,12)`. Runtime below 3.11 is UNVERIFIED (no such interpreter present); the counter invokes the tool with
`sys.executable -I -B`, so the interpreter that matters in the scored path is whichever runs `count-c2.py` — 3.11
through 3.14 all pass here.

No bytecode is written when `-B` is omitted either: after a no-flag run `find pcopy -name '__pycache__' -o -name
'*.pyc'` printed nothing (the tool is `__main__`, never imported). `-W error` selftest also passes, rc 0.

## 2. `TMPDIR` — honoured, and what it creates

The tool reads no environment variable of its own (`grep -nE 'os\.environ|getenv|expanduser|HOME|TMPDIR'` matches only
the docstring line 47); `TMPDIR` reaches it only through `tempfile.mkdtemp` (line 254). A spy that wraps
`tempfile.mkdtemp`/`shutil.rmtree` shows:

```
created = ['/fast/scratch/hyaku/mori-r53/Mo53ExecToolPortability/tmp/mori-commit-runway-pz5qq0my']
tempdir = /fast/scratch/hyaku/mori-r53/Mo53ExecToolPortability/tmp
exists_after = [False]

snapshot before rmtree:
{'root': '…/tmp/mori-commit-runway-2oizx5pg', 'dirs': 47, 'files': 159,
 'dir_modes': ['700', '755'], 'file_modes': ['644'],
 'entries': ['host-mode0-over-limit', 'mode0-limit-mismatch', 'mode0-under-limit', …]}
```

47 dirs = 1 root (0700) + 23 per-case dirs + 23 `vm/` dirs; 159 files = one file per materialised key. Per-case tree:

```
files= ['host-mode0-over-limit/meminfo', 'host-mode0-over-limit/present',
        'host-mode0-over-limit/vm/admin_reserve_kbytes', 'host-mode0-over-limit/vm/overcommit_kbytes',
        'host-mode0-over-limit/vm/overcommit_memory', 'host-mode0-over-limit/vm/overcommit_ratio',
        'host-mode0-over-limit/vm/user_reserve_kbytes']
```

Cleanup holds on every exit path I could force:

| path | output | leftover in `TMPDIR` |
|---|---|---|
| PASS 23/23 (5 interpreters, sequential) | `PASS 23/23` rc 0 | `''` (empty after each) |
| FAIL 22/23 (one expectation +1) | `FAIL mode2-ok: usable_kb 55040 != 55041` `SELFTEST: FAIL 22/23` rc 1 | none |
| cases file missing | `FAIL cannot load cases ([Errno 2] …)` rc 1 | none (no dir created before load) |
| malformed JSON / no `cases` key | `FAIL cannot load cases (Expecting value: …)` / `('cases')` rc 1 | none |
| uncaught `FileExistsError` (duplicate id) | traceback, rc 1 | none (`finally` rmtree ran) |
| uncaught `KeyError: 'expect'` | traceback, rc 1 | none |

`TMPDIR` variants, all `PASS 23/23` rc 0, nothing left in `/tmp`:

```
TMPDIR=<scratch>/tmp                 honoured, dir under it, removed
TMPDIR="<scratch>/tmp dir" (spaces)  PASS, spaced dir empty afterwards
TMPDIR=/var/tmp/mori-r53-porttest    PASS (other filesystem), empty afterwards
TMPDIR unset (env -i)                PASS; spy shows tempdir=/tmp, created=/tmp/mori-commit-runway-jsri00ve, removed
TMPDIR=<nonexistent>                 PASS; silent fallback to /tmp, removed
TMPDIR=<regular file>                PASS; silent fallback, removed
TMPDIR=<dir chmod 500>               PASS; silent fallback, removed
LC_ALL=C LANG=C                      PASS 23/23 rc 0
umask 077                            PASS 23/23 rc 0
stdin </dev/null                     PASS 23/23 rc 0
env -i /usr/bin/python3 -I -B …      PASS 23/23 rc 0   (no HOME, no TMPDIR, no PATH)
env -u HOME … -I -B …                PASS 23/23 rc 0
```

A concurrency probe ran four selftests at once in one `TMPDIR`: four `PASS 23/23`, four rc 0, `TMPDIR` empty
afterwards (unique `mkdtemp` names). An earlier parallel batch of mine *did* see one live
`mori-commit-runway-rro4vjdw` directory in the shared `TMPDIR` while a sibling run was mid-flight; sequential re-runs
of all five interpreters returned `leftover=''` each time, so that was a concurrent live directory, not a leak.

## 3. Invocation portability

| invocation | result |
|---|---|
| `cd /` then absolute tool path | PASS 23/23 |
| `./tools/mori-commit-runway.py --selftest` (shebang) | PASS 23/23 rc 0 |
| symlink `run-link.py → tools/mori-commit-runway.py` outside the tree | PASS 23/23 rc 0 (`realpath(__file__)` at line 203–204 drives fixture resolution) |
| extraction path with spaces + non-ASCII (`extract space/ünïcode`) | PASS 23/23 rc 0 |
| `chmod -R a-w tools` (read-only tree) | PASS 23/23 rc 0; `touch tools/probe` → `Permission denied` |
| copy without exec bit, `python3 copyroot/tool.py` | PASS 23/23 rc 0 |
| cwd containing a bogus `fixtures/mori-commit-runway/cases.json` | PASS 23/23 (cwd shadows ignored); with explicit `--cases` on the bogus file: `FAIL bogus: exit 2 != 0` rc 1 (as asked) |
| `PYTHONPATH` with a shadowing `json.py`, no `-I` | `shadow json imported` rc 1 (expected: not isolated); same with `-I -B` → PASS 23/23 rc 0 |
| tool alone, no `fixtures/` (single-file `git show` extract) | `FAIL cannot load cases ([Errno 2] …/nofix/fixtures/mori-commit-runway/cases.json)` rc 1 |

So an extraction must carry `tools/fixtures/mori-commit-runway/cases.json` alongside the tool; `git archive` of
`tools/` or of the two paths together satisfies it, and `--cases FILE` overrides.

## 4. Live host with `--page-kb 16` and `--page-kb 64` (and friends)

Host truth: `getconf PAGESIZE` → `4096`; `/proc/sys/vm/overcommit_memory` 0, `overcommit_ratio` 50,
`overcommit_kbytes` 0, `admin_reserve_kbytes` 8192, `user_reserve_kbytes` 131072;
`/sys/devices/system/cpu/present` `0-31`; `MemTotal 31721796 kB`, `SwapTotal 31722876 kB`, `CommitLimit 47583772 kB`,
`Committed_AS 41462020…41520244 kB`, `Hugetlb 0 kB`.

```
default (page 4):
{"verdict":"COMMIT_HEURISTIC","mode":0,"commit_limit_kb":47583772,"committed_as_kb":41462020,
 "headroom_kb":6121752,"limit_recomputed_kb":47583772,"limit_consistent":true,
 "single_request_cap_kb":63444672,"cpus_present":32,"findings":[]}                            rc=0

--page-kb 16:
{… "limit_recomputed_kb":47583760,"limit_consistent":false,
 "findings":[{"id":"limit_mismatch","printed_kb":47583772,"recomputed_kb":47583760}],
 "single_request_cap_kb":63444656,"verdict":"COMMIT_HEURISTIC"}                              rc=0

--page-kb 64:
{… "limit_recomputed_kb":47583680,"limit_consistent":false,
 "findings":[{"id":"limit_mismatch","printed_kb":47583772,"recomputed_kb":47583680}],
 "single_request_cap_kb":63444608,"verdict":"COMMIT_HEURISTIC"}                              rc=0

--page-kb 4:  limit_recomputed_kb=47583772, limit_consistent=true, same as default
--page-kb 1:  limit_recomputed_kb=47583774, limit_consistent=false, rc 0
--page-kb 2:  limit_recomputed_kb=47583774, limit_consistent=false, rc 0
--page-kb 1024: limit_recomputed_kb=47583232, limit_consistent=false, rc 0
--page-kb 3:  {"verdict":"COMMIT_UNKNOWN", … "notes":["--page-kb must be a power of two (got 3)"]}  rc=2
--page-kb 0:  same power-of-two refusal, rc=2
```

No crash, no division by zero, mode 0 keeps `COMMIT_HEURISTIC` rc 0; the only signal that a non-native page size was
used is the `limit_mismatch` finding (the value is not cross-checked against `os.sysconf`, and the `notes` do not say
the page size may be non-native). The tool's arithmetic is internally consistent: page 16 / 64 shift
`limit_recomputed_kb` down by 12 / 92 kB from the printed 4 KiB figure, and pages 1 and 2 agree because every live
value is even in kB.

Live error paths (all `COMMIT_UNKNOWN` rc 2, all reading fields null): `--meminfo /dev/null`
(`meminfo: missing MemTotal,SwapTotal,CommitLimit,Committed_AS`), `--meminfo <a directory>`
(`…: unreadable (Is a directory)`), `--vm-dir /nonexistent` (`/nonexistent/overcommit_memory: absent`),
`--cpu-present /nope` (`/nope: absent`), `--nope`
(`{"schema":"mori-commit-runway-v1","verdict":"COMMIT_UNKNOWN","notes":["usage: unrecognized arguments: --nope"]}`
rc 2). Usage errors print JSON, not argparse prose.

## 5. Absolute-path hygiene

The seat command as written passes an absolute path to `git grep`, which `git grep` cannot resolve (`fatal: … exists
on disk, but not in …`); I used the repo-relative `.ufo/waves/round-53/` instead, same bytes.

```
$ git grep -n '/home/vgpnk' 2a4213bf… -- tools/mori-commit-runway.py \
      tools/fixtures/mori-commit-runway/cases.json .ufo/waves/round-53/
.ufo/waves/round-53/evidence/census-start.txt:1:$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori   # at entering tip 20edafa5 …
.ufo/waves/round-53/evidence/census-start.txt:25:mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
.ufo/waves/round-53/evidence/sweeps.txt:14:$ grep -rilE 'overcommit|CommitLimit|Committed_AS|percpu_counter|v7\.3' /home/vgpnk/Projects/shokuknow/merge/mori | wc -l
```

Classification: **0 hits in the tool and 0 in the fixtures**; all 3 hits are in `.ufo/waves/round-53/evidence/`
receipts and are *prose* — two recorded command lines and one census row (`census-start.txt` is a transcript; line 25
is the census's own path column). None is an executable default. The only absolute path in the tool is the portable
`#!/usr/bin/env python3` shebang (line 1); the fixture `note` cites the counter relatively
(`.ufo/waves/round-53/count-c2.py`), and the SKILL registry row (SKILL.md:1208) advertises relative
`python3 -I -B tools/mori-commit-runway.py …`.

Context-only extension (`git grep -n '/home/vgpnk' … -- tools/`, outside the assigned paths): `mori-commit-runway.py`
and its fixtures are clean, unlike three pre-existing tools — `tools/mori-round17-context-check.py:118
_FLEET_ROOT = "/home/vgpnk/Projects/shokunin"` (executable default), `tools/mori-blind-check.sh:247` (absolute lane
path argument, executable), `tools/mori-misroot-sweep.py:6,20,355` (docstring/comment prose). Not part of C2; noted so
the classification "the new tool adds no home-path coupling" is contrasted with older state.

## 6. Adversarial `--cases` shapes (the only defect found)

The registry row exposes `--selftest [--cases FILE]`, and `_materialise` (line 207–209) joins the case's `id`
verbatim under the mkdtemp root, while `selftest` only removes the root:

```
case id "../escape-probe":
MATCHER: rejected 1/1 corrupted expectations
MORI_COMMIT_RUNWAY_SELFTEST: PASS 1/1      rc=0
$ ls -A $TMPDIR
escape-probe                                ← written outside the mkdtemp root, left behind

case id "<absolute>/abs-probe":
MORI_COMMIT_RUNWAY_SELFTEST: PASS 1/1      rc=0
$ find <absolute>/abs-probe -maxdepth 2
left: …/abs-probe  left: …/abs-probe/vm  left: …/abs-probe/meminfo  left: …/abs-probe/present
left: …/abs-probe/vm/{admin_reserve_kbytes,overcommit_kbytes,overcommit_memory,overcommit_ratio,user_reserve_kbytes}
```

This contradicts the docstring guarantee at line 10 ("nothing is written outside the selftest's temporary
directory") and leaves litter; it needs a user-supplied `--cases` file, and the committed fixtures use safe ids
(`host-…`, `mode0-…`, `unknown-…`), so the frozen fixture arm and the C2 counter are unaffected.

Other shapes:

```
{"cases": []}                     MATCHER: rejected 0/0 corrupted expectations
                                  MORI_COMMIT_RUNWAY_SELFTEST: PASS 0/0      rc=0   ← vacuously green, no floor
duplicate ids                     FileExistsError traceback (makedirs at line 209) rc=1, temp root removed
case without "expect"             KeyError: 'expect' traceback (_mismatches) rc=1, temp root removed
cases file absent                 FAIL cannot load cases …                  rc=1
```

The C2 predicate's `n≥12` floor sits in the counter, so the `PASS 0/0` hole cannot reach the claim; it is a tool-side
weakness only.

## 7. Cross-item observed while checking the invocation path (frozen counter, routed forward)

`count-c2.py` runs the tool with `subprocess.run([sys.executable, "-I", "-B", tool] + args, …,
cwd=os.path.dirname(os.path.dirname(tool)))` (run_tool, counter lines ~242–248): no `env=`, so the tool inherits the
harness's `TMPDIR`, and no `TMPDIR` is pointed at `--scratch` (`work = tempfile.mkdtemp(prefix="c2-", dir=scratch)`
only covers the counter's own files; the docstring line 23 "Writes only under --scratch" is counter-scoped). The tool
itself writes only inside its inherited `TMPDIR` (proved above), so under the operator scratch directive the wave's
`--scratch` alone does not relocate the tool's selftest temp dir — an operator must also export `TMPDIR`. The counter
is frozen; this is a round-54 item, not a fix for this round.

## 8. What I did not verify (named limits of this seat)

- Runtime below Python 3.11: no interpreter available; only `ast` parse at `feature_version=(3,7)` was checked.
- Non-Linux hosts: the tool is `/proc`- and `/sys`-shaped by design; not run on any other OS (UNVERIFIED, out of scope).
- Non-root execution: this host runs me as root, so permission-denied paths inside `/proc` were not exercised.
- The fixture *values* were not recomputed from the kernel copies here — independent recomputation is another seat;
  I checked only that the 23 committed expectations pass on five interpreters and that the fixture file is
  byte-identical to the commit.
- `git status` was deliberately not run (index refresh); lane cleanliness was checked with
  `git ls-files --others --exclude-standard -- tools .ufo/waves/round-53`.
- No pacman/uv/network install was needed: nothing installed, nothing upgraded, no network fetch used.

## Findings

1. **MED** — `tools/mori-commit-runway.py:207-209` (`_materialise`) uses the case `id` verbatim as a path under the
   mkdtemp root: an `--cases` file with `id: "../x"` writes to `$TMPDIR/x` and an absolute `id` writes to that absolute
   path, both left behind after `selftest`'s `shutil.rmtree(root)` (line ~273), and the run still prints
   `SELFTEST: PASS n/n` rc 0 — contradicting the docstring guarantee at line 10 ("nothing is written outside the
   selftest's temporary directory"). Committed fixtures use safe ids, so C2's data and the counter are unaffected; the
   registry row (SKILL.md:1208) exposes `--cases FILE`, so a fix belongs to the tool, not to this round's counter.
2. **LOW** — `tools/mori-commit-runway.py:246-284` (`selftest`) has no floor: `{"cases": []}` prints
   `MATCHER: rejected 0/0 corrupted expectations` + `MORI_COMMIT_RUNWAY_SELFTEST: PASS 0/0` with rc 0. The counter's
   `n≥12` test keeps this out of the claim; the tool's own docstring claim ("exit 0 only when all pass") is vacuous on
   an empty file.
3. **LOW** — `tools/mori-commit-runway.py:209` and `_mismatches` (~line 227): a malformed *case shape* (duplicate
   `id`, missing `expect`) raises an uncaught `FileExistsError` / `KeyError` traceback with rc 1 instead of a
   `FAIL <case>: …` line. `finally: shutil.rmtree(root)` still removes the temp root (verified), so no leak.
4. **LOW** — `tools/mori-commit-runway.py:288-293,306-308`: `--page-kb` is validated only as a power of two, not
   against the host page size; on the live host `--page-kb 16` / `64` / `1` / `2` / `1024` return rc 0 with the
   mode-0 verdict unchanged and communicate the wrong page size only through `findings:[limit_mismatch]` and
   `limit_consistent:false` — the `notes` never say the page size may not be the host's. No crash and no wrong exit
   code; a reader of the SKILL row could mistake this for a real limit drift. Wording could name the diagnostic.
5. **LOW** — `tools/mori-commit-runway.py:254` + docstring line 47: the docstring says the temp tree is "under
   `$TMPDIR`", but an invalid `TMPDIR` (nonexistent, a regular file, mode 500) is silently replaced by `/tmp` and the
   selftest still passes; under the operator scratch directive that fallback can put files outside the seat scratch
   without any message. Cleanup holds in every case I tried (verified empty `/tmp` afterwards).
6. **LOW (counter-side, frozen)** — `.ufo/waves/round-53/count-c2.py` `run_tool` (lines ~242–248) neither sets `env=`
   nor points `TMPDIR` at `--scratch`, so the tool's selftest temp dirs land in the harness's inherited `TMPDIR`
   while the counter's docstring line 23 says "writes only under --scratch". The tool honours `TMPDIR` correctly;
   route the invocation-env item to round 54, do not change the frozen counter this round.
7. **PASS** — path hygiene: `git grep -n '/home/vgpnk'` at `2a4213bf…` finds 0 hits in
   `tools/mori-commit-runway.py` and 0 in `tools/fixtures/mori-commit-runway/cases.json`; the 3 hits inside
   `.ufo/waves/round-53/` are prose receipts (`evidence/census-start.txt:1,25`, `evidence/sweeps.txt:14`). The only
   absolute path in the tool is the `/usr/bin/env python3` shebang.
