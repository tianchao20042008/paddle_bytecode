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
  store_instr_pos = -1
  while instr_stack_util.num_outputs_on_stack(instructions[store_instr_pos]) != 0:
    store_instr_pos = store_instr_pos - 1
  expr_instructions = instructions[0:store_instr_pos]
  store_instructions = instructions[store_instr_pos:]
  return bytecode_ast.StatementNode(
    convert_to_expression_node(expr_instructions),
    [bytecode_ast.InstructionNode(instruction) for instruction in store_instructions]
  )

def convert_to_expression_node(instructions):
  # `symbolic_stack` contains instances of BytecodeAstNode.
  symbolic_stack = []
  for instruction in instructions:
    node = bytecode_ast.InstructionNode(instruction)
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
  assert len(symbolic_stack) == 1
  return symbolic_stack[0]
