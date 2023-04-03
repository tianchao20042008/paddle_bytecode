from typing import Callable

class CloneTransform:

  def clone(self, ast_node):
    ast_cls = type(ast_node)
    if not hasattr(self, ast_cls.__name__):
      assert len(ast_cls.__bases__) == 1
      ast_cls = ast_cls.__bases__[0]
    return getattr(self, ast_cls.__name__)(ast_node)

  def StatementListNode(self, ast_node):
    return type(ast_node)([self.clone(child) for child in ast_node.children])

  def StatementNode(self, ast_node):
    return type(ast_node)(self.clone(ast_node.expr_node),
            list([tuple(self.clone(instr) for instr in instrs) for instrs in ast_node.store_nodes]))

  def ExpressionNode(self, ast_node):
    return type(ast_node)(tuple(self.clone(child) for child in ast_node.children))

  def InstructionNodeBase(self, ast_node):
    return type(ast_node)(ast_node.instruction)
