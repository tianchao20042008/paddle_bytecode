from typing import Callable, Any

class DumpAttrTransform:

  def __init__(self, attr: Callable[["BytecodeAstNode"], Any]):
    self.attr = attr

  def __call__(self, ast_node):
    ast_cls = type(ast_node)
    if not hasattr(self, ast_cls.__name__):
      assert len(ast_cls.__bases__) == 1
      ast_cls = ast_cls.__bases__[0]
    return getattr(self, ast_cls.__name__)(ast_node)

  def StatementListNode(self, ast_node):
    return list([self(child) for child in ast_node.children])

  def StoreNodeBase(self, ast_node):
    return (self(ast_node.expr_node),
            list([tuple(self(instr) for instr in instrs) for instrs in ast_node.store_nodes]),
            self.attr(ast_node))

  def ExpressionNodeBase(self, ast_node):
    return (
      tuple(self(child) for child in ast_node.children),
      self.attr(ast_node),
    )

  def InstructionNodeBase(self, ast_node):
    return (
      ast_node.instruction.opname, ast_node.instruction.argval,
      self.attr(ast_node)
    )
