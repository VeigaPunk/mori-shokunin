# CriticInheritProbe — round 27 wave 1, C1 inheritance and self-raise probe

Seat: MoriR27.CriticInheritProbe (critic, leaf). Access date 2026-10-22. Host kernel `7.2.11-arch1-1` (`uname -r`).
Scratch: `/fast/scratch/hyaku/mori-r27/LabratInherit/` (probe scripts, raw outputs, fetched sources).
Tool installs or updates: none.

## Verdict

| Hypothesis | Result | Predicting source line |
|---|---|---|
| H1: a child inherits its parent's `oom_score_adj` across fork and execve | **held** (default 200 and a raised 300 both carried into `sh`, `cat` and `python3` children, and across a bare `exec python3`) | `kernel/fork.c:1768-1769` (fork); no write in `fs/exec.c` (execve); `fs/proc/base.c:1155` is the only writer |
| H2a: an unprivileged process can raise its own `oom_score_adj` | **held** (200 to 500 accepted, `oom_score` 800 to 1000) | `fs/proc/base.c:1131-1135` (only a value below the floor is refused) |
| H2b: it cannot lower it back below the value it had | **refuted as worded** (writing 0 fails with EACCES, but writing 200 and then 199, below the original 200, both succeed; the floor is an inherited `oom_score_adj_min` of 100, not the original value) | `fs/proc/base.c:1131-1133` (floor check) and `:1156-1157` (only a CAP_SYS_RESOURCE writer moves the floor) |

**Main counterexample:** the assigned check for H2b (write 0 after 500, see EACCES) passes on this host, but only
because 0 is below the inherited floor of 100. Writing 199, below the original 200, succeeds. So the kernel's rule for
`oom_score_adj` is not a ratchet. It is "never below `oom_score_adj_min`", and an unprivileged write never moves
that floor. The ratchet does exist, but only on the legacy `/proc/<pid>/oom_adj` interface (`base.c:1118-1120`),
which the probe also confirmed (see the section below on the legacy interface).

## Privilege state of the probe (precondition)

```
$ [ "$(id -u)" = 0 ] && echo uid_is_root || echo uid_not_root
uid_not_root
$ grep -E '^Cap(Eff|Prm|Amb)' /proc/self/status
CapPrm:	0000000000000000
CapEff:	0000000000000000
CapAmb:	0000000000000000
```

With CapEff 0, `capable(CAP_SYS_RESOURCE)` at `base.c:1132` is false, so the unprivileged branch is the one exercised.

## Commands and outputs

Script `probe.sh` (sha256 `6a1be8c9338758f5ef3a09b8a296f296eb60b4036f7f11f4f646d38a050cbb80`) plus errno helper
`pywrite.py` (sha256 `5af8baa660074937be77de38cc13d722d9aa32b65f7380b8d3ab89ea6b886ada`, a single `os.write`,
printing `errno.errorcode`). It touches only a `sh` it starts and a `sleep 30 &` it starts. It checks that
`/proc/<pid>/comm` is `sleep` before every write and before the kill, and it prints no pid. `/bin/sh` is
`/usr/bin/bash` (`readlink -f /bin/sh`). Command: `sh probe.sh`. Output file `probe-output.txt`, sha256
`fe3768e7de7c7e2753c8107bce024d639a9b85cbe00802656ed27df967b42091`. The output is shown verbatim below:

```
== H1 default carrier
parent_shell_adj=200                 # cat /proc/$$/oom_score_adj
sh_child_adj=200                     # sh -c 'cat /proc/self/oom_score_adj'
py_child_adj=200                     # python3 -c 'print(open("/proc/self/oom_score_adj").read().strip())'
== H1 non-default carrier (a sh this script starts raises itself to 300)
carrier_self=300                     # echo 300 > /proc/self/oom_score_adj inside that sh
carrier_sh_child=300
carrier_py_child=300
carrier_after_execve_python=300      # exec python3 ... (same process, new image)
== H2
sleep_orig_adj=200 sleep_orig_score=800
shell_write_500_rc=0                 # echo 500 > /proc/<sleep>/oom_score_adj
after500_adj=500 after500_score=1000
probe.sh: line 28: echo: write error: Permission denied
shell_write_0_rc=1                   # echo 0 > /proc/<sleep>/oom_score_adj
after_write0_adj=500 after_write0_score=1000
py_write_0: errno=13 EACCES Permission denied adj=500
py_write_orig: ok adj=200            # 500 -> 200 (back to original)
py_write_orig_minus_1(199): ok adj=199   # below the original: accepted
py_write_minus_1000: errno=13 EACCES Permission denied adj=199
py_write_1001: errno=22 EINVAL Invalid argument adj=199
lowest_accepted_adj(=inherited oom_score_adj_min)=100   # bisection from 1000 each step
sleep_wait_status=143                # 128+15: SIGTERM from kill, my own sleep
sleep_still_present=no
```

(`#` annotations were added here and are not in the raw file.) The "carrier" control matters. A uniform default of 200
everywhere cannot tell inheritance apart from a host-wide default. The raised 300 can, and it survives fork, fork+exec
and a bare execve.

### Legacy interface (extra falsifier, same bounds)

Script `legacy.sh` (sha256 `b23e2cc03d9832d28808812cddb12136dbd04fcfddd668f84c3e98edb43709d1`). Command:
`sh legacy.sh`. Output file `legacy-output.txt`, sha256
`e6e25989a49413d18f6724181f775ceb3344f5069f777a58695c8b9f2f3228e0`:

```
start adj=200 oom_adj=3
legacy_write_5: ok adj=294 oom_adj=4
legacy_write_4: errno=13 EACCES Permission denied adj=294
new_iface_write_235: ok adj=235
sleep_wait_status=143
```

Writing legacy 4 maps to 235 (`base.c:1229`). It is refused because 235 is below the current value 294, even though
235 is well above the floor of 100 (`base.c:1118-1120`). The same 235 through `oom_score_adj` is accepted. Reading
back legacy 5 gives 4 because of the integer scaling in `oom_adj_read` (`base.c:1097-1098`).

An earlier inline one-liner of `legacy.sh` aborted at its own `comm` guard because `$!` was empty. It made no write and
sent no signal. If it did start a `sleep`, that sleep exits by itself after 30 s [INFERENCE].

## Kernel and systemd lines that predict the results (all fetched 2026-10-22 with curl, HTTP 200)

| File (pinned URL) | sha256 of bytes | Line: verbatim quote (25 words or fewer) |
|---|---|---|
| https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c | `cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6` | 1131: `if ((short)oom_adj < task->signal->oom_score_adj_min &&` ; 1132: `!capable(CAP_SYS_RESOURCE)) {` ; 1133: `err = -EACCES;` |
| same | same | 1155: `task->signal->oom_score_adj = oom_adj;` ; 1156: `if (!legacy && has_capability_noaudit(current, CAP_SYS_RESOURCE))` ; 1157: `task->signal->oom_score_adj_min = (short)oom_adj;` |
| same | same | 1118: `if (oom_adj < task->signal->oom_score_adj &&` (legacy `oom_adj` path: true ratchet against the current value) |
| same | same | 1275: `if (oom_score_adj < OOM_SCORE_ADJ_MIN \|\|` ; 1277: `err = -EINVAL;` (the 1001 write) |
| same | same | 597: `points = (1000 + badness * 1000 / (long)totalpages) * 2 / 3;` (the `oom_score` shown) |
| same | same | 3353: `REG("oom_score_adj", S_IRUGO\|S_IWUSR, proc_oom_score_adj_operations),` (owner-writable, so a same-user write to my own sleep is allowed) |
| https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/fork.c | `359882ea981b58f5289293e5644f7c0085a8350e4f1937f39dcb94ae1cd0dd1d` | 1768: `sig->oom_score_adj = current->signal->oom_score_adj;` ; 1769: `sig->oom_score_adj_min = current->signal->oom_score_adj_min;` (inside `copy_signal`, line 1721) |
| same | same | 1955: `if ((clone_flags & (CLONE_VM \| CLONE_THREAD \| CLONE_VFORK)) != CLONE_VM)` ; 1963-1964 re-copy both fields for shared-mm children |
| https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/exec.c | `44e4185bf9332d86a2fd6bbe33c22cdd0b5129521499b703058813d2106572c7` | `grep -n oom fs_exec.c` gives only 62: `#include <linux/oom.h>` and a comment at 129. No assignment exists, so execve keeps the signal struct's values (this is a claim from an absence) |
| https://raw.githubusercontent.com/systemd/systemd/v262/units/user@.service.in | `72c2f40dcfced1d85bcc17583715966fc8a552b68af44404c213de2ea320504c` | 35: `OOMScoreAdjust=100` |
| https://raw.githubusercontent.com/systemd/systemd/v262/src/core/main.c | `5ecdca43a8e0ed088758b228b54c72df311c0b9dc3855721ed02c5b169d3aae3` | 3055: `if (getuid() == 0)` ; 3063: `b = saturate_add(a, 100, OOM_SCORE_ADJ_MAX);` |
| https://raw.githubusercontent.com/systemd/systemd/v262/NEWS | `a494f0389edd09702a90d1540c7e21c0af5a4d29a4d020855ca3062d885a7657` | 9736-9737: `For per-user service managers this now defaults to 100` (systemd 250 section, which starts at line 9634) |

How the source predicts each observation:

- **H1.** `copy_signal` copies both `oom_score_adj` and `oom_score_adj_min` into the child's new signal struct
  (fork.c:1768-1769). `fs/exec.c` never writes either field. So both the value and the floor carry through fork and
  execve. The probe observed this for the value. The floor is observed indirectly: the bisection found 100 on a
  `sleep` that inherits through three generations below the user manager.
- **H2.** The `oom_score_adj` write path refuses only values below `oom_score_adj_min` when the writer lacks
  CAP_SYS_RESOURCE (base.c:1131-1133). On success it updates `oom_score_adj` (1155) but updates the floor only if the
  writer has CAP_SYS_RESOURCE (1156-1157). An unprivileged raise therefore leaves the floor where it was, and the
  process may come back down to it.
- **Where 200 and 100 come from on this host.** PID 1 (root, privileged) starts `user@.service` with
  `OOMScoreAdjust=100`. Because PID 1 holds the capability, that write also sets the floor to 100. The user manager
  (non-root) then gives its own children its own value plus 100 (main.c:3055, 3063), which is 200. That write is
  unprivileged, so the floor stays at 100. Observed ancestor chain of this probe's shell, as process classes only:

```
$ p=$$; walk PPid to 1, print class and /proc/<p>/oom_score_adj (no pids printed)
depth=0 class=omp adj=200
depth=1 class=bash adj=200
depth=2..4 class=other adj=200
depth=5 class=systemd adj=100
depth=6 class=init adj=0
$ grep -c -E '^\s*DefaultOOMScoreAdjust' /etc/systemd/user.conf /etc/systemd/user.conf.d/*.conf
/etc/systemd/user.conf:0
/etc/systemd/user.conf.d/99-omarchy-nofile.conf:0      # key absent (presence check only), so the +100 default applies
```

- **`oom_score` values.** For a `sleep` with negligible memory, `oom_badness` is dominated by
  `oom_score_adj * totalpages / 1000` [INFERENCE: `oom_badness` lives in `mm/oom_kill.c`, row S003, which this seat
  did not open]. base.c:597 then gives about (1000 + adj) * 2 / 3: 800 at adj 200 and 1000 at adj 500, which matches
  the observed 800 and 1000.

## Findings for the C1 entry and the SKILL.md Round27 table (critic)

1. **False-ratchet risk (calibration, depth).** An entry or decision row saying "an unprivileged process can raise
   but never lower its `oom_score_adj`" would be false on this host. Correct statement: "unprivileged writes may go
   anywhere from `oom_score_adj_min` up to 1000. The floor is inherited across fork and execve and moves only on a
   CAP_SYS_RESOURCE write. Only the legacy `oom_adj` file ratchets against the current value." Evidence: the H2 output
   (199 accepted) and base.c:1118 versus base.c:1131.
2. **False-provenance risk (systemd NEWS versus code).** NEWS line 9737 says the per-user default "defaults to 100".
   The v262 code computes the manager's own value plus 100 (main.c:3063), and this host observes 200 for user
   services. A row that cites NEWS alone would mis-predict the fleet's value. Cite main.c:3063 together with
   user@.service.in:35.
3. **Fleet attribution (depth).** Every fleet runtime that runs under the user manager inherits 200 with floor 100,
   unless something along its chain rewrote it. One omp-class process (this probe's shell ancestor) was observed at
   200. System services run at 0 (PID 1 observed 0). So, all else equal, both the kernel and any scorer that reads
   `oom_score` rank user-session processes, which include the fleet, about 200 points of adj ahead of system
   services. [INFERENCE for fleet processes other than the observed chain, and for earlyoom's use of `oom_score`; the
   kill.c and main.c scouts own that part.]
4. **Precondition to state in the entry.** The results hold for writers without CAP_SYS_RESOURCE (CapEff 0 observed).
   A privileged writer can go below the floor and also moves it (base.c:1132, 1156).

## SOURCES rows (S127+ candidates)

The lane holds no row for any file this seat opened (`corpus/SOURCES.md` lists S003 for `mm/oom_kill.c` and S005 for
`oom.h`, but nothing for `fs/proc/base.c`, `kernel/fork.c`, `fs/exec.c`, or systemd `units/user@.service.in`,
`src/core/main.c` or `NEWS`). Each file is therefore a new row, not an anchor on an existing one. The peer
`MoriR27.SrcProcBaseOomScore` probably drafts the `fs/proc/base.c` row. The L1 should merge the base.c anchors above
into that single row rather than open two rows for one file. Ready-to-paste anchors:

```
fs/proc/base.c@v7.2 sha256 cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6 anchors 597,1118-1120,1131-1133,1155-1157,1229,1275-1277,3353
kernel/fork.c@v7.2  sha256 359882ea981b58f5289293e5644f7c0085a8350e4f1937f39dcb94ae1cd0dd1d anchors 1721,1768-1769,1949-1965
fs/exec.c@v7.2      sha256 44e4185bf9332d86a2fd6bbe33c22cdd0b5129521499b703058813d2106572c7 anchors 62,129 (no oom_score_adj write)
systemd v262 units/user@.service.in sha256 72c2f40dcfced1d85bcc17583715966fc8a552b68af44404c213de2ea320504c anchor 35
systemd v262 src/core/main.c sha256 5ecdca43a8e0ed088758b228b54c72df311c0b9dc3855721ed02c5b169d3aae3 anchors 3045-3070
systemd v262 NEWS sha256 a494f0389edd09702a90d1540c7e21c0af5a4d29a4d020855ca3062d885a7657 anchors 9733-9740
```

## Smallest safe correction

Change H2's second clause to "cannot lower it below its inherited `oom_score_adj_min` (100 here); it can return to,
and go below, the value it had." Pin it with the 199-accepted line rather than the 0-refused line. The 0-refused line
cannot tell the ratchet model apart from the floor model on this host.

## Bounds kept

The probe touched only a `sh` and two `sleep` processes this seat started. One SIGTERM went to each started sleep
(`wait` status 143). It printed and recorded no pid, uid, command line, journal text, settings value or
`/etc/default/earlyoom` value. Writes went only to scratch and this report. It ran no jj or git mutations and changed
no units.
