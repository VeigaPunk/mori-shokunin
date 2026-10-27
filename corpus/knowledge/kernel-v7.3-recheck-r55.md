# Linux v7.2 citation pointers rechecked at v7.3 (round 55)

source: S526 S527 S528 S529 S530 S531 S532 S533 S534 S516 S502
verified-at: 2026-10-27
recheck: on-release — re-open each pinned v7.2/v7.3 source pair and re-derive the frozen pointer scope; lines and status are mechanically checked by count-c1.py.

## Pointer ledger

| hash | entry | pointer | v7.3 source | v7.3 lines | status | disposition |
|---|---|---|---|---|---|---|
| `7b2d297eec60` | corpus/knowledge/oom-tracepoints-r47.md | `include/trace/events/oom.h:12,34` | S528 | 12,34 | same | holds |
| `909839af93ac` | corpus/knowledge/oom-tracepoints-r47.md | `fs/proc/base.c:1158` | S526 | 1158 | same | holds |
| `b50f210b822a` | corpus/knowledge/oom-tracepoints-r47.md | `mm/page_alloc.c:4630` | S527 | 4689 | moved | holds |
| `72ea8dae3688` | corpus/knowledge/oom-tracepoints-r47.md | `mm/oom_kill.c:774` | S516 | 774 | same | holds |
| `ee326a28c54f` | corpus/knowledge/oom-tracepoints-r47.md | `mm/oom_kill.c:673` | S516 | 673 | same | holds |
| `441f0b4099e5` | corpus/knowledge/oom-tracepoints-r47.md | `mm/oom_kill.c:582` | S516 | 582 | same | holds |
| `46fdbd52a22f` | corpus/knowledge/oom-tracepoints-r47.md | `mm/oom_kill.c:595` | S516 | 595 | same | holds |
| `1c11a3f36bf3` | corpus/knowledge/oom-tracepoints-r47.md | `mm/oom_kill.c:567,578` | S516 | 567,578 | same | holds |
| `db108c1ad61c` | corpus/knowledge/oom-tracepoints-r47.md | `mm/page_alloc.c:4265` | S527 | 4311 | moved | holds |
| `c9f1c6e1a950` | corpus/knowledge/oom-tracepoints-r47.md | `include/trace/events/oom.h:105` | S528 | 105 | same | holds |
| `c6be347a84e3` | corpus/knowledge/oom-tracepoints-r47.md | `mm/oom_kill.c:751-775` | S516 | 751-775 | same | holds |
| `d42ca4c96d7f` | corpus/knowledge/oom-tracepoints-r47.md | `mm/oom_kill.c:656-674` | S516 | 656-674 | same | holds |
| `301bfba80d7d` | corpus/knowledge/oom-tracepoints-r47.md | `mm/oom_kill.c:562-599` | S516 | 562-599 | same | holds |
| `5d7ff106d1ab` | corpus/knowledge/system-pressure-r24.md | `Documentation/accounting/psi.rst:60-65` | S529 | 60-65 | same | holds |
| `ea75ed04d3da` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:342-360,408-411,551,572` | S530 | 342-360,408-411,551,572 | same | holds |
| `7a851b9d617d` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:1268-1270` | S530 | 1268-1270 | same | holds |
| `d568cd9dcd32` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:1372-1373` | S530 | 1372-1373 | same | holds |
| `ccaf95f97c2a` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:1379-1380` | S530 | 1379-1380 | same | holds |
| `0d7523eee480` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:1712` | S530 | 1712 | same | holds |
| `2547b0838a9b` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:1017` | S530 | 1017 | same | holds |
| `901c19ca0925` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:1540,1545,1550` | S530 | 1540,1545,1550 | same | holds |
| `49a5b3e454cd` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:1686` | S530 | 1686 | same | holds |
| `b43c5ba94e6e` | corpus/knowledge/system-pressure-r24.md | `Documentation/accounting/psi.rst:36-38` | S529 | 36-38 | same | holds |
| `0e16bb6f5925` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:1710-1721` | S530 | 1710-1721 | same | holds |
| `f701e7773747` | corpus/knowledge/system-pressure-r24.md | `Documentation/accounting/psi.rst:40-43` | S529 | 40-43 | same | holds |
| `57c24f3d7024` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:1290-1296` | S530 | 1290-1296 | same | holds |
| `d2836bd245d1` | corpus/knowledge/system-pressure-r24.md | `Documentation/accounting/psi.rst:45-56` | S529 | 45-56 | same | holds |
| `079fc0192229` | corpus/knowledge/system-pressure-r24.md | `Documentation/accounting/psi.rst:57-59` | S529 | 57-59 | same | holds |
| `037f662ce719` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:1282-1288` | S530 | 1282-1288 | same | holds |
| `4d36e9bc2eef` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:1540,1545,1550,1686` | S530 | 1540,1545,1550,1686 | same | holds |
| `0ee301f4c8ae` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:1284-1288` | S530 | 1284-1288 | same | holds |
| `b049eb15da6e` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:342-360` | S530 | 342-360 | same | holds |
| `cf580afc5628` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:160-164` | S530 | 160-164 | same | holds |
| `c63a3852c4f7` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:1268` | S530 | 1268 | same | holds |
| `3ba4ca51577f` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:1269-1270` | S530 | 1269-1270 | same | holds |
| `14238678b995` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:600-602` | S530 | 600-602 | same | holds |
| `3b2c0c15134d` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:1273-1296` | S530 | 1273-1296 | same | holds |
| `2b9148b31cd6` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:1032-1042` | S530 | 1032-1042 | same | holds |
| `9422468b8e8f` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:1364-1367` | S530 | 1364-1367 | same | holds |
| `e828a0db4c5f` | corpus/knowledge/system-pressure-r24.md | `include/linux/psi_types.h:41-49,57-70` | S531 | 41-49,57-70 | same | holds |
| `a0d9bf2a5096` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:1717-1719` | S530 | 1717-1719 | same | holds |
| `ee7308fa713e` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:1260-1263` | S530 | 1260-1263 | same | holds |
| `77e3ebacc391` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:1257-1258` | S530 | 1257-1258 | same | holds |
| `864abdf951ac` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:228-240` | S530 | 228-240 | same | holds |
| `5c4886b1e126` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:149-158` | S530 | 149-158 | same | holds |
| `dcc8749c4c9c` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:1553-1566` | S530 | 1553-1566 | same | holds |
| `d71526aeb0fc` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:1711-1719` | S530 | 1711-1719 | same | holds |
| `eee4454705c0` | corpus/knowledge/system-pressure-r24.md | `Documentation/admin-guide/kernel-parameters.txt:5505-5507` | S532 | 5540-5542 | moved | holds |
| `8386d1267a7c` | corpus/knowledge/system-pressure-r24.md | `Documentation/accounting/psi.rst:67-88` | S529 | 67-88 | same | holds |
| `400c6cd157cb` | corpus/knowledge/system-pressure-r24.md | `Documentation/accounting/psi.rst:102-104` | S529 | 102-104 | same | holds |
| `b7c369d84995` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:167` | S530 | 167 | same | holds |
| `905a72e0bfd9` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:1596-1598` | S530 | 1596-1598 | same | holds |
| `6078f2d783e3` | corpus/knowledge/system-pressure-r24.md | `Documentation/accounting/psi.rst:178-187` | S529 | 178-187 | same | holds |
| `1c3dad2ad6e2` | corpus/knowledge/system-pressure-r24.md | `Documentation/admin-guide/cgroup-v2.rst:1066-1081` | S533 | 1066-1081 | same | holds |
| `1490a683aca7` | corpus/knowledge/system-pressure-r24.md | `Documentation/admin-guide/cgroup-v2.rst:1083-1087` | S533 | 1083-1087 | same | holds |
| `edd8b8c361b4` | corpus/knowledge/system-pressure-r24.md | `Documentation/admin-guide/cgroup-v2.rst:1215-1221` | S533 | 1240-1246 | moved | holds |
| `02b8d2d11094` | corpus/knowledge/system-pressure-r24.md | `Documentation/admin-guide/cgroup-v2.rst:1911-1915` | S533 | 1938-1942 | changed | holds |
| `77bd396cffd3` | corpus/knowledge/system-pressure-r24.md | `Documentation/admin-guide/cgroup-v2.rst:2171-2175` | S533 | 2202-2206 | changed | holds |
| `c4dba1eb36cf` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:408-410` | S530 | 408-410 | same | holds |
| `a3f8d244205e` | corpus/knowledge/system-pressure-r24.md | `Documentation/accounting/psi.rst:70-88` | S529 | 70-88 | same | holds |
| `a6e5226259c9` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:845-857` | S530 | 845-857 | same | holds |
| `0124918d278a` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:551,1269-1270` | S530 | 551,1269-1270 | same | holds |
| `6f9f1d32ac46` | corpus/knowledge/system-pressure-r24.md | `kernel/sched/psi.c:1538-1550` | S530 | 1538-1550 | same | holds |
| `68afd0d6fa2f` | corpus/knowledge/system-pressure-r24.md | `Documentation/admin-guide/cgroup-v2.rst:1066-1087` | S533 | 1066-1087 | same | holds |
| `0527161c4edd` | corpus/knowledge/oom-victim-selection-r27.md | `fs/proc/base.c:597` | S526 | 597 | same | holds |
| `82952b5a6ec2` | corpus/knowledge/oom-victim-selection-r27.md | `mm/oom_kill.c:228-229` | S516 | 228-229 | same | holds |
| `2ba00a976118` | corpus/knowledge/oom-victim-selection-r27.md | `mm/oom_kill.c:160-167` | S516 | 160-167 | same | holds |
| `d0338d4263b9` | corpus/knowledge/oom-victim-selection-r27.md | `fs/proc/base.c:583-599` | S526 | 583-599 | same | holds |
| `bfb67ed4f174` | corpus/knowledge/oom-victim-selection-r27.md | `fs/proc/base.c:596-599` | S526 | 596-599 | same | holds |
| `53875978a00b` | corpus/knowledge/oom-victim-selection-r27.md | `mm/oom_kill.c:226-235` | S516 | 226-235 | same | holds |
| `531bf618617a` | corpus/knowledge/oom-victim-selection-r27.md | `mm/oom_kill.c:102-103` | S516 | 102-103 | same | holds |
| `9a8d29e96280` | corpus/knowledge/oom-victim-selection-r27.md | `Documentation/filesystems/proc.rst:1811-1812` | S502 | 1812-1813 | moved | holds |
| `07a985363937` | corpus/knowledge/oom-victim-selection-r27.md | `Documentation/admin-guide/cgroup-v2.rst:1450-1466` | S533 | 1477-1493 | moved | holds |
| `617f9a677bd9` | corpus/knowledge/oom-victim-selection-r27.md | `mm/oom_kill.c:998-1006,1040-1053` | S516 | 998-1006,1040-1053 | same | holds |
| `4eea9d9f5ae5` | corpus/knowledge/oom-victim-selection-r27.md | `kernel/fork.c:1768-1769,1949-1966` | S534 | 1795-1796,1976-1993 | moved | holds |
| `3b61086e4467` | corpus/knowledge/oom-victim-selection-r27.md | `fs/proc/base.c:1131-1133` | S526 | 1131-1133 | same | holds |
| `9dc189629a14` | corpus/knowledge/oom-victim-selection-r27.md | `fs/proc/base.c:1275-1279` | S526 | 1275-1279 | same | holds |
| `64dc96352472` | corpus/knowledge/oom-victim-selection-r27.md | `mm/oom_kill.c:228-234,340-348,358-376` | S516 | 228-234,340-348,358-376 | same | holds |
