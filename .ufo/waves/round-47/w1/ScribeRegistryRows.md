# ScribeRegistryRows — round 47 wave w1 (build + first falsifiers)

Seat: ScribeRegistryRows (leaf; no subagents dispatched). Lane: mori-shokunin.
Date: 2026-10-25. Freeze commit: `63eecf27` (entering tip `2d85e33d`).

Scope: draft two SKILL.md gate-registry rows (8 cells) for
`tools/mori-pin-check.py` and `.ufo/waves/round-47/count-c2.py` under a new
`### Round-47 registry additions` heading, run each `--selftest` under
`TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47-ScribeRegistryRows`,
pin the exact tally line and the sha256 of each file, read the docstring verdict
maps, ensure no unescaped `|` inside cells.

## Evidence

### Instrument bytes vs frozen contract

| file | freeze blob (git show 63eecf2) | contract sha256 | status |
|---|---|---|---|
| `tools/mori-pin-check.py` | `e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1` | `e3ef425…d903e1` | match |
| `.ufo/waves/round-47/count-c2.py` | `fc77b93338b3f49b9038eaac3832537b1be2e0ff9dff2476fef750153978901e` | `fc77b933…978901e` | match |

Commands:

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin
git show 63eecf2:tools/mori-pin-check.py | sha256sum
# e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1  -
git show 63eecf2:.ufo/waves/round-47/count-c2.py | sha256sum
# fc77b93338b3f49b9038eaac3832537b1be2e0ff9dff2476fef750153978901e  -
```

Working-tree observation: `.ufo/waves/round-47/count-c2.py` is byte-identical to
the freeze blob (`fc77b933…`, verified by `sha256sum` at report time). At my
first read, `tools/mori-pin-check.py` also matched the freeze hash
(`e3ef425…`); mid-session the working-tree copy changed to
`104cf3dd8174933799de97ec0b11e6cdb1923bb2bda1130f0bb3afeff1e4f56d` — `git diff`
shows one deletion (`bound = []`, a dead local in `pin_commands`). That edit is
not mine (I touched no production file); it is a concurrent in-flight change.
The selftests below were run on the **frozen committed bytes** (the bytes the
contract measures), extracted read-only via `git show` into my scratch dir.

### Selftest runs (TMPDIR = .scratch/r47-ScribeRegistryRows)

Run 1 — `python3 .scratch/r47-ScribeRegistryRows/mori-pin-check-freeze.py --selftest`
(extracted from `git show 63eecf2:tools/mori-pin-check.py`, sha256
`e3ef425…`):

- exit code: 0
- last line: `PIN_CHECK_SELFTEST pass=22 fail=0`
- all 22 cases printed `PASS`: honest, stale_tally, stale_in_cell_true_elsewhere,
  pin_moved_out_of_cell, digest_ok, digest_stale, malformed_row, no_command,
  digitless_pin, timeout, bare_flag_rev_entry, escaped_pipe_cell, below_floor,
  mutant_pin_bound_to_mutant, mutant_pin_wrong, tmpdir_inside_measured_tree,
  token_boundary_truncated_pin, baseline_row_deleted, baseline_all_present,
  nonzero_rc_with_fail0, cli_met_rc0, cli_bad_rev_rc2.

Run 2 — `python3 .scratch/r47-ScribeRegistryRows/count-c2-freeze.py --selftest`
(extracted from `git show 63eecf2:.ufo/waves/round-47/count-c2.py`, sha256
`fc77b933…`):

- exit code: 0
- last line: `C2_SELFTEST pass=13 fail=0`
- all 13 checks printed `PASS` (12 fixture cases + `cli_not_a_repo_rc2`).

### Verdict maps (from docstrings)

- `tools/mori-pin-check.py` (docstring lines 47–49): exit 0 met · 1 unmet · 2
  setup (usage, unresolvable revision/baseline, unreadable SKILL); output
  `PIN_CHECK=met|unmet tally_pins=N digest_pins=N mismatches=N unparsed=N no_command=N rev=…`.
- `.ufo/waves/round-47/count-c2.py` (docstring lines 17–21): exit 0 met · 1
  unmet · 2 setup; output
  `C2=met|unmet events=N rows=N name_mismatch=N field_mismatch=N callsite_mismatch=N pin_mismatch=N source_row=ok|bad provenance=ok|bad rev=R` plus `failed=` list when unmet.

### Tooling

No tool was installed or updated for this seat (plain `python3` used; per
RULES.md, no installs to record). No pacman transaction attempted.

## Draft registry rows (for L1 integration into SKILL.md)

```markdown
### Round-47 registry additions

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| registry pin reconciler (r47, C1) | gate | `python3 tools/mori-pin-check.py --rev <rev> [--repo DIR] [--min-tally-pins N] [--baseline-rev REV] [--skill PATH] [--timeout S]` (`--root DIR` measures a directory as-is) | 0 → `PIN_CHECK=met` (mismatches=0, unparsed=0, no_command=0, dropped=0, tally pins ≥ N) · 1 → `PIN_CHECK=unmet`, one `pin line=… state=mismatch\|unparsed\|no_command\|dropped` line per finding · 2 → `PIN_CHECK_SETUP` (no `--rev`/`--root`, unresolvable revision or baseline, unreadable SKILL) | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=22 fail=0` at sha256 `e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1` of `tools/mori-pin-check.py` | round-47 floor `--min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53` (`.ufo/waves/round-47/contract.md` P-C1); limits: line-count pins and truncated digests are not checked | its own export and TMPDIR under `<repo>/.scratch` (removed on exit); runs the registered selftests, which write only their own temp dirs | mori |
| r47 tracepoint catalogue (C2) | gate | `python3 .ufo/waves/round-47/count-c2.py <rev> [--repo DIR] [--entry PATH]` | 0 → `C2=met events=8 rows=8 …` · 1 → `C2=unmet … failed=<checks>` (entry absent, provenance, table, name/field/call-site mismatch, pin mismatch, source row) · 2 → `C2_SETUP` (usage, unresolvable revision) | `python3 .ufo/waves/round-47/count-c2.py --selftest` → `C2_SELFTEST pass=13 fail=0` at sha256 `fc77b93338b3f49b9038eaac3832537b1be2e0ff9dff2476fef750153978901e` of `.ufo/waves/round-47/count-c2.py` | sha256 of the four v7.2 copies under `corpus/evidence/sources-r47/` (in-script `PINS`); `ROW_ID = "S475"`; entry `corpus/knowledge/oom-tracepoints-r47.md` | none (read-only `git show`) | mori |
```

Notes on the drafts: both tallies are the exact observed `--selftest` lines
(reproduced from the frozen bytes, exit 0). Each row's full 64-hex sha256
pin names the file itself, so `tools/mori-pin-check.py` will match it against
the committed bytes at measure time. No cell contains an unescaped `|`; the
only literal pipes are escaped as `\|` in the row-1 verdict map. Docstring
exit maps are transcribed verbatim (0/1/2).

## Out-of-scope

No edits to SKILL.md, SOURCES.md, corpus/, tools/, LOG.md, SCORECARD.md or any
other production file. No git/jj mutations. No host-state changes. Nothing was
run under /tmp (lane tools ran with lane-local TMPDIR). Scratch used:
`.scratch/r47-ScribeRegistryRows/` (selftest transcripts
`pin-selftest-out.txt`, `c2-selftest-out.txt`, freeze extracts).

## Findings

1. Frozen instrument sha256 both match the contract's frozen bytes.
2. Both selftests pass on the frozen bytes; tally lines are exactly
   `PIN_CHECK_SELFTEST pass=22 fail=0` and `C2_SELFTEST pass=13 fail=0`.
3. Working-tree `tools/mori-pin-check.py` drifted mid-session (dead-line
   removal `bound = []`); current worktree sha256 `104cf3dd…` ≠ freeze. The
   contract measures the freeze bytes, so this does not affect P-C1's
   instrument, but L1 should be aware when integrating from the working tree.
