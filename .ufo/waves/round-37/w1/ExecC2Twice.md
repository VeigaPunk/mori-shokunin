# ExecC2Twice — is the round-37 C2 counter deterministic across repeated runs?

**Item attacked.** Determinism / idempotence of the C2 freshness counter
`.ufo/waves/round-37/count-c2.py` at the scored tip
`e57c58b57c025364e79d130fbdf764d2674d83d6`: does running it twice produce
byte-identical output and identical exit codes, i.e. is the C2 measurement a
stable function of the revision under test rather than of ambient state
(HEAD drift, wall clock, cwd, `TMPDIR`, concurrent runs, leftover scratch)?

Scored tip under test: `e57c58b57c025364e79d130fbdf764d2674d83d6` (pushed).
Entering tip (not under test here): `842a32074b5c7972e9728f3f629d83eb92f127c2`.
No lane byte was modified. No tool installs were made. No `pacman`
invocation. Scratch root: `/fast/scratch/hyaku/mori-r37/ExecC2Twice/`.

## Axes named (godspeed)

1. **Byte-determinism** — two consecutive runs, same bytes?
2. **Exit-code stability** — same exit code on both runs, and on repeats?
3. **Idempotence** — no state drift between runs (HEAD moved during the
   window; the counter must not depend on it).
4. **Ambient independence** — cwd, `TMPDIR`, `TZ`/locale must not move the output.
5. **Concurrency safety** — two counters in flight simultaneously must not
   interfere (shared scratch, shared port, shared temp files).
6. **Scratch hygiene** — the counter's own `mkdtemp` work dir must be removed;
   no residue in the lane repo or `/tmp`.
7. **Discrimination sanity** — the counter must still be *sensitive* (not a
   constant printer): a bogus rev and the entering tip must fail, otherwise
   "deterministic" would be trivially true of a stub.

## 1. Primary assignment measurement (exact target command)

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && \
  python3 .ufo/waves/round-37/count-c2.py e57c58b57c025364e79d130fbdf764d2674d83d6 \
    > /fast/scratch/hyaku/mori-r37/ExecC2Twice/a.txt 2>&1; echo $?
EXIT_A=0

$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && \
  python3 .ufo/waves/round-37/count-c2.py e57c58b57c025364e79d130fbdf764d2674d83d6 \
    > /fast/scratch/hyaku/mori-r37/ExecC2Twice/b.txt 2>&1; echo $?
EXIT_B=0

$ diff a.txt b.txt
DIFF_EXIT=0
```

Final re-run of the same pair (later in the window, after lane `HEAD` had
moved) reproduced it exactly:

```
EXIT_A_FINAL=0
EXIT_B_FINAL=0
DIFF_EXIT_FINAL=0
7d278eb95c6d3201e58a86b7acdb2d20596eb9f58041d975f68dcfa9a5ebaa4d  a.txt
7d278eb95c6d3201e58a86b7acdb2d20596eb9f58041d975f68dcfa9a5ebaa4d  b.txt
```

`diff.txt` (the `a.txt` vs `b.txt` diff artifact) is **0 bytes** — the diff is
empty, not merely "no differences printed".

**Both exit codes are 0. The diff is empty.** Acceptance criterion satisfied.

Retained evidence — full stdout of run `a` (identical to `b`):

```
P-C2: at revision R, tools/mori-source-drift.py passes its selftest with the named arms `huge_cap` and `redirect_private_refused`, each of those arms fails in a copy with its policy removed (4 MiB read cap; post-redirect public-destination policy), and the committed corpus binds the hardening (knowledge entry citing this round's source rows and commit 8ff9bba, a SCORECARD capability row, two README coverage-map rows) with the round's live sweep receipt present.
check tool_present   PASS (path=tools/mori-source-drift.py)
check selftest       PASS (exit=0 arms=[('exit_code', 'PASS'), ('huge_cap', 'PASS'), ('missing_sources_exit2', 'PASS'), ('redirect_private_refused', 'PASS'), ('row_states', 'PASS'), ('summary', 'PASS')])
check cap_kill       PASS (exit=1 huge_cap=FAIL)
check redirect_kill  PASS (exit=1 redirect_private_refused=FAIL)
check knowledge      PASS (present=True rows=['S205', 'S221', 'S222', 'S223', 'S224', 'S225'] cited_commit=True)
check capability     PASS (rows=1 names_tool=True)
check readme         PASS (r36_row=True r37_row=True)
check live           PASS (present=True sentence=True)
C2=met
```

## 2. Repeat-run battery (19 invocations, all exit 0, all one hash)

| # | variant | exit | output |
|---|---|---|---|
| 1 | `a.txt` (target run 1) | 0 | `7d278eb9…5ebaa4d` |
| 2 | `b.txt` (target run 2) | 0 | `7d278eb9…5ebaa4d` |
| 3 | `c.txt` (third, timed) | 0 | `7d278eb9…5ebaa4d` |
| 4 | `d.txt` (private `TMPDIR`) | 0 | `7d278eb9…5ebaa4d` |
| 5 | `e.txt` | 0 | `7d278eb9…5ebaa4d` |
| 6 | `f.txt` | 0 | `7d278eb9…5ebaa4d` |
| 7 | `g_cwd.txt` (run from `cwd=/tmp`) | 0 | `7d278eb9…5ebaa4d` |
| 8–9 | `par1.txt`, `par2.txt` (two counters concurrently) | 0, 0 | `7d278eb9…5ebaa4d` |
| 10–14 | `rep1.txt` … `rep5.txt` (5× serial repeat) | 0 ×5 | `7d278eb9…5ebaa4d` |
| 15–18 | `priv1.txt` … `priv4.txt` (4× private `TMPDIR`) | 0 ×4 | `7d278eb9…5ebaa4d` |
| 19 | `tz.txt` (`TZ=Asia/Tokyo LANG=C.UTF-8`) | 0 | `7d278eb9…5ebaa4d` |

Machine check over the 18 files hashed together:

```
$ sha256sum a.txt b.txt c.txt d.txt e.txt f.txt g_cwd.txt par1.txt par2.txt rep*.txt priv*.txt | awk '{print $1}' | sort | uniq -c
     18 7d278eb95c6d3201e58a86b7acdb2d20596eb9f58041d975f68dcfa9a5ebaa4d
```

`tz.txt` was checked separately against `a.txt` → `A_EQ_TZ=YES`. So **19/19
runs: exit 0, byte-identical stdout+stderr**.

## 3. Axis-by-axis findings

**Byte-determinism / exit-code stability.** PASS. 19/19 identical bytes, all
exit 0. The output embeds no wall-clock, no elapsed-time, no PID, no temp
path, no port, no hostname:

```
$ grep -lEi 'elapsed|[0-9]{2}:[0-9]{2}:[0-9]{2}|seconds|/tmp/' <all 18 outputs>
(no matches)
```

**Idempotence under HEAD drift.** PASS. Lane `HEAD` moved during my window
(`git rev-parse HEAD` → `1ae1d6d69282f6c4f51355308db6a4be9a8e3d42`), yet runs
before and after the move produced the same hash. This is expected by
construction: `show()` at `count-c2.py:100-113` reads *committed bytes* via
`git -C <repo> show <rev>:<path>` and `git cat-file -e`, never the worktree —
so the measurement is a pure function of the requested revision.

**Ambient independence.**
- cwd: run from `/tmp` → `A_EQ_G=YES`, exit 0 (`--repo` defaults to the
  absolute `DEFAULT_REPO`, `count-c2.py:42`, `:141`, `:145`; no cwd-relative
  path is opened — the only `open(...,"w")` calls at `:157`, `:167`, `:174`
  target paths inside the `mkdtemp` work dir).
- `TMPDIR`: 5 runs under private `TMPDIR`s → same hash, exit 0.
- `TZ`/locale: `TZ=Asia/Tokyo LANG=C.UTF-8` → same hash, exit 0.

**Concurrency safety.** PASS. Two counters launched simultaneously
(`par1`/`par2`), both exit 0, outputs identical to each other and to `a.txt`
(`PAR_EQ=YES`, `A_EQ_P1=YES`). The probe's HTTP server binds
`("127.0.0.1", 0)` (`tools/mori-source-drift.py:291`) — ephemeral port, no
fixed-port collision.

**Scratch hygiene.** PASS with one caveat noted below.
- The counter's own work dir is `tempfile.mkdtemp(prefix="mori-c2-r37-")`
  (`count-c2.py:153`) and is removed in a `finally: shutil.rmtree(work,
  ignore_errors=True)` (`:184-185`). Confirmed: 4 private-`TMPDIR` runs left
  **0** entries in their `TMPDIR` (`leftover=0` each).
- Default-`TMPDIR` leak test with before/after snapshots:
  `before=0 after=0`, `LEAK_DIFF_EXIT=0` — no new `/tmp/mori-c2-r37-*` left.
- Caveat (not a defect of this item, and not attributable to the C2 counter's
  logic): `/tmp/mori-c2-r37-*` directories *do* appear transiently while a run
  is in flight — I observed 2–7 of them mid-window, and they vanish once the
  owning process exits (`/tmp/mori-c2-r37-iv_0pr4c` present at 17:11:37, gone
  by 17:12:50; count reached 0 again). Concurrent peer agents in this wave
  were running the same counter, so those dirs were other runs' in-flight
  work dirs, and the `finally` block removed them. No stale dir survived.
- Lane repo: no tracked file modified by the counter.
  `git status --porcelain --untracked-files=no` → only
  `M .ufo/waves/round-37/w1/MutC2CapArm.md`, which is a *peer mutation
  agent's* report file, not produced by the counter and not mine. The
  counter writes nothing into the repo (all writes are under the `mkdtemp`
  dir).

**Discrimination sanity (the counter is not a constant printer).** PASS.
- Bogus rev `0000…0000`: `EXIT_BOGUS=1`, `C2=unmet`, every check FAIL
  (`tool_present FAIL`, `selftest FAIL (tool absent)`, `knowledge FAIL
  (present=False rows=[] cited_commit=False)`, …).
- Entering tip `842a32074b5c7972e9728f3f629d83eb92f127c2`: `EXIT_ENTERING=1`,
  `C2=unmet` — and it discriminates *partially*, not all-or-nothing:
  `tool_present PASS`, `selftest FAIL (exit=0 arms=[('exit_code','PASS'),
  ('missing_sources_exit2','PASS'), ('row_states','PASS'), ('summary','PASS')])`
  i.e. the `huge_cap` and `redirect_private_refused` arms are absent at the
  entering tip, `cap_kill`/`redirect_kill` FAIL, and `knowledge`/`capability`/
  `readme`/`live` FAIL. So the C2 signal is genuinely tied to the round-37
  hardening landing, and the tip-scoped measurement is not a rubber stamp.

**Runtime.** Each run takes ~13.7–15.7 s wall (`real 0m13.716s` measured;
`user 4m20s` — the counter's selftest arms fan out threads/servers). Well
inside the script's own `PROBE_BUDGET_S = 180` / `PROBE_GRACE_S = 5`
(`count-c2.py:39-40`).

## Risks / notes

- **Not a defect, but worth flagging upstream:** `count-c2.py:40` imports
  `tempfile` and `:153` uses `tempfile.mkdtemp(prefix="mori-c2-r37-")` — a
  *global* `/tmp` path, not repo-relative or under the wave scratch. Under
  high concurrency (this wave had ≥7 sibling agents running the same
  counter) that produces a visible, if transient, spread of `/tmp` work dirs.
  The `finally` block cleans them, so it is cosmetic, but it is the same
  class of issue as the routed r36 debt (g) "mkdtemp scratch". I did **not**
  change the lane file (lane is read-only for this seat, and the item is
  detection-only).
- The counter reads `LIVE_REL` (`.ufo/waves/round-37/evidence/drift-live-r37.txt`)
  as *committed bytes at the rev* (`show()`), so the `live` check is
  rev-scoped and does not read the live worktree file — consistent with the
  deterministic result.
- Environment note: `git rev-parse HEAD` reported `1ae1d6d6…` during my
  window while the scored tip is `e57c58b5…`; this is expected because the
  counter is invoked with an explicit rev and never consults `HEAD`.
- No packages were installed or upgraded for this item (the assignment needed
  only `python3`, `git`, `diff`, `sha256sum`, all pre-present); nothing to
  record under the tooling directive.

## Verdict

Both runs exited **0**; `diff a.txt b.txt` produced **no output** (diff
artifact 0 bytes, `diff` exit 0); the two files hash identically
(`7d278eb9…5ebaa4d`). Extended battery: 19/19 runs exit 0 with byte-identical
output, stable under HEAD drift, cwd change, `TMPDIR` change, `TZ`/locale
change, and concurrent execution; no scratch leak, no lane mutation; and the
counter still discriminates (exit 1 at the bogus rev and at the entering tip).
The C2 counter is deterministic and idempotent at
`e57c58b57c025364e79d130fbdf764d2674d83d6`.

VERDICT: PASS
