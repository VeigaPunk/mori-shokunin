# Mo52ExecWritersConform — round-51 routed defect 8: in-lane writer inventory (read-only)

Seat: `Mo52ExecWritersConform` (executor, leaf). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Data revision: `8524904adb25e44f24d9f25aac7eae909625c18c` (entering tip `4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d`).
Scratch: `/fast/scratch/hyaku/mori-r52/Mo52ExecWritersConform/` (removed at the end; every output cited here was copied into this report first).
No file outside this report was written in the lane; nothing was edited, committed, staged or stashed anywhere.

## 0. Answer in one table (writes into the lane)

| instrument | writes into LANE on a passing `--selftest`? | paths (lane-relative) | redirectable by `--repo`? |
|---|---|---|---|
| `.ufo/waves/round-38/conform.py` | **yes** | `.ufo/waves/round-38/scratch/mori-conform-selftest-<rand>/` (removed on clean exit) **and, through the counter it runs**, `.ufo/waves/round-38/scratch/mori-c1-tool-<rand>/`, `.ufo/waves/round-38/scratch/c1-<rand>/` (**left behind**) | **no** — `SCRATCH_ROOT` is built from the `LANE` literal (L38) and the `mkdtemp` parent is `SCRATCH_ROOT` (L239) |
| `.ufo/waves/round-39/conform.py` | **yes** | `.ufo/waves/round-39/scratch/` (parent created, left) + `…/mori-conform-selftest-<rand>/` (removed on clean exit) | **no** — same shape, `SCRATCH_ROOT` from `LANE` (L54), `makedirs`/`mkdtemp` L491–492 |
| `.ufo/waves/round-41/conform.py` | **yes, by default** | `.ufo/waves/round-41/scratch/` (parent created, left) + `…/mori-conform-selftest-<rand>/` (removed) | **yes** — `scratch_root = os.path.join(repo, …)` (L928); with `--repo` elsewhere the lane is not written |
| `.ufo/waves/round-42/conform.py` | **yes, by default** | **`.ufo/waves/round-41/scratch/`** (parent created, left) + `…/mori-conform-selftest-<rand>/` (removed) | **yes** — but it writes into the **round-41** parent (L944), not round-42 |
| `.ufo/waves/round-40/conform.py` *(not in the routed four; named by SKILL.md, see §6)* | **no** (instrument itself) | none — `SCRATCH_ROOT = tempfile.gettempdir()` (L73), `LANE` derived from `__file__` (L72) | n/a |

Reads under LANE, all four: the contract path, the counter source(s), the hang fixture, the summary-only fixture (repo-relative) and the lane repository through `git -C <repo>`; plus, for round-42, its own `fixtures/` directory. Exact literals and line numbers in §2.

## 1. Method, and why the runs were contained

Frozen bytes were never edited and the lane was never written. Because round-38 and round-39 write to the `LANE` literal and ignore `--repo` (§2.1, §2.2), running their `--selftest` "from a git archive under scratch" cannot avoid the lane by arguments alone. The selftests were therefore run inside a **private mount namespace** — `unshare -rm` + `mount --bind <copy> /home/vgpnk/Projects/shokunin/mori-shokunin` — so that the hardcoded LANE path resolved to a copy in scratch while the frozen bytes ran unmodified.

Containment probe (before any selftest):

```
$ unshare -rm bash -c "mount --bind '<copy>' /home/vgpnk/Projects/shokunin/mori-shokunin && cd /home/vgpnk/Projects/shokunin/mori-shokunin && git rev-parse --show-toplevel && echo probe-$$ > .ufo/waves/round-38/.probe-x && ls .ufo/waves/round-38/.probe-x"
/home/vgpnk/Projects/shokunin/mori-shokunin
.ufo/waves/round-38/.probe-x
$ ls /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-38/.probe-x
ls: cannot access '/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-38/.probe-x': No such file or directory
$ ls <copy>/.ufo/waves/round-38/.probe-x
<copy>/.ufo/waves/round-38/.probe-x
```

Read-only inputs:

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive 8524904adb25e44f24d9f25aac7eae909625c18c | tar -x -C src      # rc=0, 332M
$ git clone -q --no-local /home/vgpnk/Projects/shokunin/mori-shokunin lane-rXX
$ git -C lane-rXX checkout -q --detach 8524904adb25e44f24d9f25aac7eae909625c18c
$ git -C lane-rXX rev-parse --show-toplevel   # prints the clone dir before any use
$ git -C lane-rXX rev-parse HEAD              # 8524904adb25e44f24d9f25aac7eae909625c18c (all five copies)
```

One per instrument (`lane-r38`, `lane-r39`, `lane-r40`, `lane-r41`, `lane-r42`), `TMPDIR` under scratch. The lane's `git status --porcelain --ignored` was captured before (§5) and after.

Method deviation, disclosed: the first attempt used `git clone --shared` copies. Inside the namespace the clone's `objects/info/alternates` re-resolved to the copy itself, so `git rev-parse --verify <rev>^{commit}` failed and every arm of every selftest reported `timeout_state → exit=2`. Those readings were discarded; all numbers below come from the `--no-local` copies. (`count-c1.py` reports it itself: `counter setup error: git rev-parse --verify 8524904a…^{commit} failed in .: fatal: Needed a single revision`, exit 2.)

## 2. Per-instrument inventory (line numbers in the 8524904a blob)

Hashes and sizes at the data revision:

```
580a0bf15a815b5a26aed908f67a3d74f29d714b19175cee6057fb694aaeb01e  13403  .ufo/waves/round-38/conform.py
fe0be179aba9df7150f0b6cdb50a5f9bbdb411efb1263b46ffa6b21d46ef7987  24712  .ufo/waves/round-39/conform.py
e1f2e11e7556cb4522c36cf22b3666650561e8eba0a7a7e85dc8c22c65475427  44139  .ufo/waves/round-41/conform.py
8efa9cfc4d2c36c21bea0cbdcd0a82fa67e15e9bd10c40556710b8f06cf48064  46994  .ufo/waves/round-42/conform.py
7f5174d542bd983552670b06f6cc424b10e53c81e55ecabcdd919f4043bdfa23  36650  .ufo/waves/round-40/conform.py   (extra, §6)
```

### 2.1 `round-38/conform.py` — lane writes are unconditional

Reads/writes under the hardcoded lane (`LANE = "…/mori-shokunin"` L37):

| line | kind | path |
|---|---|---|
| 38 | const | `SCRATCH_ROOT = os.path.join(LANE, ".ufo/waves/round-38/scratch")` |
| 39–40 | const | `DEFAULT_COUNTERS = LANE/.ufo/waves/round-38/count-c1.py`, `…/count-c4.py` |
| 41 | const | `DEFAULT_CONTRACT = LANE/.ufo/waves/round-38/contract.md` |
| 42 | const | `FIXTURE_REL = .ufo/waves/round-38/fixtures/summary-only.py` (resolved against the counter's `--repo`) |
| 43 | const | `HANG_FIXTURE = LANE/.ufo/waves/round-38/fixtures/hang-after-flush.py` |
| 267 | default | `--repo` default = `LANE` |
| 138 | read | `open(contract_path)` → lane round-38 contract |
| 176, 204, 237 | read | `open(<counter>)` → lane counters under test |
| 163, 191 | run | `--print-tool FIXTURE_REL --repo <repo>`; `<counter> <rev> --repo <repo> --tool HANG_FIXTURE --tool-timeout 3 …` |
| **238** | **write** | `os.makedirs(SCRATCH_ROOT, exist_ok=True)` — **absolute LANE path, ignores `--repo`** |
| **239** | **write** | `tempfile.mkdtemp(prefix="mori-conform-selftest-", dir=SCRATCH_ROOT)` |
| 248 | **write** | `open(path, "w")` → `…/mori-conform-selftest-<rand>/counter-<mutation>.py` |
| 259 | delete | `shutil.rmtree(work)` — only the work dir; the `SCRATCH_ROOT` parent is never removed |

Transitive writes, via the counter it runs (`round-38/count-c1.py`): `DEFAULT_REPO` L68, `SCRATCH_ROOT` L70 and `CHALLENGE_PARENT` L71 both `LANE/.ufo/waves/round-38/scratch`, `NEGATIVES_DIR` L72 `LANE/.ufo/waves/round-38/fixtures`; `_scratch_parent()` L907–920 (`makedirs` L915, probe `mkdtemp` L916); main creates `mori-c1-tool-<rand>` L992 and `c1-<rand>` L1029 in that parent and removes them at L1041/L1099/L1127/L1129 — those `finally` blocks do not run when the process is killed (§4). `round-38/count-c4.py` carries the same `SCRATCH_ROOT` (L45, `makedirs` L279, `mkdtemp` L280) but is only audited statically by the selftest.

### 2.2 `round-39/conform.py` — same shape, one round later

`LANE` L53; `SCRATCH_ROOT = os.path.join(LANE, ".ufo", "waves", "round-39", "scratch")` L54; `DEFAULT_COUNTERS` L55 (`round-39/count-c7.py`); `DEFAULT_CONTRACT` L56; `FIXTURE_REL` L57; `HANG_FIXTURE` L58; `--repo` default L520.
Writes: `makedirs(SCRATCH_ROOT)` **L491**, `mkdtemp(dir=SCRATCH_ROOT)` **L492**, `open(path, "w")` L501, `rmtree(work)` L512 — the parent `.ufo/waves/round-39/scratch` is created and left.
Reads: contract L306; counters L345, L385, L402, L456; hang fixture L369; `FIXTURE_REL` L331; lane git through `git -C <repo>`.
Transitive: `round-39/count-c7.py` `SCRATCH_ROOT` L62 = lane `round-39/scratch`, `makedirs` L475, `mkdtemp` L476. On the selftest path these are not reached (its `timeout_state` runs the counter with `--arms selftest`, which returns before the scratch block), so only the parent is created.

### 2.3 `round-41/conform.py` — scratch follows `--repo`

No module-level `SCRATCH_ROOT`. `LANE` L66; `DEFAULT_COUNTERS` L67 (`lane/.ufo/waves/round-40/count-c8.py`); `DEFAULT_CONTRACT` L70 (`lane/.ufo/waves/round-39/contract.md`); `FIXTURE_REL` L71; `HANG_FIXTURE` L72; `--repo` default L960.
Writes: `scratch_root = os.path.join(repo, ".ufo", "waves", "round-41", "scratch")` **L928**, `makedirs` **L929**, `mkdtemp` **L930**, `open(path, "w")` L939, `rmtree(work)` L952. With the default `--repo` this is the lane; with `--repo <copy>` it stays in the copy — the only reason this instrument is re-executable off-lane.
Reads: contract L604; counters L643, L691, L712, L926; hang fixture L675; `FIXTURE_REL` resolution L629; lane git through `git -C <repo>`.
Transitive: `round-40/count-c8.py` `SCRATCH_ROOT` L62 = **lane `round-39/scratch`** (not round-40), `makedirs` L470. Reached only on a full run; the selftest's `timeout_state` uses `--arms selftest`, which returns before it (verified: the run created no `round-39/scratch`, while a direct `--arms real` invocation of the same counter created it — §4).

### 2.4 `round-42/conform.py` — writes into round-41's scratch

`LANE` L73; `DEFAULT_COUNTERS` L74 (`lane/.ufo/waves/round-40/count-c8.py`); `DEFAULT_CONTRACT` L77; `FIXTURE_REL` L78; `HANG_FIXTURE` L79; `--repo` default L1008.
Writes: `scratch_root = os.path.join(repo, ".ufo", "waves", "round-41", "scratch")` **L944** (round **41**), `makedirs` **L945**, `mkdtemp` **L946**, `open(path, "w")` L955, `rmtree(work)` L1000.
Reads: contract L619; counters L658, L706, L727, L942; hang fixture L690; fixtures L644; **its own fixture directory** `os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")` L977–980 (three extra arms); lane git through `git -C <repo>`.
Transitive: same `count-c8.py` lane `round-39/scratch` (L62) as §2.3, likewise unreached on the selftest path.

## 3. Selftest runs (contained; commands exactly as named)

Runner per instrument: snapshot the copy's tree, then

```
unshare -rm bash -c "mount --bind <copy> /home/vgpnk/Projects/shokunin/mori-shokunin \
  && cd /home/vgpnk/Projects/shokunin/mori-shokunin \
  && export TMPDIR=<scratch>/tmp/<r> \
  && exec timeout 1500 python3 .ufo/waves/round-<r>/conform.py 8524904adb25e44f24d9f25aac7eae909625c18c --selftest"
```

(the form exactly as written in `SKILL.md` L908/L910/L911 for r38/r39/r40, and as written in the receipts for r41/r42, whose defaults supply the same `--repo` / `--contract` / `--counter`).

| instrument | exit | elapsed | last line | residue created inside the lane path |
|---|---|---|---|---|
| round-38 | **0** | 42 s | `CONFORM_SELFTEST pass=6 fail=0` | `.ufo/waves/round-38/scratch/c1-1mfcgqel/`, `.ufo/waves/round-38/scratch/mori-c1-tool-dg24j_gn/` (both empty, 0 B, **left**) |
| round-39 | **0** | 51 s | `CONFORM_SELFTEST pass=9 fail=0` | `.ufo/waves/round-39/scratch/` (empty parent, **left**) |
| round-41 | **0** | 68 s | `CONFORM_SELFTEST pass=14 fail=0` | `.ufo/waves/round-41/scratch/` (empty parent, **left**) |
| round-42 | **0** | 78 s | `CONFORM_SELFTEST pass=17 fail=0` | **`.ufo/waves/round-41/scratch/`** (empty parent, **left**) |
| round-40 (extra) | **0** | 58 s | `CONFORM_SELFTEST pass=11 fail=0` | none (work tree went to `TMPDIR`, removed) |

All pass counts match the shipped receipts — `round-38/evidence/c5-after-selftest.txt` `pass=6`, `round-39/evidence/c8-after-selftest.txt` `pass=9`, `round-41/evidence/control-after.txt` `pass=14`, `round-40/evidence/c10-after-selftest.txt` `pass=11` — except **round-42**, whose only receipt `round-42/evidence/control-c1-v4.txt:8` records `CONFORM_SELFTEST pass=14 fail=0` at revision `9de7323d…`, while the landed bytes ship 17 arms (14 mutations + 3 fixture arms, docstring `selftest()`): no `pass=17` receipt exists.

Representative output (round-38, first and last arms):

```
FAIL→PASS lines elided; sample:
PASS timeout_state  budget flag ignored -> only timeout_state failed
PASS scratch        scratch parent moved off-lane -> only scratch failed
CONFORM_SELFTEST pass=6 fail=0
```

`git -C <copy>/.git/index` size+mtime was part of every snapshot and did not change in any run: the instruments' git use is read-only.

## 4. What a passing run leaves, and what a killed run leaves

Passing: the `mkdtemp` work directory is removed (`rmtree` in `finally`), but the **parent** `makedirs` is not — so `.ufo/waves/round-39/scratch` (r39), `.ufo/waves/round-41/scratch` (r41 ***and*** r42) appear in the lane and stay. Round-38 is worse in one respect: it writes into a **tracked** directory, and the counter it runs leaves two empty dirs there per run.

Killed run (observed live in the lane, not by this seat): `rmtree` never executes, so the whole work tree stays — mutated counter copies included:

```
$ ls .ufo/waves/round-39/scratch/mori-conform-selftest-6ftxqxje/
counter-bounded_reads.py  counter-head_pin.py  counter-predicate.py
counter-timeout_value.py  counter-tool_resolve.py
$ du -sh .ufo/waves/round-39/scratch
360K
$ git status --porcelain --ignored -- .ufo/waves/round-39/scratch | wc -l
1
```

The r38 residue has the same cause, and it is the checker's own mutant arm that produces it — not a crash of the honest counter. The honest counter's `--arms real` run against the hanging tool cleans up after itself:

```
$ unshare -rm … timeout 25 python3 .ufo/waves/round-38/count-c1.py 8524904a… --repo . \
    --tool …/.ufo/waves/round-38/fixtures/hang-after-flush.py --tool-timeout 3 --arms real --seed 5
C1=unmet  seed=5  head_at_measurement=8524904a…   EXIT=1
$ ls .ufo/waves/round-38/scratch | grep -E '^(c1-|mori-c1-tool-)'   → (none)
```

whereas the shipped `timeout_state` mutation (`_TOOL_BUDGET[0] = TOOL_TIMEOUT_S`) — one of the six arms the r38 selftest applies — hangs, is killed by the checker's outer bound, and leaves the two directories the run itself left behind:

```
$ sed 's/_TOOL_BUDGET\[0\] = max(1, args.tool_timeout)/_TOOL_BUDGET[0] = TOOL_TIMEOUT_S/' count-c1.py > counter.py
$ unshare -rm … timeout 15 python3 counter.py 8524904a… --repo . --tool …/hang-after-flush.py --tool-timeout 3 --arms real --seed 5
EXIT=124   (SIGKILL from the outer bound)
$ ls .ufo/waves/round-38/scratch | grep -E '^(c1-|mori-c1-tool-)'
c1-jlxhav5p
mori-c1-tool-85b9ja_q          # both 0 bytes — empty, therefore invisible to git
```

So every passing r38 selftest deposits two empty directories in the tracked lane scratch — one pair per killed mutant arm.

Direct probe that `count-c8.py` writes the lane whenever it is not short-circuited (this is what `--repo` cannot redirect):

```
$ unshare -rm … python3 .ufo/waves/round-40/count-c8.py 8524904a… --repo . \
    --tool …/.ufo/waves/round-39/fixtures/hang-after-flush.py --tool-timeout 3 --arms real
… C7=met   EXIT=0
$ ls -d <lane>/.ufo/waves/*/scratch
…/round-38/scratch  …/round-39/scratch   ← created by that run
…/round-40/scratch  …/round-41/scratch
```

## 5. Lane status before and after (this seat contributes nothing)

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --porcelain --ignored
before: 36 lines  sha256 ee999a933206e4327a45e924c1d2760381fb4c80553f44ba0d7ee8200db2ce7f
after:  58 lines  sha256 18b49498ec01f72694488b2b71b8ba55db42928ca3e583ee7b5bcff958925180
```

The diff contains only sibling wave traffic: new `.ufo/waves/round-52/w1/*.md` reports (Mo52Ent01/03, Mo52Crit*, Mo52Scribe*, Mo52Scout*, …), `w1.ready.partial` → `w1.ready.dispatched`, and the **removal** of `?? .ufo/waves/round-38/scratch/mori-conform-selftest-vd9tc6xm/` by another seat. No path in the diff is attributable to this seat; nothing was added under `round-38/39/41/42` by me.

Concurrently, other seats were exercising the same instruments against the lane: `.ufo/waves/round-39/scratch` was recreated at 21:16:41 and pushed out four `mori-conform-selftest-*` directories by 21:16:54 (696K → later 360K as they were partially cleaned), and `.ufo/waves/round-38/scratch` holds **18** `c1-*` / `mori-c1-tool-*` directories right now (all empty). Those are the defect happening in production, not my writes.

Empty residue is invisible to `git status`:

```
$ ls -1 .ufo/waves/round-38/scratch | grep -cE '^(c1-|mori-c1-tool-|challenge-)'
18
$ find .ufo/waves/round-38/scratch -maxdepth 2 -path '*c1-*' -type f | wc -l
0
$ git status --porcelain --ignored -- .ufo/waves/round-38/scratch | wc -l
0
```

## 6. Discovery surface: SKILL.md names three of the five

```
$ git -C …/mori-shokunin grep -n 'conform.py' 8524904a… -- SKILL.md
SKILL.md:908  counter conformance (r38)     … --selftest (six mutations …)
SKILL.md:910  counter conformance v2 (r39)  … --selftest (nine mutations …)
SKILL.md:911  counter conformance v3 (r40)  … --selftest → CONFORM_SELFTEST pass=11 fail=0
SKILL.md:1073 … .ufo/waves/round-40/conform.py:69 hardcoded the lane path, so a re-execution off-host died as a setup error
$ grep -c 'round-41/conform' SKILL.md   → 0
$ grep -c 'round-42/conform' SKILL.md   → 0
```

So SKILL.md's gate table carries r38, r39 and r40 only; the routed list (r38, r39, r41, r42) and the SKILL-named list (r38, r39, r40) overlap in two. The r41/r42 selftest forms live only in receipts: `round-41/evidence/control-after.txt:64` (`… conform.py <rev> --repo <repo> --contract .ufo/waves/round-39/contract.md --counter .ufo/waves/round-41/fixtures/c1/count-c8.py --selftest`) and `round-42/evidence/control-c1-v4.txt:4`. I ran r40 as well because the SKILL.md discovery sentence names it; it is the only one of the five whose own scratch root is outside the lane.

## 7. Counter weakness seen, routed not fixed

`count-c1.py`'s `lane_writes` limit in the round-52 contract reads "only paths that `git status --ignored` lists". The residue this inventory found in the lane is mostly **empty directories**, which git cannot list at all (§5: 18 dirs, 0 status lines). A lane-writer that leaves only empty directories therefore scores `lane_writes=0`. That is a named limit of the C1 counter, not a defect of the claim measured this round; it is routed to round 53 as a successor design (count residue by directory entry, not by git status).

The fix for the writers themselves is likewise a successor freeze, not an in-place edit (contract §5 item 6/8): round-40's shape (`LANE` from `__file__`, L72; `SCRATCH_ROOT = tempfile.gettempdir()`, L73) plus a `--scratch` on the counters is the pattern the other four predate.

## 8. Tooling

No tool was installed, upgraded or removed. No `pacman` call of any kind (host-wide pause honoured). `disk-guard.sh status` read before the heavy runs: `/fast/scratch/hyaku` 25 % used, 606.5 G free, rc=0. Scratch (≈2.2 GB of clones and copies) removed at the end.

## Findings

1. **HIGH** — `.ufo/waves/round-38/conform.py:38` (with `:238`–`:239`) and `.ufo/waves/round-39/conform.py:54` (with `:491`–`:492`) build the selftest scratch parent from the `LANE` literal, so `--repo` (L267 / L520) cannot redirect it: the `--selftest` form writes into `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-38/scratch` and `…/round-39/scratch` unconditionally, and cannot be re-executed off the lane at all.
2. **HIGH** — `.ufo/waves/round-38/scratch` is a **tracked** directory, and every passing r38 selftest deposits untracked empty directories into it: the `timeout_state` mutant arm drives `round-38/count-c1.py` into the hang fixture, the checker kills it at its own bound, and the counter's `finally` blocks (`count-c1.py:1041`, `:1129`) never run, leaving `mori-c1-tool-<rand>/` (L992) and `c1-<rand>/` (L1029). Reproduced with the shipped mutation alone: `EXIT=124`, two empty dirs. The lane holds 18 such directories today; they are invisible to `git status` because they are empty.
3. **MED** — `.ufo/waves/round-39/conform.py:491` and `.ufo/waves/round-41/conform.py:929` / `round-42/conform.py:945` create their scratch parent with `makedirs` and never remove it, so a **passing** selftest permanently adds `.ufo/waves/round-39/scratch` and `.ufo/waves/round-41/scratch` to the lane as untracked paths.
4. **MED** — `.ufo/waves/round-42/conform.py:944` points its scratch root at the **round-41** directory (`.ufo/waves/round-41/scratch`), so two rounds' instruments contend for one parent; a round-42 run mutates a round-41 path.
5. **MED** — a killed run never reaches the `finally: shutil.rmtree` (`round-38:259`, `round-39:512`, `round-41:952`, `round-42:1000`) and leaves the full work tree, including mutated counter copies, in the lane: observed live at `.ufo/waves/round-39/scratch/mori-conform-selftest-*/counter-*.py` (360 K, untracked and visible).
6. **MED** — the counters these instruments run hardcode the same lane scratch and take no scratch override: `round-38/count-c1.py:70` and `round-38/count-c4.py:45` → `round-38/scratch`, `round-39/count-c7.py:62` and `round-40/count-c8.py:62` → `round-39/scratch`, each with `makedirs`+`mkdtemp` (c1 `:915`/`:916`, c4 `:279`/`:280`, c7 `:475`/`:476`, c8 `:470`/`:471`). `--repo` never redirects a write.
7. **LOW** — `SKILL.md:908`, `:910`, `:911` name selftest forms for round-38, round-39 and round-40 only; `.ufo/waves/round-41/conform.py` and `round-42/conform.py` have no SKILL.md row, so the routed writer list cannot be rediscovered from the gate table — their forms exist only in `round-41/evidence/control-after.txt:64` and `round-42/evidence/control-c1-v4.txt:4`.
8. **LOW** — `.ufo/waves/round-42/conform.py` ships 17 selftest arms, but its only receipt (`round-42/evidence/control-c1-v4.txt:8`) records `pass=14 fail=0` at revision `9de7323d…`; my run at `8524904a` prints `CONFORM_SELFTEST pass=17 fail=0`. The three fixture arms have no receipt at the landed revision.
9. **LOW** — `.ufo/waves/round-40/conform.py:72`–`:73` is the only one of the five that derives `LANE` from `__file__` and puts `SCRATCH_ROOT` outside the lane (`tempfile.gettempdir()`); it is also the form a successor should copy. Its own run created nothing in the lane. Its counter (`round-40/count-c8.py:62`) would still write `.ufo/waves/round-39/scratch` on any full (`--arms real`) invocation — verified by direct probe.
10. **LOW** — the C1 `lane_writes` arm cannot see the dominant residue of these writers (empty directories): 18 empty scratch dirs in the lane produce 0 `git status --ignored` lines. Named limit of the frozen counter; routed to round 53, not changed here.
