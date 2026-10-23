# AttackSrc184 — source row S184 (Linux block/blk-core.c at v7.2)

Seat: wave 2 attack, source row S184. Read-only in the lane; no lane edits, no commits.
Revision under test: `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8` (lane master, `git rev-parse HEAD` → same).

Verdict: **no blocker**. One judge-dependent weakness in the teaches cell wording (F1, major if the
judge is literal, minor if it accepts the quoted function name) and one scope-label overreach that no
entry clause depends on (F2, minor). Every hard requirement of P-C1 that touches S184 passes (F3).

## F1 — teaches cell says "completed"/"ends" via a word no Gate quote contains (major, judge-dependent)

Attacks: `corpus/SOURCES.md:190` column `teaches` —
"bdev_end_io_acct adds the completed sectors with part_stat_add; update_io_ticks adds the elapsed time
to io_ticks only when an I/O ends or one is in flight."

Evidence — the three Gate quotes are `corpus/lessons/round-33.md:19`:

1. `S184.src:1100` (7 words): `void bdev_end_io_acct(struct block_device *bdev, enum req_op op,`
2. `S184.src:1110` (3 words): `part_stat_add(bdev, sectors[sgrp], sectors);`
3. `S184.src:1067-1068` (8 words): `(end || bdev_count_inflight(part))) __part_stat_add(part, io_ticks, now - stamp);`

Checked: the token "completed" (or "complet…", "finish…") occurs in **none** of the three quotes.
`command: python3` intersection of `[a-z0-9_]+` tokens — gate token set is
{bdev, block_device, bdev_end_io_acct, part_stat_add, sectors, sgrp, io_ticks, stamp, part,
__part_stat_add, bdev_count_inflight, void, enum, req_op, struct}; no completion word. The completion
fact is inferred from the *name* `bdev_end_io_acct` in quote 1 (line 1100), not stated by a token.
Same for "an I/O ends": quote 3 contains the bare parameter name `end` (line 1067); the line that makes
"end" mean *the end path* is `S184.src:1108` — `update_io_ticks(bdev, now, true);` — which is **not** in
the anchor `block/blk-core.c:1067-1068,1100,1110`.

Why this is a real risk, not a hypothetical: the wave-1 seat's draft quoted exactly that missing region —
`.ufo/waves/round-33/w1/SrcBlkCore.md:22` cites `SRC.src:1108-1111` (11 words:
"update_io_ticks(bdev, now, true); part_stat_inc(bdev, ios[sgrp]); part_stat_add(bdev, sectors[sgrp], sectors); part_stat_add(bdev, nsecs[sgrp], jiffies_to_nsecs(duration));").
The L1 narrowed the anchor to line 1110 alone, which dropped the `true` argument that carries the "ends"
reading. Under R-R ("a clause the judge would accept only with a caveat … is unsupported") a literal judge
can refuse this clause.

Propagation (same word, other files, all resting on the same quotes):
- `corpus/knowledge/disk-write-rate-r33.md:20` (row 2) reading: "The kernel adds to the sector counters
  when an I/O completes: `bdev_end_io_acct` adds the sectors it is given with `part_stat_add`…".
- `corpus/knowledge/disk-write-rate-r33.md:21` (row 3) reading: "…and completed sectors are added
  through `part_stat_add`…".

Cheap, contract-compliant repair (advice only; I did not edit): widen quote 2 to `S184.src:1108-1110`, which
is contiguous in the copy and 9 words — inside the 3-25 word and 1-4 quote bounds:
`update_io_ticks(bdev, now, true); part_stat_inc(bdev, ios[sgrp]); part_stat_add(bdev, sectors[sgrp], sectors);`
That states both `end == true` on the end path and the sector add, without adding a fourth quote.
(Adding line 1120, `bdev_end_io_acct(orig_bdev, bio_op(bio), bio_sectors(bio), start_time);`, would also
state that the added sectors come from a completed bio, but S184 already carries 3 quotes, so a 4th is the
ceiling — contract.md:23 "1-4 quotes of 3-25 words each".)

Confidence: high that the words are absent; medium on whether the judge will refuse (name-based acceptance
is defensible). [INFERENCE] on the judge's reading either way — my verdict is not counted.

## F2 — scope cell's "bio-based accounting" label is not established by the anchored lines (minor)

Attacks: `corpus/SOURCES.md:190` column `scope` — "v7.2 bio-based accounting: sectors added in
bdev_end_io_acct through part_stat_add; io_ticks advanced by elapsed time when I/O is in flight or ending".

The clause after the colon is stated by quotes 1-3. The label "bio-based" is not: the anchored lines
(1067-1068, 1100, 1110) live in `update_io_ticks` and `bdev_end_io_acct`; the bio link is only at
`S184.src:1117-1121`:

```
1117  void bio_end_io_acct_remapped(struct bio *bio, unsigned long start_time,
1118  			      struct block_device *orig_bdev)
1119  {
1120  	bdev_end_io_acct(orig_bdev, bio_op(bio), bio_sectors(bio), start_time);
1121  }
```

and `bdev_end_io_acct` is also the non-bio entry drivers call (S184.src:1100-1116, `EXPORT_SYMBOL`). So the
row labels a shared helper "bio-based". Impact is nil for C1: no entry clause depends on the bio link —
rows 2, 3 and 6 only need the sector add and the io_ticks guard. Severity minor (framing, not a fact any cell
asserts as observation).

## F3 — checks that passed (no defect found, with the checks named)

1. Live re-fetch, byte identity, sha256 triple match.
   `curl -sSL --fail -m 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-core.c -o live.src`
   → rc=0, 36689 bytes. sha256 of live = `528501312dbd8da7649051006f12203fbef03f5180c4408ccc20856262c77827`
   = committed copy (`sha256sum corpus/evidence/sources-r33/S184.src` → same) = Gate column
   (`corpus/lessons/round-33.md:19`). `cmp` committed vs live → identical. No 429, so no retry needed.
   Wave-1's two fetches also matched (`w1/SrcBlkCore.md:7-8`, 02:39:49Z and 02:39:54Z).
2. Every Gate quote at its stated locator in the committed copy (`sed -n` output):
   - 1065-1068: `	if (unlikely(time_after(now, stamp)) && / 	    likely(try_cmpxchg(&part->bd_stamp, &stamp, now)) && / 	    (end || bdev_count_inflight(part))) / 		__part_stat_add(part, io_ticks, now - stamp);`
   - 1100: `void bdev_end_io_acct(struct block_device *bdev, enum req_op op,`
   - 1110: `	part_stat_add(bdev, sectors[sgrp], sectors);`
   Enclosing functions confirmed: `update_io_ticks` def at 1060, body closes at 1074 (so 1067-1068 is inside
   it); `bdev_end_io_acct` signature 1100, body 1102-1114, `EXPORT_SYMBOL` 1115 (so 1110 is inside it).
   Whitespace-collapsed containment: `tr -s '[:space:]' ' ' < S184.src | grep -c -F '<quote>'` → 1 for each of
   the three quotes (including the two-line quote 1067-1068).
3. Stated word counts match a whitespace split: 7, 3, 8 — as written in the Gate row.
4. `io_ticks` is written in exactly one place in the whole file (`grep -n io_ticks` → 1060, 1068, 1080, 1108),
   so "only when an I/O ends or one is in flight" follows from the single guard at 1065-1068; no unguarded add
   exists that would falsify "only".
5. URL is tag-pinned, not a moving ref: the path is `/v7.2/`, and
   `GET api.github.com/repos/torvalds/linux/git/ref/tags/v7.2` → HTTP 200, `ref: refs/tags/v7.2`,
   `object.type: tag`, `object.sha: 237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63`. (A `git ls-remote --tags <url> v7.2`
   produced no ref line within its 100 s cap — the pipeline reported rc=0 from `head`, not from git, so that 0 is not
   a git exit status. I do not count ls-remote as evidence; the API response is the deciding check.)
6. No duplicate URL. Current tip: `grep -n -F '<url>' corpus/SOURCES.md` → only `SOURCES.md:190`;
   `grep -n 'blk-core' corpus/SOURCES.md` → only line 190. Entering tip: `git show 7d382043:corpus/SOURCES.md`
   → no match for the URL or for `blk-core` (grep rc=1), and no `| S184 |` row existed there.
7. Exactly one Gate row with that URL: `grep -c -F 'block/blk-core.c' corpus/lessons/round-33.md` → 1 (line 19);
   `grep -n S184 corpus/lessons/round-33.md` → line 19 only.
8. kind/tier: `code` / `A` matches the artifact — upstream kernel source at a release tag, plain C text
   (`head -1` → `// SPDX-License-Identifier: GPL-2.0`; zero hits for `<!DOCTYPE`, `<html`,
   `raw.githubusercontent.com` in the copy), same classification as sibling rows S182/S183/S185.
9. Row metadata consistency: `status` mined = Gate "admit, A, mined"; `recheck` on-release and
   `used-by corpus/knowledge/disk-write-rate-r33.md` are correct — that file cites S184 at lines 20, 21 and 24.
   `opened` 2026-10-23 equals the UTC date of the Gate `accessed` stamp 2026-10-23T02:39:49Z; in local time that
   moment was 2026-10-22T23:39-03 (`date -u` → 03:00Z while `date` → 2026-10-23 00:00 -03), so the column is
   UTC-dated. All eleven new rows S180-S190 carry 2026-10-23, so the convention is batch-consistent; no
   S184-specific defect.
10. Counter-side properties that depend on S184 (spot-checked with the counter's own tokenizer,
    `count-c1-a1.py:90-91` `[a-z0-9_]+`): rows citing S184 share enough 4+-letter words with S184's quotes —
    line 20: 3 (`bdev_end_io_acct`, `part_stat_add`, `sectors`); line 21: 2 (`part_stat_add`, `sectors`);
    line 24: 2. No reading cell of those rows contains a 6-consecutive-word run from an S184 quote (longest
    runs 1, 1, 2), so the anti-shortcut clause is not tripped by S184's quotes.

## What I did not check (unknowns / out of scope)

- I did not run `count-c1-a1.py` (counter attack belongs to another seat); item 10 above is a hand replication
  of its tokenizer, not the counter's verdict.
- I did not verify that the `v7.2` tag's peeled commit is what distros ship, nor any host-side behaviour
  (out of scope: this seat only judges whether the copy and the cells are upstream-supported).
- Whether the C1 judge treats a name-derived "completed" as a caveat — unobservable before the judge runs.
- Tool installs/updates: none. No processes left running (the one `git ls-remote` job finished; nothing of mine
  remains).
