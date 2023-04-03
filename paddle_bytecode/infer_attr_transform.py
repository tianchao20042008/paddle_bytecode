from typing import Callable
from .infer_static_convertible_transform import InferStaticConvertibleTransform
from .infer_lifetime_allways_static_transform import InferLifetimeAllwaysStaticTransform

class InferAttrTransform:
  def __init__(self,
               mut_attr: Callable[["BytecodeAstNode"], "BytecodeAttr"],
               is_procedure_static_convertible: Callable[["BytecodeAstNode"], bool],
               is_result_static_convertible: Callable[["Instruction"], List[bool]]):
    self.mut_attr = mut_attr
    self.is_procedure_static_convertible = is_procedure_static_convertible
    self.is_result_static_convertible = is_result_static_convertible

  def infer(self, ast_node):
    infer_static_convertible = InferStaticConvertibleTransform(
      self.mut_attr,
      self.is_procedure_static_convertible,
      self.is_result_static_convertible,
    )
    infer_static_convertible.infer(ast_node)
    infer_lifetime = InferLifetimeAllwaysStaticTransform(
      self.mut_attr,
      self.is_procedure_static_convertible,
    )
    infer_lifetime.infer(ast_node)
