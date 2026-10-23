# RevC4Live — `live_rows` verification at f725f3076972e6e70595b5ac8279be524a111ff8

Scope: re-derive the `live_rows` content check (C4) against the committed live
receipt `.ufo/waves/round-37/evidence/drift-live-r37.txt` and the registry
`corpus/SOURCES.md`, both at the scored tip. All commands run in
`/home/vgpnk/Projects/shokunin/mori-shokunin` (lane repo, read-only).

## Verdict: PASS (no mismatch, no duplicate id, no id outside the registry)

## 1. Receipt identity

`git show f725f307:.ufo/waves/round-37/evidence/drift-live-r37.txt | sha256sum`
= `82d79f0d550412313765f440981e7a60acefb4e32b0cee6f008e584535686c16` —
byte-identical to the working-tree copy (same hash), so the checked artifact is
the committed one.

## 2. Counts (independently re-derived)

- Per-row lines matching `^S[0-9]{3} (fresh|excerpt|drifted|unavailable|no-copy)$`: **225**
- `<S###> drifted` lines: **10**
- Summary lines matching `^MORI_SOURCE_DRIFT `: **1**
- Summary value: `rows=225 fresh=53 excerpt=0 drifted=10 unavailable=0 no-copy=162`
  (`drifted=10` = drifted-line count = 10 → consistent)
- Duplicate ids across all 225 `^S[0-9]{3} ` lines: **0**
  (`grep -oE '^S[0-9]{3}' | sort | uniq -d | wc -l` → 0)

Drifted ids named: `S156 S157 S158 S159 S160 S176 S177 S210 S211 S223`.

## 3. Registry membership at f725f307

`git show f725f307:corpus/SOURCES.md | grep -cE '^\| S[0-9]{3} '` → **226** rows.
All 10 named ids match a `| S### ` registry row at the tip:

| id | SOURCES.md line | row topic (truncated) |
|---|---|---|
| S156 | 162 | systemd v262 shared property printer |
| S157 | 163 | systemd v262 `unit_notify()` timestamps |
| S158 | 164 | systemd v262 journald rate-limit notice |
| S159 | 165 | earlyoom commit edd3d94 `Restart=always` |
| S160 | 166 | systemd v262 journalctl option grammar |
| S176 | 182 | Python 3.15.1 unicodedata docs |
| S177 | 183 | Python html module docs |
| S210 | 216 | git-rev-parse(1) |
| S211 | 217 | PMC mirror of Nosek et al. 2018 |
| S223 | 229 | Python 3 urllib.request docs |

`unknown=[]` — no named id falls outside the registry.

## 4. Counter cross-check

`python3 .ufo/waves/round-38/count-c4.py f725f3076972e6e70595b5ac8279be524a111ff8`
→ `C4=met`, exit 0; live_rows detail:

```
check live_rows        PASS (named=10 summary_drifted=10 unknown=[])
```

Matches my independent derivation exactly (named=10, summary_drifted=10,
unknown=[]). Semantics (count-c4.py:184-197): collect `^S\d{3} drifted$` lines
as `named`, take `drifted` from the `MORI_SOURCE_DRIFT` summary regex, require
`drifted >= 1 and len(named) == drifted and not unknown` where `unknown` =
named ids absent from the `^\| (S\d{3}) ` registry set.

## 5. Residual note (not a failure)

`named` is a list of drifted *lines*, not unique ids — a duplicated drifted id
is caught only indirectly: it inflates `len(named)` so it fails the count
equality unless the summary `drifted=` is simultaneously inflated to match (a
crafted receipt with `S156 drifted` twice and `drifted=2` would pass). The live
receipt has zero duplicates, so the real artifact is clean; the gap is narrow
because the drift tool's own summary would count its emitted rows.

## Tooling

No installs or updates performed; no tool needed beyond git/python3/grep
already present.

Report: .ufo/waves/round-38/w2/RevC4Live.md
