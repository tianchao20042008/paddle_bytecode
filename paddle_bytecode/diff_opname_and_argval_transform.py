from . import bytecode_ast

class DiffOpnameAndArgvalTransform:

  def __call__(self, lhs_ast_node, rhs_ast_node):
    ast_cls = type(lhs_ast_node)
    if ast_cls != type(rhs_ast_node):
      return False
    if not hasattr(self, ast_cls.__name__):
      assert len(ast_cls.__bases__) == 1
      ast_cls = ast_cls.__bases__[0]
    if hasattr(self, ast_cls.__name__):
      return getattr(self, ast_cls.__name__)(lhs_ast_node, rhs_ast_node)
    else:
      lhs_flat_children = list(lhs_ast_node.flat_children())
      rhs_flat_children = list(rhs_ast_node.flat_children())
      if len(lhs_flat_children) != len(rhs_flat_children):
        return False
      for lhs_child, rhs_child in zip(lhs_flat_children, rhs_flat_children):
        if not self(lhs_child, rhs_child):
          return False
      return True

  def MakeFunctionExprNode(self, lhs_ast_node, rhs_ast_node):
    return self(lhs_ast_node.function_body, rhs_ast_node.function_body)

  def InstructionNodeBase(self, lhs_ast_node, rhs_ast_node):
    return (lhs_ast_node.instruction.opname == rhs_ast_node.instruction.opname
      and lhs_ast_node.instruction.argval == rhs_ast_node.instruction.argval)
