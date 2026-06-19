import random
import math

longitud_sucesion = 0
while longitud_sucesion <=0:
    longitud_sucesion = int(input("Ingrese la cantidad de números a generar: "))

sucesion = []
parametro = float(input("Ingrese el lambda: "))

for _ in range(longitud_sucesion):
    x = 0
    tr = random.random()
    b = math.exp(-parametro)
    while tr >= b:
        x += 1
        tr = tr * random.random()

    sucesion.append(x)

#print(sucesion)

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import math

valores_unicos, conteos = np.unique(sucesion, return_counts=True)
frecuencias_relativas = conteos / longitud_sucesion

plt.bar(valores_unicos, frecuencias_relativas, color='skyblue', edgecolor='black', alpha=0.7, label='Frecuencia Resultante')

x_teorico = np.arange(0, max(sucesion) + 1)
pmf_teorica = stats.poisson.pmf(x_teorico, mu=parametro)
plt.plot(x_teorico, pmf_teorica, 'ro--', lw=2, label='PMF Teórica Poisson')

plt.title(f'Distribución de Poisson - Lambda: {parametro} - {longitud_sucesion} números generados')
plt.xlabel('Cantidad de eventos')
plt.ylabel('Probabilidad / Frecuencia Relativa')
plt.legend()
plt.show()


def test_chi_cuadrado(sucesion_numeros, tipo, alfa=0.05):
    print(f" \n  PRUEBA DE CHI-CUADRADO ({tipo})")

    k = 10
    longitud_sucesion = len(sucesion_numeros)
    intervalos = np.linspace(0.0, 1.0, k + 1)  # Define los intervalos
    observados, _ = np.histogram(sucesion_numeros, bins=intervalos)  # Cuenta las frecuencias observadas
    esperados = longitud_sucesion / k  # Calculo de la frecuencia esperada

    chi_cuadrado_tabla = [((o_i - esperados) ** 2) / esperados for o_i in observados]
    estadistico_chi2 = sum(chi_cuadrado_tabla)

    grados_libertad = k - 1
    p_valor = 1 - stats.chi2.cdf(estadistico_chi2, grados_libertad)

    print(
        f"\nCantidad de números evaluados (n): {longitud_sucesion} \nIntervalos: {k} \nFrecuencia esperada por intervalo: {esperados}")
    print("\n")
    print("Distribución de los números en los intervalos:")
    for i in range(k):
        print(f" Intervalo [{intervalos[i]:.1f} - {intervalos[i + 1]:.1f}): Observados = {observados[i]}")
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


def test_general(eTeorica, vTeorica):
    #calculo de media
    sumaMedia = 0
    for n in sucesion:
        sumaMedia += n
    esperanza = sumaMedia / longitud_sucesion

    dif_abs_e = abs(esperanza - eTeorica)

    print("ESPERANZA:")
    print("Teórica: ", eTeorica)
    print("Obtenida: ", esperanza)
    print("Diferencia absoluta: ", dif_abs_e)
    margen_permitido_e = 1.96 * math.sqrt(vTeorica) / math.sqrt(longitud_sucesion)
    print("Margen permitido: ", margen_permitido_e)
    print("Veredicto:")
    if dif_abs_e <= margen_permitido_e:
        print("LA ESPERANZA PASA EL TEST")
    else:
        print("LA ESPERANZA NO PASA EL TEST")

    #calculo de varianza
    sumaVarianza = 0
    for n in sucesion:
        sumaVarianza = sumaVarianza + (n - esperanza) ** 2
    varianza = sumaVarianza / (longitud_sucesion - 1)

    errorRelV = abs((varianza - vTeorica) / vTeorica)

    print("VARIANZA:")
    print("Teórica: ", vTeorica)
    print("Obtenida: ", varianza)
    print("Error relativo: ", errorRelV)
    margen_permitido_v = 0.05
    print("Margen permitido: ", margen_permitido_v)
    print("Veredicto:")
    if errorRelV <= margen_permitido_v:
        print("LA VARIANZA PASA EL TEST")
    else:
        print("LA VARIANZA NO PASA EL TEST")

eTeorica = parametro
vTeorica = parametro
test_general(eTeorica, vTeorica)