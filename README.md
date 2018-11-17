Check-Hashes
==========================

Derek Merck  
<derek_merck@brown.edu>  
Rhode Island Hospital and Brown University  
Providence, RI  

Store or check file hashes against a gist.

## Setup

```bash
$ pip install git+https://github.com/derekmerck/check-hashes
```

Platform Dependencies:  Docker


## Usage

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

For hashing files in Docker images, use the format `docker:image:file`.  For example:

```bash
$ check-hashes.py print  <gist_id> <project> docker:orthanc-amd64:/usr/local/sbin/Orthanc
```

## License

MIT
