from typing import Dict, List
import paddle_bytecode.instr_stack_util as instr_stack_util
import paddle_bytecode.graph_util as graph_util

class ValueSymbol:
  
  def for_ctrl(self):
    raise NotImplemented()


class CtrlSymbol(ValueSymbol):

  def for_ctrl(self):
    return True


g_ctrl_symbol = CtrlSymbol()

class DataSymbol(ValueSymbol):

  def for_ctrl(self):
    return False

g_data_symbol = DataSymbol()

class MarkControlInstructionTransform:

  def __init__(self, instructions: List["Instruction"]):
    self.instructions = list(instructions)
    self.offset_to_instruction_index = {
      instr.offset:i for i, instr in enumerate(self.instructions)
    }

  def __call__(self) -> Dict["Instruction", bool]:
    initial_offset = self.instructions[0].offset
    initial_value_symbol_stack = []
    # `offset2value_symbol_stack[offset]` is the symbol stack before running instruction at `offset`.
    offset2value_symbol_stack: Dict[int, List[ValueSymbol]] = {
      initial_offset:initial_value_symbol_stack
    }
    instruction2is_ctrl: Dict["Instruction", bool] = {}
    for instr in graph_util.bfs_visited_nodes([self.instructions[0]], self.get_next_instructions):
      instruction2is_ctrl[instr] = self.is_ctrl_instruction(
        instruction=instr,
        stack=offset2value_symbol_stack[instr.offset]
      )
      self.update_offset2value_symbol_stack(
        instruction=instr,
        for_ctrl=instruction2is_ctrl[instr],
        offset2value_symbol_stack=offset2value_symbol_stack
      )
    return instruction2is_ctrl

  def outputs_used_for_ctrl(self, stack, instruction, jump):
    num_inputs_on_stack = instr_stack_util.num_inputs_on_stack(instruction, jump)
    inputs_used_for_ctrl = tuple(
      symbol.for_ctrl() for symbol in stack[len(stack)-num_inputs_on_stack:]
    )
    return instr_stack_util.outputs_used_for_ctrl(inputs_used_for_ctrl, instruction, jump)

  def is_ctrl_instruction(self, instruction, stack):
    num_inputs_on_stack = instr_stack_util.num_inputs_on_stack(instruction)
    for symbol in stack[len(stack)-num_inputs_on_stack:]:
      if symbol.for_ctrl():
        return True
    if instr_stack_util.is_jump_instruction(instruction):
      return True
    elif instruction not in instr_stack_util.opnames_with_static_convertible_output:
      return True
    else:
      return False

  def update_offset2value_symbol_stack(self, instruction, for_ctrl, offset2value_symbol_stack):
    cur_value_symbol_stack = offset2value_symbol_stack[instruction.offset]
    for next_instruction, jump in self.get_next_instruction_and_jump_flags(instruction):
      next_value_symbol_stack = cur_value_symbol_stack[:] # immutable access `cur_value_symbol_stack`
      self.update_value_symbol_stack(next_value_symbol_stack, instruction, jump)
      offset = next_instruction.offset
      if offset in offset2value_symbol_stack:
        assert offset2value_symbol_stack[offset] == next_value_symbol_stack
      else:
        offset2value_symbol_stack[offset] = next_value_symbol_stack

  def update_value_symbol_stack(self, stack, instruction, jump):
    num_inputs_on_stack = instr_stack_util.num_inputs_on_stack(instruction, jump)
    for _ in range(num_inputs_on_stack):
      stack.pop()
    for for_ctrl in self.outputs_used_for_ctrl(stack, instruction, jump):
      stack.append(g_ctrl_symbol if for_ctrl else g_data_symbol)

  def get_next_instructions(self, instruction):
    for next_instruction, _ in self.get_next_instruction_and_jump_flags(instruction):
      yield next_instruction

  def get_next_instruction_and_jump_flags(self, instruction):
    return instr_stack_util.get_next_instruction_and_jump_flags(
      instruction,
      self.get_instruction_index_by_offset,
      self.get_instruction_by_index
    )

  def get_instruction_index_by_offset(self, offset):
    if offset not in self.offset_to_instruction_index:
      return len(self.instructions)
    return self.offset_to_instruction_index[offset] 

  def get_instruction_by_index(self, index):
    if index >= len(self.instructions):
      return None
    return self.instructions[index]
