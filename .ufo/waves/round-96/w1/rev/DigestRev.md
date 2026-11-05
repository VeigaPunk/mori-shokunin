# DigestRev — independent non-author verification of C2 (round 96, wave w1)

Seat: DigestRev (reviewer, leaf member). Date: 2026-11-05. Lane HEAD entering wave: `66c5518e239eeacd6070be26d78085ef702392cb`; observed at review time (read-only `git -C … rev-parse HEAD`): `b88c8ae8ff85d1cb7df81fffef2f46a0512e76b5` (the freeze commit that adds the contract). Scope: claim C2 freshness, rows S125 S612 S615 S616 S622 S623 only. Executor DigestExec is a different seat; all numbers below are my own. Detection and report only — no remediation, no edits outside this file. No tools were installed or upgraded (curl, python3, coreutils, diff all preexisting); no host settings touched; git used read-only exactly once.

## 1. My own recorded-values run (not the executor's)

```
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-source-digest.py \
    /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md \
    /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence
DIGEST S125 unpinned recorded=e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136 actual=-
DIGEST S612 unpinned recorded=0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd actual=-
DIGEST S615 unpinned recorded=7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b8f1a60ad1a6f0 actual=-
DIGEST S616 unpinned recorded=6842ed0f53882c5a4d7a852ff969842f62aba92f918e2192db0df6ed23c3cb72 actual=-
DIGEST S622 unpinned recorded=f206647fba42b627f46d29993490fbb585adedaa5d27b9ed575f50ef9002f69b actual=-
DIGEST S623 unpinned recorded=90ac3b25cb2dd28192a5d1c7d45da5ef966d32666d0c583a13eb2ec6f4831ad0 actual=-
DIGEST_CHECK rows=124 ok=86 mismatch=0 superseded=1 prefix_only=31 unpinned=6
exit=1
```

Reproduces the frozen before-state exactly (unpinned=6, same six rows). Tool semantics note: for S125 the tool pairs the row with the sibling-repo **receipt** digest `e60f1bbc…` (`.ufo/waves/round-25/capture/capture.txt`, a copy-clause path); the row's URL-bytes digest `ecafdcdd…` is attributed to "entry bytes", which the tool's docstring explicitly ignores. Both are compared below.

## 2. My fresh fetches (curl -sS -L, no compression negotiation; identity bytes)

| row | URL (effective, 0 redirects all) | UTC (start–end) | HTTP | bytes | sha256 (mine) |
|---|---|---|---|---|---|
| S125 | raw.githubusercontent.com/VeigaPunk/tsukuroi-shokunin/157ee255/corpus/knowledge/memory-pressure-r25.md | 12:21:59Z | 200 | 27,828 | `ecafdcdd1cc3417f5da40bf8dc9d46925e39550ec1be5baad0949e2458bdcd25` |
| S612 | pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html | 12:21:59–12:22:00Z | 200 | 357,953 | `0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd` |
| S615 | docs.python.org/3/library/ast.html | 12:22:00Z | 200 | 362,493 | `5e531ef083fe5255fe45b6148bf07eec5d595bf8d9791537aa307242832ab696` |
| S616 | docs.python.org/3/library/tokenize.html | 12:22:00Z | 200 | 53,982 | `91bea7a659ed4cf3ea66d9552480c3f2c4cb02066219c527b2c56f0594106758` |
| S622 | git-scm.com/docs/git-log | 12:22:00Z | 200 | 375,834 | `f206647fba42b627f46d29993490fbb585adedaa5d27b9ed575f50ef9002f69b` |
| S623 | docs.python.org/3/using/cmdline.html | 12:22:00Z | 200 | 171,073 | `f0a033694b4368dad6f54616e94d7f13452a59ce28cc0b29d9bb91ef85a53cdf` |

All six byte counts equal the rows' recorded counts (27,828 / 357,953 / 362,493 / 53,982 / 375,834 / 171,073).

## 3. Digest comparison (mine vs recorded) and cmp vs executor's staged copies (`.ufo/waves/round-96/w1/digest/pinned/`, declared final by DigestExec 2026-11-05)

- **S125** — my fetch `ecafdcdd…` == row's recorded URL-bytes digest `ecafdcdd…` (exact). Tool-paired receipt digests: executor staged `pinned/.ufo/waves/round-25/capture/capture.txt` sha `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136` == recorded, and `capture-earlyoom.txt` sha `7adbe069326afaaa103c447b95d507e989503356c864d9726edc45381fd40309` == recorded; both `cmp` IDENTICAL to the sibling originals at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/capture/` (read-only cmp). No copy of the URL bytes itself was staged (staged file list: `posix-shell-v3-chap02.html`, `git-log-docs.html`, `.ufo/…` receipts only).
- **S612** — fetch == recorded `0889867a…`. `cmp S612.fetch pinned/posix-shell-v3-chap02.html` → IDENTICAL.
- **S615** — fetch `5e531ef0…` ≠ recorded `7891c588…8f1a60ad1a6f0` (same 362,493 bytes). No executor copy staged. Note: `corpus/lessons/round-91.md` C-1 already declares this recorded digest "not the full sha256 of its pinned copy"; my footer substitution (below) reproduces S619's corrected digest `7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b0f83b9a8a42f5`, not the original. Diff vs round-90 pinned copy `.ufo/waves/round-90/w1/Mo90S01Sources/sources/python-ast-3.15.2.html` (sha `7891c588…b0f83b9a8a42f5`, verified): exactly one line — `Last updated on Nov 05, 2026 (12:03 UTC).` vs `(00:37 UTC.)`.
- **S616** — fetch `91bea7a6…` ≠ recorded `6842ed0f…` (same 53,982 bytes). Proof the only difference is the docs build footer: rewriting my fetched bytes' footer minute to `00:37` reproduces the recorded digest **exactly** (`6842ed0f53882c5a4d7a852ff969842f62aba92f918e2192db0df6ed23c3cb72`). Content unchanged; live page is the 12:03 build.
- **S622** — fetch == recorded `f206647f…`. `cmp S622.fetch pinned/git-log-docs.html` → IDENTICAL.
- **S623** — fetch `f0a03369…` ≠ recorded `90ac3b25…` (same 171,073 bytes). Footer-minute substitution `08:02` reproduces the recorded digest **exactly** (`90ac3b25cb2dd28192a5d1c7d45da5ef966d32666d0c583a13eb2ec6f4831ad0`). Content unchanged; live page is the 12:03 build. All three python.org pages now carry `Last updated on Nov 05, 2026 (12:03 UTC).`

Tool probe of the staged layout (read-only; recorded digests untouched):

```
$ python3 tools/mori-source-digest.py corpus/SOURCES.md .ufo/waves/round-96/w1/digest/pinned
DIGEST S125 ok recorded=e60f1bbc…  actual=e60f1bbc…
DIGEST S612 ok recorded=0889867a…  actual=0889867a…
DIGEST S615 unpinned recorded=7891c588…8f1a60ad1a6f0 actual=-
DIGEST S616 unpinned recorded=6842ed0f… actual=-
DIGEST S622 ok recorded=f206647f…  actual=f206647f…
DIGEST S623 unpinned recorded=90ac3b25… actual=-
DIGEST_CHECK rows=124 ok=89 mismatch=0 superseded=1 prefix_only=31 unpinned=3
```

## 4. Quote sanity grep (S622, S623; tags stripped via script/style removal + `<[^>]*>` + entity unescape; whitespace-normalized matching)

| row | quoted phrase | result |
|---|---|---|
| S622 | "Select only files that are Added (A), Copied (C), Deleted (D), Modified (M), Renamed (R), have their type" | FOUND (ws-normalized) |
| S622 | "abbreviated commit hash" | FOUND (exact) |
| S623 | "Run Python in isolated mode. This also implies -E, -P and -s options." | FOUND (ws-normalized) |
| S623 | "All PYTHON* environment variables are ignored, too." | FOUND (ws-normalized) |

Raw-byte line hits: S622 diff-filter quote at raw line 6732 (row claims tag-stripped 6730-6744), `%h` phrase at 5504 (claims 5493-5504), S623 `-I` text at 528 (claims 527-535) — all inside the claimed spans. S612's claimed lines 1385-1386 not reproduced under any of three candidate strippers (quote sits at raw line 2103); convention unverifiable, named in §7, not a C2 axis.

## 5. Per-row verdict

| row | fetched==recorded? | P2 judged from executor copies? | verdict |
|---|---|---|---|
| S125 | URL bytes == recorded entry-bytes digest; staged receipts == recorded receipt digests == sibling originals | yes (probe: ok) | **ok** |
| S612 | yes (exact) | yes (cmp IDENTICAL; probe: ok) | **ok** |
| S615 | no (sha differs, same size) | no — precondition fails; no copy staged | **stale** (docs build moved 00:37→12:03; recorded digest already declared defective by r91 C-1; superseded-corrected digest verified against live content modulo footer) |
| S616 | no (sha differs, same size) | no — precondition fails | **stale** (footer-only difference proven; content unchanged) |
| S622 | yes (exact) | yes (cmp IDENTICAL; probe: ok) | **ok** |
| S623 | no (sha differs, same size) | no — precondition fails | **stale** (footer-only difference proven; content unchanged) |

## 6. C2 bearing (recommendation only)

With the executor's staged copies the command prints `unpinned=3 mismatch=0` — P2's `unpinned=0` is unmet and the kill rule's naming lands on S615, S616, S623 as stale. The three rows cannot be resolved by placing copies: their live bytes no longer hash to the recorded digests (docs.python.org rebuilds daily and the footer minute alone changes the sha), and recorded digests are never edited. The stale rows' teaching content is demonstrably unchanged (footer-substitution proofs); the gap is the digest-vs-build churn mechanism, which is the L1's to weigh. I express no remediation.

## 7. Checks not run (named)

- Provenance of S615's *original* recorded digest: not reproduced by any Nov 05 00:00–12:03 footer minute (724 candidates tested); deeper archaeology (r90 fetch env, Accept-Encoding variants) unrun.
- Whether a staged-copy layout other than the executor's (e.g. `corpus/evidence/` integration by the L1) changes the probe classification: unrun (copies not yet integrated).
- S125 git-blob identity (`be3065ae…`, a git object id, not a sha256): not computed; HTTP fetch + sha256 only.
- Tag-stripped line-number convention behind the rows' anchor line claims: not reproduced (S612 1385-1386 vs raw 2103); anchor-line bookkeeping is outside C2's predicate.
- DigestExec.md report cross-read: deliberately not relied on (independence requirement).

Scratch `/fast/scratch/hyaku/mori-r96/DigestRev` removed at exit (trap).
