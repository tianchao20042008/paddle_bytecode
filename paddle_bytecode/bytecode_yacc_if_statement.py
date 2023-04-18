from paddle_bytecode import bytecode_ast

class BytecodeYaccIfStatement:

    def p_if_false(self, p):
        'statement : LABEL statement_list POP_JUMP_IF_FALSE expression'
        cond_jump_node = self.convert_to_instruction_node(p[3])
        p[0] = bytecode_ast.IfStatementNode(p[4], cond_jump_node, p[2])

    def p_if_true(self, p):
        'statement : LABEL statement_list POP_JUMP_IF_TRUE expression'
        cond_jump_node = self.convert_to_instruction_node(p[3])
        p[0] = bytecode_ast.IfStatementNode(p[4], cond_jump_node, p[2])

    def p_if_false_else(self, p):
        'statement : LABEL statement_list LABEL JUMP_FORWARD statement_list POP_JUMP_IF_FALSE expression'
        cond_jump_node = self.convert_to_instruction_node(p[6])
        jump_fw_node = self.convert_to_instruction_node(p[4])
        p[0] = bytecode_ast.IfElseStatementNode(p[7], cond_jump_node, p[5], jump_fw_node, p[2])

    def p_if_true_else(self, p):
        'statement : LABEL statement_list LABEL JUMP_FORWARD statement_list POP_JUMP_IF_TRUE expression'
        cond_jump_node = self.convert_to_instruction_node(p[6])
        jump_fw_node = self.convert_to_instruction_node(p[4])
        p[0] = bytecode_ast.IfElseStatementNode(p[7], cond_jump_node, p[5], jump_fw_node, p[2])

