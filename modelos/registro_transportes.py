#RF9 - deduplicação de buscas
#Vai guardar os transportes ja vistos em um dicionario indexado pela chave de identificação de cada um deles 
class RegistroTransportes:
    def __init__(self):
        #encapsulamento - dicionario protegido, so podeser manipulado pelosmétodos públicos dessa classe
        self._registros = {}
    def registrar(self, transporte) -> bool:
        #rf9 -  a chave vai vir de cada objeto(polimorifsmo), se a chave ja existir, o registro antigo vai ser substituido pelo mais recente, sem duplicar
        chave = transporte.chave_identificacao()
        era_novo = chave not in self._registros
        self ._registros[chave] = transporte
        return era_novo
    def listar(self) -> list:
        return list(self._registros.values())
    def quantidade(self) -> int:
        return len(self._registros)