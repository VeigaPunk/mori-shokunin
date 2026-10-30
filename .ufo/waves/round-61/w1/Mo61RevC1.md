# Mo61RevC1 — bypass hunt on frozen `count-c1.py` (registry rows that pass while lying)

Counter audited: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/count-c1.py`
(frozen at freeze rev `7370a731…`). All line refs are to that file.
Method: static read + fixture repo at scratch (`git init`, `t <t@t>`), counter run with
`--repo <fixture> --scratch <seat scratch>`. Fixture deleted after run; receipts embedded below.

## Verdict table

| Assigned lie | Counter catches it? | Evidence |
|---|---|---|
| 1. Entry cell names path inside a longer token | **NO — passes** | commit `13c6e0c2` → `C1=met` |
| 2. Two live rows, superseded one is the real one | **NO — passes** (but see F3: honest version fails) | commit `13c6e0c2` → `C1=met` |
| 3. Owner cell whitespace-only | Depends on the whitespace: ASCII/NBSP **caught**; zero-width space **passes** | `d4517d38` → `thin:…:owner`; `13c6e0c2` → `met` |
| 4. `--selftest` named for a tool without that mode | **NO — passes**, even when the cell *denies* a selftest exists | `8bc28179` → `C1=met` |

Result: all four lies slip past the counter. The counter only enforces row *shape*
(8 non-empty cells, substring presence), never row *truth*.

## F1 — entry-cell matching is a raw substring test (count-c1.py:62-70)

```python
toks = [t.strip().strip("`") for t in r["entry"].replace("(", " ") ... .split()]
if path in toks or path in r["entry"]:
    hits.append(r)
```

The second disjunct (`path in r["entry"]`) makes the tokenizer dead code: **any** entry
cell containing the manifest path as a byte substring counts as "naming" it.
Demonstrated passing rows (commit `13c6e0c2`, `C1=met`):

- entry `` `tools/gate-a.py.bak` `` — the named path does not exist in the repo;
  the row registered `tools/gate-a.py` anyway (`unres` checks the *manifest* path,
  never the *named* path).
- entry `` `https://example.invalid/x/tools/gate-b.py` `` — a URL tail satisfied
  "names the path".

Corollary the contract never imagined: **one row can register multiple gates** — a row
whose entry cell mentions path X also registers any gate whose path is a substring of
X (e.g. `count-c1.py` inside `.ufo/waves/round-52/count-c1.py`… wait, inverted: a row
naming `.ufo/waves/round-52/count-c1.py.bak` registers `.ufo/waves/round-52/count-c1.py`
for free). Nothing requires the entry referent to resolve or even be a path.

## F2 — superseded-vs-live is a form check, not a semantic one (count-c1.py:96-103)

```python
live = [r for r in hits if "supersed" not in r["name"].lower()
        and "supersed" not in r["scope"].lower()]
...
row = live[0] if live else hits[0]
```

- Only `name` and `scope` cells are scanned for `supersed*`; a superseded marker in any
  other cell (verdict, entry, self-test, owner) or spelled otherwise ("replaced",
  "deprecated", "see below") is treated as a live row.
- Only the *single surviving* live row is conformance-checked. If the true registration
  is the superseded-marked row and the live row is a stub, the stub passes.
  Demonstrated (commit `13c6e0c2`): real row marked `(superseded)` in name +
  `superseded` in scope; live stub row `verdict=TBD`, `pinned=-`, `owner=FILLME` —
  `C1=met`.

## F3 — fail-closed side: honest rows get rejected (dup / missing)

Same fixture, commit `d4517d38` →
`C1=unmet … failed=thin:tools/gate-a.py:owner,dup:tools/gate-b.py` (rc=1):

- A gate with two rows where the *retired* row says `superseded by next row` in its
  **verdict** cell (the natural place in this registry's own idiom — the frozen
  selftest fixture `SUP` itself puts `superseded: see next row` in the **scope** cell;
  had it used the verdict column, the selftest case would read `dup`, not `superseded-ok`)
  → counted `dup`. The counter's idea of "superseded" is a two-cell substring grep.
- A row containing a literal `|` inside a cell (e.g. a `a | b` verdict-map idiom) splits
  to 9 cells; `len(raw) == len(CELLS)` (count-c1.py:52) **silently drops the row** →
  `missing`. No malformed-row diagnostic is emitted.

## F4 — "non-empty" and "names --selftest" are byte checks, not truth checks

- Owner: `empty = [k for k in CELLS if not row[k]]` (count-c1.py:104) runs after
  `c.strip()`. ASCII whitespace and NBSP (`U+00A0`, stripped by Python `strip()`)
  → caught (`thin:…:owner`). Zero-width space `U+200B` is not stripped and is truthy
  → **passes** (commit `13c6e0c2`, owner cell `\u200b`, `C1=met`). Any
  non-whitespace invisible codepoint works (e.g. `U+200C`, `U+FEFF`-in-cell would
  actually strip — U+200B/C/D family does not).
- Self-test: the entire check is `"--selftest" not in row["selftest"]` (count-c1.py:109).
  The named command is never run, never resolved against the entry path, never checked
  to exist. Demonstrated passing cells:
  - `none — no --selftest mode exists` (commit `8bc28179`) — the cell *denies* a
    selftest and still satisfies the gate.
  - `` `python3 tools/gate-d.py --selftest` `` where `tools/gate-d.py` is committed in
    the fixture as a script that exits 2 on any argument — `unres` is satisfied because
    the *manifest* path resolves; the self-test claim is never exercised.
- All other cells: `verdict`, `pinned`, `scope` need only be non-empty — `TBD`, `-`,
  `X` all pass (commit `8bc28179`, row f: `C1=met`).

## Structural boundary (what the counter cannot check, named)

`count-c1.py` verifies registry *form*: 8-cell rows under a byte-exact header, path
substring presence, non-empty cells, one literal substring (`--selftest`), and manifest-
path resolution. It cannot verify registry *truth*: whether the entry cell's referent
is the path (vs. a superstring/URL), whether a row marked live is the authoritative
registration, whether any cell's content is meaningful, or whether the named self-test
command exists or runs. Scope boundary: **the counter measures "a row with the right
shape exists", not "the gate is registered"** — every semantic claim in the contract's
C1 target sentence ("holds exactly one non-superseded row whose entry cell names the
path", "a self-test cell naming a `--selftest` command", "an owner cell") is checked
syntactically only.

## Frozen selftest gap

`CASES` (count-c1.py:150-158) exercises good/missing/thin/noselftest/superseded-ok/
unres — none of the four lies above is a case. The `superseded-ok` case happens to pin
the *only* superseded spelling the counter recognizes; the verdict-cell spelling
(rejected as `dup` in F3) is untested.

## Receipts (fixture repo, scratch, deleted after capture)

```
$ python3 count-c1.py 13c6e0c2… --repo fix1   # lies 1,2,3(ZWSP),4 all planted
C1=met gates=4 registered=4 missing=0 thin=0 dup=0 unres=0 noselftest=0 noowner=0 failed=none   rc=0
$ python3 count-c1.py d4517d38… --repo fix1   # NBSP owner + verdict-cell superseded
C1=unmet gates=2 … failed=thin:tools/gate-a.py:owner,dup:tools/gate-b.py                        rc=1
$ python3 count-c1.py 8bc28179… --repo fix1   # selftest-denial cell + filler cells
C1=met gates=2 registered=2 … failed=none                                                         rc=0
```

No repo/VCS/lane writes; fixture lived only under `/fast/scratch/hyaku/mori-r61/Mo61RevC1/`.
Tools installed: none (system python3 + git only).
