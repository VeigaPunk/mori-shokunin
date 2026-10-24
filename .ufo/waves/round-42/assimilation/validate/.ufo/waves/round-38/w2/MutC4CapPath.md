# MutC4CapPath — capability-row path mutation (C1 / P-C4 `capability`)

Seat: mutation-tester, mori round 38 wave 2. Scored tip attacked: `f725f3076972e6e70595b5ac8279be524a111ff8`.
Nothing here was read from a report: every line below is re-derived by a command run in this seat's
scratch clone.

## Axes (godspeed)

1. **Fidelity of the minimal mutation** — one path token inside one SCORECARD row, nothing else.
2. **Discrimination of the detector** — does `capability` flip when only that token changes, and do the
   other four checks hold still?
3. **Reversibility** — exact bytes restored and the pristine reading reproduced.

## Claim and mechanism

C1's counter `.ufo/waves/round-38/count-c4.py` must resolve every path cited in the SCORECARD row
`source-drift re-fetch probe` (contract.md, C1 → "`capability_paths` (every backticked path in the
capability row `source-drift re-fetch probe` resolves at R)"). Mechanism under test:

- `capability_row()` — last table row containing the key: `count-c4.py:146-151`;
- `paths_in()` — backticked, slash-bearing tokens only: `count-c4.py:154-165`, grammar `PATH_RE` at
  `count-c4.py:66` (`^[A-Za-z0-9_.-]+(/[A-Za-z0-9_.<>-]+)+$`);
- `check_capability()` — returns `bool(paths)` only: `count-c4.py:176-181`;
- actual resolution — `cap_missing` / `real_cap` in `main`: `count-c4.py:249-250`, using
  `resolves()` = `git cat-file -e <rev>:<path>`: `count-c4.py:123-127`.

The row at the scored tip (lane `SCORECARD.md:2059`, byte-identical in the sandbox) cites
`tools/mori-source-drift.py`, `.ufo/waves/round-37/evidence/c2-after-v3.txt`,
`.ufo/waves/round-37/evidence/drift-live-r37.txt`.

## Sandbox

Real clone of the lane at the scored tip (the MutC4Anchor recipe — a new commit in a clone, since a
rewritten blob cannot keep `f725f30`'s hash):

```
git clone --no-checkout <lane> .ufo/waves/round-38/scratch/MutC4CapPath/sbx-clone
git -C sbx-clone checkout --detach f725f30
```

- `HEAD = f725f3076972e6e70595b5ac8279be524a111ff8`, `git status --porcelain` empty.
- `sha256(sbx-clone/SCORECARD.md) = f1a8ac58619036973fca03667c6ae3f459d2e72b00ee06e198f7a48420404b93`
  — equal to `git show f725f30:SCORECARD.md | sha256sum` in the lane.

**Baseline (pristine, same detector):**

```
python3 .ufo/waves/round-38/count-c4.py f725f30… --repo <sbx-clone>
check anchors          PASS (anchors=3 missing=[])
check capability       PASS (paths=['tools/mori-source-drift.py', '.ufo/waves/round-37/evidence/c2-after-v3.txt', '.ufo/waves/round-37/evidence/drift-live-r37.txt'] missing=[])
check live_rows        PASS (named=10 summary_drifted=10 unknown=[])
check named_row_drift  PASS (exit=0 row_states=('PASS', ''))
check drift_kill       PASS (exit=1 row_states=('FAIL', …))
C4=met   (exit 0)
```

Receipt: `scratch/MutC4CapPath/baseline-clone.txt`.

## Mutant

Single behavior-bearing point: the last path token of the row, replaced by
`evidence/no-such-file.txt` (two original paths kept, so the check cannot flip via `paths=[]`).

```diff
-| round-37 C2 | source-drift re-fetch probe | … | `tools/mori-source-drift.py`; `.ufo/waves/round-37/evidence/c2-after-v3.txt`; `.ufo/waves/round-37/evidence/drift-live-r37.txt` | 36 |
+| round-37 C2 | source-drift re-fetch probe | … | `tools/mori-source-drift.py`; `.ufo/waves/round-37/evidence/c2-after-v3.txt`; `evidence/no-such-file.txt` | 36 |
```

- Commit (sandbox only): `0a27d140e2a196694f26918fa14b6ba033053f20` ("mutant: capability row cites
  evidence/no-such-file.txt"), 1 file changed, 1 insertion/1 deletion.
- `sha256(sbx-clone/SCORECARD.md)` before = `f1a8ac58…404b93`, after = `0a6ab703992a73499b4513383a83dbcd7bc0d6f4fbe8aec4648ca4f22735e047`.
- `git show f725f30:SCORECARD.md` in the same sandbox still hashes `f1a8ac58…` (pristine object untouched).

## Mutant run

```
python3 .ufo/waves/round-38/count-c4.py 0a27d140e2a196694f26918fa14b6ba033053f20 --repo <sbx-clone>
negative witness-token-entry        rejected
negative witness-dangling-row       rejected
negative witness-summary-only-live  rejected
check anchors          PASS (anchors=3 missing=[])
check capability       FAIL (paths=['tools/mori-source-drift.py', '.ufo/waves/round-37/evidence/c2-after-v3.txt', 'evidence/no-such-file.txt'] missing=['evidence/no-such-file.txt'])
check live_rows        PASS (named=10 summary_drifted=10 unknown=[])
check named_row_drift  PASS (exit=0 row_states=('PASS', ''))
check drift_kill       PASS (exit=1 row_states=('FAIL', …))
C4=unmet   (exit 1)
```

Receipt: `scratch/MutC4CapPath/mutant-capability.txt`.

## Verdict — KILLED

Expected detector: `check capability` FAIL with the missing path named, aggregate `C4=unmet`, exit 1.
Observed: exactly that, and only `capability` flipped — `anchors`, `live_rows`, `named_row_drift`,
`drift_kill` and all three negatives held their baseline verdicts. The P-C4 resolution clause is
load-bearing on real bytes; the staged `KILLED` is a pass for the claim, not a defect in it.

## Restoration

- `git -C sbx-clone checkout --detach f725f30` → `HEAD=f725f30…`, `git status --porcelain` = 0 lines,
  `sha256(SCORECARD.md) = f1a8ac58…404b93` (the pre-mutation hash, byte-exact).
- Restored run: `check capability PASS (…missing=[])`, `C4=met`, exit 0 — receipt
  `scratch/MutC4CapPath/restored-run.txt`.
- The four mutant/variant commits remain reachable by branch name (`mut1`…`mut4`) inside the scratch
  clone as evidence; the clone itself is scratch and disposable. No lane object was written.

## Lane untouched (and one concurrent modification I did not make)

- `git -C <lane> rev-parse HEAD` = `f725f3076972e6e70595b5ac8279be524a111ff8` (unchanged).
- Capability row, workspace vs committed: `sha256(SCORECARD.md:2059)` = `6b88111292b7341451d9466f2bcd43825b1212764b7a5f517ae4742c2f289619` in **both**
  `sed -n '2059p' SCORECARD.md` and `git show f725f30:SCORECARD.md | sed -n '2059p'` — the row this
  probe mutates is byte-identical to the scored tip in the lane worktree.
- `grep -RI --exclude-dir=.ufo --exclude-dir=.git 'no-such-file.txt' .` in the lane worktree → 0 hits;
  no mutant token exists outside my scratch.
- Disclosed: `git status --porcelain -- SCORECARD.md` in the lane now prints ` M SCORECARD.md`
  (workspace `sha256=a63cd09b…`, mtime `2026-10-23 20:04:49 -0300`, 2 hunks). The diff is a claim-3
  `supersede_timing` cell correction plus an appended note — **no `re-fetch probe` row edit**. It is
  not mine: my mutants are commits `20:05:02`/`20:05:46`/`20:06:05`/`20:06:26` inside
  `scratch/MutC4CapPath/sbx-clone`, and my first mutant commit postdates that lane mtime.
  Receipt: `scratch/MutC4CapPath/verify-lane.txt`.

## Method note: the rev argument must be the mutant commit

Run literally as tasked, `count-c4.py f725f30… --repo <sbx-clone>` on the sandbox that *carries* the
mutant commit still reads the pristine `f725f30` object and prints `C4=met`, exit 0
(`scratch/MutC4CapPath/literal-rev-on-mutant-sandbox.txt`). Discrimination requires passing the
mutant commit's own sha against that sandbox — the same form MutC4Anchor used. The literal form is a
tasking shorthand, not a counter defect; recorded so nobody reads the `C4=met` line above as a
surviving mutant.

## Coverage findings from the same check (survivors, scratch-only)

These are coverage limits, not contract changes; each was run through the identical detector on the
same clone, each from a fresh branch off `f725f30`.

1. **Unbackticked citation is invisible.** Appending `; evidence/no-such-file.txt` (no backticks) to
   the row's evidence column leaves `check capability PASS (paths=[…3 original…] missing=[])` and
   `C4=met`, exit 0 (`variant-unbackticked.txt`, commit `c27773341530535c3fc2320638c04c71704be70c`).
   Cause: `paths_in` scans only backticked spans (`count-c4.py:154-165`). The frozen check text says
   "every backticked path", so the counter is faithful to it; the P-C4 blockquote's looser "every path
   the SCORECARD capability row cites" is what the implementation does not cover.
2. **Top-level files are never parsed.** Replacing the live-receipt citation with `README.md` leaves
   `check capability PASS (paths=[tool, c2-after-v3.txt] …)` — only two paths — and `C4=met`, exit 0
   (`variant-unrelated-file.txt`, commit `b72b85226ca5238f2f7dba395465ca2f27a0cd58`). `PATH_RE`
   (`count-c4.py:66`) requires at least one `/`, so a cited top-level file is skipped entirely, and the
   row can drop the real receipt pointer without a flip (the receipt itself is still caught by
   `live_rows`, which reads the file at a fixed path, not from the row).
3. **Resolution proves existence, not provenance.** Replacing the receipt citation with an unrelated
   but existing slashed path (`\`.ufo/waves/round-38/contract.md\``) leaves `check capability PASS
   (paths=[…, '.ufo/waves/round-38/contract.md'] missing=[])` and `C4=met`, exit 0
   (`variant-unrelated-slashed.txt`, commit `8190dafa85f06d929a3b1762a75d6876e585d254`). `resolves()`
   is `git cat-file -e` (`count-c4.py:123-127`), which accepts any blob or tree; it cannot tell a
   receipt from an unrelated artefact. Family of the critic's "capability path resolving to an
   unrelated file" concern; the counter's own `witness-dangling-row` fixture
   (`fixtures/witness-dangling-row.md`) covers only the *nonexistent* case.
4. **`check_capability()` alone is a token check.** The function returns `bool(paths)` and does no
   resolution (`count-c4.py:176-181`); resolution lives only in `main` (`:249-250`) and in the witness
   tuples. Any future caller reusing the helper regresses to round 37's token test. Observation only —
   the shipped aggregate path does resolve, as mutant 1 shows.

## Evidence index (all under `.ufo/waves/round-38/scratch/MutC4CapPath/`)

| file | command | observed |
|---|---|---|
| `baseline-clone.txt` | `count-c4.py f725f30 --repo sbx-clone` | `capability PASS`, `C4=met`, exit 0 |
| `mutant-capability.txt` | `count-c4.py 0a27d14 --repo sbx-clone` | `capability FAIL missing=['evidence/no-such-file.txt']`, `C4=unmet`, exit 1 |
| `literal-rev-on-mutant-sandbox.txt` | `count-c4.py f725f30 --repo sbx-clone` (mutant committed on top) | `C4=met`, exit 0 — reads pristine object |
| `restored-run.txt` | `count-c4.py f725f30 --repo sbx-clone` after restore | `capability PASS`, `C4=met`, exit 0 |
| `variant-unbackticked.txt` | `count-c4.py c277733 --repo sbx-clone` | `capability PASS`, `C4=met`, exit 0 |
| `variant-unrelated-file.txt` | `count-c4.py b72b852 --repo sbx-clone` | `capability PASS` (2 paths), `C4=met`, exit 0 |
| `variant-unrelated-slashed.txt` | `count-c4.py 8190daf --repo sbx-clone` | `capability PASS`, `C4=met`, exit 0 |
| `verify-lane.txt` | lane `sha256sum`/`git status`/commit dates | capability row unchanged; concurrent claim-3 edit disclosed |

## Hash ledger (sandbox `SCORECARD.md`)

| state | sha256 |
|---|---|
| lane committed `f725f30` / sandbox baseline | `f1a8ac58619036973fca03667c6ae3f459d2e72b00ee06e198f7a48420404b93` |
| mutant (`mut1`, `0a27d14`) | `0a6ab703992a73499b4513383a83dbcd7bc0d6f4fbe8aec4648ca4f22735e047` |
| restored (`f725f30` checkout) | `f1a8ac58619036973fca03667c6ae3f459d2e72b00ee06e198f7a48420404b93` |

## Tooling directive

No install or upgrade was needed or performed (python3/git already present); nothing to record.

**Result: mutant `capability` = KILLED (expected FAIL, observed FAIL + `C4=unmet` exit 1); sandbox
restored byte-exactly; lane rows untouched by this probe; three same-check survivors logged as
coverage findings (unbackticked citation, slash-less path grammar, existence-only resolution).**
