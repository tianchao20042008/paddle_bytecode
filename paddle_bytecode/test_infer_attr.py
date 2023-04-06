from typing import Set, Dict, Callable
import unittest
import dis
from paddle_bytecode.convert_to_bytecode_ast import convert_to_bytecode_ast
from paddle_bytecode import bytecode_attr
from paddle_bytecode import bytecode_ast
from paddle_bytecode.infer_attr_transform import InferAttrTransform
from paddle_bytecode.dump_transform import DumpTransform
from paddle_bytecode.get_instructions_transform import GetInstructionsTransform
from paddle_bytecode.get_leaf_ast_nodes_transform import GetLeafAstNodesTransform
from paddle_bytecode.symbolic_expression_transform import SymbolicExpressionTransform
import paddle_bytecode.mock_is_procedure_static_convertible_transform as mock


class TestInferAttr(unittest.TestCase):
  def check_lifetime(self,
                     f,
                     dynamic_func_names: Set[str],
                     builtin_funcs: Dict[str, Callable[["BytecodeAstNode", "BytecodeAttr"], None]]):
    ast_node = convert_to_bytecode_ast(list(dis.get_instructions(f)))
    attr, mut_attr = bytecode_attr.BytecodeAttr.make_gettable_and_mutable()
    old_builtin_funcs = builtin_funcs
    builtin_funcs = {
      name: lambda node: old_builtin_funcs[name](node, attr) for name,_ in old_builtin_funcs.items()
    }
    def is_procedure_static_convertible(ast_node):
      assert isinstance(ast_node, bytecode_ast.InstructionNodeBase)
      if ast_node.instruction.opname in {"LOAD_GLOBAL", "LOAD_DEREF"}:
        return not (ast_node.instruction.argval in dynamic_func_names)
      return True
    is_procedure_static_convertible = (
      mock.MockIsProcedureStaticConvertibleTransform(is_procedure_static_convertible)(ast_node)
    )
    def is_result_static_convertible(ast_node):
      return (True,) * ast_node.num_outputs_on_stack()
    infer_attr = InferAttrTransform(
      mut_attr,
      is_procedure_static_convertible,
      is_result_static_convertible
    )
    infer_attr(ast_node)
    symblic_interp = SymbolicExpressionTransform(builtin_funcs)
    symblic_interp(ast_node)

  def test_check_lifetime_static(self): 
    def foo():
      x = 30
      return check_lifetime_static(x)
    def check_lifetime_static(ast_node, attr):
      self.assertEqual(attr(ast_node).lifetime_allways_static, (True,))
    self.check_lifetime(
      foo,
      dynamic_func_names=set(),
      builtin_funcs=dict(check_lifetime_static=check_lifetime_static)
    )

  def test_check_lifetime_dynamic(self): 
    def foo():
      check_lifetime_static(bar())
    def check_lifetime_static(ast_node, attr):
      self.assertEqual(attr(ast_node).lifetime_allways_static, (False,))
    self.check_lifetime(
      foo,
      dynamic_func_names={"bar"},
      builtin_funcs=dict(check_lifetime_static=check_lifetime_static)
    )

  def test_check_lifetime_dynamic_nested(self): 
    def foo():
      x = bar(check_lifetime_static(bar()))
    def check_lifetime_static(ast_node, attr):
      self.assertEqual(attr(ast_node).lifetime_allways_static, (False,))
    self.check_lifetime(
      foo,
      dynamic_func_names={"bar"},
      builtin_funcs=dict(check_lifetime_static=check_lifetime_static)
    )

  def test_check_dynamic_then_static(self): 
    def foo():
      x = check_lifetime_static(bar()) + 1
    def check_lifetime_static(ast_node, attr):
      self.assertEqual(attr(ast_node).lifetime_allways_static, (False,))
    self.check_lifetime(
      foo,
      dynamic_func_names={"bar"},
      builtin_funcs=dict(check_lifetime_static=check_lifetime_static)
    )

  def test_check_dynamic_then_static_math_op(self): 
    def foo():
      x = check_lifetime_static(bar() + 1)
    def check_lifetime_static(ast_node, attr):
      self.assertEqual(attr(ast_node).lifetime_allways_static, (True,))
    self.check_lifetime(
      foo,
      dynamic_func_names={"bar"},
      builtin_funcs=dict(check_lifetime_static=check_lifetime_static)
    )

  def test_is_procedure_static_convertible_nested_dynamic_then_static(self): 
    def foo():
      x = check_lifetime_static(static_func(bar())) + 1
    def check_lifetime_static(ast_node, attr):
      self.assertEqual(attr(ast_node).is_procedure_static_convertible, True)
    self.check_lifetime(
      foo,
      dynamic_func_names={"bar"},
      builtin_funcs=dict(check_lifetime_static=check_lifetime_static)
    )

  def test_is_procedure_static_convertible_nested_static_then_dynamic(self): 
    def foo():
      x = check_lifetime_static(bar(static_func())) + 1
    def check_lifetime_static(ast_node, attr):
      self.assertEqual(attr(ast_node).is_procedure_static_convertible, False)
    self.check_lifetime(
      foo,
      dynamic_func_names={"bar"},
      builtin_funcs=dict(check_lifetime_static=check_lifetime_static)
    )

