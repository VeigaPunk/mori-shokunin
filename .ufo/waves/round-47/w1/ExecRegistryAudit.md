# ExecRegistryAudit — w1 report

Seat: `ExecRegistryAudit` (leaf executor). Assignment: run the lane's gate-registry auditor at the
freeze commit and report the verdict plus exactly which cells/rows the auditor will require, so the
L1 can add conformant rows.

## 1. Assigned run (freeze commit), exact evidence

Command (from `/home/vgpnk/Projects/shokunin/mori-shokunin`, TMPDIR=`<lane>/.scratch/r47-ExecRegistryAudit`):

```
python3 tools/mori-gate-registry.py --rev 63eecf2738db96f46b0bd02b1b2dfd66787493d0 \
  --audit tools/mori-pin-check.py --audit .ufo/waves/round-47/count-c2.py
```

Output (exit code 1):

```
audit tools/mori-pin-check.py                  FAIL (no row names tools/mori-pin-check.py)
audit .ufo/waves/round-47/count-c2.py          FAIL (no row names .ufo/waves/round-47/count-c2.py)
tables=7
rev=63eecf2738db96f46b0bd02b1b2dfd66787493d0
registered=0 unregistered=2 no_selftest=0 duplicate=0 wrong_row=0 tables=7
REGISTRY=unmet
```

Freeze commit confirmed present: `63eecf27 round-47: freeze — contract P-C1/P-C2, mori-pin-check.py,
count-c2.py, controls, v7.2 OOM source copies, collision/quarantine scratch`.

**Verdict: `REGISTRY=unmet` (exit 1), as expected before the rows are added.** It is exactly the
"unregistered" class: `unregistered=2`, all other counters zero. There is no `no_selftest`,
`duplicate`, or `wrong_row` finding at the freeze commit, so the only missing pieces are attribution
rows for the two audited paths.

## 2. What the auditor requires (cell-by-cell)

The auditor (`tools/mori-gate-registry.py`, per its docstring and `audit()`/`entry_names()`/
`entry_target()`/`selftest_flag()` code) reads every pipe table in the registry file (`SKILL.md`,
default) whose header row is exactly the eight standard cells:

`| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |`

For each audited path, exactly one row must attribute it, and the row must satisfy all of:

1. **Attribution (`entry` cell)** — the cell's **first backticked command** must invoke the audited
   path itself: the first backticked span's first non-wrapper, non-flag, non-env-assign token that
   contains `/` or ends in `.py`/`.sh` must equal the path (`tools/mori-pin-check.py` /
   `.ufo/waves/round-47/count-c2.py`). A different script earlier in the cell, a bare flag span, or
   prose elsewhere never attributes (this is what produced `no row names …`).
2. **All eight cells present and non-empty**, in the standard order.
3. **Entry resolves at the audited revision** and is repo-relative (never absolute, never escaping
   the repo).
4. **Real self-test branch** — the tool bytes at the audited revision must carry a genuine
   `--selftest` argv branch (a parser key, a flag comparison, or argv membership — not a comment or
   docstring mention). Both tools already satisfy this at the freeze commit:
   - `tools/mori-pin-check.py`: `add_argument("--selftest", action="store_true")` +
     `if args.selftest: return selftest()`;
   - `.ufo/waves/round-47/count-c2.py`: `if argv == ["--selftest"]: return selftest()`.
   If a row instead declares `selftest-flag=<flag>`, the flag name must contain `test` and the tool
   must carry it as a parser key/`case` pattern; the simple `--selftest` declaration is the
   low-risk path here.
5. **Unique `name`** across all registry tables (a duplicate name is a finding that fails the whole
   audit; currently `duplicate=0`).
6. **Global hygiene** — every existing registry row (all 7 tables at freeze) must stay conformant:
   a row whose entry is absent at the revision or leaves the repo is a `wrong_row` finding and fails
   the audit even if the two new rows are perfect. At freeze `wrong_row=0`; the L1 should not
   disturb existing rows while adding the new ones.

## 3. Required new rows (proven conformant)

Two new rows must be added to `SKILL.md` (a new table with the standard header, or the appropriate
existing table). Validated example rows — appended to a byte-identical archive of the freeze tree in
a fixture repo, the audit then reports `REGISTRY=met` (see §4):

```
| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| pin check (r47, C1) | gate | `python3 tools/mori-pin-check.py --rev <REV> --min-tally-pins 26 --baseline-rev <BASE>` | 0 `PIN_CHECK=met` · 1 `PIN_CHECK=unmet` (mismatch, dropped pin, below tally floor, or setup) · 2 `PIN_CHECK_SETUP` (usage, unresolvable revision, missing registry) | `python3 tools/mori-pin-check.py --selftest` | SKILL.md gate-table self-test tally/digest pins; baseline revision | none (read-only git; scratch under `<repo>/.scratch`) | mori |
| r47 count c2 (C2) | gate | `python3 .ufo/waves/round-47/count-c2.py <rev>` | 0 `C2=met` · 1 `C2=unmet` (entry_absent, pins, source_row) · 2 `C2_SETUP` (usage, unresolvable revision, git timeout) | `python3 .ufo/waves/round-47/count-c2.py --selftest` | corpus/knowledge/oom-tracepoints-r47.md; SOURCES row S475; v7.2 oom.h copies | none (read-only git) | mori |
```

Cell-by-cell notes for these two rows:

- **name**: any unique string; `pin check (r47, C1)` and `r47 count c2 (C2)` are free (no clash
  with census, drift pin, source drift, r44/r45 rows, counter-conformance rows, etc.).
- **entry**: the first backticked command must be `python3 tools/mori-pin-check.py …` /
  `python3 .ufo/waves/round-47/count-c2.py <rev>` respectively — nothing else before it. Placeholder
  args (`<REV>`, `<BASE>`, `<rev>`) are fine; `entry_target` only needs the script token.
- **kind**: `gate` for both (C1 calibration gate / C2 counter gate), matching sibling rows.
- **self-test**: declare `python3 tools/mori-pin-check.py --selftest` and
  `python3 .ufo/waves/round-47/count-c2.py --selftest` — both tools have a real branch at the freeze
  commit (checked at `63eecf`; also true at the current working tree).
- **verdict map / pinned values / write scope / owner**: any non-empty text; the auditor checks
  presence, not content. The examples mirror the contract's `PIN_CHECK=met|unmet` and `C2=met|unmet`
  vocabulary.

## 4. Validation evidence (fixture, in scratch)

Fixture built per seat rules: `mktemp`-style repo under
`.scratch/r47-ExecRegistryAudit/verify-repo`, `git init`, toplevel verified before first commit; the
freeze tree was materialized with `git -C <lane> archive 63eecf… | tar -x -C <fixture>` (read-only
on the lane); the two rows above were appended; committed; auditor re-run:

```
audit tools/mori-pin-check.py                  PASS row='pin check (r47, C1)' (8 cells, entry resolves, --selftest argv branch)
audit .ufo/waves/round-47/count-c2.py          PASS row='r47 count c2 (C2)' (8 cells, entry resolves, --selftest argv branch)
tables=8
rev=673a434ae55cf1c7fb06e7a4f98c61c0326c1fd1
registered=2 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0 tables=8
REGISTRY=met
exit_code=0
```

This proves the two rows above are sufficient and conformant; the L1 can copy them verbatim (modulo
verdict-map wording) into `SKILL.md`.

## 5. Notes / risks

- The lane's working-tree `SKILL.md` is currently modified (`git status` shows ` M SKILL.md`),
  presumably by a sibling seat; this report's audit targeted the frozen commit as assigned. The L1
  should land the rows on top of whatever the integrated tip is, then re-run the same command — with
  the two rows present it will print `REGISTRY=met` (exit 0).
- Re-audit must use the same `--rev` as the claim measurement; if run at `WORK` while editing is in
  flight, results are transient (parent owns post-integration gates).
- No tools were installed or updated (only the lane's own stdlib Python 3 scripts ran; no pacman, no
  `sudo`, no new binaries) — nothing to record under the tooling directive beyond this note.
