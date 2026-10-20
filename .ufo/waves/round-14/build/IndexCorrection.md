# IndexCorrection — corpus/README.md historical index correction

Seat: `MoriR14.IndexCorrection` (executor, leaf; no delegation, no background jobs).
Owned file: `corpus/README.md` only. No other file was edited.

## Basis read before editing

- `corpus/lessons/round-13-verifier-spotcheck.md:137` (routed defect 6): "README:32–33
  still abbreviates historical text-selected 5/7/9 samples as MESSAGE-free
  'kernel kills' … Do not rewrite historical append-only lessons."
- Same spotcheck `:7` (closure `rejected-harmed`) and `:84`–`:86` (OOM alarm demoted to
  INFO; cgroup-local counter is not a replacement; fleet/non-fleet split and tsukuroi
  owner routing lost).
- `corpus/knowledge/kill-classes-by-message-id-r12.md:38` — "matching MESSAGE is not
  structured counting": `journalctl --grep` selects on `MESSAGE=`; `--output-fields`
  suppresses output, not matching. The 5 kernel records are text-selected.
- `corpus/knowledge/kernel-oom-line-attribution-r12.md:37-42` — same distinction for the
  five retained `oom-kill:constraint=` samples; no admitted live kernel-token parser.
- `LOG.md:770-787` (round-14 entry): one C1 claim; historical index corrections are an
  unclaimed conformance/learning repair; gates are L1-owned.
- `.ufo/waves/round-14/spec.json` IndexCorrection item and KnowledgeRepair item (fixed
  path `corpus/knowledge/journal-alarm-routing-r14.md`).

## Changes — exact touched lines

Working-tree diff over `corpus/README.md`: `28 insertions(+), 3 deletions(-)`.

1. **Line 32** — `knowledge/kill-classes-by-message-id-r12.md` row. Removed the
   "MESSAGE-free" claim over the 5/7/9 samples and the "5 kernel kills" phrasing.
   New holds cell states: catalog `MESSAGE_ID` counts with non-`MESSAGE` output fields;
   "the historical 5/7/9 one-boot samples are **not MESSAGE-free kernel kills**: 5 are
   `--grep`-selected kernel `Killed process` text matches and 7 user + 9 system are
   catalog-ID notice records; scopes never summed". Sources cell changed from
   "MESSAGE-free journal counts 2026-10-19" to "catalog-ID counts + MESSAGE-selected
   historical samples 2026-10-19".
2. **Line 33** — `knowledge/kernel-oom-line-attribution-r12.md` row. The five samples are
   now labeled "5 retained samples, 2026-10-18, MESSAGE-selected by `--grep` — historical
   text matches, not a structured MESSAGE-free victim count"; "token-only, never MESSAGE"
   became "token-only output, never a `MESSAGE` echo" (output intent, not selection);
   fleet attribution `[UNKNOWN]` without a validated `task_memcg` token is unchanged.
3. **Line 39 (new coverage-map row)** — links the round-14 note being created by
   `MoriR14.KnowledgeRepair` at `knowledge/journal-alarm-routing-r14.md`. Holds are the
   exact set confirmed by that seat's coordination message (not dispatch inference):
   one global `OOM_KILL_JOURNAL` crit per census (notice alarm ≠ unique victim) with
   separate no-sum `user_notice`/`system_notice`/`user_unit_oom`/`system_unit_oom`
   counters; user `KILL_SIGNAL_JOURNAL` warn from process SIGKILL9 or `UNIT_RESULT=signal`;
   fleet/non-fleet by `UNIT=`/`USER_UNIT=` subject presence under
   `classification_rule=unit-name-token` (heuristic, not membership proof); unattributed
   → `UNIT_FAILURE_UNATTRIBUTED_JOURNAL` info owner=unresolved; cgroup-local not a
   substitution; signal/GPF unimplemented-versus-unrecorded; unavailable ≠ alarm;
   candidate contract, no delivery/schema claim before L1 measurement. Sources:
   `S002, S013, S015, S035, S036, S037, S038` (round 14) plus spotcheck routed defects
   1–3.
4. **Lines 280–304** — replaced the single-line `**Journal scope correction (round 13):**`
   bullet with `**Journal scope correction (round 13, qualified in round 14):**`:
   - restates that the r12 historical samples indexed above are not MESSAGE-free kernel
     kills (five `--grep` MESSAGE-selected kernel text matches; 7/9 are catalog-ID notices)
     and are not a current measurement or unique-victim count;
   - **admits the r13 harm explicitly**: "The r13 cutover is rejected-harmed, not
     admitted:" it demoted the OOM notice classes to INFO away from critical
     `OOM_KILL_JOURNAL`/DRIFT and collapsed the fleet/non-fleet `UNIT_FAILURE_*` split with
     its tsukuroi owner routing, citing `lessons/round-13-verifier-spotcheck.md` routed
     defects 1–2 and 6;
   - links `knowledge/journal-alarm-routing-r14.md` and states the round's declared C1
     behavior per the confirmed holds: one global critical `OOM_KILL_JOURNAL`/DRIFT alarm
     per census with separate never-summed notice/unit counters and no unique-victim
     claim; fleet `UNIT_FAILURE_JOURNAL` vs non-fleet `UNIT_FAILURE_OUT_OF_SCOPE` (owner
     tsukuroi) split on `UNIT=`/`USER_UNIT=` presence under the named heuristic rule;
     unattributed records stay `UNIT_FAILURE_UNATTRIBUTED_JOURNAL` info (owner unresolved),
     never invented non-fleet membership. Wording is "Round 14's C1 claim … restores",
     i.e. declared candidate contract, not an observed result.

No historical lesson or knowledge file was rewritten. All other coverage-map rows
(31, 34–38) and every Frontier row are byte-unchanged; only the previously blank
line 39 is now the inserted r14 row.

## Deliberate non-change

`corpus/README.md:37` keeps "independently scoped MESSAGE-free catalog-ID record counts".
That phrase is accurate for the r13 structured probe (filter on `MESSAGE_ID=`, non-`MESSAGE`
output fields) and is not the text-selection claim the spotcheck rejects; changing it would
misstate the structured query. `QUALITY.md:32` (spotcheck defect 6, second half) is outside
this seat's ownership and is not edited here.

## Evidence retained

- Diff: `git diff --unified=0 -- corpus/README.md` shows exactly the hunks at `@@ -32,2
  +32,2 @@`, `@@ -38,0 +39 @@`, `@@ -279 +280,25 @@`; `git diff --stat` reports
  `1 file changed, 28 insertions(+), 3 deletions(-)`.
- Post-edit inspection: `grep -n 'MESSAGE-free\|MESSAGE-selected\|kernel kills'
  corpus/README.md` returns only line 32 ("**not** MESSAGE-free kernel kills"), line 33
  ("not a structured MESSAGE-free victim count"), line 37 (accurate catalog-ID phrase), and
  line 284 (the bullet's restatement). No remaining "5 kernel kills" or MESSAGE-free index
  claim.
- `corpus/knowledge/journal-alarm-routing-r14.md` did not exist at handoff time; the link
  is forward to the in-flight KnowledgeRepair file. Its indexed holds and source set were
  confirmed verbatim in a coordination message from `MoriR14.KnowledgeRepair` after the
  first row draft; the row and bullet tail were rewritten to those holds.

## Verification status

No build, test, lint, format, selftest, gate, census, drift or oracle run was executed by
this seat — per contract, L1 owns the single post-integration gate. The only commands used
were reads (`read`/`grep`) and the diff/stat inspection above; no pass claim is made.

Tool installs/upgrades: none.

## Risks / blockers

- The r14 coverage-map row and bullet link a file whose bytes are still absent at this
  instant (KnowledgeRepair running). Its holds and source set are confirmed by that seat,
  so only existence/last-edit reconciliation is outstanding; if the delivered note changes
  path or scope, L1 must reconcile line 39 and the bullet tail.
- The bullet's restored-behavior sentence is the wave's declared C1 claim; it must not be
  read as measured behavior until L1's gate runs.
- `QUALITY.md:32` historical qualifier (routed defect 6) remains open if QualityCriteria did
  not cover it; outside this seat's writable set.
- The two r12 notes still contain "L1's MESSAGE-free extraction" at their historical `:17`
  (qualified later at `:38` / `:37`). They are not owned here and the assignment forbids
  rewriting historical material, so the index cells carry the correction instead.
