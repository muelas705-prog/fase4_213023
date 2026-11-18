
# reservas.py
# Gestión de reservas del sistema Software FJ

from datetime import datetime

from entidad import Entidad
from cliente import Cliente
from servicios import Servicio, IVA

from excepciones import (
    DatosInvalidosError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    OperacionNoPermitidaError
)


class Reserva(Entidad):

    def __init__(self, identificador, cliente, servicio, fecha,
                 duracion, impuesto=IVA, descuento=0):

        super().__init__(identificador)

        # Validar cliente
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("El cliente no es válido")

        # Validar servicio
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("El servicio no es válido")

        # Validar fecha
        if not isinstance(fecha, str) or not fecha.strip():
            raise DatosInvalidosError("La fecha es obligatoria")

        fecha = fecha.strip()

        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError as error:
            raise DatosInvalidosError(
                "La fecha debe tener el formato AAAA-MM-DD"
            ) from error

        # Validar duración
        if (isinstance(duracion, bool)
                or not isinstance(duracion, (int, float))
                or duracion <= 0):
            raise DatosInvalidosError(
                "La duración debe ser mayor que cero"
            )

        # Validar impuesto y descuento
        for valor, nombre in (
            (impuesto, "El impuesto"),
            (descuento, "El descuento")
        ):
            if (isinstance(valor, bool)
                    or not isinstance(valor, (int, float))
                    or not 0 <= valor <= 1):
                raise DatosInvalidosError(
                    nombre + " debe estar entre 0 y 1"
                )

        # Calcular el costo de la reserva
        self.__costo = servicio.calcular_costo(
            duracion,
            impuesto=impuesto,
            descuento=descuento
        )

        self.__cliente = cliente
        self.__servicio = servicio
        self.__fecha = fecha
        self.__duracion = duracion
        self.__estado = "Pendiente"
        self.__registrada = False

    # Obtener información de la reserva
    def obtener_informacion(self):
        return (
            f"Identificador: {self._identificador}\n"
            f"Cliente: {self.__cliente.obtener_nombre()}\n"
            f"Servicio: {self.__servicio.obtener_identificador()}\n"
            f"Descripción: {self.__servicio.obtener_informacion()}\n"
            f"Fecha: {self.__fecha}\n"
            f"Duración: {self.__duracion} horas\n"
            f"Costo: ${self.__costo:,.2f}\n"
            f"Estado: {self.__estado}"
        )

    # Métodos de consulta
    def obtener_cliente(self):
        return self.__cliente

    def obtener_servicio(self):
        return self.__servicio

    def obtener_fecha(self):
        return self.__fecha

    def obtener_duracion(self):
        return self.__duracion

    def obtener_costo(self):
        return self.__costo

    def obtener_estado(self):
        return self.__estado

    def esta_registrada(self):
        return self.__registrada

    # Marcar como registrada
    def _marcar_registrada(self):
        if self.__registrada:
            raise ReservaInvalidaError(
                "La reserva ya fue registrada"
            )

        self.__registrada = True

    # Confirmar reserva
    def confirmar(self):
        if not self.__registrada:
            raise OperacionNoPermitidaError(
                "Primero debe registrar la reserva"
            )

        if self.__estado != "Pendiente":
            raise OperacionNoPermitidaError(
                "Solo se pueden confirmar reservas pendientes"
            )

        self.__estado = "Confirmada"
        return "Reserva confirmada correctamente"

    # Cancelar reserva
    def cancelar(self):
        if not self.__registrada:
            raise OperacionNoPermitidaError(
                "La reserva no está registrada"
            )

        if self.__estado not in ("Pendiente", "Confirmada"):
            raise OperacionNoPermitidaError(
                "No se puede cancelar esta reserva"
            )

        self.__servicio.cambiar_disponibilidad(True)
        self.__estado = "Cancelada"

        return "Reserva cancelada correctamente"

    # Procesar reserva
    def procesar(self):
        if not self.__registrada:
            raise OperacionNoPermitidaError(
                "Primero debe registrar la reserva"
            )

        if self.__estado != "Confirmada":
            raise OperacionNoPermitidaError(
                "La reserva debe estar confirmada"
            )

        self.__estado = "Procesada"
        self.__servicio.cambiar_disponibilidad(True)

        return "Reserva procesada correctamente"


class GestorReservas:

    def __init__(self, gestor_clientes):

        if not callable(
            getattr(gestor_clientes, "buscar_cliente", None)
        ):
            raise DatosInvalidosError(
                "Se necesita un gestor de clientes válido"
            )

        self.__reservas = []
        self.__gestor_clientes = gestor_clientes

    # Registrar reserva
    def registrar_reserva(self, reserva):

        if not isinstance(reserva, Reserva):
            raise DatosInvalidosError(
                "El objeto recibido no es una reserva válida"
            )

        if reserva.esta_registrada():
            raise ReservaInvalidaError(
                "La reserva ya fue registrada"
            )

        # Comprobar identificador duplicado
        for existente in self.__reservas:
            if existente.obtener_identificador() == reserva.obtener_identificador():
                raise ReservaInvalidaError(
                    "Ya existe una reserva con ese identificador"
                )

        # Comprobar que el cliente esté registrado
        cliente = reserva.obtener_cliente()

        cliente_registrado = self.__gestor_clientes.buscar_cliente(
            cliente.obtener_identificador()
        )

        if cliente_registrado is not cliente:
            raise DatosInvalidosError(
                "El cliente no corresponde al registro existente"
            )

        # Comprobar disponibilidad del servicio
        servicio = reserva.obtener_servicio()

        if not servicio.esta_disponible():
            raise ServicioNoDisponibleError(
                "El servicio no está disponible"
            )

        servicio.validar_parametros(reserva.obtener_duracion())

        # Registrar la reserva y bloquear el servicio
        self.__reservas.append(reserva)

        try:
            servicio.cambiar_disponibilidad(False)
            reserva._marcar_registrada()

        except Exception:
            self.__reservas.remove(reserva)
            servicio.cambiar_disponibilidad(True)
            raise

        return "Reserva registrada correctamente"

    # Buscar reserva
    def buscar_reserva(self, identificador):

        if not isinstance(identificador, str) or not identificador.strip():
            raise DatosInvalidosError(
                "El identificador de reserva es obligatorio"
            )

        identificador = identificador.strip()

        for reserva in self.__reservas:
            if reserva.obtener_identificador() == identificador:
                return reserva

        raise ReservaInvalidaError(
            "No se encontró la reserva solicitada"
        )

    # Confirmar reserva
    def confirmar_reserva(self, identificador):
        reserva = self.buscar_reserva(identificador)
        return reserva.confirmar()

    # Cancelar reserva
    def cancelar_reserva(self, identificador):
        reserva = self.buscar_reserva(identificador)
        return reserva.cancelar()

    # Procesar reserva
    def procesar_reserva(self, identificador):
        reserva = self.buscar_reserva(identificador)
        return reserva.procesar()

    # Listar reservas
    def listar_reservas(self):
        return [
            reserva.obtener_informacion()
            for reserva in self.__reservas
        ]
