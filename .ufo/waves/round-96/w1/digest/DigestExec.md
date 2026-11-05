# Round 96 w1 — DigestExec (claim C2 freshness) — per-row table

Lane: /home/vgpnk/Projects/shokunin/mori-shokunin. Lane HEAD now `b88c8ae8` (contract commit, child of entering `66c5518e`; read-only `git -C ... log`).
Access times are UTC from curl runs on 2026-11-05. All six URLs returned HTTP 200 with zero redirects (`num_redirects 0`, `url_effective` equal to the requested URL).

## Per-row table

| ID | URL | HTTP | bytes | sha256 live | recorded | verdict | resolved copy (pinned/) |
|---|---|---|---|---|---|---|---|
| S125 | https://raw.githubusercontent.com/VeigaPunk/tsukuroi-shokunin/157ee255/corpus/knowledge/memory-pressure-r25.md (entry, sibling commit 157ee255) | 200 | 27828 | `ecafdcdd1cc3417f5da40bf8dc9d46925e39550ec1be5baad0949e2458bdcd25` (entry bytes; the row names this as a non-copy digest, exempt, and it matches) | copy digests `e60f1bbc…447136` (`.ufo/waves/round-25/capture/capture.txt`) and `7adbe069…409` (`…/capture-earlyoom.txt`) | ok (via the sibling receipts, below) | `pinned/.ufo/waves/round-25/capture/capture.txt`, `pinned/.ufo/waves/round-25/capture/capture-earlyoom.txt` |
| S125 receipt 1 | https://raw.githubusercontent.com/VeigaPunk/tsukuroi-shokunin/157ee255/.ufo/waves/round-25/capture/capture.txt | 200 | 5607 | `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136` | `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136` | ok | `pinned/.ufo/waves/round-25/capture/capture.txt` (fetched/S125-capture.txt) |
| S125 receipt 2 | https://raw.githubusercontent.com/VeigaPunk/tsukuroi-shokunin/157ee255/.ufo/waves/round-25/capture/capture-earlyoom.txt | 200 | 1037 | `7adbe069326afaaa103c447b95d507e989503356c864d9726edc45381fd40309` | `7adbe069326afaaa103c447b95d507e989503356c864d9726edc45381fd40309` | ok | `pinned/.ufo/waves/round-25/capture/capture-earlyoom.txt` (fetched/S125-capture-earlyoom.txt) |
| S612 | https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html | 200 | 357953 | `0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd` | `0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd` | ok | `pinned/posix-shell-v3-chap02.html` (fetched/S612.bin) |
| S615 | https://docs.python.org/3/library/ast.html | 200 | 362493 | `5e531ef083fe5255fe45b6148bf07eec5d595bf8d9791537aa307242832ab696` | `7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b8f1a60ad1a6f0` | **stale (live != recorded): not pinned** | none |
| S616 | https://docs.python.org/3/library/tokenize.html | 200 | 53982 | `91bea7a659ed4cf3ea66d9552480c3f2c4cb02066219c527b2c56f0594106758` | `6842ed0f53882c5a4d7a852ff969842f62aba92f918e2192db0df6ed23c3cb72` | **stale (live != recorded): not pinned** | none |
| S622 | https://git-scm.com/docs/git-log | 200 | 375834 | `f206647fba42b627f46d29993490fbb585adedaa5d27b9ed575f50ef9002f69b` | `f206647fba42b627f46d29993490fbb585adedaa5d27b9ed575f50ef9002f69b` | ok | `pinned/git-log-docs.html` (fetched/S622.bin) |
| S623 | https://docs.python.org/3/using/cmdline.html | 200 | 171073 | `f0a033694b4368dad6f54616e94d7f13452a59ce28cc0b29d9bb91ef85a53cdf` | `90ac3b25cb2dd28192a5d1c7d45da5ef966d32666d0c583a13eb2ec6f4831ad0` | **stale (live != recorded): not pinned** | none |

Determinism: a second live fetch of S615, S616 and S623 returned byte-identical files (same sha256 as the first fetch).

## Stale rows (named per the kill rule)

- **S615** `ast`: live `5e531ef0…`, recorded `7891c588…94b8f1a6`. The round-90 copy on disk (`.ufo/waves/round-90/w1/Mo90S01Sources/sources/python-ast-3.15.2.html`, 362493 B) hashes to `7891c588…94b0f83b`, which is the digest S619 records, not S615's. The recorded S615 digest matches neither the round-90 copy nor the live bytes. The live bytes differ from the round-90 copy in 4 bytes at offsets 362240–362244 (253 bytes before EOF, same length).
- **S616** `tokenize`: live `91bea7a6…`, recorded `6842ed0f…`. The round-90 copy (`…/python-tokenize-3.15.2.html`, 53982 B) hashes exactly to the recorded `6842ed0f…`. The live bytes differ from it in 4 bytes at offsets 53729–53733 (253 bytes before EOF, same length).
- **S623** `cmdline`: live `f0a03369…`, recorded `90ac3b25…`, same byte count (171073). The contract's quote "Run Python in isolated mode. This also implies -E, -P and -s options." is present in the live page's prose (grep line 528) but markup splits the text, so my tag-stripped check did not confirm it verbatim.

Only live bytes whose sha256 equals the recorded digest may be pinned, so none of these three are pinned. The round-90 copies were not fetched this round and are not used.

## Scratch tool output (candidate pinned set, unmodified tool, `corpus/evidence` = full real evidence tree + S125/S612/S622 pins; scratch `.ufo` linked read-only to the lane)

```
DIGEST S125 ok recorded=e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136 actual=e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136
DIGEST S611 ok recorded=0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd actual=0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd
DIGEST S612 ok recorded=0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd actual=0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd
DIGEST S615 unpinned recorded=7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b8f1a60ad1a6f0 actual=-
DIGEST S616 unpinned recorded=6842ed0f53882c5a4d7a852ff969842f62aba92f918e2192db0df6ed23c3cb72 actual=-
DIGEST S619 ok recorded=7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b0f83b9a8a42f5 actual=7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b0f83b9a8a42f5
DIGEST S622 ok recorded=f206647fba42b627f46d29993490fbb585adedaa5d27b9ed575f50ef9002f69b actual=f206647fba42b627f46d29993490fbb585adedaa5d27b9ed575f50ef9002f69b
DIGEST S623 unpinned recorded=90ac3b25cb2dd28192a5d1c7d45da5ef966d32666d0c583a13eb2ec6f4831ad0 actual=-
DIGEST_CHECK rows=124 ok=89 mismatch=0 superseded=1 prefix_only=31 unpinned=3
EXIT=1
```

Tool selftest (scratch copy of tool, run as `--selftest`): `DIGEST_SELFTEST pass=11 fail=0`, exit 0.

Diagnostic only (NOT pinned; live stale bytes placed under scratch names to see the verdict; receipt `tool-run-diag-stale-live-NOT-PINNED.txt`):

```
DIGEST S615 superseded-by S619
DIGEST S616 mismatch recorded=6842ed0f… actual=91bea7a6…
DIGEST S623 mismatch recorded=90ac3b25… actual=f0a03369…
DIGEST_CHECK rows=124 ok=89 mismatch=2 superseded=2 prefix_only=31 unpinned=0
```

Note for L1 (registry, not edited): S619's teaches cell reads "supersedes S615". If a live S615 copy were ever pinned and mismatched, the tool would classify S615 as `superseded-by S619` and drop it from mismatch=. That is the tool's documented rule, but it means a stale S615 can be hidden by a successor row. Not used here.

## Pinned set (copied byte-for-byte from fetched/ or the commit-pinned raw receipts)

```
0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd  pinned/posix-shell-v3-chap02.html   (S612)
f206647fba42b627f46d29993490fbb585adedaa5d27b9ed575f50ef9002f69b  pinned/git-log-docs.html            (S622)
e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136  pinned/.ufo/waves/round-25/capture/capture.txt         (S125)
7adbe069326afaaa103c447b95d507e989503356c864d9726edc45381fd40309  pinned/.ufo/waves/round-25/capture/capture-earlyoom.txt (S125)
```

The L1 copies `pinned/` into `corpus/evidence/` keeping the layout. The S125 receipts are cited by repo-relative `.ufo/waves/round-25/...`; the tool resolves that path under the pinned dir, so the landing location is `corpus/evidence/.ufo/waves/round-25/capture/`. S612 and S622 resolve by their recorded byte count (357953, 375834) through "the pinned copy" search, so their file names are free.

## S125 (sibling-repo path)

The S125 registry row names `tsukuroi-shokunin/corpus/knowledge/memory-pressure-r25.md` (sibling lane, commit 157ee255). Its recorded copy digests are for two sibling receipts, not for the entry: `e60f1bbc…` (capture.txt) and `7adbe069…` (capture-earlyoom.txt). Both are live-verified this round with raw fetches at commit 157ee255, and the local sibling files at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/capture/` hash identically. The sibling checkout is at a different HEAD (`64f45b79`), so the commit-pinned raw fetch is the proof used. The row's `ecafdcdd…` entry-bytes digest matches the live entry and is exempt by the tool.

## Final DIGEST_CHECK (real registry, unchanged; scratch run above is the candidate)

Real registry baseline (before pins are landed): `DIGEST_CHECK rows=124 ok=86 mismatch=0 superseded=1 prefix_only=31 unpinned=6`, exit 1.
Candidate after this seat's pins: `DIGEST_CHECK rows=124 ok=89 mismatch=0 superseded=1 prefix_only=31 unpinned=3`, exit 1.

**Predicate P2 is NOT met**: unpinned is 3 (not 0), ok is 89 (not 92). The 3 remaining unpinned rows are S615, S616, S623, all stale (live bytes do not hash to the recorded digest). Kill rule: C2 is unmet.

## Not run / not done

- No registry edits; no recorded digest edited; SOURCES.md unchanged.
- No installs (no tools installed or updated this seat).
- `corpus/evidence/` was not written (the L1 copies from `pinned/`).
- Census (`scripts/sources-census.sh`) not run: not assigned to this seat.
- Scratch dir `/fast/scratch/hyaku/mori-r96/DigestExec` removed after receipts were copied here. `HYAKU_SCRATCH` was unset; the default `/fast/scratch/hyaku` was used.
