# Round 42 verifier spot-check

author: hyaku closure (non-author integrator, Kimi fresh closure agent)

Reviewer: hyaku-closure (Kimi fresh closure agent, non-author). Did not author
the round. Verified committed bytes; did not amend counters, did not start
round 43, did not re-file the OpenAlex L0.

## Conformance

- Report `.ufo/reports/round-42/mori.md` is committed by `mori-shokunin
  <mori@shokunin.local>` at `93394cb377c9856a8789607a26ff6b1f8bb0da12`
  (2026-10-24 20:55:39 -0300). That commit is an ancestor of fleet `HEAD`.
  `SHONEN` heading present, four boxes, marks `[ ]` with inline `[~]`
  pointers, no `[x]`. Not a marker. Not promotion-ready: no named non-author
  `[x]`. Promotion stays operator-owned.
- Prompt `.ufo/prompts/mori-round-42.md` carries the template contract
  (sections 1–5: claims, frontier/census, L2 floor, report path
  `.ufo/reports/round-42/mori.md`, SHONEN, commit-then-push, push scope, L0).
  No lane-hardcoded L2 route map; the host route table is named.
- Cited lane commits `249c7e73`, `316f3dcf`, `34b92673`, `f3ec0977`,
  `62b95e51` exist, are authored `mori-shokunin`, and are ancestors of
  `master`. Entering tip `9de7323d` is an ancestor of the closure tip.
- Closure tip `2520032569dae65511e7a347181004b530d99174` is pushed
  (`jj-lane.sh state`: `ahead=0 behind=0`; `ls-remote origin refs/heads/master`
  matches). `git status --porcelain` empty. `HEAD` is detached at that same
  hash; ancestry was tested against `master`.
- Defect, status-neutral: the report cites landed tip `62b95e51` and was
  fleet-committed before `25200325` (20:56:05 -0300). That later commit is
  the one that adds `corpus/evidence/sources-r42/S235.pdf` (absent at
  `62b95e51`) and deletes the recursive scratch mirror (10645 paths under
  `assimilation/validate/.ufo`). The PDF resolves at closure. Report did not
  land last.
- Dispatch digest (watchdog.log, mutable): `2026-10-24T11:17:51-03:00 launch
  mori round=42 pgid=162932 driver=hyaku-inline attempt=1`;
  `2026-10-24T20:58:07-03:00 complete mori round=42; hyaku-inline attempt=1`.
- L0 already filed as `527fc8dd5f36a7f7ee45aff66f0e3daf413222de` (mori
  identity, ancestor of fleet HEAD). Not re-filed.

## Claims

Re-measured at `2520032569dae65511e7a347181004b530d99174` unless noted.
Counters were not amended after freeze (`git diff 249c7e73..25200325` on
`count-c1.py` `count-c2.py` `count-c3.py` `contract.md` is empty).

### C1 operability — not verified (honest stop)

Command: `python3 .ufo/waves/round-42/count-c1.py 2520032569dae65511e7a347181004b530d99174`

Observed: 28 checks PASS, including `v5_selftest_17` `pass=17 fail=0`,
each committed mutant `pass=16 fail=1` on exactly its own arm
(`timeout_scope_walrus_positive`, `timeout_scope_tupleunpack_positive`,
`timeout_scope_source_order`), and `v5_routed_four` unchanged. Then:

```
TypeError: run() got an unexpected keyword argument 'cwd'
```

at `count-c1.py:244` (`run(..., cwd=clone)`; `run()` at line 93 takes no
`cwd`). Exit 1. No `C1=` line. Same crash as committed
`evidence/c1-after.txt:30-41`. Graded on that frozen counter, not on the
28 passes and not on `evidence/c1-noharm-manual.txt`. The counter was not
amended. Axis: `unprovable`.

### C2 calibration — verified (re-measured)

Before `9de7323d`: `C2=unmet` exit 1 (round-42 LOG/SCORECARD errata absent).
After tip: `C2=met` exit 0. The counter re-derived the r41 correction from
committed r41 bytes: 19 w1 reports, scribe 5 / scout 1, attack 31/64
(reviewer 12 + critic 11 + mutation-tester 8), 3 SURVIVED reports. Those
three files exist and each carries `SURVIVED` (`MutC1Walrus.md`,
`MutC1Tuple.md`, `MutC1DropSort.md`). LOG and SCORECARD round-42 records
name the three superseded claims. Axis: `improved` (score held at 5).

### C3 depth — verified (re-measured)

Before `9de7323d`: `C3=unmet` exit 1 (manifest unreadable). After tip:
`C3=met` exit 0. Independent `git diff-tree --no-renames --name-only -r
d72ac167535229d737b9fa844513431d9a12f5ea` prints 165 paths = 145 inherited
(67 `.ufo/waves/round-40/w1/*.md`, 7 other `.ufo/waves/round-40/`, 71
`.scratch/`) + 20 named-freeze. Manifest fences at the tip name exactly
that 145-set (missing 0, extras 0). Axis: `improved` (score held at 5).

### No-harm (closure measurement, not a C1 pass)

`git diff --numstat 9de7323d 25200325 -- SCORECARD.md` is `43 0`. No axis-row
deletions. `SKILL.md`, `PROVINCE.md`, `SHONEN.md` unchanged. Scores held:
coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6.
The frozen counter's own no-harm check did not run (the `cwd` crash is
before `tools/mori-sources-appendonly.py --selftest`). That gate was not
executed here.

## Axes

| axis | verdict | why |
|---|---|---|
| operability | unprovable | C1 frozen counter crashes; no `C1=` line |
| calibration | improved | C2=met; r41 false tallies superseded and re-derived |
| depth | improved | C3=met; 145/145 inherited paths named |
| coverage | unchanged | frontier notes only; score held; PROVINCE untouched |
| freshness | unchanged | new rows carry recheck; no freshness-axis move |
| adjacency | unchanged | detection/report only; no remediation |

No axis harmed.

## Spot-check

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S235 | admit | committed `corpus/evidence/sources-r42/S235.pdf` (pdftotext) | agree | Quote present at extracted lines 1143–1144 (`无法成功捕捉容器 oom 事件`). File sha256 `9855a4986a312dfc946b1b97b6010a8e4f1e65a4a30dca99359e6df057ad8020` matches the knowledge entry, not the SOURCES anchor (see routed). |
| S262 | admit | committed `corpus/evidence/sources-r42/S262.oa.json` abstract inverted index | agree | Reconstructed abstract contains the 20-word quote beginning "Our study shows that Linux cgroups…". Scope is abstract-level. Tier-A question already filed (`527fc8dd`); not re-filed. |
| S347 | admit | live https://docs.python.org/3/library/ast.html#ast.walk and committed `S347.html` | agree | 18-word quote "Recursively yield all descendant nodes in the tree starting at node (including node itself), in no specified order." present in both. used-by path exists. recheck `90d`. |
| S268 | reject | `curl -sI` doi.org/10.1109/TSC.2026.3698682 and ieeexplore `/document/11540439` | agree | Both return HTTP 202, content-length 0. OpenAlex locations have `pdf_url` null and work `has_fulltext` false. Refusal stands. stampPDF from this session returned HTTP 418 HTML (15410 bytes), not a PDF — the lane seat's flip is not confirmed here. Not re-admitted. |

Census: `scripts/sources-census.sh validate --root … mori` exit 0, rows 238
(entering tip 231). Malformed 0. Duplicate ids: none. New ids S232–S235,
S241, S262, S347 absent at `9de7323d`. S244 and S268 absent from the
registry and uncited by the two admitted entries. New-row cells: opened
`2026-10-24`, recheck `180d` or `90d` (not prose), used-by paths exist, no
pipe in teaches, 11 columns. Indented-row guard: column-zero pattern hits 0
on `assimilation/guard/SOURCES.md`; 0–3-space pattern hits 1 (`S232`). The
guard file `collisions` containing `S232` is that fixture catch, not a
registry collision. Mirror re-run from
`assimilation/validate`: `validate --file corpus/SOURCES.md` exit 0.

## Trends

- expansion — improved. Two admitted entries
  (`oom-evidence-loss-r38.md`, `oom-victim-context-r41.md`) cite mined rows
  opened this round, on FR1 / FR1–FR13 ground `corpus/README.md` "Round-42
  coverage additions" says the map did not hold as core. S347 entry cites
  its own mined row. Registry 231 → 238, census exit 0.
- quality — improved. The three false r41 claims are superseded in
  append-only LOG and SCORECARD, and C2 fails a re-assertion. C3's
  set-membership arm is what the swap mutant hits. Not rested on C1.
- discernment — improved. This spot-check agrees with the S235/S262/S347
  admits and the S268 reject. The flip was reported, not silently admitted.
  Wave seats are still the lane; they are not this check.

## Wave and mutant evidence

One dispatch payload `counts.spawn=64` (`evidence/wave-dispatch.json`).
Registry `w1/swarm-registry.json` has 64 members, every `agentId` null.
Committed `wave-parent-out.txt` is two lines and does not contain the
name→id map. 18 reports on disk, all in the registry; 46 registry members
have no report. Returned mix: reviewer 6, critic 6, mutation-tester 5,
scout 1. Missing seats are a shortfall, not attack evidence. Returned
attack evidence is those 17 reports, not the dispatched 31. L2 floor of 8
in one batch is met. The 46 dead seats are not credited.

C1's three arm kills were re-measured by the frozen counter (above) and
then the counter crashed. C2/C3 counter-mutant kills are evidenced in
committed transcripts, not re-executed here: `w1/MutC2Record.md` prints
`C2=unmet` rc 1 on the re-asserted `8/8` mutant; `w1/MutC3Manifest.md`
prints `C3=unmet` rc 1 with the swapped path missing and the decoy extra.
Lane tree after those commits is clean (recursion removed; working tree
empty; tip pushed).

## Routed defects (next round)

1. C1 stays unverified. Do not amend frozen `count-c1.py`. A successor
   measurement must complete, including no-harm, and print `C1=`.
2. S235 SOURCES anchor sha256 is transposed (`a30cda99` in the row vs
   actual `a30dca99` on the PDF and in the knowledge entry) and the row
   says byte-identical. Append a correction; do not rewrite the row.
3. SCORECARD round-42 declaration table still says the C1 after-state is
   `C1=met`. The measured-outcome section contradicts it. Append-only
   correction.
4. S268 flip is not closure-confirmed (stampPDF HTTP 418 here). Re-gate
   only on a fetch this host can reproduce. Do not admit from the lane
   seat transcript. Already routed by the report; still open.
5. Report cited `62b95e51` and omitted `25200325`, the commit that landed
   the S235 PDF. Cite the closure tip next time; land the report last.
