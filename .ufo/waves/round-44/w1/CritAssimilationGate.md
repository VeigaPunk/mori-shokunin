# CritAssimilationGate — C3 admission falsified (mori round 44, wave 1)

**Verdict.** *In province: yes* (§3). *Clears the lane's bar: **no** — as written* (§5, five
checkable failures, all mechanical). *Frozen instrument: **C3=unmet***, and one of its five
arms is structurally red on this lane (§6) — an instrument defect, not an entry defect.

Judged bytes: `corpus/knowledge/pid-probe-conclusion-r44.md`, sha256
`3ad7992f93be33bc46bf7da070e05b6bc6a2170cb74231dabb35c69c83a1e082`, 6186 bytes; rows
`corpus/SOURCES.md:250-251`; README row `corpus/README.md:632`; working tree at HEAD
`7cb59c6891d4f5d0266fe062565f094da835dc84` (entering tip `1429c791…` is an ancestor:
`git merge-base --is-ancestor 1429c791 HEAD` → true).

**The entry is a moving target.** It changed twice while I reviewed it (5526 B → 6186 B;
the claim moved from "three worlds, the state field is the discriminator" to "two
documented worlds, one measured world, one retired"). Every line number below is against
the sha above. A Gate that scores a file that keeps changing is scoring a different claim
than the one it read (QUALITY 33: hash every verdict-driving input); **freeze the bytes
before the Gate decides**, and re-run `count-c3.py` on the frozen sha.

---

## 1. The frozen instrument's verdict, first

```
$ python3 .ufo/waves/round-44/count-c3.py WORK --row S471 --row S472
check entry_present    PASS (6186 bytes)
check entry_meta       PASS (sources S471,S472)
check rows_present     PASS (rows S471,S472 mined)
check census_ok        FAIL (exit=1)
check readme_row       PASS (names entry)
rev=WORK
C3=unmet
```

Declared Before, reproduced exactly:

```
$ python3 .ufo/waves/round-44/count-c3.py 1429c791db5891c484684feef893799909d2d6a8 --row S471 --row S472
check entry_present    FAIL (absent)
rev=1429c791db5891c484684feef893799909d2d6a8
C3=unmet
exit=1
```

`--selftest` at the frozen sha (`a12170f1…c440c68`, matches `evidence/freeze-r44.txt:5`):
`C3_SELFTEST pass=6 fail=0`, exit 0.

Four of five checks green; the fifth red for a cause no entry can fix (§6). The claim
**cannot print `C3=met` this round**.

---

## 2. What the round actually adds (the part worth admitting)

Against the entering tip the lane holds: the `cmdline` zero-character rule (S170,
`corpus/SOURCES.md:176`); the `Z` row and its verdict (`corpus/knowledge/watchdog-identity-r31.md:29`);
the state-letter positions `Z at :56-57, X at :69-70` (S171, `corpus/SOURCES.md:177`);
the kernel-thread population (`corpus/knowledge/oom-victim-selection-r27.md:107`, "kernel
threads | 668"). It does **not** hold any of the three things the current entry adds:

1. **The mm-less world.** A zero-length `cmdline` read is coextensive with an empty
   `/proc/<pid>/maps` on this host, so the *state letter* does not separate an mm-less
   kernel thread (`I`) from a sleeping user task (`S`). `grep -rIn -F 'mm-less' corpus/`
   before this entry → 0 files.
2. **The ENOENT boundary.** A pid that does not exist is not an empty read:
   `open("/proc/999999/cmdline")` → `OSError errno=2` (I reproduced it).
3. **The two-translation disagreement** on the `comm`/swap coupling, and the zh `state`
   field's five-letter `"RSDZT"` (no `X`) — verified on the page.

That is real, in-province, and useful to FR5. The entry's own §"What the lane already
holds" (`:12-17`) now says so honestly. One stale bullet contradicts it (§5.1).

---

## 3. (a) Province — fleet observability or host diagnosis?

**mori, `PROVINCE.md:6-10` (Owns, read-only probes):** "shokunin watchdog liveness (pid,
start time, log freshness, lane counters)"; Frontier **FR5** (`PROVINCE.md:48`):
"Watchdog daemon identity and degraded-pgrep visibility … Boundary: **an unavailable pid
probe is not absence**, and argv-substring matches do not establish daemon identity."

**mori, `PROVINCE.md:12-16` (Refuses):** "OS package, systemd unit, driver/firmware and
boot state (→ tsukuroi) — mori reads journal and cgroup events as fleet evidence and
reports them, never owning OS state … **Detection and report only — never remediation.**"

**tsukuroi, `PROVINCE.md:3-8`:** "the OS substrate itself: package state, systemd,
drivers/firmware, boot health", with owned surfaces including "systemd user units &
timers (`systemctl --user`, unit files, **failed states**), journal/boot triage … driver/
firmware plane".

**tsukuroi, `PROVINCE.md:24-27` (the handoff to mori):** "Host memory and kill-event
measurements support OS triage; they do not establish which fleet wave caused pressure or
whether an endpoint works. … **fleet correlation belongs to mori**."

**Verdict: in province.** The subject is what a liveness probe may conclude from a
zero-character read — FR5's own boundary sentence. The entry refuses every crossing:
no daemon identity (`:67-68`), no crash cause (`:71-72`), no census change (`:69-70`), no
remediation, no host-state diagnosis.

Two province notes the round should carry:

- **The load-bearing reading is a host-wide process census** (1931 `/proc` entries, `:31-34`),
  not watchdog liveness. mori's Core already carries host-scope readings as *evidence to
  correlate* (r24 pressure: "The reading is host scope … never proof that a lane, a wave or
  the fleet caused it"). The entry must keep that label: a host `/proc` distribution is
  host-scope evidence for a probe-design question, never a fleet fact, and never a claim
  about kernel-thread health (which would be tsukuroi's plane).
- **The swap/`comm` disagreement stays provenance, not host memory.** The entry refutes the
  coupling rather than asserting it (`:39-43`), which is the correct fence. The registry
  row does not keep that fence (§5.4).

---

## 4. (b) Is the Z/X alphabet already held? Yes — and the round's sweep cannot see it

```
$ git grep -l 'Z ゾンビ' 1429c791db5891c484684feef893799909d2d6a8 -- corpus/
(no output)   rc=1
$ git grep -n 'Z at :56-57' 1429c791… -- corpus/SOURCES.md
1429c791…:corpus/SOURCES.md:177:| S171 | … field 3 state letters (S at :49-50, Z at :56-57, X at :69-70) … | mined | … | corpus/knowledge/watchdog-identity-r31.md |
```

`watchdog-identity-r31.md:29` already carries the `Z` row ("`Z (zombie)` is the zombie
state … absent (exited, unreaped)"), and `corpus/SOURCES.md:176` (S170) already carries the
sentence "a zombie reads 0 bytes, so an empty read cannot separate a dead watchdog from a
live zombie one". So the alphabet *as a set*, and two of the three worlds, were held at the
entering tip.

What that means for the round:

1. The frozen Before/After token (`Z ゾンビ`) is a literal sweep **blind to held ground** —
   it reads 0 while `SOURCES.md:177` holds the alphabet — and it reads 1 on a string the
   entry stitched: neither page carries `Z ゾンビ` or `X 死亡` contiguously. Measured:
   `ja.count('X 死亡')` → 0; the page has `<dt id="Z">Z</dt><dd>ゾンビ (Zombie)</dd>` and
   `<dt id="X">X</dt><dd>死亡 (Dead) (Linux 2.6.0 以降)</dd>`. The After value measures the
   entry's typography, not the source's text.
2. The honest coverage sentence is the one the entry now writes at `:12-17` — *the letters
   are held; the mm-less world, the ENOENT boundary and the translation disagreement are
   new* — and **not** the stale bullet at `:63` ("This entry adds the state alphabet").
   That bullet is the replay claim; it must go (§5.1).
3. QUALITY 108 says a binding is checked for **resolvability, not token presence**. This
   instrument checks presence and not resolvability; the two rules that would have caught
   §5.3/§5.5 are exactly the ones missing.

---

## 5. (c)+(d) Does it clear the lane's bar? Five failures, then the flip

### 5.1 The coverage claim contradicts itself (QUALITY 25)

`:12-14` discloses that `watchdog-identity-r31.md:27/:29` and S171 already hold the read and
the `Z`/`X` letters; `:63` then says "This entry adds the state alphabet". Both cannot
stand. The claim is admitted at the scope measured — the narrow one.

### 5.2 The load-bearing mechanism is asserted, not measured (QUALITY 2)

`:35-38`: "**This is the load-bearing reading …** The discriminator is the absence of an
`mm`, not the state field." The committed receipt
(`.ufo/waves/round-44/evidence/cmdline-empty-by-state.txt`) states its method as:

> `# method: read-only; for every /proc/<pid>, read stat field 3 (state) and the length of cmdline bytes; no write, no signal, no cgroup change`

— it never reads an mm indicator, yet its own `# reading:` line concludes "a state I or S
task **with no mm** (kernel threads)". The mm claim is an inference riding inside a
measurement file, and the entry then promotes it to *the discriminator*.

I tested it (read-only, `read()` not `stat()`): of 920 scannable `/proc` entries, 691 read a
zero-length `cmdline` and **all 691 have an empty `/proc/<pid>/maps`**; of the 229 with a
non-empty `cmdline`, **none** has an empty `maps`. So the claim is *true* — but it is not
sourced in the entry or in the receipt, and the fix is one read plus one line in the method.

### 5.3 The counts carry no command and do not reproduce (CORPUS "A count carries its command")

The receipt records `pids_scanned=1931 empty_cmdline=1698 empty_by_state=I=1489 S=209` with
a timestamp and a method sentence but **no command**. Two re-runs 25 minutes later:

```
run 1: proc entries 1120, zero-length 886, zero-length states {S:209, I:677}
run 2: scanned 920,        zero-length 691, zero-length states {S:209, I:482}
```

The *shape* reproduces (every empty read is `I` or `S`, no `Z`/`X` at either instant) and
`S=209` is stable; the totals and the `I` count do not. A live `/proc` count is inherently
transient: it must be written as a dated snapshot with its command and must not be load-
bearing. As written, 1931/1698/1489 cannot be recomputed by a reader.

### 5.4 The registry row keeps an unswept negative about S170 (CORPUS "A negative claim carries its sweep")

`corpus/SOURCES.md:251` (S472 `scope`): "… including a swap-out branch the modern English
contract the lane holds **does not state**". The file the lane already mines states it:

```
$ curl -fsSL 'https://git.kernel.org/…/man/man5/proc_pid_cmdline.5?h=man-pages-6.20' | grep -n -i swap
15:.\" In Linux 2.3.26, this also used to be true if the process was swapped out.
```

It is a roff comment (not rendered) and S170's `anchor` cell (`:176`) omits line 15. The
honest cell reads "S170 carries the swap-out note as a commented-out historical note at
`:15`, outside its anchor list".

### 5.5 The quotations are assemblies, and one is silently re-punctuated (QUALITY 108)

Measured on the fetched bytes (contiguous / whitespace-normalized occurrences):

| quote | contiguous | normalized |
|---|---|---|
| ja cmdline (`:26-27`) | 0 | 1 |
| ja comm (`:41`) | 0 | 1 |
| zh cmdline (`:29-30`) | **0** | **0** |

The zh one is an edit, found by char diff: the page reads
`…在該檔案裡,這時候對該檔案的讀操作將返回零個字元.`; the entry writes `…在該檔案裡，…零個字元。`
— two punctuation substitutions (`,`→`，`, `.`→`。`). The `recheck` counts `僵死` and
cannot see it. The ja quotes are whitespace-split by the HTML and must either be declared
as a collapse or anchored by the ids the page exposes (`#cmdline`, `#Z`, `#X`, `#state`,
`#comm`).

Two smaller provenance items in the same class:

- `:22` and `:34` cite `evidence/cmdline-empty-by-state.txt`, which **does not resolve from
  the repo root**; the file is at `.ufo/waves/round-44/evidence/cmdline-empty-by-state.txt`
  (QUALITY 9: every path pointer resolves at the carrying commit).
- `:53-54` calls `X` "a teardown-window state" — an unsourced gloss presented as
  documentation (QUALITY 3: observation, inference and unknown stay separate).

### 5.6 The recheck reproduces but tests a word (attack (c))

Run verbatim from `:6`: `…count("ゾンビ")` → **3**, `…count("僵死")` → **2**. Both correct
today — and worth noting against the campaign source entry the draft was told to follow
(`probe-absent-vs-dead-r39.md:6`: `curl … | grep -c 'ゾンビプロセス'` → "1"; run verbatim it
prints **0**, rc=1, because both pages entity-encode CJK: literal `ゾ` = 0 / `&#x30BE;` = 4;
literal `僵` = 0 / `&#x50F5;` = 2. The draft correctly avoided that trap.)

But it counts a bare word. `ゾンビ` occurs in three unrelated places (cmdline sentence, `Z`
glossary `dd`, `stat` State list); `僵死` in two. A page that kept the words and dropped the
sentences still passes. A claim-bearing recheck counts `このファイルは空となる` → 1,
`スワップアウトされているかどうかによらず` → 1, `RSDZT` → 1. The line also packs **two**
commands where the wave spec asks for one runnable command per `recheck:`.

### 5.7 The flip (all six are mechanical; none changes the claim)

1. Delete the "adds the state alphabet" bullet (`:63`) and keep only the narrow claim.
2. Add the mm read to the receipt's method and to the entry's anchor for the load-bearing
   sentence (e.g. "691/691 zero-length `cmdline` pids read an empty `/proc/<pid>/maps`;
   229/229 non-empty ones did not — `<command>`, 2026-10-25").
3. Give the counts their command and label them a dated snapshot; drop any dependence on
   the exact totals.
4. Fix S472's `scope` cell to cite `proc_pid_cmdline.5:15` (or delete the negative).
5. Quote byte-exactly (ASCII `,`/`.` in the zh sentence) or declare the whitespace collapse
   and anchor the `dt`/`dd` ids; fix the `evidence/…` path to `.ufo/waves/round-44/evidence/…`;
   mark "teardown-window" as inference.
6. Split the `recheck:` into one command per line, each counting a claim-bearing string.

**Admit after the flip — as a translation-and-measurement entry on FR5, not as an alphabet
advance.** And record that the C3 predicate's "three worlds" is now *two documented, one
measured, one retired* (the entry's own title), which is a narrowing the round report must
state (QUALITY 25) rather than claim the predicate's wording.

---

## 6. The frozen instrument: `census_ok` is structurally red on this lane

`count-c3.py` stages the registry into a temp dir and runs the census against the staged
file (`:133` `tempfile.mkdtemp(prefix="c3-")`; `:139` `["bash", census, "validate", "--file",
staged]`, `cwd=repo`). The census derives the lane root from the **file**, not from `cwd`:

```
scripts/sources-census.sh:501    dir_abs=$(realpath -- "$(dirname -- "$file_abs")/..")
scripts/sources-census.sh:567    printf '%s\tE11\t%s missing used-by %s\n' …
```

so every repo-relative `used-by` resolves against the temp dir:

```
$ T=$(mktemp -d); cp corpus/SOURCES.md "$T/SOURCES.md"
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$T/SOURCES.md"
file	E11	S001 missing used-by corpus/lessons/2026-10-15-free-lunch-measurements-counter-baselines.md
… (279 E11 lines; 277 are pre-existing rows)
exit=1
```

The same bytes in roster mode are green (`evidence/census-start.txt`: `mori ok … rows=243`,
exit 0). **Consequence: `C3=met` is unreachable this round**; record `C3=unmet` with this
cause. The instrument is frozen — route to round 45, do not patch (`contract.md` Freeze).

**Do not take the shortcut.** Pointing `--census` at a wrapper that ignores `--file` and runs
`validate --root … mori` would green the arm while validating the *working tree*, not the
measured revision — a vacuous arm that passes on a red registry.

**Independent vacuity, same counter.** No check reads the entry body's ground, its
quotations, or the recheck's output; `entry_meta` tests for the literal strings
`verified-at:`/`recheck:`/`coverage-map:` only (`:102-111`). Its own green fixture proves
it: `:162` `recheck: 90d — \`true\` -> 1 (ran 2026-10-25)` — a command that prints nothing
and asserts 1 — scores green (`selftest PASS registered_entry_met`), and its fixture census
is `exit 0` (`:172-173`), which is why the staging defect is invisible to `--selftest`.

**Counterexample: the counter cannot tell this entry from a replay.** In a sandbox clone
(writes confined to `mktemp -d`) I committed an entry restating S170/S171 in English with the
same fabricated `recheck: … \`true\` -> 1` and two rows that **duplicate S170/S171's URLs**
(`mined`, `used-by` the replay entry):

```
check entry_present    PASS (729 bytes)
check entry_meta       PASS (sources S471,S472)
check rows_present     PASS (rows S471,S472 mined)
check census_ok        FAIL (exit=1)          <- §6, structural
check readme_row       PASS (names entry)
C3=unmet
```

`readme_row` was the only fixable difference; a sibling closed it mid-review (the README row
must carry the repo-relative `corpus/knowledge/pid-probe-conclusion-r44.md`, which the check
matches literally; the house style `knowledge/…` alone fails).

---

## 7. Lesson Gate — the admit/reject pair

### 7.1 Strongest package REJECT — `failed-scope-keeps-limit-r50.md`

Three independent grounds, any one sufficient:

1. **Its own-work source is a campaign scratch path.** S581 =
   `/home/vgpnk/Projects/shokuknow/lanes/mori/round14/.deepresearch/notes/r14-failed-scope.txt`
   (exists, 1284 B, 2026-10-24 18:37). That tree is read-only to this lane and can never be
   committed here — FR9 ("scratch paths … are not durable evidence"), QUALITY 23 by analogy.
   Round 43 already refused a campaign `file://` source (`corpus/README.md:624`).
2. **Its recheck is a host mutation**: "create a scope, oom-kill it, then `systemctl --user
   show -p MemoryMax` … before and after `systemctl --user reset-failed`". mori's
   `PROVINCE.md:16` is "Detection and report only — never remediation"; round 43 refused
   exactly the `reset-failed` mutation.
3. **Its causal verdict adjudicates another lane's code** ("The runner destroys it
   deliberately"). Mori may observe that the property reads `infinity` after a reset; it does
   not own the runner's design.

**Flip.** Re-ground S581 on a committed lane receipt from a **pre-existing** failed scope,
read-only (`systemctl --user show -p MemoryMax,LoadState,ActiveState,Result <unit>`), make the
recheck a read (no create, no oom-kill, no `reset-failed`), and reduce the verdict to the
observation.

### 7.2 Runner-up REJECT — `journal-reach-at-ceiling-r46.md`

Same campaign-source class (S537 =
`file:///home/vgpnk/Projects/shokuknow/lanes/mori/round9/.deepresearch/notes/r9-journal-reach-now.txt`,
exists, 1529 B), plus a headline that is a transient host state ("already over its ceiling",
258.3M vs 256M) and a recheck whose observed values (258.3M, 67) can never reproduce — a
recheck that expects a snapshot is not a recheck.

**Flip.** Keep S532 (`journalctl(1)`) for the rule; replace the snapshot with a read-only
predicate (`--disk-usage` ≥ the configured ceiling; `oom_kill` counter equal to the retained
kill records in the same boot), and mark the numbers as a dated observation.

### 7.3 Strongest package ADMIT — `effective-limit-is-cross-level-r44.md`

Real durable URL (S517 `systemd.resource-control(5)`), read-only, in-province (the cgroup
limit chain is the kill/limit plane mori already reads), and its ground is not held
(`grep -rn 'most stringent\|most restrictive' corpus/` → no hit). Its recheck reproduces — I
ran it:

```
$ curl -fsSL https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html | grep -c 'the most stringent limit of the unit and parent slices'
1
exit=0
```

Two conditions: (i) its `coverage-map:` names **FR12** (PSI watchers) whose boundary is about
resident trigger watchers — remap it to the limit/kill ground; (ii) re-mint its campaign ids
(S517/S519/S522) as lane rows with lane `used-by`.

---

## 8. Environment note (not my ticket; it broke my first sandbox)

`/tmp` is **100% full**: `df -h /tmp` → `128G 128G 100K 100%`. My first sandbox died with
`fatal: sha1 file '…/.git/index.lock' write error. Out of diskspace`; scratch moved to
`mktemp -d -p /home/vgpnk/.cache/mori44-crit` (562G free). Seats writing under `/tmp` will
fail, and `count-c3.py` stages through `tempfile.mkdtemp` (honours `TMPDIR`), so the
instrument is one large artifact away from a setup error. This is mori's own resource-runway
ground: report, never remediate.

## 9. What I ran, and what I did not

Ran (read-only or sandbox-only): `git grep`/`git show`/`git merge-base` at `1429c791` and
HEAD; `count-c3.py` at the entering tip, on `WORK`, and `--selftest`; the fleet census in
`--file` staging mode and in roster mode; `curl` of the two staged pages, man-pages 6.20
`proc_pid_cmdline.5`, and `systemd.resource-control.html`; the entry's two recheck commands
verbatim; contiguous/normalized quote counts and a char diff; two read-only `/proc` scans
(state, `cmdline` length, `maps` length; no argv content printed, no signal sent); one sandbox
clone with a replay entry and duplicate-URL rows, committed **inside `mktemp -d`**.

Did not run: any write to the lane checkout, `SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/`,
the frozen instruments, or any sibling repo; any `git add/commit/push` in the lane; any jj
command; any campaign tool under `/home/vgpnk/Projects/shokuknow`; any host mutation. No tool
was installed or upgraded.

Impacted axes: **coverage** (alphabet held; the new ground is mm-less + ENOENT, not the
alphabet), **calibration** (token sweep, `census_ok` staging, `readme_row` literalness,
command-less counts), **freshness** (recheck counts a word; quotations not byte-exact).
