from modelos import retrato_horario
"""
rf2 - historico de retratos

cada busca gera um novo retrato_horario (que é imutavel) e esse historico vai acumular esses restratos numa lista por transporte, sem sobrescrever nem alterar o retrato ja registrado
vai ser usado para possibilitar comparar o que mudou entre os retratos
"""
class HistoricoRetratos:
    def __init__(self):
        self._retratos = {} #lista de retratos - id_transporte

    def registrar(self, id_transporte: str, retrato): 
        #rf2: so adiciona o novo retrato ao final da lista
        self._retratos.setdefault(id_transporte, []).append(retrato)
    def ultimo(self, id_transporte:str):
        #tratamento de erro
        try:
            return self._retratos[id_transporte][-1]
        except KeyError as erro:
            raise KeyError(f"Nenhum retrato registrado para o transporte '{id_transporte}'") from erro
        except IndexError as erro:
            raise IndexError(f"Histórico de '{id_transporte}' está vazio") from erro
            
    def penultimo(self, id_transporte:str):
        lista = self._retratos.get(id_transporte, [])
        return lista[-2] if len(lista) >= 2 else None

    def mudou(self, id_transporte:str) -> str:
        #rf2 - compara dois retratos distintos e imultaveis, o penultimo e o ultimo para relatar o que mudou entre as buscas
        anterior = self.penultimo(id_transporte)
        if anterior is None:
            return " Nada a comparar ainda"
        diferenca_antes = anterior.calcular_diferenca()
        diferenca_agora = self.ultimo(id_transporte).calcular_diferenca()

        if diferenca_antes == diferenca_agora:
            return "Não houve mudanças no horário"
        
        return f"Atraso passou de {int(diferenca_antes)}minutos para {int (diferenca_agora)} minutos."