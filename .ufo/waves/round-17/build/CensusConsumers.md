# CensusConsumers — who reads mori census output and finding ids (round 17, C2 blast radius)

Axes: correctness (consumer map) · operability (exact-count and stub contracts) · calibration (fixture honesty).
Read-only seat, scout. `[OBS]` = observed this round · `[INF]` = inference. No edits, no VCS, no test runs.

## Verdict

**Nothing outside the mori lane parses census output or finding ids.** The fleet's only
programmatic census consumer is `scripts/sources-census.sh` (Sources & frontier registry), a
different tool; `scripts/` contains exactly one `mori` token (a lane-roster name), `templates/`
contains none. The real consumer set is five in-lane gates plus the census's own selftest, and all
of them parse finding lines structurally (`^FINDING (\w+) severity=(\w+) obs=…`), so **new ids
`HEAD_BRANCH_MISMATCH` / `LANE_AUTHOR_MISMATCH` break no parser by their name**. Three exact-count
/ consistency assertions are the blast radius, and two fixture-stub facts decide whether the new
probes are exercised at all:

1. `severity drift` in C2 is not a census severity. The emitter accepts `info|warn|crit` and only
   `warn|crit` increments `drift=` and flips the roll (`tools/mori-census.sh:405-416`). A literal
   `severity=drift` line is counted in `findings=` but never rolls, and the loudest consumer-side
   check (`verdict_grade`, CLEAN requires `drift=0`) **passes** it silently. Emit `warn`.
2. Every gate fixture family stubs `git`, and none of them knows `symbolic-ref`/`merge-base`:
   r13 and r14 stubs `exit 2` for unknown verbs (`tools/mori-round13-regressions.py:993-1014`,
   `tools/mori-round14-regressions.py:789-810`; r15 reuses r14, `tools/mori-round15-regressions.py:978-985`),
   while the census's own selftest stub answers absent verb files with **rc 0 and empty output**
   (`tools/mori-census.sh:2790-2791`, dispatch `:2839-2862`). Branch resolution must therefore
   fail *soft*: an empty or non-zero branch name must fall back to today's `HEAD` behaviour and
   must emit neither new finding. Otherwise r14's `drift` equality and r15's
   `want_drift = want_oom + want_signal` go red on fixtures that hold no git repo at all.

New tool `tools/mori-seat-terminal.py` (C1): no consumer exists to break. Its only integration
obligations are a `SKILL.md` gate-registry row and a self-contained r17 gate; no fleet or sibling
script enumerates lane tools or gate rows.

## 1. Method `[OBS]`

Read-only; every path absolute. Commands and result:

| command | result |
|---|---|
| `grep -rn 'mori\|MORI_' /home/vgpnk/Projects/shokunin/scripts/` | one line: `scripts/hyaku/pool.txt:9:mori` |
| `grep -rn 'mori\|MORI_' /home/vgpnk/Projects/shokunin/templates/` | zero matching lines |
| `grep -rn 'census\|mori\|findings' scripts/hyaku/jj-lane.sh` | zero matching lines |
| `grep -rn 'mori-census\|MORI_CENSUS\|mori-shokunin/tools' --include='*.sh' --include='*.py' --include='*.mjs' --include='*.js' --include='*.ts' .` (excluding `./mori-shokunin/`, `./.tower/`) | only `chousa-shokunin/tools/research-gate.sh:180,2537,2784` (comment lineage) |
| `grep -rn 'mori-shokunin' <same filters>` | `kama-shokunin/.ufo/waves/round-16/falsify/make_spec.py:126` (advice prompt) + the same chousa comments |
| `grep -rn 'OOM_KILL_JOURNAL\|LANE_SILENT\|WAVE_UNSETTLED_AGE\|WATCHDOG_ABSENT\|CGROUP_OOM_KILL\|KILL_SIGNAL_JOURNAL\|ROSTER_SET_MISMATCH' .` (excluding lane, `.tower`, `*.jsonl`) | fleet reports/prose, `MANIFEST.json`, kama advice — no executable reader |
| `git -C mori-shokunin symbolic-ref -q HEAD` | `refs/heads/master`, rc 0 |
| `git -C mori-shokunin rev-parse --short HEAD` / `refs/heads/master` | `24526ea` / `24526ea` |
| `git -C mori-shokunin merge-base --is-ancestor HEAD refs/heads/master` | rc 0 |
| `git -C mori-shokunin rev-parse --verify -q refs/remotes/origin/HEAD` | `24526ea…28cb`, rc 0 |
| `find ~/.omp/agent/sessions -type f -name '*.jsonl' \| wc -l` / `du -sh` | 5816 / 5.4 G (metadata only) |
| `bash tools/mori-census.sh --selftest` | **not run** — not permitted for this seat |

## 2. External consumers — none parse mori output

### 2.1 `scripts/` (fleet)

- `scripts/hyaku/pool.txt:9:mori` is a lane-roster token, not a reader.
- `scripts/shokunin-watchdog.sh:319-345` `sources_gate()` invokes
  `"$SHOKUNIN_ROOT/scripts/sources-census.sh" validate --root … <lane>` (`:324`) and grades its
  rc map (`:334-338`). That is the **Sources & frontier** census, not `mori-census.sh`; its finding
  ids are `E01..E11/W01..W03` (`scripts/sources-census.sh:24,126-144`). Its `rc1` blocks and `rc2`
  only warns — a mori verdict never reaches it.
- `scripts/hyaku/jj-lane.sh:115-130` is the **reference implementation** C2 must copy
  (`detect_branch`). It reads no census: it grades closure from `refs/heads/$branch`
  (`:456,543,553-554`) and provenance from `git log … refs/remotes/origin/$b..refs/heads/$b`
  (`:228`). No `findings`/`MORI_` token anywhere in the file.
- `scripts/hyaku/append-closure.py:18,97` and `scripts/hyaku/inline.sh:64-72` read `MANIFEST.json`
  for round/admission rows only. `MANIFEST.json:2369` carries historical prose
  (“live MORI_CENSUS: DRIFT findings=10”); nothing validates that prose.

### 2.2 `templates/`

Zero `mori`/`MORI_` matches. `templates/round-prompt.md:54-65` “Record the census before → after”
points at `{{FLEET_ROOT}}/scripts/sources-census.sh validate` (`:65`) — same name collision as
above. **A mori finding id cannot affect round conformance.**

### 2.3 Fleet `.ufo/`

- `.ufo/gates/root-ledgers.py` is the only fleet gate. Its docstring (`:1-38`) scopes it to
  `SCORECARD.md`/`LOG.md` header identity of the fleet **root**; `.ufo/gates/root-ledgers/expected.json:11-14`
  pins `## Gate registry — protocol lane registry home`, `## Aggregator lane`, and the
  `| closure-check | gate |` row prefix. It never reads a lane's `SKILL.md` registry and has no
  concept of finding ids. Adding a lane gate row or a new tool is invisible to it.
- `.ufo/state/mori.report-baseline` (`17 e3b0c442…`) is consumed by `scripts/shokunin-watchdog.sh:31,122-146`,
  which hashes the **report bytes** (round + sha256, `MIN_REPORT_BYTES` at `:141`). Census output
  is not involved; only the lane report's length/bytes are (unchanged by census edits, changed by
  any report edit).
- `.ufo/prompts/`, `.ufo/reports/round-*/mori.md`, `.ufo/waves/**` occurrences are prose receipts
  (`findings=10` in `.ufo/reports/round-1/mori.md:27`, `drift=11/findings=20` in the round-15
  report table) — historical text, never parsed.

### 2.4 Sibling lanes

- `chousa-shokunin/tools/research-gate.sh:180,2537-2538,2784` cites mori's r10 `--pin/--drift`
  **pattern** as lineage in comments and a generated header. It does not read mori files or ids.
- `kama-shokunin/.ufo/waves/round-16/build/advice/ConnectMori.md:20,26` cites
  `tools/mori-census.sh:46-47,1663-1669,1800-1805` as corroboration (prose).
- `tsukuroi-shokunin/.ufo/waves/round-17/falsify/outcome.json:15` publishes
  `dead_seats_provider_429` (28 lane-local seat names). This is the closest existing artefact to
  C1's capability, but it is tsukuroi's own wave record, not a consumer and not a schema mori's
  tool must satisfy. `mado-shokunin/.ufo/waves/round-17/drafts/ReportSkeleton.md:104` is a
  `{{DEAD_SEATS}}` report placeholder (template text).
- No sibling lane has a `tools/` consumer of mori: `kaidoku-shokunin/tools/` does not exist;
  `kama`/`tameshi`/`souji` tools contain no `mori-shokunin` path reads outside the two prose
  hits above.

## 3. In-lane consumers — the only real ones

| consumer | citation | reads | new-id safe? | exact assertion |
|---|---|---|---|---|
| silence oracle | `tools/mori-silence-cases.sh:595-645` (`verdict_grade`) | one `MORI_CENSUS:` line; `word` vs `drift=` digits as strings | yes | **CLEAN ⇒ `drift` exactly `0`; DRIFT ⇒ `drift` = `[1-9][0-9]*`** (`:620-645`) |
| silence oracle cases | `:669-720`, `:544-550` | `SURFACE lane.<lane>: <state>`, `^FINDING LANE_SILENT` presence (`:568-570`), rc, verdict word | yes | state/presence/rc/verdict word; **counts not compared** |
| silence shape-invariance | `:1079-1110` | two runs' state/api/finding/rc/verdict text | yes (both runs change together) | byte-identical after tree-name substitution |
| r13 gate | `tools/mori-round13-regressions.py:286-297` (`FINDING_RE = ^FINDING (\w+) severity=(\w+) obs=(.*)`), `:736-741` | finding rows by id | yes | per-id claims; no total-count assertion |
| r14 gate | `tools/mori-round14-regressions.py:271-281`, `:608-620`, `:991-994` | finding rows, `expect_findings` / `exact_counts` / `forbid_ids` | yes (per-id; unlisted ids tolerated) | **`vcounts["drift"] != case.expect_drift` ⇒ fail** (`:1975`) |
| r15 gate | `tools/mori-round15-regressions.py:1063-1076,1086-1094,1346,1440-1482` | oom/kill lines, every row's `script_sha256`, `drift` | yes | **`drift == want_oom + want_signal`** (`:1063,1075`); frozen control must also satisfy **`drift == oom_lines + kill_lines`** (`:1474-1482`) |
| r16 gate | `tools/mori-round16-regressions.py:90-92,131,1040-1043` | `MORI_JOURNAL_WINDOW_*` ids of the r16 probe; `CANARY_TOKEN_RE` only on fixture stderr | n/a | none on census output |
| census selftest | `tools/mori-census.sh:3010` (`^MORI_CENSUS: ${wverdict} `), `:4156` rollup | verdict word + explicit per-case regexes | yes | **no exact `findings=` regex exists** (`grep -n 'findings=[0-9]' tools/mori-census.sh` → no matches) |
| drift pin/drift | `:2501-2545` (`DRIFT_COUNTER_KEYS`, masks `findings drift surfaces unavailable count age_s *_epoch ts script_sha256`), `:2564-2571`, `:2626-2677` | canonical lines keyed `FINDING:<id>`/`SURFACE:<name>` | yes | line-set membership; `+FINDING:<id>` for an added line — **expected** drift |

Consequence: a new finding that fires in a fixture is red in r14/r15 (drift arithmetic) and can be
red in the silence oracle (verdict word/rc). A new finding that does not fire is invisible to all
of them.

## 4. C2 constraints that follow (each citable)

### 4.1 Severity token — `severity drift` must be implemented as `warn`

`emit_finding` (`tools/mori-census.sh:405-416`) has no severity validation; only `warn|crit`
increments `N_DRIFT` and sets `ROLL=DRIFT` (`:412-416`). A line with `severity=drift` therefore
lands in `findings=` and leaves the verdict CLEAN. `verdict_grade` would accept it, because its
cross-check is exactly “CLEAN ⇒ drift=0” (`tools/mori-silence-cases.sh:624-645`). r14/r15 would
also pass a run whose only anomaly is that line. If C2's “severity drift” is meant as “flips the
roll”, the emitted token must be `warn` (or `crit`); anything else is a silent no-op finding.
[INF] This is a contract-wording trap, not an observed defect.

### 4.2 Gate fixture stubs decide whether the new probes run at all

- r13 stub: `for a in "$@"; … rev-parse|ls-files|cat-file|log …; done; exit 2`
  (`tools/mori-round13-regressions.py:993-1014`), wired via `MORI_GIT_BIN` (`:1094`).
- r14 stub: same shape, `exit 2` (`tools/mori-round14-regressions.py:789-810`), wired in
  `census_env` (`:868-897`); r15 reuses `r14.build_fixture`/`census_env`
  (`tools/mori-round15-regressions.py:978-985`).
- census selftest stub: unknown verb ⇒ `git-other`; absent file ⇒ **rc 0, empty stdout**
  (`rc_of`/`out_of`, `:2790-2791`; dispatch, `:2839-2862`). There is no `git-other` fixture file
  (`grep -n 'git-other' tools/mori-census.sh` → only the dispatcher line).

So `symbolic-ref -q HEAD` reads as rc 0 + empty in the selftest, and rc 2 + empty in r13/r14/r15.
An implementation that treats rc 0 as success will build `refs/heads/<empty>`; one that treats
rc≠0 as “branch unresolved is drift” will fire on every r13/r14/r15 fixture. Both failure modes
are fixture-shaped, not host-shaped. **Required:** branch resolution failure (empty name, invalid
name, rc≠0) ⇒ keep today's `HEAD` probes, emit nothing. **Recommended:** add
`git-symbolic-ref` and `git-merge-base` arms to the selftest stub plus one mismatch case each;
the r17 jj gate (`mori-round17-jj-regressions.py`) is then the only real coverage, which is
consistent with C2's gate design but leaves `--selftest` unable to fail for the new arms.

### 4.3 Row 6 resolves the *root* repo, rows 9/HEAD resolve the *lane* repo

`ps_report_closed` runs `-C "$ROOT"` (`tools/mori-census.sh:2099-2102`); the report path is
fleet-root-relative for every lane (`:2094-2096`), while authorship runs `-C "$repo"` (`:2197,2207`).
The contract says “resolve the lane branch”, but two repos are in play. The silence fixtures make
this concrete: `git_init` is called on `$CASE_ROOT/<lane>-shokunin`
(`tools/mori-silence-cases.sh:445-450,1080-1095`) and only the aggregator case also commits into
`$CASE_ROOT`, which is otherwise not a repository. `HEAD_BRANCH_MISMATCH` therefore needs a
per-repo scope statement (lane repo; root repo for the report-closure probe) and must no-op when
that repo has no resolvable branch.

### 4.4 Duplicate ids interact with `--drift` pairing

`drift_line_id` keys finding lines as `FINDING:<id>` (`:2564-2571`) and `drift_report` pass 2 pairs
leftovers **by id, first unused match** (`:2645-2662`). The lane already records this as a
constraint: “routing findings keep per-scope ids (duplicate ids would break --drift line pairing)”
(`tools/mori-round13-regressions.py:208`). `LANE_AUTHOR_MISMATCH` emitted once per lane shares one
id by design; if two lanes' lines differ, leftover pairing can attribute lane A's baseline line to
lane B's new line and name the wrong changed field. [INF] Mitigation consistent with lane practice:
put `lane=` first in `obs=` and accept the risk (as `LANE_SILENT` already does, `:2291`), or emit
per-lane ids. No consumer *requires* either.

### 4.5 Live effect today `[OBS]`

- `HEAD_BRANCH_MISMATCH` **will not fire** on this host now: `symbolic-ref` → `refs/heads/master`,
  `HEAD` == `refs/heads/master` == `24526ea`, `merge-base --is-ancestor` rc 0 (§1).
- `LANE_AUTHOR_MISMATCH` **will fire** on jj-produced commits whose committer is the lane identity
  and whose author is not — exactly the F4 case measured in
  `.ufo/waves/hyaku/jj-w1/reports/JjAuditMori.md:79-94`
  (`611dfb5|Joao Pedro Veiga <jpveigao10@gmail.com>|mori-shokunin <mori@shokunin.local>|subject work`).
  Live `drift=` therefore rises by at least one for any lane that shipped such commits after
  launch. No gate parses live output; recorded live counts in reports/evidence become stale, and
  `bash tools/mori-census.sh --drift corpus/evidence/baseline-r10-20261015T2231Z.json` will add
  `+FINDING:LANE_AUTHOR_MISMATCH`. That baseline is **already red** (`SKILL.md:165`; its pinned
  `volatile_fields` header at `corpus/evidence/baseline-r10-20261015T2231Z.json:4` still lists
  `kill_signal`, absent from `DRIFT_COUNTER_KEYS` at `tools/mori-census.sh:2501-2517`), so no
  clean-drift expectation exists to break.

## 5. C1 — new tool `tools/mori-seat-terminal.py`

- No consumer exists. Nothing under `scripts/`, `templates/`, `.ufo/gates/`, or any sibling
  `tools/` reads `mori-seat-terminal*`, `mori-seat-terminal-v1`, `MORI_SEAT_TERMINAL_*`
  (whole-tree grep; only this round's `.ufo/waves/round-17/**` contract/build text matches).
- Gate registry obligation is self-declared: `SKILL.md:156-172` is a prose table with one row per
  gate/probe; nothing parses it. Adding a row is conformance bookkeeping, not a consumer contract.
  Note the existing row already carries a **stale** selftest count (`SKILL.md:164`: “104/104 at
  8d22d18”, while the round-15 report records 113 PASS) — further evidence nothing reads it.
- Field-name inconsistency to decide once: the contract puts the id in **`finding`**
  (`.ufo/waves/round-17/contract.md:62-64`) while the lane's r16 probe uses **`finding_id`**
  (`SKILL.md:172`; `tools/mori-journal-window.py:109-116,492-506`), and the r16 gate keys on
  `finding_id` (`tools/mori-round16-regressions.py:90-92`). No consumer today, but a future
  generic consumer cannot read both. Another seat reached the same conclusion independently
  (`.ufo/waves/round-17/build/ReviewExitSemantics.md:9`).
- Operability, observed container: `~/.omp/agent/sessions` holds **5816** `*.jsonl` files, 5.4 G,
  183 directories — safely under `--max-files 20000`, so rc 2 `too-many-files` will not fire
  today. [INF] Worst-case tail read at defaults is `5816 × 262144 B ≈ 1.45 GiB`; if the scan is
  run inside a wave this cost is worth naming in `--help` beside the existing limits.
- `--selftest` and the r17 gate (`mori-round17-seat-regressions.py`) have no existing harness to
  conform to; the r16 gate is tool-parameterised (`--tool PATH`, `SKILL.md:170`), so a sibling gate
  of the same shape is additive.

## 6. Residual unknowns

- [INF] Whether `drift_report` pass-2 mispairing has ever produced a wrong field name on a real
  multi-lane run was not measured (no census run permitted for this seat).
- Whether L1 intends `HEAD_BRANCH_MISMATCH` to be per-repo or root-only is not fixed by
  `contract.md`; §4.3 states the ambiguity, not a ruling.
- `JjAuditMori.md:217` names the suggested token `head_branch_mismatch` (lowercase); C2 fixes
  `HEAD_BRANCH_MISMATCH`. No consumer depends on case, but the routed evidence and the contract
  disagree on spelling.
- I did not read OMP transcript contents; the 5816-file count is filesystem metadata only.

## 7. Tooling

No installs, no upgrades, no package transactions, no host services. Commands were read-only
(`grep`, `find`, `du`, `git symbolic-ref|rev-parse|merge-base`); no selftest was executed.
