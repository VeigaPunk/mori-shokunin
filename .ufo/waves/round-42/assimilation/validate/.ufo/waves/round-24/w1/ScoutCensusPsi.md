# ScoutCensusPsi — census memory-PSI grammar, labels, finding ids, exit codes

Seat: MoriR24.ScoutCensusPsi (read-only leaf). Claim C2 surface.
Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Anchor: lane HEAD `f7eb430c25921740924bfb263fd14ca16c3766ad`; `tools/mori-census.sh`
4744 lines, sha256 `87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28`
(= the `script_sha256=` the census stamped into its own findings during the runs below;
`git status --porcelain tools/mori-census.sh` empty, so the file is committed and clean).
No files written outside `/fast/scratch/hyaku/mori-r24-a2/scout-census-psi/` (scratch
fixtures) and this report.

## 1. What the census actually reads

- Path: `CGROUP_PRESSURE=${MORI_CGROUP_PRESSURE:-${CGROUP_EVENTS%.events}.pressure}`
  (`tools/mori-census.sh:308`), with
  `CGROUP_EVENTS=${MORI_CGROUP_EVENTS:-/sys/fs/cgroup/user.slice/user-$(id -u).slice/memory.events}`
  (`:305`). Default target is therefore
  `/sys/fs/cgroup/user.slice/user-<uid>.slice/memory.pressure` — the **user slice cgroup**
  file. The census reads no `/proc/pressure/*` path anywhere (grep for `/proc/pressure`
  over the lane repo hits only `LOG.md`, `.ufo/waves/**`, `corpus/**`; grep for `pressure`
  over `tools/` hits only cgroup `memory.pressure` fixtures/usages).
  Contract C2's premise ("the census reads only the user slice's `memory.pressure`") is
  accurate.
- Reader: `psi_avg10 <text> <some|full>` (`:652-654`) then `is_decimal` (`:642-645`),
  called at `:1739-1742`; grading at `:1754-1762`.

## 2. Grammar the census accepts

`psi_avg10` (`tools/mori-census.sh:652-654`):

```
printf '%s\n' "$1" | awk -v kind="$2" '$1 == kind { for (i = 2; i <= NF; i++) if ($i ~ /^avg10=/) { sub(/^avg10=/, "", $i); print $i; exit } }' || true
```

Accepted, per kind (`some` / `full` independently):

- field 1 must equal the kind token **exactly** (case-sensitive, so `SOME` never matches);
- any later field beginning `avg10=` supplies the value; **field order is free**, and any
  other fields (`avg60=`, `avg300=`, `total=`, junk) are ignored — `avg60`/`avg300`/`total`
  are never required and `total=` is never parsed at all;
- on duplicate kind lines the **first** line that carries an `avg10=` field wins
  (awk `exit` after the first match; a kind line without `avg10=` does not stop the scan);
- the extracted token must then pass `is_decimal` (`:642-645`): non-empty, digits and dots
  only, and after deleting digits the remainder is `''` or a single `.`. So `0.00`, `10`,
  `1.`, `.5`, `.` pass; `x.xx`, `1.2.3`, `-1`, `1e3`, `avg10=` (empty) fail;
- a failing token is **blanked**, not reported (`:1741-1742`).

Everything the grammar refuses is silent: no finding, no state change, no diagnostic.
Measured (fixtures under `/fast/scratch/hyaku/mori-r24-a2/scout-census-psi/fx/`, census
run with `MORI_CGROUP_PRESSURE` pinned per variant, everything else pinned to the same
fixture tree):

| fixture bytes | `psi_some_avg10` | `psi_full_avg10` | `psi_source` | surface state | rc |
|---|---|---|---|---|---|
| canonical `some`+`full` | 0.00 | 0.00 | ok | ok | 0 |
| `some avg10=x.xx …` | unavailable | 0.00 | **ok** | ok | 0 |
| `full` line only | unavailable | 0.00 | **ok** | ok | 0 |
| `some` without any `avg10=` | unavailable | 0.00 | **ok** | ok | 0 |
| two `some` lines (25.00 then 0.00) | **25.00** | 0.00 | ok | drift | **1** |
| canonical + trailing `bogus` field | 1.50 | 0.00 | ok | ok | 0 |
| empty file | unavailable | unavailable | **ok** | ok | 0 |
| mode-000 file | unavailable | unavailable | **unreadable** | ok | 0 |
| file absent (dir present) | unavailable | unavailable | **absent** | ok | 0 |
| `full avg10=99.00`, `some avg10=0.00` | 0.00 | 99.00 | ok | ok | 0 (no finding) |
| path is a directory (`-r` true, `cat` rc≠0) | unavailable | unavailable | **unreadable** | ok | 0 |

## 3. How absent / unreadable / malformed are labelled

State machine, `tools/mori-census.sh:1735-1753`:

1. `[ -r "$CGROUP_PRESSURE" ]` → `cap cat`; `CAP_RC -eq 0` → parse, `psi_state` stays `ok`;
   `CAP_RC -ne 0` → `psi_state=unreadable` (`:1743-1745`).
2. `elif [ -e "$CGROUP_PRESSURE" ]` → `psi_state=unreadable` (`:1746-1750`; the comment
   records that a mode-000 path was once mislabelled `absent`).
3. else → `psi_state=absent` (`:1751-1752`).

- **absent** → surface field `psi_source=absent`, both averages render `unavailable`
  (`:1862`), no finding, surface state stays `ok`, exit code unaffected.
- **unreadable** → `psi_source=unreadable`, same `unavailable` averages, no finding, exit
  code unaffected. Two entry paths, both measured above.
- **malformed** → **no such label exists.** `psi_source` is `ok` for every readable file
  regardless of contents (`:1735` initialises `psi_state=ok` and nothing but the two error
  branches ever changes it), so malformed bytes are indistinguishable from "this kind is
  absent" on the average fields. The census's vocabulary for a shape-failed read exists
  only on the sibling `memory.peak` reader, which uses the token **`shape-refused`**
  (`:1830-1840`), not `malformed`; PSI never got that arm.
- **EOPNOTSUPP / EACCES / EPERM** are not distinguished: any failure after `-r` is true
  takes branch 1. `[ -r ]` is `access(2)`, which for a procfs PSI file should succeed while
  the failing `open()` returns `EOPNOTSUPP`, so a PSI-disabled kernel would most likely be
  reported `unreadable`. **[INFERENCE]** — the `cat`-rc branch itself is measured (directory
  proxy above); the EOPNOTSUPP mapping was not exercised (cannot toggle host PSI).
- **counter regression** has no PSI analogue: the census never reads `total=`. Its counter
  machinery is drift-pin normalization only, and `psi_some_avg10`/`psi_full_avg10` are
  listed in `DRIFT_VOLATILE_SPECIAL` (`:2771`) — masked, i.e. explicitly *excluded* from
  drift comparison.

## 4. Finding ids, severities, exit codes

`emit_finding` (`:419-431`): line shape
`FINDING <ID> severity=<info|warn|crit> obs=<fields> ts=<UTC> script_sha256=<sha>`;
`info` does not touch the roll, `warn|crit` sets `ROLL=DRIFT`.
`emit_surface` (`:433-440`): `SURFACE <name>: <state> (<detail>)`; state `unavailable`
only increments `N_UNAVAIL`.

Emitted by `probe_cgroup` (`:1680-1863`):

| id | severity | condition |
|---|---|---|
| `CGROUP_UNAVAILABLE` | info | `memory.events` unreadable — early return, surface `cgroup: unavailable` (`:1684-1688`; selftest `:4370-4375`) |
| `MEM_PRESSURE_HIGH` | warn | integer part of `some avg10` ≥ `MEM_PSI_WARN_AVG10` (default 10, env `MORI_MEM_PSI_WARN_AVG10`, `:367`); obs carries `psi_some_avg10=… threshold_avg10=… threshold_label=local path=…` (`:1759`) |
| `MEM_FILL_HIGH` | warn | fill pct ≥ `MEM_FILL_WARN_PCT` (85) when `memory.max` is numeric (`:1806`) |
| `MEM_AVAIL_LOW` | warn | host `MemAvailable/MemTotal` ≤ `MEM_AVAIL_MIN_PCT` (10) when `max` is the literal `max` (`:1796`) |
| `CGROUP_OOM_KILL` / `CGROUP_OOM_KILL_CUMULATIVE` | crit / info | `:1850-1857` |

There is **no finding for an absent, unreadable or malformed PSI source**; the only PSI
finding is the threshold alarm. Grading reads `some` only (`:1754-1762`): `psi10=${psi_some%%.*}`
then `is_int`, so the comparison is on the truncated integer part (a token like `.5` yields
empty and is skipped entirely), and a high `full` never fires (measured: `full avg10=99.00`
→ rc 0, no finding).

Exit codes (`:7-8`, `:410-411`, `:2717-2721`): `0` CLEAN, `1` DRIFT (≥1 warn/crit finding),
`2` setup/usage (`die_usage` `:416`; `--pin` write failure `:2934`; `--drift` baseline
missing/unreadable/malformed `:2945-2975`). Surface `unavailable` never changes the exit
code — measured rc 0 with `unavailable=6`, and pinned by the selftest at `:4370-4375`
(`SURFACE cgroup: unavailable` + `MORI_CENSUS: CLEAN`). Summary line:
`MORI_CENSUS: CLEAN|DRIFT (findings=N drift=D unavailable=U surfaces=S)` (`:2714`).

## 5. Inconsistencies between census conventions and contract C2

None of these is a defect in either artifact; each is a place where the L1 must decide
whether `tools/mori-pressure.py` follows the census or the contract.

1. **State vocabulary.** Census PSI source states are exactly `ok | absent | unreadable`
   (`:1735-1753`). C2 requires six (`ok | absent | unsupported | unreadable | malformed |
   counter_regressed`). Three have no census precedent at all, and the census's `ok` is
   *not* evidence of a successful parse — it means only "the read returned 0". Consequence
   for comparison: C2 `unsupported` → census `unreadable` (lossy), C2 `malformed` → census
   `ok` + `unavailable` token (lossy), C2 `counter_regressed` → no census analogue.
2. **Malformed handling.** The census deliberately drops unparsable tokens rather than
   labelling the resource (`:1741-1742`, comment at `:625-628` frames this as print safety
   for operator-pinnable paths). C2 makes any non-canonical shape a `malformed` state that
   is reported. Same bytes, different labels: measured `some avg10=x.xx` → census
   `source=ok`, some `unavailable`, rc 0, no finding; C2 case P08 expects io `malformed`
   with verdict PARTIAL.
3. **Grammar strictness.** Census accepts a superset of C2's frozen grammar: extra trailing
   fields (measured: accepted, `some=1.50`), free field order, missing `avg60`/`avg300`/
   `total`, and duplicate kinds where the first line wins (measured: `dup-some` fires
   `MEM_PRESSURE_HIGH`, rc 1). Under C2 all four are `malformed`/`PRESSURE_PARTIAL`, and
   P09 (`memory` missing `full`) is `malformed` whereas the census's tolerance for a missing
   kind is per-resource only by accident — it never requires `some` on memory either
   (measured `full`-only → `source=ok`). C2's irq-`full`-only tolerance is a rule the census
   does not have; the census's "missing kind is fine" is a rule C2 does not have.
4. **Decimal shape.** `is_decimal` (`:642-645`) accepts `1.`, `.5` and `.`; C2 writes `D` as
   "a decimal" without pinning digits-before/after-dot. If the tool's regex is
   `\d+\.\d+`, `.5`/`1.` become `malformed` where the census accepts them (and `.5` is
   silently ungraded by the census because `${psi_some%%.*}` is empty). Worth one frozen
   case if the L1 wants the two readings comparable.
5. **Grading kind and comparison.** Census grades `some` of memory only, on the truncated
   integer part, `≥ 10`; `full` is read and printed but never graded (measured: `full=99.00`
   → rc 0). C2 grades `some` of cpu/io/memory and `full` of memory/io/irq with a float
   threshold (`--warn-avg10`, default 10.0). Same default, same `threshold_label=local`
   convention (`:1759`; C2 "labeled local, not calibrated") — the label convention is
   consistent and should be preserved; the `full`-of-memory arm is new capability, not a
   conflict.
6. **Exit-code semantics for unavailability.** Census: unavailability never decides the exit
   code (a run with every surface unavailable still exits 0 if no warn/crit fired).
   C2: `PRESSURE_UNAVAILABLE` → exit 2 when every resource is unavailable, `PARTIAL` → exit 0.
   C2's use of exit 2 for "cannot observe" collides with the census's exit 2 = "the probe
   itself could not run / usage error", which is a different meaning of the same code. The
   census's nearest analogue for partial unavailability is the `unavailable=U` counter in
   the verdict line plus per-surface `unavailable` state.
7. **Finding/verdict naming.** Census `MEM_PRESSURE_HIGH` (surface-scoped, `MEM_` prefix,
   severity + free-form `obs=`), C2 `PRESSURE_HIGH` with structured `findings[]` objects
   carrying `id` and `resource` and no severity field. Verdict words `CLEAN|DRIFT` vs
   `PRESSURE_OK|PRESSURE_HIGH|PRESSURE_PARTIAL|PRESSURE_UNAVAILABLE`. No contradiction, but
   no shared vocabulary either; the census offers no precedent for a resource-scoped
   finding id or for a verdict word other than CLEAN/DRIFT.
8. **Scope.** Census = cgroup user-slice `memory.pressure`; C2 = system
   `/proc/pressure/{cpu,memory,io,irq}`. Confirms C2's "unobserved" premise (no tool in
   `tools/` reads `/proc/pressure`), and means the two readings are not substitutes: a
   system-scope `absent` is not the same fact as the cgroup file being absent.

## 6. Unverified / remaining unknowns

- EOPNOTSUPP-on-open mapping to `unreadable` is inference, not measurement (host PSI is
  enabled; no PSI-disabled kernel available). The `cat`-rc branch was exercised with a
  directory proxy only.
- `tools/fixtures/mori-pressure/cases.json` does not exist yet at this revision
  (`read` returned "not found"), so the frozen P01–P12 bytes could not be diffed against
  census behaviour; item 3 above is derived from the contract text and the shared-interface
  spec in my task, not from the frozen file.
- C2's exact `D` regex and its treatment of `1.`/`.5`/`.` (item 4) are unknown until
  `tools/mori-pressure.py` lands.
- Only the PSI branch of `probe_cgroup` was probed; `MEM_FILL_HIGH`/`MEM_AVAIL_LOW`/
  `CGROUP_OOM_KILL` behaviour is read from source and the selftest, not re-measured here.

## 7. Tooling

No installs, no upgrades, no package transactions (pacman guard untouched).
