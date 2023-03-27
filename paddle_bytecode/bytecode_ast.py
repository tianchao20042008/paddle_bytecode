class BytecodeAstNode:
  def __init__(self):
    pass


class StatementListNode(BytecodeAstNode):
  def __init__(self, children):
    super().__init__(self)
    self.children = children


class InstructionNode(BytecodeAstNode):
  def __init__(self, instruction):
    super().__init__(self)
    self.instruction = instruction

class ExpressionNode(BytecodeAstNode):
  def __init__(self, children):
    super().__init__(self)
    self.children = children
