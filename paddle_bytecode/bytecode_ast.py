from typing import List, Union
from . import instr_stack_util

class BytecodeAstNode:
  def __init__(self):
    pass

  def flat_children(self):
    raise NotImplementedError()

  def flat_children_except_label(self):
    return self.flat_children()


class LabelNode(BytecodeAstNode):
  def __init__(self, offset):
    super().__init__()
    self.offset = offset

  def flat_children(self):
    yield from []

StatementType = Union["StatementListNode", "StmtExpressionNode", "LabelNode", "JumpNodeBase"]
class Program(BytecodeAstNode):
  def __init__(self, children: List[StatementType]):
    super().__init__()
    self.children = children

  def flat_children(self):
    yield from self.children

  def flat_children_except_label(self):
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
# StmtExpressionNode used to flatten expression in same cases of control flow.
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
class StmtExpressionNode(BytecodeAstNode):
  def __init__(self, statement_list_node: "StatementListNode", expr_node: "ExpressionNodeBase"):
    super().__init__()
    self.statement_list_node = statement_list_node
    self.expr_node = expr_node

  def flat_children(self):
    yield self.statement_list_node
    yield self.expr_node

class StatementNodeBase(BytecodeAstNode):
  def __init__(self):
    super().__init__()
    

class IfStatementNode(StatementNodeBase):
  def __init__(self, cond_node, cond_jump_node, true_stmt_list_node):
    self.cond_node = cond_node
    self.cond_jump_node = cond_jump_node
    self.true_stmt_list_node = true_stmt_list_node

  def flat_children(self):
    yield self.cond_node
    yield self.cond_jump_node
    yield self.true_stmt_list_node
      

class IfElseStatementNode(StatementNodeBase):
  def __init__(self, cond_node, cond_jump_node, true_stmt_list_node, jump_forward_node, false_stmt_list_node):
    self.cond_node = cond_node
    self.cond_jump_node = cond_jump_node
    self.true_stmt_list_node = true_stmt_list_node
    self.jump_forward_node = jump_forward_node
    self.false_stmt_list_node = false_stmt_list_node

  def flat_children(self):
    yield self.cond_node
    yield self.cond_jump_node
    yield self.true_stmt_list_node
    yield self.jump_forward_node
    yield self.false_stmt_list_node


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
    num_inputs_on_stack = self.children[-1].num_inputs_on_stack()
    num_outputs_on_stack = self.children[-1].num_outputs_on_stack()
    if (num_inputs_on_stack == num_outputs_on_stack
        and num_outputs_on_stack > 1
        and len(self.children) == 2):
      #e.g.: `a, b, c = d, e, f`  and `a, b, c, d = e, f, g, h`
      return max(num_outputs_on_stack, self.children[0].num_outputs_on_stack())
    else:
      return num_outputs_on_stack

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
    self._label_node = None

  @property
  def label_node(self):
    return self._label_node

  def set_label_node(self, label_node):
    self._label_node = label_node


class GenericJumpNode(JumpNodeBase):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

