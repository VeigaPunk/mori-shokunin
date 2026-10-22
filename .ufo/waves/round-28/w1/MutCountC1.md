# MutCountC1 — mutation probe of the round-28 C1 counter (landed 079a47c6)

Seat: MoriR28.MutCountC1 (mutation-tester, leaf — no subagents dispatched).
Target: `.ufo/waves/round-28/count-c1.sh`, blob at landed tip `079a47c61691f2b891d35458057b294ca5a99e77`
(blob sha256 `825dbcc3180aea58547a304bce6249fbfbb0c704f78ec6c75eb698d2f143077a`).

## Method

Scratch: `/fast/scratch/hyaku/mori-r28/MutCountC1/`.

1. `git clone --no-hardlinks` of the lane into `scratch/lane` (sandbox; the lane itself was never written to).
2. Byte copy of the counter: `scratch/count-c1.sh` — sha256 identical to the landed blob before the edit.
   Only `LANE=` differs (the one-line edit the task allows):

```
-LANE=/home/vgpnk/Projects/shokunin/mori-shokunin
+LANE=/fast/scratch/hyaku/mori-r28/MutCountC1/lane
```

3. The counter fetches the frozen check script by blob id (`count-c1.sh:20`) but that script has
   `LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"` hardcoded (`check-row-identity.py:19`).
   Without a redirect the two halves measure different repositories (see **S1** below). I installed a
   `git replace` ref inside the sandbox mapping `df886be1` to a same-parent commit whose
   `check-row-identity.py` carries the sandbox `LANE`; the frozen blob's bytes are otherwise byte-identical
   (diff shown below). The replace ref lives only in the sandbox clone.
4. Each mutant is a commit whose parent is `079a47c6` and whose only change is `corpus/SOURCES.md`
   (written via a temp index + `commit-tree`, so no mutant ever sees another mutant's history).
5. The same bounded detector (the counter) was run on pristine, mutated and restored bytes.
   Pristine baseline = the landed tip: `row_identity=rows=144 changed=3 removed=0 bad=0`,
   `superseding=0/8 ids=none`, `C1=unmet`, exit 1. The baseline fails, so it is a *before* measurement,
   not a false kill.
6. The met case is a separate fixture (the eight owed rows restored byte-for-byte to their
   first-published lines + eight new superseding rows S145..S152).

The restore baseline was taken with `scratch/first-published.py`, which mirrors `check-row-identity.py`'s
own parsing (same `ROW` and `SEP` regexes, same `--full-history --topo-order --reverse` walk) so the
restored bytes are byte-equal to what the frozen check compares against.

## Results — each scenario, output, exit

Full log: `scratch/probe-results.txt`. Summary (verdict = did the counter read what it should?):

| # | scenario | expect | row_identity | superseding | C1 | exit | verdict |
|---|---|---|---|---|---|---|---|
| m00 | **met case**: all eight restored + eight superseding rows | met | rows=152 changed=0 removed=0 bad=0 | 8/8 | met | 0 | **as expected** |
| m01 | superseding row status `queued` | unmet | rows=152 changed=0 removed=0 bad=0 | 7/8 | unmet | 1 | as expected |
| m02 | superseding row status `rejected` | unmet | rows=152 changed=0 removed=0 bad=0 | 7/8 | unmet | 1 | as expected |
| m03 | superseding row id below S144 (`S0100`) | unmet | rows=152 changed=0 removed=0 bad=0 | 7/8 | unmet | 1 | as expected |
| m03b | superseding row id **equals** S144 (collides) | unmet | rows=151 changed=0 removed=0 **bad=1** | 7/8 | unmet | 1 | as expected |
| m04 | hyphen `-` instead of em dash | unmet | rows=152 changed=0 removed=0 bad=0 | 7/8 | unmet | 1 | as expected |
| m04b | en dash `–` instead of em dash | unmet | rows=152 changed=0 removed=0 bad=0 | 7/8 | unmet | 1 | as expected |
| m05a | no space **before** the em dash | unmet | rows=152 changed=0 removed=0 bad=0 | 7/8 | unmet | 1 | as expected |
| m05b | no space **after** the em dash | unmet | rows=152 changed=0 removed=0 bad=0 | 7/8 | unmet | 1 | as expected |
| m06 | superseding row names an id **not owed** (S095) | unmet | rows=152 changed=0 removed=0 bad=0 | 7/8 | unmet | 1 | as expected |
| m07 | **seven of eight** superseding rows (S152 absent) | unmet | rows=151 changed=0 removed=0 bad=0 | 7/8 | unmet | 1 | as expected |
| m08 | restored row differs **only by whitespace** (one byte, inside the scope cell) | unmet | rows=152 **changed=0** removed=0 bad=0 | 8/8 | **met** | **0** | **SURVIVED — fail-open** |
| m08b | restored row differs by 3-space **leading indent** | unmet | rows=152 changed=0 removed=0 bad=0 | 8/8 | **met** | **0** | **SURVIVED — fail-open** |
| m08c | restored row differs by **trailing spaces** | unmet | rows=152 changed=0 removed=0 bad=0 | 8/8 | **met** | **0** | **SURVIVED — fail-open** |
| m09 | restored row differs by **internal** whitespace (`not  later`) | unmet | rows=152 **changed=1** removed=0 bad=0 | 8/8 | unmet | 1 | as expected |
| m10 | restored row differs by **one whole cell** (kind `code`→`docs`) | unmet | rows=152 changed=1 removed=0 bad=0 | 8/8 | unmet | 1 | as expected |
| m11 | a **row deleted** (S140) | unmet | rows=151 changed=0 **removed=1** bad=0 | 8/8 | unmet | 1 | as expected |
| m12 | a **malformed row line** (S127 one cell short) | unmet | rows=151 changed=0 removed=1 **bad=1** | 8/8 | unmet | 1 | as expected |
| m13 | a **duplicate id** (S145 twice) | unmet | rows=152 changed=0 removed=0 **bad=1** | 8/8 | unmet | 1 | as expected |
| m14 | prefix `Supersedes` (capital S) | unmet | rows=152 changed=0 removed=0 bad=0 | 7/8 | unmet | 1 | as expected |
| zz | revision that does not resolve (`0000…`, `deadbeef…`) | exit 2 | — | — | — | 2 | `bad_rev`, exit 2 |
| zz | usage error (no argument) | exit 2 | — | — | — | 2 | `usage: count-c1.sh <rev>`, exit 2 |
| zz | rev resolves but `corpus/SOURCES.md` absent (root commit) | exit 2 | — | — | — | 2 | `sources_absent`, exit 2 |
| zz | `df886be1` absent from the lane | exit 2 | — | — | — | 2 | `check_absent`, exit 2 |
| zz | `corpus/SOURCES.md` not valid UTF-8 | exit 2 | — | — | — | 2 | `row_identity=error`, exit 2 |

Every scenario named in the task reads `C1=unmet` with exit 1 except the whitespace variants (m08, m08b,
m08c), which read `C1=met` with exit 0, and the met case, which correctly reads `C1=met` exit 0.

## Fail-open paths

Each is a real mutant that reads `C1=met` when the claim is not satisfied. "Survives A1" = the same
mutant against the **working-tree** counter (amendment A1, sha256 `0d7a1be0…`), which is not the landed
target but is the in-flight successor; I report it so the L1 knows which gaps A1 already closes.

| id | fail-open | landed | survives A1? | smallest fix |
|---|---|---|---|---|
| **F1** | **The two halves of the counter can measure different repositories.** `count-c1.sh:9` sets `LANE`, but the frozen check script it runs has its own hardcoded `LANE` (`check-row-identity.py:19`). Editing `LANE=` — the exact edit this task prescribes — relocates only the *superseding* half; the *row-identity* half still walks the real lane. | **yes** | yes | Rewrite the fetched blob's `LANE` constant to `$LANE` right after `count-c1.sh:20`, e.g. `sed -i "s\|^LANE = .*\|LANE = \"$LANE\"\|" "$T/check.py"`. **Proven**: with the redirect the sandbox run prints `row_identity=rows=152 changed=0 removed=0 bad=0 … C1=met` exit 0; without it the same run prints `row_identity=error` exit 2. |
| **F2** | **A restored row may differ from its first-published bytes by whitespace and still count as restored.** The frozen check compares `.strip()`-ed cells (`check-row-identity.py:37`), so trailing space, leading indent and cell-edge whitespace are invisible. The contract requires "restored byte-equal to their first-published cells" (`.ufo/waves/round-28/contract.md:19`), so a whitespace-different row is not byte-equal. m08/m08b/m08c all survive. | **yes** | yes | Compare the **raw** cell bytes, not the stripped ones, in the restore comparison — i.e. keep both `cells` (stripped, for parsing) and a `raw` split, and diff `raw` for the eight non-mutable columns. Smallest change is inside `check-row-identity.py`'s `rows()`/`changed` loop; the counter needs no change. |
| **F3** | **The superseding rows may sit outside the registry table.** The counter scans every line of `corpus/SOURCES.md` for the row shape (`count-c1.sh:32`); it never checks the row is in the `## Registry` table. Eight rows under a `## Drafts` heading (f01) or inside a ` ``` ` code fence (f14) satisfy the claim. | **yes** | yes | Restrict the scan to the registry table: find the `## Registry` heading and stop at the next `## ` heading, then require the row's index to fall inside that range. |
| **F4** | **The eight new ids are not pinned to the contract's map.** The counter only requires "some row with id > S144 whose `teaches` opens `supersedes S0NN — ` for an owed id" (`count-c1.sh:38-43`). The contract fixes `S145:S096 S146:S097 S147:S101 S148:S127 S149:S128 S150:S129 S151:S131 S152:S140` (`.ufo/waves/round-28/wave1-spec.json:5`; the same map in the A1 counter's `MAP=` at `count-c1.sh:17`). A map swap (f10: S145→S097, S146→S096) and non-map ids (f06: S153…S160) both read met. | **yes** | **no** — A1 pins `MAP=` and rejects a swap (`fail S145 prefix`) and absent ids (`fail S145 row_absent`) | Already fixed by A1. If the landed counter is to be hardened in place: replace `OWED`+`MAX_OLD` with the explicit `MAP` and require the exact `new→old` pair, as A1 does. |
| **F5** | **`status` accepts `verified`, which is not a legal CORPUS status.** CORPUS.md:103-104 lists exactly `queued`, `mined`, `rejected`. The counter counts `("mined", "verified")` (`count-c1.sh:42`), so a row with the non-existent status `verified` satisfies the claim (f03). | **yes** | **no** — A1 rejects it (`fail S145 status=verified`) | Already fixed by A1. In place: drop `"verified"` from the tuple at `count-c1.sh:42`. |
| **F6** | **A superseding row may carry empty `source`/`anchor`/`opened` cells, or a `source` unrelated to the row it supersedes.** The counter inspects only `id`, `teaches` and `status` (`count-c1.sh:37`). f04 (all three empty), f08 (`source` = `https://example.invalid/…`) and f13 (source/anchor/opened empty, valid `used-by`) all read met. The contract requires the row be "re-opened against the upstream bytes in round 28" — the counter never checks it points at the same source. | **yes** | f04 **no** (A1 rejects `used_by_empty`); f08 and f13 **yes** | A1's `used_by_empty` rule covers f04 only. For f08/f13 the smallest fix is to require the superseding row's `source` cell to equal the superseded row's `source` cell, and to require non-empty `source`, `anchor` and `opened`. |
| **F7** | **The superseding row's `teaches` body may be a verbatim copy of the superseded row's `teaches`.** The counter only checks the `supersedes S0NN — ` prefix (`count-c1.sh:40`); f05 reads met with a teaches body identical to the old row's. A row that teaches nothing new is not a supersession. | **yes** | **no** — A1 rejects it (`fail S145 teaches_unchanged`) | Already fixed by A1. |
| **F8** | **The claim's `## Gate` requirement is never checked.** The contract requires the lesson `## Gate` to record URL, access time and a ≤25-word quote for every new row. The landed counter never opens `corpus/lessons/round-28.md` at all — the file does not even exist at `079a47c6`, and a run with no lesson file still reads met. | **yes** | **no** — A1 requires a `## Gate` line with an `https://` URL, a 64-hex sha256 and a quoted span | Already fixed by A1. |
| **F9** | **Live readers are never checked.** The contract says the live readers must move to the new rows. The landed counter never greps the readers, so 28 stale citations of the superseded ids remain and the counter still reads met. | **yes** | **no** — A1 adds `readers_left` and requires 0 | Already fixed by A1. |
| **F10** | **A restored row may differ in a mutable cell.** The frozen check exempts `status`, `recheck`, `used-by` from the comparison (`check-row-identity.py:22`, applied at `:74`), so a "restored" S096 with a rewritten `used-by` reads changed=0 (f02). | **yes** | yes | This is CORPUS rule 2 (append-only) and is *correct* for a general registry check, but it conflicts with the contract's "restored byte-equal to their first-published cells". Smallest fix: the counter compares the three restored ids' full raw lines against their first-published raw lines, separately from the general check. |

F1 is the one I would fix first: it is a defect in the counter's own testability, and it is the reason a
reviewer who follows this task's own instructions (edit `LANE=` in a byte copy) silently measures half the
claim against the real lane.

## Restoration evidence

- The lane was never written to. `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --cached --stat`
  is empty (no staged changes); `git status --porcelain` shows only the working-tree changes made by
  other seats (`contract.md`, `PROVINCE.md`, `SKILL.md`, `corpus/*`) plus untracked wave-1 files.
- `git -C lane rev-parse HEAD` in the sandbox = `079a47c6` for every mutant commit's parent; the lane's
  own HEAD moved to `1c4c186` during the probe because other seats landed work — not my doing
  (`git log --oneline -1` at the sandbox clone still shows `079a47c` as its tip; my mutant commits are
  unreachable, written with `commit-tree` and never referenced).
- Byte hashes of the two files I read but did not write:
  - `count-c1.sh` at `079a47c6` = `825dbcc3180aea58547a304bce6249fbfbb0c704f78ec6c75eb698d2f143077a`
    (unchanged; the working-tree file is a **different, later** A1 amendment, sha256 `0d7a1be0…`, written
    by another seat — I did not touch it).
  - `corpus/SOURCES.md` working tree = `cc1a1d6b…`, `079a47c6` blob = `05953a16…` — differs because
    sibling seats are landing the real superseding rows; not my edit.
- All my artefacts live under `/fast/scratch/hyaku/mori-r28/MutCountC1/`. The `git replace` ref exists
  only in `scratch/lane/.git`, never in the real lane.
- The sandbox `check-row-identity.py` copy differs from the frozen blob by exactly one line
  (`LANE = "…"` → the sandbox path); no other byte differs.

## Tooling

No packages installed, no system changes. Versions used: bash 5.3.20, git 2.56.0, Python 3.14.8
(all pre-existing; `python3 -I -B` throughout, as the counter itself requires).

## Scope note

The counter has two versions in play: the landed `079a47c6` blob (my target, sha256 `825dbcc3…`) and a
working-tree A1 amendment (sha256 `0d7a1be0…`) that is not yet committed. All primary results above are
against the landed blob. A1 closes F4, F5, F7, F8, F9 and f04; it does **not** close F1, F2, F3, F6
(for f08/f13) or F10 — so the same fix list still applies to the successor, minus the parts A1 already
handles.
