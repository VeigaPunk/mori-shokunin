# Mo56ScribeConsiderthese — one still-unimplemented proposal, drafted as a QUALITY criterion

Seat: leaf scribe, round 56 wave w1. Mode: read-only mining of
`considerthese/2026-10-26.md` plus one clone at the freeze tip; no product code, counter,
contract or lane file is edited. This seat ran no vote item (the wave carries none).

Report path (relative to the lane root): `.ufo/waves/round-56/w1/Mo56ScribeConsiderthese.md`.

Scratch: `/fast/scratch/hyaku/mori-r56/Mo56ScribeConsiderthese/` (`tmp/` as `TMPDIR`, one
`git clone --shared` named `r56c1` checked out at `8be2717b0809281d07dffe83dad424a4859e0747`);
removed at the end of the seat. No tool install, no pacman, no network fetch.

## 1. Which of the four suggestions still qualify

Read at the freeze tip `8be2717b0809281d07dffe83dad424a4859e0747` in `r56c1`.

| # | Suggestion | Status observed | Evidence |
|---|---|---|---|
| 1 | split pin-check mismatches into "can't run here" vs "stale" | **implemented** | `corpus/QUALITY.md:1285-1300` (criterion 138, whose Lesson names `considerthese/2026-10-26.md` suggestion 1); `tools/mori-pin-check.py:140-141` states every mismatch line carries `class=env` or `class=stale`, and the selftest at this rev prints `PIN_CHECK_SELFTEST pass=125 fail=0` (rc 0) with `class=env`/`class=stale` arms at `:1494` and `:1524` |
| 2 | follow the unfixed critic flags forward | **not implemented** | see §2 |
| 3 | re-execute what closures only evidence-verified | **implemented** | `corpus/QUALITY.md:1219-1230` (criterion 136), round-50 re-execution receipts `evidence/a2-c1-at-data.txt`, `evidence/a2-c2-at-data.txt` |
| 4 | keep a suggestion-adoption status line | not picked (see below) | the per-round lessons already state each suggestion's disposition one by one — `corpus/lessons/round-49.md:211`, `corpus/lessons/round-55.md:106` — so a separate status line adds a prose habit with no committed artifact a check could diff |

Suggestion 4 is a reporting habit, not a measurement: any check would reduce to "the lesson
mentions the four suggestions", which the two cited lessons already satisfy. Suggestion 2, by
contrast, has committed artifacts (an id-keyed defect list and a landable diff) and no
existing reader of them.

## 2. Suggestion 2, grounded in the tool's actual behavior

The counting half exists and is single-round by construction:

```
$ cd r56c1 && python3 .ufo/waves/round-49/flagged-fixed/count-flagged.py | tail -3
report RevPromptHonesty.md fixed=1 unfixed=1 na=2
flagged=45 fixed=18 unfixed=9
na=18
rc=0
```

Its scope is frozen in the source, not in an argument:

```
$ grep -n "^FREEZE\|^LANDING\|add_argument" .ufo/waves/round-49/flagged-fixed/count-flagged.py
45:FREEZE = "4387cf94b69ddce455051a1ff38e93795c2e6cde"
46:LANDING = "e4dfff32d4f97c7ef250e9a7538fa75d4f284492"
58:    ap.add_argument("--defects", default=os.path.join(here, "defects.jsonl"))
59:    ap.add_argument("--repo", default=repo_default)
60:    ap.add_argument("--freeze", default=FREEZE)
61:    ap.add_argument("--landing", default=LANDING)
```

So the tool decides round 48's 45 rows against the round-48 freeze→landing diff; nothing in
the tool, the ledger directory or the lessons reads a *previous* round's UNFIXED set against a
*later* landing. The capability was recorded as such and then never carried:
`corpus/lessons/round-49.md:159` states the tally, `:211` records the capability, and
`corpus/lessons/round-55.md:106` still calls the "carry-over-flag ledger" outstanding.

The nine UNFIXED ids and their later mention count (bare id, all revisions after the round-49
landing, excluding the round-49 ledger tree itself):

```
$ ids=$(python3 .ufo/waves/round-49/flagged-fixed/count-flagged.py | awk '/verdict=UNFIXED/{print $1}')
$ for id in $ids; do printf '%s later=%s\n' "$id" \
    "$(git grep -F -- "$id" 8be2717b -- corpus/lessons .ufo/waves \
        ':!.ufo/waves/round-49/' ':!.ufo/waves/round-17/' | wc -l)"; done
C1-F1 later=0
C1-F6 later=0
C1-F8 later=0
C2-F1 later=0
JC-D7 later=0
V3-J10 later=0
V3-J11 later=0
RA-F2 later=0
RH-F2 later=0
rc=0
```

Rounds 49 through 56 landed after that tally and none of them names a single one of the nine.
Two of them look answered in practice without a flag-level line — round 48 `C1-F1`
(variant-name leak) by round 49's opaque-handle counter, and `RH-F2` (census receipt without an
exit code) by QUALITY 152 — which is exactly the substitution a carry-over ledger has to name
rather than leave to a reader's memory.

## 3. Draft criterion (fenced; for the L1 to place and number)

```markdown
153. **An unfixed critic flag is carried by round-qualified id into the next round's ledger,
    and its disposition is decided against that round's landing.** Lesson:
    `considerthese/2026-10-26.md` suggestion 2 (operator reflection, opened 2026-10-26);
    `corpus/lessons/round-49.md:159` records the snapshot (round 48
    `flagged=45 fixed=18 unfixed=9 na=18`) and `:211` the capability;
    `corpus/lessons/round-55.md:106` still lists the "carry-over-flag ledger" as outstanding.
    Rationale: `.ufo/waves/round-49/flagged-fixed/count-flagged.py` hardcodes its freeze and
    landing (`:45-46`) and reads one `defects.jsonl` (`:58-61`), so it decides one round's rows
    against one diff; the nine UNFIXED rows it prints for round 48 are named nowhere in rounds
    49-56, and the only landing that closes two of them (round 48 `C1-F1` by round 49's
    opaque-handle counter, `RH-F2` by QUALITY 152) does so under a different artifact, so an
    id-keyed ledger is the only place a reader can see that. Check: in the lane,
    `ids=$(python3 .ufo/waves/round-49/flagged-fixed/count-flagged.py |
    awk '/verdict=UNFIXED/{print $1}')` then for each id
    `git grep -F -- "$id" <next-round-tip> -- corpus/lessons .ufo/waves
    ':!.ufo/waves/round-49/' ':!.ufo/waves/round-17/'` must match at least one line that also
    carries `fixed`, `routed` or `dropped` and the round that decided it; at
    `8be2717b` every id prints `later=0`. Shown able to fail: the nine `later=0` lines above
    (exit 0 from the loop, and `git grep` itself exiting 1 with no output) are the unmet arm,
    and the bare-id control is worse than useless without the round directory in the key —
    `C2-F1` matches 134 lines, all from `.ufo/waves/round-17/falsify/CriticC2Final.md`, a
    different defect that reuses the id, so an unscoped grep would score a false fix. The pass
    arm is a fixture repo (`mktemp -d`, commits under a fixture identity, `rev-parse
    --show-toplevel` asserted first) whose `corpus/lessons/round-50.md` carries
    `C1-F1 routed to round 57 (successor counter counts cels).`: the same
    `git grep -c -F -- C1-F1 HEAD -- corpus/lessons` prints `1`, and for an id the file does
    not carry it prints nothing and exits 1. Not covered: the grep proves a later committed
    line names the id and a disposition word, not that the disposition is true; it reads
    `corpus/lessons` and `.ufo/waves` only, so a disposition written in `LOG.md` or
    `SCORECARD.md` is invisible to it; flags closed by a substitute artifact with no flag-level
    line still need a hand-written successor clause (round 48 `C1-F1`, `RH-F2` would otherwise
    score "dropped"); per-round ids are not globally unique (round 17 and round 48 both have a
    `C2-F1`), so the round directory is part of the key and an id-only ledger is rejected; and
    the id list is the round-49 ledger's, so each new round needs its own extraction before the
    command means anything.
```

Placement note for the L1: criterion numbering starts at 153 (`corpus/QUALITY.md` ends at 152,
line 1520), and the draft follows the three-part shape the file uses at 136 and 138 (Rationale
/ Check / Shown able to fail / Not covered).

## 4. Observations on the frozen claims (this seat is not a judge)

- The seal and provenance of the two frozen claims is the verifier's business; this seat ran
  neither `count-c1.py` nor `count-c2.py` and asserts nothing about them.
- Nothing in this report proposes a change to a frozen counter, predicate, control or kill
  rule. Suggestion 2 is a criterion for *future* rounds; if the L1 adopts it, the natural
  carrier is a new per-round extractor beside the round-49 one, not an edit to it, because
  `count-flagged.py`'s default revisions are the round-48 pair.

## 5. Verification actually exercised

| Command (in `r56c1` at `8be2717b`) | Output | rc |
|---|---|---|
| `python3 .ufo/waves/round-49/flagged-fixed/count-flagged.py` | `flagged=45 fixed=18 unfixed=9` / `na=18` | 0 |
| `python3 tools/mori-pin-check.py --selftest` | `PIN_CHECK_SELFTEST pass=125 fail=0` | 0 |
| nine-id `git grep` loop (§2) | nine `later=0` lines | 0 (loop); `git grep` exits 1 per empty id |
| fixture pass arm (§3) | `hits=HEAD:corpus/lessons/round-50.md:1`; miss id rc 1 | 0 / 1 |

Not exercised: any host read (`/proc`, journal, watchdog log), any counter of this round, any
mutation outside the fixture repo and the removed scratch tree.

## Findings

1. **MED** — `.ufo/waves/round-49/flagged-fixed/count-flagged.py:45-46` freezes `FREEZE` and
   `LANDING` to the round-48 pair and `:58-61` reads one `defects.jsonl`, so the lane has no
   reader that decides a *previous* round's UNFIXED flags against a *later* landing. The nine
   round-48 UNFIXED ids (`C1-F1`, `C1-F6`, `C1-F8`, `C2-F1`, `JC-D7`, `V3-J10`, `V3-J11`,
   `RA-F2`, `RH-F2`) are named in no committed file after round 49; `corpus/lessons/round-55.md:106`
   still calls the carry-over-flag ledger outstanding.
2. **LOW** — flag ids are not globally unique across rounds: `.ufo/waves/round-17/falsify/CriticC2Final.md`
   carries its own `C2-F1`, which an unscoped bare-id grep counts 134 times. Any future
   carry-over check must key on round + id, and the draft in §3 states that.
3. **LOW** — two round-48 UNFIXED rows are answered in practice without a flag-level line
   (`C1-F1` by round 49's opaque-handle counter; `RH-F2` by QUALITY 152's exit-code rule), so a
   strict id-only ledger would read them as dropped on its first run; the criterion's successor
   clause exists for that case, and it is a hand-written disposition, not something the check
   derives.
4. **LOW** — suggestions 1 and 3 of `considerthese/2026-10-26.md` are already landed as
   QUALITY 138 and 136 and are therefore not available as this round's pick; suggestion 4 has
   no committed artifact to check beyond prose the lessons already carry.

Report: `.ufo/waves/round-56/w1/Mo56ScribeConsiderthese.md`
