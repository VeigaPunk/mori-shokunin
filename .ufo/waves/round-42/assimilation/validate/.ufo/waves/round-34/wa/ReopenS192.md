measured 2026-10-23T05:39:05Z

# Reopen S192 — findings (seat MoriR34A2.ReopenS192)

Row source: `git grep -n "^| S192 " 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3 -- corpus/SOURCES.md` → corpus/SOURCES.md:198.

## 1. Live double-fetch vs committed copy

Fetches: `curl -sSL --fail -m 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/block/holder.c` twice into scratch (/fast/scratch/hyaku/mori-r34/a2-ReopenS192/).

| fetch | accessed (UTC) | sha256 | match to committed copy |
|---|---|---|---|
| 1 (S192.live.1) | 2026-10-23T05:38:46Z | 1e41cc5cde74b89d10269351383426aef2d22dd7018fbc89ad63952562153a91 | identical |
| 2 (S192.live.2) | 2026-10-23T05:38:46Z | 1e41cc5cde74b89d10269351383426aef2d22dd7018fbc89ad63952562153a91 | identical |

Committed copy corpus/evidence/sources-r34/S192.src: sha256 1e41cc5cde74b89d10269351383426aef2d22dd7018fbc89ad63952562153a91, 3921 bytes; `git show 8d56809:corpus/evidence/sources-r34/S192.src | sha256sum` = same hash, so the copy at the pinned rev equals the live v7.2 file byte-for-byte. Quotes below from the copy therefore hold for the live source.

## 2. Anchor check (S192.src:34-54,128-153; tag v7.2)

- Lines 34-54: kernel-doc comment of `bd_link_disk_holder` (S192.src:34-61). Holds the cited code: line 35 title, line 41 "creates the following sysfs symlinks", lines 43-44 slaves/holders link directions, lines 46-50 the dm-0→sda example. ✓
- Lines 128-153: doc + body of `bd_unlink_disk_holder` (S192.src:128-155). Both `del_symlink` calls (lines 148-149) execute only under the refcnt-zero condition `!--holder->refcnt` (line 147). ✓
- tag v7.2: live fetch from the v7.2-tagged URL matches the committed copy exactly on two independent fetches. ✓

## 3. Clause-by-clause (scope + teaches cells)

Scope cell: "the v7.2 holder/slave sysfs symlinks between a stacking disk and the device it claims"
- "v7.2": provenance claim, verified via the tagged fetch path (section 1, not quoteable from content).
- "holder/slave sysfs symlinks between a stacking disk and the device it claims": S192.src:35 (10 words): "bd_link_disk_holder - create symlinks between holding disk and slave bdev" — supported.

Teaches cell clauses (all quotes contiguous from S192.src; `lane rule:` clause exempt per assignment):
1. "bd_link_disk_holder creates sysfs symlinks" → S192.src:41 (7 words): "This functions creates the following sysfs symlinks." — supported.
2. "for dm-0 mapping sda" → S192.src:46 (12 words): "For example, if /dev/dm-0 maps to /dev/sda and disk" — supported.
3. "/sys/block/dm-0/slaves/sda and /sys/block/sda/holders/dm-0" → S192.src:49 (5 tokens): "/sys/block/dm-0/slaves/sda --> /sys/block/sda" and S192.src:50 (5 tokens): "/sys/block/sda/holders/dm-0 --> /sys/block/dm-0" — supported.
4. "bd_unlink_disk_holder deletes both when the holder count reaches zero" → S192.src:147 (6 tokens): "if (!WARN_ON_ONCE(holder == NULL) && !--holder->refcnt) {" and S192.src:148-149 (8 tokens): "del_symlink(disk->slave_dir, bdev_kobj(bdev)); del_symlink(holder->holder_dir, &disk_to_dev(disk)->kobj);" — supported.
5. "lane rule: a non-empty `slaves` directory marks a stacked device (tool rule R3)." — labelled `lane rule:`; exempt from quote requirement.

No clause unsupported. No `"` or `|` inside any quoted passage.

## 4. Tooling record

No tool installed or updated (RULES.md read first; existing curl/git/coreutils used; no pacman/uv/npx action).

## 5. Proposed Gate row

| S192 | https://raw.githubusercontent.com/torvalds/linux/v7.2/block/holder.c | 2026-10-23T05:38:46Z | 1e41cc5cde74b89d10269351383426aef2d22dd7018fbc89ad63952562153a91 | "bd_link_disk_holder - create symlinks between holding disk and slave bdev" (S192.src:35); "This functions creates the following sysfs symlinks." (S192.src:41); "For example, if /dev/dm-0 maps to /dev/sda" (S192.src:46); "/sys/block/dm-0/slaves/sda --> /sys/block/sda" (S192.src:49); "/sys/block/sda/holders/dm-0 --> /sys/block/dm-0" (S192.src:50); "if (!WARN_ON_ONCE(holder == NULL) && !--holder->refcnt) {" (S192.src:147); "del_symlink(disk->slave_dir, bdev_kobj(bdev)); del_symlink(holder->holder_dir, &disk_to_dev(disk)->kobj);" (S192.src:148-149) | admit, A, mined |

VERDICT: admit
