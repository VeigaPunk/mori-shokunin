# ExecC3Counter — P-C3 counter (round 45, wave 1)

Status: **delivered**. `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/count-c3.py`
(728 lines, sha256 `37fd7c24ff52d6aa27f718ef0b0a2f2e4affa7a1cd0ab67c1fa05f028854a98e`), its
single-check mutant `.ufo/waves/round-45/fixtures/mutants/count-c3.py` (sha256
`69bf9b6eb29b781866adde9f1e866808626d7dbb56093ee5c32d49c88ad8b4b3`, one hunk), and this report.
No other lane file was edited. `round-44/count-c3.py` was read, never written.

The counter implements P-C3 including the frozen **Correction 1** (`--entering-rev REV` required,
every `--entry` absent there; `--entry` and `--row` non-empty). Everything below was run; a check
that was not run is not claimed.

## 1. The interface (what the L1 and the verifier call)

```
python3 .ufo/waves/round-45/count-c3.py <rev|WORK> --entering-rev REV \
        --entry PATH [--entry PATH ...] --row S### [--row S### ...] \
        [--coverage-map FR# ...] [--repo PATH] [--root PATH] \
        [--census PATH] [--readme PATH] [--timeout S]
python3 .ufo/waves/round-45/count-c3.py --selftest
```

- `--root` defaults to `dirname(--repo)` (the fleet root); `--census` defaults to
  `<root>/scripts/sources-census.sh`.
- Exit `0 C3=met`, `1 C3=unmet`, `2 C3_SETUP` (usage, unresolvable measured **or** entering
  revision, git/census timeout, `--repo`/`--root` not a directory).
- Verdict line (last line of stdout):

```
C3=met rev=cd0177a5… entering=6d1f4cae… entries=1 rows=S473 census_sha256=3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30
```

- Named checks, one line each (`check <name> <subject> PASS|FAIL (<detail>)`):
  `entries_declared`, `rows_declared`, then per entry `entry_present`, `entering_absent`,
  `entry_meta`, then `rows_present`, `census_ok`, then per entry `readme_row`.

## 2. The five routed round-44 defects, closed

### D1 — the census arm validates the lane through `--root`, not a staged copy

`sources-census.sh:566` tests `[ ! -e "$dir/$path" ]` where `$dir` is derived from the target;
a `SOURCES.md` staged under `$TMPDIR` resolves every `corpus/knowledge/…` used-by against
`/tmp`. The arm now runs exactly

```
bash <root>/scripts/sources-census.sh validate --root <root> mori
```

with `cwd=<repo>`, and the script's sha256 is printed in the verdict line (contract condition 5).
No `tempfile` staging exists anywhere in the counter — the `cwd`/`TMPDIR` arm asserts the decoy
`TMPDIR` stays empty.

Measured on the real lane, `TMPDIR` **unset** (i.e. `/tmp`), cwd `/`:

```
check census_ok census PASS (exit=0)
C3=unmet rev=WORK entering=554ff416459c92f0dea9762f834a556df2990187 entries=1 rows=S473 census_sha256=3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30
```

Round-44's identical arm on the identical registry printed `check census_ok FAIL (exit=1)`
unless `TMPDIR=<repo>` (r44 `w1/ExecOffHostReplay.md` §F2, matrix row 2 vs row 4). The census
digest `3fb72615…` equals `sha256sum /home/vgpnk/Projects/shokunin/scripts/sources-census.sh`.

### D2 — `--entry` repeats; each entry owns its declared rows

`--entry` is `action="append"`. Per entry the counter requires anchored `source:` (with at least
one id token), `verified-at:`, `recheck:` and `coverage-map:` lines; a row is *attributed* to an
entry iff that entry's `source:` id list names it, and `rows_present` requires the row's
`used-by` cell to name **every** entry that declares it. A `--row` declared by no entry is
`<rid> declared by no entry` → `C3=unmet` (Correction 1: `--row` non-empty is now a check,
`rows_declared`, not a usage exit).

Real bytes, two entries and three rows, one invocation:

```
check entries_declared entries PASS (2 declared)
check rows_declared   rows PASS (3 declared)
check entry_present   corpus/knowledge/pid-probe-conclusion-r44.md PASS (7151 bytes)
check entry_present   corpus/knowledge/census-cgroup-levels-r45.md PASS (8140 bytes)
check entry_meta      corpus/knowledge/pid-probe-conclusion-r44.md PASS (sources S471,S472; map FR5)
check entry_meta      corpus/knowledge/census-cgroup-levels-r45.md PASS (sources S473; map FR1,FR12)
check rows_present    rows=S471,S472,S473 FAIL (S473 absent)
...
C3=unmet rev=WORK entering=… entries=2 rows=S471,S472,S473 census_sha256=3fb72615…
```

### D3 — token-exact matching, both directions

`source:` ids are the leading id run of each `source:` line (`S\d{3,}` whole tokens only);
`coverage-map:` values are whole `[A-Za-z][A-Za-z0-9._-]*` tokens; `used-by` is split on commas
and compared as a whole path (`corpus/knowledge/x.md` and `knowledge/x.md` spellings only — never
a suffix or substring). Arms that would be false PASSes under substring matching:

- `token_collision_row_unmet` — registry holds a **mined S473 whose used-by names the entry**, the
  entry declares `S4731` only, the run declares `--row S473`: a substring lookup would print
  `C3=met`; the counter prints `rows_present FAIL (S473 declared by no entry)`.
- `coverage_token_collision_unmet` — entry `coverage-map: FR13`, run `--coverage-map FR1`:
  `FR1 ⊄ FR13` → `entry_meta FAIL`.
- `usedby_suffix_collision_unmet` — used-by `corpus/knowledge/fixture-entry-r45.md.bak`:
  `rows_present FAIL` (r44's `entry not in used` would have passed).

### D4 — absent / not-`mined` / not-naming rows and a red census are `unmet`; setup is exit 2 only

`rows_present` fails on `absent`, `status=<x>` (not `mined`), `declared by no entry`, and
`used-by does not name <entry>`. A red census is `census_ok FAIL (exit=…; <first E findings>)` →
`C3=unmet`, exit 1. `git rev-parse` for **both** revisions is inside the `try`:

```
$ … WORK --entering-rev deadbeefcafe --entry corpus/knowledge/census-cgroup-levels-r45.md --row S473
C3_SETUP cannot resolve revision 'deadbeefcafe' in /home/vgpnk/Projects/shokunin/mori-shokunin
EXIT=2
$ … WORK --entry … --row S473                       # --entering-rev missing → usage
usage: count-c3.py <rev|WORK> --entering-rev REV --entry PATH …
EXIT=2
$ … WORK --entry … --row S473 --timeout 0            # census timeout
C3_SETUP census timeout after 0s: /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
EXIT=2
```

Design point: an **absent census script** is `census_ok FAIL (absent: <path>)` → `C3=unmet`
exit 1, not setup — the contract's setup list is usage/unresolvable revision, and a missing
instrument must not be able to leave the claim unscored. Receipt:

```
$ … WORK --entry corpus/knowledge/census-cgroup-levels-r45.md --row S473 --census /nonexistent/sources-census.sh
check census_ok census FAIL (absent: /nonexistent/sources-census.sh)
C3=unmet rev=WORK entries=1 rows=S473 census_sha256=absent
EXIT=1
```

### D5 — `--selftest`: 19 arms in a throwaway git repo + fake census under `$TMPDIR`

Each fixture is `<TMPDIR>/c3st-*/<tag>/fleet/` with `fleet/scripts/sources-census.sh` (fake,
records its argv) and `fleet/mori-shokunin` (git repo, **two** commits: an entering tip with no
entry/row/map row, then the fixture commit). The fake census is the real command's shape; the met
arm asserts the recorded argv is exactly `validate --root <fleet> mori` and contains no `--file`.

| arm | what it proves |
|---|---|
| `registered_entry_met` | the whole predicate is satisfiable; census argv and 64-hex digest |
| `absent_entry_unmet` | absent entry → `entry_present` + `rows_present` |
| `entering_present_unmet` | **Correction 1**: measured rev = entering rev → `entering_absent` |
| `row_without_used_by_unmet` | `used-by = —` → `rows_present` |
| `token_collision_row_unmet` | S4731 ≠ S473 with a mined S473 available (D3) |
| `usedby_suffix_collision_unmet` | used-by path suffix ≠ the entry (D3) |
| `coverage_token_collision_unmet` | FR1 ⊄ FR13 (D3) |
| `red_census_unmet` | red census → `C3=unmet` |
| `readme_without_map_row_unmet` | prose mention in README is not a map row |
| `readme_without_map_section_unmet` | a table outside `## Coverage map` is not a map row |
| `missing_coverage_map_unmet` | no `coverage-map:` line → `entry_meta` |
| `multi_entry_met` | two entries, two rows, two map values |
| `multi_entry_row_missing_usedby_unmet` | two entries declare one row, used-by names one |
| `empty_rows_unmet` | empty `--row` set → `rows_declared`, exit 1 (Correction 1) |
| `empty_entries_unmet` | empty `--entry` set → `entries_declared` + `rows_present` |
| `cwd_tmpdir_independent_met` | cwd and `TMPDIR` moved off the repo; decoy `TMPDIR` stays empty (the r44 failure) |
| `red_census_ignores_tmpdir` | `TMPDIR=<repo>` cannot turn a red census green |
| `unresolvable_revision_setup` | two bogus sha1s → `Setup` |
| `usage_is_setup` | empty argv, and rev+entry+row without `--entering-rev` → exit 2 |

## 3. Tally (with rc)

```
$ cd / && TMPDIR=<my scratch> python3 .ufo/waves/round-45/count-c3.py --selftest
C3_SELFTEST pass=19 fail=0            EXIT=0

$ python3 .ufo/waves/round-45/fixtures/mutants/count-c3.py --selftest
selftest FAIL red_census_unmet: fails=[] want=['census_ok'] …
selftest FAIL red_census_ignores_tmpdir: fails=[] want=['census_ok'] …
C3_SELFTEST pass=17 fail=2            EXIT=1

$ diff -u count-c3.py fixtures/mutants/count-c3.py | grep -c '^@@'
1
-        record("census_ok", "census", proc.returncode == 0,
+        record("census_ok", "census", True,
```

The mutant discards exactly one check — the census exit status. It flips the **verdict**, not just
the selftest (same fixture, same red census, same revisions):

```
real counter : check census_ok census FAIL (exit=1; mori E11 S901 missing used-by …)
               C3=unmet … census_sha256=00b0e477…   EXIT=1
mutant       : check census_ok census PASS (exit=1; mori E11 S901 missing used-by …)
               C3=met   … census_sha256=00b0e477…   EXIT=0
```

`C3=met` is reachable end-to-end with the **real** census script (digest `3fb72615…`), the real
drafted entry and a real registry row, in a sandbox at
`tmp/ExecC3Counter/metfix/fleet` (real census copied to `fleet/scripts/`, `fleet/shokunin.conf`
lane row, registry with the S473 row, README with a `## Coverage map` row), `TMPDIR` unset:

```
check entries_declared entries PASS (1 declared)
check rows_declared   rows PASS (1 declared)
check entry_present   corpus/knowledge/census-cgroup-levels-r45.md PASS (7197 bytes)
check entering_absent corpus/knowledge/census-cgroup-levels-r45.md PASS (not in 6d1f4cae…)
check entry_meta      corpus/knowledge/census-cgroup-levels-r45.md PASS (sources S473; map FR1, FR12)
check rows_present    rows=S473 PASS (mined and named)
check census_ok       census PASS (exit=0)
check readme_row      corpus/knowledge/census-cgroup-levels-r45.md PASS (map row names it)
C3=met rev=cd0177a58… entering=6d1f4caea… entries=1 rows=S473 census_sha256=3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30
EXIT=0
```

(That sandbox's S473 row is my own placeholder — the L1 appends the real one. It exists only to
prove the meter can print `met`; it is not evidence that the real registry is registered.)

## 4. Findings the L1 must act on before the after-measurement

**F1 (blocking) — the declared C3 after-command will exit 2 as written.** `RevBeforeAfter` carries
`count-c3.py <rev> --entry corpus/knowledge/census-cgroup-levels-r45.md --row S473 --root …`;
Correction 1 makes `--entering-rev` required. Use:

```
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/count-c3.py <rev> \
  --entering-rev 554ff416459c92f0dea9762f834a556df2990187 \
  --entry corpus/knowledge/census-cgroup-levels-r45.md --row S473 \
  --coverage-map FR1 --coverage-map FR12 --root /home/vgpnk/Projects/shokunin
```

`--coverage-map` is optional (the line is required; token matching applies only to declared
values); passing `FR1`/`FR12` pins the entry's map tokens, which the entry's own text claims.

**F2 (blocking) — the real lane is currently `C3=unmet` on two named checks**, and neither is the
census:

```
check rows_present rows=S473 FAIL (S473 absent)
check readme_row   corpus/knowledge/census-cgroup-levels-r45.md FAIL (no map row names it)
C3=unmet rev=WORK entering=554ff416459c92f0dea9762f834a556df2990187 …
```

`S473` is simply not in `corpus/SOURCES.md` yet (the L1 appends it; note census E11 requires the
`used-by` **path to exist on disk**, so the entry must be present when the census runs — it is).

**F3 (blocking the README check, and a spec conflict).** Contract P-C3 condition 4 is "`corpus/
README.md` carries a **map row** naming the entry". The wave's `ScribeRows` instead asks for "a
row/sentence naming the entry … in the file's existing style" pointing at `## Frontier`, and
`## Frontier` holds prose bullets. Prose does **not** count (that was exactly round 44's
overclaim, below). The row must go in the `## Coverage map` table (header `| Note | Holds |
Sources |`, which ends at line 50, before `## Known gaps`):

```markdown
| `knowledge/census-cgroup-levels-r45.md` | the cgroup `memory.events`/`memory.events.local` two-level distinction and what a hierarchical count with an unnamed scope cannot attribute | S473 (kernel v7.2 admin-guide, opened 2026-10-25) |
```

Either spelling of the Note cell works (`knowledge/…` or `corpus/knowledge/…`, with or without
backticks); the cell must be the **first** cell of a table row inside `## Coverage map`. My
sandbox receipt above is exactly this row.

**F4 — round 44's `C3=met` receipt was doubly attenuated.** `after/c3-after.txt` printed
`check readme_row PASS (names entry)` for `corpus/knowledge/pid-probe-conclusion-r44.md`, but that
entry has **no** coverage-map row:

```
$ grep -c '^| `knowledge/pid-probe-conclusion-r44.md`' corpus/README.md
0            (exit 1)
```

The only mention is prose in `## Round-44 coverage additions`, `corpus/README.md:639`:

```
exist. Entry: `corpus/knowledge/pid-probe-conclusion-r44.md` (S471, S472,
```

r44's `readme_row` was `entry.encode() in readme_body` — any prose hit. Under the frozen
predicate the same entry now also fails Correction 1, exactly as intended:

```
check entry_present   corpus/knowledge/pid-probe-conclusion-r44.md PASS (7151 bytes)
check entering_absent corpus/knowledge/pid-probe-conclusion-r44.md FAIL (present at entering 554ff416459c92f0dea9762f834a556df2990187)
check entry_meta      … PASS (sources S471,S472; map FR5)
check rows_present    rows=S471,S472 PASS (mined and named)
check census_ok       census PASS (exit=0)
check readme_row      … FAIL (no map row names it)
C3=unmet …   EXIT=1
```

So round 44's entry + row can never carry round 45: the vacuity Correction 1 names is now
rejected by a named check (`entering_absent`), and its map row was never real.

## 5. Residuals, disclosed

- **R1** The census arm reads the **worktree** registry (its E11 rule is a disk test,
  `sources-census.sh:566`); the entry/registry/README checks read the bytes at `--rev`. At
  `WORK` they coincide; at a sha they can diverge mid-wave. The receipt prints `rev=` and the
  census digest, so the divergence is visible. This is the only worktree read in the counter.
- **R2** `entry_meta` requires **anchored** field lines (`^source:`, `^verified-at:`, `^recheck:`,
  `^coverage-map:`); round 44 used whole-file substrings, so a prose mention of `recheck:` used
  to satisfy the field.
- **R3** Beyond the five routed defects I scrubbed `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE`/
  `GIT_COMMON_DIR`/`GIT_NAMESPACE`/`GIT_OBJECT_DIRECTORY`/`GIT_ALTERNATE_OBJECT_DIRECTORIES`
  from the `git` environment (`git_env()`), so `--repo` stays authoritative when the caller's
  environment names another repository. Two lines, same defect class as D4 ("the revision
  address must be real"), disclosed for the trust-boundary review.
- **R4** `--coverage-map` matching is token-exact against the union of declared values; an entry
  must name at least one of them. Without `--coverage-map`, only the line (and a non-empty value)
  is required.
- **R5** The fixture git repositories are created with `git init -q -b main` (needs git ≥ 2.28);
  each selftest run removes its base directory.

## 6. Files, scratch, tooling

- Written: `.ufo/waves/round-45/count-c3.py`, `.ufo/waves/round-45/fixtures/mutants/count-c3.py`,
  this report.
- Scratch (mine, under the wave): `.ufo/waves/round-45/tmp/ExecC3Counter/` — `metfix/` (met-reachable
  sandbox), `redfix/` (red-census fixture census). No `/tmp` use, no writes to the fleet repo,
  `/home/vgpnk/Projects/shokuknow`, or any sibling `*-shokunin`.
- No tool installed, no pacman transaction, no network fetch needed for this seat.

## 7. Checks the main agent should run after integration

1. `python3 .ufo/waves/round-45/count-c3.py --selftest` → `C3_SELFTEST pass=19 fail=0`, rc 0.
2. `python3 .ufo/waves/round-45/fixtures/mutants/count-c3.py --selftest` → `pass=17 fail=2`, rc 1
   (the two census arms).
3. `diff -u count-c3.py fixtures/mutants/count-c3.py` → one hunk, `proc.returncode == 0` → `True`.
4. The F1 command at the wave tip with **no** `TMPDIR` override, after the S473 row and the
   `## Coverage map` row are appended → expect `C3=met` rc 0; at `554ff416` → `C3=unmet` rc 1
   (`entry_present` + `rows_present` + `readme_row`).
