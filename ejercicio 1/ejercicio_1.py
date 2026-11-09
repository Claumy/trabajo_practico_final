# ==========================================================
# Ejercicio 1 - Sanitización y Análisis Estadístico de Sensores
# ==========================================================

# Punto A: Normalización de Lecturas
def limpiar_registro_sensor(registro_raw: dict[str, str]):

    # Limpiamos el id    
    sensor_id = registro_raw["sensor_id"].strip()

    # Limpiamos la temperatura 
    temperatura = float(registro_raw["temperatura"]
                        .replace("ºC", "")
                        .replace("C", "")
                        .strip()
                        )
    
    # Limpiamos la ubicacion 
    ubicacion = registro_raw.get("ubicacion", "").strip()

    if ubicacion == "":
        ubicacion = "Ubicación Desconocida"

    # Diccionario
    registro_limpio = {
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "ubicacion": ubicacion
    }

    return registro_limpio


# Punto B: Monitoreo y Mapeo Estadístico
def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):
    lista_sensores_alerta = []
    suma_temperaturas = 0  

    for sensor in lista_sensores_limpios:
        temperatura = sensor["temperatura"]
        sensor_id = sensor["sensor_id"]

        if temperatura > umbral_temperatura:
            lista_sensores_alerta.append(sensor_id)
        
        suma_temperaturas += temperatura

    if len(lista_sensores_limpios) > 0:
        promedio_temperatura = suma_temperaturas / len(lista_sensores_limpios)
    else:
        promedio_temperatura = 0.0
        
    return lista_sensores_alerta, promedio_temperatura


# Bloque principal
sensores_raw = [  
    {
        "sensor_id": " SENSOR-001 ", 
        "temperatura": "24.5 ºC", 
        "ubicacion": "Planta Norte"
    },
    {
        "sensor_id": "SENSOR-002", 
        "temperatura": "32.5 C",  
        "ubicacion": " Laboratorio "
    },   
    {
        "sensor_id": "SENSOR-003", 
        "temperatura": "31.4C"
    },
    {
        "sensor_id": "SENSOR-004", 
        "temperatura": "27.1 ºC", 
        "ubicacion": " Planta Sur "
    },
    {
        "sensor_id": "SENSOR-005", 
        "temperatura": "22.5 ºC", 
        "ubicacion": " Depósito "
    }
]
    
# Limpiar los registros
sensores_limpios = []

for registro in sensores_raw:
    registro_limpio = limpiar_registro_sensor(registro)
    sensores_limpios.append(registro_limpio)

umbral = 30.0

sensores_alerta, promedio_global = generar_resumen_sensores(sensores_limpios, umbral)

# Imprimir reporte formateado
print("--- REPORTE DE SENSORES ---")
for sensor in sensores_limpios:
    
    print(f"Sensor: {sensor["sensor_id"]} | Temperatura: {sensor["temperatura"]}ºC | Ubicación: {sensor["ubicacion"]}")

print("-" * 30)
print(f"Umbral establecido: {umbral} ºC")
print(f"Promedio Global: {promedio_global:.2f} ºC")
print(f"Dispositivos en alerta (superan el umbral): {sensores_alerta}")  