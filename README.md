# Ebook Indexifier
This is a command line tool intended for Linux for adding an index to an e-book, either a PDF or a DJVU.

## Usage
Once the files are set up properly, invoke with

```
add-index "/path/to/ebook.pdf" "/path/to/index-file" 10
```

the last argument, in this example `10`, is an integer offset which will be added to the page numbers. If not included it defaults to 0.

See below for the format of the "index file".

The script will detect PDF or DJVU format from the file extension.

## The index file
The script accepts as input a file describing the book's table of contents. For an example of its format, see the file `example`.

## Installation/Dependencies
This tool requires `pdftk` and `djvused` be installed on the system. A python 3 interpreter must be available at the command `python3` and the `main.py` script in this repository must be in the same directory as the `add-index` shell script.