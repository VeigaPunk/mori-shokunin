# SrcPacmanLog — S048 draft (round 17, wave 1)

Scope: draft one SOURCES row and one Gate line for the pacman action-log location, plus the teaching note on what `pacman.log` does not record. `corpus/SOURCES.md` was NOT edited (registry owned by L1).

## Sources opened

- https://man.archlinux.org/man/pacman.conf.5 (LogFile). `read` failed twice (ECONNRESET). `curl -sS -L` returned HTTP 200, 28242 bytes, 2026-10-20, exit 0. Stripped text quoted at lines 111-114.
- https://man.archlinux.org/man/pacman.8 (--logfile). `read` failed twice (ECONNRESET). `curl -sS -L` returned HTTP 200, 41121 bytes, 2026-10-20, exit 0. Stripped text quoted at lines 199-201.
- Local cross-check: `man -P cat 5 pacman.conf` and `man -P cat 8 pacman` (Pacman v7.1.0, libalpm v16.0.1). Same wording at local man lines 79-82 and 175-177.

## Located quotes (verbatim; line breaks normalised)

- pacman.conf(5), LogFile (13 words): "Overrides the default location of the pacman log file. The default is /var/log/pacman.log."
- pacman(8), --logfile (16 words): "Specify an alternate log file. This is an absolute path, regardless of the installation root setting."

## Gate

Gate: S048 pacman action-log location — "Specify an alternate log file. This is an absolute path, regardless of the installation root setting." (pacman(8) `--logfile`, https://man.archlinux.org/man/pacman.8, accessed 2026-10-20). Companion: "Overrides the default location of the pacman log file. The default is /var/log/pacman.log." (pacman.conf(5) `LogFile`, https://man.archlinux.org/man/pacman.conf.5, accessed 2026-10-20).

## S048 draft row

Column format matches `corpus/SOURCES.md` header (`id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`):

| S048 | pacman.conf(5) LogFile and pacman(8) --logfile — https://man.archlinux.org/man/pacman.conf.5 ; https://man.archlinux.org/man/pacman.8 | docs | A | pacman action-log path override and its absolute-path rule | LogFile = /path/to/log/file (pacman.conf(5)); --logfile <file> (pacman(8)); live pages fetched by curl 2026-10-20; local man pages pacman v7.1.0 | The default action log is /var/log/pacman.log; LogFile and --logfile override it with an absolute path that the installation root does not prefix. The pages document the location only, not the record fields or the invoking user. | queued | 2026-10-20 | on-release | — |

## What pacman.log does NOT record (teaching)

Observed on this host, `/var/log/pacman.log` (3169 lines, mtime 2026-10-20 13:23). Read-only: `wc -l`, `sed -n`, `grep -o`, `grep -c`, `grep -i`.

- Record kinds seen: `[ALPM] installed|upgraded|removed|running|warning|transaction`, `[ALPM-SCRIPTLET]`, `[PACMAN] Running '<argv>'` (64 lines), `[PACMAN] synchronizing`.
- `[PACMAN] Running '…'` records the argv of an invocation, not who issued it. Example, line 1 (2026-10-03): `pacman -b /mnt//var/lib/pacman/ -r /mnt -Sy --noconfirm …` was written to the host log. This matches the man-page rule that the path is absolute regardless of the installation root.
- No field records the invoking uid, euid, login name, tty, or a sudo caller. A case-insensitive grep for `uid|user` over the whole file matched only package scriptlet text such as `Creating user 'passim' … with UID 961`, which are accounts created by packages, not the invoker. `sudo` appears only as a package name or in scriptlet hints (4 lines).
- Timestamps mix `+0000` and `-0300` offsets within one file, so the log has no single timezone reference.
- Teaching: a pacman.log line proves that a transaction ran with a given argv at a given time. It does not prove who ran it. Actor or uid evidence must come from a separate source, which this row does not establish. [INFERENCE] The absence of actor fields in the file is observed; that pacman never writes them is inferred from the man pages (location only) and the file sample.

## Touched surfaces

- Written: this report only.
- Not edited: `corpus/SOURCES.md`, lane checkout, fleet files.
- Installs or updates: none.
- Commands: `read` (failed, ECONNRESET), `curl -sS -L` (stdout only, no file written), local `man -P cat`, and read-only `wc`/`sed`/`grep` on `/var/log/pacman.log`. No `/tmp` writes, no `journalctl`, no pacman transaction.

## Out of scope and not verified

- Whether `--logfile` combined with `-r` writes to a different path: not run.
- Behaviour in other pacman versions: [INFERENCE] only; the man pages checked are v7.1.0.
- The source of actor or uid evidence: not established here.
