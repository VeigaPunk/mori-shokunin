author: hyaku closure (non-author integrator, @m_sonnet)

# Round 48 — non-author closure spot-check (mori)

Lane HEAD before `e5dbac05459887d9597ea5d1da0d8e3d024e0d17`, after `14c5110d65a2f225e7316e1996e92090b9b8e7cb`.
Driver digest (`.ufo/watchdog.log:1408,1436`): `2026-10-25T17:31:00-03:00 launch mori round=48 pgid=1899782 driver=hyaku-inline attempt=1`;
`2026-10-25T20:27:28-03:00 complete mori round=48; hyaku-inline attempt=1`.
No lane gate or selftest was executed as a verdict source. Plain re-measurements ran in a throwaway
`git archive 14c5110d` export under `/tmp/cl48`; gate verdicts (`tools/mori-pin-check.py`, `count-c1.py`) are
evidence-verified from committed receipts.

## 1. Conformance (step 1)

| check | result |
|---|---|
| report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-48/mori.md` → `mori-shokunin e60eb16757781b9303b90e6d6972b2b8953d6d86`; committer date 20:27:04, before the driver's `complete` line (20:27:28) |
| `SHONEN` heading, one line per box | present; four boxes, each `[~]` with a pointer |
| cited lane commits are ancestors of `master` | `4387cf94 e4dfff32 91fbbc2a 14c5110d` → `merge-base --is-ancestor … master` true for all four |
| pushed | `jj-lane.sh state` → `local=remote=14c5110d… ahead=0 behind=0`; `ls-remote origin refs/heads/master` → `14c5110d…` |
| no uncommitted round work | `git status --porcelain` shows no tracked change and no round file outside `.scratch/`; 114 untracked `.scratch/{c1-*,pin-*,r48-*,r48w2-*}` directories (12/41/32/29) are seat-run debris, not round work |
| prompt carries the template contract | `.ufo/prompts/mori-round-48.md` carries §1–§5 of `templates/round-prompt.md` and the §6 hyaku addendum |

Defects (status-neutral): (a) 114 untracked `.scratch/*` directories left after the round (round 47 defect 1 was the
same class; the lane's `mori-unlanded-check.py` scope excludes `.scratch`, so it cannot see them); (b) the report
commit's **author** date is 20:22:17 but it cites `14c5110d` authored 20:26:17 (committer date 20:27:04 is correct;
an author-date back-dating, minor). The report is a real report
(four landed commits, 132 changed files), not a marker.

## 2. Claims (step 2)

### C1 — the pin reconciler cannot be turned green by the frozen junk (calibration) — evidence-verified

Re-measured (plain):
- `git show 14c5110d:tools/mori-pin-check.py | sha256sum` vs the freeze: `git diff e4dfff32 14c5110d --stat -- tools .ufo/waves/round-48/count-c1.py .ufo/waves/round-48/count-c2.py` is empty, so receipts measured at `e4dfff32` cover the final bytes.
- `sha256sum` of `count-c1.py`/`count-c2.py` at the tip → `7a2a6aa0…` / `0055aed1…`, equal to `evidence/freeze-sha256.txt` (counters unchanged since the freeze `4387cf94`). `controls/tool-v2-entering.py` hash `9832e38c…` equals the entering `tools/mori-pin-check.py` recorded at freeze.
- Pin repair: `git show 14c5110d:tools/mori-round14-regressions.py | sha256sum` → `533218a566030fda…` (same bytes at `e5dbac05`); `git show 5601d12:…` → `c39e5a735266…`. So the old SKILL.md:168 pin named a historic blob, not the file on disk; the new pin matches. Real defect found and repaired.
- `git show 14c5110d:SKILL.md | grep -c 'PIN_CHECK_SELFTEST pass=60'` → 1.

Evidence-verified, not executed (lane-owned gate; frozen counter run):
- before: `evidence/control-c1-tool-v2-entering.txt` → `C1=unmet junk_met=8 honest_unmet=0 real=met errors=0 variants=12 rev=e5dbac05…` rc 1; `control-c1-stub-always-met.txt` → `junk_met=8`; `control-c1-stub-always-unmet.txt` → `junk_met=0 honest_unmet=4 real=unmet`.
- after: `evidence/after-c1-at-e4dfff32.txt` → J1–J8 `got=unmet`, H1–H4 and `real` `got=met`, `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=e4dfff32…` rc 0.
- `selftest-c1.txt` `C1_SELFTEST pass=34 fail=0`; `selftest-c2.txt` `C2_SELFTEST pass=22 fail=0`.

Ruling: the before→after is consistent and both stubs fail, so the counter discriminates; the claim as declared (frozen eight junk
unmet, four honest and the real registry met) is verified. Limits the lane names honestly and I accept as stated: the frozen
counter is passable by filename sniffing (the landed tool holds no such branch, per its `w2/R48RevHarnessLeak.md`) and v3 still
accepts seven of fourteen new junk probes. Calibration is improved on the declared scope — the overreach was caught and routed, not hidden.

### C2 — FR2 quota entry (depth) — re-measured

- Registry rows: `git show <rev>:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` → 251 at `e5dbac05`, 257 at `14c5110d`; status mined 201→207, queued 24, rejected 26; malformed rows (NF≠13) → 0; SOURCES diff is +6/−0 (append-only).
- Absence sweep: `git show e5dbac05:corpus/SOURCES.md | grep -cE 'xfs_quota|quotactl|EDQUOT|repquota'` → 0; `git cat-file -e e5dbac05:corpus/knowledge/quota-observability-r48.md` → absent at entry.
- Independent located-quote check (my own script: strip tags, decode entities, collapse whitespace over the committed copies in `corpus/evidence/sources-r48/`): 15 rows parsed, **15 located, 0 missed** (quote lengths 7–25 words). Matches `after-c2-final.txt` `C2=met claims=15 located=15 quote_missing=0 bad_rows=0 sources=4 source_rows=ok pins=ok provenance=ok rev=91fbbc2a…` and `control-c2-donothing.txt` `C2=unmet … failed=entry_absent,pins`.
- Live re-open 2026-10-25: errno.h v7.2 line 107 `EDQUOT 122`; mips line 131 `1133`; sparc line 43 `69` — equal to the entry's per-architecture claim.
- Limit (named by the lane): location is not entailment; I read the 15 rows against their quotes and found no claim stronger than its quote (the superuser row already carries the reworded scope `XFS`).

Ruling: depth improved; claim verified (re-measured).

### Axes (SCORECARD.md diff, spot reads)

`git diff e5dbac05 14c5110d -- SCORECARD.md` is +41/−0 and appends a Round 48 section; no axis-table cell changed and no score
change is claimed. LOG.md +35/−0 (append-only); corpus/QUALITY.md +39/−0; SKILL.md +42/−2 (the two removed lines are the two registry
rows edited for the pin repair/v3); PROVINCE.md unchanged; SHONEN.md four `[~]` lines, no `[x]`. No axis is harmed.

| axis | verdict | basis |
|---|---|---|
| calibration (C1) | improved | frozen eight junk edits now `unmet`, honest edits `met`; stale pin found and repaired; limits (7/14 survivors, filename sniff) named, not hidden |
| depth (C2) | improved | 15/15 located quotes re-measured independently; registry 251→257, all six new rows re-opened or checked against committed copies |
| coverage | unchanged | no coverage claim; FR2 map row advanced in README but PROVINCE not changed |
| operability | unchanged | selftest 60/60 and 13/13 are evidence-verified capability only; not claimed |
| freshness | unchanged | one stale pin repaired but not claimed as the axis move |
| adjacency | unchanged | `PROVINCE.md:3-16` unchanged; no contested scope |

## 3. Discernment spot-check (LEARNING.md)

Lesson Gate at `corpus/lessons/round-48.md` §Gate.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S481 `errno.h` v7.2 | admit, mined | `curl -A <browser> https://raw.githubusercontent.com/torvalds/linux/v7.2/include/uapi/asm-generic/errno.h \| grep -n EDQUOT` → `107:#define EDQUOT 122 /* Quota exceeded */` | agree | quote short, located at the cited line; tier A (kernel source, tagged) |
| S480 `quotactl(2)` | admit, mined | man7 page, ERRORS ESRCH: `No disk quota is found for the indicated user. Quotas have not been turned on for this filesystem.` | agree | exact; supports the "ESRCH ≠ zero" row |
| S479 `xfs_quota(8)` | admit, mined | man7 page: `XFS distinguishes between quota accounting and limit enforcement.`; also `never enforced on the superuser (nor are they enforced for group and project ID zero)` | agree | both quotes present; the superuser row's reworded scope stays within the quote |
| S482 Alibaba NAS page | admit, mined, scope limited | help.aliyun.com (browser UA, HTTP 200, 117,506 B), `dd: closing output file '/data/1G.txt': Disk quota exceeded` found after tag-strip | agree | the scope restriction (one vendor, not mori thresholds) is the correct tier call |
| S483/S484 (arch errno) | admit, mined (boundary) | v7.2 `arch/mips/.../errno.h:131` → 1133; `arch/sparc/.../errno.h:43` → 69 | agree | live values equal the rows; the lane caught its own generic-122 overclaim |
| staged `quota-id-mapping-files-r41` | reject (12-cell rows, dangling refs) | `/home/vgpnk/Projects/shokuknow/merge/mori/SOURCES.append.md` S502–S505: `awk -F'\|'` → `NF=14` (12 cells; the contract needs 13); `git show 14c5110d:corpus/SOURCES.md \| grep -cE '^ {0,3}\|[[:space:]]*S26[01][[:space:]]*\|'` → 0 | agree | malformed rows and dangling S260/S261 references are objectively checkable |
| staged `quota-path-listing-r42` (S233 mismatch) | reject | lane `S233` row is a gihyo cgroup article (`grep` on the committed registry) | agree | the staged entry's cross-reference is false in this lane |
| RHEL 9 PDF / Solaris `errno=49` | reject / not adopted | not re-fetched; lane's own receipts (403 at freeze, later 200) cited | agree (unprovable to differ) | unreachable-at-freeze is correctly classed `unreachable`, not fabricated; flip condition stated |
| `SOURCES.md` rows S479–S484 new-row quotes | ≤25 words | S479 8 words, S480 18, S481 ≈7, S482 8, S483/S484 ≈7 each (counted by `wc -w` on the quoted text) | agree | all within 25 and located (3 re-opened live, 3 against committed copies) |

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → `mori ok` (W04 duplicate-url warnings only; rc 0).

## 4. Trend verdicts

- **expansion: improved.** One admitted entry on FR2 ground the map held only as a boundary row (sweep: 0 prior rows), citing mined S479–S484; capabilities added (junk-variant counter, unlanded check).
- **quality: unchanged.** No earlier entry was re-verified or superseded; the repaired stale pin is a SKILL.md pin, not an admitted entry; no admitted entry fails its re-check.
- **discernment: improved.** Every sampled admit and reject agrees with the outside re-check; the gate's own errors (M7, "four rows") were caught by wave-2 reviewers and fed lesson-backed QUALITY 125, 126, 128 (127 cites the operator considerthese item and the Gate).

## 5. Routed defects for round 49

1. Add `.scratch/` to the lane's unlanded check or `.gitignore`, and remove the 114 untracked scratch directories (`git status --porcelain` leftover).
2. Keep the filed report's author date at or after the lane tip it cites (author date 20:22:17 vs cited commit 20:26:17).
3. Carry the lane's own routes: seven v3 survivors (`R48CritV3Junk1`), the K2–K8 classes, rule R11 for D7, the selftest arms from the three mutation seats, a successor C1 counter that hides the variant identity and includes an honest pin-updating edit, unique seat names in wave 1 (M6).
4. SHONEN boxes are all `[~]` and not fully checkable by a non-author this round (the self-tests and a round-wide log are lane-asserted); promotion stays operator-owned.
