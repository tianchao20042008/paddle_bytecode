from typing import Callable
from dataclasses import dataclass

class InferLifetimeAllwaysStaticTransform:
  def __init__(self, attr: Callable[["BytecodeAstNode"], "BytecodeAttr"]):
    self.attr = attr

@dataclass
class InferCtx:
  # tuple of bool.
  # is_result_allways_static_from_now_on[i] is True if the ith result of this ast_node is 
  # encountering only static python code before destruction.
  # is_result_allways_static_from_now_on[i] is False if the ith result of this ast_node is
  # used by dynamic python code.
  # is_result_allways_static_from_now_on[i] is False if dynamic python code executed
  # before the destruction of the ith result of this ast_node.
  is_result_allways_static_from_now_on: tuple = ()

  @staticmethod
  def make_getter(node2ctx: dict = None):
    node2ctx = {} if node2ctx is None else node2ctx
    def getter(node):
      if node not in node2ctx:
        node2ctx[node] = InferCtx()
      return node2ctx[node]
    return getter

class InferIsResultAllwaysStaticFromNowOnTransform:
  def __init__(self, attr: Callable[["BytecodeAstNode"], InferCtx]):
    self.attr = attr

  def infer(self, ast_node, consumed_by_static=True):
    return getattr(self, type(ast_node).__name__)(ast_node)
    
  def StatementListNode(self, ast_node, consumed_by_static):
    reversed_children = ast_node.children[::-1]
    for child in reversed_children:
      self.infer(child, consumed_by_static=True)

  def StatementNode(self, ast_node, consumed_by_static):
    for store_nodes in ast_node.store_nodes[::-1]:
      for store_node in store_nodes[::-1]:
        self.infer(store_node)
    self.infer(ast_node.expr_node)

  def ExpressionNode(self, ast_node, consumed_by_static):
    reversed_children = ast_node.children[::-1]
    for child in reversed_children:
      self.infer(child, consumed_by_static=True)

  def InstructionNode(self, ast_node, consumed_by_static):
    pass

  def LOAD_CONST(self, ast_node, consumed_by_static):
    pass

  def LOAD_FAST(self, ast_node, consumed_by_static):
    pass

  def STORE_FAST(self, ast_node, consumed_by_static):
    pass

