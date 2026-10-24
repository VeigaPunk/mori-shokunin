# ReviewProvinceFix — wave-2 falsify (round 30) — routed R7 fix `58b61681..af42101d` (PROVINCE.md, SKILL.md)

**Verdict: agree — the routed R7 fix holds.** All nine substituted statements re-derive as true
against observed state at fleet rev `63729047`; the "no line moved" claim is byte-verified
(9 equal-count hunks + one terminal 16-line append; PROVINCE.md unchanged to measured tip
`ad0f0474`; the post-fix SKILL.md insertions sit at :743-755 and shift neither `:374-393` nor
`:661`); every line-number citation in the appended correction block resolves at `af42101d`;
no leftover *stale-as-claimed text* remains (grep at `af42101d`: zero hits for "pending
admission"/"admission pending" in both files). Two minor residuals found, one inside the fix's
own wording, one disclosed-but-numbered-off; neither breaks the fix.

## What the fix is

Range `58b61681..af42101d` contains six round-30 commits; only `af42101d` ("round-30: routed
R7 — PROVINCE stale statements fixed by same-line substitution plus appended correction block;
SKILL.md:661 citation qualified") touches PROVINCE.md/SKILL.md (git log run). `af42101d` is an
ancestor of measured tip `ad0f0474` (merge-base --is-ancestor exit 0). R7 source finding
(`corpus/lessons/round-29-verifier-spotcheck.md:166`): "PROVINCE stale in five places
(`w1/ScoutShonen.md`); `SKILL.md:661` unqualified citation."

## 1. Every substitution true against observed state

MANIFEST at `63729047` (jq filter over `git show 63729047:MANIFEST.json`), all
 closures are `lane=="mori"`, type `closure`, with the same non-author reviewer string
 ("hyaku-closure … non-author"):

| Round | `admitted` | verdict | Fix statement verified |
|---|---|---|---|
| 16 | true | admitted | PROVINCE `:25` "admitted round 16" |
| 24 | true | admitted | PROVINCE `:236`, `:283` |
| 25 | true | admitted | PROVINCE `:294`, `:353-354` |
| 26 | true | admitted | PROVINCE `:359` |
| 27 | false | rejected-honest-stop | PROVINCE `:375` "round 27 closed `rejected-honest-stop`, so this advance is not admitted" |

(Separately measured at the same rev: round 28 admitted, round 29 rejected-honest-stop — the
fix's frame "round 29 closed `rejected-honest-stop`" stands, with round 28 admitted; the per-
round probe summary in the fix section above is engineered to be generous.)

Other substituted statements, re-derived from committed bytes / observed tree:

- **`:66` tsukuroi range** — old cite `../tsukuroi-shokunin/PROVINCE.md:21-24,35-44`: `:20-23`
  are the Arch News/pacnew/initramfs/snapper surface-table rows and `:35` is `## Adjacent —
  finding-to-owner handoffs` (awk: line content printed for 8, 9, 14, 20, 23, 35). New range
  `:8-14` holds "**Owns (surfaces, all read-only probes):** pacman state … what
  pins/holds exist." Substitution true; the old cite was wrong.
- **`:68` kagi cite** — old `SKILL.md:49` carries r15 alarm prose ("The r15 repair is
  deliberately narrow…" — awk), dead for a credential rule. New `SKILL.md:374-393` = `##
  Secret-exposure exclusions (measured by a sentinel audit)` through the …`keeps `MESSAGE``.
  bullet (awk lines 374, 391-393 at `af42101d`). True; old cite dead.
- **`:47`, `:90`, `:94` path prefix** — `../fleet-ledger/.ufo/waves/kaika-w1/…` → `../.ufo/…`.
  `fleet-ledger` absent on disk at the fleet root; 0 commits in full fleet history touch the
  path (`git log --all --oneline -- fleet-ledger` → 0). Target files exist at fleet root:
  `.ufo/waves/kaika-w1/mori-state.md` blob `4494d7cb…` and `mori-art.md` blob `d5b5e2ea…` at
  `63729047` (git ls-tree), present in the working tree. The appended block's "the
  `../fleet-ledger/` prefix never existed" is consistent with 0 hits in ALL fleet history.
- **`:25`, `:47`, `:90`, `:94` line-anchor retention** — re-read after substitution:
  `mori-state.md:31` prints the driver-counter row (".ufo/state/mori.round = 2 … 9 behind"), 
  `:180` holds the `ls /scratch` → absent fragment, `:190` opens the C15 counter/MANIFEST row
  (awk contents seen). `mori-art.md:91` opens the SOURCES table header with `|id|source|…`,
  and :92-112 hold S001–S030 continuous (read 88-112; S030 at :112; read of 113-130 not needed
  to prove 91-124 covers S001–S030).
- **`:283`** — the old text said the row was "pending admission"; substituted to "was
  **admitted** by the round-24 non-author closure" (git diff). Consistent with round-24
  closure `admitted: true` at the same rev (above). Same for `:353-354` (round 25).
- **`:375` wording** — old label said "admission pending" for round-27 knowledge;
  substituted to "round 27 closed `rejected-honest-stop`, so this advance is not admitted",
  matching the round-27 mori closure at 63729047 (`admitted: false`, verdict
  "rejected-honest-stop", `corpus/lessons/round-27-verifier-spotcheck.md:77` cited by
  DraftProvinceR7). Substitution direction true (round 27 was CLOSED and rejected, so
  "admission pending" was false in a different direction; both are now truthful).

## 2. Did any line move? — No (byte-verified)

- Stat: PROVINCE.md 29+/13−, SKILL.md 1+/1−. All nine PROVINCE hunks are equal-count
  substitutions (1/1 ×6, 2/2 ×2, 3/3 ×1 covering `:350-362` with changed lines
  `353, 354, 359`); the tenth hunk `@@ -382,3 +382,19 @@` appends 16 lines after the last
  content line `:384` (old lines 382-384 kept as trailing context). No pre-existing line
  number changes: every cited number (`22-28`, `25`, `44-57`, `47`, `66`, `68`, `90`, `94`,
  `103`, `108`, `125`, `132`, `134`, `145`, `236`, `283`, `294`, `321`, `353`, `354`, `359`,
  `375`) holds at `af42101d` (awk extraction — every hit is the claimed content; e.g. :236
  "Core, one-shot system pressure reading (…admitted round 24)", :321 "FR15 — Harness
  background-job capacity runway", :375 round-27 rejected-honest-stop line).
- Appended block is the LAST section (`:386-400`), so it cannot shift any earlier line.
- **Living-document citations into PROVINCE unaffected:** the grep sweep at `af42101d`
  (excluding wave-report history) found SKILL.md `:128, :345-346, :617, :635, :665-667, :682`
  and `corpus/README.md:455,495` citing PROVINCE `:12-18, :44-57, :51, :53, :55, :65` — all
  outside the twelve substituted lines; corpus/knowledge scope-headers (lane-silence-r2.md,
  observability-surfaces-r2.md, progressing-weak-r2.md, surfaces-r7.md, surfaces-r8.md) cite
  `:16-18`, `:9-10`, `:9`, `:9` — also out of the changed set. Validity holds. (Approx-100
  historical wave-provenance citations — e.g. `.ufo/waves/round-*/**` and LOG/SCORECARD
  entries — remain valid per line-number invariance, and were not otherwise corrected by this
  fix; DraftProvinceR7 Fix #6 was scoped to substituted content only.)
- **`PROVINCE.md` unchanged to measured tip:** `git diff --stat af42101d ad0f0474 --
  PROVINCE.md` → empty.

## 3. Anything still stale that the round claims fixed?

- **Claimed-fixed set is fully landed:** `git grep` at `af42101d` (PROVINCE.md SKILL.md) for
  "pending admission" / "admission pending" / "verification pending" → exactly ONE hit,
  `PROVINCE.md:98-99`, which is not stale text but the round-17 supersession ROW that
  documents the just-executed supersession ("Supersedes 'verification pending' in the
  same-boot window Core … spotcheck.md:9–17 admitted …"). It describes the old row in the
  past-tense sense the fix intended and must not be itself "corrected" (that would erase the
  record). Same grep at the current tip returns only this single hit too (`:98`).
- **Surviving terminology metavariable (disclosed, arguably mis-numbered, real):** the
  appended block's last line claims "the census citation `tools/mori-census.sh:211-212,282`
  at `:94` has drifted (the default now sits near `:237`, `:321`; **ScoutProvinceStale item
  8**)" — but ScoutProvinceStale's actual finding headers run F1–F9 and the census-drift
  finding is **F7** (`ScoutProvinceStale.md:156-159`); the append block pointer is off by
  two. (DraftProvinceR7 fix-list runs F1–F10, still not 8.) LOW severity, evidence-pointer
  nit; the underlying observation is real (re-derived here: `tools/mori-census.sh` at
  `af42101d`: `:237` holds `MORI_DISK_TARGETS … (default: ROOT /tmp)` in a comment block,
  `:321` holds `DISK_TARGETS=${MORI_DISK_TARGETS:-"$ROOT /tmp"}`; the cited `:211-212,282`
  hold `# Live mode writes nothing…` / `SELF=$(readlink…`).
- **`corpus/README.md:337` still carries the same `../../fleet-ledger/` unresolvable FR4
  pointer** (grep at af42101d) — same defect class as the `:47/:90/:94` fix (round-16
  ReviewCorpus/round-17 ReportTrace F4 precedent), outside the routed R7 file-pair scope but
  contradicting the appended block's fleet-root-truthing while leaving a sibling perpetuation
  of the dead prefix within the lane's own corpus index. MEDIUM-LOW, residual staleness the
  lane records elsewhere (round-17 ReportTrace) but did not sweep here.
- **`:288` tsukuroi/kumitate/kama/souji boundary rows**: unchanged content; DraftProvinceR7
  "Checked and not defects" already resolves their targets, and this review adds: `PROVINCE
  (tsukuroi) :32-33` "fleet correlation belongs to mori" (read at sibling working tree along
  with :35-44 to disconfirm 21-24,35-44 as an "owns" range), no contradiction found with the
  new `:8-14` range.

## 4. Independent SCOUT-based note (packet features)

The team's shared tracker put the `.ufo/waves/round-30/w1/*` packet-pointer questions on me;
independent derivation at `af42101d`:

- `.ufo/waves/round-30/w1/DraftProvinceR7.md` = sha256 prefix `7442274eba4a` at `af42101d`.
- `.ufo/waves/round-30/w1/ScoutProvinceStale.md` = sha256 prefix `06a09015ee68` at
  `af42101d`.

These are the two evidence files the appended block cites; both are land-committed at the fix
rev with the identities the block implicitly asserted. (Recap: fixed set is true; line map
holds; stale-as-claimed text is not what stays stale — the two LOW-class residuals above are.)
[INFERENCE] — L1's after-receipt `c1-after.txt` was not read: out of scope for this seat's
routing; directly-measured evidence above suffices. Tooling: no installs (no need arose), so
nothing to disclose under the 2026-10-19 operator directive. Privacy/scope: no settings, unit
names, uids/pids, host command lines, journal MESSAGE text, or MCP/systemd state touched;
fleet MANIFEST values used only. All git runs read-only in the lane (/fast/scratch/hyaku/
mori-r30-w2/ReviewProvinceFix/ scratch only).
