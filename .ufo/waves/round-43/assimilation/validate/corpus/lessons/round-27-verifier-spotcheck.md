# Round 27 — non-author verifier spot-check (mori)

author: hyaku closure (non-author integrator, @m_opus)

Runtime model as exposed to this closure session: `anthropic/claude-opus-5-5` (configured `task` route, no
model parameter passed). Closure dispatched by the hyaku orchestrator, not by the lane (re-dispatch: the first
closure seat was killed by an omp restart before writing anything; nothing of it is inherited). Measured
2026-10-22 (UTC ~17:45–18:00Z) against base `fc09f96c8036094bef06370dbb4b436edf96e6e3` and head
`df886be1cc75f1052002698bdb4a3d18a2eaf6c6`. Report: `.ufo/reports/round-27/mori.md` (fleet commit `ee9adb22`).
Three read-only reviewer seats re-checked entry facts against upstream bytes (ReCheckEntryFacts), no-harm evidence
(ReCheckNoHarm) and the prompt contract (ReCheckPromptContract); their findings are folded in below and named. No
lane tool, gate or check script that grades the lane (`tools/*`, `check-row-identity.py`) was executed (PROTOCOL
§Gate standard, Closure consequence). The lane's committed counters `count-c1.sh` / `count-c2.sh` (git object reads
only, not gates) were run for comparison with plain greps.

Driver digest (copied from `.ufo/watchdog.log` lines 712 and 723 at closure time):
`2026-10-22T12:35:27-03:00 launch mori round=27 pgid=3771336 driver=hyaku-inline attempt=1`;
`2026-10-22T14:25:31-03:00 complete mori round=27; hyaku-inline attempt=1`.

## Conformance (step 1)

| Check | Command | Observed | Result |
|---|---|---|---|
| report author | `git log --format='%an %ae %H %s' -- .ufo/reports/round-27/mori.md` (fleet) | `mori-shokunin mori@shokunin.local ee9adb22bb1d86b7c93b1d0f02aef0f8b8404f67 round-27: mori report`, committed 14:24:47-03:00, after lane tip `df886be1` (14:24:06-03:00) | pass |
| SHONEN heading | read report `## SHONEN` | 4 lines, one per box: `[ ]` decision tables, `[~]` end-to-end task, `[ ]` executable without oral context, `[~]` no cross-domain bleed | pass |
| cited hashes | `git rev-parse --verify <h>^{commit}` + `git merge-base --is-ancestor <h> master` for 761b4cdb 5fa0a00f dd4dbb20 126e192d 79ecf58b 5f00fd04 0becc421 b97b2e3f b89ac342 47f6543a 5e500d99 9c2c7de9 df886be1 fc09f96c | 14/14 resolve and are ancestors of `master` | pass |
| pushed | `scripts/hyaku/jj-lane.sh state mori-shokunin` | `branch=master local=df886be1… remote=df886be1… ahead=0 behind=0 head=detached tracked=0 untracked=1` | pass |
| leftovers | `git status --porcelain` | `?? .scratch/` only; contents dated 2026-10-21 (`SrcGitCommit-git-rev-parse.html`, `round22/`), pre-round, not round-27 work | pass |
| remote | `git ls-remote origin refs/heads/master` | `df886be1cc75f1052002698bdb4a3d18a2eaf6c6` | pass |
| prompt contract | ReCheckPromptContract: placeholder-substituted `templates/round-prompt.md` vs `.ufo/prompts/mori-round-27.md` | §1–§5 verbatim apart from placeholders; hyaku addendum §6 present (items 1–9); no L2 route map quoted (defers to host route table), role names all in `MISSION.md` buckets; prompt committed `bdfcc5a` 15:35:25Z, 2 s before launch | pass |

Not a marker: the report cites checkable commits and a committed entry. Status `ok`.

Conformance defect (status-neutral): amendment W1 in `.ufo/waves/round-27/contract.md` is headed
`2026-10-22T15:55Z`, but it shipped in `dd4dbb20`, author 12:45:38-03:00 (15:45:38Z), committer 12:50:10-03:00
(15:50:10Z) — the stated time is after the commit that ships it (PROTOCOL §Evidence standard: future-dated
evidence). Routed below.

## Claims (step 2)

### C1 — depth: OOM victim-selection entry (re-measured)

| Rev | Command | Observed |
|---|---|---|
| `fc09f96c` | `bash .ufo/waves/round-27/count-c1.sh fc09f96c` | `entry=absent new_rows_cited=0 skill_rows=0`, `C1=unmet`, exit 1 |
| `df886be1` | `bash .ufo/waves/round-27/count-c1.sh df886be1` | `entry=present new_rows_cited=7 skill_rows=11`, `C1=met`, exit 0 |
| `df886be1` | `git show df886be1:SKILL.md \| awk '/^## /{i=($0~/Round27/)} i&&/^\|/' \| wc -l` | 15 table lines in the `Round27` section: 8 decision rows and 3 error-pattern rows (the counter's 11) plus the two tables' header and separator lines |
| both | `git show <rev>:corpus/SOURCES.md \| grep -c '^\| S[0-9]'` | 126 → 144; ReCheckNoHarm `comm` on id sets: no id below S127 deleted, S127–S144 all present |

Reported values match (report: 7 / 11 at `df886be1`; committed `evidence/c1-after.txt` holds the `0becc421` run,
6 / 10). The counter checks shape only, so the substance was re-checked against upstream bytes by
ReCheckEntryFacts: `base.c:597` `points = (1000 + badness * 1000 / (long)totalpages) * 2 / 3;` (v7.2);
systemd v262 `main.c:3063` `b = saturate_add(a, 100, OOM_SCORE_ADJ_MAX);` and `user@.service.in:35`
`OOMScoreAdjust=100`; earlyoom v1.9.0 `kill.c:25,27` ±300 and `:411-421` (prefer/avoid added to RSS only under
`--sort-by-rss`, else to `oom_score`); `earlyoom.default:5` `EARLYOOM_ARGS="-r 3600"`; oh-my-pi v18.12.6
`executor.ts:2` `In-process execution for subagents.`; `kill.c` sha256 equals the cited `b32e0fad…0bf3`. Three
decision-relevant lines spot-read (+300 ≈ adj +450, ceiling 1466, `--ignore` and tie handling): no overclaim, the
inferences are marked. Verdict: **verified, depth improved.**

### C2 — operability: A2 case freeze (withdrawn before data; not verified)

| Rev | Command | Observed |
|---|---|---|
| `fc09f96c` | committed `evidence/c2-before.txt` | `a2_cases=0 a2_rules_covered=0/10`, `C2=unmet` |
| `df886be1` | `bash .ufo/waves/round-27/count-c2.sh df886be1` | `a2_cases=0 a2_rules_covered=0/10`, `C2=unmet`, exit 1 |

The claim was declared in `SCORECARD.md` and `contract.md` at `761b4cdb` with the after-value "`C2=met`, exit 0 at
the landed tip". Amendment W1 (`dd4dbb20`) withdrew it after its case-writer seat `WriteA2Cases` died at spawn; no
A2 case exists at any round commit, so the withdrawal preceded data and nothing was narrowed after landing.

**Ruling.** The admission rule (prompt §2, AXES.md) is "every claim verifies — measured, or exploratory with a
named non-author judgment — and no axis is harmed". A withdrawal is the lane's own statement; neither the protocol,
AXES.md nor the round prompt provides a path by which a declared claim leaves the admission set, and the declaration
is append-only in `SCORECARD.md`. Measured against its declared after-value, C2 is unmet at the tip. A withdrawn
claim is therefore not a verified claim, and the round does not admit. Because the withdrawal was disclosed before
any data, for an outside cause (route outage, `Error: No model selected.`), with the counter and its before-value
left untouched and no axis harmed, this is an honest stop, not a harm: verdict **rejected-honest-stop**. The
withdrawal was the correct call by the round's own independence condition; the lesson is about declaration timing
(the lane's own M4), not about honesty.

## No-harm checks

- `git diff --stat fc09f96c df886be1 -- tools/` → empty (ReCheckNoHarm): no tool changed; wave-2 CriticC1Admission
  `:163` records `PASS 32/32`, `21/21`, `12/12` (`MATCHER: rejected 48/48`), census `134` passed — evidence-verified,
  not re-executed.
- `git diff fc09f96c df886be1 -- SCORECARD.md` → 29 insertions, 0 deletions (declaration, W1, measured outcome); no
  axis score lowered.
- Retention scan: wave-2 ReviewPrivacyLanded `:23-28` reads `"metric": 4` at `5f00fd04` and at `fc09f96c` (ceiling
  4 met) — evidence-verified; no committed scan exists for `df886be1` itself (seven later commits). Routed.
- `corpus/QUALITY.md`: 19 insertions, 0 deletions (criteria 80–82 appended; no older criterion touched).
- Older knowledge files (`harness-job-capacity-r25.md`, `system-pressure-r24.md`, `userspace-oom-killers-r26.md`):
  every rewrite carries a dated old → new correction block; the settings-value withholding is annotated in line.
- S090, S093 (first published `df4db54`) and S124 (first published `327fbcc`): cell-by-cell diff against
  `df886be1` is empty (ReCheckNoHarm).
- Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → `mori ok`, exit 0, six
  W04 (S035, S037, S073–S076), same as the report's start and end.

## Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| depth | improved | C1 re-measured 0/0 → 7/11, `C1=met`; entry facts hold against upstream bytes |
| operability | unchanged | C2 unmet (withdrawn); `tools/` identical, self-test tallies unchanged |
| coverage | unchanged | no tool or case change |
| freshness | unchanged | corrections to older entries are hygiene (routed defects), not a declared claim |
| calibration | unchanged | no claim |
| adjacency | unchanged | adjacency paragraph added, no claim; no bleed found |

No axis harmed.

## Discernment spot-check (step 3)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S127 (`fs/proc/base.c` v7.2) | admit, A, mined | `curl https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c` → line 597 `points = (1000 + badness * 1000 / (long)totalpages) * 2 / 3;` (Gate table cites `:596-597`; 596 is the `if (badness != LONG_MIN)` guard) | agree | primary kernel source at a fixed tag; quote verbatim and located; the row's scope matches the bytes |
| separate row for `include/uapi/linux/oom.h` | reject (folded into S127) | `curl …/torvalds/linux/v7.2/include/uapi/linux/oom.h` → `:9 #define OOM_SCORE_ADJ_MIN (-1000)`, `:10 #define OOM_SCORE_ADJ_MAX 1000`; S127's source cell already lists the `oom.h?h=v7.2` URL and its scope names the -1000..1000 range | agree | a second row would duplicate a URL already held by S127 (and add a census W04) |
| separate row for v7.2 `cgroup-v2.rst` | reject (already S092) | `git show df886be1:corpus/SOURCES.md \| grep '^\| S092 \|'` → source `…/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst`, sha256 `a9433bb0e16a67f0` | agree | the same bytes are already a row; new anchors belong in the entry body (CORPUS.md Rules 2) |

New `SOURCES.md` row re-opened: **S129** (systemd v262 `man/systemd-system.conf.xml`). `curl
https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-system.conf.xml | sed -n 300,308p` → lines
305–306 read "…except if the service manager is run for an unprivileged user, in which case / this defaults to the
service manager's OOM adjustment value plus 100 (…)". The lesson Gate quote is verbatim, 24 words (≤25), located
`:305-306`; the row anchor `:305-307` covers it; status `mined`, used-by the r27 entry. Agree.

Sample result: 3/3 decisions agree, 1/1 quote verbatim and within the limit.

## Trend verdicts

- **expansion: improved** — new FR10 ground (victim selection by earlyoom and the kernel, origin of the fleet's
  adjustment 200 in systemd's user manager); SOURCES 126 → 144 rows, none deleted; SKILL `Round27` table.
- **quality: improved** — logged corrections of older knowledge (r26 D2, D4; r25 R7), S090, S093, S124 restored
  byte-equal to first publication; wave-2 corrections applied before landing. Carried: row defects in S127, S128,
  S129, S131 and in-place edits of S096, S097, S101 (disclosed, not hidden).
- **discernment: improved** — the new row-identity check surfaced five unlogged in-place row edits; wave-2 critics
  overturned entry statements that were fixed; this outside sample agrees 3/3 with the gate decisions.

## SHONEN (operator note, promotion is operator-owned)

Not fully checkable by a non-author this round: "decision tables" and "executable without oral context" are `[ ]`
in the lane's own assessment and no non-author execution exists; the two `[~]` boxes carry pointers only.

## Routed defects (the lane fixes these next round; this note changes no target)

1. **W1 future-dated** — amendment W1 heading says 15:55Z, shipping commit `dd4dbb20` committed 15:50:10Z. Append a
   dated correction (never rewrite the amendment).
2. **Tip receipts missing** — no committed C1 receipt and no committed retention scan at the landed tip `df886be1`
   (last: `0becc421` and `5f00fd04`). Commit tip-revision receipts as the last batch of a round.
3. **QUALITY 81 unmet at tip** — S096, S097, S101 still differ from their first-published cells (lane report,
   lesson "carried"); restore or supersede them.
4. **Carried row defects** — S127 scope/teaches F1–F5, S128 F1, S129 M2, S131 tree URL and F2–F4, the low finding in
   ReopenS140: superseding rows owed.
5. **C2 / r26 D7** — A2 cases still unpinned; a re-declaration needs a blind case writer on a healthy route and the
   counter fixes in `w1/CriticC2Counter.md`.
6. **r25 R1, R5** — still code debt (`tools/mori-job-runway.py`; routed-check self-test).

Operator items (not lane debt): seven fleet-root files (`base.c`, `oom_kill.c`, `MANPAGE.md`, `main.c`,
`meminfo.c`, `sd-main.c`, `user@.service.in`) are still present at the fleet root (writer unknown, per the report's
misroot note); wave-1 dead-at-spawn rate 7/34 (20.6%) traced to the route outage, not to the lane.
