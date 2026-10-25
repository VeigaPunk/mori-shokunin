# RevVerdictMap — are the four verdict maps honest?

Reviewer: `L1Mori44-4.RevVerdictMap` (wave 1, leaf member; no subagent dispatch).
Measured repo: `/home/vgpnk/Projects/shokunin/mori-shokunin` at
`7cb59c6891d4f5d0266fe062565f094da835dc84` (the freeze commit).

Frozen-byte check before any run (`sha256sum` against
`.ufo/waves/round-44/evidence/freeze-r44.txt`): `contract.md`, `count-c1.py`,
`count-c2.py`, `count-c3.py`, `tools/mori-gate-registry.py`,
`fixtures/figures-r43.tsv` and `SKILL.md` all **MATCH** (`9477824d…`, `0095d0c6…`,
`a12170f1…`, `743996b1…`, `f9b1e2bf…`). Every verdict below was produced by those
bytes, executed read-only from the lane repo. No lane byte was edited; the only
lane file written is this report.

Fixtures: throwaway git repositories under `/tmp/r44vm-l1i6a19u` (ephemeral), each
one committed and then measured through `--repo <fixture>`. "Documented" means the
verdict-map cell of the tool's row in `SKILL.md` `## Gates` (rows 183-186).
"Observed" is the exit code plus the verdict/check lines actually printed.

The documented cells under test (verbatim clauses):

- **C1** (`count-c1.py`, SKILL.md:183): `0 C1=met mismatches=0 · 1 C1=unmet (a row's
  recomputed value differs from its asserted value, or a row/class floor fails) ·
  2 C1_SETUP (usage, unresolvable revision, git timeout); a ledger whose rows are
  not single git pipelines naming @REV@ is rejected, never scored`.
- **Auditor** (`tools/mori-gate-registry.py`, SKILL.md:184): `0 REGISTRY=met ·
  1 REGISTRY=unmet (unregistered path, a missing standard cell, an entry path that
  does not resolve at the revision, or no --selftest mode in the tool) · 2
  REGISTRY_SETUP (usage, unresolvable revision, absent registry or gate table)`.
- **C2** (`count-c2.py`, SKILL.md:185): `0 C2=met · 1 C2=unmet (absent counter,
  unregistered or thin row, no selftest tally, or a mutant its own selftest cannot
  catch) · 2 C2_SETUP (usage, unresolvable revision, git timeout)`.
- **C3** (`count-c3.py`, SKILL.md:186): `0 C3=met · 1 C3=unmet (entry absent or
  missing verified-at/recheck/coverage-map, a declared row absent or not mined or
  not naming the entry in used-by, a red census, or no README map row) · 2
  C3_SETUP (usage, unresolvable revision, git timeout)`.

---

## C1 — `count-c1.py`

Fixture base: `data.txt` = `x\nx\nx\n`; ledger `.ufo/waves/round-44/figures.tsv`;
honest row = `F0N<TAB>3<TAB><class><TAB>git show @REV@:data.txt | grep -c x`.

| # | named class | minimal fixture | observed verdict line | exit | documented | honest |
|---|---|---|---|---|---|---|
| 1 | met control | 12 rows, 4 classes, all honest | `check commands_reconcile PASS (all rows match)` → `C1=met mismatches=0` | 0 | 0 | yes |
| 2 | row value differs (mismatch) | F01 asserted `4`, observed 3 | `check commands_reconcile FAIL (F01 asserted=4 observed=3)` → `C1=unmet mismatches=1` | 1 | 1 | yes |
| 3 | row floor | 11 honest rows | `check row_floor FAIL (rows=11 min=12)` → `C1=unmet mismatches=0` | 1 | 1 | yes |
| 4 | class floor | 12 rows, 3 classes | `check class_floor FAIL (classes=evidence,registry,wave min=4)` → `C1=unmet mismatches=0` | 1 | 1 | yes |
| 5 | grammar: junk producer | row 1 = `echo 3` | `check rows_parse FAIL (row 1: command is not a git pipeline; row 1: command does not name @REV@; row 1: command carries a non-byte producer)` → `C1=unmet mismatches=?` | 1 | unassigned | exit consistent, see F2/F4 |
| 6 | grammar: no `@REV@` | row 1 = `git show HEAD:data.txt \| grep -c x` | `check rows_parse FAIL (row 1: command does not name @REV@)` → `C1=unmet mismatches=?` | 1 | unassigned | see F4 |
| 7 | grammar: compound | row 1 = `git show @REV@:data.txt \| grep -c x; true` | `check rows_parse FAIL (row 1: command is not a single pipeline; row 1: command carries a non-byte producer)` → `C1=unmet mismatches=?` | 1 | unassigned | see F4 |
| 8 | grammar: non-read verb | row 1 = `git config --get x` | `check rows_parse FAIL (row 1: git verb 'config' is not a read verb; row 1: command does not name @REV@)` → `C1=unmet mismatches=?` | 1 | unassigned | see F4 |
| 9 | ledger row hangs (`--timeout 1`) | row 1 = `git show @REV@:data.txt \| sleep 5 \| grep -c x` | `check commands_reconcile FAIL (F01 <- timeout after 1s)` → `C1=unmet mismatches=1` | 1 | 2 if "git timeout" is read to include rows | see F4 |
| 10 | usage | no revision argument | `usage: count-c1.py <rev\|WORK> [--repo PATH] [--ledger PATH] [--selftest]` | 2 | 2 | code yes, token no (F3) |
| 11 | unresolvable revision | `deadbeef` | `C1_SETUP cannot resolve revision 'deadbeef'` | 2 | 2 | yes |
| 12 | **git timeout at revision resolution** | `PATH` shim: `git rev-parse` sleeps 31 s (tool timeout 30 s) | traceback, last line `Setup: git timeout: rev-parse --verify de8a95e0…^{commit}` | **1** | **2 `C1_SETUP`** | **NO — F1** |
| 13 | git timeout inside evaluate | shim: `git cat-file` sleeps 31 s | `C1_SETUP git timeout: cat-file -e de8a95e0…:.ufo/waves/round-44/figures.tsv` | 2 | 2 | yes |
| 14 | extra (not named) | `--repo /tmp/does-not-exist-r44` | `C1_SETUP repo is not a git checkout: /tmp/does-not-exist-r44` | 2 | — | sane extra |
| 15 | extra (not named) | `--bogus` | argparse `count-c1.py: error: unrecognized arguments: --bogus` | 2 | — | sane extra |

Every named class is triggerable. The only exit-code divergence is #12 (F1). Note
the asymmetry that isolates it: the same timeout raised inside `evaluate()` (#13)
does produce the documented `C1_SETUP` exit 2; only the revision-resolution call in
`main()` sits outside the `try/except Setup` (`count-c1.py:315`; the `try` opens at
`:331`), so it escapes as a traceback and Python's default exit 1.

## C2 — `count-c2.py`

Fixture base: `SKILL.md` with the eight-cell gate table, `tools/mori-gate-registry.py`
(the frozen auditor bytes), `tools/fx-one.py` (selftest prints `FIX_SELFTEST
pass=2 fail=0`, exit 0), `fixtures/mutants/fx-one.py` (prints `pass=1 fail=1`,
exit 1), and a row naming `tools/fx-one.py` with all eight cells.

| # | named class | minimal fixture | observed verdict line | exit | documented | honest |
|---|---|---|---|---|---|---|
| 1 | met control | conformant counter + killed mutant | `check counters_present PASS` / `registry_rows PASS (REGISTRY=met)` / `tool_selftest PASS (pass=6 fail=0)` / `selftest_tally PASS (fx-one.py pass=2)` / `mutant_kill PASS (fx-one.py killed (fail=1))` → `C2=met` | 0 | 0 | yes |
| 2 | absent counter | `--counter tools/fx-two.py` (absent) | `check counters_present FAIL (absent=['tools/fx-two.py'])` … → `C2=unmet` | 1 | 1 | yes |
| 3 | unregistered | registry row names `tools/other.py` only | `check registry_rows FAIL (audit tools/fx-one.py FAIL (unregistered: no row names fx-one.py))` → `C2=unmet` | 1 | 1 | yes |
| 4 | thin row | row with the `pinned values` cell emptied | `check registry_rows FAIL (… FAIL (row 'fixture counter' missing cells: pinned values))` → `C2=unmet` | 1 | 1 | yes |
| 5 | no selftest tally | counter contains `--selftest` but prints `FIX=ok` | `check selftest_tally FAIL (fx-one.py no tally)` → `C2=unmet` | 1 | 1 | yes |
| 6 | surviving mutant | mutant selftest prints `pass=2 fail=0`, exit 0 | `check mutant_kill FAIL (fx-one.py SURVIVED (pass=2 fail=0))` → `C2=unmet` | 1 | 1 | yes |
| 7 | usage | no `--counter` | `usage: count-c2.py <rev\|WORK> --counter PATH [--counter PATH ...] [--selftest]` | 2 | 2 | code yes, token no (F3) |
| 8 | unresolvable revision | `deadbeef` | `C2_SETUP cannot resolve revision 'deadbeef'` | 2 | 2 | yes |
| 9 | **git timeout at revision resolution** | same 31 s shim | traceback, last line `Setup: git timeout: rev-parse --verify 7cc3a15c…^{commit}` | **1** | **2 `C2_SETUP`** | **NO — F1** |

All four named `C2=unmet` classes trigger and exit 1. #9 is the same call-site
defect as F1 (`count-c2.py:369`, outside the `try` that opens at `:374`).

## C3 — `count-c3.py`

Fixture base: `corpus/SOURCES.md` with an 11-cell row `S901` (status `mined`,
`used-by corpus/knowledge/fixture-entry.md`), an entry carrying `source: S901`,
`verified-at:`, `recheck:` and `coverage-map: FR5`, a `corpus/README.md` line naming
the entry, and a census stub exiting 0.

| # | named class | minimal fixture | observed verdict line | exit | documented | honest |
|---|---|---|---|---|---|---|
| 1 | met control | all five checks green | `check entry_present PASS` / `entry_meta PASS (sources S901)` / `rows_present PASS (rows S901 mined)` / `census_ok PASS (exit=0)` / `readme_row PASS (names entry)` → `C3=met` | 0 | 0 | yes |
| 2 | entry absent | entry path removed | `check entry_present FAIL (absent)` → `C3=unmet` | 1 | 1 | yes |
| 3 | entry missing `verified-at` | line deleted | `check entry_meta FAIL (verified-at:; source: lacks )` → `C3=unmet` | 1 | 1 | yes (detail bug F5) |
| 4 | entry missing `recheck` | line deleted | `check entry_meta FAIL (recheck:; source: lacks )` → `C3=unmet` | 1 | 1 | yes (F5) |
| 5 | entry `coverage-map` wrong | `FR5` → `FR4` | `check entry_meta FAIL (coverage-map FR5; source: lacks )` → `C3=unmet` | 1 | 1 | yes (F5) |
| 6 | declared row absent | `--row S902` (registry holds S901) | `check entry_meta FAIL (source: lacks S902)` + `check rows_present FAIL (S902 absent)` → `C3=unmet` | 1 | 1 | yes |
| 7 | row not `mined` | status `quarantined` | `check rows_present FAIL (S901 status='quarantined')` → `C3=unmet` | 1 | 1 | yes |
| 8 | `used-by` does not name the entry | `used-by` = `—` | `check rows_present FAIL (S901 used-by does not name the entry)` → `C3=unmet` | 1 | 1 | yes |
| 9 | red census | census stub exits 1 | `check census_ok FAIL (exit=1)` → `C3=unmet` | 1 | 1 | yes |
| 10 | no README map row | README without the entry path | `check readme_row FAIL (no line names the entry)` → `C3=unmet` | 1 | 1 | yes |
| 11 | usage | no `--row` | `usage: count-c3.py <rev\|WORK> --entry PATH --row S### [--row S### ...] [--selftest]` | 2 | 2 | code yes, token no (F3) |
| 12 | unresolvable revision | `deadbeef` | `C3_SETUP cannot resolve revision 'deadbeef'` | 2 | 2 | yes |
| 13 | **git timeout at revision resolution** | 65 s shim (C3's own git timeout is 60 s) | traceback, last line `Setup: git timeout: rev-parse --verify 259a8a1f…^{commit}` | **1** | **2 `C3_SETUP`** | **NO — F1** |
| 14 | git timeout inside evaluate | 65 s shim on `cat-file` | `C3_SETUP git timeout: cat-file -e 259a8a1f…:corpus/knowledge/fixture-entry.md` | 2 | 2 | yes |
| 15 | extra: census path missing | `--census /tmp/no-such-census.sh` | `check census_ok FAIL (exit=127)` → `C3=unmet` | 1 | 1 by "a red census" | see F6 |

All five named `C3=unmet` classes trigger and exit 1; the three documented exit-2
classes hold except the revision-resolution timeout (#13, F1). Note #15: a missing
census binary is scored as a red census (`exit=127`) rather than a setup error, and
the detail cannot distinguish the two.

## Auditor — `tools/mori-gate-registry.py`

Fixture base: `SKILL.md` `## Gates` table with one eight-cell row naming
`tools/fixture-tool.sh`; tool body contains `--selftest`.

| # | named class | minimal fixture | observed verdict line | exit | documented | honest |
|---|---|---|---|---|---|---|
| 1 | met control | complete row, entry resolves, `--selftest` present | `audit tools/fixture-tool.sh PASS (row 'fixture gate': 8 cells, entry resolves, --selftest present)` → `REGISTRY=met` | 0 | 0 | yes |
| 2 | unregistered path | audit `tools/other-tool.sh`, row names the fixture tool | `audit tools/other-tool.sh FAIL (unregistered: no row names other-tool.sh)` → `REGISTRY=unmet` | 1 | 1 | yes |
| 3 | missing standard cell | `owner` cell emptied | `audit tools/fixture-tool.sh FAIL (row 'fixture gate' missing cells: owner)` → `REGISTRY=unmet` | 1 | 1 | yes |
| 4 | entry path does not resolve | row entry and audit target both `tools/ghost-tool.sh`, file absent | `audit tools/ghost-tool.sh FAIL (row 'fixture gate' entry path does not resolve at 4ec6d48067f5)` → `REGISTRY=unmet` | 1 | 1 | yes |
| 5 | no `--selftest` mode | tool body `#!/bin/sh\nexit 0` | `audit tools/fixture-tool.sh FAIL (row 'fixture gate' tool has no --selftest mode)` → `REGISTRY=unmet` | 1 | 1 | yes |
| 6 | usage | `--rev` without `--audit` | `usage: mori-gate-registry.py --rev <rev\|WORK> --audit <path> [...] [--selftest]` | 2 | 2 | code yes, token no (F3) |
| 7 | unresolvable revision | `deadbeef` | `REGISTRY_SETUP cannot resolve revision 'deadbeef'` | 2 | 2 | yes |
| 8 | absent registry | `--registry MISSING.md` | `REGISTRY_SETUP registry absent at 26d4d4c0…: MISSING.md` | 2 | 2 | yes |
| 9 | no gate table | `SKILL.md` without `## Gates` | `REGISTRY_SETUP no gate table with a name/kind header in SKILL.md` | 2 | 2 | yes |
| 10 | extra: git timeout at revision resolution | 31 s shim | traceback, last line `subprocess.TimeoutExpired: Command '['git', … 'rev-parse', '--verify', …]' timed out after 30 seconds` | 1 | not named | see F1 |
| 11 | extra: git timeout inside audit | 31 s shim on `cat-file` | `REGISTRY_SETUP Command '['git', … 'cat-file', '-e', …]' timed out after 30 seconds` | 2 | not named | sane |

All four named `REGISTRY=unmet` classes trigger and exit 1; all four documented
exit-2 classes hold. The auditor's cell names no "git timeout" class, so #10 is not
a map contradiction, but it is the same structural defect as F1 and it is the only
timeout path a reader could hit without a `REGISTRY_SETUP` line.

---

## Findings

### F1 (major — map is false in all four instruments): a git timeout at revision resolution exits 1 with a traceback, not the documented 2

Documented: `2 C1_SETUP (usage, unresolvable revision, git timeout)`, `2 C2_SETUP
(… git timeout)`, `2 C3_SETUP (… git timeout)`; the auditor's cell has no timeout
class but documents `2 REGISTRY_SETUP` for setup failures.

Observed (one run each, `PATH` shim whose `git rev-parse` sleeps past the tool's own
timeout):

```
count-c1.py  <rev> --repo <fixture>   →  exit=1  traceback, "Setup: git timeout: rev-parse --verify de8a95e0…^{commit}"
count-c2.py  <rev> --repo <fixture> --counter tools/fx-one.py → exit=1  traceback, "Setup: git timeout: rev-parse --verify 7cc3a15c…^{commit}"
count-c3.py  <rev> --repo <fixture> --entry … --row S901 → exit=1  traceback, "Setup: git timeout: rev-parse --verify 259a8a1f…^{commit}"
mori-gate-registry.py --rev <rev> --repo <fixture> --audit tools/fixture-tool.sh → exit=1  traceback, "subprocess.TimeoutExpired … timed out after 30 seconds"
```

Cause: the `rev-parse --verify` call in each `main()` precedes the
`try/except Setup` (counters) / `try/except Exception` (auditor) block, so the
timeout exception escapes: `count-c1.py:315` (try at `:331`), `count-c2.py:369`
(try at `:374`), `count-c3.py:302` (try at `:307`), `tools/mori-gate-registry.py:290`
(try at `:295`). Proof that the guarded call sites behave as documented:
the same shim on `cat-file` yields `C1_SETUP git timeout: …` (exit 2),
`C3_SETUP git timeout: …` (exit 2) and `REGISTRY_SETUP … timed out after 30
seconds` (exit 2).

Impact: a hung git at revision resolution makes a `*_SETUP` (2) condition look like
a verdict failure (1) and prints a Python traceback instead of a one-line verdict.
The map's exit-2 clause is not honest for this path. Round-45 fix (frozen bytes are
not amended this round): move the rev-parse into the guarded region, or wrap it and
emit `<TOKEN>_SETUP`.

### F2 (medium — diagnostic honesty): a grammar-rejected ledger prints `commands_reconcile PASS (all rows match)` although zero rows were scored

On all four grammar fixtures the output contains both

```
check rows_parse           FAIL (row 1: command does not name @REV@)
check commands_reconcile   PASS (all rows match)
C1=unmet mismatches=?
```

The verdict line honors the map's "rejected, never scored" (`mismatches=?`), but
`commands_reconcile PASS (all rows match)` is a false claim: `evaluate()` skips the
row loop when `problems` is non-empty and leaves `mismatches` empty, and the
`record("commands_reconcile", not mismatches, …)` call therefore reports a pass on
an empty list. A reader skimming check lines would see a PASS on a rejected ledger.
Suggested fix for round 45: when `problems` is non-empty, record
`commands_reconcile` as skipped/failed with detail "not scored: grammar rejected".

### F3 (low — token mismatch): the exit-2 usage arm prints `usage:` and never the documented `*_SETUP` token

`count-c1.py`/`count-c2.py`/`count-c3.py`/`mori-gate-registry.py` with missing
required arguments exit 2 (matching the map) but print only `usage: …`; argparse
errors (`--bogus`) exit 2 with argparse's own message. The maps say `2 C1_SETUP
(usage, …)`, `2 C2_SETUP (usage, …)`, `2 C3_SETUP (usage, …)`, `2 REGISTRY_SETUP
(usage, …)`. Exit code honest, verdict token absent.

### F4 (low — documentation gap): two classes in C1's cell carry no exit code, and "git timeout" is narrower than it reads

- The grammar-rejection class is stated after the `0/1/2` map ("a ledger whose rows
  are not single git pipelines naming `@REV@` is rejected, never scored") with no
  exit code. Observed: exit 1, `C1=unmet mismatches=?`. Consistent with `unmet`, but
  unassigned; a reader cannot tell whether rejection is 1 or 2.
- "git timeout" under exit 2 does not cover a ledger row that exceeds `--timeout`:
  that row is scored as a mismatch (`check commands_reconcile FAIL (F01 <- timeout
  after 1s)`, `C1=unmet mismatches=1`, exit 1). Defensible (a hanging row is a bad
  row), but the map does not say that exit-2 "git timeout" means only the
  instrument's own git calls — the same wording now diverges from F1.

### F5 (low — diagnostic): C3's `entry_meta` detail appends a spurious `source: lacks ` clause

When only a metadata field is missing, the detail is
`check entry_meta FAIL (verified-at:; source: lacks )` — the trailing `source: lacks `
has an empty id list (`missing` non-empty but `absent_ids` empty). Verdict correct;
detail misleading. Same for `recheck` and a wrong `coverage-map`.

### F6 (low — class boundary): a missing `--census` path is scored as a red census

`--census /tmp/no-such-census.sh` → `check census_ok FAIL (exit=127)` → `C3=unmet`,
exit 1. The map's "a red census" covers any non-zero census exit, so this is not a
contradiction, but a setup error is indistinguishable from a red census in the
detail. Round-45 option: treat a non-executable/missing census as `C3_SETUP`.

### Observation (not a map defect; owned by CritSelftestHonesty): the auditor's `unresolved_entry_rejected` selftest arm does not exercise the branch it is named for

In `tools/mori-gate-registry.py` the arm rewrites the row's entry to
`tools/ghost-tool.sh` while auditing `tools/fixture-tool.sh`; the row then no longer
matches, so the branch taken is `unregistered`, not `entry path does not resolve`.
The documented branch is reachable and correct (finding-table row 4:
`FAIL (row 'fixture gate' entry path does not resolve at 4ec6d48067f5)`), so the
verdict map is honest; only the arm's label is wrong.

---

## What the maps get right

- No named class failed to trigger: C1 (mismatch, row floor, class floor, grammar
  rejection ×4, usage, unresolvable revision), C2 (absent counter, unregistered,
  thin row, no selftest tally, surviving mutant), C3 (entry absent, entry meta ×3,
  row absent, not mined, `used-by`, red census, README), auditor (unregistered,
  missing cell, unresolved entry, no `--selftest`).
- No observed **exit 2 where exit 1 is documented**; every named `unmet` class
  produced exit 1 and the `unmet` token; every met control produced the documented
  `met` token with exit 0.
- The auditor's four documented exit-2 classes (usage, unresolvable revision, absent
  registry, no gate table) all exit 2.

## Residual risk and verification gaps

- Fixtures are synthetic and minimal: they prove each named class is reachable and
  maps to its documented code; they do not prove the round's real artifacts (the
  ledger, the three counter rows, the C3 entry) will be scored as claimed. That is
  the after-measurement seat's job.
- The timeout arms inject a `git` shim on `PATH`; they confirm the tools' timeout
  handling, not a naturally hung repository. Thresholds differ per tool (30 s for
  C1/C2/auditor, 60 s for C3), which is why the C3 shim sleeps 65 s.
- Not exercised here: `WORK` mode; `--mutants-dir`/`--min-rows`/`--min-classes`
  overrides; a multi-counter C2 run (the real call passes three counters); the
  `--selftest` tallies of the four instruments themselves (only the auditor's
  selftest was executed, as C2's `tool_selftest` check: `pass=6 fail=0`); custom
  `--registry` tables other than `SKILL.md`.
