from .get_leaf_ast_nodes_transform import GetLeafAstNodesTransform

class GetInstructionsTransform:
  def get_instructions(self, ast_node):
    for ast_node in GetLeafAstNodesTransform().get_leaf_ast_nodes(ast_node):
      yield ast_node.instruction
