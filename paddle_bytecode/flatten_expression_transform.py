from typing import Callable
from functools import reduce
from . import bytecode_ast
from .instruction import Instruction
import dis

class FlattenExpressionTransform:
  def __init__(self,
              generate_new_local_varname: Callable[[], str],
              attr: Callable[["BytecodeAstNode"], "BytecodeAttr"]):
    self.generate_new_local_varname = generate_new_local_varname
    self.attr = attr
    self.generated_ast_nodes = []

  def flatten(self, ast_node):
    ast_cls = type(ast_node)
    if not hasattr(self, ast_cls.__name__):
      assert len(ast_cls.__bases__) == 1
      ast_cls = ast_cls.__bases__[0]
    return getattr(self, ast_cls.__name__)(ast_node)

  def StatementListNode(self, ast_node):
    # use `that` instead of self in order to support nested statement list.
    that = type(self)(self.generate_new_local_varname, self.attr)
    children = []
    for child in ast_node.children: 
      flattened = that.flatten(child)
      children = children + that.generated_ast_nodes
      children.append(flattened)
      that.generated_ast_nodes = []
    return type(ast_node)(children)

  def StatementNode(self, ast_node):
    expr_in_store_nodes = reduce(
      lambda acc, nodes:
        acc and reduce(lambda a, x: a and isinstance(x, bytecode_ast.ExpressionNodeBase), nodes, True),
      ast_node.store_nodes,
      True,
    )
    get_or_replace = self.generate_local_var_for_expr if expr_in_store_nodes else lambda x:x
    return type(ast_node)(
      get_or_replace(self.flatten(ast_node.expr_node)),
      list([
        tuple(get_or_replace(self.flatten(instr)) for instr in instrs)
          for instrs in ast_node.store_nodes
      ])
    )

  def ExpressionNode(self, ast_node):
    def get_children_not_replace():
      _and = lambda x, y: x and y
      not_replace = True 
      children_not_replace = [True] * len(ast_node.children)
      # Looping in reversed order to support mixed cases:
      # -------[ origin ]-------
      # def foo():
      #   static_foo0(static_foo1(), dynamic_bar0(), static_foo1())
      # -------[ converted ]-------
      # def foo():
      #   tmp0 = static_foo1()
      #   tmp1 = dynamic_bar0()
      #   static_foo0(tmp0, tmp1, static_foo1())
      is_ast_node_static = self.attr(ast_node).is_procedure_static_convertible
      for i, child in tuple(enumerate(ast_node.children))[::-1]:
        # case0: from static to dynamic.
        # case1: from dynamic to static.
        is_child_static = self.attr(child).is_procedure_static_convertible
        same = (is_ast_node_static == is_child_static)
        not_replace = (not_replace and same)
        children_not_replace[i] = not_replace
      return children_not_replace
    def flatten_and_try_replace(child, not_replace):
      flattend_node = self.flatten(child)
      if not_replace:
        return flattend_node
      else:
        return self.generate_local_var_for_expr(flattend_node)
    new_children = tuple(
      flatten_and_try_replace(*pair) for pair in zip(ast_node.children, get_children_not_replace())
    )
    return type(ast_node)(new_children)

  def generate_local_var_for_expr(self, ast_node):
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
      bytecode_ast.StatementNode(
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
    return type(ast_node)(ast_node.instruction)
