# Mo56ScribeRows — S544/S545 registry audit (round 56, w1)

Measured revision: `8be2717b0809281d07dffe83dad424a4859e0747` (freeze tip), lane
`/home/vgpnk/Projects/shokunin/mori-shokunin`. Working tree verified equal to the freeze for the
audited file: `git diff --stat 8be2717b HEAD -- corpus/SOURCES.md` prints nothing and
`git status --porcelain -- corpus/SOURCES.md` prints nothing.
Fleet repo measured at `/home/vgpnk/Projects/shokunin` HEAD `666bc1efcddd4b711173f23def3278cfe54a418f`
(the two writer scripts last changed in `5f4fa8d85ec3041320c947717bbc38854cb6cc93`, 2026-10-25).
Scratch: `/fast/scratch/hyaku/mori-r56/Mo56ScribeRows/` (removed at the end; nothing cited here
lives only there).

Audited rows (extracted with `git show 8be2717b:corpus/SOURCES.md`, 391 lines, sha256
`6cf5c51592e8b8e69d50a46d2ff8bfcc9f32873c4e25d10e565c615d60dd7686`):

- line 324, `S544`, row sha256 `f644a49383afa41ce91ee2e3dd7d6c4fda53ff526c7feffe904f590cd360e624`
- line 325, `S545`, row sha256 `00ce2ad94fa42374449d76879809f7d5bee8ad377f5706c201bb592b2d59d768`

## Shape checks

| check | command | output | exit |
|---|---|---|---|
| 11 columns each | `awk -F'\|' 'NR==324\|\|NR==325{print NR, NF}'` | `324 13`, `325 13` | 0 |
| whole registry column shape | `awk -F'\|' '/^\| S[0-9]{3} \|/ && NF!=13'` | `bad_rows=0` | 0 |
| no literal/escaped pipe in the two cells | `sed -n '324,325p' \| grep -c '\\\\\|'` | `0` | 0 |
| no alternate pipe glyphs | `grep -c '&#124;\|｜'` | `0` | 0 |
| ids continue the registry | entering tip `5b295eee` tail: `S541 S542 S543`, 316 rows; freeze: 318 rows, tail `S544 S545`; duplicate ids: none; max id 545 | appended, no gap added at the tail | 0 |
| used-by paths exist at R | `git cat-file -e 8be2717b:<path>` for all four named paths | all `EXISTS` (`corpus/knowledge/driver-liveness-r56.md`, `tools/mori-driver-liveness.py`, `corpus/knowledge/vote-binding-r56.md`, `tools/mori-vote-bind.py`) | 0 |
| opened = 2026-10-27 | cells `[10]` of both rows | `2026-10-27`, `2026-10-27` (today's date, not future) | — |
| recheck valid | cells `[11]`: `on-release`, `on-release`; fleet validator rule E09 accepts symbolic cadences | see validator below | 0 |
| status honest | cells `[9]`: `mined`, `mined`; both entries exist and name the row (`driver-liveness-r56.md:3` "source: S544", `vote-binding-r56.md:3` "source: S545") | — | 0 |
| append-only since data commit | rows at `c419fe6d`, `6ced9da9`, `3f494b49`, `8be2717b` | identical bytes at all four (`f644a493…`, `00ce2ad9…`) | 0 |
| registry validator | `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` | `mori\tok\t/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`; no `E01–E12`; no `W01–W04` on S544/S545 | 0 |

The 227 numeric gaps below S236 are pre-existing (the entering tip already had 316 rows with max
`S543`); this round adds the two highest ids and introduces no gap or duplicate.

## Anchor verification

S544 anchor cell `[7]`:
`inline.sh launch 149, complete 176, dead 182; shokunin-watchdog.sh launch 266, complete 405, dead 448; extract corpus/evidence/sources-r56/watchdog-log-grammar.txt, sha256 38ba3e6b309e17d3d8038e8986e274bb363ac893d1c325fe145a95882a417796`

- `git show 8be2717b:corpus/evidence/sources-r56/watchdog-log-grammar.txt | sha256sum` →
  `38ba3e6b309e17d3d8038e8986e274bb363ac893d1c325fe145a95882a417796`, matching the cell.
- Extract has exactly 6 lines; each is byte-identical to the cited fleet line (Python compare,
  `a == e` for all six): `scripts/hyaku/inline.sh` 149/176/182, `scripts/shokunin-watchdog.sh`
  266/405/448 → `OK` ×6, `ext_lines=6`, exit 0.
- The extract therefore pins the *six cited shapes* only.

S545 anchor cell `[7]`:
`section 1 line 251, section 2 grammar lines 308 and 461; sha256 61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7; copy corpus/evidence/sources-r56/rfc8259.txt`

- Copy sha256 matches the cell; `curl -fsSL https://www.rfc-editor.org/rfc/rfc8259.txt` (28,360 B)
  hashes to the same value and `cmp` reports byte-identical → `COPY_IDENTICAL`.
- Copy line 251 is `A JSON text is a serialized value.  Note that certain previous` — the quoted
  sentence. Line 308 is `value = false / null / true / object / array / number / string`. Line 461
  is `string = quotation-mark *char quotation-mark`. All three lines locate their text.

## Tier question — is own-work tier A defensible for S544?

For: the source is the writers themselves, i.e. the authoritative definition of what the log can
contain; the lane's own `sources-census.sh` header carries only one tier rule ("community is never
tier A"), which S544 does not touch; every `own-work` row already in the registry is tier A
(S034, S102, S474, S477, S488 — 6/6 including S544), and the same post-review precedent (round 12,
S034) admitted an own-work receipt as "tier A for the observed … union only". The quoted bytes are
pinned by a sha256 in the row itself, so a reader reproduces the claim without trusting the lane.

Against: own-work provenance makes the row self-certifying — rows, tool and entry were authored in
the same wave by the same lane, so "mined" is satisfied by construction and nothing independent
corroborates the grammar. Tier A read as "independently authoritative" would be inflation. The
pinned extract covers only six cited lines: the entry's remaining launch variants (`steer`,
`ufo-fsd`, `runId=`, `slot=`, `mission=`) and the `launch-fail`/`wrap` shapes come from the live log
or from un-cited writer lines (see D2), so the row's authority is narrower than the entry's
heading ("The frozen grammar (S544)") suggests.

Ruling recorded here: defensible under house convention (A = primary/byte-pinned, not independent),
with the named limit that the row cannot corroborate itself and does not cover the observed
variants. No cell change recommended on this ground alone; the limit belongs in the entry prose.

## Comparison with the round-55 Gate table format

`corpus/lessons/round-55.md` `## Gate` rows are `| id | URL (+ copy path:line) | accessed | ≤25-word
located quote | decision |`, i.e. URL + committed copy + exact line + verbatim quote + admit/reject.
The registry rows S544/S545 are the 11-column registry format, which has no quote or decision
column; their equivalent is anchor (line locators + sha256 of the committed extract) plus status.
S545 matches the Gate convention closely (URL, copy path, sha256, three line locators). S544 is
weaker: no URL and no fleet-revision/sha256 for the two writer files (D3), and its anchor locates
only the three shapes per writer while the teaches cell also names `wrap` (D2). Gate rows also
carry the quote text inline; S544 delegates to the sha-pinned extract, which the registry format
allows but which leaves the `wrap` claim unquoted and unpinned.

## Defects (exact cells)

D1 — MED — S545 anchor cell `[7]`, text `section 1 line 251, section 2 grammar lines 308 and 461; …`.
Line 251 is not in section 1: section header `2.  JSON Grammar` is copy line 246 and section header
`1.  Introduction` is line 147. Lines 308 and 461 are not section 2 either — 308 is under
`3.  Values` (line 296) and 461 under `7.  Strings` (line 424); "the section-2 grammar's
productions" would be true, "section 2 … lines" is not. The same mislabel is repeated in the entry
(`corpus/knowledge/vote-binding-r56.md:31`, "S545 §1, line 251"; `:32-33`, "§2 grammar, line 308" /
"§2, line 461"). The line numbers themselves are right, so no claim is orphaned; the section
attribution is wrong. Fix route: QUALITY 81/102 make the anchor first-published, so a registry
correction note (append-only, like the round-15 note in SOURCES.md) or a supersede row — not an
in-place edit; the entry's section labels are data the L1 may correct.

D2 — MED — S544 row: teaches cell `[8]` says "The writer source per launch/complete/dead/wrap line
shape; the probe grammar is frozen from it", but anchor cell `[7]` locates no `wrap` line and the
pinned extract holds exactly six lines with none of them a wrap. The only wrap locator in the round
is `corpus/knowledge/driver-liveness-r56.md:40` → `S544 shokunin-watchdog.sh:398` (verified: fleet
line 398 is `log "wrap $lane round=$n landed; NOT respawning (fleet-wrap)"`). Likewise the
`launch-fail` shape the tool reads is located only in the entry (`:41`, 241-249), not in the row.
This is the round-55 F3 class (anchor claims less than the cell asserts). Fix route: correction
note adding `shokunin-watchdog.sh:398` (and 241-249 if the shape is kept in the row's authority).

D3 — LOW — S544 source cell `[3]`, "scripts/hyaku/inline.sh and scripts/shokunin-watchdog.sh in the
fleet repo". No fleet commit id and no writer-file sha256; the line locators were verified only
against fleet `666bc1ef` (scripts last written in `5f4fa8d8`, 2026-10-25). The row's only pinned
bytes are the 6 extract lines. Precedent S034 pins a script SHA-256 and a run stamp; adding the fleet
revision (or a writer sha256) would make the row as checkable as the Gate convention. Named limit,
not a mechanical failure (`validate` clean).

D4 — LOW — S545 anchor paraphrases rather than quotes: cell says "a JSON text is one serialized
value" where copy line 251 reads "A JSON text is a serialized value." and "a string is
quotation-mark *char quotation-mark" where copy line 461 reads
"string = quotation-mark *char quotation-mark". Line locators are correct, but a grep for the cell
text fails; the Gate rows (round-55) carry verbatim ≤25-word quotes.

D5 — LOW — S544 scope cell `[6]` confines the source to "the .ufo/watchdog.log line grammar under
the hyaku-inline and legacy daemon drivers", which is honest for the two cited writers, but the
entry heading "The frozen grammar (S544)" (`driver-liveness-r56.md:29`) also presents steered and
ufo-fsd variants that those writers do not emit. The row cell is defensible; the entry's heading
attributes more to S544 than the row's scope.

D6 — LOW — S545 teaches cell `[8]`, "A JSON-wrapped vote binds as a string scalar whose stripped
content is the anchored vote line, not as a substring", is the binder's design rule, not a sentence
of RFC 8259; it is an inference from §2 line 251 (a JSON text is one serialized value). The
round-55 F7 "templated teaches cells" disposition recorded this class as non-mechanical.

D7 — observation, no action — both used-by cells name tool files that never mention their source id
(`grep S544 tools/mori-driver-liveness.py` → empty; `grep S545 tools/mori-vote-bind.py` → empty).
Precedent S191–S193 also name tool-only consumers, so this matches house convention and the
validator's E11 is satisfied.

## UNVERIFIED / out of scope

- I did not re-run the C1/C2 counters, the probe on the live log, or the 1728-line/0-malformed
  measurement; those are other seats' claims.
- I did not fetch the writers at a historical fleet revision; the locators were checked only at
  fleet `666bc1ef`, which is the only revision the row could be checked against because it pins none.
- The registry validator was run against the lane working tree, which `git diff` shows equal to
  `8be2717b` for `corpus/SOURCES.md`.
- No tool was installed or upgraded; no `pacman` call was made.

## Findings

- **MED** — `corpus/SOURCES.md` S544 row (freeze line 324), teaches cell `[8]` names a `wrap` line
  shape, but anchor cell `[7]` and the sha-pinned extract (`corpus/evidence/sources-r56/watchdog-log-grammar.txt`,
  6 lines) locate no `wrap`; the sole locator is `corpus/knowledge/driver-liveness-r56.md:40` →
  `scripts/shokunin-watchdog.sh:398`. (D2)
- **MED** — `corpus/SOURCES.md` S545 row (freeze line 325), anchor cell `[7]` "section 1 line 251,
  section 2 grammar lines 308 and 461": line 251 is in `2.  JSON Grammar` (header line 246), 308 is
  in `3.  Values` (line 296) and 461 in `7.  Strings` (line 424); mislabel repeated in
  `corpus/knowledge/vote-binding-r56.md:31-33`. (D1)
- **LOW** — `corpus/SOURCES.md` S544 source cell `[3]` names two mutable fleet-repo scripts with no
  commit id or file sha256; locators verified only at fleet `666bc1ef` (last write
  `5f4fa8d8`). (D3)
- **LOW** — `corpus/SOURCES.md` S545 anchor cell `[7]` text is a paraphrase, not a verbatim
  substring of copy lines 251/461. (D4)
- **LOW** — `corpus/SOURCES.md` S544 scope cell `[6]` is honest for the two writers, while
  `corpus/knowledge/driver-liveness-r56.md:29` presents other writers' variants under "The frozen
  grammar (S544)". (D5)
- **LOW** — `corpus/SOURCES.md` S545 teaches cell `[8]` states a binder rule, not an RFC sentence;
  an inference from line 251. (D6)
- **PASS** — 11 columns (NF=13), no pipe/escape corruption, ids continue (`S543` → `S544`/`S545`,
  no duplicates or new gaps), `opened=2026-10-27`, `recheck=on-release` accepted by the validator,
  `status=mined` backed by entries that name each row, all four used-by paths exist, rows unchanged
  from the data commit, extract and RFC copy hashes match, fleet validator exits 0.
