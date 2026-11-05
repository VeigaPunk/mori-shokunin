# Mo91E04Digest — candidate digest-check.py (round 91 w1)

Seat: `Mo91E04Digest`. Lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin`,
frozen registry `corpus/SOURCES.md` at rev `79eaa8cfe5e0b9b1c5ff45f524199d4a123f0520`
(sha256 `9a657f7e72d4496af2148297ef13485dc25bdf126f1eab0faf667804c5ca056f`,
482 lines, byte-identical at lane HEAD `e02b8a39` — `git diff` empty).

## Deliverable

`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-91/w1/candidates/digest-check.py`
sha256 `a692b159646e8979f9fc95d5eee82a9a30cee4d8f67432ee824fff7e9d30cee7`, 440 lines,
stdlib only (`hashlib`, `os`, `re`, `sys`). Executable bit set.

CLI: `python3 digest-check.py <SOURCES.md> <pinned-dir>`.
Per in-scope row: `DIGEST <id> ok|mismatch|prefix-only|unpinned recorded=<v> actual=<sha256>`.
Trailer: `DIGEST_CHECK rows=<n> ok=<a> mismatch=<b> prefix_only=<c> unpinned=<d>`.
Exit 0 iff mismatch=prefix_only=unpinned=0; 1 otherwise; 2 on setup error.

## What it checks

A row is in scope when its anchor+source cells BOTH name a pinned copy AND record
a usable sha256. Copy references: repo-relative paths under `corpus/evidence/`
or `.ufo/waves/` (pinned-copy locations), any `corpus/`/`.ufo/` path in a
copy/receipt/extract/pinned-copy clause, directory paths (expanded to files),
"same (page )bytes as S<n>" (inherits target row's copies), and "the pinned
copy"/"pinned copy" with no path (resolved by recursive search of `<pinned-dir>`,
disambiguated by recorded byte count then longest digest-prefix match).
Digests: `sha256`-labelled hex of 8–64 chars or bare 64-hex; digests attributed
in-clause to non-copy artifacts ("script SHA-256", "git blob", "entry bytes",
"tarball") are ignored. Each digest pairs with the nearest copy reference;
multi-file directory copies pair via the byte count adjacent to the digest.
Paths under `../` or `owner/repo/` prefixes are not treated as local copies.

## Verification — real run on the frozen registry

Setup: `S=/fast/scratch/hyaku/mori-r91/Mo91E04Digest`; frozen bytes extracted
with `git show 79eaa8cf:corpus/SOURCES.md > $S/corpus/SOURCES.md` into a scratch
`corpus/` dir with symlinks `corpus/evidence -> <lane>/corpus/evidence` and
`.ufo -> <lane>/.ufo`; `<pinned-dir>` =
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-90/w1/Mo90S01Sources/sources/`.

Command:
```
python3 .ufo/waves/round-91/w1/candidates/digest-check.py \
  $S/corpus/SOURCES.md \
  .ufo/waves/round-90/w1/Mo90S01Sources/sources/
```
Exit `1`. Full output (121 row lines + trailer) captured at
`$S/run-frozen.txt`; the lane-HEAD run (`corpus/SOURCES.md`, same pinned dir)
produced byte-identical output (`diff` clean) since the registry is unchanged.

Result: `DIGEST_CHECK rows=121 ok=87 mismatch=2 prefix_only=31 unpinned=1`

Non-ok rows (verbatim):
```
DIGEST S125 unpinned recorded=e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136 actual=-
DIGEST S235 mismatch recorded=9855a4986a312dfc946b1b97b6010a8e4f1e65a4a30cda99359e6df057ad8020 actual=9855a4986a312dfc946b1b97b6010a8e4f1e65a4a30dca99359e6df057ad8020
DIGEST S502..S525, S565..S571 prefix-only  (31 rows, recorded 8–16-hex prefixes, all strict prefixes of the copies' full sha256)
DIGEST S615 mismatch recorded=7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b8f1a60ad1a6f0 actual=7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b0f83b9a8a42f5
```

Findings:
- **S615 mismatch = round-90 defect R8 confirmed.** Recorded digest differs
  from `python-ast-3.15.2.html`'s real sha256 (diverges at char ~56, not a
  prefix). Checker resolves "the pinned copy" via the 362493-byte size hint to
  the round-90 pinned dir and flags it.
- **S235 mismatch = NEW defect, same class.** Row records
  `…a30cda99359e6df057ad8020` (transposed `dc`/`cd`); the pinned
  `corpus/evidence/sources-r42/S235.pdf` hashes to `…a30dca99359e6df057ad8020`.
  The registry's own S349 row and cross-reference carry the correct variant
  (1 typo occurrence vs 2 correct in `corpus/SOURCES.md`).
- **S125 unpinned.** Names receipts `.ufo/waves/round-25/capture/capture.txt`
  and `capture-earlyoom.txt`; `git ls-tree -r 79eaa8cf` shows no `capture/`
  dir under round-25 — the pinned receipts are absent from the frozen tree.
- **prefix-only (31 rows).** S502–S525 and S565–S571 record truncated
  8–16-hex digests; every one is a strict prefix of the pinned copy's full
  sha256 (spot-verified S502 `bc178ff511e0`, S565 `11c6b712`, S571 `c4edc1e7`).
  Consistent but not full-length — reported as non-ok per the exit contract.
- **ok (87 rows)** include all explicit `copy <path> sha256 <64hex>` rows
  (S349, S475, S479–S501, S526–S559, S579–S591, S594–S602, S604–S605,
  S607–S611), receipt/extract rows (S488, S544, S547, S548, S550, S553–S559),
  the directory copy S597 (paired by adjacent byte counts 17266/824),
  same-bytes inheritance S606, and pinned-phrase rows S612, S616.

## Able-to-fail proof

Copied the frozen registry to `$S/corpus/SOURCES.md`, flipped one hex char in
S490's recorded digest (`8a28e0bc` → `9a28e0bc`, line 269), reran:
```
DIGEST S490 mismatch recorded=9a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e actual=8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e
DIGEST_CHECK rows=121 ok=86 mismatch=3 prefix_only=31 unpinned=1
```
exit `1` — the checker names the corrupted row and fails. (`$S/run-corrupt.txt`)

## Scope accounting (389 registry rows)

- 121 in scope (copy ref + recorded digest) — all emitted a DIGEST line.
- 90 rows record sha256 but name no pinned copy (fetched-page digests only,
  e.g. S066, S077–S177 range, S473, S478, S552) — out of scope.
- 17 rows name a copy but record no sha256 (e.g. S232–S234, S241, S262, S347,
  S476, S546, S561–S564, S613–S614) — out of scope.
- S560 is the only row with a digest plus only non-copy path mentions
  (`corpus/lessons/…`, `corpus/SOURCES.md`) — excluded; its `1603404d…` is the
  ROMA PDF's digest, not a local copy's.
- S034 excluded: its only digest is "script SHA-256" (tools/mori-census.sh at
  round-12 commit; the script has since changed) — attributed to a non-copy
  artifact, not the receipt copy.

## Limits / defects of the checker

- Nearest-path pairing is heuristic; rows naming several copies with several
  digests could mispair, though every multi-copy row in this registry resolved
  correctly (verified S125, S553–S559, S588–S591, S597).
- "the pinned copy" resolution depends on `<pinned-dir>` containing the copy;
  with a different pinned-dir the three phrase rows (S612/S615/S616) would
  report unpinned rather than guessing — intentional, not silent.
- prefix-only is a distinct non-ok class: the recorded value is a genuine
  prefix of the copy digest, not corruption; the L1 decides whether truncated
  registry digests are acceptable.
- The checker does not repair the registry; S235/S615 corrections are L1's call.
- No temp files; TMPDIR irrelevant (read-only). No writes outside stdout.

## Files written

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-91/w1/candidates/digest-check.py` — sha256 `a692b159646e8979f9fc95d5eee82a9a30cee4d8f67432ee824fff7e9d30cee7`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-91/w1/Mo91E04Digest.md` — this report

Scratch `/fast/scratch/hyaku/mori-r91/Mo91E04Digest/` deleted after receipts
were captured above.
