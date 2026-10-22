Verdict: **defect found.** A1 bullet 3a holds an undisclosed relaxation that C1=met depends on. A3 is a narrowing made after the data, and its disclosure is incomplete in three places. Every A2 bullet is harder or clarifying, but A2's "before the data" claim does not hold for the allowlist.

# CriticAmendments — round 30 wave 2 (MoriR30.CriticAmendments)

Attacked: the contract's amendments A1–A3 (`.ufo/waves/round-30/contract.md:122-222` at `ad0f0474`). Everything here was
re-derived from committed bytes, and the counters and gates were run from their commit blobs inside the lane (read-only
git only). I did not trust any author receipt. No tools were installed or updated. Scratch:
`/fast/scratch/hyaku/mori-r30-w2/CriticAmendments/` holds the gate blobs, the counter blob, two one-line mutants and a
sandbox clone.

## 1. Timeline (`git log --format='%h %cI' 58b61681..ad0f0474`; all times −03:00, plus internal UTC stamps)

| time | commit / event | relevance |
|---|---|---|
| 18:08:28 | `a66751b` contract | the original rules |
| 18:11:50 | `e936482` wave-1 dispatch | every `CaseR30a-d` task starts with `/skill:godspeed`; the wave context says "read /home/vgpnk/.omp/agent/RULES.md first" (`wave1-dispatch.json` context and tasks[0..3]) |
| 21:12:02Z–21:23:00Z | source fetches by the Src* seats; DraftEntryC1 fetches 21:16:16Z–21:17:20Z | internal stamps in `w1/Src*.md` and `w1/DraftEntryC1.md` (committed later, in `6c47dd0`) |
| 18:15:51 | `b039dd4` writer reports CaseR30a-d **and ProbeC1Cases** | ProbeC1Cases `:11-29` is a ready-to-paste 13-row C1 decision table |
| 18:19:42 | `05db57e` **A1** | 3m51s after a C1 row draft was in the lane |
| 18:22:16 | `3767108` **A2** | 6m25s after the writer reports; committed together with CriticC2Design, which read their files-opened lists |
| 18:32:49 | `32e287f` gate (A2 version, blob `893e69d`) | |
| 21:33:43Z | A2 gate run on the writer wave (`evidence/gate-a2-prefreeze.txt:1`) | **the data seen** |
| 18:33:54 | `55f9a69` **A3**, gate blob `dbcbe50` | 11 s after that run |
| 18:48:00 | `8ac9535` C2 counter | |
| 18:48:21 | `db1ec46` freeze; gate blob still `dbcbe50` (`git rev-parse db1ec46:…check-blind-wave.sh`) | A3 is the counted gate |
| 18:52:41 | `6c47dd0` C1 counter (sha256 `6d825e1e…`, recomputed: matches) | |
| 18:58:39 | `ee61010` entry, excerpts, SOURCES S156-S160, SKILL rows | first commit of the counted C1 data (`git log --reverse --diff-filter=A`) |

Strict commit order: A1 comes before the C1 counter and before the entry and excerpts. A2 comes before the gate, the
counter and the freeze. A3 comes before the counter and the freeze. All three statements hold. The questions below are
about what each amendment's author had already seen.

## 2. A1, bullet by bullet

| bullet | class | evidence |
|---|---|---|
| 2a distinct | harder | adds pairwise distinctness and requires at least 2 verdicts |
| 2b scope content | harder | forced 6 of ProbeC1Cases' 13 ids to change (diff of the probe ids against entry `:95-107`) |
| 2c syntax | clarifying (one formatting relaxation: a backticked verdict cell is allowed); the `, ` separator and typed compare are harder | `contract.md:132-135` |
| 3a tool blob | formally narrower, no effect at the tip | see F3 |
| **3a duplicate ids** | **narrower (relaxation), load-bearing** | see F1 |
| 4a novelty, 4b binding, 4c grammar | harder or clarifying | `:139-145` |
| 5a SKILL rows | formally a different test, not a superset of the original; no effect at the tip | see F3 |
| 1a header, Provenance (F17), Separability | harder | `:147-152` |

## 3. A2, bullet by bullet

All harder or clarifying when compared with `a66751b`: gate exercised with `scanned=k`; allowlist (looser than its
source's version-pinned prefixes at CriticC2Design `:80-82`, but stricter than the original "public upstream earlyoom
and systemd sources"); freeze identification; tool run order; no change to shape verdicts; shape tightened (S1);
undecided pins as a miss; two judges; the residual-fix bound; authorship; counters from blobs; disclosure; C1 parse
rules. None of them relaxes a condition of the original. The authorship dual form is load-bearing: two of the eight
frozen cases carry `"author": "MoriR30.CaseR30c"` (`db1ec46:tools/fixtures/mori-oom-killers/cases-a2-r30.json`).
CriticSizing derived that dual form from the brief text before any data existed (`w1/CriticSizing.md:113-125`), and the
original contract had no author-key check at all, so it is harder. See F7 for A2's timing claim.

## 4. Findings

### F1 (high; attacks A1 bullet 3a; axes: depth, calibration). The duplicate-id clause relaxes condition 3, and C1=met depends on it

- The original condition 3 reads "Every row's case id exists in **exactly one** of `cases.json`,
  `cases-supplementary.json`, `cases-a2.json`" (`contract.md:32`). A1 3a adds: "A case id may occur in more than one
  eligible file only when every copy's `inputs` and `expect` are identical" (`:137-138`).
- A1's preamble says "nothing is narrowed" (`:124`). Its own source calls the original rule unambiguous and harmful to
  these rows. CriticC1Design F12: "'exactly one of' silently excludes the scope-boundary cases … `c02-…`, `c03-…`,
  `c04-…` … a correct entry citing them is unmet" (`05db57e:.ufo/waves/round-30/w1/CriticC1Design.md:139-143`). That
  is a relaxation, not a format ambiguity.
- It was written after the row data existed. ProbeC1Cases, committed at `b039dd4` before A1, already cites `c03` and
  `c04` in its ready-to-paste table (`ProbeC1Cases.md:16,18`).
- It is load-bearing. Entry rows `:95-97` cite `c03`, `c02` and `c04`. All three ids are in both `cases.json` and
  `cases-supplementary.json` at `58b61681`, with identical inputs and expect (my python check: 29 of 65 pool ids sit in
  more than one file).
- Counter blob `6c47dd0` at `ad0f0474`: `rows=13 rows_ok=13 … C1=met`, exit 0.
- Scratch mutant that adds only `len(copies)!=1` at `count-c1.sh:170` (the original "exactly one of"):
  `case=c03-… case_ok=bad`, `case=c02-… case_ok=bad`, `case=c04-… case_ok=bad`, `rows_ok=10`, `C1=unmet`, exit 1.
- Smallest safe correction: append an A1 disclosure stating that 3a's duplicate-id clause relaxes condition 3, was
  written after ProbeC1Cases' rows, and is load-bearing for three rows. The closure then judges C1 on the original
  condition 3 (unmet as landed). It may accept the relaxation only as an explicitly admitted tradeoff. By the
  contract's own rule ("A declared claim is never withdrawn or narrowed", `contract.md:5`), the canonical judge should
  reject it.

### F2 (medium; attacks A1's heading "before any entry, row or excerpt is committed"; axis: calibration). False provenance wording

- A 13-row decision table (header `shape | verdict | fields | case | sources`) was committed at `b039dd4`
  (`ProbeC1Cases.md:11-29`) before A1.
- The Src* source fetches began at 21:12:02Z, and DraftEntryC1's fetches ran 21:16:16Z–21:17:20Z. Both predate A1
  (21:19:42Z).
- A1 was calibrated with that data in hand: "eligible pool with two or more version lines is exactly 8" and
  "DraftEntryC1 does not cite c02-c05" (CriticC1Design `:144`, `:149`; see also `:48`).
- Apart from F1, the bullets made C1 harder against that draft (6 of 13 ids changed), so this is wording, not
  tailoring. Correction: restate the heading as "before the C1 counter and before the entry, its excerpts and SKILL
  rows; after the ProbeC1Cases draft table".

### F3 (low; attacks A1 3a tool swap and 5a). Formal narrowings with no effect at this tip

- **3a tool swap.** A1 replaces "the tool at `<rev>`" (`:35`) with the entering-tip blob.
  - The tip tool on the entering-tip blobs prints `PASS 32/32` (`cases.json`), `PASS 32/32` (`cases-supplementary.json`)
    and `PASS 30/30` (`cases-a2.json`) (my runs of `ad0f047:tools/mori-oom-killers.py --selftest --cases …`).
  - Row `:101` cites `a2-06-inactive-earlier-invocation-sends-acted`, one of the two older cases whose output the fix
    changed (`evidence/c2-differential.txt:3`). The changed fields (`dryrun_send_lines`, `grammar`,
    `process_group_lines`, `version`) are not among the row's pins (`earlier_invocation_send_lines=3`,
    `state="inactive"`), so the row still holds.
- **5a SKILL rows.** The original requires rows "containing `Round30` and the entry's path" (`:43`). The counter checks
  only heading, basename and case id (`count-c1.sh:224-226`).
  - All 4 rows under `## Round30` (`SKILL.md:752-755`) contain both `Round30` and
    `corpus/knowledge/earlyoom-invocation-scope-r30.md` (my per-row grep).
- No correction is needed for C1 at this tip. A1's "nothing is narrowed" should name both.

### F4 (high; attacks the completeness of A3's disclosure; axes: operability, calibration). The A2 gate masked a non-host-file hit, and A3 does not cure it

- The gate records only the **first** forbidden files-opened line per report. `files_forbidden_seen` guards the capture,
  and one violation is emitted per file (gate blob `dbcbe50`, `check-blind-wave.sh:129-131,159-160`; the A2 blob has the
  same logic).
- A2 blob run in the lane at `db1ec46`: `scanned=4`, `blind_violations=4` (a:96, b:116, c:79, d:110). This matches
  `gate-a2-prefreeze.txt:3-8`.
- My every-hit scratch mutant of the A2 blob finds **six** lines: CaseR30a `:96`, `:97` and `:105`, b `:116`, c `:79`,
  d `:110`. CaseR30a `:105` is the closing prose sentence ("The scratch JSON passed python3 json.load; …"). It is not a
  host file.
- A3 names only the godspeed path and RULES.md (`contract.md:211-213`) and claims "nothing else changes". The A3 blob in
  the lane at `db1ec46` prints `blind_violations=1` with `CaseR30a.md:105`, and my every-hit mutant of the A3 blob finds
  only `:105`.
- The A3 commit records only the gate self-test (file list of `55f9a69`). No A3-version run on the wave was committed
  before the freeze (file lists of `55f9a69`, `8ac9535`, `db1ec46`). A3's sentence "the closure judges whether C2.4
  stands on the A3 version or misses on the A2 version" (`:221`) suggests A3 could pass. It cannot.
- Outcome: C2.4 misses on both versions, so the author's C2 miss stands (`evidence/c2-after.txt:19-21`). The uncounted
  A4 diagnostic is correctly kept outside the count.

### F5 (medium; attacks A3's statements "the A2 allowlist omitted" and "bound before it ran on the round's own inputs"; axis: calibration). An on-hand warning is not disclosed

- CriticC2Design, committed **in A2's own commit** `3767108`, read the writers' files-opened lists (`:7`). It proposed an
  allowlist that included `/home/vgpnk/.omp/agent/RULES.md` and "skill files" (`:80-81`). It stated "All four writers
  list the godspeed skill file" (`:86`) and that three of the four omit RULES.md (`:93-94`).
- The round-29 writer reports also list the same godspeed path (`git grep godspeed d6d5cb0a -- .ufo/waves/round-29/w1/`:
  7 writer reports).
- So the omission was made against a warning drawn from this round's own data, not merely "bound before it ran". A3 and
  its `## Mistakes` cause line do not say this.

### F6 (medium; attacks A3's statement "the original contract … forbade only lane files other than rule-text.md"; axis: calibration). The original is misquoted, so A3 relaxes the original too

- The original and current text: writers "read only `.ufo/waves/round-30/rule-text.md` … and public upstream earlyoom
  and systemd sources; they open no other lane file" (`contract.md:81-83`, unchanged since `a66751b`). The writer brief
  says "you may read ONLY" those (`wave1-dispatch.json` tasks[0..3]).
- Both host files fall outside that allowlist. A3 is therefore narrower than the original as well as A2, and it was
  made after data (21:33:43Z run, 18:33:54 commit). Under the contract's no-narrowing rule (`:5`) it is forbidden as a
  counted change.
- Root cause: the L1's own dispatch contradicted the contract from 18:11:50 by injecting `/skill:godspeed` into every
  writer task and telling every seat to read RULES.md.

What A3 states truly (checked):
- It came before the freeze and the counter (timeline).
- The A2 receipt stays committed (`55f9a69`).
- Both paths resolve outside the lane and the fleet repo (`readlink -f` returns the same `/home/vgpnk/.agents/…` and
  `/home/vgpnk/.omp/…` paths).
- Neither file carries rule text, tool source or expected values. I read both: a 16-line posture skill and the
  14-line tooling directive.
- The gate diff adds exactly those two literal paths (`git diff 32e287f 55f9a69 -- …check-blind-wave.sh`: 3 added lines,
  one `case` arm).

### F7 (medium; attacks A2's heading "before the L1 opens any writer report"; axis: calibration). The governed data was already summarized to the L1

- The writer reports were committed at `b039dd4`, 6m25s before A2.
- A2 cites CriticC2Design G1–G4 (`:162-166`). That report carries writer-report data (`:7`, `:83`, `:86`, `:93-94`) and
  shipped in the same commit.
- Whether the L1 opened a report file cannot be falsified from the bytes. The claim that A2 was "before the data" does
  not hold for the allowlist bullet. No A2 bullet is narrower, so this is provenance wording, not a counted defect.
- CriticC2Design F3 (`:99-103`) predicted this class: "the gate is edited to allowlist a path that one writer listed".
  A2's freeze-blob rule closes it only after the freeze, and A3 is the same move made before the freeze.

### F8 (low; side finding on A2's "counters from blobs"). The gate result depends on the checkout path

- `rule_abs` is `$(git rev-parse --show-toplevel)/.ufo/waves/round-30/rule-text.md` (gate `:87`, `:240`).
- Run from a sandbox clone, the A2 blob flags `CaseR30c.md:78`, CaseR30c's absolute lane rule-text path, instead of
  `:79`. Run in the lane it flags `:79`.
- The counted runs are made in the lane, so no counted result changes, but re-runs from a clone differ.

## 5. Smallest safe corrections (L1 appends; nothing below edits earlier text)

1. A1: disclose F1 (load-bearing relaxation; the closure scores C1 on the original condition 3, or explicitly admits
   the tradeoff) and F2/F3 (heading wording and the two no-effect formal narrowings).
2. A3: append a correction naming the masked CaseR30a `:97` and `:105` hits (F4), CriticC2Design G4/G5 (F5) and the
   original allowlist wording (F6). Score C2.4 on the A2 version: a miss, the same outcome as now.
3. Next round (not this one): the gate should emit every forbidden files-opened line, and the allowlist should be run
   on a dry wave before it is bound.

## 6. Checks the main agent should run

- `bash <(git show 6c47dd0:.ufo/waves/round-30/count-c1.sh) ad0f0474…` and the scratch mutant
  `/fast/scratch/hyaku/mori-r30-w2/CriticAmendments/count-c1-exactly-one.sh` (expect met / unmet).
- In the lane: `bash /fast/scratch/hyaku/mori-r30-w2/CriticAmendments/gate-A2-all.sh db1ec46 .ufo/waves/round-30/w1 '^CaseR30[a-d]\.md$'`
  (expect six ALLHIT lines on stderr).
