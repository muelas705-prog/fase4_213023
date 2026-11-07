print("actividad colaborativa grupo 213023")
print("universidad abierta y a distancia")
# tarea 4 grupo 213023
from abc import ABC, abstractmethod

# Clase abstracta general del sistema Software FJ
class Entidad(ABC):

    def __init__(self, identificador):

        # Validar que exista un identificador
        if not isinstance(identificador, str) or not identificador.strip():
            raise ValueError("El identificador es obligatorio")

        # Atributo protegido
        self._identificador = identificador.strip()

    # Método abstracto: obliga a las clases hijas
    # a implementar su propia información
    @abstractmethod
    def obtener_informacion(self):
        pass

    # Método para consultar el identificador
    def obtener_identificador(self):
        return self._identificador
