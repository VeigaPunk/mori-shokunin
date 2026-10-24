# Round-40 witness fixture byte comparison

Compared round-40 fixtures against their round-39 counterparts. Working directory for every command below: `/home/vgpnk/Projects/shokunin/mori-shokunin`.

## SHA-256

Command:
```sh
sha256sum .ufo/waves/round-40/fixtures/witness-token-entry.md .ufo/waves/round-40/fixtures/witness-dangling-row.md .ufo/waves/round-40/fixtures/witness-summary-only-live.txt .ufo/waves/round-40/fixtures/witness-comment-anchors.md
```
Output:
```text
ce4dac65d1dd0ee55f71de1ee5937d474fdfecf32ea599ea3a204395178194f2  .ufo/waves/round-40/fixtures/witness-token-entry.md
bc62b0b3db38fbf6086eb5dbdff50a90e5901046ab012abb23e89d9c50357ff2  .ufo/waves/round-40/fixtures/witness-dangling-row.md
8ac9e82bae369a2e41f4a4377016c3e82d58c8c6de484722f1d85b0bbf7cb4af  .ufo/waves/round-40/fixtures/witness-summary-only-live.txt
fc95dc69153f47c2f934a0e9be069764a9da7b606dc0274ffd0f5672f3bd4623  .ufo/waves/round-40/fixtures/witness-comment-anchors.md
```

Command:
```sh
sha256sum .ufo/waves/round-39/fixtures/witness-token-entry.md .ufo/waves/round-39/fixtures/witness-dangling-row.md .ufo/waves/round-39/fixtures/witness-summary-only-live.txt .ufo/waves/round-39/fixtures/witness-comment-anchors.md
```
Output:
```text
ce4dac65d1dd0ee55f71de1ee5937d474fdfecf32ea599ea3a204395178194f2  .ufo/waves/round-39/fixtures/witness-token-entry.md
bc62b0b3db38fbf6086eb5dbdff50a90e5901046ab012abb23e89d9c50357ff2  .ufo/waves/round-39/fixtures/witness-dangling-row.md
8ac9e82bae369a2e41f4a4377016c3e82d58c8c6de484722f1d85b0bbf7cb4af  .ufo/waves/round-39/fixtures/witness-summary-only-live.txt
fc95dc69153f47c2f934a0e9be069764a9da7b606dc0274ffd0f5672f3bd4623  .ufo/waves/round-39/fixtures/witness-comment-anchors.md
```

## Direct byte comparisons

Each command printed `MATCH` and exited successfully:

- `cmp -s .ufo/waves/round-40/fixtures/witness-token-entry.md .ufo/waves/round-39/fixtures/witness-token-entry.md && printf 'MATCH\n'` → `MATCH`
- `cmp -s .ufo/waves/round-40/fixtures/witness-dangling-row.md .ufo/waves/round-39/fixtures/witness-dangling-row.md && printf 'MATCH\n'` → `MATCH`
- `cmp -s .ufo/waves/round-40/fixtures/witness-summary-only-live.txt .ufo/waves/round-39/fixtures/witness-summary-only-live.txt && printf 'MATCH\n'` → `MATCH`
- `cmp -s .ufo/waves/round-40/fixtures/witness-comment-anchors.md .ufo/waves/round-39/fixtures/witness-comment-anchors.md && printf 'MATCH\n'` → `MATCH`

**Result:** all four round-40 witness files are byte-identical to their round-39 counterparts.

**Path note:** the delivered assignment/spec contained no literal `Report:` trailer filename. This report uses the declared `reportDir` `.ufo/waves/round-40/w1/` plus this seat's name (`ExeWitnessBytes.md`).