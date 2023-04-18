class BytecodeYaccLoadExpression:

    def p_LOAD_GLOBAL(self, p):
        'expression : LOAD_GLOBAL'
        p[0] = self.parse_load_expression(p[1])

    def p_LOAD_CONST(self, p):
        'expression : LOAD_CONST'
        p[0] = self.parse_load_expression(p[1])

    def p_LOAD_FAST(self, p):
        'expression : LOAD_FAST'
        p[0] = self.parse_load_expression(p[1])

    def p_LOAD_NAME(self, p):
        'expression : LOAD_NAME'
        p[0] = self.parse_load_expression(p[1])

    def p_LOAD_DEREF(self, p):
        'expression : LOAD_DEREF'
        p[0] = self.parse_load_expression(p[1])

    def p_LOAD_ATTR(self, p):
        'expression : LOAD_ATTR expression'
        p[0] = self.parse_basic_expression([p[2]], p[1])

