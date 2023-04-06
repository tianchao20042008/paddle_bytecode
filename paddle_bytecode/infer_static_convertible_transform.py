import dis
from typing import Callable,List
from . import bytecode_ast


class InferIsProcedureStaticConvertibleTransform:

  def __init__(self,
               is_procedure_static_convertible: Callable[["BytecodeAstNode"], bool],
               mut_attr: Callable[["BytecodeAstNode"], "BytecodeAttr"]):
    self.is_procedure_static_convertible = is_procedure_static_convertible
    self.mut_attr = mut_attr

  def infer(self, ast_node):
    return getattr(self, type(ast_node).__name__)(ast_node)

  def StatementListNode(self, ast_node):
    is_procedure_static_convertible = True
    for child in ast_node.children:
      self.infer(child)
      is_procedure_static_convertible = (
        is_procedure_static_convertible and self.mut_attr(child).is_procedure_static_convertible
      )
    self.mut_attr(ast_node).is_procedure_static_convertible = is_procedure_static_convertible

  def StatementNode(self, ast_node):
    is_procedure_static_convertible = True
    self.infer(ast_node.expr_node)
    is_procedure_static_convertible = (
      is_procedure_static_convertible and self.mut_attr(ast_node.expr_node).is_procedure_static_convertible
    )
    for store_node_tuple in ast_node.store_nodes:
      if len(store_node_tuple) == 1:
        # example0: `a = foo()`
        self.mut_attr(store_node_tuple[0]).is_procedure_static_convertible = True
      elif len(store_node_tuple) == 2:
        # example0: `a[bar()] = foo()`
        # example1: `a.bar = foo()`
        self.infer(store_node_tuple[0])
        is_procedure_static_convertible = (
          is_procedure_static_convertible and self.mut_attr(store_node_tuple[0]).is_procedure_static_convertible
        )
        self.mut_attr(store_node_tuple[1]).is_procedure_static_convertible = True
      else:
        raise NotImplementedError()
    self.mut_attr(ast_node).is_procedure_static_convertible = is_procedure_static_convertible

  def ExpressionNode(self, ast_node):
    for child in ast_node.children:
      self.infer(child)
    self.mut_attr(ast_node).is_procedure_static_convertible = (
      self.mut_attr(ast_node.children[-1]).is_procedure_static_convertible
    )

  def InstructionNode(self, ast_node):
    self.mut_attr(ast_node).is_procedure_static_convertible = self.is_procedure_static_convertible(ast_node)

  def LOAD_CONST(self, ast_node):
    self.mut_attr(ast_node).is_procedure_static_convertible = True

  def LOAD_FAST(self, ast_node):
    self.mut_attr(ast_node).is_procedure_static_convertible = True

  def STORE_FAST(self, ast_node):
    self.mut_attr(ast_node).is_procedure_static_convertible = True

class InferIsResultStaticConvertibleTransform:

  def __init__(self,
               is_result_static_convertible: Callable[["Instruction"], List[bool]],
               mut_attr: Callable[["BytecodeAstNode"], "BytecodeAttr"]):
    self.is_result_static_convertible = is_result_static_convertible
    self.mut_attr = mut_attr
    self.local_name2is_result_static_convertible = {}

  def infer(self, ast_node):
    return getattr(self, type(ast_node).__name__)(ast_node)

  def StatementListNode(self, ast_node):
    for child in ast_node.children:
      self.infer(child)
    # StatementList has no results on stack.
    self.mut_attr(ast_node).is_result_static_convertible = ()

  def StatementNode(self, ast_node):
    self.infer(ast_node.expr_node)
    for i, store_node_tuple in enumerate(ast_node.store_nodes):
      if len(store_node_tuple) == 1:
        # example0: `a = foo()`
        store_node = store_node_tuple[0]
        # store_node has no results on stack.
        self.mut_attr(store_node).is_result_static_convertible = ()
        if store_node.instruction.opname == "STORE_FAST":
          # help to infer is_result_static_convertible for added instructions in compile pass.
          self.store_is_local_var_static_convertible(
            store_node, self.mut_attr(ast_node.expr_node).is_result_static_convertible[i]
          )
      elif len(store_node_tuple) == 2:
        # example0: `a[bar()] = foo()`
        # example1: `a.bar = foo()`
        self.infer(store_node_tuple[0])
        # store_node_tuple[1] has no results on stack.
        self.mut_attr(store_node_tuple[1]).is_result_static_convertible = ()
      else:
        raise NotImplementedError()
    # Statement has no results on stack.
    self.mut_attr(ast_node).is_result_static_convertible = ()

  def ExpressionNode(self, ast_node):
    last_child = None
    for child in ast_node.children:
      self.infer(child)
      last_child = child
    # expression is in reversed Polish notation.
    self.mut_attr(ast_node).is_result_static_convertible = self.mut_attr(last_child).is_result_static_convertible

  def InstructionNode(self, ast_node):
    self.mut_attr(ast_node).is_result_static_convertible = self.is_result_static_convertible(ast_node)

  def LOAD_CONST(self, ast_node):
    self.mut_attr(ast_node).is_result_static_convertible = (True,)

  def LOAD_FAST(self, ast_node):
    if ast_node.instruction.argval in self.local_name2is_result_static_convertible:
      self.mut_attr(ast_node).is_result_static_convertible = (
        self.local_name2is_result_static_convertible[ast_node.instruction.argval]
      )
    else:
      self.mut_attr(ast_node).is_result_static_convertible = self.is_result_static_convertible(ast_node)

  def store_is_local_var_static_convertible(self, ast_node, is_value_static_convertible):
    self.local_name2is_result_static_convertible[ast_node.instruction.argval] = (is_value_static_convertible,)

class InferStaticConvertibleTransform:
  def __init__(self,
               mut_attr: Callable[["BytecodeAstNode"], "BytecodeAttr"],
               is_procedure_static_convertible: Callable[["BytecodeAstNode"], bool],
               is_result_static_convertible: Callable[["Instruction"], List[bool]]):
    self.mut_attr = mut_attr
    self.is_procedure_static_convertible = is_procedure_static_convertible
    self.is_result_static_convertible = is_result_static_convertible

  def infer(self, ast_node):
    infer_procedure = InferIsProcedureStaticConvertibleTransform(
      self.is_procedure_static_convertible,
      self.mut_attr,
    )
    infer_procedure.infer(ast_node)
    infer_result = InferIsResultStaticConvertibleTransform(
      self.is_result_static_convertible,
      self.mut_attr,
    )
    infer_result.infer(ast_node)
