# Mo61SimplC1 — dead code / unused arms / needless complexity in the r61 frozen counters

**Seat:** Mo61SimplC1 (simplification axis, advisory only) · **Lane:** mori-shokunin · **Round:** 61
**Frozen bytes audited (unmodified, verified):**
`.ufo/waves/round-61/count-c1.py` sha256 `a6684e697583746e8b6318d6984f3ada5e619c45a0a3449ecf46d79193433e00`,
`.ufo/waves/round-61/count-c2.py` sha256 `82d0fee6124685f8a50f93550f3665703a33dce644948958db642a77d5aec2d8`
— both identical to the freeze commit `7370a731abcafc4c803111de7c22cd6264d63be1`
(`git -C … diff --stat 7370a731 -- …/count-c1.py …/count-c2.py` → empty; `git show 7370a731:<path> | sha256sum` reproduces both digests).
**No edits, no commits, no VCS mutation, no production/sibling/fleet writes.** All fixtures were throwaway git repos created at
`/fast/scratch/hyaku/mori-r61/Mo61SimplC1/` (asserted `git -C "$D" rev-parse --show-toplevel` == the fixture dir before every commit).
**Method:** full read of both counters (224 + 306 lines), `python3 -m trace` line coverage of each selftest battery, three isolated
falsification fixtures for `count-c1.py`, one range-semantics probe for `count-c2.py`, and live runs of both counters at the entering
revision `325f7e639916fcbc77fa2ec7475951a1b86bb1cb` and at the freeze revision. Disk guard was green before heavy work
(`/fast/scratch/hyaku` 354.6 G free); no tool was installed or upgraded (nothing to install — `python3` 3.14 and `trace` are stdlib).

---

## F1 — `count-c2.py --selftest` is RED at the counter's own default floor; the committed receipt was produced with `--floor 0`

`count-c2.py:38` sets `FLOOR_DEFAULT = 40` and `count-c2.py:291` wires it as the `--floor` default, but the synthetic battery builds a source
entry from one sentence repeated 22× (`count-c2.py:212-213`), which `enumerate_pointers()` deduplicates to **6** distinct pointers. The
floor check at `count-c2.py:183-184` therefore fires in every case, including the intended-green "good" case. Observed at the frozen bytes
(`python3 .ufo/waves/round-61/count-c2.py --selftest --scratch <scratch>`): `case good: ok=False want=True FAIL failed=['pointer_floor:6<40']`,
`C2_SELFTEST pass=9 fail=1`, `rc=1`. The same bytes with `--floor 0` print `C2_SELFTEST pass=10 fail=0`, `rc=0`, and that output is
**byte-identical** to the committed receipt `.ufo/waves/round-61/evidence/selftest-c2.txt` (`diff` of the receipt against my `--floor 0` run
shows only the receipt's extra `rc=0` trailer line; `diff` against the default-floor run differs on all 11 case lines). The contract's
`## Selftests` section asserts "a red selftest blocks dispatch", and the documented counting command carries no `--floor`, so the
red/green status of the frozen battery depends on an undeclared flag. This is a reporting defect in the frozen claim, not a code change to
apply: the receipt should state the floor it was run with, or the fixture should carry ≥40 distinct pointers.

## F2 — the C1 gate set is not pinned to the measured revision, and the committed C1 control is reproducible only through that unpinned path

`count-c1.py:208-211` reads the manifest from the **working tree** whenever `--manifest` is an absolute path to an existing file, and only
from `git show <rev>:<path>` otherwise. `gate-manifest.json` was introduced by the freeze commit itself
(`git log --diff-filter=A -- .ufo/waves/round-61/gate-manifest.json` → `7370a731…`; `git ls-tree 325f7e63… .ufo/waves/round-61/` → empty),
so **no manifest exists at the entering revision**: the documented command
`python3 .ufo/waves/round-61/count-c1.py 325f7e63… --repo <lane> --scratch <scratch>` prints
`C1=unmet gates=0 registered=0 missing=0 … failed=manifest_unreadable rev=325f7e63…` (rc=1), whereas the contract's frozen before-state
for C1 reads "`C1=unmet gates=25 registered=0 missing=25 …`". The committed control receipt
`.ufo/waves/round-61/evidence/control-c1-do-nothing.txt` shows exactly `gates=25 registered=0 missing=25 … rev=325f7e63…`, and I reproduced
that line **byte-identically** only by passing the working-tree manifest absolutely:
`python3 .ufo/waves/round-61/count-c1.py 325f7e63… --repo <lane> --manifest <lane>/.ufo/waves/round-61/gate-manifest.json` →
first line identical to the receipt (`diff` → identical), rc=1. Consequence: the "25 gates" of the frozen met line is not bound to any
committed bytes by the counter; a future run can point `--manifest` at an arbitrary file and obtain `gates=N` for any N. The pinning idiom
that C3 already uses for `count-c1.py`/`count-c2.py` shas (contract §C3 target (d)) is the natural future-round repair — not applied here.

## F3 — `row_hits()` has a dead exact-token branch, and its effective semantics are raw substring matching

`count-c1.py:62-70` computes `toks` (a backtick-stripped, whitespace/paren/comma-split token list) and then tests
`if path in toks or path in r["entry"]` (`count-c1.py:68`). Every token is a contiguous substring of the entry cell after the replacements, so
`path in toks` **implies** `path in r["entry"]` — the `toks` computation and its test are dead work, and the apparent exactness of the token
match is discarded by the `or`. What survives is a raw substring test, which registers gates that no row names: in an isolated fixture
(manifest `["tools/g.py"]`, one registry row whose entry cell names `tools/g.pyc`, both files present) the frozen counter prints
`C1=met gates=1 registered=1 … failed=none` (rc=0) — a gate whose entry cell names a *different* file counts as registered. The same
substring semantics let a **directory** path be treated as a gate: with manifest `["tools"]` and one row naming `tools/g.py`, the counter
prints `C1=met gates=1 registered=1 …` (rc=0) and `git show <rev>:tools` returns a tree listing with rc=0. A one-line change
(`path in r["entry"]` → exact-token or whole-cell comparison) would remove both artifacts; the redundant `toks` branch would go with it.

## F4 — a path whose only row is superseded is counted as *registered*, contradicting the contract's kill rule

`count-c1.py:96-98` filters out rows whose **name** or **scope** cell contains "supersed", and `count-c1.py:103` then falls back
`row = live[0] if live else hits[0]` — i.e. when *every* hit is superseded, the superseded row is used for the cell checks and the gate is
counted in `res["registered"]`. The contract's C1 kill rule says the claim fails if "any manifest path has **no conformant row**", and the
target says the tables must "hold exactly one **non-superseded** row". Isolated fixture (manifest `["tools/sub/x.py"]`, one row whose scope
cell is `superseded: see next row`, file present) → `C1=met gates=1 registered=1 missing=0 thin=0 dup=0 unres=0 noselftest=0 noowner=0
failed=none` (rc=0). The frozen selftest's own "superseded-ok" case encodes this behaviour as *expected green*
(`count-c1.py:146` + `count-c1.py:156`), so the defect is inside the frozen battery, not just in the implementation. Note the supersession
detection only inspects the `name` and `scope` cells — a registry row that marks supersession in the *verdict* column would be counted as
live and would trigger `dup` against the replacement row.

## F5 — `noowner` is a dead metric that is nevertheless printed in the frozen met line

`res["noowner"]` is initialised to 0 at `count-c1.py:75` and `count-c1.py:214`, printed at `count-c1.py:127`, and **never incremented
anywhere** in the file (grep of `noowner` in the frozen bytes returns exactly those three lines). The empty-owner case is in fact caught by
the generic thin-row check (`count-c1.py:104-108`, `empty = [k for k in CELLS if not row[k]]`, `CELLS` contains `"owner"`), so the
`noowner=0` token in the contract's frozen met line `… noselftest=0 noowner=0 rev=<rev>` is a constant that carries no measurement.
Grep-level proof: `grep -n noowner count-c1.py` → `75: "unres": 0, "noselftest": 0, "noowner": 0, "failed": []`, `127: f"noselftest=… noowner=…`,
`214: … "noowner": 0,`. Cost of the dead field: one more token in a met line that seats will string-match.

## F6 — two of `count-c1.py`'s failure arms are never exercised by the frozen selftest, and the "unres" case does not test `unres`

Line coverage of the frozen battery (`python3 -m trace --count --file=count-c1.cover count-c1.py --selftest --scratch <scratch>`) shows
`count-c1.py:100-101` (`res["dup"] += 1` / `failed.append("dup:…")`) and `count-c1.py:114-115` (`res["unres"] += 1` /
`failed.append("unres:…")`) with **no execution count** — never reached. The reason is visible in the case table: the "unres" case
(`count-c1.py:157`) pairs the `GOOD` row with manifest path `tools/nothere.py`, which no row names, so the case exits through the
`missing` arm instead; the battery prints `case unres: ok=False want=False pass failed=['missing:tools/nothere.py']` — the label promises
the unresolved-path arm and exercises the missing-path arm. The `dup` arm is likewise unreached (the "thin" case uses two rows naming two
*different* paths, so no path has two hits). Both arms are reachable in the implementation — my directory fixture did fire
`failed=dup:tools/g.py,dup:tools` — but the frozen battery cannot detect a regression in either.

## F7 — three of `count-c2.py`'s failure arms are never exercised by the frozen battery

The same trace run over `count-c2.py` (`--file=count-c2.cover`) shows `count-c2.py:112` (`copy_absent:{f}`), `count-c2.py:157`
(`loc_oob:{anchor}`) and `count-c2.py:170` (`registry_absent`) with no execution count: the synthetic fixture always writes all four copies,
never writes an out-of-range location, and always writes `corpus/SOURCES.md`. The arms that do fire (`loc_bad` ×2, `copy_pin` ×1,
`quote_missing` ×1, `rows_src` ×8, `sources_floor` ×1, `provenance` ×1, `rows_ne_pointers` ×2) are all reachable from the case table.
Combined with F1, the frozen C2 battery proves 9 of 10 cases for reasons unrelated to the case under test (the floor trips in every case),
and never proves the copy-absence, out-of-range or registry-absence branches.

## F8 — stale tool name in the C1 docstring, and a resolution check that accepts trees

`count-c1.py:11` states the counter materializes paths "via `git show` / `git cat-file -e`", but the implementation only ever calls
`git show` (`count-c1.py:29-38`); `cat-file` appears nowhere else in the frozen bytes (grep: single hit at line 11). The contract's C1
target also names `git cat-file -e` as the resolution probe. Because `git show <rev>:<tree>` prints a tree listing and exits 0, the
`cat(...) is None` resolution test (`count-c1.py:113`) accepts **directories** as resolved gates (measured: `git show <rev>:tools` →
`tree 09cc234e…:tools\n\ng.py\n`, rc=0). `git cat-file -e <rev>:tools` also exits 0 for a tree, so switching the probe would not by itself close this;
the missing predicate is "the entry must be a blob", which neither the contract nor the counter states. The docstring should stop naming a
tool the code does not call.

## F9 — `parse_tables()` matches one exact header spelling and silently parses zero tables

`count-c1.py:40-59` recognises a registry table only when its header cells (lowercased, `count-c1.py:44-47`) equal `HEADER_CELLS`
(`count-c1.py:21-22`) exactly: `name | kind | entry | verdict map | self-test | pinned values | write scope | owner`. A registry that writes
"verdict" instead of "verdict map" — a one-word synonym — yields **zero** parsed rows and no distinct failure token; the counter then reports
every gate as unregistered. Measured in an isolated fixture (header `| name | kind | entry | verdict | self-test | pinned values | write scope
| owner |`, one fully conformant row for `tools/g.py`): `C1=unmet gates=1 registered=0 missing=1 thin=0 dup=0 unres=0 noselftest=0
noowner=0 failed=missing:tools/g.py` (rc=1). For a calibration claim this is the worst failure shape available — "the registry table is
syntactically different" and "25 gates were never registered" are indistinguishable in the output. A "no registry table found" token
distinct from `missing:` would separate them.

## F10 — the contract's C2 met-line and before-line strings are not the counter's output format

The contract freezes the C2 predicate as `C2=met pointers=N rows=N quotes_ok=N spans_ok=N sources>=4 rows_src=ok provenance=ok
failed=none`; the counter's `fmt()` (`count-c2.py:191-196`) emits `C2=met pointers=N rows=N same=… moved=… changed=… quotes_ok=N
spans_ok=N sources=<int> failed=… rev=…` — it never prints `sources>=4`, `rows_src=ok` or `provenance=ok`, and it prints three extra
tokens the contract does not mention. Symmetrically, the contract's C2 before-state reads `failed=entry_absent,rows_missing,…`, but the
counter returns at `count-c2.py:114-116` and prints only `failed=entry_absent` (measured at the entering revision:
`C2=unmet pointers=47 rows=0 same=0 moved=0 changed=0 quotes_ok=0 spans_ok=0 sources=0 failed=entry_absent
rev=325f7e639916fcbc77fa2ec7475951a1b86bb1cb`, rc=1 — the C2 control *is* faithfully reproducible). The C1 met line is closer, but the
counter additionally prints `failed=none` between `noowner=0` and `rev=`, so the contract's literal strings are paraphrases rather than
outputs; a seat string-matching the frozen line against counter stdout will mismatch on all three counters.

## F11 — the C2 selftest leaves its module globals half-restored, and carries a dead parameter

`count-c2.py:247-252` saves `PINS`, replaces `PINS` with synthetic digests, rebinds `FILES[:]` to the four synthetic names and rebinds the
global `NAMES`; `count-c2.py:281` restores `PINS` only — `FILES` and `NAMES` are left pointing at the synthetic fixture. In the CLI this is
harmless (the selftest branch exits at `count-c2.py:296-297`), but any in-process caller — a harness, a wrapper, or a future counter that
imports this module — would afterwards measure the live ledger with synthetic file names and pins. `build()`'s `extra=""` parameter
(`count-c2.py:210`) is concatenated into the ledger template (`count-c2.py:226`) but is never passed a non-default value by any of the ten
cases — a dead parameter that suggests a ledger-splicing capability the battery does not use.

## F12 — accumulated needless complexity in both counters (a future-round backlog, not a defect)

Redundancies that can be removed without touching any predicate: the `res` dict literal is spelled out twice in C1 (`count-c1.py:74-75` and
`count-c1.py:213-214`) with the same nine keys; `HEADER_CELLS` (`count-c1.py:21-22`) and `CELLS` (`count-c1.py:25-26`) are two eight-item
lists describing the same columns under different labels (one table of `(header_label, key)` pairs would serve both); C2's printed
`same=`/`moved=`/`changed=` counters are incremented only inside the successful-quote branch (`count-c2.py:161-162`), so their sum is
identically `quotes_ok` — three printed fields carrying no information beyond a partition the contract does not use; `--scratch` is accepted
by both counters and only `mkdir -p`-ed on the live path (`count-c1.py:202-203`, `count-c2.py:294-295`), where neither writes a single byte
(measured: a live run of both counters leaves the scratch directory empty) — it is a no-op parameter in live mode; and `sh()`/`cat()` are
byte-identical duplicated helpers in both files. **Caveat for the future round:** the shared-helper refactor must *not* be done by importing a
common module, because C3's boundary repair depends on each counter being self-contained and sha-pinned; the duplication is the price of the
boundary, not waste.

---

## Falsified hypotheses (recorded so the frontier is not re-walked)

* **"The range end in C2 is off by one."** `count-c2.py:159` builds `hay = "\n".join(lines[lo - 1:hi])` with `hi = max(end, start)`, which
  looks like an exclusive end. It is not: indices `lo-1 … hi-1` are lines `lo … hi`, inclusive of both ends. Probe output:
  `span_of('a.rst:5-7') = ('a.rst', 5, 7)`; counter hay for range 5-7 = `'alpha line 5 … \nalpha line 6 … \nalpha line 7 …'`; a ledger row
  quoting **line 7** of the range yields `quotes_ok=1 spans_ok=1` with no `quote_missing`. A control row quoting line 5 yields the same.
  No defect; hypothesis dropped.
* **"The C1 `dup` arm is unreachable."** It is reachable (my directory fixture produced `dup=2`); it is only *unexercised by the frozen
  selftest* (F6).
* **"The C2 selftest failure is an artifact of my scratch reuse."** No: the failure reproduces deterministically at the default floor in an
  isolated scratch directory (F1), and the committed receipt reproduces exactly at `--floor 0`. (A separate, genuine scratch-collision
  hazard did surface: both counters' selftests name their fixture directories `st-<case>`, so running C1's and C2's batteries against the
  same `--scratch` root makes them delete each other's fixtures — C1's battery died with `FileNotFoundError` on its own manifest until the
  two batteries were given separate roots. Harmless today, but a real footgun for a wave that runs both batteries in one tree.)

## Preserved contract (what I did not touch and what must not be simplified away)

The frozen bytes stand as committed; every simplification above is a **future-round** item and none was applied. The predicates that carry
the claims are intact and were exercised, not edited: C1's eight-cell conformance, `--selftest` requirement, owner cell, superseded-row
filter, and path resolution (`count-c1.py:96-117`); C2's pointer enumeration, floor, quote byte-location, distinct-bytes/word-count,
pairwise-distinct quotes, ≥4 cited copies, sha pins on the six v7.3 copies, `mined`/`used-by` binding and the provenance trio
(`count-c2.py:95-186`). The C2 pin table (`count-c2.py:39-45`) matches the committed copies' digests as frozen, and the C1/C2 controls
reproduce their committed receipts exactly — with the single documented exception in F2 (C1's control is reproducible only via the
unpinned absolute `--manifest` path).

## Evidence index (commands actually run; outputs quoted above)

| # | command (all paths absolute) | result |
|---|---|---|
| 1 | `python3 .ufo/waves/round-61/count-c1.py --selftest --scratch <scratch>` | `C1_SELFTEST pass=6 fail=0` rc=0; `case unres: … failed=['missing:tools/nothere.py']` |
| 2 | `python3 .ufo/waves/round-61/count-c2.py --selftest --scratch <scratch>` (default floor) | `case good: … FAIL failed=['pointer_floor:6<40']`; `pass=9 fail=1` rc=1 |
| 3 | same with `--floor 0` | `pass=10 fail=0` rc=0; identical to `evidence/selftest-c2.txt` |
| 4 | `python3 -m trace --count --file=count-c1.cover …count-c1.py --selftest …` | lines 100-101, 114-115 never executed |
| 5 | `python3 -m trace --count --file=count-c2.cover …count-c2.py --selftest …` | lines 112, 157, 170 never executed |
| 6 | `count-c1.py 325f7e63… --repo <lane> --scratch <scratch>` | `gates=0 … failed=manifest_unreadable` rc=1 |
| 7 | `count-c1.py 325f7e63… --repo <lane> --manifest <abs working-tree manifest>` | first line identical to `evidence/control-c1-do-nothing.txt` |
| 8 | `count-c2.py 325f7e63… --repo <lane> --scratch <scratch>` | identical to `evidence/control-c2-do-nothing.txt` |
| 9 | `count-c1.py 7370a731… --repo <lane> --scratch <scratch>` | `gates=25 registered=0 missing=25` rc=1 (registry tables end at r51) |
| 10 | fixture `falsehit` / `suponly` / `dirpath` (throwaway git repos under scratch) | `C1=met … registered=1` in all three (F3, F4) |
| 11 | fixture `header-synonym` | `registered=0 missing=1` — zero tables parsed (F9) |
| 12 | `python3 -m trace`… / `sha256sum` on both counters vs `git show 7370a731:<path>` | identical digests; frozen bytes untouched |

## Limits, blockers, and non-claims

* I audited **code simplification only**. I do not judge the claims, do not propose counter or contract amendments (barred after the freeze),
  and applied no remediation: the F1/F2 items are defects in the frozen claim's receipts and are reported, not fixed.
* No `git`/`jj` mutation anywhere in the lane or fleet; every mutating call targeted a scratch fixture created by `git init` at an explicit
  scratch path with the throwaway identity `t <t@t>`, and each fixture asserted its own toplevel before committing.
* Nothing under `/tmp` is cited as evidence; all scratch artifacts lived under `/fast/scratch/hyaku/mori-r61/Mo61SimplC1/` and were removed
  after the receipts above were copied into this report.
* The C2 `changed`-status reading (`count-c2.py:147-150` treats `changed` exactly like `moved`, i.e. range-bound) may or may not match the
  contract's "anywhere in the copy for changed" clause; the wording is ambiguous and I did not score it as a defect — flagged here only so
  the L1 does not read the ledger as requiring a different placement than the counter enforces.
* No tool was installed or upgraded during this seat (nothing required); channel/version/reason table is therefore empty by design.
