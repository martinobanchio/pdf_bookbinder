# booklet-style-PDF-reordering-python-script

Two simple python scripts for reordering a PDF file in 
* a foldable booklet, or
* a bound book, divided in signatures. 

Two pdf pages per face, and you can fold the printed papers in the middle, and read it like a normal book. 

## requirement

```
pip install pypdf
```

## Usage

For a single, foldable booklet, simply call
```
python booklet.py input_file.pdf
```

For the bound book, choose how many pages go in a signature (4, 8, 12, or 16) and call
```
python booklet.py input_file.pdf pages_in_signature
```

## note

Two-sided printing with flip-on-short-edge option yields the result. 