# Mo97RevStamp — revenger report (mori round 97, w1, attempt 1)

Role: reverse-engineer the docs.python.org byte churn behind C2's three re-pinned rows
(S615 ast, S616 tokenize, S623 cmdline) and test hypothesis **H**:

> every byte difference between any two of {r96 live fetch, r90 copy, r97 pinned copy, fresh live fetch}
> is confined to the single `Last updated on <Mon DD, YYYY> (<HH:MM UTC).` line.

Detection and report only; nothing was remediated, no lane/tool/corpus file was edited, no git/jj mutation was run.
Scratch: `$HYAKU_SCRATCH/mori-r97/Mo97RevStamp` (`/fast/scratch/hyaku/mori-r97/Mo97RevStamp`), removed on exit.
Tools installed/updated: none (no install was needed; `pacman` not invoked).

---

## 1. Reconstructed contract (C2 leg d, the surface under attack)

`tools/mori-drift-recheck.py` classifies a row by comparing the **newest** copy
`corpus/evidence/sources-rN/<sid>.*` (highest N; `tools/mori-source-drift.py:87 find_copy`) with a **fresh** fetch:

* `tools/mori-drift-recheck.py:140-142`
  `STAMP_RE = re.compile(rb"^[ \t]*Last updated on [A-Z][a-z]{2} [0-9]{2}, [0-9]{4} \([0-9]{2}:[0-9]{2} UTC\)\.[ \t]*$")`
* `:178-180 stamp_free(body)` — drops every line matching `STAMP_RE`.
* `:310` `elif stamp_free(copy) == stamp_free(body_t): token = "time-churn"` (the only branch that yields `time-churn`).
* `:322` second arm on the pinning UA (`curl/8.21.0`, `SECOND_UA_DEFAULT`); a stamp+content delta satisfies
  neither grammar and falls to `content-drift` (`:327`).
* Frozen C2 counter `count-c2.py` leg (d) requires exit 0 and every one of S615/S616/S623 in `{fresh, time-churn}`.

So C2's live leg is exactly: *the pinned bytes and today's bytes differ only in stamp lines*.

## 2. Evidence chain (bytes on disk, hashes computed this run)

Sources used (all absolute):

| member | path | sha256 | bytes | stamp line |
|---|---|---|---|---|
| S615 r96 fetch | `.ufo/waves/round-96/w1/digest/fetched/S615.bin` | `5e531ef083fe5255fe45b6148bf07eec5d595bf8d9791537aa307242832ab696` | 362493 | L3328 `(12:03 UTC)` |
| S615 r90 copy | `.ufo/waves/round-90/w1/Mo90S01Sources/sources/python-ast-3.15.2.html` | `7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b0f83b9a8a42f5` | 362493 | L3328 `(00:37 UTC)` |
| S615 pinned r97 | `corpus/evidence/sources-r97/S615.html` | `7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b0f83b9a8a42f5` | 362493 | L3328 `(00:37 UTC)` |
| S615 live now | fresh `curl` fetch | `d5d9d590abfda6b55a9469b9330e42f25bdb0bc28f2e6490f18797d671265e8f` | 362493 | L3328 `(12:47 UTC)` |
| S616 r96 fetch | `.ufo/waves/round-96/w1/digest/fetched/S616.bin` | `91bea7a659ed4cf3ea66d9552480c3f2c4cb02066219c527b2c56f0594106758` | 53982 | L704 `(12:03 UTC)` |
| S616 r90 copy | `.ufo/waves/round-90/w1/Mo90S01Sources/sources/python-tokenize-3.15.2.html` | `6842ed0f53882c5a4d7a852ff969842f62aba92f918e2192db0df6ed23c3cb72` | 53982 | L704 `(00:37 UTC)` |
| S616 pinned r97 | `corpus/evidence/sources-r97/S616.html` | `6842ed0f53882c5a4d7a852ff969842f62aba92f918e2192db0df6ed23c3cb72` | 53982 | L704 `(00:37 UTC)` |
| S616 live now | fresh `curl` fetch | `bce324892ae8b1c3d5208eb130ea0ab0ad6eace6ef1cd1fdcb70e74c8703da0e` | 53982 | L704 `(12:47 UTC)` |
| S623 r96 fetch | `.ufo/waves/round-96/w1/digest/fetched/S623.bin` | `f0a033694b4368dad6f54616e94d7f13452a59ce28cc0b29d9bb91ef85a53cdf` | 171073 | L1911 `(12:03 UTC)` |
| S623 pinned r97 | `corpus/evidence/sources-r97/S623.html` | `90ac3b25cb2dd28192a5d1c7d45da5ef966d32666d0c583a13eb2ec6f4831ad0` | 171073 | L1911 `(08:02 UTC)` |
| S623 live now | fresh `curl` fetch | `57b7f76ba01d888cecf61e184cc2dfddd148b31716284e71f44a92df6d0e6811` | 171073 | L1911 `(12:47 UTC)` |

Fresh fetch (this run, 2026-11-05 ~20:52 UTC), both UAs:

```
$ curl -sS --max-time 60 -A "curl/8.21.0"        -o live-<id>.html    -w "$id http=%{http_code} bytes=%{size_download} url=%{url_effective}\n" "$u"
$ curl -sS --max-time 60 -A "mori-source-drift/1.0" -o toolua-<id>.html -w "$id http=%{http_code} bytes=%{size_download}\n" "$u"
ast http=200 bytes=362493 url=https://docs.python.org/3/library/ast.html
tokenize http=200 bytes=53982 url=https://docs.python.org/3/library/tokenize.html
cmdline http=200 bytes=171073 url=https://docs.python.org/3/using/cmdline.html
d5d9d590abfda6b55a9469b9330e42f25bdb0bc28f2e6490f18797d671265e8f  live-ast.html
57b7f76ba01d888cecf61e184cc2dfddd148b31716284e71f44a92df6d0e6811  live-cmdline.html
bce324892ae8b1c3d5208eb130ea0ab0ad6eace6ef1cd1fdcb70e74c8703da0e  live-tokenize.html
```

`toolua-*.html` hashes are **identical** to `live-*.html` (no UA-serving split), and the diff tool-UA vs curl-UA bodies is empty.

## 3. Test of H — pairwise diffs (line-exact)

Script `$S/churn.py` (scratch, this run) compares every pair inside each group, prints each differing line, and
independently re-checks `STAMP_RE` membership of every differing line.

```
GROUP S615
  r96-fetch   stamps=1 L3328 "      Last updated on Nov 05, 2026 (12:03 UTC)."
  r90-copy    stamps=1 L3328 "      Last updated on Nov 05, 2026 (00:37 UTC)."
  pinned-r97  stamps=1 L3328 "      Last updated on Nov 05, 2026 (00:37 UTC)."
  live-now    stamps=1 L3328 "      Last updated on Nov 05, 2026 (12:47 UTC)."
  PAIR r96-fetch vs r90-copy    differing_lines=1   stamp_free_equal=True
  PAIR r96-fetch vs pinned-r97  differing_lines=1   stamp_free_equal=True
  PAIR r96-fetch vs live-now    differing_lines=1   stamp_free_equal=True
  PAIR r90-copy  vs pinned-r97  differing_lines=0   stamp_free_equal=True
  PAIR r90-copy  vs live-now    differing_lines=1   stamp_free_equal=True
  PAIR pinned-r97 vs live-now    differing_lines=1   stamp_free_equal=True
GROUP S616
  r96-fetch L704 "(12:03 UTC)" | r90-copy L704 "(00:37 UTC)" | pinned-r97 L704 "(00:37 UTC)" | live-now L704 "(12:47 UTC)"
  PAIRs: differing_lines = 1,1,1,0,1,1 ; stamp_free_equal=True in every pair
GROUP S623
  r96-fetch L1911 "(12:03 UTC)" | pinned-r97 L1911 "(08:02 UTC)" | live-now L1911 "(12:47 UTC)"
  PAIR r96-fetch vs pinned-r97 differing_lines=1 stamp_free_equal=True
  PAIR r96-fetch vs live-now   differing_lines=1 stamp_free_equal=True
  PAIR pinned-r97 vs live-now   differing_lines=1 stamp_free_equal=True
```

Every differing line printed is of the form `      Last updated on Nov 05, 2026 (HH:MM UTC).`
(the differing line is the *same line number* in both members: 3328 / 704 / 1911).

Byte-level corroboration (independent of line splitting): replacing the single stamp line with a `<STAMP>`
placeholder in each member gives **one** canonical sha per group:

```
GROUP S615 distinct_canon_shas=1 -> BYTE-IDENTICAL APART FROM STAMP   (c97acb8f…2e5e1; CR=0 in all members)
GROUP S616 distinct_canon_shas=1 -> BYTE-IDENTICAL APART FROM STAMP   (fb8d9649…dc94)
GROUP S623 distinct_canon_shas=1 -> BYTE-IDENTICAL APART FROM STAMP   (63381075…040d)
```

**H holds.** No non-stamp line differs in any of the 14 pairs; no member has more than one stamp line;
no CR bytes anywhere.

## 4. Does the tool's stamp regex match those exact lines and nothing else?

* `STAMP_RE` matches **exactly one** line per page (3328 / 704 / 1911) in all 11 inspected files
  (r96 fetches, r90 copies, r97 pins, curl-UA and tool-UA live copies).
* A case-insensitive scan for `last updated` over those 11 files returns **only** the three stamp lines
  (`live-cmdline.html:1451` contains the prose "the updated setting is also seen in subprocesses" — it does
  **not** contain the substring "last updated" and does not match the regex).
* No other `UTC)` occurrence exists in the three live pages — no second stamp-shaped line can hide.
* Regex shape probes (the exact `STAMP_RE` from the tool, this run):

```
MATCH b'      Last updated on Nov 05, 2026 (12:47 UTC).'
MATCH b'Last updated on Nov 05, 2026 (12:47 UTC).'
MATCH b'\tLast updated on Nov 05, 2026 (12:47 UTC).  '
no    b'Last updated on Nov 05, 2026 (12:47 UTC)'          # no trailing period
no    b'Last updated on November 05, 2026 (12:47 UTC).'     # long month
no    b'Last updated on Nov 05, 2026 (12:47 PST).'         # non-UTC zone
no    b'Last updated on Nov 05, 2026 12:47 UTC.'           # no parens
no    b'See Last updated on Nov 05, 2026 (12:47 UTC).'     # not sole content
no    b'      Last updated on Nov 5, 2026 (12:47 UTC).'    # single-digit day
```

So the regex matches the real stamp lines and rejects the near misses; the `time-churn` classification is
earned by the stamp grammar and nothing else.

## 5. Reconstructing the recorded bytes from the live bytes (provenance of the pins)

Substituting the recorded stamp into **today's live** bytes and hashing reproduces the recorded digests exactly:

```
ast       live stamp (12:47 UTC) -> substituted (00:37 UTC) reconstructs recorded digest 7891c588…a42f5 MATCH
tokenize  live stamp (12:47 UTC) -> substituted (00:37 UTC) reconstructs recorded digest 6842ed0f…cb72 MATCH
cmdline   live stamp (12:47 UTC) -> substituted (08:02 UTC) reconstructs recorded digest 90ac3b25…ad0 MATCH
```

Interpretation: since sha256 equality is cryptographic, the r97 pins are **byte-for-byte** the recorded fetches,
and the *only* thing that has changed between the recorded fetch and now is the timestamp string. S623's pin
is therefore a faithful reconstruction, not a stand-in: substituting one line into today's body yields the
recorded digest bit-for-bit. S615's pin is byte-identical to the r90 ast copy (and to S619's recorded digest);
S616's pin is byte-identical to the r90 tokenize copy.

S615's own recorded digest is the known r91 C-1 mis-record (shares a 46-hex-char prefix with the truth, then
diverges: `7891c588…c94b8f1a60ad1a6f0` vs `7891c588…c94b0f83b9a8a42f5`); the digest tool therefore prints
`superseded-by S619` for S615 and `ok` for S616/S623, and the counter's hole guard checks the pin against
S619's `actual=` — satisfied.

## 6. Independent re-measurement of the frozen counters (read-only)

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive e85ed91249953094b067554bfa79fcdc65791f8e | tar -x -C landing
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-97/count-c2.py --root landing
TARGET S615 superseded-by S619 successor_ok=yes copy_equals_successor=yes copy=corpus/evidence/sources-r97/S615.html copy_sha=7891c58897fe9f78
TARGET S616 ok copy_matches_tool=yes copy=corpus/evidence/sources-r97/S616.html copy_sha=6842ed0f53882c5a
TARGET S623 ok copy_matches_tool=yes copy=corpus/evidence/sources-r97/S623.html copy_sha=90ac3b25cb2dd281
LIVE S615 time-churn as-of=2026-11-05T20:53:04Z
LIVE S616 time-churn as-of=2026-11-05T20:53:04Z
LIVE S623 time-churn as-of=2026-11-05T20:53:04Z
LIVE MORI_DRIFT_RECHECK rows=3 adjudicated=3 fresh=0 excerpt=0 time-churn=3 asset-churn=0 receipt-open=0 receipt-stale=0 ua-serving=0 content-drift=0 gate=0 unavailable=0 window=2026-11-05T20:53:04Z..2026-11-05T20:53:04Z
C2=met mismatch=0 unpinned=0 targets_ok=3/3 hole_guard=pass live=S615:time-churn,S616:time-churn,S623:time-churn checks_failed=- root=…/landing
exit=0

$ python3 …/count-c2.py --root entering        # entering rev 973b2af
TARGET S615 unpinned copy=- copy_sha=-   / TARGET S616 unpinned … / TARGET S623 unpinned …
LIVE S615 no-copy / LIVE S616 no-copy / LIVE S623 no-copy
C2=unmet mismatch=0 unpinned=3 targets_ok=0/3 hole_guard=n/a live=S615:no-copy,S616:no-copy,S623:no-copy checks_failed=unpinned,target_S615,target_S616,target_S623,live
exit=1

$ python3 …/count-c1.py --root landing
TARGET tools/mori-cgroup-pressure.py row='cgroup PSI survey (r62 tool, registry r97)' selftest_rc=0 selftest_line='MORI_CGROUP_PRESSURE_SELFTEST: pass=12 fail=0' stated_in_cell=yes token_in_verdict_map=yes
TARGET tools/mori-drift-recheck.py row='drift re-check (r66 tool, registry r97)' selftest_rc=0 selftest_line='MORI_DRIFT_RECHECK_SELFTEST: PASS (10 cases)' stated_in_cell=yes token_in_verdict_map=yes
TARGET tools/mori-scorecard-calibration.py row='SCORECARD Last-change calibration counter (r96 tool, registry r97)' selftest_rc=0 selftest_line='CALIB_SELFTEST pass=11 fail=0' stated_in_cell=yes token_in_verdict_map=yes
TARGET tools/mori-source-digest.py row='SOURCES digest check (r91 tool, registry r97)' selftest_rc=0 selftest_line='DIGEST_SELFTEST pass=11 fail=0' stated_in_cell=yes token_in_verdict_map=yes
C1=met unregistered=0 registry=met targets_ok=4/4 checks_failed=- root=…/landing
exit=0

$ python3 …/count-c1.py --root entering
TARGET tools/mori-cgroup-pressure.py unattributed  (…4 tools…)
C1=unmet unregistered=4 registry=unmet targets_ok=0/4 checks_failed=registry,target_mori-cgroup-pressure.py,… root=…/entering
exit=1

$ python3 landing/tools/mori-gate-registry.py --rev WORK --repo landing --audit-all
registered=65 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0 tables=17
REGISTRY=met
AUDIT_EXIT=0

$ python3 landing/tools/mori-drift-recheck.py --selftest
MORI_DRIFT_RECHECK_SELFTEST: PASS (10 cases)

$ python3 landing/tools/mori-source-digest.py landing/corpus/SOURCES.md landing/corpus/evidence
DIGEST S615 superseded-by S619
DIGEST S616 ok recorded=6842ed0f…cb72 actual=6842ed0f…cb72
DIGEST S619 ok recorded=7891c588…a42f5 actual=7891c588…a42f5
DIGEST S623 ok recorded=90ac3b25…ad0 actual=90ac3b25…ad0
DIGEST_CHECK rows=125 ok=92 mismatch=0 superseded=2 prefix_only=31 unpinned=0
DIGEST_EXIT=1   # exit 1 is the standing 31 prefix_only rows, explicitly out of scope this round
```

Counter bytes were re-hashed and match the contract: `count-c1.py` `78a09016…d2a95`, `count-c2.py` `957a7be6…9a1e91`.

## 7. Divergences found (reported, not patched)

1. **Docstring vs regex (tool `tools/mori-drift-recheck.py:74` vs `:140-142`).** The docstring says the stamp is
   "optionally indented, **with an optional trailing period**", but the regex requires the period (`\)\.`).
   A probe line without the period does not match. Every real docs.python.org render observed here carries the
   period, so this does not affect the three rows — but a future render without it would be classified
   `content-drift` and would trip C2's kill rule. Docs-only defect; the tool is frozen for this round.
   `[INFERENCE]` — no render without the period was observed in any inspected artifact.
2. **Ground citation drift (tool docstring `:75-77`).** The docstring cites `corpus/evidence/sources-r66/S577.html:2638-2639`
   as the ground for the stamp grammar; that file has **zero** `STAMP_RE` matches — lines 2638-2639 are the prose
   description of Sphinx's `html_last_updated_fmt` option ("If set, a 'Last updated on:' timestamp is inserted into
   the page footer"), i.e. it documents the *mechanism*, not an observed stamp instance. The actual observed
   instance is `corpus/evidence/sources-r65/S347.html:3328`, which the regex's own source comment cites and which
   does match the regex (verified this run: 1 match, exact text
   `      Last updated on Nov 01, 2026 (05:22 UTC).`). Provenance is sound via S347; the S577 citation is a
   mechanism citation mis-labelled as a stamp-instance citation.
3. **Stale-by-design exit.** `mori-source-digest.py` exits 1 because of the 31 standing `prefix_only` rows.
   The contract excludes them, and the frozen C2 counter reads only `mismatch=`/`unpinned=` from `DIGEST_CHECK`
   (`count-c2.py:100-108`), so the C2 verdict is unaffected — but "digest gate exit 0" is not achievable without
   touching out-of-scope rows. Noted so no one reads the exit-1 as a C2 failure.

None of these touches the predicate, the pinned bytes, the counters, or the receipts.

## 8. Confidence

* **H holds — high confidence (observed, not inferred).** 14/14 pairs differ in exactly one line; that line is
  always the stamp; canonical-sha equality adds byte-level confirmation independent of line splitting.
* **Regex scope — high confidence.** Exactly one match per file across 11 files; only one "last updated" substring
  per page; nine near-miss probes behave as the regex comment claims.
* **Pins are the recorded bytes — high confidence** (sha256 reconstruction, not resemblance).
* **C1/C2 at the landing revision — high confidence**, counters re-run from the archived tree at the landing rev.
* **Forward risk on the trailing period — medium confidence, `[INFERENCE]`** (never observed without the period).

## 9. Unrun checks

* The r97 controls (`evidence/controls-r97.txt`) were **read**, not re-executed — the control fixtures
  (`c2-hole`, `c2-livebytes`, `c2-contentdrift`) live under `$HYAKU_SCRATCH/mori-r97/controls/`, outside my seat's
  scratch, and re-running them would consume another live fetch round; their recorded outputs are quoted in §6
  only as *read*, not as evidence I produced.
* `mori-scorecard-calibration.py` / `mori-cgroup-pressure.py` / `mori-source-digest.py` selftests were **not**
  re-run by me directly — the C1 counter ran them (`selftest_rc=0` for all four, lines quoted in §6).
* No mutation-testing of the frozen counters was performed by this seat (other wave seats own that).
* `git log/diff/show` beyond `show --stat` of the landing commit was not run; no branch/worktree inspection.

## 10. Verdict lines

`VERDICT C2 holds: the churn hypothesis H is confirmed for all 14 pairs across S615/S616/S623 — every differing line is the single `Last updated on … (HH:MM UTC).` stamp, and the tool's STAMP_RE matches that line and nothing else on the three pages.`

`VERDICT C1 holds: independently re-measured at the landing revision, `C1=met unregistered=0 registry=met targets_ok=4/4` with `REGISTRY=met` and all four selftests exiting 0.`

Report: .ufo/waves/round-97/w1/Mo97RevStamp.md
