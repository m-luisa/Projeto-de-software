class Viagem: 
    def __init__(self, trechos:list):
        self.trechos = trechos
    
    def atraso_total(self) -> float:
        return sum(trecho.calcular_atraso() for trecho in self.trechos) #qqui vai chamar o metodo calcular_atraso de todos os trechos da lista, o calcular atraso utiliza o metodo proprio de cada trecho de cada um dos modais

    def exibir_status(self) -> str:
        linhas = [trecho.exibir_status() for trecho in self.trechos]
        linhas.append(f"Atraso acumulado da viagem: {int(self.atraso_total())} minutos")
        return "\n".join(linhas) #vai juntar todos os status dos trechos em uma string so
        