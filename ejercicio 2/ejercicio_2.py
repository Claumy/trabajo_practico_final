# ==========================================================
# Ejercicio 2 - Modelo de productos, excepciones y persistencia
# EcoTech Solutions
# ==========================================================

import json


# ----------------------------------------------------------
# EXCEPCIÓN PERSONALIZADA
# ----------------------------------------------------------
class StockInvalidoError(Exception):
    """Se lanza cuando se intenta asignar un stock negativo."""
    pass


# ----------------------------------------------------------
# CLASE BASE: DispositivoEcológico
# ----------------------------------------------------------
class DispositivoEcológico:
    """Representa un producto genérico del catálogo ecológico."""

    def __init__(self, codigo: str, nombre: str, precio: float, stock: int):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.__stock = 0
        self.asignar_stock(stock)

    # Setter
    def asignar_stock(self, nuevo_stock):
        if nuevo_stock < 0:
            raise StockInvalidoError("El stock no puede ser negativo")
        self.__stock = nuevo_stock

    # Getter
    def obtener_stock(self):
        return self.__stock

    # Ficha técnica básica
    def mostrar_ficha_tecnica(self):
        return f"Código: {self.codigo} | Nombre: {self.nombre} | Precio: ${self.precio} | Stock: {self.obtener_stock()} unidades"


# ----------------------------------------------------------
# CLASE HIJA: PanelSolar (HERENCIA)
# ----------------------------------------------------------
class PanelSolar(DispositivoEcológico):
    """Panel solar: hereda de DispositivoEcológico y agrega sus datos propios."""

    def __init__(self, codigo, nombre, precio, stock, potencia_watts, eficiencia):
        super().__init__(codigo, nombre, precio, stock)

        # Atributos específicos del panel solar
        self.potencia_watts = potencia_watts
        self.eficiencia = eficiencia

    # POLIMORFISMO
    def mostrar_ficha_tecnica(self):
        return f"Código: {self.codigo} | Nombre: {self.nombre} | Precio: ${self.precio} | Stock: {self.obtener_stock()} unidades | Potencia: {self.potencia_watts}W | Eficiencia: {self.eficiencia}%"


# ----------------------
# GESTOR DE INVENTARIO: 
# ----------------------
class GestorInventario:
    """Se encarga de guardar el catálogo de productos en disco."""

    def guardar_catalogo_json(self, lista_dispositivos, ruta_archivo):
        catalogo = []

        for dispositivo in lista_dispositivos:
            producto = {
                "codigo": dispositivo.codigo,
                "nombre": dispositivo.nombre,
                "precio": dispositivo.precio,
                "stock": dispositivo.obtener_stock()
            }

            if type(dispositivo) == PanelSolar:
                producto["potencia_watts"] = dispositivo.potencia_watts
                producto["eficiencia"] = dispositivo.eficiencia

            catalogo.append(producto)

        with open(ruta_archivo, "w", encoding="utf-8") as file:
            json.dump(catalogo, file, indent=4)

        print("Catálogo guardado correctamente")


# ==========================================
# BLOQUE DE PRUEBAS Y EJECUCIÓN
# ==========================================

# --- Creación de productos válidos ---
panel1 = PanelSolar(
    "PS-001",
    "SolarMax-500",
    390000,
    18,
    500,
    24.5
)

panel2 = PanelSolar(
    "PS-002",
    "SolarTurbo-2000",
    890000,
    49,
    2000,
    28.5
)

# Producto de la clase base (no es un panel solar)
equipo1 = DispositivoEcológico(
    "EE-001",
    "Controlador de Carga",
    190000,
    33
)


# --- Prueba 1: crear un producto con stock negativo ---
try:
    panel_invalido = PanelSolar(
        "PS-004",
        "Panel Solar Defectuoso",
        430000,
        -5,
        600,
        22.5
    )
except StockInvalidoError as error:
    print(f"Error controlado: {error}")


# --- Prueba 2: modificar el stock de un producto existente ---
try:
    panel1.asignar_stock(-5)
except StockInvalidoError as error:
    print(f"Error controlado: {error}")


# --- Mostrar las fichas técnicas  ---
productos = [panel1, panel2, equipo1]

print("--- FICHAS TÉCNICAS ---")
for producto in productos:
    print(producto.mostrar_ficha_tecnica())


# --- Exportación al archivo JSON ---
admin_catalogo = GestorInventario()
admin_catalogo.guardar_catalogo_json(productos, "catalogo_ecotech.json")