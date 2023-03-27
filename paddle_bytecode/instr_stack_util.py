import dis
import sys

def stack_effect(instruction):
  return dis.stack_effect(instruction.opcode, instruction.arg)

def stack_num_inputs(instruction):
  return stack_num_outputs(instruction) - stack_effect(instruction)
  
# For all instructions Please keep that
#
#   stack_num_outputs(instruction) ==
#       stack_effect(instruction) + actual_number_stack_elements_consumed(instruction)
#
# e.g.
#   stack_effect(ROT_THREE) is 0, actual_number_stack_elements_consumed(ROT_THREE) is 3,
#   so we must define stack_num_outputs(ROT_THREE) as 3.
#  
def stack_num_outputs(instruction):
  return opcode2stack_num_outputs[instruction.opcode](instruction)


if sys.version_info[0:2] == (3, 8):
  opname2output_num_or_f = dict(
    POP_TOP=0,
    ROT_TWO=2,
    ROT_THREE=3,
    DUP_TOP=1,
    DUP_TOP_TWO=2,
    ROT_FOUR=4,
    NOP=0,
    UNARY_POSITIVE=1,
    UNARY_NEGATIVE=1,
    UNARY_NOT=1,
    UNARY_INVERT=1,
    BINARY_MATRIX_MULTIPLY=1,
    INPLACE_MATRIX_MULTIPLY=1,
    BINARY_POWER=1,
    BINARY_MULTIPLY=1,
    BINARY_MODULO=1,
    BINARY_ADD=1,
    BINARY_SUBTRACT=1,
    BINARY_SUBSCR=1,
    BINARY_FLOOR_DIVIDE=1,
    BINARY_TRUE_DIVIDE=1,
    INPLACE_FLOOR_DIVIDE=1,
    INPLACE_TRUE_DIVIDE=1,
    GET_AITER=1,
    GET_ANEXT=1,
#    BEFORE_ASYNC_WITH=?,
#    BEGIN_FINALLY=?,
#    END_ASYNC_FOR=?,
    INPLACE_ADD=1,
    INPLACE_SUBTRACT=1,
    INPLACE_MULTIPLY=1,
    INPLACE_MODULO=1,
    STORE_SUBSCR=1,
    DELETE_SUBSCR=0,
    BINARY_LSHIFT=1,
    BINARY_RSHIFT=1,
    BINARY_AND=1,
    BINARY_XOR=1,
    BINARY_OR=1,
    INPLACE_POWER=1,
    GET_ITER=1,
    GET_YIELD_FROM_ITER=1,
    PRINT_EXPR=0,
    LOAD_BUILD_CLASS=1,
    YIELD_FROM=0,
    GET_AWAITABLE=1,
    INPLACE_LSHIFT=1,
    INPLACE_RSHIFT=1,
    INPLACE_AND=1,
    INPLACE_XOR=1,
    INPLACE_OR=1,
#    WITH_CLEANUP_START=?,
#    WITH_CLEANUP_FINISH=?,
    RETURN_VALUE=0,
    IMPORT_STAR=0,
    SETUP_ANNOTATIONS=0,
    YIELD_VALUE=0,
#    POP_BLOCK=?,
#    END_FINALLY=?,
#    POP_EXCEPT=?,
    STORE_NAME=0,
    DELETE_NAME=0,
    UNPACK_SEQUENCE=lambda instr: instr.arg,
#    FOR_ITER=?,
    UNPACK_EX=lambda instr: instr.arg + 1,
    STORE_ATTR=0,
    DELETE_ATTR=0,
    STORE_GLOBAL=0,
    DELETE_GLOBAL=0,
    LOAD_CONST=1,
    LOAD_NAME=1,
    BUILD_TUPLE=1,
    BUILD_LIST=1,
    BUILD_SET=1,
    BUILD_MAP=1,
    LOAD_ATTR=1,
    COMPARE_OP=1,
    IMPORT_NAME=0,
    IMPORT_FROM=1,
#    JUMP_FORWARD=?,
#    JUMP_IF_FALSE_OR_POP=?,
#    JUMP_IF_TRUE_OR_POP=?,
#    JUMP_ABSOLUTE=?,
#    POP_JUMP_IF_FALSE=?,
#    POP_JUMP_IF_TRUE=?,
    LOAD_GLOBAL=1,
#    SETUP_FINALLY=?,
    LOAD_FAST=1,
    STORE_FAST=0,
    DELETE_FAST=0,
    RAISE_VARARGS=0,
    CALL_FUNCTION=1,
    MAKE_FUNCTION=1,
    BUILD_SLICE=1,
    LOAD_CLOSURE=1,
    LOAD_DEREF=1,
    STORE_DEREF=0,
    DELETE_DEREF=0,
    CALL_FUNCTION_KW=1,
    CALL_FUNCTION_EX=1,
#    SETUP_WITH=?,
    LIST_APPEND=0,
    SET_ADD=0,
    MAP_ADD=0,
    LOAD_CLASSDEREF=1,
#    EXTENDED_ARG=?,
    BUILD_LIST_UNPACK=1,
    BUILD_MAP_UNPACK=1,
    BUILD_MAP_UNPACK_WITH_CALL=1,
    BUILD_TUPLE_UNPACK=1,
    BUILD_SET_UNPACK=1,
#    SETUP_ASYNC_WITH=?,
    FORMAT_VALUE=1,
    BUILD_CONST_KEY_MAP=1,
    BUILD_STRING=1,
    BUILD_TUPLE_UNPACK_WITH_CALL=1,
    LOAD_METHOD=1,
    CALL_METHOD=1,
#    CALL_FINALLY=?,
#    POP_FINALLY=?,
  )
else:
  raise NotImplementedError("paddle_bytecode module is not supported in version" % sys.version_info)

def generate_opcode2stack_num_outputs():
  def UnimplementedFunction(instruction):
    raise NotImplementedError("static_num_outputs is not implemented for " % instruction)
  def Const(number):
    return lambda _: number
  max_op_code = 256
  opcode2stack_num_outputs = [UnimplementedFunction] * max_op_code
  for op_name, num_or_f in opname2output_num_or_f.items():
    f = num_or_f if callable(num_or_f) else Const(num_or_f)
    opcode2stack_num_outputs[dis.opmap[op_name]] = f
  return opcode2stack_num_outputs

opcode2stack_num_outputs = generate_opcode2stack_num_outputs()
