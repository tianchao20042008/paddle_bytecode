from .get_leaf_ast_nodes_transform import GetLeafAstNodesTransform

class GetInstructionsTransform:
  def __call__(self, ast_node):
    for ast_node in GetLeafAstNodesTransform()(ast_node):
      yield ast_node.instruction
