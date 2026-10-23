# ExecDriftLive — live drift-probe run against the round-36 C1 receipt

Seat: `mori-r36-w2-ExecDriftLive-11` (leaf; no subagent dispatch).
Item attacked: **the live byte behaviour of the landed C1 probe** `tools/mori-source-drift.py` and its
agreement with the round-36 data receipt `.ufo/waves/round-36/evidence/c1-after.txt`
(`real_rows=220 oracle_fetched=58 oracle_fresh=49 oracle_drifted=9 oracle_excluded=0 tool_exit=1
tool_rows=220 mismatches=0`), and with the lane's own registry row count.

Scope: read-only measurement only. No lane file was edited, no git/jj mutating command was run, no
remediation. Scratch (own code, live fetches, captured outputs):
`/fast/scratch/hyaku/mori-r36/ExecDriftLive/` — `oracle_check.py` (an independent re-implementation of
the contract's classification rules, written from `contract.md:35-47`, **not** from the tool's source),
`oracle.json`, `tool-run.txt`, `tool-run2.txt`, `tool-run.exit`, live bodies `S176.live`, `S177.live`,
`S210.live`, `S211.live`, `s211.1/2/3`.

No tools were installed or upgraded (host already had `python3` 3.14.8, `curl` 8.23.0 / OpenSSL 3.6.5).

## 1. The live run (full output)

Command (from the lane repo root; the probe is read-only):

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin && python3 tools/mori-source-drift.py --root /home/vgpnk/Projects/shokunin/mori-shokunin
```

Output (220 row lines + 1 summary line; captured verbatim in
`/fast/scratch/hyaku/mori-r36/ExecDriftLive/tool-run.txt`):

```
S001 no-copy
S002 no-copy
S003 no-copy
S004 no-copy
S005 no-copy
S006 no-copy
S007 no-copy
S008 no-copy
S009 no-copy
S010 no-copy
S011 no-copy
S012 no-copy
S013 no-copy
S014 no-copy
S015 no-copy
S016 no-copy
S017 no-copy
S018 no-copy
S019 no-copy
S020 no-copy
S021 no-copy
S022 no-copy
S023 no-copy
S024 no-copy
S025 no-copy
S026 no-copy
S027 no-copy
S028 no-copy
S029 no-copy
S030 no-copy
S031 no-copy
S032 no-copy
S033 no-copy
S034 no-copy
S035 no-copy
S036 no-copy
S037 no-copy
S038 no-copy
S039 no-copy
S040 no-copy
S041 no-copy
S042 no-copy
S043 no-copy
S044 no-copy
S045 no-copy
S046 no-copy
S047 no-copy
S048 no-copy
S049 no-copy
S050 no-copy
S051 no-copy
S052 no-copy
S053 no-copy
S054 no-copy
S055 no-copy
S056 no-copy
S057 no-copy
S058 no-copy
S059 no-copy
S060 no-copy
S061 no-copy
S062 no-copy
S063 no-copy
S064 no-copy
S065 no-copy
S066 no-copy
S067 no-copy
S068 no-copy
S069 no-copy
S070 no-copy
S071 no-copy
S072 no-copy
S073 no-copy
S074 no-copy
S075 no-copy
S076 no-copy
S077 no-copy
S078 no-copy
S079 no-copy
S080 no-copy
S081 no-copy
S082 no-copy
S083 no-copy
S084 no-copy
S085 no-copy
S086 no-copy
S087 no-copy
S088 no-copy
S089 no-copy
S090 no-copy
S091 no-copy
S092 no-copy
S093 no-copy
S094 no-copy
S095 no-copy
S096 no-copy
S097 no-copy
S098 no-copy
S099 no-copy
S100 no-copy
S101 no-copy
S102 no-copy
S103 no-copy
S104 no-copy
S105 no-copy
S106 no-copy
S107 no-copy
S108 no-copy
S109 no-copy
S110 no-copy
S111 no-copy
S112 no-copy
S113 no-copy
S114 no-copy
S115 no-copy
S116 no-copy
S117 no-copy
S118 no-copy
S119 no-copy
S120 no-copy
S121 no-copy
S122 no-copy
S123 no-copy
S124 no-copy
S125 no-copy
S126 no-copy
S127 no-copy
S128 no-copy
S129 no-copy
S130 no-copy
S131 no-copy
S132 no-copy
S133 no-copy
S134 no-copy
S135 no-copy
S136 no-copy
S137 no-copy
S138 no-copy
S139 no-copy
S140 no-copy
S141 no-copy
S142 no-copy
S143 no-copy
S144 no-copy
S145 no-copy
S146 no-copy
S147 no-copy
S148 no-copy
S149 no-copy
S150 no-copy
S151 no-copy
S152 no-copy
S153 no-copy
S154 no-copy
S155 no-copy
S156 drifted
S157 drifted
S158 drifted
S159 drifted
S160 drifted
S161 fresh
S162 fresh
S163 fresh
S164 fresh
S165 fresh
S166 no-copy
S167 fresh
S168 no-copy
S169 fresh
S170 fresh
S171 fresh
S172 fresh
S173 fresh
S174 fresh
S175 fresh
S176 drifted
S177 drifted
S178 no-copy
S179 no-copy
S180 fresh
S181 fresh
S182 fresh
S183 fresh
S184 fresh
S185 fresh
S186 fresh
S187 fresh
S188 fresh
S189 fresh
S190 fresh
S191 fresh
S192 fresh
S193 fresh
S194 fresh
S195 fresh
S196 fresh
S197 fresh
S198 fresh
S199 fresh
S200 no-copy
S201 no-copy
S202 no-copy
S203 fresh
S204 fresh
S205 fresh
S206 fresh
S207 fresh
S208 fresh
S209 fresh
S210 drifted
S211 drifted
S212 fresh
S213 fresh
S214 fresh
S215 fresh
S216 fresh
S217 fresh
S218 fresh
S219 fresh
S220 fresh
MORI_SOURCE_DRIFT rows=220 fresh=49 excerpt=0 drifted=9 unavailable=0 no-copy=162
```

Exit code: **1** (the tool's contract: 1 when any row is `drifted`, `contract.md:47`; `SKILL.md:872`
registry row "1 `drifted>0`"). stderr empty.

A second identical run (`tool-run2.txt`) produced a **byte-identical** file
(`diff tool-run.txt tool-run2.txt` → no output; exit 1 again). The run is deterministic even though
one of the drifted rows is served with a per-request nonce (see §5).

## 2. Check A — `rows=N` equals the registry row count

The tool's registry regex is `ROW_RE = re.compile(r"^\| S\d{3} ")` (`tools/mori-source-drift.py:41`),
i.e. a line starting `| S` + three digits **plus a space**.

```
$ grep -cE '^\| S[0-9]{3} ' corpus/SOURCES.md
220
$ grep -oE '^\| (S[0-9]{3})' corpus/SOURCES.md | sort -u | wc -l
220
$ grep -cE '^S[0-9]{3} ' /fast/scratch/hyaku/mori-r36/ExecDriftLive/tool-run.txt
220
```

Registry rows = 220, unique ids = 220, tool row lines = 220, tool summary `rows=220`. No duplicate id
in the tool output (`grep -oE '^S[0-9]{3}' tool-run.txt | sort | uniq -d` → empty). **A holds.**

## 3. Check B — the summary counts sum to N

```
$ python3 -c "import re;s=open('tool-run.txt').read().splitlines()[-1];d=dict(re.findall(r'(\w+)=(\d+)',s));print('rows=',d['rows'],'sum=',sum(int(v) for k,v in d.items() if k!='rows'),'match=',sum(int(v) for k,v in d.items() if k!='rows')==int(d['rows']))"
rows= 220 sum= 220 match= True
```

49 + 0 (excerpt) + 9 (drifted) + 0 (unavailable) + 162 (no-copy) = 220 = `rows`. **B holds.**

## 4. Check C — the drifted ids against the receipt

The receipt (`.ufo/waves/round-36/evidence/c1-after.txt:2-3`) states counts, not ids:

```
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
real_rows=220 oracle_fetched=58 oracle_fresh=49 oracle_drifted=9 oracle_excluded=0 tool_exit=1 tool_rows=220 mismatches=0
```

Live tool counts vs the receipt's counter/oracle subset:

| quantity | receipt (counter, `c1-after.txt:3`) | live tool run (full 220) | live independent oracle (58 copy rows) |
|---|---|---|---|
| rows | `real_rows=220` | `rows=220` | 220 parsed |
| tool rows | `tool_rows=220` | 220 | — |
| tool exit | `tool_exit=1` | 1 | — |
| fetched (oracle subset) | `oracle_fetched=58` | 58 (= rows with a copy) | 58 |
| fresh | `oracle_fresh=49` | `fresh=49` | 49 |
| drifted | `oracle_drifted=9` | `drifted=9` | 9 |
| unavailable | (0 rows unavailable to the tool; `oracle_excluded=0`) | `unavailable=0` | 0 |
| excluded | `oracle_excluded=0` | — | 0 |
| mismatches | `mismatches=0` | 0 disagreements vs my oracle | — |

The tool's whole-row partition (49 fresh + 9 drifted = 58) coincides **exactly** with the counter's
oracle subset (58 fetched = 49 + 9): every row the oracle classified was also classified by the tool,
none was `unavailable` to the tool, none was excluded.

**Drifted ids (live tool run, 9):** `S156, S157, S158, S159, S160, S176, S177, S210, S211`.

Because the receipt pins `oracle_drifted=9` with `mismatches=0`, the oracle's drifted set at the tip is
the same set of nine. I re-derived the set independently of the tool's code
(`oracle_check.py`, rules re-written from `contract.md:35-47`; registry parse, newest-`N` copy
resolution, fetch, sha256 → fresh → contiguous-substring → excerpt → drifted):

```
$ python3 /fast/scratch/hyaku/mori-r36/ExecDriftLive/oracle_check.py
independent rows=220 {"drifted": 9, "fresh": 49, "no-copy": 162}
independent drifted=['S156', 'S157', 'S158', 'S159', 'S160', 'S176', 'S177', 'S210', 'S211']
independent fresh=49 ids
```

Per-row comparison over **all 220** rows (tool output vs my independent oracle):

```
tool rows parsed: 220 independent rows: 220
registry row count (tool ROW_RE '| Sddd '): 220
id sets equal: True
per-row disagreements: 0 {}
tool histogram: {'no-copy': 162, 'drifted': 9, 'fresh': 49}
independent histogram: {'no-copy': 162, 'drifted': 9, 'fresh': 49}
```

**0 disagreements.** The receipt's counts are reproduced live, and the drifted id set is stable.

Custody of the receipt: the frozen counter bytes still match the pin, so `c1-after.txt` is a receipt
of *this* claim:

```
$ grep -E 'count-c[12]' .ufo/waves/round-36/evidence/freeze-v2.txt
86dd3b7ab2d2563bbc811e83717b35dfea3d69717dab4d41d454f8b87c8764c0  count-c1.py
c7edaacfff029c2055bee6ddda42ff6f5c040dad7fbac81e9d169602edcbac34  count-c2.py
$ sha256sum .ufo/waves/round-36/count-c1.py .ufo/waves/round-36/count-c2.py
86dd3b7ab2d2563bbc811e83717b35dfea3d69717dab4d41d454f8b87c8764c0  .ufo/waves/round-36/count-c1.py
c7edaacfff029c2055bee6ddda42ff6f5c040dad7fbac81e9d169602edcbac34  .ufo/waves/round-36/count-c2.py
```

Also verified: the copy files are the newest-`N` ones and each id has **at most one** copy, so the
`highest N` selection rule is not exercised by this corpus (the blind arm covers it):

```
copies total: 58 | with 'id: S' header: 5 (S156.txt..S160.txt) | without header: 53
ids with >1 copy: {}
copy dirs: ['sources-r30','sources-r31','sources-r32','sources-r33','sources-r34','sources-r35','sources-r36']
```

## 5. What the drifted rows actually are (mechanism, per row)

Bytes fetched by me now vs the committed copy (independent fetches, `--location`, UA
`mori-r36-independent-oracle`):

- **S156, S157, S158, S159, S160** (copies `sources-r30/S15*.txt`, annotated excerpts with a 5-field
  header). The copy's `sha256:` header (line 3) equals the **live full-document** sha for all five:

  ```
  S156 header=b56aa781be9c29b610156925030d3c4ab720c0ad73d57907d230ca3047302f2a live=b56aa781… match=YES
  S157 header=47e98d394462e05b…  live=47e98d394462e05b…  match=YES
  S158 header=428dc8308d5caf70…  live=428dc8308d5caf70…  match=YES
  S159 header=dc5a771c9ed178751…  live=dc5a771c9ed178751…  match=YES
  S160 header=285b3d0c1217b9a3…  live=285b3d0c1217b9a3…  match=YES
  ```

  The source bytes are unchanged; the *copy file* differs because it carries the header and
  line-number prefixes. Representation difference, not a changed source.
- **S176, S177** (`sources-r32/S176.src`, `S177.src`): the only difference is the docs.python.org build
  footer (`diff` shows one hunk each):

  ```
  721c721
  <       Last updated on Oct 23, 2026 (00:01 UTC).
  ---
  >       Last updated on Oct 23, 2026 (18:17 UTC).
  370c370
  <       Last updated on Oct 23, 2026 (00:01 UTC).
  ---
  >       Last updated on Oct 23, 2026 (18:17 UTC).
  ```

  Rebuild of the page, source semantics unchanged.
- **S210** (`sources-r36/S210.src`, sha `64c603545b3f9799…`): live body sha `9b8f63b653029da4…`,
  122331 B vs 122463 B copy; the diff is **two** lines only — the stylesheet link and the script tag
  (`application.min.<digest>.css` / `.js`, plus the `integrity=` attributes present in the copy and
  absent live). The man-page prose is byte-identical; the site's asset build changed.
- **S211** (`sources-r36/S211.src`, sha `a4e104ec9d6da304…`): the copy is a raw `curl` body of
  `pmc.ncbi.nlm.nih.gov/articles/PMC5856500/`. Live body differs in **four** lines only — the
  `ncbi_phid` meta and the `csrfmiddlewaretoken` hidden input. Three consecutive fetches give three
  different shas (`7c2cc201…`, `c9e88c6f…`, `b1193c00…`), so this row is **structurally incapable of
  ever being `fresh`**: the difference is a per-request nonce, not the source. It is also a *rejected*
  row (`SOURCES.md:217`, status `rejected`, duplicate URL already named by S056).

## 6. Finding — the landed corpus text enumerates **seven** drifted rows; the round's own receipt and
## the live probe both say **nine**

The landed documentation at the tip `bf0df77` describes the drifted set as seven rows and names only
those seven:

- `corpus/knowledge/source-drift-r36.md:17` — "seven `drifted` rows were five annotated excerpts from
  round 30 (S156–S160: header lines and line-number prefixes; each header's full-document sha256 still
  equals the live body) and two docs.python.org pages whose only change is the build footer (S176,
  S177)".
- `corpus/QUALITY.md:841` (criterion 105, "Shown able to fail") — "all seven real drifted rows were
  representation differences (S156–S160 annotated excerpts whose header sha256 equals the live body;
  S176/S177 build footers)".
- `SKILL.md:860` — names only "annotated excerpts (round 30, S156–S160) and rebuilt doc pages
  (S176, S177)".

But the same tip's data receipt says `oracle_drifted=9` (`evidence/c1-after.txt:3`), and the live probe
at that same tip prints `drifted=9` with the two extra ids `S210` and `S211` (both round-36 copies
under `corpus/evidence/sources-r36/`). The "seven" figure is the wave-1 population, before the r36
copies S205–S220 existed; it was carried into the landed text unchanged. Three landed files therefore
contradict the receipt they ship with, and the knowledge note's reader-action table
(`source-drift-r36.md:25`) has no guidance for the two rows it does not know about — for S210 and S211
that guidance would have to conclude "diff shows only site chrome / a per-request token, the taught
passage is unchanged".

Two consequences, both measured:

1. **Enumeration is wrong at the tip.** Any reader who runs the probe and sees `drifted=9` with S210 and
   S211 unnamed in the standing guidance is reading guidance written for a population that no longer
   exists. (`corpus/README.md` carries a *worktree* edit from a concurrent seat at 15:41 local that
   says "all 9 oracle-drifted rows were representation differences (annotated excerpts S156–S160,
   docs.python.org build footers S176/S177)" — it corrects the count to 9 but still enumerates only
   seven ids and does not name S210/S211. That file is uncommitted and not mine; recorded as
   observation.)
2. **Criterion 105's own procedure is not executable for the two rows the receipt counts as
   drifted.** `corpus/QUALITY.md:837-843` requires: "for every real row a counter counts as drifted,
   compare the source's full-document sha256 with the one recorded when the row was opened (**the copy
   header or the lesson Gate**), and count the row as a source change only when they differ."
   - Neither `sources-r36/S210.src` nor `sources-r36/S211.src` carries a `sha256:` header (only the
     five `sources-r30/S15*.txt` excerpts do — measured: 5 of 58 copies have an `id: S` header), and
     `corpus/lessons/round-36.md` does not exist at the tip (`git cat-file -e
     bf0df77…:corpus/lessons/round-36.md` → "path does not exist"; `corpus/lessons/` ends at
     `round-35.md`). So for S211 there is **no recorded sha in either place the criterion names**
     (its sha `a4e104ec…` survives only in the wave-1 report `.ufo/waves/round-36/w1/SupS179.md:17`),
     and the mechanical rule, applied to the next-best available digest, would report S211 and S210 as
     *source changes* — while the diffs show only a site-asset rebuild and a per-request CSRF token.
   - The criterion's stated reason for existing is precisely "a freshness or drift witness is checked
     for what changed before it is used as a target"; applied mechanically to these two rows it
     produces a false "changed source" verdict, which is the failure mode the criterion was written to
     prevent.

I report this as a measured defect; remediation is out of scope for this seat (mori province: detect
and report only). Sibling seat `RevQuality105` (w2) also observed the 9-vs-7 gap but scoped it out
("S210/S211 additionally drifted — round-36 supersede rows whose copies are raw HTML, outside this
item") and still passed criterion 105.

**Note on `excerpt`:** `excerpt=0` in the live run and in my oracle. The tool compares the *whole copy
file* (header + line-number-prefixed lines) against the fetched body, so the five r30 excerpt copies
cannot be contiguous substrings of the body and land as `drifted`, not `excerpt`. That is the contract's
rule (`contract.md:42-44`) applied to annotated excerpts; consistent with the wave-1 analysis that these
rows are representation differences. No defect here — recorded so the `excerpt=0` figure is not read as
"the excerpt path is broken".

## 7. Risk for the parent's post-integration gate (not my item, observed)

The counter's real arm refuses to run when the worktree `corpus/` differs from the measured revision
(`count-c1.py:575-580`: `git diff --quiet <rev> -- corpus` and no untracked file under `corpus/`). Right
now a **concurrent seat has modified `corpus/README.md`** in the worktree (uncommitted; the diff adds
a "Round-36 coverage additions" section), so:

```
$ git diff --quiet bf0df77fee4b6ef54a90aea09335c7617f125151 -- corpus/ ; echo $?
1
$ git status --porcelain -- corpus/
 M corpus/README.md
$ git ls-files --others --exclude-standard -- corpus/ | wc -l
0
```

A re-run of `count-c1.py bf0df77…` in this state would return
`real=unmet worktree_corpus_differs_from_rev`, not the receipt's verdict. `corpus/SOURCES.md` and
`corpus/evidence/sources-r36/` are untouched (identical to the tip), so the drift measurement above is
unaffected. I made no change to the lane; this is a read-only observation for whoever owns the gate.

## 8. Freshness-admission scan (C1 must not be read as a freshness verdict)

Searched the landed lane corpus for any place that infers freshness admission from C1: `grep -rn
'C1=met|freshness (is|was) (proven|established|admitted)|proves freshness|admit.{0,20}fresh'` over the
lane → no hit outside historical wave JSON. The standing texts actively disclaim it:
`corpus/knowledge/source-drift-r36.md:15` ("`fresh` proves only byte identity with the committed copy,
never that the row's `teaches` is right"), `SKILL.md:872` (exit 0 is "not proof every URL was
reachable"), `corpus/README.md:565` (worktree edit, "no freshness verdict is claimed from it"), and
`corpus/QUALITY.md:104` ("A green C1 fixture gate does not establish freshness"). No freshness admission
is inferred from the probe anywhere I can see.

## 9. What my item attacks, and the result

Attacked: the live byte behaviour of `tools/mori-source-drift.py` at the landed tip
`bf0df77fee4b6ef54a90aea09335c7617f125151` and its agreement with the round-36 C1 receipt
`evidence/c1-after.txt`, plus the drifted id set and the lane's own description of that set.

- rows=N (220) = registry row count (220 unique ids): **holds**.
- summary counts sum to N (49+0+9+0+162 = 220): **holds**.
- receipt agreement on every printed quantity (`real_rows=220`, `tool_rows=220`, `tool_exit=1`,
  `oracle_fetched=58`, `oracle_fresh=49`, `oracle_drifted=9`, `oracle_excluded=0`, `mismatches=0`):
  **holds**; the drifted id set (`S156–S160, S176, S177, S210, S211`) reproduces under an independent
  re-implementation with **0** per-row disagreements across all 220 rows; two runs byte-identical;
  frozen-counter sha256 still matches `evidence/freeze-v2.txt`.
- **Defect found (documentation/enumeration, adjacent to my item but measured here):** the landed
  corpus text at `corpus/knowledge/source-drift-r36.md:17`, `corpus/QUALITY.md:841` and `SKILL.md:860`
  states **seven** drifted rows (S156–S160, S176, S177) while the same tip's receipt and the live probe
  both give **nine** (adds S210, S211); and criterion 105's prescribed procedure
  (`corpus/QUALITY.md:837-843`, "the copy header or the lesson Gate") has no recorded full-document
  sha256 available for either of the two rows the receipt counts as drifted, because the r36 copies
  carry no `sha256:` header (5 of 58 copies do) and `corpus/lessons/round-36.md` does not exist at the
  tip — so the mechanical rule would mislabel a site-asset rebuild (S210) and a per-request CSRF nonce
  (S211, proven unreproducible across three consecutive fetches) as source changes.

VERDICT: FAIL

Defect path:line evidence —
`/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/knowledge/source-drift-r36.md:17` (and `:25`),
`/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/QUALITY.md:841` (and `:837-843`),
`/home/vgpnk/Projects/shokunin/mori-shokunin/SKILL.md:860`; contradicted by
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/evidence/c1-after.txt:3`
(`oracle_drifted=9`) and by the live run above (`drifted=9`, ids `S156, S157, S158, S159, S160, S176,
S177, S210, S211`).

The probe itself and the receipt agree exactly (Checks A, B, C all pass); the failure is the landed
narrative and criterion 105's applicability to the two rows the round's own counter counts as drifted.
