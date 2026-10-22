# Routed R1 (wave 2) — tip-receipt plan, seat ReviewTipReceiptPlan

Verdict: **agree** — the routed R1 plan (`.ufo/waves/round-30/w1/TipReceiptsR1.md`) is correct on both asked
points; I independently reproduced its `met`/`unmet` checker results on the surviving mock commits, and the
contract's counters list has no extra script. One naming trap and two residuals noted below.

## 1. What `check-tip-receipts.sh <tip> 30` actually requires

Derived from `.ufo/waves/round-28/check-tip-receipts.sh` (101 lines, read in full):

- Measured revision `P` = full 40-hex **first parent** of `<tip>` (`:40-41`; rationale comment `:14-16`).
- Counter set = `grep -oE 'count-[a-z0-9-]+\.sh'` over `.ufo/waves/round-30/contract.md` **at `<tip>`**,
  `sort -u` (`:43-45`). Contract must exist at `<tip>` (`:43`).
- Candidate receipts = every path under `.ufo/waves/round-30/evidence/` in the tree at `<tip>` (`:46-47`).
- A receipt satisfies a counter iff its body (a) contains the counter script name (`:62`), (b) contains the
  40-hex `P` (`:63`), (c) has a line matching `^exit: *[0-9]+` (`:64`), (d) has ≥3 non-empty lines (`:65`).
  First matching candidate in sorted order wins (`:66`).
- The receipt's **basename** must occur as a substring in `LOG.md` + `corpus/lessons/round-30.md`
  concatenated **at `<tip>`** (default reports `:38`; concat `:48-51`; citation test `:69-70`). Missing
  receipt or uncited receipt ⇒ `rc=1` (`:70,:77`).
- The retention scan is a **hard-coded fourth requirement**, not derived from the contract: a receipt whose
  body contains `mori-retention-gate.py`, `P`, an `exit:` line, ≥3 lines (`:80-88`, name test `:83`), basename
  cited the same way (`:90-91`, missing `:98`).
- All hits ⇒ prints `tip_receipts=met`, exit 0 (`:100-101`).

Note the checker never greps a header line as such — the "header" matters only because it carries `P` and the
operation name into the body.

## 2. Answer: exact file names and receipt header

Given the premise (LOG.md and the lesson at the tip name `tip-c1.txt`, `tip-c2.txt`, `tip-retention.txt` —
verified: `git show 713be294669272b8b29e9a8cd60c5313704a2ee1:LOG.md` lines 1965-1966 and 1988;
`corpus/lessons/round-30.md` lines 189 and 199), the last receipts-only batch `<tip>` must add exactly:

- `.ufo/waves/round-30/evidence/tip-c1.txt`
- `.ufo/waves/round-30/evidence/tip-c2.txt`
- `.ufo/waves/round-30/evidence/tip-retention.txt`

where `<P>` below is the full 40-hex hash of the commit immediately before that batch (its first parent,
never the batch's own hash). Minimal body proven to pass (exactly the w1 mock shape, re-run by me):

```text
# measured at parent <P>; counter count-c1.sh
command: bash .ufo/waves/round-30/count-c1.sh <P>
<at least one line of the real counter run's stdout at <P>>
exit: <the run's real exit status>
```

`tip-c2.txt` identically with `count-c2.sh`. `tip-retention.txt` must contain `mori-retention-gate.py` and
`<P>`; the generator's form:

```text
# measured at parent <P>; scan mori-retention-gate.py
command: python3 -I -B tools/mori-retention-gate.py scan --repo <sandbox-clone> --rev <P> --policy .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json
<stdout, ≥1 line>
exit: <real status>
```

The w1 scratch generator (`/fast/scratch/hyaku/mori-r30/TipReceiptsR1/make-tip-receipts-r30.sh`) emits a
slightly different but checker-equivalent header — `# measured at parent <P>; the landed tip adds only receipt
files under .ufo/waves/round-30/evidence/; operation <script>` (`:51,:56`). Its internals are consistent:
`write_receipt` takes five args (`:54`) and all three calls pass five (`run_counter` at `:75`, retention at
`:96`); counters are invoked with the single `$parent` argument, matching the contract's command forms
(`.ufo/waves/round-30/contract.md:47,:91`), and the round-29 `fleet_rev` extra arg is gone. It was never
executed (w1 says so; I did not run it — it writes into the lane out-dir), so the mock receipts, not generator
output, are what I verified end-to-end.

## 3. Answer: extra counters in the contract?

**No.** `grep -oE 'count-[a-z0-9-]+\.sh'` on the contract yields only `count-c1.sh` (3 mentions: contract
lines 25, 47, 149) and `count-c2.sh` (2: lines 58, 91) — identical at both `ad0f04745ced…` and
`713be294669…` (`uniq -c`: `3 count-c1.sh`, `2 count-c2.sh`). No third counter receipt is needed. The
retention receipt is additional to the counters list but required by the checker's hard-coded loop
(`check-tip-receipts.sh:80-99`) — the plan already includes it, so nothing is missing.

## 4. Independent verification performed

- Re-ran the checker via the w1 read-only git router (`/fast/scratch/hyaku/mori-r30/TipReceiptsR1/bin/git`,
  which redirects the checker's `git -C <lane>` to the w1 sandbox clone):
  - `eb82b011730c2c799c7a6e8ea6272d37a8b494fb` (mock batch, parent `52a509f7ff21ba2b2f76c42707e38cedb186dd5e`
    — confirmed for both mock children via `rev-parse ^1`): all three receipts hit, all `cited_lane=yes`,
    prints `tip_receipts=met`, exit 0. Receipt bodies confirmed by `git show` from the clone: each is exactly
    the 4-line shape of §2 with `exit: 0` and a `mock stdout:` line.
  - Mutation child `99667b48ca77350515bab27c6a883321adde0217` (same parent, same receipts, `tip-c2.txt`
    citation count 0 in both mock reports vs 1/1 in the normal child): only the c2 line flips to
    `cited_lane=no`; prints `tip_receipts=unmet`, exit 1. Isolates the citation condition exactly as w1
    reported.
- Live lane state: `bash .ufo/waves/round-28/check-tip-receipts.sh ad0f04745ced… 30` →
  `counter=count-c1.sh receipt=.ufo/waves/round-30/evidence/c1-after.txt … cited_lane=yes`,
  `counter=count-c2.sh receipt=MISSING measured=ee61010dec…`, `retention receipt=MISSING`, `unmet`, exit 1.
  Same command at current HEAD `713be294669272b8b29e9a8cd60c5313704a2ee1` → all three `MISSING`,
  `measured=ad0f04745ced…`, `unmet`. So the receipts-only batch is still pending; evidence dir at HEAD holds
  13 files, none named `tip-*`.
- Batch `ad0f047..713be29` adds only wave-2 files (`.ufo/waves/round-30/w1/swarm-registry.json`,
  `wave2-dispatch.json`, `wave2-run.{err,json}`, `wave2-spec.json`); LOG.md and the lesson are untouched by it,
  so the pre-announcement lines predate it — the "named before the receipts-only batch" discipline holds.

## 5. Findings

- **F1 (minor, naming trap — no defect in the plan).** `LOG.md:1907` (round-28 close-out) names
  `evidence/tip-count-c1.txt`, `tip-count-c2.txt`. Those were round-28's literal receipt names (commit
  `1fc6bb0` "round-28: tip receipts …"); round-29 used `tip-c1.txt` etc. (commit `b581173`). The checker would
  accept either r30 spelling (basename substring match, `:69-70`), but only `tip-c1.txt`/`tip-c2.txt`/
  `tip-retention.txt` keeps `corpus/lessons/round-30.md:199` ("adds only … tip-c1.txt, tip-c2.txt and
  tip-retention.txt") true. The lane owner must copy the r29/r30 naming, not the r28 one.
- **F2 (residual, checker looseness — informational).** Receipt matching is content-based with first-match-
  wins over a sorted listing (`:46-47,:60-66`): at `ad0f047` the count-c1 requirement was already satisfied by
  `evidence/c1-after.txt` (it contains `count-c1.sh`, its parent hash, an `exit:` line, and is cited in LOG).
  A stray evidence file containing the new `P` plus an operation name could silently satisfy a slot. The
  citation condition limits but does not eliminate this. Not a plan defect; do not "clean up" old evidence
  files in the receipts-only batch — that would violate receipts-only anyway.
- **F3 (residual, unverifiable by this checker).** The checker cannot enforce "receipts-only": it measures the
  first parent whatever else the batch changes. The receipts-only discipline lives only in
  `LOG.md:1988` and `corpus/lessons/round-30.md:199`. If wave-2 fixes share the final batch, receipts would
  still validate while the lesson's claim becomes false. Keep the last batch receipts-only.

## 6. Residual risk and verification gaps

- The real counter/retention runs at the final parent do not exist yet; §2's bodies are shape-proven on mocks
  with synthetic stdout (`mock stdout:` lines), so real outcomes (C1=met, C2 currently unmet, retention count)
  remain unverified by this seat. [INFERENCE from mock wiring only: a real batch of this shape passes the
  checker regardless of counter verdicts, since receipts record withdrawals too (checker comment `:20`).]
- The w1 scratch generator has never been executed; if used, its `out-dir` write lands in the lane (MoriR30's
  act, not mine). Its emitted header wording differs from the mock's; both proven checker-equivalent.
- The `--report-repo/--report-rev` fleet-citation branch (`:53-56,:72-74`) was not exercised (no fleet round
  report path in the r30 plan); cited_fleet=na in all runs.

## 7. Bounds and tooling

Wrote only this report in the lane; scratch work confined to reading w1's sandbox read-only. No git/jj writes
anywhere; no pacman/uv installs (none needed — recorded per operator directive: zero installs this seat).
