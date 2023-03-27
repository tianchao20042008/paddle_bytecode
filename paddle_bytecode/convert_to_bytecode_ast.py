from . import bytecode_ast
from . import instr_stack_util
import dis

def convert_to_bytecode_ast(instructions):
  instructions = list(instructions) # `instructions` may be a generator.
  print(dis.dis(code_object))

def convert_to_statement_list_node(instructions):
  acc = 0
  sub_instructions = []
  children = []
  for instruction in instructions:
    acc = acc + instr_stack_util.stack_effect(instruction)
    if acc > 0:
      sub_instructions.append(instruction)
    else:
      children.append(convert_to_expression_node(sub_instructions))
      sub_instructions = []


def convert_to_expression_node(instructions):
  virtual_stack = []
  for instruction in instructions:
    virtual_stack.append(bytecode_ast.InstructionNode(instruction))
    stack_effect = instr_stack_util.stack_effect(instruction)
    if stack_effect == 0:
      last = virtual_stack.pop()

def convert_to_instruction_node(instruction):
  TODO()
