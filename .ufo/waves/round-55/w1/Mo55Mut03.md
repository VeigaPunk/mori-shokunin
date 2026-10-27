# Mo55Mut03 — C1 fake-settlement mutation probe (round 55 w1)

Seat: mutation tester, leaf. Lane: mori-shokunin. Detector: frozen counter
`.ufo/waves/round-55/count-c1.py` (sha256 `e30658be34bfbf866860b20c9bde4117d467e351bb79e523131424cd5061e20b`,
untouched). All experiments ran inside a scratch clone at
`/fast/scratch/hyaku/mori-r55/Mo55Mut03/repo` (branch `mutprobe`, data base `b8b7064c2b54c8b6b22c288232a96c43fae1af47`;
`git rev-parse --show-toplevel` asserted = scratch clone before every mutation). Lane source, ledger, git/jj: never
modified. No RECHECK/ENTAIL/REPLACE/QUOTE vote lines are emitted by this seat.

## Method

1. Extracted the 78 scoped hashes + dispositions from the real ledger at `b8b7064c` (all 78 disposition cells are
   `holds`; statuses 69 same / 7 moved / 2 changed).
2. Built `s0`, a synthetic-but-honest settled wave on top of the landed data: 16 voter reports
   (`Mo55Rc01`–`Mo55Rc16`) each with 78 final unfenced lines `RECHECK <hash> holds`, plus
   `.ufo/waves/round-55/w1-results.json` binding every voter's output to those lines.
3. Ran the frozen counter per mutant commit: `python3 .ufo/waves/round-55/count-c1.py <rev>` (cwd = scratch clone).
4. Each mutant = one child commit of `s0`; working tree restored to `s0` between mutants
   (`git reset --hard s0` + `git clean -fdq`).

Baseline control (`s0`, rev `6e205ec817eebe5926b900261566eca49cc29cd1`):
`C1=met scope=78 rows=78 matched=78 status_ok=78 line_ok=78 source_rows=ok pins=ok provenance=ok same=69 moved=7
changed=2 broken=0 holds=78 stale=0 voted=78 dissent=0` — exit 0. Confirms the real landed data passes the vote arm
when honestly settled; every mutant below differs from this by exactly one defect class.

## Assigned fake-settlement cases

| mutant | defect injected | counter result | verdict |
|---|---|---|---|
| m01 report-only | all 16 reports prose-only; outputs still carry all lines | unmet `voted=0 failed=votes` (rc=1) | killed |
| m02 output mismatch (word) | outputs echo `RECHECK <h> stale` while reports/disposition say `holds` | unmet `voted=0 dissent=0 failed=votes` | killed |
| m03 output mismatch (hash) | outputs echo line with first hash char toggled | unmet `voted=0 failed=votes` | killed |
| m04 fenced (``` ) | vote lines inside backtick fences, all reports | unmet `voted=0 failed=votes` | killed |
| m05 fenced (~~~) | vote lines inside tilde fences | unmet `voted=0 failed=votes` | killed |
| m19 fence + info string | fence opened as ` ```text ` | unmet `voted=0 failed=votes` | killed |
| m20 indented fence | fence line indented 4 spaces (still toggles via lstrip) | unmet `voted=0 failed=votes` | killed |
| m07 extra-name only | real 16 prose-only; `Mo55Rc17.md` + `Mo55Mut03.md` agreeing and output-bound | unmet `voted=0 failed=votes` | killed |
| m08 one real + extras | only `Mo55Rc01` bound-agreeing; `Mo55Rc17` bound-agreeing | unmet `voted=0 failed=votes` — extras cannot top up | killed |
| m09 dissent (bound) | `Mo55Rc09` final word `stale` on hash[0]; output echoes it | unmet `dissent=1 failed=votes` | killed |
| m10 dissent (unbound) | report says `stale` on hash[0]; output lacks the line | unmet `dissent=1 failed=votes` (report-alone dissent) | killed |
| m14 uppercase word | reports vote `RECHECK <h> HOLDS` | unmet `voted=0 failed=votes` (VOTE_RE is lowercase-only) | killed |
| m15 name trailing space | results.json name `Mo55Rc01 ` for the only would-be second voter | unmet `voted=0 failed=votes` (name-exact) | killed |
| m16 one voter | single bound agreeing voter | unmet `voted=0 failed=votes` (MIN_VOTES=2 distinct) | killed |
| m17 results absent | reports agree; `w1-results.json` deleted | unmet `voted=0 failed=votes` | killed |

All 15 assigned cases are killed. The vote arm holds against report-only, output-mismatch, fenced-vote, extra-name
substitution, and dissent (bound and unbound) fraud on the real landed ledger.

## Surviving mutants / uncovered kills

1. **m11 two-fabricated-voters (survives — declared trust anchor).** Only `Mo55Rc01`+`Mo55Rc02` reports exist, plus
   results.json entries whose outputs echo the agreeing lines: `C1=met ... voted=78 dissent=0`, exit 0. Any two of the
   sixteen frozen voter identities, fully fabricated end-to-end (report bytes + orchestrator results.json binding),
   flip C1 to `met` on otherwise pristine data. This is the predicate's declared trust model ("the results binding
   proves the orchestrator recorded a seat of that name whose output repeats the vote line, not who wrote the report
   bytes"). It is a characterization, not a counter defect: the residual risk lives in results.json provenance and
   seat identity, which C1 explicitly places outside its scope. Minimum fraud surface = 2 voter identities + the
   results.json trust anchor; 1 voter (m16) and extra names (m07/m08) are provably insufficient.
2. **m06 fenced-dissent suppression (survives — kill-rule blind spot).** All 16 reports carry unfenced agreement; one
   voter appends a fenced block containing `RECHECK <hash[0]> stale`: `C1=met ... dissent=0`. `final_votes()` ignores
   fenced lines, so a voter can launder dissent through a fence and never registers a differing final word. This
   conforms to the predicate letter ("final unfenced line ... no RECHECK voter's final word for it differs") but
   weakens the contract kill rule "dissent => unmet" for fenced content; it cannot create settlement by itself.
3. **Over-strict kills — dead `startswith` arm at `count-c1.py:301` (defect, opposite direction).** Line 301:
   `bound = voter in outputs and any(l == "RECHECK %s %s" % (h, w) or l.startswith("RECHECK %s %s ") for l in out_lines)`.
   The `startswith` argument is the literal string `RECHECK %s %s ` — never interpolated with `(h, w)` — so that arm
   is dead code; binding requires exact whole-line equality after strip. Evidence:
   - m13 output-suffix-junk (outputs echo `RECHECK <h> holds (auto-captured)`): unmet `voted=0` — unexpectedly killed.
   - m21 holds-with-reason (report+output verbatim `RECHECK <h> holds -- verified`): unmet `voted=0` — unexpectedly
     killed (equality compares against the canonical two-token form, not the report's actual line).
   - m25 stale reason-form (ledger row hash[0] disposition=`stale`, report+output verbatim contract form
     `RECHECK <h> stale -- oom_kill.c:673 no longer matches v7.3`): unmet `stale=1 voted=0` — the contract-mandated
     stale line does not bind at all.
   - m26 workaround: same plus a bare canonical `RECHECK <h> stale` echo in output: hash[0] binds (`voted=1` for the
     stale row). m27 control (plain canonical line both sides): binds.
   Impact: over-strict, liveness/consensus direction only — it cannot enable fake settlement (it only rejects). Any
   stale-disposition row settled with the contract-required reason form fails to bind unless the orchestrator output
   also carries the bare canonical line. All 78 current rows are `holds`, so the live wave is unaffected; latent for
   stale rows.

## Characterizations (met, by design)

- m18 last-line-wins: unfenced trailing `stale` then `holds` → final word `holds` → met (selftest-covered).
- m22 agreeing-but-unbound: 2 bound agreeing + 1 agreeing voter with no results.json entry → met (unbound agreeing
  votes are ignored, never counted, never dissent).
- m12 duplicate results.json entries are last-wins: m12b (only `Mo55Rc01`, entries [lines, junk]) → junk wins →
  unmet `voted=0` (a junk-appended result revokes that voter's binding — griefing-only channel); m12c ([junk, lines])
  → binds but single voter → unmet. With 16 real voters present, revoking one leaves 15 → still met.
- m23/m24 binding is strip-tolerant: output lines with trailing/leading whitespace bind → met.

## Restoration evidence

- Clone restored to `s0` after every mutant; after the final probe: all 18 baseline files (16 reports + results.json
  + counter copy + ledger copy) sha256-identical to pre-mutation hashes (`pristine_ok_after_all_probes: True`);
  `git status --porcelain -- .ufo/waves/round-55` empty in the clone; clone HEAD `6e205ec8` (s0).
- Lane repo untouched by this seat: no writes outside the assigned report path; frozen counter sha256
  `e30658be34bfbf866860b20c9bde4117d467e351bb79e523131424cd5061e20b`; ledger sha256
  `462e67c148d66ce1f886d21540474a19bd6244ae56c5fc1c5c8391ba6e7d5e8e` (both identical to pre-probe values; the
  counter was only read).
- Scratch dir `/fast/scratch/hyaku/mori-r55/Mo55Mut03` removed after report write (probe drivers and JSON results
  were ephemeral; full evidence inlined above). Disk guard before work: `/fast/scratch` 594.2G free, 27% used — no
  ENOSPC.

## Findings

- **Medium — counter defect, over-strict binding:** dead `startswith` arm at `count-c1.py:301` means only the exact
  canonical line `RECHECK <hash> <word>` binds; the contract-mandated stale reason form (`RECHECK <hash> stale —
  reason + path:line`) never binds on its own (evidence: mutants m13/m21/m25 vs m26/m27 above; lane source ref
  `mori-shokunin/.ufo/waves/round-55/count-c1.py:301`). Liveness risk for any stale row; no fake-settlement exposure.
- **Low — kill-rule blind spot:** fenced dissent is invisible to the vote arm (mutant m06); a voter can avoid
  registering dissent by fencing it. Predicate-letter conformant; cannot fabricate settlement.
- **Info — declared trust anchor:** two fully fabricated voter identities + results.json binding settle C1 (mutant
  m11); one voter or extra names cannot (m07/m08/m16). Residual risk is results.json provenance / seat identity,
  explicitly outside C1's frozen scope.
- **Info — robustness confirmed:** report-only, output word/hash mismatch, both fence dialects (+info string,
  indented), extra-name substitution, bound/unbound dissent, case-shifted words, name-with-space, missing results:
  all killed (mutants m01–m05, m07–m10, m14–m17, m19, m20).
