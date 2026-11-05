## Gate

No source row is admitted by round 90 at the entering revision, so this section has no source block. Evidence: `git show --stat --format='%H %s' d1c8488986512a6a0475af88cc52779ce4703e00` lists six files, all under `.ufo/waves/round-90/`, none under `corpus/`; `.ufo/waves/round-90/w1/` held only `swarm-registry.json` when this seat read it, so no `Mo90S01Sources` report exists to admit rows from. No URL or access date is entered here.

Registry discipline the round must follow if rows are admitted:

- `corpus/SOURCES.md` is a registry with columns `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`; `status` is `mined`, `queued` or `rejected`, and `recheck` is a dated trigger (`on-release`, `90d`) or `—`.
- A rejected candidate keeps its row with the reason in the `scope` cell (`S030`, `corpus/SOURCES.md:36`, "REJECTED: …"). A duplicate candidate is kept as rejected, not deleted (`S179`, `corpus/SOURCES.md:185`; `S211`, `:217`).
- The admission bar (`corpus/QUALITY.md:1-8`): every claim carries a source; observation, inference and unknown stay separate; errata are append-only; "A rejection is kept, not silently dropped."
- A rejection states its flip condition, as the round-89 table does for `S608` (`corpus/lessons/round-89.md`, `## Gate`).

## Mistakes

| Class | Evidence pointer | Captured-by | Fix, and what makes it able to fail |
|---|---|---|---|
| `selftest-orientation-unpinned-and-red-unrecorded` — the inherited round-90 `count-c1.py` gave its two synthetic gates opposite orientations relative to its own `bound()` test. `bound()` treats `binding_problems(...) == []` as binding (`.ufo/waves/round-90/count-c1.py:120-125`); the arms define `deny` as returning `[]` (`:232-233`) and `allow` as returning `['cmd-binding']` (`:234-235`). Contract A1 (`.ufo/waves/round-90/contract.md:65-71`) says the inherited arms passed these gates "in the wrong order (`deny` binds, `allow` refuses)" and that four arms failed. The committed bytes carry that same orientation and pass. No committed bytes hold the red reading: `git log --all -- .ufo/waves/round-90/count-c1.py` lists only `d1c84889`, which already contains the repaired file, and `.ufo/waves/round-90/evidence/controls-r90.txt` §4 holds only the green line `C1_COUNTER_SELFTEST pass=12 fail=0` (rc 0). The pre-repair selftest named as this row's pointer does not exist in the lane. | `.ufo/waves/round-90/controls-r90.sh` §4 "counter selftests (detectors green before data)" runs the selftest, but only on the repaired bytes. Rules that bind it: a counter's own selftest must be green before it grades anything (QUALITY 174, 188). Neither was violated by committed bytes; what was missing is a committed record of the inherited bytes' red reading. | Three checks, each red today. (1) Commit the selftest of any counter replacing an inherited one run on the inherited bytes, expected rc 1 with named FAIL labels, before the repair lands. (2) Add an orientation arm: by the counter's own `bound()`, a gate returning `[]` binds and a gate returning a problem list does not. (3) Keep a committed negative control: a copy with the two gate bodies swapped must read `C1_COUNTER_SELFTEST pass=6 fail=6` and rc 1. This seat measured (3) at the entering bytes (scratch copy, see Seat findings): `pass=6 fail=6`, rc 1, six arms red, not four. A counter that stays green on the swapped copy cannot grade orientation, and the row is then reopened. |

## Assimilation

Still unimplemented, fits C2 (calibration): `considerthese/2026-10-24.md`, "Keep a cumulative survivor ledger" (bullet 2). QUALITY 114 states the rule (`corpus/QUALITY.md:927-937`: a cumulative ledger "re-runs every committed survivor fixture against the newest conformance checker and reports any that still pass"), but no committed reader globs or enumerates the survivor fixtures; readers name files by hand. `.ufo/waves/round-42/count-c1.py:35-39` lists three round-41 survivor paths; `.ufo/waves/round-42/fixtures/mutants/` (six files) is read only by name (`round-42/count-c1.py:188,216`, `round-43/count-c1s.py:143`); `tools/mori-pin-check.py` mentions survivors only in a comment (`:1421`). Falsifiable form: a committed ledger of survivor fixture paths and a reader that prints `LEDGER survivors_still_passing=N` and exits 1 when N > 0 against the round's counter. Round 90's C2 population (15 mutants) does not include the older committed survivors.

## Seat findings (not lesson body; L1 strips this section)

Seat `Mo90S02Lesson`. Entering: contract `037c02ca43a5ff36e23e449d0d6bcf50a1f2cbec`; lane HEAD `d1c8488986512a6a0475af88cc52779ce4703e00` (`git rev-parse HEAD`; `d1c84889` is the commit that preserved the round's in-flight files). Both resolve (`git rev-parse --verify -q <rev>^{commit}`), and `037c02ca` is an ancestor of `d1c8488` (`git merge-base --is-ancestor`, rc 0). The assignment's "entering revision d1c8488" is the HEAD, not the contract's entering value.

Measured:

- `count-c1.py --selftest` on the committed bytes (run in a scratch tree that symlinks the read-only `round-89` directory): `C1_COUNTER_SELFTEST pass=12 fail=0`, rc 0. Matches `evidence/controls-r90.txt` §4.
- The same counter with the two gate bodies swapped (`deny` returns `['cmd-binding']`, `allow` returns `[]`): `C1_COUNTER_SELFTEST pass=6 fail=6`, rc 1. Red arms: `branch_open_counted`, `branch_closed_zero`, `harm_counted`, `harm_absent_when_gate_binds`, `newopen_absent`, `newopen_counted`. Green: `reach_uncounted`, `branch_ids_frozen`, `target_literal`, `load_cases_class_split`, `counted_population`, `own_arms_pinned`.
- Corrections to the assignment's evidence pointer and count: `controls-r90.txt` holds the post-repair reading only, and no committed artifact shows four failing arms. The row above states this rather than the requested "pre-repair selftest" pointer.
- Survivor-reader check: `grep -rIl "glob\|listdir\|scandir\|rglob" tools .ufo/waves --include=*.py --include=*.sh | xargs grep -l -i survivor` returns 16 files. I grep-inspected the survivor hits in `round-42/conform.py`, `round-42/count-c1.py` and `tools/mori-pin-check.py` (`:1592`, `:1626` are `os.listdir` on unrelated scratch dirs; the survivor word is in a comment at `:1421`); the other hits are per-round spec builders I did not open. No hit globs the committed survivor fixture set.

Not run: no lane counter was run at the entering revision by this seat beyond the selftests above; the `after-r90` receipt does not exist yet.

Tooling: none installed or updated. Scratch `/fast/scratch/hyaku/mori-r90/Mo90S02Lesson` removed; no lane file, corpus file or registry row was written.

Report: .ufo/waves/round-90/w1/Mo90S02Lesson.md
