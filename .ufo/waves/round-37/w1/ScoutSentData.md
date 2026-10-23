# Round 37 wave 1 — SentData re-sweep

**Item attacked:** r36 SentData evidence-file safety, re-run on this round: `.ufo/waves/round-37/evidence/` and `corpus/evidence/sources-r37/`. Axes: absolute operator paths (`/home/vgpnk`), credential material, raw journal cursors. Contract debt (e) (`contract.md:88`) requires repo-relative lane paths and no absolute operator path in new evidence.

**Seat:** ScoutSentData (leaf). Lane read-only. Installs: none.

## Inventory

- `glob` `.ufo/waves/round-37/evidence/` → 12 files: `c1-after-tip.txt`, `c1-after.txt`, `c1-before-memo.txt`, `c1-before-summary.txt`, `c2-after-tip.txt`, `c2-after.txt`, `c2-before.txt`, `census-end.txt`, `census-start.txt`, `drift-live-r37.txt`, `freeze-r37.txt`, `r17-jj-selftest-r37.txt`.
- `glob` `corpus/evidence/sources-r37/` → `S221.src`–`S225.src` (5 files).

## Measurements

Pattern set is the r36 `w2/SentData.md` sweep, plus the acceptance predicate `/home/vgpnk`.

1. `grep` `/home/vgpnk` over both trees → **4 hits**, all in evidence (sources: no matches):
   - `.ufo/waves/round-37/evidence/c1-before-memo.txt:2` — `tool: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-37/fixtures/memo-n1.py`
   - `.ufo/waves/round-37/evidence/c1-before-summary.txt:2` — `tool: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-37/fixtures/summary-only.py`
   - `.ufo/waves/round-37/evidence/census-start.txt:16` — `mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`
   - `.ufo/waves/round-37/evidence/census-end.txt:16` — `mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`
   Direct `read` of those lines matches. `census-start.txt` and `census-end.txt` are the same 17-line body (snapshot `#93BB`); the other 15 lines are public duplicate-url warnings, then `EXIT=0`. No other lane path.
2. Token / key-block scan `(gh[pousr]_…|github_pat_…|AKIA|ASIA|BEGIN … PRIVATE KEY|Bearer|Basic <b64>)` over both trees → **no matches**.
3. Header-value scan `(cookie|set-cookie|authorization|proxy-authorization): <value>` and `(access_token|refresh_token|api_key|client_secret|password|passwd) = <8+>` → **one lexical hit**: `corpus/evidence/sources-r37/S221.src:4312` `Proxy-Authorization: basic aGVsbG86d29ybGQ=` inside the RFC 9110 CONNECT example (`S221.src:4307-4312`, host `server.example.com`). Base64 is the published `hello:world` example, not an operator secret. Not counted as credential material.
4. `op://…` and `BEGIN/END PRIVATE KEY` → **no matches**.
5. Credentialed-URL scan (`user:pass@` or `?token|key|password|…=`) → **one lexical hit**: `corpus/evidence/sources-r37/S225.src:5800` `https://bar.invalid/api?key=730d67a37d7f3d802e96396d00280768773813fbe726d116944d814422fc1a45&data=about:unicorn` inside the Fetch CORS example (`S225.src:5791-5802`, hosts `foo.invalid` / `bar.invalid`). Published spec example, not an operator secret. Not counted as credential material.
6. Cursor / journal scan `(__CURSOR|_CURSOR=|cursor=<16+>|journal s=/i=/b=/m=|_BOOT_ID=|MESSAGE=.{80,}|journalctl -o export|json)` over both trees, plus a keyword pass `(__CURSOR|_CURSOR=|journalctl|MESSAGE=|_BOOT_ID)` on evidence → **no matches**.
7. Broader evidence path pass (`/home/`, `/Users/`, `vgpnk`, `/fast/scratch`, `~/`, `tool:`) → the four hits in (1) only. Other tool lines are not operator-home paths:
   - `c1-after.txt:2` `tool: /tmp/mori-c1-tool-exj399_h/mori-sources-appendonly.py`
   - `c1-after-tip.txt:2` `tool: /tmp/mori-c1-tool-kp9oujix/mori-sources-appendonly.py`
   - `c2-before.txt:2`, `c2-after.txt:2`, `c2-after-tip.txt:2` `path=tools/mori-source-drift.py` (repo-relative)
   - `freeze-r37.txt` pins are repo-relative (`.ufo/waves/round-37/…`, `tools/…`)
   - `drift-live-r37.txt` is `Snnn` state lines plus `MORI_SOURCE_DRIFT rows=220 …` / `EXIT=1`; no path
   - `r17-jj-selftest-r37.txt` is `SELFTEST ok: …` / `EXIT=0`; no path

`S221.src` / `S222.src` / `S223.src` / `S225.src` also contain the words token, password, Authorization, and HTTPPasswordMgr as spec or cheat-sheet prose (ABNF `Authorization = credentials` at `S221.src:5070,5145,9764,9807`). No secret value attached. Same classification as r36 source-copy lexical hits.

## Finding

Debt (e) is still open. Four new evidence lines disclose the operator account and workspace layout. No credential material and no raw journal cursor in either tree.

VERDICT: FAIL — `/home/vgpnk` at `evidence/c1-before-memo.txt:2`, `evidence/c1-before-summary.txt:2`, `evidence/census-start.txt:16`, `evidence/census-end.txt:16`.
