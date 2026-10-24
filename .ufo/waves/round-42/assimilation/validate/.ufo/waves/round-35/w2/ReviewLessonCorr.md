measured 2026-10-23T09:27:05Z

# ReviewLessonCorr — falsify corpus/lessons/round-35.md at cedb0ec4f3a4f672804deac388b7191258f01fcd

Scope: the round-34.md:46 correction (lines 42-46), the S182/S193 old->new log (lines 32-40), the
routed-defect outcome table (lines 48-58) and the Mistakes table (lines 60-66). Method: read-only git
on the lane at the frozen rev; check/counter reruns in scratch clone
/fast/scratch/hyaku/mori-r35/MoriR35.ReviewLessonCorr/clone (git clone --no-hardlinks of the lane);
upstream fetches by curl only. LSP: no server answers these md/py lane files; findings are literal
text evidence, not semantic proof.

## Corrections section (lesson :42-46)

VERDICT: supported — `round-34.md:46` resolves exactly: `awk NR==46` of corpus/lessons/round-34.md@cedb0ec is the line starting `supported. No status or recheck cell of an existing row changed.` and the quoted sentence appears verbatim there.

VERDICT: supported — the sentence is literally true: per-commit column diff over all three round-34 commits touching corpus/SOURCES.md (8d56809a, ff334073, 406d91a4, confirmed by `git log -- SOURCES.md` at dd76eb79) changes only cells anchor (col 5), teaches (6) and used-by (10); no status (7), recheck (9) or any other cell of a pre-existing row moved.

VERDICT: supported — and it is misleading: 8d56809a changed S182's anchor and used-by in place, 406d91a4 rewrote S193's anchor and teaches in place (verified row-level diffs). Fleet `CORPUS.md` §SOURCES.md rule 2 at /home/vgpnk/Projects/shokunin HEAD:116 reads Append-only: only status, recheck and used-by change in place; so both edits violated the frozen rule. QUALITY.md@cedb0ec:373-374 (item 81) restates it.

VERDICT: supported — S182/S193 are now superseded by S201/S202: SOURCES.md@cedb0ec:207-208 rows S201/S202 carry teaches opening `supersedes S182 —` / `supersedes S193 —`; S182/S193 themselves are left as they stand (line 188 anchor still contains the round-34-added 485-486,512-518,620-623 lines; line 199 keeps the rewritten anchor/teaches).

## S182/S193 old->new log (lesson :32-40)

VERDICT: supported — `Row changes logged old->new this round: none`: `git diff dd76eb79 cedb0ec4 -- corpus/SOURCES.md` is 6 insertions, 0 deletions (the six S199-S204 rows, ids confirmed present).

VERDICT: supported — S182 anchor old `block/genhd.c:1353,1371-1374,1395,1403,1418-1425 (diskstats_show, diskstats_op, proc_create_seq); tag v7.2` -> same plus `; 485-486,512-518,620-623 (__add_disk parent, holders and slaves directories, device_add_disk)`: byte-faithful to the -/+ rows of `git show 8d56809a -- corpus/SOURCES.md`.

VERDICT: supported — S193 anchor `...:3508-3510,3542-3543; tag v7.2` -> `...,4653-4657; tag v7.2` and teaches old->new (add/delete parent+partition sentence -> plus reparent `device_move` clause with no partition check): byte-faithful to `git show 406d91a4` diff.

VERDICT: supported — the added S182 lines rest on S201: S201's anchor is exactly `block/genhd.c:485-486,512-518,620-623 (__add_disk, device_add_disk); tag v7.2`; S202's anchor covers 4653-4657 and 4704-4706 behind the S193 reparent clause.

VERDICT: supported — lesson :14 claim used by the log: no corpus/evidence/sources-r35/S201.src or S202.src exists (`git cat-file -e` fails on both); committed corpus/evidence/sources-r33/S182.src sha256 8c2faa15…d39a5 and sources-r34/S193.src fa223c8f…1c9fa are byte-identical to live `https://raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c` and `.../drivers/base/core.c` (curl sha256 match), matching the gate-table hashes for S201/S202. `8d56809a`, `406d91a4`, `ff334073`, `dd76eb79`, `721040a9`, `913df22e`, `d677cf3` all resolve to commits whose subjects match their descriptions.

VERDICT: unsupported — the no-row enumeration in lesson :25-30. The committed sweep `.ufo/waves/round-35/w1/SrcDmStack.md` opened `Documentation/admin-guide/md.rst` (:72, sha-pinned, no stating sentence) and sysstat `README.md` (:53, sha-pinned) this round; the lesson names neither. The named list omits two opened files, so the bullet list is incomplete. `Identified 12, included 0` is only consistent if the 12 are the no-row files: 10 named + md.rst + README.md = 12 (opened files total 14 including the two S203/S204 rows; md.c is a prior-round citation, sysfs-block a 404). The count can be reconciled; the enumeration cannot. Minor completeness defect, not a correctness one: the missing files are still reject-evidence for the same claim.

## Routed-defect outcome table (lesson :48-58)

VERDICT: supported — item 1: corpus/lessons/round-34-verifier-spotcheck.md:96-104 records 98 not answering the reader-action clause of round-33 §8 item 1 (round-33 spot-check :226-228); QUALITY.md@cedb0ec:779-787 (item 100) requires verdict cells to name a reader action; fleet MANIFEST rounds[524] keeps round 34 `rejected-honest-stop`; the counter counts missing and extra/bad arms (count-c1.py:17-20,115-150) = two-sided bounds.

VERDICT: supported — item 2: `.ufo/waves/round-35/check-sources-appendonly.py` exists at cedb0ec and enforces the rule (COMPARE = all cells but status/recheck/used-by, supersedes-discharge); QUALITY 102 (:799-808) records it; the round-34.md:46 correction is present in this file (:42-46).

VERDICT: supported — item 3: corpus/knowledge/disk-write-rate-r33.md:100-108 carries the append-only Round-35 correction naming committed `wa/JudgeRow3r.md`, `JudgeRow6r.md`, `JudgeRow7r.md`, `JudgeRow13r.md`, `wb/ReJudgeRow{3r,6r,7r,13r}.md` and `wb/residual/MoriR34A3.JudgeRow3r2.md`; all exist in the cedb0ec tree; `.ufo/waves/round-34/` has no `w1/` entry (dangling pointer confirmed by ls-tree).

VERDICT: supported — item 4: SKILL.md:834 is the stacked-device clause; :844-853 Round35 corrections mark it miscited/observed-not-sourced and keep S203/S204 as rejected rows; SrcDmStack VERDICT: fails.

VERDICT: supported — item 5: QUALITY.md:769-778 is the append-only 98 correction itemizing D1, D2, D4 exactly as the table says.

VERDICT: supported — item 6 left alone: `git show dd76eb79:LOG.md | awk NR==1801` is byte-identical to cedb0ec:1801 (the async.maxJobs operator line); `refs/jj/keep/3b19cacb0444e799b4685e4bb8e8d76fbb51104a` exists in the lane; SHONEN.md untouched this round (nothing in the dd76eb79..cedb0ec SOURCES diff or lesson claims otherwise).

VERDICT: supported — axes row: SCORECARD.md:11 names old value `round 28` then `round 31 (improved, score held)`; :12 names `round 12` then `round 31`; fleet MANIFEST rounds[495] is the admitted round-31 closure grading depth+operability improved; rounds 32/33/34 (498,504,524) all rejected-honest-stop, so round 31 is the latest admitted closure grading each improved; round-31-verifier-spotcheck.md:154-155 grades depth and operability improved; `.ufo/waves/round-35/w1/AxesOracle.md` exists.

## Mistakes table (lesson :60-66)

VERDICT: supported — M1: evidence/c1-controls.txt@cedb0ec records 10c CtlSkipDesign B (empty capability/what cells) and 9d CtlDangling D (unbackticked path prose) both `C1=met exit 0` with the residual ruling; contract.md@cedb0ec:79-93 controls list names no server-echo, observed-column-copy, no-decision, rule-changed or denial control (QUALITY 98's shapes at :715-717); QUALITY 98:722-723 says a met control means the counter or target is wrong; kaidoku-shokunin/corpus/lessons/round-32-verifier-spotcheck.md:76 (denial scored equal to repair breaks calibration) and :116 (require denial controls scored before data) back the denial-control requirement; QUALITY 101 (:788-798) is the fix and is shown able to fail on 10c.

VERDICT: supported — M2: rerun in scratch clone: `python3 check.py dd76eb79 --repo clone` exits 1, `appendonly_violations=17` including S182 (changed_at 8d56809a) and S193 (changed_at 406d91a4); at cedb0ec exits 1 with `appendonly_violations=15`, S182/S193 discharged by the S201/S202 supersedes rows; the 15 remaining changed_at are 62db24c0/5126891f/ab8f4cfe — all round-32/33 commits, i.e. edited in place before round 34, consistent with `routed`.

VERDICT: supported — M3: SCORECARD.md:586-592 at cedb0ec still shows `## Capabilities` + `| — none yet — |` (contract-field scaffold added at d677cf3, confirmed `git show d677cf3:SCORECARD.md`); per-round tables exist instead (verified); `.ufo/waves/round-35/w1/RevengerNoneYet.md` exists and documents this; rerun `python3 count-c1.py dd76eb79 --repo clone` -> `matched=0 missing=18 bad=0 extra=5 mismatches=23 C1=unmet`, exit 1, exactly the fix cell's `count-c1.py dd76eb79 -> mismatches=23 C1=unmet`.

## Auxiliary pointers/hashes (all resolve)

- count-c1.py@cedb0ec sha256 = 27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167 = frozen; f2d28711 and 913df22e resolve and their subjects match; contract.md exists.
- Committed source hashes match gate table prefixes exactly: S199.src 04ea5c9e…7d993, S203.src c84b28a2…7681b8e, S204.src b01ff2d6…bab8b02b; S200's git-show bytes hash to 0b414b8a…ae9952 (fleet MANIFEST.json@37b51a24); fleet MANIFEST has 525 rounds, [524] = round-34 rejected-honest-stop, [313].capabilities_added[0] = sources-registry (34 rows; census clean), 13 admitted mori entries carrying capabilities.
- SCORECARD last `## Capabilities` at :1941 holds 18 `rounds[i].capabilities_added[j]` rows (:1961-1978) and declares itself the current self-assessment superseding the `— none yet —` table.
- dd76eb79 is an ancestor of cedb0ec (merge-base check); dd76eb79 subject is the round-34 verifier spot-check.

## Residual risk / gaps

- w1/ file contents for AxesOracle.md, Skill834.md, QualClause2.md, QualQ98Corr.md, MineAppendOnly.md spot-checked for existence, not audited line-by-line.
- Disks.html/dm.c/AXES.md upstream bytes not re-fetched (committed srcs carry the matching sha values).
- No installs. Scratch clone + coldiff.py + copied counter/check under /fast/scratch/hyaku/mori-r35/MoriR35.ReviewLessonCorr/ only.
