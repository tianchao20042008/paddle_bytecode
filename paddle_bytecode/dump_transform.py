from typing import Callable

class DumpTransform:

  def __call__(self, ast_node):
    ast_cls = type(ast_node)
    if not hasattr(self, ast_cls.__name__):
      assert len(ast_cls.__bases__) == 1
      ast_cls = ast_cls.__bases__[0]
    return getattr(self, ast_cls.__name__)(ast_node)

  def StatementListNode(self, ast_node):
    return list([self(child) for child in ast_node.children])

  def StatementNode(self, ast_node):
    return (self(ast_node.expr_node),
            list([tuple(self(instr) for instr in instrs) for instrs in ast_node.store_nodes]))

  def ExpressionNode(self, ast_node):
    return (tuple(self(child) for child in ast_node.children))

  def InstructionNodeBase(self, ast_node):
    return (ast_node.instruction.opname, ast_node.instruction.argval)
