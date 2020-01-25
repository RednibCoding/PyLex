import sys


class Stream:
	def __init__(self, inputStr:list):
		self.__pos = 0
		self.__line = 1
		self.__col = 0
		self.__inputStr = inputStr

	def next(self)->str:
		if self.__pos >= len(self.__inputStr):
			return ""

		char = self.__inputStr[self.__pos]
		self.__pos += 1

		if(char == "\n"):
			self.__line += 1
			self.__col = 0
		else:
			self.__col += 1

		return char

	def peek(self, offset:int=0)->str:
		if self.__pos+offset >= len(self.__inputStr):
			return ""
		return self.__inputStr[self.__pos+offset] 

	def eof(self)->bool:
		return self.peek() == ""

	def error(self, msg:str):
		print(f"Error in line {str(self.__line)} at: {str(self.__col)}: \n>>> {msg}")
		sys.exit()