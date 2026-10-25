# MutRegistry — six adversarial registry fixtures against `tools/mori-gate-registry.py`

Seat: mutation tester (leaf). Round 44 wave 1. Instrument **not mutated**: every probe is an
input mutant (a `SKILL.md` gate table) handed to the frozen auditor; no instrument byte was
edited, and the instrument copy's hash is identical before and after the run.

- Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin` (HEAD `7cb59c6891d4f5d0266fe062565f094da835dc84`,
  the freeze commit; `git status --porcelain` shows only sibling work: `M SCORECARD.md`,
  `?? .ufo/waves/round-44/w1-spec.json`, `?? .ufo/waves/round-44/w1/` — none of it mine).
- Instrument copy: `git show 7cb59c68…:tools/mori-gate-registry.py` → `/tmp/mutreg44.I0sp78/mori-gate-registry.py`
- sha256 before **and** after all probes:
  `743996b11d19261b87e3ea6c0d0be4c0e5e6750d05f6d603af51dc1a7e125a1f`
  (equals `evidence/freeze-r44.txt:9` and the lane checkout's own hash).
- Sandbox: `/tmp/mutreg44.I0sp78` (`mktemp -d`); each probe is its own `git init` repo with
  `SKILL.md` + `tools/…` committed, audited at its own `rev-parse main`.
- Baseline (pristine instrument, own selftest): `python3 mori-gate-registry.py --selftest` →
  `GATE_REGISTRY_SELFTEST pass=6 fail=0`, rc 0. Control fixture (well-formed row) →
  `REGISTRY=met`, rc 0. So a FAIL below is a real rejection, not a broken harness.
- Tooling installed/upgraded: **none** (system python 3.14.8, git 2.56.0).

Verdict convention: **KILLED** = the auditor rejects the defective registry (mutant caught);
**SURVIVED** = the defective registry is accepted as `REGISTRY=met`.

## Verdict table

| # | probe | fixture | instrument output | rc | verdict |
|---|---|---|---|---|---|
| 1 | empty `verdict map` cell | `p1a-empty-verdict` | `FAIL (row 'fixture gate' missing cells: verdict map)` / unmet | 1 | **KILLED** |
| 1 | empty `owner` cell | `p1b-empty-owner` | `FAIL (row 'fixture gate' missing cells: owner)` / unmet | 1 | **KILLED** |
| 2 | entry names a path absent at rev | `p2-ghost-entry` | `FAIL (row 'ghost gate' entry path does not resolve at 62d37d73c86b)` / unmet | 1 | **KILLED** |
| 2b | *adjacent*: entry path absent but its basename matches the target | `p2b-ghost-suffix` | `PASS (row 'suffix gate': 8 cells, entry resolves, --selftest present)` / met | 0 | **SURVIVED** |
| 3 | entry names `tools/mori-gate-registry-old.py` | `p3-substring-tool` | `FAIL (unregistered: no row names mori-gate-registry.py)` / unmet | 1 | **KILLED** |
| 3b | *adjacent*: entry names `tools/not-mori-gate-registry.py` | `p3b-prefix-tool` | `PASS (row 'not-gate': …)` / met | 0 | **SURVIVED** |
| 3c | *adjacent*: entry names `tools/fixture-tool.sh.d/other.sh` | `p3c-dirprefix` | `PASS (row 'dir gate': …)` / met | 0 | **SURVIVED** |
| 4 | header `self test` instead of `self-test` | `p4-renamed-header` | `FAIL (row 'fixture gate' missing cells: self-test)` / unmet | 1 | **KILLED** |
| 5 | escaped pipe `--scope user\|system` in verdict map | `p5a-escaped-pipe` | splits to **8 cells**; `PASS (row 'fixture gate': 8 cells, …)` / met | 0 | **KILLED** (no smuggled column) |
| 5b | escaped pipe + genuinely empty owner | `p5b-empty-owner-escaped` | splits to 8; `FAIL (missing cells: owner)` / unmet | 1 | **KILLED** |
| 5c | escaped *column boundary* (owner merged into write scope) | `p5c-escaped-owner-boundary` | splits to 7; `FAIL (missing cells: name,kind,entry,verdict map,self-test,pinned values,write scope,owner)` / unmet | 1 | **KILLED** |
| 5d | *adjacent*: 9 cells (stray trailing cell) | `p5d-nine-cells` | splits to 9; `PASS (… 8 cells …)` / met | 0 | **SURVIVED** (extra cell unreported) |
| 6a | duplicate rows; bad row has the shorter entry cell | `p6a-short-bad-wins` | scores `bad-short` → `FAIL (missing cells: owner)` / unmet | 1 | **KILLED** |
| 6b | duplicate rows; bad row has the longer entry cell | `p6b-long-bad-loses` | scores `good-short` → `PASS` / met | 0 | **SURVIVED** (malformed duplicate invisible) |
| 6c | duplicate rows, equal entry-cell length | `p6c-tie-file-order` | scores `bad-tie-first` (file order) → `FAIL` / unmet | 1 | **KILLED** |

---

## 1. Empty `verdict map` cell / empty `owner` cell — KILLED

Fixture `p1a` (`SKILL.md` sha256 `a049c189…2c72`, rev `b2e07d067cb6`), the only gate row:

```
| fixture gate | gate | `bash tools/fixture-tool.sh` |  | `bash tools/fixture-tool.sh --selftest` | in-script cases | stdout only | mori |
```

```
$ python3 mori-gate-registry.py --repo $SB/repos/p1a-empty-verdict --rev b2e07d067cb6… --registry SKILL.md --audit tools/fixture-tool.sh
audit tools/fixture-tool.sh                    FAIL (row 'fixture gate' missing cells: verdict map)
rev=b2e07d067cb601c68f5ab0f2cbe4f68b3d0d7823
REGISTRY=unmet
```

`p1b` (sha256 `aa261fb4…5309`, rev `78cb550befd2`) is the same row with `| mori |` → `|  |`:

```
audit tools/fixture-tool.sh                    FAIL (row 'fixture gate' missing cells: owner)
REGISTRY=unmet
```

Both empty-cell branches are live: the row still splits to 8 cells, `cells` is a full 8-key dict,
and the `FIELDS` non-empty sweep names exactly the emptied column. Note the row is scored
*before* resolution/`--selftest`, so the receipt is unambiguous. Tool body used everywhere:
`#!/bin/sh\n# --selftest mode\nexit 0\n` (sha256 `3769cd51…cf0b`).

## 2. Entry names a path that does not exist at the revision — KILLED (assigned form)

Fixture `p2` (sha256 `69a988be…013d`, rev `62d37d73c86b`), row entry `bash tools/ghost-tool.sh`,
no such file committed; the audit target is the same ghost path so the row *is* the registering
row:

```
audit tools/ghost-tool.sh                      FAIL (row 'ghost gate' entry path does not resolve at 62d37d73c86b)
REGISTRY=unmet
```

`exists_at(repo, rev, base)` runs `git cat-file -e <rev>:<base>` and the miss is reported.
**Scope of the kill:** the check resolves the *audited target*, never the path written in the
entry cell. Adjacent probe `p2b` (sha256 `6d647159…3973`, rev `74a916de9d0e`) makes that gap
concrete — a row whose entry names `bash tools/old/mori-gate-registry.py` (absent), audited
against the real `tools/mori-gate-registry.py`:

```
audit tools/mori-gate-registry.py              PASS (row 'suffix gate': 8 cells, entry resolves, --selftest present)
REGISTRY=met
```

→ **SURVIVED**: the row's own entry path does not exist, but the fallback basename match
(`name in r[2]`) pairs it with the real tool, and `exists_at` then validates the *real* path.
A row naming a nonexistent sibling by basename therefore counts as registration.

## 3. Entry names a different tool sharing a substring — KILLED for `-old.py`

Fixture `p3` (sha256 `c40ec68b…3344`, rev `f20be22d63a9`). Repo commits the real instrument at
`tools/mori-gate-registry.py` (same sha256 `743996b1…`); the only row says:

```
| old gate | gate | `bash tools/mori-gate-registry-old.py --audit x` | … | … | in-script cases | stdout only | mori |
```

```
$ python3 mori-gate-registry.py --repo …/p3-substring-tool --rev f20be22d63a9… --audit tools/mori-gate-registry.py
audit tools/mori-gate-registry.py              FAIL (unregistered: no row names mori-gate-registry.py)
REGISTRY=unmet
```

Why it holds here: `entry_names` is anchored (`^(bash|sh|python3|node|time|env )*<base>(\s|$)`),
so `…-old.py` fails it; and the fallback `base in cell or name in cell` also fails, because
neither `tools/mori-gate-registry.py` nor `mori-gate-registry.py` is a substring of
`tools/mori-gate-registry-old.py`. The kill is therefore **suffix-specific, not structural**.

Adjacent mutations of the same idea, both accepted:

- `p3b` (sha256 `97448a1d…70fd`, rev `44b322126eb9`): entry `bash tools/not-mori-gate-registry.py`
  → `PASS (row 'not-gate': 8 cells, entry resolves, --selftest present)` / `REGISTRY=met`.
  `entry_names` rejects it, but the fallback matches the **basename** inside the longer name.
- `p3c` (sha256 `a159b3a0…1368`, rev `aae12c131e7e`): entry
  `bash tools/fixture-tool.sh.d/other.sh` → `PASS (row 'dir gate': …)` / `REGISTRY=met`.
  Same fallback: the real path is a *prefix* substring of the fake one.

So the instrument distinguishes "different tool with a longer name that extends my name"
(`-old.py`, caught) from "different tool whose name contains mine" (`not-…`, `….d/other.sh`,
accepted). The frozen predicate's own wording is "a row whose entry cell names its repo-relative
path"; the fallback is strictly weaker than that.

## 4. Renamed header (`self test`) — KILLED, but misdiagnosed

Fixture `p4` (sha256 `39bfbd9e…910d`, rev `13bebdd82a85`). Header only:

```
| name | kind | entry | verdict map | self test | pinned values | write scope | owner |
```

```
audit tools/fixture-tool.sh                    FAIL (row 'fixture gate' missing cells: self-test)
REGISTRY=unmet
```

The header is still **accepted** as a header (`parse_gate_table` only demands `low[0]=="name"` and
`low[1]=="kind"`, and it lowercases cells), so the run does not fail with `REGISTRY_SETUP`; the
renamed column just stops satisfying `FIELDS`, and the row is rejected through the
`missing_cell` branch. The rejection is correct; the *receipt* is wrong — it blames the row for
an empty cell that the row does not have, instead of reporting a header whose names do not match
the standard. An operator fixing by the message would add text to the row, not rename the column.
(Not probed, so not scored: header case/whitespace is normalised by `low = [c.lower() …]` on
already-stripped cells, so `Self-Test` would pass.)

## 5. Escaped pipe `--scope user\|system` — 8 cells, no false accept (KILLED)

Fixture `p5a` (sha256 `bbb5df24…f80b`, rev `1b86dab3ea31`), verdict-map cell:

```
0 clean · 1 failed · 2 could-not-evaluate (--scope user\|system)
```

`split_row` over that line, using the instrument's own `CELL_SPLIT = (?<!\\)\|`:

```
CELLS: 8
['fixture gate', 'gate', '`bash tools/fixture-tool.sh`', '0 clean · 1 failed · 2 could-not-evaluate (--scope user\\|system)', '`bash tools/fixture-tool.sh --selftest`', 'in-script cases', 'stdout only', 'mori']
audit tools/fixture-tool.sh                    PASS (row 'fixture gate': 8 cells, entry resolves, --selftest present)
REGISTRY=met
```

Answer to the question as asked: **yes, the row still parses to 8 cells**, the escape stays inert
(the cell keeps the literal `\|`, which the instrument never unescapes — harmless because only
emptiness is tested), and no extra cell is created. Two control directions confirm the escape
cannot be used to defeat the cell-count check:

- `p5b` (sha256 `3c1686c0…7092`, rev `7f1a5c375441`): escaped pipe in the verdict map **plus** a
  genuinely empty owner → still 8 cells → `FAIL (row 'fixture gate' missing cells: owner)`.
  Escaping cannot pad a short row.
- `p5c` (sha256 `ad6689cd…0664`, rev `8c8cfa5ab0cf`): escaping the *owner* boundary
  (`… | stdout only \| mori |`) merges two columns → 7 cells → `len(row) >= len(header)` is
  false → `cells = {}` → `FAIL (missing cells: name,kind,entry,verdict map,self-test,pinned values,write scope,owner)`
  / unmet. Escaping cannot hide a column. (Same receipt defect as probe 4: the row has all
  eight texts; the message says every cell is missing.)

Adjacent, `p5d` (sha256 `4a4934fe…52d7`, rev `e9765140c41f`): a 9-cell row
(`… | mori | stray |`) → `split_row` yields 9, `dict(zip(header, row))` silently drops the 9th,
and the auditor prints `PASS (row 'fixture gate': 8 cells, entry resolves, --selftest present)` /
`REGISTRY=met` → **SURVIVED**. The extra cell is unreported and the receipt asserts "8 cells"
about a 9-cell row; the frozen predicate's eight-cell floor is still satisfied by the first eight.

## 6. Two rows for the same tool — shortest entry cell wins; the choice is verdict-bearing

Selection rule in `audit()`: `row = sorted(matches, key=lambda r: len(r[2]))[0]` — matches sorted by
**entry-cell string length**, ascending; Python's sort is stable, so equal lengths keep file order.
Measured cell lengths: `tools/fixture-tool.sh` = 21, `` `bash tools/fixture-tool.sh` `` = 28,
`` `bash tools/fixture-tool.sh --verbose` `` = 38.

| fixture | rows (name / entry) | scored row | verdict |
|---|---|---|---|
| `p6a` sha256 `5abfdcdc…7cba`, rev `9390669b5304` | `good-long` / 28, `bad-short` (owner empty) / 21 | `bad-short` | `FAIL (row 'bad-short' missing cells: owner)` / unmet |
| `p6b` sha256 `2b1f6ede…7a18`, rev `e86123819ddb` | `good-short` / 21, `bad-long` (owner empty) / 38 | `good-short` | `PASS (row 'good-short': 8 cells, …)` / met |
| `p6c` sha256 `90dc6158…a6a5`, rev `3c4e2f621c07` | `bad-tie-first` / 28, `good-tie-second` / 28 | `bad-tie-first` (file order) | `FAIL (row 'bad-tie-first' missing cells: owner)` / unmet |

Answer to the question as asked: **the shortest entry cell is scored, and yes, the choice changes
the verdict** — the same pair of rows flips `met`↔`unmet` purely by which entry cell is longer
(`p6a` vs `p6b`). `p6b` is the coverage finding: a malformed duplicate row is never reported at
all, because only one match is ever scored and no "duplicate registration" check exists. `p6c`
shows the tie-break is file order, i.e. an earlier malformed row poisons a later valid one. The
instrument's own selftest has no duplicate-row arm (its six arms are `registered_row_met`,
`missing_cell_rejected`, `unresolved_entry_rejected`, `unregistered_path_rejected`,
`no_selftest_rejected`, `seven_cell_row_rejected`), so all three duplicate behaviours are outside
the frozen selftest's coverage.

---

## Restoration / non-mutation evidence

- The instrument was only ever *copied*; no edit tool touched it. sha256 of the sandbox copy after
  every probe: `743996b11d19261b87e3ea6c0d0be4c0e5e6750d05f6d603af51dc1a7e125a1f` — byte-identical
  to the pre-probe hash, the freeze manifest (`evidence/freeze-r44.txt:9`), and
  `git show 7cb59c68…:tools/mori-gate-registry.py`.
- Lane repo: no `git add/commit/push/checkout/stash/reset`, no mutating `jj`, no writes outside
  this report. HEAD is still `7cb59c6891d4f5d0266fe062565f094da835dc84`.
- Scratch fixtures are disposable under `/tmp/mutreg44.I0sp78` (kept for the receipts above).

## Coverage findings (not permission to change the contract)

1. **Substring fallback** (`base in r[2] or name in r[2]`): accepts a row whose entry names a
   different tool when the real path/basename is embedded in it (`p3b`, `p3c`) — probe 3's kill
   holds only for names that extend the real name (`-old.py`).
2. **Resolution is of the target, not the entry**: a row naming an absent path is accepted when
   its basename matches the real tool (`p2b`) — probe 2's kill holds only when the *target* is
   absent.
3. **Duplicate rows**: shortest-entry-cell-wins, silent, verdict-flipping (`p6a`/`p6b`/`p6c`).
4. **Receipt accuracy**: a renamed header is reported as an empty row cell (`p4`); a 7-cell row
   is reported as all-eight-missing (`p5c`); a 9-cell row is reported as "8 cells" (`p5d`).
   All three are correct rejections/acceptances per the frozen predicate; only the diagnosis text
   is misleading, which matters because the contract treats the receipt as evidence.
