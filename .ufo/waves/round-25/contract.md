# mori round 25 (attempt 1) — claim contract

L1: MoriR25 (fresh in-session lane subagent, dispatched 2026-10-22T09:42:02Z). Entering lane tip
`28b79d3d1b76824f0c825aabe6cb6c5dc49961bf` (round 24 admitted; spot-check
`corpus/lessons/round-24-verifier-spotcheck.md`). No earlier attempt of round 25 left work in the lane.

Two claims. Each declares one after-value that one command over committed bytes re-derives. A miss is
an honest stop; the targets below are never narrowed after landing.

## C1 — repair the round-24 routed defects D1–D4 (axis: calibration, active score 5, lowest tie)

Source: `corpus/lessons/round-24-verifier-spotcheck.md:135-146`. Each routed defect is a place where a
lane-written statement or record disagrees with the committed bytes. New read-only check
`tools/mori-routed-r24.py --repo PATH --rev REV` reads git objects only (no working tree, no git
writes) and reports one row per item:

| Item | Routed defect | Held at REV when |
|---|---|---|
| D1 | `c2-selftest-after.txt` names no revision and predates the tool it shipped with | `.ufo/waves/round-25/evidence/pressure-selftest.txt` exists; its first line is `revision: <40 hex>` naming a commit R that is an ancestor of (or equal to) REV; the blob of `tools/mori-pressure.py` and the tree of `tools/fixtures/mori-pressure` are identical at R and at REV; its second line is `exit: <n>`; the remaining bytes equal the stdout of R's `tools/mori-pressure.py --selftest` run under `python3 -I -B` from a temporary extract of R (git object reads only), and `<n>` equals that run's exit code |
| D2 | the knowledge entry still carries the corrected K5, K4 and P3 wording; no K4 row in its corrections section | in `corpus/knowledge/system-pressure-r24.md`, outside every section whose heading starts `## Corrections`, with line breaks folded to single spaces, 0 matches of each of `refreshed on each read`, `a shorter spike between two reads can be invisible` and `` `null` means *undefined* ``; and some `## Corrections` section contains the token `(K4)` |
| D3 | the round-24 lesson says the supplementary file is S01–S06, `PASS 6/6`; it held 7 cases at the round-24 tip | let n = number of cases in `tools/fixtures/mori-pressure/supplementary-cases.json` at `4f05dd5a32055e85a9297eb8fc8dfec7dfc4625e` (7); `corpus/lessons/round-24.md` at REV has a line containing `Correction` and `PASS n/n` |
| D4 | untracked `tools/__pycache__/` is not ignored | `.gitignore` at REV has a line that is exactly one of `__pycache__/`, `__pycache__`, `**/__pycache__/`, `tools/__pycache__/`, `*.pyc`, `*.py[cod]` |

Output: one JSON object, `schema: mori-routed-r24-v1`, `items: 4`, `held: N`, `mismatches: 4 - N`,
per-item `{id, held, reasons[]}`. Exit 0 when `mismatches` is 0, 1 otherwise, 2 when the repo or revision
cannot be read.

- **Before (expected):** at `28b79d3d`, `mismatches: 4` (no round-25 evidence file; three phrases
  present and no K4 row; only `PASS 6/6`; `.gitignore` has no such line).
- **Declared after:** `python3 -I -B tools/mori-routed-r24.py --repo <lane> --rev <landed tip>` prints
  `"mismatches": 0` with `"held": 4` of `"items": 4`, exit 0.

The carried bound (round-24 R4 trusts lane-written times) is answered, not counted: each round-25 attempt
row records the seat gate's own ledger line (epoch seconds written by `wave-slot.sh`), a time the lane
does not write. The six surviving round-24 pressure mutants are replayed against the tip tool and either
killed by new supplementary cases or explained; that work is not counted toward C1.

## C2 — harness background-job runway capability (axis: coverage, active score 6; sourced)

Live fact opened this round: this omp process refuses `task` calls while 100 or more background jobs run,
although `~/.omp/agent/config.yml` sets `async.maxJobs: 200`, and background shell jobs count too. The
installed binary (`omp/18.12.6`, `~/.local/bin/omp`, 256,702,432 bytes) carries
`maxRunningJobs: () => Math.min(100, XPe.get(R))` once and the setting `async.maxJobs` with
`default: 100` once (L1 byte search, 2026-10-22). No mori tool reads this runway; it is new PROVINCE ground.

New read-only tool `tools/mori-job-runway.py [--config PATH] [--binary PATH] [--selftest]`, Python 3
standard library only, runs under `python3 -I -B`. Defaults: `--config ~/.omp/agent/config.yml`,
`--binary` = the real path of `omp` found on PATH. It never runs omp, never writes, and never edits settings.

Rules (binding for the tool and the frozen cases):

1. **configured** — from the config text. Find a line exactly `async:` (column 0, optional trailing
   `# comment`). Its block is the following lines up to the next non-blank, non-comment line at column 0.
   Direct children sit at the indentation of the block's first non-blank, non-comment line; deeper lines
   are ignored. A direct child `maxJobs: <value>` (optional trailing `# comment`) gives the value.
   State `set` with the integer when the value is an unquoted decimal integer; `malformed` (value null) when
   the value is anything else, when `maxJobs` appears twice as a direct child, or when `async:` carries an
   inline value (for example `async: {maxJobs: 50}`); `absent` when the file does not exist, has no `async:`
   line, or the block has no direct `maxJobs`; `unreadable` when the path exists but cannot be read as a
   file (for example it is a directory). Keys under other top-level blocks never count.
2. **clamp** — every match in the binary bytes of
   `maxRunningJobs:\s*\(\)\s*=>\s*Math\.min\(\s*(\d+)\s*,\s*[\w$]+\.get\([\w$]+\)\s*\)`. State `found` with
   the value when there is at least one match and all matches carry the same number (`sites` = match count);
   `ambiguous` (value null) when the numbers differ; `absent` (value null) when there is no match;
   `unreadable` when the binary cannot be read. An absent clamp is never read as "no clamp".
3. **setting_default** — every match of `id:\s*"async\.maxJobs",[^}]{0,300}?default:\s*(\d+)`. Same states
   as the clamp.
4. **effective** — null unless the clamp is `found` and either configured is `set`, or configured is
   `absent` and the default is `found`. Then base = configured value if `set`, else the default value, and
   effective = max(1, min(clamp, base)) (the binary's `Math.max(1, Math.floor(...))` over `Math.min`).
5. **verdict / exit** — effective null → `RUNWAY_UNKNOWN`, exit 2. Configured `set` and effective ≠
   configured → `RUNWAY_CLAMPED`, exit 1. Configured `set` and equal → `RUNWAY_AS_CONFIGURED`, exit 0.
   Configured `absent` → `RUNWAY_DEFAULT`, exit 0. Usage errors exit 2.
6. **output** — one JSON object: `schema: mori-job-runway-v1`, `config_path`, `binary_path`,
   `binary_sha256` (null when unreadable), `configured {state, value}`, `clamp {state, value, sites}`,
   `setting_default {state, value, sites}`, `effective`, `verdict`.
7. **selftest** — `--selftest` loads `tools/fixtures/mori-job-runway/cases.json` (resolved from the script's
   own path), writes each case's `config` and `binary` into a fresh temporary directory (`config: null` →
   no file; `config: {"dir": true}` → a directory at that path), runs the same evaluation, and compares the
   case's `expect` fields. It prints `MORI_JOB_RUNWAY_SELFTEST: PASS n/N` (or `FAIL n/N` plus one line per
   failing case) and exits 0 only when all pass.

- **Scope bounds:** the tool reads one config file, not project-level or environment overrides; it reports
  the per-session cap the binary computes, not how many jobs run now. The live running-job count is not
  readable from outside the session and stays frontier.
- **Before:** `git cat-file -e 28b79d3d:tools/mori-job-runway.py` exits 128.
- **Declared after:** `python3 -I -B tools/mori-job-runway.py --selftest` prints
  `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21`, exit 0, over `tools/fixtures/mori-job-runway/cases.json`
  committed before the tool (21 cases J01–J21, frozen with this contract).
- **Sourced:** the knowledge entry `corpus/knowledge/harness-job-capacity-r25.md` cites `SOURCES.md` rows
  opened this round (upstream oh-my-pi source at the tag matching 18.12.6, plus the installed binary as an
  own-work row). A live run against this host is committed as evidence; it is not the after-value.

Held and observed: operability 7, depth 5, freshness 5, adjacency 6. No retirement, waiver, exploratory
claim or promotion.

## Amendment A1 (10:12Z, before the C1 tool lands; wave-1 seats CriticC1Predicates and CriticSizing)

Findings: D2 and D3 passed on paraphrase, heading renames, row deletion and spacing; D1 re-created only the
round-24 output, needed the closure to run a registered gate, and passed on a red run; D4 is hygiene, not a
lane self-assessment; neither after-value required committed evidence. C2 is unchanged except wording.

**C1 counted items are now the three where a lane self-assessment contradicts committed bytes.**

| Item | Self-assessment contradicted | Held at REV when (git object reads only; no code from REV is run) |
|---|---|---|
| D1 | `SCORECARD.md:1514` says the pressure selftest prints `PASS 12/12` then `MATCHER: rejected 48/48`; the committed evidence `c2-selftest-after.txt` lacks the second line and names no revision | `.ufo/waves/round-25/evidence/pressure-selftest.txt` exists with header lines, in order, `revision: <40 hex>` (a commit R that is REV or an ancestor of REV), `command: python3 -I -B tools/mori-pressure.py --selftest`, `tool_blob: <oid>` equal to the blob of `tools/mori-pressure.py` at R and at REV, `fixtures_tree: <oid>` equal to the tree `tools/fixtures/mori-pressure` at R and at REV, `exit: 0`; the body after the header contains the line `MORI_PRESSURE_SELFTEST: PASS 12/12` and a line starting `MATCHER: rejected 48/48`. Optional `--rerun` re-executes R's tool from a temporary extract and reports whether the body is byte-equal; it is reported, never needed for `held` |
| D2 | the entry's own banner (`system-pressure-r24.md:11`, "this section wins") and the round-24 report say the six statements were corrected | over the entry text with `*`, `_` and backticks removed, case folded and all whitespace runs folded to one space: exactly one heading starting `## corrections`; headings `## facts` and `## decision table` both present; the decision table has at least as many data rows as at `28b79d3d`; outside the corrections section, 0 matches of `refreshed on (each|every) read`, `spike[^|.]{0,60}(is|are|can be|may be) invisible` and `null[^|.]{0,15}means[^|.]{0,15}undefined`; outside it, both `only when the next` (K5) and `not tracked` (P3) occur; inside it, a line contains `(k4)` and `total` |
| D3 | `SCORECARD.md:1521` says the supplementary file passes `PASS 7/7`; `corpus/lessons/round-24.md:79-80` says S01–S06, `PASS 6/6` | with n = cases in `tools/fixtures/mori-pressure/supplementary-cases.json` at `4f05dd5a` (7): `corpus/lessons/round-24.md` at REV has one line containing `Correction`, `S07`, `PASS 7/7` not followed by a digit, and a 7–40 hex token naming a commit at which that file has n cases |

**D4 is reported as a hygiene row, not counted:** held when `.gitignore` at REV has a line that is exactly one
of `__pycache__/`, `__pycache__`, `**/__pycache__/`, `tools/__pycache__/`, `*.pyc`, `*.py[cod]`; no `.gitignore`
in the REV tree has a `!` line mentioning `pycache` or `.py`; and no tracked path under `tools/` contains
`__pycache__` or ends `.pyc`.

Output: `schema: mori-routed-r24-v1`, `items: 3`, `held`, `mismatches`, per-item rows, `hygiene: {id: D4, held,
reasons}`. Exit 0 only when `mismatches` is 0 and hygiene holds; 1 otherwise; 2 when the repo or revision
cannot be read. The tool writes nothing outside a temporary directory it creates and removes (only `--rerun`
uses one).

- **Before (re-derived by wave-1 PlanDataWalk at `28b79d3d`):** all three counted items red, `mismatches: 3`;
  D4 hygiene red.
- **Declared after (replaces the original C1 after-value):** `python3 -I -B tools/mori-routed-r24.py --repo
  <lane> --rev <landed tip>` prints `"mismatches": 0` with `"held": 3` of `"items": 3` and hygiene held, exit 0.

**Committed evidence for both after-values (CriticSizing F1).** Each lands as a file under
`.ufo/waves/round-25/evidence/` with header lines `revision:` (full hash), `command:`, `exit:`, then the full
stdout: `routed-r24-after.txt` for C1 and `runway-selftest.txt` for C2, written after the last change to the
measured tool. The C2 cases blob is pinned: `tools/fixtures/mori-job-runway/cases.json` =
`48df844a` at `7634be75`. `pressure-selftest.txt` lands after the last change to the pressure tool and fixtures
(CriticSizing F2).

**Wording (F6).** C2's tool and selftest write nothing outside a fresh temporary directory they create and
remove. The seat-gate ledger line in each attempt row is a copy of a mutable, uncommitted harness file; it is
evidence of the grant time, not a pinned record.

## Amendment A2 (10:22Z, before any change to the landed C2 tool `09f55b62`; wave-1 seat CriticC2Rules)

Finding: none of the 21 frozen expected values is wrong under rules 1–7, but eleven YAML forms make the landed
tool report a number omp does not use (exit 0) or `set` for a file omp refuses to load (tested by the seat
against Bun 1.4.3, the parser the binary embeds). The tool must abstain on forms it cannot read the way omp
does. Rule 1 gains these `malformed` conditions; none changes a frozen J case:

- more than one top-level line whose key, after removing quotes and spaces before the colon, is `async`
  (a second `async:` block, `"async":`, `async :`); a top-level `<<:` merge key or a `? ` complex key anywhere;
- inside the async block, a direct child whose key, after removing quotes, is `maxJobs` but is not written
  exactly `maxJobs:`, or a `<<:` / `? ` line;
- a tab character in the indentation of any line of the async block; a `---` or `...` document marker line
  anywhere in the file;
- a `maxJobs` value with a `#` not preceded by whitespace, or a value opening a quote or a block scalar.

A leading UTF-8 byte-order mark is removed before parsing. The selftest still loads only the frozen 21
cases by default; these forms are tested by a co-evolved file `tools/fixtures/mori-job-runway/
supplementary-cases.json` (loaded with `--cases PATH`), which is not counted toward the after-value. Values
omp itself accepts but the tool abstains on (non-integers, `abc` falling back to 100, duplicates and flow
mappings that Bun reads) stay abstentions: `RUNWAY_UNKNOWN` is never a false number.

Scope wording (CriticC2Rules, CriticLearningClaim): the cap is per root omp session — one job manager is built
when a session has no parent task prefix, and its subagents share it — not per host. The tool reads one file,
not `config.yaml` fallbacks, project `.omp/config.yml`, `--config`/`PI_CONFIG_FILES` overlays, profiles or
runtime overrides; `RUNWAY_DEFAULT`/`RUNWAY_AS_CONFIGURED` describe that file only.

## Amendment A3 (before the C1 tool lands; wave-1 seat ReviewContractAgainstSpotcheck H1, H2)

- **D1 body is exact, not contained.** After the five header lines the body must be byte-equal to
  `MORI_PRESSURE_SELFTEST: PASS 12/12\nMATCHER: rejected 48/48 corrupted expectations\n`, the two lines
  `SCORECARD.md:1514` claims; any extra line (a FAIL, a traceback) leaves D1 unheld.
- **D2 also requires the banner gone.** Outside the corrections section, 0 matches of `this section wins`
  (normalized text); the routed fix is in place, so precedence by banner is no longer claimed.
- Not counted, disclosed: the reviewer found decision-table rows (173, 176, 177 at `28b79d3d`) that also lag
  the corrections (K3 version scope, P4 causes). The round fixes them in the same edit; the predicate does not
  test them, and the sibling-file sweep of `corpus/README.md` and `SKILL.md` is reported, not counted.

## Amendment A4 (records a deviation found while building; lands with the C1 tool, before the after-value is measured)

A3's banner clause tests `this section wins` outside the corrections section, but at `28b79d3d` the banner sits
inside it (`system-pressure-r24.md:11`, heading at line 8), so the clause as written could not tell a fixed entry
from an unfixed one. The landed tool (`e54b644b`) gates on the phrase being absent from the whole normalized entry
and reports both counts. This is stricter than A3's letter, changes no before-value (D2 is red at `28b79d3d` on
seven sub-reasons either way) and no declared after-value.
