from typing import Callable
from functools import reduce
from . import bytecode_ast
from .instruction import Instruction
import dis
from .get_undefined_local_var_names_transform import GetUndefinedLocalVarNamesTransform
from .get_defined_dynamic_var_names_transform import GetDefinedDynamicVarNamesTransform
from .is_static_convertible_transform import IsStaticConvertibleTransform

class FuseTraceTransform:
  def __init__(self,
               func_name: str,
               attr: Callable[["BytecodeAstNode"], "BytecodeAttr"],
               generate_func_name: Callable[[], str]):
    self.func_name = func_name
    self.attr = attr
    self.generate_func_name = generate_func_name
    self.is_static_convertible = IsStaticConvertibleTransform(attr)

  def __call__(self, ast_node):
    ast_cls = type(ast_node)
    if not hasattr(self, ast_cls.__name__):
      assert len(ast_cls.__bases__) == 1
      ast_cls = ast_cls.__bases__[0]
    return getattr(self, ast_cls.__name__)(ast_node)

  def StatementListNode(self, ast_node):
    new_children = []
    static_trace_ast_nodes = []
    for child in ast_node.children:
      if self.is_static_convertible(child):
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
    transform = GetUndefinedLocalVarNamesTransform(self.attr)
    for ast_node in static_trace_ast_nodes:
      transform(ast_node)
    return transform.undefined_local_varnames

  def get_output_varnames(self, static_trace_ast_nodes):
    transform = GetDefinedDynamicVarNamesTransform(self.attr)
    for ast_node in static_trace_ast_nodes:
      transform(ast_node)
    return transform.defined_dynamic_varnames

  def generate_ast_nodes_for_func_call(self, static_trace_ast_nodes):
    if len(static_trace_ast_nodes) == 0:
      return
    func_name = self.generate_func_name()
    input_varnames = self.get_input_varnames(static_trace_ast_nodes)
    output_varnames = self.get_output_varnames(static_trace_ast_nodes)
    if len(output_varnames) == 0:
      func_body = self.generate_func_body_for_zero_return(
        backbone=static_trace_ast_nodes,
      )
    elif len(output_varnames) == 1:
      func_body = self.generate_func_body_for_one_return(
        backbone=static_trace_ast_nodes,
        ret_varname=output_varnames[0],
      )
    else:
      func_body = self.generate_func_body_for_multi_return(
        backbone=static_trace_ast_nodes,
        ret_varnames=output_varnames
      )
    func_make_ast_node = self.create_func_make_ast_node(
      func_body=func_body,
      func_name=func_name,
      co_argcount=input_varnames,
    )
    func_store_ast_node = self.create_func_store_ast_node(
      func_make_ast_node=func_make_ast_node,
      func_name=func_name
    )
    yield func_store_ast_node
    func_call_ast_node = self.create_func_call_ast_node(
      func_name=func_name,
      input_varnames=input_varnames
    )
    if len(output_varnames) > 0:
      ret_store_ast_node = self.create_ret_store_ast_node(
        func_call_ast_node=func_call_ast_node,
        output_varnames=output_varnames
      )
      yield ret_store_ast_node
    else:
      pop_top_ast_node = self.create_pop_top_ast_node(
        func_call_ast_node=func_call_ast_node,
      )
      yield pop_top_ast_node

  def generate_func_body_for_zero_return(self, backbone):
    '''append python code `return`'''

    load_const_opname = "LOAD_CONST"
    load_const_instr = Instruction(
      opcode=dis.opmap[load_const_opname],
      opname=load_const_opname,
      arg=-1,
      argval=None,
      argrepr="",
      offset=-1,
      starts_line=-1,
      is_jump_target=None,
    )
    load_const_node = bytecode_ast.LOAD_CONST(load_const_instr)
    return_value_opname = "RETURN_VALUE"
    return_value_instr = Instruction(
      opcode=dis.opmap[return_value_opname],
      opname=return_value_opname,
      arg=-1,
      argval=None,
      argrepr="",
      offset=-1,
      starts_line=-1,
      is_jump_target=None,
    )
    return_value_node = bytecode_ast.GenericInstructionNode(return_value_instr) 
    return [*backbone, load_const_node, return_value_node]

  def generate_func_body_for_one_return(self, backbone, ret_varname):
    '''append python code `return $ret_varname`'''

    load_fast_opname = "LOAD_FAST"
    load_fast_instr = Instruction(
      opcode=dis.opmap[load_fast_opname],
      opname=load_fast_opname,
      arg=-1,
      argval=ret_varname,
      argrepr=ret_varname,
      offset=-1,
      starts_line=-1,
      is_jump_target=None,
    )
    load_fast_node = bytecode_ast.LOAD_FAST(load_fast_instr)
    return_value_opname = "RETURN_VALUE"
    return_value_instr = Instruction(
      opcode=dis.opmap[return_value_opname],
      opname=return_value_opname,
      arg=-1,
      argval=None,
      argrepr="",
      offset=-1,
      starts_line=-1,
      is_jump_target=None,
    )
    return_value_node = bytecode_ast.GenericInstructionNode(return_value_instr) 
    return [*backbone, load_fast_node, return_value_node]

  def generate_func_body_for_multi_return(self, backbone, ret_varnames):
    '''append python code `return *$ret_varnames`'''
    load_fast_nodes = []
    for ret_varname in ret_varnames:
      load_fast_opname = "LOAD_FAST"
      load_fast_instr = Instruction(
        opcode=dis.opmap[load_fast_opname],
        opname=load_fast_opname,
        arg=-1,
        argval=ret_varname,
        argrepr=ret_varname,
        offset=-1,
        starts_line=-1,
        is_jump_target=None,
      )
      load_fast_nodes.append(bytecode_ast.LOAD_FAST(load_fast_instr))
    build_tuple_opname = "BUILD_TUPLE"
    build_tuple_instr = Instruction(
      opcode=dis.opmap[build_tuple_opname],
      opname=build_tuple_opname,
      arg=len(ret_varnames),
      argval=len(ret_varnames),
      argrepr="",
      offset=-1,
      starts_line=-1,
      is_jump_target=None,
    )
    return_value_opname = "RETURN_VALUE"
    return_value_instr = Instruction(
      opcode=dis.opmap[return_value_opname],
      opname=return_value_opname,
      arg=-1,
      argval=None,
      argrepr="",
      offset=-1,
      starts_line=-1,
      is_jump_target=None,
    )
    return_value_node = bytecode_ast.GenericInstructionNode(return_value_instr) 
    return [*backbone, *load_fast_nodes, build_tuple_opname, return_value_node]

  def create_func_make_ast_node(self, func_body, func_name, co_argcount):
    children = []
    def create_load_const_code_obj():
      load_const_opname = "LOAD_CONST"
      load_const_instr = Instruction(
        opcode=dis.opmap[load_const_opname],
        opname=load_const_opname,
        arg=-1,
        argval=None, # put a None as a placeholder. The actual PyCodeObject will be created in later pass.
        argrepr=None,
        offset=-1,
        starts_line=-1,
        is_jump_target=None,
      )
      load_const_node = bytecode_ast.LOAD_CONST(load_const_instr)
      return load_const_node
    children.append(create_load_const_code_obj())
    def create_load_const_func_name():
      load_const_opname = "LOAD_CONST"
      load_const_instr = Instruction(
        opcode=dis.opmap[load_const_opname],
        opname=load_const_opname,
        arg=-1,
        argval="%s.<locals>.%s"%(self.func_name, func_name),
        argrepr="%s.<locals>.%s"%(self.func_name, func_name),
        offset=-1,
        starts_line=-1,
        is_jump_target=None,
      )
      load_const_node = bytecode_ast.LOAD_CONST(load_const_instr)
      return load_const_node
    children.append(create_load_const_func_name())
    def create_make_function_node():
      make_function_opname = "MAKE_FUNCTION"
      make_function_instr = Instruction(
        opcode=dis.opmap[make_function_opname],
        opname=make_function_opname,
        arg=0,
        argval=0,
        argrepr="",
        offset=-1,
        starts_line=-1,
        is_jump_target=None,
      )
      make_function_node = bytecode_ast.GenericInstructionNode(make_function_instr)
      return make_function_node
    children.append(create_make_function_node())
    def create_make_function_expr_node(children):
      make_function_expr_node = bytecode_ast.MakeFunctionExprNode(children)
      make_function_expr_node.function_body = bytecode_ast.StatementListNode(func_body)
      make_function_expr_node.co_argcount = co_argcount
      return make_function_expr_node
    return create_make_function_expr_node(children)

  def create_func_store_ast_node(self, func_make_ast_node, func_name):
    def create_store_fast_node():
      store_fast_opname = "STORE_FAST"
      store_fast_instr = Instruction(
        opcode=dis.opmap[store_fast_opname],
        opname=store_fast_opname,
        arg=-1,
        argval=func_name,
        argrepr=func_name,
        offset=-1,
        starts_line=-1,
        is_jump_target=None,
      )
      store_fast_node = bytecode_ast.STORE_FAST(store_fast_instr)
      return store_fast_node
    store_node = create_store_fast_node()
    def create_func_store_statement_node(store_node):
      func_store_statement_node = bytecode_ast.GenericStoreNode(
        func_make_ast_node, [(store_node,)]
      )
      return func_store_statement_node
    func_store_statement_node = create_func_store_statement_node(store_node)
    return func_store_statement_node

  def create_func_call_ast_node(self, func_name, input_varnames):
    children = []
    def create_load_fast_func_obj_or_input_varnames(var_name):
      load_fast_opname = "LOAD_FAST"
      load_fast_instr = Instruction(
        opcode=dis.opmap[load_fast_opname],
        opname=load_fast_opname,
        arg=func_name,
        argval=func_name,
        argrepr="",
        offset=-1,
        starts_line=-1,
        is_jump_target=None,
      )
      load_fast_node = bytecode_ast.GenericInstructionNode(load_fast_instr)
      return load_fast_node
    children = [
      *children,
      *list(map(create_load_fast_func_obj_or_input_varnames, [func_name, *input_varnames]))
    ]
    def create_call_function_node():
      call_function_opname = 'CALL_FUNCTION'
      call_function_instr = Instruction(
        opcode=dis.opmap[call_function_opname],
        opname=call_function_opname,
        arg=len(input_varnames),
        argval=len(input_varnames),
        argrepr="",
        offset=-1,
        starts_line=-1,
        is_jump_target=None,
      )
      call_function_node = bytecode_ast.GenericInstructionNode(call_function_instr)
      return call_function_node
    children.append(create_call_function_node())
    func_call_expr_node = bytecode_ast.GenericExpressionNode(children)
    return func_call_expr_node

  def create_ret_store_ast_node(self, func_call_ast_node, output_varnames):
    def create_unpack_seq_ast_node():
      unpack_seq_opname = "UNPACK_SEQUENCE"
      unpack_seq_instr = Instruction(
        opcode=dis.opmap[unpack_seq_opname],
        opname=unpack_seq_opname,
        arg=len(output_varnames),
        argval=len(output_varnames),
        argrepr="",
        offset=-1,
        starts_line=-1,
        is_jump_target=None,
      )
      unpack_seq_ast_node = bytecode_ast.GenericInstructionNode(upack_seq_instr)
      return unpack_seq_ast_node
    if len(output_varnames) == 1:
      # no UNPACK_SEQUENCE.
      unpack_seq_expr_node = func_call_ast_node
    else:
      unpack_seq_children = [func_call_ast_node, create_unpack_seq_ast_node()]
      unpack_seq_expr_node = bytecode_ast.GenericExpressionNode(unpack_seq_children)
    def create_store_fast_node(varname):
      store_fast_opname = "STORE_FAST"
      store_fast_instr = Instruction(
        opcode=dis.opmap[store_fast_opname],
        opname=store_fast_opname,
        arg=varname,
        argval=varname,
        argrepr="",
        offset=-1,
        starts_line=-1,
        is_jump_target=None,
      )
      store_fast_node = bytecode_ast.GenericInstructionNode(store_fast_instr)
      return store_fast_node
    store_ast_nodes = list((create_store_fast_node(varname),) for varname in output_varnames)
    def create_statement_ast_node(unpack_seq_expr_node, store_ast_nodes):
      ret_store_ast_node = bytecode_ast.GenericStoreNode(unpack_seq_expr_node, store_ast_nodes)
      return ret_store_ast_node
    ret_store_ast_node = create_statement_ast_node(unpack_seq_expr_node, store_ast_nodes)
    return ret_store_ast_node

  def create_pop_top_ast_node(self, func_call_ast_node):
    def create_pop_top_instr_node():
      pop_top_opname = 'POP_TOP'
      pop_top_instr = Instruction(
        opcode=dis.opmap[pop_top_opname],
        opname=pop_top_opname,
        arg=None,
        argval=None,
        argrepr="",
        offset=-1,
        starts_line=-1,
        is_jump_target=None,
      )
      pop_top_instr_node = bytecode_ast.GenericInstructionNode(pop_top_instr)
      return pop_top_instr_node
    pop_top_instr_node = create_pop_top_instr_node()
    def create_statement_ast_node(pop_top_instr_node):
      pop_top_expr_node = bytecode_ast.GenericStoreNode(
        func_call_ast_node, [(pop_top_instr_node,)]
      )
      return pop_top_expr_node
    pop_top_expr_node = create_statement_ast_node(pop_top_instr_node)
    return pop_top_expr_node


