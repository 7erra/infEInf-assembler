"""Unit tests for the assembler module"""
import unittest
from src import assembler
class TestAssembler(unittest.TestCase):
    """Collection of test cases"""
    def test_0(self):
        """Test a program that always ends in 0 for a register"""
        self.assertEqual(assembler.Program("test/test_0.txt").run({100: 5}), {100: 0})
    def test_move(self):
        """Move a value from one register to another"""
        prog = assembler.Program("test/test_move.txt")
        self.assertEqual(prog.run({100: 0, 101: 5}), {100: 5, 101: 0})
    def test_copy(self):
        """Copy a value from one register to another"""
        prog = assembler.Program("test/test_copy.txt")
        self.assertEqual(prog.run({100: 0, 101: 5, 102: 0}), {100: 5, 101: 5, 102: 0})

    def test_error_index(self):
        """Program that tires to access a command counter beyond the last line"""
        with self.assertRaises(IndexError):
            assembler.Program("test/test_error_index.txt").run()
    def test_error_target(self):
        """Argument (target) is not an integer"""
        with self.assertRaises(assembler.TargetError):
            assembler.Program("test/test_error_target.txt").run()
    def test_error_infinite(self):
        """Loop infinitely"""
        with self.assertRaises(assembler.InfiniteLoopError):
            assembler.Program("test/test_error_infinite.txt").run()

if __name__ == "__main__":
    unittest.main()
