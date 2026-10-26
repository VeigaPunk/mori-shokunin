# Mo51ScribeLogScorecard — LOG.md and SCORECARD.md round-51 drafts (scribe, w1)

Seat: Mo51ScribeLogScorecard, leaf scribe. No product file was edited; nothing was installed; no counter and no
predicate is proposed for change. Everything below is read from committed bytes or from the frozen receipts, with the
command that produced it. Drafts are fenced and must be integrated by the L1.

## Sources read (with the exact commands)

| what | command | observed |
|---|---|---|
| contract | `read .ufo/waves/round-51/contract.md` | 147 lines, freeze-listed; P-C1/P-C2, controls table, named limits, routed-defect carriers |
| LOG house shape | `tail -n 120 LOG.md` (`LOG.md` is 2763 lines) | `## Round 50 (L1 MoriR50a2, attempt 2; C1 calibration, C2 depth)` is the last section; no `## Round 51` (`grep -n '^## Round 51' LOG.md SCORECARD.md` → rc 1) |
| SCORECARD house shape | `tail -n 90 SCORECARD.md` + `sed -n '1,40p' SCORECARD.md` | `## Round 50 — …` is the last section; `## Axes` gives the entering scores |
| C1 before | `cat .ufo/waves/round-51/evidence/control-c1-do-nothing.txt` | quote below, `exit=1` |
| C1 at data | `cat .ufo/waves/round-51/evidence/c1-at-data.txt` | quote below, `exit=0` |
| C2 before / at data | `cat …/control-c2-do-nothing.txt …/c2-at-data.txt` | quotes below, `exit=1` each |
| C1 controls | `grep -E '^(C1=\|exit=\|\$ )' …/control-c1-{scratch-only,conform-only,class-only,always-env,witness}.txt` | quotes below |
| freeze contents | `git show --stat 4677910e…` | 22 files, +7406; no data file |
| data contents | `git show --stat 87e0c374…` | 8 files, +327 −33 |
| claim surfaces | `git diff --stat aa3af1ec… 87e0c374… -- tools/mori-pin-check.py .ufo/waves/round-40/conform.py SKILL.md SHONEN.md corpus/SOURCES.md corpus/knowledge/` | pin-check 137 lines changed, conform.py 7, SKILL.md 2, SHONEN.md 2, SOURCES.md 5, entry 65 |
| registry rows | `git show aa3af1ec…:corpus/SOURCES.md \| grep -cE '^\| S[0-9]+ '` and the same on the working tree | 264 at entering, 269 after rows S492–S496 |
| selftests | `head/tail …/evidence/selftests/mori-pin-check.txt`, `…/mori-unlanded-check.txt` | `PIN_CHECK_SELFTEST pass=119 fail=0`, `UNLANDED_SELFTEST pass=17 fail=0` |
| C2 selftest | `cat …/evidence/selftest-c2.txt` | `C2_SELFTEST pass=34 fail=0` |
| census | `cat …/evidence/census-start.txt` | `mori ok`, `rc=0`, 22 W04 lines |
| wave spec | `json .ufo/waves/round-51/w1-spec.json` (python read) | `.wave=mori-r51-w1`, 68 items; roles reviewer 14, critic 12, executor 18, mutation-tester 3, scout 2, scribe 9, simplifier 2, sentinel 4, connector 3, revenger 1; no name starts `MoriR51` |
| dispatch commit | `git show --stat b504cb17` | spec, dispatch, validation (0 bytes), `c1-at-data.txt`, `c2-at-data.txt`, `c2-hashes-at-data.txt` |
| new pin-check arms | `git diff aa3af1ec… 87e0c374… -- tools/mori-pin-check.py` | `v5_class_env_setup_error`, `v5_class_env_timeout`, `v5_class_stale_tally`, `v5_class_stale_digest`, `v5_rev_export_outside_repo` = 114 → 119 |
| working tree | `git status --porcelain --ignored` | 14 lines; one untracked scratch dir (finding 2), the rest mid-wave files and ignored caches |

Exact lines quoted by the drafts (verbatim, from the receipts above):

- C1 before: `C1=unmet kill_residue=12547 relocated=unmet reloc_mismatch=1 classified=bad selftest=pass=114,fail=0 rev=aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd failed=kill_residue,relocated,classified`, `exit=1`.
- C1 at data: `C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=119,fail=0 rev=87e0c374537557754bf71dd68036ded3ddc6699c failed=-`, `exit=0`.
- C2 before: `C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=bad provenance=bad entailed=0 dissent=0 rev=aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd failed=entry_absent,pins`, `exit=1`.
- C2 at data: `C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=87e0c374537557754bf71dd68036ded3ddc6699c failed=entailment`, `exit=1`.
- C1 controls: scratch-only `C1=unmet kill_residue=0 relocated=unmet reloc_mismatch=3 classified=bad selftest=pass=114,fail=0 rev=cb0a8c52… failed=relocated,classified` `exit=1`; conform-only `C1=unmet kill_residue=12478 relocated=met reloc_mismatch=0 classified=bad selftest=pass=114,fail=0 rev=d57cd56e… failed=kill_residue,classified` `exit=1`; class-only `C1=unmet kill_residue=1 relocated=unmet reloc_mismatch=2 classified=ok selftest=pass=118,fail=1 rev=a7223fe2… failed=kill_residue,relocated,selftest` `exit=1`; always-env `C1=unmet kill_residue=0 relocated=unmet reloc_mismatch=1 classified=bad selftest=pass=118,fail=1 rev=8ee22bde… failed=relocated,classified,selftest` `exit=1`; witness `C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=119,fail=0 rev=42719d0f… failed=-` `exit=0`.

Not rerun by this seat: no counter, no control, no selftest. The receipts are quoted as committed. The at-landed-tip
values do not exist yet and are marked `[L1 fills]` in both drafts.

---

## Draft A — LOG.md `## Round 51` entry (append after the Round 50 section)

```markdown
## Round 51 (L1 MoriR51, attempt 1; C1 operability, C2 depth)

Entering tip `aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd` (round-50 closure,
`corpus/lessons/round-50-verifier-spotcheck.md`); freeze `4677910eae6df3dabd38fe9a0daf1945146a1110` (contract, both
counters, `controls/` builder and witness bytes, the six C1 control receipts with the C2 do-nothing receipt, the
census-start receipt and the five source copies under `corpus/evidence/sources-r51/`; digests in
`evidence/freeze-sha256.txt`; 22 files, no data file); data `87e0c374537557754bf71dd68036ded3ddc6699c` (8 files). One v2
wave `w1` ran after the data. Scores entering (SCORECARD.md `## Axes`): coverage 6, operability 7, depth 5, freshness 5,
calibration 5, adjacency 6. The lowest non-retired axes are depth, freshness and calibration (tied at 5), so C2 works
depth and C1 works operability. No stagnation waiver and no exploratory claim; no score change is claimed by the lane,
and the non-author closure rules.

Motivating evidence: round-50 closure §5 items 1 and 4 — two instruments wrote their export inside the repo they read
(`tools/mori-pin-check.py:884-887` at the entering tip; `.ufo/waves/round-40/conform.py:69`) and a depth claim rested on
quote location alone — plus `considerthese/2026-10-26.md` suggestion 1 (split "cannot run here" from "stale").

- **C1 (operability): pin re-execution is hermetic and says why a pin failed.** `tools/mori-pin-check.py` v5: the `--rev`
  measured tree is a `git clone --shared --no-checkout` checked out detached at R under `--scratch DIR` (default: the
  TMPDIR temp dir), never `<repo>/.scratch` — a SIGKILLed run leaves its clone in scratch, not in the repo it reads — and
  every mismatch line ends `class=env` (the pinned command printed no tally line: it could not run here) or `class=stale`
  (it ran and printed a different tally, a tally whose exit code contradicts it, or a differing digest/line-count pin); the
  summary line ends `env=N stale=N`, and env + stale = mismatches. `.ufo/waves/round-40/conform.py` derives `LANE` from its
  own path (`<lane>/.ufo/waves/round-40/conform.py`) and puts its selftest scratch under TMPDIR. Selftest 114 → 119 (five
  arms: env setup error, env timeout, stale tally, stale digest, export outside the repo); `SKILL.md`'s registry row pins
  `PIN_CHECK_SELFTEST pass=119 fail=0` and `SHONEN.md`'s tally cell pins `(119/119)` with the round-51 receipts.
  - Counting command: `python3 .ufo/waves/round-51/count-c1.py R [--scratch DIR]` — four arms: (A) a SIGKILLed
    `--rev` run in a fresh `--no-local` clone leaves 0 lines in `git status --porcelain --ignored --untracked-files=all`;
    (B) a run in a second clone under bubblewrap with the lane working-tree path hidden exits 0 with `PIN_CHECK=met`;
    (C) the five-row fixture registry tags its two no-tally pins `class=env`, its different-tally and rc-contradicting
    pins `class=stale`, its matching pin carries no class, and the summary ends ` env=2 stale=2`; (D) the selftest exits 0
    with `PIN_CHECK_SELFTEST pass=N fail=0`, N >= 114.
  - Before (`aa3af1ec`): `C1=unmet kill_residue=12547 relocated=unmet reloc_mismatch=1 classified=bad
    selftest=pass=114,fail=0 rev=aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd failed=kill_residue,relocated,classified`,
    rc 1 — `evidence/control-c1-do-nothing.txt`.
  - At data (`87e0c374`): `C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok
    selftest=pass=119,fail=0 rev=87e0c374537557754bf71dd68036ded3ddc6699c failed=-`, rc 0 — `evidence/c1-at-data.txt`.
    The arm-C reading in that receipt is the fixture registry, which is deliberately unmet (`mismatches=4`); it proves the
    classes, not that the lane's own `SKILL.md` reconciles.
  - After: `[L1 fills: the at-landed-tip C1 line (exit code) and its receipt path.]`
- **C2 (depth): what `/proc/meminfo`'s MemAvailable is.** `corpus/knowledge/memavailable-estimate-r51.md` — the kernel's
  estimate of the memory a new application can start with, its inputs (free pages minus `totalreserve_pages`, the two file
  LRU lists, reclaimable kernel memory), the low-watermark holdbacks (the smaller of half and the summed low watermarks),
  the zero clamp, the kB printing helper, and the 2014 commit's stated reason the older free-plus-cached sum misleads (it
  counts shared memory, tmpfs and ramfs that cannot be dropped); 21 claim rows over five sources. New rows S492
  (`Documentation/filesystems/proc.rst` at v7.2, new scope), S493 (`mm/show_mem.c`), S494 (`fs/proc/meminfo.c`), S495
  (`include/linux/mm_inline.h`), S496 (commit `34e431b0ae39`), all opened 2026-10-26; copies under
  `corpus/evidence/sources-r51/`, digests in `evidence/freeze-sha256.txt`; registry rows 264 → 269.
  - Counting command: `python3 .ufo/waves/round-51/count-c2.py R` (the predicate is the counter's docstring verbatim). The
    entailment arm is routed defect 4: every row needs a report under `.ufo/waves/round-51/w1/` (names not starting
    `MoriR51`) carrying at least one line `ENTAIL <h> entailed` for the row's claim text and no line `ENTAIL <h> overclaim`,
    `<h>` = first 12 hex of sha256 of the whitespace-collapsed claim cell.
  - Before (`aa3af1ec`): `C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=bad
    provenance=bad entailed=0 dissent=0 rev=aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd failed=entry_absent,pins`, rc 1 —
    `evidence/control-c2-do-nothing.txt`.
  - At data (`87e0c374`): `C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok
    provenance=ok entailed=0 dissent=0 rev=87e0c374537557754bf71dd68036ded3ddc6699c failed=entailment`, rc 1 —
    `evidence/c2-at-data.txt`: every quote is located in its committed copy, and the claim is unmet on the entailment arm
    alone, because no non-L1 seat had yet recorded a judgment.
  - After: `[L1 fills: the at-landed-tip C2 line with entailed=N and dissent=N, its exit code and its receipt path.]`
- **Controls (C1, all scored by the frozen counter before data; receipts under `.ufo/waves/round-51/evidence/`):**
  do-nothing `kill_residue=12547 relocated=unmet reloc_mismatch=1 classified=bad selftest=pass=114,fail=0`, rc 1 — the
  target is not reachable without work; scratch-only `kill_residue=0 relocated=unmet reloc_mismatch=3 classified=bad
  selftest=pass=114,fail=0`, rc 1 — moving the export alone breaks three git-reading pins outside the repo; conform-only
  `kill_residue=12478 relocated=met reloc_mismatch=0 classified=bad selftest=pass=114,fail=0`, rc 1 — the path fix alone
  makes the relocated run green and leaves the residue and the classes; class-only `kill_residue=1 relocated=unmet
  reloc_mismatch=2 classified=ok selftest=pass=118,fail=1`, rc 1 — classes without the scratch move leave the export in
  the repo; always-env `kill_residue=0 relocated=unmet reloc_mismatch=1 classified=bad selftest=pass=118,fail=1`, rc 1 — a
  classifier that says env for everything fails the stale fixtures. Feasibility witness,
  disclosed as built by the L1 and not as the claim's landing (`evidence/control-c1-witness.txt`): `C1=met kill_residue=0
  relocated=met reloc_mismatch=0 classified=ok selftest=pass=119,fail=0`, rc 0. The do-nothing `kill_residue` varies between
  runs (12475–12547 observed; it counts the paths the export had written when the kill landed) and any nonzero value is
  unmet.
- **Controls (C2):** do-nothing unmet on `entry_absent,pins`; the data commit itself reads `failed=entailment` before any
  seat reviews it; `C2_SELFTEST pass=34 fail=0` (`evidence/selftest-c2.txt`) carries the entry-level controls (altered
  quote, quote from the wrong copy, breadcrumb claims, echo claims, unreviewed row, dissent, an L1-authored vote, a vote in
  another directory, a vote on other text).
- **Frontier / assimilation / considerthese / mistake.** Census at round start
  `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → `mori ok`, rc 0, 22 W04 duplicate-URL
  warnings only (`evidence/census-start.txt`); round end `[L1 fills]`. Sourced claim: the five rows opened 2026-10-26.
  Assimilation: none — `merge/mori/` holds no staged entry or row on MemAvailable (`evidence/sweep-memavailable.txt` tail:
  the staged-tree grep returns rc 1, no file). considerthese 2026-10-26 suggestion 1 is implemented inside C1 arm C.
  Mistake mined: the round-49/50 instruments that silently read git objects from the tree they ran in, which the
  relocation witness exposed.
- **Round shape.** One v2 wave `w1` of 68 items, dispatched after the data (`w1-spec.json`, `w1-dispatch.json`,
  `w1-validate.err` empty and the dispatch commit records `v2 validated rc 0`): inside the contract band 64–128, inside the routed 100-seat ceiling, total
  round seats 68 <= 128, and the L1 held the planner seat. Reports at settle and results path:
  `[L1 fills: N of 68 reports on disk, w1-results.json path.]` What the wave added beyond its votes:
  `[L1 fills: QUALITY criteria numbers, lesson path, README/SKILL cells, any draft it integrated.]`
- **Routed defects (round-50 spot-check §5):**
  1. `.scratch` producers — **closed at data for the two named instruments**: `tools/mori-pin-check.py` v5 writes its
     `--rev` tree as a `git clone --shared` under `--scratch`/TMPDIR and `.ufo/waves/round-40/conform.py` derives its lane
     and uses TMPDIR; measured by C1 arms A and B (at-data line above). After-value and the round-38 residue noted below:
     `[L1 fills.]`
  2. Round shape — **met**: one wave, 68 seats, after the data, within both ceilings; no amendment was needed because the
     frozen contract already specified one v2 wave. The final disposition of the 35 round-50 attempt-1 seats that never
     reported: `[L1 fills — no disposition artifact was in the round-51 tree when this entry was drafted.]`
  3. Successor calibration counter and K4 beyond `SHONEN.md` — **not done this round.** Both stay routed to round 52. This
     is a named deviation under routed defect 5, recorded here rather than dropped silently.
  4. C2 entailment — taken as the entailment arm of P-C2, not as a separate instrument. At the data commit the claim is
     unmet on that arm alone (`entailed=0 dissent=0 failed=entailment`); the wave's recorded judgments:
     `[L1 fills: entailed=N dissent=N and whether any overclaim forced a claim-text replacement (new hash).]`
  5. Contract deviations in the record — this entry names the only deviation known at draft time (item 3 above), and the
     named limits live in `SCORECARD.md` `## Round 51`. `[L1 fills: any further deviation the wave's reviewers found.]`
  6. Fleet-owned author date — `scripts/hyaku/fleet-commit.sh:84-85` (`jj metaedit --update-author`) is the operator's and
     the lane cannot fix it; the filing commit's author date versus the lane tip is the operator's to check:
     `[L1 fills: the filing commit and its author date.]`
- **Correction:** none.
- **Not done, stated:** the successor C1 counter and K4 beyond `SHONEN.md` (routed to round 52); the lane-resident scratch
  producers of `.ufo/waves/round-38/count-c1.py:992` and `.ufo/waves/round-38/conform.py:38`, which are outside C1's two
  instruments and were observed writing under `.ufo/waves/round-38/scratch/` during `w1`; `[L1 fills: anything the wave
  leaves open.]`
```

---

## Draft B — SCORECARD.md `## Round 51` section (append after the Round 50 section)

```markdown
## Round 51 — pin re-execution that leaves no residue and says why a pin failed (C1) and MemAvailable as the kernel's estimate (C2)

L1 MoriR51, attempt 1. Entering tip `aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd`; freeze
`4677910eae6df3dabd38fe9a0daf1945146a1110` (`.ufo/waves/round-51/contract.md`; both counters, the controls, the
receipts and the five source copies committed before any seat); data `87e0c374537557754bf71dd68036ded3ddc6699c`. One v2
wave `w1` (68 seats) ran after the data. Scores entering: coverage 6, operability 7, depth 5, freshness 5, calibration 5,
adjacency 6; both claims work a lowest (tied 5) axis (C2 depth, C1 operability). No score change is claimed by the lane;
the non-author closure rules.

| Claim | Axis (held) | Counting command | Before | After |
|---|---|---|---|---|
| C1 pin re-execution is hermetic (no residue in the repo it reads, runs with the lane path hidden) and every mismatch says `class=env` (could not run here) or `class=stale` | operability 7 | `python3 .ufo/waves/round-51/count-c1.py R [--scratch DIR]` | `C1=unmet kill_residue=12547 relocated=unmet reloc_mismatch=1 classified=bad selftest=pass=114,fail=0 rev=aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd failed=kill_residue,relocated,classified`, rc 1 — `evidence/control-c1-do-nothing.txt` | `[L1 fills: C1=met … at the landed tip, rc 0 and receipt path.]` At the data commit: `C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=119,fail=0 rev=87e0c374537557754bf71dd68036ded3ddc6699c failed=-`, rc 0 — `evidence/c1-at-data.txt` |
| C2 what `/proc/meminfo`'s MemAvailable is at kernel v7.2 — the estimate, its formula and what it leaves out; 21 located quotes over 5 sources (FR: resource runway) | depth 5 | `python3 .ufo/waves/round-51/count-c2.py R` | `C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=bad provenance=bad entailed=0 dissent=0 rev=aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd failed=entry_absent,pins`, rc 1 — `evidence/control-c2-do-nothing.txt` | `[L1 fills: C2=met claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=N dissent=0 at the landed tip, rc 0 and receipt path.]` At the data commit: `C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=87e0c374537557754bf71dd68036ded3ddc6699c failed=entailment`, rc 1 — `evidence/c2-at-data.txt` (located quotes without a recorded non-L1 entailment judgment do not meet P-C2) |

The C1 landing is `tools/mori-pin-check.py` v5 (the `--rev` measured tree is a `git clone --shared --no-checkout` checked
out detached at R under `--scratch`, default TMPDIR, never `<repo>/.scratch`; every mismatch line ends `class=env` or
`class=stale`; the summary ends `env=N stale=N`; five new selftest arms, 114 → 119) and `.ufo/waves/round-40/conform.py`
(`LANE` derived from its own path, selftest scratch under TMPDIR). The pin cells that name those tallies were updated with
the change: `SKILL.md`'s registry row and `SHONEN.md`'s "executable without oral context" line now pin `pass=119` with the
round-51 receipts. The C2 landing is `corpus/knowledge/memavailable-estimate-r51.md` with rows S492–S496 (opened
2026-10-26) and the five copies under `corpus/evidence/sources-r51/`; registry rows 264 → 269.

Controls that skip the work stay unmet (all receipts under `.ufo/waves/round-51/evidence/`, scored by the frozen counter
before data): C1 do-nothing `kill_residue=12547 relocated=unmet reloc_mismatch=1 classified=bad selftest=pass=114,fail=0`
rc 1; scratch-only `kill_residue=0 relocated=unmet reloc_mismatch=3 classified=bad selftest=pass=114,fail=0` rc 1 (moving
the export alone breaks three git-reading pins outside the repo); conform-only `kill_residue=12478 relocated=met
reloc_mismatch=0 classified=bad selftest=pass=114,fail=0` rc 1 (the path fix alone leaves the residue and the classes);
class-only `kill_residue=1 relocated=unmet reloc_mismatch=2 classified=ok selftest=pass=118,fail=1` rc 1; always-env
`kill_residue=0 relocated=unmet reloc_mismatch=1 classified=bad selftest=pass=118,fail=1` rc 1 (a classifier that says
env for everything fails the stale fixtures). Feasibility witness disclosed as built by the L1, not as the claim's landing
(`control-c1-witness.txt`): `C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok
selftest=pass=119,fail=0`, rc 0. C2 controls: do-nothing `entry_absent,pins`; the data commit itself `failed=entailment`;
entry-level selftest `C2_SELFTEST pass=34 fail=0` (`evidence/selftest-c2.txt`).

### capabilities: demonstrated round 51

| Capability | What it can now do | Evidence | First-working round |
|---|---|---|---|
| classed pin mismatch | say, per mismatching pin, whether the pinned command could not run here (`class=env`) or ran and disagreed (`class=stale`), with `env=N stale=N` on the summary line, so "can't run here" stops reading as "stale" | `python3 .ufo/waves/round-51/count-c1.py 87e0c374537557754bf71dd68036ded3ddc6699c` arm C (`class=env` on the two no-tally pins, `class=stale` on the different-tally and rc-contradicting pins, ` env=2 stale=2`); selftest arms `v5_class_env_setup_error`, `v5_class_env_timeout`, `v5_class_stale_tally`, `v5_class_stale_digest` | 51 |
| hermetic `--rev` re-execution | measure a revision in a `git clone --shared` under `--scratch`/TMPDIR, so a killed or completed run leaves nothing in the repo it reads and a run with the lane working tree hidden still reconciles | `python3 .ufo/waves/round-51/count-c1.py …` arms A (`kill_residue=0`) and B (`relocated=met reloc_mismatch=0`) at the data commit; selftest arm `v5_rev_export_outside_repo` | 51 |

### Round 51 measured outcome (appended after wave w1; the tables above are the declaration)

| Claim | After (measured at the landed tip) | Verdict proposed for the closure |
|---|---|---|
| C1 | `[L1 fills: the C1 line at the landed tip and its receipt path.]` | `[L1 fills: the closure's verdict, with the named limits below.]` |
| C2 | `[L1 fills: the C2 line at the landed tip including entailed=N dissent=N and its receipt path.]` | `[L1 fills: the closure's verdict, with the entailment limit below.]` |

Limits named before data (nothing below is a counter change; each is a named limit of the frozen predicate): C1 arm A kills
at one moment (3 s after the first write) and proves nothing about a kill at another moment; arm B hides one path (the
lane) and does not prove portability to another host, user or kernel; arm C's fixture is five rows and its rule is "no tally
line ⇒ env", so a tool that prints a tally and then fails for an environmental reason is classed stale; the counter trusts
bubblewrap's mount namespace and checks only that `<lane>/SKILL.md` is invisible inside it; `--root` mode still writes temp
dirs under `<root>/.scratch` (unchanged, not claimed); the counter has no selftest mode of its own, so its arms are
exercised only through the five controls. C2: a located quote proves the words occur; an
`entailed` vote proves a non-L1 wave seat recorded that judgment for that exact text, not that the judgment is right; v7.2
code says nothing about other kernels; no host meminfo value is claimed as typical; `totalreserve_pages` is not exported as
one line, so the estimate cannot be recomputed exactly from `/proc/meminfo` alone. Cross-instrument limit observed during
the round: two other lane instruments still write scratch inside the lane — `.ufo/waves/round-38/count-c1.py:992`
(`mori-c1-tool-*`) and `.ufo/waves/round-38/conform.py:38` (`mori-conform-selftest-*`) — and one such directory was present
untracked in the working tree at the time of this draft; C1 fixes only the two instruments its predicate names.

Planned (round 52): the successor C1 counter (the named survivors: verdict-word substring, a second `## Axes`, the unread
Score column, the vacuous `admitted` arm, a symlinked pin path) and K4 beyond `SHONEN.md` — tally pins in `QUALITY.md`,
`README.md` and `LOG.md` — which this round does not claim; the relocation sweep of the remaining lane-resident scratch
producers; whatever the closure rules on the wave's residues.
```

---

## Findings

1. **MED — routed defect 2 is only half discharged: the 35 round-50 attempt-1 seats with no report have no disposition.**
   `corpus/lessons/round-50-verifier-spotcheck.md:177` (defect 2) asks for "a final disposition for the 35 attempt-1 seats
   with no report". The round-51 tree carries none: `grep -rn "35" .ufo/waves/round-51/contract.md` → no match, and no file
   under `.ufo/waves/round-51/evidence/` names them. Both drafts mark the point `[L1 fills]`; if the record is to be
   truthful, the L1 must either write the disposition (late, dead, unknown as a class) or keep the `[L1 fills]` marker open.

2. **MED — lane-resident scratch producers remain outside C1's two fixed instruments, and one wrote during this wave.**
   `.ufo/waves/round-38/count-c1.py:992` (`tool_dir = tempfile.mkdtemp(prefix="mori-c1-tool-", dir=_scratch_parent())`) and
   `.ufo/waves/round-38/conform.py:38` (`SCRATCH_ROOT = os.path.join(LANE, ".ufo/waves/round-38/scratch")`) still write
   under the lane; `.ufo/waves/round-38/scratch/mori-conform-selftest-8k8u7zky/` carries mtime `19:49:45` on 2026-10-26
   (observed live while `w1` ran), and empty `c1-*` / `mori-c1-tool-*` dirs from 2026-10-24 remain.
   `git status --porcelain --ignored` shows `?? .ufo/waves/round-38/scratch/mori-conform-selftest-8k8u7zky/`. C1's
   `kill_residue=0` is about the repo the *pin check* reads and says nothing about these; routed defect 1's text covers
   only `tools/mori-pin-check.py` and the round-40 `conform.py`. Relevant to the contract's "relocation sweep of the other
   host-path instruments" build item and to the L1's pre-report cleanup.

3. **LOW — the round-51 selftest receipts record a working-tree run, not a run on committed bytes.**
   `.ufo/waves/round-51/evidence/selftests/mori-pin-check.txt:1` and `mori-unlanded-check.txt:1` both read
   `$ TMPDIR=<scratch> python3 tools/… --selftest   # working tree after the round-51 C1 data edit, run 2026-10-26` — no
   revision and no digest. `SHONEN.md:7` pins `(119/119)` to those receipts. Round 50's receipts ran on a `git archive` of
   the freeze revision (`corpus/lessons/round-50-verifier-spotcheck.md` §1). The numbers are consistent with the committed
   tool (`PIN_CHECK_SELFTEST pass=119 fail=0` at `evidence/selftests/mori-pin-check.txt:122`), but a reader cannot
   re-derive the pin from the receipt alone.

4. **LOW — `count-c1.py` has no self-check mode.** Its CLI is `rev [--repo] [--hide] [--scratch] [--keep]`
   (`grep -n add_argument .ufo/waves/round-51/count-c1.py` → five options, no `--selftest`), so the harness that scores C1
   is exercised only through the five control receipts. Draft B states this as a named limit; no counter change is
   proposed (frozen).

5. **LOW — wording risk in the C1 "classified" arm.** At the data commit the receipt's `classified: PIN_CHECK=unmet …
   mismatches=4` line is the five-row fixture registry, not the lane's own `SKILL.md`. Both drafts say so explicitly; a
   reader who takes `C1=met` to mean `PIN_CHECK=met` on the lane tree would be wrong.

6. **LOW — mid-wave untracked files must be gone before the report is filed.** `git status --porcelain --ignored` at draft
   time lists `?? .ufo/waves/round-51/w1.ready`, `?? .ufo/waves/round-51/w1.ready.dispatched`, `?? .ufo/waves/round-51/w1/`
   (the wave's own reports) and the finding-2 scratch dir. `tools/mori-unlanded-check.py` is the lane's own gate for this;
   the L1 integrates `w1/` and should remove the two `w1.ready*` markers.

7. **LOW — the census after-value does not exist yet.** `evidence/census-start.txt` is the only census receipt (`mori ok`,
   rc 0, 22 W04). The contract's round-end census is unfilled, so both drafts carry `[L1 fills]` and no after-warning count
   is asserted here.

8. **INFO — the registry-row delta (264 → 269) is this seat's count, not a receipt.** `git show
   aa3af1ec…:corpus/SOURCES.md | grep -cE '^\| S[0-9]+ '` → 264; the working tree at the data state → 269; the five new rows
   are S492–S496. No counter checks this number, and the drafts state it as a count.

9. **INFO — no product code, counter, contract file, SKILL/SHONEN/corpus/QUALITY/LOG/SCORECARD file was touched by this
   seat.** The only file written is this report. Scratch `/fast/scratch/hyaku/mori-r51/Mo51ScribeLogScorecard/` was created
   and removed (empty; no clone, no fixture, nothing to copy). No tool was installed or upgraded, so there is no tool row
   to record. Lane git state was read only (`show`, `diff`, `log`, `status`, `rev-parse`); no jj command ran.

10. **INFO — conflicts to report verbatim for the canonical judge.** None found between the contract and the receipts: the
    do-nothing `reloc_mismatch=1` and `kill_residue=12547`, the at-data `kill_residue=0`/`classified=ok`, and the
    `selftest=pass=119` all match `contract.md`'s filled table and the quoted receipts line for line. The only variance is
    the one the contract itself names: the do-nothing `kill_residue` count ranges 12475–12547 between runs.

Report: .ufo/waves/round-51/w1/Mo51ScribeLogScorecard.md
