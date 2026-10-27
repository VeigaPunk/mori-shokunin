# Mo52SentBoundary — adjacency and safety review of the round-52 data

Seat: Mo52SentBoundary (sentinel, leaf). Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Data under review: `8524904adb25e44f24d9f25aac7eae909625c18c` (committed 2026-10-26 21:07:40 -0300), diffed against
entering tip `4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d`. Lane tip during review: `075436b1346ca659afb8be7a46f0e67e4170aa83`.
Contract read first: `.ufo/waves/round-52/contract.md`. Counters/predicates/controls/kill rules not touched, not
proposed as changed. No tool installed, no host write, no sysctl read or write, no pacman invocation.

Scratch: `/fast/scratch/hyaku/mori-r52/Mo52SentBoundary/` (`TMPDIR` set inside it, removed at the end). One
`git archive` extraction (the round-39 instrument only, 120K) and one throwaway fixture repo; toplevel verified
`/fast/scratch/hyaku/mori-r52/Mo52SentBoundary/fakelane` before the first commit. Disk guard checked before the
work: `/fast/scratch/hyaku` 24% used, 616.3G free.

## What I checked (three arms of my seat)

    $ git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff 4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d 8524904adb25e44f24d9f25aac7eae909625c18c
      33 files +7933 -3   (10 non-round files: SCORECARD.md, corpus/QUALITY.md, corpus/README.md, corpus/SOURCES.md,
      corpus/evidence/sources-r52/*.v7.2 x5, corpus/knowledge/overcommit-commit-limit-r52.md)
    $ git -C <lane> diff <entering> 8524904adb -- corpus/QUALITY.md corpus/README.md   -> 34 added lines
    $ git -C <lane> show 8524904adb:corpus/knowledge/overcommit-commit-limit-r52.md     -> 75 lines
    $ git -C <lane> grep -n '/home/vgpnk' 8524904adb -- .ufo/waves/round-52/
      build-w1-spec.py:4  evidence/census-start.txt:2  evidence/control-c1-*.txt:1 each  w1-spec.json:67
      count-c1.py:0  count-c2.py:0  controls/c1-controls.py:0  controls/c1-data.py:0  contract.md:0

### Arm 1 — text that instructs a host write, an allocation, a swap/cgroup change, or claims host configuration

| text | what it says | verdict |
|---|---|---|
| `overcommit-commit-limit-r52.md:63-66` | "mori reads them and never writes a `vm.*` sysctl. Choosing or changing the overcommit mode is host configuration, which the operator owns." + "this entry claims no sysctl ownership for either lane." | clean — the ownership claim runs the safe way: the lane disclaims it |
| `overcommit-commit-limit-r52.md:70` | "this host's sysctl values are not claimed" | clean |
| `overcommit-commit-limit-r52.md:9` (`recheck:`) | `for u in <5 urls>; do curl -fsSL "$u" \| sha256sum; done` | clean — reads stdin to stdout, writes no file, needs no TMPDIR |
| `overcommit-commit-limit-r52.md` reading-rules table | a named kernel log line (`__vm_enough_memory: pid: N, comm: X, bytes: B not enough memory for the allocation`) as a refusal signal, "rate-limited, so not a count" | clean — it is not a kill record and the entry does not tell the reader to count it (QUALITY 15 concerns counting a journal class by message text; no count is made) |
| `corpus/SOURCES.md` S497–S501 | quotes and anchors only | clean — `grep -cE 'sysctl -w\|> /proc\|tee /proc'` over the added rows = 0 |
| `corpus/evidence/sources-r52/vm.rst.v7.2:256,260,264` | `echo 1 > /proc/sys/vm/drop_caches` (and 2, 3) | clean — upstream documentation bytes copied as evidence, not an instruction; the entry never cites drop_caches |
| `SCORECARD.md` 3 Axes cells; `SHONEN.md` unchanged (`0` added lines) | no host-configuration claim | clean |

No added line anywhere in the diff instructs a reader to write a sysctl, to trigger an allocation, or to change
swap, a cgroup limit or a watermark (scan over all `+` lines for `sysctl -w`, `/proc/sys/*` redirects, `swapoff`,
`swapon`, `cgroup`, `systemd-run`, `fallocate`, `truncate -s`, `memory.max`, `oom_score_adj`: the only hits are the
prohibition line in the dispatch spec and the upstream drop_caches quote above).

### Arm 2 — commands in the entry and the appended QUALITY/README text that write

| command as published | writes? | where |
|---|---|---|
| `python3 tools/mori-sources-appendonly.py --selftest` — `QUALITY.md:1360`, `README.md:727` | yes, bounded and self-cleaning | `tempfile.mkdtemp(prefix="mori-sources-appendonly-selftest-")` (no `dir=`, so `$TMPDIR`), removed at `shutil.rmtree(root)`; QUALITY 141 states the `git archive` + `TMPDIR`-in-scratch condition |
| `python3 .ufo/waves/round-52/count-c1.py <rev>` — `QUALITY.md:1361,1370`, `README.md:733` | archive under `--scratch`/`$TMPDIR`, refuses a scratch inside the repo (`:504-506`), removes it on exit | `.ufo/waves/round-52/count-c1.py` — but it executes the pinned commands, so it inherits the row below |
| `python3 .ufo/waves/round-39/conform.py 4f266ef2… --selftest` — `README.md:728` | **yes, into the lane** | see F1 |

### Arm 3 — new absolute host path in committed executable code

| file (new in this diff) | `/home/vgpnk` hits | used to resolve IO? | verdict |
|---|---|---|---|
| `.ufo/waves/round-52/build-w1-spec.py` | 4 (lines 46, 47 in the seat-rules string; 111 and 193 in prompt templates) | **no** — `L`, `F`, `W` derive from `os.path.abspath(__file__)` (lines 9-12); `X` is the scratch root | no host path is a default; the hits are prose inside committed prompt text |
| `count-c1.py`, `count-c2.py`, `controls/c1-controls.py`, `controls/c1-data.py`, `contract.md` | 0 | — | clean |
| `w1-spec.json` (dispatch record, data not code) | 67 | — | embeds the absolute lane/scratch paths it dispatched with; a record, not an IO default |

No new committed executable file outside `.ufo/waves/round-52/` was added by this diff.

## F1 evidence — the appended README pin writes into the lane, and round 52 made it runnable and machine-run

1. The published pin, at DATA (`corpus/README.md:728`):
   `python3 .ufo/waves/round-39/conform.py 4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d --selftest` → `CONFORM_SELFTEST pass=9 fail=0`.
   At the entering tip (`README.md:607`) the same row held only `` `--selftest` → `pass=9 fa… ``, which named no
   command. The round-52 appended block supplies the runnable form, so this row becomes a live pin that arm (C)
   runs on every C1 run.
2. Arm (C) did run it at data — `.ufo/waves/round-52/evidence/c1-at-data.txt:16`:
   `item living corpus/README.md:728 expect=CONFORM_SELFTEST_pass=9_fail=0 got=CONFORM_SELFTEST_pass=9_fail=0_rc=0 state=ok`
   (`$ python3 .ufo/waves/round-52/count-c1.py 8524904adb… --scratch /fast/scratch/hyaku/mori-r52/l1/c1data`, exit 0).
3. The instrument's write target is a hardcoded lane path (`.ufo/waves/round-39/conform.py` at DATA):
   `:53  LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"`
   `:54  SCRATCH_ROOT = os.path.join(LANE, ".ufo", "waves", "round-39", "scratch")`
   `:491 os.makedirs(SCRATCH_ROOT, exist_ok=True)`
   `:492 work = tempfile.mkdtemp(prefix="mori-conform-selftest-", dir=SCRATCH_ROOT)`
   `:501 with open(path, "w", encoding="utf-8") as handle:`   (nine mutant counters, one per check)
   `:520 parser.add_argument("--repo", default=LANE)`  and `counters = args.counter or DEFAULT_COUNTERS`, where
   `DEFAULT_COUNTERS = [os.path.join(LANE, ".ufo/waves/round-39/count-c7.py")]`.
   Because the `dir=` is explicit and LANE-derived, `TMPDIR` (which `count-c1.py` sets to `<scratch>/tmp`) does not
   move the write, and because the constant is absolute, running from the counter's `git archive` of R does not
   sandbox it either: the archived copy still writes the live lane and reads the live lane's working-tree
   `count-c7.py`.
4. Isolated reproduction — `git archive 8524904adb .ufo/waves/round-39/{conform.py,count-c7.py,contract.md,fixtures}`
   into a throwaway repo, **only change** `LANE` repointed to that repo, `cwd` = that repo:
   `$ python3 .ufo/waves/round-39/conform.py HEAD --selftest` → `CONFORM_SELFTEST pass=9 fail=0`, **rc=0**.
   After it: `.ufo/waves/round-39/scratch/` exists and is empty; `git status --porcelain --ignored --untracked-files=all`
   prints **0** lines. While a work dir is populated the same command prints
   `?? .ufo/waves/round-39/scratch/mori-conform-selftest-PROBE/counter-x.py`; after the work dir is removed, 0 lines again.
5. The real lane, live during this wave (three point-in-time reads; nothing of mine wrote there):

       $ ls -la /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-39/scratch   # 21:13:19
         drwx------ mori-conform-selftest-x0r6pur0   (counter-bounded_reads.py, counter-drain_shape.py,
         counter-head_pin.py, counter-predicate.py, counter-timeout_value.py, counter-tool_resolve.py, ~22 KB each)
       $ find <that dir> -printf '%y %s %TH:%TM:%TS %p'   # 21:15:29
         d 264 21:15:28 …/mori-conform-selftest-rg3dxsb9
         f 22531 21:15:11 …/rg3dxsb9/counter-predicate.py
         f 22520 21:15:15 …/rg3dxsb9/counter-head_pin.py   (… six mutant counters, ~3.2 s apart)
         d 220 21:15:28 …/mori-conform-selftest-0tcik9lr    (five files by 21:15:29)
         d 220 21:15:29 …/mori-conform-selftest-f123bwhj
         d 172 21:15:27 …/mori-conform-selftest-qsv_zgwo
         count=24 entries, du -sb = 450137 bytes
       $ stat -c '%n ctime=%z' .ufo/waves/round-39 .ufo/waves/round-39/scratch .git/index
         .ufo/waves/round-39          ctime=2026-10-25 03:49:32   (the parent, so `scratch` pre-dates today)
         .ufo/waves/round-39/scratch  ctime=2026-10-26 21:15:16   (entry churn today)
         .git/index                  ctime=2026-10-26 21:11:32

   So: up to four concurrent runs wrote ~450 KB of ~22 KB mutant counters into the committed lane tree at
   21:11-21:15 today, each run leaving only the (possibly pre-existing) empty parent behind. This is exactly the
   class routed defect 8 names, now demonstrated with a lane write, and it is reached by a command this round's own
   appended README text publishes.

Impact on the claim (F2, reported separately because the remedy is different): the at-data receipt asserts
`lane_writes=0`, and the guard is `status()` = `git -C repo status --porcelain --ignored --untracked-files=all`
sampled once after evaluation. A write that is removed before the sample, or that leaves only an empty directory,
is invisible to it — as my probe shows — and so is any write into `.git/` (the guard's own `git status` rewrote
`.git/index` at 21:11:32). The 450 KB observed in the lane therefore coexists with the receipt's `lane_writes=0`
without contradiction, which is the defect.

Smallest honest remediation *for the data* (L1's call; not a counter change): the README bullet at
`corpus/README.md:728` can carry the same disclosure QUALITY 141 carries, in a form that is true — the instrument's
write target is `<lane>/.ufo/waves/round-39/scratch/`, not `$TMPDIR`, so a "run it in an archive with TMPDIR in
scratch" clause would be false here. The window remedy is the successor freeze of the round-38..42 `conform.py`
writers (routed defect 8), routed again below.

## Checked and clean (no finding)

- The entry's ownership sentence (`:63-66`) and boundary (`:70`) are correct as written: read-only reads, operator
  owns the mode, no sysctl ownership claimed for mori or tsukuroi.
- `tools/mori-sources-appendonly.py --selftest` writes only under a bare `tempfile.mkdtemp()` (`:963`) and removes
  it (`:1070`); QUALITY 141's check text already states the archive + `TMPDIR` condition.
- `count-c1.py` refuses a `--scratch` inside the measured repo (`C1_SETUP scratch … lies inside the repo`, exit 2)
  and removes its archive; its own writes are outside the lane.
- `count-c2.py` opens lane files read-only (`:327`) and runs only `git show`/`ls-tree`/`rev-parse`.
- The five `corpus/evidence/sources-r52/*.v7.2` copies are frozen upstream bytes; their `echo N > /proc/…` lines are
  quotations in evidence, not lane instructions.
- `SCORECARD.md`'s three edited Axes cells and the unchanged `SHONEN.md` carry no host-configuration claim.

## Named limits of this review

- My reproduction repointed one constant (`LANE`) in a scratch copy of `conform.py`; the real instrument's target is
  the same expression with the lane path (source lines 53-58, 491-501), so the behaviour, not just the text, was
  observed — but the real run itself was deliberately not executed by me.
- I did not run `count-c1.py` at DATA (heavy, CPU-contended, and it would perform the write in F1). I read the
  at-data receipt instead; its `README.md:728 … state=ok` line is the proof that arm (C) executed the pin.
- Live-lane observations are point-in-time (21:11, 21:13, 21:15). The 24 entries / 450137 bytes is a snapshot, not a
  peak.
- I did not read or judge the claim rows (entailment is the ENTAILMENT seats' arm), nor the counters' logic beyond
  the write and guard paths.

## Routed to round 53 (no counter, predicate, control or kill-rule change proposed for this round)

1. `conform.py` in `.ufo/waves/round-38/`, `round-39/`, `round-41/`, `round-42/`: derive `LANE` from `--repo`/env and
   `SCRATCH_ROOT` from an explicit `--scratch`, so an archive run cannot reach the lane (successor freeze; routed
   defect 8).
2. `lane_writes` (count-c1.py `status()`/`lane_writes()`): a post-run `git status` snapshot cannot see a write that
   was removed, an empty-dir residue, or a `.git/` write. Any successor should diff the tree between sample points.
3. `controls/c1-controls.py:57-58` writes its receipts straight into `{W}/evidence/control-c1-<name>.txt`; add an
   output-directory argument before any seat is invited to run it unqualified.

## Findings

| # | severity | file / line | finding |
|---|---|---|---|
| F1 | HIGH | `corpus/README.md:728` (round-52 appended block) with `.ufo/waves/round-39/conform.py:53,54,491,492,501,520` | The appended README text publishes `python3 .ufo/waves/round-39/conform.py <rev> --selftest` as a runnable living pin. Run as written — and run automatically by `count-c1.py` arm (C) on every C1 run, per `evidence/c1-at-data.txt:16` — it creates `mori-shokunin/.ufo/waves/round-39/scratch/<work>/` and writes nine ~22 KB mutant counters there, because the instrument's `LANE` and `SCRATCH_ROOT` are hardcoded to the lane and `mkdtemp(dir=…)` ignores `TMPDIR` and the counter's archive. Observed in the real lane at 21:11-21:15 on 2026-10-26: up to four concurrent work dirs, 24 entries, 450137 bytes. Neither the README bullet nor QUALITY 141 discloses a lane write; a "run it in an archive with `TMPDIR` in scratch" clause would not prevent it. Verdict: the round's data instructs a reader to write into the measured lane. |
| F2 | HIGH | `.ufo/waves/round-52/count-c1.py` `status()` at `:527`, `run()` at `:534`, `lane_writes()` at `:562`; receipt `evidence/c1-at-data.txt` (`lane_writes=0`) | The claim's no-write guard cannot see F1's writes: it samples `git status` once after evaluation, so a write removed by the instrument's own `finally` or one that leaves only an empty directory leaves `lane_writes=0`. Reproduced: after a selftest run the residue directory exists and `git status --porcelain --ignored --untracked-files=all` prints 0 lines; a populated work dir prints `?? …/counter-x.py`. The guard also mutates the lane's `.git/index` itself (mtime 21:11:32) and, by the counter's own named limit, cannot see `.git/` writes. Verdict: `lane_writes=0` at data is not evidence that the measured repo was unwritten. Named limit and round-53 item, not a change now. |
| F3 | MED | `.ufo/waves/round-52/controls/c1-controls.py:56-63` | The script's default output is `{W}/evidence/control-c1-<name>.txt` (line 56 builds the path, line 57 opens it `"w"`), i.e. the frozen control receipts other seats cite; there is no `--out`. One unqualified run rewrites them in place — the round-51 defect-6 class. The wave spec warns seats to copy and edit (`build-w1-spec.py:117`), but the hazard is a default of committed executable code, not a documented option. Verdict: latent receipt-rewrite path; no rewrite observed in this wave. |
| F4 | LOW | `.ufo/waves/round-52/build-w1-spec.py:206` | `open(os.path.join(W, "w1-spec.json"), "w")` rewrites the committed dispatch record (the 68 prompts actually sent) in place; the file also embeds 67 absolute host/scratch paths. Regeneration after dispatch silently changes the record of what was dispatched. Path resolution itself is portable (`__file__`-derived), so the absolute-path arm is clean. |
| F5 | LOW | wave context and `build-w1-spec.py:37-38` vs `evidence/` at DATA | `evidence/c1-at-data.txt`, `c2-at-data.txt`, `c2-hashes-at-data.txt` do not exist at DATA: `git cat-file -e 8524904adb:.ufo/waves/round-52/evidence/c1-at-data.txt` → `fatal: … exists on disk, but not in '8524904adb'`, exit 128. They were written at 21:08 and land in `075436b1`. Every seat is pointed at them "at DATA". The receipts are genuine runs at the data rev (first line is the literal command), so this is a pointer/timing defect, not fabricated provenance. |
| F6 | LOW | `corpus/knowledge/overcommit-commit-limit-r52.md:65-66` | The ownership disclaimer cites `../tsukuroi-shokunin/PROVINCE.md:8-14,28`: the quoted words "Detection and report; the operator remediates" are at line 28 (verified), but `:8-14` is the pacman/systemd/driver owns block and does not cover memory or sysctls — the memory sentence is at `:30-32` and the domain at `:3-4`. The disclaimer is correct and the pointer is near; the range is approximate. |

Report: `.ufo/waves/round-52/w1/Mo52SentBoundary.md`
