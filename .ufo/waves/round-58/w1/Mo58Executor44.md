# Mo58Executor44 — C1 pointer-resolution attack (round 58, wave 1)

**Seat:** Mo58Executor44 (executor, leaf)
**Scope:** attack the frozen `git cat-file -e` evidence-path checks in `.ufo/waves/round-58/count-c1.py`
**Freeze revision used:** `fe8801120a67c1a6b8899d7d0423839caa09e7d0`
**Contract read:** `.ufo/waves/round-58/contract.md` (C1 section)
**Lane:** `/home/vgpnk/Projects/shokunin/mori-shokunin` · **Fleet root:** `/home/vgpnk/Projects/shokunin`

## What I did

Ran the **frozen** counter's own `measure()` against **26 throwaway git fixtures** in scratch, with the
counter's `LANE`/`FLEET` globals rebound to each fixture — the same rebinding the counter's own
`_run_selftest()` performs. Frozen bytes were read with
`git -C <lane> show fe88011:.ufo/waves/round-58/count-c1.py` and executed **unmodified**.

No production file was edited. No commit, no lane VCS mutation, no fleet/sibling write.
Every fixture repo was `git init`-ed at an explicit scratch path and every git command used
`git -C <that path>`; each fixture asserted `git rev-parse --show-toplevel` == the fixture dir.

**Frozen bytes integrity (re-verified):**
```
frozen counter sha256 : 6ecdb627bb55522c258dc484ed5c530cfd6f7c57c6a89b4c38179df4c0f84e4b
worktree  sha256      : 6ecdb627bb55522c258dc484ed5c530cfd6f7c57c6a89b4c38179df4c0f84e4b
bytes identical       : True
```

**Baseline at the freeze revision (real lane):**
```
python3 .ufo/waves/round-58/count-c1.py fe8801120a67c1a6b8899d7d0423839caa09e7d0
C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=fe8801120a67c1a6b8899d7d0423839caa09e7d0   (exit 0)
python3 .ufo/waves/round-58/count-c1.py --selftest
C1_SELFTEST pass=4 fail=0   (exit 0)
```
Instrumented `git cat-file -e` call trace on the real lane: **exactly 4 calls**, one per whitelisted
pointer. The counter resolves the landed register correctly.

**Receipt (reproducible):**
- `.ufo/waves/round-58/w1/Mo58Executor44.receipt.py` — harness (26 arms + real-lane audit)
- `.ufo/waves/round-58/w1/Mo58Executor44.receipt.txt` — its full output

Run: `export TMPDIR=/fast/scratch/hyaku/mori-r58/Mo58Executor44; python3 …/Mo58Executor44.receipt.py`

---

## FINDING 1 (headline) — the pointer whitelist makes the contract's §9 do-nothing control pass-through

`count-c1.py` gates pointer resolution on a **hard-coded three-prefix whitelist** before it ever
calls `git cat-file -e` (frozen source, lines 110–118):

```python
for path in re.findall(r"`([^`]+)`", ln):
    if "/" not in path and not path.endswith((".py", ".txt", ".md")):
        continue
    if path.startswith((".ufo/", "tools/", "corpus/")):     # <-- whitelist gate
        q = _git("cat-file", "-e", f"{rev}:{path}")
        if q.returncode != 0:
            pointers = "bad"; failed.append("pointers")
```

Any backticked path **not** under `.ufo/`, `tools/`, or `corpus/` is never handed to git at all.
The contract's §9 do-nothing control says:

> "a fixture register whose two rows name a nonexistent evidence path MUST score `C1=unmet … failed=pointers`, exit 1"

That holds only for the three whitelisted prefixes. **Measured, same fixture shape, only the pointer
prefix varies:**

| pointer in row 0 | `git cat-file -e` truth | counter verdict | contract §9 |
|---|---|---|---|
| `tools/no-such-tool.py` | rc=128 (does not exist) | `C1=unmet … failed=pointers`, exit 1 | honoured |
| `corpus/no-such.md` | rc=128 | `C1=unmet … failed=pointers`, exit 1 | honoured |
| `.ufo/no-such.txt` | rc=128 | `C1=unmet … failed=pointers`, exit 1 | honoured |
| `evidence/no-such.txt` | rc=128 | **`C1=met rows=2 pointers=ok … failed=none`, exit 0** | **VIOLATED** |
| `docs/no-such.md` | rc=128 | **`C1=met … failed=none`, exit 0** | **VIOLATED** |
| `scripts/no-such.txt` | rc=128 | **`C1=met … failed=none`, exit 0** | **VIOLATED** |
| `no-such-tool.py` (basename only) | rc=128 | **`C1=met … failed=none`, exit 0** | **VIOLATED** |
| `/tools/mori-vote-bind.py` (absolute) | rc=128 | **`C1=met … failed=none`, exit 0** | **VIOLATED** |
| `/home/vgpnk/…/tools/mori-vote-bind.py` (absolute host path) | rc=128 | **`C1=met … failed=none`, exit 0** | **VIOLATED** |
| `../MANIFEST.json` (escapes the tree) | rc=128 | **`C1=met … failed=none`, exit 0** | **VIOLATED** |
| `MANIFEST.json` (fleet-root file, not in lane tree) | rc=128 | **`C1=met … failed=none`, exit 0** | **VIOLATED** |

Exact fixtures (26-arm receipt, root `…/m58exec44-receipt-mso3ei8s/`):

```
R05_missing_under_evidence_prefix   git_rc=128  cnt_rc=0  C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=b7a27b15d98e294db774f5ed4b7db4c3d9c27eba
R06_missing_under_docs_prefix        git_rc=128  cnt_rc=0  C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=37b93a01d248a64d5dd0add71b024f0c103b88fa
R07_missing_basename_only           git_rc=128  cnt_rc=0  C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=0ea2053805f3605e2e8301779f21dc46bf290552
R08_missing_absolute_path           git_rc=128  cnt_rc=0  C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=cd217f1f910c16688af9294aa828e159f070e358
R09_missing_absolute_host_path      git_rc=128  cnt_rc=0  C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=af406465f322be3386b60ed3efc63117b73389ea
R10_pointer_escapes_tree            git_rc=128  cnt_rc=0  C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=67048ce404ece108c42d33a605c16b0472d9c7a9
R11_pointer_to_fleet_root_file      git_rc=128  cnt_rc=0  C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=986b2efdaae0330ee90e273f4fb679b047abd927
```

**Verdict: the counter's pointer-resolution is prefix-scoped, not universal.** A register whose two
rows name a *nonexistent* evidence pointer under `evidence/`, `docs/`, `scripts/`, a bare filename, an
absolute path, or a tree-escaping path scores **`C1=met`, exit 0** — a false green against the
contract's own do-nothing control. The defect is latent, not currently firing: the **landed** round-56
rows use `tools/…` and `.ufo/…` only, so the real register measures `pointers=ok` honestly.

**Why the counter's own selftest does not catch it (FINDING 1b):** the four `--selftest` arms are
`conformant_active_register`, `stub_only_binding_refused`, `nonexistent_pointer_fails`,
`wrong_key_row_fails`. The single nonexistent-pointer arm is
`ROW_BAD_PTR = … | \`tools/no-such-tool.py\` | 56 |` — a **whitelisted** prefix. So
`C1_SELFTEST pass=4 fail=0` is green while the hole is live.

## FINDING 2 — pointer resolution is vacuous when the row carries no pointer

The contract clause (b) is "every evidence pointer in the two rows resolved via `git cat-file -e R:<path>`".
With **zero** pointers in the rows, the clause holds vacuously and the counter reports `pointers=ok`:

```
R12_no_pointer_at_all        cnt_rc=0  C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=3369bcac4a053eeca5dbe867dc1d2c7cbca45d8e
R13_both_evidence_cells_empty cnt_rc=0  C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=88e73081ff4fec93aebc796fc8fd7b4794ddd402
R15_empty_backticks          cnt_rc=0  C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=ae73c135cacd491d34e262272bdc2b48a61e4740
```

`R13` has both evidence cells empty (`—`); the counter still prints `pointers=ok`. A pointer check that
cannot distinguish "checked and resolved" from "never checked" is not a resolution check.
`R14` shows the same for an un-backticked pointer (`tools/no-such-tool.py` written without backticks):
git says the path does not exist, the counter says `pointers=ok`.

## FINDING 3 — malformed paths under the whitelist ARE caught (this part works)

Reported for balance — these all correctly produce `failed=pointers`, exit 1:

| arm | pointer | git truth | counter |
|---|---|---|---|
| R18 | `tools/../tools/mori-vote-bind.py` | rc=128 | `C1=unmet … failed=pointers` |
| R19 | `tools//mori-vote-bind.py` | rc=128 | `C1=unmet … failed=pointers` |
| R20 | `tools/*.py` (glob) | rc=128 | `C1=unmet … failed=pointers` |
| R21 | `tools/mori-vote-bind.py ` (trailing space) | rc=128 | `C1=unmet … failed=pointers` |

Git does **not** glob-expand, does **not** normalise `//`, does **not** follow `..`, and does **not**
tolerate a trailing space inside `R:path` — each is a literal tree lookup that misses. The counter
passes these through correctly.

**Wrong-tree (rev-scoped) resolution also works.** A pointer that exists at HEAD but is absent at the
measured rev is correctly rejected (`A18_wrong_tree_same_prefix` → `C1=unmet … failed=pointers`), and
a pointer added *after* the measured rev is correctly rejected (`B14` → `C1=unmet … failed=pointers`).
The counter resolves against the tree of the measured revision, not the working tree — correct.

## FINDING 4 — a directory pointer satisfies the "resolved evidence pointer" clause

`git cat-file -e R:tools` returns **rc=0** (it resolves the *tree*), so a pointer naming a directory
scores as a resolved evidence pointer:

```
R16_directory_pointer  git_rc=0  cnt_rc=0  C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=02650285f75c5a7dc10dcf52b1f89c70ebdf5473
```

The counter never checks that the resolved object is a *blob* (`git cat-file -t`). A pointer to
`tools` or `corpus/knowledge` is not evidence of anything but is accepted. (Note: `corpus/knowledge`
as a pointer in the receipt fixture was rc=128 because that fixture does not create the directory;
where the directory exists — arm `B11` in the working set — git returns rc=0 and the counter scores met.)

## FINDING 5 — the stub marker never matches the lane's real stub bytes

`STUB_MARK = "-- none yet --"` (ASCII hyphens, 14 chars). The lane's **actual** stub row at
`SCORECARD.md:599` is:

```
| — none yet — | | | |          (em-dashes U+2014)
```

Verified: `"-- none yet --" in SCORECARD.md` → **False**; `"— none yet —" in SCORECARD.md` → **True**.
So the stub-refusal clause is a **no-op against the lane's own stub bytes**.

It does not currently cause a false green, because the real stub is independently refused by two
other clauses (it has no binding sentence, and its header is `| Capability | What it can now do | …`,
not `| key | capability |`). Verified directly: feeding the real stub section to
`_find_register()` returns `(None, "active_register_not_found")`.

But the clause is inert, and a section carrying the lane's **actual** em-dash stub row *plus* the
binding sentence *plus* the `| key | capability |` header is accepted:

```
R24_emdash_stub_marker_not_matched  cnt_rc=0  C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=47a595f4f07507cd129797c7941d8b9b1f3f80ba
R25_hyphen_stub_marker_matched      cnt_rc=1  C1=unmet rows=0 pointers=ok manifest=bad binding=bad failed=binding rev=1242aa867ca209b6ae05d38f966aa2e8219cf484
```

`R25` (hyphen marker) is refused; `R24` (the lane's real em-dash marker) is not.

## FINDING 6 — the register binding is "first `## Capabilities` section matching the preamble", not "the active register"

`_find_register` returns the **first** heading whose body contains the binding sentence, the
`| key | capability |` header, and not the stub marker. A **decoy** section placed earlier in the file
that satisfies those three clauses and carries the two round-56 keys **wins**, even when the genuine
round-35 register later in the file has **no** round-56 rows at all:

```
R26_decoy_section_wins_over_real_register  cnt_rc=0  C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=e4fe0f09858f72e1d43d1bbefc988e9588b0f319
```

This is the round-57 defect class (wrong-table selection) surviving in reduced form: the fix moved from
"first `## Capabilities` heading" to "first `## Capabilities` heading whose preamble matches a literal
sentence", which is a **content** test but still positionally first-match, with no check that the
chosen section is the one the contract names (`SCORECARD.md:1953`).

Related, in the same clause: `R23_key0_twice_key1_absent` — two rows **both** keyed
`` `rounds[832].capabilities_added[0]` `` and **no** row keyed `…[1]` — scores
`C1=met rows=2` (rev `91a1a9d83660745a7b1028daea9d52b6b8bf64be`). The counter selects rows by
`any(k in ln for k in R56_KEYS)` and only checks `len(rows) == 2`, so a **duplicate** of one key
satisfies the pair requirement. Contract (c) binds "each row's key" to the manifest slot; the counter
binds only the *count*.

## FINDING 7 — the contract's frozen target-output string does not match the counter's actual output

Contract line 30 declares:

```
Frozen target output (after): `C1=met rows=2 pointers=ok manifest=ok binding=ok selftest=ok rev=R`
```

The frozen counter prints (line 124–126):

```
C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=<rev>
```

Measured at the freeze revision:
```
contract target : 'C1=met rows=2 pointers=ok manifest=ok binding=ok selftest=ok rev=R'
actual stdout   : 'C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=fe8801120a67c1a6b8899d7d0423839caa09e7d0'
BYTE-EXACT MATCH: False
contract-only tokens: ['selftest=ok', 'rev=R']
actual-only tokens  : ['failed=none', 'rev=fe8801120a67c1a6b8899d7d0423839caa09e7d0']
```

The counter has **no `selftest=ok` field anywhere** (`grep -n 'selftest='` on the frozen source: no
match) and **no `failed=none`** field in the contract string. The counter's `--selftest` mode is a
*separate process* that prints `C1_SELFTEST pass=N fail=0`, never `selftest=ok` inside the measure
line. So the contract's stated byte-exact target is unreachable by the frozen counter as written.

This bears on the kill rule ("any post-freeze change to the counter bytes, the predicate sentence, or
**the target output** invalidates the claim"). The counter bytes are frozen and unchangeable; the
target string as frozen cannot be produced by them. Flagging for the L1 — **I am not proposing a
remediation**; per the contract the kill rule is immutable and this seat is detection-only.

---

## Summary table — 26 arms

| arm | git truth | counter rc | verdict |
|---|---|---|---|
| R01 control, all resolvable | rc=0 | 0 | met (correct) |
| R02 missing `tools/` | 128 | 1 | unmet `failed=pointers` (correct) |
| R03 missing `corpus/` | 128 | 1 | unmet `failed=pointers` (correct) |
| R04 missing `.ufo/` | 128 | 1 | unmet `failed=pointers` (correct) |
| **R05 missing `evidence/`** | **128** | **0** | **met — FALSE GREEN** |
| **R06 missing `docs/`** | **128** | **0** | **met — FALSE GREEN** |
| **R07 missing basename-only** | **128** | **0** | **met — FALSE GREEN** |
| **R08 missing absolute path** | **128** | **0** | **met — FALSE GREEN** |
| **R09 missing absolute host path** | **128** | **0** | **met — FALSE GREEN** |
| **R10 tree-escaping `../MANIFEST.json`** | **128** | **0** | **met — FALSE GREEN** |
| **R11 fleet-root `MANIFEST.json`** | **128** | **0** | **met — FALSE GREEN** |
| **R12 no pointer at all** | — | **0** | **met — vacuous `pointers=ok`** |
| **R13 both evidence cells empty** | — | **0** | **met — vacuous `pointers=ok`** |
| **R14 un-backticked nonexistent pointer** | **128** | **0** | **met — FALSE GREEN** |
| **R15 empty backticks** | — | **0** | **met — vacuous** |
| R16 directory pointer `tools` | 0 | 0 | met — tree accepted as evidence |
| R17 subdirectory pointer | 128 | 1 | unmet (dir absent in that fixture) |
| R18 traversal `tools/../tools/…` | 128 | 1 | unmet (correct) |
| R19 double slash | 128 | 1 | unmet (correct) |
| R20 glob `tools/*.py` | 128 | 1 | unmet (correct) |
| R21 trailing space | 128 | 1 | unmet (correct) |
| R22 swapped pointers | 0,0 | 0 | met — no capability↔pointer identity |
| **R23 key0 twice, key1 absent** | 0,0 | **0** | **met — key-pair not enforced** |
| **R24 em-dash stub marker** | 0,0 | **0** | **met — stub clause inert** |
| R25 hyphen stub marker | 0,0 | 1 | unmet `failed=binding` (correct) |
| **R26 decoy section wins** | 0,0 | **0** | **met — wrong-table false green** |

## What is NOT broken (negative results, so the L1 can scope the repair)

- Rev-scoped resolution is correct: pointers are resolved against the **measured revision's tree**,
  not the working tree. A pointer present at HEAD but absent at R → `failed=pointers`.
- Malformed paths under a whitelisted prefix (`..`, `//`, glob, trailing space) are all correctly rejected.
- Git does not glob-expand or normalise in `R:path` lookups, so no shell/path-normalisation injection path exists.
- `_git()` uses an argv list (no shell), so no shell-injection surface via pointer text.
- The real landed register's four pointers all resolve (`git_rc=0` each), and the counter issues
  exactly the 4 expected `git cat-file -e` calls — no over- or under-resolution on the real bytes.
- The two contract §9 controls that the counter *does* implement (stub-only register → `binding=bad`;
  nonexistent pointer under a whitelisted prefix → `failed=pointers`) both behave as specified.

## Risks

1. **FINDING 1 is a live false-green class** against the contract's own §9 control. It does not change
   the landed verdict (the real rows use whitelisted prefixes), but a future register edit that moves an
   evidence pointer to `evidence/`, `docs/`, `scripts/`, a bare filename, or an absolute path would
   score `C1=met` while the pointer is unresolvable. The claim's clause (b) is therefore not verified
   by the counter for arbitrary pointer shapes.
2. **FINDING 7 is a contract/implementation mismatch on the frozen target string.** Since the kill
   rule freezes both the counter bytes and the target output, and they disagree, any byte-exact
   comparison of the landed output to the contract's target will fail. This is a claim-validity
   question for the L1, not a repair I can make.
3. **FINDING 6 leaves the round-57 wrong-table defect partially open** — the register selection is
   still first-match-wins over a positional scan, and the key-pair check is a count, not an identity.
4. This seat ran **no** build/lint/test of the lane; per the wave rules the parent owns the
   post-integration gate.

## Blockers

None. All findings are measured against the frozen counter at the freeze revision with exact fixtures,
revs and stdout captured in `Mo58Executor44.receipt.txt`.

## Artifacts

- `.ufo/waves/round-58/w1/Mo58Executor44.md` — this report
- `.ufo/waves/round-58/w1/Mo58Executor44.receipt.py` — reproducible harness (26 arms + real-lane audit)
- `.ufo/waves/round-58/w1/Mo58Executor44.receipt.txt` — its captured output (96 lines)

**Files changed by this seat:** only the three files above (all under
`.ufo/waves/round-58/w1/`). No production file, no corpus registry, no SCORECARD, no LOG, no lane VCS
mutation, no fleet/sibling write.

**Tooling:** no installs or updates were performed this wave; no pacman transaction was run. The
Python standard library and `git` (already present) were the only tools used.
