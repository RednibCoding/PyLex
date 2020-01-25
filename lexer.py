from stream import Stream

class Lexer:
	"""
		The Lexer expects a Stream object containing the data to tokenize. (See: stream.py)
		Example:
			# Open and read a file:
			data = ""
			with open(filename, "r") as file:
				data = file.read()
			# Create a Stream object and pass the read data
			stream = Stream(data)

		The lexer exspects a dictionary containing:
			- keywords
			- punctuation
			- operators
			- single line comment symbol
			- multi line comment start symbol
			- multi line comment end symbol
			- stringSymbols

		Example:
			Creating a symbols dictionary:
			symbols = {
				"keywords": "if then else let def true false print",
				"operators": "+ - * / % = & | < > >= && || <= !",
				"punctuation": ", ; ( ) { } [ ]",
				"stringSymbols": "\" '",
				"slComment": "//",
				"mlCommentStart": "/*",
				"mlCommentEnd": "*/",
			}

			Note:
				- symbols must be seperated by spaces
				- punctuation and stringSymbols may only consist of one character eg. '"' or ";"
				- all comments (slComment, mlCommentStart, mlCommentEnd) may contain only one symbol
				  (Having more than one symbol representing a comment wouldn't make that much sense, wouldn't it?)
				  Usually a programming language has 3 comment tokens:
				  	- A symbol for single line comments eg. //  (slComment)
					- A symbol for multi line comment start eg. /*  (mlCommentStart)
					- A symbol for multi line comment end eg */  (mlCommentEnd)

	"""
	def __init__(self, inputStream:Stream, symbols:dict):
		keywords = symbols["keywords"].split(" ")
		punctuation = symbols["punctuation"].split(" ")
		operators = symbols["operators"].split(" ")
		slComment = symbols["slComment"].split(" ")
		mlCommentStart = symbols["mlCommentStart"].split(" ")
		mlCommentEnd = symbols["mlCommentEnd"].split(" ")
		stringSymbols = symbols["stringSymbols"].split(" ")


		self.__current = None
		self.__inputStream = inputStream

		self.__keywords = keywords
		self.__punctuation = punctuation
		self.__operators = operators
		self.__slComment = slComment
		self.__mlCommentStart = mlCommentStart
		self.__mlCommentEnd = mlCommentEnd
		self.__stringSymbols = stringSymbols
	
	def isKeyword(self, kw:str)->bool:
		return kw in self.__keywords

	def isDigit(self, char:str)->bool:
		return char in "0123456789"

	def isIdentifierStart(self, char:str)->bool:
		# Avoid regex :p
		return char in ("_abcdefghijklmnopqrstuvwxyz"
						"ABCDEFGHIJKLMNOPQRSTUVWXYZ")

	def isIdentifier(self, char:str)->bool:
		return self.isIdentifierStart(char) or self.isDigit(char)

	def isOperator(self, char:str)->bool:
		if char in self.__operators:
			return True

	def isSubOfOperator(self, char:str)->bool:
		for ch in self.__operators:
			if char in ch:
				return True
		return False

	def getOperatorFromSubOp(self, char:str)->str:
		# Check if char is a subpart of an operator (eg. '&&' or '==' etc.)
		maybeIsOp = False
		for ch in self.__operators:
			if char in ch:
				maybeIsOp = True
				break
		# Get the longest operator (eg. === would consist of 3 characters)
		longest = 0
		if maybeIsOp:
			for ch in self.__operators:
				longest = len(ch) if len(ch) > longest else longest

			peeked = ""
			for i in range(0, longest):
				peeked += self.__inputStream.peek(i)
				for ch in self.__operators:
					if peeked in self.__operators:
						return peeked
		return ""
		

	def isPunctuation(self, char:str)->bool:
		return char in self.__punctuation

	def isWhitespace(self, char:str)->bool:
		return char in " \t\n\r"

	def readWhile(self, function)->str:
		string = ""
		while not self.__inputStream.eof() and function(self.__inputStream.peek()):
			string += self.__inputStream.next()
		return string

	def readNumber(self)->dict:
		hasDot = False
		def number(char):
			nonlocal hasDot
			if char == ".":
				if hasDot: return False
				hasDot = True
				return True
			return self.isDigit(char)
		num = self.readWhile(number)

		return {
			"type":		"float" if hasDot else "int",
			"value":	float(num) if hasDot else int(num)
		}

	def readIdentifier(self)->dict:
		identifier = self.readWhile(self.isIdentifier)
		return {
			"type":		"kw" if self.isKeyword(identifier) else "ident",
			"value":	identifier
		}

	def readEscaped(self, end:str)->str:
		escaped = False
		string = ""
		self.__inputStream.next()
		while not self.__inputStream.eof():
			char = self.__inputStream.next()
			if escaped:
				string += char
			elif char == "\\":
				escaped = True
			elif char == end:
				break
			else:
				string += char
		return string

	def readString(self, stringSymbol:str)->dict:
		return {
			"type":		"str",
			"value":	self.readEscaped(stringSymbol)
		}

	def skipSLComment(self)->None:
		self.readWhile(lambda char: char != "\n")
		self.__inputStream.next()

	def isSlComment(self, char)->bool:
		# Get all chars building the single line comment symbol
		lenSlComment = len(self.__slComment[0])
		slComment = ""
		if lenSlComment > 1:
			for i in range(0, lenSlComment):
				slComment += self.__inputStream.peek(offset=i)
		else:
			slComment = char

		if slComment in self.__slComment:
			return True
		return False

	def skipMlComment(self)->None:
		def isNotMlCommentEnd(char):
			if self.isMlCommentEnd():
				return False
			return True
		self.readWhile(isNotMlCommentEnd)
		self.__inputStream.next()

	def isMlCommentStart(self):
		# Get all chars building the single line comment symbol
		lenMlCommentStart = len(self.__mlCommentStart[0])
		mlCommentStart = ""
		if lenMlCommentStart > 1:
			for i in range(0, lenMlCommentStart):
				mlCommentStart += self.__inputStream.peek(offset=i)
		if mlCommentStart in self.__mlCommentStart:
			return True
		return False

	def isMlCommentEnd(self):
		# Get all chars building the multi line comment symbol
		lenMlCommentEnd = len(self.__mlCommentEnd[0])
		mlCommentEnd = ""
		if lenMlCommentEnd > 1:
			for i in range(0, lenMlCommentEnd):
				mlCommentEnd += self.__inputStream.peek(offset=i)
		if mlCommentEnd in self.__mlCommentEnd:
			# Advance read position to skip the comment symbol as well
			for _ in range(0, lenMlCommentEnd):
				self.__inputStream.next()
			return True
		return False

	def readNext(self)->dict:
		self.readWhile(self.isWhitespace)
		if self.__inputStream.eof(): return None
		char = self.__inputStream.peek()
		if self.isSlComment(char):
			self.skipSLComment()
			return self.readNext()
		if self.isMlCommentStart():
			self.skipMlComment()
			return self.readNext()
		for strSymbol in self.__stringSymbols:
			if char == strSymbol: return self.readString(strSymbol)
		if self.isDigit(char): return self.readNumber()
		if self.isIdentifierStart(char): return self.readIdentifier()
		if self.isPunctuation(char):
			return {
				"type":		"punc",
				"value":	self.__inputStream.next()
			}
		if self.isSubOfOperator(char):
			value = self.readWhile(self.isOperator)
			if value in self.__operators:
				return {
					"type":		"op",
					"value":	value
				}
			else:
				value = self.getOperatorFromSubOp(char)
				if value in self.__operators:
					# Advance read position
					for _ in range(0, len(value)):
						self.__inputStream.next()
					return {
						"type":		"op",
						"value":	value
					}
				else:
					self.__inputStream.error(f"Unexpected symbol: {value}")
 
		self.__inputStream.error(f"Unexpected symbol: {char}")

	def peek(self)->dict:
		if not self.__current:
			self.__current = self.readNext()
		return self.__current

	def next(self)->dict:
		token = self.__current
		self.__current = None
		return token or self.readNext()

	def eof(self)->bool:
		return self.peek() == None