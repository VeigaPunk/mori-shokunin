measured 2026-10-23T12:00:34Z
control J3 shape generic rows
control_sha256 d639aa1f90c48e712a4c259047b0c1632b8d86a1dbfe770d34b7fdde96008467
counter_sha256 302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb

Axes: shape fidelity, frozen-counter integrity, containment.
The substitute reads ids at the requested revision, sorts them, copies them into ids,
superseded and round_changed, sets deleted=[] and exits 1; no history is consulted
(.ufo/waves/round-36/c0/controls/J3.py:24-26,54-60).
Expected detector: C2=unmet, exit 1; exact-list comparisons reject generic ids
(.ufo/waves/round-36/count-c2.py:517-522,608-611,720-723).

Freeze verification before scoring: command timeout 120 sha256sum on both counter paths
and contract.md under .ufo/waves/round-36; output:
```text
ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145  count-c1.py
302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb  count-c2.py
d903c67950a081c3e25d19a208f79c84ab6e34f99680acea31d3f8590eaa431a  contract.md
```
These match evidence/freeze.txt:2-4; no mismatch.

Scored command (no --seed):
```text
timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py 6bd57097 --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J3.py
```
Full counter stdout:
```text
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J3.py
blind arm: 0/24 sandbox histories matched the hidden truth (2.3s; coverage: deletions=22 changed-back=15 superseded=9)
  repo00 FAIL: lists differ
      want: appendonly_violations=5 ids=[S216,S282] deleted=[S058,S225,S278] superseded=[S216,S282] round_changed=[S058,S278]
      got:  appendonly_violations=9 ids=[S038,S049,S130,S214,S216,S218,S232,S247,S282] deleted=[] superseded=[S038,S049,S130,S214,S216,S218,S232,S247,S282] round_changed=[S038,S049,S130,S214,S216,S218,S232,S247,S282]
  repo01 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S271] superseded=[] round_changed=[S216]
      got:  appendonly_violations=10 ids=[S057,S152,S164,S165,S181,S216,S226,S239,S264,S282] deleted=[] superseded=[S057,S152,S164,S165,S181,S216,S226,S239,S264,S282] round_changed=[S057,S152,S164,S165,S181,S216,S226,S239,S264,S282]
  repo02 FAIL: lists differ
      want: appendonly_violations=3 ids=[] deleted=[S074,S075,S258] superseded=[] round_changed=[S074]
      got:  appendonly_violations=3 ids=[S006,S042,S236] deleted=[] superseded=[S006,S042,S236] round_changed=[S006,S042,S236]
  repo03 FAIL: lists differ
      want: appendonly_violations=5 ids=[S206,S264] deleted=[S103,S150,S230] superseded=[] round_changed=[S134,S150,S206,S230,S264]
      got:  appendonly_violations=7 ids=[S088,S134,S145,S167,S206,S264,S280] deleted=[] superseded=[S088,S134,S145,S167,S206,S264,S280] round_changed=[S088,S134,S145,S167,S206,S264,S280]
  repo04 FAIL: lists differ
      want: appendonly_violations=3 ids=[S055,S146] deleted=[S089] superseded=[S146] round_changed=[S055]
      got:  appendonly_violations=9 ids=[S055,S061,S091,S118,S146,S159,S197,S240,S280] deleted=[] superseded=[S055,S061,S091,S118,S146,S159,S197,S240,S280] round_changed=[S055,S061,S091,S118,S146,S159,S197,S240,S280]
  repo05 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S276] superseded=[] round_changed=[S065]
      got:  appendonly_violations=11 ids=[S002,S065,S076,S096,S106,S107,S135,S195,S257,S272,S287] deleted=[] superseded=[S002,S065,S076,S096,S106,S107,S135,S195,S257,S272,S287] round_changed=[S002,S065,S076,S096,S106,S107,S135,S195,S257,S272,S287]
  repo06 FAIL: lists differ
      want: appendonly_violations=4 ids=[S135] deleted=[S018,S069,S100] superseded=[S135] round_changed=[S018,S069]
      got:  appendonly_violations=9 ids=[S111,S135,S154,S155,S160,S173,S198,S226,S261] deleted=[] superseded=[S111,S135,S154,S155,S160,S173,S198,S226,S261] round_changed=[S111,S135,S154,S155,S160,S173,S198,S226,S261]
  repo07 FAIL: lists differ
      want: appendonly_violations=2 ids=[] deleted=[S142,S268] superseded=[] round_changed=[S142]
      got:  appendonly_violations=12 ids=[S029,S030,S034,S061,S069,S085,S130,S186,S198,S217,S286,S297] deleted=[] superseded=[S029,S030,S034,S061,S069,S085,S130,S186,S198,S217,S286,S297] round_changed=[S029,S030,S034,S061,S069,S085,S130,S186,S198,S217,S286,S297]
  repo08 FAIL: lists differ
      want: appendonly_violations=2 ids=[S299] deleted=[S242] superseded=[S299] round_changed=[S114]
      got:  appendonly_violations=12 ids=[S029,S108,S114,S115,S139,S155,S189,S229,S257,S265,S295,S299] deleted=[] superseded=[S029,S108,S114,S115,S139,S155,S189,S229,S257,S265,S295,S299] round_changed=[S029,S108,S114,S115,S139,S155,S189,S229,S257,S265,S295,S299]
  repo09 FAIL: lists differ
      want: appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[S171]
      got:  appendonly_violations=12 ids=[S026,S032,S043,S097,S104,S123,S126,S155,S171,S180,S196,S241] deleted=[] superseded=[S026,S032,S043,S097,S104,S123,S126,S155,S171,S180,S196,S241] round_changed=[S026,S032,S043,S097,S104,S123,S126,S155,S171,S180,S196,S241]
  repo10 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S263] superseded=[] round_changed=[S263]
      got:  appendonly_violations=14 ids=[S028,S110,S132,S133,S137,S153,S196,S212,S233,S240,S247,S274,S283,S294] deleted=[] superseded=[S028,S110,S132,S133,S137,S153,S196,S212,S233,S240,S247,S274,S283,S294] round_changed=[S028,S110,S132,S133,S137,S153,S196,S212,S233,S240,S247,S274,S283,S294]
  repo11 FAIL: lists differ
      want: appendonly_violations=3 ids=[S207,S248] deleted=[S265] superseded=[] round_changed=[S107,S207,S248]
      got:  appendonly_violations=5 ids=[S004,S107,S207,S248,S298] deleted=[] superseded=[S004,S107,S207,S248,S298] round_changed=[S004,S107,S207,S248,S298]
  repo12 FAIL: lists differ
      want: appendonly_violations=4 ids=[S231,S269] deleted=[S021,S209] superseded=[S231,S269] round_changed=[S183,S231]
      got:  appendonly_violations=15 ids=[S008,S031,S042,S058,S162,S183,S189,S199,S203,S222,S226,S231,S238,S248,S269] deleted=[] superseded=[S008,S031,S042,S058,S162,S183,S189,S199,S203,S222,S226,S231,S238,S248,S269] round_changed=[S008,S031,S042,S058,S162,S183,S189,S199,S203,S222,S226,S231,S238,S248,S269]
  repo13 FAIL: lists differ
      want: appendonly_violations=4 ids=[S035,S180] deleted=[S085,S174] superseded=[] round_changed=[S085,S174,S180]
      got:  appendonly_violations=11 ids=[S027,S035,S087,S104,S119,S158,S180,S247,S263,S281,S291] deleted=[] superseded=[S027,S035,S087,S104,S119,S158,S180,S247,S263,S281,S291] round_changed=[S027,S035,S087,S104,S119,S158,S180,S247,S263,S281,S291]
  repo14 FAIL: lists differ
      want: appendonly_violations=5 ids=[S275] deleted=[S049,S188,S228,S289] superseded=[] round_changed=[S049,S188,S228,S275,S289]
      got:  appendonly_violations=8 ids=[S012,S077,S080,S150,S185,S213,S251,S275] deleted=[] superseded=[S012,S077,S080,S150,S185,S213,S251,S275] round_changed=[S012,S077,S080,S150,S185,S213,S251,S275]
  repo15 FAIL: lists differ
      want: appendonly_violations=3 ids=[S083] deleted=[S198,S237] superseded=[] round_changed=[S083,S198,S267]
      got:  appendonly_violations=6 ids=[S054,S083,S163,S188,S267,S274] deleted=[] superseded=[S054,S083,S163,S188,S267,S274] round_changed=[S054,S083,S163,S188,S267,S274]
  repo16 FAIL: lists differ
      want: appendonly_violations=4 ids=[S093] deleted=[S032,S122,S231] superseded=[S093] round_changed=[S032,S098,S231]
      got:  appendonly_violations=9 ids=[S018,S020,S035,S054,S093,S098,S216,S279,S285] deleted=[] superseded=[S018,S020,S035,S054,S093,S098,S216,S279,S285] round_changed=[S018,S020,S035,S054,S093,S098,S216,S279,S285]
  repo17 FAIL: lists differ
      want: appendonly_violations=4 ids=[S005,S099] deleted=[S161,S289] superseded=[] round_changed=[S005,S053,S099,S289]
      got:  appendonly_violations=4 ids=[S005,S053,S099,S253] deleted=[] superseded=[S005,S053,S099,S253] round_changed=[S005,S053,S099,S253]
  repo18 FAIL: lists differ
      want: appendonly_violations=4 ids=[S219] deleted=[S055,S237,S262] superseded=[] round_changed=[S237,S262]
      got:  appendonly_violations=5 ids=[S058,S117,S219,S228,S229] deleted=[] superseded=[S058,S117,S219,S228,S229] round_changed=[S058,S117,S219,S228,S229]
  repo19 FAIL: lists differ
      want: appendonly_violations=2 ids=[S048,S160] deleted=[] superseded=[S048] round_changed=[S017,S160]
      got:  appendonly_violations=10 ids=[S017,S048,S116,S160,S164,S173,S214,S220,S230,S258] deleted=[] superseded=[S017,S048,S116,S160,S164,S173,S214,S220,S230,S258] round_changed=[S017,S048,S116,S160,S164,S173,S214,S220,S230,S258]
  repo20 FAIL: lists differ
      want: appendonly_violations=5 ids=[S192,S247] deleted=[S132,S135,S256] superseded=[S192] round_changed=[S247,S256]
      got:  appendonly_violations=11 ids=[S020,S022,S031,S049,S097,S109,S116,S140,S177,S192,S247] deleted=[] superseded=[S020,S022,S031,S049,S097,S109,S116,S140,S177,S192,S247] round_changed=[S020,S022,S031,S049,S097,S109,S116,S140,S177,S192,S247]
  repo21 FAIL: lists differ
      want: appendonly_violations=5 ids=[S039,S136,S255] deleted=[S150,S275] superseded=[S136,S255] round_changed=[S001,S039,S136,S150,S255,S275]
      got:  appendonly_violations=12 ids=[S001,S039,S100,S127,S131,S136,S142,S164,S204,S208,S222,S255] deleted=[] superseded=[S001,S039,S100,S127,S131,S136,S142,S164,S204,S208,S222,S255] round_changed=[S001,S039,S100,S127,S131,S136,S142,S164,S204,S208,S222,S255]
  repo22 FAIL: lists differ
      want: appendonly_violations=6 ids=[S171,S288] deleted=[S076,S128,S160,S239] superseded=[] round_changed=[S076,S160,S171,S288]
      got:  appendonly_violations=8 ids=[S063,S095,S158,S171,S193,S216,S231,S288] deleted=[] superseded=[S063,S095,S158,S171,S193,S216,S231,S288] round_changed=[S063,S095,S158,S171,S193,S216,S231,S288]
  repo23 FAIL: lists differ
      want: appendonly_violations=2 ids=[] deleted=[S107,S158] superseded=[] round_changed=[]
      got:  appendonly_violations=7 ids=[S055,S153,S200,S217,S235,S248,S296] deleted=[] superseded=[S055,S153,S200,S217,S235,S248,S296] round_changed=[S055,S153,S200,S217,S235,S248,S296]
real arm: FAIL (2.3s)
  tool:   appendonly_violations=204 ids=[S001,S002,S003,S004,S005,S006,S007,S008,S009,S010,S011,S012,S013,S014,S015,S016,S017,S018,S019,S020,S021,S022,S023,S024,S025,S026,S027,S028,S029,S030,S031,S032,S033,S034,S035,S036,S037,S038,S039,S040,S041,S042,S043,S044,S045,S046,S047,S048,S049,S050,S051,S052,S053,S054,S055,S056,S057,S058,S059,S060,S061,S062,S063,S064,S065,S066,S067,S068,S069,S070,S071,S072,S073,S074,S075,S076,S077,S078,S079,S080,S081,S082,S083,S084,S085,S086,S087,S088,S089,S090,S091,S092,S093,S094,S095,S096,S097,S098,S099,S100,S101,S102,S103,S104,S105,S106,S107,S108,S109,S110,S111,S112,S113,S114,S115,S116,S117,S118,S119,S120,S121,S122,S123,S124,S125,S126,S127,S128,S129,S130,S131,S132,S133,S134,S135,S136,S137,S138,S139,S140,S141,S142,S143,S144,S145,S146,S147,S148,S149,S150,S151,S152,S153,S154,S155,S156,S157,S158,S159,S160,S161,S162,S163,S164,S165,S166,S167,S168,S169,S170,S171,S172,S173,S174,S175,S176,S177,S178,S179,S180,S181,S182,S183,S184,S185,S186,S187,S188,S189,S190,S191,S192,S193,S194,S195,S196,S197,S198,S199,S200,S201,S202,S203,S204] deleted=[] superseded=[S001,S002,S003,S004,S005,S006,S007,S008,S009,S010,S011,S012,S013,S014,S015,S016,S017,S018,S019,S020,S021,S022,S023,S024,S025,S026,S027,S028,S029,S030,S031,S032,S033,S034,S035,S036,S037,S038,S039,S040,S041,S042,S043,S044,S045,S046,S047,S048,S049,S050,S051,S052,S053,S054,S055,S056,S057,S058,S059,S060,S061,S062,S063,S064,S065,S066,S067,S068,S069,S070,S071,S072,S073,S074,S075,S076,S077,S078,S079,S080,S081,S082,S083,S084,S085,S086,S087,S088,S089,S090,S091,S092,S093,S094,S095,S096,S097,S098,S099,S100,S101,S102,S103,S104,S105,S106,S107,S108,S109,S110,S111,S112,S113,S114,S115,S116,S117,S118,S119,S120,S121,S122,S123,S124,S125,S126,S127,S128,S129,S130,S131,S132,S133,S134,S135,S136,S137,S138,S139,S140,S141,S142,S143,S144,S145,S146,S147,S148,S149,S150,S151,S152,S153,S154,S155,S156,S157,S158,S159,S160,S161,S162,S163,S164,S165,S166,S167,S168,S169,S170,S171,S172,S173,S174,S175,S176,S177,S178,S179,S180,S181,S182,S183,S184,S185,S186,S187,S188,S189,S190,S191,S192,S193,S194,S195,S196,S197,S198,S199,S200,S201,S202,S203,S204] round_changed=[S001,S002,S003,S004,S005,S006,S007,S008,S009,S010,S011,S012,S013,S014,S015,S016,S017,S018,S019,S020,S021,S022,S023,S024,S025,S026,S027,S028,S029,S030,S031,S032,S033,S034,S035,S036,S037,S038,S039,S040,S041,S042,S043,S044,S045,S046,S047,S048,S049,S050,S051,S052,S053,S054,S055,S056,S057,S058,S059,S060,S061,S062,S063,S064,S065,S066,S067,S068,S069,S070,S071,S072,S073,S074,S075,S076,S077,S078,S079,S080,S081,S082,S083,S084,S085,S086,S087,S088,S089,S090,S091,S092,S093,S094,S095,S096,S097,S098,S099,S100,S101,S102,S103,S104,S105,S106,S107,S108,S109,S110,S111,S112,S113,S114,S115,S116,S117,S118,S119,S120,S121,S122,S123,S124,S125,S126,S127,S128,S129,S130,S131,S132,S133,S134,S135,S136,S137,S138,S139,S140,S141,S142,S143,S144,S145,S146,S147,S148,S149,S150,S151,S152,S153,S154,S155,S156,S157,S158,S159,S160,S161,S162,S163,S164,S165,S166,S167,S168,S169,S170,S171,S172,S173,S174,S175,S176,S177,S178,S179,S180,S181,S182,S183,S184,S185,S186,S187,S188,S189,S190,S191,S192,S193,S194,S195,S196,S197,S198,S199,S200,S201,S202,S203,S204]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  diff: ids: want=['S041', 'S044', 'S051', 'S062', 'S064', 'S069', 'S179', 'S180', 'S181', 'S182', 'S183', 'S184', 'S185', 'S186', 'S188', 'S189', 'S190', 'S193'] got=['S001', 'S002', 'S003', 'S004', 'S005', 'S006', 'S007', 'S008', 'S009', 'S010', 'S011', 'S012', 'S013', 'S014', 'S015', 'S016', 'S017', 'S018', 'S019', 'S020', 'S021', 'S022', 'S023', 'S024', 'S025', 'S026', 'S027', 'S028', 'S029', 'S030', 'S031', 'S032', 'S033', 'S034', 'S035', 'S036', 'S037', 'S038', 'S039', 'S040', 'S041', 'S042', 'S043', 'S044', 'S045', 'S046', 'S047', 'S048', 'S049', 'S050', 'S051', 'S052', 'S053', 'S054', 'S055', 'S056', 'S057', 'S058', 'S059', 'S060', 'S061', 'S062', 'S063', 'S064', 'S065', 'S066', 'S067', 'S068', 'S069', 'S070', 'S071', 'S072', 'S073', 'S074', 'S075', 'S076', 'S077', 'S078', 'S079', 'S080', 'S081', 'S082', 'S083', 'S084', 'S085', 'S086', 'S087', 'S088', 'S089', 'S090', 'S091', 'S092', 'S093', 'S094', 'S095', 'S096', 'S097', 'S098', 'S099', 'S100', 'S101', 'S102', 'S103', 'S104', 'S105', 'S106', 'S107', 'S108', 'S109', 'S110', 'S111', 'S112', 'S113', 'S114', 'S115', 'S116', 'S117', 'S118', 'S119', 'S120', 'S121', 'S122', 'S123', 'S124', 'S125', 'S126', 'S127', 'S128', 'S129', 'S130', 'S131', 'S132', 'S133', 'S134', 'S135', 'S136', 'S137', 'S138', 'S139', 'S140', 'S141', 'S142', 'S143', 'S144', 'S145', 'S146', 'S147', 'S148', 'S149', 'S150', 'S151', 'S152', 'S153', 'S154', 'S155', 'S156', 'S157', 'S158', 'S159', 'S160', 'S161', 'S162', 'S163', 'S164', 'S165', 'S166', 'S167', 'S168', 'S169', 'S170', 'S171', 'S172', 'S173', 'S174', 'S175', 'S176', 'S177', 'S178', 'S179', 'S180', 'S181', 'S182', 'S183', 'S184', 'S185', 'S186', 'S187', 'S188', 'S189', 'S190', 'S191', 'S192', 'S193', 'S194', 'S195', 'S196', 'S197', 'S198', 'S199', 'S200', 'S201', 'S202', 'S203', 'S204']
  diff: superseded: want=['S069', 'S182', 'S193'] got=['S001', 'S002', 'S003', 'S004', 'S005', 'S006', 'S007', 'S008', 'S009', 'S010', 'S011', 'S012', 'S013', 'S014', 'S015', 'S016', 'S017', 'S018', 'S019', 'S020', 'S021', 'S022', 'S023', 'S024', 'S025', 'S026', 'S027', 'S028', 'S029', 'S030', 'S031', 'S032', 'S033', 'S034', 'S035', 'S036', 'S037', 'S038', 'S039', 'S040', 'S041', 'S042', 'S043', 'S044', 'S045', 'S046', 'S047', 'S048', 'S049', 'S050', 'S051', 'S052', 'S053', 'S054', 'S055', 'S056', 'S057', 'S058', 'S059', 'S060', 'S061', 'S062', 'S063', 'S064', 'S065', 'S066', 'S067', 'S068', 'S069', 'S070', 'S071', 'S072', 'S073', 'S074', 'S075', 'S076', 'S077', 'S078', 'S079', 'S080', 'S081', 'S082', 'S083', 'S084', 'S085', 'S086', 'S087', 'S088', 'S089', 'S090', 'S091', 'S092', 'S093', 'S094', 'S095', 'S096', 'S097', 'S098', 'S099', 'S100', 'S101', 'S102', 'S103', 'S104', 'S105', 'S106', 'S107', 'S108', 'S109', 'S110', 'S111', 'S112', 'S113', 'S114', 'S115', 'S116', 'S117', 'S118', 'S119', 'S120', 'S121', 'S122', 'S123', 'S124', 'S125', 'S126', 'S127', 'S128', 'S129', 'S130', 'S131', 'S132', 'S133', 'S134', 'S135', 'S136', 'S137', 'S138', 'S139', 'S140', 'S141', 'S142', 'S143', 'S144', 'S145', 'S146', 'S147', 'S148', 'S149', 'S150', 'S151', 'S152', 'S153', 'S154', 'S155', 'S156', 'S157', 'S158', 'S159', 'S160', 'S161', 'S162', 'S163', 'S164', 'S165', 'S166', 'S167', 'S168', 'S169', 'S170', 'S171', 'S172', 'S173', 'S174', 'S175', 'S176', 'S177', 'S178', 'S179', 'S180', 'S181', 'S182', 'S183', 'S184', 'S185', 'S186', 'S187', 'S188', 'S189', 'S190', 'S191', 'S192', 'S193', 'S194', 'S195', 'S196', 'S197', 'S198', 'S199', 'S200', 'S201', 'S202', 'S203', 'S204']
  diff: round_changed: want=['S182', 'S193'] got=['S001', 'S002', 'S003', 'S004', 'S005', 'S006', 'S007', 'S008', 'S009', 'S010', 'S011', 'S012', 'S013', 'S014', 'S015', 'S016', 'S017', 'S018', 'S019', 'S020', 'S021', 'S022', 'S023', 'S024', 'S025', 'S026', 'S027', 'S028', 'S029', 'S030', 'S031', 'S032', 'S033', 'S034', 'S035', 'S036', 'S037', 'S038', 'S039', 'S040', 'S041', 'S042', 'S043', 'S044', 'S045', 'S046', 'S047', 'S048', 'S049', 'S050', 'S051', 'S052', 'S053', 'S054', 'S055', 'S056', 'S057', 'S058', 'S059', 'S060', 'S061', 'S062', 'S063', 'S064', 'S065', 'S066', 'S067', 'S068', 'S069', 'S070', 'S071', 'S072', 'S073', 'S074', 'S075', 'S076', 'S077', 'S078', 'S079', 'S080', 'S081', 'S082', 'S083', 'S084', 'S085', 'S086', 'S087', 'S088', 'S089', 'S090', 'S091', 'S092', 'S093', 'S094', 'S095', 'S096', 'S097', 'S098', 'S099', 'S100', 'S101', 'S102', 'S103', 'S104', 'S105', 'S106', 'S107', 'S108', 'S109', 'S110', 'S111', 'S112', 'S113', 'S114', 'S115', 'S116', 'S117', 'S118', 'S119', 'S120', 'S121', 'S122', 'S123', 'S124', 'S125', 'S126', 'S127', 'S128', 'S129', 'S130', 'S131', 'S132', 'S133', 'S134', 'S135', 'S136', 'S137', 'S138', 'S139', 'S140', 'S141', 'S142', 'S143', 'S144', 'S145', 'S146', 'S147', 'S148', 'S149', 'S150', 'S151', 'S152', 'S153', 'S154', 'S155', 'S156', 'S157', 'S158', 'S159', 'S160', 'S161', 'S162', 'S163', 'S164', 'S165', 'S166', 'S167', 'S168', 'S169', 'S170', 'S171', 'S172', 'S173', 'S174', 'S175', 'S176', 'S177', 'S178', 'S179', 'S180', 'S181', 'S182', 'S183', 'S184', 'S185', 'S186', 'S187', 'S188', 'S189', 'S190', 'S191', 'S192', 'S193', 'S194', 'S195', 'S196', 'S197', 'S198', 'S199', 'S200', 'S201', 'S202', 'S203', 'S204']
  diff: violations: want=18 got=204
  tool exit=1
C2=unmet
seed=11746362866300023066
```
Counter stderr: empty.
Counter exit code: 1.

Pristine detector command (TMPDIR=/fast/scratch/hyaku/mori-r36/CtlJ3):
```text
timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py 6bd57097
```
Full pristine output:
```text
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool_absent
C2=unmet
seed=12509186477027806848
EXIT=1
```
Pristine stderr: empty.
Restored selection uses the same pristine command and unchanged source bytes:
```text
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool_absent
C2=unmet
seed=12364518884780500954
EXIT=1
```
Restored stderr: empty.
Mutation-probe classification: inconclusive, not killed or survived: the pristine
program is absent at 6bd57097 and already fails. The substitute control itself is
rejected (scored stdout above: blind 0/24; real FAIL; C2=unmet).

Restoration evidence: only the requested new control and this report were authored;
no original target, frozen counter or contract bytes were edited. The requested
control is retained. Before and after timeout 120 sha256sum outputs were identical:
```text
d639aa1f90c48e712a4c259047b0c1632b8d86a1dbfe770d34b7fdde96008467  c0/controls/J3.py
ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145  count-c1.py
302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb  count-c2.py
d903c67950a081c3e25d19a208f79c84ab6e34f99680acea31d3f8590eaa431a  contract.md
```
L1 MoriR36 authorized the unmodified frozen counter's self-cleaning transient scratch
and clone writes in its reply to the containment question. Authored paths stayed scoped.
All subprocess calls were synchronous and bounded with timeout; all returned.
Tool installs or updates: none.

VERDICT: J3 unmet exit 1
