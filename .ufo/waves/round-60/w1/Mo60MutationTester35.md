# Mo60MutationTester35 — selftest consistency: all four `--selftest` gates, TMPDIR set vs unset

Seat: Mo60MutationTester35 (leaf, read-only over the lane; no subagent dispatch).
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Freeze/amended freeze `ac496c7cde8cad965079858accae3bedfe4a73f2`; entering
`ddfb12fb0838b4307c445194a844f0c4b1950195`; lane tip observed during the seat
`b3c256138f00c704d5aa56eb0332d74506502ef2` (C1 data landing, as the contract warned).
All work in scratch `/fast/scratch/hyaku/mori-r60/Mo60MutationTester35`; no lane, VCS,
fleet, HOME or PATH writes. Tool installs: none. Disk guard read before and after:
`scripts/hyaku/disk-guard.sh status` exit 0, `/fast` 27% used / 595 G free.

**Result: pass counts identical in both arms (6/8/3/13), all exit 0, stderr empty,
deterministic and cwd-independent; zero persistent strays, zero writes outside scratch
in arm A, zero anywhere outside the system temp dir in arm B. One documentation/
semantics defect found: `--scratch` is inert on every one of the four selftests, so
selftest write containment is TMPDIR-only.**

## Frozen bytes under test (pinned, verified at three points)

| object | `ac496c7c` (freeze) | tip `b3c2561` | working tree | expected pin |
|---|---|---|---|---|
| `.ufo/waves/round-60/count-c1.py` | `795c1f3193a76406…617ddbae` | same | same | `795c1f31…ddbae` (count-c3 `PIN_C1`) ✔ |
| `.ufo/waves/round-60/count-c2.py` | `8c4814f54c564a7f…e8e3ccdf976` | same | same | `8c4814f5…df976` (count-c3 `PIN_C2`) ✔ |
| `.ufo/waves/round-60/count-c3.py` | `fabde06c9d0a94a8…d5153514` | same | same | — (instrument, sha recorded here) |
| `tools/mori-entry-claims-check.py` | `cffe9f3359097277a7ea39729309efdc5831a1738994ceb30ee023ac0eae6e69` | same | same | `cffe9f33…e6e69` (`PIN_EC`, contract C2) ✔ |

`git log ac496c7c..b3c2561 -- <those five paths>` → empty: the C1 data-landing commits
(`398d3225`, `b3c2561`) did not touch any instrument. Every measurement below is therefore
pinned equally to `ac496c7c` and to the observed tip.

## Method

- Oracle = the lane's own bytes, executed in place (`python3 <lane>/<path> --selftest`).
  No copies for the consistency matrix; copies only for the mutant arms (F4/F5).
- **Arm A**: `TMPDIR=<scratch>/tmpdir-a` exported; cwd = lane root; four selftests run
  5× each (20 runs); the tool additionally run with `--selftest --scratch <scratch>/explicit-scratch`.
- **Arm B**: `env -u TMPDIR`; cwd = `/` (not the lane, to test cwd independence);
  3× each (12 runs); tool additionally run with `--selftest --scratch <scratch>/tmpdir-b-explicit`.
- Write containment measured two independent ways:
  1. `strace -f -e trace=openat,open,creat,mkdir,mkdirat,unlink,unlinkat,rename,
     renameat,renameat2,symlink,symlinkat` on all 8 instrument×arm combinations, plus a
     catch-all `-e trace=%file` pass on the two writing instruments in both arms;
     write-class = `O_WRONLY|O_RDWR|O_APPEND|O_CREAT|O_TMPFILE`, `mkdir*`, `symlink*`,
     `unlink*`, `rename*`.
  2. Filesystem snapshots: `ls -1 /tmp` before/after arm B (3496 entries → 3496),
     `find /tmp -maxdepth 1 -newer <marker>`, and an existence re-check of every traced
     write target after the runs.

## Result matrix

| instrument | expected token (contract) | arm A (TMPDIR=scratch) | arm B (TMPDIR unset) | identical |
|---|---|---|---|---|
| `count-c1.py --selftest` | `C1_SELFTEST pass=6 fail=0`, exit 0 (contract:66) | `C1_SELFTEST pass=6 fail=0` rc 0 | same, rc 0 | **IDENTICAL** (md5 `3954be39…`) |
| `count-c2.py --selftest` | `C2_SELFTEST pass=8 fail=0`, exit 0 (contract:96) | `C2_SELFTEST pass=8 fail=0` rc 0 | same, rc 0 | **IDENTICAL** (md5 `1de85a24…`) |
| `count-c3.py --selftest` | `C3_SELFTEST pass=3 fail=0`, exit 0 (contract:121) | `C3_SELFTEST pass=3 fail=0` rc 0 | same, rc 0 | **IDENTICAL** (md5 `b517f4a4…`) |
| `tools/mori-entry-claims-check.py --selftest` | `ENTRYCLAIMS_SELFTEST pass=13 fail=0`, exit 0 (contract:96-97) | `ENTRYCLAIMS_SELFTEST pass=13 fail=0` rc 0 | same, rc 0 | **IDENTICAL** (md5 `12cf5ae2…`) |

- stderr byte count across all 10 first-pass runs: **0**. Pass counts never varied over
  20 (arm A) + 12 (arm B) repeated runs; cwd was the lane root in arm A and `/` in arm B
  with no effect.
- Static `chk(` call counts inside each `selftest()` (6 / 8 / 3 / 13) equal the observed
  pass counts exactly ⇒ every statically present check executed and passed; no check was
  skipped and no count was inflated.

## Write containment (measured)

| arm | distinct write targets | under scratch | under `/tmp` | elsewhere (lane / HOME / `/var/tmp` / cwd) |
|---|---|---|---|---|
| A (TMPDIR = scratch) | 12 | **12** | 0 | **0** |
| B (TMPDIR unset) | 14 | 0 | **14** | **0** |

- Write-free selftests: `count-c1.py` and `count-c3.py` issue **0** write-class syscalls
  in both arms (`A_c1=0, A_c3=0, B_c1=0, B_c3=0`) — pure in-memory predicates, zero TMPDIR
  sensitivity. Only `count-c2.py` and the tool's selftest write (their `mkdtemp` sandboxes).
- Arm A targets (all under `tmpdir-a/`; `mkdtemp` roots `mori-r60-c2st-*`, `mori-r60-ecst-*`
  and their `in/`, `in/f.txt`, `ln` symlink, `corpus/…`, `e.md`, `c1.json`, `c2.json`).
- Arm B targets, all transient and all gone afterwards:
  `/tmp/mori-r60-c2st-n9hpqb0i{,/in,/in/f.txt}`, `/tmp/mori-r60-ecst-0gcukrfa/{,corpus,
  corpus/evidence,corpus/evidence/{c1,c2}.json,corpus/knowledge,corpus/knowledge/e.md,
  corpus/SOURCES.md}`, plus the two `tempfile` writability probes `/tmp/ywzui86a`,
  `/tmp/p2k8_q2x` (created then `unlink`ed by `tempfile._get_default_tempdir`).
- **Stray dirs: none.** `ls -d /tmp/mori-r60-*` → none; every traced write target tested
  with `[ -e ]` after the runs → none present; arm-A scratch (`tmpdir-a`) left with 0
  entries (both `shutil.rmtree(base)` finally-blocks fired); `/tmp` entry-count delta over
  the whole arm-B sequence: 0 (identical `ls -1` before/after).
- No `.pyc`/`__pycache__` writes anywhere: all `pycache` hits in the traces are
  `O_RDONLY` reads of `/usr/lib/python3.14/…`; the lane's pre-existing
  `tools/__pycache__` keeps its `Oct 28 12:24` mtime. No lane path (`/home/...`) appears
  among any write-class syscall.

## Findings (detection only; no claim or contract change proposed)

- **F1 — `--scratch` is inert on all four selftests; containment is TMPDIR-only.**
  - `count-c1.py:277`, `count-c2.py:453`, `count-c3.py:279` dispatch to `selftest()` on
    `if "--selftest" in argv` *before* any option parsing, so a trailing `--scratch DIR`
    is silently ignored (`count-c1.py:25` even advertises `--selftest` in its usage block
    directly under `<rev> [--repo DIR] [--scratch DIR]`).
  - `tools/mori-entry-claims-check.py:242` declares `def selftest(scratch=None)` but never
    reads `scratch`; `:253` builds `base = mkdtemp(dir=os.environ.get("TMPDIR") or None)`.
    `main()` at `:442-447` dutifully parses `--scratch` and passes it into the dead
    parameter, while the docstring at `:34-37` advertises
    `mori-entry-claims-check.py --selftest [--scratch DIR]` and promises "writes only
    inside its own selftest scratch".
  - Empirical: `--selftest --scratch <path>` never creates `<path>` for any of the four
    (`scratch_created=no` ×3 counters, `explicit2_created=no` for the tool); `strace`
    shows the sandboxes landing under TMPDIR instead. Consequence: an operator who pins
    the selftest with `--scratch` instead of exporting `TMPDIR` gets arm-B behaviour
    (writes in `/tmp`).
- **F2 — with TMPDIR unset the selftests write outside the explicit scratch** (14
  transient targets under `/tmp`, listed above), fully cleaned up. This is correct
  `tempfile` behaviour, not a leak; it only matters because F1 removes the flag-based
  way to prevent it.
- **F3 — asymmetric fragility on a broken TMPDIR.** `TMPDIR=<nonexistent>`:
  `count-c2.py` and the tool exit **1** with `FileNotFoundError: … /does-not-exist/mori-r60-c2st-*`
  / `…mori-r60-ecst-*` on stderr and **no summary line on stdout at all**; `count-c1.py`
  and `count-c3.py` still print their normal lines and exit 0 (they never touch the FS).
  No fallback to `/tmp` occurs (good for containment; a harness that greps the summary
  token sees an empty string rather than a pass/fail line).
- **F4 — exit 0 discriminates (not vacuous).** Four single-substitution mutants of
  scratch copies each flip exactly one check:
  `count-c1` `dead_uncorrected(...)==1 → ==2` → `C1_SELFTEST pass=5 fail=1` rc 1;
  `count-c2` `len(FROZEN_EXPECTS)==13 → ==12` → `pass=7 fail=1` rc 1;
  `count-c3` `len(PIN_C1)==64 → ==65` → `pass=2 fail=1` rc 1;
  tool `reasons == [] → reasons != []` → `ENTRYCLAIMS_SELFTEST pass=12 fail=1` rc 1
  (each with the matching `FAIL <name>` on stderr).
- **F5 — a dropped check survives the instrument's own exit code; only the exact
  pass-count token kills it.** Deleting one `chk(...)` from a pristine copy yields
  `C3_SELFTEST pass=2 fail=0` rc 0 (`d-c3.py`) and `ENTRYCLAIMS_SELFTEST pass=12 fail=0`
  rc 0 (`d-ec.py`). The tool is covered inside count-c2 by the literal token
  `EXPECT_SELFTEST = "ENTRYCLAIMS_SELFTEST pass=13 fail=0"` (`count-c2.py:55`, used at
  `:187`); `C1_SELFTEST pass=6` and `C3_SELFTEST pass=3` are pinned only by the frozen
  contract text (contract:66, :121), and those counters' bytes are SHA-pinned by
  count-c3 (`PIN_C1`/`PIN_C2`), so a dropped check is reachable only through a byte
  change that the pins already forbid. Recorded as coverage, not as a hole.
- **F6 — the counters' selftest *arm* is TMPDIR-contained even though its `--scratch`
  argument is decorative.** `count-c2.py:184-187` invokes the pinned tool as
  `--selftest --scratch <scratch>/st`, which creates no `st` directory; the containment
  actually comes from `run_pinned`'s `env={**os.environ, "TMPDIR": str(scratch)}`
  (`count-c2.py:151`). Verified: tool selftest under `TMPDIR=scratch` wrote only under
  `scratch/mori-r60-ecst-*`. So C2's `selftest=ok` arm is unaffected by F1 — but the
  `--scratch …/st` argument reads as a containment guarantee it does not provide.

## Evidence — literal commands and outputs

```
$ sha256sum .ufo/waves/round-60/count-c{1,2,3}.py tools/mori-entry-claims-check.py tools/mori-settlement-scan.py
795c1f3193a76406a40561ac60fedb3eee75fc38df2b2efb3fc5295d617ddbae  count-c1.py
8c4814f54c564a7f00beec5249de092a2d3b2c4043e07be773d80e8e3ccdf976  count-c2.py
fabde06c9d0a94a8487e5de45be3e413f6084816fb0507a71fd335bad5153514  count-c3.py
cffe9f3359097277a7ea39729309efdc5831a1738994ceb30ee023ac0eae6e69  tools/mori-entry-claims-check.py
4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9  tools/mori-settlement-scan.py

$ git log --oneline ac496c7c..b3c2561 -- .ufo/waves/round-60/count-c1.py .ufo/waves/round-60/count-c2.py \
    .ufo/waves/round-60/count-c3.py tools/mori-entry-claims-check.py tools/mori-settlement-scan.py
(no output)
```

Arm A (cwd = lane root, `TMPDIR=<scratch>/tmpdir-a`):

```
$ python3 .ufo/waves/round-60/count-c1.py --selftest   -> C1_SELFTEST pass=6 fail=0        rc=0
$ python3 .ufo/waves/round-60/count-c2.py --selftest   -> C2_SELFTEST pass=8 fail=0        rc=0
$ python3 .ufo/waves/round-60/count-c3.py --selftest   -> C3_SELFTEST pass=3 fail=0        rc=0
$ python3 tools/mori-entry-claims-check.py --selftest  -> ENTRYCLAIMS_SELFTEST pass=13 fail=0 rc=0
$ python3 tools/mori-entry-claims-check.py --selftest --scratch <scratch>/explicit-scratch
                                                        -> ENTRYCLAIMS_SELFTEST pass=13 fail=0 rc=0
$ find <scratch>/tmpdir-a -mindepth 1 | wc -l           -> 0
```

Arm B (cwd = `/`, `env -u TMPDIR`): identical five lines, `rc=0`, stderr empty;
`ls -d <scratch>/tmpdir-b-explicit` → "No such file or directory";
`ls -1 /tmp` before/after → no diff; `find /tmp -maxdepth 1 -newer <marker>` → only `/tmp`.

Write-path classification:

```
arm A distinct write targets: 12 | under scratch: 12 | under /tmp: 0 | elsewhere: 0
arm B distinct write targets: 14 | under scratch: 0 | under /tmp: 14 | elsewhere: 0
A_c1/A_c3/B_c1/B_c3 write-class syscalls: 0 / 0 / 0 / 0
lanes+HOME paths among write-class syscalls: (none)
```

Mutant arms (scratch copies only, `TMPDIR=<scratch>/tmpdir-a`):

```
$ python3 m-c1.py --selftest   -> C1_SELFTEST pass=5 fail=1            rc=1  FAIL dead_plain
$ python3 m-c2.py --selftest   -> C2_SELFTEST pass=7 fail=1            rc=1  FAIL frozen_trees
$ python3 m-c3.py --selftest   -> C3_SELFTEST pass=2 fail=1            rc=1  FAIL pins
$ python3 m-ec.py --selftest   -> ENTRYCLAIMS_SELFTEST pass=12 fail=1  rc=1  FAIL good_no_reasons
$ python3 d-c3.py --selftest   -> C3_SELFTEST pass=2 fail=0            rc=0  (one chk dropped)
$ python3 d-ec.py --selftest   -> ENTRYCLAIMS_SELFTEST pass=12 fail=0  rc=0  (one chk dropped)
```

Broken-TMPDIR probe:

```
$ TMPDIR=<scratch>/does-not-exist python3 count-c2.py --selftest  -> rc=1, stdout empty,
    stderr: FileNotFoundError: [Errno 2] No such file or directory: '…/does-not-exist/mori-r60-c2st-0jdv9oj3'
$ TMPDIR=<scratch>/does-not-exist python3 tools/mori-entry-claims-check.py --selftest -> rc=1,
    stderr: FileNotFoundError: … '…/does-not-exist/mori-r60-ecst-29itr0nw'
$ TMPDIR=<scratch>/does-not-exist python3 count-c1.py --selftest  -> C1_SELFTEST pass=6 fail=0 rc=0
$ TMPDIR=<scratch>/does-not-exist python3 count-c3.py --selftest  -> C3_SELFTEST pass=3 fail=0 rc=0
```

## Restoration / no-mutation evidence

- Instrument bytes are the frozen bytes, before and after: five `sha256sum` values above
  equal at `ac496c7c`, at tip `b3c2561`, in the working tree, and re-checked after every
  run in this seat.
- `git -C <lane> status --porcelain` shows only the pre-existing untracked wave artefacts
  (`evidence/c1-at-data.txt`, `w1.ready*`, `w1/` from sibling seats) — no modification of
  any tracked file by this seat; no commit, no VCS/Git mutation, no fixture repo created.
- Mutants were written as **new files** under `<scratch>/mut/`; pristine originals were
  never rewritten, so no restoration step was needed.
- Scratch self-check before cleanup: `tmpdir-a` 0 entries, no `/tmp/mori-r60-*`, all traced
  write targets absent; scratch tree then removed. Nothing outside
  `/fast/scratch/hyaku/mori-r60/Mo60MutationTester35` was written except this report.

## Limits

- Consistency was measured for the four `--selftest` entry points named by the seat and
  the write classification for their direct syscalls; the full counter runs
  (`measure()`) are other seats' scope (C2/C3 at-freeze receipts already cover them).
- F4/F5 mutants are copies-under-scratch probes of the selftest's own discrimination, not
  mutations of the frozen instruments; the frozen claim artefacts are untouched.
- F5's "c1/c3 pass-count tokens are contract-only" is a static reading of count-c1/c2/c3
  plus the contract, corroborated by the SHA pins; it is a coverage note, not a defect
  against any frozen predicate.
- Observation only: no remediation, no provider/death inference, no claim mutation. The
  contract's selftest lines and the at-freeze receipts remain as scored at `ac496c7c`.
