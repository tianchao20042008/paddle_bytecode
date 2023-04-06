import unittest
import dis
from paddle_bytecode.convert_to_bytecode_ast import convert_to_bytecode_ast
from paddle_bytecode import bytecode_attr
from paddle_bytecode.infer_attr_transform import InferAttrTransform
from paddle_bytecode.clone_transform import CloneTransform
from paddle_bytecode.flatten_left_value_transform import FlattenLeftValueTransform
from paddle_bytecode.diff_opname_and_argval_transform import DiffOpnameAndArgvalTransform
from paddle_bytecode.dump_transform import DumpTransform
from paddle_bytecode.get_instructions_transform import GetInstructionsTransform
import paddle_bytecode.mock_is_procedure_static_convertible_transform as mock

class TestFlatten(unittest.TestCase):
  def make_getter_generate_new_local_varname(self, prefix, init=0):
    counter = init - 1 # `counter++` will be used later.
    def generate_new_local_varname():
      nonlocal counter
      counter += 1
      return prefix + str(counter)
    return generate_new_local_varname

  def get_flattened_bytecode(self, f, generate_new_local_varname):
    ast_node = convert_to_bytecode_ast(list(dis.get_instructions(f)))
    flatten_expr = FlattenLeftValueTransform(generate_new_local_varname)
    return flatten_expr(ast_node)

  def get_flattened_and_expected(
        self, origin_func, expected_func, local_var_prefix, local_var_seq_init):
    generate_new_local_varname = self.make_getter_generate_new_local_varname(
      local_var_prefix, init=local_var_seq_init
    )
    ast_node0 = self.get_flattened_bytecode(
      origin_func, generate_new_local_varname=generate_new_local_varname
    )
    ast_node1 = convert_to_bytecode_ast(list(dis.get_instructions(expected_func))) 
    return ast_node0, ast_node1

  def test_simple(self): 
    def foo0():
      bar().x = 1
    def foo1():
      tmp1 = 1
      tmp2 = bar()
      tmp2.x = tmp1
    flattened_ast_node, expected_ast_node = self.get_flattened_and_expected(
      origin_func=foo0,
      expected_func=foo1,
      local_var_prefix="tmp",
      local_var_seq_init=1
    )
    self.assertTrue(DiffOpnameAndArgvalTransform()(flattened_ast_node, expected_ast_node))

  def test_unpack_store_attr(self): 
    def foo0(a, b):
      bar().x, bar().y = a, a + b
    def foo1(a, b):
      tmp1, tmp3 = a, a + b
      tmp2 = bar()
      tmp2.x = tmp1
      tmp4 = bar()
      tmp4.y = tmp3
    flattened_ast_node, expected_ast_node = self.get_flattened_and_expected(
      origin_func=foo0,
      expected_func=foo1,
      local_var_prefix="tmp",
      local_var_seq_init=1
    )
    # from pprint import pprint
    # pprint(list((i.opname, i.argval) for i in GetInstructionsTransform()(flattened_ast_node)))
    # pprint(list((i.opname, i.argval) for i in GetInstructionsTransform()(expected_ast_node)))
    self.assertTrue(DiffOpnameAndArgvalTransform()(flattened_ast_node, expected_ast_node))

  def test_unpack_store_subscr(self): 
    def foo0(a, b):
      x[bar()], y[bar()] = a, a + b
    def foo1(a, b):
      tmp1, tmp3 = a, a + b
      tmp2 = bar()
      x[tmp2] = tmp1
      tmp4 = bar()
      y[tmp4] = tmp3
    flattened_ast_node, expected_ast_node = self.get_flattened_and_expected(
      origin_func=foo0,
      expected_func=foo1,
      local_var_prefix="tmp",
      local_var_seq_init=1
    )
    # from pprint import pprint
    # pprint(list((i.opname, i.argval) for i in GetInstructionsTransform()(flattened_ast_node)))
    # pprint(list((i.opname, i.argval) for i in GetInstructionsTransform()(expected_ast_node)))
    self.assertTrue(DiffOpnameAndArgvalTransform()(flattened_ast_node, expected_ast_node))

  def test_store_attr_store_subscr(self): 
    def foo0(a, b):
      bar0().x[bar1()] = a, a + b
    def foo1(a, b):
      tmp1 = a, a + b
      tmp2 = bar0().x
      tmp3 = bar1()
      tmp2[tmp3] = tmp1
    flattened_ast_node, expected_ast_node = self.get_flattened_and_expected(
      origin_func=foo0,
      expected_func=foo1,
      local_var_prefix="tmp",
      local_var_seq_init=1
    )
    # from pprint import pprint
    # pprint(list((i.opname, i.argval) for i in GetInstructionsTransform()(flattened_ast_node)))
    # pprint(list((i.opname, i.argval) for i in GetInstructionsTransform()(expected_ast_node)))
    self.assertTrue(DiffOpnameAndArgvalTransform()(flattened_ast_node, expected_ast_node))

  def test_unpack_store_attr_store_subscr(self): 
    def foo0(a, b):
      bar0().x[bar1()], bar0().y[bar1()] = a, a + b
    def foo1(a, b):
      tmp1, tmp4 = a, a + b
      tmp2 = bar0().x
      tmp3 = bar1()
      tmp2[tmp3] = tmp1
      tmp5 = bar0().y
      tmp6 = bar1()
      tmp5[tmp6] = tmp4
    flattened_ast_node, expected_ast_node = self.get_flattened_and_expected(
      origin_func=foo0,
      expected_func=foo1,
      local_var_prefix="tmp",
      local_var_seq_init=1
    )
    # from pprint import pprint
    # pprint(list((i.opname, i.argval) for i in GetInstructionsTransform()(flattened_ast_node)))
    # pprint(list((i.opname, i.argval) for i in GetInstructionsTransform()(expected_ast_node)))
    self.assertTrue(DiffOpnameAndArgvalTransform()(flattened_ast_node, expected_ast_node))


if __name__ == '__main__':
    unittest.main()
