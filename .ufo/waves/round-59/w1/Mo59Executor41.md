# Mo59Executor41 — C1 fixture-battery enumeration (executor)

**Seat:** Mo59Executor41 (executor) · **Lane:** `/home/vgpnk/Projects/shokunin/mori-shokunin`
**Freeze revision:** `60b3a76ad0524c8978cc51922940be1c8c388915` · **Entering revision:** `2b9f03975bfb6e508f35074ac8181ec8bf54e805`
**Lane HEAD observed:** `8ff344ff18924c1ea63d46c3b3969f9fea05bc51` (round-59 dispatch payload; C1/C2 bytes identical to freeze)
**Scratch:** `/fast/scratch/hyaku/mori-r59/Mo59Executor41` (cleaned before yield)
**Disk guard:** `scripts/hyaku/disk-guard.sh status` → green (`/fast/scratch/hyaku` 27% used, 592.6G free)

**Scope note.** This seat's assignment is the C1 fixture battery. Everything below is read-only on
the lane: `git show` / `ls-tree` / `cat-file` only. No production file, corpus file, SCORECARD,
LOG, MANIFEST or lane VCS mutation was made. The only lane write is this report. All fixtures were
materialized into scratch, never into the lane.

---

## 1. Primary deliverable — the fixture battery table

Method: each fixture tree was materialized **from git at the freeze revision** into scratch
(`git show REV:<path>`), then the frozen tool
`tools/mori-register-check.py` (sha256 `38b733d8…472b8`, PIN-verified) was invoked with the
counter's exact fixture-arm arguments:

```
python3 tool.py --scorecard F/scorecard.md --manifest F/manifest.json --root F/_files \
  --require rounds[832].capabilities_added[0] \
  --require rounds[832].capabilities_added[1]
```

### 1a. Table as the counter runs it (count-c1.py's own layout)

This is the layout `count-c1.py` builds (payload materialized under `_files/<full repo-relative path>`).

| # | fixture | verdict | exit | expect token | expect matched | reasons emitted |
|---|---|---|---|---|---|---|
| 1 | `f01-stub-only` | REGISTER_UNMET | 1 | `binding` | yes | `binding:declared_register=0(capabilities_sections=1)`; `keys:missing=rounds[832].capabilities_added[0]`; `keys:missing=rounds[832].capabilities_added[1]` |
| 2 | `f02-two-declared` | REGISTER_UNMET | 1 | `binding` | yes | `binding:declared_register=2(capabilities_sections=3)`; `keys:missing=…[0]`; `keys:missing=…[1]` |
| 3 | `f03-dup-key` | REGISTER_UNMET | 1 | `keys` | yes | `keys:duplicate=rounds[832].capabilities_added[0]`; `manifest:name=…[0]`; +4 spurious `pointers:missing=…` (see F1) |
| 4 | `f04-missing-key` | REGISTER_UNMET | 1 | `keys` | yes | `pointers:missing=tools/mori-vote-bind.py`; `pointers:missing=.ufo/waves/round-56/evidence/c2-at-landed.txt`; `keys:missing=rounds[832].capabilities_added[1]` |
| 5 | `f05-pointer-missing` | REGISTER_UNMET | 1 | `pointers` | yes | `pointers:missing=tools/mori-vote-bind.py`; `pointers:missing=.ufo/…/c2-at-landed.txt`; `pointers:missing=tools/mori-driver-liveness.py`; `pointers:missing=.ufo/…/c1-at-landed.txt` |
| 6 | `f06-pointer-absolute` | REGISTER_UNMET | 1 | `pointers` | yes | `pointers:bad=/etc/passwd`; +3 spurious `pointers:missing=…` |
| 7 | `f07-pointer-relative-parent` | REGISTER_UNMET | 1 | `pointers` | yes | `pointers:missing=tools/mori-vote-bind.py`; `pointers:bad=../../etc/passwd`; +2 spurious `pointers:missing=…` |
| 8 | `f08-manifest-name-altered` | REGISTER_UNMET | 1 | `manifest:name` | yes | `manifest:name=rounds[832].capabilities_added[0]`; +4 spurious `pointers:missing=…` |
| 9 | `f09-manifest-substring-only` | REGISTER_UNMET | 1 | `manifest:name` | yes | `manifest:name=rounds[832].capabilities_added[0]`; +4 spurious `pointers:missing=…` |
| 10 | `f10-manifest-foreign-lane` | REGISTER_UNMET | 1 | `manifest:lane` | yes | `manifest:lane='kotoba'` (×2); +4 spurious `pointers:missing=…` |
| 11 | `f11-manifest-wrong-index` | REGISTER_UNMET | 1 | `manifest` | yes | `manifest:lane=None`; `manifest:entry_missing=…[0]`; `manifest:lane_round=…[0]`; same ×2 for `[1]`; +4 spurious `pointers:missing=…` |
| 12 | `f12-lane-round-mismatch` | REGISTER_UNMET | 1 | `manifest:lane_round` | yes | `manifest:lane_round=rounds[832].capabilities_added[0]`; `manifest:lane_round=rounds[832].capabilities_added[1]`; +4 spurious `pointers:missing=…` |
| 13 | `f13-empty-pointer` | REGISTER_UNMET | 1 | `pointers` | yes | `pointers:missing=tools/mori-vote-bind.py`; `pointers:missing=.ufo/…/c2-at-landed.txt`; `pointers:none=rounds[832].capabilities_added[1]` |

**Result: 13/13 fixtures score UNMET (exit 1), 13/13 expect tokens matched, 0/13 score MET.**
The frozen contract's fixture-arm requirement ("each MUST score UNMET covering its frozen expect
prefix") is met literally.

### 1b. Same battery, payload materialized correctly (payload at `_files/<path relative to fixture dir>`)

| # | fixture | verdict | expect matched | reasons (correct layout) |
|---|---|---|---|---|
| 1 | `f01-stub-only` | UNMET | yes | `binding:declared_register=0(capabilities_sections=1)`; `keys:missing=…[0]`; `keys:missing=…[1]` |
| 2 | `f02-two-declared` | UNMET | yes | `binding:declared_register=2(capabilities_sections=3)`; `keys:missing=…[0]`; `keys:missing=…[1]` |
| 3 | `f03-dup-key` | UNMET | yes | `keys:duplicate=rounds[832].capabilities_added[0]`; `manifest:name=…[0]` |
| 4 | `f04-missing-key` | UNMET | yes | `keys:missing=rounds[832].capabilities_added[1]` |
| 5 | `f05-pointer-missing` | UNMET | yes | `pointers:missing=.ufo/waves/round-56/evidence/c2-at-landed.txt` |
| 6 | `f06-pointer-absolute` | UNMET | yes | `pointers:bad=/etc/passwd` |
| 7 | `f07-pointer-relative-parent` | UNMET | yes | `pointers:bad=../../etc/passwd` |
| 8 | `f08-manifest-name-altered` | UNMET | yes | `manifest:name=rounds[832].capabilities_added[0]` |
| 9 | `f09-manifest-substring-only` | UNMET | yes | `manifest:name=rounds[832].capabilities_added[0]` |
| 10 | `f10-manifest-foreign-lane` | UNMET | yes | `manifest:lane='kotoba'`; `manifest:lane='kotoba'` |
| 11 | `f11-manifest-wrong-index` | UNMET | yes | `manifest:lane=None`; `manifest:entry_missing=…[0]`; `manifest:lane_round=…[0]`; same ×2 for `[1]` |
| 12 | `f12-lane-round-mismatch` | UNMET | yes | `manifest:lane_round=…[0]`; `manifest:lane_round=…[1]` |
| 13 | `f13-empty-pointer` | UNMET | yes | `pointers:none=rounds[832].capabilities_added[1]` |

**13/13 UNMET, 13/13 expect matched in both layouts.** The verdicts agree; only the *reason sets*
differ — 11/13 differ, always by the extra `pointers:missing=…` family. That difference is the
root of F1/F2 below.

---

## 2. Counter and tool receipts (frozen, unmodified)

| command | result |
|---|---|
| `python3 .ufo/waves/round-59/count-c1.py --selftest` | `C1_SELFTEST pass=6 fail=0`, exit 0 |
| `count-c1.py 60b3a76ad052…` (freeze) | `C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=60b3a76ad0524c8978cc51922940be1c8c388915`, exit 0 |
| `count-c1.py 8ff344ff1892…` (HEAD) | `C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=8ff344ff18924c1ea63d46c3b3969f9fea05bc51`, exit 0 |
| `count-c1.py 2b9f03975bfb…` (entering, do-nothing control) | `C1=unmet selftest=bad fixtures=bad real=bad pointers=bad rev=2b9f039… failed=tool_absent,selftest,fixtures_absent,real,pointers`, exit 1 — matches the contract's frozen before-arm |
| `python3 tools/mori-register-check.py --selftest` | `REGCHECK_SELFTEST pass=12 fail=0`, exit 0 |
| `python3 tools/mori-settlement-scan.py --selftest` | `SETSCAN_SELFTEST pass=10 fail=0`, exit 0 |
| `count-c2.py --selftest` | `C2_SELFTEST pass=9 fail=0`, exit 0 |
| `count-c2.py 60b3a76ad052…` / `8ff344ff…` (committed) | `C2=unmet … failed=copy_absent:…×6,entry_absent,tree`, exit 1 |
| `count-c2.py HEAD` (working tree, corpus artifacts landed during this wave) | `C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 rev=HEAD`, exit 0 |
| `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` | exit 0; mori lane `ok`; only pre-existing `W04` duplicate-URL warnings |

**Frozen-byte integrity** (sha256, freeze vs HEAD vs worktree — all SAME):
`count-c1.py` `2be6fda8c54633fd…`, `count-c2.py` `2df3ae84f6d66f9e…`, `contract.md` `427fca0bf2a92813…`,
`tools/mori-register-check.py` `38b733d896f880f5…` (== PIN), `tools/mori-settlement-scan.py`
`4c04bf2170b04841…` (== PIN). `git diff --stat HEAD -- .ufo/waves/round-59/fixtures-c1` is empty.

---

## 3. Findings

### F1 — HIGH — the counter's fixture arm materializes fixture payload at a path the tool never reads

`count-c1.py:151` materializes each fixture's non-`scorecard.md`/`manifest.json`/`expect.txt` file
with the **full repo-relative path** as the destination key:

```python
file_list = git(repo, "ls-tree", "-r", "--name-only", rev, base + "/")
for f in (…):
    rel = f[len(base) + 1:]            # <-- rel computed, then never used
    if rel in ("scorecard.md", "manifest.json", "expect.txt"):
        continue
    materialize(repo, rev, [f], fdir / "_files")   # <-- uses `f`, not `rel`
```

`materialize()` writes `root / rel`, so `f01`'s `tools/mori-vote-bind.py` lands at
`_files/.ufo/waves/round-59/fixtures-c1/f01-stub-only/tools/mori-vote-bind.py`, while the tool is
invoked with `--root <fdir>/_files` and looks for `_files/tools/mori-vote-bind.py`
(`mori-register-check.py:184-185`). **Consequence: no fixture pointer ever resolves.** Every fixture
emits spurious `pointers:missing=…` reasons for paths that are in fact present in the fixture tree.

Observed directly (`find` on the counter's own scratch):

```
c1-freeze/fx/f08-manifest-name-altered/_files/.ufo/waves/round-59/fixtures-c1/f08-manifest-name-altered/tools/mori-vote-bind.py
```

The `rel` variable is computed one line above and discarded — the fix is a one-token change
(`[f]` → `[f[len(base) + 1:]]`, or materialize `rel` under the fixture root).

Contrast the **real** arm, which is correct: `count-c1.py:193`
`materialize(repo, rev, [rel2], proot)` materializes at the path the tool expects, and the real arm
verifies REGISTER_MET with zero pointer reasons (my independent replay: `pass2 verdict:
REGISTER_MET rc=0, reasons: []`, bound = the two frozen names).

**Impact.** The counter still reaches `fixtures=ok` because the frozen expect prefixes are satisfied
by *some* `pointers:*` reason. But the fixture arm is not measuring what it appears to measure.

### F2 — HIGH — the fixture battery does not certify the checks its fixtures are named for

Because of F1, `pointers:missing=…` is emitted by **every** fixture; and the four pointer fixtures
(f05, f06, f07, f13) carry the coarse frozen prefix `pointers`. I deleted each pointer-related
rejection check one at a time in a scratch copy of the tool and re-ran the battery under both
layouts. "Detected" = the fixture no longer satisfies (UNMET **and** expect-prefix-covered), i.e.
the fixture stops certifying its designed defect.

| deleted check | detected under COUNTER layout (count-c1.py's own) | detected under CORRECT layout |
|---|---|---|
| `pointers:none` (empty evidence cell) | **NONE** | `f13-empty-pointer` |
| absolute/`~` pointer rejection (`pointer_ok`, tool:96) | **NONE** | `f06-pointer-absolute` |
| `..` parent pointer rejection (tool:98) | **NONE** | NONE (see note) |
| pointer existence check (tool:185) | `f05-pointer-missing` | `f05-pointer-missing` |
| `binding:declared_register` | `f01`, `f02` | `f01`, `f02` |
| `keys:duplicate` | `f03` | `f03` |
| `keys:missing` | `f04` | `f04` |
| `manifest:lane` | `f10` | `f10` |
| `manifest:entry_missing` | `f11` | `f11` |
| `manifest:name` | `f08`, `f09` | `f08`, `f09` |
| `manifest:lane_round` | `f12` | `f12` |
| `keys:short_row` | NONE | NONE |
| `keys:empty_name` | NONE | NONE |
| `manifest:unreadable` | NONE | NONE |
| `manifest:index_missing` | NONE | NONE |

**Checks not detected by any fixture under the counter's own layout: 7/15.** Under the correct
layout: 6/15.

Concretely, the frozen battery does **not** detect deletion of the absolute-pointer rejection
(`pointer_ok`, `mori-register-check.py:96`) — `f06-pointer-absolute` still reports UNMET with the
coarse `pointers` prefix satisfied by a spurious `pointers:missing=…`:

```
P1 (absolute+tilde rejection deleted), f06, COUNTER layout:
  verdict=REGISTER_UNMET rc=1
  pointers:missing=.ufo/waves/round-56/evidence/c2-at-landed.txt
  pointers:missing=tools/mori-driver-liveness.py
  pointers:missing=.ufo/waves/round-56/evidence/c1-at-landed.txt
P1, f06, CORRECT layout:
  verdict=REGISTER_MET rc=0        <-- correctly detected here
```

Nor does it detect deletion of `pointers:none` (tool:179) — `f13-empty-pointer` still passes on the
spurious `pointers:missing` reasons.

**Counter-level confirmation** (importing the frozen `count-c1.py` read-only and feeding it a
mutated tool blob): with `pointers:none` deleted, the counter's own arms report
`verdict=UNMET failed=tool_sha` and **no `fixture:` failure** — the fixture arm still says `ok`:

```
detail: {'selftest': True, 'real': True, 'pointers': True}
=> the FIXTURE arm still says ok (no 'fixture:' failure): True
```

The only thing that caught these mutants was the `tool_sha` PIN arm — i.e. the byte pin, not the
semantic battery. The battery is the arm the contract names as the semantic evidence, so this is
the load-bearing gap.

Note on `..`: even under the correct layout, `f07-pointer-relative-parent` does not detect deletion
of the `..` rejection (tool:98), because with that check gone the pointer `../../etc/passwd` fails
the *existence* check instead and is reported as `pointers:missing=../../etc/passwd` — the same
coarse `pointers` prefix. `f07` therefore cannot distinguish "rejected as parent-relative" from
"rejected as non-existent" under either layout.

### F3 — MEDIUM — `Path(root) / rel` escapes `--root` for absolute pointers

`mori-register-check.py:184-185`:

```python
rel = p[2:] if p.startswith("./") else p
if not (Path(root) / rel).is_file():
```

Python's `pathlib` drops the left operand when the right is absolute:

```
Path('/scratch/root') / '/etc/passwd'  ->  /etc/passwd     is_file() -> True
```

The absolute-pointer rejection at tool:96 is what prevents this today, so it is not currently
exploitable — but the *existence* check has no containment of its own. If the absolute/`~`
rejection is ever weakened (exactly the mutant F2 shows the battery cannot catch), an absolute
pointer resolves against the real filesystem root rather than `--root`. A defense-in-depth
`Path(root, rel)` / `os.path.commonpath` containment check would close it independently.
This compounds F2: the two checks that would have caught it are mutually redundant, and neither is
independently enforced.

### F4 — LOW — dead code in the frozen counter's fixture arm

`count-c1.py:155-157` computes `got = {…}` from the reasons and **never uses it**; the matching
decision uses `matched` on the next line instead. `got` is the only reason-token set the counter
computes and it is dead — it reads like a leftover from an intended exact-reason-set comparison.
Harmless to the verdict (verified: the counter's verdict is identical with `got` removed, since
`got` is never referenced), but it marks a missed opportunity: the fixture arm currently accepts
*any* reason with the right prefix, which is precisely what lets F2's spurious `pointers:missing`
reasons satisfy the pointer fixtures' expectations. Comparing against `got` (exact reason-family
sets per fixture) would have caught F1/F2.

### F4b — receipt taken at the final tip

The lane tip advanced during this wave (integrator commits `be737211` "land C2 data" and
`7b86704d` "data correction — K11 demoted to prose"). Re-verified at the final tip
`7b86704d7c0754a09958d131b64dbfa2a6d3eaed`:

```
count-c1.py HEAD -> C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=HEAD   (exit 0)
count-c2.py HEAD -> C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok
                          pins=ok tree=ok claims=13 files=6 rev=HEAD               (exit 0)
```

Frozen bytes freeze → final tip: `count-c1.py`, `count-c2.py`, `contract.md`,
`mori-register-check.py`, `mori-settlement-scan.py` — all **UNCHANGED**. The kill rule holds.

### F5 — informational — C2 corpus artifacts landed mid-wave

At the freeze revision and at committed HEAD, C2 is UNMET (`copy_absent:…×6, entry_absent, tree`)
because `corpus/evidence/sources-r59/*.json` and `corpus/knowledge/wave-settlement-artifacts-r59.md`
were not yet committed. They are present in the **working tree** during this wave, and
`count-c2.py HEAD` (working tree) returns
`C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6`
(exit 0). Not a defect — the wave is a build wave — but the C2 receipt must be taken against a
revision where those files are committed, not against the working tree.

### F6 — informational — the C2 fixture rows' `used-by` binding is asserted only by the counter, not by the tool

Not this seat's assigned scope; noted because F2's remedy (tightening reason matching) would need
the same treatment applied symmetrically to `count-c2.py`'s tree arm, which has an analogous
coarse-prefix expectation shape.

---

## 4. What I did **not** find

- No fixture scores MET. The contract's literal fixture-arm requirement holds at freeze and HEAD.
- The counter's **real** arm is sound: independent replay (SCORECARD.md at freeze + MANIFEST.json at
  `2807c6ab8a9b04dcf256682bcd722c695fdd6e14`, pointers materialized under `--root`) gives
  `REGISTER_MET`, exit 0, empty reasons, bound = the two frozen names
  (`dual-shape seat-output vote binding …`, `strict per-event driver-liveness probe …`).
- Both PINs verify byte-exactly at freeze and HEAD.
- Frozen bytes (contract, both counters, both tools) are identical freeze ↔ HEAD ↔ worktree; the
  kill rule is not violated.
- The tools write only under the given `--scratch` / `TMPDIR` (`mori-register-check.py:211-216,
  240-248`); the counter honors `TMPDIR` and takes `--scratch`.
- The do-nothing control at entering `2b9f0397` reproduces the contract's frozen before-arm exactly.
- No PACMAN install or tool update was needed; no tool was installed or updated by this seat.

---

## 5. Reproduction

All scratch artifacts live under `/fast/scratch/hyaku/mori-r59/Mo59Executor41` and are removed
before yield. Scripts used (all read-only on the lane):

- `enum-fixtures.py REV SCRATCH` — materialize each fixture from git at REV, run the tool with the
  counter's exact arguments, print verdict + reasons + expect match.
- `mutants2.py SCRATCH` — control-flow-preserving single-check deletions in a scratch copy of the
  tool; per-fixture detection under both layouts.
- `matrix.py SCRATCH` — the full 15-check coverage matrix in §F2.
- `payload-test.py SCRATCH` — layout diff (F1) and the payload-stripped counter run.
- `counter-mutants.py SCRATCH` / `cm2.py` / `cm3.py` / `cm4.py` — the frozen `count-c1.py` imported
  read-only with a patched `git_show`, so the counter's own arms are exercised against mutants.

Key line pointers: `count-c1.py:151` (F1 bug site), `count-c1.py:155` (F4 dead `got`),
`count-c1.py:193` (correct real-arm materialization), `mori-register-check.py:96` / `:98` (pointer
syntax rejections), `:179` (`pointers:none`), `:184-185` (F3 existence check / root escape).

---

## 6. Recommendation to L1 (advisory only — no production edit made)

F1 is a one-token fix in the frozen counter (`[f]` → the already-computed `rel`), but the counter
bytes are frozen and the kill rule forbids post-freeze changes — so this is a **next-round** item,
not a round-59 remediation. If the round-59 claim is to be scored on the strength of the fixture
battery as semantic evidence, note that 7/15 of the tool's rejection checks are not exercised by
it as the counter currently materializes fixtures; the `tool_sha` PIN arm is what actually holds
the line. The same one-token materialization fix, plus replacing the coarse `pointers` expect
prefixes with exact reason-family sets (the `got` set already computed at `count-c1.py:155`), would
restore the battery's certifying power in a future round.
