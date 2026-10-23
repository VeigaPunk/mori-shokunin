measured 2026-10-23T07:46:33Z

# ExecCloneRerun — C1 re-measured from fresh clones at the lane tip

Seat: MoriR34A3.ExecCloneRerun (leaf; no subagents, no background jobs). Assignment: re-measure C1 at
the lane tip as a closure would, using fresh clones, fresh seeds, and seed 1; confirm byte identity of
the judged tool and the counter; record every receipt line and exit code.

## 1. Provenance gates

| gate | command | result |
|---|---|---|
| expected master == fd25213 | `git rev-parse master` (lane) | **FAILED**: `5216d78dd1bc4ce57356555b509c9135a9702088` |
| fd25213 is an ancestor of master | `git merge-base --is-ancestor fd2521351c6cef47384aef30afbe1e4db7e6912e master; echo $?` | `0` |
| what master adds | `git log --oneline fd2521351c6cef47384aef30afbe1e4db7e6912e..master` | one commit `5216d78 round-34: wave B spec/dispatch (41 seats, attempt 3) before dispatch` |
| files that commit adds | `git diff --name-status fd25213..5216d78` | only `A .ufo/waves/round-34/wb-dispatch.json`, `A .../wb-run.json`, `A .../wb-spec.json` |
| tool identical ba525e1 vs fd25213 | `git diff --quiet ba525e1a0394154837eea5090e8bd27ed69c539c fd2521351c6cef47384aef30afbe1e4db7e6912e -- tools/mori-disk-rate.py; echo $?` | `exit=0` (identical) |
| tool blob at each rev | `git rev-parse <rev>:tools/mori-disk-rate.py` for ba525e1, fd25213, master | all `c7ea8bdac9c98b8d350a489fb8aca3a4750bcfbf` |
| tool sha256 | `sha256sum tools/mori-disk-rate.py`; `git cat-file blob c7ea8bd… \| sha256sum` | both `370932deb525b95135f0c30e4caaf2666b95c6feeffe76b70f06b48c09caa74b` |
| counter identical to committed copy | `git diff --quiet fd25213 -- .ufo/waves/round-34/count-c1-a1.py; echo $?` | `exit=0` |
| counter blob | `git rev-parse fd25213:.ufo/waves/round-34/count-c1-a1.py` | `6cb6c484df924202bb62c0ae266ac98ebb71740f` |
| counter sha256 | `sha256sum .ufo/waves/round-34/count-c1-a1.py`; `git cat-file blob 6cb6c48… \| sha256sum` | both `c14c3494d7356fa7c619a0e30c10cd9b71baa99eb0fb74cfd34c7f21b3b181e2` |
| tool+counter unchanged fd25213 → master | `git diff --quiet fd25213 5216d78 -- tools/mori-disk-rate.py .ufo/waves/round-34/count-c1-a1.py; echo $?` | `exit=0` |
| clones | `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-hardlinks <lane> clone{1,2,3}` | three clones, each `git rev-parse HEAD` = `5216d78…`; `git status --porcelain` empty (0 lines) |

Deviation from the assignment's stated expectation: `master` is **not** fd25213; it is fd25213 plus
one wave-B spec/dispatch commit that adds three `.ufo/waves/round-34/*.json` files. It changes neither
the judged tool nor the counter (two identity checks above). I therefore ran the three required
measurements at fd25213 and one additional closure measurement at the actual tip 5216d78.

The counter extracts the judged object from the commit, not from a working tree:
`src = subprocess.run(["git", "-C", repo, "show", f"{rev}:{TOOL}"], ...)` at
`.ufo/waves/round-34/count-c1-a1.py:393`, resolved commit verified at line 389. Its freshness,
capability drop and path hiding are at lines 219-220 (live) and 339-342 (fed live):
`mount -t tmpfs none /home && mount -t tmpfs none /fast && exec setpriv --bounding-set=-all …` inside
`unshare --user --map-root-user --mount`. `met` requires guard clean, 12/12 fixed-seed, 300/300
random, live ok, all six states and all five classes seen, `nrand == 300` (line 410). Fresh seed comes
from `os.urandom(8)` (line 404).

## 2. Receipts (verbatim, exit codes)

Run 1 — fresh seed, clone1, rev fd25213
```
START 2026-10-23T07:45:00Z run1 no-seed fresh
measured_at=2026-10-23T07:45:00Z repo=/fast/scratch/hyaku/mori-r34/a3-ExecCloneRerun/clone1 rev=fd2521351c6cef47384aef30afbe1e4db7e6912e
tool=present guard=clean seed=2434344022782873824
fixed_pass=12/12 random_pass=300/300
states_seen=['absent', 'bad-line', 'gone', 'new', 'ok', 'reset'] classes_seen=['disk', 'partition', 'stacked', 'unknown', 'virtual'] coverage=ok
live=ok
C1=met
```
`EXIT=0` (command: `timeout 600 python3 .ufo/waves/round-34/count-c1-a1.py fd25213 --repo .../clone1`, wall 11.63 s). Log: `/fast/scratch/hyaku/mori-r34/a3-ExecCloneRerun/run1.log`, sha256 `73f3dd6431e9c9691674b6a8e722d941fd3efd09dbd02918dde6377e7d1686f7`.

VERDICT: C1=met (run 1, fd25213, fresh seed 2434344022782873824, exit 0)

Run 2 — fresh seed, clone2, rev fd25213
```
START 2026-10-23T07:45:26Z run2 no-seed fresh clone2
measured_at=2026-10-23T07:45:26Z repo=/fast/scratch/hyaku/mori-r34/a3-ExecCloneRerun/clone2 rev=fd2521351c6cef47384aef30afbe1e4db7e6912e
tool=present guard=clean seed=4798878277683655959
fixed_pass=12/12 random_pass=300/300
states_seen=['absent', 'bad-line', 'gone', 'new', 'ok', 'reset'] classes_seen=['disk', 'partition', 'stacked', 'unknown', 'virtual'] coverage=ok
live=ok
C1=met
```
`EXIT=0` (wall 11.47 s). Log: `run2.log`, sha256 `b4366778077f95c5a1753bf72d173c94411d2eefd4d007aad2afcb59d0b3f336`.

VERDICT: C1=met (run 2, fd25213, fresh seed 4798878277683655959, exit 0)

Run 3 — pinned seed 1, clone3, rev fd25213
```
START 2026-10-23T07:45:41Z run3 seed=1 clone3
measured_at=2026-10-23T07:45:41Z repo=/fast/scratch/hyaku/mori-r34/a3-ExecCloneRerun/clone3 rev=fd2521351c6cef47384aef30afbe1e4db7e6912e
tool=present guard=clean seed=1
fixed_pass=12/12 random_pass=300/300
states_seen=['absent', 'bad-line', 'gone', 'new', 'ok', 'reset'] classes_seen=['disk', 'partition', 'stacked', 'unknown', 'virtual'] coverage=ok
live=ok
C1=met
```
`EXIT=0` (command includes `--seed 1`; wall 10.56 s). Log: `run3.log`, sha256 `10a5e94e0b6b5248a44a3afad04aab1dd25e586503e65cb1a5701ddd271be315`.

VERDICT: C1=met (run 3, fd25213, seed 1, exit 0)

Run 4 — additional closure check at the actual tip, fresh seed, clone1
```
START 2026-10-23T07:46:01Z run4 master-tip fresh clone1
measured_at=2026-10-23T07:46:01Z repo=/fast/scratch/hyaku/mori-r34/a3-ExecCloneRerun/clone1 rev=5216d78dd1bc4ce57356555b509c9135a9702088
tool=present guard=clean seed=5751392494430092286
fixed_pass=12/12 random_pass=300/300
states_seen=['absent', 'bad-line', 'gone', 'new', 'ok', 'reset'] classes_seen=['disk', 'partition', 'stacked', 'unknown', 'virtual'] coverage=ok
live=ok
C1=met
```
`EXIT=0` (wall 11.45 s). Log: `run4-master.log`, sha256 `537d3733fdfa10548c618f97dc9c68d6407d6d7f6645cf154a8412ed07a36108`.

VERDICT: C1=met (run 4, tip 5216d78, fresh seed 5751392494430092286, exit 0)

## 3. What the receipts establish and their limits

- Four independent executions (three at the judged rev, one at the current tip) all print `C1=met`
  with exit 0. Two unrelated 64-bit fresh seeds plus pinned seed 1 all pass; this is a genuine
  re-derivation on clones that contain only tracked lane content.
- The counter ran the judged blob, not any scratch draft: extraction is `git show <rev>:tools/...`
  (`count-c1-a1.py:393`), and that blob is byte-identical at ba525e1, fd25213 and master.
- `live=ok` means the A1 live and fed-live clauses were exercised in the same run as the oracle
  comparison; the counter builds both (lines 219-220, 339-342) and `met` requires both (line 410).
  The receipts do not print the per-device live JSON; they print only the aggregate `live=ok`.
- These runs confirm the frozen predicate on this host at this time. They do not amend contract
  R1-R7 or Amendment A1, and they do not by themselves judge the C2 calibration claim.

## 4. Findings for the integrator

1. **Tip drift (benign for C1).** `git rev-parse master` = `5216d78`, not `fd25213`. The extra commit
   adds three wave-B dispatch JSONs only; tool and counter are unchanged across the two revs
   (diff exit 0, blobs `c7ea8bd…` / `6cb6c48…`). C1 remains met at both revs.
2. **Judged tool identity is stable.** `tools/mori-disk-rate.py` is the same blob at ba525e1,
   fd25213 and master (sha256 `370932de…`), matching the frozen claim.
3. **Counter identity is stable.** The lane counter file is byte-identical to the copy committed at
   fd25213 (diff exit 0; sha256 `c14c3494…`). No uncommitted edit was measured.
4. **Fresh-seed diversity.** Run seeds `2434344022782873824` and `4798878277683655959` differ and
   both pass 300/300 with full six-state/five-class coverage; a fixed seed does not carry the result.
5. No defect in the tool or counter was observed in this move; run 3 (`--seed 1`) matching the
   fixed-seed sweep gives no sign of seed-dependent flakiness.

VERDICT: no defect found (judged tool blob `c7ea8bd…` unchanged at all three revs; counter byte-identical)

## 5. Risks and blockers

- None blocking this move. The only measured deviation is the master tip (finding 1); because the
  wave's closure may quote `fd25213` as "master", the integrator should cite the actual tip
  `5216d78` (or state fd25213 + one spec-only commit) to keep the receipt exact.
- `live=ok` is an aggregate; a closure wanting per-device live rows must read the tool's own JSON in
  a separate, explicitly-scoped run. [INFERENCE] the aggregate passed all A1 live clauses, since
  `met` gates on `lv` being `None` (line 410).
- Host disk load during runs (other seats active) could in principle perturb rate bounds; all four
  runs passed, so no evidence of such interference here.

## 6. Scratch, cleanup, tooling

- Scratch root: `/fast/scratch/hyaku/mori-r34/a3-ExecCloneRerun/` (logs `run1.log`, `run2.log`,
  `run3.log`, `run4-master.log` retained as evidence; clones deleted after the runs to release disk).
- Lane writes: this report only. Read-only git in the lane (rev-parse, log, diff, cat-file,
  merge-base, status); no git/jj writes, no index changes.
- Tooling: no installs or updates were needed or performed.
- No processes were left running; each counter invocation was capped with `timeout 600`.
