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
		super().__init__(f"Infinite loop, stopped program after {maxIter} steps!")

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

	def run(self, register=dict(), verbose=False, step_by_step=False):
		"""Run the program.

		The register is a dict() containing all values for the register, eg:
			{100: 0, 101: 5, 102: 0}

		Enabling verbose will print information each step in the following
		format:

			Command: DEC , Target: 100 , Step: 2
			Counter Register
				  3 {100: 5}
				  4 {100: 4}

		The first line contains the command that is executed, what the command
		is targeting (can be a register or the command counter) and how many
		times any command was executed. After this information follows a table
		with the first column "Counter" which contains the command counter and a
		a second column with the state of the register. The first line of the
		table represents the state before the execution of the command while the
		second line is the state after the execution.
		
		Arguments:
		register -- The starting register. If no register is given it will be asked from the user.
		verbose -- Print more information each step (default False)
		step_by_step -- Ask for input after each step, also enables verbose (default False)
		"""
		verbose = verbose or step_by_step
		self.counter = 0
		for s in self.statements:
			# Analyze the commands and ask for missing values
			if s.command in {"TST", "INC", "DEC"}:
				while not s.target in register:
					value = input(f"Value for register {s.target}: ")
					if not value.isdigit():
						print("INVALID: Only integers are allowed!")
						continue
					register[s.target] = int(value)
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
			if step_by_step:
				input()
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
