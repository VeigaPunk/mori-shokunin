# mori round 49 — frozen contract (L1 MoriR49, attempt 1)

Entering lane tip: `b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86` (round 48 closure,
`corpus/lessons/round-48-verifier-spotcheck.md`). This file, both counters, the committed source
copies and the controls under `controls/` and `evidence/` are committed in one freeze commit before
any wave seat runs. A predicate, counter, floor or kill rule changed after any seat has scored is not
the claim's rule. Round-48 spot-check disposition: `.ufo/waves/round-49/disposition.md` (written
after the freeze; it changes no frozen byte).

Scores entering (SCORECARD.md Axes table): coverage 6, operability 7, depth 5, freshness 5,
calibration 5, adjacency 6. Lowest non-retired axes: depth, freshness, calibration (tied at 5). Both
claims work a lowest axis; no stagnation waiver is used. Frozen instrument bytes (sha256) are printed
in `evidence/freeze-sha256.txt`; if working-tree bytes ever differ, the claim is measured with
`git show <freeze>:<path>`.

## C1 — calibration: the pin reconciler reads what a reader sees, and the counter hides which edit it is scoring

Surface: `tools/mori-pin-check.py` (v3 at entering) and the junk-variant counter that scores it.
Routed by round 48: `w2/R48CritV3Junk1.md` (seven new row shapes that print `PIN_CHECK=met`),
`w2/R48ExecD7.md` (D7 misattribution, rule R11), `w1/CritC1Counter.md` F1 (a tool keyed on the
harness's variant filename passed C1), `corpus/lessons/round-48-verifier-spotcheck.md` §5 item 3.
Mined proposal: `considerthese/2026-10-25.md` suggestion 3 (see the frontier section).

**P-C1.** At revision R, `python3 .ufo/waves/round-49/count-c1.py --tool <tools/mori-pin-check.py
at R> --rev R` prints `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26` and exits 0:
the tool bytes under test score `PIN_CHECK=unmet` (exit 1) on each of the eighteen frozen junk edits
(round 48's J1-J8 and the new N1-N10) and `PIN_CHECK=met` (exit 0) on each of the seven frozen honest
edits (H1-H7), on R's SKILL.md read through an opaque-named copy, and on R's unedited SKILL.md, every
run with `--min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53`. Every variant
reaches the tool under an opaque name (the SKILL.md copy and scratch directory are named by a sha256
prefix of their bytes; run order follows that hash; N10 and H5 are built in a throwaway fixture repository
whose path and commit message carry no variant name). A tool crash, setup exit or timeout is `errors`, never `unmet`.

Variants (functions in `count-c1.py`, listed in its docstring): J1-J8 and H1-H4 are the round-48 edits
imported unchanged; N1 one gate row inside an HTML comment, N2 NBSP in the self-test header plus a
zero-width space in the pin token, N3 a tab-indented pipe row in a fence, N4 a four-space-indented pipe
row outside a table, N5 a second row for one command with a contradicting exit contract, N6 a
pin-less command row plus prose `fail=0` and a continuation line recording `fail=3`, N7 the junk row as
HTML table markup, N8 the reconciler's own row re-pointed (entry cell names the reconciler, self-test
cell runs the unlanded check), N9 a new row naming the gate registry while pinning the reconciler's
tally, N10 (fixture) an instrument gains one self-test arm (two arms to three) and the registry pin stays
stale at the old tally; H5 (fixture) the same instrument edit with the registry pin moved to the new tally; H6 an HTML comment
and an HTML table that carry no pin token; H7 an indented pipe row and a tab-indented fenced row that
carry no pin token.

- Before (entering tool, `controls/tool-v3-entering.py`, sha256 `85a89a3b…` = `tools/mori-pin-check.py`
  at `b3e3453d`): receipt `evidence/control-c1-tool-v3-entering.txt`.
- Target after: `C1=met … variants=26` at the landed tip, same command, tool at R.
- Controls (each scored with this counter before data, committed; none may reach `met`):
  do-nothing = the entering v3 tool; `controls/stub-always-met.py`; `controls/stub-always-unmet.py`;
  `controls/stub-filename-sniffer.py` (keys on round-48 variant and scratch names — it scores `met`
  under the round-48 counter, `evidence/control-c1-sniffer-under-r48-counter.txt`, and must stay unmet
  here); `controls/tool-r48-surface-fixes.py` (round 48's five surface rules, no R11) and
  `controls/tool-r48-r11-only.py` (R11 only) — partial candidates that show each half of the target is
  separately required. `controls/tool-r48-merged-witness.py` (the two round-48 candidates merged by the
  L1, not by a wave seat) is a feasibility witness only; its receipt is recorded, it is not the claim's
  tool, and the claim does not rest on it.
- Kill rule: if the landed tip prints `C1=unmet`, C1 is not verified; no re-scoring under a changed
  counter. The counter's own selftest pin and the freeze sha256 are receipts, not part of the predicate.
- Named limits (before data): the variants are the classes found by rounds 47-48 seats, not the class of
  all junk (round 48's K2-K8 — env-prefix substitution, pin deletion, pins outside the self-test cell,
  namespace join, floor slack, line-count rebinding, rc-free pins — are NOT in this predicate and stay
  routed); a tool can pass by being narrower than the junk, so H1-H7 and the real registry are part of the
  predicate; the counter does not run the tool's own `--selftest`; wave 2 attacks with fresh classes and
  reports survivors as limits, never as a re-score.

## C2 — depth: journal retention reach (FR1 evidence reach), a located quote per claim

Surface: `corpus/knowledge/` — how far back the journal evidence that mori reads can reach (the retention
rule, the persistent-versus-volatile split, the vacuum order, this host's effective ceilings). Assimilation
theme from `/home/vgpnk/Projects/shokuknow/merge/mori/`: staged entries
`knowledge/corpus/knowledge/journal-effective-retention-r45.md`, `journal-reach-at-ceiling-r46.md`,
`runtime-journal-reach-is-the-boot-r49.md` (and the rows S516, S532, S560), rewritten as one entry
`corpus/knowledge/journal-reach-r49.md`. The staged own-work rows (S524, S537, S544) cite receipts outside
this lane and are not adopted; this round's host receipt replaces them. Coverage sweep before data
(`evidence/sweep-journal-rows.txt`): `SystemMaxUse`, `MaxRetentionSec` and `RuntimeMaxUse` occur in
`corpus/SOURCES.md` and `corpus/knowledge/` 0 times at `b3e3453d`, and no row names the `journald.conf` page;
the lane holds the `--disk-usage` sentence (S470, `journal-disk-usage-total-r51.md`) and the alarm-routing
"vacuumed → no retained record" class (`journal-alarm-routing-r14.md:166,176`) without the rule that sets the
reach. The lane's own earlier refusal of this theme is row **S351** (`journalctl(1)`, rejected, flip: "the
public --vacuum-size= sentence plus a committed read-only disk-usage receipt, and no MESSAGE grep"): this
claim is that flip — the public sentence from the committed copy plus a committed read-only receipt, no
MESSAGE grep — recorded as a new row whose `teaches` opens `supersedes S351 —`; S351 itself stays a rejected row.

**P-C2.** At revision R, `corpus/knowledge/journal-reach-r49.md` opens with `source:` lines,
`verified-at:` and `recheck:`, and carries a table whose header cells are `claim`, `source`, `quote` with
at least 8 rows; each row's source cell is one S-id naming a `corpus/SOURCES.md` row at R that is `mined`,
opened 2026-10-25, names its source among the four frozen sources in `count-c2.py` (three freedesktop.org
manual pages and the host receipt) and lists the entry in `used-by`; each row's quote cell is one
backticked span of 6 to 25 words, unique in the table, that occurs (script, style and comment blocks
dropped, tags stripped, entities decoded, whitespace collapsed) in the committed copy of that row's source
under `corpus/evidence/sources-r49/`, and the table draws on at least 3 distinct sources; every committed
copy matches its frozen sha256.

Counting command: `python3 .ufo/waves/round-49/count-c2.py R` → `C2=met|unmet …`.

- Before (entering `b3e3453d`): `C2=unmet … failed=entry_absent,pins` (`evidence/control-c2-donothing.txt`;
  the pins arm reads `bad` because the copies are not at the entering revision).
- Target after: `C2=met claims=N located=N quote_missing=0 bad_rows=0 sources=S source_rows=ok pins=ok
  provenance=ok` with N ≥ 8 and S ≥ 3 at the landed tip.
- Controls: do-nothing; the counter's selftest arms carry the entry-level controls with their reason
  isolated (staged entry byte-exact, altered quote, wrong-copy quote, short and long quotes, duplicate
  quote, unmined row, row opened another day, missing `used-by`, digest mismatch, script/style/comment
  text in a copy — the round-48 survivor — `C2_SELFTEST pass=26 fail=0` at freeze).
- Kill rule: `C2=unmet` at the landed tip → C2 not verified.
- Named limits: a located quote proves the quoted words occur in the committed copy, not that the claim
  cell follows from them, not that the page is unchanged today, and — for the host receipt — not that the
  host still reads this way (the receipt is the 2026-10-25 capture; the journal total moved from 269M
  (S470 entry, 2026-10-24) to 56M within one day). Wave 2 reviewers re-open every row against the page text
  around its quote and report the result as a limit.

## Separability

C1 touches only `tools/mori-pin-check.py`, its SKILL.md registry rows and `count-c1.py`'s variants; C2
touches only the journal-reach entry, its SOURCES rows and `corpus/evidence/sources-r49/`. Either counter
can be run with the other claim's changes reverted. No claim edits the other's counter.

## Frontier step, assimilation, mistake, considerthese (not claims)

- Census: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` at round start
  (`evidence/census-start.txt`, exit 0, 21 lines: 20 W04 duplicate-url warnings and one `ok`) and round end.
- Assimilation: theme journal retention reach (FR1). Collision check, 0-3-space guard proof and the
  quarantine slice are in `assimilation/` (14 collisions S471-S484 for the whole package; the three staged
  rows adopted by document, S516/S532/S560, collide with none). Admit/reject per staged entry in the
  lesson `## Gate`; renumber by document. The three quarantine-slice rows (S244, S262, S268) keep their
  round-48 verdicts; none is cited by an admitted entry and none is appended.
- considerthese: `considerthese/2026-10-25.md` suggestion 3 (flagged-versus-fixed critic count) lands as a
  lesson measurement over round 48 and a QUALITY criterion with its counting command; suggestions 1, 2, 4
  were mined by rounds 47-48 (`w1/ScoutConsiderthese.md` of round 48).
- Mistake: the round-48 counter let a tool pass by reading the harness's file names (`w1/CritC1Counter.md`
  F1, round-48 lesson Wave 1) and the round-48 closure routed 114 untracked `.scratch` directories; the fix
  for the first is this counter's opaque handles, shown able to fail by the sniffer pair of receipts.
- Round-48 routed defects carried: unique seat names in wave 1; `.scratch/` residue (cleaned at round end,
  `.gitignore` entry); report author date at or after the lane tip it cites.

## Round shape

Two v1 waves (policy `scripts/hyaku/ufo-wave-policy.json`, band 32-64): w1 build + first falsifiers, w2
falsify after landing. Total within 64-100; the L1 holds the planner seat.

## Freeze receipts (recorded at the freeze commit; no predicate above changed after them)

Scored with `count-c1.py` at the entering tip `b3e3453d` (jobs 4; receipts `evidence/control-c1-*.txt`):

| control | result line | reading |
|---|---|---|
| entering v3 tool (do-nothing) | `C1=unmet junk_met=9 honest_unmet=0 real=met errors=0 variants=26` | N1-N9 print `met`; the do-nothing control cannot reach the target |
| `stub-always-met` | `junk_met=18` | rejects nothing |
| `stub-always-unmet` | `honest_unmet=8 real=unmet` | rejects everything |
| `stub-filename-sniffer` | `junk_met=18` | the round-48 leak is closed: it scores `met` under the round-48 counter (`control-c1-sniffer-under-r48-counter.txt`) |
| `tool-r48-surface-fixes` | `junk_met=1` (N9) | the five surface rules alone leave D7 open |
| `tool-r48-r11-only` | `junk_met=7` (N1-N7) | R11 alone leaves the surface shapes open |
| `tool-r48-merged-witness` | `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26` | **the predicate is reachable by integrating the two round-48 patch sets** (F1-F5 from `w2/R48CritV3Junk1.md` and R11 from `w2/R48ExecD7.md`, merged mechanically by the L1 with `patch`; selftest 65/65) |

Disclosure the closure should weigh: the witness shows the target tool bytes are largely pre-existing round-48
seat output, so the claim's new work is (a) landing and testing that tool in `tools/` with selftest arms and the
K-class rules wave 1 proves, (b) the successor counter itself (opaque handles, a fixture-built honest
pin-updating edit, three new honest controls, the real registry read twice), and (c) the false-red audit of the
new rules against earlier SKILL.md revisions. A first draft of H5 built the pin-moving edit in a clone of the lane
and scored `unmet` under every tool including the witness (the clone's round-40 `conform.py --selftest` pin fails
there for a reason unrelated to the edit); the receipts above are from the final counter, where H5 and N10 are built in a small fixture repository.
`C1_SELFTEST pass=44 fail=0`, `C2_SELFTEST pass=26 fail=0` at freeze.
