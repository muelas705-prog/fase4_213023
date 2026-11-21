
# main.py
# Sistema Integral de Gestión de Clientes, Servicios y Reservas
# Empresa Software FJ

# Importación de los módulos del proyecto

from cliente import Cliente, GestorClientes

from servicios import (
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada
)

from reservas import Reserva, GestorReservas
from logs import GestorLogs

from excepciones import SoftwareFJError


# ==========================================
# INICIALIZACIÓN DEL SISTEMA
# ==========================================

gestor_clientes = GestorClientes()
gestor_reservas = GestorReservas(gestor_clientes)
gestor_logs = GestorLogs()


# Crear los servicios disponibles

servicios = {
    "SAL001": ReservaSala(
        "SAL001",
        "Sala de reuniones",
        50000,
        20
    ),

    "EQU001": AlquilerEquipo(
        "EQU001",
        "Proyector HD",
        20000,
        "Audiovisual"
    ),

    "ASE001": AsesoriaEspecializada(
        "ASE001",
        "Asesoria tecnologica",
        80000,
        "Computacion en la nube"
    )
}


# ==========================================
# CONTROL DE OPERACIONES Y EXCEPCIONES
# ==========================================

def ejecutar_operacion(operacion, descripcion):

    try:
        resultado = operacion()

    except SoftwareFJError as error:

        print("\nError controlado:", error)

        try:
            gestor_logs.registrar_excepcion(
                error,
                descripcion
            )
        except Exception as error_log:
            print("Error al guardar el registro:", error_log)

    except Exception as error:

        print("\nError inesperado:", error)

        try:
            gestor_logs.registrar_excepcion(
                error,
                descripcion
            )
        except Exception as error_log:
            print("Error al guardar el registro:", error_log)

    else:

        if resultado is not None:
            print("\n", resultado)

        try:
            gestor_logs.registrar_evento(
                descripcion + " realizada correctamente"
            )
        except Exception as error_log:
            print("Error al guardar el evento:", error_log)

    finally:
        print("\nFinalizó la operación.")


# ==========================================
# REGISTRO DE CLIENTES
# ==========================================

def registrar_cliente():

    identificador = input("Identificador del cliente: ")
    nombre = input("Nombre completo: ")
    correo = input("Correo electronico: ")
    telefono = input("Telefono: ")

    cliente = Cliente(
        identificador,
        nombre,
        correo,
        telefono
    )

    return gestor_clientes.registrar_cliente(cliente)


# ==========================================
# CONSULTAR CLIENTES
# ==========================================

def listar_clientes():

    clientes = gestor_clientes.listar_clientes()

    if not clientes:
        print("No hay clientes registrados.")
        return

    for cliente in clientes:
        print("\n", cliente)
        print("-" * 40)


# ==========================================
# CONSULTAR SERVICIOS
# ==========================================

def listar_servicios():

    print("\nSERVICIOS DISPONIBLES")

    for servicio in servicios.values():

        print("\n", servicio.obtener_informacion())

        if servicio.esta_disponible():
            print("Estado: Disponible")
        else:
            print("Estado: No disponible")


# ==========================================
# CREAR RESERVAS
# ==========================================

def crear_reserva():

    identificador = input("Identificador de la reserva: ")

    identificador_cliente = input(
        "Identificador del cliente: "
    )

    identificador_servicio = input(
        "Codigo del servicio (SAL001, EQU001, ASE001): "
    )

    if identificador_servicio not in servicios:
        raise SoftwareFJError(
            "El servicio seleccionado no existe"
        )

    cliente = gestor_clientes.buscar_cliente(
        identificador_cliente
    )

    servicio = servicios[identificador_servicio]

    fecha = input("Fecha de reserva (AAAA-MM-DD): ")

    duracion = float(
        input("Duracion en horas: ")
    )

    reserva = Reserva(
        identificador,
        cliente,
        servicio,
        fecha,
        duracion
    )

    return gestor_reservas.registrar_reserva(reserva)


# ==========================================
# CONFIRMAR RESERVAS
# ==========================================

def confirmar_reserva():

    identificador = input(
        "Identificador de la reserva: "
    )

    return gestor_reservas.confirmar_reserva(
        identificador
    )


# ==========================================
# CANCELAR RESERVAS
# ==========================================

def cancelar_reserva():

    identificador = input(
        "Identificador de la reserva: "
    )

    return gestor_reservas.cancelar_reserva(
        identificador
    )


# ==========================================
# PROCESAR RESERVAS
# ==========================================

def procesar_reserva():

    identificador = input(
        "Identificador de la reserva: "
    )

    return gestor_reservas.procesar_reserva(
        identificador
    )


# ==========================================
# CONSULTAR RESERVAS
# ==========================================

def listar_reservas():

    reservas = gestor_reservas.listar_reservas()

    if not reservas:
        print("No hay reservas registradas.")
        return

    for reserva in reservas:
        print("\n", reserva)
        print("-" * 40)


# ==========================================
# CONSULTAR REGISTROS DEL SISTEMA
# ==========================================

def consultar_registros():

    registros = gestor_logs.consultar_logs()

    if not registros:
        print("No existen registros todavía.")
        return

    print("\nHISTORIAL DE EVENTOS Y ERRORES")

    for registro in registros:
        print(registro, end="")


# ==========================================
# MENÚ PRINCIPAL
# ==========================================

def mostrar_menu():

    print("\n" + "=" * 50)
    print("             SOFTWARE FJ")
    print("GESTION DE CLIENTES, SERVICIOS Y RESERVAS")
    print("=" * 50)

    print("1. Registrar cliente")
    print("2. Consultar clientes")
    print("3. Consultar servicios")
    print("4. Crear reserva")
    print("5. Confirmar reserva")
    print("6. Cancelar reserva")
    print("7. Procesar reserva")
    print("8. Consultar reservas")
    print("9. Consultar registros")
    print("0. Salir")

    print("=" * 50)


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

def main():

    print("\nBienvenido al sistema de gestion Software FJ")

    while True:

        mostrar_menu()

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":

            ejecutar_operacion(
                registrar_cliente,
                "Registro de cliente"
            )

        elif opcion == "2":

            ejecutar_operacion(
                listar_clientes,
                "Consulta de clientes"
            )

        elif opcion == "3":

            ejecutar_operacion(
                listar_servicios,
                "Consulta de servicios"
            )

        elif opcion == "4":

            ejecutar_operacion(
                crear_reserva,
                "Creacion de reserva"
            )

        elif opcion == "5":

            ejecutar_operacion(
                confirmar_reserva,
                "Confirmacion de reserva"
            )

        elif opcion == "6":

            ejecutar_operacion(
                cancelar_reserva,
                "Cancelacion de reserva"
            )

        elif opcion == "7":

            ejecutar_operacion(
                procesar_reserva,
                "Procesamiento de reserva"
            )

        elif opcion == "8":

            ejecutar_operacion(
                listar_reservas,
                "Consulta de reservas"
            )

        elif opcion == "9":

            ejecutar_operacion(
                consultar_registros,
                "Consulta de registros"
            )

        elif opcion == "0":

            print("\nGracias por utilizar Software FJ.")
            print("Sistema finalizado correctamente.")
            break

        else:

            error = SoftwareFJError(
                "Seleccione una opcion valida del menu"
            )

            print("\nError:", error)

            try:
                gestor_logs.registrar_excepcion(
                    error,
                    "Seleccion del menu"
                )
            except Exception as error_log:
                print("No se pudo guardar el error:", error_log)


# Ejecutar el programa

if __name__ == "__main__":
    main()
