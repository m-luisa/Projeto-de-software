class Transporte:
    def __init__(self, origem, destino, retrato_horario):
        self.origem = origem
        self.destino = destino
        self.retrato_horario = retrato_horario

    def calcular_diferenca(self):
        return self.retrato_horario.calcular_diferenca()

    #RF4 - polimorfismo
    def calcular_atraso(self):
        raise NotImplementedError

    def exibir_status(self):
        raise NotImplementedError


class Voo(Transporte):
    def __init__(self, origem, destino, retrato_horario, numero_voo):
        super().__init__(origem, destino, retrato_horario)
        self.numero_voo = numero_voo

    def calcular_atraso(self):
        diferenca = self.calcular_diferenca()

        if diferenca <= 15:
            return 0

        return diferenca

    def exibir_status(self):
        atraso = self.calcular_atraso()
        horario = self.retrato_horario.horario_real.strftime("%H:%M")

        if atraso == 0:
            status = "No horário"
        else:
            status = f"Atrasado em {int(atraso)} minutos"

        return f"Voo {self.numero_voo} -> {horario} {status}"


class Onibus(Transporte):
    def __init__(self, origem, destino, retrato_horario, linha_onibus, posicao_onibus=None):
        super().__init__(origem, destino, retrato_horario)
        self.linha_onibus = linha_onibus
        self.posicao_onibus = posicao_onibus

    def calcular_atraso(self):
        diferenca = self.calcular_diferenca()

        if diferenca <= 10:
            return 0

        return diferenca

    def exibir_status(self):
        atraso = self.calcular_atraso()
        horario = self.retrato_horario.horario_real.strftime("%H:%M")

        if atraso == 0:
            status = "No horário"
        else:
            status = f"Atrasado em {int(atraso)} minutos"

        return f"Ônibus {self.linha_onibus} -> {horario} {status}"


class Trem(Transporte):
    def __init__(self, origem, destino, retrato_horario, linha_trem, posicao_trem=None):
        super().__init__(origem, destino, retrato_horario)
        self.linha_trem = linha_trem
        self.posicao_trem = posicao_trem

    def calcular_atraso(self):
        diferenca = self.calcular_diferenca()

        #regra provisoria para trem enquanto a regra definitiva de definir atraso com base na operadora nao é implementada
        if diferenca <= 5:
            return 0

        return diferenca

    def exibir_status(self):
        atraso = self.calcular_atraso()
        horario = self.retrato_horario.horario_real.strftime("%H:%M")

        if atraso == 0:
            status = "No horário"
        else:
            status = f"Atrasado em {int(atraso)} minutos"

        return f"Trem {self.linha_trem} -> {horario} {status}"