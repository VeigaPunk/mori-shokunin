# Mo51ExecRound40Reexec — does the round-51 `conform.py` edit change any round-40 verdict?

Seat: Mo51ExecRound40Reexec (executor, leaf). Wave `w1`, round 51, lane mori-shokunin.
Assignment: take round 40's scored revisions and its `conform.py` receipts, re-execute the frozen
round-40 checker bytes and the round-51 data bytes against the same counters and revisions, and
answer AGREE / DIVERGE per receipt with the exact diff.

**Answer: AGREE, 13 of 13 `c10-after-*` receipts.** No round-40 verdict changes. Under both byte
versions, at the same revision (`265a955cc67be4eae97d2dc5a9338a25f31eb29b`) and over the same
counters/fixtures, every receipt reproduces the same `CONFORM=`/`CONFORM_SELFTEST` line, the same
set of failing checks and the same exit code. The frozen bytes reproduce the receipts
*byte-identically*; the edited bytes reproduce them byte-identically as well once the checker is
invoked at its canonical lane path, and differ elsewhere only in the absolute path text of the
`tool_resolve` detail line (always PASS). One real behaviour change exists, and it bites
*re-derivation of round-40's retained copies*, not its recorded verdicts — finding 3.

Scratch: `/fast/scratch/hyaku/mori-r51/Mo51ExecRound40Reexec/` (clone, TMPDIR, outputs; removed at
the end of this seat — see §9). Apart from this report nothing was written under the lane, and
nothing at all to the fleet root or any sibling lane.

## 1. What round 40 scored, and which receipts name the checker

`LOG.md` round-40 entry:

- C1 operability: `python3 .ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b`
  → `CONFORM=met` exit 0 (`evidence/c10-after.txt`); `--selftest` → `CONFORM_SELFTEST pass=11 fail=0`
  (`evidence/c10-after-selftest.txt`); the per-fixture after receipts (`c10-after-<fixture>.txt`),
  the gutted-conjunct copy (`c10-after-conjunct.txt`), the two-counter audit
  (`c10-after-multicounter.txt`); before-side `c10-red-*` runs the round-39 bytes
  (`fixtures/extracted/conform-v2-r39.py`); `c10-parity.txt` is a count-c7/count-c8 parity receipt.
- The round-40 instrument commit is `265a955c`; `evidence/freeze-r40.txt` pins
  `5025b9664632d01063c11b4f5dadd4f9a063db66d73315d7ed25db8d90b83aaf  .ufo/waves/round-40/conform.py`.
  The 13 `c10-after-*` receipts themselves landed in one later commit, `8d3badd0`
  (`git log --oneline -- <each receipt path>` prints exactly one line), so the files compared here
  are the committed bytes, unchanged since.

The edit under test (`87e0c37`, round-51 data commit) is one hunk:

```
--- .ufo/waves/round-40/conform.py  (5025b966…, at 265a955c / aa3af1ec)
+++ .ufo/waves/round-40/conform.py  (7f5174d5…, at 87e0c374)
@@ -66,8 +66,11 @@
 import sys
 import tempfile

-LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
-SCRATCH_ROOT = os.path.join(LANE, ".ufo", "waves", "round-40", "scratch")
+# Round 51 (C1, routed defect 1 of the round-50 spot-check): the lane is the tree this file
+# sits in (<lane>/.ufo/waves/round-40/conform.py), not a hardcoded host path, and the selftest
+# scratch lives under TMPDIR, not inside the lane.
+LANE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
+SCRATCH_ROOT = tempfile.gettempdir()
 DEFAULT_COUNTERS = [os.path.join(LANE, ".ufo/waves/round-40/count-c8.py")]
```

`git diff --name-status aa3af1ec 87e0c37` shows the only round-40 file touched is `conform.py`;
`count-c8.py` is byte-identical at both revisions
(`4e4d50eb1e96d947f0e9d2ab25a13b2b8c33963f216f3be43060a3348702f6da` at `265a955c` and at `87e0c37`),
and no file under `.ufo/waves/round-39/` or `.ufo/waves/round-40/fixtures/` changes. So
`c10-red-*` (round-39 extracted bytes) and `c10-parity.txt` (counter bytes) cannot be affected by
this hunk; they are out of the measured set below and are recorded here as untouched by
construction, not by replay.

## 2. Method

The receipts were produced with the checker's own `LANE` hardcoded to the lane path, running
against the lane. Two things must be true of a faithful replay: the revision must resolve in the
tree the checker reads, and no write may land in the fleet repo (the checker's `--selftest` writes
and removes a scratch dir under the checker's `SCRATCH_ROOT`, and the counter carries a lane-path
`SCRATCH_ROOT` with `os.makedirs` + `mkdtemp` at `count-c8.py:470-471`).

Setup (one clone, per the seat limit; `--no-local`, because a `--shared` clone's `alternates`
file points at the lane's `.git/objects` and would be shadowed by the sandbox's lane bind):

```
S=/fast/scratch/hyaku/mori-r51/Mo51ExecRound40Reexec
git clone --no-local --quiet /home/vgpnk/Projects/shokunin/mori-shokunin "$S/A"
git -C "$S/A" checkout -q 265a955cc67be4eae97d2dc5a9338a25f31eb29b
git -C "$S/A" rev-parse --show-toplevel      # -> $S/A   (asserted before any commit-adjacent work)
sha256sum "$S/A/.ufo/waves/round-40/conform.py"
5025b9664632d01063c11b4f5dadd4f9a063db66d73315d7ed25db8d90b83aaf   (frozen round-40 bytes)
```

Byte versions used, extracted with read-only git:

```
git -C <lane> show 265a955c:.ufo/waves/round-40/conform.py > bytes/conform-r40.py   5025b966…
git -C <lane> show 87e0c37:.ufo/waves/round-40/conform.py > bytes/conform-r51.py   7f5174d5…
cmp bytes/conform-r40.py "$S/A/.ufo/waves/round-40/conform.py"      # identical
```

Every run happens inside a bubblewrap namespace that binds the clone onto the lane path, so the
frozen bytes' hardcoded `LANE` and the counter's hardcoded `DEFAULT_REPO` resolve to the clone and
every scratch write lands in the clone, never in the fleet repo. `TMPDIR` is the seat scratch:

```
bwrap --dev-bind / / --bind "$S/A" /home/vgpnk/Projects/shokunin/mori-shokunin \
      --chdir /home/vgpnk/Projects/shokunin/mori-shokunin --setenv TMPDIR "$S/tmp" \
      /usr/bin/python3 .ufo/waves/round-40/conform.py 265a955c <case args>
```

Sandbox sanity, checked before the measurement passes: `lane files: 22` (the clone, not the
113 MB lane), `git rev-parse HEAD` inside the namespace
`265a955cc67be4eae97d2dc5a9338a25f31eb29b`, `TMPDIR` under scratch.

Run order per byte version: the 11 non-selftest invocations (the `after` run plus ten
fixture/multi-counter runs), `--selftest`, and the gutted-conjunct copy. The clone's `conform.py` was overwritten with the bytes under test before
each pass (`7f5174d5…` for the round-51 pass, then restored to `5025b966…` and replayed again so
the exit codes of the frozen-bytes pass are recorded next to its outputs; the frozen pass produced
the same rc pattern both times).

Two differences between my command lines and the recorded `command:` lines, neither of which
changes output: (a) the receipts' fixture invocations show bare basenames
(`--counter survivor-cond.py`), I passed full paths, and the checker prints
`os.path.basename` (all outputs matched line for line); (b) the gutted-conjunct fixture is absent
at `265a955c` (it was committed at `ede486b7`, pinned in the round-41 freeze additions as
`20e324228735d39ad6bb293aac9dfd4b3a27a009a0f2ecf222731771bd2aaabf`), so I copied the lane's
working-tree file, verified its sha256 equals that pin, into the clone's
`.ufo/waves/round-40/fixtures/generated/`.

## 3. Per-receipt result

Cell shape: verdict line, exit code, failing checks. Left run uses the frozen bytes (`5025b966…`),
right run the round-51 bytes (`7f5174d5…`), same clone, same revision `265a955c`, same inputs.

| receipt | round-40 frozen bytes | round-51 bytes | vs receipt |
|---|---|---|---|
| `c10-after.txt` | `CONFORM=met` rc=0, fails=- | `CONFORM=met` rc=0, fails=- | AGREE / AGREE |
| `c10-after-multicounter.txt` | `CONFORM=unmet` rc=1, fails=`drain_bind,selftest_conjunct` | same | AGREE / AGREE |
| `c10-after-cond.txt` | `CONFORM=unmet` rc=1, fails=`timeout_scope` | same | AGREE / AGREE |
| `c10-after-decoy.txt` | `CONFORM=unmet` rc=1, fails=`drain_bind` | same | AGREE / AGREE |
| `c10-after-divzero.txt` | `CONFORM=unmet` rc=1, fails=`predicate,head_pin,tool_resolve,timeout_scope,timeout_state` | same | AGREE / AGREE |
| `c10-after-inf.txt` | `CONFORM=unmet` rc=1, fails=`timeout_scope` | same | AGREE / AGREE |
| `c10-after-second-popen.txt` | `CONFORM=unmet` rc=1, fails=`drain_bind` | same | AGREE / AGREE |
| `c10-after-shadow-neg.txt` | `CONFORM=unmet` rc=1, fails=`timeout_scope` | same | AGREE / AGREE |
| `c10-after-shadow-none.txt` | `CONFORM=unmet` rc=1, fails=`timeout_scope` | same | AGREE / AGREE |
| `c10-after-tuple.txt` | `CONFORM=unmet` rc=1, fails=`drain_bind` | same | AGREE / AGREE |
| `c10-after-underscore.txt` | `CONFORM=unmet` rc=1, fails=`drain_bind` | same | AGREE / AGREE |
| `c10-after-selftest.txt` | `CONFORM_SELFTEST pass=11 fail=0` rc=0 | same | AGREE / AGREE |
| `c10-after-conjunct.txt` | `CONFORM_SELFTEST pass=0 fail=10` rc=1 | same | AGREE / AGREE |

Comparison rule: receipt body (all lines after the `command:` wrapper, all lines before `EXIT=`)
against the replay's stdout, plus replay exit code against the receipt's `EXIT=`; absolute tree
prefixes normalised to `<tree>`. Result:

```
receipts: 13
r40 AGREE (normalised tree prefix, exit compared): 13 / 13
r51 AGREE (normalised tree prefix, exit compared): 13 / 13
mismatches: []
```

Without normalisation the frozen-bytes pass is byte-identical to every receipt (including
`resolved=/home/vgpnk/Projects/shokunin/mori-shokunin/….witness-summary-only-live.txt`), because
the frozen bytes print the lane path they were handed. The round-51 pass, run from the clone,
prints that path relative to the tree the checker sits in —
`resolved=/fast/scratch/…/A/.ufo/waves/round-39/fixtures/witness-summary-only-live.txt` — on
exactly 11 lines (one `tool_resolve` detail per non-selftest, non-conjunct receipt); every one of
those lines is still PASS and the difference is the edit's intended behaviour (the checker now
names the tree it derives from). Invoked at the lane path inside the same sandbox, the round-51
bytes are byte-identical to the receipt, which is the production layout:

```
$ bwrap … --chdir /home/vgpnk/Projects/shokunin/mori-shokunin python3 \
      /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/conform.py 265a955c
rc=0
$ diff <(receipt body of c10-after.txt) <(that run's stdout)   # no output
BYTE-IDENTICAL to c10-after.txt
```

Selftest detail under the edited bytes (same 11 arm lines and the same per-arm PASS text as the
receipt, including the scratch arm):

```
PASS predicate          predicate token changed -> only predicate failed
PASS head_pin           pin label renamed -> only head_pin failed
PASS tool_resolve       relative resolution removed -> only tool_resolve failed
PASS bounded_reads      git helper run timeout removed -> only bounded_reads failed
PASS timeout_scope      timeout value replaced with None -> only timeout_scope failed
PASS timeout_scope_shadow function-local None shadow inserted -> only timeout_scope failed
PASS drain_bind         communicate drains replaced by wait+read -> only drain_bind failed
PASS drain_bind_decoy   decoy used communicate beside a wait+read drain -> only drain_bind failed
PASS timeout_state      budget flag ignored -> only timeout_state failed
PASS scratch            scratch parent moved off-lane -> only scratch failed
PASS selftest_conjunct  communicate timeout keyword stripped -> only selftest_conjunct failed
CONFORM_SELFTEST pass=11 fail=0
```

and `$S/tmp` was empty after the run (`mori-conform-selftest-*` removed by the `finally`), i.e.
the scratch relocation writes nothing into the tree.

## 4. Supplementary: the round-40 gate command at the round-51 data commit

Same clone, checked out at `87e0c374537557754bf71dd68036ded3ddc6699c` (committed bytes
`7f5174d5…`), sandbox binding the lane path, `TMPDIR` in scratch. The lane has since advanced to
`b504cb17` (wave `w1` spec/receipts); I did not clone past the data commit, so this is the data
commit, not the later tip:

```
$ python3 .ufo/waves/round-40/conform.py 87e0c374537557754bf71dd68036ded3ddc6699c
check predicate          PASS (exit=0 equal=True)
check head_pin           PASS (pin=87e0c374537557754bf71dd68036ded3ddc6699c tip=87e0c374537557754bf71dd68036ded3ddc6699c)
check tool_resolve       PASS (exit=0 resolved=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-39/fixtures/witness-summary-only-live.txt)
check bounded_reads      PASS (count-c8.py: bounded=[] value=[])
check timeout_scope      PASS (count-c8.py: bounded=[] value=[])
check drain_bind         PASS (count-c8.py: violations=[])
check timeout_state      PASS (exit=1 timeout_reason=True pass=False)
check scratch            PASS (count-c8.py: mkdtemp_dir=True root=True)
check selftest_conjunct  PASS (count-c8.py: honest_comm=[] strips=6 detected=6 anchor=True entry_live=True)
CONFORM=met
rc=0
```

The gate still reads `CONFORM=met` at the data commit. `head_pin` shows that tip, not
`265a955c`: that is the same drift the round-40 wave seat `w1/ExeConformMet.md` recorded when it
replayed at `ede486b7` — see finding 4. It is not a verdict change for the claim, which is
measured at `265a955c`.

## 5. The one behaviour change: derived `LANE` is depth-sensitive (finding 3)

`LANE = dirname⁴(abspath(__file__))` is correct only when the checker sits exactly at
`<lane>/.ufo/waves/round-40/conform.py`. Round 40 keeps *copies* of the checker one and two
directories deeper:

- `.ufo/waves/round-40/fixtures/generated/conform-v3-conjunct-gutted.py` (the copy behind
  `c10-after-conjunct.txt`; committed, 36374 bytes, pin `20e32422…`),
- `.ufo/waves/round-40/scratch/mutconform-arms2/conform-pristine.py` and
  `conform-mut-cond-unconditional.py` (the mutation harness behind `w1/MutConformArms.md`).

Both retained copies still carry the frozen `LANE = "…/mori-shokunin"` line (verified:
`conform-pristine.py` sha256 `5025b966…`, `conform-v3-conjunct-gutted.py` sha256 `20e32422…`), so
round-40's receipts re-execute unchanged. But a copy regenerated from the round-51 bytes exits 2
before any check runs. Measured, same sandbox, round-51 bytes placed one level deeper:

```
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/fixtures/generated/conform-r51-copy.py 265a955c
rc=2
stderr: conformance setup error: [Errno 2] No such file or directory:
        '/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/.ufo/waves/round-39/contract.md'

$ … conform-r51-copy.py 265a955c --selftest
rc=2
stderr: conformance setup error: [Errno 2] No such file or directory:
        '/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/.ufo/waves/round-40/count-c8.py'
```

(`dirname⁴` of the copy is `<lane>/.ufo/waves`, hence the doubled `.ufo/waves`.) Measured at both
retained depths — one level deeper (`fixtures/generated/`) and two deeper
(`scratch/mutconform-arms2/`, rc=2, identical setup error naming
`<lane>/.ufo/waves/.ufo/waves/round-39/contract.md`); both land on the same wrong
`LANE=<lane>/.ufo/waves`. Consequence: regenerating `conform-v3-conjunct-gutted.py`
from current bytes would replace a `pass=0 fail=10` artifact with a `conformance setup error`
artifact — the round-40 receipt would no longer be re-derivable from the shipped checker, even
though the committed receipt and the committed fixture remain valid.

Round 51's own controls are not exposed to this: `controls/c1-controls.py` computes its `LANE` as
`dirname⁴` of `.ufo/waves/round-51/controls` (correct) and installs the witness checker bytes at
the canonical `.ufo/waves/round-40/conform.py` path in the control clone.

## 6. Disk and environment

```
$ /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status
… (idle-file list; no ENOSPC state)
$ df -h /fast
/dev/nvme1n1p2  804G  216G  588G  27%  /fast
```

No package manager ran (host-wide pacman pause respected); no tool was installed or upgraded, so
there is nothing to record under the install ledger. No kernel-log text was read, no cgroup,
sysctl, swap or watermark touched, no service commands. Lane and fleet repos were only read
(`git log/show/diff/ls-tree/rev-parse`). `/home/vgpnk/Projects/shokunin/shokuknow` was not touched.

Containment probe (run after the measurements, to verify the sandbox claim): a write to the lane
path inside the namespace landed in the clone and not in the lane.

```
$ bwrap … --chdir <lane path> python3 -c 'p="<lane>/.ufo/waves/round-40/scratch/probe-ns-write.txt"; open(p,"w").write("probe\n"); print(os.path.realpath(p))'
wrote <lane path>…/probe-ns-write.txt realpath <lane path>…/probe-ns-write.txt    rc=0
$ ls -l $S/A/.ufo/waves/round-40/scratch/probe-ns-write.txt     -> exists (clone)
$ ls -l <lane>/.ufo/waves/round-40/scratch/probe-ns-write.txt   -> No such file or directory
```

(Probe file removed from the clone immediately.) The clone's `.ufo/waves/round-39/scratch/` does
not exist after these runs, i.e. the counter's `SCRATCH_ROOT` path was never written in these
invocations.

Concurrent lane activity observed, not from this seat: the lane's `.ufo/waves/round-40/scratch/`
holds two leftover untracked directories, `mori-conform-selftest-858cf_2r` (19:54:13) and
`mori-conform-selftest-y5k7kzyi` (19:53:24), each with partial `counter-*.py` mutation copies, and
that directory's mtime moved to 19:57:28 — after this seat's last run (19:56:49) — while the
lane's `.ufo/waves/round-39/scratch/` was created/emptied at 19:56:31. Both are the scratch roots
of the frozen checker/counter, so another seat is replaying them unsandboxed in the same window
(see finding 6). This seat's writes went to the clone, as the probe shows.

## 7. Named limits of this replay

- One moment of the counters: `timeout_state` runs the counter under a 3 s tool budget; a loaded
  host could flip that arm. It held in every run here (two frozen-bytes passes and one edited-bytes
  pass, 13 receipts each), but I did not repeat each receipt a third time or under load.
- The sandbox is bubblewrap on this host and kernel; it proves the replay does not need the fleet
  repo for writes, not that the checker is portable.
- The revision is the one the receipts name (`265a955c`). I did not replay the *before* controls
  (`c10-red-*`, round-39 extracted bytes) or the mutation arms (`w1/MutConformArms.md`), because
  the edit cannot reach their bytes; that is an inference from `git diff --name-status`, not a
  replay.
- `c10-parity.txt` is a counter-vs-counter parity receipt, not a checker run; untouched.
- One clone, as the seat rule allows; the tip run reused it after a checkout, so the tip check and
  the `265a955c` checks share object storage but not a working tree state at the same time.

## 8. Round-40 instrument observations (no fix proposed; instruments are frozen)

- `head_pin` compares the counter's `--pin-only --repo` output (the repo's HEAD) with
  `git -C repo rev-parse HEAD` on the same repo, so it cannot detect that the replayed revision is
  not the tip; a replay at a later tip prints PASS with a drifted pin. This is the mechanism behind
  the round-40 wave seat's `head_pin` drift note in `w1/ExeConformMet.md`.
- The fixture receipts' `command:` lines record bare basenames; a later replayer cannot recover the
  exact argv from the receipt alone (my full-path replay produced identical output because the
  checker prints basenames).

## 9. Scratch removal

`rm -rf /fast/scratch/hyaku/mori-r51/Mo51ExecRound40Reexec` after this report was written (clone,
`bytes/`, `out/`, `tmp/`, runner and comparison scripts). Everything cited above is quoted in this
file, so nothing needed from the seat survives only in scratch.

## Findings

1. **LOW — no round-40 verdict changes.** All 13 `c10-after-*` receipts reproduce identically
   (verdict line, failing-check set, exit code) under both the frozen bytes
   (`5025b966…`, `.ufo/waves/round-40/conform.py` at `265a955c`) and the round-51 bytes
   (`7f5174d5…`, at `87e0c37`), same revision `265a955c`. Evidence: §3 table, 13/13 AGREE.
   Files: `.ufo/waves/round-40/evidence/c10-after*.txt`.
2. **LOW — the only textual difference is layout-relative, not a verdict.**
   `tool_resolve`'s `resolved=` prefix prints the tree the checker derives; PASS in every case, and
   byte-identical to `c10-after.txt` when the edited checker is invoked at the canonical lane path.
   File: `.ufo/waves/round-40/conform.py:72` (`LANE = dirname⁴(__file__)`).
3. **MED — the derived `LANE` is sensitive to the checker's depth, so round-40's retained copies
   cannot be regenerated from the current bytes.** A copy one directory deeper
   (`…/fixtures/generated/conform-r51-copy.py`) computes `LANE=<lane>/.ufo/waves` and exits 2
   (`conformance setup error`, both the plain and the `--selftest` form) before any check runs;
   round-40's `conform-v3-conjunct-gutted.py` and the `scratch/mutconform-arms2/` harness live at
   that depth or deeper. Recorded receipts are unaffected because those committed copies still hold
   the frozen bytes. Files: `.ufo/waves/round-40/conform.py:72`,
   `.ufo/waves/round-40/fixtures/generated/conform-v3-conjunct-gutted.py:69`,
   `.ufo/waves/round-40/scratch/mutconform-arms2/conform-pristine.py:69`.
4. **LOW — the frozen `head_pin` check cannot fail on a same-repo replay.** It compares the
   counter's repo HEAD against `git -C repo rev-parse HEAD` on the same repo, so replaying at any
   tip prints PASS with a drifted pin rather than FAIL (observed at `87e0c37` in §4; the round-40
   wave seat saw the same at `ede486b7`). File: `.ufo/waves/round-40/conform.py` `evaluate()`
   `head_pin` block.
5. **LOW — fixture receipt commands name bare basenames**, so the recorded `command:` lines do not
   pin the argv a replayer must use; output happened to be path-independent because the checker
   prints basenames. Files: `.ufo/waves/round-40/evidence/c10-after-{cond,decoy,divzero,inf,
   second-popen,shadow-neg,shadow-none,tuple,underscore}.txt` (line 1).
6. **LOW — lane scratch residue from concurrent unsandboxed replays, not this seat's.**
   `.ufo/waves/round-40/scratch/mori-conform-selftest-858cf_2r` (19:54:13) and
   `.ufo/waves/round-40/scratch/mori-conform-selftest-y5k7kzyi` (19:53:24) are unfinished
   selftest scratch trees (partial `counter-*.py` copies) left in the lane; the round-39 scratch
   root was also created/emptied at 19:56:31. My writes are contained in the clone (probe in §6),
   and the round-40 scratch directory changed again at 19:57:28, after this seat's last run.
   Whoever runs the frozen checker or counter without a lane bind will keep planting these; the
   round-40 receipts are unaffected. File/dir: `.ufo/waves/round-40/scratch/`.
