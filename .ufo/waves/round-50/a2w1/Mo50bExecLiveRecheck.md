# Mo50bExecLiveRecheck — round 50 a2w1 (live recheck of the C2 entry, census)

Seat: leaf executor, no subagent dispatched (none needed; every check is a direct command).
Lane: mori-shokunin. Read-only on the lane, the fleet repo and the host; the only file written is this report.

Revisions read (read-only `git show` / `git archive`; nothing added, committed or checked out):

| rev | role | SOURCES.md sha256 | entry sha256 |
|---|---|---|---|
| `487941b9395e89678af0053cc443cdb49cdee6e3` | attempt-2 landed data (the rev the counters score) | `33f294439e479f3891fbc5b71b5ceb0a623871cad6980285dcbc696be04fc185` | `0fac741cce21d76eda26b9b0a915509e34be499b52041cb7e6c3b1c8cb97c109` |
| `9b8562a371dc916fdc0fc686619ea1e271a3e118` | attempt-1 salvaged working tree (before-data side) | `2411aa96ec7ff6d5b94fbcf1d391310ead9da2542047d96ad6de3a7f08d40453` | — |
| working tree (HEAD `4548a34dc8b4072abaa4335c1f54a9efcfcc314a`) | live bytes | `33f2944…` (same as landed) | `0fac741…` (same as landed) |

Working-tree `corpus/SOURCES.md` and `corpus/knowledge/oom-memcg-stat-r50.md` are byte-identical to the landed rev, so no
post-landing drift exists in either scored file at the time of this seat.

Scratch: `/fast/scratch/hyaku/mori-r50/Mo50bExecLiveRecheck/` (two `git archive` extractions, 328 MB each;
`TMPDIR=/fast/scratch/hyaku/mori-r50/Mo50bExecLiveRecheck/tmp`). `disk-guard.sh status` before the run: rc=0,
`/fast/scratch/hyaku` 24% used, 614.0G free. Removed before yielding.

No tool installed or upgraded; no pacman; no clone (both revisions extracted from the existing repo with `git archive`).

## 1. The entry's recheck command (line 7), run verbatim

Line 7 is the `recheck:` line (`grep -nE '^(source:|verified-at:|recheck:)'` → 3,4,5 `source:`, 6 `verified-at:`, 7 `recheck:`).

```
$ export TMPDIR=/fast/scratch/hyaku/mori-r50/Mo50bExecLiveRecheck/tmp
$ for u in https://docs.kernel.org/7.2/admin-guide/cgroup-v2.html \
           https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/memcontrol.c \
           https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c; do
    curl -fsSL "$u" | sha256sum; echo "curl_rc=${PIPESTATUS[0]}"; done
2d716cb798eacf8fbcf431b52697fbb8c5ed8ea9f58ac15b2b55351247c0bf34  -
curl_rc=0
8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e  -
curl_rc=0
452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e  -
curl_rc=0
```

Three runs, three exit codes 0, three hashes in the entry's stated order. HTTP metadata (separate fetch, bytes discarded):

```
status=200 size=168438 effective=https://docs.kernel.org/7.2/admin-guide/cgroup-v2.html
status=200 size=160768 effective=https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/memcontrol.c
status=200 size=34311  effective=https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c
```

No redirect (`url_effective` equals the requested URL), and the sizes equal the committed copy sizes exactly
(168438 / 160768 / 34311), so the hashes are of the real documents, not of an error page.

## 2. Live hashes versus the committed copies (four-way)

| source | live fetch | entry line 7 records | committed copy (worktree) | `git show 487941b9:` | `git show 9b8562a3:` | `evidence/freeze-sha256.txt` |
|---|---|---|---|---|---|---|
| cgroup-v2.7.2.html | `2d716cb798eacf8fbcf431b52697fbb8c5ed8ea9f58ac15b2b55351247c0bf34` | same | same | same | same | same |
| memcontrol.c.v7.2 | `8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e` | same | same | same | same | same |
| oom_kill.c.v7.2 | `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e` | same | same | same | same | same |

Commands: `curl … | sha256sum`; `sha256sum corpus/evidence/sources-r50/*` in the lane; `git show <rev>:<path> | sha256sum`;
`cat .ufo/waves/round-50/evidence/freeze-sha256.txt`. All rc 0.

Two consequences, both observed:

- The entry's sentence "ran 2026-10-26; all three matched the committed copies" holds on an independent rerun today.
- The copies are identical at `9b8562a3` (attempt 1's salvaged tree, fetched a day earlier) and at `487941b9`, i.e. two
  independent fetches of the same tag-pinned URLs produced the same bytes. C2's `pins=bad` at the *entering* rev
  `7197160b` was therefore the copies' absence there, not different copy bytes.

The three SOURCES rows carry the same three hashes in their `anchor` cells (S489 `2d716…`, S490 `8a28e…`, S491 `452f…`),
so the registry, the entry and the files agree.

## 3. `sources-census.sh validate --root … mori`

```
$ cd /home/vgpnk/Projects/shokunin
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
mori	W04	S035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in across scopes
mori	W04	S037 duplicate url www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html across scopes
mori	W04	S073 duplicate url docs.python.org/3/library/pathlib.html across scopes
mori	W04	S074 duplicate url kubernetes.io/docs/concepts/architecture/controller across scopes
mori	W04	S075 duplicate url ftp.gnu.org/gnu/bash/bash-5.3.tar.gz across scopes
mori	W04	S076 duplicate url michaelfeathers.silvrback.com/characterization-testing across scopes
mori	W04	S147 duplicate url raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/docs/settings.md across scopes
mori	W04	S148 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes
mori	W04	S149 duplicate url man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html across scopes
mori	W04	S150 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml across scopes
mori	W04	S166 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes
mori	W04	S168 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst across scopes
mori	W04	S201 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c across scopes
mori	W04	S218 duplicate url github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch across scopes
mori	W04	S220 duplicate url raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c across scopes
mori	W04	S228 duplicate url docs.python.org/3/library/os.path.html across scopes
mori	W04	S349 duplicate url www.openeuler.org/whitepaper/openEuler%2024.03%20LTS%20%E6%8A%80%E6%9C%AF%E7%99%BD%E7%9A%AE%E4%B9%A6.pdf across scopes
mori	W04	S351 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori	W04	S470 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori	W04	S476 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
mori	W04	S486 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori	W04	S491 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
rc=0
```

- rc = 0, `ok`, no E-code (so S489–S491 pass E01–E12: rows 11-column, ids new, no duplicate URL+scope, kind/tier/status
  enums valid, `opened` a past date, `recheck` a legal cadence (`on-release`), no community-at-A, used-by paths exist).
- 22 W04 lines; the S491 line is present and reads exactly as the frozen contract characterises it — same URL as S003 and
  S476, different scope, warning not error. `grep -E '^\| *S003 *\|'` confirms S003 opens with the same
  `https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c` URL.
- Same command run inside the extracted landed tree (`cd $S/t4879 && sources-census.sh validate --file corpus/SOURCES.md`)
  also gives rc 0 with the same 22 W04 lines, so the working tree and the landed commit validate identically.
- The round-start receipt `.ufo/waves/round-50/evidence/census-start.txt` holds 21 W04 lines + `census-rc=0`. Landed = 22.
  The single new warning is S491; the other 21 are unchanged.

## 4. Manual census commands from `CORPUS.md` (`## SOURCES.md — where a shokunin learns`) at both revisions

Run from each extracted tree root (so the used-by existence check resolves against that revision's own files).

| metric (command) | `9b8562a3` (before data) | `487941b9` (landed) | delta |
|---|---|---|---|
| rows (`grep -cE '^\| *S[0-9]{3,} *\|'`) | 261 | 264 | +3 |
| malformed (`awk … NF!=13`) | 0 | 0 | 0 |
| tier histogram (`awk … $5`) | `A=230 B=14 C=17` | `A=233 B=14 C=17` | +3 A |
| status histogram (`awk … $9`) | `mined=211 queued=24 rejected=26` | `mined=214 queued=24 rejected=26` | +3 mined |
| duplicate ids (`uniq -d`) | (empty) | (empty) | 0 |
| enum / tier-inflation (`awk … NF==13`) | (empty) | (empty) | 0 |
| mined used-by path missing | (empty) | (empty) | 0 |

Exact outputs:

```
===== t9b85  (rev 9b8562a371dc916fdc0fc686619ea1e271a3e118) =====
rows: 261
malformed: 0
tier: A=230 B=14 C=17
status: mined=211 queued=24 rejected=26
-- duplicate ids:
-- enum/tier inflation:
-- mined used-by missing:

===== t4879  (rev 487941b9395e89678af0053cc443cdb49cdee6e3) =====
rows: 264
malformed: 0
tier: A=233 B=14 C=17
status: mined=214 queued=24 rejected=26
-- duplicate ids:
-- enum/tier inflation:
-- mined used-by missing:
```

Maintained parser corroboration (`sources-census.sh census --root … --file <extracted SOURCES.md> mori`), both rc 0:

```
487941b9: file rows 264 | tier.A 233 | tier.B 14 | tier.C 17 | status.mined 214 | queued 24 | rejected 26
           FLEET rows 264 | tier.invalid 0 | status.invalid 0 | missing 0
9b8562a3: file rows 261 | tier.A 230 | tier.B 14 | tier.C 17 | status.mined 211 | queued 24 | rejected 26
           FLEET rows 261 | tier.invalid 0 | status.invalid 0 | missing 0
```

Row-level delta (`diff` of the registry rows, 9b85 → 4879) is exactly three appended rows and nothing else:

```
261a262,264
> | S489 | Control Group v2 (v7.2) — https://docs.kernel.org/7.2/admin-guide/cgroup-v2.html | docs | A | … | mined | 2026-10-26 | on-release | corpus/knowledge/oom-memcg-stat-r50.md |
> | S490 | Linux mm/memcontrol.c at tag v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/memcontrol.c | code | A | … | mined | 2026-10-26 | on-release | corpus/knowledge/oom-memcg-stat-r50.md |
> | S491 | Linux mm/oom_kill.c at tag v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c | code | A | … | mined | 2026-10-26 | on-release | corpus/knowledge/oom-memcg-stat-r50.md |
```

Both new ids are fresh: max id at `9b8562a3` is `S488`, and `grep -cE '^\| *S489 *\|'` on that file is 0, so the
"renumber by document, next unused id" rule was applied without reuse (S533 → S489 as the contract states), and the
duplicate-id check on the landed file is silent.

## 5. Method notes (how not to misread these commands)

- `sources-census.sh validate --file <path>` resolves each mined row's `used-by` against the **current working
  directory**, not against the file's directory. Running it from a scratch cwd against an extracted `SOURCES.md` emits
  four spurious `E11` rows (`S488`, `S489`, `S490`, `S491 missing used-by corpus/knowledge/…`) and rc=1. Re-run with
  `cd <tree> && --file corpus/SOURCES.md` (or the lane-root `--root … mori` form) and it is rc=0 / `ok`. Recorded so no
  later seat reads that E11 batch as a defect of the landed data — it is an invocation artifact.
- The `overdue` mode treats `on-release` as symbolic (reported, never judged overdue), so the rows' cadence cannot be
  machine-overdue; only the entry's own `recheck: 90d` is a dated cadence.
- Live-state noise I observed and did not act on: `git status --porcelain` in the lane shows untracked
  `.ufo/waves/round-50/a2w1/`, `.ufo/waves/round-50/a2w1.ready`, and a `round-40/scratch/mori-conform-selftest-*`
  directory whose random suffix changed between two reads a minute apart — a live peer running a selftest, not lane
  drift. `.scratch/` is still tracked at the landed rev (225 files); the round-49 carrier that deletes it is a
  round-end action, so its presence mid-round is not a finding here.

## Findings

1. **LOW — `corpus/knowledge/oom-memcg-stat-r50.md:7`** — the recheck command is print-only: it emits three hashes for a
   human to compare against the list on the same line, does not diff them against `corpus/evidence/sources-r50/`, and
   exits 0 even when they differ; it also passes no `--max-time`, so a hung connection stalls a recheck run
   indefinitely. Mitigation present: the three expected hashes are embedded in the line, and today they matched
   exactly. Not a counter or predicate issue (both counters are frozen and neither reads this line).
2. **LOW — entry line 7 versus `corpus/SOURCES.md` S489–S491** — the entry declares `recheck: 90d` while all three rows
   declare `on-release`. Both forms are legal under SOURCES-CONTRACT-v1 rule `recheck`, and neither `validate` nor
   `count-c2.py` compares them, so the entry's freshness cadence is unenforced against its registry rows. Data-level
   inconsistency only; no scored predicate reads it.
3. **LOW — `scripts/sources-census.sh` (validate, `--file` mode)** — used-by paths are resolved against cwd, so the same
   registry file validates `ok`/rc 0 from its own tree and `E11`×4/rc 1 from a scratch cwd. A reviewer repeating the
   census in a scratch tree will see four false errors. Recorded as a named limit of my method, not a defect in the
   landed data (the lane-root `--root … mori` invocation used for the round receipts is unaffected: rc 0).
4. **LOW — `.ufo/waves/round-50/evidence/census-start.txt` versus a round-end census** — the W04 count moves 21 → 22 by
   the landed S491 row; the contract calls this expected ("a W04 warning, not an error"). Filed so that a later seat
   diffing start-of-round and end-of-round census output reads the delta as the new row, not as drift.

No HIGH or MED finding: on this seat's checks the entry's recheck claim, the three committed copies, the frozen sha256
pins, the S489–S491 registry rows and the census histograms are all internally consistent and consistent with the live
upstream bytes as fetched today.
