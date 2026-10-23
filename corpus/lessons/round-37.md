# Round 37 — 2026-10-23 (L1 MoriR37, attempt 1)

## Gate

Candidates this round (five, all opened 2026-10-23; copies under `corpus/evidence/sources-r37/`):

| candidate | decision | URL, access date, located quote (≤25 words) |
|---|---|---|
| S221 — HTTP Semantics (RFC 9110) §15.4 | **admitted** (mined) | `https://www.rfc-editor.org/rfc/rfc9110.txt`, opened 2026-10-23; §15.4 at `S221.src:7230-7234`: "The 3xx (Redirection) class of status code indicates that further action needs to be taken by the user agent in order to fulfill the request." |
| S222 — OWASP SSRF Prevention Cheat Sheet | **admitted** (mined, tier B: secondary) | `https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html`, opened 2026-10-23; "Unsafe redirect" note at `S222.src:5031`: "Disable the support for the following of the redirection in your web client in order to prevent the bypass of the input validation" |
| S223 — Python 3 `urllib.request` documentation | **admitted** (mined) | `https://docs.python.org/3/library/urllib.request.html`, opened 2026-10-23; `HTTPRedirectHandler.redirect_request` at `S223.src:1140-1142`: "does not strictly follow RFC 2616, which says that 301 and 302 responses to POST requests must not be automatically redirected without confirmation" |
| S224 — Yama LSM documentation | **admitted** (mined) | `https://docs.kernel.org/admin-guide/LSM/Yama.html`, opened 2026-10-23; `ptrace_scope` level 1 at `S224.src:217-221`: "1 - restricted ptrace: a process must have a predefined relationship with the inferior it wants to call PTRACE_ATTACH on." |
| S225 — Fetch Standard §4.5 | **admitted** (mined) | `https://fetch.spec.whatwg.org/`, opened 2026-10-23; "HTTP-redirect fetch" at `S225.src:8355`: "redirect count is 20, then return a network error" |

Rejected: none new. S222's blanket "disable redirects" advice is admitted only for its countermeasure
scope; the probe must follow redirects, so the entry records the final-destination-only gap as a
limit instead (search-log note, `corpus/SOURCES.md`).

Registry changes old→new: none. All five rows are new (`queued` → `mined` in one step, each with a
citing `used-by` path: `corpus/knowledge/source-drift-hardening-r37.md`), and no existing row's
`status`, `recheck` or `used-by` cell was edited this round.

Gate notes for non-author verification: each quote above is contiguous in the committed copy named
by its `S###.src` file and at the line range given; `S223`'s quote is a mid-sentence fragment (the
sentence continues "…by the user"), quoted verbatim up to the 25-word guard; `S225` is a `<var>`-
interleaved sentence, quoted from "redirect count" to the end of the clause.

## Mistakes

| # | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M1 | harness (a mutation fixture that resizes with the value it mutates) | the first `huge_cap` arm built its fixture as `b"y" * FETCH_MAX_BYTES`; under the cap mutant (`1 << 40`) the selftest died with `MemoryError` instead of failing the arm, so the mutation was not a clean kill | the mutation probe itself (the run crashed rather than printing `FAIL`); no criterion named it before | the arm uses a literal `cap_body = 4 * 1024 * 1024` with the reason in place (`tools/mori-source-drift.py:402-403`); the mutant now prints `selftest huge_cap FAIL (over_cap=body at_cap=body len=4194304)` and exits 1. Shown able to fail: `.ufo/waves/round-37/evidence/c2-after.txt` `check cap_kill PASS`, and the pre-fix traceback is recorded in this round's scratch transcript |
| M2 | measurement (a negative fixture that does not reproduce the class it names) | the first `memo-n1.py` printed only the summary constant; the round-37 counter rejected it on the **real** arm (`rejected (real arm fails)`) — i.e. the per-id check caught it, not the challenge arm, so the fixture did not reproduce w2/RevNgC2 N1 | the counter's own per-negative detail line, which named the wrong arm | the fixture now also prints the 18 `changed` lines the published summary implies, so blind and real arms pass and only the challenge arm can reject it: `negative memo-n1.py rejected (challenge: lists differ …)`. Shown able to fail: the round-36 counter scores the same bytes `C2=met` (`evidence/c1-before-memo.txt`) |
| M3 | measurement (a counter that under-reads its tool's interface) — carried from round 36 | round-36 `count-c2.py` compares only the summary line, so a program omitting the contract's per-id `deleted <id>` lines passes it | r36 w2/MutC2Deleted limit 3 (recorded, no criterion then) | QUALITY 107 + `count-c1.py` parses the per-id grammar on every arm and rejects `fixtures/summary-only.py`; the r36 counter scores the same fixture `C2=met` (`evidence/c1-before-summary.txt`) |
| M4 | environment (a gate assertion that assumes a runtime side effect) — carried from round 36 | `tools/mori-round17-jj-regressions.py`'s `jj_config_redirected` required `$HOME/.config/jj` to exist, but jj 0.45.1 writes repo config only inside a jj workspace and the sandbox is git-only; 9/204 assertions red | r36 w2/ExecCensusRegression (routed as debt d) | the assertion is scoped to the testable redirect property (all config roots inside the case home, case home not the operator's home or an ancestor of it) and additionally requires the jj file when a sandbox carries a jj workspace. Shown able to fail: pre-fix 9/204 red (`corpus/lessons/round-36.md`, Collateral note), post-fix `--selftest` exit 0 (`evidence/r17-jj-selftest-r37.txt`) |

| M5 | packaging (a large new file inside a named commit directory is skipped) | `corpus/evidence/sources-r37/S225.src` (1,854,393 bytes) exists on disk and is cited by row S225 and the entry, but `git status --porcelain` after the first two helper commits still showed `?? corpus/evidence/sources-r37/S225.src`: the helper commits a named directory like `git add <dir>` and skips new files over 1 MiB | the post-commit `git status` sweep (no criterion named it before); the helper's own warning was not surfaced to the L1 | the file is committed by naming it explicitly (`52d636d5`); `git ls-tree 52d636d5 corpus/evidence/sources-r37/` now lists all five copies. Shown able to fail: the pre-fix `git status` line above, and the post-fix `ls-tree` listing |


## Round shape and debts

Round shape (orchestrator-inline contract): one validated v2 wave prepared and returned to the
orchestrator for inline dispatch (see the report). L1 work in this session: the freeze, both
counters, the three negative fixtures, the scoped j17 fix, the corpus rows and entries, both
scoring receipts.

r36 routed debts: (a) drift hardening verify + entry → claim C2; (b) memoization hardening → claim
C1; (c) per-id `deleted <id>` checks → claim C1 + QUALITY 107; (d) r17-jj environment → M4, fixed
and re-run green; (e) SentData path hygiene → the round-37 counters print repo-relative lane paths
(`display_path`) and no new evidence file carries an absolute operator path; (f) SIGKILL boundary →
disclosed as `tool_timeout` with SIGTERM-then-SIGKILL in `count-c1.py` and in the contract; (g)
seed-collision scratch → `tempfile.mkdtemp` per arm; (h) 9-vs-7 drifted prose → re-verified at
`corpus/knowledge/source-drift-r36.md:24-33` (nine, S210/S211 named) and `corpus/README.md`
Round-36 section. Frozen-byte residuals from round 36 remain frozen evidence and are not edited.

Misroot sweep: `git -C /home/vgpnk/Projects/shokunin status --porcelain` was run before the report;
no file under the fleet root names this lane/round (see the report's Misroot line).
