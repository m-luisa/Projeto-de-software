from aviationstack_usuario import AviationStack

cliente = AviationStack()
voo = cliente.buscar_voo("SQ8451")  #troca por um código de voo real e ativo
print(voo)