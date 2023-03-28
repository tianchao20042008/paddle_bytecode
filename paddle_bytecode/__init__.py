from .convert_to_bytecode_ast import convert_to_bytecode_ast

# NOTE used in repl.
# TODO delete them before release.
import dis
def acc_stack_effect(instructions):
  acc = 0
  for instruction in instructions:
    acc = acc + dis.stack_effect(instruction.opcode, instruction.arg)
    print(acc, instruction)
    
# NOTE used in repl.
# TODO delete them before release.
def test_convert():
  def foo(a):
    b = bar(1 + a ** 2)
    c.x, d = b + a, 30
    return bar(c.x)
  instructions = list(dis.get_instructions(foo))
  acc_stack_effect(instructions)
  from pprint import pprint
  pprint(convert_to_bytecode_ast(instructions).dump())
