# Round 28, wave 1 — SupersedeS097 (seat MoriR28.SupersedeS097)

Claim: C1 (freshness). Row S097 was edited in place after its first publication; the edit was never logged as a
correction row. This report gives the L1 the exact restore bytes, one ready-to-paste superseding row S146, the Gate
line, the QUALITY 77 sweep list, and the falsifications run on a sandbox copy. The lane was not written; the only
lane write is this file. Scratch: `/fast/scratch/hyaku/mori-r28/MoriR28.SupersedeS097/`.

## 0. Result in one paragraph

S097 was first published at `df4db54a341f396271ea39be9e3db47ac794eb73` and changed in place at `7c77fba32937671101780ebc22a89c34a30ecee3`
("round-24: wave-2 source corrections (S093 anchor, S096 teaches, S097 cells)"); two immutable cells differ, `anchor`
and `teaches`. The rejection still holds — the URL is still HTTP 404 with the same 196-byte body and SHA-256 — but the
old row's digest width, its wrong row id for the `psi.rst` line numbers, its missing `flip:` clause (a rejected row
must carry one, `CORPUS.md:102`) and its unswept negative claims are wrong. The corrected wording goes into a new row
S146 whose `teaches` opens `supersedes S097 — `; both lines were falsified on a sandbox clone (row-identity check
drops S097, `changed=3` → `changed=2`; census exit 0; the counter's own logic counts S097).

## 1. First-published row and the row at the tip

First publication (the command the assignment gives, run read-only in the lane):

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --reverse --format=%H -S'| S097 |' -- corpus/SOURCES.md | head -1
df4db54a341f396271ea39be9e3db47ac794eb73
```

`df4db54` is "round-24: sources S090-S097, system pressure knowledge entry, lesson, evidence" (2026-10-22 05:45:30
-0300). The pickaxe lists only that commit because the in-place edit kept `| S097 |` once per row; the edit commit was
found with `git log --format=%H -L 103,103:corpus/SOURCES.md`, which prints `7c77fba` first.

First-published row (`git show df4db54:corpus/SOURCES.md`, line 103):

```
| S097 | proc_pressure(5) candidate manual page — https://man7.org/linux/man-pages/man5/proc_pressure.5.html | docs | C | candidate manual page for the /proc/pressure file format — no such page exists in the man-pages project (current release 6.20, 2026-10-21) | HTTP 404 Not Found fetched 2026-10-22T08:21:47Z; body 196 bytes, sha256 80c3fe2ae1062abf5; man-pages 6.20 contains no man5/proc_pressure page and no page mentioning /proc/pressure; proc(5) on man7 mentions no pressure file | REJECTED: the assigned manual page does not exist, so it supports no claim about the /proc/pressure line grammar or the system-wide CPU full line; flip: the same scope is documented by the kernel PSI documentation (S001; kernel v7.2 Documentation/accounting/psi.rst lines 42-43 and 57-58), where CPU full is undefined at the system level. | rejected | 2026-10-22 | on-release | corpus/lessons/round-24.md |
```

Row at the entering tip `6ebd518f` (`git show 6ebd518f:corpus/SOURCES.md`, line 103):

```
| S097 | proc_pressure(5) candidate manual page — https://man7.org/linux/man-pages/man5/proc_pressure.5.html | docs | C | candidate manual page for the /proc/pressure file format — no such page exists in the man-pages project (current release 6.20, 2026-10-21) | HTTP 404 Not Found fetched 2026-10-22T08:21:47Z; body 196 bytes, sha256 80c3fe2ae1062abf; man-pages 6.20 contains no man5/proc_pressure page and no page mentioning /proc/pressure; proc(5) on man7 mentions no pressure file | REJECTED: the assigned manual page does not exist, so it supports no claim about the /proc/pressure line grammar or the system-wide CPU full line; flip: the man-pages project publishes a proc_pressure page; until then the same scope is documented by the kernel PSI documentation (S090, kernel v7.2 Documentation/accounting/psi.rst lines 42-43 and 57-58; S001 is the rendered page), where CPU full is undefined at the system level. | rejected | 2026-10-22 | on-release | corpus/knowledge/system-pressure-r24.md, corpus/lessons/round-24.md |
```

Cells that differ (column-wise diff of the two rows; the immutable ones are the ones QUALITY 81 checks):

| cell | first published (`df4db54`) | at `6ebd518f` | mutable? |
|---|---|---|---|
| `anchor` | `… sha256 80c3fe2ae1062abf5;` (17 hex digits) | `… sha256 80c3fe2ae1062abf;` (12 hex digits) | **no** — differs |
| `teaches` | `… flip: the same scope is documented by the kernel PSI documentation (S001; kernel v7.2 …)` | `… flip: the man-pages project publishes a proc_pressure page; until then the same scope is documented by the kernel PSI documentation (S090, kernel v7.2 …; S001 is the rendered page) …` | **no** — differs |
| `used-by` | `corpus/lessons/round-24.md` | `corpus/knowledge/system-pressure-r24.md, corpus/lessons/round-24.md` | yes (`status`, `recheck`, `used-by` only, `CORPUS.md:116-118`) — allowed in place |
| id, source, kind, tier, scope, status, opened, recheck | identical | identical | — |

So the row-identity check prints `changed S097 cells=anchor,teaches`, which is what the round-27 lesson records at
`corpus/lessons/round-27.md:35`.

## 2. The source re-opened today, and every claim checked against the bytes

All fetches: ordinary `curl` GET, no redirect tricks, no challenge. Access times are UTC (`date -u +%FT%TZ`).

| URL | accessed | result | SHA-256 of the bytes fetched |
|---|---|---|---|
| https://man7.org/linux/man-pages/man5/proc_pressure.5.html | 2026-10-22T17:59:40Z | HTTP 404, 196 bytes | `80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880` |
| https://www.kernel.org/pub/linux/docs/man-pages/ | 2026-10-22T18:00:50Z | HTTP 200, 10625 bytes | (listing; newest entry `man-pages-6.20.tar.xz`, 21-Oct-2026 13:08; before it 6.19, 6.18, 6.17; no 6.21) | — |
| https://www.kernel.org/pub/linux/docs/man-pages/man-pages-6.20.tar.xz | 2026-10-22T18:00:50Z | HTTP 200, 1914692 bytes | `180f0d16a2142dd9671760ac0afeadcc25e861f695eb420293e1206a87ca083f` (equals the digest line at `sha256sums.asc:61`) |
| https://man7.org/linux/man-pages/dir_section_5.html | 2026-10-22T18:00:58Z | HTTP 200, 39543 bytes | `1caa9e6d9b3700e20292bcee6a41b9f393af21d617af012ee06de96896fc1e74` |
| https://man7.org/linux/man-pages/man5/proc.5.html | 2026-10-22T18:00:58Z | HTTP 200, 31125 bytes | `b197c5fa64577269f992d50f60acfd5e0cc3df756644ddd8bd19a02591272a97` |
| https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst | 2026-10-22T18:00:07Z | HTTP 200, 6792 bytes | `11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692` |
| https://api.github.com/repos/mkerrisk/man-pages/git/trees/master?recursive=1 | 2026-10-22T18:00:07Z | HTTP 200, 712500 bytes | 2519 paths, `truncated: false`, no path contains `pressure` |

Statement-by-statement check of what the corrected row says:

1. "the assigned page returns HTTP 404" — holds. The body is 196 bytes, digest as above. Body lines, verbatim:
   line 3 `<title>404 Not Found</title>`, line 5 `<h1>Not Found</h1>`, line 6
   `<p>The requested URL was not found on this server.</p>`. The row's quote is on line 6 (9 words).
2. "the digest of those bytes" — holds: the first 16 hex of the true digest are `80c3fe2ae1062abf`; the
   first-published cell's `80c3fe2ae1062abf5` is 17 hex (one past the lane's own convention of 16, `corpus/lessons/round-24.md:21`)
   and the tip's `80c3fe2ae1062abf` is 12. Both are prefixes of the same digest, so no cell states a false digest;
   both are off-convention.
3. "man-pages 6.20 holds no proc_pressure page and no page mentioning /proc/pressure" — holds. In the extracted
   6.20 tree: `man/man5` has 180 files and none of their names contains `pressure` (`find -iname '*pressure*'` → no
   hit); `grep -ril 'proc/pressure'` over `man/` → no hit; the word `pressure` appears in `man/man5` only in
   `proc_meminfo.5` and `tmpfs.5` (both about memory pressure).
4. "6.20 is the current release" — holds. The kernel.org listing's newest entry is `man-pages-6.20.tar.xz`, dated
   21-Oct-2026 13:08, and there is no 6.21, so the scope cell's "(current release 6.20, 2026-10-21)" still stands.
5. "the upstream man-pages tree holds no pressure page" — holds. The recursive tree has 2519 paths, none containing
   `pressure`; the `man5/` contents listing (HTTP 200) has 42 entries, none `proc_pressure`.
6. "man7's section-5 index holds no pressure entry, and proc(5) mentions no pressure file" — both hold: zero
   case-insensitive `pressure` matches in either page. Note the index path: only the root path
   `https://man7.org/linux/man-pages/dir_section_5.html` serves it; `…/man5/dir_section_5.html` returns HTTP 404 today
   with the same 196-byte body, so `corpus/lessons/round-24-verifier-spotcheck.md:122`'s bare `dir_section_5.html`
   is citable only at the root path (a LOW finding).
7. "the flip target is the kernel documentation, and the psi.rst lines are 42-43 and 57-58" — holds.
   `psi.rst` line 42 `some avg10=0.00 avg60=0.00 avg300=0.00 total=0`, line 43
   `full avg10=0.00 avg60=0.00 avg300=0.00 total=0`, lines 57-58 `CPU full is undefined at the system level, but has
   been reported` / `since 5.13, so it is set to zero for backward compatibility.` The digest matches the one the
   round-24 Gate recorded for S090 (`corpus/lessons/round-24.md:25`).
8. "those line numbers belong to S090, not S001" — holds. S090 is the tag-pinned raw `psi.rst`
   (`corpus/SOURCES.md:96`); S001 is the rendered HTML page with different anchors (`corpus/SOURCES.md:7`), as the
   round-24 wave-2 seat already found (`.ufo/waves/round-24/w2/ReopenS094S097.md:117-122`, its F5).

Not verified today (gaps, not passes): the old anchor's fetch timestamps (`2026-10-22T08:21:47Z` in the row, `08:21:46Z`
in the Gate at `corpus/lessons/round-24.md:32`) cannot be re-observed; the man-pages `.sign` was not PGP-verified.

## 3. Ready-to-paste lines

(a) **Restore S097 in place.** Replace `corpus/SOURCES.md:103` with this line, byte-identical to `df4db54`'s line
(898 bytes plus newline; `cmp` in scratch confirmed byte equality):

```text
| S097 | proc_pressure(5) candidate manual page — https://man7.org/linux/man-pages/man5/proc_pressure.5.html | docs | C | candidate manual page for the /proc/pressure file format — no such page exists in the man-pages project (current release 6.20, 2026-10-21) | HTTP 404 Not Found fetched 2026-10-22T08:21:47Z; body 196 bytes, sha256 80c3fe2ae1062abf5; man-pages 6.20 contains no man5/proc_pressure page and no page mentioning /proc/pressure; proc(5) on man7 mentions no pressure file | REJECTED: the assigned manual page does not exist, so it supports no claim about the /proc/pressure line grammar or the system-wide CPU full line; flip: the same scope is documented by the kernel PSI documentation (S001; kernel v7.2 Documentation/accounting/psi.rst lines 42-43 and 57-58), where CPU full is undefined at the system level. | rejected | 2026-10-22 | on-release | corpus/lessons/round-24.md |
```

Note for the L1: `used-by` is mutable, so it may be widened to `corpus/knowledge/system-pressure-r24.md,
corpus/lessons/round-24.md, PROVINCE.md` (the round-24 wave-2 seat's F2, `.ufo/waves/round-24/w2/ReopenS094S097.md:103-110`);
that change must be logged old→new in the round-28 lesson. Observed at 18:05Z, not by this seat: the lane working tree
already carries an S097 restore whose immutable cells (id…teaches) are byte-equal to `df4db54`, with the widened
`used-by` kept; that variant also satisfies the check, and no S146 row exists in the working tree yet.

(b) **New row S146.** Insert after `corpus/SOURCES.md:150` (the S144 row, the last row of the `## Registry` table,
before the blank line and `## Paths`). Id 146 is free: the highest id at the entering tip is S144
(`corpus/SOURCES.md:150`), and the round-28 counter requires a superseding id above 144
(`.ufo/waves/round-28/count-c1.sh`, `MAX_OLD=144`).

```text
| S146 | man-pages 6.20 release tarball — https://www.kernel.org/pub/linux/docs/man-pages/man-pages-6.20.tar.xz | docs | A | the man-pages project's published man5 page set at release 6.20: no proc_pressure(5) page and no page mentioning /proc/pressure | man-pages 6.20 tarball https://www.kernel.org/pub/linux/docs/man-pages/man-pages-6.20.tar.xz sha256 180f0d16a2142dd9671760ac0afeadcc25e861f695eb420293e1206a87ca083f (kernel.org listing 21-Oct-2026 13:08, the newest; sha256sums.asc line 61): man/man5 holds no proc_pressure page and no file name containing "pressure"; grep -ril 'proc/pressure' over man/ returns nothing; man7 dir_section_5.html sha256 1caa9e6d9b3700e2 holds no "pressure" entry; man7 proc.5.html sha256 b197c5fa64577269f992d50f60acfd5e0cc3df756644ddd8bd19a02591272a97 mentions no pressure file; upstream man-pages master tree (GitHub API, 2519 paths, untruncated) holds no path containing "pressure"; the man7 candidate page https://man7.org/linux/man-pages/man5/proc_pressure.5.html returns HTTP 404, 196 bytes, sha256 80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880 (body line 6 "The requested URL was not found on this server.") | supersedes S097 — S097's anchor carried a 17-hex digest (80c3fe2ae1062abf5), one character past the lane's 16-hex convention, and its negative claims about the man-pages tree and man7 carried no URL or digest of their own; its flip cited S001 for the psi.rst lines 42-43 and 57-58, which belong to S090; and as a rejected row it stated no flip at all. Re-opened 2026-10-22: man-pages 6.20 and the upstream master tree publish no proc_pressure page and man7 proc(5) mentions no pressure file, so the rejection stands; flip: the man-pages project publishes a proc_pressure page; until then the /proc/pressure line grammar and the system-level CPU full rule are documented by the kernel documentation (S090, kernel v7.2 Documentation/accounting/psi.rst lines 42-43 and 57-58, sha256 11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692; S001 is the rendered page), where CPU full is undefined at the system level and is set to zero for backward compatibility since 5.13. | mined | 2026-10-22 | on-release | corpus/knowledge/system-pressure-r24.md, corpus/lessons/round-24.md, corpus/lessons/round-24-verifier-spotcheck.md, corpus/lessons/round-27.md, corpus/lessons/round-27-verifier-spotcheck.md, PROVINCE.md |
```

Cell notes: `teaches` opens exactly `supersedes S097 — ` (em dash), `status` is `mined`, `opened` is `2026-10-22`,
`recheck` is `on-release` (S097's convention), `used-by` is the set of files citing S097 today (§5); no cell holds a
`|`, the row splits into 13 fields (checked).

Alternative row, if the L1 prefers the house pattern of keeping the superseded row's own URL (as S142 did for S090):
the same row with `source` = `proc_pressure(5) candidate manual page — https://man7.org/linux/man-pages/man5/proc_pressure.5.html`,
`scope` = the S097 scope text and `tier` = `C`, the rest unchanged. Measured too (§6): census exit 0 but one new
`W01` line (a tier-C row that is `mined` and cited is the census's "lead mined and cited" smell); the recommended row
avoids it, the man-pages release tarball being primary for its scope.

## 4. Gate line (round-28 lesson `## Gate`)

| Row | URL | Accessed | Located quote (verbatim, ≤25 words) | Decision |
|---|---|---|---|---|
| S146 | https://www.kernel.org/pub/linux/docs/man-pages/man-pages-6.20.tar.xz (with https://man7.org/linux/man-pages/man5/proc_pressure.5.html, https://man7.org/linux/man-pages/dir_section_5.html, https://man7.org/linux/man-pages/man5/proc.5.html) | 2026-10-22T18:00:50Z | 404 body line 6 (man7 candidate page): "The requested URL was not found on this server." (9 words) | admit, A, mined |
| S146 (supporting) | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst | 2026-10-22T18:00:07Z | `:57-58` "CPU full is undefined at the system level, but has been reported since 5.13, so it is set to zero for backward compatibility." (23 words) | admit, A, mined (the format authority the flip points at) |

## 5. QUALITY 77 sweep: every place in the lane whose prose states the defective wording

Line numbers are at the entering tip `6ebd518f`. "Live surface" = a file that states the fact and that the round-28
sweep should update; "record" = a closed round's lesson or spot-check that states the defect or the fact as history.
The lane's S090 precedent left the closed round-24 lesson alone and logged old→new in the new round's lesson
(`.ufo/waves/round-27/w2/SupersedeS090.md:104-106`); I recommend the same, and flag the one line QUALITY 77 read
literally would still need answered by a dated correction.

Live surfaces to correct:

1. `corpus/SOURCES.md:103` — the row itself: anchor digest 12 hex, teaches naming S090 and the flip. Replaced by (a)
   plus (b).
2. `corpus/SOURCES.md:195` — round-24 registry summary: "S097 rejected (HTTP 404, no such page in man-pages 6.20)."
   States the fact with no row id for the corrected wording; should name S146.
3. `corpus/knowledge/system-pressure-r24.md:1` — provenance header: "Rejected candidate: S097 (proc_pressure(5) does
   not exist; HTTP 404)." Should carry the corrected wording and S146.
4. `corpus/knowledge/system-pressure-r24.md:224` — U6: "No `proc_pressure(5)` page exists (S097, rejected: HTTP 404;
   man-pages 6.20 has no such page). The kernel documentation (S090) is the format authority." This is the sentence
   the lane's users read; it should cite S146 and keep the flip.
5. `PROVINCE.md:258` — "`proc_pressure(5)` does not exist (S097, rejected)." Should name S146.

Records (keep as history; log the correction in the round-28 lesson):

6. `corpus/lessons/round-24.md:32` — Gate row with the 12-hex digest `80c3fe2ae1062abf` and the 404 quote.
7. `corpus/lessons/round-24.md:38-39` — registry-change prose: "(used-by widened, digest cell trimmed to 16 hex and
   flip pointed at S090 after wave-2 ReopenS094S097)". **This statement is false against the bytes**: the digest was
   trimmed from 17 hex to 12 hex, not to 16. QUALITY 77 read literally requires this contradicted line to be
   answered; the lane's W1 precedent (`.ufo/waves/round-28/contract.md`, "Correction to round-27 amendment W1") is to
   append a dated correction in the round-28 lesson, never to rewrite the closed round's lesson. Recommend that.
8. `corpus/lessons/round-24.md:40-43` — the S096 bullet that carries the flip ("Flip: the man-pages project
   publishes a `proc_pressure` page."); the flip belongs to S097's own row.
9. `corpus/lessons/round-24.md:62` — M3 row naming the "rejection row S097"; `:89` — "Contract A5's 'S097 is cited
   by nothing' is wrong …".
10. `corpus/lessons/round-24-verifier-spotcheck.md:122` — spot-check row for S097 (12-hex digest, "(= Gate)"), and
    its `dir_section_5.html` mention, which today is citable only at the root path (see §2 item 6).
11. `corpus/lessons/round-27.md:35` — M2 names "S097 (anchor, teaches)".
12. `corpus/lessons/round-27.md:128` — routed-disposition list: "S096, S097, S101 restores".
13. `corpus/lessons/round-27-verifier-spotcheck.md:133` — "in-place edits of S096, S097, S101 (disclosed, not hidden)".
14. `corpus/lessons/round-27-verifier-spotcheck.md:148-149` — routed defect 3: "S096, S097, S101 still differ from
    their first-published cells".

`SKILL.md` names S097 nowhere (`git grep -n 'S097' 6ebd518f -- SKILL.md` → no hit), so no SKILL sweep is owed.

Observed at 18:05Z, not by this seat: the lane working tree already carries the S097 restore (immutable cells
byte-equal to `df4db54`), and the integrator's in-flight sweep already writes "`proc_pressure(5)` does not exist
(S146, rejected)" at `PROVINCE.md:258`, so S146 is the id the sweep expects. No S145/S146 row exists yet in the
working tree's `corpus/SOURCES.md`; row (b) below is what that file still needs.

Files that cite S097 today (the `used-by` list of the draft row; `git -C <lane> grep -n 'S097' 6ebd518f -- corpus
SKILL.md PROVINCE.md`): `corpus/SOURCES.md:103,195`, `corpus/knowledge/system-pressure-r24.md:1,224`,
`corpus/lessons/round-24.md:32,38,39,40,62,89`, `corpus/lessons/round-24-verifier-spotcheck.md:122`,
`corpus/lessons/round-27.md:35,128`, `corpus/lessons/round-27-verifier-spotcheck.md:133,148`, `PROVINCE.md:258`. (The
`round-24.md:40` and `:89` hits are the string `ReopenS094S097`, not the row id.) The round-28 lesson will cite S097
and S146 once more, so the L1 may add `corpus/lessons/round-28.md` to the used-by cell when it exists.

## 6. Falsifications run (sandbox clone, lane untouched)

Sandbox: `git clone --no-hardlinks` of the lane into `/fast/scratch/hyaku/mori-r28/MoriR28.SupersedeS097/sandbox` (and
`sandboxB` for the alternative row), checked out at `6ebd518f`; the two lines were applied and committed there.

1. Row-identity check (QUALITY 81), `LANE` repointed at the sandbox: at the tip it prints `changed S096 cells=teaches`,
   `changed S097 cells=anchor,teaches`, `changed S101 cells=teaches`, `rows=144 changed=3 removed=0 bad=0`, exit 1;
   with (a) and (b) applied it prints `rows=145 changed=2 removed=0 bad=0` — S097 is gone, the two rows left (S096,
   S101) belong to other seats.
2. Census `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root <scratch> mori` on the
   unmodified tip: exit 0, six `W04` lines (S035, S037, S073, S074, S075, S076), `mori ok`. With the recommended row
   (b, tier A): exit 0, the same six `W04` lines and no new finding. With the alternative tier-C row: exit 0 plus one
   new line `W01 S146 tierC mined used-by=…`.
3. Round-28 counter detection logic (the python block inside `.ufo/waves/round-28/count-c1.sh`, run against the
   sandbox's `corpus/SOURCES.md` with the owed list `S096 S097 S101 S127 S128 S129 S131 S140` and `MAX_OLD=144`):
   prints `1 S097` — the new row is counted as a superseding row for S097; the other seven ids belong to other
   seats, so C1 stays `unmet` until they land. `cmp` in scratch: the pasted restore line is byte-identical to
   `git show df4db54:corpus/SOURCES.md` line 103.

## 7. Findings for the L1

- **MEDIUM — the old row violates the rejected-row format.** `CORPUS.md:102` requires a rejected row's `teaches` to
  read `REJECTED: <reason>; flip: <what would change the verdict>`. The first-published S097 teaches has no `flip:`
  clause at all; the in-place edit at `7c77fba` added one — a needed correction made in the wrong place (Rule 2,
  `CORPUS.md:116-118`). S146 carries the flip; the restored row keeps the historical text (S090/S142 precedent).
- **LOW — the digest width is off-convention in both texts.** 17 hex at first publication (the lane convention is 16,
  `corpus/lessons/round-24.md:21`), 12 hex at the tip; S146's anchor carries the full 64-hex digest plus "first 16 hex".
- **LOW — the negative claims had no sweep.** "man-pages 6.20 contains no man5/proc_pressure page and no page
  mentioning /proc/pressure; proc(5) on man7 mentions no pressure file" asserted three negatives with no registered
  URL or digest (`CORPUS.md:39-40` requires a negative claim to carry its sweep; the round-24 wave-2 seat's F3,
  `.ufo/waves/round-24/w2/ReopenS094S097.md:107-113`). S146's anchor registers each with a digest.
- **LOW — the round-24 lesson misstates its own change.** `corpus/lessons/round-24.md:39` says the digest cell was
  "trimmed to 16 hex"; the bytes show 17 → 12. Answer with a dated correction in the round-28 lesson (§5 item 7).
- **NOTE — a mined tier-C row trips the census.** The contract fixes `status` as `mined`, and the census warns on a
  tier-C row that is mined and cited (`W01`); the recommended row is tier A over the man-pages release tarball, which
  is primary for its scope and keeps the census output unchanged. The round-24 wave-2 seat's report
  (`.ufo/waves/round-24/w2/ReopenS094S097.md`, F2–F5) is the record of the in-place edit; the round-28 lesson can
  cite it instead of re-deriving those findings.

## 8. Bounds, tools, installs

- Lane writes: this file only. No `git add/commit/stash/checkout/switch/reset/pull/push` in the lane; only read-only
  `git log/show/grep/clone`; no jj command ran. No unit started, stopped or signalled; no harness settings or MCP file
  read or written; no OMP settings value, session id or session-store path appears in this report.
- Fetches: ordinary `curl` GET only, no challenge, no bot bypass; counts, states, versions and digests only. Tools
  used: `curl`, `sha256sum`, `tar`/`xz`, `python3` (`-I -B`), read-only `git`, `grep`/`find` on scratch copies.
  Installed or upgraded: **nothing**; no pacman, uv, npm or cargo operation ran (host pacman transactions are paused
  by the operator's standing rule).
- Privacy: no uid, pid, `user-<digits>.slice`, `user@<digits>.service`, user-session unit name, journal MESSAGE text
  or `/etc/default/earlyoom` value is quoted; no fixture was written; nothing installed.
