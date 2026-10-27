# Mo58Sentinel62 — C2 registry binding: S550 row-parser attack

Seat: sentinel (attack share). Surface: round-58 C2 counter rows arm only.
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`. Freeze rev
`fe8801120a67c1a6b8899d7d0423839caa09e7d0`; entering rev `b783d0b8…`.
Counter under attack (read-only, bytes unchanged):
`.ufo/waves/round-58/count-c2.py` sha256
`aab888ad787964f7a153d64d85dafa58f652f977e21e22eaa492706a691010d3` (227 lines).

**Verdict: counterexamples found.** Five constructions make the frozen counter print
`C2=met … rows=ok` and exit 0 while the registry row S550 violates the frozen
predicate (`… | mined | … | <used-by naming the entry> |`). Every construction is
reproduced by executing the frozen `measure()` against throwaway git fixtures; no
production file, lane VCS, SCORECARD, LOG or corpus registry was touched.

Assimilation: none.

## 1. The arm as frozen

`count-c2.py:95-108`:

```
95   reg = _show(rev, SOURCES) or ""
97   row_lines = [ln for ln in reg.splitlines() if ln.startswith(f"| {ROW_ID} ")]
98   if len(row_lines) != 1:
...
102      cells = [c.strip() for c in row_lines[0].split("|")]
104      if len(cells) < 12 or cells[8] != "mined" or ENTRY not in cells[11]:
105          rows = "bad"
```

Four independent weaknesses: (i) row detection is a literal 5-byte prefix on the
line, not an ID-cell comparison; (ii) the scan covers the whole `SOURCES.md`, not
the registry table; (iii) status is a positional index (`cells[8]`) with no
column-count equality and no header mapping; (iv) used-by is a **substring** test
(`ENTRY in cells[11]`) with no path resolution, although C1 resolves every
backticked pointer with `git cat-file -e R:<path>` (`count-c1.py:105`) and
contract "Routed defects for round 58" #2 asks for exactly that.

## 2. Method (bounded, reproducible)

Fixture driver `probe_s550_row.py` (sha256
`97a73c634d52ec27627ad5ab84a66f472a6b3dd70dff4f702f28409952a46ced`, full source
in §7) loads the frozen counter via `importlib`, repoints its `LANE` global at a
throwaway repo per case (`git init` under `$HYAKU_SCRATCH/mori-r58/Mo58Sentinel62/`,
`git -C <fixture>` for every call, `git rev-parse --show-toplevel` asserted equal to
the fixture dir), builds `tools/mori-driver-liveness.py`, the pinned copy, a
conformant `corpus/knowledge/driver-events-r58.md`, and a synthetic
`corpus/SOURCES.md` whose only variable is the S550 row, then calls `measure(rev)`
and records (rc, stdout). Baseline `A0` scores `C2=met … rows=ok` with the
counter's own `ROW_OK`, so every negative below is attributable to the mutation, not
to a broken fixture. Counter-side controls at the lane are unchanged:
`python3 .ufo/waves/round-58/count-c2.py b783d0b8…` → `C2=unmet entry=absent
failed=entry`, rc=1; `--selftest` → `C2_SELFTEST pass=6 fail=0`, rc=0. Scratch was
the only write target and is removed (§8).

## 3. Confirmed false-greens (counter met, predicate false)

| # | case | registry state | counter stdout | rc |
|---|---|---|---|---|
| S1 | D1_usedby_suffix_dangling | used-by = `corpus/knowledge/driver-events-r58.md.orig` — nonexistent path | `C2=met claims=8 located=8 copy=ok tree=ok rows=ok sources=ok failed=none` | 0 |
| S1b | D2_usedby_prefix_dangling | used-by = `archive/corpus/knowledge/driver-events-r58.md` | same `C2=met … rows=ok` | 0 |
| S1c | D3_usedby_dotdir_dangling | used-by = `./corpus/knowledge/driver-events-r58.md.bak` | same | 0 |
| S1d | F3_usedby_parent_relative | used-by = `../corpus/knowledge/driver-events-r58.md` | same | 0 |
| S2 | B1_dup_nospace_second_rejected | two S550 rows: canonical `mined`, duplicate `|S550 |` **rejected** | same | 0 |
| S2b | B2_dup_two_spaces_second_rejected | duplicate written `|  S550 |`, rejected | same | 0 |
| S2c | B3_dup_tab_second_rejected | duplicate written `| S550\t|`, rejected | same | 0 |
| S2d | F1_indented_dup_rejected | duplicate written `|  S550 |`, rejected | same | 0 |
| S2e | F7_dup_second_queued_nospace | duplicate `|S550 |` status **queued** | same | 0 |
| S3 | E4_shifted_status_rejected | 12-column row: real status cell `rejected`, bogus column at split-index 8 holds `mined`, entry path at index 11 | same | 0 |
| S4 | E6_row_in_fenced_example | **no table row**: the only S550 line is inside a fenced code block | same | 0 |
| S5 | D4_usedby_entry_plus_dangling_sibling | used-by = `<entry>, corpus/knowledge/nonexistent-r99.md` | same | 0 |

Fixture revisions for exact reproduction: D1 `c0d67418…`, D2 `f3e83bc7…`, D3
`ffa5552b…`, F3 `8ef8ec62…`, B1 `a141ddae…`, B2 `d1464519…`, B3 `f7be94d0…`,
F1 `fb90dff9…`, F7 `6cb9f321…`, E4 `950c5366…`, E6 `55f9c2fb…`, D4 `86b0e579…`
(each is a throwaway `git init`+one commit under the seat scratch dir, deleted).

### Severity, exploit path, impact, smallest remediation

**S1 — used-by bound by substring, not identity. Severity: high (predicate false green).**
Exploit: write the S550 row exactly as `ROW_OK` but set the used-by cell to
`corpus/knowledge/driver-events-r58.md.orig` (or `archive/…`, `./….bak`, `../…`).
The entry file itself exists at R (that arm is real), so the counter reaches the
rows arm and passes `ENTRY in cells[11]` on a path that names **a different,
nonexistent file**. Counter prints `rows=ok`, exit 0; the frozen claim's "S550's
`used-by` names the entry" is false and the registry backlink is unresolvable —
the exact failure class routed for round 58 (#2 pointer resolution). Impact: C2
can be scored met with a fabricated registry backlink. Smallest fix: split
`cells[usedby_idx]` on `,`, strip, require **exact equality** with `ENTRY`, and for
every path in the list run `_git("cat-file", "-e", f"{rev}:{path}")` (mirror
`count-c1.py:105`); fail `rows` on any non-zero.

**S2 — duplicate-ID guard is spacing-literal. Severity: medium.**
`startswith("| S550 ")` misses `|S550 |`, `|  S550 |`, `| S550\t|`, so
`len(row_lines) != 1` never fires and a contradictory second S550 row (status
`rejected`, used-by `—`) coexists in the registry while the counter reports
`rows=ok`. The real registry is uniformly spaced today (322 rows all `| Sxxx `,
plus one header and one separator line — `awk` over `HEAD:corpus/SOURCES.md`), so
this needs a hand edit, but the arm's stated purpose is to reject exactly that
ambiguity. Impact: a verified registry can hold two S550 rows of opposite status
and the counter still binds to one. Smallest fix: parse cell 1 of every `|`-led
line (`[c.strip() for c in ln.split("|")]` → `cells[1] == ROW_ID`) instead of the
literal prefix, then count.

**S3 — status is positional (`cells[8]`) with no column-count equality. Severity: medium.**
A 12-column row whose real status cell reads `rejected` passes when a bogus column
lands at split-index 8 with the literal `mined` and the entry path lands at index
11 (`E4`). `len(cells) < 12` also accepts 13+ cells, so "used-by is the last
column" is never checked — the row can carry any number of trailing columns.
Impact: a malformed row of the wrong status scores as a mined binding. Smallest
fix: require the canonical `len(cells) == 13` (leading `|` + 11 columns + trailing
`|`), and resolve `status`/`used-by` indexes from the table header
(`| id | source | … | status | opened | recheck | used-by |`) rather than
hard-coded 8/11.

**S4 — the row need not be in the registry table. Severity: medium-low.**
`reg.splitlines()` scans the whole file: a syntactically perfect S550 row placed
inside a fenced example block and nowhere else scores `rows=ok` (`E6`); symmetric
evidence that the arm is section-blind is `E7` (rejected row under `## Superseded`
plus a good in-table row → `rows=bad`). Impact: the "registry binding" can bind to
documentation prose. Smallest fix: scope the scan to the table that starts at the
`| id | source |` header and ends at the first blank/non-`|` line; scan fenced
blocks never.

**S5 — used-by siblings are never resolved. Severity: low.**
`<entry>, corpus/knowledge/nonexistent-r99.md` → `rows=ok` (`D4`). The predicate
"sources=ok/rows=ok" does not literally require sibling resolution, but C1 resolves
every pointer on the same contract revision, so C2's registry arm is the weaker
half of routed defect #2. Same fix as S1 (the `cat-file -e` loop covers siblings).

## 4. No-counterexample classes (bounded negative results)

These attacks were executed and correctly rejected — the counter is not
indiscriminate; the failures above are specific:

| case | registry state | counter stdout | rc |
|---|---|---|---|
| A0_base_conformant | canonical good row | `C2=met … rows=ok` (control) | 0 |
| A1_dup_canonical | two canonical S550 rows | `C2=unmet … rows=bad failed=rows` | 1 |
| A2_dup_canonical_second_rejected | canonical mined + canonical rejected | `… rows=bad failed=rows` | 1 |
| A3_wrong_status_canonical | only row, status `rejected` | `… rows=bad failed=rows` | 1 |
| B4_only_lookalike_spacing | only row is `|S550 |` rejected | `… rows=bad` | 1 |
| C1_lookalike_S5501_only / C2_lookalike_S550_suffix_only | only `S5501` / `S550x` row | `… rows=bad` | 1 |
| C3 / C4 | good S550 + rejected `S5501` / `S550x` | `C2=met` (correct: lookalike is a distinct row) | 0 |
| E1_ten_columns_no_usedby | used-by column dropped (10 cols) | `… rows=bad` | 1 |
| E3_eleven_columns_no_trailing_pipe | row without closing `|` | `C2=met` (cells still 12, used-by last — benign) | 0 |
| E5_pipe_in_teaches_shift | unescaped `|` in teaches shifts columns | `… rows=bad` | 1 |
| E7_row_outside_registry_section | rejected row under another heading + good in-table | `… rows=bad` | 1 |
| F4_usedby_entry_variant_filename | used-by `…driver-events-r58-old.md` | `… rows=bad` | 1 |
| F2_crlf_good | CRLF file, canonical row | `C2=met` (benign) | 0 |

So: genuine lookalike **IDs** (`S5501`, `S550x`, `S55`) are rejected as the brief
hoped; the escapes are the *spacing* variants of the real ID (S2) and the
*superstring* variants of the used-by path (S1), plus the positional/table-scope
holes (S3, S4).

## 5. Selftest coverage gap (why these shipped)

`--selftest` (6 cases, `pass=6 fail=0`, rc=0) covers: conformant, junk quotes,
copy sha drift, missing frontmatter, row_not_usedby (`—`), entry absent. It has
**no** case for: duplicate rows, a used-by that is a superstring of the entry
path, column-count/column-shift, or a row outside the table. Each of the six
false-green constructions above is invisible to the current selftest, so the gap
is structural, not accidental. Suggested minimum additions (one per finding):
`dup_row` → `rows=bad`; `usedby_superstring` → `rows=bad`;
`usedby_missing_target` → `rows=bad`; `row_shifted_status` → `rows=bad`;
`row_in_fence` → `rows=bad`. Under the frozen contract these counter bytes cannot
change this round (kill rule), so this is a routed defect for the next freeze, not
a remediation here.

## 6. Verdict for the wave

Detection result only: the S550 rows arm admits predicate-violating registries
under five distinct constructions (S1 high; S2/S3/S4 medium; S5 low). The strongest
single exploit to check before scoring C2 met: the used-by cell in
`corpus/SOURCES.md` must be **exactly** `corpus/knowledge/driver-events-r58.md` (or
a comma-list whose every member resolves at R). A hand check of the landed row's
used-by cell against `git cat-file -e R:corpus/knowledge/driver-events-r58.md` is
sufficient to close S1 on the landed data even while the counter stays frozen.
No production or registry change is proposed by this seat beyond the drafted
counter fix, and no claim about provider/liveness behaviour is made.

## 7. Receipt — fixture driver (verbatim, sha256 `97a73c63…`)

```python
#!/usr/bin/env python3
"""Mo58Sentinel62 adversarial probe: round-58 C2 counter rows/S550 arm."""
import contextlib, importlib.util, io, os, subprocess, tempfile

COUNTER = "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-58/count-c2.py"
SCR = os.path.dirname(os.path.abspath(__file__))
TOOL = "tools/mori-driver-liveness.py"
ENTRY = "corpus/knowledge/driver-events-r58.md"
COPY = "corpus/evidence/sources-r58/mori-driver-liveness.py"
SOURCES = "corpus/SOURCES.md"

spec = importlib.util.spec_from_file_location("count_c2", COUNTER)
c2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)

def git(d, *a): return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True)

def mk(namespace, rows_text, entry=None):
    d = tempfile.mkdtemp(dir=SCR, prefix=f"fx-{namespace}-")
    assert subprocess.run(["git", "-C", d, "init", "-q"]).returncode == 0
    assert os.path.realpath(git(d, "rev-parse", "--show-toplevel").stdout.strip()) == os.path.realpath(d)
    for sub in ("corpus/knowledge", "corpus/evidence/sources-r58", "tools"):
        os.makedirs(os.path.join(d, sub), exist_ok=True)
    open(os.path.join(d, TOOL), "w").write(c2.TOOL_TEXT)
    open(os.path.join(d, COPY), "w").write(c2.TOOL_TEXT)
    open(os.path.join(d, ENTRY), "w").write(entry if entry is not None else c2.ENTRY_OK)
    header = ("# SOURCES\n\n## Registry\n\n"
              "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
              "|---|---|---|---|---|---|---|---|---|---|---|\n")
    open(os.path.join(d, SOURCES), "w").write(header + rows_text)
    git(d, "add", "-A"); git(d, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "fixture")
    return d, git(d, "rev-parse", "HEAD").stdout.strip()

def run(d, rev):
    old = c2.LANE; c2.LANE = d; buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf): rc = c2.measure(rev)
    finally: c2.LANE = old
    return rc, buf.getvalue().strip()

def row(status="mined", usedby=ENTRY, **kw):
    f = dict(id="S550", source="mori driver-liveness event classes", kind="own-work", tier="A",
             scope="event-class semantics", anchor="`parse_log` lines 77-174",
             teaches="Grounds the classes", status=status, opened="2026-10-27",
             recheck="90d", usedby=usedby); f.update(kw)
    return (f"| {f['id']} | {f['source']} | {f['kind']} | {f['tier']} | {f['scope']} | "
            f"{f['anchor']} | {f['teaches']} | {f['status']} | {f['opened']} | "
            f"{f['recheck']} | {f['usedby']} |\n")
# cases A0–E7 as tabled in §3/§4; each built by mk(name, rows), scored by run(d, rev).
```

Observed stdout for the driver run (`probe-s550-row.out` sha256
`6e27945acd8cf583aa2b9fabf615c8ae41fe2f3e8c84e6bb23063f30cf3a170a`, 107 lines):
`COUNTER_SHA256=aab888ad…` then one `case<TAB>rc=N<TAB>C2=…` line per case, exactly
as tabled above; the second batch (F1–F7) printed
`F1_indented_dup_rejected rc=0 C2=met … rows=ok`,
`F2_crlf_good rc=0 C2=met … rows=ok`,
`F3_usedby_parent_relative rc=0 C2=met … rows=ok`,
`F4_usedby_entry_variant_filename rc=1 C2=unmet … rows=bad`,
`F5_usedby_exact_entry rc=0 C2=met … rows=ok`,
`F6_usedby_space_separated_list rc=0 C2=met … rows=ok`,
`F7_dup_second_queued_nospace rc=0 C2=met … rows=ok`.

## 8. Scratch, cleanup, non-mutation

Scratch root `$HYAKU_SCRATCH/mori-r58/Mo58Sentinel62/` (`/fast/scratch/hyaku`);
`TMPDIR` set there; disk-guard at start: `/fast 31% used, 556G free` (green). Only
writes: the driver, its output, and the per-case throwaway repos — all removed
after this report was written. No `pacman`, no installs, no lane/fleet VCS command
(other than read-only `git -C` on the lane and on fixtures), no edits to
`count-c1.py`, `count-c2.py`, contract, corpus registry, SCORECARD, LOG,
MANIFEST or any sibling repo.
