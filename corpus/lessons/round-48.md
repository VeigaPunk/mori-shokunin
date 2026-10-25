# Round 48 lesson

Entering tip `e5dbac05459887d9597ea5d1da0d8e3d024e0d17`; freeze `4387cf94b69ddce455051a1ff38e93795c2e6cde`
(contract `.ufo/waves/round-48/contract.md`, both counters, controls, the four quota source copies). Claims:
C1 calibration (the pin reconciler cannot be turned green by the junk the round-47 closure found, scored by
`count-c1.py` with eight junk and four honest edits), C2 depth (FR2 filesystem-quota entry, every claim a
located quote, scored by `count-c2.py`). Wave-1 seat reports: `.ufo/waves/round-48/w1/`.

## Gate

### New SOURCES rows (each opened this round; rule 1)

All six rows were opened by me and by the row scribes on 2026-10-25. The four doc/code pages were fetched with a
browser User-Agent; `xfs_quota.8`, `quotactl.2` and `errno.h` are byte-identical to the committed copies
(`cmp`, 2026-10-25); the Aliyun page is not (embedded JSON differs between fetches) and its quotes are stable.

| id | URL / locator | accessed | ≤25-word located quote | decision |
|---|---|---|---|---|
| S479 | https://man7.org/linux/man-pages/man8/xfs_quota.8.html (copy sha256 `6375e40e…`) | 2026-10-25 | "XFS distinguishes between quota accounting and limit enforcement." — §QUOTA ADMINISTRATION item 3 | admit, mined |
| S480 | https://man7.org/linux/man-pages/man2/quotactl.2.html (copy sha256 `0d4ab273…`) | 2026-10-25 | "No disk quota is found for the indicated user. Quotas have not been turned on for this filesystem." — §ERRORS ESRCH | admit, mined |
| S481 | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/uapi/asm-generic/errno.h (copy sha256 `66a5ad60…`) | 2026-10-25 | "#define EDQUOT 122 /* Quota exceeded */" — errno.h:107 | admit, mined |
| S482 | https://help.aliyun.com/zh/nas/user-guide/set-quotas-on-the-subdirectories-of-nas-nfs-volumes (copy sha256 `747fef1b…`) | 2026-10-25 | "dd: closing output file '/data/1G.txt': Disk quota exceeded" — §验证目录配额限制 | admit, mined, scope limited to Alibaba NAS directory quotas |
| S483 | https://raw.githubusercontent.com/torvalds/linux/v7.2/arch/mips/include/uapi/asm/errno.h (copy sha256 `006286df…`) | 2026-10-25 | "#define EDQUOT 1133 /* Quota exceeded */" — arch/mips errno.h:131 | admit, mined (boundary row) |
| S484 | https://raw.githubusercontent.com/torvalds/linux/v7.2/arch/sparc/include/uapi/asm/errno.h (copy sha256 `530c3cc2…`) | 2026-10-25 | "#define EDQUOT 69 /* Quota exceeded */" — arch/sparc errno.h:43 | admit, mined (boundary row) |

S483/S484 were added by me after the counter froze: ScribeEntryA's draft said the number 122 is the Linux value; the
generic header is, but `arch/mips` and `arch/sparc` carry other numbers. `for a in mips sparc alpha parisc; do curl -s
https://raw.githubusercontent.com/torvalds/linux/v7.2/arch/$a/include/uapi/asm/errno.h | grep EDQUOT; done` → mips 1133,
sparc 69, alpha 69, parisc 69 (alpha and parisc were read by grep only, no copy kept, no row).

Changed in place (rule 2), old → new: none. S478's `recheck` stays `180d`. Round-47 routed defect 5 is a re-open note, not a cell:
S478 re-opens need a browser User-Agent — `curl -A 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)
Chrome/131.0.0.0 Safari/537.36' https://ieeexplore.ieee.org/ielx8/4629386/11644734/11540439.pdf`; a plain curl returns HTTP
418 (anti-bot), which is not a source failure. Re-verified 2026-10-25 by `ExecS478Recheck`: HTTP 200, sha256
`1603404dd25b3a0dff93f2dcb23c75b671d4e2d78da3cce8f461e87ebde6add2`, 14 pages. No registry row has an ISO-date `recheck`
(`w1/ExecS478Recheck.md` §4: 251 rows, all symbolic cadences).

### Assimilation (addendum §10) — theme FR2, filesystem quota observability

Package `/home/vgpnk/Projects/shokuknow/merge/mori/` read only; no campaign tool run; nothing written there.

- **Collision check** (before any append, `.ufo/waves/round-48/assimilation/{reg-ids,staged-ids,collisions}`):
  registry 251 ids, staged 136 ids → 8 collisions `S471 S472 S473 S474 S475 S476 S477 S478` (the first four were
  round 47's; S475–S478 are round 47's own new rows). The 0–3-space guard was re-proven on a scratch fixture: an
  indented `  | S002 |` row collides under the 0–3-space pattern (`w1/ExecCensusGuard.md`).
- **Renumber by document** (the URL is the evidence, the id follows it): staged S477 `xfs_quota(8)` → lane **S479**;
  staged S478 `quotactl(2)` → **S480**; staged S482 `errno.h` → **S481**; staged S479 Aliyun NAS page → **S482**.
  No staged id is kept. Staged S481 (RHEL 9 Japanese PDF) is not adopted (below).
- **Admit:** staged `quota-observability-r38.md`, rewritten as `corpus/knowledge/quota-observability-r48.md`: a claims
  table of 15 rows, each a located quote in a committed copy, correcting the staged entry where the copies disagree
  (the staged `Disk quota exceeded` claim holds — an ScribeEntryA note that the string is absent from the Aliyun copy was
  wrong, it searched raw HTML across tags and `w1/ScribeEntryB.md` located it; the staged link between that string and
  the lane's `dead_quota` seat class is false — `seat-terminal-status-r17.md:20` maps a Z.AI provider quota token, not a
  filesystem quota).
- **Reject, with flip:**
  - staged `quota-id-mapping-files-r41.md` — rows S502–S505 carry an unescaped `|` in the recheck cell (12 cells, not
    11: the used-by value is displaced, `w1/ScoutStagedQuota.md` §4), cite `S260/S261` rows this lane does not have
    (`grep -cE '^ {0,3}\| *S26[01] *\|' corpus/SOURCES.md` → 0), and anchor currency on RHEL 7. Flip: re-emit the rows
    with 11 cells, drop the dangling references, anchor on a current release.
  - staged `quota-path-listing-r42.md` — the entry says the lane holds S233 at a different scope and S260/S261; in
    this lane S233 is a gihyo cgroup article and S260/S261 do not exist (`w1/ScoutStagedQuota.md` §5). Flip: rewrite
    the cross-references to this lane's ledger; the print/report sentence itself was verified.
  - staged `quota-counter-freshness-r39.md` — the second Chinese quote drops 目录 from the page's wording, the API-repeat
    claim was never fetched, and the kernel-side freshness statement is an unmarked inference (§2). Flip: correct the
    quote, mark the inference, fetch or drop the API claim.
  - staged `quota-id-to-path-r40.md` — its own-work row points at evidence outside this lane (QUALITY 9 needs a
    lane-local pointer) and its cross-references are package-internal (§3). Flip: copy the receipt into
    `corpus/evidence/`, rename the references.
  - staged `alarm-latency-model-r39.md` — outside the FR2 theme this round; mori runs no alert channel, the page is
    another product's alarm model (FR8 vocabulary only). Flip: a concrete mori reporting requirement for the four
    clocks.
  - Solaris `errno=49` — Solaris's number (S484/S483 show the Linux numbers differ by architecture too); stays rejected.
  - RHEL 9 Japanese PDF and the staged `+` / `grace` claims — the freeze fetch returned HTTP 403 for both a plain and a
    browser User-Agent; `w1/ScoutStagedQuota.md` later got HTTP 200 (1,555,738 B). Classified `unreachable` at the
    freeze, not fabrication, and not part of this claim; no lane row, no copy. Flip: open a lane row with a committed
    copy and a located quote.
- **Quarantine slice** (`assimilation/quarantine-slice`: S244, S262, S268; register class "the cited source could not be
  fetched, so no quote was checked"): hand-checked by three scouts, none appended (no admitted entry cites them).
  - S244 — PRESENT: the DOI `10.1145/3643916.3644413` resolves; arXiv 2403.18832's abstract carries "98.9% of commits in
    our dataset contain sentences with rationale information" (`w1/ScoutQuarantineS244.md`). The lane has no S244 row.
  - S262 — PRESENT: ROMA, same document as lane S262/S478; the quote is in the publisher PDF fetched with a browser
    User-Agent (`w1/ScoutQuarantineS262.md`); the earlier failure is the IEEE bot wall (HTTP 202/0 bytes, 418).
  - S268 — PRESENT: the same ROMA PDF, sha256 `1603404d…`, lines 139–141 (`w1/ScoutQuarantineS268.md`). Note: the
    register's S268 row carried no quote; the quote located is the renumbered staged S507's.
- **considerthese:** `considerthese/2026-10-25.md` suggestion 2 (host-path portability count, opened 2026-10-25) lands
  as QUALITY 127 and the counting command below. `w1/ScoutConsiderthese.md` lists every suggestion's state; the next
  unimplemented one is 2026-10-25 #3 (flagged-versus-fixed critic count).
  Counting command (scope stated, because the reflection's "13" depends on it): tools — `git ls-tree -r --name-only
  <rev> -- tools/ | grep -E '\.(py|sh)$' | xargs git grep -l -F '/home/vgpnk' <rev> --` → 3 at both `e5dbac05` and
  `2d85e33d`; rounds 40–43 top-level wave instruments — same with `.ufo/waves/round-4[0-3]/` top-level → 10; together
  13, matching the reflection. All tracked `.py`/`.sh` under tools/ and `.ufo/waves/round-*/`: 395 at both revisions
  (`w1/ExecPortability.md`). The round-48 instruments (`count-c1.py`, `count-c2.py`, `tools/mori-unlanded-check.py`,
  `tools/mori-pin-check.py`) hold none; `.ufo/waves/round-48/build-w1-spec.py` holds some (a wave builder).

### Spot-check

Previous outside check: `corpus/lessons/round-47-verifier-spotcheck.md` (hyaku closure, @m_sonnet). Disagreements and
routed defects of that file, each with this round's disposition: defect 1 (late files untracked) → committed in
`356fb94a`, LOG erratum, and `tools/mori-unlanded-check.py` (M1 below); defect 2 (report filed after the driver's
`complete` line) → carried: this round's report is filed after the last wave settles and the pre-report gate, not
before; defect 3 (own routes) → the successor C2 shape (used-by arm, 0–3-space rows, one path per cell) is realised
in `count-c2.py`, the v2 selftest arms for symlink, argv sub-checks and case-insensitive `unparsed` are in the v3
selftest, line-count pins and truncated digests are v3 rules R5/R6; defect 4 → cited here; defect 5 → S478 note above.
Round-48 gate decisions are awaiting this round's non-author closure (LEARNING.md); sample offered: admit S479–S482
and the rewritten entry, reject staged `quota-id-mapping-files-r41.md` (12-cell rows, checked).

## Mistakes

| id | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M1 | landing | Round 47 filed its report while `w2/CritV2Junk.md`, `w2/MutV2Rebound.md`, `w2/ScoutMisroot.md` and `w2-results.json` were untracked (`corpus/lessons/round-47-verifier-spotcheck.md` §1, §5.1) | none — the pre-report gate checks the branch hash, not the working tree | `tools/mori-unlanded-check.py` (`UNLANDED_SELFTEST pass=13`); shown able to fail: arm `untracked_late_result_exit1_names_it` — the same check on a sandbox with a late `w2` file exits 1 and names it, exit 0 without it; run at the entering tip it prints `UNLANDED=dirty` for this round's own uncommitted wave files |
| M2 | survivor | The round-47 v2 pin check printed `PIN_CHECK=met` on eight structural junk edits (`evidence/control-c1-tool-v2-entering.txt`: `junk_met=8`, the same edits scored by `count-c1.py` at `e5dbac05`) | QUALITY 123 (re-run from committed bytes) — it checked values, not visibility | v3 rules R1–R6; shown able to fail: the counter scores the entering v2 `unmet` (`junk_met=8`), two stubs unmet (`evidence/control-c1-stub-*.txt`) and the landed v3 `met` |
| M3 | survivor | Wave-1 critic `w1/CritJunkClasses.md` D1 (digest of a decoy file named elsewhere in the row), D2 (tally on a continuation line), D5 (tally in another cell), D18 (tally outside backticks) all scored `met` under v2 and D1/D2/D5/D18 survive the spec's R1–R8 | none | v3 R9 (hidden tallies) and R10 (digest binds to the nearest preceding in-tree path); shown able to fail by selftest arms `r10_digest_decoy_file_in_other_cell`, `r10_trunc_digest_decoy_file_in_other_cell`, `r9a_tally_in_pinned_values_cell`, `r9b_continuation_line_tally`, `r9c_tally_outside_backticks`. Not closed: D7 (row names instrument A, self-test runs instrument B) — a rule turns four legitimate mutant-command rows red |
| M4 | number-drift | `SKILL.md:168` pinned the r14 harness as sha256 `c39e5a73…` since round 14; the harness changed and no file in the tree has that prefix (`w1/ExecRealRegistryAudit.md`: whole-tree scan of 12,111 files) | QUALITY 123 covers tallies and full digests, not truncated ones | v3 R6 found it (`pin line=168 kind=digest state=mismatch`, `PIN_CHECK=unmet … mismatches=1` at `e5dbac05`); the cell now names the historical blob and pins the current `533218a5…` |
| M5 | scope | `ExecV3ImplA` edited the tracked `tools/mori-pin-check.py` while implementing its candidate and restored it itself (`w1-results.json`); `CritC1Counter` and `ExecV3Residuals` saw the file dirty at 18:35 — the round-47 M4 class, again | the wave context "Write ONLY your own report file" (stated, not enforced); round-47 M4 detection was a sha256 compare | `tools/mori-unlanded-check.py` lists a modified `tools/` file (scope `tools/`); wave-end rule: the L1 runs it and the frozen-sha256 compare before integration. Not prevented: a seat can still edit and restore between two runs |
| M6 | attribution | Eight wave-1 results (`ScribeQuality`, `ScribeScorecard`, `ConnSiblings`, `ConnCrossClaim`, `RevC1Counter`, `RevC2Counter`, `MutC1Counter`, `MutC2Counter`) carry output of other lanes' seats of the same name (`w1-results.json`: reports at `.ufo/waves/round-45/…`, `round-47/…`, `round-49/…`, `round-40/…`, `round-55/…`) and no report is on disk under `w1/`; they did not run this lane's tasks | none | seat names are unique per round and lane in wave 2 (an `R48`-prefixed name); the count of seats with a report on disk is part of the report. Not shown able to fail: a duplicate-name check needs the orchestrator's registry |
| M7 | attribution | `w1/ScribeEntryA.md` stated that `Disk quota exceeded` is absent from the Aliyun copy; it searched the raw HTML, where the words are split by tags; the normalised copy holds it (offset 5042) | QUALITY 124 (counts carry their command) in spirit, not for negative claims | the claim is dropped; negative claims about a copy are made on the normalised text the counter uses |

## Wave 1 — integrated findings

- Counters (frozen, not changed): `w1/CritC1Counter.md` F1 — a tool that never reads the registry but keys on the
  harness's variant filename (`variant-J*.md`) or the per-variant `TMPDIR` name scores `C1=met`; and `w1/CritC2Counter.md`
  — eight 8–10-word fragments of `<script>`/JSON text in the copies score `C2=met`. Both are limits of the frozen
  predicates (P-C1 named "a tool can pass by being narrower than the junk"; this is the harness-leak form). Closure
  attack items for wave 2: the landed tool must contain no variant-name or `TMPDIR`-name branch, and the landed entry's
  quotes must be prose (reviewers check each row's claim against the surrounding page text, `w1/CritEntryRisk.md`).
- `w1/CritContractFreeze.md`: no freeze defect; four precision notes. `w1/ExecC1Replay.md`: labels J/H confirmed.
- `w1/ExecRealRegistryAudit.md`: one in-scope stale pin (M4).
- `w1/SentCopies.md`: copies scanned for credential material; `w1/SimpCounters.md`: dead code in the C1 selftest
  (one identity `text.replace` line), proposal for a successor, counters stay frozen.
- `w1/RevAssimPlan.md` F1 (the plan committed no Gate reject) is met by the rejects above; F2 (flip conditions for the
  RHEL PDF and Solaris `errno=49`) is met above; F3: `merge/mori/MERGE-REPORT.md`'s Adopt checklist conflicts with §10 —
  it names a `SOURCES-PROPOSED.md` that is not in the package, a sample re-open instead of every source, a bulk append of
  all 136 rows (which would import the eight colliding ids) and 80 copied entries. This round followed §10, not the
  checklist: one theme, one admitted entry, six appended rows, renumbered by document.
- `w1/CritV3Spec.md`, `w1/CritJunkClasses.md`, `w1/CritEntryRisk.md`: the spec's R4 keys on `(row name, prefix)` and
  not on the prefix alone; R5 and R6 disagree on which path a digest binds to; D1/D2/D5/D18 survive R1–R8 (M3); six
  claim/quote pairs the counter scores as met but a reader rejects (overclaim, negation context, example scope, other
  filesystem, vendor page used for Linux, a number from a comment) — the reviewer checklist for the entry in wave 2.
- Seat accounting for wave 1: 49 seats spawned; 39 wrote a report to `w1/`; ten did not — the eight of M6,
  `ExecV3ImplA` (aborted after editing the tracked tool and restoring it) and `ExecUnlandedCheck` (ended mid-debug, so
  the tool was written by the L1); results mapping in `w1-results.json`.
