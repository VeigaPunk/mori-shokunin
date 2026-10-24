# MutC4Live — live_rows mutation probe (C1 / P-C4)

Seat: mutation-tester, mori round 38, wave 2. Target revision
`f725f3076972e6e70595b5ac8279be524a111ff8` (`git rev-parse HEAD` in the lane printed this, and the
lane's `.ufo/waves/round-37/evidence/drift-live-r37.txt` hashed to the blob committed at that tip:
`git hash-object <file>` = `git rev-parse f725f3076972e6e70595b5ac8279be524a111ff8:.ufo/waves/round-37/evidence/drift-live-r37.txt`
= `66c17a2fe47e831ee36edf7d6b9b43ababa76c1f`). Lane files were read-only; all mutation work ran on
a fresh sandbox under `.ufo/waves/round-38/scratch/MutC4Live/w2/`.

Detector under probe: `.ufo/waves/round-38/count-c4.py`, sha256
`3340d594123e4f983ddadc4759fd108438bd9b314dda17ab56690a08a7302403`. The arm is
`check_live_rows` at `count-c4.py:184-197`; its pass predicate is
`drifted >= 1 and len(named) == drifted and not unknown` (`count-c4.py:196`), where `named` are the
lines matching `^(S\d{3}) drifted$` and `unknown` are named ids absent from the 225-row registry
`corpus/SOURCES.md` at the same revision.

Baseline sanity, run before any mutation: `--repo` the fresh sandbox at `f725f30` printed
`check live_rows  PASS (named=10 summary_drifted=10 unknown=[])` and `C4=met`, exit 0
(`w2/baseline-sandbox.txt`, `w2/baseline-sandbox.err` empty). This baseline is the pristine run the
two mutants are measured against.

## Mutants

Both mutants derive from the committed receipt at `f725f30` only; `git diff --name-only f725f30
<mutant>` shows exactly one changed path, `.ufo/waves/round-37/evidence/drift-live-r37.txt`, in both
cases. No other byte differs.

**Mutant A — summary kept, per-row lines dropped.** `grep -v -E '^S[0-9]{3} '` over the pristine
receipt leaves the command header, the summary sentence and `EXIT=1`; 225 row lines removed
(`git diff --stat` = `1 file changed, 225 deletions(-)`). 3 lines, git blob
`da4acfcfce5de2788a409987345d52384cfdb48c`, sha256
`22b8242bbe4f8dd88edff20ad7343c35b97fb33fd019fb79c8e3197d784e360e`.

```diff
--- drift-live-r37.txt (f725f30)
+++ drift-live-r37.txt (mutant A)
@@
 command: timeout 900 python3 tools/mori-source-drift.py --root .   # at the 225-row registry, all five r37 copies committed
-S001 no-copy
-S002 no-copy
… (223 more S### lines) …
-S225 fresh
 MORI_SOURCE_DRIFT rows=225 fresh=53 excerpt=0 drifted=10 unavailable=0 no-copy=162
 EXIT=1
```

**Mutant B — rows kept, one named id unregistered.** Single-line rename `S156 drifted` →
`S999 drifted`, keeping 10 ` drifted` rows and the summary unchanged. 228 lines, git blob
`7469d715b707608d0e2a0b9097f784349a7d5f1a`, sha256
`6e59ae3c89375f886b57977ae02caebb99c1d5749ef20b904d8d7fb5cd50cd0f`.

```diff
--- drift-live-r37.txt (f725f30)
+++ drift-live-r37.txt (mutant B)
@@ -154,7 +154,7 @@ S152 no-copy
 S155 no-copy
-S156 drifted
+S999 drifted
 S157 drifted
```

Sandbox: `w2/sbx` = `git clone --shared --no-checkout` of the lane (HEAD `f725f30`, objects via
`.git/objects/info/alternates` → lane `.git/objects`, read-only). Mutant commits were created with
plumbing only, no worktree checkout:

- A: `hash-object -w` → `read-tree f725f30` → `update-index --add --cacheinfo 100644,<blob>,<path>`
  → `write-tree` = `fec580eb47ead39f1a6127f959d322b8dc04ed90` → `commit-tree -p f725f30` =
  `4d2fa76c382039b9cc250f404289af93a2c2bf1b` (`refs/heads/mutantA`).
- B: same plumbing → tree `db6b5f6245b7f05cf0e77dc7a24931ebd992ac3f` → commit
  `2cfb2adb49b617d564bbd3205a87009ceec99174` (`refs/heads/mutantB`).

## Detector command (identical bytes run on pristine, both mutants, restored)

```
python3 .ufo/waves/round-38/count-c4.py f725f3076972e6e70595b5ac8279be524a111ff8 --repo <w2/sbx>
python3 .ufo/waves/round-38/count-c4.py 4d2fa76c382039b9cc250f404289af93a2c2bf1b --repo <w2/sbx>
python3 .ufo/waves/round-38/count-c4.py 2cfb2adb49b617d564bbd3205a87009ceec99174 --repo <w2/sbx>
python3 .ufo/waves/round-38/count-c4.py f725f3076972e6e70595b5ac8279be524a111ff8 --repo <w2/sbx>   # after ref deletion
```

## Output

Baseline, pristine `f725f30` — **C4=met, exit 0** (`w2/baseline-sandbox.txt`, 9.16 s):

```
negative witness-token-entry        rejected
negative witness-dangling-row       rejected
negative witness-summary-only-live  rejected
check anchors          PASS (anchors=3 missing=[])
check capability       PASS (paths=['tools/mori-source-drift.py', '.ufo/waves/round-37/evidence/c2-after-v3.txt', '.ufo/waves/round-37/evidence/drift-live-r37.txt'] missing=[])
check live_rows        PASS (named=10 summary_drifted=10 unknown=[])
check named_row_drift  PASS (exit=0 row_states=('PASS', ''))
check drift_kill       PASS (exit=1 row_states=('FAIL', "got=[('S101', 'fresh'), … ('S103', 'excerpt') …] want=[… ('S103', 'drifted') …]"))
C4=met
```

Mutant A, `4d2fa76` — **C4=unmet, exit 1** (`w2/mutantA-run.txt`, `w2/mutantA-exit.txt`):

```
check anchors          PASS (anchors=3 missing=[])
check capability       PASS (paths=[…] missing=[])
check live_rows        FAIL (named=0 summary_drifted=10 unknown=[])
check named_row_drift  PASS (exit=0 row_states=('PASS', ''))
check drift_kill       PASS (exit=1 row_states=('FAIL', …))
C4=unmet
```

Mutant B, `2cfb2ad` — **C4=unmet, exit 1** (`w2/mutantB-run.txt`, `w2/mutantB-exit.txt`):

```
check anchors          PASS (anchors=3 missing=[])
check capability       PASS (paths=[…] missing=[])
check live_rows        FAIL (named=10 summary_drifted=10 unknown=['S999'])
check named_row_drift  PASS (exit=0 row_states=('PASS', ''))
check drift_kill       PASS (exit=1 row_states=('FAIL', …))
C4=unmet
```

Both mutants flip exactly `live_rows`; `anchors`, `capability`, `named_row_drift`, `drift_kill` and
the three negative witnesses are unchanged from baseline, so the failure is attributable to the
mutated row content and not to a side effect on other checks.

- A fails the count arm: 0 named drifted lines against a summary claiming 10.
- B fails the registry-membership arm: 10 named rows (count matches the summary), but `S999` is not
  a row of `corpus/SOURCES.md` at the revision, so `unknown=['S999']`. `S156` (the id it replaced)
  is registered, confirming the flip comes from the unregistered id, not from losing a row.

## Verdict

**Both mutants KILLED by `live_rows` — acceptance PASS.** Mutant A: `check live_rows FAIL
(named=0 summary_drifted=10 unknown=[])`, `C4=unmet`, exit 1. Mutant B: `check live_rows FAIL
(named=10 summary_drifted=10 unknown=['S999'])`, `C4=unmet`, exit 1. The detector discriminates a
summary-only receipt and a receipt whose rows name an unregistered id, while the pristine receipt
still passes at the same revision.

Scope note (not run, no claim): this probe exercised the count and registry-membership arms of
`check_live_rows`. A duplicate-registered-id substitution that keeps `named == summary_drifted`
(e.g. two `S157 drifted` lines and no `S156 drifted`) would satisfy both tested arms by
construction; the detector does not compare the named id *set* against the true drifted set. Noted
as probe scope only — no contract change proposed, and no remediation performed.

## Restoration evidence

- Mutant refs deleted from the sandbox (`git update-ref -d refs/heads/mutantA`,
  `… mutantB`); `git -C sbx for-each-ref` afterwards lists only `refs/heads/master` and the
  `refs/remotes/origin/*` refs, all at their original object ids (`master` =
  `f725f3076972e6e70595b5ac8279be524a111ff8`). Temporary indexes `.git/index-mutA`/`index-mutB`
  removed.
- Restored tree re-reads exact pristine bytes: `git -C sbx rev-parse
  f725f30:.ufo/waves/round-37/evidence/drift-live-r37.txt` = `66c17a2fe47e831ee36edf7d6b9b43ababa76c1f`;
  `git -C sbx show f725f30:<path> | sha256sum` =
  `82d79f0d550412313765f440981e7a60acefb4e32b0cee6f008e584535686c16`.
- Restored bytes re-run through the same detector: **C4=met, exit 0**, `check live_rows PASS
  (named=10 summary_drifted=10 unknown=[])` (`w2/restored-run.txt`, 9.17 s).
- Mutant blobs never entered the lane object store: `git cat-file -e
  da4acfcfce5de2788a409987345d52384cfdb48c` in the lane fails (`LANE_OBJECT_STORE_CLEAN`); the
  sandbox's alternates link only reads the lane store, and `hash-object -w` wrote the mutant blobs
  into `w2/sbx/.git/objects` (mutant blobs remain there as unreachable scratch objects after ref
  deletion; sandbox is disposable scratch, not the lane).

## Lane untouched

- `.ufo/waves/round-37/evidence/drift-live-r37.txt` sha256 before and after the probe:
  `82d79f0d550412313765f440981e7a60acefb4e32b0cee6f008e584535686c16`; `git hash-object` =
  `66c17a2…` = the blob committed at `f725f30`; `cmp` against the scratch copy
  `w2/pristine-live.txt`: identical.
- No `git add/commit/push/fetch/reset/stash`, no jj command, no lane file edited by this seat.
  `find .ufo/waves/round-38/scratch -maxdepth 1 -name 'mori-c4-*'` printed 0 leftovers (the counter's
  own `mkdtemp` dirs are removed by its `finally`).
- All seat outputs are under `.ufo/waves/round-38/scratch/MutC4Live/w2/`:
  `baseline-sandbox.txt`, `mutantA-run.txt`, `mutantB-run.txt`, `restored-run.txt`,
  `mutantA-exit.txt`, `mutantB-exit.txt`, `commitA.txt`, `commitB.txt`, the three live-receipt
  fixtures (`pristine-live.txt`, `mutantA-summary-only.txt`, `mutantB-s999.txt`), and the `sbx/`
  sandbox. Note: `scratch/MutC4Live/` also contains wave-1 leftovers (`c4-*.txt`, `sandbox/`,
  `verify/`, timestamps 19:37–19:54, predating this seat); they were not used as evidence — every
  finding above was re-derived by the commands shown.

## Tooling

No installs or upgrades were needed; no package manager was invoked. `git 2.56.0` and the system
`python3` were sufficient. The only lane-relative file written by this seat is this report.

Report: .ufo/waves/round-38/w2/MutC4Live.md
