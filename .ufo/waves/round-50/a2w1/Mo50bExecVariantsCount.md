# Mo50bExecVariantsCount — what round 49's `variants=26` counts, and which printed line is not a variant

Seat: leaf executor, round 50 attempt 2, wave a2w1. Assigned move: explain round 49's `variants=26` against the
27 printed `variant name=…` lines in `.ufo/waves/round-49/evidence/after-c1-at-tip.txt`; name the printed line that
is not a variant; reproduce by re-running the round-49 counter at its scored revision from scratch; supply the
one-sentence documentation for the lesson.

Scratch: `/fast/scratch/hyaku/mori-r50/Mo50bExecVariantsCount/` (created with `mkdir -p`, `TMPDIR` set to its `tmp/`,
removed at the end — see §7). One `git clone --shared` of the lane (330 MB) at most; no other clone. Disk guard
checked before the run: `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` listed only idle entries;
`df -h /fast` = 618 G free. No tool install or upgrade, no pacman transaction (host-wide pause respected), no writes
outside this file, no host log read, no cgroup or service change.

## 1. The counter's own arithmetic (source, verbatim)

`.ufo/waves/round-49/count-c1.py:303-306`:

```
    line = "C1=%s junk_met=%d honest_unmet=%d real=%s errors=%d variants=%d rev=%s" % (
        "met" if met else "unmet", junk_met, honest_unmet, real, errors, len(results) - 1, rev)
    return met, line
```

`variants` is `len(results) - 1`: one per executed run, minus exactly one. It is not a count of edits, of staged
files, or of names matching a variant pattern; the same `verdict()` computes `junk_met`, `honest_unmet`, `errors` and
`real` from the row names but never from the name for `variants`.

Where the runs come from, `count-c1.py:260-279` (`plan`):

```
        for name, expect, fn in list(r48.VARIANTS) + NEW_VARIANTS:
            stage(name, expect, fn(text))
        stage("real-opaque", "met", text)
        for name, expect, move in CLONE_VARIANTS:
            d, sha, base = fixture_variant(scratch, move)
            jobs.append((name, expect, None, d, sha, os.path.join(scratch, "t-" + opaque(sha)), base, 1))
...
    jobs.append(("real", "met", None, repo, rev, os.path.join(scratch, "t-" + opaque(rev, "real")), baseline, min_tally))
```

Enumerated at the scored revision (import of the frozen module, scratch `TMPDIR`, no run):

```
len(ORDER)=27
ORDER=J1,J2,J3,J4,J5,J6,J7,J8,H1,H2,H3,H4,N1,N2,N3,N4,N5,N6,N7,N8,N9,H6,H7,N10,H5,real,real-opaque
r48.VARIANTS=12 NEW=11 CLONE=2
edits=25
order_minus_one_excluded=['real', 'real-opaque']
dups=[]
```

So the 27 runs are 25 edit functions (J1-J8, H1-H4 = 12; N1-N9, H6, H7 = 11; N10, H5 = 2 fixture edits) plus two
runs of **unedited** `SKILL.md` at R: `real` (R's own file, no staging copy) and `real-opaque` (a byte-identical copy
staged under a sha256-derived name). `26 = 27 - 1` therefore lands on **25 edits + `real-opaque`**.

The counter's docstring says the same thing in prose, `count-c1.py:8-9`: "… and on R's SKILL.md read **twice** (as the
revision's own file and as an opaque-named copy)". Both of those are unedited, so by the predicate's own wording
`variants` is not the variant count.

## 2. The printed line that is not a variant

`variant name=real expect=met got=met rc=0` — the last line but one. It is the only run whose argument is the repo
itself rather than a staged file or fixture repo, and it is the run the `- 1` drops.

Strictly, two printed lines carry no edit (`real` and `real-opaque`); the arithmetic drops only `real`, which is why
`variants=26` exceeds the edit count 25. Round 48 had no `real-opaque` run (`.ufo/waves/round-48/count-c1.py:242`
appends only `("real", "met", None)`; `ORDER` is `VARIANTS + ["real"]`, and `len(VARIANTS)=12` for
J1-J8,H1-H4 — read by import), so under that counter `variants` happened to equal the edit count (12, as
`corpus/lessons/round-49.md:166` records). Round 49 added `real-opaque` to close round 48's harness leak without
changing the `- 1`, so the same field moved to "one more than the edits". Nothing regressed: the contract target
`.ufo/waves/round-49/contract.md:25` itself pins `variants=26`, and the counter reaches it.

## 3. Committed evidence, read-only

- `.ufo/waves/round-49/evidence/after-c1-at-tip.txt`: `grep -c '^variant name='` = **27**; `C1=met junk_met=0
  honest_unmet=0 real=met errors=0 variants=26 rev=64c2d5fcd95a11f195de0387fa791cab7a54ecb1`, `exit=0`. Name set
  equals `ORDER` (`same_set=True missing=[] extra=[]` from the import check in §1).
- `.ufo/waves/round-49/evidence/control-c1-tool-v3-entering.txt`: the entering v3 tool also prints 27 lines and
  `variants=26` (rev `b3e3453d45ff…`), so the number is revision- and tool-independent — it is the run count.
- `.ufo/waves/round-49/evidence/selftest-c1.txt`: `PASS order_covers_every_variant  27` and
  `PASS verdict_line_shape  C1=met … variants=3 rev=r` (four synthetic rows in, `variants=3` out) — the committed
  selftest already states the `runs - 1` rule.
- Direct probe of the frozen `verdict()` (import, no tool run): `runs=1 -> variants=0`, `runs=2 -> variants=1`,
  `runs=26 -> variants=25`, `runs=27 -> variants=26`.

## 4. Reproduction at the scored revision

Round-49 revision used by the C1 receipt: `64c2d5fcd95a11f195de0387fa791cab7a54ecb1` (`git log` subject "round-49: data
C1 — pin reconciler v4 (114 arms), unlanded check (17 arms), …"; `LOG.md` round-49 entry gives entering `b3e3453d` and
freeze `0df17b7b`, the receipt line names the tip). Setup, all inside scratch:

```
S=/fast/scratch/hyaku/mori-r50/Mo50bExecVariantsCount; export TMPDIR=$S/tmp
cp .ufo/waves/round-49/count-c1.py $S/waves/round-49/count-c1.py      # frozen counter + its round-48 import
cp .ufo/waves/round-48/count-c1.py $S/waves/round-48/count-c1.py
git show 64c2d5fc:tools/mori-pin-check.py > $S/tool-r49.py            # tool bytes AT the scored rev (1425 lines)
git clone --shared -q /home/vgpnk/Projects/shokunin/mori-shokunin $S/repo   # history for --rev and --baseline-rev
```

Run (`--jobs 4`, the receipt's default), wall time 9 m 29 s — inside the 10-minute budget:

```
$ python3 -I -B $S/waves/round-49/count-c1.py --tool $S/tool-r49.py --repo $S/repo \
    --rev 64c2d5fcd95a11f195de0387fa791cab7a54ecb1 --scratch $S/c1 --jobs 4
variant name=J1 expect=unmet got=unmet rc=1
variant name=J2 expect=unmet got=unmet rc=1
variant name=J3 expect=unmet got=unmet rc=1
variant name=J4 expect=unmet got=unmet rc=1
variant name=J5 expect=unmet got=unmet rc=1
variant name=J6 expect=unmet got=unmet rc=1
variant name=J7 expect=unmet got=unmet rc=1
variant name=J8 expect=unmet got=unmet rc=1
variant name=H1 expect=met got=met rc=0
variant name=H2 expect=met got=met rc=0
variant name=H3 expect=met got=met rc=0
variant name=H4 expect=met got=met rc=0
variant name=N1 expect=unmet got=unmet rc=1
variant name=N2 expect=unmet got=unmet rc=1
variant name=N3 expect=unmet got=unmet rc=1
variant name=N4 expect=unmet got=unmet rc=1
variant name=N5 expect=unmet got=unmet rc=1
variant name=N6 expect=unmet got=unmet rc=1
variant name=N7 expect=unmet got=unmet rc=1
variant name=N8 expect=unmet got=unmet rc=1
variant name=N9 expect=unmet got=unmet rc=1
variant name=H6 expect=met got=met rc=0
variant name=H7 expect=met got=met rc=0
variant name=N10 expect=unmet got=unmet rc=1
variant name=H5 expect=met got=met rc=0
variant name=real expect=met got=met rc=0
variant name=real-opaque expect=met got=met rc=0
C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26 rev=64c2d5fcd95a11f195de0387fa791cab7a54ecb1
exit=0
```

`diff -u` against the committed receipt is empty for every one of the 28 output lines (the only difference the diff
reports is the receipt's trailing `exit=0` line, which the counter does not print; I appended it). At that revision
the tool **reaches** the target, which is consistent with `LOG.md:2727` and the contract's target row.

## 5. The one-sentence documentation for the lesson

```
`variants` is the number of executed runs minus the single `real` control (`count-c1.py:305`, `len(results) - 1`) — not the number of edits: round 49's 27 printed `variant name=…` lines are 25 frozen edits plus `real-opaque`, a byte-identical opaque-named copy of the unedited `SKILL.md`, so `variants=26` matches the 27 lines and the one line the arithmetic leaves out is `variant name=real`.
```

(A shorter variant if the lesson row needs one clause: "`variants` counts runs minus one — the `real` run; `real-opaque`,
though itself unedited, is inside the 26.")

## 6. Limits of this seat's work

- I did not operate on any data file. The lesson sentence is a draft in §5; `.ufo/waves/round-49/count-c1.py`, the
  contracts and the receipts were read only, and no counter, predicate or kill rule was changed or proposed for change.
- The `variants` naming is a frozen-counter property. It is a documentation limit only: P-C1's number and the counter
  agree, so nothing in round 49's score is affected.
- Round 48's "12" is code-read plus the lane's own lesson text (`corpus/lessons/round-49.md:166`); I did not re-run the
  round-48 counter at its own revision.
- `[UNVERIFIED]` whether any reader outside this lane has already interpreted `variants` as an edit count; I checked the
  round-49 contract, disposition and the round-49 lesson, none of which defines the field.

## 7. Scratch

`rm -rf /fast/scratch/hyaku/mori-r50/Mo50bExecVariantsCount` after quoting §1-§4. Everything cited here is inside this
file; no `/tmp` path is evidence and no scratch file was left behind.

## Findings

- **LOW — `.ufo/waves/round-49/count-c1.py:305` (`variants=%d … len(results) - 1`) and `:38` (output spec):** the field
  is `runs - 1`, not an edit count, and no comment or docstring says so near the format string; a reader comparing it
  with 27 printed lines cannot tell the arithmetic from the file. The one sentence in §5 closes this. Severity LOW
  because the contract target (`contract.md:25`) pins `variants=26` and the counter reaches it — no score changes.
- **LOW — `.ufo/waves/round-49/count-c1.py:266` (`stage("real-opaque", …)`) vs the same file's docstring `:8-9`:** the
  predicate describes both `real` and `real-opaque` as "R's SKILL.md read twice", yet `real-opaque` is counted inside
  `variants` while `real` is not, so `variants` (26) is one greater than the 25 edits. Not a defect in the run set —
  a naming limit that the lesson sentence must state, otherwise a later round that adds a second unedited control
  will move the number without moving any edit.
- **LOW — `.ufo/waves/round-49/contract.md:25,48` and `.ufo/waves/round-50/contract.md:151` (routed defect 6):** the
  routed item asks for the documentation and it is still not in `corpus/lessons/round-49.md` (`grep -n "variants"`
  shows only lines 166, 197, 200, none of which defines the field). §5 supplies it; the L1 integrates.
- **INFO — `.ufo/waves/round-48/count-c1.py:242,253`:** round 48's `variants` equalled its edit count only because that
  counter had no `real-opaque` run; the `- 1` convention is inherited unchanged from there.
