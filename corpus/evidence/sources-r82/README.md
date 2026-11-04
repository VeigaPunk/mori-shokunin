# sources-r82 — pinned source bytes (round 82, wave 1)

Public git-project documentation source fetched twice each on 2026-11-04 and byte-identical
across the two fetches, from the git project's own repository at tag `v2.56.0`
(`https://git.kernel.org/pub/scm/git/git.git`; tag object
`2478544319491bbd2a42cc57a83e3d2f4730a280`, peeled commit
`a018953688f1b10bddf91bff8747068f5f4746a4`). Bytes are unmodified upstream AsciiDoc: no
credentials, no host data, no lane state. Hash and size are of the file in this directory.

`gitrevisions(7)` is built from two upstream files: the page shell
`Documentation/gitrevisions.adoc` (NAME, SYNOPSIS, and `include::revisions.adoc[]`) and the
shared body `Documentation/revisions.adoc`. Both are pinned: the graded `<rev>:<path>` sentence
lives in the body, and the shell is what makes that body the `gitrevisions(7)` page and names
`git-show(1)` as a command that takes revision parameters denoting non-commit objects.

| file | url | sha256 | lines | bytes |
|---|---|---|---|---|
| gitrevisions.7.git-2.56.0.adoc | https://git.kernel.org/pub/scm/git/git.git/plain/Documentation/gitrevisions.adoc?h=v2.56.0 | afe4cab8520820d9bf583ec5688beea000d50cce6fdd3c841eb9df94763feadd | 36 | 824 |
| gitrevisions.7.git-2.56.0.body.adoc | https://git.kernel.org/pub/scm/git/git.git/plain/Documentation/revisions.adoc?h=v2.56.0 | b23a9eb17d9b193adccee6b79cb1c1fef450703dae925a33b8a1c6f6639d82ff | 424 | 17266 |

Provenance: each response carried `etag: "<blob id>"` equal to `git hash-object` of the served
bytes — body `3fbfbd3d5fc09190467fc0e359c04a634f6a36a9`, shell
`7146117de5f23fa12cdff7f4dc80c82514ab52a1` — so the pinned bytes are the blobs at v2.56.0, not a
re-render. `last-modified` is the render time (it equals the request time on every fetch) and is
not a page revision; the version is fixed by the `?h=v2.56.0` selector.

Rendered cross-check, not persisted because its base URL is already registry row S227:
`https://git-scm.com/docs/gitrevisions` fetched 2026-11-04, HTTP 200, 74654 bytes, 2751 lines,
sha256 `1ab7124a99e6919e6882be82f77c629ac8fe623bb36af56a749fd4db1919070b` (re-derive with
`curl -sSL https://git-scm.com/docs/gitrevisions | sha256sum`; reproduced on a later fetch the
same day). Its changelog says "last updated in 2.56.0" (`:1294`), it carries the same path-suffix
sentence at `:2440-2442`,
and it renders the `^{<type>}` error clause at `:2390` exactly as the body states it (`:177`).

Located quotes, word counts, duplicate sweep and exit-behaviour receipts are in
`.ufo/waves/round-82/w1/Mo82Sc01Source.md`.
