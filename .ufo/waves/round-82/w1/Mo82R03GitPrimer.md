# Mo82R03GitPrimer — git primitives the C3 revision arm relies on

Seat: `Mo82R03GitPrimer` (leaf scout; no subagent dispatch). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Entering revision: `ebcf2c72df203c855cfafb5223c6e22b1e12c481`. Probe window: 2026-11-04T04:44–04:57 -03:00.
Host: `git version 2.56.0`, Python 3.14.8, Linux 7.2.11-arch1-1.
Scope: one bounded, read-only probe in a scratch fixture. **No lane file was changed except this report.**
No commit, push, checkout, reset, stash or other mutating git/jj command was run in the lane.

## Hypothesis under test (falsifiable)

> `git -C <repo> show <rev>:<path>` alone is a sufficient, unambiguous primitive for the revision
> arm's four failure modes — row-value, rev-unresolvable, path-absent, rev-bytes — and its exit
> codes distinguish them without parsing stderr.

**Verdict: falsified as stated. A three-call, exit-code-only sequence is sufficient and is the
robust choice.** Details and evidence below.

## Fixture (recipe; scratch deleted after the probe)

```
S=/fast/scratch/hyaku/mori-r82/Mo82L01SourceProbe
mkdir -p "$S"; D=$(mktemp -d -p "$S")
git init -q -b master "$D"
test "$(git -C "$D" rev-parse --show-toplevel)" = "$D"     # asserted before the first commit
# commit A: SCORECARD.md = "| row | pointers=237 |", docs/a b c.md, tools/x.py,
#           a:b.md, ü.md, -file.md, crlf.md, notrail.md ("k=1" no LF), eol.txt
#           (.gitattributes: "*.txt text eol=crlf")
# commit B: SCORECARD.md = "| row | pointers=240 |"
# commit C: bin.dat = b"a\0b\n", link.md -> SCORECARD.md
```

Measured: commit A `0b43e7386d3b706c681606eb1402861f187fb2c0`, commit B
`75904c77972862185518e0ca3ca45d87fbc4eb82`, A8 `0b43e738`, branch `master`.
A second/third repo were initialised with `git -c init.defaultBranch=main init` and
`…=trunk`. A 3000-commit `git fast-import` stream produced 9422 objects / 3404 commits and 606
four-hex prefix collisions (for the ambiguity probe).

---

## 1. Unresolvable rev — rc and stderr shape

All commands prefixed `git -C "$D"`.

| command | rc | stderr (exact shape) |
|---|---|---|
| `rev-parse --verify deadbeef^{commit}` | **128** | 1 line: `fatal: Needed a single revision` |
| `rev-parse --verify --quiet deadbeef^{commit}` | **1** | empty (0 lines) |
| `rev-parse --verify 0000…0^{commit}` (40 zeros) | 128 | `fatal: Needed a single revision` |
| `rev-parse --verify --quiet 0000…0^{commit}` | 1 | empty |
| `rev-parse --verify HEAD~99^{commit}` | 128 | `fatal: Needed a single revision` |
| `rev-parse --verify --quiet HEAD~99^{commit}` | 1 | empty |
| `rev-parse --verify ^{commit}` (empty rev) | 128 | `fatal: Needed a single revision` |
| `rev-parse --verify <tree>^{commit}` | 128 | 2 lines: `error: <tree>^{commit}: expected commit type, but the object dereferences to tree type` + `fatal: Needed a single revision` |
| `show deadbeef:SCORECARD.md` | 128 | `fatal: invalid object name 'deadbeef'.` |
| `show HEAD~99:SCORECARD.md` | 128 | `fatal: invalid object name 'HEAD~99'.` |
| `show 0000…0:SCORECARD.md` | 128 | **`fatal: path 'SCORECARD.md' exists on disk, but not in '0000…0'`** — a *path* message for an unresolvable rev |
| `show SCORECARD.md:whatever` (rev is a path) | 128 | `fatal: invalid object name 'SCORECARD.md'.` |
| `cat-file -e deadbeef:SCORECARD.md` | 128 | `fatal: invalid object name 'deadbeef'.` |
| `cat-file -t deadbeef:SCORECARD.md` | 128 | same |
| `cat-file -e 0000…0` (no colon; valid syntax, missing object) | **1** | empty |
| `cat-file -e deadbeef` (short invalid name) | 128 | `fatal: Not a valid object name deadbeef` |
| `cat-file -t 0000…0` | 128 | `fatal: git cat-file: could not get object info` |

Ambiguous short prefix (measured prefix `0244`, two commits `02443fbc…`, `0244fb07…`):

| command | rc | stderr |
|---|---|---|
| `rev-parse --verify 0244^{commit}` | 128 | 5 lines: `error: short object ID 0244 is ambiguous` + 3 `hint: The candidates are:`/`hint:   02443fb commit 2023-11-14 - f746` lines + `fatal: Needed a single revision` |
| `rev-parse --verify --quiet 0244^{commit}` | **1** | empty — `--quiet` suppresses even the ambiguity hint |
| `show 0244:f.txt`, `cat-file -e 0244:f.txt`, `cat-file -t 0244:f.txt` | 128 | the same 5-line ambiguity text |

**Trap:** the 40-zero case shows stderr text alone misroutes an unresolvable rev to path-absent.
The ambiguity hint text contains user-controlled commit subjects — another reason never to parse it.

## 2. Path absent at a valid rev

| command (`A` = full commit A) | rc | stderr |
|---|---|---|
| `show A:nope.md` | 128 | `fatal: path 'nope.md' does not exist in '<A>'` |
| `show A:tools/nope.py` | 128 | `fatal: path 'tools/nope.py' does not exist in '<A>'` |
| `show A:SCORECARD.md/nope` | 128 | `fatal: path 'SCORECARD.md/nope' does not exist in '<A>'` |
| `cat-file -e A:nope.md` | **128** | same path message — **not 1** |
| `cat-file -t A:nope.md` | 128 | same path message |
| `rev-parse --verify A:nope.md` | 128 | `fatal: Needed a single revision` (no path detail) |
| `rev-parse --verify --quiet A:nope.md` | 1 | empty |

So `cat-file -e` is **not** the path-exists predicate the docs suggest: for a missing path it
returns 128, and it returns 0 for a tree. Its rc vocabulary is inconsistent across cases
(`1` for a syntactically valid missing object, `128` for missing paths and invalid names).

## 3. Path that is a directory at the rev (falsifies `show` as a bytes read)

```
$ git -C "$D" show A:tools ; echo rc=$?
tree 0b43e7386d3b706c681606eb1402861f187fb2c0:tools

x.py
rc=0
```

- rc **0**, stdout is a 3-line *tree listing*; final line `x.py`.
- `cat-file -e A:tools` → rc 0. `cat-file -t A:tools` → `tree` (rc 0).
- `rev-parse --verify A:tools` → rc 0, tree oid `2b3924c5757894df4be7c474b64f596717d1ca63`.
- `show A:` (empty path) → rc 0, root tree listing (12 lines, names incl. `docs/`, `tools/`).
- `cat-file -e A:tools/` → rc 0.

**A tree path can pass a `key=value` byte search.** Measured end-to-end: a repo with
`dir/survivors=0` committed, `git show <rev>:dir` prints `tree <sha>:dir\n\nsurvivors=0\n`, rc 0,
and the live arm's own `contains_value("survivors", 0)` regex matches that listing. A gitlink is
worse: `cat-file -t HEAD:sub` → `commit`; `show HEAD:sub` → rc 0 and a full commit object dump
(`commit <sha>\nAuthor: …`), i.e. arbitrary commit-message text is searchable as if it were the
file's bytes. **The type guard (`-t` == `blob`) is mandatory.**

## 4. Path with a space, 8-hex prefix, `<branch>~1`, and path shapes

| command | rc | output |
|---|---|---|
| `show A:docs/a b c.md` | 0 | `n=1\n` (space in path is fine; one argv) |
| `rev-parse --verify --quiet 0b43e738^{commit}` | 0 | full 40-hex + LF (41 bytes) |
| `show 0b43e738:SCORECARD.md` | 0 | `| row | pointers=237 |` |
| `show master~1:SCORECARD.md` (master repo) | 0 | `pointers=237` |
| `rev-parse --verify master~1^{commit}` | 0 | == A |
| `show A:a:b.md` | 0 | `c=1` (split is at the first colon after the rev; colons in the path are fine) |
| `show A:ü.md` | 0 | `u=1` |
| `show A:-file.md` | 0 | `d=1` (dash after the colon is not an option) |
| `show A:./SCORECARD.md` with `-C "$D"` | 0 | `pointers=237` (`./` resolves against `-C`'s cwd = repo root) |
| `git show A:./SCORECARD.md` from `$D/docs` (no `-C`) | 128 | `fatal: path 'docs/SCORECARD.md' does not exist in '<A>'` |
| `git show A:../SCORECARD.md` from `$D/docs` (no `-C`) | 0 | `pointers=237` — **`./` and `../` are cwd-relative** |
| `show A:docs/../SCORECARD.md` | 128 | `fatal: path 'docs/../SCORECARD.md' exists on disk, but not in '<A>'` — interior `..` is literal, not normalised |
| `show A:/SCORECARD.md` | 128 | leading `/` is not accepted as root-relative |
| `show A:../../etc/passwd` | 128 | `fatal: '../../etc/passwd' is outside repository at '<D>'` |

Default-branch matrix (measured in repos initialised with `init.defaultBranch` = `master`, `main`,
`trunk`):

| repo HEAD | `<HEAD>~1` | `master~1` | `main~1` | `trunk~1` | 8-hex rev |
|---|---|---|---|---|---|
| master | 0 | 0 | 1 | 1 | 0 |
| main | 0 | 1 | 0 | 1 | 0 |
| trunk | 0 | 1 | 1 | 0 | 0 |

`HEAD~1` and a resolved sha are branch-agnostic; **`master~1` / `main~1` are not**. The arm never
needs to synthesize a ref: it consumes the pins' `rev`, so the only default-branch hazard would be
inventing `HEAD` or a branch name. Do not.

## 5. `cat-file -e` present vs absent

| case | rc |
|---|---|
| `cat-file -e A:SCORECARD.md` (blob) | **0** |
| `cat-file -e A:tools` (tree) | **0** |
| `cat-file -e A:nope.md` (absent path, valid rev) | **128** |
| `cat-file -e 0000…0` (no colon, missing object) | **1** |
| `cat-file -e deadbeef` (short invalid name) | **128** |
| `cat-file -t A:SCORECARD.md` | 0, `blob` |
| `cat-file -t A:tools` | 0, `tree` |
| `cat-file -t A:nope.md` | 128 |

**Never test for `rc == 1`.** Positive predicate is `rc == 0`; any nonzero is failure. On this git
a missing *path* is 128, and `cat-file -e` accepts trees, so existence without a type check is
insufficient.

## 6. Byte fidelity of the revision read (rev-bytes mode)

| object | `show <rev>:<path>` | `cat-file blob <rev>:<path>` | worktree |
|---|---|---|---|
| `eol.txt` (attr `*.txt text eol=crlf`) | `b'x=1\n'` sha `98752ee2…` | sha `98752ee2…` (equal) | `b'x=1\r\n'` (smudged) |
| `notrail.md` (committed `b'k=1'`) | `b'k=1'`, len 3 (no LF appended) | same | same |
| `crlf.md` | `b'k=1\r\nsecond\r\n'` | same | same |
| `bin.dat` | `b'a\x00b\n'` (NUL preserved) | same | same |
| `link.md` (symlink) | type `blob`, bytes `b'SCORECARD.md'` (target text, no LF) | same | symlink |

`show` and `cat-file blob` produce identical bytes for a blob (sha256 equal). Revision bytes are
the **object** bytes: no `.gitattributes` smudge, no newline addition, no CRLF conversion.
A tree/gitlink is the exception (see §3), which is why the type check comes first.

**Python capture hazard:** `subprocess.run(..., text=True)` translates newlines. Measured:
`printf 'a\r\nb'` → `text=True` gives `'a\nb'`; bytes give `b'a\r\nb'`. The live arm's
`run_command` uses `text=True, encoding='utf-8', errors='replace'`
(`tools/mori-record-sweep.py:155-159`), so it is not reading revision bytes, only a
newline-normalised UTF-8 approximation. ASCII `key=<int>` tokens happen to survive, but the claim
is about bytes. Capture bytes and search `b'%s=%d' % (key, value)`.

## 7. Ambiguities that change what `<rev>:<path>` means

**Replace refs.** With `git replace A B` in the fixture:

| command | result |
|---|---|
| `show A:SCORECARD.md` | `b'| row | pointers=240 |\n'` (B's bytes) — rc 0 |
| `--no-replace-objects show A:SCORECARD.md` | `b'| row | pointers=237 |\n'` — the named revision's bytes |
| `cat-file blob A:SCORECARD.md` | B's bytes |
| `--no-replace-objects cat-file blob A:SCORECARD.md` | A's bytes |

`--no-replace-objects` is a **global** option: it must precede the subcommand. Placing it after
`show` gives rc 128 `fatal: unrecognized argument: --no-replace-objects` (measured). The lane
currently has no `refs/replace` refs (`git -C <lane> for-each-ref refs/replace` → empty), is not
shallow, has no `objects/info/alternates`, and has no promisor config; but "the bytes of the
revision it names" is only well-defined with replace objects disabled (or verified absent).

## 8. Locale robustness (`LC_ALL`)

A `de_DE.UTF-8` locale was generated with
`localedef -i de_DE -f UTF-8 $S/locales/de_DE.UTF-8` and used via `LOCPATH=$S/locales`
(`/usr/share/locale/de/LC_MESSAGES/git.mo` is installed, so git is translated).

| command | `LC_ALL=C` / `en_US.utf8` | `LC_ALL=de_DE.UTF-8` | rc all |
|---|---|---|---|
| `show deadbeef:SCORECARD.md` | `fatal: invalid object name 'deadbeef'.` | `Schwerwiegend: ungültiger Objektname 'deadbeef'.` | 128 |
| `show 0000…0:SCORECARD.md` | `fatal: path 'SCORECARD.md' exists on disk, but not in '0000…0'` | `Schwerwiegend: Pfad 'SCORECARD.md' befindet sich im Dateisystem, aber nicht in '0000…0'` | 128 |
| `show A:nope.md` | `fatal: path 'nope.md' does not exist in '<A>'` | `Schwerwiegend: Pfad 'nope.md' existiert nicht in '<A>'` | 128 |
| `rev-parse --verify deadbeef^{commit}` | `fatal: Needed a single revision` | `Schwerwiegend: Benötigte einen einzelnen Commit` | 128 |
| `rev-parse --verify --quiet deadbeef^{commit}` | *(empty)* | *(empty)* | **1** |
| `cat-file -e A:nope.md` | path message | translated path message | 128 |

Exit codes are invariant; stderr text is not, and the zero-zero case is path-shaped even in `C`.
`--quiet` is the only text-free failure signal. Set `LC_ALL=C` in the child for deterministic
diagnostics, but **classify on rc only**.

## 9. Repo discovery / environment hazards

| command / env | rc | stderr |
|---|---|---|
| `git -C <nonexistent> show HEAD:SCORECARD.md` | 128 | `fatal: cannot change to '…': No such file or directory` |
| `git -C <regular file> …` | 128 | `fatal: cannot change to '…': Not a directory` |
| `git -C <dir not a repo> …` | 128 | `fatal: not a git repository (or any parent up to mount point /)` |
| `GIT_DIR=/nonexistent/gitdir git -C <lane> show …` | 128 | `fatal: not a git repository: '/nonexistent/gitdir'` — **env overrides `-C` discovery** |
| `GIT_OBJECT_DIRECTORY=/nonexistent/objects git -C <lane> show …` | 128 | `fatal: not a git repository (or any parent up to mount point /)` |

The arm must scrub `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`,
`GIT_ALTERNATE_OBJECT_DIRECTORIES`, `GIT_COMMON_DIR`, `GIT_NAMESPACE`, `GIT_CEILING_DIRECTORIES`
and `GIT_PREFIX` from the child environment, and run one setup probe
(`git -C DIR rev-parse --git-dir`) so a broken repo/`safe.directory`/missing git is a **setup
exit 2**, not a per-binding `rev-unresolvable`.

SHA-256 repos (measured: `git init --object-format=sha256`): `rev-parse --verify --quiet
<rev>^{commit}` prints a **64-hex** id (len 64), and `<sha>:SCORECARD.md` + `cat-file -t/-blob`
work unchanged. Do not hardcode 40 hex; use rev-parse's stdout (or accept `[0-9a-f]{40,64}`).

---

## Real-lane calibration — A1 frozen population

The contract was amended at 04:44 (A1, `.ufo/waves/round-82/contract.md:183-199`) after the freeze
commit. The **current** frozen population is the A1 table (`contract.md:196-198`), verified here
against the lane at 04:51 (read-only; another seat was editing `SCORECARD.md` concurrently, so
line numbers may shift at landing; row text is stable history):

| row_contains | matching table rows | exact token present | first `key=` on that row (r81 `stated_value`) | rev resolves | `cat-file -t` | token occurrences at rev |
|---|---|---|---|---|---|---|
| `row_tally=19` (SCORECARD.md:4051) | 1 | yes | 19 | 0, `075574c83eae…` | `blob` | 1 |
| `survivors=0` (SCORECARD.md:4052) | 1 | yes | **2** | 0, `075574c83eae…` | `blob` | 1 |
| `wrong=0 fixtures=7` (SCORECARD.md:4120) | 1 | yes | **7** | 0, `482dc48d…` | `blob` | 1 |

Commands (lane root `L=/home/vgpnk/Projects/shokunin/mori-shokunin`):
`git -C "$L" rev-parse --verify --quiet --end-of-options <rev>^{commit}`,
`git -C "$L" cat-file -t --end-of-options <sha>:SCORECARD.md`,
`git -C "$L" cat-file blob --end-of-options <sha>:SCORECARD.md`.

**Row-value landmine (measured, important):** the A1 rows for `survivors=0` and `wrong=0
fixtures=7` each carry **two** values for the same key — the stale "before" token first
(`survivors=2`, `wrong=7`) and the frozen "after" token later (`survivors=0`, `wrong=0`). The
contract's interface says the first matching row "must state `key=value`" (presence,
`contract.md:143-147`). The r81 helper `stated_value` (`tools/mori-record-sweep.py:49-61`)
returns the **first regex capture**, which is 2 and 7 — so reusing it would emit `row-value`
mismatches for 2 of 3 real bindings. The live revision arm's `contains_value`
(`tools/mori-record-sweep.py:113-116`) does a presence test with identifier boundaries and is
**correct** for these rows; keep it.

The pre-A1 third row (`Control-receipt binding guard`, `pass=19`, `142998f5`) would have failed
row-value: the only matching table row is `SCORECARD.md:4018`, which states "selftest 19 in-memory
cases" but not `pass=19` (`pass=19` appears only in prose at `SCORECARD.md:4026`, not in a table
row). A1 supersedes that row; no action, recorded so the original table is not reinstated.

`.ufo/waves/round-82/record-pins.json` (mtime 04:45:07, read 04:57) carries `"bindings": []` and
the three A1 `revisions` (same row strings, keys, values and revs). This is consistent with A1.
With the live summary counting both lists
(`tools/mori-record-sweep.py:17` and the `all_bindings`/`emit` path), the real run prints
`bindings=3`, satisfying `count-c3.py:290-293` (`bindings >= 3`). If `bindings` is reverted to
counting only the r81 command list, it becomes 0 and C3 goes unmet — keep the current counting.

## Adversarial review of the live arm (as read 04:53–04:57; uncommitted, another seat's bytes)

Correct as written:

- Resolve-first: `rev-parse --verify --end-of-options <rev>^{commit}`, `rc != 0` →
  `rev-unresolvable` (`tools/mori-record-sweep.py:132-135`). This is the right rc usage: any
  nonzero, never a specific code, never stderr.
- Row-value presence with the first matching row, and "missing row is a mismatch"
  (`:119-130`); `contains_value` boundaries exclude `pointers=2400`, `other-pointers=240`, etc.
- Order is row-value → rev → path → bytes, every binding graded, `continue` on green
  (`:119-151`), matching `contract.md:143-147`.
- `revisions=` counts mismatches and is emitted only when `revisions` is present in the pins
  (`:184-196`), preserving r81 summary compatibility.

Soundness gaps (none triggered by the A1 population or the counter's fixtures, all measured):

1. **`show` as the bytes read is not sound** (`tools/mori-record-sweep.py:137`). For a tree path
   `show` returns rc 0 and a listing; for a gitlink it returns rc 0 and a commit dump. Measured
   false pass: `dir/survivors=0` → `show <rev>:dir` prints `survivors=0` and the arm's own
   `contains_value` matches. Fix: `cat-file -t --end-of-options <sha>:<path>`; nonzero or
   `!= b'blob'` → `path-absent`; else `cat-file blob --end-of-options <sha>:<path>` for bytes.
   Add a selftest arm where the fake reader returns rc 0 with `tree <sha>:x\n\nsurvivors=0\n`
   and require `path-absent` (and one for a gitlink dump).
2. **Text-mode capture** (`:155-159`): `text=True` newline translation and
   `errors='replace'` are not byte-faithful (measured `a\r\nb` → `a\nb`). Capture bytes; search
   `b'%s=%d'`.
3. **No `--no-replace-objects`** (`:132-137`): a `refs/replace/*` in the graded repo swaps the
   object read (measured 240 vs 237). Add the global flag before the subcommand (`git
   --no-replace-objects -C DIR …`). The lane has no replace refs today; the fixture repos created
   by the counter do not either, so this is untriggered defense.
4. **No env scrub** (`:155-163`): a `GIT_DIR`/`GIT_OBJECT_DIRECTORY` inherited from an agent
   shell overrides `-C` (measured rc 128) and would silently mark every binding
   `rev-unresolvable`. Scrub the `GIT_*` discovery variables.
5. **No setup probe**: a missing git binary returns 127 and is reported per binding as
   `rev-unresolvable`; a non-repo `--git` returns 128 as `rev-unresolvable`. Run
   `git -C DIR rev-parse --git-dir` once and map failure to `RECORD_SWEEP_SETUP` exit 2.
6. **`--git` resolution** (`:331`): `Path(args.git).resolve()` resolves a relative value against
   the process cwd, while pins/carriers are root-relative (`:16-17`). Use
   `(root / args.git).resolve()` for relative values.
7. Minor: `commit.strip()` is used without validating that rev-parse's stdout is a single hex
   object name. `--verify` guarantees one line on success, so this is defense-in-depth; accept
   40 or 64 hex (SHA-256 measured) rather than 40 only.

No live failure was observed for the frozen A1 population: all three rows state the token, all
three revs resolve to blobs, and each token occurs once in the named revision's bytes. I did **not**
run the tool's `--selftest` or the C3 counter (out of seat; the executor/L1 owns that verification).

---

## One-line conclusion

`rc` alone is sufficient **only for the sequenced primitive** — `git -C DIR
--no-replace-objects rev-parse --verify --quiet --end-of-options <rev>^{commit}` (any nonzero →
`rev-unresolvable`), then `git -C DIR --no-replace-objects cat-file -t --end-of-options
<resolved-sha>:<path>` (nonzero or type ≠ `blob` → `path-absent`), then `git -C DIR
--no-replace-objects cat-file blob --end-of-options <resolved-sha>:<path>` for bytes — while a
single `git show <rev>:<path>` is **not** sufficient: its rc 128 conflates rev-unresolvable,
path-absent, not-a-repo and option errors, its rc 0 also covers trees and gitlinks (measured
false-pass channel), and its stderr is locale-translated and can report a *path* error for an
unresolvable rev; none of this depends on the repo's default branch as long as the pins' `rev` is
resolved once to a full object id (40 or 64 hex) and that id is used thereafter
(`master~1`/`main~1` are not portable; `HEAD~1` and resolved ids are).

## What I could not verify

- git behaviour on versions other than 2.56.0 (the `cat-file -e` rc vocabulary is
  version-sensitive in the docs; the "any nonzero = failure" rule is the version-robust one).
- A promisor/partial-clone repo (lazy fetch on `cat-file`); the lane has no promisor remote, no
  alternates and is not shallow (verified), so no network path was exercised.
- Non-Linux path semantics (Windows drive letters, case folding), and repo object formats other
  than SHA-1/SHA-256 (both measured).
- Paths containing newlines or invalid UTF-8 (not present in the lane's pins).
- The live tool's `--selftest`, its real-lane run and the C3 counter: not run by this seat.

## Tooling

No installs or upgrades. `git 2.56.0` (system) was used; `localedef` generated a `de_DE.UTF-8`
locale into scratch solely to measure stderr translation. Scratch
`/fast/scratch/hyaku/mori-r82/Mo82L01SourceProbe` was deleted after the probe; no `/tmp` path was
used as evidence.
