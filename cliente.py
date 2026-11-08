
from entidad import Entidad
from excepciones import DatosInvalidosError, ClienteNoEncontradoError


# Clase Cliente heredada de Entidad
class Cliente(Entidad):

    def __init__(self, identificador, nombre, correo, telefono):

        # Inicializar la clase padre
        super().__init__(identificador)

        # Validar nombre
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError("El nombre es obligatorio")

        # Validar correo
        if (not isinstance(correo, str)
                or correo.count("@") != 1
                or "." not in correo.split("@")[-1]):
            raise DatosInvalidosError("El correo no es válido")

        # Validar teléfono
        if (not isinstance(telefono, str)
                or not telefono.isdigit()
                or len(telefono) < 7
                or len(telefono) > 15):
            raise DatosInvalidosError("El teléfono no es válido")

        # Encapsulación de los datos personales
        self.__nombre = nombre.strip()
        self.__correo = correo.strip()
        self.__telefono = telefono.strip()

    # Implementación del método abstracto
    def obtener_informacion(self):
        return (
            f"Identificador: {self._identificador}\n"
            f"Nombre: {self.__nombre}\n"
            f"Correo: {self.__correo}\n"
            f"Teléfono: {self.__telefono}"
        )

    # Métodos de acceso a los atributos privados
    def obtener_nombre(self):
        return self.__nombre

    def obtener_correo(self):
        return self.__correo

    def obtener_telefono(self):
        return self.__telefono


# Clase para administrar los clientes
class GestorClientes:

    def __init__(self):
        # Lista interna de clientes
        self.__clientes = []

    # Registrar un cliente
    def registrar_cliente(self, cliente):

        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError(
                "El objeto recibido no es un cliente válido"
            )

        # Evitar identificadores repetidos
        for existente in self.__clientes:
            if existente.obtener_identificador() == cliente.obtener_identificador():
                raise DatosInvalidosError(
                    "Ya existe un cliente con ese identificador"
                )

        self.__clientes.append(cliente)
        return "Cliente registrado correctamente"

    # Buscar un cliente por identificador
    def buscar_cliente(self, identificador):

        for cliente in self.__clientes:
            if cliente.obtener_identificador() == identificador:
                return cliente

        raise ClienteNoEncontradoError(
            "No se encontró el cliente solicitado"
        )

    # Mostrar todos los clientes
    def listar_clientes(self):

        return [
            cliente.obtener_informacion()
            for cliente in self.__clientes
        ]
