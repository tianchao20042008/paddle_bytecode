from typing import Callable, Set, List
from collections import OrderedDict

class GetDefinedDynamicVarNamesTransform:
  def __init__(self, attr: Callable[["BytecodeAstNode"], "BytecodeAttr"]):
    self.attr = attr
    self._defined_dynamic_varnames: Dict[str, None] = OrderedDict() # as ordered set

  @property
  def defined_dynamic_varnames(self):
    return list(k for k,_ in self._defined_dynamic_varnames.items())

  def __call__(self, ast_node):
    ast_cls = type(ast_node)
    if not hasattr(self, ast_cls.__name__):
      assert len(ast_cls.__bases__) == 1
      ast_cls = ast_cls.__bases__[0]
    if hasattr(self, ast_cls.__name__):
      return getattr(self, ast_cls.__name__)(ast_node)
    else:
      for child in ast_node.flat_children():
        self(child)

  def STORE_FAST(self, ast_node):
    varname = ast_node.instruction.argval
    assert len(self.attr(ast_node).lifetime_allways_static) == 1
    if self.attr(ast_node).lifetime_allways_static[0]:
      # Do nothing.
      pass
    else:
      self._defined_dynamic_varnames[varname] = None
