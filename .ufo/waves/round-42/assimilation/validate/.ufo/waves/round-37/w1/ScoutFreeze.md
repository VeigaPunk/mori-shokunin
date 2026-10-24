# ScoutFreeze — post-freeze edits to the eight pinned paths

Item under attack: any commit in `842a320..e57c58b` (and any descendant of the freeze pin) that edits a path pinned in `.ufo/waves/round-37/evidence/freeze-r37.txt` after that pin.

Axes: (1) commit list per frozen path in the assigned range, (2) ancestry after the pin versus side refs, (3) tip blob equals the pin. No tool installs.

## Freeze pin

`evidence/freeze-r37.txt` is introduced by the only commit in the range. That commit is the freeze pin.

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-list 842a32074b5c7972e9728f3f629d83eb92f127c2..e57c58b57c025364e79d130fbdf764d2674d83d6
e57c58b57c025364e79d130fbdf764d2674d83d6

$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --format='%H %ci %s' 842a320..e57c58b57c025364e79d130fbdf764d2674d83d6 -- .ufo/waves/round-37/evidence/freeze-r37.txt
e57c58b57c025364e79d130fbdf764d2674d83d6 2026-10-23 16:58:19 -0300 round-37: freeze (contract, c1/c2 counters, negative fixtures) + data (drift hardening entry, S221-S225, capability rows, scoped r17-jj assertion)

$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse e57c58b57c025364e79d130fbdf764d2674d83d6^@
842a32074b5c7972e9728f3f629d83eb92f127c2
```

Parent is the entering tip. Range length is 1.

## Commit list per path

Command form: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --oneline 842a320..e57c58b57c025364e79d130fbdf764d2674d83d6 -- <path>`

| path | commits in range | name-status `842a320..e57c58b` |
|---|---|---|
| `.ufo/waves/round-37/contract.md` | `e57c58b` only | `A` (+98) |
| `.ufo/waves/round-37/count-c1.py` | `e57c58b` only | `A` (+960) |
| `.ufo/waves/round-37/count-c2.py` | `e57c58b` only | `A` (+225) |
| `.ufo/waves/round-37/fixtures/memo-n1.py` | `e57c58b` only | `A` (+41) |
| `.ufo/waves/round-37/fixtures/const.py` | `e57c58b` only | `A` (+24) |
| `.ufo/waves/round-37/fixtures/summary-only.py` | `e57c58b` only | `A` (+24) |
| `tools/mori-source-drift.py` | `e57c58b` only | `M` (+20/−0) |
| `tools/mori-sources-appendonly.py` | (none) | absent from the diff |

Observed `log --oneline` subject on the seven non-empty lists is the freeze subject above. The append-only log printed nothing.

`git diff --name-status 842a32074b5c7972e9728f3f629d83eb92f127c2 e57c58b57c025364e79d130fbdf764d2674d83d6 -- <eight paths>` listed the seven rows above and did not list `tools/mori-sources-appendonly.py`. Numstat for `tools/mori-source-drift.py` is `20 0`.

## After the pin

No descendant of the pin touches a frozen path. `git log --name-status e57c58b57c025364e79d130fbdf764d2674d83d6..HEAD -- <eight paths>` printed nothing. First-parent commits after the pin (`bcf65505`, `5dff52a1`, `52d636d5`, `4bec58eb`, `c31076ed`) are outside the assigned range and do not edit these paths.

HEAD (`c31076ed85b3aadf2454637747343e0ab97eb58f`) blobs equal the freeze pins and the `e57c58b` blobs:

```
61a768a37a00ea5b4a79fb6ec2dfece272c98b06  .ufo/waves/round-37/contract.md
7518fef8f54afff69ee38a99f2acbf518006f5ad  .ufo/waves/round-37/count-c1.py
6213cf9a5ada709da8cd867581782737b2f06c71  .ufo/waves/round-37/count-c2.py
19324701f23a225e5ded21c4785c491e7530ac7c  .ufo/waves/round-37/fixtures/memo-n1.py
2f3993a04906ce33033ab207a284d9ca7d7ff57a  .ufo/waves/round-37/fixtures/const.py
2d62f742fbef39634a5ff04e25b399b87ce4c941  .ufo/waves/round-37/fixtures/summary-only.py
162ee87b5b0789c6815f967f3db93d277bab38d9  tools/mori-source-drift.py
dfb5040b159f7a0b4afedc90a633d997352908f0  tools/mori-sources-appendonly.py
```

`tools/mori-sources-appendonly.py` is the same blob at `842a320` and at the pin (`dfb5040b…`). The other seven blobs at `e57c58b` match the pin file; at `842a320` the six round-37 paths are absent and `tools/mori-source-drift.py` is `d59eb2ed05` (not the pin).

`git log --all e57c58b..` does reach other commits that touch `tools/mori-source-drift.py` (and, for `3a68c320`, the six new round-37 paths). They are not after the pin: `merge-base --is-ancestor` is false both ways against `e57c58b` and against HEAD. The same-timestamp ones are `refs/jj/keep/38b16e06`, `refs/jj/keep/3a68c320`, `refs/jj/keep/babd3aa8` (parent `842a320`, empty subject, 2026-10-23 16:58:19 -0300). Older keeps and `origin/wip/operator-save-20261023` (`4ea7bd61`) are likewise not descendants of the pin. Not counted as post-freeze edits.

## Verdict

Only the freeze commit `e57c58b57c025364e79d130fbdf764d2674d83d6` touches a frozen path inside `842a320..e57c58b`. Nothing after that pin, through HEAD, changes those blobs. `tools/mori-sources-appendonly.py` is untouched in the range and still the pinned blob.

VERDICT: PASS
