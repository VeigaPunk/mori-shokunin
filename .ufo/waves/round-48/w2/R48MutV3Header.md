# R48MutV3Header — mutation probe: mori-pin-check.py v3 selftest arms (R1–R3)

**Attacked:** the claim that the landed v3 tool `tools/mori-pin-check.py` (tip e4dfff32d4f97c7ef250e9a7538fa75d4f284492) carries self-test arms that kill single-point removals of R1 header recognition (`HEADER_CELLS`), R2 hidden-row accounting (`hidden_rows` row-shaped branch), and R3 ASCII span checks (`span_kind`). Method: 6 mutants (2 per rule), each one single-point edit in a scratch copy; detector = `python3 <mutant> --selftest`; killed iff non-zero exit.

**Verdict: BREAKS — coverage class.** 3 of 6 mutants survive the 60-arm selftest (exit 0). The three *whole-feature* removals are all killed; the three *partial* removals survive, exposing three concrete arm gaps (R1 case-variant headers untested; R2 `--selftest` trigger redundant with the token trigger; R3 non-ascii branch redundant with the NFKC-casefold branch for the pinned fullwidth arm). Each survivor has a demonstrated reproducer and a demonstrated one-line killing arm; the killing arms pass 61/61 on the pristine tool (no false kills). This is a selftest-coverage finding only — no defect is claimed in the shipped tool's behavior, and the contract is not changed.

## Baseline (pristine)

- Copy: `.scratch/r48w2-R48MutV3Header/mori-pin-check.py`, sha256 `85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1` (byte-identical to the tracked file).
- `TMPDIR=<scratch> python3 mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=60 fail=0`, **exit 0**.

## Results table

| Rule | Mutant | Single-point mutation (pristine line) | selftest result | Verdict | Killing arm(s) |
|---|---|---|---|---|---|
| R1 | m1r1 | `HEADER_CELLS = ("self-test", "selftest", "self test")` → `("self-test",)` — alias spellings removed (L113) | `pass=58 fail=2`, rc=1 | **KILLED** | `r1_header_selftest_spelling`, `r1_header_self_test_spelling` |
| R1 | m2r1 | `low = [c.lower() for c in cells]` → `low = list(cells)` — case folding removed (L201) | `pass=60 fail=0`, rc=0 | **SURVIVED** (false-red class) | new arm `r1_header_case_insensitive` (below) |
| R2 | m1r2 | `if kind in ("candidate", "fence_body") and row_shaped:` → `if kind in ("candidate",) and row_shaped:` — fenced rows no longer hidden (L254) | `pass=59 fail=1`, rc=1 | **KILLED** | `r2_hidden_fenced` |
| R2 | m2r2 | `if HIDDEN_TOKEN_RE.search(raw) or "--selftest" in raw:` → `if HIDDEN_TOKEN_RE.search(raw):` — `--selftest` trigger removed (L255) | `pass=60 fail=0`, rc=0 | **SURVIVED** (false-green class) | new arm `r2_hidden_selftest_arg_no_token` (below) |
| R3 | m1r3 | casefold branch deleted: `if PINLIKE_T0_RE.fullmatch(unicodedata.normalize("NFKC", tok0)): return "unparsed", "casefold-selftest-prefix"` (L292–293) | `pass=58 fail=2`, rc=1 | **KILLED** | `r3_lowercase_prefix`, `r3_mixedcase_prefix` |
| R3 | m2r3 | non-ascii branch deleted: `if any(ord(c) > 127 for c in tok0): return "unparsed", "non-ascii-token"` (L290–291) | `pass=60 fail=0`, rc=0 | **SURVIVED** (false-green class) | new arm `r3_nonascii_decorative_span` (below) |

Killed-mutant failure lines (actual output, rc=1 each):

```
FAIL r1_header_selftest_spelling  PIN_CHECK=unmet ... hidden=1 ...   (m1r1)
FAIL r1_header_self_test_spelling PIN_CHECK=unmet ... hidden=1 ...   (m1r1)
FAIL r2_hidden_fenced             PIN_CHECK=met   ... hidden=0 ...   (m1r2)
FAIL r3_lowercase_prefix          PIN_CHECK=met   ... unparsed=0 ... (m1r3)
FAIL r3_mixedcase_prefix          PIN_CHECK=met   ... unparsed=0 ... (m1r3)
```

## Survivor detail

### m2r1 — R1 case folding removable without a failing arm (false-red survivor)

Every selftest header cell is already lowercase, so removing `.lower()` changes nothing the arms can see.

Reproducer — SKILL.md variant with a title-case header cell (mutant scores **unmet**, real tool scores **met**):

```markdown
| name | kind | entry | verdict map | Self-Test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| foo | gate | `python3 tools/foo.py` | 0 ok | `python3 tools/foo.py --selftest` → `FOO_SELFTEST pass=3 fail=0` | none | none | mori |
```

Observed (`python3 <tool> --root <tree> --repo <scratch> --skill <doc>`):

```
pristine: rc=0  PIN_CHECK=met tally_pins=1 ... hidden=0
m2r1:     rc=1  pin line=3 kind=row state=hidden row='| foo | gate | `python3 tools/foo.py` | 0 ok | ...'
                PIN_CHECK=unmet tally_pins=0 ... hidden=1
```

(under the mutant the honest row is no longer inside a parsed table and is flagged `hidden` — the mutant rejects an honest document.)

Killing arm (one line, appended after `r1_header_self_test_spelling` in `cases`):

```python
cases.append(("r1_header_case_insensitive", HDR.replace("self-test", "Self-Test", 1) + row(good), 1, True, None))
```

Demonstrated: mutant + arm → `pass=60 fail=1`, rc=1, `FAIL r1_header_case_insensitive PIN_CHECK=unmet ... hidden=1 ...`; pristine + arm → `pass=61 fail=0`, rc=0.

### m2r2 — R2 `--selftest` trigger removable without a failing arm (false-green survivor)

All hidden-row arms use rows that carry an ASCII `[A-Z][A-Z0-9_]*SELFTEST` token, so the second trigger (`"--selftest" in raw`) is unexercised; removing it leaves every arm green.

Reproducer — SKILL.md variant with a row-shaped candidate line carrying `--selftest` but no uppercase SELFTEST token (mutant scores **met**, real tool scores **unmet**):

```markdown
| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| foo | gate | `python3 tools/foo.py` | 0 ok | `python3 tools/foo.py --selftest` → `FOO_SELFTEST pass=3 fail=0` | none | none | mori |

| hidd | gate | `bash tools/a.sh --selftest` | 0 ok | `clean` | none | none | mori |
```

Observed (same CLI form):

```
pristine: rc=1  pin line=5 kind=row state=hidden row='| hidd | gate | `bash tools/a.sh --selftest` | 0 ok | `clean` | ...'
                PIN_CHECK=unmet tally_pins=1 ... hidden=1
m2r2:     rc=0  PIN_CHECK=met tally_pins=1 ... hidden=0
```

Killing arm (appended after `r2_hidden_selftest_arg`):

```python
cases.append(("r2_hidden_selftest_arg_no_token", HDR + row(good) + "\n" + "| hidd | gate | `bash tools/a.sh --selftest` | 0 ok | `clean` | none | none | mori |\n", 1, False, "hidden"))
```

Demonstrated: mutant + arm → `pass=60 fail=1`, rc=1, `FAIL r2_hidden_selftest_arg_no_token PIN_CHECK=met ... hidden=0 ...`; pristine + arm → `pass=61 fail=0`, rc=0.

### m2r3 — R3 non-ascii-token branch removable without a failing arm (false-green survivor)

The only non-ascii arm (`r3_fullwidth_prefix`, `PIN_CHECK＿SELFTEST …`) is still caught after deletion: NFKC folds `＿`→`_` and the casefold branch returns `unparsed` (reason `casefold-selftest-prefix`). The non-ascii branch is therefore redundant for everything the arms pin — spans whose first token is non-ascii but never folds to a SELFTEST-shaped token.

Reproducer — SKILL.md variant with a decorative non-ascii span in the self-test cell (mutant scores **met**, real tool scores **unmet**):

```markdown
| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| foo | gate | `python3 tools/foo.py` | 0 ok | `python3 tools/foo.py --selftest` → `FOO_SELFTEST pass=3 fail=0`; `café — vérifié ✓` | none | none | mori |
```

Observed (same CLI form):

```
pristine: rc=1  pin line=3 kind=span state=unparsed reason=non-ascii-token span='café — vérifié ✓'
                PIN_CHECK=unmet tally_pins=1 ... unparsed=1
m2r3:     rc=0  PIN_CHECK=met tally_pins=1 ... unparsed=0
```

Killing arm (appended after `r3_mixedcase_prefix`):

```python
cases.append(("r3_nonascii_decorative_span", HDR + row(good + "; `café ✓`"), 1, False, "unparsed"))
```

Demonstrated: mutant + arm → `pass=60 fail=1`, rc=1, `FAIL r3_nonascii_decorative_span PIN_CHECK=met ... unparsed=0 ...`; pristine + arm → `pass=61 fail=0`, rc=0.

## Provenance, hashes, restoration

- Scratch lab: `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48MutV3Header/` (mutants `m1r1.py m2r1.py m1r2.py m2r2.py m1r3.py m2r3.py`; killer copies `k2r{1,2,3}.py` = survivor+arm; controls `p2r{1,2,3}.py` = pristine+arm; reproducer fixtures under `repro/`). All lane-tool runs used `TMPDIR=<scratch>`; no fixture repos were needed (the tool's own selftest builds its trees in the system temp dir, redirected to the scratch dir).
- The tracked file `tools/mori-pin-check.py` was never opened for writing; all edits were made to scratch copies only. No git/jj state was mutated (the only git use was a read-only `git status --porcelain`).
- Hashes: pristine/base `85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1`; after mutation — m1r1 `932c3388509ddf96d866fb137c1f7e62b140efe2bbdc4a3a315afcd8fdd57d35`, m2r1 `47f31856868f5ea6f002438d71426c1c90c4ffe64e2aa4d70960ed5313cf6ba9`, m1r2 `c7ffdd0d90d92576052bf0b93c30c04f5bfd447fc19c56aa05f86cc52f3bbfbd`, m2r2 `6bcd97908ae079b8d0328b8200084ee90bd9396eac6971d338d27695f6c46cd8`, m1r3 `d54798cac3aa8b3e80c954061286a50c32d1b0fdc3b5dd0b6a26588bacd745cb`, m2r3 `986355029481eaf401ea431ff533e21836b0f8c026ee16631a8461cfa653dd6a`.
- Restoration evidence (post-run, this session): `sha256sum tools/mori-pin-check.py` → `85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1`; `cmp` tracked vs pristine scratch copy → identical; `git status --porcelain -- tools/mori-pin-check.py` → empty (0 lines).
- No tool installs or upgrades were performed (existing python3 only). Nothing in this report depends on the C1/C2 counters; they were not run or judged here.
