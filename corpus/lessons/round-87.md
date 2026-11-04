# Round 87 — mori (L1 MoriR87), attempt 1, wave w1 — lesson

round: 87
date: 2026-11-04
entering: `6fc09d69edbb11e5070ff33258de49f062c0fb9b`
freeze: `142542e0d853b4e8ec1aa1adb86708dc5786d9c0` (contract, both counters, the controls, the
population probe); amendment A1 at `b9e6f68d887c570909c7bacc8bac86579d850d1d` (the C2 counter's
subject arm count follows C1's two extra arms; no target, population or kill rule moved)
read at: `b9e6f68d` (the wave ran while the C1/C2 landing commits `03b66a43` and `98f48dba` were
already on the branch)
seat scope: this lesson and its `## Gate`. The wave seats write their own reports under
`.ufo/waves/round-87/w1/`; they do not commit.

Axes this round: **operability** (six surviving r86-counter clauses get their arms) and
**calibration** (a legacy receipt is superseded only by a replaying successor). Detection and
report only.

## What the round did

Two claims, frozen at `142542e0` before any after-value existed, each with a named do-nothing
control in `.ufo/waves/round-87/evidence/controls-r87.txt`:

- **C1 operability (7)** — a new population-control counter `.ufo/waves/round-87/count-c1.py`
  re-derives six mutants from any revision's bytes (anchors: three in `count-c1.py`, two in
  `count-c2.py`, one in `count-c3.py`), runs each mutated copy's own `--selftest`, and requires
  the three pristine copies green at exactly 18/13/23 arms; target `C1=met mutants=6 killed=6
  survivors=0 total=6 arms=54`. Entering control: `C1=unmet ... survivors=6 total=6 arms=48`
  (rc 1); a label-only fixture still reads `survivors=6`, so labels are not the work.
- **C2 calibration (5, tied lowest)** — a new counter `.ufo/waves/round-87/count-c2.py` grades a
  seven-receipt population and a supersede rule: a legacy receipt counts `superseded` only when a
  present, problem-free successor names it in `# supersedes:` and that successor's `# replay:
  clone` reproduces its body in a `--shared` clone checked out at the receipt's own `# rev:`.
  Target `C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4
  matched=6 defeated=1 superseded=2 legacy=1 unexpected=0`. Entering control: `C2=unmet
  receipts=5 absent=2 ... superseded=0 legacy=3` (rc 1); a header-only fixture with fabricated
  bodies reads `matched=4 superseded=0 legacy=3 unexpected=2` (rc 1).

Wave shape: one v1 wave, 12 seats (3 executor, 1 simplifier, 1 scout, 2 scribe, 2 reviewer,
1 critic, 1 mutation-tester, 1 connector; attack 4/12 = 33.3 %), validated under policy v1
(`w1-dispatch.json` counts `spawn 12`), reports under `.ufo/waves/round-87/w1/`.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix delivered and what makes it able to fail |
|---|---|---|---|
| `supersede-by-presence` — the supersede rule retired a legacy receipt when a successor merely *existed* in the population, not when the successor verified. A successor whose body its own command does not produce (`replay-mismatch`) still counted `superseded`, so the claim's own evidence class ("recorded is not verified", S602) was violated inside the instrument that was supposed to enforce it. | `.ufo/waves/round-87/count-c2.py` at its first worktree state: the loop `if clean and supersede_verdict(name, set(present), superseders)`; the header-only control measured `C2=unmet ... matched=4 defeated=1 superseded=2 legacy=1 unexpected=2` (rc 1) — the two stale successors retired both legacy receipts while failing their own replay. Recorded at `.ufo/waves/round-87/evidence/supersede-controls-r87.txt` §PRE-FIX. | The §9 do-nothing control, built before data: "build the cheapest control that skips the claimed work and score it with the frozen counter". The header-only fixture (correct headers, headers' digests, fabricated bodies) is exactly that cheap path, and it turned the target's `superseded=2` into a *defect witness* instead of a pass. | `supersede_counts(legacy_rows, clean_names, superseders)` counts only problem-free successors, and `clean_names` is populated only when `problems` is empty; two selftest arms (`supersede_requires_clean`, `supersede_counts_positive`) pin the function. Able to fail: on one fixture the pre-fix call site reads `superseded=2 legacy=1` and the fixed one reads `superseded=0 legacy=3` (same revision, same receipts, one call-site line different — `evidence/supersede-controls-r87.txt`); the header-only control in `evidence/controls-r87.txt` §C2 shows the same split. Named limit: the arms exercise the function, not the call site — the call-site evidence is the fixture pair, not an arm. |

Nothing else was mined: the r86 spot-check's eight routed defects belong to round 86's report and
are recorded as inherited, not re-litigated here (the r87 prompt's §5 asks for a
`round-86-verifier-spotcheck` read; it was read, and the only defect class that bears on this
round's instruments — a cited output that the receipt does not carry — is answered by every
after-value here naming its receipt and revision).

## Gate

Sources opened this round. One new row; one re-opened row whose `used-by` changed; one rejection.

| Candidate | Decision | Evidence / flip condition |
|---|---|---|
| **S603** — git-clone(1), `https://git-scm.com/docs/git-clone` | **ADMIT** (tier A, `docs`, `mined`; row after S602, `used-by corpus/knowledge/receipt-supersede-r87.md`, recheck `on-release`) | Accessed **2026-11-04**; two fetches byte-identical (`cmp` clean): HTTP 200, `redirects=0`, final URL identical, **107882 bytes**, **3391 lines**, sha256 `d31b6c9f293a5dfc52c551b86be211b2d6dad3d2b4cf0d9c696d5fbed713554a`. Located quotes in the tag-stripped joined text, each occurring **exactly once**: "Clones a repository into a newly created directory, creates remote-tracking branches for each branch in the cloned repository" (**18 words**, raw lines 2627-2628) and "instead of using hard links, automatically setup .git/objects/info/alternates to share the objects with the source repository" (**16 words**, raw lines 2696-2699). The row grounds the measured tree-versus-clone split (`revisions=3` rc 1 in a `git archive` export, `revisions=0` rc 0 in a clone at the same revision). |
| **S600** — Reproducible Builds — Definitions, `https://reproducible-builds.org/docs/definition/` | **RE-OPENED, `used-by` changed** `corpus/knowledge/receipt-provenance-r85.md` → `corpus/knowledge/receipt-provenance-r85.md, corpus/knowledge/receipt-supersede-r87.md` | Fetched **2026-11-04**: HTTP 200, `redirects=0`, 37681 bytes, 3662 lines, sha256 `a558c89f5f27dffa69fd1dc49904179b60233bcfdfc64807abfe1acf37518ebb` — **byte-identical to the registered sha**, so the row's bytes still stand. `status` stays `mined`, `opened` stays 2026-11-04, `recheck` stays 365d. |
| **reproducible-builds.org/docs/definition/ as a NEW row** | **REJECTED** (duplicate URL+scope of S600) | The r86 bounded search excluded it for the same reason and this round's fetch confirms it is S600's page; the registry census (`.ufo/waves/round-87/assimilation` is not used — this is a normal round) counts **375 → 376** rows, and a second row for one URL would be a within-scope duplicate (E04). Flip condition: a *different* scope on that page (for example the verification-tooling section) that S600's scope cell does not cover, freshly pinned and quoted, opened as a new row with its own anchor. |

Registry census, both runs on this worktree:

```text
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md          # before: rc 0, 375 rows
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md          # after:  rc 0, 376 rows
```

Row counts by the contract grammar `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`:
**375 → 376**; warnings 35 → 35 (all `W04` duplicate-URL, the entering tolerance), zero `E` codes
both times.

Gate limits, named: this round verified the S603 bytes at the `git-scm.com` page it fetched, not
that page at another revision; the quote positions are raw HTML lines and a reader must strip tags
to see them as one sentence. **Assimilation: none** — no `merge/mori/` package was adopted this
round; `/home/vgpnk/Projects/shokukinow` was not touched. `considerthese/2026-10-26.md` suggestion
3 ("re-execute what closures only evidence-verified") is the C2 rule's standing motivation and is
cited by QUALITY 181; it is not newly implemented as a proposal this round.

## Seat findings merged at integration (Mo87S01Lesson, wave w1)

The lesson scribe wrote its own draft of this file; the L1 kept the version committed at `728bc5f4`
(which carries the `## Gate` the seat could not write — `gate-input.md` was never supplied, and the
seat correctly refused to invent rows) and merges the seat's four findings here.

1. **`supersede_absent_target` does not build the case its label names.** Its fixture is
   `supersede_verdict("old.txt", set(), [("new.txt", "old.txt")])`: the successor is in the
   superseder list and only absent from the clean set, so the arm re-tests uncleanliness and dies
   under the same mutation as `supersede_requires_clean`. The case "a `# supersedes:` naming a
   receipt outside the population" is covered only by the `SUPERSEDE … absent=1` branch
   (`count-c2.py:297-301`), which has no arm. **Routed defect for round 88:** add an arm whose
   population omits the named receipt.
2. **The rule is guarded at the function, not at the call site.** `superseders` is appended during
   the header pass (`count-c2.py:241`) and correctness depends on `supersede_counts` being its only
   reader (`:294`); a second consumer of the list would reintroduce the header-only answer without
   turning either arm red. Named limit, not fixed this round.
3. **Amendment A1's premise checks out statically.** The r86 subject `count-c2.py` has 11 arms at
   `6fc09d69` and 13 at `03b66a43`/`98f48dba`, so a counter frozen at 11 would have read
   `subject=selftest` unmet at C2's landing revision — which is exactly what the pre-A1 run did.
4. **The defect's history rests on an author's worktree run, not a committed diff.** The seat
   verified that the pre-freeze jj drafts `a0f185e0`/`d749ef88` already carry the fixed conjunct, so
   no committed blob shows the pre-fix rule. The L1's pre-freeze fixture
   (`.ufo/waves/round-87/evidence/supersede-controls-r87.txt`: pre-fix `superseded=2 legacy=1`,
   fixed `superseded=0 legacy=3`) and the seat's mutation reconstruction
   (`pass=15 fail=2`, fixture `superseded=2 legacy=1 detector=red`) agree; both are recorded as what
   they are.
