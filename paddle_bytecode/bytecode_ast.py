from typing import List, Union
from . import instr_stack_util

class BytecodeAstNode:
  def __init__(self):
    pass

  def flat_children(self):
    raise NotImplementedError()


class LabelNode(BytecodeAstNode):
  def __init__(self):
    super().__init__()

  def flat_children(self):
    yield from []

StatementType = Union["StatementListNode", "StmtExpresionNode", "LabelNode", "JumpNodeBase"]
class Program(BytecodeAstNode):
  def __init__(self, children: List[StatementType]):
    super().__init__()
    self.children = children

  def flat_children():
    for child in self.children:
      if not isinstance(child, LabelNode):
        yield child

class StatementListNode(BytecodeAstNode):
  def __init__(self, children):
    super().__init__()
    self.children = children

  def flat_children(self):
    yield from self.children


# Like c gnu extention statement expression `({a; b; c})`.
# https://gcc.gnu.org/onlinedocs/gcc/Statement-Exprs.html
# StmtExpresionNode used to flatten expression in same cases of control flow.
#
# e.g.
#
# origin:
# ```
#   while dynamic_foo()(static_bar(static_bar(x))):
#     ...
# ```
# converted:
# ```
#   while ({tmp = static_bar(static_bar(x)); dynamic_foo()}):
#     ...
# ```
class StmtExpresionNode(BytecodeAstNode):
  def __init__(self, statement_list, expr):
    super().__init__()
    self.statement_list = statement_list
    self.expr = expr

  def flat_children(self):
    yield from self.statement_list
    yield self.expr

class StatementNodeBase(BytecodeAstNode):
  def __init(self):
    super().__init__()
    

class StoreNodeBase(StatementNodeBase):
  def __init__(self, expr_node, store_nodes):
    super().__init__()
    self.expr_node: BytecodeAstNode = expr_node
    self.store_nodes: List[List[BytecodeAstNode]] = store_nodes

  def flat_children(self):
    yield self.expr_node
    for instructions in self.store_nodes:
      yield from instructions

class GenericStoreNode(StoreNodeBase):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

class ReturnValueNode(StoreNodeBase):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

class ExpressionNodeBase(BytecodeAstNode):
  def __init__(self, children):
    super().__init__()
    self.children = children

  def num_outputs_on_stack(self):
    return self.children[-1].num_outputs_on_stack()

  def flat_children(self):
    yield from self.children

class GenericExpressionNode(ExpressionNodeBase):
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

  def stack_effect(self):
    return instr_stack_util.stack_effect(self.instruction)

  @property
  def opname(self):
    return self.instruction.opname

  @property
  def opcode(self):
    return self.instruction.opcode


class GenericInstructionNode(InstructionNodeBase):
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

class RETURN_VALUE(InstructionNodeBase):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)


class JumpNodeBase(InstructionNodeBase):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)


class GenericJumpNode(JumpNodeBase):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

