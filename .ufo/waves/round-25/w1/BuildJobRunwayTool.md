# BuildJobRunwayTool — round 25, claim C2 (harness background-job runway)

Seat: `MoriR25.BuildJobRunwayTool` (executor). Claim C2, contract
`.ufo/waves/round-25/contract.md` rules 1–7. Scope of this seat: the tool only.
The C2 knowledge entry (`corpus/knowledge/harness-job-capacity-r25.md`), the
upstream-source rows and the live evidence file belong to other seats.

## Files changed

| Path | Where | Note |
|---|---|---|
| `tools/mori-job-runway.py` | sandbox clone `/fast/scratch/hyaku/mori-r25/wt-runway` (branch `r25-wt-runway`) | new file, committed (`9cb0dc3`, pre-A2; the lane copy landed as `09f55b62`), then the A2 abstentions in `2b9223f` on top of lane `6a92d5ee` |
| `tools/fixtures/mori-job-runway/supplementary-cases.json` | sandbox clone `/fast/scratch/hyaku/mori-r25/wt-runway` | new file (A2 co-evolved cases R01–R18), committed in `2b9223f` |
| `.ufo/waves/round-25/w1/BuildJobRunwayTool.md` | lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin` | this report |

Nothing else was written. `tools/fixtures/mori-job-runway/cases.json` was **not**
touched (frozen): identical sha256 `7098b008d614e84c4328af96d15badef700ea84b75a43ba4a375264a01755fb4`
in lane and sandbox, and `git log -- tools/fixtures/mori-job-runway/cases.json`
in the sandbox shows only the freeze commit `7634be7`.

## Final artefact

* File path (sandbox): `/fast/scratch/hyaku/mori-r25/wt-runway/tools/mori-job-runway.py`
* sha256 of the file: `08217582fdad69cf224bfc63d289c85196a96f3ee63ac10690eb4344cfbffe69`
* sha256 of the committed blob `git show HEAD:tools/mori-job-runway.py`: identical
  (`08217582fdad69cf224bfc63d289c85196a96f3ee63ac10690eb4344cfbffe69`) — the
  working tree is clean (`git status --short` empty).
* Sandbox commit: `9cb0dc3c4f04e9e35ccfb00912fcd70f0fd806fa`
  ("round-25 C2: add read-only tools/mori-job-runway.py (harness background-job runway)"),
  parent `7634be75c74891b5cd2815d0bd5374f89abd7087`. Not pushed (the sandbox's
  `origin` is the lane repo; lane mutation is out of bounds for a seat).

## Behaviour implemented (contract C2 rules 1–7)

* Python 3 standard library only (`argparse, errno, hashlib, json, mmap, os, re,
  shutil, sys, tempfile`), `#!/usr/bin/env python3`, runs under `python3 -I -B`.
* Read-only: reads one config file and one binary; never runs `omp`, never edits
  settings, never writes outside the `--selftest` temporary directories.
  `~/.omp/agent/config.yml`, `~/.omp/agent/mcp.json` and OMP settings were only
  read, never edited.
* Rule 1 `configured`: column-0 `async:` (optional trailing `# comment`) opens a
  block ending at the next non-blank, non-comment line at column 0; direct
  children are the lines at the indentation of the block's first non-blank,
  non-comment line; deeper lines ignored. States `set` / `malformed` / `absent` /
  `unreadable` exactly as worded (inline `async: {maxJobs: 50}` → `malformed`;
  duplicate direct `maxJobs` → `malformed`; directory → `unreadable`).
* Rule 2 `clamp`: `mmap` + `re` over the raw binary bytes with the contracted
  pattern; `found` (+`sites`), `ambiguous` (differing numbers), `absent` (no
  match — never read as "no clamp"), `unreadable` (binary cannot be read).
* Rule 3 `setting_default`: same pattern family
  `id:\s*"async\.maxJobs",[^}]{0,300}?default:\s*(\d+)`, same states.
* Rule 4 `effective`: null unless the clamp is `found` and (configured `set`, or
  configured `absent` and default `found`); then `max(1, min(clamp, base))`.
* Rule 5 verdict/exit: `RUNWAY_UNKNOWN`/2, `RUNWAY_CLAMPED`/1,
  `RUNWAY_AS_CONFIGURED`/0, `RUNWAY_DEFAULT`/0; usage errors exit 2 (argparse
  exits 2 — verified below).
* Rule 6 output: one JSON object, `schema: mori-job-runway-v1`, `config_path`,
  `binary_path`, `binary_sha256` (null when unreadable), `configured {state,
  value}`, `clamp {state, value, sites}`, `setting_default {state, value,
  sites}`, `effective`, `verdict`.
* Rule 7 `--selftest`: resolves `tools/fixtures/mori-job-runway/cases.json`
  from the script's own path, materialises each case in a fresh
  `tempfile.TemporaryDirectory` (`config: null` → no file; `config: {"dir":
  true}` → a directory at that path; `binary` written as UTF-8), runs the same
  `evaluate()` used by the live path, and compares **only the keys present in
  `expect`** (recursive subset compare, per the fixture's own `note`). Prints
  `MORI_JOB_RUNWAY_SELFTEST: PASS n/N` or `FAIL n/N` plus one line per failing
  case; exit 0 only when all pass.

## Retained evidence (commands and outputs, run in the sandbox)

### 1. Selftest (declared after-value)

```
$ cd /fast/scratch/hyaku/mori-r25/wt-runway
$ python3 -I -B tools/mori-job-runway.py --selftest
MORI_JOB_RUNWAY_SELFTEST: PASS 21/21
EXIT=0
```

### 2. Live run against this host

```
$ python3 -I -B tools/mori-job-runway.py
{
  "schema": "mori-job-runway-v1",
  "config_path": "/home/vgpnk/.omp/agent/config.yml",
  "binary_path": "/home/vgpnk/.local/bin/omp",
  "binary_sha256": "85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4",
  "configured": {
    "state": "set",
    "value": 200
  },
  "clamp": {
    "state": "found",
    "value": 100,
    "sites": 1
  },
  "setting_default": {
    "state": "found",
    "value": 100,
    "sites": 1
  },
  "effective": 100,
  "verdict": "RUNWAY_CLAMPED"
}
EXIT=1
```

### 3. Head and file hashes at the committed tip

```
$ git -C /fast/scratch/hyaku/mori-r25/wt-runway rev-parse HEAD
9cb0dc3c4f04e9e35ccfb00912fcd70f0fd806fa
$ sha256sum tools/mori-job-runway.py
08217582fdad69cf224bfc63d289c85196a96f3ee63ac10690eb4344cfbffe69  tools/mori-job-runway.py
$ git show HEAD:tools/mori-job-runway.py | sha256sum
08217582fdad69cf224bfc63d289c85196a96f3ee63ac10690eb4344cfbffe69  -
$ git status --short
(no output)
```

### 4. Live facts the tool re-derives (independent byte read, same host)

```
$ ls -la ~/.omp/agent/config.yml ~/.local/bin/omp
-rwxr-xr-x 1 vgpnk vgpnk 256702432 Oct 21 20:37 /home/vgpnk/.local/bin/omp
-rw------- 1 vgpnk vgpnk      7098 Oct 22 05:01 /home/vgpnk/.omp/agent/config.yml
$ grep -n 'async:' -A1 ~/.omp/agent/config.yml
async:
  maxJobs: 200
```
Byte search of the binary with the two contracted patterns (mmap + re, read-only):
clamp sites `1` → `100`; `async.maxJobs` default sites `1` → `100`. The tool's
live output agrees with the contract's L1 byte search
(`maxRunningJobs: () => Math.min(100, XPe.get(R))` once; `async.maxJobs` with
`default: 100` once).

### 5. Edge probes (beyond the frozen cases, run in the sandbox)

| Probe | Observed |
|---|---|
| tab-indented `async:` block, `maxJobs: 7` | `configured {set, 7}`, effective 7, `RUNWAY_AS_CONFIGURED` |
| `maxJobs: "50"` (quoted) | `configured {malformed, null}`, effective null, `RUNWAY_UNKNOWN` |
| `maxJobs: -1` | `configured {set, -1}`, effective 1 (floor), `RUNWAY_CLAMPED` |
| `--binary` pointing at a missing path | `clamp {unreadable, null, 0}`, `setting_default {unreadable, null, 0}`, `binary_sha256 null`, effective null, `RUNWAY_UNKNOWN` |
| `--binary` pointing at a directory | `clamp {unreadable, null, 0}`, `RUNWAY_UNKNOWN` |
| `--config` pointing at a directory | `configured {unreadable, null}`, effective null, `RUNWAY_UNKNOWN` |
| `--bogus` (unknown flag) | exit 2 |

## Frozen-case review (read-only; `cases.json` unchanged)

All 21 cases J01–J21 pass as frozen. I found **no case that contradicts the
contract text**; two readings of the contract that the cases do pin down are
recorded here so the integrator does not re-derive them:

1. **Rule 5 precedence.** The contract lists "configured `absent` → `RUNWAY_DEFAULT`"
   after the "effective null → `RUNWAY_UNKNOWN`" clause. J14 (config absent,
   no setting default in the binary, clamp found) expects `RUNWAY_UNKNOWN`/2, so
   the effective-null clause must be evaluated **first**. The tool implements
   that order. J05/J06/J04/J13/J19 (configured absent, default found) still land
   on `RUNWAY_DEFAULT`/0.
2. **`setting_default` only matters when configured is absent.** J21 has an
   ambiguous default (100 and 50) but a configured value of 200 → effective 100
   and `RUNWAY_CLAMPED`; the ambiguous default does not poison the result.

Points the contract leaves open, resolved by the tool and documented in its
docstring (no case depends on them):

* A signed integer (`-1`, `+7`) is accepted as an "unquoted decimal integer";
  the value is then floored by rule 4's `max(1, …)`.
* More than one column-0 `async:` line: the first block is used; any `async:`
  line that carries an inline value makes the configuration `malformed`.
* `sites` is always emitted for `clamp` and `setting_default` (0 when
  unreadable/absent), per rule 6's `{state, value, sites}` shape.
* A missing binary file is `unreadable` (the contract's `absent` for the clamp
  means "no match in the bytes", not "no file").
* `configured` `malformed`/`unreadable` reach rule 4 as "not set and not
  absent" → effective null → `RUNWAY_UNKNOWN`/2 (J07, J08, J16, J20).

## Risks and blockers

* **No blocker.** The declared after-value holds: `python3 -I -B
  tools/mori-job-runway.py --selftest` prints `MORI_JOB_RUNWAY_SELFTEST: PASS
  21/21`, exit 0, over the committed frozen cases.
* The live run exits **1** by design (configured 200 vs clamp 100 →
  `RUNWAY_CLAMPED`). A gate that treats a non-zero exit as a tool failure would
  misread it; the contract fixes exit 1 for this verdict.
* The config reader is a line-grammar approximation of YAML, as the contract
  specifies ("Find a line exactly `async:`"); it does not implement YAML
  anchors, multi-line scalars or flow mappings beyond the contracted inline
  `async:` → `malformed` rule.
* The binary scan reads the whole file through `mmap`; the installed binary is
  256,702,432 bytes and the scan takes well under a second (the live run
  completed inside the sandbox in ~1 s including interpreter start-up).
* `AGENTS.md` in the lane asks for a `LOG.md` entry with every change. I did
  **not** append one: `LOG.md` is a repo-wide artefact owned by the integrator
  and concurrent seats are landing in the same round, so appending it from the
  sandbox would collide on cherry-pick. Suggested line for the L1:
  "round-25 C2: added read-only `tools/mori-job-runway.py`; selftest PASS 21/21
  over the frozen cases; live run on this host: configured 200, clamp 100 →
  `RUNWAY_CLAMPED` (exit 1)."
* Not done here (other seats): the C2 knowledge entry with the `SOURCES.md`
  rows, the upstream oh-my-pi source citations, and the committed live-run
  evidence file. The tool's evidence base is the installed binary's bytes only.

## A2 — contract amendment A2 (lane commit `6a92d5ee`)

Amendment A2 (contract `.ufo/waves/round-25/contract.md`, section
"Amendment A2 (10:22Z, before any change to the landed C2 tool `09f55b62`;
wave-1 seat CriticC2Rules)") adds abstentions to rule 1 and asks for a
co-evolved supplementary case file. The L1 relayed the follow-up; the findings
behind it are in `.ufo/waves/round-25/w1/CriticC2Rules.md` (11 YAML forms, F4).

### Branch and base

The sandbox branch was rebuilt on the lane tip carrying A2:

```
$ git fetch origin
$ git branch backup/r25-runway-preA2 9cb0dc3        # the pre-A2 sandbox commit
$ git checkout -B r25-wt-runway 6a92d5ee           # lane commit with A2
$ git log --oneline -3
2b9223f round-25 C2: A2 abstentions in tools/mori-job-runway.py (BOM, YAML forms) plus co-evolved supplementary cases
6a92d5e round-25: contract amendment A2 (C2 abstains on YAML forms omp reads differently) before the tool changes
51ddd01 round-25: contract amendment A1 (C1 counted items tied to self-assessments, hardened predicates, D4 hygiene row, committed evidence) before the C1 tool lands
```

The lane's copy of the tool (landed as `09f55b62`) was byte-identical to my
pre-A2 sandbox commit (`08217582fdad69cf224bfc63d289c85196a96f3ee63ac10690eb4344cfbffe69`
for both), so the A2 work is a clean single commit on top of `6a92d5ee`.

### What changed in `tools/mori-job-runway.py`

A2 conditions, all of them abstentions (`configured {malformed, null}` →
`effective: null` → `RUNWAY_UNKNOWN`, exit 2), never a number:

1. more than one top-level line whose key, once quotes and the spaces before
   the colon are removed, is `async` (a second `async:` block, `"async":`,
   `async :`);
2. a top-level `<<:` merge key or a `? ` complex key anywhere in the file;
3. inside the async block, a direct child whose key, once quotes are removed,
   is `maxJobs` but is not written exactly `maxJobs:` (covers `"maxJobs":`,
   `maxJobs :`, `maxJobs:200`), or a `<<:` / `? ` line;
4. a tab character in the indentation of any line of the async block;
5. a `---` or `...` document marker line anywhere in the file;
6. a `maxJobs` value whose `#` is not preceded by whitespace (a `#` preceded by
   whitespace still opens a comment), or a value opening a quote or a block
   scalar;
7. a quoted scalar that spans lines or never closes (the line it hides is not
   a key, and the file is one the tool cannot read the way omp reads it);
8. a leading UTF-8 byte-order mark is removed before parsing (the only A2 form
   that is *not* an abstention: the file is then read normally).

Implementation notes: the `? `/`<<:`/document-marker/duplicate-`async` checks
run over the whole file before the block is parsed; a line that belongs to a
multi-line quoted scalar is excluded from the top-level key scan and from the
direct-child scan; the `#` rule now only cuts a comment at a `#` that is at the
start of the value or preceded by whitespace.

### New CLI option

`--cases PATH` selects the case file for `--selftest`; without it the frozen
21 cases are loaded from the script's own path (unchanged default). Using
`--cases` without `--selftest` is a usage error (exit 2), mirroring
`tools/mori-pressure.py`.

### New fixture

`tools/fixtures/mori-job-runway/supplementary-cases.json` — same schema as the
frozen file (`mori-job-runway-cases-v1`), ids `R01`–`R18`, one case per A2
form (the 11 forms of `CriticC2Rules.md` F4 are R01–R11) plus seven guards.
It is co-evolved with the tool and is **not** counted toward the after-value.
`tools/fixtures/mori-job-runway/cases.json` was not touched: sha256
`7098b008d614e84c4328af96d15badef700ea84b75a43ba4a375264a01755fb4`, and
`git log -- tools/fixtures/mori-job-runway/cases.json` still shows only the
freeze commit `7634be7`.

| id | form | expected | tool |
|---|---|---|---|
| R01 | `"async":` key | malformed / RUNWAY_UNKNOWN | malformed, exit 2 |
| R02 | `async :` key | malformed / RUNWAY_UNKNOWN | malformed, exit 2 |
| R03 | leading BOM | normal value (set 50, effective 50) | set 50, `RUNWAY_AS_CONFIGURED`, exit 0 |
| R04 | `"maxJobs":` child | malformed / RUNWAY_UNKNOWN | malformed, exit 2 |
| R05 | `<<: *d` merge key in the block | malformed / RUNWAY_UNKNOWN | malformed, exit 2 |
| R06 | `? maxJobs` explicit key | malformed / RUNWAY_UNKNOWN | malformed, exit 2 |
| R07 | two `async:` blocks | malformed / RUNWAY_UNKNOWN | malformed, exit 2 |
| R08 | `maxJobs: 50#x` | malformed / RUNWAY_UNKNOWN | malformed, exit 2 |
| R09 | `---` document marker | malformed / RUNWAY_UNKNOWN | malformed, exit 2 |
| R10 | tab indentation | malformed / RUNWAY_UNKNOWN | malformed, exit 2 |
| R11 | multi-line quoted scalar hiding `maxJobs` | malformed / RUNWAY_UNKNOWN | malformed, exit 2 |
| R12 | `...` end marker | malformed / RUNWAY_UNKNOWN | malformed, exit 2 |
| R13 | top-level `<<:` merge key | malformed / RUNWAY_UNKNOWN | malformed, exit 2 |
| R14 | top-level `? ` complex key | malformed / RUNWAY_UNKNOWN | malformed, exit 2 |
| R15 | quoted value `"50"` | malformed / RUNWAY_UNKNOWN | malformed, exit 2 |
| R16 | block-scalar value `|` | malformed / RUNWAY_UNKNOWN | malformed, exit 2 |
| R17 | guard: `maxJobs: 50 # raised` | normal value (set 50) | set 50, `RUNWAY_AS_CONFIGURED`, exit 0 |
| R18 | guard: inline `async: {maxJobs: 50}` | malformed / RUNWAY_UNKNOWN | malformed, exit 2 |

### Outputs at the committed A2 tip

```
$ git -C /fast/scratch/hyaku/mori-r25/wt-runway rev-parse HEAD
2b9223f5cccec728b9ca1245e559f3ac52b0c1e1

$ python3 -I -B tools/mori-job-runway.py --selftest
MORI_JOB_RUNWAY_SELFTEST: PASS 21/21
EXIT=0

$ python3 -I -B tools/mori-job-runway.py --selftest --cases tools/fixtures/mori-job-runway/supplementary-cases.json
MORI_JOB_RUNWAY_SELFTEST: PASS 18/18
EXIT=0

$ python3 -I -B tools/mori-job-runway.py
{
  "schema": "mori-job-runway-v1",
  "config_path": "/home/vgpnk/.omp/agent/config.yml",
  "binary_path": "/home/vgpnk/.local/bin/omp",
  "binary_sha256": "85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4",
  "configured": {
    "state": "set",
    "value": 200
  },
  "clamp": {
    "state": "found",
    "value": 100,
    "sites": 1
  },
  "setting_default": {
    "state": "found",
    "value": 100,
    "sites": 1
  },
  "effective": 100,
  "verdict": "RUNWAY_CLAMPED"
}
EXIT=1
```

The live run is unchanged: configured 200, clamp 100 → effective 100 →
`RUNWAY_CLAMPED` (exit 1), the same answer as before A2.

Other probes at the A2 tip: `--cases` without `--selftest` → usage error, exit
2; `--selftest --cases /tmp/nope.json` → `MORI_JOB_RUNWAY_SELFTEST: FAIL 0/0`
with the read error, exit 2.

### A2 artefact hashes

| artefact | sha256 |
|---|---|
| `tools/mori-job-runway.py` | `892fa5323adc10db5d23acf04778c0af832d9c02e66a276d45aa99f1ef71b623` |
| `tools/fixtures/mori-job-runway/supplementary-cases.json` | `8d09756d10a9f501b0fa69599e096ce6ef5f3cd9debda89b5de2bc094679ffd6` |
| committed blobs (`git show HEAD:<path> \| sha256sum`) | identical to both rows above |

Sandbox commit: `2b9223f5cccec728b9ca1245e559f3ac52b0c1e1`, parent `6a92d5ee`,
working tree clean, not pushed (the sandbox's `origin` is the lane repo).

### A2 risks

* Every A2 form is an abstention, so the tool can under-report a value omp
  would use (`"async":`, `async :`, a merge key, an explicit key). That is the
  safe direction A2 asks for (`RUNWAY_UNKNOWN` is never a false number), but
  the knowledge entry should say the tool abstains on these forms rather than
  claiming they have no value.
* Residual forms the line grammar still does not model, not in A2 and not in
  the 11 forms: a plain multi-line scalar (a folded continuation line) and a
  block scalar whose content the tool ignores. Both are reported `absent`
  (effective null or the default) rather than `malformed`; they were not
  changed because A2 does not list them and no frozen case covers them.
* The `? `/`<<:`/document-marker checks are file-wide, so a merge key or a
  complex key in an unrelated top-level block also makes the tool abstain. That
  is over-abstention in the safe direction.

## Tooling

No tool was installed or upgraded by this seat (no `pacman`, `uv tool`,
`cargo` or `npm` transaction). Interpreter used: system `python3`, version
`3.14.8` (`python3 -V`). Existing tooling only: `git` (sandbox clone) and the
coreutils `sha256sum`/`grep`/`ls` for the evidence above.

## Reproduction

```
git -C /fast/scratch/hyaku/mori-r25/wt-runway checkout 9cb0dc3c4f04e9e35ccfb00912fcd70f0fd806fa
cd /fast/scratch/hyaku/mori-r25/wt-runway
python3 -I -B tools/mori-job-runway.py --selftest   # PASS 21/21, exit 0
python3 -I -B tools/mori-job-runway.py               # RUNWAY_CLAMPED, exit 1
```
