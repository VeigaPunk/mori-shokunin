# SentCopies — security & hygiene review of committed source copies (round 48, w1)

Seat: SentCopies (mori-shokunin, leaf; no subagents).
Scope: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r48/` — the four committed copies pinned by
`.ufo/waves/round-48/count-c2.py` COPIES.
Date: 2026-10-25. All paths absolute; all commands read-only (host reads). No lane tools run; nothing installed
(no tooling directive entries).

## 1. Integrity: sha256 vs COPIES pins (and freeze record)

Commands (exit 0):

```
$ sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r48/*
747fef1bcc8c6d6c18908f4534879922bebdaece1a476831d48be93c4e22719f  .../aliyun-nas-quota.html
66a5ad60566fdd62e41701bcfc42bfeca5e5696ad1d47d78981575e0c51622be  .../errno.h
0d4ab273503d078ee0d9765c616b5082514e7d86e2c6a6b16c70cb7fba8b6ee8  .../quotactl.2.html
6375e40e9c0e950d78b38edbe9b7e7fdf5868d55be07040d4a029c552c437d5f  .../xfs_quota.8.html
```

All four match the COPIES pins in `count-c2.py` lines 36-45 byte-for-byte, and the four copy rows in
`.ufo/waves/round-48/evidence/freeze-sha256.txt` (lines 8-11). Verified.

## 2. Size cap (lane helper skips >1 MiB)

`stat`/`wc -c` (max shown):

| file | bytes | < 1 MiB |
|---|---|---|
| aliyun-nas-quota.html | 117506 | yes |
| xfs_quota.8.html | 33702 | yes |
| quotactl.2.html | 17114 | yes |
| errno.h | 5826 | yes |

No file exceeds 1,048,576 bytes. Directory contains exactly these four regular files (`ls -la`: `-rw-r--r--`, no symlinks, no hidden files).

## 3. Credential material, tokens, cookies, session ids, `op://` — none

Scan method: regex sweeps over raw bytes plus manual read of `errno.h` (127 lines, read in full) and of every `<script>`/comment block. Patterns included AWS `AKIA/ASIA` keys, JWT `eyJ…`, GitHub `gh[pous]_`, Slack `xox*`, Stripe `sk/pk_live_`, Google `AIza…`, Aliyun `LTAI…` AccessKey IDs, PEM private keys, `op://`, and assignment-style `password/secret/token/cookie/session/csrf/auth/… = value` patterns. All negative.

- The only value-like tokens found are public analytics identifiers, not credentials:
  - `sc_project=7422636`, `sc_security="9b6714ff"` — StatCounter site id/security code (quotactl.2.html line 313-315, xfs_quota.8.html line 592-594).
  - `UA-9830363-8` — Google Analytics property id (quotactl.2.html line 335, xfs_quota.8.html line 614).
  - aplus beacon `trid=213e053517929606271031590e14da&asid=AQAAAABzaN5qJ7KcaQAAAABgLWgnOov7Hg==` — Alibaba tracker request correlation ids (aliyun-nas-quota.html line 81, byte 46848).
- Credential-keyword regex hits were all benign substrings: `sts` inside the `nas-sts` StatefulSet examples (aliyun file, 24 occurrences, e.g. byte 20351, 21479, 23091, 27250; and xfs_quota.8.html bytes 7910, 10498, 15712, 26392), and `auth` in `author of` (man-page credit line, both man pages). No comment block contained any risky keyword.
- Emails found are public maintainer addresses: `man-pages@man7.org` (quotactl.2.html byte 12295; xfs_quota.8.html byte 30909), `linux-xfs@vger.kernel.org` (xfs_quota.8.html byte 30212).

## 4. Private URLs, `file://`, `op://` — none

No `localhost`, `127.0.0.1`, `0.0.0.0`, `::1`, RFC1918 (10./8, 172.16-31./12, 192.168./16), `*.local`/`*.internal`/`*.corp`-style hosts, `file:///`, or `op://` anywhere. All `http(s)://` URLs are public (man7.org, statcounter.com, google-analytics.com, alicdn.com, alyasset.com, aliyun.com, xfs.org, beian.*.gov.cn, www.w3.org).

## 5. Absolute host paths — none (all path literals are documentation text)

Path-shaped literals are all Unix doc examples, not host-local paths revealing a machine:

- xfs_quota.8.html: `/etc/projects`, `/etc/projid` (bytes 4843, 5067, 10666, 16106, 24091, 24865, 26334, 27351, 27365), `/tmp` (9829), `/proc/self/mounts` in quotactl.2.html (9946), and `/dev/xvm/home`, `/home`, `/dev/xvm/var`, `/var`, `/var/log` in example commands (bytes 26720-27417).
- aliyun-nas-quota.html: `/dev/zero`, `/data/20G.txt`, `/data/1G.txt` inside `dd` demo commands (bytes 27265, 29896, 87294, 89789); the remaining hits are `/home` appearing inside public URL paths (`https://home.console.aliyun.com/home/dashboard/ProductAndService` byte 55496; `https://www.alibabagroup.com/cn/global/home` byte 110418).

No `/home/<user>`, `/Users/…`, `C:\…`, or `~`-style host paths.

## 6. Embedded scripts that execute when the file is opened

`errno.h` is a plain C header (no markup, no scripts). The three HTML files carry live script surface. All are stock site runtime/analytics assets (unmodified page copies); none is malicious, but all run when opened with network access, and the Alibaba page injects a remote script at parse time.

aliyun-nas-quota.html (23 `<script>` blocks; 269 lines):
- Inline data/timing scripts (harmless): line 25-27 `window.pageStartTime`; 43-55 JSON-LD `application/ld+json` (schema.org WebPage data, not executed as JS); 61-71 `window.globalData` + `$ACE_TRACKER_CONFIG`; 72-77 `window.__ICE_SSR_ENABLED__/__ICE_APP_DATA__/__ICE_PAGE_PROPS__` (SSR props JSON incl. doc body); 84-86 and 223-225 performance marks; 228-247 `ALIYUN_PERF` beacon builder.
- **Dynamic injector (executes on open):** line 80-82 (byte 46848-47175): `with(document)…insertBefore(createElement("script"),firstChild))setAttribute("exparams",…,id="tb-beacon-aplus",src=(location>"https"?"//g":"//g")+".alicdn.com/alilog/mlog/aplus_v2.js")` — creates a `<script>` element fetching Alibaba's aplus loader from `g.alicdn.com`.
- External `<script src>` (execute on open, fetch remote): line 249 `g.alicdn.com/…/react.production.min.js,react-dom…`; 250 lodash; 252 inline `window.resourceBaseUrl`; 254-255 `index.js`, `vendor.js` (help-portal-fe 0.12.63); 257 `fast-login.js?tenantName=help-new-aliyun-com`; 258 perf `index.js`; 259 `//cloud-assets.alicdn.com/website.js` (protocol-relative); 262-265 alyasset.com `npm.combo`/`code.combo` bundles (biu-loader, hmod-preact, lowcode-env-inject, global-nav/search); plus two `lowcode/entry/prod/…js` loads (bytes 117038, 117383).
- External `<link rel="stylesheet">` (CSS load, not script exec) at lines 76-77 and footer; `data:image/png;base64,…` at bytes 37821 and 97340 are 1×1 transparent PNG placeholders (inert).

quotactl.2.html (351 lines) and xfs_quota.8.html (630 lines) — identical tracking tail:
- StatCounter: inline config + `<script src="https://www.statcounter.com/counter/counter.js">` (quotactl lines 312-319, bytes 15991-16204; xfs lines 591-598, bytes 32579-32792); `<noscript>` image fallback to `c.statcounter.com` (lines 320-325 / 599-604).
- Google Analytics: inline `_gaq.push(['_setAccount','UA-9830363-8'])` then dynamic `document.createElement('script')` loading `ga.js` (quotactl lines 332-344, bytes 16559-17032; xfs lines 611-623, bytes 33147-33620).

Negative controls across all four files: no event-handler attributes (`on*=`), no `javascript:` URIs, no `<iframe>/<object>/<embed>/<applet>`, no `<base>`, no `<meta http-equiv=refresh>`, no `data:text/html`, no `<form>` except the benign Google search box on the man pages (`<form method="get" action="https://www.google.com/search">`, quotactl byte 1707, xfs byte 1925).

## 7. Verdict

Clean: no credential material, tokens, cookies, session ids, `op://` references, private URLs, or absolute host paths in any of the four committed copies; all four hashes match the COPIES pins and the freeze record; all sizes < 1 MiB. Hygiene note only: the three HTML copies contain live third-party analytics/runtime scripts (StatCounter, Google Analytics, Alibaba CDN including an on-open script injector) that make network requests and execute JS if the files are opened in a browser; this is inherent to the fetched pages, not an injected artefact — quotes taken from these copies should be treated as data, never opened/executed interactively.
