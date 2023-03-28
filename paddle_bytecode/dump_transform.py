class DumpTransform:

  def dump(self, ast_node):
    ast_cls = type(ast_node)
    if not hasattr(self, ast_cls.__name__):
      assert len(ast_cls.__bases__) == 1
      ast_cls = ast_cls.__bases__[0]
    return getattr(self, ast_cls.__name__)(ast_node)

  def StatementListNode(self, ast_node):
    return list([self.dump(child) for child in ast_node.children])

  def StatementNode(self, ast_node):
    return (self.dump(ast_node.expr_node),
            list([tuple(self.dump(instr) for instr in instrs) for instrs in ast_node.store_instructions]))

  def ExpressionNode(self, ast_node):
    return (tuple(self.dump(child) for child in ast_node.children), ast_node.is_procedure_static_convertible)

  def InstructionNodeBase(self, ast_node):
    return (ast_node.instruction.opname, ast_node.instruction.arg, ast_node.instruction.argval, ast_node.is_procedure_static_convertible)
