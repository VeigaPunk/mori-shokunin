# ReopenS146 — round 28, wave 2 (attempt 1)

partial — S146 (supersedes S097) re-opens clean: the restore is byte-exact, every re-fetched digest matches, all readers
moved to S146, and the counter counts it; but the teaches cell contains one verbatim-false historical claim, and a
recommended dated correction for a false round-24 lesson line never landed.

Seat: MoriR28.ReopenS146 (leaf; no subagents; detection and report only). Lane: /home/vgpnk/Projects/shokunin/mori-shokunin.
Attack rev: `f2de0eedcd60d2e354da75265ea6122bc3896073` (all `git show` below at that rev). Scratch:
`/fast/scratch/hyaku/mori-r28-w2/ReopenS146/`. Fetches by plain `curl` between 18:55:08Z and 18:56:27Z.

## Fetches and digest check (re-opened now)

| URL | fetched | bytes | sha256 vs row/Gate |
|---|---|---|---|
| https://www.kernel.org/pub/linux/docs/man-pages/man-pages-6.20.tar.xz | 18:55:08Z, HTTP 200 | 1,914,692 | `180f0d16a2142dd9671760ac0afeadcc25e861f695eb420293e1206a87ca083f` — EQUALS Gate and anchor |
| …/man5/proc_pressure.5.html | HTTP 404 | 196 | `80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880` — equals anchor |
| …/dir_section_5.html | HTTP 200 | 39,543 | `1caa9e6d9b3700e20292bcee6a41b9f393af21d617af012ee06de96896fc1e74` — equals anchor |
| …/man5/proc.5.html | HTTP 200 | 31,125 | `b197c5fa64577269f992d50f60acfd5e0cc3df756644ddd8bd19a02591272a97` — equals anchor |
| kernel.org listing | HTTP 200 | 10,625 | `man-pages-6.20.tar.xz` at :95 dated 21-Oct-2026 13:08; newest `.tar.xz` is 6.20; no 6.21 (grep 0 hits) |
| sha256sums.asc | HTTP 200 | 5,988 | line 61 carries the same 64-hex digest for `man-pages-6.20.tar.xz` |
| psi.rst (raw.githubusercontent v7.2) | HTTP 429 twice (18:55:25Z, 18:55:53Z), 199-byte "429: Too Many Requests" body | — | NOT verified at that host; see below |
| psi.rst (git.kernel.org plain ?h=v7.2) | HTTP 200 | 6,792 | `11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692` — equals anchor digest; lines 42-43 `some/full avg10=0.00…`, 57-58 "CPU full is undefined at the system level, but has been reported / since 5.13, so it is set to zero for backward compatibility." Same upstream bytes, different mirror [INFERENCE: content identical, digest equal] |
| api.github.com mkerrisk/man-pages master tree | HTTP 200 | 712,500 | `"truncated": false`; 2,519 paths; zero paths contain "pressure" |

Tarball contents (extracted to scratch): 180 `man/man5` files, zero filenames containing "pressure" (tar listing grep -c → 0); `grep -ril 'proc/pressure'` over the tree → no hit. `grep -ci pressure` on dir_section_5.html → 0; on proc.5.html → 0.

## Gate line (corpus/lessons/round-28.md:66)

Present at :66. sha256 cell `180f0d16…083f` equals my tarball fetch exactly. Quote cell cites the *companion* URL, not
the tarball — verbatim at my fetch: `proc_pressure.5.html` body line 6 reads
`<p>The requested URL was not found on this server.</p>` (9 words). Contract A1 (contract.md:90) requires "an https
URL, a 64-hex sha256 and a quoted span" — the digest is of the first-named URL and the span is honestly labelled
"man7 candidate page". Honest, but the quote does not come from the digested artifact (Low; see F3).

## Cell-by-cell verdict on S146 (corpus/SOURCES.md:152)

| cell | verdict |
|---|---|
| id/source/kind/tier | PASS — S146; man-pages 6.20 tarball URL, docs, A |
| scope | PASS — "no proc_pressure(5) page and no page mentioning /proc/pressure" re-verified against my extracted tree |
| anchor | PASS — every digest, byte count and negative claim reproduced above (see fetch table) |
| teaches | PARTIAL — opens `supersedes S097 — `; flip now cites S090 (correct: psi.rst :42-43,57-58, digest matches S090's) with a real verdict-changing condition. BUT it states "as a rejected row it stated no flip at all" — verbatim false (F1) |
| status/opened/recheck | PASS — mined / 2026-10-22 / on-release; counted by `count-c1.sh` (`superseding=7/8 ids=…S097…`, `readers_left=0`, at attack rev; only `fail S147 row_absent` — another seat's row) |
| used-by | PASS — `corpus/knowledge/system-pressure-r24.md, PROVINCE.md, corpus/lessons/round-28.md`; all three cite S146 as a word (knowledge :1, :224; PROVINCE :258; lesson :66) |

## Defect named by round-27/wave-1 — fixed, not copied?

Round-27 lesson `round-27.md:35` (M2) names S097's in-place `anchor`+`teaches` edits; wave-1 `w1/SupersedeS097.md`
names: (a) restore S097 to first-published bytes; (b) corrected wording in a new superseding row; (c) reader sweep.

- (a) PASS — column-wise diff of `df4db54a…:SOURCES.md` S097 fields 2–8 (id..teaches) vs the attack-rev row: byte-identical. Restored row carries the first-published 17-hex digest and the S001-flip — i.e., the historical defect is back in the immutable cells, per the freeze rule, and the correction lives on S146.
- (b) PASS with F1 — S146 registers every negative claim with URL+digest, fixes the flip target S001→S090 (psi.rst lines belong to S090, confirmed; S001 is the rendered page), and adds a verdict-changing condition. None of it is copied wording: teaches text differs from S097's (counter requirement met).
- (c) PASS — live readers swept (below).

## Reader sweep (QUALITY 77; A1 scope: SKILL.md, PROVINCE.md, corpus/README.md, corpus/knowledge/)

`git grep 'S097\|proc_pressure' <rev> -- SKILL.md corpus/README.md corpus/knowledge/ PROVINCE.md`: zero S097 hits;
S146 cited at `PROVINCE.md:258`, `system-pressure-r24.md:1,224`. SKILL.md and corpus/README.md: no mention at all.
The defective wording (S097's flip citing S001 for psi.rst lines) survives in no live reader — U6 at
`system-pressure-r24.md:224` correctly names S090 as the format authority. `counter readers_left=0` agrees.
Residual: `corpus/SOURCES.md:202` (round-24 bounded-search summary) still says "S097 rejected (HTTP 404…)" — a
historical summary inside the registry, outside A1's live-reader list; wave-1 (§5 item 2) suggested naming S146.
Not defective wording; note only.

## Findings

**F1 — Medium — S146 teaches asserts a verbatim-false history.** `SOURCES.md:152` teaches: "its flip cited S001 for
the psi.rst lines 42-43 and 57-58 … **and as a rejected row it stated no flip at all**." The row's own first-published
bytes (`git show df4db54:corpus/SOURCES.md:103`) contain `flip: the same scope is documented by the kernel PSI
documentation (S001; …)`, and S146's own preceding clause says "its flip cited S001" — the cell contradicts itself.
The claim is also false about *which* row lacked a proper flip: the first-published flip was textually present but
named no verdict-changing condition (round-24 F5), while it was the *edited* flip that gained one. The wave-1 report
makes the same error (`SupersedeS097.md` §7 MEDIUM: "The first-published S097 teaches has no `flip:` clause at all;
the in-place edit at `7c77fba` added one") while its own §1 diff table shows both texts carrying `flip:`. Frozen into
an immutable teaches cell, the clause needs a future correction row to fix.

**F2 — Low — recommended dated correction never landed.** Wave-1 §5 item 7 and §7 LOW asked for a dated correction
in the round-28 lesson answering `corpus/lessons/round-24.md:39`'s false "trimmed to 16 hex" (bytes: 17→12). The
round-28 lesson carries no such line (grep `round-24\|17 hex\|16 hex` → only :10). Closed-round lesson is history, so
QUALITY 77/A1 do not require it; the recommendation was dropped silently.

**F3 — Low — Gate quote cell quotes a different URL than the digested one.** Lesson :66 digests the tarball but
quotes the man7 404 body. Labelled honestly ("(man7 candidate page)") and the contract text is satisfied; a Gate
reader must open the second URL to see the quoted bytes. Cosmetic.

**F4 — Low — S097 used-by left stale.** Restored S097's `used-by` keeps
`corpus/knowledge/system-pressure-r24.md` which no longer cites S097, and omits `corpus/lessons/round-28.md` which
does. Mutable cell; bookkeeping drift only. The wave-1 report itself sanctioned widening this way at 18:05Z.

## Verification gaps

- psi.rst re-fetch on raw.githubusercontent.com blocked by HTTP 429; digest and lines verified on the
  git.kernel.org `?h=v7.2` mirror (same tag, equal digest).
- `sha256sums.asc`/`.sign` not PGP-verified; digest cross-checked only against the `.asc` listing file.
- The original 08:21:47Z fetch timestamp in S097's anchor is historical and cannot be re-observed.

## Bounds / tools

Lane writes: this file only. Read-only git (`show`, `grep`, `diff` on pipes); no add/commit/checkout/reset/jj; no
units, signals, harness files, or OMP settings touched; no uid/pid/service/journal/earlyoom values in this report.
Sources fetched by `curl` only, UTC access times recorded above. Installs: none (pacman paused host-wide); tools used:
curl, sha256sum, tar/xz, python3, grep/find on scratch only.
