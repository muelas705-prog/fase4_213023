
# Excepción general del sistema
class SoftwareFJError(Exception):
    pass


# Error cuando los datos son incorrectos
class DatosInvalidosError(SoftwareFJError):
    pass


# Error cuando un cliente no existe
class ClienteNoEncontradoError(SoftwareFJError):
    pass


# Error cuando un servicio no está disponible
class ServicioNoDisponibleError(SoftwareFJError):
    pass


# Error cuando una reserva no es válida
class ReservaInvalidaError(SoftwareFJError):
    pass


# Error cuando se intenta realizar
# una operación no permitida
class OperacionNoPermitidaError(SoftwareFJError):
    pass
