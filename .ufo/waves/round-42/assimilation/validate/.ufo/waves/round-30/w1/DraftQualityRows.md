# Round 30 W1 — draft QUALITY criteria 88–92 (routed R1, R2, R3, R5/M2, R6)

Seat `MoriR30.DraftQualityRows`, leaf (no subagents, no background jobs). Entering tip `a66751b1a97fb6422a4756f867d94269de9bcdd5`, per
`.ufo/waves/round-30/contract.md:4`. Wrote only this report and `/fast/scratch/hyaku/mori-r30/MoriR30.DraftQualityRows/`; no lane
file, product code, tool, fixture or counter edited; no install needed. No writer was messaged.

## 1. Product

Five criteria numbered 88–92 (last is 87 at `corpus/QUALITY.md:448-460`; the round-29 note ends at `:464`), each with a statement, a
check I ran, and a committed revision where it fails. Ready-to-paste text is §3.

## 2. Checks run (committed bytes; scratch repos are mine)

| # | command | target | observed | exit |
|---|---|---|---|---|
| 88 | `check-tip-receipts.sh b581173a 29` | lane `b581173a` | `cited_lane=no` for both counters, `tip_receipts=unmet` | 1 |
| 88 pass | `check-tip-receipts.sh 1fc6bb0 28` | lane `1fc6bb0` | `tip_receipts=met`; batch adds exactly the three receipts | 0 |
| 89 | inline check 89 | lane `a66751b1` r29 | `line=65`, `absence_reject_rows=1 malformed=1` | 1 |
| 89 pass | inline check 89 on `lab` | scratch `aba1e5d` | `absence_reject_rows=1 malformed=0` | 0 |
| 90 | inline check 90 | lane `a66751b1` r29 | `word_labels=16 mismatched=5` (lines 57, 60, 61, 62, 63) | 1 |
| 90 pass | inline check 90 on `lab` | scratch `9adf993` | `word_labels=3 mismatched=0` | 0 |
| 91 | `git cat-file -e a66751b1:.ufo/waves/round-30/check-blind-wave.sh` | lane `a66751b1` | path absent | 128 |
| 91 | committed `d6d5cb0a` gate with `--selftest` | lane `d6d5cb0a` | `usage: check-blind-wave.sh <lane-rev> <wave-report-dir> <writer-name-regex>` | 2 |
| 92 | inline check 92 | lane `a66751b1` | `missing_case_file=…/cases-a2-r30.json` | 2 |
| 92 pass | inline check 92 on `lab` | scratch `aba1e5d` | `pinned=1 limit_stated=yes frozen=yes` | 0 |
| 92 red | `lab2` / `lab4` / `lab5` | scratch | `pinned=0` / `frozen=no` / `limit_stated=no` | 1 |

At `b581173a` the batch adds only `tip-c1.txt`, `tip-c2.txt`, `tip-retention.txt`; the two counter receipts are cited only in
`SCORECARD.md:1796-1797` (spot-check `:154-156`). At `1fc6bb0`, `LOG.md` at the parent already names `tip-count-c1.txt`, so the citation predates the receipts batch.

````markdown
## Criteria added round 30 — round-29 routed defects

88. A round's tip receipts are cited by name in the files its tip check reads — `LOG.md` and
    `corpus/lessons/round-<N>.md` — before the receipts-only batch that lands them, so the tip holds the citations
    without editing a report. `bash .ufo/waves/round-28/check-tip-receipts.sh <tip> <N>` prints `tip_receipts=met`,
    exit 0. A receipt cited only in another report (`SCORECARD.md`) prints `cited_lane=no` for that counter and
    `tip_receipts=unmet`, exit 1. The check credits a receipt named in either default report, so a `met` line proves
    the receipts are named where the check reads, not that each of the two files names each receipt; a round claiming
    this row records the per-file counts beside the `met` line. Because QUALITY 87 lets the tip batch add only receipt
    files, a citation read at the tip was written in an earlier batch. ← lessons/round-29-verifier-spotcheck.md:154-156
    (routed R1); lessons/round-29.md:102-103 (M4); QUALITY 84, 87.
    Check: `bash .ufo/waves/round-28/check-tip-receipts.sh <tip> <N>` prints one `counter=…` or
    `retention receipt=…` line per required receipt and then `tip_receipts=met|unmet`; exit 0 met, 1 unmet, 2 on a
    bad revision or missing input. It FAILS at `b581173a` (round-29 tip: `counter=count-c1.sh … cited_lane=no`,
    `counter=count-c2.sh … cited_lane=no`, `tip_receipts=unmet`, exit 1; its batch adds only the three receipts) and
    PASSES at `1fc6bb0` (round-28 tip: batch adds exactly `tip-count-c1.txt`, `tip-count-c2.txt`, `tip-retention.txt`;
    `tip_receipts=met`, exit 0; `LOG.md` at the parent already names `tip-count-c1.txt`). Red inputs: a receipt cited
    only in `SCORECARD.md` (round 29's state); a receipts batch that also edits `LOG.md` or the lesson (QUALITY 87's
    `tip_adds_nonreceipt`); a receipt naming its own hash instead of the first parent.

89. A `## Gate` reject row whose reason asserts absence — matching `no line`, `no match`, `no matches`, `no hit`,
    `no occurrence` or `returned no` (case-insensitive) — carries the exact `grep` invocation it ran in backticks and
    that invocation's output in the same row: `exit 1` (grep's own no-match status) or a printed `0`. A row that
    narrates the absence without command and output is malformed even when its decision is right; a reason that
    asserts a fact (a declaration, a duplicate URL, an HTTP status) is out of scope. ←
    lessons/round-29-verifier-spotcheck.md:157-158 (routed R2); lessons/round-29.md:65 (the S155 reject row: "a
    case-insensitive grep for `dryrun` and `version` returned no line in either file", with no command and no output).
    Check, over committed bytes:

    ```sh
    lane=<lane>; rev=<rev>; round=<N>
    git -C "$lane" cat-file -e "$rev:corpus/lessons/round-$round.md" || { echo missing_lesson; exit 2; }
    git -C "$lane" show "$rev:corpus/lessons/round-$round.md" | python3 -I -B -c '
    import re,sys
    ab = re.compile(r"\b(no line|no match(?:es)?|no hit|no occurrence|returned no)\b",re.I)
    cmd = re.compile(r"`[^`]*\bgrep\b[^`]*`")
    wit = re.compile("exit[ =]1\\b|\u2192\\s*`?0\\b|0 matches",re.I)
    g = 0
    rows = bad = 0
    for ln,line in enumerate(sys.stdin,1):
        s = line.rstrip("\n")
        if re.match(r"^##\s+Gate\b",s): g = 1; continue
        if g and re.match(r"^##\s",s): g = 0; continue
        if not g or not s.startswith("|"): continue
        d = s.rstrip().rstrip("|").rsplit("|",1)[-1].strip()
        if not d.startswith("reject,") or not ab.search(d[7:]): continue
        rows += 1
        if not (cmd.search(s) and wit.search(s)):
            bad += 1
            print("line=%d absence_reason_without_grep_command_or_output" % ln)
    print("absence_reject_rows=%d malformed=%d" % (rows,bad))
    sys.exit(0 if bad == 0 else 1)'
    ```

    prints `absence_reject_rows=<n> malformed=<n>`, exit 0 when malformed=0, 1 otherwise, 2 on a missing lesson. It
    FAILS at `a66751b1` on the round-29 Gate (`line=65`, `absence_reject_rows=1 malformed=1`, exit 1) and PASSES on
    a scratch Gate row carrying `` `grep -in dryrun f.go` → `0`, exit 1 `` (`absence_reject_rows=1 malformed=0`,
    exit 0). Red inputs: the round-29 row as written; a row whose only "command" is the word grep in prose; a row
    carrying the command but no output.

90. Every word-count label in a `## Gate` table and in `corpus/SOURCES.md` — a `(N words)` before a quote
    (`(N words): "…"`) or after one (`"…" (N words)`), including `/`-joined pairs — equals `wc -w` of the quoted text
    as carried in the file, between the quote marks, with `\|` still counted as a whitespace-separated token. A label
    that differs by one is a defect, not rounding. A Gate row with no located quote is QUALITY 86's business; this
    row measures labels that exist, and requires at least one (`n>0`) so a Gate that carries no label fails rather
    than passing vacuously. ← lessons/round-29-verifier-spotcheck.md:159 (routed R3); lessons/round-29.md:57, :60-63.
    Check, over committed bytes:

    ```sh
    lane=<lane>; rev=<rev>; round=<N>
    git -C "$lane" cat-file -e "$rev:corpus/lessons/round-$round.md" || { echo missing_lesson; exit 2; }
    git -C "$lane" cat-file -e "$rev:corpus/SOURCES.md" || { echo missing_sources; exit 2; }
    { echo "@@LESSON"; git -C "$lane" show "$rev:corpus/lessons/round-$round.md"
      echo "@@SOURCES"; git -C "$lane" show "$rev:corpus/SOURCES.md"; } | python3 -I -B -c '
    import re,subprocess,sys
    Q = r"\"((?:[^\"\\]|\\.)*)\""
    after = re.compile(Q + r"\s*\((\d+) words?\)")
    before = re.compile(r"\((\d+) words?\)\s*:\s*(" + Q + r"(?:\s*/\s*" + Q + r")*)")
    unit = re.compile(Q)
    def wc(q):
        return int(subprocess.run(["wc","-w"],input=q.encode(),stdout=subprocess.PIPE).stdout.split()[0])
    src = ""; gate = 0; n = bad = 0; el = 0
    for line in sys.stdin:
        if line == "@@LESSON\n": src = "lesson"; el = 0; continue
        if line == "@@SOURCES\n": src = "sources"; el = 0; continue
        el += 1
        if src == "lesson":
            if re.match(r"^##\s+Gate\b",line): gate = 1; continue
            if gate and re.match(r"^##\s",line): gate = 0; continue
            if not gate: continue
        if not line.lstrip().startswith("|"): continue
        spans = []
        for m in after.finditer(line): spans.append((int(m.group(2)),[m.group(1)]))
        for m in before.finditer(line): spans.append((int(m.group(1)),unit.findall(m.group(2))))
        for k,qs in spans:
            n += 1
            w = sum(wc(q) for q in qs)
            if w != k:
                bad += 1
                print("line=%d label=%d wc=%d quote=%s" % (el,k,w," / ".join(qs)[:70]))
    print("word_labels=%d mismatched=%d" % (n,bad))
    sys.exit(0 if bad == 0 and n > 0 else 1)'
    ```

    prints `word_labels=<n> mismatched=<n>` and exits 0 only when `mismatched=0` and `n>0`, 1 otherwise, 2 on a
    missing lesson or `SOURCES.md`. It FAILS at `a66751b1` (`word_labels=16 mismatched=5`, exit 1): `:57` 11 vs 10,
    `:60` 11 vs 10, `:61` 5 vs 4, `:62` 17 vs 16, `:63` 8 vs 6. The routed R3 names two of these (11 vs 10 and 17 vs
    16); the check finds three more in the same Gate, so "Two word-count labels are one high" is under-sampled. It
    PASSES on a scratch lesson (`word_labels=3 mismatched=0`, exit 0). The same check flags round 28's S147
    (`label=11 wc=14`, `corpus/lessons/round-28.md:67`) because the escaped cell separators `\|` count as tokens; a
    round that wants rendered-word semantics must carve out `\|` in the criterion, not in a silent edit. Red inputs:
    a label one high (round 29's five); a label attached to the wrong quote in a multi-quote cell; a label computed
    from the location token instead of the quote.

91. A gate enters a counted condition only with a committed `--selftest` that shows it discriminates: it reports `0`
    (`blind_violations=0`) on a known-clean input adjudicated clean by a non-author closure, and reports a violation
    for each planted leak class it claims to catch — for the round-30 blindness gate: a tool line citation, a tool
    output marker, a forbidden path in a files-opened list, and a missing files-opened list. The selftest is committed
    before the counted run and before the freeze commit it grades; a gate without it may be an observation, never a
    counted condition, and its result can neither certify nor sink a claim. ← lessons/round-29.md:32-37 (M2), :96-99
    (M2 correction: "not yet a QUALITY row; not shown able to fail"); lessons/round-29-verifier-spotcheck.md:162-163
    (routed R5); .ufo/waves/round-30/contract.md:75-79 (the four classes); corpus/QUALITY.md:461-464 (the round-29
    note on 85 records the same gap). Check: `bash .ufo/waves/round-30/check-blind-wave.sh --selftest` prints `PASS`
    and exits 0 when the known-clean input reports 0 and every planted class raises a violation, 1 when a class is
    missed or the clean input reports a hit, 2 on a usage error, a missing input or a gate path absent at `<rev>`. It
    FAILS at `a66751b1`: the path is absent (`git cat-file -e` exits 128), so no selftest can run. The committed
    round-29 gate at `d6d5cb0a` also fails the interface: `--selftest` prints `usage: check-blind-wave.sh <lane-rev>
    <wave-report-dir> <writer-name-regex>` and exits 2, and its first counted run at that freeze printed
    `blind_violations=20`, all 20 adjudicated false positives (lessons/round-29.md:32-37; spot-check :162-163). Until
    the round-30 gate and its selftest are committed this row is unenforced and no round may claim it. Red inputs:
    the round-29 gate's interface; a selftest with no clean-input run; a selftest that catches the four classes but
    not the writer-vocabulary false positives behind round 29's 20 hits; a selftest committed after the counted run.

92. The disputed A2a verdict — an active earlyoom whose `ActiveEnterTimestampMonotonic` is absent or `0`, a journal
    with at least two version lines, a real send line before the last version line and none after it, then a plain
    restart; verdict `KILLERS_UNKNOWN` — is pinned by a frozen case in
    `tools/fixtures/mori-oom-killers/cases-a2-r30.json` whose blob equals the blob at the first commit that added the
    file, and the A2a limit is stated where the next reader looks: a line in `SKILL.md` or a `corpus/knowledge/`
    entry that names the case id and `limit`, saying the rule does not attribute a send that precedes the latest
    version line. ← lessons/round-29-verifier-spotcheck.md:164-165 (routed R6); .ufo/waves/round-30/contract.md:64-69
    (the shape and the pinned fields). Check, over committed bytes:

    ```sh
    lane=<lane>; rev=<rev>
    python3 -I -B -c '
    import json,re,subprocess,sys
    L = sys.argv[1]; R = sys.argv[2]
    def sh(*a):
        return subprocess.run(("git","-C",L)+a,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL).stdout.decode()
    p = "tools/fixtures/mori-oom-killers/cases-a2-r30.json"
    t = sh("show",R+":"+p)
    if not t:
        print("missing_case_file"); sys.exit(2)
    cs = json.loads(t)["cases"]
    SENDS = ("sending SIGTERM to process ","sending SIGKILL to process ","escalating to SIGKILL after ")
    def disputed(c):
        i = c.get("inputs",{})
        kv = dict(x.split("=",1) for x in i.get("earlyoom_show","").splitlines() if "=" in x)
        if kv.get("ActiveState") != "active": return 0
        if kv.get("ActiveEnterTimestampMonotonic","0") not in ("","0"): return 0
        m = [str(e.get("MESSAGE","")).lstrip() for e in i.get("earlyoom_journal",[])]
        v = [k for k,x in enumerate(m) if x.startswith("earlyoom ")]
        s = [k for k,x in enumerate(m) if x.startswith(SENDS)]
        if len(v) < 2 or not s: return 0
        if any(k > v[-1] for k in s) or not any(k < v[-1] for k in s): return 0
        return str(c.get("expect",{}).get("verdict","")) == "KILLERS_UNKNOWN"
    h = [c for c in cs if disputed(c)]
    ids = [c.get("id","") for c in h if c.get("id")]
    limit = "no"
    docs = ["SKILL.md"] + [x for x in sh("ls-tree","-r","--name-only",R,"--","corpus/knowledge/").splitlines() if x.endswith(".md")]
    for d in docs:
        for line in sh("show",R+":"+d).splitlines():
            if re.search(r"\blimit",line,re.I) and any(cid in line for cid in ids):
                limit = "yes"; break
        if limit == "yes": break
    added = sh("log","--format=%H","--diff-filter=A","--max-count=1",R,"--",p).strip()
    blob = sh("rev-parse",R+":"+p).strip()
    frozen = "yes" if added and sh("rev-parse",added+":"+p).strip() == blob else "no"
    print("pinned=%d limit_stated=%s frozen=%s" % (len(h),limit,frozen))
    sys.exit(0 if h and limit == "yes" and frozen == "yes" else 1)' "$lane" "$rev"
    ```

    prints `pinned=<n> limit_stated=<yes|no> frozen=<yes|no>`; exit 0 when `pinned>=1`, `limit_stated=yes` and
    `frozen=yes`; 1 otherwise; 2 when the case file is missing or unparseable. It FAILS at `a66751b1`
    (`missing_case_file`, exit 2: no frozen case for the shape exists at the entering tip) and PASSES on a scratch
    one-commit repo holding one disputed case and a `Limit: case pin-a2a …` line (`pinned=1 limit_stated=yes
    frozen=yes`, exit 0). Red inputs: a case whose verdict is `KILLER_ACTED` (`pinned=0`, exit 1); a second commit
    that edits the frozen case (`frozen=no`, exit 1); a correct case with no limit line in `SKILL.md` or the
    knowledge entry (`limit_stated=no`, exit 1).
````

## 4. Findings

1. **R3 is under-sampled.** The routed text says two labels are one high (spot-check `:159`); the literal `wc -w` check finds five at
   `a66751b1` (`:57` 11/10, `:60` 11/10, `:61` 5/4, `:62` 17/16, `:63` 8/6).
2. **R2's false sentence is still live at the tip.** `corpus/lessons/round-29.md:65` at `a66751b1` still says the grep "returned no line
   in either file", though `kill.h:36-37` matches `dryrun` (spot-check `:157-158`).
3. **88's `met` line is weaker than its statement.** The checker concatenates `LOG.md` and the lesson; at `1fc6bb0` it is met while the
   lesson names only `tip-retention.txt` (per-file `grep -cF`: LOG 3/3, lesson 1/3).
4. **90 has a consequence beyond round 29.** It flags round 28's S147 (`corpus/lessons/round-28.md:67`, label 11, `wc` 14) because `\|`
   counts as a token; the L1 must accept or carve that out explicitly.
5. **91/92 are unenforced at the entering tip.** The round-30 gate and case file are not committed at `a66751b1`; their checks can only fail there, and the draft says no round may claim those rows until the paths land.

## 5. Limits and out-of-scope

- Did not run the round-30 `--selftest` or read its case file: neither exists at `a66751b1`. I verified the absence and the round-29 gate's refusal, not future behaviour.
- `blind_violations=20` is cited from `corpus/lessons/round-29.md:32-37` and spot-check `:162-163`; not rerun.
- The label parser handles `(N words): "…"` and `"…" (N words)`; an unparsed label lowers `word_labels` (trips the `n>0` guard), never
  raises `mismatched`.
- The R2 checker reads the last cell of a `## Gate` row; a literal `|` there would split it, a shape no Gate row has today.
- No pacman/uv/npx/cargo install ran; nothing to record. No `tools/mori-oom-killers.py` source or run output is pasted; the only pasted
  outputs are §2's check lines.

## 6. Artifacts

- Scratch: `/fast/scratch/hyaku/mori-r30/MoriR30.DraftQualityRows/` — `inline_r2.sh`, `inline_r3.sh`, `inline_r6.sh` (the exact §3
  bodies), `wc_labels.py`, `absence_reason.py`, `pin_r6.py`, `gate-r29.sh`, `r1-pass.txt`; repos `lab` (`aba1e5d`, `9adf993`), `lab2`
  (`afc0121`), `lab4` (`14205c7`), `lab5` (`2bb7031`).
