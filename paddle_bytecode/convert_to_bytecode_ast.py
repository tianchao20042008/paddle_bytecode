from typing import Dict, List
from . import bytecode_ast
from . import instr_stack_util
from dataclasses import dataclass
import dis

class ConvertContext:
  def __init__(self,
               offset2label_node: Dict[int, bytecode_ast.LabelNode],
               instruction_nodes: List[bytecode_ast.InstructionNodeBase]):
    self.offset2label_node = offset2label_node
    self.instruction_nodes = instruction_nodes
    self.pos = len(instruction_nodes) - 1

  def top_instruction_node(self, offset=0) -> bytecode_ast.InstructionNodeBase:
    pos = self.pos - offset
    if pos < 0:
      return None
    else:
      return self.instruction_nodes[pos]

  def pop_instruction_node(self):
    self.pos = self.pos - 1

  def label_node4offset(self, offset: int) -> bytecode_ast.LabelNode:
    return self.offset2label_node[offset]


def convert_to_bytecode_ast(instructions):
  offset2label_node: Dict[int, bytecode_ast.labelnode] = {}
  def convert_instruction(instruction):
    return convert_to_label_node_and_instruction_node(instruction, offset2label_node)
  instruction_nodes = [n for i in instructions for n in convert_instruction(i)]
  convert_ctx = ConvertContext(offset2label_node, instruction_nodes)
  return convert_to_program(convert_ctx)


def convert_to_program(convert_ctx: ConvertContext) -> bytecode_ast.Program:
  reversed_children = []
  while convert_ctx.top_instruction_node() is not None:
    current_node = convert_ctx.top_instruction_node()
    if isinstance(current_node, bytecode_ast.JumpNodeBase):
      # jump
      convert_ctx.pop_instruction_node()
      offset = current_node.instruction.argval
      current_node.set_label_node(convert_ctx.label_node4offset(offset))
      reversed_children.append(current_node)
    elif isinstance(current_node, bytecode_ast.LabelNode):
      # label
      convert_ctx.pop_instruction_node()
      reversed_children.append(current_node)
    elif instr_stack_util.opcode2is_store_or_delete[current_node.opcode]:
      # statement
      statement_list_node = convert_to_statement_list_node(convert_ctx)
      reversed_children.append(statement_list_node)
    else:
      # expression
      statement_list_node = bytecode_ast.StatementListNode([])
      expression_node = convert_to_expression_node(convert_ctx)
      stmt_expr_node = bytecode_ast.StmtExpressionNode(statement_list_node, expression_node)
      reversed_children.append(stmt_expr_node)
  assert convert_ctx.top_instruction_node() is None
  children = reversed_children[::-1]
  return bytecode_ast.Program(children)


def convert_to_statement_list_node(convert_ctx: ConvertContext):
  reversed_children = []
  while convert_ctx.top_instruction_node() is not None:
    current_node = convert_ctx.top_instruction_node()
    if isinstance(current_node, bytecode_ast.LabelNode):
      break
    if instr_stack_util.opcode2is_store_or_delete[current_node.opcode]:
      statement_node = convert_to_statement_node(convert_ctx)
      reversed_children.append(statement_node)
    else:
      break
  children = reversed_children[::-1]
  return bytecode_ast.StatementListNode(children)


def convert_to_statement_node(convert_ctx: ConvertContext):
  return StoreNodeCreator()(convert_ctx)

class StoreNodeCreator:
  def __call__(self, convert_ctx: ConvertContext):
    opname = convert_ctx.top_instruction_node().opname
    reversed_store_node_tuples = []
    while True:
      current_node = convert_ctx.top_instruction_node()
      if instr_stack_util.opcode2is_store_or_delete[current_node.opcode]:
        store_node_tuple = self.convert_to_store_node_tuple(convert_ctx)
        reversed_store_node_tuples.append(store_node_tuple)
      else:
        break
    store_node_tuples = reversed_store_node_tuples[::-1]
    expr_node = convert_to_unpack_expression_node(
      convert_ctx, num_outputs_required_on_stack=len(store_node_tuples)
    )
    return self.create_store_node(opname, expr_node, store_node_tuples)

  def convert_to_store_node_tuple(self, convert_ctx: ConvertContext):
    store_instruction = convert_ctx.top_instruction_node()
    if store_instruction.num_inputs_on_stack() == 1:
      convert_ctx.pop_instruction_node()
      return (store_instruction,)
    elif store_instruction.num_inputs_on_stack() == 2:
      convert_ctx.pop_instruction_node()
      expr_node0 = convert_to_expression_node(convert_ctx)
      return (expr_node0, store_instruction)
    elif store_instruction.num_inputs_on_stack() == 3:
      convert_ctx.pop_instruction_node()
      expr_node1 = convert_to_expression_node(convert_ctx)
      expr_node0 = convert_to_expression_node(convert_ctx)
      return (expr_node0, expr_node1, store_instruction)
    else:
      raise NotImplementedError()
    

  def create_store_node(self, opname, expr_node, store_nodes):
    method_name = opname
    create = getattr(self, method_name) if hasattr(self, method_name) else self.generic_create
    return create(expr_node, store_nodes)

  def generic_create(self, expr_node, store_nodes):
    return bytecode_ast.GenericStoreNode(expr_node, store_nodes)

  def RETURN_VALUE(self, expr_node, store_nodes):
    return bytecode_ast.ReturnValueNode(expr_node, store_nodes)

def convert_to_unpack_expression_node(convert_ctx: ConvertContext, num_outputs_required_on_stack: int):
  expr_node_list = convert_to_expression_node_list(convert_ctx, num_outputs_required_on_stack)
  assert len(expr_node_list) == 1
  unpack_expr_node = expr_node_list[0]
  assert unpack_expr_node.num_outputs_on_stack() == num_outputs_required_on_stack
  return unpack_expr_node

def convert_to_expression_node(convert_ctx: ConvertContext):
  current_node = convert_ctx.top_instruction_node()
  ret = None
  if isinstance(current_node, bytecode_ast.LabelNode):
    # e.g.: `a if b else c`
    return convert_to_if_expression_node(convert_ctx)
  elif current_node.num_inputs_on_stack() == 0:
    convert_ctx.pop_instruction_node()
    return current_node
  else:
    convert_ctx.pop_instruction_node()
    arg_node_list = convert_to_expression_node_list(convert_ctx, current_node.num_inputs_on_stack())
    expr_node = bytecode_ast.GenericExpressionNode([*arg_node_list, current_node])
    return ExprCreator()(expr_node)


def convert_to_if_expression_node(convert_ctx: ConvertContext):
  TODO


def convert_to_expression_node_list(convert_ctx: ConvertContext, num_outputs_required_on_stack: int):
  reversed_reduced = []
  while num_outputs_required_on_stack > 0:
    ast_node = convert_to_expression_node(convert_ctx)
    reversed_reduced.append(ast_node)
    num_outputs_required_on_stack -= ast_node.num_outputs_on_stack()
  assert num_outputs_required_on_stack == 0
  return reversed_reduced[::-1]


class ExprCreator:
  def __call__(self, expr_node):
    if not isinstance(expr_node, bytecode_ast.ExpressionNodeBase):
      return expr_node
    last_node = expr_node.children[-1]
    if isinstance(last_node, bytecode_ast.InstructionNodeBase):
      opname = last_node.instruction.opname
      if hasattr(self, opname):
        return getattr(self, opname)(expr_node)
      else:
        return expr_node
    else:
      return expr_node

  def MAKE_FUNCTION(self, expr_node):
    make_function_node = bytecode_ast.MakeFunctionExprNode(expr_node.children)
    code_obj = expr_node.children[0].instruction.argval
    make_function_node.function_body = convert_to_bytecode_ast(list(dis.get_instructions(code_obj)))
    make_function_node.co_argcount = code_obj.co_argcount
    return make_function_node


def convert_to_label_node_and_instruction_node(
    instruction, mut_offset2label_node: Dict[int, bytecode_ast.LabelNode]
  ):
  if instruction.is_jump_target:
    label_node = bytecode_ast.LabelNode()
    assert instruction.offset not in mut_offset2label_node
    mut_offset2label_node[instruction.offset] = label_node
    yield label_node
  yield convert_to_instruction_node(instruction)


def convert_to_instruction_node(instruction):
  if hasattr(bytecode_ast, instruction.opname):
    cls = getattr(bytecode_ast, instruction.opname)
  elif instr_stack_util.is_jump_instruction(instruction):
    cls = bytecode_ast.GenericJumpNode
  else:
    cls = bytecode_ast.GenericInstructionNode
  return cls(instruction)
