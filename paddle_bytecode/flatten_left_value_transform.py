from typing import Callable
from functools import reduce
from . import bytecode_ast
from .instruction import Instruction
import dis

class FlattenLeftValueTransform:
  def __init__(self, generate_new_local_varname: Callable[[], str]):
    self.generate_new_local_varname = generate_new_local_varname
    self.generated_ast_nodes = []

  def __call__(self, ast_node):
    ast_cls = type(ast_node)
    if not hasattr(self, ast_cls.__name__):
      assert len(ast_cls.__bases__) == 1
      ast_cls = ast_cls.__bases__[0]
    return getattr(self, ast_cls.__name__)(ast_node)

  def StatementListNode(self, ast_node):
    # use `that` instead of self in order to support nested statement list.
    that = type(self)(self.generate_new_local_varname)
    children = []
    for child in ast_node.children: 
      flattened = that(child)
      children.append(flattened)
      children = children + that.generated_ast_nodes
      that.generated_ast_nodes = []
    return type(ast_node)(children)

  def StoreNodeBase(self, ast_node):
    return type(ast_node)(
      ast_node.expr_node,
      list(self.replace_left_value_with_local_var(instrs) for instrs in ast_node.store_nodes)
    )

  def GenericExpressionNode(self, ast_node):
    return ast_node

  def replace_left_value_with_local_var(self, store_nodes):
    if len(store_nodes) == 1:
      assert isinstance(store_nodes[-1], bytecode_ast.InstructionNodeBase)
      return store_nodes
    local_varname = self.generate_new_local_varname()
    load_opname = "LOAD_FAST"
    load_instr = Instruction(
      opcode=dis.opmap[load_opname],
      opname=load_opname,
      arg=-1,
      argval=local_varname,
      argrepr=local_varname,
      offset=-1,
      starts_line=-1,
      is_jump_target=None,
    )
    self.generated_ast_nodes.append(
      bytecode_ast.GenericStoreNode(
        bytecode_ast.LOAD_FAST(load_instr),
        [tuple(map(self.replace_right_value_with_local_var, store_nodes))]
      )
    )
    store_opname = "STORE_FAST"
    store_instr = Instruction(
      opcode=dis.opmap[store_opname],
      opname=store_opname,
      arg=-1,
      argval=local_varname,
      argrepr=local_varname,
      offset=-1,
      starts_line=-1,
      is_jump_target=None,
    )
    return (bytecode_ast.STORE_FAST(store_instr),)

  def replace_right_value_with_local_var(self, ast_node):
    if not isinstance(ast_node, bytecode_ast.ExpressionNodeBase):
      return ast_node
    local_varname = self.generate_new_local_varname()
    store_opname = "STORE_FAST"
    store_instr = Instruction(
      opcode=dis.opmap[store_opname],
      opname=store_opname,
      arg=-1,
      argval=local_varname,
      argrepr=local_varname,
      offset=-1,
      starts_line=-1,
      is_jump_target=None,
    )
    self.generated_ast_nodes.append(
      bytecode_ast.GenericStoreNode(
        ast_node,
        [(bytecode_ast.STORE_FAST(store_instr),)]
      )
    )
    load_opname = "LOAD_FAST"
    load_instr = Instruction(
      opcode=dis.opmap[load_opname],
      opname=load_opname,
      arg=-1,
      argval=local_varname,
      argrepr=local_varname,
      offset=-1,
      starts_line=-1,
      is_jump_target=None,
    )
    return bytecode_ast.LOAD_FAST(load_instr)

  def InstructionNodeBase(self, ast_node):
    return ast_node
