print("class BytecodeYaccBuiltinCall:\n")

for i in range(1, 64):
    print(f"    def p_call_function_arg_{i-1}(self, p):")
    print(f"        'expression : ARG{i-1} CALL_FUNCTION expression_list_{i}'")
    print(f"        p[0] = self.parse_basic_expression(p[3], p[2])")
    print(f"")

print(f"    def p_build_tuple_0(self, p):")
print(f"        'expression : ARG0 BUILD_TUPLE'")
print(f"        p[0] = self.parse_basic_expression([], p[2])")
print(f"")

print(f"    def p_build_map_0(self, p):")
print(f"        'expression : ARG0 BUILD_MAP'")
print(f"        p[0] = self.parse_basic_expression([], p[2])")
print(f"")

print(f"    def p_build_list_0(self, p):")
print(f"        'expression : ARG0 BUILD_LIST'")
print(f"        p[0] = self.parse_basic_expression([], p[2])")
print(f"")

print(f"    def p_build_set_0(self, p):")
print(f"        'expression : ARG0 BUILD_SET'")
print(f"        p[0] = self.parse_basic_expression([], p[2])")
print(f"")
for i in range(1, 64):
    print(f"    def p_build_tuple_{i}(self, p):")
    print(f"        'expression : ARG{i} BUILD_TUPLE expression_list_{i}'")
    print(f"        p[0] = self.parse_basic_expression(p[3], p[2])")
    print(f"")

    print(f"    def p_build_map_{i}(self, p):")
    print(f"        'expression : ARG{i} BUILD_MAP expression_list_{i}'")
    print(f"        p[0] = self.parse_basic_expression(p[3], p[2])")
    print(f"")

    print(f"    def p_build_list_{i}(self, p):")
    print(f"        'expression : ARG{i} BUILD_LIST expression_list_{i}'")
    print(f"        p[0] = self.parse_basic_expression(p[3], p[2])")
    print(f"")

    print(f"    def p_build_set_{i}(self, p):")
    print(f"        'expression : ARG{i} BUILD_SET expression_list_{i}'")
    print(f"        p[0] = self.parse_basic_expression(p[3], p[2])")
    print(f"")
