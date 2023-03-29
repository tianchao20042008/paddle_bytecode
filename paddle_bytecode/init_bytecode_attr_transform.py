import bytecode_attr

class InitBytecodeAttrTransform:
  def init(self, ast_node):
    ast_node.data = bytecode_attr.BytecodeAttr()
    for child in ast_node.flat_children():
      self.init(child)
