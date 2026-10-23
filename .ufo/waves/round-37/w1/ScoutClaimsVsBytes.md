# ScoutClaimsVsBytes — claim → file:line at e57c58b

Attack: do C1's challenge arm and per-id grammar, and C2's two named arms plus the two fetch-policy lines, exist as bytes at `e57c58b57c025364e79d130fbdf764d2674d83d6`?

Worktree HEAD is `c31076ed85b3aadf2454637747343e0ab97eb58f` (later). Every line below is from `git show <rev>:<path> | nl -ba`, cross-checked with `git grep -n` on that commit. Not the worktree.

Tools installed: none.

## Pins (observed)

```
git rev-parse --verify e57c58b57c025364e79d130fbdf764d2674d83d6^{commit}
→ e57c58b57c025364e79d130fbdf764d2674d83d6

git rev-parse e57c58b57c025364e79d130fbdf764d2674d83d6:.ufo/waves/round-37/count-c1.py
→ 7518fef8f54afff69ee38a99f2acbf518006f5ad
git rev-parse e57c58b57c025364e79d130fbdf764d2674d83d6:.ufo/waves/round-37/count-c2.py
→ 6213cf9a5ada709da8cd867581782737b2f06c71
git rev-parse e57c58b57c025364e79d130fbdf764d2674d83d6:tools/mori-source-drift.py
→ 162ee87b5b0789c6815f967f3db93d277bab38d9
```

Those three blobs are the freeze pins in `e57c58b:.ufo/waves/round-37/evidence/freeze-r37.txt` (lines for `count-c1.py`, `count-c2.py`, `tools/mori-source-drift.py`). `wc -l` on the shown blobs: count-c1.py 960, count-c2.py 225, mori-source-drift.py 466.

## Map

| Claim element | Bytes | file:line at e57c58b |
|---|---|---|
| C1 id grammar (`changed` / `deleted`) | `ID_CHANGED_RE`, `ID_DELETED_RE` | `.ufo/waves/round-37/count-c1.py:540-541` |
| C1 id-line parser | `parse_id_lines` | same file `:544-563` |
| C1 id-line predicate | `same_id_lines` (malformed==0, sorted ids, sorted deleted, no duplicates) | same file `:566-572` |
| C1 grammar enforced on blind | `parse_id_lines` then `same_id_lines` | `:690`, `:703` |
| C1 grammar enforced on real | same | `:731`, `:734`, `:747` |
| C1 grammar enforced on challenge | same | `:773`, `:782` |
| C1 challenge clothing | `CHALLENGE_PARENT`, `LANE_TITLE`, `LANE_IDENTITY` | `:56`, `:288-289` |
| C1 challenge arm | `challenge_arm`: `mkdtemp` under the lane scratch, even index (forced deletion), lane identity + title, truth from the op log | `:754-791` (`:765-770` deletion witness) |
| C1 challenge judged | `run_negative` calls `challenge_arm`; main scores it; `met` requires it | `:799`, `:921-928`, `:949` |
| C2 policy: 4 MiB bounded read | `FETCH_MAX_BYTES = 4 * 1024 * 1024` | `tools/mori-source-drift.py:54` |
| C2 policy applied | `resp.read(FETCH_MAX_BYTES + 1)` then over-cap → `unavailable` | `:163-165` |
| C2 policy: post-redirect public destination | `def _public_redirect_target` | `:113-135` |
| C2 policy line the counter mutates | `if not _public_redirect_target(final):` | `:158` (refuse `:159`) |
| C2 arm `huge_cap` | over-cap body `4*1024*1024+64` at `:322`; literal at-cap body `:402-403`; check named `huge_cap` | `:401-411` |
| C2 arm `redirect_private_refused` | route `("redir", "/fresh")` `:323`; 302 `Location` `:277-279`; check named `redirect_private_refused` | `:412-416` |
| C2 counter names both anchors | `CAP_ANCHOR`, `REDIRECT_ANCHOR` | `.ufo/waves/round-37/count-c2.py:50-52` |
| C2 counter requires both arms PASS | `selftest` check | `:161-163` |
| C2 counter kills each policy | `cap_kill` replaces the cap; `redirect_kill` replaces the `if not` line | `:166-171`, `:173-180` |

Anchor uniqueness (so each mutation hits exactly one line):

```
git grep -n -F 'FETCH_MAX_BYTES = 4 * 1024 * 1024' e57c58b… -- tools/mori-source-drift.py
→ tools/mori-source-drift.py:54 only
git grep -n -F 'if not _public_redirect_target(final):' e57c58b… -- tools/mori-source-drift.py
→ tools/mori-source-drift.py:158 only
git grep -n -E 'def challenge_arm|def parse_id_lines|def same_id_lines' e57c58b… -- .ufo/waves/round-37/count-c1.py
→ :754, :544, :566
```

## Notes (not missing elements)

- `redirect_private_refused` does not embed a literal `http://127.0.0.1` Location. The fixture body is the relative path `"/fresh"` (`mori-source-drift.py:323`), sent as `Location` (`:279`). The request URL is `http://127.0.0.1:<port>/redir` (`:308`, `:412`). Refusal is still the policy at `:158` calling `_public_redirect_target` (`:113-127`, `addr.is_global`).
- `"/fresh" % {"port": 9}` on this interpreter returns `'/fresh'` (no `TypeError`). Observed: `python3 -c 'print(repr("/fresh" % {"port": 9}))'`.
- `evidence/c2-after.txt` is on disk and not in this commit (`git show e57c58b:.ufo/waves/round-37/evidence/c2-after.txt` → exists on disk, not in the commit). The policy and arm bytes above are in the commit; the receipt is not part of this map.

VERDICT: PASS
