from pathlib import Path
import re
class TargetError(Exception):
	""" Exception raised when the target of a command is not an integer.

	Attributes:
		expression -- input expression in which the error occured
		message -- explanation of the error
	"""
	def __init__(self, expression, message):
		self.expression = expression
		self.message = message
class InfiniteLoopError(Exception):
	""" Exception raised when the program takes too long."""
	def __init__(self, maxIter):
		self.message = f"Infinite loop, program stopped after {maxIter} steps!"

class Statement:
	"""An executable line from the program.

	Keyword arguments:
	program -- The program that this Statement is part of
	command -- The command. One of:
		"TST" - Increase counter by two instead of one when the value of target is 0
		"INC" - Increase the value of target by one
		"DEC" - Decrease the value of target by one
		"JMP" - Set the value of the counter to the target value
		"HLT" - Stops the program
	target: The target can be a register or the counter, depending on the command
	"""
	def __init__(self, program, command, target=None):
		self.program = program
		self.command = command
		self.target = target
	
	def execute(self):
		"""Execute this statement"""
		if self.command == "INC":
			self.program.register[self.target] += 1
		elif self.command == "DEC":
			self.program.register[self.target] -= 1
		elif self.command == "TST":
			if self.program.register[self.target] == 0:
				self.program.counter += 1
		elif self.command == "JMP":
			self.program.counter = self.target - 1
			return
		elif self.command == "HLT":
			pass
		self.program.counter += 1


class Program:
	"""Initializes an Assembler program.

	Arguments:
	file -- The file that contains the program
	"""
	regex_command = re.compile(r"(?P<cmd>HLT|TST|INC|DEC|JMP)(?:\s+(?P<target>\d+))?")
	
	def __init__(self, file):
		self.compile(file)

	def compile(self, file):
		"""Converts the file into a list of statements"""
		self.statements = []
		with open(file) as f:
			self.statements = tuple([self.compileStatement(s, i) for i, s in enumerate(f.readlines())])

	def run(self, register=None, verbose=False):
		"""Run the program.
		
		Arguments:
		register -- The starting register. If no register is given it will be asked from the user.
		verbose -- Print more information each step (default False)
		"""
		self.counter = 0
		self.register = dict()
		if not register:
			# No register given, analyze program and ask for values
			for s in self.statements:
				if s.command in {"TST", "INC", "DEC"}:
					if not (s.target in self.register):
						while True:
							value = input(f"Value for register {s.target}: ")
							if (value.isdigit()):
								self.register[s.target] = int(value)
								break
							print("INVALID: Only integers are allowed!")
		else:
			self.register = register
		run = 0
		max_runs = 1000
		while True:
			current = self.statements[self.counter]
			if (verbose):
				print("Command:", current.command, ", Target:", current.target, ", Step:", run)
				print("Counter", "Register")
				print(f"{self.counter:7} {self.register}")
			current.execute()
			if current.command == "HLT":
				break
			if (verbose):
				print(f"{self.counter:7} {self.register}\n")
			run += 1
			if run >= max_runs:
				raise InfiniteLoopError(run)
		print("Final register:", self.register)
		return self.register
	
	def compileStatement(self, string, line):
		"""Convert a string into a statement"""
		match = self.regex_command.match(string)
		cmd = match["cmd"]
		target = match["target"]
		try:
			target = int(target)
		except TypeError:
			if cmd != "HLT":
				raise TargetError(f"[LINE {line + 1}]: {string.strip()}", "Target must be an integer!")
		return Statement(self, cmd, target)
