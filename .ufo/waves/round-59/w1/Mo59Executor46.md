# Mo59Executor46 — SOURCES census manual re-derivation vs census validator

**Seat:** Mo59Executor46 (executor) · **L1:** MoriR59a2
**Lane:** `/home/vgpnk/Projects/shokunin/mori-shokunin`
**Freeze revision:** `60b3a76ad0524c8978cc51922940be1c8c388915`
**Entering revision:** `2b9f03975bfb6e508f35074ac8181ec8bf54e805`
**Lane HEAD at seat time:** `8ff344ff18924c1ea63d46c3b3969f9fea05bc51` ("round-59: validated w1 dispatch payload (64 seats, v2)")
**Scratch root:** `/fast/scratch/hyaku/mori-r59/Mo59Executor46` (created with `mkdir -p`; `TMPDIR` exported to it for every command)

**Scope note.** This seat's item is the census cross-check only. No production file, corpus registry, SCORECARD, LOG, or lane VCS was edited. Every git command ran read-only (`git show`, `git status`, `git rev-parse`, `git worktree list`, `jj status`) against the lane. One `git worktree add` was used to materialise a read-only fixture and was **removed and pruned in the same command** (`git worktree remove --force` + `git worktree prune`); `git worktree list` afterwards shows only the lane itself. The lane is a jj repo (`jj --repository . status` → working copy `ykwoqlwo` / `b8e75096`, parent `xwlyolkx` / `8ff344ff`), whose git view is a detached export by design (`git symbolic-ref -q HEAD` → detached; reflog shows `export from jj`). No commit, no branch move, no lane write.

---

## 1. The claim under test

The contract's Census section (`.ufo/waves/round-59/contract.md`, "## Census") requires:

> `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` at round start and round end (exit 0 required at end; new S rows for the C2 artifacts raise the row count).

This seat independently re-derives the census **by hand** (own parser, not the census script) from the **committed** bytes of `corpus/SOURCES.md`, and compares it to the census validator's output. Both are pasted below.

---

## 2. Committed bytes under test

`corpus/SOURCES.md` is byte-identical at the entering revision, the freeze revision, the current HEAD, and the worktree — so "committed" and "worktree" are the same census input and there is no drift to reconcile.

```
$ git -C mori-shokunin show <rev>:corpus/SOURCES.md | sha256sum
2b9f03975bfb6e508f35074ac8181ec8bf54e805  03f2102b2baa49e5049076f03e8c6dee0d9e7bd3dad1d03cbf168ccfe6ea6a25
60b3a76ad0524c8978cc51922940be1c8c388915  03f2102b2baa49e5049076f03e8c6dee0d9e7bd3dad1d03cbf168ccfe6ea6a25
8ff344ff18924c1ea63d46c3b3969f9fea05bc51  03f2102b2baa49e5049076f03e8c6dee0d9e7bd3dad1d03cbf168ccfe6ea6a25
$ sha256sum mori-shokunin/corpus/SOURCES.md
03f2102b2baa49e5049076f03e8c6dee0d9e7bd3dad1d03cbf168ccfe6ea6a25
```

Structural facts of the file (`corpus/SOURCES.md`, 406 lines):

- H2 sections, in order: `## Registry` (line 3), `## Paths` (334), `## Search log` (344), `## Leads (unopened)` (397). **Exactly one `## Registry` section** (the "unique Registry" the census requires).
- No `###` headings anywhere; the only single-`#` heading is line 1 `# SOURCES — where mori learns`.
- Registry table header at line 5 (`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`), separator at line 6.
- **All 327 registry table lines have indent width 0 and `NF == 13`** (gawk `-F'|'` field count = 11 content cells + 2 edge empties), i.e. every registry row is well-formed.

---

## 3. MANUAL RE-DERIVATION (independent parser, committed bytes)

Parser written from the census script's documented semantics, **not** by invoking gawk or the census script: `/fast/scratch/hyaku/mori-r59/Mo59Executor46/recensus.py`. It re-implements the section gate (`## Registry` opens, any other `#`/`##` closes), the row gate (`^ {0,3}\|`), the header/separator skip, the `NF != 13` malformation test, and the `invalid` bucket rules for tier and status.

```
$ python3 recensus.py HEAD
=== MANUAL RE-DERIVATION (HEAD:corpus/SOURCES.md) ===
bytes_sha256: 03f2102b2baa49e5049076f03e8c6dee0d9e7bd3dad1d03cbf168ccfe6ea6a25
rows	325
tier.A	292
tier.B	14
tier.C	19
tier.invalid	0
status.queued	24
status.mined	272
status.rejected	29
status.invalid	0
malformed_rows(NF!=13)	0
registry_sections	1
duplicate_ids	none
s_rows_outside_registry	none
```

Two further independent counts from plain shell (no census script, no custom parser):

```
$ awk 'NR>=3 && NR<=333' corpus/SOURCES.md | grep -cE '^\| S[0-9]{3,} '
325
$ awk '/^## Registry/{f=1;next} /^## /{f=0} f' corpus/SOURCES.md | grep -cE '^\|'
327            # 325 data rows + header + separator
$ ... | awk -F'|' '{gsub(/^ +| +$/,"",$5); print $5}' | sort | uniq -c
    292 A
     14 B
     19 C
$ ... | awk -F'|' '{gsub(/^ +| +$/,"",$9); print $9}' | sort | uniq -c
    272 mined
     24 queued
     29 rejected
```

---

## 4. CENSUS VALIDATOR OUTPUT (the thing being compared)

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin mori
mori	rows	325
mori	tier.A	292
mori	tier.B	14
mori	tier.C	19
mori	status.mined	272
mori	status.queued	24
mori	status.rejected	29
FLEET	rows	325
FLEET	tier.A	292
FLEET	tier.B	14
FLEET	tier.C	19
FLEET	tier.invalid	0
FLEET	status.queued	24
FLEET	status.mined	272
FLEET	status.rejected	29
FLEET	status.invalid	0
FLEET	missing	0
EXIT=0
```

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
mori	W04	S035 duplicate url raw.githubusercontent.com/systemd/systemd/... across scopes
mori	W04	S037 duplicate url www.freedesktop.org/.../systemd.journal-fields.html across scopes
mori	W04	S073 duplicate url docs.python.org/3/library/pathlib.html across scopes
mori	W04	S074 duplicate url kubernetes.io/docs/concepts/architecture/controller across scopes
mori	W04	S075 duplicate url ftp.gnu.org/gnu/bash/bash-5.3.tar.gz across scopes
mori	W04	S076 duplicate url michaelfeathers.silvrback.com/characterization-testing across scopes
mori	W04	S147 duplicate url raw.githubusercontent.com/can1357/oh-my-pi/... across scopes
mori	W04	S148 duplicate url raw.githubusercontent.com/torvalds/linux/.../fs/proc/base.c across scopes
mori	W04	S149 duplicate url man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html across scopes
mori	W04	S150 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml across scopes
mori	W04	S166 duplicate url raw.githubusercontent.com/torvalds/linux/.../fs/proc/base.c across scopes
mori	W04	S168 duplicate url raw.githubusercontent.com/torvalds/linux/.../Documentation/filesystems/proc.rst across scopes
mori	W04	S201 duplicate url raw.githubusercontent.com/torvalds/linux/.../block/genhd.c across scopes
mori	W04	S218 duplicate url github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch across scopes
mori	W04	S220 duplicate url raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c across scopes
mori	W04	S228 duplicate url docs.python.org/3/library/os.path.html across scopes
mori	W04	S349 duplicate url www.openeuler.org/whitepaper/openEuler%2024.03%20LTS...pdf across scopes
mori	W04	S351 duplicate url www.freedesktop.org/.../journalctl.html across scopes
mori	W04	S470 duplicate url www.freedesktop.org/.../journalctl.html across scopes
mori	W04	S476 duplicate url raw.githubusercontent.com/torvalds/linux/.../mm/oom_kill.c across scopes
mori	W04	S486 duplicate url www.freedesktop.org/.../journalctl.html across scopes
mori	W04	S491 duplicate url raw.githubusercontent.com/torvalds/linux/.../mm/oom_kill.c across scopes
mori	W04	S492 duplicate url raw.githubusercontent.com/torvalds/linux/.../Documentation/filesystems/proc.rst across scopes
mori	W04	S546 duplicate url www.rfc-editor.org/rfc/rfc8259.txt across scopes
mori	W04	S552 duplicate url doi.org/10.1109/TSC.2026.3698682 across scopes
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
EXIT=0
```

Code tally of that validate output: **25 × `W04`, 1 × `ok`, 0 × any `E01`–`E12` code.** (Full captured output: `validate.out` in this seat's scratch; the W04 URLs above are abbreviated only where the line was truncated for width — the ids, codes and scopes are verbatim.)

---

## 5. COMPARISON — manual vs validator

Two comparisons are given: the **committed baseline** (the state this seat was dispatched against) and the **landed state** (after the C2 data landed concurrently — see §9a). Both agree.

### 5a. Committed baseline (`HEAD` = `8ff344ff`, `corpus/SOURCES.md` sha256 `03f2102b…6a25`)

| metric | manual re-derivation | census validator | agree |
|---|---|---|---|
| rows | 325 | 325 | ✅ |
| tier.A | 292 | 292 | ✅ |
| tier.B | 14 | 14 | ✅ |
| tier.C | 19 | 19 | ✅ |
| tier.invalid | 0 | 0 | ✅ |
| status.queued | 24 | 24 | ✅ |
| status.mined | 272 | 272 | ✅ |
| status.rejected | 29 | 29 | ✅ |
| status.invalid | 0 | 0 | ✅ |
| malformed rows (NF≠13) | 0 | 0 (`E01` count = 0) | ✅ |
| `## Registry` sections | 1 | 1 (single `mori ok` line) | ✅ |
| duplicate ids | none | 0 (`E03` count) | ✅ |
| S-rows outside Registry | none | 0 (`E12` count) | ✅ |
| validate exit code | — | 0 | ✅ |

**Every metric agrees exactly. No discrepancy found.** Row total also matches the round-58 spot-check's recorded end-of-round figure of 325 (`corpus/lessons/round-58-verifier-spotcheck.md:79`), i.e. the registry was unchanged since round 58 at dispatch — consistent with the contract's note that new S rows arrive only with the C2 artifacts.

### 5b. Landed state (after the C2 rows + entry landed)

| metric | manual re-derivation | census validator | agree |
|---|---|---|---|
| rows | 333 | 333 | ✅ |
| tier.A | 297 | 297 | ✅ |
| tier.B | 16 | 16 | ✅ |
| tier.C | 20 | 20 | ✅ |
| tier.invalid | 0 | 0 | ✅ |
| status.queued | 24 | 24 | ✅ |
| status.mined | 279 | 279 | ✅ |
| status.rejected | 30 | 30 | ✅ |
| status.invalid | 0 | 0 | ✅ |
| malformed rows (NF≠13) | 0 | 0 (`E01` count = 0) | ✅ |
| `## Registry` sections | 1 | 1 | ✅ |
| duplicate ids | none | 0 | ✅ |
| validate exit code | — | 0 | ✅ |

The rise is 325 → 333 = exactly 8 new rows (`S553`–`S560`): 7 `mined` (`status.mined` 272 → 279) and 1 `rejected` (`status.rejected` 29 → 30), with `tier.A` +5, `tier.B` +2, `tier.C` +1 — all consistent with the landed rows.

Full fleet census (same command, no lane argument) also exits 0: `FLEET rows 3667, tier.A 3053, tier.B 474, tier.C 140, tier.invalid 0, status.queued 280, status.mined 3137, status.rejected 250, status.invalid 0, missing 0`.

---

## 6. The "0 malformed" result is a LIVE detector, not a dead one

A zero count is only meaningful if the detector can produce a non-zero. Two probes on throwaway scratch fixtures (each `git init -q` at an explicit scratch path; `git -C <path>` only):

**Probe A — malformed row is caught.** Fixture with one 11-column row and one 10-column row:

```
$ sources-census.sh validate --file $D/corpus/SOURCES.md --today 2026-10-28
file	W03	S001 mined but unused
file	E01	S002 fields=10
EXIT=1
```

`E01 fields=10` fires on exactly the short row. The `rows` metric still counts it (`file rows 2`) because the census counts a row before the `NF` test — confirmed identical in my parser.

**Probe B — differential equivalence, 19 adversarial fixtures.** `difftest.py` generates 19 edge-case registries and compares my parser's rows / tier histogram / status histogram / malformed count against the census script's `census` mode and its `E01` findings:

```
plain-3-rows                 PASS   one-malformed-13col          PASS
header-only                  PASS   one-malformed-9col           PASS
one-malformed-10col          PASS   pipe-inside-cell             PASS
one-malformed-12col          PASS   bad-tier                     PASS
row-outside-registry         PASS   bad-status                   PASS
indented-2sp-row             PASS   indented-4sp-row             PASS
h3-inside-registry           PASS   second-registry-section      PASS
no-registry-at-all            PASS   duplicate-ids                PASS
trailing-no-newline          PASS   all-statuses                 PASS
all-tiers                    PASS

DIFF_FAILURES=0 of 19
```

Covered semantics that match: 10/12/13/9-column rows, `|` inside a cell, tier/status outside the enums (→ `invalid` bucket), a row outside `## Registry`, 2-space vs 4-space indentation (4-space is correctly *not* a row), an `###` heading inside the Registry (correctly does **not** close the section), two `## Registry` sections, no `## Registry` at all, duplicate ids, and a file with no trailing newline.

**Conclusion: the census validator and the manual re-derivation are semantically equivalent on this corpus, and both report the registry as clean.**

---

## 7. Forward check — the round-end census gate, simulated

The contract requires the round-end census to exit 0 **after** the C2 S rows land. The C2 counter binds those rows tightly (`count-c2.py:180-190`): for each cited `S###` id, the registry row must have `cells[7] == "mined"` and `cells[10] == "corpus/knowledge/wave-settlement-artifacts-r59.md"` (the entry path), and `count-c2.py` requires the entry file to exist for its pin/span checks. The census's own `E11` rule (`sources-census.sh:538-572`) independently requires every `mined` row's `used-by` path to exist on disk.

Simulated on a full copy of the lane tree (scratch `fixture-clean.*/lane`, `cp -a` of `corpus/` + `tools/` + `SKILL.md`/`PROVINCE.md`/`SCORECARD.md`/`README.md`):

- Baseline copy → `validate` exit **0**, 25 W04, 0 E-codes; census `rows 325 / tier.A 292 / tier.B 14 / tier.C 19 / status.mined 272 / queued 24 / rejected 29` — identical to the live lane. The copy reproduces the baseline exactly, so the fixture is faithful.
- Append 3 C2-shaped rows (`S553`/`S554`/`S555`, status `mined`, `used-by corpus/knowledge/wave-settlement-artifacts-r59.md`) **with the entry file absent** → `E11` fires on all three, `validate` exit **1**.
- Same 3 rows **with the entry file present** → `validate` exit **0**, 25 W04, 0 E-codes; census `rows 328 / tier.A 295 / tier.B 14 / tier.C 19 / status.mined 275 / queued 24 / rejected 29`.

**So the round-end census gate is satisfiable, and the binding constraint is exactly one thing: the C2 entry file `corpus/knowledge/wave-settlement-artifacts-r59.md` must exist on disk at the moment the C2 S rows are added.** The C2 counter already requires that file (it is the entry it evaluates), so the two requirements are consistent — but the ordering matters: **rows must not land before the entry file, or the interim census goes red on `E11`.**

### 7b. A second round-end hazard: `E04`, not just `E11`

`E04` (duplicate URL **within** the same scope, non-rejected, no `supersedes S###` in the `teaches` cell) is an **error** code and fails validation. This is directly reachable from the C2 work, because the C2 registry rows cite the same settlement artifacts as their sources. Probed on the scratch copy:

- A new row carrying the **same URL but a different scope string** → only `W04` (across scopes), exit **0**. Harmless.
- A new row carrying the **same URL and the same scope string** as an existing non-rejected row (I cloned `S478`'s URL + scope, status `mined`, no `supersedes`) → `E04 … duplicate url ieeexplore.ieee.org/…/11540439.pdf within scope …`, plus `E07`/`E08` from the deliberately malformed clone columns, exit **1**.

**Hazard for the C2 author:** if two of the new C2 registry rows cite the same artifact URL under an identical scope string, the round-end census goes red on `E04`. Give each new row a distinct scope string, or make the later row carry `supersedes S###` in its `teaches` cell (the census exempts that case), or mark the superseded row `rejected`.

### 7c. Second `S552`-style duplicate — REMEDIATED during this seat's run

`S552` (line 332) and `S478` (line 257) carry the **same paper, the same page-3016 paragraph, and the same PDF sha256 `1603404dd25b3a0dff93f2dcb23c75b671d4e2d78da3cce8f461e87ebde6add2`**; `S262` (line 243) carries the same DOI. This is the round-58 routed defect #2 (`corpus/lessons/round-58-verifier-spotcheck.md:85`).

**At the start of this seat's run the defect was open** (no `## Mistakes` section in `corpus/SOURCES.md`; no reconciliation paragraph naming `S478`; no round-59 lesson; `corpus/QUALITY.md`'s last criterion still 154). **By the end of the run a concurrent sibling had landed the remediation** — registry row `S560` (line 340), `supersedes S552 — duplicate of S478 …`, status `rejected`, tier `C`, `used-by corpus/lessons/round-59.md` — which is exactly the "appended reconciliation, do not rewrite S552" shape the defect asked for. `S552` itself is unchanged. The census continues to surface the underlying overlap only as the non-fatal `W04 duplicate url doi.org/10.1109/TSC.2026.3698682 across scopes`, which is correct: the row is now `rejected`, so the E04 within-scope duplicate exemption applies (`count` semantics: `status != "rejected"` guard at `sources-census.sh:655`).

`corpus/lessons/round-59.md` and a QUALITY criterion above 154 were still absent when this seat finished; they are the remaining pieces of defect #2 and are **not** visible to the census validator.

---

## 8. Counter runs (frozen counters, read-only, scratch-isolated)

**At dispatch (committed `HEAD`, data not yet landed):**

```
$ python3 .ufo/waves/round-59/count-c1.py HEAD --scratch .../c1
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=HEAD          EXIT=0

$ python3 .ufo/waves/round-59/count-c2.py HEAD --scratch .../c2
C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=bad rows=bad pins=bad tree=bad claims=0 files=0 rev=HEAD
failed=copy_absent:corpus/evidence/sources-r59/w1-results-r54.json, … r58.json, … w1-settlement-r58.json, entry_absent, tree   EXIT=1

$ python3 .ufo/waves/round-59/count-c1.py --selftest
C1_SELFTEST pass=6 fail=0                                           EXIT=0
$ python3 .ufo/waves/round-59/count-c2.py --selftest
C2_SELFTEST pass=9 fail=0                                           EXIT=0
```

C2 was `unmet` at dispatch **only because the data had not landed yet** — the entry, the copies and the rows were all absent from the *committed* tree. This is the expected pre-data state, not a defect in the counter.

**Against the landed state (§9a) — a scratch clone of the lane with the sibling's landed data committed, since the counters read committed bytes via `git show <rev>:<path>`:**

```
$ python3 .ufo/waves/round-59/count-c2.py HEAD --repo <landed snapshot> --scratch …
C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=bad rows=ok pins=ok tree=ok claims=14 files=7 rev=HEAD failed=entry   EXIT=1
      ↳ reason: files:outside=corpus/evidence/sources-r59/w1-results-r53.json   (defect B)

$ python3 .ufo/waves/round-59/count-c1.py HEAD --repo <landed snapshot> --scratch …
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=HEAD                                                               EXIT=0

# after the two fixes (K11 claim → prose; literal pipe removed from S560):
$ python3 .ufo/waves/round-59/count-c2.py HEAD --repo <fixed snapshot> --scratch …
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 rev=HEAD                     EXIT=0

# final snapshot of the live lane as it stands at seat end:
$ python3 .ufo/waves/round-59/count-c2.py HEAD --repo <final live snapshot> --scratch …
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 rev=HEAD                     EXIT=0
$ python3 .ufo/waves/round-59/count-c1.py HEAD --repo <final live snapshot> --scratch …
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=HEAD                                                               EXIT=0
```

Every counter invocation used `--scratch` under this seat's scratch root and `--repo` pointing at a **scratch clone**; the lane working copy was never a counter target.

Supporting observations:

- The C2 copies had already appeared in the **worktree** (`corpus/evidence/sources-r59/`, untracked in jj) from a concurrent sibling. I verified each is **byte-equal** to its `.ufo` artifact at `HEAD`:

  | copy | sha256 | `.ufo` artifact | equal |
  |---|---|---|---|
  | `w1-results-r53.json` | `0d644e0f…584260` | `.ufo/waves/round-53/w1-results.json` | ✅ |
  | `w1-results-r54.json` | `ea48a0cc…59335f` | `.ufo/waves/round-54/w1-results.json` | ✅ |
  | `w1-results-r55.json` | `2e5b0a0f…89763b` | `.ufo/waves/round-55/w1-results.json` | ✅ |
  | `w1-results-r56.json` | `19536201…5d761` | `.ufo/waves/round-56/w1-results.json` | ✅ |
  | `w1-results-r57.json` | `29e7a35d…beb1` | `.ufo/waves/round-57/w1-results.json` | ✅ |
  | `w1-results-r58.json` | `a57b660d…fc61fc` | `.ufo/waves/round-58/w1-results.json` | ✅ |
  | `w1-settlement-r58.json` | `b259e73c…b5588` | `.ufo/waves/round-58/evidence/w1-settlement.json` | ✅ |

  Note the r53 copy is byte-equal to its artifact too — but `count-c2.py`'s `ARTIFACTS` map admits only r54–r58 + `w1-settlement-r58`, and r53 is the deliberate **drift** file (`DRIFT_SCAN = [".ufo/waves/round-53/w1-results.json"]`, `count-c2.py:75`). An r53 copy present in `corpus/evidence/sources-r59/` is harmless but is **not** a citable artifact; a claim naming it would trip `files:outside=…`.
- The C1 and C2 tool pins match the contract exactly:
  `tools/mori-register-check.py` → `38b733d896f880f5b7ecb464848b80798810ab052fcf0a8afb320918151472b8` ✅
  `tools/mori-settlement-scan.py` → `4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9` ✅
- **Frozen bytes intact** (kill rule): `contract.md`, `count-c1.py`, `count-c2.py` each hash **identically** at the freeze revision `60b3a76a`, at `HEAD`, and in the worktree — no post-freeze mutation of counter bytes, contract bytes, or predicates.

---

## 9. Findings

**F1 — Census re-derivation matches the validator exactly; registry is clean.** Manual and validator agree on every metric: 325 rows, tier A/B/C = 292/14/19 (invalid 0), status queued/mined/rejected = 24/272/29 (invalid 0), malformed 0, one `## Registry`, no duplicate ids, no rows outside the Registry, `validate` exit 0. Equivalence is backed by a 19-case differential test (0 failures) and by a proof that the malformed detector is live (`E01 fields=10` on a deliberately short row). **No census defect.**

**F2 — Round-end census gate depends on file ordering.** The census's `E11` rule and the C2 counter's `used-by`-binding both require `corpus/knowledge/wave-settlement-artifacts-r59.md` to exist. The C2 S rows must not land before that file, or the interim round-end census exits 1 with `E11` on each new row. Verified in both directions on a scratch copy.

**F3 — `E04` is a second, less obvious round-end hazard.** Two new C2 registry rows sharing one artifact URL under an identical scope string (and no `supersedes`) fail validation with `E04`. Distinct scope strings, a `supersedes S###` marker, or `rejected` status avoids it. **Recommendation to the C2 author: give each new row a distinct scope string.**

**F4 — Round-58 routed defect #2 (S552 duplicate row) was remediated during this seat's run** by a concurrent sibling (registry row `S560`, `supersedes S552 — duplicate of S478 …`, status `rejected`; `S552` left untouched as the defect required). The remaining pieces — `corpus/lessons/round-59.md` and a QUALITY criterion above 154 — were still absent when this seat finished, and are invisible to the census validator.

**F5 — The lane's census posture is otherwise healthy.** `FLEET missing 0`, `tier.invalid 0`, `status.invalid 0`, full-fleet census exit 0, and the census script's own selftest passes (`selftest ok`, exit 0, all `killed` mutants) — the validator is not merely present but mutation-checked.

---

## 9a. LIVE-STATE RE-CHECK — two real defects found in the landed C2 data

The C2 data landed in the lane **while this seat was running** (jj working copy went from clean to `M corpus/SOURCES.md` + untracked `corpus/evidence/sources-r59/`, then `corpus/knowledge/wave-settlement-artifacts-r59.md`). Because the contract's census is a **round-end** gate, this seat re-ran everything against the landed state. **Two genuine defects surfaced, one of which was a live round-end census failure.**

### Defect A — a literal `|` inside a cell splits the row and turns the round-end census RED (`E01`)

The `S560` reconciliation row as first landed contained the routed-defect sweep command with a **backslash-pipe**:

```
| S560 | supersedes S552 — … | paper | C | … | round-58 verifier spot-check (…); `grep -n '10.1109/TSC.2026.3698682\|1603404d' corpus/SOURCES.md` shows S262, S478, S552 | …
```

The census splits registry rows with `gawk -F'|'` and **has no escape handling**, so the `\|` inside the anchor cell is treated as a real column separator:

```
$ sed -n '340p' corpus/SOURCES.md | tr -cd '|' | wc -c
12                                     # 13 pipes → NF=14, one too many
$ awk -F'|' '{print NF}'  <<< '| a | b\|c | d |'
6                                     # gawk splits on the backslash-pipe too
$ sources-census.sh validate --root <lane> mori
mori	E01	S560 fields=12
EXIT=1                              # ← ROUND-END CENSUS GATE WAS RED
```

Two census metrics were corrupted by the same single character: `E01 S560 fields=12` and `status.invalid 1` (the row's `status` cell was read from the wrong column, so `rejected` was not recognised — the histogram showed `status.rejected 29` + `status.invalid 1` instead of `rejected 30`).

**Root cause is generic, not specific to `S560`: any registry cell containing a literal `|` — escaped or not — is silently split, and the row then fails `E01` and mis-files its `status`/`tier` cells.** The rest of the registry is clean (a scan of every registry row for `NF != 13` found **only** line 340), and the wider corpus does use `\|` inside markdown tables elsewhere (`corpus/knowledge/journal-alarm-routing-r14.md:162`, `corpus/knowledge/lane-silence-r2.md:58`) — so the hazard is real and recurring, not a one-off.

**Fix (verified):** the pipe must be removed from the cell entirely; `gawk -F'|'` cannot be taught to honour an escape. The sibling's landed fix was to rewrite the sweep as `grep -n -e '10.1109/TSC.2026.3698682' -e '1603404d' corpus/SOURCES.md` — two `-e` patterns, no pipe. That is the shape to use: **`grep -n -e A -e B` instead of `grep -n 'A\|B'`.**

Verified in scratch: with the pipe removed, `validate` → exit 0, `E01` gone, `status.rejected 30`, `status.invalid 0`, census `rows 333 / tier.A 297 / tier.B 16 / tier.C 20 / status.mined 279 / queued 24 / rejected 30`. **The live lane now passes** (`CENSUS_EXIT=0`, `NF=13` for `S560`).

### Defect B — a claim citing the r53 drift-control copy is outside the frozen `ARTIFACTS` set (`C2` `entry=bad`)

The C2 entry cited the r53 copy in a pin-bound claim:

```
- **K11** — the round-53 artifact's member entries carry a report_file field … Quote: `   "report_file": ".ufo/waves/round-53/w1/Mo53Fr01.md"` (corpus/evidence/sources-r59/w1-results-r53.json:line:16; pin 0d644e0f…)
```

But the frozen `ARTIFACTS` map (`count-c2.py:59-68`) admits only r54–r58 plus `w1-settlement-r58` — **r53 is deliberately excluded, because r53 is the counter's drift control** (`DRIFT_SCAN = [".ufo/waves/round-53/w1-results.json"]`, `count-c2.py:75`): it is the file that MUST scan FAIL (`report_file` extra key = schema drift, reported not fixed). Citing it as a citable pinned copy is therefore outside the frozen set:

```
$ python3 .ufo/waves/round-59/count-c2.py HEAD --repo <snapshot>
C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=bad rows=ok pins=ok tree=ok claims=14 files=7 rev=HEAD failed=entry
$ # eval_entry reasons:
files:outside=corpus/evidence/sources-r59/w1-results-r53.json
```

The observation itself is sound (r53 line 16 really is `   "report_file": ".ufo/waves/round-53/w1/Mo53Fr01.md"`, and r58 line 16 is a different key) — it is the *pin-bound claim* form that is inadmissible, because the r53 copy is not in `ARTIFACTS`.

**Fix (verified):** keep the observation as prose (no `**K<n>` claim marker, no `Quote:` trigger) so it survives the `grammar:` detector while remaining outside the pin-bound claim set. Two fixes verified green:

| fix | counter verdict | `eval_entry` |
|---|---|---|
| drop the `K11` line outright | `C2=met … claims=13 files=6` exit 0 | ok, no reasons |
| rewrite `K11` as prose (no `**K`, no `Quote:`) | `C2=met … claims=13 files=6` exit 0 | ok, no reasons |

**The live lane now passes** — the `K11` claim line is gone (only a prose mention of "K11's absence claim" remains at line 43) and the final snapshot verifies:

```
$ python3 .ufo/waves/round-59/count-c2.py HEAD --repo <final live snapshot>
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 rev=HEAD   EXIT=0
$ python3 .ufo/waves/round-59/count-c1.py HEAD --repo <final live snapshot>
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=HEAD                                             EXIT=0
```

### Manual re-derivation on the LANDED file also agrees

```
$ python3 recensus.py --file <lane>/corpus/SOURCES.md
bytes_sha256: 46c333d2e90fbc61ecd3c6486975990e3dd94a35931369420c95244fe30b2d63
rows	333          tier.A 297   tier.B 16   tier.C 20   tier.invalid 0
status.queued 24  status.mined 279  status.rejected 30  status.invalid 0
malformed_rows(NF!=13)	0        registry_sections	1
duplicate_ids	none             s_rows_outside_registry	none
```

Validator on the same file: `rows 333 / tier.A 297 / tier.B 16 / tier.C 20 / status.mined 279 / queued 24 / rejected 30` — **identical, and `validate` exit 0.** The round-end row count rose 325 → 333 exactly as the contract predicted ("new S rows for the C2 artifacts raise the row count"): 8 new rows (`S553`–`S560`), of which 7 are `mined` and 1 is `rejected`.

### Defect C (counter property, not a lane defect) — `entry_ok` ignores `grammar:` reasons

While testing fix variants I found an asymmetry inside the frozen counter that is worth recording, even though the counter bytes are immutable and the lane cannot act on it:

- The **tree arm** uses `eval_entry`'s boolean `ok` (`count-c2.py:349`), which counts **all** reasons including `grammar:` — so hostile tree `t12-malformed-claim` (`expect.txt` = `grammar`) correctly fails.
- The **entry arm** computes `entry_ok` from a **prefix whitelist** that omits `grammar` (`count-c2.py:304-307`: `not any(r.startswith(("frontmatter", "distinct", "claims_min", "files", "span", "entry_absent")))`).

Demonstrated: with the K11 claim dropped, inserting a malformed claim line (`- **KBAD** — … Quote: \`no pin tuple here\` (not-a-pin)`) **after** the frontmatter yields `eval_entry ok=False, reasons=['grammar:- **KBAD** …']` yet the counter reports **`C2=met … entry=ok`**, exit 0. The malformed line is neither counted as a claim nor able to fail the entry arm.

This is a *latent* weakness, not an active false-green in the current lane: the live entry has **no** malformed claim line (verified: `C2=met … claims=13 files=6` and `eval_entry` returns no reasons at all), and the frozen `t12` tree still covers the grammar path for the trees arm. Recording it so the next round's freeze does not inherit the same asymmetry. **No lane action is available or needed** — the counter is frozen and its bytes are verified intact.

---

## 9b. Final state summary (live lane, at seat end)

| check | command | result |
|---|---|---|
| mori census | `sources-census.sh census --root … mori` | `rows 333, tier.A 297, tier.B 16, tier.C 20, status.mined 279, queued 24, rejected 29→30, invalid 0` — exit 0 |
| mori validate | `sources-census.sh validate --root … mori` | **exit 0**, 25 × `W04`, 1 × `ok`, **0 E-codes** |
| manual re-derivation | `recensus.py --file corpus/SOURCES.md` | identical on every metric; malformed 0 |
| fleet census | `sources-census.sh census --root …` (no lane) | `FLEET rows 3675, tier.invalid 0, status.invalid 0, missing 0` — exit 0 |
| C1 counter | `count-c1.py HEAD --repo <snapshot>` | `C1=met selftest=ok fixtures=ok real=ok pointers=ok` — exit 0 |
| C2 counter | `count-c2.py HEAD --repo <snapshot>` | `C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6` — exit 0 |
| C1 selftest | `count-c1.py --selftest` | `C1_SELFTEST pass=6 fail=0` — exit 0 |
| C2 selftest | `count-c2.py --selftest` | `C2_SELFTEST pass=9 fail=0` — exit 0 |
| census selftest | `sources-census.sh selftest` | `selftest ok` — exit 0 |
| frozen bytes | sha256 of contract + both counters at freeze rev / HEAD / worktree | identical — kill rule intact |
| tool pins | `tools/mori-register-check.py`, `tools/mori-settlement-scan.py` | match the contract's `38b733d8…472b8` and `4c04bf21…5ac9a9` |
| fixture counts | `.ufo/waves/round-59/fixtures-c1/`, `trees-c2/` | 13 and 12 — both counters' arms report `fixtures=ok` / `trees=ok` |

---

## 10. Evidence index

| Artifact | Path (this seat's scratch; cleaned on yield) |
|---|---|
| Manual re-derivation parser | `recensus.py` |
| Manual census output (baseline) | `manual-census.out` |
| Manual census output (landed) | `manual-census-landed.out` |
| Census validator output (mori, validate) | `validate.out`, `validate-final.out`, `validate-post.out` |
| Census output (mori + fleet) | `mori-census.out`, `fleet-census.out` |
| Differential fuzz harness | `difftest.py`, `difftest.out` (19/19 PASS) |
| Counter outputs | `c1.out`, `c2.out` |
| Scratch fixtures | `fixture-malformed.*`, `fixture-clean.*`, `fixture-r59rows.*`, `clone-landed.*`, `clone-live2.*`, `clone-gram.*`, `clone-fix.*`, `clone-final.*` (all `git init -q` / `git clone` at explicit scratch paths; `git -C` only) |

All scratch content is under `/fast/scratch/hyaku/mori-r59/Mo59Executor46/` and was removed on yield. Nothing was written to the fleet root, sibling repos, `~/.local/bin`, or any PATH directory; the only lane write was this report at `.ufo/waves/round-59/w1/Mo59Executor46.md`.

## 11. Risks / blockers

- **No blocker.** The census claim is verified as stated, on the committed baseline *and* on the landed state, by two independent methods.
- **Both live defects are resolved in the lane as of seat end** (defect A's `S560` pipe, defect B's `K11` r53 claim). The final live snapshot verifies `C1=met` and `C2=met`, `validate` exit 0, 0 E-codes.
- **Recurrence risk (defect A):** any future registry cell containing a literal `|` — even escaped `\|` — silently splits the row, failing `E01` and mis-filing the `status`/`tier` cells. `gawk -F'|'` cannot be taught to honour an escape, so the pipe must be **removed** from the cell (use `grep -n -e A -e B`, or prose). The wider corpus already contains `\|` inside markdown tables (`corpus/knowledge/journal-alarm-routing-r14.md:162`, `corpus/knowledge/lane-silence-r2.md:58`), so this is a recurring hazard, not a one-off. **Recommendation: the L1 should scan every registry row for `NF != 13` at round end, not only rely on the census exit code** — the exit code did catch it here, but the histogram corruption (`status.invalid 1`) shows the blast radius is wider than one row.
- **Residual defect-#2 pieces (F4):** `corpus/lessons/round-59.md` and a QUALITY criterion above 154 are still absent. The census cannot see them; the integrator's spot-check must.
- **Latent counter property (defect C):** the frozen C2 counter's `entry_ok` whitelist omits `grammar:`, so a malformed claim line in the *real* entry cannot fail the entry arm (the trees arm does catch it). The counter is frozen and its bytes are verified intact — **no lane action is available**, and the current entry has no malformed line. Recorded so the next round's freeze does not inherit the same asymmetry.
- **Ordering risk (F2, F3):** the round-end census is satisfiable but order-sensitive — C2 rows must not land before `corpus/knowledge/wave-settlement-artifacts-r59.md` exists (else `E11`), and no two new rows may share one URL under an identical scope string (else `E04`).
