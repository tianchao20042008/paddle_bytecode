from typing import Set, Dict, Callable
import unittest
import dis
from paddle_bytecode.convert_to_bytecode_ast import convert_to_bytecode_ast
from paddle_bytecode import bytecode_attr
from paddle_bytecode import bytecode_ast
from paddle_bytecode.infer_attr_transform import InferAttrTransform
from paddle_bytecode.dump_transform import DumpTransform
from paddle_bytecode.dump_attr_transform import DumpAttrTransform
from paddle_bytecode.get_instructions_transform import GetInstructionsTransform
from paddle_bytecode.get_leaf_ast_nodes_transform import GetLeafAstNodesTransform
from paddle_bytecode.symbolic_expression_transform import SymbolicExpressionTransform
from paddle_bytecode.is_statement_static_convertible_transform import IsStatementStaticConvertibleTransform
import paddle_bytecode.mock_is_procedure_static_convertible_transform as mock
from pprint import pprint


class TestInferAttr(unittest.TestCase):
  def check_attr(self,
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

  def check_is_static_convertible(
      self,
      f,
      dynamic_func_names: Set[str],
      builtin_funcs: Dict[str, Callable[["BytecodeAstNode", "BytecodeAttr"], None]]):
    ast_node = convert_to_bytecode_ast(list(dis.get_instructions(f)))
    attr, mut_attr = bytecode_attr.BytecodeAttr.make_gettable_and_mutable()
    bool_attr = IsStatementStaticConvertibleTransform(attr)
    old_builtin_funcs = builtin_funcs
    builtin_funcs = {
      name: lambda node: old_builtin_funcs[name](node, bool_attr) for name,_ in old_builtin_funcs.items()
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
    print('-'*80)
    pprint(DumpAttrTransform(IsStatementStaticConvertibleTransform(attr))(ast_node))
    print('-'*80)
    symblic_interp = SymbolicExpressionTransform(builtin_funcs)
    symblic_interp(ast_node)

  def test_is_static_convertible_return(self): 
    def foo():
      x = static_func() + 1
      check(x)
      return x
    def check(ast_node, attr):
      pprint(DumpTransform()(ast_node))
      pprint(attr(ast_node))
      # self.assertEqual(attr(ast_node), False)
    self.check_is_static_convertible(
      foo,
      dynamic_func_names=set('check'),
      builtin_funcs=dict(check=check)
    )

if __name__ == '__main__':
    unittest.main()
