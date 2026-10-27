# Mo55Scout02 — package/considerthese state + selected source routes (reopen, read-only)

Seat: scout (leaf, no dispatch, non-voter). Round-55 wave w1, mori-shokunin lane.
Entered: HEAD `b8a70adf93ebd9d1e4e95bef8627a220f2fa816b`; entering tip per contract `ca52426ea496bc6592e3e867cc9d28843e45f196`.
Access date for all live route reopens: **2026-10-27 (UTC ~06:44–06:52; local −03)**.
Method: read-only shell + `curl` (no writes outside this report and my scratch `/fast/scratch/hyaku/mori-r55/Mo55Scout02`, removed at exit).

## 1. Package state (reopened)

Lane lesson claim under test (`corpus/lessons/round-55.md:74`): "No `merge/mori/` package entry was adopted" this round; assimilation none.

Observed:

- Fleet root has no `merge/`: `ls /home/vgpnk/Projects/shokunin/merge/` → `No such file or directory`.
- The campaign package lives in the corpus-expansion repo: `/home/vgpnk/Projects/shokuknow/merge/mori/` exists, mtime **2026-10-24 23:33** (three days before this round opened). Contents: `MERGE-REPORT.json` (35,006 B), `MERGE-REPORT.md` (20,896 B), `SOURCES.append.md` (154,847 B), `amendments/corpus/knowledge/` (5 files), `knowledge/corpus/knowledge/` (dozens of files).
- `MERGE-REPORT.md:1-8`: staged by `corpus-expansion-1`; "Nothing was written into the lane repo."; 136 proposed rows accepted / 0 refused; 80 proposed knowledge entries; first staged id S471.
- No lane commit in the round-55 range touches it: `git log --oneline ca52426e..HEAD --name-only` shows only round-55 corpus/evidence/wave files; no `merge/`, no shokuknow writes.
- Package dir is byte- and mtime-unchanged since staging (all entries `Oct 24 23:33`).

Verdict: package state matches the lesson — present, unopened, unadopted this round. No new package material arrived during w1 (directory mtimes predate the freeze `c9b908f0`).

## 2. considerthese state (reopened)

Observed:

- `considerthese/` holds 8 daily reflections, `2026-10-19.md` … `2026-10-26.md`. No `2026-10-27.md`.
- Latest commit `649e14cf considerthese: 2026-10-26 daily reflection` **is an ancestor** of the entering tip: `git merge-base --is-ancestor 649e14cf ca52426e` → exit 0. The reflection predates round 55.
- `git log --oneline ca52426e..HEAD -- considerthese/ tools/` → **empty**. No considerthese file and no tool changed in the round-55 range.
- `considerthese/2026-10-26.md` proposals (read in full):
  1. split pin-check mismatches into "can't run here" vs "stale";
  2. carry the unfixed-flag ledger forward round over round;
  3. re-execute closures that were only evidence-verified;
  4. keep a suggestion-adoption status line.
- Adoption check this round: no `tools/` commits exist in `ca52426e..HEAD`, so proposals 1–3 have no implementation landing in r55; proposal 4 has no new adoption-status line in the round (the lesson's assimilation paragraph at `round-55.md:74` records the check itself: suggestions "were checked; its outstanding pin-environment split and carry-over-flag ledger are not part of the frozen claims").
- Working tree: `git status --porcelain` shows `M corpus/QUALITY.md`, `M corpus/knowledge/disk-runway-enospc-r55.md`, `M corpus/lessons/round-55.md` — none under `considerthese/`. Uncommitted, mid-wave, untouched by this seat.

Verdict: considerthese state matches the lesson. The four 2026-10-26 proposals remain outstanding, unacted, and correctly excluded from the frozen claims.

## 3. Selected source routes (reopened; exact access date + quote/failure)

### 3.1 git.kernel.org canonical routes — new failure mode observed

All three `git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/...` routes tested returned **HTTP 200 with a 7.7 KB HTML anti-bot challenge** ("Making sure you're not a bot!" — Anubis/LF challenge), not source bytes:

```
=== .../plain/fs/xfs/xfs_super.c?h=v7.3            HTTP 200 bytes=7724
=== .../plain/Documentation/filesystems/tmpfs.rst?h=v7.3 HTTP 200 bytes=7744
=== .../plain/Documentation/ABI/testing/sysfs-fs-btrfs?h=v7.3 HTTP 200 bytes=7744
```

Body head (identical boilerplate for all three): `<!doctype html><html lang="en"><head><title>Making sure you're not a bot!</title>...`.

Finding: the HTTP-200 challenge page **mimics success on a status-code-only check**; only body inspection or sha256 comparison detects the block. This matters for any future seat that reopens a pinned git.kernel.org route with `curl -w '%{http_code}'` or `curl -o` without hashing the body. The r55 capture receipts predate this; the SOURCES.md access-route URLs remain correct but no longer curl-reopenable as of 2026-10-27.

### 3.2 Mirror reopens — all pinned copies re-confirmed

Mirror used: `https://raw.githubusercontent.com/torvalds/linux/<tag>/<path>` (tag-for-tag with the pinned copies). Every reopened body is sha256-identical to the lane's frozen copy in `corpus/evidence/sources-r55/`:

| Row | Route (mirror) | HTTP | Live sha256 | Pinned sha256 | Match |
|---|---|---|---|---|---|
| S537 | .../v7.3/fs/xfs/xfs_super.c | 200 (72,886 B) | `0f806bf4ea1859a482d8a7031e2e4c2a80835b3bdd15a4d5fb2ae11c91eed831` | same | ✓ |
| S540 | .../v7.3/Documentation/filesystems/tmpfs.rst | 200 (13,078 B) | `5ce3dffe9323912b9146a5f33744776ff623ef42cf8accd6b2dfbea0b9db5be6` | same | ✓ |
| S536 | .../v7.3/fs/statfs.c | 200 | `34e684be1575eb3ce9938a01a8fd2d62e92b0be8fac1a46092884f7600905398` | same | ✓ |
| S538 | .../v7.3/fs/btrfs/super.c | 200 (81,330 B) | `6715b89d60575dd4438710fab318c1a3f501f2df3b5c5c1d142ebc3c5eee43fc` | same | ✓ |
| C1 src | .../v7.2/Documentation/accounting/psi.rst | 200 (6,792 B) | `11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692` | same | ✓ |
| S543 | raw.githubusercontent.com/coreutils/coreutils/v9.12/doc/coreutils.texi | 200 (683,185 B) | `e6521c9b2e677dd278820887d7ad94fad8260f2535dd923728462cdcb6148db9` | same | ✓ |

The man-pages canonical route **is not challenged**: `https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man2/statfs.2?h=man-pages-6.19` → HTTP 200, real roff source, sha256 `3dc4ed703d7e2b5edee6765ea33152c89671b6cde5d3ea6f4236160700713b9d` = pinned `statfs.2.man-pages-6.19`. The challenge is scoped to the torvalds/linux cgit tree at this time.

Freeze integrity cross-check, run from lane root: `sha256sum -c <(grep sources-r55 .ufo/waves/round-55/evidence/freeze-sha256.txt)` → **24/24 OK**, zero failures.

### 3.3 Quote re-verification at cited line numbers (live mirror bodies)

- S537 `xfs_super.c:955` — live lines 955–956: `if (M_IGEO(mp)->maxicount)` / `st->f_files = min_t(typeof(st->f_files), st->f_files,`. Ledger quote at `SOURCES.md:317` is the two lines whitespace-joined; wording exact.
- S540 `tmpfs.rst:83` — live: `nr_inodes  The maximum number of inodes for this instance. The default` (source has two spaces after `nr_inodes`; ledger normalizes to one). Wording exact.
- S536 `statfs.c:62,67` — live: `memset(buf, 0, sizeof(*buf));` / `retval = security_sb_statfs(dentry);` (line 62) and `if (retval == 0 && buf->f_frsize == 0)` / `buf->f_frsize = buf->f_bsize;` (line 67). Ledger quotes join line pairs with `; ` — wording exact, same normalization pattern.
- S538 `btrfs_super.c:1771` — live: `/* Account global block reserve as used, it's in logical size already */` ✓. `:1792` — `delta to a 4M threshold.  (Practically observed delta was ~2M.)` (ledger collapses the double space) ✓. `:1797` — `succeed even if the Avail is zero. But this is better than the other` ✓. `:1803-1805` — three-line comment matching the ledger's joined form ✓.

### 3.4 Previously rejected route — rejection re-confirmed on the mirror

`.../v7.3/Documentation/ABI/testing/sysfs-fs-btrfs`:
- canonical git.kernel.org route: unconfirmable today (Anubis 200-challenge, §3.1);
- mirror: `HTTP 404`, body `404: Not Found` (14 bytes).

The path does not exist at tag v7.3; the round's rejection (`round-55.md:50` — "not admitted as a source; ... grounded in S538/S539") stands.

## 4. Failure records

- git.kernel.org torvalds/linux plain routes: FAIL (anti-bot challenge served as HTTP 200 HTML, ~7.7 KB). Recorded with body excerpt at §3.1.
- No other failures. Package and considerthese reopens succeeded; all mirror reopens and the man-pages canonical reopen returned pinned-identical bytes.

## Findings

- **MEDIUM — route health regression on canonical kernel routes** — as of 2026-10-27, `git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/*` serves an Anubis challenge page with HTTP 200 to non-browser agents. Evidence: scratch captures `xfs_super.c.live`, `tmpfs.rst.live`, `btrfs-abi.live` (challenge HTML, sha256 `4a0bd3dd…`, `ce99fe89…`, `c4913e86…` — none match any pinned source); §3.1 status table. Any future "reopen the cited URL" check that trusts status codes alone will silently pass on a challenge body. The lane's pinned copies remain byte-identical via the GitHub mirror (§3.2), so round-55 evidence is unaffected; the observation is about future freshness falsifiability.
- **LOW — quote whitespace normalization in ledger rows** — S536/S537/S538/S540 ledger quotes collapse runs of whitespace and join line pairs with `; ` or a single space (examples §3.3). Wording is exact in every case checked; pins are byte-exact. A stricter counter that byte-compared quotes to source lines would flag these rows; the current counters accept them.
- **INFO — package and considerthese state consistent with lane claims** — `shokuknow/merge/mori/` present and unchanged since 2026-10-24 23:33, nothing adopted in r55 (`round-55.md:74` confirmed by `git log ca52426e..HEAD` over `merge`-adjacent and `tools/` paths); considerthese latest `649e14cf` predates the round, zero r55 commits, four 2026-10-26 proposals remain outstanding and unacted.

Non-voter: this report emits no RECHECK / ENTAIL / REPLACE / QUOTE lines.
