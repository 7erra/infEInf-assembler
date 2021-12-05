import unittest
from src import assembler
from pathlib import Path
class TestAssembler(unittest.TestCase):
	def test_0(self):
		self.assertEqual(assembler.Program("test/test_0.txt").run({100: 5}), {100: 0})
		
	def test_error_index(self):
		with self.assertRaises(IndexError):
			assembler.Program("test/test_error_index.txt").run()
	def test_error_target(self):
		with self.assertRaises(assembler.TargetError):
			assembler.Program("test/test_error_target.txt").run()
	def test_error_infinite(self):
		with self.assertRaises(assembler.InfiniteLoopError):
			assembler.Program("test/test_error_infinite.txt").run()

if __name__ == "__main__":
	unittest.main()