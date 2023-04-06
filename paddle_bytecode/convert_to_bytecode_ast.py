from . import bytecode_ast
from . import instr_stack_util
import dis

def convert_to_bytecode_ast(instructions):
  return convert_to_statement_list_node(instructions)

def convert_to_statement_list_node(instructions):
  acc = 0
  sub_instructions = []
  children = []
  for instruction in instructions:
    acc = acc + instr_stack_util.stack_effect(instruction)
    sub_instructions.append(instruction)
    if acc > 0:
      pass
    elif acc == 0:
      children.append(convert_to_statement_node(sub_instructions))
      sub_instructions = []
    else:
      raise NotImplementedError("accumulated stack_effect should never be negative.")
  return bytecode_ast.StatementListNode(children)


def convert_to_statement_node(instructions):
  assert instr_stack_util.num_outputs_on_stack(instructions[-1]) == 0, instructions[-1]
  store_nodes = []
  while True:
    instructions, store_instructions = _get_prev_store_instructions(instructions)
    if len(store_instructions) == 0:
      break;
    elif len(store_instructions) == 1:
      store_nodes.append((convert_to_instruction_node(store_instructions[0]),))
    elif len(store_instructions) > 1:
      store_node = convert_to_instruction_node(store_instructions[-1])
      assert store_node.num_outputs_on_stack() == 0, store_instructions[-1]
      store_nodes.append((*convert_to_expression_node_tuple(store_instructions[:-1]), store_node))
    else:
      raise NotImplementedError("store instructions not supported: %s" % store_instructions[-1])
  return bytecode_ast.StatementNode(convert_to_expression_node(instructions), store_nodes[::-1])

def _get_prev_store_instructions(instructions):
  if not instr_stack_util.opcode2is_store_or_delete[instructions[-1].opcode]:
    return instructions, []
  acc_stack_effect = 0
  pos = len(instructions)
  while pos > 0:
    pos -= 1
    acc_stack_effect += instr_stack_util.stack_effect(instructions[pos])
    if acc_stack_effect == -1:
      return instructions[0:pos], instructions[pos:]
  raise NotImplementedError("dead code")

def convert_to_expression_node_tuple(instructions):
  # `symbolic_stack` contains instances of BytecodeAstNode.
  symbolic_stack = []
  for instruction in instructions:
    node = convert_to_instruction_node(instruction)
    num_inputs_on_stack = node.num_inputs_on_stack()
    if num_inputs_on_stack == 0:
      symbolic_stack.append(node)
    else:
      # expression_children is initialized in reversed order.
      expression_children = [node]
      while num_inputs_on_stack > 0:
        instruction_as_arg = symbolic_stack.pop()
        num_inputs_on_stack -= instruction_as_arg.num_outputs_on_stack()
        assert num_inputs_on_stack >= 0
        expression_children.append(instruction_as_arg)
      assert num_inputs_on_stack == 0
      expression_children.reverse()
      symbolic_stack.append(bytecode_ast.ExpressionNode(expression_children))
  return symbolic_stack

def convert_to_expression_node(instructions):
  symbolic_stack = convert_to_expression_node_tuple(instructions)
  assert len(symbolic_stack) == 1, symbolic_stack
  return symbolic_stack[0]

def convert_to_instruction_node(instruction):
  if hasattr(bytecode_ast, instruction.opname):
    cls = getattr(bytecode_ast, instruction.opname)
  else:
    cls = bytecode_ast.InstructionNode
  return cls(instruction)
