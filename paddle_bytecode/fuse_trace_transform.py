from typing import Callable
from functools import reduce
from . import bytecode_ast
from .instruction import Instruction
import dis

class FuseTraceTransform:
  def __init__(self,
              generate_new_local_varname: Callable[[], str],
              generate_new_func_name: Callable[[], str],
              attr: Callable[["BytecodeAstNode"], "BytecodeAttr"]):
    self.generate_new_local_varname = generate_new_local_varname
    self.generate_new_func_name = generate_new_func_name
    self.attr = attr

  def __call__(self, ast_node):
    ast_cls = type(ast_node)
    if not hasattr(self, ast_cls.__name__):
      assert len(ast_cls.__bases__) == 1
      ast_cls = ast_cls.__bases__[0]
    return getattr(self, ast_cls.__name__)(ast_node)

  def StatementListNode(self, ast_node):
    def is_static_convertible(ast_node):
      TODO()
    new_children = []
    static_trace_ast_nodes = []
    for child in ast_node.children:
      if is_static_convertible(child):
        static_trace_ast_nodes.append(child)
      else:
        for generated_ast_node in self.generate_ast_nodes_for_func_call(static_trace_ast_nodes):
          new_children.append(generated_ast_node)
        new_children.append(child)
        static_trace_ast_nodes = []
    for generated_ast_node in self.generate_ast_nodes_for_func_call(static_trace_ast_nodes):
      new_children.append(generated_ast_node)
    return type(ast_node)(new_children)

  def get_input_varnames(self, static_trace_ast_nodes):
    defined_var_names = set()
    TODO()

  def get_output_varnames(self, static_trace_ast_nodes):
    TODO()

  def generate_ast_nodes_for_func_call(self, static_trace_ast_nodes):
    if len(static_trace_ast_nodes) == 0:
      return
    func_name = self.generate_new_func_name()
    input_varnames = self.get_input_varnames(static_trace_ast_nodes)
    output_varnames = self.get_output_varnames(static_trace_ast_nodes)
    if len(output_varnames) == 0:
      TODO()
    elif len(output_varnames) == 1:
      TODO()
    else:
      TODO()
