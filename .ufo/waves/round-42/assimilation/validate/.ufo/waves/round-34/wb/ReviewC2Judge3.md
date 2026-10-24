measured 2026-10-23T08:06:08Z
# ReviewC2Judge3 — C2 (QUALITY 98), named non-author review; audit of attempt-2 reports

## Method and containment

- Judged bytes read from git (read-only): `git show fd2521351c6cef47384aef30afbe1e4db7e6912e:corpus/QUALITY.md` (731 lines), `git show fdf4371f:.ufo/waves/round-33/contract.md` (134), `git show b9fb029e:.ufo/waves/round-34/contract.md` (150), `git show b9fb029:.ufo/waves/round-34/evidence/c1-controls.txt` (55), `git show fdf4371f:.ufo/waves/round-33/evidence/c1-controls.txt` (78), `corpus/lessons/round-33-verifier-spotcheck.md` at fd25213 (243). Scratch dumps under `/fast/scratch/hyaku/mori-r34/a3-ReviewC2Judge3/`. Only this report written in the lane.
- Counter re-run by me (frozen `count-c1-a1.py`, working-tree bytes sha256 `c14c3494…` = `b9fb029` blob): `python3 .ufo/waves/round-34/count-c1-a1.py ef936fb4e0834d0a1ce676aef735debe2eef9d27 --repo /fast/scratch/hyaku/mori-r34/a2-CritPostDataShortcut/clone` → `fixed_pass=12/12 random_pass=300/300 … live=ok C1=met`, `EXIT=0`, fresh seed `14794041770328378793`, 5.49 s wall, measured_at 07:50:39Z. Reproduces the L1 rescore receipt (`evidence/ctl-postdata-shortcut/receipt.txt`, measured 05:49:11Z, seed `3441622588333245736`, `C1=met`).
- No tool installed or updated (none needed; pacman transactions are paused host-wide and were not touched). No subagents, no background jobs; every process returned before I finished.

## What 98 claims, and the discriminating bytes

QUALITY 98 (fd25213 `corpus/QUALITY.md:713-727`): before any data seat, a measured claim's contract maps each leg-rejection shape — generic rows or copying the observed column; server echo; label- or id-keyed answers; skip-work or do-nothing; content-free output; no-decision content; a rule changed, or rows deleted, after data — to a named control or a stated inapplicability with reason; a control discharges a shape only when it is the deliverable with that shape's defect injected (generic absence / guard trip discharges only skip-work and content-free); each control scored under the frozen counter with the receipt committed in an ancestor of the first data commit; a control scored met means counter or target is wrong. Check: (a) table names every shape once; (b) each named control has a receipt line; (c) `git merge-base --is-ancestor <receipt> <first data commit>`.

## My application of 98's checks

**Round-33 contract at `fdf4371f` — 98 fails it.** The controls list (`r33 contract`, C1 section) names nine: do-nothing, junk rows, all-false judge, no-reader judge, receipt without R-J / loosened rule, stale `judged-sha256`, fabricated sources, sources already registered, shortcut keyed on ids/labels. Check (a): no no-decision control (the routed defect, spotcheck `:128-129`, §8 item 1 at `:226-228`); also no server echo, no copy-observed-column, no rule-changed/rows-deleted mapping. (b) holds: the receipt at `fdf4371f` has Part B `count-c1-a1.py` rows for all nine (e.g. do-nothing `:16`, id/label shortcut `:19`, fabricated sources `:24-25`, honest junk `:62`; the forged-receipt state `5ae82bab` at `:63` is the declared residual). (c) holds: `git merge-base --is-ancestor fdf4371f 62db24c` exit 0 (my run). The post-data no-decision control CtlGlossaryA1 met P-C1-A1 (spotcheck §3.2 `:103-137`, closure ruling `:112`). Fails decisively on (a).

**Round-34 contract at `b9fb029e` — 98 passes it (with defects D1–D2).** Table at contract `:69-81` maps skip-work→C-absent, content-free→C-junk/C-allnull, no-decision→C-naive/C-alldisk/C-noreset, wrong-surface→C-sinceboot, label-keyed→C-labelkey, server echo→C-echo "unmet (guard)", wrong sysfs root→C-sysblock; copy-observed-column and rows-deleted are stated inapplicable with reasons (`:80-81`). (b) holds: receipt rows 01–16 all print `C1=unmet` under P-C1-A1; positives 17–18 `C1=met` under both. (c) holds: receipt measured 05:13:09Z at `b9fb029` (05:30:38Z is `ba525e1`, 05:34:40Z is `8d56809` — `%cI`); `git merge-base --is-ancestor b9fb029 ba525e1` and `… b9fb029 8d56809` both exit 0 (my runs). So 98 discriminates: fails round 33's contract, passes round 34's.

## Defects found (by severity; report only — nothing amended)

- **D2 (moderate, C1-side normative gap):** the server-echo discharge violates 98's own discharge sentence. Table maps echo → `C-echo … unmet (guard)` (contract `:77-78`); receipt rows 09 and 16 carry a dirty guard under P-C1-A1 (`guard=['.ufo', 'count-c1']`), and rows 10–11 fail by environment absence (fixed 0/12, random 0/300, `live-rc=1`). Per `QUALITY.md:718-720` a guard-tripped/generic-absence failure discharges only skip-work and content-free. A1's namespace makes echo impossible (prevention by construction), but 98's taxonomy has no such mapping — 98's own worked example relies on a discharge 98 does not license.
- **D1 (minor, wording):** 98's "Round 34's table maps each shape" (`QUALITY.md:725-727`) overstates on a strict reading of check (a): no table row names "a rule changed [after data]" (only the rows-deleted half, contract `:81`), and "generic rows" is never literally named. Defensible purposively (the kill rule at contract `:13-15` freezes counter/rules; the content-free row carries the generic-junk family), but the criterion's mechanical check does not literally hold on its own positive example.
- **D3 (minor, citation):** 98 cites `corpus/lessons/round-34.md` and "(round-34 Mistakes M1)" for the rule-order defect (`QUALITY.md:724-727`). That file is absent from every committed tree through fd25213 (`git ls-tree fd25213:corpus/lessons` ends at `round-33.md`); the uncommitted worktree draft numbers the rule-order defect M3, with M1 = the no-decision gap and M2 = the post-data shortcut. The pointer verifies against nothing at the judged revision and contradicts the only observable numbering [INFERENCE: attempt-2 numbering likely differed when 98 landed].
- **D4 (minor, C1-side):** the r34 contract's receipts paragraph says "(three of them met P-C1)"; four negative-control runs met P-C1 (receipt rows 10, 11, 13, 14). "Three" holds only by counting shapes (emptylive + its zero-variant, echo v2, echo v3 — contract Amendment A1 text).
- **D5 (observation, verified):** ef936fb4 meets P-C1-A1 (my re-run above). See §below.
- **D6 (observation):** 98's mechanical checks (a)–(c) do not encode the discharge-quality sentence; substituting an already-scored absent-tool control under kept shape names passes (a)–(c) (confirmed by MutQ98's mutant 2; consistent with the text of `QUALITY.md:715-723`).

## §8 item 1 second clause — not answered

§8 item 1 (spotcheck `:226-228`) has two clauses: (1) a no-decision-proof predicate with the control receipt committed before data; (2) "require each verdict cell to name a reader action, checked by something other than the header label". 98 contains no verdict-cell or reader-action requirement (`QUALITY.md:713-727`). Round 34's C1 is a tool claim with no verdict cells, so clause 2 had no direct object this round, but as the routed answer it silently drops clause 2, and the contract's routing line "item 1 … is answered by QUALITY 98 (C2)" (contract `:9`) overstates coverage.

## ef936fb4 — counts as a bound, not a refutation

The probe reads the regular `/proc/diskstats` once (rate 0 for every device) and twice only when it is a FIFO (the counter's fed arm), and classifies by name patterns (receipt `:3`). My re-run confirms `C1=met` under a fresh seed. Relation to 98: the battery passed (16/16 negative controls unmet pre-data), yet a post-data shortcut meets the counter. If the probe is read as harness-keyed, it is a variant of 98's label-keyed shape whose mapped control (C-labelkey, keyed on the 12 fixed-seed input bytes) did not inject it — the mutant-2 weakness at shape level (the uncommitted lesson draft M2 says exactly this and routes the fix to QUALITY 99). If read as a new shape, it falls in the class 98 itself declares "Not covered" (`QUALITY.md:727`). Either way 98 cannot be sold as counter soundness — only as pre-data discipline that demonstrably bites. It un-verifies C1 (the receipt's own L1 ruling: "under addendum §9 C1 is not verified"), not 98's process check.

## Verdict rationale

98 is a real step beyond QUALITY 95–97 (all three regulate post-hoc receipts/quoting: judged-bytes sha256, re-open sweep evidence, verbatim judge rule — `QUALITY.md:683-711`) and beyond the round prompt's §9, whose only in-repo trace is the round-33 spotcheck's quote (`:125-127`: a frozen target a cheap control meets after data has failed, not amendable; `wa-run.json` likewise references "Adversarial §9 attack … after data"). 98 front-loads that test pre-data with a named-shape battery, discharge semantics, per-control receipts and an ancestry check. It has demonstrated force in this very round: four control runs met the pre-A1 counter and forced a re-design before any data seat — 98's "a control scored met means the counter or the target is wrong" exercised, not hypothetical. It fails round 33's contract on the exact routed defect and passes round 34's. The defects D1–D6 are wording-level, taxonomy-level, or declared residuals; the second clause of §8 item 1 is unanswered, narrowing the claim's coverage but not its clause-1 improvement. Verification is necessarily exploratory (no counting command), and I am the named non-author reviewer.

VERDICT: unprovable-but-better

## Audit of .ufo/waves/round-34/wa/ReviewC2Judge.md (measured 05:40:31Z)

My verdict was fixed from the primary bytes before I opened this file; a search snippet of its §3 heading reached me mid-run before the verdict was typed — the verdict logic above was already committed to the discriminating facts by then.

1. Nine round-33 pre-data controls, none no-decision — agree (r33 contract controls list; spotcheck `:128-129`).
2. Check (a) fails on round 33, missing no-decision/echo/copy-column/rule-or-rows shapes — agree (my application).
3. (b) holds: r33 receipt Part A/Part B at `fdf4371f`, pre-wave-1 — agree (78-line file, Part B header; `fdf4371f` ancestor of `62db24c`, exit 0).
4. (c) holds for `fdf4371f` — agree.
5. r34 table at `:69-81`, byte-identical at HEAD — agree (`b9fb029` blob == fd25213 blob == worktree; table lines 69–81 measured).
6. Receipt sha256 `fb15da47…` = working tree — agree (my sha256 match).
7. Soft spots: "generic rows" not literal; "a rule changed after data" only via the deletion half — agree (my D1).
8. (b): rows 01–16 cover every named control; all sixteen P-C1-A1 lines unmet; positives met under both — agree (my receipt read).
9. (c): `b9fb029` ancestor of `ba525e1`/`8d56809`/`fd25213` — agree (my merge-base exits 0).
10. "The first data commit does not exist yet" at 05:40:31Z — disagree: `ba525e1` (05:30:38Z, the tool = the claim's deliverable) and `8d56809` (05:34:40Z, corpus rows) had landed before their measurement; their `git log` evidence covers only `w1/`/`wa/` report paths, a narrower reading of "data". Their (c)-holds conclusion survives under every reading.
11. §3: over 95–97 yes, those are post-hoc receipt criteria — agree.
12. §3: prompt §9 characterized via `mori-round-34.md:343-365` with ":352-356 fix it before data" — disagree as a lane-verifiable fact: that file exists in no tree I checked (fd25213, 89791013, fdf4371f, 62db24c) nor the worktree, and is not embedded in `wa-dispatch.json`; the only in-repo §9 trace attributes r33-prompt `:352-356` to §2b item 4 and §9 to `:357-360` (spotcheck `:124-127`). The described §9 content is plausible [INFERENCE] but unverifiable from the lane.
13. §4: the claim's asserted specifics all verify — agree (each independently verified by me).
14. §4: lesson pointer absent mid-round — agree, and stronger than stated: absent at the judged revision entirely (my D3), and the worktree draft's numbering contradicts the M1 pointer.
15. §5: 98 answers only clause 1 of §8 item 1; the routing line overstates — agree (my reading; contract `:9`).
16. §6: echo discharge open under 98's strict semantics — agree (my D2).
17. Final verdict "unprovable-but-better" — agree (same verdict, reached independently before I opened this file).

AUDIT: agree 15 / disagree 2

## Audit of .ufo/waves/round-34/wa/MutQ98.md (measured 05:44:10Z)

1. Sources pinned to the four committed blobs; scratch isolation at `a2-MutQ98/`; no `w1/` input — agree (their `quality98.md` matches the committed 98 text; dir exists).
2. (a) family-normalized reading declared; `a_literal_exactly_once=false` on pristine (3 no-decision rows, contract `:73-75`) — agree as reported; note exactly-once is not the natural reading of 98's "once" (98's own example fails r33 for naming a shape zero times, so "once" = at-least-once).
3. (b): `C-echo` → receipt `C-echo-v1-literal`; all baseline results unmet; amendment controls have receipt lines — agree (receipt rows 09, 29–49 region).
4. (c): first data = `ba525e1`; ancestry exit 0 — agree (my own merge-base exit 0; `ba525e1` is the better-defined "first data" choice, the deliverable itself).
5. Mutant 1 (delete the three no-decision rows) killed by (a) — agree (probe-summary: mutated exit=1, a=0; restored exit=0; logic consistent with 98's text).
6. Mutant 2 (keep shape names, point cells at `C-absent`) survived stated checks, correctly scoped to (a)–(c) with the normative discharge sentence applied by hand — agree (probe-summary: exit=0, a=1 b=1 c=1; this is my D6, independently confirmed).
7. Mutant 3 (receipt after synthetic first-data commit) killed by (c); receipt blob equality `3bc54a46…` — agree (probe-summary: merge_base_exit=1 with synthetic commits; the kill is the definition of (c)).
8. Round-33 historical negative: (a) rejects; (b) nine categories map to committed A1 receipt lines; (c) `fdf4371f`→`62db24c` exit 0; scores read not rerun, disclosed — agree (their hand mapping verified against the receipt bytes: do-nothing `:16`, id/label `:19`, fabricated/registered `:24-25`, judge shapes `:35/:43/:45/:55`, honest junk `:62`, forged-met residual `:63`; my merge-base exit 0).
9. Limitation 1 (strict-once reading would make the comparisons inconclusive) — agree as stated, with the reading caveat in row 2.
10. Limitation 2 (pristine not certified under full normative 98 because the echo row's discharge is guard-based) — agree (my D2).
11. Restoration hashes and "only this report was written in the lane" — agree as reported (no contrary evidence observed; the lane-side write I can see is `wa/MutQ98.md` itself).

AUDIT: agree 11 / disagree 0

## Residual risk and verification gaps

- The round-34 prompt §9 is not verifiable from lane bytes (never committed; `.ufo/prompts/` absent from every tree checked and the worktree). My §9 comparison rests on the r33 spotcheck quote and `wa-run.json`'s §9 reference; the attempt-2 reviewer's line-level §9 citation remains unverifiable, not disproven.
- MutQ98's detector runs and synthetic history were audited from their preserved outputs and logic, not re-executed by me.
- "First data commit" is undefined in 98; I verified (c) against both candidate readings (`ba525e1`, `8d56809`) — exit 0 both — so the gap is currently harmless.
- `corpus/lessons/round-34.md` (M1–M3 numbering, M2's QUALITY-99 routing) is uncommitted worktree material; I used it as a lead only, per the wave rules.

## Tooling record

No tools installed or updated. Everything ran with the lane's existing python3/git; the only stateful action was my 5.49 s frozen-counter re-run in the pre-existing attempt-2 sandbox clone (read-only w.r.t. the lane; namespaces/tmpfs are the counter's own designed containment).
