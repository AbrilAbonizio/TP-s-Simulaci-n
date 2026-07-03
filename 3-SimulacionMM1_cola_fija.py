import random
import math
import matplotlib.pyplot as plt

# INGRESO DE PARAMETROS POR CONSOLA
mu = 0
while mu <= 0:
    mu = int(input("Ingrese la tasa de servicio (mu): "))
    if mu <= 0:
      print("El número debe ser 0 o mayor")

tiempo_total = 0
while tiempo_total <= 0:
    tiempo_total = float(input("Ingrese el tiempo total de simulación: "))
    if mu <= 0:
      print("El número debe ser mayor a 0")

dt = 0.01                  
repeticiones = 10          
porcentajes = [0.25, 0.50, 0.75, 1.00, 1.25]
tamaños_cola_a_probar = [0, 2, 5, 10, 50]

cola_graficos = 5
datos_hist_n = None
lista_tiempos_sistema_grafico = []
lista_tiempos_cola_grafico = []


# SIMULACION M/M/1

def simular(lambda_arribo, limite_cola):
    en_cola = 0
    servidor_ocupado = False
    tiempo_servicio_restante = 0.0
    tiempo_ocupado = 0.0
    
    # Contadores para denegacion de servicio
    intentos_arribo = 0
    rechazados = 0

    clientes_esperando = []   # Guarda el tiempo de llegada a la cola
    tiempos_cola = []         # Wq
    tiempos_sistema = []      # W

    suma_en_cola = 0
    suma_en_sistema = 0
    pasos = 0

    # Diccionario para contar los pasos que la cola pasa en cada tamaño (n)
    tiempo_en_n_clientes = {i: 0 for i in range(limite_cola + 1)}
    tiempo_actual = 0.0

    while tiempo_actual < tiempo_total:

        # Llegada de clientes
        p_llegada = 1 - math.exp(-lambda_arribo * dt)
        if random.random() < p_llegada:
            intentos_arribo += 1 # Intentaron entrar
            
            if servidor_ocupado and en_cola >= limite_cola:
                rechazados += 1  # Denegacion de servicio
            elif servidor_ocupado:
                en_cola += 1
                clientes_esperando.append(tiempo_actual)
            else:
                servidor_ocupado = True
                t_serv = random.expovariate(mu)
                tiempo_servicio_restante = t_serv
                # Si entra directo, no espera en cola (Wq = 0) pero si pasa tiempo en sistema (W = t_serv)
                tiempos_cola.append(0)
                tiempos_sistema.append(t_serv)

        #Proceso en el servidor
        if servidor_ocupado:
            tiempo_servicio_restante -= dt
            tiempo_ocupado += dt

            if tiempo_servicio_restante <= 0:
                servidor_ocupado = False
                tiempo_servicio_restante = 0

                if en_cola > 0:
                    en_cola -= 1
                    tiempo_llegada = clientes_esperando.pop(0)
                    t_espera_cola = tiempo_actual - tiempo_llegada
                    t_serv = random.expovariate(mu)
                    
                    tiempos_cola.append(t_espera_cola)
                    tiempos_sistema.append(t_espera_cola + t_serv) # W = Wq + Ts
                    
                    servidor_ocupado = True
                    tiempo_servicio_restante = t_serv

        # Acumulacion para estadisticas
        suma_en_cola += en_cola
        suma_en_sistema += en_cola + (1 if servidor_ocupado else 0)
        
        
        if en_cola in tiempo_en_n_clientes:
            tiempo_en_n_clientes[en_cola] += 1
            
        pasos += 1
        tiempo_actual += dt

    
    probabilidades_n = {n: cant_pasos / pasos for n, cant_pasos in tiempo_en_n_clientes.items()}
    prob_denegacion = rechazados / intentos_arribo if intentos_arribo > 0 else 0

    return {
        'en_cola_promedio': suma_en_cola / pasos,
        'en_sistema_promedio': suma_en_sistema / pasos,
        'utilizacion': tiempo_ocupado / tiempo_total,
        'prob_denegacion': prob_denegacion,
        'tiempos_cola': tiempos_cola,
        'tiempos_sistema': tiempos_sistema,
        'probabilidades_n': probabilidades_n
    }



print("=" * 85)
print("SIMULACION M/M/1")
print(f"Mu = {mu} | Tiempo max = {tiempo_total}")
print("=" * 85)

for capacidad_actual in tamaños_cola_a_probar:
    print("-" * 85)
    print(f"\n CAPACIDAD MAXIMA DE LA COLA = {capacidad_actual}")
    
    for porcentaje in porcentajes:
        lambda_arribo = mu * porcentaje
        rho_teorico = lambda_arribo / mu

        acum_en_cola = 0
        acum_en_sistema = 0
        acum_espera_cola = 0
        acum_espera_sistema = 0
        acum_utilizacion = 0
        acum_denegacion = 0
        
        
        acum_prob_n = {i: 0.0 for i in range(capacidad_actual + 1)}

        for rep in range(repeticiones):
            resultado = simular(lambda_arribo, limite_cola=capacidad_actual)
            
            acum_en_cola += resultado['en_cola_promedio']
            acum_en_sistema += resultado['en_sistema_promedio']
            acum_utilizacion += resultado['utilizacion']
            acum_denegacion += resultado['prob_denegacion']

            if len(resultado['tiempos_cola']) > 0:
                acum_espera_cola += sum(resultado['tiempos_cola']) / len(resultado['tiempos_cola'])
            if len(resultado['tiempos_sistema']) > 0:
                acum_espera_sistema += sum(resultado['tiempos_sistema']) / len(resultado['tiempos_sistema'])
                
            for n in acum_prob_n:
                acum_prob_n[n] += resultado['probabilidades_n'][n]

            if capacidad_actual == cola_graficos and porcentaje == 0.75 and rep == 0:
                datos_hist_n = {k: v for k, v in resultado['probabilidades_n'].items()}
                lista_tiempos_sistema_grafico = resultado['tiempos_sistema']
                lista_tiempos_cola_grafico = resultado['tiempos_cola']

        prom_en_cola = acum_en_cola / repeticiones
        prom_en_sistema = acum_en_sistema / repeticiones
        prom_espera_cola = acum_espera_cola / repeticiones
        prom_espera_sistema = acum_espera_sistema / repeticiones
        prom_utilizacion = acum_utilizacion / repeticiones
        prom_denegacion = acum_denegacion / repeticiones

        print(f"\n>>> Lambda = {lambda_arribo:.2f} ({porcentaje*100:.0f}% de mu) | rho teorico = {rho_teorico:.2f}")
        print(f"  Clientes promedio en cola (Lq):     {prom_en_cola:.2f}")
        print(f"  Clientes promedio en sistema (L):   {prom_en_sistema:.2f}")
        print(f"  Tiempo promedio en cola (Wq):       {prom_espera_cola:.4f}")
        print(f"  Tiempo promedio en sistema (W):     {prom_espera_sistema:.4f}")
        print(f"  Utilización del servidor:           {prom_utilizacion:.2%}")
        print(f"  Probabilidad Denegación Servicio:   {prom_denegacion:.2%}")
        
    
        string_probs = ", ".join([f"P({n})={acum_prob_n[n]/repeticiones:.2%}" for n in range(min(3, capacidad_actual+1))])
        print(f"  Probabilidad de n clientes en cola: {string_probs} ...")


if datos_hist_n:
    
    #Gráfico de barras horizontales
    plt.figure(figsize=(6, 5))
    clientes = list(datos_hist_n.keys())
    probabilidades = list(datos_hist_n.values())
    
    # Calcular acumulada
    acumulada_n = []
    suma_temp = 0
    for p in probabilidades:
        suma_temp += p
        acumulada_n.append(suma_temp)
        
    plt.barh(clientes, probabilidades, label='Discreta', height=0.4)
    plt.plot(acumulada_n, clientes, marker='o', label='Acumulada', linewidth=2)
    
    plt.gca().invert_yaxis()  # Invertir eje Y para que el 0 quede arriba
    plt.title('Probabilidad Discreta', fontsize=14, pad=15)
    plt.xlabel('Probabilidad')
    plt.ylabel('Clientes')
    plt.xlim(-0.05, 1.25)
    plt.yticks(clientes)
    plt.legend(loc='upper right', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False)
    plt.tight_layout()
    plt.show()

    # Grafico 2 de tiempo
    plt.figure(figsize=(6, 5))
    
    # Ordenar datos para armar la función de probabilidad acumulada
    if lista_tiempos_sistema_grafico and lista_tiempos_cola_grafico:
        ts_ordenados = sorted(lista_tiempos_sistema_grafico)
        tq_ordenados = sorted(lista_tiempos_cola_grafico)
        
       
        pasos_grafico = 10
        indices_ts = [int(i * (len(ts_ordenados) - 1) / (pasos_grafico - 1)) for i in range(pasos_grafico)]
        indices_tq = [int(i * (len(tq_ordenados) - 1) / (pasos_grafico - 1)) for i in range(pasos_grafico)]
        
        puntos_x_ts = [ts_ordenados[idx] for idx in indices_ts]
        puntos_y_ts = [indices_ts[i] / len(ts_ordenados) for i in range(pasos_grafico)]
        
        puntos_x_tq = [tq_ordenados[idx] for idx in indices_tq]
        puntos_y_tq = [indices_tq[i] / len(tq_ordenados) for i in range(pasos_grafico)]
        
        plt.plot(puntos_x_ts, puntos_y_ts, marker='o', label='Tiempo en sistema', linewidth=2)
        plt.plot(puntos_x_tq, puntos_y_tq, marker='d', label='Tiempo en cola', linewidth=1.5)
        
        plt.title('Probabilidad Basada en el Tiempo', fontsize=14, pad=15)
        plt.xlabel('Tiempo Transcurrido')
        plt.ylabel('Probabilidad Acumulada')
        plt.ylim(-0.05, 1.25)
        plt.xticks(rotation=45)
        plt.legend(loc='upper right', bbox_to_anchor=(0.5, -0.2), ncol=2, frameon=False)
        plt.tight_layout()
        plt.show()