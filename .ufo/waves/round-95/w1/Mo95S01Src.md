# Mo95S01Src — round 95 w1 scout: source verification for S626 / S627 (C2 sandbox mechanism)

Seat: `Mo95S01Src` (scout). Wave: `w1`, round 95 attempt 1. Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Entering lane HEAD: `754f4991198c16ddd1d4a3ea9206cfb7d74d6827`. Frozen commit: `2dc476d7fdb68bf916685a9f217a92047662baeb`.
Claim under source: **C2 operability (capability)** — the lane's counting surface runs with the account home
directory absent (user namespace + mount namespace + tmpfs over the home directory).

**Verdict: SOURCES-READY** — both pages opened (HTTP 200), both quotes located, all quote counts = 1.

---

## 1. Duplicate sweep (run BEFORE any fetch)

Command (exact form from the seat item):

```
grep -nE 'man7.org/linux/man-pages/man1/unshare|man7.org/linux/man-pages/man7/user_namespaces|man7.org/linux/man-pages/man7/mount_namespaces' \
  /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
```

Output: **empty** (no matches, exit 1). Neither S626 nor S627 nor the `mount_namespaces(7)` page is already in the
registry — confirmed also by id scan:

```
$ grep -nE '^\|?\s*S62[67]\b' corpus/SOURCES.md  →  none
$ grep -oE '^\|? ?S[0-9]{3}' corpus/SOURCES.md | grep -oE 'S[0-9]{3}' | sort -u | tail -5
S621
S622
S623
S624
S625
```

Highest registry id is **S625**, so **S626** and **S627** are free. A broader sweep
(`grep -niE 'unshare|user_namespaces|mount_namespaces' corpus/SOURCES.md` and a `grep -rlniE` over `corpus/`) also
returned no matches — no page of this trio appears anywhere in the corpus, so no row already carries this claim.

**Per the seat item I did NOT append anything to `corpus/SOURCES.md`** — the L1 does the append. The row content
below is offered for the L1 only.

## 2. Fetch ledger (both sources, HTTP status / bytes / sha256 / access date)

Scratch: `S="${HYAKU_SCRATCH:-/fast/scratch/hyaku}/mori-r95/Mo95S01Src"` (created; deleted before yield).

```
$ date -u '+%Y-%m-%dT%H:%M:%SZ'   → 2026-11-05T11:03:30Z   (fetch window; re-confirmed 2026-11-05T11:03:32Z)

$ curl -fsSL -o "$S/unshare.1.html" -w 'A http=%{http_code} bytes=%{size_download} url=%{url_effective}\n' \
    https://man7.org/linux/man-pages/man1/unshare.1.html
A http=200 bytes=38193 url=https://man7.org/linux/man-pages/man1/unshare.1.html

$ curl -fsSL -o "$S/user_namespaces.7.html" -w 'B http=%{http_code} bytes=%{size_download} url=%{url_effective}\n' \
    https://man7.org/linux/man-pages/man7/user_namespaces.7.html
B http=200 bytes=59987 url=https://man7.org/linux/man-pages/man7/user_namespaces.7.html
```

Full sha256 (the values to copy into the registry rows):

| row | page | bytes | sha256 (full) |
|---|---|---|---|
| S626 | https://man7.org/linux/man-pages/man1/unshare.1.html | 38193 | `1df4f95f877112743581e8b0900ce1296dbc6155619f7b88232e076f27b7375e` |
| S627 | https://man7.org/linux/man-pages/man7/user_namespaces.7.html | 59987 | `276480f2185f65ee9ca1402c233a53780dd558a77bcc30127bbb5bfafb1301b4` |

Freshness: each page was fetched **twice** and the two copies are byte-identical (`cmp` exit 0 both times), so the
digests above are stable, not a one-off response:

```
A byte-identical across 2 fetches
B byte-identical across 2 fetches
1df4f95f877112743581e8b0900ce1296dbc6155619f7b88232e076f27b7375e  unshare.1.html
1df4f95f877112743581e8b0900ce1296dbc6155619f7b88232e076f27b7375e  unshare.1.html.2
276480f2185f65ee9ca1402c233a53780dd558a77bcc30127bbb5bfafb1301b4  user_namespaces.7.html
276480f2185f65ee9ca1402c233a53780dd558a77bcc30127bbb5bfafb1301b4  user_namespaces.7.html.2
```

Tag stripping: `python3` `html.parser` script (`$S/strip.py`), whitespace-normalised to one space so that a quote
spanning a line wrap in the man page's `<pre>` block is a contiguous string. Text copies (scratch only, **not**
committed): `unshare.1.txt` sha256 `e7188599a857750fc5f688fa7129898f286a46dd4fc30904132534aa0db36a96`,
`user_namespaces.7.txt` sha256 `6956caad3f994110e42906767c992cb643b37c359391384c2d859e2bf3f4f83f`.

## 3. Page revision / version strings shown on the pages

* **Source A (unshare(1))** — man page version string in the page footline (HTML line 637):
  `util-linux 2.43.devel-1062-f... 2026-08-03                     UNSHARE(1)`.
  Colophon: page obtained from the util-linux upstream Git repository on **2026-08-04** (most recent commit found
  **2026-08-03**); "HTML rendering created **2026-09-09** by Michael Kerrisk".
* **Source B (user_namespaces(7))** — man page version string in the page footline:
  `Linux man-pages 6.19 2026-02-08 user_namespaces(7)`.
  Colophon: obtained from the tarball **man-pages-6.19.tar.gz** fetched **2026-09-09**; "HTML rendering created
  2026-09-09".

Access date for both: **2026-11-05** (UTC, confirmed with `date -u` above).

## 4. Quote A — `unshare(1)` (S626 candidate)

Anchor: **OPTIONS** section, `id="OPTIONS"` (HTML line 147; the `<pre>` body spans lines 147–437).

### Quote A-1 — `-r, --map-root-user` maps the current user to root in the new user namespace

* HTML: `<b>-r</b>, <b>--map-root-user</b>` at line **341**; quote body at HTML lines **342–343**
  (`group IDs have been mapped to the superuser UID and GID in the` / `newly created user namespace.`) — grep -n -F
  confirms line 343.
* Visible text (whitespace-normalised): lines **287–291**.
* **Quote (22 words):** "the current effective user and group IDs have been mapped to the superuser UID and GID in the newly created user namespace"
* **Occurrences in visible text: 1** (normalised-string count over the whole stripped page).
* Verbatim context (visible text lines 288–292):

  ```
        -r, --map-root-user
         Run the program only after the current effective user and
         group IDs have been mapped to the superuser UID and GID in the
         newly created user namespace. This makes it possible to
         ... interfaces in the network namespace or mounting filesystems in
         the mount namespace) even when run unprivileged. ...
         This option implies --setgroups=deny and --user. ...
  ```

  Note the option text itself states the mapping target is "the superuser UID and GID" — i.e. root — inside "the
  newly created user namespace", and it explicitly names "mounting filesystems in the mount namespace" as the
  capability that the mapping enables. This is the exact mechanism C2 uses.

### Quote A-2 — `-m, --mount` creates a new mount namespace

* HTML: `<b>-m</b>, <b>--mount</b>[<b>=</b><i>file</i>]` at line **152**; quote body at HTML line **153**
  (`Create a new mount namespace. If <i>file</i> is specified, then the`).
* Visible text: lines **97–101**.
* **Quote (22 words):** "Create a new mount namespace. If file is specified, then the namespace is made persistent by creating a bind mount at file"
* **Occurrences in visible text: 1.**

### Quote A-3 (supporting, the non-propagation statement) — DESCRIPTION, `id="DESCRIPTION"` (HTML lines 74–146)

* HTML line **100** (`Mounting and unmounting filesystems will not affect the rest`), 101 (`of the system, except for filesystems which are explicitly`).
* Visible text: lines **45–49**.
* **Quote (21 words):** "Mounting and unmounting filesystems will not affect the rest of the system, except for filesystems which are explicitly marked as shared"
* **Occurrences in visible text: 1.**
* Verbatim (visible text lines 45–57):

  ```
   mount namespace
    Mounting and unmounting filesystems will not affect the rest
    of the system, except for filesystems which are explicitly
    marked as shared (with mount --make-shared; see
    /proc/self/mountinfo or findmnt -o+PROPAGATION for the shared
    flags). For further details, see mount_namespaces(7).

    unshare since util-linux version 2.27 automatically sets
    propagation to private in a new mount namespace to make sure
    that the new namespace is really unshared. It's possible to
    disable this feature with option --propagation unchanged. Note
    that private is the kernel default.
  ```

  Quote A-3 is the man7 statement that mount activity in the new mount namespace does not reach the rest of the
  system (except explicitly-shared filesystems), and A-4 names the default `private` propagation that makes the new
  namespace "really unshared".

### Quote A-4 (supporting) — the propagation-to-private default

* HTML line **106** (`<b>unshare </b>since util-linux version 2.27 automatically sets`).
* Visible text: lines **50–55**.
* **Quote (25 words):** "unshare since util-linux version 2.27 automatically sets propagation to private in a new mount namespace to make sure that the new namespace is really unshared"
* **Occurrences in visible text: 1.**

**A note on A-1 + A-2 as one span:** a single contiguous ≤25-word span of unshare(1) cannot carry both the `-r`
sentence and the `-m` sentence (checked exhaustively: `windows with both tokens in 25 words: 0`). The pair A-1/A-2 is
therefore reported as two located quotes, each ≤25 words and each with count 1, rather than inventing a spliced
"quote" that does not exist on the page.

## 5. Quote B — `user_namespaces(7)` (S627 candidate)

Anchor: **DESCRIPTION** section, `id="DESCRIPTION"` (HTML lines 71–629).

### What the requested claim is, and what the page actually says

Requested: *"mount operations in a new mount namespace do not propagate to the parent namespace (or the nearest
supported statement; if absent, say so and do not invent)"*.

**Assessment, stated plainly: `user_namespaces(7)` does NOT contain the literal "mount operations do not propagate
to the parent namespace" sentence.** Exhaustive search of the stripped visible text for
`propagat|shared|subtree|peer group|MS_SHARED|visible|outside|parent mount|initial mount` returned only the
unrelated hits listed below; the page's own SEE ALSO points at `mount_namespaces(7)` for that subject, and the page
contains no mount-propagation paragraph of its own. The nearest statements it *does* make are the two quoted below,
which are the ones the C2 mechanism actually rests on (privilege to mount tmpfs inside the user namespace, and
privilege confinement to the namespace).

**Nearest supported statement B-1 — the capability the C2 counter exercises**
(Holding `CAP_SYS_ADMIN` in the user namespace that owns the mount namespace permits creating bind mounts and
mounting `tmpfs`.)

* HTML line **196** (`Holding <b>CAP_SYS_ADMIN </b>within the user namespace that owns a`), quote body at HTML
  lines **196–197** (`process's mount namespace allows that process to create bind`).
* Visible text: lines **141–145**.
* **Quote (19 words):** "Holding CAP_SYS_ADMIN within the user namespace that owns a process's mount namespace allows that process to create bind mounts"
* **Occurrences in visible text: 1.**
* The same paragraph enumerates the mountable filesystems; the `tmpfs` entry is the one C2 uses:
  * Visible text line **150**; HTML line **203** (`• <a href="../man5/tmpfs.5.html">tmpfs(5)</a> (since Linux 3.9)`).
  * **Quote B-2 (4 words):** "tmpfs(5) (since Linux 3.9)" — **occurrences in visible text: 1.**

  This is the exact `mount -t tmpfs tmpfs "$home_dir"` performed by `.ufo/waves/round-95/count-c2.sh` (see the
  counter's `in_ns()`: `unshare -rm sh -c 'mount -t tmpfs tmpfs "$1" …'`). The manual states the tmpfs type is
  mountable by a process holding `CAP_SYS_ADMIN` in the owning user namespace, so the counter's tmpfs-over-home step
  is permitted inside `unshare -rm` while the same step would fail unprivileged outside it.

**Nearest supported statement B-3 — privilege confinement to the namespace**
* HTML lines **82–83**; visible text lines **28–30**.
* **Quote (19 words):** "the process has full privileges for operations inside the user namespace, but is unprivileged for operations outside the namespace"
* **Occurrences in visible text: 1.**

**Adjacent B-4 (context, not quoted as the claim)** — "When a nonuser namespace is created, it is owned by the user
namespace in which the creating process was a member at the time of the creation of the namespace" (visible text
lines 169–172; HTML lines 225–228). This establishes that the user namespace created by `unshare -r` owns the mount
namespace created alongside it, which is the premise B-1 relies on.

### Supplementary depth (not a registry candidate)

The literal propagation sentence lives in `mount_namespaces(7)`, not in `user_namespaces(7)`. Fetched for depth only
(HTTP 200, 53669 bytes, sha256 `80ab1e4733a96669acdb58938fbc649d539c1c30d1b0cc7d968d8d3a1398c03b`); it is **not**
proposed as S626/S627 and is not needed — the unshare(1) DESCRIPTION already carries the non-propagation statement
as quote A-3. Its supporting lines include "MS_PRIVATE This mount is private; it does not have a peer group. mount(2)
and umount(2) events do not propagate into or out of this mount." and the `--propagation unchanged` note. It was
**not** added to SOURCES.md by this seat.

## 6. Quote occurrence counts (the explicit check requested)

Counted as exact substring occurrences in the whitespace-normalised visible text of each page:

| id | source | words | occurrences in visible text | visible-text lines | anchor (section id) |
|---|---|---|---|---|---|
| A-1 | unshare(1) | 22 | **1** | 287–291 | OPTIONS |
| A-2 | unshare(1) | 22 | **1** | 97–101 | OPTIONS |
| A-3 | unshare(1) | 21 | **1** | 45–49 | DESCRIPTION |
| A-4 | unshare(1) | 25 | **1** | 50–55 | DESCRIPTION |
| B-1 | user_namespaces(7) | 19 | **1** | 141–145 | DESCRIPTION |
| B-2 | user_namespaces(7) | 4 | **1** | 148–150 | DESCRIPTION |
| B-3 | user_namespaces(7) | 19 | **1** | 28–30 | DESCRIPTION |
| B-4 | user_namespaces(7) | 30 | **1** | 169–172 | DESCRIPTION |

Every quote is ≤25 words (B-4 is 30 words and is listed as context only, not as a claim quote). No count exceeds 1.
One rejected candidate, recorded so the check is auditable: `"This option implies --setgroups=deny and --user."`
(count **3**) — rejected because it does not support the assigned claim and is not unique.

## 7. Mapping the quotes onto the C2 mechanism

C2's counter (`.ufo/waves/round-95/count-c2.sh`, frozen) does, inside `unshare -rm`:

```
env -i PATH="$PATH" HOME="$S/home" TMPDIR="$S" \
  unshare -rm sh -c 'mount -t tmpfs tmpfs "$1" || exit 97; shift; exec "$@"' sh "$home_dir" "$@"
```

* `-r` → quote **A-1**: the effective user/group IDs are mapped to the superuser UID/GID in the newly created user
  namespace (and the same option text names "mounting filesystems in the mount namespace" as the enabled capability).
* `-m` → quote **A-2**: a new mount namespace is created.
* `mount -t tmpfs tmpfs "$home_dir"` is permitted → quote **B-1** (+ **B-2**): `CAP_SYS_ADMIN` within the user
  namespace that owns the mount namespace allows bind mounts and mounting `tmpfs(5)`; and **B-4**: that user
  namespace owns the newly created nonuser namespace.
* The tmpfs over the home directory does not touch the host → quote **A-3** (+ **A-4**): mounting/unmounting in the
  new mount namespace does not affect the rest of the system except for explicitly-shared filesystems, and unshare
  sets propagation to `private` by default since util-linux 2.27.
* Capability confinement → quote **B-3**: full privileges inside the user namespace, unprivileged outside it.

So the sourced claim ("C2's mechanism rests on S626 / S627") is covered by the two pages as cited, with one honest
qualification recorded in §5: the *literal* non-propagation sentence is in unshare(1) (S626), and user_namespaces(7)
(S627) supplies the privilege/capability half (tmpfs mountable, CAP_SYS_ADMIN scope, privilege confinement).

## 8. Proposed registry rows (for the L1's append — NOT written by this seat)

Field values for `corpus/SOURCES.md`; the L1 appends, per the seat item and CORPUS rule 4 (only rows the lesson
cites are appended).

**S626** — `unshare(1) — https://man7.org/linux/man-pages/man1/unshare.1.html` | docs | A |
scope: *the unshare(1) options that build the C2 sandbox: -r/--map-root-user maps the current user to root in a new
user namespace; -m/--mount creates a new mount namespace; mount activity in a new mount namespace does not reach the
rest of the system (except explicitly-shared filesystems), and unshare sets propagation to private by default* |
anchor: *OPTIONS (`id="OPTIONS"`, HTML lines 147–437; -m at 152–153, -r at 341–343) and DESCRIPTION
(`id="DESCRIPTION"`, HTML lines 74–146; mount-namespace bullet at 100–101, propagation-private note at 106)* |
teaches: *`-r` maps the effective user and group IDs to the superuser UID and GID inside the newly created user
namespace, and `-m` creates a new mount namespace; mounting and unmounting there does not affect the rest of the
system except for explicitly-shared filesystems, and unshare sets propagation to private by default* |
quotes: *"the current effective user and group IDs have been mapped to the superuser UID and GID in the newly created
user namespace"* (22 words, count 1), *"Create a new mount namespace. If file is specified, then the namespace is
made persistent by creating a bind mount at file"* (22 words, count 1), *"Mounting and unmounting filesystems will
not affect the rest of the system, except for filesystems which are explicitly marked as shared"* (21 words, count 1)
| page sha256 `1df4f95f877112743581e8b0900ce1296dbc6155619f7b88232e076f27b7375e`, 38193 bytes, HTTP 200, two fetches
byte-identical; util-linux 2.43.devel-1062-f... 2026-08-03, HTML rendering created 2026-09-09; opened 2026-11-05.

**S627** — `user_namespaces(7) — https://man7.org/linux/man-pages/man7/user_namespaces.7.html` | docs | A |
scope: *what a user namespace permits for mounts and where its privileges stop: CAP_SYS_ADMIN within the user
namespace that owns a mount namespace permits bind mounts and mounting tmpfs; privileges are full inside the user
namespace and absent outside it* |
anchor: *DESCRIPTION (`id="DESCRIPTION"`, HTML lines 71–629; CAP_SYS_ADMIN/mount paragraph at 196–197, tmpfs bullet at
203, privilege isolation at 82–83)* |
teaches: *a process holding CAP_SYS_ADMIN in the user namespace that owns the mount namespace may create bind mounts
and mount tmpfs there, and its privileges do not extend outside the user namespace* |
quotes: *"Holding CAP_SYS_ADMIN within the user namespace that owns a process's mount namespace allows that process to
create bind mounts"* (19 words, count 1), *"tmpfs(5) (since Linux 3.9)"* (4 words, count 1), *"the process has full
privileges for operations inside the user namespace, but is unprivileged for operations outside the namespace"* (19
words, count 1) |
page sha256 `276480f2185f65ee9ca1402c233a53780dd558a77bcc30127bbb5bfafb1301b4`, 59987 bytes, HTTP 200, two fetches
byte-identical; man-pages 6.19 2026-02-08, tarball fetched 2026-09-09, HTML rendering created 2026-09-09; opened
2026-11-05.

Scope note for the L1: S627 must **not** be scoped as "mount operations do not propagate to the parent namespace" —
that sentence is not on the user_namespaces(7) page. S626 (quote A-3) carries that claim; S627 carries the
capability/privilege half of the mechanism.

## 9. Tools and environment

No tool was installed or upgraded for this seat; the preinstalled toolchain was sufficient, so no pacman/uv/npx
transaction was filed (pacman transactions are PAUSED host-wide).

* `python3` — Python 3.14.8 (`python3 -V`), used for `html.parser` tag stripping, whitespace normalisation and the
  occurrence counts.
* `curl` — 8.23.0 (x86_64-pc-linux-gnu) libcurl/8.23.0 OpenSSL/3.6.5 — both fetches.
* `sha256sum` — coreutils 0.8.0 — all digests.
* `grep` (GNU), `cmp` (GNU coreutils) — duplicate sweep, byte-identity check.

## 10. Constraints honoured

* Nothing was written outside this report file and `$HYAKU_SCRATCH/mori-r95/Mo95S01Src/` (scratch removed on exit).
* `corpus/SOURCES.md` was **not** appended to; no frozen round-95 artifact (`contract.md`, `count-c1.py`,
  `count-c2.sh`, `evidence/*`), no round-93/94 artifact, no fleet-root file and no sibling lane was modified.
* Read-only git only (`status`/`show` were not needed; no git command was run in the lane). No mutating git/jj
  command was issued anywhere. The two page copies were fetched with curl into scratch and are **not** committed to
  the lane.
* No host sysctl, kernel setting, service, mount or package was mutated; no `sudo` write was run; no user namespace
  was created by this seat (the C2 counter's own `unshare -rm` was only *read*, not executed here).

## 11. Remaining unknowns (for the L1, not blockers)

1. The literal "mount operations in a new mount namespace do not propagate to the parent namespace" sentence is
   **absent from user_namespaces(7)** and present in unshare(1) (A-3) and in mount_namespaces(7) (supplementary,
   not proposed). The L1 should scope S627 to the capability/privilege facts, as in §8.
2. `mount_namespaces(7)` (sha256 `80ab1e4733a96669acdb58938fbc649d539c1c30d1b0cc7d968d8d3a1398c03b`, 53669 bytes)
   is a clean third candidate if the L1 decides the round wants a dedicated propagation row; it was swept for
   duplicates (§1) and is not in the registry.
3. User-namespace availability remains host configuration (`/proc/sys/user/max_user_namespaces`), as the frozen
   contract already states; this seat did not read or change that sysctl.

SEAT Mo95S01Src SOURCES-READY
