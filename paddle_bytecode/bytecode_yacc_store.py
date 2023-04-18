class BytecodeYaccStore:

    def p_POP_TOP(self, p):
        'store : POP_TOP'
        p[0] = self.parse_store([], p[1])

    def p_STORE_GLOBAL(self, p):
        'store : STORE_GLOBAL'
        p[0] = self.parse_store([], p[1])

    def p_STORE_FAST(self, p):
        'store : STORE_FAST'
        p[0] = self.parse_store([], p[1])

    def p_STORE_NAME(self, p):
        'store : STORE_NAME'
        p[0] = self.parse_store([], p[1])

    def p_STORE_DEREF(self, p):
        'store : STORE_DEREF'
        p[0] = self.parse_store([], p[1])

    def p_STORE_ATTR(self, p):
        'store : STORE_ATTR expression'
        p[0] = self.parse_store([p[2]], p[1])

    def p_STORE_SUBSCR(self, p):
        'store : STORE_SUBSCR expression expression'
        p[0] = self.parse_store([p[3], p[2]], p[1])

    def p_store_list_terminal(self, p):
        'store_list : store'
        p[0] = [p[1]]

    def p_store_list(self, p):
        'store_list : store_list store'
        p[0] = [p[2], *p[1]]
