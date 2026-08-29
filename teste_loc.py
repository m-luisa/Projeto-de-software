from modelos.localizacao import Localizacao

# Isso deve funcionar normalmente
posicao_valida = Localizacao(-19.92, -43.94)  # Belo Horizonte de verdade
print(f"Posição válida aceita: {posicao_valida.latitude}, {posicao_valida.longitude}")

# Isso deve dar erro controlado
try:
    posicao_invalida = Localizacao(950, 10)
    print("ERRO: isso não deveria ter passado!")
except ValueError as erro:
    print(f"Rejeitado corretamente: {erro}")