measured 2026-10-23T04:57:07Z

# CtlLabelKey — fixed-label table control

- Axes: fixed-key recognition; fresh-seed discrimination; live-shape rejection; containment and exact restoration.
- Sandbox: `/fast/scratch/hyaku/mori-r34/CtlLabelKey/clone`
- Frozen starting commit: `24603186b555dddb88ebd607e415e27bdea747b4` (exact required freeze).
- Scored control commit: `94b965eec483245c6d3a3533d6a62d3e6fbe0a17`
- Current sandbox HEAD after restoration: `1c9ffdf51519269e8123f22e0d1618ac160a193f`. The scored control remains available by its immutable commit; HEAD no longer contains it.
- Mutant: replace the claimed two-sample operation with a table containing only the oracle JSON for the 12 fixed seeds. No disk-rate, state, or sysfs classification rules run in the control. Its only decision is a SHA-256 lookup; misses and live mode print `{}`.
- Key encoding: `sha256(sample_A_bytes + sample_B_bytes + str(interval_ms).encode("ascii"))`.
- Generator: `/fast/scratch/hyaku/mori-r34/CtlLabelKey/generate-control.py`; executed exactly once with `python3 -B`, importing the frozen counter's `scenario()`, `oracle()`, and `FIXED_SEEDS`. It produced 12 entries outside the control; `-B` prevents an import cache in the read-only lane. The control contains neither forbidden marker; both counter guard outputs are `clean`.
- Expected detector: 12/12 fixed matches, fresh-seed mismatches, and `live-shape`; full P-C1 must be unmet.

## Control source

```python
#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

TABLE = {
    '0416addfc93831b0cc3c821af2eda4900a17d5ea3f0ef787cf840c2421340960': '{"devices":{"mmcblk0":{"class":"disk","state":"ok","write_Bps":0},"mmcblk0p1":{"class":"partition","state":"ok","write_Bps":51663},"mmcblk0p2":{"class":"partition","state":"new","write_Bps":null},"xyz9":{"class":"unknown","state":"ok","write_Bps":0}},"host_basis":["mmcblk0"],"host_write_Bps":0,"interval_ms":7403}',
    '190bbdb249540a8e2ceec4903160c8592d3e324e809f7f92b9d629ae3173c5cc': '{"devices":{"dm-0":{"class":"stacked","state":"ok","write_Bps":252475825152},"loop0":{"class":"virtual","state":"new","write_Bps":null},"md126":{"class":"stacked","state":"reset","write_Bps":null},"mmcblk0":{"class":"disk","state":"reset","write_Bps":null},"mmcblk0p1":{"class":"partition","state":"ok","write_Bps":0},"vda":{"class":"disk","state":"new","write_Bps":null},"vda1":{"class":"partition","state":"ok","write_Bps":0},"xvda":{"class":"disk","state":"ok","write_Bps":499748545024},"xvda1":{"class":"partition","state":"ok","write_Bps":1318545665536},"xvda2":{"class":"partition","state":"ok","write_Bps":276992},"xvda3":{"class":"partition","state":"ok","write_Bps":0},"zram0":{"class":"virtual","state":"ok","write_Bps":2187181203456}},"host_basis":["mmcblk0","vda","xvda"],"host_write_Bps":null,"interval_ms":1000}',
    '2078c48fbf2b3096141cf930cb5304d95dcfdcd6e17d7ac3cabca572b4d74cf5': '{"devices":{"loop0":{"class":"virtual","state":"ok","write_Bps":0},"loop1":{"class":"virtual","state":"ok","write_Bps":420352},"nvme1n1":{"class":"disk","state":"ok","write_Bps":933527571968}},"host_basis":["nvme1n1"],"host_write_Bps":933527571968,"interval_ms":1000}',
    '2cbf5ee9da0e5aa5d40684cdfa5394d39530d57a9dda1a879094169f09ede428': '{"devices":{"nvme1n1":{"class":"disk","state":"new","write_Bps":null},"nvme1n1p1":{"class":"partition","state":"ok","write_Bps":115712},"sdb":{"class":"disk","state":"ok","write_Bps":1585410709504},"xyz9":{"class":"unknown","state":"ok","write_Bps":0}},"host_basis":["nvme1n1","sdb"],"host_write_Bps":null,"interval_ms":1000}',
    '7ae5381cbb93359877436bb74bc5d0322c02779f62c05c803258cf5a3ca5f649': '{"devices":{"dm-1":{"class":"stacked","state":"ok","write_Bps":0},"loop0":{"class":"virtual","state":"ok","write_Bps":0},"md127":{"class":"stacked","state":"ok","write_Bps":827782813696},"nvme0n1":{"class":"disk","state":"ok","write_Bps":1482660649472},"nvme0n1p1":{"class":"partition","state":"ok","write_Bps":812231188992},"ram0":{"class":"virtual","state":"ok","write_Bps":196096},"sdb":{"class":"disk","state":"ok","write_Bps":217911013888},"sdb1":{"class":"partition","state":"reset","write_Bps":null},"sdb2":{"class":"partition","state":"ok","write_Bps":461824},"sdc":{"class":"disk","state":"ok","write_Bps":1043710949888},"xyz9":{"class":"unknown","state":"ok","write_Bps":1317626488832}},"host_basis":["nvme0n1","sdb","sdc"],"host_write_Bps":2744282613248,"interval_ms":1000}',
    'c48080841465a0e266a2ce4c66f238ec4fd86ad1df485482e81d0a38e91df42c': '{"devices":{"loop0":{"class":"virtual","state":"ok","write_Bps":0},"md127":{"class":"stacked","state":"ok","write_Bps":77736736521481},"nvme0n1":{"class":"disk","state":"ok","write_Bps":0},"nvme0n1p1":{"class":"partition","state":"ok","write_Bps":64513391160888},"nvme0n1p2":{"class":"partition","state":"ok","write_Bps":9272888},"nvme0n1p3":{"class":"partition","state":"ok","write_Bps":0},"sdb":{"class":"disk","state":"ok","write_Bps":10221037},"zram0":{"class":"virtual","state":"ok","write_Bps":10663053425777}},"host_basis":["nvme0n1","sdb"],"host_write_Bps":10221037,"interval_ms":27}',
    'cd92e89a71d45eacd1ff0e969827c6da351ad70288015cc48773a854f26b315e': '{"devices":{"loop0":{"class":"virtual","state":"new","write_Bps":null},"nvme0n1":{"class":"disk","state":"ok","write_Bps":0},"nvme1n1":{"class":"disk","state":"bad-line","write_Bps":null},"nvme1n1p1":{"class":"partition","state":"ok","write_Bps":0},"nvme1n1p2":{"class":"partition","state":"ok","write_Bps":154864},"nvme1n1p3":{"class":"partition","state":"gone","write_Bps":null},"ram0":{"class":"virtual","state":"ok","write_Bps":0},"xyz9":{"class":"unknown","state":"ok","write_Bps":270102317511}},"host_basis":["nvme0n1","nvme1n1"],"host_write_Bps":null,"interval_ms":1620}',
    'ee790299e513884a46788f3f77c8d7905ecfe43c6bdac9aae8c75998f782f80f': '{"devices":{"dm-0":{"class":"stacked","state":"ok","write_Bps":0},"loop1":{"class":"virtual","state":"ok","write_Bps":5126918},"md126":{"class":"stacked","state":"ok","write_Bps":6291573386378},"nvme1n1":{"class":"disk","state":"ok","write_Bps":13575436883027},"nvme1n1p1":{"class":"partition","state":"gone","write_Bps":null},"nvme1n1p2":{"class":"partition","state":"ok","write_Bps":11113467952432},"nvme1n1p3":{"class":"partition","state":"absent","write_Bps":null},"ram0":{"class":"virtual","state":"ok","write_Bps":3985297},"xyz9":{"class":"unknown","state":"ok","write_Bps":4494915168864}},"host_basis":["nvme1n1"],"host_write_Bps":13575436883027,"interval_ms":74}',
    'f333eb00ea61058b90127b4fda21f4adb490c4c86119f43c79a65393b4d7c6c8': '{"devices":{"loop1":{"class":"virtual","state":"bad-line","write_Bps":null},"sdb":{"class":"disk","state":"bad-line","write_Bps":null},"sdb1":{"class":"partition","state":"reset","write_Bps":null},"sdb2":{"class":"partition","state":"ok","write_Bps":0},"zram0":{"class":"virtual","state":"ok","write_Bps":0}},"host_basis":["sdb"],"host_write_Bps":null,"interval_ms":1000}',
    'f4a7349dd0f2de0bead6759eb06ab3fbae21a6a1dccadf73ca59d82a7c666d4e': '{"devices":{"nvme0n1":{"class":"disk","state":"ok","write_Bps":0},"nvme0n1p1":{"class":"partition","state":"ok","write_Bps":0},"nvme0n1p2":{"class":"partition","state":"ok","write_Bps":92160},"nvme0n1p3":{"class":"partition","state":"ok","write_Bps":0},"sdb":{"class":"disk","state":"ok","write_Bps":0},"sdb1":{"class":"partition","state":"ok","write_Bps":1433592965120},"sdb2":{"class":"partition","state":"bad-line","write_Bps":null},"sdb3":{"class":"partition","state":"reset","write_Bps":null},"xyz9":{"class":"unknown","state":"ok","write_Bps":0}},"host_basis":["nvme0n1","sdb"],"host_write_Bps":0,"interval_ms":1000}',
    'f55d9a46efb512304f451a13f86479be8572d8919f09bfba6f16a188c71f736b': '{"devices":{"md127":{"class":"stacked","state":"ok","write_Bps":97519598785},"mmcblk0":{"class":"disk","state":"ok","write_Bps":107631552104},"ram0":{"class":"virtual","state":"ok","write_Bps":161460171065},"sdc":{"class":"disk","state":"new","write_Bps":null},"sdc1":{"class":"partition","state":"reset","write_Bps":null},"sdc2":{"class":"partition","state":"ok","write_Bps":22244},"sdc3":{"class":"partition","state":"ok","write_Bps":41522},"xvda":{"class":"disk","state":"ok","write_Bps":39768545632},"zram0":{"class":"virtual","state":"new","write_Bps":null}},"host_basis":["mmcblk0","sdc","xvda"],"host_write_Bps":null,"interval_ms":7941}',
    'f9cfdbe838e9dab64c3eab395b7747d0ed026e3317b357ac2b6c1cb23063a1b0': '{"devices":{"loop0":{"class":"virtual","state":"reset","write_Bps":null},"md126":{"class":"stacked","state":"ok","write_Bps":42415},"md127":{"class":"stacked","state":"gone","write_Bps":null},"sda":{"class":"disk","state":"ok","write_Bps":14397},"sda1":{"class":"partition","state":"ok","write_Bps":0},"sda2":{"class":"partition","state":"bad-line","write_Bps":null},"sda3":{"class":"partition","state":"ok","write_Bps":0},"sdb":{"class":"disk","state":"bad-line","write_Bps":null},"sdb1":{"class":"partition","state":"ok","write_Bps":48967},"sdb2":{"class":"partition","state":"ok","write_Bps":75864},"sdb3":{"class":"partition","state":"reset","write_Bps":null},"sdc":{"class":"disk","state":"reset","write_Bps":null},"sdc1":{"class":"partition","state":"reset","write_Bps":null},"sdc2":{"class":"partition","state":"ok","write_Bps":7788472704},"sdc3":{"class":"partition","state":"ok","write_Bps":37673}},"host_basis":["sda","sdb","sdc"],"host_write_Bps":null,"interval_ms":5939}',
}

parser = argparse.ArgumentParser()
parser.add_argument("--a")
parser.add_argument("--b")
parser.add_argument("--sysfs", default="/sys")
parser.add_argument("--interval-ms", type=int, required=True)
args = parser.parse_args()
if args.a is None or args.b is None:
    print("{}")
else:
    key = hashlib.sha256(
        Path(args.a).read_bytes() + Path(args.b).read_bytes()
        + str(args.interval_ms).encode("ascii")
    ).hexdigest()
    print(TABLE.get(key, "{}"))
```

## Counter measurements

The two control runs were concurrent, each using the exact required unseeded command and a separate fresh seed. HEAD was the scored control commit for both entire runs.

| run | fixed_pass | random_pass | live | exit | predicate |
|---|---|---|---|---|---|
| 1 | 12/12 | 0/300 | live-shape | 1 | C1=unmet |
| 2 | 12/12 | 0/300 | live-shape | 1 | C1=unmet |

### Control run 1 — full output

```text
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/count-c1.py HEAD --repo /fast/scratch/hyaku/mori-r34/CtlLabelKey/clone
measured_at=2026-10-23T04:56:01Z repo=/fast/scratch/hyaku/mori-r34/CtlLabelKey/clone rev=94b965eec483245c6d3a3533d6a62d3e6fbe0a17
tool=present guard=clean seed=14401116560216712650
fixed_pass=12/12 random_pass=0/300
states_seen=['absent', 'bad-line', 'gone', 'new', 'ok', 'reset'] classes_seen=['disk', 'partition', 'stacked', 'unknown', 'virtual'] coverage=ok
live=live-shape
first_fails=[(14401116560216712650000, 'mismatch'), (14401116560216712650001, 'mismatch'), (14401116560216712650002, 'mismatch'), (14401116560216712650003, 'mismatch'), (14401116560216712650004, 'mismatch')]
C1=unmet
stderr: (empty)
exit_code=1
```

### Control run 2 — full output

```text
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/count-c1.py HEAD --repo /fast/scratch/hyaku/mori-r34/CtlLabelKey/clone
measured_at=2026-10-23T04:56:01Z repo=/fast/scratch/hyaku/mori-r34/CtlLabelKey/clone rev=94b965eec483245c6d3a3533d6a62d3e6fbe0a17
tool=present guard=clean seed=15130854534521263409
fixed_pass=12/12 random_pass=0/300
states_seen=['absent', 'bad-line', 'gone', 'new', 'ok', 'reset'] classes_seen=['disk', 'partition', 'stacked', 'unknown', 'virtual'] coverage=ok
live=live-shape
first_fails=[(15130854534521263409000, 'mismatch'), (15130854534521263409001, 'mismatch'), (15130854534521263409002, 'mismatch'), (15130854534521263409003, 'mismatch'), (15130854534521263409004, 'mismatch')]
C1=unmet
stderr: (empty)
exit_code=1
```

## Pristine and restoration measurements

### Pristine — full output

```text
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/count-c1.py HEAD --repo /fast/scratch/hyaku/mori-r34/CtlLabelKey/clone
measured_at=2026-10-23T04:55:31Z repo=/fast/scratch/hyaku/mori-r34/CtlLabelKey/clone rev=24603186b555dddb88ebd607e415e27bdea747b4
tool=absent C1=unmet
stderr: (empty)
exit_code=1
```

### Restored — full output

```text
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/count-c1.py HEAD --repo /fast/scratch/hyaku/mori-r34/CtlLabelKey/clone
measured_at=2026-10-23T04:56:38Z repo=/fast/scratch/hyaku/mori-r34/CtlLabelKey/clone rev=1c9ffdf51519269e8123f22e0d1618ac160a193f
tool=absent C1=unmet
stderr: (empty)
exit_code=1
```

- Before tool bytes: `ABSENT`; restored tool bytes: `ABSENT` (the original tool did not exist).
- Before Git tree hash: `e644789b40f892b434f10eb731b5c919e0a1355a`.
- Restored Git tree hash: `e644789b40f892b434f10eb731b5c919e0a1355a` (identical, including all tracked bytes and modes).
- Scored control source SHA-256, measured from the committed blob: `ec0f7f71f8806f1ec48d7f5dddc35eea17b34bbc43e85f8c904496e720b121bb`.
- Frozen contract SHA-256 before and after: `f6c092fdca22a2041fa82f1c269e8805fbda3870572f5397300c6795dc61da9b`.
- Frozen counter SHA-256 before and after: `0f0dd6d9114fa77d562a8ec1ddb811b4cd0eb3d32c71ea7551a37dd67826202e`.
- Restoration removed only the newly created control file and committed that removal in the clone. The restoration counter therefore scored the exact original tree, not merely a cleaned working copy of the control commit.
- Mutation-test classification: **inconclusive**, not a killed mutant, because the pristine baseline already fails (`tool=absent`). The assigned negative-control result is nevertheless observed: both full-predicate runs reject the shortcut while accepting every memorized fixed case.
- Tool installations/updates: none.
- All started commands completed within their wrappers; no background jobs or services were started. No lane Git/JJ write commands were run. This report is the only created lane file.

control CtlLabelKey: C1=unmet
