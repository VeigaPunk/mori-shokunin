# Round 65 — mori verifier spotcheck (closure)

author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))

Round: mori lane-round 65. Entering `7d369cd26d0ec697f5b734fd63fa4aba8fdc7891`, landed tip
`73a57b8102f28300dee0b9533e29481a566032a3` (branch tip, pushed). All git work in this file used
index-free commands only (`rev-parse`, `cat-file`, `ls-tree`, `diff`, `diff-tree`,
`merge-base --is-ancestor`, `show`, `log`, `ls-remote`, `grep`); no mutating git command was run
anywhere. Verifier live fetches were read-only GETs into a verifier scratch dir outside the lane
repo; cited evidence is committed bytes, re-runnable commands, or re-opened URLs.

## 1. Step-1 conformance

| Check | Command (abbreviated) | Observed | Verdict |
|---|---|---|---|
| Report committed in fleet repo by lane identity | `git -C <fleet> log --format='%an <%ae> %H' -1 -- .ufo/reports/round-65/mori.md` | `mori-shokunin <mori@shokunin.local> 758f18e0b641911112d8578d0b47f1ba22b846f9` | pass |
| `SHONEN` heading | read of the report | `## SHONEN`, 4/4 boxes `[~]` each with a resolvable pointer | pass |
| Cited lane commits exist and are ancestral | `merge-base --is-ancestor <c> refs/heads/master` for `7d369cd26d0e…`, `40c192e74e9a…`, `711067078883…`, `73a57b8102f2…` | all four ancestral, rc 0 each | pass |
| Branch tip pushed | `rev-parse refs/heads/master` vs `ls-remote origin refs/heads/master` | both `73a57b8102f28300dee0b9533e29481a566032a3` | pass |
| Round work reachable in range | `git log 7d369cd2..73a57b81` | exactly the three helper commits (`40c192e7` data, `71106707` evidence+re-pins, `73a57b81` freshstart+lesson-4); `diff 7d369cd2 73a57b81 --stat` = 32 files, +26279/−3 — matches the report | pass |
| Dispatch evidence | fleet `.ufo/watchdog.log` | `2026-10-31T23:23:59-07:00 launch mori round=65 base=7d369cd26d0e` and `2026-11-01T00:51:44-07:00 complete mori round=65 head=73a57b8102f2 pushed=True` — matches the closure digest | pass |
| Prompt committed | `git -C <fleet> log -1 -- .ufo/prompts/mori-round-65.md` | committed (`94eba49b`, "round-65: mori dispatch evidence") | pass |
| Marker predicate | content read | real report: work performed, evidence pointers, per-claim before→after, cited lane commits that exist — not a marker | pass (status `ok`) |

## 2. Claim re-checks

### C1 — freshness: per-row disposition of the 23 r64 drift findings — RE-MEASURED, verified

Before, re-derived at `7d369cd2` (my commands over committed bytes):
`git ls-tree -r 7d369cd2 --name-only | grep -c round-65` = 0; `… | grep -c sources-r65` = 0;
`git cat-file -e 7d369cd2:tools/mori-drift-adjudicate.py` rc 128. The controls receipt
(`.ufo/waves/round-65/evidence/controls-r65.txt`) agrees: SOURCES 348, r64 sweep state
`drifted=23`, adjudicator absent.

After, re-derived at `73a57b81`:
- `git show 73a57b81:.ufo/waves/round-65/evidence/disposition-semantic-review-r65.txt | grep -c "^S"` = 23.
  Tally line: KEEP-C 5 (S156–S160) · KEEP-A 2 (S572 S573) · KEEP-CHROME 1 (S241) ·
  GATE+KEEP-CHROME 1 (S262) · REPIN 14 (S175 S176 S177 S206 S209 S210 S223 S226 S227 S228 S229
  S230 S231 S347); unclassified 0. Every REPIN names its diff, its teaching-anchor verification,
  and its new sha; every KEEP names its renewed evidence.
- Post-disposition sweep receipt (`evidence/drift-live-post-r65.txt`):
  `MORI_SOURCE_DRIFT rows=349 fresh=70 excerpt=0 drifted=9 unavailable=2 no-copy=268` rc 1 — the
  honest remainder; the 9 drifted rows are exactly the 9 KEEP-class rows
  (receipt-shape 5, UA-serving 2, chrome 1, gate 1).

Re-pin integrity — ALL 14 re-pins checked (the contract asked for ≥2): for each of the 14 files in
`corpus/evidence/sources-r65/`, `git cat-file blob 73a57b81:<path> | sha256sum` equals the
semantic-review receipt's `new pin` sha256 AND the refetch receipt's (`evidence/disposition-refetch-r65.txt`)
`curlsha=` digest for that row; byte counts equal the receipts' values. 14/14 exact matches —
zero silent re-pins confirmed (14 re-pins + S576 = the 15 committed copies).

Verifier live re-fetches (read-only, later on 2026-11-01):
- S230 (REPIN): live body sha256 `a0a069f2757da8391bcb4fbed2fc3415b444d2d6467b534cba73c7141ba9d79e`
  == committed re-pin == receipt digest. Byte-identical today.
- S223 (REPIN, the real-content row): live body differs from the committed re-pin by exactly ONE
  line — the docs.python.org page-generation stamp ("Last updated on Nov 01, 2026 (05:22 UTC)" →
  "(07:39 UTC)"); teaching anchors `redirect_request` 2==2, `301` 7==7 in both; the new paragraph
  "Exceptions raised while reading or parsing an HTTP response are not wrapped in URLError and
  propagate unchanged." is verbatim in the pinned body at the insertion point. The re-pin and its
  disposition are sound; the post-round delta is template chrome.
- S572 (KEEP-A): live curl-default-UA fetch sha `3f2fd8a26e9258ecb8e5456819992338a96343adb456affc248fe56892f71bf6`
  == the r63 pin == receipt; live tool-UA fetch differs (bytes 62249). KEEP-A confirmed live under
  both UAs. (The tool-UA digest differs from the round's tool-UA digest — the vendor serves
  variable tool-UA bytes; the class claim "curl-UA == pin, tool-UA differs" holds.)
- S156 (KEEP-C): live raw body sha256 `b56aa781be9c29b610156925030d3c4ab720c0ad73d57907d230ca3047302f2a`
  == the receipt's recorded opening sha; 17,973 B == the row's recorded size. The r30 excerpt
  receipt's header still matches today's body — KEEP-C confirmed live.

Nit (status-neutral, routed): the report's second C1 counting command
`grep -c " drifted" .ufo/waves/round-65/evidence/drift-live-post-r65.txt` yields 10, not 9 — it
counts the 9 row lines plus the summary line. The authoritative 9 is the summary line's `drifted=9`.

### C2 — depth: the drift-adjudicator capability — RE-MEASURED + evidence-verified, verified

- Frozen-bytes checks (the round-note requirement): `tools/mori-source-drift.py` blob
  `1c6b437fae185b325e746c40b3f0c556bcb8274d` identical at base and tip; `SKILL.md` blob
  `65966b34c585ef28b8a435b777b03efa1290fc45` identical at base and tip; the SKILL:905 tally pin
  (`MORI_SOURCE_DRIFT_SELFTEST: PASS (6 cases)`) reads true from the committed bytes; the r38
  content anchors (`FETCH_MAX_BYTES = 4 * 1024 * 1024`, `if not _public_redirect_target(final):`,
  `return "drifted"`) all occur in the frozen tool bytes, so the anchor binding is intact.
- Selftest, verifier's own runs (worktree verified byte-identical to the tip for both tools,
  SOURCES.md, and all 15 pinned copies before executing): two runs of
  `python tools/mori-drift-adjudicate.py --selftest` → `MORI_DRIFT_ADJUDICATE_SELFTEST: PASS
  (5 cases)` rc 0 both. Committed receipt (`evidence/adjudicate-selftest-r65.txt`): 5/5, two
  dedicated runs identical, plus 3/3 in the battery (`evidence/selftests-r65.txt`) — consistent.
- Live `--only`, verifier's own run of the committed receipt's exact command at the tip: rc 0,
  `rows=23 adjudicated=17 passthrough=6 receipt-open=5 receipt-stale=0 ua-serving=2
  content-drift=9 gate=1 unavailable=0`. Token-level agreement with the committed receipt
  (`evidence/adjudicate-live-r65.txt`, measured 07:06:39Z) on 15/23 rows; the 8 docs.python.org
  re-pins (S176 S177 S223 S226 S228 S229 S231 S347) classify `content-drift` in my later run
  because the vendor rebuilt those pages after the round's fetch (my S223 diff pins the delta to
  the single page-stamp line; S230's 3.13 page was not rebuilt and stays `pass-through fresh`).
  This is time-of-measurement sensitivity of an hourly-regenerated template, not a defect in the
  committed evidence — and it is exactly the tool's disclosed boundary (byte-level truth;
  semantic-review classifies the changed bytes). The committed receipt's 23/23 agreement with the
  manual dispositions stands at its measurement time: adjudicated=9 = KEEP-C 5 + KEEP-A 2 +
  content-drift 1 (S241) + gate 1 (S262), passthrough=14 = the re-pinned rows.
- Capability row present in SCORECARD capabilities table, first-working round 65, evidence
  pointer resolves (this verifier executed both cited commands).

### Carry-in 1 — r64 LOG correction is an append, not a rewrite — DIFF-VERIFIED

`git diff 7d369cd26d0e 73a57b8102f2 -- LOG.md` = +117/−0 (pure append). The correction is a
bracketed appended block in the r64 entry's tail; no prior-entry line was touched. Substance
confirmed at base: the r64 LOG entry says "Mistakes mined: three" while
`corpus/lessons/round-64.md` carries 4 numbered mistake rows, the fourth being the S575 quote
word-count — exactly what the appended correction names. The round's −3 deletions are the SHONEN
evidence-line replacements, not LOG.

### No axis harmed

`diff-tree -r -p 7d369cd2 73a57b81 -- SCORECARD.md` = pure append (+67/−0): the Round-65 section
with the two claims and the capability row; scores held 6/7/5/5/5/6, no scalar claimed. Standing
selftests green in the committed v2 battery (register 12/12, settlement-scan 10/10, vote-bind
16/16, pin-check 125/125, drift 6/6 ×3, adjudicator 5/5 ×3, runway 9/9, all rc 0, with the
degraded-loopback-transport condition disclosed). No owned axis harmed.

## 3. Discernment spot-check (non-author)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S576 admit (OpenAlex work-object docs) | row admitted, `mined`, tier A | live GET `https://docs.openalex.org/api-entities/works/work-object`; sha256 of my fetch `4671f96d60872768fb0caa4f50e981fd559a3213e94a40bee496027cf66876d9` == committed pin `corpus/evidence/sources-r65/S576.html`; quote at `:62` verbatim, 15 words; `abstract_inverted_index` heading at `:61` | agree | The page teaches exactly what the row and the S262 disposition need (abstract ships as inverted index; `updated_date` a shared record attribute); byte-identical pin; quote ≤25 words and located |
| Reject-class: work-fields page given no row | not rowed | live GET `https://docs.openalex.org/api-entities/works/work-fields` | agree | Page carries no `abstract_inverted_index` content and its own text defers the attribute docs ("documented once" elsewhere) — it does not teach the ground; declining the row is correct curation |
| Fresh-start reject-class: r61 honest stop re-derived | r61 C2 stands unmet | verifier re-ran `python .ufo/waves/round-61/count-c2.py 986d4b46db6e67682ef84091f606d125f987ecbc` | agree | Same verdict `C2=unmet` with the identical 14 `quote_words` anchors as the round's receipt (`evidence/freshstart-spotchecks-r65.txt`) — the round re-opened the counter rather than citing it |

Census: verifier ran `bash <fleet>/scripts/sources-census.sh validate --root <fleet> mori` — rc 0,
final verdict `ok`, only the tolerated W04 duplicate-URL class (31 rows). The fleet-root
`mori-shokunin` entry is an NTFS junction to this lane repo, so the validator reads the lane's
live tree (r64 D6 precision note holds). SOURCES 348 → 349 with only the S576 row added
(diff-verified; no cell edits).

## 4. Per-axis verdicts (agrees with the closure JSON)

| Axis | Verdict | Basis |
|---|---|---|
| freshness | improved | C1 verified: 23/23 findings dispositioned with two-UA receipts and named diffs; 14 loud re-pins (14/14 sha-verified by this verifier); S241's r64 class-B misreading corrected against the bytes; sweep re-run to a receipted honest remainder |
| depth | improved | C2 verified: the capability runs — verifier's own selftest 5/5 ×2 rc 0 and own live `--only` rc 0; live-run agreement with the manual dispositions; frozen module, SKILL tally pin and r38 anchors all intact |
| coverage | unchanged | no new province surface; the disposition writes stayed inside the lane's own corpus/evidence store |
| operability | unchanged | all standing selftests green in the committed v2 battery; the new tool's selftest and live mode verified executable (counted under depth's claim; no separate operability move declared) |
| calibration | unchanged | honest disclosures (v1 receipt discarded, transport degradation, guard-wiring open) are good practice but no calibration axis-move was declared; no score claimed |
| adjacency | unchanged | disposition wrote only lane-owned pinned-copy store and receipts; S262 gate behavior reported, not normalized; no sibling surface touched |

## 5. Trend verdicts (verifier's, using the four words)

- expansion: improved — the drift-adjudicator capability row entered the table with a passing
  demonstration this verifier re-executed; SOURCES 348 → 349, one tier-A `mined` row (S576,
  re-opened byte-identical by this verifier).
- quality: improved — the 23 findings moved from provisional classes to receipted per-row
  dispositions (re-pin integrity 14/14 sha-verified, S223 content verified at paragraph level,
  S156/S572 keeps confirmed live); the S241 correction chose the bytes over the earlier reading;
  the sweep re-run to a receipted honest remainder.
- discernment: improved — the round's Gate decisions survive this non-author spot-check (1/1
  admits, 1/1 reject-class re-opened, fresh-start counter re-derived with identical output);
  four mistakes mined with captured-by and fix; the degraded-transport finding disclosed and
  routed to L0 (line present at `<fleet>/.ufo/l0-questions.md`, `mori | round-65`) rather than
  patched; the guard-wiring planned item reported open, not claimed.

## 6. Routed defects / notes for the operator (all status-neutral)

1. C1 counting-command nit: `grep -c " drifted"` on the post-sweep receipt counts 10 (9 rows +
   the summary line); the claimed 9 comes from the summary token. Prefer a row-line-isolating
   count next time the receipt is cited.
2. `census-start-r65.txt` / `census-end-r65.txt` record the validator output but no explicit rc
   line; the report's "rc 0 at both ends" is confirmed by this verifier's own run (rc 0) but the
   receipts themselves should carry the rc line they cite.
3. Time-of-measurement observation for r66: hourly-regenerating vendor template pages
   (docs.python.org class) re-drift within hours of a re-pin — 8 of the 14 re-pins already
   classify `content-drift` again on a same-day re-run (delta: one page-stamp line). Strengthens
   the round's own planned r66 item: a standing adjudicate step after every sweep, and a
   convention that re-pins of this page class certify a moment, not the day.
4. SHONEN note for the operator: all four boxes are `[~]` (asserted-by-author, correct for a
   non-promoted lane) with resolvable pointers, and each looks checkable by a non-author
   (decision tables present; end-to-end tasks logged with receipts; selftest instructions were
   executed by this non-author verifier for the new tool; write scope stayed in-repo per the
   diff file list). Per protocol only a non-author may write `[x]` — operator's call, not
   exercised here.
5. L2 dispatch: no AgentSwarm surface on this host; the round ran L1-only and claimed no
   wave-based evidence; the disclosure and the carried L0 line are present. Round numbers are
   consistent everywhere inspected (report, LOG, SCORECARD, lesson, receipts, commits).

Verdict: every declared claim verifies against committed bytes and live re-measurement; no axis
is harmed; the round is admitted.
