# Book PDF Merger
Book PDF Merger is a free and open-source pdf merger for scanned PDFs.
Because many scanners can only single-side, you have to merge two PDFs. However, it isn't delightful to read them alternatively. This script makes it easy :)

## Installation
```
git clone https://github.com/harajune/book-pdf-merger.git
cd book-pdf-merger
pip install -r requirements.txt
```

## How to Use
```
usage: main.py [-h] --out OUT --in1 IN1 --in2 IN2 [--reverse1] [--reverse2]

optional arguments:
  -h, --help  show this help message and exit
  --out OUT   output file path
  --in1 IN1   first input pdf path
  --in2 IN2   second input pdf path
  --reverse1  reverse first pdf page order
  --reverse2  reverse second pdf page order
```