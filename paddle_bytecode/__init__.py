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
  node = convert_to_bytecode_ast(instructions)
  from .bytecode_attr import BytecodeAttr
  get_attr = BytecodeAttr.make_getter()
  from .dump_transform import DumpTransform
  pprint(DumpTransform(get_attr).dump(node))

# NOTE used in repl.
# TODO delete them before release.
def test_infer_static_convertible():
  def foo(a):
    b = bar(1 + a ** 2)
    print(b)
    c.x, d = b + a, 30
    return bar(c.x)
  instructions = list(dis.get_instructions(foo))
  from pprint import pprint
  node = convert_to_bytecode_ast(instructions)
  from .bytecode_attr import BytecodeAttr
  get_attr = BytecodeAttr.make_getter()
  from .dump_transform import DumpTransform
  from .infer_static_convertible_transform import InferIsProcedureStaticConvertibleTransform
  def is_procedure_static_convertible(ast_node):
    i = ast_node.instruction
    return not (i.opname == "LOAD_GLOBAL" and i.argval == "print")
  InferIsProcedureStaticConvertibleTransform(is_procedure_static_convertible, get_attr).infer(node)
  from .infer_static_convertible_transform import InferIsResultStaticConvertibleTransform
  def is_result_static_convertible(ast_node):
    return (True,) * ast_node.num_outputs_on_stack()
  InferIsResultStaticConvertibleTransform(is_result_static_convertible, get_attr).infer(node)
  pprint(DumpTransform(get_attr).dump(node))
