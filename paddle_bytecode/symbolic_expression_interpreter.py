from typing import Dict, Callable
from . import bytecode_ast

class SymbolicExpressionInterpreter:

  def __init__(self,
               builtin_funcs: Dict[str, Callable[["BytecodeAstNode", "BytecodeAttr"], None]]):
    self.builtin_funcs = builtin_funcs

  def interpret(self, ast_node):
    ast_cls = type(ast_node)
    if not hasattr(self, ast_cls.__name__):
      assert len(ast_cls.__bases__) == 1
      ast_cls = ast_cls.__bases__[0]
    if hasattr(self, ast_cls.__name__):
      return getattr(self, ast_cls.__name__)(ast_node)
    else:
      return self.intepret_flat_children(ast_node)

  def intepret_flat_children(self, ast_node):
    for child in ast_node.flat_children():
      self.interpret(child)

  def ExpressionNode(self, ast_node):
    for child in ast_node.children:
      self.interpret(child)
    if not isinstance(ast_node.children[0], bytecode_ast.InstructionNodeBase):
      return
    if not isinstance(ast_node.children[-1], bytecode_ast.InstructionNodeBase):
      return
    if ast_node.children[-1].instruction.opname != "CALL_FUNCTION":
      return
    if ast_node.children[0].instruction.opname not in {"LOAD_GLOBAL", "LOAD_DEREF"}:
      return
    func_name = ast_node.children[0].instruction.argval
    if func_name not in self.builtin_funcs:
      return
    return self.builtin_funcs[func_name](*ast_node.children[1:-1])
