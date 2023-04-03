import unittest
import dis
from .convert_to_bytecode_ast import convert_to_bytecode_ast

class TestEmpty(unittest.TestCase):
  def test_function_without_return(self): 
    def foo():
      pass
    ast_node0 = convert_to_bytecode_ast(list(dis.get_instructions(foo)))


if __name__ == '__main__':
    unittest.main()
