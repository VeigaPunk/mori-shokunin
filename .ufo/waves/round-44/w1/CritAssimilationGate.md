# CritAssimilationGate — C3 admission falsified (mori round 44, wave 1)

**Verdict.** *In province: yes.* *Clears the lane's bar: **no*** — three named failures
(§4, §5). *Frozen instrument: **C3=unmet***, and one of its five arms is structurally red
on this lane (§6) — an instrument defect, not an entry defect.

Target measured: entry `corpus/knowledge/pid-probe-conclusion-r44.md` (5526 bytes),
rows `corpus/SOURCES.md:250-251`, README row `corpus/README.md:632`, working tree at
HEAD `7cb59c6891d4f5d0266fe062565f094da835dc84` (entering tip `1429c791…` confirmed an
ancestor: `git merge-base --is-ancestor 1429c791 HEAD` → true). The entry was **revised
while I reviewed it** (its title and claim moved from "three worlds" to "two worlds
grounded, the swap-out branch retired"); everything below is measured against the
current bytes, and the revision itself is a finding (§4.4).

---

## 1. The frozen instrument's verdict, first

```
$ python3 .ufo/waves/round-44/count-c3.py WORK --row S471 --row S472
check entry_present    PASS (5526 bytes)
check entry_meta       PASS (sources S471,S472)
check rows_present     PASS (rows S471,S472 mined)
check census_ok        FAIL (exit=1)
check readme_row       PASS (names entry)
rev=WORK
C3=unmet
exit=1
```

At the entering tip, the declared Before state reproduces exactly:

```
$ python3 .ufo/waves/round-44/count-c3.py 1429c791db5891c484684feef893799909d2d6a8 --row S471 --row S472
check entry_present    FAIL (absent)
rev=1429c791db5891c484684feef893799909d2d6a8
C3=unmet
exit=1
```

`--selftest` at the frozen sha (`a12170f1…c440c68`, matches `evidence/freeze-r44.txt:5`):

```
$ python3 .ufo/waves/round-44/count-c3.py --selftest
… 6 arms …
C3_SELFTEST pass=6 fail=0
exit=0
```

So: four of five checks green, the fifth red for a cause the entry cannot fix. The
claim **cannot print `C3=met` this round** no matter how good the entry is (§6).

---

## 2. (a) Province — fleet observability or host diagnosis?

**mori, `PROVINCE.md:6-10` (Owns, read-only probes):** "shokunin watchdog liveness (pid,
start time, log freshness, lane counters)"; and Frontier **FR5** (`PROVINCE.md:48`):
"Watchdog daemon identity and degraded-pgrep visibility … Boundary: **an unavailable pid
probe is not absence**, and argv-substring matches do not establish daemon identity."

**mori, `PROVINCE.md:12-16` (Refuses):** "OS package, systemd unit, driver/firmware and
boot state (→ tsukuroi) — mori reads journal and cgroup events as fleet evidence and
reports them, never owning OS state … **Detection and report only — never remediation.**"

**tsukuroi, `PROVINCE.md:3-8` (Core, owns):** "the OS substrate itself: package state,
systemd, drivers/firmware, boot health"; its named surfaces include "systemd user units &
timers (`systemctl --user`, unit files, **failed states**), journal/boot triage … driver/
firmware plane".

**tsukuroi, `PROVINCE.md:24-27` (handoff to mori):** "Host memory and kill-event
measurements support OS triage; they do not establish which fleet wave caused pressure or
whether an endpoint works. … **fleet correlation belongs to mori**."

**Finding: in-province, as written.** The entry's subject is *what a liveness probe may
conclude from a zero-character read* — FR5's own boundary sentence, mori's ground. It
does not diagnose unit state, does not explain a kill, and forbids the reading that would
cross into tsukuroi (`:63-66`: "No probe, surface, finding id or threshold is added …
kill/OOM classification stays with the journal and cgroup rows"). The one place it touches
host memory — the swap-out world — it now **refutes** rather than asserts (`:52-55`:
"the swap-out world only by the older translation, and contradicted by S471 on the
adjacent field"), which is the correct fence: a translation's historical claim is
provenance, not a host-memory diagnosis. No remediation, no config, no probe change.

The province verdict would flip to **tsukuroi** the moment a later round used
"swapped out ⇒ empty cmdline" as current behaviour to explain a fleet pressure reading.
The entry forbids that; the *registry row* does not (§4.3).

---

## 3. (b) Is the Z/X alphabet already held? **Yes — the coverage claim is replay.**

The contract's Before sweep:

```
$ git grep -l 'Z ゾンビ' 1429c791db5891c484684feef893799909d2d6a8 -- corpus/
(no output)
rc=1
```

But the lane *does* hold the alphabet at the same revision, under a different token:

```
$ git grep -n 'Z at :56-57' 1429c791… -- corpus/SOURCES.md
1429c791…:corpus/SOURCES.md:177:| S171 | proc_pid_stat(5) at man-pages 6.20 — https://git.kernel.org/…/proc_pid_stat.5?h=man-pages-6.20 | docs | A | … field 3 state letters (S at :49-50, Z at :56-57, X at :69-70) … | mined | 2026-10-22 | on-release | corpus/knowledge/watchdog-identity-r31.md |
```

That row is `status: mined` and its `used-by` names `corpus/knowledge/watchdog-identity-r31.md`,
which at `:29` already carries:

> | `/proc/<pid>/stat` third value (state) is `Z` | the state letter follows the
> parenthesised task name, and `Z (zombie)` is the zombie state; [INFERENCE] a zombie has
> exited and is not yet reaped … | absent (exited, unreaped) | S167, S171 |

and the other two worlds' mechanism is held in the same corpus:

- `corpus/SOURCES.md:176` (S170, `teaches`): "a zombie reads 0 bytes, so **an empty read
  cannot separate a dead watchdog from a live zombie one**" — worlds 2 vs 3, held.
- `corpus/SOURCES.md:173` (S167, `teaches`): "an exited-but-unreaped task still answers
  the file, so a pid entry proves **presence, not execution**" — the present-but-dead
  world, held.

What the round genuinely adds, then, is narrow and should be said that way: the
*meanings* in two translations (ゾンビ/死亡/僵死), the `X` version qualifier, the zh
`state` field's `"RSDZT"` (five letters, no `X` — verified on the page), and the
comm/swap contradiction between the two pages. The entry instead claims it "adds the
state alphabet (`Z`, `X` and the `X` version qualifier)" (`:57-58`) without citing S171 or
S167. **That is the coverage-claim defect:** the alphabet as a set was held; only the
gloss was not (and `watchdog-identity-r31.md:29` itself records that gap — "no cited line
carries this gloss (residual JudgeC1Rows: row 9 unsupported)").

Two consequences worth naming for the round:

1. The frozen Before/After token is a **literal sweep that is blind to held ground**: it
   returns 0 while `SOURCES.md:177` and `watchdog-identity-r31.md:29` hold the alphabet,
   and it returns 1 on a string the entry itself stitched — neither page carries `Z ゾンビ`
   or `X 死亡` contiguously (measured: `ja.count('X 死亡')` → 0; the page has
   `<dt id="Z">Z</dt><dd>ゾンビ (Zombie)</dd>` and `<dt id="X">X</dt><dd>死亡 (Dead)
   (Linux 2.6.0 以降)</dd>`). The After value therefore measures the entry's typography,
   not the source's text.
2. This is QUALITY 108's defect inverted: "a corpus binding is checked for
   **resolvability**, not token presence". Here presence is the check and resolvability
   is not (§4.2).

---

## 4. (c) Does the recheck test the mechanism, or a word?

**4.1 It reproduces — that much is honest.** Run verbatim from `:6`:

```
$ curl -fsSL --max-time 40 '…/focal/ja/man5/proc.5.html' | python3 -c 'import sys,html;print(html.unescape(sys.stdin.read()).count("ゾンビ"))'
3
$ curl -fsSL --http1.1 --max-time 40 'https://man.archlinux.org/man/proc.5.zh_TW' | python3 -c '…count("僵死")'
2
```

Both observed values are correct today. (Contrast the campaign source entry the draft was
told to follow, `probe-absent-vs-dead-r39.md:6`: `curl … | grep -c 'ゾンビプロセス'` → "1".
Run verbatim it prints **0**, rc=1 — the pages entity-encode CJK (`&#x30BE;`×4 in the ja
page, `&#x50F5;`×2 in the zh page; literal `ゾ` = 0, literal `僵` = 0). A raw-byte grep for
CJK on these pages is a false recheck; the draft correctly avoided it.)

**4.2 But it counts a bare word, not the claim.** `ゾンビ` occurs three times: the cmdline
sentence, the `Z` glossary `dd`, and the `stat` State list. `僵死` occurs twice: the
cmdline `dd` and the `state` `dd`. The recheck does not test that a zero-character read
has more than one explanation, nor that the state field is the discriminator — the two
things the entry claims. A page rewrite that keeps the words and drops the sentences
passes. A claim-bearing recheck would count `このファイルは空となる` → 1,
`スワップアウトされているかどうかによらず` → 1, `RSDZT` → 1.

**4.3 The quoted sentences are assemblies, and one is silently edited.** Measured on the
fetched bytes (contiguous / whitespace-normalized):

| quote | contiguous | normalized |
|---|---|---|
| ja cmdline (`:18`) | 0 | 1 |
| ja comm (`:41`) | 0 | 1 |
| zh cmdline (`:21`) | **0** | **0** |

The zh one is a real edit, found by char diff: the page reads
`…在該檔案裡,這時候對該檔案的讀操作將返回零個字元.` and the entry writes
`…在該檔案裡，…零個字元。` — two punctuation substitutions (`,`→`，`, `.`→`。`). The
recheck counts `僵死` and cannot see it. Under CORPUS.md ("A quote names its location")
and QUALITY 108 (occurrence byte-exact), a quotation that is re-punctuated and re-wrapped
without saying so is not a citation.

**4.4 The registry row makes an unswept negative about S170.**

`corpus/SOURCES.md:251` (S472 `scope`): "… including a swap-out branch the modern English
contract the lane holds **does not state**". The file the lane already mines states it:

```
$ curl -fsSL 'https://git.kernel.org/…/man/man5/proc_pid_cmdline.5?h=man-pages-6.20' | grep -n -i swap
15:.\" In Linux 2.3.26, this also used to be true if the process was swapped out.
```

It is a roff comment (not rendered), and S170's `anchor` cell (`:176`) lists
`:13-14, :16-17, :26-31, :33-40, :42-45, :47` — line 15 is omitted. So the honest
statement is "S170 carries the swap-out note as a commented-out historical note at `:15`,
outside its anchor list", not "does not state". CORPUS.md: "A negative claim carries its
sweep" — this one has none.

**4.5 The revision changed the claim under the frozen predicate.** P-C3 asks for "the
**three worlds** a zero-character `/proc/<pid>/cmdline` read is consistent with". The
current entry says the opposite (`:52`): "**Two worlds are grounded here, not three.**"
The entry enumerates three (`:30-32`) and then retires one — which is the *correct*,
better-grounded reading (the zh page is a Linux 1.3.11-era translation: page text
"本手冊頁基本上是針對Linux 1.3.11核心", "最後更新也是針對Linux 1.3.11", header `2000/11/26`).
But the frozen predicate's sentence is then not literally satisfied, and QUALITY 25
("admitted at the scope it was measured; narrowing is an explicit correction") requires
the round to **record the narrowing**, not to claim the predicate's wording. This is a
calibration item, not an entry defect — and it arrived mid-review, so the round must
re-read the entry before scoring.

---

## 5. (d) Strongest reason to REFUSE, and the flip

**Strongest reason.** The entry's coverage claim is false at the entering tip: the Z/X
alphabet it says it adds is already held by `corpus/SOURCES.md:177` (S171, mined, used-by
the r31 entry) and by `corpus/knowledge/watchdog-identity-r31.md:29`. The round's only
instrument for that claim is a literal-token sweep (`git grep -l 'Z ゾンビ'`) that is
blind to the held rows and green on a string the entry stitched itself. Admitting the
entry as written would record a *new-ground* advance on ground the lane already had —
exactly the false-provenance class this seat exists to catch. Two supporting failures
stand on their own: the zh quotation is re-punctuated (§4.3) and S472's `scope` cell makes
an unswept negative about S170 (§4.4).

**Flip condition (all four, each checkable).**

1. **Cite the held ground.** Add S171 and S167 to the entry's `source:` lines (or a
   held-ground paragraph) and restate the claim as: *the letters are held (S171); this
   entry adds their meanings in two translations, the `X` version qualifier, the zh
   `RSDZT` alphabet without `X`, and the comm/swap contradiction.* The r31 row-9 residual
   ("no cited line carries this gloss") is the honest peg — say that this entry discharges
   it.
2. **Quote byte-exactly.** Replace the four quotations with the pages' own text — ASCII
   `,`/`.` in the zh sentence — or mark the whitespace collapse explicitly and anchor the
   `dt`/`dd` pairs by the ids the page exposes (`#Z`, `#X`, `#state`, `#comm`) instead of
   the stitched `Z ゾンビ` / `X 死亡`.
3. **Fix or drop the S170 negative.** Either cite `proc_pid_cmdline.5:15` (the commented
   swap note) or delete "does not state" from S472's `scope` cell.
4. **Make the recheck claim-bearing and single.** One command per `recheck:` line (the
   wave spec says "one runnable command"; the draft packs two), each counting a
   claim-bearing string, e.g. ja `このファイルは空となる` → 1, ja
   `スワップアウトされているかどうかによらず` → 1, zh `RSDZT` → 1.

If those four land, the entry is admissible **as a translation-and-gloss entry**, not as
a coverage advance on the alphabet; the round report must say so (QUALITY 25) and must
record the C3 predicate's "three worlds" as narrowed to two-grounded-one-retired.

---

## 6. The frozen instrument: `census_ok` is structurally red on this lane

`count-c3.py` stages the registry into a temp dir and runs the census against the staged
file (`:133` `tempfile.mkdtemp(prefix="c3-")`, `:139` `["bash", census, "validate",
"--file", staged]`, `cwd=repo`). The census derives the lane root from the **file**, not
from `cwd`:

```
scripts/sources-census.sh:501    dir_abs=$(realpath -- "$(dirname -- "$file_abs")/..")
scripts/sources-census.sh:567    printf '%s\tE11\t%s missing used-by %s\n' …
```

so every repo-relative `used-by` cell resolves against the temp dir:

```
$ T=$(mktemp -d); cp corpus/SOURCES.md "$T/SOURCES.md"
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$T/SOURCES.md"
file	E11	S001 missing used-by corpus/lessons/2026-10-15-free-lunch-measurements-counter-baselines.md
…
(279 E11 lines, 277 of them pre-existing rows)
exit=1
```

The same bytes in roster mode are green (`evidence/census-start.txt`: "mori ok … rows=243",
exit 0). So the arm can only pass if the staged file sits in `<lane>/corpus/` — which the
counter never does. **Consequence: `C3=met` is unreachable this round**, and the round
must record `C3=unmet` with this cause rather than hunt for an entry fix. The instrument
is frozen: route to round 45, do not patch (`contract.md` Freeze).

**Do not take the shortcut.** Pointing `--census` at a wrapper that ignores `--file` and
runs `validate --root … mori` would turn the arm green while validating the *working
tree*, not the measured revision — a vacuous arm that passes on a red registry. That is
instrument gaming, not a fix.

**Independent vacuity, same counter.** None of the five checks reads the entry body's
ground, its quotations, or the recheck's output; `entry_meta` only tests for the literal
strings `verified-at:`/`recheck:`/`coverage-map:` (`:102-111`). Its own green fixture
proves it: `:162` `recheck: 90d — \`true\` -> 1 (ran 2026-10-25)` — a command that prints
nothing and asserts the observed value 1 — and the counter scores it green
(`selftest PASS registered_entry_met`). Its fixture census is `exit 0` (`:172-173`), which
is why the staging defect is invisible to `--selftest`.

**Counterexample that the counter cannot tell this round's entry from a replay.** In a
sandbox clone (writes confined to `mktemp -d`), I committed an entry that restates S170/
S171 in English, carries the same fabricated `recheck: … \`true\` -> 1`, and two rows that
**duplicate S170/S171's URLs** (`status mined`, `used-by` the replay entry):

```
check entry_present    PASS (729 bytes)
check entry_meta       PASS (sources S471,S472)
check rows_present     PASS (rows S471,S472 mined)
check census_ok        FAIL (exit=1)          <- §6, structural
check readme_row       PASS (names entry)
C3=unmet
```

`readme_row` was the only fixable difference and a sibling closed it mid-review (the
README row now carries the repo-relative `corpus/knowledge/pid-probe-conclusion-r44.md`,
which the check demands literally; the house style `knowledge/…` alone fails it).

---

## 7. Lesson Gate — the admit/reject pair

### 7.1 Strongest package REJECT — `failed-scope-keeps-limit-r50.md`

Three independent grounds, any one sufficient:

1. **Its own-work source is a campaign scratch path.** S581 =
   `/home/vgpnk/Projects/shokuknow/lanes/mori/round14/.deepresearch/notes/r14-failed-scope.txt`
   (exists, 1284 B, mtime 2026-10-24 18:37). That tree is read-only to this lane and can
   never be committed here — FR9's boundary ("scratch paths … are not durable evidence")
   and QUALITY 23's rule by analogy. Round 43 already refused a campaign `file://` source
   (`corpus/README.md:624`: "Two assimilation entries on adjacent ground were refused
   (campaign file:// plus a MESSAGE grep; `reset-failed` host mutation)").
2. **Its recheck is a host mutation.** `recheck: 90d — create a scope, oom-kill it, then
   \`systemctl --user show -p MemoryMax <unit>.scope\` before and after \`systemctl --user
   reset-failed <unit>.scope\``. mori's `PROVINCE.md:16` is "Detection and report only —
   never remediation"; round 43 refused exactly the `reset-failed` mutation.
3. **Its causal verdict adjudicates another lane's code** ("The runner destroys it
   deliberately"). Mori may observe that the property reads `infinity` after a reset; it
   does not own the runner's design.

**Flip.** Re-ground S581 on a committed lane receipt from a **pre-existing** failed scope,
read-only (`systemctl --user show -p MemoryMax,LoadState,ActiveState,Result <unit>`), make
the recheck a read (no create, no oom-kill, no `reset-failed`), and reduce the verdict to
the observation ("the runner calls `reset-failed`; after it the property reads
`infinity`"), dropping the intent attribution.

### 7.2 Runner-up REJECT — `journal-reach-at-ceiling-r46.md`

Same campaign-source class (S537 =
`file:///home/vgpnk/Projects/shokuknow/lanes/mori/round9/.deepresearch/notes/r9-journal-reach-now.txt`,
exists, 1529 B), plus a headline that is a *transient host state* ("already over its
ceiling", 258.3M vs 256M) and a recheck whose observed values (258.3M, 67) can never
reproduce tomorrow — a recheck that expects a snapshot is not a recheck.

**Flip.** Keep S532 (`journalctl(1)`) for the rule; replace the snapshot with a read-only
predicate (`--disk-usage` value ≥ the configured ceiling; `oom_kill` counter equal to the
retained kill records in the same boot), and mark the numbers as a dated observation.

### 7.3 Strongest package ADMIT — `effective-limit-is-cross-level-r44.md`

Real durable URL (S517 `systemd.resource-control(5)`), read-only, in-province (the cgroup
limit chain is the kill/limit plane mori already reads), and its ground is **not** held:
`grep -rn 'most stringent\|most restrictive' corpus/` → no hit. Its recheck reproduces —
I ran it:

```
$ curl -fsSL https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html | grep -c 'the most stringent limit of the unit and parent slices'
1
exit=0
```

Two conditions before admission: (i) its `coverage-map:` names **FR12** (PSI watchers),
whose boundary is about resident trigger watchers — the content is the cgroup limit chain;
map it to the limit/kill ground instead; (ii) its campaign ids (S517/S519/S522) must be
re-minted as lane rows with lane `used-by` values.

---

## 8. Environment note (not my ticket, but it broke my first sandbox)

`/tmp` is **100% full**: `df -h /tmp` → `128G 128G 100K 100%`. My first sandbox died with
`fatal: sha1 file '…/.git/index.lock' write error. Out of diskspace`; I moved scratch work
to `mktemp -d -p /home/vgpnk/.cache/mori44-crit` (562G free). Seats writing artifacts
under `/tmp` will fail, and `count-c3.py` stages into `tempfile.mkdtemp` (honours `TMPDIR`),
so the instrument itself is one large artifact away from a setup error. This is mori's own
resource-runway ground: report, never remediate.

## 9. What I ran, and what I did not

Ran (read-only or sandbox-only): `git grep`/`git show`/`git merge-base` at `1429c791` and
HEAD; `count-c3.py` at the entering tip, on `WORK`, and `--selftest`; the fleet census in
`--file` staging mode and in roster mode; `curl` of the two staged pages, the man-pages
6.20 `proc_pid_cmdline.5`, and `systemd.resource-control.html`; the entry's two recheck
commands verbatim; contiguous/normalized quote counts and a char diff; one sandbox clone
with a replay entry and two duplicate-URL rows (committed **inside `mktemp -d`**, never in
the lane repo).

Did not run: any write to the lane checkout, `SKILL.md`, `SCORECARD.md`, `LOG.md`,
`corpus/`, the frozen instruments, or any sibling repo; any `git add/commit/push` in the
lane; any jj command; any campaign tool under `/home/vgpnk/Projects/shokuknow`; any host
mutation. No tool was installed or upgraded.

Impacted axes: **coverage** (C3 claim is replay), **calibration** (token sweep, `census_ok`
staging, `readme_row` literalness), **freshness** (recheck counts a word; quotations not
byte-exact).
