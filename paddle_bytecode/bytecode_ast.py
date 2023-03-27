from . import instr_stack_util

class BytecodeAstNode:
  def __init__(self):
    pass

class StatementListNode(BytecodeAstNode):
  def __init__(self, children):
    super().__init__()
    self.children = children

  def dump(self):
    return list([child.dump() for child in self.children])

class StatementNode(BytecodeAstNode):
  def __init__(self, expr_node, store_instructions):
    super().__init__()
    self.expr_node = expr_node
    self.store_instructions = store_instructions

  def dump(self):
    return (self.expr_node.dump(), [instr.dump() for instr in self.store_instructions])

class ExpressionNode(BytecodeAstNode):
  def __init__(self, children):
    super().__init__()
    self.children = children

  def num_outputs_on_stack(self):
    return self.children[-1].num_outputs_on_stack()

  def dump(self):
    return tuple(child.dump() for child in self.children)

class InstructionNode(BytecodeAstNode):
  def __init__(self, instruction):
    super().__init__()
    self.instruction = instruction

  def num_inputs_on_stack(self):
    return instr_stack_util.num_inputs_on_stack(self.instruction)

  def num_outputs_on_stack(self):
    return instr_stack_util.num_outputs_on_stack(self.instruction)

  def dump(self):
    return (self.instruction.opname, self.instruction.arg, self.instruction.argval)
