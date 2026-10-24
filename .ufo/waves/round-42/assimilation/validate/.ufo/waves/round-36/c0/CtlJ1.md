measured 2026-10-23T11:59:44Z
control J1 shape skip-work / do-nothing
control_sha256 da68bfbacefaa5d986c68f12b71ffe1ce9bf9515016a4f425119191505e5363f
counter_sha256 302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb

Axes: defect fidelity, CLI fidelity, detector discrimination, byte integrity.

Program: `.ufo/waves/round-36/c0/controls/J1.py:7-13` accepts the assigned positional revision and optional repo, round-base, and path arguments, performs no history inspection, prints the empty summary, and exits normally. This is the assigned J1 shape (`.ufo/waves/round-36/contract.md:62-77,90-92`). Expected detector: hidden-truth list comparison rejects the empty lists when truth is nonempty (`.ufo/waves/round-36/count-c2.py:590-621,624-641`).

Before scoring, command `timeout 120 sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py` returned:
```text
ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py
302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
```
Both match `.ufo/waves/round-36/evidence/freeze.txt:3-4` and the assigned frozen hashes.

Scored command, without --seed, cwd `/home/vgpnk/Projects/shokunin/mori-shokunin`:
```text
timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py 6bd57097 --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J1.py
```
Full counter output:
```text
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J1.py
blind arm: 0/24 sandbox histories matched the hidden truth (2.0s; coverage: deletions=22 changed-back=18 superseded=11)
  repo00 FAIL: lists differ
      want: appendonly_violations=3 ids=[S233] deleted=[S040,S056] superseded=[S233] round_changed=[S040,S122]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  repo01 FAIL: lists differ
      want: appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[S232]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  repo02 FAIL: lists differ
      want: appendonly_violations=4 ids=[] deleted=[S004,S057,S084,S148] superseded=[] round_changed=[S004,S057,S084,S148]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  repo03 FAIL: lists differ
      want: appendonly_violations=2 ids=[S276] deleted=[S258] superseded=[] round_changed=[S258,S276]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  repo04 FAIL: lists differ
      want: appendonly_violations=5 ids=[S001,S062,S250] deleted=[S039,S290] superseded=[S250] round_changed=[S001,S039,S299]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  repo05 FAIL: lists differ
      want: appendonly_violations=3 ids=[S056,S219] deleted=[S042] superseded=[S219] round_changed=[S056]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  repo06 FAIL: lists differ
      want: appendonly_violations=2 ids=[S139] deleted=[S028] superseded=[S139] round_changed=[S028]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  repo07 FAIL: lists differ
      want: appendonly_violations=5 ids=[S023,S187] deleted=[S061,S124,S129] superseded=[] round_changed=[S023,S061,S071,S124,S187]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  repo08 FAIL: lists differ
      want: appendonly_violations=2 ids=[S268] deleted=[S147] superseded=[S268] round_changed=[]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  repo09 FAIL: lists differ
      want: appendonly_violations=2 ids=[S227] deleted=[S181] superseded=[] round_changed=[S016,S181,S227,S260]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  repo10 FAIL: lists differ
      want: appendonly_violations=4 ids=[S116,S294] deleted=[S024,S268] superseded=[] round_changed=[S040,S116,S268,S294]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  repo11 FAIL: lists differ
      want: appendonly_violations=4 ids=[S169,S229] deleted=[S027,S079] superseded=[] round_changed=[S027,S079,S169,S229,S296]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  repo12 FAIL: lists differ
      want: appendonly_violations=3 ids=[S039] deleted=[S175,S223] superseded=[S039] round_changed=[S223]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  repo13 FAIL: lists differ
      want: appendonly_violations=5 ids=[S198,S252] deleted=[S036,S051,S072] superseded=[S198] round_changed=[S036,S051,S132,S176,S198]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  repo14 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S216] superseded=[] round_changed=[]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  repo15 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S184] superseded=[] round_changed=[S184]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  repo16 FAIL: lists differ
      want: appendonly_violations=3 ids=[S043] deleted=[S063,S268] superseded=[S043] round_changed=[S063]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  repo17 FAIL: lists differ
      want: appendonly_violations=4 ids=[] deleted=[S172,S181,S230,S295] superseded=[] round_changed=[S172]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  repo18 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S231] superseded=[] round_changed=[]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  repo19 FAIL: lists differ
      want: appendonly_violations=5 ids=[S151,S235,S241] deleted=[S083,S096] superseded=[S151] round_changed=[S235]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  repo20 FAIL: lists differ
      want: appendonly_violations=2 ids=[S051] deleted=[S121] superseded=[S051] round_changed=[S121]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  repo21 FAIL: lists differ
      want: appendonly_violations=3 ids=[S024] deleted=[S111,S193] superseded=[] round_changed=[S019,S024,S111,S193]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  repo22 FAIL: lists differ
      want: appendonly_violations=4 ids=[S164] deleted=[S123,S138,S262] superseded=[] round_changed=[S123,S164]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  repo23 FAIL: lists differ
      want: appendonly_violations=2 ids=[S018,S210] deleted=[] superseded=[S018] round_changed=[S018,S188,S210]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
real arm: FAIL (2.4s)
  tool:   appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  diff: ids: want=['S041', 'S044', 'S051', 'S062', 'S064', 'S069', 'S179', 'S180', 'S181', 'S182', 'S183', 'S184', 'S185', 'S186', 'S188', 'S189', 'S190', 'S193'] got=[]
  diff: superseded: want=['S069', 'S182', 'S193'] got=[]
  diff: round_changed: want=['S182', 'S193'] got=[]
  diff: violations: want=18 got=0
  tool exit=0
C2=unmet
seed=13849288804729767862
```
Counter exit code: 1. Control rejected: all 24 blind histories differed; the real oracle reported 18 violations versus the control's zero (scored output above).

Integrity/restoration evidence: the pre-score `timeout 120 sha256sum` command for J1.py, count-c2.py, and contract.md returned respectively `da68bfbacefaa5d986c68f12b71ffe1ce9bf9515016a4f425119191505e5363f`, `302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb`, and `d903c67950a081c3e25d19a208f79c84ab6e34f99680acea31d3f8590eaa431a`. After scoring, `timeout 120 sha256sum` on J1.py, count-c1.py, count-c2.py, and contract.md returned:
```text
da68bfbacefaa5d986c68f12b71ffe1ce9bf9515016a4f425119191505e5363f  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J1.py
ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py
302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
d903c67950a081c3e25d19a208f79c84ab6e34f99680acea31d3f8590eaa431a  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/contract.md
```
No existing target source was edited; the new control is retained as assigned. Pristine/restored behavioral runs were not performed: this receipt scores the assigned substitute control, not a killed-mutant claim from a passing baseline.

Containment: L1 MoriR36 authorized the frozen counter's self-cleaning transient directories and clone in its direct reply to the containment question. The prescribed command completed synchronously; no background jobs or services were started. Counter cleanup is implemented at `.ufo/waves/round-36/count-c2.py:715-718`. Before running, `timeout 120 df -h /fast` reported 69G available, 92% used. No tools were installed or updated.

VERDICT: J1 unmet exit 1
