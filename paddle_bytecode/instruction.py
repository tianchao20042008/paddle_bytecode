from typing import Union, Any
import dis

class Instruction:
  def __init__(self, opcode: int, opname: str, arg: int, argval, argrepr: Any, offset: int, starts_line: Union[int, None], is_jump_target: bool):
    self.opcode         = opcode
    self.opname         = opname
    self.arg            = arg
    self.argval         = argval
    self.argrepr        = argrepr
    self.offset         = offset
    self.starts_line    = starts_line
    self.is_jump_target = is_jump_target

  @staticmethod
  def clone_from(instruction: Union[dis.Instruction, Instruction]):
    return Instruction(
      opcode=instruction.opcode,
      opname=instruction.opname,
      arg=instruction.arg,
      argval=instruction.argval,
      argrepr=instruction.argrepr,
      offset=instruction.offset,
      starts_line=instruction.starts_line,
      is_jump_target=instruction.is_jump_target
    )

  @staticmethod
  def make(opname, arg, argval=None):
    return Instruction(
      opcode=dis.opmap[opname],
      opname=opname,
      arg=arg,
      argval=argval,
      argrepr=str(argval),
      offset=None,
      starts_line=None,
      is_jump_target=False
    )
