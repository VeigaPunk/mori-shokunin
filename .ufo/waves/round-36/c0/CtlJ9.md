measured 2026-10-23T12:00:12Z
control J9 shape word bag
control_sha256 75849ce2c6ef03d781412608217686bda10ae00a492dfacbec8d6b704b60e6b1
counter_sha256 302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb

Axes: control-shape fidelity; detector discrimination; frozen-byte and write containment.
Mutation: independent random.SystemRandom subsets of ids present at the requested revision for each list (controls/J9.py:49-70). No ancestry is examined. CLI, sorted lists, count and exit conventions follow contract.md:60-77; round_changed is empty without --round-base (controls/J9.py:12-16,55-56).
Expected detector: C2=unmet, exit 1 [INFERENCE before measurement]. Present-only deleted lists cannot match histories containing genuinely absent ids; the detector requires at least 12 deletion histories (count-c2.py:595-596,701-704).

Freeze check before scoring:
Command: timeout 30 sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
Output:
ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py
302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
Both matched evidence/freeze.txt:3-4 before scoring. The contract hash from timeout 20 sha256sum was d903c67950a081c3e25d19a208f79c84ab6e34f99680acea31d3f8590eaa431a, matching evidence/freeze.txt:2.

Containment:
The scored command ran unchanged inside bwrap with a read-only host root, /tmp and the counter scratch root remapped into /fast/scratch/hyaku/mori-r36/CtlJ9/, and a private process namespace. The initial mount omitted --dev /dev; git could not open /dev/null read/write. That setup attempt was inconclusive, not a killed mutant. It was corrected only by mounting private writable devices; neither control nor counter bytes changed.
L1 MoriR36 explicitly authorized counter-owned transient clone packs above 10 MB in a message during this probe. Authored control and report remain below 10 MB.
Command: timeout 15 df -h /fast
Output: /dev/nvme1n1p2 804G 734G 70G 92% /fast

Initial inconclusive setup attempt, full output:
```
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
counter setup error: git rev-parse --verify 6bd57097^{commit} failed in /home/vgpnk/Projects/shokunin/mori-shokunin: fatal: could not open '/dev/null' for reading and writing: Permission denied
exit 2
```

Scored command (no --seed):
```
timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py 6bd57097 --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J9.py
```
Containment wrapper:
```
bwrap --ro-bind / / --dev /dev --bind /fast/scratch/hyaku/mori-r36/CtlJ9/tmp /tmp --bind /fast/scratch/hyaku/mori-r36/CtlJ9 /fast/scratch/hyaku/mori-r36 --unshare-user --unshare-pid --proc /proc --die-with-parent --new-session -- <scored command>
```

Full scored counter stdout:
```
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J9.py
blind arm: 0/24 sandbox histories matched the hidden truth (2.1s; coverage: deletions=24 changed-back=13 superseded=10)
  repo00 FAIL: lists differ
      want: appendonly_violations=2 ids=[S267] deleted=[S198] superseded=[S267] round_changed=[S198]
      got:  appendonly_violations=11 ids=[S006,S060,S099,S134] deleted=[S006,S007,S023,S060,S092,S127,S134] superseded=[S006,S023,S040,S060,S099,S116,S127,S134] round_changed=[S006,S023,S040,S060,S127,S134]
  repo01 FAIL: lists differ
      want: appendonly_violations=2 ids=[S006] deleted=[S065] superseded=[] round_changed=[S006,S065,S266]
      got:  appendonly_violations=7 ids=[S032,S124,S266,S270,S285] deleted=[S124,S266] superseded=[S019,S252,S266,S270] round_changed=[S006,S032,S036,S124,S252,S266,S270,S285]
  repo02 FAIL: lists differ
      want: appendonly_violations=2 ids=[] deleted=[S128,S192] superseded=[] round_changed=[S192]
      got:  appendonly_violations=15 ids=[S051,S098,S109,S133,S146,S170,S185,S206,S290] deleted=[S098,S109,S141,S146,S170,S185] superseded=[S098,S133,S141,S290] round_changed=[S133,S141,S146,S170,S185,S290]
  repo03 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S185] superseded=[] round_changed=[S046,S185,S222]
      got:  appendonly_violations=8 ids=[S042,S163,S202,S287] deleted=[S042,S046,S163,S202] superseded=[S202,S222,S287] round_changed=[S042,S202,S287,S299]
  repo04 FAIL: lists differ
      want: appendonly_violations=2 ids=[S190] deleted=[S239] superseded=[S190] round_changed=[S239]
      got:  appendonly_violations=4 ids=[S088,S254] deleted=[S120,S212] superseded=[S088,S190,S202,S212] round_changed=[S120,S190]
  repo05 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S100] superseded=[] round_changed=[S089,S100]
      got:  appendonly_violations=6 ids=[S013,S158,S231] deleted=[S158,S195,S249] superseded=[S013,S089] round_changed=[S158,S195]
  repo06 FAIL: lists differ
      want: appendonly_violations=3 ids=[S064] deleted=[S033,S293] superseded=[] round_changed=[S033,S064,S293]
      got:  appendonly_violations=9 ids=[S064,S106,S169] deleted=[S064,S106,S112,S206,S258,S283] superseded=[S112,S206] round_changed=[S106,S121,S169,S206,S258,S283]
  repo07 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S004] superseded=[] round_changed=[S004,S048,S109]
      got:  appendonly_violations=10 ids=[S006,S048,S105,S138,S174] deleted=[S006,S048,S109,S138,S174] superseded=[S006,S048,S105,S174] round_changed=[S006,S012,S105]
  repo08 FAIL: lists differ
      want: appendonly_violations=2 ids=[S158] deleted=[S017] superseded=[S158] round_changed=[S017]
      got:  appendonly_violations=6 ids=[S083,S283] deleted=[S078,S115,S158,S283] superseded=[S124,S148,S158,S283] round_changed=[S083,S115,S148,S283]
  repo09 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S131] superseded=[] round_changed=[S046,S131,S175,S180,S219]
      got:  appendonly_violations=8 ids=[S040,S117,S136,S175,S247] deleted=[S136,S175,S180] superseded=[S040,S078,S136,S175] round_changed=[S078,S117,S136,S175,S180,S219]
  repo10 FAIL: lists differ
      want: appendonly_violations=3 ids=[] deleted=[S075,S117,S191] superseded=[] round_changed=[S075,S117,S191,S246]
      got:  appendonly_violations=7 ids=[S015,S065] deleted=[S015,S030,S065,S246,S250] superseded=[S246,S250,S283] round_changed=[S015,S065,S246,S250]
  repo11 FAIL: lists differ
      want: appendonly_violations=6 ids=[S118,S170,S288,S296] deleted=[S051,S156] superseded=[S288,S296] round_changed=[S118]
      got:  appendonly_violations=18 ids=[S099,S118,S147,S153,S170,S195,S208,S265,S288,S296] deleted=[S087,S153,S195,S207,S208,S265,S288,S296] superseded=[S087,S099,S118,S153,S170,S207,S208,S265] round_changed=[S118,S147,S153,S195,S207,S208,S265]
  repo12 FAIL: lists differ
      want: appendonly_violations=5 ids=[S014] deleted=[S024,S127,S229,S279] superseded=[S014] round_changed=[S127]
      got:  appendonly_violations=4 ids=[S053,S173] deleted=[S053,S174] superseded=[S106] round_changed=[S014]
  repo13 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S274] superseded=[] round_changed=[S271]
      got:  appendonly_violations=7 ids=[S139,S143,S223] deleted=[S014,S139,S223,S271] superseded=[S049,S143,S271] round_changed=[S143,S149,S223,S265]
  repo14 FAIL: lists differ
      want: appendonly_violations=4 ids=[S129] deleted=[S004,S025,S189] superseded=[S129] round_changed=[S004,S025,S129,S189]
      got:  appendonly_violations=5 ids=[S019,S129,S132,S278] deleted=[S019] superseded=[] round_changed=[S019,S023,S129]
  repo15 FAIL: lists differ
      want: appendonly_violations=2 ids=[S063] deleted=[S122] superseded=[S063] round_changed=[S029]
      got:  appendonly_violations=4 ids=[S063,S073] deleted=[S179,S249] superseded=[S063,S093,S179,S217,S249] round_changed=[S029,S063,S073,S093,S179]
  repo16 FAIL: lists differ
      want: appendonly_violations=5 ids=[S080,S094,S131] deleted=[S074,S228] superseded=[S094] round_changed=[S080,S131,S228]
      got:  appendonly_violations=4 ids=[S248] deleted=[S080,S082,S131] superseded=[S082,S094,S129,S248] round_changed=[S094,S131]
  repo17 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S094] superseded=[] round_changed=[S112]
      got:  appendonly_violations=9 ids=[S066,S111,S218,S259] deleted=[S066,S088,S111,S112,S259] superseded=[S066,S088,S111,S259] round_changed=[S111,S112]
  repo18 FAIL: lists differ
      want: appendonly_violations=3 ids=[S026,S065] deleted=[S093] superseded=[S026] round_changed=[S026,S065,S093]
      got:  appendonly_violations=11 ids=[S018,S026,S065,S112,S138,S243,S264] deleted=[S138,S190,S243,S254] superseded=[S012,S018,S026,S112,S138,S163,S179,S264,S292] round_changed=[S018,S098,S112,S190,S243]
  repo19 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S054] superseded=[] round_changed=[S054,S168,S222]
      got:  appendonly_violations=12 ids=[S027,S068,S168,S185,S193] deleted=[S002,S074,S115,S168,S185,S193,S283] superseded=[S002,S074,S115,S193,S222,S283] round_changed=[S002,S027,S105,S165,S168,S185,S193,S222]
  repo20 FAIL: lists differ
      want: appendonly_violations=3 ids=[S125] deleted=[S242,S297] superseded=[S125] round_changed=[S242]
      got:  appendonly_violations=16 ids=[S032,S056,S102,S126,S128,S171,S189,S262] deleted=[S032,S125,S126,S189,S234,S262,S264,S293] superseded=[S032,S125,S126,S128,S167,S171,S189] round_changed=[S032,S056,S171,S262]
  repo21 FAIL: lists differ
      want: appendonly_violations=5 ids=[S053] deleted=[S010,S118,S134,S267] superseded=[] round_changed=[S010,S053,S134,S265,S267]
      got:  appendonly_violations=7 ids=[S053,S129] deleted=[S053,S129,S243,S265,S292] superseded=[S053,S265] round_changed=[S129,S243,S265,S292]
  repo22 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S192] superseded=[] round_changed=[]
      got:  appendonly_violations=10 ids=[S009,S275,S296] deleted=[S114,S173,S234,S247,S275,S284,S296] superseded=[S009,S173,S178,S234,S247,S275,S296] round_changed=[S114,S178,S234,S284,S296]
  repo23 FAIL: lists differ
      want: appendonly_violations=2 ids=[S262] deleted=[S016] superseded=[] round_changed=[S004,S262]
      got:  appendonly_violations=8 ids=[S081,S089,S138,S199,S262] deleted=[S081,S089,S199] superseded=[S004,S089,S108,S140,S199] round_changed=[S004,S081,S108,S199,S262]
real arm: FAIL (2.7s)
  tool:   appendonly_violations=194 ids=[S004,S005,S006,S013,S014,S015,S016,S020,S025,S027,S029,S031,S032,S038,S042,S044,S046,S047,S048,S050,S057,S058,S063,S064,S067,S068,S070,S071,S076,S077,S079,S083,S084,S085,S086,S087,S089,S091,S092,S095,S096,S097,S099,S101,S102,S103,S105,S106,S109,S110,S114,S116,S120,S122,S123,S124,S128,S129,S131,S132,S133,S137,S138,S139,S140,S141,S142,S145,S147,S149,S150,S151,S153,S154,S156,S158,S159,S161,S162,S163,S168,S169,S170,S171,S172,S178,S182,S183,S185,S186,S188,S190,S191,S194,S196,S197,S202,S203] deleted=[S001,S004,S007,S009,S011,S012,S015,S018,S019,S021,S025,S027,S028,S029,S031,S033,S034,S035,S036,S037,S040,S041,S045,S048,S049,S052,S056,S057,S061,S062,S063,S064,S066,S068,S070,S072,S073,S074,S077,S078,S079,S081,S085,S086,S090,S091,S092,S097,S101,S102,S103,S107,S109,S110,S112,S114,S116,S117,S119,S121,S122,S123,S125,S129,S130,S131,S140,S141,S142,S143,S145,S146,S147,S149,S154,S157,S162,S164,S167,S170,S171,S172,S173,S174,S176,S180,S181,S184,S187,S190,S194,S195,S197,S199,S200,S203] superseded=[S001,S002,S004,S007,S010,S011,S014,S015,S017,S019,S020,S022,S025,S026,S028,S029,S031,S033,S035,S040,S041,S045,S048,S049,S050,S053,S056,S057,S061,S064,S068,S070,S072,S073,S083,S085,S086,S088,S089,S095,S099,S100,S101,S104,S105,S108,S109,S110,S111,S113,S114,S115,S116,S117,S120,S121,S123,S124,S127,S128,S129,S132,S133,S136,S138,S141,S144,S147,S148,S150,S152,S153,S157,S158,S159,S160,S161,S162,S165,S167,S168,S169,S173,S175,S176,S177,S178,S179,S182,S184,S185,S187,S188,S192,S193,S194,S195,S196,S198,S201,S202,S204] round_changed=[S001,S002,S003,S004,S006,S011,S013,S015,S017,S020,S021,S022,S024,S025,S029,S030,S032,S033,S034,S035,S038,S041,S042,S043,S044,S045,S046,S051,S055,S057,S058,S061,S062,S063,S065,S066,S067,S068,S069,S070,S071,S073,S077,S078,S080,S081,S082,S084,S086,S087,S088,S090,S091,S093,S096,S098,S100,S104,S105,S106,S107,S113,S116,S121,S123,S124,S125,S126,S129,S133,S134,S136,S137,S138,S139,S140,S141,S145,S149,S154,S156,S157,S158,S159,S161,S165,S166,S168,S169,S170,S171,S173,S175,S178,S180,S181,S182,S183,S187,S189,S190,S191,S192,S193,S194,S196,S198,S199,S201,S203,S204]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  diff: ids: want=['S041', 'S044', 'S051', 'S062', 'S064', 'S069', 'S179', 'S180', 'S181', 'S182', 'S183', 'S184', 'S185', 'S186', 'S188', 'S189', 'S190', 'S193'] got=['S004', 'S005', 'S006', 'S013', 'S014', 'S015', 'S016', 'S020', 'S025', 'S027', 'S029', 'S031', 'S032', 'S038', 'S042', 'S044', 'S046', 'S047', 'S048', 'S050', 'S057', 'S058', 'S063', 'S064', 'S067', 'S068', 'S070', 'S071', 'S076', 'S077', 'S079', 'S083', 'S084', 'S085', 'S086', 'S087', 'S089', 'S091', 'S092', 'S095', 'S096', 'S097', 'S099', 'S101', 'S102', 'S103', 'S105', 'S106', 'S109', 'S110', 'S114', 'S116', 'S120', 'S122', 'S123', 'S124', 'S128', 'S129', 'S131', 'S132', 'S133', 'S137', 'S138', 'S139', 'S140', 'S141', 'S142', 'S145', 'S147', 'S149', 'S150', 'S151', 'S153', 'S154', 'S156', 'S158', 'S159', 'S161', 'S162', 'S163', 'S168', 'S169', 'S170', 'S171', 'S172', 'S178', 'S182', 'S183', 'S185', 'S186', 'S188', 'S190', 'S191', 'S194', 'S196', 'S197', 'S202', 'S203']
  diff: deleted: want=[] got=['S001', 'S004', 'S007', 'S009', 'S011', 'S012', 'S015', 'S018', 'S019', 'S021', 'S025', 'S027', 'S028', 'S029', 'S031', 'S033', 'S034', 'S035', 'S036', 'S037', 'S040', 'S041', 'S045', 'S048', 'S049', 'S052', 'S056', 'S057', 'S061', 'S062', 'S063', 'S064', 'S066', 'S068', 'S070', 'S072', 'S073', 'S074', 'S077', 'S078', 'S079', 'S081', 'S085', 'S086', 'S090', 'S091', 'S092', 'S097', 'S101', 'S102', 'S103', 'S107', 'S109', 'S110', 'S112', 'S114', 'S116', 'S117', 'S119', 'S121', 'S122', 'S123', 'S125', 'S129', 'S130', 'S131', 'S140', 'S141', 'S142', 'S143', 'S145', 'S146', 'S147', 'S149', 'S154', 'S157', 'S162', 'S164', 'S167', 'S170', 'S171', 'S172', 'S173', 'S174', 'S176', 'S180', 'S181', 'S184', 'S187', 'S190', 'S194', 'S195', 'S197', 'S199', 'S200', 'S203']
  diff: superseded: want=['S069', 'S182', 'S193'] got=['S001', 'S002', 'S004', 'S007', 'S010', 'S011', 'S014', 'S015', 'S017', 'S019', 'S020', 'S022', 'S025', 'S026', 'S028', 'S029', 'S031', 'S033', 'S035', 'S040', 'S041', 'S045', 'S048', 'S049', 'S050', 'S053', 'S056', 'S057', 'S061', 'S064', 'S068', 'S070', 'S072', 'S073', 'S083', 'S085', 'S086', 'S088', 'S089', 'S095', 'S099', 'S100', 'S101', 'S104', 'S105', 'S108', 'S109', 'S110', 'S111', 'S113', 'S114', 'S115', 'S116', 'S117', 'S120', 'S121', 'S123', 'S124', 'S127', 'S128', 'S129', 'S132', 'S133', 'S136', 'S138', 'S141', 'S144', 'S147', 'S148', 'S150', 'S152', 'S153', 'S157', 'S158', 'S159', 'S160', 'S161', 'S162', 'S165', 'S167', 'S168', 'S169', 'S173', 'S175', 'S176', 'S177', 'S178', 'S179', 'S182', 'S184', 'S185', 'S187', 'S188', 'S192', 'S193', 'S194', 'S195', 'S196', 'S198', 'S201', 'S202', 'S204']
  diff: round_changed: want=['S182', 'S193'] got=['S001', 'S002', 'S003', 'S004', 'S006', 'S011', 'S013', 'S015', 'S017', 'S020', 'S021', 'S022', 'S024', 'S025', 'S029', 'S030', 'S032', 'S033', 'S034', 'S035', 'S038', 'S041', 'S042', 'S043', 'S044', 'S045', 'S046', 'S051', 'S055', 'S057', 'S058', 'S061', 'S062', 'S063', 'S065', 'S066', 'S067', 'S068', 'S069', 'S070', 'S071', 'S073', 'S077', 'S078', 'S080', 'S081', 'S082', 'S084', 'S086', 'S087', 'S088', 'S090', 'S091', 'S093', 'S096', 'S098', 'S100', 'S104', 'S105', 'S106', 'S107', 'S113', 'S116', 'S121', 'S123', 'S124', 'S125', 'S126', 'S129', 'S133', 'S134', 'S136', 'S137', 'S138', 'S139', 'S140', 'S141', 'S145', 'S149', 'S154', 'S156', 'S157', 'S158', 'S159', 'S161', 'S165', 'S166', 'S168', 'S169', 'S170', 'S171', 'S173', 'S175', 'S178', 'S180', 'S181', 'S182', 'S183', 'S187', 'S189', 'S190', 'S191', 'S192', 'S193', 'S194', 'S196', 'S198', 'S199', 'S201', 'S203', 'S204']
  diff: violations: want=18 got=194
  tool exit=1
C2=unmet
seed=15133620845239658448
```
Full scored counter stderr: empty.
Counter exit 1.

Post-probe byte evidence:
Command: timeout 20 sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J9.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/contract.md
Output:
75849ce2c6ef03d781412608217686bda10ae00a492dfacbec8d6b704b60e6b1  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J9.py
ca65c75984333f1cc442c42438453377d94cb1688f71b116d1e5f3e1c3e74045  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py
302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
d903c67950a081c3e25d19a208f79c84ab6e34f99680acea31d3f8590eaa431a  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/contract.md

Restoration evidence: J9.py has the same pre/post hash and is intentionally retained as the assigned substitute control. C2 and contract bytes have the same pre/post hashes. No original tool was mutated, so no pristine/mutated/restored source trial or mutation-kill claim is made. The initial setup error is not counted as rejection evidence. The valid scored run rejected J9 on 0/24 matched blind histories and the real arm, with exit 1 (full output above).
Freeze provenance: the C1 post-probe hash differs from its pre-score freeze hash. MoriR36 confirmed by direct L1 message that this is the L1's intentional pre-data C1 redesign after K9 and K13 met v1, not a CtlJ9 edit, and that this C2 v1 receipt stands. I stopped additional probes and did not restore the L1's bytes. The C2 counter used here remained unchanged.
Cleanup evidence: read /fast/scratch/hyaku/mori-r36/CtlJ9/ returned only tmp/; read /fast/scratch/hyaku/mori-r36/CtlJ9/tmp/ returned an empty directory. Counter sandbox and clone directories were removed. The bwrap supervisor returned exit 1, ending its private process namespace; no background jobs were started.
Tools installed or updated: none.
VERDICT: J9 unmet exit 1
