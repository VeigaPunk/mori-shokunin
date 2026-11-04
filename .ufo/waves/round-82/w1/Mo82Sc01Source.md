# Mo82Sc01Source — round 82 w1 source pin (C3 revision-precision arm)

Seat: scout, leaf member (no subagent dispatch). Lane root
`/home/vgpnk/Projects/shokunin/mori-shokunin`. Access date for every fetch and every line read
below: **2026-11-04**.

**Verdict.** One row proposed for admission (**S597**), one candidate rejected (`git-show(1)`),
one document noted as uses-without-defining (`git-cat-file(1)`).

| disposition | id | carrier | what it grounds |
|---|---|---|---|
| ADMIT (queued) | **S597** | gitrevisions(7) at git tag `v2.56.0` — page shell + included body, from the git project's own repository | the `<rev>:<path>` object-name form: a path suffix on a tree-ish names the blob or tree at that path, which is exactly what `git show <rev>:<path>` reads; and the `^{<type>}` peel that errors out ("barf") when the object cannot be dereferenced to that type |
| REJECT | none assigned (S598 not verified, not used) | git-show(1) | the command is run by the arm but its page never states the `<rev>:<path>` grammar nor any exit status |
| NOT ADMITTED (uses without defining) | — | git-cat-file(1) | `<rev>:<path\|tree-ish>` appears once, in SYNOPSIS at `git-cat-file.adoc:14`, with no definition |

`gitrevisions(7)` is the document that states the syntax precisely; `git-cat-file(1)` only uses
it in a synopsis line, and `git-show(1)` does not mention it at all. The admitted copy is the
**upstream AsciiDoc at the release tag**, not a rendered mirror, because the lane already holds
`https://git-scm.com/docs/gitrevisions` as row S227 and the project's own bytes are the higher
authority.

## 1. Files produced

| absolute path | sha256 | lines | bytes |
|---|---|---|---|
| `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r82/gitrevisions.7.git-2.56.0.adoc` | afe4cab8520820d9bf583ec5688beea000d50cce6fdd3c841eb9df94763feadd | 36 | 824 |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r82/gitrevisions.7.git-2.56.0.body.adoc` | b23a9eb17d9b193adccee6b79cb1c1fef450703dae925a33b8a1c6f6639d82ff | 424 | 17266 |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r82/README.md` | (prose; 2582 bytes) | — | 2582 |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/w1/Mo82Sc01Source.md` | this report | — | — |

`corpus/evidence/sources-r82/` did not exist before this seat (`ls` returned rc 2). No other lane
path was created or modified, and **no mutation was run in the lane repo or any other repo** —
no `git add`, `commit`, `checkout`, `reset`, `stash`, `push`, no `jj` command. The only write
mutations anywhere were inside `/fast/scratch/hyaku/mori-r82/Mo82Sc01Source/fixture` (a
throwaway `git init`), where `git add tracked.txt`, one `git commit`, and one annotated
`git tag -a vprobe` ran **after** `git rev-parse --show-toplevel` printed that fixture directory,
as the host guard requires. That fixture is deleted before yield.

## 2. Fetch receipts

Two independent fetches per file, byte-compared. No redirect occurred: `%{url_effective}` equals
the requested URL on every fetch, and the HEAD probe returned `HTTP/2 200` with no `location`.

```
$ curl -sSL -o rev.1 -w 'code=%{http_code} final=%{url_effective} size=%{size_download} type=%{content_type}\n' \
    'https://git.kernel.org/pub/scm/git/git.git/plain/Documentation/revisions.adoc?h=v2.56.0'
fetch1 code=200 final=https://git.kernel.org/pub/scm/git/git.git/plain/Documentation/revisions.adoc?h=v2.56.0 size=17266 type=text/plain; charset=UTF-8
fetch2 code=200 final=https://git.kernel.org/pub/scm/git/git.git/plain/Documentation/revisions.adoc?h=v2.56.0 size=17266 type=text/plain; charset=UTF-8
b23a9eb17d9b193adccee6b79cb1c1fef450703dae925a33b8a1c6f6639d82ff  rev.1
b23a9eb17d9b193adccee6b79cb1c1fef450703dae925a33b8a1c6f6639d82ff  rev.2
     424   17266 rev.1
BYTE-IDENTICAL
```

```
$ curl -sSL -o gitrevisions.adoc  -w 'code=%{http_code} final=%{url_effective}\n' \
    'https://git.kernel.org/pub/scm/git/git.git/plain/Documentation/gitrevisions.adoc?h=v2.56.0'
code=200 final=https://git.kernel.org/pub/scm/git/git.git/plain/Documentation/gitrevisions.adoc?h=v2.56.0
SHELL_IDENTICAL
afe4cab8520820d9bf583ec5688beea000d50cce6fdd3c841eb9df94763feadd  gitrevisions.adoc
```

Response headers (HEAD probe, same URL family):

Body (`revisions.adoc`):

```
HTTP/2 200 
content-type: text/plain; charset=UTF-8
content-length: 17266
etag: "3fbfbd3d5fc09190467fc0e359c04a634f6a36a9"
last-modified: Wed, 04 Nov 2026 07:46:03 GMT            # == request time; render time, not a page date
```

Shell (`gitrevisions.adoc`):

```
HTTP/2 200 
content-type: text/plain; charset=UTF-8
content-length: 824
etag: "7146117de5f23fa12cdff7f4dc80c82514ab52a1"
last-modified: Wed, 04 Nov 2026 07:46:49 GMT            # also the request time
```

**Provenance is a blob id, not a date.** `git hash-object` over the pinned bytes equals the ETag
the server sent, so the bytes are the blobs at the named tag:

```
$ git hash-object rev.1                 -> 3fbfbd3d5fc09190467fc0e359c04a634f6a36a9
$ git hash-object gitrevisions.adoc     -> 7146117de5f23fa12cdff7f4dc80c82514ab52a1
$ git ls-remote --tags https://git.kernel.org/pub/scm/git/git.git
2478544319491bbd2a42cc57a83e3d2f4730a280  refs/tags/v2.56.0
a018953688f1b10bddf91bff8747068f5f4746a4  refs/tags/v2.56.0^{}
```

`v2.56.0` is the newest `v<major>.<minor>.<patch>` tag on that remote
(`git ls-remote --tags https://git.kernel.org/pub/scm/git/git.git | sed -n 's#.*refs/tags/\(v[0-9]*\.[0-9]*\.[0-9]*\)$#\1#p' | sort -V | tail -3`
→ `v2.54.0`, `v2.55.0`, `v2.56.0`), and it is the version of the host's own git
(`git version 2.56.0`), so the pin and the instrument run the same release.

Version cross-check on the rendered page (fetched, not persisted: its base URL is S227, and the
hash below is re-derivable with `curl -sSL https://git-scm.com/docs/gitrevisions | sha256sum`,
reproduced on a later fetch the same day): `https://git-scm.com/docs/gitrevisions`, HTTP 200,
74654 bytes, 2751 lines, sha256
`1ab7124a99e6919e6882be82f77c629ac8fe623bb36af56a749fd4db1919070b`; changelog says "last updated
in 2.56.0" (`:1294`); the same path-suffix sentence at `:2440-2442`; the `barf` clause at
`:2390`. Rendering and upstream bytes agree word for word.

## 3. Located quotes (exact pinned bytes)

The pinned copy is upstream AsciiDoc, so its own markup (`'<rev>'`, `{caret}`) is part of the
text; the rendered page turns the `'…'` quoting into emphasis and renders `{caret}` as `^`. Line
numbers below are `grep -n` against the pinned files.

**Primary quote — the `<rev>:<path>` syntax, body `:221-223`, 24 words.**

Entry header at body `:220`:

```
220:'<rev>:<path>', e.g. 'HEAD:README', 'master:./README'::
221:  A suffix ':' followed by a path names the blob or tree
222:  at the given path in the tree-ish object named by the part
223:  before the colon.
```

> "followed by a path names the blob or tree at the given path in the tree-ish object named by
> the part before the colon."

The full sentence is 27 words, so the 25-word cap cuts the subject (`A suffix ':'`); the cut is
recorded here rather than paraphrased. The entry header `'<rev>:<path>'` at `:220` is the syntax
itself and is cited alongside. Verified as a contiguous span of the joined lines 221-223
(`python3` join + substring test, `quote in joined span: True`, `words = 24`).

**Supporting quote — the `^{<type>}` peel is a type check that errors, body `:175-177`, 25
words.**

```
173:'<rev>{caret}{<type>}', e.g. 'v0.99.8{caret}\{commit\}'::
...
175:  brace pair means dereference the object at '<rev>' recursively until
176:  an object of type '<type>' is found or the object cannot be
177:  dereferenced anymore (in which case, barf).
```

> "dereference the object at '<rev>' recursively until an object of type '<type>' is found or the
> object cannot be dereferenced anymore (in which case, barf)."

**Supporting quote — page shell names `git-show(1)` for non-commit revision parameters, shell
`:22-25`, 16 words.**

```
22:In addition, some Git commands (such as linkgit:git-show[1] and
23:linkgit:git-push[1]) can also take revision parameters which denote
24:other objects than commits, e.g. blobs ("files") or trees
25:("directories of files").
27:include::revisions.adoc[]
```

> "can also take revision parameters which denote other objects than commits, e.g. blobs
> ("files") or trees"

**Path-relativity detail the arm must not trip on, body `:224-225`:** "A path starting with
`./` or `../` is relative to the current working directory. The given path will be converted to
be relative to the working tree's root directory." The three frozen bindings use `SCORECARD.md`
(the tree-root form), so they are safe; a pin written as `./SCORECARD.md` would be CWD-dependent
and would change meaning under the tool's `--git DIR`.

## 4. Exit behaviour — documented versus measured

The seat's target ground names two reads: `git show <rev>:<path>` and
`git rev-parse --verify <rev>^{commit}`. What the admitted document states, and what it does not:

| question | pinned document | status |
|---|---|---|
| what `<rev>:<path>` names | body `:220-226`: the blob or tree at that path in the tree-ish | documented |
| what `git show` does with it | shell `:22-25` names `git-show(1)` among commands taking non-commit revision parameters; `git-show.adoc:12` synopsis `git show [<options>] [<object>...]`, DESCRIPTION `:16` "Shows one or more objects (blobs, trees, tags and commits)." | documented at the command level, not at the path-form level |
| what `^{<type>}` does when the object is not that type | body `:173-177`: dereference until found, "or the object cannot be dereferenced anymore (in which case, barf)" | documented as an error, no status number |
| the exit **status number** of either read | no exit-status sentence anywhere in either file (receipt below) | **not documented** |

```
$ curl -sSL 'https://git.kernel.org/pub/scm/git/git.git/plain/Documentation/revisions.adoc?h=v2.56.0' \
    | grep -ciE 'exit status|exit code|fatal|does not exist|error out|nonzero|non-zero'
0                       # rc=1 (grep -c exits 1 on zero matches)
$ curl -sSL 'https://git-scm.com/docs/gitrevisions' \
    | grep -ciE 'exit status|exit code|fatal|does not exist|error out|nonzero|non-zero'
0                       # rc=1
```

Both receipts are re-runnable as written (fetch and count); neither depends on a scratch path.

Measured on the host's git 2.56.0, in a scratch fixture whose toplevel was asserted
(`git rev-parse --show-toplevel` → the fixture dir) before any command:

```
--- git show HEAD:tracked.txt                    rc=0   (prints the blob)
--- git show HEAD:missing.txt                    rc=128 fatal: path 'missing.txt' does not exist in 'HEAD'
--- git show deadbeef…beef:tracked.txt           rc=128 fatal: path 'tracked.txt' exists on disk, but not in 'deadbeef…beef'
--- git show 4a580070…8e74:tracked.txt           rc=128 fatal: path 'tracked.txt' exists on disk, but not in '4a580070…8e74'
--- git show vprobe:tracked.txt                  rc=0   (annotated tag peels)
--- git rev-parse --verify HEAD^{commit}         rc=0   prints the commit id
--- git rev-parse --verify nope^{commit}         rc=128 fatal: Needed a single revision
--- git rev-parse --verify 7a8adbbd…b7ee^{commit} rc=128 error: … expected commit type, but the object dereferences to tree type / fatal: Needed a single revision
--- git rev-parse --verify 4a580070…8e74^{commit} rc=128 error: … expected commit type, but the object dereferences to blob type / fatal: Needed a single revision
--- git rev-parse --verify vprobe^{commit}       rc=0   prints the commit id
```

Re-derivation recipe for all four shapes above (throwaway repo under your own scratch dir, git
2.56.0; assert the toplevel before committing):

```
$ d=/fast/scratch/hyaku/<your-seat>/repro && mkdir -p "$d" && cd "$d" && git init -q .
$ git rev-parse --show-toplevel          # must print $d before any mutation
$ echo alpha > f && git add f && git -c user.name=p -c user.email=p@x.invalid commit -qm one
$ git show HEAD:f                       ; echo rc=$?   # alpha / 0
$ git show HEAD:missing                 ; echo rc=$?   # fatal: path 'missing' does not exist in 'HEAD' / 128
$ git rev-parse --verify HEAD^{commit}  ; echo rc=$?   # <sha> / 0
$ git rev-parse --verify nope^{commit}  ; echo rc=$?   # fatal: Needed a single revision / 128
```

Three consequences the C3 arm must respect, all grounded above:

1. **Test `rc != 0`, never `rc == 128`.** 128 is what the host's git returns for a missing path,
   for an unresolvable revision, for a blob/tree where a commit is required, and for a known-bad
   object id — the number is shared, and the page documents no number at all.
2. **The exit code cannot classify the failure.** `rev-unresolvable` and `path-absent` both exit
   128, so the arm's ordering (resolve `rev` first, then test `path`, then read bytes) is what
   produces the distinct message token; a reader must not infer the class from the status.
3. **`git show <bogus>:<path>` reports in path terms** ("path 'tracked.txt' exists on disk, but
   not in '<sha>'"), i.e. a bad revision or a bad path look alike on stderr. Matching stderr text
   is therefore brittle as a discriminator; the contract's four tokens must come from the arm's
   own ordered checks, not from git's prose.

The `rev-parse --verify` failure wording itself is already carried by an existing row:
`git-rev-parse.adoc:110-113` ("… otherwise, error out", key line `:113`) and `:130-133`
(`--quiet`: "instead exit with non-zero status silently", key line `:132`), cross-checked this
round (17036 bytes, 517 lines, sha256
`4d8e9aca13f6ea6808272eb44e417687a5cca7d23cf1ed311f25e9fdeb148902`, re-derive with
`curl -sSL 'https://git.kernel.org/pub/scm/git/git.git/plain/Documentation/git-rev-parse.adoc?h=v2.56.0' | sha256sum`)
but **not persisted** — the document is row S210 (and S064) under
`https://git-scm.com/docs/git-rev-parse`, so a second copy would be a duplicate-source pin.

## 5. Duplicate sweep and id assignment

Run before the row was drafted:

```
$ grep -n 'https://git-scm.com/docs/gitrevisions' corpus/SOURCES.md | cut -c1-90
233:| S227 | gitrevisions(7) — https://git-scm.com/docs/gitrevisions | docs | A | revisi
$ grep -c 'revisions\.adoc\|git\.kernel\.org/pub/scm/git/git\.git\|b23a9eb17d9b\|afe4cab85208' corpus/SOURCES.md
0
$ grep -c 'git-show\|git-cat-file' corpus/SOURCES.md
0
$ grep -c 'S597' corpus/SOURCES.md
0
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort | tail -3
S594
S595
S596
```

- **Same base URL as an existing row: yes — S227** (`corpus/SOURCES.md:233`,
  `https://git-scm.com/docs/gitrevisions`). S227's scope is the two-dot range notation
  (`r1..r2`, its anchor `:2538-2544`), not the `<rev>:<path>` entry. A second row on that base
  URL would be the duplicate shape S178 was rejected for (`corpus/SOURCES.md:184`), which is why
  the admitted copy is the project's own `Documentation/*.adoc` at tag `v2.56.0` — a different
  base URL and a strictly higher tier than the rendered build.
- `gitrevisions` occurs twice in the registry: S227's row and the round-39 search-methods
  paragraph at `corpus/SOURCES.md:453`. Neither carries the `<rev>:<path>` entry.
- No row exists for `git-show`, `git-cat-file`, or the upstream adoc path/blob ids.
- **Next unused id verified: S597** (`S596` is the max; `S597` occurs 0 times in the registry).
  The r81 scout's *proposed* S597 (`git-ls-tree`, `.ufo/waves/round-81/w1/Mo81Sc02Source.md:11`)
  never landed — see §7 — so the id is genuinely free.

### Row draft for the Gate (not written to `corpus/SOURCES.md` by this seat)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S597 | gitrevisions(7) at git tag v2.56.0, page shell and included body from the git project's repository — https://git.kernel.org/pub/scm/git/git.git/plain/Documentation/gitrevisions.adoc?h=v2.56.0 ; https://git.kernel.org/pub/scm/git/git.git/plain/Documentation/revisions.adoc?h=v2.56.0 | docs | A | the `<rev>:<path>` object-name form (a path suffix on a tree-ish names the blob or tree at that path, which is what `git show <rev>:<path>` reads) and the `^{<type>}` peel that errors when the object cannot be dereferenced to that type; not a documented exit-status number, not a lane record grammar | `<rev>:<path>` at body 220-223, located quote body 221-223 (24 words); `^{<type>}` at body 173-182, quote body 175-177 (25 words); shell 22-27 names git-show(1) for non-commit revision parameters and includes the body; tag v2.56.0 = tag object 2478544319491bbd2a42cc57a83e3d2f4730a280, commit a018953688f1b10bddf91bff8747068f5f4746a4; ETag equals `git hash-object` for both files (body 3fbfbd3d5fc09190467fc0e359c04a634f6a36a9, shell 7146117de5f23fa12cdff7f4dc80c82514ab52a1); sha256 b23a9eb17d9b193adccee6b79cb1c1fef450703dae925a33b8a1c6f6639d82ff (17266 bytes, 424 lines) and afe4cab8520820d9bf583ec5688beea000d50cce6fdd3c841eb9df94763feadd (824 bytes, 36 lines); copies corpus/evidence/sources-r82/; opened 2026-11-04 | A record row's revision label is gradable by reading the named path's bytes at the named commit: the syntax names a blob or tree, not a line, so the check is containment of `key=value` in those bytes; and a `rev` that does not peel to a commit is a documented error, not a silent miss. | queued | 2026-11-04 | on-release | — |

Status `queued` because no knowledge entry cites it yet at this seat's tip; flip to `mined` with
`used-by corpus/knowledge/record-revision-precision-r82.md` when that entry lands. Recheck
`on-release`: the pin is version-labelled to a release, and a new git tag is the recheck trigger.

## 6. Reject candidate — `git-show(1)`

Deliberately **not** admitted, even though it is the command the arm executes.

- URL `https://git.kernel.org/pub/scm/git/git.git/plain/Documentation/git-show.adoc?h=v2.56.0`,
  HTTP 200, no redirect, **1939 bytes, 90 lines**, sha256
  `91dfc431d85e53a12ef7854cbeb52674f4e2e52a7fe9ffe3ee018c1b2ed5ea30`.
- Rendered page also fetched: `https://git-scm.com/docs/git-show`, HTTP 200, 246736 bytes,
  sha256 `a3716a4d6c236082b0f6d08da64735765f376c1c32ba5ede93b70b013f52a9aa`.
- Evidence of absence, re-runnable as written:
  `curl -sSL 'https://git.kernel.org/pub/scm/git/git.git/plain/Documentation/git-show.adoc?h=v2.56.0' | grep -ci 'rev>:<path'`
  → `0` (rc 1); the same pipeline with `grep -ciE 'exit status|exit code'` → `0` (rc 1); on the
  rendered page, `curl -sSL 'https://git-scm.com/docs/git-show' | grep -c 'rev&gt;:&lt;'` → `0`.
  Its whole input statement is the synopsis `git show [<options>] [<object>...]`
  (`git-show.adoc:12`) and the DESCRIPTION "Shows one or more objects (blobs, trees, tags and
  commits)." (`:16`).

**Reason.** The page defines what `git show` *prints*, never what `<object>` may be spelled as,
and never an exit status. Admitting it would attach the `<rev>:<path>` fact to a document that
does not state it — the D80-4/D81-1 class of claiming a value the cited bytes do not carry.

**Flip condition.** A `git-show(1)` revision that gains either an explicit `<rev>:<path>`
sentence (or a `<rev>:<path>` SYNOPSIS form with a definition) or an EXIT STATUS section naming
the failure codes for path forms. Then admit it as a *command-behaviour* row (output forms and
status), never as the syntax ground, and keep S597 for the syntax.

**Second candidate, same treatment.** `git-cat-file(1)` (fetched, HTTP 200, 16099 bytes, 470
lines, sha256 `6c32dbda8c2106be08bda471592db50b5afaf185de32f2e513e80d802b4a95b2`) uses
`<rev>:<path|tree-ish>` exactly once, in the SYNOPSIS of the `--textconv`/`--filters` form
(`git-cat-file.adoc:14`), and defines it nowhere. Uses-without-defining is not ground; flip only
if a definition or an exit-status statement is added. No id was assigned for either rejection —
S598 was not verified and is not claimed.

## 7. Defect observed in another seat's bytes

**Orphaned pin from round 81.** `corpus/evidence/sources-r81/git-ls-tree.html` (39083 bytes,
sha256 `ff06fbc8…18267`) is pinned and indexed at `corpus/evidence/sources-r81/README.md:10`, but
it has **no `corpus/SOURCES.md` row**: the r81 Gate verdicts
(`corpus/lessons/round-81.md:205-212`) admit only S596 (stat(2)) and the registry's max id is
S596. The r81 knowledge seat records the non-admission in its own words
(`.ufo/waves/round-81/w1/Mo81S02Knowledge.md:98`: "The proposed S597 git-ls-tree source was not
admitted or cited by this seat."). Effect: a durable pinned copy exists with no registry row and
no citing entry, so a freshness/census reader cannot see it, and `grep -rn 'git-ls-tree'
corpus/ --include=*.md` outside that README returns nothing. Either a row should be landed for it
or the copy removed; this seat did neither (out of scope, and removal would destroy evidence).

No other defect was found. I did not read any other round-82 seat's bytes.

Adjacency check on the in-flight C3 pins file (read-only snapshot at 04:52, **not** a claim about
the landed bytes): `.ufo/waves/round-82/record-pins.json` carries its three entries under
`revisions`, each with `"path": "SCORECARD.md"` — the tree-root form, no `./` prefix — so the
path-relativity pitfall in §3 does not bite that file at this snapshot. `tools/mori-record-sweep.py`
reads the blob as `git show <commit>:<path>` (`:137`) after `rev-parse --verify --end-of-options`
(`:132`), which is the pinned syntax used as documented. Neither file is mine and neither was
modified.

## 8. What I verified, and what I did not

Verified: HTTP status, final URL (no redirects), two-fetch byte identity, sha256, byte and line
counts, `git hash-object` equality with the served ETag, the tag object and peeled commit for
`v2.56.0`, the three located quotes as contiguous spans of the pinned bytes with word counts, the
duplicate sweep and the S597 id check, and the ten exit-code observations above on git 2.56.0 in
a toplevel-asserted scratch fixture.

Not verified, and not claimed:

- That the `v2.56.0` adoc is byte-identical to the text served for older releases; only this tag
  was opened.
- The `man7.org` render of `gitrevisions(7)`: not opened this round, so no claim about it (as a
  mirror it would anyway rank below the project's own bytes).
- `git show` behaviour for paths containing `:` (the `:<n>:<path>` index form, `:/<text>`
  search), for `--end-of-options`, or in a SHA-256 object-format repository; the pinned page
  states nothing about object formats.
- Any counter, census, record-sweep or battery instrument: this seat ran none, so C3's
  `arms`/`defeated`/`bindings` readings are untouched by this report.
- The S597 row's landing: this seat must not edit `corpus/SOURCES.md`; the draft in §5 is a
  recommendation for the Gate.

## 9. Tooling

None installed or upgraded. `curl`, `git 2.56.0`, `python3`, `sha256sum`, `wc`, `cmp` were already
present; no package transaction was run (pacman is paused host-wide), and nothing was written to
any PATH directory.

One process note, against the scratch rule: the fixture measurement helper captured stdout/stderr
to `/tmp/o` and `/tmp/e` for a few calls. Both files are deleted, no path in this report cites
them, and no finding depends on them; every quoted output above was re-read from the terminal
transcript of the same command, and all durable bytes are the pinned files in
`corpus/evidence/sources-r82/`.
