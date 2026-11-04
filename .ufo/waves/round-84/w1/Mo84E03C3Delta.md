# Mo84E03C3Delta — round 84 w1 — C3 depth: per-token live-delta classification

Seat: executor (C3). Enter `5adf4337`, freeze `daa77bd5`, amendments applied up to A6 (`5a231ef8`).
Lane commit state at seat start: `39190f8` (A2), working tree clean for the edited file.

## Changed (absolute paths)

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-83/count-c2.py` — the only file
  edited (working tree; the L1 owns the lane commit). No other lane file touched. No tool
  installs or upgrades were needed (nothing to record under the 2026-10-19 tooling rule).
  1. `live_delta(snapshot_tokens, live_tokens, names, stated)` — pure module-level classifier
     (exact name/order per A6). Ordered `(token, class)` over the union: snapshot order first,
     then live-only tokens in live order; every token exactly once (duplicates collapse to first
     occurrence). Live class = `derive(token, names)`; snapshot class = the `stated` one
     (derived only as fallback for an unclassified token). Classes exactly `absent-live`,
     `added-live`, `agreed`, `class-changed:<snapshot>-><live>`.
  2. `grade()` computes the delta after `live_agree`: `union_n`, `absent_live`, `added_live`,
     `class_changed`, `deltas = absent+added+changed` (= union − agreed-class count). `met` adds
     exactly two conjuncts — `agreed == live_agree` and `union_n == len(set(tokens))` (every union
     token classified exactly once) — keeping every existing conjunct; no particular live token
     count is required. Tail extends with
     `delta=classified classified=<n> union=<n> absent_live=<n> added_live=<n> class_changed=<n>
     deltas=<n>` while keeping `tokens=`, `residual=`, `live=`, `live_tokens=`, `live_agree=`.
     Exactly one `LIVE_DELTA <token> <class>` note per non-agreed token, none for agreed.
  3. Four selftest arms over synthetic snapshot/live pairs, no census run: `delta_agreed`,
     `delta_absent_live`, `delta_added_live`, `delta_class_changed` (12 → 16 arms total).
  4. Docstring documents the P-C3 extension.
- A2 anchor preservation, verified count=1 each after the edit (and before): `and not
  unclassified`, `and residual == 0`, `agreed == len(snapshot_tokens)`, `residual += duplicates`,
  `duplicates == 0` (existing wrap kept; no conjunct merged or deleted; no arm has
  `residual`/`unclassified` non-zero with all other met conjuncts — the four new arms never call
  `met`).

## Commands and outputs

```
$ python3 -m py_compile .ufo/waves/round-83/count-c2.py
py_compile OK

$ for s in 'and not unclassified' 'and residual == 0' 'agreed == len(snapshot_tokens)' \
     'residual += duplicates' 'duplicates == 0'; do grep -cF -- "$s" <file>; done
1 1 1 1 1

$ python3 -I .ufo/waves/round-83/count-c2.py --selftest --scratch $S/st
PASS conformant … delta=classified classified=4 union=4 … deltas=0
PASS snapshot_absent … PASS hash_mismatch … PASS asof_mismatch … PASS unclassified_token …
PASS class_disagrees … class_changed=1 deltas=1
PASS green_live_unmet … absent_live=4 … deltas=4
PASS duplicate_line_residual … PASS retired_row_snapshot_required … PASS red_cell_keeps_unmet …
PASS duplicate_header_unmet … PASS foreign_snapshot_path_unmet …
PASS delta_agreed [('+SURFACE:lane.new', 'agreed'), ('fields', 'agreed')]
PASS delta_absent_live [('+audit', 'absent-live')]
PASS delta_added_live [('+VERDICT', 'added-live')]
PASS delta_class_changed [('fields', 'class-changed:added-since-r10->value-changed')]
C2_COUNTER_SELFTEST pass=16 fail=0
rc=0
```

Scratch probe flow (fixture clone; commits used `-c user.name=t -c user.email=t@t`;
`git -C "$D" rev-parse --show-toplevel` asserted equal to `$D` before the commit):

```
$ git clone --shared /home/vgpnk/Projects/shokunin/mori-shokunin $S/lane
$ cp <edited counter> $S/lane/.ufo/waves/round-83/count-c2.py && git -C $S/lane commit -qam …
PROBE=4311f8239793252bca354e257fe7166cda3ac18a

$ python3 -I .ufo/waves/round-84/count-c3.py $PROBE --repo $S/lane --scratch $S/c3
C3=unmet delta=classified tokens=64 classified=71 union=71 residual=0 live=derived \
  live_tokens=52 live_agree=45 deltas=26 arms=16 classifier=5/5 rev=4311f8239793
LIVE_DELTA +FINDING:ROSTER_SET_MISMATCH absent-live        (…19 absent-live lines…)
LIVE_DELTA +SURFACE:lane.audio absent-live … LIVE_DELTA obs absent-live
LIVE_DELTA +FINDING:WATCHDOG_LOG_UNAVAILABLE added-live    (…7 added-live lines…)
LIVE_DELTA +path added-live … LIVE_DELTA targets added-live
C2=unmet snapshot=bound asof=1 tokens=64 agreed=64 residual=0 live=derived live_tokens=52 \
  live_agree=45 delta=classified classified=71 union=71 absent_live=19 added_live=7 \
  class_changed=0 deltas=26 rev=4311f8239793
rc=1        (pre-A6 counter bytes: real 0m0.402s)
```

Same probe rev, real fleet root — the substrate the integration run will observe (read-only
census; run via the subject's own `--fleet-root` flag):

```
$ python3 -I $S/lane/.ufo/waves/round-83/count-c2.py $PROBE --repo $S/lane \
    --fleet-root /home/vgpnk/Projects/shokunin --scratch $S/c2real
C2=met snapshot=bound asof=1 tokens=64 agreed=64 residual=0 live=derived live_tokens=64 \
  live_agree=64 delta=classified classified=64 union=64 absent_live=0 added_live=0 \
  class_changed=0 deltas=0 rev=4311f8239793
rc=0        real 0m4.839s user 7.661s sys 3.814s
```

Falsifications (the counter is shown able to fail three ways):

```
$ python3 -I .ufo/waves/round-84/count-c3.py 5adf4337b6510dd246b247092c11cbaa97c930d3 \
    --repo $S/lane --scratch $S/c3n
C3=unmet delta=absent rev=5adf4337b651        rc=1

# mutant probe: live_delta's absent-live class word replaced by "agreed" in a fixture commit
MUT=0bef1d8367759516879f481bf1c6b186ad13cd81
$ python3 -I .ufo/waves/round-84/count-c3.py $MUT --repo $S/lane --scratch $S/c3m
C3=unmet delta=absent arms=15 selftest=red rc=1 rev=0bef1d836775
FAIL delta_absent_live [('+audit', 'agreed')]

$ python3 -I .ufo/waves/round-84/count-c3.py --selftest --scratch $S/c3st   # A6 counter bytes
C3_COUNTER_SELFTEST pass=11 fail=0        rc=0
```

## Live census numbers (requested by the item)

- Token count: live token line = **64** against the real fleet root (exactly the snapshot's 64;
  `tokens == recount == 64`), **52** against the scratch-clone substrate.
- Delta lines at the probe: 26 on the scratch substrate (19 `absent-live` + 7 `added-live`,
  listed in full above); **0** against the real fleet root (union=64, all agreed).
- Duration: whole C3 counter probe run 0.402 s real on the scratch substrate; subject grade incl.
  the live census of the real fleet 4.839 s real (user 7.661 s, sys 3.814 s).

## Verified / not verified

Verified: selftest pass=16 fail=0 with the four frozen delta arms PASS; A2's five anchors each
exactly once after the edit; the A6 counter accepts the bytes (`classifier=5/5`, `arms=16`,
arm labels present, `tokens == recount == 64` per the L1's measurement and my run's tail);
delta arithmetic exact in every observed case (`classified == union`, `deltas == union −
live_agree == number of LIVE_DELTA lines`, no token twice, class words frozen); the counter
fails on the entering revision, on a red subject selftest, and on a broken classifier word.

Not verified (honest stops): the prescribed scratch-clone flow cannot print `C3=met` — the
frozen counter resolves the census fleet root as `dirname(repo)` when the repo path ends
`-shokunin`, so a clone under `/fast/scratch/hyaku/...` points the live census at a near-empty
scratch dir and `agreed(64) == live_agree(45)` fails there (19 fleet-specific snapshot tokens
absent from that observation). The identical probe rev with the real fleet root reads
`C2=met … live_agree=64 … deltas=0` rc 0. This is a substrate property of the frozen counter's
fleet resolution, not a defect in the graded bytes; at integration (repo = the real lane
checkout) the census observes the real fleet and `C3=met` is the expected after-value. I did not
modify the frozen counter (outside my seat scope).

## Defects in other seats' bytes

None found.

## Cleanup

Scratch `/fast/scratch/hyaku/mori-r84/Mo84E03C3Delta/` (clone, mutants, counter scratch trees)
is removed after this report is written. Nothing written outside the edited file, this report,
and that scratch dir; no lane/OS/service/credential state changed; no commits in the lane repo.
