"""
rf1 - localizações validadas
Essa classe vai validar as coordenadas geográficas de forma a ser inviável a criação de objetos com localizações que não existem

Encapsulamento - __latitude e __longitude são atributos privados e não existem setters, ou seja, depois de criado o objeto não pode ser alterado
Tratamento de erro: TypeError quando os valores não são números e ValueError quando estão fora dos parametros de coordenadas válidas

 """
class Localizacao:
    def __init__(self,latitude,longitude):
        #rf1
        if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
            raise TypeError(
                f"Latitude e longitude devem ser numéricas, recebido: "
                f"{type(latitude).__name__}, {type(longitude).__name__}."
            )
        if latitude < -90 or latitude > 90:
            raise ValueError("Latitude inválida.")
        if longitude < -180 or longitude > 180:
            raise ValueError("Longitude inválida.")
        #encapsulamento: atributos privados, so sao expostos por @property
        self.__latitude = latitude
        self.__longitude = longitude

        
    @property
    def latitude(self):
        return self.__latitude
    @property
    def longitude(self):
        return self.__longitude
    