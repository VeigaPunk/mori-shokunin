# CriticC1Admission — round 26 wave 2, attack on C1 admission

Seat: MoriR26.CriticC1Admission (critic, leaf). Date 2026-10-22. Lane tip under attack
`16935e24c93fa7e7567413d7ec091339a5df1474`, read with git only. The only lane write is this file.
Sandbox: `/fast/scratch/hyaku/mori-r26/CriticC1Admission/sb` (a `git clone --no-hardlinks` of the
lane; the variant commit exists only there). Tools installed or upgraded: none. No upstream source
opened. No journal `MESSAGE` text read or copied; the host read below is unit states and versions only.

## Verdict a non-author closure would most likely reach

**C1 admits as `improved`, bounded.** Three caveats go on the record:

1. The **counter is narrower than the statement**. This is a low-severity defect: it does not
   inflate the value at the real bytes, but the closure has to re-derive the uncounted clauses by
   hand.
2. The **quality trend is at risk** from stale `systemd 261` lines in another admitted entry. They
   were found this round and named only as debt in SCORECARD; the entry itself is still unmarked.
   This does not touch C1's counted value, but it can stop LEARNING `quality: improved` (moderate).
3. Whether **freshness moves from 5 to 6** is the closure's decision. The SCORECARD row holds it at
   5 pending closure, which is honest.

**A1 timing holds.** A1 landed before any committed C1 after-state.

## Findings

### F1 — A1 landed before any C1 after-measurement (attacks contract.md:127, A1 header). **Holds.**

- A1 commit: `99338de` at `2026-10-22 10:21:07 -0300`. It adds `count-c1.sh` and the A1 text
  (`git show --stat 99338de`). The first C1 content commit is `327fbcc` at `10:39:06 -0300`
  (`git log --format='%h %ad' 248408f..16935e2`).
- `git diff --stat 99338de 16935e2 -- .ufo/waves/round-26/count-c1.sh` is empty, so the counter has
  not changed since A1.
- I ran the A1 counter at every lane commit from the entering tip forward:
  - `248408f`, `28b0494`, `5e5e86f`, `5b10649`, `c2fdd92`, `99338de`, `278f02e`, `825f988`,
    `b4473ed`, `5854050`, `93aa1b9`, `738eec1` and `21386b9` all print
    `stale_present=4 r26_entry=absent r26_new_source_ids=0 r12_names_r26=0`.
  - `327fbcc`, `4dba9cc`, `c6ea248`, `2ecb661` and `16935e2` all print
    `stale_present=0 r26_entry=present r26_new_source_ids=13 r12_names_r26=4`.
  - `deadbeef` prints `bad_rev` and exits 2.
- So no committed revision showed an after-state when A1 landed.
- Caveats, not defects:
  - The planned rewrite text already existed as a draft before A1. `w1/DraftR12Corrections.md`
    has mtime 10:17:49, and its line 237 states the after requirement; it is not a measurement.
    `w1/CriticC1Width.md:34-40` ran sandbox variants with the pre-A1 command, not the lane.
    [INFERENCE] The mtimes are working-tree times, not commit times.
  - A1 only tightens. It adds two predicates, exits 2 on a bad revision or a missing file, and
    folds whitespace and emphasis, which can only raise the stale count
    (`count-c1.sh:4,8,9,11,14-15`). So knowing the draft could not have inflated the target.
  - A1 discloses its timing for C2 (contract.md:144-146) but says nothing about the C1 drafts
    existing. That is a minor disclosure gap.

### F2 — The statement is wider than the counter (attacks contract.md:21-24, 43-44 against count-c1.sh). **Defect (low).**

| Statement clause | What the A1 counter checks | Gap |
|---|---|---|
| The four phrases "contradict the committed round-26 capture" | nothing | The capture is never read |
| The r26 `source:` cites ≥1 SOURCES row "opened in round 26" | `count-c1.sh:14`: S-ids greater than 113 on the first `source:` line | Never checks that the row exists in `corpus/SOURCES.md` |
| The stale lines are rewritten "as dated past-tense records that name the superseding entry" | `count-c1.sh:15`: the number of r12 lines naming `userspace-oom-killers-r26.md` | README F4 is not checked; dating and tense are not checked; a paraphrase passes |

**Counterexample, run in the sandbox (`stub` commit `2d8968e`, on top of `248408f5`):**

- The four phrases are paraphrased with their meaning kept: "neither service is active", ASCII
  `->`, "Neither service unit is active", "not running on this host".
- r12 gains one line naming `userspace-oom-killers-r26.md`.
- r26 is a two-line stub: `source: S999` and `verified-at: never`.
- I ran `count-c1.sh` with only `L=` repointed to the sandbox (the diff shows line 3 only). It
  printed `stale_present=0 r26_entry=present r26_new_source_ids=1 r12_names_r26=1` and exit 0.
  That meets every A1 after-value.
- `git grep -c S999 stub -- corpus/SOURCES.md` finds no row.
- This is the same hole `w1/CriticC1Width.md:35` (P4–P6) reported before A1. A1 cites only
  CriticLearningRules (contract.md:129) and did not close it.

**The real tip does not exploit the gap. I checked each clause by hand:**

- **Sources.** SOURCES has 13 rows S114–S126 at `16935e2` and 0 at `248408f`, whose last row is
  S113 (`git show <rev>:corpus/SOURCES.md | rg '^\| S1(1[4-9]|2[0-6]) '`). The r26 `source:`
  line names S114–S126 with URLs, sha256 values and "opened 2026-10-22"
  (`userspace-oom-killers-r26.md:1`).
- **Capture.** `.ufo/waves/round-26/capture/capture.txt:10-13` (committed in `b4473ed`) reads
  earlyoom active/enabled and systemd-oomd inactive/disabled. That contradicts the old phrases.
- **Rewrites.** `userspace-oom-killers-r12.md:6,14,18` and `corpus/README.md:34` are now dated
  2026-10-19 and 2026-10-22 records in past tense, and each names `userspace-oom-killers-r26.md`.

Smallest safe correction: the closure records the three hand checks above as its re-derivation of
the uncounted clauses. Optionally, a future counter looks up each S-id in `$R:corpus/SOURCES.md`,
requires it to be absent at `248408f5`, and checks README for the r26 path. The counted value does
not change either way.

### F3 — Do four phrase removals plus a new entry earn freshness `improved`? **Holds, bounded.**

AXES.md:14 defines freshness as "skill claims re-verified against live surfaces; stale items
flagged or fixed".

- **Re-verified against live surfaces.**
  - The r26 entry records a host capture and upstream bytes pinned at tags v1.9.0 and v262 with
    sha256 values (`userspace-oom-killers-r26.md:1-3,28-42`).
  - My own read-only check today: `systemctl is-active earlyoom.service systemd-oomd.service`
    gives `active`, `inactive`. `is-enabled` gives `enabled`, `disabled`.
    `pacman -Q earlyoom systemd` gives `earlyoom 1.9.0-1`, `systemd 262-1`. `uname -r` gives
    `7.2.11-arch1-1`.
  - All of these match r26 F1 (`:28-33`), so the entry passes its own recheck now.
- **Stale items fixed.** The four frozen items, plus the uncounted r12 lines 3 and 6 (SCORECARD
  round-26 "Uncounted, same change"), are fixed in place. They are not shadowed by a banner.
- **Stale items flagged.** The three r14 lines are flagged in SCORECARD (line 1613 of the tip
  file), not fixed. See F4.
- **LOG signal.** The AXES.md:14 signal is that each round's LOG entry includes a re-verification
  result. LOG.md:1820-1829 (the declaration) carries the 2026-10-22 read-only re-check. No
  outcome LOG entry exists yet at the tip; I treat that as closure-time work, not a defect.
- **Width.** The counted move is small: four phrases in one ground. The SCORECARD row says so: it
  is "bounded to the four frozen phrases plus the superseding entry; freshness 5 → 5 held pending
  closure".
- [INFERENCE] A non-author would accept `improved` but would likely not raise the score past 6 on
  this evidence alone. The round's own sweep found more stale lines than C1 fixed.

### F4 — Does LEARNING `quality: improved` ("a weaker entry superseded by a stronger one") hold? **Holds for the r12→r26 pair; at risk overall. Defect (moderate) against the trend, not against C1.**

**The supersession holds.**

- r12's host-state ground was one `systemctl` reading (`r12:14`) under sources at v261 and
  upstream master (`r12:1-3`).
- r26 adds 13 new rows (12 tier A, 1 tier B; SOURCES S114–S126) pinned at tags with sha256
  values, tags each fact as `verified`, `scoped` or `[INFERENCE]`, and carries a full recheck
  (`r26:1-3,22-24`).
- r12 now names r26 as "the superseding host-state record" (`r12:6,18`).
- The supersession is **partial**: r12 still holds the oomd mechanism claims (`r12:11-13`). The
  closure should write "superseded on host state", not "superseded".

**The counterexample to `improved`.** LEARNING.md:34 has two conditions that bite:

- `improved` needs "no admitted entry failing its re-check".
- `harmed` applies when "an entry is found false or stale and left unmarked".

Wave-1 ScoutStaleSweep (`w1/ScoutStaleSweep.md:75-77`) re-checked
`corpus/knowledge/journal-alarm-routing-r14.md`:

- `:342` says "host systemd is 261", in plain present tense.
- `:67-68` and `:290` also name host systemd 261.
- The live host runs `systemd 262-1` (command above).

At the tip these lines are unchanged (`git show 16935e2:…r14.md`, lines 67-68, 290, 342). They are
named only as "named debt" in SCORECARD (tip file line 1613). No in-entry mark exists:
`git grep journal-alarm-routing-r14 16935e2` shows no round-26 hit outside SCORECARD.

By the round's own rule this is stale. r12 also carried a dated `verified-at` header (`r12:2`), and
the contract still counted its present-tense lines as stale (contract.md:21-24).

Impact on C1: none. Other entries are explicitly unclaimed (contract.md:46), and the freshness axis
is not harmed: r14 was equally stale at entry and is now at least flagged. The impact is on the
trend. A strict closure could read `quality: unchanged` instead of `improved`, or call the unmarked
r14 lines `harmed`.

Smallest safe correction: add three dated, past-tense correction lines in r14 at `:67-68,290,342`
(the r16 style that `w1/ScoutStaleSweep.md:148` proposed), naming systemd 262-1 on 2026-10-22.
This is an uncounted hygiene change, under 10 lines. It clears both LEARNING conditions without
touching C1's counted value.

### F5 — Do the SCORECARD round-26 rows overstate C1? **Holds.**

- The tip SCORECARD measured-outcome row for C1 quotes the A1 counter values at `327fbcca`. I
  reproduced them, and the same values hold at `16935e2`.
- The declaration row (tip SCORECARD line 1597) still shows the pre-A1 contract command and
  after-values. That is historical, and A1 supersedes it (contract.md:134-138).
- Nothing in the C1 rows claims a host census, kill history or other entries.

## Impacted axes

| Axis or trend | Assessment |
|---|---|
| freshness (C1) | Verifies `improved`, bounded |
| calibration | Counter weaker than statement (F2), plus a minor A1 C1-draft disclosure gap (F1) |
| LEARNING quality trend | At risk from unmarked r14 lines (F4) |

## Not run

- I did not check C2.
- I did not review the r26 facts F2–F11 against upstream bytes; other seats own those.
- I did not run a retention scan.
