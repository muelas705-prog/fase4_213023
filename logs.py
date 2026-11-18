
# logs.py
# Registro de eventos y errores del sistema Software FJ

from datetime import datetime

from excepciones import (
    DatosInvalidosError,
    OperacionNoPermitidaError
)


class GestorLogs:

    def __init__(self, archivo="software_fj.log"):

        if not isinstance(archivo, str) or not archivo.strip():
            raise DatosInvalidosError(
                "El nombre del archivo es obligatorio"
            )

        self.__archivo = archivo.strip()

    # Validar mensaje
    def __validar_mensaje(self, mensaje):

        if not isinstance(mensaje, str) or not mensaje.strip():
            raise DatosInvalidosError(
                "El mensaje del registro es obligatorio"
            )

    # Crear registro con fecha y hora
    def __crear_registro(self, tipo, mensaje):

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return f"[{fecha}] {tipo}: {mensaje.strip()}\n"

    # Guardar información en el archivo
    def __guardar(self, registro):

        try:
            with open(
                self.__archivo,
                "a",
                encoding="utf-8"
            ) as archivo:

                archivo.write(registro)

        except OSError as error:
            raise OperacionNoPermitidaError(
                "No fue posible guardar el registro"
            ) from error

    # Registrar evento
    def registrar_evento(self, mensaje):

        self.__validar_mensaje(mensaje)

        registro = self.__crear_registro(
            "EVENTO",
            mensaje
        )

        self.__guardar(registro)

        return "Evento registrado correctamente"

    # Registrar error
    def registrar_error(self, mensaje):

        self.__validar_mensaje(mensaje)

        registro = self.__crear_registro(
            "ERROR",
            mensaje
        )

        self.__guardar(registro)

        return "Error registrado correctamente"

    # Registrar una excepción
    def registrar_excepcion(self, error, contexto=""):

        if not isinstance(error, BaseException):
            raise DatosInvalidosError(
                "El objeto recibido no es una excepción válida"
            )

        detalle = f"{type(error).__name__}: {error}"

        if contexto:
            detalle = f"{contexto} | {detalle}"

        # Registrar la causa original del error
        if error.__cause__ is not None:

            causa = error.__cause__

            detalle += (
                f" | Causa original: "
                f"{type(causa).__name__}: {causa}"
            )

        return self.registrar_error(detalle)

    # Consultar registros
    def consultar_logs(self):

        try:
            with open(
                self.__archivo,
                "r",
                encoding="utf-8"
            ) as archivo:

                return archivo.readlines()

        except FileNotFoundError:
            return []

        except OSError as error:
            raise OperacionNoPermitidaError(
                "No fue posible consultar los registros"
            ) from error

    # Ejecutar operaciones con manejo de excepciones
    def ejecutar_operacion(self, operacion, descripcion):

        try:
            resultado = operacion()

        except Exception as error:

            print("Se presentó un error:", error)

            try:
                self.registrar_excepcion(error, descripcion)

            except Exception as error_log:
                print("No fue posible guardar el error:", error_log)

            return None

        else:

            try:
                self.registrar_evento(
                    descripcion + " completada correctamente"
                )

            except Exception as error_log:
                print("No fue posible guardar el evento:", error_log)

            return resultado

        finally:
            print("Finalizó la operación:", descripcion)
