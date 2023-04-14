from typing import Callable

class CloneTransform:

  def __call__(self, ast_node):
    ast_cls = type(ast_node)
    if not hasattr(self, ast_cls.__name__):
      assert len(ast_cls.__bases__) == 1
      ast_cls = ast_cls.__bases__[0]
    return getattr(self, ast_cls.__name__)(ast_node)

  def Program(self, ast_node):
    return type(ast_node)([self(child) for child in ast_node.children])

  def LabelNode(self, ast_node):
    return ast_node 

  def StatementListNode(self, ast_node):
    return type(ast_node)([self(child) for child in ast_node.children])

  def StoreNodeBase(self, ast_node):
    return type(ast_node)(self(ast_node.expr_node),
            list([tuple(self(instr) for instr in instrs) for instrs in ast_node.store_nodes]))

  def GenericExpressionNode(self, ast_node):
    return type(ast_node)(tuple(self(child) for child in ast_node.children))

  def InstructionNodeBase(self, ast_node):
    return type(ast_node)(ast_node.instruction)
