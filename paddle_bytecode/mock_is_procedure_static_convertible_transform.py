from typing import Callable
from . import bytecode_ast

class MockIsProcedureStaticConvertibleTransform:
  def __init__(self,
               get_is_procedure_static_convertible: Callable[["ByteocdeAstNode"], bool]):
    self.old_get_is_procedure_static_convertible = get_is_procedure_static_convertible
    (self.get_is_procedure_static_convertible, self.set_is_procedure_static_convertible) = (
      self.make_updated_getter_and_setter(get_is_procedure_static_convertible)
    )

  def make_updated_getter_and_setter(
      self, get_is_procedure_static_convertible: Callable[["ByteocdeAstNode"], bool]):
    ast_node2is_procedure_static_convertible = {}
    def new_get_is_procedure_static_convertible(ast_node):
      if ast_node in ast_node2is_procedure_static_convertible:
        return ast_node2is_procedure_static_convertible[ast_node]
      else:
        return get_is_procedure_static_convertible(ast_node)
    def set_is_procedure_static_convertible(ast_node, val):
      ast_node2is_procedure_static_convertible[ast_node] = val
    return new_get_is_procedure_static_convertible, set_is_procedure_static_convertible


  def mock(self, ast_node):
    ast_cls = type(ast_node)
    if not hasattr(self, ast_cls.__name__):
      assert len(ast_cls.__bases__) == 1
      ast_cls = ast_cls.__bases__[0]
    if hasattr(self, ast_cls.__name__):
      getattr(self, ast_cls.__name__)(ast_node)
    else:
      self.mock_flat_children(ast_node)
    return self.get_is_procedure_static_convertible

  def mock_flat_children(self, ast_node):
    for child in ast_node.flat_children():
      self.mock(child)

  def ExpressionNode(self, ast_node):
    for child in ast_node.children:
      self.mock(child)
    if not isinstance(ast_node.children[0], bytecode_ast.InstructionNodeBase):
      return
    if not isinstance(ast_node.children[-1], bytecode_ast.InstructionNodeBase):
      return
    if ast_node.children[-1].instruction.opname != "CALL_FUNCTION":
      return
    if ast_node.children[0].instruction.opname not in {"LOAD_GLOBAL", "LOAD_DEREF"}:
      return
    self.set_is_procedure_static_convertible(
      ast_node.children[-1],
      self.get_is_procedure_static_convertible(ast_node.children[0])
    )
