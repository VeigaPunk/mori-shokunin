# Round 22 — SourceAdmit: S064 quote and scope review

Path root for relative paths in this report: /home/vgpnk/Projects/shokunin/mori-shokunin.

Seat: MoriR22.SourceAdmit (leaf reviewer). Author-side lane evidence only. This is not the outside non-author closure: the contract says "Outside closure decides admission", and round-21 lesson line 29 says "Lane-dispatched source reviewers do not replace this check." Static review only. No executions, tests, builds, linters, installs, delegation, or edits. This file is the only write.

Inputs read first: `.ufo/waves/round-22/denominator-correction.md` (no S064 bearing); `contract.md` (lines 3, 11, Frontier); `corpus/lessons/round-22.md` lines 20-35 (Gate, carried scope); `corpus/SOURCES.md` S046, S064, S065 rows and bounded search 13; `corpus/lessons/round-19.md` S064 row, C2 section, Main spot-check; `corpus/knowledge/retention-reconciliation-r22.md`; `corpus/knowledge/freeze-order-r18.md:40-57`; `evidence/source-spotcheck.json`; `build/SrcGitCommit.md` and `build/SrcRejectHash.md` (verified, not repeated); `tools/mori-retention-reconcile.py` lines 1-283, all ranges read. Docs: https://git-scm.com/docs/git-rev-parse (2.56.0, reader text and raw HTML); installed `/usr/share/man/man1/git-rev-parse.1.gz` ("Source: Git 2.56.0"); pacman local DB lists `git-2.56.0-1` (names only).

## Result

- Both S064 Gate quotes are verbatim in the 2.56.0 docs after markup normalization. Both are within 25 words and correctly located. The admitted scope, "resolving an existing commit", is supported by the quoted sentence.
- The non-claims (authorship, push status, privacy, authenticity) are correct. The page is silent on them. No round-22 lesson, knowledge note, registry row, or falsify report uses S064 for privacy, secrecy, or authenticity.
- The shipping tool's rev-parse use (`tools/mori-retention-reconcile.py:65-69`, `:165-166`) matches the documented pattern. The S064 scope holds for the code as shipped.
- Defects are attribution and linkage: the outside-check record is unlinked (SA-1); the registry `teaches` cell credits S064 with blob-binding it does not state (SA-2); several cells and notes are stale or incomplete (SA-3 to SA-8). None invalidates a quote.
- Status of the S064 re-admission: author-admitted. The outside check is recorded but unlinked, so the re-admission should not be cited as outside-closed until SA-1 is resolved.

## Findings (severity order)

All actions are dated appended notes. No immutable cell is rewritten.

### SA-1 — Medium — Outside-check record exists but is unlinked; lesson says "pending"

- Evidence: `.ufo/waves/round-22/evidence/source-spotcheck.json:3-16` records Main (parent orchestrator, non-author) with verdict "agree" for S064. Its scope is "Source admit/reject sample only". Its quote claim checks out (VN1).
- `corpus/lessons/round-22.md:31`: "Outside admit/reject review remains pending unless a separately retained named non-author record is appended." No corpus file cites the round-22 record; a corpus grep for `source-spotcheck` returns only the round-21 lesson.
- Precedent: `corpus/lessons/round-21.md:29` cites its own spot-check file. `corpus/lessons/round-19.md:121-139` records the Main check in the lesson. `corpus/lessons/round-12.md:33` (M10): the named non-author spot-check belongs in the lesson's Gate section.
- Impact: the lesson of record is inconsistent with its own evidence. Whether Main counts as outside closure is a protocol call. Round-19 treated Main as outside; round-21 says lane-dispatched reviewers do not count. This seat does not decide it.
- Action: append a dated pointer in the lesson Gate. Either cite `source-spotcheck.json` as the named non-author record with its stated scope, or keep "pending" and give the reason. Leave line 31 unchanged.

### SA-2 — Medium — Registry `teaches` cell credits S064 with content it does not state

- Evidence: `corpus/SOURCES.md:70` teaches: "…then separately bind the actual loaded register/correction bytes to blobs at that commit; a hash printer alone does not prove the latter."
- Supported by the docs: `--verify` emits the object name, and `^{commit}` makes the name existing and commit-ish (raw HTML lines 2725-2728; reader line 340). The `--short` entry ("Same as --verify but shortens the object name", raw line 2759) supports full-name output for plain `--verify`.
- Not stated by the docs: loaded-bytes binding, and anything about hash printers. The closest documented blob naming is SPECIFYING REVISIONS `<rev>:<path>`: "names the blob or tree at the given path in the tree-ish object named by the part before the colon". The tool does not use that form.
- The tool binds blobs with `ls-tree -r -z --full-tree` and `cat-file blob` (`tools/mori-retention-reconcile.py:71-89`, `:160`, `:170`). No SOURCES row, README, QUALITY, or round-22 knowledge note cites `ls-tree` or `cat-file`. Other matches in the corpus are command text (evidence logs, lessons, and knowledge notes such as `corpus/knowledge/audit-r11.md:158`), not source citations.
- Related: `.ufo/waves/round-22/build/SrcRejectHash.md:21` says the measured-revision-to-blob linkage "comes from Git object resolution (S064 scope)". That is not supported as written. S064's registry scope excludes "input-tree equality", and blob reads go through ls-tree and cat-file, not rev-parse.
- Impact: a future reader could cite S064 for the core provenance claim. The round-22 lesson does not do this; its Gate row cites only the `--verify` quote.
- Action: append an attribution note moving the blob-binding and hash-printer sentence to the lesson or knowledge note that owns it. If the corpus should ground ls-tree and cat-file, open those docs and admit them with Gate quotes (L1 decision; ≤25-word rule applies). Good precedent in the same registry: `corpus/knowledge/freeze-order-r18.md:51-54` cites S064 only for `--verify`/peeling.

### SA-3 — Low-Medium — `used-by` omits two knowledge notes that cite S064

- Evidence: `SOURCES.md:70` used-by lists only `corpus/lessons/round-19.md, corpus/lessons/round-22.md`. Cited but unlisted: `corpus/knowledge/freeze-order-r18.md:51-52` and `corpus/knowledge/retention-reconciliation-r22.md:1` and `:37`. The registry convention lists knowledge notes in used-by (S002 at `SOURCES.md:8`, S013 at `:19`).
- Build note `build/SrcGitCommit.md:14` found the freeze-order citation, but its proposed used-by addition omitted it.
- Impact: lineage gap only. No admission effect.
- Action: append used-by old→new in the same style as `round-22.md:29`, naming both knowledge notes.

### SA-4 — Low — The lesson's reason for not rewriting S064 cells does not apply

- Evidence: `round-22.md:29`: "Immutable original version/anchor cells are not rewritten because a live page version changed." The live page (checked 2026-10-21) still reads "git-rev-parse last updated in 2.56.0", with the 2.56.0 entry dated 2026-09-28. That matches the anchor at `SOURCES.md:70`. The installed man page reads "Source: Git 2.56.0".
- Action: append a dated note that no S064 version change was observed, and that the cells are unchanged for that reason.

### SA-5 — Low — S064 scope carries round-19's claim label; round 22 uses C1

- Evidence: `SOURCES.md:70` scope begins "C2 resolving…" (round-19 claim). Round 22 has one claim, C1 (`contract.md:3`). The Gate row (`round-22.md:26`) names no claim. `build/SrcGitCommit.md:63` says "C1 revision resolution only".
- Action: append a note naming C1 as the round-22 use of S064.

### SA-6 — Low — Anchor and Gate scope omit parts the shipping tool relies on

- (a) The `<rev>^{<type>}` definition, and `<refname>` precedence for symbolic names, live in SPECIFYING REVISIONS. The OPTIONS `--verify` text the anchor cites gives only the example.
- (b) "If you are verifying a name from an untrusted source, it is wise to use `--end-of-options`" (reader 343-345) is used in both rev-parse calls (`tools/mori-retention-reconcile.py:67`, `:165`). The Gate scope "only for resolving an existing commit" does not name it.
- (c) Symbolic `--rev` names such as `master` resolve by the SPECIFYING REVISIONS rules. The receipt binds the resolved object id (`input_revision`, line 230) and records the original selector in argv (line 233). The contract's "exact committed input revision" (`contract.md:11`) holds by object id after resolution, not by name. The lesson's "strict committed-input provenance" (`round-22.md:31`) should be read the same way.
- Action: append an anchor addendum naming SPECIFYING REVISIONS and the `--end-of-options` use. No cell rewrite.

### SA-7 — Low — SHA-256 branch of the OID check is not covered by the `--verify` text

- Evidence: `--verify` says "can be turned into a raw 20-byte SHA-1" (reader 332-334). The shipping check accepts 40 or 64 lowercase hex (`tools/mori-retention-reconcile.py:20`, `:68`). S064 documents SHA-256 only under `--output-object-format` and `--show-object-format` (reader 398-408, 563-566).
- Impact: none for the SHA-1 repository in use. The build note reports sha1; I did not re-verify that, since nothing was executed. Latent scope gap.
- Action: derive the expected width from `--show-object-format`, which the page does document. Otherwise record the 64-hex branch as unexercised.

### SA-8 — Low — Ancestry claims are unsourced in the corpus; build note misstates the registry

- Evidence: `corpus/knowledge/retention-reconciliation-r22.md:35` says the measured commit is "an ancestor of or equal to the input commit". S046 (`SOURCES.md:52`, tier A, "ancestry-check exit status": 0 ancestor, 1 not ancestor, other nonzero error) covers the exit codes. Its scope text says nothing about the equal-commit case.
- `build/SrcGitCommit.md:67` says "R14 ancestry has no admitted source." That is wrong as a registry statement. S046 is admitted, and is currently used only by `jj-branch-anchor-r17.md`.
- The tool's exit mapping (`tools/mori-retention-reconcile.py:167-168`) matches S046. The equal-commit case rests on unrecorded observation.
- Action: the knowledge note should cite S046 for the exit semantics and mark the equal-commit case as observed or source it. Do not carry the build note's "no admitted source" claim forward.

### Incidental (outside S064 scope)

- `tools/mori-retention-reconcile.py:167` comment: status 1 is a "divergence (distinct finding)". Lines 168 and 59 map status 1 and other nonzero statuses to the same exit-2 SETUP. They differ only in the sanitized error code. Comment wording only.

## Checked, no finding

- **VN1** Quote 1, `round-22.md:26`: "git rev-parse "$VAR^{commit}" will make sure $VAR names an existing object that is a commit-ish". Raw HTML lines 2727-2728 match after tag stripping and whitespace normalization. Reader line 340 matches. Location: OPTIONS → Options for Output (reader line 307) → `--verify` (line 330). 15 words.
- **VN2** Quote 2, `round-19.md:42`: "This will error out if $REV is empty or not a valid revision." Verbatim at reader line 1168 and in the installed man page EXAMPLES.
- **VN3** The non-claims in `round-22.md:26` and `SOURCES.md:70` (authorship, push status, privacy; remote publication, source authenticity, input-tree equality) are correct. The page does not address them.
- **VN4** "Untrusted source" (reader 343-345) concerns option injection, not authenticity. It must never be cited for authenticity.
- **VN5** Shipping `resolve()` (`tools/mori-retention-reconcile.py:65-69`) is `rev-parse --verify --end-of-options <sel>^{commit}` plus a full-OID check. This matches the S064 EXAMPLES. `a.rev` is used only at line 158; later steps use the resolved `revision`. AttackR24's concern about echoing the selector does not apply to current source: line 230 emits `revision`.
- **VN6** `measured_revision` handling (`:163-166`): full-OID shape plus `^{commit}` peel-equality. This is consistent with S064 peeling semantics and the `--short` contrast.
- **VN7** Annotated-tag peeling for `--rev` is documented behavior (SPECIFYING REVISIONS `<rev>^{<type>}`; `--verify` text on annotated tags). It is not a silent defect. The AttackR13 build note's "silently peels" is accurate about the outcome but is not a defect.
- **VN8** No authenticity or privacy claim is attributed to S064 in the round-22 lesson, knowledge, registry, or falsify files. Tool output carries `receipt_authenticity: 'unattested'` (`:231`) and `privacy_clearance: False` (`:230`, `:278`).
- **VN9** Local docs match web docs. The installed man page reads Git 2.56.0, and the pacman DB lists `git-2.56.0-1`. The cited docs describe the binary the tool calls (static inference).

## Residual risk and verification gaps

- No execution. Runtime behavior of rev-parse, merge-base, ls-tree, and cat-file is inferred from docs and source reading. The selftest (`:238-266`) was not run.
- Outside closure (SA-1) remains unresolved in the lesson of record.
- The SHA-256 path (SA-7) and the equal-commit ancestry case (SA-8) are unexercised.
- S064 speaks of "your object database" (raw line 2725). A resolved id therefore names an object in the local store, including any alternates. S064 does not establish that store's authenticity or integrity, and the tool neither checks alternates nor grafts. This bounds the phrase "strict committed-input provenance" and is not sourced.
- S065 and the rest of the round-22 Gate are outside this assignment and were not reviewed.

## Build-note verification

- `build/SrcGitCommit.md`: quote verified (VN1); "--short implies full name" verified; hash-width note verified (SA-7); "R14 has no admitted source" refuted (SA-8).
- `build/SrcRejectHash.md:21` ("linkage comes from … S064 scope"): refuted as written (SA-2).
- `build/AttackR13.md:63` ("silently peels"): outcome correct, not a defect (VN7).
- `build/AttackR24.md:21` (echoing `a.rev`): not true of current source (VN5).

## Process disclosures

- Repo-wide `S064` grep matched 91 files. The 20 displayed were all under `.ufo/waves/`. I did not page further and did not open any result outside `.ufo/waves/`. The matches included wave dispatch and response JSON records (assignment text). I did not open those records and read no session transcript, agent DB, credential, or shell-history content. The displayed context carried field names from those records, not transcript content.
- A round-22 `rev-parse` grep and an `S064` grep over `corpus` and `.ufo/waves/round-22` produced the same kind of matches, with the same limit.
- Other searches were scoped to `corpus/`, `tools/`, `.ufo/waves/round-22/`, and the docs named above.
- Web: `https://git-scm.com/docs/git-rev-parse`, read as reader text and raw HTML. Local: `/usr/share/man/man1/git-rev-parse.1.gz`, and the pacman local DB directory listing (names only).
- Installs or updates: none. No file was written except this report. No `/tmp` use. No matched retention text is reproduced here.
