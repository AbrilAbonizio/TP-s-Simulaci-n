import random
import math
import matplotlib.pyplot as plt

# INGRESO DE PARAMETROS POR CONSOLA
mu = 0
while mu <= 0:
    mu = int(input("Ingrese la tasa de servicio (mu): "))
    if mu <= 0:
        print("El número debe ser 0 o mayor")

cantidad_clientes = 0
while cantidad_clientes <= 0:
    cantidad_clientes = int(input("Ingrese la cantidad total de clientes a simular: "))
    if cantidad_clientes <= 0:
        print("El número debe ser mayor a 0")

repeticiones = 10          
porcentajes = [0.25, 0.50, 0.75, 1.00, 1.25]
# Se agrega float('inf') para modelar la cola infinita pura (M/M/1)
tamaños_cola_a_probar = [0, 2, 5, 10, 50, float('inf')]

# Función para obtener los valores matemáticos exactos y compararlos
def calcular_teoricos(lambd, mu, limite_cola):
    rho = lambd / mu
    
    # Modelo M/M/1 (Cola Infinita)
    if limite_cola == float('inf'):
        if rho >= 1:
            return {"Lq": "No se puede calc.", "L": "No se puede calc.", 
                    "Wq": "No se puede calc.", "W": "No se puede calc.", 
                    "Util": "No se puede calc.", "P_deneg": "No se puede calc."}
        else:
            L = rho / (1 - rho)
            Lq = (rho**2) / (1 - rho)
            W = 1 / (mu - lambd)
            Wq = rho / (mu - lambd)
            return {"Lq": f"{Lq:.2f}", "L": f"{L:.2f}", "Wq": f"{Wq:.4f}", 
                    "W": f"{W:.4f}", "Util": f"{rho:.2%}", "P_deneg": "0.00%"}
    
    # Modelo M/M/1/K (Cola Finita, donde K = límite de cola + 1 en servicio)
    else:
        K = limite_cola + 1
        # Usamos isclose por precisión de punto flotante en Python
        if math.isclose(rho, 1.0):
            P0 = 1 / (K + 1)
            Pk = 1 / (K + 1)
            L = K / 2
        else:
            P0 = (1 - rho) / (1 - rho**(K+1))
            Pk = (rho**K) * P0
            L = (rho / (1 - rho)) - ((K + 1) * rho**(K+1) / (1 - rho**(K+1)))
        
        lambda_eff = lambd * (1 - Pk)
        if lambda_eff > 0:
            W = L / lambda_eff
            Wq = W - (1 / mu)
            Lq = lambda_eff * Wq
        else:
            W, Wq, Lq = 0, 0, 0
            
        utilizacion = 1 - P0
        return {"Lq": f"{max(0, Lq):.2f}", "L": f"{L:.2f}", "Wq": f"{max(0, Wq):.4f}", 
                "W": f"{W:.4f}", "Util": f"{utilizacion:.2%}", "P_deneg": f"{Pk:.2%}"}

def graficar_todos_rhos(datos_graficos, capacidad, porcentajes):
    titulo_cap = "Infinita" if math.isinf(capacidad) else capacidad
    
    # Bucle para crear una ventana separada por cada porcentaje
    for pct in porcentajes:
        # Creamos una figura de 1 fila x 2 columnas
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Título de la ventana (para identificarla en la barra de tareas)
        fig.canvas.manager.set_window_title(f'Cap: {titulo_cap} - Carga: {pct*100:.0f}%')
        fig.suptitle(f'Evolución del Sistema (Capacidad: {titulo_cap} | Carga: {pct*100:.0f}%)', fontsize=14, fontweight='bold')
        
        datos = datos_graficos[pct]
        datos_hist_n = datos['hist_n']
        lista_tiempos_sistema = datos['t_sistema']
        lista_tiempos_cola = datos['t_cola']

        # --- GRÁFICO 1: Barras verticales (Probabilidad Discreta) ---
        clientes = [k for k in datos_hist_n.keys() if k <= 15] 
        probabilidades = [datos_hist_n[k] for k in clientes]
        
        acumulada_n = []
        suma_temp = 0
        for p in probabilidades:
            suma_temp += p
            acumulada_n.append(suma_temp)
            
        ax1.bar(clientes, probabilidades, label='Discreta P(n)', color='skyblue', edgecolor='black', width=0.4)
        ax1.plot(clientes, acumulada_n, marker='o', color='red', label='Acumulada', linewidth=2)
        
        ax1.set_title('Probabilidad de n clientes en cola', fontsize=11)
        ax1.set_xlabel('Cantidad de Clientes (n)')
        ax1.set_ylabel('Probabilidad')
        ax1.set_xticks(clientes)
        
        max_cli = max(clientes) if clientes else 0
        ax1.set_xlim(-0.5, max(1.5, max_cli + 0.5))
        ax1.set_ylim(0, 1.1)
        ax1.legend(loc='center right', frameon=False)
        ax1.grid(axis='y', linestyle='--', alpha=0.7)

        # --- GRÁFICO 2: Función de Distribución Acumulada de Tiempos ---
        if lista_tiempos_sistema:
            ts_ordenados = sorted(lista_tiempos_sistema)
            pasos_grafico = max(10, min(50, len(ts_ordenados) // 10))
            indices_ts = [int(j * (len(ts_ordenados) - 1) / (pasos_grafico - 1)) for j in range(pasos_grafico)]
            
            puntos_x_ts = [ts_ordenados[idx] for idx in indices_ts]
            puntos_y_ts = [indices_ts[j] / len(ts_ordenados) for j in range(pasos_grafico)]
            ax2.plot(puntos_x_ts, puntos_y_ts, marker='o', label='Tiempo en sistema (W)', linewidth=2, color='navy')
            
            if lista_tiempos_cola:
                tq_ordenados = sorted(lista_tiempos_cola)
                indices_tq = [int(j * (len(tq_ordenados) - 1) / (pasos_grafico - 1)) for j in range(pasos_grafico)]
                puntos_x_tq = [tq_ordenados[idx] for idx in indices_tq]
                puntos_y_tq = [indices_tq[j] / len(tq_ordenados) for j in range(pasos_grafico)]
                ax2.plot(puntos_x_tq, puntos_y_tq, marker='d', label='Tiempo en cola (Wq)', linewidth=1.5, color='orange')
            
            ax2.set_title('Distribución Acumulada de Tiempos', fontsize=11)
            ax2.set_xlabel('Tiempo (t)')
            ax2.set_ylabel('Probabilidad P(Tiempo ≤ t)')
            
            max_ts = max(ts_ordenados) if ts_ordenados else 1.0
            ax2.set_xlim(-0.05 * max_ts, max_ts * 1.05)
            ax2.set_ylim(-0.05, 1.1)
            ax2.legend(loc='lower right', frameon=False)
            ax2.grid(linestyle='--', alpha=0.7)

        plt.tight_layout()

    # Muestra todas las ventanas creadas en el bucle en simultáneo.
    # El programa se pausará hasta que cierres las 5 ventanas.
    #plt.show()
    # Eliminar o comentar: plt.show()
        
        # Agregar:
        nombre_archivo = f"Grafico_Cap_{titulo_cap}_Carga_{pct*100:.0f}.png"
        plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')
        plt.close(fig) # Cierra la figura en memoria para no saturar la RAM

# SIMULACION M/M/1 - EVENTOS DISCRETOS (Procesando hasta el último cliente)
def simular(lambda_arribo, limite_cola, total_clientes_a_simular):
    en_sistema = 0
    tiempo_actual = 0.0
    
    # Eventos futuros
    t_proxima_llegada = random.expovariate(lambda_arribo)
    t_proxima_salida = float('inf') # Infinito significa que el servidor está inactivo
    
    # Contadores
    intentos_arribo = 0
    clientes_procesados = 0
    rechazados = 0
    cola_llegadas = [] 
    tiempos_cola = []
    tiempos_sistema = []
    
    # Acumuladores de área (Tiempo * Cantidad)
    area_en_cola = 0.0
    area_en_sistema = 0.0
    tiempo_ocupado = 0.0
    tiempo_en_n_clientes = {} 

    # El bucle corta cuando se PROCESA a todos (no solo cuando llegan)
    while clientes_procesados < total_clientes_a_simular:
        t_evento = min(t_proxima_llegada, t_proxima_salida)
        
        delta_t = t_evento - tiempo_actual
        tiempo_actual = t_evento
        
        # Calcular estados para acumular áreas de las estadísticas continuas
        en_cola_actual = max(0, en_sistema - 1)
        area_en_sistema += en_sistema * delta_t
        area_en_cola += en_cola_actual * delta_t
        if en_sistema > 0:
            tiempo_ocupado += delta_t
            
        tiempo_en_n_clientes[en_cola_actual] = tiempo_en_n_clientes.get(en_cola_actual, 0) + delta_t

        # EVENTO: LLEGADA
        if t_evento == t_proxima_llegada:
            intentos_arribo += 1
            
            # Cortamos las llegadas si ya alcanzamos la cantidad de simulación
            if intentos_arribo < total_clientes_a_simular:
                t_proxima_llegada = tiempo_actual + random.expovariate(lambda_arribo)
            else:
                t_proxima_llegada = float('inf') # No hay más llegadas
            
            if en_sistema >= limite_cola + 1:
                rechazados += 1 
                clientes_procesados += 1 # Cliente rechazado cuenta como procesado
            else:
                en_sistema += 1
                if en_sistema == 1: 
                    # Pasa directo al servidor vacío
                    ts = random.expovariate(mu)
                    tiempos_cola.append(0)
                    tiempos_sistema.append(ts)
                    t_proxima_salida = tiempo_actual + ts
                else:
                    # Espera en cola
                    cola_llegadas.append(tiempo_actual)

        # EVENTO: SALIDA
        else:
            en_sistema -= 1
            clientes_procesados += 1 # Cliente atendido cuenta como procesado
            
            if en_sistema > 0:
                # Entra a servicio el próximo en la cola
                t_llegada_cliente = cola_llegadas.pop(0)
                tiempo_esperado = tiempo_actual - t_llegada_cliente
                ts = random.expovariate(mu)
                
                tiempos_cola.append(tiempo_esperado)
                tiempos_sistema.append(tiempo_esperado + ts)
                t_proxima_salida = tiempo_actual + ts
            else:
                # El servidor queda libre
                t_proxima_salida = float('inf')

    # El tiempo total es el tiempo de la última salida (o rechazo)
    tiempo_total_simulacion = tiempo_actual

    # Calcular estadísticas finales dividiendo áreas sobre tiempo total real simulado
    probabilidades_n = {n: t / tiempo_total_simulacion for n, t in tiempo_en_n_clientes.items()}
    prob_denegacion = rechazados / intentos_arribo if intentos_arribo > 0 else 0

    return {
        'en_cola_promedio': area_en_cola / tiempo_total_simulacion,
        'en_sistema_promedio': area_en_sistema / tiempo_total_simulacion,
        'utilizacion': tiempo_ocupado / tiempo_total_simulacion,
        'prob_denegacion': prob_denegacion,
        'tiempos_cola': tiempos_cola,
        'tiempos_sistema': tiempos_sistema,
        'probabilidades_n': probabilidades_n
    }

print("=" * 95)
print("SIMULACION A EVENTOS DISCRETOS")
print("=" * 95)

# Fijamos semilla para que el TP tenga resultados reproducibles
random.seed(42)

for capacidad_actual in tamaños_cola_a_probar:
    cap_str = "INFINITA" if math.isinf(capacidad_actual) else capacidad_actual
    print("-" * 95)
    print(f"\n CAPACIDAD MAXIMA DE LA COLA = {cap_str}")
    
    # Diccionario para guardar los datos de los gráficos de cada porcentaje
    datos_graficos_capacidad = {}
    
    for porcentaje in porcentajes:
        lambda_arribo = mu * porcentaje
        rho_teorico = lambda_arribo / mu

        acum_en_cola = 0
        acum_en_sistema = 0
        acum_espera_cola = 0
        acum_espera_sistema = 0
        acum_utilizacion = 0
        acum_denegacion = 0
        acum_prob_n = {}
        
        teoricos = calcular_teoricos(lambda_arribo, mu, capacidad_actual)

        for rep in range(repeticiones):
            # Imprimimos la configuración de prueba que usa el límite de clientes
            resultado = simular(lambda_arribo, limite_cola=capacidad_actual, total_clientes_a_simular=cantidad_clientes)
            
            acum_en_cola += resultado['en_cola_promedio']
            acum_en_sistema += resultado['en_sistema_promedio']
            acum_utilizacion += resultado['utilizacion']
            acum_denegacion += resultado['prob_denegacion']

            if len(resultado['tiempos_cola']) > 0:
                acum_espera_cola += sum(resultado['tiempos_cola']) / len(resultado['tiempos_cola'])
            if len(resultado['tiempos_sistema']) > 0:
                acum_espera_sistema += sum(resultado['tiempos_sistema']) / len(resultado['tiempos_sistema'])
                
            for n, prob in resultado['probabilidades_n'].items():
                acum_prob_n[n] = acum_prob_n.get(n, 0) + prob

            # Guardamos la repetición 0 para armar los gráficos al final
            if rep == 0:
                datos_graficos_capacidad[porcentaje] = {
                    'hist_n': {k: v for k, v in resultado['probabilidades_n'].items()},
                    't_sistema': resultado['tiempos_sistema'],
                    't_cola': resultado['tiempos_cola']
                }

        prom_en_cola = acum_en_cola / repeticiones
        prom_en_sistema = acum_en_sistema / repeticiones
        prom_espera_cola = acum_espera_cola / repeticiones
        prom_espera_sistema = acum_espera_sistema / repeticiones
        prom_utilizacion = acum_utilizacion / repeticiones
        prom_denegacion = acum_denegacion / repeticiones

        print(f"\n>>> Lambda = {lambda_arribo:.2f} ({porcentaje*100:.0f}% de mu) | rho = {rho_teorico:.2f}")
        print(f"  Clientes prom. en cola (Lq):       Sim={prom_en_cola:.2f} \t| Teo={teoricos['Lq']}")
        print(f"  Clientes prom. en sistema (L):     Sim={prom_en_sistema:.2f} \t| Teo={teoricos['L']}")
        print(f"  Tiempo prom. en cola (Wq):         Sim={prom_espera_cola:.4f} \t| Teo={teoricos['Wq']}")
        print(f"  Tiempo prom. en sistema (W):       Sim={prom_espera_sistema:.4f} \t| Teo={teoricos['W']}")
        print(f"  Utilización del servidor:          Sim={prom_utilizacion:.2%} \t| Teo={teoricos['Util']}")
        print(f"  Probabilidad Denegación Servicio:  Sim={prom_denegacion:.2%} \t| Teo={teoricos['P_deneg']}")
        
        max_keys = min(3, max(acum_prob_n.keys()) + 1 if acum_prob_n else 3)
        string_probs = ", ".join([f"P({n})={acum_prob_n.get(n, 0)/repeticiones:.2%}" for n in range(max_keys)])
        print(f"  Probabilidad de n clientes en cola: {string_probs} ...")
        
    # Una vez terminados todos los porcentajes de esta capacidad, mostramos la grilla
    graficar_todos_rhos(datos_graficos_capacidad, capacidad_actual, porcentajes)