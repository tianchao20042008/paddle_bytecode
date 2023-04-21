import unittest
import dis
from paddle_bytecode.mark_control_instruction_transform import MarkControlInstructionTransform

class TestMarkControlInstruction(unittest.TestCase):
  def test_naive(self):
    def foo():
      return 0
    instructions = list(dis.get_instructions(foo))
    mark_ctrl = MarkControlInstructionTransform(instructions)
    instruction_to_is_ctrl = mark_ctrl()
    self.assertFalse(instruction_to_is_ctrl[instructions[0]]) # LOAD_CONST
    self.assertTrue(instruction_to_is_ctrl[instructions[1]]) # RETURN_VALUE

if __name__ == '__main__':
  unittest.main()
