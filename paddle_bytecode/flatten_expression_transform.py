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

  def flatten(self, ast_node, replace_with_local_var=False):
    ast_cls = type(ast_node)
    if not hasattr(self, ast_cls.__name__):
      assert len(ast_cls.__bases__) == 1
      ast_cls = ast_cls.__bases__[0]
    return getattr(self, ast_cls.__name__)(ast_node, replace_with_local_var)

  def StatementListNode(self, ast_node, replace_with_local_var):
    # use `that` instead of self in order to support nested statement list.
    that = type(self)(self.generate_new_local_varname, self.attr)
    children = []
    for child in ast_node.children: 
      flattened = that.flatten(child, replace_with_local_var)
      children = children + that.generated_ast_nodes
      children.append(flattened)
      that.generated_ast_nodes = []
    return type(ast_node)(children)

  def StatementNode(self, ast_node, replace_with_local_var):
    expr_in_store_nodes = reduce(
      lambda acc, nodes:
        acc and reduce(lambda a, x: a and isinstance(x, bytecode_ast.ExpressionNodeBase), nodes, True),
      ast_node.store_nodes,
      True,
    )
    get_or_replace = self.generate_local_var_for_expr if expr_in_store_nodes else lambda x:x
    return type(ast_node)(
      get_or_replace(self.flatten(ast_node.expr_node, replace_with_local_var)),
      list([
        tuple(get_or_replace(self.flatten(instr, replace_with_local_var)) for instr in instrs)
          for instrs in ast_node.store_nodes
      ])
    )

  def ExpressionNode(self, ast_node, replace_with_local_var):
    def calc_children_must_replace_with_local_var():
      _and = lambda x, y: x and y
      must_replace = False 
      children_must_place = [False] * len(ast_node.children)
      # Looping in reversed order to support mixed cases:
      # -------[ origin ]-------
      # def foo():
      #   static_foo0(static_foo1(), dynamic_bar0(), static_foo1())
      # -------[ converted ]-------
      # def foo():
      #   tmp0 = static_foo1()
      #   tmp1 = dynamic_bar0()
      #   static_foo0(tmp0, tmp1, static_foo1())
      from .dump_transform import DumpTransform
      from pprint import pprint
      pprint(DumpTransform().dump(ast_node))
      for i, child in tuple(enumerate(ast_node.children))[::-1]:
        static_convertible = (
          self.attr(child).is_procedure_static_convertible
          and reduce(_and, self.attr(child).is_result_static_convertible, True)
        )
        lifetime_allways_static = reduce(_and, self.attr(child).lifetime_allways_static, True)
        pprint((static_convertible, lifetime_allways_static))
        # Handle cases from static python code to dynamic python code or
        # cases from dynamic python code to static python code.
        must_replace = must_replace or (static_convertible != lifetime_allways_static)
        children_must_place[i] = must_replace
      return children_must_place
    new_children = tuple(
      self.flatten(*pair) for pair in zip(ast_node.children, calc_children_must_replace_with_local_var())
    )
    get_or_replace = self.generate_local_var_for_expr if replace_with_local_var else lambda x:x
    return get_or_replace(type(ast_node)(new_children))

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

  def InstructionNodeBase(self, ast_node, replace_with_local_var):
    return type(ast_node)(ast_node.instruction)
