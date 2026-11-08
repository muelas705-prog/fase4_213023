
from cliente import Cliente, GestorClientes
from excepciones import DatosInvalidosError, ClienteNoEncontradoError

# Crear el administrador de clientes
gestor = GestorClientes()

print("SISTEMA SOFTWARE FJ")
print("PRUEBAS DE GESTIÓN DE CLIENTES")
print("-" * 40)

# PRUEBA 1: Registrar un cliente válido
try:
    cliente1 = Cliente(
        "C001",
        "Carlos Perez",
        "carlos@gmail.com",
        "3001234567"
    )

    print(gestor.registrar_cliente(cliente1))

except DatosInvalidosError as error:
    print("Error:", error)


# PRUEBA 2: Registrar otro cliente válido
try:
    cliente2 = Cliente(
        "C002",
        "Maria Lopez",
        "maria@gmail.com",
        "3101234567"
    )

    print(gestor.registrar_cliente(cliente2))

except DatosInvalidosError as error:
    print("Error:", error)


# PRUEBA 3: Registrar un cliente sin nombre
try:
    cliente3 = Cliente(
        "C003",
        "",
        "juan@gmail.com",
        "3001234567"
    )

    gestor.registrar_cliente(cliente3)

except DatosInvalidosError as error:
    print("Error controlado:", error)


# PRUEBA 4: Buscar un cliente inexistente
try:
    gestor.buscar_cliente("C999")

except ClienteNoEncontradoError as error:
    print("Error controlado:", error)


# PRUEBA 5: Mostrar clientes registrados
print("\nCLIENTES REGISTRADOS:")

for informacion in gestor.listar_clientes():
    print(informacion)
    print("-" * 30)

print("Las pruebas finalizaron correctamente.")
