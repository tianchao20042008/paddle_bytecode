class DiffOpnameAndArgvalInterpreter:

  def diff(self, lhs_ast_node, rhs_ast_node):
    ast_cls = type(lhs_ast_node)
    if ast_cls != type(rhs_ast_node):
      return False
    if hasattr(lhs_ast_node, "instruction") and hasattr(rhs_ast_node, "instruction"):
      return self.compare_opname_and_argval(lhs_ast_node, rhs_ast_node)
    lhs_flat_children = list(lhs_ast_node.flat_children())
    rhs_flat_children = list(rhs_ast_node.flat_children())
    if len(lhs_flat_children) != len(rhs_flat_children):
      return False
    for lhs_child, rhs_child in zip(lhs_flat_children, rhs_flat_children):
      if not self.diff(lhs_child, rhs_child):
        return False
    return True

  def compare_opname_and_argval(self, lhs_ast_node, rhs_ast_node):
    return (lhs_ast_node.instruction.opname == rhs_ast_node.instruction.opname
      and lhs_ast_node.instruction.argval == rhs_ast_node.instruction.argval)
