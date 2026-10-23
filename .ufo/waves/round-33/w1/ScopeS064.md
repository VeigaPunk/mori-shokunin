# S064 scope audit — routed round-32 defect 3

Axes reviewed: source-support fidelity and lane-scope clarity.

## Provenance and surfaces

- Base row command: `timeout 60s git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 7d382043:corpus/SOURCES.md`. Its output contains the S064 row reproduced below (registry line 70); the source cell matches the current row at `corpus/SOURCES.md:70`.
- Round-32 recheck: `corpus/lessons/round-32.md:43` records S064's URL, access time, SHA-256 and three quotes, with verdict `current`.
- Committed page copy: `corpus/evidence/recheck-r32/S064.src`; relevant passages and exact locators are quoted below.
- The closure records CriticScopingRows' S064 finding as unadjudicated: `corpus/lessons/round-32-verifier-spotcheck.md:100-104,190-192`.
- Comparison patterns: S073, S074 and S076 explicitly separate the source statement from a lane rule in their teaches cells (`corpus/SOURCES.md:79-82`). Round 22 had already recorded that S064's immutable teaches cell over-attributes blob binding to the page; the reconciler uses lane code (`corpus/lessons/round-22.md:69-72`).
- Git-scm's URL was already registered at the base, so I did not fetch or add a source. No tool was installed. No product code, registry row, judge, commit, or test was changed/run. The only written artifact is this report.

## Clause findings

Page-supported material in the committed copy:

- `S064.src:2720-2722` (18 words): "Verify that exactly one parameter is provided, and that it can be turned into a raw 20-byte SHA-1"
- `S064.src:2729` (8 words): "names an existing object that is a commit-ish"
- `S064.src:2736` (12 visible words): "wise to use <span class='synopsis'><code>--end-of-options</code></span> so that the name argument is not mistaken"
- `S064.src:3061` (8 words): "The full SHA-1 object name (40-byte hexadecimal string)"
- `S064.src:3763` (13 words): "Print the commit object name from the revision in the $REV shell variable"

The copy thus supports `--verify`, the end-of-options safeguard, commit-type peeling, existing commit-object resolution, and an emitted full SHA-1 name. It does not state that the lane must resolve only once, retain that result, compare loaded register/correction bytes against blobs, or treat the printer alone as proof of those bytes. The page discusses trees/blobs and remote-tracking refs elsewhere, but those passages do not assert the row's input-byte binding or remote publication/authenticity. The lane procedure is separately stated in `corpus/lessons/round-19.md:52-60`; the over-attribution is explicitly corrected at `corpus/lessons/round-22.md:69-72`.

1. **Scope — `C2 resolving an explicit selector to an existing commit object`.** `C2` is the lane's scope label, not wording from the page. The underlying resolution-to-existing-commit statement is supported by the `--verify`/commit-ish quotes above.
2. **Scope — `not remote publication, source authenticity or input-tree equality`.** These are lane scope exclusions, not statements by git-rev-parse. No located quote in the committed copy states these exclusions; declare them as lane rules.
3. **Teaches — `Resolve a selector once with --verify --end-of-options and commit peeling`.** The flags and commit peeling are supported as described above; `once` is a lane procedure choice, not a documented property.
4. **Teaches — `retain the full object id`.** The page documents the full SHA-1 object name/output, but not the lane's instruction to retain it. The retention action is lane procedure.
5. **Teaches — `then separately bind the actual loaded register/correction bytes to blobs at that commit`.** Lane application, not page content. Round 19 states the binding requirement; round 22 says the reconciler's blob binding rests on lane code, not S064 (`corpus/lessons/round-19.md:52-60`; `corpus/lessons/round-22.md:69-72`).
6. **Teaches — `a hash printer alone does not prove the latter`.** Lane inference about the boundary of commit resolution versus input provenance, not a statement on this page. The page's resolution examples do not describe the loaded register/correction bytes.

## Old cells and proposed cells

Old scope cell:
```text
C2 resolving an explicit selector to an existing commit object; not remote publication, source authenticity or input-tree equality
```

Proposed scope cell (all original wording retained; lane boundaries declared):
```text
C2 resolving an explicit selector to an existing commit object; not remote publication, source authenticity or input-tree equality. Lane rule: C2 labels the lane's use of the page; the three exclusions delimit that use, not claims made by git-rev-parse.
```

Old teaches cell:
```text
Resolve a selector once with --verify --end-of-options and commit peeling, retain the full object id, then separately bind the actual loaded register/correction bytes to blobs at that commit; a hash printer alone does not prove the latter.
```

Proposed teaches cell (all original wording retained; non-page steps declared):
```text
Resolve a selector once with --verify --end-of-options and commit peeling, retain the full object id, then separately bind the actual loaded register/correction bytes to blobs at that commit; a hash printer alone does not prove the latter. Lane rule: “once” and retaining the id are procedure choices; binding the actually loaded register/correction bytes to blobs, and the hash-printer limitation, are lane application, not claims made by git-rev-parse.
```

Old → proposed diff:
```diff
- C2 resolving an explicit selector to an existing commit object; not remote publication, source authenticity or input-tree equality
+ C2 resolving an explicit selector to an existing commit object; not remote publication, source authenticity or input-tree equality. Lane rule: C2 labels the lane's use of the page; the three exclusions delimit that use, not claims made by git-rev-parse.
- Resolve a selector once with --verify --end-of-options and commit peeling, retain the full object id, then separately bind the actual loaded register/correction bytes to blobs at that commit; a hash printer alone does not prove the latter.
+ Resolve a selector once with --verify --end-of-options and commit peeling, retain the full object id, then separately bind the actual loaded register/correction bytes to blobs at that commit; a hash printer alone does not prove the latter. Lane rule: “once” and retaining the id are procedure choices; binding the actually loaded register/correction bytes to blobs, and the hash-printer limitation, are lane application, not claims made by git-rev-parse.
```

## Limits

This report proposes transparent cell wording; it does not adjudicate the routed finding or modify the immutable row. No URL fetch, judge run, source-counter run, test, build, or lint was performed. The source-support finding is bounded to the committed copy and cited passages.