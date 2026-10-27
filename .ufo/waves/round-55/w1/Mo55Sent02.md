# Mo55Sent02 — sentinel: results/report voter binding (spoofable identity, evidence limits)

Role: sentinel, non-voter, non-author. Surface: the vote arm of the two frozen counters — `count-c1.py` and
`count-c2.py` — plus the record they read (`w1-results.json`), the reports they read, and the capture path that
produces the record. Detection only; no production edit, no counter edit, no git/jj mutation.

Frozen bytes audited (sha256 matches `evidence/freeze-sha256.txt:3,6,7`):

```
e30658be34bfbf866860b20c9bde4117d467e351bb79e523131424cd5061e20b  .ufo/waves/round-55/count-c1.py
ccb2333a7e3d6744f00041b5bb95a95cb5191b6b5d5a8a963949db4891e12754  .ufo/waves/round-55/count-c2.py
3050b1fd99763114fbbc6d39b5e782101d82e8881ac7b4d19ce4f91cfebd6c17  .ufo/waves/round-55/contract.md
```

## Method

1. Read both counters' vote arms and their aggregation (`count-c1.py:270-304,384-390,402-403`;
   `count-c2.py:144-176,264-271`), the two selftests (`checks/selftest-c1.py`, `checks/selftest-c2.py`) and the
   receipts (`evidence/selftest-c1.txt` = `pass=44 fail=0`, `evidence/selftest-c2.txt` = `pass=10 fail=0`).
2. Read the capture path that produces the record (`scripts/hyaku/inline-dispatcher.py:278-296,375-382`) and a
   prior round's record as ground truth for the recorded shape (`mori-shokunin/.ufo/waves/round-54/w1-results.json`).
3. Loaded the frozen counter modules in scratch (`importlib`) and drove `votes()` / `entail_votes()` with synthetic
   read/ls callables — the same interface the counters use. Every result below is an executed observation, not a
   reading of intent.
4. Measured the live wave: 14 of 16 C1 reports on disk (`Mo55Rc01`–`Mo55Rc13`, `Mo55Rc16`; Rc14/Rc15 in flight),
   138 vote lines over 78 distinct hashes, all 78 hashes present in the ledger (78 rows, all disposition `holds`);
   9 C2 reports covering 23 rows twice. Sampled live seat outputs via `agent://` (Rc01, Rc05, Rc07, Rc12, En01).

Commands used: `sha256sum`, `python3` module loads, `git ls-tree`/`git ls-files`/`git log` (read-only), `df` and
`scripts/hyaku/disk-guard.sh status` (26% used on `/fast`, 594.6G free — no ENOSPC, proceeded).

## F1 — HIGH — C1's output binding cannot match the shape this wave's seats actually emit

`count-c1.py:299-302` builds the output side as `strip()`ed lines of `str(h.output())`, then requires either exact
equality with `RECHECK <h> <word>` or `l.startswith("RECHECK %s %s ")`. That second branch is **dead code**: the
literal is never formatted with `(h, w)` (verified with `cat -A`; `%s` is still in the string), so it matches
nothing. Binding is therefore exact equality after strip.

Every sampled live C1 seat yields a JSON object whose vote lines are **array elements**:

```
agent://Mo55Rc05 -> {"report": "...", "findings": "...", "votes": ["RECHECK 901c19ca0925 holds", ...]}
agent://Mo55Rc07 -> {"findings": [], "report": "...", "votes": ["RECHECK 0ee301f4c8ae holds", ...], ...}
agent://Mo55Rc12 -> {"report": "...", "votes": ["RECHECK b7c369d84995 holds", ...]}
agent://Mo55Rc01 -> {"findings": "...", "report": "...", "rows": "10/10 holds", "vote_lines": ["RECHECK 7b2d297eec60 holds", ...]}
```

The record stores `str(h.output())` (`inline-dispatcher.py:283`); round-54's committed `w1-results.json` shows that
form is JSON text, not the seat's markdown (`"output": "{\n  \"seat\": \"Mo54Rc01\",\n  \"role\": ...`). Split on
newlines, each element line is `    "RECHECK 901c19ca0925 holds",`; after `strip()` it is
`"RECHECK 901c19ca0925 holds",` — leading quote and trailing comma, so equality fails and the dead prefix branch
cannot rescue it.

Executed on the frozen module (scratch, `bindtest.py`), one report line and one recorded output each:

| recorded output shape | rows where a genuine vote binds |
|---|---|
| JSON object, array-valued vote list (round-54/55 shape) | 0 |
| `str(dict)` (Python repr, single quotes) | 0 |
| single JSON string field with `\n`-separated lines | interior lines only — of 3, first and last unbound |
| plain newline-joined text | all |

Arithmetic on the live wave: 16 C1 seats × 10 rows ≈ 160 assignments over 78 rows (measured: 60 rows at 2 live
voters, 18 rows at 1 while Rc14/Rc15 are in flight) — i.e. essentially exactly 2 voters per row, zero margin. If no
array-shaped vote binds, `voted` is 0 for every row and `if voted != len(sc)` (`count-c1.py:402`) reports
`failed=votes`. **Impact:** a false-unmet of the whole C1 arm with 138 legitimate vote lines on disk; the honest
result at R is `C1=unmet ... voted=0`. **Smallest remediation:** normalize before compare (strip JSON punctuation /
list bullets) or format the prefix branch, and have voters emit one plain newline-delimited text field; for this
round, record the limitation — do not repair it by editing the settlement record (see F4).

## F2 — MEDIUM — negative votes need no output binding, and the report directory is shared-writable

Agreeing votes must be echoed in the captured output; differing words need not be.

- C1: `count-c1.py:303` adds every report vote to `per` regardless of `bound`; aggregation at `:385-387` treats any
  `w != disp` value as dissent. A single line written into `w1/<voter>.md` by **any** process forces
  `dissent>=1` → C1 unmet.
- C2: `count-c2.py:169` accepts an `overclaim` line without any output check (`m.group(2) == "overclaim" or ...`),
  and `:265` lets one overclaim veto the row even when two bound `entailed` votes exist.
- C2 REPLACE is worse: `:173` records authorship from a `REPLACE <h> :: <text>` line in the *voter's own report*,
  and `:264` then voids that voter's `entailed` vote. The text needed is the row's own claim text (public in the
  ledger), so appending one line to one voter's report drops a 2-voter row to 1 → unmet.

Executed: report-only stale (C1) and report-only overclaim (C2) both registered with the writer's output saying
`no votes`/`nothing`; a REPLACE line hashed to the row voided that voter. Live semantics are already exercised
legitimately — `Mo55En01` carries two overclaim lines that will bite two rows regardless of its output.

**Impact:** targeted denial of a row or a seat by any co-writer (including a careless one), no false-met.
**Smallest remediation:** bind dissent symmetrically (the differing word must also appear in the captured output),
and count REPLACE authorship only when the REPLACE line is echoed in the output.

## F3 — MEDIUM — "distinct voters" is name-only; identical bytes count twice

`count-c1.py:295-303` / `count-c2.py:156-176` key voters by filename under `w1/`. Executed: two byte-identical
report files under `Mo55Rc01` and `Mo55Rc02`, each echoed in its own recorded output, yield two agreeing voters for
the same hash. Nothing compares report bytes, authors, or transcripts. With F1's zero margin, one copied report
closes a row. **Impact:** the independence the arm claims is name-distinctness, not author-distinctness.
**Smallest remediation:** no counter change needed this round; at closure spot-check one transcript per author pair
(or have each seat echo a dispatch nonce, F4).

## F4 — HIGH — the settlement record is unpinned and has no independent witness

`evidence/freeze-sha256.txt` (35 lines) pins the contract, both counters, both controls, both selftests, the receipts
and the source copies. It does **not** pin `w1-results.json` or anything under `w1/`. The record is written by the
orchestrator at finalize (`inline-dispatcher.py:289-295`) into the lane tree and then lands in the L1's commit; the
counter reads it from that same commit (`count-c1.py:424-430`, `git show R:...`). The L1 therefore controls both the
record the gate trusts and the reports it joins against, with no pre-landing copy elsewhere.

Exploit path (requires only write access before the landing commit, which integration has by design): add a
`name`/`output` pair carrying a vote line for a seat that did not vote, and add the matching report line; the counter
at R reads `met` and no artifact records what the orchestrator actually captured. **Impact:** the 2-vote
independence gate collapses to the L1's assertion — a provenance/fabricated-readiness defect, and the exact pressure
F1 creates (the natural reaction to `voted=0` is to "fix" the record). **Smallest remediation:** have the dispatcher
include a sha256 of `w1-results.json` (and per-seat output digests) in its `WAVE-DONE` message so the digest lands in
the L1's transcript before landing; closure compares. No frozen-counter change required.

## F5 — LOW — duplicate result names are silently last-wins

`outputs[r["name"]] = ...` (`count-c1.py:291`, `count-c2.py:153`) overwrites; neither counter nor selftest checks
for duplicates. Executed: the same two-entry record binds or does not bind depending on entry order. A resumed or
amended wave (`adopt()`/`bootstrap()` paths, `inline-dispatcher.py:217,358-390`) that writes twice, or any hand edit,
changes the verdict without any signal. **Smallest remediation:** reject a record with duplicate names.

## F6 — LOW — the two arms disagree on what a settled voter is

C1 adds a report-only voter to `per` with `bound=False`, so such a voter can dissent (`count-c1.py:296-303`);
C2 skips a voter absent from the record entirely (`count-c2.py:158`), so its overclaim is ignored. Executed: a
`stale` line in a report with no record entry produces `dissent=1` in C1. In the normal finalize path every name has
an entry, so both fail closed; the definitions still differ. **Smallest remediation:** align the gate.

## F7 — MEDIUM-LOW — independence is asserted, not measured

Neither counter reads `w1-dispatch.json` (`grep -c dispatch` = 0 in both), so a voter may vote outside its band and
two seats may cover all 78 rows. The passing witnesses in the selftests are exactly that: two voters on every row
(`checks/selftest-c1.py:54-60,80`; `checks/selftest-c2.py:20-22` uses `c2.VOTERS[:2]` for all 23 rows). `count-c1.py`
prints `voted=N` counting **rows**, not participating seats, so `voted=78` cannot distinguish "16 seats, 2 per row"
from "2 seats, all rows". The live wave happens to be partitioned 10 rows/seat with 2 voters per row (measured), but
nothing enforces it. **Impact:** a closure sentence claiming a 16-seat review would be true to the counter and false
to the arm. **Smallest remediation:** print distinct bound voters and per-row voter ids; require band partition if
independence is being claimed.

## F8 — LOW — C2 binds by substring, C1 by line

`count-c2.py:169` tests `("ENTAIL %s %s" % (h, "entailed")) in out`; executed, the sentence
`I did NOT write ENTAIL <h> entailed anywhere.` binds the vote. The report side is anchored
(`ENTAIL_RE = ^\s*ENTAIL ...`), so the practical effect is a binding that tolerates negation and quotation in the
output — a false-positive path where C1 has (over-strict) line equality. **Smallest remediation:** normalize both
sides to the same line rule.

## F9 — LOW — 20k truncation can drop trailing vote lines

`inline-dispatcher.py:283` stores `str(h.output())[:20000]`. No historical instance (round-53: 0/67, round-54: 0/74
at the cap; round-53 had 1 null output), but a verbose seat whose vote lines sit last would bind nothing. Fails
closed. **Remediation:** none needed now; note in the seat contract.

## Confirmed limits (no defect)

- Non-frozen names do not count; fenced votes do not count; a voter absent from the record binds nothing; missing or
  malformed record fails closed (`checks/selftest-c1.py:161-192`; `selftest-c2.py:38-44`). Observed, not assumed.
- The docstrings' named limit is accurate: the arm proves a seat of that name was recorded echoing the line, not who
  wrote the report bytes and not that the judgment was made (`count-c1.py:35-38`, `count-c2.py:30-34`). The dispatch
  itself supplies each voter's hash list (`w1-dispatch.json`, task text), so binding proves the seat echoed its
  assigned hashes.
- Positive votes cannot be forged across seat names without write access to the record: the orchestrator captures
  each handle's output, and a sibling can only write report bytes (which buys dissent, not agreement).
- Round-54 → 55 transition: round-54 bound on the report alone; its 74 recorded outputs contain 0 line-start vote
  lines (4 substring mentions of the word), which is why round-55 added output binding — and why the fleet's habitual
  JSON `votes` dicts satisfy neither arm.

## Operational note

At HEAD no file under `.ufo/waves/round-55/w1/` is committed (`git ls-tree -r HEAD .ufo/waves/round-55/w1` empty), and
the counters read reports via `git ls-tree`/`git show` at R. A report left untracked at landing silently contributes
no votes — fail-closed but indistinguishable from a missing seat.

## Findings

| # | Severity | Finding | Evidence |
|---|---|---|---|
| F1 | HIGH | C1 output binding is exact-line equality after strip; the prefix branch at `count-c1.py:302` is unformatted dead code; array-shaped yields (4/4 sampled live C1 seats) bind 0 votes, and the 2-per-row design has zero margin → false unmet | `count-c1.py:299-303,402` ; `w1/Mo55Rc01.md`–`Mo55Rc16.md` (138 lines/78 rows) ; `agent://Mo55Rc01,05,07,12` ; `round-54/w1-results.json` ; executed emulation |
| F2 | MEDIUM | Dissent/overclaim/REPLACE are report-only and the report dir is shared-writable: any co-writer can force C1 dissent, C2 overclaim, or void a voter's entailed vote | `count-c1.py:303,385-387` ; `count-c2.py:169,173,264-265` ; `w1/Mo55En01.md` |
| F3 | MEDIUM | "Distinct voters" is filename-only; identical report bytes under two names count as two voters | `count-c1.py:295-303` ; executed emulation |
| F4 | HIGH | `w1-results.json` is not in the freeze and has no independent witness; orchestrator-written, L1-committed, counter-trusted → 2-vote gate reduces to L1 assertion | `evidence/freeze-sha256.txt:1-35` ; `inline-dispatcher.py:289-295` ; `count-c1.py:424-430` |
| F5 | LOW | Duplicate result names last-wins, no validation; verdict is entry-order dependent | `count-c1.py:291` ; `count-c2.py:153` ; executed emulation |
| F6 | LOW | C1 counts report-only dissent from a voter absent from the record; C2 skips such a voter | `count-c1.py:296-303` vs `count-c2.py:158` ; executed emulation |
| F7 | MEDIUM-LOW | Independence unmeasured: no counter reads the dispatch map; passing witnesses are 2 voters on all rows; `voted` counts rows, not seats | `count-c1.py` (0 dispatch refs) ; `selftest-c1.py:54-60,80` ; `selftest-c2.py:20-22` |
| F8 | LOW | C2 binds by substring; a negated/quoted sentence binds | `count-c2.py:169` ; executed emulation |
| F9 | LOW | 20k output truncation can drop trailing vote lines (no historical instance) | `inline-dispatcher.py:283` ; round-53/54 records |

No vote lines are emitted by this seat: sentinel, not a voter.

Hygiene: scratch `/fast/scratch/hyaku/mori-r55/Mo55Sent02` created and removed; disk guard read before work (26%
used, 594.6G free); no installs, no pacman, no git/jj mutation, no writes outside this report and scratch; only
read-only commands against the lane.
