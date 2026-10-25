# ExecC1Replay — C1 control replay, round 48 wave w1

Seat: `ExecC1Replay` (leaf; no subagents). Lane: `mori-shokunin`. Date: 2026-10-25.
Entering tip `rev` = `e5dbac05459887d9597ea5d1da0d8e3d024e0d17`; baseline = `2d85e33d14198d388fd3cda9cc15ec07e57e7a53`.
Scratch: `.scratch/r48-ExecC1Replay/` (TMPDIR used for every lane tool run).
Report path: `.ufo/waves/round-48/w1/ExecC1Replay.md` (this file, lane-relative).

## 1. Selftest replay

Command (with `TMPDIR=…/r48-ExecC1Replay`):

```
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-48/count-c1.py --selftest
```

Observed output (exit 0):

```
PASS apply_J1 … (34 PASS lines, 0 FAIL) C1_SELFTEST pass=34 fail=0
```

Matches receipt `evidence/selftest-c1.txt` (`C1_SELFTEST pass=34 fail=0`).

## 2. Entering-tool control replay (receipt `evidence/control-c1-tool-v2-entering.txt`)

Command (control tool byte-identical to the frozen `controls/tool-v2-entering.py`, sha256
`9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6` = freeze `controls/tool-v2-entering.py`
and `tools/mori-pin-check.py` at `e5dbac05`; `--jobs 8`, `--scratch` under my scratch; ~198 s wall):

```
TMPDIR=…/r48-ExecC1Replay python3 …/round-48/count-c1.py \
  --tool …/round-48/controls/tool-v2-entering.py \
  --rev e5dbac05459887d9597ea5d1da0d8e3d024e0d17 --repo …/mori-shokunin \
  --scratch …/r48-ExecC1Replay/control-replay --jobs 8
```

Observed output (exit 1), identical to the receipt line-for-line:

```
variant name=J1 expect=unmet got=met rc=0
variant name=J2 expect=unmet got=met rc=0
variant name=J3 expect=unmet got=met rc=0
variant name=J4 expect=unmet got=met rc=0
variant name=J5 expect=unmet got=met rc=0
variant name=J6 expect=unmet got=met rc=0
variant name=J7 expect=unmet got=met rc=0
variant name=J8 expect=unmet got=met rc=0
variant name=H1 expect=met got=met rc=0
variant name=H2 expect=met got=met rc=0
variant name=H3 expect=met got=met rc=0
variant name=H4 expect=met got=met rc=0
variant name=real expect=met got=met rc=0
C1=unmet junk_met=8 honest_unmet=0 real=met errors=0 variants=12 rev=e5dbac05459887d9597ea5d1da0d8e3d024e0d17
rc=1
```

The other two C1 receipts were read (not re-run; they are control stubs, not the claim instrument):

- `evidence/control-c1-stub-always-met.txt` — stub green on all 12 variants + real: `C1=unmet junk_met=8 …`.
- `evidence/control-c1-stub-always-unmet.txt` — stub red on H1-H4 + real: `C1=unmet junk_met=0 honest_unmet=4 real=unmet …`.

## 3. Variant regeneration (from the counter's own functions)

Method: imported `count-c1.py` as a module (`importlib.util.spec_from_file_location`); took
`git show e5dbac05:SKILL.md` (150,380 bytes, 940 lines) as the base text; applied each of the
12 `VARIANTS` functions; wrote each body to `.scratch/r48-ExecC1Replay/variant-<name>.md`;
`diff -u -U0` against the unedited `skilled-unedited.md`. Anchors required by J7/J8 were
present at the rev (`(743 lines)` at line 184; `37fd7c24ff52…` at line 192), so no variant
raised `Anchor`; all 12 bodies differ from base (all `diff` rc=1).

Full zero-context unified diffs (identical to the observed output):

```diff
############ J1 ############
--- /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecC1Replay/skilled-unedited.md	2026-10-25 18:32:45.072759780 -0300
+++ /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecC1Replay/variant-J1.md	2026-10-25 18:32:45.074370490 -0300
@@ -936 +936 @@
-| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
+| name | kind | entry | verdict map | selftest | pinned values | write scope | owner |
@@ -938,2 +938,2 @@
-| registry pin reconciler (r47, C1) | gate | `python3 tools/mori-pin-check.py --rev <rev> [--repo DIR] [--min-tally-pins N] [--baseline-rev REV] [--skill PATH] [--timeout S]` (`--root DIR` measures a directory as-is) | 0 → `PIN_CHECK=met` (mismatches=0, unparsed=0, no_command=0, dropped=0, rebound=0, duplicate=0, tally pins ≥ N) · 1 → `PIN_CHECK=unmet`, one `pin … state=mismatch\|unparsed\|no_command\|dropped\|rebound\|duplicate` line per finding · 2 → `PIN_CHECK_SETUP` (no `--rev`/`--root`, unresolvable revision or baseline, unreadable SKILL) | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=34 fail=0` | round-47 floor `--min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53` (`.ufo/waves/round-47/contract.md` P-C1); limits: line-count pins and truncated digests are not checked | its own export and TMPDIR under `<repo>/.scratch` (removed on exit); runs the registered selftests, which write only their own temp dirs | mori |
-| r47 tracepoint catalogue (C2) | gate | `python3 .ufo/waves/round-47/count-c2.py <rev> [--repo DIR] [--entry PATH]` | 0 → `C2=met events=8 rows=8 …` · 1 → `C2=unmet … failed=<checks>` (entry absent, provenance, table, name/field/call-site mismatch, pin mismatch, source row) · 2 → `C2_SETUP` (usage, unresolvable revision) | `python3 .ufo/waves/round-47/count-c2.py --selftest` → `C2_SELFTEST pass=13 fail=0` | sha256 of the four v7.2 copies under `corpus/evidence/sources-r47/` (in-script `PINS`); `ROW_ID = "S475"`; entry `corpus/knowledge/oom-tracepoints-r47.md` | none (read-only `git show`) | mori |
+| registry pin reconciler (r47, C1) | gate | `python3 tools/mori-pin-check.py --rev <rev> [--repo DIR] [--min-tally-pins N] [--baseline-rev REV] [--skill PATH] [--timeout S]` (`--root DIR` measures a directory as-is) | 0 → `PIN_CHECK=met` (mismatches=0, unparsed=0, no_command=0, dropped=0, rebound=0, duplicate=0, tally pins ≥ N) · 1 → `PIN_CHECK=unmet`, one `pin … state=mismatch\|unparsed\|no_command\|dropped\|rebound\|duplicate` line per finding · 2 → `PIN_CHECK_SETUP` (no `--rev`/`--root`, unresolvable revision or baseline, unreadable SKILL) | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=1 fail=0` | round-47 floor `--min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53` (`.ufo/waves/round-47/contract.md` P-C1); limits: line-count pins and truncated digests are not checked | its own export and TMPDIR under `<repo>/.scratch` (removed on exit); runs the registered selftests, which write only their own temp dirs | mori |
+| r47 tracepoint catalogue (C2) | gate | `python3 .ufo/waves/round-47/count-c2.py <rev> [--repo DIR] [--entry PATH]` | 0 → `C2=met events=8 rows=8 …` · 1 → `C2=unmet … failed=<checks>` (entry absent, provenance, table, name/field/call-site mismatch, pin mismatch, source row) · 2 → `C2_SETUP` (usage, unresolvable revision) | `python3 .ufo/waves/round-47/count-c2.py --selftest` → `C2_SELFTEST pass=1 fail=0` | sha256 of the four v7.2 copies under `corpus/evidence/sources-r47/` (in-script `PINS`); `ROW_ID = "S475"`; entry `corpus/knowledge/oom-tracepoints-r47.md` | none (read-only `git show`) | mori |
diff rc=1
############ J2 ############
--- /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecC1Replay/skilled-unedited.md	2026-10-25 18:32:45.072759780 -0300
+++ /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecC1Replay/variant-J2.md	2026-10-25 18:32:45.076686930 -0300
@@ -939,0 +940 @@
+| r48 junk fullwidth | gate | `python3 tools/mori-pin-check.py --rev <rev>` | 0/1/2 | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK＿SELFTEST pass=999 fail=0` | none | none | mori |
diff rc=1
############ J3 ############
--- /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecC1Replay/skilled-unedited.md	2026-10-25 18:32:45.072759780 -0300
+++ /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecC1Replay/variant-J3.md	2026-10-25 18:32:45.078375370 -0300
@@ -939,0 +940 @@
+| r48 junk cyrillic | gate | `python3 tools/mori-pin-check.py --rev <rev>` | 0/1/2 | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SЕLFTEST pass=999 fail=0` | none | none | mori |
diff rc=1
############ J4 ############
--- /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecC1Replay/skilled-unedited.md	2026-10-25 18:32:45.072759780 -0300
+++ /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecC1Replay/variant-J4.md	2026-10-25 18:32:45.080072701 -0300
@@ -939,0 +940 @@
+| r48 junk archived copy | gate | `python3 .ufo/waves/round-40/fixtures/extracted/gate-v2-bb1f2457.py <rev> --round-base REV` | 0/1/2 | `python3 .ufo/waves/round-40/fixtures/extracted/gate-v2-bb1f2457.py --selftest` → `MORI_SOURCES_APPENDONLY_SELFTEST pass=12 fail=0` | none | none | mori |
diff rc=1
############ J5 ############
--- /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecC1Replay/skilled-unedited.md	2026-10-25 18:32:45.072759780 -0300
+++ /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecC1Replay/variant-J5.md	2026-10-25 18:32:45.081825081 -0300
@@ -938,2 +938,4 @@
-| registry pin reconciler (r47, C1) | gate | `python3 tools/mori-pin-check.py --rev <rev> [--repo DIR] [--min-tally-pins N] [--baseline-rev REV] [--skill PATH] [--timeout S]` (`--root DIR` measures a directory as-is) | 0 → `PIN_CHECK=met` (mismatches=0, unparsed=0, no_command=0, dropped=0, rebound=0, duplicate=0, tally pins ≥ N) · 1 → `PIN_CHECK=unmet`, one `pin … state=mismatch\|unparsed\|no_command\|dropped\|rebound\|duplicate` line per finding · 2 → `PIN_CHECK_SETUP` (no `--rev`/`--root`, unresolvable revision or baseline, unreadable SKILL) | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=34 fail=0` | round-47 floor `--min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53` (`.ufo/waves/round-47/contract.md` P-C1); limits: line-count pins and truncated digests are not checked | its own export and TMPDIR under `<repo>/.scratch` (removed on exit); runs the registered selftests, which write only their own temp dirs | mori |
-| r47 tracepoint catalogue (C2) | gate | `python3 .ufo/waves/round-47/count-c2.py <rev> [--repo DIR] [--entry PATH]` | 0 → `C2=met events=8 rows=8 …` · 1 → `C2=unmet … failed=<checks>` (entry absent, provenance, table, name/field/call-site mismatch, pin mismatch, source row) · 2 → `C2_SETUP` (usage, unresolvable revision) | `python3 .ufo/waves/round-47/count-c2.py --selftest` → `C2_SELFTEST pass=13 fail=0` | sha256 of the four v7.2 copies under `corpus/evidence/sources-r47/` (in-script `PINS`); `ROW_ID = "S475"`; entry `corpus/knowledge/oom-tracepoints-r47.md` | none (read-only `git show`) | mori |
+```markdown
+| registry pin reconciler (r47, C1) | gate | `python3 tools/mori-pin-check.py --rev <rev> [--repo DIR] [--min-tally-pins N] [--baseline-rev REV] [--skill PATH] [--timeout S]` (`--root DIR` measures a directory as-is) | 0 → `PIN_CHECK=met` (mismatches=0, unparsed=0, no_command=0, dropped=0, rebound=0, duplicate=0, tally pins ≥ N) · 1 → `PIN_CHECK=unmet`, one `pin … state=mismatch\|unparsed\|no_command\|dropped\|rebound\|duplicate` line per finding · 2 → `PIN_CHECK_SETUP` (no `--rev`/`--root`, unresolvable revision or baseline, unreadable SKILL) | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=1 fail=0` | round-47 floor `--min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53` (`.ufo/waves/round-47/contract.md` P-C1); limits: line-count pins and truncated digests are not checked | its own export and TMPDIR under `<repo>/.scratch` (removed on exit); runs the registered selftests, which write only their own temp dirs | mori |
+| r47 tracepoint catalogue (C2) | gate | `python3 .ufo/waves/round-47/count-c2.py <rev> [--repo DIR] [--entry PATH]` | 0 → `C2=met events=8 rows=8 …` · 1 → `C2=unmet … failed=<checks>` (entry absent, provenance, table, name/field/call-site mismatch, pin mismatch, source row) · 2 → `C2_SETUP` (usage, unresolvable revision) | `python3 .ufo/waves/round-47/count-c2.py --selftest` → `C2_SELFTEST pass=1 fail=0` | sha256 of the four v7.2 copies under `corpus/evidence/sources-r47/` (in-script `PINS`); `ROW_ID = "S475"`; entry `corpus/knowledge/oom-tracepoints-r47.md` | none (read-only `git show`) | mori |
+```
diff rc=1
############ J6 ############
--- /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecC1Replay/skilled-unedited.md	2026-10-25 18:32:45.072759780 -0300
+++ /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecC1Replay/variant-J6.md	2026-10-25 18:32:45.083957931 -0300
@@ -938 +938,2 @@
-| registry pin reconciler (r47, C1) | gate | `python3 tools/mori-pin-check.py --rev <rev> [--repo DIR] [--min-tally-pins N] [--baseline-rev REV] [--skill PATH] [--timeout S]` (`--root DIR` measures a directory as-is) | 0 → `PIN_CHECK=met` (mismatches=0, unparsed=0, no_command=0, dropped=0, rebound=0, duplicate=0, tally pins ≥ N) · 1 → `PIN_CHECK=unmet`, one `pin … state=mismatch\|unparsed\|no_command\|dropped\|rebound\|duplicate` line per finding · 2 → `PIN_CHECK_SETUP` (no `--rev`/`--root`, unresolvable revision or baseline, unreadable SKILL) | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=34 fail=0` | round-47 floor `--min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53` (`.ufo/waves/round-47/contract.md` P-C1); limits: line-count pins and truncated digests are not checked | its own export and TMPDIR under `<repo>/.scratch` (removed on exit); runs the registered selftests, which write only their own temp dirs | mori |
+
+| registry pin reconciler (r47, C1) | gate | `python3 tools/mori-pin-check.py --rev <rev> [--repo DIR] [--min-tally-pins N] [--baseline-rev REV] [--skill PATH] [--timeout S]` (`--root DIR` measures a directory as-is) | 0 → `PIN_CHECK=met` (mismatches=0, unparsed=0, no_command=0, dropped=0, rebound=0, duplicate=0, tally pins ≥ N) · 1 → `PIN_CHECK=unmet`, one `pin … state=mismatch\|unparsed\|no_command\|dropped\|rebound\|duplicate` line per finding · 2 → `PIN_CHECK_SETUP` (no `--rev`/`--root`, unresolvable revision or baseline, unreadable SKILL) | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=1 fail=0` | round-47 floor `--min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53` (`.ufo/waves/round-47/contract.md` P-C1); limits: line-count pins and truncated digests are not checked | its own export and TMPDIR under `<repo>/.scratch` (removed on exit); runs the registered selftests, which write only their own temp dirs | mori |
diff rc=1
############ J7 ############
--- /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecC1Replay/skilled-unedited.md	2026-10-25 18:32:45.072759780 -0300
+++ /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecC1Replay/variant-J7.md	2026-10-25 18:32:45.084620061 -0300
@@ -184 +184 @@
-| r44 gate registry (C2) | gate | `python3 tools/mori-gate-registry.py --rev <rev> --audit <repo-relative path> [--audit ...]` (`--registry PATH`, `--repo PATH`, `--selftest`) | 0 `REGISTRY=met` · 1 `REGISTRY=unmet` (unregistered path, a missing standard cell, an entry path that does not resolve at the revision, or no `--selftest` mode in the tool) · 2 `REGISTRY_SETUP` (usage, unresolvable revision, absent registry or gate table) | `python3 tools/mori-gate-registry.py --selftest` → measured `GATE_REGISTRY_SELFTEST pass=15 fail=0` at sha256 `8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832` (743 lines); v2 covers second-table registration, duplicate names, comment-only selftest, population mode and escape flags | in-script fixture registry rows; the audited surface is this SKILL.md `## Gates` table at `--rev` | stdout only; reads registry and audited paths at `--rev`; selftest fixtures use an isolated temporary tree | mori |
+| r44 gate registry (C2) | gate | `python3 tools/mori-gate-registry.py --rev <rev> --audit <repo-relative path> [--audit ...]` (`--registry PATH`, `--repo PATH`, `--selftest`) | 0 `REGISTRY=met` · 1 `REGISTRY=unmet` (unregistered path, a missing standard cell, an entry path that does not resolve at the revision, or no `--selftest` mode in the tool) · 2 `REGISTRY_SETUP` (usage, unresolvable revision, absent registry or gate table) | `python3 tools/mori-gate-registry.py --selftest` → measured `GATE_REGISTRY_SELFTEST pass=15 fail=0` at sha256 `8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832` (742 lines); v2 covers second-table registration, duplicate names, comment-only selftest, population mode and escape flags | in-script fixture registry rows; the audited surface is this SKILL.md `## Gates` table at `--rev` | stdout only; reads registry and audited paths at `--rev`; selftest fixtures use an isolated temporary tree | mori |
diff rc=1
############ J8 ############
--- /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecC1Replay/skilled-unedited.md	2026-10-25 18:32:45.072759780 -0300
+++ /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecC1Replay/variant-J8.md	2026-10-25 18:32:45.085429811 -0300
@@ -192 +192 @@
-| r45 corpus coverage (C3) | gate | `python3 .ufo/waves/round-45/count-c3.py <rev> --entry PATH --row S###` (`--entry`, `--row` and `--coverage-map` are each repeatable; `--root` defaults to the parent directory of `--repo`; `--census PATH` defaults to `<root>/scripts/sources-census.sh`; `--readme`, `--repo`, `--timeout S`, `--selftest`) | 0 → `C3=met rev=… entries=N rows=… census_sha256=…` · 1 → `C3=unmet` (an entry absent or missing `source:`/`verified-at:`/`recheck:`/`coverage-map:`, a declared row absent, not `mined`, or not naming the entry in `used-by`, a token collision such as S473 against S4731 or FR5 against FR12, a red census, or no README map row) · 2 → `C3_SETUP` (usage, a missing `--entry` or `--row`, unresolvable revision, census timeout) | `python3 .ufo/waves/round-45/count-c3.py --selftest` → measured `C3_SELFTEST pass=19 fail=0` rc 0 at sha256 `37fd7c24ff52…`; the mutant `.ufo/waves/round-45/fixtures/mutants/count-c3.py` (sha256 `69bf9b6eb29b…`) disables the census exit check (`proc.returncode == 0` to `True`) and its own run reads `C3_SELFTEST pass=17 fail=2` rc 1 | `--census` default `<root>/scripts/sources-census.sh`, whose sha256 the verdict line prints; the `corpus/README.md` map section; the declared entries and rows; lane `mori` | stdout only; fixtures are written under a `c3st-` `tempfile.mkdtemp` in the caller TMPDIR; the census arm executes `bash <root>/scripts/sources-census.sh validate --root <root> mori` with the caller's privileges, so that caller-named program is not sandboxed | mori |
+| r45 corpus coverage (C3) | gate | `python3 .ufo/waves/round-45/count-c3.py <rev> --entry PATH --row S###` (`--entry`, `--row` and `--coverage-map` are each repeatable; `--root` defaults to the parent directory of `--repo`; `--census PATH` defaults to `<root>/scripts/sources-census.sh`; `--readme`, `--repo`, `--timeout S`, `--selftest`) | 0 → `C3=met rev=… entries=N rows=… census_sha256=…` · 1 → `C3=unmet` (an entry absent or missing `source:`/`verified-at:`/`recheck:`/`coverage-map:`, a declared row absent, not `mined`, or not naming the entry in `used-by`, a token collision such as S473 against S4731 or FR5 against FR12, a red census, or no README map row) · 2 → `C3_SETUP` (usage, a missing `--entry` or `--row`, unresolvable revision, census timeout) | `python3 .ufo/waves/round-45/count-c3.py --selftest` → measured `C3_SELFTEST pass=19 fail=0` rc 0 at sha256 `37fd7c24ff53…`; the mutant `.ufo/waves/round-45/fixtures/mutants/count-c3.py` (sha256 `69bf9b6eb29b…`) disables the census exit check (`proc.returncode == 0` to `True`) and its own run reads `C3_SELFTEST pass=17 fail=2` rc 1 | `--census` default `<root>/scripts/sources-census.sh`, whose sha256 the verdict line prints; the `corpus/README.md` map section; the declared entries and rows; lane `mori` | stdout only; fixtures are written under a `c3st-` `tempfile.mkdtemp` in the caller TMPDIR; the census arm executes `bash <root>/scripts/sources-census.sh validate --root <root> mori` with the caller's privileges, so that caller-named program is not sandboxed | mori |
diff rc=1
############ H1 ############
--- /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecC1Replay/skilled-unedited.md	2026-10-25 18:32:45.072759780 -0300
+++ /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecC1Replay/variant-H1.md	2026-10-25 18:32:45.086251381 -0300
@@ -939,0 +940,2 @@
+
+A prose line appended by the round-48 honest control.
diff rc=1
############ H2 ############
--- /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecC1Replay/skilled-unedited.md	2026-10-25 18:32:45.072759780 -0300
+++ /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecC1Replay/variant-H2.md	2026-10-25 18:32:45.087898311 -0300
@@ -938 +938 @@
-| registry pin reconciler (r47, C1) | gate | `python3 tools/mori-pin-check.py --rev <rev> [--repo DIR] [--min-tally-pins N] [--baseline-rev REV] [--skill PATH] [--timeout S]` (`--root DIR` measures a directory as-is) | 0 → `PIN_CHECK=met` (mismatches=0, unparsed=0, no_command=0, dropped=0, rebound=0, duplicate=0, tally pins ≥ N) · 1 → `PIN_CHECK=unmet`, one `pin … state=mismatch\|unparsed\|no_command\|dropped\|rebound\|duplicate` line per finding · 2 → `PIN_CHECK_SETUP` (no `--rev`/`--root`, unresolvable revision or baseline, unreadable SKILL) | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=34 fail=0` | round-47 floor `--min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53` (`.ufo/waves/round-47/contract.md` P-C1); limits: line-count pins and truncated digests are not checked | its own export and TMPDIR under `<repo>/.scratch` (removed on exit); runs the registered selftests, which write only their own temp dirs | mori |
+| registry pin reconciler (r47, C1) | gate | `python3 tools/mori-pin-check.py --rev <rev> [--repo DIR] [--min-tally-pins N] [--baseline-rev REV] [--skill PATH] [--timeout S]` (`--root DIR` measures a directory as-is) | 0 → `PIN_CHECK=met` (mismatches=0, unparsed=0, no_command=0, dropped=0, rebound=0, duplicate=0, tally pins ≥ N) · 1 → `PIN_CHECK=unmet`, one `pin … state=mismatch\|unparsed\|no_command\|dropped\|rebound\|duplicate` line per finding · 2 → `PIN_CHECK_SETUP` (no `--rev`/`--root`, unresolvable revision or baseline, unreadable SKILL) | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=34 fail=0` | round-47 floor `--min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53` (`.ufo/waves/round-47/contract.md` P-C1); limits: line-count pins and truncated digests are not checked | its own export and TMPDIR under `<repo>/.scratch` (removed on exit); runs the registered selftests, which write only their own temp dirs | mori \|
diff rc=1
############ H3 ############
--- /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecC1Replay/skilled-unedited.md	2026-10-25 18:32:45.072759780 -0300
+++ /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecC1Replay/variant-H3.md	2026-10-25 18:32:45.088980828 -0300
@@ -936 +936 @@
-| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
+| name | kind | entry | verdict map | Self-Test | pinned values | write scope | owner |
diff rc=1
############ H4 ############
--- /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecC1Replay/skilled-unedited.md	2026-10-25 18:32:45.072759780 -0300
+++ /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecC1Replay/variant-H4.md	2026-10-25 18:32:45.091909621 -0300
@@ -939,0 +940 @@
+| r48 honest second pin row | gate | `python3 .ufo/waves/round-47/count-c2.py <rev> [--repo DIR]` | 0/1/2 | `python3 .ufo/waves/round-47/count-c2.py --selftest` → `C2_SELFTEST pass=13 fail=0` | none | none | mori |
diff rc=1
```

## 4. Per-variant verdicts (junk/honest, changed line)

| Var | Change (line in base SKILL.md) | Label | Why |
|---|---|---|---|
| J1 | header line 936 `self-test`→`selftest`; pins on the two r47 gate rows (lines 938-939) `pass=34 fail=0`→`pass=1 fail=0`, `pass=13 fail=0`→`pass=1 fail=0` | junk | The registry's self-test tally column now claims `PIN_CHECK_SELFTEST pass=1 fail=0` and `C2_SELFTEST pass=1 fail=0`. Both are false: the v2 tool's own `--selftest` (run at e5dbac05) prints `PIN_CHECK_SELFTEST pass=34 fail=0` rc 0, and `.ufo/waves/round-47/count-c2.py --selftest` prints `C2_SELFTEST pass=13 fail=0` rc 0. The header spelling change additionally ducks parsers looking for the `self-test` header cell. False claims in a trusted registry → junk. |
| J2 | new row line 940: tally prefix `PIN_CHECK＿SELFTEST` (U+FF3F fullwidth low line) with `pass=999 fail=0` | junk | The prefix is not an ASCII tally name; it would not be emitted by the tool (which prints only `PIN_CHECK_SELFTEST`), so the claimed `pass=999` is fabricated. Non-ASCII spelling hides the row from ASCII-aware matching while NFKC-folding it to the real name → misleading. |
| J3 | new row line 940: tally prefix `PIN_CHECK_SЕLFTEST` (Cyrillic `Е` U+0415) with `pass=999 fail=0` | junk | Same fabrication (`pass=999` never observed; tool emits only `PIN_CHECK_SELFTEST pass=34 fail=0`); foreign-script letter disguises the tally name. |
| J4 | new row line 940: `MORI_SOURCES_APPENDONLY_SELFTEST pass=12 fail=0` for `python3 .ufo/waves/round-40/fixtures/extracted/gate-v2-bb1f2457.py --selftest` | junk (nuance below) | The prefix `MORI_SOURCES_APPENDONLY_SELFTEST` is bound in the baseline to `python3 tools/mori-sources-appendonly.py --selftest` (baseline line 912, live tool). The new row rebinds the same prefix to a different argv (the archived round-40 fixture) and asserts `pass=12`, while the live appendonly row at e5dbac05 (line 912) asserts `pass=22` for the same prefix — my single variant run also observed the live tool printing `pass=22 fail=0` for that prefix. Two registry rows claiming the same tally name with different bindings and conflicting values is exactly the misleading "rebound by prefix" class. Nuance: the literal number is not fabricated — I ran the archived fixture's `--selftest` and it really prints `MORI_SOURCES_APPENDONLY_SELFTEST pass=12 fail=0` rc 0. The falsehood is the identity/binding, not the arithmetic. |
| J5 | lines 938-939 (the two r47 gate rows) replaced by a fenced ` ```markdown ` block carrying the same rows with pins corrupted to `pass=1 fail=0` | junk | Rows hidden inside a code fence while claiming `pass=1` — false tallies in a place a reader trusts (fences read as non-table content). |
| J6 | blank line inserted at line 938 (between separator and first data row); line 938/939 pin `pass=34 fail=0`→`pass=1 fail=0` | junk | The blank line detaches the row from its table; the corrupted pin is false (`pass=34` is the real value). |
| J7 | line 184 (r44 gate registry row): `(743 lines)`→`(742 lines)` | junk | `tools/mori-gate-registry.py` at e5dbac05 has 743 lines (verified: `git show e5dbac05:tools/mori-gate-registry.py | wc -l` → 743). The mutated claim (742) is false. |
| J8 | line 192 (r45 corpus coverage row): digest `37fd7c24ff52…`→`37fd7c24ff53…` | junk | The pin binds to `.ufo/waves/round-45/count-c3.py` (nearest preceding path in the cell); its sha256 at e5dbac05 starts `37fd7c24ff52d6aa…` (verified) so the original prefix is true and the mutant `…ff53…` is false. |
| H1 | one prose line appended after line 940 | honest | No registry fact changed; the appended prose is outside the table. |
| H2 | line 938 ends `|`→`\|` (escaped pipe) | honest | Pure markdown formatting; the cell content and pins are untouched (verified `pass=34 fail=0` still present). |
| H3 | header line 936 `self-test`→`Self-Test` | honest | Case-only change; same semantics, no fact altered. |
| H4 | new row line 940: `C2_SELFTEST pass=13 fail=0` for `python3 .ufo/waves/round-47/count-c2.py --selftest`, new row name `r48 honest second pin row` | honest | Verified: `.ufo/waves/round-47/count-c2.py --selftest` at e5dbac05 prints `C2_SELFTEST pass=13 fail=0` rc 0. The claim is true. |

## 5. Disputed labels

None. All eight J1-J8 are genuinely junk (a false or misleading claim in a place a reader
trusts) and all four H1-H4 are genuinely honest. The only nuance worth recording is J4 (its
literal pin value is true for the archived file; its junkness comes from rebinding a documented
prefix to a different instrument with a conflicting tally, and the contract's own named class
for it is "rebound by prefix"). I agree with the counter's labels.

## 6. Tooling

No tools were installed or upgraded (none were needed). No pacman/uv/npx/cargo actions.
Verified `sudo`-free read-only host access throughout.

## 7. Risks / notes for the L1

- The entering v2 tool is green (`PIN_CHECK=met`, rc 0) on all eight junk variants — confirmed
  independently — which is exactly the calibration gap P-C1 targets.
- The entrance control is heavyweight: each variant run executes every pinned selftest command in
  the registry (~26 tally pins; a single variant run ~72 s real). The full 13-run control took
  ~198 s wall with `--jobs 8`. Budget accordingly for the landed-tip acceptance run.
- First replay attempt used the default `--jobs 4` and was still running at 300 s (my own bash
  deadline), so it was killed and re-run with `--jobs 8` (197.6 s wall). Do not run this control
  with a timeout under ~5 minutes.
- Counter anchors that must survive at the landed tip: J7 needs `(743 lines)` and J8 needs
  `37fd7c24ff52…` in SKILL.md; if the landed registry edit rewords those cells, the counter exits
  2 (setup), not 0/1.
- The working-tree control bytes match the freeze sha256 (`9832e38c…`); no divergence.

## 8. Checks for the main agent

1. After v3 lands: `python3 .ufo/waves/round-48/count-c1.py --tool tools/mori-pin-check.py --rev <landed tip> --repo <lane> --scratch <scratch> --jobs 8` must print `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12` and exit 0.
2. Re-run `count-c1.py --selftest` (must stay `pass=34 fail=0`).
3. Confirm the landed v3 tool's own `--selftest` still prints `PIN_CHECK_SELFTEST pass=34 fail=0` (registry pins stay true at the landed tip).
