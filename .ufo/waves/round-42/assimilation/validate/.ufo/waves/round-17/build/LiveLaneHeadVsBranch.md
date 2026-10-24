# LiveLaneHeadVsBranch — lanes: HEAD vs `refs/heads/<branch>` (round 17, wave 1, advice)

Read-only census of every LANES row in `/home/vgpnk/Projects/shokunin/shokunin.conf`
(23 rows). Snapshot `2026-10-20T15:58:39-03:00`; `git version 2.56.0`; every git call under
`GIT_OPTIONAL_LOCKS=0`; **no `jj` command was run**; no writes outside this file; no `/tmp`.

Axes walked: (a) HEAD/branch identity coherence per lane row, (b) branch-resolution path the C2
probes must survive, (c) count of commits whose committer is the lane identity while the author
differs (the `LANE_AUTHOR_MISMATCH` predicate of `contract.md` C2).

Branch rule applied per row: `git symbolic-ref -q --short HEAD`, else
`git symbolic-ref -q --short refs/remotes/origin/HEAD` (strip `origin/`), else unique of
`refs/heads/master` / `refs/heads/main`.

## Table — per lane row

| lane | repo (rel. to fleet root) | `rev-parse HEAD` | branch | branch src | `refs/heads/<branch>` tip | `merge-base --is-ancestor HEAD <branch>` rc | committer=lane & author≠lane, last 30 branch commits |
|---|---|---|---|---|---|---|---|
| protocol | `.` | 9c32569848d9c42a9a159664328dc7056af95ba1 | master | symbolic-ref | 9c32569848d9c42a9a159664328dc7056af95ba1 | 0 | 0 |
| aggregator | `.` | 9c32569848d9c42a9a159664328dc7056af95ba1 | master | symbolic-ref | 9c32569848d9c42a9a159664328dc7056af95ba1 | 0 | 0 |
| kaidoku | `kaidoku-shokunin` | a1140e76fffdc1be032d9d813dbb686157803bbc | main | origin/HEAD | a1140e76fffdc1be032d9d813dbb686157803bbc | 0 | 0 |
| kasegi | `kasegi-shokunin` | 922a4dde90b60b465e2b8b241d1fe363f1f27e98 | master | symbolic-ref | 922a4dde90b60b465e2b8b241d1fe363f1f27e98 | 0 | 0 |
| kengaku | `kengaku-shokunin` | 6180e4fb92e90c0b172e9788e2c765d097f2e142 | master | symbolic-ref | 6180e4fb92e90c0b172e9788e2c765d097f2e142 | 0 | **1** |
| kake | `kake-shokunin` | 7c61c8cc791bde36dd5e3688bdfea2678d90146c | master | symbolic-ref | 7c61c8cc791bde36dd5e3688bdfea2678d90146c | 0 | 0 |
| kumitate | `kumitate-shokunin` | 1770305fae20826b39905a8251ddeca6b4957ac4 | master | symbolic-ref | 1770305fae20826b39905a8251ddeca6b4957ac4 | 0 | 0 |
| kotoba | `kotoba-shokunin` | c61a973b2e02e1ded169703ddcb06466f4edd8bd | master | symbolic-ref | c61a973b2e02e1ded169703ddcb06466f4edd8bd | 0 | 0 |
| kagi | `kagi-shokunin` | c2cab35bc92e57e39e5489bac3386db078345b3f | master | symbolic-ref | c2cab35bc92e57e39e5489bac3386db078345b3f | 0 | 0 |
| kama | `kama-shokunin` | 54a29268e2083caa2b1e0d54ee1e7d90961302f3 | master | origin/HEAD | 54a29268e2083caa2b1e0d54ee1e7d90961302f3 | 0 | 0 |
| lore | `lore-shokunin` | 01306d51252f837909af5252c398ee4e31259f9b | main | symbolic-ref | 01306d51252f837909af5252c398ee4e31259f9b | 0 | 0 |
| revenger | `revenger-shokunin` | cf02419276e5dd8aafb6fe09d4e9aaa6bcb78c97 | main | symbolic-ref | cf02419276e5dd8aafb6fe09d4e9aaa6bcb78c97 | 0 | 0 |
| tameshi | `tameshi-shokunin` | e3827ee67d58673e1e9a1141ba1c8333125f4de8 | master | origin/HEAD | e3827ee67d58673e1e9a1141ba1c8333125f4de8 | 0 | 0 |
| mado | `mado-shokunin` | 7b4839d31d60af5bac40e3e74aec70e928601dfc | master | origin/HEAD | 7b4839d31d60af5bac40e3e74aec70e928601dfc | 0 | 0 |
| tsukuroi | `tsukuroi-shokunin` | 842a5312b704b5cda10fd80ec1fdee5fb381ba97 | master | origin/HEAD | 842a5312b704b5cda10fd80ec1fdee5fb381ba97 | 0 | 0 |
| tabi | `tabi-shokunin` | 2bff864fdfee684ddbcd066cc8e735adaba2735c | master | origin/HEAD | 2bff864fdfee684ddbcd066cc8e735adaba2735c | 0 | 0 |
| mori | `mori-shokunin` | 24526ea9617cd020fee16c28fe4d4a2789dc28cb | master | symbolic-ref | 24526ea9617cd020fee16c28fe4d4a2789dc28cb | 0 | 0 |
| chousa | `chousa-shokunin` | d730ae4c33989ad9c8535764d4cae77b4db869f6 | master | symbolic-ref | d730ae4c33989ad9c8535764d4cae77b4db869f6 | 0 | 0 |
| kotodama | `kotodama-shokunin` | 4ad26836552462d28a946ca3b067cab0b5ce3532 | main | symbolic-ref | 4ad26836552462d28a946ca3b067cab0b5ce3532 | 0 | 0 |
| souji | `souji-shokunin` | 4f4834390ad4845b76804e94cc04d8f867ef9b54 | master | origin/HEAD | 4f4834390ad4845b76804e94cc04d8f867ef9b54 | 0 | 0 |
| audio | `audio-shokunin` | 0462a5440f23f45707ba681e2a011940e3c923dd | main | symbolic-ref | 0462a5440f23f45707ba681e2a011940e3c923dd | 0 | 0 |
| game-dev-2d | `game-dev-2d-shokunin` | bce53b83a21ea43ddc2bf050bfe78cb4f2b68550 | main | symbolic-ref | bce53b83a21ea43ddc2bf050bfe78cb4f2b68550 | 0 | 0 |
| game-dev-3d | `game-dev-3d-shokunin` | 3118be0b18dd7351b1faf6ce99d26a34370793ec | main | symbolic-ref | 3118be0b18dd7351b1faf6ce99d26a34370793ec | 0 | 0 |

Row totals: 23 rows / 22 distinct repos (protocol and aggregator both resolve to the fleet root).
`HEAD == refs/heads/<branch>` tip: **true for all 23 rows**. Ancestor rc 0: **all 23**.
Branch-source distribution: symbolic-ref **16**, origin/HEAD **7**, master/main fallback **0**.
`refs/heads/<branch>` == `refs/remotes/origin/<branch>` and ahead/behind `0 0`: **all rows**.

## Exception detail (the only non-zero identity cell)

`kengaku` tip `6180e4fb92e90c0b172e9788e2c765d097f2e142` (subject `Integrate remote
documentation; preserve local round log`):

- author `protocol-shokunin <protocol@shokunin.local>`
- committer `kengaku-shokunin <kengaku@shokunin.local>`
- committer date `2026-10-19T22:05:18-03:00`

Kengaku's last launch anchor in `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` is
`2026-10-15T01:50:57-03:00 launch kengaku round=13` (last of 35 kengaku lines; no later kengaku
launch line exists), so this commit is strictly post-launch and the contract's
`LANE_AUTHOR_MISMATCH` predicate selects exactly this one commit fleet-wide.
No commit in any row's window has a partial identity diff (same name/different email or
converse); name-only vs name+email comparison is indistinguishable on this data.

## Observed facts (direct commands, high confidence)

1. The fleet is moving during the probe. Two earlier snapshots in the same session returned
   different tips, each an advance: root `bb44c290…` → `9c325698…`, kaidoku `85589ac7…` →
   `a1140e76…`, mado `c7693eb2…` → `7b4839d3…`, souji `d7e648d5…` → `4f483439…`, tameshi
   `0ff2734…` → `e3827ee6…`. Every re-read kept `HEAD == tip`, ancestor rc 0, ahead/behind 0 0.
2. 8 lane repos carry `.jj`: kaidoku, kama, tameshi, mado, tsukuroi, tabi, mori, souji. 7 of
   them have **detached HEAD** (`symbolic-ref -q HEAD` rc1, `rev-parse --abbrev-ref HEAD` =
   `HEAD`); those 7 are exactly the rows resolved via `origin/HEAD`. `mori` is jj-colocated
   **with an attached HEAD** (`refs/heads/master`), so jj-colocation does not imply detachment.
3. `git config --get lane.branch` exists in only 5 repos (kaidoku=`main`,
   mado/tsukuroi/tabi/mori=`master`) and is absent in the other 17, including kama, tameshi and
   souji which do have `.jj`. The repo binding cannot be the census's branch source; the
   contract's symbolic-ref → origin/HEAD → unique master/main chain is the only universal one.
4. `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh:115` `detect_branch` has **no**
   master/main fallback (it returns rc1 after the origin/HEAD branch); that fallback lives in
   the caller at `jj-lane.sh:162-168`. The census implementation must therefore add the
   fallback itself, not delegate the contract's full rule to `detect_branch`.
5. `jj-lane.sh:404` guards init with `HEAD is detached on a non-tip commit` — i.e. the
   helper's own model is that detached HEAD must equal `refs/heads/<branch>` at init time.
6. The C2 row-6 disclosure string at `tools/mori-census.sh:2276` still prints
   `cat-file -e HEAD:...`; a branch cutover that updates only `:2100` and `:2102` would leave
   the census misdescribing its own probe.
7. Reverse direction (author is the lane, committer differs): 9 lanes carry exactly one commit
   authored `<lane>-shokunin` but committed by
   `Devin AI <158243242+devin-ai-integration[bot]@users.noreply.github.com>`, all dated
   `2026-10-17T15:52Z` (kasegi, kengaku, kake, kumitate, kagi, mori, audio, game-dev-2d,
   game-dev-3d). The contract's committer-is-lane predicate excludes these by construction;
   including them would add 9 fleet-wide false positives.

## Inference (not directly observed)

- **[INFERENCE]** In jj colocation the working-copy commit `@` is what git `HEAD` names, and it
  is normally a *child* of the exported bookmark commit that `refs/heads/<branch>` names.
  Therefore `merge-base --is-ancestor HEAD refs/heads/<branch>` fails during ordinary
  in-progress jj work, so `HEAD_BRANCH_MISMATCH` will fire on normal work (HEAD ahead of
  branch), not only on genuine drift. Evidence cut: at this quiesced snapshot all 7 detached
  lanes have HEAD == tip, so no live instance exists either way; the contract's documented
  gate must synthesize both directions in its own sandboxes.
- **[INFERENCE]** Row-6's `HEAD:<path>` → `refs/heads/<branch>:<path>` cutover is behavior
  neutral on today's fleet (identical commit objects in all 23 rows) and becomes
  behavior-bearing only for unexported working-copy commits in jj lanes.

## Remaining unknowns

- No real `HEAD_BRANCH_MISMATCH` instance exists on the fleet to falsify the new finding; every
  row is branch-anchored at snapshot. Real-lane probes cannot test it — only synthetic
  sandboxes can.
- The master/main fallback path has zero live coverage (0 of 23 rows); its correctness must be
  established by the C2 regression sandboxes.
- I did not run `tools/mori-census.sh`, so kengaku's actual `LA_ROUND`/anchor used by the
  census is inferred from the watchdog log (round 13) rather than observed from a run.
- Whether any jj lane ever holds an unexported working-copy commit (HEAD ≠ branch tip) could
  not be observed without running jj or catching such a moment; three probes each saw equality.

## Command inventory (all read-only, `GIT_OPTIONAL_LOCKS=0`)

- `git -C <repo> rev-parse --verify --quiet HEAD` — 23/23 rc 0.
- `git -C <repo> symbolic-ref -q --short HEAD` — 16 rc 0; 7 rc 1 (detached).
- `git -C <repo> symbolic-ref -q --short refs/remotes/origin/HEAD` — 7/7 rc 0 for the detached set.
- `git -C <repo> rev-parse --verify --quiet refs/heads/<branch>` — 23/23 rc 0.
- `git -C <repo> merge-base --is-ancestor HEAD refs/heads/<branch>` — 23/23 rc 0.
- `git -C <repo> log -30 --format='%cn%x00%ce%x00%an%x00%ae' refs/heads/<branch>` — 23/23 rc 0;
  30 commits returned for every row.
- `git -C <repo> rev-list --left-right --count refs/heads/<branch>...refs/remotes/origin/<branch>` —
  23/23 rc 0, `0 0`.
- `git -C <repo> config --get lane.branch` — 5 rc 0, 18 rc 1.
- `test -d <repo>/.jj` — 8 present.
- `git --version` — rc 0, `2.56.0` (census comments at `tools/mori-census.sh` cite measurements
  on 2.55.0; `--since` inclusivity is version-sensitive, so pin/record the version when running
  the gate).
- Read-only file reads: `shokunin.conf`, `.ufo/waves/round-17/contract.md`,
  `.ufo/waves/round-17/wave1-context.txt`, `tools/mori-census.sh` (`:2100`, `:2102`, `:2197`,
  `:2200`, `:2276`), `scripts/hyaku/jj-lane.sh` (`:85`, `:115`, `:162`, `:404`),
  `.ufo/watchdog.log` (kengaku launch lines only).

No tool installs or upgrades were performed.
