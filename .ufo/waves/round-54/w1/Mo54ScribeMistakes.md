# Round-54 scribe — draft of the lesson's `## Mistakes` (M1 receipt-revision, M2 stale-strays, M3 wrong-file)

Seat Mo54ScribeMistakes, lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin`, read at working tree +
`HEAD = 2d0347a3` (round-54 wave spec commit) with `39dcf4d7` (entering tip), `6830f3af` (freeze), `1116c092` (data)
as comparison revisions. Leaf seat: no subagents, no lane edits, no counter or vote runs. Every number below is from a
command in §Observed; nothing is copied from a peer report without naming it as that peer's measurement.

The draft is fenced and self-contained. It is written for `corpus/lessons/round-54.md` and assumes the lesson's
numbering is exactly this order (M1, M2, M3) — `corpus/QUALITY.md:1479` (`QUALITY 148`) already cites
`lessons/round-54.md#M1` and `:1492` (`QUALITY 149`) cites `#M2`, so the anchors are pre-committed by the criteria.

## Observed

### M1 — receipt revision in the round-53 claim rows

The two cells, read at `HEAD` (identical to `39dcf4d7`, the rows were committed in round 53):

```
$ awk 'NR==2796{print substr($0,length($0)-260)}' SCORECARD.md
… holds=46 changed=0 voted=46 dissent=0`, rc 0 — `evidence/c1-at-salvage.txt` (R = `0df80303`; the at-landed re-run is named in the round-53 report) |
$ awk 'NR==2797{print substr($0,length($0)-300)}' SCORECARD.md
… registry=ok live=ok`, rc 0 — `evidence/c2-at-salvage.txt` (R = `0df80303`; the data commit read `n=23`, `evidence/c2-at-data.txt`; the at-landed re-run is named in the round-53 report) |
```

Nothing numeric differs between the cited and the landed receipts (contra round 53's own M1, which was digit drift):

```
$ for c in c1 c2; do grep -h "^${c^^}=" .ufo/waves/round-53/evidence/$c-at-salvage.txt | head -1 | sed 's/ rev=[0-9a-f]*//' > /tmp/s;
  grep -h "^${c^^}=" .ufo/waves/round-53/evidence/$c-at-landed.txt | head -1 | sed 's/ rev=[0-9a-f]*//' > /tmp/l;
  cmp -s /tmp/s /tmp/l && echo "$c identical-modulo-rev"; done
c1 identical-modulo-rev
c2 identical-modulo-rev
```

Fix check (`QUALITY 148`'s instrument), run by this seat:

```
$ python3 .ufo/waves/round-54/checks/receipt-stage.py 39dcf4d7e410d362781a47e8365ca23b5c807598
FLAG line 2668 round 50 cites a2-c1-at-data while .ufo/waves/round-50/evidence/a2-c1-at-landed.txt exists
FLAG line 2669 round 50 cites a2-c2-at-data while .ufo/waves/round-50/evidence/a2-c2-at-landed.txt exists
FLAG line 2796 round 53 cites c1-at-salvage while .ufo/waves/round-53/evidence/c1-at-landed.txt exists
FLAG line 2797 round 53 cites c2-at-salvage while .ufo/waves/round-53/evidence/c2-at-landed.txt exists
FLAG line 2797 round 53 cites c2-at-data while .ufo/waves/round-53/evidence/c2-at-landed.txt exists
RECEIPT_STAGE rev=39dcf4d7 cited_intermediate=5 flagged=5
exit=1

$ python3 .ufo/waves/round-54/checks/receipt-stage.py 2d0347a3…   (HEAD)
… same five FLAG lines …
RECEIPT_STAGE rev=2d0347a3 cited_intermediate=5 flagged=5
exit=1
```

Positive direction, which no committed revision can produce (the two correction paragraphs are working-tree only):
this seat built a four-file fixture in its scratch (`D=/fast/scratch/hyaku/mori-r54/Mo54ScribeMistakes/fixture-receipt-stage`,
`git -C "$D" init -q`, `rev-parse --show-toplevel` printed `$D`, commit `e34deaf7`), holding the working-tree
`SCORECARD.md` plus `git show HEAD:` of the four `*-at-landed.txt` files the flags name:

```
$ python3 .ufo/waves/round-54/checks/receipt-stage.py e34deaf7ad50ebda01b7a037da1bc7478994a5a6 --repo "$D"
RECEIPT_STAGE rev=e34deaf7 cited_intermediate=5 flagged=0
exit=0
```

State of the fix's bytes: `git status --porcelain` lists ` M SCORECARD.md` (`git diff --stat` → `SCORECARD.md | 15
+++++++++++++++`, `corpus/QUALITY.md | 41 +++++…`); the correction paragraphs are at `SCORECARD.md:2850`
(`**Round-53 correction:**`) and `:2858` (`**Round-50 correction:**`). No `receipt-stage-after.txt` exists in
`.ufo/waves/round-54/evidence/` (`ls` lists `receipt-stage-before.txt` only).

### M2 — eight lane-root strays

```
$ git ls-tree --name-only 39dcf4d7
.gitignore .scratch .ufo 0 AGENTS.md LOG.md MANPAGE.md MINT.md PROVINCE.md README.md SCORECARD.md SHONEN.md
SKILL.md base.c considerthese corpus main.c meminfo.c oom_kill.c sd-main.c tools user@.service.in
$ git ls-tree --name-only HEAD
.gitignore .scratch .ufo AGENTS.md LOG.md MINT.md PROVINCE.md README.md SCORECARD.md SHONEN.md SKILL.md
considerthese corpus tools
```

```
$ git log --format='%h %ci %s' --diff-filter=A -- base.c
763d3469 2026-10-22 15:06:33 -0300 round-28: amendment A1 before data … misroot sweep of seven r27 fetches with hash check
$ git log --format='%h %ci %s' --diff-filter=D -- base.c
1116c092 2026-10-27 01:33:23 -0300 round-54: data — … D3 lane-root strays relocated under rounds 28/38
$ git log --format='%h %ci %s' --diff-filter=AD -- 0
1116c092 … deleted …
96f7f97e 2026-10-23 23:47:54 -0300 round-38: residual re-check … misroot relocations (0, m9) …
$ git log --format='%h %ci %s' --diff-filter=AD -- MANPAGE.md
1116c092 … deleted …   /   763d3469 … added …
```

Relocation is byte-exact (blob ids compared end to end):

```
$ for p in base.c main.c meminfo.c oom_kill.c sd-main.c "user@.service.in" MANPAGE.md; do
    [ "$(git rev-parse "39dcf4d7:$p")" = "$(git rev-parse "HEAD:.ufo/waves/round-28/misroot-lane-root/$p")" ] \
      && echo "OK $p"; done;  … 0 → .ufo/waves/round-38/misroot-lane-root/0 …
OK base.c 780f8125…  OK main.c e695f375…  OK meminfo.c 25936e19…  OK oom_kill.c 5f372f6e…
OK sd-main.c 61726a02…  OK user@.service.in a58af4a7…  OK MANPAGE.md 456ee62c…  OK 0 4225074e…
$ git ls-tree --name-only HEAD .ufo/waves/round-28/misroot-lane-root/ .ufo/waves/round-38/misroot-lane-root/
… eight files, all tracked …
```

`ls -a` at the lane root lists no `--repo/` (the untracked empty directory is gone; `d3-relocation.txt:9` records
`rmdir`). `LOG.md` has no round-54 section — `grep -n "^## " LOG.md | tail -5` ends `2841:## Round 53 …`, and
`LOG.md` is not among the working-tree modifications — so the contract's "with a LOG entry" half of the D3 fix is not
in the tree at this read.

### M3 — the tracepoint's first candidate

```
$ sha256sum <l1 fetch> /…/mori-r54/l1/src/include_ras_ras_event.h.v7.3   corpus/evidence/sources-r54/memory-failure-trace.h.v7.3
408ddc2ac2a5f17282ecd4cecc6b3727d1e4f46e2f0855a26f2e27073026802b  …ras_event.h.v7.3   (11341 B)
a395e62b36ace3d1295fd3e9e469fc525f67c7787f529a380633d6b800f051ea  …memory-failure-trace.h.v7.3   (2964 B)
$ grep -c "TRACE_EVENT(memory_failure_event" <both>
…ras_event.h.v7.3:0      …memory-failure-trace.h.v7.3:1
$ grep -c "memory_failure" …ras_event.h.v7.3        → 0
$ grep -c "TRACE_SYSTEM ras" …ras_event.h.v7.3      → 1
$ grep -c 'For historical versions' …ras_event.h.v7.3 → 0   ; …trace.h.v7.3 → 1
$ grep -c 'TP_printk("pfn' …ras_event.h.v7.3 → 0            ; …trace.h.v7.3 → 1
```

`gate-rejects.txt:3-6` (L1, 2026-10-27 01:2x, pre-freeze) records the same fetch and the same `0` / `1` counts, plus
`memory-failure.c.v7.3:66:#include <trace/events/memory-failure.h>`. The shipped copy's `:7` is `#define TRACE_SYSTEM
ras` and `:74` is `TRACE_EVENT(memory_failure_event,` (S524's anchor says `74-98`; `grep -n` → `74:`).
`corpus/SOURCES.md:303` is S524; `count-c2.py:68` pins the sha256 `a395e62b…`;
`evidence/c2-claims.txt:75-78` are rows 19/20, both `source=S524`.

`include/ras/ras_event.h` is *identical* at v7.2 and v7.3 — the v7.2 fetch in `w1/Mo54ExecMfV72.md:29-30` gives the
same `11341` bytes and `408ddc2ac2a5f172…`, 0 `memory_failure` matches — so the wrong pick was stale path memory, not
a v7.3 change. This seat's one probe of the alternative historical home:

```
$ curl -fsS -o trace-events-ras.h.v7.3 "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/trace/events/ras.h?h=v7.3"
curl: (22) The requested URL returned error: 404        exit=22
```

v7.2 not checked; `[INFERENCE]` the brief's "moved to" wording — the observed fact is where the event lives at
v7.2/v7.3.

`gate-rejects.txt` is untracked (`git status --porcelain` → `?? .ufo/waves/round-54/evidence/gate-rejects.txt`) and is
not in the freeze commit (`git ls-tree 6830f3af .ufo/waves/round-54/evidence/` lists no such file).

## Draft — lesson `## Mistakes` (fenced; paste as-is, L1 integrates)

```markdown
## Mistakes

- M1: receipt-revision — the round-53 claim rows name the *salvage* revision's receipt while their numbers are the
  *landed* revision's. `SCORECARD.md:2796` (C1 After cell) ends `… dissent=0`, rc 0 — `evidence/c1-at-salvage.txt`
  (R = `0df80303`; the at-landed re-run is named in the round-53 report)`, and `:2797` (C2) names
  `evidence/c2-at-salvage.txt` (R = `0df80303`) with `evidence/c2-at-data.txt` as its aside; the landed receipts
  `<round-53>/evidence/c1-at-landed.txt` and `c2-at-landed.txt` (R = `0b36d23e`) exist beside them. No number was
  wrong: with `rev=` removed the `C1=`/`C2=` lines of the salvage and landed receipts are byte-equal (`cmp` silent for
  both counters), so QUALITY 146's digit arm had nothing to fire on. Evidence: those two rows,
  `corpus/lessons/round-53-verifier-spotcheck.md` §Conformance defects D2, and the two pairs of receipts; the same
  defect stands on two round-50 rows (`SCORECARD.md:2668-2669`, `a2-c{1,2}-at-data.txt` beside `*-at-landed.txt`).
  Captured-by: none — QUALITY 146 compares a row's digits with the receipt the row names, and both receipts print the
  same digits, so naming the wrong revision is invisible to it; the non-author closure found it by reading. Fix:
  `QUALITY 148` and its instrument `python3 .ufo/waves/round-54/checks/receipt-stage.py <rev>`, which flags a claim
  row whose After cell cites `evidence/<x>-at-data.txt` or `<x>-at-salvage.txt` while `<x>-at-landed.txt` exists in
  that round's evidence directory and no later `**Round-N correction:**` paragraph names it; the corrections are
  appended, never a rewrite (`SCORECARD.md:2850`, `:2858`). Shown able to fail: `RECEIPT_STAGE rev=39dcf4d7
  cited_intermediate=5 flagged=5`, exit 1 (`.ufo/waves/round-54/evidence/receipt-stage-before.txt`; re-run by the
  round-54 scribe at `39dcf4d7` and at `2d0347a3`, same five FLAG lines), and `cited_intermediate=5 flagged=0`, exit
  0, over a fixture carrying the working-tree `SCORECARD.md` with the four landed receipts (round-54 scribe, fixture
  commit `e34deaf7`). Not covered: a correction paragraph satisfies the check by name, not by content, so the cell
  still cites the intermediate receipt; rows before the `-at-landed` naming (rounds ≤ 49) are out of reach; and the
  passing direction is only readable from a revision that carries the corrections — at this round's write the
  corrections were a working-tree edit, so the criterion's `flagged=0` had no receipt in
  `.ufo/waves/round-54/evidence/` until integration committed them.

- M2: stale-strays — the misroot sweeps' own output sat at the lane root for 26 round numbers. Seven files (`base.c`,
  `main.c`, `meminfo.c`, `oom_kill.c`, `sd-main.c`, `user@.service.in`, `MANPAGE.md`) were added by round 28's commit
  `763d3469` (2026-10-22 15:06:33 -03) and stayed at the lane root through round 53; the eighth, `0`, was added by
  round 38's `96f7f97e` (2026-10-23 23:47:54 -03) and stayed from round 38. They were tracked, diffable files that
  belong to no lane purpose — a reader listing the lane saw eight C sources, a systemd unit template and a man page
  at the top level — and the empty untracked `--repo/` directory the same sweep left stood beside them.
  Evidence: `corpus/lessons/round-53-verifier-spotcheck.md` D3; `.ufo/waves/round-54/evidence/d3-relocation.txt`;
  `git ls-tree --name-only 39dcf4d7` lists all eight, `git ls-tree --name-only 1116c092` lists none;
  `git log --diff-filter=AD -- base.c` and `-- 0` give the add and delete commits. Captured-by: none — QUALITY 43
  scopes a misroot sweep to the fleet root and no criterion reads the lane root, so a stray that the sweep itself
  carried survived 26 rounds of integration; the round-53 non-author closure found them by listing the root. Fix:
  byte-exact relocation under the wave directory of the round that swept them
  (`.ufo/waves/round-28/misroot-lane-root/`, `.ufo/waves/round-38/misroot-lane-root/`) at `1116c092`, `rmdir` of the
  empty `--repo/`, and `QUALITY 149` (a lane-root listing holds only the lane's own entries). Shown able to fail: the
  same listing prints `0 MANPAGE.md base.c main.c meminfo.c oom_kill.c sd-main.c user@.service.in` at `39dcf4d7` and
  none of them at `1116c092`/HEAD, and all eight relocations are byte-identical (`git rev-parse` of each blob at both
  ends: 8/8 equal, round-54 scribe). Not covered: the allowed set is one round's list and must be amended when the
  lane adds a root file on purpose; a misroot deeper in the tree is not caught; and the routed fix also asked for a
  LOG entry, which was not in the tree at this write (`LOG.md`'s last heading is `## Round 53`, `:2841`) — open.

- M3: wrong-file — the `ras:memory_failure_event` tracepoint was first looked for in `include/ras/ras_event.h`, which
  does not define it. At v7.3 that path is 11341 B, sha256
  `408ddc2ac2a5f17282ecd4cecc6b3727d1e4f46e2f0855a26f2e27073026802b`, with 0 occurrences of `memory_failure` and 0 of
  `TRACE_EVENT(memory_failure_event`; the event is in `include/trace/events/memory-failure.h` (2964 B, sha256
  `a395e62b…`), `TRACE_EVENT(memory_failure_event` at `:74-98`, `#define TRACE_SYSTEM ras` at `:7`, included by
  `mm/memory-failure.c.v7.3:66`. Evidence: `.ufo/waves/round-54/evidence/gate-rejects.txt:3-6` (the pre-freeze fetch
  and `grep -c`, 2026-10-27 01:2x), `corpus/SOURCES.md:303` (S524), `count-c2.py:68` (the sha256 pin),
  `.ufo/waves/round-54/evidence/c2-claims.txt:75-78` (rows 19/20). The pick was not a v7.3 change:
  `include/ras/ras_event.h` is byte-identical at v7.2 and v7.3 (v7.2 fetch in `w1/Mo54ExecMfV72.md:29-30`, same
  11341 B and sha256, 0 `memory_failure` matches), so what failed was memory of a pre-v7.2 home, not the release.
  Captured-by: 128 — the C2 location arm would have failed this pick for these two rows, whose quotes occur 0 times
  in `ras_event.h` and once each in the shipped copy; but the arm proves location only, so a row quoting text both
  files carry (`TRACE_SYSTEM ras`, 1 in each) would pass against the wrong file, and what actually caught it was the
  author's own `grep -c "TRACE_EVENT(memory_failure_event"` before the freeze. Fix: S524 pins the trace/events path
  with its sha256 and its anchor names `TRACE_EVENT(memory_failure_event) 74-98`, and both S524 rows locate in that
  copy. Shown able to fail: the counts above (0 against `ras_event.h`, 1 plus both row quotes in the shipped copy) —
  a row certified against `ras_event.h` reads `quote_missing`. Not covered: no check reads a new source row's *path*
  against the symbol it is cited for; only quoted text is located.
```

## Notes for the L1 integration

- The draft cites two still-uncommitted artefacts by line (`SCORECARD.md:2850`, `:2858`; `QUALITY 148`/`149`; the
  `checks/receipt-stage.py` instrument). If integration reflows `SCORECARD.md` before the lesson lands, the two cell
  references `:2796` and `:2797` are the stable ones (they were committed in round 53); the correction line numbers
  are not.
- The draft's "26 round numbers" is the round-number span 28–53; only the seven round-28 files span it. The eighth
  (`0`) spans 38–53 (16 round numbers) — stated separately in M2 rather than folded into the "26".
- M1's class is deliberately not round 53's M1 class: round 53's M1 was digit drift against a wrongly named receipt
  (QUALITY 146); this one is correct digits with the wrong revision (QUALITY 148). Both classes are the same failure
  in a scorecard row: an author citing a receipt other than the one the round landed.
- `receipt-stage.py` reads `git show <rev>:SCORECARD.md`, so the criterion's green direction cannot be produced from
  a revision until the corrections are committed; if the L1 wants that reading receipted, run it after the SCORECARD
  correction lands and save `receipt-stage-after.txt` beside the `-before` one.

## Out of scope (not touched)

No edit to `corpus/lessons/`, `SCORECARD.md`, `QUALITY.md`, `LOG.md`, `SKILL.md`, `PROVINCE.md`, `corpus/`, `tools/`,
`considerthese/`, or any file under `.ufo/waves/round-54/` other than this report. No counter, control, selftest or
vote run; no `RECHECK`/`ENTAIL` measurement. No host write, no sysctl, no cgroup, no module, no `systemctl`; no
pacman transaction; no tool installed, so no tool record. Read-only git only (`ls-tree`, `log`, `rev-parse`,
`show`, `cat-file`, `status`, `diff --stat`). Scratch
`/fast/scratch/hyaku/mori-r54/Mo54ScribeMistakes/` (fixture repo `e34deaf7`, `TMPDIR` under it) was removed before
this report was written; the fixture's SCORECARD is the lane's working-tree copy, cited above, not evidence of a
committed state. One network fetch (`include/trace/events/ras.h?h=v7.3`, HTTP 404); the `ras_event.h` bytes read are
the L1's own fetch in the lane scratch, hashed here.

## Findings

- MED — `LOG.md`: no round-54 section (last heading `## Round 53` at `LOG.md:2841`; `LOG.md` not in
  `git status --porcelain`), so the D3 relocation landed at `1116c092` without the LOG entry the contract's routed fix
  names. The M2 draft records this as an open half of the fix.
- MED — `corpus/QUALITY.md:1479` (`QUALITY 148`): the criterion's `flagged=0` "after this round's appended
  corrections" reading has no receipt (no `receipt-stage-after.txt` in `.ufo/waves/round-54/evidence/`) and cannot be
  produced from any committed revision, because the correction paragraphs were a working-tree edit (`SCORECARD.md`
  +15, uncommitted) at this read. The failing direction is receipted and was reproduced twice
  (`flagged=5`, exit 1 at `39dcf4d7` and at `2d0347a3`).
- LOW — `.ufo/waves/round-54/evidence/gate-rejects.txt`: untracked and absent from the freeze commit `6830f3af`, and
  it is M3's only written evidence; if integration drops it, M3's wrong-file pick rests on the L1's word.
- LOW — `corpus/QUALITY.md:1492` (`QUALITY 149`) / brief wording "eight … for 26 rounds": the 26-round span holds for
  the seven round-28 files; `0` was added at round 38 (`96f7f97e`, 2026-10-23 23:47:54 -03) and spans 16 round
  numbers. The M2 draft states both.
- LOW — `corpus/QUALITY.md:1479,1492` cite `lessons/round-54.md#M1`/`#M2` and `corpus/lessons/round-54.md` does not
  exist yet; this draft supplies those anchors and assumes the order M1, M2, M3 (a re-order at integration breaks the
  two criteria's pointers).
- LOW — the M3 premise "moved to `include/trace/events/memory-failure.h`": `include/ras/ras_event.h` is byte-identical
  at v7.2 and v7.3 with zero `memory_failure` mentions, so the observed fact is the event's location at those tags, not
  a move at v7.3; the second candidate path this seat probed, `include/trace/events/ras.h?h=v7.3`, answers HTTP 404.
  M3's draft is worded to the observed bytes.
