# Routed R1 — tip receipts

## Checker and requested baseline

Read the complete checker (`.ufo/waves/round-28/check-tip-receipts.sh:1-101`). It reads committed objects, measures the child’s first parent, and requires round-scoped receipts that name the counter/retention command and measured parent, include `exit:` plus stdout, and are cited by name (`.ufo/waves/round-28/check-tip-receipts.sh:5-22,37-46,58-100`).

Command:

```sh
bash /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-28/check-tip-receipts.sh b581173afd85d82283291492de12666d505eb58b 29
```

Output:

```text
counter=count-c1.sh receipt=.ufo/waves/round-29/evidence/tip-c1.txt measured=67779aa8f761ac4e1f1620f67c2746076d8f31d3 cited_lane=no cited_fleet=na
counter=count-c2.sh receipt=.ufo/waves/round-29/evidence/tip-c2.txt measured=67779aa8f761ac4e1f1620f67c2746076d8f31d3 cited_lane=no cited_fleet=na
retention receipt=.ufo/waves/round-29/evidence/tip-retention.txt measured=67779aa8f761ac4e1f1620f67c2746076d8f31d3 cited_lane=yes cited_fleet=na
tip_receipts=unmet
exit=1
```

This is the requested `unmet` baseline. The output shows the two counter receipts were not cited; the retention receipt was cited.

## Round-30 mock batch

Created a no-hardlinks sandbox clone at `/fast/scratch/hyaku/mori-r30/TipReceiptsR1/repo` with:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin /fast/scratch/hyaku/mori-r30/TipReceiptsR1/repo
```
The mock parent was prepared and committed in that clone with:

```sh
cp /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-30/contract.md /fast/scratch/hyaku/mori-r30/TipReceiptsR1/repo/.ufo/waves/round-30/contract.md
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mori-r30/TipReceiptsR1/repo add -- LOG.md corpus/lessons/round-30.md .ufo/waves/round-30/contract.md
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mori-r30/TipReceiptsR1/repo -c user.name='TipReceiptsR1 mock' -c user.email='tipreceiptsr1@example.invalid' commit -m 'Build mock round-30 receipt parent'
```

Commit output:

```text
[master 52a509f] Build mock round-30 receipt parent
2 files changed, 5 insertions(+), 1965 deletions(-)
create mode 100644 corpus/lessons/round-30.md
```

The parent is `52a509f7ff21ba2b2f76c42707e38cedb186dd5e`. Both mock reports contain this receipt citation line:

```text
Receipts: `tip-c1.txt`, `tip-c2.txt`, and `tip-retention.txt`.
```

`git show --format= --name-status <parent>` reported `M LOG.md` and `A corpus/lessons/round-30.md`; `git show <parent>:LOG.md` and `git show <parent>:corpus/lessons/round-30.md` printed the mock heading and citation above. The lane contract was copied into the parent. `sha256sum` of the lane contract and scratch copy, plus `git show <parent>:.ufo/waves/round-30/contract.md | sha256sum`, yielded this same digest each time: `7f1051947220f3f7946d2c9864e1ec442fd95de75b2e56be5d8e28ed965efca9`. This is the lane contract at `.ufo/waves/round-30/contract.md`; its round-30 counter command forms are at `:44-48,88-92`.

Child add/commit command:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mori-r30/TipReceiptsR1/repo add -- .ufo/waves/round-30/evidence/tip-c1.txt .ufo/waves/round-30/evidence/tip-c2.txt .ufo/waves/round-30/evidence/tip-retention.txt
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mori-r30/TipReceiptsR1/repo -c user.name='TipReceiptsR1 mock' -c user.email='tipreceiptsr1@example.invalid' commit -m 'Add mock round-30 tip receipts'
```

Commit output:

```text
[master eb82b01] Add mock round-30 tip receipts
3 files changed, 12 insertions(+)
create mode 100644 .ufo/waves/round-30/evidence/tip-c1.txt
create mode 100644 .ufo/waves/round-30/evidence/tip-c2.txt
create mode 100644 .ufo/waves/round-30/evidence/tip-retention.txt
```
The normal child is `eb82b011730c2c799c7a6e8ea6272d37a8b494fb`. `git diff-tree --no-commit-id --name-status -r <child>` returned only:

```text
A .ufo/waves/round-30/evidence/tip-c1.txt
A .ufo/waves/round-30/evidence/tip-c2.txt
A .ufo/waves/round-30/evidence/tip-retention.txt
```

The exact mock receipt header lines are:

```text
# measured at parent 52a509f7ff21ba2b2f76c42707e38cedb186dd5e; counter count-c1.sh
# measured at parent 52a509f7ff21ba2b2f76c42707e38cedb186dd5e; counter count-c2.sh
# measured at parent 52a509f7ff21ba2b2f76c42707e38cedb186dd5e; scan mori-retention-gate.py
```

Each body also has its full-parent command line, a `mock stdout:` line and `exit: 0` (`/fast/scratch/hyaku/mori-r30/TipReceiptsR1/repo/.ufo/waves/round-30/evidence/tip-{c1,c2,retention}.txt:1-4`). These are synthetic receipts, not runs of the counters or retention scan.

The checker hard-codes the lane path (`.ufo/waves/round-28/check-tip-receipts.sh:24`), so a scratch-only Git router at `/fast/scratch/hyaku/mori-r30/TipReceiptsR1/bin/git` redirected its `git -C <lane>` reads to the clone. The router unsets inherited Git directory/index variables (`.../bin/git:1-7`). Command and output:

```sh
PATH=/fast/scratch/hyaku/mori-r30/TipReceiptsR1/bin:$PATH bash /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-28/check-tip-receipts.sh eb82b011730c2c799c7a6e8ea6272d37a8b494fb 30
```

```text
counter=count-c1.sh receipt=.ufo/waves/round-30/evidence/tip-c1.txt measured=52a509f7ff21ba2b2f76c42707e38cedb186dd5e cited_lane=yes cited_fleet=na
counter=count-c2.sh receipt=.ufo/waves/round-30/evidence/tip-c2.txt measured=52a509f7ff21ba2b2f76c42707e38cedb186dd5e cited_lane=yes cited_fleet=na
retention receipt=.ufo/waves/round-30/evidence/tip-retention.txt measured=52a509f7ff21ba2b2f76c42707e38cedb186dd5e cited_lane=yes cited_fleet=na
tip_receipts=met
exit=0
```

## Uncited-receipt mutation

Created a separate child of the same parent (`99667b48ca77350515bab27c6a883321adde0217`) with the same three receipts, but removed only the `tip-c2.txt` citation from both mock reports. The `tip-c2.txt` receipt remains present and still measures the correct first parent. Command and output:

The mutation child was made from the same parent on a sibling branch:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mori-r30/TipReceiptsR1/repo switch -c mock-uncited 52a509f7ff21ba2b2f76c42707e38cedb186dd5e
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mori-r30/TipReceiptsR1/repo add -- LOG.md corpus/lessons/round-30.md .ufo/waves/round-30/evidence/tip-c1.txt .ufo/waves/round-30/evidence/tip-c2.txt .ufo/waves/round-30/evidence/tip-retention.txt
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mori-r30/TipReceiptsR1/repo -c user.name='TipReceiptsR1 mock' -c user.email='tipreceiptsr1@example.invalid' commit -m 'Remove C2 citation in mock receipt batch'
```

Commit output:

```text
[mock-uncited 99667b4] Remove C2 citation in mock receipt batch
5 files changed, 14 insertions(+), 2 deletions(-)
create mode 100644 .ufo/waves/round-30/evidence/tip-c1.txt
create mode 100644 .ufo/waves/round-30/evidence/tip-c2.txt
create mode 100644 .ufo/waves/round-30/evidence/tip-retention.txt
```

```sh
PATH=/fast/scratch/hyaku/mori-r30/TipReceiptsR1/bin:$PATH bash /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-28/check-tip-receipts.sh 99667b48ca77350515bab27c6a883321adde0217 30
```

```text
counter=count-c1.sh receipt=.ufo/waves/round-30/evidence/tip-c1.txt measured=52a509f7ff21ba2b2f76c42707e38cedb186dd5e cited_lane=yes cited_fleet=na
counter=count-c2.sh receipt=.ufo/waves/round-30/evidence/tip-c2.txt measured=52a509f7ff21ba2b2f76c42707e38cedb186dd5e cited_lane=no cited_fleet=na
retention receipt=.ufo/waves/round-30/evidence/tip-retention.txt measured=52a509f7ff21ba2b2f76c42707e38cedb186dd5e cited_lane=yes cited_fleet=na
tip_receipts=unmet
exit=1
```

This isolates the report-citation condition: only C2 changes from `cited_lane=yes` to `no`; the gate changes from met to unmet. The mutation is a sibling child of the same parent so the first-parent hash remains valid.

## Round-30 generator adaptation

Read the complete `.ufo/waves/round-29/make-tip-receipts.sh` (`:1-108`). Unchanged, it is not a round-30 generator: it writes a round-29 header, uses round-29 counter paths, and passes a hard-coded extra argument to C1 (`:13-16,50-63,86-105`). A round-30 copy is at `/fast/scratch/hyaku/mori-r30/TipReceiptsR1/make-tip-receipts-r30.sh`. It changes the evidence path in the header, puts the measured operation in each header, switches both counters to `.ufo/waves/round-30/count-c*.sh`, calls each with only `$parent`, and removes the round-29 `fleet_rev` argument (`:49-60,64-93,96-100`). The single-parent counter arguments match the round-30 contract (`.ufo/waves/round-30/contract.md:44-48,88-92`).

After the round-30 counters are committed and with `PARENT` set to the full hash immediately before the receipt-only batch, the exact lane-owner invocation is:

```sh
PARENT=<full-40-hex-parent>
bash /fast/scratch/hyaku/mori-r30/TipReceiptsR1/make-tip-receipts-r30.sh "$PARENT" /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-30/evidence
```

This seat did not run that command because it writes into the lane; only the assigned report was written there. No packages were installed. The mock validates checker wiring only: its stdout and exit values are deliberately synthetic, so real counter and retention outcomes remain unverified. No blocker to the requested mock/checker demonstration.