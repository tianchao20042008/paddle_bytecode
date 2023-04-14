from typing import Callable

class DumpTransform:

  def __call__(self, ast_node):
    ast_cls = type(ast_node)
    while not hasattr(self, ast_cls.__name__):
      assert len(ast_cls.__bases__) == 1
      ast_cls = ast_cls.__bases__[0]
    assert hasattr(self, ast_cls.__name__), "type(ast_node): %s" % type(ast_node)
    return getattr(self, ast_cls.__name__)(ast_node)

  def Program(self, ast_node):
    return list([self(child) for child in ast_node.flat_children_except_label()])

  def StmtExpressionNode(self, ast_node):
    if len(ast_node.statement_list_node.children) > 0:
      return (self(ast_node.statement_list_node), self(ast_node.expr_node))
    else:
      return self(ast_node.expr_node)

  def StatementListNode(self, ast_node):
    return list([self(child) for child in ast_node.children])

  def StoreNodeBase(self, ast_node):
    return (self(ast_node.expr_node),
            list([tuple(self(instr) for instr in instrs) for instrs in ast_node.store_nodes]))

  def ExpressionNodeBase(self, ast_node):
    return (tuple(self(child) for child in ast_node.children))

  def MakeFunctionExprNode(self, ast_node):
    return (self(ast_node.function_body), tuple(map(self.__call__, ast_node.children)))

  def InstructionNodeBase(self, ast_node):
    return (ast_node.instruction.opname, ast_node.instruction.argval)
