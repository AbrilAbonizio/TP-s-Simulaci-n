import random
import math
import matplotlib.pyplot as plt


# INGRESO DE PARAMETROS POR CONSOLA
i=True
costo_orden_fijo=0
while costo_orden_fijo<=0:
  try:
    costo_orden_fijo = float(input("Ingrese el Costo de realizar una orden (K): "))
    if costo_orden_fijo>0:
      break
    else:
        print("El número debe ser mayor a 0")
  except:
    print("Ingrese un número válido (ej: 10.5)")


costo_mant_unitario=0
while costo_mant_unitario<=0:
  try:
    costo_mant_unitario = float(input("Ingrese el Costo de Mantenimiento (por unidad) (h): "))
    if costo_mant_unitario>0:
        break
    else:
        print("El número debe ser mayor a 0")
  except:
    print("Ingrese un número válido (ej: 10.5)")


costo_faltante_unitario=0
while costo_faltante_unitario<=0:
  try:
    costo_faltante_unitario = float(input("Ingrese el Costo por Faltantes (por unidad) (p): "))
    if costo_faltante_unitario>0:
      break
    else:
        print("El número debe ser mayor a 0")
  except:
    print("Ingrese un número válido (ej: 10.5)")


dias_simulacion=0
while dias_simulacion<=0:
  try:
    dias_simulacion = int(input("Ingrese los dias totales de simulacion: "))
    if dias_simulacion>0:
        break
    else:
        print("El número debe ser mayor a 0")
  except:
    print("Ingrese un número válido (ej: 100)")



#Valores fijos de politica y demanda

punto_pedido_s = 20        # s: si el stock baja de 20, se pide
stock_maximo_S = 100       # S: se pide hasta alcanzar 100 unidades
demanda_media = 8          # promedio de unidades vendidas por día
tiempo_entrega = 3         # días que tarda el proveedor en traer el pedido
repeticiones = 10          # Mínimo de 10 corridas exigido por el TP


# SIMULACIÓN DE INVENTARIO

def simular_inventario():
    inventario_actual = stock_maximo_S
    pedido_en_camino = False
    dias_para_entrega = 0
    cantidad_ordenada = 0
    
    # Contadores de costos 
    total_costo_orden = 0.0
    total_costo_mantenimiento = 0.0
    total_costo_faltante = 0.0

    # Historiales los gráficos
    historial_stock = []
    historial_costos_acum = []

    for dia in range(1, dias_simulacion + 1):
        #Llega el pedido
        if pedido_en_camino:
            dias_para_entrega -= 1
            if dias_para_entrega == 0:
                inventario_actual += cantidad_ordenada
                pedido_en_camino = False

        # Generacion de la demanda
        demanda_del_dia = random.poissonvariate(demanda_media) if hasattr(random, 'poissonvariate') else int(random.gauss(demanda_media, 2))
        demanda_del_dia = max(0, demanda_del_dia)

        inventario_actual -= demanda_del_dia

        # Evaluacion de costos
        if inventario_actual >= 0:
            total_costo_mantenimiento += inventario_actual * costo_mant_unitario
        else:
            total_costo_faltante += abs(inventario_actual) * costo_faltante_unitario

        # Politicas de control
        # Inventario neto = actual + lo que tiene que llegar
        inventario_neto = inventario_actual + (cantidad_ordenada if pedido_en_camino else 0)
        
        if inventario_neto <= punto_pedido_s and not pedido_en_camino:
            cantidad_ordenada = stock_maximo_S - inventario_actual
            total_costo_orden += costo_orden_fijo
            pedido_en_camino = True
            dias_para_entrega = tiempo_entrega

        # Guardado de estado diario
        historial_stock.append(inventario_actual)
        historial_costos_acum.append(total_costo_orden + total_costo_mantenimiento + total_costo_faltante)

    return {
        'c_orden': total_costo_orden,
        'c_mant': total_costo_mantenimiento,
        'c_falt': total_costo_faltante,
        'c_total': total_costo_orden + total_costo_mantenimiento + total_costo_faltante,
        'hist_stock': historial_stock,
        'hist_costos': historial_costos_acum
    }



acum_orden = 0
acum_mant = 0
acum_falt = 0
acum_total = 0

# Datos de la primer corrida
datos_grafico = None

for rep in range(1, repeticiones + 1):
    res = simular_inventario()
    
    acum_orden += res['c_orden']
    acum_mant += res['c_mant']
    acum_falt += res['c_falt']
    acum_total += res['c_total']
    
    if rep == 1:
        datos_grafico = res
        
    print(f"  Corrida {rep:02d} -> Orden: ${res['c_orden']:.2f} | Mant: ${res['c_mant']:.2f} | Faltante: ${res['c_falt']:.2f} | Total: ${res['c_total']:.2f}")

# Promedios finales 
prom_orden = acum_orden / repeticiones
prom_mant = acum_mant / repeticiones
prom_falt = acum_falt / repeticiones
prom_total = acum_total / repeticiones

print("\n" + "="*60)
print("MEDIDAS DE RENDIMIENTO PROMEDIO FINALES (10 CORRIDAS)")
print("="*60)
print(f"  Costo de Orden Promedio:         ${prom_orden:.2f}")
print(f"  Costo de Mantenimiento Promedio: ${prom_mant:.2f}")
print(f"  Costo de Faltante Promedio:      ${prom_falt:.2f}")
print(f"  COSTO TOTAL PROMEDIO:            ${prom_total:.2f}")
print("="*60)

# GENERACIÓN DE GRÁFICOS 

if datos_grafico:
    
    dias = list(range(1, dias_simulacion + 1))
    
    # Gráfico de Evolución del Stock
    plt.figure(figsize=(10, 4))
    plt.plot(dias, datos_grafico['hist_stock'], label='Nivel de Stock')
    plt.axhline(y=punto_pedido_s, color='r', linestyle='--', label='Punto de Pedido (s)')
    plt.axhline(y=0, color='black', linewidth=0.8, linestyle=':')
    plt.title('Evolución Temporal del Inventario')
    plt.xlabel('Días')
    plt.ylabel('Unidades Disponibles')
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.show()

    # Gráfico de Costos Acumulados
    plt.figure(figsize=(10, 4))
    plt.plot(dias, datos_grafico['hist_costos'], label='Costo Total Acumulado')
    plt.title('Evolución del Costo Total en Relación al Tiempo')
    plt.xlabel('Días')
    plt.ylabel('Dinero ($)')
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.show()