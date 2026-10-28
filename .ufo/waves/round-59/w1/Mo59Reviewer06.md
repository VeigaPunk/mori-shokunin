# Mo59Reviewer06 — C1 do-nothing re-derivation

Seat task: run the frozen counter at the entering revision; enumerate the cheapest
work-skipping states that could reach `met`; adversarial finding or bounded
no-counterexample. Read-only; no production/VCS writes. Scratch:
`/fast/scratch/hyaku/mori-r59/Mo59Reviewer06/` (TMPDIR set; cleaned post-report).

Counter bytes verified vs freeze:
`git show 60b3a76a:count-c1.py | sha256sum` == worktree file ==
`2be6fda8c54633fd96f9d447e8e78ff4ba4a6d6136670f79a9d622003f0c9dfd`. Kill-rule
intact. Counter `--selftest`: `C1_SELFTEST pass=6 fail=0`, exit 0.

## Reproductions (all observed)

| command (lane cwd) | observed |
|---|---|
| `python3 .ufo/waves/round-59/count-c1.py 2b9f03975bfb6e508f35074ac8181ec8bf54e805 --scratch …/c1-entering` | `C1=unmet selftest=bad fixtures=bad real=bad pointers=bad rev=2b9f…e805 failed=tool_absent,selftest,fixtures_absent,real,pointers`, exit 1 |
| `python3 .ufo/waves/round-59/count-c1.py 60b3a76ad0524c8978cc51922940be1c8c388915 --scratch …/c1-freeze` | `C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=60b3…8915`, exit 0, ~1.2 s |
| `python3 .ufo/waves/round-59/count-c1.py HEAD --scratch …/c1-head` | `C1=met … rev=HEAD`, exit 0 (HEAD=`8ff344ff…`, merge-base check: freeze IS ancestor) |

## FINDING F1 (primary, high): C1 is met by the freeze itself — the wave cannot do the work, only break it

The freeze commits landed the claim's payload, not just the counter:

- `git log --diff-filter=A -- tools/mori-register-check.py` → sole add is
  `ccfd554e "round-59: freeze contract, C1/C2 counters, tools, fixtures, controls"`.
- `git show 60b3a76a:tools/mori-register-check.py | sha256sum` ==
  `38b733d896f880f5b7ecb464848b80798810ab052fcf0a8afb320918151472b8` == PIN
  (count-c1.py:38). All 13 fixture dirs present at freeze rev (f01–f13).
- `measure()` (count-c1.py:84) reads **exclusively** via `git show/ls-tree/cat-file`
  at R: tool blob (88–90), fixture trees (131–149), `SCORECARD.md` (169), evidence
  pointers (188–197). MANIFEST read is pinned to fleet rev
  `2807c6ab…` (170). Nothing reads the working tree; no diff of wave artifacts.

Consequence: for every R whose diff against the freeze leaves the six input
classes untouched (tool blob, `fixtures-c1/` tree, `SCORECARD.md`, the four
pointer paths, fleet MANIFEST at pin), `C1=met` — observed at freeze and HEAD.
**Cheapest work-skipping state = literal do-nothing; cost ~1.2 s.** The frozen
do-nothing control binds to pre-freeze `2b9f0397`, which no wave scoring run
will ever measure; it bounds nothing about wave work. The claim "the lane lands
a capability … plus a frozen counter" is true the moment freeze commits — the
build side is degenerate (satisfied by the freeze event), and the falsify side
survives only through (a) unfrozen-input drift — e.g. a seat legitimately
rewriting the `## Capabilities` section in `SCORECARD.md` flips `real` to bad;
`git diff 60b3a76a..HEAD -- SCORECARD.md` is currently empty, so the coupling
is live — or (b) a kill-rule-invalidating edit of frozen bytes. `rev=` in the
target output is bound to a commit only if the R passed is one (echo verbatim).

## FINDING F2 (medium): counter accepts `--repo`/`--fleet` overrides — `met` receipts are mintable off-lane

`main()` (count-c1.py:249–259) defaults `repo`/`fleet` to the lane/fleet but
accepts flag overrides; the frozen counting command
`python3 .ufo/waves/round-59/count-c1.py R` pins neither, and no check verifies
that `repo` is the lane or that R is a lane commit/descendant. Demonstrated:
built `…/fakerepo` (git init, 96 files copied via `git show` from freeze —
tool at PIN, all 13 fixtures, SCORECARD.md, 4 pointer paths), committed as
`9215f30c8d2fe1bd8d8d5a3fad9498c117ecf178`, then:

`count-c1.py 9215f30c… --repo …/fakerepo --scratch …/c1-forge` →
`C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=9215f30c8d2fe1bd8d8d5a3fad9498c117ecf178`, exit 0.

A `met` receipt costs minutes of scripted `git show`, zero lane state. Cost is
bounded by needing the real PIN'd tool bytes and real fleet MANIFEST (both
public to any seat). Mitigation class: receipts must name a lane-commit sha
verifiable via `git merge-base`/membership; F1 already makes this moot for
scoring this wave (any descendant R is met anyway), but the door stands for
receipt honesty generally. Related: `rev=` echoes argv[0] — `rev=HEAD` receipts
(above) carry no commit binding at all.

## Enumerated non-doors (checked, closed)

- Working-tree plant: counter never reads WT; uncommitted tool/fixture files
  can't score. Closed.
- Vacuous-fixture: empty `dirs` → `fixtures_absent` fail (135–138); per-fixture
  missing expect/scorecard/manifest → `fixture:<n>:incomplete` (143–147);
  `matched` requires real UNMET verdict (163–166). Closed.
- Pointer vacuity: `all_exist = bool(ptrs)` → empty pointer list fails
  `pointers` (186–187). Closed.
- Fleet skip: `mf is None` → `manifest` fail (169–172). Closed.
- Stale-scratch replay: leftover `tool.py` can't flip unmet→met — `tool_absent`,
  `selftest` are unconditional fails gated on `tool_b is not None` (90–128).
  Closed.
- `materialize()` return ignored in fixture loop (159) → missing fixture file
  only makes the fixture *more* unmet. Fail-closed. Closed.
- Tree-name path escape: crafted `..` names unreachable — git fsck/tree parsing
  rejects `..` components; `git show`/`cat-file` fail before write. Closed.
- Interpreter shadowing of `python3`: a hostile PATH could forge all
  subprocess arms, but the host guard forbids PATH writes; flagged as
  environment assumption, not a lane door.

## Residual risk / verification gaps

- F1 makes C1's wave outcome insensitive to 63/64 seats' work; only
  `SCORECARD.md`/pointer-path drift or a kill-rule event can change it. Whether
  that was intended ("pre-landed claim") or a freeze-payload leak is for L1 to
  adjudicate — the contract's predicate sentence is literally satisfied, so
  this is an admission-of-claim design defect, not a counter bug.
- Did not re-run all 13 fixture arms individually (counter did, `fixtures=ok`
  at freeze/HEAD/forged-repo runs — each judged UNMET with expect coverage).
- `--fleet` override untested (real fleet MANIFEST rev suffices for F2; a
  forged `--fleet` repo would only ease it further).
- No C2 claims here (sibling seats own the C2 axis).

Tooling: none installed (system python3/git only). Disk guard green throughout
(27% used). Scratch cleaned.
