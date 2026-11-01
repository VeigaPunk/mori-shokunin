# Round 70 — mori (L1 MoriR70): C1 depth verified met (the short-window rotation-bound receipts: at computed windows 31 s / 91 s / 304 s the observed per-response rotation is non-uniform — caught within the 91 s window, absent within 31 s and 304 s — sourced S581, the documented immunity-time scale, no TTL decided); C2 operability verified met, sourced S582 (capability acquisition `tools/mori-uptime-win.py`, the Windows host-uptime read, `count=biased boot_identity=absent` traveling on every receipt line)

author: mori L1 (MoriR70)
round: 70
date: 2026-11-01
entering: `9dc4314d` (`9dc4314d1572fe3e2ae18dd8c9c8f51f1263736f`, r69 verifier spotcheck tip)

## Fresh start (r59–r61 rejected closures re-read; what was ruled out)

The §7 digests name r59/r60/r61 `rejected-honest-stop`. Spot-checks re-run this
round with own receipts, not cited from r69
(`.ufo/waves/round-70/evidence/freshstart-spotchecks-r70.txt`): the frozen r61
counter re-derived at the r61 data tip (`python .ufo/waves/round-61/count-c2.py
986d4b46…` → `C2=unmet` rc 1, `failed=quote_words:…` ×14 — the same verdict the
r61 closure and the r65–r69 re-derivations reached); the r59 entering/data revs
(2b9f0397/7b86704d), r60's entering/data revs (ddfb12fb/6752eafd) and r61's
entering/freeze/data tips (325f7e63/7370a731/d21c0e5c) all `cat-file -e` PRESENT
and `merge-base --is-ancestor` of refs/heads/master rc 0 each; the three fleet
report commits (2807c6ab, eeedfd53, 3bb9b8e7) PRESENT in the fleet repo.

Ruled out as r70 claims, and why:

1. Re-declaring the r59/r60/r61 entry-claims-class instruments — their
   met-flip counterexamples stand on frozen bytes (re-derived unmet again this
   round, receipt above).
2. Scalar score moves — no closure states a new number and no lane convention
   licenses an L1-authored scalar; the head axes table stays untouched
   (append-only SCORECARD, the r69 closure's own check).
3. Claims on the old Linux host's live surfaces — absent here, honestly
   `unavailable` (the Round-62 host note stands).
4. Editing the frozen bytes (SKILL.md, `tools/mori-source-drift.py`,
   `tools/mori-drift-adjudicate.py`, PROVINCE.md, AGENTS.md, corpus/README.md)
   — the SKILL:905 tally pin and the r65–r69 receipts bind those bytes; this
   round's diff contains none of them.
5. A bare re-run of the standing sweep/re-check/separation work (the r64–r69
   admitted moves) — the full sweep was last adjudicated r66, S572/S573 were
   last dispositioned r65 (same day), so a re-run would re-declare admitted
   work, not move an axis.
6. A third churn grammar for the vendor's serving — r67's ruling stands; the
   r70 receipts observe rotation at new window scales and teach no grammar
   (QUALITY 159 untouched: no row re-classed, no grammar taught).
7. A live observation of the cross-check arm's inconsistent branch (the r69
   planned note) — the vendor's serving arms decide that; the arm stays a
   standing one that fires only if the two sides ever disagree. Cannot be
   manufactured honestly, so not declared.
8. A boot-identity read for the uptime surface — the API returns none and the
   province refuses boot-state diagnosis (tsukuroi); the claim stays inside
   `uptime + biased-count caveats` and prints `boot_identity=absent` on every
   line.

All declared claims are unreachable by a do-nothing round
(`.ufo/waves/round-70/evidence/controls-r70.txt`: every r70 receipt, tool,
entry and source pin absent at entering rc 128; SOURCES 353 rows at entering
with zero rows matching either new URL; `corpus/lessons/round-70.md` absent
rc 128).

## Gate

Two sources opened this round, each fetched with `curl -sS -m 60 -L` into the
lane pin store, duplicate sweeps run INTO the receipts first (the r69 lesson's
rule, applied from the start this round):

- S581 AWS WAF "Setting timestamp expiration and token immunity times" —
  https://docs.aws.amazon.com/waf/latest/developerguide/waf-tokens-immunity-times.html
  — opened 2026-11-01T19:52:49Z — quotes (`S581.html:54`, 10 words): "This
  section explains how challenge and CAPTCHA timestamps expire."; mechanism
  (`:59-60`, 19 words): "AWS WAF records a successful response to a challenge
  or CAPTCHA by updating the corresponding timestamp inside the token.";
  scale (`:70-71`, 15 words): "The default protection pack (web ACL) setting
  for both immunity times is 300 seconds."; floor (`:83-84`, 11 words): "The
  minimum value for the challenge immunity time is 300 seconds."; CAPTCHA
  floor 60 seconds (`:84`). Copy `corpus/evidence/sources-r70/S581.html`
  sha256 `5e5b941e97c0aa6e2d7bd958bdc66a6fbb2a260508880e99becda543e71fc865`
  (16179 bytes). Sweeps: `waf-tokens-immunity-times` 0, `token immunity` 0,
  `immunity` (case-insensitive) 0 — receipted INSIDE
  `.ufo/waves/round-70/evidence/source-s581-r70.txt` before the fetch. The
  row lands `mined`, used-by this lesson (C1's window work).
- S582 Microsoft Learn "GetTickCount64 function (sysinfoapi)" —
  https://learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/nf-sysinfoapi-gettickcount64
  — opened 2026-11-01 — quotes (`S582.html:829`, 14 words): "Retrieves the
  number of milliseconds that have elapsed since the system was started.";
  `:833` "The number of milliseconds."; `:836` resolution "typically in the
  range of 10 milliseconds to 16 milliseconds"; `:842` (20 words): "To obtain
  the time the system has spent in the working state since it was started,
  use the QueryUnbiasedInterruptTime function."; debug-build ~49-day shift
  note `:845`. Copy `corpus/evidence/sources-r70/S582.html` sha256
  `580f1935fb47b5c992a48d22299f7452aaeb00099f2ac96ba74c92002a18277f` (52661
  bytes). Sweeps: `gettickcount64` 0, `sysinfoapi` 0 — receipted INSIDE
  `.ufo/waves/round-70/evidence/source-s582-r70.txt` before the fetch. The
  row lands `mined`, used-by `corpus/knowledge/uptime-win-r70.md` (C2's
  entry).

Both rows appended INSIDE the Registry section immediately after S580 (the
r68 sectioned-append rule applied from the start; position verified by the
end validator run). SOURCES row count 353 → 355 counted by
`grep -c "^| S" corpus/SOURCES.md`.

reject sample: the no-TTL-decision boundary was applied against the
tempting-to-overreach reading of C1 — the receipts catch rotation within 91 s
while the documented challenge floor is 300 s, and the claim names that
tension WITHOUT asserting the documented machinery produced the rotation (the
client answers no challenges; S581's mechanism sentence describes
challenge-response updates, which this client never performs). What is
claimed: the observed non-uniformity at documented scale points, nothing
about cause.

## Mistakes

1. class: calibration (a citation drafted with a digest typed from memory) —
   the uptime knowledge entry's `source:` header was first written with a
   sha256 typed from working memory as a placeholder (`6a2c15b3…`), while the
   real pin digest is `580f1935…`
   (`corpus/evidence/sources-r70/S582.html`, receipt
   `.ufo/waves/round-70/evidence/source-s582-r70.txt`). captured-by: the
   verify-before-land re-read — the entry's digest was greped against the
   receipt's own sha line before anything cited it and it did not match; the
   entry was fixed in place within the minute, before SCORECARD/LOG/commit.
   Nothing ever cited the wrong value. fix: the working rule is now: a
   digest is PASTED from the receipt's own `sha256sum` line into any Write
   payload at write time, never typed from memory — a drafted citation is
   already a claim once it exists in the tree, and a placeholder digest is a
   fabricated one wearing a wait-queue.
2. class: verification (an existence check run against the wrong repo) — the
   fresh-start receipt first recorded `7370a731: ABSENT` under the FLEET
   repo: the r61 freeze commit is LANE-side (the r61 report header says so),
   and the check had been applied in the wrong checkout. captured-by: the
   receipt line itself — "ABSENT" next to a sha the r61 report names as a
   freeze pin contradicts the report being real, so the line was re-derived
   against the lane repo (PRESENT, ancestor rc 0) and the receipt carries an
   explicit correction line rather than a silent rewrite. fix: an absent-sha
   verdict names the checkout it ran in; a sha named by a report is
   re-looked-up in the repo that report names before "absent" is written.
3. class: landing (a receipt header transcribed the wrong file) — the
   controls receipt's last command header printed
   `git show <entering>:corpus/SOURCES.md` while the executed command read
   `corpus/QUALITY.md` (the control is QUALITY 161's row count).
   captured-by: re-reading the receipt before landing — a reader re-running
   the printed command would have counted a different file. fixed in place
   (the header now spells the file actually read); the output rows were
   correct throughout. fix: the printed command line in a receipt must be
   the command that ran — copy it from the invocation, not from memory.
4. class: landing (a lesson edit duplicated its own sentences) — the fix-up
   edit for mistake 3 was applied against a stale match in the author's
   context and inserted a duplicate copy of the block's middle sentences
   (including the stray `captured-by` line-wrap), caught on the immediate
   re-read of the block before anything else consumed it; the committed
   bytes carry the clean rewrite only. captured-by: the same read-back rule
   as mistakes 1–3 — a file that was just edited is re-read in full before
   it is counted landed. fix: edits to prose blocks are verified by reading
   the whole block, not by trusting the edit tool's success report; the
   same discipline that caught the placeholder digest caught this.

## Wave

None — no dispatch surface on this host (carried disclosure; the mori
round-62/round-65 L0 lines stand open — re-verified unanswered this round in
`.ufo/waves/round-70/evidence/l0-considerthese-r70.txt` — routed around,
never treated as answered). Round 70 ran L1-only over committed bytes, this
host's network and this host's own surfaces; no wave-based evidence is
claimed.

## Assimilation

considerthese mined (2026-10-19…2026-10-26, all eight files; no newer file
exists — checked this round, receipt
`.ufo/waves/round-70/evidence/l0-considerthese-r70.txt`): the 2026-10-26
suggestion 1 (split pin-check mismatches into "can't run here" vs "stale")
remains the one still-unimplemented proposal and remains behind the
operator's open instrument-change ruling (the mori | round-65 L0 line);
suggestions 2–4 stay proposals (suggestion 3 is the standing fresh-start
spot-check practice, re-performed this round). Assimilation: none —
shokuknow unreachable.
