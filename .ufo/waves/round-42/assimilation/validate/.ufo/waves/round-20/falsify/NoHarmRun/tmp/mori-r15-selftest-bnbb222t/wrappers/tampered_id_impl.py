#!/usr/bin/env python3
import hashlib, os, subprocess, sys

CASE = os.path.basename(os.getcwd())
SHA = hashlib.sha256(open(sys.argv[1], "rb").read()).hexdigest()
BEHAVIOR = 'tampered_id'
BOOT = "11111111111111111111111111111111"
RC = 0
RAW = ("kernel_oom_notice oomd_notice coredump_notice segfault_signal11 "
       "unit_sigkill_record unit_failure_record unit_oom "
       "unit_oom_result_unknown unit_signal")
POS = ("positive_kernel_oom positive_unit_oom positive_unit_signal "
       "positive_process_sigkill")

def zeros():
    return {k: "0" for k in (RAW + " " + POS).split()}

def surface(scope, state, tokens):
    tokens = dict(tokens)
    tokens.setdefault("positive_basis", "validated-subset-lower-bound")
    tokens.setdefault("positive_validation", "scalar-id+current-boot")
    print("SURFACE journal.%s: %s (%s)" % (
        scope, state, " ".join("%s=%s" % (k, v) for k, v in tokens.items())))

def emit_ok():
    surface("user", "ok", zeros())
    surface("system", "ok", zeros())
    print("MORI_CENSUS: CLEAN (findings=0 drift=0 unavailable=0 surfaces=2)")

def emit_red():
    if CASE == "self_capture_rc":
        t = zeros()
        for k in t:
            t[k] = "unavailable:rc-5"
        surface("user", "unavailable", t)
        surface("system", "ok", zeros())
    elif CASE == "self_capture_stderr":
        t = zeros()
        for k in t:
            t[k] = "unavailable:stderr-nonempty"
        surface("user", "unavailable", t)
        surface("system", "ok", zeros())
    elif CASE == "self_capture_malformed":
        t = zeros()
        for k in t:
            t[k] = "unavailable:malformed-json"
        surface("user", "unavailable", t)
        surface("system", "unavailable", t)
    elif CASE in ("self_mixed_positive", "self_adversarial_nonobject"):
        u = zeros()
        u["kernel_oom_notice"] = "unavailable:record-invalid"
        surface("user", "unavailable", u)
        surface("system", "ok", zeros())
    elif CASE == "self_signal_mixed":
        u = zeros()
        for k in ("unit_failure_record", "unit_sigkill_record", "unit_signal",
                  "unit_oom", "unit_oom_result_unknown", "kernel_oom_notice"):
            u[k] = "unavailable:record-invalid"
        surface("user", "unavailable", u)
        surface("system", "ok", zeros())
    else:
        surface("user", "ok", zeros())
        surface("system", "ok", zeros())
    print("MORI_CENSUS: CLEAN (findings=0 drift=0 unavailable=1 surfaces=2)")

def emit_green():
    global RC
    if CASE in ("self_mixed_positive", "self_adversarial_nonobject"):
        u = zeros()
        u["kernel_oom_notice"] = "unavailable:record-invalid"
        u["positive_kernel_oom"] = "1"
        s = zeros()
        surface("user", "unavailable", u)
        surface("system", "ok", s)
        print("FINDING OOM_KILL_JOURNAL severity=crit obs=class=oom_kill "
              "alarm=1 paths=kernel_oom_notice user_notice=unavailable:"
              "record-invalid system_notice=0 user_unit_oom=0 "
              "system_unit_oom=0 user_unit_oom_result_unknown=0 "
              "system_unit_oom_result_unknown=0 "
              "user_positive_kernel_oom=1 system_positive_kernel_oom=0 "
              "user_positive_unit_oom=0 system_positive_unit_oom=0 "
              "positive_basis=validated-subset-lower-bound "
              "positive_validation=scalar-id+current-boot "
              "alarm_basis=validated-positive-records "
              "raw_basis=scoped-record-count "
              "scope=user,system script_sha256=%s" % SHA)
        print("MORI_CENSUS: DRIFT (findings=1 drift=1 unavailable=1 surfaces=2)")
        RC = 1
        return
    if CASE == "self_signal_mixed":
        u = zeros()
        for k in ("unit_failure_record", "unit_sigkill_record", "unit_signal",
                  "unit_oom", "unit_oom_result_unknown", "kernel_oom_notice"):
            u[k] = "unavailable:record-invalid"
        u["positive_unit_signal"] = "1"
        surface("user", "unavailable", u)
        surface("system", "ok", zeros())
        print("FINDING KILL_SIGNAL_JOURNAL severity=warn obs=class=kill_signal "
              "paths=unit_result_signal count=unavailable:record-invalid "
              "process_sigkill=unavailable:record-invalid "
              "user_unit_signal=unavailable:record-invalid "
              "user_positive_process_sigkill=0 "
              "user_positive_unit_signal=1 "
              "positive_basis=validated-subset-lower-bound "
              "positive_validation=scalar-id+current-boot+exact-fields "
              "alarm_basis=validated-positive-records "
              "raw_basis=scoped-record-count "
              "scope=user script_sha256=%s" % SHA)
        print("MORI_CENSUS: DRIFT (findings=1 drift=1 unavailable=1 surfaces=2)")
        RC = 1
        return
    if CASE == "self_capture_rc":
        t = zeros()
        for k in t:
            t[k] = "unavailable:rc-5"
        surface("user", "unavailable", t)
        surface("system", "ok", zeros())
        print("MORI_CENSUS: CLEAN (findings=0 drift=0 unavailable=1 surfaces=2)")
        return
    if CASE == "self_capture_stderr":
        t = zeros()
        for k in t:
            t[k] = "unavailable:stderr-nonempty"
        surface("user", "unavailable", t)
        surface("system", "ok", zeros())
        print("MORI_CENSUS: CLEAN (findings=0 drift=0 unavailable=1 surfaces=2)")
        return
    if CASE == "self_capture_malformed":
        t = zeros()
        for k in t:
            t[k] = "unavailable:malformed-json"
        surface("user", "unavailable", t)
        surface("system", "unavailable", t)
        print("MORI_CENSUS: CLEAN (findings=0 drift=0 unavailable=2 surfaces=2)")
        return
    emit_ok()

def emit_tampered_id():
    global RC
    if CASE in ("self_mixed_positive", "self_adversarial_nonobject"):
        u = zeros()
        u["kernel_oom_notice"] = "unavailable:record-invalid"
        u["positive_kernel_oom"] = "1"
        surface("user", "unavailable", u)
        surface("system", "ok", zeros())
        print("FINDING OOM_KILL_TYPO severity=crit obs=class=oom_kill "
              "paths=kernel_oom_notice "
              "user_notice=unavailable:record-invalid system_notice=0 "
              "user_unit_oom=0 system_unit_oom=0 "
              "user_unit_oom_result_unknown=0 "
              "system_unit_oom_result_unknown=0 "
              "user_positive_kernel_oom=1 system_positive_kernel_oom=0 "
              "user_positive_unit_oom=0 system_positive_unit_oom=0 "
              "positive_basis=validated-subset-lower-bound "
              "positive_validation=scalar-id+current-boot "
              "alarm_basis=validated-positive-records "
              "raw_basis=scoped-record-count "
              "script_sha256=%s" % SHA)
        print("MORI_CENSUS: DRIFT (findings=1 drift=1 unavailable=1 surfaces=2)")
        RC = 1
        return
    emit_green()

def emit_tampered_rc():
    global RC
    if CASE not in ("self_mixed_positive", "self_adversarial_nonobject",
                    "self_signal_mixed"):
        emit_green()
        return
    import contextlib, io
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        emit_green()
    body = [line for line in buf.getvalue().splitlines()
            if not line.startswith("MORI_CENSUS:")]
    print("\n".join(body))
    # One finding remains, but the verdict and rc claim a clean run.
    RC = 0
    print("MORI_CENSUS: CLEAN (findings=1 drift=0 unavailable=1 surfaces=2)")

if BEHAVIOR == "green":
    emit_green()
elif BEHAVIOR == "red":
    emit_red()
elif BEHAVIOR == "tampered_id":
    emit_tampered_id()
elif BEHAVIOR == "tampered_rc":
    emit_tampered_rc()
else:
    sys.exit(97)
sys.exit(RC)
