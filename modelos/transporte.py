"""
rf3 - multiplos modais de transporte

trasporte é a classe base
voo, onibus e trem herdam dela e cada um deles vai sobrescrever os metodos calcular_atraso, exibir_status e identificador_unico com a logica de cada modal

"""

class Transporte:
    def __init__(self, origem, destino, retrato_horario):
        self.origem = origem
        self.destino = destino
        self.retrato_horario = retrato_horario

    def calcular_diferenca(self):
        return self.retrato_horario.calcular_diferenca()
        #delega para retrato_horario o calculo da diferença, a interpretação do resultado vai ser função de cada uma das classes

    #as subclasses devem sobrescrever esses métodos, caso não o façam o erro aparece quando o método for chamado
    def calcular_atraso(self):
        raise NotImplementedError 

    def exibir_status(self):
        raise NotImplementedError

    #RF9-duplicação de buscas usando polimorfismo - cada modal deve saber qual seu identificador, o que permite deduplicar buscas repetidas
    def identificador_unico(self):
        raise NotImplementedError   

    #combina o tipo concreto com o identificdor do modal, forma a chave usada pelo RegistroTransportes pra reconhecer os transportes
    def chave_identificacao(self) -> str:
        return f"{type(self).__name__}:{self.identificador_unico()}"

class Voo(Transporte):
    def __init__(self, origem, destino, retrato_horario, numero_voo): #herança: reaproveita o __init__ da classe base
        super().__init__(origem, destino, retrato_horario)
        self.numero_voo = numero_voo
    
    #rf3 regra do atraso específico do modal
    def calcular_atraso(self):
        diferenca = self.calcular_diferenca()
        if diferenca <= 15:
            return 0 
        else:
            #tolerancia de 15min
            return diferenca 

    #polimorfismo: mesma assinatura de onibus e trem mas com texto de saída para o voo
    def exibir_status(self):
        atraso = self.calcular_atraso()
        horario = self.retrato_horario.horario_real.strftime("%H:%M")
        if atraso == 0:
            status = "No horário"  
        else:
            status = f"Atrasado em {int(atraso)} minutos"
        return f"Voo {self.numero_voo} ({self.origem} -> {self.destino}) -> {horario} {status}"
 

    def identificador_unico(self):
        return self.numero_voo   

class Onibus(Transporte):
    def __init__(self, origem, destino, retrato_horario, linha_onibus, identificador=None):
        super().__init__(origem, destino, retrato_horario)
        self.linha_onibus = linha_onibus
        if identificador is not None:
            self.identificador = identificador  
        else:
            self.identificador = linha_onibus

    def calcular_atraso(self):
        diferenca = self.calcular_diferenca()
        if diferenca <= 10:
            return 0 
        else:
            return diferenca

    def exibir_status(self):
        atraso = self.calcular_atraso()
        horario = self.retrato_horario.horario_real.strftime("%H:%M")
        if atraso == 0:
            status = "No horário"
        else:
            status = f"Atrasado em {int(atraso)} minutos"
        return f"Ônibus {self.linha_onibus} -> {horario} {status}"

    def identificador_unico(self):
        return self.identificador 

class Trem(Transporte):
    def __init__(self, origem, destino, retrato_horario, linha_trem, status_operadora, operacao_normal=True, identificador=None):
        super().__init__(origem, destino, retrato_horario)
        self.linha_trem = linha_trem
        self.status_operadora = status_operadora
        if identificador is not None:
            self.identificador = identificador 
        else:
            self.identificador = linha_trem

    def calcular_atraso(self):
        return 0 if self.status_operadora == "no horário" else 1

    def exibir_status(self):
        return f"Trem {self.linha_trem} -> {self.origem} → {self.destino}: {self.status_operadora}"

    def identificador_unico(self):
        return self.identificador