# Mo52ConnCrossClaim — cross-claim / cross-round pattern (round 52, wave w1)

Seat: `Mo52ConnCrossClaim` (connector). Lane: mori-shokunin. Measured revision: data commit
`8524904adb25e44f24d9f25aac7eae909625c18c` (entering `4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d`).
Item: find the shared principle behind C1's living-pin rule (supersede, never rewrite) and C2's authorship
rule (a voter never judges text it wrote), the QUALITY rows that already state part of it, and any place in
the lane where the same mistake class is still open. All reads read-only over committed bytes; no file in the
fleet repo, lane, jj state or git index was mutated. Scratch
`/fast/scratch/hyaku/mori-r52/Mo52ConnCrossClaim/` is created and removed by this seat.

## 1. The shared principle

Both C1 and C2 are instances of one rule: **no self-certification — the actor that authors a claim or a
record may not be the (sole) verifier of it, and the original authored bytes must survive in the record so
that verification is attributable and checkable.**

| claim | rule | instantiation |
|---|---|---|
| C1 | a stale tally pin is superseded by a later line, never rewritten in place | `count-c1.py` docstring: "Every pin present at the entering tip E is still present, byte for byte, at R (the record is appended to, never rewritten)" (`.ufo/waves/round-52/count-c1.py:30-31`); contract K4 house rule (`.ufo/waves/round-52/contract.md:24-28`); control proof: rewriting a stale pin in place reads `pin_removed_or_rewritten` ×3 (`evidence/control-c1-rewrite-in-place.txt`) |
| C2 | a voter's `entailed` vote does not count for a row whose text that voter wrote | `count-c2.py` docstring: "a voter's `entailed` line does not count for a row whose text that voter wrote (its report carries an unfenced `REPLACE <old> :: <text>` line…)" (`.ufo/waves/round-52/count-c2.py:18-20`); contract P-C2 (`.ufo/waves/round-52/contract.md:65-68`); origin: round-51 closure §5 item 2 — "require ≥2 votes per row from seats that did not write the row's text, so the four single-vote, self-authored replacements of this round would read unmet" (`corpus/lessons/round-51-verifier-spotcheck.md:174-178`) |

The two claims apply the principle to different objects: C1 bars a *document* from certifying its own current
tally (mutating the record erases the evidence); C2 bars a *voter* from certifying text it wrote (mutating
the verdict-by-authorship link erases the independence). Both preserve the historical byte (C1: pin bytes at
E; C2: the claim text hashed, and REPLACE recording the old hash) and both place the judgment outside the
author (C1: the frozen counter vs the fleet MANIFEST/closures; C2: two distinct non-author ENTAILMENT seats).

## 2. QUALITY rows that already state part of it

| QUALITY | line | states |
|---|---|---|
| 39 | `corpus/QUALITY.md:100` | "Writing a selftest … is not permission to run it … having written the implementation never justifies an executed result" — the instrument-must-not-grade-its-own-output half |
| 41 | `corpus/QUALITY.md:104` | a green fixture/sibling gate never establishes freshness; a re-pin that only turns red green is rejected — self-gating does not certify |
| 46 | `corpus/QUALITY.md:127-130` | a stale pending/version statement is superseded by a dated appended note, never rewritten into a claim about the current host — C1's rule stated verbatim in prose |
| 102 | `corpus/QUALITY.md:799-817` | SOURCES rows are append-only; no in-place change to an existing row; a superseding disposition does not erase an in-place change |
| 122 | `corpus/QUALITY.md:1013-1022` | "a census that publishes its own finding has discharged it" — the discharge-self class, fixed by restricting the receipt corpus |
| 123 | `corpus/QUALITY.md:1028-1029` | a registry pin is calibrated only when an instrument re-runs it from committed bytes and reads it from its own cell |
| 134 | `corpus/QUALITY.md:1178-1186` | a round reconciles its own self-assessment with the fleet record and the instruments; "the lane's own self-assessment was outside every check" — C1's direct origin |
| 141 | `corpus/QUALITY.md:1356-1364` | a living pin prints its tally today or a later line supersedes it; "the stale pin itself is never rewritten" (this row supersedes 112's check cell only) |
| 142 | `corpus/QUALITY.md:1366-` | a self-assessment pointer lands on the words it reports |

## 3. Where the same mistake class is still open

### 3.1 A document that rewrites its own pin — SOURCES rows S490/S491/S492

Command (read-only git):

```
$ python3 tools/mori-sources-appendonly.py 8524904adb25e44f24d9f25aac7eae909625c18c
…
changed S490 superseded_by=-
changed S491 superseded_by=-
changed S492 superseded_by=-
appendonly_violations=21 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193,S490,S491,S492] deleted=[] superseded=[…] round_changed=[]
$ echo $?
1
```

With the round range the round is clean (`--round-base 4f266ef2…` → same line, `exit=0`); the violations are
carried debt. Cell-level diffs against first sighting (immutable cells):

- S490: first sighting `487941b9` (round-50 data) → changed at `bae8656e` (round-50 integrate, commit message
  "S490/S491 anchors"): anchor cell `mm/memcontrol.c:1546-1608,1693-1748,1751,1770,1787-1830,4905-4919` →
  `mm/memcontrol.c:629,1546-1608,1628-1665,1693-1748,1751,1770-1784,1787-1830,1994-1999,4905-4919`; summary
  cell "not a per-page charge count" → "not the page counter's own failcnt".
- S491: same commits, anchor cell `mm/oom_kill.c:400-410,424-431,444-454,456-469,912-951,1169-1170` →
  `mm/oom_kill.c:400-410,424-431,444-454,456-469,912-985,1008-1054,1146-1170`.
- S492: first sighting `87e0c374` (round-51 data) → changed at `7c0b6232` (round-51 wave integration part 1):
  scope cell "S168 was the rejected same-scope duplicate" → "S168 was the rejected same-URL candidate (a
  duplicate of S082)".

Per QUALITY 102 these rows should have been superseded by a new row, not edited. They remain listed with
`superseded_by=-` at the data tip.

### 3.2 An instrument that grades its own output — C2 authorship is declared, not detected

C2's authorship rule is enforced only through the voter's own `REPLACE` line; nothing checks that the voter
actually wrote the row. The round-52 attack `Mo52CritC2Voters` demonstrates the class is still live:

```
== T3 author (no REPLACE) own vote counts       -> MET
   C2=met claims=12 … entailed=12 dissent=0 rev=R
== T4 REPLACE text != final claim -> author vote counts -> MET
   C2=met claims=12 … entailed=12 dissent=0 rev=R
```

(`.ufo/waves/round-52/w1/Mo52CritC2Voters.md`, evidence 2). So a row whose text a voter wrote reaches
`entailed` with that voter's own vote when the REPLACE declaration is omitted or stale. The contract names this
limit ("a REPLACE line is the only authorship signal read", `.ufo/waves/round-52/contract.md:84-85`), but note
the asymmetry: C1's rewrites are detected objectively (byte-for-byte comparison against E), while C2's
self-authorship is detectable only by author self-report. The counter does not compare the entry's claim text
against any voter's prose.

### 3.3 Instruments that write into the repo they measure

- `count-c1.py` (round 48/49) defaults scratch inside the lane: `scratch = opts["--scratch"] or
  tempfile.mkdtemp(prefix="c1-", dir=os.path.join(repo, ".scratch"))` — `.ufo/waves/round-48/count-c1.py:292`
  and `.ufo/waves/round-49/count-c1.py:332`. Without `--scratch` the instrument creates files under the repo it
  measures. Round-50 deleted one `.scratch` residue (`bae8656e` commit message: ".scratch residue deleted
  (receipt)") but the default behavior is unchanged. Round-51 closure §5 item 8 plans an inventory; it has not
  landed yet.
- Round-40 `conform.py` was edited in place after its freeze. The freeze receipt records
  `5025b9664632d01063c11b4f5dadd4f9a063db66d73315d7ed25db8d90b83aaf .ufo/waves/round-40/conform.py`
  (`evidence/freeze-r40.txt:9`); at `8524904a` the file hashes to `7f5174d542bd983552670b06f6cc424b10e53c81e55ecabcdd919f4043bdfa23` (last edit `87e0c374`, "conform.py path fix"). D-e is carried, not closed.

### 3.4 The discharge-self census admission is unbuilt

QUALITY 122 states the fix (restrict `receipt` to `corpus/evidence/*` and `.ufo/waves/<round>/evidence/*`,
excluding `w1/*` seat prose) and says "the narrower corpus is not yet built (this criterion is the admission, not
the instrument)" (`corpus/QUALITY.md:1022`). No instrument in `tools/` or `scripts/hyaku/` implements the
restriction today (`grep -rn -E "uncited|discharge" tools/ scripts/hyaku/` → no hits). The discharge-self class
remains admission-only.

### 3.5 Note — QUALITY 77 vs 141 wording

QUALITY 77 says a stated-fact correction sweeps every mention in place and "the superseded wording is removed,
not shadowed" (`corpus/QUALITY.md:349-351`), while QUALITY 141 says a stale tally pin is never rewritten. These
govern different objects (asserted facts vs instrument pins) and do not conflict, but the two phrases sit side by
side in the same document and are the kind of wording that allowed earlier in-place registry edits (S490-492).

## Evidence commands

```
$ python3 tools/mori-sources-appendonly.py 8524904adb25e44f24d9f25aac7eae909625c18c
   → appendonly_violations=21 ids=[…S490,S491,S492] superseded_by=- … round_changed=[] ; exit=1
$ python3 tools/mori-sources-appendonly.py 8524904adb25e44f24d9f25aac7eae909625c18c --round-base 4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d
   → same ids line ; exit=0 (no new violations this round)
$ git show 8524904a:.ufo/waves/round-40/conform.py | sha256sum
   → 7f5174d542bd983552670b06f6cc424b10e53c81e55ecabcdd919f4043bdfa23  -   (freeze says 5025b966…)
$ git log --oneline -G 'S490' -- corpus/SOURCES.md   → bae8656e, 487941b9
$ git log --oneline -G 'S492' -- corpus/SOURCES.md   → 7c0b6232, 87e0c374
$ git diff 4f266ef2 8524904a -- corpus/SOURCES.md   → only +5 appended rows S497-S501 (no row edits)
```

## Findings

- **HIGH** — `corpus/SOURCES.md` rows S490/S491/S492 were rewritten in place after first sighting (anchor and
  scope cells; commits `bae8656e`, `7c0b6232`); the append-only gate still lists them
  `appendonly_violations=21`, `superseded_by=-`, exit 1 at the data tip. Same mistake class as the C1 pin
  rewrites, in the registry.
- **HIGH** — C2's authorship rule is unverifiable when the `REPLACE` line is omitted or stale: a voter can vote
  `entailed` on rows it wrote and P-C2 still reads `met` (attack T3/T4 in `Mo52CritC2Voters.md`). The counter
  cannot distinguish self-certification from independent judgment; only the author's self-report marks
  authorship.
- **MED** — `count-c1.py` round 48/49 default scratch to `<repo>/.scratch`, writing inside the repo they measure
  (`.ufo/waves/round-48/count-c1.py:292`, `.ufo/waves/round-49/count-c1.py:332`); the round-51 inventory is
  not landed.
- **MED** — round-40 `conform.py` still diverges from its freeze record (`7f5174d5…` vs `5025b966…`, D-e).
- **MED** — QUALITY 122's discharge-self fix is admission-only; the narrower receipt corpus is unbuilt and no
  tool enforces it.
- **LOW** — QUALITY 77 ("removed, not shadowed") and 141 ("never rewritten") coexist with opposite-sounding
  wording for different object classes; flagged to prevent future drift.
