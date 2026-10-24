measured 2026-10-23T11:51:45Z
control J6 shape rule-level skip (position-keyed)
control_sha256 6c8d4be47891c27fee95c7bedaf1f813d540aa1b7c894bc1b278c1eedd69a640
counter_sha256 302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb

Axes: identity-rule fidelity; detector discrimination; byte-exact restoration; write containment.

Mutation: controls/J6.py:15-16 returns the physical registry line position instead of the id; the key is consumed at controls/J6.py:35-49. All other rules remain in the same checker. The isolated scratch probe was changed at its sole identity return and then restored.
Expected detector: the unchanged C2 counter must reject position-based identity because row identity is the id, not position (contract.md:62-77); reorders and deletions occur in the blind histories (contract.md:79-83).
Paths cited without an absolute prefix are relative to /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/.

Containment: the launch below mounts the seat's scratch as the counter's fixed scratch root (count-c2.py:42,687-688), with TMPDIR there (count-c2.py:668). The rest of the filesystem is read-only; /dev and /proc are namespace mounts. Each synchronous child ran inside an isolated PID namespace and was reaped; no background jobs were started. The counter removes its temporary trees in its finally blocks (count-c2.py:715-718).
Tool installs/updates: none.

## Frozen hashes before scoring
Command: timeout 20 sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
```text
ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py
302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
```
Matched evidence/freeze.txt:3-4. The C2 hash was checked again before both scored tool variants and after restoration, with the same value.

## Initial infrastructure attempt (inconclusive, not a killed mutant)
Command: timeout 900 bwrap --ro-bind / / --bind /fast/scratch/hyaku/mori-r36/CtlJ6 /fast/scratch/hyaku/mori-r36 --unshare-user --unshare-pid --proc /proc --die-with-parent --setenv TMPDIR /fast/scratch/hyaku/mori-r36/tmp --setenv PYTHONDONTWRITEBYTECODE 1 -- timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py 6bd57097 --tool /fast/scratch/hyaku/mori-r36/probe.py
```text
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
counter setup error: git rev-parse --verify 6bd57097^{commit} failed in /home/vgpnk/Projects/shokunin/mori-shokunin: fatal: could not open '/dev/null' for reading and writing: Permission denied
exit 2
```
Correction: added the ephemeral --dev /dev mount to the launcher, without changing checker or counter bytes. All three runs below use that corrected launcher.

## Pristine detector output
Command: timeout 900 bwrap --ro-bind / / --bind /fast/scratch/hyaku/mori-r36/CtlJ6 /fast/scratch/hyaku/mori-r36 --dev /dev --unshare-user --unshare-pid --proc /proc --die-with-parent --setenv TMPDIR /fast/scratch/hyaku/mori-r36/tmp --setenv PYTHONDONTWRITEBYTECODE 1 -- timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py 6bd57097 --tool /fast/scratch/hyaku/mori-r36/probe.py
```text
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /fast/scratch/hyaku/mori-r36/probe.py
blind arm: 24/24 sandbox histories matched the hidden truth (2.9s; coverage: deletions=23 changed-back=16 superseded=11)
real arm: pass (2.1s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
C2=met
seed=16448960526940153087
exit 0
```
stderr: empty.

## J6 scored detector output (complete)
Command: timeout 900 bwrap --ro-bind / / --bind /fast/scratch/hyaku/mori-r36/CtlJ6 /fast/scratch/hyaku/mori-r36 --dev /dev --unshare-user --unshare-pid --proc /proc --die-with-parent --setenv TMPDIR /fast/scratch/hyaku/mori-r36/tmp --setenv PYTHONDONTWRITEBYTECODE 1 -- timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py 6bd57097 --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J6.py
```text
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J6.py
blind arm: 1/24 sandbox histories matched the hidden truth (3.0s; coverage: deletions=20 changed-back=15 superseded=9)
  repo00 FAIL: lists differ
      want: appendonly_violations=3 ids=[S027,S294] deleted=[S023] superseded=[S294] round_changed=[S023,S027,S294]
      got:  appendonly_violations=11 ids=[S014,S027,S103,S105,S117,S133,S138,S172,S197,S294,S296] deleted=[] superseded=[S294] round_changed=[S014,S027,S103,S105,S117,S133,S138,S172,S197,S294,S296]
  repo01 FAIL: lists differ
      want: appendonly_violations=2 ids=[S173] deleted=[S031] superseded=[] round_changed=[S173]
      got:  appendonly_violations=8 ids=[S025,S041,S062,S097,S173,S190,S216] deleted=[S041] superseded=[] round_changed=[S025,S041,S062,S097,S173,S190,S216,S229]
  repo02 FAIL: lists differ
      want: appendonly_violations=3 ids=[S154] deleted=[S113,S150] superseded=[] round_changed=[S154]
      got:  appendonly_violations=8 ids=[S041,S064,S097,S098,S134,S154,S205,S289] deleted=[] superseded=[] round_changed=[S154,S289]
  repo04 FAIL: lists differ
      want: appendonly_violations=4 ids=[S114] deleted=[S021,S067,S281] superseded=[S114] round_changed=[S067]
      got:  appendonly_violations=9 ids=[S084,S114,S128,S194,S206,S217,S257] deleted=[S194,S217] superseded=[S114] round_changed=[S084,S128,S194,S206,S217,S257]
  repo05 FAIL: lists differ
      want: appendonly_violations=2 ids=[S104,S171] deleted=[] superseded=[S171] round_changed=[S062,S104,S171]
      got:  appendonly_violations=7 ids=[S062,S104,S150,S152,S171,S176,S211] deleted=[] superseded=[S171] round_changed=[S062,S104,S171]
  repo06 FAIL: lists differ
      want: appendonly_violations=5 ids=[S153,S271] deleted=[S024,S036,S147] superseded=[] round_changed=[S024,S036,S147,S153,S271,S278]
      got:  appendonly_violations=8 ids=[S053,S153,S271,S278,S289] deleted=[S053,S153,S271] superseded=[] round_changed=[S024,S036,S053,S147,S153,S271,S278,S289]
  repo07 FAIL: lists differ
      want: appendonly_violations=2 ids=[S236] deleted=[S249] superseded=[S236] round_changed=[S249]
      got:  appendonly_violations=13 ids=[S008,S055,S073,S126,S158,S189,S197,S226,S236,S256,S274,S277] deleted=[S277] superseded=[S236] round_changed=[S008,S055,S073,S126,S158,S189,S197,S226,S236,S256,S274,S277]
  repo08 FAIL: lists differ
      want: appendonly_violations=3 ids=[S109,S298] deleted=[S188] superseded=[S109,S298] round_changed=[S109,S188,S298]
      got:  appendonly_violations=8 ids=[S092,S099,S100,S109,S153,S179,S201,S298] deleted=[] superseded=[S109,S298] round_changed=[S092,S099,S100,S109,S153,S179,S201,S298]
  repo09 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S043] superseded=[] round_changed=[S264]
      got:  appendonly_violations=3 ids=[S195,S264] deleted=[S264] superseded=[] round_changed=[S264]
  repo10 FAIL: lists differ
      want: appendonly_violations=3 ids=[S095,S296] deleted=[S137] superseded=[] round_changed=[S095,S137,S296]
      got:  appendonly_violations=9 ids=[S015,S050,S092,S095,S233,S273,S294,S296] deleted=[S294] superseded=[] round_changed=[S015,S050,S092,S095,S233,S273,S294,S296]
  repo11 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S183] superseded=[] round_changed=[S066,S183,S194]
      got:  appendonly_violations=8 ids=[S034,S057,S066,S124,S161,S178,S194,S267] deleted=[] superseded=[] round_changed=[S034,S057,S066,S124,S161,S178,S185,S194,S267]
  repo12 FAIL: lists differ
      want: appendonly_violations=2 ids=[S263] deleted=[S173] superseded=[S263] round_changed=[S173]
      got:  appendonly_violations=12 ids=[S056,S060,S071,S097,S108,S126,S151,S164,S182,S210,S227,S263] deleted=[] superseded=[S263] round_changed=[S056,S060,S071,S097,S108,S126,S151,S164,S182,S210,S227,S263]
  repo13 FAIL: lists differ
      want: appendonly_violations=2 ids=[S240] deleted=[S278] superseded=[] round_changed=[S211,S240,S278]
      got:  appendonly_violations=5 ids=[S092,S136,S164,S240] deleted=[S092] superseded=[] round_changed=[S008,S092,S136,S164,S211,S232,S240]
  repo14 FAIL: lists differ
      want: appendonly_violations=3 ids=[S278] deleted=[S053,S218] superseded=[] round_changed=[S053,S218,S278]
      got:  appendonly_violations=10 ids=[S013,S026,S029,S039,S051,S143,S195,S265,S267,S278] deleted=[] superseded=[] round_changed=[S013,S018,S026,S029,S039,S051,S053,S143,S195,S218,S265,S267,S278]
  repo15 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S098] superseded=[] round_changed=[S098,S255]
      got:  appendonly_violations=12 ids=[S018,S033,S049,S105,S106,S119,S234,S244,S255,S285,S294] deleted=[S285] superseded=[] round_changed=[S018,S033,S049,S105,S106,S119,S234,S244,S255,S285,S294]
  repo16 FAIL: lists differ
      want: appendonly_violations=4 ids=[S095,S267] deleted=[S068,S237] superseded=[S095] round_changed=[S068,S084,S237,S267]
      got:  appendonly_violations=7 ids=[S002,S080,S083,S084,S095,S171,S267] deleted=[] superseded=[S084,S095] round_changed=[S002,S080,S083,S084,S095,S171,S237,S267]
  repo17 FAIL: lists differ
      want: appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[S229]
      got:  appendonly_violations=11 ids=[S078,S095,S100,S102,S111,S185,S215,S229,S238,S258,S281] deleted=[] superseded=[] round_changed=[S078,S095,S100,S102,S111,S185,S215,S229,S238,S258,S281]
  repo18 FAIL: lists differ
      want: appendonly_violations=6 ids=[S056,S096,S241] deleted=[S042,S216,S293] superseded=[S096] round_changed=[S042,S056,S216,S241,S293]
      got:  appendonly_violations=12 ids=[S054,S056,S087,S096,S154,S183,S218,S222,S241,S270,S284] deleted=[S054] superseded=[S096] round_changed=[S042,S054,S056,S087,S096,S154,S183,S216,S218,S222,S241,S270,S284,S293]
  repo19 FAIL: lists differ
      want: appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[S033]
      got:  appendonly_violations=10 ids=[S024,S033,S150,S163,S173,S175,S211,S254,S265,S277] deleted=[] superseded=[] round_changed=[S033,S047,S150,S163,S173,S175,S211,S230,S265,S277]
  repo20 FAIL: lists differ
      want: appendonly_violations=4 ids=[S034,S155] deleted=[S261,S269] superseded=[S034] round_changed=[S155,S261]
      got:  appendonly_violations=11 ids=[S010,S016,S034,S106,S154,S155,S157,S173,S243,S274] deleted=[S010] superseded=[S034] round_changed=[S010,S016,S034,S106,S154,S155,S157,S173,S243,S261,S274]
  repo21 FAIL: lists differ
      want: appendonly_violations=2 ids=[S012] deleted=[S196] superseded=[] round_changed=[S012,S196,S218]
      got:  appendonly_violations=5 ids=[S012,S082,S089,S198,S218] deleted=[] superseded=[] round_changed=[S012,S082,S089,S092,S196,S198,S218]
  repo22 FAIL: lists differ
      want: appendonly_violations=3 ids=[S066] deleted=[S133,S290] superseded=[] round_changed=[S066,S133,S136,S290]
      got:  appendonly_violations=7 ids=[S010,S066,S094,S095,S136,S203,S295] deleted=[] superseded=[S136] round_changed=[S010,S066,S094,S095,S136,S203,S290,S295]
  repo23 FAIL: lists differ
      want: appendonly_violations=5 ids=[S053] deleted=[S026,S050,S086,S159] superseded=[] round_changed=[S155]
      got:  appendonly_violations=6 ids=[S053,S075,S082,S155] deleted=[S050,S075] superseded=[] round_changed=[S155]
real arm: FAIL (2.2s)
  tool:   appendonly_violations=23 ids=[S041,S044,S051,S062,S064,S069,S147,S148,S149,S150,S151,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  diff: ids: want=['S041', 'S044', 'S051', 'S062', 'S064', 'S069', 'S179', 'S180', 'S181', 'S182', 'S183', 'S184', 'S185', 'S186', 'S188', 'S189', 'S190', 'S193'] got=['S041', 'S044', 'S051', 'S062', 'S064', 'S069', 'S147', 'S148', 'S149', 'S150', 'S151', 'S179', 'S180', 'S181', 'S182', 'S183', 'S184', 'S185', 'S186', 'S188', 'S189', 'S190', 'S193']
  diff: violations: want=18 got=23
  tool exit=1
C2=unmet
seed=7488248360023087836
exit 1
```
stderr: empty.

## Restored detector output
Command: timeout 900 bwrap --ro-bind / / --bind /fast/scratch/hyaku/mori-r36/CtlJ6 /fast/scratch/hyaku/mori-r36 --dev /dev --unshare-user --unshare-pid --proc /proc --die-with-parent --setenv TMPDIR /fast/scratch/hyaku/mori-r36/tmp --setenv PYTHONDONTWRITEBYTECODE 1 -- timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py 6bd57097 --tool /fast/scratch/hyaku/mori-r36/probe.py
```text
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /fast/scratch/hyaku/mori-r36/probe.py
blind arm: 24/24 sandbox histories matched the hidden truth (2.8s; coverage: deletions=22 changed-back=14 superseded=9)
real arm: pass (2.2s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
C2=met
seed=18327114383962493407
exit 0
```
stderr: empty. No run supplied --seed; the same frozen detector independently drew each run's histories.

## Byte restoration evidence
Command before mutation: timeout 20 sha256sum /fast/scratch/hyaku/mori-r36/CtlJ6/probe.py
```text
7bb81fa0b0686dc204a0b189fc2829afe577b9424ae57fdb86b881cbf5c7b24e  /fast/scratch/hyaku/mori-r36/CtlJ6/probe.py
```
Command at mutation: timeout 20 sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J6.py /fast/scratch/hyaku/mori-r36/CtlJ6/probe.py
```text
6c8d4be47891c27fee95c7bedaf1f813d540aa1b7c894bc1b278c1eedd69a640  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J6.py
6c8d4be47891c27fee95c7bedaf1f813d540aa1b7c894bc1b278c1eedd69a640  /fast/scratch/hyaku/mori-r36/CtlJ6/probe.py
```
Command after restoration: timeout 20 sha256sum /fast/scratch/hyaku/mori-r36/CtlJ6/probe.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J6.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
```text
7bb81fa0b0686dc204a0b189fc2829afe577b9424ae57fdb86b881cbf5c7b24e  /fast/scratch/hyaku/mori-r36/CtlJ6/probe.py
6c8d4be47891c27fee95c7bedaf1f813d540aa1b7c894bc1b278c1eedd69a640  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J6.py
302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
```
Scratch before and restored hashes are identical; the lane control intentionally retains the assigned mutant. Only the named control and this report were written in the lane; no lane git writes were performed.
Mutation outcome: killed. Pristine and restored runs each matched 24/24 blind histories and passed the real arm; J6 matched 1/24 and failed the real arm. These are detector observations, not a ruling on integration or the claim.
VERDICT: J6 unmet exit 1
