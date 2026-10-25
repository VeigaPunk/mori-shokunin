# ScribeSkillRows — round 48 w1 report

Seat: ScribeSkillRows (scribe). Lane: mori-shokunin. Date: 2026-10-25.
Task: draft the SKILL.md `## Round48` additions (fenced) — prose naming the C1 counter, v3
rules R1-R8 and the unlanded check; gate-table rows for the v3 pin reconciler, the C1 and C2
counters and the unlanded check; a decision-table row for FR2 quota observability. No product
files were edited; the draft lives only in this report.

## Files read

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-48/contract.md` (P-C1, P-C2,
  separability, frontier step; entering tip `e5dbac05`, freeze `4387cf94`).
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-48/v3-spec.md` (R1-R8).
- `/home/vgpnk/Projects/shokunin/mori-shokunin/SKILL.md` (top-level `## Decision table`,
  `## Round47` section, its gate-table header/rows, file tail at line 939).
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-48/count-c1.py` and
  `count-c2.py` (full source; usage, outputs, selftest arms).
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-48/evidence/` receipts:
  `control-c1-tool-v2-entering.txt`, `control-c2-donothing.txt`, `selftest-c1.txt`,
  `selftest-c2.txt`, `freeze-sha256.txt`.
- `/home/vgpnk/.omp/agent/RULES.md` (tooling authorization). No tool install or update was
  needed for this seat (no installs performed).

## Verification of the selftest pins (both run with lane TMPDIR)

Command (C1):
`TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ScribeSkillRows python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-48/count-c1.py --selftest`

Output: 34 `PASS` lines (`apply_J1`..`missing_anchor_is_setup`) then:
```
C1_SELFTEST pass=34 fail=0
```
Exit code: 0. Verified: the `C1_SELFTEST pass=34 fail=0` pin is real.

Command (C2):
`TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ScribeSkillRows python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-48/count-c2.py --selftest`

Output: 22 `PASS` lines (`honest_met`..`other_entry_path_unmet`) then:
```
C2_SELFTEST pass=22 fail=0
```
Exit code: 0. Verified: the `C2_SELFTEST pass=22 fail=0` pin is real.

Both match the frozen receipts `evidence/selftest-c1.txt` / `evidence/selftest-c2.txt`.

Git state (read-only): lane HEAD is the freeze commit `4387cf94`; entering tip `e5dbac05`
is its parent; `git status --porcelain` shows only untracked `.scratch/`, round-48 w1
dispatch/ready files and `.ufo/waves/round-48/w1/` (no tracked-file modifications).

## Unlanded check tally

The executor seat `ExecUnlandedCheck` (peer) was still running at report time; its candidate
`tools/mori-unlanded-check.py` and its selftest tally were not yet final. Per the seat
instruction the unlanded-check gate row uses the placeholder `UNLANDED_SELFTEST pass=<N> fail=0`
for the L1 to fill from the executor's candidate (the same placeholder rule applies to the v3
row's `PIN_CHECK_SELFTEST pass=<N> fail=0`).

## Draft — SKILL.md additions (fenced; L1 integrates)

Insert at the end of `/home/vgpnk/Projects/shokunin/mori-shokunin/SKILL.md` (after the
round-47 gate table, current line 939). Same eight columns as the Round47 table, header cell
`self-test`:

```markdown
## Round48 — registry pin reconciler v3, calibration/depth counters and the unlanded check

Round 48's calibration claim (C1) is scored by the frozen junk-variant counter
`.ufo/waves/round-48/count-c1.py`: it rewrites the measured revision's SKILL.md with eight
frozen junk edits J1-J8 of the round-47 gate table (header spelled `selftest`, fullwidth- and
Cyrillic-letter tally prefixes, a stale tally pinned to an archived instrument copy, the two
gate rows replaced by a fenced block, a blank line between header and first row, a line-count
pin off by one, a truncated digest pin off by one hex digit) and four honest edits H1-H4
(appended prose, trailing escaped pipe, header case only, a new honest c2 row), runs the tool
under test on each variant and on the real registry, and requires `PIN_CHECK=unmet` on all
junk, `PIN_CHECK=met` on every honest edit and on the registry. `tools/mori-pin-check.py`
moves to v3 per `.ufo/waves/round-48/v3-spec.md`, rules R1-R8: R1 header (the self-test cell
is recognised case-insensitively as `self-test`/`selftest`/`self test`), R2 visibility (a
non-table row carrying an ASCII `*SELFTEST` token or `--selftest` counts `hidden` and is
fatal; fenced blocks are not exempt), R3 ASCII (a backticked span whose first token holds a
non-ASCII character, or whose NFKC-casefolded text contains `selftest` without being an ASCII
tally pin, is `unparsed`), R4 rebound by prefix (a baseline prefix bound to an argv outside
its baseline set is `rebound`), R5 line-count pins (`(\d+) lines` binds to the nearest
preceding in-tree path; a mismatch or no such path is `mismatch`/`unparsed`), R6 truncated
digest pins (`[0-9a-f]{8,63}…` must prefix the sha256 of an in-tree path named in the row),
R7 residuals (escaped `\|` stays in-cell; a tally pin not at its span start is `unparsed`; a
setup failure exits 2 with one line, never a traceback), R8 selftest (an arm for every rule,
symlink containment of digest paths, each `argv_ok` sub-check, and case-insensitive
`unparsed` detection). The unlanded check `tools/mori-unlanded-check.py` (candidate drafted in
`.scratch/r48-ExecUnlandedCheck/`) closes round-47 routed defect 1 — late seat results left
uncommitted — by listing every path under `.ufo/waves/round-N/` and `corpus/lessons/` that is
untracked or modified relative to the lane's branch tip, so a seat's result cannot silently
stay off the committed record again.

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| registry pin reconciler v3 (r48, C1) | gate | `python3 tools/mori-pin-check.py --rev <rev> [--repo DIR] [--min-tally-pins N] [--baseline-rev REV] [--skill PATH] [--timeout S]` (`--root DIR` measures a directory as-is) | 0 → `PIN_CHECK=met` · 1 → `PIN_CHECK=unmet`, one `pin … state=mismatch\|unparsed\|no_command\|dropped\|rebound\|duplicate` line per finding · 2 → `PIN_CHECK_SETUP` (no `--rev`/`--root`, unresolvable revision or baseline, unreadable SKILL) — v3 appends counters after `duplicate=` and adds `hidden`/`mismatch` findings; see `.ufo/waves/round-48/v3-spec.md` R1-R8 | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=<N> fail=0` | supersedes the r47 row above (kept); round-47 floor `--min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53`; v3 rules R1-R8; scored by `count-c1.py` variants J1-J8/H1-H4 | its own export and TMPDIR under `<repo>/.scratch` (removed on exit); runs the registered selftests, which write only their own temp dirs | mori |
| round-48 C1 junk-variant counter | gate | `python3 .ufo/waves/round-48/count-c1.py --tool PATH [--rev R] [--repo DIR] [--baseline E] [--min-tally N] [--jobs N] [--scratch DIR]` | 0 → `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=R` · 1 → `C1=unmet …`, one `variant name=… expect=… got=… rc=…` line per variant · 2 → `C1_SETUP` (usage, unresolvable revision, SKILL.md unreadable at R, variant anchor absent) | `python3 .ufo/waves/round-48/count-c1.py --selftest` → `C1_SELFTEST pass=34 fail=0` | P-C1 flags `--min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53`; variants J1-J8/H1-H4 built into the counter; controls `controls/tool-v2-entering.py`, `controls/stub-always-met.py`, `controls/stub-always-unmet.py` with receipts `evidence/control-c1-*.txt`; freeze sha256 in `evidence/freeze-sha256.txt` | read-only `git show`; the tool under test writes only inside `--scratch` | mori |
| round-48 C2 quota-observability counter | gate | `python3 .ufo/waves/round-48/count-c2.py <rev> [--repo DIR] [--entry PATH]` | 0 → `C2=met claims=N located=N quote_missing=0 bad_rows=0 sources=S source_rows=ok pins=ok provenance=ok rev=R` (N ≥ 8, S ≥ 3) · 1 → `C2=unmet … failed=<checks>` (entry_absent, table, claims_floor, bad_rows, quote_missing, sources_floor, source_rows, pins, provenance) · 2 → `C2_SETUP` (usage, unresolvable revision) | `python3 .ufo/waves/round-48/count-c2.py --selftest` → `C2_SELFTEST pass=22 fail=0` | sha256 of the four copies under `corpus/evidence/sources-r48/` (in-script `COPIES`); entry `corpus/knowledge/quota-observability-r48.md`; SOURCES ids S479+ opened 2026-10-25, mined, with the entry in `used-by` | none (read-only `git show`) | mori |
| mori-unlanded-check (r48, routed defect 1) | gate | `python3 tools/mori-unlanded-check.py --repo DIR --round N` | 0 → `UNLANDED=clean` · 1 → `UNLANDED=unclean` listing every path under `.ufo/waves/round-N/` and `corpus/lessons/` that is untracked or modified relative to the lane's branch tip (`.scratch/` ignored) · 2 → usage / not-a-repo | `python3 tools/mori-unlanded-check.py --selftest` → `UNLANDED_SELFTEST pass=<N> fail=0` | round-47 late files (w2/CritV2Junk.md, w2/MutV2Rebound.md, w2/ScoutMisroot.md, w2-results.json) committed in 356fb94a; red before commit, green after | read-only `git status --porcelain=v1 -z --no-optional-locks` | mori |
```

Draft — decision-table row for FR2 quota observability (insert in the top-level `## Decision
table` of SKILL.md; same four columns):

```markdown
| Are filesystem quotas / EDQUOT observable? (FR2, r48) | `corpus/knowledge/quota-observability-r48.md` (claim/source/quote table, ≥8 rows, each quote 6-25 words located in a committed copy under `corpus/evidence/sources-r48/` — xfs_quota(8), quotactl(2), errno.h, Aliyun NAS quota page; rows cite SOURCES ids S479+ opened 2026-10-25, with the entry in `used-by`) | claiming quota behaviour without a located quote; treating EDQUOT as a generic error; using the rejected Solaris errno=49 doc or the HTTP 403 RHEL PDF | `python3 .ufo/waves/round-48/count-c2.py <rev>` → `C2=met claims=N located=N quote_missing=0 bad_rows=0 sources=S source_rows=ok pins=ok provenance=ok` |
```

## Notes for the L1

- `C1_SELFTEST pass=34 fail=0` and `C2_SELFTEST pass=22 fail=0` are real and verified (see
  above). The two `<N>` tallies (v3 row, unlanded-check row) are placeholders by instruction.
- The v3 row supersedes the r47 row but does not delete it; the r47 row keeps its own pin.
- The unlanded-check row's final tally/prefix should be taken from the executor's report
  (`w1/ExecUnlandedCheck.md`) once it lands; if its tool names a different selftest prefix,
  adjust the pin prefix to match the candidate's actual output.
- No tool installs were performed; RULES.md was read. No production files were touched.

Report: `.ufo/waves/round-48/w1/ScribeSkillRows.md`
