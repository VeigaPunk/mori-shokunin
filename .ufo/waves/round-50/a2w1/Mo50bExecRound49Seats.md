# Mo50bExecRound49Seats — the two round-49 wave-1 seats that had no report at filing

Seat: Mo50bExecRound49Seats (executor, leaf). Round 50, wave a2w1, lane `mori-shokunin`.
Mode: **read-only accounting** of round 49's two late seats. No lane file was edited; nothing was
committed, staged, checked out or reset; no jj command was run; `pacman` was not run and nothing was
installed. Scratch: `/fast/scratch/hyaku/mori-r50/Mo50bExecRound49Seats/tmp` (`TMPDIR` set for every
call; removed before this report was finalised). The only file written is this report.
Frozen artefacts (round-50 counters, controls, kill rules) were read, never proposed for change.

Ticket: routed defect 5 of `/home/vgpnk/Projects/shokunin/.ufo/reports/round-49/mori.md` line 9 —
account for `Mo49ExecCounterTiming` and `Mo49SimpCounters`.

---

## 1. The premise is now out of date: both seats have reports on disk, and both are committed

The round-49 report filed at `43d84666` (author and committer `2026-10-25 22:56:42 -0300`) says 47 of
49 reports were on disk. That was true at the filing instant. Both missing seats wrote their reports
**after** that instant, so the correct reading is "two reports arrived late", not "two dead seats":

| artefact | mtime (disk) | first commit carrying it | commit dates |
|---|---|---|---|
| `.ufo/waves/round-49/w1/Mo49SimpCounters.md` (23,158 B, 339 lines) | `2026-10-25 23:02:40` | `7197160b927f04db294c9553fb48fadcc7a3f4e3` | author `2026-10-25 23:04:10`, committer `2026-10-25 23:16:36` |
| `.ufo/waves/round-49/w1/Mo49ExecCounterTiming.md` (21,140 B, 288 lines) | `2026-10-25 23:39:03` | `9b8562a371dc916fdc0fc686619ea1e271a3e118` | author `2026-10-26 09:05:31`, committer `2026-10-26 09:05:33` |

Report-file population of `.ufo/waves/round-49/w1/` by revision (`git ls-tree --name-only <rev> -- .ufo/waves/round-49/w1/`):

| revision | entries | `.md` | SimpCounters | CounterTiming |
|---|---|---|---|---|
| `43d84666` (round-49 filing) | 48 | 47 | absent | absent |
| `7197160b` (orchestrator in-flight snapshot; round-50 entering tip) | 49 | 48 | present | absent |
| `9b8562a3` (round-50 salvage) | 50 | 49 | present | present |
| `487941b9` (round-50 attempt-2 data) / `HEAD` `4548a34d` | 50 | 49 | present | present |

- `Mo49SimpCounters.md` entered the tree inside commit `7197160b`, whose message is *"hyaku run 7
  interrupted: in-flight snapshot committed by the orchestrator (not a landing); lane L1 resumes from
  here"* — `git show --stat 7197160b` reports exactly one file, `+339` lines. It was therefore already
  committed **before** any round-50 paper existed, including the round-50 contract that says "one late
  report is on disk".
- `Mo49ExecCounterTiming.md` was written 42 minutes after the lane tip commit and stayed untracked
  through the round-49 closure and through round-50 attempt 1's wave 1
  (`.ufo/waves/round-50/w1/Mo50ScribeEntryA.md:13` records it as the only untracked round-49 report).
  The round-50 salvage committed it. `git log --format='%h %ci' -- .ufo/waves/round-49/w1/Mo49ExecCounterTiming.md`
  → `9b8562a3 2026-10-26 09:05:33 -0300`, i.e. the salvage is its only commit.
- Bytes are identical on disk, at `HEAD` and at `9b8562a3`:
  `sha256(Mo49ExecCounterTiming.md) = 128a6fb14403789b82e6632fc32e121c56c2c302d7e907ab1ec1cf7b9a83e7e0`
  for all three reads; `sha256(Mo49SimpCounters.md) = fe8b27c085b5195d227e94f4eb3652eda77d0816fee95b96b046536b4c8f3f22`.
  `git status --porcelain --ignored -- .ufo/waves/round-49/` prints only `!! .ufo/waves/round-49/__pycache__/`, rc 0.

So: **`Mo49SimpCounters` is not a seat with no output anywhere** — the round-50 contract's parenthetical
"one late report" undercounts by one. Both seats delivered complete reports; neither is a dead seat.

## 2. What the late `Mo49ExecCounterTiming` report contains

It is a real 288-line cost profile of the reconciler under the round-49 C1 counter (subject bytes: the
entering tool `controls/tool-v3-entering.py`, `85a89a3b…` = `tools/mori-pin-check.py` at `b3e3453d`),
not a stub and not a marker. Six findings (`.ufo/waves/round-49/w1/Mo49ExecCounterTiming.md:248-288`):

| # | sev | finding | line |
|---|---|---|---|
| CT-1 | MED | one pinned command is 69 % of every reconciler run and is idle: `conform.py <rev> --selftest` = 58.69 s wall / 3.62 s CPU of an 85.3 s pin phase; pins are measured strictly serially, so the wait is paid 26× per counter invocation | `:250` |
| CT-2 | MED | the counter's isolation claim does not hold: `conform.py` hardcodes the absolute lane path and `mkdtemp`s `mori-conform-selftest-*` **inside the lane repo**, 26× per counter run, while `count-c1.py`'s usage paragraph says the lane repo is only read; `ignore_errors=True` hides cleanup failures | `:257` |
| CT-3 | MED | per-variant wall is scheduler noise (identical SKILL.md text scored 440.9 s and 125.5 s in one run); child CPU is flat 24.2–28.8 s, so a wall-based "slowest variant" is not a variant property | `:268` |
| CT-4 | LOW | the 900 s `TOOL_TIMEOUT` is not close today (worst 441.8 s = 49 %) but is load-coupled; inner `TIMEOUT_S = 600` is 10.2× the slowest pin | `:274` |
| CT-5 | LOW | every run re-exports the same 324.7 MB / 12,237-file tree (4.08 s, ≈17 GB churn per counter run, 641 MB peak RSS/run) | `:278` |
| CT-6 | LOW | the cheapest lever is a flag (`--jobs`, default 4), measured 1.73× (3→6) and 1.53× (4→8) in simultaneous pairs, output byte-identical | `:282` |

I checked two of its load-bearing factual claims directly rather than taking them on report:

- CT-2's mechanism is present in the bytes: `.ufo/waves/round-40/conform.py:70` `LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"`, `:743` `work = tempfile.mkdtemp(prefix="mori-conform-selftest-", dir=SCRATCH_ROOT)` with `SCRATCH_ROOT = <LANE>/.ufo/waves/round-40/scratch`, `:765` `shutil.rmtree(work, ignore_errors=True)`.
- CT-2's residue claim reproduces today (§4).
- Its own artefacts survived: `.scratch/r49-Mo49ExecCounterTiming` is 1.7 GB and
  `sha256(tool-par-pins.py) = bb982819b5caf3cef61add016944f1069d6c185abdd36671ac0eb4a11eecc1ec`,
  exactly the digest the report cites (`:190`). So the report's scratch claims are true, not aspirational.

Its internal date line ("Author date 2026-10-25") cannot be corroborated from git — the only git date
available is the salvage commit's `2026-10-26 09:05:31` author date — but it is corroborated by the
file mtime `2026-10-25 23:39:03`, which is after the lane tip and before the salvage.

## 3. Does any of it change a round-49 verdict? **No.**

Round 49's recorded outcome (`MANIFEST.json` at the pinned fleet revision `e0144996…`, `rounds/723`):
`verdict: admitted`; verdicts calibration improved, depth improved, coverage/operability/freshness/
adjacency unchanged; trends expansion improved, quality unchanged, discernment improved; capabilities
`count-c1.py` (selftest 44/44 committed) and `count-flagged.py`. Its C1 recheck rests on: freeze
`sha256 -c` all OK, counter/controls unchanged since freeze, `C1=unmet junk_met=9` at the entering v3 →
`C1=met junk_met=0 variants=26` at `64c2d5fc` with tool bytes equal at tip (`697ab2cc`), the counter's
committed selftest, and an independent awk over the 27 variant lines (9 mismatches → 0).

| finding | what it touches | can it move a round-49 verdict? |
|---|---|---|
| CT-1, CT-3, CT-4, CT-5, CT-6 | cost, scheduling noise, timeout margin, re-export waste, a `--jobs` lever | No. The C1 predicate scores the 26 variants' `got=` values; the counter records no wall time, and no round-49 number is a timing. |
| CT-2 | the docstring sentence "the lane repo is only read" (`.ufo/waves/round-49/count-c1.py:40`) and the residue the closure already lists as left in place | No. Isolation is not in P-C1 and is not cited anywhere in the closure's recheck. It is a claim-accuracy defect **of the instrument's prose**, and it is the mechanism behind round-50 routed defect 4 (delete the `round-40/scratch/mori-conform-selftest-*` debris). |
| Simp 1 (`plan_ok` arm cannot fail, `count-c1.py:372-373`) | the strength of the committed `C1_SELFTEST pass=44 fail=0` receipt that the closure cites | No verdict change, but it weakens that receipt: 44/44 contains one unfalsifiable arm. The verdict survives because the closure also re-derived the result from the variant lines. This belongs in the limits list. |
| Simp 2 (`--rev HEAD` resolves a moving ref; receipts should pin the sha) | receipt hygiene | No. No round-49 receipt used `--rev HEAD`: `grep -rn -- "--rev HEAD" .ufo/waves/round-49/evidence/` → no match, rc 0. |
| Simp 3, 4 (unwritten `real-opaque` staged path; staging duplicated so the selftest only exercises the copy) | `plan_text_only`, and the reach of the selftest over the production `plan()/stage()` path | No. Simp 4 is the **same** limit round-49's own report already disclosed as (c) "the counter's selftest runs a twin of `plan()`"; it corroborates the disclosure, it does not overturn anything. Simp 3 lives only in the sniffer/selftest path. |
| Simp 5–9, 11 (dead parameters, duplicate header literal, always-`None` returns, unused seams) | dead weight in frozen counters and the witness | No. None is a predicate or a receipt. |
| Simp 10 (witness docstring says "up to three leading spaces, then `|`" while the code uses `^\s*\|`) | a control's prose vs its code | No. The code is the intent there (the widened rule is what makes N4/N7 unmet) and the hidden-row scan is not in the scored C1 predicate. The stale sentence did propagate into the landed tool: `tools/mori-pin-check.py:300` (prose) vs `:311` (`re.match(r"^\s*\|", raw)`) — still present at `HEAD`. |

Positive corroboration, not contradiction: both late reports independently re-printed the round-49
evidence lines they touched. `Mo49SimpCounters.md` §5 ran the counter with the witness tool at
`0df17b7b` and got `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26`, matching
`evidence/control-c1-tool-r48-merged-witness.txt` and the closure's disclosure (a); the
`b3e3453d` C2 run reproduced `failed=entry_absent,pins` exactly as `evidence/control-c2-donothing.txt`.
`Mo49ExecCounterTiming.md` §1 reports every one of its 27-variant runs printing the freeze receipt's
`C1=unmet junk_met=9 honest_unmet=0 real=met errors=0 variants=26`.

**Verdict impact: none** on C1, C2, either trend, the axis grades, or `admitted`. What should change is
the **limit set**, not the verdicts: round 49's C1 limits should carry "the counter's prose says the
lane is only read; the dominant pin writes into the lane, and cleanup failures leave debris" and "one
selftest arm (`plan_ok`) cannot fail"; both are additional limits on the same settled verdict.

## 4. Why CT-2 is not stale: the residue reproduces in round 50, live

The lane's `.ufo/waves/round-40/scratch/` was watched for the duration of this seat:

| time (local) | `mori-conform-selftest-*` dirs | `conform.py` processes |
|---|---|---|
| 09:47 | 0 | — |
| 09:49:46 (dir mtimes) | 8 | 5 |
| 09:51:17 | 13 | — |
| 09:51:45 | 4 | 4 |

The parents of those `conform.py` processes are not the round-50 counter:
`ps -o ppid= -p <pid>` → `/usr/bin/python3 -I -B /fast/scratch/hyaku/mori-r50/Mo50bScribeQuality/pin-check-at-64c2d5fc.py --rev 64c2d5fc… --repo /home/vgpnk/…` —
a round-50 seat re-executing the reconciler in **measurement mode**, which runs every `SKILL.md` pin
including `conform.py <rev> --selftest` (`SKILL.md:911`), and each of those writes into the lane.

Scoping, so this is not overstated: the round-50 frozen C1 counter does **not** do that itself.
`.ufo/waves/round-50/count-c1.py` runs only the two SHONEN packs (`:307`
`subprocess.run([sys.executable, path, "--selftest"], cwd=tree, env=env)`) with `TMPDIR` redirected to
its own scratch (`:305`), and both pinned tools mkdtemp under `TMPDIR`
(`tools/mori-pin-check.py:976` `mkdtemp(prefix="pin-selftest-")`,
`tools/mori-unlanded-check.py:86` `mkdtemp(prefix="unlanded-selftest-")`). So `count-c1.py:23`
("Read-only on the lane and the fleet repo") holds for the counter's own execution; the lane writes
come from measurement-mode reconciler runs — i.e. from the round-49 counter's design and from any seat
that re-executes an older counter today. The defect is inherited, not introduced by round 50, and the
dirs are transient while a run is in flight; only an interrupted run leaves orphans. I deleted nothing.

## 5. Does `Mo49SimpCounters` have output anywhere? Yes — a full report, plus its scratch; and nowhere else

| channel | result |
|---|---|
| report file | `.ufo/waves/round-49/w1/Mo49SimpCounters.md`, 339 lines / 23,158 B, tracked since `7197160b`, clean at `HEAD` |
| its scratch | `.scratch/r49-Mo49SimpCounters` = 14 MB; `a/.ufo/waves/round-49/count-c1.py` = `3c262a15…` and `a/…/count-c2.py` = `be39475d…` equal the freeze pins in `evidence/freeze-sha256.txt`; `b/…/count-c1.py` = `6dedc49c…`, `b/…/count-c2.py` = `01b3a42a…`, exactly the digests the report cites (`:250`). The report's A/B artefacts are real. |
| results json | none for round 49: `find .ufo/waves/round-49 -maxdepth 2 -name '*results*'` → empty; `ls .ufo/waves/round-49 \| grep -i result` rc 1. (Rounds 47 and 48 do have `w1-results.json`/`w2-results.json`, so this is a real absence, not a naming mismatch.) The fleet report agrees: "No `w1-results.json` / WAVE-DONE reached the L1" (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-49/mori.md:54`). |
| swarm registry | `.ufo/waves/round-49/w1/swarm-registry.json` records 49 members, **all** of the form `{"kind":"spawn","agentId":null,"role":…,"item":null}` — including the 47 seats that did report (`Mo49ExecImplA` is identical). `createdAt` = `updatedAt` = `2026-10-26T00:36:42.501Z`. The file carries the plan, not outcomes; it can answer neither "reported" nor "silent". |
| fleet state | the names occur only in `.ufo/reports/round-49/mori.md` (lines 9 and 54–58). |
| persisted agent history | `history://Mo49SimpCounters` → `Unknown agent` (round-49 seat ids are not in the persisted roster), so no transcript survives either way. |
| landed docs | `git grep -l` for both names outside the wave's own dispatch/spec/registry/report files matches exactly one file: `corpus/lessons/round-49-verifier-spotcheck.md` (D-b, line 25). Nothing in `LOG.md`, `SKILL.md`, `SCORECARD.md`, `SHONEN.md`, `corpus/knowledge/` or `tools/` cites either report, so "neither is relied on" still holds. |

## 6. Draft: one-paragraph accounting for the lesson (for the L1 to integrate; not landed by me)

```text
**Round-49 late seats (routed defect 5).** Both seats the round-49 report named as having no report at
filing were alive and late, not dead: `Mo49SimpCounters` wrote `.ufo/waves/round-49/w1/Mo49SimpCounters.md`
(339 lines, 23,158 B) at 23:02:40, six minutes after the lane tip commit `43d84666` (22:56:42), and it
entered the tree inside the orchestrator's interrupted-run snapshot `7197160b` ("not a landing"), which
is the round-50 entering tip; `Mo49ExecCounterTiming` wrote `.ufo/waves/round-49/w1/Mo49ExecCounterTiming.md`
(288 lines, 21,140 B) at 23:39:03, forty-two minutes after the tip, and stayed untracked until the
round-50 salvage `9b8562a3` committed it. The wave's report-file population therefore reads 47 at filing,
48 at `7197160b`, 49 since `9b8562a3`; the round-50 contract's parenthetical "one late report" undercounts
by one, and the report's "status unknown" was a statement about the filing instant, not about the seats.
Neither report was relied on by any verdict and neither changes one: both are instrument accounts (the
reconciler's cost profile, and dead weight in the two frozen counters), and both re-printed the same
`C1=`/`C2=` lines the round-49 receipts carry; their only verdict-adjacent content is two additional
limits on the settled C1 verdict — the counter's "the lane repo is only read" sentence is false (the
pinned `conform.py --selftest` writes `mori-conform-selftest-*` into the lane, 26× per counter run, which
is also the source of the round-40 scratch debris routed for deletion), and one selftest arm (`plan_ok`,
`count-c1.py:372-373`) cannot fail while counting toward the committed 44/44. The lesson: a wave's
report count is a snapshot of a moving population — a seat that reports after the filing cut-off must be
recorded as **late** (with its commit) rather than as missing, a wave with no results file cannot
distinguish late from dead and should say so in those words, and a seat's report arriving after the
closure is an addition to the named limits, never a revision of the verdict it does not touch.
```

If the L1 prefers to correct D-b in place, the minimal edit is to append to
`corpus/lessons/round-49-verifier-spotcheck.md:25` one sentence naming the two commits and the two
mtimes above; the report's own erratum trace (47 files) stays true and needs no change.

## 7. Evidence transcript (commands and outputs, as run)

```text
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --format='%h %ci %s' -- .ufo/waves/round-49/w1/Mo49ExecCounterTiming.md
9b8562a3 2026-10-26 09:05:33 -0300 round-50: hyaku run-8 orchestrator salvage of unlanded attempt-1 wave state and knowledge draft, plus a late round-49 seat report (…)

$ git log --format='%h a=%ai c=%ci %s' -- .ufo/waves/round-49/w1/Mo49SimpCounters.md
7197160b a=2026-10-25 23:04:10 -0300 c=2026-10-25 23:16:36 -0300 hyaku run 7 interrupted: in-flight snapshot committed by the orchestrator (not a landing); lane L1 resumes from here

$ git show --stat 7197160b | head
 .ufo/waves/round-49/w1/Mo49SimpCounters.md | 339 +++++++++++++++++++++++++++++
 1 file changed, 339 insertions(+)

$ for c in 43d84666 7197160b 9b8562a3 487941b9 HEAD; do … done
43d84666 entries=48 md=47 simp=0 ct=0
7197160b entries=49 md=48 simp=1 ct=0
9b8562a3 entries=50 md=49 simp=1 ct=1
487941b9 entries=50 md=49 simp=1 ct=1
HEAD     entries=50 md=49 simp=1 ct=1

$ stat -c '%n size=%s mtime=%y' .ufo/waves/round-49/w1/Mo49SimpCounters.md .ufo/waves/round-49/w1/Mo49ExecCounterTiming.md
Mo49SimpCounters.md      size=23158 mtime=2026-10-25 23:02:40 -0300
Mo49ExecCounterTiming.md size=21140 mtime=2026-10-25 23:39:03 -0300

$ sha256sum .ufo/waves/round-49/w1/Mo49ExecCounterTiming.md ; git show HEAD:<same> | sha256sum ; git show 9b8562a3:<same> | sha256sum
128a6fb14403789b82e6632fc32e121c56c2c302d7e907ab1ec1cf7b9a83e7e0  (identical three times)

$ git status --porcelain --ignored -- .ufo/waves/round-49/
!! .ufo/waves/round-49/__pycache__/                                   (rc 0)

$ find .ufo/waves/round-49 -maxdepth 2 -name '*results*'              (no output, rc 0)
$ find .ufo -maxdepth 3 -name '*results*' | head
/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-47/w1-results.json
/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-47/w2-results.json
/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-48/w1-results.json
/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-48/w2-results.json

$ python3 (json) .ufo/waves/round-49/w1/swarm-registry.json
schema=ufo-swarm-registry-v1 wave=mori-r49-w1-build createdAt=2026-10-26T00:36:42.501Z updatedAt=<same>
members=49 ; shapes: 16 executor, 14 scribe, 4 scout, 4 connector, 4 critic, 3 reviewer, … all {"agentId":null,"item":null,"kind":"spawn","role":…}
Mo49SimpCounters    = {"kind":"spawn","agentId":null,"role":"simplifier","item":null}   (line 278)
Mo49ExecCounterTiming = {"kind":"spawn","agentId":null,"role":"executor","item":null}   (line 284)

$ grep -rn -- "--rev HEAD" .ufo/waves/round-49/evidence/            (no match, rc 0)
$ sha256sum .scratch/r49-Mo49SimpCounters/{a,b}/.ufo/waves/round-49/count-c{1,2}.py
3c262a15… count-c1.py (a, = freeze)    6dedc49c… count-c1.py (b, = report §6)
be39475d… count-c2.py (a, = freeze)    01b3a42a… count-c2.py (b, = report §6)
$ sha256sum .scratch/r49-Mo49ExecCounterTiming/tool-par-pins.py
bb982819b5caf3cef61add016944f1069d6c185abdd36671ac0eb4a11eecc1ec   (= report §4 item 2)

$ sed -n '70p;743p;765p' .ufo/waves/round-40/conform.py
LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
    work = tempfile.mkdtemp(prefix="mori-conform-selftest-", dir=SCRATCH_ROOT)
        shutil.rmtree(work, ignore_errors=True)

$ ls -1d .ufo/waves/round-40/scratch/mori-conform-selftest-* | wc -l
0 (09:47) → 8 (09:49:46) → 13 (09:51:17) → 4 (09:51:45)
$ pgrep -af conform.py | head -3   →  parents: /fast/scratch/hyaku/mori-r50/Mo50bScribeQuality/pin-check-at-64c2d5fc.py --rev 64c2d5fc…
$ sed -n '305,307p' .ufo/waves/round-50/count-c1.py
        env = dict(os.environ, TMPDIR=os.path.join(base, "tmp"), PYTHONDONTWRITEBYTECODE="1")
            q = subprocess.run([sys.executable, path, "--selftest"], cwd=state["tree"], env=env, …
$ grep -n 'three leading spaces' tools/mori-pin-check.py ; grep -n 're.match(r"^\s*\|"' tools/mori-pin-check.py
300:    (R2) row-shaped lines (up to three leading spaces, then `|`) outside a parsed
311:        row_shaped = bool(re.match(r"^\s*\|", raw))
```

## 8. Limits of this accounting

- UNVERIFIED: whether either seat was still running at the filing instant, or whether the L1 ever saw
  the files. No process evidence survives; `history://` has no round-49 seat transcripts. The mtimes
  show only that the files were written after the tip commit.
- UNVERIFIED (not re-run): the round-49 counter's lane writes during the *round-49* scored run. I
  confirmed the mechanism statically (`conform.py:70/743/765`, the counter's measurement-mode
  `run_tool` at `count-c1.py:224`) and observed it live for round-50 re-executions (§4); I did not run
  the frozen round-49 counter (~14–32 min per run on a loaded host), and the late report's own
  measurement (`residue_dirs_before=6 after=6`) is cited, not re-derived.
- The round-49 verdicts quoted here are the fleet MANIFEST's, read at the pinned revision
  `e0144996…`; I did not re-judge the closure.
- The four `.scratch/r49-*` and 187-dir `.scratch` state is observed, not cleaned: deleting it is
  routed defect 4, owned elsewhere. No file outside this report was written or removed.
- `Mo49ExecCounterTiming.md`'s "Author date 2026-10-25" is a claim in the file; the git author date is
  the salvage's. Both are reported above so neither is mistaken for the other.

## Findings

1. **MED — the round-50 contract undercounts the late reports: both round-49 seats are committed, not
   one.** `.ufo/waves/round-50/contract.md` (routed-defect carriers, item 5) reads "the two round-49
   seats with no report are accounted (one late report is on disk and is committed as inherited)";
   `Mo49SimpCounters.md` has been tracked since `7197160b` (before the contract existed) and
   `Mo49ExecCounterTiming.md` since `9b8562a3`. Concerns `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-50/contract.md`
   (carrier 5) and `/home/vgpnk/Projects/shokunin/.ufo/reports/round-49/mori.md:9`.
2. **MED — the round-49 counter's isolation sentence is false, and its mechanism is live in round 50.**
   `.ufo/waves/round-49/count-c1.py:40` ("the lane repo is only read") vs
   `.ufo/waves/round-40/conform.py:70,743,765`; observed 0 → 13 → 4 `mori-conform-selftest-*` dirs in
   `.ufo/waves/round-40/scratch/` during this seat, parented by round-50 measurement-mode reconciler runs.
   Named limit for round-49 C1 and the mechanism behind round-50 routed defect 4; not a verdict change.
3. **MED — the report-count snapshot is being read as a mortality statement.** `.ufo/reports/round-49/mori.md:9`
   ("no report … status unknown") and `.ufo/reports/round-49/mori.md:54` ("dead-seat status is unknown")
   were true at 22:56:42 and stale by 23:02:40; `corpus/lessons/round-49-verifier-spotcheck.md:25` (D-b)
   repeats the reading. Both seats were late, not dead; the lesson draft in §6 is the correction.
4. **LOW — one arm of the committed `C1_SELFTEST pass=44 fail=0` receipt cannot fail.**
   `.ufo/waves/round-49/count-c1.py:372-373` (`plan_ok` asserts `err is None` on a function with no
   failure path), counted in `.ufo/waves/round-49/evidence/selftest-c1.txt` (line `PASS plan_ok  None`),
   which the closure cites as "counter selftest 44/44 committed". Verdict stands on the independent
   variant-line re-derivation; add to the C1 limits.
5. **LOW — the round-49 wave registry stores no per-seat outcome, so a fleet reader cannot tell a late
   seat from a dead one without listing the report directory.** `.ufo/waves/round-49/w1/swarm-registry.json:278,284`
   (and all 49 members: `agentId:null, item:null`, `createdAt == updatedAt`).
6. **LOW — the control docstring's hidden-row spec is stale and propagated into the landed tool.**
   `.ufo/waves/round-49/controls/tool-r48-merged-witness.py:253` vs `:264`, and at `HEAD`
   `tools/mori-pin-check.py:300` ("up to three leading spaces") vs `:311` (`re.match(r"^\s*\|", raw)`).
   Round-49's harness docstring finding landed with the tool; the prose was not corrected.
7. **LOW — the round-49 wave left no results file and no wave 2, so the wave's completion state is only
   reconstructible from report filenames.** `.ufo/waves/round-49/` has no `w1-results.json` (rounds 47 and
   48 do) and `.ufo/waves/round-49/w2/` is empty; the late-seat accounting above had to be rebuilt from
   `git log` per file.
