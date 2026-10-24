# SupersedeS101 — C1 row S147 superseding S101 (round 28, wave 1)

Seat: `MoriR28.SupersedeS101` (scribe, leaf; no subagent dispatch; no background job).
Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`; entering tip `6ebd518f` (round-27 verifier spot-check); lane HEAD
`1c4c186` at read time. Scratch: `/fast/scratch/hyaku/mori-r28/SupersedeS101/` (one `git clone --no-hardlinks`
sandbox; commits only inside it). Lane writes by this seat: this report file only.

## 0. Result in one paragraph

S101 was first published at `90ed9b778593867b3a543e020f62e2bb955d8b18` ("round-25: sources S098-S111 (7
admitted, 7 rejected) and knowledge entry harness-job-capacity-r25 (C2)") and edited in place at
`d3b7af2a287339c5d94655d741f83e5af07090cc` ("round-25: wave-2 fixes: … S101 teaches cell no longer overclaims");
**one** cell differs, `teaches`. The first-published `teaches` is **false against the bytes it points at**: it says
the settings page "states no upper bound" and that therefore "docs and code disagree for values above 100", but the
page states a floor of 1 and no ceiling (`:623`), and the upstream tree at the same commit states the ceiling in
`docs/tools/eval.md:258` — the docs and the code agree. The row was restored byte-equal to its first publication at
`1c4c186` (lane HEAD), so the registry now carries the defective wording again in S101's own cell and the corrected
teaching must live on a superseding row. This report gives that row (**S147**), its Gate line, the QUALITY 77 sweep
list, and the falsifications run on a sandbox clone (census exit 0 with one new W04; the counter's own per-row test
accepts S147; the row-identity check stays `changed=0`).

## 1. First-published cells versus the tip

First commit carrying `| S101 |` in `corpus/SOURCES.md` (the command the assignment gives, run read-only in the lane):

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --reverse --format=%H -S'| S101 |' -- corpus/SOURCES.md | head -1
90ed9b778593867b3a543e020f62e2bb955d8b18
```

`90ed9b7` is "round-25: sources S098-S111 (7 admitted, 7 rejected) and knowledge entry harness-job-capacity-r25
(C2)" (2026-10-22 07:20:23 -0300). The row sits at `corpus/SOURCES.md:107` at `90ed9b7`, at `6ebd518f` and at
`1c4c186` (same line number at all three revisions).

The in-place edit is `d3b7af2` (2026-10-22 08:43:00 -0300). `git log -S'|' -- corpus/SOURCES.md` lists both commits
because the pickaxe matches the string count, not the id; the edit is confirmed by the frozen QUALITY 81 check,
which prints `changed S101 cells=teaches` for `6ebd518f` (and `changed=3` overall: S096, S097, S101).

| # | cell | first published `90ed9b7` | tip `6ebd518f` | differs |
|---|---|---|---|---|
| 1 | id | S101 | S101 | no |
| 2 | source | oh-my-pi settings reference at v18.12.6 — https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/docs/settings.md | same | no |
| 3 | kind | docs | docs | no |
| 4 | tier | A | A | no |
| 5 | scope | the user-facing description of `async.maxJobs`: declared type, default and stated bounds; not the runtime clamp | same | no |
| 6 | anchor | section "### Tools and approvals":593, table row `async.maxJobs`:623; tag v18.12.6 = commit 45c35e40c46166dc726ccc52f5d27f40f2449f99; file sha256 0b2e1457021fa526f2c35015672f1d7ccbac95e7b9f217528ab8022c55ed5883; opened 2026-10-22 | same | no |
| 7 | **teaches** | The reference gives the default 100 and a floor of 1 **but states no upper bound, so a configured value above 100 reads as honoured; the code clamps it, so docs and code disagree for values above 100.** | The reference gives the default 100 and a floor of 1 **and states no maximum, so a reader of this page alone would expect a configured value above 100 to be honoured; the 100 maximum is documented only in docs/tools/eval.md:258 (S103) and enforced in sdk.ts:2284 (S099). The page omits the maximum; it does not contradict it.** | **yes** |
| 8 | status | mined | mined | no |
| 9 | opened | 2026-10-22 | 2026-10-22 | no |
| 10 | recheck | on-release | on-release | no |
| 11 | used-by | corpus/knowledge/harness-job-capacity-r25.md | same | no |

Byte-level: `90ed9b7` line 107 is 803 bytes; `6ebd518f` line 107 is 928 bytes; the first difference is at byte 574
(the `teaches` cell); the tail after it (status / opened / recheck / used-by) is identical. Only one cell changed, and
no other cell of S101 was touched in the whole history (`git log -S'| S101 |'` lists exactly the two commits above).

**The lane's own readers already called the defect, in round 25, and the fix was logged nowhere.** The wave-2
critic named it as the row's medium finding (`.ufo/waves/round-25/w2/CriticSourcesDiscernment.md:14`, `:55`,
`:172` — "S101's `teaches` claims that 'docs and code disagree'. Its sibling row S103, from the same upstream docs
tree at the same commit, states the maximum."), and the wave-2 re-open gave the smallest fix
(`.ufo/waves/round-25/w2/ReopenDocsAndCommit.md:19` — "**Low.** S101 says 'so docs and code disagree for values
above 100'. That overstates it."). The round-25 wave-2 fix commit applied it **in place** (the commit subject says
"S101 teaches cell no longer overclaims"), which is the breach of CORPUS.md Rules 2 that round 27's lesson names
(`corpus/lessons/round-27.md:35`: "S101 (teaches)") and that the outside check routed
(`corpus/lessons/round-27-verifier-spotcheck.md:148`: "S096, S097, S101 still differ from their first-published
cells … restore or supersede them").

**Restore state at lane HEAD `1c4c186`: done.** `cmp` of `git show 90ed9b7:corpus/SOURCES.md | sed -n '107p'` and
`git show 1c4c186:corpus/SOURCES.md | sed -n '107p'` → identical, 803 bytes both. The registry therefore holds the
defective wording in S101's own `teaches` cell again, which is exactly why the corrected text must move to S147 and
every live reader must cite S147 (see §5).

## 2. The source re-opened today, and every statement checked against the bytes

URL: `https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/docs/settings.md`
(tag v18.12.6 = commit `45c35e40c46166dc726ccc52f5d27f40f2449f99`; the tag's commit was re-confirmed today through
the GitHub commits API: `sha 45c35e40c46166dc726ccc52f5d27f40f2449f99`, committer date 2026-10-21T20:49:59Z,
subject "chore: bump version to 18.12.6").

- Fetch: HTTP 200, 148,359 bytes, accessed **2026-10-22T17:59:03Z**, sha256
  `0b2e1457021fa526f2c35015672f1d7ccbac95e7b9f217528ab8022c55ed5883` — **identical to the digest S101's anchor
  cell already records**, so the file has not changed since round 25 and the anchor needs no digest edit.
- `:593` is exactly `### Tools and approvals`.
- `:623` is exactly:
  `| \`async.maxJobs\` | number | \`100\` | Running background-job cap, floored to at least 1; parked/queued jobs do not consume execution slots. |`
- A case-sensitive scan of the whole file for `maxJobs|maximum 100|Background job limit|background-job cap`
  returns **one** line: `:623`. The page states a floor of 1, a default of 100, and **no maximum** — the
  "no upper bound" claim of the first-published cell is wrong (the page does state a bound: the floor), and the
  "docs and code disagree" claim is wrong (see below).
- The other `maximum` hits in the file (`:611`, `:646`, `:647`, `:687`, `:746`, `:971`) are other settings
  (`tools.maxTimeout`, `computer.maxWidth/Height`, `bash.direnvLoadTimeoutMs`, context windows,
  `providers.streamIdleTimeoutSeconds`); none is about `async.maxJobs`.
- **The tree-wide sweep** (whole upstream tree at the tag, fetched as the 76,435,207-byte tarball
  `codeload.github.com/can1357/oh-my-pi/tar.gz/45c35e40…`, sha256
  `645df2d527de1b0ff62514ac14250230622439d5d5e84f781ffa06d38415b8d0`, accessed 2026-10-22T18:18:45Z): only **four**
  files mention `maxJobs` at all — `docs/settings.md`, `docs/tools/eval.md`,
  `packages/coding-agent/src/tools/settings.ts` (the accessor, no description) and one test file. The string
  "default and maximum" occurs exactly **once** in the whole tree, at `docs/tools/eval.md:258`:
  "every handle is a running background job counted against the session-wide `async.maxJobs` cap (default and
  maximum 100) … `agent()` fails with `Background job limit reached` once that cap is full." `docs/settings.md:623`
  is the only other doc-level statement. So at v18.12.6 the upstream docs state the maximum **once**, on the eval
  page; the settings page omits it. The docs and the code agree; there is no disagreement to report.
- `docs/tools/eval.md` (sha256 `fb2fc4a139ba187f1cc062fab53bd72a48dd13b1f81f0c3318ec7a79d41e495c`, 28,027 bytes,
  accessed 2026-10-22T17:59:10Z) → `:258` is the `agent()` bullet quoted above.
- `packages/coding-agent/src/sdk.ts` (sha256 `c0228addd4cfe93cfd370c7248e9db29743f0fa802aea0e1d1adf4994dbe6957`) →
  `:2284` is exactly `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings)),` — the 100 ceiling, matching
  the `docs/tools/eval.md:258` statement. The clamp site's **floor** was removed upstream on 2026-09-24 (S140/S152
  carry that history), so `sdk.ts:2284` alone shows the ceiling and no floor; the effective floor of 1 comes from
  `async/job-manager.ts:305` (S152's Gate line). This matters for the corrected row: S147 must not repeat the
  first-published claim that the settings page is the only place the cap is stated.
- `packages/coding-agent/src/tools/settings.ts:941-946` registers `async.maxJobs` with `default: 100` and **no**
  `ui` block, i.e. no label or description; `config/settings-schema.ts` is **HTTP 404** at this tag (the file was
  removed upstream on 2026-09-24, S140's lineage). So the settings *schema* carries no ceiling either.
- The upstream `async.maxJobs` table row was first committed on 2026-09-30 in `1b3222187919` ("chore: updated
  docs", author 2026-09-30T17:57:16Z, parent `30aec05d`): fetched at that commit the row is present at `:613`, and
  fetched at its parent it is **absent** (0 occurrences of `maxJobs`). This is the date the round-25 wave-2 re-open
  asked for and never got (`.ufo/waves/round-25/w2/ReopenDocsAndCommit.md:11`, finding 3: "S101 has no date for its
  row").

## 3. Ready-to-paste row S147

Paste position: insert after the `| S152 |` row (last registry row) and before the blank line and `## Paths`. 13
pipe-separated fields, no `|` inside any cell, `teaches` opens `supersedes S101 — ` (em dash U+2014 + space), status
`mined`, opened `2026-10-22`, recheck `on-release` (S101's convention), used-by as the L1 specified.

```text
| S147 | oh-my-pi settings reference at v18.12.6 — https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/docs/settings.md | docs | A | the upstream settings reference's own statements about `async.maxJobs` at v18.12.6: the declared type, the default, the floor it states and the maximum it does not state; the ceiling is documented on the eval page (S103) and enforced in the code (S099), not here | section "### Tools and approvals":593, table row `async.maxJobs`:623 (the only `async.maxJobs` mention in the file); the table row was first committed upstream 2026-09-30 (1b3222187919, absent from its parent 30aec05d); tag v18.12.6 = commit 45c35e40c46166dc726ccc52f5d27f40f2449f99; file sha256 0b2e1457021fa526f2c35015672f1d7ccbac95e7b9f217528ab8022c55ed5883 (148,359 bytes); re-opened 2026-10-22T17:59:03Z, digest unchanged | supersedes S101 — the old row's teaches said the reference "states no upper bound" and that therefore "a configured value above 100 reads as honoured" and "docs and code disagree for values above 100"; the page states no ceiling and does not contradict the code, and a reader's expectation is not a document's claim. The reference gives the default 100 and a floor of 1 and states no maximum; the 100 maximum is documented only in docs/tools/eval.md:258 (S103) and enforced in sdk.ts:2284 (S099); the page omits the maximum, it does not contradict it. | mined | 2026-10-22 | on-release | corpus/knowledge/harness-job-capacity-r25.md, corpus/lessons/round-28.md |
```

Why each cell reads as it does:

- **source / kind / tier** — unchanged from S101 (same URL, same `docs` kind, same tier A): the row's subject did not
  change, only its wording.
- **scope** — replaced. S101's scope ("declared type, default and stated bounds") is true but silent on the point
  the row is about: the page states a floor and no maximum. The new scope names both halves and excludes the two
  other rows' subjects (the eval page S103 and the code S099), so no reader can take S147 for the source of the
  ceiling. The scope differs from S101's, so the census raises a **W04** "duplicate url … across scopes" for S147
  (a warning, not an error — §6).
- **anchor** — S101's anchor, plus the two facts the round-25 wave-2 re-open asked for and the row never got: the
  date the upstream table row was first committed (`1b3222187919`, 2026-09-30, absent from its parent), and the
  statement that `:623` is the file's only `async.maxJobs` mention. The digest is unchanged from S101's, so the
  anchor keeps one sha256 rather than two.
- **teaches** — opens `supersedes S101 — `, then names what the old row got wrong (the "no upper bound" reading,
  the untagged "reads as honoured" inference, and the "docs and code disagree" claim, which the tree-wide sweep
  refutes), then states the corrected teaching: default 100, floor of 1, **no maximum stated**; the maximum is
  documented only at `docs/tools/eval.md:258` (S103) and enforced at `sdk.ts:2284` (S099); the page omits the
  maximum and does not contradict the code. The corrected text is byte-identical to the wording the round-25 wave-2
  critic proposed (`.ufo/waves/round-25/w2/CriticSourcesDiscernment.md:74`), re-verified against today's bytes.
- **used-by** — the two live files that cite S147 at the landed rev: the harness entry
  `corpus/knowledge/harness-job-capacity-r25.md` (front-matter `:1` and F1 `:47`, both repointed from S101 to
  S147 in the lane's own working tree) and the round-28 lesson `corpus/lessons/round-28.md` (Gate line below).
  The closed lessons and the outside check cite S101 as **history** and are not repointable (they are the record of
  what round 25 and round 27 knew); listing them would fail the counter's `used_by_not_citing` test, which requires
  every used-by path to name the new id at the landed rev (the same constraint the sibling S152 seat measured:
  `.ufo/waves/round-28/w1/SupersedeS140.md:54`).

## 4. Gate line (round-28 lesson `## Gate`)

Paste after the `| S152 |` line of the round-28 lesson's Gate table (the table has the columns
`| id | source | access time | sha256 | located quote | decision |`).

```text
| S147 | https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/docs/settings.md | 2026-10-22T17:59:03Z | `0b2e1457021fa526f2c35015672f1d7ccbac95e7b9f217528ab8022c55ed5883` | `:623` "`async.maxJobs` \| number \| `100` \| Running background-job cap, floored to at least 1" (11 words) | admit, A, mined (SupersedeS101) |
```

The quote is verbatim from `docs/settings.md:623` (the row text, truncated at "floored to at least 1"; the full
line continues "; parked/queued jobs do not consume execution slots.") and is 11 words. The counter's Gate test
(`count-c1.sh`, the `gate_line` check) needs an https URL, a 64-hex sha256 and a quoted span on the line: all three
are present. The sha256 is the digest of the fetched bytes and matches the digest already recorded in S101's anchor.

## 5. QUALITY 77 sweep — every place whose prose states the defective wording

Live surfaces (must carry the corrected wording, or cite the row that carries it, at the correction commit):

1. `corpus/SOURCES.md:107` — **S101's own `teaches` cell.** QUALITY 81 freezes it to the first-published bytes, so
   the defective wording stands in the registry row itself; the correction is S147, not an edit. This is the same
   tension the sibling S096 seat recorded (`.ufo/waves/round-28/w1/SupersedeS096.md:14`, "QUALITY 81 … and QUALITY
   77 … cannot both hold for this row"): the restore is what the contract's C1 claim demands, and the superseding
   row plus the reader repointing is what QUALITY 77 gets.
2. `corpus/knowledge/harness-job-capacity-r25.md:1` (front-matter `source:` list) and `:47` (F1: "with type
   `number` and default `100` (S147, …)") — already repointed to S147 in the lane's working tree; verified at HEAD
   `1c4c186`: the file cites S147 twice and S101 **zero** times.
3. `corpus/lessons/round-28.md` — the new lesson: its Gate line above names S147, and it is the second used-by
   path of the row. Its body prose (`:11`) already says the corrected text lives "on only in the superseding rows
   S145–S147".

Records (keep as history; the correction is logged in the round-28 lesson, not rewritten):

4. `corpus/lessons/round-25.md:13` — "The settings reference states a default and a floor but no maximum (S101);
   only the eval page says "default and maximum 100" (S103)." — already the corrected wording, but it cites S101,
   whose restored cell now carries the defective one. The lesson is closed history and the counter exempts lessons
   from the reader test; the honest fix is a dated note in the round-28 lesson, which the L1 owns.
5. `corpus/lessons/round-25.md:61` — the round-25 Gate line for S101 (records what round 25 admitted).
6. `corpus/lessons/round-25-verifier-spotcheck.md:170` — "S101 overclaim before the report" (outside check, history).
7. `corpus/lessons/round-27.md:35` and `:128` — the M2 mistake record and the carried-debt line naming S101.
8. `corpus/lessons/round-27-verifier-spotcheck.md:133` and `:148` — the routed defect naming S101.
9. `.ufo/waves/round-25/w1/SrcSettingsDefault.md:76` — the wave-1 seat's draft row, the origin of the defective
   wording (it is quoted in the wave-2 critic's report, `:55`).
10. `.ufo/waves/round-25/w2/CriticSourcesDiscernment.md:14`, `:55`, `:172` and
    `.ufo/waves/round-25/w2/ReopenDocsAndCommit.md:11`, `:19` — the wave-2 seats **quote** the defective wording to
    name it as a defect; those quotes are the audit trail and must not be rewritten.

**No live file outside `corpus/SOURCES.md` and the two repointed S147 readers states the defective claim.** A
whitespace-folded, emphasis-stripped sweep of the whole tree at `6ebd518f` for `docs and code disagree`,
`states no upper bound`, `reads as honoured` and `the code clamps it, so` returns only the ten history locations
above; `corpus/knowledge/`, `SKILL.md`, `PROVINCE.md` and `corpus/README.md` carry none of them.

## 6. Falsifications (sandbox clone; the lane was not written)

Sandbox: `/fast/scratch/hyaku/mori-r28/SupersedeS101/sim3` (`git clone --no-hardlinks` of the lane at `1c4c186`),
with the S147 row of §3 inserted after `| S152 |` and the Gate line of §4 inserted after the `| S152 |` Gate row of
`corpus/lessons/round-28.md`; committed there as `6b95e7eb` (scratch only).

- **Census** `scripts/sources-census.sh validate --today 2026-10-22 --root <sandbox-root> mori` → **exit 0**, output
  `mori ok …/corpus/SOURCES.md`, with the six pre-existing W04 lines for S035/S037/S073–S076 plus **one new W04**:
  `mori W04 S147 duplicate url raw.githubusercontent.com/can1357/oh-my-pi/45c35e40…/docs/settings.md across scopes`.
  W04 is a warning (a URL reused under a different scope), not an error, and it is what the sibling S148/S149/S150
  rows already produce (the same six W04s plus three more, visible in the lane's own working tree). No E-code and
  no E11 for S147: both used-by paths exist in the sandbox root.
- **Row-identity check** (the frozen round-27 script, `df886be1:.ufo/waves/round-27/check-row-identity.py`, with
  only its `LANE` constant repointed to the sandbox): `rows=149 changed=0 removed=0 bad=0`. S101 stays out of the
  changed list — the restore holds with S147 present, and the new row is not a diff.
- **C1 counter** (`count-c1.sh`, amended A1; `LANE` repointed to the sandbox): `row_identity=rows=149 changed=0
  removed=0 bad=0`, `superseding=3/8 ids=S101,S131,S140`, `readers_left=0`. **No `fail S147` line**: the prefix is
  `supersedes S101 — `, the teaches differs from S101's, status is `mined`, both used-by paths name S147 at the
  rev, and the Gate line carries a URL, a sha256 and a quoted span. The remaining failures are the other seats'
  rows (`fail S145`/`fail S146` used-by, `fail S148`/`S149`/`S150` row_absent), not S147's.
- **Negative control**: with the Gate line removed but the row present, the counter prints
  `fail S147 gate_line` — so the Gate line is load-bearing, not decoration.
- **Negative control**: with the row's `teaches` replaced by S101's exact restored cell, the counter prints
  `fail S147 teaches_unchanged`.

## 7. Bounds, tools, installs

Lane writes: this report file only. No `git add/commit/stash/checkout/switch/reset/pull/push` in the lane; only
read-only `git log/show/grep/rev-parse/ls-tree/diff/cmp` and one `git clone --no-hardlinks` into scratch (commits
made in the scratch clone only). No `jj` command ran, at the fleet root or anywhere else. Fetches: plain `curl` GETs
to public URLs only, no bot challenge, no headless browser. Privacy: no OMP settings values, session ids, pids,
uids, unit names or journal text; upstream code quotes, digests, line numbers and counts only. **No installs or
upgrades** — nothing was needed, and pacman transactions are paused host-wide. `/home/vgpnk/.omp/agent/RULES.md`
read first; its tooling directive needed no action for this seat.

## 8. Findings for the L1

1. **S101's restore is done and byte-verified** at HEAD `1c4c186` (`cmp` of the two `sed -n '107p'` outputs: equal,
   803 bytes). The defective wording is therefore back in the registry row; S147 plus the reader repointing is the
   only correction route QUALITY 81 permits.
2. **The live readers are already repointed** to S147 in the working tree (`harness-job-capacity-r25.md:1` and
   `:47`); at HEAD the file cites S147 twice and S101 zero times, and the counter's `readers_left=0` at `1c4c186`
   confirms no live reader names S101, S096, S097, S127, S128, S129, S131 or S140 any more.
3. **Open item the L1 owns**: `corpus/lessons/round-25.md:13` states the corrected fact but still cites S101, whose
   restored cell now holds the defective wording. A dated note in the round-28 lesson (the lane's convention for
   closed lessons — cf. `corpus/lessons/round-27.md`) is the fix; a rewrite of the closed lesson is not.
4. **W04 is expected and harmless**: S147 reuses S101's URL under a different scope, so the census prints one W04,
   exactly as the sibling S148/S149/S150 rows already do in the lane's working tree. Validate still exits 0.
5. **A row defect of the same shape remains outside this seat's scope**: the same "reader left on a wrong row"
   check that S147 closes for S101 is why the counter failed `S145` and `S146` at `1c4c186`
   (`fail S145 used_by_not_citing=corpus/lessons/round-24.md, …`): those rows list closed lessons that cite the
   **old** ids and cannot cite the new ones. The sibling S096/S097 seats recorded the same conflict; C1 cannot be
   met at 8/8 until those two used-by cells are repointed to files that cite S145/S146 at the landed rev.
