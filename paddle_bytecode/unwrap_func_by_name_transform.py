from . import bytecode_ast

class UnwrapFuncByNameTransform:

  def __init__(self, func_name):
    self.func_name = func_name

  def __call__(self, ast_node):
    ast_cls = type(ast_node)
    if not hasattr(self, ast_cls.__name__):
      assert len(ast_cls.__bases__) == 1
      ast_cls = ast_cls.__bases__[0]
    return getattr(self, ast_cls.__name__)(ast_node)

  def StatementListNode(self, ast_node):
    return type(ast_node)([self(child) for child in ast_node.children])

  def StatementNode(self, ast_node):
    return type(ast_node)(
      self(ast_node.expr_node),
      list([tuple(self(instr) for instr in instrs) for instrs in ast_node.store_nodes])
    )

  def ExpressionNode(self, ast_node):
    if not isinstance(ast_node.children[-1], bytecode_ast.InstructionNodeBase):
      return self.NaiveProcessExpressionNode(ast_node)
    else:
      opname = ast_node.children[-1].instruction.opname
      if hasattr(self, opname):
        return getattr(self, opname)(ast_node)
      else:
        return self.NaiveProcessExpressionNode(ast_node)

  def CALL_FUNCTION(self, ast_node):
    children = ast_node.children
    if len(children) != 3:
      return self.NaiveProcessExpressionNode(ast_node)
    elif not isinstance(children[0], bytecode_ast.InstructionNodeBase):
      return self.NaiveProcessExpressionNode(ast_node)
    elif not isinstance(children[0], bytecode_ast.InstructionNodeBase):
      return self.NaiveProcessExpressionNode(ast_node)
    elif children[0].instruction.opname != "LOAD_GLOBAL":
      return self.NaiveProcessExpressionNode(ast_node)
    elif children[0].instruction.argval != self.func_name:
      return self.NaiveProcessExpressionNode(ast_node)
    else:
      return self(children[1])

  def NaiveProcessExpressionNode(self, ast_node):
      return type(ast_node)(tuple(self(child) for child in ast_node.children))

  def InstructionNodeBase(self, ast_node):
    return type(ast_node)(ast_node.instruction)
