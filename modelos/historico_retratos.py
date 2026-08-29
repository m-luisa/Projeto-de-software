class HistoricoRetratos:
    def __init__(self):
        self._retratos = {} #dicionario vazio

    def registrar(self, id_transporte: str, retrato): #adiciona um retrato novo na pasta certi
        self._retratos.setdefault(id_transporte, []).append(retrato)
    def ultimo(self, id_transporte:str):
        return self._retratos[id_transporte][-1]
    def penultimo(self, id_transporte:str):
        lista = self._retratos.get(id_transporte, [])
        return lista[-2] if len(lista) >= 2 else None

    def mudou(self, id_transporte:str) -> str:
        anterior = self.penultimo(id_transporte)
        if anterior is None:
            return " Nada a comparar ainda"
        diferenca_antes = anterior.calcular_diferenca()
        diferenca_agora = self.ultimo(id_transporte).calcular_diferenca()

        if diferenca_antes == diferenca_agora:
            return "Não houve mudanças no horário"
        
        return f"Atraso passou de {int(diferenca_antes)}minutos para {int (diferenca_agora)} minutos."