# Six source-cell edits — adversarial review

Review target: `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8`, compared with `7d382043`.
Axes: source-attribution fidelity; complete clause coverage; minimality and audit accuracy.
Advisory findings only: no adjudication, integration, product edits, or runtime invocation.
Paths below are relative to the lane unless absolute. `S###.src` means `corpus/evidence/recheck-r32/S###.src`.
Frozen requirements: `.ufo/waves/round-33/contract.md:85-88,96-97`; repair account: `corpus/lessons/round-33.md:77-96`.

## 1. Word-level diff and old-to-new account

Executed the requested diff, bounded by `timeout 60s prlimit --as=1073741824 --`:

```sh
git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff 7d382043 62db24c01d5b7c2247f43852ea2b28d0ae5e40c8 -- corpus/SOURCES.md
```

Also executed the same command with `--word-diff=plain --unified=0`. Relevant output:

```text
S041: ... time window; {+lane rule:+} it does not identify ...
S044: ... HEAD state; {+lane rule:+} a commit-id read ...
S051: ... under schedules. {+lane rule:+} A class-hit gate ...
S062: ... duplicate names; {+lane rule:+} -0 ... errata; {+lane rule:+} a Python ...
S064 scope: ... commit object; {+lane rule:+} not remote publication ...
S064 teaches: ... full object [-id,-]{+id; lane rule:+} then separately bind ...
S069: ... see symlinks: {+lane rule:+} reject absolute ...
```

The five rows other than S064 have insertion-only changes. S064 additionally changes the comma after `id` to a semicolon. All six changes match the old-to-new list at `corpus/lessons/round-33.md:82-92`, including its explicit S064 punctuation change at `:89-90`. No lexical content beyond the labels changes in these six rows; the stronger claim “only inserted labels” has that punctuation exception. The diff also adds S180–S190, outside this assignment.

**Severity: minor, audit precision only.** Attack: any labels-only description of `corpus/SOURCES.md:70`; not a semantic objection to the semicolon. Smallest correction: describe “labels plus S064's comma-to-semicolon boundary,” rather than insertion-only bytes. The lesson's narrower “no other word changed” at `round-33.md:79` need not mean punctuation was unchanged.

## 2. Major — S064 still leaves two lane instructions undeclared

Attack: `corpus/SOURCES.md:70`, teaches cell; completion claim at `corpus/lessons/round-33.md:79-80,89-91`.

The unlabelled prefix still says **“Resolve a selector once ... retain the full object id”**. The source states the flags, peeling, and printed name, not resolve-once or retention policy:

- `S064.src:2720-2723`: “Verify that exactly one parameter is provided” and “If so, emit it to the standard output; otherwise, error out.” One parameter is not one resolution for the lane's entire procedure.
- `S064.src:2725-2732`: add the `^{type}` peeling operator; the commit example “names an existing object that is a commit-ish”.
- `S064.src:2735-2737`: for an untrusted name, “wise to use” `--end-of-options` so the name is not mistaken for an option.
- `S064.src:3061-3065`: “The full SHA-1 object name (40-byte hexadecimal string)” describes an object name, not a requirement to retain it.
- `S064.src:3763-3766`: “Print the commit object name from the revision in the $REV shell variable”, followed by `git rev-parse --verify --end-of-options $REV^{commit}`.

A full-copy search for `exactly one|\bonce\b|\bretain\b|retention` found the parameter statement (`:2720`), an unrelated remote configuration statement (`:3218`), and an unrelated dereferencing statement (`:3283`); no retention instruction. A separate search for `register|correction|publication|authenticity|loaded` found no matching source statement.

The wave-1 draft explicitly identified **both** `once` and retaining the id as lane procedure (`.ufo/waves/round-33/w1/ScopeS064.md:24,28-31,50-52`). Thus the L1's later label preserves the documented flags but also accidentally preserves these unsupported instructions outside the declaration. This is not an unavoidable tradeoff.

Impacted axes: clause coverage and source attribution. Smallest safe correction: separate the supported API description from the policy, e.g. “`--verify --end-of-options` with commit peeling prints the commit object name; lane rule: resolve the selector once, retain the full id, then separately bind ...”. Keep the existing scope exclusions and blob-binding/hash-printer limits declared as lane rules.

## 3. Major — S062's unlabelled “no whitespace” loses a source restriction

Attack: `corpus/SOURCES.md:68`, teaches cell.

The page does not state an unrestricted prohibition on whitespace:

- `S062.src:379`: **“Whitespace between JSON tokens MUST NOT be emitted.”**
- `S062.src:347`: **“parsed JSON string data MUST NOT be altered during subsequent serializations.”**
- `S062.src:456-460`: Unicode outside the ASCII control range must be serialized “as is”, except backslash and quotation mark.
- The page's own JCS test data contains `“Euro Sign”` and `“Carriage Return”` (`S062.src:603-608`), with the spaced strings preserved in its expected ordering (`:618-626`).

[INFERENCE] Those source rules require preserving the space in a string such as `{"x":" "}`. Reading the cell's “no whitespace” literally forbids that; accepting it as “no whitespace *between tokens*” needs the omitted qualification. No serializer was executed: this counterexample is derived from the quoted source rules and the page's own spaced-string data.

Impacted axes: source fidelity and clause precision under R-R's no-caveat wording (`contract.md:85-88`). Smallest correction: `no whitespace between JSON tokens`. Also make the subject explicitly `JCS canonicalization`, rather than suggesting that every canonical form for hashing requires JCS's choices; the page describes JCS as one way to obtain a canonical representation (`S062.src:138-149`).

## 4. Major — S062's erratum provenance is not turned into doctrine by a label

Attack: `corpus/SOURCES.md:68`, `lane rule: -0 is a parser SHOULD-error per the verified errata`.

The committed RFC copy does not state this parser recommendation or the claimed verified status. Its located errata material is a link, **“RFC 8785 Errata”** (`S062.src:1691-1692`), not the erratum text. The copy separately gives a “Minus zero” serialization sample with output `0` (`:920-928`); that is not a parser SHOULD-error statement and does not refute an external erratum either.

The row's source cell names only the RFC URL; its anchor mentions an errata record and verification date without naming that page's URL (`corpus/SOURCES.md:68`). Wave 1 already acknowledged the erratum text is absent from this copy (`.ufo/waves/round-33/w1/ScopeS062.md:25`). A label can declare a lane's chosen rejection policy, but **“per the verified errata” remains a factual provenance assertion**, not a policy choice.

Impacted axes: provenance and source-attribution fidelity. Smallest safe correction: either state the parser rejection solely as the lane's own choice, without the ungrounded external attribution, or name and commit the exact erratum page and locate a quote supporting the complete recommendation and status. This review did not fetch or judge that external erratum; its truth is not established here.

## 5. Complete six-row clause ledger

### S041 — no additional placement defect found (severity: none)

Attack surface: `corpus/SOURCES.md:47`; list agrees at `round-33.md:82`.

Unlabelled scope/status clause is stated: `S041.src:243` names “429 Too Many Requests”; `:245-246` says **“The 429 status code indicates that the user has sent too many requests in a given amount of time”**.

Both labelled parts—no vendor-business-error identification and no permanent-seat-death proof—are not stated. Full-copy search `vendor|business error|permanent|seat|death` returned no matches. The nearby source limitation concerns how users are identified and requests counted (`S041.src:269-274`), not those lane conclusions. The label covers both. No correction beyond retaining this boundary.

### S044 — no additional placement defect found (severity: none)

Attack surface: `corpus/SOURCES.md:50`; list agrees at `round-33.md:83`.

Unlabelled scope: **“A colocated Jujutsu workspace is a hybrid Jujutsu/Git workspace”**, sharing a working copy (`S044.src:2223-2227`). Unlabelled teaches clause: **“jj commands will usually put the Git repo in a \"detached HEAD\" state”** (`:2234-2235`).

Labelled commit-id/branch-identity proof limitation is not stated. Full-copy search `commit.id read|branch.identity|proof|proves|commit id|commit hash` returned no matches; the adjacent source says there is no “currently tracked branch” concept (`:2235-2236`), which is not itself the proof claim. No correction beyond retaining this boundary.

### S051 — no additional placement defect found (severity: none)

Attack surface: `corpus/SOURCES.md:57`; list agrees at `round-33.md:84`.

The committed copy is a binary PDF, so I extracted it with:

```sh
timeout 60s prlimit --as=1073741824 -- pdftotext -layout /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/recheck-r32/S051.src /fast/scratch/hyaku/mori-r33/AttackScopeEdits/S051.txt
```

Exit 0. Located extraction output below is `S051.txt` under that scratch directory, from the committed PDF (printed ES-2, 1-1, 4-3, and appendix D):

- Minimum-necessary scope: **“Organizations should minimize the use, collection, and retention of PII to what is strictly necessary to accomplish their business purpose and mission.”** (`S051.txt:249-250`).
- Federal/voluntary scope: **“prepared for use by Federal agencies”** and **“may be used by nongovernmental organizations on a voluntary basis”** (`:412-414`).
- Retention-purpose test: **“Only retaining PII for as long as is necessary to fulfill the specified purpose(s)”** (`:2582-2585`); no-current-purpose clause: **“If the PII serves no current business purpose, then the PII should no longer be used or collected.”** (`:1250-1251`).
- Periodic review: **“an organization should regularly review ... its holdings of previously collected PII”** to determine relevance and necessity (`:1253-1255`).
- Disposal under schedules: **“must be conducted in accordance with any litigation holds and the Federal Records Act and records control schedules”** approved by NARA (`:1256-1258`). The cell does not say schedules are the only constraint.

The labelled class-hit-gate assertion is not stated: full extracted-text search `class.hit|\bgate\b|necessity` returned no matches. The quoted purpose/review rules do not assert that lane gate's evidentiary meaning. No correction beyond retaining this boundary.

### S062 — two placement boundaries present; residual defects above

Attack surface: `corpus/SOURCES.md:68`; list agrees at `round-33.md:85-87`.

Unlabelled scope clauses have located support: JCS/hashable canonical representation (`S062.src:134-149,203-205`); string escapes (`:447-460`); UTF-16 property-name code-unit sorting (**“arrays of UTF-16 ... code units”**, `:551-556`); ECMAScript number serialization (**“MUST be serialized according to Section 7.1.12.1”** of ECMA-262, `:481-483`); UTF-8 output (**“MUST be encoded in UTF-8”**, `:647-649`). The JCS specification uses normative requirements, while explicitly saying informational/not Standards Track (`:144-149,157-165`); date and Independent Stream metadata are at `:1681,1685`.

Unlabelled teaches facts: UTF-16 sorting and ECMAScript numbers as above; **“JSON objects MUST NOT exhibit duplicate property names”** (`:327-328`); NaN/Infinity **“MUST cause a compliant JCS implementation to terminate with an appropriate error”** (`:497-500`). The whitespace clause is supported only with the missing between-tokens restriction (finding 3).

Both labelled clauses are absent as statements of this page: the parser-erratum claim (finding 4) and the Python `json.dumps` restricted-domain comparison. Full-copy searches for `json\.dumps|SHOULD.error|2024.05.15|parser.*error|error.*parser` found no such statement. Its Python implementation link (`S062.src:1538`) is not that comparison. No page-stated clause was newly labelled, but the erratum attribution remains improperly presented as a source-backed fact.

### S064 — labelled material correctly delimited, unlabelled policy remains

Attack surface: `corpus/SOURCES.md:70`; list agrees at `round-33.md:88-91`.

Supported resolution/flags/peeling/full-name material is quoted in finding 2. The `C2` prefix is a lane use identifier, not a statement by Git; do not treat it as page provenance. Neither labelled scope exclusions (remote publication/authenticity/input-tree equality) nor labelled register/correction-byte binding and the hash-printer limitation are stated by this copy; source search and API quotes are recorded in finding 2. No source-stated fact was wrongly labelled. **`once` and `retain` are still undeclared**, despite the wave-1 draft naming both.

### S069 — no additional placement defect found (severity: none)

Attack surface: `corpus/SOURCES.md:75`; list agrees at `round-33.md:92`.

Unlabelled string-only/symlink claim: **“works with strings. It does not check or access the underlying file structure”** and **“assumes that no symlinks are present in the path”** (`S069.src:918-922`). Unlabelled lexical/resolved scope is also supported by **“This method is string-based; it neither accesses the filesystem nor treats ‘..’ segments specially”** (`:783-784`) and the instruction to call `resolve()` when needed for symlinks (`:920-922`).

Both labelled instructions—reject absolute/`..` before any filesystem call, and test symlinks separately—are not stated. Full-copy search `reject absolute|before any filesystem|test symlinks|test.*separately|reject.*\.\.|lexical.*reject|reject.*lexical` returned no matches. The source's conditional `resolve()` recommendation is not that rejection/testing policy. No correction beyond retaining this boundary.

## Limits and tools

Performed: both fixed-revision diffs; direct committed-copy passage reads and targeted full-copy searches; PDF extraction; comparison against all six old-to-new entries and ScopeS064's draft. Working-tree copies were used under the assignment's explicit identity statement, not independently hashed against the revision.
Not performed: fresh URL fetches, judge/counter runs, tests, builds, or serializer execution. Labels declare attribution; they do not themselves make the lane clauses page-supported under R-R (`contract.md:85-88`).
No tools installed or updated. Only this report was written inside the lane; scratch extraction stayed under the assigned seat directory. All commands ran synchronously and returned; no background process was started.
