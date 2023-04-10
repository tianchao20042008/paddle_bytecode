from typing import Callable
from functools import reduce
from . import bytecode_ast
from .instruction import Instruction
import dis

class IsStaticConvertibleTransform:
  def __init__(self, attr: Callable[["BytecodeAstNode"], "BytecodeAttr"]):
    self.attr = attr

  def __call__(self, ast_node):
    ast_cls = type(ast_node)
    if not hasattr(self, ast_cls.__name__):
      assert len(ast_cls.__bases__) == 1
      ast_cls = ast_cls.__bases__[0]
    if hasattr(self, ast_cls.__name__):
      return getattr(self, ast_cls.__name__)(ast_node)
    else:
      return self.attr(ast_node).is_procedure_static_convertible

  def StoreNodeBase(self, ast_node):
    is_result_static_convertible = self.attr(ast_node.expr_node).is_result_static_convertible
    _and = lambda a, b: a and b
    is_expr_static_convertible = reduce(_and, is_result_static_convertible, True)
    def is_store_node_static_convertible(store_nodes):
      for store_node in store_nodes:
        assert isinstance(store_node, bytecode_ast.InstructionNodeBase), (
          "LOAD_* or STORE_* supported only. Please do FlattenLeftValueTransform first."
        )
      print(store_nodes[-1].instruction.opanme, self.attr(store_nodes[-1]).is_procedure_static_convertible)
      return self.attr(store_nodes[-1]).is_procedure_static_convertible
    def is_store_static_convertible():
      store_nodes_is_static_convertible = map(
        is_store_node_static_convertible, ast_node.store_nodes
      )
      reduced_is_static_convertible = reduce( _and, store_nodes_is_static_convertible, True)
      return reduced_is_static_convertible
    static_convertible = is_expr_static_convertible and is_store_static_convertible()
    return static_convertible
