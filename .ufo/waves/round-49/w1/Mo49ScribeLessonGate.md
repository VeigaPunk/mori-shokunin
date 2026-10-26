# Mo49ScribeLessonGate — draft `## Gate` and assimilation for `corpus/lessons/round-49.md`

Seat: scribe, leaf. Draft only, inside this file; no lane file was edited. Scope: `## Gate` and the
assimilation parts of the round-49 lesson. `## Mistakes`, QUALITY, SCORECARD, LOG, README and the entry
itself belong to other seats; where my draft needs their output I leave a bracketed marker instead of
inventing a value.

Lane reads, all read-only: `corpus/lessons/round-48.md` (house shape), `corpus/lessons/round-48-verifier-spotcheck.md`,
`/home/vgpnk/Projects/shokunin/CORPUS.md`, `/home/vgpnk/Projects/shokuknow/merge/mori/MERGE-REPORT.md`,
`/home/vgpnk/Projects/shokuknow/merge/mori/SOURCES.append.md`, the five staged journal entries, the lane
registry at `b3e3453d`, the frozen counter `count-c2.py`, the four committed copies, and the
`assimilation/` id lists. Nothing under `/home/vgpnk/Projects/shokuknow` was executed.

Environment: HEAD is the freeze commit `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115`; the entering tip
`b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86` is its parent. No tool was installed or upgraded for this
seat (no pacman transaction was attempted; the host-wide pause was not tested). Scratch:
`.scratch/r49-Mo49ScribeLessonGate/`, used as `TMPDIR` for every python/bash snippet below.

---

## 1. Evidence actually exercised

| # | command (cwd = lane root unless shown) | observed output | rc |
|---|---|---|---|
| E1 | `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` | `257` | 0 |
| E2 | `grep -oE '^\| *S[0-9]+' corpus/SOURCES.md \| tr -d '| ' \| sort -V \| tail -3` | `S482 S483 S484` | 0 |
| E3 | `awk -F'\|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md` | `mined=207 queued=24 rejected=26` | 0 |
| E4 | `awk -F'\|' '… NF!=13 {n++} …' corpus/SOURCES.md` | `0` | 0 |
| E5 | `grep -cE '^ {0,3}\| *S48[5-8] *\|' corpus/SOURCES.md` | `0` (all four planned ids free) | 1 |
| E6 | `comm -12 <(sort .ufo/waves/round-49/assimilation/reg-ids) <(sort .ufo/waves/round-49/assimilation/staged-ids)` | `S471 … S484`, `count=14` | 0 |
| E7 | `git show b3e3453d:corpus/SOURCES.md \| grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' \| tr -d ' \|' \| sort` vs `assimilation/reg-ids` | `diff` empty, `257` ids — the committed id list is reproducible from the registry at the entering tip | 0 |
| E8 | `for id in S516 S524 S532 S537 S544 S560 S554; do grep -cx "$id" assimilation/reg-ids; done` | `0` for each — none of the candidate staged rows collides | 1 |
| E9 | guard fixture in scratch: `printf '%s\n' "| S002 | a |" "  | S002 | b |" "   | S003 | c |" "    | S002 | d |"` then `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` / `grep -cE '^\|[[:space:]]*S[0-9]{3,}'` | `3` / `1`; ids seen `S002 S002 S003` — a row indented 1–3 spaces is a row, 4 spaces is code and is skipped | 0 |
| E10 | `sha256sum corpus/evidence/sources-r49/*` | `be3952cb…` host-journal-reach.txt, `75440570…` journalctl.1.html, `b4a9b53e…` journald.conf.5.html, `a7b44356…` systemd-journald.service.8.html — equal to `evidence/freeze-sha256.txt` and to `count-c2.py`'s `COPIES` | 0 |
| E11 | python: `count-c2.py`'s own `normalise()` over the four copies, substring test of the staged entries' public sentences | `--vacuum-size= removes the oldest archived journal files until …` FOUND (18 words); `only operates on archived journal files` FOUND (6); `shows the sum of the disk usage of all archived and active journal files` FOUND (14); `stores log data either persistently below /var/log/journal … (in the latter case, it is lost at reboot)` FOUND (23) | 0 |
| E12 | same harness, location of the default sentence in `journald.conf.5.html` | `The first pair defaults to 10% and the second to 15% of the size of the respective file system, but each of the calculated default values is capped to 4G.` FOUND | 0 |
| E13 | same harness, `-g` semantics in `journalctl.1.html` | `-g , --grep= ¶ Filter output to entries where the MESSAGE= field matches the specified regular expression.` FOUND | 0 |
| E14 | `grep -cF 'software/systemd/man/latest/journalctl.html' corpus/SOURCES.md` and the same for the other two pages | `3` (rows S014, S351, S470), `0` (journald.conf), `0` (systemd-journald.service) | 0 |
| E15 | `grep -n 'W04\|E04' /home/vgpnk/Projects/shokunin/scripts/sources-census.sh` | W04 = "same URL across scopes" (warning, lines 33, 644-645); E04 = duplicate URL *within* a scope, exempt for a rejected twin or a `supersedes S###` in `teaches` (lines 646-649) | 0 |
| E16 | `grep -c 'W04' .ufo/waves/round-49/evidence/census-start.txt`; `wc -l` | `20`; `21` — 20 warnings + one `ok` | 0 |
| E17 | `for f in .ufo/waves/round-48/w1/Crit*.md .ufo/waves/round-48/w1/Rev*.md; do grep -cE '^#{2,4} .*\b(F[0-9]{1,2}\|D[0-9]{1,2}\|P[0-9]\|J[0-9]{1,2})\b' "$f"; done` | `8 0 0 6 9 3 0 4` (`CritC1Counter`, `CritC2Counter`, `CritContractFreeze`, `CritEntryRisk`, `CritJunkClasses`, `CritV3Spec`, `RevAssimPlan`, `RevPromptHonesty`), total `30`; `grep -cE '^\*\*F[0-9]' …/RevAssimPlan.md` → `5`; `CritC2Counter.md` carries one named counterexample | 0 / 1 |
| E18 | `grep -n 'script\|style\|comment' .ufo/waves/round-49/count-c2.py`; `cat .ufo/waves/round-49/evidence/selftest-c2.txt` | `normalise()` strips `<script>`/`<style>` (line 60) and `<!-- -->`; arms `normalise_drops_script_text`, `…_style_text`, `…_comment_text` PASS; `C2_SELFTEST pass=26 fail=0` | 0 |
| E19 | `tail -3 evidence/control-c1-stub-filename-sniffer.txt`; `tail -3 evidence/control-c1-sniffer-under-r48-counter.txt` | round-49 counter: `C1=unmet junk_met=18 … variants=26`, rc 1; round-48 counter: `C1=met junk_met=0 … variants=12`, rc 0 | 0 |
| E20 | `grep -nE '^ *\| *S351 *\|' corpus/SOURCES.md` | the rejected journalctl(1) row, flip text quoted in §3 below | 0 |
| E21 | `grep -rnE 'S244\|S268' corpus/SOURCES.md corpus/knowledge corpus/README.md`; `grep -cE '^ {0,3}\| *S244 *\|'`; same for `S268` | no S244/S268 registry row (`0`, `0`); one prose mention, `corpus/README.md:620`; `corpus/knowledge/oom-victim-context-r41.md` cites `S262` | 0 |
| E22 | `stat -c '%n %s'` on the four staged `file://` receipts under `/home/vgpnk/Projects/shokuknow/lanes/mori/round{8,9,10,11}/.deepresearch/notes/` | `1761 1529 1275 1088` bytes — the notes exist; read-only, nothing executed there | 0 |
| E23 | `cat corpus/evidence/sources-r49/host-journal-reach.txt` | `--disk-usage` 56M, `--system` 19M, `--user` 37M (all rc 0); `cat-config` shows the stock file with every journald key commented out plus one drop-in setting `SystemMaxUse=256M` / `RuntimeMaxUse=64M`; drop-in 46 bytes, mtime 2026-10-16; `findmnt -no FSTYPE /run` → `tmpfs`; `findmnt -no FSTYPE /var/log/journal` → rc 1; `ls -A /run/log/journal` empty, rc 0; `--list-boots` lists exactly two boots (idx -1 and 0); the daemon's two limit lines come from `-q -g 'Journal .* is .*max'` | 0 |
| E24 | `ls /home/vgpnk/Projects/shokuknow/merge/mori/` | `MERGE-REPORT.{md,json} SOURCES.append.md amendments knowledge` — `SOURCES-PROPOSED.md`, which `MERGE-REPORT.md` step 1 names, is absent | 0 |
| E25 | `grep -oE '^[0-9]+\.' corpus/QUALITY.md \| tr -d '.' \| sort -n \| tail -2` | `127 128` — next free criterion is 129 | 0 |
| E26 | `git status --porcelain \| grep -c '^?? .scratch/'`; `cat .gitignore` | `165`; no `.scratch/` entry (round-48 routed defect 1 still open) | 0 |

---

## 2. Draft (fenced)

````markdown
## Gate

### New SOURCES rows (each opened this round; rule 1)

Four rows, all opened 2026-10-25 by the row scribes and drafted in `w1/Mo49ScribeRow{Conf,Ctl,Svc,Host}.md`.
The quote column carries a marker, not a sentence: the L1 pastes each scribe's located quote and its
location there, and must not paraphrase it (CORPUS.md, "a quote names its location"). The three pages were
copied at the freeze `0df17b7b` and every copy matches its `count-c2.py` pin — `sha256sum
corpus/evidence/sources-r49/*` → `b4a9b53e…` `journald.conf.5.html`, `75440570…` `journalctl.1.html`,
`a7b44356…` `systemd-journald.service.8.html`, `be3952cb…` `host-journal-reach.txt`, rc 0 — so the rows are
grounded in bytes this lane holds, not in a live page.

| id | URL / locator | accessed | ≤25-word located quote | decision |
|---|---|---|---|---|
| S485 | https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html — copy `journald.conf.5.html` | 2026-10-25 | `[from ScribeRowConf]` — `SystemMaxUse=` / `MaxRetentionSec=` entries | admit, mined, kind docs, tier A for the retention options only, recheck 180d |
| S486 | https://www.freedesktop.org/software/systemd/man/latest/journalctl.html — copy `journalctl.1.html` | 2026-10-25 | `[from ScribeRowCtl]` — `--vacuum-size=` / `--disk-usage` entries | admit, mined, tier A, recheck 180d; `teaches` opens `supersedes S351 —`; scope text differs from S014's (cursor/field selection) and S470's (`--disk-usage` total) |
| S487 | https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.service.html — copy `systemd-journald.service.8.html` | 2026-10-25 | `[from ScribeRowSvc]` — storage paragraph | admit, mined, tier A, recheck 180d |
| S488 | own-work: host-journal-reach — `corpus/evidence/sources-r49/host-journal-reach.txt` | 2026-10-25 (receipt captured 2026-10-25T20:43:09-03:00) | `[from ScribeRowHost]` — a receipt line under its command heading | admit, mined, kind own-work, tier A scoped to this host on 2026-10-25, recheck 90d; the token `own-work: host-journal-reach` appears verbatim in the source cell, because `count-c2.py` matches the URL key on those words |

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
  .ufo/waves/round-48/w1/Rev*.md` → `8 0 0 6 9 3 0 4`). Disposition tally: `[from Mo49ExecFlaggedFixed]`.
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
````

---

## 3. Integration notes for the L1

1. **Markers to fill:** `[from ScribeRowConf]`, `[from ScribeRowCtl]`, `[from ScribeRowSvc]`,
   `[from ScribeRowHost]` in the new-row table, and `[from Mo49ExecFlaggedFixed]` in the considerthese
   bullet. Nothing else in the draft is a placeholder.
2. **`## Mistakes` is not drafted here** (seat `Mo49ScribeMistakes`). My draft deliberately does not cite
   M-numbers, and the Gate's census forecast is the only forward claim.
3. **Numbers to re-check at integration** (they move with the landing): row count 257 → 261; status
   histogram `mined 207 → 211`; the `W04` count 20 → 21; `diff` of the committed `reg-ids` against a fresh
   extraction from the landed `SOURCES.md`.
4. **The S351 sentence is the one that needs a decision, not an edit.** If the L1 reads S351's flip as
   "no kernel MESSAGE grep", say so in S486's `teaches` and the entry's `source:`/provenance line; if it
   reads it literally, the entry must not use the two `-g`-derived daemon lines and S486 must not claim
   the flip. I did not choose for the lane.
5. Spelling of the pull-in: the receipt's own text uses the token `own-work: host-journal-reach`;
   `count-c2.py` matches a URL key by substring, so any rewording of that token in S488's source cell
   breaks `provenance`/`bad_rows`.

---

## Findings

- **HIGH — `.ufo/waves/round-49/w1/Mo49ScribeLessonGate.md` §2 "Reject, with flip" (S351).** The
  contract's description of this round ("the public sentence … plus a committed read-only receipt, no
  MESSAGE grep") is not satisfied literally: `corpus/evidence/sources-r49/host-journal-reach.txt` obtains
  the daemon's limit lines with `journalctl -q -g 'Journal .* is .*max'`, and the committed
  `journalctl(1)` copy defines `-g`/`--grep=` as filtering on `MESSAGE=`. Either S486's `teaches` states
  the narrow reading or the entry must drop those two lines. This is a Gate predicate issue, not a counter
  issue (the counter locates the quotes either way).
- **MED — `corpus/evidence/sources-r49/host-journal-reach.txt`, `--disk-usage`/`--system`/`--user` lines.**
  The receipt shows three stores, not two: total 56M = system 19M + user 37M, volatile empty. The staged
  entries (r47, r48) and their titles say "two journals"; the admitted entry must not repeat that store
  count, or must name the user store explicitly.
- **MED — `/home/vgpnk/Projects/shokuknow/merge/mori/MERGE-REPORT.md` (adopt checklist).** The checklist
  is unexecutable as written (step 1 names an absent `SOURCES-PROPOSED.md`) and would break the id rule
  (step 3 bulk-appends the 136 staged rows, 14 of which collide) and the entry cap (step 4 adds 80
  entries). Round 48 filed this as `RevAssimPlan` F3 and it is unfixed in the package; the round follows
  §10, and the lesson should say so.
- **MED — candidate row list, round-49 seat dispatch.** The seat list names staged rows S516, S524, S532,
  S537, S544, S560, but `reach-per-journal-second-instance-r48.md` cites **S554** as its only source; an
  integration that trusts the list leaves one staged row unexamined. S554 is rejected here on the same
  ground as S524/S537/S544.
- **MED — `corpus/evidence/sources-r49/host-journal-reach.txt` (`ls -A /run/log/journal`).** The receipt
  lists the parent directory; the staged recheck command in `runtime-journal-reach-is-the-boot-r49.md`
  lists `/run/log/journal/<machine-id>`. "Holds no files" is shown for the parent, which is compatible
  with a child directory existing and being empty, but the two commands are not interchangeable as written.
- **LOW — lane ids S485–S488 vs staged ids S485–S488.** Four unrelated documents share the numbers: a
  reader of `SOURCES.append.md` will see MaxCompute, MaxCompute Logview, CPFS quota and CloudMonitor rows
  under the same ids. The Gate states the mapping; no rule is broken because no staged row is appended.
- **LOW — `corpus/SOURCES.md` new rows, S486 (census).** A fourth row on the `journalctl.html` URL with a
  new scope necessarily adds a `W04` warning (the row prompt asks only that `E04` not fire). Warnings do
  not fail validation, but the round-end census should be read as 21 warnings + `ok`, not as a regression.
- **LOW — `.gitignore`.** Round-48 routed defect 1 is unfixed: `165` untracked `.scratch/` directories at
  the freeze and no `.scratch/` entry in `.gitignore`. It belongs to the mistakes/landing seats, but a
  round-end `git status` will show it again.
- **LOW — staged `journal-reach-at-ceiling-r46.md`.** "2215 times the subtree came within reach of a limit
  boundary" glosses a cgroup counter without citing its semantics; the rule half of the entry is sound
  (three sentences located), the gloss is not the page's.
