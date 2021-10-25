from inspect import currentframe
import os
import sys
from time import perf_counter

linenumber = lambda : currentframe().f_back.f_lineno

def findpads(text):
	for j in range(len(text)):
		if text[j] not in (' ', '\t'):
			break

	return text[:j].count(' ') + text[:j].count('\t')*4

def buildtextwithpads(text, pads):
	return ' ' * pads + text

class Timer():
	__slots__ = ('t1', 'file', 'line', 'blockcontent', 'withcontent', 'name', 'checkpoints', 'autoprint', '__finaltime', 'dividelines')

	def __init__(self, line = None, name = None, autoprint = True):
		self.dividelines = []
		self.autoprint = bool(autoprint)
		self.checkpoints = []
		self.withcontent = False
		self.file = sys.argv[0]
		self.name = name
		self.line = line - 1 if line != None else None

	def __enter__(self):
		self.t1 = perf_counter()
		return self

	def __exit__(self, *args):
		self.__finaltime = perf_counter() - self.t1
		self.blockcontent = self.getcontent()
		if self.autoprint:
			print(f'TOTAL TIME:  {self.__finaltime} sec - > {self.name} ')
			if self.checkpoints:
				for point in range(len(self.checkpoints)):
					print(f"Checkpoint: {point+1} -> {self.checkpoints[point]} sec - > {self.name}\n")
			else:
				print("CHECKPOINTS: Not found\n")
			if self.line:
				print(''.join(self.blockcontent))

	@property
	def finaltime(self):
		try:
			return self.__finaltime
		except:
			pass
		raise AttributeError('You cannot use this while it is in progress.') from None

		
	def __isemptytext(self, text):
		i = 0
		invalid = ('\t', ' ', '\n')
		for j in text:
			if j not in invalid:
				return False
		return True

	def getcontent(self):
		if self.line == None:
			raise AttributeError("Undefined line number, use Timer(line = linenumber()) ")

		content = []

		checkpointindex = 1

		with open(self.file, 'r') as f:
			code = f.readlines()
			startpads = findpads(code[self.line])
			longestline = len(f'{len(code)} : ')

			for j in range(self.line, len(code)):
				if j == len(code) - 1:
					pass
					# print(startpads >= findpads(code[j]), j != self.line)
				if self.__isemptytext(code[j]):
					currentnumber = f'{j+1} | '
					content += [f">>  {buildtextwithpads(currentnumber, longestline - len(currentnumber))}\n"]


				elif h:= ((startpads >= findpads(code[j])) and (j != self.line)):
					break

				else:
					currentnumber = f'{j+1} | '
					linecontent = buildtextwithpads(code[j].lstrip(), findpads(code[j]) - startpads)

					content += [f">>  {buildtextwithpads(currentnumber, longestline - len(currentnumber))} {linecontent}"]
			for j in range(len(content)-1, -1, -1):
				if self.__isemptytext(content[j].split('|')[1]):
					del content[j]
				else:
					break
		return content

	def checkpoint(self):
		self.checkpoints.append(perf_counter() - self.t1)

class CoolTimer:

	pass