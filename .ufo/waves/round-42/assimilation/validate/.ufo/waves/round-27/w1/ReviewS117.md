# ReviewS117 — routed D2: the r26 entry's S117 citation vs the landed row

Seat: MoriR27.ReviewS117 (reviewer, leaf). Date: 2026-10-22. Lane: mori-shokunin.
Route: round-26 spot-check D2 — "the r26 entry's `source:` line describes S117 as a different
source than the row (URLs and scope)" (`corpus/lessons/round-26-verifier-spotcheck.md:183-185`).

**Verdict.** The entry's description of S117 diverges from the landed row on two URLs and on
scope. Of the three claim groups the entry hangs on S117, two are grounded by other landed rows
(S114, S016); the third — the 2026-02-02 master re-introduction date — is grounded nowhere with
a located quote, so **a new SOURCES row is needed**. QUALITY #77 requires the line-1 fix to be
swept in place, not banner-corrected; exact text in §5. Row draft and Gate block in §6.

## 1. Read and re-opened (receipts)

Local: `corpus/SOURCES.md:123` (S117), `:120` (S114), `:125` (S119), `:22` (S016);
`corpus/knowledge/userspace-oom-killers-r26.md` (whole entry; S117 occurs only in line 1 —
repo-wide sweep over `corpus/` found no other entry use); `corpus/QUALITY.md:349-364`;
`corpus/lessons/round-26-verifier-spotcheck.md:149,165-166,183-187`;
`.ufo/waves/round-26/w1/DraftEntryR26.md:316-591` (the scribe draft's §3–§4).

Remote (ordinary `curl`, no browser, no challenge; access date 2026-10-22):

| URL | Bytes | sha256 |
|---|---|---|
| `https://api.github.com/repos/rfjakob/earlyoom/releases/tags/v1.9.0` | 2,170 B | `796dee931d1a093f48f2fe47fac5530dbdd0163ecd264ee3027eb8987de3ff46` |
| `https://api.github.com/repos/rfjakob/earlyoom/commits?path=main.c&per_page=100` | 403,197 B | `e21b1c770fdd364189b89719aed86b4f65079ad021ec22f6a7bdb587a7337533` |
| `…/earlyoom/v1.9.0/main.c` | 552 lines | `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4` (= row S117/S119 and entry line 1) |
| `…/earlyoom/v1.9.0/README.md` | — | `23411dbfd8b409d433f984a5d6677830e86a383ec76935fc1e1d675e6b4374dd` (= S114) |
| `…/earlyoom/master/main.c` | — | `baeb78a6e45037ba17901b6897b780f3997687db61d23c7811b424fa99264370` |
| `…/earlyoom/750a7c0d97bb01c1bdf126fd6bf5722da17e8998/main.c` | 585 lines | `d24a26c97744458706a870ee3eb1ddcd5e5f05dda11fe22a71d6a4952028df3e` |

The single-release endpoint returns `tag_name` `v1.9.0`, `published_at`
`2025-09-16T19:11:03Z`, `target_commitish` `master` — and `"body": ""`: the v1.9.0 release
carries **no notes text**, so no release-body sentence can ground any entry claim. (These are
JSON fields, not located lines — the same weakness the round-26 spot-check recorded for the
original S117 Gate quote, `round-26-verifier-spotcheck.md:149`.)

Tooling: nothing installed (preexisting `curl` and `python3`); no pacman transaction. Scratch:
`/fast/scratch/hyaku/mori-r27/ReviewS117/`.

## 2. The row vs the entry's description — exact divergences

Row S117 (`corpus/SOURCES.md:123`): title "earlyoom release and tag history with the
logged-message grammar at tags v1.7, v1.8 and v1.9.0"; URLs `api.github.com/repos/rfjakob/earlyoom/tags`,
`api.github.com/repos/rfjakob/earlyoom/releases`, plus raw `main.c`, `kill.c`, `msg.h`,
`README.md` at v1.9.0 and `main.c`, `kill.c` at v1.8 and v1.7; scope = which tag carries 1.9.0
and its date, and the stability of the log-message prefixes across those tags; explicitly not
kill-selection logic, host unit state, or kill history.

Entry line 1 says: "S117 (earlyoom tag history — https://github.com/rfjakob/earlyoom/releases
and https://api.github.com/repos/rfjakob/earlyoom/commits?path=main.c — the v1.9.0 tag and
commit, the v1.2 removal of the kernel-oom option and its 2026-02-02 re-introduction on master;
opened 2026-10-22)".

| # | Aspect | Row (SOURCES.md:123) | Entry (userspace-oom-killers-r26.md:1) | Divergence |
|---|---|---|---|---|
| 1 | Releases URL | `https://api.github.com/repos/rfjakob/earlyoom/releases` (API list) + `…/earlyoom/tags` | `https://github.com/rfjakob/earlyoom/releases` (HTML page) | different identifiers; the HTML page is in no row |
| 2 | Commits URL | absent | `https://api.github.com/repos/rfjakob/earlyoom/commits?path=main.c` | the entry attributes a URL the row does not carry |
| 3 | Scope | tag identity/date + log-grammar stability at v1.7/v1.8/v1.9.0 | "the v1.2 removal of the kernel-oom option and its 2026-02-02 re-introduction on master" | option history is outside the row's declared scope and period |
| 4 | Title | "release and tag history with the logged-message grammar …" | "earlyoom tag history" | shortened, drops the grammar subject |
| 5 | Evidence | tags/releases anchors, per-file sha256s, opened date | "opened 2026-10-22" only | no sha256 or anchor for the attributed claims |

## 3. What rests on S117, and whether another row grounds it

Per line 1, three claim groups are attributed to S117:

**(a) The v1.9.0 tag and commit** — consumed by `verified-at` (entry line 2) and every
"at tag v1.9.0" anchor (F2, F5, F6, F7, Limits). Also grounded without S117: the S114 row
records "tag v1.9.0 = commit 202d4db0d308ca6478f68de68b46cae34896ddaf (2025-09-16)"
(`SOURCES.md:120`), as do S119 (`:125`) and the entry's own S114 parenthetical (line 1).
**Redundantly grounded: yes.**

**(b) The v1.2 removal of the kernel-oom option** (F7, entry:128-132: "the `-k` / kernel-OOM
option was removed in v1.2 and is ignored for compatibility"). Grounded by **S114 as landed**:
its evidence cell anchors "kernel-oom absence:65-67,383,289-293" (`SOURCES.md:120`), and
`README.md:383` at v1.9.0 reads "Remove option to use kernel oom-killer (`-k`, now ignored for
compatibility)" (11 words; the issue link follows on :384). The ignore literal itself is in
v1.9.0 `main.c:245-246`: `case 'k': fprintf(stderr, "Option -k is ignored since earlyoom
v1.2\n");` — inside S119's bytes, though S119's declared scope (`SOURCES.md:125`) does not name
option parsing. The round-26 spot-check's summary ("also anchored in S114",
`round-26-verifier-spotcheck.md:165-166`) is confirmed against current bytes. **Grounded
elsewhere: yes (S114); S117 attribution unnecessary.**

**(c) The 2026-02-02 re-introduction on master** (F7 Limit, entry:139: "Upstream master has
carried a kernel-OOM trigger option again since 2026-02-02"). Split verdict:
- *That master carries it:* grounded by **S016** (`SOURCES.md:22`) — upstream master README at
  pinned commit `8477c902` (2026-10-19), scope "earlyoom userspace kill flow, logged actions and
  --kernel-oom delegation".
- *The date "since 2026-02-02":* grounded **nowhere with a located quote**. The only in-corpus
  assertion is S114's unanchored evidence parenthetical "the flag was added upstream on
  2026-02-02, after this tag" (`SOURCES.md:120`) — no commit id, no line. **Gap.**
- Verified upstream today: the `commits?path=main.c` query returns commit
  `750a7c0d97bb01c1bdf126fd6bf5722da17e8998`, author date `2026-02-02T05:00:04Z`, committer
  date `2026-02-17T20:30:10Z`, subject "kill: option for triggering kernel oom killer"
  (7 words). `main.c` at that commit carries the option: longopts entry `:201`
  (`{ "kernel-oom", no_argument, NULL, LONG_OPT_USE_KERNEL_OOM },`), parse case and flag
  `:315-316`, startup line `:317` `"Using kernel OOM killer (requires Linux v5.17+)"`
  (7 words), help `:352` `"--kernel-oom … use kernel OOM killer via /proc/sysrq-trigger"`,
  threshold variant `:437-438`, poll-loop trigger `:553-554`. The entry's "since 2026-02-02"
  matches the **author** date; the commit reached master **2026-02-17** — the corrected text
  should carry both (see §5).

So the entry's body statements are true; the defect is the citation: one claim group (c-date)
rests on an unanchored parenthetical, and line 1 names URLs and a scope S117 does not have.

## 4. QUALITY 77–79 determination

- **#77** (`QUALITY.md:349-355`): "A correction sweeps every mention in place … the superseded
  wording is removed, not shadowed. A 'this section wins' banner or a general disclaimer is not
  a fix … a statement a critic named explicitly gets its own named correction row."
  → An appended-only correction block would leave the contradicted line-1 parenthetical
  standing, which #77 calls a defect. The fix is **in place** (line 1 is the only mention) plus
  a dated section carrying the critic's name (D2). House style precedent:
  `corpus/knowledge/system-pressure-r24.md:8-11`, `roster-truth-r12.md:27`.
- **#78** (`QUALITY.md:356-360`): not applicable — no counting command in this fix.
- **#79** (`QUALITY.md:361-364`): satisfied by the corrected parenthetical naming the refs it
  holds for (tags v1.7/v1.8/v1.9.0; master commit `750a7c0d`).
- **CORPUS.md Rules 2** (as stated in `round-26-verifier-spotcheck.md:186-187`; the rule text
  lives in the shokunin skill's protocol CORPUS.md, SOURCES.md section): a landed SOURCES row
  may change in place only in `status`, `recheck`, `used-by`. → S117's scope must **not** be
  widened in place; the kernel-oom history gets its own new row — exactly D2's second remedy
  ("align the entry's description with the row or open a new row for the kernel-oom history").

## 5. Exact correction text for the entry

### 5.1 Line 1 — replace the S117 parenthetical in place (same commit as §5.3)

Old (verbatim substring of line 1):

```
S117 (earlyoom tag history — https://github.com/rfjakob/earlyoom/releases and https://api.github.com/repos/rfjakob/earlyoom/commits?path=main.c — the v1.9.0 tag and commit, the v1.2 removal of the kernel-oom option and its 2026-02-02 re-introduction on master; opened 2026-10-22)
```

New:

```
S117 (earlyoom release and tag history with the logged-message grammar at tags v1.7, v1.8 and v1.9.0 — https://api.github.com/repos/rfjakob/earlyoom/tags and https://api.github.com/repos/rfjakob/earlyoom/releases — the v1.9.0 tag and commit and the stability of the logged-message prefixes across those tags; opened 2026-10-22); S127 (earlyoom kernel-oom option history — https://api.github.com/repos/rfjakob/earlyoom/commits?path=main.c and https://raw.githubusercontent.com/rfjakob/earlyoom/750a7c0d97bb01c1bdf126fd6bf5722da17e8998/main.c — the v1.2 removal of the kernel-oom option (S114, README.md:383) and its re-introduction on master, authored 2026-02-02, merged 2026-02-17; opened 2026-10-22)
```

(`S127` is the tentative id — the planner allocates; round-27 C1 opens S127+.)

### 5.2 F7 grounding touches (substance unchanged; same commit)

- F7 verdict line (entry:133-136): after "the absence of the option is verified on the tag's
  sources", append "(`main.c:245-246` at v1.9.0; the v1.2 removal is S114's README.md:383
  anchor; the option-history dates are S127's)" — and note that the "(§3.3)" pointer is fixed
  separately (§7).
- F7 Limit (entry:139): "since 2026-02-02" → "authored 2026-02-02 and merged 2026-02-17
  (S127, commit `750a7c0d`)".

### 5.3 Appended dated correction block (end of entry, after "Not claimed")

```markdown
## Correction 2026-10-22 (round-26 spot-check D2 — S117 citation)

The `source:` line described S117 as "earlyoom tag history" grounded on the HTML releases page
and a `commits?path=main.c` query, with a kernel-oom option-history scope. The landed row
(`corpus/SOURCES.md` S117) is the tags/releases API history row whose scope is the v1.9.0 tag
identity and the stability of the logged-message grammar across tags v1.7, v1.8 and v1.9.0; it
carries neither URL and no option-history scope. Corrected in place above. The kernel-oom
option history is now grounded by the new row S127 (commit `750a7c0d97bb01c1bdf126fd6bf5722da17e8998`:
authored 2026-02-02T05:00:04Z, merged 2026-02-17; `main.c` at that commit, lines 201, 315-317,
352), with the v1.2 removal anchored on S114 (`README.md:383`) as that row already records. No
body statement is retracted: F7's absence claim was verified on the v1.9.0 sources and the
installed binary, and the master-side claim was true but under-cited.
```

## 6. New SOURCES row — needed: yes

Why: (i) the 2026-02-02 date currently rests on S114's unanchored parenthetical — no located
quote, no commit id anywhere in the corpus; (ii) CORPUS.md Rules 2 (per D3,
`round-26-verifier-spotcheck.md:186-187`) forbids widening S114/S016/S117 in place; (iii) both
new URLs (the commits query; `main.c` at commit `750a7c0d`) are in no existing row, so this is
a new row, not an anchor — per the round-27 convention I say which: **new row**; the tag-side
facts stay on S114 (already landed) and S119's bytes.

Ready to paste (planner allocates the final id; tentative S127):

```
| S127 | earlyoom kernel-oom option history — https://api.github.com/repos/rfjakob/earlyoom/commits?path=main.c ; https://raw.githubusercontent.com/rfjakob/earlyoom/750a7c0d97bb01c1bdf126fd6bf5722da17e8998/main.c | code | A | when earlyoom removed and re-introduced the option to delegate kills to the kernel OOM killer: the v0.6 introduction and v1.2 removal with compatibility-ignore (S114 README.md:416,383; v1.9.0 main.c:245-246), and the master re-introduction commit with its author and merge dates; not the option's runtime behaviour on any host, not the v1.7-v1.9.0 log grammar (S117) | commits query: 750a7c0d97bb01c1bdf126fd6bf5722da17e8998, author date 2026-02-02T05:00:04Z, committer date 2026-02-17T20:30:10Z, subject "kill: option for triggering kernel oom killer" (first page of 100, 2018-07-16 to 2026-10-15); main.c at that commit: 201 (longopts "kernel-oom"), 315-317 (case; flag; "Using kernel OOM killer (requires Linux v5.17+)"), 352 (help "use kernel OOM killer via /proc/sysrq-trigger"), 437-438 (threshold line variant), 553-554 (poll-loop trigger); main.c@750a7c0d sha256 d24a26c97744458706a870ee3eb1ddcd5e5f05dda11fe22a71d6a4952028df3e, 585 lines; opened 2026-10-22 | The kernel-OOM delegation option left earlyoom in v1.2 and returned on master in February 2026, so a 1.9.0 binary prints "Option -k is ignored since earlyoom v1.2" while current master grows a --kernel-oom long option (S016 documents it from the master README); delegation claims must name the build they hold for. | mined | 2026-10-22 | on-release | corpus/knowledge/userspace-oom-killers-r26.md, corpus/knowledge/oom-victim-selection-r27.md |
```

Gate block (located quotes; each ≤25 words, verbatim):

- `commits?path=main.c` entry (JSON fields — unlocated by nature; the located counterpart
  follows): commit `750a7c0d97bb01c1bdf126fd6bf5722da17e8998`; `.commit.author.date`
  `2026-02-02T05:00:04Z`; `.commit.committer.date` `2026-02-17T20:30:10Z`; subject
  "kill: option for triggering kernel oom killer".
- `main.c` at `750a7c0d`, line 201: `{ "kernel-oom", no_argument, NULL, LONG_OPT_USE_KERNEL_OOM },`
- `main.c` at `750a7c0d`, line 317: `"Using kernel OOM killer (requires Linux v5.17+)\n"`
- `main.c` at `750a7c0d`, line 352: `"  --kernel-oom              use kernel OOM killer via /proc/sysrq-trigger\n"`
- Byte identity: sha256 `d24a26c97744458706a870ee3eb1ddcd5e5f05dda11fe22a71d6a4952028df3e`
  (585 lines), fetched 2026-10-22.

Note for the entry wording: "since 2026-02-02" is the **author** date; the commit reached
master 2026-02-17 (committer date). §5.2 carries both.

## 7. Adjacent findings (outside D2; for the planner, not fixed here)

- **Dangling § references.** The landed entry cites §3.1, §3.2, §3.3 (entry:41-42,74,107,118,136,180)
  and §4.2 (entry:252), but it contains no §3 or §4 — its only sections are Scope, Facts,
  Decision table, Limits, "What it changes for mori", Adjacency, "Not claimed"
  (headers at entry:8,26,186,204,232,254,269). Those sections exist only in the scribe draft
  `.ufo/waves/round-26/w1/DraftEntryR26.md:316-591`. Moreover F7's "(§3.3)" is wrong even
  against the draft: the draft's installed-binary evidence is §3.4 (`DraftEntryR26.md:404`);
  §3.3 is the round-26 tool (`:394`).
- **S117 evidence-cell noise (informational).** S117's evidence column lists a `msg.c` sha256
  (`a771c915…5197`) although `msg.c` is not among the row's URLs — it is S118's file
  (`SOURCES.md:123` vs `:124`).

## 8. Residual risk and verification gaps

- sha256s of API JSON responses are fetch receipts, not stable content (reaction counts
  change; the commits list is a paginated first page of 100, spanning author dates
  2018-07-16T07:04:01Z to 2026-10-15T17:28:19Z). The drafted row therefore anchors on the
  pinned-commit file lines and ids, not on a JSON hash.
- I did not re-open the row's `tags` or releases-**list** endpoints; their recorded values are
  corroborated indirectly (single-release endpoint's `published_at` matches S117's evidence
  cell; the tag→commit mapping matches S114's recorded commit, and the fetched v1.9.0 files are
  byte-identical to the hashes recorded in S114/S117/S119/entry line 1).
- The HTML releases page named by the entry (divergence #1) was not fetched — the divergence is
  documentary (URL not in any row), so fetching it could not change the finding.
- I did not verify that the v1.2-removal commit itself appears in the commits list page; the
  v1.2 removal is grounded on S114's README anchor, which is sufficient for the entry's claim.
