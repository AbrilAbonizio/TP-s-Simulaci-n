import sys 
import statistics
import math
from cProfile import label

import matplotlib.pyplot as plt
import random


# Valida que los argumentos sean los correctos
if len(sys.argv) != 7 or sys.argv[1] != "-c" or sys.argv[3] != "-n" or sys.argv[5] != "-e" or sys.argv[7] != "-s" or sys.argv[9] != "-a":
  print("Parámetros Incorrectos")
  sys.exit(1)

tiradas = int(sys.argv[2])
corridas = int(sys.argv[4])
num_elegido = int(sys.argv[6])
estrategia =  str(sys.argv[8])
tipo_capital = str(sys.argv[10])


frec_abs = [] # Cantidad de veces que salió el número elegido por cada tirada
frec_rel = [] # Porcentaje que representa el numero elejido frente a los que ssalieron en cada tirada
promedios = [] # Valor promedio de todos los numeros por tirada
desv_estandar = []
varianzas = []
todos_los_numeros = []
capitales = []
apuesta = 10


# Valores teóricos esperados
fr_esperada = 1/37 #1/cantidad de numeros
prom_esperado = (0+36)/2 #(min + max)/2 
varianza_esperada = ((37*37)-1)/12 #((n*n)+1)/12
desv_estandar_esperado = math.sqrt(varianza_esperada)


    
def estrategia_dalembert(resultado, apuesta):
  
  if resultado:  # Si gana la tirada, aumenta su capital y disminuye el monto de la proxima apuesta en 1 unidad
    nueva_apuesta -= apuesta
  else:
    nueva_apuesta += apuesta

  return nueva_apuesta


def estrategia_martingala(apuesta_anterior, resultado_anterior, tipo_capital, capital=0):
  if resultado_anterior: # Si acaba de ganar, se reinicia a la apuesta inicial
    return(apuesta)
  else: # Si acaba de perder, se duplica la apuesta
    nueva_apuesta=apuesta_anterior*2


def estrategia_fibonacci(n, num_elegido, monto, tipo_capital, apuesta, contador, fibonacci, ganancias, frec_rel):
  if n != num_elegido:
    if tipo_capital == 'f':
      monto -= apuesta
      apuesta = fibonacci[-1] + fibonacci[-2]
      fibonacci.append(apuesta)
      bancarrota = 1 if monto <= 0 else 0
    else: 
      ganancias = ganancias - apuesta
      apuesta = fibonacci[-1] + fibonacci[-2]
      fibonacci.append(apuesta)
      bancarrota = 0
  else:
    if tipo_capital == 'f':
      monto += apuesta*36
      if len(fibonacci) > 3:
        apuesta = fibonacci[-3]
      fibonacci.append(apuesta)
      frec_rel[contador] += 1
    else:
      ganancias = ganancias + apuesta*36
      if len(fibonacci)>3:
        apuesta = fibonacci[-3]
      fibonacci.append(apuesta)
    bancarrota = 0 
  
  return monto, apuesta, ganancias, bancarrota, fibonacci


def estrategia_paroli(apuesta_anterior, resultado_anterior, tipo_capital, capital=0):
  if resultado_anterior: # Si acaba de ganar, se duplica la apuesta
    nueva_apuesta=apuesta_anterior*2
    if tipo_capital == 'f': # Cuando el capital es finito, la apuesta está restringida al capital disponible
      return(nueva_apuesta if capital >= nueva_apuesta else capital)
    else: # Cuando el capital es infinito, la apuesta no está restringida
      return(nueva_apuesta)
  else: # Si antes perdió, se reinicia a la apuesta inicial
    return(apuesta)


def tirada_ruleta(capital=0):
  
  # Números obtenidos en las tiradas de la ruleta
  numeros = []

  # Listas provisionales
  frec_abs_prov= []
  frec_rel_prov = [] 
  prom_prov = [] 
  desv_prov = [] 
  var_prov = []
  capital_prov = []
  
  
  for i in range (1, tiradas+1):
    resultado = numeros.append(random.randint(0,36))
    if resultado == num_elegido:
      gano = True
      capital_actual = capital_actual + apuesta
      capital_prov.append(capital_actual)
    else:
      gano = False
      capital_actual = capital_actual - apuesta
      capital_prov.append(capital_actual)

    if estrategia == "m":
      apuesta = estrategia_martingala("apuesta anterior", gano, tipo_capital, capital_actual) 
   
    elif estrategia == "d":
      apuesta = estrategia_dalembert(gano, apuesta)
      
    elif estrategia == "f":
      estrategia_fibonacci() #faltan parametros
    
    elif estrategia == "o":
      apuesta = estrategia_paroli("apuesta anterior", gano, tipo_capital, capital_actual) #faltan parametros
    
    if tipo_capital == 'f': # Cuando el capital es finito, la apuesta está restringida al capital disponible y si no alcanza hace all-in
      apuesta = apuesta if capital_actual >= apuesta else capital_actual

    resultado = numeros.append(random.randint(0,36))
    if resultado == num_elegido:
      gano = True
      capital_actual = capital_actual + apuesta
      capital_prov.append(capital_actual)
    else:
      gano = False
      capital_actual = capital_actual - apuesta
      capital_prov.append(capital_actual)

    if tipo_capital == 'f' and capital_actual <=0:
      break


  # Calculo de medidas
    fa = numeros.count(num_elegido)
    frec_abs_prov.append(fa)
    frec_rel_prov.append(fa/i)
    prom_prov.append(statistics.mean(numeros))
    
    if len(numeros) > 1:
      desv_prov.append(statistics.stdev(numeros))
      var_prov.append(statistics.variance(numeros))
    else:
      # En la primera tirada, el desvío es 0
      desv_prov.append(0.0) 
      var_prov.append(0.0)
  
  frec_abs.append(frec_abs_prov)
  frec_rel.append(frec_rel_prov)
  promedios.append(prom_prov)
  desv_estandar.append(desv_prov)
  varianzas.append(var_prov)
  todos_los_numeros.append(numeros)
  capitales.append(capital_prov)


rachas_general = []
def calcular_rachas(lista_numeros, elegido):
  for corrida in lista_numeros:
      rachas_corrida = []
      contador = 0
      ultimo_es_elegido = False
      for tirada in range(len(corrida)):
        if corrida[tirada] == elegido:
          rachas_corrida.append(contador)
          contador = 0  # Reseteamos al encontrar el número
        else:
          contador += 1
          if tirada == len(corrida)-1:
              rachas_corrida.append(contador)
      rachas_general.append(rachas_corrida)


# Programa principal
if (num_elegido<0 or num_elegido>36):
  print ("El numero elegido debe estar entre 0 y 36")
else:
  # Cantidad de corridas de la ruleta 
  if tipo_capital == "f":
    capital_inicial = int(input("Ingrese el monto deseado: "))
  for _ in range (0, corridas):
    tirada_ruleta(capital_inicial)
    


#fig, axes = plt.subplots(2, 2, figsize = (12,10)) # --> para mostrar los 4 graficos en una misma ventana
                    # 2 filas 2 columnas
#fig.suptitle(f"{corridas} corridas simultaneas - {tiradas} tiradas - número {num_elegido}")


# Gráfico de Frecuencias Relativas
# Cálculo del promedio entre corridas
frecuencias_general = []
for i in range(tiradas):
    suma = 0
    for j in range(corridas):
        suma = frec_rel[j][i] + suma
    frecuencias_general.append(suma/corridas)
#   Gráfico
plt.figure(figsize=(10,5))
plt.suptitle(f"{corridas} corridas simultaneas - {tiradas} tiradas - número {num_elegido}")
plt.title("Frecuencias Relativas")
plt.xlabel("n (número de tiradas)")
plt.ylabel("fr (frecuencias relativas)")
plt.axhline(fr_esperada, linestyle = "--", color = "black", label=f"Frec. Rel. Esperada: {fr_esperada}")

for i in range (corridas):
  plt.plot(frec_rel[i], linewidth = 0.5 )  # Dibuja el gráfico

plt.plot(frecuencias_general, linewidth=3, label = "Promedio de todas las corridas", color="red")
plt.legend()


# Gráfico de Promedios
# Cálculo del promedio entre corridas
promedios_general = []
for i in range(tiradas):
    suma = 0
    for j in range(corridas):
        suma = promedios[j][i] + suma
    promedios_general.append(suma/corridas)
#   Gráfico
plt.figure(figsize=(10,5))
plt.suptitle(f"{corridas} corridas simultaneas - {tiradas} tiradas - número {num_elegido}")
plt.title("Promedios")
plt.xlabel("n (número de tiradas)")
plt.ylabel("vp (valores promedios)")
plt.axhline(prom_esperado, linestyle = "--", color = "black", label=f"Promedio Esperado: {prom_esperado}")

for i in range (corridas):
  plt.plot(promedios[i], linewidth = 0.5)  # Dibuja el gráfico

plt.plot(promedios_general, linewidth=3, label = "Promedio de todas las corridas", color="red")
plt.legend()


# Gráfico del Desvío Estándar
# Cálculo del promedio entre corridas
desv_estandar_general = []
for i in range(tiradas):
    suma = 0
    for j in range(corridas):
        suma = desv_estandar[j][i] + suma
    desv_estandar_general.append(suma/corridas)
#   Gráfico
plt.figure(figsize=(10,5))
plt.suptitle(f"{corridas} corridas simultaneas - {tiradas} tiradas - número {num_elegido}")
plt.title("Desvío Estándar")
plt.xlabel("n (número de tiradas)")
plt.ylabel("vd (valor del desvío)")
plt.axhline(desv_estandar_esperado, linestyle = "--", color = "black", label=f"Desv. Estándar Esperado: {desv_estandar_esperado}")

for i in range (corridas):
  plt.plot(desv_estandar[i], linewidth = 0.5)  # Dibuja el gráfico

plt.plot(desv_estandar_general, linewidth=3, label = "Promedio de todas las corridas", color="red")
plt.legend()


# Gráfico de la Varianza
# Cálculo del promedio entre corridas
varianza_general = []
for i in range(tiradas):
    suma = 0
    for j in range(corridas):
        suma = varianzas[j][i] + suma
    varianza_general.append(suma/corridas)
#   Gráfico
plt.figure(figsize=(10,5))
plt.suptitle(f"{corridas} corridas simultaneas - {tiradas} tiradas - número {num_elegido}")
plt.title("Varianza")
plt.xlabel("n (número de tiradas)")
plt.ylabel("vv (valor de la varianza)")
plt.axhline(varianza_esperada, linestyle = "--", color = "black", label=f"Varianza Esperada: {varianza_esperada}")

for i in range (corridas):
  plt.plot(varianzas[i], linewidth = 0.5)  # Dibuja el gráfico

plt.plot(varianza_general, linewidth=3, label = "Promedio de todas las corridas", color="red")
plt.legend()


#plt.subplots_adjust(hspace=0.5, top=0.9)

fig2, axes = plt.subplots(2, figsize = (12,10)) 
fig2.suptitle(f"{corridas} corridas simultaneas - {tiradas} tiradas - número {num_elegido}")


# Obtener las frecuencias absolutas finales de cada corrida
fa_finales = [frec_abs[i][-1] for i in range(corridas)]


# Calcular cuantas tiradas de ruleta hubo sin que saliera el número elegido
calcular_rachas(todos_los_numeros, num_elegido)
# Aplanar rachas
mis_rachas = [n for racha in rachas_general for n in racha]


# Grafico de barras (muestra cuantas veces salio el numero elegido en cada corrida)
axes[0].set_title("Gráfico de barras del número elegido")
axes[0].set_xlabel("Número de corrida")
axes[0].set_ylabel("Frecuencia Absoluta")
axes[0].bar(range(1, corridas + 1), fa_finales)
axes[0].axhline(tiradas * fr_esperada, linestyle="--", color="red", label=f"FA esperada ({tiradas/37:.2f})")
axes[0].set_xticks(range(1, corridas + 1, 5))  # muestra 1, 6, 11, 16...
axes[0].tick_params(axis='x', rotation=45)


# Histograma de rachas perdidas 
# (cuantas tiradas de ruleta hubo sin que salga el número elegido)

axes[1].set_title("Histograma de rachas perdidas")
axes[1].set_xlabel("Longitud de la racha (Tiradas sin ganar)")
axes[1].set_ylabel("Frecuencia (cuántas veces ocurrió)")
axes[1].hist(mis_rachas, bins=30, edgecolor= "black", color='skyblue' )
axes[1].set_xticks(range(0, int(max(mis_rachas)) + 20, 20))


plt.tight_layout()
plt.subplots_adjust(hspace=0.5, top=0.9)
plt.show()
