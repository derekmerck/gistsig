import os, logging
from pathlib import Path
from hashlib import sha1


def get_pkg_hash(pkg):

    lines = ""
    path = os.path.dirname(pkg.__loader__.path)
    fps = []
    for root, dir, files in os.walk(path):
        for fn in files:
            if os.path.splitext(fn)[-1] == ".py":
                fp = Path(root, fn)
                fps.append(fp)

    for fp in sorted(fps):
        logging.debug(fp)
        with open(fp) as f:
            lines = lines + f.read()

    s = sha1(lines.encode('utf-8')).hexdigest()
    return s


def get_pkg_key(pkg):

    sig = "{n}:{v}".format(n=pkg.__name__,
                           v=pkg.__version__)
    return sig


def get_pkg_info(pkg_name):

    pkg = __import__(pkg_name)

    value = get_pkg_hash(pkg=pkg)
    key = get_pkg_key(pkg=pkg)

    return key, value

