import sys
import random
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

print(sys.argv)
# Valida que los argumentos sean los correctos
if (len(sys.argv) != 5 or sys.argv[1] != "-g" or sys.argv[3] != "-n"):
  print("Parámetros Incorrectos")
  sys.exit(1)

tipo_generador = str(sys.argv[2])
longitud_sucesion = int(sys.argv[4])

sucesion = []
seed = 0

def generador_GCL(seed):
  
  mGCL = pow(2,32) 
  while seed <= 0 or seed >= mGCL:
      seed = int(input("Ingresar la semilla: "))
      if seed <= 0 or seed >= mGCL:
          print("La semilla debe ser un valor entero entre 0 y 4.294.967.296")
  sucesion.append(seed)

  if tipo_generador == "GCL":
    a = random.randint(0,mGCL-1 // 4) * 4 + 1  
    c = random.randint(0,mGCL-1)
    c = c | 1 # Fuerza que sea impar
    for i in range(0,longitud_sucesion):
        sucesion.append((a*sucesion[-1]+c) % mGCL)


  print("a utilizado = " + str(a))
  print("c utilizado = " + str(c))
  print("m utilizado = " + str(mGCL))
  print("Los " + str(longitud_sucesion) + " generados son: ")
  print(sucesion[1:])
  
  return seed


valores = []

def generador_CM(seed):  # CM = Cuadrados Medios
    
  while seed <= 0 or len(str(seed)) != 4:
    seed = int(input("Ingresar la semilla: "))
    if seed <= 0 or len(str(seed)) != 4:
      print("La semilla debe ser un valor entero mayor a 0 y de 4 dígitos")
  
    
  seed_entero = int(seed)
  sucesion.append(seed_entero)
  nueva_semilla = seed_entero

  for _ in range(0, longitud_sucesion):
    
    valor = nueva_semilla ** 2
    valor_str = str(valor)
        
    if len(valor_str) != 8:
      valor_str = valor_str.zfill(8)

    valores.append(int(valor_str))    
    centro = valor_str[2:6]
    nueva_semilla = int(centro)

    sucesion.append(nueva_semilla)

  
  print("Valores: ", valores)
  
  print("Los " + str(longitud_sucesion) + " generados son: ")
  print(sucesion[1:])
  return seed 


def generador_Mersenne_Twister(seed):
  
  while seed <= 0:
    seed = int(input("Ingresar la semilla: "))
    if seed <= 0:
      print("La semilla debe ser un valor entero mayor a 0")
  
  random.seed(seed)
  sucesion.append(seed)

  for _ in range(0, longitud_sucesion):
    sucesion.append(random.random())
  

  print("Los " + str(longitud_sucesion) + " generados son: ")
  print(sucesion[1:])
  return seed


def test_chi_cuadrado(sucesion_numeros, tipo, alfa=0.05):
   
    datos_originales = sucesion_numeros[1:] # numeros generados sin la semilla
    
    # Normalización de los datos
    if tipo == "GCL":
      mGCL = pow(2, 32)
      datos = [x / mGCL for x in datos_originales]
        
    elif tipo == "CM":
      datos = [x / 10000 for x in datos_originales]
        
    else: # Solo para generador MT
      datos = datos_originales 

    
    print(f" \n  PRUEBA DE CHI-CUADRADO ({tipo})")
    
    k = 10
    intervalos = np.linspace(0.0, 1.0, k + 1) # Define los intervalos
    observados, _ = np.histogram(datos, bins=intervalos) # Cuenta las frecuencias observadas
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


# PROGRAMA PRINCIPAL 
if tipo_generador == "GCL":
  seed = generador_GCL(seed) 
elif tipo_generador == "CM":
  seed = generador_CM(seed)
elif tipo_generador == "MT":
  seed = generador_Mersenne_Twister(seed)


test_chi_cuadrado(sucesion, tipo_generador)

plt.figure(figsize=(10,5))
plt.suptitle(f"{longitud_sucesion} números generados - Generador {tipo_generador} - Semilla {seed}")
plt.title("Números generados")
plt.xlabel("n")
plt.ylabel("res (Número generado)")
generacion = list(range(1, longitud_sucesion + 1))
plt.scatter(generacion, sucesion[1:], color='red', s=10, label='Número generado')

plt.tight_layout()
plt.subplots_adjust(hspace=0.5, top=0.9)
plt.show()