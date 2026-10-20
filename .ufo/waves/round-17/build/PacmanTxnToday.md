# Pacman transactions on 2026-10-20, and the host-wide pause ruling

Scope: detection only. Every fact below was read from `/var/log/pacman.log` and the
fleet `.ufo` text artifacts. **No pacman invocation of any kind was run** (only `grep`,
`sed`, `stat`, `git log/show` reads). No journal query. No tool install or upgrade.

All times are host-local `-0300`, exactly as written in the log (which switches to
`+0000` for a few 2026-10-03 lines only; no 2026-10-20 line is UTC).

## 1. Verdict

- The 2026-10-20 log holds **20 `[PACMAN] Running` invocations**, of which **15 opened an
  `[ALPM] transaction started` … `transaction completed` pair**; the other 5 are
  2× `-Sw` download-only and 3× `-D` database-only, which never start a transaction.
- **Both named entries are confirmed**: the `-Syu` at **09:15:30** (`/var/log/pacman.log:2462`)
  and the `-U zcode` at **13:23:08** (`:3161`).
- The host-wide pacman pause was in force **no later than 05:35:41 -0300** (first
  dispatch artifact carrying the guard, commit `67f4e00`). **15 invocations / 11 actual
  transactions ran after it**, from **07:45:36 through 13:23:09** — including the
  **09:15:30 `-Syu` full system upgrade** and the **13:23:08 `-U zcode`**.
- The 09:15:30 `-Syu` did both things the guard forbids: it **synchronized package
  lists** (`:2463`, a `-Sy` inside `-Syu`) and applied a **full upgrade of 448 package
  actions (413 upgraded + 35 installed, `:2479`–`:2941`)**, carrying exactly the
  boot-chain packages the tsukuroi `/sysroot` update-safety gate exists to protect.

## 2. Full census — every 2026-10-20 invocation

| # | log line | time | invocation (verbatim head) | class | ALPM transaction evidence |
|---|---|---|---|---|---|
| 1 | 2410 | 01:06:49 | `pacman -S --needed --noconfirm wayland-utils` | install | 2412–2414; `installed wayland-utils (1.3.0-1)` |
| 2 | 2416 | 01:07:12 | `pacman -S --needed --noconfirm man-pages` | install | 2418–2420; `installed man-pages (6.19-1)` |
| 3 | 2422 | 02:41:25 | `pacman -Sw --noconfirm wlr-protocols` | download-only | none (no ALPM lines; next line is the `-S`) |
| 4 | 2423 | 02:41:32 | `pacman -S --needed --noconfirm wlr-protocols` | install | 2425–2427; `installed wlr-protocols (r112.a741f0a-1)` |
| 5 | 2429 | 04:25:16 | `pacman -S --needed --noconfirm libinput libinput-tools` | upgrade | 2431–2437; `upgraded libinput (1.31.3-1 -> 1.32.0-1)` + `installed python-libevdev 0.13.1-1`, `python-pyudev 0.24.4-1`, `python-yaml 6.0.3-2`, `libinput-tools 1.32.0-1` |
| 6 | 2440 | 07:45:36 | `pacman -S --needed --noconfirm compsize pacman-contrib` | install | 2442–2445; `installed compsize (1.5-2)`, `installed pacman-contrib (1.13.1-1)` |
| 7 | 2448 | 07:50:25 | `pacman -S --needed --noconfirm fclones` | install | 2450–2452; `installed fclones (0.35.0-2)` |
| 8 | 2454 | 08:14:12 | `pacman -Rns --noconfirm electron39 mbedtls` | remove | 2456–2459; `removed mbedtls (4.2.0-1)`, `removed electron39 (39.8.10-2)` |
| 9 | 2461 | 08:20:52 | `pacman -Sw --noconfirm --cachedir /tmp/pkgcheck limine-mkinitcpio-hook plymouth mkinitcpio` | download-only | none; pre-stages three boot-chain packages under `/tmp/pkgcheck` |
| 10 | 2462 | 09:15:30 | `pacman -Syu --needed --noconfirm nvme-cli smartmontools fio xfsprogs pacman-contrib earlyoom iotop-c sysstat stress-ng btrbk linux-lts linux-lts-headers` | **full-upgrade** | `:2463` `synchronizing package lists`; `:2464` `starting full system upgrade`; txn 2479–2941 = **448 actions: 413 upgraded + 35 installed** |
| 11 | 3064 | 09:27:39 | `pacman -S --needed --noconfirm fwupd` | install | 3066–3074; 7 new: `fwupd-efi 1.8-2`, `libmbim 1.34.0-1`, `libmm-glib 1.24.2-1`, `libqrtr-glib 1.4.0-1`, `libqmi 1.38.0-1`, `passim 0.1.12-1`, `fwupd 2.1.8-1` |
| 12 | 3085 | 09:29:39 | `pacman -S --noconfirm --config /etc/pacman.conf -- extra/go` | install | 3087–3089; `installed go (2:1.27.2-1)` |
| 13 | 3091 | 09:29:40 | `pacman -D -q --asdeps --noconfirm --config /etc/pacman.conf -- go` | database-only | none |
| 14 | 3092 | 09:31:03 | `pacman -U --noconfirm --config /etc/pacman.conf -- .../yay/elephant/*.pkg.tar.zst` | local | 3094–3121; 12 upgrades `elephant* 2.21.0-1 -> 2.22.1-1` + 12 `*-debug 2.22.1-1` installs (yay cache) |
| 15 | 3125 | 09:31:04 | `pacman -D -q --asdeps ... -- elephant ...` | database-only | none |
| 16 | 3126 | 09:31:04 | `pacman -R -s -u --noconfirm --config /etc/pacman.conf -- go` | remove | 3128–3130; `removed go (2:1.27.2-1)` |
| 17 | 3132 | 09:38:33 | `pacman -Rns --noconfirm btrbk elephant-*-debug` | remove | 3134–3149; 12 `elephant-*-debug` + `removed btrbk (0.32.7-1)` — **btrbk was installed at 09:16:28 (`:2525`) in the `-Syu` and removed 22 min later** |
| 18 | 3152 | 09:39:21 | `pacman -Rns --noconfirm gst-plugin-gtk hyprwayland-scanner webp-pixbuf-loader` | remove | 3154–3158; 3 removals |
| 19 | 3161 | 13:23:08 | `pacman -U --needed --noconfirm --config /etc/pacman.conf -- .../yay/zcode/zcode-3.16.2-1-x86_64.pkg.tar.zst` | **local** | 3163–3165; `installed zcode (3.16.2-1)` (new package, not an upgrade) |
| 20 | 3169 | 13:23:09 | `pacman -D -q --asexplicit --noconfirm --config /etc/pacman.conf -- zcode` | database-only | none |

Counts (all `rc=0`): day lines `760`; `Running` `20`; `transaction started` `15`;
`transaction completed` `15`; `starting full system upgrade` `1`; `synchronizing package
lists` `1`; `-U` `2`; `-D` `3`; `-Sw` `2`; `-R*` `4`.

Log ends at `:3169` (`13:23:09`); `stat` mtime `2026-10-20 13:23:09 -0300`, 244858 bytes.
**No pacman line was written after 13:23:09** (observed at read time, ≈15:45).

### The 09:15 `-Syu` payload (boot-chain lines, all in txn 2479–2941)

`glibc` 2.44+r24 → 2.44+r50 (`:2481`) · `systemd-libs`/`systemd` 261.2 → 262
(`:2487`, `:2531`) · `mkinitcpio` 41.1-1 → **42.2-1** (`:2539`) · `linux-lts` 6.18.57-2 +
headers **installed** (`:2540`, `:2542`) · `limine` 12.8.0 → 12.9.3 (`:2851`) ·
`limine-mkinitcpio-hook` 1.38.0-1.1 → **1.40.0-2** (`:2852`) · `limine-snapper-sync`
(`:2854`) · `linux` 7.2.3 → **7.2.11** (`:2855`) · `linux-headers` (`:2870`) ·
`nvidia-open-dkms` 610.57.04 → **615.78.08** (`:2892`) · `plymouth` -2 → -3 (`:2898`) ·
`systemd-sysvcompat` (`:2922`). The UKI rebuild that followed is logged at `:2990`–`:3063`
(`btrfs-overlayfs` and `plymouth` hooks visible at `:2992`, `:3006`, `:3025`, `:3038`).

## 3. When the pause was issued

No artifact carries a ruling timestamp of its own; the ruling is bracketed by the
following, all `-0300`:

| when | evidence | what it says |
|---|---|---|
| 04:25:16 | `pacman.log:2429`, `:2431–2437` | the incident itself: libinput 1.31.3-1 → 1.32.0-1 (mado r15 seat), host 413 packages behind sync |
| 04:28:42 | fleet git commit `8657033`, `.ufo/l0-questions.md:54` | hyaku orchestrator opens the L0 host partial-upgrade question; asks operator; "Lanes now dry-run every install (`pacman -Sp`) and refuse any upgrade of an installed package" |
| 05:11:49 | fleet git commit `e5b87e1`, `.ufo/l0-questions.md:55` | tsukuroi r15 host-recovery question: "consider a host-wide pause on all pacman transactions until an operator-owned recovery/update plan clears the mkinitcpio42 hook compatibility risk" |
| **05:35:41** | fleet git commit `67f4e00` ("round-16: mado dispatch evidence"); `.ufo/prompts/mado-round-16.md:254`; `.ufo/watchdog.log:462` (`launch mado round=16` 05:35:42) | first dispatch artifact carrying the operative sentence: "**all pacman transactions are PAUSED host-wide** (orchestrator ruling 2026-10-20 …)"; same guard in tsukuroi-r16 (`5a9055f`, 05:43:24), mori-r16 (`cd7a1a8`, 05:44:36), kake-r21 (`e159f30`, 05:51:50) |
| 06:25:31 | fleet git commit `6f05c91`, `.ufo/waves/hyaku/HANDOFF.md:91` (file mtime 06:30:33) | "Orchestrator ruling: all pacman transactions paused host-wide pending that decision." |

**Observed consequence:** the ruling was in force by 05:35:41. Exact issue time is
`[INFERENCE]` inside `(05:11:49, 05:35:41]`; no rate-limit-free timestamped ruling
record exists in `.ufo`.

`watchdog.log` itself has **no** pause/ruling entry (0 matches for `pacman`/`pause`);
it only timestamps dispatches, and its `launch mado round=16` at 05:35:42 corroborates
the 05:35:41 dispatch commit.

## 4. Post-ruling transactions (after 05:35:41)

15 invocations, **11 ALPM transactions**, all before any pause release is recorded:

| time | # | class | note |
|---|---|---|---|
| 07:45:36 | 6 | install | compsize, pacman-contrib |
| 07:50:25 | 7 | install | fclones |
| 08:14:12 | 8 | remove | electron39, mbedtls |
| 08:20:52 | 9 | download-only | pre-stages limine-mkinitcpio-hook, plymouth, mkinitcpio to `/tmp/pkgcheck` |
| **09:15:30** | **10** | **full-upgrade** | **-Syu: sync DB refreshed + 448 actions, incl. every guarded boot-chain package** |
| 09:27:39 | 11 | install | fwupd suite (7 pkgs) |
| 09:29:39 | 12 | install | go |
| 09:29:40 | 13 | database-only | `-D --asdeps go` |
| 09:31:03 | 14 | local | `-U` elephant suite 2.21.0 → 2.22.1 (24 actions) |
| 09:31:04 | 15 | database-only | `-D --asdeps elephant*` |
| 09:31:04 | 16 | remove | `-R -s -u go` |
| 09:38:33 | 17 | remove | btrbk + 12 elephant-debug |
| 09:39:21 | 18 | remove | gst-plugin-gtk, hyprwayland-scanner, webp-pixbuf-loader |
| **13:23:08** | **19** | **local** | **-U zcode 3.16.2-1** |
| 13:23:09 | 20 | database-only | `-D --asexplicit zcode` |

Pre-ruling window held only 5 invocations / 4 transactions (01:06:49, 01:07:12,
02:41:25 `-Sw`, 02:41:32 `-S`, 04:25:16 libinput upgrade).

## 5. Caveats / residual unknowns

- Actor identity for the post-ruling runs is **not observed here** (journal queries are
  forbidden for seats). Routed evidence: tsukuroi r17 states the journal attributes the
  13 runs 07:45–09:39 to account `vgpnk` with PWD split `~/Documents/nvhelpme` (4),
  `/home/vgpnk/tmp` (4), `/home/vgpnk` (5) — that is tsukuroi's read-only capture, not
  re-verified in this seat.
- Whether the 09:15 `-Syu` passed tsukuroi's `/sysroot` update-safety gate is **not
  observable from `pacman.log`**. Routed evidence `.ufo/l0-questions.md` (tsukuroi r17)
  states "no pacman/service/boot write by tsukuroi"; the off-log `limine-update` hook
  rebuild after the upgrade is likewise tsukuroi-reported, not in the log.
- `-D` rows are db-only and start no transaction; they are included for completeness,
  not counted as transactions.
- The 08:20:52 `-Sw` wrote its cache to `/tmp/pkgcheck`; flagged because probe/scratch
  output under `/tmp` is disallowed for seats, and this invocation is inside the
  post-ruling window.
- Pause status **after** 13:23:09 is not observable from the log beyond the fact that no
  further pacman line exists (log mtime 13:23:09 at read time ≈15:45).

## 6. Commands run (read-only, `rc` recorded)

- `grep -n '2026-10-20' /var/log/pacman.log | grep -E '[PACMAN]|transaction|full system upgrade|Running'` → rc 0
- `grep -n '^\[2026-10-20' … | grep -c …` count battery → rc 0 (`760/20/15/15/1/1/2/3/2/4`)
- `sed -n '2412,2414p;…' /var/log/pacman.log | grep '[ALPM] (installed|upgraded|removed)'` → rc 0
- `sed -n '2479,2941p' /var/log/pacman.log | grep -cE '\[ALPM\] (installed|upgraded|…) '` → `448` (`35 installed`, `413 upgraded`), rc 0
- `stat -c '%y %s' /var/log/pacman.log`, `tail -n 1` → rc 0
- `git -C /home/vgpnk/Projects/shokunin log/show -S … -- .ufo` (fleet, read-only) → rc 0

Tools installed/updated: none.
