# Mo87S01Lesson — round-87 lesson scribe, wave w1

round: 87 · attempt: 1 · wave: w1 · lane: mori · seat: Mo87S01Lesson (scribe, leaf — no subagent
dispatch) · date: 2026-11-04
axes: calibration (mined mistake + fixture) and operability (the supersede arms measured able to
fail). Detection and report only; no lane, gate or counter state changed.

Authority read: `.ufo/waves/round-87/contract.md` (frozen, incl. A1), both frozen counters,
`evidence/controls-r87.txt`, `evidence/probe-r87.txt`, `corpus/lessons/round-86-verifier-spotcheck.md`
(`## Routed defects`), `corpus/lessons/round-86.md`, `SCORECARD.md` `## Planned (round 87)`.

## Deliverable state and authorship (read this first)

The lesson file was contested by a live writer. This is the observed sequence, not a reconstruction:

1. **~10:20** — this seat wrote `corpus/lessons/round-87.md` (13,542 bytes): header, `## What the
   round did`, `## Mistakes` with the supersede rule as the mined mistake and a rebuildable fixture,
   and a `## Gate` block stating that no rows were written because
   `.ufo/waves/round-87/gate-input.md` was absent at read time.
2. **728bc5f4** (`round-87: after receipt, S603 + knowledge entry, lesson, QUALITY 181-182,
   SCORECARD and LOG`) — the L1's own 81-line lesson was committed over that path, together with
   `evidence/after-r87.txt` and `evidence/supersede-controls-r87.txt` (sha256 `b9ca89cf…`). This
   seat's draft bytes are in no revision; its distinctive sections are absent from the final file
   (`grep -c` 0 for "Arms shown able to fail", "criterion that should have caught it",
   "predicate-underreach"), so no draft text is claimed as authored.
3. **a42b1d79** (`round-87: lesson integration — the seat's four findings merged (absent-target arm
   defect routed to round 88)`) — the L1 merged four findings this seat had put in its report and
   message into a `## Seat findings merged at integration (Mo87S01Lesson, wave w1)` section.
4. **1523b6cf** (`round-87: lesson — the material C2 falsifier (target reachable with zero
   replays), wording fix, deferred TUF candidate`) — the attribution correction this seat proposed
   landed here (the row now reads "the pre-fix call site on the header-only fixture measured"; the
   `grep -c` at HEAD is 1), and the missing-replay falsifier was added as `## Material attack
   finding`.
5. **a90126ef** (`round-87: lesson — deferred TUF candidate recorded (flip condition for round
   88)`) — the lesson's final observed bytes. `corpus/lessons/round-87.md` is **146 lines**, sha256
   `0060c76f6cccccf3f234345f8bf30b711b67c85a118a0b9c00cc1af5d7299ead`, worktree clean. After it the
   L1 appended contract erratum E1 (`859b7e9a`) and the planned-88 SCORECARD block (`22fa2919`);
   the lesson bytes did not change in either.
6. This seat did **not** edit the committed lesson after the integration and claims no authorship
   of its bytes. Its product is the evidence below plus the four findings, which the lesson carries
   by integration, and the independent reproduction of the material falsifier recorded under
   Findings.

## What this seat measured first-hand

Lane at `b9e6f68d`; scratch `/fast/scratch/hyaku/mori-r87/Mo87S01Lesson`, deleted before yield.
Fixtures are `git clone --shared` of the lane with the toplevel asserted equal to the fixture
directory before the first commit; commits use `-c user.name=t -c user.email=t@t`; fixture commit
ids are fixture-local and the recipes reproduce the readings.

| # | measurement | observed |
|---|---|---|
| 1 | frozen `count-c2.py --selftest` | `C2_COUNTER_SELFTEST pass=17 fail=0`, rc 0 |
| 2 | frozen `count-c1.py --selftest` | `C1_COUNTER_SELFTEST pass=18 fail=0`, rc 0 |
| 3 | fixture A (headers kept, bodies fabricated: `revisions=0→9`, `pointers=266→274`), frozen counter | `C2=unmet … matched=4 defeated=1 superseded=0 legacy=3 unexpected=2 detector=green`, rc 1 |
| 4 | mutation A — drop `name in clean_names` inside `supersede_verdict` (function-level header-only rule): `--selftest` | `FAIL supersede_absent_target`, `FAIL supersede_requires_clean`, `pass=15 fail=2`, rc 1 |
| 5 | mutation A on fixture A | `… superseded=2 legacy=1 unexpected=2 detector=red`, rc 1 |
| 6 | mutation B — `supersede_counts` never supersedes: `--selftest` | `FAIL supersede_counts_positive`, `pass=16 fail=1`, rc 1 |
| 7 | mutation C — the call site passes `set(present)` instead of `clean_names` (the pre-fix state named by the L1's receipt): `--selftest` | `pass=17 fail=0`, rc 0 — **the arms do not see a call-site defect** |
| 8 | mutation C on fixture A | `… superseded=2 legacy=1 unexpected=2 detector=green`, rc 1 |
| 9 | static arm counts, `grep -c 'cases.append('` on committed blobs | r86 counters `15/11/22` at `6fc09d69` → `18/13/23` at `03b66a43`/`98f48dba` — the C1 move |
| 10 | fixture B: both successors keep every header **except** `# replay:`, bodies fabricated; frozen counter | `C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=a54f2ee8178d`, rc 0 — the exact target with **zero** replays of the two successors (`RECEIPT … expect=met met problems=-`, no `REPLAY` line for either) |
| 11 | mechanism, static: the r86 grammar's `missing-replay` problem (`count-c2.py:115` at `6fc09d69`, cleared at `:209`) has no counterpart in the r87 bytes (`grep` 0); the r87 replay gate is `if mode in ("required", "clone") and fields["replay"] is not None` (`count-c2.py:269`) | a population row declared `clone` with its `# replay:` deleted is neither flagged nor replayed, and still counts `replay=4` |

Readings 3 and 8 are the pair the supersede claim rests on: same revision, same receipts, one
call-site line different, `superseded=0 legacy=3` versus `superseded=2 legacy=1`. Reading 7 is the
measured limit: the two arms bracket the function, and a call-site regression keeps the detector
green, so only the fixture pair catches it; under that mutation the counter prints `detector=green`,
which is the one wording difference from the L1's `supersede-controls-r87.txt` §PRE-FIX line (it
elides that field). Reading 10 is this seat's independent reproduction of the lesson's
`## Material attack finding`: the frozen target line is reachable with zero replays, so the
detector's refusal — not the round's after-value — is what fails. At the real revision `98f48dba`
both successors do carry `# replay: clone` and the committed `evidence/after-r87.txt` records
`REPLAY record-sweep-r87.txt mode=clone rc=0` and `REPLAY claim-sweep-r87.txt mode=clone rc=0` with
both receipts `met`, so the after-value is not falsified.

Not run by this seat: the C1 and C2 gate runs over the lane, and any re-derivation of the
after-values. `evidence/after-r87.txt` (now committed in `728bc5f4`) is cited as the wave's record,
not restated as this seat's measurement.

## Gates

None executed. Readings 1–11 are detector selftests and counter runs against fixtures. The lesson's
`## Gate` rows (S603 admit, S600 re-open, one duplicate-URL reject) were supplied by the sources
seat and the L1; this seat did not verify them and, per its spec, wrote no rows while
`.ufo/waves/round-87/gate-input.md` was absent. The lesson's deferred TUF candidate is the sources
seat's pointer recorded for round 88; the L1 states it was not re-fetched, and this seat did not
re-fetch it either.

## Touched surfaces

- `.ufo/waves/round-87/w1/Mo87S01Lesson.md` — this report only.
- `corpus/lessons/round-87.md` — written once by this seat (13,542 bytes at ~10:20) and replaced by
  the L1's `728bc5f4`; not edited by this seat afterwards.
- Scratch `/fast/scratch/hyaku/mori-r87/Mo87S01Lesson` — created and deleted.

No counter, receipt, `SCORECARD.md`, `corpus/QUALITY.md`, `LOG.md`, `corpus/SOURCES.md`,
`corpus/README.md`, `corpus/knowledge/*`, `MANIFEST.json`, `.ufo/state/`, `.ufo/watchdog.log`,
`considerthese/`, fleet-root path or git/jj state was written. No commit, no `agent://all`, no
subagent dispatch. Tooling: nothing installed (no pacman/`uv`/`npx`/binary transaction).

## Out of scope / not done

- No Gate row written and no `gate-input.md` manufactured; the L1's supplied rows are the round's.
- No claim after-value re-derived; no gate executed.
- No rewrite of the L1's committed lesson.

## Findings

1. **`supersede_absent_target` does not build the case its label names.** `count-c2.py:329` is
   `supersede_verdict("old.txt", set(), [("new.txt", "old.txt")])`: the successor is in the
   superseder list and only absent from the clean set, so the arm re-tests uncleanliness and dies
   under the same mutation as `supersede_requires_clean` (reading 4). The case "a `# supersedes:`
   naming a receipt outside the population" is covered only by the `SUPERSEDE … absent=1` branch
   (`:297-301`), which has no arm. Carried by the lesson as the routed defect for round 88.
2. **The rule is guarded at the function, not at the call site.** `superseders` is appended during
   the header pass (`:241`); correctness depends on `supersede_counts` (`:294`) being its only
   reader. Reading 7 shows a call-site regression leaves both arms green. Carried as a named limit.
3. **A1's premise checks out statically, and its timing sentence needed E1.** The r86 subject
   `count-c2.py` has 11 arms at `6fc09d69` and 13 at `03b66a43`/`98f48dba` (reading 9), so a C2
   counter frozen at `SUBJECT_ARMS = 11` reads `subject=selftest` unmet at C2's landing revision.
   Contract erratum E1 (`859b7e9a`, appended post-data) corrects the timing: the successors landed
   at `98f48dba`, one commit before A1 at `b9e6f68d`, so A1 is post-data and what did not exist
   before it was the *measured* `C2=met` line, not the receipts. E1 states the scope claim (no
   target, population, supersede rule or kill rule moved) is verified and stands, and names
   `b9e6f68d` counter over `98f48dba` subject as the canonical grading form — which is what
   `after-r87.txt` records.
4. **The supersede defect's history rests on an author's worktree run, not a committed diff.** The
   earliest commits touching `.ufo/waves/round-87/count-c2.py` are the pre-freeze jj drafts
   `a0f185e0` and `d749ef88` (`refs/jj/keep/`, empty subject); both already carry
   `name in clean_names` (`:134`), and `git diff --name-only a0f185e0 142542e0` is empty. The
   behaviour is a reconstruction (readings 7–8 for the call-site form, 4–5 for the function-level
   form); the L1's receipt records the former. The lesson's row still says "`count-c2.py` at its
   first worktree state", which reads as a committed state; the lesson's integrated item 4 states
   the limit plainly, so the record is internally honest only when both are read together.
5. **The lesson's material attack finding is correct and this seat reproduced it independently
   (reading 10).** Stripping `# replay:` from both successors and fabricating their bodies makes the
   frozen counter print the exact target, rc 0, with no replay of either successor — because the
   r87 bytes dropped the r86 grammar's `missing-replay` problem (reading 11) and gate replay on the
   header field being present. The round's after-value at `98f48dba` is not falsified (both real
   successors replay); the *detector's refusal* is, and the lesson routes the repair to round 88 as
   highest priority. This is the round's own class (a claim about execution accepted from a header)
   recurring one level up: the supersede rule was fixed, the replay obligation it leans on still
   has a header-shaped bypass.
6. **The attribution correction landed at `1523b6cf`.** HEAD now reads "the pre-fix call site on the
   header-only fixture measured … superseded=2 legacy=1", which is the artifact that carries that
   reading, while `controls-r87.txt` §C2 (the committed post-fix control) reads `superseded=0
   legacy=3` for the same fixture. Verified by `grep` at `a90126ef`; issue closed.
7. **Round-86 routed defect 7 is discharged substantively, not literally,** by C2: the two r87
   successors re-run both sweeps at the named revision `25a74d4c` with `# replay: clone`, but they
   are r87 receipts, whereas the defect asked for an r86 receipt. Routed defects 1–6 and 8 are not
   touched by this round; routed defect 4 (Gate reject rows) is answered by the L1's supplied Gate
   rows, not by this seat.
8. **The final lesson carries one deferred source candidate (TUF v1.0.37) with an explicit flip
   condition and no row.** Cited from the sources seat; not verified here, and the L1 states it did
   not re-fetch it either. No registry row was written for it, which is the correct stop.

## Limits of this report

- Readings 1–11 were taken against the lane at `b9e6f68d` (counters) with the fixtures rebuilt
  afterwards; HEAD moved through `728bc5f4`, `a42b1d79`, `1523b6cf`, `a90126ef`, `859b7e9a` and
  `22fa2919` during the seat.
  The counters were unchanged across all of them (count-c2.py sha256 `264a43f0…`, count-c1.py
  `e2ff9687…` at `b9e6f68d` and at the final read).
- The fixtures reproduce receipt *bodies* and headers only; they do not re-run the sweep commands
  outside the counter's replay path, and fixture commit ids are not reproducible across runs
  (contents and readings are).
- The mutation readings (4, 6, 7) come from edited copies of the frozen counter under scratch, never
  written inside the lane; the counter's own selftest is the detection surface, and no committed
  mutation harness exists for them.
- Reading 10 shows the target is reachable with zero replays; it does not show the real population
  is in that state — `after-r87.txt` records both replays at `98f48dba`.

## Artifact paths

- report: `.ufo/waves/round-87/w1/Mo87S01Lesson.md`
- lesson (L1-authored, seat findings merged): `corpus/lessons/round-87.md` — bytes fixed at
  `a90126ef`, 146 lines, sha256 `0060c76f…`, worktree clean; HEAD at final read `22fa2919` (later
  commits touch the contract and SCORECARD only)
- cited wave artifacts: `.ufo/waves/round-87/contract.md` (`bf208a44…` as read at `b9e6f68d`;
  `afa154ff…` at final HEAD `22fa2919`, E1 appended), `count-c1.py`
  (`e2ff9687…`), `count-c2.py` (`e1dfd45a…` frozen, `264a43f0…` at `b9e6f68d`), `controls-r87.txt`
  (`53d65a42…`), `probe-r87.txt` (`530e35e6…`), `after-r87.txt` (`282513c0…` at read),
  `supersede-controls-r87.txt` (`b9ca89cf…`)
