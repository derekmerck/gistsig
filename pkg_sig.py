import os, logging
from pathlib import Path
from hashlib import sha1


def get_pkg_hash(pkg_name):

    pkg = __import__(pkg_name)
    lines = ""
    path = os.path.dirname(pkg.__loader__.path)
    for root, dir, files in os.walk(path):
        for fn in files:
            if os.path.splitext(fn)[-1] == ".py":
                fp = Path(root, fn)
                logging.debug(fp)
                with open(fp) as f:
                    lines = lines + f.read()
    s = sha1(lines.encode('utf-8')).hexdigest()
    return s


def get_pkg_key(pkg_name):

    pkg = __import__(pkg_name)
    sig = "{n}:{v}".format(n=pkg.__name__,
                           v=pkg.__version__)
    return sig


