# RevC7CapPath — capability row `source-drift re-fetch probe` at `13bfba2`

**Verdict: PASS.** All three paths cited by the single capability row resolve to `blob` at
`13bfba23b7ca063c76d3504a2ff6eb7b6a294932`, and exactly one table row in `SCORECARD.md` carries the
capability key (line 2059). No non-blob, no ambiguous row match.

Scored rev: `13bfba23b7ca063c76d3504a2ff6eb7b6a294932` (`git cat-file -t` → `commit`).
`SCORECARD.md` at that rev is blob `f9f34f98729b656a460c6a53f0461090e87acfe4`.

## 1. Path → type table (direct `git cat-file -t <rev>:<path>`)

| path cited by row 2059 | `git cat-file -t` | exit | mode (`git ls-tree`) | size |
|---|---|---|---|---|
| `tools/mori-source-drift.py` | `blob` | 0 | `100755` | 19676 |
| `.ufo/waves/round-37/evidence/c2-after-v3.txt` | `blob` | 0 | `100644` | 1220 |
| `.ufo/waves/round-37/evidence/drift-live-r37.txt` | `blob` | 0 | `100644` | 3033 |

Raw receipt (scratch): `.ufo/waves/round-39/scratch/RevC7CapPath/path-types.txt`

```
tools/mori-source-drift.py	blob	exit=0
.ufo/waves/round-37/evidence/c2-after-v3.txt	blob	exit=0
.ufo/waves/round-37/evidence/drift-live-r37.txt	blob	exit=0
```

Mode check matters: `git cat-file -t` reports a symlink as `blob` too, so I additionally confirmed the
tree modes are regular files (`100755`/`100644`, not `120000` gitlinks/symlinks and not `040000` trees).
All three are non-empty; heads confirm identity with the row's description (tool docstring: "re-fetch each
corpus/SOURCES.md row that has a committed copy"; `c2-after-v3.txt` carries the P-C2 predicate and
`tool_present/selftest/cap_kill` lines; `drift-live-r37.txt` carries a `command:` line plus `S### no-copy`
rows).

## 2. Row-count check — exactly one row carries the key

Capability key (canonical constant, `.ufo/waves/round-39/count-c7.py:63`):
`CAPABILITY_KEY = "source-drift re-fetch probe"`.

Independent scan of the committed `SCORECARD.md` blob:

- table rows (`line.startswith("|")` **and** key present): **1** — line **2059**.
- table rows with leading whitespace tolerated (`line.lstrip().startswith("|")`): **1** — line 2059.
- any occurrence of the key anywhere in the file: lines 2059, 2071, 2175. Lines 2071 and 2175 are prose
  ("`round-37 C1` … and `round-37 C2` (source-drift re-fetch probe), both demonstrated" / "…
  `source-drift re-fetch probe` capability row's …"), not rows, so they cannot enter the check.
- Case/format variants: `grep -iE "source.?drift.*re.?fetch|refetch|re_fetch"` returns only the same
  three lines — no `refetch`/`re_fetch`/hyphenated alternative exists.
- Near-key table rows: `| C1 — source-drift byte probe (exploratory …) |` (line 2012, the round-36 claim
  table, **not** a capabilities-register row) and `| C2 freshness — drift-probe hardening |` (line 2066,
  round-37 outcome table) do **not** contain the exact key, so neither displaces or duplicates it.

Row content at rev, verbatim (`SCORECARD.md:2059`, capacities register opened at line 2054):

```
| round-37 C2 | source-drift re-fetch probe | Re-fetches every registry row with a committed copy and classifies the copy against today's body under a 4 MiB bounded read and a post-redirect public-destination policy; round 37 added `--selftest` 6 cases with two named, mutation-killable arms (the probe's live run first worked in round 36) | `tools/mori-source-drift.py`; `.ufo/waves/round-37/evidence/c2-after-v3.txt`; `.ufo/waves/round-37/evidence/drift-live-r37.txt` | 36 |
```

## 3. The canonical selection is fail-closed on multiplicity

`count-c7.py:270-273`:

```python
def capability_row(scorecard_text):
    rows = [line for line in (scorecard_text or "").splitlines()
            if line.startswith("|") and CAPABILITY_KEY in line]
    return rows[-1] if len(rows) == 1 else None
```

So "the last single row" means: with exactly one match it returns that row; with **zero or two-plus** it
returns `None`, and `check_capability_v2` (`count-c7.py:301-310`) then reports `False, "row absent"`.
A duplicate row cannot silently win — it fails the check. Predicate wording (`count-c7.py:80-81`):
"every path the SCORECARD capability row cites resolves at R to a committed file, not a directory".

Executable proof, importing the canonical module against the committed bytes (read-only):

```
capability_row None? False
real paths_in: ['tools/mori-source-drift.py', '.ufo/waves/round-37/evidence/c2-after-v3.txt', '.ufo/waves/round-37/evidence/drift-live-r37.txt']
check_capability_v2: (True, "paths=[...3...] not_file=[]")
  object_type tools/mori-source-drift.py -> blob
  object_type .ufo/waves/round-37/evidence/c2-after-v3.txt -> blob
  object_type .ufo/waves/round-37/evidence/drift-live-r37.txt -> blob
```

Negative controls on the same function (no lane bytes touched):

- duplicate row appended to a scratch copy → `capability_row None? True`, `check_capability_v2` → `False`.
- one cited path renamed to `tools/mori-source-drift-nope.py` → `(False, "… not_file=['tools/mori-source-drift-nope.py']")`.

The recorded wave receipt agrees: `.ufo/waves/round-39/evidence/c7-after.txt:8` —
`check capability_v2    PASS (paths=[…3…] not_file=[])`.

## 4. Working-tree/tip parity

`git diff --stat 13bfba2 -- SCORECARD.md tools/mori-source-drift.py .ufo/waves/round-37/evidence/c2-after-v3.txt .ufo/waves/round-37/evidence/drift-live-r37.txt .ufo/waves/round-39/count-c7.py`
is empty: the bytes I read and imported are the scored bytes, not an edited working copy. The report
method was checkable without LSP: no `lsp` device is exposed in this seat's toolset, so semantic proof
came from importing the canonical checker module (executable behavior), with text grep only used to
enumerate line numbers, as recorded here.

## 5. Findings

No defect in scope. Two residual risks, neither triggered by the scored row:

1. **`paths_in` requires backticks and a dot-suffixed final segment** (`PATH_RE` in
   `count-c7.py:93`, extraction at `:276-284`). A capability row that cited a directory or
   extension-less path would be *skipped*, not failed: `paths_in("`corpus/evidence`")` → `[]`,
   `paths_in("`tools`")` → `[]`; likewise an unquoted (non-backtick) path is invisible. The scored row
   backticks all three paths and each ends in `.py`/`.txt`, so the check exercises all of them. This is a
   bounded-read/predicate-shape property of P-C7, not a mismatch with the assignment (all cited paths are
   files), but it is the check's weakest seam for future rows.
2. **Existence/type only.** `check_capability_v2` never reads the evidence files' content; a row citing
   three unrelated committed blobs would pass. That is what P-C7 specifies ("resolves … to a committed
   file, not a directory"), so it is not a violation, but the capability claim is stronger than the
   check.

Observation, not ambiguity: a second table row (line 2012, round-36 claim table) cites the same tool path
`tools/mori-source-drift.py`, but it is not a capabilities-register row and does not carry the key; the
key-based selection is therefore unambiguous (count = 1).

## 6. Verification gaps

- I did not re-run the full `count-c7.py <rev> --seed 20261024` calibration (C7 exit-0 receipt belongs to
  the C7 calibration seat); I exercised only its capability branch plus the two row controls above.
- No tool was installed or upgraded for this seat (pacman paused host-wide and unnecessary here).

Scratch artifacts: `.ufo/waves/round-39/scratch/RevC7CapPath/{SCORECARD.md,path-types.txt}` (copy of the
committed blob and the type receipt).
