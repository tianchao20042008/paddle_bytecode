from typing import Callable
import paddle_bytecode.bytecode_ast as bytecode_ast

class PrintTransform:

  def __call__(self, ast_node, depth=0):
    ast_cls = type(ast_node)
    while not hasattr(self, ast_cls.__name__) and ast_cls is not bytecode_ast.BytecodeAstNode:
      assert len(ast_cls.__bases__) == 1, type(ast_node)
      ast_cls = ast_cls.__bases__[0]
    assert hasattr(self, ast_cls.__name__), "type(ast_node): %s" % type(ast_node)
    return getattr(self, ast_cls.__name__)(ast_node, depth)

  def num_space_for_tab(self):
    return 2

  def Program(self, ast_node, depth):
    print("Program:\n")
    for child in  ast_node.flat_children():
      self(child, depth=depth+1)

  def LabelNode(self, ast_node, depth):
    depth = depth - 1 if depth > 0 else depth
    print("%s%s:" % (' ' * depth * self.num_space_for_tab(), ast_node.offset))

  def StmtExpressionNode(self, ast_node, depth):
    self(ast_node.statement_list_node, depth)
    self(ast_node.expr_node, depth)

  def StatementListNode(self, ast_node, depth):
    for child in ast_node.children:
      self(child, depth)

  def StoreNodeBase(self, ast_node, depth):
    self(ast_node.expr_node, depth+1)
    for instrs in ast_node.store_nodes:
      for instr in instrs:
        self(instr, depth)

  def ExpressionNodeBase(self, ast_node, depth):
    for child in ast_node.children[:-1]:
      self(child, depth=depth+1)
    self(ast_node.children[-1], depth=depth)

  def MakeFunctionExprNode(self, ast_node, depth):
    self(ast_node.function_body, depth=depth+1)
    for child in ast_node.children:
      self(child, depth)

  def InstructionNodeBase(self, ast_node, depth):
    print("%s%s%s%s" %
      (
        ' ' * depth * self.num_space_for_tab(),
        ast_node.instruction.opname,
        ' ' * self.num_space_for_tab(),
        ast_node.instruction.argval
      )
    )
