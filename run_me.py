from stream import Stream
from lexer import Lexer

def openFile(filename:str):
		with open(filename, "r") as file:
			data = file.read()
			return data

symbols = {
	"keywords": "if then else let def true false print",
	"operators": "+ - * / % = & | < > >= && || <= !",
	"punctuation": ", ; ( ) { } [ ]",
	"stringSymbols": "\" '",
	"slComment": "//",
	"mlCommentStart": "/*",
	"mlCommentEnd": "*/",
	
}

data = openFile("example.lang")
lexer = Lexer(Stream(data), symbols)

while True:
	token = lexer.readNext()
	if not token: break
	print(token)

