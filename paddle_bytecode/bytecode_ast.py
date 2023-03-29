from . import instr_stack_util

class BytecodeAstNode:
  def __init__(self, data=None):
    self.data = data

  def flat_children(self):
    raise NotImplementedError()

class StatementListNode(BytecodeAstNode):
  def __init__(self, children, **kwargs):
    super().__init__(**kwargs)
    self.children = children

  def flat_children(self):
    yield from self.children

class StatementNode(BytecodeAstNode):
  def __init__(self, expr_node, store_instructions, **kwargs):
    super().__init__(**kwargs)
    self.expr_node = expr_node
    self.store_instructions = store_instructions

  def flat_children(self):
    yield self.expr_node
    for instructions in self.store_instructions:
      yield from instructions


class ExpressionNode(BytecodeAstNode):
  def __init__(self, children, **kwargs):
    super().__init__(**kwargs)
    self.children = children

  def num_outputs_on_stack(self):
    return self.children[-1].num_outputs_on_stack()

  def flat_children(self):
    yield from self.children

class InstructionNodeBase(BytecodeAstNode):
  def __init__(self, instruction, **kwargs):
    super().__init__(**kwargs)
    self.instruction = instruction

  def flat_children(self):
    yield from []

  def num_inputs_on_stack(self):
    return instr_stack_util.num_inputs_on_stack(self.instruction)

  def num_outputs_on_stack(self):
    return instr_stack_util.num_outputs_on_stack(self.instruction)


class InstructionNode(InstructionNodeBase):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)


class LOAD_CONST(InstructionNodeBase):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)


class LOAD_FAST(InstructionNodeBase):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)


class STORE_FAST(InstructionNodeBase):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
