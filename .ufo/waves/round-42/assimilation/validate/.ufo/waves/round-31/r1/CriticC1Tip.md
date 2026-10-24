# CriticC1Tip — falsify C1 at tip a29f3e3f (residual seat, critic)

Seat: MoriR31.CriticC1Tip (non-author). Tip judged: committed bytes of
`a29f3e3f7f7259afb07df29c5ee8f68882712e96`. The judge receipt (`r1/JudgeC1Rows.md`) is another seat's work and is out
of scope here.

## Verdict

Every P-C1-A1 condition other than the judge holds at the tip; I could not break any of them mechanically. I did find
one real content defect, a fixable one: the `/proc/locks` row (entry row 14, SKILL row at `SKILL.md:770`) and the
Limits note `watchdog-identity-r31.md:46-48` make claims that are false for this watchdog. Its verdict `alive` can be
a false positive, and the PID it tells the reader to check is never the watchdog. A judge should mark row 14
`unsupported`. That alone does not stop the claim: 13 rows remain, all of them citing a new id, and A1 needs at least
8 supported, of which at least 6 cite a new id. Nothing in this review calls for amending the predicate. The only
needed change is to the entry text.

## Counters re-run (exercised)

- `timeout 120 python3 .ufo/waves/round-31/count-c1.py a29f3e3f…` printed `rows=14 rows_ok=14 new_id_rows=14
  new_ids=12`, `gates_ok=12/12 copies_ok=12/12 fetch_ok=12/12`, `skill_rows=6` and `C1=met`, with exit 0.
- `timeout 200 python3 .ufo/waves/round-31/count-c1-a1.py a29f3e3f…` printed `html_comments=0`, `distinct_rows=14`,
  `short_readings=0`, `distinct_sources=yes`, `rows_without_quote_overlap=0`, `judge=absent`, `skill_rows=6`,
  `unmet_conditions=judge` and `C1=unmet`, with exit 1. That is the expected result before the judge receipt lands.
- I compared this output with `evidence/c1-after-prejudge.txt`. With the `$ python3` lines stripped and the revision
  normalised, `diff` printed `IDENTICAL`. The receipt was measured at `458ff1c3`, not at the tip.
  `git diff --name-only 458ff1c3 a29f3e3f -- corpus SKILL.md tools | wc -l` printed `0`, because the tip commit adds
  only `.ufo/waves/round-31/` files. So the receipt still describes the tip's C1 bytes.

## Findings, ranked

### F1 — major, fixable: the `/proc/locks` row's PID and `alive` verdict do not hold for this watchdog

Here is how the watchdog takes its lock (fleet `scripts/shokunin-watchdog.sh:381-382`):
`exec {LOCKFD}>"$UFO/.watchdog.lock"` followed by `flock -n "$LOCKFD"`. The lock is acquired by the `flock(1)`
utility, which is a separate child process that exits straight away. The bash watchdog only keeps the descriptor open.

1. **The PID shown is never the watchdog's.** The kernel stores the PID of the process that called flock(2):
   `fl->c.flc_pid = current->tgid;` in `flock_make_lock`, Linux v7.2 `fs/locks.c:490` (fetched from
   `https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/locks.c`, sha256 `a7fe7bd0…aa60d1`). It also keeps
   printing that PID after the process dies (`fs/locks.c:2387-2391`: "If the flock owner process is dead and its pid
   has been already freed … we still want to show flock owner pid number in init pidns").
   I reproduced the watchdog's two lines in a throwaway script (`/fast/scratch/hyaku/mori-r31/CriticC1Tip/wd2.sh`). The
   results were: `lock pid == watchdog bash pid: no` and `lock pid alive (/proc/<lockpid> exists): no`.
   So the instruction at `SKILL.md:770`, "names the pid that owns the watchdog's singleton lock … check that pid's start
   time and cmdline next", can never succeed. The same goes for the entry's `:47-48` instruction "Compare the owning
   pid's start time (field 22) and cmdline". If that PID is later reused, the check reads an unrelated process.
   The Limits note at `:46` says the row "assumes the lock is held by the process that ran `flock`". For this watchdog
   that assumption is always false, not an edge case.
2. **`alive` can be a false positive.** Every child of `main()` inherits the descriptor. `launch_lane` closes it only
   for lane spawns (`:208-212`). The tick `sleep "$INTERVAL"` (`:407`, default 450 s per `:6`) does not close it.
   In my probe I sent SIGKILL to the script's bash process while it was in `sleep`. The results were: `watchdog bash
   alive: no`, `lock lines after kill=1`, and `flock -n exit=1 (1 = still held)`. In other words, a FLOCK WRITE line on
   the lock inode stays visible for up to one tick after the watchdog is dead.
   util-linux `flock(1)` documents the same mechanism. Its `--close` option exists "if _command_ spawns a child process
   which should not be holding the lock" (`sys-utils/flock.1.adoc:72`, tag v2.41).
3. **Wording.** Row 14's "the watchdog takes a flock on that file at start" describes the wrong actor: the helper
   process takes the lock on an open file description the watchdog shares.

Impacted axes: depth (a decision row that would lead a reader to act wrongly) and discernment. No predicate condition
fails. This is the "reading follows from quote" residual that the contract leaves to non-authors. S174's quote is
accurate. What goes wrong is applying it to a lock taken through a helper process.

Smallest safe correction:

- Change row 14's verdict to `candidate (lock held by some holder of the descriptor)`.
- Change its reading to say that the PID field is the process that called flock(2). Here that is the short-lived
  `flock -n` helper, so the field never names the watchdog. The lock can also outlive a killed watchdog for up to one
  tick, while its `sleep` child still holds the descriptor.
- Delete the "check that pid's start time and cmdline" advice in `SKILL.md:770` and in the entry at `:46-48`.
- Cite the live probe as lane evidence. Citing `fs/locks.c` would need a new SOURCES row and Gate row first, and that
  is optional.

Both texts change, so both counters must be re-run before the judge scores. The row keeps S174 and stays a new-id
row.

### F2 — minor: the SKILL grounding pointers drift from the entry rows they cite

- `SKILL.md:769` cites entry "rows 9–11", but its text carries only rows 10–11 (start time and PID reuse). Row 9 (the
  `Z` state) is not reflected anywhere in it.
- `SKILL.md:766` states that the env shebang "makes its name `bash`". That rests on entry row 4, which cites
  S164 and S165, yet the SKILL row's grounding lists S161–S164 and omits S165.

Neither affects any predicate. The fix is to re-point the first row at rows 10–11 and add S165 to the second.

### F3 — none found in the other assigned checks

- **SKILL rows are real decisions.** Rows `SKILL.md:765-770` each pair a situation with "What to conclude" and "What not
  to conclude", and each matches the entry rows it cites, except as noted in F1 and F2. 6 lines name both `Round31`
  and `corpus/knowledge/watchdog-identity-r31.md`, counted with `grep -c` on lines 757–771 (output `6`).
- **No contradiction with existing lane entries.** I ran `git grep -nwiE 'comm|pgrep|cmdline' a29f3e3f --
  corpus/knowledge` with the new entry excluded, then checked each hit:
  - `audit-r11.md:201` (D06, the open argv-substring false-positive class) agrees with rows 1–2.
  - `observability-surfaces-r2.md:105-110` (an editor match is counted; the filter drops only `pgrep` lines) agrees
    with rows 1–2.
  - `oom-victim-selection-r27.md:30` (comm is at most 15 bytes) agrees with rows 5–6.
  - `observability-census-r1.md:31` and `observability-surfaces-r2.md:59` (`WATCHDOG_ABSENT` when pgrep finds no
    match) agree with row 12, which scopes that absence to the one query.
  - The `comm` hits in `roster-truth-r12.md` and `surfaces-r8.md` refer to coreutils `comm`, which is unrelated.
  - The entry's own citations hold: `tools/mori-census.sh:711-715` is the `pgrep -af` filter and `:716-720` is the
    missing-binary arm.
- **The new ids' URLs are new.** For each of the 12 admitted URLs (S161–S165, S167, S169–S174), `grep -cF` against
  `git show a12c68ae:corpus/SOURCES.md` printed `0`. A looser search for each file's path stem (for example `pgrep.c`,
  `fs/proc/array.c`, `proc_locks`) also printed `0`, so no new id renumbers a file that was already registered. The
  only URLs present at `a12c68ae` were `fs/proc/base.c` (2 hits) and `proc.rst` (1 hit). Those belong to the rejected
  S166 and S168, which is correct.
- **S166 and S168 are cited nowhere they should not be.** `grep -nE 'S16[68]'` on the entry exited 1 (no match), and
  the same search on SKILL lines 757–771 exited 1. `git grep -nE 'S16[68]\b' a29f3e3f -- corpus/knowledge SKILL.md
  corpus/README.md` printed nothing. Both appear only as rejected rows in `corpus/SOURCES.md` (tip lines 172 and 174).
- **Privacy.** I grepped the entry and SKILL lines 757–771 for `uid`, PID-plus-digits, digit runs of 3 to 7,
  `user-N`, `user@N`, `session` and `.omp`. The only hits were line numbers, versions and log counts. The counts
  `208` and `3` at `:38` match `.ufo/watchdog.log` now: `grep -c 'driver=hyaku-inline'` gives 208 and
  `grep -cE 'driver=hyaku( |$)'` gives 3. There is no PID, uid or session value, and `environ` is explicitly
  excluded at `:62-63`.
- **Depth is the right axis by surface (prompt section 6, item 9).** The surface that changes is a new sourced decision
  table: the knowledge entry plus the SKILL rows, on FR5 ground. That fits AXES.md's depth definition (`AXES.md:11`:
  "decision tables with real thresholds, named error signatures, cited sources"). The census probe is unchanged
  (`:60`), so this is not coverage. Is it "re-scoring a rule the lane already holds"? Only rows 1, 2 and 5 restate
  lane facts (from audit-r11, surfaces-r2 and r27). The other 11 rows hold facts the lane did not have, which is above
  the floor of 8 even if those three are discounted. The do-nothing state also shows the surface unmoved:
  `count-c1.py a12c68ae` gives `entry=absent` (contract `:13-14`). The counter cannot be met with a sourceless table
  either, as controls (a) and (b) show.

## Conditions table — P-C1-A1 without the judge

| condition | state at tip | evidence |
|---|---|---|
| P-C1 (all of count-c1.py) | met | `C1=met`, exit 0 |
| no HTML comment, table outside a code fence | met | `html_comments=0`, `decision_tables=1` |
| rows pairwise distinct, readings at least 8 words | met | `distinct_rows=14 short_readings=0` |
| new ids mined, URL new at a12c68ae, URL and sha256 distinct | met | `distinct_sources=yes`, plus my `grep -cF` (all 0) |
| Gate quotes at least 3 words behind a locator | met | `gates_ok=12/12` |
| row-to-quote word overlap | met | `rows_without_quote_overlap=0` |
| SKILL: at least 4 distinct lines of at least 12 words | met | `skill_rows=6` |
| judge receipt | absent, not my seat | `judge=absent` |

## Bounds and hygiene

- Writes: this report, plus scratch under `/fast/scratch/hyaku/mori-r31/CriticC1Tip/` (`wd.sh`, `wd2.sh`, `lk`, `lk2`,
  `locks.c`, `flock.1.adoc`, the counter outputs, and the SOURCES copies at `a12c68ae` and at the tip). No lane, fleet
  or jj writes were made.
- Processes: everything I started had exited before I returned. The probe children were removed with `kill` on the
  child I recorded, and in the second probe with `pkill -f '^sleep 30$'`. I chose that exact pattern to match only the
  probe's own `sleep 30`, and `pgrep -fc` afterwards printed `0`. A PID-targeted kill would have been tighter, and I
  note that here.
- Installs: none.
