# Wave 2 — ReviewRoutedCode (C1 `tools/mori-routed-check.py` at a730ecfefbdb5c31b1db13aca2c40eecd5e97abc)

Reviewer: MoriR24.ReviewRoutedCode (leaf; no subagents dispatched).
Method: read the file at the pinned commit, then falsified each attack surface with
mutant commits and worktree mutants in scratch clones only
(`/fast/scratch/hyaku/mori-r24-a2/w2/MoriR24.ReviewRoutedCode/{review-clone,mc-r2,mc-r4,mc-git}`).
No tool installs were needed (python3 3.14.8, git 2.56.0, both already present).
All line numbers refer to `tools/mori-routed-check.py` at a730ecf.
Every result below was actually run; commands are reproducible verbatim.

## Declared values reproduce

- After-value: `python3 -I tools/mori-routed-check.py --repo /home/vgpnk/Projects/shokunin/mori-shokunin --rev a730ecfefbdb5c31b1db13aca2c40eecd5e97abc`
  → `"held": 4, "items": 4`, exit 0. Confirmed.
- Before: `--repo <scratch clone> --rev c725aa37aa3c9ec4f34e3c2abc8ca1b616c7c130 --round 23`
  → held 3/4, R4 red (`attempt_ledger_not_clean`, `dispatch_committed_after_dispatch`×7,
  `dispatch_path_missing`×8), exit 1. Confirmed.
- `--rev c725aa37... --round 24` → R4 red `no_round_ledger`, exit 1. Confirmed.

## Findings by severity

### F1 — HIGH — R2 goes green on a committed privacy-clearance violation via an uncommitted working-tree `.gitattributes` (isolation claim broken)

`tools/mori-routed-check.py:6-7` claims "Every predicate reads git objects only … the
working tree is never consulted". False for R2's added-line scan. `_git_env()`
(lines 114-124) neutralizes config (GIT_CONFIG_GLOBAL, GIT_CONFIG_NOSYSTEM) and passes
`--no-textconv` (line 232 of the diff invocation, lines 224-239), but sets no
`GIT_ATTR_SOURCE` and no attribute pin. `git -C repo diff base rev` in a non-bare repo
reads attribute sources from the repo's **working tree** (`.gitattributes`,
`.git/info/attributes`), so one uncommitted line `LOG.md -diff` makes git report the file
as binary, no `+` lines are emitted, and the scan (lines 245-261) sees nothing.

A/B proof, same commit `b2ce05c` (mutant: `privacy_clearance = true` appended to LOG.md,
in A1 scope), scratch clone `mc-r2`:

```
# without attributes: red
python3 -I $S/mc-r2/tools/mori-routed-check.py --repo $S/mc-r2 --rev b2ce05c --round 24
  → exit 1; R2 held False ['privacy_clearance_true_line_added']
# same rev, one uncommitted worktree file:  printf 'LOG.md -diff\n' > .gitattributes
python3 -I $S/mc-r2/tools/mori-routed-check.py --repo $S/mc-r2 --rev b2ce05c --round 24
  → exit 0; R2 held True, reasons [], exit 0 for the whole check
```

The only difference between the two runs is the uncommitted worktree file. A mutant needs
zero commits to silence R2. Latent same-class vectors: `repo/.git/info/attributes`, and the
global `core.attributesFile` default `~/.config/git/attributes` (config nulling does not
remove this default; `HOME` falls back to the passwd entry). On this host today
`/home/vgpnk/.config/git/` contains only `config`, so the global variant is latent, not live.

### F2 — HIGH — R1 goes green with `CaseEscapedSpace` committed under `tools/` when the file name is not valid UTF-8

`_list_paths` decodes `ls-tree -z` records with `errors="replace"` (line 217); the mangled
path then fails `_blob_bytes`, and `_check_r1` silently skips the file
(lines 398-402: `except GitUnavailable: continue`). End-to-end proof, scratch clone `mc-r4`,
rev `4028ad0` — the only mutation from a fully green rev (91b5261) is a committed file
named `tools/bad\xff.py` whose blob is `x = "CaseEscapedSpace"`:

```
python3 -I $S/mc-r4/tools/mori-routed-check.py --repo $S/mc-r4 --rev 4028ad0 --round 24
  → exit 0, held 4/4, R1 detail historical_case_hits: []
git ls-tree -r -z 4028ad0   → path bytes b'tools/bad\xff.py' present, blob contains the needle
```

Contract A4's R1 predicate "no file under tools/ contains CaseEscapedSpace" is violated;
the check says held.

### F3 — MEDIUM — R2 goes green on an added line whose content starts `++ ` (diff parser swallows it as a file header)

The parser at lines 245-261 is line-count-blind: the `+++ ` file-header branch
(lines 249-257) runs before the added-line branch (260-261) and `continue`s without
appending. An added line with content `++ privacy_clearance = true` is emitted by git as
`+++ privacy_clearance = true` — verified in git's own raw diff output
(`git diff c725aa37..34c1f1c -- PROVINCE.md`, line 62 of the output) — and is parsed as a
header, never scanned. Proof, scratch clone `mc-r2`:

```
python3 -I $S/mc-r2/tools/mori-routed-check.py --repo $S/mc-r2 --rev 34c1f1c --round 24
  → exit 0; R2 held True although PROVINCE.md at that rev contains the violating line
# control: plain line re-added (c508c9a) is caught → exit 1, R2 red
```

### F4 — LOW — argparse usage errors exit 2 with no JSON

`args = parser.parse_args(...)` (line 680): `--round abc` exits 2, prints usage to stderr,
leaves stdout empty. Contract C1 reserves exit 2 for "repo/rev/base cannot be read" with
one JSON object on stdout; a wrapper keying on exit codes cannot distinguish a usage error
from could-not-evaluate. True exit-2 cases are clean (all verified):
`--round 0` → JSON `could-not-evaluate`; unresolvable rev → JSON `could-not-evaluate`;
nonexistent repo → JSON `could-not-evaluate`; `--rev=-HEAD` → JSON `could-not-evaluate`.

### F5 — LOW — dispatched ledger tool runs with the operator's real HOME

`_run_ledger_verify` line 333: `env["HOME"] = env.get("HOME", os.path.expanduser("~"))` —
`_git_env()` never sets HOME, so this always resolves to the caller's real home. The
dispatched bytes are repo-controlled code at rev (declared design, docstring lines 12-13;
execution is bounded by the sandbox-only mutation rule), but the real-HOME pin is an
avoidable isolation gap on top of that design. Timeout of the dispatched tool fails closed
(TimeoutExpired → GitUnavailable → `dispatch_ledger_tool_unavailable`, red R4, exit 1 —
code path lines 563-569).

## Checked and passed (evidence, not assumption)

- **git environment isolation / cwd hijack — refuted by test.** Hypothesis: `PATH`
  defaults to `os.defpath` with an empty first element, letting a repo-cwd executable
  named `git` hijack every git call. Disproved on this runtime: Python 3.14.8 has
  `os.defpath == '/bin:/usr/bin'` (absolute, no empty element). Executable wrapper placed
  at `<clone>/git` and runs with cwd=clone root never executed (0 marker lines across
  T1a/T1b; verdicts unchanged). Env replacement also blocks caller GIT_DIR/GIT_CONFIG
  leakage. Caveat for other hosts: on runtimes with the legacy `:/bin:/usr/bin` defpath
  the hijack would exist; the tool's guarantee is Python-version-sensitive here.
- **subprocess argument safety.** All git and ledger invocations are list-form without a
  shell; `rev` is resolved to a 40-hex commit before any object read (lines 688-696), so
  no `rev:path` metacharacter path survives; ledger argv is
  `[sys.executable, "-I", "-", "verify", "--repo", repo, "--rev", <hex>, "--ledger", <committed path>]`.
- **revision validation.** Bad rev/repo/round/base produce JSON `could-not-evaluate`
  exit 2 (each exercised, see F4 list).
- **dispatch-ledger exit 2 → red R4.** Synthetic ledger w95d (dispatch_path missing at
  rev) → committed tool exits 2 → R4 red with `attempt_ledger_not_clean` +
  `ledger_finding:DISPATCH_PATH_UNAVAILABLE` + `dispatch_not_committed`, overall exit 1
  (not 2). Mapping at lines 574-578 fails closed and surfaces finding IDs.
- **timezone handling of `at`.** `_parse_timestamp` (lines 285-298) rejects naive values
  and normalizes Z. Verified with fixture ledgers (round-95, dispatch last changed
  2026-10-21T12:00Z, epoch 1792584000): row at `2026-10-21T15:00:00+02:00` and row at
  `2026-10-21T13:00:00+00:00` are the same instant — both `bound_before_call`, identical
  `at_epoch` 1792587600, R4 held 4/4 exit 0. Naive `2026-10-21T13:00:00` →
  `dispatch_at_invalid` red (and the dispatched tool flags AT_INVALID). Comparison against
  committer epoch (line 612) is correct.
- **last-changed commit lookup.** `_last_change_epoch` (lines 300-315) picks the commit
  that last *modified* the dispatch blob, not the creating commit: with commits at 10:00Z
  (create) and 12:00Z (modify), row `at` 10:30Z → red
  `dispatch_committed_after_dispatch` (changed_epoch 1792584000 > at_epoch 1792578600);
  rows after 12:00Z → green.
- **R2 scope per A1.** `R2_SCAN_SCOPE` (lines 57-64) is exactly SCORECARD.md, PROVINCE.md,
  SKILL.md, LOG.md, README.md, corpus/. `scanned_paths` across all runs never contained a
  `.ufo/` or `tools/` path. Plain violating lines in scope files are caught (M1/M3 red).
- **exit codes 0/1/2 main paths.** held==4 → 0 (tip and fixtures), any red → 1
  (round-23 base, all mutants), repo/rev/base unreadable → 2 (edge runs above).

## Residual risk and verification gaps

- Only one attribute-vector variant was proven (`LOG.md -diff` in the worktree); `* -diff`,
  `.git/info/attributes`, and a live global attributesFile are the same mechanism but were
  not each exercised.
- The diff parser was not fuzzed beyond the `++ ` case; any future fix should track hunk
  line counts instead of header-sniffing (F3 class).
- `_last_change_epoch` uses default history simplification; exotic merge topologies
  (evil merges, octopus) were not tested.
- The dispatched `tools/mori-dispatch-ledger.py` bytes at rev execute with operator
  privileges (declared design; real HOME added by F5). No hostile committed ledger tool
  was executed beyond the sandbox fixtures.
- F2's skip likely affects any per-path blob read driven by `_list_paths`; only the R1
  needle scan was proven end-to-end.

Mutant commits cited: mc-r2 `b2ce05c` (M1), `34c1f1c` (M2), `c508c9a` (M3), `5f3d54c` (M4);
mc-r4 `91b5261`, `04bc15a`, `fbff793`, `89a585c`, `6b599f8`, `4028ad0`. All exist only in
`/fast/scratch/hyaku/mori-r24-a2/w2/MoriR24.ReviewRoutedCode/` clones; the lane repo was
never mutated (report file excepted). Tooling installs: none.
