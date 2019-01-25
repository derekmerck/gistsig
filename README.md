`gistsig`
==========================

Derek Merck  
<derek_merck@brown.edu>  
Rhode Island Hospital and Brown University  
Providence, RI  

Sign and verify Python packages by version using a public gist.

## Setup

```bash
$ pip install git+https://github.com/derekmerck/gistsig
```


## Usage

Create a gist to store version hashes and note the id.

```bash
$ export GIST_OAUTH_TOK=<github token>
$ gistsig store  -g <gist_id> <pkgs>
$ gistsig verify -g <gist_id> <pkgs>
Process finished with exit code 0
$ echo "/n" >> <pkg>.py
$ gistsig verify -g <gist_id> <pkgs>
Process finished with exit code 1
```

## License

MIT
