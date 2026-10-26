# Mo50bExecScratchInventory — routed defect 4 (scratch inventory), round 50 a2w1

- Seat: `Mo50bExecScratchInventory` (executor, leaf). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
- Data revision read: `487941b9395e89678af0053cc443cdb49cdee6e3`. Working-tree HEAD at read time: `4548a34dc8b4072abaa4335c1f54a9efcfcc314a` (read only, never mutated).
- Routed defect: `corpus/lessons/round-49-verifier-spotcheck.md` §5 item 4 ("Delete the `.scratch/` residue (D-e) and the seven `round-40/scratch/mori-conform-selftest-*` dirs, then record the `git status --porcelain --ignored` count. Ignoring is not removal."), defect D-e at `:28`.
- Method: read-only. Every command below was run against the lane as it stood; no file was deleted, no git/jj mutating command was issued, nothing was committed. Scratch dir `/fast/scratch/hyaku/mori-r50/Mo50bExecScratchInventory/` held every temp file and was removed at the end.
- Tool installs: none needed (no `pacman`; nothing installed via uv/npx/binary).
- Counter contract untouched: `count-c1.py` / `count-c2.py` / controls / kill rules were not read for modification and none of this report proposes a counter change.

**The measurement is a moving target.** Sibling a2w1 seats were running throughout. Two timestamped snapshots are given; the drift between them is itself evidence (see §1 and §4).

## 1. `git status --porcelain --ignored` counts (item 1)

| time (local) | `status --porcelain --ignored \| wc -l` | `-- .scratch` | `status --porcelain \| wc -l` |
|---|---|---|---|
| 09:36 scan | **176** | **166** | **2** (`?? .ufo/waves/round-50/a2w1.ready`, `?? .ufo/waves/round-50/a2w1/`) |
| 09:50:44 | **187** | **170** | **9** (6 `??` round-40 conform selftest dirs + the 3 round-50 wave paths) |

Composition at 09:50:44 (187 lines): 170 `!!` under `.scratch/`, 6 `!! .ufo/waves/round-4*/__pycache__/`, 1 `!! tools/__pycache__/`, 1 `!! .jj/`, 9 `??` (all round-40 conform-selftest dirs plus the round-50 wave paths).

Composition at 09:36 (176 lines): 166 `!! .scratch`, 6 `!! .ufo/waves/round-4*/__pycache__/` (round-44,45,47,48,49,50), 1 `!! tools/__pycache__/`, 1 `!! .jj/`, 2 `??` (round-50 wave paths only).

Commands (exit 0 each):
```
git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --porcelain --ignored | wc -l           # 176 then 187
git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --porcelain --ignored -- .scratch | wc -l  # 166 then 170
git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --porcelain | wc -l                     # 2 then 9
```
Zero `??` paths existed under `.scratch/` at either time: every untracked byte there is ignored, so `git clean -X` reaches all of it.

## 2. `.scratch` on disk (item 2)

| measure | t1 09:36 | t2 09:50 |
|---|---|---|
| `ls -d /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/*/ \| wc -l` | **183** | **187** |
| top-level entries in `ls -A .scratch` | 187 (184 dirs incl. the dot-dir, 3 files) | 188 |
| `du -sh /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch` | **25G** | **26G** |

`du` then grew again on a third read (26G). `/home` is `/dev/mapper/root 930G, 318G used, 580G avail` (36%) — no ENOSPC risk, but the residue is the single largest consumer in the lane worktree.

Disk top-level breakdown (184 dirs at t2):

- **13 tracked top-level names** = 10 dirs + 3 root files: `round22/` (154 files), `rev-scorecard-claims/` (13), `CritFreezeTiming/` (13), `mutgate-eligible/` (11), `MutGateFirstParent/` (11), `CritConjunctSemantics/` (10), `CritNewSurvivor/` (3), `CritDrainedTuple/` (3), `critnewdag/` (2), `MutGateReadd/` (2), and root files `ExeDagN-c11-after-fixture-n.txt`, `SrcGitCommit-git-rev-parse.html`, `c11-after-fixture-r-ExeDagR.txt`. **225 tracked files, 28.3 MiB** (`git ls-tree -r -l 487941b -- .scratch` → `files=225 bytes=29682295`). Worktree `du` of those ten dirs: `round22` 28M, `CritFreezeTiming` 252K, rest 32–168K.
- **174 untracked dirs at t1, 178 at t2** (all ignored), grouped by name prefix at t1:

```
  56  pin-check-*      (17G total)
  38  r49-*            (6.5G; r49-L1 4.7G, r49-Mo49ExecCounterTiming 1.7G)
  34  r48-*            (2.1G with r48w2)
  33  r48w2-*          (r48w2-R48CritV3Junk2 328M)
  14  c1-*             (30M)
   1  reuse-hzxh6iqh
   1  rt-vrt6l1e1
   1  .scratch/.scratch  (nested, empty, 0 bytes)
```
- **8 of them are empty dirs**: `.scratch/.scratch`, `r48-ExecS478Recheck`, `r48-ScribeSkillRows`, `r48w2-R48RevEntryErrnoAliyun`, `r48w2-R48RevSkillScore`, `r48w2-R48RevEntryQuotactl`, `r48w2-R48ConnSiblings`, `r49-Mo49ScribeReadme`. Git never lists them, which is why 174 dirs yield only 166 `!!` lines.
- Age: every untracked dir is ≤ ~16.5 h old (oldest `.scratch/.scratch`, 59398 s; then `r48-ScribeRowQuotactl` 55023 s at read time). **4 dirs were created inside this session** — `pin-check-3zo2kvtm`, `-davjmdao`, `-hj3kv5fu`, `-yqc8dcmu` (mtime < 1 h), i.e. they belong to sibling a2w1 seats still running.

Where the 26G comes from: **`pin-check-*` alone is 17G in 56 dirs** (mean ≈ 300M; `pin-check-6pzn3pjt` 632M, eight others 326M each). `tools/mori-pin-check.py:884-887` creates `scratch = tempfile.mkdtemp(prefix="pin-check-", dir=os.path.join(repo, ".scratch"))` and `export_rev` (`:844-861`) extracts a **full `git archive` of the measured revision** into it; the cleanup is `finally: shutil.rmtree(scratch, ignore_errors=True)` at `:919-920`. So each *completed* run removes its own copy, and each killed/interrupted run permanently leaks ~300 MB. 56 leaks = 17 GB. `c1-*` (round-48/49 `count-c1.py:292/:332` default `--scratch` under `<repo>/.scratch`) is only 30M; seat dirs (r48/r49) hold the other ~8.6G.

## 3. Which `.scratch/<dir>` names committed files cite (item 3)

`git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -l '\.scratch/' 487941b` → 22560 output lines, 200+ files; most of them are the tracked `.scratch` files themselves. Resolution of every distinct citation token found by one pass (`git grep -I -o` at 487941b, 22683 `file:token` pairs, 5879 distinct tokens):

| resolution | file:token pairs |
|---|---|
| resolves to a **tracked** path under `.scratch` | 7288 |
| resolves to a path present on disk but **untracked** ("disk-only") | **613** |
| resolves to nothing (historical, truncated with `...`, or glob prose) | 14782 |

- **No file outside `.ufo/waves/` cites a disk-only `.scratch` path.** All 613 disk-only citations live in wave artifacts (219 distinct files under `.ufo/waves/`), overwhelmingly seat reports naming their own scratch dirs (`r48-*`, `r49-*`, `pin-check-*`). `corpus/knowledge/`, `corpus/lessons/`, `LOG.md`, `SKILL.md`, `SCORECARD.md` and `corpus/SOURCES.md` cite only **tracked** or **already-absent** `.scratch` paths.
- Therefore **no committed claim (corpus entry, SOURCES row, SCORECARD/SHONEN cell, counter, control) depends on bytes that exist only in the untracked residue.** The two committed surfaces that do name `.scratch` are:
  1. `corpus/knowledge/inheritance-d72ac16-r42.md:105-177` — 71 inherited `.scratch/*` paths named as the r41 freeze's provenance. **All 71 are tracked** (verified per directory above), so the entry stays resolvable from git after any worktree deletion.
  2. `corpus/lessons/round-40-verifier-spotcheck.md:53,58,84,89` — reproduction commands. `:58` uses `.scratch/CritNewSurvivor/survivor-deadloop-rebind.py` (present, tracked), `:53` uses `.scratch/CritFreezeTiming/…` (present, tracked). **`:84-89` uses `.scratch/critnewdag/repos/dag-z`, which is ALREADY ABSENT** (`test -e` → ABSENT). That committed reproduction command cannot run today, before any deletion of this round. `critnewdag/` survives with only its 2 tracked files (`build-dags.py`, `runlog.txt`); a nested git repo could never be tracked in the first place.
  3. Also already absent: `.scratch/MutMissing/`, `.scratch/MutStaleC1/`, `.scratch/MutStaleC2/` — cited by `corpus/lessons/round-46-verifier-spotcheck.md:73` only as debris to delete, so their absence is the desired outcome.
  4. `.scratch/.scratch/` (nested, empty) is cited by `.ufo/waves/round-47/w2/MutV2Rebound.md:125-127` as an empty parent left by a failed claim attempt; it holds nothing.
- Paths cited inside tool sources are fixture-relative, not lane paths: `tools/mori-pin-check.py:1043-1052,1319-1350` build `.scratch/old/foo.py` inside throwaway fixture trees, `tools/mori-unlanded-check.py:132` writes `.scratch/seat/out.txt` into its selftest fixture repo. `corpus/evidence/retention-allowlist.json` does not mention `.scratch` (`git grep -c` → rc 1).

## 4. `round-40/scratch/mori-conform-selftest-*` (item 4)

- At 09:36: **0** such dirs (`ls -d …/mori-conform-selftest-* | wc -l` → 0); `find` under the lane and `/tmp` → 0. The seven dirs the round-49 spotcheck saw are gone from disk. `.ufo/waves/round-40/scratch/` then held only its **8 tracked files** (`mutconform-arms2/` ×6, `selftest-v3-draft.txt`, `selftest-v3-draft2.txt`) and no untracked entry.
- At 09:50 a **peer re-created 9 of them** while this seat was reading: `mori-conform-selftest-{6_fk5rma, 6s3xg13_, 7thua84y, dm3w68ze, j83rllht, lwy1qfp9, m2cymdnp, mgcg1ura, nekzi665, zjnk_f21}` (9 at 09:50:01, 6 remained visible in `git status` at 09:50:44), 24–240K each, each holding the ten `counter-*.py` mutation copies. They are `??` — **not ignored**.
- Creator: `.ufo/waves/round-40/conform.py:70` `SCRATCH_ROOT = os.path.join(LANE, ".ufo", "waves", "round-40", "scratch")`; `:743` `work = tempfile.mkdtemp(prefix="mori-conform-selftest-", dir=SCRATCH_ROOT)` inside `def selftest(...)`; cleanup `:765` `shutil.rmtree(work, ignore_errors=True)` in the `try/finally`. So a *completed* `--selftest` leaves nothing; a run killed mid-way (timeout, SIGKILL, host crash) leaves one full dir. The same pattern with their own roots exists in `round-38/conform.py:239`, `round-39/conform.py:492`, `round-41/conform.py:930` (`dir=scratch_root`), `round-42/conform.py:946`, plus the round-40 fixture copies.
- They escape every gate: `.ufo/waves/round-40/scratch` is **not** gitignored (`git check-ignore` → rc 1), but `tools/mori-unlanded-check.py:15` scopes to `.ufo/waves/round-<N>/` for the current N only (selftest arm `other_round_not_listed`, `:135-137`), and QUALITY 80 (`corpus/QUALITY.md:366-372`) uses the same pathspec. Round-40 residue is therefore invisible to the unlanded gate forever.

## 5. Does any tool depend on `.scratch` existing? (item 5)

| tool | dependency | satisfied if `.scratch` is deleted? |
|---|---|---|
| `tools/mori-retention-gate.py --selftest` | `:459-468` requires `TMPDIR` to resolve to `<lane>/.scratch` **and `is_dir()`**; otherwise `SELFTEST retention-gate FAIL 0/21` rc 2 | Yes, **only if the caller runs the documented command**, which recreates it: `SKILL.md:178` writes `mkdir -p .scratch && TMPDIR=$PWD/.scratch python3 tools/mori-retention-gate.py --selftest`. A bare `TMPDIR=$PWD/.scratch …` after deletion fails rc 2 until the `mkdir` runs. |
| `tools/mori-pin-check.py` | `:532-534` `os.makedirs(root/.scratch, exist_ok=True)` then `mkdtemp(prefix="pin-tmp-")`; `:884-887` `os.makedirs(repo/.scratch, exist_ok=True)` then `mkdtemp(prefix="pin-check-")` | Yes — creates it on demand. |
| `tools/mori-pin-check.py --selftest` (SHONEN pin) | `:976` `mkdtemp(prefix="pin-selftest-")` under `TMPDIR` | Yes — never touches the lane's `.scratch`. |
| `tools/mori-unlanded-check.py --selftest` (SHONEN pin) | `:86` `mkdtemp(prefix="unlanded-selftest-")` under `TMPDIR` | Yes. |
| `tools/mori-content-review.py`, `mori-round19-regressions.py`, `mori-evidence-loss.py` | documented as `TMPDIR=$PWD/.scratch` (`SKILL.md:181,182,545`); `mori-content-review.py:383` uses `dir=tmpdir`, `mori-evidence-loss.py:779` reads `TMPDIR` | Yes — they need *a* `TMPDIR`, and the lane-`.scratch` choice is a documented convention (lane tools refuse a TMPDIR outside the lane root), not a stored state. |

Conclusion: **no tool needs the residue to exist**; the only path that needs the *directory itself* is the r18 retention-gate selftest, and its documented invocation creates it. Nothing in the frozen C1 surface (`SCORECARD.md` Axes cells, `SHONEN.md` pins, `count-c1.py`) reads `.scratch`, so removal cannot move C1 or C2.

## 6. Exact deletion list and commands (this seat deletes nothing)

Preconditions, in order: (a) only after the a2w1 wave is settled and the L1 has taken its own `git status` snapshot for the report; (b) a live sibling currently holds `.scratch/pin-check-*` and round-40 conform dirs, so run after WAVE-DONE, not mid-wave; (c) dry-run first.

### 6.1 The untracked/ignored residue (~26G, the routed defect)

```
L=/home/vgpnk/Projects/shokunin/mori-shokunin
git -C "$L" status --porcelain --ignored -- .scratch | wc -l        # BEFORE  (170 at 09:50:44)
git -C "$L" clean -ndX  -- .scratch                                  # dry run: names every path it would remove
git -C "$L" clean -fdX  -- .scratch                                  # DELETE
git -C "$L" status --porcelain --ignored -- .scratch | wc -l        # AFTER   (expected 0)
du -sh "$L/.scratch"                                                 # expected ~28.3 MiB (the tracked half)
```

`clean -X` removes **ignored** entries only and never removes a tracked file, so the 225 tracked files and the 10 tracked dirs survive; the pathspec `.scratch` keeps it from touching `.ufo/waves/*/__pycache__`, `tools/__pycache__` or `.jj/`. Never use `-x` (lower case) and never omit the pathspec.

The 178 top-level names its dry run would list, as read at 09:50:01 (a2w1 siblings added 4 more `pin-check-*` after this snapshot — the dry run above is authoritative at execution time):

```
.scratch
c1-0hwb4hai
c1-1x495mxj
c1-4wbl9rzh
c1-5pata5a4
c1-6_palov3
c1-7abgnspi
c1-92ev0hvl
c1-a4vak8t8
c1-dtqwk81s
c1-ia583qzp
c1-jop24kmf
c1-m0ua3cxh
c1-qm_4c5fn
c1-tgbnbdjm
pin-check-06xaefwz
pin-check-0cy90_mk
pin-check-15glu6ot
pin-check-187af_8h
pin-check-1btueoqu
pin-check-22cjc57q
pin-check-2dli76qp
pin-check-3feilgb1
pin-check-3pydnuk9
pin-check-3zo2kvtm
pin-check-51tsgf0q
pin-check-64i_4y27
pin-check-6pzn3pjt
pin-check-719mtsek
pin-check-76jccoid
pin-check-76uatnch
pin-check-7qpviv9j
pin-check-8vz5ihhm
pin-check-9bcyr_ki
pin-check-9ezbun8l
pin-check-_inon1ry
pin-check-_lurqwzj
pin-check-_yfoj3l2
pin-check-bqnxkdss
pin-check-davjmdao
pin-check-e_7l957x
pin-check-emgatfhj
pin-check-fc4lie4c
pin-check-fixxx_5q
pin-check-flkht0ed
pin-check-fvf56wxu
pin-check-g03_qw2w
pin-check-hj3kv5fu
pin-check-hv4xhuuk
pin-check-ibtrccoe
pin-check-ivsuogh1
pin-check-jactb34m
pin-check-jt0k9xn1
pin-check-kvsjhl53
pin-check-l33uhocv
pin-check-lbm38mz_
pin-check-lfqbxuzd
pin-check-mrkdly48
pin-check-nuhbnojp
pin-check-oixj90yr
pin-check-p6lscdby
pin-check-r2_fyswg
pin-check-r5g0gkny
pin-check-rgp261p1
pin-check-sfjnt4zf
pin-check-w12whlb9
pin-check-w4njmh9b
pin-check-wc3j6eet
pin-check-xe1436dy
pin-check-xm6f9q4n
pin-check-yqc8dcmu
r48-CritC1Counter
r48-CritC2Counter
r48-CritContractFreeze
r48-CritEntryRisk
r48-CritJunkClasses
r48-CritV3Spec
r48-ExecAppendSweep
r48-ExecC1Replay
r48-ExecCensusGuard
r48-ExecPortability
r48-ExecQuoteFinderErrno
r48-ExecQuoteFinderMan
r48-ExecRealRegistryAudit
r48-ExecS478Recheck
r48-ExecSkillRowsRun
r48-ExecUnlandedCheck
r48-ExecV3ImplA
r48-ExecV3ImplB
r48-ExecV3Residuals
r48-MutC1Variants
r48-RevPromptHonesty
r48-ScoutQuarantineS262
r48-ScoutQuarantineS268
r48-ScoutQuotaHost
r48-ScoutStagedQuota
r48-ScribeEntryA
r48-ScribeEntryB
r48-ScribeRowAliyun
r48-ScribeRowErrno
r48-ScribeRowQuotactl
r48-ScribeRowXfs
r48-ScribeSkillRows
r48-SimpCounters
r48-l1
r48w2-R48ConnSiblings
r48w2-R48CritEntryClaims
r48w2-R48CritFreeze
r48w2-R48CritV3Junk1
r48w2-R48CritV3Junk2
r48w2-R48ExecCensusEnd
r48w2-R48ExecD7
r48w2-R48ExecGates
r48w2-R48ExecLiveRefetch
r48w2-R48ExecRealRegistry
r48w2-R48ExecRerunC1
r48w2-R48ExecRerunC1Clone
r48w2-R48ExecRerunC2
r48w2-R48MutC1Counter
r48w2-R48MutC2Counter
r48w2-R48MutUnlanded
r48w2-R48MutV3Bind
r48w2-R48MutV3Header
r48w2-R48MutV3Hidden
r48w2-R48RevC1Counter
r48w2-R48RevC2Counter
r48w2-R48RevEntryErrnoAliyun
r48w2-R48RevEntryQuotactl
r48w2-R48RevEntryXfs
r48w2-R48RevHarnessLeak
r48w2-R48RevLesson
r48w2-R48RevQuality
r48w2-R48RevSkillScore
r48w2-R48RevV3Code
r48w2-R48ScoutEntryContext
r48w2-R48ScribeTrends
r48w2-R48SentTools
r48w2-R48SimpV3
r49-L1
r49-Mo49CritC1Counter
r49-Mo49CritC2Counter
r49-Mo49CritContractFreeze
r49-Mo49CritNewClasses
r49-Mo49ExecArmsBindUnlanded
r49-Mo49ExecArmsHeader
r49-Mo49ExecCensusMirror
r49-Mo49ExecControlsReplay
r49-Mo49ExecCounterTiming
r49-Mo49ExecFlaggedFixed
r49-Mo49ExecImplA
r49-Mo49ExecK2K8
r49-Mo49ExecK3K6K7
r49-Mo49ExecK5X1
r49-Mo49ExecQuotesConf
r49-Mo49ExecQuotesHost
r49-Mo49ExecQuotesSvc
r49-Mo49ExecRegistryAudit
r49-Mo49ExecRegressionCorpus
r49-Mo49ExecScratchHygiene
r49-Mo49MutC1Counter
r49-Mo49MutC2Counter
r49-Mo49RevC1Counter
r49-Mo49RevC2Counter
r49-Mo49RevPromptHonesty
r49-Mo49ScoutStagedJournal
r49-Mo49ScribeDisposition
r49-Mo49ScribeEntryA
r49-Mo49ScribeEntryB
r49-Mo49ScribeLessonGate
r49-Mo49ScribeReadme
r49-Mo49ScribeRowConf
r49-Mo49ScribeRowCtl
r49-Mo49ScribeRowHost
r49-Mo49ScribeRowSvc
r49-Mo49ScribeSkillRows
r49-Mo49SimpCounters
reuse-hzxh6iqh
rt-vrt6l1e1
```

### 6.2 The round-40 conform-selftest dirs (not ignored, so `clean -X` does not reach them)

```
find "$L/.ufo/waves/round-40/scratch" -maxdepth 1 -name 'mori-conform-selftest-*' -type d -print   # dry run
find "$L/.ufo/waves/round-40/scratch" -maxdepth 1 -name 'mori-conform-selftest-*' -type d -exec rm -rf {} +
```
0 dirs existed at 09:36; 9 appeared at 09:50 from a peer's killed run. Nothing under that path is tracked (`git ls-tree -r 487941b -- .ufo/waves/round-40/scratch` → 8 files, none matching).

### 6.3 The tracked half — a decision, not a cleanup

225 tracked files (28.3 MiB) are tracked *and* matched by `.gitignore:5`. Two coherent choices:

- **Leave tracked (recommended, zero claim risk).** They are committed evidence; `inheritance-d72ac16-r42.md:105-177` enumerates 71 of them and round-40's reproduction commands at `:53,58` use two. Bytes are already in git; nothing dangles.
- **Drop from the index while keeping history:** `git -C "$L" rm -r --cached --quiet .scratch` then one lane commit. This makes them untracked-and-ignored, so a *later* `clean -fdX` would then delete the worktree copies; they stay recoverable via `git show 487941b:.scratch/<path>` and the r41 freeze commit `d72ac16`. Do not pair `--cached` with a same-day `clean -fdX` in one step.

Do **not** use `git rm -r .scratch` in this round: it would delete the 71 paths `inheritance-d72ac16-r42.md` names from the worktree, and it is a 225-deletion commit inside a data-only round.

### 6.4 Counts the L1 should record after execution

- `git status --porcelain --ignored | wc -l`: 187 (at 09:50:44) → **17** after 6.1 + 6.2 (6 `!! .ufo/waves/round-4*/__pycache__/`, 1 `!! tools/__pycache__/`, 1 `!! .jj/`, and the `??` round-50 wave paths that the L1 will commit → **8** once those land).
- `ls -d .scratch/*/ | wc -l`: 187 → **10** (exactly the ten dirs that contain tracked files; every other top-level dir is in 6.1's list, including the hidden empty `.scratch/.scratch`, which `ls -d *` never counted).
- `du -sh .scratch`: 26G → **~28 MiB**.

## 7. Retained evidence (command → observed, rc 0 unless stated)

- `git -C $L status --porcelain --ignored | wc -l` → `176` (09:36), `187` (09:50:44)
- `git -C $L status --porcelain --ignored -- .scratch | wc -l` → `166`, then `170`
- `git -C $L status --porcelain | wc -l` → `2`, then `9` (contents quoted in §1)
- `ls -d $L/.scratch/*/ | wc -l` → `183`, then `187`
- `du -sh $L/.scratch` → `25G`, then `26G`
- `git -C $L ls-tree -r --name-only 487941b -- .scratch | wc -l` → `225`; top-level dirs → 10; root files → 3
- `git -C $L ls-tree -r -l 487941b -- .scratch | awk '{s+=$4} END{print NR, s}'` → `225 29682295` (28.3 MiB)
- `du -sch $L/.scratch/pin-check-* | tail -1` → `17G`; `ls -d pin-check-* | wc -l` → `56`; `du -sch r49-* | tail -1` → `6.5G`; `du -sch r48* | tail -1` → `2.1G`; `du -sch c1-* | tail -1` → `30M`
- `df -h $L` → `/dev/mapper/root 930G 318G 580G 36% /home`
- one-pass citation resolution at 487941b: `22683` pairs → tracked `7288`, disk-only `613`, absent `14782`; all disk-only citations under `.ufo/waves/` (219 files)
- `git -C $L grep -l '\.scratch/' 487941b` → 200+ files (22560 lines); non-wave subset = `.gitignore`, `LOG.md`, `SKILL.md`, `considerthese/2026-10-24.md`, `corpus/knowledge/inheritance-d72ac16-r42.md`, 30 `corpus/lessons/*.md`, `tools/mori-pin-check.py`, `tools/mori-unlanded-check.py`
- `test -e $L/.scratch/critnewdag/repos/dag-z` → ABSENT; `…/CritNewSurvivor/survivor-deadloop-rebind.py` → PRESENT (tracked); `…/MutMissing`, `…/MutStaleC1`, `…/MutStaleC2` → ABSENT
- `ls -d $L/.ufo/waves/round-40/scratch/mori-conform-selftest-*` → 0 at 09:36; `find … -name 'mori-conform-selftest-*'` → 9 at 09:50 (all `??`, 24–240K)
- `git -C $L check-ignore -v .scratch/x` → `.gitignore:5:.scratch/` rc 0; `check-ignore .ufo/waves/round-40/scratch/x` → rc 1 (not ignored)
- `sed -n '459,468p' tools/mori-retention-gate.py` → `expected_tmp = (root/".scratch").resolve()` … `if actual_tmp != expected_tmp or not actual_tmp.is_dir(): return FAIL 0/21, 2`
- `grep -n 'rmtree\|finally:' tools/mori-pin-check.py` → `548/549`, `919/920`, `1414/1415`

## 8. Limits / risks I could not close

- **The count is live.** 4 (then 9) paths appeared during this read; the 09:50:44 figure is not reproducible after the wave settles. The L1 must re-measure, and the numbers a report cites should carry their timestamp.
- `.scratch` growth is **structural, not one-off**: 56 leaked `pin-check-*` full-tree exports are 17G of the 26G, and every killed `pin-check --rev`/`--root` run adds ~300M. Deletion alone does not close the routed defect; the durable fix would be a cleanup for interrupted runs or an off-lane export root — that is a tool change, which this round's freeze and the data-only remit put out of scope. Named as a limit, not proposed as a fix.
- I did not read `/tmp` contents beyond counting `mori-conform-selftest-*` (0). Round-38's `/tmp` leak report (`round-38/w2/RevC5Scratch.md:56`) is historical; no `/tmp` path is cited as evidence here.
- No host/kernel state was touched: no journal/MESSAGE read, no cgroup, no systemctl, no OOM. No pacman.
- Attribution of the 09:50 conform-selftest burst to a specific peer is not possible from read-only evidence; the roster shows six sibling executors/mutation-testers running.

## Findings

1. **MED — routed defect 4 is only half realisable by deletion, because 225 of the residue's files are *tracked*.** `.scratch/` at 487941b holds 225 tracked files in 10 dirs + 3 root files (28.3 MiB) while `.gitignore:5` also matches them. A naive `rm -rf .scratch` leaves 225 worktree deletions in `git status`; `git clean -X` correctly leaves them alone. Files: `.gitignore:5`, `.scratch/**` at 487941b.
2. **MED — 17G of the 26G residue is leaked by the lane's own registered instrument.** `tools/mori-pin-check.py:884-887` exports a full `git archive` of the measured revision into `<lane>/.scratch/pin-check-<rand>` (~300M per run; one at 632M) and removes it only in `finally: shutil.rmtree(...)` at `:919-920`; 56 killed runs ⇒ 17G. Lines: `tools/mori-pin-check.py:844-861,884-887,919-920`.
3. **MED — the `round-40/scratch/mori-conform-selftest-*` debris is live, not historical.** 0 dirs at 09:36; 9 re-created at 09:50 by a sibling running `.ufo/waves/round-40/conform.py --selftest`; they are untracked-and-not-ignored (`??`), so they count in plain `git status --porcelain` and are invisible to the unlanded gate, which scopes to the current round only (`tools/mori-unlanded-check.py:15,135-137`; `corpus/QUALITY.md:366-372`). Lines: `.ufo/waves/round-40/conform.py:70,743,765`.
4. **MED — a committed reproduction command already cannot run.** `corpus/lessons/round-40-verifier-spotcheck.md:84-89` invokes `tools/mori-sources-appendonly.py … --repo .scratch/critnewdag/repos/dag-z`, and `.scratch/critnewdag/repos/dag-z` does not exist on disk and never could be tracked (nested git repo). Pre-existing, independent of this round's deletion. Lines: `corpus/lessons/round-40-verifier-spotcheck.md:84,89`.
5. **MED — deleting mid-wave destroys sibling work.** 4 `pin-check-*` dirs were created inside this session (<1 h mtime), and 6 conform dirs were mid-flight at 09:50:44; the deletion must run after WAVE-DONE, and the `pin-check` cleanup is not idempotent against live runs.
6. **LOW — the round-49 figure is already stale.** `corpus/lessons/round-49-verifier-spotcheck.md:28` records "about 183 `.scratch/` directories"; the count read 183 at 09:36 and 187 at 09:50. The L1's post-deletion count needs its own timestamp and command. Line: `corpus/lessons/round-49-verifier-spotcheck.md:28`.
7. **LOW — one tool's selftest needs the `.scratch` *directory*.** `tools/mori-retention-gate.py:459-468` fails rc 2 unless `TMPDIR` resolves to `<lane>/.scratch` and is a directory; the documented invocation recreates it (`SKILL.md:178` = `mkdir -p .scratch && TMPDIR=$PWD/.scratch …`). Deletion is safe only if callers use the documented form. Lines: `tools/mori-retention-gate.py:459-468`, `SKILL.md:178`.
8. **LOW — `git status --porcelain` alone understates the residue.** All untracked `.scratch` content is ignored (0 `??` there), so `--porcelain` showed 2 (then 9) while `--ignored` showed 176 (then 187). A round that records only the plain count records none of the 26G. Command pair in §1.
9. **LOW — no committed claim is at risk from the deletion.** 613 disk-only `.scratch` citations exist, all inside `.ufo/waves/` seat reports; every `corpus/knowledge`, `corpus/SOURCES.md`, `SCORECARD.md`, `SHONEN.md` and lesson citation resolves to a tracked path or is already absent (§3). Reporting that the tracked half *is* cited (71 paths, `corpus/knowledge/inheritance-d72ac16-r42.md:105-177`) so the L1 does not delete it by accident.
