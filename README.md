# PyLex
A minimal and easy to use lexer

## What is pylex
Pylex is a minimal lexer to tokanize a given text by given rules.
Rules are pretty simple: just define a symbols dictionary and pass it to the lexer. See the how to below.

## How to:
The Lexer expects a Stream object containing the data to tokenize. (See: stream.py)

```python
    # Open and read a file:
    data = ""
    with open(filename, "r") as file:
        data = file.read()
    # Create a Stream object and pass the read data
    stream = Stream(data)
```
The lexer exspects a dictionary containing:
* keywords
* punctuation
* operators
* single line comment symbol
* multi line comment start symbol
* multi line comment end symbol
* stringSymbols


```python
    # Creating a symbols dictionary:
    symbols = {
        "keywords": "if then else let def true false print",
        "operators": "+ - * / % = & | < > >= && || <= !",
        "punctuation": ", ; ( ) { } [ ]",
        "stringSymbols": "\" '",
        "slComment": "//",
        "mlCommentStart": "/*",
        "mlCommentEnd": "*/",
    }
```
    Note:
        - symbols must be seperated by spaces
        - punctuation and stringSymbols may only consist of one character eg. '"' or ";"
        - all comments (slComment, mlCommentStart, mlCommentEnd) may contain only one symbol
            (Having more than one symbol representing a comment wouldn't make that much sense, wouldn't it?)
            Usually a programming language has 3 comment tokens:
            - A symbol for single line comments eg. //  (slComment)
            - A symbol for multi line comment start eg. /*  (mlCommentStart)
            - A symbol for multi line comment end eg */  (mlCommentEnd)
            
See: run_me.py to see how to run the lexer.
