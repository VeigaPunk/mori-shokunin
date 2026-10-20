# SkillRegistry — round-17 registry rows (C1, C2, misroot, r17 context) and stale-row flags

Scout report for L1 `MoriR17`. Advisory only: I do not edit `SKILL.md`, judge a claim, or
integrate. All detail is here; the final message is the path plus one verdict line.

Snapshot: lane HEAD `24526ea` (`git rev-parse --short HEAD`, exit 0), read at
2026-10-20 ~15:54–16:02 host time. Executor clones were still moving during the read
(sizes/mtimes moved between 15:57 and 16:00), so every clone observation below is a
timestamped snapshot, not a delivered artifact.

Nothing under the fleet root was written. One accidental scratch file is disclosed in §7.

---

## 1. Verdict for L1 (short)

1. Six row actions: rewrite the existing `census` row (C2 findings), and append five rows —
   `seat terminal (r17)` (probe), `r17 seat regressions` (gate), `r17 jj regressions`
   (gate), `misroot sweep (r17)` (probe), `r17 context check` (gate). Exact cells in §3.
2. The `census` row at `SKILL.md:164` is stale today: it pins the r14 tally/SHA
   (`104/104 at 8d22d18`, census `0e41cb83…`). Current census bytes are `f1f8d1b6…` and the
   committed r15 receipt measures `113/113`. The C2 edit invalidates both numbers; the row
   must carry L1's post-C2 measurement, never a predicted tally.
3. The r16 “no hidden flags” sentence (`SKILL.md:169`) is true only in its narrow sense
   (removed bypass flags; unknown args rc2). It must not be extended to the new CLIs as a
   blanket guarantee; the r15/r16 entry cells already omit accepted diagnostic flags
   (`--case`, `--timeout` / `--run-timeout`, `--capture-cap`). New rows list every accepted
   flag, and L1 verifies final argparse after build.
4. One PROTOCOL gap: the C2 gate (`contract.md:91-94`, JjGate dispatch) has **no
   `--selftest`**, while `PROTOCOL.md:386-389` requires every gate to expose one. The row
   below assumes L1 adds it; otherwise the gate is registered non-conformant, not green.
5. The two existing round-17 context-check receipts are **r16-checker results**
   (`clauses_checked: 8`); they do not establish the r17 12-clause result.
6. The census selftest hardcodes `/tmp/mori-census-selftest.XXXXXX` and ignores `TMPDIR`,
   which collides with the wave’s `/tmp` prohibition; the row discloses the path (§5 S2).

---

## 2. Observed facts (path:line, command, exit)

### F1 — Registry home and column format
- `SKILL.md:155` “## Gates”; table header `SKILL.md:162`:
  `| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |`.
- Current rows: census `:164`, drift pin `:165`, silence oracle `:166`, r13 `:167`,
  r14 `:168`, r15 `:169`, r16 regressions `:170`, r16 context check `:171`,
  journal window `:172`.
- `PROTOCOL.md:397-406` (“Registry”): row fields are name, `gate|probe`, entry command,
  verdict map (code → class), self-test command and spelling, pinned-value path, write
  scope, owner. `PROTOCOL.md:386-389` requires a self-invocation mode for every gate.
- `PROTOCOL.md:380-383`: `0` clean, `1` failed, every other exit declared and mapped.

### F2 — The r16 “no hidden flags” sentence and what it actually covers
- Exact text at `SKILL.md:169`: “The r15 CLI has no hidden flags: `--selftest-child` and
  `--no-frozen-control` were removed from it … any unknown argument is refused by argparse
  with rc2, and `--selftest` refuses `--output` and `--pin-fixtures` with rc2.”
- Observed in source, `tools/mori-round15-regressions.py:2310-2319`: accepted flags are
  `--census`, `--fixtures`, `--output`, `--frozen`, `--expected`, `--pin-fixtures`,
  `--case`, `--timeout`, `--selftest`. No `--selftest-child`, no `--no-frozen-control`.
  The refusal is real at `:2323-2326` (`if args.selftest: if args.output or
  args.pin_fixtures: return 2`).
- The r15 entry cell (`SKILL.md:169`) does **not** list `--case` or `--timeout`; the r16
  entry cell (`SKILL.md:170`) does not list `--case`, `--run-timeout`, `--capture-cap`
  (accepted at `tools/mori-round16-regressions.py:1738-1743`). The sentence is therefore
  true about *bypass* flags and unknown-argument refusal, not about “every accepted flag is
  in the row”.
- r16 context check is clean: `tools/mori-round16-context-check.py:523-525` accepts only
  `--spec` and `--selftest`, both in its entry cell.
- New-CLI snapshot at 15:58/16:00: `MisrootSweep/tools/mori-misroot-sweep.py` accepts
  exactly `--fleet-root`, `--lane`, `--round`, `--legacy-pathspec`, `--selftest`;
  `ContextCheck17/tools/mori-round17-context-check.py` accepts exactly `--spec`,
  `--selftest`. All are in the proposed entry cells. SeatTool/SeatGate/JjGate had **no
  tool file yet** at the snapshot (`ls` of the six clone `tools/` directories, exit 0 for
  four files; no `mori-seat-terminal.py`, no `mori-round17-seat-regressions.py`, no
  `mori-round17-jj-regressions.py`).

### F3 — C1 interface (contract, verbatim anchors)
- Tool: `contract.md:24-67`. CLI `--sessions-dir`, repeatable `--prefix`, `--max-tail-bytes`
  (262144), `--max-files` (20000); recursive `*.jsonl`, no symlinks; only `type=="message"`
  records parsed; classes and order at `:36-53`; per-seat fields at `:54-58`; JSON schema
  `mori-seat-terminal-v1` at `:57-60`; exit 0/1/2 and finding ids at `:61-64`.
- Gate: `contract.md:75-78` — `--tool PATH --fixtures DIR --output DIR`, one real
  subprocess per case, `run-manifest.json` with `match|mismatch|capability_absent` and
  input SHA-256 before/after, rc0 only if every case matches, missing tool path =
  `capability_absent` for every case and rc1. The dispatch text for `SeatGate` adds
  “exit … 2 on setup”, the output-under-`tools/|.git|.jj|corpus` guard, and selftest arms
  green/capability_absent/mismatch/fixture drift/output guard
  (`.ufo/waves/round-17/wave1-spec.json`, item `SeatGate`).
- `SeatTool` dispatch adds `>=16` selftest arms and the `credential_pin` trap (same spec
  file, item `SeatTool`). `SeatFixtures` dispatch requires `>=40` fixture cases plus
  `expected.json` (item `SeatFixtures`).

### F4 — C2 interface (contract, verbatim anchors)
- Branch resolution at `contract.md:81-82`: `symbolic-ref -q HEAD` →
  `refs/remotes/origin/HEAD` → unique of `refs/heads/master` / `refs/heads/main`.
- `refs/heads/<branch>` replaces `HEAD` in row-6 closure and row-9 authorship
  (`contract.md:83-84`; current `HEAD` sites at `tools/mori-census.sh:2100` `cat-file -e
  "HEAD:$rpath"` and `:2197` `rev-parse --verify -q HEAD`, `:2200` `log --since`).
- `HEAD_BRANCH_MISMATCH` and `LANE_AUTHOR_MISMATCH`, both severity drift, at
  `contract.md:85-89`; grading semantics otherwise unchanged.
- Gate at `contract.md:91-94`: `--census PATH --output DIR`; real colocated jj sandboxes in
  its own temp tree; counts failed case assertions; run against the entering census
  (`git show 24526ea:tools/mori-census.sh`) and the delivered census. The JjGate dispatch
  adds `[--scratch DIR]`, real `git` + `~/.local/bin/jj`, `HOME`/`XDG_CONFIG_HOME`/
  `JJ_CONFIG`/`GIT_CONFIG_GLOBAL` redirection, census stub/override environment, and
  `>=8` cases (helper-shaped control; HEAD ahead; ambient author + lane committer; plain
  git control; detached at tip; report off-branch). No `--selftest` in either text.
- Snapshot in `CensusJj` clone at 15:57–15:59: branch resolution present
  (`tools/mori-census.sh:2100-2135` in the clone), row-6 closure reads
  `refs/heads/$branch` (`:2194`, `:2197`), head-branch probe with explicit
  `head_branch_probe_unavailable=...` for probe errors (`:2140-2178`), row-9 scan now reads
  `%an <%ae>` and `%cn <%ce>` (`:2323-2326`). **No `emit_finding HEAD_BRANCH_MISMATCH` and
  no `emit_finding LANE_AUTHOR_MISMATCH` existed in the snapshot** (grep over the clone,
  zero emit lines; only comments). Build was still in flight; do not register the findings
  as implemented from this snapshot.
- `jj` exists at `/home/vgpnk/.local/bin/jj` (32,107,192 bytes, 2026-10-03; `ls`, exit 0);
  `git` is `/usr/bin/git`.

### F5 — Misroot sweep interface and the r16 blind spot
- R16 evidence `command` (.ufo/waves/round-16/evidence/misroot-sweep.json):
  `git -C /home/vgpnk/Projects/shokunin status --porcelain -- .ufo/waves .ufo/reports` —
  a pathspec that cannot see a file at the fleet root. The archived r16-shaped file is
  `.ufo/waves/hyaku/misroots/MoriR16.Lesson` (847 bytes, 2026-10-20 05:52; first line is a
  BootContinuity disclosure; content not reproduced).
- MisrootSweep dispatch (wave1-spec item `MisrootSweep`): `--fleet-root R --lane ID
  --round N [--legacy-pathspec P ...]`; `git status --porcelain=v1 -z
  --untracked-files=all` with no pathspec by default; ≤64 KiB of each untracked regular
  file; candidate when the bytes name the lane (case-insensitive) and the round
  (`R17`/`round-17`/`r17`); JSON out; rc0/1/2; never moves or deletes.
- Snapshot tool (15:58, 26,014 bytes) implements exactly those five flags, schema
  `mori-misroot-sweep-v1`, findings `MORI_MISROOT_CLEAN`/`_CANDIDATE`/`_SETUP` at
  `:44-46`, `GIT_OPTIONAL_LOCKS=0` at `:57`, status argv at `:61-66`, read cap 64 KiB,
  selftest arms plant the r16-shaped root file and prove no-pathspec finds it while
  `--legacy-pathspec` misses it (`:595-628`). A failed selftest arm reports
  `MORI_MISROOT_SELFTEST_FAIL` with rc1.

### F6 — R17 context checker interface
- `ContextCheck17` dispatch (wave1-spec item): start from
  `tools/mori-round16-context-check.py` (same CLI, finding ids, rc contract, subprocess
  selftest); add `no_fleet_root_writes`, `no_background_jobs`, `no_vcs_mutation`,
  `transcript_fields_only`; keep all r16 clauses.
- r16 tool: `_CLAUSES` length **8** (AST parse of
  `tools/mori-round16-context-check.py`); CLI `--spec`/`--selftest` only (`:523-525`);
  finding ids `CONTEXT_OK`/`CONTEXT_MISSING`/`CONTEXT_SETUP` (`:58-62`).
- r17 clone at 16:00 (28,920 bytes): `_CLAUSES` length **12**, ids in order
  `no_broadcast_exact_id`, `lane_report_resolution`, `no_verification_permission`,
  `pacman_pause`, `credential_prohibition`, `write_scope`, `no_live_journal_queries`,
  `no_tmp_probe_outputs`, `no_fleet_root_writes`, `no_background_jobs`, `no_vcs_mutation`,
  `transcript_fields_only` (AST parse); CLI `--spec`/`--selftest` only.
- Existing receipts `.ufo/waves/round-17/evidence/context-check-wave1.json`
  (`CONTEXT_OK`, `clauses_checked: 8`) and `…-original.json` (`CONTEXT_MISSING`, missing
  `no_tmp_probe_outputs`, `clauses_checked: 8`) are r16-checker runs;
  `spec_sha256=6969eb19…` matches `sha256sum .ufo/waves/round-17/wave1-spec.json`. No
  12-clause receipt existed at the snapshot.

### F7 — Census staleness measurements
- `sha256sum tools/mori-census.sh` → `f1f8d1b62bb617bbcc4664057ab807d3fed8c275b7aabbdf7b373323c5501ff7`
  (exit 0).
- `git log --oneline -8 -- tools/mori-census.sh` top: `26f6589 round-15: retain valid
  positive alarms beside unavailable class totals`, then `8d22d18 round-14…` (exit 0).
- `.ufo/waves/round-14/evidence/census-selftest.json`: `exit 0`,
  `sha256["tools/mori-census.sh"]=0e41cb83fce2…`, stdout summary
  `MORI_CENSUS_SELFTEST: PASS (104 cases, 104 passed, 0 failed)` — matches
  `SKILL.md:164` for r14.
- `.ufo/waves/round-15/evidence/census-selftest.json`: `exit 0`,
  `sha256_start["tools/mori-census.sh"]=f1f8d1b62bb6…`, `inputs_changed: false`, summary
  `MORI_CENSUS_SELFTEST: PASS (113 cases, 113 passed, 0 failed)`. The registry still says
  104/104 at `0e41cb83…`, i.e. it is one census revision behind.
- `git show 5601d12:tools/mori-round14-regressions.py | sha256sum` → `c39e5a73…`; current
  `tools/mori-round14-regressions.py` → `533218a5…` (changed by `26f6589`). The r14 row’s
  “at 5601d12, harness SHA `c39e5a73…`” is a correctly anchored historical value, not a
  stale current-identity claim.
- Census selftest path: `tools/mori-census.sh:2768`
  `MORI_SELFTEST_WORK=$(mktemp -d /tmp/mori-census-selftest.XXXXXX)`; `grep -n TMPDIR
  tools/mori-census.sh` returned no match (exit 1). Clone at 15:59 has the same hardcoded
  path at `:2916`.

---

## 3. Proposed rows — exact, existing 8-column format

Placement: replace the one line at `SKILL.md:164` with Row C; append Rows A, B, D, E, F
after `SKILL.md:172` (journal window) in that order. Owner is `mori` on every row.

```markdown
| seat terminal (r17) | probe | `python3 tools/mori-seat-terminal.py --sessions-dir <DIR> [--prefix <P> ...] [--max-tail-bytes <N>] [--max-files <N>]` (`--selftest`; `--help` states: last observed state, seats not incidents, prefixes not authenticated membership) | probe, not a gate: rc0 `MORI_SEAT_TERMINAL_OK` · rc1 `MORI_SEAT_TERMINAL_DEAD` (≥1 seat in `dead_rate_limit`/`dead_quota`/`dead_error_other`; an observation, not a severity or DRIFT) · rc2 `MORI_SEAT_TERMINAL_SETUP` (usage, unreadable directory, `too-many-files` above `--max-files`); detection only — never edits, resumes or re-routes a session | `python3 tools/mori-seat-terminal.py --selftest` — ≥16 hermetic arms as real subprocesses over synthetic transcripts under TMPDIR, asserting rc, finding and per-seat class (error-then-stop completed, 429/type=1302, resource_exhausted, quota, other error, aborted, toolUse, toolResult, empty file, malformed line, tail cut, credential_pin trap, symlink skip, --prefix, --max-files); tally recorded at L1 integration, not predicted here | none; class vocabulary, tail bound (`--max-tail-bytes` default 262144) and file cap (`--max-files` default 20000) are in-script; the sessions directory is the caller's path | stdout JSON only (`mori-seat-terminal-v1`: `totals`, `by_prefix`, `by_provider_model`, `seats`); never writes the sessions tree; never emits errorMessage text, content or usage; selftest synthetic tree under TMPDIR | mori |
| r17 seat regressions | gate | `python3 tools/mori-round17-seat-regressions.py --tool <PATH> --fixtures <DIR> --output <DIR>` | 0 every case matches · 1 ≥1 `mismatch` or `capability_absent` (a missing `--tool` path yields `capability_absent` for every case; capability, not a production bug) · 2 could-not-evaluate (usage/setup, unreadable or schema-invalid expected table, `--output` equal to or covering lane `tools/`, `.git`, `.jj` or `corpus/`, fixture input SHA-256 changed during the run) | `python3 tools/mori-round17-seat-regressions.py --selftest` — isolated fake tool and fixtures under TMPDIR; arms green, `capability_absent`, mismatch, fixture-hash drift and output guard; tally recorded at L1 integration, not predicted here | `.ufo/waves/round-17/fixtures/seat/expected.json` commits per-case `rc`/`finding`/`totals`/`seats`; `run-manifest.json` records per-case result plus fixture SHA-256 before and after; no in-script digest pin of `--tool` (the caller names it) | `<dir>` evidence only (`run-manifest.json`, per-run stdout/stderr digests); fixtures read-only; selftest temp tree; refuses an `--output` equal to or covering the lane `tools/`, `.git`, `.jj` or `corpus/` | mori |
| census | gate | `bash tools/mori-census.sh` (`MORI_SHOKUNIN_ROOT=<fleet root>` outside the fleet tree) | 0 clean · 1 failed (DRIFT; now includes the drift findings `HEAD_BRANCH_MISMATCH` and `LANE_AUTHOR_MISMATCH`) · 2 could-not-evaluate | `--selftest` (last measured 113/113 over census `f1f8d1b6…` at r15, `.ufo/waves/round-15/evidence/census-selftest.json`; the r14 104/104 at `0e41cb83…` is superseded; the r17 C2 edit requires L1 to re-measure and record the new tally here, never a predicted one; new stub-git cases cover HEAD ahead of branch, ambient author with lane committer, detached HEAD at branch tip (no finding) and a plain attached git lane (no finding, unchanged verdict)) | expected ids/exits in `run_selftest()`, now including the two r17 findings; `head_branch_probe_unavailable=…` is recorded as an observation and never promoted to a finding | none live; selftest builds its fixture tree under `/tmp/mori-census-selftest.XXXXXX` (hardcoded; ignores `TMPDIR`) | mori |
| r17 jj regressions | gate | `python3 tools/mori-round17-jj-regressions.py --census <PATH> --output <DIR> [--scratch <DIR>]` (`--selftest`) | 0 every case assertion passes for the census under test · 1 ≥1 failed case assertion · 2 could-not-evaluate (usage/setup, missing real `git` or `~/.local/bin/jj`, sandbox build failure, an unstubbable live surface, output/scratch guard) | `python3 tools/mori-round17-jj-regressions.py --selftest` — the in-script sandbox case table (≥8 cases: helper-shaped control, HEAD ahead of branch, ambient author with lane committer, plain attached git control, detached at tip control, report committed only off-branch) run as isolated real-git/jj subprocesses; tally recorded at L1 integration, not predicted here | case table in-script (≥8); `run-manifest.json` records per-case assertions, failed count and census SHA-256; the round's evidence names both census digests (entering `git show 24526ea:tools/mori-census.sh` and delivered); no in-script digest pin of `--census` (the caller names it) | `--output` evidence tree and `--scratch` sandbox only; real `git` and `~/.local/bin/jj` with `HOME`, `XDG_CONFIG_HOME`, `JJ_CONFIG` and `GIT_CONFIG_GLOBAL` redirected into the sandbox; census run with its own stub/override environment (no live journal, systemd, tmux or cgroup query); never the lane, the fleet root or the real `~/.config/jj` | mori |
| misroot sweep (r17) | probe | `python3 tools/mori-misroot-sweep.py --fleet-root <R> --lane <ID> --round <N> [--legacy-pathspec <P> ...]` (`--selftest`; no pathspec by default) | probe, not a gate: rc0 `MORI_MISROOT_CLEAN` · rc1 `MORI_MISROOT_CANDIDATE` (≥1 untracked file naming the lane and round; an observation for L1, not severity or DRIFT) · rc2 `MORI_MISROOT_SETUP` (usage, unreadable/unowned git root, status failure); never moves, edits or deletes | `python3 tools/mori-misroot-sweep.py --selftest` — sandbox git repo under TMPDIR with a planted r16-shaped root file, a sibling naming another lane, a tracked file and an ignored file; asserts the no-pathspec sweep finds the planted file while `--legacy-pathspec .ufo/waves .ufo/reports` misses it (the r16 blind spot shown able to fail); a failed arm reports `MORI_MISROOT_SELFTEST_FAIL` rc1; tally recorded at L1 integration | none; lane id and round are caller-supplied; reads `git status --porcelain=v1 -z --untracked-files=all` (with `GIT_OPTIONAL_LOCKS=0`) and ≤64 KiB of each untracked regular file | stdout JSON only (`mori-misroot-sweep-v1`); never writes the fleet root; selftest sandbox under TMPDIR | mori |
| r17 context check | gate | `python3 tools/mori-round17-context-check.py --spec <PATH>` (`--selftest`; same CLI as r16) | 0 `CONTEXT_OK` · 1 `CONTEXT_MISSING` · 2 `CONTEXT_SETUP` (usage, unreadable or invalid JSON); twelve required clauses = the eight r16 clauses plus `no_fleet_root_writes`, `no_background_jobs`, `no_vcs_mutation` and `transcript_fields_only`; static text validation is not runtime prevention (`claims_runtime_prevention: false`) | `python3 tools/mori-round17-context-check.py --selftest` — positive, one negative per clause, absent-context and malformed-spec arms as isolated subprocesses; observed result recorded by L1, not predicted | in-script clause patterns; `.ufo/waves/round-17/wave1-spec.json` is the first measured spec (the existing 8-clause receipts do not satisfy the 12-clause checker) | none live; reads only `--spec`; selftest temp tree under TMPDIR | mori |
```

### Kind rationale (probe vs gate)

`seat terminal (r17)` and `misroot sweep (r17)` are proposed as **probes**: neither compares
against an expected-value baseline persisted in the repo, and `contract.md:66-67` frames C1
as “detection and report only”. Their rc1 is a detection observation, phrased the way
`SKILL.md:172` phrases the journal probe (“probe, not a gate … no severity, no DRIFT”).
`PROTOCOL.md:377-379` defines a gate by comparison against persisted expected values; a tool
that merely classifies observed state does not meet it even though it can exit 1. If L1
prefers to read rc1 `DEAD`/`CANDIDATE` as a failed class, both rows become `gate` — but then
the row would have to name an expected-value source, and there is none; the probe reading is
the honest one. The regression harnesses, census and context checker are gates: each
compares against in-script expected ids/shares or a committed expected table.

### Proposed r17 prose paragraph (insert after the r16 paragraph, i.e. after `SKILL.md:242`)

> **Regression gates, probe and conformance checks (r17).** `tools/mori-seat-terminal.py`
> (registered above as `seat terminal (r17)`) is a detection-only probe over OMP seat
> transcripts: it reads at most the last `--max-tail-bytes` of each `*.jsonl`, parses only
> `type == "message"` records, and emits one JSON document with the last observed terminal
> class per seat, per prefix and per provider/model; it never emits `errorMessage` text,
> content or usage, and rc1 is one observation per seat, not an incident count, a resume
> signal or proof that a session cannot recover. `tools/mori-round17-seat-regressions.py`
> (registered above as `r17 seat regressions`) runs the tool once per committed fixture
> case; `capability_absent` is capability, not a production bug, and a green fixture run
> does not claim live seats are healthy. C2 changes no grading semantics: the census
> resolves the lane branch like `scripts/hyaku/jj-lane.sh detect_branch`
> (`symbolic-ref -q HEAD` → `refs/remotes/origin/HEAD` → unique of
> `refs/heads/master`/`refs/heads/main`) and asks the row-6 closure and row-9 authorship
> probes of `refs/heads/<branch>` instead of `HEAD`; `HEAD_BRANCH_MISMATCH` and
> `LANE_AUTHOR_MISMATCH` are drift findings, an unresolvable HEAD or branch tip is recorded
> as `head_branch_probe_unavailable` and is never promoted to a finding, and a detached
> HEAD at the branch tip or a plain attached git lane yields no finding and an unchanged
> verdict. `tools/mori-round17-jj-regressions.py` (registered above as `r17 jj
> regressions`) builds real colocated jj sandboxes under its own `--scratch` with
> `HOME`/`XDG_CONFIG_HOME`/`JJ_CONFIG`/`GIT_CONFIG_GLOBAL` redirected, runs the census with
> its own stub/override environment (no live journal, systemd, tmux or cgroup query), and
> counts failed case assertions; the entering census (`git show 24526ea:tools/mori-census.sh`)
> is the red control and the delivered census is the green subject.
> `tools/mori-misroot-sweep.py` (registered above as `misroot sweep (r17)`) repeats the r16
> status query with no pathspec, because the r16 evidence
> (`.ufo/waves/round-16/evidence/misroot-sweep.json`) restricted `git status` to
> `.ufo/waves .ufo/reports` and was blind to a file at the fleet root; it reads at most the
> first 64 KiB of each untracked regular file and never moves, edits or deletes anything.
> `tools/mori-round17-context-check.py` (registered above as `r17 context check`) keeps the
> eight r16 clauses and adds `no_fleet_root_writes`, `no_background_jobs`, `no_vcs_mutation`
> and `transcript_fields_only`; it is a static text check and `CONTEXT_OK` is not runtime
> prevention. The misroot sweep and the context check are unclaimed conformance work, not
> C1/C2 evidence. No selftest tally is predicted here; L1 measures the delivered revisions
> once after integration.

---

## 4. Stale / imprecise rows — flags for L1

### S1 — `census` row (`SKILL.md:164`) is stale (must be rewritten)
- Row says `104/104 at 8d22d18, census SHA 0e41cb83…` and cites the r14 receipt. That was
  accurate for r14. At `24526ea`, `tools/mori-census.sh` hashes `f1f8d1b6…` and the
  committed r15 receipt measures `113/113`, exit 0, `inputs_changed: false`
  (`.ufo/waves/round-15/evidence/census-selftest.json`). The r15 commit `26f6589` is the
  change event (`git log -- tools/mori-census.sh`).
- C2 edits the census again, so the corrected row must carry L1’s **post-C2 measured**
  tally and digest. Do not copy 104/104 or 113/113 as if current; do not predict a new
  number. The proposed Row C above says exactly that.

### S2 — `census` write scope hides a hardcoded `/tmp` selftest path
- `tools/mori-census.sh:2768` uses `mktemp -d /tmp/mori-census-selftest.XXXXXX`; no
  `TMPDIR` reference exists anywhere in the file (grep exit 1). The clone has the same path
  at `:2916`.
- The wave context (`wave1-context.txt:7`) forbids writing probe outputs, downloads or
  scratch to `/tmp` for every seat. The CensusJj dispatch instructs the executor to run
  `bash tools/mori-census.sh --selftest` “with TMPDIR set” — that instruction cannot
  redirect this selftest. The row should disclose the path (as proposed) or L1 should
  explicitly authorize the gate-owned temp tree. Making the census honor
  `${TMPDIR:-/tmp}` is a second census edit and requires another re-measure; I do not
  recommend smuggling it into C2.

### S3 — `drift pin` row (`SKILL.md:165`) carries red debt, not a stale claim
- The pinned baseline is still `corpus/evidence/baseline-r10-20261015T2231Z.json`; r16
  recorded the pin red as carried debt C15-5 (`corpus/lessons/round-16.md:37`). No re-pin
  is proposed. The r17 report must not let a green census or the C2 fix imply freshness.

### S4 — “no hidden flags” (`SKILL.md:169`) is narrower than it reads
- True claims: `--selftest-child` and `--no-frozen-control` are gone from the r15 CLI, and
  unknown arguments fail via argparse rc2; `--selftest` refuses `--output`/`--pin-fixtures`
  (`tools/mori-round15-regressions.py:2323-2326`).
- Overbroad reading: the r15 CLI accepts `--case` and `--timeout`
  (`:2316-2318`) and the r16 CLI accepts `--case`, `--run-timeout`, `--capture-cap`
  (`tools/mori-round16-regressions.py:1738-1743`), none of which appear in their registry
  entry cells. Recommendation: either list every accepted flag in each entry (the new rows
  do), or reword to “no hidden control-bypass flags”. Do not extend the r15 sentence to the
  r17 tools as a blanket guarantee.
- New-CLI check performed at snapshot: MisrootSweep (5 flags) and ContextCheck17 (2 flags)
  are fully listed in §3. SeatTool, SeatGate and JjGate were not built yet; L1 must verify
  their final argparse before committing the rows, and must add any diagnostic flag they
  introduce (`--case`, `--timeout`, …) to the entry cell.

### S5 — `r16 context check` row (`SKILL.md:171`) is accurate; do not edit it
- `_CLAUSES` is length 8 in `tools/mori-round16-context-check.py` (AST parse); the row’s
  “eight required clauses” is correct. The r17 checker adds four and gets its own row; do
  not rewrite the r16 row to say 12.
- The two round-17 receipts
  (`.ufo/waves/round-17/evidence/context-check-wave1.json` and `…-original.json`) both say
  `clauses_checked: 8`; they are r16-checker evidence and cannot be cited for the r17 row.

### S6 — `r14 regressions` harness SHA is a historical anchor (`SKILL.md:168`)
- `c39e5a73…` is the byte identity at `5601d12` (`git show 5601d12:tools/mori-round14-regressions.py
  | sha256sum`); the current file hashes `533218a5…` after `26f6589`. The row’s “at
  5601d12, harness SHA …” wording is accurate; keep the anchor explicit and do not present
  the SHA as current. The frozen pins `0e41cb83…` (r15 row) and `39abda0a…` (r14 row) are
  likewise historical frozen inputs and are not affected by C2.

### S7 — no other row-level staleness found
- `r13`, `r14` (other than S6), `r15`, `r16 regressions` and `journal window` cells were
  read against the current tools; their anchors name commits or frozen paths explicitly.
  The r15 “no hidden flags” sentence is S4; the drift debt is S3.

---

## 5. Unresolved gaps and decisions for L1

- **G1 — JjGate has no `--selftest`.** `contract.md:91-94` and the JjGate dispatch describe
  only `--census/--output/--scratch` plus the case table; `PROTOCOL.md:386-389` requires
  every gate to expose a self-invocation mode with committed expected values. The proposed
  Row D assumes L1 requires the executor to add `--selftest` over the same sandboxed case
  table. If the delivered gate lacks it, the honest registry entry is a gate with
  “self-test: none — PROTOCOL non-conformance”, and L1 should route it back rather than
  register an un-selftested gate as green.
- **G2 — JjGate verdict map is not specified.** The contract says only “counts failed case
  assertions”. Row D’s `0/1/2` map is `[INFERENCE]` from the r13/r15 gate pattern
  (`0` all pass, `1` ≥1 failed assertion, `2` could-not-evaluate). L1 should have the
  executor declare the `2` conditions in `--help`; the registry row must match the CLI.
- **G3 — C1 gate code for a mid-run fixture hash change.** The contract requires recording
  SHA-256 before/after but assigns no code. Row B proposes `2` (could-not-evaluate,
  “moving inputs”), consistent with `SKILL.md:170`. `[INFERENCE]`
- **G4 — `--scratch` is dispatch-only.** It appears in the JjGate dispatch, not in
  `contract.md:91`. Row D includes it; if the final CLI names it differently, fix the row,
  not the contract.
- **G5 — probe kind for seat terminal and misroot sweep.** See §3 kind rationale. If L1
  disagrees, the rows flip to `gate` with the same entry/verdict text; the expected-value
  source is the unresolved part.
- **G6 — build state is fluid.** At snapshot, `SeatTool/`, `SeatGate/` and `JjGate/` had no
  tool files; `CensusJj` had branch resolution and `refs/heads` closure but no emit line
  for either new finding; `ContextCheck17` had 12 clauses; `MisrootSweep` had the five
  flags. Clone sizes changed between reads (e.g. census 228,129 bytes at 15:57 → 239,777
  at 15:59). Every row above must be checked against the delivered bytes before L1 writes
  `SKILL.md`. No selftest was executed by this seat.

---

## 6. Exact commands used (read-only; no selftest, no journalctl, no pacman)

All run from `/home/vgpnk/Projects/shokunin/mori-shokunin` unless noted; all exit 0 unless
marked.

- `read .ufo/waves/round-17/contract.md`; `read SKILL.md:140-200`, `:155-172:raw`,
  `:173-245`; `read .ufo/waves/round-17/wave1-context.txt`.
- `git rev-parse --short HEAD` → `24526ea`.
- `git log --oneline -8 -- tools/mori-census.sh`; `git log --oneline -3 --
  tools/mori-round14-regressions.py tools/mori-round15-regressions.py
  tools/mori-round16-regressions.py tools/mori-round16-context-check.py
  tools/mori-journal-window.py`.
- `git show 5601d12:tools/mori-round14-regressions.py | sha256sum` → `c39e5a73…`.
- `sha256sum tools/mori-census.sh tools/mori-round1*-regressions.py
  tools/mori-round16-context-check.py tools/mori-journal-window.py` → census
  `f1f8d1b6…`, r14 `533218a5…`.
- `python3 -c` JSON tallies over `.ufo/waves/round-14/evidence/census-selftest.json` and
  `.ufo/waves/round-15/evidence/census-selftest.json` → 104/104, 113/113; SHA keys as
  quoted in §2 F7.
- `grep -n add_argument` over the four Python gates/probe → flags in §2 F2.
- `python3 -c` AST `_CLAUSES` count: r16 → 8; r17 clone → 12, with ids as quoted.
- `grep -n 'HEAD\|ps_report_closed\|rev-parse --verify\|--since' tools/mori-census.sh`
  → `:2100`, `:2197`, `:2200`.
- `grep -n 'mktemp -d\|TMPDIR' tools/mori-census.sh` and the clone → hardcoded `/tmp` at
  `:2768` / clone `:2916`; TMPDIR grep exit 1 (no match).
- `python3 .ufo/waves/round-17/...`? No — no tool executed. Clone inspection only via
  `grep`/`sed`/`python3` AST over files.
- `ls -la ~/.local/bin/jj`; `command -v jj git` → `/home/vgpnk/.local/bin/jj`,
  `/usr/bin/git`.
- `ls -la /home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/misroots/` → `MoriR16.Lesson`
  847 bytes.
- `cat .ufo/waves/round-17/evidence/context-check-wave1.json` and `…-original.json` →
  `clauses_checked: 8`, spec sha `6969eb19…`.
- `sha256sum .ufo/waves/round-17/wave1-spec.json` → `6969eb19…` (matches the receipt).

No installs were needed; tooling directive unused. No VCS mutation, no background jobs, no
host services, no `/tmp` writes.

---

## 7. Discipline disclosure

One self-correction: at the start of the read I extracted a few dispatch prompts with a
shell redirect into `.ufo/waves/round-17/build/.tmp_prompts_skillregistry.txt` (10,134
bytes). That was outside my write scope (report file only). I read it once and removed it
immediately with `rm -f` in the same directory; the directory listing after removal shows
no such file. Nothing was written to the fleet root, no clone, `MANIFEST.json`,
`.ufo/state`, script or sibling lane was touched, and `SKILL.md` was not edited.

## 8. Confidence

- Stale census tally/SHA, r16 clause count, hardcoded `/tmp`, C1/C2 interface text, and the
  JjGate `--selftest` gap: **high** (direct file/git evidence, quoted lines).
- Proposed verdict maps for the JjGate (rc2) and C1 gate (mid-run drift): **medium**
  (`[INFERENCE]` from lane precedent; contract silent).
- Probe-vs-gate kind for seat terminal and misroot sweep: **medium** (contract’s
  “detection only” plus `PROTOCOL.md:377-379` definition; L1 owns the final call).
- Clone-snapshot implementation details (12 clauses, five misroot flags, no finding emit
  yet in the census clone): **snapshot-only, not final**.
