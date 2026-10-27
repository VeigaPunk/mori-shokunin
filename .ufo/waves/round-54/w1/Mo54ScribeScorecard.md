# Mo54ScribeScorecard — SCORECARD.md additions for round 54 (drafts only; the L1 integrates)

Seat: `Mo54ScribeScorecard` (scribe, wave w1, round 54, `2026-10-27`). Lane root
`/home/vgpnk/Projects/shokunin/mori-shokunin` at HEAD `2d0347a3` (`round-54: wave w1 spec (74 seats, v2 validated:
24 voters, 39 attack seats), dispatch payload, at-data receipts`). Frozen contract `.ufo/waves/round-54/contract.md`
(sha256 `1e06f99f9235…`, `evidence/freeze-sha256.txt:1`) read first.

Behaviour: two fenced drafts for `SCORECARD.md` — (1) an appended `**Round-53 correction:**` naming the landed
receipts of the round-53 C1/C2 rows, with the token identity of landed vs salvage verified here; (2) the
`## Round 54` section in the round-53 house shape (claim table with `[L1 fills]` After cells, controls line, limits,
`Planned (round 55)`). No product file, counter, control, kill rule or corpus byte was changed; the only write is
this report. The counters were **not** re-run by this seat (their replay is `w1/Mo54ExecC1Replay.md`,
`Mo54ExecC2Replay.md`, `Mo54ExecControlsReplay.md`); every number below is read from a receipt or a report file and
named as such.

## 1. Gate — the round-53 receipts are token-identical apart from `rev=` (seat item 1)

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-53/evidence
$ grep -n '^C[12]=' c1-at-landed.txt c1-at-salvage.txt c2-at-landed.txt c2-at-salvage.txt
c1-at-landed.txt:3:C1=met scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok …
c1-at-salvage.txt:3:C1=met scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok …
c2-at-landed.txt:3:C2=met tool=present selftest=pass n=31 fixtures=80 agree=80 disagree=0 registry=ok live=ok rev=0b36d2…
c2-at-salvage.txt:3:C2=met tool=present selftest=pass n=31 fixtures=80 agree=80 disagree=0 registry=ok live=ok rev=0df80…
$ diff <(grep '^C1=' c1-at-landed.txt | sed -E 's/ rev=[0-9a-f]{40}$//') \
       <(grep '^C1=' c1-at-salvage.txt | sed -E 's/ rev=[0-9a-f]{40}$//'); echo "rc=$?"
rc=0
$ diff <(grep '^C2=' c2-at-landed.txt | sed -E 's/ rev=[0-9a-f]{40}$//') \
       <(grep '^C2=' c2-at-salvage.txt | sed -E 's/ rev=[0-9a-f]{40}$//'); echo "rc=$?"
rc=0
$ for f in c1-at-landed.txt c1-at-salvage.txt c2-at-landed.txt c2-at-salvage.txt; do
    printf '%s ' "$f"; grep -E '^C[12]=' "$f" | sed -E 's/ rev=[0-9a-f]{40}$//' | wc -w; done
c1-at-landed.txt 15
c1-at-salvage.txt 15
c2-at-landed.txt 9
c2-at-salvage.txt 9
```

`diff` prints nothing and exits 0 for both claims; the token counts are equal (15 C1 tokens, 9 C2 tokens). The only
difference is the trailing `rev=`: `0b36d23e596276c70725873621fe15a28c87189f` (landed) versus
`0df803033fba2386b10f5dcc6aa96bdef65cba15` (salvage). So the correction's claim "token-identical apart from `rev=`"
holds, and no number in either After cell changes.

## 2. Gate — the correction's other two facts

1. **The rows do cite the at-salvage receipts.** Extracted from the committed cells at `2d0347a3`
   (`awk -F'|' 'NR==2796{print $6}' SCORECARD.md`, `…NR==2797…`): the round-53 C1 After cell ends
   "`…` rc 0 — `evidence/c1-at-salvage.txt` (R = `0df80303`; the at-landed re-run is named in the round-53 report)`"
   and the C2 After cell "`…` rc 0 — `evidence/c2-at-salvage.txt` (R = `0df80303`; the data commit read `n=23`,
   `evidence/c2-at-data.txt`; the at-landed re-run is named in the round-53 report)`". Both at-salvage, as the
   correction says.
2. **`0b36d23e` is the revision the round-53 report measures.** `corpus/lessons/round-53-verifier-spotcheck.md:6-7`
   ("receipts measured at `0b36d23e596276c70725873621fe15a28c87189f`") and `:49` ("at-salvage receipts
   (R = `0df80303`), not the final integration tip `0b36d23e` that the report measures"). The landed receipt files
   exist in the lane: `git ls-tree -r --name-only 39dcf4d7 -- .ufo/waves/round-53/evidence` lists
   `c1-at-landed.txt` and `c2-at-landed.txt`.

State of the working tree, read-only: `git diff --stat SCORECARD.md` → `1 file changed, 15 insertions(+)`. The two
correction blocks are **already present, uncommitted**, at `SCORECARD.md:2850-2856` (`**Round-53 correction:**`) and
`SCORECARD.md:2858-2863` (`**Round-50 correction:**`), appended by the L1 before this seat ran. Draft 1 below is that
block verbatim: verified, nothing to change except the optional attribution note in §3.

## 3. Draft 1 — appended `**Round-53 correction:**` (fenced)

```markdown
**Round-53 correction:** the round-53 C1 and C2 After cells above cite the at-salvage receipts
`evidence/c1-at-salvage.txt` and `evidence/c2-at-salvage.txt` (R = `0df803033fba2386b10f5dcc6aa96bdef65cba15`);
the landed measurement of those rows is `.ufo/waves/round-53/evidence/c1-at-landed.txt` and
`.ufo/waves/round-53/evidence/c2-at-landed.txt` (R = `0b36d23e596276c70725873621fe15a28c87189f`, the revision the
round-53 report measures). The verdict lines are token-identical apart from `rev=` (`diff` of the `C1=`/`C2=` lines
with `rev=` removed prints nothing, round-54 L1), so no number in the cells changes; the rows are retained as filed
(append-only; round-53 closure D2, routed defect 1; lesson `corpus/lessons/round-54.md` M1).
```

This is byte-identical to the block already at `SCORECARD.md:2850-2856` (seven lines, no trailing space). If the L1
wants the identity check attributed to the seat that ran it, replace `round-54 L1` with
`w1/Mo54ScribeScorecard.md §1` — no other token changes, and the sentence still reads true (§1 is the diff above).

Placement check, by the check's own rule (`.ufo/waves/round-54/checks/receipt-stage.py`, `--repo`=lane):
`python3 .ufo/waves/round-54/checks/receipt-stage.py 39dcf4d7e410d362781a47e8365ca23b5c807598` at the entering tip
prints five FLAG lines (`round 50` ×2 lines 2668-2669, `round 53` ×3 lines 2796-2797) and
`RECEIPT_STAGE rev=39dcf4d7 cited_intermediate=5 flagged=5`, rc 1 — the committed receipt
`.ufo/waves/round-54/evidence/receipt-stage-before.txt` records the same five lines and `exit=1` (checked in full;
the file is currently untracked, `git status --porcelain` → `??`). A correction paragraph must start
`**Round-53 correction:**` (as drafted) and sit after the rows, which it does; with both blocks committed the same
check should print `cited_intermediate=5 flagged=0`, rc 0 — a gate for the L1 to run at the landed tip.

## 4. Draft 2 — the `## Round 54` section (fenced)

```markdown
## Round 54 — the remaining v7.2-pinned located quotes re-verified at Linux v7.3 (C1) and hardware memory-failure kills at v7.3 (C2)

L1 MoriR54 (attempt 1: freeze, data, one data correction before any seat, wave w1). Entering tip
`39dcf4d7e410d362781a47e8365ca23b5c807598` (round-53 verifier spot-check); freeze
`6830f3af992d906bfa1e17e3743e631ab834f67c` (`.ufo/waves/round-54/contract.md` with both counters, `controls/` and the
fourteen control receipts, both counter selftests, the C1 scope listing, census-start, the sweeps and the ten v7.3
copies, listed with sha256 in `evidence/freeze-sha256.txt`); data `1116c092`; data correction `78295c76` (C2 row 1
reworded, decision-table counting note under QUALITY 15). Scores entering: coverage 6, operability 7, depth 5,
freshness 5, calibration 5, adjacency 6; both claims work a lowest (tied 5) axis. No capability row is claimed this
round (both claims are corpus work) and no score change is claimed by the lane; the non-author closure rules.

| Claim | Axis (held) | Counting command | Before | After |
|---|---|---|---|---|
| C1 the 31 remaining v7.2-pinned located-quote claims of `oom-memcg-stat-r50.md` (22), `commit-runway-read-r53.md` (8) and `quota-observability-r48.md` (1) re-verified at Linux v7.3: one ledger row per claim hash in `kernel-v7.3-recheck-r54.md` with a v7.3 source row S515–S520 (or S508/S514), a located v7.3 quote, the line of the copy on which it begins and a `holds`/`changed` disposition, every v7.3 copy matching its frozen sha256, and, per row, at least two of the twelve RECHECK seats carrying that disposition as the final unfenced `RECHECK <h> <word>` line, none of them carrying the other word and each listed in the orchestrator's `w1-results.json` | freshness 5 | `python3 .ufo/waves/round-54/count-c1.py R` | `C1=unmet scope=31 rows=0 matched=0 status_ok=0 line_ok=0 quote_ok=0 source_rows=bad pins=bad provenance=bad held=0 absent=0 holds=0 changed=0 voted=0 dissent=0 … failed=ledger_absent,pins`, rc 1 — `evidence/control-c1-do-nothing.txt` (R = `39dcf4d7`) | `[L1 fills]` |
| C2 hardware memory-failure kills at Linux v7.3, the kill-event class an OOM-line census does not see: new entry `memory-failure-kills-r54.md` with 21 claim|source|quote rows over six copies (S521 `mm/memory-failure.c`, S522 `hwpoison.rst`, S523 `sysfs-devices-node`, S524 `events/memory-failure.h`, S507 `vm.rst`, S502 `proc.rst`) — the SIGBUS/SIGKILL lines, the recovery-action line and its four results, the per-node `memory_failure` counters, `HardwareCorrupted`, the early/late kill and recovery sysctls, v7.3's `panic_on_unrecoverable_memory_failure` and the `ras:memory_failure_event` tracepoint — each row entailed by at least two of the twelve ENTAILMENT seats listed in `w1-results.json`, none of them writing `overclaim` | depth 5 | `python3 .ufo/waves/round-54/count-c2.py R` | `C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=bad provenance=bad entailed=0 dissent=0 … failed=entry_absent,pins`, rc 1 — `evidence/control-c2-do-nothing.txt` (R = `39dcf4d7`) | `[L1 fills]` |

Target after (contract §C1/§C2), which replaces each `[L1 fills]`: C1
`C1=met scope=31 rows=31 matched=31 status_ok=31 line_ok=31 quote_ok=31 source_rows=ok pins=ok provenance=ok …
voted=31 dissent=0`; C2 `C2=met claims≥14 located=claims quote_missing=0 bad_rows=0 sources≥4 source_rows=ok pins=ok
provenance=ok entailed=claims dissent=0`. The settled read must be taken at a revision that carries the twelve seat
reports **and** the orchestrator's `w1-results.json`; before that, the counter returns `failed=votes` /
`failed=entailment` by construction (`w1/Mo54ExecC1Replay.md` F6; at the data commit `78295c76`:
`evidence/c1-at-data.txt` `rows=31 … line_ok=31 quote_ok=31 … voted=0 … failed=votes`, `evidence/c2-at-data.txt`
`claims=21 located=21 … entailed=0 … failed=entailment`, rc 1 each).

The C1 landing is `corpus/knowledge/kernel-v7.3-recheck-r54.md` (31 rows) with rows S515–S520 in `corpus/SOURCES.md`,
the used-by cells of S508/S514, the six v7.3 copies under `corpus/evidence/sources-r54/` and the release-pinned
rendered page `docs.kernel.org/7.3/admin-guide/cgroup-v2.html` — the flip the round-53 closure named for rendered
docs carried out; the C2 landing is `corpus/knowledge/memory-failure-kills-r54.md` (21 rows) with rows S521–S524 and
the used-by cells of S502/S507. Both land at the data commit `78295c76`; wave w1 is one v2 wave (`w1-spec.json`: 74
seats, of which 24 are voters; dispatch commit `2d0347a3`). Round-53 closure routed defects: D2 lands as the
`**Round-53 correction:**` paragraph appended after the round-53 section (it must stay after that section's rows
for `checks/receipt-stage.py` to read it); D3 relocated eight lane-root strays byte-exact
(`.ufo/waves/round-54/evidence/d3-relocation.txt`, eight `cmp=ok`) under `.ufo/waves/round-28|38/misroot-lane-root/`
and removed the empty `--repo/` directory; D1 is disclosed only.

Controls that skip the work stay unmet (receipts `evidence/control-*.txt`, readings in the contract's closing table):
C1 do-nothing `rows=0 … pins=bad … failed=ledger_absent,pins`; copies-only `rows=0 … pins=ok … failed=ledger_absent`
(the freeze state); no-line `rows=31 line_ok=0 quote_ok=31 voted=31`, `failed=line` — the round-53 all-held relabel
fails exactly the line arm; v72-copies `held=31 … pins=bad`, `failed=pins` (errno.h is byte-identical across the two
tags, so only the pins separate the bytes); no-votes `voted=0`, `failed=votes`; unsettled-voters (voter files, no
results file) `voted=0`, `failed=votes`; the witness (feasibility only, `controls/c1data.py` plus a fixture results
file) met, disclosed. C2 do-nothing `claims=0 … failed=entry_absent,pins`; copies-only `claims=0 … pins=ok`,
`failed=entry_absent`; quote-echo `claims=14 bad_rows=14 sources=0`,
`failed=bad_rows,entailment,provenance,source_rows,sources_floor`; unlocated `located=0 quote_missing=14`,
`failed=quote_missing,sources_floor`; no-votes `located=14 entailed=0`, `failed=entailment`; two-sources
`located=14 sources=2`, `failed=sources_floor`; the witness (synthetic claim text over real located quotes, fixture
results file) met, disclosed. Counter selftests `C1_SELFTEST pass=57 fail=0` and `C2_SELFTEST pass=54 fail=0`
(`evidence/selftest-c1.txt`, `evidence/selftest-c2.txt`).

Limits named before data (contract, verbatim in the two counter docstrings): all 31 v7.2 quotes still occur in the
v7.3 copies, so the status arm cannot separate a lazy all-held labeller — the line, pin and vote arms do; the line
arm proves where the words begin, not that the code around them means the same, and the disposition with its votes
carries the meaning; votes are seats of the lane, not outside verification, and the results binding proves the
orchestrator recorded a seat of that name, not who wrote the report bytes; D covers claim|source|quote tables only
(not prose, `oom-tracepoints-r47.md`'s catalogue or `system-pressure-r24.md`'s v7.2 anchors); the pins prove the
bytes are what the L1 fetched; on C2 a located quote proves the words exist in the copy, nothing here was observed
firing (no memory failure has occurred on this host), the v7.3 bytes describe the release while the host runs
7.2.11, and the entry is detection knowledge only — mori never injects poison, loads `hwpoison_inject` or writes a
memory-failure sysctl.

Limits wave w1 confirmed or added (the lesson `## Wave w1 — integrated findings` carries the full list; frozen bytes
were not changed in-round): the C1 status arm is degenerate on this dataset, `held=31 absent=0` confirmed by an
independent checker, so only the votes carry the freshness content (`w1/Mo54ExecC1Replay.md` F1); a line cell proves
an occurrence, not the cited one — `460b0cafc999` begins at v7.3 lines 1430 and 1636 (F2); the S-id is bound to a
copy by the counter's frozen URL map, not by the SOURCES row's own copy/digest cells (F3, no divergence on the
landed data); scope reads only the SOURCES row's source cell (F4, repeated over every cell, no divergence); the
round-50 entry's in-prose anchors still name v7.2 lines (F5, outside D by contract); the C1 selftest never executes
main()'s entering-tip revision branch, so a scope-read-at-scored-rev mutant survives (`w1/Mo54MutC1.md` MED); C2's
`normalise_text` collapses newlines, so a located quote can join two constructs across a blank line — 17 of 21 quotes
span more than one raw line and rows 1, 5, 11, 19 present adjacency joins (`w1/Mo54ExecC2Replay.md` finding 4); 19 of
the 21 C2 rows are shared 7.2/7.3 bytes and three of the six copies are byte-identical at both tags
(`w1/Mo54ExecMfV72.md` finding 4), so the located arm cannot separate this entry by freshness; the C2 selftest cannot
kill a `MIN_CLAIM_WORDS` or `MAX_WORDS` drift and several substring assertions match their own metric names
(`w1/Mo54MutC2.md`, four MED/LOW); control receipts are verdict-reproducible, not byte-reproducible, `controls.py:19`
cannot be replayed out of tree, and C2's `source_rows`/`provenance` cascade from a row defect so a `failed=` set must
be compared with the cascade expected (`w1/Mo54ExecControlsReplay.md`); on this host tracefs is `0700 root:root` so
`ras:memory_failure_event` is unreadable unprivileged, `dmesg` is closed by `dmesg_restrict=1` while `journalctl -k
-b` is open, and no EDAC/`rasdaemon` corrected-error counter exists (`w1/Mo54ExecHostRead.md`, three MED). Data-level
findings the wave routed to the L1 as allowed corrections: C2 rows 11 and 20 (`w1/Mo54ExecMfV72.md`), the entry's
boundary and sysctl list (`w1/Mo54SentC2Boundary.md`), the missing round-54 SOURCES search-log note and the S508
anchor gap (`w1/Mo54RevSourcesC1.md`).

Planned (round 55): the frozen-counter weaknesses wave w1 routed, by name — C1's degenerate status arm and its line
arm that cannot name a unique occurrence (`w1/Mo54ExecC1Replay.md` F1/F2), the S-id not bound to the row's own
copy/digest cells and the scope test reading one cell (F3/F4), the selftest gap on the entering-tip scope revision
(`w1/Mo54MutC1.md` MED); C2's whitespace-splicing located arm (`w1/Mo54ExecC2Replay.md` finding 4 — an arm that
separates a contiguous quotation from an adjacency join), the `MIN_CLAIM_WORDS`/`MAX_WORDS` selftest gaps and the
substring-assertion style (`w1/Mo54MutC2.md`), and the `failed=` cascade coupling (`w1/Mo54ExecControlsReplay.md`);
the control runner's `LANE` derivation and a receipt format that records a placeholder instead of the fixture commit
(same report); the v7.3 trigger for what D does not cover, carried from round 53 — `oom-tracepoints-r47.md`,
`oom-victim-selection-r27.md`, `disk-write-rate-r33.md`, `watchdog-identity-r31.md`, S511–S513, and the round-50
entry's v7.2 in-prose anchors (`Mo54ExecC1Replay.md` F5); the round-53 items this round did not take — the locator
sweep beyond the Axes rows (`QUALITY.md` and `README.md` hold 78 pointers it does not read), receipts that are pure
text, arm A's verdict pinned only to `admitted`, the in-lane writers' successor freeze including round-40
`conform.py`, FR8's calibrated `COMMIT_LOW` threshold (measured refusal behaviour, not a counter change), and the 30
round-52 flags dropped without an owner; and the entry-side follow-ups the host read opens — an unprivileged
detection path for `ras:memory_failure_event`, journald as the only log channel on this host, the taint bits as a
text-free signal, and the `vm.enable_soft_offline` / `vm.panic_on_unrecoverable_memory_failure` knobs the re-read
recipe currently skips.
```

Notes on the draft that the L1 needs before integrating:

- `[L1 fills]` appears twice (the two After cells). Nothing in this seat can fill them: `w1-results.json` does not
  exist yet (`ls .ufo/waves/round-54/w1-results.json` → `No such file or directory`) and no at-landed receipt exists
  (`ls .ufo/waves/round-54/evidence/ | grep landed` → rc 1), so any After text written now would be the at-data
  reading restated, which the round-53 lesson M1 correction exists to prevent.
- The C1 claim cell's "S515–S520 (or S508/S514)" is the contract's own split: six new v7.3 copies plus the two
  v7.2-pinned rows whose used-by gained the ledger. If the L1 wants the exact per-row distribution it is
  `evidence/c1-claims.txt` and the ledger's `source` column.
- The section claims no capability row. That is a statement about this round's claims (both are corpus work; no new
  tool is in `## C1`/`## C2`), not a judgement about the round.
- The census line is deliberately omitted (the round-53 section carries none); the round gate is `census-end` exit 0
  in the L1 report. For reference the start receipt is `evidence/census-start.txt`: 25 lines, 23 `W04` findings,
  final line `exit=0`.

## 5. Inputs read (paths, revisions)

| input | what was taken |
|---|---|
| `.ufo/waves/round-54/contract.md` (`6830f3af`; sha256 `1e06f99f9235…`) | claims, P-C1/P-C2, targets, controls table, named limits, separability, round shape, routed defects D1–D3 |
| `.ufo/waves/round-54/count-c1.py`, `count-c2.py` (frozen sha256 `e97a1198…`, `d6b42f89…`) | predicate docstrings only; not executed |
| `.ufo/waves/round-54/evidence/control-*.txt` (14 files) | before readings quoted in the claim table and every control token in the controls paragraph |
| `.ufo/waves/round-54/evidence/selftest-c1.txt`, `selftest-c2.txt` | `C1_SELFTEST pass=57 fail=0`, `C2_SELFTEST pass=54 fail=0` |
| `.ufo/waves/round-54/evidence/c1-at-data.txt`, `c2-at-data.txt` (`78295c76`) | the at-data readings named as "not the After cell" |
| `.ufo/waves/round-53/evidence/{c1,c2}-at-{landed,salvage,data}.txt` | §1 diff and token counts |
| `SCORECARD.md` at `2d0347a3` (`git show`) and working tree | round-53 house shape, the two cells' citations, the two uncommitted correction blocks |
| `corpus/lessons/round-53-verifier-spotcheck.md:6-7,18,44,49,80,100,103,116` | `0b36d23e` as the revision the round-53 report measures; D1/D2 wording |
| `.ufo/waves/round-54/w1/Mo54ExecC1Replay.md`, `Mo54ExecC2Replay.md`, `Mo54ExecControlsReplay.md`, `Mo54ExecHostRead.md`, `Mo54SentC2Boundary.md`, `Mo54RevSourcesC1.md`, `Mo54ExecMfV72.md`, `Mo54MutC1.md`, `Mo54MutC2.md` | the wave-confirmed limits and the routed data corrections quoted in the limits paragraph |
| `.ufo/waves/round-54/w1-spec.json` | 74 items, 24 voter names |
| `.ufo/waves/round-54/evidence/census-start.txt`, `d3-relocation.txt`, `receipt-stage-before.txt`, `freeze-sha256.txt` | census count, D3 `cmp=ok` lines, the five FLAG lines, freeze hashes |

## 6. Touched surfaces, out of scope, not done

- Not run: `count-c1.py`, `count-c2.py`, `controls/controls.py` at any revision (their replay belongs to the executor
  seats; running them here would be decoration, and a dispatched seat is not an independent judge).
- Not edited: `SCORECARD.md`, `SKILL.md`, `SHONEN.md`, `LOG.md`, `PROVINCE.md`, `corpus/`, `tools/`, `considerthese/`,
  any `.ufo/waves/round-54/` file other than this report. The two correction blocks in the working tree are the L1's
  and were left untouched.
- Not decided: any score move, the axes-table `Last change` cells, the wave's lesson, and the settlement
  (`w1-results.json`). The `Planned (round 55)` list is a carrying list, not a scope commitment.
- Not verified: whether the twelve RECHECK and twelve ENTAILMENT seats will land the dispositions the ledger rows
  carry — the vote arm is exactly what the L1's at-landed read measures.

## 7. Scratch

`/fast/scratch/hyaku/mori-r54/Mo54ScribeScorecard/` (`tmp/`) created for the one throwaway file the diff pipeline
needed; the verification commands above are pure `diff`/`grep`/`wc` over lane files and wrote nothing into the lane.
The directory is removed before this report is filed (`rm -rf`); no clone, no work tree, no fixture repo was made.

## Findings

- **MED — `corpus/lessons/round-54.md` does not exist yet, and the block this seat drafts and the L1 already has in
  the working tree cite it** (`SCORECARD.md:2850-2856`, "lesson `corpus/lessons/round-54.md` M1"). If the lesson is
  not written at the landed tip, the correction points at a missing file. Checked: `ls corpus/lessons/ | grep -E
  'round-5[34]'` lists only `round-53-verifier-spotcheck.md` and `round-53.md`.
- **MED — the two SCORECARD additions are uncommitted at HEAD `2d0347a3`** (`git diff --stat SCORECARD.md` → 15
  insertions; `git status --porcelain SCORECARD.md` → ` M`). They are the round-53 and round-50 corrections; until
  the L1 commits them, `checks/receipt-stage.py` still flags round 53 (verified at `39dcf4d7`: three round-53 FLAG
  lines, rc 1). A checkout or rebase in the lane would lose the only fix for the routed defect.
- **MED — the C1 After cell cannot be filled from anything that exists now**: no `w1-results.json`, no
  `.ufo/waves/round-54/evidence/c1-at-landed.txt`/`c2-at-landed.txt` (`grep landed` → rc 1). The contract's target
  line names `voted=31`, which requires all twelve voter reports committed plus the settlement record; the at-data
  receipt reads `voted=0 … failed=votes` by construction (`w1/Mo54ExecC1Replay.md` F6). Draft 2 therefore leaves
  `[L1 fills]` and names the target beside it rather than pre-writing a measurement.
- **LOW — `receipt-stage-before.txt` is untracked** (`git status --porcelain` → `??`) and therefore not covered by
  `freeze-sha256.txt` (0 hits for `receipt-stage`). It does contain the correct five FLAG lines and `exit=1` — this
  seat first read only its first three lines and nearly reported a stale receipt; the full file is right. LOW
  because the bytes are correct, but an unfrozen and untracked receipt is exactly the "pure text receipt" limit
  round 53 routed forward.
- **LOW — the round-53 correction's wording "round-54 L1" attributes the diff to the L1**, while the run was made by
  this seat (`§1`). True either way (the L1 committed the block and can re-run the one-line diff in seconds), but the
  attribution is not what happened; §3 gives the one-token replacement if the L1 prefers the seat's name.
- **LOW — the round-54 section's limits paragraph cites reports that may still change** before `w1` settles
  (`w1/Mo54MutC1.md`, `Mo54MutC2.md`, `Mo54ExecHostRead.md`, `Mo54SentC2Boundary.md`, `Mo54RevSourcesC1.md`,
  `Mo54ExecMfV72.md` were read while their seats were still running). The tokens quoted were stable in the files at
  read time; the L1 should re-check the pointers against the settled reports and the lesson's
  `## Wave w1 — integrated findings` before committing the section.

Conflicts for the canonical judge, verbatim:

- **Data versus source, C2 row 20 (`8248e6d24be8`)** — `w1/Mo54ExecMfV72.md` finding 1: the claim says the traced
  line "repeats the page type and outcome strings of the logged recovery line", while the copies read
  `MF_MSG_ALREADY_POISONED` as `"already poisoned"` in `memory-failure-trace.h.v7.3:49` and `"already poisoned
  page"` in `memory-failure.c.v7.3:897`. The entry as written is broader than its sources; the seat's MED stands
  until the row is reworded (a new hash) — the L1's call, data-level, and outside this seat's write scope.
- **Severity difference, not a fact conflict** — the C1 and C2 mutation seats rate the analogous selftest
  substring-assertion weakness LOW (`w1/Mo54MutC1.md`, M07/M10 still killed) and MED (`w1/Mo54MutC2.md`,
  `"bad_rows" in line` matches `bad_rows=0` in eight checks). Both routed; no counter, predicate or kill rule
  differs between the reports, and neither proposes an in-round fix (frozen bytes).

Artifact paths (this seat): `.ufo/waves/round-54/w1/Mo54ScribeScorecard.md` (this report; the only write).
Drafts are the two fenced blocks in §3 and §4. No `Report:` trailer other than this path was written.
