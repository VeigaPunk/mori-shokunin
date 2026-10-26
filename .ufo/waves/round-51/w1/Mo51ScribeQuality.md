# Mo51ScribeQuality — QUALITY criteria draft (round 51, wave w1)

Seat: Mo51ScribeQuality (scribe). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`. Scratch:
`/fast/scratch/hyaku/mori-r51/Mo51ScribeQuality/` (created, used, removed before this report was finished).
Read first: `.ufo/waves/round-51/contract.md` (freeze `4677910e`), the data commit
`87e0c374537557754bf71dd68036ded3ddc6699c`, and `corpus/QUALITY.md` lines 1124-1250. The last numbered criterion
is 136; this draft adds 137-140. No product, judge, counter, corpus, tool or other wave file was edited; this
report is the only file written outside scratch. No tool installed; no pacman transaction; `~/.local/bin`
untouched.

## 1. Observed runs

### 1a. Candidate (b) — the `class=` field, reproduced at both revisions

I rebuilt the frozen five-row fixture registry from `count-c1.py`'s own `HDR`/`FIXTURES`/`ROWS` constants and ran
`git show <rev>:tools/mori-pin-check.py` on it with `--root` (TMPDIR in scratch; scratch paths elided, and each
`pin line=` shown abridged at `…` — the class suffix and the summary tail are verbatim):

```
$ python3 tool-at-data.py --root fx-data --timeout 60          # tool from 87e0c374
pin line=3 … prefix=ENVA_SELFTEST state=mismatch … rc=2 … class=env
pin line=4 … prefix=ENVB_SELFTEST state=mismatch … rc=1 … class=env
pin line=5 … prefix=STLA_SELFTEST state=mismatch … observed='pass=5 fail=0' rc=0 … class=stale
pin line=6 … prefix=STLB_SELFTEST state=mismatch … observed='pass=2 fail=0' rc=1 … class=stale
pin line=7 … prefix=OKAY_SELFTEST state=match … (no class)
PIN_CHECK=unmet … mismatches=4 … env=2 stale=2
rc=1
$ python3 tool-at-entering.py --root fx-entering --timeout 60  # tool from aa3af1ec
pin line=3 … prefix=ENVA_SELFTEST state=mismatch … rc=2 …            (no class)
pin line=4 … prefix=ENVB_SELFTEST state=mismatch … rc=1 …            (no class)
pin line=5 … prefix=STLA_SELFTEST state=mismatch … observed='pass=5 fail=0' rc=0 …   (no class)
pin line=6 … prefix=STLB_SELFTEST state=mismatch … observed='pass=2 fail=0' rc=1 …   (no class)
PIN_CHECK=unmet … mismatches=4 … (no env=/stale= tail)
rc=1
```

The data tool ends every mismatch line with `class=env` or `class=stale` and its summary with `env=2 stale=2`;
the entering tool has neither. This reproduces the class arm of `evidence/c1-at-data.txt` and the bare-mismatch
shape of `evidence/control-c1-do-nothing.txt` without re-running the heavy counter. I also read
`tools/mori-pin-check.py:804-866`: `kind = "env" if observed is None else "stale"`, and the summary prints
`env=%d stale=%d`.

### 1b. Candidate (d) — entailment arm

```
$ python3 .ufo/waves/round-51/count-c2.py --hashes 87e0c374537557754bf71dd68036ded3ddc6699c > hashes.txt
$ diff hashes.txt .ufo/waves/round-51/evidence/c2-hashes-at-data.txt
(diff empty, rc 0)
$ python3 .ufo/waves/round-51/count-c2.py 87e0c374537557754bf71dd68036ded3ddc6699c
C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok
entailed=0 dissent=0 rev=87e0c374537557754bf71dd68036ded3ddc6699c failed=entailment
rc=1
$ python3 .ufo/waves/round-51/count-c2.py --selftest | tail -1
C2_SELFTEST pass=34 fail=0
rc=0
```

The at-data line equals `evidence/c2-at-data.txt` line for line; the 21 hashes equal `c2-hashes-at-data.txt`.
I read `count-c2.py:117-133` (`ENTAIL_RE = ^\s*ENTAIL\s+([0-9a-f]{12})\s+(entailed|overclaim)\b`; every line of
every `.md` under `w1/` whose basename does not start `MoriR51`, no fence awareness, no writer-role check) and
`:215-226` (overclaim wins, one entailed vote is enough).

### 1c. Candidate (c) — MemAvailable versus a free-plus-cached sum

```
$ grep -rn 'MemFree' tools/ corpus/knowledge/
tools/mori-round17-jj-regressions.py:440:… "MemTotal: …\nMemAvailable: …\nMemFree: …\n"   (a fixture file, no arithmetic)
corpus/knowledge/memavailable-estimate-r51.md:23:… quote of the doc's input list …
corpus/knowledge/memavailable-estimate-r51.md:37:… quote of the two adjacent print calls …
corpus/knowledge/memavailable-estimate-r51.md:46:- Read `MemAvailable` itself for runway; never rebuild it as `MemFree + Cached` — …
$ grep -rnE 'MemFree[[:space:]]*\+' tools/ corpus/knowledge/ | grep -v 'never rebuild'
(no output, rc 1)
$ grep -rnE '\+[[:space:]]*MemFree' tools/ corpus/knowledge/
(no output, rc 1)
$ grep -c 'never rebuild it as' corpus/knowledge/memavailable-estimate-r51.md
1
$ grep -n 'meminfo_field MemAvailable' tools/mori-census.sh
1792:    mavail=$(meminfo_field MemAvailable)
```

Failure arm (uncommitted, on a scratch copy with the rule inverted to `rebuild it as \`MemFree + Cached\``):

```
$ grep -nE 'MemFree[[:space:]]*\+' entry-inverted.md | grep -v 'never rebuild'
46:- Read `MemAvailable` itself for runway; rebuild it as `MemFree + Cached` — …   (rc 0)
$ grep -c 'never rebuild it as' entry-inverted.md
0
```

So the check distinguishes the landed rule from a sum, but that arm has no committed receipt under `evidence/`.
The live reading is `tools/mori-census.sh:1792`; seven `corpus/knowledge/` entries read `MemAvailable`.

### 1d. Candidate (a) — outside-repo re-execution and the hidden lane path

Not re-executed by this seat. The quoted verdict is the L1's at-data run
(`evidence/c1-at-data.txt`: `C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok
selftest=pass=119,fail=0 rev=87e0c374… failed=-`, exit 0); the two failure arms are the committed controls
`evidence/control-c1-do-nothing.txt` (`kill_residue=12547 relocated=unmet reloc_mismatch=1`, exit 1) and
`evidence/control-c1-scratch-only.txt` (`kill_residue=0 relocated=unmet reloc_mismatch=3`, exit 1). I read the
counter's arm code: `fresh_clone` uses `git clone --no-local`; `arm_kill` polls the clone's
`status --porcelain --ignored --untracked-files=all` and its TMPDIR, waits 3 s after progress, SIGKILLs the
process group, and counts the clone's status lines; `arm_relocated` runs inside
`bwrap --tmpfs <lane>` and asserts `<lane>/SKILL.md` does not exist; scratch inside the repo or inside the hidden
path is refused (`main`, `C1_SETUP scratch inside`). The heavy rerun is `ExecC1Rerun`'s item; this seat did not
duplicate it.

Receipt tracking (all read-only): `c1-at-data.txt`, `c2-at-data.txt` and `c2-hashes-at-data.txt` are tracked at
`b504cb17` (the wave dispatch commit), not at `87e0c374`, the revision they measure. Every path cited below
resolves at HEAD.

## 2. Draft criteria (for `corpus/QUALITY.md`, after 136)

```markdown
## Criteria added round 51 — a re-execution outside the repo, a mismatch class, a runway reading, an entailment vote

137. **An instrument that re-executes pins runs on a tree outside the repo it reads, and the re-execution holds
    with that repo's path hidden.** Lesson: `corpus/lessons/round-51.md` M1 (hidden location dependence; the row
    is drafted this wave with `captured-by` QUALITY 127). Rationale: at the entering tip
    `tools/mori-pin-check.py`'s `--rev` mode exported the tree it measured under `<repo>/.scratch`, so a
    SIGKILLed run left 12,547 untracked or ignored paths in the repo it read
    (`C1=unmet kill_residue=12547 relocated=unmet reloc_mismatch=1`,
    `.ufo/waves/round-51/evidence/control-c1-do-nothing.txt`, exit 1); moving that export to TMPDIR removed the
    residue but left three pins failing outside the repo (`reloc_mismatch=3`,
    `.ufo/waves/round-51/evidence/control-c1-scratch-only.txt`, exit 1) because
    `.ufo/waves/round-49/count-c1.py` reads the `master` branch and `tools/mori-round19-regressions.py` reads git
    objects from the tree it runs in — a `git archive` export has neither. v5 checks out a `git clone --shared`
    of R under `--scratch`/TMPDIR instead (`tools/mori-pin-check.py` docstring: "never `<repo>`"). Check:
    `python3 .ufo/waves/round-51/count-c1.py <rev>` exits 0 with
    `C1=met kill_residue=0 relocated=met reloc_mismatch=0`, where arm A starts
    `tools/mori-pin-check.py --rev R --repo C0` in a fresh `--no-local` clone C0 with TMPDIR in scratch, waits
    until it is writing, waits 3 s, SIGKILLs the process group, and counts
    `git -C C0 status --porcelain --ignored --untracked-files=all` lines; arm B runs in a second clone inside
    bubblewrap with `--tmpfs <lane>` and asserts `<lane>/SKILL.md` is absent. At the data commit `87e0c374` it
    printed `C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=119,fail=0
    rev=87e0c374… failed=-`, exit 0 (`.ufo/waves/round-51/evidence/c1-at-data.txt`). Shown able to fail: the two
    receipts above, `kill_residue=12547` and `reloc_mismatch=3`, each `C1=unmet` and exit 1. Not covered: arm A
    kills at one moment (3 s after the first write) and proves nothing about a kill at another; arm B hides one
    path and does not prove portability to another host, user or kernel; the counter's C0/C1 are `--no-local`
    clones but v5's own measured tree is `--shared`, so a repack or prune of the source repo during the run is
    untested; `--root` mode still writes `<root>/.scratch` and is not claimed.

138. **A pin mismatch carries a class that separates "could not run here" from "the pin is stale", and the
    summary counts both.** Lesson: `corpus/lessons/round-51.md` M1 — the hidden dependence surfaced as a bare
    mismatch; the class rule itself is `considerthese/2026-10-26.md` suggestion 1 (operator reflection, opened
    2026-10-26), not an M row. Rationale: at the entering tip a mismatch line read `state=mismatch …
    observed=None rc=2` and ended with no class (`.ufo/waves/round-51/evidence/control-c1-do-nothing.txt`; this
    seat reproduced that shape with the `aa3af1ec` tool on the frozen five-row fixture), so a pin that could not
    run and a pin that had drifted looked alike. v5 tags `class=env` when the pinned command printed no tally
    line for its prefix (setup error, missing path, timeout, OS error), `class=stale` when it ran and printed a
    different tally, a tally its exit code contradicts, or a digest/line-count difference, and its summary ends
    `env=N stale=N` with env + stale = mismatches (`tools/mori-pin-check.py:804-866`). Check:
    `python3 .ufo/waves/round-51/count-c1.py <rev>` prints `classified=ok` and five `classified:` lines —
    `ENVA_SELFTEST … class=env`, `ENVB_SELFTEST … class=env`, `STLA_SELFTEST … class=stale`,
    `STLB_SELFTEST … class=stale`, `OKAY_SELFTEST state=match` with no class — and a summary ending
    `env=2 stale=2`; at `87e0c374` the receipt's lines are those
    (`.ufo/waves/round-51/evidence/c1-at-data.txt`). Shown able to fail: a classifier that says env for
    everything prints `class=env` on the two stale rows and ends `env=4 stale=0`, with `classified=bad` and
    `C1=unmet` (`.ufo/waves/round-51/evidence/control-c1-always-env.txt`, exit 1); the class-only control is
    green on this arm (`classified=ok`) while residue and relocation still fail
    (`.ufo/waves/round-51/evidence/control-c1-class-only.txt`, exit 1), so the class alone is not the claim. Not
    covered: the rule is "no tally line ⇒ env", so a tool that prints its tally and then dies for an
    environmental reason is classed stale (named in the contract); every class observed so far is on a synthetic
    five-row registry — no real lane pin mismatched at the data commit; `--root` mode's classes are not claimed.

139. **A runway reading is read from `MemAvailable`, and no lane instrument or entry rebuilds it as the sum of
    free and cached memory.** Lesson: no round-51 M row covers this rule; the pointer is
    `corpus/knowledge/memavailable-estimate-r51.md` Reading rules, sourced by S496 (the 2014 commit says workload
    placers summed "free" and "cached" and calls that wrong because `Cached` includes shmem and tmpfs). Rationale:
    the dispatcher gates seat spawns on `MemAvailable` and `tools/mori-census.sh:1792` reads the field itself
    (`mavail=$(meminfo_field MemAvailable)`), while a `MemFree + Cached` sum counts tmpfs and shmem pages the
    estimate does not add (entry rows 4, 7, 17, 20) — the reading the commit that introduced the line replaced.
    Check: `grep -n 'meminfo_field MemAvailable' tools/mori-census.sh` prints
    `1792:    mavail=$(meminfo_field MemAvailable)`; `grep -c 'never rebuild it as'
    corpus/knowledge/memavailable-estimate-r51.md` prints `1`; and
    `for p in 'MemFree[[:space:]]*\+' '\+[[:space:]]*MemFree'; do printf '%s -> ' "$p"; grep -rE "$p" tools/
    corpus/knowledge/ | grep -v 'never rebuild' | wc -l; done` prints `MemFree[[:space:]]*\+ -> 0` and
    `\+[[:space:]]*MemFree -> 0`. Shown able to fail: on a scratch copy of the entry whose bullet reads
    "rebuild it as `MemFree + Cached`" the same loop prints `1` for the first pattern and the rule count prints
    `0` (run in this seat's scratch; no committed receipt under `.ufo/waves/round-51/evidence/`, so the committed
    arm is `not yet shown`). Not covered: the greps prove no lane file spells the sum, not that every reading
    uses `MemAvailable` (a reading could use `MemTotal` or swap); row 2 legitimately names `MemFree` as an input
    of the kernel's formula, so the rule is about rebuilding the output, not about mentioning the input;
    `MemAvailable` is itself a model (entry rows 1 and 3), so a threshold on it is a threshold on an estimate;
    S116 (earlyoom) records a fallback guesstimate and is not covered by the grep.

140. **A depth claim carries a committed entailment vote for every row, and an `overclaim` vote blocks the row
    until its text is replaced.** Lesson: `corpus/lessons/round-50.md` M4 (an overclaim survived the counter),
    carried by `corpus/lessons/round-50-verifier-spotcheck.md` §5 item 4; no round-51 M row. Rationale: round
    50's depth counter met at `487941b9` with `claims=22 located=22` while wave a2w1 found six claims their quotes
    do not carry (M4) — location proves the quoted words exist, not that the claim follows. P-C2 adds: for every
    row, the report files committed at R under `.ufo/waves/round-51/w1/` whose names do not start `MoriR51` carry
    at least one line `ENTAIL <h> entailed` and no line `ENTAIL <h> overclaim`, where `<h>` is the first 12 hex
    digits of the sha256 of the row's claim cell with whitespace collapsed and ends stripped; `--hashes R` prints
    each `<h>` (`count-c2.py:117-133`). Check: `python3 .ufo/waves/round-51/count-c2.py <rev>` exits 0 and prints
    `C2=met claims=21 located=21 … entailed=21 dissent=0`, and
    `python3 .ufo/waves/round-51/count-c2.py --hashes <rev>` lists 21 row hashes equal to
    `.ufo/waves/round-51/evidence/c2-hashes-at-data.txt`. At the data commit the counter printed
    `C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok
    entailed=0 dissent=0 … failed=entailment`, exit 1 (`.ufo/waves/round-51/evidence/c2-at-data.txt`), and the
    same command reproduced that line in this seat's run. Shown able to fail: that receipt;
    `C2_SELFTEST pass=34 fail=0` (`.ufo/waves/round-51/evidence/selftest-c2.txt`) carries
    `entail_one_row_unreviewed_unmet`, `entail_dissent_unmet`, `entail_l1_file_ignored_unmet`,
    `entail_other_dir_ignored_unmet`, `entail_hash_of_other_text_unmet` and `entail_non_md_ignored_unmet`. Not
    covered: a vote records that a non-L1 seat asserted the judgment for that exact text, not that the judgment
    is right; the counter filters `MoriR51*` files by name and accepts any other `.md` under `w1/`, so it cannot
    tell an ENTAILMENT seat's vote from another seat's line, and it parses lines inside fenced blocks; one
    `entailed` vote meets the arm although the wave dispatches two seats per row; the hash covers the claim cell
    only, not the quote; an `overclaim` clears only when the claim text is replaced (new hash), never by deleting
    the vote.
```

## 3. What the draft rests on, and what it does not

- Every quoted counter line is from committed bytes: `count-c2.py` and the entry were re-read at `87e0c374`; the
  C1 line is the committed at-data receipt (the L1's run). This seat ran the C2 counter at the data revision
  (exit 1, line equal to the receipt), the C2 selftest (exit 0), `--hashes` (diff empty, exit 0), and the
  five-row class fixture against both tool revisions (exit 1 each).
- The heavy C1 arms (two full clones, kill, bwrap) were not re-executed here; the independent rerun is
  `ExecC1Rerun`'s item, and re-running it to decorate the report is what the lane's scribe rule forbids.
- Candidate (c)'s failure arm is a scratch demonstration only; the committed arm is marked `not yet shown`.
- Criteria 139 and 140 have no `corpus/lessons/round-51.md` M row to point at: the Mistakes rows drafted this
  wave are M1 (hidden location dependence) and M2 (the round-50 residue producers). Their `Lesson:` lines name
  the originating row (`S496`; `corpus/lessons/round-50.md` M4 + spot-check §5 item 4) instead. If the integrator's
  final lesson adds a row for either, 139/140 should be renumbered to it; 137 and 138 cite M1 as drafted.
- No host kill or OOM record was read; no `/proc` value is claimed.

## Findings

1. **MED — the frozen entailment arm cannot tell a vote from a quoted line.** `count-c2.py:117-133` matches any
   line beginning (after spaces) with the hash and the verdict in any `.md` under `.ufo/waves/round-51/w1/`
   whose basename does not start `MoriR51`, without reading the writer's seat role and without skipping fenced
   blocks. A non-entailment seat that quotes another seat's vote inside a fence casts a vote for that hash; the
   wave prompt's "only ENTAILMENT seats write such lines" is not measurable by the counter. Named as a limit in
   criterion 140; the counter is frozen, so this is a report for the closure, not a change.
2. **LOW — the round shape's two-seats-per-row rule is not the predicate.** The frozen P-C2 requires one
   `entailed` vote per row (`count-c2.py:219-222`), while the contract's Round shape dispatches votes "by at
   least two seats of different roles"; a row with one vote meets the claim and a row whose two voters share a
   model is indistinguishable from two independent judgments. Reported, not fixed.
3. **LOW — the class arm is demonstrated only on synthetic fixtures.** Every `class=` line in
   `evidence/c1-at-data.txt` is a five-row `--root` fixture; no real lane pin mismatched at `87e0c374`, so no
   committed receipt shows a real instrument classified. The rule's own edge ("tally printed, then an
   environmental death ⇒ stale") is named in the contract and untested by any receipt
   (`tools/mori-pin-check.py:824`).
4. **LOW — the at-data receipts are not in the revision they measure.** `evidence/c1-at-data.txt`,
   `c2-at-data.txt` and `c2-hashes-at-data.txt` are tracked at `b504cb17`, not at `87e0c374`; a reader running
   `git show 87e0c374:.ufo/waves/round-51/evidence/c1-at-data.txt` gets nothing. The criteria cite the paths,
   which resolve at HEAD; the closure's LOG/SCORECARD should name the receipt commit.
5. **LOW — the MemAvailable check matches the rule's own wording.** `corpus/knowledge/memavailable-estimate-r51.md:46`
   is the only lane line containing `MemFree +`, and it is the prohibition; the pass therefore depends on
   `grep -v 'never rebuild'`. An honest rewording of that bullet ("do not sum free and cached") would make the
   check read 0 while the rule still stands, and a use phrased differently would evade it. The criterion's Check
   carries the filter explicitly for this reason.
6. **LOW — the `--shared` measured tree's dependence on the source object store is untested.** v5 checks out a
   `git clone --shared` of R (`tools/mori-pin-check.py` docstring), which borrows objects from the repo it reads;
   neither arm A nor arm B exercises a source-repo repack or prune during the run. This is the concern the
   wave's `RevenScratchProducers` / `SentKillSafety` items probe; criterion 137 names it in Not covered.
