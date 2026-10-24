author: hyaku closure (non-author integrator, @m_strong)

# Mori round 15 — non-author verification and closure

Date: 2026-10-20. Reviewer: `CloseMoriR15`, dispatched by the orchestrator, not by mori.
Read-only assistance: `CloseMoriR15.MoriEvidenceReview` (reviewer) and
`CloseMoriR15.MoriProcedureReview` (critic); neither wrote files or ran lane gates.

## Decision

**status: ok · admitted: true · verdict: admitted.** C1 coverage verifies at
its declared finite-fixture scope; no axis harm is established. Execution is
**not fully conformant**: the disclosed broadcast, outside-lane writes and
mid-flight checks remain violations, with additional correction-sweep and
wave-context defects routed below. Admission is not a retroactive waiver.
PROTOCOL Round-robin preserves real-report status despite these defects;
claim admission separately requires every claim verified and no axis harmed.
Those conditions hold on the settled committed evidence, not on the tainted
seat checks. Corpus admission/source structure is conformant at this bounded
scope; active registry prose has the specific defect recorded below.

Compared revisions:
- Entering: `0fa5e0de194bcc270a927a166664113e6821442b`.
- Delivered: `61cce328935924d9c9e03bab2f6267ed259e1512`.
- Final gate measurements: `1822145d95682709069bbc8f4e1b947ddbe20078`;
  delivered verdict-driving bytes match that revision.
- Fleet report: `.ufo/reports/round-15/mori.md`, committed by mori as
  `1ccac09e954e5dc523f692022f49f36b8d0eefd6`.

## Step-1 conformance and dispatch digest

Commands run by this reviewer (absolute repo roots were used):

```sh
git -C /home/vgpnk/Projects/shokunin log --format='%an %H %aI' -- .ufo/reports/round-15/mori.md
git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --porcelain
git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-list --count '@{u}..HEAD'
git -C /home/vgpnk/Projects/shokunin/mori-shokunin merge-base --is-ancestor <cited-hash> HEAD
git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff 0fa5e0de194bcc270a927a166664113e6821442b 61cce328935924d9c9e03bab2f6267ed259e1512 -- SCORECARD.md
```

Observed: report author `mori-shokunin`, hash `1ccac09e954e5dc523f692022f49f36b8d0eefd6`,
author time `2026-10-20T05:35:15-03:00`; empty lane porcelain; ahead count `0`.
All three carrying hashes (`26f6589dfa2a07e41a6dcfda99c2998bce2c0932`,
`1822145d95682709069bbc8f4e1b947ddbe20078`, delivered HEAD) exist and each
ancestry command exited 0. Their authors are `mori-shokunin <mori@shokunin.local>`;
times are 05:20:01, 05:27:57 and 05:32:21−03 respectively, preceding the report.
The report has all required sections, real committed work, and four `[~]`
assessment lines beneath `## SHONEN`; it is not a completion marker.
`SHONEN.md` retains the canonical four unchecked boxes.

A plain Python string comparison rendered `templates/round-prompt.md` with
LANE=mori, ROUND=15, the dispatched axes/root and repo substitution:
`prompt.startswith(rendered_template.rstrip())` returned `True`.
The full canonical contract precedes the campaign addendum. The dispatched
addendum explicitly makes wave 2 **optional**; a later instruction requiring
wave 2 is not retroactively substituted. Committed `dispatch.json` recount:
spawn64/resume0/total64; executor24/scout8/connector6/reviewer8/scribe6/
critic8/sentinel2/revenger2, zero task model fields, registry members64.
The report records L1 holding the canonical planner seat. No runtime model
routing is inferred from aliases printed in the historical prompt.

Copied mutable driver evidence, corroborated by reopening `.ufo/watchdog.log`:

```text
2026-10-20T04:25:40-03:00 launch mori round=15 pgid=2391770 driver=hyaku-inline attempt=1
2026-10-20T05:35:38-03:00 complete mori round=15; hyaku-inline attempt=1
```

## C1 re-check: measurement versus gate-evidence verification

I did **not** execute `mori-census.sh`, any mori regression gate or any
selftest. PROTOCOL Gate standard requires verifying their committed
self-test/frozen-run/revision evidence, not executing a sibling's gate.
I independently re-counted committed case records and retained raw alarm
lines; these are static measurements, not a claim to have rerun production.

The following Python core was executed in Eval using subprocess `git show`
against the delivered commit, so counts do not depend on uncommitted files:

```python
import subprocess, json, hashlib, re
lane = '/home/vgpnk/Projects/shokunin/mori-shokunin'
after = '61cce328935924d9c9e03bab2f6267ed259e1512'
def committed(path, rev=after):
    return subprocess.check_output(['git', '-C', lane, 'show', f'{rev}:{path}'])
for name in ['red-before-final', 'green-after-final', 'capture-boundary']:
    m = json.loads(committed(f'.ufo/waves/round-15/evidence/{name}/run-manifest.json'))
    print(name, len(m['cases']),
          sum(c['sut_behavior']['status'] == 'fail' for c in m['cases']),
          sum(c['sut']['status'] == 'fail' for c in m['cases']),
          sum(c['sut']['status'] == 'pass' for c in m['cases']),
          sum(c['frozen']['control'] == 'red_confirmed' for c in m['cases']),
          m['revision']['start']['head'], m['revision']['stable'], m['inputs']['unchanged'])
```

Observed columns: bundle · cases · behavioral-fail · schema-fail · SUT-pass ·
confirmed-frozen-red · actual starting HEAD · revision-stable · inputs-unchanged:

```text
red-before-final 63 34 63 0 34 1822145d95682709069bbc8f4e1b947ddbe20078 True True
green-after-final 63 0 0 63 34 1822145d95682709069bbc8f4e1b947ddbe20078 True True
capture-boundary 7 0 0 7 1 1822145d95682709069bbc8f4e1b947ddbe20078 True True
```

Both final core manifests have zero inconclusive/unexpected frozen controls.
The 34 red controls completed with CLEAN/rc0 and specifically missed a
wanted alarm; arbitrary error, timeout or integrity rejection is not the red
witness. The other 29 controls pass. Their two outer command receipts record
exit1 before and exit0 after. Full-schema63→0 includes added metadata and is
not 63 historical production defects; the behavioral metric is **34→0**.

Independent retained-stdout spot counts (`re.findall` on anchored
`^FINDING OOM_KILL_JOURNAL ` / `^FINDING KILL_SIGNAL_JOURNAL `):

| Committed case | Before rc / OOM / signal | After rc / OOM / signal | After raw semantics |
|---|---|---|---|
| `bootarray-user-kernel-oom-boot-array-current` | 0 / 0 / 0 | 1 / 1 / 0 | `user_notice=unavailable:record-invalid`; positive witness remains1 |
| `bootarray-user-unit-signal-boot-null` | 0 / 0 / 0 | 1 / 0 / 1 | unavailable raw arm retained, not replaced by a subset total |

For each manifest run and each stdout/stderr path I compared
`sha256(committed(path))` to the recorded digest: **252/252**, **252/252**
and **28/28** retained streams match respectively; zero digest mismatches.
All16 core fixture-pack hashes match the expected table, containing63 cases.
Both core bundles record126 runs (63 SUT +63 frozen); every recorded run
has12 journal argv entries. This is finite query-bound evidence, not a
latency distribution or proof of no performance regression.

Plain `hashlib.sha256(git_show_bytes)` observations:

| Input | SHA-256 |
|---|---|
| delivered `tools/mori-census.sh` | `f1f8d1b62bb617bbcc4664057ab807d3fed8c275b7aabbdf7b373323c5501ff7` |
| `tools/mori-round15-regressions.py` | `6a55c33cc13e2cd862ebd44db66e8af635a35d7cd2a85168360569c886d62ffe` |
| `.ufo/waves/round-15/expected.json` | `9024256dd6b7132180288413d745ba233c4cb8d4b280c841d0087b53641926f3` |
| frozen entering census | `0e41cb83fce2e8c5c711171e1cde2e6fa2809dcfce630eccabe52bcbe41516d9` |

All four are byte-identical at measured1822145 and delivered61cce32.
The frozen census equals `git show 0fa5e0d:tools/mori-census.sh` exactly.
Expected-table digest matches both manifests' loaded input digest. Actual
start/end HEAD is1822145, not the retained env annotation0fa5e0d; the latter
is explicitly annotation-only. Exact dirty paths are retained under the
round's evidence subtree; stable inputs are not called a clean whole tree.

Seven boundary cases re-count to7 pass/0 fail with1/1 frozen red. Raw stdout
counts show no OOM or signal finding for failed producer rc124/137/5, stderr
or malformed JSON; the mixed control and unaffected other-scope case each
retain one OOM finding. `boundary-pin-red.json` is setup-error evidence, not
production behavioral red or a single-delta causal proof of the oracle fix.

Committed preservation receipts verified, not rerun:
- `census-selftest.json`: exit0, `MORI_CENSUS_SELFTEST: PASS (113 cases, 113 passed, 0 failed)`.
- `r13-selftest.json`: exit0, checks33/cases2; `r14-selftest.json`: exit0,
  checks20 including real-gate red rc1/tamper rc2.
- `r15-selftest-final.json`: exit0, classifier PASS and full selftest PASS;
  scope starts/ends at1822145 with empty porcelain, inputs_changed=false.
- `r13-preserved.json`: exit0, 24pass +2mutation-red; `r14-preserved.json`:
  exit0, 44pass, with the disclosed intentional mixed-control migration.
- `silence-oracle.json`: exit0, matched28/total28.
- `live-census.json`: exit1, findings20/drift11/unavailable1/surfaces8.
- `drift-current.json`: exit1; old r10 pin remains red and is not re-pinned.
- `control-bypass-refused.json`: removed flags rejected as unrecognized, exit2.

Census/r13/r14/silence verdict-driving files compare byte-equal between the
preservation receipts'26f6589 and delivered HEAD. The final r15 selftest is
bound by its clean1822145 scope; its stdout is not a numeric selftest tally.
No live positive load, universal event coverage, authenticated emitter,
unique-victim count or performance improvement is admitted.

## Per-axis verdicts

`SCORECARD.md` diff is83 insertions/0 deletions, adding the declared result
and capability without raising scores or rewriting prior observations.

| Axis | Verdict | Reason |
|---|---|---|
| coverage | improved | C1 finite mixed-invalid alarm failures34→0, raw-total unavailability preserved; owned score6 held |
| operability | unchanged | settled selftests, frozen controls, boundaries and prior routing/silence receipts hold; stale registry wording routed, not a gate bypass |
| depth | unchanged | primary-source typed predicates are grounded; no separate depth claim |
| freshness | unchanged | live observation retained; old red pin is pre-existing disclosed debt, not newly blessed |
| calibration | unchanged | fixture/live and subset/total boundaries explicit; procedural and wording debt remain, no universal or score-increase claim |
| adjacency | unchanged | aggregate-only subject routing and tsukuroi INFO route retained; no OS remediation, dispatch or ownership expansion |

## Outside discernment spot-check

Sources were reopened on2026-10-20. The original `## Gate` candidate is
explicitly superseded by `## Measured Gate decision` in the same lesson.

| Item | Lane decision | Re-opened source | Outside judgment | Reason |
|---|---|---|---|---|
| Individually qualified positives beside unavailable aggregates | admit, bounded and pending outside closure | committed final before/after manifests and retained stdout; `knowledge/journal-positive-evidence-r15.md`; [systemd journal fields, User/Trusted Journal Fields](https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html) | agree | Same-capture witness presence is distinct from complete counts; raw unavailable and trust limits survive; static recount confirms34→0 |
| Salvage malformed JSON or MESSAGE text for an alarm | reject | `boundary-fixtures/capture.json:7`, committed `boundary_malformed_json` run and expected result; same primary docs, MESSAGE= | agree | A syntactically broken stream supplies no successfully parsed structured witness; captured boundary has no OOM/signal finding; MESSAGE is not metadata |
| Authenticate or infer no event from invalid/absent positive evidence | reject | same primary docs, User Journal Fields and `_BOOT_ID=`; knowledge note:156–182 | agree | Client-supplied fields are not authenticated; no matching retained record does not establish event absence |
| Re-pin merely to silence drift | reject | committed `drift-current.json`, exit1 | agree | A schema/volatile-field change does not itself justify a semantically reviewed new baseline |

There are **no newly added source rows** (38→38), so I sampled a newly
extended row instead of inventing a nonexistent new-row obligation.
**S038** now cites the r15 knowledge note. Reopened immutable source:
[service.c at cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af, service_result_table:6588–6602](https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/core/service.c).
The lesson's whitespace-normalized quote
`[SERVICE_FAILURE_OOM_KILL] = "oom-kill",` is3 whitespace-separated words,
within25, and matches the source; nearby `SERVICE_FAILURE_SIGNAL` maps to
`"signal"`. Agree with scoped tierA: spelling vocabulary only, not emitter
authentication or victim identity. S037's reopened subject-unit quote also
matches: “Used by the system and user managers when logging about specific units.”

Source census executed by this reviewer:

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
```

Observed exit0:

```text
mori W04 S035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in across scopes
mori W04 S037 duplicate url www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html across scopes
mori ok /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
```

Independent Python census read committed before/after bytes using
`re.match(r'^\|\s*S\d{3,}\s*\|', line)`, split11 cells, and
`collections.Counter(row[3])` / `Counter(row[7])`:
38→38, A35/B2/C1 held, mined17/queued20/rejected1 held. Comparing row cells
found only S014/S015/S037/S038 cell10 (`used-by`) changed; each old cell is
preserved as the new cell's prefix plus the new path. No immutable-cell
change, status/recheck change or newly added ID was found. The lesson logs
all four transitions.

## Learning trends

- **expansion: improved.** `git diff --name-only --diff-filter=A` over
  `corpus/knowledge` finds exactly `journal-positive-evidence-r15.md`.
  Its source trio cites minedS014/S015/S037/S038; README FR1 and PROVINCE
  identify the newly held mixed-class failure-mode ground, not full FR1.
- **quality: improved.** The r14 mixed-class suppression limitation is
  explicitly superseded with qualified positive-witness semantics and
  committed red/green evidence, while capture failure remains refused.
  No sampled admitted fact failed re-check; the stale gate-registry sentence
  below remains a documentation defect, not evidence of a working bypass.
- **discernment: improved.** This independent sample agrees on both admit
  and rejects. Prior outside findings are also learned in lessonM1–M3 and
  appended QUALITY33–36 (diff18 insertions/0 deletions), rather than calling
  the author's64 seats an outside review. Procedural-disclosure precision
  still requires the appended correction below.

## Procedural adjudication and routed defects

**M4–M6 are real violations, status-neutral, and not silently repaired by
passing tests.** The claim is admitted only because later independent L1
measurements over settled committed inputs replace the prohibited checks;
canonical URLs replace temporary downloads as source authority. A broadcast
is coordination noise with no evidenced C1 output corruption; no secret or
production record payload was established. Exact-id corrections are reported
by L1, not a proven retroactive restoration of the original wave contract.

Open queue for mori's next steered round (do not rewrite this filed report,
prior lessons, or historical seat observations):

1. **Wave-context omission / broadcast prevention.** This reviewer counted
   zero `agent://` tokens in both committed spec and dispatch JSON. Thus the
   dispatched L1's explicit no-broadcast/exact-id restriction was not passed
   into the initial seats' context. Append a correction to M4 assigning L1
   responsibility for the omission, and carry the exact-id/no-broadcast
   restriction in future wave contexts. Do not describe an admonition as a
   tested preventative repair. The violation remains recorded.
2. **Outside-lane writes include more than source downloads.** Besides
   RegistryFrontier:63–72, `build/HarnessBuild.md:248–267` explicitly records
   a `--pin-fixtures /tmp/mori-r15-expected-probe-final.json` write. Append
   that omitted instance to the procedural-debt disposition and keep future
   deliberate probe outputs within authorized scope. Temporary isolated
   selftest trees allowed by Gate standard do not authorize running the
   selftests mid-flight or arbitrary outside-lane probe artifacts.
3. **Mid-flight verification was not authorized.** The actual committed
   HarnessBuild task says “No execution” and “do not run verification”; its
   context says skip all builds/tests. The historical report:301–307 wrongly
   justifies earlier checks as explicitly required. Append a correction
   distinguishing implementation of subprocess selftest arms from permission
   to execute them; preserve the historical report. The final clean1822145
   selftest and final paired receipts, not early seat results, remain the
   admissible verification.
4. **Correction sweep missed active registry prose.** `SKILL.md:134` still
   claims `--no-frozen-control` needs hidden `--selftest-child`; delivered
   code and `control-bypass-refused.json` instead remove/refuse both flags.
   Correct the active registry in the next lane-authored commit and append
   the lesson-backed disposition. `build/SkillInterface.md:88` is historical
   draft advice, not a live interface contract; do not rewrite that history.
   This is PROTOCOL Evidence standard correction-sweep debt, not an actual
   bypass or a failed C1 witness.
5. **Carry the old drift-pin debt.** Preserve the redr10 observation until a
   separately reasoned semantic review justifies any re-pin; a green C1
   fixture gate is not a full freshness pass. Keep all victim/authentication,
   access/retention, F01/F02 causal-scope and fixture/live qualifications.

Promotion remains operator-owned. There is substantial evidence for the
four SHONEN topics, but this closure does not certify all four as fully
checkable: the active registry contradiction must be resolved before a
blanket executable-instructions assertion. No boxes or rank were changed.
No new L0 question is needed to close this bounded claim; orchestrator should
carry this defect queue into mori's next round. No tools were installed or
updated by this closure or its two reviewers; no pacman transaction, host
service change, credential read or separate omp process was performed.
