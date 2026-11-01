# Round 70 — mori — non-author verifier spotcheck

author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))
round: 70
date: 2026-11-01
entering: `9dc4314d1572fe3e2ae18dd8c9c8f51f1263736f`
landed: `de431a7484f250d46ecd3f6c008524f47134aa1e` (branch tip, pushed)
scope: verify, spot-check, close. No lane-authored file was edited; this file is written
by closure and left uncommitted for the orchestrator. All commands below were run by
closure on this host against committed bytes (`git show`/`diff-tree`/`ls-tree`/index-free
git only; worktree bytes were first verified equal to the landed blobs for every file
re-measured).

## 1. Step-1 conformance — OK

| Check | Command (abbreviated) | Observed | Verdict |
|---|---|---|---|
| Report committed by lane identity | `git -C <fleet> log --format='%an <%ae> %H' -1 -- .ufo/reports/round-70/mori.md` | `mori-shokunin <mori@shokunin.local> 63f4f506` (2026-11-01T12:51:39-08:00) | ok |
| SHONEN heading | read of the report | `## SHONEN` heading present, 4/4 boxes each one `[~]` line with resolvable pointers | ok |
| Cited lane commits exist + ancestral | `merge-base --is-ancestor <hash> refs/heads/master` | `9dc4314d` ok; `de431a74` ok | ok |
| Branch tip pushed | `ls-remote origin refs/heads/master` vs local `rev-parse refs/heads/master` | both `de431a7484f250d46ecd3f6c008524f47134aa1e`, ahead=0 | ok |
| Round work reachable | `diff-tree -r --stat 9dc4314d de431a74` | 24 files, +2740/−3 — matches the report's own count; every path inside the lane repo; none of the six frozen files (SKILL.md, PROVINCE.md, AGENTS.md, corpus/README.md, mori-source-drift.py, mori-drift-adjudicate.py) in the diff | ok |
| Dispatch digest | `grep 'mori round=70' .ufo/watchdog.log` | `11:13:18-08:00 launch mori round=70 base=9dc4314d1572 (zcode run14)`; `12:51:38-08:00 complete mori round=70 head=de431a7484f2 pushed=True` — matches the contract's digest | ok |
| Marker rule | report content | real report: work performed, per-claim before→after with counting commands, checkable commit citations — not a marker | ok |
| Lane commit identity | `log -1 --format='%an <%ae> %H' de431a74` | `mori-shokunin <mori@shokunin.local>` | ok |

## 2. Claim re-checks

Worktree-vs-commit equality was verified by sha256 for every file re-measured or
re-executed (12/12 MATCH: both tools, all three shortwin receipts, both uptime receipts,
both source pins, SOURCES.md, the lesson, the knowledge entry).

### C1 — depth — verified met (re-measured + independently re-run)

- Before: `git cat-file -e 9dc4314d…:.ufo/waves/round-70/evidence/shortwin-b-r70.txt`
  → rc 128 (absent at entering). Re-derived by closure.
- After: `grep -oE "window-s=[0-9]+" shortwin-{a,b,c}-r70.txt | sort -u` → 31, 91, 304.
  `grep -h UA_VARIANCE … | grep -c "per-response=4"` → 1; `per-response=0` → 2. All match
  the report exactly.
- Window derivations verified against S581's documented scale, read in the pinned copy
  (`corpus/evidence/sources-r70/S581.html`): default protection-pack immunity 300 s
  (`:70`), challenge minimum 300 s (`:83`), CAPTCHA minimum 60 s (`:84`), timestamp
  updated on each successful challenge response (`:59-60`). The three computed windows
  are internally consistent with each receipt's own as-of timestamps
  (31 = 19:57:41−19:57:10; 91 = 20:00:04−19:58:33; 304 = 20:07:41−20:02:37) and sit
  below the CAPTCHA minimum (31 s), between the CAPTCHA minimum and the default (91 s),
  and at the default (304 s) — "at and below the documented scale" holds.
- Byte-identity spans verified across receipts: pair A body == pair B capture A
  (`e4bf924c…`); pair B capture B == pair C capture A (`6e7b906d…`).
- Closure's own A/A pair at the stated ~91 s window (same committed tool, same S241 URL,
  same committed r42 pin; captures kept in closure scratch, never committed):
  captures at 2026-11-01T21:05:45Z and 21:07:17Z → computed window 92 s;
  `UA_VARIANCE label=r70-verifier-92s per-response=0 stable=1499 stable-not-in-pin=4 …
  same-bytes=true … window-s=92 … rc=0`, both captures sha256 `066513da…`. Note: the
  served body differs from both round-time bodies (new token bytes since 20:07Z) and no
  rotation was caught in this particular ~91 s window — consistent with the round's own
  finding (rotation is NON-UNIFORM; the claim decides no TTL and names no mechanism), and
  it independently demonstrates the r71 planned item (recurrence is checkable). The
  finding as stated is not contradicted: one 91 s-scale catch, no catch at 31 s, 304 s,
  or closure's 92 s.

### C2 — operability — verified met (re-executed by closure)

- Before: `tools/mori-uptime-win.py`, the knowledge entry and both source pins are new in
  this round's diff (absent from the entering tree; controls receipt shows rc 128 for
  each).
- Selftest ×3 at the committed bytes: `python -I tools/mori-uptime-win.py --selftest` →
  `UPTIME_WIN_SELFTEST: PASS (8 cases)` rc 0, three consecutive runs (grammar,
  unit_math, zero_is_real, honest_unavailable, negative_rejected, noninteger_rejected,
  redaction, uint64_max_rendered).
- Live ×1: `surface uptime: state=ok uptime_ms=489381578 uptime_s=489381 uptime_d=5
  count=biased boot_identity=absent` / `UPTIME_WIN: AVAILABLE surfaces=1 ok=1
  unavailable=0`, rc 0 — same boot window as the round's receipt (486230312 ms at
  20:12Z → 489381578 ms at closure, ≈8.7 h apart, both uptime_d=5); caveats travel on
  the line.
- Truncation arm verified in source: restype pinned `c_ulonglong`
  (`tools/mori-uptime-win.py:107`); selftest arm 8 pins the exact unsigned-64-max
  rendering (`uptime_ms=18446744073709551615`). Nuance (not a defect): the selftest is
  fixture-based, so the pinned rendering proves the render path; the live-read restype
  pinning is the source line — both are disclosed in the tool docstring, and the
  redaction arm rejects extra fixture keys before rendering.
- Receipt-stated tool sha256 `04e437fe…` matches the committed bytes (recomputed).

### SOURCES / frontier — verified

- Row count: `grep -c "^| S" corpus/SOURCES.md` = 353 at `9dc4314d` (re-derived from the
  entering blob) → 355 at `de431a74`. S581/S582 rows sit inside the Registry section
  immediately after S580; both `mined`; quotes ≤25 words; anchors name the pinned copies.
- Pinned copies: S581 sha256 `5e5b941e…` 16179 bytes, S582 sha256 `580f1935…` 52661
  bytes — both recomputed and matching the rows.
- Live re-open (closure fetch, 2026-11-01T21:1xZ): both URLs refetched; each live body
  is BYTE-IDENTICAL to its pin (sha256 equal), and every quoted sentence was found in the
  live pages.
- Census: closure ran `sources-census.sh validate --root <fleet> mori` → `mori ok`, exit
  0, tolerated W04 duplicate-URL class only (same 31 pre-existing rows as the committed
  start/end receipts).
- Append-only gate receipt: `round_changed=[]` (no round-scoped violations; the 50
  historical ids unchanged), matching the report.

### Fresh-start duty — verified

- Closure re-ran the frozen r61 counter at the r61 data tip:
  `python -I .ufo/waves/round-61/count-c2.py 986d4b46db6e67682ef84091f606d125f987ecbc`
  → `C2=unmet pointers=47 rows=47 same=30 moved=3 changed=0 quotes_ok=33 spans_ok=33
  sources=5 failed=quote_words:…` rc 1 — byte-identical to the freshstart receipt.
- r59/r60/r61 revs and fleet report commits: receipted PRESENT/ancestral, including the
  corrected lane-side `7370a731` (see Mistakes).

### Four mined mistakes — each verified in the disclosed artifacts

1. Placeholder digest from memory: the entry's `source:` carries the correct
   `580f1935…`; the wrong placeholder `6a2c15b3` appears exactly ONCE in the landed tree
   (`git grep` over `de431a74`) — inside the lesson's own disclosure row. Nothing cites
   the wrong value. Consistent with the disclosure.
2. Wrong-repo existence check: the freshstart receipt carries the original
   `7370a731: ABSENT` line (fleet-side section) AND the explicit correction line naming
   the checkout error and the lane-side re-check (PRESENT, ancestor rc 0). Not a silent
   rewrite.
3. Mis-transcribed receipt header: the committed controls receipt's last command header
   spells `corpus/QUALITY.md`, and closure's independent re-run
   (`git show 9dc4314d:corpus/QUALITY.md | grep -c '^161\.'`) gives rows=1 rc 0 — the
   header now matches the output rows.
4. Duplicated edit: mechanical check over the committed lesson (all lines >60 chars,
   `sort | uniq -d`) → zero duplicates; full read is clean. The committed bytes carry the
   clean rewrite only.

## 3. Discernment spot-check (non-author)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S581 (AWS WAF token immunity times) | admit, tier A docs, mined | URL refetched by closure; live body byte-identical to pin (`5e5b941e…`); scale sentences found at `:70/:83/:84` | agree | Official vendor docs; teaches the documented clock scale the C1 windows probe; anchored and byte-pinned. |
| S582 (GetTickCount64) | admit, tier A docs, mined | URL refetched by closure; live body byte-identical to pin (`580f1935…`); definition sentence found at `:829` | agree | Official API docs; grounds the new capability; caveats (:841/:842 text) are real and travel on every receipt line (pointer drift defect below). |
| Reject sample: the no-TTL-decision boundary on C1 | reject (of the overreach reading) | S581 `:59-60` mechanism sentence re-read in the pinned copy | agree | The documented mechanism describes challenge-response timestamp updates, which this client never performs; reporting observed non-uniformity without asserting cause is the correct boundary. Correctly refused. |

Note: the lesson's Gate records its S582 pre-row sweep as "`sysinfoapi` 0" but the
receipt (primary evidence) records `rows=1 rc=0` — see defect D2; the
page-identifying `gettickcount64` sweep is 0, so the admit decision itself stands.

## 4. Per-axis verdicts (closure)

| Axis | Verdict | Basis |
|---|---|---|
| depth | improved | C1 re-measured and independently re-run at the stated window; receipts, pin and scale verified. |
| operability | improved | C2 re-executed: selftest 8/8 ×3, live rc 0; truncation and redaction arms verified in source. |
| freshness | unchanged | No freshness claim; standing battery receipt (12/12, 10/10, 16/16, 125/125, 5/5, 10/10, 14/14) on unchanged bytes; frozen set absent from the round diff. |
| coverage | unchanged | No coverage claim; the surface gain is recorded as capability + entry; PROVINCE head byte-frozen (untouched in the diff). |
| calibration | unchanged | Window grammar applied, not extended; the overreach reading was declined (spot-check above); the located-quote drift (D1) is an evidence-hygiene defect, routed — not a calibration move. |
| adjacency | unchanged | No sibling surface touched; boot-state diagnosis stays tsukuroi/operator in the entry's Boundaries; appendonly gate `round_changed=[]`. |

No axis harmed: SCORECARD diff is +49/−0 (append-only at EOF; the axes table bytes are
untouched); SHONEN marks stayed `[~]` (3 evidence lines updated only).

## 5. Trend verdicts (closure)

- expansion: improved — SOURCES 353→355, both rows opened/pinned/mined this round
  (re-opened byte-identical by closure); one capability demonstrated and entered the
  repertoire table in the same round; both claims carry falsifiable before→after data.
- quality: improved — C1 adds stated-window receipts at new scale points with an honest
  non-uniformity result; C2's caveats travel on its output line; standing battery green
  on unchanged bytes; the four defects were caught before landing and mined. The landed
  located-quote drift (D1) is routed below, status-neutral — no entry was found false
  and left unmarked.
- discernment: improved — the no-TTL/no-mechanism boundary was applied against the
  tempting reading of its own best data (spot-checked above, agree); eight fresh-start
  rule-outs with reasons; four mistakes mined with captured-by and fix, each verified in
  the disclosed artifacts; the L0 lines were re-verified unanswered and routed around.

## 6. Routed defects (lane must fix in round 71; corrections are new entries, never in-place rewrites)

- D1 (reference-drift, evidence-standard "a quote names its location"): the S582
  located-line pointers are off against the pinned copy. Actual lines in
  `corpus/evidence/sources-r70/S582.html`: "The number of milliseconds." is at `:834`
  (stated `:833`); the working-state QueryUnbiasedInterruptTime sentence is at `:841`
  (stated `:842`); the debug-build ~49-day note is at `:842` (stated `:845`). S581's
  pointers (`:54/:59/:70/:83/:84`) are exact. The drift appears in
  `.ufo/waves/round-70/evidence/source-s582-r70.txt`, the S582 SOURCES row anchor, the
  lesson Gate, the knowledge entry K2/K4/K5, and the fleet report. The quoted texts are
  real and verified; only the stated locations drift. Fix next round as an erratum/new
  rows naming the superseded pointers.
- D2 (number-drift): the lesson Gate records the S582 `sysinfoapi` pre-row sweep as 0;
  the receipt (and closure's re-derivation at the entering rev) record rows=1 rc=0 —
  the S574 row (GlobalMemoryStatusEx, same sysinfoapi tree). The page-identifying
  `gettickcount64` sweep is 0, so the no-duplicate decision stands; the lesson prose
  mis-states the receipt. Correct in the next lesson with old→new.
- Nit (status-neutral): the report describes the census receipts as "command + rc
  embedded"; the committed receipts carry only the validator output (`mori ok …`), no
  explicit command/rc line. Closure re-ran the validator itself (exit 0), so the census
  requirement is met regardless.
- Nit (status-neutral): SHONEN box 3's updated evidence line runs the r70 and r69
  battery references together without a separator ("…selftests-battery-r70.txt`
  round-69 standing battery…"); both pointers resolve.

## 7. Verdict

All declared claims verify (C1 re-measured + independently re-run; C2 re-executed);
no axis is harmed; conformance is clean; the defects above are named, status-neutral,
and routed. Round 70 is **admitted** (lanes.mori = ok). SHONEN boxes remain `[~]`;
as non-author, closure executed the box-3 instructions (new tool selftest ×3 + live;
battery receipt verified) and the box-2 evidence (C1/C2 LOG entry + receipts); a
promotion review could check all four boxes against this file.
