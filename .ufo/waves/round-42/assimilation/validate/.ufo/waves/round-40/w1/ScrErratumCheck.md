# ScrErratumCheck — round-39 erratum verification (mori r40, w1)

Axes: (1) source fidelity of each erratum sentence, (2) provenance (committed
vs on-disk, and at which commit), (3) append-only discipline (round-39 bytes
unmodified), (4) the S227 word count.

Verdict: **the three named sources back the erratum's factual corrections.**
The c8-red-wait receipt refutes the old "bypass-wait likewise → met" sentence;
the S227 quote is 17 words, not 18; the r39 contract's `pass=11` is stale
against the gate's `pass=12`; and the c10 decoy pair is a working before/after
control. One LOW wording finding: the erratum's immutability rationale names
the registry anchor cell, but the "(18 words)" label under correction is not in
that cell. Five INFO notes (attribution, provenance, residual visibility) are
recorded below. No production edit was made; this report is the only write.

## Sources checked

| Erratum lines | Claim | Source read | Result |
|---|---|---|---|
| 3-4 | r39 fleet report + SCORECARD C2 row say r38 printed `CONFORM=met` on bypass-wait | `SCORECARD.md:2199`; fleet `/home/vgpnk/Projects/shokunin/.ufo/reports/round-39/mori.md:20-24,57-58` | backed |
| 5-7 | `c8-red-wait.txt` shows `CONFORM=unmet exit=1` / "not reproduced" | `.ufo/waves/round-39/evidence/c8-red-wait.txt:3,7,10,11` | backed |
| 6-8 | r38 rejected the final pure wait+read fixture via `bounded_reads` popen detection, not drain shape | same receipt (`check bounded_reads FAIL (… popen=False …)`; six-check list has no `drain_shape`) | backed |
| 8-9 | the intermediate form r38 accepted also passes the r39 checker | `corpus/lessons/round-39.md:86-89` (finding 11) | record-backed; no standalone receipt |
| 9-10 | no fixture is met-by-r38 and unmet-by-r39 via `drain_shape` | `corpus/lessons/round-39.md:86-89` | backed (lesson record) |
| 10-14 | drain_shape half re-claimed with a genuine before-control: r39 checker accepts decoy fixture; r40 checker rejects via `drain_bind` | `.ufo/waves/round-40/evidence/c10-red-decoy.txt`, `c10-after-decoy.txt` | backed |
| 14-16 | r39 report/SCORECARD sentence superseded; fleet report is committed fleet history outside lane write scope | erratum committed in `265a955`; fleet report last touched by `ce8debe`, reachable from fleet HEAD | backed |
| 18-20 | lesson Gate row labels the quote "(18 words)"; the quote is 17 words | `corpus/lessons/round-39.md:7`; `corpus/evidence/sources-r39/S227.src` (quote spans 2542-2544) | backed |
| 20-21 | r39 closure routed the label correction (routed defect 4) | `corpus/lessons/round-39-verifier-spotcheck.md:63` | backed |
| 21-22 | "the registry row's anchor cell is immutable, so the count is corrected here" | `QUALITY.md:919-920`; `SOURCES.md:292` | immutability rule true; location description imprecise (F1) |
| 24-25 | r39 contract prose `pass=11` was stale; the gate prints 12 | `.ufo/waves/round-39/contract.md:146`; `.ufo/waves/round-39/evidence/gate-selftest-after.txt` | backed |
| 25-27 | r39 C3 before-cell cites `fixtures/make-ancestry-dags.py`, a path in no commit | `.ufo/waves/round-39/contract.md:139`; `git log --all` empty; 0 objects match | backed |
| 26-27 | real builders are the pinned `run-c9-dags.py` plus the gate's embedded DAG selftest cases | freeze pin line 6; blob at `13bfba23`; gate lines 501/566 there | backed |
| 28 | both corrections recorded here; r39 bytes stay frozen | erratum sha `5cfea377…` at `265a955`; no r39-dir commit or working-tree diff vs `265a955` | backed |

## Key receipt content

`c8-red-wait.txt` (verbatim, whole file):

```text
command: r38 conform bypass-wait.py
r38 conform on bypass-wait.py at 13f3db7e:
exit=1
check predicate        PASS (exit=0 equal=True)
check head_pin         PASS (pin=f920eaf7dbe85372a20b6710f1f4848c74d06c47 tip=f920eaf7dbe85372a20b6710f1f4848c74d06c47)
check tool_resolve     PASS (exit=0 resolved=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-38/fixtures/summary-only.py)
check bounded_reads    FAIL (bypass-wait.py: run=True popen=False cap=True mkdtemp=True scratch=True)
check timeout_state    FAIL (exit=None timeout_reason=False pass=False)
check scratch          PASS (bypass-wait.py: mkdtemp_dir=True root=True)
CONFORM=unmet
verdict: not reproduced
```

Decoy control (same fixture bytes, `.ufo/waves/round-40/fixtures/generated/survivor-decoy.py`):

```text
c10-red-decoy.txt  command: python3 .ufo/waves/round-40/fixtures/extracted/conform-v2-r39.py bb1f2457 --counter .ufo/waves/round-40/fixtures/generated/survivor-decoy.py
                   check drain_shape        PASS (violations=[])
                   CONFORM=met
                   EXIT=0
c10-after-decoy.txt command: python3 .ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --counter .ufo/waves/round-40/fixtures/generated/survivor-decoy.py
                   check drain_bind         FAIL (survivor-decoy.py: violations=['Popen at line 143 not drained by a bound, consumed communicate in its function'])
                   CONFORM=unmet
                   EXIT=1
```

The fixture is the intended decoy shape (`make-survivor-fixtures.py:79-85`):
in `run_tool`, a dummy `Popen` is drained by `dummy.communicate(timeout=timeout)`
(`survivor-decoy.py:147-148`) while the real `proc` is drained by
`proc.wait(timeout=timeout)` + `proc.stdout.read()` (`:149-150`). Line 143 is
the real `proc = subprocess.Popen(...)`.

## Findings

- **F1 (LOW, wording):** erratum lines 21-22 say "the registry row's anchor cell
  is immutable, so the count is corrected here rather than by an in-place edit."
  The "(18 words)" label being corrected is in the round-39 lesson Gate row
  (`corpus/lessons/round-39.md:7`) and in the round-39 bounded-search log
  (`corpus/SOURCES.md:292`). The S227 registry anchor cell
  (`corpus/SOURCES.md:233`) carries the quote and location but **no word count**.
  The immutability rule is independently true (QUALITY 113 at
  `QUALITY.md:919-920`; `SOURCES.md:292` states the same rule for S226/S228),
  and the correction itself is valid and contract-directed; only the sentence's
  description of the corrected surface is imprecise. A tighter sentence would
  say the round-39 records are append-only (or cite the lesson/search-log
  surface). No edit made.
- **F2 (INFO, attribution):** the exact phrase "bypass-wait likewise" is
  verbatim only in `SCORECARD.md:2199`. The fleet report states the same claim
  in different words: "both bypass fixtures … print `CONFORM=unmet` … where the
  r38 checker printed `CONFORM=met` (`evidence/c8-red-none.txt`,
  `c8-red-wait.txt`)" (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-39/mori.md:20-24`)
  and the C2 before line at `:57-58`. The erratum's combined attribution is
  substantively accurate.
- **F3 (INFO, provenance limit):** the sentence "the intermediate form that r38
  accepted also passes the round-39 checker" (lines 8-9) rests on lesson finding
  11 text (`corpus/lessons/round-39.md:86-89`); no standalone receipt for the
  intermediate fixture survives. `grep -rl 'intermediate'` over
  `.ufo/waves/round-39/evidence`, `.ufo/waves/round-39/scratch` and
  `.ufo/waves/round-38/evidence` returned nothing. The adjacent negative
  sentence explicitly cites finding 11, so the paragraph is traceable, but this
  clause is record-backed rather than receipt-backed.
- **F4 (INFO, provenance):** both c10 decoy receipts are committed at `8d3badd`
  (the labeled evidence commit, child of the scored tip `265a955`) and also
  appear in `fab8eee` (empty-subject child of `265a955`); neither file is in
  `265a955` itself. The red side's checker bytes match the frozen r39 blob
  (sha `fe0be179…`, also freeze-r39 line 3), and the after side's checker and
  fixture match the `265a955` blobs (`5025b966…`, `cfdb030c…`), so the control
  is reproducible from committed bytes; the erratum's citation resolves at the
  evidence commit, not the instrument tip.
- **F5 (INFO, verified):** the fleet report is committed fleet history: its last
  touching commit is `ce8debe` ("round-39: mori report erratum — C2 survivor
  class detail (finding 8)"), reachable from fleet HEAD
  (`git merge-base --is-ancestor ce8debe HEAD` → yes). It lives at
  `/home/vgpnk/Projects/shokunin/.ufo/reports/round-39/mori.md`, outside the
  lane, so the lane write-scope statement is structurally true.
- **F6 (INFO, residual visibility):** the stale "(18 words)" text still stands at
  `corpus/lessons/round-39.md:7` and `corpus/SOURCES.md:292`; the erratum is the
  superseding record, so a reader of those files alone still sees the label.
  This is consistent with append-only correction, not a contradiction.

No erratum sentence was found to contradict its cited evidence. The one
factual-sensitive negative ("no single fixture was met-by-r38 and
unmet-by-r39 via `drain_shape`") is scoped by its finding-11 citation.

## Commands run and outputs

Read-only verification; no conform/gate/census re-run (executor/reviewer seats
own those). Git commands used are non-mutating; no jj command was run.

```sh
cd /home/vgpnk/Projects/shokunin/mori-shokunin
python3 -c 'import re; b=open("corpus/evidence/sources-r39/S227.src",encoding="utf-8").read(); q="you can ask for commits that are reachable from r2 excluding those that are reachable from r1"; f=re.sub(r"\s+"," ",b); print("present=",q in f); print("words=",len(q.split())); print("occurrences=",f.count(q))'
```
```text
present= True
words= 17
occurrences= 1
```

```sh
grep -n '18 words' corpus/lessons/round-39.md corpus/SOURCES.md
```
```text
corpus/SOURCES.md:292: … Located quotes: `S227.src:2542-2544` (the two-dot range sentence, 18 words); …
corpus/lessons/round-39.md:7: … `S227.src:2542-2544`: "you can ask for commits that are reachable from r2 … reachable from r1" (18 words) …
```

```sh
grep -n 'word-count label\|routed defect' corpus/lessons/round-39-verifier-spotcheck.md
```
```text
63:4. Lesson Gate: S227 quote word-count label says 18, actual 17.
```

```sh
grep -n 'pass=11' .ufo/waves/round-39/contract.md
cat .ufo/waves/round-39/evidence/gate-selftest-after.txt
```
```text
146:no fabricated edit on fixture C, `MORI_SOURCES_APPENDONLY_SELFTEST pass=11 fail=0`,
MORI_SOURCES_APPENDONLY_SELFTEST pass=12 fail=0
EXIT=0
```

```sh
git log --all --oneline -- .ufo/waves/round-39/fixtures/make-ancestry-dags.py; echo "LOG_EXIT=$?"
git rev-list --all --objects | grep -c 'make-ancestry-dags' || echo NO_OBJECT_MATCH
git ls-tree -r --name-only 13bfba23 -- .ufo/waves/round-39/fixtures/
```
```text
LOG_EXIT=0          # no commits
0
NO_OBJECT_MATCH
.ufo/waves/round-39/fixtures/hang-after-flush.py
.ufo/waves/round-39/fixtures/make-m19-bypass.py
.ufo/waves/round-39/fixtures/run-c7-reds.py
.ufo/waves/round-39/fixtures/run-c8-receipts.py
.ufo/waves/round-39/fixtures/run-c9-dags.py
.ufo/waves/round-39/fixtures/witness-comment-anchors.md
.ufo/waves/round-39/fixtures/witness-dangling-row.md
.ufo/waves/round-39/fixtures/witness-summary-only-live.txt
.ufo/waves/round-39/fixtures/witness-token-entry.md
```

```sh
grep -n 'run-c9-dags' .ufo/waves/round-39/evidence/freeze-r39.txt
sha256sum .ufo/waves/round-39/fixtures/run-c9-dags.py
git show 13bfba23:.ufo/waves/round-39/fixtures/run-c9-dags.py | sha256sum
git show 13bfba23:tools/mori-sources-appendonly.py | grep -n 'def _selftest_dag_cases\|def _make_dag_repo'
```
```text
6:d75d774092aac06da9690310782a4e95c83975c7e59282264dc71d04791e59b8  .ufo/waves/round-39/fixtures/run-c9-dags.py
d75d774092aac06da9690310782a4e95c83975c7e59282264dc71d04791e59b8  .ufo/waves/round-39/fixtures/run-c9-dags.py
d75d774092aac06da9690310782a4e95c83975c7e59282264dc71d04791e59b8  -
501:def _selftest_dag_cases():
566:def _make_dag_repo(path, kind, bodies, env):
```

```sh
sha256sum .ufo/waves/round-40/fixtures/extracted/conform-v2-r39.py
git show bb1f2457:.ufo/waves/round-39/conform.py | sha256sum
sha256sum .ufo/waves/round-40/conform.py
git show 265a955cc67be4eae97d2dc5a9338a25f31eb29b:.ufo/waves/round-40/conform.py | sha256sum
sha256sum .ufo/waves/round-40/fixtures/generated/survivor-decoy.py
git show 265a955cc67be4eae97d2dc5a9338a25f31eb29b:.ufo/waves/round-40/fixtures/generated/survivor-decoy.py | sha256sum
```
```text
fe0be179aba9df7150f0b6cdb50a5f9bbdb411efb1263b46ffa6b21d46ef7987  .ufo/waves/round-40/fixtures/extracted/conform-v2-r39.py
fe0be179aba9df7150f0b6cdb50a5f9bbdb411efb1263b46ffa6b21d46ef7987  -
5025b9664632d01063c11b4f5dadd4f9a063db66d73315d7ed25db8d90b83aaf  .ufo/waves/round-40/conform.py
5025b9664632d01063c11b4f5dadd4f9a063db66d73315d7ed25db8d90b83aaf  -
cfdb030cee30b50ddd374195b75b0e0f8a3034a27aab57d44f0e234ed08cfc0e  .ufo/waves/round-40/fixtures/generated/survivor-decoy.py
cfdb030cee30b50ddd374195b75b0e0f8a3034a27aab57d44f0e234ed08cfc0e  -
```

```sh
git cat-file -e 265a955cc67be4eae97d2dc5a9338a25f31eb29b:.ufo/waves/round-40/evidence/c10-red-decoy.txt
git cat-file -e 265a955cc67be4eae97d2dc5a9338a25f31eb29b:.ufo/waves/round-40/evidence/c10-after-decoy.txt
git cat-file -e 8d3badd:.ufo/waves/round-40/evidence/c10-red-decoy.txt; echo RED_EXIT=$?
git cat-file -e 8d3badd:.ufo/waves/round-40/evidence/c10-after-decoy.txt; echo AFTER_EXIT=$?
git log --all --oneline -- .ufo/waves/round-40/evidence/c10-red-decoy.txt .ufo/waves/round-40/evidence/c10-after-decoy.txt
```
```text
fatal: path '.ufo/waves/round-40/evidence/c10-red-decoy.txt' exists on disk, but not in '265a955cc…'
fatal: path '.ufo/waves/round-40/evidence/c10-after-decoy.txt' exists on disk, but not in '265a955cc…'
RED_EXIT=0
AFTER_EXIT=0
8d3badd round-40: evidence receipts, wave spec (66-seat v2, validated), SCORECARD/LOG/lesson
fab8eee
```

```sh
grep -n 'bypass-wait likewise' SCORECARD.md
grep -n 'bypass' /home/vgpnk/Projects/shokunin/.ufo/reports/round-39/mori.md
```
```text
2199:| C2 … bypass-wait likewise (`evidence/c8-red-wait.txt`); …
20: … both bypass fixtures (`timeout=None-valued name`,
22: … (`evidence/c8-after-none.txt`, `c8-after-wait.txt`) where the r38 checker printed `CONFORM=met`
57:- C2: before — `python3 <r38 conform> 13f3db7e --counter <bypass-none|bypass-wait>` → `CONFORM=met` exit 0
```

```sh
git log --oneline -5
git log -1 --format='%H %P %s' 8d3badd
git merge-base --is-ancestor 265a955cc67be4eae97d2dc5a9338a25f31eb29b 8d3badd && echo YES
git show 265a955cc67be4eae97d2dc5a9338a25f31eb29b:corpus/lessons/round-39-erratum.md | sha256sum
sha256sum corpus/lessons/round-39-erratum.md
git log --oneline bb1f2457bb8d3e8d5dfe98488b91e8c02e378ca3..265a955cc67be4eae97d2dc5a9338a25f31eb29b -- .ufo/waves/round-39/
git diff --stat 265a955cc67be4eae97d2dc5a9338a25f31eb29b -- .ufo/waves/round-39/
```
```text
ede486b round-40: repair S229 registry placement (E12: row inside ## Registry) + commit referenced gutted-conjunct fixture
8d3badd round-40: evidence receipts, wave spec (66-seat v2, validated), SCORECARD/LOG/lesson
265a955 round-40: instruments — conform v3 (P-C10), gate v3 (P-C11), S229, r39 erratum
bb1f245 round-39 verifier spot-check (integrator, hyaku): non-author admit/reject
44151c5 round-39: wave-1 report RevC9Ancestry …
8d3badd0647c5dbfaf5f5a1443c5d4d5109a8d21 265a955cc67be4eae97d2dc5a9338a25f31eb29b round-40: evidence receipts, wave spec (66-seat v2, validated), SCORECARD/LOG/lesson
YES
5cfea3774885697ecb4201de839c36dec7eb97292231199aefc17557709747f6  -
5cfea3774885697ecb4201de839c36dec7eb97292231199aefc17557709747f6  corpus/lessons/round-39-erratum.md
# no commits touching .ufo/waves/round-39/ in the range
# no working-tree diff vs 265a955 for .ufo/waves/round-39/
```

```sh
cd /home/vgpnk/Projects/shokunin
GIT_OPTIONAL_LOCKS=0 git log --oneline -1 -- .ufo/reports/round-39/mori.md
GIT_OPTIONAL_LOCKS=0 git merge-base --is-ancestor ce8debe HEAD && echo REPORT_ON_FLEET_HEAD_HISTORY
```
```text
ce8debe round-39: mori report erratum — C2 survivor class detail (finding 8)
REPORT_ON_FLEET_HEAD_HISTORY
```

## Bounds and out-of-scope

- Read-only seat: no production, corpus, contract, evidence, instrument or
  fleet edit; the only write is this report. No index-mutating git command and
  no jj command was run; no pacman; nothing installed or upgraded.
- I did not re-run `conform.py`, the gate, or the census; their live
  reproduction is other seats' work. The verdicts above are read against the
  committed/on-disk receipts and source blobs, not a fresh execution.
- The intermediate-fixture clause (F3) is not independently replayable from a
  committed receipt; it is verified against the committed lesson finding only.
- The `pass=11`/`pass=12` check is historical (r39 gate); the round-40 gate's
  `pass=15` is outside this erratum's claim.
