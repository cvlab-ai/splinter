# Exam Ground truth answer parser

## Usage

* Download answers .zip file an place it in this directory
* Run module using
  ```
  python3 -m answer_parser
  ```
* parsed answers will be saved in the `ground_thruth` directory.

### Help
```
usage: answer_parser [-h] [--search-dir SEARCH_DIR] [--dest-dir DEST_DIR] [--archive-re ARCHIVE_RE] {unpack} ...

Parse answers

positional arguments:
  {unpack}              Unpack answers archives

optional arguments:
  -h, --help            show this help message and exit
  --search-dir SEARCH_DIR
                        Directory to search for answer archives
  --dest-dir DEST_DIR   Directory to unpack answer archives into
  --archive-re ARCHIVE_RE
                        Regular expression to match answer archive name
```
