import unittest
import dis
from paddle_bytecode.convert_to_bytecode_ast import convert_to_bytecode_ast
from paddle_bytecode import bytecode_attr
from paddle_bytecode.infer_attr_transform import InferAttrTransform
from paddle_bytecode.clone_transform import CloneTransform
from paddle_bytecode.flatten_expression_transform import FlattenExpressionTransform
from paddle_bytecode.diff_opname_and_argval_interpreter import DiffOpnameAndArgvalInterpreter
from paddle_bytecode.dump_transform import DumpTransform
from paddle_bytecode.get_instructions_transform import GetInstructionsTransform

class TestFlatten(unittest.TestCase):
  def make_getter_generate_new_local_varname(self, prefix, init=0):
    counter = init
    def generate_new_local_varname():
      nonlocal counter
      counter += 1
      return prefix + str(counter)
    return generate_new_local_varname

  def get_flattened_bytecode(self, f,
                             is_procedure_static_convertible,
                             is_result_static_convertible,
                             generate_new_local_varname):
    ast_node = convert_to_bytecode_ast(list(dis.get_instructions(f)))
    mut_attr = bytecode_attr.BytecodeAttr.make_getter()
    infer_attr = InferAttrTransform(
      mut_attr,
      is_procedure_static_convertible,
      is_result_static_convertible
    )
    infer_attr.infer(ast_node)
    flatten_expr = FlattenExpressionTransform(generate_new_local_varname, mut_attr)
    return flatten_expr.flatten(ast_node)

  def get_dynamic_procedure_flattened_and_expected(
        self, origin_func, expected_func, builtin_dynamic_funcs, local_var_prefix, local_var_seq_init):
    def is_procedure_static_convertible(ast_node):
      return not (
        ast_node.instruction.opname == "LOAD_GLOBAL"
        and ast_node.instruction.argval in builtin_dynamic_funcs
      )
    is_result_static_convertible = lambda ast_node: (True,) * ast_node.num_outputs_on_stack()
    generate_new_local_varname = self.make_getter_generate_new_local_varname(
      local_var_prefix, init=local_var_seq_init
    )
    ast_node0 = self.get_flattened_bytecode(
      origin_func,
      is_procedure_static_convertible=is_procedure_static_convertible,
      is_result_static_convertible=is_result_static_convertible,
      generate_new_local_varname=generate_new_local_varname
    )
    ast_node1 = convert_to_bytecode_ast(list(dis.get_instructions(expected_func))) 
    return ast_node0, ast_node1

  def test_nested_dynamic_expression(self):
    def origin_func(x):
      x = bar(bar())
      return x
    def expected_func(x):
      x = bar(bar())
      return x
    flattened_ast_node, expected_ast_node = self.get_dynamic_procedure_flattened_and_expected(
      origin_func=origin_func,
      expected_func=expected_func,
      builtin_dynamic_funcs={"bar"},
      local_var_prefix="tmp",
      local_var_seq_init=0
    )
    from pprint import pprint
    self.assertTrue(DiffOpnameAndArgvalInterpreter().diff(flattened_ast_node, expected_ast_node))

if __name__ == '__main__':
    unittest.main()
