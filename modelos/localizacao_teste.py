from localizacao import Localizacao

try:
    Localizacao("40.5", 10)
    print("ERRO: deveria ter lançado TypeError")
except TypeError:
    print("OK: TypeError para tipo inválido")

try:
    Localizacao(91, 10)
    print("ERRO: deveria ter lançado ValueError")
except ValueError:
    print("OK: ValueError para latitude fora do intervalo")

try:
    Localizacao(10, 200)
    print("ERRO: deveria ter lançado ValueError")
except ValueError:
    print("OK: ValueError para longitude fora do intervalo")