# ReviewCensusMemoryPsi — round 24 wave 1 (claim C2 support, read-only)

Seat: MoriR24.ReviewCensusMemoryPsi (leaf reviewer; no subagents used).
Subject: the census memory PSI reader in `tools/mori-census.sh` (block at lines
1728-1762, helper `psi_avg10` at 654-658) checked against the kernel document
https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst
("psi.rst v7.2"), with kernel behavior grounded in
https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c (v7.2).
Scope: detection and report only. The census is not changed this round; these
findings inform C2's no-harm boundary. Nothing was written outside this report
file and `${TMPDIR}` probe scratch (removed after each probe).

Baseline facts used throughout:

- psi.rst v7.2 defines the format as two lines, `some` then `full`, each
  `avg10= avg60= avg300= total=`; the cgroup2 section says each cgroup carries
  `cpu.pressure`, `memory.pressure`, `io.pressure` "the format is the same as
  the /proc/pressure/ files".
- The census reads only the cgroup file `$CGROUP_PRESSURE`
  (default `${CGROUP_EVENTS%.events}.pressure`, line 308), never
  `/proc/pressure/*`. The path is operator-pinnable via `MORI_CGROUP_PRESSURE`
  (line 224), which is why malformed-content behavior matters.
- Reader chain: `cap cat -- "$CGROUP_PRESSURE"` (1737; `cap` at 561-565 merges
  stderr into `CAP_OUT` and returns `CAP_RC`), then `psi_avg10 "$CAP_OUT" some`
  and `... full` (1739-1740), each result shape-gated by `is_decimal` (641-644)
  at 1741-1742. Grading reads only `some`: `psi10` integer part vs
  `MEM_PSI_WARN_AVG10` (1754-1761, finding `MEM_PRESSURE_HIGH` at 1759). The
  state field `psi_source` is written only at 1735/1744/1750/1752 and consumed
  only in the surface row at 1862.

## Findings, by severity

### F1 — Medium: a missing `full` line is reported as `psi_source=ok` (malformed content never demotes the state)

- `psi_state` starts `ok` (1735) and is demoted only on a failed read
  (`CAP_RC != 0`, 1743-1744) or when the file is present-but-unreadable /
  absent (1746-1752). A read that succeeds but does not match the psi.rst
  format leaves the state at `ok`: `psi_avg10` finds no `full` line and
  returns empty (657), `is_decimal` refuses the empty token (1742), and the
  row prints `psi_full_avg10=unavailable` next to `psi_source=ok` (1862).
  psi.rst v7.2 declares both lines part of the format, so a one-line
  memory.pressure is not a conformant read, yet the census can express only
  ok / unreadable / absent — there is no malformed state.
- Empirical (probe, pinned `MORI_CGROUP_PRESSURE` to a file containing only
  `some avg10=3.50 avg60=0.00 avg300=0.00 total=10`):
  `psi_some_avg10=3.50 psi_full_avg10=unavailable psi_source=ok`, census exit
  from that surface unperturbed, zero bytes on stderr. The state field claims
  a healthy read while the value is silently missing.
- Verdict impact is correctly none — grading uses `some` only (1754-1761) — so
  this is a disclosure-honesty defect, not a crash or false DRIFT. The same
  root covers a pinned foreign file (e.g. text with no PSI lines at all):
  `psi_source=ok` with both values `unavailable`.
- Context: on a PSI-enabled kernel >= 4.20 a real memory.pressure always has
  both lines, so the edge is reachable through truncation/short reads or the
  operator pin, not the live kernel. (Contrast in psi.rst v7.2: system-wide
  cpu `full` is "set to zero for backward compatibility" since 5.13 — present
  but zero — which is a different situation the census never sees, since it
  reads the cgroup memory file only.)

### F2 — Low: EOPNOTSUPP collapses into `unreadable`; "PSI unsupported" is not expressible

- Kernel grounding: v7.2 psi.c `psi_show` returns `-EOPNOTSUPP` when PSI is
  disabled at boot (`psi=` param or `CONFIG_PSI_DEFAULT_DISABLED`) and for
  `PSI_IRQ` without irqtime (kernel/sched/psi.c lines 1255-1262 in v7.2: the
  `static_branch_likely(&psi_disabled)` guard and the
  `!irqtime_enabled() && res == PSI_IRQ` guard). Open still succeeds, so
  `[ -r "$CGROUP_PRESSURE" ]` (1736) is true, `cap cat` fails, and the file
  lands in `psi_state=unreadable` (1743-1744).
- Empirical stand-in (a read that fails after a successful open — pinned path
  was a directory): `psi_some_avg10=unavailable psi_full_avg10=unavailable
  psi_source=unreadable`, zero stderr bytes (cat's error is merged into
  `CAP_OUT` by `cap`, 563, and never echoed), census completed without crash.
- I could not reproduce literal EOPNOTSUPP read-only: this host has PSI
  enabled (live `memory.pressure` reads as two well-formed lines, measured:
  `some ... total=26596` / `full ... total=26421`), and disabling PSI would
  require a boot or service change, which this seat forbids. The mapping
  rests on the shared cap-failure code path plus the psi.c source, not a
  literal reproduction — stated plainly as a verification gap.
- Judgment: no crash, and the 1746-1750 branch correctly keeps this distinct
  from `absent`. The gap is labeling fidelity only: a host with PSI compiled
  out or disabled reads `psi_source=unreadable`, a fact the census cannot
  separate from a permissions accident.

### F3 — No defect: extra whitespace is handled correctly

- `psi_avg10` (656-658) uses awk's default field splitting: leading blanks,
  tabs, and runs of spaces collapse, and `$1 == kind` matches the bare token;
  the value is then shape-gated by `is_decimal` (641-644), so nothing
  whitespace-tainted can reach the row.
- Empirical: fixture with a leading tab, doubled spaces, and a tab before
  `avg60` parsed cleanly — `psi_some_avg10=4.50 psi_full_avg10=1.25
  psi_source=ok`, rc 0, no stderr.
- Residual corners, none kernel-emitted: `avg10 = 1.00` (space inside the
  pair) finds no token and falls under F1's silent-ok; a CR glued to the kind
  token (`some\r`) misses `$1 == kind`. Both matter only for operator-pinned
  foreign files.

### F4 — Medium: no selftest case covers any of the three edges

- Exhaustive fixture census (grep over `memory.pressure|MORI_CGROUP_PRESSURE`
  writers in the selftest region 3006-4716): exactly three fixtures — line
  3196 (baseline, well-formed quiet), 4421 (`mem-psi-high`, drift), 4428
  (`mem-psi-under`, clean) — plus the wiring at 3256 (`sut_env`). All three
  are well-formed two-line files. No one-line / missing-`full` fixture, no
  empty or garbage fixture, no whitespace variant, no CRLF variant.
- No unreadable-pressure fixture either: every `chmod 000` in the selftest
  (3445, 3513, 4348, 4362, 4506, 4553) touches shokunin.conf, ufo/state,
  wave trees, or a lane subtree — never memory.pressure. Sharpest single gap:
  the mode-000 fix at 1746-1750 (its comment cites a measured misreport of a
  mode-000 pressure file as `absent`) shipped with no regression case, so
  that exact fix could silently disappear while the suite stays green.
- Measured today: `tools/mori-census.sh --selftest` →
  `MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)`, rc 0,
  about 13 s. The pass is real and covers none of the three edges.

## No-harm boundary implications for C2 (informs, does not change, the census)

- The census's observable PSI vocabulary is exactly `psi_source` in
  {ok, unreadable, absent} with values {decimal token, unavailable} (1862).
  A same-identity comparator on shared fixtures should pin these exact
  strings; an expectation of `malformed` or `unsupported` from the census
  would be comparing against behavior the census never had.
- Malformed content is disclosed as `ok` + `unavailable` today (F1). If C2's
  new tool reports `malformed` on the same content, that is a deliberate
  vocabulary extension on the C2 side, not a census regression either way.
- EOPNOTSUPP reads as `unreadable` in the census (F2); C2's frozen interface
  distinguishes `unsupported`. The comparator must treat census `unreadable`
  as the pre-existing label for that kernel condition.
- The census grades only `some` (1754-1761) and emits no delta or stall-ratio
  fields; `full` is display-only. Assertions of drift on `full`-only fixtures
  are outside census behavior by construction.

## Method, installs, verification gaps

- No tool installs or updates were needed or made (curl, grep, awk, bash all
  present). Pacman untouched, per the host pause.
- Ran, all read-only toward the repo and host: `tools/mori-census.sh
  --selftest` (writes only under `${TMPDIR:-/tmp}/mori-census-selftest.*`
  per its header, lines 211-212; cleaned by its own trap); three pinned
  live-census probes with scratch under `${TMPDIR}` (removed); read-only
  `cat` of the host's live `memory.pressure`.
- Did not run: literal EOPNOTSUPP reproduction (needs PSI disabled — a boot
  or service change, forbidden for this seat); `--pin`/`--drift` paths; any
  `/proc/pressure/*` reader (out of scope — the census reads only the cgroup
  memory.pressure file); no jj or git state was touched beyond reads.
