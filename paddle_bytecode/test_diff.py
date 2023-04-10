import unittest
import dis
from paddle_bytecode.convert_to_bytecode_ast import convert_to_bytecode_ast
from paddle_bytecode.diff_opname_and_argval_transform import DiffOpnameAndArgvalTransform
from paddle_bytecode.dump_transform import DumpTransform

class TestDiff(unittest.TestCase):
  def test_same_inner_functions(self):
    def foo0():
      def bar():
        pass

    def foo1():
      def bar():
        pass

    ast_node0 = convert_to_bytecode_ast(dis.get_instructions(foo0))
    ast_node1 = convert_to_bytecode_ast(dis.get_instructions(foo1))
    self.assertTrue(DiffOpnameAndArgvalTransform()(ast_node0, ast_node1))

  def test_different_inner_functions(self):
    def foo0():
      def bar():
        pass

    def foo1():
      def bar():
        return 999

    ast_node0 = convert_to_bytecode_ast(dis.get_instructions(foo0))
    ast_node1 = convert_to_bytecode_ast(dis.get_instructions(foo1))
    # from pprint import pprint
    # pprint(DumpTransform()(ast_node0))
    # pprint(DumpTransform()(ast_node1))
    self.assertFalse(DiffOpnameAndArgvalTransform()(ast_node0, ast_node1))

if __name__ == '__main__':
    unittest.main()
