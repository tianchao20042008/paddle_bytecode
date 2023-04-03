import unittest
import dis
from paddle_bytecode.convert_to_bytecode_ast import convert_to_bytecode_ast
from paddle_bytecode import bytecode_attr
from paddle_bytecode.infer_attr_transform import InferAttrTransform
from paddle_bytecode.clone_transform import CloneTransform
from paddle_bytecode.flatten_expression_transform import FlattenExpressionTransform
from paddle_bytecode.diff_opname_and_argval_interpreter import DiffOpnameAndArgvalInterpreter
from paddle_bytecode.dump_transform import DumpTransform

class TestEmpty(unittest.TestCase):
  def test_function_without_return(self): 
    def foo():
      pass
    ast_node0 = convert_to_bytecode_ast(list(dis.get_instructions(foo)))
    ast_node1 = CloneTransform().clone(ast_node0) 
    mut_attr = bytecode_attr.BytecodeAttr.make_getter()
    def is_procedure_static_convertible(ast_node):
      return True
    def is_result_static_convertible(ast_node):
      return tuple(True) * ast_node.num_outputs_on_stack()
    infer_attr = InferAttrTransform(
      mut_attr,
      is_procedure_static_convertible,
      is_result_static_convertible
    )
    infer_attr.infer(ast_node1)
    counter = 0
    def generate_new_local_varname():
      nonlocal counter
      counter += 1
      return "tmp" + str(counter)
    flatten_expr = FlattenExpressionTransform(generate_new_local_varname, mut_attr)
    ast_node2 = flatten_expr.flatten(ast_node1)
    from pprint import pprint
    pprint(DumpTransform(mut_attr).dump(ast_node0))
    pprint(DumpTransform(mut_attr).dump(ast_node1))
    pprint(DumpTransform(mut_attr).dump(ast_node2))
    self.assertTrue(DiffOpnameAndArgvalInterpreter().diff(ast_node0, ast_node1))
    self.assertTrue(DiffOpnameAndArgvalInterpreter().diff(ast_node0, ast_node2))

if __name__ == '__main__':
    unittest.main()
