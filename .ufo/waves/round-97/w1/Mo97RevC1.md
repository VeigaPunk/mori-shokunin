# Mo97RevC1 — reviewer, claim C1 (gate registry backfill), mori round 97 w1

Landed rev `e85ed91249953094b067554bfa79fcdc65791f8e`, freeze `dd1ae1150f53df54e7530311b2323368e3c0e5e9`.
Method: landing tree materialized via `git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive e85ed912… | tar -x -C /fast/scratch/hyaku/mori-r97/Mo97RevC1/landing`; working-tree SKILL.md and all four tools sha256-identical to the landing copies (SKILL.md `923c22b3a62777064ced20b3b7e6f1347fca5a211aeaeda78b376e118a381de6`; tools `aa5bfc37…`, `61ea74cc…`, `662fafde…`, `38f9ea77…`). Every cell below cites the landed bytes.

## 1. Append-only (SKILL.md)

`git -C …/mori-shokunin diff dd1ae115… e85ed912… -- SKILL.md`: one hunk `@@ -1429,3 +1429,20 @@`, `+18` lines matching `^+` (17 content lines + the `+++ b/SKILL.md` header), `-1` line matching `^-` and that line is the `--- a/SKILL.md` diff header itself — **0 content lines removed**. Full landing diffstat touches only `SKILL.md` (+17) and C2 corpus files; no `tools/` bytes moved. The section is the file's tail (SKILL.md is 1448 lines; line 1448 is the fourth row). **Append-only: accurate.**

## 2. Auditor at the landing revision (ran now)

```
$ python3 tools/mori-gate-registry.py --rev e85ed91249953094b067554bfa79fcdc65791f8e --repo /home/vgpnk/Projects/shokunin/mori-shokunin --audit-all
audit tools/mori-cgroup-pressure.py        PASS row='cgroup PSI survey (r62 tool, registry r97)' (8 cells, entry resolves, --selftest argv branch)
audit tools/mori-drift-recheck.py          PASS row='drift re-check (r66 tool, registry r97)' (8 cells, entry resolves, --selftest argv branch)
audit tools/mori-scorecard-calibration.py  PASS row='SCORECARD Last-change calibration counter (r96 tool, registry r97)' (8 cells, entry resolves, --selftest argv branch)
audit tools/mori-source-digest.py          PASS row='SOURCES digest check (r91 tool, registry r97)' (8 cells, entry resolves, --selftest argv branch)
tables=17
rev=e85ed91249953094b067554bfa79fcdc65791f8e
registered=65 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0 tables=17
REGISTRY=met
(ec=0)
```

## 3. Self-tests run now (landing bytes, TMPDIR=$S)

| tool | final line now | ec | pinned cell (SKILL.md) | match |
|---|---|---|---|---|
| mori-cgroup-pressure.py | `MORI_CGROUP_PRESSURE_SELFTEST: pass=12 fail=0` | 0 | same, "(r97 landing)" | verbatim |
| mori-drift-recheck.py | `MORI_DRIFT_RECHECK_SELFTEST: PASS (10 cases)` | 0 | same, "(r97 landing; fixtures served on 127.0.0.1)" | verbatim |
| mori-scorecard-calibration.py | `CALIB_SELFTEST pass=11 fail=0` | 0 | same, "(r97 landing)" | verbatim |
| mori-source-digest.py | `DIGEST_SELFTEST pass=11 fail=0` | 0 | same, "(r97 landing)" | verbatim |

## 4. Cell-by-cell (row file:line = SKILL.md; source file:line = tools/<tool>.py)

### Row 1 — `cgroup PSI survey (r62 tool, registry r97)` (SKILL.md:1445)
- **name**: accurate — first landing commit `43cfbb10 "round-62: freeze C1/C2 instruments, cgroup-pressure probe…"`.
- **kind `probe`**: accurate — docstring "Read-only per-cgroup pressure (PSI) survey" (:1-2), "Detection and report only" (:12).
- **entry**: accurate — `--root` default `/sys/fs/cgroup` (:44), `--group PATH` (:45, default `user.slice`), `--resources cpu,memory,io,irq` (:39, :242-243), `--warn-avg10 N` (:244-245); `--selftest`/`--cases`/`--scratch` all real flags (:246-251). All bracketed as optional and all have defaults.
- **verdict map**: accurate — "one JSON object (schema `mori-cgroup-pressure-v1`)" (:35, :197-198) "then a `MORI_CGROUP_PRESSURE:` verdict line" (:218-219); `0 -> ok or high-guarded · 1 -> high · 2 -> partial or unavailable` mirrors the tool docstring verbatim (:19-21) and the constants `RC_OK=0 RC_HIGH=1 RC_PARTIAL=2 RC_UNAVAILABLE=2` (:55-57) with verdict selection (:215-216) and `rc = RC_HIGH if… else RC_OK if… else RC_PARTIAL` (:216). Note (pre-existing wording, not a row defect): the only exit-0 verdict the landed code produces is `PRESSURE_OK`; "high-guarded" is the r62 docstring's own vocabulary ("as mori-pressure-v1", :20) with no reachable `GUARDED` token. The "zero is never evidence of no stall" clause is docstring (:9-11) + `PSI_ACCOUNTING_DISABLED` finding (:177-183).
- **self-test**: accurate — command spelled exactly; final line matches run-now byte-for-byte; exit 0 iff `fail==0 and passed>0` (:324).
- **pinned values**: accurate — `tools/fixtures/mori-cgroup-pressure/cases.json` exists in the landing tree (default cases path :257-260); `psi.c:1285-1294` (docstring cites psi.c:1285-1288 and :1292-1294, both inside the stated span, :4-6) and `cgroup-v2.rst:1066-1074` (:7-8) are named in the docstring.
- **write scope**: accurate — main path opens cgroupfs read-only (:90-97, :118-126), writes only stdout (:346-347); docstring "opens files read-only, writes nothing to cgroupfs or /proc, registers no PSI trigger" (:12-14). Landed `_selftest` performs no disk writes at all (reads fixtures, prints; :282-324); `--scratch` ("selftest temp output; honored, TMPDIR fallback", :248-249) is accepted but currently unused — conservative over-disclosure, no contradiction.
- **owner `mori`**: accurate — lane-authored tool.

### Row 2 — `drift re-check (r66 tool, registry r97)` (SKILL.md:1446)
- **name**: accurate — first landing commit `c62683fb "round-66: the standing drift re-check — mori-drift-recheck.py…"`.
- **kind `probe`**: accurate — fetches and classifies; reports, does not gate surfaces.
- **entry**: accurate — cell matches the usage block verbatim (:7-9): `--root DIR [--only S###,S###] [--second-ua UA]` or `--from-sweep RECEIPT` (+ `--selftest`); `--only`/`--from-sweep` mutually exclusive (:646-649).
- **verdict map**: **accurate with one omission** — token list fresh/excerpt/time-churn/asset-churn/receipt-open/receipt-stale/ua-serving/content-drift/gate/unavailable = `TOKENS` (:161-162), decided at :295-341; `<id> no-copy` (:279, :286); summary `MORI_DRIFT_RECHECK rows=… adjudicated=… … window=…` (:341-347); `0 ->` every copy-bearing row carries a token / `1 ->` any unresolved (`return 1 if unresolved else 0`, :348) / `2 ->` setup (missing upstream tool chain :221-229, unreadable SOURCES.md :234-237, bad usage :629-657, from-sweep disagreement :335-339). Omission: the tool can also emit `<id> unresolved as-of=T` (:328-330) when a receipt-shaped copy has no parsable header sha256 (`elif h is None: token = None`, :303); that row shape is absent from the cell's token enumeration, though the cell's exit leg discloses the state ("1 -> any unresolved"). Minor; does not touch predicate P1(c) (`MORI_DRIFT_RECHECK` present, :341).
- **self-test**: accurate — final line matches run-now verbatim; ec=0; fixtures bound on `127.0.0.1` (:447 `ThreadingHTTPServer(("127.0.0.1", 0)…`, docstring :105-106).
- **pinned values**: accurate — `STAMP_CLASS_NAME = "python-docs-page-stamp"` (:144) ground S577 (:76-77); `ASSET_CLASS_NAME = "learn-microsoft-asset-build-id"` (:153); newest copy `corpus/evidence/sources-r<N>/<id>.<ext>` per row — upstream `find_copy` "highest N" (`mori-drift-adjudicate.py:60 COPY_DIR_RE`, `:88` docstring; convention stated at `mori-source-drift.py:11`).
- **write scope**: accurate — "Read-only under DIR; the selftest serves fixtures on 127.0.0.1 only" (:105-106); run() emits to stdout (:264, :341); fetched bodies held in memory, no file writes outside the selftest's own tempdir fixtures (:456-485).
- **owner `mori`**: accurate.

### Row 3 — `SCORECARD Last-change calibration counter (r96 tool, registry r97)` (SKILL.md:1447)
- **name**: accurate — first landing commit `9bde9322 "round-96: calibration counter…"`.
- **kind `gate`**: accurate — exit code decides met/unmet.
- **entry**: accurate — `rev` positional + `--manifest`/`--repo`/`--base` (:483-490; usage :11).
- **verdict map**: accurate — per axis `axis <name> cell=… expect=… state=ok|mismatch|error` (:204, docstring :18); summary `C1=met|unmet axes=6 mismatches=M columns_unchanged=yes|no rows=R rev=<sha12>` (:208-216; `rev_full[:12]` :216; `len(AXES)=6` :39/:211); `0 -> met · 1 -> unmet` (measure returns `(0 if met else 1)`, :219) `· 2 -> setup (bad git, unreadable manifest)` (`SetupError` :48-49; run() :505-506). Frozen token `C1=met` present (:208).
- **self-test**: accurate — final line matches run-now verbatim; ec=0; 11 arms = 10 fixture arms (:248-318) + `setup_bad_manifest_exit2` (:460-468); prints at :474.
- **pinned values**: accurate — base `66c5518e239eeacd6070be26d78085ef702392cb` byte-exact (`BASE_DEFAULT`, :41; docstring :7-8); "expected leads from fleet MANIFEST.json admitted mori closures" (`MANIFEST_DEFAULT` = fleet-root MANIFEST.json, :42; expectation loader = highest admitted mori closure per axis, docstring :5-6, :93-97).
- **write scope**: accurate — stdout only (:507); "selftest fixtures in a TMPDIR temp dir, removed" (docstring :23-24; `mkdtemp(dir=tmp_root…)` :460; `shutil.rmtree(tmp_root…)` :473).
- **owner `mori`**: accurate.

### Row 4 — `SOURCES digest check (r91 tool, registry r97)` (SKILL.md:1448)
- **name**: accurate — first landing commit `bee9f21e "round-91: … digest-class gate … QUALITY 193 …"`.
- **kind `gate`**: accurate.
- **entry**: accurate — `corpus/SOURCES.md corpus/evidence` matches `<SOURCES.md> <pinned-dir>` argv arity 3 (:262-266); `--selftest` (`argv[1:] == ["--selftest"]`, :260).
- **verdict map**: accurate — per-row `DIGEST <id> ok|mismatch|prefix-only|unpinned recorded=<value> actual=<sha256>` (:13, :463-464) or `DIGEST <id> superseded-by <successor>` (:17, :460); final `DIGEST_CHECK rows=N ok=A mismatch=B superseded=S prefix_only=C unpinned=D` (:21, :466-468); `0 ->` mismatch=0 ∧ prefix_only=0 ∧ unpinned=0, `1 ->` any of them, `2 ->` setup (:23-24; `exit_code` :472-473; setup paths :262-285); QUALITY 193 "(prefix agreement fails the gate)" (:24); the known-limit sentence matches the docstring's supersession clause ("if and only if S<id> classifies mismatch AND the row itself classifies ok … a failing successor supersedes nothing", :26-30) and names the count-c2 hole-guard pairing per contract. Frozen token `DIGEST_CHECK` present (:466).
- **self-test**: accurate — final line matches run-now verbatim; ec=0 (:32-33 docstring).
- **pinned values**: accurate — QUALITY 193 (:24); "supersession only for an `ok` successor" (:26-28).
- **write scope**: accurate — "the CLI writes only to stdout/stderr" (:68-69); selftest fixtures in `tempfile.TemporaryDirectory` (TMPDIR honoured, removed) (:68, :544).
- **owner `mori`**: accurate.

## 5. Predicate-P1 spot-check (evidence above)

(a) auditor `REGISTRY=met` at `--rev e85ed912… --audit-all` ✓; (b) each attributed row's `self-test` cell contains, verbatim, the final line each tool's `--selftest` prints run-now, and all four exit 0 ✓; (c) verdict-map cells contain the frozen tokens `MORI_CGROUP_PRESSURE` (:219), `MORI_DRIFT_RECHECK` (:341), `C1=met` (:208), `DIGEST_CHECK` (:466) ✓.

## 6. Findings and residual risk

1. **Minor (row 2 verdict map)**: the emitted row shape `<id> unresolved as-of=T` (`mori-drift-recheck.py:330`, reachable via unparsable receipt header `:303`) is not in the token enumeration, though the exit leg ("1 -> any unresolved") discloses the state. Cosmetic incompleteness; no predicate, counter, or exit contract touched.
2. **Note (row 1 verdict map)**: "high-guarded" is the r62 docstring's own vocabulary; the landed code only ever exits 0 on `PRESSURE_OK`. The row mirrors the tool's documented contract, so it is not a registry defect.
3. Unrun checks: the frozen counter `.ufo/waves/round-97/count-c1.py` was not re-executed by this seat (landing receipts + auditor run cover the assignment's scoped checks); upstream kernel-source line numbers (psi.c / cgroup-v2.rst) were not re-opened against the v7.2/7.3 pins — only their presence in the docstring was verified.

**VERDICT C1 holds** — all 32 cells accurate (one cosmetic token-list omission, disclosed by the same cell's exit leg), the section is append-only at EOF, every selftest cell matches the tool's run-now final line with exit 0, and the auditor ends `REGISTRY=met` (`unregistered=0`) at the landing revision.
