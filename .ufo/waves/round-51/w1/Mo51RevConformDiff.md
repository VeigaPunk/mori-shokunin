# Mo51RevConformDiff — review of the round-51 change to `.ufo/waves/round-40/conform.py`

- Seat: Mo51RevConformDiff (reviewer, round 51 wave w1, leaf — no subagents used)
- Date: 2026-10-26 · MACHINE_ID: 432d02b544a5459ebbff9c42ec68334d
- Scope: `git diff aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd 87e0c374537557754bf71dd68036ded3ddc6699c -- .ufo/waves/round-40/conform.py` — does any check change verdict, is the run output the same on entering vs data bytes, and is editing a round-40 frozen instrument honest given round 40's freeze.
- LSP: no `lsp` device is mounted in this seat (checked `xd://lsp`: "No such tool"); all caller/definition checks are text + execution based. Recorded as unavailability, not as semantic proof.
- Tools installed: none.

## 1. The change (complete diff, 5+/2−)

```diff
--- a/.ufo/waves/round-40/conform.py        (blob 71fa59774c676267224a7845e416fd84d19a4e96)
+++ b/.ufo/waves/round-40/conform.py        (blob 63cff4a61b2d585270e9bbb6e07f7f16faea2da8)
@@ -66,8 +66,11 @@ import subprocess
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

Byte identity of the rest verified: count-c8.py, the round-39 contract, and both round-39 fixtures named by conform.py are byte-identical between the two commits (empty `git diff` over all four paths); conform.py's diff leaves every other line untouched; at HEAD b504cb17 and in the working tree conform.py is still exactly the 87e0c374 bytes (`git diff 87e0c374..b504cb17` and `git diff 87e0c374` over the path both empty).

## 2. Static answer: no check of conform.py can change verdict from this diff

Read of the full 808-line file at 87e0c374:

- The nine checks consume these inputs: `contract_predicate(open(DEFAULT_CONTRACT))` (round-39 contract bytes — unchanged), `open(counters[0]).read()` static audits (count-c8.py — unchanged), `git -C repo rev-parse HEAD` and the first counter's `--pin-only` (both keyed to the `--repo` argument, not to LANE), `FIXTURE_REL` resolved against `--repo` (unchanged, repo-relative), and `HANG_FIXTURE` = `LANE/.ufo/waves/round-39/fixtures/hang-after-flush.py`. `main()` defaults `--repo LANE`, `--contract DEFAULT_CONTRACT`, `--counter DEFAULT_COUNTERS`. After the diff, all four constants derive from the file's own location; at the canonical lane path the derived LANE is byte-for-byte the same string as the old hardcode, so a lane-native run is behaviorally identical.
- **The `scratch` check (~line 466-474) does not inspect conform.py at all.** It statically scans each audited COUNTER's source for an `SCRATCH_ROOT` assignment whose segment contains `".ufo"`, `"waves"`, `"round-39"`, `"scratch"` — i.e. it requires count-c8.py:62 (`SCRATCH_ROOT = os.path.join(DEFAULT_REPO, ".ufo", "waves", "round-39", "scratch")`) to stay on-lane; the selftest mutation `"scratch"` flips exactly by moving that counter line to `/tmp/mori-r39-scratch`. Changing conform.py's own SCRATCH_ROOT therefore cannot touch this check, and conversely the check freezes the counter's lane-coupled shape (see Finding 3).
- `head_pin` compares the counter's `head_at_measurement=` output against `git -C <repo> rev-parse HEAD`. It is self-consistent for any repo; the diff changes only WHICH tree supplies the default counter bytes and the default `--repo`. Verdict unchanged; measurement object changed (see §4, run D2).
- `selftest_conjunct` reads `inspect.getsource(selftest)`/`selftest_mutations` of conform.py itself — both functions are untouched by the diff — and the counter bytes — unchanged. `FIXTURE_REL`, `CHECK_NAMES`, `PREDICATE` (the P-C10 sentence), the eleven-mutation table and `MUTATION_CHECK_ALIAS` are untouched.
- Failure mode of a copy placed outside `<tree>/.ufo/waves/round-40/`: the derived LANE is wrong, the first file open (`selftest()`: `open(counter)`; main: `open(contract_path)`) raises OSError, caught by `__main__`'s `except Exception` → `conformance setup error`, exit 2 — before any write (`os.makedirs(SCRATCH_ROOT)` is only reached after the counter opens). Honest rc-2, never a wrong verdict.
- Note: `LANE` uses `abspath(__file__)`, not `realpath` — a symlinked invocation would mis-derive (Finding 5).

## 3. Dynamic answer: runs, all in scratch per operator directive

Scratch `/fast/scratch/hyaku/mori-r51/Mo51RevConformDiff/` (TMPDIR=`…/tmp`, `disk-guard.sh status` rc 0, 595G free). One clone (`git clone --shared` of the lane, then `git repack -a -d` + alternates removal to make it self-contained — lane store 114M, packed copy 100.9M, read-only w.r.t. the lane; no git mutation in the lane or fleet root; `git rev-parse --show-toplevel` = the clone for every fixture operation). Sandbox = bubblewrap 0.13.1 (`--ro-bind /usr /usr --ro-bind /etc /etc --proc /proc --dev /dev`, lane `--ro-bind` or absent as noted, the two on-lane scratch dirs `--bind`-redirected into my scratch so nothing can be written to the lane, TMPDIR/HOME inside scratch).

| run | bytes | mode | lane | result |
|---|---|---|---|---|
| A | data 87e0c374 | `conform.py 87e0c374 --selftest`, native in clone | n/a (tree-local) | eleven `PASS <name> … -> only <name> failed` lines, `CONFORM_SELFTEST pass=11 fail=0`, rc 0 |
| B | data 87e0c374 | `conform.py 87e0c374`, native in clone | n/a | nine checks PASS, `CONFORM=met`, rc 0; `head_pin pin=87e0c374 tip=87e0c374`; `tool_resolve` resolved inside the clone; clone and TMPDIR left clean |
| C | entering aa3af1e | same selftest command, sandboxed, lane ro | visible | **line-for-line identical stdout to A**, `pass=11 fail=0`, rc 0 |
| D2 | entering aa3af1e | same main command, sandboxed, lane ro | visible | nine checks PASS, `CONFORM=met`, rc 0 — but `head_pin pin=b504cb17 tip=b504cb17` (the **lane's** HEAD, not the rev under test, not the clone) and `tool_resolve` resolved inside `/home/vgpnk/…/mori-shokunin` |
| E | entering aa3af1e | main, lane path absent | hidden | `conformance setup error: [Errno 2] No such file or directory: '…/mori-shokunin/.ufo/waves/round-39/contract.md'`, rc 2 |
| E2 | entering aa3af1e | selftest, lane absent | hidden | `conformance setup error: [Errno 2] … '.ufo/waves/round-40/count-c8.py'`, rc 2 |
| F2 | data 87e0c374 | main, lane absent, self-contained clone | hidden | nine checks PASS, `CONFORM=met`, rc 0 |
| F3 | data 87e0c374 | selftest, lane absent, self-contained clone | hidden | `CONFORM_SELFTEST pass=11 fail=0`, rc 0 |
| G | data 87e0c374 | main, lane ro-bound (control for F v1) | visible ro | `CONFORM=met`, rc 0 |

Kill test: entering bytes, selftest SIGTERM'd 8 s in (before `finally`), redirected scratch captured `mori-conform-selftest-uzoh_x4m` inside the mapped `<lane>/.ufo/waves/round-40/scratch/` — the exact mechanism of the residue class C1 arm A targets; on clean exit the work dir is rmtree'd and only the (empty) scratch parent remains.

**Same output?** Verdict-bearing output: YES — A≡C identical line-for-line; B≡D identical on all nine `check … PASS` lines and `CONFORM=met` (detail fields legitimately differ: which tip is pinned and which paths resolve — that difference is the defect being fixed: entering bytes measure the hardcoded lane, D2 proves it by pinning `b504cb17` while asked about rev `87e0c374`). Relocated (lane hidden): NO, by design — entering bytes cannot run at all (E, E2, rc 2; this is the do-nothing control's "one pin fails (conform.py, setup error)"); data bytes are fully green (F2, F3).

Verification gap, resolved and disclosed: my first lane-absent data run (F v1) printed `CONFORM=unmet` with `timeout_state FAIL (exit=2)` — cause was MY `--shared` clone, whose `objects/info/alternates` point into the lane; with the lane absent git cannot read objects (`counter setup error: cannot resolve 87e0c374… in <clone>`, rc 2 — `--pin-only` still worked because rev-parse HEAD needs only refs). After `git repack -a -d` + alternates removal the same command is green (F2/F3). Operational note: a `--shared` clone is not lane-independent; C1's relocated arm correctly uses `--no-local`.

## 4. Honesty of editing a round-40 frozen instrument

Round-40 facts (contract.md, evidence/freeze-r40.txt):
- conform.py v3 is a frozen instrument; freeze pin sha256 = `5025b9664632d01063c11b4f5dadd4f9a063db66d73315d7ed25db8d90b83aaf`. The entering tip's bytes hash to exactly that value (measured); the data commit's bytes hash `7f5174d542bd983552670b06f6cc424b10e53c81e55ecabcdd919f4043bdfa23`. So the working tree no longer matches the r40 pin — that breakage is real and must be named (Finding 1).
- The freeze rule is semantic where it matters: "A change to a **predicate** after this freeze is a new counter version, not an edit", and receipts "remain valid at their frozen commits" (r40 contract; r51 contract §freezes: working-tree drift is measured with `git show <freeze>:<path>`). The P-C10 predicate, the nine checks, the verdict map (0/1/2) and the eleven-mutation table are all byte-unchanged; measured verdicts are unchanged (§3: A≡C, B≡D). The edit changes provenance (where inputs/scratch live), not what the instrument computes — it does not trip any r40 kill rule (the selftest still prints `pass=11 fail=0`, the tally the frozen receipt and SKILL.md:911 pin).
- The edit is the claimed work, not a stealth edit: the frozen round-51 contract routes round-50 spot-check defect 1 to C1 and names `conform.py:69` (the entering hardcode, confirmed at entering line 69) as the defect, and §Separability names `.ufo/waves/round-40/conform.py` as a C1 surface.
- Round-40 receipts stay reproducible: every c10-*/c11-* receipt was measured on the v3 bytes, which remain retrievable at aa3af1ec (and any earlier commit) and hash-verified against the freeze pin. No receipt is invalidated; re-running one requires extracting the frozen bytes (`git show aa3af1ec:.ufo/waves/round-40/conform.py`), the same convention r40 itself used for r39 bytes.
- SKILL.md:911 (r40 conformance row) was NOT edited by this data commit; none of its cells went stale (usage, verdict map, `pass=11 fail=0`, "read-only" all still true — re-verified by runs A/C/F3). SKILL/SHONEN hunks in this diff touch only the pin-check v5 registry row and its 114→119 selftest tally.

Verdict: the edit is honest **iff** it is disclosed with the pin break and the receipt-validity statement — i.e. it must be said in the lesson (and LOG.md), not merely implied by the diff. That disclosure is currently nowhere in the changed files; the diff comment says what changed but not that it breaks freeze-r40.txt's pin for the working tree.

## 5. What the lesson must say

1. Round 51 (C1) modified round-40 frozen instrument `.ufo/waves/round-40/conform.py`: pin `5025b966…` → `7f5174d5…` (blob 71fa5977 → 63cff4a6); scope limited to the `LANE` derivation (hardcoded host path → four `dirname()`s of its own path) and `SCRATCH_ROOT` (lane `round-40/scratch` → `tempfile.gettempdir()`); no predicate, check, verdict-map or mutation-table change.
2. All round-40 receipts remain valid **at their frozen bytes**: sha256 `5025b966…` still matches `git show aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd:.ufo/waves/round-40/conform.py`; any r40 receipt re-run must extract those bytes, per the r40/r51 `git show <freeze>:<path>` convention. Working-tree drift from a freeze pin is henceforth expected for this path and is not tampering.
3. Equivalence evidence: entering and data bytes print identical verdict output on the same inputs (`CONFORM=met`; `CONFORM_SELFTEST pass=11 fail=0`, same eleven arms), measured this wave in a scratch clone (entering under a read-only-lane sandbox so the lane stayed untouched).
4. Why the edit was necessary (observed, not assumed): entering bytes pin and read the hardcoded lane regardless of the tree they run in — run D2 pinned lane HEAD `b504cb17` while asked to judge rev `87e0c374` — and exit 2 setup-error when the lane path is hidden (E, E2); their selftest scratch is written inside the lane and a killed selftest leaves untracked `mori-conform-selftest-*` residue there (reproduced under redirection; also observed accumulating live in the lane, Finding 2). The new bytes are tree-local and TMPDIR-local: `CONFORM=met` / `pass=11 fail=0` with the lane path entirely absent (F2, F3) — the mechanistic explanation of C1's `relocated=met`.
5. Named residual limit: the audited counter `count-c8.py` (r40 frozen bytes, untouched) still hardcodes `DEFAULT_REPO = "/home/vgpnk/Projects/shokunin/mori-shokunin"` (count-c8.py:55; used by its `--repo` default at :388 and its drift-suite scratch at :62/:470-471) — and conform.py's `scratch` check affirmatively REQUIRES that on-lane shape, so the counter could not be de-hardcoded this round without breaking the frozen r40 selftest. The surface pair is therefore hermetic only from conform.py's side; count-c8's own drift-suite main run remains lane-coupled (not exercised by any conform.py check; count-c8 takes no `--selftest` flag).
6. Operational note: `git clone --shared` of the lane is not relocation-safe (alternates reach into the lane; rev resolution fails when the lane vanishes) — relocation tests need `--no-local` clones, as C1 arm B already uses.

## Findings

- MED — `.ufo/waves/round-40/evidence/freeze-r40.txt`: the working tree now violates its conform.py pin (pinned `5025b966…`, working tree `7f5174d5…` at 87e0c374). No lane file records the break; it must be stated in the round-51 lesson/LOG.md with the receipt-validity rule of §5.2, or the next provenance audit reads the r40 instrument as tampered.
- MED — `.ufo/waves/round-40/scratch/` (lane working tree): untracked `mori-conform-selftest-*` residue from entering-bytes selftests is accumulating live — observed `ux20v9vq` (19:51), then `y5k7kzyi`, then `858cf_2r` with up to 9 `counter-*.py` files; `git status --porcelain -uall` counts 9 such paths right now; the dirs are not gitignored (`git check-ignore` rc 1). Detection/report only — not touched by this seat (my runs had the lane ro, absent, or redirected). Root cause is exactly the entering behavior this diff removes; the dirs themselves are leftovers of pre-data/entering-byte runs and should be swept by whoever owns lane hygiene.
- LOW — `.ufo/waves/round-40/count-c8.py:55,62,388` (frozen bytes, not this diff): hardcoded `DEFAULT_REPO` keeps the counter lane-coupled and is *mandated* by conform.py's `scratch` check + `"scratch"` selftest mutation; de-hardcoding requires a future round to change both under its own freeze. Also cosmetic: conform.py's docstring (line ~42) says the counter's scratch parent is under `round-40/scratch` while the check and count-c8 use `round-39/scratch` (pre-existing frozen mismatch).
- LOW — `.ufo/waves/round-40/conform.py:72` (this diff): `LANE` derives from `abspath(__file__)`, not `realpath(__file__)`; a symlinked invocation would mis-derive the lane. Failure mode is rc 2 setup error (honest), never a wrong verdict; canonical execution is the in-tree path.
- LOW — lane residue class generalization: the same kill-residue hazard the diff fixes for conform.py's selftest still exists for any killed count-c8 drift-suite run (`mori-c7-*` under `<lane>/.ufo/waves/round-39/scratch`, r40 frozen bytes); none present at review time (dir empty; mtime churn 19:56:31 observed, consistent with sibling activity).

UNVERIFIED: I did not re-run `count-c1.py` or `mori-pin-check.py` themselves (other seats' items; the C1=met at-data receipt is taken as the L1's reading); I did not run the round-40 survivor-fixture suite against the new bytes (the r40 receipts pin the v3 bytes, which I did not disturb).

Scratch `/fast/scratch/hyaku/mori-r51/Mo51RevConformDiff/` (clone, sandboxes, redirected-scratch captures, TMPDIR) is removed after this report is written; all cited evidence is quoted above.
