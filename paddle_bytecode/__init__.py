from .convert_to_bytecode_ast import convert_to_bytecode_ast

# NOTE used in repl.
# TODO delete them before release.
import dis
def acc_stack_effect(instructions):
  acc = 0
  for instruction in instructions:
    acc = acc + dis.stack_effect(instruction.opcode, instruction.arg)
    print(acc, instruction)
    
