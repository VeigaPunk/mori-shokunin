# Mo60Sentinel42 — write-boundary audit (round 60, wave w1)

Seat: **Mo60Sentinel42** (sentinel). Scope: snapshot `git status --porcelain` before/after
one full run of each round-60 counter; confirm zero lane-tree writes; drive the G2
`materialize()` cases independently under scratch.

Status: **read-only audit — no production/corpus/SCORECARD/LOG/VCS edits, no commits, no
fleet or sibling writes, no remediation applied.** Only this report was written.

## Pins and environment

- Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`; tip at audit start
  `b3c256138f00c704d5aa56eb0332d74506502ef2`, tip at audit close
  `0f8340cf62b588fd64be8d9176ed7d5444c426b2` (lane moved under the wave, as the contract warns).
- Amended freeze revision `ac496c7cde8cad965079858accae3bedfe4a73f2`; entering revision
  `ddfb12fb0838b4307c445194a844f0c4b1950195`.
- Scratch `S=/fast/scratch/hyaku/mori-r60/Mo60Sentinel42` (`mkdir -p`, `TMPDIR=$S`, every run
  passed `--scratch $S/run-*`), disk guard green before work (`/fast/scratch/hyaku` 26% used,
  600 G free).
- Counter/tool bytes are identical at `ac496c7c`, `b3c25613` and `0f8340c` (all three tips):

```
$ for f in .ufo/waves/round-60/count-c{1,2,3}.py tools/mori-entry-claims-check.py tools/mori-settlement-scan.py; do
    git -C $LANE show ac496c7c:$f | sha256sum; done
795c1f3193a76406a40561ac60fedb3eee75fc38df2b2efb3fc5295d617ddbae  count-c1.py  (== count-c3 PIN_C1)
8c4814f54c564a7f00beec5249de092a2d3b2c4043e07be773d80e8e3ccdf976  count-c2.py  (== count-c3 PIN_C2)
fabde06c9d0a94a8487e5de45be3e413f6084816fb0507a71fd335bad5153514  count-c3.py
cffe9f3359097277a7ea39729309efdc5831a1738994ceb30ee023ac0eae6e69  mori-entry-claims-check.py (== PIN_EC)
4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9  mori-settlement-scan.py (== PIN_SCAN)
```

## Method

Per run, under `strace -f -y -qq -e trace=%file` (whole process tree, children included):

```
snapshot:  git -C $LANE rev-parse HEAD; git -C $LANE status --porcelain
           find $LANE \( -path $LANE/.git -o -path $LANE/.ufo/waves/round-60/w1 \
                -o -name 'w1.ready*' \) -prune -o -type f -printf '%p\t%s\t%T@\n' | sort
run:       strace -f -y -qq -e trace=%file -o $S/trace-<n>.txt \
             python3 $LANE/.ufo/waves/round-60/count-c<N>.py <PINNED-REV> \
             --repo $LANE --scratch $S/run-<n>
resolve:   python3 $S/writes.py $S/trace-<n>.txt $S <initial-cwd>
```

`writes.py` re-resolves every write-intent syscall (`open*` with `O_WRONLY|O_RDWR|O_CREAT|
O_TRUNC|O_APPEND|O_TMPFILE`, `mkdir*`, `rmdir`, `rename*`, `unlink*`, `symlink*`, `link*`,
`truncate`, `chmod*`, `utimensat`) against: per-pid cwd (initial cwd + `chdir` + clone/fork
inheritance) and `*at()` dirfd annotations (`strace -y`), and knows each call's written-path
argument (`symlink`/`link`/`rename` write the **last** path, not the first). Only `/dev/null`
is whitelisted (harness redirected the counters' own stdout/stderr into scratch).

Runs: tip `b3c25613` from a scratch cwd (**c1,c2,c3**), tip `b3c25613` from the lane-root cwd
(the contract's prescribed invocation) (**c1,c2,c3**), freeze `ac496c7c` from the lane-root cwd
(**c2,c3**), newest tip `0f8340c` (**c1**). Nine full runs.

## Verdict

| arm | result |
|---|---|
| W1 — zero lane-tree writes by the counters | **PASS** (9/9 runs; write-intent targets outside `$S` = 0) |
| G2 — `materialize()` refuses symlink-parent escapes | **PASS** (all real escape classes refused, nothing written outside the given root) |
| G1 — unpinned blob never executed (observed end-to-end) | **PASS** (new-counter scratch has no marker; old-counter control writes one, both under `$S`) |
| Frozen target outputs reproduced | **PASS** — C1 exact at `b3c25613`/`0f8340c`, C2/C3 exact at `ac496c7c` and `b3c25613` |

### Run receipts

```
c1-scratchcwd  C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=b3c25613…  rc=0
c2-scratchcwd  C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok
               claims=13 files=6 spans=13 rev=b3c25613…                                    rc=0
c3-scratchcwd  C3=met toolgate=ok containment=ok expectgate=ok cases=6 rev=b3c25613…         rc=0
c1-lanecwd     C1=met … rev=b3c25613…                                                        rc=0
c2-lanecwd     C2=met … claims=13 files=6 spans=13 rev=b3c25613…                              rc=0
c3-lanecwd     C3=met … cases=6 rev=b3c25613…                                                rc=0
c2-freeze      C2=met … claims=13 files=6 spans=13 rev=ac496c7c…                              rc=0
c3-freeze      C3=met … cases=6 rev=ac496c7c…                                                rc=0
c1-newtip      C1=met … rev=0f8340c…                                                         rc=0
```

Write-boundary resolution (unique write targets / events; lane and fleet targets = 0 in every run):

```
c1-scratchcwd  538/1029  OUTSIDE $S: 0      c2-freeze  221/517  OUTSIDE $S: 0
c2-scratchcwd  221/517   OUTSIDE $S: 0      c3-freeze  213/359  OUTSIDE $S: 0
c3-scratchcwd  213/359   OUTSIDE $S: 0      c1-newtip  (manifest IDENTICAL)
c1-lanecwd     538/1029  OUTSIDE $S: 0
c2-lanecwd     221/517   OUTSIDE $S: 0
c3-lanecwd     213/359   OUTSIDE $S: 0
```

Every write target resolves under `$S` (`run-c1*`, `run-c2*`, `run-c3*`, `g2drive`), including
the four-repository git fixtures (`$S/run-c3*/poc-{exec,expect}/.git`), the r59 receipt
re-runs (`$S/run-c1*/rr-{0,1}`), and the pinned-tool bytecode caches. No lane, fleet, `$HOME`,
`/tmp` or `/var/tmp` target.

### Manifest diffs (only two, both externally attributed)

```
$ diff before-c1-scratchcwd.txt after-c1-scratchcwd.txt
25952a25953
> $LANE/.ufo/waves/round-60/__pycache__/build-fixtures-r60.cpython-314.pyc  14982  1793204154.9783245560

$ diff before-c2-lanecwd.txt after-c2-lanecwd.txt
8d7   < ?? EXEC-MARKER
486d484 < $LANE/EXEC-MARKER  92  1793204188.2268889460
```

Both are foreign-seat writes: the counters' own strace shows **no** write-intent on either path
(`grep -c 'EXEC-MARKER' trace-c2-lanecwd.txt → 0`; `python3 writes.py trace-c1-scratchcwd.txt
$S → lane_targets 0`), and Python does not cache a directly-executed script (`count-c1.py` was
the whole process tree). See F1/F6.

### E2 — G2 `materialize()` driven independently (frozen bytes, sha-pinned)

Loaded `git show ac496c7c:.ufo/waves/round-60/count-c2.py` (sha re-checked =
`8c4814f5…df976`), then attacked the writer from `g2drive.py`:

```
rel ../escape.txt:                 ret=False
rel a/../../../escape2:            ret=False
abs outside path:                  ret=False
inside/f.txt:                      ret=True
inside/../inside2/f:               ret=True
abs inside path:                   ret=True
symlink-parent escape (ln -> existing outside dir):  ret=False
nested symlink escape (nest/ln2 -> outside):         ret=False
symlink-file overwrite (filelink -> outside/keep):   ret=False   (keep.txt unchanged)
dangling symlink parent:                             ret=False
symlink to inside dir:                               ret=False   (conservative)
root-as-symlink write:                               ret=False   (see F4)
target is a directory:             ret=EXC IsADirectoryError      (see F3)
parent is a regular file:          ret=EXC FileExistsError       (see F3)
empty rel:                         ret=EXC IsADirectoryError      (see F3)

[containment verdicts] parent_walk True deep_walk True absolute True inside True
walk_inside True abs_inside True symlink_parent True symlink_nested True
symlink_file True symlink_dangling True symlink_inside True root_symlink False
```

`g2drive/outside-target/` after the drive: only `keep.txt` (10 B, unchanged); no
`escape*.txt`/`pwn*.txt` anywhere under `/fast/scratch/hyaku` (searched depth 3). The
`..` and absolute refusals come from the resolved-path check (`count-c2.py:114-130`), the
symlink refusals from the ancestor walk (`:118-121`); the write itself is `:137-141`.

Hostile-tree-to-symlink vector is closed: a git tree cannot carry a live symlink here —
`git show HEAD:link` for a committed mode-120000 entry returns the target *text*, and
`materialize()` writes a regular file:

```
$ git ls-tree HEAD link        → 120000 blob 7c7eea6…  link
$ git show HEAD:link | xxd     → 6f7574736964652d746172676574  ("outside-target")
materialize ret=True islink=False mode=0o644 bytes=b'outside-target'
```

Mutation check on **count-c3's own** G2 arm (`count-c3.py:202-227`), symlink guard deleted from
`contained()`: `"../escape.txt": false`, `"inside/f.txt": true`, `"ln-after-link":
"EXC:FileExistsError"` → the counter's expression evaluates **False** only because the mutant
raises; there is no false `containment=ok`, but the arm fails via traceback, not verdict. See F2.

### G1 observed end-to-end (from c3 runs, under scratch)

```
new counter : newfstatat($S/run-c3/g1-new/EXEC-MARKER) = -1 ENOENT   (stat only, never created)
old control : openat($S/run-c3/g1-old/st2/EXEC-MARKER, O_WRONLY|O_CREAT|O_TRUNC) = 3
```

## Findings

### F1 — lane-root `EXEC-MARKER` written mid-wave by a concurrent seat (Medium, environment)
Exploit path: a seat runs the G1 old-counter PoC (or the r59 count-c2 it wraps) with cwd = the
lane root and without `--scratch`; the unpinned fixture blob writes `EXEC-MARKER` into `.`.
Evidence: the marker (92 B, mtime `1793204188.226` = 13:16:28.226) appears in
`before/after-c1-lanecwd` (13:17:05.77 / 13:17:07.76) and `before-c2-lanecwd` (13:17:07.96) and
is gone in `after-c2-lanecwd` (13:17:09.37); none of the nine counter traces references it
(`grep -c EXEC-MARKER`: c1/c2 runs 0; the four c3 hits are all under `$S/run-c3*/g1-*`), and
no trace has any lane write target. Same-second scratch artifact:
`/fast/scratch/hyaku/mori-r60/Mo60Executor58/full-old/st2/EXEC-MARKER`, 86 B, 13:16:28.192
(34 ms earlier); at the same moment 10 scratch roots in this wave (nine peer seats plus
`L1-build`) held 34 `g1-old/*/EXEC-MARKER` artifacts of the same class.
Impact: the contract's read-only-lane rule was violated transiently by a seat; a status-only
zero-write claim taken in that window would be false, and an unattributed marker could be
misread as a counter leak. Smallest remediation (owner: L1): require PoC drivers to run with
cwd inside the seat scratch and `--scratch` set; at wave close run
`find $LANE -name EXEC-MARKER` (currently 0) before freezing receipts.

### F2 — count-c3's symlink G2 case cannot demonstrate an escape (Low, control quality)
`count-c3.py:215-219` links `g2/ln -> "nowhere"` (dangling) and asserts
`not (g2/"nowhere"/"f.txt").exists()` — a path that can never exist, so that conjunct is
vacuous; `r3 is False` is equally satisfied by a containment refusal and by a failed write.
When the guard is removed, `materialize` raises `FileExistsError` (measured), i.e. the arm
aborts instead of reporting `containment=bad`; a regression that also wrapped writes in
`try/except: return False` would read `containment=ok` while never testing an escape.
Impact: the G2 arm's falsifiability rests on the `..` case only; the symlink half is
tautological. Smallest remediation (not applied): point `ln` at an existing directory outside
`g2` (as in my `symlink_parent` case) and assert the outside target stays absent; keep one
dangling case for the crash path, plus a symlink-file case.

### F3 — `materialize()` raises uncaught exceptions on non-regular targets (Low, robustness)
`count-c2.py:132-141` does `t.parent.mkdir(parents=True, exist_ok=True); t.write_bytes(blob)`
with no `OSError` handling: target-is-a-directory → `IsADirectoryError`; parent-is-a-regular-file
→ `FileExistsError`; empty `rel` → `IsADirectoryError` (all measured). Not reachable from
git-sourced materialization — git forbids a blob and a subtree with the same name and symlink
entries materialize as regular files (verified above) — so no counter path is currently
affected; it is a tripwire for future callers with a caller-supplied `rel`.
Smallest remediation (not applied): return `False` on `OSError`, or reject `rel` when empty or
when the target exists and is not a regular file.

### F4 — containment refuses a symlinked *root* argument (Info, behavior)
`contained()` tests `cur.is_symlink()` before the `cur == root` break (`count-c2.py:118-121`),
so passing a symlink as the materialize root refuses every write (`root-as-symlink` case:
`ret=False`). The counters always pass a freshly created real dir (`scratch/{root,trees/*,
real,drift}`), so no impact this round; note for future callers so a symlinked scratch subtree
is not mistaken for an escape.

### F5 — C1 receipts arm inherits r59 absolute defaults and pre-G1 execution semantics (Low)
`count-c1.py:121-137` executes the r59 counters from bytes pinned at `R59_DATA` (immutable, so
no injection surface) but passes only `<rev> --repo <lane> --scratch <dir>`; the executed r59
bytes carry absolute host defaults — `git show 7b86704d:.ufo/waves/round-59/count-c1.py:246-247`
(`repo = "/home/vgpnk/…/mori-shokunin"`, `fleet = "/home/vgpnk/Projects/shokunin"`) and
`…/count-c2.py:437` (same `repo`) — and neither r59 counter sha-gates its tool before executing
it (`r59 count-c1.py:104-117`, `r59 count-c2.py:203-212`: `tp.write_bytes(tool_b)` then run).
Measured: receipts=2/2 on this host, and the r59 re-runs write only under `$S/run-c1*/rr-*`.
Impact: C1's receipts claim is not location-independent — without the fleet repo at that exact
path (and `MANIFEST_REV`) the re-run cannot reproduce — and the executed instruments keep the
pre-G1 pattern (safe only because git objects are immutable). Smallest remediation (not
applied): pass an explicit `--fleet`/parent of `--repo` from count-c1, or record the dependency
in the predicate.

### F6 — lane `__pycache__` (4 files) written by a concurrent seat; invisible to `git status` (Info/low hygiene)
`$LANE/.ufo/waves/round-60/__pycache__/{build-fixtures-r60,count-c1,count-c2,count-c3}.*.pyc`
appeared at 13:15:54.978 (during my first run window) from a seat that imported the four lane
modules; zero counter trace references. It does not appear in `git status` because
`.gitignore:3:__pycache__/`. Impact: `git status --porcelain` alone is insufficient evidence for
"zero lane-tree writes" (my `%p\t%s\t%T@` manifest is what caught it), and importing frozen
counters straight from the lane mutates the lane. Smallest remediation (owner: seats/L1):
materialize imports from a scratch copy (count-c3 already does exactly this at `:204-211`) and
remove lane `__pycache__` before close.

## Notes, limits, non-findings

- Pin discipline works under a moving tip: `corpus/lessons/round-60.md` was transiently
  `MM` (staged + unstaged edit) in the lane working tree mid-audit (observed 13:20; already
  gone by the 13:23 final check, tip unchanged at `0f8340c`), yet C1 stayed `lesson=ok` at
  `b3c25613` and `0f8340c` because the counter reads it with `git show R:path`. A working-tree
  read would have been poisoned; none was observed.
- Limit of the write audit: writes through already-open inherited fds are not path writes (the
  harness redirected the counters' stdout/stderr into `$S`); `strace` was not started
  privileged, so no kernel-module or mmap-only writes are observable — none of the counters
  uses either (sources read in full).
- `run_pinned`/tool bytes are written only after a sha match; `run_pinned` uses `python3` from
  PATH (`count-c2.py:149`, `count-c3.py:124`), which is host-trusted, not repo-supplied.
- C3 evidence claims and the frozen target lines match my independent outputs verbatim (with
  `rev=R` substituted) for C1/C2/C3 at the named revisions; nothing in this audit contradicts
  C2=met / C3=met at `ac496c7c`.
- No tool installs or updates were needed; pacman was not run; no fixture lived outside `$S`;
  all fixture git commands used `git -C <scratch path>` and were `init`-ed under `$S`.
- Scratch `/fast/scratch/hyaku/mori-r60/Mo60Sentinel42` (traces ~17 MB, manifests ~56 MB) was
  used only for this seat and has been removed after this report was written.
