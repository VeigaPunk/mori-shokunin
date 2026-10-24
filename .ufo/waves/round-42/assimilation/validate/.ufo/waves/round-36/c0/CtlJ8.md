measured 2026-10-23T12:01:08Z
control J8 shape denial
control_sha256 3332b68e76bf52f7ddd37fd818cc37991399de9e0e888162c3076e389a92476b
counter_sha256 302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb

Axes: detector correctness, defect specificity, scratch containment and exact restoration.

## Mutant and expected detector

The only scratch mutation was `probe.py:66`, replacing `return ids, round_changed` with
`return set(tip) - ids, (set(tip) - round_changed if has_base else set())`.
The retained control has identical mutated bytes: `.ufo/waves/round-36/c0/controls/J8.py:65-66`.
Thus ids is the complement over rows present at rev; round_changed is the complement over those rows
when a round base is supplied, and remains empty without a base. Deletion detection is unchanged;
counts, changed lines, superseded subset and exits follow the emitted lists (control:99-119).
This is the requested denial at the output projection, not a replacement history rule
(contract:62-77; control:81-101).
Expected detector: exact hidden-truth list comparison rejects denial
(`.ufo/waves/round-36/count-c2.py:517-522,601-621`).

## Frozen bytes

Command: `timeout 30 sha256sum /fast/scratch/hyaku/mori-r36/CtlJ8/probe.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J8.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py`
Output before scoring the mutant:
```text
3332b68e76bf52f7ddd37fd818cc37991399de9e0e888162c3076e389a92476b  /fast/scratch/hyaku/mori-r36/CtlJ8/probe.py
3332b68e76bf52f7ddd37fd818cc37991399de9e0e888162c3076e389a92476b  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J8.py
ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py
302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
```
Both counters match `.ufo/waves/round-36/evidence/freeze.txt:3-4`.

## Execution containment

Each detector ran the following unchanged inner command, without --seed:
`timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py 6bd57097 --tool <program>`.
Outer wrapper: `timeout 900 unshare --user --map-root-user --mount --pid --fork --kill-child /bin/sh /fast/scratch/hyaku/mori-r36/CtlJ8/run-counter.sh <program>`.
The runner bind-mounts the seat scratch over the counter scratch root and sets TMPDIR there
(`/fast/scratch/hyaku/mori-r36/CtlJ8/run-counter.sh:3-6`). PID namespace teardown contains all descendants;
all three wrapper invocations returned, with the exits below. No background jobs were started.
For pristine/restored only, the inner program path is the namespace alias of the seat's probe.py.
L1 authorized counter-owned transient clone pack files over 10 MB; the authored files remain below 10 MB.
Capacity check before clone writes: `timeout 20 df -h /fast` reported 804G size, 735G used, 69G available, 92% used.

## Pristine detector output

```text
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /fast/scratch/hyaku/mori-r36/probe.py
blind arm: 24/24 sandbox histories matched the hidden truth (3.2s; coverage: deletions=22 changed-back=14 superseded=7)
real arm: pass (2.5s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
C2=met
seed=4620255492431270592
exit=0
```

## Assigned J8 counter output (full)

Program: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J8.py`.
```text
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J8.py
blind arm: 0/24 sandbox histories matched the hidden truth (1.9s; coverage: deletions=24 changed-back=15 superseded=7)
  repo00 FAIL: lists differ
      want: appendonly_violations=4 ids=[S144,S208] deleted=[S213,S260] superseded=[S144,S208] round_changed=[S208,S213]
      got:  appendonly_violations=11 ids=[S048,S080,S085,S099,S146,S158,S178,S188,S268] deleted=[S213,S260] superseded=[] round_changed=[S048,S080,S085,S099,S144,S146,S158,S178,S188,S268]
  repo01 FAIL: lists differ
      want: appendonly_violations=3 ids=[S254,S275] deleted=[S045] superseded=[] round_changed=[S034,S254,S275,S281]
      got:  appendonly_violations=6 ids=[S034,S053,S161,S177,S281] deleted=[S045] superseded=[] round_changed=[S053,S161,S177]
  repo02 FAIL: lists differ
      want: appendonly_violations=3 ids=[S177] deleted=[S049,S160] superseded=[] round_changed=[S160,S177]
      got:  appendonly_violations=12 ids=[S005,S014,S030,S039,S042,S104,S111,S113,S212,S263] deleted=[S049,S160] superseded=[] round_changed=[S005,S014,S030,S039,S042,S104,S111,S113,S212,S263]
  repo03 FAIL: lists differ
      want: appendonly_violations=3 ids=[S283] deleted=[S125,S199] superseded=[S283] round_changed=[S067,S125,S199]
      got:  appendonly_violations=12 ids=[S004,S036,S067,S100,S109,S112,S159,S206,S250,S278] deleted=[S125,S199] superseded=[] round_changed=[S004,S036,S100,S109,S112,S159,S206,S250,S278,S283]
  repo04 FAIL: lists differ
      want: appendonly_violations=2 ids=[S122] deleted=[S243] superseded=[S122] round_changed=[S243]
      got:  appendonly_violations=14 ids=[S016,S020,S056,S080,S119,S149,S159,S221,S234,S239,S252,S253,S284] deleted=[S243] superseded=[] round_changed=[S016,S020,S056,S080,S119,S122,S149,S159,S221,S234,S239,S252,S253,S284]
  repo05 FAIL: lists differ
      want: appendonly_violations=3 ids=[S272] deleted=[S212,S286] superseded=[] round_changed=[S272,S286,S288]
      got:  appendonly_violations=9 ids=[S023,S080,S087,S112,S116,S173,S288] deleted=[S212,S286] superseded=[] round_changed=[S023,S080,S087,S112,S116,S173]
  repo06 FAIL: lists differ
      want: appendonly_violations=2 ids=[S076] deleted=[S255] superseded=[] round_changed=[S076,S255,S270]
      got:  appendonly_violations=15 ids=[S046,S047,S090,S102,S113,S123,S129,S146,S173,S206,S224,S245,S262,S270] deleted=[S255] superseded=[S270] round_changed=[S046,S047,S090,S102,S113,S123,S129,S146,S173,S206,S224,S245,S262]
  repo07 FAIL: lists differ
      want: appendonly_violations=2 ids=[S079] deleted=[S198] superseded=[] round_changed=[S079,S198,S250]
      got:  appendonly_violations=14 ids=[S001,S035,S050,S103,S109,S132,S141,S147,S163,S177,S188,S211,S250] deleted=[S198] superseded=[] round_changed=[S001,S035,S050,S103,S109,S132,S141,S147,S163,S177,S188,S211]
  repo08 FAIL: lists differ
      want: appendonly_violations=4 ids=[S115,S121] deleted=[S027,S093] superseded=[S115] round_changed=[S093,S121]
      got:  appendonly_violations=9 ids=[S023,S108,S128,S245,S254,S262,S290] deleted=[S027,S093] superseded=[] round_changed=[S023,S108,S115,S128,S245,S254,S262,S290]
  repo09 FAIL: lists differ
      want: appendonly_violations=3 ids=[] deleted=[S022,S262,S286] superseded=[] round_changed=[S171,S262,S286]
      got:  appendonly_violations=13 ids=[S009,S035,S085,S091,S167,S171,S172,S185,S251,S263] deleted=[S022,S262,S286] superseded=[S171] round_changed=[S009,S035,S085,S091,S167,S172,S185,S251,S263]
  repo10 FAIL: lists differ
      want: appendonly_violations=2 ids=[S236] deleted=[S208] superseded=[] round_changed=[S082,S236]
      got:  appendonly_violations=12 ids=[S028,S054,S082,S085,S171,S174,S185,S244,S256,S268,S280] deleted=[S208] superseded=[S082] round_changed=[S028,S054,S085,S171,S174,S185,S244,S256,S268,S280]
  repo11 FAIL: lists differ
      want: appendonly_violations=2 ids=[S245] deleted=[S292] superseded=[] round_changed=[S198,S245]
      got:  appendonly_violations=10 ids=[S010,S035,S039,S072,S085,S198,S234,S267,S269] deleted=[S292] superseded=[] round_changed=[S010,S035,S039,S072,S085,S234,S267,S269]
  repo12 FAIL: lists differ
      want: appendonly_violations=3 ids=[S239] deleted=[S089,S094] superseded=[S239] round_changed=[S089,S094]
      got:  appendonly_violations=7 ids=[S083,S154,S210,S227,S294] deleted=[S089,S094] superseded=[] round_changed=[S083,S154,S210,S227,S239,S294]
  repo13 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S043] superseded=[] round_changed=[S043,S219]
      got:  appendonly_violations=15 ids=[S037,S048,S056,S071,S073,S135,S142,S159,S165,S211,S217,S219,S253,S278] deleted=[S043] superseded=[] round_changed=[S037,S048,S056,S071,S073,S135,S142,S159,S165,S211,S217,S253,S278]
  repo14 FAIL: lists differ
      want: appendonly_violations=4 ids=[S176] deleted=[S028,S192,S203] superseded=[] round_changed=[S176,S192,S203]
      got:  appendonly_violations=8 ids=[S008,S012,S083,S216,S282] deleted=[S028,S192,S203] superseded=[] round_changed=[S008,S012,S083,S216,S282]
  repo15 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S096] superseded=[] round_changed=[S096,S215,S265]
      got:  appendonly_violations=9 ids=[S101,S148,S157,S215,S254,S265,S278,S282] deleted=[S096] superseded=[] round_changed=[S101,S148,S157,S254,S278,S282]
  repo16 FAIL: lists differ
      want: appendonly_violations=7 ids=[S004,S100,S109] deleted=[S036,S037,S064,S227] superseded=[S100,S109] round_changed=[S004,S036,S037,S064,S100,S109,S227]
      got:  appendonly_violations=9 ids=[S056,S189,S246,S250,S284] deleted=[S036,S037,S064,S227] superseded=[] round_changed=[S056,S189,S246,S250,S284]
  repo17 FAIL: lists differ
      want: appendonly_violations=4 ids=[S012] deleted=[S102,S197,S262] superseded=[] round_changed=[S012,S102,S262]
      got:  appendonly_violations=11 ids=[S071,S084,S087,S144,S242,S245,S257,S275] deleted=[S102,S197,S262] superseded=[] round_changed=[S071,S084,S087,S144,S242,S245,S257,S275]
  repo18 FAIL: lists differ
      want: appendonly_violations=5 ids=[S146] deleted=[S035,S072,S171,S232] superseded=[] round_changed=[S072,S146,S171]
      got:  appendonly_violations=7 ids=[S084,S139,S295] deleted=[S035,S072,S171,S232] superseded=[] round_changed=[S084,S139,S295]
  repo19 FAIL: lists differ
      want: appendonly_violations=2 ids=[] deleted=[S021,S212] superseded=[] round_changed=[S021,S159,S212]
      got:  appendonly_violations=11 ids=[S016,S028,S045,S107,S139,S159,S284,S285,S287] deleted=[S021,S212] superseded=[] round_changed=[S016,S028,S045,S107,S139,S284,S285,S287]
  repo20 FAIL: lists differ
      want: appendonly_violations=7 ids=[S118,S158,S221,S252] deleted=[S145,S194,S217] superseded=[S221] round_changed=[S118,S158,S217]
      got:  appendonly_violations=6 ids=[S184,S193,S253] deleted=[S145,S194,S217] superseded=[] round_changed=[S184,S193,S221,S252,S253]
  repo21 FAIL: lists differ
      want: appendonly_violations=2 ids=[S110] deleted=[S140] superseded=[] round_changed=[S041,S110,S140]
      got:  appendonly_violations=6 ids=[S041,S072,S099,S275,S296] deleted=[S140] superseded=[] round_changed=[S072,S099,S275,S296]
  repo22 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S040] superseded=[] round_changed=[S265]
      got:  appendonly_violations=9 ids=[S021,S052,S096,S158,S215,S247,S265,S279] deleted=[S040] superseded=[] round_changed=[S021,S052,S096,S158,S215,S247,S279]
  repo23 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S105] superseded=[] round_changed=[S021,S105]
      got:  appendonly_violations=12 ids=[S002,S021,S041,S069,S090,S099,S173,S180,S236,S265,S297] deleted=[S105] superseded=[] round_changed=[S002,S041,S069,S090,S099,S173,S180,S236,S265,S297]
real arm: FAIL (1.8s)
  tool:   appendonly_violations=186 ids=[S001,S002,S003,S004,S005,S006,S007,S008,S009,S010,S011,S012,S013,S014,S015,S016,S017,S018,S019,S020,S021,S022,S023,S024,S025,S026,S027,S028,S029,S030,S031,S032,S033,S034,S035,S036,S037,S038,S039,S040,S042,S043,S045,S046,S047,S048,S049,S050,S052,S053,S054,S055,S056,S057,S058,S059,S060,S061,S063,S065,S066,S067,S068,S070,S071,S072,S073,S074,S075,S076,S077,S078,S079,S080,S081,S082,S083,S084,S085,S086,S087,S088,S089,S090,S091,S092,S093,S094,S095,S096,S097,S098,S099,S100,S101,S102,S103,S104,S105,S106,S107,S108,S109,S110,S111,S112,S113,S114,S115,S116,S117,S118,S119,S120,S121,S122,S123,S124,S125,S126,S127,S128,S129,S130,S131,S132,S133,S134,S135,S136,S137,S138,S139,S140,S141,S142,S143,S144,S145,S146,S147,S148,S149,S150,S151,S152,S153,S154,S155,S156,S157,S158,S159,S160,S161,S162,S163,S164,S165,S166,S167,S168,S169,S170,S171,S172,S173,S174,S175,S176,S177,S178,S187,S191,S192,S194,S195,S196,S197,S198,S199,S200,S201,S202,S203,S204] deleted=[] superseded=[S067,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140] round_changed=[S001,S002,S003,S004,S005,S006,S007,S008,S009,S010,S011,S012,S013,S014,S015,S016,S017,S018,S019,S020,S021,S022,S023,S024,S025,S026,S027,S028,S029,S030,S031,S032,S033,S034,S035,S036,S037,S038,S039,S040,S041,S042,S043,S044,S045,S046,S047,S048,S049,S050,S051,S052,S053,S054,S055,S056,S057,S058,S059,S060,S061,S062,S063,S064,S065,S066,S067,S068,S069,S070,S071,S072,S073,S074,S075,S076,S077,S078,S079,S080,S081,S082,S083,S084,S085,S086,S087,S088,S089,S090,S091,S092,S093,S094,S095,S096,S097,S098,S099,S100,S101,S102,S103,S104,S105,S106,S107,S108,S109,S110,S111,S112,S113,S114,S115,S116,S117,S118,S119,S120,S121,S122,S123,S124,S125,S126,S127,S128,S129,S130,S131,S132,S133,S134,S135,S136,S137,S138,S139,S140,S141,S142,S143,S144,S145,S146,S147,S148,S149,S150,S151,S152,S153,S154,S155,S156,S157,S158,S159,S160,S161,S162,S163,S164,S165,S166,S167,S168,S169,S170,S171,S172,S173,S174,S175,S176,S177,S178,S179,S180,S181,S183,S184,S185,S186,S187,S188,S189,S190,S191,S192,S194,S195,S196,S197,S198,S199,S200,S201,S202,S203,S204]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  diff: ids: want=['S041', 'S044', 'S051', 'S062', 'S064', 'S069', 'S179', 'S180', 'S181', 'S182', 'S183', 'S184', 'S185', 'S186', 'S188', 'S189', 'S190', 'S193'] got=['S001', 'S002', 'S003', 'S004', 'S005', 'S006', 'S007', 'S008', 'S009', 'S010', 'S011', 'S012', 'S013', 'S014', 'S015', 'S016', 'S017', 'S018', 'S019', 'S020', 'S021', 'S022', 'S023', 'S024', 'S025', 'S026', 'S027', 'S028', 'S029', 'S030', 'S031', 'S032', 'S033', 'S034', 'S035', 'S036', 'S037', 'S038', 'S039', 'S040', 'S042', 'S043', 'S045', 'S046', 'S047', 'S048', 'S049', 'S050', 'S052', 'S053', 'S054', 'S055', 'S056', 'S057', 'S058', 'S059', 'S060', 'S061', 'S063', 'S065', 'S066', 'S067', 'S068', 'S070', 'S071', 'S072', 'S073', 'S074', 'S075', 'S076', 'S077', 'S078', 'S079', 'S080', 'S081', 'S082', 'S083', 'S084', 'S085', 'S086', 'S087', 'S088', 'S089', 'S090', 'S091', 'S092', 'S093', 'S094', 'S095', 'S096', 'S097', 'S098', 'S099', 'S100', 'S101', 'S102', 'S103', 'S104', 'S105', 'S106', 'S107', 'S108', 'S109', 'S110', 'S111', 'S112', 'S113', 'S114', 'S115', 'S116', 'S117', 'S118', 'S119', 'S120', 'S121', 'S122', 'S123', 'S124', 'S125', 'S126', 'S127', 'S128', 'S129', 'S130', 'S131', 'S132', 'S133', 'S134', 'S135', 'S136', 'S137', 'S138', 'S139', 'S140', 'S141', 'S142', 'S143', 'S144', 'S145', 'S146', 'S147', 'S148', 'S149', 'S150', 'S151', 'S152', 'S153', 'S154', 'S155', 'S156', 'S157', 'S158', 'S159', 'S160', 'S161', 'S162', 'S163', 'S164', 'S165', 'S166', 'S167', 'S168', 'S169', 'S170', 'S171', 'S172', 'S173', 'S174', 'S175', 'S176', 'S177', 'S178', 'S187', 'S191', 'S192', 'S194', 'S195', 'S196', 'S197', 'S198', 'S199', 'S200', 'S201', 'S202', 'S203', 'S204']
  diff: superseded: want=['S069', 'S182', 'S193'] got=['S067', 'S070', 'S071', 'S083', 'S084', 'S090', 'S093', 'S096', 'S097', 'S101', 'S124', 'S127', 'S128', 'S129', 'S131', 'S140']
  diff: round_changed: want=['S182', 'S193'] got=['S001', 'S002', 'S003', 'S004', 'S005', 'S006', 'S007', 'S008', 'S009', 'S010', 'S011', 'S012', 'S013', 'S014', 'S015', 'S016', 'S017', 'S018', 'S019', 'S020', 'S021', 'S022', 'S023', 'S024', 'S025', 'S026', 'S027', 'S028', 'S029', 'S030', 'S031', 'S032', 'S033', 'S034', 'S035', 'S036', 'S037', 'S038', 'S039', 'S040', 'S041', 'S042', 'S043', 'S044', 'S045', 'S046', 'S047', 'S048', 'S049', 'S050', 'S051', 'S052', 'S053', 'S054', 'S055', 'S056', 'S057', 'S058', 'S059', 'S060', 'S061', 'S062', 'S063', 'S064', 'S065', 'S066', 'S067', 'S068', 'S069', 'S070', 'S071', 'S072', 'S073', 'S074', 'S075', 'S076', 'S077', 'S078', 'S079', 'S080', 'S081', 'S082', 'S083', 'S084', 'S085', 'S086', 'S087', 'S088', 'S089', 'S090', 'S091', 'S092', 'S093', 'S094', 'S095', 'S096', 'S097', 'S098', 'S099', 'S100', 'S101', 'S102', 'S103', 'S104', 'S105', 'S106', 'S107', 'S108', 'S109', 'S110', 'S111', 'S112', 'S113', 'S114', 'S115', 'S116', 'S117', 'S118', 'S119', 'S120', 'S121', 'S122', 'S123', 'S124', 'S125', 'S126', 'S127', 'S128', 'S129', 'S130', 'S131', 'S132', 'S133', 'S134', 'S135', 'S136', 'S137', 'S138', 'S139', 'S140', 'S141', 'S142', 'S143', 'S144', 'S145', 'S146', 'S147', 'S148', 'S149', 'S150', 'S151', 'S152', 'S153', 'S154', 'S155', 'S156', 'S157', 'S158', 'S159', 'S160', 'S161', 'S162', 'S163', 'S164', 'S165', 'S166', 'S167', 'S168', 'S169', 'S170', 'S171', 'S172', 'S173', 'S174', 'S175', 'S176', 'S177', 'S178', 'S179', 'S180', 'S181', 'S183', 'S184', 'S185', 'S186', 'S187', 'S188', 'S189', 'S190', 'S191', 'S192', 'S194', 'S195', 'S196', 'S197', 'S198', 'S199', 'S200', 'S201', 'S202', 'S203', 'S204']
  diff: violations: want=18 got=186
  tool exit=1
C2=unmet
seed=12745497570481147933
exit=1
```

## Restoration evidence and repeated detector

Command: `timeout 30 sha256sum /fast/scratch/hyaku/mori-r36/CtlJ8/probe.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J8.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py`
Output after restoring scratch line 66:
```text
1df538f68fd134bd0a478903d3191c5e02fba8fe3c7c6c33ce9d1d6d34e4c462  /fast/scratch/hyaku/mori-r36/CtlJ8/probe.py
3332b68e76bf52f7ddd37fd818cc37991399de9e0e888162c3076e389a92476b  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J8.py
302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
```
Pristine pre-mutation SHA-256 was also 1df538f68fd134bd0a478903d3191c5e02fba8fe3c7c6c33ce9d1d6d34e4c462, from `timeout 20 sha256sum /fast/scratch/hyaku/mori-r36/CtlJ8/probe.py`; restoration is exact.
```text
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /fast/scratch/hyaku/mori-r36/probe.py
blind arm: 24/24 sandbox histories matched the hidden truth (2.0s; coverage: deletions=20 changed-back=17 superseded=12)
real arm: pass (1.9s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
C2=met
seed=13699073715465768182
exit=0
```

Mutation outcome: killed. Pristine and restored detectors each matched 24/24 histories and passed the real arm;
J8 matched 0/24 and failed the real arm (actual receipts above). Runs used independent random seeds printed above.
Tools installed or updated: none. No lane git writes or integration were performed.
VERDICT: J8 unmet exit 1
