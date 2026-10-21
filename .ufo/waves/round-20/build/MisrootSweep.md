# MisrootSweep: mori round 20 (read-only sweep)

Seat `MoriR20.MisrootSweep` (leaf scout). Local clock is `-0300` (UTC−3). Read-only: nothing deleted, moved, or written except this report. No git writes. No tools installed or updated. No subagents.

## Verdict

- **Untracked fleet-root files whose content names mori round 20 or a wave-1 seat: none.**
- Untracked fleet-root files in total: **one**, `.ufo/waves/round-20/final/AuditCase07.md`. Its content is the souji lane's round-20 audit, not mori's (§2).
- Wave-1 member report trailers pointing outside the lane `build/`: **0 of 76**. The fleet root has no `.ufo/waves/round-20/build/` (§3).
- Historical mori misroots documented in `corpus/lessons/round-16.md` to `round-19.md`: **two entries covering three files**, all in round 16. All three were relocated or archived. Rounds 18 and 19 document none (§4).
- Method caveat: the archived misrooted `MoriR16.Lesson` contains no mori, seat, lane, or round token, so a content-only check would miss it. This sweep enumerated every untracked entry and checked both names and content (§4.4).

## 1. Commands and results (all read-only)

- `git -C /home/vgpnk/Projects/shokunin status --porcelain` → ` M .ufo/state/{kagi,kama,mori,tabi}.report-baseline`, ` M .ufo/watchdog.log`, `?? .ufo/waves/round-20/`.
- Same command with `-uall` → `?? .ufo/waves/round-20/final/AuditCase07.md`, the only untracked file.
- Guarded re-run, `git --no-optional-locks … status --porcelain -uall` → identical.
- `git check-ignore -v -- mori-shokunin .ufo/waves/round-20` → `.gitignore:1:*-shokunin/	mori-shokunin`; `round-20` is not ignored.
- Disclosure: the first two status runs did not pass `--no-optional-locks`. `git status` may refresh `.git/index` under an optional lock. No tracked content changed, and the guarded re-run matched. This is the deviation class recorded at `round-17.md:239`.
- Name checks:
  - Untracked file, ignored scratch dirs: the 76 wave-1 names plus `mori`, case-insensitive.
  - `.tower` report subtrees: `MoriR20|mori-r20|mori-shokunin/.ufo/waves/round-20` plus the 76 names as whole words, case-sensitive.
  - Positive control: a subset including `MisrootSweep` matched `round-17.md:17` and `:239`.
- One overbroad read-only pass: a `find`/`sha256sum` over `mori-shokunin` that did not prune `.ufo/worktrees/` (§6).

## 2. Untracked fleet-root files and residue

| Path (fleet root) | Size · mtime (local) | Names mori round 20 or a seat? | Attribution from content |
|---|---|---|---|
| `.ufo/waves/round-20/final/AuditCase07.md` (**untracked**) | 8,784 B · 2026-10-21 07:02:53 | No. `mori`: 0 matches. 76 names: 0 matches. | "AuditCase07: round-20 C1 case `deliver-exact-patch`". Names souji paths (`tools/souji-seat-audit.py`, `/var/tmp/souji-r20-audit-contract.*`, wave `souji-r20w2-audit-contract`). Self-described author-side advisory. Owner: [INFERENCE] souji lane; the file records no owner. |

- Empty directories, invisible to git: `.ufo/waves/round-20/w1/` (06:57:00, before mori's dispatch) and `.ufo/waves/round-17/w1/` (2026-10-20 12:27:49). Mori's wave-1 `reportDir` is `.ufo/waves/round-20/build`, so neither is a mori target.
- `.ufo/waves/round-20/` mtime is 07:27 local (10:27Z), the minute of mori's dispatch (`dispatched_at` `2026-10-21T10:26:45Z..10:27Z`). No current entry explains the change. [INFERENCE: a transient entry was created and removed; not observed.]
- Tracked, not untracked: `.ufo/waves/round-16/` holds six committed files (`before.md`, `dispatch.md`, `clobber/classify.{sh,out}`, `gate/{mutate.sh,runs.md}`) from commit `7c5b34f` (2026-10-19). They are fleet round-16 protocol material (R16Planner, R16Connector, "kaika worktrees"), with no mori tokens. Not misroots.
- The tracked modifications in §1 were not diffed or attributed. They are outside this sweep's scope.

## 3. Seat-name cross-check

- Names: 76 `mori-r20-build` members from `wave1-run.json` `.taskCall.tasks`. `wave1-dispatch-receipt.json` reports `returned_count` 76.
- Untracked file: 0 matches.
- Ignored `.ufo/waves/*/*-scratch/` (`.gitignore:5`): 14 dirs, 36 files, 2,802,336 B, 0 matches. Names are xsentinel/xconnector outputs. Contents not printed, since some are secret-scan outputs.
- `.tower/` report subtrees (`.git/info/exclude:8`): 0 matches for the mori seat-ID forms or the 76 whole-word names (§5).
- Fleet-root top-level names matching `mori|lesson|seat|misroot`, case-insensitive: only `mori-shokunin`.
- Trailers: all 76 `Report:` paths are distinct and under `.ufo/waves/round-20/build/`. None is outside the lane. The C2 "misrooted" test (same relative path under the fleet root) therefore has no fleet-root candidate for this wave.

## 4. Historical mori misroots (lessons round-16 to round-19)

### 4.1 Fleet-root misroots (the lessons' own term)

| ID | Lesson record | Misrooted file(s) | Verified now |
|---|---|---|---|
| **R16-A** | `round-16.md:244` (M33, "misroot / scope"). Evidence: `mori-shokunin/.ufo/waves/round-16/evidence/misroot-sweep.json` | `FieldDocs.md` and `ReviewLesson.md` were written under fleet `.ufo/waves/round-16/build/` despite absolute-path instructions. Attribution: seat header `MoriR16`, target `mori-shokunin`. | Lane copies present: `mori-shokunin/.ufo/waves/round-16/build/FieldDocs.md` (31,345 B, sha256 `e451a53aced2c5ba0951f56b92ba4ec689854eb0318e924753922a60edf76778`) and `ReviewLesson.md` (10,681 B, sha256 `e6eaf7540592317e380914c3db11b61f82efd76f853d189f086fda5585fd679c`). Both match the record's `lane_sha256`. Fleet `round-16/build/` is absent. The record says the copies were byte-exact (cmp 0) and the fleet copies deleted. |
| **R16-B** | `round-16.md:264-267`. Detail: `round-17.md:34-36, 66, 114, 136-138` | Plain file `MoriR16.Lesson` at fleet root, 847 B, sha256 `15f9f82d707d5c79b11643eed1ab4754b6959d2bede5887e07364442ada5510e`. Missed by the round-16 pathspec sweep. Found later by non-author closure. | Archived: `mori-shokunin/.ufo/waves/round-17/frozen/MoriR16.Lesson` and `…/frozen/c3-tree/MoriR16.Lesson`, both 847 B with the same sha256. No `MoriR16.Lesson` at fleet top level now. |

The round-16 sweep's recorded `command` is `git -C /home/vgpnk/Projects/shokunin status --porcelain -- .ufo/waves .ufo/reports` (`misroot-sweep.json`). The pathspec limited the scan to two directories, so R16-B was outside it.

### 4.2 Round-17 detection and deviation records (not new misroots)

- `round-17.md:34-36`: admit C3 only against the byte-exact `frozen/MoriR16.Lesson`. Reject the old pathspec sweep's clean result as evidence of a clean fleet root.
- `round-17.md:66` (M1): the prior addendum wrongly prescribed a pathspec. The fix is a no-pathspec sweep that checks filename or content.
- `round-17.md:136-138`: the C3 witness. The legacy pathspec detected 0. The default detected exactly `MoriR16.Lesson`.
- `round-17.md:239` (M12): "MisrootSweep sandbox git writes exceeded its narrow exception", and some git-status calls lacked optional-lock guards. Recorded as a scoped deviation, "not proof of live data loss".
- `round-17.md:349-354`: the final unrestricted sweep reported 0 misroot candidates. Ten untracked entries were driver baselines or unattributed. None was claimed or deleted.

### 4.3 Related outside-lane or wrong-target writes (the lessons label these "scope", not "misroot")

- `round-16.md:64` (M20): sibling seat `MoriR16.ReviewCounts` overwrote the lane file `corpus/lessons/round-16.md` with an 11-byte placeholder. The placeholder was restored. In-lane.
- `round-16.md:65-67` (M21–M23): `/tmp` writes (`/tmp/x`, `/tmp/sc.tsv`, `/tmp/_pack_ps.txt`, `/tmp/__none`, `/tmp/_jr_err`) and a `mktemp -d` under `/tmp`. Outside the lane, not the fleet root.
- `round-17.md:238` (M11): accidental `/tmp/does-not-exist` writes and sandbox git/jj experiments without `-R`.

### 4.4 Method note: content-only checks miss this class

`round-17/frozen/MoriR16.Lesson` (847 B) is a BootContinuity disclosure. A case-insensitive search for `mori|MoriR16|round|R16|lane|Seat` matched only the substring "round" inside "background". The file has no mori, seat, lane, or round token. A detector keyed only on content would have missed R16-B, so a filename check is required. This sweep enumerated every untracked entry and checked both name and content.

### 4.5 Rounds 18 and 19

- `round-18.md` (68 lines): no misroot, fleet-root, relocation, archive, pathspec, or untracked record.
- `round-19.md` (253 lines): no such record. Related but not a misroot: `round-19.md:104-113` ("Recovery interruption and evidence gaps"). At recovery "many started seats had no final body", and "missing reports are missing evidence". No location is recorded.
- Lane evidence files, not lesson text:
  - `round-18/evidence/misroot-sweep.txt`: fleet-root untracked at that observation were `?? .ufo/waves/round-25/` and `?? .ufo/waves/round-37/`. Neither is mori-named. Owners not examined.
  - `round-19/evidence/misroot-sweep.json` (`mori-misroot-observation-v1`): `own_candidates` 0, `moves_or_deletions` 0, empty status output.

## 5. Blind spots (what `git status` cannot show)

- `.gitignore:1` `*-shokunin/`: `mori-shokunin` and 20 sibling lanes are invisible to `git status`. Sibling lanes were not opened.
- `.gitignore:5` `.ufo/waves/*/*-scratch/`: 14 dirs, 36 files, 0 matches (§3).
- `.gitignore:6` `r80-baseline-frozen-worktree/`: absent.
- `.git/info/exclude:7` `.devin/mcp_config.local.json`: no such file at `.devin/` top level. Not read.
- `.git/info/exclude:8` `.tower/`: 4,930 regular files.
  - Report subtrees (`quarantine`, `comms/findings`, `comms/reviews`, `comms/missions`, `comms/MISSIONS.md`, `jj-probe`): 0 matches for the mori seat-ID forms or the 76 whole-word names. A broad case-insensitive `mori` search instead matched other lanes' cross-references (chousa LOG, research-gate comments, quarantine README), none naming a round-20 seat.
  - Filenames with `mori|r20|round-20` across `.tower`: 6, all under `jj-probe/` for `kotoba-shokunin` and `chousa-shokunin`.
  - Not content-searched: `comms/inbox`, `comms/log`, `comms/state.json` (message and state stores).
  - `.tower/quarantine/kaika-fleetroot-20261019/` (2026-10-19) holds kaika-lane files quarantined from the fleet root, for example `dedupe.rs`, `gc-v2.54.0.c`, and `mado-LOG-append.diff`. Not mori. Names only.

## 6. Caveats

- Git: the first two status runs lacked `--no-optional-locks`. See §1.
- My `find`/`sha256sum` pass over `mori-shokunin` did not prune `.ufo/worktrees/`. It ran about 180 s and printed 32,190 lines, roughly 16,000 matching paths [INFERENCE: each path printed a find line and a hash line]. It exposed nested worktree copies, for example `mori-shokunin/.ufo/worktrees/round-19/ContentGate/.ufo/worktrees/round-19/ContentGate/…/frozen/MoriR16.Lesson`. I did not analyze them. Nested worktrees inside the lane may be a hygiene problem for L1 [INFERENCE: cause not checked].
- Tool discipline: I used shell `grep` and `awk` for a fleet-root name filter and a byte sum. Neither was a content search, and I did not repeat them.
- Not verified: the round-19 "48 missing reports" figure. It comes from the contract's citation of MANIFEST closure notes, not from the lesson file. `round-16-verifier-spotcheck.md:202-219`, cited by round-17 M1, is outside the requested file set and was not read.
- The fleet-copy deletions in R16-A and R16-B are taken from the lane records and the observed absence. I did not observe the deletions.

## 7. For the main agent (no action taken by me)

1. Record an owner for `.ufo/waves/round-20/final/AuditCase07.md`. It is not a mori file. It shares the `round-20` path namespace, and its content points to the souji lane.
2. After integration, re-run the sweep with the guard: `git --no-optional-locks -C /home/vgpnk/Projects/shokunin status --porcelain --untracked-files=all`. Add the filename check and the scratch-dir check (§3, §5). Untracked entries can change between runs; round-17 recorded transient ones.
3. Explain the 07:27 mtime change on `.ufo/waves/round-20/` (§2). Its cause is unobserved.
