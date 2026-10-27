# Mo52ScribeReadme — `corpus/README.md` round-52 coverage additions (draft, fenced)

Seat: Mo52ScribeReadme (leaf; no subagents). Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`, entering tip
`4f266ef2`, freeze `d3a8ea59`, data `8524904a`, wave-spec tip `075436b1`. Scratch
`/fast/scratch/hyaku/mori-r52/Mo52ScribeReadme/` (created per the operator directive, `TMPDIR` inside it, removed
before this report was written; the draft below was copied into this report before removal). The contract
(`.ufo/waves/round-52/contract.md`) was read first.

## Behavior

Read, in this order: the contract; the round-51 coverage block and the round-52 corrections block of
`corpus/README.md`; the `## Frontier` table and its FR8 row (`corpus/README.md:348`); the C2 entry
`corpus/knowledge/overcommit-commit-limit-r52.md`; `corpus/SOURCES.md` S497–S501;
`.ufo/waves/round-52/evidence/sweep-overcommit.txt`; `.ufo/waves/round-52/evidence/c2-at-data.txt`; and the three
instruments the draft row cites (`tools/mori-census.sh`, `scripts/hyaku/inline-dispatcher.py`,
`scripts/hyaku/wave-slot.sh`), plus `SKILL.md:3,19,1115-1123` for the lane's runway remit and the round-51 runway
reading rules.

Drafted one section, in three parts, for the END of `corpus/README.md` (after `## Round-52 corrections (living
pins)`, which starts at line 722):

1. `## Round-52 coverage additions` — one coverage-map row under the round-50/51 house header
   `| coverage-map row | entry | ground | sweep |`, covering the overcommit entry as resource-runway, new ground,
   with the sweep receipt and the instrument reads that bound the ground cell.
2. A `Count:` paragraph that records the data-commit counter receipt rather than asserting a tally that runs
   today: 28 claim rows, 28 located quotes, `failed=entailment` (the one arm open at the data commit).
3. A dated append-only note: round 52 supersedes the resource-runway ground's silence about the commit ledger;
   FR8 alert-threshold calibration stays open and no `Committed_AS/CommitLimit` threshold is proposed; no frontier
   row is rewritten.

Placement is append-only on purpose: the section is added after the committed round-52 corrections block, so no
byte above it moves and the frontier table (`corpus/README.md:338-352`) stays untouched. `git status --porcelain
corpus/README.md` is empty (rc 0) — this seat edited no lane file.

## Evidence

| # | command (cwd = lane root unless absolute) | output | rc |
|---|---|---|---|
| a | `git -C …/mori-shokunin log --oneline -3` | `075436b1 round-52: wave w1 spec …`; `8524904a round-52: data …`; `d3a8ea59 round-52: freeze …` | 0 |
| b | `grep -c 'CommitLimit\|Committed_AS\|overcommit' corpus/README.md` | `0` | 1 |
| c | same over `SCORECARD.md` | `0` | 1 |
| d | same over `corpus/QUALITY.md` | `0` | 1 |
| e | `sed -n '/^## Claims/,/^## Reading rules/p' corpus/knowledge/overcommit-commit-limit-r52.md \| awk -F'\|' '/^\|/ && $3 ~ /S[0-9]/ {…count…}' \| sort` | `S497 7`, `S498 6`, `S499 9`, `S500 2`, `S501 4` (sum 28) | 0 |
| f | same range, `grep -c '^\|'` | `30` (header + separator + 28 claim rows) | 0 |
| g | `grep -rl 'CommitLimit\|Committed_AS' --include='*.sh' --include='*.py' /home/vgpnk/Projects/shokunin` (read-only, `.git` filtered) | `.ufo/waves/round-52/count-c2.py` (docstring only, `:2`), `.ufo/waves/round-52/build-w1-spec.py` (spec text, `:38`); no script reads either line | 0 |
| h | `grep -n 'meminfo_field MemAvailable' tools/mori-census.sh` | `1792:    mavail=$(meminfo_field MemAvailable)` | 0 |
| i | `grep -n 'MemAvailable' scripts/hyaku/inline-dispatcher.py scripts/hyaku/wave-slot.sh` | `inline-dispatcher.py:45,130,133`; `wave-slot.sh:8,68` (`mem_avail_mb()` awk over `/proc/meminfo`) | 0 |
| j | `grep -n '^## Round-5' corpus/README.md` | `685:## Round-50 coverage additions`; `698:## Round-51 coverage additions`; `722:## Round-52 corrections (living pins)` | 0 |
| k | `git status --porcelain corpus/README.md` | empty | 0 |
| l | `ls .ufo/waves/round-52/evidence/ \| grep -E 'c2-at-data\|control-c2\|control-c1'` | `c2-at-data.txt`, `control-c1-*.txt` ×7, `control-c2-do-nothing.txt` | 0 |
| m | `.ufo/waves/round-52/evidence/c2-at-data.txt` (read) | `python3 .ufo/waves/round-52/count-c2.py 8524904a…` → `C2=unmet claims=28 located=28 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=8524904a… failed=entailment`, `exit=1` | (receipt; I did not re-run the counter — draft-only seat) |
| n | `.ufo/waves/round-52/evidence/sweep-overcommit.txt` (read) | 13 terms → `0` files each over `corpus/SOURCES.md corpus/knowledge SKILL.md`; `merge/mori`: `CommitLimit 0`, `Committed_AS 0`, `overcommit 0` | — |
| o | `scripts/hyaku/disk-guard.sh status` | `/fast/scratch/hyaku/mori-r52` 12.6G, no ENOSPC line | 0 |
| p | static pin check (frozen regexes `TALLY/ANY_TALLY/PIN/LPIN/HIDDEN` exec'd from `.ufo/waves/round-52/count-c1.py:71-79`, applied to the draft bytes) | `PIN []`, `LPIN []`, `HIDDEN []`, `TALLY []`, `ANY_TALLY []`; no draft line starts with the two vote keywords; backtick parity 0; row length 1895 chars | 0 |

Two claims in the draft row are grounded in (h)–(i) and (g): the census reads `MemAvailable` only, the two hyaku
gates read `MemAvailable` only, and no fleet `*.sh`/`*.py` reads `CommitLimit` or `Committed_AS`. The row's
"new ground" clause rests on (b)–(d) plus (n): the three living documents and the pre-data sweep hold neither line.

## Draft (append at the end of `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/README.md`)

```markdown
## Round-52 coverage additions

| coverage-map row | entry | ground | sweep |
|---|---|---|---|
| resource runway — what `/proc/meminfo`'s two commit lines, `CommitLimit` and `Committed_AS`, are (the ledger `vm_commit_limit()` prints as RAM minus hugetlb pages scaled by `vm.overcommit_ratio`, or `vm.overcommit_kbytes` when that knob is nonzero, plus every swap page; `Committed_AS` is a batched per-CPU counter, and the meminfo line is its full sum) and when the limit is enforced: a request is charged under every mode, but only `vm.overcommit_memory=2` refuses (mode 0 refuses only a request larger than all RAM plus swap, mode 1 never refuses), so `Committed_AS > CommitLimit` is normal under the default modes and a refusal is ENOMEM at request time, not a kill when pages are touched | `knowledge/overcommit-commit-limit-r52.md` (S497–S501, opened 2026-10-26; 28 claim rows: S497 7, S498 6, S499 9, S500 2, S501 4) | new ground — no FR row held it; the map and the instruments held `MemAvailable` only (round-51 row above; `tools/mori-census.sh:1792`, `../../scripts/hyaku/inline-dispatcher.py:133`, `../../scripts/hyaku/wave-slot.sh:68`, and no script reads either commit line). States the kernel's model at v7.2, never a host value as typical, and reports rather than configures (`vm.overcommit_memory`, `vm.overcommit_ratio`, `vm.overcommit_kbytes` and both reserves are tsukuroi's; mori reads and never writes a `vm.*` sysctl), and reads the pair with `vm.overcommit_memory` or the two numbers cannot say whether the limit is enforced | `CommitLimit`, `Committed_AS`, `overcommit_memory`, `overcommit_ratio`, `overcommit_kbytes`, `vm_commit_limit`, `__vm_enough_memory`, `vm_committed_as`, `user_reserve_kbytes`, `admin_reserve_kbytes`, `MAP_NORESERVE`, `OVERCOMMIT_NEVER` and `overcommit-accounting` → 0 in `corpus/SOURCES.md`, `corpus/knowledge` and `SKILL.md` at `4f266ef2`, and read-only `merge/mori` holds 0 files on it (`.ufo/waves/round-52/evidence/sweep-overcommit.txt`) |

Count: 28 claim rows and 28 located quotes over the five sources — at the data commit `8524904a`
`.ufo/waves/round-52/evidence/c2-at-data.txt` records
`python3 .ufo/waves/round-52/count-c2.py 8524904adb25e44f24d9f25aac7eae909625c18c` → `C2=unmet claims=28
located=28 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 …
failed=entailment` (exit 1): every quote resolves in its committed copy, and the wave's per-row entailment
votes — at least two ENTAILMENT seats that did not write the row's text — were the one arm still open at the
data commit.

Dated note (append-only, 2026-10-26): round 52 supersedes the resource-runway ground's silence about the commit
ledger — `CommitLimit` and `Committed_AS` are printed under every overcommit mode but enforced only under mode 2,
which refuses a mapping at request time instead of killing a process when pages are touched, so an over-committed
total is not pressure by itself and the limit is not a kill threshold
(`knowledge/overcommit-commit-limit-r52.md`, S497–S501); no frontier row is rewritten. Still frontier: no host
`Committed_AS` or `CommitLimit` value is claimed, the entry claims the v7.2 bytes only, the ledger's named holes —
ptrace pages unaccounted, hugetlb `MAP_NORESERVE` mappings uncharged even under mode 2 — bound every sum read from
it, and FR8's alert-threshold calibration stays open: no `Committed_AS/CommitLimit` threshold is proposed, and the
overcommit mode and both reserve knobs are host configuration the operator owns.
```

Integration notes for the L1:

- Append exactly as fenced, after `corpus/README.md:733` (`Counter: … arm (C) (QUALITY 141).`); nothing above it is
  edited. If the L1 prefers round-52 material contiguous, the block may be inserted between line 720 (end of the
  round-51 dated note) and line 722 (`## Round-52 corrections (living pins)`) — that inserts bytes but deletes
  none. I drafted the append form.
- The row claims no host value and no threshold, so it needs no host read and cannot go stale by a host reading
  changing.
- The `Count:` paragraph is a receipt quote with the commit named; it deliberately carries no `--selftest` span and
  no `pass=/fail=` tally, so the frozen C1 living-pin arm (LPIN) does not enumerate it (evidence p). If the L1
  rewrites it into a "prints today" sentence, that sentence will be false after the vote reports land, because
  `count-c2.py` reads the reports from the working tree.

## Touched surfaces

- Written: this report only (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-52/w1/Mo52ScribeReadme.md`).
- Created and removed: `/fast/scratch/hyaku/mori-r52/Mo52ScribeReadme/` (held the draft copy; the directory is
  removed, so only this report carries the bytes).
- Not touched: `corpus/README.md`, `SHONEN.md`, `SCORECARD.md`, `LOG.md`, `corpus/`, `tools/`, `considerthese/`,
  `SKILL.md`, any other round-52 file, `/home/vgpnk/Projects/shokunin` root, `~/.local/bin`, any jj or git state.
- No tool installed or upgraded (pacman paused host-wide; nothing was needed).

## Out of scope

- Running `count-c1.py` or `count-c2.py` (verification is the L1's; both were read only, and I quote their
  receipts).
- Editing the Frontier FR8 row, the round-51 row, or the round-52 corrections block — all append-only surfaces.
- Any `/proc/meminfo` host value: the draft claims none, and one wave seat holds the read-only host check as
  own-work evidence.
- Any claim about C1's remaining mismatches or about the vote outcome.

## Findings

- MED — `corpus/README.md:348` (FR8 row in `## Frontier`): the `first evidence` cell still reads
  `knowledge/audit-r11.md:205` only, although two rounds have since bounded this frontier's calibration ground
  (`knowledge/memavailable-estimate-r51.md`, `knowledge/overcommit-commit-limit-r52.md`). Frontier rows are
  append-only, so the draft carries the update in its dated note; the cell itself stays stale by design and is
  routed, not fixed here.
- MED — instrument gap for the new ground: no census, gate or receipt reads `CommitLimit` or `Committed_AS`
  (evidence g–i; the census and both hyaku gates read `MemAvailable`). The entry is depth ground and its row says
  so, but a reader looking for a runway row on the commit ledger will find none; a commit-ledger census line is a
  candidate item for round 53, not a fix for this round.
- LOW — `corpus/README.md:702` names the round-51 sweep revision `aa3af1ec` while the new row names `4f266ef2`;
  both are the revision their sweep actually ran at. Recorded so the L1 does not "unify" them into one revision.
- LOW — `corpus/README.md:722` (round-52 corrections) now precedes the appended round-52 coverage block, so
  round-52 sections are not contiguous. Accepted to keep the change pure append; the alternative (insertion before
  line 722) is noted above.
- LOW — a data-commit `C2=unmet … failed=entailment` receipt cannot be reproduced after the wave, because
  `count-c2.py` reads the vote reports from the working tree; the draft therefore states it as a receipt quote
  ("records", commit named) and keeps it out of the living-pin arm. This is the same shape round 51 shipped, and it
  is a named limit of the `Count:` convention, not a counter defect.
