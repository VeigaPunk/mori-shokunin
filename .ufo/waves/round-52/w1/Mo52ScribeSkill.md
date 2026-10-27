# Mo52ScribeSkill — round 52 w1: draft `SKILL.md` `## Round52`

Seat: Mo52ScribeSkill (scribe, leaf — no subagents dispatched). Slice: a fenced draft of `SKILL.md` `## Round52`
carrying three items — (1) a decision row for reading `CommitLimit`/`Committed_AS` by mode, (2) the refusal log line
as a detection signal, rate-limited and not a count, (3) the living-pin rule for `corpus/QUALITY.md` and
`corpus/README.md` (supersede, never rewrite; counter arm C). No sysctl advice. I wrote nothing but this file.

Scratch: `/fast/scratch/hyaku/mori-r52/Mo52ScribeSkill/` (`tmp/` created, removed before I finished; nothing in it
was cited). Lane repo and fleet repo untouched: no git/jj mutation, no counter run, no file under
`.ufo/waves/round-52/` written except this report. Disk guard at start: `/fast/scratch/hyaku` 25 % used, 602.5 G
free.

## What I read (read-only; no replay)

| command | result |
|---|---|
| `read …/.ufo/waves/round-52/contract.md` | P-C1 four-arm predicate, P-C2 entailment arm, floors, kill rules, control table |
| `read …/corpus/knowledge/overcommit-commit-limit-r52.md` | 28 claim rows + 4-row `Reading rules (mori)` table + Boundaries |
| `read …/SKILL.md:1000-1141` | `## Round51` house shape: heading with title, lede paragraphs per counter, counters table, `### Decision row — …` table, `### Pin mismatch classes` subsection |
| `git -C …/mori-shokunin diff --stat 4f266ef2… 8524904a…` | 33 files, 7933 insertions; `SKILL.md` not touched by the data commit (grep `^## Round5[12]` finds only line 1069 `## Round51`) |
| `git -C … diff 4f266ef2… 8524904a… -- SCORECARD.md corpus/QUALITY.md corpus/README.md` | QUALITY +21 lines (criteria 141–142 at lines 1356, 1366), README +13 (note at 722–730), SCORECARD Axes tail cells +3/−3 |
| `git show 8524904a…:corpus/QUALITY.md \| awk 'NR>=1350'`; `…:corpus/README.md \| awk 'NR>=715'` | the appended supersession text, quoted below |
| `cat .ufo/waves/round-52/evidence/c1-at-data.txt` | `C1=met items=42 axes=6 pins=2 boxes=4 living=7 superseded=4 locators=27 mismatches=0 errors=0 hidden=0 lane_writes=0 manifest=6209bdb8e400`, exit=0 |
| `cat …/evidence/c2-at-data.txt` | `C2=unmet claims=28 located=28 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 failed=entailment`, exit=1 |
| `tail -3 …/evidence/selftest-c1.txt` / `selftest-c2.txt` | `C1_SELFTEST pass=42 fail=0` exit=0 · `C2_SELFTEST pass=45 fail=0` exit=0 |
| `grep -E '^item (living\|pin\|locator)' …/evidence/control-c1-do-nothing.txt` | three living mismatches at the entering tip (quoted in § Findings) |
| `grep -E '^(item living\|C1=)' …/evidence/control-c1-{rewrite-in-place,delete-stale-pins}.txt` | `pin_removed_or_rewritten` ×3 on both controls, `C1=unmet … mismatches=3` |
| `awk` claim-row numbering over `overcommit-commit-limit-r52.md`; `sed` on `corpus/QUALITY.md` 85–100, 880–902, `corpus/README.md` 722–732 | claim rows 1, 2, 8, 9, 14, 17, 20, 21, 22, 26; QUALITY 15 (journal classes by MESSAGE_ID); QUALITY 111 supersedes 109's check; README note bullets one line each |
| `grep -n 'vm_acct_memory(pages)' corpus/evidence/sources-r52/util.c.v7.2`; `sed -n '996,1001p'`; `awk` 940–966 | charge at `:964`, `error:` at `:996`, `pr_warn_ratelimited("%s: pid: %d, comm: %s, bytes: %lu not enough memory for the allocation\n", __func__, …)` at `:998-999`, `vm_unacct_memory(pages)` at `:1000`, `return -ENOMEM` at `:1002`, enclosing function `int __vm_enough_memory(...)` at `:959`, so the printed prefix is `__vm_enough_memory` |
| `scripts/hyaku/disk-guard.sh status` | rc 0 (used above) |

UNVERIFIED: I ran neither `count-c1.py` nor `count-c2.py`; every counter figure below is copied from the receipt
named beside it, as read.

## Draft — `## Round52` (fenced; append after `## Round51`, do not edit it)

```markdown
## Round52 — the self-assessment counter, the overcommit ledger and the living-pin rule

Round 51 said what `MemAvailable` is; round 52 takes the two other runway lines of `/proc/meminfo`, `CommitLimit`
and `Committed_AS`, and counts the lane's own pointers. Both counters are frozen with the round: a counter weakness
found after scoring is a named limit, never a repair.

`.ufo/waves/round-52/count-c1.py` (calibration) scores the lane's self-assessment at R over four arms — (A) the six
`SCORECARD.md` `## Axes` rows against the fleet MANIFEST's newest admitted verdict and the newest closure's per-axis
score, (B) every `SHONEN.md` tally pin re-run at R with a receipt under `.ufo/waves/round-52/evidence/selftests/`,
(C) every single-line command-tally pin in `corpus/QUALITY.md` and `corpus/README.md` good or superseded, (D) every
backticked `path:N` locator in the six Axes rows and the SHONEN boxes landing on the quoted words or the read
`proposed A → B` pair — with floors of 2 pins and 4 boxes. Entering
`4f266ef2` it read `C1=unmet … mismatches=8` (`.ufo/waves/round-52/evidence/control-c1-do-nothing.txt`); at the
data commit `8524904a` it read `C1=met items=42 axes=6 pins=2 boxes=4 living=7 superseded=4 locators=27
mismatches=0 errors=0 hidden=0 lane_writes=0` (`.ufo/waves/round-52/evidence/c1-at-data.txt`). Its selftest reads
`C1_SELFTEST pass=42 fail=0` (`.ufo/waves/round-52/evidence/selftest-c1.txt`).

`.ufo/waves/round-52/count-c2.py` (depth) scores `corpus/knowledge/overcommit-commit-limit-r52.md` against the five
frozen copies under `corpus/evidence/sources-r52/`: at least 12 claim rows, each row naming one mined `SOURCES.md`
row (S497–S501) that lists the entry in `used-by` and quoting one 6–25-word span located in that row's committed
copy, all five sources drawn on and every copy sha256-pinned, and — the round-51
closure's hardened arm — for every row an `entailed` vote from two distinct ENTAILMENT seats of the frozen twelve
that did not write that row's text. At the data commit it read `C2=unmet claims=28 located=28 quote_missing=0
bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 failed=entailment`
(`.ufo/waves/round-52/evidence/c2-at-data.txt`): every quote is located and no seat has judged them yet. Its
selftest reads `C2_SELFTEST pass=45 fail=0` (`.ufo/waves/round-52/evidence/selftest-c2.txt`).

### Decision row — the overcommit ledger (round 52)

| situation | do | do not | source |
|---|---|---|---|
| a runway read takes `CommitLimit` and `Committed_AS` off `/proc/meminfo` | read `/proc/sys/vm/overcommit_memory` beside the two lines and split by mode: at 0 or 1 the limit is printed and not enforced, so `Committed_AS` above `CommitLimit` is normal; only at 2 is the committed total capped and new work refused | read the gap as memory pressure or an imminent kill under any mode; read either line without the mode beside it | `corpus/knowledge/overcommit-commit-limit-r52.md` (S497–S499, rows 1, 2, 8, 9) |
| the host runs mode 2 and a seat asks for runway | read the limit as RAM less hugetlb pages at `vm.overcommit_ratio` percent plus every swap page, lowered further for a caller without `CAP_SYS_ADMIN` and by the requesting process's share of the user reserve, and report the first `fork`, `brk` or private-mapping ENOMEM as the runway signal beside `MemAvailable`, not instead of it | read `CommitLimit` as free memory, or expect a mode-2 refusal to show in `MemAvailable` first; choose, propose or write an overcommit mode or ratio — the mode is host configuration the operator owns, and mori reads no `vm.*` sysctl | `corpus/knowledge/overcommit-commit-limit-r52.md` (rows 10, 12, 14, 15, 18, 19) |
| `vm.overcommit_ratio` reads 0 | read `vm.overcommit_kbytes` beside it: setting one knob zeroes the other, so a zero ratio can mean the kbytes knob is in force | read 0 as a swap-only limit, or as the compiled-in default of 50 | `corpus/knowledge/overcommit-commit-limit-r52.md` (rows 11, 15, 21) |
| a refused request is followed by a `Committed_AS` read | read the refusal as leaving nothing behind: the request is charged before the mode is examined and the error path uncharges it before returning ENOMEM, so the ledger nets zero for it | read a steady ledger as proof the refusal went uncounted, or a later rise as the refused request's pages arriving | `corpus/knowledge/overcommit-commit-limit-r52.md` (rows 17, 20); `corpus/evidence/sources-r52/util.c.v7.2:964,996-1002` |
| `Committed_AS` sits at or just under `CommitLimit` under mode 2 | read the boundary as approximate — the charge counter is a per-CPU sum and the mode-2 test takes a cheaper approximate read of it — and read the ledger as having holes (ptrace pages unaccounted, hugetlb file mappings with `MAP_NORESERVE` uncharged) | read the last unrefused page as an exact refusal point, or the ledger as a complete account of every commitment | `corpus/knowledge/overcommit-commit-limit-r52.md` (rows 6, 18, 22, 26; Boundaries) |

### Decision row — the refusal line (round 52)

| situation | do | do not | source |
|---|---|---|---|
| a kernel line `__vm_enough_memory: pid: N, comm: X, bytes: B not enough memory for the allocation` is seen | read it as a commit refusal and report the pid, the command and the byte count it names, with the window it was read over, and check `vm.overcommit_memory` before attributing it | read it as an OOM kill (the kill report is a different block, `corpus/knowledge/oom-memcg-stat-r50.md`); read its absence in a window as a healthy ledger or as "no refusals happened" | `corpus/knowledge/overcommit-commit-limit-r52.md` (row 20; Reading rules rows 2–3) |
| refusals are tallied for a report or a gate | report presence, rate-limited: the warning is emitted by `pr_warn_ratelimited`, so a window shows that refusals occurred, not how many | count refusals from these lines, or count any journal class from message text (a journal class is counted by MESSAGE_ID or another trusted structured field, `corpus/QUALITY.md` 15); sum the `bytes` values as refused memory | `corpus/knowledge/overcommit-commit-limit-r52.md` (row 20; Reading rules row 3); `corpus/QUALITY.md` 15 |

### Living pins (round 52) — supersede, never rewrite

A command in `corpus/QUALITY.md` or `corpus/README.md` that prints a tally is a living pin: a reader runs it today.
Both files are records, so a stale pin is answered by a later line and never by an edit — every pin present at the
entering tip is still present byte for byte. `count-c1.py` arm (C) enumerates every single-line command-tally pin in
both files and classes it.

| state | what the counter read | what the lane does |
|---|---|---|
| good | the span parses (shlex) as a `python3` or `bash` command naming a repo-relative path, the path is a regular file at R, the command exits 0 and its last tally line carries the pinned numbers and prefix (item line ends `…_rc=0`) | nothing: the pin is current |
| superseded | in `QUALITY.md` a later numbered criterion says `supersedes N's check`; in either file a later line carries `supersedes` with the stale span and its tally verbatim, which makes the quoted span a quotation and not a pin | leave the stale row byte for byte and put the replacement pin on the supersession line itself — one bullet per line, because the counter reads a quoted stale pin as a quotation only when its replacement stands on the same line |
| mismatch | `pin_removed_or_rewritten` (a pin present at the entering tip is gone or edited), `unrunnable` (the span names no command), or a different tally: the row and the instrument disagree at R | re-add the original line and supersede it instead of editing it; settle a different tally in the same commit that changes the instrument, and say in the receipt which of the two moved |

At the data commit `8524904a` arm (C) read `living=7 superseded=4`: the two pins at `pass=12` (`QUALITY.md:909`,
`README.md:608`) and the bare `--selftest` span (`README.md:607`, which names no command) are superseded by QUALITY
141 and by the README round-52 note, and the three replacement pins ran `rc=0`. Entering `4f266ef2` the same arm
read three mismatches (`.ufo/waves/round-52/evidence/control-c1-do-nothing.txt`); editing those pins in place
instead reads `pin_removed_or_rewritten` ×3 (`.ufo/waves/round-52/evidence/control-c1-rewrite-in-place.txt`).
Named limit, frozen with the counter: a pin split across lines, or one carrying a placeholder, is not enumerated as
a living pin.
```

## Evidence behind each drafted item

**(1) Ledger decision row.** The entry's `Reading rules (mori)` rows supply the mode split: row 1 (`Committed_AS` >
`CommitLimit` under mode 0 or 1 is normal, the limit is printed not enforced), row 2 (mode 2: new private writable
mappings, `brk` and `fork` can fail with ENOMEM before `MemAvailable` is low), row 4 (`vm.overcommit_ratio` reads 0
may mean `vm.overcommit_kbytes` in force). Claim rows substantiate the mechanism: row 2 (cap = swap + configurable
share, default 50 %), row 8 (mode 0 compares against total RAM + swap), row 9 (mode 1 pretends there is always
enough), row 10 (ratio applies only in mode 2), row 11 (kbytes and ratio mutually exclusive), row 12 (user reserve),
row 14 (`allowed = ((totalram_pages() - hugetlb_total_pages()) * ratio / 100); allowed += total_swap_pages;`), row 15
(kbytes replaces the ratio term), row 17 (charged before the mode is examined), row 18 (`percpu_counter_read_positive`
< `allowed`), row 19 (`!cap_sys_admin` subtracts the admin reserve), row 21 (compiled-in ratio default 50), row 22
(per-CPU drift under loose modes), row 26 (hugetlb file mappings strict unless `MAP_NORESERVE`). The charge/uncharge
pair is read from the frozen copy, not from prose: `vm_acct_memory(pages)` at `util.c.v7.2:964`,
`vm_unacct_memory(pages)` at `:1000`, `return -ENOMEM` at `:1002`.

**(2) Refusal row.** The exact format string is `util.c.v7.2:998-999`:
`pr_warn_ratelimited("%s: pid: %d, comm: %s, bytes: %lu not enough memory for the allocation\n", __func__,
current->pid, current->comm, bytes_failed)`, with `bytes_failed = pages << PAGE_SHIFT` at `:997` and `__func__`
inside `int __vm_enough_memory(...)` (`:959`). So the entry's literal `__vm_enough_memory: pid: N, comm: X,
bytes: B …` line shape holds, the fields are pid, comm and bytes, and the warning is rate-limited by construction.
The lane rule that keeps the row honest is `corpus/QUALITY.md:29` (criterion 15): a journal class is counted by
MESSAGE_ID or another trusted structured field, never by message text — which is why the row permits presence and
forbids a count.

**(3) Living-pin rule.** Arm (C)'s three states and their tests are the counter docstring verbatim
(`.ufo/waves/round-52/count-c1.py`, lines 29–42 of the frozen file): good (shlex-parseable `python3|bash`
invocation, regular file at R, exit 0, last tally line matching numbers and prefix), superseded (QUALITY: a later
numbered criterion says `supersedes N's check`; either file: a later line carries `supersedes` with the stale span
and tally verbatim), and every pin at the entering tip still present byte for byte. Observed items, copied from the
receipts:

| item (data commit `8524904a`, `c1-at-data.txt`) | state |
|---|---|
| `corpus/QUALITY.md:885` expect `CONFORM_SELFTEST pass=6 fail=0` | `superseded` (criterion 111, `corpus/QUALITY.md:900`: "This row supersedes 109's check") |
| `corpus/QUALITY.md:909` expect `pass=12 fail=0` | `superseded` (criterion 141, `corpus/QUALITY.md:1356`) |
| `corpus/QUALITY.md:1360` expect `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0` | `ok`, `…_rc=0` |
| `corpus/README.md:607` expect `pass=9 fail=0` (bare `--selftest`) | `superseded` (note at `corpus/README.md:722`) |
| `corpus/README.md:608` expect `pass=12 fail=0` | `superseded` (same note) |
| `corpus/README.md:727`, `:728` expect `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0`, `CONFORM_SELFTEST pass=9 fail=0` | `ok`, `…_rc=0` |

At the entering tip (`control-c1-do-nothing.txt`) the three open pins read `QUALITY.md:909 → got=…pass=22…`,
`README.md:608 → got=…pass=22…`, `README.md:607 → got=unrunnable`; the README note states the same-line rule the
draft cites ("the counter reads a quoted stale pin as a quotation only when its replacement pin stands on the same
line", `corpus/README.md:729-730`).

## Out of scope (not drafted, not mine to add)

- The round-52 counter registry table rows (`| name | kind | entry | verdict map | … |`) and the round-52 LOG.md /
  SCORECARD round section: left to the L1 or the seat that holds them; my draft is the section body only, with no
  landed-tip reading invented.
- Landed-tip counter readings: the draft quotes the data-commit and entering-tip receipts only. Appending the
  landed-tip `C1=`/`C2=` lines is the L1's integration step.
- Entailment votes: I am not an ENTAILMENT seat; no `entailed`/`overclaim` judgment on any C2 row is recorded here,
  and no line of this report begins with the ENTAIL or REPLACE token.
- No re-run of either counter (receipts read, not reproduced).

## Line placement for SHONEN box 1 (asked by Mo52ScribeShonen)

`SKILL.md` at the data commit `8524904a`: 1141 lines, last line 1141 is 88 characters and the file's final byte is
`\n` (`tail -c 20 | od -c` → `… o o d . \n`). The round-50/51 boundary is one blank line then the heading
(`SKILL.md:1068` blank, `:1069` `## Round51 …`). My fenced draft is heading-first and carries 64 content lines
(report lines 38–101, fence lines 37 and 102), so an integration that appends one blank line then the block lands:

| position | line |
|---|---|
| last existing line of `## Round51` | 1141 |
| separator blank line | 1142 |
| `## Round52 — the self-assessment counter, the overcommit ledger and the living-pin rule` | **1143** |
| last line of the drafted section (`a living pin.`) | 1206 |

Mo52ScribeShonen's pin `SKILL.md:1143` is therefore correct for this draft unchanged. It shifts by exactly the
number of lines the L1 inserts before the heading (an extra blank line, or any lede/registry paragraph placed above
it); the draft itself contains no `path:N` locator pointing into `SKILL.md`, so nothing inside it renumbers.
Appending at EOF leaves `SKILL.md:1018-1067` and `SKILL.md:1069-1141` valid, both `state=ok` in
`evidence/c1-at-data.txt`.

## Findings

| # | severity | finding | file / line |
|---|---|---|---|
| 1 | LOW | The draft's living-pin rule inherits arm (C)'s enumeration limit verbatim: a pin split across lines, or one carrying a placeholder such as `<rev>`, is not enumerated as a pin, so a stale multi-line pin could pass. Stated in the draft as a named limit; the counter is frozen this round, so this is a routed item, not a repair. | `.ufo/waves/round-52/count-c1.py` docstring (pins/limits paragraph); `corpus/QUALITY.md:1362-1365` (141's "Not covered") |
| 2 | LOW | The entry's `Reading rules` say what a refusal means but not that the refused request leaves the ledger: `vm_acct_memory` at `util.c.v7.2:964` is undone by `vm_unacct_memory` at `:1000` before `-ENOMEM` at `:1002`. A reader watching `Committed_AS` around a refusal can reasonably expect a permanent step. My draft row cites the copy line numbers; if the L1 wants it in the entry, it is a data correction (allowed) and not a counter change. | `corpus/knowledge/overcommit-commit-limit-r52.md` `## Reading rules (mori)` row 3; `corpus/evidence/sources-r52/util.c.v7.2:964,996-1002` |
| 3 | LOW | The refusal line's printed prefix is `__func__`, i.e. `__vm_enough_memory`; the entry writes it as literal text, which I checked against the copy and it holds — recorded so a later reader does not treat the prefix as a source-file path. No correction needed. | `corpus/evidence/sources-r52/util.c.v7.2:959,998-999`; `corpus/knowledge/overcommit-commit-limit-r52.md` Reading rules row 3 |
| 4 | LOW | Arm (C) runs the pinned command unsandboxed inside an archive at R and watches only `git status` of the lane repo, so a living pin whose command writes to its cwd is invisible to `lane_writes`. Named limit, frozen; routed to round 53 with finding 1. | `.ufo/waves/round-52/count-c1.py` docstring limits paragraph; `evidence/c1-at-data.txt` (`lane_writes=0`) |
| 5 | LOW | `hidden=0` is scanned over `SHONEN.md` only (the docstring says so); a stray tally token in `corpus/QUALITY.md` or `corpus/README.md` outside a pin is not a hidden finding, so an un-pinned number there reads as prose. Named limit; routed. | `.ufo/waves/round-52/count-c1.py` docstring (B) arm and limits paragraph |
| 6 | LOW | Not a defect, recorded for the integrator: `SKILL.md` is untouched at the data commit (1141 lines, last byte `\n`, `## Round51` at 1069), so the heading-first draft appended after one blank line lands its `## Round52` heading at **1143** and its last line at 1206 — the line Mo52ScribeShonen pins in SHONEN box 1; appending at EOF does not disturb the `SKILL.md:1018-1067`, `SKILL.md:1069-1141` locators arm (D) already scores `ok`. | `SKILL.md:1069,1141`; `evidence/c1-at-data.txt` locator items; § Line placement above |

Scratch cleanup: `/fast/scratch/hyaku/mori-r52/Mo52ScribeSkill/` removed after the reads; no clone, no fixture, no
`/tmp` file, and no file created inside the lane or fleet repo by this seat except this report.
