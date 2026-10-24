measured 2026-10-23T09:14:03Z
# MutQ100 — isolated-cell action check

## Target and axes

Attacked QUALITY criterion 100 at `cedb0ec4f3a4f672804deac388b7191258f01fcd`, not a moving working-tree version: `corpus/QUALITY.md:779-787`.
Axes: header independence, imperative action, resolving object, acceptance of a valid action, and byte-exact restoration (`/fast/scratch/hyaku/mori-r35/MutQ100/expectations.txt:1-9`).

Scratch root below is `/fast/scratch/hyaku/mori-r35/MutQ100/`.
The frozen source snapshot is `QUALITY.frozen.md:779-787`, obtained with:

```sh
timeout 30 prlimit --as=1073741824 --cpu=20 git -C /home/vgpnk/Projects/shokunin/mori-shokunin show cedb0ec4f3a4f672804deac388b7191258f01fcd:corpus/QUALITY.md
```

Observed: success, 77554 bytes; SHA-256 `a4bc5d6e2d83ef8b867f594743ca956cda06b488602e3cac19f5880c43b69e98` (`observations.txt:1-3`).

## Detector and baseline

Applied the written Check manually: select the verdict by position, then judge only its own text, excluding header and neighbouring cells. The predicate being judged is the criterion's imperative plus resolving command, path or field; this is not merely a keyword test (`QUALITY.frozen.md:779-782`).

The bounded helper only extracts the cell and hashes the fixture. Its successful execution is not a semantic PASS (`select-cell.py:6,13-27`; `observations.txt:5-7,44`). No new semantic gate or other runtime was invoked.

For each of `header-only.md`, `unresolvable.md`, `bare-label.md`, and `passing-action.md`, ran this same command on pristine, mutated and restored bytes:

```sh
timeout 15 prlimit --as=268435456 --cpu=5 python3 -I -B /fast/scratch/hyaku/mori-r35/MutQ100/select-cell.py /fast/scratch/hyaku/mori-r35/MutQ100/<fixture>
```

All twelve selections completed successfully and selected `table1,data-row1,column2`. Every pristine cell was Read `corpus/QUALITY.md` criterion 100. Manual baseline result: accept, because Read is imperative and the named file and criterion resolve at the pinned revision (`observations.txt:7-12,38-41`; `QUALITY.frozen.md:779-787`). Expected outcomes were recorded before mutation (`expectations.txt:4-9`).

Each fixture has one data row. Its fixed column-2 header is Read next, and the fixed neighbouring observation identifies `corpus/QUALITY.md` criterion 100. Only the verdict cell on line 3 changed; the selected text never includes the header or observation (`header-only.md:1-3`; `select-cell.py:19-27`; `expectations.txt:9`).

## 1. Action supplied only by header

Mutation: delete Read from the pristine verdict, leaving `corpus/QUALITY.md` criterion 100.
Expected: reject; the header cannot supply the missing imperative (`expectations.txt:5`; `QUALITY.frozen.md:781-782`).
Observed selected text: `corpus/QUALITY.md` criterion 100. Manual Check: reject. This names an object but gives no action without the excluded Read next header (`observations.txt:14-18`).
VERDICT: killed — header-only action

## 2. Imperative with an unresolvable object

Mutation: replace the verdict with Read it.
Expected: reject; the imperative remains, but it has no antecedent within the cell (`expectations.txt:6`).
Observed selected text: Read it. Manual Check: reject. Resolving it from the neighbouring observation would violate the written Check; the reader cannot identify a command, path or field from the cell itself (`observations.txt:20-24`; `QUALITY.frozen.md:779-782`).
VERDICT: killed — unresolvable object

## 3. Bare label

Mutation: replace the verdict with candidate.
Expected: reject, including under the criterion's explicit failing example (`expectations.txt:7`; `QUALITY.frozen.md:782-784`).
Observed selected text: candidate. Manual Check: reject; neither an imperative nor a resolving object is present (`observations.txt:26-30`).
VERDICT: killed — bare label

## 4. Passing-action control

Mutation: change Read to Report, retaining `corpus/QUALITY.md` criterion 100 as its object.
Expected: accept; this is a positive control, not an injected defect (`expectations.txt:8`).
Observed selected text: Report `corpus/QUALITY.md` criterion 100. Manual Check: accept; the cell independently supplies an imperative and resolving object (`observations.txt:32-36`; `QUALITY.frozen.md:779-780`).
VERDICT: survived — passing action, expected positive-control acceptance

## Hashes and restoration

Every pristine fixture SHA-256 was:
`6e17a5cb2aa704436cab8dee8b198f29000e75e2a0e0d530ddce91d9fb9170b1` (`observations.txt:9-10`).

Mutated full-fixture SHA-256 outputs:
- header-only: `a807dcf7f272ee8969012d19febd21f24e99e1b7a9c4e7703289b2b4464a0d0b` (`observations.txt:15`).
- unresolvable: `af2599a4650a48fe416f072440947bb0b37f8ca6f8c75edc473aa1a0f041420e` (`observations.txt:21`).
- bare-label: `fce32e1a870695a37123273cd484678b782026a6f511fa299ba493ccaa33d5ca` (`observations.txt:27`).
- passing-action: `c05624637840a6f165afda2f0709b21751410c49b2f9dc6eafe69757380c0314` (`observations.txt:33`).

All four fixtures were restored. Each restored command printed the original complete-fixture SHA-256 above and the original Read action; manual Check again accepted each. No baseline failure or inconclusive case occurred (`observations.txt:38-41`).

## Holes and limits

No coverage hole was exposed by these four manual applications: the three invalid cells were rejected and the valid action was retained (`observations.txt:14-36`). The unresolved-object probe covers a dangling pronoun, not every plausible-looking nonexistent command, path or field. Automatic semantic enforcement was not measured: the helper only selects bytes (`select-cell.py:6,25-27`). Action correctness, sourcing and whether the claim's counter rejects a no-decision control remain explicitly outside criterion 100 (`QUALITY.frozen.md:786-787`).

## Containment

Only this report was written in the lane; fixture, expectation, source-snapshot, helper and observation writes stayed under the scratch root. No Git writes, lane-source mutation, host-service changes, installations, background jobs or subagents were used. All command processes completed; no process tree remains to stop. The only live host observations were bounded date and filesystem-capacity commands; `df -h /fast` reported 170G available before scratch creation. The measured timestamp above is the output recorded at `observations.txt:42-43`. No builds, linters, broader selftests or C1 counter runs were performed.
