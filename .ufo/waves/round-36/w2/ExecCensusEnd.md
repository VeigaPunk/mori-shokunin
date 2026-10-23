# ExecCensusEnd — round-end source-census conformance gate (mori, round 36, wave 2)

Seat: `ExecCensusEnd` (executor). L1: MoriR36. Lane repo:
`/home/vgpnk/Projects/shokunin/mori-shokunin` (read-only for this seat; jj-colocated, git backend).
Fleet repo `/home/vgpnk/Projects/shokunin` read-only. No lane file was edited by this seat; the only
file written is this report. No `git add/commit/push/fetch/reset`, no mutating `jj` command, no
pacman, no installs (nothing to record).

## 1. What this item attacks

The round-end **source-census conformance gate** for lane `mori`, i.e.:

- the exit code of `scripts/sources-census.sh validate` for lane `mori` at the round-end tip
  (exit 0 required), and
- the **delta of W-lines** against the round-start receipt
  `.ufo/waves/round-36/evidence/census-start.txt`.

It does not re-judge C1/C2, does not score the counters, and does not touch the append-only gate's
own verdict beyond using it as a cross-check (below, §5).

## 2. The measured gate (full output + exit code)

Command (exactly as assigned):

```
$ cd /home/vgpnk/Projects/shokunin
$ bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori; echo "EXIT=$?"
```

Observed output (verbatim, 16 lines) and exit code:

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
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
EXIT=0
```

**Exit code 0 — required condition met. Lane verdict line is `mori ok`, not `mori E…`.**

No `E01–E12` line appears for lane `mori` at all (E-codes would set exit 1; `findings=1` → `exit 1`,
`scripts/sources-census.sh:800-805`).

## 3. Comparison against the round-start receipt — the new W-lines

Round-start receipt (`evidence/census-start.txt`, sha256
`aaae9654652a42fa0768ce90f985d1e1f331db60140a9fb47f49d9417ace3991`, 15 lines: 13 W04 + `ok` + `EXIT=0`):

```
$ grep -c W04 .ufo/waves/round-36/evidence/census-start.txt
13
$ diff <(sort evidence/census-start.txt) <(sort /fast/scratch/hyaku/mori-r36/ExecCensusEnd/census-end.txt)
1d0
< EXIT=0
15a15,16
> mori	W04	S218 duplicate url github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch across scopes
> mori	W04	S220 duplicate url raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c across scopes
DIFF_EXIT=1
```

**Exactly two new W-lines, both `W04` (informational), zero new E-lines:**

| new line | id | url | scope key collision with |
|---|---|---|---|
| W04 | S218 | `github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch` | S188 (`corpus/SOURCES.md:194`) |
| W04 | S220 | `raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c` | S190 (`corpus/SOURCES.md:196`) |

All 13 pre-existing W04 lines (S035, S037, S073–S076, S147–S150, S166, S168, S201) are retained
byte-for-byte; nothing regressed and nothing was dropped.

### 3.1 Root cause of the two new W04s (measured, not inferred)

`S218` (`corpus/SOURCES.md:224`) and `S220` (`corpus/SOURCES.md:226`) are the two round-36
superseding rows whose **scope cell was reworded** rather than copied verbatim from the row they
supersede; the other 13 round-36 supersede rows (`S206`–`S217`, `S219`) carry their predecessor's
scope string byte-identically:

```
$ python3 (rows parsed from corpus/SOURCES.md)
S041 -> S206: scope_equal=True   S189 -> S219: scope_equal=True
S044 -> S207: scope_equal=True   S188 -> S218: scope_equal=False   scope_len 183 -> 360
S051 -> S208: scope_equal=True   S190 -> S220: scope_equal=False   scope_len 187 -> 201
S062 -> S209: scope_equal=True   (S044,S051,S062,S064,S179,S180,S181,S183,S184,S185,S186,S189: True)
S064 -> S210: scope_equal=True
S179 -> S211: scope_equal=True
S180 -> S212: scope_equal=True
S181 -> S213: scope_equal=True
S183 -> S214: scope_equal=True
S184 -> S215: scope_equal=True
S185 -> S216: scope_equal=True
S186 -> S217: scope_equal=True
```

Causal proof on a **scratch copy** (the lane's real `corpus/SOURCES.md` was not touched): copying
S188's scope into S218 and S190's scope into S220 in a copy of the tip tree makes both W04 lines
disappear.

```
$ bash scripts/sources-census.sh validate <scratch-copy>/mori-shokunin --today 2026-10-23 | grep -cE "S218|S220"
0
```
(vs. 2 W04 lines for S218/S220 in the unmodified tip export). The mechanism is the census's own
`W04` rule: same normalized URL seen under a **different** scope key →
`scripts/sources-census.sh:643-645`; the `E04` duplicate-URL+scope rule is *not* triggered because
these rows carry `supersedes S###` in `teaches` (`:646-649`).

### 3.2 Is the new W04 a defect? (No — with the precedent and the rule cited)

- The census contract states W-codes never change status: "W04 same URL across scopes (warnings do
  not affect clean lanes)" (`scripts/sources-census.sh:33`) and exit semantics
  "0 clean or warnings · 1 E/overdue findings" (`:29-31`). Exit is 0 and the lane prints `ok`.
- **Lane precedent:** round 35's superseding row `S201` (over `S182`) produced exactly this shape —
  a new `W04` for a superseder that shares its predecessor's URL with a reworded scope — and the
  round-35 verifier recorded it as benign: "It prints 13 `W04` lines … The only new one is S201,
  which shares S182's URL by design as its superseder"
  (`corpus/lessons/round-35-verifier-spotcheck.md:143-145`). Round-35's own start→end receipt pair
  shows the same growth (12 → 13 W04, `.ufo/waves/round-35/evidence/census-start.txt` vs
  `census-end.txt`).
- **Rule compliance:** CORPUS §SOURCES.md rule 2 (`/home/vgpnk/Projects/shokunin/CORPUS.md:116-118`)
  restricts *in-place* edits to `status`/`recheck`/`used-by` and says "A correction is a new row
  whose `teaches` opens `supersedes S0NN —`". `S218` and `S220` are **new rows** carrying
  `supersedes S188 —` / `supersedes S190 —`; their scope text is new content, not an in-place
  rewrite. `git diff 6bd57097 bf0df77 -- corpus/SOURCES.md` shows **16 added rows and 0 modified or
  deleted rows** (`grep -cE '^-' ` → 1, and that single line is the `--- a/corpus/SOURCES.md`
  diff header). The scope reword is the correction payload, which is what a superseding row is for
  (S188's scope said flush requests are "triggered by requests that are usually zero-size writes"
  while its own `teaches` said "usually barriers, zero-size writes"; S218 corrects that wording
  and adds the field-17 millisecond claim).

## 4. Fidelity and determinism of the measurement

- **The round-start receipt is faithful to the round base.** Exporting the round base
  `6bd57097` (`git archive 6bd57097` into scratch) and running the same validator reproduces the
  receipt byte-for-byte modulo the lane label and the path prefix:
  ```
  $ diff <(sed -e 's/^mori-shokunin\t/mori\t/' -e 's#<scratch>/base-tree/mori-shokunin#/home/vgpnk/Projects/shokunin/mori-shokunin#' census-base-faithful.txt) \
         <(grep -v '^EXIT=' .ufo/waves/round-36/evidence/census-start.txt)
  RECEIPT_VS_REPRODUCED_BASE_DIFF_EXIT=0
  ```
  So the 13 W04 lines in the start receipt are the base's, and the two new ones are genuinely
  introduced by the round-36 landing (S205–S220).
- **Tip tree vs. live tree agree.** `git diff 6bd57097 bf0df77 -- corpus/SOURCES.md` is 16
  insertions; the working tree's `corpus/SOURCES.md` is byte-identical to the tip blob
  (sha256 `e40f9cb2eed2bac873f24bf8bf6e45d9c12db488375afc09f29cbd25a2f9d7b1` for both
  `corpus/SOURCES.md` and `git show bf0df77:corpus/SOURCES.md`). The measured output therefore
  reflects the landed tip, not a dirty tree.
- **Deterministic.** Three consecutive runs are byte-identical
  (`md5sum` → `48bb263d69e788d03a11fc9e3ad5b21e` ×3) and the output is invariant under
  `TZ=UTC|America/Sao_Paulo|Asia/Tokyo` and under `--today 2026-10-24` (same md5 in all four
  invocations).
- **The gate tool was not tampered with.** `git show HEAD:scripts/sources-census.sh` and the
  worktree copy have the same sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`,
  and `git diff --quiet -- scripts/sources-census.sh` is clean. The script's own selftest passes
  (`bash scripts/sources-census.sh selftest` → `selftest ok`, exit 0).
- **Fleet-wide context:** `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin`
  (all lanes) → exit 0, 318 lines, **0** `E`-coded lines, every lane `ok` (mori among them).

## 5. Cross-check of the routed round-35 repair claim (18 ids discharged)

The dispatched claim is "SOURCES supersede rows S205–S220 (18 in-place-edited ids discharged)". The
frozen append-only gate at the tip confirms it (same tool, same rev):

```
$ python3 tools/mori-sources-appendonly.py bf0df77fee4b6ef54a90aea09335c7617f125151 --round-base 6bd57097; echo "EXIT=$?"
changed S041 superseded_by=S206
changed S044 superseded_by=S207
changed S051 superseded_by=S208
changed S062 superseded_by=S209
changed S064 superseded_by=S210
changed S069 superseded_by=S073
changed S179 superseded_by=S211
changed S180 superseded_by=S212
changed S181 superseded_by=S213
changed S182 superseded_by=S201
changed S183 superseded_by=S214
changed S184 superseded_by=S215
changed S185 superseded_by=S216
changed S186 superseded_by=S217
changed S188 superseded_by=S218
changed S189 superseded_by=S219
changed S190 superseded_by=S220
changed S193 superseded_by=S202
appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] round_changed=[]
EXIT=0
```

`superseded` now lists **all 18** ids (S069/S182/S193 were already superseded at round 35; the other
15 are discharged by `S206`–`S220`), `round_changed=[]`, exit 0. `tools/mori-sources-appendonly.py
--selftest` → `MORI_SOURCES_APPENDONLY_SELFTEST pass=8 fail=0` (exit 0). The `index clean` gate is
also green at the tip: `bash tools/mori-index-clean.sh /home/vgpnk/Projects/shokunin/mori-shokunin`
→ `MORI_INDEX_CLEAN staged=0 intent_to_add=0`, exit 0.

Side observation (not a census finding): wave-1's `SrcCorpus.md` reported
`E11 S205 missing used-by tools/mori-source-drift.py` against a *draft* registry. At the tip the
tool exists and is committed (`git ls-tree bf0df77 tools/mori-source-drift.py` →
`100755 blob 103965ac…`), so the E11 does not reproduce in the measured run above.

## 6. Findings, risks, blockers

**Findings**

1. Round-end census gate for `mori`: **exit 0**, lane `ok`, no E-coded line. Required condition met.
2. Delta vs. round-start receipt: **two new W-lines, both `W04`** — S218 and S220 — and **no new
   E-line**. Cause: the two round-36 supersede rows that reworded the scope cell; proven by the
   scratch-copy control in §3.1. Informational by the census contract; same shape as round 35's
   accepted `S201` W04.
3. Round-start receipt is faithful (byte-reproducible from base `6bd57097`); measurement is
   deterministic, TZ/date-invariant, and made against the landed tip bytes.
4. Routed repair "18 in-place-edited ids discharged" confirmed by the frozen gate: 18/18 superseded,
   `round_changed=[]`, exit 0.

**Risks (for the L1 to weigh, not defects I can remediate from this seat)**

- **R1 — missing round-end census receipt.** Rounds 31, 32, 33, 35 all carry
  `.ufo/waves/round-<N>/evidence/census-end.txt`; round 36 has `census-start.txt` but **no**
  `census-end.txt` at the tip (`ls .ufo/waves/round-36/evidence/census-end.txt` → "No such file").
  This seat is bounded to one file (this report) and to a read-only lane, so it did not write the
  receipt. If the round's close-out requires the receipt, the L1 should land exactly the bytes
  measured in §2. A ready-to-paste form (matching the round-35 receipt shape:
  `# census end <UTC ts> (SOURCES.md bytes as committed at bf0df77; unchanged since)` + the 16
  lines of §2 + `EXIT=0`) is at
  `/fast/scratch/hyaku/mori-r36/ExecCensusEnd/census-end-receipt-form.txt`
  (its census body sha256 `6b422b9740e7b054732e42f321facae03c97072d71b89cbff6a5498c68ba593d`,
  identical to the raw output; the header line adds the tip + `corpus/SOURCES.md` sha256
  `e40f9cb2…`).
- **R2 — receipt provenance header absent in the start receipt.** `evidence/census-start.txt`
  begins directly with the first W04 line, whereas rounds 34/35 start with a
  `# census start <ts> lane tip <rev>` / `measured <ts> at lane tip <rev>` header. This does not
  affect the gate's meaning (I re-derived the base state independently and it matches byte-for-byte),
  but the round-36 start receipt does not name the tip it was measured at, unlike its predecessors.
- **R3 — two inconsistent supersede shapes inside one landing.** 13 of 15 round-36 supersede rows
  copy the predecessor's scope verbatim; `S218`/`S220` reword it. Both are rule-2-legal, but the
  mixture is the sole source of the two new W04 lines, so any future claim of "the census output is
  unchanged by the round" would be false for W04 purposes (the count moved 13 → 15).

**Blockers:** none. No remediation was attempted (mori province: detection and report only).

## 7. Artefacts left in scratch (not in the lane)

`/fast/scratch/hyaku/mori-r36/ExecCensusEnd/` — `census-end.txt`, `census-end-2.txt`,
`census-end-final.txt` (all md5 `48bb263d69e788d03a11fc9e3ad5b21e`), `census-end-receipt-form.txt`,
`census-base-faithful.txt` (base `6bd57097` export run), `census-base-export.txt`,
`census-base-reproduced.txt`, `census-tip-export.txt`, `fleet-validate.txt` (all-lane run),
`SOURCES-base.md`. Large temporary trees (`base-tree`, `tip-tree`, `mut`, `lanecopy`) were deleted
after use. Lane repo: only this report was added; `corpus/SOURCES.md` untouched.

VERDICT: PASS

Report: .ufo/waves/round-36/w2/ExecCensusEnd.md
