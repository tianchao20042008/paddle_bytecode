import dis
import paddle_bytecode.instr_stack_util as instr_stack_util

def is_instruction_arg_none(opname):
  try:
    dis.stack_effect(dis.opmap[opname], None)
  except:
    return False
  return True

print("# Do not edit directly. This file is generated by tools/generate_yacc_basic_expression_class.py")
print("class BytecodeYaccBasicExpression:\n")

for opname,output_num_or_f in instr_stack_util.opname2output_num_or_f.items():
  if type(output_num_or_f) is not int:
    continue
  output_num = output_num_or_f
  if output_num != 1:
    continue
  if not is_instruction_arg_none(opname):
    continue
  input_num = output_num - dis.stack_effect(dis.opmap[opname], None)
  if input_num == 0:
    continue
  assert output_num == 1
  assert input_num > 0
  print(f"    def p_basic_expression_{opname}(self, p):\n        'expression : expression_list {opname}'\n        p[0] = self.parse_basic_expression(p[1], p[2])\n\n")
