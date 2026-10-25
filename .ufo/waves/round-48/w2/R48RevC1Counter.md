# R48RevC1Counter — fresh review of the frozen counter `count-c1.py` (round 48, w2)

Seat: R48RevC1Counter (leaf; no subagents). Target: the frozen C1 counter
`.ufo/waves/round-48/count-c1.py` — variant edit functions vs docstring, `verdict()`
conjunction, `run_tool()` consistency, thread-pool scratch handling, exit codes, and
whether w1 `CritC1Counter.md` F1 (harness-identity leak) is the only way a tool passes
without reading the registry.

**Attacked:** the counter's verdict logic, error paths, and every non-registry channel
to `C1=met`. **Verdict: the counter HOLDS as a predicate enforcer — no false-met path
found in `verdict()`/`run_tool()`/exit codes, and the landed claim prints `C1=met`
(exit 0). But F1 is NOT the only non-registry green: a second, independent class —
frozen-corpus fingerprinting — passes with zero registry work even after F1's proposed
fix (finding R1 below).** Report is limits/defects only; the counter stays frozen.

Frozen bytes: `count-c1.py` sha256 `7a2a6aa09b92…` identical at freeze `4387cf94`, tip
`e4dfff32`, and `evidence/freeze-sha256.txt:1`. All runs used
`TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48RevC1Counter`;
scratch copies under that dir only.

## Claim receipt (observed)

```
$ python3 .ufo/waves/round-48/count-c1.py --tool $PWD/tools/mori-pin-check.py \
    --rev e4dfff32d4f97c7ef250e9a7538fa75d4f284492 \
    --scratch $PWD/.scratch/r48w2-R48RevC1Counter/c1run          # exit 0, 17m18s
variant name=J1..J8 expect=unmet got=unmet rc=1   (all eight)
variant name=H1..H4 expect=met   got=met   rc=0   (all four)
variant name=real expect=met got=met rc=0
C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492
```

`--scratch` is the counter's documented flag; the stated claim command omits it and
would default to `mkdtemp(dir=<repo>/.scratch)`. Measured bytes = committed bytes:
`git show e4dfff32:tools/mori-pin-check.py` sha256 `85a89a3b6ba4…` == working tree
(`git status` clean for `tools/`; w1 F8 non-issue at tip). Selftest at tip:
`C1_SELFTEST pass=34 fail=0`, exit 0. Landed tool contains no variant-name/TMPDIR-name
branch — it opens `--skill` as a path (line 663-668); `grep -nE 'variant|c1-|basename'
tools/mori-pin-check.py` → no hits (the w2 closure item from w1 F1).

---

## R1 (class b, new) — frozen-corpus fingerprinting: a second non-registry green, independent of F1

w1 F1 showed a tool can pass keying on the harness's variant names. The fix proposed
(opaque `--skill` basenames, neutral `TMPDIR`) removes that channel — but does not
close this one, which needs **no metadata at all**, only the input file's bytes:

The 12 variants are pure functions of `git show <rev>:SKILL.md`, and `--repo`/`--rev`
are handed to the tool on its own argv. A tool can import the counter module (or
reimplement the 12 edits), regenerate every expected input, fingerprint each by hash,
and answer by lookup — never parsing a registry row, never reading a filename:

```python
# .scratch/r48w2-R48RevC1Counter/tool_fingerprint.py (essence)
m = importlib.util.spec_from_file_location("c", COUNTER); m.loader.exec_module(...)
base = git_show(repo, rev + ":SKILL.md")
table = {sha256(fn(base)): expect for name, expect, fn in m.VARIANTS}
if --skill absent: print("PIN_CHECK=met"); return 0
hit = table.get(sha256(open(--skill).read()))   # -> its expected verdict
```

**Observed** (counter against this tool, exit 0):

```
variant name=J1..J8 got=unmet rc=1   variant name=H1..H4 got=met rc=0   real got=met
C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=e4dfff32…
```

The tool does zero registry validation — it recognizes members of the counter's own
deterministic input set. So F1's two channels are *instances*, not the whole class;
"the harness-identity leak is the only way" is **disproven**. This is an open-book
exam: the frozen counter fully describes the test corpus. A real fix needs per-run
opaque input generation (e.g. salted whitespace/ordering perturbations the registry
tolerates) or the predicate accepts fingerprinting as a named limit.

## R2 (class b) — the F1 identity leak is wider than the two named channels

w1 F1 named `--skill` basename (`variant-J1.md`, line 238) and `TMPDIR` `c1-<name>-*`
prefix (lines 206, 247). Three more channels leak the same bits:

- **Sibling listing:** all 12 variant files are written into one shared `--scratch`
  dir (lines 238-241). `os.listdir(os.path.dirname(--skill))` recovers every
  `variant-<name>.md` basename even if the tool's own path were opaque.
- **mtime ordering:** variant files are written sequentially in `VARIANTS` order
  (lines 233-241), so `st_mtime` ranking leaks the J1..H4 ordinals even with uniform
  names.
- **`/proc` argv:** the 13 runs are concurrent (line 244-248); siblings'
  `/proc/<pid>/cmdline` carries `--skill <scratch>/variant-<name>.md`.

Plus leftovers: a reused `--scratch` accumulates `c1-<name>-*` dirs across runs
(w1 F7). Consequence for any future counter: neutral names alone are insufficient;
each run needs a private directory (or content-addressed input names).

## R3 (class c) — setup paths exit 1 with tracebacks instead of documented exit 2

Docstring/contract: setup errors → `C1_SETUP` line, exit 2 (lines 29-30, 281-283,
290-291). Observed violations (all still fail-safe — never `met`):

| input | observed | expected |
|---|---|---|
| `--min-tally abc` | `ValueError` traceback, exit 1 (line 294) | exit 2 |
| `--jobs 0` | `ValueError: max_workers` traceback, exit 1 (line 244) | exit 2 |
| trailing `--tool` (no value) | `IndexError` traceback, exit 1 (line 278) | usage, exit 2 |
| no `--scratch` and `<repo>/.scratch` absent | `FileNotFoundError` traceback, exit 1 (line 292; fixture-verified: `mkdtemp` needs the parent) | exit 2 |
| `git_show` timeout / `git` missing / non-UTF8 SKILL.md | `TimeoutExpired`/`FileNotFoundError`/`UnicodeDecodeError` propagate, exit 1 (lines 194-198) | setup error — inconsistent with `rev-parse`'s catch at 286-291 |

**w1 F6 correction:** F6 predicted a missing `--tool` crashes the counter with
`FileNotFoundError`. Observed the opposite of a crash: `python3 /nonexistent.py`
itself exits 2 → every arm `got=error rc=2` → clean `C1=unmet … errors=13`, exit 1.
Only a missing *interpreter* would propagate; `sys.executable` always exists. The
other two F6 items (bad int, missing flag value) stand — reproduced above.

## R4 (class a, extends w1 F2) — H4 is "honest" only under the landed row-scoped R4

H4 re-binds the existing prefix `C2_SELFTEST` to `python3
.ufo/waves/round-47/count-c2.py --selftest` under a new row name (lines 176-183). The
literal spec text (v3-spec line 14: "a row, new or old, that uses a baseline prefix
with an argv not in that prefix's baseline set is `rebound`") makes H4 **rebound →
unmet**: baseline `2d85e33d`'s `C2_SELFTEST` set is {round-44, round-45 count-c2}. The
landed tool passes H4 only because its R4 is keyed on `(row name, prefix)` — the same
spec-vs-registry incoherence w1 F2 flagged for real row 939. H4 therefore smuggles
the contested interpretation into the predicate's *honest* side: under a literal-R4
candidate, `honest_unmet=1` → `C1=unmet`. Same disposition as F2 (resolve in the spec
or the registry); recorded so it isn't re-found as an H4-specific surprise.

## R5 (class d) — shared-scratch integrity is honor-system; timeouts leave grandchildren

- Variant inputs sit in a world-visible shared dir for the whole measurement
  (lines 238-248). A tool instance can rewrite sibling `variant-*.md` files mid-run —
  self-harm only (it degrades its own siblings' inputs into junk-looking text), so no
  green path, but the counter's "the tool under test writes only inside `--scratch`"
  (docstring line 30, SKILL.md row 971's write-scope cell) is a convention the harness
  does not enforce: nothing watches for writes outside `TMPDIR` or into the input
  files themselves.
- `subprocess.run(timeout=TOOL_TIMEOUT)` (line 208) kills only the direct child; a
  tool's grandchildren survive a timeout. Harmless to the verdict (counted `timeout`),
  litter under `TMPDIR` only.
- Whole-run cost observed: 17m18s at `--jobs 4` for the landed tool; the `TOOL_TIMEOUT
  = 900` ceiling is per arm (line 42).

## Verified clean (no defect found)

- **`verdict()` conjunction (257-266):** equivalent to "every arm `got==expect`,
  `real==met`, no `error`/`timeout`" — `junk_met`/`honest_unmet`/`errors` are
  exhaustive over the only `got` values `run_tool` can produce (`met|unmet|error|
  timeout`). Errors can never satisfy `met` (`errors==0` conjunct; an erroring junk
  arm also trips `junk_met`). Selftest covers the six adversarial shapes
  (`correct_met`, `do_nothing`, `always_unmet`, `one_junk_green`, `real_red`,
  `error_not_unmet`) — all PASS.
- **Variants faithful to docstring at `e4dfff32`:** all 12 anchors resolve —
  `PIN_CHECK_SELFTEST`/`C2_SELFTEST` rows adjacent at SKILL.md lines 938/939 (0-based
  937/938), gate-table header line 936 (`self-test` literal present), `(743 lines)`
  unique at row 184's self-test cell, `37fd7c24ff52…` unique at row 192's self-test
  cell, J5 adjacency holds, `new_row` cell order matches the real convention (entry
  cell = gate argv, self-test cell = `argv → PREFIX pin`). Wording nits, not defects:
  J6's blank goes between *separator row* and first data row (`insert(h+2)`, line 137)
  where the docstring says "between header and first row"; J7/J8 replace the first
  literal occurrence — unique at tip, fragile if the literal reappears earlier in a
  non-cell position (anchor wouldn't catch it; the resulting edit might silently stop
  being junk).
- **`run_tool` consistency (201-224):** `rc ∉ {0,1}` or no `PIN_CHECK=` line → `error`;
  `got`/rc disagreement → `error`; timeout → `error`; last `PIN_CHECK=` line wins
  (deterministic; multi-emission resolves to the final line). `sys.executable -I -B`
  + `PYTHONDONTWRITEBYTECODE` consistent.
- **Pool/scratch mechanics (227-254):** variant files written before pool start;
  per-run `mkdtemp` names unique, created synchronously; results appended on the main
  thread; deterministic sort by `VARIANTS` order + `real`. No data race found (w1 F7
  stands).
- **Exit codes:** 0 met / 1 unmet / 2 setup verified live (`--selftest` 0; claim run
  0; stub-style failures 1; bad `--rev` and missing `--repo` → `C1_SETUP` 2). See R3
  for the traceback paths.
- **Frozen integrity:** counter identical freeze↔tip↔receipt; `git status` clean at
  measurement; `--tool` bytes == `--rev` bytes at tip.

## Residual risk / gaps

- R1 (fingerprinting) survives *every* presentation-layer fix to F1; only
  input-space salt or a stated limit closes it. Any future counter sharing this
  deterministic-corpus design inherits it.
- R2/R5: shared scratch is both an identity oracle and an unenforced write scope;
  per-run private dirs kill both.
- Not checked (UNVERIFIED): counter behavior under concurrent counter invocations
  sharing `--scratch`; tool stdin-blocking hangs (would resolve via timeout);
  `Anchor` handling for hypothetical `re` failures inside variants other than the
  declared ones (none reachable with the fixed function set).
- Report-scope note: this seat reviewed the counter; the landed tool's v3 rule
  correctness is other seats' scope.

Artifacts: `.scratch/r48w2-R48RevC1Counter/` holds `tool_fingerprint.py`, its counter
transcript (`fingerprint-run`), the claim-run transcript (`c1run`), the no-`.scratch`
fixture (`fixrepo-*`), and probe outputs. No tools installed (stdlib + git only);
nothing outside my report and scratch dir written.
