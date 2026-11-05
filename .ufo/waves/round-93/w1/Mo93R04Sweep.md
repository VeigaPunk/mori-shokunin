# Mo93R04Sweep — round-93 frozen-artifact sweep (wave w1, 2026-11-05)

Scope: sweep the frozen round-93 artifacts at 6d82b8d7 for round-92 Mistakes classes and
re-check every contract premise at entering revision 7b3fe9d5. Read-only seat: no patch
produced. Work ran in a `--shared --no-checkout` scratch clone checked out at the patch
base (per contract), `TMPDIR` pointed into the scratch; the lane tree was never written —
`git status --porcelain` was byte-identical before and after every step. No tools were
installed or upgraded (operator 2026-10-19 directive: nothing needed).

## 1. Frozen set vs contract

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin show --stat --format=%h 6d82b8d7
6d82b8d7
 .ufo/waves/round-93/contract.md                    | 116 +++++++++++++
 .ufo/waves/round-93/controls-r93.sh                |  87 ++++++++++
 .ufo/waves/round-93/count-c1.py                    | 181 +++++++++++++++++++++
 .ufo/waves/round-93/count-c2.py                    | 108 ++++++++++++
 .../waves/round-93/evidence/c1-derive-entering.txt |  98 +++++++++++
 .ufo/waves/round-93/evidence/controls-r93.txt      |  23 +++
 .../round-93/evidence/measure-c1-entering.txt      |   1 +
 .../round-93/evidence/measure-c2-entering.txt      |   1 +
 8 files changed, 615 insertions(+)
```

- Task framing: `contract.md`, `count-c1.py`, `count-c2.py`, `controls-r93.sh` — all
  present ✓. The freeze is exactly one commit on the entering tip (`git log --oneline
  7b3fe9d5..6d82b8d7` → only 6d82b8d7) and `merge-base --is-ancestor 7b3fe9d5 6d82b8d7`
  → ok ✓.
- **D1 (medium, ordering):** contract Ordering step 1 requires the wave spec
  `w1-spec.json` committed *together* with the frozen set; it is absent from 6d82b8d7 and
  arrived later in d8a9b28c (2026-11-05 06:03:11 -0300, with `w1-dispatch.json` and
  `w1/swarm-registry.json`). Both commits precede the untracked dispatch marker, so the
  spec was committed before dispatch — but not in the freeze commit the contract names.
  Evidence: `git ls-tree -r --name-only 6d82b8d7 -- .ufo/waves/round-93/` lists 8 files
  (no spec); the same at HEAD adds the three wave files.

## 2. Premise re-check at 7b3fe9d5 (QUALITY 196)

- **P1 lesson sentence** — present, wrapped over lines 51–52, unchanged at HEAD
  (`git diff 7b3fe9d5 HEAD -- corpus/lessons/round-92.md` is empty):
```
$ git show 7b3fe9d5:corpus/lessons/round-92.md | sed -n '51,52p'
- Provenance trio lines on 19 knowledge entries (C1 presence). Each `verified-at` names the admission
  commit of its file (`git log --diff-filter=A`); each `recheck` is taken from the entry's own body or
```
- **The 12 file names + entering measurement** — rerunning the frozen counter at the
  entering revision reproduces the frozen receipt `evidence/measure-c1-entering.txt`
  byte-for-byte:
```
$ python3 -I .ufo/waves/round-93/count-c1.py 7b3fe9d5 --repo <clone> --report
C1_REPORT rev=7b3fe9d540c9 trio=98 claim_r92_true=0 files=19 adm_ok=7 adm_fail=12
patched12=0/12 seven_same=7/7 census_rc=0 failures=counter-semantics-r78.md ac=2360cc3b ...
```
  All 12 admission hashes in `evidence/c1-derive-entering.txt` (MISMATCH rows:
  2360cc3b counter-semantics-r78, 6a230c4b counter-win-r77, 5be89432 drift-pin-r10,
  c89e5b6e execution-binding-r89, 2a4213bf kernel-v7.3-recheck-r53, 3da84149
  lane-silence-r2, 71107662 rotation-receipt-grammar-r76, dc50c80b rotation-schedule-r74,
  32132cfb rotation-series-r75, cffb37ef selftest-flake-r9, 9738f1ab surfaces-r8,
  3627fac0 workstate-win-r71) equal the counter's live `git log --diff-filter=A` output;
  the 7 OK rows are exactly the seven files the contract requires to stay unchanged ✓.
- **The 3 tool names** — `tools/mori-blind-check.sh`, `tools/mori-misroot-sweep.py`,
  `tools/mori-round17-context-check.py` (count-c2.py:28–32; same three in the deletion and
  rename controls of controls-r93.sh:52,62–63); C2 rerun at 7b3fe9d5 reports `tools=3/3
  selftests=3/3` ✓.
- **18 vgpnk bytes** — the contract's grep gives exactly 12 lines in the three files:
```
$ git grep -n vgpnk 7b3fe9d5 -- tools        # 12 lines: blind-check.sh:247 (1),
# misroot-sweep.py:6,20,355 (3), round17-context-check.py:39,116,118,508,535,557,559,565 (8)
```
  Independent byte count over `git archive 7b3fe9d5 tools`:
```
tools/mori-blind-check.sh home_lits=1 vgpnk=1
tools/mori-misroot-sweep.py home_lits=3 vgpnk=3
tools/mori-round17-context-check.py home_lits=14 vgpnk=14
TOTAL home_literals=18 vgpnk_refs=18
```
  The fourth file `tools/mori-round17-jj-regressions.py:1903-1905` has only
  `<case>/home/...` case-relative paths and contributes 0 to both counts (the `>`
  lookbehind excludes them), exactly as P2 states ✓. C2 rerun at 7b3fe9d5:
```
C2_REPORT rev=7b3fe9d540c9 home_literals=18 vgpnk_refs=18 tools=3/3 selftests=3/3 census_rc=0
```
  — identical to the frozen receipt `evidence/measure-c2-entering.txt` ✓.
- **The base** — `git rev-parse 7b3fe9d5^{commit}` →
  `7b3fe9d540c98b8b0390a0f9bbe78de4341092a5` (full hash matches the contract) ✓.
- QUALITY 196/197 exist at 7b3fe9d5 (`corpus/QUALITY.md:2253`, `:2255`; 197 names the
  same three tools and plans their repair for round 93) ✓.

## 3. Counter hygiene (round-92 classes)

- `/tmp` literals: none functional. Only hits are the docstring phrase "no /tmp literal"
  (count-c1.py:26, count-c2.py:18). Writes go to
  `tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR"))` (count-c1.py:131,
  count-c2.py:65) ✓.
- Imports: argparse, os, re, subprocess, sys, tarfile, tempfile in both counters —
  Python standard library only; no third-party imports ✓.
- **D2 (medium-low, the round-92 class inside the round's own tooling):** both counters
  hardcode the fleet root — count-c1.py:39 and count-c2.py:39
  `CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"`. This is exactly
  the QUALITY 197 class C2 repairs under `tools/`, replicated in the verification
  tooling itself; on any host with a different fleet root the census call fails and both
  claims report unmet regardless of the data. Outside the C2 predicate scope (tools/
  only), so it does not unmeet the claim; flagging for the L1.
- **D3 (low, predicate-sentence drift):** count-c2.py:10-11 states the home regex as
  `/home/[a-z_][a-z0-9_-]*/` (no lookarounds, trailing slash), while the compiled regex
  (count-c2.py:38) and contract P-C2 use
  `(?<![>\w])/home/[a-z_][a-z0-9_-]*(?![a-zA-Z0-9_.-])`. The contract requires the
  sentence "same in count-c2.py, the receipt and this line"; the docstring variant is
  weaker (it would count case-relative `<case>/home/x/` paths). Compiled behavior is the
  contract's, so measurements are unaffected.

## 4. controls-r93.sh

- `set -u` at controls-r93.sh:6; executed end-to-end with `TMPDIR=<scratch>`: all 7
  controls ran, every verdict UNMET with rc=1 as designed, script rc=0 (~25 s). Verdict
  lines are byte-identical to the frozen receipt `evidence/controls-r93.txt`; only the
  fresh fixture commit hashes differ (expected for new clones). Key lines from my run:
```
C1 do-nothing:    C1=unmet trio=98 adm_ok=7 adm_fail=12 patched12=0  checks_failed=admission,patched12 rc=1
C1 text-only:     C1=unmet adm_fail=12 (lesson reword, data unchanged)  rc=1
C1 deletion:      C1=unmet trio=86 adm_fail=12  rc=1
C1 forgery:       C1=unmet adm_ok=19 patched12=11  checks_failed=patched12  rc=1
C2 do-nothing:    C2=unmet home_literals=18 vgpnk_refs=18  rc=1
C2 deletion:      C2=unmet tools=0 selftests=0/3  rc=1
C2 rename:        C2=unmet home_literals=18 vgpnk_refs=0  rc=1
```
- Fixtures are all clones: the only repo-creation call is
  `git clone -q --shared --no-checkout` (controls-r93.sh:18); there is no `git init`
  anywhere in the script ✓.
- No lane writes: `$LANE` is used only as a clone source and a read-only counter
  `--repo`; the script writes only `$OUT` and `$TMPDIR/mori-r93-controls/**`; empirically
  `git status --porcelain` of the lane is identical before/after the full run ✓.
- **D4 (low, dead weight):** controls-r93.sh:23 defines
  `GIT=(git -c user.name=mori-shokunin -c user.email=mori@shokunin.local)` which is never
  used — `commit_fixture` (:22) inlines the same flags. Harmless under `set -u`; delete
  or use it.

## 5. Registry census

The census command lives in fleet-root `CORPUS.md:131-135` (`grep -cE
'^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`, run from the lane root).
Note: the task text says "corpus/CORPUS.md", but no `CORPUS.md` exists anywhere in the
lane tree at 7b3fe9d5 or HEAD (corpus/ has QUALITY.md, README.md, SOURCES.md, evidence,
knowledge, lessons); the rules doc is at the fleet root. Pointers to CORPUS.md in-lane
(e.g. SCORECARD.md:4707) resolve only against the fleet root.

```
rows at 7b3fe9d5: 393
rows at HEAD:     393
rows in worktree: 393
```

No rows appended since the entering revision ✓. Corroborated by
`git diff --stat 7b3fe9d5 HEAD -- corpus/SOURCES.md` (empty) and by the counters'
`sources-census.sh validate --file` exiting 0 at 7b3fe9d5.

## Observations (not round-93 defects)

- `count-c1.cover` (60734 B) and `count-c2.cover` (58288 B) are TRACKED binary coverage
  pickles at the lane root (present at 7b3fe9d5 and HEAD) embedding host paths (e.g.
  `/home/vgpnk/.../round-61/count-c1.py`) — old round-61 debris; QUALITY-197-adjacent but
  outside the tools/ scope of C2.
- Lane worktree is mid-flight: `M corpus/QUALITY.md` plus untracked w1 markers — L1's
  business, untouched by this seat.
- The round-92 lesson correction has not started in the lane (round-92.md identical
  between 7b3fe9d5 and HEAD) — consistent with "appended, not edited in place".

## Checks run / not run

Run: (1) frozen-set stat vs contract; (2) all five premise literals at 7b3fe9d5 (lesson
sentence, 12 file names via counter rerun + derivation cross-check, 3 tool names, 12-line
grep and 18/18 byte count, base hash + ancestry) plus both counter reruns reproducing
both frozen receipts; (3) /tmp-literal and stdlib-import greps of both counters;
(4) controls-r93.sh executed under `set -u` with clone-only fixtures and a lane-untouched
diff check; (5) official census at base/HEAD/worktree. Counter reruns and the controls
run also verify the census validator exit at the entering revision.
Not run: post-landing checks (equivalence receipt `evidence/equivalence-c2.txt` and the
after-receipts do not exist yet — landing has not happened); no w1 seat reports reviewed
(out of scope for this seat).
