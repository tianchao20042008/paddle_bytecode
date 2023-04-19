import dis
import ply.lex as lex
import ply.yacc as yacc
from bytecode_lexer_token import BytecodeLexerToken
from bytecode_yacc_basic_expression import BytecodeYaccBasicExpression
from bytecode_yacc_load_expression import BytecodeYaccLoadExpression
from bytecode_yacc_store import BytecodeYaccStore
from bytecode_yacc_builtin_call import BytecodeYaccBuiltinCall
from bytecode_yacc_expression_list import BytecodeYaccExpressionList
from bytecode_yacc_if_statement import BytecodeYaccIfStatement
from paddle_bytecode import bytecode_ast
from paddle_bytecode import instr_stack_util

class BytecodeParser(BytecodeLexerToken,
                     BytecodeYaccBasicExpression,
                     BytecodeYaccLoadExpression,
                     BytecodeYaccBuiltinCall,
                     BytecodeYaccExpressionList,
                     BytecodeYaccIfStatement,
                     BytecodeYaccStore):
    t_ignore = (" \t\r\n")

    def __init__(self, **kwargs) -> None:
        self.init()
        self.create_expr = ExprCreator()

    def init(self):
        self.instruction_index = 0
        self.instructions = dict()
        self.target_offset2num_jump = dict()

    def parse_token(self, t):
        t.value = self.instructions[self.instruction_index]
        self.instruction_index += 1
        return t

    def t_error(self, t: lex.LexToken) -> lex.LexToken:
        print(f"Illegal character '{t.value}' in {t.lineno}:{t.lexpos}")
        t.lexer.skip(1)

    def parse_load_expression(self, instruction):
        return self.convert_to_instruction_node(instruction)

    def parse_basic_expression(self, children, instruction):
        instruction_node = self.convert_to_instruction_node(instruction)
        return self.create_expr(bytecode_ast.GenericExpressionNode([*children, instruction_node]))

    def parse_store(self, exprs, store_instruction):
        return (*exprs, self.convert_to_instruction_node(store_instruction))

    def convert_to_instruction_node(self, instruction):
      if hasattr(bytecode_ast, instruction.opname):
        cls = getattr(bytecode_ast, instruction.opname)
      elif instr_stack_util.is_jump_instruction(instruction):
        cls = bytecode_ast.GenericJumpNode
      else:
        cls = bytecode_ast.GenericInstructionNode
      return cls(instruction)

    def p_program_0(self, p):
        'program : statement_list'
        p[0] = bytecode_ast.Program([p[1]])

    def p_statement_list_terminal(self, p):
        'statement_list : statement'
        p[0] = bytecode_ast.StatementListNode([p[1]])

    def p_statement_list(self, p):
        'statement_list : statement_list statement'
        p[1].children = [p[2], *p[1].children]
        p[0] = p[1]

    def p_statement_store_one_value(self, p):
        'statement : store expression'
        p[0] = bytecode_ast.GenericStoreNode(p[2], [p[1]])

    def p_unpack_expression_out_2(self, p):
        'unpack_expression : ROT_TWO expression expression'
        rot_two_node = bytecode_ast.GenericInstructionNode(p[1])
        p[0] = bytecode_ast.GenericExpressionNode([p[3], p[2], rot_two_node])
  
    def p_unpack_expression_out_3(self, p):
        'unpack_expression : ROT_TWO ROT_THREE expression expression expression'
        rot_three_node = bytecode_ast.GenericInstructionNode(p[2])
        rot_three_expr = bytecode_ast.GenericExpressionNode([p[5], p[4], p[3], rot_three_node])
        rot_two_node = bytecode_ast.GenericInstructionNode(p[1])
        p[0] = bytecode_ast.GenericExpressionNode([rot_three_expr, rot_two_node])

    def p_unpack_expression_out_4(self, p):
        'unpack_expression : ROT_TWO ROT_THREE ROT_FOUR expression expression expression expression'
        rot_four_node = bytecode_ast.GenericInstructionNode(p[3])
        rot_three_node = bytecode_ast.GenericInstructionNode(p[2])
        rot_two_node = bytecode_ast.GenericInstructionNode(p[1])
        rot_four_expr = bytecode_ast.GenericExpressionNode([p[7], p[6], p[5], p[4], rot_four_node])
        rot_three_expr = bytecode_ast.GenericExpressionNode([rot_four_expr, rot_three_node])
        rot_two_expr = bytecode_ast.GenericExpressionNode([rot_three_expr, rot_two_node])
        p[0] = rot_two_expr

    def p_unpack_expression_unpack_sequence(self, p):
        'unpack_expression : UNPACK_SEQUENCE expression'
        unpack_seq_node = bytecode_ast.GenericInstructionNode(p[1])
        p[0] = bytecode_ast.GenericExpressionNode([p[2], unpack_seq_node])

    def p_unpack_expression_unpack_EX(self, p):
        'unpack_expression : UNPACK_EX expression'
        unpack_ex_node = bytecode_ast.GenericInstructionNode(p[1])
        p[0] = bytecode_ast.GenericExpressionNode([p[2], unpack_ex_node])

    def p_statement_unpack_expression(self, p):
        'statement : store_list unpack_expression'
        p[0] = bytecode_ast.GenericStoreNode(p[2], p[1])
  
    def p_statement_return(self, p):
        'statement : RETURN_VALUE expression'
        return_node = bytecode_ast.GenericInstructionNode(p[1])
        p[0] = bytecode_ast.ReturnValueNode(p[2], [(return_node,)])

    def get_token_strs(self, instruction):
        if instruction.opname in {"CALL_FUNCTION", "BUILD_MAP", "BUILD_LIST", "BUILD_TUPLE"}:
            yield f"ARG{instruction.arg}"
        yield instruction.opname
        if instruction.is_jump_target:
          for _ in range(self.target_offset2num_jump[instruction.offset]):
            yield "LABEL"

    def update_target_offset2num_jump(self):
        for instr in self.instructions:
            if not instr_stack_util.is_jump_instruction(instr):
                continue
            if instr.argval not in self.target_offset2num_jump:
                self.target_offset2num_jump[instr.argval] = 0
            self.target_offset2num_jump[instr.argval] += 1

    def parse(self, f):
        self.init()
        self.instructions = list(dis.get_instructions(f))[::-1]
        self.update_target_offset2num_jump()
        lexer = lex.lex(module=self)
        parser = yacc.yacc(module=self, start='program')
        tokens = [t for i in self.instructions for t in self.get_token_strs(i)]
        #print("\n".join(tokens))
        return parser.parse("\n".join(tokens))


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


if __name__ == "__main__":
    def foo():
        a = 30 * 40
        c, d = bar, cd
        c[30], d.b, e.c = bar, cd, nice
        if cond:
            b = 30 / 40
        else:
            if cond:
                if cond:
                    e = 50
            else:
                d = 50
        return a + 30 * bar(bar(), bar(bar()))
    parser = BytecodeParser()
    from paddle_bytecode.print_transform import PrintTransform
    print('-'*100)
    dis.dis(foo)
    print('-'*100)
    PrintTransform()(parser.parse(foo))
    print('-'*100)

