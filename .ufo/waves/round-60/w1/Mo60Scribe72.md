# Mo60Scribe72 — draft row S564 for Mo59Sentinel58 (round 60, w1)

Seat: scribe, leaf. Work mode: read-only on the lane (no production/corpus/SCORECARD/LOG edits, no
lane VCS mutation, no fleet/sibling writes, no subagents, no installs). Lane HEAD during the seat:
`b3c256138f00c704d5aa56eb0332d74506502ef2`. Pins:

| file | sha256 |
|---|---|
| `corpus/SOURCES.md` (worktree = HEAD blob) | `e8bda4a85241e9cf2ae719afa790e1b2b61da5fb7ec36568335d8c618add9441` |
| `corpus/lessons/round-60.md` at HEAD (quoted) | `ca3f1e10cbb8d4b9673097a568eab762ea5e863255b434ae0a3e0777a2264b78` |
| `corpus/lessons/round-60.md` worktree (after a sibling's mid-seat edit) | `ebabff297c97eadcf55767e98ec44b2fb13401a6bd02022b80f37227bfa00780` |
| `corpus/knowledge/entry-claims-hardening-r60.md` | `6aa1b604217e50ec1055f69703976b33fc4ef49261bf441a5b130ee93195924f` |
| `.ufo/waves/round-59/w1/Mo59Sentinel58.md` | `b4d32a26d8be68d59ba995a9e5804c34e41bcad0e1841c404c7e288c45f94157` |
| `.ufo/waves/round-59/w1/Mo59Sentinel57.md` | `2e7a0cbb2a77f1a91927c3b8ec0e229292bad7c33cefff01bfbaac2cd424e326` |

`git status --porcelain` at seat start showed only this wave's untracked files (`w1/`, `w1.ready*`,
`evidence/c1-at-data.txt`); `corpus/SOURCES.md` and the knowledge entry are still clean against
HEAD. Mid-seat, `corpus/lessons/round-60.md` moved in the worktree (adds the absent-set reading note
at :65-71, credited to Mo60Reviewer03); `diff` of the quoted Gate block (:33-37) between the HEAD
blob and the worktree is empty, so the quote below is byte-stable across that move. The file is not
mine and was not touched by this seat.

## Deliverable 1 — the exact row

The row is already landed in the Registry table (`corpus/SOURCES.md:344`, 11 cells, `NF=13`).
My draft is byte-identical to it (I did not edit the file):

```
| S564 | mori round-59 w1 sentinel report Mo59Sentinel58 — tool-bytes execution gate review | own-work | B | same execution-gate scope as S562 | report `.ufo/waves/round-59/w1/Mo59Sentinel58.md` F1 | REJECTED: duplicate scope of S562 (same F1 execution-gate finding, no additional construction used this round); flip: a future round needing Sentinel58's distinct expect-tamper construction (F2) re-opens the row | rejected | 2026-10-28 | 180d | corpus/lessons/round-60.md |
```

Provenance: added by `398d3225` (data commit), moved into the Registry section by
`b3c25613` ("move S561-S564 rows into the Registry table (census E12 fix)"); `S564` is absent at
entering `ddfb12fb` and freeze `ac496c7c` (`git show <rev>:corpus/SOURCES.md | grep -c S564` →
`0`/`0`), present once at `398d3225` and HEAD (`1`/`1`). `grep -c '^| S564 |' corpus/SOURCES.md` → `1`.

## Deliverable 2 — the Gate quote

`corpus/lessons/round-60.md:33-37`, verbatim:

```
- Rejected:
  - S564 — Mo59Sentinel58 report: REJECTED as a same-scope duplicate of
    S562 (same F1 execution-gate finding; this round used none of its
    constructions); flip: a future round needing its distinct F2
    expect-tamper construction re-opens the row. Kept as the taste record.
```

Supporting frozen clause, `contract.md` §2b: "Mo59Sentinel58 opened and rejected as a
duplicate-scope row".

## Reason verified — F1 is the same finding as S562

- S564 anchor `F1` = `Mo59Sentinel58.md:34` "the SHA-256 pin is advisory, not an execution gate;
  committed tool bytes run as the operator"; body `:36-37` "Both counters compute `tool_ok` from the
  pin and then **execute the bytes anyway** whenever the path exists. The pin only removes `met`;
  it never suppresses execution."
- S562 anchor `F1-F4` includes `Mo59Sentinel57.md:20` "counters execute the repo tool blob even
  when its sha256 ≠ PIN, then write repo blobs without containment/symlink checks → arbitrary file
  overwrite outside scratch (demonstrated)" and `:24` "Both counters compute `tool_ok` but gate
  only the *bookkeeping*, not execution".
- Sentinel58's extra F1 points are subsumed by S562/Sentinel57: env inheritance (`F1(b)`) is
  Sentinel57 `F3` (`Mo59Sentinel57.md:106` "full ambient environment handed to repo-supplied code
  (no scrub)"); the `selftest=ok`-from-unverified-bytes note is the same execution-gate scope; the
  16-execution count is the same call sites. No new surface.

## Flip verified — round 60 replays none of F2's three constructions

`Mo59Sentinel58.md:77` F2 ("negative-control expectations are attacker-controlled committed bytes")
executed three constructions, all on the r59 C1/C2 fixture arms: `:92-95` replace
`f08/expect.txt` with `binding` after swapping the body; `:96-98` add `f99-empty-expect` with an
empty expect; `:100-104` a validating C2 tree with an empty expect.

Round-60 uses none of them:

- `grep -c 'expect' .ufo/waves/round-60/count-c1.py` → `0` (r60 C1 has no fixture/expect arm at
  all; its re-runs are revision-pinned).
- r60 C2's tree arm instead compares the committed `expect.txt` to a counter-side frozen table:
  `.ufo/waves/round-60/count-c2.py:83` `FROZEN_EXPECTS = {…}` and `:343-365`
  (`expect_tamper:%s` on disagreement); `h02` frozen expect is `["grammar"]` and HEAD's committed
  `trees-c2h/h02-malformed-claim/expect.txt` is exactly `grammar`.
- r60 C3's G3 PoC is the opposite polarity from F2: `count-c3.py:233-248` commits
  `grammar\nTAMPERED-EXTRA\n` and requires `expect_tamper:h02-malformed-claim`, i.e. the tamper is
  *detected*, not a neutered control that stays `met`.

So "no additional construction used this round" holds at the construction/exploit level.

## Findings (report-only; no edits made)

### S1 — MATERIAL consistency conflict: the round-60 knowledge entry attributes G3 to the rejected
F2, which contradicts "no additional construction used this round" under a class-level reading.

`corpus/knowledge/entry-claims-hardening-r60.md:39`:

```
| G3 | hostile-tree expect prefixes live in the counter's frozen table; a committed `expect.txt` that disagrees is `expect_tamper:<tree>` — the scored repo can no longer grade itself | Mo59Sentinel58 F2 (attacker-controlled expect.txt) |
```

and `:37` (G1) "Mo59Sentinel57 F1; Mo59Sentinel58 F1 (S562; S564 rejected as duplicate scope)".
The r59 verifier spot-check also routes the item to the same report:
`corpus/lessons/round-59-verifier-spotcheck.md:105-106` "attacker-controlled `expect.txt`
(Sentinel58 F2)".

Two readings, reported for the canonical judge:

1. Construction-level (the row's wording): the round closed F2's *surface* with its own frozen
   table and a disagreeing-expect PoC; it did not replay F2's weakened/empty-expect escapes. The
   flip ("a future round needing Sentinel58's distinct expect-tamper construction") is not
   triggered; REJECTED stands. The landed wording narrows the flip to a *future* round, which is
   what keeps it consistent with round 60's G3.
2. Class-level: G3 is the fix for F2 and the entry says so, so round 60 *did* need an expect-tamper
   construction from this report; the flip condition stated in the seat spec ("a distinct
   expect-tamper construction this round actually needs") is then met, the row would need
   `mined` (scope "expect-tamper class closed by G3", used-by `corpus/knowledge/entry-claims-hardening-r60.md`),
   and §2b's rest-set is incomplete.

Do not resolve here: the contract's claims are frozen (immutable after scoring) and the row is
already landed. Recorded verbatim for the Rust judge.

### S2 — LOW pointer completeness: anchor cites `F1` while `teaches` names `F2`

The anchor cell is `report .ufo/waves/round-59/w1/Mo59Sentinel58.md F1`; the flip in `teaches`
depends on F2, which the anchor does not cover (S562's anchor covers `F1-F4`). Smallest correction,
not applied: anchor → ``report `.ufo/waves/round-59/w1/Mo59Sentinel58.md` F1-F2``. No dead pointer:
both paths and headings exist at HEAD (`F1` at :34, `F2` at :77).

### S3 — INFO: the rejected Gate bullet carries no located report quote

Admitted rows in the same Gate carry quoted spans; S564's bullet carries reason+flip only. This is
convention-consistent with the prior rejected own-work row (`corpus/lessons/round-57.md:16` S549
rejection carries no quote), so it is not a defect against §2b, whose "Gate quotes" sentence names
the admitted reports. If a quote is wanted, the establishing F2 sentence is
`Mo59Sentinel58.md:79-80`: "The counters read fixture bodies **and** their `expect` files from the
same revision R they grade, and nothing pins those bytes (only the tool is pinned)."

### S4 — INFO: `used-by` vs the entry's parenthetical

S564's `used-by` is `corpus/lessons/round-60.md` only. `entry-claims-hardening-r60.md:37` mentions
"S564 rejected as duplicate scope"; that is a rejection-provenance note, not a use of the row.
Census raises no W02/W03 for S564.

## Checks run (read-only, pinned)

1. `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → rc `0`; 25 standing W04
   lines + `mori ok …/corpus/SOURCES.md`; no E class. `census` → `rows 337` (= round-start 333 + 4).
2. Row shape: `awk -F'|' 'NR==344{print NF}'` → `13`; cells listed 1..11; `rejected`, `2026-10-28`,
   `180d`, lesson `used-by` exists on disk.
3. E12 provenance reproduced: validate on the extracted `398d3225` blob (scratch copy,
   `--file … --root …/mori-shokunin`) → `E12 S561..S564 row outside Registry section`, rc `1`;
   after `b3c25613` (4 insertions / 4 deletions) HEAD validates clean.
4. `git show HEAD:corpus/SOURCES.md | sha256sum` equals the worktree sha (pinned above). The row,
   lesson (HEAD blob) and knowledge entry were read at HEAD; only the lesson's worktree bytes moved
   mid-seat, below the quoted block (see pins).

## Non-actions / scope

No commits, VCS mutation, production edits, registry edits, SCORECARD/LOG edits, fleet/sibling
writes, subagents or installs. Only this report was written. Scratch
`/fast/scratch/hyaku/mori-r60/Mo60Scribe72` (TMPDIR there) removed before yielding; disk guard was
green at start (`/fast/scratch/hyaku` 26%, 597.4 G free; `/tmp` 14%; `/var/tmp` 38%).
