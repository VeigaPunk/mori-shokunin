# Mo49ScribeScorecard — round 49, wave w1

Seat: leaf scribe (no subagents). Assignment: draft the `## Round 49` declaration section for
`SCORECARD.md` in the style of `## Round 48`, then audit the Axes table. Deliverable below is a
fenced draft; I edited no lane file. All reads absolute and read-only; no counter was run (the
assignment did not instruct it), so every `After` value is an unfilled `<…>` marker, not a result.

## Evidence observed

| # | command | output (abridged) | exit |
|---|---|---|---|
| 1 | `git rev-parse HEAD HEAD^` | `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115` / `b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86` | 0 |
| 2 | `sha256sum -c .ufo/waves/round-49/evidence/freeze-sha256.txt` | 31 entries, none differ (contract, both counters, 7 controls, 13 evidence receipts, 4 source copies, 4 assimilation files; the manifest is the 14th `.txt` and does not list itself); `grep -cv ': OK$'` on stderr → `0` | 0 |
| 3 | `cat` each file under `.ufo/waves/round-49/evidence/` | quoted below; C1 lines all end `rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86` | 0 |
| 4 | `sed -n '1,60p'` / `sed -n '290,320p'` `count-c1.py`; `grep -n 'honest_unmet = sum\|len(results) - 1'` | `verdict()` at `:298`; `honest_unmet` at `:300`; result line at `:304-305` with `variants=%d rev=%s` from `len(results) - 1`; `real-opaque` staged at `:266`, ordered at `:213` | 0 |
| 5 | `sed -n '1,45p'` + `grep -n 'C2='` `count-c2.py` | predicate/MIN_CLAIMS=8/MIN_SOURCES=3/word 6-25/`COPIES` with frozen sha256; result line `:188-192`, `failed=` only when unmet | 0 |
| 6 | `cat controls/stub-filename-sniffer.py stub-always-met.py` | sniffer: `unmet` iff argv/TMPDIR matches `variant-[JN]\d\|c1-[JN]\d`, else prints `PIN_CHECK=met` | 0 |
| 7 | `sha256sum` + `cmp` on `control-c1-stub-always-met.txt`, `control-c1-stub-filename-sniffer.txt` | both `673966107b7ca1f0e415699e2bdf9f3836299fdcdea86c769b929b0c250331e3`; `cmp` rc 0 (byte-identical) | 0 |
| 8 | `grep -c 'S485\|S486\|S487\|S488' corpus/SOURCES.md`; `grep -n journal-reach-r49 corpus/SOURCES.md` | `0`; no match | 1, 1 |
| 9 | `ls corpus/knowledge/ \| grep -i journal` | `journal-alarm-routing-r14.md`, `journal-cursor-window-r16.md`, `journal-disk-usage-total-r51.md`, `journal-positive-evidence-r15.md`, `structured-journal-scopes-r13.md` — no `journal-reach-r49.md` | 0 |
| 10 | `ls corpus/evidence/sources-r49/` | the four frozen copies present (`journald.conf.5.html`, `systemd-journald.service.8.html`, `journalctl.1.html`, `host-journal-reach.txt`) | 0 |
| 11 | `sed -n '1,30p' tools/mori-pin-check.py` | header says `v3 (round 48, wave w1)`; no v4 header at `0df17b7b` | 0 |
| 12 | `awk -F'\|' 'NR==248'` `corpus/SOURCES.md` | `S351: status= rejected \|opened= 2026-10-24 \|usedby= —` | 0 |
| 13 | `git diff 63eecf27…HEAD -- SCORECARD.md \| grep -E '^[+-]\| (coverage\|…\|adjacency) '` | no output — no Axes row changed across rounds 47-48 | 1 |
| 14 | `grep -n 'No axis table cell changed\|Axis harm\|No score change is claimed by the lane'` `SCORECARD.md` | `2620`, `2621`, `2568`, `2590`; `Score changes were not admitted` at `2549` | 0 |
| 15 | `cat .gitignore`; `git status --porcelain \| grep -c '^?? .scratch/'` | 4 lines (`.ufo/interactive-sessions/`, `.ufo/worktrees/`, `__pycache__/`, `*.pyc`) — no `.scratch/`; 162 untracked `.scratch/` directories | 0, 0 |
| 16 | `wc -l evidence/census-start.txt` | 21 (20 `W04` duplicate-url lines + one `ok`) | 0 |
| 17 | `grep -rn 'Axes\|score' .ufo/waves/round-49/w1/*.md` | only unrelated uses (`scores the two new bind-rule case rows`, `rev-scorecard-claims`, `scored through count-c2.evaluate()`); no seat claims a score move | 0 |

Receipt lines I quote (frozen bytes, check 2):

- `control-c1-tool-v3-entering.txt`: `C1=unmet junk_met=9 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86` / `exit=1`; N1-N9 each `expect=unmet got=met rc=0`.
- `control-c1-stub-always-met.txt`: `C1=unmet junk_met=18 honest_unmet=0 real=met errors=0 variants=26 rev=…` / `exit=1`.
- `control-c1-stub-always-unmet.txt`: `C1=unmet junk_met=0 honest_unmet=8 real=unmet errors=0 variants=26 rev=…` / `exit=1`.
- `control-c1-stub-filename-sniffer.txt`: `C1=unmet junk_met=18 honest_unmet=0 real=met errors=0 variants=26 rev=…` / `exit=1`.
- `control-c1-sniffer-under-r48-counter.txt`: `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=…` / `exit=0`.
- `control-c1-tool-r48-surface-fixes.txt`: `C1=unmet junk_met=1 … variants=26` / `exit=1` (N9 `got=met`).
- `control-c1-tool-r48-r11-only.txt`: `C1=unmet junk_met=7 … variants=26` / `exit=1` (N1-N7 `got=met`).
- `control-c1-tool-r48-merged-witness.txt`: `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26 rev=…` / `exit=0`.
- `control-c2-donothing.txt`: `C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=bad provenance=bad rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 failed=entry_absent,pins` / `exit=1`.
- `selftest-c1.txt`: last line `C1_SELFTEST pass=44 fail=0`; `PASS handles_carry_no_variant_name  []`, `PASS order_not_expect_sorted  `, `PASS filename_sniffer_not_met  C1=unmet junk_met=17 honest_unmet=0 real=met errors=0 variants=24 rev=b3e3453d…`.
- `selftest-c2.txt`: last line `C2_SELFTEST pass=26 fail=0`.
- `sweep-journal-rows.txt`: `SystemMaxUse SOURCES.md=0 knowledge=0`, `MaxRetentionSec SOURCES.md=0 knowledge=0`, `journald\.conf SOURCES.md=0 knowledge=1`, `RuntimeMaxUse SOURCES.md=0 knowledge=0`, `vacuum SOURCES.md=3 knowledge=12`.

## Draft — append to `SCORECARD.md` after line 2624

```md
## Round 49 — the opaque-handle junk battery (C1) and the journal retention-reach entry (C2)

L1 MoriR49, attempt 1. Entering tip `b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86` (the freeze commit
`0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115`'s parent); freeze `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115`
(`.ufo/waves/round-49/contract.md`; both counters, seven controls, four source copies and their 13 receipts
committed before any seat, all 31 frozen paths verified by `sha256sum -c`). Scores entering: coverage 6,
operability 7, depth 5, freshness 5, calibration 5, adjacency 6; both claims work a lowest (tied 5) axis.
No score change is claimed by the lane; the non-author closure rules.

| Claim | Axis (held) | Counting command | Before (entering `b3e3453d`) | After |
|---|---|---|---|---|
| C1 the pin reconciler rejects eighteen frozen junk edits and accepts seven honest edits and the real registry while every variant reaches it under an opaque name | calibration 5 | `python3 .ufo/waves/round-49/count-c1.py --tool tools/mori-pin-check.py --rev R` | entering v3 tool: `C1=unmet junk_met=9 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86`, `exit=1` — `evidence/control-c1-tool-v3-entering.txt`; N1-N9 each print `expect=unmet got=met rc=0` | measured at the landed tip, appended below |
| C2 the FR1 journal retention-reach entry: ≥8 rows, each a located quote from one of four committed copies (three manual pages and the host receipt), at least three copies used | depth 5 | `python3 .ufo/waves/round-49/count-c2.py R` | `C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=bad provenance=bad rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 failed=entry_absent,pins`, `exit=1` — `evidence/control-c2-donothing.txt` | measured at the landed tip, appended below |

Reading of the C1 line: the predicate is its `C1=… variants=26` prefix; the trailing ` rev=R` field is the
counter's own (`count-c1.py:304-305`), read the same way as round 48's after cell (`SCORECARD.md:2617`).
`variants=26` counts 18 junk edits (J1-J8, N1-N10), 7 honest edits (H1-H7) and the real registry; a 27th run —
the real registry read a second time through an opaque-named copy — is listed and scored but not counted
(`len(results) - 1`), so `honest_unmet=8` on a tool that fails every `met`-expected run is 7 honest edits plus
that copy. C2's `pins` arm is the four committed copies against the counter's frozen sha256; it reads `bad`
before the copies exist at `b3e3453d` and at the landed tip.

Controls, each scored with this counter before any data, none reaching `met` (every line quoted from `evidence/`):

| Control | Quoted result | Reading |
|---|---|---|
| do-nothing: entering v3 tool (`controls/tool-v3-entering.py`, sha256 `85a89a3b…`) | `C1=unmet junk_met=9 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d…`, `exit=1` | the tool the lane entered with cannot reach the target; N1-N9 are the nine shapes it still accepts |
| `controls/stub-always-met.py` | `C1=unmet junk_met=18 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d…`, `exit=1` | rejects nothing |
| `controls/stub-always-unmet.py` | `C1=unmet junk_met=0 honest_unmet=8 real=unmet errors=0 variants=26 rev=b3e3453d…`, `exit=1` | rejects everything, including the real registry |
| `controls/stub-filename-sniffer.py` | here `C1=unmet junk_met=18 …`, `exit=1`; under the round-48 counter `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=b3e3453d…`, `exit=0` (`evidence/control-c1-sniffer-under-r48-counter.txt`) | the opaque handles close the round-48 filename leak; the sniffer falls back to `met` when no variant name reaches it, so its round-49 receipt is byte-identical to the always-met stub (sha256 `67396610…`) and the leak evidence is the round-48-counter receipt plus the `PASS filename_sniffer_not_met` arm |
| `controls/tool-r48-surface-fixes.py` | `C1=unmet junk_met=1 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d…`, `exit=1` (N9) | round 48's five surface rules alone leave D7 open |
| `controls/tool-r48-r11-only.py` | `C1=unmet junk_met=7 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d…`, `exit=1` (N1-N7) | R11 alone leaves the surface shapes open |
| `controls/tool-r48-merged-witness.py` | `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d…`, `exit=0` | feasibility witness only; not the claim's tool and not round-49 seat output |
| C2 do-nothing | `C2=unmet … failed=entry_absent,pins`, `exit=1` | no entry, no source rows |
| C1 selftest arms | `C1_SELFTEST pass=44 fail=0` (`evidence/selftest-c1.txt`) | variant application, pairwise-distinct variants (23), `PASS handles_carry_no_variant_name  []`, `PASS order_not_expect_sorted`, the sniffer arm, the eight fixture lines (`fixture_False_*` and `fixture_True_*`, four behaviours each), `PASS lane_head_unchanged` |
| C2 selftest arms | `C2_SELFTEST pass=26 fail=0` (`evidence/selftest-c2.txt`) | entry-level controls with their reason isolated: staged entry byte-exact, altered quote, wrong-copy quote, short and long quote, duplicate quote, unmined row, row opened another day, missing `used-by`, digest mismatch, script/style/comment text in a copy, fence-hidden table, wrong header |

Disclosure the closure should weigh (contract, freeze receipts): the merged-witness control reaches the target
line at the entering revision, so the target tool bytes are largely pre-existing round-48 seat output. Round 49's
C1 work is (a) landing and testing the successor reconciler in `tools/` with the K-class rules and their selftest
arms, (b) the opaque-handle counter itself — SKILL.md copy and scratch directory named by a sha256 prefix of
their bytes, run order taken from that hash, a throwaway fixture repository for the two edits that change a second
tracked file, three new honest edits (H5-H7) — and (c) the false-red audit of the new rules against earlier
`SKILL.md` revisions. The reconciler capability was first demonstrated in round 47; the K-class rules and the
opaque handles are what is new.

Limits named before data (contract): the variants are the classes rounds 47-48 found, not the class of all junk —
round 48's K2-K8 (env-prefix substitution, pin deletion, pins outside the self-test cell, namespace join, floor
slack, line-count rebinding, rc-free pins) are not in this predicate and stay routed; a tool can pass by being
narrower than the junk, so H1-H7 and the real registry are part of the predicate; the counter does not run the
tool's own `--selftest`; wave 2 attacks with fresh classes and reports survivors as limits, never as a re-score.
For C2 a located quote proves the quoted words occur in the committed copy, not that the claim cell follows from
them, not that the page is unchanged today, and — for `host-journal-reach.txt` — not that the host still reads
this way: the receipt is the 2026-10-25 capture and the journal total moved from 269M to 56M within one day of
S470's entry. Coverage sweep before data (`evidence/sweep-journal-rows.txt`): `SystemMaxUse SOURCES.md=0
knowledge=0`, `MaxRetentionSec SOURCES.md=0 knowledge=0`, `RuntimeMaxUse SOURCES.md=0 knowledge=0`, and
`journald\.conf SOURCES.md=0 knowledge=1` — no registry row named the page, one knowledge mention existed. The
S351 flip is recorded as a new row whose `teaches` opens `supersedes S351 —`; S351 stays rejected
(`corpus/SOURCES.md:248`).

### capabilities: demonstrated round 49

| Capability | What it can now do | Evidence | First-working round |
|---|---|---|---|
| pin reconciler (v4) | reject the nine N-class junk shapes the entering v3 scores `met` (N1-N9) — the riders the contract routes from `w2/R48CritV3Junk1.md`, including the D7 shape that rule R11 closes — while accepting H1-H7 and the real registry | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=<v4 selftest tally> fail=0`; `<after-c1 receipt>` | 49 for the K-class rules and their arms; the reconciler itself first worked in 47 |
| opaque-handle junk-variant counter | score a registry checker against 18 junk and 7 honest edits plus the real registry without telling it which edit it is scoring — hash-named SKILL.md copy and scratch directory, hash-ordered runs, the two second-file edits built in a throwaway fixture repository, and the real registry read twice | `python3 .ufo/waves/round-49/count-c1.py --selftest` → `C1_SELFTEST pass=44 fail=0`; `PASS handles_carry_no_variant_name  []`; controls `evidence/control-c1-*.txt` | 49 |

No axis table cell changed and no score change is claimed: both claims work axes already at 5, the Axes table's
last-change cells read depth `round 31` and calibration `round 25` (`SCORECARD.md:12,14`), and no Axes row has
changed since round 47's freeze `63eecf27` (`git diff 63eecf27..HEAD -- SCORECARD.md` shows no such line).
Planned (round 50): land round 48's K2-K8 classes as frozen variants (they stay routed here); score the tool's
own `--selftest` as a counter arm so a narrow tool cannot pass while its arms fail; carry whatever wave-2
survivors this predicate reports as routed defects, never as a re-score; re-open each journal-reach quote against
the page text around it, as wave 2 does, and re-date the host receipt whose journal total moved 269M to 56M within
one day.
```

## Draft — measured-outcome appendix template (fill after wave 2; do not commit unfilled)

```md
### Round 49 measured outcome (appended after wave 2; the table above is the declaration)

| Claim | After (measured at `<landed tip>`) | Verdict proposed for the closure |
|---|---|---|
| C1 | `<C1=met|unmet junk_met=N honest_unmet=N real=… errors=N variants=26 rev=<landed tip>>`, rc `<0|1>` — `.ufo/waves/round-49/evidence/after-c1-<label>.txt` | `<verified|unprovable|not verified>` with `<the wave-2 survivors and any receipt mismatch>` |
| C2 | `<C2=met|unmet claims=N located=N quote_missing=0 bad_rows=0 sources=S source_rows=ok pins=ok provenance=ok rev=<landed tip>>`, rc `<0|1>` — `evidence/after-c2-<label>.txt` | `<…>` with `<wave-2 context review of every row, and the one-day host drift>` |
```

## Axes-table audit — which cells would change if the closure grants C1 and C2

**Answer: `none claimed`.** No Axes cell moves, and the evidence says so in five places:

1. The Axes table's scores are the ones the round-49 contract states as entering (`SCORECARD.md:10-15`:
   coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6 — identical to the contract's
   "Scores entering" line). C1 is calibration 5, C2 is depth 5; neither proposes a number.
2. No Axes row has changed in the two rounds that ran the same declaration shape:
   `git diff 63eecf27..HEAD -- SCORECARD.md | grep -E '^[+-]\| (coverage|operability|depth|freshness|calibration|adjacency) '`
   → no output, exit 1.
3. Round 48 handled the same question the same way, verbatim: "No axis table cell changed and no score change is
   claimed." (`SCORECARD.md:2620`) and "Axis harm: `w2/R48RevSkillScore.md` found the Axes table unchanged."
   (`:2621`) — i.e. the lane recorded the audit's answer in the round section and left the table alone.
   Round 47: "No score change is claimed by the lane; the non-author closure rules." (`:2568`); round 45:
   "Score changes were not admitted; scores remain coverage 6, operability 7, depth 5, freshness 5, calibration 5,
   adjacency 6." (`:2549`).
4. No wave-1 report of this round asks for a cell change: the only "score" hits in `.ufo/waves/round-49/w1/*.md`
   are one probe scoring two case rows, one scratch name, and one `count-c2.evaluate()` call.
5. What a grant would actually license: a *grade* ("calibration improved", "depth improved") with no number, which
   the table's own precedent (`depth … latest admitted closure grades depth improved … and states the score stays
   5`, `SCORECARD.md:12`) treats as a pointer refresh in a later correction round, not a score move. If the closure
   instead grades either axis *harmed* — e.g. C1 met but wave 2 shows the tool reads harness state, or C2 met with a
   row whose quote does not support its claim — then the honest repair is the round's section plus a routing row,
   still not a silent cell edit; the lane's history shows score moves only when a closure states a number
   (depth `4 → 5` at `SCORECARD.md:613`; operability's `6 → 7` in round 13's table, quoted in the Axes cell at
   `SCORECARD.md:11`).

No cell can legitimately move under either grant; a harmed grade would be a closure statement, and this draft
pre-commits no number.

## Limits of this report

- **UNVERIFIED:** both `After` values. I did not run `count-c1.py` or `count-c2.py`; the assignment did not instruct
  it, and a run is a measurement of landed bytes that do not exist yet (`corpus/knowledge/journal-reach-r49.md`
  absent, no S485-S488 rows, `tools/mori-pin-check.py` still headed `v3` at `0df17b7b`). The draft's After columns
  stay "measured at the landed tip, appended below".
- **UNVERIFIED / contract-stated:** the merged witness's own `PIN_CHECK_SELFTEST 65/65` (contract, freeze receipts);
  I did not execute `controls/tool-r48-merged-witness.py --selftest`. The witness's `C1=met` line *is* observed in
  `evidence/control-c1-tool-r48-merged-witness.txt`.
- **UNVERIFIED:** wave-2 outcomes. The appendix above is a template with markers, not a result.
- The predicate prefix/`rev=` reading is my reading of `count-c1.py:304-305` combined with round 48's own after-cell
  quoting (`SCORECARD.md:2617`); the L1 owns whether the closure reads it that way.
- I did not check whether the counter's four `COPIES` urls are still live pages (read-only, out of seat scope) and
  did not touch `/home/vgpnk/Projects/shokuknow*`.
- Hygiene: I ran no lane tool, so no `TMPDIR` scratch of mine exists. One temporary file `/tmp/r49sha.err` held
  `sha256sum -c` stderr inside a plain digest check and was removed; `ls /tmp/r49sha.err` now exits 2.

## Findings

- **MED** — `contract.md` P-C1 and P-C2 print the target as `C1=met junk_met=0 honest_unmet=0 real=met errors=0
  variants=26` / `C2=met … provenance=ok`, but both counters append a ` rev=<R>` field to that line
  (`count-c1.py:304-305`, `count-c2.py:188-190`; every freeze receipt ends `rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86`).
  A closure that tests the predicate as a whole-line equality would read the met receipts as unmet. The lane's
  convention is the prefix (round 48's after cell quoted without `rev`, `SCORECARD.md:2617`); my draft states the
  reading rule explicitly so the closure need not re-derive it.
- **MED** — carried routed defect unlanded at the freeze tip: `.gitignore:1-4` has no `.scratch/` entry, and the lane
  tree at `0df17b7b` holds untracked `.scratch/` directories — `git status --porcelain | grep -c '^?? .scratch/'` →
  **162**, then **174** on a re-count minutes later (the number is live while seats run counters), plus **11**
  untracked `.ufo/waves/round-40/scratch/*` directories from an older round; `git status --porcelain | grep -c '^ M'`
  → `0`, so no tracked file is modified by them. The round-49 close must add the ignore entry and clean, or the
  round-48 routed defect ("`.scratch/` residue") recurs in the same shape. I left it out of the drafted declaration
  on purpose: the L1 may close it this round, and a committed declaration should not carry an open hygiene item as
  if it were settled.
- **LOW** — `honest_unmet=8` on `stub-always-unmet` (`evidence/control-c1-stub-always-unmet.txt:28`) against seven
  honest edits: `count-c1.py:300` counts every `expect=met` row except `real`, which includes the uncounted
  `real-opaque` run (`:266`, ordered at `:213`). A closure table that reads the field as "8 honest edits" would
  misstate the variant set; my draft spells out the accounting.
- **LOW** — evidence duplication: `control-c1-stub-always-met.txt` and `control-c1-stub-filename-sniffer.txt` are
  byte-identical (both sha256 `673966107b7ca1f0e415699e2bdf9f3836299fdcdea86c769b929b0c250331e3`, `cmp` rc 0),
  because `controls/stub-filename-sniffer.py:10-13` prints `PIN_CHECK=met` when no variant/scratch name reaches it,
  and the receipts record only `got`/`rc`, not the tool's stdout. The sniffer control therefore proves "does not
  pass" and nothing more; the leak-closure evidence a closure should cite is
  `control-c1-sniffer-under-r48-counter.txt` (`C1=met … variants=12`, exit 0) plus selftest arm
  `PASS filename_sniffer_not_met … junk_met=17 … variants=24`. My draft's controls table says this in the row.
- **LOW** — `variants=26` is `len(results) - 1` (`count-c1.py:305`) over 27 listed runs; a reader taking the field
  as a run count is off by one. Same family as the `honest_unmet` finding; both are read-time hazards, not predicate
  defects (P-C1 is met by the prefix as written).
- **LOW** — the C2 sweep's own line `journald\.conf SOURCES.md=0 knowledge=1` (`evidence/sweep-journal-rows.txt:4`)
  shows one pre-existing `corpus/knowledge/` mention of the page. The contract's claim ("no row names the
  `journald.conf` page") holds for SOURCES, but a closure or lesson summary saying the theme was absent from the
  knowledge corpus would overstate it. My draft quotes the line with the nuance.
- **LOW** — capability attribution risk: `controls/tool-r48-merged-witness.py` reaches the full target line at the
  entering revision (`evidence/control-c1-tool-r48-merged-witness.txt`, exit 0), so a `### capabilities` row could
  be read as new round-49 capability. The contract already discloses this; my draft repeats it in the declaration
  and pins the v4 row's "first-working round" to the K-class rules, with the reconciler itself attributed to 47.
