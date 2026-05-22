import sys 
import statistics
import math
from cProfile import label

import matplotlib.pyplot as plt
import random



print(sys.argv)
# Valida que los argumentos sean los correctos
if (len(sys.argv) != 9 or sys.argv[1] != "-c" or sys.argv[3] != "-n" or sys.argv[5] != "-s" or sys.argv[7] != "-a"):
  print("Parámetros Incorrectos")
  sys.exit(1)

tiradas = int(sys.argv[2])
corridas = int(sys.argv[4])
estrategia =  str(sys.argv[6])
tipo_capital = str(sys.argv[8])

frec_rel = [] # Porcentaje que representa el numero elejido frente a los que ssalieron en cada tirada
todos_los_numeros = []
capitales = []
fibonacci = []
monto_base = 10

# Valores teóricos esperados
fr_esperada = 18/37 #cantidad de numeros pares (sin el 0)/cantidad de numeros

    
def estrategia_dalembert(resultado, apuesta):
  if resultado:  # Si gana la tirada, aumenta su capital y disminuye el monto de la proxima apuesta en 1 unidad
    nueva_apuesta = apuesta - monto_base
    if apuesta < monto_base:  # El monto de apuesta no puede ser menor al monto base
      apuesta = monto_base
  else: # Si pierde se aumenta la apuesta en una unidad
    nueva_apuesta = apuesta + monto_base

  return (nueva_apuesta)


def estrategia_martingala(resultado_anterior, apuesta_anterior):
  if resultado_anterior: # Si acaba de ganar, se reinicia a la apuesta inicial
    return(monto_base)
  else: # Si acaba de perder, se duplica la apuesta
    nueva_apuesta = apuesta_anterior*2
    return(nueva_apuesta)


def calcular_fibonacci(indice):
  nuevo = fibonacci[indice] + fibonacci[indice-1]
  fibonacci.append(nuevo)


def estrategia_fibonacci(resultado, indice_fibonacci):
  if (indice_fibonacci + 1) >= len(fibonacci):
    calcular_fibonacci(indice_fibonacci)  
  
  if resultado: 
    if indice_fibonacci < 2:
      indice_fibonacci = 0
    else: 
      indice_fibonacci -= 2
  else:
    indice_fibonacci += 1
    
  nueva_apuesta = fibonacci[indice_fibonacci]
  return (nueva_apuesta, indice_fibonacci)


def estrategia_paroli(resultado_anterior, apuesta_anterior, tipo_capital, racha, capital=0):
  if resultado_anterior: # Si acaba de ganar, se duplica la apuesta
    nueva_apuesta = apuesta_anterior*2
    racha += 1
    if racha == 3:
        racha = 0
        nueva_apuesta = monto_base
    if tipo_capital == 'f': # Cuando el capital es finito, la apuesta está restringida al capital disponible
      return(nueva_apuesta if capital >= nueva_apuesta else capital, racha)
    else: # Cuando el capital es infinito, la apuesta no está restringida
      return(nueva_apuesta, racha)
  else: # Si antes perdió, se reinicia a la apuesta inicial
    racha = 0
    return(monto_base, racha)


def tirada_ruleta(capital=0):
  # Números obtenidos en las tiradas de la ruleta
  numeros = []

  # Listas provisionales
  frec_rel_prov = [] 
  capital_prov = []

  # Inicialización de variables
  capital_actual = capital
  capital_prov.append(capital_actual)
  apuesta = monto_base
  racha_paroli = 0
  indice_fibonacci = 0
  LIMITE_APUESTA = 5000

  for i in range (1, tiradas+1):
    resultado = random.randint(0,36)
    numeros.append(resultado)

    if resultado % 2 == 0 and resultado != 0:
      gano = True
      capital_actual = capital_actual + apuesta
      capital_prov.append(capital_actual)
    else:
      gano = False
      capital_actual = capital_actual - apuesta
      capital_prov.append(capital_actual)


    if estrategia == "m":
      apuesta = estrategia_martingala(gano, apuesta) 
   
    elif estrategia == "d":
      apuesta = estrategia_dalembert(gano, apuesta)
      
    elif estrategia == "f":
      apuesta, indice_fibonacci = estrategia_fibonacci(gano, indice_fibonacci)
    
    elif estrategia == "o":
        apuesta, racha_paroli = estrategia_paroli(gano, apuesta, tipo_capital, racha_paroli, capital_actual)
    
    if tipo_capital == "i":
     apuesta = min(apuesta, LIMITE_APUESTA)

    if tipo_capital == 'f': # Cuando el capital es finito, la apuesta está restringida al capital disponible y si no alcanza hace all-in
      apuesta = apuesta if capital_actual >= apuesta else capital_actual

  # Calculo de medidas
    fa = len([n for n in numeros if n % 2 == 0 and n != 0])
    frec_rel_prov.append(fa/i)
    
    if tipo_capital == 'f' and capital_actual <= 0:
      break

  frec_rel.append(frec_rel_prov)
  capitales.append(capital_prov)

  print(numeros)
  print("CAPITALES:")
  print(capitales)
  return (capital_actual)


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
# Cantidad de corridas de la ruleta 
if tipo_capital == "f":
  capital_inicial = 0
  while capital_inicial <= 0:
    capital_inicial = int(input("Ingrese el monto deseado: "))
    if capital_inicial <= 0:
      print("El capital inicial debe ser mayor a 0")
else:
  capital_inicial = 0
  
if estrategia == "f":
  fibonacci.append(monto_base)
  fibonacci.append(monto_base) 

bancarrotas = 0

for _ in range (0, corridas):
  c = tirada_ruleta(capital_inicial)
  if c == 0 and tipo_capital == "f":
    bancarrotas += 1

# Frecuencia Relativa de Apuesta Favorable de la 1° corrida

plt.figure(figsize=(10,5))
plt.suptitle(f"{corridas} corridas simultaneas - {tiradas} tiradas - Estrategia {estrategia} - Capital {tipo_capital}")
plt.title("Frecuencias Relativas de Apuesta Favorable (1° corrida)")
plt.xlabel("n (número de tiradas)")
plt.ylabel("fr (frecuencia relativa)")
tiradas_x = list(range(1, len(frec_rel[0]) + 1))
plt.bar(tiradas_x, frec_rel[0], color='red', width=0.6, label='frsa obtenida')
plt.axhline(fr_esperada, linestyle = "--", color = "black", label=f"FR Esperada: {fr_esperada}")


# Evolución del capital de la 1° corrida

plt.figure(figsize=(10,5))
plt.suptitle(f"{corridas} corridas simultaneas - {tiradas} tiradas - Estrategia {estrategia} - Capital {tipo_capital}")
plt.title("Flujo de caja (1° corrida)")
plt.xlabel("n (número de tiradas)")
plt.ylabel("cc (cantidad de capital)")
plt.axhline(capital_inicial, linestyle = "--", color = "black", label=f"Capital Inicial: {capital_inicial}")
plt.plot(capitales[0], linewidth = 0.5)


# Evolución del capital de todas las corridas

plt.figure(figsize=(10,5))
plt.suptitle(f"{corridas} corridas simultaneas - {tiradas} tiradas - Estrategia {estrategia} - Capital {tipo_capital}")
plt.title("Flujo de caja de todas las corridas")
plt.xlabel("n (número de tiradas)")
plt.ylabel("cc (cantidad de capital)")
plt.axhline(capital_inicial, linestyle = "--", color = "black", label=f"Capital Inicial: {capital_inicial}")
plt.plot([], [], '', label = f"Bancarrota: {bancarrotas}")
plt.legend(loc = "upper right")

for i in range(0, corridas):
  plt.plot(capitales[i], linewidth = 0.5)
  if tipo_capital == 'f' and capitales[i][-1] == 0:
    ultimo_punto_x = len(capitales[i]) - 1
    ultimo_punto_y = capitales[i][-1]
    plt.scatter(ultimo_punto_x, ultimo_punto_y, color='red', s=5, zorder=3)



plt.tight_layout()
plt.subplots_adjust(hspace=0.5, top=0.9)
plt.show()
