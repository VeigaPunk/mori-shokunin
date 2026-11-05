# Reading user-namespace runway, and detecting the writes that take it away

source: S629 — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/sysctl/user.rst — docs, tier A, Documentation/admin-guide/sysctl/user.rst at tag v7.2 (intro, max_user_namespaces), committed copy `corpus/evidence/sources-r98/S629-user.rst`, opened 2026-11-05
source: S630 — https://man7.org/linux/man-pages/man2/unshare.2.html — docs, tier A, unshare(2) ERRORS (ENOSPC), Linux man-pages 6.19 (2026-02-08), committed copy `corpus/evidence/sources-r98/S630-unshare.2.html`, opened 2026-11-05
source: S631 — https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/proc_ns.h — code, tier A, include/linux/proc_ns.h at tag v7.2 (PROC_USER_INIT_INO), committed copy `corpus/evidence/sources-r98/S631-proc_ns.h`, opened 2026-11-05
source: S632 — https://raw.githubusercontent.com/torvalds/linux/v7.2/include/uapi/linux/nsfs.h — code, tier A, include/uapi/linux/nsfs.h at tag v7.2 (USER_NS_INIT_INO), committed copy `corpus/evidence/sources-r98/S632-nsfs.h`, opened 2026-11-05
verified-at: 2026-11-05
recheck: on-release — `python3 tools/mori-userns-runway.py --selftest`; at the next kernel tag fetch the four paths (S629, S631, S632 from raw.githubusercontent.com/torvalds/linux/<tag>/, S630 from man7.org) and compare with the committed copies; the host runs 7.2.11
coverage-map: resource runway (user namespaces — new ground at round 98, read by `tools/mori-userns-runway.py`)

On 2026-11-05 wave seats set `user.max_user_namespaces` to 0 with sudo; from then until the limit was restored,
every bwrap sandbox on the host failed with ENOSPC. The lane had no reading of this resource. The kernel keeps a
per-user count of user namespaces in every user namespace, and `/proc/sys/user/max_user_namespaces` is the limit
for the namespace the reader runs in. When creating one more would cross the limit, `unshare`/`clone` with
`CLONE_NEWUSER` fail with ENOSPC. A limit of 0 therefore refuses every new user namespace, which is what every
bwrap sandbox needs. `tools/mori-userns-runway.py` reads the limit and the namespaces visible on process links and
reports runway. It also scans the sudo command log for kernel-tunable writes, so the cause of the next incident is
named with a timestamp instead of found by hand.

## Claims

| claim | source | quote |
|---|---|---|
| The files in /proc/sys/user set per-user, per-user-namespace limits on how many namespaces and similar objects can be created. | S629 | `The files in this directory can be used to override the default limits on the number of namespaces and other objects that have per user per user namespace limits.` |
| max_user_namespaces is the per-user cap on user namespaces created inside the reader's current user namespace. | S629 | `The maximum number of user namespaces that any user in the current user namespace may create.` |
| A creation is charged to the creating user in its own namespace and is checked against that namespace's limit. | S629 | `The creation of per user per user namespace objects are charged to the user in the user namespace who created the object and` |
| The charge also goes to the users who created each enclosing user namespace, so nested namespaces count toward the outer limit. | S629 | `The creation of objects is also charged to all of the users who created user namespaces the creation of the object happens` |
| Hitting the /proc/sys/user limit when creating a user namespace fails with ENOSPC (since Linux 4.9). | S630 | `doing so would have caused the limit defined by the corresponding file in /proc/sys/user to be exceeded.` |
| The kernel names the initial user namespace's inode PROC_USER_INIT_INO, defined as USER_NS_INIT_INO. | S631 | `PROC_USER_INIT_INO	= USER_NS_INIT_INO,` |
| USER_NS_INIT_INO is 0xEFFFFFFD, which is 4026531837 in decimal, the `user:[4026531837]` link the host's own processes show. | S632 | `USER_NS_INIT_INO	= 0xEFFFFFFDU,` |

## Reading rules (mori)

| reading | tool verdict | what it means | what it does not mean |
|---|---|---|---|
| limit = 0 | `state=exhausted`, exit 1 | no new user namespace can be created in this namespace; bwrap/unshare -U fail with ENOSPC | not a count problem: nothing has to be "in use" for this to bite |
| runway = 0, limit > 0 | `state=exhausted`, exit 1 | the visible count has reached the limit | the true count can be higher (see lower bound) |
| runway < low (default 32) | `state=low`, exit 1 | a few more sandboxes and spawns will fail | not a fault yet |
| runway >= low | `state=ok`, exit 0 | room on the visible count | not proof of room: `used_lb` is a lower bound |
| limit missing/unparsable, no process entries | `USERNS_RUNWAY_SETUP`, exit 2 | the reading failed: fail closed | never read as limit 0 or as ok |
| `SYSCTL_WRITE ... key=user.max_user_namespaces value=0` | scan exit 1, `userns_zero` counts it | a sudo-logged command set the limit to 0 at that timestamp | not proof the write succeeded (the log records the command, not its result); read the limit to confirm |

Lower bound: `used_lb` counts distinct non-initial inodes on readable `/proc/<pid>/ns/user` links. Namespaces held
only by an open file descriptor or a bind mount have no process link. Links of other users' processes are
unreadable to a non-root reader and are counted as `unreadable`, not as namespaces. The limit is per user, so
another user's namespaces do not consume this user's runway in the same namespace. They only matter when they
enclose the creation (claim 4).

Error signature to match: ENOSPC (`No space left on device`) from `unshare -U` or `clone(CLONE_NEWUSER)` while the
disk has room (claim 5). Here ENOSPC is about the namespace limit, not disk space: read
`tools/mori-userns-runway.py` before `df`. The exact bwrap message text was not captured this round.

## Observed (2026-11-05, this host, read-only)

- Live read (non-root, initial namespace): `USERNS_RUNWAY limit=122865 used_lb=7 pids=3828 unreadable=3527
  runway=122858 low=32 state=ok`, exit 0. 122865 = threads-max/2 (threads-max 245730), the value the orchestrator
  restored.
- Incident scan (`.ufo/waves/round-98/evidence/journal-incident-r98.txt`, the 276 sudo command lines between 05:14
  and 05:43 -03): `SYSCTL_WRITES n=6 keys=1 userns_zero=2`, the writes at 05:14:52 (0), 05:14:54 (10000), 05:16:04
  (15638, twice: `sysctl key=value` without `-w` is also a write), 05:22:02 (0), 05:42:18 (122865). The two
  `sysctl -a` reads in the window are not counted.

## Limits and boundaries

- Detection and report only. The tool never writes a sysctl, never creates or destroys a namespace, and never
  restores a value. Restoring host configuration belongs to the operator; repairing OS state belongs to tsukuroi.
- The write scan sees only commands sudo logged. A root shell that writes `/proc/sys` directly, or a write through
  a systemd unit, leaves no `COMMAND=` line and is not seen.
- The default `low` threshold (32) is the lane's choice, not a kernel value.
