from typing import Callable, Set, List

class GetUndefinedLocalVarNamesTransform:
  def __init__(self, attr: Callable[["BytecodeAstNode"], "BytecodeAttr"]):
    self.attr = attr
    self._defined_local_varnames: Set[str] = set()
    self._undefined_local_varnames: List[str] = []

  @property
  def undefined_local_varnames(self):
    return self._undefined_local_varnames

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
    self._defined_local_varnames.add(varname)

  def LOAD_FAST(self, ast_node):
    varname = ast_node.instruction.argval
    if varname not in self._defined_local_varnames:
      self._undefined_local_varnames.append(varname)
    else:
      # Do nothing.
      pass
