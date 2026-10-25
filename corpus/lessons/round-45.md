# Round 45 lesson

author: `L1Mori45.ScribeLesson` (round-45 wave 1, scribe seat). Seats this lane
dispatched are still the lane, not a non-author reviewer; no outside spot-check
of this round's gate decisions is on record at write time, so the `disagree`
half of LEARNING's discernment check is not claimed here.

Inherited: nothing. `corpus/lessons/round-45.md` did not exist at the entering
tip (`ls` → "No such file or directory"); this is its first write. Entering tip
`554ff416459c92f0dea9762f834a556df2990187` (contract), measured tip
`3ad8faaa637ae466c61f9427fea1c208bf49ea82`; the worktree at write time held only
untracked artifacts — `.ufo/waves/round-45/`, the round's new
`corpus/knowledge/census-cgroup-levels-r45.md`, and this lesson
(`git status --porcelain`). Seat reports landed mid-write
(`RevengerAuditorHistory.md`, `ExecWitnesses.md`, `ScribeQuarantine.md`,
`ExecRegistryAuditor.md`, `ExecCollisionGuard.md`, `PlanDataWalk.md`,
`ScoutKernelDoc.md`, `ScoutS472.md`, `ScribeRows.md`); `RevAudit.md` was still
absent, so the reviewer
measurements the L1 relayed are cited from that seat's scratch receipts
(`tmp/RevAudit/v2-bypass-probes.txt`), not from a report. No seat verdict below
is quoted from prose alone, and none is invented.

## Sources

Every fetch is this seat's own `curl -sS -L --max-time 40` unless marked
seat-opened; **all were opened on 2026-10-25**; `sha256` is of the saved bytes;
`fetched-at` is file mtime in local `-03:00` (the shell's `date -u` reads ~3 h
ahead of the mtimes, so the lane's local receipts and these mtimes are the same
clock).

| route | fetched-at | status / type | bytes | sha256 | located quote, location, words | verdict |
|---|---|---|---|---|---|---|
| `https://cdn.jsdelivr.net/gh/torvalds/linux@v7.2/Documentation/admin-guide/cgroup-v2.rst` | 07:42:13 | 200 `application/octet-stream` | 133236 | `a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad` | "all fields in this file are hierarchical and the file modified event can be generated due to an event down the hierarchy." `:1474-1476`, 22 w; "For the local events at the cgroup level see memory.events.local." `:1476-1477`, 10 w; "Similar to memory.events but the fields in the file are local to the cgroup i.e. not hierarchical." `:1518-1519`, 17 w | **admitted S473** |
| same document, `https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst` | 07:42:13 | 200 `text/plain; charset=utf-8` | 133236 | `a9433bb0…6b7ad` (identical) | — | route, not a second source |
| same document, `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/admin-guide/cgroup-v2.rst?h=v7.2` | 07:42:14 | 200 `text/plain; charset=UTF-8` | 133236 | `a9433bb0…6b7ad` (identical) | — | route, not a second source |
| `elixir.bootlin.com` HTML render (seat-opened: `tmp/ScoutKernelDoc/elixir.html`; URL not recorded in the scratch name) | 07:42 | seat-opened copy, status not re-checked | 3157249 | `88dca0d9a960d1bb6ca6481f79d84d72b89535fd903db0c5efbb4159e686066d` | not used: a render, so `.rst` line numbers do not travel into it | route only |
| `https://man.archlinux.org/man/proc.5.zh_TW` | 07:42:16 | 200 `text/html; charset=utf-8` | 61889 | `b8ede81db8d462b46f5312b392caab7c5fe8d125057ca6093c2d3152efba8be7` | 「該檔案儲存了程序的完整命令列. 如果該程序已經被交換出記憶體, 或者該程序已經僵死, 那麼就沒有任何東西在該檔案裡, 這時候對該檔案的讀操作將返回零個字元.」 entity-decoded lines `:91-98`, 74 non-space chars | **re-opened** (S472, admitted round 44; not re-admitted) |
| `https://doi.org/10.1145/3643916.3644413` → `https://dl.acm.org/doi/10.1145/3643916.3644413` | 07:42:16 | **403** `text/html` | 5471 | `19e1e728cc8f452da0d488829d92b8d4b5bcdd2295c742d6d47911b7d63200f8` | body opens `<title>Just a moment...</title>` — a Cloudflare interstitial, not the article | refused at the publisher (S244) |
| `https://arxiv.org/abs/2403.18832` | 07:42:16 | 200 `text/html; charset=utf-8` | 41919 | `2f302c3cb6c055452cd81d708e1e071b9fc9264681e550724e5a5d90cb771bb4` | title: "Rationale Dataset and Analysis for the Commit Messages of the Linux Kernel Out-of-Memory Killer" | companion (S244) |
| `https://arxiv.org/pdf/2403.18832` (text via `pdftotext`, no `-layout`) | 07:49 | 200 `application/pdf` | 1420568 | `ab8ab19551fb3614307b818e48b49885eca6f8af933b9eddfde8a18e6bf6018e` | "We find that 98.9% of commits in our dataset contain sentences with rationale information" — extracted text `:29-30`, 14 w | **`quote-present`** (S244 carrier) |
| `https://doi.org/10.1109/TSC.2026.3698682` → `https://ieeexplore.ieee.org/document/11540439/` | 07:42:16 | **202** `text/html` | **0** | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty) | none served | refused (S262, S268) |
| `https://api.openalex.org/works/doi:10.1109/TSC.2026.3698682` | 07:42:16 | 200 `application/json` | 67270 | `43beb85ed970e371ab747a633296ff2906d920ef9431300ac4850fa4b40a973f` | reconstructed abstract, words `52-68`, 16 w: "leave behind unreclaimed shared resources, such as POSIX/SysV shared memory, message queues, semaphores, and tmpfs files." | companion; S262 row's declared anchor |
| `https://api.openalex.org/works/doi:10.1145/3643916.3644413` | 07:42:16 | 200 `application/json` | 15977 | `b5090cd7020463e84d874aa244edc348fb524e9d9eee4574e6a37e6ecc463359` | title read; no quote taken | companion; no quote |

Two byte facts a reader needs. (a) **The same OpenAlex JSON hashed differently
across two fetches on the same day**: mine is `43beb85e…`, the quarantine seat's
is `f757c4a6…`, both 67270 bytes (its URL form is not in its table). A digest
anchor on a JSON API must therefore be paired with a content check, not used
alone. (b) **A route claim is not a measurement**: the wave item asserted
"`raw.githubusercontent.com` returns HTTP 429 and `git.kernel.org` serves a bot
wall" (`w1-spec.json`, `ScoutKernelDoc`). Both returned 200 with bytes identical
to the jsdelivr copy, and the seat's scratch holds **four** 133236-byte copies —
`{cgroup-v2,raw-gh,gko,gitlab-mirror}.rst` — all `a9433bb0…6b7ad`
(`tmp/ScoutKernelDoc/`, 07:41-07:42). The round records **no failed route** on
the kernel doc; the only bot walls measured are the ACM/Cloudflare 403 above and
the S268 PDF endpoints (418/15410, per `ScribeQuarantine.md`).

## Gate

Admit, one: **the level-naming theme, re-grounded** —
`corpus/knowledge/census-cgroup-levels-r45.md` (122 lines, mtime 07:44), whose
`source:` is S473, `verified-at: 2026-10-25`, `coverage-map: FR1, FR12`. The
source grounds the two levels by name (`:1474-1477`, `:1518-1519`). The entry's
new ground is narrow and measured: on the fallback branch `local_oom_kill` is
filled from the *service's hierarchical* `memory.events` while keeping the word
"local" (`tools/mori-census.sh:1708-1711`, `:1862`). Not new, and recorded as
such: `surfaces-r7.md:88-90` already holds the two counters, and
`oom-kill-counter-kernel-only-r12.md:12` already holds the local-vs-hierarchical
distinction (from S002). The staged entries' theme was adopted; their `file://`
sources were not. At write time the S473 row was **not yet in the register**
(`grep -c 'S473' corpus/SOURCES.md` → 0; the L1 appends `ScribeRows.md`'s row).

Reject, from the assimilation set:

- `who-sets-the-scope-cap-r45.md` — refuse: its "who" answer rests on `source:
  S528 — file:///…/lanes/mori/round8/.deepresearch/notes/r8-cap-run-who-sets-
  the-cap.txt` (own-work), and its second source S530 is an upstream *issue*
  statement that grounds only "the runtime caps nothing", not who sets the cap;
  the answer it reaches is a kumitate-owned runner (`cap-run.mjs`), adjacent-lane
  material the lane may read and report but not own. Flip: a public, re-openable
  ground for the same sentence (the runner source at a pinned commit, read-only,
  or `systemd.resource-control(5)` for the directive), with the claim stated as a
  reading of the caller's parameter and no policy for the owner.
- `cap-control-wording-r52.md` — refuse: it is an argument for a change
  (`MemoryHigh=` on the kumitate runner). Its own Limits section says "It does
  not choose for the owner… that is the kumitate lane's decision", but the body
  still concludes "Adding `MemoryHigh=`… changes what the fleet's kills mean";
  `PROVINCE.md` is "Detection and report only — never remediation", and the
  quoted semantics are the systemd manual's. Flip: a documentation-only entry
  (the two directives' semantics, no recommendation), opened from the manual
  alone, plus a committed read-only receipt of what the runner sets — a
  measurement, not a proposal.
- The two `file://`-only staged rows were **not adopted**: `S558`
  (`cgroup-surface-two-levels-r49.md:3`) and `S559`
  (`selftest-cannot-tell-levels-r49.md:3`) both cite `file:///…/lanes/mori/
  round12/.deepresearch/notes/r12-census-two-levels.txt` — the campaign's own
  notes. Their claims survive only where the round re-measured them from the
  lane's bytes; the entry cites `tools/mori-census.sh:3252-3254` and `:3906`,
  not the note.

## Quarantine

Slice from the campaign's absent-defect register
(`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`,
read-only; all 109 id cells of the never-checked table are malformed, `S244\``
not `S244 |`, so the slice was derived by pattern, `assimilation/quarantine-slice`).
Each row's class is "the cited source could not be fetched, so no quote was
checked". Two of the three have **no row in `corpus/SOURCES.md` in any commit**
(`git log --oneline -S'S244' -- corpus/SOURCES.md` → 0; same for `S268`); their
row content is staged (`merge/mori/SOURCES.append.md:19` = `S483`,
`:43` = `S507`). S262 is the one lane row (`corpus/SOURCES.md:243`).

| id | register line + cited URL | lane / staged row | re-fetch | verdict |
|---|---|---|---|---|
| S244 | `:356` — `https://doi.org/10.1145/3643916.3644413` | no lane row; staged `S483`, whose `used-by` `kernel-oom-line-attribution-r12.md` exists but references neither the DOI, the arXiv id, nor `98.9%` (`grep -cE '3643916\|2403\.18832\|98\.9%'` → 0) | publisher 403/5471 B (Cloudflare); **PDF carrier 200/1420568 B**, quote located `:29-30` | **`quote-present`** — the span is in the row's own declared carrier; the publisher endpoint stays unreadable |
| S262 | `:357` — `https://doi.org/10.1109/TSC.2026.3698682` | lane `SOURCES.md:243`, anchor = the OpenAlex record, `used-by corpus/knowledge/oom-victim-context-r41.md` (`grep -c 'S262'` → 9) | publisher 202/0 B; OpenAlex 200/67270 serves the abstract | **`quote-present`** — words `52-68` of the reconstructed abstract; the publisher endpoint itself unreadable |
| S268 | `:358` — same DOI | no lane row; staged `S507`, whose `used-by` `corpus/knowledge/oom-tracing-tracepoints-r42.md` **does not exist** (`ls` → absent) | publisher 202/0 B; every PDF endpoint 418/15410 or "Full text not available" (quarantine seat) | `unverifiable` — the full-text span (`mark_victim`, …) is in no carrier this host can fetch today. **Not fabrication.** |

`unreachable` is not a fabrication verdict: the register's own class text says a
quote *was not checked*, and the census agrees — its three mori findings are
`fetch-failed` with no `quote` key. Totals, read correctly: the register header
prints **194** rows with an absent quote and **324** absent quotes; its two
tables hold **194 + 109 = 303** flagged rows over 19 lanes (`## By lane` sums to
194 and omits the never-checked table). The census behind it (`quote-lint-full-
v5.json`) counted 1901 rows, 4152 quotes, 78 `fetch_failed`; this slice is 3 of
the 109 never-checked rows, not 3 of the 194 absent ones. The carrier is
intermittent — the S268 PDF was a 200 on 2026-10-24 (`round-42/w1/RevRefusal.md`)
and 418 today — so an `unreachable` verdict must carry the date it was measured,
and this one carries 2026-10-25.

## Renumber

Own run at the write tip (245 registry ids, 136 staged ids, staged tail `S606`):
`comm -12 reg-ids staged-ids` → **2 collisions, `S471` and `S472`** — the same
two ids as round 44, now `assimilation/{reg-ids,staged-ids,collisions}`. The
lane's ids stand (append-only); the staged ids are **shadowed by document**:

| id | lane document (kept) | staged document (shadowed) |
|---|---|---|
| S471 | proc(5) 日本語訳, `manpages.ubuntu.com/manpages/focal/ja/man5/proc.5.html` | gihyo.jp article 0061, cgroup v2 memory controller (6) |
| S472 | proc(5) 中文翻譯, `man.archlinux.org/man/proc.5.zh_TW` | gihyo.jp article 0056, cgroup v2 memory controller (1) |

`assimilation/renumber-map.tsv` is 162 lines: 26 comment lines, then 136
mapping rows from `:27` (`S471→S474`) to `:162` (`S606→S609`) — a +3 offset
because **`S473` is reserved for this round's own admitted row** (`:10-14`;
`census-cgroup-levels-r45.md:3`). It is a routing table, not an arithmetic
transform: **citations are re-pointed by document** (URL and anchor are the
evidence; the id follows it), so an adopted row keeps its lane id where one
exists and takes the next free id only where it does not. The map I read at
07:47 was a 136-line file with no comments whose line 1 mapped `S471→S473`;
the delivered map reserves that id and opens at `S474`. That intermediate state
is M8, and it is closed in the delivered bytes — the reservation is what
produced the offset, and it is not a derivation from the offset.

Row arithmetic for the C2 audit (the L1's numbers, both re-derived here):
the C2 population is **36** at the entering tip and **39** at the landed tip
(33 `tools/*.py|sh` + 3 round-44 counters + 3 round-45 counters, per
`PlanDataWalk.md`); the registry now holds **7** eight-cell tables — `SKILL.md`
headers at `:162, :524, :588, :643, :718, :796, :881` — with **43** rows
(23 + 2 + 1 + 2 + 3 + 1 + 11), of which the `## Gates` table's 23 are the only
ones v1 reads. Round 44 called this "six secondary tables plus `## Gates`";
the count is unchanged, the under-read is 20 rows wide.

## Mistakes

| id | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M1 | the round-44 auditor under-read the registry (`## Gates`' first table only) and credited a `--selftest` that occurs inside a **comment** | tool `tools/mori-gate-registry.py` at `7cb59c68`: `parse_gate_table` `:81-95` (docstring "Rows of the `## Gates` table" `:82`; `break` on the next `## ` `:94-95`), substring fallback `:124-126`, `unregistered` verdict `:128`, byte test `:146`. Report `w1/ExecGateInventory.md:19, :29, :44` (PASS — "FALSE POSITIVE"), `:65-67` (18 PASS contains 1 false positive), `:91-92` (prose claims "a real `--selftest` argv branch"), `:114-117` (PASS only because the bytes contain the literal in comments). Observed on three shadowed tools: `w1/RevengerAuditorHistory.md:141-143` (`--audit mori-blind-check.sh\|mori-source-drift.py\|mori-pressure.py` → "unregistered", rc 1, rows exist at `:796/:881/:643`). Tool side: in the committed bytes at `7cb59c68`, `git show 7cb59c68:tools/mori-silence-cases.sh \| grep -n -- '--selftest'` → **one** hit, `:20`, a comment (`git log -S'--selftest'` → one commit, `3da84149`); the worktree file gained a real `--selftest` argv branch **during this wave** (`git diff` → `case "${1:-}" in --selftest) SELFTEST=1`), so that row is no longer the live defect — this M1 is about the bytes the round-44 audit read | **none** — QUALITY 118's check is that same auditor (`corpus/QUALITY.md:958-971`), and its "Not covered" names duplicate rows, absent paths and nine-cell rows, not the comment arm | P-C2 item 4 + the C2 kill rule. Proof it can fail: (a) v1 — a scratch repo with an 8-cell row and a comment-only tool prints `PASS (row 'fixture gate': 8 cells, entry resolves, --selftest present)` / `REGISTRY=met`, rc 0; (b) v2 — the three probes M3/M4/M5 below, all on the round's own draft |
| M2 | the round-44 ledger counter accepted revision-constant rows **and** rows that read `HEAD` while merely containing `@REV@` | `w1/MutC1.md:33` (`SURVIVED (C1=met)`), `:93-104`, `:286-287` ("`@REV@` presence is textual, not semantic"); `w1/ExecWitnesses.md:120-127` — the **unmodified** r44 counter scores `w-revconst`, `w-head` and `w-dup` all `C1=met mismatches=0`, rc 0 | QUALITY 117 "Not covered" (`corpus/QUALITY.md:943-957`) — disclosed, but its check cannot catch it | P-C1 rule 1 + witnesses. **Observed fixed**: `.ufo/waves/round-45/count-c1.py` requires `--other-rev` and `--witness-dir` for `C1=met` (`:32-36`), `check_witnesses` `:396-437`, and its selftest prints `C1_SELFTEST pass=10 fail=0`, rc 0, including `head_reading_row_rejected`, `revision_constant_row_rejected`, `witness_dir_one_passing_witness` (this seat, at the write tip). Independent repro of the defect: a 12-row ledger — 8 `git diff @REV@ @REV@ --stat \| wc -l` asserted 0, 4 `git show HEAD:data.txt \| grep -c x # @REV@` asserted 5 — at rev `710e313c` (3 lines) with HEAD `cb742247` (5 lines) prints `C1=met mismatches=0` under the r44 counter. The full `C1=met` run still awaits `figures.tsv` (absent at write time) |
| M3 | v2's item-4 rule accepts a `--selftest` that appears only inside **another argument's `help=` string** | `tmp/RevAudit/v2-bypass-probes.txt:4-13` — E4, repo `repos/e4-help-string`, rev `222741d0`: `PASS … (8 cells, entry resolves, --selftest argv branch)`, `no_selftest=0`, `REGISTRY=met`, rc 0; fixture body `fixtures.py:212-226` (`add_argument("--verbose", …, help="see --selftest for the test suite")`) | **none** | round 46: require the flag as a parser key (`add_argument("--selftest"`) or a `case` pattern, never inside a string literal. Proof it can fail: the E4 body is the input the current rule accepts, so a keyed rule turns it red while `--audit` on a real branch stays green |
| M4 | the documented `selftest-flag=` escape can be pointed at `--help` | `v2-bypass-probes.txt:15-24` — E5, rev `7b3195ec`: row cell `bash tools/fixture-tool.sh --help` + `selftest-flag: --help`, tool's only branch `--help) echo "usage: fixture"` (`fixtures.py:232-245`), prints `PASS … --help argv branch`, `REGISTRY=met`, rc 0 | **none** | round 46: the escape must name a flag that produces a pass/fail tally token. Proof: the same fixture must go red; it is one cell and one branch, nothing else changes |
| M5 | the v2 branch marker is too **narrow**: a genuine `--selftest` branch whose argv is a named parameter is rejected | `v2-bypass-probes.txt:26-35` — E6, rev `aa6838ab`: `FAIL … tool has no real --selftest argv branch`, `no_selftest=1`, `REGISTRY=unmet`, rc 1; fixture `fixtures.py:246-262` | **none** | round 46: widen the window to the `case` pattern / `sys.argv` membership. Proof: E6 must pass while E4/E5 fail — the three probes together are the falsifier set |
| M6 | the v1 positive control encodes the defect it is meant to close | `tmp/RevAudit/aud-v1.py:188` — `tool_ok = "#!/bin/sh\n# --selftest mode\n"`, the "good" fixture's only occurrence is a comment; `:146` the byte test; `fixtures.py:199-208` (S4 expects `no_selftest`, notes "v1 passes: b'--selftest' present") | **none** | make the good fixture carry a real argv branch and make S4 failing. Proof: the M1 run accepts a comment-only tool today, so a fail-closed S4 turns the tally red — the fixture is the control, not the prose |
| M7 | the wave item asserted two failed routes as fact | `w1-spec.json` (`ScoutKernelDoc`: "429" and "bot wall"); this seat's GETs both 200/133236/`a9433bb0…`; seat scratch holds four identical copies (`tmp/ScoutKernelDoc/`) | **none** | a route claim in a wave item carries its receipt or is phrased as a hypothesis. Proof: the digests contradict the premise |
| M8 | a **draft** `renumber-map.tsv` mapped its first staged row to `S473`, the id this round's own admitted row occupies | draft as read at 07:47: 136 lines, no comments, line 1 `S471→S473`; delivered map: `:27` `S471→S474`, `:162` `S606→S609`, with `S473` reserved (`:10-14`); the entry's `source: S473` (`census-cgroup-levels-r45.md:3`); `grep -c 'S473' corpus/SOURCES.md` → 0 at write time | the census executor's cross-check (`ExecAssimCensus`), relayed by the L1 after this lesson's first draft | reserve every id named by the round's own admitted rows before computing the map — **applied in the delivered map**. Proof: delivered `:27` reaches `S474`, so no target equals the entry's `source:` id; the draft's line 1 did. The +3 offset is the reservation, not an arithmetic derivation — citations are re-pointed by document |
| M9 | the quarantine item says "read the row in `corpus/SOURCES.md`" for two ids that file never held | 245 id cells, `grep -nE '^\| S(244\|268) \|'` → rc 1; `git log -S'S244' -- corpus/SOURCES.md` → 0 commits; the rows live in the register and the staging append (`S483`/`S507`) | **none** | the slice file carries the register's URL cell; the item must say "the lane row if it exists, else the staged/register row", and a slice derived from a campaign register must not be described as reading the lane registry. Proof: the rc-1 grep and the empty `-S` history |
| M10 | a count in the round-44 audit's prose was not re-derived from its own grep | `w1/ExecGateInventory.md:114-117` says "in two comments"; on the committed bytes `git show 7cb59c68:tools/mori-silence-cases.sh \| grep -n -- '--selftest'` → **1** hit (`:20`); the second hit in the file is the bare token `selftest` at `:290` | QUALITY 117 in principle; not applied to the audit's own prose | derive the count with the grep that is cited, in the same receipt. Proof: grep says 1, the prose says 2 |
| M11 | four round-44 write-scope cells are false under an inherited `GIT_DIR`, and the round-44 verifier's clean-env hash marked them ✓ | `w1/RevengerAuditorHistory.md:278-296` (cells at `SKILL.md:183-186`, verbatim), `:327-331` (`GIT_DIR=… python3 tools/mori-gate-registry.py --selftest` writes into the foreign repo; registry +6, c1 +6, c2 +35, c3 +6 commits, every selftest still green). Count correction: F8 names **four** cells (`183–186`), not two; the silence-oracle cell `:166` (`temp fixtures`) was **not** named by F8 and is true as written | **none** | round 46: a write-scope cell is a claim about the instrument's writes under any environment; the selftest must scrub `GIT_*` (or the cell must say "inherits the caller's git environment"). Proof: Revenger's four observed commit totals under `GIT_DIR`; not re-run by this seat |

**Post-freeze correction observed mid-write.** `contract.md` grew 28 lines while
this lesson was being written: `Correction 1` (`:111-137`) appends — it does not
rewrite — and closes four holes, of which two bear on this lesson's numbers:
`tables>=7` for C2 (`:126`) is exactly the seven-table count measured in
Renumber above, so the v1 under-read is now a predicate violation rather than a
reader preference; and `moved>=1` for C1 (`:121`) is the M2 class in predicate
form. The worktree also gained modified tracked files from other seats during
the write (`git diff --stat`: `tools/mori-gate-registry.py` +747,
`mori-routed-r24.py` +588, `mori-routed-check.py` +314,
`mori-round19-regressions.py` +313, `mori-disk-rate.py` +206,
`mori-silence-cases.sh` +168, `mori-round41-calibration.py` +16, `contract.md`
+28). Every tool line number in this lesson names the committed bytes at
`7cb59c68` (v1) or a scratch draft under `tmp/RevAudit/`; none names the
post-edit worktree file, so a reader re-checking against the worktree must
expect different line numbers — and the `mori-silence-cases.sh` line has already
moved from `:20` to `:27`.

M1-M5 are the round's load-bearing mistakes. The frozen C2 item 4 says only "a
real argv branch", and the three probes (M3, M4, M5) show the rule that tries to
implement it both over-accepts (a help string, an `--help` escape) and
under-accepts (a named-parameter branch). The contract's kill rule is therefore
necessary but not sufficient until the rule is keyed on parser keys and `case`
patterns. M2 is the one mistake whose fix is observed in this round's bytes; M1's
fix exists but fails its own probes as of the last read. M11 is the only one whose
evidence is a seat's measurement this seat did not re-run, and it is labelled as
such.

## Carrier

The round's new instruments see a ledger's revision sensitivity and uniqueness
(C1), a row's presence, attribution and (once keyed correctly) argv branch (C2),
and an entry's `used-by` plus census (C3) — but none reads the prose a figure was
transcribed from or the carrier a quote came from, so an admissible, attributed,
census-green row that counts the wrong thing, or cites a span only its own
companion serves, still passes all three.
