from dataclasses import dataclass

@dataclass
class BytecodeAttr:

  # True if no dynamic python code touched when running this ast_node.
  is_procedure_static_convertible: bool = None

  # tuple of bool.
  # is_result_static_convertible[i] is True if the ith result of this ast_node are static convertible.
  is_result_static_convertible: tuple = ()

  # True if no dynamic python code touched during the lifetime of the results of this ast_node.
  lifetime_allways_static: bool = None

  @staticmethod
  def make_getter(node2attr: dict = None):
    node2attr = {} if node2attr is None else node2attr
    def getter(node):
      if node not in node2attr:
        node2attr[node] = BytecodeAttr()
      return node2attr[node]
    return getter

  @staticmethod
  def make_ctx():
    node2attr = {}
    return node2attr, make_getter(node2attr)
