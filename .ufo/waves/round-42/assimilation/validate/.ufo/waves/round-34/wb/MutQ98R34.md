measured 2026-10-23T07:49:09Z
# MutQ98R34 — QUALITY 98 contract mutations

Axes: shape coverage; defect-bearing controls; receipt chronology; exact-byte restoration.
Target: `fd2521351c6cef47384aef30afbe1e4db7e6912e:corpus/QUALITY.md:715-731`, applied to `b9fb029e05dcfb79757c46821dc4b61cb79d1a29:.ufo/waves/round-34/contract.md`.

Evidence directory **S** = `/fast/scratch/hyaku/mori-r34/a3-MutQ98R34`.
All four variants are independent copies of the pristine contract, not cumulative edits.
Included script: `S/check98.py:1-84`; complete actual commands, stdout, stderr and exits: `S/probe-results.json:1-98`.
Pinned inputs: `S/contract-pristine.md`, `S/QUALITY-pinned.md`, `S/c1-controls-original.txt`, captured with read-only `git show` at the revisions above.

## Detector and interpretation

The script is a finite hand transcription of the written Check (a)-(c), not a new lane gate or an implementation of the frozen C1 counter (`S/check98.py:2-7`).
It treats the seven semicolon-separated shape groups as seven obligations, keeping the two `or` alternatives as alternatives. As the assignment specifies, C-naive is the full no-decision control; the two `no-decision, partial` rows are supplemental. `Once` means exactly once (`S/check98.py:39-46`).
Inapplicability needs a stated nonempty reason; neither (a), (b), nor (c) requires an independent assessment of that reason (`S/QUALITY-pinned.md:715-725`; `S/check98.py:60-64`).
Named controls must have an `unmet` P-C1-A1 receipt, not merely a P-C1 result. The table's C-echo is bound to the Amendment A1 base64 echo control, not its earlier literal-string guard failure (`S/check98.py:53-71`; `S/c1-controls-original.txt:26-31`).
The receipt commit is the addition commit of the cited file, determined from Git history; (c) uses Git ancestry, not the receipt's printed timestamp (`S/check98.py:72-76`).

Exact detector invocation, repeated on the same active path at each pristine/mutated/restored stage (`S/probe-results.json:5,13,21`):

```sh
timeout 30s prlimit --as=268435456 --cpu=20 -- python3 -I -B /fast/scratch/hyaku/mori-r34/a3-MutQ98R34/check98.py /fast/scratch/hyaku/mori-r34/a3-MutQ98R34/contract-active.md /fast/scratch/hyaku/mori-r34/a3-MutQ98R34/clone
```

## Real commit order and the late-receipt fixture

Read-only command: `timeout 30s prlimit --as=536870912 --cpu=20 -- git -C /home/vgpnk/Projects/shokunin/mori-shokunin show --no-patch --format='%H%nparents=%P%ncommitter=%cI%nsubject=%s' 2460318 b9fb029 ba525e1`.
Actual output establishes this direct-parent chain:

| Commit | Parent | Committer time | Content |
|---|---|---|---|
| `24603186b555dddb88ebd607e415e27bdea747b4` | `f10a320d9056d19a6d007420df49d7b16a3bf857` | `2026-10-23T01:53:22-03:00` | initial contract/counter freeze |
| `b9fb029e05dcfb79757c46821dc4b61cb79d1a29` | `24603186b555dddb88ebd607e415e27bdea747b4` | `2026-10-23T02:13:33-03:00` | C0 receipts and pre-data A1 |
| `ba525e1a0394154837eea5090e8bd27ed69c539c` | `b9fb029e05dcfb79757c46821dc4b61cb79d1a29` | `2026-10-23T02:30:38-03:00` | first landed C1 tool/data |

`git log --reverse --format='%H %cI %s' --name-status f10a320d..ba525e1 -- .ufo/waves/round-34 tools/mori-disk-rate.py` printed `A .ufo/waves/round-34/evidence/c1-controls.txt` at b9fb029 and `A tools/mori-disk-rate.py` at ba525e1. Thus b9fb029 is not post-tool just because it is later than the initial freeze. Ancestry checks for 2460318→b9fb029 and b9fb029→ba525e1 both exited 0 (`S/chronology.txt:1-2`).

For variant 4 only, I created the explicitly synthetic scratch commit `92982c4f4460ad4286a51932aa370d4cfe57bd66`, direct child of the real ba525e1, adding only `.ufo/waves/round-34/evidence/c1-controls-late.txt` with the original receipt bytes. The contract cites that new path and commit; its table is unchanged. This is a late filing fixture, not a claimed new measurement or a lane commit (`S/chronology.txt:3-8`; `S/variant-4-late-receipt.md:143-144`).
Its committer time is `2026-10-23T04:47:15-03:00`; reverse ancestry to ba525e1 exited 1. Original and late receipt hashes are identical: `fb15da4786671b9a341399f658dbed2375f306b06f31eefe25a9e255928976ab` (`S/chronology.txt:4-7`; `S/probe-results.json:79,87`).

## Results

Pristine: (a)=true, (b)=true, (c)=true, `check98=accept`, exit 0 before every mutation. Every restored run produced the same result; stderr was empty in all twelve runs (`S/probe-results.json:1-98`).

### 1. Delete C-naive

Delta: delete the entire original contract row 73; retain both partial rows (`S/variant-1-delete-naive.md:71-75`; original `S/contract-pristine.md:73-75`).
Expected detector: (a) rejects the missing full no-decision shape.
Actual: `a=false a_bad={"no-decision":0} b=true c=true check98=reject`, exit 1 (`S/probe-results.json:11-16`).
VERDICT: killed — variant 1, missing no-decision shape.

### 2. Relabel C-alldisk and substitute absence

Delta: replace original row 74 with `| no-decision | tool absent | unmet |`; leave C-naive present (`S/variant-2-absence.md:73-75`).
Expected detector: (a) finds two full no-decision rows and (b) cannot bind `tool absent` to a named control receipt. Independently, the criterion's substantive absence clause rejects an absent deliverable as a no-decision witness (`S/QUALITY-pinned.md:718-720`).
Actual: `a=false a_bad={"no-decision":2} b=false b_bad=["unnamed-control:tool absent"] c=true check98=reject`, exit 1 (`S/probe-results.json:35-40`).
VERDICT: killed — variant 2, duplicate shape and unnamed receipt; also disallowed by the explicit absence clause.
This probe does not isolate enforcement of defect injection: the syntactic failures already kill it. Even if `tool absent` were read as C-absent, the substantive clause still rejects its use for no-decision content. No stronger enforcement claim is inferred.

### 3. Declare label-keying inapplicable

Delta: replace C-labelkey with `inapplicable: the rate contract uses numeric counters, not labels, as its rate inputs`, expected `—` (`S/variant-3-inapplicable.md:77`).
Expected detector: accept the reason-bearing inapplicability, retain the shape, and require receipts only for the remaining named controls.
Actual: `a=true b=true c=true check98=accept`, exit 0 (`S/probe-results.json:59-64`).
VERDICT: survived — variant 3, reason-bearing inapplicability bypasses a label-keyed control requirement.
[INFERENCE] The reason does not establish that an implementation cannot key answers on input labels/bytes. The real contract explicitly proposes that shortcut, and the committed original receipt records its fixed cases passing 12/12 but random cases passing 0/300 (`S/contract-pristine.md:77`; `b9fb029e:.ufo/waves/round-34/evidence/c1-controls.txt:23-25`). Survival is a coverage finding about the written checks, not permission to change the criterion or proof that the proposed inapplicability is true.

### 4. Cite a post-tool receipt file

Delta: change only the receipt citation to the synthetic late path/commit described above; retain the table (`S/variant-4-late-receipt.md:143-144`).
Expected detector: (a) and (b) pass, but (c) rejects a receipt added in a child of first data.
Actual: `a=true b=true c=false ancestry_rc=1 check98=reject`, exit 1 (`S/probe-results.json:83-88`).
VERDICT: killed — variant 4, late cited receipt fails ancestry.
This does not erase or invalidate the real earlier receipt at b9fb029; it tests the named late citation only.

## Hashes and restoration

Pristine SHA-256 **H** = `695c8412769da278932b44198649853c140d0eeda88e7591f71bc2950765cc11` (`S/probe-results.json:7`).
Every row below is an observed pristine→mutated→restored sequence on `S/contract-active.md`; the stored variants remain available as scratch inputs.

| Variant | Before | Mutated SHA-256 | Restored | Exits |
|---|---|---|---|---|
| 1 | H | `0254c87e4864edf4a45ae1153392a3f1d39518a199ac1e78f8731c86e93d5030` | H | 0→1→0 |
| 2 | H | `135c2eb120c4217e7b2a907e1c8c742e3e60881cba17ea0f5695ac539d781087` | H | 0→1→0 |
| 3 | H | `1767be46c60b15fd3e14d37ca417dc6fcad1175cd182b33d1e0883c620b82603` | H | 0→0→0 |
| 4 | H | `a00fb0f64a4284dd6447480cff4e185144f13151093dedede8135932637683ae` | H | 0→1→0 |

Restoration evidence: `S/probe-results.json:7,15,23,31,39,47,55,63,71,79,87,95`. Restoration ran in a `finally` block using the original frozen bytes after each mutation. There was no baseline failure or inconclusive run.

## Bounds and disclosure

No tool or package was installed or updated. Only this report was written in the lane; all fixtures, the synthetic Git object and the detector are under S. No lane Git/jj writes, subagents, background jobs, live disk-rate/counter runs, block-device changes, harness changes or write-load files were used. The only executed behavioral check was the assigned bounded script above; each command was time- and memory-bounded. All subprocess calls returned before reporting (`S/check98.py:23-30`; `S/probe-results.json:1-98`).
Before the sandbox clone, `timeout 15s prlimit --as=268435456 --cpu=10 -- df -h /fast` printed `804G` size, `590G` used, `214G` available, `74%` use. Report timestamp comes from `timeout 10s prlimit --as=134217728 --cpu=5 -- date -u +%FT%TZ` → `2026-10-23T07:49:09Z`.
