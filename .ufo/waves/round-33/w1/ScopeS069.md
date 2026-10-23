# S069 scope review

Axes: source attribution; clause coverage; minimal correction.

## Behavior and gates
- This is a scoped audit, not a product change. The frozen S069 rule recommends lexical path rejection before filesystem access and separate symlink tests; the proposed edit labels those actions as lane doctrine rather than page teaching.
- No build, tests, counter, or judge were run. No source URL was fetched; the existing recheck copy was inspected. No tool was installed or updated. `/home/vgpnk/.omp/agent/RULES.md:1-14` was read first.

## Provenance
- Read-only lookup command: `timeout 30s git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 7d382043:corpus/SOURCES.md | grep -n '^| S069 '`.
- Its output was line 75, the frozen S069 row reproduced below. The round-32 recheck row is `corpus/lessons/round-32.md:46`; saved page copy is `corpus/evidence/recheck-r32/S069.src`.

## Findings

The scope cell describes page material, not lane doctrine. The saved page distinguishes lexical `PurePath.relative_to()` from resolution and documents the symlink caveat (`corpus/evidence/recheck-r32/S069.src:918-922, 2327-2330`). The claim that string-only containment does not inspect the filesystem and assumes symlinks absent is supported at `S069.src:918-922`.

The teaches cell has two lane-application clauses:
1. “reject absolute and .. lexically before any filesystem call” — JudgeRecheck itself calls this the lane's tool rule (`.ufo/waves/round-32/judge/JudgeRecheck.md:68`). The page explains `relative_to()` behavior and a `resolve()` caveat; it does not state this lane's pre-filesystem rejection rule (`S069.src:902-922, 2327-2330`).
2. “test symlinks separately” — lane testing policy, not a statement of the page's API behavior (`S069.src:918-922`; the closure lists S069 among the undeclared lane-inference/application findings at `corpus/lessons/round-32-verifier-spotcheck.md:100-104, 190-192`).

The other teaches clause, “String-only containment cannot see symlinks,” is a page-backed paraphrase of the PurePath string-only / no-filesystem-access description and the warning about symlinks (`S069.src:918-922`).

### Old and proposed cells

Old scope cell, from frozen row `7d382043:corpus/SOURCES.md:75`:
```text
lexical versus resolved path containment and the symlink caveat
```

Proposed scope cell (unchanged):
```text
lexical versus resolved path containment and the symlink caveat
```

Old teaches cell, from frozen row `7d382043:corpus/SOURCES.md:75`:
```text
String-only containment cannot see symlinks: reject absolute and .. lexically before any filesystem call, and test symlinks separately.
```

Proposed teaches cell (inserted only `lane rule: `; all other words and punctuation retained):
```text
String-only containment cannot see symlinks: lane rule: reject absolute and .. lexically before any filesystem call, and test symlinks separately.
```

Old-to-new diff:
```diff
-String-only containment cannot see symlinks: reject absolute and .. lexically before any filesystem call, and test symlinks separately.
+String-only containment cannot see symlinks: lane rule: reject absolute and .. lexically before any filesystem call, and test symlinks separately.
```

## Judge-reason conflict

Yes. The frozen S069 teaches cell lacks an own-rule disclaimer (`7d382043:corpus/SOURCES.md:75`), but JudgeRecheck S069 says “lexical-reject rule is the lane's tool rule (superseding S073 says so)” (`.ufo/waves/round-32/judge/JudgeRecheck.md:68`). The closure explicitly records that S069's reason “imports S073's own-rule disclaimer, but S069's frozen cell lacks it” (`corpus/lessons/round-32-verifier-spotcheck.md:103-104`). S073 supplies that disclaimer at `corpus/SOURCES.md:79`; S074 and S076 also declare their lane boundary/application in their teaches cells at `corpus/SOURCES.md:80,82`.

## Touched surfaces and limits

- Read-only surfaces: frozen source row, round-32 recheck row/copy, closure note, JudgeRecheck reason, and comparison rows S073/S074/S076.
- Written surface: `.ufo/waves/round-33/w1/ScopeS069.md` only. No source row, judge, counter, commit, or other lane file was changed.
- Out of scope: adjudication and any counter execution; the L1 remains responsible for those.

Artifact: `.ufo/waves/round-33/w1/ScopeS069.md`.
