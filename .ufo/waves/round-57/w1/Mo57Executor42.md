# Mo57Executor42 — C2 counter attack (mori round 57, wave 1)

Seat: Mo57Executor42 (leaf executor). Assignment: attack the frozen **C2** counter by
devising a fixture that makes it falsely report eight located claims or a mined S548
source; execute the frozen counter on the entering revision; inspect the counter
implementation; return exact evidence, counterexamples and verdict. No production edits,
no commits, no remediation.

Entering revision `53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2`; freeze `618562c72a03dc4d17386b715357f863fd327274`
(lane HEAD, unchanged). Counter under test:
`.ufo/waves/round-57/count-c2.py`, sha256 `0fe9e6f4cdde0ac14bd8cad907e948edcb8a51f7c950622cf84cae5f1f75f742`
— identical to `git show 618562c…:.ufo/waves/round-57/count-c2.py` (same sha256) and
never modified by this seat. The counter is absent at the entering revision
(`git cat-file -e 53e2b47:.ufo/waves/round-57/count-c2.py` → `fatal: … exists on disk, but not
in '53e2b47…'`, rc=128), so the file under test is exactly the frozen one.

## 1. Baseline: frozen counter on the entering revision

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ python3 .ufo/waves/round-57/count-c2.py 53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2
C2=unmet claims=0 source=bad rev=53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2
EXIT=1
$ python3 .ufo/waves/round-57/count-c1.py 53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2
C1=unmet rows=0 evidence=bad rev=53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2
EXIT=1
```

Reproduces `.ufo/waves/round-57/controls.txt` exactly (same strings, same exit codes).
Entering-revision registry facts used below: `corpus/SOURCES.md` 393 lines, **271**
occurrences of `mined`, **0** occurrences of `S548`; the entry
`corpus/knowledge/watchdog-unclosed-r57.md` does not exist (rc=128).

## 2. The frozen counter, line by line (what it actually measures)

```
 4  R=sys.argv[1]; repo="/home/vgpnk/Projects/shokunin/mori-shokunin"
 5  def show(path):
 6   p=subprocess.run(["git","-C",repo,"show",f"{R}:{path}"],capture_output=True,text=True)
 7   return p.stdout if p.returncode == 0 else None
 8  entry=show("corpus/knowledge/watchdog-unclosed-r57.md")
 9  registry=show("corpus/SOURCES.md")
12  claims=[x for x in entry.splitlines() if x.startswith("| K")]
13  source_ok="S548" in entry and "| S548 |" in registry and "mined" in registry
14  quote_ok=all("`" in x and "`" in x for x in claims)
15  ok=len(claims)==8 and source_ok and quote_ok and "pairing count" in entry
```

Four mechanical observations:

* **D1 (line 14, duplicated conjunct).** `"`" in x and "`" in x` is the *same predicate
  twice*: `quote_ok` needs **one** backtick per row. No pairing, no closure, no content.
* **D2 (lines 8–9, no source is ever read).** The only two paths read are the entry and
  `SOURCES.md`. No anchor column, no `corpus/evidence/…` copy, no `tools/…` file is opened.
  "Each claim with a located quote in the source copy" is therefore *outside what the
  counter can falsify* — the quotes need not exist anywhere.
* **D3 (line 13, three substring tests).** `"S548" in entry` is satisfied by any mention
  (including a rejection note, while `source:` names another row). `"| S548 |" in registry`
  is satisfied by any table row, whatever its status/anchor/opened date. `"mined" in registry`
  is satisfied by **any other of the 271 `mined` occurrences** — so S548's own row may be
  `queued`/unopened. Nothing compares the row against the entering revision, so "newly
  opened" is unchecked (S548 count at entering rev: 0).
* **D4 (line 15, substring semantics).** `"pairing count" in entry` matches a *negated* or
  *rejecting* sentence. Nothing tests "rather than a present-running count", and the
  "opens with `source:`/`verified-at:`/`recheck:`" clause is never inspected at all.
* **D5 (line 6, `R` verbatim).** `R` is interpolated into `git show {R}:{path}` with no
  revision validation: any ref works (`forged-ref`), and `R=""` degenerates to
  `git show :<path>` — the **staged index**, i.e. a non-revision that no commit records.

## 3. Probe matrix (frozen counter, unmodified)

Method: one scratch git repo (`/fast/scratch/hyaku/mori-r57/Mo57Executor42/fixture`,
`git rev-parse --show-toplevel` asserted `== fixture` before every mutation, all git calls
via explicit `git -C`). The frozen counter was run **as written** with
`GIT_DIR=<fixture>/.git GIT_WORK_TREE=<fixture>` so its own `git -C repo show R:path`
resolves inside the fixture (verified: `GIT_DIR`+`GIT_WORK_TREE` wins over `-C`;
`GIT_DIR` alone does not). No copy of the counter exists; no lane file was written.
Drivers: `drive.py`, `drive2.py`, `drive3.py` (retained with `probe-log*.txt`).

| Probe | Fixture content | Output | Exit |
|---|---|---|---|
| P1 full forgery | 8 claim rows, quotes fabricated (absent from every source copy), `source: S001 (… S548 was considered and rejected)`, S548 registry row `queued`/`opened 2020-01-01`/anchor `-`, no `verified-at`/`recheck` lines, negated pairing sentence | `C2=met claims=8 source=ok quotes=ok rev=042bdb9a525e6a401c1fb748b04d293aedd0d7f7` | **0** |
| P2 one backtick/row | as P1, every row carries a single **unbalanced** backtick | `C2=met claims=8 source=ok quotes=ok rev=9b89b2d3a5346140b9d478667e53d057f11bd8c6` | **0** |
| P7 duplicate rows | eight **identical** rows, one fabricated quote repeated | `C2=met … rev=921e17c0eec85ee017fd45fc17221f6910abc308` | **0** |
| P8 `R=""` (index read) | forged entry staged only; the commit holding that path is benign | `C2=met claims=8 source=ok quotes=ok rev=` | **0** |
| P8 control | same fixture, benign commit | `C2=unmet claims=0 source=bad quotes=ok rev=dda94323…` | 1 |
| Q1 semantic inversion | body: “`unclosed` counts the driver processes running right now”; phrase `pairing count` survives only in `The phrase "pairing count" does not describe this field.` | `C2=met … rev=17fbc3da078d0670d1e305dcf4cced6559a22185` | **0** |
| Q2 fenced rows | the eight rows sit inside a ```` ``` ```` code block | `C2=met … rev=ccc951109a9c7ca32c7ee689e1a70ec7d7255a8f` | **0** |
| Q4 arbitrary ref | tag `forged-ref` on the forged commit | `C2=met … rev=forged-ref` | **0** |
| T3 self-referential quotes | `| Ki | \`see Ki\` |` — quotes name their own row, no source text | `C2=met … rev=22f56bb3641bbeaad9be26ca843d52f3901da073` | **0** |
| T1 true positive | eight quotes that really are substrings of the cited copy | `C2=met … rev=ebf671965d2fa86a1d6d172d05d7a98bb189a129` | 0 |
| P3 seven claims | 7 rows | `C2=unmet claims=7 …` | 1 |
| P4 no S548 row | registry without S548 | `C2=unmet … source=bad …` | 1 |
| P5 no backticks | 8 rows, zero backticks | `C2=unmet … quotes=bad …` | 1 |
| P6 no phrase | no `pairing count` substring | `C2=unmet …` | 1 |
| T2 honest bullets | eight genuine located claims written as `* claim: \`…\`` | `C2=unmet claims=0 …` | 1 |

**Fabrication check** (quotes used in P1 are real strings only in the fixture, absent from
the actual source copies). `grep -rF` over `tools/mori-driver-liveness.py` and
`corpus/evidence/sources-r56/` returns **count=0 for all eight**, e.g.
`count=0 :: unclosed equals the number of running driver processes`,
`count=0 :: a wrap never closes a round`.

**Minimum counterexample** (P1, verbatim entry):

```
# unclosed pairing reading

source: S001 (not S548; S548 was considered and rejected)

This entry does not show that `unclosed` is a pairing count rather than a present-running count.

| id | claim |
|---|---|
| K1 | `the kernel reports live process counts per lane` |
| K2 | `unclosed equals the number of running driver processes` |
| K3 | `every launch line is authenticated by the writer` |
| K4 | `the watchdog daemon owns the pairing table` |
| K5 | `rounds are closed by the kernel scheduler` |
| K6 | `malformed lines are silently dropped` |
| K7 | `a wrap never closes a round` |
| K8 | `the log carries a monotonic sequence number` |
```

with registry `| S548 | forged row, never opened | own-work | A | x | - | - | queued | 2020-01-01 | never | - |`.
This entry cites no S548 row as its source, contains no opened/recheck line, has zero
source-copy reads behind any quote, states the *opposite* of the required pairing claim,
and the counter reports `C2=met claims=8 source=ok quotes=ok` exit 0.

## 4. Ground truth for what the entry must actually say

`tools/mori-driver-liveness.py` at the entering revision: `"in_flight": row["last_event"] == "launch"`
(line 172), `"unclosed": len(row["open_launches"])` (line 173), and the docstring line 239
`"in_flight/unclosed are log-shape facts, not health verdicts"`. `open_launches` is appended
on `launch`, removed on `complete`/`wrap`, and pruned per-round on
`lane-dead-no-report` — i.e. `unclosed` is a **launch/close pairing count**, and it is
neither a running-process gauge nor a health verdict. P1/Q1 satisfy the counter while
contradicting this ground truth; the counter has no access to the distinction.

## 5. Verdict

**Attack succeeds; the C2 predicate is not established by its counter.** `C2=met` is
produced by content that fails at least five contract clauses at once:

1. “cites a newly opened source row” — S548 row may be `queued`, opened 2020-01-01, no anchor (D3; P1).
2. “each with a located quote in the source copy” — no source copy is ever opened; eight
   fabricated quotes pass (D2; P1), as do one-sided backticks (D1; P2), duplicates (P7),
   self-references (T3), and rows inside a code fence (Q2).
3. “opens with `source:` / `verified-at:` / `recheck:`” — unparsed; P1 omits two of the three.
4. “states that `unclosed` is a pairing count rather than a present-running count” —
   substring match admits negation (P1) and inversion (Q1).
5. “measured at revision R” — `R` is unvalidated: any ref passes (Q4), and `R=""` reads the
   staged index with no commit behind it (P8: `C2=met rev=` while the committing rev gives
   `C2=unmet claims=0`).

Conversely the counter is also **under-inclusive**: an honest entry listing eight genuinely
located claims as bullets reports `C2=unmet claims=0` (T2). Passing and failing are both
decoupled from the predicate, so a wave-2 `C2=met` cannot be read as evidence of depth
(axis 5) and a wave-2 `C2=unmet` cannot be read as absence of a sourced entry.

Residual discrimination that *does* work (useful as partial checks only): row count ≠ 8
(P3), missing `| S548 |` registry row (P4), zero backticks (P5), absent `pairing count`
substring (P6).

## 6. Limits of this seat's method (stated, not hidden)

* The frozen counter hardcodes its repo path, so the fixture content was reached by
  redirecting git repository discovery (`GIT_DIR`+`GIT_WORK_TREE`) rather than by editing
  the counter. The attacked logic is byte-identical to the frozen file
  (sha256 `0fe9e6f4…`, equal to `git show 618562c…:.ufo/waves/round-57/count-c2.py`).
  What this bypass does **not** test is the hardcoded repo constant — no claim is made about it.
* `R=""` (P8) is demonstrated in the fixture only. The in-lane variant (stage without
  committing, run `count-c2.py ""`) was **not** attempted: staging in the lane repo is a
  repository mutation and out of this seat's bounds. It follows from the code (line 6) but
  is unreproduced in-lane.
* Counters and predicates are frozen; no fix was proposed or applied. Findings only.
* No secrets, tokens, session material or private URLs were read or reproduced.

## 7. State and artefacts

* No production edits, no commits, no tags in the lane repo: `git status --porcelain=v1 -- corpus/`
  is empty; lane HEAD is still `618562c72a03dc4d17386b715357f863fd327274`. The `forged-ref` tag
  exists only inside the scratch fixture repo.
* Scratch: `/fast/scratch/hyaku/mori-r57/Mo57Executor42/` — drivers `drive.py`, `drive2.py`,
  `drive3.py` and logs `probe-log.txt`, `probe-log2.txt`, `probe-log3.txt` retained; the
  scratch fixture repository (`fixture/`, disposable, rebuilt by `drive.py`) removed after
  the run. `TMPDIR` never left the scratch dir; nothing was written under `/tmp`.
* Disk guard checked before work: `/fast/scratch/hyaku` 27% used, 590 G free. No package
  manager or tool install was performed.
