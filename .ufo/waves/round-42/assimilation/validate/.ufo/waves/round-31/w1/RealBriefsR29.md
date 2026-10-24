# RealBriefsR29 — the files-opened hit set a rule-faithful gate must report on the eight real round-29 briefs

Seat `MoriR31.RealBriefsR29` (leaf, round 31 wave 1). Question: by hand, from `.ufo/waves/round-31/rule-text.md`
alone, what is the exact expected `(line, rule)` hit set for `tools/mori-blind-check.sh <rev>
.ufo/waves/round-29/w1 '^CaseA2(07|10)[a-d]\.md$' <allow>` on the eight real round-29 writer briefs? No gate ran:
the tool is absent at HEAD `1d94055d` (`git cat-file -e HEAD:tools/mori-blind-check.sh` → `does not exist`); the
bytes came from `d6d5cb0a` via `git show`, and only read-only git and text inspection ran.

| brief | blob at d6d5cb0a | sha256 of bytes read | lines |
|---|---|---|---|
| CaseA207a | `ece1c7354a20c3efed45eb6901a2a0d977e5f139` | `6ac883d4db539465d4eeffa4843d52d86d850d5b54292a110c64bb0d45fecbbb` | 215 |
| CaseA207b | `a3bac0ac05e2bda6b132f05a6c134347842f1059` | `7f87f65481a6a77d25854d18e999eac7fa96e1afa3551b97c7801e507d5011f3` | 209 |
| CaseA207c | `66cc803a11efee7403f28acdf4bbc9e9ec485c3c` | `0fe85d0b2ce857cd954c6831ec907043590651ec47794760512f87f88a505a0a` | 210 |
| CaseA207d | `7d49792e59d74da44fac043dedad4ca010f3bb81` | `1c09bde25c198f811b4432321a2fc9d20cdcdae40f2bfa82eb9cf7872edbfbfd` | 220 |
| CaseA210a | `35fe92145513f04c93839f9b2406acf0166973f8` | `57e1e62cb81f91704ff9186d8467bf5781816618592af3b4b86340234ce47ddd` | 216 |
| CaseA210b | `6d5a2555289e4b604a7306287484641680ed44d3` | `70fc85f0e7d5b207777810e9edbc3817b11dd3260120f1a34bd290296e2d592a` | 211 |
| CaseA210c | `ce561289af4e51f99d53f23ce57fc90e12cca2c1` | `b018d2cccbf5b114161b311452dd91b21e271c4c16cecbb86a91578516c2f7f2` | 206 |
| CaseA210d | `645df6bd7c520f0c9d34bc8bd6f039bc4806aebf` | `df5c3bdc9d37fe30b4c442cd94b1fc538473473425355bcfeb9edd5812e0ebca` | 191 |

Allow list applied (five lines; `{report}` = brief basename without `.md`): `.ufo/waves/round-29/rule-text.md`;
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-29/rule-text.md`;
`/fast/scratch/hyaku/mori-r29/{report}`; `/fast/scratch/hyaku/mori-r29/*`;
`https://raw.githubusercontent.com/rfjakob/earlyoom/*`.

Both rule-text lines are inert: `.ufo/waves/round-29/rule-text.md` exists at neither `d6d5cb0a` (`git ls-tree -r
--name-only d6d5cb0a .ufo/waves/round-29/` lists no such path) nor HEAD (`| grep -c rule-text` → `0`), and
`round-29/wave1-spec.json` never names it; no entry below names it either. Every contract, fixture, `SKILL.md` and
`RULES.md` hit is forbidden by this allow list alone — round 29 permitted those reads
(`round-29/w2/AdjudicateBlindHits.md:64-65`).

## Two points the text does not decide, and the fixtures do not pin

**A. Rule 1's phrase (`rule-text.md:10-12`).** Adjacent substrings do not match `## Files and URLs opened`
(`CaseA207b.md:195`, `CaseA207c.md:192`, `CaseA210b.md:195`). The round-30 gate reads it as word order with any
gap — `files.*opened || opened.*files` (`round-30/check-blind-wave.sh:115`) — and expects forbidden-path, not
missing-list, reports for those three (`:172-178`); their `:1` lines are among the 20 adjudicated round-29 false
positives that must not reappear (`:179-185`; `round-30/contract.md:170-172`). The adjacent reading re-emits three.

**B. Rule 3's closing (`rule-text.md:16`).** With rule 2 skipping only blank lines, lead-in prose or a sub-heading
ends the block before the first entry: `CaseA207a.md:194` (`Local files requested:`), `CaseA207b.md:197` (`Local
files: …`), `CaseA207d.md:196` (`### Lane files`). Each then has zero entries, and rule 5 (`rule-text.md:21`) makes
it a `:1` missing-list hit — three more adjudicated false positives. Skipping lead-in prose clears the first two;
only "close at a heading of the same or higher level than the opener" clears 207d.

**C. Rule 4's quantifier is immaterial here.** Every entry below either has all candidates allowed or at least one
unmatched, so the existential and universal readings give identical rows (F02/F13 in `c2-fixtures.json` assume the
existential one).

Variants, each passing all 16 fixtures: **V1** adjacent phrase + literal close; **V2** word-order phrase + literal
close; **V3** V2 + lead-in prose skipped before the first entry; **V4** V3 + close only at a heading of the same or
higher level (the minimal repair). Verdicts: `A` an allow line matches, `F` at least one candidate unmatched, `N` no
candidate (rule 4 makes N a hit).

## Per brief

**CaseA207a** (215 lines). Opener `192 ## Opened files and URLs`. V1-V3 close at `194 Local files requested:` → 0
entries; V4 skips it and closes at `203 External sources fetched …`.
- `196 F` — `skill://godspeed`; `/home/vgpnk/.agents/skills/godspeed/SKILL.md`
- `197 F` — `/home/…/.ufo/waves/round-27/contract.md` (`:40-80` stripped)
- `198 F` — `/home/…/.ufo/waves/round-26/contract.md` (`:1-190`)
- `199 F` — `/home/…/tools/fixtures/mori-oom-killers/cases.json`; `cases-a2.json`
- `200 A` — `/fast/scratch/hyaku/mori-r29/CaseA207a/cases.json`
- `201 A` — `/fast/scratch/hyaku/mori-r29/CaseA207a/sources/`

V1-V3: `1:writer-missing-files-opened-list`. V4: `196,197,198,199:writer-forbidden-opened-path`. Table `205-211` is
in no block (prose 203 closes it); a read-past-the-list gate (`check-blind-wave.sh:127`) would add 207 (`main.c`),
208 (`kill.c`), 211 (freedesktop URL).

**CaseA207b** (209 lines). Opener `195 ## Files and URLs opened` (V2-V4 only). V1/V2 close at `197 Local files: …` →
0 entries; V3/V4 skip 197 and `199 Fetched with curl …`, close at `207 Validation: …`.
- `201 F` — URL `…/v1.9.0/main.c` A; `main.c:161`→`main.c`, `main.c:295`→`main.c`
- `202 F` — URL A; `kill.c:318`→`kill.c`, `kill.c:627`→`kill.c`
- `203 A` — URL `…/msg.h`, nothing else
- `204 F` — URL A; `MANPAGE.md:206`→`MANPAGE.md`
- `205 F` — `https://raw.githubusercontent.com/systemd/systemd/…`; `systemd.journal-fields.xml`

V1/V2: `1:writer-missing-files-opened-list`. V3/V4: `201,202,204,205:writer-forbidden-opened-path`.

**CaseA207c** (210 lines). Opener `192 ## Files and URLs opened` (V2-V4); every opening variant closes at `200
Fetched source evidence …`.
- `194 F` — `…/skills/godspeed/SKILL.md`; `/home/vgpnk/.omp/agent/RULES.md`
- `195 F` — `/home/…/.ufo/waves/round-27/contract.md`
- `196 F` — `/home/…/.ufo/waves/round-26/contract.md` (`:78-190`)
- `197 F` — `/home/…/cases.json`; `cases-a2.json`
- `198 F` — scratch A; `kill.c`, `msg.h`, `MANPAGE.md`, `systemd.journal-fields.html`

V1: `1:writer-missing-files-opened-list`. V2-V4: `194,195,196,197,198:writer-forbidden-opened-path`. Table `202-208`
is outside the block.

**CaseA207d** (220 lines). Opener `194 ## Opened files and source evidence`. `196 ### Lane files` is a heading, so
V1-V3 close with 0 entries; `206 ### Upstream sources fetched with curl` is not an opener. V4 keeps the deeper
heading open and closes at `204 **Scope deviation:** …`.
- `198 F` — `/home/…/.ufo/waves/round-27/contract.md`
- `199 F` — `/home/…/.ufo/waves/round-26/contract.md`
- `200 F` — `/home/…/cases.json`
- `201 F` — `/home/…/cases-a2.json`
- `202 A` — `/fast/scratch/hyaku/mori-r29/CaseA207d/cases.json`

V1-V3: `1:writer-missing-files-opened-list`. V4: `198,199,200,201:writer-forbidden-opened-path`. Items `208-214`
stay outside every block; without prose closing, 211 (`journalctl.html`), 212 (`journalctl.xml`) and 214
(`systemd.journal-fields.xml`) would be added.

**CaseA210a** (216 lines). Opener `203 ## Opened files and scope`; entries `205-212`; `214 ## Validation` closes.
Identical V1-V4.
- `205 F` — `skill://godspeed`; `…/godspeed/SKILL.md`
- `206 F` — `/home/…/round-27/contract.md`; `/home/…/round-26/contract.md`
- `207 F` — `/home/…/cases.json`; `cases-a2.json`
- `208 F` — scratch `earlyoom-main.c` A; `earlyoom-kill.c`, `earlyoom-msg.h`, `earlyoom-MANPAGE.md`, `systemd-journal-fields.xml`
- `209 A` — `/fast/scratch/hyaku/mori-r29/CaseA210a/cases-a2-10.json`
- `210 F` — `timestamps/hashes` (prose token with `/`)
- `211 F` — `schema/journal` (prose token with `/`)
- `212 F` — `tools/mori-oom-killers.py`; `.ufo/waves/`

All variants: `205,206,207,208,210,211,212:writer-forbidden-opened-path`.

**CaseA210b** (211 lines). Opener `195 ## Files and URLs opened` (V2-V4); entries `197-204`; `206 ## Validation,
tooling, and blindness` closes; no lead-in prose, so V2-V4 agree.
- `197 F` — `…/godspeed/SKILL.md`; `skill://godspeed`
- `198 F` — `/home/vgpnk/.omp/agent/RULES.md`
- `199 F` — `/home/…/round-27/contract.md`
- `200 F` — `/home/…/round-26/contract.md`
- `201 F` — `/home/…/cases.json`
- `202 F` — `/home/…/cases-a2.json`
- `203 F` — scratch `main.c` A; `kill.c`, `msg.h`, `MANPAGE.md`, `systemd.journal-fields.html`, `cases-a2-10.json`
- `204 N` — no candidate (`URLs opened are the five URLs …`)

V1: `1:writer-missing-files-opened-list`. V2-V4: `197,198,199,200,201,202,203,204:writer-forbidden-opened-path`.
Table `185-193` sits under `183 ## Upstream source evidence`, before the opener, and is never parsed.

**CaseA210c** (206 lines). Opener is the label form `194 Files opened:` (rule 1 clause 2). Entries `196-203`; `205 I
did not open or run …` is prose and closes. Identical V1-V4.
- `196 F` — `skill://godspeed`; `…/godspeed/SKILL.md`
- `197 F` — `/home/vgpnk/.omp/agent/RULES.md`
- `198 F` — `/home/…/round-27/contract.md`
- `199 F` — `/home/…/round-26/contract.md`
- `200 F` — `/home/…/cases.json`
- `201 F` — `/home/…/cases-a2.json`
- `202 F` — scratch `main.c` A; `kill.c`, `msg.h`, `MANPAGE.md`, `systemd.journal-fields.html`
- `203 A` — `/fast/scratch/hyaku/mori-r29/CaseA210c/cases-a2-10.json`

All variants: `196,197,198,199,200,201,202:writer-forbidden-opened-path`. **No missing-list hit.**

**CaseA210d** (191 lines). Opener `182 ## Opened files, source URLs, and evidence`; entries `184-191` to end of
file; identical V1-V4.
- `184 F` — `/home/…/round-27/contract.md`
- `185 F` — `/home/…/round-26/contract.md`
- `186 F` — `/home/…/cases.json`; `.../cases-a2.json`; `why/expect`
- `187 F` — `…/RULES.md`; `…/SKILL.md`; `skill://godspeed`
- `188 F` — `[main.c](https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c)`, stripped to `main.c](https://…`
- `189 F` — `main.c:161`, `main.c:295`, `kill.c:318` → `main.c`, `kill.c`
- `190 F` — scratch `main.c` A; `kill.c`, `msg.h`, `systemd.journal-fields.html`, `MANPAGE.md`
- `191 F` — `tools/mori-oom-killers.py` (the writer's own "I did not open or run" clause)

All variants: `184,185,186,187,188,189,190,191:writer-forbidden-opened-path`.

## Final sets

`scanned=8`, exit 1, and no `writer-tool-source-citation` or `writer-tool-run-output` hit on this wave in any
variant. That is swept, not assumed: `grep -nE
'mori-oom-killers[.]py[[:space:]]*:[[:space:]]*[0-9]|…tool[[:space:]]+lines?|…tool[[:space:]]*:[[:space:]]*[0-9]|
--inputs|MORI_OOM_KILLERS'` over the eight files exits 1 with no output, and every line matching the round-30
`tool_run_re` (`check-blind-wave.sh:82`) is either a file's last line or followed by no line holding both a verdict
and an exit (`:145`).

| variant | hits | `:1` missing-list | forbidden counts |
|---|---|---|---|
| V1 adjacent phrase, literal close | 27 | 207a, 207b, 207c, 207d, 210b | 210a 7, 210c 7, 210d 8 |
| V2 word-order phrase, literal close | 38 | 207a, 207b, 207d | 207c 5, 210a 7, 210b 8, 210c 7, 210d 8 |
| V3 + lead-in prose skipped | 44 | 207d | 207a 4, 207b 4, 207c 5, 210a 7, 210b 8, 210c 7, 210d 8 |
| V4 + same-or-higher-level heading | 47 | none | 207a 4, 207b 4, 207c 5, 207d 4, 210a 7, 210b 8, 210c 7, 210d 8 |

V4 in full (each line is `CaseA2…md:<lines>:writer-forbidden-opened-path`):

```
CaseA207a.md 196 197 198 199
CaseA207b.md 201 202 204 205
CaseA207c.md 194 195 196 197 198
CaseA207d.md 198 199 200 201
CaseA210a.md 205 206 207 208 210 211 212
CaseA210b.md 197 198 199 200 201 202 203 204
CaseA210c.md 196 197 198 199 200 201 202
CaseA210d.md 184 185 186 187 188 189 190 191
```

## CaseA210c, said plainly

`CaseA210c.md:194` is `Files opened:`, a label-form list, not a heading. **Yes, it has a files-opened list**, and
rule 1 clause 2 (`rule-text.md:11-12`) opens a block there; entries 196-203 are parsed, only 203 passes the allow
list, so the file gets **seven forbidden hits and no missing-list hit** in every variant. The round-30 gate expected
a missing-list hit because it set `files_h2_active=0` for the label form (`check-blind-wave.sh:116-117`) and set
`files_entry_seen` only while that flag was 1 (`:128`) — the locked-in false positive routed as D1
(`corpus/lessons/round-30-verifier-spotcheck.md:176-177`). Round 31's clause 2 drops the flag and the false positive
disappears.

## Findings for the L1

1. **C2's fixtures cannot tell V1 from V4, so `exact=16/16` does not pin the behavior that decides this wave.** No
   fixture in `.ufo/waves/round-31/c2-fixtures.json` has (a) a heading with words between `files` and `opened`,
   (b) lead-in prose between opener and first entry, (c) a sub-heading inside the block, (d) a markdown link entry,
   or (e) a bare upstream filename citation. F01 covers prose only after the entries, F03 the label form, F06 the
   table form. All 16 pass under all four readings.
2. **Rule 1 needs the word-order wording or three adjudicated false positives return.** V1 re-emits
   `CaseA207b.md:1`, `CaseA207c.md:1`, `CaseA210b.md:1` from the list in `check-blind-wave.sh:179-185`, which
   `round-30/contract.md:170-172` forbids; V2's phrase is what `:115` already implements.
3. **Rule 3 also re-emits false positives; only the heading-level repair clears all of them.** V2 emits 207a:1,
   207b:1, 207d:1; V3 emits 207d:1; V4 emits none of the 20. `CaseA207d.md:196` forces the level rule.
4. **Vocabulary hits survive any allow list.** Of V4's 47, ten rest on prose or bare upstream filenames no path
   allow list can admit: 207c:198 and 210a:208 (bare `kill.c`, `msg.h`), 210a:210 (`timestamps/hashes`), 210a:211
   (`schema/journal`), 210b:203, 210b:204 (no candidate), 210c:202, 210d:188 (markdown-link token), 210d:189
   (`main.c`), 210d:190. Two more — 210a:212, 210d:191 — are the writer's "I did not open
   `tools/mori-oom-killers.py`" disclosure read as an opened path. That is the class the round-29 spot-check named
   (`corpus/lessons/round-29-verifier-spotcheck.md:162-163`).
5. **No round-29 anchor prints `blind_violations=0` under this rule.** Even allowing every lane path, `SKILL.md`,
   `RULES.md` and every fetched URL, at least six hits remain (210a:210, 210a:211, 210b:204, 210d:188, 210d:189,
   210d:190). [INFERENCE] A round-29 anchor must pin the V4 set, not zero.
6. **Optional widening.** Adding `/home/vgpnk/.agents/skills/godspeed/SKILL.md` and `/home/vgpnk/.omp/agent/RULES.md`,
   as round-30 A3 did (`check-blind-wave.sh:20`), clears exactly 207c:194, 210b:198, 210c:197. The five lines citing
   `skill://godspeed` (207a:196, 210a:205, 210b:197, 210c:196, 210d:187) stay hits: that token matches no allow line.

## Minimal rule-text delta that makes the eight briefs converge (draft)

```
1. A block opens at a Markdown heading (any level) whose text holds "files" then "opened", or "opened" then
   "files", in that order with anything between (case-insensitive), or at a trimmed line starting with
   `Files opened:` or `Opened files:` (case-insensitive).
3. The block closes at the first heading of the same or higher level than the opener, or at the first non-blank
   line that is not an entry once an entry has been seen; prose and blanks before the first entry are skipped.
```

With those two sentences the wave yields the V4 set and none of the 20 adjudicated false positives. Add fixtures for
shapes 1(a)-(e): `## Files and URLs opened`; a `Local files:` lead-in; `### Lane files` inside the block;
`[main.c](https://…)`; a `main.c:161` row.

## Bounds

This report is the only file written; nothing under `.ufo/waves/round-29/` or `round-30/` changed. No tool was
installed or updated. No process left running. No uid, real pid, unit name, journal text or session path appears
above. Unrun check: the gate itself was not executed — it does not exist at HEAD and the question asked for a hand
derivation.
