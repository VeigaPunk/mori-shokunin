# R48CritV3Junk2 — command-binding false greens against the landed v3

**Seat.** R48CritV3Junk2 (critic, wave w2). Leaf seat, no subagent dispatch, no tool installed.
**Lane repo.** `/home/vgpnk/Projects/shokunin/mori-shokunin`. **Landed tip under attack.**
`e4dfff32d4f97c7ef250e9a7538fa75d4f284492` (freeze `4387cf94`, entering `e5dbac05`).
**Instrument under attack.** `tools/mori-pin-check.py` (v3, sha256
`85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1`; identical bytes at
`e4dfff3` and in the working tree: `git diff --stat e4dfff32 -- tools/mori-pin-check.py SKILL.md`
is empty, exit 0).

## Verdict

**P-C1 HOLDS at the landed tip** — I reproduced the acceptance run byte for byte
(`C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12`, exit 0). No frozen variant was
re-scored, no predicate or counter byte was touched.

**The tool's reach BREAKS on seven new junk classes** (K2-K8 below, plus the already-routed K1)
that the frozen 12 variants do not carry.
Sixteen junk edits (13 against `e4dfff3`'s real `SKILL.md`, 3 against a purpose-built fixture
instrument) print `PIN_CHECK=met` although each one is a false green by the round-46 M1 /
round-47 FG doctrine ("a pin that a checker cannot see is not a pin", "a deleted pin is not a
fix"). Four controls held. One **tool defect** (not a survivor): a junk registry row that makes an
existing baseline row's bound command unresolvable makes v3 exit **2** (`PIN_CHECK_SETUP can only
join an iterable`) instead of reporting a finding — a `TypeError` at
`tools/mori-pin-check.py:552`.

| class | what it defeats | landed-tip arms | verdict |
|---|---|---|---|
| K1 misattribution (D7) | row names instrument A, self-test cell runs B | 3 | survives — **known** (`w1/CritJunkClasses.md` D7) |
| K2 env-prefix substitution | `VAR=x cmd` prefix is stripped and never applied | 1 + 1 fixture | survives — **new** |
| K3 pin deletion | line-count / truncated-digest pins have no presence counter | 2 | survives — **new** |
| K4 pins outside the self-test cell | full digest, `(N lines)`, non-`pass=`/`PASS` tally spelling | 2 | survives — **new** |
| K5 namespace join | a prefix shared by ≥2 baseline instruments admits any new argv | 2 (1 real, 1 fixture) | survives — **new** |
| K6 floor slack | 31 tally pins vs `--min-tally-pins 26`; the self row is not in the baseline | 1 | survives — **new** |
| K7 line-count rebinding | `(N lines)` binds to any nearest preceding in-tree path (R10 was applied to digests only) | 1 | survives — **new** |
| K8 rc-free PASS pins | a pin without `fail=0` never checks the exit code | 1 fixture | survives — **new** |
| X1 setup exit on junk | baseline binding becomes `None` → `" ".join(None)` | 2 | **defect**, not green |

Impacted axes: **calibration** (C1 — the claim is met but its title overreaches: "cannot be turned
green by the junk the round-47 closure found" is true of *that* junk and false of the classes
below). Operability is affected only through X1 (exit 2 on a registry finding). C2 is untouched by
this seat.

## Method

* Every arm is scored with **count-c1.py's own `run_tool`** (imported, not re-implemented):
  `python3 -I -B <tool> --rev e4dfff3 --repo <lane> --min-tally-pins 26 --baseline-rev 2d85e33d
  --skill <variant>` with `TMPDIR` = a per-arm scratch dir. The verdict line quoted per arm is the
  same argv run once more with output captured (`PIN_CHECK=…`).
* Variants are exact-substring edits of `SKILL.md@e4dfff3` (saved as
  `.scratch/r48w2-R48CritV3Junk2/variant-<name>.md`); a non-unique anchor is an arm error, never a
  silent no-op (`attack.py --dry` prints all 19 anchors `OK`).
* Fixture arms use a purpose-built repo (`$(mktemp -d)`, `git init -q`,
  `rev-parse --show-toplevel` verified equal before the first commit, every later call
  `git -C "$D"`) because K2/K8/K5 need an instrument whose output actually depends on the
  environment/exit code; only `--repo`, `--rev`, `--baseline-rev` and the tally floor (1) differ
  from the acceptance flags.
* Read-only over the lane: no `git add/commit/stash/checkout/reset/pull/push`, no jj mutation, no
  edit outside `.scratch/r48w2-R48CritV3Junk2/` and this report.

Harness: `.scratch/r48w2-R48CritV3Junk2/{attack.py,fixture.py,corrections.py,analyze.py}`;
raw outputs `attack-out.txt`, `results.json`, `fixture-results.json`, `variants.diff`,
`run-<arm>/tool-out.txt`.

## Acceptance run (ground truth, reproduced)

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && \
  TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48CritV3Junk2 \
  timeout 3300 python3 .ufo/waves/round-48/count-c1.py \
    --tool /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-pin-check.py \
    --rev e4dfff32d4f97c7ef250e9a7538fa75d4f284492 \
    --scratch /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48CritV3Junk2/acc-c1 --jobs 6
variant name=J1 expect=unmet got=unmet rc=1
… (J2-J8 identical) …
variant name=H1 expect=met got=met rc=0
… (H2-H4 identical) …
variant name=real expect=met got=met rc=0
C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492
EXIT=0            (wall 853.62 s)
```

The real registry through `--skill` (control arm `CONTROL-real`, exit 0):

```
PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0
rebound=0 duplicate=0 hidden=0 min_tally_pins=26 rev=e4dfff32… baseline=yes
```

## Survivors, with reproducers

Each block is the exact edit (relative to `SKILL.md@e4dfff3`), the arm's verdict, and the class.

### K1 — misattribution (D7): the row names A, the self-test cell runs B

Already routed by `w1/CritJunkClasses.md` D7 and declared open in `SKILL.md:960-962`. I confirm it
against the **landed bytes** with three shapes, and one of them attacks the landed registry row
itself:

```
+| r44 gate registry (C2) — v3 recheck | gate | `python3 tools/mori-gate-registry.py --rev <rev> --audit <path>` | 0/1/2 | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=60 fail=0` | none | none | mori |
```
```
D7-new-row-entry-A-runs-B   want=met got=met rc=0
PIN_CHECK=met tally_pins=32 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0
```
A reader attributes `pass=60` to `mori-gate-registry.py`; that instrument's real selftest is
`pass=15` (`pin line=184 … pinned='pass=15 fail=0' observed='pass=15 fail=0'`).

Same with the **bare `.py` span** (the mutant slot), which has no entry coupling either:

```
+| r44 gate registry (C2) — v3 recheck bare | gate | `python3 tools/mori-gate-registry.py --rev <rev> --audit <path>` | 0/1/2 | the named mutant `tools/mori-pin-check.py` reads `PIN_CHECK_SELFTEST pass=60 fail=0` | none | none | mori |
```
```
D7-bare-span-entry-A-runs-B   want=met got=met rc=0        (same counters)
```

And the strongest form — **the row that pins the reconciler is re-pointed at another instrument**
(row 938 is new since the round-47 baseline, so `dropped` cannot see it):

```
-… `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=60 fail=0` …
+… `python3 tools/mori-unlanded-check.py --selftest` → `UNLANDED_SELFTEST pass=13 fail=0` …
```
```
D7-existing-self-row-repointed   want=met got=met rc=0
PIN_CHECK=met tally_pins=31 digest_pins=8 … dropped=0 rebound=0 …
```

Cause: `command_from_span`/`pin_commands` (`tools/mori-pin-check.py:325-356`) never relate the bound
argv to `cells[eidx]`; the entry cell is read only for the bare `--selftest` form
(`derive_command`, 364-390).

The purest form of the assigned class — a **registered `tools/` stub that prints the pinned text
unconditionally** — cannot be instantiated against a fixed revision, because the measured tree is a
`git archive` export of R: the stub must be *committed at R*, i.e. the attack is a landing-time pair
(one row + one stub). Fixture `STUB-joins-namespace` is that pair, and v3 runs the stub and calls
the pin a match.

**Smallest safe correction.** Compare the *first* tally pin's argv path with the entry cell's first
`.py`/`.sh` path (normalised) and report `misattributed`. Measured against the landed registry:
**0 of 58 rows break** (`corrections.py` §C-a). The two legitimate exceptions are *later* pins —
rows 190 and 192, ordinal 1, `.ufo/waves/round-45/fixtures/mutants/count-{1,3}.py` — so a
first-pin-only rule costs nothing. This matters because `SKILL.md:960-962` justifies leaving D7
open with "closing it as a rule turns four legitimate mutant-command rows red"; at `e4dfff3` I
measure **2 pins over 2 rows**, both non-first. That sentence does not reproduce (see Limits).

### K2 — `VAR=x` env prefix: stripped, never applied

`strip_env` (`358-362`) pops leading `VAR=value` words; `run_cmd` (`400-417`) builds
`env = dict(os.environ, TMPDIR=tmp, …)` and never applies them, so the command that runs is **not
the command the row writes**.

```
+| r47 tracepoint catalogue (C2) — env arm | gate | `python3 tools/mori-pin-check.py --rev <rev>` | 0/1/2 | `MORI_FAST=1 python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=60 fail=0` | none | none | mori |
```
```
ENV-prefix-new-row   want=met got=met rc=0     PIN_CHECK=met tally_pins=32 … no_command=0 …
```

That arm only shows the shape. The false *claim* needs an instrument that reads the variable —
fixture arm `ENV-prefix-false-as-written` (row's self-test span becomes
`MORI_STRICT=1 python3 tools/x.py --selftest`, pin unchanged):

```
ENV-prefix-false-as-written   want=met got=met rc=0
PIN_CHECK=met tally_pins=5 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 baseline=yes
as-written `MORI_STRICT=1 python3 tools/x.py --selftest` -> rc=1 out='X_SELFTEST pass=2 fail=1'
```
The row pins `X_SELFTEST pass=3 fail=0`; the command it names prints `pass=2 fail=1` and exits 1.
v3 runs it without `MORI_STRICT` and calls the pin a match.

**Smallest safe correction — not free.** `reject` (make an env-prefixed bound argv `no_command`)
would red **3 landed rows**: 181 `r19 content review (C1)`, 545 `retained-loss audit`, 609
`retention reconciliation schema-v2 (r23)`, each of which writes `TMPDIR=$PWD/.scratch` or
`TMPDIR=<existing-private-scratch> python3 … --selftest` (`corrections.py` §C-b). So the correction
is a **paired tool + registry change**: drop `strip_env` from `argv_ok`, add a fatal `env_prefix`
counter, and reword those three cells (their TMPDIR is supplied by `run_cmd` anyway). Applying the
assignments instead is *not* safe: `$PWD`/`<…>` are not shell-expanded, so the child would get a
literal TMPDIR outside the tree.

### K3 — a deleted pin is not counted (line-count, truncated digest)

`pin_keys` (`419-435`) counts only tally spans and **full** 64-hex digests. `(N lines)` and
`hex{8,63}…` pins exist only while present; R5/R6 validate them but nothing counts them.

```
-`8b82ac…f5832` (743 lines)                       # row 184, line-count pin deleted
```
```
DEL-linecount-pin   want=met got=met rc=0
PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0
```
```
- at sha256 `37fd7c24ff52…`;                      # row 192, truncated-digest pin deleted
```
```
DEL-trunc-digest-pin   want=met got=met rc=0
PIN_CHECK=met tally_pins=31 digest_pins=7 … dropped=0 …
```
(`digest_pins` falls 8 → 7 and nothing else moves.)

**Smallest safe correction.** Per baseline row, per pin kind (tally prefix / digest / lines), the
count at R must be ≥ the count at `--baseline-rev`. Measured (`corrections.py` §C-f): **53
baseline rows, 58 landed rows, 0 obligation breakages**. The baseline's stale `c39e5a73…` was
*repaired to a full digest* `533218a566030fda…`, so a digest-*kind* count — not an identity — is
what survives. An identity-based `pin_keys` extension would red the landed tip: the baseline carries `c39e5a73…` and
`e4dfff3` does not.

### K4 — pins the checker never reads (outside the self-test cell)

`check()` reads `cells[idx]` only; `hidden_rows`' R9a catches tally-looking tokens in other cells
via `TALLY_TEXT_RE = [A-Z][A-Z0-9_]*SELFTEST[:=]?\s*(?:pass=\d+|PASS)` (`121`) and nothing else.
Row 191's *pinned-values* cell already carries a full digest and a line count that v3 never
measures (`AUDITOR_REL = tools/mori-gate-registry.py` … `sha256 8b82ac…`, `743 lines`).

```
-(v2, sha256 `8b82ac…f5832`, 743 lines)           # row 191 cell 5 → both made false
+(v2, sha256 `0000…0000`, 742 lines)
```
```
CELL5-digest-and-count-stale   want=met got=met rc=0
PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 … hidden=0 …
```
and a tally in another cell whose spelling `TALLY_TEXT_RE` does not know:

```
+| … | `python3 .ufo/waves/round-44/count-c3.py --selftest` → `C3_SELFTEST pass=6 fail=0` | `C3_SELFTEST 999/0` | none | mori |
```
```
TALLY-other-cell-no-pass-form   want=met got=met rc=0     (tally_pins=32, hidden=0)
```

**Smallest safe correction — has a real cost.** A *stale-check* of digest/line-count spans in every
cell reds the landed registry at row 817 (`blind-writer gate (r31)` cell 5 carries
`79b774f7…`/`3c26ef69…`, prose digests of a *gate blob*, whose nearest preceding in-tree path is
`…/expected.json`) — 2 spans, `corrections.py` §C-d. A *presence* rule would additionally red row
191. So this class cannot be closed tool-side alone; it needs a paired registry rewording (rows 191,
817) plus the rule. Until then it is a **limit**, and the cheapest honest mitigation is a non-fatal
`elsewhere=N` field on the `PIN_CHECK=` line so the invisibility is at least reported.

### K5 — namespace join: a shared prefix admits any new argv

`check()` exempts a prefix whose baseline bindings have `len(set) > 1` (`543-548`, comment at
`470-471`: "a prefix already shared by several instruments is a namespace; new genuine instruments
may join it"). At `2d85e33d` the shared prefixes are `C1_SELFTEST` (3 argvs), `C2_SELFTEST` (2),
`C3_SELFTEST` (3). A **fourth** instrument joins `C1_SELFTEST` with an argv the baseline never saw:

```
+| r44 gate registry (C2) — fourth instrument | gate | `python3 tools/mori-gate-registry.py --rev <rev> --audit <path>` | 0/1/2 | `python3 .ufo/waves/round-48/count-c1.py --selftest` → `C1_SELFTEST pass=34 fail=0` | none | none | mori |
```
```
NS-join-C1-fourth-instrument   want=met got=met rc=0
PIN_CHECK=met tally_pins=32 … rebound=0 …
```
(`NS-join-C1-namespace`, which re-runs an argv already in the set, is met for the same reason.)

Fixture `STUB-joins-namespace` shows what the exemption buys an attacker — an **unconditional
printer** joins a two-instrument prefix:

```
STUB-joins-namespace   want=met got=met rc=0
PIN_CHECK=met tally_pins=6 … rebound=0 …          # entry names tools/g.py, span runs tools/stub.py
                                                  # stub prints GATE_REGISTRY_SELFTEST pass=99 fail=0 (g.py prints pass=15)
```
and the control on a single-instrument prefix is caught:

```
STUB-joins-solo-prefix  want=unmet got=unmet rc=1
PIN_CHECK=unmet tally_pins=6 … rebound=1 …
```

**Smallest safe correction.** K1's first-pin entry↔argv check already covers the misattribution
part of a namespace join; with it in place the `len(set) > 1` exemption is only needed for *later*
pins (mutants). If the exemption is kept for all pins, make membership explicit in the registry
(a `namespace` cell listing the allowed argvs) instead of inferring it from the baseline.

### K6 — floor slack: 31 pins, floor 26, and the self row is not in the baseline

```
-| registry pin reconciler (r47, C1) | gate | …      # row 938 deleted whole
```
```
DEL-self-row   want=met got=met rc=0
PIN_CHECK=met tally_pins=30 digest_pins=8 … dropped=0 … min_tally_pins=26
```
The landed registry carries 31 tally pins (`corrections.py` §C-e: tally=31, full_digest=5,
truncated=3, line-count=2 in self-test cells), so five can vanish under the frozen floor, and the
row that pins the instrument under test is not in `2d85e33d`, so `dropped` cannot see it.

**Smallest safe correction.** This is a *contract* number, not a tool rule: the counter's
`MIN_TALLY` 26 is the round-47 floor. Route for round 49: raise the floor to the landed count (31)
or add a per-row existence obligation for the row whose entry names the tool file under
measurement. No tool-only change closes it without a new flag, so I report it as a limit.

### K7 — line-count pin rebound to a decoy path in the same cell

R10 binds a digest to the nearest preceding in-tree path *of its cell* (closing the elsewhere-in-row
decoy), but `line_count_pins` (`306-311`) keeps the same nearest-path rule with no tie to the row's
instrument:

```
-`8b82ac…f5832` (743 lines)
+`8b82ac…f5832` of `tools/mori-unlanded-check.py` (209 lines)
```
```
REBIND-linecount-decoy-path   want=met got=met rc=0
PIN_CHECK=met … mismatches=0 …
```
(`tools/mori-unlanded-check.py` has 209 newlines at `e4dfff3`; the pin is now true of the decoy and
says nothing about `mori-gate-registry.py`.)

**Smallest safe correction.** Require a line-count pin's nearest preceding path to be the row's
bound argv path. Safe: at `e4dfff3` both line-count pins (rows 184, 194) already bind
`tools/mori-gate-registry.py`, which is the argv path of both rows (C-a: 0 breakages).

### K8 — a pin without `fail=0` never checks the exit code

`576`: `if ok and re.search(r"\bfail=0\b", want) and rc != 0: ok = False`. Five landed pins use the
PASS form (`: PASS 21/21`, `: PASS 32/32`, `: PASS 12/12`, `: PASS (6 cases)`,
`: PASS (23 cases, 23 passed, 0 failed)`), so rc is unconstrained for them. Fixture
`PASS-form-rc1` (instrument prints `P_SELFTEST: PASS (6 cases)` then exits 1):

```
PASS-form-rc1   want=met got=met rc=0
PIN_CHECK=met tally_pins=5 … mismatches=0 …
as-written `python3 tools/p.py --selftest` -> rc=1 out='P_SELFTEST: PASS (6 cases)'
```

**Smallest safe correction.** Require `rc == 0` unless the pinned text asserts a nonzero failure
(`re.search(r"\bfail=[1-9]", want)`). Safe at the landed tip: all 31 tally pins were re-run with
output captured (`run-CONTROL-real/tool-out.txt`); the only nonzero rcs are the two mutant pins
(`pass=15 fail=1` rc=1, `pass=17 fail=2` rc=1) and every PASS-form pin is rc=0.

## Defect (not a false green): X1 — a junk registry row exits 2 instead of reporting

Two independent junk edits that make an **existing baseline row's** bound command unresolvable
(`python3 ./tools/…` and `python3 -c "…" --selftest`) both print one line and exit 2:

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && python3 -I -B \
    /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-pin-check.py \
    --rev e4dfff32d4f97c7ef250e9a7538fa75d4f284492 \
    --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
    --min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 \
    --skill /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48CritV3Junk2/variant-SPELL-dot-slash-baseline-row.md
PIN_CHECK_SETUP can only join an iterable          (rc=2, no pin lines)
```

Cause, reproduced without git (`pc.check(...)` on a two-line synthetic registry):

```
  File "tools/mori-pin-check.py", line 552, in check
    % (line, prefix, " ".join(norm)))
TypeError: can only join an iterable
```

The rebound branch `543-544` fires when `bkey in base_bind and base_bind[bkey] is not None and
norm != base_bind[bkey]` — with `norm is None` (the new binding is invalid) that is true, and the
finding formatter then joins `None`. main's `except Exception` (`R7 L5`) turns it into a setup exit.
Consequences: (a) the tool reports "setup" for a registry finding, which is the wrong class for a
reader (the SKILL row documents exit 2 as `PIN_CHECK_SETUP` for usage/unresolvable
revision/unreadable SKILL); (b) **no finding line is printed at all**, because `check()` prints only
at the end; (c) the selftest has no arm for "a baseline row's binding disappears" — its
`v2_rebound_to_other_tool` / `v2_entry_rebound` arms both keep a *valid* new argv, so the crash is
invisible to `--selftest`. It does **not** turn C1 green: count-c1 classifies rc=2 / no
`PIN_CHECK=` line as `error`, and `errors=0` is required for met (my two arms scored
`got=error rc=2`, i.e. not met).

**Smallest safe correction.** Format the finding as `cmd=%r % (norm,)` (or emit `no_command` for
that pin) so the tally pin falls through to `words is None → no_command`, exit 1; add a selftest arm
`baseline_binding_disappears` that asserts rc 1 + `no_command`/`rebound`, not rc 2.

## What held (controls)

| control | edit | result |
|---|---|---|
| `SH-existing-row-bash-to-sh` | row 166 `bash` → `sh` | `unmet rebound=1` (exit 1) |
| `SH-new-row-baseline-prefix` | new row, `MORI_SILENCE_CASES_SELFTEST` + `sh` | `unmet rebound=1` |
| `SPELL-double-slash-baseline-row` | row 184 `tools//mori-gate-registry.py` | `unmet rebound=1` |
| `SPELL-dot-slash-baseline-row` | row 184 `./tools/mori-gate-registry.py` | rc 2 (X1 crash — not green, wrong class) |
| fixture `STUB-joins-solo-prefix` | stub on a single-instrument prefix | `unmet rebound=1` |

So `bash` vs `sh` and path respelling are **closed** wherever a baseline obligation exists
(single-instrument prefix, existing row with a resolvable baseline binding). They ride free only on
the two unchecked prefix classes (K5 namespace, K2/K6-style new prefixes) — i.e. the path-spelling
arm `SPELL-double-slash-self-row` (row 938, `tools//mori-pin-check.py`, `met`) is a *consequence* of
K1/K5, not an independent hole: `PIN_CHECK_SELFTEST` has no baseline binding at `2d85e33d`.

## Impacted axes and recommended routing

* **Calibration (C1).** P-C1 is met and stays met; these are named limits under the contract's
  "Named limits" clause, not a re-score. The one thing a round-49 claim should not repeat is
  `SKILL.md:960-962`'s cost estimate for closing D7 (see Limits).
* **Operability.** X1 is the only finding that changes how an operator reads the tool: a junk
  registry currently looks like a setup failure and hides every finding.
* Cheapest high-value fixes, in order: X1 (one-line formatter + one selftest arm), K1 (first-pin
  entry↔argv, 0 landed rows break), K3 (per-row pin-kind count, 0 landed rows break), K8
  (`fail=[1-9]` exclusion, 0 landed rows break), K7 (line-count path tie, 0 landed rows break).
  K2 and K4 are paired tool+registry changes; K6 is a contract-number change.

## Limits of this review

* I did not re-score P-C1, did not modify `count-c1.py`, `count-c2.py`, the tool, `SKILL.md`,
  `corpus/`, or any frozen file; every arm lives in
  `.scratch/r48w2-R48CritV3Junk2/`.
* Fixture arms use `--min-tally-pins 1` (a one-table fixture cannot reach 26); the argv shape and
  the baseline mechanics are otherwise identical.
* K2/K8/K5's fixture instruments are mine, not lane tools: they prove the *rule* is blind to the
  env prefix / rc / namespace join, not that a lane tool currently misbehaves that way.
* `SKILL.md:960-962` says closing D7 "turns four legitimate mutant-command rows red". At `e4dfff3`
  I measure 2 pins over 2 rows (190/192, ordinal 1) and 0 rows red under a first-pin-only check.
  Either the sentence refers to a different formulation or it is stale; I did not verify which.
* I did not test the counter's own arms, C2, or the `count-c2`/quota surface (other seats own
  them). No tool was installed or updated for this seat.
