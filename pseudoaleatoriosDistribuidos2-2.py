import sys
import random
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import math

print(sys.argv)
# Valida que los argumentos sean los correctos
if (len(sys.argv) != 5 or sys.argv[1] != "-d" or sys.argv[3] != "-n"):
  print("Parámetros Incorrectos")
  sys.exit(1)

tipo_distribucion = str(sys.argv[2])
longitud_sucesion = int(sys.argv[4])

sucesion = []
sucesion_real = []
sucesion_binario = []


def generador_Mersenne_Twister(seed):
  global sucesion_binario
  while seed <= 0:
    seed = int(input("Ingresar la semilla: "))
    if seed <= 0:
      print("La semilla debe ser un valor entero mayor a 0")
  
  random.seed(seed)

  m_mt = pow(2,32)

  for _ in range(0, longitud_sucesion):
    numero_entero = random.getrandbits(32)
    sucesion.append(numero_entero)

    numero_real = numero_entero / m_mt
    sucesion_real.append(numero_real)
  
  sucesion_binario = entero_a_binario(sucesion, 32)

  return seed


def dist_uniforme():
    a = float(input("Ingrese el valor mínimo del intervalo (a): "))
    b = a
    while b <= a:
        b = float(input("Ingrese el valor máximo del intervalo (b, debe ser mayor que a): "))
    for _ in range(longitud_sucesion):
      sucesion.append(a+(b-a)*random.random())
    plt.hist(sucesion, bins=15, density=True, color='skyblue', edgecolor='black', alpha=0.7)
    
    altura_teorica = 1 / (b - a)
    plt.hlines(altura_teorica, a, b, colors='red', linestyles='dashed', 
    label='Curva Teórica FDP')
    
    plt.title('Distribución Uniforme')
    plt.xlabel('Valor generado')
    plt.ylabel('Densidad')
    plt.legend()
    plt.show()


def dist_exponencial():
  esperanza = 0
  while esperanza <= 0:
    esperanza = float(input("Ingrese el valor la esperanza: "))
  for _ in range(longitud_sucesion):
    sucesion.append(-esperanza*math.log(random.random()))
  
  plt.hist(sucesion, bins=15, density=True, color='skyblue', edgecolor='black', alpha=0.7)

  x = np.linspace(0, max(sucesion), 1000)
  pdf_teorica = stats.expon.pdf(x, scale=esperanza)
  plt.plot(x, pdf_teorica, 'r-', lw=2, label='PDF Teórica')

  plt.title('Distribución Exponencial')
  plt.xlabel('Valor generado')
  plt.ylabel('Densidad')
  plt.legend()
  plt.show()


def test_chi_cuadrado(sucesion_numeros, tipo, alfa=0.05):  
  print(f" \n  PRUEBA DE CHI-CUADRADO ({tipo})")
    
  k = 10
  longitud_sucesion = len(sucesion_numeros)
  intervalos = np.linspace(0.0, 1.0, k + 1) # Define los intervalos
  observados, _ = np.histogram(sucesion_numeros, bins=intervalos) # Cuenta las frecuencias observadas
  esperados = longitud_sucesion / k   # Calculo de la frecuencia esperada
    
  chi_cuadrado_tabla = [((o_i - esperados) ** 2) / esperados for o_i in observados]
  estadistico_chi2 = sum(chi_cuadrado_tabla)
    
  grados_libertad = k - 1
  p_valor = 1 - stats.chi2.cdf(estadistico_chi2, grados_libertad)

  print(f"\nCantidad de números evaluados (n): {longitud_sucesion} \nIntervalos: {k} \nFrecuencia esperada por intervalo: {esperados}")
  print("\n")
  print("Distribución de los números en los intervalos:")
  for i in range(k):
    print(f" Intervalo [{intervalos[i]:.1f} - {intervalos[i+1]:.1f}): Observados = {observados[i]}")
  print("\n")
  print(f"Estadístico Chi-cuadrado calculado (X²): {estadistico_chi2:.4f}")
  print(f"p-valor obtenido: {p_valor:.6f}")
  print(f"Nivel de significancia (alfa): {alfa}")
  print("\n")
    

  if p_valor < alfa:
    print("SE RECHAZA H0 (Los números NO son uniformes)")
    print("El generador NO pasa la prueba de uniformidad")
  else:
    print("NO SE RECHAZA H0 (Los números son uniformes)")
    print("El generador PASA la prueba de uniformidad")


def test_frecuencia_monobit(cadena):
  n = len(cadena)
  print("----------TEST FRECUENCIA MONOBIT---------------")
  print("Funciona mejor en cadenas de más de 100 bits. La cadena tiene ", n, " bits.")

  cant_unos = cadena.count('1')
  cant_ceros = n - cant_unos
  suma_monobit = cant_unos - cant_ceros

  estadistico_prueba = abs(suma_monobit) / math.sqrt(n)

  p_value =   math.erfc(estadistico_prueba / math.sqrt(2))

  if p_value < 0.01:
    print("El generador NO PASA la prueba de frecuencia monobit.")
  else:
    print("El generador PASA la prueba de frecuencia monobit.")
  
  return cant_unos / n
  


def test_frecuencia_bloque(cadena):
  n = len(cadena)

  print("----------TEST FRECUENCIA DENTRO DEL BLOQUE---------------")
  print("Funciona mejor en cadenas de más de 100 bits. La cadena tiene ", n, " bits.")

  cant_bloques_max = min(99, n // 20)

  if cant_bloques_max < 2:
    print("La cadena es demasiado corta para hacer un test válido.")

  else:
    cant_bloques = random.randint(2, cant_bloques_max)
    tam_bloque = n // cant_bloques
    print("Se usarán ", cant_bloques, " bloques de ", tam_bloque, " bits cada uno.")

    proporciones = [ # Array con la proporcion de 1s en cada bloque
      cadena[i:i + tam_bloque].count('1') / tam_bloque 
      for i in range(0, cant_bloques * tam_bloque, tam_bloque)
      ]
    suma_desvios = sum((pi - 0.5)**2 for pi in proporciones)
    chi_sq_obs = 4 * tam_bloque * suma_desvios

    p_value = stats.chi2.sf(chi_sq_obs, cant_bloques)

    if p_value < 0.01:
      print("El generador NO PASA la prueba de frecuencia de bloque.")
    else:
      print("El generador PASA la prueba de frecuencia de bloque.")


def test_rachas(cadena, pi):
  n = len(cadena)
  print("----------TEST DE RACHAS---------------")
  print("Funciona mejor en cadenas de más de 100 bits. La cadena tiene ", n, " bits.")
  print()
  print("PRE-TEST:")
  if abs(pi - 0.5) >= 2 / math.sqrt(n):
        print("NO PASA pre-test -> NO PASA el test de rachas")
  else:
    print("PASA pre-test")
    print("TEST DE RACHAS")
    
    saltos = 0

    for i in range(n-1):
      if cadena[i] != cadena[i+1]:
        saltos += 1
    
    vn_obs = saltos + 1

    num = abs(vn_obs - 2 * n * pi * (1 - pi))
    den = 2 * math.sqrt(2 * n) * pi * (1 - pi)
    p_value = math.erfc(num / den)

    if p_value < 0.01:
      print("El generador NO PASA la prueba de rachas.")
    else:
      print("El generador PASA la prueba de rachas.")  


def entero_a_binario(lista_enteros, cant_bits):
  return "".join(f"{num:0{cant_bits}b}" for num in lista_enteros)


# PROGRAMA PRINCIPAL 
if tipo_distribucion == "u": #uniforme
  dist_uniforme()
  test_chi_cuadrado(sucesion)
  print(sucesion)
  
elif tipo_distribucion == "e": #exponencial
  dist_exponencial()
elif tipo_distribucion == "n": #normal
  seed = generador_Mersenne_Twister(seed)
elif tipo_distribucion == "b": #binomial
  pass
elif tipo_distribucion == "p": #poisson
  pass
elif tipo_distribucion == "d": #empírica discreta
  pass
'''
test_chi_cuadrado(sucesion_real, tipo_generador)

pi_monobit = test_frecuencia_monobit(sucesion_binario)

test_frecuencia_bloque(sucesion_binario)

test_rachas(sucesion_binario, pi_monobit)

# Test numeros aleatorios
aleatorios_enteros = [int(i * (2**13)) for i in numeros_aleatorios] # Se sacrifica precisión para obtener un resultado no sesgado por el espacio de valores sobrantes.
aleatorios_binarios = entero_a_binario(aleatorios_enteros, 13)
test_chi_cuadrado(numeros_aleatorios, "random.org")
pi_monobit = test_frecuencia_monobit(aleatorios_binarios)
test_frecuencia_bloque(aleatorios_binarios)
test_rachas(aleatorios_binarios, pi_monobit)

plt.figure(figsize=(10,5))
plt.suptitle(f"{longitud_sucesion} números generados")
generacion = list(range(1, longitud_sucesion + 1))
plt.title("Números Pseudo-Aleatorios")
plt.xlabel("n")
plt.ylabel("res (Número generado)")
plt.scatter(generacion, sucesion, color='red', s=10, label='Número generado')

plt.figure(figsize=(10,5))
plt.suptitle("Números Aleatorio - Generador random.org")
plt.xlabel("n")
plt.ylabel("res (Número Obtenido)")

if longitud_sucesion <= len(numeros_aleatorios):
  numeros_a_graficar = numeros_aleatorios[:longitud_sucesion]
  eje_x_random = list(range(1, longitud_sucesion + 1))
else:
  numeros_a_graficar = numeros_aleatorios
  eje_x_random = list(range(1, len(numeros_aleatorios) + 1))

plt.scatter(eje_x_random, numeros_a_graficar, color='red', s=10, label='Número Obtenido')
plt.legend()

plt.tight_layout()
plt.subplots_adjust(hspace=0.5, top=0.9)
plt.show()
'''