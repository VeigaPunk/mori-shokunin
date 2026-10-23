# RevC5Bounds — wave-2 falsify: `bounded_reads` audit (C5 / P-C5 bounds clause)

Seat: `MoriR38.RevC5Bounds` · Scored tip audited: `f725f3076972e6e70595b5ac8279be524a111ff8`
Method: independent `ast` parse of the committed blobs (`git show f725f30:.ufo/waves/round-38/{count-c1,count-c4}.py`,
script `scratch/RevC5Bounds/ast_audit.py`, output `scratch/RevC5Bounds/ast-audit.txt`), plus a live run of the checker
(`scratch/RevC5Bounds/conform-live.txt`, `conform-live-2.txt`) and an empirical drain PoC (`scratch/RevC5Bounds/poc-drain.py`).

## Verdict: FAIL

Fail rules applied verbatim: (a) calls without a timeout exist — one unbounded `proc.communicate()` in each
counter (`count-c1.py:129`, `count-c4.py:99`); (b) the checker's `popen=True`/`cap=True` PASS is asserted by
substring scans that never visit those `communicate` calls or the cap application site (conform.py:96, :100-103).

## AST table (scored-tip blobs; every exec-family call, verbatim from `ast-audit.txt`)

### `.ufo/waves/round-38/count-c1.py` (48,142 bytes)

| line | call | kwargs | `timeout=` |
|---|---|---|---|
| 113 | `subprocess.Popen` | cwd, env, start_new_session, stderr, stdout, text | — (Popen takes none; bound comes from `communicate`) |
| 116 | `proc.communicate` | timeout | `timeout` (=`run()` arg, default 120) |
| 123 | `proc.communicate` | timeout | `TOOL_GRACE_S` (=5, c1:80) |
| **129** | **`proc.communicate`** | **(none)** | **absent — unbounded** |
| 136 | `run` (own helper, all `git()` calls route here) | env, timeout | `timeout` (default 120) |
| 556 | `run` (`run_tool`) | cwd, env, timeout | `_TOOL_BUDGET[0]` (=`max(1, --tool-timeout)`, c1:938,959) |

- No direct `subprocess.run` call exists; every subprocess invocation routes through the bounded helper.
- `MAX_BLOB_BYTES` def `4*1024*1024` (c1:73); **enforced** at c1:991-1001 — `cat-file -s` size gate, setup-error
  exit 2 before the `git show` content read at c1:1003. Cap present and operative: **4 MiB** on the tool blob.

### `.ufo/waves/round-38/count-c4.py` (13,759 bytes)

| line | call | kwargs | `timeout=` |
|---|---|---|---|
| 83 | `subprocess.Popen` | cwd, env, start_new_session, stderr, stdout, text | — (Popen) |
| 86 | `proc.communicate` | timeout | `timeout` (=`run()` arg, default `SELFTEST_BUDGET_S`=120) |
| 93 | `proc.communicate` | timeout | `SELFTEST_GRACE_S` (=5) |
| **99** | **`proc.communicate`** | **(none)** | **absent — unbounded** |
| 113 | `subprocess.run` (`cat-file -e`) | capture_output, env, timeout | 120 |
| 117 | `subprocess.run` (`cat-file -s` size gate) | capture_output, env, text, timeout | 120 |
| 124 | `subprocess.run` (`git show` content read) | capture_output, env, text, timeout | 120 |
| 132 | `subprocess.run` (`cat-file -e`, `resolves()`) | capture_output, env, timeout | 120 |
| 202 | `run` (`selftest_arms`) | cwd, env, timeout | `SELFTEST_BUDGET_S` |
| 227 | `subprocess.run` (`rev-parse`) | capture_output, env, text, timeout | 120 |

- `MAX_BLOB_BYTES` def `8*1024*1024` (c4:50); **enforced** at c4:121-123 — `cat-file -s` gate raises
  `BlobTooLarge` before the `git show` at c4:124, inside `show()` so it covers **every** blob read the counter makes.
- Excluded from the table as non-primitives: `run_tool`, `run_negative`, `blind_arm`, `real_arm` wrappers — each
  routes to the bounded `run()`; grep confirms no `os.system`, `os.popen`, `subprocess.call/check_output`,
  `.wait(`, `pty`, `asyncio`, `multiprocessing`, `concurrent` anywhere in either file.

## Checker detail line (live, this run; byte-identical to `evidence/c5-after.txt`)

```
check bounded_reads    PASS (count-c1.py: run=True popen=True cap=True mkdtemp=True scratch=True; count-c4.py: run=True popen=True cap=True mkdtemp=True scratch=True)
```

Full run `CONFORM=met`, `EXIT=0` (`scratch/RevC5Bounds/conform-live-2.txt`; first live run identical).

## Findings, by severity

### F1 HIGH — `bounded_reads` reports PASS over two unbounded waits it never parsed

The claim is "bounds every child and git read by a timeout". In each counter's `run()` the SIGTERM→grace→SIGKILL
escalate ends in a **timeout-less `proc.communicate()`** (c1:129, c4:99). That call is the deciding site for
"every child wait bounded" and the checker's parse does not contain it: `static_checks` (conform.py:100-104)
requires only `start_new_session` inside the `Popen` segment plus the **file-level substring**
`"communicate(timeout="` — satisfied by c1:116/123 and c4:86/93, which exist regardless of what :129/:99 do.
The selftest `bounded_reads` mutation (conform.py:218-221) only strips `timeout=` from the `git()` helper call;
no mutation can reach the drain, so the check is structurally un-verifiable by selftest.

Empirical: `poc-drain.py` replicates the exact escalate sequence; a `setsid`'d grandchild holding the stdout pipe
kept `communicate()` blocked **4.51 s after** the SIGKILL deadline (`t=6.01 returned` vs `t=1.50 last deadline`).
Scale the grandchild's hold to a live process and the counter hangs indefinitely — the precise runaway the r37
SentTools item was routed to close, closed only until a descendant escapes the group (`killpg` cannot reach it;
`start_new_session` does not constrain grandchildren).

### F2 MEDIUM — `cap=True` is substring presence, not an enforced-cap parse

`blob_cap = "MAX_BLOB_BYTES" in source and '"-s"' in source` (conform.py:96) cannot distinguish a defined-but-unused
constant from a gate; a counter naming `MAX_BLOB_BYTES` in a dead constant plus any `cat-file -e`/`"-s"` string would
PASS with an uncapped read. (On the real bytes the cap **is** enforced — c1:991-1003, c4:121-123 — so this is
checker weakness, not a counter defect.) Additionally the `cap` leg is gated **only on `counters[0]`**
(conform.py:184-188 `if path == first: ok = ok and blob_cap`), yet the detail prints `cap=True` for count-c4 —
a displayed field not part of `ok`, conflating checked and unchecked truth in the same line. Claim-scoped
observation: c1's `git show` reads of the **registry** blob (c1:635, c1:639) are timeout-bounded but byte-uncapped;
P-C5's singular "committed-blob read" names the tool blob, so this is notation, not a breach.

### F3 MEDIUM — `freeze-r38.txt` pins are stale at the scored tip

Committed `evidence/freeze-r38.txt` (unmodified at f725f30, verified via `git status`/diff) pins
`count-c1.py=4e59eeff…` and `count-c4.py=5d416a1c…`; the committed blobs at the scored tip are
`9ebf10a1…`/`3340d594…` (sha256, both equal to working copies). "Pins are recorded in freeze-r38.txt" is not true
of the scored bytes — outside my axis but a freeze-integrity defect any C1/C5 verdict built on those pins inherits.

### F4 LOW — exec-primitive coverage gaps in the checker

The `run_ok` rule keys on call name `run`/`Popen` only. `subprocess.call`, `subprocess.check_output`,
`os.system`, `os.popen` would be passed silently (none present today — verified by AST + grep on tip blobs).
Converse brittleness: a legitimately bounded `Popen` waited via `proc.wait(timeout=)` would FAIL `popen_ok`.

### F5 INFO — working-copy audit and concurrent WIP

`evaluate` reads `--counter` paths from disk (conform.py:177-183), not at `<rev>`; tip-versus-disk identity held at
measurement time by sha256. The lane is being concurrently edited by the orchestrator mid-wave-2: working
`conform.py` (`3bd3b0fe`, adds `dir=SCRATCH_ROOT` to selftest mkdtemp) and `count-c1.py` (`e6fa1e76`, `_scratch_parent`
fail-closed fix citing a `RevC5Scratch` finding) differ from tip; neither touches the exec helper, `communicate`
sites, or the cap — all findings reproduce identically on both byte sets.

## Residual risk

- Reachable hang: any counter child that spawns a detached descendant inheriting its pipes turns the last
  `communicate()` into an unbounded wait; `timeout_state`'s hang fixture doesn't exercise it.
- Checker selftest gives false assurance for the `bounded_reads` arm: the check can regress silently on any
  future counter that keeps one `communicate(timeout=` substring.
- Untracked WIP of the checker/counter means a re-run later today audits different bytes than the scored tip.

## Verification gaps

- Did not test whether `blind_arm`'s 24 sandbox `git` calls each honor a caller-supplied `timeout=` — all default
  to the helper's 120 s bound, which is bounded-but-long; flagged as adequate-not-tight.
- The grandchild-escape PoC runs the replicate, not the counter binary itself; same call sequence and same
  constants (verified line-by-line), so the blocked drain is c1:129/c4:99's own code path.

Tooling: no installs needed or made (stdlib `ast`, `subprocess`; GNU `timeout` for the PoC harness).

Report: .ufo/waves/round-38/w2/RevC5Bounds.md
