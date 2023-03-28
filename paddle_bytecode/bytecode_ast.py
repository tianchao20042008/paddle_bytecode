from . import instr_stack_util

class BytecodeAstNode:
  def __init__(self,
              is_procedure_static_convertible=None,
              is_result_static_convertible=(),
              lifetime_allways_static=None):
    # True if no dynamic python code touched when running this ast_node.
    self.is_procedure_static_convertible = is_procedure_static_convertible
    # tuple of bool.
    # self.is_result_static_convertible[i] is True if the ith result of this ast_node are static convertible.
    self.is_result_static_convertible = is_result_static_convertible
    # True if no dynamic python code touched during the lifetime of the results of this ast_node.
    self.lifetime_allways_static = lifetime_allways_static


class StatementListNode(BytecodeAstNode):
  def __init__(self, children, **kwargs):
    super().__init__(**kwargs)
    self.children = children


class StatementNode(BytecodeAstNode):
  def __init__(self, expr_node, store_instructions, **kwargs):
    super().__init__(**kwargs)
    self.expr_node = expr_node
    self.store_instructions = store_instructions


class ExpressionNode(BytecodeAstNode):
  def __init__(self, children, **kwargs):
    super().__init__(**kwargs)
    self.children = children

  def num_outputs_on_stack(self):
    return self.children[-1].num_outputs_on_stack()


class InstructionNodeBase(BytecodeAstNode):
  def __init__(self, instruction, **kwargs):
    super().__init__(**kwargs)
    self.instruction = instruction

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
