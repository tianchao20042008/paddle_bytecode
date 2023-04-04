class GetLeafAstNodesTransform:

  def get_leaf_ast_nodes(self, ast_node):
    children = list(ast_node.flat_children())
    if len(children) == 0:
      yield ast_node
    else:
      for child in children:
        yield from self.get_leaf_ast_nodes(child)
