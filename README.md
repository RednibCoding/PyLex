# PyLex
A minimal and easy to use lexer

## What is pylex
Pylex is a minimal lexer to tokanize a given text by given rules.
Defining rules is pretty simple: just define a symbols dictionary and pass it to the lexer. See the **How to** below.

## The output
On each *readNext()* call which is a method of *Lexer*, the lexer returns the next found token as a dictionary or *None*, if there are no further tokens or the end of stream has been reached:
```python
token = lexer.readNext()
print(token)
```
Possible output:
```
{'type': 'str', 'value': "This is a 'string'"}
```

Pylex differentiates between the following tokens:

| Type          | Token         | Example  |
| ------------- | ------------- | -------- |
| identifier    | ident         | myVar    |
| keyword       | kw            | function |
| punctuation   | punc          | ; , { (  |
| operator      | op            | + - / &  |
| string        | str           |"A string"|
| integer       | int           |  34      |
| float         | float         |  21.438  |

Note:
* Comments are ignored.
* The example column is just an example. The output depends on what you have defined in the symbols-dictionary (see: **How to**) and the content that is being lexed.

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


## Example
By running the lexer on the example.lang
```javascript
// This is a comment

/*
    This is a
    multi line comment
*/

let myStr = "This is a 'string'"
let myStr2 = 'This is also a "string"'

def a() { // This is also a comment
    let a = 5;
    let b = 6;
    let isNice = true;
    if a >= b && isNice {
        print "This lexer is nice";
    } else {
        print "Uhm.. didn't expect that...";
    }
}

let a = 10.3; // This is a float
let b = a + 5; // This is an int
```

with the following symbols-dictionary:
```python
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

the output is:
```
{'type': 'kw', 'value': 'let'}
{'type': 'ident', 'value': 'myStr'}
{'type': 'op', 'value': '='}
{'type': 'str', 'value': "This is a 'string'"}
{'type': 'kw', 'value': 'let'}
{'type': 'ident', 'value': 'myStr2'}
{'type': 'op', 'value': '='}
{'type': 'str', 'value': 'This is also a "string"'}
{'type': 'kw', 'value': 'def'}
{'type': 'ident', 'value': 'a'}
{'type': 'punc', 'value': '('}
{'type': 'punc', 'value': ')'}
{'type': 'punc', 'value': '{'}
{'type': 'kw', 'value': 'let'}
{'type': 'ident', 'value': 'a'}
{'type': 'op', 'value': '='}
{'type': 'int', 'value': 5}
{'type': 'punc', 'value': ';'}
{'type': 'kw', 'value': 'let'}
{'type': 'ident', 'value': 'b'}
{'type': 'op', 'value': '='}
{'type': 'int', 'value': 6}
{'type': 'punc', 'value': ';'}
{'type': 'kw', 'value': 'let'}
{'type': 'ident', 'value': 'isNice'}
{'type': 'op', 'value': '='}
{'type': 'kw', 'value': 'true'}
{'type': 'punc', 'value': ';'}
{'type': 'kw', 'value': 'if'}
{'type': 'ident', 'value': 'a'}
{'type': 'op', 'value': '>='}
{'type': 'ident', 'value': 'b'}
{'type': 'op', 'value': '&&'}
{'type': 'ident', 'value': 'isNice'}
{'type': 'punc', 'value': '{'}
{'type': 'kw', 'value': 'print'}
{'type': 'str', 'value': 'This lexer is nice'}
{'type': 'punc', 'value': ';'}
{'type': 'punc', 'value': '}'}
{'type': 'kw', 'value': 'else'}
{'type': 'punc', 'value': '{'}
{'type': 'kw', 'value': 'print'}
{'type': 'str', 'value': "Uhm.. didn't expect that..."}
{'type': 'punc', 'value': ';'}
{'type': 'punc', 'value': '}'}
{'type': 'punc', 'value': '}'}
{'type': 'kw', 'value': 'let'}
{'type': 'ident', 'value': 'a'}
{'type': 'op', 'value': '='}
{'type': 'float', 'value': 10.3}
{'type': 'punc', 'value': ';'}
{'type': 'kw', 'value': 'let'}
{'type': 'ident', 'value': 'b'}
{'type': 'op', 'value': '='}
{'type': 'ident', 'value': 'a'}
{'type': 'op', 'value': '+'}
{'type': 'int', 'value': 5}
{'type': 'punc', 'value': ';'}
```
