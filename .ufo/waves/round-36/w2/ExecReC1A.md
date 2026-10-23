measured 2026-10-23T18:45Z
# ExecReC1A — re-score the C1 byte predicate with a fresh draw (network)

Item attacked: **C1's frozen byte predicate P-C1**, re-scored with a fresh (network) draw at the landed data tip
`bf0df77fee4b6ef54a90aea09335c7617f125151`. This is **byte-behavior evidence only**. Per the round-36 contract's
"C1 declared exploratory before data" section (`contract.md:113-124`) and wave-1 `w1/CritAxisFit.md`, **no freshness
verdict is claimed or inferred from anything below**; C1 verifies only as *unprovable-but-better* with a named
non-author reviewer, else it lands *unprovable*. C2 (measured, operability) is the round's measured claim.

Lane bounds honored: read-only on the lane repo (no `git add/commit/push/fetch/reset`, no mutating `jj`, no lane file
edits). Only this report was written. Scratch: `/fast/scratch/hyaku/mori-r36/ExecReC1A/`. No tool installs, no pacman.

---

## 1. The requested run — full output and exit code

Command (from the lane repo):

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin && python3 .ufo/waves/round-36/count-c1.py bf0df77fee4b6ef54a90aea09335c7617f125151
```

Observed output (verbatim), exit code `0`:

```
P-C1: at revision R, tools/mori-source-drift.py classifies every row of a 40-row blind fixture drawn at run time exactly as the counter's hidden truth, and on the lane's own corpus/SOURCES.md at R it agrees with the counter's independent live oracle on every row the oracle classified, with at least 10 oracle-fetched rows including at least one oracle-fresh and one oracle-drifted row.
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
real_rows=220 oracle_fetched=58 oracle_fresh=49 oracle_drifted=9 oracle_excluded=0 tool_exit=1 tool_rows=220 mismatches=0
C1=met
seed=17263505606192669537
```

Exit code: `0`.

### Second and third independent draws (stability)

Same command re-run twice more, each drawing a fresh seed from `os.urandom` (`count-c1.py:698-699`):

```
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
real_rows=220 oracle_fetched=58 oracle_fresh=49 oracle_drifted=9 oracle_excluded=0 tool_exit=1 tool_rows=220 mismatches=0
C1=met
seed=803864615566597897
```
```
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
real_rows=220 oracle_fetched=58 oracle_fresh=49 oracle_drifted=9 oracle_excluded=0 tool_exit=1 tool_rows=220 mismatches=0
C1=met
seed=8430371212992900000
```

Three draws, three distinct seeds (`17263505606192669537`, `803864615566597897`, `8430371212992900000`), all
`C1=met`, exit `0`. The L1's own recorded receipt `evidence/c1-after.txt` (seed `7388485190103051243`) reports the
same arm numbers (`oracle_fetched=58 oracle_fresh=49 oracle_drifted=9 oracle_excluded=0 mismatches=0`), so the result
is reproducible across an independently-drawn seed.

---

## 2. Verification checklist — item by item

### 2.1 P-C1 sentence byte-identical to `contract.md:21` — **PASS**

`contract.md` line 21 is the P-C1 sentence; the counter holds it as the module-level constant `PREDICATE`
(`count-c1.py:50-58`) and prints it at `count-c1.py:669` as the first stdout line.

```
$ awk 'NR==21' .ufo/waves/round-36/contract.md | sha256sum
304a3d0afb5682e12e4c2d8c3be7ba7e01eddcf2d838de290d52dd5cba771c2a  -
```

```
$ python3 - <<'EOF'   # AST-extract PREDICATE from the counter, compare with contract.md:21
...
stdout_line=(pred+"\n").encode()
print('stdout first line sha256:',hashlib.sha256(stdout_line).hexdigest())
print('contract.md:21 sha256   :',hashlib.sha256(contract[20]).hexdigest())
print('BYTE-IDENTICAL:',stdout_line==contract[20])
EOF
stdout first line sha256: 304a3d0afb5682e12e4c2d8c3be7ba7e01eddcf2d838de290d52dd5cba771c2a
contract.md:21 sha256   : 304a3d0afb5682e12e4c2d8c3be7ba7e01eddcf2d838de290d52dd5cba771c2a
BYTE-IDENTICAL: True
```

The counter's printed line is byte-identical to `contract.md:21` **including** the trailing newline (the counter's
`PREDICATE` constant carries no trailing `\n`; `print()` supplies exactly the one the contract line has). The
sentence is unchanged across the whole contract history — the P-C1 line hash is `304a3d0a…771c2a` at all three
contract commits:

```
$ for c in 5842dc04 c1a026cb da12b378; do printf "%s L21sha=%s\n" "$c" "$(git show $c:.ufo/waves/round-36/contract.md | sed -n '21p' | sha256sum | cut -c1-16)"; done
5842dc04 L21sha=304a3d0afb5682e1
c1a026cb L21sha=304a3d0afb5682e1
da12b378 L21sha=304a3d0afb5682e1
```

`da12b378` = the original freeze; `c1a026c` = the v2 re-design; `5842dc0` = the exploratory declaration. The predicate
sentence did not move. (The `contract.md` *file* hash differs from `freeze-v2.txt` only because `5842dc0` appended the
exploratory-declaration section below line 21; `freeze-v2.txt` pins `dbd3f6d7…` = the `c1a026c` bytes. The predicate
line itself is unchanged — that is the frozen thing P-C1 is.)

### 2.2 Blind arm 40/40, mismatches=0 — **PASS**

`blind_rows=40 tool_rows=40 mismatches=0` in all three draws. The fixture is drawn at run time from `os.urandom`
(`count-c1.py:698-699`), ids sampled without replacement from S001–S299, 8 rows per state, decoy copies written on 12
fresh/excerpt rows (`count-c1.py:399-407`), truth held only in counter memory (`count-c1.py:377-382`).

### 2.3 Real arm: fetched≥10, fresh≥1, drifted≥1, mismatches=0 — **PASS**

`oracle_fetched=58` (need 10), `oracle_fresh=49` (need 1), `oracle_drifted=9` (need 1), `oracle_excluded=0`,
`mismatches=0` over `real_rows=220`. Thresholds are enforced at `count-c1.py:630-637`.

### 2.4 `C1=met` — **PASS** (exit 0; `count-c1.py:714`)

### 2.5 Fresh seed printed — **PASS**

`seed=` is printed after scoring on every run, drawn from `os.urandom` when `--seed` is absent
(`count-c1.py:698-699`). Three of my runs printed three different seeds, all different from the L1's receipt seed.

### 2.6 Counter sha256 matches `evidence/freeze-v2.txt` — **PASS**

```
$ sha256sum .ufo/waves/round-36/count-c1.py
86dd3b7ab2d2563bbc811e83717b35dfea3d69717dab4d41d454f8b87c8764c0  .ufo/waves/round-36/count-c1.py
$ git show bf0df77:...count-c1.py | sha256sum
86dd3b7ab2d2563bbc811e83717b35dfea3d69717dab4d41d454f8b87c8764c0  -
$ grep count-c1 .ufo/waves/round-36/evidence/freeze-v2.txt
86dd3b7ab2d2563bbc811e83717b35dfea3d69717dab4d41d454f8b87c8764c0  count-c1.py
```

Worktree bytes == tip bytes == the v2 freeze pin. The counter is unmodified since the freeze; the receipt is a receipt
of this claim.

---

## 3. Falsification attempts on the counter (does P-C1 discriminate?)

A passing counter that cannot fail is worthless, so I re-ran the frozen counter against substitute programs via the
documented `--tool` control path (`count-c1.py:653-659` — the lane's real tool was never edited).

**Control K2 (generic rows / copying the observed column — every row `fresh`):**

```
$ python3 .ufo/waves/round-36/count-c1.py bf0df77... --tool /fast/scratch/hyaku/mori-r36/ExecReC1A/k2_all_fresh.py
blind_rows=40 tool_exit=0 tool_rows=40 mismatches=32
blind_mismatch S017 tool=fresh truth=unavailable
blind_mismatch S023 tool=fresh truth=no-copy
...
real_arm=skipped
C1=unmet
EXIT=1
```

**Control K5 (denial — labels inverted: fresh→drifted, excerpt→drifted, else fresh):**

```
$ python3 .ufo/waves/round-36/count-c1.py bf0df77... --tool /fast/scratch/hyaku/mori-r36/ExecReC1A/k5_denial.py
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=24
blind_mismatch S003 tool=drifted truth=excerpt
blind_mismatch S029 tool=fresh truth=drifted
...
real_arm=skipped
C1=unmet
EXIT=1
```

Both substitutes are rejected (`C1=unmet`, exit 1) with the real arm correctly skipped to spare the rate-limited hosts
(`count-c1.py:704-707`). The counter discriminates: the `C1=met` above is a real verdict, not a constant.

The tool's own self-test also passes:

```
$ python3 tools/mori-source-drift.py --selftest
selftest exit_code            PASS
selftest row_states           PASS
selftest summary              PASS
selftest missing_sources_exit2 PASS
MORI_SOURCE_DRIFT_SELFTEST: PASS (4 cases)
SELFTEST_EXIT=0
```

---

## 4. Defect found — the landed documentation's drift tally is stale, and one new drifted row is a **changed source**

The counter is sound and the receipt is honest. But re-running the tool directly against the live network exposes a
**defect in the landed corpus documentation**, which is exactly the claim C1's exploratory status must not smuggle
through.

### 4.1 The defect

`corpus/knowledge/source-drift-r36.md:16-19` (landed at `bf0df77`, sha256 `54d7cb65…75d81`) states:

> `fresh` proves only byte identity with the committed copy, never that the row's `teaches` is right. `drifted` means
> the committed copy is not reproducible from today's body. That is not the same as a changed source: on 2026-10-23 the
> **seven** `drifted` rows were five annotated excerpts from round 30 (S156–S160 …) and two docs.python.org pages whose
> only change is the build footer (S176, S177)

`corpus/QUALITY.md:840-842` (landed at `bf0df77`, sha256 `23952044…63388`) repeats it:

> … round 36's frozen P-C1 required "at least one oracle-drifted row", and **all seven real drifted rows were
> representation differences** (S156–S160 annotated excerpts whose header sha256 equals the live body; S176/S177 build
> footers)

`SKILL.md:858-861` repeats it a third time.

**All three say seven. The counter measures nine.** The counter's own real arm — the frozen oracle, the landed tool,
the L1's own receipt `evidence/c1-after.txt`, and three of my independent draws — all report `oracle_drifted=9`.

### 4.2 The two extra drifted rows: S210 and S211

Running the tool directly on the lane (read-only, `python3 tools/mori-source-drift.py --root .`):

```
$ grep " drifted$" /fast/scratch/hyaku/mori-r36/ExecReC1A/tool-direct.txt
S156 drifted
S157 drifted
S158 drifted
S159 drifted
S160 drifted
S176 drifted
S177 drifted
S210 drifted
S211 drifted
$ tail -2 /fast/scratch/hyaku/mori-r36/ExecReC1A/tool-direct.txt
MORI_SOURCE_DRIFT rows=220 fresh=49 excerpt=0 drifted=9 unavailable=0 no-copy=162
```

The mechanism: the "seven" figure was measured on the **base** corpus (204 rows, no `sources-r36/` copies —
`evidence/c0-rescore-v2.txt:1156` reads `real_rows=204 oracle_fetched=42 oracle_fresh=35 oracle_drifted=7`). The round
landed 16 new rows S205–S220 with `corpus/evidence/sources-r36/*.src` raw-body copies, and two of them (S210, S211) do
not reproduce. The documentation was written against the pre-round corpus and never re-measured against the corpus it
was landed with.

**S210 — a genuine changed source, contradicting "not the same as a changed source".** S210's committed copy
`corpus/evidence/sources-r36/S210.src` has sha256 `64c603545b3f9799cc9525228ba70cf80444a063b32a4be37de2a5ca09b83421`,
which is byte-identical to the digest recorded for the same URL when the row was opened
(`corpus/lessons/round-32.md:43`, S064 row: `64c603545b3f9799cc9525228ba70cf80444a063b32a4be37de2a5ca09b83421`).
Today's live body hashes to `9b8f63b653029da49bce87f6b292f099dc8f1b3667a85515c92f66a6f5eb2978`:

```
$ sha256sum corpus/evidence/sources-r36/S210.src /fast/scratch/hyaku/mori-r36/ExecReC1A/S210.live
64c603545b3f9799cc9525228ba70cf80444a063b32a4be37de2a5ca09b83421  corpus/evidence/sources-r36/S210.src
9b8f63b653029da49bce87f6b292f099dc8f1b3667a85515c92f66a6f5eb2978  /fast/scratch/hyaku/mori-r36/ExecReC1A/S210.live
$ diff S210.live corpus/evidence/sources-r36/S210.src
36c36,37
<   <link rel="stylesheet" href="/application.min.ee050e6639aacc8d3f18c4718a1a579307a7b4f7e327a148fb17dba7398c7476.css">
---
>   <link rel="stylesheet" href="/application.min.c863b1eca1217b6c0d4a322bad3dcbe8f057d08564bd9fb8dca5a00a04dc66e6.css" integrity="sha256-yGOx7KEhe2wNSjIrrT3L6PBX0IVkvZ&#43;43KWgCgTcZuY=">
4007c4008,4009
< <script src="/js/application.min.eab2fadf7c740b753eac932d50ce3f1a8faccdef730adfe2b7d9c14c898960c9.js"></script>
---
> <script src="/js/application.min.2c50db482403f7c73cf1c3fdff10121a98d563baede24a87cbc8b056a298196a.js" integrity="sha256-LFDbSCQD98c88cP9/xASGpjVY7rt4kqHy8iwVqKYGWo=">
```

Four changed lines: the site rebuilt its CSS/JS asset bundle and dropped the `integrity=` attributes. The row's *taught*
content is unchanged (`"page last updated in 2.56.0"` and `2026-09-28` are present in both live and copy), so this is
not a change to the row's claim — but it is **not** a "representation difference" of the S156–S160 annotated-excerpt
kind either, and it is not the S176/S177 build-footer kind: the source document's bytes genuinely differ from the
copy. QUALITY 105's own test (`corpus/QUALITY.md:837-839`: compare the source's full-document sha256 with the one
recorded when the row was opened, and count the row as a source change only when they differ) applied to S210 gives
`sha256(copy)=64c60354…` vs `sha256(live)=9b8f63b6…` — **they differ** ⇒ by the lane's own landed criterion S210 is a
source change. The landed documents assert the opposite for all drifted rows.

**S211 — a byte-unstable source, permanently un-reproducible.** `corpus/evidence/sources-r36/S211.src` hashes
`a4e104ec9d6da304cc642346112b6f450dd2e4ef45d1a8e43531949842f39511`. Two consecutive fetches of the *same* URL,
seconds apart, give two further distinct hashes:

```
$ sha256sum S211.live S211.fetch1 S211.fetch2 corpus/evidence/sources-r36/S211.src
148fe2718973fc741254a51844f679cb7d181c3852392c72816227022bb974e8  S211.live
eb206332edb8647105c84b0f6cd59413fcf8400932a2a2fd3d3ebea001e8db50  S211.fetch1
07f5f98b0ca14975f826e7f132fdc559eec01fc814b8676bf965630d4e7737b2  S211.fetch2
a4e104ec9d6da304cc642346112b6f450dd2e4ef45d1a8e43531949842f39511  corpus/evidence/sources-r36/S211.src
```

The diff is per-request noise, not content:

```
$ diff S211.fetch1 S211.fetch2
77c77
< <meta name="ncbi_phid" content="C1EDC843ADBA2DE310C843004F0870EE.m_1" />
---
> <meta name="ncbi_phid" content="E73CD865ADBA641310D865003536E82E.m_1" />
1934c1934
<     <input type="hidden" name="csrfmiddlewaretoken" value="FzhVvRoQoGEilP8HMBhQVLkYtNd44AFGTDfz6SxYDo0ZzQcW69zHCWJOKRgkaOXY">
---
>     <input type="hidden" name="csrfmiddlewaretoken" value="vut0pPHSwhJ0Tjr7CtqAfHcprU1QqypDAjZJeGJAbQ6qMoLhTq8FjXE1tfHGTFXH">
```

PMC injects a per-session `ncbi_phid` and a per-session `csrfmiddlewaretoken`. The page can therefore **never** be
byte-reproducible against any stored copy, so S211 will classify `drifted` on every future run forever, and the probe's
`drifted` signal for it carries zero information about source change. The knowledge doc's `drifted` reader-action cell
(`corpus/knowledge/source-drift-r36.md:25`) tells the reader to "compare that value with `curl -sS <URL> | sha256sum`"
— for S211 that comparison can never succeed, and the doc gives no way to know that in advance.

### 4.3 Why this matters for the round's own declared limits

QUALITY 105 was landed as the round's answer to the C1 axis-fit defect: a drift witness must be checked for *what
changed* before it is used as a target (`corpus/QUALITY.md:837-843`). Its "Shown able to fail" evidence is the stale
"all seven real drifted rows were representation differences". Re-measured at the landed tip, that premise is false in
both directions — the count is 9, and S210/S211 are two new kinds of drift the criterion does not cover. QUALITY 105's
`Not covered:` clause only names "semantic drift of a page whose bytes never change"; it does not name the two cases
that actually occurred (site asset-bundle rebuild with unchanged taught content, and per-session-token byte instability).
QUALITY 105 therefore has no rule for S210 (does a changed asset bundle count as a source change? its own sha test says
yes) or S211 (a row that can never be fresh).

The same stale tally is repeated in `SKILL.md:858-861` and in `corpus/README.md:565` ("all 9 oracle-drifted rows were
representation differences (annotated excerpts S156–S160, docs.python.org build footers S176/S177)" — note this one
says **9** while listing only 7 ids, and `corpus/README.md` is currently an **uncommitted** worktree edit).

### 4.4 Independent corroboration from a sibling seat

While I was writing this report, the sibling seat `ExecDriftLive` produced its own live run of the same tool and wrote
it to `.ufo/waves/round-36/evidence/drift-live-r36.txt`. Its result is identical to mine, from a separate invocation:

```
$ grep " drifted$" .ufo/waves/round-36/evidence/drift-live-r36.txt
S156 drifted
S157 drifted
S158 drifted
S159 drifted
S160 drifted
S176 drifted
S177 drifted
S210 drifted
S211 drifted
$ tail -1 .ufo/waves/round-36/evidence/drift-live-r36.txt
MORI_SOURCE_DRIFT rows=220 fresh=49 excerpt=0 drifted=9 unavailable=0 no-copy=162
```

Two independent invocations, the same nine ids, the same summary counters. At the time of writing, the stale "seven"
claim is still present in the worktree at `corpus/knowledge/source-drift-r36.md:17` and `corpus/QUALITY.md:841`
(verified by grep after the sibling seat's edit landed). The defect is live, not a transient.

### 4.5 Precise defect statement

`corpus/knowledge/source-drift-r36.md:17` and `corpus/QUALITY.md:841` (and `SKILL.md:860`) assert that the drifted set is
**seven** rows and that **all** of them were representation differences. Measured at the landed tip with the frozen
counter and the landed tool, the drifted set is **nine** rows (`S156 S157 S158 S159 S160 S176 S177 S210 S211`), and two of
them are not representation differences: S210's live bytes differ from the copy in the site's asset bundle
(sha256 `9b8f63b6…` vs the recorded/copied `64c60354…` — QUALITY 105's own test calls this a source change), and S211
is byte-unstable by construction (per-session `ncbi_phid` / `csrfmiddlewaretoken`), so it can never classify `fresh`
and its `drifted` verdict is uninformative. The counter and the receipt are not implicated — the tool and the oracle
agree on all 220 rows, and both correctly report nine.

---

## 5. Secondary observations (not defects, recorded for the parent)

1. **The C1 receipt is a worktree file, not a committed artifact.** `evidence/c1-after.txt` and `evidence/c2-after.txt`
   are untracked at `bf0df77` (`git status --porcelain` → `?? .ufo/waves/round-36/evidence/c1-after.txt`,
   `?? .ufo/waves/round-36/evidence/c2-after.txt`). The brief cites them as "data receipt evidence/c2-after.txt" /
   "evidence/c1-after.txt"; at the landed tip they are not in the commit. Not a C1-predicate defect — the counter is
   what the freeze pins — but the receipts are not yet durable.

2. **A dirty `corpus/` flips the whole C1 verdict.** `count-c1.py:571-577` requires the worktree `corpus/` to equal the
   rev (no diff, no untracked file). With `corpus/README.md` modified (an in-flight uncommitted edit), the same frozen
   counter at the same rev returns:

   ```
   blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
   real=unmet worktree_corpus_differs_from_rev
   C1=unmet
   EXIT=1
   ```

   That is the v2 design working as intended (the K9 harness-keyed defence), but it means any C1 re-score by another
   seat must run against a clean `corpus/` or it will report `C1=unmet` for a reason unrelated to the tool. My three
   passing draws were run before the `corpus/README.md` edit landed in the worktree (mtime 15:41 local; my draws
   15:33–15:39 local); the fourth draw above, after it, shows the flip.

3. **A dirty `corpus/` also puts the corpus out of step with `evidence/c0-rescore-v2.txt`'s base corpus.** The C0
   re-score ran against 204 rows / 7 drifted (base `6bd57097`); the landed corpus has 220 rows / 9 drifted. Any seat
   quoting "7 drifted" from the C0 receipt as the current state is quoting the pre-round corpus.

4. **The probe's `excerpt` state never fired on any real row** in any run (`excerpt=0`, `fresh=49`, `drifted=9`,
   `no-copy=162`). 162 of 220 rows have no copy file at all, so the tool cannot observe them. This is consistent with
   the contract's design and is disclosed in the knowledge doc's `no-copy` cell; recorded here because the real arm's
   `oracle_fetched=58` is the only part of the corpus the probe can say anything about.

---

## 6. Verdict

The **counter and the predicate are sound**: the P-C1 sentence is byte-identical to `contract.md:21`
(`304a3d0a…771c2a`), the blind arm is 40/40 with `mismatches=0`, the real arm meets every threshold
(`oracle_fetched=58 oracle_fresh=49 oracle_drifted=9 oracle_excluded=0 mismatches=0` over 220 rows), `C1=met` with
exit 0, a fresh seed is printed on every run, the counter's sha256 matches the `evidence/freeze-v2.txt` pin
(`86dd3b7a…c8764c0`), three independent draws agree, and two substitute programs (K2 all-fresh, K5 denial) are
correctly rejected — the counter discriminates.

**But the landed corpus documentation of the drift result is wrong**, and that documentation is the place where the
C1 probe's byte verdict gets turned into a statement about sources. `corpus/knowledge/source-drift-r36.md:17` and
`corpus/QUALITY.md:841` (with `SKILL.md:860`) say **seven** drifted rows, all representation differences; the frozen
counter and the landed tool measure **nine**, and S210 and S211 are two drift kinds the landed criterion does not
cover — S210 by QUALITY 105's own sha256 test counts as a changed source, and S211 is byte-unstable so it can never be
`fresh`.

This finding does **not** assert a freshness verdict for C1, does not disturb C2, and does not claim the probe is wrong —
the tool and the oracle agree on every row. It asserts that the landed prose misstates what the landed probe measures
on the landed corpus, and that QUALITY 105 (the round's own guard for this failure mode) is built on that misstatement.

Defect, with path:line evidence:

- `corpus/knowledge/source-drift-r36.md:17` — "the **seven** `drifted` rows were five annotated excerpts from round 30
  (S156–S160 …) and two docs.python.org pages … (S176, S177)"; measured drifted set is nine
  (`S156 S157 S158 S159 S160 S176 S177 S210 S211`), and the sentence "That is not the same as a changed source" is
  false for S210 (`corpus/evidence/sources-r36/S210.src` sha256 `64c60354…` == the digest recorded at
  `corpus/lessons/round-32.md:43`; live sha256 `9b8f63b6…` — they differ, so by `corpus/QUALITY.md:837-839` it is a
  source change) and unsatisfiable for S211 (per-session `ncbi_phid` / `csrfmiddlewaretoken`; four distinct hashes for
  one URL, so it can never classify `fresh`).
- `corpus/QUALITY.md:841` — "all seven real drifted rows were representation differences"; the count is nine and two
  of the nine are not representation differences. `corpus/QUALITY.md:843` — "Not covered: semantic drift of a page whose
  bytes never change" omits the two cases that actually occurred.
- `SKILL.md:860` — repeats the same seven-row list.
- `corpus/README.md:565` — "all 9 oracle-drifted rows were representation differences (annotated excerpts S156–S160,
  docs.python.org build footers S176/S177)": says 9, lists 7 ids, and the file is currently an uncommitted worktree
  edit.
- Counter-side evidence (no defect found): the frozen counter at `bf0df77` reports `oracle_drifted=9` in three
  independent fresh-seed draws and in the L1's receipt `evidence/c1-after.txt`; the mismatch is in the prose, not the
  measurement.

**Item attacked:** the C1 frozen byte predicate P-C1 (`.ufo/waves/round-36/count-c1.py` against
`tools/mori-source-drift.py` at revision `bf0df77fee4b6ef54a90aea09335c7617f125151`), re-scored with a fresh network
draw. Byte-behavior evidence only; **no freshness admission is claimed or inferred from it** (C1 is exploratory per
`contract.md:113-124` and `w1/CritAxisFit.md`).

VERDICT: FAIL
