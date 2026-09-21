#rf6 - viagens com multiplos trechos - nesse requisito funcional a chegada ou atraso geral da viagem é calculada identificando individualmente o atraso de cda trecho, aqui não é verificado qual é o tipo de trecho, apenas chama os métodos e cada modal aplica a própria regra de atraso

class Viagem: 
    def __init__(self, trechos:list):
        #tratamento de erro
        if not trechos:
            raise ValueError("A viagem precisa de pelo menos um trecho (voo, ônibus ou trem).")
        self.trechos = trechos
    
    def atraso_total(self) -> float:
        #rf6: soma o atraso de cada trecho chamando o método de cada um dos modais
        return sum(trecho.calcular_atraso() for trecho in self.trechos) 

    def exibir_status(self) -> str:
        linhas = [trecho.exibir_status() for trecho in self.trechos]
        linhas.append(f"Atraso acumulado da viagem: {int(self.atraso_total())} minutos")
        return "\n".join(linhas) 
        