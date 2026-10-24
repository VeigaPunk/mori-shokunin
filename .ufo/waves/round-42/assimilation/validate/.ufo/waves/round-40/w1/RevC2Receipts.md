# RevC2Receipts — C2 (P-C11) receipt audit — mori round 40, wave 1

Seat: reviewer (read-only). Lane root: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Scope: all ten `.ufo/waves/round-40/evidence/c11-*.txt`; command / rev / exit
discipline; the red/after pair for each P-C11 fixture DAG; reproduction of every
receipt against the frozen instrument bytes. No production file was written; the
only outputs are this report and `/tmp` reproductions.

## 1. Identity of the instruments before auditing

| artifact | check | result |
|---|---|---|
| `tools/mori-sources-appendonly.py` (v3) | `sha256sum` vs `evidence/freeze-r40.txt` | `bde5a9a34c7e…06777ec` = pinned |
| v3 gate | `git hash-object` vs `git rev-parse 265a955cc:tools/…` | both `9f29290966ad…31583f` |
| `fixtures/extracted/gate-v2-bb1f2457.py` (v2) | `git hash-object` vs `git rev-parse bb1f2457:tools/…` | both `d2c961609004…a9ae13da` |
| v2 gate | `sha256sum` vs freeze | `62cd4132dbe1…cfc01e7` = pinned |
| `contract.md`, `fixtures/run-c11-dags.py` | `sha256sum` vs freeze | `6514914…` / `0cd7f1d…` = pinned |
| all 10 `c11-*.txt` | `git hash-object` vs `git rev-parse HEAD:<path>` | identical (committed in `8d3badd`, 02:56:11 −03) |

## 2. Commands run (exact) and outputs

All from the lane root. `EXIT=` is the shell exit; for the runner, the `EXIT=`
line inside its receipt is the gate child's exit, and the runner itself always
returns 0 (it does not propagate the child's status).

1. `python3 tools/mori-sources-appendonly.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --repo .` → `EXIT=1`

   ```text
   supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S067,S069,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193,S226] stale_supersede=[]
   ```

   **35 ids** (34 commas), not 19 (contract) and not 34 (wave summary). Content
   equals `c11-after-lane.txt` modulo its hand-written `command:` line.
2. `python3 tools/mori-sources-appendonly.py e37dcc6 --repo .` → `EXIT=1`;
   `superseded_as_of` = 33 ids, `stale_supersede=[S069]`. Equals
   `c11-after-e37dcc6.txt`.
3. `python3 tools/mori-sources-appendonly.py --selftest` →
   `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0`, `EXIT=0`. Equals
   `c11-after-selftest.txt`.
4. `python3 .ufo/waves/round-40/fixtures/extracted/gate-v2-bb1f2457.py bb1f2457 --repo .` → `EXIT=1`;
   18 ids, `stale_supersede=[]`. Equals `c11-before-lane.txt`.
5. `python3 .ufo/waves/round-40/fixtures/extracted/gate-v2-bb1f2457.py 265a955cc… --repo .` → `EXIT=1`;
   18 ids. Used for the v2→v3 set difference below.
6. `python3 .ufo/waves/round-40/fixtures/run-c11-dags.py tools/mori-sources-appendonly.py /home/vgpnk/Projects/shokunin/mori-shokunin /tmp/rev-c11-after-fixtures.txt dag-n dag-p dag-r`
   → all three blocks equal the three committed `c11-after-fixture-*.txt`
   receipts (only the out-path argument and a trailing blank line differ).
7. `python3 .ufo/waves/round-40/fixtures/run-c11-dags.py .ufo/waves/round-40/fixtures/extracted/gate-v2-bb1f2457.py /home/vgpnk/Projects/shokunin/mori-shokunin /tmp/rev-c11-red-fixtures.txt dag-n dag-p dag-r`
   → all three blocks equal the three committed `c11-red-*.txt` receipts.
8. Independent eligible-set count from the tip blob (not the gate):
   `git show 265a955cc:corpus/SOURCES.md` parsed with the gate's own
   `parse_registry` → 229 rows, **35 distinct `supersedes S###` targets present
   at the tip** (39 lines carry the string; `S069` is superseded twice, by `S073`
   and by `S226`). At `e37dcc6`: 225 rows, 34 targets.
9. Independent `S069` ancestry: last immutable-cell edit `62db24c01d5b`
   (round-33); `S226`'s superseding row first appears at `daa1d4d2501e`
   (round-38); `git merge-base --is-ancestor 62db24c… daa1d4d…` → 0 (ancestor)
   ⇒ `S069` is genuinely as-of at the tip. At `e37dcc6` the latest superseder is
   `S073` (`71abd41…`), which landed before `62db24c`, hence stale there.
10. Isolated dag-r control (fixture rebuilt in `/tmp` from the frozen builders,
    base = `r1` instead of the receipt's `b0`), both gates:
    - v2: `round_changed=[S008]`, `as_of=[]`, `stale=[]`, `EXIT=1`
    - v3: `round_changed=[]`, `as_of=[S008]`, `stale=[]`, `EXIT=0`
11. Mutant check (copy of v3 in `/tmp` with v2's linear re-add branch restored),
    dag-r base `b0`: `as_of=[]`, `stale=[S008]` — i.e. the committed *after*
    receipt would fail if the re-add branch were still present.
12. `python3 tools/mori-sources-appendonly.py bb1f2457 --repo .` (extra check;
    v3 at the entering tip) → 35 as-of ids, `stale=[]`.

## 3. Receipt inventory: command / rev / exit

| receipt | command recorded | rev named | EXIT |
|---|---|---|---|
| `c11-before-lane.txt` | `…gate-v2-bb1f2457.py bb1f2457 --repo .` | yes (`bb1f2457`, arg + filename) | 1 |
| `c11-red-neveredited.txt` | runner + `…gate-v2-bb1f2457.py` | v2 rev encoded in filename; fixture base `b0=07be6c7f1765` (12 chars); fixture HEAD sha **not** recorded | 0 |
| `c11-red-firstparent.txt` | same, `dag-p` | same | 1 |
| `c11-red-readd.txt` | same, `dag-r` | same | 1 |
| `c11-after-lane.txt` | `… 265a955cc… --repo .` | yes | 1 |
| `c11-after-e37dcc6.txt` | `… e37dcc6 --repo .` | yes | 1 |
| `c11-after-selftest.txt` | `… --selftest` | **no revision** | 0 |
| `c11-after-fixture-n.txt` | runner + `tools/mori-sources-appendonly.py` | **no gate revision**; fixture base truncated; HEAD sha not recorded | 0 |
| `c11-after-fixture-p.txt` | same, `dag-p` | same | 1 |
| `c11-after-fixture-r.txt` | same, `dag-r` | same | 1 |

The full frozen predicate line is captured verbatim in each v3 receipt
(`len == 1036`, `== PREDICATE`) and each v2 receipt (`len == 832`, `== PREDICATE`).
All receipts carry a `command:` line and an `EXIT=` line.

## 4. Red/after pair analysis (per fixture DAG)

The pairs are compared line-by-line after dropping the versioned predicate line.

**dag-n — contradicts as declared.** red: `superseded=[]`, timing `[] / []`;
after: `superseded=[S001]`, `as_of=[S001]`, `stale=[]`. The never-edited row is
omitted by v2 and as-of in v3. (The summary `superseded` list also changes; that
is undeclared but consistent with one shared eligible set.)

**dag-p — contradicts only on the timing line, not as declared.** The two
receipts are identical except:

```diff
-supersede_timing superseded_as_of=[] stale_supersede=[S001]
+supersede_timing superseded_as_of=[S001] stale_supersede=[]
```

`changed S001 superseded_by=S002` and `round_changed=[S001]` are present and
identical in **both** receipts. The contract's before cell says v2 "fabricates a
`changed` line plus a stale verdict" (contract.md:130-131); the fabricated merge
edit is real inside v2 (`changed_at[m]`) and its consequence is receipted (the
stale verdict), but the fabricated `changed` **line** is not what the pair shows:
v3 prints the same line, legitimately, because `ids` compares tip cells against
first-sighting cells (tip `anchor a v3` vs first `anchor a`).

**dag-r — does not contradict as declared.** red: `superseded=[]`,
`round_changed=[S008]`, timing `[] / []`; after: `superseded=[S008]`,
`round_changed=[S008]`, `as_of=[S008]`, `stale=[]`. The contract's before cell
says v2 "prints a `changed` event for the linear delete-then-re-add"
(contract.md:132-133); the after receipt prints the **same**
`round_changed=[S008]`, and neither receipt prints a `changed S008` line. With
the receipt's base `b0`, the delete at `s1` and the re-add at `r2` are both inside
`b0..HEAD`, so `round_changed` cannot attribute the event to the re-add; the only
red/after difference is the eligible set (`superseded=[]` → `[S008]`) and the
timing line. The declared changed-event contradiction is therefore not exhibited.

The re-add corner **is** real and the after receipt **does** discriminate it
(check 11: restoring the branch flips the after verdict to `stale=[S008]`), and
the isolating control is available but unrun in the evidence: with base `r1`,
v2 prints `round_changed=[S008]` / `EXIT=1` while v3 prints `round_changed=[]` /
`EXIT=0` (check 10). The committed red receipt thus cannot serve as a genuine
before-control for the re-add corner — the same failure mode (masked
before-control) that r39 lesson finding 11 routed against C1.

## 5. Findings, by severity

### F1 (high) — the declared lane line is 19 ids; the receipt prints 35

- `contract.md:119` (frozen P-C11) says "S226 joins superseded_as_of (19 ids) at
  the landed tip"; `contract.md:137` declares the after line as
  `superseded_as_of=[19 ids incl. S226]`; the gate's own `PREDICATE`
  (`tools/mori-sources-appendonly.py:87-88`) carries the same "(19 ids)".
- `evidence/c11-after-lane.txt` and my reproduction print **35** ids
  (`S067,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140,S226`
  join the 18 edit-bounded ids; set difference vs v2 at the tip: added = those
  17, removed = none).
- The predicate is therefore self-contradictory: its operative clause ("every
  superseded id present at R") yields 35 — confirmed independently from the tip
  blob (35 superseder targets, check 8) — while its parenthetical says 19. The
  wave summary's "34 as-of ids" (ticket / `w1-spec.json` items 5, 20, 52, 53) is
  also off by one: `S069` is as-of at the tip (check 9); 34 is the `e37dcc6`
  eligible count (33 as-of + `S069` stale).
- The gate's behaviour is correct per the operative clause; the frozen claim text
  is not. A grader applying `contract.md:137` literally finds the receipt
  contradicts the claim. This needs an erratum / new counter version for the
  predicate parenthetical and the contract After line; the number cannot be
  silently restated because P-C11 is frozen verbatim.

### F2 (medium) — dag-r red/after pair does not show the declared contradiction; before-control masked

- `c11-red-readd.txt` vs `c11-after-fixture-r.txt`: `round_changed=[S008]` in
  both; no `changed S008` line in either; only `superseded=[]`→`[S008]` and the
  timing line differ. The contract's before claim ("prints a `changed` event",
  `contract.md:132-133`) is not contradicted by the pair.
- The re-add edit exists in v2 (its linear re-add branch) but is invisible at the
  receipt's base `b0` because the delete event also contributes `S008` to
  `round_changed`; the before-control the claim needs is the base-`r1` run
  (check 10), which is not in the evidence.
- Suggested fix: add the base-`r1` dag-r receipt (v2 `[S008]` / v3 `[]`), and
  state the before as "attributes the re-add as the last edit" rather than
  "prints a changed event". The after receipt remains a valid discriminator
  (check 11).

### F3 (medium-low) — dag-p before claim overstates the observable

- Contract (`contract.md:132-134`) says v2 "fabricates a `changed` line plus a
  stale verdict". The pair shows the stale verdict flip only; the `changed S001`
  line is identical in both receipts and is legitimate v3 output (`ids` vs
  first-sighting). The fabricated *event* is real (and is what causes the stale
  verdict), but the wording points at a line the pair does not distinguish.
- Suggested fix: correct the before cell to "attributes the merge as the last
  edit → stale verdict", citing the timing line.

### F4 (low) — after receipts do not name the measured revision

- `contract.md:157-164` requires "Receipts name the measured revision (r39 lesson
  finding 9 discipline)". The three `c11-after-fixture-*.txt` receipts and
  `c11-after-selftest.txt` name no gate revision (only the worktree path); the
  fixture HEAD sha is not recorded, only the 12-char `--round-base` value. The
  red fixture receipts name v2 only via the extracted filename
  (`gate-v2-bb1f2457.py`).
- Identity is currently recoverable (freeze sha256 == worktree == tip blob,
  §1) but not from the receipt. Low risk while the freeze holds; add the gate
  sha/rev to the runner's `command:` line or the receipt header.

### F5 (info) — one after receipt's mtime postdates the evidence commit

- `c11-after-fixture-p.txt` mtime `03:00:22`, the other after receipts
  `02:49:31–02:49:55`, the evidence commit `8d3badd` `02:56:11`, the tip commit
  `265a955cc` `02:47:29`. Its content equals the committed blob and my
  reproduction, so no byte-level defect; the timeline suggests a post-commit
  re-write (identical content) of that one receipt. Noted for provenance only.

## 6. Residual risk and verification gaps

- **Shared fixture library.** `run-c11-dags.py` builds both the red and the after
  DAGs with the *landed v3 gate's* `_selftest_dag_cases` / `_make_dag_repo`
  (documented in its docstring). A bug in those builders would affect both arms
  of every pair; the base shas reproduce deterministically (my run produced
  `b0=07be6c7f1765` and the same verdicts), so the construction is stable, but
  it is not independent of the instrument under test.
- **History-wide `sup_map`.** `analyze` computes `superseded` as tip ids present
  in the history-wide `sup_map`, not as "a superseding row present at R". At the
  tip and at `e37dcc6` every superseding row is present, so the receipts do not
  exercise the case where a superseder row is deleted before R; P-C11's words
  ("present at R") and the code would then disagree. No receipt covers it.
- **`round_changed` conflates changed and deleted events** (module docstring
  lines 23-25), so "no changed event" is not directly observable at base `b0`;
  only the base-`r1` control isolates it (F2).
- **Not audited here:** the C1 / `c10-*` receipts and the conform checker (other
  seats); the C1 instruments were not run. I did not mutation-test the gate
  beyond the re-add-branch check in §2.11 and the natural red controls; the
  gate's selftest `pass=15 fail=0` is the instrument's own claim, reproduced but
  not independently re-derived arm by arm.

## 7. Verdict

The v3 gate's measured behaviour at the landed tip and at `e37dcc6` matches
P-C11's operative clause (35 as-of at the tip, none stale; `S069` stale at
`e37dcc6`), the selftest reproduces `pass=15 fail=0`, and the three after fixture
receipts reproduce byte-for-byte against the frozen gate. The C2 **claim text**
does not survive its own receipts: the declared lane line (19 ids) is false
against the measured 35, and two of the three declared red/after contradictions
(dag-p's "changed line", dag-r's "changed event") are not exhibited by the pair —
the dag-r before-control is masked and the isolated control is unrun. C2 should
not be admitted on the current declaration until the predicate parenthetical /
contract After line are corrected by a new counter version or erratum and the
dag-r base-`r1` control is receipted.
