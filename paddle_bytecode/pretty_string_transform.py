RED = ""
GREEN = ""
YELLOW = ""
BLUE = ""
MAGENTA = ""
CYAN = ""
CLR = ""
 
 
class PrettyStringTransform:
 
  def __init__(self, indent_size=2):
    self.indent_size = indent_size
 
  def __call__(self, ast_node, indent_level=0):
    ast_cls = type(ast_node)
    if not hasattr(self, ast_cls.__name__):
      assert len(ast_cls.__bases__) == 1
      ast_cls = ast_cls.__bases__[0]
    return getattr(self, ast_cls.__name__)(ast_node, indent_level)
  
  def indent(self, indent_level):
     return indent_level * self.indent_size * " "
  
  def Program(self, ast_node, indent_level=0):
    dump_string = ""
    dump_string += RED
    dump_string += f"{self.indent(indent_level)}Program(\n"
    dump_string += f"{self.indent(indent_level + 1)}children=[\n"
    dump_string += CLR
    for child in ast_node.flat_children_except_label():
      dump_string += self(child, indent_level + 2)
    dump_string += RED
    dump_string += f"{self.indent(indent_level + 1)}]\n"
    dump_string += f"{self.indent(indent_level)})\n"
    dump_string += CLR
    return dump_string
 
  def StmtExpressionNode(self, ast_node, indent_level=0):
    dump_string = ""
    dump_string += GREEN
    dump_string += f"{self.indent(indent_level)}StmtExpressionNode(\n"
    dump_string += f"{self.indent(indent_level + 1)}statement_list_node=\n"
    dump_string += CLR
    dump_string += self(ast_node.statement_list_node, indent_level + 2)
    dump_string += GREEN
    dump_string += f"{self.indent(indent_level + 1)}expr_node=\n"
    dump_string += CLR
    dump_string += self(ast_node.expr_node, indent_level + 2)
    dump_string += GREEN
    dump_string += f"{self.indent(indent_level)})\n"
    dump_string += CLR
    return dump_string
  
  def StatementListNode(self, ast_node, indent_level=0):
    dump_string = ""
    dump_string += GREEN
    dump_string += f"{self.indent(indent_level)}StatementListNode(\n"
    dump_string += f"{self.indent(indent_level + 1)}children=[\n"
    dump_string += CLR
    for child in ast_node.children:
      dump_string += self(child, indent_level + 2)
    dump_string += GREEN
    dump_string += f"{self.indent(indent_level + 1)}]\n"
    dump_string += f"{self.indent(indent_level)})\n"
    dump_string += CLR
    return dump_string
  
  def JumpNodeBase(self, ast_node, indent_level=0):
    dump_string = ""
    dump_string += GREEN
    dump_string += f"{self.indent(indent_level)}JumpNodeBase(\n"
    dump_string += f"{self.indent(indent_level + 1)}instruction={CLR}{CYAN}Instruction(opname={ast_node.instruction.opname}, argval={ast_node.instruction.argval}){CLR}{GREEN}\n"
    if ast_node.label_node is not None:
      dump_string += f"{self.indent(indent_level + 1)}label_node=\n"
      dump_string += CLR
      dump_string += self(ast_node.label_node, indent_level + 2)
      dump_string += GREEN
    else:
      print("WARN: label_node is None")
    dump_string += f"{self.indent(indent_level + 1)}\n"
    dump_string += f"{self.indent(indent_level)})\n"
    dump_string += CLR
    return dump_string
  
  def LabelNode(self, ast_node, indent_level=0):
    dump_string = ""
    dump_string += GREEN
    dump_string += f"{self.indent(indent_level)}LabelNode()\n"
    dump_string += CLR
    return dump_string
  
  def StoreNodeBase(self, ast_node, indent_level=0):
    dump_string = ""
    dump_string += YELLOW
    dump_string += f"{self.indent(indent_level)}StoreNodeBase(\n"
    dump_string += f"{self.indent(indent_level + 1)}expr_node=\n"
    dump_string += CLR
    dump_string += self(ast_node.expr_node, indent_level + 2)
    dump_string += YELLOW
    dump_string += f"{self.indent(indent_level + 1)}store_nodes=[\n"
    dump_string += CLR
    for instrs in ast_node.store_nodes:
      dump_string += f"{self.indent(indent_level + 2)}(\n"
      for instr in instrs:
          dump_string += self(instr, indent_level + 3)
      dump_string += f"{self.indent(indent_level + 2)})\n"
    dump_string += YELLOW
    dump_string += f"{self.indent(indent_level + 1)}]\n"
    dump_string += f"{self.indent(indent_level)})\n"
    dump_string += CLR
    return dump_string
  
  def ExpressionNodeBase(self, ast_node, indent_level=0):
    dump_string = ""
    dump_string += BLUE
    dump_string += f"{self.indent(indent_level)}{type(ast_node).__name__}(\n"
    dump_string += f"{self.indent(indent_level + 1)}children=[\n"
    dump_string += CLR
    for child in ast_node.children:
        dump_string += self(child, indent_level + 2)
    dump_string += BLUE
    dump_string += f"{self.indent(indent_level + 1)}]\n"
    dump_string += f"{self.indent(indent_level)})\n"
    dump_string += CLR
    return dump_string
 
  def MakeFunctionExprNode(self, ast_node, indent_level=0):
    dump_string = ""
    dump_string += BLUE
    dump_string += f"{self.indent(indent_level)}{type(ast_node).__name__}(\n"
    dump_string += f"{self.indent(indent_level + 1)}function_body=\n"
    dump_string += self(ast_node.function_body, indent_level+2)
    dump_string += f"{self.indent(indent_level + 1)}children=[\n"
    dump_string += CLR
    for child in ast_node.children:
        dump_string += self(child, indent_level + 2)
    dump_string += BLUE
    dump_string += f"{self.indent(indent_level + 1)}]\n"
    dump_string += f"{self.indent(indent_level)})\n"
    dump_string += CLR
    return dump_string
 
  def InstructionNodeBase(self, ast_node, indent_level=0):
    dump_string = ""
    dump_string += MAGENTA
    dump_string += f"{self.indent(indent_level)}{type(ast_node).__name__}(\n"
    dump_string += f"{self.indent(indent_level + 1)}instruction={CLR}{CYAN}Instruction(opname={ast_node.instruction.opname}, argval={ast_node.instruction.argval}){CLR}{MAGENTA}\n"
    dump_string += f"{self.indent(indent_level)})\n"
    dump_string += CLR
    return dump_string
