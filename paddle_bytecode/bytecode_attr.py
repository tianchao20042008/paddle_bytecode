from typing import List
from dataclasses import dataclass

@dataclass
class BytecodeAttr:

  # True if no dynamic python code touched when running this ast_node.
  is_procedure_static_convertible: bool = None

  # tuple of bool.
  # is_result_static_convertible[i] is True if the ith result of this ast_node is static convertible.
  is_result_static_convertible: List[bool] = ()

  # tuple of bool.
  # lifetime_allways_static[i] is True if no dynamic python code touched
  # during the lifetime of the ith result of this ast_node.
  lifetime_allways_static: List[bool] = None

  @staticmethod
  def make_getter(node2attr: dict = None):
    node2attr = {} if node2attr is None else node2attr
    def getter(node):
      if node not in node2attr:
        node2attr[node] = BytecodeAttr()
      return node2attr[node]
    return getter

  @staticmethod
  def make_gettable_and_mutable(node2ctx: dict = None):
    node2ctx = {} if node2ctx is None else node2ctx
    def gettable(node):
      assert node in node2ctx, node
      return node2ctx[node]
    def mutable(node):
      if node not in node2ctx:
        node2ctx[node] = BytecodeAttr()
      return node2ctx[node]
    return gettable, mutable

