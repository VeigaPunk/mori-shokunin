# RevPinCheckCode — review of `tools/mori-pin-check.py` (mori round 47, wave w1)

2026-10-25 · leaf seat, no subagents.

## Target and method

- Reviewed bytes: **frozen** `tools/mori-pin-check.py` sha256
  `e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1` — verified equal to the
  blob at freeze commit `63eecf2738db96f46b0bd02b1b2dfd66787493d0` at review start.
- **Mid-review byte flip:** while I was testing, another seat's uncommitted edit changed the
  working-tree tool to sha256 `86e25de804214233b49d75825cd9478de91f7da4c4b09b8c15ad707a0d04f105`
  (`git status`: ` M tools/mori-pin-check.py`, 111 insertions / 15 deletions vs frozen; adds
  `rebound=`/`duplicate=` counters, a `PY_FLAGS` strip, an exact-equality matcher, and extends
  selftest to 595 lines). Per the frozen contract the claim is measured with
  `git show <freeze>:<path>`, so **all line numbers and receipts below are from the frozen
  bytes**, extracted to `.scratch/r47-RevPinCheckCode/bin/mori-pin-check.py` (sha re-verified).
  Where known, I note whether the in-flight edit already touches a finding.
- Runtime: Python 3.14.8 (Arch host). Working-tree `SKILL.md` is also dirty (` M`, sha
  `86aa99ab…` vs committed `74ef3efa…` at both entering `2d85e33` and HEAD) — the C1 fix is
  in progress there; my real-registry parses below state which bytes they read.
- No tools installed or upgraded; pacman untouched. Only read-only git
  (`show`/`diff`/`status`/`rev-parse`). All fixtures under
  `.scratch/r47-RevPinCheckCode/` (lane tool runs with `TMPDIR` set there).

## Selftest receipt (frozen bytes)

```
$ TMPDIR=.scratch/r47-RevPinCheckCode python3 .scratch/r47-RevPinCheckCode/bin/mori-pin-check.py --selftest
… 22 case lines, all PASS …
PIN_CHECK_SELFTEST pass=22 fail=0        rc=0   (~5.5 s)
```

## Real-registry reconciliation (parse-only, rev substituted; no selftests executed)

Importing the frozen module and running `parse_registry` + `pin_commands` over SKILL.md bytes:

| bytes | tally pins | no_command | digest pins |
|---|---|---|---|
| entering `2d85e33` (`git show`) | 26 | 0 | 5 |
| committed HEAD `63eecf2` (identical SKILL.md) | 26 | 0 | 5 |
| working tree (dirty, mid-fix) | 28 | 0 | 5 |

This matches the committed receipt
`.ufo/waves/round-47/evidence/control-c1-donothing.txt` exactly (`PIN_CHECK=unmet
tally_pins=26 digest_pins=5 mismatches=1 unparsed=0 no_command=0 dropped=0 … rc=1`, the one
mismatch being `SKILL.md:912` `MORI_SOURCES_APPENDONLY_SELFTEST` pinned `pass=15 fail=0`,
observed `pass=22 fail=0`). The receipt also confirms two behaviors I could not otherwise
exercise on real data: `<rev>` substitution injects the measured sha into derived commands
(`cmd='python3 .ufo/waves/round-40/conform.py 2d85e33… --selftest'`), and mutant pins bound to
bare `.py` spans run the mutant with `rc=1` and match because their text lacks `fail=0`.

## Findings (severity order; line numbers = frozen bytes)

### M1 — stale-echo decoy defeats freshness: last-line-wins over prefix-substring lines

`check()` picks `seen[-1]` — the **last** output line merely *containing* the prefix — and
reads the text after its first occurrence (lines 255–256):

```python
seen = [l for l in text_out.splitlines() if prefix in l]
observed = seen[-1].split(prefix, 1)[1] if seen else None
```

A tool that echoes a historical tally after its live line (compat banners, regression
"previous run:" prints — the exact stale-receipt class round 46 was burned by, at row
granularity) makes a stale pin measure **met**. Reproducer (frozen bytes, fixture tree
`.scratch/r47-RevPinCheckCode/repro`, `tools/decoy.py`):

```python
print('FOO_SELFTEST pass=4 fail=0')        # live tally
print('compat: FOO_SELFTEST pass=3 fail=0')  # stale echo, printed last
```

Row: `` `python3 tools/decoy.py --selftest` → `FOO_SELFTEST pass=3 fail=0` ``

```
$ …/bin/mori-pin-check.py --root …/repro --skill …/repro/D_decoy_last_line.md --min-tally-pins 1
pin line=3 kind=tally prefix=FOO_SELFTEST state=match pinned='pass=3 fail=0' observed='pass=3 fail=0' rc=0 cmd='python3 tools/decoy.py --selftest'
PIN_CHECK=met tally_pins=1 … mismatches=0 …        rc=0
```

False green, rc 0. The docstring (lines 32–33) documents "the last output line containing the
prefix", so it is spec-conformant — but the spec is the defect: the pinned text should be
required on the *fresh* tally line, not the last mention. **In-flight edit: still open**
(`seen[-1]` unchanged at working-tree line 334).

### M2 — token-boundary lookahead excludes `_` → decorated tallies match weakened pins

Line 261: `re.match(re.escape(want) + r"(?![0-9A-Za-z])", observed.strip())`. The digit case
(`pass=2` vs `pass=22`, control-c1-truncated) is closed, but `_` passes the lookahead.
Repro (`tools/draft.py` prints `FOO_SELFTEST pass=3 fail=0_draft`, rc 0; pin `… pass=3 fail=0`):

```
pin line=3 … state=match pinned='pass=3 fail=0' observed='pass=3 fail=0_draft' rc=0
PIN_CHECK=met … rc=0
```

False green, rc 0. Fix: `(?![0-9A-Za-z_])`. **In-flight edit: apparently closed** — the
matcher became `observed.strip() == want` (working line 338); that swap is UNVERIFIED by me
against the in-flight selftest, and it also changes semantics for legitimately partial pins.

### M3 — no GFM structural awareness: fenced example tables are measured as a registry

`parse_registry` (lines 89–107) scans every `|`-opening line of the whole file: no code-fence
state, and `header` resets only on a non-`|` line (96–97), so a later table's header row
becomes a data row of the previous self-test table when no blank line separates them.
Repro (no real table in the file, only a ```markdown fence containing a complete gate table):

- honest example row → `PIN_CHECK=met tally_pins=1 … rc=0` — **fenced documentation rows
  satisfy the tally floor**;
- example row pinned `pass=9` → `state=mismatch mismatches=1 … rc=1` — **a doc example alone
  flips the verdict red**.

Latent today: SKILL.md contains zero ``` fences (grep receipt: no matches) and all tables are
blank-line separated. **In-flight edit: not addressed** (no fence handling in the diff).

### L1 — bare `--selftest` derivation hardcodes the entry cell at index 2

Line 157: `entry_spans = SPAN_RE.findall(cells[2] …)` — the header is never consulted for the
entry column. Repro (header `| name | entry | self-test | pinned |`, entry at index 1, bare
`--selftest` in the self-test cell):

```
pin line=3 kind=tally prefix=FOO_SELFTEST state=no_command
PIN_CHECK=unmet tally_pins=1 … no_command=1 …    rc=1
```

(the derivation reads the self-test cell itself, finds the bare flag, and yields None). Latent:
all eight gate tables place `entry` at index 2 (headers at SKILL.md 162, 543, 607, 662, 737,
815, 900, 923 — verified). **In-flight edit: not addressed** (no `cells[2]` change).

### L2 — GFM `\\|` (escaped backslash, then a real separator) is mis-split

Line 77 `re.split(r"(?<!\\)\|", s)` treats a separator preceded by the second backslash of a
`\\` escape as escaped. Repro row `| foo | gate | a\\| \`python3 tools/foo.py --selftest\` →
\`FOO_SELFTEST pass=3 fail=0\` | none | none | mori |` is well-formed 8-cell GFM (cell 3 = `a\`)
but measures:

```
pin line=3 kind=row state=unparsed cells=6 header=8
PIN_CHECK=unmet … unparsed=1 …                   rc=1     (false red)
```

Latent: no `\\|` anywhere in SKILL.md (grep receipt: no matches). Single `\|` is handled
correctly (see non-defects).

### L3 — bare-flag derivation truncates at interpreter flags → false red

Lines 165–167 break at the first `-`-word, so entry `` `python3 -u tools/foo.py` `` with a
bare `--selftest` pin derives `python3 --selftest` (rc 2, no output):

```
pin line=3 … state=mismatch pinned='pass=3 fail=0' observed=None rc=2 cmd='python3 --selftest'
PIN_CHECK=unmet … mismatches=1 …                 rc=1
```

Latent: direct command spans keep their flags (receipt rows `python3 -I`/`python3 -I -B`
measured fine), and today's bare-flag rows (SKILL.md 905, 911, 912) derive from flagless
prefixes. **In-flight edit: addressed** — a `PY_FLAGS` strip was added (UNVERIFIED by me).

### L4 — a pin not at the start of its span is silently skipped (no pin line at all)

Line 131 `re.match(r"([A-Z][A-Z0-9_]*SELFTEST)(.*)$", span)` requires the prefix at span
start; a span like `` `run: FOO_SELFTEST pass=3 fail=0` `` binds nothing, is not a command, and
produces **no diagnostic** — only the tally floor notices. Repro: `tally_pins=0`, zero `pin`
lines, `PIN_CHECK=unmet … rc=1` purely via `min_tally_pins=1`. With the C1 floor at 26 a few
such pins would erode the floor invisibly while everything else stays green; `pin_keys`
(baseline, line 202) uses the same regex, so baseline `dropped` does not catch them either.
Entering registry has zero such spans (parse receipt above).

### L5 — setup-class failures exit 1 with a traceback instead of the documented 2

Docstring line 49 and SKILL.md:925 promise exit 2 for setup; uncaught-exception paths break
it: `run_cmd`'s `makedirs`/`mkdtemp` (187–188), `export_rev`'s `os.mkdir`/`tarfile`/
`extractall` (310–312, also TypeError on pre-3.12 Pythons lacking the `filter` backport), and
`main`'s `makedirs` (337). Repro:

```
$ …/bin/mori-pin-check.py --rev HEAD --repo /nonexistent-r47-revpincheck
…Traceback … PermissionError: [Errno 13] Permission denied: '/nonexistent-r47-revpincheck'
rc=1   (documented contract: 2)
```

### L6 — design notes, no current false verdict

- Any bare `.py`/`.sh` span inside a self-test cell becomes the binding command for later pins
  (111–118, 135–137). Live example: SKILL.md:912's prose span `` `tools/mori-pin-check.py` `` —
  harmless while it trails the row's only pin; a silent rebind if a second pin ever follows it.
- `REV_WORDS` includes bare `REV` (line 69); in `--root` mode (`rev=None`, line 168) it stays
  literal, and `<rev>` rows measure `no_command` there by design.
- `strip_env` (141–144) silently drops leading `VAR=value` words — documented, but a pin whose
  selftest behaves differently without that env measures the no-env behavior.

### L7 — dead weight / unchecked limits

- `scratch` parameters of `run_cmd` (183) and `check` (221) are unused — dead plumbing.
- Digest `PATH_RE` extension whitelist `py|sh|json|md|txt|tsv` (67): a digest row naming only
  other extensions (`.jsonl`, `.c`, …) always mismatches (fails safe); not in the contract's
  named limits.
- `git archive` honors `export-ignore`; the lane has no `.gitattributes` (verified absent), so
  the committed-bytes equivalence holds today.

## Verified non-defects

- Single `\|` splitting matches GFM and command argv: cells keep `\|`, `shlex` unescapes in
  command spans (selftest `escaped_pipe_cell` PASS; receipt rows containing `\|` — SKILL.md
  739, 925 — parsed and ran).
- Digit token boundary `pass=2` vs `pass=22` closed (selftest `token_boundary_truncated_pin`).
- `fail=0` rc arm (selftest `nonzero_rc_with_fail0`; receipt L190/L192 mutant pins rc 1
  without `fail=0` correctly matched).
- `<rev>` → measured-sha substitution (receipt `cmd=` fields for SKILL.md 911/912).
- Baseline multiset `dropped` accounting (selftest `baseline_row_deleted`; entering receipt
  `dropped=0`).
- TMPDIR under the measured tree with per-run removal (selftest
  `tmpdir_inside_measured_tree`; no leftover `pin-check-*`/`pin-tmp-*` dirs after my runs).
- Exit codes 0/1/2 on the documented happy paths (selftest `cli_met_rc0`, `cli_bad_rev_rc2`).

## Residual risk and verification gaps

- I did not execute the C1 claim command against the real registry; real-row match/mismatch
  statements are parse-level plus the committed receipt — the measurement seat owns the live
  run (and the SKILL.md fix is uncommitted as of this review).
- `git archive` edges (symlinks, submodule paths) untested; `tarfile` `filter="data"` needs
  the ≥3.12 backport (host 3.14.8 — fine here, untested elsewhere).
- The in-flight rewrite was diffed only for overlap; only M2 (apparently closed) and M1
  (`seen[-1]` still present) were cross-checked against it.
- If the freeze sha changes again, every receipt above must be re-run against the new frozen
  bytes.

Repro fixture tree preserved at `.scratch/r47-RevPinCheckCode/repro/` (cases A, B,
`C_underscore_boundary`, `D_decoy_last_line`, `E2_pin_words_inside_span`,
`F_gfm_double_backslash_pipe`, `H_fence_credit`, `H_fence_stale`, plus `tools/{foo,draft,decoy}.py`).
