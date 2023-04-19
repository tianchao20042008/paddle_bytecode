import unittest
import dis
from paddle_bytecode.convert_to_bytecode_ast import convert_to_bytecode_ast
from paddle_bytecode import bytecode_attr
from paddle_bytecode.infer_attr_transform import InferAttrTransform
from paddle_bytecode.clone_transform import CloneTransform
from paddle_bytecode.flatten_left_value_transform import FlattenLeftValueTransform
from paddle_bytecode.flatten_right_value_transform import FlattenRightValueTransform
from paddle_bytecode.diff_opname_and_argval_transform import DiffOpnameAndArgvalTransform
from paddle_bytecode.fuse_trace_transform import FuseTraceTransform
from paddle_bytecode.dump_transform import DumpTransform
from paddle_bytecode.dump_attr_transform import DumpAttrTransform
from paddle_bytecode.pretty_string_transform import PrettyStringTransform
from paddle_bytecode.get_instructions_transform import GetInstructionsTransform
import paddle_bytecode.mock_is_procedure_static_convertible_transform as mock

class TestFuseTrace(unittest.TestCase):
  def make_getter_generate_local_varname(self, prefix, init=0):
    counter = init - 1 # `counter++` will be used later.
    def generate_local_varname():
      nonlocal counter
      counter += 1
      return prefix + str(counter)
    return generate_local_varname

  def infer_attr(self, ast_node, is_procedure_static_convertible, is_result_static_convertible):
    attr, mut_attr = bytecode_attr.BytecodeAttr.make_gettable_and_mutable()
    is_procedure_static_convertible = (
      mock.MockIsProcedureStaticConvertibleTransform(is_procedure_static_convertible)(ast_node)
    )
    infer_attr = InferAttrTransform(
      mut_attr,
      is_procedure_static_convertible,
      is_result_static_convertible
    )
    infer_attr(ast_node)
    return attr

  def flatten_bytecode(self, f,
                       is_procedure_static_convertible,
                       is_result_static_convertible,
                       generate_local_varname):
    ast_node = convert_to_bytecode_ast(list(dis.get_instructions(f)))
    flatten_lvalue = FlattenLeftValueTransform(generate_local_varname)
    ast_node = flatten_lvalue(ast_node)
    attr = self.infer_attr(
      ast_node=ast_node,
      is_procedure_static_convertible=is_procedure_static_convertible,
      is_result_static_convertible=is_result_static_convertible
    )
    flatten_rvalue = FlattenRightValueTransform(generate_local_varname, attr)
    return flatten_rvalue(ast_node)

  def get_trace_fused_ast_nodes_and_expected(
        self,
        origin_func,
        expected_func,
        builtin_dynamic_funcs,
        local_var_prefix,
        local_var_seq_init,
        func_name_prefix,
        func_name_seq_init):
    def is_procedure_static_convertible(ast_node):
      return not (
        ast_node.instruction.opname == "LOAD_GLOBAL"
        and ast_node.instruction.argval in builtin_dynamic_funcs
      )
    is_result_static_convertible = lambda ast_node: (True,) * ast_node.num_outputs_on_stack()
    generate_local_varname = self.make_getter_generate_local_varname(
      local_var_prefix, init=local_var_seq_init
    )
    generate_func_name = self.make_getter_generate_local_varname(
      func_name_prefix, init=func_name_seq_init
    )
    ast_node0 = self.flatten_bytecode(
      origin_func,
      is_procedure_static_convertible=is_procedure_static_convertible,
      is_result_static_convertible=is_result_static_convertible,
      generate_local_varname=generate_local_varname
    )
    attr = self.infer_attr(
      ast_node=ast_node0,
      is_procedure_static_convertible=is_procedure_static_convertible,
      is_result_static_convertible=is_result_static_convertible,
    )
    from pprint import pprint
    pprint(DumpAttrTransform(lambda node: attr(node).lifetime_allways_static)(ast_node0))
    fuse_trace = FuseTraceTransform(
      func_name=expected_func.__qualname__,
      attr=attr,
      generate_func_name=generate_func_name,
    )
    ast_node0 = fuse_trace(ast_node0)
    ast_node1 = convert_to_bytecode_ast(list(dis.get_instructions(expected_func))) 
    return ast_node0, ast_node1

  def test_pure_static(self): 
    def foo0():
      x = static_bar() + 1
      return x
    def foo1():
      def func0():
        x = static_bar() + 1
        return x
      x = func0()
      return x
    fused_ast_node, expected_ast_node = self.get_trace_fused_ast_nodes_and_expected(
      origin_func=foo0,
      expected_func=foo1,
      builtin_dynamic_funcs=set(),
      local_var_prefix="tmp",
      local_var_seq_init=1,
      func_name_prefix="func",
      func_name_seq_init=0,
    )
    from pprint import pprint
    print('-'*100)
    print(PrettyStringTransform()(fused_ast_node))
    print('-'*100)
    print(PrettyStringTransform()(expected_ast_node))
    print('-'*100)
    self.assertTrue(DiffOpnameAndArgvalTransform()(fused_ast_node, expected_ast_node))

  def _test_simple_dynamic_expression_assign(self): 
    def foo0():
      x = bar() + 1
      return x
    def foo1():
      tmp1 = bar()
      def func0(tmp1):
        x = tmp1 + 1
        return x
      x = func0(tmp1)
      return x
    fused_ast_node, expected_ast_node = self.get_trace_fused_ast_nodes_and_expected(
      origin_func=foo0,
      expected_func=foo1,
      builtin_dynamic_funcs={"bar"},
      local_var_prefix="tmp",
      local_var_seq_init=1,
      func_name_prefix="func",
      func_name_seq_init=0,
    )
    from pprint import pprint
    print('-'*100)
    pprint(DumpTransform()(fused_ast_node))
    print('-'*100)
    pprint(DumpTransform()(expected_ast_node))
    print('-'*100)
    self.assertTrue(DiffOpnameAndArgvalTransform()(fused_ast_node, expected_ast_node))

  def _test_mixed_dynamic_expression_assign(self):
    def foo0(x):
      x = static_func(1 + x, bar(), 2 + x)
      return x
    def foo1(x):
      tmp1 = 1 + x
      tmp2 = bar()
      x = static_func(tmp1, tmp2, 2 + x)
      return x
    flattened_ast_node, expected_ast_node = self.get_trace_fused_ast_nodes_and_expected(
      origin_func=foo0,
      expected_func=foo1,
      builtin_dynamic_funcs={"bar"},
      local_var_prefix="tmp",
      local_var_seq_init=1,
      func_name_prefix="func",
      func_name_seq_init=0,
    )
    self.assertTrue(DiffOpnameAndArgvalTransform()(flattened_ast_node, expected_ast_node))

  def _test_static_dynamic_interleave_expression_assign(self):
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
    flattened_ast_node, expected_ast_node = self.get_trace_fused_ast_nodes_and_expected(
      origin_func=origin_func,
      expected_func=expected_func,
      builtin_dynamic_funcs={"bar"},
      local_var_prefix="tmp",
      local_var_seq_init=1,
      func_name_prefix="func",
      func_name_seq_init=0,
    )
    self.assertTrue(DiffOpnameAndArgvalTransform()(flattened_ast_node, expected_ast_node))

  def _test_nested_dynamic_expression(self):
    def origin_func(x):
      x = bar(bar())
      return x
    def expected_func(x):
      x = bar(bar())
      return x
    flattened_ast_node, expected_ast_node = self.get_trace_fused_ast_nodes_and_expected(
      origin_func=origin_func,
      expected_func=expected_func,
      builtin_dynamic_funcs={"bar"},
      local_var_prefix="tmp",
      local_var_seq_init=1,
      func_name_prefix="func",
      func_name_seq_init=0,
    )
    self.assertTrue(DiffOpnameAndArgvalTransform()(flattened_ast_node, expected_ast_node))

  def _test_nested_static_expression(self):
    def origin_func(x):
      x = static_bar(static_bar())
      return x
    def expected_func(x):
      x = static_bar(static_bar())
      return x
    flattened_ast_node, expected_ast_node = self.get_trace_fused_ast_nodes_and_expected(
      origin_func=origin_func,
      expected_func=expected_func,
      builtin_dynamic_funcs={"bar"},
      local_var_prefix="tmp",
      local_var_seq_init=1,
      func_name_prefix="func",
      func_name_seq_init=0,
    )
    self.assertTrue(DiffOpnameAndArgvalTransform()(flattened_ast_node, expected_ast_node))


if __name__ == '__main__':
    unittest.main()
