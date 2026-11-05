# Mo97ScoutLive — round 97 w1, seat report (scout, lane `mori`)

Seat: independent re-open of the four sources this round touches. Detection/report only; no remediation.
Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin`. Scratch: `$HYAKU_SCRATCH/mori-r97/Mo97ScoutLive`
(`/fast/scratch/hyaku/mori-r97/Mo97ScoutLive`, removed on exit). Landing revision measured: `e85ed91249953094b067554bfa79fcdc65791f8e`.
All four fetches were made from a scratch cwd; `TMPDIR` set to the scratch root for the tool runs.

---

## 1. Live re-open of the four sources (independent, not the lane's receipt)

Command (one fetch per URL, `-L --max-time 60`, default UA):

```
for spec in "S615 https://docs.python.org/3/library/ast.html" "S616 https://docs.python.org/3/library/tokenize.html" "S623 https://docs.python.org/3/using/cmdline.html" "S628 https://raw.githubusercontent.com/python/docsbuild-scripts/main/README.md"; do
  id=${spec%% *}; url=${spec#* }
  echo "=== $id $url"; echo "access_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  curl -sS -o "live-$id" -w "http_status=%{http_code} size_download=%{size_download} url_effective=%{url_effective} content_type=%{content_type}\n" -L --max-time 60 "$url"
  printf "bytes=%s sha256=%s\n" "$(stat -c%s "live-$id")" "$(sha256sum "live-$id" | cut -d' ' -f1)"
done
```

Exact output:

```
=== S615 https://docs.python.org/3/library/ast.html
access_utc=2026-11-05T20:51:58Z
http_status=200 size_download=362493 url_effective=https://docs.python.org/3/library/ast.html content_type=text/html
bytes=362493 sha256=d5d9d590abfda6b55a9469b9330e42f25bdb0bc28f2e6490f18797d671265e8f
=== S616 https://docs.python.org/3/library/tokenize.html
access_utc=2026-11-05T20:51:58Z
http_status=200 size_download=53982 url_effective=https://docs.python.org/3/library/tokenize.html content_type=text/html
bytes=53982 sha256=bce324892ae8b1c3d5208eb130ea0ab0ad6eace6ef1cd1fdcb70e74c8703da0e
=== S623 https://docs.python.org/3/using/cmdline.html
access_utc=2026-11-05T20:51:58Z
http_status=200 size_download=171073 url_effective=https://docs.python.org/3/using/cmdline.html content_type=text/html
bytes=171073 sha256=57b7f76ba01d888cecf61e184cc2dfddd148b31716284e71f44a92df6d0e6811
=== S628 https://raw.githubusercontent.com/python/docsbuild-scripts/main/README.md
access_utc=2026-11-05T20:51:58Z
http_status=200 size_download=6835 url_effective=https://raw.githubusercontent.com/python/docsbuild-scripts/main/README.md content_type=text/plain; charset=utf-8
bytes=6835 sha256=0ae6b8806cbb28edd4f8b1ae98ac5045ced71234ba8c81dfa3bf7312eccac618
```

Second, independent fetch of the same four URLs at `2026-11-05T20:57:38Z` with `-A "curl/8.21.0"` and response
headers captured (`curl -sS -D hdr-$id.txt -o live2-$id ...`): HTTP/2 200 for all four, byte-identical sizes and
sha256 to the first fetch (`d5d9d590…5e8f`, `bce32489…da0e`, `57b7f76b…6811`, `0ae6b880…c618`), i.e. no
between-fetch churn inside the window. Server headers for the three python pages:
`server: nginx`, `last-modified: Thu, 05 Nov 2026 12:49:35 GMT` (S615, S616) / `12:49:36 GMT` (S623),
`etag: "6aec7b5f-587fd"` / `"6aec7b5f-d2de"` / `"6aec7b60-29c41"`, `x-cache: MISS, HIT` / `HIT, HIT` / `HIT, HIT`,
`date: Thu, 05 Nov 2026 20:57:38 GMT`. S628: HTTP/2 200, `etag: "36a0bf5100e64be3fba56bcc24fdea9be2bbddfc1d7824212a682c971a7fa4b8"`,
`content-type: text/plain; charset=utf-8`.

### 1a. Pinned copies in the landing tree (independently hashed)

`git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive e85ed91249953094b067554bfa79fcdc65791f8e | tar -x -C landing`
then sha256 over `landing/corpus/evidence/sources-r97/`:

```
S615.html 362493 7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b0f83b9a8a42f5
S616.html 53982 6842ed0f53882c5a4d7a852ff969842f62aba92f918e2192db0df6ed23c3cb72
S623.html 171073 90ac3b25cb2dd28192a5d1c7d45da5ef966d32666d0c583a13eb2ec6f4831ad0
S628.md 6835 0ae6b8806cbb28edd4f8b1ae98ac5045ced71234ba8c81dfa3bf7312eccac618
```

`cmp` against the working-tree copies: all four **IDENTICAL**. Provenance of the two python pins confirmed
byte-for-byte against the r90 copies in the same tree:
`.ufo/waves/round-90/w1/Mo90S01Sources/sources/python-ast-3.15.2.html` and `…/python-tokenize-3.15.2.html`
→ `cmp` **IDENTICAL** for S615 and S616 respectively (same sha256 values as above).
S623's pin is a reconstruction of the recorded bytes (see §2), not a raw copy of a prior commit.

---

## 2. The three python pages: single stamp line, time-only swap, diff counts

Each page carries exactly **one** `Last updated on … (HH:MM UTC).` line
(`grep -c "Last updated on"` = 1 for S615.html, S616.html, S623.html; live and pinned alike).

Stamp line numbers (raw file lines) and contents:

| id | pinned stamp line | pinned stamp | live stamp line | live stamp |
|---|---|---|---|---|
| S615 | 3328 | `Last updated on Nov 05, 2026 (00:37 UTC).` | 3328 | `Last updated on Nov 05, 2026 (12:47 UTC).` |
| S616 | 704 | `Last updated on Nov 05, 2026 (00:37 UTC).` | 704 | `Last updated on Nov 05, 2026 (12:47 UTC).` |
| S623 | 1911 | `Last updated on Nov 05, 2026 (08:02 UTC).` | 1911 | `Last updated on Nov 05, 2026 (12:47 UTC).` |

### 2a. Replace ONLY the time in the live stamp with the pinned copy's time → does sha256 equal the pin?

Script (per id): regex `STAMP = re.compile(rb"Last updated on ([A-Z][a-z]{2} [0-9]{2}, [0-9]{4}) \(([0-9]{2}:[0-9]{2}) UTC\)\.")`;
substitute only group 2 (the HH:MM), keeping the live date; hash; compare with sha256 of the pinned copy.

```
S615 live_date= Nov 05, 2026 live_time= 12:47 pinned_time= 00:37 time_only_swap_sha= 7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b0f83b9a8a42f5 ==pinned: True changed_lines= 2 differing_lines= 1
S616 live_date= Nov 05, 2026 live_time= 12:47 pinned_time= 00:37 time_only_swap_sha= 6842ed0f53882c5a4d7a852ff969842f62aba92f918e2192db0df6ed23c3cb72 ==pinned: True changed_lines= 2 differing_lines= 1
S623 live_date= Nov 05, 2026 live_time= 12:47 pinned_time= 08:02 time_only_swap_sha= 90ac3b25cb2dd28192a5d1c7d45da5ef966d32666d0c583a13eb2ec6f4831ad0 ==pinned: True changed_lines= 2 differing_lines= 1
```

**Answer: YES for all three.** Replacing only the `HH:MM` of the live stamp reproduces the pinned copy's
sha256 exactly. A whole-stamp replacement (the same result) was also computed and agrees:
S615 → `7891c588…42f5`, S616 → `6842ed0f…cb72`, S623 → `90ac3b25…31ad0`.

### 2b. Every differing line, live vs pinned

Unified diff of the decoded pages (`difflib.unified_diff(pinned_lines, live_lines, n=0)`):

```
S615: changed_lines=2 differing_lines=1
    -      Last updated on Nov 05, 2026 (00:37 UTC).
    +      Last updated on Nov 05, 2026 (12:47 UTC).
S616: changed_lines=2 differing_lines=1
    -      Last updated on Nov 05, 2026 (00:37 UTC).
    +      Last updated on Nov 05, 2026 (12:47 UTC).
S623: changed_lines=2 differing_lines=1
    -      Last updated on Nov 05, 2026 (08:02 UTC).
    +      Last updated on Nov 05, 2026 (12:47 UTC).
```

**Differing-line count = 1 per page** (the stamp line only). Line totals identical (S615 3339/3339,
S616 715/715, S623 1922/1922); `difflib.SequenceMatcher` opcodes: exactly 1 `replace` per page at the
stamp line. So the delta is the per-build stamp and nothing else — consistent with the C2 claim's
"time-churn = docs.python.org 'Last updated on' stamp only".

---

## 3. S628 — the new row's quote, word count, and row fields

### 3a. Does the quote occur in live bytes and in the pinned copy?

Quote as carried in `corpus/SOURCES.md` (S628 row) and `corpus/lessons/round-97.md` (Gate):
`This repository contains scripts for automatically building the Python documentation on docs.python.org.`

Raw-substring count (`grep -c -F` / `bytes.count`), live and pinned:

```
live occurrences: 0
pin  occurrences: 0
```

The sentence is present in both files but **not** as a raw contiguous substring: the README carries a
markdown link and a line break. Live and pinned copies of lines 6–7 are byte-identical:

```
This repository contains scripts for automatically building the Python
documentation on [docs.python.org](https://docs.python.org).
```

Normalized count (markdown link stripped to its text, whitespace collapsed) — this is where the quote lives:

```
live raw_exact= 0 linkstripped_exact= 0 collapsed_exact= 1
pin  raw_exact= 0 linkstripped_exact= 0 collapsed_exact= 1
```

So: the quote occurs **once** in the live bytes and **once** in the pinned copy *after* link-stripping and
whitespace collapsing; it occurs **zero** times as a raw byte substring in either. The pinned copy is
byte-identical to the live body (`diff live-S628.md pinned/S628.md` → no output, exit 0) and both hash to
`0ae6b8806cbb28edd4f8b1ae98ac5045ced71234ba8c81dfa3bf7312eccac618`.

### 3b. Word count

`printf '%s' "This repository contains scripts for automatically building the Python documentation on docs.python.org." | wc -w` → **12**
(as carried in the file between the quote marks: 12). The link-marked variant
(`… on [docs.python.org](https://docs.python.org).`) is also 12 words. The bound "≤25 words" holds (12 ≤ 25).

**Discrepancy worth routing (not a claim falsification):** `corpus/lessons/round-97.md` Gate row S628 labels
the quote **"14 words"**. The actual `wc -w` of the quoted text as carried is **12**. QUALITY 90 requires
every word-count label in a `## Gate` table to equal `wc -w` of the quoted text as carried in the file.
The committed QUALITY-90 checker does **not** flag it, because its regexes only recognise a label written as
`(N words)` immediately before/after the quote, whereas r97's Gate writes it inside a longer parenthetical
(`(pinned copy … raw lines 6-7, 14 words)`). Running the frozen QUALITY-90 check at both revisions:

```
landing  e85ed912: word_labels=16 mismatched=3   (line=362 label=15 wc=14; line=365 label=17 wc=15; line=365 label=22 wc=26)
entering 973b2af : word_labels=16 mismatched=3   (same three rows, all pre-existing SOURCES.md rows)
```

i.e. r97 introduces no *new* checker-detected mismatch; the S628 "14 words" label is a silent miscount.

### 3c. S628 row fields in `corpus/SOURCES.md`

| field | value in the row | check |
|---|---|---|
| kind | `code` | matches the source (a repository README) ✔ |
| tier | `B` | matches the lesson's decision cell (`**admit, mined, tier B**`) ✔ |
| digest | `sha256 0ae6b8806cbb28edd4f8b1ae98ac5045ced71234ba8c81dfa3bf7312eccac618` | equals sha256 of the pinned copy **and** of the live fetch ✔ |
| pinned copy path | `corpus/evidence/sources-r97/S628.md` | resolves in the landing tree; digest tool prints `DIGEST S628 ok recorded=0ae6b880… actual=0ae6b880…` ✔ |
| URL | `https://raw.githubusercontent.com/python/docsbuild-scripts/main/README.md` | HTTP 200, 6835 B, sha256 as recorded ✔ |
| access date | `fetched 2026-11-05` | my fetch 2026-11-05T20:51:58Z / 20:57:38Z, HTTP 200 ✔ |

---

## 4. Cross-checks of the two claimed surfaces at the landing revision (read-only, re-run by me)

### C2 counter, re-run by me on the landing tree

```
$ python3 .ufo/waves/round-97/count-c2.py --root $S/landing
TARGET S615 superseded-by S619 successor_ok=yes copy_equals_successor=yes copy=corpus/evidence/sources-r97/S615.html copy_sha=7891c58897fe9f78
TARGET S616 ok copy_matches_tool=yes copy=corpus/evidence/sources-r97/S616.html copy_sha=6842ed0f53882c5a
TARGET S623 ok copy_matches_tool=yes copy=corpus/evidence/sources-r97/S623.html copy_sha=90ac3b25cb2dd281
LIVE # MORI_DRIFT_RECHECK second_ua=curl/8.21.0 only=S615,S616,S623 from-sweep=- findings=- run-start=2026-11-05T20:52:27Z stamp-class=python-docs-page-stamp asset-class=learn-microsoft-asset-build-id
LIVE S615 time-churn as-of=2026-11-05T20:52:27Z
LIVE S616 time-churn as-of=2026-11-05T20:52:27Z
LIVE S623 time-churn as-of=2026-11-05T20:52:27Z
LIVE MORI_DRIFT_RECHECK rows=3 adjudicated=3 fresh=0 excerpt=0 time-churn=3 asset-churn=0 receipt-open=0 receipt-stale=0 ua-serving=0 content-drift=0 gate=0 unavailable=0 window=2026-11-05T20:52:27Z..2026-11-05T20:52:27Z
C2=met mismatch=0 unpinned=0 targets_ok=3/3 hole_guard=pass live=S615:time-churn,S616:time-churn,S623:time-churn checks_failed=- root=…/landing
exit=0
```

(The live leg ran again at `20:58:02Z` on the same tree with the same three `time-churn` classes and
`drift_exit=0`.) This matches the lane's `evidence/landing-c2.txt` byte-for-byte apart from the run
timestamps and the scratch root.

Digest tool over the landing tree's whole evidence dir (`tools/mori-source-digest.py corpus/SOURCES.md corpus/evidence`):

```
DIGEST S615 superseded-by S619
DIGEST S616 ok recorded=6842ed0f…cb72 actual=6842ed0f…cb72
DIGEST S619 ok recorded=7891c588…42f5 actual=7891c588…42f5
DIGEST S623 ok recorded=90ac3b25…31ad0 actual=90ac3b25…31ad0
DIGEST S628 ok recorded=0ae6b880…c618 actual=0ae6b880…c618
DIGEST_CHECK rows=125 ok=92 mismatch=0 superseded=2 prefix_only=31 unpinned=0
digest_exit=1        # exit 1 from the 31 pre-existing prefix_only rows, unchanged and out of scope per the contract
```

Note on S615 (expected, per the contract): S615's **own** recorded digest in `corpus/SOURCES.md` is
`7891c588…b8f1a60ad1a6f0`, which differs from the sha256 of the copy now pinned
(`…b0f83b9a8a42f5`) — that is the r91 mis-record the contract names; S619 carries the correct full digest,
the tool prints `superseded-by S619`, and the new copy hashes exactly to S619's `ok` digest
(`copy_equals_successor=yes`), so the r96 supersession hole is closed rather than exploited.

### C1 counter, re-run by me on the landing tree

```
$ python3 .ufo/waves/round-97/count-c1.py --root $S/landing
TARGET tools/mori-cgroup-pressure.py row='cgroup PSI survey (r62 tool, registry r97)' selftest_rc=0 selftest_line='MORI_CGROUP_PRESSURE_SELFTEST: pass=12 fail=0' stated_in_cell=yes token_in_verdict_map=yes
TARGET tools/mori-drift-recheck.py row='drift re-check (r66 tool, registry r97)' selftest_rc=0 selftest_line='MORI_DRIFT_RECHECK_SELFTEST: PASS (10 cases)' stated_in_cell=yes token_in_verdict_map=yes
TARGET tools/mori-scorecard-calibration.py row='SCORECARD Last-change calibration counter (r96 tool, registry r97)' selftest_rc=0 selftest_line='CALIB_SELFTEST pass=11 fail=0' stated_in_cell=yes token_in_verdict_map=yes
TARGET tools/mori-source-digest.py row='SOURCES digest check (r91 tool, registry r97)' selftest_rc=0 selftest_line='DIGEST_SELFTEST pass=11 fail=0' stated_in_cell=yes token_in_verdict_map=yes
C1=met unregistered=0 registry=met targets_ok=4/4 checks_failed=- root=…/landing
exit=0
```

The four registry rows exist in the landing `SKILL.md` (lines 1445–1448) with the row names the counter
attributes to each tool.

---

## 5. Observations (reported, not remediated)

1. **S628 Gate word-count label is wrong.** `corpus/lessons/round-97.md` Gate row S628 says "14 words";
   `wc -w` of the quoted text as carried is **12**. QUALITY 90 requires equality; the committed checker
   misses it because the label is not in the `(N words)` adjacency form its regexes accept. Route to the
   L1 as a QUALITY-90 defect (label correction is an in-place edit of a frozen-round lesson — the L1 decides).
2. **The S628 quote is not a raw substring of either copy** (raw count 0 in live and pinned). It is a
   link-stripped, whitespace-collapsed rendering of raw lines 6–7. The lane's HTML rows declare
   "tag-stripped lines …"; the S628 row declares "raw lines 6-7", which is where the sentence physically
   sits, but a reader grepping the pinned copy for the printed quote gets 0 hits. Not a predicate input
   for C2 (the counter does not test quotes); worth an L1 note on whether a markdown-source row should
   declare its normalisation.
3. **The three anchors were computed on two different "tag-stripped" conventions, and neither is
   reproducible by grepping the committed pin — QUALITY 162's own verification form fails on all three
   rows.** This is the sharpest thing my seat found, and it is **inherited** (the rows are byte-unchanged
   between entering `973b2af` and landing `e85ed912` except for the added S628 row).

   The authoring seats' own reports declare two different conversions:
   - r90 (S615, S616): *"Line numbers are those of the tag-stripped text of each fetched page (the seat's
     own conversion, not the raw HTML)"* (`.ufo/waves/round-90/w1/Mo90S01Sources-entry.md:39`).
   - r93 (S623): *"a 1:1 line-for-line tag strip of the fetched HTML"*
     (`.ufo/waves/round-93/w1/Mo93Sc01Src.md:30-31`).

   I reproduced the r90 convention exactly (drop `<script>`/`<style>`, strip tags, drop blank lines,
   collapse whitespace): it yields **1907** for `ast.walk`, **1881** for `get_source_segment` and **38**
   for the tokenize sentence — matching the r90 receipt's `start_line=1907 / 1881 / 38`
   (`.ufo/waves/round-90/w1/Mo90S01Sources.md:34-39`). So S615/S616's anchors are *internally honest*
   against the r90 conversion. S623's 527–535 is honest against the r93 1:1 strip (quote at 528 and
   531–532 of that strip).

   But the r97 landing **commits the pins under `corpus/evidence/sources-r97/` for the first time** —
   `git ls-tree -r 973b2af… | grep -E 'sources-r9[0-6]/.*(S615|S616|S623)'` returns **nothing**, so before
   r97 these three rows had **no corpus-level pin**. QUALITY 162 requires the located-line pointer to be
   verified **against the pinned copy**: *"the quoted text must appear on the named line of the pin (a
   grep of the exact sentence against that one line returns 1)"* (`corpus/QUALITY.md:1704-1707`). Against
   the r97 pins, that grep returns **0** for every recorded span:
   ```
   sed -n '1907,1908p' corpus/evidence/sources-r97/S615.html | grep -c -F "Recursively yield all descendant nodes in the tree starting at node (including node itself), in no specified order."   → 0
   sed -n '38,39p'    corpus/evidence/sources-r97/S616.html | grep -c -F "The scanner in this module returns comments as tokens as well"                                                            → 0
   sed -n '527,535p'  corpus/evidence/sources-r97/S623.html | grep -c -F "Run Python in isolated mode. This also implies -E, -P and -s options."                                                  → 0
   sed -n '527,535p'  corpus/evidence/sources-r97/S623.html | grep -c -F "All PYTHON* environment variables are ignored, too."                                                                → 0
   ```
   The lane's own `tools/mori-anchor-check.py` (registered in `SKILL.md:1326`, QUALITY 162 made runnable)
   says `verdict=mislocated` for all three rows on the r97 pins. Raw-pin line numbers where the quotes
   actually sit: S615 → 2864 (`ast.walk`) and 2812 (`get_source_segment`); S623 → 528 (`-I`, but the
   second sentence "All PYTHON* environment variables are ignored, too." is split across raw lines 531–532
   and never greps as one line); S616 → the sentence exists only in `<meta>` attributes and as
   `<p>`-wrapped fragments, never on one raw line.

   The contrast that proves this is a **pin/anchor-convention mismatch, not a broken pin**: the lane's
   own passing example (r74, S589) uses a raw HTML pin whose quote sits intact on raw line 524, and
   `mori-anchor-check.py --pin corpus/evidence/sources-r74/S589.html --check "monotonic_return|524|13|…"`
   prints `verdict=ok located_on=524` / `ANCHOR_CHECK: PASS` — I re-ran it. So the tool works when the
   pin and the anchor share a convention; for S615/S616/S623 they do not, because the pins were newly
   committed as **raw HTML** while the anchors index a **stripped-text line numbering** that is not
   committed anywhere. Nothing in the r97 tree lets a verifier reproduce "tag-stripped lines 1907-1908"
   without re-deriving the r90 seat's private conversion.

   Scope note: this is **not** a C1/C2 predicate input — `count-c2.py` checks digests, copy/successor
   equality, the hole guard and the live classes, never anchors; so the C2 verdict below is unaffected.
   It is a **routed defect for the L1** (QUALITY 162 class: a located-line pointer that the newly
   committed pin contradicts), to be fixed append-only per QUALITY 162 ("a drifted pointer is corrected by
   a NEW supersedes row … never an in-place anchor edit"), not by editing the rows in place.
   Also unrun by me: whether any *other* row that gained a corpus-level pin this round has the same
   mismatch, and the r66/r72/r74 rows that predate a corpus pin.
4. S623's live page and the pinned copy differ **only** in the stamp time, so the reconstructed pin's
   sha256 equal to the recorded digest is reproducible from a fresh fetch — that supports the contract's
   claim that the pin is "today's live page with the build stamp line restored".
5. **Working-tree drift observed during this seat (not mine).** At the end of the session
   `git status --porcelain` in the lane repo shows `M LOG.md`, `M SCORECARD.md`, `M SKILL.md` and
   `M corpus/lessons/round-97.md` — a SCORECARD append, a 2-line SKILL.md edit (rows at
   `SKILL.md:1445-1446`), a 10-line LOG.md append and a 30-line lesson amendment. These appeared
   **after** my seat began (my first `git status` showed only untracked round-97 wave files) and are not
   my edits: I wrote only this report file, and every measurement above is against the **committed**
   landing tree `git archive e85ed912…` (which contains the four registry rows at `SKILL.md:1445-1448`),
   never against the dirty working tree. The lesson amendment now includes a "quote-length label not
   counted" item recording my observation 1, but **not** the anchor/pin-convention mismatch of
   observation 3 — that item is still unrecorded in the lesson, so it needs the L1's attention.
   Flagging so the L1 knows the working tree no longer equals the landing revision it is integrating.

---

## 6. Unrun / out-of-scope checks (named, not silently omitted)

- I did **not** run `tools/mori-anchor-check.py --selftest`; I ran it only with `--check` specs (four
  r97-pin runs, all `mislocated`, plus the lane's own r74/S589 example, which passes).
- I started an exhaustive brute-force over tag-strip conventions (0–3 tag classes × script/style removal
  × blank-line handling) asking whether **one** convention reproduces all three recorded anchors, and
  **cancelled it**: the two authoring seats' own receipts settle the question — r90 declares its
  conversion and I reproduced its `start_line=1907 / 1881 / 38` exactly, r93 declares a 1:1
  line-for-line strip and its `527-535` resolves under that — so the anchors were computed under two
  *declared but different* conventions, which is the finding. The cancelled search could only have
  added a third possible convention, not changed the mismatch with the committed raw-HTML pins
  (whose greps return 0 for all four spans regardless of convention).
- I did **not** run the tools' `--selftest` batteries directly (count-c1 did, as its receipts show).
- I did **not** run `tools/mori-drift-recheck.py` with `--from-sweep` or against any row other than
  S615/S616/S623, and did not run `mori-cgroup-pressure.py`, `mori-scorecard-calibration.py`, or
  `mori-source-digest.py --selftest` standalone.
- I did **not** verify the S623 pin against a **prior committed copy** of the cmdline page: no such copy
  exists in the tree (only `.ufo/waves/round-89/w1/Mo89S01Sources/sources/cmdline-3.14.10.html`, a
  3.14.10 page, and `.ufo/waves/round-96/w1/digest/fetched/S623.bin`, sha256 `f0a03369…3cdf` ≠ recorded).
  S623's pin is therefore verified only by digest equality with its recorded digest plus live-swap equality.
- I did **not** check the `prefix_only` 31 rows or the two `unpinned` rows (S125, S612, S622) that the digest
  tool reports when run against the r97 evidence dir alone; they are outside the C2 targets.
- I did **not** audit the S615/S616/S623 anchor spans beyond the two conventions in §5.3, and did not
  attempt to reproduce the historical r90/r93 line-numbering method beyond those conventions.
- No host sysctl, service, limit, or kernel setting was touched; no git/jj mutation was performed
  (`git archive`, `git show`, `git log -S`, `git rev-parse`, `git ls-tree` only).

VERDICT C2 holds: all three pins byte-match their recorded digests, the live re-open at 2026-11-05T20:51:58Z/20:57:38Z shows a 1-line stamp-only delta per page, the time-only swap reproduces each pin's sha256 exactly, and the fresh drift-recheck classifies all three `time-churn` — the residual items are the S628 "14 words" miscount and the undeclared markdown-link normalisation, neither of which is a C2 predicate input.
VERDICT C1 holds: the landing tree's `SKILL.md` carries the four registry rows, each tool's selftest exits 0 with the line the row states, and the frozen counter prints `C1=met unregistered=0 registry=met targets_ok=4/4` on my own re-run.

Report: `.ufo/waves/round-97/w1/Mo97ScoutLive.md`
