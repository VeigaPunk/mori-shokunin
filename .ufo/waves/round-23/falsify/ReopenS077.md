# ReopenS077 — S077 source re-open (round23 falsification)

- Seat: `MadoR22-2.ReopenS077` (read-only source re-opener; no subagents).
- Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`; pinned production
  `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` (ancestor of lane HEAD `6eb889c`;
  confirmed with `git merge-base --is-ancestor`), expectation seal
  `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`.
- Scope: re-open registry row S077 only — URL/anchor, raw SHA-256, lesson23 Gate
  quote (≤25 words), and the new knowledge note's XFS claims versus S077/S078.
  No implementation, oracle, case, expected, frozen, or registry bytes touched.
  No live host/quota reads, no session transcripts, no builds/tests/linters.

## Observed verification

### 1. URL, tag, and byte identity (three-way)

| Check | Observed value | Result |
|---|---|---|
| Registry URL (`corpus/SOURCES.md:83`) | `https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/xfs.rst` | exact |
| Fetched bytes (curl to `$TMPDIR/xfs.rst`) | 22719 B | — |
| SHA-256 of fetched bytes | `53bda67b5612a3f2c02820604d05825c9d37addba9855e1d4fba330a516d051c` | matches registry/manifest |
| `evidence/sources/S077-Documentation_admin-guide_xfs.rst` | byte-identical (`cmp` exit 0), same SHA-256 | matches |
| Git blob at pin `f3dc07c0:…/evidence/sources/S077-…` | same SHA-256 | matches |
| `evidence/sources-manifest.json` S077 | `bytes: 22719`, same `sha256`, same URL | matches |
| `evidence/source-quotes.json` S077 | same quote, `word_count: 11`, `found_in_whitespace_normalized_source: true`, same sha256 | matches |
| Tag identity via GitHub API `refs/tags/v7.2` | annotated tag object `237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63`; path blob SHA-1 `acdd4b65964c058647a7b383d8c2c778777a538e`, size 22719 | tag-bound, equals local `git hash-object` |

The registry’s truncated `sha256 53bda67b5612a3f2` is a correct 16-hex prefix of
the full digest. Every byte identity agrees; no mismatch.

### 2. Scope and anchor

`Mount Options` section runs lines 19–225 (`Deprecation of V4 Format` starts at
226). The quota option vocabulary is exactly lines 171–185:

- 171–173 `noquota`
- 175–177 `uquota/usrquota/uqnoenforce/quota`
- 179–181 `gquota/grpquota/gqnoenforce`
- 183–185 `pquota/prjquota/pqnoenforce`

All `quota` matches in the file are confined to 171–185 plus two non-option
mentions (519, 525: quotacheck workqueue text). Registry anchor
`Mount Options:171-185`, tier `A`, `docs`, status `mined`, date `2026-10-21`,
freshness `on-release` all agree with the source and the Gate statement. No
scope overreach in the registry row: it claims “noquota and per-scope option
vocabulary, not limit values”, which is exactly what the file documents.

### 3. Gate quote (lesson23 line 43)

Quote: “Forcibly turns off all quota accounting and enforcement within the
filesystem.”

- Source location: sentence text on lines **172–173**; it is the description of
  the `noquota` entry whose key line is 171.
- Word count: 11 (≤25). Unique occurrence in the whitespace-normalized file
  (count 1); the line-break join “enforcement” + “within” is the only
  normalization needed.
- Gate decision/scope (“Admit A for XFS noquota vocabulary only, not limits or
  all enforcement states”) matches the source: the file states no numeric limit
  and does not enumerate runtime enforcement states.

Precision observation (not a wrong quote): the Gate cites `171–173`, which is
the whole option entry including the key line; the quoted sentence itself starts
on 172. `build/DraftSourceRows.md:61` records the sentence at `xfs.rst:172-173`.
Both readings are defensible (entry range vs sentence range); nothing in the
registry, oracle, or case bytes depends on the distinction.

### 4. New knowledge note claim-vs-source (XFS rows only)

`corpus/knowledge/quota-surface-r23.md` lines 37–40, checked against S077 and
S078 (`fs/xfs/xfs_super.c`, fetched: SHA-256
`0a95697dcfcdab8f7ab6ea26fdb941db952db4b73ed93c30d21e40861ed0450c`):

| Note row | Claim | Source check |
|---|---|---|
| 37 | `noquota`, no other quota flag → disabled; “S077/S078: no accounting flags” | Supported. S077:172–173 says noquota turns off all accounting/enforcement; S078:253–254 emits `,noquota` only when `!(m_qflags & XFS_ALL_QUOTA_ACCT)`; parser clears `XFS_ALL_QUOTA_ACCT|XFS_ALL_QUOTA_ENFD` (S078:1542–1543). No capacity/health statement exists in S077. |
| 38 | `usrquota/grpquota/prjquota` or accepted enforcing alias → enabled/enforced; “at least one enforcement flag, not a nonzero limit or every quota type” | Supported, but by **S078**, not by S077 alone: S078:238–252 emits `usrquota`/`prjquota`/`grpquota` only under the corresponding `*_ENFD` flag, else the `*noenforce` token. S077’s own wording is weaker (“limits (optionally) enforced”), so the note is correct to cite S078 for the state mapping. The row does not claim a limit value. |
| 39 | only `uqnoenforce/gqnoenforce/pqnoenforce` → enabled/accounting_only; “accounting is not enforcement” | Supported for **observable mountinfo output**: S078:241/246/251 emit only those three accounting-only tokens; S078:1553–1558 maps them to ACCT-without-ENFD. Caveat below on input-vocabulary completeness. |
| 40 | `noquota` plus a quota flag, or no quota token → unknown; “defensive parser rules, not claimed normal v7.2 kernel output” | Supported as a non-claim: `xfs_fs_show_options` cannot emit either shape (per-type ENFD/ACCT token, plus `,noquota` only when no ACCT), so these fixture inputs are synthetic. The note explicitly declines to attribute them to kernel output. No contradiction with S077. |

No note claim contradicts S077/S078. Two precision caveats, neither a false
claim and neither an implementation finding:

1. **`qnoenforce` is an accepted input alias but is not in the note’s
   enumeration.** S078:116,165–168 accepts `qnoenforce`, and S078:1553–1558
   maps it to user-quota ACCT-without-ENFD (same as `uqnoenforce`). The
   contract’s accounting-only key list includes it; `xfs.rst` does not document
   it, and `xfs_fs_show_options` never emits it. So the note’s three-token list
   is complete for *surface evidence* but not for *accepted input vocabulary*.
2. Row 38’s “enforced” is a statement about the enforcement flag being set, not
   about any limit existing; the row states this limitation itself, matching
   S077’s “limits (optionally) enforced”.

The note’s line 54 “XFS /tmp with noquota” is a dated control observation, not
an S077 claim; it was not re-read here (live host reads are outside this seat’s
authorization).

## Concrete discrepancies (reported only; nothing edited)

1. **`build/CaseXfsDevMismatch.md:41` and `:128`** cite “`xfs.rst` lines
   170–184”. The verified quota block is **171–185**: 170 is a blank line and
   184 truncates the project-quota description before its final line 185. The
   registry (`171-185`), `build/DraftSourceRows/rows.md:10`,
   `build/CaseXfsOptionsAbsent.md:108`, and `build/SrcXfsDoc.md:118` already use
   the correct range; `SrcXfsDoc.md` explicitly records the 170–184 → 171–185
   correction. Severity: low, stale draft citation, not frozen authority.
2. **`build/CaseXfsConflict.md:61`** cites `:171-172` for a quotation that
   includes “within the filesystem.” (line 173). Correct entry range is
   171–173; correct quoted-sentence range is 172–173. Severity: low, draft
   citation only.
3. **Gate anchor vs sentence anchor**: lesson23:43 cites `171–173` for a
   sentence typed on 172–173 (`DraftSourceRows.md:61` cites 172–173). Entry
   range vs sentence range; informational, no correction requested, and no
   registry/lesson edit made.

No discrepancy was found in the registry row itself: URL, anchor, prefixed
SHA-256, scope statement, tier, status, date, freshness, and used-by pointers
(`corpus/lessons/round-23.md`, `corpus/knowledge/quota-surface-r23.md`) are all
consistent with the re-opened bytes. Both cited consumer files exist and cite
S077.

## Non-claims and limits

- This seat read only the pinned source, the registry/lesson/note, the named
  evidence files, and wave build drafts; it did not read any implementation,
  oracle, frozen case/expectation bytes, transcripts, or host state.
- No claim is made about C1 calibration, C2 coverage, the frozen
  `CaseEscapedSpace` contradiction, the quota selftest, or any driver result;
  none was executed or inspected here beyond the governance documents.
- Nothing was installed or updated; scratch was
  `/fast/scratch/hyaku/mori-r23/ReopenS077/` only, no `/tmp`.
- Confidence: high for byte/hash/tag/line/scope identities (independently
  fetched and compared to pinned git blobs); high for the note rows’ source
  support as stated, with the `qnoenforce` enumeration caveat above; the dated
  `/tmp` control observation remains unverified by design.

report: .ufo/waves/round-23/falsify/ReopenS077.md
