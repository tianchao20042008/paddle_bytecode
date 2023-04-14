from .bytecode_ast import InstructionNodeBase

class GetLeafAstNodesTransform:

  def __call__(self, ast_node):
    if isinstance(ast_node, InstructionNodeBase):
      yield ast_node
    else:
      for child in ast_node.flat_children_except_label():
        yield from self(child)
