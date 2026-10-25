# ScribeLogErratum — round 48 w1 seat report

Seat: `ScribeLogErratum` (scribe, leaf). Assignment: draft the LOG.md `## Round 48`
entry head and an erratum for round 47 (fenced), per the frozen round-48 contract
(`.ufo/waves/round-48/contract.md`). Write only this report; drafts live inside it as
fenced blocks; no production file was touched; no tool install was needed
(nothing to record under the tooling-authorization rule). No subagents were dispatched.

## 1. Reads and checks performed (read-only)

All runs were read-only git / file reads on the lane repo at the round-48 entering tip
`e5dbac05459887d9597ea5d1da0d8e3d024e0d17`; no scratch was needed, so
`.scratch/r48-ScribeLogErratum/` was not created (nothing ran).

- `git cat-file -t 356fb94a` → `commit`; `git show --stat --oneline 356fb94a` →
  commit message `round-47: w2 settled — results, late reports (CritV2Junk, MutV2Rebound,
  ScoutMisroot), lesson note`, touching exactly:
  - `.ufo/waves/round-47/w2-results.json` (230 +)
  - `.ufo/waves/round-47/w2/CritV2Junk.md` (187 +)
  - `.ufo/waves/round-47/w2/MutV2Rebound.md` (152 +)
  - `.ufo/waves/round-47/w2/ScoutMisroot.md` (250 +)
  - `corpus/lessons/round-47.md` (6 +)
  - 5 files changed, 825 insertions. Exit 0.
- `git log --oneline -14` → `4387cf94` (round-48 freeze) → `e5dbac05` (round-47 verifier
  spot-check) → `356fb94a` (w2 settled, late files) → `dd17d927` (round-47 main landing,
  carries the report that said the three seats had not returned) → `68d66ca5` → …
- `git merge-base --is-ancestor 356fb94a e5dbac05459887d9597ea5d1da0d8e3d024e0d17` →
  exit 0 (printed `ANCESTOR_OK`): the late-files commit is an ancestor of the entering tip.
- `git rev-parse 4387cf94b69ddce455051a1ff38e93795c2e6cde` and
  `git rev-parse e5dbac05459887d9597ea5d1da0d8e3d024e0d17` → both resolve to exactly the
  contract's freeze and entering-tip hashes. Exit 0.
- `git status --porcelain` → 16 untracked paths (exit 0). None is a round-47
  `.scratch/r47-*` or `r47w2-*` path; the residue is this round's own scratch
  (`.scratch/r48-*`, 10 dirs), the L1's not-yet-committed wave files
  (`.ufo/waves/round-48/w1*`), and two pre-existing dirs
  (`.scratch/pin-check-9_ifrvgu/`, `.ufo/waves/round-40/scratch/mori-conform-selftest-id510ti3/`).
- `read` `corpus/lessons/round-47-verifier-spotcheck.md` §5 — routed defects 1–5
  (quoted in §4).
- `read` `corpus/lessons/round-47.md` — `## Spot-check` (lines 55–58) reads "No non-author
  spot-check of this round's gate decisions exists yet; the hyaku closure session is the
  outside check" (defect 4).
- `read` `corpus/SOURCES.md:raw:257` (S478 row) — the `recheck` cell is `180d`; the
  browser-User-Agent fact appears only in the `anchor` cell ("fetched 2026-10-25 with a
  browser user agent") (defect 5).
- `read` `considerthese/2026-10-25.md` — suggestion 2 (lines 47–49): "Keep a host-path
  portability list. Track how many wave instruments and `tools/` scripts contain an absolute
  `/home/vgpnk` path, and report the change day to day. The count is 13 files today."
- `read` frozen round-48 artifacts (verbatim, exit 0):
  - `contract.md`, `v3-spec.md` (cited in the drafts).
  - `evidence/freeze-sha256.txt` — 11 frozen hashes incl. `9832e38c…  controls/tool-v2-entering.py`
    and `9832e38c…  tools/mori-pin-check.py` (the entering v2 bytes).
  - `evidence/control-c1-tool-v2-entering.txt` — enter v2 control:
    `C1=unmet junk_met=8 honest_unmet=0 real=met errors=0 variants=12 rev=e5dbac05…`, rc 1;
    every junk variant J1–J8 is `expect=unmet got=met rc=0`, every honest H1–H4 + real is
    `expect=met got=met rc=0`.
  - `evidence/control-c1-stub-always-met.txt` — identical to the do-nothing receipt
    (`C1=unmet junk_met=8 … rc=1`).
  - `evidence/control-c1-stub-always-unmet.txt` — `C1=unmet junk_met=0 honest_unmet=4
    real=unmet errors=0 variants=12 rc=1`.
  - `evidence/control-c2-donothing.txt` — `C2=unmet claims=0 located=0 quote_missing=0
    bad_rows=0 sources=0 source_rows=bad pins=bad provenance=bad rev=e5dbac05…
    failed=entry_absent,pins rc=1`.
  - `evidence/selftest-c1.txt` — `C1_SELFTEST pass=34 fail=0`.
  - `evidence/selftest-c2.txt` — `C2_SELFTEST pass=22 fail=0`.
  - `evidence/sweep-quota-rows.txt` — `# grep -cE 'xfs_quota|quotactl|EDQUOT|repquota'
    corpus/SOURCES.md at e5dbac05` → `0`.
  - `evidence/census-start.txt` — `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`
    → 19 W04 lines + `mori ok …/corpus/SOURCES.md` (exit 0 at freeze).

No gate was rerun to decorate this report; every fact above comes from the run shown.
Nothing is UNVERIFIED.

## 2. Draft A — LOG.md `## Round 48` entry head (fenced; result lines left out for the L1)

```markdown
## Round 48 (L1 MoriR48; C1 calibration, C2 depth)

Froze at `4387cf94b69ddce455051a1ff38e93795c2e6cde` (contract P-C1/P-C2, `tools/mori-pin-check.py`
v2 entering control, `count-c1.py`, `count-c2.py`, v3 spec, controls, the four quota source copies under
`corpus/evidence/sources-r48/`) on entering tip `e5dbac05459887d9597ea5d1da0d8e3d024e0d17`
(round-47 closure). Before: `C1=unmet junk_met=8 honest_unmet=0 real=met errors=0 variants=12` rc 1
with the entering v2 tool (`evidence/control-c1-tool-v2-entering.txt`), `C2=unmet … failed=entry_absent,pins`
rc 1 (`evidence/control-c2-donothing.txt`); frozen sha256s in `evidence/freeze-sha256.txt`.

- **C1 — calibration (5): the pin reconciler cannot be turned green by the junk the round-47
  closure found.** `tools/mori-pin-check.py` v3 rejects the eight frozen junk edits J1–J8 (header
  spelled selftest, fullwidth and Cyrillic prefix rows, archived-copy rebinding, fenced replacement,
  blank-line hiding, stale line-count pin, stale truncated digest) and accepts the four honest edits
  H1–H4 and the real registry, under `--min-tally-pins 26 --baseline-rev 2d85e33d…`.
- **C2 — depth (5): filesystem-quota observability (FR2), field by field, each claim a located
  quote.** `corpus/knowledge/quota-observability-r48.md` opens with `source:`/`verified-at:`/
  `recheck:` and a claim/source/quote table of ≥8 rows, each quote 6–25 words located in the
  committed copy under `corpus/evidence/sources-r48/` (xfs_quota.8.html, quotactl.2.html, errno.h,
  aliyun-nas-quota.html); each row cites a mined S-id opened 2026-10-25 (new ids start at S479;
  staged S477–S482 collide with lane S477/S478 and are renumbered by document).
- Assimilation (theme FR2, quota): staged entry `knowledge/corpus/knowledge/quota-observability-r38.md`
  from `/home/vgpnk/Projects/shokuknow/merge/mori/` (read-only); admit/reject per entry in the lesson
  `## Gate`, with the quarantine-slice rows S244/S262/S268 hand-checked.
- considerthese: `considerthese/2026-10-25.md` suggestion 2 (host-path portability count — 13 files
  today) lands as a lesson and QUALITY criterion with the counting command.

**Evidence:** `.ufo/waves/round-48/` — `contract.md`, `v3-spec.md`, `count-c1.py`, `count-c2.py`,
`controls/{tool-v2-entering.py,stub-always-met.py,stub-always-unmet.py}`,
`evidence/{freeze-sha256.txt,control-c1-tool-v2-entering.txt,control-c1-stub-always-met.txt,
control-c1-stub-always-unmet.txt,control-c2-donothing.txt,selftest-c1.txt,selftest-c2.txt,
census-start.txt,sweep-quota-rows.txt}`.
```

## 3. Draft B — erratum for round 47 (fenced, append-only style per house precedent)

```markdown
## Erratum appended round 48 — round-47 late files and routed defects

Appended after the filed bytes; the round-47 entry above is not rewritten (round-47 closure routed
defect 1; round-48 C1/C2). The round-47 report said the three w2 seats `CritV2Junk`,
`MutV2Rebound`, `ScoutMisroot` had not returned and their results were uncommitted; they are
committed in `356fb94a` ("round-47: w2 settled — results, late reports …, lesson note", 5 files,
+825, ancestor of the entering tip `e5dbac05`):

- `.ufo/waves/round-47/w2-results.json`
- `.ufo/waves/round-47/w2/CritV2Junk.md`
- `.ufo/waves/round-47/w2/MutV2Rebound.md`
- `.ufo/waves/round-47/w2/ScoutMisroot.md`

The round-47 `.scratch/r47-*`/`r47w2-*` debris is no longer untracked in the round-48 working tree.

Routed defect dispositions (source: `corpus/lessons/round-47-verifier-spotcheck.md` §5):

1. **Late seat results never committed (landing class).** *Fixed:* the four files above are
   committed at `356fb94a` and named by this erratum; the r47 scratch dirs are gone from the
   working tree (`git status --porcelain` shows none).
2. **Report filed after the driver's `complete` line (17:27:24 vs 17:25:39).** *Carried:*
   observational and status-neutral per the spot-check §1 ("noted, status-neutral"); no retroactive
   repair exists, and round-48 keeps the same commit-with-round reporting path.
3. **Carry the lane's own routes** (successor `count-c2` shape; v2 selftest arms; line-count and
   truncated-digest pins; lesson F4 citation precision). *Fixed in the frozen round-48 artifacts:*
   the count-c2 successor shape (used-by arm, 0–3-space rows, one path per cell) is realized in
   `count-c2.py`; the v2 selftest arms (symlink containment, argv sub-checks, case-insensitive
   unparsed) ride C1's v3 tool work (`v3-spec.md` R8); line-count and truncated-digest pins are v3
   rules R5/R6. *Carried:* the F4 citation-precision element (no round-48 artifact targets it).
4. **Lesson `## Spot-check` says "no spot-check exists yet".** *Fixed by citation:* this entry and
   erratum cite `corpus/lessons/round-47-verifier-spotcheck.md` (§5 is the source of these
   dispositions); the round-47 lesson file itself stays untouched (append-only).
5. **Record the browser User-Agent in S478's recheck.** *Partially:* the S478 row's anchor cell
   already records "fetched 2026-10-25 with a browser user agent", but the `recheck` cell still
   reads `180d` — *carried* for the recheck-cell wording.
```

## 4. Dispositions at a glance

| # | defect | disposition |
|---|---|---|
| 1 | 53 untracked paths incl. late w2 files | fixed — committed at `356fb94a`, scratch debris gone, named by erratum |
| 2 | report filed after driver complete | carried (observational, status-neutral) |
| 3 | lane routes (count-c2 shape, selftest arms, pins, F4) | fixed — frozen round-48 contract/counters/v3 spec (R5/R6/R8); F4 element carried |
| 4 | lesson says no spot-check exists | fixed by citation of `round-47-verifier-spotcheck.md` |
| 5 | S478 recheck browser-UA note | partial — fact in anchor cell, recheck cell still `180d`, carried |

## 5. Limits

- The drafts are exactly that: fenced blocks in this report. The L1 integrates them into LOG.md
  and appends the result/wave lines after the landed run; nothing here pre-empts those lines.
- No production file (LOG.md, SKILL.md, SOURCES.md, corpus/, tools/, frozen round-48 files) was
  written or edited by this seat.
