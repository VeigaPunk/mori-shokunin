#!/usr/bin/python3
import os, sys, time
_OUT = '/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/NoHarmRun/r16/cases/timeout_user_anchor_plus_kernel_oom_and_sigkill/payload-stdout.bin'
_ERR = '/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/NoHarmRun/r16/cases/timeout_user_anchor_plus_kernel_oom_and_sigkill/payload-stderr.bin'
_LOG = '/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/NoHarmRun/r16/cases/timeout_user_anchor_plus_kernel_oom_and_sigkill/journalctl-argv.txt'
_PAD = 0
_SLEEP = 5
_RC = 0
def _emit():
    data = open(_OUT, 'rb').read() + b'x' * _PAD
    off = 0
    while off < len(data):
        off += os.write(1, data[off:])
    err = open(_ERR, 'rb').read()
    off = 0
    while off < len(err):
        off += os.write(2, err[off:])
with open(_LOG, 'w') as fh:
    fh.write('\x00'.join(sys.argv[1:]))
pid = os.fork()
if pid == 0:
    try:
        time.sleep(_SLEEP)
        _emit()
    except (BrokenPipeError, OSError):
        pass
    finally:
        os._exit(0)
sys.exit(_RC)
