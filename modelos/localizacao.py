
"""
implementação do requisito funcional
a classe Localizacao encapsula latitude e longitude usando atributos privados, impede que uma localização inválida seja criada."""
class Localizacao:
    def __init__(self,latitude,longitude):
        if latitude < -90 or latitude > 90:
            raise ValueError("Latitude inválida.")

        if longitude < -180 or longitude > 180:
            raise ValueError("Longitude inválida.")

        self.__latitude = latitude
        self.__longitude = longitude

    @property
    def latitude(self):
        return self.__latitude
    @property
    def longitude(self):
        return self.__longitude
    