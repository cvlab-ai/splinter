
# Requirements

## 1.

Recommended python version is 3.10.13.

  

## 2.

To run this project, you need to install [poppler](https://poppler.freedesktop.org/) and [libgl1](https://packages.ubuntu.com/libgl1).

  

```(linux)

apt-get install libgl1 poppler-utils

```

  

## 3.

Install pip packages located in [inference_engine/requirements.txt](https://github.com/cvlab-ai/splinter/blob/main/inference_engine/requirements.txt).

If you are in the current directory, you can type:
```
pip install -r ../../requirements.txt
```
# Usage

```
python main.py [SOURCE_DIRECTORY] [TARGET_DIRECTORY] [FILE_FILENAME_PATTERN] [LOG_FILENAME_PATTERN]
```

Default values:
- SOURCE_DIRECTORY: .
- TARGET_DIRECTORY: ./output
- FILE_FILENAME_PATTERN: `(empty)`
- LOG_FILENAME_PATTERN: (txt|log)

# Output

Anonymized files are located in the `TARGET_DIRECTORY` directory.