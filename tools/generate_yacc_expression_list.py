print("class BytecodeYaccExpressionList:\n")
print("    def p_expression_list_1(self, p):\n        'expression_list_1 : expression'\n        p[0] = [p[1]]\n")
for i in range(2, 64):
  print(f"    def p_expression_list_{i}(self, p):\n        'expression_list_{i} : expression_list_{i-1} expression'\n        p[0] = [p[2], *p[1]]\n")
