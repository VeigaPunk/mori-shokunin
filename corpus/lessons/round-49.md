# Round 49 lesson

Entering tip `b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86`; freeze `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115` (contract
`.ufo/waves/round-49/contract.md`, both counters, controls, receipts, the four source copies). Claims: C1 calibration
(the pin reconciler reads what a reader sees, scored by `count-c1.py` with opaque handles, 18 junk and 7 honest edits),
C2 depth (journal retention-reach entry, every claim a located quote, scored by `count-c2.py`). Wave-1 seat reports:
`.ufo/waves/round-49/w1/` (48 of 49 reports on disk when this lesson was written). **No wave 2 ran** (see Wave 1 below).

## Gate

### New SOURCES rows (each opened this round; rule 1)

Four rows, all opened 2026-10-25 by the row scribes (`w1/Mo49ScribeRow{Conf,Ctl,Svc,Host}.md`) and written into
`corpus/SOURCES.md` by the L1 (S485–S488, after S484). The quote column is each row's located quote with its
location (CORPUS.md, "a quote names its location"); each also locates under `count-c2.py`'s `normalise()`. The three pages were
copied at the freeze `0df17b7b` and every copy matches its `count-c2.py` pin — `sha256sum
corpus/evidence/sources-r49/*` → `b4a9b53e…` `journald.conf.5.html`, `75440570…` `journalctl.1.html`,
`a7b44356…` `systemd-journald.service.8.html`, `be3952cb…` `host-journal-reach.txt`, rc 0 — so the rows are
grounded in bytes this lane holds, not in a live page.

| id | URL / locator | accessed | ≤25-word located quote | decision |
|---|---|---|---|---|
| S485 | https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html — copy `journald.conf.5.html` | 2026-10-25 | "Also note that only archived files are deleted to reduce the space occupied by journal files." (16 words) — §Options, `SystemMaxUse=` entry | admit, mined, kind docs, tier A for the retention options only, recheck 180d |
| S486 | https://www.freedesktop.org/software/systemd/man/latest/journalctl.html — copy `journalctl.1.html` | 2026-10-25 | "--vacuum-size= removes the oldest archived journal files until the disk space they use falls below the specified size" (18 words) — §Commands, `--vacuum-size=` entry | admit, mined, tier A, recheck 180d; `teaches` opens `supersedes S351 —`; scope text differs from S014's (cursor/field selection) and S470's (`--disk-usage` total) |
| S487 | https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.service.html — copy `systemd-journald.service.8.html` | 2026-10-25 | "systemd-journald will automatically remove the oldest archived journal files to limit disk use" (13 words) — §Files, `/var/log/journal` entry; the storage paragraph sentence "The journal service stores log data either persistently below /var/log/journal or in a volatile way below /run/log/journal/" (17 words) is in §Description | admit, mined, tier A, recheck 180d |
| S488 | own-work: host-journal-reach — `corpus/evidence/sources-r49/host-journal-reach.txt` | 2026-10-25 (receipt captured 2026-10-25T20:43:09-03:00) | "Archived and active journals take up 56M in the file system." (11 words) — receipt line 5, under `$ journalctl --disk-usage` | admit, mined, kind own-work, tier A scoped to this host on 2026-10-25, recheck 90d; the token `own-work: host-journal-reach` appears verbatim in the source cell, because `count-c2.py` matches the URL key on those words |

Every row carries the three fields `count-c2.py` reads — status `mined`, opened `2026-10-25`, and
`corpus/knowledge/journal-reach-r49.md` in `used-by` — plus one of the four frozen URLs in its source
cell (an 11-cell row, `srow[7]`, `srow[8]`, `srow[10]`; the counter's `sources_row()`).

Changed in place (rule 2), old → new: none. S351 (`journalctl(1)`, `rejected`) is **not** edited:
the contract keeps the rejection and records the flip in the successor row, so rule 2's status change is
not used. Rule 1 is met by four rows opened in this round, each with a committed copy and a located quote.

The four lane ids S485–S488 coincide numerically with four **staged** ids for unrelated documents (staged
S485 MaxCompute 作业洞察, S486 MaxCompute Logview, S487 CPFS 配额管理, S488 CloudMonitor 告警规则). Those
staged rows are not appended, so no id rule is broken; the collision guard does not see this because it
compares the registry with the staged set, not the two documents behind one number. Stated here so a reader
of `SOURCES.append.md` does not take lane S485 for staged S485.

### Assimilation (addendum §10) — theme FR1, journal retention reach

Package `/home/vgpnk/Projects/shokuknow/merge/mori/` read only; no campaign tool run; nothing written there.
The package states 136 proposed rows (first id S471) and 80 proposed entries. The adopt checklist in
`MERGE-REPORT.md` is not followed, for the reasons round 48 already recorded and this round re-checks:
step 1 names a `SOURCES-PROPOSED.md` the package does not contain (`ls` lists only `MERGE-REPORT.md`,
`MERGE-REPORT.json`, `SOURCES.append.md`, `amendments/`, `knowledge/`); step 3's bulk append would import
every staged id, 14 of which the lane now holds (S471–S484); step 4 would add 80 entries against §10's
1–3 entry cap. One theme, one entry, four rows renumbered by document.

- **Candidates considered** (five staged entries, six staged rows). All five entries are in the FR1 theme
  and all five cite an own-work `file:///home/vgpnk/Projects/shokuknow/lanes/mori/round{8,9,10,11}/…`
  receipt. Those notes exist (1761 / 1529 / 1275 / 1088 bytes) and were read-only — the lane's own rule,
  written into S351's rejection, is that a shokuknow note is not lane evidence, so their numbers are not
  adopted whatever they say. Their public-page halves do hold: the four sentences the entries attribute to
  `journalctl(1)` and `systemd-journald.service(8)` all locate in the committed copies under
  `count-c2.py`'s `normalise()` (18, 6, 14 and 23 words; substring test, rc 0). So the theme was rejected
  for provenance and duplication, not for fabrication.

  | staged entry | rows | what it claims | verdict |
  |---|---|---|---|
  | `journal-effective-retention-r45.md` | S524 | the daemon's own effective limits, the drop-in that sets them, and "this host's store is at its ceiling" | reject as an entry; its rule half is rewritten (below) |
  | `journal-reach-at-ceiling-r46.md` | S532, S537 | the reach shrinks from the oldest end **by size**, and this host is over its ceiling with counter = journal count | reject as an entry; the vacuum-order rule is adopted through S486 |
  | `runtime-journal-reach-is-the-boot-r49.md` | S560 | the runtime journal is bounded by the boot, not by its 64M ceiling | reject as an entry; the boot-bound rule is adopted through S487 |
  | `reach-is-per-journal-r47.md` | S544 | the reach is a property of a journal, not of a host; only one host is measurable from this seat | reject (host numbers from another capture; the "uniform rule" clause is unsupported) |
  | `reach-per-journal-second-instance-r48.md` | S554 | the second journal's ceiling is 64M and its reach is nothing at all | reject (own capture; S554 is outside this round's row list; see below) |

- **Collision check** (before any append; `assimilation/{reg-ids,staged-ids,collisions}`): registry 257 ids,
  staged 136 ids → **14 collisions `S471 S472 S473 S474 S475 S476 S477 S478 S479 S480 S481 S482 S483 S484`**
  for the whole package, reproducible from the two committed id lists
  (`comm -12 <(sort reg-ids) <(sort staged-ids)` → those 14, rc 0), and the committed `reg-ids` is itself
  identical to the ids re-derived from `git show b3e3453d:corpus/SOURCES.md` under the 0–3-space pattern
  (257 ids, `diff` empty). None of the candidate rows collides: `grep -cx` of each of S516, S524, S532,
  S537, S544, S560 against `reg-ids` → `0` (and S554 → `0`). The three rows adopted by document (S516,
  S532, S560) are collision-free.
- **0–3-space guard proof** (the pattern the census and the id lists share): on a scratch fixture of four
  rows, `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` → `3` and `grep -cE '^\|[[:space:]]*S[0-9]{3,}'` → `1`;
  the ids seen are `S002 S002 S003`, so `  | S002 |` and `   | S003 |` are rows, while `    | S002 |` is
  indented code and is skipped. An indented row therefore cannot hide from the collision check, and a code
  block cannot manufacture an id.
- **Renumber by document** (the URL is the evidence, the id follows it; no staged id is kept):
  staged S516 `journald.conf(5)` → lane **S485**; staged S532 `journalctl(1)` → **S486**; staged S560
  `systemd-journald.service(8)` → **S487**; this round's own host receipt has no staged id and becomes
  **S488**. The staged own-work rows S524, S537, S544 (and S554, used by the fifth entry) are not adopted
  and get no lane id; this round's receipt replaces them.
- **Admit:** one rewritten entry, `corpus/knowledge/journal-reach-r49.md`, replacing the five staged
  entries with one claims table grounded in S485–S488. The staged entries overstate in ways the committed
  copies correct, and the entry must not inherit them:
  - "at that ceiling and evicting" (r45) — its own figure 250.3M sits **under** the 256M ceiling and no
    vacuum is shown; r46 later reports 258.3M, a different minute, from a receipt the lane cannot read.
  - "already over its ceiling" (r46) is a number from that outside capture, not a lane fact; this round's
    receipt reads a 56M store against the same 256M drop-in (`--disk-usage`, rc 0).
  - "2215 times the subtree came within reach of a limit boundary" (r46) is the entry's own gloss on a
    `memory.events` counter whose semantics it does not cite.
  - "two journals … reaches of six boots and none" (r47, r48) understates what the receipt shows: the
    `--disk-usage` total of 56M decomposes into `--system` 19M and `--user` 37M, the volatile store is
    empty, and `--list-boots` lists **two** boots, not six. Whatever the entry says about stores must
    name the stores the receipt actually reads.
  - "The ceiling is not the documented default" (r45) is correct and was left unquoted there; the
    committed `journald.conf(5)` copy carries the default in one sentence — "The first pair defaults to
    10% and the second to 15% of the size of the respective file system, but each of the calculated
    default values is capped to 4G." — so S485 grounds it.
- **Reject, with flip:**
  - staged own-work rows **S524, S537, S544** (and **S554**, which the seat's row list omitted and the
    fifth entry cites as its only source): the pointer is a `file://` note under
    `/home/vgpnk/Projects/shokuknow/lanes/mori/roundN/.deepresearch/notes/`, outside this lane. Flip: copy
    the note into `corpus/evidence/sources-r49/` (as this round did for the host receipt), pin its sha256
    in the row, and cite the command headings and capture time. The receipt is evidence; a path into
    another repo's tree is a lead.
  - staged `reach-is-per-journal-r47.md` and `reach-per-journal-second-instance-r48.md`: every number is
    from another capture (six boots, 64M, "no records"), one `ls` at one moment is treated as a reach, and
    r47's "the rule that produces it is uniform" has no support — two stores on one host cannot show a
    rule to be uniform. Flip: re-measure both stores on this host with a committed read-only receipt, name
    which stores exist, and state the unit claim from that receipt.
  - staged `runtime-journal-reach-is-the-boot-r49.md` as an entry: its host half is asserted, not quoted,
    and its recheck command lists `/run/log/journal/<machine-id>` while this round's receipt lists
    `/run/log/journal` (the parent, empty, rc 0) — the two commands do not measure the same directory.
    Flip: run both commands on this host, cite the receipt line, and say which directory was listed.
  - staged `journal-effective-retention-r45.md` and `journal-reach-at-ceiling-r46.md` as entries: the
    overclaims listed under **Admit** above. Flip: keep the rule, drop the outside numbers, cite the
    committed page for the default, and state the ceiling relation without "evicting" unless the store is
    over it.
  - the S351 flip, and how far it is met: S351's flip text reads "the public `--vacuum-size=` sentence
    plus a committed read-only disk-usage receipt, and no MESSAGE grep". Two of three elements are met —
    the `--vacuum-size=` sentence is in the committed copy (18 words, located) and
    `corpus/evidence/sources-r49/host-journal-reach.txt` is a committed receipt whose `journalctl
    --disk-usage` exits 0 — and the third is **not** met literally: the receipt obtains the daemon's two
    limit lines with `journalctl -q -g 'Journal .* is .*max'`, and the committed `journalctl(1)` copy
    defines that option as "Filter output to entries where the MESSAGE= field matches the specified
    regular expression" (located). Under the narrow reading of S351 (no kernel MESSAGE grep for kill
    records) the flip is met; under the literal reading it is not. S486's `teaches` must therefore say
    which reading it satisfies, or the entry must lean on the non-MESSAGE lines only (`--disk-usage`,
    `--system`, `--user`, `--list-boots`, `cat-config`, `findmnt`, `ls`). S351 stays `rejected`.
    **Decision (L1):** the narrow reading. S486's `teaches` says "with no kernel-message grep", and
    `corpus/knowledge/journal-reach-r49.md` rests no claim row on the receipt's two `-g`-derived daemon lines
    (the 45M and 8M boot lines) and says so in its host section; the frozen receipt keeps them as captured
    (`evidence/freeze-sha256.txt` pins its bytes). The breach of the literal wording is disclosed here, not repaired.
- **Quarantine slice** (`assimilation/quarantine-slice`; register class "the cited source could not be
  fetched, so no quote was checked"): S244, S262, S268 keep their round-48 verdicts and none is cited by
  the admitted entry.
  - S244 — no lane row (`grep -cE '^ {0,3}\| *S244 *\|'` → `0`); round-48 verdict PRESENT stands.
  - S262 — a lane row (line 243, `mined`, `used-by corpus/knowledge/oom-victim-context-r41.md`); the
    round-48 verdict PRESENT and the round-41 citation predate this slice and are unchanged. It is **not**
    cited by `journal-reach-r49.md`.
  - S268 — no lane row (`0`); the round-48 verdict PRESENT stands, with its note recorded in
    `corpus/README.md:620`.
  - None of the three was appended and none was edited.
- **considerthese:** `considerthese/2026-10-25.md` suggestion 3 ("track whether in-round critic flags get
  fixed") lands twice: as the round-48 measurement carried by `w1/Mo49ExecFlaggedFixed.md`, and as QUALITY
  criterion **129** (next free; the current highest is 128). The measurement's unit and counting command:
  a *flag* is one `##`/`###`/`####` heading in a round-48 `w1/Crit*.md` or `w1/Rev*.md` that names an id
  (`F`, `D`, `P`, `J`), plus the bold `**F1 —` lines of `RevAssimPlan.md` and the named counterexample of
  `CritC2Counter.md`; the disposition is FIXED when the landing diff `git diff 4387cf94 e4dfff32` changes
  the file:line the flag names (or the flag's repro no longer holds at `e4dfff32`), else UNFIXED, and
  NOT-APPLICABLE when the flag is about a frozen instrument that may not change. Denominator measured
  here: 8 reports, 30 heading-named flags + 5 bold lines + 1 counterexample = **36 flags**
  (`grep -cE '^#{2,4} .*\b(F[0-9]{1,2}|D[0-9]{1,2}|P[0-9]|J[0-9]{1,2})\b' .ufo/waves/round-48/w1/Crit*.md
  .ufo/waves/round-48/w1/Rev*.md` → `8 0 0 6 9 3 0 4`). Disposition tally: flagged=45 fixed=18 unfixed=9 na=18 (`python3 .ufo/waves/round-49/flagged-fixed/count-flagged.py`, freeze `4387cf94` → landing `e4dfff32`; control with the freeze as landing: `flagged=45 fixed=0 unfixed=27 na=18`).
  Two dispositions are already visible in this round's frozen instruments and are the reason the criterion
  is not ceremony: `CritC2Counter.md`'s script/style class is closed — `count-c2.py` strips
  `<script>`/`<style>`/comments before matching (line 60) and its selftest arms
  `normalise_drops_script_text`, `…_style_text`, `…_comment_text` pass (`C2_SELFTEST pass=26 fail=0`) —
  and `CritC1Counter.md` F1 (a tool that keys on the harness's filename) is closed by opaque handles, with
  the sniffer control showing both directions: `junk_met=18` under this round's counter (rc 1) and
  `C1=met junk_met=0 … variants=12` under round 48's (rc 0).
- **Census forecast:** the only predicted change is one warning and no error. `journalctl.html` already
  appears under three scopes (S014, S351, S470 — `grep -cF` → `3`), so S486's fourth scope adds a `W04`
  "same URL across scopes" warning; `E04` (duplicate URL *within* a scope) does not fire because the scope
  text differs, and warnings do not affect a clean lane (`sources-census.sh:33`). The three other URLs
  appear 0 times. Expected round-end line count: 22 (21 at the start — 20 `W04` + one `ok`, rc 0).

### Spot-check

Previous outside check: `corpus/lessons/round-48-verifier-spotcheck.md` (hyaku closure, @m_sonnet). Its
routed defects and this round's disposition: 1 (`.scratch/` residue, no `.gitignore` entry) → carried and
still open (`165` untracked `.scratch/` directories at the freeze; the entry is not in `.gitignore`);
2 (report author date behind the cited tip) → carried as a landing rule; 3 (the seven v3 survivors, the
K2–K8 classes, rule R11, `CritC1Counter` F1's filename sniff) → the C1 predicate and its controls this
round; 4 (SHONEN boxes not checkable by a non-author) → operator-owned, unchanged.
Round-49 gate decisions are awaiting this round's non-author closure (LEARNING.md). Sample offered:

- **admit, re-open one:** S486 — re-open the committed `journalctl.1.html` and confirm the row's quote
  locates (the `--vacuum-size=` sentence is 18 words and was found under `count-c2.py`'s `normalise()`,
  rc 0), then check that `teaches` opens `supersedes S351 —` and that its scope text differs from S014's
  and S470's.
- **reject, re-open one:** staged `reach-per-journal-second-instance-r48.md` — re-read the entry's
  `source:` line (S554, a `file:///home/vgpnk/Projects/shokuknow/…` note) and check the claim "reaches of
  six boots and none" against this round's receipt (`--list-boots` lists two boots; the volatile store is
  empty; `--disk-usage` 56M = `--system` 19M + `--user` 37M). It is a reject on provenance and on the
  store count, not on the boot-bound rule.

## Mistakes

| id | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M1 | survivor | The round-48 C1 counter handed each variant to the tool as `--skill <scratch>/variant-J1.md … variant-H4.md` and `TMPDIR=<scratch>/c1-<variant>-…` (`.ufo/waves/round-48/count-c1.py:238,247`), so a tool that read neither `SKILL.md` nor any row printed `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12` (exit 0) by branching on the name (`.ufo/waves/round-48/w1/CritC1Counter.md:26-52`, the two channels at `:49-50`, reproducer at `:28-33`) | none — QUALITY 126's harness-leak check is tool-scoped: it "claims only that the tool doesn't exploit them", and records the harness leak itself as residual (`w2/R48RevQuality.md:71-73`) | Opaque handles in this round's frozen counter: the `SKILL.md` copy and the per-run scratch dir are a sha256 prefix of their bytes, the run order follows that hash, and runs are launched against `TMPDIR=t-<hash>` (`count-c1.py:216-221,257,274`), with selftest arm `handles_carry_no_variant_name` rejecting any handle matching `variant\|junk\|honest\|[JNH]\d\|real` (`count-c1.py:374-376`); the honest pin-moving edit H5 that F1 asked for (`w1/CritC1Counter.md:64-68`) is also in the set. **Shown able to fail**, by the sniffer pair, both opened: the name-keyed control (`controls/stub-filename-sniffer.py`, keys on `variant-[JN]\d\|c1-[JN]\d`) scores `C1=met … variants=12 rev=b3e3453d…` under the round-48 counter (`.ufo/waves/round-49/evidence/control-c1-sniffer-under-r48-counter.txt`, exit 0) and `C1=unmet junk_met=18 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d…` under this round's counter (`evidence/control-c1-stub-filename-sniffer.txt`, exit 1) — every `N*`/`J*` line `got=met`, so the control cannot reach `met` |
| M2 | landing | After round 48, `git status --porcelain` still showed 114 untracked `.scratch/{c1-*,pin-*,r48-*,r48w2-*}` directories (12/41/32/29) of seat-run debris (`corpus/lessons/round-48-verifier-spotcheck.md:20`, defects at `:23-25`, routed defect 1 at `:100`) | none — QUALITY 80 carries the pathspec `.ufo/waves/round-<N>/` (`corpus/QUALITY.md:368-372`), and `tools/mori-unlanded-check.py:15` excludes `.scratch/` "on purpose" | `.gitignore` entry plus a round-end removal (contract, "Round-48 routed defects carried"). **Not yet shown** at the entering tip: `git show b3e3453d:.gitignore` lists four entries (`.ufo/interactive-sessions/`, `.ufo/worktrees/`, `__pycache__/`, `*.pyc`) and no `.scratch`; `git diff b3e3453d -- .gitignore tools/mori-unlanded-check.py` is empty; the class has grown — `find .scratch -mindepth 1 -maxdepth 1 -type d` → 184, of which 120 carry a round-48 prefix with an mtime before the freeze commit `0df17b7b` (2026-10-25T21:36:32-03:00), the excess over the closure's 114 coming from counter-run scratch (`count-c1.py:332` makes `c1-*` under `.scratch`; `tools/mori-pin-check.py:405` makes `pin-tmp-*`) |
| M3 | landing | Round 48's filed report commit `e60eb16757781b9303b90e6d6972b2b8953d6d86` (fleet repo) has **author** date `2026-10-25T20:22:17-03:00` while it cites lane commit `14c5110d65a2f225e7316e1996e92090b9b8e7cb` authored `2026-10-25T20:26:17-03:00`; only its committer date (`20:27:04`) is after the tip (`corpus/lessons/round-48-verifier-spotcheck.md:23-26`, routed defect 2 at `:101`) | none — no QUALITY criterion reads a commit's author date; the nearest, 75, states the limit outright: "both times are lane-written (a backdated commit passes)" (`QUALITY.md:329-336`, the clause at `:333`) | File the report with an author date at or after the lane tip it cites. **Not yet shown** — there is no instrument for it and this round's report does not exist yet; the observable is `git -C /home/vgpnk/Projects/shokunin log -1 --format='%aI %cI' <report commit>` against the cited tip's `%aI` |
| M4 | survivor | Seven of fourteen new junk probes printed `PIN_CHECK=met` exit 0 against the landed v3 at `e4dfff32`: `v1_html_comment`, `v2_zwsp_header_prefix`, `v3b_tab_fence`, `v4_fourspace`, `v6_dup_authority`, `v7_split_tally`, `v8_html_table`, while P-C1 stayed `C1=met` (`.ufo/waves/round-48/w2/R48CritV3Junk1.md:13-19`, table at `:62-75`, "Seven survivors, seven caught" at `:77`, repair set at `:451-476`) | none — QUALITY 125's check is `hidden=0 unparsed=0`, which is exactly what each survivor printed (`R48CritV3Junk1.md:62,64,68,69,73,74,75`), and QUALITY 126's check is `junk_met=0` over the eight J edits only, so no criterion's check goes red on these shapes | The seven shapes enter this round's frozen counter as N1–N7 (`count-c1.py:20-26` and `NEW_VARIANTS` at `:206-209`), so the landed tool must score each `unmet`. **Shown able to fail**: the entering tool (`controls/tool-v3-entering.py`, sha256 `85a89a3b…` = `tools/mori-pin-check.py` at `b3e3453d`) prints `C1=unmet junk_met=9 honest_unmet=0 real=met errors=0 variants=26`, with N1–N7 and N9 `got=met rc=0` (`evidence/control-c1-tool-v3-entering.txt`, exit 1); the five round-48 surface rules alone leave `junk_met=1` (N9, `evidence/control-c1-tool-r48-surface-fixes.txt`, exit 1). **Not yet shown**: no repaired tool has landed — `sha256sum tools/mori-pin-check.py` is still `85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1`, `git diff b3e3453d -- tools/ SKILL.md` is empty, and `ls .ufo/waves/round-49/evidence/` holds no `after-c1` receipt; the target is `C1=met … variants=26` at the landed tip |
| M5 | number-drift | The wave-1 dispatch told `Mo49ScribeSkillRows` to pin `C1_SELFTEST pass=42` while the frozen counter prints 44 (`w1/Mo49RevPromptHonesty.md` F1; `evidence/selftest-c1.txt`) | none — the plan text was not run | the seat verified and pinned 44; SKILL.md pins 44 and 114 were measured, not copied. Shown able to fail: the reconciler would mark a wrong pin `mismatch` |
| M6 | landing | `jj` snapshot of the lane failed ("Failed to read directory .scratch/pin-check-…") while seats created and deleted temp dirs under the untracked `.scratch/`, so the first two landing attempts exited non-zero; and registered selftests left `.ufo/waves/round-40/scratch/mori-conform-selftest-*` untracked dirs | none | `.scratch/` added to `.gitignore` (landed `24ebc799`), after which the helper landed; the round-40 selftest debris is reported, not deleted. Shown able to fail: the two failed helper runs |


## Wave 1 — integrated findings

- **Counters (frozen, not changed)** — `w1/Mo49CritC1Counter.md`: the opaque handle is `sha256(rev, body)[:12]`, a function of the variant, so a stub that imports the counter and recomputes it, or sorts the sibling copies by mtime (the order equals the variant order), scores `C1=met`; the contract's "hides which edit" holds against filename and scratch-name sniffers only. `w1/Mo49MutC1Counter.md` F1/F2: the counter's selftest runs a text-only twin of `plan()` and no arm covers a crashed or timed-out tool. `w1/Mo49CritC2Counter.md`: eight breadcrumb quotes with identical six-word claims score `C2=met` (location, not depth); a quote containing `|` is unrepresentable; `w1/Mo49MutC2Counter.md` and `w1/Mo49RevC2Counter.md`: the sources-floor, word-bound and wrong-copy arms do not isolate their guard. All are limits of frozen instruments, reported, not re-scored.
- **Tool** — the L1 integrated: merged witness (F1–F5, R11) + `Mo49ExecArmsHeader` arms + `Mo49ExecArmsBindUnlanded` arms + `Mo49ExecK2K8` (K2, K8) + `Mo49ExecK5X1` (K5, X1) + `Mo49ExecK3K6K7` (R12–R14) + `Mo49ExecImplA`'s ported arms and its one behavioural finding (D1: the verdict-map column was looked up without the F2 normalisation, so a NBSP in the header hid F5 — fixed, arm `f5_nbsp_verdict_map_header_still_read`). `PIN_CHECK_SELFTEST pass=114`. `Mo49ExecRegistryAudit`: the history-wide false-red audit is non-discriminating (58 of 60 revisions fail on drift unrelated to the rules); only "no false red on the entering registry" is shown.
- **Entry** — `Mo49ScoutStagedJournal`: the staged entries' numbers are outside-lane captures and four claims exceed their quotes; `Mo49ScoutHostJournal`: a `sudo journalctl --vacuum-size=50M` line at 2026-10-25 13:10:39 is consistent with the 269M → 56M movement (actor unverified, not a frozen source); `Mo49ScoutS351`/`Mo49ScoutCoverage`: the receipt's `-g` lines breach S351's literal "no MESSAGE grep" — disclosed in the Gate and the entry, claims do not rest on them; the host name appears in the frozen receipt (`Mo49SentCopies` F1, not a credential).
- **Hygiene** — `Mo49ExecScratchHygiene`: `.scratch/` 22–32 GB, 59 untracked dirs cited as evidence by committed reports, 225 tracked files; `.gitignore` entry landed, deletion not performed this round (it would dangle citations and is souji's province per `Mo49ConnAdjacencyRouting`).
- **considerthese** — 2026-10-25 suggestion 3 implemented as `.ufo/waves/round-49/flagged-fixed/` (`count-flagged.py`, `defects.jsonl`): round 48 `flagged=45 fixed=18 unfixed=9 na=18`; QUALITY 133.
- Seat accounting for wave 1: 49 seats dispatched; 48 reports on disk at writing; no `w1-results.json` was delivered (no WAVE-DONE message reached the L1), so seat death is unknown beyond the missing report. I held the planner seat.
