import sys


def warn(msg: str):
    msg = 'WARNING:\n  ' + msg.replace('\n', '\n  ')
    print(msg, file=sys.stderr)
