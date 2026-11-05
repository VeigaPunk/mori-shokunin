# Round 92 — mori (L1 MoriR92, attempt 1) — lesson

Entering revision `f63d1ab030d4179576e494342f48ef8718e497a5`. Frozen contract
`.ufo/waves/round-92/contract.md` committed at `699f6276` (with `count-c1.py`, `count-c2.py`, the
do-nothing controls `evidence/controls-r92.txt`, `evidence/c1-missing-entering.txt` and
`evidence/census-before-full.txt`). One v1 wave `w1`, 11 seats. The landing commit is named in the
report (`.ufo/reports/round-92/mori.md`); this lesson cannot cite its own commit.

## Claims and their verdicts

- **C1 depth — every `corpus/knowledge/` entry carries the provenance trio in its first 12 lines.**
  Control at the entering revision: `C1=unmet knowledge=98 missing=19 floor=98`, exit 1
  (`evidence/controls-r92.txt`, `evidence/c1-missing-entering.txt`). Landing: the 19 files were
  patched (waves `Mo92K01Trio`, `Mo92K02Trio`; both verified move-only, Mistake 5). The
  after-receipt is at the landing revision (`evidence/after-r92.txt`). Verdict: the frozen predicate
  measures **presence** only, and the attack seat showed three forgeries pass it
  (`Mo92R01Atk`: fenced keys, empty values, unrelated body). The critic seat (`Mo92K03Crit` §1)
  judged a trio line to be traceability metadata, not a depth move under the lane's own bar (quotes
  and entailment). The lane reports C1 as **met as frozen; depth not established**; the depth ruling
  is for the non-author closure.
- **C2 freshness — the digest gate reports zero unresolved mismatches after supersession rows.**
  **Not met as frozen. Honest stop; not admitted.** Two defects in the frozen predicate, found in this
  round. Neither can be repaired without voiding the claim (contract §Ordering 4):
  1. Negative fixture B requires a successor row for S235 whose deletion exposes a mismatch. The
     registry already carries **S349**, a valid pre-existing successor of S235
     (`corpus/SOURCES.md` line 246 at f63d1ab0: `supersedes S235 —`, correct full digest). S235 is
     superseded by S349 regardless of any new row, so fixture B cannot print `DIGEST S235 mismatch`.
     The contract did not grep for this premise (Mistake 1).
  2. The frozen clause "exit 0 with prefix_only=31 unpinned=1" can only hold if the gate's exit rule
     ignores prefix-only and unpinned rows. The executor changed the rule that way; the critic
     (`Mo92K03Crit` §3, A6) and the L1 both rejected it, because QUALITY 193 says a prefix agreement
     fails the gate and that change would turn 31 failing rows green. The entering exit rule is
     restored in the landed tool.
  What landed for C2 (not a claim): the digest tool gains supersession and a selftest
  (`tools/mori-source-digest.py`: `DIGEST_SELFTEST pass=11 fail=0`, exit 0); the correction row S619
  (`supersedes S615`) is appended. S620 was **not** appended (rejected: redundant with S349, see the
  Gate). On the landed registry the tool reads `DIGEST S235 superseded-by S349`,
  `DIGEST S615 superseded-by S619`, `DIGEST_CHECK rows=122 ok=88 mismatch=0 superseded=2
  prefix_only=31 unpinned=1`, exit 1; the remaining exit 1 is the known QUALITY 193 debt. The frozen
  counter's verdict at the landing revision is in `evidence/after-r92.txt`.

Round verdict: **honest stop** (C2 unmet as frozen; C1 verifies as presence). Per the contract, this
lane does not admit either claim; the operator and the non-author closure rule on the trade.

## Work the round landed (not claims)

- The digest tool capability (supersession and selftest), demonstrated running (selftest 11/11 and
  the registry run above). Row added to the SCORECARD capabilities table.
- Correction row S619 for S615's recorded digest (round-91 correction of record C-1). Its digest is the
  full sha256 of the pinned copy, recomputed this round.
- Provenance trio lines on 19 knowledge entries (C1 presence). Each `verified-at` names the admission
  commit of its file (`git log --diff-filter=A`); each `recheck` is taken from the entry's own body or
  is `manual, <path:line>` where the body gives none.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| `unchecked-registry-premise` — the C2 contract assumed no existing successor of S235 and froze a fixture on that assumption; S349 already supersedes S235 | `.ufo/waves/round-92/w1/Mo92E01Digest.md` §5; `corpus/SOURCES.md` S349 (line 246 at f63d1ab0); `git grep -n 'supersedes S235' f63d1ab0 -- corpus/SOURCES.md` → rc 0 (`evidence/premise-and-hostpath.txt`) | none — no step grepped a frozen predicate's registry premise before the freeze | QUALITY 196: grep every premise a predicate names and commit the grep output with the contract. Shown able to fail: the grep returns S349 where the contract assumed none. |
| `frozen-exit-rule-relaxation-proposed` — the executor changed the gate's exit rule so that a predicate's exit-0 clause could hold, turning 31 prefix-only rows green | `Mo92E01Digest.md` §2; `Mo92K03Crit.md` §3 (A6); `Mo92R02Atk.md` §3; QUALITY 193 | QUALITY 193 (caught by two seats and the L1; the executor flagged it as a decision) | Exit rule restored to the entering rule; the two executor arms that encoded the relaxed rule were changed to rc 1. Shown able to fail: the restored rule gives rc 1 on the prefix-only arm and the unpinned arm (`DIGEST_SELFTEST pass=11 fail=0`); the relaxed rule would give rc 0 on both. |
| `truncated-receipt` — `evidence/census-before.txt` was written with `tail -2`, keeping 2 of 44 lines and hiding 41 W04 warnings | `evidence/census-before.txt` (2 lines); `evidence/census-before-full.txt` (44 lines, exit 0, rows 391, W04 = 41); `Mo92R03Sweep.md` §3 | none — the L1 wrote the receipt without a diff against a fresh run | The full receipt is `census-before-full.txt`, from a clean clone at f63d1ab0. The truncated file is kept as evidence of the defect, not rewritten. Shown able to fail: `wc -l` 2 versus 44. |
| `fleet-root-scratch` — the L1 wrote `.ufo/mo92-*` scratch files (a counter probe and its output) into the fleet root during the freeze | removed by the L1; the fleet-root `.ufo` listing after removal is in `evidence/fleet-root-after-removal.txt` (no `mo92` entries) | none — the L1 did not apply the scratch-root rule to its own work | Not counted as a fix (no QUALITY criterion, no able-to-fail claim): the scratch-root rule of the wave contract is applied from this round on. All L1 scratch is under `/fast/scratch/hyaku/mori-r92/lead/`. |
| `moved-body-lines` — the instruction was to add only missing keys, but 12 files carried 18 trio key lines in the body, outside the first 12 lines; the scribes moved those lines to the header | `Mo92K01Trio.patch`, `Mo92K02Trio.patch`; `evidence/trio-moveonly.txt` (per-file check) | none — the frozen counter (first 12 lines) and the no-duplicate rule could not both hold without a move | Move-only check (python, `evidence/trio-moveonly.txt`): every removed line reappears byte-identical among the additions, except two removed blank lines (drift-pin-r10, lane-silence-r2), disclosed here. Shown able to fail: the check reports `removed_not_reappearing=1` for those two files, so a body edit would be reported. |

## Corrections of record

- C-2 (round 91) said the S235 correction was deferred to round 92. In fact S349 already corrected
  S235 (pre-existing). The C-2 record is unchanged (append-only); this lesson is the correction. The
  S235 row's own recorded digest is still wrong, and S349 is the valid successor.
- `considerthese/2026-10-25.md` proposal 2 gave the host-home-path count as 13 files. The measured
  count at f63d1ab0 differs (Assimilation and considerthese).

## Gate (sources, protocol §2b)

| Row | URL | Access and recomputation | Located quote (≤25 words) | Decision |
|---|---|---|---|---|
| S619 | https://docs.python.org/3/library/ast.html (pinned copy `.ufo/waves/round-90/w1/Mo90S01Sources/sources/python-ast-3.15.2.html`) | 2026-11-05; full sha256 `7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b0f83b9a8a42f5`, 362493 bytes, re-hashed at f63d1ab0 (`Mo92Sc01Src`) | "Recursively yield all descendant nodes in the tree starting at node" (counted in the tag-stripped text by the scout) | **admit** (mined; used-by this lesson): correction of record C-1; the ast facts of S615 are unchanged |
| S620 | (not written) | — | — | **reject** (not written): S349 already supersedes S235 with the same full digest `9855a4986a312dfc946b1b97b6010a8e4f1e65a4a30dca99359e6df057ad8020`. The scout also measured the S235 copy: the quoted iSulad bullet is at PDF page 27 (printed page 25), so the anchor a new row would need is that page note; flip: S349 found invalid, or a different digest for the S235 copy |
| S621 | FIPS PUB 180-4, Update 1 landing page — https://csrc.nist.gov/pubs/fips/180-4/upd1/final (PDF linked there) | 2026-11-05; landing page HTTP 200 (read tool); PDF fetched 833315 bytes, sha256 measured by the scout and not retained as a copy (no digest recorded in the row) | "The final result of SHA-256 is a 256-bit message digest." (10 words, section 6.2, printed page 21, grep -c -F = 1) | **queued** (opened; no knowledge entry cites it this round); the 64-hex digest semantics are its `teaches` cell |

Census: before (full, clean clone at f63d1ab0) `rows=391`, exit 0 (`evidence/census-before-full.txt`);
after (landing working tree, `evidence/census-after.txt`) `rows=393` (S619 and S621 appended; S620 not written).

## Assimilation and considerthese

- **Assimilation: none.** `merge/mori/` (shokuknow, corpus-expansion-1) stages 136 proposed rows and 80
  knowledge entries; none of its themes fits this round's two claims, and mori is not in the
  wave-4 quarantine-first set.
- **considerthese (one item): `considerthese/2026-10-25.md` proposal 2 (host-path portability list).**
  Grounded through the lane's own bar: the count was measured at f63d1ab0
  (`evidence/premise-and-hostpath.txt`): `git grep -l '/home/vgpnk' f63d1ab0 -- tools | wc -l` = 3
  (`tools/mori-blind-check.sh`, `tools/mori-misroot-sweep.py`, `tools/mori-round17-context-check.py`);
  tracked `.ufo/waves/*.py|*.sh` = 436; tracked `*.py|*.sh` anywhere = 458. The reflection's 13 is not
  reproduced. Landed as QUALITY 197, red at entering; the three tools are debt, not fixed this round.

## Trend verdicts (lane)

Recorded in the report. Expansion: unchanged (no knowledge entry admitted; one correction row).
Quality: unchanged as to admissions; the exit-rule relaxation was refused, and the premise check is
now a criterion. Discernment: the non-author closure must rule on C1 depth and on the frozen-predicate
defect; the lane's gate decisions above are the sample (admit S619, reject S620).

## Planned (round 93)

1. Re-declare C2 with the S349 premise and the exit rule stated, and the premise grep committed before
   the freeze (QUALITY 196); fixture B constructed on S349, not on a new row.
2. The three tools under `tools/` with a host home path (QUALITY 197): a bounded change of its own.
3. Carried: the 31 prefix-only rows and the 1 unpinned row (S125) as reported debt; the round-91
   C1/C2 gate-clause arming (families must be mapped from the subject's real labels before any
   re-declaration); the nonce guard for the round-90 gate (QUALITY 191); the supersession record of the
   round-87 arm pins.

## Correction of record (round 93) — appended, not an edit in place

Corrects the sentence wrapped over lines 51–52 of this file, in `## Work the round landed`: "Each
`verified-at` names the admission commit of its file (`git log --diff-filter=A`)". At the round-92 landing
`9dce2ca6` that sentence was false: it held for 7 of the 19 trio files and failed for 12.

- At `9dce2ca6`: `python3 -I .ufo/waves/round-93/count-c1.py 9dce2ca6 --repo <lane> --report` →
  `adm_ok=7 adm_fail=12` (same counts at `7b3fe9d5`, `.ufo/waves/round-93/evidence/measure-c1-entering.txt`).
- Round 93 repaired the 12 `verified-at:` values (`Mo93E02Verif`; landing `1fc921cf75afa6650b9dc9451b33a2ec0610ae0a`).
  At that landing `C1=met trio=98 claim_r92_true=1 adm_ok=19 adm_fail=0`
  (`.ufo/waves/round-93/evidence/after-c1-1fc921cf75afa6650b9dc9451b33a2ec0610ae0a.txt`). The sentence is true
  of those 19 files at that landing.

Scope: the sentence is true of the 19 round-92 trio files, not of the 98 knowledge entries, and the commit
form is this lane's stricter criterion (LEARNING.md accepts a date). The round-92 verdicts are not changed by
this entry: C1 presence met as frozen, depth not established; C2 unmet and not admitted. The counter checks
that the short hash appears inside `verified-at:` (a plain substring; boundary check routed in
`corpus/lessons/round-93.md`).
