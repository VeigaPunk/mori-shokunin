# Mo50bSentHostPaths — portability and scratch-discipline audit (round 50, attempt 2, wave a2w1)

Seat: sentinel / portability audit (round prompt §7 item 4; QUALITY 127; `considerthese/2026-10-25.md`
suggestion 2). Lane `mori-shokunin`. Read-only on the lane, the fleet repo and `/home/vgpnk/Projects/shokuknow`.
Frozen contract read first: `.ufo/waves/round-50/contract.md`. Data revision audited:
`487941b9395e89678af0053cc443cdb49cdee6e3` (T). Diary baseline revision: `9834fed4`
(the HEAD named in `considerthese/2026-10-25.md`). Entering tip `7197160b927f04db294c9553fb48fadcc7a3f4e3` (E).
Freeze `950e99be6757a52b00e9eb70ae1a1a7bbe2ea379` (FZ). HEAD while I ran: `4548a34dc8b4072abaa4335c1f54a9efcfcc314a`
(the a2w1 spec commit; it carries `build-a2w1-spec.py`, which does not exist at T).

Environment: `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → exit 0,
`/fast/scratch/hyaku 24% use 613.5G free`, `/tmp 2% 125.3G`. Scratch
`/fast/scratch/hyaku/mori-r50/Mo50bSentHostPaths/` (one `git clone --shared -n` of the lane plus a probe copy,
removed at the end). No tool install or upgrade; no pacman. No lane file written; the only writes were inside
the scratch clone and this report.

## 1. The seat's three commands, verbatim

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && git grep -n '/home/vgpnk' 487941b9 -- .ufo/waves/round-50/
487941b9:.ufo/waves/round-50/build-w1-spec.py:7:L = "/home/vgpnk/Projects/shokunin/mori-shokunin"
487941b9:.ufo/waves/round-50/build-w1-spec.py:8:F = "/home/vgpnk/Projects/shokunin"
487941b9:.ufo/waves/round-50/build-w1-spec.py:10:S = "/home/vgpnk/Projects/shokuknow/merge/mori"
487941b9:.ufo/waves/round-50/build-w1-spec.py:32:- {S} and /home/vgpnk/Projects/shokuknow are read-only: ...
487941b9:.ufo/waves/round-50/build-w1-spec.py:33:- Tooling authorization ... /home/vgpnk/.omp/agent/RULES.md ...
487941b9:.ufo/waves/round-50/build-w1-spec.py:93:... absolute `/home/vgpnk` path among the lane's wave instruments ...
487941b9:.ufo/waves/round-50/build-w1-spec.py:124:... (count `/home/vgpnk` occurrences in {W} and say which ...
487941b9:.ufo/waves/round-50/contract.md:84:Assimilation theme from `/home/vgpnk/Projects/shokuknow/merge/mori/`: staged entries
487941b9:.ufo/waves/round-50/controls/c2-controls.py:20:STAGED = "/home/vgpnk/Projects/shokuknow/merge/mori"
487941b9:.ufo/waves/round-50/evidence/census-start.txt:22:mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
487941b9:.ufo/waves/round-50/w1-dispatch.json:277: ... (generated dispatch context) ...
487941b9:.ufo/waves/round-50/w1-spec.json:4|39|44|49|54|59|64|69|74|79|84|89|94|99|104|109|114|119|124|129|134|139|144|149|154|159|164|169|174|179|184|189|194|199|204: ... (generated prompts) ...
487941b9:.ufo/waves/round-50/w1.ready:1:{"lane":"mori",...,"dispatch":"/home/vgpnk/.../w1-dispatch.json",...}
487941b9:.ufo/waves/round-50/w1/Mo50ScoutCoverageFR1.md:50-54
487941b9:.ufo/waves/round-50/w1/Mo50ScribeEntryA.md:3,26,81,343,347
487941b9:.ufo/waves/round-50/w1/Mo50ScribeEntryB.md:8
487941b9:.ufo/waves/round-50/w1/Mo50ScribeRowMemcontrol.md:181,203,240,262
487941b9:.ufo/waves/round-50/w1/Mo50ScribeRowOomKill.md:9,11,21,131,183,208,247,250
EXIT=0
```

Counts for that tree (exact `git grep -c` output):

```
$ git grep -l '/home/vgpnk' 487941b9 -- .ufo/waves/round-50/ | wc -l      -> 12
$ git grep -o '/home/vgpnk' 487941b9 -- .ufo/waves/round-50/ | wc -l      -> 345
$ git grep -c '/home/vgpnk' 487941b9 -- .ufo/waves/round-50/
w1-spec.json:41   w1-dispatch.json:41   build-w1-spec.py:7   w1/Mo50ScribeRowOomKill.md:8
w1/Mo50ScribeEntryA.md:5   w1/Mo50ScoutCoverageFR1.md:5   w1/Mo50ScribeRowMemcontrol.md:4
contract.md:1   controls/c2-controls.py:1   evidence/census-start.txt:1   w1.ready:1   w1/Mo50ScribeEntryB.md:1
```

```
$ git grep -n '/home/vgpnk' 487941b9 -- tools/
tools/mori-blind-check.sh:247:/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-31/rule-text.md
tools/mori-misroot-sweep.py:6:    git -C /home/vgpnk/Projects/shokunin status --porcelain -- .ufo/waves .ufo/reports
tools/mori-misroot-sweep.py:20:(`/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/misroots/MoriR16.Lesson`,
tools/mori-misroot-sweep.py:355:# /home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/misroots/MoriR16.Lesson
tools/mori-round17-context-check.py:39,116,118,508,535,557,559,565
EXIT=0
# files 3, occurrences 18
```

```
$ git grep -nE 'mkdtemp\(dir="/tmp|/tmp/' 487941b9 -- .ufo/waves/round-50/ tools/
.ufo/waves/round-50/w1/Mo50ScribeEntryA.md:306:- `scope-charge-fields-r46.md` `recheck:` writes its fetched page to `/tmp/cg72.html`. ...
tools/mori-census.sh:106:#     arm in isolation (/tmp/r8m/micro-disk.log) ...
tools/mori-census.sh:107:#     gate, interleaved (/tmp/r8m/disk-cost.log), host load ~68:
tools/mori-census.sh:144:#     3 s apart, /tmp/r8m/mem-samples.log; cgroup walk /tmp/r8m/cgroup-max-census.sh):
tools/mori-round15-regressions.py:109:      --fixtures .ufo/waves/round-15/fixtures --output /tmp/r15-gate
tools/mori-silence-cases.sh:309:  WORK=$(mktemp -d /tmp/mori-silence-cases.XXXXXX)
EXIT=0
```

## 2. The baseline (13) and the counts in both directions

Counting command (one line, the definition in suggestion 2):

```
git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -l '/home/vgpnk' <REV> \
  -- '.ufo/waves/round-*/count-*.py' '.ufo/waves/round-*/conform.py' '.ufo/waves/round-*/controls/*.py' 'tools/*' \
  | wc -l
```

| revision | files | files that carry `/home/vgpnk` |
|---|---|---|
| `9834fed4` (the diary's own HEAD) | **32** | see §3 |
| `7197160b` (E) | **32** | identical set |
| `487941b9` (T) | **33** | identical + `.ufo/waves/round-50/controls/c2-controls.py` |

Diff in both directions, baseline 13 → T 33: **+20 files, 0 removed**. Diff against the reproducible
number at the diary's own HEAD: **+1 file** (round-50's `c2-controls.py`), **0 removed**.

The stated baseline of 13 is **not reproducible**. Its own enumeration names eleven files
(`round-40/conform.py`, `count-c8.py`, `round-41/conform.py`, `round-42/count-c1..c3.py`,
`round-43/count-c1s.py`, `count-c2.py` = 8; `mori-blind-check.sh`, `mori-misroot-sweep.py`,
`mori-round17-context-check.py` = 3), and the literal glob above gives 32 at that same commit. Neither
13 nor 11 matches. The 20 extra files are round 31–39 instruments that the diary does not mention
(`round-31` ×4, `round-32`, `round-33` ×2, `round-35`, `round-36` ×2, `round-37` ×2, `round-38` ×4,
`round-39` ×2) plus two committed fixture copies. So a reader of suggestion 2 would watch a number that
is 2.5× too small and would never see that rounds 31–39 are still host-bound.

Round-50's own instruments (the glob restricted to `.ufo/waves/round-50/`): 5 files, **1** carrying a host
path (`controls/c2-controls.py`); `count-c1.py`, `count-c2.py`, `controls/c1-controls.py` carry none.
`build-w1-spec.py` (committed at FZ and T, not matched by the instrument glob) carries 7 occurrences;
`build-a2w1-spec.py` (only at HEAD) carries 4 (§5).

## 3. Per-hit classification (43 occurrences, 33 files, at T)

Classes: **A** = executable filesystem default with no override (breaks off-host replay);
**B1** = executable default that is the author's absolute path but is overridden by `--repo`;
**B2** = `conform.py`, same as B1 plus a scratch root derived from the hardcoded lane, no `--scratch`;
**C** = prose, fixture data or a match-target literal only.

| file (at T) | lines | n | class | note |
|---|---|---|---|---|
| `.ufo/waves/round-31/count-c1.py` | 23 | 1 | B1 | `LANE = '/home/vgpnk/...'`, `repo = LANE`, `--repo` replaces it (line 59-66) |
| `.ufo/waves/round-31/count-c1-a1.py` | 26 | 1 | B1 | same |
| `.ufo/waves/round-31/count-c2.py` | 20 | 1 | B1 | same |
| `.ufo/waves/round-31/count-c2-a1.py` | 23 | 1 | B1 | same |
| `.ufo/waves/round-32/count-c1.py` | 49 | 1 | B1 | same |
| `.ufo/waves/round-33/count-c1.py` | 43 | 1 | B1 | same |
| `.ufo/waves/round-33/count-c1-a1.py` | 52 | 1 | B1 | same |
| `.ufo/waves/round-35/count-c1.py` | 95-96 | 2 | B1 | `repo =`/`fleet =` literals inside the default path |
| `.ufo/waves/round-36/count-c1.py` | 59 | 1 | B1 | `DEFAULT_REPO =`, `repo = DEFAULT_REPO` (650) then `--repo` (655) |
| `.ufo/waves/round-36/count-c2.py` | 40 | 1 | B1 | same |
| `.ufo/waves/round-37/count-c1.py` | 54 | 1 | B1 | same |
| `.ufo/waves/round-37/count-c2.py` | 42 | 1 | B1 | same |
| `.ufo/waves/round-38/conform.py` | 37 | 1 | B2 | `SCRATCH_ROOT = os.path.join(LANE, ...)`; `os.makedirs(SCRATCH_ROOT)` at 238 |
| `.ufo/waves/round-38/count-c1.py` | 68 | 1 | B1 | `DEFAULT_REPO` |
| `.ufo/waves/round-38/count-c4.py` | 39 | 1 | B1 | `DEFAULT_REPO` |
| `.ufo/waves/round-38/scratch/red-receipts/count-c4-m1-red.py` | 39 | 1 | B1 | committed scratch residue, same literal |
| `.ufo/waves/round-39/conform.py` | 53 | 1 | B2 | `SCRATCH_ROOT` + `os.makedirs` at 491 |
| `.ufo/waves/round-39/count-c7.py` | 55 | 1 | B1 | `DEFAULT_REPO` |
| `.ufo/waves/round-40/conform.py` | 69 | 1 | B2 | `SCRATCH_ROOT` + `os.makedirs` at 742 |
| `.ufo/waves/round-40/count-c8.py` | 55 | 1 | B1 | `DEFAULT_REPO` |
| `.ufo/waves/round-40/fixtures/extracted/count-c7-r39.py` | 55 | 1 | B1 | committed fixture copy |
| `.ufo/waves/round-41/conform.py` | 66 | 1 | B2 | `LANE` (scratch root not created in this one; `SCRATCH_ROOT` absent) |
| `.ufo/waves/round-41/fixtures/c1/count-c8.py` | 55 | 1 | B1 | committed fixture copy |
| `.ufo/waves/round-42/conform.py` | 73 | 1 | B2 | `LANE` |
| `.ufo/waves/round-42/count-c1.py` | 27 | 1 | B1 | `LANE`, rebound by `--repo` (129-131) |
| `.ufo/waves/round-42/count-c2.py` | 23 | 1 | B1 | same |
| `.ufo/waves/round-42/count-c3.py` | 20 | 1 | B1 | same |
| `.ufo/waves/round-43/count-c1s.py` | 21 | 1 | B1 | `LANE` |
| `.ufo/waves/round-43/count-c2.py` | 13 | 1 | B1 | `LANE` |
| `.ufo/waves/round-50/controls/c2-controls.py` | 20 | 1 | **A** | `STAGED` outside the repo, no override (§4.2) |
| `tools/mori-blind-check.sh` | 247 | 1 | C | line inside a `--selftest` heredoc allow-list (`allow.txt` fixture input), not path resolution; the tool itself uses `${TMPDIR:-/tmp}` (239) |
| `tools/mori-misroot-sweep.py` | 6,20,355 | 3 | C | docstring usage + docstring + comment; the tool requires `--fleet-root` |
| `tools/mori-round17-context-check.py` | 39,116,508,535,557,559,565 | 7 | C | comment/docstring and prompt-string literals |
| `tools/mori-round17-context-check.py` | 118 | 1 | C (match target) | `_FLEET_ROOT` is used only inside regexes (261-270) as the text the checker searches for; not a filesystem path |

Round-50 hits outside the instrument glob are prompt/report text: `w1-spec.json`/`w1-dispatch.json`
(generated seat prompts, 41 each), the five w1 reports, `contract.md:84`, `evidence/census-start.txt:22`
(an output path inside a census receipt), `w1.ready:1` (dispatch pointer). None is executed.

## 4. Are the round's own counters and controls portable?

I replayed them from a `git clone --shared -n` of the lane at
`/fast/scratch/hyaku/mori-r50/Mo50bSentHostPaths/lane` (HEAD `4548a34d`), i.e. a repo path that differs from
the author's, with `TMPDIR=/fast/scratch/hyaku/mori-r50/Mo50bSentHostPaths/tmp`.

### 4.1 `count-c1.py` and `count-c2.py` — portable (verified)

Neither file contains a host path. `repo` is derived from `__file__` (`count-c1.py:266-267`,
`count-c2.py:245-246`), the fleet repo defaults to the lane's parent and is overridden by `--fleet-repo`,
scratch comes from `tempfile.gettempdir()` (honours `TMPDIR`) or `--scratch`, and the extracted tree is
removed on exit.

```
$ python3 $S/lane/.ufo/waves/round-50/count-c2.py 487941b9
C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=487941b9...
exit=0

$ python3 $S/lane/.ufo/waves/round-50/count-c1.py 487941b9            # default fleet = clone's parent
C1_SETUP cannot resolve manifest
exit=2                         # documented: the fleet repo is the lane's parent, --fleet-repo overrides

$ python3 $S/lane/.ufo/waves/round-50/count-c1.py 487941b9 --fleet-repo /home/vgpnk/Projects/shokunin --scratch $S/c1scratch
C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=487941b9...
exit=0

$ python3 $S/lane/.ufo/waves/round-50/count-c1.py 487941b9 --fleet-repo /home/vgpnk/Projects/shokunin
C1=met ... exit=0
$ ls -a /fast/scratch/hyaku/mori-r50/Mo50bSentHostPaths/tmp   -> . ..
$ find $S/c1scratch -maxdepth 2                                   -> c1scratch, c1scratch/tmp
```

So: both counters are path-portable and `TMPDIR`-clean. Two residual dependencies, both benign and named:
the external `git` and `tar` binaries plus `sys.executable`; and `count-c1` requires the fleet repo (argument
or the parent-directory layout). One scratch residue: with `--scratch DIR` the extracted tree is removed but
an empty `DIR/tmp/` is left behind (`count-c1.py:320-322` removes `state["tree"]` only); the default
`TMPDIR` path is removed whole. LOW.

### 4.2 `controls/c1-controls.py` — layout-bound, crashes off-layout

`FLEET = os.path.dirname(LANE)` (`c1-controls.py:29`) is the only fleet source — there is no `--fleet-repo`
option — and it is read at line 85 (`git -C FLEET show e4a...:MANIFEST.json`). With the lane cloned anywhere
but directly under the fleet repo the script dies before building any control:

```
$ python3 $S/lane/.ufo/waves/round-50/controls/c1-controls.py 487941b9 --scratch $S/c1ctl
Traceback (most recent call last):
  File ".../controls/c1-controls.py", line 85, in main
    manifest = g(FLEET, "show", "%s:MANIFEST.json" % c1.FLEET_REV)
subprocess.CalledProcessError: Command '['git', '-C', '/fast/scratch/.../Mo50bSentHostPaths',
'show', 'e0144996...:MANIFEST.json']' returned non-zero exit status 128.
exit=1                                  # no receipt written; not the documented exit 2
```

Path derivation itself is portable (`HERE`/`WAVE`/`LANE`), and the script's own fixture clone is under
`--scratch` with a toplevel check (79-80) and a fixture-only identity (81-82). The defect is the unchecked
layout assumption plus an uncaught exception instead of a setup error.

### 4.3 `controls/c2-controls.py` — hardcoded path outside the repo; every control dies off-host

Line 20: `STAGED = "/home/vgpnk/Projects/shokuknow/merge/mori"` — a module constant, no argument and no
environment override. `main()` opens it unconditionally (line 33) **before** the control loop, so the
do-nothing control too, not only the three staged ones, depends on a directory outside the repo.

Observed, unmodified, with the freeze copies absent from the clone's worktree (they are read with `open()`
from the worktree at lines 34-35, not via `git show`):

```
FileNotFoundError: [Errno 2] No such file or directory:
  '/fast/scratch/.../lane/corpus/evidence/sources-r50/cgroup-v2.7.2.html'
exit=1
```

Observed again after extracting `corpus/evidence/sources-r50` into the clone (on this host STAGED exists,
so it runs and reproduces the receipts):

```
do-nothing   C2=met claims=22 ... rev=487941b9
staged-r46   C2=unmet ... failed=claims_floor,provenance,source_rows,sources_floor,table
staged-r47   C2=unmet ... failed=claims_floor,provenance,source_rows,sources_floor,table
staged-rows  C2=unmet ... failed=claims_floor,provenance,source_rows,sources_floor,table
```

Observed with `STAGED` pointed at a nonexistent directory (probe copy
`controls/c2-controls-probe.py` in the scratch clone; the frozen file was not touched):

```
  File ".../controls/c2-controls-probe.py", line 33, in main
    s533 = [l for l in open(os.path.join(STAGED, "SOURCES.append.md"), encoding="utf-8")...][0]
FileNotFoundError: [Errno 2] No such file or directory: '/nonexistent/shokuknow/merge/mori/SOURCES.append.md'
exit=1                                  # fails before the do-nothing control, writes no receipt
```

So the frozen control set (whose receipts are committed at `evidence/control-c2-*.txt`) cannot be replayed on
any host without `/home/vgpnk/Projects/shokuknow/merge/mori`, and it additionally needs a populated worktree
for the three copies. The scoring path itself (`count-c2.evaluate`) is portable; only the harness is not.

## 5. The two spec builders

| file | host paths | output | off-host replay |
|---|---|---|---|
| `build-w1-spec.py` (committed at FZ and T) | `L`(7), `F`(8), `S`(10), `X`(20) hardcoded; `W = L + "/.ufo/waves/round-50"` (9) | `open(W + "/w1-spec.json")` (135-137) | **breaks**: the output path itself resolves to `/home/vgpnk/...`; on a host without that tree the write fails. All 7 occurrences are code constants or f-string prompt text built from them |
| `build-a2w1-spec.py` (HEAD only) | `L`(10) and `F`(11) derived from `__file__`; `S`(13) and `X`(26) hardcoded | `open(os.path.join(W, "a2w1-spec.json"))` (192) | **runs**: the output path is relative to the script; the generated prompts still bake `S` and `X` (e.g. line 51 `Scratch: {X}/{n}/`) |

So `build-w1-spec.py` hardcodes its own output location; `build-a2w1-spec.py` fixed that for the repo side
(`L`,`F`,`W`) but still hardcodes the staged corpus and the scratch root inside the prompt text. Neither
reads a file: the only I/O is the single JSON write.

## 6. `/tmp` discipline

Round-50: **0** `/tmp` in any instrument (counters, controls, builders). The one hit is prose
(`w1/Mo50ScribeEntryA.md:306`, describing a staged entry's `/tmp/cg72.html` recheck and the operator
directive). `count-c1.py` uses `tempfile.gettempdir()`; `c1-controls.py`/`count-c1.py` pass `TMPDIR` into
every child run.

Tools: two prose hits (`mori-census.sh:106,107,144` comments; `mori-round15-regressions.py:109` usage
docstring) and **one executable default**: `mori-silence-cases.sh:309`
`WORK=$(mktemp -d /tmp/mori-silence-cases.XXXXXX)` in the non-selftest branch — it ignores `TMPDIR` even when
the caller set it (the `--selftest` branch at 301-307 requires an absolute `TMPDIR` and refuses otherwise).
Supplementary sweep: three tools use the `${TMPDIR:-/tmp}` form and therefore honour `TMPDIR`
(`mori-blind-check.sh:239`, `mori-census.sh:3012`, `mori-index-clean.sh:147`).

## Findings

- **MED — `.ufo/waves/round-50/controls/c2-controls.py:20`** (`STAGED = "/home/vgpnk/Projects/shokuknow/merge/mori"`, opened unconditionally at line 33; copies read from the worktree at 34-35). The frozen control set cannot be replayed off-host: every control, including do-nothing, raises `FileNotFoundError` before writing a receipt (observed with a probe copy), and a no-checkout clone fails even earlier. The committed receipts are therefore not independently re-derivable on another host.
- **MED — `.ufo/waves/round-50/controls/c1-controls.py:29,85`** (`FLEET = os.path.dirname(LANE)`, no `--fleet-repo`). Replay requires the lane to be cloned directly under the fleet repo; otherwise the script dies with an uncaught `CalledProcessError` (exit 1, no receipt) instead of a setup error. Path derivation and fixture isolation are otherwise correct.
- **MED — `considerthese/2026-10-25.md` suggestion 2 ("the count is 13 files today")**. The baseline is not reproducible: the stated definition gives 32 files at the diary's own HEAD `9834fed4` (33 at T, of which 1 is new), and the diary's own enumeration names 11. The number the diary proposes to watch is ~2.5× too small and hides rounds 31-39.
- **MED — `.ufo/waves/round-50/build-w1-spec.py:7-12,20,135-137`** (`L`,`F`,`S`,`X` hardcoded, `W = L + ...` is the output directory). The spec builder's own output path is host-bound, so it cannot be replayed off-host; `build-a2w1-spec.py:13,26` improved `L`/`F`/`W` but still hardcodes `S` and `X` inside the generated prompts.
- **LOW — `.ufo/waves/round-50/count-c1.py:320-322`**. With `--scratch DIR` the extracted tree is removed but an empty `DIR/tmp/` is left (observed `c1scratch/tmp`); the default `TMPDIR` path is removed entirely. Scratch-discipline residue only.
- **LOW — `.ufo/waves/round-38/conform.py:38,238`, `round-39/conform.py:54,491`, `round-40/conform.py:70,742`**. `SCRATCH_ROOT` is derived from the hardcoded `LANE` and created with `os.makedirs` on every run; `--repo` overrides the git reads but not the scratch root, so off-host replay writes (or fails) under `/home/vgpnk/...`. This is also the origin of the committed `round-38/scratch` residue (`round-38/scratch/red-receipts/count-c4-m1-red.py`, which itself carries the host literal).
- **LOW — `tools/mori-silence-cases.sh:309`**. `mktemp -d /tmp/mori-silence-cases.XXXXXX` in the non-selftest branch ignores `TMPDIR`; the selftest branch (301-307) correctly requires an absolute `TMPDIR`. A `/tmp` path is never evidence.
- **LOW (positive, verified) — `.ufo/waves/round-50/count-c1.py`, `count-c2.py`**. Zero host paths; both replay from a foreign clone path (`C1=met … exit 0`, `C2=met … exit 0`) with `TMPDIR`-honouring scratch and full cleanup. `count-c1` needs `--fleet-repo` when the lane is not a child of the fleet repo (documented). `tools/mori-misroot-sweep.py` (all 3 hits prose, `--fleet-root` required) and `tools/mori-blind-check.sh` (1 hit is heredoc fixture data) are likewise clean.
