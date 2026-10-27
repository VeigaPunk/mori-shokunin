# Mo53SentHostPaths — host-path portability of the round-53 files at `2a4213bf`

Seat: sentinel, round 53 wave w1, leaf. Target: lane commit
`2a4213bf8da72f7cd78189baa5bb9be825dca1df` (2026-10-26 22:31:29 -0300), the data commit, for
`.ufo/waves/round-53/` (both counters, `controls/*.py`, receipts) and `tools/mori-commit-runway.py`.
Everything below is read from committed bytes (`git show <commit>:<path>`), never from the working tree, as the
contract requires when working-tree bytes differ. Scratch: `/fast/scratch/hyaku/mori-r53/Mo53SentHostPaths/`
(created for the seat, removed at the end; every number below was copied into this file first).
No tool was installed or upgraded; no network fetch; `scripts/hyaku/disk-guard.sh status` was read before the
first run (free space 608 G on `/fast`). No file was created or modified inside the lane except this report.

Verdict in one line: the two required sweeps find **no executable host-path default** in any round-53 script or in
the tool — the only hits are three prose receipts; the temp-directory discipline is `TMPDIR` (or the explicit
`--scratch`), never a `/tmp` literal. The counters and the tool replay from a clone at an arbitrary path
(verified, including a path with a space and `ü`), but the counters' repo root is derived by fixed depth from
`__file__`, `count-c2.py` turns two setup failures into `unmet`, `controls/controls.py` writes its receipts into
the lane (not under its scratch argument), and `controls/c1-data.py` reads the UTF-8 `corpus/SOURCES.md` with the
process default encoding. One MED, six LOW, rest PASS.

## 1. The two required sweeps (verbatim)

Sweep A — host path literal in the round-53 directory or the tool:

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -n '/home/vgpnk' \
      2a4213bf8da72f7cd78189baa5bb9be825dca1df -- .ufo/waves/round-53/ tools/mori-commit-runway.py
2a4213bf…:.ufo/waves/round-53/evidence/census-start.txt:1:$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori   # at entering tip 20edafa5, 2026-10-26T22:28:00-03:00
2a4213bf…:.ufo/waves/round-53/evidence/census-start.txt:25:mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
2a4213bf…:.ufo/waves/round-53/evidence/sweeps.txt:14:$ grep -rilE 'overcommit|CommitLimit|Committed_AS|percpu_counter|v7\.3' /home/vgpnk/Projects/shokuknow/merge/mori | wc -l
EXIT=0
```

Sweep B — `/tmp` literal or `mkdtemp(dir="/tmp")`:

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -nE 'mkdtemp\(dir="/tmp|/tmp/' \
      2a4213bf8da72f7cd78189baa5bb9be825dca1df -- .ufo/waves/round-53/ tools/mori-commit-runway.py
EXIT=1        # no hits
```

Sweep C (mine, so the zero in B is not over-read) — every temp/scratch mention in the same two paths:

```
$ git -C … grep -nE '/fast/scratch|TMPDIR|tempfile|mkdtemp' 2a4213bf… -- .ufo/waves/round-53/ tools/mori-commit-runway.py
controls/controls.py:94:    env = dict(os.environ, TMPDIR=tmp)
count-c2.py:23:Exit 0 met, 1 unmet, 2 setup. Writes only under --scratch (default: a fresh directory under $TMPDIR), removed
count-c2.py:40:import tempfile
count-c2.py:339:        root = tempfile.mkdtemp(prefix="fixtures-", dir=os.path.dirname(tree))
count-c2.py:405:    work = tempfile.mkdtemp(prefix="c2-", dir=scratch)
count-c2.py:512:    base = tempfile.mkdtemp(prefix="c2-selftest-")
tools/mori-commit-runway.py:47:file's directory) in a temporary directory under ``$TMPDIR``, …
tools/mori-commit-runway.py:62:import tempfile
tools/mori-commit-runway.py:254:    root = tempfile.mkdtemp(prefix="mori-commit-runway-")
+ one `$` receipt line per control file (`--repo /fast/scratch/hyaku/…`, clones removed after the run)
+ evidence/selftest-c2.txt:1: `$ TMPDIR=/fast/scratch/hyaku/mori-r53/L1/tmp python3 … --selftest`
```

### Classification of every hit

| hit | what it is | classification |
|---|---|---|
| `evidence/census-start.txt:1` | a recorded `$` command line of the round-start census, with the fleet root spelled out twice | **prose only** (receipt). It is the input of one run, not a default: `scripts/sources-census.sh` takes `--root`, so the instrument itself is relocatable; the receipt pins where that run happened |
| `evidence/census-start.txt:25` | a table data cell (`mori ok <lane>/corpus/SOURCES.md`) emitted by that census | **prose only** |
| `evidence/sweeps.txt:14` | a recorded `$` sweep command naming `/home/vgpnk/Projects/shokuknow/merge/mori` | **prose only** |
| the four control receipts and `evidence/selftest-c2.txt` (found by sweep C, not by A/B) | recorded `$` lines carrying `--repo /fast/scratch/…` clone paths and one `TMPDIR=/fast/scratch/…/L1/tmp` | **prose only**; the clone paths were removed after the run by contract, so a verbatim replay of a receipt line cannot succeed — the receipt documents a past run, not a re-runnable command |
| sweep B | — | **no hits**: no script or the tool hardcodes `/tmp` or `mkdtemp(dir="/tmp")`; every temp site is `tempfile.mkdtemp()` (TMPDIR) or `mkdtemp(dir=<scratch>)` |
| `/proc/meminfo`, `/proc/sys/vm`, `/sys/devices/system/cpu/present` (`count-c2.py:299-303`, `count-c2.py:441-443`, wrapper fallbacks; `mori-commit-runway.py:297-299`) | device paths, not host-specific | **host-reading default**: correct on Linux, overridable by flags in the tool, hardwired in the counter's live leg (finding 5) |

No executable host-path default exists in `count-c1.py`, `count-c2.py`, `controls/controls.py`,
`controls/c1-data.py` or `tools/mori-commit-runway.py`.

## 2. Per-file portability (evidence per file)

### 2.1 `tools/mori-commit-runway.py` — portable

* Runs from a bare `git archive` extraction under scratch, cwd `/`, `TMPDIR` = scratch:
  `MATCHER: rejected 23/23 corrupted expectations` / `MORI_COMMIT_RUNWAY_SELFTEST: PASS 23/23`, exit 0;
  `ls -A $TMPDIR` empty after, nothing created in the cwd.
* Fixtures resolve via `os.path.realpath(__file__)` (`_cases_path`, line 203) → symlink-proof; defaults are
  `/proc`/`/sys` but every fixture invocation overrides all three paths, and an absent path is handled, not
  crashed: `--meminfo /nonexistent/… --vm-dir … --cpu-present …` → `verdict: COMMIT_UNKNOWN`, one `notes` entry
  `"/nonexistent/meminfo: absent"`, exit 2.
* Live defaults work on this host: mode 0, `commit_limit_kb=47583772`, `limit_recomputed_kb=47583772`,
  `limit_consistent=true`, `cpus_present=32`, `COMMIT_HEURISTIC`, exit 0.
* Writes are confined to the inherited `TMPDIR` under `strace -f -e trace=openat,creat,mkdir,…`: zero
  write-class opens outside `$TMPDIR`, zero lane references, zero cwd writes (numbers in §4).
* The tool's deeper axes (five interpreters, spaced/non-ASCII/read-only paths, `env -i`, `--cases` shapes) are
  covered by the sibling seat `Mo53ExecToolPortability.md`; I did not repeat them and found nothing that
  contradicts its PASS items. Its MED (`_materialise` uses the case `id` as a path) is real on the committed
  bytes and is a tool-side, not a counter-side, defect.

### 2.2 `.ufo/waves/round-53/count-c1.py` — portable on its committed layout; two arm-only setup paths degrade

* Repo root: `lane_root()` = four `dirname(abspath(__file__))` (lines 296-297); `--repo DIR` overrides it.
  No host literal; no temp use at all (no `tempfile` import); writes nothing (trace in §4).
* Scored path from cwd `/` against the lane, and against a clone at another path, and against a clone at a path
  containing a space and `ü` — identical line, exit 1 at this revision (votes not yet committed):
  `C1=unmet scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok
  held=44 absent=2 holds=46 changed=0 voted=0 dissent=0 rev=2a4213bf… failed=votes`
* `--scope` from `/`: `scope=46`, exit 0. Under `env -i PATH=/usr/bin TMPDIR=…`: `scope=46`, exit 0 (no
  `HOME`/locale/environment dependency observed).
* `--selftest`: `C1_SELFTEST pass=37 fail=0` under Python 3.11, 3.13 and 3.14, from cwd `/`, and from a clone
  (`<clone>/.ufo/waves/round-53/count-c1.py --selftest` → 37/0) — so the fixed-depth root assumption is fine for
  every layout the contract uses.
* Failure modes when the assumption or a tool is missing (both **measured**, both LOW, finding 4):
  - no `git` on PATH, scored path → `C1_SETUP unresolvable revision <rev>`, exit 2 (clean);
  - no `git` on PATH, `--scope` → `FileNotFoundError: … 'git'` traceback, exit 1;
  - counter reached through a directory symlink, `--scope` → `scope=0`, exit 2 (silent-empty, no message);
  - counter reached through a directory symlink, `--selftest` → traceback
    `FileNotFoundError: …/corpus/evidence/sources-r53/proc.rst.v7.3`, exit 1.

### 2.3 `.ufo/waves/round-53/count-c2.py` — portable for the scored arms; setup failures can read as `unmet`

* Fixtures are embedded (`frozen_fixtures`, line 178), not read from the tree, so `--selftest` is
  location-independent: from cwd `/` with `TMPDIR`=scratch → `C2_SELFTEST pass=30 fail=0`, exit 0, and from a
  clone at another path → same. `--selftest` accepts the live witness as `ok` **or** `error`, so it does not
  require `/proc` (`harness_live_witness`).
* Scored path (data commit) from cwd `/`, lane repo, `--scratch` under scratch:
  `C2=met tool=present selftest=pass n=23 fixtures=80 agree=80 disagree=0 registry=ok live=ok rev=2a4213bf…`,
  exit 0 — equal to `evidence/c2-at-data.txt`. Same line under Python 3.11, against a clone at another path, and
  against the clone moved to `space dir/lane ü`.
* Seeded-fixture determinism across interpreters (the seed is `sha256(commit id)`, so a version-dependent
  generator would judge a tool against different fixtures on a different host). `--fixtures` output sha256 is
  identical on 3.11.17, 3.12.15, 3.13.16, 3.14.8:
  `cdca9015098731a7838c80eec3fa0cc65c84133f014c7450c7c762463af46077`. No reproducibility gap observed.
* `TMPDIR`: honoured. With `TMPDIR`=scratch and `--scratch`=scratch, `ls -A $TMPDIR` is empty after the run and
  the `--scratch` directory keeps only its own (empty) self. `--scratch` is used verbatim (no `abspath`, no
  containment, no lane check): a relative value resolves against the caller's cwd — measured: `cd $S && … --scratch relc2`
  → `C2=met …` and `$S/relc2/` created, empty after the run (finding 6).
* Missing `tar` (present `git`): `FileNotFoundError: … 'tar'` traceback at line 413, **exit 1**, scratch cleaned —
  i.e. an environment failure is reported with the claim's `unmet` exit code, not the documented `setup`=2
  (finding 3). Missing `git` is clean: `C2_SETUP unresolvable revision …`, exit 2.
* Live leg (finding 5): `live_check` (lines 298-303) reads `/proc/meminfo`, five `/proc/sys/vm/*`,
  `/sys/devices/system/cpu/present` and `os.sysconf("SC_PAGE_SIZE")` directly, and `main` always calls
  `evaluate_tree(…, live=True)`; there is no flag to skip it. On a non-Linux host the fixture/selftest arms pass
  but the run ends `failed=live`; `C2=met` is Linux-only. The contract names this as a limit ("the live leg …
  depends on the host"); the counter is frozen, so this is a round-54 item.

### 2.4 `.ufo/waves/round-53/controls/controls.py` — builds under the scratch argument, but writes receipts into the lane

* `HERE`/`W`/`LANE` are `abspath(__file__)` derivations (lines 14-16); the clone goes to `<scratch>/clone-<name>`
  with the toplevel assertion `git -C <clone> rev-parse --show-toplevel == <clone>` before `checkout --detach`
  (lines 62-65), and child processes get `TMPDIR=<scratch>/tmp` (line 94). Clone, commit and counter runs are all
  under the caller's scratch argument.
* **Receipts are not.** `receipt()` writes to `os.path.join(W, "evidence", "control-%s.txt")` (line 78) — the
  directory next to the script, not under the scratch argument, and there is no flag to redirect it. Proof of
  derivation from a fake layout (module import has no side effects):
  `HERE=$S/fake/lane/.ufo/waves/round-53/controls`, `W=…/round-53`, `LANE=…/fake/lane`,
  `receipt_dir=…/fake/lane/.ufo/waves/round-53/evidence`. Consequence: running the **lane** copy writes eleven
  `control-*.txt` files into `.ufo/waves/round-53/evidence/`, overwriting the round's frozen receipts in place —
  a write into the lane that no wave seat may make, and a violation of the freeze rule ("a frozen file is never
  edited in place"). I did not execute it, for that reason (finding 1).
* Needs `git` (clone/checkout/commit/add/rev-parse) and `sys.executable`; `git clone --shared` means the clones
  read the lane's object store, so the lane must be present (it is `LANE`, derived, not a literal).

### 2.5 `.ufo/waves/round-53/controls/c1-data.py` — writes only into its clone argument; default-encoding read

* `HERE`/`W`/`LANE` by depth (lines 19-21); it imports `../count-c1.py` through `importlib` (line 24) — so it
  only loads from a committed layout. `apply(clone, parts)` writes only under the `clone` argument: ledger
  (line 140), `corpus/SOURCES.md` (144-149), synthetic voter files (154), v7.2 copies (167). No lane write on any
  path except when `clone` *is* the lane (caller's choice). `--print-table` reads the lane (read-only).
* Portability defect: `lines = open(p).read()` (line 144) and `open(p, "w")` (line 149) on
  `corpus/SOURCES.md` use the process default encoding. That file is UTF-8 with 317 non-ASCII lines (em dashes
  in source titles, e.g. line 7). Measured on a 355-line copy at the data commit:
  default host encoding `UTF-8`, read succeeds; with `LC_ALL=C PYTHONUTF8=0 PYTHONCOERCECLOCALE=0`
  (`ANSI_X3.4-1968`) the same read raises `UnicodeDecodeError: 'ascii' codec can't decode byte 0xe2 in position 10`,
  exit 1 (finding 2). The failure is at the read, before any write, so it cannot leave a half-written
  `SOURCES.md`; it does block off-host reproduction of the C1 controls on a non-UTF-8-default host.
  `controls.py`'s own default-encoding append to `SKILL.md` (line 110) writes ASCII only, so it is safe under an
  ASCII default; its receipt write is explicitly `encoding="utf-8"` (line 79).

## 3. Replay matrix (all observed, data commit `2a4213bf`)

| arm | lane repo | clone at `$S/clonetest/lane` | clone moved to `$S/space dir/lane ü` |
|---|---|---|---|
| `count-c1.py <rev>` | `C1=unmet … voted=0 … failed=votes` exit 1 | identical line, exit 1 | identical line, exit 1 |
| `count-c1.py --selftest` (lane copy) | 37/0 exit 0 | 37/0 exit 0 (clone's own copy) | — |
| `count-c2.py <rev> --scratch …` | `C2=met … agree=80 disagree=0 registry=ok live=ok` exit 0 | identical, exit 0 | identical, exit 0 |
| `count-c2.py --selftest` | 30/0 exit 0 (also under 3.11) | 30/0 exit 0 | — |
| tool `--selftest` from bare archive | PASS 23/23 exit 0 | — | — |

Interpreters exercised for the counters: `/usr/bin/python3` 3.14.8, `python3.11` 3.11.17, `python3.13` 3.13.16.
Seeded fixture bytes identical across 3.11-3.14 (§2.3).

## 4. Write-containment traces (`strace -f`, cwd `/`-outside, `TMPDIR` = scratch)

```
tool --selftest        write-class opens outside $TMPDIR: 0   lane refs: 0   cwd files after: 0   $TMPDIR after: 0
count-c1.py <rev>      write-class opens outside /dev,/proc: 0 (whole run: it writes nothing)
count-c2.py <rev>      write-class opens under the lane: 0
                       write-class opens under --scratch: 1413   under inherited $TMPDIR: 345
```

The 345/1413 split is the observable form of the counter-side item: the counter's own work tree and fixture
directories go under `--scratch`, while every tool-selftest temp root (`mori-commit-runway-*`) goes to the
inherited `TMPDIR`, because `run_tool` (lines 264-268) passes no `env=` and does not point `TMPDIR` at
`--scratch`. The counter's docstring line 23 ("Writes only under --scratch") is therefore counter-scoped, not
run-scoped; the sibling seat `Mo53ExecToolPortability.md` §7 reaches the same item from the tool side. Frozen
counter → round 54.

## 5. Currency note (working-tree drift at audit time)

The lane working tree at audit time (HEAD `95cf78eef71979f9b740ef6bc3c5299b6beff86e`) has uncommitted changes to
`tools/mori-commit-runway.py` (159 lines changed, including case-id/read-size hardening), `SKILL.md` and
`corpus/knowledge/commit-runway-read-r53.md`. Those are not mine; every statement above is about the bytes at
`2a4213bf` read with `git show`, which is what the contract says a claim is measured with. The untracked
`.ufo/waves/round-53/w1/` (sibling reports), `w1.ready*` and `evidence/selftests/` are also not mine;
`git status --porcelain` showed no change caused by this seat's runs (the traces in §4 show why).

## 6. What this seat did not verify (named limits)

- Non-Linux hosts: not run. The tool's `/proc`/`/sys` defaults and the counter's live leg are Linux-shaped by
  design; the off-host failure I *can* state is the counter's `failed=live` outcome, inferred from the code paths
  plus the absent-input behaviour I measured on the tool (UNVERIFIED on a real non-Linux host).
- `controls/controls.py` was never executed (its receipt write would land in the lane; finding 1). The clone,
  commit, `TMPDIR` and receipt paths above are code-read with a fake-layout derivation proof, not a run.
- `controls/c1-data.py` was never executed either; the encoding defect was reproduced on its exact read call
  against a byte copy of `corpus/SOURCES.md` at the data commit, not through the script.
- Scored-path counters were not re-run under a *missing* `git` for `count-c1.py`'s evaluate arm (only the
  `rev-parse` guard, which is the first call); a `git` that disappears between the two calls would traceback.
- Windows/macOS default encodings and CRLF checkouts were not exercised; the CRLF concern is bounded by the
  vote parser (`^\s*RECHECK …` prefix match, whitespace-collapsing quote compare), which would tolerate `\r`.
- No claim verdict is asserted here: a dispatched seat is not an independent judge. C1/C2 gate status is the
  reviewers' and the L1's to read.

## Findings

1. **MED** — `.ufo/waves/round-53/controls/controls.py:78`: `receipt()` writes `control-<name>.txt` into
   `os.path.join(W, "evidence")`, i.e. next to the script and **not** under the `<scratch-dir>` argument the
   script takes (clones line 60, child `TMPDIR` line 94 do honour it, and there is no output-dir flag). Running
   the lane copy therefore overwrites the round's frozen control receipts inside
   `.ufo/waves/round-53/evidence/` — a write into the lane by any seat that runs it, and an in-place edit of
   frozen evidence. Derived-path proof: fake layout at `…/fake/lane/.ufo/waves/round-53/controls/controls.py`
   resolves `W=…/fake/lane/.ufo/waves/round-53`, `receipt_dir=…/fake/lane/.ufo/waves/round-53/evidence`.
   A clone-at-same-layout run writes into that clone; only the lane copy is dangerous. Not executed here for
   that reason.
2. **LOW** — `.ufo/waves/round-53/controls/c1-data.py:144,149`: reads and rewrites the UTF-8
   `corpus/SOURCES.md` with the process default encoding (317 non-ASCII lines at the data commit). Under an
   ASCII default (`LC_ALL=C PYTHONUTF8=0 PYTHONCOERCECLOCALE=0`, measured:
   `UnicodeDecodeError ... byte 0xe2 in position 10`, exit 1) the C1 control build fails on a non-UTF-8 host;
   the failure is at the read, so no partial `SOURCES.md` is left. Ledger and vote writes are ASCII-safe. The
   script is frozen control tooling; round-54 item, not a fix this round.
3. **LOW** — `.ufo/waves/round-53/count-c2.py:413` (`subprocess.run(["tar", …], check=True)`): with `git`
   present and `tar` absent, the counter dies with a `FileNotFoundError` traceback and **exit 1** — the claim's
   `unmet` code — instead of the documented setup code 2 (measured with `PATH` holding only a `git` symlink;
   scratch was still cleaned). An environment failure is thus indistinguishable from a real `C2=unmet` by exit
   code alone.
4. **LOW** — `.ufo/waves/round-53/count-c1.py:282,310,339`: two arms degrade to a traceback with exit 1 rather
   than the documented setup exit 2 — `--scope` on a host without `git` (`FileNotFoundError: … 'git'`) and
   `--selftest` when the counter is reached through a directory symlink (root resolves four levels above the
   symlink, `FileNotFoundError: …/corpus/evidence/sources-r53/proc.rst.v7.3`). The scored path is clean (missing
   `git` → `C1_SETUP unresolvable revision`, exit 2) and a clone at any path passes (37/0), so this affects only
   the auxiliary arms.
5. **LOW (frozen counter, named limit)** — `.ufo/waves/round-53/count-c2.py:298-303` (live leg) with
   `main:416`: `live_check` hardwires `/proc/meminfo`, `/proc/sys/vm/*`, `/sys/devices/system/cpu/present` and
   `os.sysconf("SC_PAGE_SIZE")`, and `main:416` calls `evaluate_tree(tree, seed, skill)`, whose `live` default is
   `True`; no flag skips it. On any non-Linux host the fixture and selftest arms can pass but the run ends
   `failed=live`, so `C2=met` is unreachable off the host family the claim targets. Route to round 54 (add a
   `--no-live` / host-override arm); do not change the counter this round.
6. **LOW (frozen counter, round-54 item)** — `.ufo/waves/round-53/count-c2.py:403-405,264-268`: `--scratch` is
   used verbatim (no `abspath`, no containment or outside-the-lane check; a relative value resolves against the
   caller's cwd — measured, `--scratch relc2` created under cwd), and `run_tool` passes no `env=`/`TMPDIR`, so the
   tool's selftest temp roots land in the inherited `TMPDIR` while the counter's own work tree lands under
   `--scratch` (trace: 1413 write ops under `--scratch` vs 345 under `TMPDIR`; zero under the lane). Under the
   operator scratch directive a caller must set both `--scratch` and `TMPDIR`. Corroborates
   `Mo53ExecToolPortability.md` §7.
7. **LOW (design note)** — the repo root is derived by fixed depth from `abspath(__file__)` and never via
   `realpath` or a `--root` flag in four files: `count-c1.py:296-297`, `count-c2.py:365-366`,
   `controls.py:14-16`, `c1-data.py:19-21`. A symlinked or relocated script resolves a *wrong* root (measured:
   `--scope` → `scope=0` exit 2 with no message; `--selftest` → traceback), and `count-c2.py`'s selftest witness
   imports the counter from whichever directory the invoked path names. Every failure I saw is loud, and a clone
   at the same lane layout (including a path with a space and `ü`) replays both counters identically, so this is
   robustness, not a scoring hazard.
8. **PASS** — no executable host-path literal: sweep A's three hits are prose receipts (`census-start.txt:1,25`,
   `sweeps.txt:14`), and sweep B (the `/tmp` class) has zero hits across `.ufo/waves/round-53/` and
   `tools/mori-commit-runway.py`; temp use is `tempfile.mkdtemp()` (TMPDIR), `mkdtemp(dir=<scratch>)`, or
   `controls.py`'s explicit child `TMPDIR=<scratch>/tmp`. Independent of the sibling seat's identical result.
9. **PASS** — write containment: `count-c1.py` performs no write at all, `tools/mori-commit-runway.py` writes only
   inside the inherited `TMPDIR` (and cleans it), and `count-c2.py` performs zero write-class opens under the lane
   (`strace -f`, full data-commit run). Both counters and the tool replay from a `git archive`/clone at an
   arbitrary path and cwd `/`; seeded fixtures and selftests are byte-identical on Python 3.11-3.14.
