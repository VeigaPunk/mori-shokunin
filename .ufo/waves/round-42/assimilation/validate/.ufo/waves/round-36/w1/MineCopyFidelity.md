measured 2026-10-23T12:05:25Z
# MineCopyFidelity — source-copy fidelity sweep (round 36, wave 1)

Seat: `MoriR36.MineCopyFidelity` (leaf; no subagents). Task: for S156–S160, S176, S177
(L1 live probe: do not sha-match live bytes) and S161, S184, S204 (tag-pinned, do match),
fetch each URL once, compare to the committed copy (sha256, size, contiguity, line numbers),
and check what the committing round claimed about the copy.

Scratch: `/fast/scratch/hyaku/mori-r36/MineCopyFidelity/` (fetch.sh sha256
`4873b7d38570265c9dfbfbef1a8e26c21ae2f943a48ff5357a43fb9901dc00c2`; live downloads
`live_S###`; inline comparison scripts run via `timeout 120 python3 -`). No tools installed.
Verification below is the only exercised check.

## Result table (live fetched 2026-10-23 ~11:54–12:02Z, one fetch per URL, all HTTP 200)

| row | committed file (sha256 first 16) | live sha256 (first 16) | gate/registry sha (first 16) | byte-status |
|---|---|---|---|---|
| S156 | sources-r30/S156.txt `4c02999410622d78` | `b56aa781…` | `b56aa781…` (round-30.md:114) | excerpt, faithful |
| S157 | sources-r30/S157.txt `bff6495cd91a9b8f` | `47e98d39…` | `47e98d39…` (round-30.md:116) | excerpt, faithful |
| S158 | sources-r30/S158.txt `9e375293fea6d643` | `428dc830…` | `428dc830…` (round-30.md:126) | excerpt, faithful |
| S159 | sources-r30/S159.txt `e6fe760c95ba3bb7` | `dc5a771c…` | `dc5a771c…` (round-30.md:135) | excerpt, faithful |
| S160 | sources-r30/S160.txt `d458d674a8e7bd4b` | `285b3d0c…` | `285b3d0c…` (round-30.md:138) | excerpt, faithful |
| S161 | sources-r31/S161.src `c2024c384dd88df2` | `c2024c38…` | `c2024c38…` (round-31.md:72) | **byte-exact** |
| S176 | sources-r32/S176.src `d3d261bcde4906ce` | `e6dddcc2…` | `d3d261bc…` (round-32.md:66) | byte-exact at commit; live footer-only drift |
| S177 | sources-r32/S177.src `650c53ac7695b816` | `8a531a2d…` | `650c53ac…` (round-32.md:67) | byte-exact at commit; live footer-only drift |
| S184 | sources-r33/S184.src `528501312dbd8da7` | `52850131…` | `52850131…` (round-33.md:19) | **byte-exact** |
| S204 | sources-r35/S204.src `b01ff2d6285efff1` | `b01ff2d6…` | `b01ff2d6…` (round-35.md:23) | **byte-exact** |

All three tag-pinned rows are byte-identical to the live tag bytes **and** to the sha the
committing round's Gate recorded. The L1 probe's "do not sha-match" is reproduced for the
other seven, with two distinct, fully explained causes:

## S156–S160 (systemd v262 / earlyoom commit patches): excerpts, not byte copies — and the round said so

- The committed files are delimited excerpts: each carries a 5-field header (`id`, `url`,
  `sha256` = the sha of the **full fetched document**, `accessed`, `lines` = span of line
  numbers covered) followed by tab-prefixed quoted lines (e.g. `sources-r30/S156.txt:1-6`).
- The header sha equals today's live sha for every one of the five (immutable v262 tags and
  commit patches), so the recorded digest is correct and current (see table).
- Body fidelity: for each of the five files, after dropping the header and the `N<TAB>`
  prefix, every body line was compared to the live file line at its stated number — 0 content
  mismatches across all five; line numbers are monotonic increasing; the excerpt is a true
  selection of real live lines, not transformed or fabricated text.
- S157 (17 lines), S158 (6), S160 (39) are contiguous live runs, so their stripped text is a
  contiguous substring of live bytes (checked `text in live`). S156 (73 selected lines over
  span 16–426) and S159 (27 over 6–36) are deliberately gap-selected per their SOURCES scope
  (e.g. SOURCES.md:162,165), so the stripped text is not a contiguous substring — expected for
  a multi-anchor excerpt, and every included line still matches live exactly.
- What round 30 claimed: LOG.md:1985 names "S156–S160, excerpts"; round-30.md:106-110 says
  admit quotes were "checked verbatim against the committed excerpt `…/sources-r30/S###.txt`"
  — i.e. the round's own contract is excerpt semantics, never byte-copy semantics. No Gate row,
  SOURCES row or README row claims the committed file equals the served document bytes.

## S176/S177 (docs.python.org): byte-exact snapshots at commit; live page rebuilt a timestamp

- Committed sizes and shas equal the round-32 Gate's recorded shas exactly: S176 55,620 B
  `d3d261bc…` (round-32.md:66), S177 20,100 B `650c53ac…` (round-32.md:67; matches
  SOURCES.md:183 "20 100 bytes"). The committed copies are exactly the bytes those Gates sha'd.
- Live pages today are the same size (55,620 / 20,100 B) and differ from the committed copies
  at exactly one byte run each: the footer `Last updated on Oct 23, 2026 (00:01 UTC).` →
  `… (09:57 UTC).` (first diff at byte 55,367 / 19,847; no other diff in 74,720 compared
  bytes). The pages are rebuilt several times a day; the committed snapshot is the 00:01 UTC
  build.
- The admitted quotes are present in the committed HTML (S176 lines 516–517 and 533–536,
  S177 entry sentence; markup/tag-normalization accounts for the Gate's rendered wording).
- Round 32 claimed only a live recheck of the passages (SKILL.md:796-806), not byte stability
  of a mutable-URL page; the drift is the page's own build cycle, not a wrong copy.

## Divergence from the L1 probe framing

The L1's probe read the S156–S160 headers' `sha256` as the hash the committed file itself
should carry; it is instead the hash of the full document fetched at `accessed` (matching the
Gate columns). The committed *files* therefore never match that hash — by design, and the
round's own language ("excerpts", "committed excerpt") says so. No lesson, Gate or SOURCES row
claims a byte copy that the committed file does not carry.

## Verdict

VERDICT: none
Sweep found no mistake row: all ten committed copies are faithful (seven excerpts whose every
line matches live tag bytes; three byte-exact copies; two byte-exact full-page snapshots whose
only drift is docs.python.org's build timestamp). No claimed sha is contradicted by the
committed bytes.
