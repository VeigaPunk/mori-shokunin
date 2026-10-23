measured 2026-10-23T09:17:21Z

# GateS200 — live re-open of source row S200 and its Gate line at cedb0ec4

VERDICT: admit — agree with the Gate's `admit, A` decision on S200. Row is at `corpus/SOURCES.md:206`,
Gate line at `corpus/lessons/round-35.md:19`, tip `cedb0ec4f3a4f672804deac388b7191258f01fcd`.

## Fetch, sha256, committed copy

- `git -C /home/vgpnk/Projects/shokunin show 37b51a243302e8009c7067431e8a47f9a722fd14:MANIFEST.json`
  → `/fast/scratch/hyaku/mori-r35/GateS200/MANIFEST.live.json`, 1,281,173 bytes,
  sha256 `0b414b8a926f44b54f11fedbbc4f9a00ef2075659dcf1e52db5ff57395ae9952`.
  Matches the Gate cell `0b414b8a…ae9952` (`round-35.md:19`).
- Committed copy: the source IS a fleet git object, so the fetch is the committed copy by content
  addressing. Consistent with the Gate listing `.src` copies only for S199/S203/S204 and the
  byte-identity note for S201/S202 (`round-35.md:13`); no `S200.src` exists
  (`git ls-tree cedb0ec4 corpus/evidence/sources-r35/` → S199/S203/S204 only). This is a policy gap
  to note, not a defect: content-addressed bytes need no duplicate receipt. Fetch receipt retained
  under scratch for the wave.

## Quote check (S200)

- Gate quote `sources-registry (34 rows; census clean)` located at `rounds[313].capabilities_added[0]`.
  Verified: `rounds[313]` is `{"lane":"mori","round":12,"admitted":true}`, and
  `capabilities_added[0]` is the exact contiguous string `sources-registry (34 rows; census clean)`;
  5 whitespace words, no `"` or `|`. Match.
- Gate claim `13 admitted mori entries carry 18 capabilities`: verified — 23 entries with
  `lane:"mori"`, 13 `admitted:true`, summing exactly 18 `capabilities_added` strings. Caveat noted
  for the record, not a defect: `rounds[372]` (mori round 17, `admitted:false`,
  `verdict:"rejected-harmed"`) also carries 3 `capabilities_added` — the claim is precisely "for an
  admitted round", which is what it states.

## Anchors / teaches (S200)

- Anchor: `rounds[*] entries with lane mori` — all 23 mori entries carry
  `round, admitted, capabilities_added, commit, verification, report` (0 missing keys across the set).
- Teaches says only what the lines state: entries record admission; `capabilities_added` holds the
  capability strings per admitted closure; "keyed by position" is borne out by `SCORECARD.md:1945`
  (`The key is that closure's rounds[i].capabilities_added[j]` — positional list index).
- used-by `SCORECARD.md` resolves (`SCORECARD.md:1945` cites S200 explicitly).

## Supersedes and no-edit checks (Change §3)

- S201 teaches opens `supersedes S182 —` and S202 opens `supersedes S193 —` (`SOURCES.md:207-208`). ✓
- `git diff dd76eb79..cedb0ec4 -- corpus/SOURCES.md`: single hunk, only `+` rows S200–S202; zero
  `+`/`-` lines on S182 or S193 rows. "S182 itself is left as it stands" / "S193 itself is left as
  it stands" (`round-35.md:36,40`) confirmed.
- S201/S202 corroborated live: `genhd.c` sha `8c2faa15…d39a5` and `core.c` sha `fa223c8f…1c9fa` match
  the Gate, and are byte-identical to committed `corpus/evidence/sources-r33/S182.src` /
  `sources-r34/S193.src` (same digests) — the "no new copy" rationale holds. All six quoted lines
  verified contiguous verbatim at `genhd.c:485,518,623` and `core.c:3508,4655,4706`; no `"`/`|` in
  any quote. S201 teaches is bounded by `genhd.c:485-486` (parent+groups), `:512-518`
  (part0 bd_holder_dir + slave_dir), `:620-623` (device_add_disk passes parent to add_disk_fwnode).
  S202 teaches is bounded by `core.c:2430-2433` (device_is_not_partition def), `:3508-3510`,
  `:3542-3543` (add/remove gated on parent && not-partition), `:4653-4657`, `:4704-4706`
  (device_move → device_move_class_links, old-parent remove / new-parent create with no partition
  check inside the function).

## Findings

1. **defect (minor, cell accuracy) — S201 word-count labels.** Gate `round-35.md:20` labels the three
   S201 quotes (4),(4),(6); `wc -w` gives 3,3,5 (the `->`,`(` tokens don't split words). S200's (5)
   and S202's (5),(2),(5) are correct. Same failure class the round-30 correction recorded for
   `round-29.md` (`SOURCES.md` search-log correction). Quotes themselves are verbatim and located;
   decision unaffected.
2. **defect (adjacent rows, shared Gate table) — QUALITY-86 gate-format check fails on round-35.**
   The QUALITY-86 awk (QUALITY.md:441, committed this wave) run on `round-35.md` at cedb0ec4 prints
   `gate_reject_rows=0 none_declared=0 malformed=2`, exit 1: S203/S204 decision cells read
   `**reject**: <reason>` (round-35.md:22-23) instead of `reject, <reason>`. S200's own cell
   `admit, A …` conforms; reported here because the check governs the whole Gate artifact.
3. **observation — kind vocabulary.** S200 is the registry's only `dataset` kind; the Gate cites a
   "CORPUS rule for `own-work`" which actually governs reject-row source prefixes (QUALITY.md:435,
   requires `https?://|own-work:|gist:` for reject rows only — admit rows unconstrained, so no rule
   breach). S034 precedent shows `own-work` kind for a repo-command source; `dataset` is new but
   unenforced by any committed check.

## Residual risk / gaps

- No committed `.src` receipt for S200 (see Fetch); if a future fleet gc or rewrite dropped the
  object, the row would be unreproducible — currently a non-issue since the object is fleet-committed.
- Word-count convention for Gate cells is de-facto `wc -w` (round-30 correction); recommend the L1
  log the S201 mislabels append-only, as round-30 did.
- Did not re-derive `34 rows` inside the quoted capability string (it is the string's own content,
  not a Gate claim); noted only.
- Scratch: `/fast/scratch/hyaku/mori-r35/GateS200/` (MANIFEST.live.json, genhd.c, core.c).
- No installs performed; standard tools (git, curl, sha256sum, awk, python3) sufficed.
