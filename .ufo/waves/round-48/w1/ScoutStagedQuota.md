# ScoutStagedQuota — staged quota-entry scouting (round 48 w1)

Scope: six staged entries under
`/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/` plus their rows in
`/home/vgpnk/Projects/shokuknow/merge/mori/SOURCES.append.md`. Report is read-only scouting;
no file in the lane or in the merge tree was modified. Scratch (fetched pages, PDF text,
quote checks) under `.scratch/r48-ScoutStagedQuota/` (in-lane scratch only).

## Method

- Frozen committed copies under `corpus/evidence/sources-r48/` were checked with the same
  normalisation the counter uses (tags stripped, entities decoded, whitespace collapsed):
  sha256 all match the frozen pins (xfs_quota.8.html 6375e40e…, quotactl.2.html
  0d4ab273…, errno.h 66a5ad60…, aliyun-nas-quota.html 747fef1b…).
- Pages not in the frozen set were fetched read-only into scratch on 2026-10-25 (HTTP 200
  for all six checked: aliyun CPFS, man7 projects.5/projid.5/repquota.8, torvalds
  quota_tree.h, Google Cloud Lustre zh-cn, Alibaba CloudMonitor 2.0 rules and delay page,
  RHEL 7 EN/ZH PDFs). **The RHEL 9 Japanese PDF returned HTTP 200 / application/pdf /
  1,555,738 B on this fetch, not the 403 named in the frozen contract** — see §5.
- Host-side checks for the own-work rows: `lsattr -p /home/vgpnk` → project id 0 on all
  entries; `/etc/projects` and `/etc/projid` both absent (ls exit 2); matches the shokuknow
  evidence file `host-quota-and-peak.txt` (read-only, exists).

## 1. quota-observability-r38.md (FR2)

| item | finding |
|---|---|
| Claim | Quota exhaustion is per-id state with own counters/error/markers; `df` cannot see it. Four facts: accounting≠enforcement (S477); ESRCH vs zero (S478); directory-scoped quota surfaces as "Disk quota exceeded" in a separate 配额管理 view (S479); report markers `+`/`grace` (S481); platform note EDQUOT=122 (S482). |
| Source rows | S477 xfs_quota.8, S478 quotactl.2, S479 aliyun NAS, S481 RHEL 9 ja PDF, S482 errno.h — all staged `mined` opened 2026-10-23, used-by `corpus/knowledge/quota-observability-r38.md`. |
| Page support | All four committed-copy quotes verified verbatim: "distinguishes between quota accounting and limit enforcement"; state command monitors "space occupied by the quota system itself"; "Quota exceeded (EDQUOT) error" on hard-limit fails; quotactl ESRCH "No disk quota is found for the indicated user. Quotas have not been turned on for this filesystem."; quotactl_fd "instead works on the mount point" (HISTORY: Linux 5.14); errno.h line 107 `#define EDQUOT 122`; aliyun dd output `Disk quota exceeded` + 配额管理 console view. RHEL 9 ja PDF: 23.4 クォータ強制適用の有効化 text ("クォータアカウンティングは…デフォルトで有効になりますが、クォータの強制適用は有効になりません"; quotaon / mount-option enforcement), 23.8 soft-limit +/grace markers and units (秒、分、時間、日、週、または月) — all located in the fetched PDF. |
| PROVINCE | FR2 (quota/EDQUOT observability, detection/report only). Probes are read-only; no quota state change. Fits. |
| QUALITY | Claims carry located quotes/anchors; boundaries and delivery-path limits present. Caveats: (a) S481 was excluded from the C2 claim by the frozen contract (403 at freeze); the PDF is reachable now (§5) but still not one of the four frozen URLs, so it cannot feed the C2 table. (b) S477–S482 ids collide with lane S477/S478; per contract, renumber by document to S479+ and re-stamp `opened 2026-10-25`. |
| Verdict | **ADMIT** for the C2 basis: the four frozen-URL rows (xfs_quota, quotactl, aliyun-nas, errno.h) support ≥8 quotable 6–25-word spans across 4 sources (feasible). Keep S481 as a knowledge/knowledge-side row with a `recheck:` note; it is not a counter row. Flip condition: if the RHEL 9 ja PDF is again 403 at integration time, drop S481 (and its claims) from the entry. |

## 2. quota-counter-freshness-r39.md (FR2, FR8)

| item | finding |
|---|---|
| Claim | A quota-usage reading is a lagged counter (~15 min for that vendor), not a point-in-time fact; a breach observed now may have happened up to 15 min ago. |
| Source rows | S487 aliyun CPFS quota-management (mined, opened 2026-10-23, used-by quota-counter-freshness-r39.md). |
| Page support | Verified: "配额的统计大约有 15 分钟的延迟，当前的实际使用量大约 15 分钟之后才会生效。" occurs verbatim. The second quote in the entry ("修改配额时，设置的配额容量或文件数必须高于已使用容量或文件数，否则会报错") has a **quote drift**: the page reads "修改目录配额时，…" (missing 目录 in the entry). The entry's claim that "the same product's API reference repeats it" is **UNVERIFIED** (I did not fetch the SetFilesetQuota API page; the staged row cites it without a fetched anchor). |
| PROVINCE | FR2 boundary-adjacent: it is a cloud-vendor product semantics comparison, not a host/fleet surface; the entry itself scopes it as a comparison shape. Acceptable under FR2/FR8 as vocabulary, must not become a threshold authority. |
| QUALITY | Quote drift (fixable); "kernel's own quotactl() read returns the counter as the kernel holds it at that moment" is presented unmarked — it is inference from the r38 entry, not a located quote (QUALITY #3: observation/inference separation). API-repeat claim unverified. |
| Verdict | **ADMIT with fixes**: correct the drifted Chinese quote to the page text, mark the kernel-side freshness statement as [INFERENCE], and either fetch/quote the API page or drop the API-repeat claim. Not usable for the C2 table (not among the four frozen URLs). Flip condition: if the quote is corrected and the API claim removed/verified, admit; otherwise reject. |

## 3. quota-id-to-path-r40.md (FR2)

| item | finding |
|---|---|
| Claim | (1) Kernel quota tree is keyed by block offset, not id/path (S494); (2) project id is an inode attribute assigned per path with inheritance (S495); (3) id→name map is a userspace file that may not exist (S500). |
| Source rows | S494 kernel quota_tree.h, S495 Google Cloud Managed Lustre zh-cn, S500 own-work (file:///home/vgpnk, evidence `lanes/mori/round3/.deepresearch/notes/host-quota-and-peak.txt`). |
| Page support | quota_tree.h (fetched v7.2): `#define QT_TREEOFF 1` and `struct qt_disk_dqdbheader` with next/prev free block + entry-count fields — verified. Lustre zh-cn: "忽略 -r 意味着项目 ID 不会应用于现有文件和子目录。忽略 -s 意味着稍后创建的新文件和目录不会继承项目 ID。" and "此项目 ID 是 Lustre 文件系统标识符…不是您的 Google Cloud 项目 ID" — verified verbatim. S500 own-work: host check reproduced (id 0; /etc/projects,/etc/projid absent); evidence file exists in shokuknow and matches. |
| PROVINCE | FR2 attribution half; read-only. Fits. |
| QUALITY | S500 evidence file lives outside the lane repo (shokuknow). For the lane, the pointer must resolve inside `corpus/evidence/` to satisfy QUALITY #9 (every path pointer resolves at the carrying commit). Cross-references ("wave 1's quota-observability-r38.md") are package-internal and need renaming/renumbering on admission. |
| Verdict | **ADMIT with fixes**: copy the S500 evidence bytes into the lane corpus (or cite a lane-local equivalent receipt), rewrite cross-references to lane-local file names/ids, keep S500 scoped one-host-one-moment. No C2 role (URLs not among the four frozen). |

## 4. quota-id-mapping-files-r41.md (FR2)

| item | finding |
|---|---|
| Claim | A quota id resolves through two optional files (/etc/projects, /etc/projid); a missing mapping degrades silently to a bare number, not an error. |
| Source rows | S502 RHEL 7 EN PDF, S503 RHEL 7 ZH PDF, S504 projects(5), S505 projid(5). |
| Page support | projects(5): "provides a mapping between numeric project identifiers and those directories which are the roots of the quota tree", `10:/export/cage`, "optional, instead xfs_quota(8) can be used with the -p argument" — verified. projid(5): "displayed as a numeric value", `cage:10`, "similar relationship…" — verified. RHEL 7 EN: "known as managed trees", "Each managed tree is uniquely identified by a project ID and an optional project name", `echo 11:/var/log >> /etc/projects`, `echo logfiles:11 >> /etc/projid` — verified. ZH PDF: 受管树 quotes verified (count 2; the second exact sentence matches modulo PDF line-break whitespace). |
| **Structural defect (checked)** | Staged rows S502–S505 are **12 cells**, not the lane's 11-column format: the `recheck:` cell contains an unescaped `|` (e.g. `pdftotext … - | grep -c …`), so `split_cells` yields 12 columns and the `used-by` value is displaced (cell 10 shows the grep tail). The frozen `count-c2.py` requires `len(srow) == 11` (`row_ok`), so copying these rows verbatim into the lane registry would fail the source-row parse. Must be re-emitted with escaped pipes (or the pipeline moved out of the cell). |
| PROVINCE | FR2 resolution; read-only. Fits. |
| QUALITY | Currency rests on RHEL 7 (EOL product, 2014-era) docs; the entry asserts the same model is documented "for the current release" via the RHEL 9 ja PDF, which the frozen contract excluded (403 at freeze; fetchable now). Cross-references to "round 4's rows S260/S261" are dangling in this lane: mori-shokunin's SOURCES.md has **no S260/S261 rows** (checked), so those references describe the shokuknow registry, not this lane's. |
| Verdict | **REJECT as drafted.** Grounds: (a) malformed 12-cell staged rows would break the lane registry/11-cell parse (checked); (b) dangling S260/S261 cross-references (checked: absent from lane registry); (c) currency claim anchored on a source excluded by the contract. Flip condition: re-emit S502–S505 with escaped pipes and exactly 11 cells; rewrite/remove the S260/S261 references; and replace the currency anchor with a fetchable current release (the RHEL 9 ja PDF fetched fine today) or drop the sentence — then re-screen. |

## 5. quota-path-listing-r42.md (FR2)

| item | finding |
|---|---|
| Claim | The documented id→path resolution is `xfs_quota -c print`; its path list is a report-time join over the command line, mount table and /etc/projects. The lane's round-4 "Pathname column" request has no source (zero "Pathname" occurrences in the man page and repquota(1)). |
| Source rows | S509 xfs_quota.8 (same URL as S477). |
| Page support | Exact sentence verified in the committed copy: "Lists all paths with devices/project identifiers. The path list can come from several places - the command line, the mount table, and the /etc/projects file." `report` "report utilisation for those projects (directory trees)" verified. "Pathname" count in committed xfs_quota.8.html = **0** (checked); repquota.8 (fetched) "Pathname" = **0** (checked); RHEL 7 EN PDF's single "Pathname" hit is `Pathname checks` in the xfs_repair phase list (mount/repair option, not a report column) — verified. |
| PROVINCE | FR2; read-only. Fits. |
| QUALITY | **False lane-local claim (checked):** the entry says "the lane already holds this page at a different scope (round 1's S233…)" and "round 4's rows S260 (`projects(5)`) and S261 (`projid(5)`)". In mori-shokunin's registry S233 is the gihyo cgroup v2 article (not xfs_quota), and S260/S261 do not exist (checked). Those references describe the shokuknow lane's history, not this lane's; the "correction to the lane's own ledger" is therefore not true for mori-shokunin — this lane's ledger never requested a "Pathname" column (checked: zero xfs_quota/quotactl/projects/projid rows pre-round-48). S509 duplicates S477's URL; acceptable only as a distinct scope (accounting/enforcement vs print/report/path-sources) and must be reconciled in the registry. |
| Verdict | **ADMIT substance with mandatory fixes**: keep the verified print/report/zero-Pathname claims; delete or rewrite the S233/S260/S261 cross-references to lane reality (or state the correction applies to the source package's registry, not this lane); renumber S509 on admission. If the cross-reference claims are kept as-is, reject. |

## 6. alarm-latency-model-r39.md (FR8)

| item | finding |
|---|---|
| Claim | Four clocks govern alert visibility: metric period, detection period, silence period, effective window; confusing them yields false stories. Vendor's rule outside its effective window still records history and sends nothing. |
| Source rows | S488 Alibaba CloudMonitor 2.0 alert rules, S489 delay-explanation page. |
| Page support | S488 verified: "通道沉默周期 ：报警发生后未恢复正常，间隔多久重复发送一次报警通知。取值：1、5、10、15、30、50分钟，1、3、6、12、24小时。", "生效时间 ：报警规则的生效时间。报警规则仅在生效期内才会发送报警通知", "当报警规则不在生效期时，不会发送报警通知，但是报警历史记录仍然会显示在报警历史列表中", and 持续时间/告警阈值 with 紧急/警告/普通 ladder. S489 verified: "警示的檢測周期由監控指標的Period決定"; "大多數監控指標的Period為60秒…過去60秒所有監控值的彙總值". |
| PROVINCE | FR8 (thresholds labeled local). The entry is explicitly a comparison shape, refuses copying the vendor's numbers, and keeps the FR8 boundary. Within mori's FR8 frontier. Note: mori does not operate an alert-notification channel; the entry is vocabulary/boundary only. |
| QUALITY | Quotes located and verified; boundaries and delivery-path limits declared. Fit. |
| Verdict | **ADMIT** (FR8 coverage-map; no C2 role). No quota URL among the four frozen, so it is knowledge-only. Flip: none material — if it is re-framed as authority for mori thresholds, reject. |

## Summary table

| staged entry | claim | support | PROVINCE | QUALITY | verdict |
|---|---|---|---|---|---|
| quota-observability-r38 | per-id exhaustion; df blind | all 4 frozen-URL quotes verified verbatim; S481 PDF fetchable today (was 403 at freeze) | FR2 ✓ | located quotes; S481 not a C2 URL; renumber needed | **ADMIT** (C2 basis) |
| quota-counter-freshness-r39 | lagged counter | main quote verified; second quote drifted (missing 目录); API-repeat UNVERIFIED | FR2/FR8 ✓ | quote drift; unmarked inference | **ADMIT with fixes** / reject if unfixed |
| quota-id-to-path-r40 | block-trie; inode attr; optional map | S494/S495 verified; S500 host-check reproduced | FR2 ✓ | S500 evidence outside lane; dangling refs | **ADMIT with fixes** |
| quota-id-mapping-files-r41 | two optional files degrade silently | man pages + RHEL7 PDFs verified | FR2 ✓ | **12-cell malformed rows (checked)**; S260/S261 absent in lane; EOL currency anchor | **REJECT as drafted** |
| quota-path-listing-r42 | print join; no Pathname column | exact sentence verified; Pathname=0 in xfs_quota and repquota (checked) | FR2 ✓ | false lane-local S233/S260/S261 claims (checked) | **ADMIT substance with fixes**, else reject |
| alarm-latency-model-r39 | four clocks | S488/S489 quotes verified | FR8 ✓ | clean | **ADMIT** |

## Notes for the L1 integrator

- Renumber staged S477–S482 (and any other staged ids) to new lane ids starting at S479;
  every admitted row must be `mined`, `opened 2026-10-25`, with `used-by` pointing at the
  r48 entry name, per the frozen counter.
- The C2 table must draw only on the four frozen URLs; the four committed copies contain
  enough 6–25-word spans (xfs_quota, quotactl, aliyun-nas, errno.h) for ≥8 rows across ≥3
  sources — feasible.
- S481 (RHEL 9 ja PDF) returned **HTTP 200 / 1,555,738 B PDF on 2026-10-25**, contrary to
  the frozen contract's 403 observation. The contract still excludes it from C2 (not one of
  the four frozen URLs). Record the discrepancy; do not use it as a counter row.
- No tools were installed (used existing python3/curl/pdftotext); no pacman; no writes
  outside the assigned report and `.scratch/r48-ScoutStagedQuota/`.
