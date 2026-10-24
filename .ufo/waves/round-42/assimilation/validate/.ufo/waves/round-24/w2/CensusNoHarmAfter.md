# CensusNoHarmAfter: census no-harm measurement at the round-24 wave-2 tip

Seat: `MoriR24.CensusNoHarmAfter`. Leaf: no subagents, no peer messages, no `agent://all`.
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Assigned tip: `a730ecfefbdb5c31b1db13aca2c40eecd5e97abc` ("round-24: wave-1 seat reports, S090 wording correction, contract amendment A5").
Times are UTC (`Z`) unless marked `-03:00` (lane commits, lane reflog, `.ufo/watchdog.log`).

## 1. Verdict

- **Census untouched.** `tools/mori-census.sh` is blob `c7d952d6fabe3137a91b9afbea991317ceba1f3e` (mode 100755, sha256 `87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28`) at c725aa37, 29c1bf4, a730ecf, 89849a7 and 7c77fba. No commit in c725aa37..89849a7 or 89849a7..7c77fba touches it.
- **Selftest reproduces the wave-1 baseline byte for byte.** Four runs at three lane tips: exit 0, `MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)`, stdout sha256 `a67a336bf02cb9d88453917a7ed53d1aec673a76e8c85f7016051d449554777f`, stderr 0 bytes, TMPDIR empty afterwards. The stdout bytes equal the baseline's stored file `/fast/scratch/hyaku/mori-r24-a2/selftest.out`.
- **Pre-existing `tools/` blobs unchanged.** All 21 blobs present at c725aa37 are identical at a730ecf (19 `*.py`, `mori-census.sh`, `mori-silence-cases.sh`). The only `tools/` changes in that range are three additions: `tools/mori-pressure.py`, `tools/mori-routed-check.py`, `tools/fixtures/mori-pressure/cases.json`.
- **One live run, no census-side harm.** Exit 1, stderr empty, verdict `MORI_CENSUS: DRIFT (findings=30 drift=12 unavailable=1 surfaces=8)` as in the baseline, and the `script_sha256` stamp on all 30 findings equals the pinned digest. Two finding ids differ: `WATCHDOG_STALE` appears and `LANE_SILENT` disappears. Both trace to host-state transitions in the watchdog ledger and log (section 3). Neither comes from census bytes or from C2.
- **Strict reading of the baseline's live criterion is not met** (its id-set clause), while the harm signal the baseline names (a changed digest or a changed selftest tally) is not triggered. Details in section 3.5.
- **Defects found in the wave-1 baseline document:** three factual errors (section 4). None changes its pinned digests or tallies.

## 2. Checks, commands and results

### 2.1 Census bytes and blob identity (read-only git)

```
git ls-tree <rev> -- tools/mori-census.sh
  rev = c725aa37, 29c1bf4, a730ecf, 89849a7, 7c77fba
  -> 100755 blob c7d952d6fabe3137a91b9afbea991317ceba1f3e  tools/mori-census.sh   (all five)
git cat-file blob a730ecf:tools/mori-census.sh | sha256sum
  -> 87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28
sha256sum tools/mori-census.sh      (clone worktree at a730ecf)
  -> 87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28
sha256 of the lane worktree file (plain file read, no git)
  -> 87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28
git diff --quiet <rev> 89849a7 -- tools/mori-census.sh   -> exit 0 for rev = c725aa37, 29c1bf4, a730ecf
git log --oneline c725aa37..89849a7 -- tools/mori-census.sh   -> (empty)
git log --oneline 89849a7..7c77fba -- tools/mori-census.sh    -> (empty)
git merge-base --is-ancestor c725aa37 a730ecf                  -> rc 0
```

The baseline's §2 digest table (29c1bf4, 4059ffb, 11d8f71, lane worktree) is consistent with this. 4059ffb and 11d8f71 were not cat-filed individually; their blob is inferred from the empty path logs, which cover every commit between c725aa37 and 7c77fba.

### 2.2 Selftest (`bash tools/mori-census.sh --selftest`)

| Run | Checkout | TMPDIR (under seat scratch) | Wall | Exit | Summary | stdout sha256 | stderr | TMPDIR afterwards |
|---|---|---|---|---|---|---|---|---|
| 1 | a730ecf (`w2/CensusNoHarmAfter/repo`) | `.../CensusNoHarmAfter/tmp` | 14.0 s | 0 | PASS 134/134 | a67a336b... | 0 B | empty |
| 2 | a730ecf | `.../CensusNoHarmAfter/tmp2` | 13.9 s | 0 | PASS 134/134 | a67a336b... | 0 B | empty |
| 3 | 89849a7 (`repo-89849a7/`) | `.../CensusNoHarmAfter/tmp3` | 13.5 s | 0 | PASS 134/134 | a67a336b... | 0 B | empty |
| 4 | 7c77fba (`repo-master/`) | `.../CensusNoHarmAfter/tmp4` | 13.6 s | 0 | PASS 134/134 | a67a336b... | 0 B | empty |

- Run 1 stdout is 9600 bytes and 135 lines: 134 `PASS` lines and the summary. Its bytes equal the baseline's `selftest.out` (Python bytes comparison: True).
- The tail of run 1 (`selftest-run1.out` lines 129-135) is `PASS drift: missing baseline exits 2 with a diagnostic (exit 2)`, `PASS drift: changed volatile contract is reported (exit 1)`, `PASS cli: unknown arg exit 2 (exit 2)`, `PASS cli: --help exit 0 (exit 0)`, `PASS cli: --pin without a path exits 2 (exit 2)`, `PASS cli: --drift without a path exits 2 (exit 2)`, then the summary. The baseline's quoted tail is wrong (section 4.2).
- `git status --porcelain` in each clone after its run: empty.
- Census-named entries in `/tmp` before and after run 3 (glob `/tmp/mori-census*` and `/tmp/*census-selftest*`): none.

### 2.3 Pre-existing `tools/` blobs, c725aa37 against a730ecf

- `git ls-tree -r -z c725aa37 -- tools/` lists 21 blobs: 19 `*.py`, `tools/mori-census.sh`, `tools/mori-silence-cases.sh`. `tools/fixtures/` is a directory, not a blob.
- The same 21 paths at a730ecf have identical mode, type and blob id: 21 of 21. None modified, none missing.
- `git diff --no-renames --name-status c725aa37 a730ecf -- tools/` prints exactly three lines, all `A`: `tools/fixtures/mori-pressure/cases.json`, `tools/mori-pressure.py`, `tools/mori-routed-check.py`.
- sha256 of each direct `tools/*.py` blob, base and tip (identical for all 19):

```
mori-content-review.py          fa88a6b034d1cdb9    mori-round15-regressions.py     6a55c33cc13e2cd8
mori-dispatch-ledger.py         9ec14ed3457596af    mori-round16-context-check.py   b0bd0aacfae65324
mori-evidence-loss.py           de189084a5d197c4    mori-round16-regressions.py     e70ed67ce502a7b2
mori-freeze-order.py            ec1be305d9fbf81d    mori-round17-context-check.py   ffdcd1154f5bc0d5
mori-journal-window.py          d61e0d220a1825d7    mori-round17-jj-regressions.py  da3e080aa5181e8e
mori-misroot-sweep.py           51072bd7a891fd24    mori-round17-seat-regressions.py 3f3512c41d94c20c
mori-retention-gate.py          cf0896a2ea36f169    mori-round19-regressions.py     0ccd17307c9ff21e
mori-retention-reconcile.py     4599ee1aff95f217    mori-seat-terminal.py           de845692000e0318
mori-round13-regressions.py     23b753c1b0f742dd    mori-wave-settlement.py         79e7f9dedb8a16a9
mori-round14-regressions.py     533218a566030fda
```

- The read-only `ls-tree` on the lane repository gives the same blob ids at c725aa37 and a730ecf.
- `git cat-file -e <rev>:tools/mori-pressure.py`: rc 128 at c725aa37 and at 29c1bf4; rc 0 at a730ecf and 89849a7. This matches the contract's before-state.
- `tools/mori-routed-check.py` is a new file (status A), so the C1 work did not alter any pre-existing tool.

### 2.4 Live run (one run, fleet root, read-only)

Command, run from the a730ecf clone:
`MORI_SHOKUNIN_ROOT=/home/vgpnk/Projects/shokunin TMPDIR=.../CensusNoHarmAfter/tmp bash tools/mori-census.sh > live.out 2> live.err`

Exit 1, wall 73.8 s, `live.err` 0 bytes, TMPDIR empty afterwards. I did not set `GIT_OPTIONAL_LOCKS`; the census sets it on every Git child (`tools/mori-census.sh:594`).

| Field | Baseline (29c1bf4 clone, 08:16:37Z) | This run (a730ecf clone, 09:04:06Z) |
|---|---|---|
| Exit / stderr | 1 / 0 B | 1 / 0 B |
| Lines / raw sha256 | 63 / `9e8e3319...` | 63 / `ef68369c...` (16866 bytes) |
| Header | `mori-census census-r6 - mode=live - read-only` | same |
| Verdict | `DRIFT (findings=30 drift=12 unavailable=1 surfaces=8)` | same |
| `script_sha256` on findings | `87b8d680...` | `87b8d680...` (all 30) |
| Finding ids, 30 total | WATCHDOG_STATE_LAG 15, WAVE_UNSETTLED_AGE 10, WATCHDOG_ABSENT 1, **LANE_SILENT 1 (warn)**, COREDUMP_NOTICE_JOURNAL_USER 1, JOURNAL_CLASSES_UNMEASURED 1, ROSTER_SET_MISMATCH 1 | WATCHDOG_STATE_LAG 15, WAVE_UNSETTLED_AGE 10, WATCHDOG_ABSENT 1, **WATCHDOG_STALE 1 (warn)**, COREDUMP_NOTICE_JOURNAL_USER 1, JOURNAL_CLASSES_UNMEASURED 1, ROSTER_SET_MISMATCH 1 |
| Surfaces | 8 surface lines + 23 lane rows (31 `SURFACE` lines) | same count |
| Surface states | watchdog drift, waves drift, journal.user ok, journal.system ok, cgroup ok, disk ok, **silence drift**, tmux unavailable | same except **silence ok** |
| Silence tallies | silent=1 progressing=6 young=6 not_open=6 unavailable=4 | silent=0 progressing=6 young=8 not_open=5 unavailable=4 |
| Lane rows that moved | lane.kake `silent` (launch 00:53:53Z); lane.kama `not-open` (round 24 closed) | lane.kake `young` (launch 08:16:42Z); lane.kama `young` (round 25 launched 08:16:40Z) |

The drift roll (12) and unavailable count (1) are unchanged, because the two differing finding ids are both warn severity.

### 2.5 Census write and side-effect surface (code read, live code = lines 1-3005)

- The only file write outside the selftest is `printf '%s' "$text" > "$path"` at `tools/mori-census.sh:2932`, inside the `--pin` path. The census states that `--pin` writes exactly the named file and `--drift` writes nothing (`:213`, `SKILL.md:516`).
- Other redirections in live code are file-descriptor plumbing for journal capture (`:1227-1241`), stderr discards, and `cap()` capturing `CAP_OUT=$("$@" 2>&1)` (`:561-566`).
- The census states live mode creates no files (`:211-212`, usage `:412`).
- Every Git child goes through `git_cap()` (`:591-595`): an `env` scrub of `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, trace and config variables (`:580-590`) plus `GIT_OPTIONAL_LOCKS=0`. The only raw `"$GIT_BIN"` invocation is `:594`.
- Git verbs used in live mode: `config --get`, `rev-parse`, `symbolic-ref`, `show-ref`, `merge-base --is-ancestor`, `cat-file -e`, `log`, `log -1`, and `ls-files -mo --exclude-standard` (`:2389`). None is an index-writing verb (section 2.6 tests the one that touches the index).
- Reads only: user-slice cgroup files (`:304-310`, `:1680-1862`), `/proc/diskstats`, `/proc/uptime`, `/proc/meminfo`, `/proc/sys/kernel/random/boot_id` (`:311-313`, `:341`). No `/proc/pressure`, no system PSI read, no PSI trigger write. This matches C2's statement that the census reads only the user slice.
- Coupling check: no reference to `mori-pressure`, `mori-routed-check`, `cases.json` or supplementary cases, and no `.py` reference anywhere in the census. The only tool path is a comment at `:300` naming `tools/mori-silence-cases.sh`.
- No code under `tools/` enumerates the tools directory. Grep hits for `os.walk`, `scandir`, `iterdir` and `rglob` walk their own input roots.

### 2.6 Lane index during the live run (lane not written)

- Lane `.git/index` mtime: `2026-10-22 06:05:03.4956 -0300` (09:05:03Z). My live run ran from 09:04:06Z to about 09:05:20Z, so the index write falls inside that window.
- Lane reflog (`git reflog show --date=iso master`, read-only): `a536b18 master@{2026-10-22 06:05:01 -0300}: export from jj`. The six most recent master reflog entries are all "export from jj", so the lane is jj-colocated. The jj export 2 s before the index write is the likely writer. [INFERENCE from timestamps; the lane was not snapshotted before and after.]
- Clone experiment (in my clone, not the lane): touch a tracked file (stat change only, content unchanged), then run `git -c core.fsmonitor=false -c core.quotePath=false ls-files -mo --exclude-standard` once with `GIT_OPTIONAL_LOCKS=0` and once with it unset. Both calls returned rc 0 with empty stdout, and the clone's index mtime (nanoseconds) was unchanged after each. So the census's only index-adjacent call does not refresh the index in this test.
- Lane operations by this seat were read-only: `rev-parse`, `log`, `reflog`, `diff` between two commits, `ls-tree`, `cat-file`, `merge-base`, `clone` (source reads), `stat`, and file reads. No `status`, `add`, `commit`, `checkout`, `reset`, `stash`, `fetch`, `pull`, `push`, or any jj command.

### 2.7 Lane movement during the window, and C2 tool changes

| Lane commit | Committer and reflog time | UTC | Census blob | Selftest (this seat) | `tools/` change |
|---|---|---|---|---|---|
| 753d227 | 05:56:36 -03:00 | 08:56:36Z | not separately read; empty census log in range | - | - |
| 13208d2 | 05:56:58 -03:00 | 08:56:58Z | same | - | - |
| 89849a7 | 05:59:07 -03:00 | 08:59:07Z | c7d952d6 (`ls-tree`) | run 3, PASS 134/134 | `M tools/mori-pressure.py`; `A tools/fixtures/mori-pressure/supplementary-cases.json` (vs a730ecf) |
| 6a344d2 | 06:03:35 -03:00 | 09:03:35Z | same (empty census log in range) | - | not measured alone; included in the 89849a7..7c77fba `tools/` diff (see row 7c77fba) |
| a536b18 | 06:05:01 -03:00 | 09:05:01Z | same (empty census log in range) | - | not measured alone; included in the 89849a7..7c77fba `tools/` diff (see row 7c77fba) |
| 7c77fba | 06:11:03 -03:00 | 09:11:03Z | c7d952d6 (`ls-tree`) | run 4, PASS 134/134 | `M tools/mori-pressure.py` only (vs 89849a7) |

The lane's `master` was already at 89849a7 on my first read. The assigned tip a730ecf is no longer the head.

## 3. Attribution of the two finding-id differences (host state)

1. **`WATCHDOG_STALE` (present now, absent in the baseline).** The census reports `age_s=1929 stale_threshold_s=900` at 09:04:06Z (`live.out` lines 2 and 33). The file `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` has mtime `05:31:57 -03:00` (08:31:57Z), and 09:04:06 minus 08:31:57 is 1929 s. The baseline's watchdog row at 08:16:37Z had `age_s=86` (baseline `live.out` line 2). The last ledger line (667) is the 05:31:57 entry. `WATCHDOG_ABSENT` is present in both runs (baseline line 48, ours line 49), so no watchdog process is running. This census did not write the log (live mode writes nothing, and the mtime predates my run by about 32 minutes).
2. **`LANE_SILENT` for kake (baseline only).** The baseline graded kake from the launch at `2026-10-21T21:53:53-03:00` (00:53:53Z; ledger line 646), so its row showed `silent` with `age_s=26564`. This run graded kake from a new ledger line, `2026-10-22T05:16:42-03:00 launch kake round=28 pgid=374706 driver=hyaku-inline attempt=2` (08:16:42Z; ledger line 663). Its row shows `young` with `age_s=2844` under the 7200 s gate. Ledger line 665 records that this kake attempt was later stood down at 08:30Z by Main ("process job limit 100 (config says 200) left 8 lanes without seats ... capacity decision, not a lane fault").
3. **lane.kama (silence tally change).** The baseline row was `not-open` for round 24, closed by ledger line 647 (`complete kama round=24`). This run shows `young` after `2026-10-22T05:16:40-03:00 launch kama round=25 pgid=370096 driver=hyaku-inline attempt=1` (08:16:40Z; ledger line 662).
4. **Timing.** Both launch lines (08:16:40Z and 08:16:42Z) fall 3 to 5 seconds after the baseline census timestamp of 08:16:37Z. They are written by the `hyaku-inline` driver. The census has no spawn or ledger-write path (section 2.5), so it did not cause them. I found no causal link and record the timing as a coincidence.
5. **Consistency check.** The silence tally moves by exactly these two transitions: silent 1 to 0 (kake), not_open 6 to 5 (kama), young 6 to 8 (both).

### 3.5 Against the baseline's own after-run rule

The baseline (§5 and §8) asks that the after-run keep the same finding id set. Under that literal reading this run does not pass, because two warn ids differ. The baseline also names the harm signal it exists for: "a changed digest or a changed selftest tally." Neither changed. The id difference is explained by ledger and log events in section 3. Recommendation for the lead: state the after-run rule as census bytes, selftest stdout hash and `script_sha256` stamp, and report finding ids against a stated host snapshot.

## 4. Errors in the wave-1 baseline (`.ufo/waves/round-24/w1/CensusNoHarmBaseline.md`)

1. **§6 cites the wrong file for "live mode writes nothing".** It says `SKILL.md:211`. `SKILL.md:211` is "one-second kill grace (`MORI_JOURNAL_TIMEOUT_S`), not a whole-census deadline." The statement is in `tools/mori-census.sh:211-212` ("Live mode writes nothing. --selftest writes only under ${TMPDIR:-/tmp}/mori-census-selftest.XXXXXX") and in the usage text at `tools/mori-census.sh:412` ("live mode creates no files"). The registry row at `SKILL.md:164` says "none live". The claim is true. The citation is wrong.
2. **§3 "verbatim" tail is wrong** (baseline lines 65-67). The output file, which is hash-identical to the baseline's stored file, ends `PASS cli: --help exit 0 (exit 0)` (line 132), `PASS cli: --pin without a path exits 2 (exit 2)` (line 133), `PASS cli: --drift without a path exits 2 (exit 2)` (line 134), then the summary (line 135). The baseline's "(exit 0)" on the `--pin` line and its ordering are wrong. Its hash claim stands.
3. **§7 omits jq.** The baseline says the census needs only bash, journalctl, df, pgrep, tmux and coreutils. The journal arm also needs jq: `tools/mori-census.sh:233` (`MORI_JQ_BIN` default `jq`), `:317` (`JQ_BIN=${MORI_JQ_BIN:-jq}`), and `SKILL.md:208` ("The journal arm needs `jq`, `timeout`, and `wc`"). In child shells, `jq` resolves to `/home/vgpnk/.local/bin/jq`, which reports `jq-1.8.2` (section 7).
4. **§5 and §8 after-run criterion** is not host-invariant (section 3.5). Recommended restatement in section 3.5.

Verified as stated in the baseline: the §2 digest table (for the commits checked); §1 `cat-file -e 29c1bf4:tools/mori-pressure.py` absent (rc 128, re-run at 29c1bf4); §3 exit 0, 134/134, 135 stdout lines, sha256 `a67a336b...`, stderr 0 bytes, wall about 14 s; §4 live exit 1, 63 lines, stderr 0 bytes, verdict tally; and the normalized copy digest `7a602716...`, which reproduces from the stored raw `live.out` with the mask `ts=\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z` to `ts=<T>`.

## 5. Comment accuracy in the census (no behaviour change; a fix would change census bytes)

- `tools/mori-census.sh:3086-3087` and `:4597` say the sleeping stub "exists only under /tmp" and "lives ONLY under the /tmp fixture tree". `:4639` and `:4676` say the mutants are "/tmp copies of THIS script". The code places them under `$work`, which is `mktemp -d "${TMPDIR:-/tmp}/mori-census-selftest.XXXXXX"` (`:3012`), and `PD_DIR="$work/dp"` (`:4647`). With TMPDIR set, nothing lands in `/tmp`, as all my runs showed. The wording is stale. Any edit changes the census bytes and needs a re-pin, so record it for a later round.
- `:212` and `:407` ("writes only under ${TMPDIR:-/tmp}") are accurate.

## 6. Outside this seat's scope (observed, not verified further)

- `tools/mori-pressure.py` changed twice after the assigned tip (89849a7 and 7c77fba). C2's declared after-value (`MORI_PRESSURE_SELFTEST: PASS 12/12`) was not run by this seat. Its owner should re-measure it at the current lane head. The census does not read that tool, and I saw no census effect.
- The new SKILL.md registry row for C2 is kind `gate` ("gate (host-surface verdict; not a census or fleet-admission gate)"). The contract describes a read-only capability, and `mori-journal-window` is registered as a probe, not a gate. The kind may need a check against that convention. Not checked further.
- Fleet capacity, for Main: ledger line 665 records a stand-down by Main at 08:30Z (process job limit 100, config says 200).

## 7. Tools, installs and versions (per `/home/vgpnk/.omp/agent/RULES.md`, read first)

- **No installs, upgrades or package transactions were performed.** The census needed none. pacman was not touched.
- Versions observed: git 2.56.0 (`/usr/bin/git`); bash 5.3.20(1)-release; GNU coreutils `timeout` 9.12; `sha256sum` (coreutils); jq-1.8.2 as resolved in child shells (`/home/vgpnk/.local/bin/jq`; `/usr/bin/jq` is also jq-1.8.2); `journalctl` at `/usr/bin/journalctl`; `tmux` at `/usr/bin/tmux` (the census's tmux probe got rc 1 from `tmux ls`, meaning no server); Python 3.14.8 (used only as a subprocess and file harness, not a census dependency).
- Caveat on my own tool shell: it defines builtins named `jq`, `wc`, `timeout` and `pgrep`. In that shell `jq --version` reports `jaq 3.1.1`. Census child processes resolve these names to external files (`type -t` returns `file` in a child bash), so the census used the external jq 1.8.2.

## 8. Scope, cleanup and gaps

- **Writes:** this report, the only file created in the lane. Scratch under `/fast/scratch/hyaku/mori-r24-a2/w2/CensusNoHarmAfter/`: `repo/` (a730ecf clone), `repo-89849a7/`, `repo-master/` (7c77fba), TMPDIRs `tmp/`, `tmp2/`, `tmp3/`, `tmp4/` (all empty after their runs), `selftest-run1.out/.err`, `selftest-run2.out/.err`, `selftest-at-89849a7.out/.err`, `selftest-at-master.out`, `live.out`, `live.err`, `skill-base-tip.diff`. Nothing written under `/tmp`.
- **Commands run:** the selftest runs listed in section 2.2 (Python subprocess harness with `TMPDIR` set); one live census run (section 2.4); read-only git (`ls-tree`, `cat-file`, `log`, `diff`, `rev-parse`, `merge-base`, `reflog`, `clone` from the lane, `ls-files` in a clone only); `grep`-style searches over census source and `tools/`; stat and reads of the fleet ledger and watchdog log.
- **Not run:** no `--pin` or `--drift` live round trip (the selftest covers both through fixture arms, for example "drift: --pin writes a baseline", "drift: pin -> drift is clean", "drift: changed volatile contract is reported"); no live census at 89849a7 or 7c77fba (selftest only); the C2 tool's own selftest.
- **Gaps:** one live sample at a730ecf. Host state moved within minutes (after my first read at 89849a7, the lane head moved three more times, the last at 09:11:03Z), so the finding set is a point sample. No full before-and-after filesystem snapshot of the fleet root was taken. The "no write" conclusion for live mode rests on the code read (section 2.5), the empty `live.err`, and the watchdog log mtime predating the run.
- **Checks the main agent should run:** the C2 selftest and after-value at the current lane head (section 6), and a decision on the after-run criterion (section 3.5).
