from . import instr_stack_util

class BytecodeAstNode:
  def __init__(self, is_static_convertible=None, lifetime_allways_static=None):
    self.is_static_convertible = is_static_convertible
    self.lifetime_allways_static = lifetime_allways_static


class StatementListNode(BytecodeAstNode):
  def __init__(self, children, **kwargs):
    super().__init__(**kwargs)
    self.children = children

  def dump(self):
    return list([child.dump() for child in self.children])

class StatementNode(BytecodeAstNode):
  def __init__(self, expr_node, store_instructions, **kwargs):
    super().__init__(**kwargs)
    self.expr_node = expr_node
    self.store_instructions = store_instructions

  def dump(self):
    return (self.expr_node.dump(),
            list([tuple(instr.dump() for instr in instrs) for instrs in self.store_instructions]))

class ExpressionNode(BytecodeAstNode):
  def __init__(self, children, **kwargs):
    super().__init__(**kwargs)
    self.children = children

  def num_outputs_on_stack(self):
    return self.children[-1].num_outputs_on_stack()

  def dump(self):
    return tuple(child.dump() for child in self.children)

class InstructionNode(BytecodeAstNode):
  def __init__(self, instruction, **kwargs):
    super().__init__(**kwargs)
    self.instruction = instruction

  def num_inputs_on_stack(self):
    return instr_stack_util.num_inputs_on_stack(self.instruction)

  def num_outputs_on_stack(self):
    return instr_stack_util.num_outputs_on_stack(self.instruction)

  def dump(self):
    return (self.instruction.opname, self.instruction.arg, self.instruction.argval)
