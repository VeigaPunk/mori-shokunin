measured 2026-10-23T07:46:41Z

# GateS193 — wave-B re-derivation of the S193 row

Objects attacked:
- Gate row: /fast/scratch/hyaku/mori-r34/a3-L1/drafts/corpus_lessons_round-34.md (S193 table row)
- Registry row: /fast/scratch/hyaku/mori-r34/a3-L1/drafts/corpus_SOURCES.md:199
- Committed copy: corpus/evidence/sources-r34/S193.src @ fd2521351c6cef47384aef30afbe1e4db7e6912e
- Scratch: /fast/scratch/hyaku/mori-r34/a3-GateS193/{S193-live.src,S193-committed.src}

## 1. Live fetch vs committed copy
- `curl -fsS --max-time 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/base/core.c` at
  2026-10-23T07:41:28Z -> sha256 `fa223c8f9f1bb40ca52c73f156439d311065e9be04efa2c6cf57039940e1c9fa`.
- `git show fd2521351:corpus/evidence/sources-r34/S193.src` -> identical sha256; `cmp` live vs committed:
  BYTE-IDENTICAL. 5434 lines, 151293 bytes. Gate-row sha256 cell agrees.

## 2. Gate quotes (whitespace runs collapsed)
- `S193.src:3508-3509` (9w) — verbatim match ("if (dev->parent && device_is_not_partition(dev)) { error =
  sysfs_create_link(&dev->kobj, &dev->parent->kobj,"), 9 words, contiguous, no `"`, no `|`. PASS.
- `S193.src:3542` (4w) — verbatim match, 4 words, contiguous, clean. PASS.
- Lesson reject note holds: `3542-3543` would span `sysfs_remove_link(&dev->kobj, "device");` — contains `"`,
  correctly rejected upstream.

## 3. Registry row, cell by cell (draft :199; diff vs tip shows only used-by change)
- id/source/kind/tier/status/opened/recheck: S193, correct v7.2 URL, code, A, mined, 2026-10-23, on-release. PASS.
- Anchor `drivers/base/core.c:3508-3510,3542-3543; tag v7.2`:
  - 3508-3510 hold the guarded create (`if (dev->parent && device_is_not_partition(dev)) {` /
    `error = sysfs_create_link(&dev->kobj, &dev->parent->kobj,` / `"device");`).
  - 3542-3543 hold the guarded remove (`if (...) ` / `sysfs_remove_link(&dev->kobj, "device");`).
  - tag v7.2 serves the URL live; bytes equal the copy. HELD.
- used-by `tools/mori-disk-rate.py`: exists at fd2521351 (`git cat-file -e` ok); the tool cites S193 in its
  docstring (`tools/mori-disk-rate.py:47-48`) and probes `"device"` at `:197`. PASS.
- teaches non-lane clause: "The `device` symlink is created, and removed, only when the device has a parent
  and is not a partition." — **UNSUPPORTED (defect)**.
  - `device_move_class_links` (S193.src:4647-4658), called by exported `device_move` (:4667; calls :4706,:4709),
    removes `"device"` iff `old_parent` non-NULL (:4653-4654) and creates it iff `new_parent` non-NULL
    (:4655-4657) — the entire reparent path has no `device_is_not_partition` check. `grep -n
    device_is_not_partition` hits only 2430/2435 (def), 3508, 3542.
  - Also the add-error unwind `out_device:` (:3522) removes `"device"` unconditionally (benign no-op, but
    another unguarded remove).
  - The clause's universal "only when ... is not a partition" is falsified by the copy itself: on reparent
    the link follows the parent with no partition guard.
  - `lane rule:` clause correctly labelled, exempt.
- attempt2-tracked.diff S193 row change: used-by `tools/mori-disk-rate.py; SKILL.md Round34` ->
  `tools/mori-disk-rate.py` only (diff lines 125 vs 133); consistent with lesson M6 narrative.

## 4. Verdict
VERDICT: reject — teaches cell of the S193 row (draft corpus_SOURCES.md:199) is unsupported: replace
"The `device` symlink is created, and removed, only when the device has a parent and is not a partition."
with a scoped clause, e.g. "The `device` symlink is created on add and removed on delete only when the
device has a parent and is not a partition (S193.src:3508-3510,3542-3543); on reparent via device_move the
link follows the parent without the partition check (:4653-4657)." Optionally extend anchor to
`drivers/base/core.c:3508-3510,3542-3543,4653-4657; tag v7.2`. All other cells pass; both Gate quotes pass.

## Audit of .ufo/waves/round-34/wa/ReopenS193.md
The seat enumerated the reparent path (§4, §6) but judged it "outside the row's creates/removes claim" and
admitted with "All clauses supported." Per-claim:
1. Row at corpus/SOURCES.md:199 at 8d56809, blob `ef1207c8…`, identical at tip — agree (rev-parse verified).
2. Copy 5434 lines / 151293 bytes — agree (wc).
3. Live fetch 05:38:54Z, sha256 `fa223c8f…1c9fa` — agree (hash reproduced at 07:41:28Z; its timestamp
   unverifiable, consistent).
4. Second fetch same sha256 — agree (same checkable content; second timestamp unverifiable).
5. S193.src blob `4d026682…` at 8d56809 and tip — agree (rev-parse).
6. `cmp` byte-identical live vs committed vs working tree — agree (reproduced).
7. `git status --porcelain` clean for the two files at 05:38Z — agree [unverifiable point-in-time claim;
   consistent with pre-integration timing].
8. Anchor A1/A2 verbatim quotes at 3508-3510 / 3542-3543 — agree.
9. Tag v7.2 resolves; served bytes equal the copy — agree.
10. §3 located quotes (3508, 3509, 3542, 2432 "return !(dev->type == &part_type);") are accurate — agree.
11. §4 create/remove site enumeration (3510, 3522, 3543, 4653-4657) — agree (my grep: 3510, 3522, 3543,
    4654, 4657).
12. §4 caller lines 3708 (device_add), 3814 (add error path), 3947 (device_del) — agree.
13. §5 proposed quotes all locate with right word counts — agree (landed row chose different ones).
14. §3 conclusion "All clauses supported; none unsupported" — disagree: the "only when" universal is
    falsified by 4653-4657 (and unconditionally by 3522); located quotes support only the guarded direction.
15. §4 "def at 4651" for device_move_class_links — disagree: def is at 4647 (4651 is `int error = 0;`);
    device_move def is 4667, not cited.
16. §4/§6 "reparent path is outside the row's 'creates and removes' claim" / noted-as-residual — disagree:
    the teaches clause states a universal; the reparent path is in scope and makes it unsupported.
17. VERDICT: admit — disagree (row must fix the teaches cell).

AUDIT: agree 13 / disagree 4

## Residual risk / gaps
- The tool's docstring gloss (tools/mori-disk-rate.py:47-48, "the `device` link is created only for a device
  whose parent is not a partition") reads the guard loosely, but the tool is the judged object and is not
  edited; noted only.
- Live match is point-in-time byte equality of a tag URL; tag mutability not asserted.
- Tooling: nothing installed (pacman paused; no need). Used system curl, sha256sum, wc, python3, read-only git.
