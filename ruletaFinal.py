import sys 
import statistics
import math
import matplotlib.pyplot as plt
import random


# Valida que los argumentos sean los correctos
if len(sys.argv) != 7 or sys.argv[1] != "-c" or sys.argv[3] != "-n" or sys.argv[5] != "-e":
  print("Parámetros Incorrectos")
  sys.exit(1)

tiradas = int(sys.argv[2])
corridas = int(sys.argv[4])
num_elegido = int(sys.argv[6])

frec_abs = [] # Cantidad de veces que salió el número elegido por cada tirada
frec_rel = [] # Porcentaje que representa el numero elejido frente a los que ssalieron en cada tirada
promedios = [] # Valor promedio de todos los numeros por tirada
desv_estandar = []
varianzas = []
todos_los_numeros = []

# Valores teóricos esperados
fr_esperada = 1/37 #1/cantidad de numeros
prom_esperado = (0+36)/2 #(min + max)/2 
varianza_esperada = ((37*37)-1)/12 #((n*n)+1)/12
desv_estandar_esperado = math.sqrt(varianza_esperada)


def tirada_ruleta():
  # Números obtenidos en las tiradas de la ruleta
  numeros = []

  # Listas provisionales
  frec_abs_prov= []
  frec_rel_prov = [] 
  prom_prov = [] 
  desv_prov = [] 
  var_prov = []
  
  for i in range (1, tiradas+1):
    numeros.append(random.randint(0,36))
  
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
  for _ in range (0, corridas):
    tirada_ruleta()


#fig, axes = plt.subplots(2, 2, figsize = (12,10)) # --> para mostrar los 4 graficos en una misma ventana
                    # 2 filas 2 columnas
#fig.suptitle(f"{corridas} corridas simultaneas - {tiradas} tiradas - número {num_elegido}")


# Gráfico de Frecuencias Relativas
plt.figure(figsize=(10,5))
plt.title("Frecuencias Relativas")
plt.xlabel("n (número de tiradas)")
plt.ylabel("fr (frecuencias relativas)")
plt.axhline(fr_esperada, linestyle = "--", color = "black", label=f"Frec. Rel. Esperada: {fr_esperada}")
#plt.legend(ncol=2)

for i in range (corridas):
  plt.plot(frec_rel[i], label = f"Corrida {i+1}", linewidth = 0.5 )  # Dibuja el gráfico


# Gráfico de Promedios
plt.figure(figsize=(10,5))
plt.title("Promedios")
plt.xlabel("n (número de tiradas)")
plt.ylabel("vp (valores promedios)")
plt.axhline(prom_esperado, linestyle = "--", color = "black", label=f"Promedio Esperado: {prom_esperado}")
#plt.legend(ncol=2)

for i in range (corridas):
  plt.plot(promedios[i], label = f"Corrida {i+1}", linewidth = 0.5)  # Dibuja el gráfico


# Gráfico del Desvío Estándar
plt.figure(figsize=(10,5))
plt.title("Desvío Estándar")
plt.xlabel("n (número de tiradas)")
plt.ylabel("vd (valor del desvío)")
plt.axhline(desv_estandar_esperado, linestyle = "--", color = "black", label=f"Desv. Estándar Esperado: {desv_estandar_esperado}")
#plt.legend(ncol=2)

for i in range (corridas):
  plt.plot(desv_estandar[i], label = f"Corrida {i+1}", linewidth = 0.5)  # Dibuja el gráfico


# Gráfico de la Varianza
plt.figure(figsize=(10,5))
plt.title("Varianza")
plt.xlabel("n (número de tiradas)")
plt.ylabel("vv (valor de la varianza)")
plt.axhline(varianza_esperada, linestyle = "--", color = "black", label=f"Varianza Esperada: {varianza_esperada}")
#plt.legend(ncol=2)

for i in range (corridas):
  plt.plot(varianzas[i], label = f"Corrida {i+1}", linewidth = 0.5)  # Dibuja el gráfico


#plt.subplots_adjust(hspace=0.5, top=0.9)

fig2, axes = plt.subplots(2, figsize = (12,10)) 
fig2.suptitle(f"{corridas} corridas simultaneas - {tiradas} tiradas - número {num_elegido}")


# Convertir a la lista de listas en una sola lista larga
lista_plana = [n for corrida in todos_los_numeros for n in corrida]


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

