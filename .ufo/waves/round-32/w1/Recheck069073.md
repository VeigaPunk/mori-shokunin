# Round-32 C1 recheck — S069, S073

Seat: `MoriR32A2.Recheck069073`. Population url (both ids): https://docs.python.org/3/library/pathlib.html
Population rows read from `.ufo/waves/round-32/c1-population.json` (`population[].id`); SOURCES rows at
`corpus/SOURCES.md:75` (S069) and `corpus/SOURCES.md:79` (S073).
Fetched with `curl -sSL --fail -m 60` (curl 8.23.0), one attempt needed for each id, HTTP 200, no redirect
(`%{url_effective}` == the population url). Tools installed this run: none (python3 3.14.8, curl 8.23.0 pre-existing).

## 1. Copies

| id | url | accessed (UTC) | bytes | sha256 | scratch copy |
|---|---|---|---|---|---|
| S069 | https://docs.python.org/3/library/pathlib.html | 2026-10-23T01:31:30Z | 271189 | a5cfbc6b1fc4d570c434f1b737547ea87a3f964dd79b15e42ff01627b6fe85f0 | /fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck069073/S069.src |
| S073 | https://docs.python.org/3/library/pathlib.html | 2026-10-23T01:31:35Z | 271189 | a5cfbc6b1fc4d570c434f1b737547ea87a3f964dd79b15e42ff01627b6fe85f0 | /fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck069073/S073.src |

Bytes are the untouched curl output; `sha256sum S069.src S073.src` printed the same 64-hex for both (one copy per id
rule, same bytes). Normalised text saved for quoting at the same scratch dir `S069.norm.txt` (60950 bytes), produced by
`python3 .ufo/waves/round-32/seat-check.py text S069.src`. Every quote below is copied verbatim from that output.
Fetch transcript: `S069.curlerr.txt` is empty (no failures). The page self-identifies as **Python 3.15.1
documentation** (`grep -o 'Python 3.15.[0-9]* documentation'` → `Python 3.15.1 documentation`); the population anchor
of both rows says 3.15.0. Substance of the cited passages is unchanged — see note in §5.

## 2. Ready-to-paste rows

```markdown
| S069 | https://docs.python.org/3/library/pathlib.html | 2026-10-23T01:31:30Z | a5cfbc6b1fc4d570c434f1b737547ea87a3f964dd79b15e42ff01627b6fe85f0 | "This function is part of PurePath and works with strings. It does not check or access the underlying file structure."; "it assumes that no symlinks are present in the path; call resolve() first if necessary to resolve symlinks"; "When walk_up is false (the default), the path must start with other" | current |
| S073 | https://docs.python.org/3/library/pathlib.html | 2026-10-23T01:31:35Z | a5cfbc6b1fc4d570c434f1b737547ea87a3f964dd79b15e42ff01627b6fe85f0 | "This function is part of PurePath and works with strings. It does not check or access the underlying file structure."; "it assumes that no symlinks are present in the path; call resolve() first if necessary to resolve symlinks"; "This can impact the walk_up option as it assumes that no symlinks are present in the path" | current |
```

## 3. What each quote bears on

S069 teaches cell: "String-only containment cannot see symlinks: reject absolute and .. lexically before any filesystem
call, and test symlinks separately."

- Q1 (`This function is part of PurePath and works with strings. It does not check or access the underlying file
  structure.`) bears on "String-only containment cannot see symlinks" and on "before any filesystem call": `PurePath`
  is documented as string-only and as never consulting the filesystem, so a containment test built on it cannot observe
  a symlink and needs no stat. Normalised `S069.norm.txt:18020`.
- Q2 (`it assumes that no symlinks are present in the path; call resolve() first if necessary to resolve symlinks`)
  bears on "test symlinks separately": the `relative_to(walk_up=True)` Warning names the symlink assumption and the
  remedy (`resolve()` first). `S069.norm.txt:18153`. This is the same sentence round-20 recorded
  (`corpus/lessons/round-20.md:48`), so no drift since admission.
- Q3 (`When walk_up is false (the default), the path must start with other`) bears on "reject absolute and .. lexically":
  with `walk_up=False` the path must start with `other`, so an absolute non-subpath or a `..` escape raises
  `ValueError` before any filesystem call; the PurePath section on `foo/../bar` (`S069.norm.txt:5044`) states `..` is not
  collapsed, because doing so "is wrong if foo is a symbolic link to another directory". That is lexical rejection of
  `..`, exactly the cell's second clause.
- Verdict `current`: every clause of the teaches cell is still stated by the live page; nothing it says contradicts the
  cell. The operational ordering "before any filesystem call" is the corollary of Q1, and S073 already records that the
  rejection policy itself belongs to mori's tool rule (no new drift) — see §5.

S073 teaches cell: "supersedes S069 — string-only containment (relative_to with walk_up) assumes no symlinks; resolve()
first if needed. Rejecting .. and absolute trailer paths before any stat is mori's own tool rule, not taught by this
page."

- Q1 bears on "string-only containment (relative_to with walk_up)": the page states the method "works with strings" and
  "does not check or access the underlying file structure" (`S069.norm.txt:18020`) — the narrowed claim is exactly the
  page's own wording.
- Q2 bears on "assumes no symlinks; resolve() first if needed": the Warning says walk_up "assumes that no symlinks are
  present in the path; call resolve() first if necessary to resolve symlinks" (`S069.norm.txt:18153`).
- Q3 (`This can impact the walk_up option as it assumes that no symlinks are present in the path`) bears on the scope
  cell "symlink caveat of lexical containment only": the caveat is attached to the `walk_up` option specifically, not to
  containment at large — the narrowing S073 claims.
- Verdict `current`: the Warning that names `walk_up` still exists, still carries the symlink caveat and the `resolve()`
  remedy, and says nothing about rejecting absolute paths — consistent with S073's "not taught by this page".

## 4. seat-check output (verbatim)

S069:

```
sha256=a5cfbc6b1fc4d570c434f1b737547ea87a3f964dd79b15e42ff01627b6fe85f0
quotes=3 words=[20, 18, 12] in_copy=[True, True, True]
shared_tokens=['call', 'path', 'purepath', 'symlinks', 'walk'] topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
exit=0
```

S073:

```
sha256=a5cfbc6b1fc4d570c434f1b737547ea87a3f964dd79b15e42ff01627b6fe85f0
quotes=3 words=[20, 18, 17] in_copy=[True, True, True]
shared_tokens=['assumes', 'first', 'purepath', 'resolve', 'symlinks', 'walk'] topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
exit=0
```

(`live_quotes_ok=True` is the helper's own fresh fetch of the population url, i.e. the counter's R3 live leg already
passes for both rows. R4 judge and R5 drifted-correction are out of scope here: no drifted row.)

## 5. Drift / notes

- No substantive drift: the Q2 sentence matches the text recorded at admission in `corpus/lessons/round-20.md:48`
  word-for-word after normalisation, and `corpus/lessons/round-20.md:49` records the same quote for S073.
- Version label observed, not a substance change: the live page is "Python 3.15.1 documentation" while both population
  anchors say "Python 3.15.0 docs". The `PurePath.relative_to` paragraph, its `walk_up` samples and the Warning are
  unchanged; the teaches cells make no patch-version claim, so both verdicts stay `current`. [INFERENCE] A future round
  may want to refresh the anchor version string; no `Round32` correction is drafted because no knowledge entry's claim
  is altered.
- No redirect: HTTP 200 from the population url itself, so the url cell is the fetched url.
- No tools installed or updated this run; no processes left running (all commands wrapped in `timeout`).

## Gaps

- None for this ticket. Only R4's semantic judge and R5's Round32-line rule remain for L1 to run at integration; both
  rows are `current`, so R5 should not apply.
