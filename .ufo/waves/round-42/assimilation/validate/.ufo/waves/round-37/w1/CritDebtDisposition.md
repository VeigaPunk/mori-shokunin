# CritDebtDisposition — r36 debt table attack

Scope: `.ufo/waves/round-37/contract.md:80-91` and `corpus/lessons/round-37.md:50-57`; scored tip `e57c58b57c025364e79d130fbdf764d2674d83d6`, entering tip `842a32074b5c7972e9728f3f629d83eb92f127c2`. Axes: calibration (b/c), freshness/evidence fidelity (a/h), operability (d/g), and safety/provenance (e/f). Artifact closure below is not an axis-score or admission ruling.

## One line per debt

- **(a) CLOSED-ARTIFACT:** `tools/mori-source-drift.py:398-416` names both policy arms; `corpus/knowledge/source-drift-hardening-r37.md:25-58` binds policies, sources and mutation kills; `.ufo/waves/round-37/evidence/c2-after.txt:3-11` records both kills, corpus bindings, `C2=met`, `EXIT=0`.
- **(b) CLOSED-ARTIFACT, specifically the routed N1 fixture class:** `.ufo/waves/round-37/count-c1.py:754-810` adds the real-clothing challenge and rejects a negative if any arm fails; `evidence/c1-after.txt:8-14` records the honest challenge passing and `memo-n1.py` rejected on the challenge. This does not certify immunity to every harness-keyed strategy.
- **(c) CLOSED-ARTIFACT:** `.ufo/waves/round-37/count-c1.py:540-572,688-707,729-750,771-785` checks deleted-id lines on blind, real and challenge arms; `evidence/c1-after.txt:13` records `summary-only.py` rejected for per-id mismatch; `corpus/lessons/round-37.md:34` connects this to QUALITY 107.
- **(d) CLOSED-ARTIFACT:** `tools/mori-round17-jj-regressions.py:1040-1069` scopes config redirection to observable environment roots and retains positive jj-file evidence when a workspace exists; `evidence/r17-jj-selftest-r37.txt:1-2` records `SELFTEST ok` and `EXIT=0`, matching lesson M4.
- **(e) OPEN, incorrectly claimed absent:** newly committed `evidence/c1-before-memo.txt:2`, `evidence/c1-before-summary.txt:2`, and `evidence/census-start.txt:16` contain absolute operator-home paths; the current `evidence/census-end.txt:16` does too. This contradicts `contract.md:88` and `corpus/lessons/round-37.md:52-53` verbatim; a formatter used by the new counter does not sanitize the old-counter/census captures.
- **(f) OPEN, behavior disclosed but the original obligation not closed:** `SCORECARD.md:2025-2026` routes restructuring to **avoid SIGKILL**, while new `count-c1.py:100-114` and `count-c2.py:77-91` still issue it after grace. `contract.md:44-47,89` and lesson `:53-54` disclose continued killing, but substitute a slow-versus-hung/timeout-classification boundary for the original no-kills debt; disclosure suffices only to carry this honestly as open, not to close it.
- **(g) CLOSED-ARTIFACT:** C1 allocates unique `mkdtemp` parents at `count-c1.py:763,872,892,932`; seed/index-derived `repo%02d` children (`:314`) are inside those unique parents, so same-seed concurrent runs do not share their scratch tree. No concurrency run performed.
- **(h) CLOSED-ARTIFACT:** `corpus/knowledge/source-drift-r36.md:23-37` distinguishes the historical seven from the dated nine and names S210/S211 with open-time hashes; `corpus/README.md:568-574` repeats the nine-row enumeration. This is inherited corrected prose, not a new correction this round.

## Strongest counterexamples and evidence

**E1 — direct pinned-byte counterexample to (e), fixable disclosure defect.** Commands run with lane-root cwd:

```text
git diff --name-status 842a32074b5c7972e9728f3f629d83eb92f127c2 e57c58b57c025364e79d130fbdf764d2674d83d6
```
Observed additions include `.ufo/waves/round-37/evidence/c1-before-memo.txt`, `c1-before-summary.txt`, and `census-start.txt`; these are new round-37 files, not untouched round-36 receipts.

```text
git show e57c58b57c025364e79d130fbdf764d2674d83d6:.ufo/waves/round-37/evidence/c1-before-memo.txt
```
Observed line 2: `tool: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-37/fixtures/memo-n1.py`.

```text
git show e57c58b57c025364e79d130fbdf764d2674d83d6:.ufo/waves/round-37/evidence/census-start.txt
```
Observed line 16: `mori\tok\t/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`; line 17 `EXIT=0`. Thus the claim fails even without counting later/current receipts. Additional new source files also embed absolute lane paths (`count-c1.py:53`, `count-c2.py:42`, `fixtures/memo-n1.py:14`, `fixtures/summary-only.py:12`); these source constants are distinct from, and unnecessary to prove, the evidence-hygiene failure.

**F1 — original obligation versus disclosed replacement.** Read commands and observed text:

- `read(SCORECARD.md:2025-2028)` → “restructure the frozen counters' timeout path to avoid SIGKILL of the sandbox child”.
- `read(.ufo/waves/round-36/w2/RevNoHarm.md:11-13)` → the child-only kill is explicitly described as violating the literal no-kills boundary; `read(.ufo/waves/round-36/evidence/freeze-v3.txt:21-22)` → “r37 debt to restructure”.
- `read(.ufo/waves/round-37/count-c1.py:92-114)` → `os.killpg(os.getpgid(proc.pid), signal.SIGTERM)` at line 102, then `signal.SIGKILL` at line 109; `read(.ufo/waves/round-37/count-c2.py:71-91)` → corresponding calls at lines 79/86.
- `read(.ufo/waves/round-37/contract.md:44-47,88-90)` → grace-period killing and slow/hung uncertainty are disclosed, with no explicit open no-kills disposition. The advertised disclosure “in C1's predicate output” is also not present in the printed `PREDICATE` at `count-c1.py:42-51` or `evidence/c1-after.txt:1`; the timeout prose is elsewhere.

A timeout-cleanup exemption is a policy tradeoff for the canonical judge, not an exemption this critic can create. No timeout/SIGKILL experiment was run: static evidence establishes that the operation remains, without violating this review's own no-kills bound.

## Receipt observations, not reruns

- `read(.ufo/waves/round-37/evidence/c1-after.txt:1-16)` → blind `24/24`, real/challenge `pass`, all three negatives `rejected`, `C1=met`, seed `13985344346805549517`, `EXIT=0`. The recorded producer command is `python3 .ufo/waves/round-37/count-c1.py e57c58b5` (`SCORECARD.md:2065`); not executed by this critic.
- `read(.ufo/waves/round-37/evidence/c2-after.txt:1-11)` → six named selftest arms pass, `cap_kill PASS (exit=1 huge_cap=FAIL)`, `redirect_kill PASS (exit=1 redirect_private_refused=FAIL)`, remaining bindings PASS, `C2=met`, `EXIT=0`. Recorded producer: `python3 .ufo/waves/round-37/count-c2.py e57c58b5` (`SCORECARD.md:2066`); not rerun.
- `read(.ufo/waves/round-37/evidence/r17-jj-selftest-r37.txt:1-2)` → `SELFTEST ok`, `EXIT=0`; recorded producer is `tools/mori-round17-jj-regressions.py --selftest` (lesson M4); not rerun.

## Smallest safe correction

Append a truthful correction marking (e) open and (f) open under its original avoid-SIGKILL/no-kills identity; do not describe either as a discharged counter property. Preserve frozen historical receipts, and bind any superseding, repo-relative evidence capture explicitly rather than silently rewriting the old bytes. Closing (f), rather than merely reporting it open, requires a no-kills-compatible implementation or an explicit exemption from the canonical authority; neither is established here. No remediation performed.

Only this report was written. No tools installed or updated; no counters, selftests, mutations, kills, or other runtime invoked. Read-only git inspection and an ancillary `strings` inspection were used; the latter exposed an absolute source filename in the C1 bytecode, while the C2 bytecode path was absent in the changing worktree, and neither observation is needed for the verdict.

Report: .ufo/waves/round-37/w1/CritDebtDisposition.md
VERDICT: FAIL
