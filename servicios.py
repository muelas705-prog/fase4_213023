
# Importamos abstractmethod para crear métodos abstractos
from abc import abstractmethod

# Importamos la clase abstracta Entidad (archivo entidad.py)
from entidad import Entidad

# Importamos las excepciones personalizadas (archivo excepciones.py)
from excepciones import DatosInvalidosError, ServicioNoDisponibleError

# IVA por defecto (19 %) escrito como decimal
IVA = 0.19


# Clase abstracta Servicio: hereda de Entidad
class Servicio(Entidad):

    # Constructor: recibe los datos comunes de todos los servicios
    def __init__(self, identificador, nombre, tarifa_base):
        # Llamamos al constructor de Entidad para guardar el identificador
        super().__init__(identificador)
        # Validamos que el nombre no esté vacío
        if not isinstance(nombre, str) or nombre.strip() == "":
            raise DatosInvalidosError("El nombre del servicio es obligatorio")
        # Validamos que la tarifa sea un número mayor que cero
        if not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise DatosInvalidosError("La tarifa base debe ser mayor que cero")
        # Guardamos los datos como atributos protegidos (encapsulación)
        self._nombre = nombre.strip()
        self._tarifa_base = tarifa_base
        # Todo servicio nuevo empieza disponible
        self._disponible = True

    # Método para consultar si el servicio está disponible
    def esta_disponible(self):
        return self._disponible

    # Método para cambiar la disponibilidad (True o False)
    def cambiar_disponibilidad(self, valor):
        # Solo se aceptan True o False
        if not isinstance(valor, bool):
            raise DatosInvalidosError("La disponibilidad debe ser True o False")
        self._disponible = valor

    # Método abstracto: cada servicio describe sus datos a su manera
    @abstractmethod
    def describir(self):
        pass

    # Método abstracto: cada servicio valida la duración a su manera
    @abstractmethod
    def validar_parametros(self, duracion):
        pass

    # Método abstracto: cada servicio calcula su costo a su manera
    # impuesto y descuento son opcionales (así se logra la "sobrecarga" en Python)
    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        pass

    # Método de Entidad que debemos implementar: devuelve la descripción
    def obtener_informacion(self):
        return self.describir()

    # Validación común: disponibilidad y duración positiva
    def _validar_basico(self, duracion):
        # Si no está disponible, lanzamos la excepción correspondiente
        if not self._disponible:
            raise ServicioNoDisponibleError("El servicio " + self._nombre + " no está disponible")
        # La duración debe ser un número mayor que cero
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatosInvalidosError("La duración debe ser un número mayor que cero")

    # Aplica descuento e impuesto a un subtotal
    def _aplicar_ajustes(self, subtotal, impuesto, descuento):
        # El impuesto y el descuento deben estar entre 0 y 1 (0.10 = 10 %)
        if impuesto < 0 or impuesto > 1:
            raise DatosInvalidosError("El impuesto debe estar entre 0 y 1")
        if descuento < 0 or descuento > 1:
            raise DatosInvalidosError("El descuento debe estar entre 0 y 1")
        # Primero se aplica el descuento
        total = subtotal - (subtotal * descuento)
        # Luego se suma el impuesto
        total = total + (total * impuesto)
        # Redondeamos a 2 decimales
        return round(total, 2)

    # Variante de costo: calcula directamente con IVA
    def calcular_costo_con_iva(self, duracion):
        return self.calcular_costo(duracion, impuesto=IVA)

    # Variante de costo: calcula con IVA y un descuento
    def calcular_costo_con_descuento(self, duracion, descuento):
        return self.calcular_costo(duracion, impuesto=IVA, descuento=descuento)


# Servicio 1: reserva de salas (se cobra por hora)
class ReservaSala(Servicio):

    # Constructor: datos comunes más capacidad
    def __init__(self, identificador, nombre, tarifa_base, capacidad):
        # Llamamos al constructor de Servicio
        super().__init__(identificador, nombre, tarifa_base)
        # La capacidad debe ser un entero mayor que cero
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatosInvalidosError("La capacidad debe ser un entero mayor que cero")
        self._capacidad = capacidad

    # Describe la sala
    def describir(self):
        return ("Sala " + self._nombre + " | Capacidad: " + str(self._capacidad)
                + " personas | Tarifa: $" + str(self._tarifa_base) + " por hora")

    # La sala se reserva máximo 12 horas
    def validar_parametros(self, duracion):
        # Validación común
        self._validar_basico(duracion)
        # Validación propia de la sala
        if duracion > 12:
            raise DatosInvalidosError("Una sala no se puede reservar por más de 12 horas")
        return True

    # Costo = tarifa x horas
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        # Validamos primero
        self.validar_parametros(duracion)
        # Calculamos el subtotal
        subtotal = self._tarifa_base * duracion
        # Aplicamos descuento e impuesto
        return self._aplicar_ajustes(subtotal, impuesto, descuento)


# Servicio 2: alquiler de equipos (se cobra por hora)
class AlquilerEquipo(Servicio):

    # Constructor: datos comunes más tipo de equipo
    def __init__(self, identificador, nombre, tarifa_base, tipo_equipo):
        # Llamamos al constructor de Servicio
        super().__init__(identificador, nombre, tarifa_base)
        # El tipo de equipo no puede estar vacío
        if not isinstance(tipo_equipo, str) or tipo_equipo.strip() == "":
            raise DatosInvalidosError("El tipo de equipo es obligatorio")
        self._tipo_equipo = tipo_equipo.strip()

    # Describe el equipo
    def describir(self):
        return ("Equipo " + self._nombre + " | Tipo: " + self._tipo_equipo
                + " | Tarifa: $" + str(self._tarifa_base) + " por hora")

    # El equipo solo necesita la validación básica
    def validar_parametros(self, duracion):
        self._validar_basico(duracion)
        return True

    # Costo = tarifa x horas
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        # Validamos primero
        self.validar_parametros(duracion)
        # Calculamos el subtotal
        subtotal = self._tarifa_base * duracion
        # Aplicamos descuento e impuesto
        return self._aplicar_ajustes(subtotal, impuesto, descuento)


# Servicio 3: asesorías especializadas (se cobra por hora)
class AsesoriaEspecializada(Servicio):

    # Constructor: datos comunes más especialidad
    def __init__(self, identificador, nombre, tarifa_base, especialidad):
        # Llamamos al constructor de Servicio
        super().__init__(identificador, nombre, tarifa_base)
        # La especialidad no puede estar vacía
        if not isinstance(especialidad, str) or especialidad.strip() == "":
            raise DatosInvalidosError("La especialidad es obligatoria")
        self._especialidad = especialidad.strip()

    # Describe la asesoría
    def describir(self):
        return ("Asesoría " + self._nombre + " | Especialidad: " + self._especialidad
                + " | Tarifa: $" + str(self._tarifa_base) + " por hora")

    # La asesoría dura entre 1 y 8 horas
    def validar_parametros(self, duracion):
        # Validación común
        self._validar_basico(duracion)
        # Validación propia de la asesoría
        if duracion < 1 or duracion > 8:
            raise DatosInvalidosError("Una asesoría debe durar entre 1 y 8 horas")
        return True

    # Costo = tarifa x horas
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        # Validamos primero
        self.validar_parametros(duracion)
        # Calculamos el subtotal
        subtotal = self._tarifa_base * duracion
        # Aplicamos descuento e impuesto
        return self._aplicar_ajustes(subtotal, impuesto, descuento)


# Pruebas: solo se ejecutan si corremos este archivo directamente
if __name__ == "__main__":

    # Creamos un servicio de cada tipo
    sala = ReservaSala("SAL-001", "Innovación", 50000, 20)
    equipo = AlquilerEquipo("EQU-001", "Proyector HD", 20000, "Audiovisual")
    asesoria = AsesoriaEspecializada("ASE-001", "Cloud", 80000, "Computación en la nube")

    # Los guardamos en una lista y los recorremos (polimorfismo)
    servicios = [sala, equipo, asesoria]
    for s in servicios:
        print(s.describir())
        print("  Costo 2 horas:", s.calcular_costo(2))
        print("  Costo con IVA:", s.calcular_costo_con_iva(2))
        print("  Costo con 10% de descuento e IVA:", s.calcular_costo_con_descuento(2, 0.10))

    # Casos con errores: el programa los captura y sigue funcionando
    print("\n--- Pruebas con errores ---")

    # Error 1: duración negativa
    try:
        sala.calcular_costo(-1)
    except DatosInvalidosError as e:
        print("Error controlado:", e)

    # Error 2: sala por más de 12 horas
    try:
        sala.calcular_costo(15)
    except DatosInvalidosError as e:
        print("Error controlado:", e)

    # Error 3: tarifa inválida al crear un equipo
    try:
        AlquilerEquipo("EQU-002", "Portátil", -5, "Cómputo")
    except DatosInvalidosError as e:
        print("Error controlado:", e)

    # Error 4: servicio no disponible
    equipo.cambiar_disponibilidad(False)
    try:
        equipo.calcular_costo(2)
    except ServicioNoDisponibleError as e:
        print("Error controlado:", e)
