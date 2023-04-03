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

  def flatten(self, ast_node, called_in_expr=False):
    ast_cls = type(ast_node)
    if not hasattr(self, ast_cls.__name__):
      assert len(ast_cls.__bases__) == 1
      ast_cls = ast_cls.__bases__[0]
    return getattr(self, ast_cls.__name__)(ast_node, called_in_expr)

  def StatementListNode(self, ast_node, called_in_expr):
    # use `that` instead of self in order to support nested statement list.
    that = type(self)(self.generate_new_local_varname, self.attr)
    children = []
    for child in ast_node.children: 
      children = children + that.generated_ast_nodes
      children.append(that.flatten(child, called_in_expr))
      that.generated_ast_nodes = []
    return type(ast_node)(children)

  def StatementNode(self, ast_node, called_in_expr):
    expr_in_store_nodes = reduce(
      lambda nodes, acc:
        acc and reduce(lambda x, a: a and isinstance(x, bytecode_ast.ExpressionNodeBase), nodes, True),
      ast_node.store_nodes,
      True,
    )
    def get_identity_or_replace(sub_ast_node):
      if expr_in_store_nodes:
        return self.generate_local_var_for_expr(sub_ast_node)
      else:
        return ast_node
    return type(ast_node)(
      get_identity_or_replace(self.flatten(ast_node.expr_node, called_in_expr)),
      list([
        tuple(get_identity_or_replace(self.flatten(instr, called_in_expr)) for instr in instrs)
          for instrs in ast_node.store_nodes
      ])
    )

  def ExpressionNode(self, ast_node, called_in_expr):
    new_children = tuple(self.flatten(child, called_in_expr=True) for child in ast_node.children)
    if called_in_expr:
      _and = lambda x, y: x and y
      static_convertible = (
        self.attr(ast_node).is_procedure_static_convertible
        and reduce(_and, self.attr(ast_node).is_result_static_convertible, True)
      )
      lifetime_allways_static = reduce(_and, self.attr(ast_node).lifetime_allways_static, True)
      # Handle cases from static python code to dynamic python code or
      # cases from dynamic python code to static python code.
      if static_convertible != lifetime_allways_static:
        new_children = tuple(map(self.generate_local_var_for_expr, new_children))
    return type(ast_node)(new_children)

  def generate_local_var_for_expr(self, ast_node):
    if not isinstance(ast_node, bytecode_ast.ExpressionNodeBase)
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
        [tuple(bytecode_ast.STORE_FAST(store_instr))]
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

  def InstructionNodeBase(self, ast_node, called_in_expr):
    return type(ast_node)(ast_node.instruction)
