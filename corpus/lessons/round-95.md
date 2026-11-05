# Round 95 — mori lesson

Lane round: mori round 95, attempt 2 (the L1 resumed the attempt-1 wave `w1`; the attempt-1 L1 ended without a report at
08:10:36 after the wave had settled and its outputs were complete). Entering `754f4991198c16ddd1d4a3ea9206cfb7d74d6827`.
Freeze `2dc476d7fdb68bf916685a9f217a92047662baeb` (contract, `count-c1.py`, `count-c2.sh`, before receipts). Spec, dispatch,
registry and results: `.ufo/waves/round-95/` (`w1-spec.json`, `w1-dispatch.json`, `w1/swarm-registry.json`, `w1-results.json`).
Axes: calibration (C1), operability (C2). No score moves are claimed.

## Claims and verdicts

### C1 — calibration: the round-94 admission battery's kill coverage

Frozen predicate P-C1r95 (`.ufo/waves/round-95/contract.md`, docstring of `count-c1.py`):
`python3 -I .ufo/waves/round-95/count-c1.py <rev> --lane <lane> --census <census>` prints `C1=met survivors=0 killed=7/7`
and exits 0 iff the pristine counter (sha256 `6eb7fa4c…`) is green on BASE and each of the seven mutants m1, m1b, m2, m3, m4,
m6, m7 is killed by at least one fixture.

- Before (round-94 battery only, same run): `before_r94_survivors=4 r94_survivor_ids=m2,m3,m4,m6`
  (`.ufo/waves/round-95/evidence/before-c1-r95.txt:1`). This is the do-nothing control: it does not meet the claim.
- After (battery plus R95-LEN, R95-CEN, R95-TRIO, R95-PAT): `C1=met survivors=0 killed=7/7 pristine=green crash_ids=-`, exit 0
  (`before-c1-r95.txt:1`; landing re-run `evidence/landing-c1-r95.txt`, see the report).
- Independent replays of the same frozen bytes: `Mo95E01Replay` (exit 0, identical), `Mo95R01Atk` (A1–A6, verdict HOLDS;
  revert-control per killer fixture; forged counter rejected by the sha pin, exit 2), `Mo95K02Crit` (fresh run, identical).
- Non-author disagreement, recorded and not overridden: critic `Mo95K01Crit` (`w1/Mo95K01Crit.md` K1) holds that C1 is battery
  coverage growth, not a calibration move. The round-94 lesson already recorded the four survivors as known, so no inaccurate
  self-assessment was corrected and no mismatch was counted. The L1 agrees with that reading. **Calibration verdict: not admitted.**
  The instrument is stronger on the named set; crediting it on another axis is an operator ruling (L0 line this round).
- Residuals, named and not patched into the frozen battery (amendment rule, contract §C1):
  - m8 `seven_same` gate skip (`count-c1v2.py:187-188`), m10 `verified-at` constraint drop (`:118-119`), m11 head window
    12→200 (`:65`): each survives all seven fixtures (`Mo95K02Crit`, H4).
  - m9 `tok=value[-1]` is killed only incidentally by R95-CEN/PAT/TRIO.
  - Kill-rule mismatch: `count-c1.py:212` compares full verdict tuples including returncode; the docstring says token plus
    `checks_failed`. It kills a superset; `killed=7/7` is unaffected.
- Declared equivalent m5 (`adm_ok != 19` vs `adm_ok < 1`): `Mo95R01Atk` A4 enumerates all 20 reachable pairs; no difference.
- Mutation coverage gap: both mutation-tester seats (`Mo95M01Mut`, `Mo95M02Mut`) died before producing a report, so no
  independent mutant sweep beyond the frozen seven and the K02/R01 residuals exists this round.

**C1 verdict: predicate met as frozen (measured, replayed by four seats); calibration axis not admitted (non-author critic
disagreement); no harm.**

### C2 — operability (capability acquisition): the counting surface runs with the account home absent

Frozen predicate P-C2r95 (`count-c2.sh` header, contract §C2): prints `HOSTINDEP hidden=1 before=C1=unmet(...)
after=C1=met(rc=0) control_outside=C1=met(rc=0)` and exits 0 when, inside `unshare -rm` with the home replaced by a tmpfs,
(a) the census path under the home is absent, (b) the round-93 counter is unmet or non-zero, (c) the round-94 counter with
`--census` on a copied census prints `C1=met` rc 0, and (d) the round-93 counter outside the namespace prints `C1=met` rc 0.

- Measured at the freeze: `HOSTINDEP hidden=1 before=C1=unmet(rc=1) after=C1=met(rc=0) control_outside=C1=met(rc=0)
  census_sha=3fb7261569f4 rev=2dc476d7fdb6`, exit 0 (`evidence/landing-c2-r95.txt`; before receipt `before-c2-r95.txt:1`).
- Replays: `Mo95E01Replay` (identical), `Mo95R02Atk` (independent unshare probe, mount-table leak check: none on the host),
  `Mo95Lab01` (H1: the round-93 verdict is caused by the census path's absence, not counter logic; A0 positive control
  `C1=met`, A1 absent `rc127`, A2 real copy `C1=met`, A3 failing stub `C1=unmet rc1`, A4 passing stub `C1=met`).
- Negative controls and their results:
  - `Mo95R02Atk` B5: a stub before-counter printing `C1=met` makes C2 exit 1 (rejected, as required).
  - `Mo95R02Atk` B4: a do-nothing stub after-counter passes C2 (C2 certifies the artifact's host-independence, not its
    judgment; C1 covers judgment).
  - `Mo95E02Relo` control A: a literal host fallback in `census_path` (not on the invoked path) **survives** (exit 0, expected 1).
    The frozen C2 harness exercises only `--census`. The literal fallback is exercised only by a supplemental mutant that forces
    the literal on the explicit argument (exit 1). Residual: C2 cannot see a dormant literal.
  - `Mo95E02Relo` control B: an absent fleet census gives `C2_SETUP`, exit 2.
- **The do-nothing control fails (L1 finding, frozen by this round's contract).** The contract says the entering state is a
  do-nothing control that fails clause (b). It does not. Clause (b) is met by the round-93 counter's unmet verdict, which already
  exists at entering; clause (c) is met by the round-94 counter, which also already exists at entering. The critic `Mo95K01Crit`
  (K5) ran P-C2r95 at `754f4991` (entering) and got `rc=0`; the L1 re-ran it at the freeze and got `rc=0`. So the frozen predicate
  is reachable without any round-95 work, and it does not discriminate this round's contribution. The claim fails the §9
  do-nothing rule. This is recorded as a defect of the frozen predicate; the predicate is not amended after data.
- **Operability verdict: not admitted; operability unchanged (7).** The axis move is not credited.
- **Capability acquired (AXES.md *Capabilities*):** the harness runs and its output verifies (the measurements above, with the
  controls as its positive and negative arms). Capability row entered, bounded to the harness: `host-independent counting
  namespace` — the harness demonstrates the home-hidden comparison of the two named counters. It does not claim that the
  counters became host-free in round 95; the round-94 successor carried that property at entering.

**C2 verdict: predicate met as frozen; do-nothing control reaches it (claim not admitted as an operability move); capability
row entered with its limits; no harm.**

## Frontier step (corpus/SOURCES.md, contract v1)

- Census before→after: `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 397 at entering
  `754f4991` (`git show 754f4991:corpus/SOURCES.md`), 399 now. `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`
  → exit 0 at round start (`evidence/census-before-r95.txt`) and exit 0 at round end (see the report).
- Rows added this round: S626 (tier A, mined), S627 (tier A, rejected). Rows touched old→new: none.
- **S626 — unshare(1)**, `https://man7.org/linux/man-pages/man1/unshare.1.html`, opened 2026-11-05 by scout `Mo95S01Src`, re-opened
  by the L1 the same day: page sha256 `1df4f95f877112743581e8b0900ce1296dbc6155619f7b88232e076f27b7375e`, 38193 bytes.
  Located quote (≤25 words, count 1 in the tag-stripped text, L1 re-count): "Mounting and unmounting filesystems will not affect the
  rest of the system, except for filesystems which are explicitly marked as shared" (DESCRIPTION, mount namespace bullet).
  Also located: `-r` maps the effective user and group IDs to the superuser UID and GID in the newly created user namespace
  (OPTIONS; count 1). Anchors: OPTIONS and DESCRIPTION sections; util-linux 2.43.devel, page rendered 2026-09-09.
  **Admitted (mined) for:** the propagation non-escape of the mount-namespace tmpfs and the user-namespace mapping used by C2.
  Cited by this lesson.
- **S627 — user_namespaces(7)**, `https://man7.org/linux/man-pages/man7/user_namespaces.7.html`, opened 2026-11-05, re-opened
  by the L1: sha256 `276480f2185f65ee9ca1402c233a53780dd558a77bcc30127bbb5bfafb1301b4`, 59987 bytes. Located quotes (count 1):
  "Holding CAP_SYS_ADMIN within the user namespace that owns a process's mount namespace allows that process to create bind mounts";
  "tmpfs(5) (since Linux 3.9)"; "the process has full privileges for operations inside the user namespace, but is unprivileged
  for operations outside the namespace". **Rejected as a source for mount-event non-propagation:** the page has no mount-propagation
  sentence (L1 search for `mount operations` returns 0; `propagat` returns 1 and that is unrelated). Flip: a located
  propagation statement in `user_namespaces(7)`. The privilege statements are located but no admitted entry cites S627 (CORPUS rule 4).
- Sourced claim: C2's mechanism (user and mount namespace, tmpfs over a directory) is evidenced by S626; the claim sits in the
  C2 section above and the registry row's `used-by` names this lesson.
- Search log (CORPUS rule 5): the scout's duplicate sweep (`grep -nE 'man7.org/linux/man-pages/man1/unshare|man7.org/linux/man-pages/man7/user_namespaces|man7.org/linux/man-pages/man7/mount_namespaces' corpus/SOURCES.md`) was empty before the fetch; highest id was S625. Fetch: `curl -fsSL` twice per page, byte-identical. Negative claim "no propagation sentence in S627" carries that search.
- Assimilation: none. No `merge/mori/` theme was taken this round; the frozen predicates were the round's scope.
- considerthese: the latest file `considerthese/2026-10-26.md` has an unimplemented "Suggestions for improving myself (proposals only, not acted on)" section. Not taken this round: the L1 had no spare seat to ground it, and the protocol allows one per round; it waits for round 96.

## Mistakes (CORPUS: class · evidence · captured-by · fix)

| # | Class | Evidence | Captured-by | Fix |
|---|---|---|---|---|
| 1 | do-nothing control mis-specified (a predicate the entering repository already meets) | contract §C2 "Do-nothing control" vs `Mo95K01Crit.md` K5 (entering `754f4991` rc 0) and this lesson's C2 section | none before freeze; the §9 rule was not run as a committed control | QUALITY 208: a control at the entering revision is scored before freeze; a predicate it already meets is not a claim. Shown able to fail by the K5 run. |
| 2 | successor-as-before recurrence (round 94 K01) | `corpus/lessons/round-94.md` Mistakes 4; this round measured the pre-existing round-93 counter under home hiding, positive control outside | QUALITY 206 (round-94 criterion) | Taken for the before measurement; the do-nothing gap in #1 is a separate defect. |
| 3 | dormant literal survives the harness | `Mo95E02Relo.md` control A (exit 0 vs expected 1) | none: no criterion covers an unexercised code path in an invoked-argument harness | Routed to round 96: a second arm forcing the fallback path, in a successor harness. Frozen C2 bytes are unchanged. |
| 4 | residual mutant survivors in the frozen battery (m8, m10, m11, m9 incidental, kill-rule doc/code mismatch) | `Mo95K02Crit.md` H4; `count-c1.py:212` vs docstring | QUALITY 205 (names the set, reports survivors) | Routed to round 96 as a frozen-battery amendment (new revision, never an edit). |
| 5 | seat deaths: two mutation-testers and the scribe ended without a complete report (provider limit / zai 429) | results file `w1-results.json`; `Mo95M01Mut`, `Mo95M02Mut`, `Mo95Sc01Lesson` | none — the registry marks spawned, not settled-with-report | L1 disclosed the gap, did not replace seats (protocol: never replace a dead seat), and re-verified the scribe's and mutation-testers' cited measurements independently. |

Additional classes checked: fleet-root misroot sweep (`git -C /home/vgpnk/Projects/shokunin status --porcelain` before the report:
only the orchestrator-owned `.scratch/run15-state.json` is modified, not authored by this lane; no misroot to move).

## Routed items (status-neutral)

- D1 planner binding — operator-owned (L0, round 93/94; still open).
- Sibling host-literal class — the connector `Mo95Conn01` mapped 21 lane directories with `/home/vgpnk` hits (lexical,
  9,381 files; 8,917 outside mori). Routed to owners via L0 (already routed in round 94; not repeated).
- env fail-open (`C1_SETUP` text check) — round 96.
- Digest debt — `tools/mori-source-digest.py` on the historical pinned set reports `unpinned=3` (S125, S622, S623); S622 and
  S623 are open debt, not closed here.
- Host: `user.max_user_namespaces` = 122865 read-only here; the labrat and the reviewer both read it. Seats must not change
  host sysctls. Namespace availability remains host configuration.

## Draft criteria (QUALITY.md)

205–208 appended this round, each grounded in the lesson's table above (see QUALITY.md).
