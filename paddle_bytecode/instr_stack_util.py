from typing import Callable, Optional
import dis
import sys

def get_next_instruction_and_jump_flags(
    instruction: "Instruction",
    get_instruction_index_by_offset: Callable[[int], int],
    get_instruction_by_index: Callable[[int], Optional['Instruction']]
  ):
    def next_instruction_if_jump_true():
      next_offset = instruction.argval
      next_index = get_instruction_index_by_offset(next_offset)
      next_instruction = get_instruction_by_index(next_offset)
      assert next_instruction is not None
      return next_instruction
    def next_instruction_if_jump_false():
      next_index = get_instruction_index_by_offset(instruction.offset) + 1
      next_instruction = get_instruction_by_index(next_index)
      return next_instruction
    if not is_jump_instruction(instruction):
      next_instruction = next_instruction_if_jump_false()
      if next_instruction is not None:
        yield (next_instruction, None)
    elif instruction.opname in {'JUMP_FORWARD', 'JUMP_ABSOLUTE'}:
      yield (next_instruction_if_jump_true(), True)
    else:
      yield (next_instruction_if_jump_true(), True)
      next_instruction = next_instruction_if_jump_false()
      if next_instruction is not None:
        yield (next_instruction, False)

def outputs_used_for_ctrl(inputs_used_for_ctrl, instruction, jump):
  assert len(inputs_used_for_ctrl) == num_inputs_on_stack(instruction, jump)
  if instruction.opname == 'ROT_TWO':
    return inputs_used_for_ctrl[-1], inputs_used_for_ctrl[-2]
  elif instruction.opname == 'ROT_THREE':
    return inputs_used_for_ctrl[-1], inputs_used_for_ctrl[-3], inputs_used_for_ctrl[-2]
  elif instruction.opname == 'ROT_FOUR':
    return (
      inputs_used_for_ctrl[-1],
      inputs_used_for_ctrl[-4],
      inputs_used_for_ctrl[-3],
      inputs_used_for_ctrl[-2],
    )
  if instruction.opname == 'DUP_TOP':
    return (inputs_used_for_ctrl[0], inputs_used_for_ctrl[0])
  if instruction.opname == 'DUP_TOP_TWO':
    return (
      inputs_used_for_ctrl[-2],
      inputs_used_for_ctrl[-1],
      inputs_used_for_ctrl[-2],
      inputs_used_for_ctrl[-1],
    )
  else:
    for_ctrl = instruction.opname not in opnames_with_static_convertible_output
    return (for_ctrl,) * num_outputs_on_stack(instruction, jump)
    
if sys.version_info[0:2] == (3, 8):
  opnames_with_static_convertible_output = {
    'POP_TOP',
    'ROT_TWO',
    'ROT_THREE',
    'DUP_TOP',
    'DUP_TOP_TWO',
    'ROT_FOUR',
    'NOP',
    'UNARY_POSITIVE',
    'UNARY_NEGATIVE',
    'UNARY_NOT',
    'UNARY_INVERT',
    'BINARY_MATRIX_MULTIPLY',
    'INPLACE_MATRIX_MULTIPLY',
    'BINARY_POWER',
    'BINARY_MULTIPLY',
    'BINARY_MODULO',
    'BINARY_ADD',
    'BINARY_SUBTRACT',
    'BINARY_SUBSCR',
    'BINARY_FLOOR_DIVIDE',
    'BINARY_TRUE_DIVIDE',
    'INPLACE_FLOOR_DIVIDE',
    'INPLACE_TRUE_DIVIDE',
   #'GET_AITER',
    'GET_ANEXT',
   #'BEFORE_ASYNC_WITH',
   #'BEGIN_FINALLY',
   #'END_ASYNC_FOR',
    'INPLACE_ADD',
    'INPLACE_SUBTRACT',
    'INPLACE_MULTIPLY',
    'INPLACE_MODULO',
    'STORE_SUBSCR',
    'DELETE_SUBSCR',
    'BINARY_LSHIFT',
    'BINARY_RSHIFT',
    'BINARY_AND',
    'BINARY_XOR',
    'BINARY_OR',
    'INPLACE_POWER',
   #'GET_ITER',
   #'GET_YIELD_FROM_ITER',
   #'PRINT_EXPR',
   #'LOAD_BUILD_CLASS',
   #'YIELD_FROM',
   #'GET_AWAITABLE',
    'INPLACE_LSHIFT',
    'INPLACE_RSHIFT',
    'INPLACE_AND',
    'INPLACE_XOR',
    'INPLACE_OR',
   #'WITH_CLEANUP_START',
   #'WITH_CLEANUP_FINISH',
   #'RETURN_VALUE',
   #'IMPORT_STAR',
   #'SETUP_ANNOTATIONS',
   #'YIELD_VALUE',
   #'POP_BLOCK',
   #'END_FINALLY',
   #'POP_EXCEPT',
    'STORE_NAME',
    'DELETE_NAME',
    'UNPACK_SEQUENCE',
    'FOR_ITER',
    'UNPACK_EX',
    'STORE_ATTR',
    'DELETE_ATTR',
    'STORE_GLOBAL',
    'DELETE_GLOBAL',
    'LOAD_CONST',
    'LOAD_NAME',
    'BUILD_TUPLE',
    'BUILD_LIST',
    'BUILD_SET',
    'BUILD_MAP',
    'LOAD_ATTR',
    'COMPARE_OP',
   #'IMPORT_NAME',
   #'IMPORT_FROM',
   #'JUMP_FORWARD',
   #'JUMP_IF_FALSE_OR_POP',
   #'JUMP_IF_TRUE_OR_POP',
   #'JUMP_ABSOLUTE',
   #'POP_JUMP_IF_FALSE',
   #'POP_JUMP_IF_TRUE',
    'LOAD_GLOBAL',
   #'SETUP_FINALLY',
    'LOAD_FAST',
    'STORE_FAST',
    'DELETE_FAST',
   #'RAISE_VARARGS',
    'CALL_FUNCTION',
    'MAKE_FUNCTION',
    'BUILD_SLICE',
    'LOAD_CLOSURE',
    'LOAD_DEREF',
    'STORE_DEREF',
    'DELETE_DEREF',
    'CALL_FUNCTION_KW',
    'CALL_FUNCTION_EX',
   #'SETUP_WITH',
    'LIST_APPEND',
    'SET_ADD',
    'MAP_ADD',
    'LOAD_CLASSDEREF',
    'EXTENDED_ARG',
    'BUILD_LIST_UNPACK',
    'BUILD_MAP_UNPACK',
    'BUILD_MAP_UNPACK_WITH_CALL',
    'BUILD_TUPLE_UNPACK',
    'BUILD_SET_UNPACK',
   #'SETUP_ASYNC_WITH',
    'FORMAT_VALUE',
    'BUILD_CONST_KEY_MAP',
    'BUILD_STRING',
    'BUILD_TUPLE_UNPACK_WITH_CALL',
    'LOAD_METHOD',
    'CALL_METHOD',
   #'CALL_FINALLY',
   #'POP_FINALLY',
  }
else:
  raise NotImplementedError("paddle_bytecode module is not supported in version %s" % sys.version_info)

def is_jump_instruction(instruction):
  return opcode2hasjrel[instruction.opcode] or opcode2hasjabs[instruction.opcode]

def stack_effect(instruction, jump=None):
  return dis.stack_effect(instruction.opcode, instruction.arg, jump=jump)

def num_inputs_on_stack(instruction, jump=None):
  return num_outputs_on_stack(instruction, jump) - stack_effect(instruction, jump)
  
# For all instructions Please keep that
#
#   num_outputs_on_stack(instruction) ==
#       stack_effect(instruction) + actual_number_stack_elements_consumed(instruction)
#
# e.g.
#   stack_effect(ROT_THREE) is 0, actual_number_stack_elements_consumed(ROT_THREE) is 3,
#   so we must define num_outputs_on_stack(ROT_THREE) as 3.
#  
def num_outputs_on_stack(instruction, jump=None):
  return opcode2num_outputs_on_stack[instruction.opcode](instruction, jump)


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
    BEFORE_ASYNC_WITH=2,
    BEGIN_FINALLY=6,
    END_ASYNC_FOR=0,
    INPLACE_ADD=1,
    INPLACE_SUBTRACT=1,
    INPLACE_MULTIPLY=1,
    INPLACE_MODULO=1,
    STORE_SUBSCR=0,
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
    WITH_CLEANUP_START=8,
    WITH_CLEANUP_FINISH=1,
    RETURN_VALUE=0,
    IMPORT_STAR=0,
    SETUP_ANNOTATIONS=0,
    YIELD_VALUE=0,
    POP_BLOCK=0,
    END_FINALLY=0,
    POP_EXCEPT=0,
    STORE_NAME=0,
    DELETE_NAME=0,
    UNPACK_SEQUENCE=lambda instr, jump=None: instr.arg,
    FOR_ITER=1,
    UNPACK_EX=lambda instr, jump=None: instr.arg + 1,
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
    JUMP_FORWARD=0,
    JUMP_IF_FALSE_OR_POP=lambda arg, jump: 1 if jump else 0,
    JUMP_IF_TRUE_OR_POP=lambda arg, jump: 1 if jump else 0,
    JUMP_ABSOLUTE=0,
    POP_JUMP_IF_FALSE=0,
    POP_JUMP_IF_TRUE=0,
    LOAD_GLOBAL=1,
    SETUP_FINALLY=lambda arg, jump: 6 if jump else 0,
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
    SETUP_WITH=lambda arg, jump: 7 if jump else 2,
    LIST_APPEND=0,
    SET_ADD=0,
    MAP_ADD=0,
    LOAD_CLASSDEREF=1,
    EXTENDED_ARG=0,
    BUILD_LIST_UNPACK=1,
    BUILD_MAP_UNPACK=1,
    BUILD_MAP_UNPACK_WITH_CALL=1,
    BUILD_TUPLE_UNPACK=1,
    BUILD_SET_UNPACK=1,
    SETUP_ASYNC_WITH=lambda arg, jump: 7 if jump else 2,
    FORMAT_VALUE=1,
    BUILD_CONST_KEY_MAP=1,
    BUILD_STRING=1,
    BUILD_TUPLE_UNPACK_WITH_CALL=1,
    LOAD_METHOD=1,
    CALL_METHOD=1,
    CALL_FINALLY=lambda arg, jump: 1 if jump else 0,
    POP_FINALLY=0,
  )
  opname2is_store_or_delete = dict(
    POP_TOP=True, # POP_TOP is regardded as delete instruction.
    ROT_TWO=False,
    ROT_THREE=False,
    DUP_TOP=False,
    DUP_TOP_TWO=False,
    ROT_FOUR=False,
    NOP=False,
    UNARY_POSITIVE=False,
    UNARY_NEGATIVE=False,
    UNARY_NOT=False,
    UNARY_INVERT=False,
    BINARY_MATRIX_MULTIPLY=False,
    INPLACE_MATRIX_MULTIPLY=False,
    BINARY_POWER=False,
    BINARY_MULTIPLY=False,
    BINARY_MODULO=False,
    BINARY_ADD=False,
    BINARY_SUBTRACT=False,
    BINARY_SUBSCR=False,
    BINARY_FLOOR_DIVIDE=False,
    BINARY_TRUE_DIVIDE=False,
    INPLACE_FLOOR_DIVIDE=False,
    INPLACE_TRUE_DIVIDE=False,
    GET_AITER=False,
    GET_ANEXT=False,
    BEFORE_ASYNC_WITH=False,
    BEGIN_FINALLY=False,
    END_ASYNC_FOR=False,
    INPLACE_ADD=False,
    INPLACE_SUBTRACT=False,
    INPLACE_MULTIPLY=False,
    INPLACE_MODULO=False,
    STORE_SUBSCR=True,
    DELETE_SUBSCR=True,
    BINARY_LSHIFT=False,
    BINARY_RSHIFT=False,
    BINARY_AND=False,
    BINARY_XOR=False,
    BINARY_OR=False,
    INPLACE_POWER=False,
    GET_ITER=False,
    GET_YIELD_FROM_ITER=False,
    PRINT_EXPR=False,
    LOAD_BUILD_CLASS=False,
    YIELD_FROM=False,
    GET_AWAITABLE=False,
    INPLACE_LSHIFT=False,
    INPLACE_RSHIFT=False,
    INPLACE_AND=False,
    INPLACE_XOR=False,
    INPLACE_OR=False,
    WITH_CLEANUP_START=False,
    WITH_CLEANUP_FINISH=False,
    RETURN_VALUE=True,
    IMPORT_STAR=False,
    SETUP_ANNOTATIONS=False,
    YIELD_VALUE=True,
    POP_BLOCK=False,
    END_FINALLY=False,
    POP_EXCEPT=False,
    STORE_NAME=True,
    DELETE_NAME=True,
    UNPACK_SEQUENCE=False,
    FOR_ITER=False,
    UNPACK_EX=False,
    STORE_ATTR=True,
    DELETE_ATTR=True,
    STORE_GLOBAL=True,
    DELETE_GLOBAL=True,
    LOAD_CONST=False,
    LOAD_NAME=False,
    BUILD_TUPLE=False,
    BUILD_LIST=False,
    BUILD_SET=False,
    BUILD_MAP=False,
    LOAD_ATTR=False,
    COMPARE_OP=False,
    IMPORT_NAME=False,
    IMPORT_FROM=False,
    JUMP_FORWARD=False,
    JUMP_IF_FALSE_OR_POP=False,
    JUMP_IF_TRUE_OR_POP=False,
    JUMP_ABSOLUTE=False,
    POP_JUMP_IF_FALSE=False,
    POP_JUMP_IF_TRUE=False,
    LOAD_GLOBAL=False,
    SETUP_FINALLY=False,
    LOAD_FAST=False,
    STORE_FAST=True,
    DELETE_FAST=True,
    RAISE_VARARGS=False,
    CALL_FUNCTION=False,
    MAKE_FUNCTION=False,
    BUILD_SLICE=False,
    LOAD_CLOSURE=False,
    LOAD_DEREF=False,
    STORE_DEREF=True,
    DELETE_DEREF=True,
    CALL_FUNCTION_KW=False,
    CALL_FUNCTION_EX=False,
    SETUP_WITH=False,
    LIST_APPEND=False,
    SET_ADD=False,
    MAP_ADD=False,
    LOAD_CLASSDEREF=False,
    EXTENDED_ARG=False,
    BUILD_LIST_UNPACK=False,
    BUILD_MAP_UNPACK=False,
    BUILD_MAP_UNPACK_WITH_CALL=False,
    BUILD_TUPLE_UNPACK=False,
    BUILD_SET_UNPACK=False,
    SETUP_ASYNC_WITH=False,
    FORMAT_VALUE=False,
    BUILD_CONST_KEY_MAP=False,
    BUILD_STRING=False,
    BUILD_TUPLE_UNPACK_WITH_CALL=False,
    LOAD_METHOD=False,
    CALL_METHOD=False,
    CALL_FINALLY=False,
    POP_FINALLY=False,
  )
else:
  raise NotImplementedError("paddle_bytecode module is not supported in version %s" % sys.version_info)

def generate_opcode2num_outputs_on_stack():
  def UnimplementedFunction(opcode):
    def f(instruction, jump=None):
      raise NotImplementedError("static_num_outputs is not implemented for opname: %s" % dis.opname[opcode])
    return f
  def Const(number):
    return lambda _, jump=None: number
  opcode_size = 256
  opcode2num_outputs_on_stack = [UnimplementedFunction(i) for i in range(opcode_size)]
  for opname, num_or_f in opname2output_num_or_f.items():
    f = num_or_f if callable(num_or_f) else Const(num_or_f)
    opcode2num_outputs_on_stack[dis.opmap[opname]] = f
  return opcode2num_outputs_on_stack

opcode2num_outputs_on_stack = generate_opcode2num_outputs_on_stack()

def generate_opcode2is_store_or_delete():
  opcode_size = 256
  opcode2is_sotre_or_delete = [False] * opcode_size
  for opname, is_sotre_or_delete in opname2is_store_or_delete.items():
    opcode2is_sotre_or_delete[dis.opmap[opname]] = is_sotre_or_delete
  return opcode2is_sotre_or_delete

opcode2is_store_or_delete = generate_opcode2is_store_or_delete()

def generate_opcode2hasjrel():
  opcode_size = 256
  opcode2hasjrel = [False] * opcode_size
  for opcode in dis.hasjrel:
    opcode2hasjrel[opcode] = True
  return opcode2hasjrel

opcode2hasjrel = generate_opcode2hasjrel()

def generate_opcode2hasjabs():
  opcode_size = 256
  opcode2hasjabs = [False] * opcode_size
  for opcode in dis.hasjabs:
    opcode2hasjabs[opcode] = True
  return opcode2hasjabs

opcode2hasjabs = generate_opcode2hasjabs()
