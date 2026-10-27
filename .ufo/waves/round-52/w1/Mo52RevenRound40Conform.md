# Mo52RevenRound40Conform — round-40 `conform.py` in-place edit: bytes, receipts, pins, successor-freeze draft

- Seat: Mo52RevenRound40Conform (revenger, round 52 wave `w1`, leaf — no subagents).
- Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin` (git backend; every read via read-only git).
- Scratch: `/fast/scratch/hyaku/mori-r52/Mo52RevenRound40Conform/` (one clone, TMPDIR, outputs; removed after this
  report — see §8).
- LSP: **no `lsp` device is mounted in this seat** (`read xd://lsp` → "No such tool: xd://lsp"). Every
  definition/call-site statement below is text search plus execution; recorded as unavailability, not presented as
  semantic proof.
- Tools installed: none.

Assignment: round-51 closure D-e — `.ufo/waves/round-40/conform.py` was edited in place so it no longer matches
`.ufo/waves/round-40/evidence/freeze-r40.txt` (`5025b966…` → `7f5174d5…`). Reconstruct the frozen-vs-current diff, the
commit history, which receipts were measured with which bytes, and whether any SKILL.md pin or QUALITY row names a
tally only the edited bytes print; draft the successor-freeze record text.

## 0. Answer

1. **The edit is one 5-line hunk** at the file's header: the hardcoded lane literal and the lane-relative selftest
   scratch root are replaced by a four-`dirname()` derivation from `__file__` and `tempfile.gettempdir()`; the file
   grows 805 → 808 lines, 36401 → 36650 bytes, blob `71fa5977…` → `63cff4a6…`, sha256 `5025b966…` → `7f5174d5…`.
   No predicate, check, verdict map, mutation table, counter, contract or fixture byte changes.
2. **History is two commits, both in the lane's linear log**: `265a955c` (2026-10-24 02:47:29, the frozen bytes) and
   `87e0c374` (2026-10-26 19:37:45, the edit — round-51's *data* commit, described in its subject as "conform.py path
   fix"). Nothing else ever wrote the path. `git diff 4f266ef2 8524904 -- .ufo/waves/round-40/` is empty, so round
   52's data commit did not touch it.
3. **Every round-40 receipt predates the edit and was measured with the frozen bytes** (mtimes 2026-10-24 02:41–04:23:
   13 `c10-after-*` — 12 name the tracked path, 1 names the gutted conjunct mutant copy `conform-v3-conjunct-gutted.py`
   —, 11 `c10-red-*` which run the round-39 extracted bytes, and `c10-parity`, which runs only counters). Post-edit
   executions of the r40 tally exist only in round-51 wave reports (pin-check `--rev` runs and two executed equivalence
   reports), never as round-40 receipts.
4. **No SKILL.md pin and no QUALITY row names a tally only the edited bytes print.** Executed both byte sets on the same
   inputs in my clone: `CONFORM_SELFTEST pass=11 fail=0` is printed byte-identically by both (diff empty), and
   `CONFORM=met` by both. `SKILL.md:911` (the only pin naming an r40 tally) is satisfied by either. What *is*
   exclusive to the edited bytes is the pin staying green when the measured tree is not the host lane: measured, the
   frozen bytes silently pinned the real lane's HEAD `075436b1` while asked about rev `4f266ef2` (`CONFORM=met`), and
   round-51 measured rc=2 setup error off-host; the edited bytes pinned `4f266ef2` = the rev asked (rc 0).
5. **The freeze record has no successor slot**: `freeze-r40.txt` still lists `5025b966…`, the working tree is
   `7f5174d5…`, and round 52's own `evidence/freeze-sha256.txt` does not include the path. Draft successor-freeze text
   in §7.

## 1. Reconstructed contract (what the file is, and what its freeze promised)

`.ufo/waves/round-40/conform.py` is the round-40 C10 conformance gate ("conform v3", 805 lines): nine checks
(`predicate`, `head_pin`, `tool_resolve`, `bounded_reads`, `timeout_scope`, `drain_bind`, `timeout_state`, `scratch`,
`selftest_conjunct`) over a counter of record (`count-c8.py`) and a contract (`round-39/contract.md`), exit 0 `met` /
1 `unmet` / 2 setup error, plus `--selftest` (eleven textual mutations, each must flip exactly its own check).

Frozen contract, quoted (`git show 265a955c:.ufo/waves/round-40/contract.md:7-13`):

> … Pins are recorded in `evidence/freeze-r40.txt` (sha256 over the frozen paths). A change to a predicate after this
> freeze is a new counter version, not an edit. The round-39 instruments under `.ufo/waves/round-39/` stay byte-frozen
> at their commits; their receipts remain valid at their frozen commits. …

`evidence/freeze-r40.txt` (lines 1-9; unchanged since `d72ac167`, 2026-10-24 04:46:03):

```
freeze-r40: sha256 over the round-40 frozen instrument paths
pinned: 2026-10-24T05:46:06Z by L1 mori-r40 attempt 1 (resumed)
note: the prior launch died before persisting this receipt; before-receipts
      run committed bytes extracted via 'git show bb1f2457:<path>' (see
      fixtures/extracted/), so before-controls are measured at entering bytes.

6514914885e6a1249ed7903931b9734a55e828275121353c2727348eae504a8d  .ufo/waves/round-40/contract.md
4e4d50eb1e96d947f0e9d2ab25a13b2b8c33963f216f3be43060a3348702f6da  .ufo/waves/round-40/count-c8.py
5025b9664632d01063c11b4f5dadd4f9a063db66d73315d7ed25db8d90b83aaf  .ufo/waves/round-40/conform.py
```

Last-known-good invariant (re-measured this seat):

```
$ git -C <lane> show 265a955c:.ufo/waves/round-40/conform.py | sha256sum
5025b9664632d01063c11b4f5dadd4f9a063db66d73315d7ed25db8d90b83aaf  -
$ sha256sum <lane>/.ufo/waves/round-40/conform.py
7f5174d542bd983552670b06f6cc424b10e53c81e55ecabcdd919f4043bdfa23  .ufo/waves/round-40/conform.py
$ git -C <lane> rev-parse 265a955c:.ufo/waves/round-40/conform.py 87e0c374:.ufo/waves/round-40/conform.py
71fa59774c676267224a7845e416fd84d19a4e96
63cff4a61b2d585270e9bbb6e07f7f16faea2da8
$ git -C <lane> cat-file -s <blob>   # 36401 (frozen) / 36650 (current)
$ git -C <lane> status --porcelain .ufo/waves/round-40/conform.py   # empty: HEAD == working tree
$ git -C <lane> log --format='%H %ci' -- .ufo/waves/round-40/conform.py
87e0c374537557754bf71dd68036ded3ddc6699c 2026-10-26 19:37:45 -0300
265a955cc67be4eae97d2dc5a9338a25f31eb29b 2026-10-24 02:47:29 -0300
```

The same bytes hold at the round-52 entering tip: `git show 4f266ef2:.ufo/waves/round-40/conform.py | sha256sum` →
`7f5174d5…`. Invariant that broke: the *first* pin in `freeze-r40.txt` whose subject is an executable instrument (the
`conform.py` line) no longer describes the working tree, and no file in the lane records the successor pin (round-51's
lesson and the round-51 verifier spot-check D-e say the edit happened; neither records a replacement sha in a freeze
file). Round 52's `evidence/freeze-sha256.txt` (21 entries, read in full) lists only round-52 files — no round-40 path.

## 2. The diff, verbatim

`diff -u <(git show 265a955c:.ufo/waves/round-40/conform.py) <lane>/.ufo/waves/round-40/conform.py` (exit 1):

```
--- /dev/fd/63	2026-10-26 21:14:10.293454255 -0300
+++ .ufo/waves/round-40/conform.py	2026-10-26 19:37:14.160580850 -0300
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
 # The counter's predicate of record is frozen in the round-39 contract
 # (P-C7); the round-40 contract carries P-C10/P-C11 for the new instruments.
```

Line map: frozen `LANE` = `:69`, `SCRATCH_ROOT` = `:70`; current comment `:69-71`, `LANE` = `:72`, `SCRATCH_ROOT` =
`:73`. (Round-50 reports cite `:69`/`:70` and `:743`/`:765` from the frozen bytes; those line numbers are now off by
three from `:735`/`:746` onward.) Four constants and one main body derive from the changed pair (`DEFAULT_CONTRACT:77`,
`FIXTURE_REL:78`, `HANG_FIXTURE:79`, `DEFAULT_COUNTERS:74`, `--repo` default `LANE`, `os.makedirs(SCRATCH_ROOT)` +
`mkdtemp(dir=SCRATCH_ROOT)` inside `selftest()`); the nine checks and `selftest_mutations` body do not.

## 3. Which receipts were measured with which bytes

| receipts | file times | bytes in force | verdict |
|---|---|---|---|
| `.ufo/waves/round-40/evidence/c10-after.txt` + `c10-after-{cond,decoy,divzero,inf,multicounter,second-popen,selftest,shadow-neg,shadow-none,tuple,underscore}.txt` (12 files; each `command:` line names `python3 .ufo/waves/round-40/conform.py 265a955c…`) | 2026-10-24 02:47–04:23 | frozen `5025b966…` | valid; frozen bytes retrievable |
| `.ufo/waves/round-40/evidence/c10-after-conjunct.txt` (command names `fixtures/generated/conform-v3-conjunct-gutted.py`, the round-41-pinned mutant copy, not the tracked path) | 2026-10-24 04:23 | mutant copy `20e32422…` derived from the frozen bytes | unaffected by either tracked byte set |
| `.ufo/waves/round-40/evidence/c10-red-{cond,conjunct,decoy,divzero,inf,multicounter,second-popen,shadow-neg,shadow-none,tuple,underscore}.txt` (11 files; `command:` names `fixtures/extracted/conform-v2-r39.py`) | 2026-10-24 02:41–04:23 | round-39 bytes `fe0be179…`, unaffected by the edit | valid |
| `.ufo/waves/round-40/evidence/c10-parity.txt` | 2026-10-24 02:45 | counter bytes only (`count-c7`/`count-c8`) | unaffected |
| `.ufo/waves/round-47/evidence/after-c1-v1-frozen.txt:31`, `after-c1-v2.txt:31` | 2026-10-25 17:06 | frozen `5025b966…` | `pin line=911 … state=match pinned='pass=11 fail=0' observed='pass=11 fail=0' rc=0 cmd='python3 .ufo/waves/round-40/conform.py af2250d8… --selftest'` |
| `.ufo/waves/round-50/evidence/a2-pin-check-at-landed.txt:36` | 2026-10-26 10:53 | frozen `5025b966…` | same shape, `cmd='… bae8656e… --selftest'`, match rc=0 |
| round-51 wave reports `w1/Mo51ExecPinCheckLaneRev.md:38,56,160` | 2026-10-26 ≥19:37 | **edited** `7f5174d5…` (rev `87e0c374`) and frozen (rev `aa3af1ec`) | edited: match rc=0 at both host and off-host; frozen off-host: `state=mismatch … observed=None rc=2 … class=env` (`:109,141`) |
| round-51 reports `w1/Mo51ExecRound40Reexec.md`, `w1/Mo51RevConformDiff.md` | 2026-10-26 ≥19:37 | both byte sets, in `--no-local` clones / bwrap | 13/13 receipts AGREE under each byte set; two divergence classes named (§4) |

No round-40 receipt was re-measured with the edited bytes; no receipt cites the new sha. There is therefore no
receipt-vs-bytes ambiguity: **r40 receipts ⇒ frozen bytes; r51 pin receipts ⇒ edited bytes**. The round-51 pin-check
`--selftest` receipt (`.ufo/waves/round-51/evidence/selftests/mori-pin-check.txt`) does not execute the r40 command
(grep for `line=911`/`conform`: 0 hits) — it exercises pin-check's own arms only.

## 4. Executed equivalence and divergence (my own measurement)

Setup (one clone, per the seat limit): `git clone --shared <lane> clone`, `checkout 4f266ef2`, then
`git repack -a -d` + remove `.git/objects/info/alternates` because a `--shared` clone cannot resolve `^{commit}`
while the lane is shadowed (`counter setup error: cannot resolve 4f266ef2… ; rc=2` reproduced before the repack —
the same trap round-51 recorded). `git -C clone rev-parse --show-toplevel` = the clone. `TMPDIR` = seat scratch.
Frozen bytes extracted with `git show 265a955c:… > bytes/conform-5025.py` (sha `5025b966…` verified). bwrap 0.13.1
provides the lane path.

R1 — edited bytes, native clone (`clone/.ufo/waves/round-40/conform.py`, sha `7f5174d5…`):

```
$ python3 .ufo/waves/round-40/conform.py 4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d
… (P-C10 predicate line) …
check predicate          PASS (exit=0 equal=True)
check head_pin           PASS (pin=4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d tip=4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d)
check tool_resolve       PASS (exit=0 resolved=/fast/scratch/hyaku/mori-r52/Mo52RevenRound40Conform/clone/.ufo/waves/round-39/fixtures/witness-summary-only-live.txt)
check bounded_reads      PASS (count-c8.py: bounded=[] value=[])
check timeout_scope      PASS (count-c8.py: bounded=[] value=[])
check drain_bind         PASS (count-c8.py: violations=[])
check timeout_state      PASS (exit=1 timeout_reason=True pass=False)
check scratch            PASS (count-c8.py: mkdtemp_dir=True root=True)
check selftest_conjunct  PASS (count-c8.py: honest_comm=[] strips=6 detected=6 anchor=True entry_live=True)
CONFORM=met
rc=0
```

R1b — same bytes, `--selftest` (rc 0): eleven `PASS <name> … -> only <name> failed` lines, ending
`CONFORM_SELFTEST pass=11 fail=0`.

R2 — frozen bytes (`5025b966…`) run from the clone with the lane path **bound to the clone**
(`bwrap --dev-bind / / --bind clone <lane> --chdir <lane> …`):

```
rc=0
diff R1-main R2-main:
4c4
< check tool_resolve       PASS (exit=0 resolved=/fast/scratch/…/clone/.ufo/waves/round-39/fixtures/witness-summary-only-live.txt)
---
> check tool_resolve       PASS (exit=0 resolved=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-39/fixtures/witness-summary-only-live.txt)
```

Selftest under R2: `diff R1-selftest R2-selftest` → empty; `CONFORM_SELFTEST pass=11 fail=0`, rc 0. So on identical
inputs the two byte sets differ **only** in the absolute path printed inside the always-PASS `tool_resolve` detail;
the tally the pin names is identical.

R3 — the divergence that the edit exists to remove. Frozen bytes in the clone, real lane **read-only bound** at its own
path, asked about rev `4f266ef2`:

```
$ bwrap --dev-bind / / --ro-bind <lane> <lane> --chdir clone … python3 .ufo/waves/round-40/conform.py 4f266ef2…
check head_pin           PASS (pin=075436b1346ca659afb8be7a46f0e67e4170aa83 tip=075436b1346ca659afb8be7a46f0e67e4170aa83)
check tool_resolve       PASS (exit=0 resolved=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-39/fixtures/witness-summary-only-live.txt)
CONFORM=met
rc=0
```

`075436b1` is the **lane's** HEAD, not the revision the command named (`4f266ef2`); the frozen bytes measured the
hardcoded lane and reported `met`. Edited bytes, same namespace, same arguments:

```
check head_pin           PASS (pin=4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d tip=4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d)
check tool_resolve       PASS (exit=0 resolved=/fast/scratch/…/clone/.ufo/waves/round-39/fixtures/witness-summary-only-live.txt)
CONFORM=met
rc=0
```

Interpretation (observed, not inferred): the frozen gate takes its repo, contract, counter and fixture from the
host literal, so in any tree that is not the host lane it either measures the host lane (silently, rc 0) or exits 2
when the host path is absent — round-51 measured the rc=2 side (E, E2: `conformance setup error: [Errno 2] …`), and
its `class=env` pin mismatch off-host is the same fact seen through pin-check v5's clone execution. The edited gate is
tree-local; with the lane path entirely absent it is fully green (round-51 F2/F3), which my R1 reproduces with the
lane only present read-only.

Write discipline: R3 showed the lane's `git status --porcelain --ignored` count 58 → 59 and round-40 scratch entry
count 3 → 3 across my own runs (21:19:22 / 21:19:29). The one new entry is the **peer** directory
`.ufo/waves/round-39/scratch/`, whose children appeared at 21:19:43, 21:19:54, 21:20:18, 21:20:22, 21:20:26 — i.e.
after my last command — while three `round-39/conform.py … --selftest` processes and two `round-40/conform.py
8524904… --selftest` processes from other seats were visible in `ps`. None of my three runs can write there: the
frozen run was under a read-only lane bind, and the edited run's `SCRATCH_ROOT` is `tempfile.gettempdir()` with
`TMPDIR` in my scratch. I did not attribute the residue to a seat (UNVERIFIED which one).

## 5. Pins and QUALITY rows that touch this file

Full text search over `SKILL.md`, `SHONEN.md`, `corpus/QUALITY.md`, `corpus/README.md` for `conform` / `CONFORM`:

- **`SKILL.md:911`** — the only pin that names an r40 tally: entry
  `python3 .ufo/waves/round-40/conform.py <rev> [--counter PATH]... [--selftest]`, self-test cell
  `` `--selftest` → `CONFORM_SELFTEST pass=11 fail=0` ``, pinned values "contract P-C10 bytes; scope-aware timeout
  resolution …; per-Popen `communicate` drain binding with consumed result", write scope "read-only". All three cells
  are still true of the edited bytes; the row was not edited by `87e0c374` (that commit touched the pin-check row and
  `SHONEN.md` only).
- **`QUALITY.md:885`** pins round-38 `conform.py --selftest` → `pass=6 fail=0`; **`QUALITY.md:898-903`** (criterion 111)
  is the *runnable-form* note for that command; **`QUALITY.md:933`** (criterion 114) pins round-42 `conform.py`.
  Round-52's C1 counter runs these today and they pass (`evidence/c1-at-data.txt:10`:
  `item living corpus/QUALITY.md:885 … got=superseded state=ok`; `corpus/README.md:728 … pass=9 fail=0 rc=0`). None
  names an r40 tally.
- **`QUALITY.md:115`** (criterion 115) contains the sentence "The r40 `conform.py` hardcoded `LANE` is the pointer,
  not the evidence." Its `Check:` command is a round-43 `count-c1s.py` run and is unaffected; the rationale sentence
  is now **past-tense-false at HEAD** (the file no longer hardcodes `LANE`). See Findings (LOW).
- **`QUALITY.md:127`** (criterion 137) lists lane-resident writers as out of scope and names `.ufo/waves/round-39/
  conform.py` and round-48/49 `count-c1.py` — consistent with what I observed live (§8), and it does not name
  round-40 `conform.py`, correctly, for scratch (the edited file writes TMPDIR).
- `SHONEN.md`: no CONFORM pin (its third box pins `mori-pin-check.py --selftest` 119/119 and
  `mori-unlanded-check.py --selftest` 17/17, both round-51 receipts). Nothing to re-score.

**Answer to the tally question: no.** `CONFORM_SELFTEST pass=11 fail=0` and `CONFORM=met` are printed by both byte
sets on the same inputs (R1 vs R2: identical selftest stdout; main stdout differs only inside the `tool_resolve`
detail path, which no pin quotes). The asymmetry is provenance, not tally: only the edited bytes keep `SKILL.md:911`
rc=0 when the pin is executed against a clone (pin-check v5's execution model) or any tree other than the host lane.

## 6. Named limits (routed for round 53; not proposed as fixes here)

1. `freeze-r40.txt` is a flat sha256 list with no succession grammar; `mori-pin-check.py` recognises `--` digest pins
   and tally pins but has no class for "this frozen path has a successor sha at commit X". A successor record is
   therefore prose that only a human/verifier can check (this seat's §7 draft).
2. `head_pin` cannot detect substitution: it compares the counter's `--pin-only` output (repo HEAD) against
   `git -C repo rev-parse HEAD`, both from the same repo, so R3's frozen run "passed" while measuring a different
   tree than the rev named on the command line. The check would need the *requested* rev in the comparison; frozen
   bytes make that impossible without editing them.
3. The `scratch` check *requires* each audited counter's `SCRATCH_ROOT` to contain the literal segments `.ufo waves
   round-39 scratch` (`conform.py:467-473` frozen / `:470-476` current), so `count-c8.py:55,62` stay lane-coupled by
   design and the r40 selftest's `scratch` mutation anchors on the counter, not on `conform.py`. De-hardcoding the
   counter would break the frozen mutation table — a successor-version change, not an edit.
4. The edited `LANE` uses `abspath(__file__)`, not `realpath`; a symlinked invocation mis-derives and fails closed as
   rc 2 (already a LOW finding in round-51's review, still true).
5. The lane still has no machine check that a frozen instrument's working-tree sha equals its freeze line. Round-52's
   C1 counter runs living pins, not frozen-path sha comparisons; `freeze-r40.txt` is never validated. My own probe
   (one `sha256sum` against one freeze line) had to be written by hand.

## 7. Draft successor-freeze record text (fenced, for the L1 to land — not landed by this seat)

Proposed carrier: append to a round-52 successor-freeze file (e.g.
`.ufo/waves/round-52/evidence/freeze-successor-r40-conform.txt`) and cite it from the round-52 lesson; do **not** edit
`freeze-r40.txt` (it is a dated record).

```
freeze-successor r40-conform v3 maintenance revision (recorded round 52, wave w1)
supersedes: the .ufo/waves/round-40/conform.py line of .ufo/waves/round-40/evidence/freeze-r40.txt
recorded-by: Mo52RevenRound40Conform (revenger), evidence below re-measured 2026-10-26

frozen (round 40, still authoritative for every round-40 receipt)
  5025b9664632d01063c11b4f5dadd4f9a063db66d73315d7ed25db8d90b83aaf  .ufo/waves/round-40/conform.py
  blob 71fa59774c676267224a7845e416fd84d19a4e96, 805 lines, 36401 bytes
  at 265a955cc67be4eae97d2dc5a9338a25f31eb29b and every earlier commit; extract with
  'git show 265a955c:.ufo/waves/round-40/conform.py'
successor (in-tree since the round-51 data commit; no longer matches the r40 line)
  7f5174d542bd983552670b06f6cc424b10e53c81e55ecabcdd919f4043bdfa23  .ufo/waves/round-40/conform.py
  blob 63cff4a61b2d585270e9bbb6e07f7f16faea2da8, 808 lines, 36650 bytes
  at 87e0c374537557754bf71dd68036ded3ddc6699c and later (4f266ef2, 8524904, 075436b1 verified)

scope of the change (5+/2-, header only): frozen :69-70 -> current :69-73
  LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"        -> four dirname() of abspath(__file__)
  SCRATCH_ROOT = os.path.join(LANE, ".ufo", "waves",
                              "round-40", "scratch")           -> tempfile.gettempdir()
unchanged bytes at both revisions: count-c8.py 4e4d50eb..., round-39/contract.md 65149148..., every fixture and
generated mutant; the P-C10 predicate, the nine checks, the verdict map (0/1/2) and the eleven-mutation table.

receipt validity
  receipts dated before 87e0c374 (round-40 c10-after-*, c10-red-*; round-47 pin receipts; round-50
  a2-pin-check-at-landed) were measured with 5025b966... and remain valid at their frozen bytes.
  receipts dated after 87e0c374 that execute the r40 tally (round-51 pin-check --rev runs) were measured with
  7f5174d5...; SKILL.md:911 is satisfied by both, measured.

equivalence (executed 2026-10-26, both byte sets, clone at 4f266ef2, TMPDIR in scratch)
  CONFORM=met                         rc=0  under both bytes on the same tree; stdout differs only in the
                                            absolute path inside the always-PASS tool_resolve detail
  CONFORM_SELFTEST pass=11 fail=0     rc=0  byte-identical stdout under both bytes
behaviour that differs, and is the reason for the change
  frozen bytes asked about rev 4f266ef2 with the real lane read-only bound printed
  'head_pin PASS (pin=075436b1... tip=075436b1...)' CONFORM=met rc=0 — the host lane's HEAD, not the rev named
  (silent substitution); off-host or under --tmpfs <lane> the same bytes exit 2 'conformance setup error'.
  edited bytes print 'head_pin PASS (pin=4f266ef2... tip=4f266ef2...)' rc=0, and stay green with the lane path
  absent (round-51 F2/F3).

standing rules
  1. no further in-place edit of .ufo/waves/round-40/conform.py; a later change lands as a copy (successor path)
     with its own freeze line, and this record is superseded append-only.
  2. a replay of a round-40 receipt extracts 5025b966... via 'git show 265a955c:...' before running it.
  3. working-tree drift from the freeze-r40.txt conform line is expected from 87e0c374 on and is not tampering;
     count-c8.py's line in freeze-r40.txt is unchanged and still binds.
```

## 8. Custody

- Scratch `/fast/scratch/hyaku/mori-r52/Mo52RevenRound40Conform/` (clone 433 MB after self-containment, TMPDIR,
  `out/`, `bytes/`), removed after this report was written. `scripts/hyaku/disk-guard.sh status` at start:
  `/fast/scratch/hyaku 25% use, 606.1G free`. Nothing cited depends on the scratch bytes: every quoted output is in
  this report, and every input is re-derivable with `git show` from the lane.
- Writes: this report only. No fleet-root or lane tracked file written; no git/jj mutation in the lane or fleet root
  (all git use read-only: `log`, `show`, `rev-parse`, `cat-file`, `status`, `diff`, `clone`); the one clone is in
  scratch with `rev-parse --show-toplevel` verified before any work; the single `git checkout -- .ufo/.../conform.py`
  and `git repack`/`alternates` removal ran **inside the clone** only.
- Host reads: none beyond filesystem/git. No sysctl, cgroup, journal or systemd command. No tool installed.
- Live co-tenant observation (detection only, not mine): lane `.ufo/waves/round-39/scratch/` accumulated
  `mori-conform-selftest-*` dirs at 21:19:43–21:20:26 with three `round-39/conform.py 4f266ef2 --selftest` and two
  `round-40/conform.py 8524904 --selftest` processes from other seats in flight (`ps -eo pid,etimes,args`); the
  round-40 pair write TMPDIR under the edited bytes, the round-39 writers still target the lane.

## Findings

- **HIGH — `.ufo/waves/round-40/evidence/freeze-r40.txt:9` vs `.ufo/waves/round-40/conform.py:72-73`.** The freeze
  line still names `5025b966…`; the tree has been `7f5174d5…` since `87e0c374`, and no lane file records a successor
  sha for this path (round-52 `evidence/freeze-sha256.txt` does not list it). A provenance audit that trusts the
  freeze reads the instrument as tampered; the §7 draft is the missing record.
- **MED — `.ufo/waves/round-40/conform.py:72-73` (successor bytes).** Off-tree execution is safe but the old bytes'
  failure mode is silent, not loud: my R3 run shows a `CONFORM=met`, rc=0 verdict for rev `4f266ef2` computed against
  lane HEAD `075436b1`. Any receipt re-run with the frozen bytes from a non-lane cwd must be rejected as measuring the
  wrong tree; the r40 receipts themselves are unaffected because they were produced in the lane.
- **MED — `corpus/QUALITY.md:115`.** Criterion 115's rationale sentence ("The r40 `conform.py` hardcoded `LANE` is the
  pointer, not the evidence.") is now false at HEAD; its `Check:` command is unaffected. House rule is supersession by
  a later row, never an in-place rewrite, so this needs an appended supersession line (or an erratum) naming
  `87e0c374`.
- **LOW — `SKILL.md:911`.** Still correct (measured under both byte sets: `pass=11 fail=0`, `CONFORM=met`, read-only),
  but its command path now resolves its inputs from its own location; the row's "pinned values" cell does not say so.
  No re-score needed; a note in the successor record is enough.
- **LOW — `.ufo/waves/round-40/conform.py:467-476` (frozen and current, unchanged by the edit).** The `scratch` check
  freezes the audited counter's lane-coupled `SCRATCH_ROOT` literal, so `count-c8.py:55,62` cannot be de-hardcoded
  without a successor counter version; the hermetically-swept surface is one-sided (the checker, not the counter).
- **LOW — lane `.ufo/waves/round-39/scratch/`.** Live `mori-conform-selftest-*` residue from other seats'
  `round-39/conform.py --selftest` runs (four dirs 21:19:43–21:20:26; `ps` evidence above). Round-51's C1 arm A
  already scopes this as `kill_residue`; it is not produced by the edited r40 bytes and is not mine to delete.
- **LOW — `.ufo/waves/round-40/conform.py:72`.** `abspath(__file__)` without `realpath`: a symlinked invocation
  mis-derives `LANE` and exits 2 (honest setup error; never a wrong verdict).
