#! python3
"""
check-hashes.py
Derek Merck
Fall 2018

Create a gist for your project and note the id.

```bash
$ export GIST_OAUTH_TOK=<github token>
$ python3 check-hashes.py store  <gist_id> <project> ./README.md
$ python3 check-hashes.py verify <gist_id> <project> ./README.md
Process finished with exit code 0
$ echo "/n" >> ./README.md
$ python3 check-hashes.py verify <gist_id> <project> ./README.md
Process finished with exit code 255
```

For hashing files in docker images, use the format `docker:image:file`.  For example:

```bash
$ check-hashes.py print  <gist_id> <project> docker:orthanc-amd64:/usr/local/sbin/Orthanc
```

"""

import logging, json, os, subprocess
from typing import Mapping
from pprint import pprint
from argparse import ArgumentParser
from hashlib import md5
import requests

gist_token = os.environ.get("GIST_OAUTH_TOK")

def parse_args():

    p = ArgumentParser()
    p.add_argument("action", choices=["print", "store", "verify"])
    p.add_argument("gist_id")
    p.add_argument("name")
    p.add_argument("paths", nargs="+")

    opts = p.parse_args()
    return opts


def update_hashlist(gist_id, name, hashes):

    headers = {
        "Content-Type": "application/json",
        "Authorization": "token {}".format(gist_token)
    }
    url = "https://api.github.com/gists/{}".format(gist_id)
    data = {
        "files": {
                    "{}.json".format(name):  {"content": json.dumps(hashes, indent=2, separators=(',', ': '))}
                 }
            }
    r = requests.patch(url, headers=headers, json=data)
    if r.status_code > 299:
        logging.error(r.json())


def download_hashlist(gist_id, name):

    url = "https://api.github.com/gists/{}".format(gist_id)
    r = requests.get(url)
    content = r.json().get('files').get("{}.json".format(name)).get('content')
    hashes = json.loads(content)
    return hashes


def get_md5(filename, block_size=2 ** 20):
    hash = md5()
    try:
        file = open(filename, 'rb')
        while True:
            data = file.read(block_size)
            if not data:
                break
            hash.update(data)
    except IOError:
        print('File \'' + filename + '\' not found!')
        return None
    except:
        return None
    return hash.hexdigest()


def get_hashes(paths):

    hashes = {}

    for path in paths:

        if os.path.isfile(path) and \
          subprocess.call(["git", "check-ignore", "-q", path]):
            hashes[path] = get_md5(path)

        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    if not file.startswith(".") and \
                      file.find("/.") < 0 and \
                      subprocess.call(["git", "check-ignore", "-q", os.path.join(root, file)]):
                        hashes[os.path.join(root, file)] = get_md5(os.path.join(root,file))

        elif path.startswith("docker"):
            _, image, file = path.split(":")
            cmd = ["docker", "run", image, "md5sum", file]
            output = subprocess.getoutput(" ".join(cmd))
            hashes[path] = output.split()[0]

    return hashes


def compare_hash_dicts(a: Mapping, b: Mapping) -> bool:
    if a.items() <= b.items():
        return True
    return False


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    opts = parse_args()

    if opts.action == "print":
        hashes = get_hashes(opts.paths)
        pprint( hashes )

    elif opts.action == "store":
        hashes = get_hashes(opts.paths)
        update_hashlist(opts.gist_id, opts.name, hashes)

    elif opts.action == "verify":
        hashes = get_hashes(opts.paths)
        cardinal_hashes = download_hashlist(opts.gist_id, opts.name)

        cmp = compare_hash_dicts(hashes, cardinal_hashes)
        exit(cmp-1)

