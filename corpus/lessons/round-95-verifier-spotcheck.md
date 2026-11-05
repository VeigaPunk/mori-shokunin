author: hyaku closure (non-author integrator, @m_zfl)

# Round 95 — non-author verifier spot-check (hyaku closure, mori)

Verifier: hyaku closure judge, fresh non-author session, 2026-11-05. Report `.ufo/reports/round-95/mori.md`
(fleet commit `084d99b1`, author `mori-shokunin <mori@shokunin.local>`). Lane entering `754f4991`, freeze `2dc476d7`,
landed `155069fa86a44258e9231dbb89c514e73d2b7db8` (= `origin/master` tip). No lane-authored file was edited by this check.

## 1. Conformance (PROTOCOL step 1)

- Report commit: `git log --format='%an %H' -- .ufo/reports/round-95/mori.md` → `mori-shokunin <mori@shokunin.local> 084d99b1…`. Lane identity ✓.
- `SHONEN` heading with one line per box: report carries `## SHONEN` with 4 `[~]` lines; lane `SHONEN.md` has exactly 4 boxes; no `[x]` anywhere. ✓
- Cited hashes exist and are ancestors of the branch ref: `git merge-base --is-ancestor <h> master` exit 0 for `754f4991`, `2dc476d7`, `155069fa`. ✓
- Pushed, no leftovers: `scripts/hyaku/jj-lane.sh state mori-shokunin` → `branch=master local=155069fa remote=155069fa ahead=0 behind=0`; `git status --porcelain` empty. ✓
- Driver digest matches `.ufo/watchdog.log` lines 2816/2820/2821/2827 (launch 07:45:39 attempt 1; `lane-dead-no-report` 08:10:36; launch 08:10:38 attempt 2; complete 08:58:23). Attempt-1 no-report is disclosed in the report and lesson. ✓
- Prompt `.ufo/prompts/mori-round-95.md` carries the template contract: mission/axes binding (§1), L2 floor ≥8 in one batched call (§3), commit-then-push and push scope (§5), L0 side channel (§5), report path + `SHONEN` heading + measured-commit rule (§4), report-lands-last (addendum line 516), write scope (addendum line 582). Route map in the prompt is the run-15 restore map; `MISSION.md` holds no per-lane route field, no conflict. ✓
- Landed diff `754f4991..155069fa` touches only the wave dir, `LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/lessons/round-95.md`, plus operator-authored `considerthese/2026-11-05.md` (commit `a2b054c4`, João Pedro Veiga — operator bookkeeping, not lane work). No `PROVINCE.md`/`SKILL.md`/`knowledge/` drift. ✓
- Status: `ok` — real report, real committed work, no marker. Defects below are status-neutral.

## 2. Per-claim re-checks

Re-measured by this verifier (plain measurements over committed bytes): frozen sha pins, census, SOURCES count, SCORECARD diff,
LOG/lesson/QUALITY records. Evidence-verified per PROTOCOL §Gate standard Closure consequence (lane-owned gates NOT executed here):
the C1/C2 verdict receipts, seat replays and attack reports. `count-c1.py` and `count-c2.sh` are committed verdict scripts the lane
owns, so their committed evidence is the check, never a re-run by a sibling.

- **Frozen pins** — `git show 155069fa:.ufo/waves/round-95/count-c1.py | sha256sum` →
  `6c288d70c39a5736b6aba0b4a0525159010124c0b5494f047a10aab6dfeaa450` (= report pin); `count-c2.sh` →
  `014980bc82b71b7a48764b45e7e550050e928956a32cd6e4ef3b4208aa844b9f` (= pin); pristine
  `.ufo/waves/round-94/count-c1v2.py` → `6eb7fa4cf0ecf86064bb2714a5b93b52bf3356dc6e38e5dc7ee51f7255a7b384` (= pin). Frozen bytes unchanged at landing. ✓
- **C1 (calibration)** — committed receipts: `evidence/before-c1-r95.txt:1` =
  `C1=met survivors=0 killed=7/7 before_r94_survivors=4 r94_survivor_ids=m2,m3,m4,m6 … pristine=green equiv=m5(declared) crash_ids=-`
  with per-fixture KILL lines (`m2 by=R95-LEN`, `m3 by=R95-CEN`, `m4 by=R95-TRIO`, `m6 by=R95-PAT`) and `exit=0`;
  landing re-run `evidence/landing-c1-r95.txt` identical, `exit=0`, measured at freeze `2dc476d7`. The four R95 fixtures
  each kill a round-94 survivor, so the predicate discriminates round work (before=4 survivors unmet → after=0 met).
  Replays committed: `w1/Mo95E01Replay.md`, `w1/Mo95R01Atk.md` (A1–A6 HOLDS, forged counter rejected by the sha pin), `w1/Mo95K02Crit.md`. **Predicate verified.**
- **C2 (operability, capability)** — committed receipts: `evidence/before-c2-r95.txt` =
  `HOSTINDEP hidden=1 before=C1=unmet(rc=1) after=C1=met(rc=0) control_outside=C1=met(rc=0) census_sha=3fb7261569f4 rev=754f4991198c`,
  `exit=0`; `evidence/landing-c2-r95.txt` same line at `rev=2dc476d7fdb6`, `exit=0`. The before receipt is itself the do-nothing
  evidence: P-C2r95 exits 0 at the entering revision, exactly as `w1/Mo95K01Crit.md` K5 reports. The predicate does not
  discriminate round-95 work; the claim fails the §9 do-nothing rule as an operability axis-move. The lane disclosed this
  before closure, did not amend the frozen predicate, and entered the capability row bounded to the harness demonstration
  (`landing-c2-r95.txt`, `w1/Mo95R02Atk.md` B1–B6, `w1/Mo95Lab01.md` controls). **Predicate met as frozen; axis-move not admitted — agreed.**
- **No axis harmed** — `git diff 754f4991 155069fa -- SCORECARD.md` = 27 insertions, 0 deletions (round-95 section, claim table, capability row, planned only); no other axis row touched. `w1/Mo95K02Crit.md` six-axis check: H1/H2/H3 NO-HARM, residuals named (H4). ✓

## 3. Per-axis verdicts (closure judge)

| Axis | Verdict | Reason |
|---|---|---|
| calibration | unchanged | C1 predicate met and discriminating, but the axis attribution is disputed by non-author critic K01 (battery coverage, not a counted self-assessment mismatch); the lane itself does not admit calibration and routes the ruling to the operator (L0). No score move claimed. |
| operability | unchanged | Do-nothing control reaches P-C2r95 at entering `754f4991` (committed receipt + K01 K5); the axis move verifies as pre-existing, not round work. Capability row is demonstration-only and bounded. |
| depth | unchanged | No depth work claimed; SCORECARD additions-only. |
| coverage | unchanged | K02 grades coverage "improved, with named residuals" for the battery's fixture set, but no coverage-axis score move is claimed and no PROVINCE/surface change landed; held unchanged, not harmed. |
| freshness | unchanged | No freshness work claimed. |
| adjacency | unchanged | K02 H1 NO-HARM; namespace sandbox writes confined; sibling host-literal class routed, not absorbed. |

## 4. Discernment spot-check (LEARNING.md, from outside)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S626 unshare(1) (mined, tier A) | admit | `https://man7.org/linux/man-pages/man1/unshare.1.html` fetched 2026-11-05: sha256 `1df4f95f…7375e`, 38193 bytes — byte-identical to the lesson pin | agree | The 21-word DESCRIPTION quote "Mounting and unmounting filesystems will not affect the rest of the system, except for filesystems which are explicitly marked as shared" occurs exactly once in the tag-stripped text (≤25 words ✓) and grounds `teaches` (private propagation confines the tmpfs); the `-r` mapping sentence is located in OPTIONS ("…current effective user and group IDs have been mapped to the superuser UID and GID in the newly created user namespace"). |
| S627 user_namespaces(7) (tier A) | reject | `https://man7.org/linux/man-pages/man7/user_namespaces.7.html` fetched 2026-11-05: sha256 `276480f2…301b4`, 59987 bytes — byte-identical to the lesson pin | agree | Absence claim verified: `mount operations` count 0; `propagat` count 1 and unrelated (EPERM restriction propagating down child user namespaces). The page's privilege/bind-mount sentences do not ground mount-event non-propagation; rejection reason and flip condition are sound. |
| QUALITY 205–208 | admit | `corpus/QUALITY.md:2307-2313` | agree | Each criterion cites lesson evidence and a shown-able-to-fail instance (207's `env -u` sweep prints `C1_SETUP` 0; 208's ground is the K5 rc-0-at-entering run). |
| census | — | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` re-run by this verifier | — | exit 0, final line `mori ok`; 42 pre-existing W04 duplicate-URL warnings, no E-class finding. ✓ |

## 5. Trend verdicts (closure judge; evidence above)

- **expansion: unchanged** — no admitted `knowledge/` entry landed (`git diff 754f4991 155069fa -- corpus/knowledge/` empty); two registry rows only (S626 mined, S627 rejected). CORPUS rule 4: rows are not entries. Lane verdict agreed.
- **quality: improved** — QUALITY 205–208 appended, each grounded and shown able to fail; the frozen battery's named survivor set moved 4→0 (`before-c1-r95.txt:1`); residuals m8/m10/m11 and the kill-rule doc/code mismatch named, not hidden (K02 H4, `count-c1.py:212`). Lane verdict agreed.
- **discernment: improved** (lane self-graded unchanged; closure grades improved) — LEARNING.md's improved condition is met twice: this outside spot-check agrees with the gate on both sampled decisions (admit S626, reject S627), and the K01 disagreement became a lesson (Mistakes 1) with a grounded criterion (QUALITY 208) whose able-to-fail instance is committed (K5's rc-0-at-entering run). The still-open operator ruling on C1's axis classification is a routing debt, not an unlearned disagreement.

## 6. Routed defects for round 96 (status-neutral)

1. **Unregistered gates:** `.ufo/waves/round-95/count-c1.py` and `count-c2.sh` are gates under the protocol definition but have no registry row at the lane's registry home (`SKILL.md`) and no self-test mode (`grep -c selftest` = 0 in both bytes). Register the r95 battery/harness (or fold into the planned successor battery) with verdict map + selftest.
2. **Lesson heading:** the round-95 lesson carries its gate decisions under `## Frontier step`, not a literal `## Gate` section (CORPUS layout). Content complete; heading defect only. Use `## Gate` next round.
3. **r94 routed items partially discharged:** the C2-counter mutant battery amendment (r94 spotcheck item 2, C2 half) did not land; the env fail-open `C1_SETUP` text check (item 3) is recorded as QUALITY 207 and re-routed to round 96.
4. **Digest debt:** `tools/mori-source-digest.py` reports `unpinned=3` (S125, S622, S623) — open debt named in the lesson's routed items.
5. **Operator rulings owed (L0 lines 342–344):** C1 axis classification; C2 do-nothing/capability-row; seat-death routing. Also carried: D1 planner binding; sibling host-literal class.

Operator note: all four SHONEN boxes carry `[~]` with resolvable pointers and no `[x]`; the boxes look fully checkable by a
non-author verifier (promotion review remains operator-owned).
