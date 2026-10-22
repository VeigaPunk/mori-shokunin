# CensusAtTip — source-census delta and QUALITY 82 lint at `f2de0eed`

**Verdict: holds** — attacked the census warning delta (S145–S152) and the QUALITY 82 host-identifier lint over
every file added/changed between `6ebd518f` and `f2de0eedcd60d2e354da75265ea6122bc3896073`. Census: exit 0, zero
`E` codes, +3 `W04` lines (S148, S149, S150), all three expected consequences of corrected superseding scopes, none
a defect. QUALITY 82: 0 hits in 69 files. One adjacent, material defect found outside my question: **S147 is absent
and `count-c1.sh f2de0eed` prints `C1=unmet`** (§4).

## 1. Method and what was actually run (all at 2026-10-22T18:56Z)

Tool bytes: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, sha256
`3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`. No tool was installed or upgraded. Scratch:
`/fast/scratch/hyaku/mori-r28-w2/CensusAtTip/`; lane writes: this report only.

1. **Working tree** (required command):
   `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → **exit 0**, 9 `W04`, one
   `mori ok` line (`/fast/scratch/hyaku/mori-r28-w2/CensusAtTip.validate-tip.txt:1-10`).
2. **Committed bytes, worktree-free** (script allows it): `git archive f2de0eed | tar -x` into
   `.../CensusAtTip/tiproot/mori-shokunin`, then `validate --root .../tiproot .../tiproot/mori-shokunin` → exit 0,
   same 9 `W04` + `ok` (`.../CensusAtTip/validate-extract.txt:1-10`). Byte comparison: working-tree
   `corpus/SOURCES.md` sha256 `afb571cd…e95ee` equals `f2de0eed:corpus/SOURCES.md`, so the working tree had not
   drifted at read time.
3. **Baseline reproduced, not assumed**: same command on a `git archive 6ebd518f` extract → exit 0, exactly six
   `W04` (S035, S037, S073, S074, S075, S076) + `ok` (`.../CensusAtTip/validate-baseline.txt:1-7`). The
   round-start six-W04 assertion is therefore grounded, not taken on faith.
4. `--file` note: `--file <SOURCES.md outside a corpus/ tree>` resolves `used-by` against the file's parent-of-parent
   (`sources-census.sh:500-502`) and therefore floods spurious `E11`; with the file at
   `<tree>/corpus/SOURCES.md` inside the full extract it prints the identical 9 `W04` + `ok`, exit 0
   (`.../CensusAtTip/validate-filemode.txt:1-10`). The flood is a layout artifact, **not** a lane defect.

## 2. New W04/E lines tied to S145–S152 — one ruling each

Delta (tip minus baseline): `W04 S148`, `W04 S149`, `W04 S150` — nothing else; **no `E01`–`E12` line exists at the
tip** for any row (exit 0, `ok`). Rows: `corpus/SOURCES.md:151-157` (S145, S146, S148, S149, S150, S151, S152; no
S147).

| new line | row line | duplicate URL class | ruling | evidence |
|---|---|---|---|---|
| `W04 S148` | `corpus/SOURCES.md:153` | same 3 URL set as S127 | **not a defect** | S148 carries `supersedes S127 — ` and corrects S127's `scope` (cgroup-`oom.group` pointer moved to S092's file; the LONG_MIN return moved to S003). W04 fires *because* the scope text differs — the documented "same URL across scopes" warning (`scripts/sources-census.sh:33,645`); exit 0. Wave-1 seat measured "one expected W04 … a warning, not an error" (`.ufo/waves/round-28/w1/SupersedeS127.md:143-144`). |
| `W04 S149` | `corpus/SOURCES.md:154` | same man7 URL pair as S128 | **not a defect** | Corrected scope for the F3 finding (3% root term / totalpages scaling attributed to S003); seat measured the exact line and ruled it the price of the correction, exit 0, no `E` (`.ufo/waves/round-28/w1/SupersedeS128.md:121,127`). |
| `W04 S150` | `corpus/SOURCES.md:155` | same `man/systemd.exec.xml` URL as S129 | **not a defect** | Corrected scope for the per-unit unset-default wording and the unprivileged-user-manager branch; seat measured the line and noted a verbatim-scope variant would be census-silent at the cost of keeping the wrong scope (`.ufo/waves/round-28/w1/SupersedeS129.md:20,185,201-203`). |

Why W04 (not E04): E04 requires the same URL **and** the same scope (`sources-census.sh:646-648`; W04 condition
`:644-645`); these rows
deliberately changed the scope cell, and all three `teaches` cells open `supersedes S0NN —`, so no E04 exemption
question arises. W04 is warning-only by the script's own contract (`sources-census.sh:33`) and does not change the
exit code.

The warning stays benign only while no live reader still cites the superseded rows. At `f2de0eed` the counter prints
`readers_left=0`; the one remaining S127 token in `corpus/knowledge/oom-victim-selection-r27.md:203` is the
tsukuroi-registry mention the counter excludes, as the wave-1 seat predicted
(`.ufo/waves/round-28/w1/SupersedeS127.md:27`). [INFERENCE] If a later batch re-cites S127/S128/S129 in a live
reader, this W04 class becomes load-bearing rather than cosmetic.

## 3. Rows tied to S145–S152 that produced **no** new line (and why that is not hiding a defect)

- S145 (`:151`) — reuses S096's URL with the **identical** scope text, so the census stays silent by design. Matches
  the seat's prediction of "only the six pre-existing W04" (`.ufo/waves/round-28/w1/SupersedeS096.md:183`).
- S146 (`:152`) — different URL (`man-pages-6.20.tar.xz` vs the 404 man7 page), so no duplicate exists to warn on.
- S151 (`:156`), S152 (`:157`) — URL cells changed (S151 adds `?recursive=1` plus Makefile/init-script files; S152
  pins two commits' raw files), so no normalized-URL collision. Consistent with
  `.ufo/waves/round-28/w1/SupersedeS131.md:127` and `SupersedeS140.md:68`.
- S147 — **no row exists**, so the census cannot warn about it; see §4. Census silence here is the absence of a
  row, not health.

## 4. Adjacent defect at the attack revision (outside my assigned question, material)

`bash .ufo/waves/round-28/count-c1.sh f2de0eedcd60d2e354da75265ea6122bc3896073` prints:

```
row_identity=rows=151 changed=0 removed=0 bad=0
superseding=7/8 ids=S096,S097,S127,S128,S129,S131,S140
fail S147 row_absent
readers_left=0
C1=unmet
exit=1
```

C1's own `MAP` expects `S147:S101` (quoted in `.ufo/waves/round-28/w1/SupersedeS128.md:112`), and `corpus/SOURCES.md`
at `f2de0eed` has no S147 row (ids present above S144: S145, S146, S148–S152). So at this exact revision the C1
statement — "for each of S096, S097, S101, … a new row" — is unmet, and the census cannot detect it because
`validate` has no expected-id list. This is a C1 finding, not a census finding; I did not attempt to judge whether a
later batch closes it. [INFERENCE] The L1 is still integrating, so this may be transient, but it is the state of the
attack target.

## 5. QUALITY 82 lint — 0 hits

Definition at `corpus/QUALITY.md:378-381` (pattern `grep -nE 'user-[0-9]{3,}\.slice|user@[0-9]{3,}\.service|\bpid[
=:]*[0-9]{3,}|\buid[ =:]+[0-9]{3,}'`). Scope: all 69 files in `git diff --name-only 6ebd518f f2de0eed`
(58 added, 11 modified, 0 deleted), each read at the revision with `git show f2de0eed:<path>`.

Result: **`hits=0`**, `files_checked=69`, empty stderr, so there is no `path:line` to list. A positive control on a
synthetic line (`.../CensusAtTip/q82-control.txt`) returned `control-hits=1`, proving the pattern and pipeline
actually match (an unrun or dead control would not count as a pass). No matched value is reproduced here.

## 6. Confidence and open items

- Confidence: **high** on the census outputs (three independent surfaces: working tree, committed extract, baseline
  extract; identical deltas), on the `W04` rulings (script semantics read at `sources-census.sh:638-650` plus three
  independent wave-1 measurements), and on the QUALITY 82 zero (with control).
- Not verified by me (out of question): whether the corrected scope cells in S148/S149/S150 are *factually* right
  against the upstream bytes, and whether C2 or the retention no-harm check passes. I did not reopen any source and
  did not run `count-c2.sh`.
- The S147 absence is the only red flag; it is invisible to the census and is reported as a C1 matter.
