# Mo52ScribeQuality — QUALITY.md criteria 143-144 (drafts)

Seat: Mo52ScribeQuality (scribe). Assignment: draft `corpus/QUALITY.md` criterion 143 onward in the house style
(Lesson, Check, Shown able to fail, Not covered): (a) a depth row needs two `entailed` votes from voters that did
not write its text (P-C2 arm); (b) a runway reading of `CommitLimit` is mode-dependent — under modes 0/1 the line
is printed, not enforced. Drafts are fenced below and NOT applied: this seat wrote only this report file.

Entering facts read, not rerun: data commit `8524904adb25e44f24d9f25aac7eae909625c18c`; lane tip at seat start
`075436b1346ca659afb8be7a46f0e67e4170aa83`; contract `.ufo/waves/round-52/contract.md`; entry
`corpus/knowledge/overcommit-commit-limit-r52.md` (75 lines); SOURCES rows S497-S501 at `corpus/SOURCES.md:276-280`;
counter `.ufo/waves/round-52/count-c2.py` (522 lines); receipts `evidence/c2-at-data.txt`,
`evidence/selftest-c2.txt`, `evidence/c2-hashes-at-data.txt`.

## Observed gates (command + output + exit code)

Data commit, from the committed receipt `evidence/c2-at-data.txt`:

```
$ python3 .ufo/waves/round-52/count-c2.py 8524904adb25e44f24d9f25aac7eae909625c18c
C2=unmet claims=28 located=28 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=8524904adb25e44f24d9f25aac7eae909625c18c failed=entailment
exit=1
```

Same command at lane tip `075436b1`, run read-only by this seat (`--repo` the lane, nothing written):

```
C2=unmet claims=28 located=28 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=075436b1346ca659afb8be7a46f0e67e4170aa83 failed=entailment
exit=1
```

`ls .ufo/waves/round-52/w1/Mo52Ent*.md | wc -l` printed `10` at that moment: ten voter files exist in the working
tree, and the counter reads committed bytes at R only, so they contributed nothing yet. Observation, not a defect:
P-C2 is met only by commits.

Selftest arms for (a), read from `evidence/selftest-c2.txt` (last line `C2_SELFTEST pass=45 fail=0`, `exit=0`):
`PASS entail_one_voter_unmet`, `PASS entail_same_voter_twice_unmet`, `PASS entail_one_row_single_vote_unmet`,
`PASS entail_author_vote_not_counted_unmet`, `PASS entail_author_plus_two_others_met`,
`PASS entail_fenced_replace_not_authorship_met`.

Row hashes: `evidence/c2-hashes-at-data.txt` holds 28 `row=N hash=<h>` lines (rows 1-28, `row=1 hash=9afaa81505da`
… `row=28 hash=42295e410c2b`), and `count-c2.py --hashes 8524904a…` printed the same 28 lines, `exit=0`.

Counter internals cited by the drafts (read, not modified): `VOTERS` `:44`, `MIN_VOTES = 2` `:45`,
`entail_votes()` `:126-149` (fence toggle `:136-142`), the per-row test `:238-243` (`ok_voters` excludes a voter
whose `REPLACE` text hashes to the row), `--hashes` mode `:291-299`.

## Replay of the (a) arm on the real 28-row entry (this seat's scratch)

Fixture: `git clone --shared --no-checkout` of the lane into
`/fast/scratch/hyaku/mori-r52/Mo52ScribeQuality/repo`, `git -C … rev-parse --show-toplevel` printed that path,
`git -C … reset --hard 8524904a…` checked out the data commit, votes written under
`.ufo/waves/round-52/w1/` and committed there only (`-c user.name=scribe -c user.email=scribe@localhost`).

```
# commit 328ba5cd9d514020135d6db2b1dd89ad246376bc — Mo52Ent01.md, 28 lines, one voter
C2=unmet claims=28 located=28 … entailed=0 dissent=0 rev=328ba5cd9d514020135d6db2b1dd89ad246376bc failed=entailment
exit=1
# commit 34d41196ffa251057ede9043bce430a684091798 — Mo52Ent02.md added, same 28 lines
C2=met claims=28 located=28 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=28 dissent=0 rev=34d41196ffa251057ede9043bce430a684091798
exit=0
# commit 60835c799c1e3fdac3debff0475f887698349ae4 — Mo52Ent01.md also carries
# "REPLACE 9afaa81505da :: <row 1 claim text>"
C2=unmet claims=28 located=28 … entailed=27 dissent=0 rev=60835c799c1e3fdac3debff0475f887698349ae4 failed=entailment
exit=1
```

So on the real entry, one voter leaves every row uncounted, two voters meet all 28, and a voter's own `REPLACE`
line on row 1 drops exactly that row. No committed receipt under `.ufo/waves/round-52/evidence/` and the scratch
tree was removed, so the draft marks this replay `not yet shown` as a committed arm.

## Falsifier for the (b) rule (this seat's scratch)

The entry's reading row is `corpus/knowledge/overcommit-commit-limit-r52.md:58`. Copied the committed bytes of the
entry to scratch (`git -C repo show 8524904a…:corpus/knowledge/overcommit-commit-limit-r52.md`), then made
`entry-bad.md` whose row reads "| `Committed_AS` > `CommitLimit` under mode 0 or 1 | the kernel refuses further
allocations at the limit | memory pressure |". Loop:

```
$ for p in 'printed under every mode' 'printed, not enforced' 'enforced only under mode 2'; do
    printf '%s -> ' "$p"; grep -c -- "$p" "$f"; done
== entry-ok.md
printed under every mode -> 1
printed, not enforced -> 1
enforced only under mode 2 -> 2
== entry-bad.md
printed under every mode -> 1
printed, not enforced -> 0        (grep exit 1 on the last pattern run)
```

Source gates, run against the frozen copies under `corpus/evidence/sources-r52/` and the round-51 copy:

```
$ grep -n 'if (sysctl_overcommit_memory == OVERCOMMIT_\|allowed = vm_commit_limit' corpus/evidence/sources-r52/util.c.v7.2
969:	if (sysctl_overcommit_memory == OVERCOMMIT_ALWAYS)
972:	if (sysctl_overcommit_memory == OVERCOMMIT_GUESS) {
978:	allowed = vm_commit_limit();
$ grep -n 'vm_acct_memory(pages);' corpus/evidence/sources-r52/util.c.v7.2
964:	vm_acct_memory(pages);
$ grep -n 'CommitLimit:' corpus/evidence/sources-r51/meminfo.c.v7.2
125:	show_val_kb(m, "CommitLimit:    ", vm_commit_limit());
```

`fs/proc/meminfo.c` prints the line at `:125` with no mode branch around it (`:118-132` read), and the only
comparison against the limit is after the two loose-mode returns. The entry's own line 14 already cites
`fs/proc/meminfo.c:125-126` for the round-51 copy (S494).

## Drafts (fenced, NOT applied)

Draft text for insertion under the existing heading `## Criteria added round 52 — a living pin is current or
superseded, and a self-assessment pointer lands on its words`, after 142:

```markdown
143. **A depth row is counted only when two ENTAILMENT voters that did not write its text vote `entailed`, and any
    voter's `overclaim` blocks the row.** This row supersedes 140's arm sentence only; 140's criterion stands.
    Lesson: `corpus/lessons/round-51-verifier-spotcheck.md` §5 item 2 (round 51's arm met with one `entailed` line
    per row although the wave dispatches three voters per block of seven rows; 140's Not covered names that
    one-vote arm); no round-52 M row. Rationale: at the data commit `8524904a` the counter printed
    `C2=unmet claims=28 located=28 … entailed=0 dissent=0 … failed=entailment` (`evidence/c2-at-data.txt`, exit 1),
    so location alone did not satisfy depth. P-C2 (`count-c2.py:44-45,126-149,236-243`) counts a row only when at
    least two distinct voters from the frozen list `Mo52Ent01`–`Mo52Ent12` carry an unfenced line
    `ENTAIL <h> entailed`, where `<h>` is the row's claim cell with whitespace collapsed and ends stripped hashed
    to 12 hex digits, and a voter's own `REPLACE <old> :: <text>` line whose text hashes to `<h>` removes that
    voter's vote on that row. Check: `python3 .ufo/waves/round-52/count-c2.py <rev>` exits 0 and prints
    `C2=met claims=28 located=28 … entailed=28 dissent=0`, and `python3 .ufo/waves/round-52/count-c2.py --hashes
    <rev>` prints 28 `row=N hash=<h>` lines equal to `.ufo/waves/round-52/evidence/c2-hashes-at-data.txt`. Shown
    able to fail: `C2_SELFTEST pass=45 fail=0` (`.ufo/waves/round-52/evidence/selftest-c2.txt`) carries
    `entail_one_voter_unmet`, `entail_same_voter_twice_unmet`, `entail_author_vote_not_counted_unmet` and
    `entail_author_plus_two_others_met`; replaying the entry at `8524904a` in a scratch clone, one voter printed
    `entailed=0` exit 1, a second voter printed `entailed=28 dissent=0` exit 0, and that voter's `REPLACE` line
    for row 1 printed `entailed=27` exit 1 (seat scratch `Mo52ScribeQuality`, no committed receipt, so the
    committed arm is `not yet shown`). Not covered: an `entailed` line records that a lane seat asserted the
    judgment for that exact claim-cell text, not that the judgment is right; `REPLACE` is the only authorship
    signal read, so a voter that rewrites text without that line keeps its vote; a fenced vote is invisible, so a
    voter that quotes the format in a fence loses the vote; the hash covers the claim cell, not the quote (the
    quote is located separately, never voted); two voters meet the arm although the wave dispatches three per
    block, so a row can meet on a minority of its voters; `<h>` is 12 hex digits, so two different claim cells
    could collide (unobserved).
144. **A runway reading of `CommitLimit` names the overcommit mode: under `vm.overcommit_memory` 0 or 1 the line is
    printed, not enforced, and no lane document reports a commit refusal without mode 2.** This row complements
    139 (the `MemAvailable` runway line) and supersedes nothing. Lesson: no round-51 or round-52 M row; the
    pointer is `corpus/knowledge/overcommit-commit-limit-r52.md` Reading rules, sourced by S497 (the three modes)
    and S499 (`__vm_enough_memory`). Rationale: the other two meminfo runway lines were undefined in the lane until
    this round (`evidence/sweep-overcommit.txt`: thirteen terms at 0). `fs/proc/meminfo.c:125-126` prints
    `CommitLimit` and `Committed_AS` with no mode branch, while the comparison against the limit sits in
    `__vm_enough_memory`: charging at `mm/util.c:964`, the `OVERCOMMIT_ALWAYS` return at `:969`, the
    `OVERCOMMIT_GUESS` block at `:972-977`, and `allowed = vm_commit_limit()` at `:978` — so under modes 0 and 1
    the committed counter grows and no request is measured against the limit. Check:
    `for p in 'printed under every mode' 'printed, not enforced' 'enforced only under mode 2'; do printf '%s -> '
    "$p"; grep -c -- "$p" corpus/knowledge/overcommit-commit-limit-r52.md; done` prints
    `printed under every mode -> 1`, `printed, not enforced -> 1`, `enforced only under mode 2 -> 2`;
    `grep -n 'if (sysctl_overcommit_memory == OVERCOMMIT_\|allowed = vm_commit_limit'
    corpus/evidence/sources-r52/util.c.v7.2` prints `969:`, `972:`, `978:`; and `grep -c 'CommitLimit'
    corpus/evidence/sources-r51/meminfo.c.v7.2` prints `1`. Shown able to fail: on a scratch copy of the entry
    whose mode-0/1 row reads "the kernel refuses further allocations at the limit", the loop prints
    `printed, not enforced -> 0` and that grep exits 1 (seat scratch `Mo52ScribeQuality`, no committed receipt, so
    the committed arm is `not yet shown`). Not covered: v7.2 bytes only; this seat read no host
    `/proc/sys/vm/overcommit_memory`, so the row says nothing about this host's mode or values; the greps catch
    explicit enforcement wording, not a reading that implies a refusal in other words; under mode 2 the pair still
    does not predict a kill (entry row 3), and `CommitLimit` includes swap, so together the lines are a ledger in
    every mode, not a forecast in any.
```

## Touched surfaces

- Wrote only `.ufo/waves/round-52/w1/Mo52ScribeQuality.md` (this file).
- Read-only elsewhere: `corpus/QUALITY.md`, `corpus/knowledge/overcommit-commit-limit-r52.md`,
  `corpus/SOURCES.md:276-280`, `corpus/lessons/round-52.md`, `corpus/evidence/sources-r52/*`,
  `corpus/evidence/sources-r51/meminfo.c.v7.2`, `.ufo/waves/round-52/{contract.md,count-c2.py,evidence/*}`,
  `scripts/hyaku/disk-guard.sh status` (rc 0, `/fast/scratch/hyaku` 25% used, 605.1G free).
- Scratch `/fast/scratch/hyaku/mori-r52/Mo52ScribeQuality/` (clone + three fixture commits + entry copies) created
  with `TMPDIR` inside it and removed with `rm -rf` before this report; nothing was written into the lane, the
  fleet repo, `~/.local/bin`, or `shokuknow`. No tool installed or upgraded this seat.
- Out of scope, untouched: C1 (`SCORECARD.md`, `SHONEN.md`, `count-c1.py`, the living pins), the L1's data
  wording, the counter and its predicate, and every sibling `w1/*.md`.

## Findings

- LOW — `corpus/knowledge/overcommit-commit-limit-r52.md:58`: the reading row's pointer `util.c.v7.2:969-977`
  stops one line before `allowed = vm_commit_limit()` at `:978`, so a reader following that pointer alone sees the
  two loose-mode returns but not the line that applies the limit; the row's own sentence is correct for modes 0/1,
  and extending the range to `:969-978` (or `:964-978`) would carry both halves. The L1 may correct the cite; the
  counter is unaffected.
- LOW — `.ufo/waves/round-52/w1/`: at tip `075436b1` ten `Mo52Ent*.md` files existed in the working tree while the
  counter read `entailed=0`, because P-C2 reads committed bytes at R. The wave's votes must be committed before the
  closing gate or C2 stays `unmet` with `failed=entailment`; this is the arm working as frozen, recorded here so
  the closing seat does not read `entailed=0` as a vote-writing failure.
- LOW — the draft 143 Check names `entailed=28` as the target line, which is true only after the votes land; the
  draft therefore also cites the data-commit receipt (`entailed=0`) as the arm's pre-vote reading, mirroring 140.
  A closing seat that runs the counter before the vote commit will read `C2=unmet` by design.
- LOW — `evidence/selftest-c2.txt` records 45 arms and none of them exercises the `CommitLimit` mode rule of draft
  144 (the entry-level arms are structural: header, table, quotes, sources, provenance). Draft 144's shown-able-to-
  fail leg is a scratch copy, not a counter arm, so the rule is documented but not instrumented; a successor arm
  would belong to round 53's counter freeze, not to this round's frozen counter.
