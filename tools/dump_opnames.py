import dis

for opname, _ in dis.opmap.items():
  print(opname)
