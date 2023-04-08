import unittest
import dis
from paddle_bytecode.convert_to_bytecode_ast import convert_to_bytecode_ast
from paddle_bytecode import bytecode_attr
from paddle_bytecode.infer_attr_transform import InferAttrTransform
from paddle_bytecode.clone_transform import CloneTransform
from paddle_bytecode.flatten_right_value_transform import FlattenRightValueTransform
from paddle_bytecode.diff_opname_and_argval_transform import DiffOpnameAndArgvalTransform
from paddle_bytecode.dump_transform import DumpTransform
from paddle_bytecode.get_instructions_transform import GetInstructionsTransform
import paddle_bytecode.mock_is_procedure_static_convertible_transform as mock

class TestFlatten(unittest.TestCase):
  def test_function_without_return(self): 
    def foo():
      pass
    ast_node0 = convert_to_bytecode_ast(list(dis.get_instructions(foo)))
    ast_node1 = CloneTransform()(ast_node0) 
    mut_attr = bytecode_attr.BytecodeAttr.make_getter()
    def is_procedure_static_convertible(ast_node):
      return True
    def is_result_static_convertible(ast_node):
      return (True,) * ast_node.num_outputs_on_stack()
    infer_attr = InferAttrTransform(
      mut_attr,
      is_procedure_static_convertible,
      is_result_static_convertible
    )
    infer_attr(ast_node1)
    counter = 0
    def generate_new_local_varname():
      nonlocal counter
      counter += 1
      return "tmp" + str(counter)
    flatten_rvalue = FlattenRightValueTransform(generate_new_local_varname, mut_attr)
    ast_node2 = flatten_rvalue(ast_node1)
    self.assertTrue(DiffOpnameAndArgvalTransform()(ast_node0, ast_node1))
    self.assertTrue(DiffOpnameAndArgvalTransform()(ast_node0, ast_node2))

  def test_function_with_return(self): 
    def foo():
      return 65536
    ast_node0 = convert_to_bytecode_ast(list(dis.get_instructions(foo)))
    ast_node1 = CloneTransform()(ast_node0) 
    mut_attr = bytecode_attr.BytecodeAttr.make_getter()
    def is_procedure_static_convertible(ast_node):
      return True
    def is_result_static_convertible(ast_node):
      return (True,) * ast_node.num_outputs_on_stack()
    infer_attr = InferAttrTransform(
      mut_attr,
      is_procedure_static_convertible,
      is_result_static_convertible
    )
    infer_attr(ast_node1)
    counter = 0
    def generate_new_local_varname():
      nonlocal counter
      counter += 1
      return "tmp" + str(counter)
    flatten_rvalue = FlattenRightValueTransform(generate_new_local_varname, mut_attr)
    ast_node2 = flatten_rvalue(ast_node1)
    self.assertTrue(DiffOpnameAndArgvalTransform()(ast_node0, ast_node1))
    self.assertTrue(DiffOpnameAndArgvalTransform()(ast_node0, ast_node2))

  def test_flat_dynamic_function_assign(self): 
    def foo():
      x = bar()
      return x
    ast_node0 = convert_to_bytecode_ast(list(dis.get_instructions(foo)))
    ast_node1 = CloneTransform()(ast_node0) 
    mut_attr = bytecode_attr.BytecodeAttr.make_getter()
    def is_procedure_static_convertible(ast_node):
      return not (
        ast_node.instruction.opname == "LOAD_GLOBAL"
        and ast_node.instruction.argval == "bar"
      )
    def is_result_static_convertible(ast_node):
      return (True,) * ast_node.num_outputs_on_stack()
    is_procedure_static_convertible = (
      mock.MockIsProcedureStaticConvertibleTransform(is_procedure_static_convertible)(ast_node1)
    )
    infer_attr = InferAttrTransform(
      mut_attr,
      is_procedure_static_convertible,
      is_result_static_convertible
    )
    infer_attr(ast_node1)
    counter = 0
    def generate_new_local_varname():
      nonlocal counter
      counter += 1
      return "tmp" + str(counter)
    flatten_rvalue = FlattenRightValueTransform(generate_new_local_varname, mut_attr)
    ast_node2 = flatten_rvalue(ast_node1)
    self.assertTrue(DiffOpnameAndArgvalTransform()(ast_node0, ast_node1))
    self.assertTrue(DiffOpnameAndArgvalTransform()(ast_node0, ast_node2))

  def make_getter_generate_new_local_varname(self, prefix, init=0):
    counter = init - 1 # `counter++` will be used later.
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
    is_procedure_static_convertible = (
      mock.MockIsProcedureStaticConvertibleTransform(is_procedure_static_convertible)(ast_node)
    )
    infer_attr = InferAttrTransform(
      mut_attr,
      is_procedure_static_convertible,
      is_result_static_convertible
    )
    infer_attr(ast_node)
    flatten_rvalue = FlattenRightValueTransform(generate_new_local_varname, mut_attr)
    return flatten_rvalue(ast_node)

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

  def test_simple_dynamic_expression_assign(self): 
    def foo0():
      x = bar() + 1
      return x
    def foo1():
      tmp1 = bar()
      x = tmp1 + 1
      return x
    flattened_ast_node, expected_ast_node = self.get_dynamic_procedure_flattened_and_expected(
      origin_func=foo0,
      expected_func=foo1,
      builtin_dynamic_funcs={"bar"},
      local_var_prefix="tmp",
      local_var_seq_init=1
    )
    from pprint import pprint
    print('---------------------')
    pprint(list((i.opname, i.argval) for i in GetInstructionsTransform()(flattened_ast_node)))
    print('---------------------')
    pprint(list((i.opname, i.argval) for i in GetInstructionsTransform()(expected_ast_node)))
    print('---------------------')
    self.assertTrue(DiffOpnameAndArgvalTransform()(flattened_ast_node, expected_ast_node))

  def test_mixed_dynamic_expression_assign(self):
    def foo0(x):
      x = static_func(1 + x, bar(), 2 + x)
      return x
    def foo1(x):
      tmp1 = 1 + x
      tmp2 = bar()
      x = static_func(tmp1, tmp2, 2 + x)
      return x
    flattened_ast_node, expected_ast_node = self.get_dynamic_procedure_flattened_and_expected(
      origin_func=foo0,
      expected_func=foo1,
      builtin_dynamic_funcs={"bar"},
      local_var_prefix="tmp",
      local_var_seq_init=1
    )
    self.assertTrue(DiffOpnameAndArgvalTransform()(flattened_ast_node, expected_ast_node))

  def test_static_dynamic_interleave_expression_assign(self):
    def origin_func(x):
      x = static_func(1 + x, bar(static_func(bar())), 2 + x)
      return x
    def expected_func(x):
      tmp1 = 1 + x
      tmp2 = bar()
      tmp3 = static_func(tmp2)
      tmp4 = bar(tmp3)
      x = static_func(tmp1, tmp4, 2 + x)
      return x
    flattened_ast_node, expected_ast_node = self.get_dynamic_procedure_flattened_and_expected(
      origin_func=origin_func,
      expected_func=expected_func,
      builtin_dynamic_funcs={"bar"},
      local_var_prefix="tmp",
      local_var_seq_init=1
    )
    self.assertTrue(DiffOpnameAndArgvalTransform()(flattened_ast_node, expected_ast_node))

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
      local_var_seq_init=1
    )
    self.assertTrue(DiffOpnameAndArgvalTransform()(flattened_ast_node, expected_ast_node))

  def test_nested_static_expression(self):
    def origin_func(x):
      x = static_bar(static_bar())
      return x
    def expected_func(x):
      x = static_bar(static_bar())
      return x
    flattened_ast_node, expected_ast_node = self.get_dynamic_procedure_flattened_and_expected(
      origin_func=origin_func,
      expected_func=expected_func,
      builtin_dynamic_funcs={"bar"},
      local_var_prefix="tmp",
      local_var_seq_init=1
    )
    self.assertTrue(DiffOpnameAndArgvalTransform()(flattened_ast_node, expected_ast_node))


if __name__ == '__main__':
    unittest.main()
