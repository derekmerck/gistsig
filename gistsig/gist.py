import requests
import json
import logging


def get_gist(gist_id, name):

    url = "https://api.github.com/gists/{}".format(gist_id)
    r = requests.get(url)
    if r.status_code != 200:
        return {}
    try:
        logging.info("Found gist")
        content = r.json().get('files').get("{}.json".format(name)).get('content')
        hashes = json.loads(content)
        return hashes
    except:
        logging.warning("Missing file")
        return {}


def update_gist(oauth_tok, gist_id, name, content):

    headers = {
        "Content-Type": "application/json",
        "Authorization": "token {}".format(oauth_tok)
    }
    url = "https://api.github.com/gists/{}".format(gist_id)
    data = {
        "files": {
            "{}.json".format(name):
                {"content": json.dumps(content, indent=2, separators=(',', ': '))}
                 }
            }
    r = requests.patch(url, headers=headers, json=data)
    if r.status_code > 299:
        logging.error(r.json())

