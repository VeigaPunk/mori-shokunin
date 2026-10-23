measured 2026-10-23T05:40:31Z
# ReviewC2Judge — exploratory claim C2 (QUALITY 98), named non-author reviewer

Claim under review: QUALITY criterion 98 improves the lane's pre-data self-assessment of a claim, which round 33
lacked (nine pre-data controls had no no-decision control; a post-data glossary control met its counter). Verdict
line at the end.

## 1. Check (a)–(c) applied by me to the round-33 contract at fdf4371f

Contract text: `git show fdf4371f:.ufo/waves/round-33/contract.md` (controls list in the C1 section). The nine
pre-data controls: do-nothing (entering tip), junk rows, all-false judge, no-reader judge, receipt without R-J /
loosened rule, stale judged-sha256, fabricated sources, sources already registered, shortcut keyed on ids or labels.

- (a) FAILS. Of the seven shape items enumerated in QUALITY 98 (QUALITY.md:715-721), the list names only
  skip-work/do-nothing, content-free (junk rows) and label-/id-keyed (shortcut). It names no no-decision control,
  no server echo, no copy-observed-column control as such, and no rule-changed/rows-deleted-after-data mapping.
  This is exactly the designed failure mode claimed by 98 (QUALITY.md:726-728, "name no no-decision control, so
  (a) fails").
- (b) HOLDS: evidence/c1-controls.txt exists at fdf4371f (Part A summaries per seat, Part B `count-c1-a1.py`
  rows for every named control commit), committed before wave 1.
- (c) HOLDS: fdf4371f (A1 + receipts) precedes the wave-1/wave-2 data commits (62db24c0, 7a0234c2, a193627c).

## 2. Check (a)–(c) applied by me to the round-34 contract at b9fb029e

Contract text: `git show b9fb029e:.ufo/waves/round-34/contract.md` (Pre-data controls table, lines 69-81;
byte-identical at HEAD). Receipt: evidence/c1-controls.txt at b9fb029e, sha256 `fb15da47…` = working tree.

- (a) HOLDS on the common reading: table rows map skip-work/do-nothing → C-absent; content-free → C-junk/C-allnull;
  no-decision → C-naive/C-alldisk/C-noreset; label-keyed → C-labelkey; server echo → C-echo; copy observed column →
  stated inapplicable with reason; rows deleted after judgment → stated inapplicable with reason. Two soft spots:
  (i) "generic rows" is not literally named (closest discharge is C-naive, titled no-decision); (ii) "a rule
  changed after data" is not named separately — the "rows deleted after judgment" row covers the compound item
  "a rule changed, or rows deleted, after data" via its deletion half only. Neither breaks the mapping on a
  charitable reading; both are documented as ambiguity.
- (b) HOLDS: receipt rows 01–16 cover every named control (C-absent, C-junk, C-allnull, C-naive, C-alldisk,
  C-noreset, C-sinceboot, C-labelkey, C-echo v1/v2/v3/literal2, C-sysblock, C-emptylive, C-zero-singleread,
  C-echo-ppid); all sixteen P-C1-A1 lines print C1=unmet; the two positive controls print C1=met under both
  predicates.
- (c) HOLDS today and is pre-verified: b9fb029e is an ancestor of every subsequent commit (ba525e1, 8d56809,
  fd25213 — `git merge-base --is-ancestor` all YES). The first data commit does not exist yet: no commit touches
  `.ufo/waves/round-34/w1/` or `wa/` (`git log --all -- <paths>` empty); wave-A seat reports are uncommitted.
  (c) will hold for the first data commit when it lands.

## 3. Is 98 a real improvement over QUALITY 95–97 and the prompt's §9?

- Over 95–97 (QUALITY.md:681-711): yes. 95 (judge receipt sha256), 96 (never-re-opened sweep evidence), 97
  (verbatim judge rule in dispatch and receipt) all regulate post-hoc receipts, sweeps and quoting. None imposes a
  pre-data adversarial control battery or a leg-rejection shape taxonomy. 98 adds a distinct admission dimension.
- Over prompt §9 (mori-round-34.md:343-365): yes, but incremental. §9 already requires one cheapest skip-work
  control scored under the frozen counter with a committed receipt before data ("fix it before data", :352-356)
  and freeze-before-data predicate parity (:357-360). 98 generalizes this to seven shape families, requires each
  to map to a control or a stated inapplicability with reason, defines discharge semantics (deliverable-minus-work
  vs generic absence/guard trip), and adds per-shape receipts plus an ancestor-of-first-data-commit check. It is
  the operationalized, generalized form of §9's single-control rule — a real step, not a duplicate.

## 4. Does it overclaim?

- The claim as stated in the contract (contract.md:92-97) and in this assignment verifies on every specific:
  nine pre-data controls had no no-decision control (verified §1); the post-data glossary CtlGlossaryA1 met
  P-C1-A1 (round-33-verifier-spotcheck.md §3.2, :103-137); 98 is able to fail (applied myself, §1); the receipt
  scores 16 negative controls C1=unmet under P-C1-A1 before any data seat (verified §2).
- Two soft spots in the criterion's own positive example (not in the claim's asserted specifics): the "maps each
  shape" wording for the round-34 table (§2 soft spots) and the lesson pointer to corpus/lessons/round-34.md,
  which does not exist yet mid-round (expected to land by round end). No material overclaim.

## 5. Does 98 answer the second clause of §8 item 1?

- No. §8 item 1 has two clauses (round-33-verifier-spotcheck.md:226-228): (1) freeze a predicate a no-decision
  control cannot meet and commit that control's receipt before data; (2) require each verdict cell to name a
  reader action, checked by something other than the header label. 98 implements clause 1 (no-decision shape
  forced into the control table with pre-data receipt). 98 nowhere mentions verdict cells or reader actions.
- The contract's routing line (contract.md:9, :104) says item 1 "is answered by QUALITY 98 (C2)"; that
  overstates the coverage — only clause 1 is answered. The C2 claim itself, as framed ("improves the lane's
  pre-data self-assessment … which round 33 lacked"), is narrower and accurate with respect to clause 1.

## 6. Residual risk and verification gaps

- (c) completes only when the first data commit lands; until then it is pre-verified by ancestry alone.
- Discharge semantics for the server-echo shape: C-echo's unmet under P-C1-A1 comes from the environment hiding
  (/home, /fast tmpfs + capability drop → live-rc=1), which 98's own definition treats as "guard tripped" —
  per 98 that discharges only skip-work/content-free shapes, not echo. The round-34 table maps the shape
  nominally; whether it discharges it under 98's strict semantics is open (C1-side question, not this claim).
- "Generic rows" and "a rule changed after data" naming ambiguity (§2) is a small reduction in the criterion's
  mechanical checkability; it does not change the verdict.

## Verdict

VERDICT: unprovable-but-better
