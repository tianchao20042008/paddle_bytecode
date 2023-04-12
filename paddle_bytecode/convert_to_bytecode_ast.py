from . import bytecode_ast
from . import instr_stack_util
import dis

def convert_to_bytecode_ast(instructions):
  instruction_nodes = [convert_to_instruction_node(i) for i in instructions]
  return convert_to_statement_list_node(instruction_nodes)

def convert_to_statement_list_node(instruction_nodes):
  acc = 0
  sub_instruction_nodes = []
  children = []
  for instruction_node in instruction_nodes:
    acc = acc + instruction_node.stack_effect()
    sub_instruction_nodes.append(instruction_node)
    if acc > 0:
      pass
    elif acc == 0:
      children.append(convert_to_statement_node(sub_instruction_nodes))
      sub_instruction_nodes = []
    else:
      raise NotImplementedError("accumulated stack_effect should never be negative.")
  return bytecode_ast.StatementListNode(children)


def convert_to_statement_node(instruction_nodes):
  assert instruction_nodes[-1].num_outputs_on_stack() == 0, instruction_nodes[-1].instruction
  store_nodes = []
  while True:
    instruction_nodes, store_instruction_nodes = _get_prev_store_instructions(instruction_nodes)
    if len(store_instruction_nodes) == 0:
      break;
    elif len(store_instruction_nodes) == 1:
      store_nodes.append((store_instruction_nodes[0],))
    elif len(store_instruction_nodes) > 1:
      store_node = store_instruction_nodes[-1]
      assert store_node.num_outputs_on_stack() == 0, store_instruction_nodes[-1]
      store_nodes.append((*convert_to_expression_node_tuple(store_instruction_nodes[:-1]), store_node))
    else:
      raise NotImplementedError("store instructions not supported: %s" % store_instruction_nodes[-1])
  return StoreNodeCreator()(convert_to_expression_node(instruction_nodes), store_nodes[::-1])

class StoreNodeCreator:
  def __call__(self, expr_node, store_nodes):
    if len(store_nodes) == 1:
      opname = store_nodes[0][-1].instruction.opname
      method_name = opname
      has_entry = hasattr(self, method_name)
      if has_entry:
        create = getattr(self, method_name)
        return create(expr_node, store_nodes)
      else:
        return self.generic_create(expr_node, store_nodes)
    else:
      return self.generic_create(expr_node, store_nodes)

  def generic_create(self, expr_node, store_nodes):
    return bytecode_ast.GenericStoreNode(expr_node, store_nodes)

  def RETURN_VALUE(self, expr_node, store_nodes):
    return bytecode_ast.ReturnValueNode(expr_node, store_nodes)

def _get_prev_store_instructions(instruction_nodes):
  if not instr_stack_util.opcode2is_store_or_delete[instruction_nodes[-1].opcode]:
    return instruction_nodes, []
  acc_stack_effect = 0
  pos = len(instruction_nodes)
  while pos > 0:
    pos -= 1
    acc_stack_effect += instruction_nodes[pos].stack_effect()
    if acc_stack_effect == -1:
      return instruction_nodes[0:pos], instruction_nodes[pos:]
  raise NotImplementedError("dead code")

def convert_to_expression_node_tuple(instruction_nodes):
  # `symbolic_stack` contains instances of BytecodeAstNode.
  symbolic_stack = []
  for instruction_node in instruction_nodes:
    num_inputs_on_stack = instruction_node.num_inputs_on_stack()
    if num_inputs_on_stack == 0:
      symbolic_stack.append(instruction_node)
    else:
      # expression_children is initialized in reversed order.
      expression_children = [instruction_node]
      while num_inputs_on_stack > 0:
        instruction_as_arg = symbolic_stack.pop()
        num_inputs_on_stack -= instruction_as_arg.num_outputs_on_stack()
        assert num_inputs_on_stack >= 0
        expression_children.append(instruction_as_arg)
      assert num_inputs_on_stack == 0
      expression_children.reverse()
      symbolic_stack.append(bytecode_ast.GenericExpressionNode(expression_children))
  return symbolic_stack

def convert_to_expression_node(instruction_nodes):
  symbolic_stack = convert_to_expression_node_tuple(instruction_nodes)
  assert len(symbolic_stack) == 1, symbolic_stack
  return ExprCreator()(symbolic_stack[0])

class ExprCreator:
  def __call__(self, expr_node):
    if not isinstance(expr_node, bytecode_ast.ExpressionNodeBase):
      return expr_node
    last_node = expr_node.children[-1]
    if isinstance(last_node, bytecode_ast.InstructionNodeBase):
      opname = last_node.instruction.opname
      if hasattr(self, opname):
        return getattr(self, opname)(expr_node)
      else:
        return expr_node
    else:
      return expr_node

  def MAKE_FUNCTION(self, expr_node):
    make_function_node = bytecode_ast.MakeFunctionExprNode(expr_node.children)
    code_obj = expr_node.children[0].instruction.argval
    make_function_node.function_body = convert_to_bytecode_ast(list(dis.get_instructions(code_obj)))
    make_function_node.co_argcount = code_obj.co_argcount
    return make_function_node

def convert_to_instruction_node(instruction):
  if hasattr(bytecode_ast, instruction.opname):
    cls = getattr(bytecode_ast, instruction.opname)
  else:
    cls = bytecode_ast.GenericInstructionNode
  return cls(instruction)
