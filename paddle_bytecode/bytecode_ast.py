from . import instr_stack_util

class BytecodeAstNode:
  def __init__(self):
    pass

  def flat_children(self):
    raise NotImplementedError()

class StatementListNode(BytecodeAstNode):
  def __init__(self, children):
    super().__init__()
    self.children = children

  def flat_children(self):
    yield from self.children

class StatementNode(BytecodeAstNode):
  def __init__(self, expr_node, store_nodes):
    super().__init__()
    self.expr_node = expr_node
    self.store_nodes = store_nodes

  def flat_children(self):
    yield self.expr_node
    for instructions in self.store_nodes:
      yield from instructions

class ExpressionNodeBase(BytecodeAstNode):
  def __init__(self, children):
    super().__init__()
    self.children = children

  def num_outputs_on_stack(self):
    return self.children[-1].num_outputs_on_stack()

  def flat_children(self):
    yield from self.children

class ExpressionNode(ExpressionNodeBase):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

class MakeFunctionExprNode(ExpressionNodeBase):
  def __init__(self, children):
    super().__init__(children)
    self._function_body : StatementListNode = None

    @property
    def function_body(self):
      assert self._function_body is not None
      return self._function_body

    @function_body.setter
    def function_body(self, value):
      self._function_body = value

class InstructionNodeBase(BytecodeAstNode):
  def __init__(self, instruction):
    super().__init__()
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
