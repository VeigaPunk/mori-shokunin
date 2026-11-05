#!/usr/bin/env python3
"""Round-100 C1 counter (coverage): the seat terminal census separates credential/entitlement deaths.

Predicate P1 (frozen; same sentence in contract.md and in the receipt label):
  C1=met iff, for the lane tree --root DIR,
   (battery) every case of a battery GENERATED AT MEASUREMENT TIME from a printed seed is classified by
             DIR/tools/mori-seat-terminal.py as planted: auth deaths (HTTP 401/403 with no quota/rate
             evidence, or a Connect/gRPC/provider auth spelling) -> dead_auth; quota/rate evidence beside an
             auth status or spelling keeps dead_quota/dead_rate_limit; Z.AI codes keep their meaning;
             non-auth errors (plain 'permission denied' words, 5xx, safety refusals, resource_exhausted)
             stay dead_error_other; settled/unsettled/completed seats keep their class;
   (selftest) `DIR/tools/mori-seat-terminal.py --selftest` exits 0 with finding SELFTEST_OK;
   (r17gate) the lane's registered round-17 fixture gate in DIR, run on DIR's tool over DIR's round-17
             fixtures, prints `GATE ok` and exits 0;
   (registry) DIR/SKILL.md's seat-terminal registry row names `dead_auth`;
   (sourced) DIR/corpus/knowledge/seat-auth-deaths-r100.md cites S637 and S638 in `source:` lines and
             DIR/corpus/SOURCES.md holds both rows with status `mined`.
Exit 0 met, 1 unmet, 2 setup. Scratch: --work (default $TMPDIR or $HYAKU_SCRATCH), removed on exit.
"""
import argparse, json, os, pathlib, random, re, shutil, subprocess, sys, tempfile

NOW_MS = 1793000000000
OLD = NOW_MS - 3_600_000          # settled (older than the 900 s window)
NEW = NOW_MS - 10_000             # unsettled

PROVIDERS = ["commandcode", "anthropic", "openai", "devin", "opencode-go", "amr", "minimax-code", "acme"]
TAILS = ["", " Please re-authenticate.", " (request id r-%d)", " Contact your administrator.",
         " See the console for details.", " [trace %d]"]


def tail(rng):
    t = rng.choice(TAILS)
    return t % rng.randint(1000, 99999) if "%d" in t else t


VOCAB = ["request", "failed", "upstream", "model", "account", "stream", "error", "server", "provider", "denied",
         "access", "plan", "route", "key", "token", "session", "header", "invalid", "expired", "closed", "retry",
         "later", "region", "node", "gateway", "permission", "authentication", "forbidden", "unavailable"]
AUTH_SPELLINGS = ["permission_denied", "PERMISSION_DENIED", "unauthenticated", "UNAUTHENTICATED",
                  "authentication_error", "permission_error"]


def words(rng):
    return " ".join(rng.choice(VOCAB) for _ in range(rng.randint(3, 9)))


def battery(rng):
    """Return list of (case_id, family, record, expected_class)."""
    cases = []

    def add(fam, exp, ts=OLD, stop="error", **fields):
        body = {"role": "assistant", "stopReason": stop, "completedAt": ts,
                "provider": fields.pop("provider", rng.choice(PROVIDERS)), "model": "m%d" % rng.randint(1, 9)}
        body.update(fields)
        cases.append(("C%03d" % (len(cases) + 1), fam, body, exp))

    # A1 auth by HTTP status, no quota/rate evidence, no auth spelling required
    a1 = ["%d Invalid 'Authorization' header or token." , "%d Unauthorized", "%d Forbidden: key revoked",
          "%d {\"error\":{\"message\":\"Your current subscription does not have access to this model\"}}",
          "%d invalid x-api-key", "%d token expired"]
    for _ in range(8):
        st = rng.choice([401, 403])
        add("A1-auth-status", "dead_auth", errorStatus=st, errorMessage=(rng.choice(a1) % st) + tail(rng))
    # A2 auth by spelling, no status
    a2 = ["Devin stream error permission_denied: This model is no longer available for your account.",
          "stream error unauthenticated: token is not valid", "PERMISSION_DENIED: caller lacks access to model",
          "UNAUTHENTICATED: request had invalid authentication credentials",
          "provider error (type=authentication_error) invalid key",
          "{\"type\":\"error\",\"error\":{\"type\":\"permission_error\",\"message\":\"no access\"}}",
          "Retry budget exhausted after %d retries: Devin stream error permission_denied: model unavailable"]
    for _ in range(8):
        m = rng.choice(a2)
        if "%d" in m:
            m = m % rng.randint(2, 10)
        add("A2-auth-spelling", "dead_auth", errorMessage=m + tail(rng))
    # A3 auth spelling hidden behind a JSON escape in the transcript bytes (tool decodes escapes)
    for tok in rng.sample(["permission_denied", "unauthenticated", "permission_error"], 2):
        add("A3-auth-escaped", "dead_auth", errorMessage="stream error %s: denied" % tok, _escape=tok)
    # N1 quota evidence beside an auth status or spelling -> quota
    n1 = ["%d Quota exceeded for quota metric requests", "%d usage limit reached for this key",
          "%d no credits remaining on account", "permission_denied: weekly usage quota exhausted"]
    for _ in range(4):
        m = rng.choice(n1)
        if "%d" in m:
            st = rng.choice([401, 403])
            add("N1-quota-wins", "dead_quota", errorStatus=st, errorMessage=m % st)
        else:
            add("N1-quota-wins", "dead_quota", errorMessage=m)
    # N2 rate evidence beside auth status/spelling -> rate
    for _ in range(3):
        m = rng.choice(["%d rate limit exceeded for organization", "%d RATE_LIMITED try later",
                        "permission_denied then rate_limit hit"])
        if "%d" in m:
            add("N2-rate-wins", "dead_rate_limit", errorStatus=403, errorMessage=m % 403)
        else:
            add("N2-rate-wins", "dead_rate_limit", errorMessage=m)
    # N3 non-auth errors stay other
    n3 = [(500, "500 internal error: permission denied writing cache"),
          (None, "Codex error event: This content was flagged for possible cybersecurity risk."),
          (None, "resource_exhausted: upstream capacity"), (400, "400 invalid_request_error: bad schema"),
          (None, "connection reset by peer after 4013 bytes"), (502, "502 Bad Gateway"),
          (None, "authentication service unreachable: dial tcp timeout"),
          (500, "upstream answered 403 bytes then closed")]
    for st, m in rng.sample(n3, 7):
        f = {"errorMessage": m + tail(rng)}
        if st is not None:
            f["errorStatus"] = st
        add("N3-other-stays", "dead_error_other", **f)
    # A4/A5/N5 composed at measurement time from a word list (no fixed template a lookup could key on)
    for _ in range(4):
        add("A4-auth-status-composed", "dead_auth", errorStatus=rng.choice([401, 403]),
            errorMessage=words(rng))
    for _ in range(4):
        tok = rng.choice(AUTH_SPELLINGS)
        ws = words(rng).split(" ")
        ws.insert(rng.randint(0, len(ws)), tok + rng.choice(["", ":", ","]))
        add("A5-auth-spelling-composed", "dead_auth", errorMessage=" ".join(ws))
    for _ in range(4):
        f = {"errorMessage": words(rng)}
        st = rng.choice([None, 400, 500, 503])
        if st is not None:
            f["errorStatus"] = st
        add("N5-other-composed", "dead_error_other", **f)
    # N4 non-dead seats with auth text keep their class
    add("N4-unsettled", "error_unsettled", ts=NEW, errorStatus=401, errorMessage="401 Unauthorized")
    add("N4-completed", "completed", stop="stop", errorMessage="permission_denied mentioned in text")
    add("N4-aborted", "aborted", stop="aborted", errorStatus=403)
    # Z1 Z.AI codes keep their meaning; unmapped code + 401 -> auth
    add("Z1-zai-quota-code", "dead_quota", provider="zai", errorStatus=403,
        errorMessage="403 plan blocked (type=1308)")
    add("Z1-zai-rate-code", "dead_rate_limit", provider="zai", errorStatus=401,
        errorMessage="401 too many (type=1302)")
    add("Z1-zai-unmapped-auth", "dead_auth", provider="zai", errorStatus=401,
        errorMessage="401 key invalid (type=%d)" % rng.randint(1400, 1499))
    rng.shuffle(cases)
    return cases


def write_case(root, cid, body):
    esc = body.pop("_escape", None)
    rec = json.dumps({"type": "message", "message": body}, separators=(",", ":"))
    if esc:
        i = esc.index("_") if "_" in esc else 1
        ch = esc[i]
        rec = rec.replace(esc, esc[:i] + "\\u%04x" % ord(ch) + esc[i + 1:], 1)
    p = root / "r100" / (cid + ".jsonl")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"type": "session", "version": 3}) + "\n" + rec + "\n", encoding="utf-8")


def run(cmd, cwd=None, env=None, timeout=900):
    try:
        r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        return -9, "", "timeout"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    d = pathlib.Path(a.root).resolve()
    tool = d / "tools/mori-seat-terminal.py"
    if not tool.is_file():
        print("C1=setup reason=tool-missing"); return 2
    seed = a.seed if a.seed is not None else random.SystemRandom().randrange(1, 2**31)
    base = a.work or os.environ.get("TMPDIR") or os.environ.get("HYAKU_SCRATCH")
    if not base:
        print("C1=setup reason=no-scratch (set --work or TMPDIR)"); return 2
    os.makedirs(base, exist_ok=True)
    w = pathlib.Path(tempfile.mkdtemp(prefix="c1r100-", dir=base))
    env = dict(os.environ, TMPDIR=str(w))
    try:
        rng = random.Random(seed)
        cases = battery(rng)
        sess = w / "sessions"
        for cid, _fam, body, _exp in cases:
            write_case(sess, cid, dict(body))
        rc, out, err = run([sys.executable, str(tool), "--sessions-dir", str(sess), "--now-ms", str(NOW_MS),
                            "--max-files", "1000"], env=env)
        got = {}
        try:
            obj = json.loads(out.strip().splitlines()[-1])
            for s in obj.get("seats", []):
                got[s.get("seat")] = s.get("class")
        except (ValueError, IndexError, AttributeError):
            pass
        bad = []
        for cid, fam, _b, exp in cases:
            if got.get(cid) != exp:
                bad.append("%s:%s:want=%s:got=%s" % (cid, fam, exp, got.get(cid)))
        ok_cases = len(cases) - len(bad)
        fam_bad = sorted({b.split(":")[1] for b in bad})
        # selftest
        src, sout, _ = run([sys.executable, str(tool), "--selftest"], env=env)
        selftest = "ok" if src == 0 and '"finding_id":"SELFTEST_OK"' in sout.replace(" ", "") else "rc%d" % src
        # r17 gate
        gate = d / "tools/mori-round17-seat-regressions.py"
        fx = d / ".ufo/waves/round-17/fixtures/seat"
        if gate.is_file() and fx.is_dir():
            grc, gout, gerr = run([sys.executable, str(gate), "--tool", str(tool), "--fixtures", str(fx),
                                   "--output", str(w / "r17out")], env=env)
            r17 = "ok" if grc == 0 and "GATE ok" in (gout + gerr) else "rc%d" % grc
        else:
            r17 = "missing"
        # registry
        skill = (d / "SKILL.md").read_text(encoding="utf-8", errors="replace") if (d / "SKILL.md").is_file() else ""
        row = [l for l in skill.splitlines() if l.startswith("| seat terminal status (r17) |")]
        registry = "met" if len(row) == 1 and "dead_auth" in row[0] else "unmet"
        # sourced
        ent = d / "corpus/knowledge/seat-auth-deaths-r100.md"
        srcs = (d / "corpus/SOURCES.md").read_text(encoding="utf-8", errors="replace") \
            if (d / "corpus/SOURCES.md").is_file() else ""
        sourced_ok = ent.is_file()
        if sourced_ok:
            et = ent.read_text(encoding="utf-8", errors="replace")
            for sid in ("S637", "S638"):
                if not re.search(r"^source: %s\b" % sid, et, re.M):
                    sourced_ok = False
                rows = [l for l in srcs.splitlines() if re.match(r"^ {0,3}\| *%s *\|" % sid, l)]
                if len(rows) != 1:
                    sourced_ok = False
                    continue
                cells = [c.strip() for c in rows[0].strip().strip("|").split("|")]
                if len(cells) != 11 or cells[7] != "mined":
                    sourced_ok = False
        sourced = "met(S637,S638)" if sourced_ok else "unmet"
        failed = [n for n, v in (("battery", ok_cases == len(cases)), ("selftest", selftest == "ok"),
                                 ("r17gate", r17 == "ok"), ("registry", registry == "met"),
                                 ("sourced", sourced_ok)) if not v]
        met = not failed
        print("C1=%s cases_ok=%d/%d families_failed=%s selftest=%s r17gate=%s registry=%s sourced=%s "
              "checks_failed=%s seed=%d tool_rc=%d" % (
                  "met" if met else "unmet", ok_cases, len(cases), ",".join(fam_bad) or "-", selftest, r17,
                  registry, sourced, ",".join(failed) or "-", seed, rc))
        for b in bad[:12]:
            print("  miss", b)
        return 0 if met else 1
    finally:
        shutil.rmtree(w, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
