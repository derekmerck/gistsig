`gistsig`
==========================

Derek Merck  
<derek_merck@brown.edu>  
Rhode Island Hospital and Brown University  
Providence, RI  

Sign and verify Python packages by version using a public gist.

See <https://gist.github.com/derekmerck/4b0bfbca0a415655d97f36489629e1cc> for my package signatures.

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
$ echo "/n" >> <pkg>/main.py
$ gistsig verify -g <gist_id> <pkgs>
Process finished with exit code 1
```


## Algorithm

This simple signing algorithm is _only_ intended to verify that the scripts for an installed Python package have not been tampered with since that version was tested and released.

1. Find package path
2. `os.walk` the package path and filter for "*.py"
3. Concatenate the file contents in file path sorted order
4. Compute the sha1 digest of the result

This can be easily implemented from the command-line as well:

```bash
$ gistsig -g 4b0bfbca0a415655d97f36489629e1cc show diana
Local package has signature python-diana:2.0.13:9fec66ac3f4f87f8b933c853d8d5f49bdae0c1dc

$ python -c "import diana; print(diana.__version__)"
2.0.13

$ find $(python -c "import diana; print(diana.__path__[0])") -name *.py | sort -n | xargs cat| sha1sum 
9fec66ac3f4f87f8b933c853d8d5f49bdae0c1dc
```


## License

MIT
