# SrcGitCommit — S064 re-open for round22 C1 (git-rev-parse)

Seat: MoriR22.SrcGitCommit (scout, read-only). Report-only; no registry, lesson or production edits.

## Opened

| Item | Value |
|---|---|
| URL | https://git-scm.com/docs/git-rev-parse |
| Access date | 2026-10-21 (fetched 2026-10-21T13:52:58Z, `curl -sSL`, HTTP body 122331 bytes) |
| Page version | "git-rev-parse last updated in 2.56.0", changes entry 2.56.0 2026-09-28 (unchanged from S064 anchor) |
| Fetched body SHA-256 | `2edcf32444aefd1305e09191266772acbc4e0c2a6a03e4e2ff47449666d736f0` (local copy `.scratch/SrcGitCommit-git-rev-parse.html`; a hash of the page snapshot, not authentication of content) |
| Existing row | `corpus/SOURCES.md:70` S064, docs, tier A, status mined, used-by `corpus/lessons/round-19.md` |
| Existing Gate use | `corpus/lessons/round-19.md:42` (EXAMPLES quote); `corpus/knowledge/freeze-order-r18.md:51` |

## Located quote (≤25 words)

Proposed for the round22 lesson Gate (15 words), section **OPTIONS → `--verify`**:

> “git rev-parse "$VAR^{commit}" will make sure $VAR names an existing object that is a commit-ish”

Alternate, already used in round-19 (EXAMPLES, after "Print the commit object name from the revision in the $REV shell variable"):

> “This will error out if $REV is empty or not a valid revision.”

Both strings were located verbatim in the fetched page text. I recommend the OPTIONS quote because it addresses commit typing directly, which is the property round22 needs for `--rev` and `measured_revision`.

## Narrow grounding assessment

Observed in the source:
- `--verify` takes exactly one parameter and either emits the object name or errors out. `^{commit}` peels to a commit-ish. `--end-of-options` is recommended for names from an untrusted source. `-q` makes failure silent with a non-zero status.
- `--short` is described as the abbreviated variant of `--verify`, so plain `--verify` prints the full object name.
- `--show-object-format` reports the repository's hash algorithm.

Grounded by S064 (round22 contract requirement IDs):
- Resolving `--rev` once to a commit object: `git -C DIR rev-parse --verify --quiet --end-of-options REV^{commit}`.
- R13: an unresolvable `measured_revision`, or one that is not a commit, returns exit 2.
- Safe argument separation for receipt-supplied revision strings (`--end-of-options`).

Partially grounded (requires [INFERENCE]):
- "Receipt `measured_revision` must be a full commit": S064 supports resolving the string to a full object id. Rejecting abbreviations, refnames and tag names comes from a tool-side equality check (input string == resolved full id). That rule is a design consequence, not documented rev-parse behaviour.
- Hash width: the `--verify` text still says "raw 20-byte SHA-1". This repo reports `sha1` (`git rev-parse --show-object-format`; local git 2.56.0). A full-id check should derive its expected length from the object format instead of hard-coding 40 hex digits [INFERENCE]. This is a scope caveat, not a reason to reject the row.

Not grounded by S064 (out of scope; no source opened for these):
- R14 ancestry (`measured_revision` is an ancestor of `--rev`). That is `git merge-base --is-ancestor` semantics, and the rev-parse page only defines ancestry notation (`~<n>`, `^r1 r2`). This remains an unresolved source gap. No broad search was run, per the assignment.
- Reading receipt, policy and allowlist bytes from Git blobs, byte equality across revisions (R15/R16), committed symlink rejection (R21, tree mode), NUL skipping (R22), and the retention recomputation itself.
- Any privacy, secrecy or authenticity property. A resolved commit id does not show that private data is absent, and it does not show that loaded bytes match that tree. This is consistent with the existing S064 scope exclusions and with contract `privacy_clearance=false`.

Disposition: S064 remains narrowly adequate (tier A) for C1's revision-resolution and commit-typing step only. Its existing scope cell already excludes publication, authenticity and input-tree equality, and nothing on the 2026-10-21 page contradicts the row.

## Proposed used-by addition (round22 lesson only)

Append to the S064 `used-by` cell, keeping the existing value:

`corpus/lessons/round-19.md, corpus/lessons/round-22.md`

Conditions: add this only after `corpus/lessons/round-22.md` exists (it is absent at lane HEAD `306e06ecd02e0ea8e544fbd30d1ff7e7359c581e`), and only if its Gate carries the located quote above with access date 2026-10-21. Do not change any other S064 field (scope, anchor, teaches, status, opened, recheck). L1 owns the edit.

Proposed Gate row for the round22 lesson:

| Row | URL | Access date | Decision / located quote (at most 25 words) |
|---|---|---|---|
| S064 | https://git-scm.com/docs/git-rev-parse | 2026-10-21 | Re-opened A, C1 revision resolution only. “git rev-parse "$VAR^{commit}" will make sure $VAR names an existing object that is a commit-ish” — OPTIONS `--verify`. Does not ground ancestry, blob-byte equality or privacy clearance. |

## Remaining unknowns

- R14 ancestry has no admitted source. A candidate would be git-merge-base(1) `--is-ancestor`, which was not opened this round.
- Whether L1 prefers reusing the round-19 EXAMPLES quote over the new OPTIONS quote.

## Run log

- Commands: one `curl` GET of the URL into `.scratch/`; local Python HTML-to-text extraction; `sha256sum`; read-only `git -C … rev-parse HEAD` and `--show-object-format`; `git --version`; `rg`/`sed` reads of `corpus/`.
- Tools installed or updated: none.
- Measurements, tests and builds: none run.
