# Mo53ScribeReportConvention — the report's own commit: convention draft and the round-52 erratum line

Seat: scribe. Task: routed defect 2 of the round-52 closure (`corpus/lessons/round-52-verifier-spotcheck.md`
§Routed defects) — the round-52 report left `[FILL]` where its own commit belongs — draft (fenced) the convention
text for the lesson (how a report names its own commit without a placeholder, by a command over the fleet repo)
and the erratum line for round 52 with the existing hash `aacd7a83027cdee8e950a2c39d490feaed3be13c`.

Tree read: fleet repo `/home/vgpnk/Projects/shokunin` at `fd697467` (detached — see finding L4), lane work tree
`/home/vgpnk/Projects/shokunin/mori-shokunin` at `95cf78ee` (round-53 wave spec). Everything below is read-only:
no write outside this report, no git/jj mutation in either repo, no fixture, no clone, no network fetch, no tool
install, no pacman transaction. Host reads: none beyond `df`. Scratch
`/fast/scratch/hyaku/mori-r53/Mo53ScribeReportConvention/` was created empty (`mkdir -p`), never used for a file,
and removed at the end (§6).

## 1. What the round-52 report actually carries

The filed report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-52/mori.md` (115 lines, 10107 bytes) carries the
literal token twice:

```
$ grep -n '\[FILL\]' .ufo/reports/round-52/mori.md          # cwd /home/vgpnk/Projects/shokunin, rc 0
5:… `37af57f263cf0f035fa6d19f666d2de7790b63b7` (receipts commit; `git ls-remote origin refs/heads/master` prints it). Report commit `[FILL]`.
46:| `[FILL]` | receipts at landed tip: `c1-at-landed.txt`, `c2-at-landed.txt`, `census-end.txt` | Round 52 |
```

Line 45 of the same `## Landed changes` table is the row `| `37af57f2` | receipts at landed tip: `c1-at-landed.txt`,
`c2-at-landed.txt`, `census-end.txt` | Round 52 |` — so line 46 repeats its neighbour's description verbatim and
differs only in the commit cell. That matters for the erratum: the wrong "fix" is to drop the lane receipts hash
`37af57f2` into the `[FILL]` cells, which would produce a duplicate row and a second, false citation of a commit
line 5 already cites as the lane tip.

The commit that does exist, measured with the command the seat spec names:

```
$ git -C /home/vgpnk/Projects/shokunin log --format='%H %an' -- .ufo/reports/round-52/mori.md
aacd7a83027cdee8e950a2c39d490feaed3be13c mori-shokunin
```

Corroboration (`/home/vgpnk/Projects/shokunin`, all read-only):

| check | command | output |
|---|---|---|
| commits touching the file | `git log --format=%H -- .ufo/reports/round-52/mori.md \| wc -l` | `1` |
| file-adding commit | `git log --diff-filter=A --format='%H %an' -- .ufo/reports/round-52/mori.md` | `aacd7a83027cdee8e950a2c39d490feaed3be13c mori-shokunin` |
| payload | `git show --stat --format='%H%n%an <%ae>%n%ad%n%s' aacd7a83` | `1 file changed, 115 insertions(+)`; `mori-shokunin <mori@shokunin.local>`; `Mon Oct 26 21:55:24 2026 -0300`; `round-52: mori report` |
| ancestry | `git merge-base --is-ancestor aacd7a83 HEAD && echo ancestor=yes` | `ancestor=yes` |
| filed bytes unamended | `git diff --stat aacd7a83 HEAD -- .ufo/reports/round-52/mori.md` | no output, rc 0 |

So the hash is a fleet-repo, report-only commit carrying the lane identity — exactly the "report commit" the
`[FILL]` slots were for, and exactly the hash the round-52 verifier's D1 already identified
(`round-52-verifier-spotcheck.md`, §Conformance defects D1).

## 2. The siblings: the premise of the task does not hold as stated

The seat spec says "two sibling reports of round 52 under `/home/vgpnk/Projects/shokunin/.ufo/reports/round-52/`
that cite their own commit (grep 'Report commit')". Measured, that set is empty:

```
$ cd /home/vgpnk/Projects/shokunin/.ufo/reports/round-52 && ls
chousa.md  kake.md  kotoba.md  kotodama.md  kumitate.md  mori.md          # 6 files
$ grep -rn 'Report commit' .            # rc 1 for every file except mori.md
mori.md:5:… Report commit `[FILL]`.
```

`grep -rl 'Report commit' /home/vgpnk/Projects/shokunin/.ufo/reports/` returns 31 files across all rounds; inside
round-52 only `mori.md` matches, and its match is the defect. The five siblings cite the commit that carries their
*work*, never their own report commit, and each does so in a lane-side form:

| sibling | line | self-referential citation |
|---|---|---|
| `chousa.md` | 5 | freeze `37468eadd8d098e80289b2f31a22de3872d4a1f6`; `:21` table row W1 integration `01c17ce3` |
| `kake.md` | 3-4 | `base: 93d7fdbd…`, `measured revision: a4a890cf…`, `tip a1d83ecf…`; `:62` row `r51-5 measured commit descriptive`, whose cell reads "this report and SCORECARD name the measured revision hash and its receipts" |
| `kumitate.md` | 4-6 | R1 `ab5dde40…` … R4 `17dd42e1e37d8f8abfde08417a20482e1ebfb8fa` = "report-only … = lane tip" (a **lane** report-only commit, not the fleet report commit) |
| `kotoba.md` | 3-5 | "Lane head after this round: `0c9180a6…`", "content commit `a44196d8…`" |
| `kotodama.md` | 3 | "Lane HEAD (pushed): `2eb489fb…`" |
| `mori.md` | 5 | "Report commit `[FILL]`" |

None of the five states a self-citation slot at all, so none can supply the convention by example. The convention
must therefore rest on the fleet's earlier precedents, which §3 collects — and the absence in five of six siblings
is itself the second half of the finding: the slot only exists when a lane volunteers one, so a convention that
says "name it by command" also needs a rule for lanes that would rather omit the slot (see DRAFT A, last
paragraph).

## 3. Why a hash cannot be written at write time (the convention's ground)

- `PROTOCOL.md:117` — "A lane report **lands last** — written only after the lane's child-repo work is committed,
  and it must cite that commit's hash." The hash that clause requires is the *lane* HEAD (round 52: `37af57f2`),
  which exists when the report is written. The report's own commit exists only after the file is written and
  committed, so it is a second, later commit.
- `PROTOCOL.md:125` — "Landed also means landed *by the lane*: the commit that adds `.ufo/reports/round-<N>/<id>.md`
  carries the lane identity." That commit is the object of the self-citation, and it is a fleet-repo commit
  (§1: `aacd7a83`, author `mori-shokunin`).
- `AGGREGATE.md:1191` (D-88) — the respawn driver's completion signal is the report file's *existence*, so a tick
  between write and commit leaves a lane's own report commit unreachable; a slot filled by hand at write time
  cannot be filled correctly.
- `AGGREGATE.md:680` (D-12) and `.ufo/reports/round-10/kengaku.md:5` — the fleet's orphaned-hash precedent: the
  round-7 kengaku report cited `85b22e3`, which an amend orphaned (`merge-base --is-ancestor` → exit 1). The
  round-10 report responds by citing the commit *by the command that adds the file*.
- `PROTOCOL.md:135` — a correction lands "in the correcting round's own report, or as an erratum appended after
  the filed bytes in a new commit and naming the text it supersedes — never a rewrite of the filed bytes": the
  erratum path is legal, and it is the one DRAFT B uses.

The fleet already has four instances of the command-or-"this file" form, so DRAFT A is codifying practice, not
inventing it:

| precedent | text |
|---|---|
| `.ufo/reports/round-10/kengaku.md:5` | "main-repo report commit: the commit adding this file (verify: `git -C ~/projects/shokunin log -1 --format=%h -- .ufo/reports/round-10/kengaku.md`; not cited by hash here because round 7's amended-away `85b22e3` citation is this fleet's orphaned-hash precedent)" |
| `.ufo/reports/round-11/kengaku.md:7` | "main-repo report commit: the commit adding this file (verify: `git -C ~/projects/shokunin log -1 --format=%h -- .ufo/reports/round-11/kengaku.md`)" |
| `.ufo/reports/round-48/kake.md:8` | "report commit: (this file's fleet commit)" |
| `.ufo/reports/round-34/kaidoku.md:69` | "\| fleet report commit \| this file \| cites `2e8a7758` \|" |

The lane's own rule is already the same rule at one remove: `corpus/QUALITY.md:17` (criterion 9) — "Every path,
line or commit pointer resolves at the carrying commit; a report names the commit that carries its work". A
`[FILL]` token resolves to nothing, which is why D1 is a conformance defect and not a style nit.

## 4. The multi-touch case the convention must survive (measured)

`.ufo/reports/round-19/souji.md` is the fleet's append-only erratum example:

```
$ git log --format=%H -- .ufo/reports/round-19/souji.md | wc -l        → 23
$ git log --diff-filter=A --format='%H %an %s' -- .ufo/reports/round-19/souji.md
cf557a61f6b88916086ba3bcddb27088e4e69836 souji-shokunin round-19: souji report
f47ad6ba8d306f8125597401cb2ce45c1297a593 protocol-shokunin repair: restore fleet tree deleted by stray commit 35b91714 (author t <t@t>, 09:21:14 -03)
```

Two consequences, both relevant to the text I draft:

1. After an erratum append, `git log --format=%H -- <path>` prints one hash per touching commit (23 here), so the
   bare command the round-53 contract names resolves a *fresh* report (`round-53/mori.md`, one commit) but not an
   amended one. The report commit is the earliest add: `git log --diff-filter=A --format=%H -- <path> | tail -1`.
2. `--diff-filter=A` alone is not unique either: a tree restore re-adds the path, so the filter lists two commits.
   Earliest still wins (`cf557a61`).
3. Side observation, checked and discarded as a counterexample: `souji.md:188` reads "Report committed in lane
   commit `7d199d2b…`", which looks like a hash-form self-citation but is not — `git -C souji-shokunin show --stat
   7d199d2b` → ` .ufo/waves/round-19/w1/CriticD5.md | 24 ++++`, a *seat* report, and the next bullet names the lane
   tip separately. No mislabel there; the hash form simply names a different artifact.

## 5. DRAFT A — convention section for the lesson (fenced; L1 integrates)

Target file: `corpus/lessons/round-53.md` (does not exist yet — `ls corpus/lessons/ | tail` ends at
`round-52-verifier-spotcheck.md`), placed next to the mistake row that mines the round-52 `[FILL]` self-citation
(contract §"Mistakes to mine", closure D1). Alternative home if the L1 prefers an erratum file: a new
`corpus/lessons/round-52-report-erratum.md` in the shape of `round-51-erratum.md`. Nothing below is written to disk
by this seat.

```markdown
## Convention — a report names its own commit by command, never by a placeholder

A report cannot carry its own commit hash, and it must not pretend to. `PROTOCOL.md:117` makes the report
land last: the hash a report cites is the lane repo's HEAD when the report is written. The commit that adds
`.ufo/reports/round-<N>/<id>.md` is a *later*, fleet-repo commit (`PROTOCOL.md:125`, landed by the lane), so
its hash does not exist while the file is being written — and the driver's completion signal is the file's
existence, so a tick between write and commit can strand the slot (`AGGREGATE.md:1191`, D-88). A hash guessed
anyway and then amended orphans the citation: round-7's `85b22e3` (`AGGREGATE.md:680`, D-12;
`.ufo/reports/round-10/kengaku.md:5`).

So the slot carries the command that resolves it, run at the fleet root, quoted verbatim in backticks:

    git log --format=%H -- .ufo/reports/round-<N>/<id>.md

This is the round-53 contract's form and prints exactly one 40-hex hash for a report landed once (round 52:
`aacd7a83027cdee8e950a2c39d490feaed3be13c`, `mori-shokunin`, 1 file / 115 insertions). Never write `[FILL]`,
`TODO`, `TBD`, an empty table cell, or the hash of some other commit. In particular the lane tip and the
report commit are two different citations and both belong in the header: the lane tip as a hash (it exists),
the report commit as the command (it does not). A lane that would rather not carry the slot at all omits it
and says so; it never leaves a marker.

If the file is later amended — an erratum appended after the filed bytes in a new commit (`PROTOCOL.md:135`) —
one hash per touching commit appears and the report commit is the earliest, the commit that added the file:

    git log --diff-filter=A --format=%H -- .ufo/reports/round-<N>/<id>.md | tail -1

Measured precedent for both shapes: `.ufo/reports/round-52/mori.md` (1 touching commit, add = the above);
`.ufo/reports/round-19/souji.md` (23 touching commits; `cf557a61` adds, `f47ad6ba` re-adds after a tree restore
— only the earliest add is the report commit). Note that `--diff-filter=A` alone is ambiguous under a restore,
which is why the draft takes the earliest.

Checks, in order, both at the fleet root:

    grep -nE '\[FILL\]|TODO:|TBD' .ufo/reports/round-<N>/<id>.md        # before landing: rc 1 = clean
    git log --format=%H -- .ufo/reports/round-<N>/<id>.md | wc -l       # after landing: 1 per landing

The census that motivated the rule, for scale: 741 filed `round-*/*.md` reports under `.ufo/reports/`, exactly
one carrying a literal `[FILL]` — the round-52 mori report. The defect is rare, cheap to grep and invisible to
every lane instrument (nothing in `tools/` or the counters reads report bytes), which is why the convention is
carried as text plus two commands rather than as a tool.
```

## 6. DRAFT B — the round-52 erratum (fenced; append-only, names the superseded text)

Target: appended after the filed bytes of `/home/vgpnk/Projects/shokunin/.ufo/reports/round-52/mori.md` in a new
commit (`PROTOCOL.md:135`), or — the protocol's other legal home — carried verbatim in the round-53 report's
`## Extras and defects` with the same superseded-text naming. This seat writes neither.

```markdown
## Erratum — the report's own commit (appended round 53; nothing above is rewritten)

Two slots in this report hold the literal `[FILL]` where its own commit belongs. The commit that adds this file
is `aacd7a83027cdee8e950a2c39d490feaed3be13c`:

    $ git -C /home/vgpnk/Projects/shokunin log --format='%H %an' -- .ufo/reports/round-52/mori.md
    aacd7a83027cdee8e950a2c39d490feaed3be13c mori-shokunin

It is a fleet-repo commit carrying the lane identity (`mori-shokunin <mori@shokunin.local>`, 2026-10-26
21:55:24 -0300, "round-52: mori report"), report-only (`git show --stat aacd7a83` → 1 file changed, 115
insertions), an ancestor of fleet HEAD, and the only commit that touches the file
(`git log --format=%H -- .ufo/reports/round-52/mori.md | wc -l` → 1; `git diff aacd7a83 HEAD --
.ufo/reports/round-52/mori.md` prints nothing).

- Line 5, superseded text ``… Report commit `[FILL]`.``: the report commit is
  `aacd7a83027cdee8e950a2c39d490feaed3be13c`, resolved by `git log --format=%H --
  .ufo/reports/round-52/mori.md` at the fleet root. Per the round-53 convention (`corpus/lessons/round-53.md`)
  a report names its own commit by that command, never by a placeholder and never by a hash it cannot know at
  write time.
- Line 46, superseded row ``| `[FILL]` | receipts at landed tip: `c1-at-landed.txt`, `c2-at-landed.txt`,
  `census-end.txt` | Round 52 |``: the cells after the commit repeat line 45's description of the lane receipts
  commit `37af57f2` verbatim, so the row as filed describes the wrong commit. It is the fleet report commit
  `aacd7a83027cdee8e950a2c39d490feaed3be13c` (report-only: it touches no receipt file and no `LOG.md`). Resolve it
  to `aacd7a83…`, and never to `37af57f2`, which line 5 already cites as the lane tip.

The two citations stay distinct: `37af57f2` is the lane repo's HEAD when the report was written
(`git ls-remote origin refs/heads/master` prints it), `aacd7a83` is the fleet commit that adds this file. The
verdict of the round is unaffected; this is bookkeeping, and the filed bytes above stand as filed.
```

## 7. Verification run by this seat

| command (cwd) | result |
|---|---|
| `git -C /home/vgpnk/Projects/shokunin log --format='%H %an' -- .ufo/reports/round-52/mori.md` | `aacd7a83027cdee8e950a2c39d490feaed3be13c mori-shokunin` (rc 0) |
| `git log --format=%H -- .ufo/reports/round-52/mori.md \| wc -l` | `1` |
| `git show --stat --format='%H%n%an <%ae>%n%ad%n%s' aacd7a83` | 1 file, 115 insertions, lane identity, `round-52: mori report` |
| `git merge-base --is-ancestor aacd7a83 HEAD` | rc 0 |
| `git diff --stat aacd7a83 HEAD -- .ufo/reports/round-52/mori.md` | empty, rc 0 |
| `grep -rn 'Report commit' .ufo/reports/round-52/` | 1 hit, `mori.md:5` (`[FILL]`); the other five files rc 1 |
| `grep -rln '\[FILL\]' .ufo/reports/round-*/*.md` | 1 of 741 files |
| `git log --format=%H -- .ufo/reports/round-19/souji.md \| wc -l` | `23`; `--diff-filter=A` lists `cf557a61` and `f47ad6ba` |
| `git -C souji-shokunin show --stat 7d199d2b` | `.ufo/waves/round-19/w1/CriticD5.md`, 24 insertions (seat report, not souji's own) |
| `grep -n` of the four precedent lines (`round-10/kengaku.md:5`, `round-11/kengaku.md:7`, `round-48/kake.md:8`, `round-34/kaidoku.md:69`) | present, quoted verbatim in §3 |
| `grep -n` of `PROTOCOL.md:117,125,135`, `AGGREGATE.md:680,1191`, `corpus/QUALITY.md:17` | present |
| `df -h /fast` | 610G free (no heavy run was needed) |

Nothing above is a re-run of lane work: no counter, tool, selftest, census or fixture was executed, and no claim
of round 53 was scored.

## 8. Limits

- The convention is drafted, not landed: DRAFT A and DRAFT B are fenced text and the L1 owns both integrations
  (lesson file, erratum append). I did not create `corpus/lessons/round-53.md` or touch the filed round-52 report.
- The round-53 form (`git log --format=%H -- .ufo/reports/round-53/mori.md`) cannot be exercised yet: the report
  file does not exist (`ls .ufo/reports/round-53/` — no `mori.md`). Its single-hash behaviour is inferred from the
  round-52 analogue (same path shape, one landing commit), not observed for round 53.
- Whether an erratum append to `.ufo/reports/round-52/mori.md` is the L1's chosen home or the round-53 report's
  `## Extras` is the L1's routing decision; `PROTOCOL.md:135` permits both and I verified only that the text names
  the superseded strings at the right lines (`:5`, `:46` of the filed file at `fd697467`).
- The grep guard is literal: a differently spelled placeholder (`PLACEHOLDER`, `??`, an empty commit cell) passes
  it. This matches the sibling scribe's independent limit (`Mo53ScribeMistakes.md:112`) and is not fixed here.
- Fleet HEAD is detached in this work tree, so any convention text that named a branch would be wrong; DRAFT A
  names none, and both commands work on a detached HEAD. Whether the detached state is this session's checkout or
  the repository's steady state is UNVERIFIED here (no mutation performed to find out).
- Lane work-tree state at write time (reported, not touched): `git -C mori-shokunin status --porcelain` lists
  ` M SKILL.md`, ` M corpus/knowledge/commit-runway-read-r53.md`, ` M tools/mori-commit-runway.py`,
  ` M tools/fixtures/mori-commit-runway/cases.json`, and untracked `.ufo/waves/round-53/w1.ready`,
  `w1.ready.dispatched`, `w1/`, `evidence/selftests/` — sibling-seat activity during the wave. This seat's only
  write is this report file; the lane tip read for §1 (`95cf78ee`) is therefore the committed tip, not the working
  tree.

## Findings

- **MED — the task premise, `.ufo/reports/round-52/` (all six files).** No sibling round-52 report cites its own
  commit under `Report commit`: `grep -rn 'Report commit'` over the directory returns exactly one hit, `mori.md:5`,
  and it is the `[FILL]` defect itself. The convention therefore cannot be drafted "in the siblings' manner"; §3
  grounds it on `round-10/kengaku.md:5`, `round-11/kengaku.md:7`, `round-48/kake.md:8`, `round-34/kaidoku.md:69`
  plus `PROTOCOL.md:117/125/135` and `AGGREGATE.md:680/1191`. Five of six siblings omit the slot entirely.
- **MED — `.ufo/reports/round-52/mori.md:46`.** The `[FILL]` row repeats line 45's `37af57f2` description, so the
  obvious resolution (drop the lane tip into the cells) yields a duplicate row and a false citation; the row is
  the fleet report commit `aacd7a83…`, report-only. DRAFT B says this explicitly.
- **LOW — `.ufo/reports/round-19/souji.md` vs `.ufo/reports/round-52/mori.md`.** `--diff-filter=A` is not unique
  under a tree restore (`f47ad6ba` re-adds after stray commit `35b91714`; 23 commits touch the file), so the
  convention's primary command is exact only for a single-landing report; the earliest-add form is the general
  one. Drafted into DRAFT A's second paragraph.
- **LOW — fleet repo `/home/vgpnk/Projects/shokunin`, `git rev-parse --abbrev-ref HEAD` → `HEAD`.** The fleet
  work tree is detached at `fd697467`; convention text must not name a branch, and the two commands it carries do
  not. Cause of the detached state not investigated (read-only seat).
- **LOW — census, `.ufo/reports/round-*/*.md`.** 1 of 741 filed reports carries a literal `[FILL]` (the round-52
  mori report); the token is caught only by `grep`, since no lane instrument reads report bytes
  (`Mo53ScribeMistakes.md:100` says the same). The convention's two commands are the whole check.
- **LOW — `corpus/QUALITY.md:17` (criterion 9).** The existing rule ("every … commit pointer resolves at the
  carrying commit") already forbids `[FILL]` but was not applied to a report's own commit; DRAFT A is its
  extension for this one slot and needs no new QUALITY item (sibling drafts 144+ cover the criteria; this is the
  text side).
