measured 2026-10-23T11:59:49Z
control J10 shape label- or id-keyed (QUALITY 99 i)
control_sha256 fe92f448805384651189415415c81af249c4ff8f8418a1798beadac71199cbbc
counter_sha256 302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb

Axes: shape fidelity, CLI fidelity, detector discrimination, containment.
Mutant: current ids with number divisible by 3 enter ids; historical ids divisible by 7 enter deleted; flagged ids divisible by 5 enter superseded. round_changed is the union of row labels at path commits 2, 4, ... after the base. No cells are compared (/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J10.py:45-57; shape requirement: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/contract.md:98).
Expected detector: reject this label/order-only substitute because all four lists must match hidden history truth, including real history (/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/contract.md:23,60-83).

## Scored command and complete counter output

Command, without --seed:
```
timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py 6bd57097 --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J10.py
```
Actual containment wrapper; frozen counter bytes and CLI arguments unchanged:
```
timeout 900 bwrap --ro-bind / / --dev-bind /dev /dev --bind /fast/scratch/hyaku/mori-r36/CtlJ10 /fast/scratch/hyaku/mori-r36 --setenv TMPDIR /fast/scratch/hyaku/mori-r36/tmp timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py 6bd57097 --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J10.py
```
The command exited 1. Complete stdout/stderr follows (artifact://38893:1-86):
```
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J10.py
blind arm: 0/24 sandbox histories matched the hidden truth (3.2s; coverage: deletions=23 changed-back=16 superseded=10)
  repo00 FAIL: lists differ
      want: appendonly_violations=3 ids=[S011,S239] deleted=[S165] superseded=[S239] round_changed=[S011,S165]
      got:  appendonly_violations=6 ids=[S147,S156,S162,S216,S288] deleted=[S147] superseded=[] round_changed=[]
  repo01 FAIL: lists differ
      want: appendonly_violations=2 ids=[S072] deleted=[S118] superseded=[S072] round_changed=[S072]
      got:  appendonly_violations=5 ids=[S069,S072,S288] deleted=[S196,S238] superseded=[] round_changed=[S004,S069,S072,S100,S134,S137,S184,S196,S238,S269,S288,S293]
  repo02 FAIL: lists differ
      want: appendonly_violations=5 ids=[] deleted=[S006,S013,S050,S083,S147] superseded=[] round_changed=[]
      got:  appendonly_violations=7 ids=[S024,S048,S063,S132,S291] deleted=[S063,S147] superseded=[] round_changed=[]
  repo03 FAIL: lists differ
      want: appendonly_violations=2 ids=[] deleted=[S031,S216] superseded=[] round_changed=[S031]
      got:  appendonly_violations=4 ids=[S090] deleted=[S049,S098,S238] superseded=[S090] round_changed=[S001,S049,S090,S098,S118,S146,S193,S209,S236,S238,S250]
  repo04 FAIL: lists differ
      want: appendonly_violations=4 ids=[S118] deleted=[S130,S226,S296] superseded=[S118] round_changed=[S118,S130,S226,S296]
      got:  appendonly_violations=3 ids=[S033,S291] deleted=[S196] superseded=[] round_changed=[S033,S118,S130,S170,S196,S271,S291]
  repo05 FAIL: lists differ
      want: appendonly_violations=2 ids=[] deleted=[S133,S203] superseded=[] round_changed=[S075,S133,S157,S203]
      got:  appendonly_violations=5 ids=[S075,S099,S150] deleted=[S133,S203] superseded=[S075,S150] round_changed=[S047,S075,S133,S150,S155,S157,S187]
  repo06 FAIL: lists differ
      want: appendonly_violations=5 ids=[S125,S265] deleted=[S120,S150,S291] superseded=[S125] round_changed=[S120,S125]
      got:  appendonly_violations=2 ids=[S237] deleted=[S287] superseded=[] round_changed=[S020,S025,S037,S104,S118,S120,S125,S172,S209,S237,S265]
  repo07 FAIL: lists differ
      want: appendonly_violations=2 ids=[S049] deleted=[S091] superseded=[] round_changed=[S049,S109]
      got:  appendonly_violations=8 ids=[S054,S108,S120,S123,S231] deleted=[S049,S091,S231] superseded=[S120] round_changed=[S049,S054,S076,S108,S109,S120,S123,S178,S188,S194,S197,S231,S241,S292]
  repo08 FAIL: lists differ
      want: appendonly_violations=3 ids=[S149] deleted=[S211,S234] superseded=[S149] round_changed=[S234]
      got:  appendonly_violations=2 ids=[S009,S270] deleted=[] superseded=[S270] round_changed=[S009,S052,S080,S086,S149,S270]
  repo09 FAIL: lists differ
      want: appendonly_violations=3 ids=[S139] deleted=[S065,S294] superseded=[S139] round_changed=[S065,S086,S139,S294]
      got:  appendonly_violations=3 ids=[] deleted=[S119,S238,S294] superseded=[] round_changed=[S086,S119,S139,S233,S238,S294]
  repo10 FAIL: lists differ
      want: appendonly_violations=5 ids=[] deleted=[S062,S085,S144,S145,S262] superseded=[] round_changed=[S190,S262]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[S067,S076,S148,S190,S223,S254,S298]
  repo11 FAIL: lists differ
      want: appendonly_violations=2 ids=[S111] deleted=[S100] superseded=[] round_changed=[S016,S111,S167]
      got:  appendonly_violations=3 ids=[S024,S111] deleted=[S119] superseded=[] round_changed=[S013,S016,S024,S111,S119,S167,S274,S299]
  repo12 FAIL: lists differ
      want: appendonly_violations=3 ids=[S241] deleted=[S024,S267] superseded=[S241] round_changed=[]
      got:  appendonly_violations=7 ids=[S045,S063,S084,S138,S213] deleted=[S063,S084] superseded=[S045] round_changed=[S045,S055,S061,S063,S065,S084,S100,S138,S176,S202,S213,S223,S241,S262,S275]
  repo13 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S165] superseded=[] round_changed=[S165]
      got:  appendonly_violations=5 ids=[S060,S084,S150] deleted=[S084,S119] superseded=[S060,S150] round_changed=[]
  repo14 FAIL: lists differ
      want: appendonly_violations=2 ids=[] deleted=[S208,S265] superseded=[] round_changed=[S031,S208]
      got:  appendonly_violations=5 ids=[S075,S090,S276,S285] deleted=[S217] superseded=[S075,S090,S285] round_changed=[S013,S031,S075,S090,S160,S185,S217,S276,S285]
  repo15 FAIL: lists differ
      want: appendonly_violations=3 ids=[S245] deleted=[S083,S264] superseded=[] round_changed=[S051,S245,S259,S264,S298]
      got:  appendonly_violations=3 ids=[S051] deleted=[S245,S259] superseded=[] round_changed=[S017,S037,S041,S051,S059,S122,S179,S212,S227,S245,S259,S264,S298]
  repo16 FAIL: lists differ
      want: appendonly_violations=3 ids=[S103] deleted=[S011,S036] superseded=[S103] round_changed=[S011,S036,S103]
      got:  appendonly_violations=2 ids=[S141,S156] deleted=[] superseded=[] round_changed=[S036,S103,S141,S156,S181,S208,S229,S263]
  repo17 FAIL: lists differ
      want: appendonly_violations=2 ids=[S091] deleted=[S110] superseded=[] round_changed=[S239]
      got:  appendonly_violations=4 ids=[S021] deleted=[S007,S021,S091] superseded=[] round_changed=[S007,S021,S091,S220,S223,S239]
  repo18 FAIL: lists differ
      want: appendonly_violations=4 ids=[S015] deleted=[S005,S059,S232] superseded=[] round_changed=[S015,S059]
      got:  appendonly_violations=5 ids=[S015,S066,S246,S294] deleted=[S294] superseded=[S015] round_changed=[S015,S066,S246,S294]
  repo19 FAIL: lists differ
      want: appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
      got:  appendonly_violations=4 ids=[S114,S192] deleted=[S119,S175] superseded=[] round_changed=[]
  repo20 FAIL: lists differ
      want: appendonly_violations=6 ids=[S037] deleted=[S102,S113,S173,S243,S295] superseded=[S037] round_changed=[S102,S173,S295]
      got:  appendonly_violations=2 ids=[S117] deleted=[S140] superseded=[] round_changed=[S037,S117,S140,S173,S209,S295]
  repo21 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S298] superseded=[] round_changed=[S005]
      got:  appendonly_violations=4 ids=[S072,S108,S291] deleted=[S238] superseded=[] round_changed=[]
  repo22 FAIL: lists differ
      want: appendonly_violations=7 ids=[S205,S240] deleted=[S076,S080,S249,S266,S274] superseded=[S205] round_changed=[S205,S240,S249,S266]
      got:  appendonly_violations=3 ids=[S240] deleted=[S182,S266] superseded=[S240] round_changed=[S067,S095,S169,S182,S205,S240,S249]
  repo23 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S048] superseded=[] round_changed=[S048,S085]
      got:  appendonly_violations=3 ids=[S024,S210] deleted=[S210] superseded=[S210] round_changed=[]
real arm: FAIL (2.7s)
  tool:   appendonly_violations=97 ids=[S003,S006,S009,S012,S015,S018,S021,S024,S027,S030,S033,S036,S039,S042,S045,S048,S051,S054,S057,S060,S063,S066,S069,S072,S075,S078,S081,S084,S087,S090,S093,S096,S099,S102,S105,S108,S111,S114,S117,S120,S123,S126,S129,S132,S135,S138,S141,S144,S147,S150,S153,S156,S159,S162,S165,S168,S171,S174,S177,S180,S183,S186,S189,S192,S195,S198,S201,S204] deleted=[S007,S014,S021,S028,S035,S042,S049,S056,S063,S070,S077,S084,S091,S098,S105,S112,S119,S126,S133,S140,S147,S154,S161,S168,S175,S182,S189,S196,S203] superseded=[S015,S030,S045,S060,S075,S090,S105,S120,S135,S150,S165,S180,S195] round_changed=[S001,S002,S003,S004,S005,S006,S007,S008,S009,S010,S011,S012,S013,S014,S015,S016,S017,S018,S019,S020,S021,S022,S023,S024,S025,S026,S027,S028,S029,S030,S031,S032,S033,S034,S035,S036,S037,S038,S039,S040,S041,S042,S043,S044,S045,S046,S047,S048,S049,S050,S051,S052,S053,S054,S055,S056,S057,S058,S059,S060,S061,S062,S063,S064,S065,S066,S067,S068,S069,S070,S071,S072,S073,S074,S075,S076,S077,S078,S079,S080,S081,S082,S083,S084,S085,S086,S087,S088,S089,S090,S091,S092,S093,S094,S095,S096,S097,S098,S099,S100,S101,S102,S103,S104,S105,S106,S107,S108,S109,S110,S111,S112,S113,S114,S115,S116,S117,S118,S119,S120,S121,S122,S123,S124,S125,S126,S127,S128,S129,S130,S131,S132,S133,S134,S135,S136,S137,S138,S139,S140,S141,S142,S143,S144,S145,S146,S147,S148,S149,S150,S151,S152,S153,S154,S155,S156,S157,S158,S159,S160,S161,S162,S163,S164,S165,S166,S167,S168,S169,S170,S171,S172,S173,S174,S175,S176,S177,S178,S179,S180,S181,S182,S183,S184,S185,S186,S187,S188,S189,S190,S191,S192,S193,S194,S195,S196,S197,S198,S199,S200,S201,S202,S203,S204]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  diff: ids: want=['S041', 'S044', 'S051', 'S062', 'S064', 'S069', 'S179', 'S180', 'S181', 'S182', 'S183', 'S184', 'S185', 'S186', 'S188', 'S189', 'S190', 'S193'] got=['S003', 'S006', 'S009', 'S012', 'S015', 'S018', 'S021', 'S024', 'S027', 'S030', 'S033', 'S036', 'S039', 'S042', 'S045', 'S048', 'S051', 'S054', 'S057', 'S060', 'S063', 'S066', 'S069', 'S072', 'S075', 'S078', 'S081', 'S084', 'S087', 'S090', 'S093', 'S096', 'S099', 'S102', 'S105', 'S108', 'S111', 'S114', 'S117', 'S120', 'S123', 'S126', 'S129', 'S132', 'S135', 'S138', 'S141', 'S144', 'S147', 'S150', 'S153', 'S156', 'S159', 'S162', 'S165', 'S168', 'S171', 'S174', 'S177', 'S180', 'S183', 'S186', 'S189', 'S192', 'S195', 'S198', 'S201', 'S204']
  diff: deleted: want=[] got=['S007', 'S014', 'S021', 'S028', 'S035', 'S042', 'S049', 'S056', 'S063', 'S070', 'S077', 'S084', 'S091', 'S098', 'S105', 'S112', 'S119', 'S126', 'S133', 'S140', 'S147', 'S154', 'S161', 'S168', 'S175', 'S182', 'S189', 'S196', 'S203']
  diff: superseded: want=['S069', 'S182', 'S193'] got=['S015', 'S030', 'S045', 'S060', 'S075', 'S090', 'S105', 'S120', 'S135', 'S150', 'S165', 'S180', 'S195']
  diff: round_changed: want=['S182', 'S193'] got=['S001', 'S002', 'S003', 'S004', 'S005', 'S006', 'S007', 'S008', 'S009', 'S010', 'S011', 'S012', 'S013', 'S014', 'S015', 'S016', 'S017', 'S018', 'S019', 'S020', 'S021', 'S022', 'S023', 'S024', 'S025', 'S026', 'S027', 'S028', 'S029', 'S030', 'S031', 'S032', 'S033', 'S034', 'S035', 'S036', 'S037', 'S038', 'S039', 'S040', 'S041', 'S042', 'S043', 'S044', 'S045', 'S046', 'S047', 'S048', 'S049', 'S050', 'S051', 'S052', 'S053', 'S054', 'S055', 'S056', 'S057', 'S058', 'S059', 'S060', 'S061', 'S062', 'S063', 'S064', 'S065', 'S066', 'S067', 'S068', 'S069', 'S070', 'S071', 'S072', 'S073', 'S074', 'S075', 'S076', 'S077', 'S078', 'S079', 'S080', 'S081', 'S082', 'S083', 'S084', 'S085', 'S086', 'S087', 'S088', 'S089', 'S090', 'S091', 'S092', 'S093', 'S094', 'S095', 'S096', 'S097', 'S098', 'S099', 'S100', 'S101', 'S102', 'S103', 'S104', 'S105', 'S106', 'S107', 'S108', 'S109', 'S110', 'S111', 'S112', 'S113', 'S114', 'S115', 'S116', 'S117', 'S118', 'S119', 'S120', 'S121', 'S122', 'S123', 'S124', 'S125', 'S126', 'S127', 'S128', 'S129', 'S130', 'S131', 'S132', 'S133', 'S134', 'S135', 'S136', 'S137', 'S138', 'S139', 'S140', 'S141', 'S142', 'S143', 'S144', 'S145', 'S146', 'S147', 'S148', 'S149', 'S150', 'S151', 'S152', 'S153', 'S154', 'S155', 'S156', 'S157', 'S158', 'S159', 'S160', 'S161', 'S162', 'S163', 'S164', 'S165', 'S166', 'S167', 'S168', 'S169', 'S170', 'S171', 'S172', 'S173', 'S174', 'S175', 'S176', 'S177', 'S178', 'S179', 'S180', 'S181', 'S182', 'S183', 'S184', 'S185', 'S186', 'S187', 'S188', 'S189', 'S190', 'S191', 'S192', 'S193', 'S194', 'S195', 'S196', 'S197', 'S198', 'S199', 'S200', 'S201', 'S202', 'S203', 'S204']
  diff: violations: want=18 got=97
  tool exit=1
C2=unmet
seed=16452666225485966171
```
VERDICT: J10 unmet exit 1

The control was rejected: 0/24 blind histories matched and the real arm failed (output above). This is not a killed-source-mutant claim: the pristine tool is absent, so the pristine/mutated/restored source-mutation classification is inconclusive.

## Pristine and restored detector receipts

Both use the same wrapper above with the --tool argument removed, at revision 6bd57097.
Pristine output, exit 1:
```
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool_absent
C2=unmet
seed=15897183447645914355
```
Restored output, exit 1:
```
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool_absent
C2=unmet
seed=6517510179672195018
```
An earlier containment setup attempt omitted --dev-bind /dev /dev and exited 2 before scoring. Its complete output was:
```
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
counter setup error: git rev-parse --verify 6bd57097^{commit} failed in /home/vgpnk/Projects/shokunin/mori-shokunin: fatal: could not open '/dev/null' for reading and writing: Permission denied
```
That setup failure is inconclusive, not a rejected mutant; the subsequent scored run used the corrected wrapper shown above.

## Hash and restoration evidence

Before scoring and after scoring, timeout 120 sha256sum on the four paths below produced identical output:
```
fe92f448805384651189415415c81af249c4ff8f8418a1798beadac71199cbbc  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J10.py
d903c67950a081c3e25d19a208f79c84ab6e34f99680acea31d3f8590eaa431a  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/contract.md
ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py
302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
```
Both counter hashes matched the required freeze before scoring (/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/evidence/freeze.txt:2-4). No original tool or counter bytes were overwritten: this probe used a separate --tool file, and both original-revision runs reported tool_absent (receipts above).

L1 authorized the frozen counter's own transient clone writes, including packs over 10 MB (agent://MoriR36, containment ruling received before scoring). The bwrap bind confined them to the seat scratch; the counter removes its scratch and tool directories in finally blocks (/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py:715-718).
After the detector runs, read /fast/scratch/hyaku/mori-r36/CtlJ10 listed only tmp/. Then timeout 120 rmdir /fast/scratch/hyaku/mori-r36/CtlJ10/tmp /fast/scratch/hyaku/mori-r36/CtlJ10 exited 0 with no output, establishing that both directories were empty and removed. All detector commands completed in the foreground; none timed out.
Capacity preflight: timeout 120 df -h /fast reported 70G available, 92% used, before the counter clone. Existing sandbox binary: timeout 120 which bwrap returned /usr/bin/bwrap. Tool installs or updates: none.
