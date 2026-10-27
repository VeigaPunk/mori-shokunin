# Mo56ExecCensus — round-56 w1 census before-state (captured bytes)

Seat: Mo56ExecCensus. Lane: mori-shokunin. Wave: round-56 w1.
Scope: census before-state for the round-56 corpus registry, captured as bytes
only (routed defect 1 from round 55, QUALITY 152). Detection and report only —
no file under the lane was modified by this seat.

Scratch (removed at exit): `/fast/scratch/hyaku/mori-r56/Mo56ExecCensus/`
(`before/`, `before-root/`, `probe-root/`, `tmp/`, captured outputs).
`TMPDIR=/fast/scratch/hyaku/mori-r56/Mo56ExecCensus/tmp` for the run.
Disk guard checked first: `/fast/scratch/hyaku` 585.6 G free, exit 0 — no ENOSPC.

No tool was installed or upgraded for this seat; no package manager was invoked.
(Operator tooling directive 2026-10-19: nothing needed installing; `pacman`
remains paused host-wide and was not run.)

---

## 1. The census command, run with stdout+stderr redirected straight into a file

Command (absolute path, cwd = fleet root `/home/vgpnk/Projects/shokunin`):

```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori > <scratch>/census-run.txt 2>&1
printf 'exit=%s\n' "$ec" >> <scratch>/census-run.txt
```

Exit code of the command itself, re-confirmed by a second direct invocation
with output to /dev/null: `exit=0`.

Full captured bytes (25 lines; tabs shown as literal TAB in the first block):

```
mori	W04	S035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in across scopes
mori	W04	S037 duplicate url www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html across scopes
mori	W04	S073 duplicate url docs.python.org/3/library/pathlib.html across scopes
mori	W04	S074 duplicate url kubernetes.io/docs/concepts/architecture/controller across scopes
mori	W04	S075 duplicate url ftp.gnu.org/gnu/bash/bash-5.3.tar.gz across scopes
mori	W04	S076 duplicate url michaelfeathers.silvrback.com/characterization-testing across scopes
mori	W04	S147 duplicate url raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/docs/settings.md across scopes
mori	W04	S148 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes
mori	W04	S149 duplicate url man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html across scopes
mori	W04	S150 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml across scopes
mori	W04	S166 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes
mori	W04	S168 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst across scopes
mori	W04	S201 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c across scopes
mori	W04	S218 duplicate url github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch across scopes
mori	W04	S220 duplicate url raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c across scopes
mori	W04	S228 duplicate url docs.python.org/3/library/os.path.html across scopes
mori	W04	S349 duplicate url www.openeuler.org/whitepaper/openEuler%2024.03%20LTS%20%E6%8A%80%E6%9C%AF%E7%99%BD%E7%9A%AE%E4%B9%A6.pdf across scopes
mori	W04	S351 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori	W04	S470 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori	W04	S476 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
mori	W04	S486 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori	W04	S491 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
mori	W04	S492 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst across scopes
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
exit=0
```

Line 24 (the `ok` line) is byte-exact; the URL in the S349 line contains percent
escapes (`%2024.03%20LTS%20%E6%8A%80%E6%9C%AF%2079%BD%E7%9A%AE%E4%B9%A6.pdf`).

### 1a. Byte comparison against the committed receipt

```
$ cmp <scratch>/census-run.txt .ufo/waves/round-56/evidence/census-start.txt
BYTE_IDENTICAL
$ sha256sum .ufo/waves/round-56/evidence/census-start.txt
611391325d4d0d20955c8939cc9688dc0fa54d329c11eac7fa25abfc1ef9c61b  .ufo/waves/round-56/evidence/census-start.txt
$ wc -c .ufo/waves/round-56/evidence/census-start.txt
2580 .ufo/waves/round-56/evidence/census-start.txt
$ grep -c 'W04' .ufo/waves/round-56/evidence/census-start.txt
23
$ grep -c 'rows' .ufo/waves/round-56/evidence/census-start.txt
0
```

The committed receipt **is** a faithful captured-bytes receipt for the W04 set
and the exit code: a fresh run today reproduces it byte for byte. QUALITY 152's
capture discipline holds for that portion.

But the receipt contains **no row count at all** (`grep -c 'rows'` = 0), and it
carries **no `rev=` stamp** (`grep -c 'rev='` = 0). Both facts matter below.

---

## 2. CORPUS.md manual counting commands over `corpus/SOURCES.md`

The commands were extracted verbatim from `/home/vgpnk/Projects/shokunin/CORPUS.md`
lines 134–147 (the `grep`/`awk` lines only, so no prose leaked into the script)
and run from the lane root, as CORPUS.md directs ("run from the lane root").

Extraction:

```
$ sed -n '134,147p' /home/vgpnk/Projects/shokunin/CORPUS.md | grep -E '^(grep|awk) ' > <scratch>/corpus-commands.sh
$ wc -l <scratch>/corpus-commands.sh
7
```

### 2a. At the round-56 tip (working tree, HEAD `acc62f54`)

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && bash <scratch>/corpus-commands.sh; echo "exit=$?"
318
0
A=287 B=14 C=17 
mined=267 queued=24 rejected=27 
exit=0
```

Line by line, in CORPUS.md order: row count **318**; malformed-row count **0**
(as required); tier histogram **A=287 B=14 C=17**; status histogram
**mined=267 queued=24 rejected=27**; duplicate-id check **empty**; enum-violation
and tier-inflation check **empty**; mined used-by existence check **empty**
(no `missing:` lines).

### 2b. At the entering tip `5b295eeebd87ebd610d8d39bfe2035742f740cfa`

Materialised read-only from the git object store into scratch
(`git archive 5b295eee | tar -x -C <scratch>/before`), so no lane file was touched:

```
$ cd <scratch>/before && bash <scratch>/corpus-commands.sh; echo "exit=$?"
316
0
A=285 B=14 C=17 
mined=265 queued=24 rejected=27 
exit=0
```

Same seven checks, same shapes: row count **316**; malformed **0**; tier
**A=285 B=14 C=17**; status **mined=265 queued=24 rejected=27**; duplicate ids
empty; enum violations empty; used-by missing empty.

### 2c. Cross-check with the maintained parser (`census` mode, which does print rows)

Lane-scoped run (only `mori` is a target, so the FLEET aggregate equals the
lane's own totals):

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin mori
mori	rows	318
mori	tier.A	287
mori	tier.B	14
mori	tier.C	17
mori	status.mined	267
mori	status.queued	24
mori	status.rejected	27
FLEET	rows	318
FLEET	tier.A	287
FLEET	tier.B	14
FLEET	tier.C	17
FLEET	tier.invalid	0
FLEET	status.queued	24
FLEET	status.mined	267
FLEET	status.rejected	27
FLEET	status.invalid	0
FLEET	missing	0
exit=0
```

Fleet-wide run (all lanes, for context only — no lane other than mori is in
this seat's scope):

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin
…
FLEET	rows	3550
FLEET	tier.A	2973
FLEET	tier.B	461
FLEET	tier.C	116
FLEET	tier.invalid	0
FLEET	status.queued	279
FLEET	status.mined	3049
FLEET	status.rejected	222
FLEET	status.invalid	0
FLEET	missing	0
exit=0
```

At the entering tip (same lane-scoped command against the scratch tree holding a
copy of the lane at `5b295eee`, plus a copy of the fleet `shokunin.conf` so the
lane resolves): `mori	rows	316`, `tier.A 285 / tier.B 14 / tier.C 17`,
`status.mined 265 / queued 24 / rejected 27`, exit 0.

Two independent counters agree at both ends: `grep -cE` and the maintained
parser both say **316** before and **318** after.

### 2d. Before → after arithmetic

| quantity | entering tip `5b295eee` | tip `acc62f54` | delta |
|---|---|---|---|
| rows | 316 | 318 | **+2** |
| tier A / B / C | 285 / 14 / 17 | 287 / 14 / 17 | +2 / 0 / 0 |
| status mined / queued / rejected | 265 / 24 / 27 | 267 / 24 / 27 | +2 / 0 / 0 |
| malformed rows | 0 | 0 | 0 |
| duplicate ids | none | none | 0 |
| enum / tier-inflation violations | none | none | 0 |
| mined used-by paths missing on disk | none | none | 0 |
| W04 warnings | 23 | 23 | 0 |

The +2 rows are exactly **S544** and **S545**, added by the round-56 data commit
`c419fe6d` (`corpus/SOURCES.md | 2 ++`). Both are tier A and both are `mined`,
which is why tier.A and status.mined each move by exactly 2 and every other
bucket holds. The W04 warning set is unchanged: the 23 flagged ids are the same
23 before and after (`diff` of the sorted id columns is empty), so the two new
rows introduce no new duplicate-URL class.

### 2e. Non-vacuity of the used-by existence check

The used-by check passes trivially if it never examines a path. It is not
vacuous here:

```
$ awk -F'|' '... if (s=="mined") { ... print p }' corpus/SOURCES.md | wc -l
361
$ awk -F'|' '... if (s=="mined" && u=="—") print $2' corpus/SOURCES.md | wc -l
0
```

361 mined used-by paths are checked and all exist; zero mined rows carry the
`—` placeholder that would make the check skip them.

### 2f. Registry rows and used-by targets at the tip

```
$ grep -nE '^\|[[:space:]]*S(544|545)[[:space:]]*\|' corpus/SOURCES.md
324:| S544 | shokunin driver launch-log grammar — scripts/hyaku/inline.sh and scripts/hokunin-watchdog.sh in the fleet repo | own-work | A | ... | mined | 2026-10-27 | on-release | corpus/knowledge/driver-liveness-r56.md, tools/mori-driver-liveness.py |
325:| S545 | RFC 8259 The JavaScript Object Notation (JSON) Data Interchange Format — https://www.rfc-editor.org/rfc/rfc8259.txt | spec | A | ... | mined | 2026-10-27 | on-release | corpus/knowledge/vote-binding-r56.md, tools/mori-vote-bind.py |
```

All four named used-by targets exist on disk (`EXISTS` for each), and both rows
are `NF==13` (11 columns).

---

## 3. Comparison with `evidence/census-start.txt` (start of round: 316 rows, 23 W04, exit 0)

| claim in the seat brief / contract | receipt bytes | verdict |
|---|---|---|
| exit 0 | `exit=0` on the last line | **supported** |
| 23 W04 | 23 `W04` lines | **supported** |
| 316 rows | 0 occurrences of `rows` in the receipt | **NOT supported by the receipt bytes** |

The 316-row figure is true for the moment of capture, but it is **not in the
receipt**. Supporting evidence that the capture happened before the registry
edit: the receipt's mtime `2026-10-27 10:18:46 -0300` precedes `corpus/SOURCES.md`'s
mtime `2026-10-27 10:34:44 -0300`, and both landed in the same commit
`c419fe6d` (10:39:19). mtimes are weak evidence though (a checkout can rewrite
them), and the decisive fact is the next one.

### 3a. The receipt cannot distinguish 316 rows from 318 rows

`validate` mode structurally **cannot** print a row count: the parser only
emits `rows`/tier/status in `census` mode (`scripts/sources-census.sh:689-693`,
guarded by `if (mode=="census")`), and the `validate)` branch of the mode
dispatch (`scripts/sources-census.sh:737-747`) prints only E/W findings plus an
`ok` line. Probe (scratch only, on a copy of the entering-tip tree with two
extra rows inserted inside the Registry section so they do not trip E12):

```
$ diff <scratch>/probe-318.txt <scratch>/census-before-316.txt
24c24
< mori	ok	<scratch>/probe-root/mori-shokunin/corpus/SOURCES.md
---
> mori	ok	<scratch>/before-root/mori-shokunin/corpus/SOURCES.md
$ diff <(cut -f1,2 <scratch>/probe-318.txt) <(cut -f1,2 <scratch>/census-before-316.txt)
(no output — IDENTICAL_MODULO_PATH)
```

A 316-row registry and a 318-row registry produce **identical** validate output
apart from the absolute path echoed on the `ok` line. The receipt therefore
carries no information about the registry size, and cannot by itself support a
before→after row-count claim. This is the same class the round says it is
fixing: the number in the prose is not backed by captured bytes.

### 3b. The receipt is byte-identical to round 55's receipts

```
$ sha256sum .ufo/waves/round-55/evidence/census-start.txt \
            .ufo/waves/round-55/evidence/census-end.txt \
            .ufo/waves/round-56/evidence/census-start.txt
611391325d4d0d20955c8939cc9688dc0fa54d329c11eac7fa25abfc1ef9c61b  .ufo/waves/round-55/evidence/census-start.txt
611391325d4d0d20955c8939cc9688dc0fa54d329c11eac7fa25abfc1ef9c61b  .ufo/waves/round-55/evidence/census-end.txt
611391325d4d0d20955c8939cc9688dc0fa54d329c11eac7fa25abfc1ef9c61b  .ufo/waves/round-56/evidence/census-start.txt
```

Round 55's start receipt, round 55's end receipt, and round 56's start receipt
are the same 2580 bytes. The round-56 receipt is a fresh capture (mtime
2026-10-27 10:18) whose content happens to be unchanged — so it is honest as a
capture, but it is not round-discriminating evidence either.

### 3c. Revision stamping across the round-56 receipts

```
c1-at-freeze.txt                 rev=3f494b49cde612d929e82887a48e1660c022c359
c2-at-freeze.txt                 rev=3f494b49cde612d929e82887a48e1660c022c359
c2-old-counter-voted0.txt        rev=5b295eeebd87ebd610d8d39bfe2035742f740cfa
census-start.txt                 <NO-REV-STAMP>
controls.txt                     rev=5b295eee…  (two do-nothing lines)
driver-liveness-live.txt         <NO-REV-STAMP>
freeze-sha256.txt                <NO-REV-STAMP>
selftest-c1-counter.txt          <NO-REV-STAMP>
selftest-c2-counter.txt          <NO-REV-STAMP>
selftest-vote-bind.txt           <NO-REV-STAMP>
tally-r55.txt                    <NO-REV-STAMP>
```

The census receipt is the one a before→after row is expected to cite, and it is
the one that stamps nothing.

---

## 4. Notes on method, and one observation about the manual-command surface

- The CORPUS.md manual commands must be run **from the lane root**. The
  used-by existence check resolves repo-relative paths against the current
  working directory; run from elsewhere it reports all 361 mined paths as
  `missing:`. I confirmed this: the same awk pipeline run from a scratch cwd
  emits 361 false `missing:` lines. CORPUS.md does say "run from the lane root",
  so this is a documented precondition, not a defect — but the captured receipt
  records no cwd, so a reviewer cannot tell from the bytes which cwd produced
  it.
- In one of my early invocations the enum-violation check printed
  `kind S029 book` / `kind S061 book`. It did not reproduce in any later run of
  the CORPUS.md command, and I traced the cause: the CORPUS.md kind enum
  includes `book`, and the two rows with `kind=book` are the only rows that
  would be flagged if that one alternative were dropped from a hand-typed
  regex. Reproducing the regex without `book` yields exactly those two lines;
  the verbatim CORPUS.md regex yields nothing. This is an artifact of my own
  transcription in that single call, **not** a lane defect, and it is direct
  evidence for the lesson's own stated fix ("row counts come from
  `grep -cE …` / the census validator, not retyping"): a hand-retyped regex
  silently changes its meaning. S029 and S061 are `kind=book`, which is a valid
  enum value per CORPUS.md line 91 and per the maintained parser's own E05
  check.
- `git` was used read-only throughout (`log`, `show`, `rev-parse`, `status`,
  `archive`, `ls-files`). No `add`/`commit`/`stash`/`checkout`/`reset`/`pull`/`push`
  in the lane or the fleet root; no mutating `jj` command; no fixture repo was
  created; nothing was written outside this seat's report file and the scratch
  directory.

---

## Findings

**F1 — HIGH — the round's own row-count claim is a retyped summary, not captured bytes.
**Files: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/contract.md:70`
(committed, frozen) and `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-56.md:46`
(L1's working-tree draft, currently untracked — `git status` shows it as `??`).
Both write the census receipt as `(exit 0, 316 rows, 23 W04)`, but
`.ufo/waves/round-56/evidence/census-start.txt` contains 0 occurrences of
`rows` — `validate` mode cannot emit one (§3a). No artifact committed in
round-56 captures the counting command's output for the before state: at
`3f494b49` the only occurrence of `316` anywhere under `.ufo/waves/round-56`
is the contract sentence itself (verified with
`git grep -c '316' 3f494b49 -- .ufo/waves/round-56`, which lists
`contract.md` alone). This is precisely the QUALITY 152 / routed
defect 1 class ("census before→after must be captured bytes or the counting
command") that this round states it is applying. The number 316 is not wrong
(§2b, two independent counters agree), but it is not evidenced by the receipt
cited for it. The counters, predicates and kill rules are frozen and untouched
by this finding; the fix is data-side: capture `census`-mode output (which
prints `mori rows N`) beside the validate receipt, and cite the captured
counting-command output for the before→after row count. The contract sentence
is frozen, so the actionable part lands on the lesson draft, the end receipt
(F4), and the round report — all L1-owned.

**F2 — HIGH — the census receipt carries no measured-revision stamp, though the
contract's own routed defect 2 requires receipts to stamp it.**
File: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/evidence/census-start.txt`
(`grep -c 'rev='` = 0). Contract lines 61–62 state that receipts here stamp the
measured revision and that a before→after row cites the receipt's stamped
revision; the lesson's fix column likewise claims After cells cite the
receipt's own stamped `rev=` field. Every other round-56 receipt that measures a
revision stamps it (`c1-at-freeze.txt`, `c2-at-freeze.txt` → `rev=3f494b49…`;
`c2-old-counter-voted0.txt`, `controls.txt` → `rev=5b295eee…`). The census
receipt is the one the before→after row must cite, and it stamps nothing, so
there is no stamped revision to cite — the round-56 fix as written is
unsatisfiable for this receipt.

**F3 — MED — the receipt cannot distinguish the before registry from the after
registry, and is byte-identical to round 55's receipts.**
File: `.ufo/waves/round-56/evidence/census-start.txt` (sha256 `611391325…`,
2580 bytes — the same sha as `.ufo/waves/round-55/evidence/census-start.txt`
and `.ufo/waves/round-55/evidence/census-end.txt`). §3a proves the validate
output is invariant to the registry's row count (316 vs 318 rows produce
identical bytes apart from the echoed path), and §3b shows the round-56 receipt
is the same 2580 bytes as both round-55 receipts. The receipt is an honest
capture (§1a: a fresh run reproduces it byte for byte, so QUALITY 152's capture
discipline is met) but it is a low-information artifact: it demonstrates that
the W04 set and the lane verdict are unchanged, and nothing more. It cannot
carry the 316→318 row-count claim of F1.

**F4 — MED — no end census receipt exists yet.**
Directory: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/evidence/`
(contains `census-start.txt` only; round 55 had both `census-start.txt` and
`census-end.txt`). The contract (line 70) requires "End census must exit 0" and
the lesson defers it to "after the last registry edit". This is an open item at
wave time rather than a defect, but the L1's end receipt should carry a captured
row count (census mode) and a revision stamp, or F1 and F2 recur unchanged into
round 57.

**F5 — LOW — the manual used-by existence check is working-directory dependent
and the receipt records no cwd.**
Files: `/home/vgpnk/Projects/shokunin/CORPUS.md:147` (the awk/while pipeline)
and the receipts that would embed its output. The check resolves repo-relative
paths against the cwd: from the lane root it prints nothing (361 paths verified
present, §2e); from any other directory the same pipeline prints 361 false
`missing:` lines. CORPUS.md states the precondition ("run from the lane root"),
so this is not a defect in the recipe — but a captured byte stream of that
check carries no cwd, so a reviewer cannot distinguish a clean lane from a
mis-captured one. Named limit; a cwd line in the receipt would close it.

**F6 — LOW — the enum-violation half of the manual census surface is
transcription-fragile.**
File: `/home/vgpnk/Projects/shokunin/CORPUS.md:145`. The kind enum is a
ten-alternative alternation embedded in a single long awk program; dropping one
alternative silently yields false "kind" hits on exactly the rows using that
kind (in this registry, `kind=book` → S029 and S061). The maintained parser
carries the same enum in one place (`scripts/sources-census.sh:655`), so the
parser is the safer oracle. This is evidence for the lesson's stated fix
direction (count from the validator, not a retyped regex), not a lane defect.
Observed and chased down in §4; the lane registry is enum-clean under both the
CORPUS.md command and the maintained validator (no E05, no E06, no E10 at
either revision).

---

## What this seat did not check

- The C1 and C2 counters, their predicates, the frozen pins, the 13/16-case
  selftests, the driver fixtures, the vote-binder tally and the freeze-sha256
  pins are outside this seat's scope and were not adjudicated here.
- The end-census receipt (F4) does not exist yet; its content and exit code are
  UNVERIFIED.
- Whether the L1's pending `corpus/lessons/round-56.md` and the round-56
  report end up pasting captured counting-command output for the before→after
  row count (the fix F1 asks for) is UNVERIFIED — at the time of this seat's
  run `corpus/lessons/round-56.md` existed only as an untracked working-tree
  draft and no `.ufo/reports/round-56/` directory existed in the lane.
- No claim is made here about whether F1/F2 should be fixed inside round 56
  (re-pin consequences) or routed to round 57; that is the L1's call.

## Evidence index (all under the seat scratch, removed at exit)

```
corpus-commands.sh      the 7 CORPUS.md commands, extracted verbatim (grep -E '^(grep|awk) ')
census-run.txt          fresh validate capture + exit=0 (byte-identical to the committed receipt)
census-before-316.txt   validate capture against the entering-tip tree, exit=0
manual-head.txt         7 CORPUS.md commands at HEAD, + exit=0
manual-before.txt       7 CORPUS.md commands at the entering tip, + exit=0
census-mode-mori.txt    lane-scoped census-mode capture (prints the row count), + exit=0
fleet-census.txt        fleet-wide census-mode capture, + exit=0
probe-318.txt           validate capture against a 318-row probe tree (invariance probe)
head-recheck.txt        second HEAD validate capture, + exit=0 (identical to the receipt)
before-recheck.txt      second entering-tip validate capture, + exit=0
w04-before.txt / w04-after.txt   sorted W04 id columns, before vs after (diff empty)
before/                 entering-tip lane tree (git archive 5b295eee | tar -x), read-only
before-root/            same tree + fleet shokunin.conf, for lane resolution in census mode
probe-root/             copy of the entering-tip tree + 2 probe rows, for the invariance probe
tmp/                    TMPDIR for every run in this seat
```

Every block pasted in this report is verified byte-identical to the named
capture file (checked by extracting the fenced blocks and comparing against the
files). The one exception is the fleet-wide block in §2c, which is an excerpt
(marked with `…`) of `fleet-census.txt`; its listed lines are all present in
that file, and its `exit=0` is the appended exit code.

Two corrections I made to my own draft during verification, recorded here so
the next reader does not rely on the earlier text: (1) the S349 URL in the
pasted receipt was mistyped as `%E6%8A%80%E6%9C%AF%2079%BD` and is now the
byte-exact `%E6%8A%80%E6%9C%AF%E7%99%BD`; (2) the first draft's fleet block
spliced the lane-scoped `FLEET rows 318` with the fleet-wide tier/status
totals, which no single command produced — §2c now shows the lane-scoped run
and the fleet-wide run as two separate captured blocks.
