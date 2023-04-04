from typing import Callable, List
from dataclasses import dataclass
from .bytecode_attr import BytecodeAttr

@dataclass
class InferCtx:
  # tuple of bool.
  # is_result_allways_static_from_now_on[i] is True if the ith result of this ast_node is 
  # encountering only static python code before destruction.
  # is_result_allways_static_from_now_on[i] is False if the ith result of this ast_node is
  # used by dynamic python code.
  # is_result_allways_static_from_now_on[i] is False if dynamic python code executed
  # before the destruction of the ith result of this ast_node.
  is_result_allways_static_from_now_on: tuple = ()

  @staticmethod
  def make_gettable_and_mutable(node2ctx: dict = None):
    node2ctx = {} if node2ctx is None else node2ctx
    def gettable(node):
      assert node in node2ctx, node
      return node2ctx[node]
    def mutable(node):
      if node not in node2ctx:
        node2ctx[node] = InferCtx()
      return node2ctx[node]
    return gettable, mutable

# Infer is_result_allways_static_from_now_on in reversed order.
# Q: Why in reversed order?
# A: to collect the information of all consumers of variables.
class InferIsResultAllwaysStaticFromNowOnTransform:
  def __init__(self,
               mut_attr: Callable[["BytecodeAstNode"], InferCtx],
               is_procedure_static_convertible: Callable[["BytecodeAstNode"], List[bool]]):
    self.mut_attr = mut_attr
    self.is_procedure_static_convertible = is_procedure_static_convertible
    self.var2is_allways_static_from_now_on: Dict[str, List[bool]] = {}

  def is_var_allways_static_from_now_on(self, var_name: str, default_val: List[bool]) -> List[bool]:
    bool_map = self.var2is_allways_static_from_now_on
    if var_name in bool_map:
      return bool_map[var_name]
    else: 
      return default_val

  def infer(self, ast_node, consumed_by_static: List[bool] =(True,)):
    return getattr(self, type(ast_node).__name__)(ast_node, consumed_by_static)
    
  def StatementListNode(self, ast_node, consumed_by_static):
    reversed_children = ast_node.children[::-1]
    for child in reversed_children:
      self.infer(child, consumed_by_static=(True,))
    # no results for StatementListNode.
    self.mut_attr(ast_node).is_result_allways_static_from_now_on = ()

  def StatementNode(self, ast_node, _):
    # Given python code `(*lvalue) = rvalue_expr`:
    # consumed_by_static : List[bool] = IsResultAllwaysStaticFromNowOn(*lvalue) # pseudo code
    consumed_by_static = tuple(map(self.infer_lvalue_in_store_nodes, ast_node.store_nodes[::-1]))
    self.infer(ast_node.expr_node, consumed_by_static)
    # no results for StatementNode.
    self.mut_attr(ast_node).is_result_allways_static_from_now_on = ()

  # infer whether a left-value is consumed by static python code.
  # return True if the store instruction can be static convertible
  # e.g.:
  # def foo(x, y):
  #   a = x + y # the infered consumed_by_static is False for `a` is used by print later.
  #   print(a)
  def infer_lvalue_in_store_nodes(self, store_nodes) -> bool:
    opname = store_nodes[-1].instruction.opname
    return getattr(self, opname)(store_nodes)

  def POP_TOP(self, store_nodes):
    assert len(store_nodes) == 1
    # Instruction POP_TOP: Removes the top-of-stack (TOS) item, or del TOS.
    # no more code consume tmp variable.
    # e.g.
    # def foo(x):
    #     x # generate instruction POP_TOP
    #     return x

    # no results for StatementNode.
    self.mut_attr(store_nodes[-1]).is_result_allways_static_from_now_on = ()
    return True

  def STORE_SUBSCR(self, store_nodes):
    # Instruction STORE_SUBSCR: Implements TOS1[TOS] = TOS2.
    assert len(store_nodes) == 3
    is_procedure_static_convertible = self.is_procedure_static_convertible(store_nodes[-1])
    assert len(is_procedure_static_convertible) == 1
    # the execution order is store_nodes[1] first then store_nodes[0]
    # here we in reversed order.
    self.infer(store_nodes[0], is_procedure_static_convertible)
    self.infer(store_nodes[1], is_procedure_static_convertible)
    # no results for STORE_SUBSCR.
    self.mut_attr(store_nodes[-1]).is_result_allways_static_from_now_on = ()
    return is_procedure_static_convertible[0]

  def DELETE_SUBSCR(self, store_nodes):
    # Instruction DELETE_SUBSCR: Implements del TOS1[TOS]
    assert len(store_nodes) == 2
    is_procedure_static_convertible = self.is_procedure_static_convertible(store_nodes[-1])
    assert len(is_procedure_static_convertible) == 1
    self.infer(store_nodes[0], is_procedure_static_convertible)
    # no results for DELETE_SUBSCR.
    self.mut_attr(store_nodes[-1]).is_result_allways_static_from_now_on = ()
    return is_procedure_static_convertible[0]

  def RETURN_VALUE(self, store_nodes):
    # Instruction RETURN_VALUE: Returns with TOS to the caller of the function.
    # no more code consume the returned value.

    # no results for RETURN_VALUE.
    self.mut_attr(store_nodes[-1]).is_result_allways_static_from_now_on = ()
    return True

  def YIELD_VALUE(self, store_nodes):
    # Instruction YIELD_VALUE: Pops TOS and yields it from a generator
    # the yielded value maybe used by subsequent dynamic python code. 

    # no results for YIELD_VALUE.
    self.mut_attr(store_nodes[-1]).is_result_allways_static_from_now_on = ()
    return False

  def STORE_NAME(self, store_nodes):
    # Instruction STORE_NAME: Implements name = TOS.
    # STORE_NAME may be equivalent to STORE_GLOBAL

    # no results for STORE_NAME.
    return self.STORE_GLOBAL(store_nodes)

  def DELETE_NAME(self, store_nodes):
    # Instruction DELETE_NAME: Implements del name.
    # DELETE_NAME may be equivalent to DELETE_GLOBAL

    # no results for DELETE_NAME.
    return self.DELETE_GLOBAL(store_nodes)

  def STORE_ATTR(self, store_nodes):
    # Instruction STORE_ATTR: Implements TOS.name = TOS1
    assert len(store_nodes) == 2
    is_procedure_static_convertible = self.is_procedure_static_convertible(store_nodes[-1])
    assert len(is_procedure_static_convertible) == 1
    self.infer(store_nodes[0], is_procedure_static_convertible)

    # no results for STORE_ATTR.
    self.mut_attr(store_nodes[-1]).is_result_allways_static_from_now_on = ()
    return is_procedure_static_convertible[0]

  def DELETE_ATTR(self, store_nodes):
    # Instruction DELETE_ATTR: Implements del TOS.name.
    assert len(store_nodes) == 1
    is_procedure_static_convertible = self.is_procedure_static_convertible(store_nodes[-1])
    assert len(is_procedure_static_convertible) == 1
    # no results for DELETE_ATTR.
    self.mut_attr(store_nodes[-1]).is_result_allways_static_from_now_on = ()
    return is_procedure_static_convertible[0]

  def STORE_GLOBAL(self, store_nodes):
    # Instruction STORE_GLOBAL: Works as STORE_NAME, but stores the name as a global.
    return self.STORE_FAST(store_nodes)

  def DELETE_GLOBAL(self, store_nodes):
    # Instruction DELETE_GLOBAL: Works as DELETE_NAME, but deletes a global name.
    assert len(store_nodes) == 1
    # no results for DELETE_GLOBAL.
    self.mut_attr(store_nodes[-1]).is_result_allways_static_from_now_on = ()
    # No more code consume the deleted value.
    return True

  def STORE_FAST(self, store_nodes):
    # Instruction STORE_FAST: Stores TOS into the local co_varnames[var_num]
    assert len(store_nodes) == 1
    varname = store_nodes[-1].instruction.argval
    is_allways_static_from_now_on = self.is_var_allways_static_from_now_on(varname, default_val=(True,))
    # Given `x = x + 1`, the left `x` and right `x` will be bound to different value:
    # Here we are in reversed order. we must clear the information of the left `x` before
    # processing the right `x`.
    del self.var2is_allways_static_from_now_on[varname]
    # The rvalue are regarded as results of STORE_FAST even though actually no results for STORE_FAST.
    self.mut_attr(store_nodes[-1]).is_result_allways_static_from_now_on = is_allways_static_from_now_on
    return is_allways_static_from_now_on

  def DELETE_FAST(self, store_nodes):
    # Instruction DELETE_FAST: Deletes local co_varnames[var_num].
    assert len(store_nodes) == 1
    # no results for DELETE_FAST.
    self.mut_attr(store_nodes[-1]).is_result_allways_static_from_now_on = (True,)
    # No more code consume the deleted value.
    return True

  def ExpressionNode(self, ast_node, consumed_by_static):
    is_procedure_static_convertible = self.is_procedure_static_convertible(ast_node.children[-1])
    if not is_procedure_static_convertible:
      # Touching dynamic python code makes all variable non-static.
      for key, _ in self.var2is_allways_static_from_now_on.items():
        self.var2is_allways_static_from_now_on[key] = (False,)
    reversed_children = ast_node.children[::-1]
    for child in reversed_children:
      self.infer(child, consumed_by_static=(is_procedure_static_convertible,))
    self.mut_attr(ast_node).is_result_allways_static_from_now_on = (
      is_procedure_static_convertible and consumed_by_static[0],
    )

  def InstructionNode(self, ast_node, consumed_by_static):
    assert type(consumed_by_static) is tuple
    self.mut_attr(ast_node).is_result_allways_static_from_now_on = consumed_by_static

  def LOAD_CONST(self, ast_node, consumed_by_static):
    self.InstructionNode(ast_node, consumed_by_static)

  def LOAD_FAST(self, ast_node, consumed_by_static):
    # Instruction LOAD_FAST: Pushes a reference to the local co_varnames[var_num] onto the stack.
    varname = ast_node.instruction.argval
    is_allways_static_from_now_on = self.is_var_allways_static_from_now_on(varname, default_val=(True,))
    is_allways_static_from_now_on = (consumed_by_static[0] and is_allways_static_from_now_on[0],)
    self.var2is_allways_static_from_now_on[varname] = is_allways_static_from_now_on
    self.mut_attr(ast_node).is_result_allways_static_from_now_on = is_allways_static_from_now_on

class InferLifetimeAllwaysStaticByIsAllwaysStaticFromNowOnTransform:
  def __init__(self,
               mut_attr: Callable[["BytecodeAstNode"], BytecodeAttr],
               is_allways_static_from_now_on: Callable[["BytecodeAstNode"], List[bool]]):
    self.mut_attr = mut_attr
    self.is_allways_static_from_now_on = is_allways_static_from_now_on
    self.var2lifetime_allways_static = {}

  def infer(self, ast_node):
    is_allways_static_from_now_on = self.is_allways_static_from_now_on(ast_node)
    assert type(is_allways_static_from_now_on) is tuple, type(is_allways_static_from_now_on)
    self.mut_attr(ast_node).lifetime_allways_static = is_allways_static_from_now_on
    if hasattr(self, type(ast_node).__name__):
      getattr(self, type(ast_node).__name__)(ast_node)
    for child in ast_node.flat_children():
      self.infer(child)

  def STORE_GLOBAL(self, ast_node):
    self.STORE_FAST(ast_node)
    # Global variables may be used outside current functions.
    self.mut_attr(ast_node).lifetime_allways_static = (False,)

  def STORE_FAST(self, ast_node):
    varname = ast_node.instruction.argval
    self.var2lifetime_allways_static[varname] = self.mut_attr(ast_node).lifetime_allways_static

  def LOAD_FAST(self, ast_node):
    mut_attr = self.mut_attr(ast_node)
    varname = ast_node.instruction.argval
    if varname in self.var2lifetime_allways_static:
      lifetime_allways_static = (
        mut_attr.lifetime_allways_static[0] and self.var2lifetime_allways_static[varname][0],
      )
      mut_attr.lifetime_allways_static = lifetime_allways_static

class InferLifetimeAllwaysStaticTransform:
  def __init__(self,
               mut_attr: Callable[["BytecodeAstNode"], BytecodeAttr],
               is_procedure_static_convertible: Callable[["BytecodeAstNode"], List[bool]]):
    self.mut_attr = mut_attr
    self.is_procedure_static_convertible = is_procedure_static_convertible

  def infer(self, ast_node):
    # get_infer_ctx and mut_infer_ctx use the same dict.
    get_infer_ctx, mut_infer_ctx = InferCtx.make_gettable_and_mutable()
    backward_inferer = InferIsResultAllwaysStaticFromNowOnTransform(
      mut_infer_ctx, self.is_procedure_static_convertible
    )
    backward_inferer.infer(ast_node)
    forward_inferer = InferLifetimeAllwaysStaticByIsAllwaysStaticFromNowOnTransform(
     self.mut_attr, lambda ast_node: get_infer_ctx(ast_node).is_result_allways_static_from_now_on
    )
    forward_inferer.infer(ast_node)
