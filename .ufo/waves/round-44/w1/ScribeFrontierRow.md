# ScribeFrontierRow — mori round 44, wave 1

lane: mori · round: 44 · wave: 1 · role: scribe (leaf, no dispatch) · date: 2026-10-25
lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin` · instruments frozen at
`7cb59c6891d4f5d0266fe062565f094da835dc84` · fleet repo read-only · nothing outside this
file was written · no `git add/commit/push/checkout/stash/reset`, no jj mutation.

Deliverable: the C3 frontier-map row (draft, ≤ 60 words) and a PROVINCE note fragment.
Status: **draft only** — I appended nothing to `corpus/README.md` and edited nothing in
`PROVINCE.md`. The integration owner applies both.

Sandboxes: `/tmp/mori44-scribe-0T7kNG` (git-archive copy of HEAD + row stub),
`/tmp/c3-stage-QtmQRy` (census staging repro), `/tmp/tmp.wzAS3583X2` (first repro).

---

## 1. Ground truth measured before drafting

Two states exist at once; the worktree moved under this seat (entry and README bytes were
rewritten at `2026-10-25 05:16:38 -0300` = `08:16:38Z`, after my first read at 05:12).
All drafts below are anchored to the **08:16Z worktree bytes**, and that is stated in each
draft's provenance.

| fact | HEAD `7cb59c68` | worktree at 2026-10-25T08:16Z (uncommitted) |
|---|---|---|
| `corpus/knowledge/pid-probe-conclusion-r44.md` | absent (`git cat-file -e HEAD:…` → 128) | present, 4261 bytes, mtime 05:16:27 -0300 |
| registry data rows in `corpus/SOURCES.md` | 243 | 245 |
| `S471` / `S472` rows | 0 / 0 | 1 / 1, both `mined`, `used-by corpus/knowledge/pid-probe-conclusion-r44.md` |
| `## Round-44 coverage additions` in `corpus/README.md` | 0 | 1 (line 627), section = 147 words |
| `git grep -l 'Z ゾンビ' HEAD -- corpus/` | 0 files | (not a revision) |
| fleet census on the registry | — | `exit 0` (`file ok …corpus/SOURCES.md`) |

```
$ git status --porcelain
 M LOG.md
 M SCORECARD.md
 M corpus/QUALITY.md
 M corpus/README.md
 M corpus/SOURCES.md
 M corpus/lessons/round-43.md
?? .ufo/waves/round-44/w1-spec.json
?? .ufo/waves/round-44/w1/
?? corpus/knowledge/pid-probe-conclusion-r44.md
```

Nothing of C3 is committed. A C3 after-sweep run today reads HEAD and sees 243 rows, no
entry, no README heading.

---

## 2. Draft — frontier-map row for C3

Append under a new heading, as one line (the heading is the only added structure; it matches
the r42/r43 prose-section shape the task pointed me at):

```
## Round-44 coverage additions

FR5 ground not held: the `Z`/`X` state alphabet and the three worlds a zero-character `/proc/<pid>/cmdline` read is consistent with — never existed, zombie, swapped out (translation-only, retired) — `state` discriminates (`corpus/knowledge/pid-probe-conclusion-r44.md`; S471, S472, opened 2026-10-25). PROVINCE FR5’s “an unavailable pid probe is not absence, and argv-substring matches do not establish daemon identity” bounds it: no census cutover, FR5 stays frontier.
```

Measured: **60 words** (`len(row.split())` on the exact bytes above).

Element check against the assignment:

| required element | in the row |
|---|---|
| ground the lane did not hold (Z/X state alphabet) | “the `Z`/`X` state alphabet” |
| the three worlds a zero-character cmdline read is consistent with | “the three worlds … — never existed, zombie, swapped out (translation-only, retired)” |
| entry path it names | `` `corpus/knowledge/pid-probe-conclusion-r44.md` `` (full repo-relative form; see §5 X2 for why the relative `knowledge/…` form fails the counter) |
| two source ids | `S471, S472` |
| access date | `opened 2026-10-25` |
| does not claim the census changed | “no census cutover” |
| does not claim FR5 is closed | “FR5 stays frontier” |
| states which PROVINCE sentence bounds it | quotes the FR5 boundary sentence verbatim (§4) |

Placement rule for the owner: if the provisional section already in the worktree
(`corpus/README.md:627-640`, 147 words) is kept as the heading, **replace its prose with this
one line** — do not append a second row under the same heading. The provisional prose is
measured against the same requirements in §5 X2.

Why the third world carries `(translation-only, retired)`: the entry's current bytes say
“Two worlds are grounded here, not three” and call the swap-out branch “a retired claim on
the same desk”. The qualifier keeps the row from repeating a retired claim as current ground
while still naming the three-world frame the frozen P-C3 sentence uses. See X3 for the
contract-level conflict this does not resolve.

---

## 3. Draft — PROVINCE note fragment

Insert as a new paragraph after the Round-16 note (`PROVINCE.md:40`) and before
`## Frontier` (`PROVINCE.md:42`), matching the Round-15/Round-16 note placement:

```
Round-44 C3 adds the FR5 degraded-probe reading: a zero-character
`/proc/<pid>/cmdline` read does not establish absence — the `stat` state field
(`Z` ゾンビ / `X` 死亡, the latter since Linux 2.6.0) separates a present-but-dead
process from a live one, and the older zh_TW translation adds a swapped-out
branch that the modern page retires on the same desk (`corpus/knowledge/pid-probe-conclusion-r44.md`;
S471, S472, both opened 2026-10-25). This is not a census surface and performs no
census cutover: no `SURFACE` row, finding id, baseline re-pin or threshold is
added. FR5 stays Frontier under its existing boundary sentence — "an unavailable
pid probe is not absence, and argv-substring matches do not establish daemon
identity": the entry says what a degraded probe may conclude, not how to identify
the watchdog daemon, and no held source establishes daemon identity from a
degraded or argv-substring probe.
```

The fragment deliberately does not repeat “three worlds” as grounded: it states what the
entry's current bytes state (one world grounded by both pages, one retired). If the judge
rules the retired branch may not appear in the map at all, delete the clause
“and the older zh_TW translation … same desk” — nothing else in the fragment depends on it.

---

## 4. The PROVINCE sentence that still bounds the claim (explicit)

`PROVINCE.md:48`, Frontier FR5, verbatim:

> **FR5 — Watchdog daemon identity and degraded-pgrep visibility** (state F5). First
> evidence: `corpus/knowledge/audit-r11.md:200-201`. Boundary: an unavailable pid probe is
> not absence, and argv-substring matches do not establish daemon identity.

The bounding sentence is: **“an unavailable pid probe is not absence, and argv-substring
matches do not establish daemon identity.”**

It still bounds the round-44 claim in all three ways:

1. “not absence” — the entry explains what a degraded read *may* be instead of absence; it
   never converts an empty read into evidence of presence or of a live daemon.
2. “argv-substring matches do not establish daemon identity” — the entry adds a `state`
   discriminator and explicitly refuses to identify the watchdog daemon from it; the row
   therefore does not touch daemon identity.
3. The row asserts no census cutover and leaves FR5 in Frontier; no PROVINCE Core move is
   claimed, so the FR5 bullet's own text is unedited by this round.

---

## 5. Evidence — commands run and what they returned

**E1 — HEAD absence and before-state.**
```
$ git cat-file -e HEAD:corpus/knowledge/pid-probe-conclusion-r44.md; echo $?
128
$ git show HEAD:corpus/SOURCES.md | grep -cE '^ {0,3}\| S[0-9]{3,} \|'
243
$ git show HEAD:corpus/SOURCES.md | grep -c '^| S471 '
0
$ git show HEAD:corpus/README.md | grep -c '^## Round-44'
0
$ git grep -l 'Z ゾンビ' HEAD -- corpus/ | wc -l
0
```

**E2 — worktree registry and census.**
```
$ grep -cE '^ {0,3}\| S[0-9]{3,} \|' corpus/SOURCES.md
245
$ grep -c '^| S471 ' corpus/SOURCES.md ; grep -c '^| S472 ' corpus/SOURCES.md
1
1
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --file /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md; echo exit=$?
… file	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
exit=0
```

**E3 — frozen counter on the current worktree (default entry path).**
```
$ python3 .ufo/waves/round-44/count-c3.py WORK --row S471 --row S472 \
    --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh; echo exit=$?
check entry_present    PASS (4261 bytes)
check entry_meta       PASS (sources S471,S472)
check rows_present     PASS (rows S471,S472 mined)
check census_ok        FAIL (exit=1)
check readme_row       FAIL (no line names the entry)
rev=WORK
C3=unmet
exit=1
```
`readme_row` fails because the provisional README line names `knowledge/pid-probe-conclusion-r44.md`,
not the counter's default `corpus/knowledge/pid-probe-conclusion-r44.md`.

**E4 — why the relative form cannot be rescued by `--entry`.**
```
$ python3 .ufo/waves/round-44/count-c3.py WORK --entry knowledge/pid-probe-conclusion-r44.md \
    --row S471 --row S472 --census …/sources-census.sh; echo exit=$?
check entry_present    FAIL (absent)
rev=WORK
C3=unmet
exit=1
```
`read_at` joins the entry argument onto the repo root (`count-c3.py:60-67`), so only the full
`corpus/…` path resolves; the README line must therefore carry the full path.

**E5 — the counter's own selftest.**
```
$ python3 .ufo/waves/round-44/count-c3.py --selftest; echo exit=$?
selftest PASS registered_entry_met
selftest PASS absent_entry_unmet
selftest PASS row_without_used_by_unmet
selftest PASS red_census_unmet
selftest PASS readme_without_row_unmet
selftest PASS missing_coverage_map_unmet
C3_SELFTEST pass=6 fail=0
exit=0
```

**E6 — `census_ok` fails independently of this round's additions.** At HEAD, scoring the
already-landed r43 entry and row S470:
```
$ python3 .ufo/waves/round-44/count-c3.py HEAD \
    --entry corpus/knowledge/journal-disk-usage-total-r51.md --row S470 \
    --census …/sources-census.sh; echo exit=$?
check entry_present    PASS (1063 bytes)
check entry_meta       FAIL (coverage-map FR5; source: lacks )
check rows_present     PASS (rows S470 mined)
check census_ok        FAIL (exit=1)
check readme_row       FAIL (no line names the entry)
rev=7cb59c6891d4f5d0266fe062565f094da835dc84
C3=unmet
exit=1
```

**E7 — the drafted row satisfies `readme_row` (sandbox, not the lane).** `git archive HEAD`
into `/tmp/mori44-scribe-0T7kNG`, append the §2 heading+row, add a stub entry (sandbox-only,
not the entry draft), then:
```
$ python3 /tmp/mori44-scribe-0T7kNG/.ufo/waves/round-44/count-c3.py WORK \
    --repo /tmp/mori44-scribe-0T7kNG --census …/sources-census.sh \
    --entry corpus/knowledge/pid-probe-conclusion-r44.md --row S471 --row S472; echo exit=$?
check entry_present    PASS (284 bytes)
check entry_meta       PASS (sources S471,S472)
check rows_present     FAIL (S471 absent; S472 absent)
check census_ok        FAIL (exit=1)
check readme_row       PASS (names entry)
rev=WORK
C3=unmet
exit=1
```
The row is what flipped `readme_row` to PASS; `rows_present`/`census_ok` were sandbox stubs
and are not evidence about the lane.

**E8 — the census staging repro (basis of X1).**
```
$ S=$(mktemp -d); cp corpus/SOURCES.md "$S/SOURCES.md"
$ bash …/sources-census.sh validate --file "$S/SOURCES.md"; echo staged_exit=$?
… E11 lines ×279, W04 lines ×19 …
staged_exit=1
$ bash …/sources-census.sh validate --file /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
file	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
inlane_exit=0
```

---

## 6. Findings and conflicts — reported, not resolved here

**X1 (frozen instrument defect, C3 counter). `census_ok` cannot pass.**
`count-c3.py:132-145` writes the registry to `<mkdtemp>/SOURCES.md` and runs
`sources-census.sh validate --file <that path>`. The census resolves `used-by` paths against
`realpath(dirname(file)/..)` (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:499-503`),
i.e. against `/tmp`, so every `mined` row's `corpus/…` used-by is “missing” (E11 ×279, exit 1).
Measured both ways in E8. Consequence: `C3=met` is unreachable for the real lane regardless of
what lands — E6 shows the same FAIL on a round-43 row at HEAD, so it is not caused by round-44
content. The selftest's `red_census_unmet`/met arms use a fake census script
(`count-c3.py:172,204`), which is why `pass=6 fail=0` (E5) cannot see it. Per the contract's
Freeze clause this is a lesson for round 45, never a post-freeze patch.

**X2 (README row currently in the worktree does not meet the row spec).**
`corpus/README.md:627-640` (measured 147 words): contains `knowledge/pid-probe-conclusion-r44.md`
only (no `corpus/` prefix → `readme_row` FAIL under the only resolving `--entry`, E3/E4); no
“three worlds” phrase; does not quote the bounding PROVINCE sentence. My §2 line fixes all
three and is 60 words. Owner should replace, not append.

**X3 (content conflict the row cannot settle).**
Frozen P-C3 requires “the three worlds a zero-character `/proc/<pid>/cmdline` read is consistent
with”. The source seat that opened both pages, `ScoutSources490.md` §5, states:

> On the staged bytes, only **two** worlds are stated anywhere
> … **The third world is therefore not grounded on either staged page and must not be
> attributed to them.**

and §6.2 records that S471's `comm` sentence (“実行形式がスワップアウトされているかどうかによらず、
見ることができる”) contradicts S472's swap-out coupling. The entry's 08:16Z bytes agree with the
scout: “The opened pages state **two** worlds”, “Two worlds are grounded here, not three”, and the
swap-out branch is “a retired claim on the same desk”. So the entry that lands grounds two worlds,
while the frozen predicate's parenthetical says three. The counter cannot detect the difference
(it checks ids, meta, census, README naming only). My row keeps the predicate's three-world frame
and marks the third `(translation-only, retired)` so the map repeats no retired claim; whether
that satisfies P-C3 as written, or whether P-C3's parenthetical is itself the defect, is the
judge's call. If the judge rules the third world ungrounded, the row's parenthetical must become
“two worlds per the staged pages” — a contract-level change routed to round 45, not a scribe edit.

**X4 (cross-package wording, verbatim).**
Staged campaign entry
`/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/probe-absent-vs-dead-r39.md`
(§Boundaries) says the rule is already held “as the upstream `proc_pid_cmdline(5)` row (which also
carries the Linux 2.3.26 swap-out note)”. The lane's S170 row (`corpus/SOURCES.md:176`) lists
“the zombie exception and its 0-character read …” and no swap-out note; the lane entry says S170
documents the zombie exception “not the swap-out branch”. Recorded for the judge; no lane byte
depends on the campaign wording.

**X5 (measurement target).**
C3's before/after sweeps are revision-scoped. At this seat's close, C3's entry, the two registry
rows and the README section are all uncommitted; any scored run must name the landed tip, not
`WORK` (E3 is a worktree read, E1/E6 are HEAD reads).

---

## 7. Out of scope / not done

- No edit to `corpus/README.md`, `PROVINCE.md`, `corpus/SOURCES.md`,
  `corpus/knowledge/pid-probe-conclusion-r44.md`, `SKILL.md`, `SCORECARD.md`, `LOG.md`,
  `corpus/QUALITY.md`, `corpus/lessons/round-43.md`, or any frozen instrument/fixture.
- No commit, no jj mutation, no subagent dispatch.
- No tool install or upgrade — none was needed (no record to make).
- Did not re-fetch the two source pages; page receipts and CJK quote verification belong to
  `ScoutSources490.md`. Did not verify the entry's quotes against page bytes.
- Did not run the C1 or C2 counters; their verdicts belong to their own seats.

## 8. Provenance

Read at `2026-10-25T08:16Z` unless noted: `.ufo/waves/round-44/contract.md`;
`.ufo/waves/round-44/w1-spec.json` (items 0,1,2,6); `.ufo/waves/round-44/count-c3.py`
(lines 20-160, 278-321); `corpus/README.md:588-645` (HEAD bytes first, worktree bytes at
05:12 and 05:16 -0300); `PROVINCE.md:1-50`; `corpus/SOURCES.md` (S170 at :176, S471 at :250,
S472 at :251, worktree); `corpus/knowledge/pid-probe-conclusion-r44.md` (worktree, 4261 bytes);
`.ufo/waves/round-44/w1/ScoutSources490.md`; the staged campaign entry (read-only, shokuknow).
Instrument hashes untouched; `git rev-parse HEAD` = `7cb59c6891d4f5d0266fe062565f094da835dc84`.
