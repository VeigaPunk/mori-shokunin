# Mo49ExecK2K8 — K2 (env-prefix substitution) and K8 (rc-free PASS pins) closed in a pin-reconciler copy

**Seat.** Mo49ExecK2K8 (executor, wave w1). Leaf seat: one read-only labrat slot not used; no subagent
dispatched, no tool installed or updated. **Lane.** `/home/vgpnk/Projects/shokunin/mori-shokunin`
(HEAD `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115`, the round-49 freeze commit). **Measured revision.**
`b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86` (entering tip). **Contract read:** `.ufo/waves/round-49/contract.md`.
**Class source.** `.ufo/waves/round-48/w2/R48CritV3Junk2.md` §K2, §K8.
**Report author date.** 2026-10-25 (lane HEAD `0df17b7b` at write time, i.e. after the freeze commit).

**Deliverable (scratch, not landed).** `.scratch/r49-Mo49ExecK2K8/mori-pin-check.py`,
sha256 `dc7a646187cb567413ef138ba302a2a4dafb64bcfc4b70553d866926c2ec3f28`, derived from the frozen
control `.ufo/waves/round-49/controls/tool-r48-merged-witness.py` (sha256
`c30ab6232893d984d1440784b6ce962d7c987c6d5538db0ead2f458a8ea1c9f0` = the freeze receipt in
`evidence/freeze-sha256.txt`; verified). Diff: `.scratch/r49-Mo49ExecK2K8/k2k8.diff`
(385 diff lines, 169 added / 40 removed, sha256 `f1d270cf2fd5bff1afcd33a6b8542a66954a4f07cd554366842e6515f084e332`).
The L1 integrates; this seat wrote no lane file except this report.

---

## 1. The two rules

Both rules are the smallest change that makes the tool run *the command the row writes* and refuse a
green it cannot justify. Neither is a reject-only rule: a rejection-only K2 would red an honest row that
needs the variable (arm `k2_env_applied_honest_pin` below is exactly that row, and it is met).

### K2 — the `VAR=value` prefix is applied, never dropped

`strip_env` pop'd the leading assignment words and `run_cmd` never saw them, so a span
`MORI_STRICT=1 python3 tools/x.py --selftest` was executed as `python3 tools/x.py --selftest` — a
different command from the one the row writes, and the pin was called a match.

* `split_env(words)` returns `({VAR: value}, argv)`; `derive_command` returns `(argv, env)`;
  `command_from_span` returns `(argv, env)`; `pin_commands` yields
  `(prefix, pinned, argv|None, env)` — the env travels with the binding, including the env written in
  the **entry cell** for the bare `--selftest` form (that route was open too: arm `k2_entry_cell_env`).
* `resolve_env(env, root)` is the one place where a shell is approximated: `$PWD`/`${PWD}` becomes the
  measured root (the command's cwd, so it means what a shell would mean, and it is the shape the lane's
  own three env-prefixed rows use). Any other shell reference or an angle-bracket placeholder cannot be
  reproduced without a shell; the binding is then `env_unexpanded` — a new **fatal** counter, reported
  per pin as `state=env_unexpanded variable=<VAR> cmd=…` and in the summary as `env_unexpanded=N`.
  Silently dropping such a prefix is what the class was.
* `run_cmd(..., extra_env)` applies the resolved assignments after its own defaults (a row's `TMPDIR`
  therefore wins over the private one).
* The command *including its assignments* is what the baseline comparison sees (`norm_cmd`), so changing
  or adding an assignment to a pinned command is a `rebound` exactly as changing its argv is, and the
  two-authority contract check keys on the rendered command (`render_cmd`).

### K8 — a PASS-form pin's exit code is checked

The old rule `if ok and re.search(r"\bfail=0\b", want) and rc != 0` left rc unconstrained for the five
landed PASS-form pins (`: PASS 12/12`, `: PASS 21/21`, `: PASS 32/32`, `: PASS (6 cases)`,
`: PASS (23 cases, 23 passed, 0 failed)`). A tool that prints the pinned text and exits 1 was green.

```python
if ok and rc != 0 and not re.search(r"\bfail=[1-9]\d*\b", want):
    ok = False
```

The exit code must be 0 unless the pinned text itself asserts a nonzero failure count. That keeps the
two legitimate mutant pins (`pass=15 fail=1` rc 1; `pass=17 fail=2` rc 1) met without a carve-out list —
measured, not assumed (§4).

Docstring updated in the same file: "How it measures" (assignments applied, `$PWD` meaning, the
`env_unexpanded` state; the exit-code rule for PASS-form pins) and "Output" (the summary line now ends
`… hidden=N misattributed=N env_unexpanded=N min_tally_pins=N rev=… baseline=…`).

---

## 2. Reproducers — both classes are green on the frozen control and red on the copy

Harness `.scratch/r49-Mo49ExecK2K8/repro-k2k8.py` builds a two-row synthetic tree and scores it with a
given tool (`--root`, `--min-tally-pins 1`, `TMPDIR` inside `.scratch/r49-Mo49ExecK2K8`). The row is the
critic's K2/K8 reproducer: the pinned text is what the command prints **without** the variable / with
exit 0, and the as-written run differs. Raw output: `.scratch/r49-Mo49ExecK2K8/isolate-k2k8.txt`.

```
--- k2-witness tool-r48-merged-witness.py rc=0
pin line=3 kind=tally prefix=E_SELFTEST state=match pinned='pass=3 fail=0' observed='pass=3 fail=0' rc=0 cmd='python3 tools/envtool.py --selftest'
PIN_CHECK=met tally_pins=1 … mismatches=0 …

--- k2-copy mori-pin-check.py rc=1
pin line=3 kind=tally prefix=E_SELFTEST state=mismatch pinned='pass=3 fail=0' observed='pass=2 fail=1' rc=1 cmd='MORI_STRICT=1 python3 tools/envtool.py --selftest'
PIN_CHECK=unmet tally_pins=1 … mismatches=1 … env_unexpanded=0 …

--- k8-witness tool-r48-merged-witness.py rc=0
pin line=3 kind=tally prefix=P_PASS_SELFTEST state=match pinned=': PASS (6 cases)' observed=': PASS (6 cases)' rc=1 cmd='python3 tools/passtool.py --selftest'
PIN_CHECK=met tally_pins=1 … mismatches=0 …

--- k8-copy mori-pin-check.py rc=1
pin line=3 kind=tally prefix=P_PASS_SELFTEST state=mismatch pinned=': PASS (6 cases)' observed=': PASS (6 cases)' rc=1 cmd='python3 tools/passtool.py --selftest'
PIN_CHECK=unmet tally_pins=1 … mismatches=1 … env_unexpanded=0 …
```

As-written truth printed by the same harness:

```
as-written MORI_STRICT=1 envtool.py --selftest -> rc=1 out='E_SELFTEST pass=2 fail=1'
as-written passtool.py --selftest -> rc=1 out='P_PASS_SELFTEST: PASS (6 cases)'
```

Two rows together on the control: `PIN_CHECK=met … mismatches=0` (exit 0); on the copy:
`PIN_CHECK=unmet … mismatches=2` (exit 1). Each class is closed by its own rule — in the single-row runs
above only that row's verdict changes, and the mutation table (§3) shows each rule's arms die with that
rule alone.

---

## 3. Selftest — `pass=73 fail=0`, and every new arm is killed by its own mutation

```
$ TMPDIR=$PWD/selftest-tmp python3 -I -B mori-pin-check.py --selftest ; echo exit=$?
…
PIN_CHECK_SELFTEST pass=73 fail=0
exit=0
```

(65 arms inherited from the witness; +7 cases and +1 sidecar arm.) New arms and their verdict lines
(full output `.scratch/r49-Mo49ExecK2K8/selftest-copy.txt`):

| arm | what it asserts | verdict line |
|---|---|---|
| `k2_env_prefix_as_written` | the critic's reproducer: pin claims the run without the variable | `unmet mismatches=1` |
| `k2_env_applied_honest_pin` | an honest row whose pin is true only when `E_MODE=full` is applied | `met` |
| `k2_env_pwd_expanded` | `TMPDIR=$PWD/.scratch` is expanded to the measured root and the child sees an in-tree TMPDIR | `met` |
| `k2_env_unexpanded` | `TMPDIR=<elsewhere>` cannot be reproduced → fatal, not silently green | `unmet env_unexpanded=1` |
| `k2_entry_cell_env` | the bare `--selftest` form inherits the entry cell's assignment | `unmet mismatches=1` |
| `k8_pass_form_rc0` | PASS-form pin, rc 0 | `met` |
| `k8_pass_form_rc1` | PASS-form pin, rc 1 (sidecar) | `unmet mismatches=1` |
| `k8_failure_count_exception` | pin `pass=0 fail=2` with rc 1 stays legitimate | `met` |

Mutation check (`.scratch/r49-Mo49ExecK2K8/mutate-rules.py`, raw output `mutate-rules.txt`); each mutant
removes exactly one rule and must fail its own arm(s):

```
MUTANT k8_rule_removed rc=1 PIN_CHECK_SELFTEST pass=72 fail=1
   FAILURES: k8_pass_form_rc1
MUTANT k2_env_not_applied rc=1 PIN_CHECK_SELFTEST pass=70 fail=3
   FAILURES: k2_env_prefix_as_written, k2_env_applied_honest_pin, k2_entry_cell_env
MUTANT k2_unexpanded_not_rejected rc=1 PIN_CHECK_SELFTEST pass=72 fail=1
   FAILURES: k2_env_unexpanded
MUTANT k2_pwd_not_expanded rc=1 PIN_CHECK_SELFTEST pass=72 fail=1
   FAILURES: k2_env_pwd_expanded
```

No arm survives its mutation; no mutation fails an arm it does not own.

---

## 4. Acceptance — `count-c1.py` against the copy is still `C1=met`

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && \
  TMPDIR=$PWD/.scratch/r49-Mo49ExecK2K8/c1-acc timeout 3000 python3 \
    .ufo/waves/round-49/count-c1.py \
    --tool $PWD/.scratch/r49-Mo49ExecK2K8/mori-pin-check.py \
    --rev b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 --jobs 3 \
    --scratch $PWD/.scratch/r49-Mo49ExecK2K8/c1-acc/run
variant name=J1 expect=unmet got=unmet rc=1
… (J2-J8, N1-N10 as expected) …
variant name=H1 expect=met got=met rc=0
variant name=H2 expect=met got=met rc=0
variant name=H3 expect=met got=met rc=0
variant name=H4 expect=met got=met rc=0
variant name=H6 expect=met got=met rc=0
variant name=H7 expect=met got=met rc=0
variant name=H5 expect=met got=met rc=0
variant name=real expect=met got=met rc=0
variant name=real-opaque expect=met got=met rc=0
C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86
EXIT=0            (wall 929 s)
```

Full receipt `.scratch/r49-Mo49ExecK2K8/c1-acc-out.txt` (all 27 variant lines + `EXIT=0`). Nothing was
re-scored under a changed counter: `count-c1.py` is untouched (freeze sha256
`3c262a15ae28adffa63f6646d5ec15498d1a4c735dbc3c38f68af16afc616b6d`).

---

## 5. Guard against false reds — real registry

### 5.1 The real registry stays met, and nothing in it is env-prefixed *and* pinned

```
$ TMPDIR=$PWD/t-real-copy python3 -I -B mori-pin-check.py --rev b3e3453d… --repo <lane> \
    --min-tally-pins 26 --baseline-rev 2d85e33d…
PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0
duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=26
rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes          (exit 0, 170 s)
```

41 `state=match` lines (31 tally, 8 full digest, 2 truncated digest). Exit codes: 29 tally pins `rc=0`,
2 tally pins `rc=1` — and those two are exactly the pins that assert a failure count
(`C1_SELFTEST pass=15 fail=1`, `C3_SELFTEST pass=17 fail=2`, rows 190/192, mutant fixtures). The five
PASS-form pins all measured `rc=0`:

```
MORI_WAVE_SETTLEMENT_SELFTEST | : PASS (23 cases, 23 passed, 0 failed) | rc=0
MORI_PRESSURE_SELFTEST        | : PASS 12/12                          | rc=0
MORI_OOM_KILLERS_SELFTEST     | : PASS 32/32                          | rc=0
MORI_JOB_RUNWAY_SELFTEST      | : PASS 21/21                          | rc=0
MORI_SOURCE_DRIFT_SELFTEST    | : PASS (6 cases)                      | rc=0
```

`env_unexpanded=0` is exact, not luck: the registry has **three** env-prefixed command spans and **no
tally pin binds any of them** (`dump-pins.py` over `SKILL.md@b3e3453`; full dump `pins-b3e3453.txt`):

```
ENVSPAN line=181 row='r19 content review (C1)'                    span='TMPDIR=$PWD/.scratch python3 tools/mori-content-review.py --selftest'
ENVSPAN line=545 row='retained-loss audit'                        span='TMPDIR=$PWD/.scratch python3 tools/mori-evidence-loss.py --selftest'
ENVSPAN line=609 row='retention reconciliation schema-v2 (r23)'   span='TMPDIR=<existing-private-scratch> python3 tools/mori-retention-reconcile.py --selftest'
```

So the critic's cost note ("rejecting an env-prefixed bound argv would red 3 landed rows") does not hold
at `b3e3453` for a *pin-level* rule: those three cells carry no tally pin, hence no binding, hence no
verdict. Measured, not inferred: the run above is `met` with `env_unexpanded=0`.

### 5.2 Five earlier SKILL.md revisions — identical verdicts and findings with and without the new rules

Revisions picked as every 8th entry of `git log --format=%h -n 40 -- SKILL.md` (8th, 16th, 24th, 32nd,
40th): `265a955c`, `cedb0ec4`, `5b728304`, `b89ac342`, `6fce88a3`. Two harness modes, each scoring the
frozen witness and the copy side by side (`audit-revs.py`; raw `audit-rev-26.txt`, `audit-own.txt`,
machine-readable `audit-rev-floor26.json`, `audit-own-floor0.json`):

* **mode `rev`** — the round-49 acceptance flags (`--min-tally-pins 26 --baseline-rev 2d85e33d`) applied
  at each revision, tree and SKILL.md both from that revision (`--rev`; equals `git show R:SKILL.md` for
  the registry bytes):

| rev | witness | copy | findings |
|---|---|---|---|
| `b3e3453d` | `met` 31 pins | `met` 31 pins | none |
| `265a955c` | `unmet` (dropped=25, tally=6<26, 1 mismatch) | identical | 23, identical |
| `cedb0ec4` | `unmet` (dropped=28, tally=3, 1 mismatch) | identical | 26, identical |
| `5b728304` | `unmet` (dropped=28, tally=3, 1 mismatch) | identical | 26, identical |
| `b89ac342` | `unmet` (dropped=28, tally=3, 1 mismatch) | identical | 26, identical |
| `6fce88a3` | `unmet` (dropped=30, tally=1, 1 mismatch) | identical | 28, identical |

* **mode `own`** — no baseline, floor 0, so only the tool's own rules can red a revision:
  `b3e3453d` is `met` for both tools; all five older revisions are `unmet` for **both** tools with
  **exactly one** finding each, the same line in both.

```
pin line=168 kind=digest state=mismatch digest=c39e5a73… file=None
```

Findings lists are byte-identical between witness and copy at all six revisions (verified in
`audit-rev-floor26.json`; the only textual difference is the added `env_unexpanded=0` field, which is
compared after stripping that field: `summary_equal_except_new_field=True findings_identical=True` for
6/6 revisions).

**Which revisions turn red, and why (honest reasons, none caused by K2/K8):**

1. All five earlier revisions in `rev` mode: red because the *round-49* measurement flags are applied to
   a registry that predates them — 25-30 baseline pins are absent (`dropped`), and the tally count
   (1-6) is below the round-49 floor 26. Nothing about env or exit codes is involved.
2. All five earlier revisions in `own` mode: red for one pre-existing reason that both tools report
   identically — row 168 (`r14 regressions`) pins a truncated digest in prose, `harness SHA
   \`c39e5a73…\``, with no in-tree path in its cell, so R6/R10 binds nothing (`file=None`). The lane
   repaired that pin later (full digest `533218a5…`); at these revisions it is a true stale pin.
3. No revision turns red *only* under the copy: the K2 and K8 rules add zero findings on any of the six,
   in either mode.

---

## 6. Diff against the frozen control

`diff -u controls/tool-r48-merged-witness.py .scratch/r49-Mo49ExecK2K8/mori-pin-check.py` →
169 added / 40 removed lines (`k2k8.diff`). Non-selftest hunks: docstring (3 hunks); `split_env`,
`resolve_env`, `norm_cmd`, `render_cmd` replacing `strip_env`; `derive_command`/`command_from_span`/
`pin_commands` now carry env; `run_cmd(extra_env)`; `pin_bindings`/contracts key/`check`'s pin loop use
the env-aware form; the K8 exit predicate; `env_unexpanded` counter, finding line, `met` conjunction and
summary field. Selftest hunks: 4 fixture instruments, 7 cases, 1 sidecar arm. No change to: argv shape
(`argv_ok`), parser (`scan_lines`, `split_cells`, `parse_registry`), hidden-row accounting, R4/R5/R6/
R9/R10/R11 logic, `main`'s exit codes, or `export_rev`.

---

## 7. What the L1 must do when landing (integration, not done here)

1. Land these bytes at `tools/mori-pin-check.py`. The copy's own selftest prints
   `PIN_CHECK_SELFTEST pass=73 fail=0`; the registry row **938** (`registry pin reconciler (r47, C1)`)
   pins `pass=60` today, so **the pin must be bumped to `pass=73` in the same landing**, or the real
   registry turns red at the landed tip and P-C1 fails for a reason unrelated to K2/K8. (At `b3e3453`
   this is invisible: the row's command runs `R`'s `tools/mori-pin-check.py`, which is still v3.)
2. Row 938's verdict-map text lists the `met` conditions (`mismatches=0, unparsed=0, … hidden=0`); add
   `env_unexpanded=0`, and add `env_unexpanded` to the `1 → PIN_CHECK=unmet` finding-state list.
3. No registry rewording is needed for rows 181/545/609 (they bind no tally pin). If a later round gives
   any of them a tally, row 609's `TMPDIR=<existing-private-scratch>` becomes `env_unexpanded` and must
   be reworded to `TMPDIR=$PWD/.scratch` (or the assignment dropped).

### 7.1 Measured landing rehearsal (both directions)

**Stale registry pin → red.** A copy of the `b3e3453` tree with only `tools/mori-pin-check.py` replaced by
the deliverable (built under `.scratch/r49-Mo49ExecK2K8/landed/`, measured with `--root`; the 324 MB trees
were removed after measurement, receipts kept):

```
pin line=938 kind=tally prefix=PIN_CHECK_SELFTEST state=mismatch pinned='pass=60 fail=0' observed='pass=73 fail=0' rc=0 cmd='python3 tools/mori-pin-check.py --selftest'
PIN_CHECK=unmet tally_pins=31 … mismatches=1 … no_command=2 …          (exit 1)
```

**Pin bumped to 73 → row 938 match.** Same tree committed to a throwaway fixture repository
(`fixrepo.7pzO`, `git init -q`, one identity used only inside it, `rev-parse --show-toplevel` verified,
commit `87c66ed6a8e1c30039819befe3e2d126961720e8`), measured with `--rev`:

```
pin line=938 kind=tally prefix=PIN_CHECK_SELFTEST state=match pinned='pass=73 fail=0' observed='pass=73 fail=0' rc=0 cmd='python3 tools/mori-pin-check.py --selftest'
PIN_CHECK=unmet tally_pins=31 digest_pins=8 mismatches=2 … rev=87c66ed6a8e1c30039819befe3e2d126961720e8
  pin line=182 … prefix=R19_SELFTEST state=mismatch pinned='pass=26 fail=0' observed='pass=25 fail=1' rc=1
  pin line=911 … prefix=CONFORM_SELFTEST state=mismatch pinned='pass=11 fail=0' observed='pass=1 fail=10' rc=1
```

The two remaining reds are the fixture repository's own state, not the tool: row 182's
`mori-round19-regressions.py --selftest` prints `pass=26 fail=0` in the plain archive export and
`pass=25 fail=1` (`FAIL pinned-oracle-validates`) in a one-commit repository; row 911's
`.ufo/waves/round-40/conform.py --selftest` is the exact artifact the contract records for a clone
("the clone's round-40 `conform.py --selftest` pin fails there for a reason unrelated to the edit"), and
it fails identically under the frozen witness. With `--rev` at `b3e3453` (the real export, real history)
both rows match (`mismatches=0` in §5.1).

**Note on `no_command=2` in the `--root` line above:** rows 911/912 use the bare `--selftest` form with
`<rev>` in the entry cell; with `--root` there is no revision to substitute, so both tools report
`no_command` there. Measured side by side on the pristine export — witness and copy print the same two
lines (`CONFORM_SELFTEST`, `MORI_SOURCES_APPENDONLY_SELFTEST`, `no_command=2`, `mismatches=0`) — so it is
a pre-existing property of `--root` mode, not of these rules; `count-c1.py` measures with `--rev`.

## 8. Named limits of this work (measured where stated)

* **K2 residual — the entry cell of a full-command row.** The assignment is applied when it prefixes the
  *bound span* (K2 proper) and when the entry cell *is* the command (bare `--selftest`). An assignment
  written only in the entry cell of a row whose self-test cell carries a full `python3 … --selftest`
  command is still documentation, not environment. I did not close that: it is a different shape (the
  self-test cell's command is self-contained), and closing it would apply an environment the self-test
  cell never mentions. No landed row has this shape.
* **`env_unexpanded` is fatal.** A truthful row that writes `VAR=${SOMETHING} …--selftest` with a tally
  pin is red until reworded, because a no-shell runner cannot expand it. That is the deliberate trade
  (the alternative is silently running a different command — the class). Zero landed pins affected today.
* **K8 exemption is textual.** A pin that asserts `fail=N` (N≥1) keeps a nonzero exit legitimate, but the
  rule does not additionally *require* rc≠0 for such a pin: `pass=2 fail=1` printed with rc 0 is still
  accepted (the pinned text matched exactly). Claimed-failure-with-zero-exit is internally inconsistent
  but is not what K8 measured; I left it, as closing it is a new class not in the routed reproducer.
* Two K8 boundaries observed, not closed: `rc is None` (timeout) is treated as nonzero (a timeout cannot
  match anyway, since the observed text is `timeout`); the summary line gained one field, which
  `count-c1.py` tolerates (it matches `PIN_CHECK=(met|unmet)` only) but any external consumer parsing the
  exact field list must be rechecked — the only in-lane consumer, `count-c1.py`, was run (§4).

## 9. Observed lane side effect of measuring row 911 (reported, not remediated)

While measuring, untracked directories appeared in the lane working tree outside any seat's writable
area: `.ufo/waves/round-40/scratch/mori-conform-selftest-*`. They are created by the *measured*
instrument of row 911 (`.ufo/waves/round-40/conform.py`), which hardcodes its scratch root:

```
$ sed -n '70,71p' .ufo/waves/round-40/conform.py
LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
SCRATCH_ROOT = os.path.join(LANE, ".ufo", "waves", "round-40", "scratch")
```

So even when the reconciler measures an *export* (which is what `--rev` does), row 911's command writes
its selftest scratch into the real lane. Every full-registry scoring — this seat's `count-c1` run, its
audits, and any other seat's — passes through that row. Observation receipt
`.scratch/r49-Mo49ExecK2K8/lane-conform-scratch-observed.txt`: 8 directories at 22:35, 15 at 22:36:48,
with fresh ones still appearing at 22:36:48 — i.e. after this seat's last measurement finished at
22:33:47, concurrent seats are producing them too. I deleted none (live peers may own them; the class is
the round-end sweep's, like round 48's `.scratch` residue). This is an observation of the measurement
surface, not a defect of the K2/K8 bytes: both the frozen witness and the copy go through the same row.

## Findings

* **HIGH** — landing the copy without `SKILL.md` row 938's selftest pin bumped `pass=60 → pass=73` makes
  the real registry `unmet` at the landed tip (`mismatches=1`), i.e. a false red for P-C1. File:
  `SKILL.md:938` (`PIN_CHECK_SELFTEST pass=60 fail=0`), copy `.scratch/r49-Mo49ExecK2K8/mori-pin-check.py`
  (`selftest()` prints 73 arms). §4/§7.
* **MED** — row 938's `met` condition text omits the new fatal counter; a reader following the row cannot
  derive that `env_unexpanded>0` is unmet. File: `SKILL.md:938` (verdict-map cell); §7 item 2.
* **MED** — K2 remains open for an assignment written only in the entry cell of a row whose self-test
  cell carries a full command span. File: copy `derive_command` (applies entry env only on the bare
  `--selftest` path); no landed row has this shape (§8).
* **LOW** — `env_unexpanded` is fatal by design, so a truthful row using `${VAR}`/`~`/`<placeholder>` in a
  prefixed assignment is red until reworded. File: copy `resolve_env`; zero landed pins today (§8).
* **LOW** — a pin asserting `fail=N` (N≥1) is exempt from the exit check and is accepted at rc 0; claimed
  failures with a zero exit are not refused. File: copy `check()` K8 predicate (§8).
* **LOW** — the `PIN_CHECK=` summary grew a field (`env_unexpanded=N`); any consumer parsing the exact
  field set must adapt (`count-c1.py` is unaffected — measured `C1=met`). File: copy `check()` summary.
* **MED** — measuring the registry writes into the lane: row 911's instrument hardcodes
  `LANE =/home/vgpnk/Projects/shokunin/mori-shokunin` and puts its selftest scratch under
  `.ufo/waves/round-40/scratch/`, so every `--rev` scoring (any seat, this wave included) leaves untracked
  `mori-conform-selftest-*` directories in the lane even though the reconciler is documented read-only
  over committed bytes; 8 → 15 while observed, still growing after this seat's last run. File:
  `.ufo/waves/round-40/conform.py:70`; round-end sweep should include that directory; not deleted here
  (§9).
